"""Reproduce selected anatomy atlas crops and registered component assemblies.
Run: uv run --with pillow --with numpy python .../produce.py
No anatomical geometry is drawn: operations only crop, resize, mask and composite source pixels.
"""
from pathlib import Path
import json,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
OUT=P/'assets';OUT.mkdir(exist_ok=True)
MAP={'itemIcons':{},'slotIcons':{}}
ROOT='rework/senses-circulation/assets/'
REG={}
def clean(im):
 a=im.getchannel('A').point(lambda p:0 if p<12 else p)
 im.putalpha(a);return im
def crop(src,bounds,size=None):
 im=clean(Image.open(P/'sources'/f'{src}.png').convert('RGBA').crop(bounds))
 if size:im=im.resize(size,Image.Resampling.LANCZOS)
 return im
def tight(im,pad=10):
 b=im.getchannel('A').point(lambda a:255 if a>24 else 0).getbbox()
 if not b:raise ValueError('empty image')
 im=im.crop((max(0,b[0]-pad),max(0,b[1]-pad),min(im.width,b[2]+pad),min(im.height,b[3]+pad)))
 return im
def fit(im,w=None,h=None):
 im=tight(im)
 s=w/im.width if w else h/im.height
 return im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.LANCZOS)
def compose(size,*parts):
 im=Image.new('RGBA',size)
 for part,x,y in parts:im.alpha_composite(part,(x,y))
 return im
def color(im,kind):
 ar=np.asarray(im).copy();r,g,b=[ar[:,:,i].astype(float) for i in range(3)]
 if kind=='gold': m=(r>g*1.06)&(g>b*1.15)&(r>130)
 elif kind=='vascular':m=((r>g*1.30)&(r>b*1.06))|((b>r*1.22)&(b>g*1.13))
 elif kind=='oxygen':m=(b>r*1.13)&(g>r*1.06)&(b>100)
 elif kind=='muscle':m=(r>g*1.10)&(r>b*1.05)
 ar[:,:,3]=np.where(m,ar[:,:,3],0)
 return Image.fromarray(ar)
def save(name,im,keep=False):
 filename=re.sub('[^a-z0-9]+','-',name.lower()).strip('-')+'.png'
 im=im if keep else tight(im)
 im.save(OUT/filename)
 MAP['itemIcons']['name:'+name]=ROOT+filename
 return im
# Ear: one representative cutaway and a located cochlear enlargement, constant piece sizes.
e0=fit(crop('ear',(0,0,492,513)),w=350)
drum=crop('ear',(705,100,923,470));dm=Image.new('L',drum.size);dd=ImageDraw.Draw(dm)
# The foreground oval is complete; the rear oval is excluded by its silhouette.
dd.polygon([(x-705,y-100) for x,y in [(850,111),(868,115),(892,148),(907,197),(914,244),(904,290),(886,336),(864,382),(837,418),(808,444),(777,460),(750,454),(729,437),(717,411),(710,379),(712,344),(720,303),(731,267),(746,228),(765,191),(789,157),(818,130)]],fill=255)
drum.putalpha(Image.fromarray(np.minimum(np.array(drum.getchannel('A')),np.array(dm))))
e1=fit(drum,h=110)
e2=fit(crop('ear',(1010,90,1510,455)),w=145)
cochlea=crop('ear',(0,550,492,1000));ca=np.array(cochlea);ca[:130,470:,3]=0
# Exclude the adjacent sensory inset's tiny locator stroke at upper right.
e3=fit(Image.fromarray(ca),w=190)
sensory=crop('ear',(484,530,995,975));sa=np.array(sensory)
# Lower-left pixels belong to the neighbouring large cochlea, not this inset.
sa[120:,:22,3]=0
e4=fit(Image.fromarray(sa),w=340)
e5=fit(crop('ear',(1011,572,1535,970)),w=245)
for n,im in [('Outer ears and canals',e0),('Eardrums',e1),('Middle-ear bones',e2),('Coiled inner-ear chambers and fluid',e3),('Hearing cells with tiny hairs',e4),('Hearing pathways',e5)]:save(n,im)
def ear(outer=False,drum=False,bones=False,coil=False,sensor=False,nerve=False):
 parts=[]
 for yes,im,x,y in [(outer,e0,0,0),(drum,e1,300,170),(bones,e2,345,170),(coil,e3,470,140),(sensor,e4,390,365),(nerve,e5,640,160)]:
  if yes:parts.append((im,x,y))
 return compose((900,690),*parts)
for n,v in {'Outer ears with eardrums':(1,1,0,0,0,0),'Sound-conducting ears':(1,1,1,0,0,0),'Vibration-sensitive inner ears':(0,0,0,1,1,0),'Sound-receiving ears':(1,1,1,1,1,0),'Inner ears with hearing pathways':(0,0,0,1,1,1),'Ears':(1,1,1,1,1,1)}.items():save(n,ear(*v))
# Balance: the same two cell populations stay at a fixed enlargement.
b0=fit(crop('balance',(10,10,500,480)),w=310)
b1=fit(crop('balance',(510,10,995,475)),w=320)
b2=fit(crop('balance',(1060,20,1500,181)),w=310)
b3=fit(crop('balance',(40,530,463,704)),w=310)
b4=fit(color(crop('balance',(690,625,990,845)),'gold'),w=220)
b5=fit(crop('balance',(1050,500,1520,1000)),w=300)
weighted=compose((330,225),(b3,10,90),(b2,10,0))
turning=compose((650,330),(b0,0,0),(b1,330,0))
for n,im in [('Fluid-filled loops',b0),('Turning sensor cells',b1),('Tiny mineral weights',b2),('Tilt sensor cells',b3),('Balance nerves',b4),('Eye and posture nerve routes',b5),('Weighted balance sensors',weighted),('Turn-sensing canals',turning)]:save(n,im)
def balance(t=False,w=False,n=False,o=False):
 p=[(fit(e3,w=150),250,175)] # existing cochlea, organ locator, same in all assembled sensor views
 if t:p.extend([(b0,0,0),(b1,0,340)])
 if w:p.append((weighted,330,350))
 if n:p.append((b4,390,170))
 if o:p.append((b5,660,50))
 return compose((980,680),*p)
for name,args in {'Balance organs':(1,1,0,0),'Balance response routes':(0,0,1,1),'Turning sensors with incoming nerves':(1,0,1,0),'Weighted sensors with incoming nerves':(0,1,1,0),'Balance organs with incoming nerves':(1,1,1,0),'Turning sensors with response routes':(1,0,1,1),'Weighted sensors with response routes':(0,1,1,1),'Inner ear':(1,1,1,1)}.items():save(name,balance(*args))
# Blood: common material-scale plasma, red and white populations. Molecular views explicitly located.
c0=fit(crop('blood',(25,25,490,480)),w=360)
c1=fit(crop('blood',(530,25,990,480)),w=360)
c2=fit(crop('blood',(1025,30,1535,475)),w=520)
c3=fit(crop('blood',(15,500,490,1000)),w=380)
c4=fit(crop('blood',(500,500,950,1020)),w=450)
cellDetail=crop('blood',(975,505,1281,977)); cm=Image.new('L',cellDetail.size);cd=ImageDraw.Draw(cm)
cd.ellipse((0,145,305,445),fill=255);cd.ellipse((75,0,215,115),fill=255);cd.polygon([(105,100),(170,100),(200,165),(95,165)],fill=255)
cellDetail.putalpha(Image.fromarray(np.minimum(np.array(cellDetail.getchannel('A')),np.array(cm))))
cdetail=np.array(cellDetail);cdetail[:,275:,3]=0;cellDetail=Image.fromarray(cdetail)
c5=fit(cellDetail,w=230)
c6=fit(crop('blood',(1274,505,1535,977)),w=230)
oxbase=c6.copy();oxbase.putalpha(oxbase.getchannel('A').point(lambda a:int(a*.22)))
ox=compose(c6.size,(oxbase,0,0),(color(c6,'oxygen'),0,0))
for n,im in [('Developing red blood cells',c0),('Red blood cells',c1),('Plasma water',c2),('Plasma proteins, nutrients and salts',c4),('White cells and platelets',c3),('Iron and amino acids',c5),('Oxygen molecules',ox)]:save(n,im)
# Red cell cutaway is a persistent located enlargement when oxygen is bound.
redox=compose((620,470),(c1,0,0),(c6,380,0));save('Red cells carrying oxygen',redox)
plasma=compose((560,500),(c2,20,60),(c4,55,0));save('Plasma',plasma)
def blood(red=False,white=False):
 ps=[(plasma,0,0)]
 if red:ps.append((c1,30,65))
 if white:ps.append((c3,150,30))
 if red:ps.append((c6,560,0))
 return compose((800,520),*ps)
save('Plasma with white cells and platelets',blood(white=True));save('Plasma with oxygen-carrying red cells',blood(red=True));save('Blood',blood(True,True))
# Vessel family, same wall and lining pixels in every assembly.
v0=fit(crop('vessels',(0,85,510,435)),w=340)
v1=fit(crop('vessels',(540,160,1000,370)),w=245)
v2=fit(crop('vessels',(1020,100,1536,430)),w=340)
valve=crop('vessels',(148,635,375,845)); mask=Image.new('L',valve.size);ImageDraw.Draw(mask).polygon([(0,0),(65,20),(226,90),(226,120),(65,170),(0,205),(10,120)],fill=255);valve.putalpha(Image.fromarray(np.minimum(np.asarray(valve.getchannel('A')),np.asarray(mask))));v3=fit(valve,w=145)
v4=fit(crop('vessels',(510,565,1020,915)),w=360)
v5=fit(crop('vessels',(1030,565,1536,915)),w=360)
artery=compose((360,250),(v0,0,0),(v1,62,66))
vein=compose((360,250),(v2,0,0),(v1,62,66));venous=compose((360,250),(vein,0,0),(v3,92,60))
cap=compose((380,260),(v5,0,0),(v4,0,0))
for n,im in [('Arterial wall',v0),('Blood-facing lining cells',v1),('Venous wall',v2),('One-way valve flaps',v3),('Tiny capillary tubes',v4),('Nearby body cells',v5),('Arterial vessels',artery),('Thin-walled veins',vein),('Venous return',venous),('Capillary bed',cap)]:save(n,im)
def network(a=False,c=False,v=False):
 return compose((1000,300),*([(artery,0,20)] if a else []),*([(cap,320,20)] if c else []),*([(venous,650,20)] if v else []))
save('Distribution and exchange bed',network(1,1,0));save('Capillaries and venous return',network(0,1,1));bodyNet=save('Body blood-vessel network',network(1,1,1))
# One generated connected pulmonary/heart master supplies every chapter12 state.
# Complementary masks rejoin exact source pixels, so no assembled hilar stump remains.
hmaster=crop('heart-connected-final',(0,0,1433,1098))
ha=np.array(hmaster);hy,hx=np.indices(ha.shape[:2])
organMask=Image.new('L',hmaster.size);omd=ImageDraw.Draw(organMask)
omd.rectangle((0,0,1433,734),fill=255)
omd.polygon([(405,590),(975,590),(952,690),(918,750),(868,811),(840,842),(700,850),(465,835),(460,690)],fill=255)
# The generated locator belongs to the coronary inset, not the un-fitted organ.
omd.line([(972,494),(1118,744)],fill=0,width=14)
heartMask=Image.new('L',hmaster.size);hmd=ImageDraw.Draw(heartMask)
hmd.polygon([(480,0),(910,0),(910,285),(960,420),(980,600),(945,750),(855,845),(700,850),(465,835),(460,690),(405,550),(405,420),(450,320),(480,220)],fill=255)
organMask=np.asarray(organMask)>0;heartMask=(np.asarray(heartMask)>0)&organMask
# Geometric extraction follows the two visible major-vessel silhouettes. Colour
# thresholds would scatter highlights into the opposite half and break continuity.
am=Image.new('L',hmaster.size);ad=ImageDraw.Draw(am)
ad.polygon([(610,0),(880,0),(915,170),(900,300),(760,340),(650,380),(575,325),(575,180)],fill=255)
pm=Image.new('L',hmaster.size);pd=ImageDraw.Draw(pm)
pd.polygon([(635,420),(728,420),(760,310),(802,270),(887,250),(1008,300),(1095,335),(1080,275),(960,205),(860,185),(755,195),(700,230),(660,285)],fill=255)
rightMask=heartMask&(hx<700)&~(np.asarray(am)>0)
rightMask|=heartMask&(np.asarray(pm)>0)
leftMask=heartMask&~rightMask
netMask=organMask&~heartMask
HS=.56
HC=(round(1433*HS),round(1098*HS))
def hpart(mask):
 arr=ha.copy();arr[~mask,3]=0
 return Image.fromarray(arr).resize(HC,Image.Resampling.LANCZOS)
hr=hpart(rightMask);hl=hpart(leftMask);hlung=hpart(netMask)
horgan=hpart(organMask)
hfull=tight(hpart(heartMask)) # consumed by chest construction; connected master retained below
for n,im in [('Right side of heart',hr),('Left side of heart',hl),('Lung blood-vessel network',hlung)]:save(n,im)
# One muscle patch, decomposed into artery versus capillaries/veins and supporting fibres.
patch=crop('heart-connected-final',(895,740,1420,1075));pm=Image.new('L',patch.size);pd=ImageDraw.Draw(pm)
for line,width in [([(0,167),(60,166),(105,184),(147,225),(190,234)],24),([(65,163),(115,120),(150,107),(190,96)],16),([(147,109),(190,59),(231,31)],8),([(82,166),(150,163),(205,146)],13),([(180,234),(230,247),(279,280)],9)]:pd.line(line,fill=255,width=width,joint='curve')
pa=np.asarray(patch);ma=np.asarray(pm)>0
arterial=pa.copy();arterial[~ma,3]=0
venous=pa.copy();venous[ma,3]=0
patchsize=(round(patch.width*HS),round(patch.height*HS))
hart=Image.fromarray(arterial).resize(patchsize,Image.Resampling.LANCZOS)
hven=Image.fromarray(venous).resize(patchsize,Image.Resampling.LANCZOS)
coronary=compose(patchsize,(hart,0,0),(hven,0,0))
for n,im in [('Arteries for the heart muscle',hart),('Heart-muscle capillaries and veins',hven),('Heart-muscle vessel network',coronary)]:save(n,im)
# Explicit organ-to-microcirculation annotations accompany the existing body bed.
def heart(right=False,left=False,lung=False,body=False,cor=False):
 p=[]
 if lung:p.append((hlung,100,0))
 if right:p.append((hr,100,0))
 if left:p.append((hl,100,0))
 if body:p.append((bodyNet,0,670))
 if cor:p.append((coronary,590,475))
 im=compose((1000,980),*p)
 d=ImageDraw.Draw(im)
 def arrow(points,colour):
  d.line(points,fill=colour,width=4)
  x,y=points[-1];px,py=points[-2];dx,dy=x-px,y-py;length=(dx*dx+dy*dy)**.5;ux,uy=dx/length,dy/length
  d.polygon([(x,y),(x-ux*17-uy*8,y-uy*17+ux*8),(x-ux*17+uy*8,y-uy*17-ux*8)],fill=colour)
 if body and left:arrow([(480,20),(50,20),(50,650),(85,650),(85,690)],'#ff939d')
 if body and right:arrow([(930,690),(960,690),(960,650),(355,650),(355,455)],'#74c9fb')
 if cor:d.line([(580,190),(620,460),(650,475)],fill='#60d6df',width=3)
 return im
save('Right heart and lung route',heart(1,0,1,0));save('Left heart and body route',heart(0,1,0,1));save('Heart and two routes',heart(1,1,1,1));save('Heart with connected vessels',heart(1,1,1,1,1))
# Shared connected organ-only raster for the chapter14/28 compositor.
horgan.save(OUT/'heart-pulmonary-connected-reference.png')
# Lung sac populations and located magnification remain registered.
l0=crop('lungs',(25,0,495,539),(520,600))
lcap=color(crop('lungs',(545,0,1015,539),(520,600)),'vascular')
lelast=color(crop('lungs',(1050,0,1520,539),(520,600)),'gold')
ltree=crop('lungs',(525,556,1008,1015),(490,350))
lpipe=fit(crop('lungs',(105,555,400,1018)),h=240)
def sacs(c=False,e=False):return compose((520,600),(l0,0,0),*([(lcap,0,0)] if c else []),*([(lelast,0,0)] if e else []))
for n,im in [('Tiny air sacs',l0),('Lung capillaries',lcap),('Elastic supporting tissue',lelast),('Windpipe',lpipe),('Branching air tubes',ltree),('Air sacs with blood vessels',sacs(1,0)),('Elastic air sacs',sacs(0,1)),('Elastic air sacs with blood vessels',sacs(1,1))]:save(n,im)
airways=compose((560,670),(ltree,30,170),(lpipe,205,0));save('Branching airways',airways)
lung=compose((560,780),(sacs(1,1),20,170),(ltree,30,170),(lpipe,205,0));save('Lungs',lung)
# Chest slots all share exactly 1000x1100 registration. Generated rib pixels stay visible.
rib=crop('chest',(15,0,710,724),(680,710))
musc=color(crop('chest',(745,0,1420,724),(680,710)),'muscle')
diap=fit(crop('chest',(1470,285,2160,723)),w=600)
chestsize=(1000,1100)
base=compose(chestsize,(musc,160,110),(rib,160,110))
save('Rib cage',rib);save('Muscles between the ribs',musc);save('Diaphragm',diap);save('Breathing apparatus',base,True)
# Organ-only view retains airway and blood-vessel sources, inset below is not in the thorax.
organSacs=sacs(1,1); om=Image.new('L',organSacs.size);od=ImageDraw.Draw(om)
for poly in [[(35,350),(44,270),(74,170),(115,75),(165,23),(220,0),(250,14),(253,98),(247,233),(222,268),(105,320)],[(268,11),(301,2),(338,19),(377,71),(419,158),(455,235),(470,335),(444,349),(342,299),(281,261),(267,201)]]:
 od.polygon([(round((x-25)*520/470),round(y*600/539)) for x,y in poly],fill=255)
organSacs.putalpha(Image.fromarray(np.minimum(np.array(organSacs.getchannel('A')),np.array(om))))
localLung=compose((560,650),(organSacs,20,170),(ltree,30,170),(lpipe,205,0))
localHeart=hfull.resize((230,262),Image.Resampling.LANCZOS)
heartLungs=compose((680,780),(localLung,60,0),(localHeart,290,245))
save('Heart and lungs',heartLungs)
riblite=rib.copy();riblite.putalpha(riblite.getchannel('A').point(lambda a:int(a*.55)))
orglayer=compose(chestsize,(heartLungs,160,40),(riblite,160,110))
diaplayer=compose(chestsize,(diap,200,600))
for key,im in [('heart-and-lungs',orglayer),('diaphragm',diaplayer)]:im.save(OUT/f'breathing-slot-{key}.png')
MAP['slotIcons']['name:Breathing apparatus']={'name:Heart and lungs':ROOT+'breathing-slot-heart-and-lungs.png','name:Diaphragm':ROOT+'breathing-slot-diaphragm.png'}
# Neck junction uses the exact generated green/blue junction from the lymph family.
lymph=crop('lymph-atlas-shared',(1000,540,1490,1000),(360,338))
lymphlayer=compose(chestsize,(lymph,430,110))
lymphlayer.save(OUT/'breathing-slot-lymph.png')
MAP['slotIcons']['name:Breathing apparatus']['name:Lymph drainage network']=ROOT+'breathing-slot-lymph.png'
# Cross-package source components are copied here before final run.
for key,name,box in [('arm','Arm assembly',(0,185,250,985)),]:
 path=P/'sources'/f'{key}-shared.png'
 if path.exists():
  im=fit(Image.open(path).convert('RGBA'),h=box[3]-box[1])
  if im.width>box[2]-box[0]:im=fit(im,w=box[2]-box[0])
  layer=compose(chestsize,(im,box[0],box[1]));layer.save(OUT/f'breathing-slot-{key}.png')
  MAP['slotIcons']['name:Breathing apparatus']['name:'+name]=ROOT+f'breathing-slot-{key}.png'
complete=compose(chestsize,(base,0,0),(orglayer,0,0),(diaplayer,0,0));complete.save(OUT/'chest-complete-reference.png')
(P/'map.json').write_text(json.dumps(MAP,indent=2)+'\n')
# Disposable review sheet, one-quarter intrinsic pixels; no independent normalization.
scratch=P.parents[5]/'runs'/'anatomy-star-rework'
scratch.mkdir(parents=True,exist_ok=True)
items=list(MAP['itemIcons'].items())
for page in range((len(items)+11)//12):
 sheet=Image.new('RGB',(1200,1100),'#031827');d=ImageDraw.Draw(sheet)
 for j,(name,path) in enumerate(items[page*12:(page+1)*12]):
  im=Image.open(OUT/Path(path).name); im=im.resize((max(1,im.width//4),max(1,im.height//4)),Image.Resampling.LANCZOS)
  x=(j%4)*300;y=(j//4)*365
  sheet.paste(im,(x+8,y+28),im);d.text((x+8,y+8),name[5:],fill='white')
 sheet.save(scratch/f'senses-review-{page}.jpg')
print(f'{len(items)} item identities; {sum(len(s) for s in MAP["slotIcons"].values())} slots')
