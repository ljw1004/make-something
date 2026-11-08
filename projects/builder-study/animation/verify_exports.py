"""Decode selected loops and verify timing, registration and transparent edges."""
from pathlib import Path
import argparse
import json
import statistics
from PIL import Image, ImageChops, ImageStat

p = argparse.ArgumentParser()
p.add_argument('--input', required=True)
args = p.parse_args()
records = []
for path in sorted(Path(args.input).glob('*-manifest.json')):
    manifest = json.loads(path.read_text())
    identity = manifest['identity']
    loop = Image.open(path.parent/(identity+'-working.webp'))
    poster = Image.open(path.parent/(identity+'.webp'))
    if loop.info.get('loop') != 0:
        raise ValueError(identity+': WebP does not loop infinitely')
    if loop.size != tuple(manifest['animationSize']) or poster.size != tuple(manifest['posterSize']):
        raise ValueError(identity+': raster sizes differ from source record')
    aspect_error = abs(loop.width/loop.height-poster.width/poster.height)
    if aspect_error > .004:
        raise ValueError(identity+': animation/poster aspect mismatch')
    frames, durations = [], []
    for i in range(loop.n_frames):
        loop.seek(i)
        loop.load()
        durations.append(loop.info['duration'])
        rgba = loop.convert('RGBA')
        if not rgba.getchannel('A').getbbox():
            raise ValueError(identity+': empty decoded frame')
        if not manifest.get('cinematic'):
            box = rgba.getchannel('A').getbbox()
            if min(box[:2]) <= 0 or box[2] >= rgba.width or box[3] >= rgba.height:
                raise ValueError(identity+': decoded silhouette touches canvas')
        white = Image.new('RGBA', rgba.size, 'white')
        white.alpha_composite(rgba)
        frames.append(white.convert('RGB'))
    if sum(durations) != manifest['durationMs']:
        raise ValueError(identity+': duration differs from requested loop')
    def difference(a, b):
        return sum(ImageStat.Stat(ImageChops.difference(a, b)).rms)/3
    adjacent = [difference(a, b) for a, b in zip(frames, frames[1:])]
    seam = difference(frames[-1], frames[0])
    records.append(dict(identity=identity, decodedFrames=loop.n_frames, durationMs=sum(durations),
                        animationSize=loop.size, posterSize=poster.size, aspectError=aspect_error,
                        medianAdjacentDifference=statistics.median(adjacent), seamDifference=seam,
                        maximumAdjacentDifference=max(adjacent)))
print(json.dumps(records, indent=2))
