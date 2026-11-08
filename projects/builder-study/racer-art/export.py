"""Use a stable pixel/metre scale within each construction family; cap loose parts."""
from pathlib import Path
import argparse
import json
from PIL import Image
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--masters',required=True);p.add_argument('--output',required=True)
args=p.parse_args();src,out=Path(args.masters),Path(args.output);out.mkdir(parents=True,exist_ok=True)
plan=json.loads((HERE/'construction-plan.json').read_text());settings=json.loads((HERE/'display-settings.json').read_text());records=[]
groups={}
for identity,info in plan.items():
    family=info['view'] if info['view'] in ['mast','underside','axle'] else info['image']
    groups.setdefault(family,set()).add(info['image'])
for family,ids in groups.items():
    images={id:Image.open(src/(id+'.png')).convert('RGBA') for id in sorted(ids)}
    boxes=[im.getchannel('A').point(lambda a:255 if a>=24 else 0).getbbox() for im in images.values()]
    crop=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
    long_css=settings['visibleLongCss'][family];ratio=4*long_css/max(crop[2]-crop[0],crop[3]-crop[1])
    for identity,im in images.items():
        part=im.crop(crop);part=part.resize((round(part.width*ratio),round(part.height*ratio)),Image.Resampling.LANCZOS)
        final=Image.new('RGBA',(part.width+24,part.height+24));final.alpha_composite(part,(12,12));final.save(out/(identity+'.webp'),quality=94,method=6)
        records.append(dict(image=identity,family=family,crop=crop,size=list(final.size),visibleLongCss=long_css))
        if identity=='wr-sail':
            scale=settings['carriedSailLongCss']/long_css
            small=final.resize((round(final.width*scale),round(final.height*scale)),Image.Resampling.LANCZOS);small.save(out/'wr-sail-carried.webp',quality=94,method=6)
(src/'export-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
