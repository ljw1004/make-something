"""Export deterministic chapter-one crops at four physical pixels per CSS px."""
from pathlib import Path
import argparse
import json
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
    (['pw-rear-rotor','pw-bearing-rotor'],settings['sharedRearStatesLongCssPixels']),
    (['pw-mounted'],settings['completeLongCssPixels']),(['pinwheel'],settings['completeLongCssPixels']),
    (['pw-hub'],settings['hubLongCssPixels']),(['pw-axle'],settings['axleLongCssPixels']),(['pw-handle'],settings['handleLongCssPixels']),
]
records=[]
for ids, long_css in groups:
    images={identity:Image.open(src/(identity+'.png')).convert('RGBA') for identity in ids}
    bounds=[im.getchannel('A').point(lambda a:255 if a>=24 else 0).getbbox() for im in images.values()]
    crop=(min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds))
    scale=long_css*4/max(crop[2]-crop[0],crop[3]-crop[1])
    for identity,im in images.items():
        part=im.crop(crop)
        part=part.resize((round(part.width*scale),round(part.height*scale)),Image.Resampling.LANCZOS)
        # The alpha drawing gets a modest 3 CSS px canvas margin.
        final=Image.new('RGBA',(part.width+24,part.height+24));final.alpha_composite(part,(12,12))
        final.save(out/(identity+'.webp'),quality=94,method=6)
        if identity=='pinwheel' and args.icon:
            drawing=final.copy();drawing.thumbnail((440,440),Image.Resampling.LANCZOS)
            icon=Image.new('RGBA',(512,512),'white');icon.alpha_composite(drawing,((512-drawing.width)//2,(512-drawing.height)//2));icon.convert('RGB').save(args.icon)
        records.append({'id':identity,'sharedCrop':ids,'crop':crop,'size':list(final.size),'visibleLongCss':long_css})
(src/'export-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
