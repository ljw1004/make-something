"""Compose labeled actual-camera views into one fixed 300 CSS px diagram."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser()
parser.add_argument('--masters', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args()
masters, out = Path(args.masters), Path(args.output)
out.mkdir(parents=True, exist_ok=True)
records = json.loads((masters/'render-manifest.json').read_text())['images']
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 42)


def bounds(im):
    return im.getchannel('A').point(lambda n: 255 if n > 24 else 0).getbbox()


def union(boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


main_images = {r['id']: Image.open(masters/r['detail']['file']).convert('RGBA') for r in records}
projected_boxes = [r['detail'].get('movingBodyProjectionBounds') for r in records]
if all(projected_boxes):
    raw_box = union(projected_boxes)
    main_box = (max(0, math.floor(raw_box[0])-8), max(0, math.floor(raw_box[1])-8),
                min(1200, math.ceil(raw_box[2])+8), min(1200, math.ceil(raw_box[3])+8))
else:
    # Earlier isolated-body pilots predate the attached-line crop metadata.
    main_box = union([bounds(im) for im in main_images.values()])
main_scale = min(880/(main_box[2]-main_box[0]), 670/(main_box[3]-main_box[1]))
setup_images = {r['id']: Image.open(masters/r['setup']['file']).convert('RGBA') for r in records}
groups = {
    'c23': {'whale-running-fair', 'whale-short-tethered', 'whale-ready-low', 'whale-nose-down', 'whale-trimmed', 'whale-hovering-low'},
    'c24': {'whale-low-tested', 'whale-garden-tethered', 'whale-aimed'},
    'c25': {'whale-garden-ready', 'fair-bannered', 'fair-whale-alight', 'fair-in-the-air'},
}
setup_boxes = {group: union([bounds(setup_images[i]) for i in identities if i in setup_images])
               for group, identities in groups.items() if identities.intersection(setup_images)}
layout = {}


def place(im, box, scale, center, canvas):
    crop = im.crop(box)
    crop = crop.resize(tuple(round(v*scale) for v in crop.size), Image.Resampling.LANCZOS)
    origin = tuple(round(center[i]-crop.size[i]/2) for i in range(2))
    canvas.alpha_composite(crop, origin)
    return [origin[0], origin[1], crop.width, crop.height]


for record in records:
    identity = record['id']
    group = next(group for group, identities in groups.items() if identity in identities)
    setup_box = setup_boxes[group]
    setup_scale = min(436/(setup_box[2]-setup_box[0]), 376/(setup_box[3]-setup_box[1]))
    canvas = Image.new('RGBA', (1200, 1200))
    draw = ImageDraw.Draw(canvas)
    main_size = [round(v*main_scale) for v in (main_box[2]-main_box[0], main_box[3]-main_box[1])]
    main_origin = [round(600-main_size[0]/2), round(395-main_size[1]/2)]
    draw.text((main_origin[0], 8), 'Whale detail', font=font, fill='#294849')
    main_rect = place(main_images[identity], main_box, main_scale, (600, 395), canvas)
    # A visible crop boundary makes the actual outgoing line continuations
    # legible as a camera-detail crop rather than invented free wire ends.
    draw.rectangle((main_rect[0], main_rect[1], main_rect[0]+main_rect[2]-1, main_rect[1]+main_rect[3]-1),
                   outline='#6f9697', width=3)
    draw.rounded_rectangle((688, 742, 1176, 1184), radius=20, fill='#faf5e5', outline='#6f9697', width=3)
    draw.text((710, 754), 'Whole setup', font=font, fill='#294849')
    setup_rect = place(setup_images[identity], setup_box, setup_scale, (932, 990), canvas)
    teaching_rect = None
    if record['teaching']:
        im = Image.open(masters/record['teaching']['file']).convert('RGBA')
        box = bounds(im)
        scale = min(602/(box[2]-box[0]), 350/(box[3]-box[1]))
        draw.rounded_rectangle((20, 742, 664, 1184), radius=20, fill='#faf5e5', outline='#6f9697', width=3)
        draw.text((42, 754), record['teaching']['label'], font=font, fill='#294849')
        teaching_rect = place(im, box, scale, (342, 990), canvas)
    dest = out/(identity+'.png')
    canvas.save(dest)
    layout[identity] = {'pixels': [1200, 1200], 'chapter': group, 'mainRectPixels': main_rect,
                        'mainReceivingBoxPixels': [main_rect[0]-12, main_rect[1]-12, main_rect[2]+24, main_rect[3]+24],
                        'mainCrop': main_box, 'mainScale': main_scale,
                        'setupRectPixels': setup_rect, 'setupCrop': setup_box, 'setupScale': setup_scale,
                        'teachingRectPixels': teaching_rect,
                        'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()}
(out/'layout.json').write_text(json.dumps(layout, indent=2)+'\n')
print('Composed', len(layout), 'fixed flight diagrams')
