"""Export new folds through the exact selected flat/full-fold crop and scale."""
from pathlib import Path
import argparse
import json
from PIL import Image

parser=argparse.ArgumentParser()
parser.add_argument('--masters',required=True)
parser.add_argument('--baseline-masters',required=True)
parser.add_argument('--output',required=True)
args=parser.parse_args()
src,base,out=Path(args.masters),Path(args.baseline_masters),Path(args.output)
out.mkdir(parents=True,exist_ok=True)
reference=next(row for row in json.loads((base/'export-manifest.json').read_text()) if row['id']=='pw-paper')
crop=tuple(reference['crop'])
scale=reference['visibleLongCss']*4/max(crop[2]-crop[0],crop[3]-crop[1])
records=[]
for identity in ['pw-one-blade','pw-two-blades','pw-three-blades']:
    image=Image.open(src/(identity+'.png')).convert('RGBA')
    bounds=image.getchannel('A').point(lambda a:255 if a>=24 else 0).getbbox()
    assert bounds[0]>=crop[0] and bounds[1]>=crop[1] and bounds[2]<=crop[2] and bounds[3]<=crop[3],(identity,bounds,crop)
    part=image.crop(crop)
    part=part.resize((round(part.width*scale),round(part.height*scale)),Image.Resampling.LANCZOS)
    final=Image.new('RGBA',(part.width+24,part.height+24));final.alpha_composite(part,(12,12))
    assert list(final.size)==reference['size']
    final.save(out/(identity+'.webp'),quality=94,method=6)
    records.append({'id':identity,'crop':crop,'size':list(final.size),'sameScaleAs':'pw-paper,pw-loose-rotor,pw-folded-rotor'})
(src/'export-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
