"""Extract exact blood-cell inhabitants from the selected continuous liquid sample."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
import json
P=Path(__file__).resolve().parent;A=P/'assets';A.mkdir(exist_ok=True);L=Image.Resampling.LANCZOS
M={'itemIcons':{}}
whole=Image.open(P/'sources/whole.png').convert('RGBA');plasma=Image.open(P/'sources/plasma.png').convert('RGBA').resize(whole.size,L)
def clean(im):
 im=im.copy();im.putalpha(im.getchannel('A').point(lambda a:0 if a<18 else a));return im
whole=clean(whole);plasma=clean(plasma)
def maskboxes(boxes):
 m=Image.new('L',whole.size);d=ImageDraw.Draw(m)
 for box in boxes:d.ellipse(box,fill=255)
 return m
def select(mask):
 im=whole.copy();im.putalpha(ImageChops.multiply(im.getchannel('A'),mask));return im
def save(name,im,title,trim=False):
 im=im.resize((900,600),L)
 if trim:
  box=im.getchannel('A').getbbox();im=im.crop(box)
 im.save(A/(name+'.png'));M['itemIcons']['name:'+title]='atlas/composition-review/blood/assets/'+name+'.png'
redmask=maskboxes([(244,262,490,470),(253,590,485,788),(983,630,1240,845)])
whitemask=maskboxes([(795,190,1161,541)])
for box in [(613,215,688,269),(105,476,170,532),(547,508,625,573),(794,649,856,697),(1230,471,1297,524),(611,805,683,853)]:
 m=maskboxes([box]);whitemask=ImageChops.lighter(whitemask,m)
reds=select(redmask);whites=select(whitemask)
save('red-cells',reds,'Red blood cells',True);save('oxygenated-red-cells',reds,'Red cells carrying oxygen',True)
save('white-cells-platelets',whites,'White cells and platelets',True)
save('plasma',plasma,'Plasma')
pr=plasma.copy();pr.alpha_composite(reds);save('plasma-red-cells',pr,'Plasma with oxygen-carrying red cells')
pw=plasma.copy();pw.alpha_composite(whites);save('plasma-white-cells',pw,'Plasma with white cells and platelets')
save('blood',whole,'Blood')
if (P/'sources/water.png').exists():save('water',Image.open(P/'sources/water.png').convert('RGBA'),'Plasma water')
(P/'map.json').write_text(json.dumps(M,indent=2)+'\n')
