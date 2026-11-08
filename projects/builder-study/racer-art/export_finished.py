"""Export the complete connected racer at its independent presentation scale."""
from pathlib import Path
import argparse
import json
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--masters', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args()
settings = json.loads((Path(__file__).parent/'finished-settings.json').read_text())
source = Path(args.masters)/'wind-racer.png'
image = Image.open(source).convert('RGBA')
crop = image.getchannel('A').point(lambda a: 255 if a >= 24 else 0).getbbox()
part = image.crop(crop)
factor = settings['visibleLongCssPixels']*4/max(part.size)
part = part.resize(tuple(round(n*factor) for n in part.size), Image.Resampling.LANCZOS)
canvas = Image.new('RGBA', (part.width+24, part.height+24))
canvas.alpha_composite(part, (12, 12))
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
canvas.save(out/'wind-racer.webp', quality=94, method=6)
(source.parent/'export-manifest.json').write_text(json.dumps({
    'id': 'wind-racer', 'crop': crop, 'size': canvas.size,
    'visibleLongCssPixels': settings['visibleLongCssPixels'],
}, indent=2)+'\n')
