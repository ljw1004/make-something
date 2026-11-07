"""Add one screen panel, copying the other twelve frozen PNGs byte for byte."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
from PIL import Image, ImageChops, ImageDraw, ImageFont

parser = argparse.ArgumentParser()
parser.add_argument('--baseline', required=True)
parser.add_argument('--screen', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args()
baseline, screen, out = Path(args.baseline), Path(args.screen), Path(args.output)
if baseline.resolve() == out.resolve():
    raise ValueError('New output must not overwrite the frozen baseline')
out.mkdir(parents=True, exist_ok=True)
layout = json.loads((baseline/'layout.json').read_text())
manifest = json.loads((screen/'screen-manifest.json').read_text())
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
assert len(layout) == 13
assert digest(screen/manifest['file']) == manifest['sha256']
unchanged = []
for identity in layout:
    if identity != 'fair-in-the-air':
        shutil.copyfile(baseline/(identity+'.png'), out/(identity+'.png'))
        assert digest(baseline/(identity+'.png')) == digest(out/(identity+'.png'))
        unchanged.append(identity)

original = Image.open(baseline/'fair-in-the-air.png').convert('RGBA')
canvas = original.copy()
draw = ImageDraw.Draw(canvas)
frame = (20, 742, 664, 1184)
draw.rounded_rectangle(frame, radius=20, fill='#faf5e5', outline='#6f9697', width=3)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 42)
draw.text((42, 754), manifest['label'], font=font, fill='#294849')
detail = Image.open(screen/manifest['file']).convert('RGBA')
detail.thumbnail((602, 350), Image.Resampling.LANCZOS)
origin = (round(342-detail.width/2), round(990-detail.height/2))
canvas.alpha_composite(detail, origin)
# Check pixel equality beyond the newly reserved panel, including both existing views.
difference = ImageChops.difference(canvas, original)
difference.paste((0, 0, 0, 0), (frame[0], frame[1], frame[2]+1, frame[3]+1))
assert all(channel.getbbox() is None for channel in difference.split())
dest = out/'fair-in-the-air.png'
canvas.save(dest)
layout['fair-in-the-air'].update({'teachingRectPixels': [*origin, detail.width, detail.height],
                               'teachingLabel': manifest['label'], 'sha256': digest(dest)})
(out/'layout.json').write_text(json.dumps(layout, indent=2)+'\n')
record = {'changedIdentity': 'fair-in-the-air', 'newPanelPixels': list(frame),
          'baselineImageSha256': digest(baseline/'fair-in-the-air.png'),
          'screenManifestSha256': digest(screen/'screen-manifest.json'),
          'outputSha256': digest(dest), 'otherTwelveByteIdentical': unchanged,
          'pixelsOutsideNewPanelUnchanged': True,
          'compositionSourceSha256': digest(Path(__file__))}
(out/'screen-composition.json').write_text(json.dumps(record, indent=2)+'\n')
print('Added Screen detail; all twelve other images and existing final-state pixels are unchanged.')
