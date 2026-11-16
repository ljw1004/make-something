"""Export selected builtin-painted families; uniform scale within each tissue family.

Run: uv run --with pillow python projects/anatomy/atlas/composition-review/body/produce.py
Cropping, masking, sizing and registered composition; no anatomy is painted by
the producer. The built-in generated masters supply every anatomical stroke.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageChops

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
PREFIX = 'atlas/composition-review/body/assets/'
items = {}
slots = {}

def save(filename, image, identity=None):
    image.save(OUT / (filename + '.png'))
    if identity:
        items[identity] = PREFIX + filename + '.png'
    return image

def masked(image, polygons):
    alpha = Image.new('L', image.size)
    for polygon in polygons:
        ImageDraw.Draw(alpha).polygon(polygon, fill=255)
    result = image.copy()
    result.putalpha(ImageChops.multiply(image.getchannel('A'), alpha))
    return result

def resize(image, factor):
    return image.resize((round(image.width * factor), round(image.height * factor)), Image.Resampling.LANCZOS)

def export_sheet(source, cells, columns, rows, scale):
    image = Image.open(ROOT / 'sources' / source).convert('RGBA')
    for index, (identity, filename) in enumerate(cells):
        col, row = index % columns, index // columns
        box = (round(col * image.width / columns), round(row * image.height / rows),
               round((col + 1) * image.width / columns), round((row + 1) * image.height / rows))
        part = image.crop(box)
        # Ignore near-transparent edge speckles when establishing the crop.
        bbox = part.getchannel('A').point(lambda a: 255 if a > 30 else 0).getbbox()
        if not bbox:
            raise ValueError(f'Empty selected cell: {identity}')
        part = part.crop(bbox)
        factor = scale[index] if isinstance(scale, list) else scale
        part = resize(part, factor)
        part.save(OUT / (filename + '.png'))
        if identity:
            items[identity] = PREFIX + filename + '.png'

export_sheet('intestinal-mucosa.png', [
    ('name:Thin intestinal lining', 'thin-intestinal-lining'),
    ('name:Fingerlike intestinal folds', 'fingerlike-intestinal-folds'),
    ('name:Intestinal capillaries', 'intestinal-capillaries'),
    ('name:Collecting vein from the intestine', 'collecting-vein-from-the-intestine'),
    ('name:Folded absorbing lining', 'folded-absorbing-lining'),
    ('name:Blood route from the intestine', 'blood-route-from-the-intestine'),
    ('name:Lining with intestinal capillaries', 'lining-with-intestinal-capillaries'),
    ('name:Intestinal absorbing surface', 'intestinal-absorbing-surface'),
], 4, 2, 1.6)
items['id:water-gut-capillary'] = items['name:Intestinal absorbing surface']

export_sheet('muscle-storage-v2.png', [
    ('name:Muscle fibres beside a blood vessel', 'muscle-fibres-beside-a-blood-vessel'),
    ('name:Muscle carbohydrate store', 'muscle-carbohydrate-store'),
], 2, 1, 0.53)

# Hormone-bearing samples use the repaired shared Blood master without
# replacing its cells. Molecular forms use the declared schematic convention.
export_sheet('molecules-fluid.png', [
    (None, 'insulin-molecules'),
    (None, 'glucagon-molecules'),
    ('name:Small fatty acids and gas', 'small-fatty-acids-and-gas'),
    ('name:Concentrated urine', 'concentrated-urine'),
], 2, 2, [0.2, 0.2, 0.5, 0.35])
blood = Image.open(ROOT.parent / 'blood/sources/whole.png').convert('RGBA')
blood.putalpha(blood.getchannel('A').point(lambda a: 0 if a < 18 else a))
blood = resize(blood, 900 / blood.width)
for material, name in [('insulin', 'Insulin in blood'), ('glucagon', 'Glucagon in blood')]:
    result = blood.copy()
    protein = Image.open(OUT / (material + '-molecules.png')).convert('RGBA')
    result.alpha_composite(protein, (330, 240))
    result.alpha_composite(resize(protein, 0.7), (440, 455))
    save(material + '-in-blood', result, 'name:' + name)

export_sheet('colon.png', [
    ('name:Colon lining', 'colon-lining'),
    (None, 'unused-mucus-outline'),
    ('name:Colon supporting tissue and vessels', 'colon-supporting-tissue-and-vessels'),
    ('name:Colon muscle wall', 'colon-muscle-wall'),
    ('name:Mucus-covered colon lining', 'mucus-covered-colon-lining'),
    ('name:Colon lining with supporting tissue', 'colon-lining-with-supporting-tissue'),
    ('name:Colon inner wall', 'colon-inner-wall'),
    ('name:Colon', 'colon'),
], 4, 2, 1.7)
(OUT / 'unused-mucus-outline.png').unlink()
export_sheet('digestive-tract.png', [
    ('name:Upper digestive tract', 'upper-digestive-tract'),
    ('name:Digestive tract', 'digestive-tract'),
], 2, 1, 1.3)

water = Image.open(ROOT / 'sources/water-recovery.png').convert('RGBA')
water_base = water.crop((0,120,512,900))
water_after = water.crop((512,120,1024,900))
water_fit = masked(water_after, [[(105,644),(130,628),(372,628),(419,649),
                                (411,679),(375,697),(138,697),(108,680)]])
save('gut-blood-vessel', resize(water_base, 1.25), 'id:water-gut-capillary')
save('gut-water-fitted', resize(water_fit, 1.25))
slots['id:water-gut-capillary'] = {'name:Drinking water': PREFIX + 'gut-water-fitted.png'}
recovery = water.crop((1024,0,1536,1024))
recovery = recovery.crop(recovery.getchannel('A').point(lambda a: 255 if a > 30 else 0).getbbox())
save('kidney-recovery-tube', resize(recovery, 1.05), 'name:Kidney recovery tube')

# The kidneys, continuous renal/ureter walls and bladder openings come from one
# painted whole. Each fitting retains that common full-system registration.
urinary = Image.open(ROOT / 'sources/urinary-system.png').convert('RGBA')
base = masked(urinary, [[(0,0),(1024,0),(1024,600),(0,600)]])
bladder_polygon = [(0,1150),(1024,1150),(1024,1536),(0,1536)]
bladder = masked(urinary, [bladder_polygon])
ureters = urinary.copy()
occupied = ImageChops.lighter(base.getchannel('A'), bladder.getchannel('A'))
ureters.putalpha(ImageChops.subtract(urinary.getchannel('A'), occupied))
factor = 0.68
save('urinary-system', resize(base, factor), 'name:Urinary system')
save('urinary-ureters-fitted', resize(ureters, factor))
save('urinary-bladder-fitted', resize(bladder, factor))
save('ureters', resize(ureters.crop(ureters.getbbox()), factor), 'name:Ureters')
save('bladder', resize(bladder.crop(bladder.getbbox()), factor), 'name:Bladder')
slots['name:Urinary system'] = {
    'name:Ureters': PREFIX + 'urinary-ureters-fitted.png',
    'name:Bladder': PREFIX + 'urinary-bladder-fitted.png',
}
exec((ROOT / 'skin.py').read_text())
exec((ROOT / 'wounds.py').read_text())
(ROOT / 'map.json').write_text(json.dumps({'itemIcons': items, 'slotIcons': slots}, indent=2) + '\n')
print(f'Exported {len(items)} item mappings')
