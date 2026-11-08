"""Export deterministic chapter-one crops at four physical pixels per CSS px."""
from pathlib import Path
import argparse
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from export_art import export
from PIL import Image

parser=argparse.ArgumentParser()
parser.add_argument('--masters',required=True)
parser.add_argument('--output',required=True)
parser.add_argument('--icon')
args=parser.parse_args()
settings=json.loads((Path(__file__).parent/'production-settings.json').read_text())['export']
src,out=Path(args.masters),Path(args.output)
out.mkdir(parents=True,exist_ok=True)
groups=[
    (['pw-paper','pw-loose-rotor','pw-folded-rotor'],settings['sharedFrontStatesLongCssPixels']),
    (['pw-rear-rotor','pw-bearing-rotor','pw-mounted'],settings['completeLongCssPixels']),
    (['pinwheel'],settings['completeLongCssPixels']),
    (['pw-hub'],settings['hubLongCssPixels']),(['pw-axle'],settings['axleLongCssPixels']),(['pw-handle'],settings['handleLongCssPixels']),
]
records=[]
for ids, long_css in groups:
    images={identity:Image.open(src/(identity+'.png')).convert('RGBA') for identity in ids}
    bounds=[im.getchannel('A').point(lambda a:255 if a>=24 else 0).getbbox() for im in images.values()]
    crop=(min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds))
    scale=long_css*4/max(crop[2]-crop[0],crop[3]-crop[1])
    for identity,im in images.items():
        record=export(im,scale,out/(identity+'.webp'))
        if identity=='pinwheel' and args.icon:
            drawing=Image.open(out/(identity+'.webp')).convert('RGBA');drawing.thumbnail((440,440),Image.Resampling.LANCZOS)
            icon=Image.new('RGBA',(512,512),'white');icon.alpha_composite(drawing,((512-drawing.width)//2,(512-drawing.height)//2));icon.convert('RGB').save(args.icon)
        records.append(dict(id=identity,scaleFamily=ids,scaleBounds=crop,visibleLongCss=long_css,**record))
(src/'export-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
