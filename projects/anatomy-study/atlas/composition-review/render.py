"""Render actual same-scale operands/result strips from frozen native states."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,sys,textwrap,math
root=Path(sys.argv[1]);font=lambda n:ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',n)
for p in sorted(root.glob('*/packet.json')):
 data=json.loads(p.read_text())
 icons=[]
 for obj in data['inventory']:
  icons.append((obj['name'],obj['base'],[]))
  if obj['layers']:icons.append((obj['name']+' (fitted)',obj['base'],obj['layers']))
 inv=Image.new('RGB',(1000,70+math.ceil(len(icons)/5)*190),(250,247,238));di=ImageDraw.Draw(inv)
 di.text((15,15),f"{data['chapter']}. {data['title']} — complete inventory",font=font(22),fill='#493c31')
 for i,(name,base,layers) in enumerate(icons):
  im=Image.open(base).convert('RGBA')
  for layer in layers:im.alpha_composite(Image.open(layer).convert('RGBA').resize(im.size,Image.Resampling.LANCZOS))
  box=im.getchannel('A').getbbox();im=im.crop(box) if box else im
  scale=min(180/im.width,130/im.height);im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS)
  x=(i%5)*200;y=70+(i//5)*190;inv.paste(im,(x+(200-im.width)//2,y+(130-im.height)//2),im)
  for j,line in enumerate(textwrap.wrap(name,27)[:3]):di.text((x+8,y+134+j*16),line,font=font(13),fill='#493c31')
 inv.save(p.parent/'inventory.jpg',quality=93)
 for n,op in enumerate(data['operations'],1):
  images=[]
  for obj in [op['a'],op['b'],op['result']]:
   im=Image.open(obj['base']).convert('RGBA')
   for path in obj['layers']:im.alpha_composite(Image.open(path).convert('RGBA').resize(im.size,Image.Resampling.LANCZOS))
   im=im.resize((max(1,round(im.width/4)),max(1,round(im.height/4))),Image.Resampling.LANCZOS);images.append(im)
  height=max(280,max(im.height for im in images)+140);width=max(350,max(im.width for im in images)+40)
  sheet=Image.new('RGB',(width*3+100,height),(250,247,238));d=ImageDraw.Draw(sheet)
  d.text((12,10),f"Chapter {data['chapter']} · operation {n} · same playing scale",font=font(18),fill='#493c31')
  for i,(im,obj) in enumerate(zip(images,[op['a'],op['b'],op['result']])):
   x=i*(width+50);sheet.paste(im,(x+(width-im.width)//2,65+(height-140-im.height)//2),im)
   for j,line in enumerate(textwrap.wrap(obj['name'],38)[:2]):d.text((x+10,height-55+j*21),line,font=font(17),fill='#493c31')
  d.text((width+7,height//2),' + ',font=font(23),fill='#493c31');d.text((2*width+53,height//2),' = ',font=font(23),fill='#493c31')
  sheet.save(p.parent/f'operation-{n:02}.png')
print('Rendered all operation strips')
