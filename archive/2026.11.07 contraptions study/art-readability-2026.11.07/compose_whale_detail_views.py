"""Compose chapter-specific whole/detail illustrations on registered canvases.

Uses rendered camera views only. It never erases or retouches an occluding
part. Main views share one union crop and scale; each chapter's detail uses
one fixed camera and crop across every state. Labels distinguish view scales.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser()
parser.add_argument('--source', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--font', required=True, help='Path to an available sans-serif font file')
parser.add_argument('--config', default=str(Path(__file__).with_name('fitted-chapter-views.json')))
args = parser.parse_args()
source, out = Path(args.source), Path(args.output)
out.mkdir(parents=True, exist_ok=True)
config = json.loads(Path(args.config).read_text())
manifest = json.loads((source/'manifest-detail.json').read_text())
raw = {entry['name']: entry for entry in manifest['images']}
scale = config['master_scale']
canvas = tuple(round(v*scale) for v in config['canvas_css'])
states = [(chapter, identity) for chapter, chapter_plan in config['chapters'].items()
          for identity in chapter_plan['ids']]
names = [f'{chapter}--{identity}--main' for chapter, identity in states]
main_images = {name: Image.open(source/(name+'.png')).convert('RGBA') for name in names}
if len({im.size for im in main_images.values()}) != 1:
    raise ValueError('Registered main sources must share one canvas resolution')
bounds = [im.getbbox() for im in main_images.values()]
union = (min(b[0] for b in bounds), min(b[1] for b in bounds),
         max(b[2] for b in bounds), max(b[3] for b in bounds))
factor = config['main']['width_css']*scale/(union[2]-union[0])
main_size = (round((union[2]-union[0])*factor), round((union[3]-union[1])*factor))
main_position = ((canvas[0]-main_size[0])//2, round(config['main']['top_css']*scale))
font = ImageFont.truetype(args.font, round(config['main']['label_font_css']*scale))
detail_font = ImageFont.truetype(args.font, round(config['detail']['label_font_css']*scale))
entries = []
for chapter, identity in states:
    chapter_plan = config['chapters'][chapter]
    main_name, detail_name = f'{chapter}--{identity}--main', f'{chapter}--{identity}--detail'
    for name in [main_name, detail_name]:
        image_path = source/(name+'.png')
        if hashlib.sha256(image_path.read_bytes()).hexdigest() != raw[name]['sha256']:
            raise ValueError('Rendered source hash mismatch: '+name)
        request = raw[name]['request']
        expected_view = config['main']['view'] if name.endswith('--main') else chapter_plan['detail_view']
        if request['view'] != expected_view:
            raise ValueError('Camera does not match the approved family: '+name)
        if abs(raw[name]['renderedHatchDegrees']-chapter_plan['hatch_degrees'][identity]) > 1e-5:
            raise ValueError('Hatch pose does not match the explicit story state: '+name)
    image = Image.new('RGBA', canvas)
    image.alpha_composite(main_images[main_name].crop(union).resize(main_size, Image.Resampling.LANCZOS), main_position)
    detail = Image.open(source/(detail_name+'.png')).convert('RGBA')
    crop = tuple(round(v*(detail.width if axis%2 == 0 else detail.height))
                 for axis, v in enumerate(chapter_plan['detail_crop_normalized']))
    detail = detail.crop(crop)
    bx, by, bw, bh = [round(v*scale) for v in config['detail']['box_css']]
    detail.thumbnail((bw, bh), Image.Resampling.LANCZOS)
    position = (bx+(bw-detail.width)//2, by+(bh-detail.height)//2)
    image.alpha_composite(detail, position)
    draw = ImageDraw.Draw(image)
    draw.rectangle((bx-2, by-2, bx+bw+1, by+bh+1), outline='#647c86', width=round(config['detail']['outline_css']*scale))
    draw.text(tuple(round(v*scale) for v in config['main']['label_position_css']), config['main']['label'],
              fill='#355866', font=font, anchor='lt')
    draw.text(tuple(round(v*scale) for v in config['detail']['label_position_css']), chapter_plan['detail_label'],
              fill='#355866', font=detail_font, anchor='lt')
    destination = out/f'{chapter}--{identity}.png'
    if destination.exists():
        raise ValueError('Never overwrite a composed master: '+str(destination))
    image.save(destination)
    entries.append({'chapter': chapter, 'id': identity, 'pixels': list(canvas),
                    'canvasCss': config['canvas_css'], 'mainUnionCrop': union,
                    'mainPositionPixels': main_position, 'mainSizePixels': main_size,
                    'detailCrop': crop, 'detailPositionPixels': position,
                    'detailSizePixels': detail.size, 'main': raw[main_name], 'detail': raw[detail_name],
                    'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()})
result = {'kind': 'registered-chapter-main-and-detail', 'images': entries,
          'configuration': config,
          'configurationSha256': hashlib.sha256(Path(args.config).read_bytes()).hexdigest(),
          'compositorSha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'fontSha256': hashlib.sha256(Path(args.font).read_bytes()).hexdigest(),
          'rawSourceManifest': str(source/'manifest-detail.json'),
          'rawSourceManifestSha256': hashlib.sha256((source/'manifest-detail.json').read_bytes()).hexdigest()}
(out/'manifest-chapters.json').write_text(json.dumps(result, indent=2)+'\n')
print('Composed', len(entries), 'registered chapter-specific masters')
