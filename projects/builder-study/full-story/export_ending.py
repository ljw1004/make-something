"""Export the native exchange as a one-shot WebP and settled static poster."""
from pathlib import Path
import argparse
import hashlib
import json
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument('--input', required=True)
p.add_argument('--output', required=True)
p.add_argument('--quality', type=int, default=88)
args = p.parse_args()
src, out = Path(args.input), Path(args.output)
manifest = json.loads((src / 'manifest.json').read_text())
if manifest['probe'] or manifest['changedSources']:
    raise ValueError('Export requires a complete render from unchanged sources')
frames = []
for index in range(manifest['frames']):
    rgba = Image.open(src / f'{index:04d}.png').convert('RGBA')
    if rgba.size != tuple(manifest['size']):
        raise ValueError(f'Unexpected frame dimensions: {index}')
    # Backgrounds are opaque scenes; holes in holdout masks reveal the white page.
    white = Image.new('RGBA', rgba.size, 'white')
    frames.append(Image.alpha_composite(white, rgba).convert('RGB'))
durations = [round((i + 1) * 1000 / manifest['fps']) - round(i * 1000 / manifest['fps'])
             for i in range(len(frames))]
out.mkdir(parents=True, exist_ok=True)
animation = out / 'ending-working.webp'
frames[0].save(animation, save_all=True, append_images=frames[1:], duration=durations,
               loop=1, quality=args.quality, method=4, minimize_size=False)
poster = out / 'ending.webp'
still=Image.open(src/'poster.png').convert('RGBA')
if still.size!=tuple(manifest['posterSize']):raise ValueError('Unexpected poster dimensions')
Image.alpha_composite(Image.new('RGBA',still.size,'white'),still).convert('RGB').save(poster, lossless=True, method=4)
record = dict(manifest, durationMs=sum(durations), loopCount=1, posterFrame=len(frames)-1,
              quality=args.quality, files={path.name: dict(bytes=path.stat().st_size,
              sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for path in (animation, poster)})
(out / 'ending-manifest.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({key: record[key] for key in ('durationMs', 'loopCount', 'posterFrame', 'files')}, indent=2))
