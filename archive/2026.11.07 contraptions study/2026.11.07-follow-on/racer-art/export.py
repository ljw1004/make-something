"""Use a stable pixel/metre scale within each construction family; cap loose parts."""
from pathlib import Path
import argparse
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from export_art import export
from PIL import Image
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--masters',required=True);p.add_argument('--output',required=True)
args=p.parse_args();src,out=Path(args.masters),Path(args.output);out.mkdir(parents=True,exist_ok=True)
plan=json.loads((HERE/'construction-plan.json').read_text());settings=json.loads((HERE/'display-settings.json').read_text());records=[]
groups={}
for identity,info in plan.items():
    family=info['view'] if info['view'] in ['mast','underside','upright','axle'] else info['image']
    groups.setdefault(family,set()).add(info['image'])
for family,ids in groups.items():
    images={id:Image.open(src/(id+'.png')).convert('RGBA') for id in sorted(ids)}
    boxes=[im.getchannel('A').point(lambda a:255 if a>=24 else 0).getbbox() for im in images.values()]
    crop=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
    long_css=settings['visibleLongCss'][family];ratio=4*long_css/max(crop[2]-crop[0],crop[3]-crop[1])
    for identity,im in images.items():
        record=export(im,ratio,out/(identity+'.webp'))
        records.append(dict(image=identity,family=family,scaleBounds=crop,visibleLongCss=long_css,**record))
        if identity=='wr-sail':
            scale=settings['carriedSailLongCss']/long_css
            carried=export(im,ratio*scale,out/'wr-sail-carried.webp')
            records.append(dict(image='wr-sail-carried',sourceImage=identity,
                                family='carried-sail',scaleBounds=crop,
                                visibleLongCss=settings['carriedSailLongCss'],**carried))
(src/'export-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
