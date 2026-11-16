#!/usr/bin/env python3
"""Mechanical extraction and registration; all depicted anatomy comes from source masters."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json
import numpy as np
from scipy import ndimage
P=Path(__file__).resolve().parent; A=P/'assets'; A.mkdir(exist_ok=True)
M={'itemIcons':{},'slotIcons':{},'hotspots':{},'placements':{}}
L=Image.Resampling.LANCZOS

def trim(im):
    im=im.convert('RGBA'); a=im.getchannel('A'); a=a.point(lambda v: 0 if v<12 else v); im.putalpha(a)
    mask=np.asarray(a)>12
    labels,n=ndimage.label(ndimage.binary_dilation(mask,iterations=2))
    if n:
        counts=np.bincount(labels.ravel()); counts[0]=0
        keep=counts>=max(20,counts.max()*.015)
        ar=np.asarray(a).copy(); ar[~keep[labels]]=0; a=Image.fromarray(ar); im.putalpha(a)
    box=a.getbbox()
    return im.crop(box) if box else im

def extract(master,col,row,cols,rows,box=None):
    im=Image.open(P/'sources'/f'{master}.png').convert('RGBA');w,h=im.size
    if master=='development':
        yy=[(0,365),(380,690),(695,1024)][row];box=(int(col*w/3),yy[0],int((col+1)*w/3),yy[1])
    if master=='organelle' and row==1 and col==0: box=(40,375,450,672)
    return trim(im.crop(box or (int(col*w/cols),int(row*h/rows),int((col+1)*w/cols),int((row+1)*h/rows))))

def fit(im,w=None,h=None):
    s=min(w/im.width if w else 1e5,h/im.height if h else 1e5)
    return im.resize((round(im.width*s),round(im.height*s)),L)

def canvas(w,h):return Image.new('RGBA',(w,h))
def put(base,im,xy):base.alpha_composite(im,tuple(map(round,xy)));return base

def save(name,im,ids=()):
    im.save(A/f'{name}.png');path=f'atlas/opening/assets/{name}.png'
    for id in ids:M['itemIcons'][id]=path
    return path

def supply(master,col,row,cols,rows,name,ids,w=340,h=340):
    im=fit(extract(master,col,row,cols,rows),w,h);save(name,im,ids);return im

# Cell geometry: free material anticipates its installed proportions.
mem=supply('cell',0,0,3,2,'lipid-membrane',['id:prelude-phospholipids'],740,740)
water=supply('cell',1,0,3,2,'water',['id:prelude-water'],520,520)
cell=fit(extract('cell',2,0,3,2),840,840);save('cell',cell,['id:opening-cell'])
envelope=supply('cell',0,1,3,2,'nuclear-envelope',['id:opening-nuclear-envelope'],320,320)
dna=supply('cell',1,1,3,2,'dna',['id:opening-dna'],220,220)
supply('cell',2,1,3,2,'nuclear-envelope-alternative',[],320,320)
nucleus=envelope.copy();d=fit(dna,205,205);put(nucleus,d,((nucleus.width-d.width)/2,(nucleus.height-d.height)*.68));save('nucleus',nucleus,['id:opening-nucleus'])
organelles={}
for n,(name,id,w,h) in enumerate([
 ('mitochondria','id:opening-mitochondria',300,260),('sugar-carrier','id:school-sugar-carrier',130,170),('ribosome','id:school-ribosome',180,160),
 ('glucose','id:school-glucose',210,210),('atp','id:school-atp',300,200),('protein','id:school-protein',270,270),
 ('amino-acids','id:school-amino-acids',280,210),('sonic-hedgehog','id:school-muscle-signals',200,170),('tgf-beta2','id:school-support-signals',230,170)]):
 organelles[name]=supply('organelle',n%3,n//3,3,3,name,[id],w,h)
M['slotIcons']['id:opening-cell']={}
for id,name,im,xy in [('id:opening-nucleus','cell-nucleus',fit(nucleus,280,280),(230,235)),('id:opening-mitochondria','cell-mitochondria',fit(organelles['mitochondria'],255,220),(445,455)),('id:school-sugar-carrier','cell-carrier',fit(organelles['sugar-carrier'],82,110),(8,340))]:
 layer=canvas(*cell.size);put(layer,im,xy);M['slotIcons']['id:opening-cell'][id]=save(name,layer)
layer=canvas(*cell.size);r=fit(organelles['ribosome'],75,65)
for xy in [(550,240),(190,500),(410,635)]:put(layer,r,xy)
M['slotIcons']['id:opening-cell']['id:school-ribosome']=save('cell-ribosomes',layer)
for n,(name,id,w,h) in enumerate([
 ('embryonic-cells','id:prelude-daughters',380,360),('muscle-rna-cells','id:school-young-muscle',400,320),('muscle-cells','id:prelude-myoblasts',420,290),
 ('tendon-rna-cells','id:school-young-support',400,300),('tendon','id:prelude-matrix',450,280),('spinal-precursors','id:neural-spinal-precursors',310,310),
 ('schwann-precursors','id:neural-schwann-precursors',350,240),('schwann-cell','id:neural-wrapping-cells',300,230),('neuregulin-source','id:neural-wrapping-messengers',580,280)]):
 supply('development',n%3,n//3,3,3,name,[id],w,h)
M['hotspots']['5']={'id:neural-wrapping-messengers':{'center':[780,600]}}
M['placements'].update({'id:neural-spinal-precursors':[780,1250],'id:neural-schwann-precursors':[340,1670],'id:school-ion-channels':[1000,1670]})
# Later plates extend this script below.
(P/'map.json').write_text(json.dumps(M,indent=2)+'\n')
# Neuron: one continuous cell, with small fitted channels and real membrane sleeves.
neur=fit(extract('neuron',0,0,3,1,box=(0,70,1160,640)),1050,510)
save('neuron',neur,['id:school-neurons'])
channel=fit(extract('neuron',1,0,3,1,box=(1170,100,1660,640)),130,150);save('ion-channel',channel,['id:school-ion-channels'])
sleeve=fit(extract('neuron',2,0,3,1,box=(1700,105,2172,285)),150,70)
M['slotIcons']['id:school-neurons']={}
layer=canvas(*neur.size);c=fit(channel,23,32)
for x in [440,610,780,900]:put(layer,c,(x,neur.height*.51-15))
M['slotIcons']['id:school-neurons']['id:school-ion-channels']=save('neuron-channels',layer)
layer=canvas(*neur.size)
for x in [450,620,790]:put(layer,sleeve,(x,neur.height*.51-32))
M['slotIcons']['id:school-neurons']['id:neural-wrapping-cells']=save('neuron-wrapping',layer)
# Brain, protective bones and nerves share one long vertical registered whole.
brain=fit(extract('nervous',0,0,3,2),310,350);skull=fit(extract('nervous',1,0,3,2),420,470)
cord=fit(extract('nervous',2,0,3,2),200,830);spine=fit(extract('nervous',0,1,3,2),280,970)
sensory=fit(extract('nervous',1,1,3,2),360,190);motor=fit(extract('nervous',2,1,3,2),360,190)
for n,im,id in [('brain',brain,'brain-model'),('skull',skull,'school-skull'),('cord',cord,'spinal-cord-model'),('backbone',spine,'school-backbone'),('sensory-root',sensory,'sensory-routes'),('motor-root',motor,'motor-routes')]:save(n,im,['id:'+id])
protected=skull.copy();b=fit(brain,270,290);put(protected,b,(100,20));save('protected-brain',protected,['id:school-protected-brain'])
back=spine.copy();c=fit(cord,125,810);put(back,c,((back.width-c.width)/2,10));save('protected-cord',back,['id:school-protected-cord'])
central=canvas(470,1350);put(central,back,(210-back.width/2,350));put(central,protected,(20,0));central=trim(central);save('central-nervous-system',central,['id:central-nervous-system-model'])
def tip(im):
 ar=np.asarray(im.getchannel('A'));ys,xs=np.where(ar>90);edge=xs.max()-6;return (float(xs[xs>=edge].mean()),float(ys[xs>=edge].mean()))
m=motor.rotate(18,expand=True,resample=Image.Resampling.BICUBIC);st=tip(sensory);mt=tip(m)
root=canvas(450,350);put(root,sensory,(20,40));put(root,m,(20+st[0]-mt[0],40+st[1]-mt[1]));root=trim(root);save('spinal-nerve',root,['id:school-peripheral-nerves'])
ns=canvas(680,central.height);put(ns,central,((680-central.width)/2,0));rootfit=fit(root,150,100)
for y in [460,565,670,775,880]:
 put(ns,rootfit,(340,y));put(ns,rootfit.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(340-rootfit.width,y))
ns=trim(ns);save('nervous-system',ns,['id:nervous-system-model'])
# Eye: mechanically isolate fitting states from ONE continuous organ master.
# All masks select existing generated anatomy; none paints new tissue.
raw=Image.open(P/'sources'/'eye-whole.png').convert('RGBA')
def maskpoly(points):
 m=Image.new('L',raw.size);ImageDraw.Draw(m).polygon(points,fill=255);return m
def selected(mask):
 im=raw.copy();im.putalpha(ImageChops.multiply(im.getchannel('A'),mask));return im
def eyedraw(im):
 return trim(im.resize((1060,707),L))
corneamask=maskpoly([(280,290),(252,400),(248,630),(284,760),(220,740),(148,670),(110,570),(110,470),(155,380),(218,320)])
irismask=maskpoly([(286,313),(310,350),(319,460),(319,620),(308,713),(286,739),(254,640),(250,420)])
lensmask=Image.new('L',raw.size);ImageDraw.Draw(lensmask).ellipse((322,375,465,695),fill=255)
frontmask=maskpoly([(0,0),(470,0),(470,1024),(0,1024)])
rearmask=ImageChops.invert(frontmask)
def ring(outer,inner):
 m=Image.new('L',raw.size);d=ImageDraw.Draw(m);d.ellipse(outer,fill=255);d.ellipse(inner,fill=0);return ImageChops.multiply(m,rearmask)
photomask=ring((170,85,1135,945),(200,110,1110,920))
neuralmask=ring((200,110,1110,920),(230,140,1080,890));ImageDraw.Draw(neuralmask).polygon([(1060,440),(1430,430),(1430,605),(1060,575)],fill=255)
for name,mask,id in [('cornea',corneamask,'Clear dome (cornea)'),('lens',lensmask,'Clear lens'),('iris',irismask,'Coloured muscle ring (iris)'),('photoreceptors',photomask,'Light-sensitive cells'),('retinal-cells',neuralmask,'Retinal nerve cells')]:save(name,eyedraw(selected(mask)),['name:'+id])
for name,remove,id in [('focusing-front',irismask,'Focusing eye front'),('cornea-iris',lensmask,'Cornea and iris'),('eye-front',Image.new('L',raw.size),'Light-controlling eye front')]:
 mask=ImageChops.subtract(frontmask,remove);save(name,eyedraw(selected(mask)),['name:'+id])
save('retina-nerve',eyedraw(selected(rearmask)),['name:Retina with optic nerve'])
eye=eyedraw(raw);save('eye',eye,['name:Eye with optic nerve'])
# Ear assemblies use the same pieces; the sensory strip fits INSIDE its coil.
outer=fit(extract('ear',0,0,3,2),480,480);drum=fit(extract('ear',1,0,3,2),88,190);bones=fit(extract('ear',2,0,3,2),225,190)
coil=fit(extract('ear',0,1,3,2),350,340);hair=fit(extract('ear',1,1,3,2),150,110)
for n,im,id in [('outer-ear',outer,'Outer ears and canals'),('eardrum',drum,'Eardrums'),('ear-bones',bones,'Middle-ear bones'),('cochlea',coil,'Coiled inner-ear chambers and fluid'),('hair-cells',hair,'Hearing cells with tiny hairs')]:save(n,im,['name:'+id])
sensing=coil.copy();put(sensing,hair,(135,177));save('sensing-cochlea',sensing,['name:Vibration-sensitive inner ears'])
canvasEar=(1100,650);out=canvas(*canvasEar);put(out,outer,(0,0));put(out,drum,(435,155));save('outer-eardrum',trim(out),['name:Outer ears with eardrums'])
put(out,bones,(480,155));save('conducting-ear',trim(out),['name:Sound-conducting ears'])
put(out,sensing.rotate(-35,expand=True,resample=Image.Resampling.BICUBIC),(570,105));save('ear',trim(out),['name:Ears'])
# A plain backing is shared by the whole edition.
Image.new('RGB',(1560,2340),(250,247,238)).save(P.parent/'blank-paper.png')
heading=canvas(840,840);put(heading,cell,((840-cell.width)/2,0));put(heading,fit(nucleus,280,280),(230,235));save('heading',heading)
(P/'map.json').write_text(json.dumps(M,indent=2)+'\n')
# Disposable montage for informed production inspection; never a runtime asset.
thumbs=[]
for name in ['cell','nucleus','glucose','embryonic-cells','muscle-cells','neuron','protected-brain','protected-cord','nervous-system','eye','ear']:
 im=Image.open(A/f'{name}.png');thumb=Image.new('RGBA',(340,380),(250,247,238,255));v=fit(im,320,350);put(thumb,v,((340-v.width)/2,(380-v.height)/2));thumbs.append(thumb)
proof=Image.new('RGBA',(340*4,380*3),(250,247,238,255))
for i,im in enumerate(thumbs):put(proof,im,((i%4)*340,(i//4)*380))
proof.convert('RGB').save(Path.cwd()/'runs/anatomy-atlas/opening-proof.jpg')
