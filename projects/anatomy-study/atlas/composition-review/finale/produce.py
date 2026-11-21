"""Mechanical constituent extraction from a single coherent whole-body painting.

Masks/crops/registration and uniform resizing only; all anatomy is generated art.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageOps
import numpy as np
import json,re
P=Path(__file__).resolve().parent;O=P/'assets';O.mkdir(exist_ok=True)
PREFIX='atlas/composition-review/finale/assets/';S=.9
M={'itemIcons':{},'slotIcons':{},'presentations':{}}
# Chapter28 primitive arrivals reserve space above the goal panel. Existing
# derived carryovers and results retain the engine's normal placement rules.
M['placements']={
 'id:atlas-final-chest':[670,400],
 'name:Lower body':[490,1130],
 'name:Skin covering':[1180,900],
 'id:art-arm-assembly':[945,1450],
 'id:final-urinary-organs':[130,1670],
 'id:final-ears':[1120,105],
}
def read(n):
 im=Image.open(P/'sources'/(n+'.png')).convert('RGBA');a=np.array(im);a[a[:,:,3]<24]=0;return Image.fromarray(a)
def blank():return Image.new('RGBA',(1024,1536))
def mask(points):
 m=Image.new('L',(1024,1536));ImageDraw.Draw(m).polygon(points,fill=255);return m
def box(b):
 m=Image.new('L',(1024,1536));ImageDraw.Draw(m).rectangle(b,fill=255);return m
def part(im,m):
 im=im.copy();im.putalpha(ImageChops.multiply(im.getchannel('A'),m));return im
def minus(im,m):return part(im,ImageOps.invert(m))
def emit(n,im,key=None,frame=None,trim=False):
 if frame:im=im.crop(frame)
 if trim:
  b=im.getchannel('A').getbbox();im=ImageOps.expand(im.crop(b),6)
 im=im.resize((round(im.width*S),round(im.height*S)),Image.Resampling.LANCZOS)
 slug=re.sub('[^a-z0-9]+','-',n.lower()).strip('-');im.save(O/(slug+'.png'));p=PREFIX+slug+'.png'
 if key:M['itemIcons'][key]=p
 return p
def pres(key,path):M['presentations'][key]=[{'chapter':'full-assembly-regions','path':path}]
def layer(owner,partkey,n,im,frame):
 p=emit(n,im,frame=frame);M['slotIcons'].setdefault(owner,{})[partkey]=p;return p
body=read('body-beneath-skin');finished=read('body-master');skin=read('skin-covering');empty=read('body-empty-abdomen')
# The regional neck cut follows beneath the jaw, excluding its small curved
# remnant from both headless exports while retaining the receiving neck tissue.
chinmask=mask([(486,180),(620,180),(620,202),(570,202),(545,198),(520,192),(500,188)])
# The regional boundary follows the existing domed diaphragm and abdominal sides.
lowmask=mask([(0,1536),(0,980),(310,980),(329,800),(354,620),(375,546),(409,532),(455,527),(496,535),(550,534),(610,544),(649,556),(670,620),(693,800),(714,980),(1024,980),(1024,1536)])
# Exclude arms from the lower body; both adult legs and pelvic walls remain.
lowmask=ImageChops.multiply(lowmask,mask([(345,520),(680,520),(715,910),(715,1536),(310,1536),(310,910)]))
chestmask=ImageOps.invert(lowmask);chestmask=ImageChops.multiply(chestmask,box((0,180,1024,980)))
# Built left arm includes its genuine clavicle up to the manubrial attachment.
armmask=mask([(0,280),(284,280),(334,270),(408,273),(481,281),(490,302),(428,306),(365,310),(342,344),(337,425),(339,505),(324,566),(297,650),(272,743),(255,798),(257,850),(242,940),(207,982),(0,982)])
# Limit the chest to its actual diaphragm boundary and complete attached arms;
# no abdominal edge scraps hang below the regional separation.
rightarm=mask([(680,280),(780,280),(900,750),(960,980),(755,980),(747,795),(704,640),(676,546),(660,430)])
chestmask=ImageChops.lighter(ImageChops.multiply(chestmask,box((0,180,1024,565))),ImageChops.lighter(armmask,rightarm))
chestmask=ImageChops.multiply(chestmask,box((0,180,1024,980)))
# Chest handoff supplies completed diaphragm, cardiopulmonary anatomy and opposite arm.
chestframe=(100,180,910,980)
chestbare=body.copy();patch=read('thorax-without-lymph').resize((520,380));chestbare.paste(patch,(250,180),patch)
chest=minus(minus(part(chestbare,chestmask),armmask),chinmask)
emit('Chest region',chest,'id:atlas-final-chest',chestframe)
arm=part(body,armmask);pres('id:art-arm-assembly',emit('Arm assembly at body scale',arm,trim=True))
layer('id:atlas-final-chest','id:art-arm-assembly','Chest arm layer',arm,chestframe)
# A supported neck/upper-thoracic tissue strip carries the selected fine lymph collector.
lymphmask=mask([(446,179),(466,179),(480,230),(481,260),(494,279),(480,297),(445,294),(426,280),(441,263),(448,239),(441,212)])
lymph=part(body,lymphmask)
pres('id:art-lymph-drainage-network',emit('Lymph return at body scale',lymph,trim=True))
layer('id:atlas-final-chest','id:art-lymph-drainage-network','Chest lymph layer',lymph,chestframe)
# The lower body's tall canvas retains the actual upper esophageal continuation.
lowframe=(310,180,715,1536)
lower=part(empty,lowmask);emit('Lower body',lower,'name:Lower body',lowframe)
# Kidney-free digestive preparation retains the whole master's abdominal layout.
gutmask=mask([(380,546),(420,530),(474,531),(497,544),(550,541),(596,547),(636,559),(649,603),(644,641),(650,675),(645,730),(624,786),(579,809),(553,819),(528,821),(505,827),(482,814),(449,801),(417,787),(390,745),(383,685),(374,634),(378,588)])
gut=blank();gut.alpha_composite(read('abdomen-digestive').resize((320,410),Image.Resampling.LANCZOS),(355,520))
gut=part(gut,gutmask)
# The prepared upper esophagus supplies the segment normally hidden behind the chest.
es=read('digestive-regional');es=part(es,box((475,45,610,600)))
es=es.resize((round(es.width*.68),round(es.height*.68)),Image.Resampling.LANCZOS)
esc=blank();esc.alpha_composite(es,(164,165));esc.alpha_composite(gut);gut=esc
pres('id:art-digestive-tract',emit('Digestive tract at body scale',gut,trim=True))
layer('name:Lower body','id:art-digestive-tract','Lower digestive layer',gut,lowframe)
# Exactly one renal pair, with reconstructed continuous ureters, occupies the
# same body coordinates as the later whole. It is behind the digestive layer.
uri=blank();uri.alpha_composite(read('abdomen-urinary').resize((320,410),Image.Resampling.LANCZOS),(355,520))
emit('Urinary organs',uri,'id:final-urinary-organs',trim=True)
layer('name:Lower body','id:final-urinary-organs','Lower urinary layer',uri,lowframe)
# Head and one anterior vertebral column: cord remains in its natural canal.
headframe=(390,0,625,940)
sp=read('head-spine-complete');column=sp.crop((390,195,635,1180));column=column.resize((181,729),Image.Resampling.LANCZOS)
head=blank();head.alpha_composite(column,(420,195));head.alpha_composite(part(body,box((390,0,610,200))))
eye=mask([(486,90),(510,81),(541,84),(557,95),(556,111),(538,119),(514,113),(491,112),(476,106)])
ear=mask([(416,110),(433,100),(448,104),(465,115),(484,123),(481,143),(467,155),(465,175),(446,178),(430,160),(417,142)])
headbase=head.copy();eh=read('head-empty').resize((220,200));headbase.paste(eh,(390,0),eh)
pres('id:nervous-system-model',emit('Head and spine',headbase,frame=headframe))
eyep=part(head,eye);earp=part(head,ear)
pres('id:art-eye-with-optic-nerve',emit('Eye at body scale',eyep,trim=True))
emit('Ears',earp,'id:final-ears',trim=True)
layer('id:nervous-system-model','id:art-eye-with-optic-nerve','Head eye layer',eyep,headframe)
layer('id:nervous-system-model','id:final-ears','Head ear layer',earp,headframe)
# The body-shaped skin covering's patch lies flush on its original surface.
patchmask=mask([(220,681),(249,680),(260,694),(247,716),(230,737),(210,745),(203,730),(211,706)])
patch=part(skin,patchmask);skinbase=minus(skin,patchmask)
fullframe=(100,0,910,1536)
emit('Skin covering',skinbase,'name:Skin covering',fullframe)
pres('id:art-repaired-skin-segment',emit('Repaired skin at body scale',patch,trim=True))
layer('name:Skin covering','id:art-repaired-skin-segment','Skin repaired layer',patch,fullframe)
# Regional joins reveal the same whole, with one central spine hidden posteriorly.
# Replace only the abdominal contents with the exact prepared constituents.
# Outer walls, chest, arms, head and legs preserve the accepted source pixels.
abdomenmask=mask([(380,546),(409,532),(455,527),(496,535),(550,534),(610,544),(649,556),
 (650,675),(645,730),(624,786),(600,824),(565,850),(548,875),(528,891),
 (520,902),(516,918),(509,918),(505,901),(495,891),(474,875),(450,850),
 (420,824),(390,745),(383,685),(374,634),(378,588)])
abdomen=part(empty,abdomenmask);abdomen.alpha_composite(uri);abdomen.alpha_composite(part(gut,box((0,520,1024,1536))))
body.alpha_composite(abdomen)
# The same contents remain visible through the accepted skin inspection window.
finished.alpha_composite(abdomen)
trunk=minus(part(body,box((0,180,1024,1536))),chinmask)
emit('Trunk and limbs',trunk,'name:Trunk and limbs',fullframe)
emit('Body beneath the skin',body,'name:Body beneath the skin',fullframe)
emit('Body',finished,'name:Body',fullframe)
(P/'map.json').write_text(json.dumps(M,indent=2)+'\n')
print('Finale assets:',len(M['itemIcons']),'items,',sum(map(len,M['slotIcons'].values())),'slots,',len(M['presentations']),'presentations')
