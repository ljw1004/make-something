"""Temporary review sheets from actual exported icons, optionally with captions."""
from pathlib import Path
import argparse
import json
import math
import textwrap
from PIL import Image,ImageDraw,ImageFont

p=argparse.ArgumentParser();p.add_argument('--assets',required=True);p.add_argument('--output',required=True)
p.add_argument('--ids',required=True,help='Comma-separated asset basenames, in review order')
p.add_argument('--captions',help='Optional JSON mapping image basenames to text-only descriptions')
p.add_argument('--natural-css',action='store_true',help='Show loose icons at their exported CSS size, capped to the cell')
args=p.parse_args();assets=Path(args.assets);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
names=list(dict.fromkeys(args.ids.split(',')));captions=json.loads(Path(args.captions).read_text()) if args.captions else {}
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',14)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',12)
width,height=270,330 if args.captions else 285
for page in range(math.ceil(len(names)/12)):
    group=names[page*12:(page+1)*12];sheet=Image.new('RGB',(width*3,height*4),'white');draw=ImageDraw.Draw(sheet)
    for i,name in enumerate(group):
        x,y=(i%3)*width,(i//3)*height
        icon=Image.open(assets/(name+'.webp')).convert('RGBA')
        cap=(min(240,round(icon.width/4)),min(235,round(icon.height/4))) if args.natural_css else (240,235)
        icon.thumbnail(cap,Image.Resampling.LANCZOS)
        sheet.paste(icon,(x+(width-icon.width)//2,y+10+(235-icon.height)//2),icon)
        draw.text((x+8,y+247),name,fill='#202820',font=font)
        if name in captions:
            for line,text in enumerate(textwrap.wrap(captions[name],40)):
                draw.text((x+8,y+266+line*14),text,fill='#283028',font=small)
        draw.rectangle((x,y,x+width-1,y+height-1),outline='#dae1dc')
    sheet.save(out/f'{page+1:02}.png')
