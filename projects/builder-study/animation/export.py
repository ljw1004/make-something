"""Pillow exporter: common alpha crop, registered poster and animated WebP."""
from pathlib import Path
import argparse
import hashlib
import json
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument('--input', required=True)
p.add_argument('--output', required=True)
p.add_argument('--css', type=float, default=350)
p.add_argument('--size', type=int, default=640)
p.add_argument('--quality', type=int, default=88)
p.add_argument('--allow-changed-sources', action='store_true', help='Disposable preview only; retains the changed-source warning')
args = p.parse_args()
src = Path(args.input)
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
manifest = json.loads((src / 'render-manifest.json').read_text())
if manifest['probe'] or (manifest['changedSources'] and not args.allow_changed_sources):
    raise ValueError('Only complete renders from frozen sources may be exported')
frames = [Image.open(src / f'{i:04d}.png').convert('RGBA') for i in range(manifest['frames'])]
boxes = [frame.getchannel('A').getbbox() for frame in frames]
if not all(boxes):
    raise ValueError('Empty animation frame')
res = manifest['resolution']
margin = 4
bounds = (max(0, min(b[0] for b in boxes) - margin), max(0, min(b[1] for b in boxes) - margin),
          min(res, max(b[2] for b in boxes) + margin), min(res, max(b[3] for b in boxes) + margin))
if manifest.get('cinematic'):
    bounds = (0, 0, res, res)
elif bounds[0] == 0 or bounds[1] == 0 or bounds[2] == res or bounds[3] == res:
    raise ValueError('Motion touches source canvas: enlarge the physical view')
w, h = bounds[2] - bounds[0], bounds[3] - bounds[1]
size = (round(w * args.size / max(w, h)), round(h * args.size / max(w, h)))
frames = [frame.crop(bounds).resize(size, Image.Resampling.LANCZOS) for frame in frames]
# Integer milliseconds alternate without introducing a cumulative duration drift.
durations = [round((i + 1) * 1000 / manifest['fps']) - round(i * 1000 / manifest['fps']) for i in range(len(frames))]
identity = manifest['identity']
animation = out / (identity + '-working.webp')
frames[0].save(animation, save_all=True, append_images=frames[1:], duration=durations, loop=0,
               quality=args.quality, method=4, minimize_size=False, exact=True)
poster = Image.open(src / 'poster.png').convert('RGBA')
ratio = poster.width / res
poster_bounds = tuple(round(v * ratio) for v in bounds)
poster_size = (round(w * args.css * 4 / max(w, h)), round(h * args.css * 4 / max(w, h)))
poster = poster.crop(poster_bounds).resize(poster_size, Image.Resampling.LANCZOS)
poster_file = out / (identity + '.webp')
poster.save(poster_file, lossless=True, method=4, exact=True)
record = dict(manifest, crop=bounds, animationSize=size, posterSize=poster_size, cssMax=args.css,
              durationMs=sum(durations), quality=args.quality,
              files={path.name: dict(bytes=path.stat().st_size, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
                     for path in (animation, poster_file)})
(out / (identity + '-manifest.json')).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({k: record[k] for k in ('identity', 'animationSize', 'posterSize', 'durationMs', 'files')}, indent=2))
