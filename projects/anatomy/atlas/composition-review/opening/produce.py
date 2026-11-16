"""Mechanical extraction and registration of selected generated anatomy."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
import json
import numpy as np
P=Path(__file__).resolve().parent;A=P/'assets';A.mkdir(exist_ok=True)
OLD=P.parents[1]/'opening/assets';L=Image.Resampling.LANCZOS
M={'itemIcons':{},'slotIcons':{},'hotspots':{},'placements':{}}
def trim(im):
 im=im.convert('RGBA');a=im.getchannel('A').point(lambda v:0 if v<18 else v);im.putalpha(a);b=a.getbbox();return im.crop(b) if b else im

def fit(im,w,h):
 s=min(w/im.width,h/im.height);return im.resize((round(im.width*s),round(im.height*s)),L)
def load(name):return Image.open(OLD/(name+'.png')).convert('RGBA')
def save(name,im,id=None):
 im.save(A/(name+'.png'));p='atlas/composition-review/opening/assets/'+name+'.png'
 if id:M['itemIcons'][id]=p
 return p
raw=Image.open(P/'sources/cell-master.png').convert('RGBA');mem=fit(trim(raw.crop((0,0,1100,raw.height))),740,740);save('membrane',mem,'id:prelude-phospholipids')
carrier=fit(trim(raw.crop((1150,0,raw.width,raw.height))),130,120);save('carrier',carrier,'id:school-sugar-carrier')
cell=load('cell');M['slotIcons']['id:opening-cell']={}
# Keep actual component dimensions consistent within this assembly.
nucleus=fit(load('nucleus'),280,280);save('nucleus',nucleus,'id:opening-nucleus');save('nuclear-envelope',fit(load('nuclear-envelope'),280,280),'id:opening-nuclear-envelope');save('dna',fit(load('dna'),180,180),'id:opening-dna')
mito=fit(load('mitochondria'),255,220);save('mitochondria',mito,'id:opening-mitochondria')
rib=fit(load('ribosome'),90,78);save('ribosome',rib,'id:school-ribosome')
complete=cell.copy()
for id,name,im,xy in [('id:opening-nucleus','nucleus',nucleus,(230,235)),('id:opening-mitochondria','mitochondria',mito,(445,455)),('id:school-sugar-carrier','carrier',carrier,(0,325))]:
 layer=Image.new('RGBA',cell.size);layer.alpha_composite(im,xy);M['slotIcons']['id:opening-cell'][id]=save('fitted-'+name,layer);complete.alpha_composite(layer)
layer=Image.new('RGBA',cell.size)
for xy in [(550,240),(190,500),(410,635)]:layer.alpha_composite(rib,xy)
M['slotIcons']['id:opening-cell']['id:school-ribosome']=save('fitted-ribosomes',layer);complete.alpha_composite(layer)
save('embryonic-cell',fit(complete,380,380),'id:prelude-daughters')
raw=Image.open(P/'sources/bone-cell-master.png').convert('RGBA')
save('bone-cell',fit(trim(raw.crop((0,0,1080,raw.height))),380,380),'id:arm-bone-cells')
save('bmp2',fit(trim(raw.crop((1150,0,raw.width,raw.height))),230,200),'id:arm-bmp2')
# Arm: physically meaningful bone boundaries selected from the matching bone master.
bones=Image.open(P/'sources/arm-bones.png').convert('RGBA');whole=Image.open(P/'sources/arm-origins-v2.png').convert('RGBA')
for im in [bones,whole]:im.putalpha(im.getchannel('A').point(lambda v:0 if v<24 else v))
def poly(size,pts):
 m=Image.new('L',size);ImageDraw.Draw(m).polygon(pts,fill=255);return m
def masked(im,m):
 out=im.copy();out.putalpha(ImageChops.multiply(im.getchannel('A'),m));return out
shoulder=poly(bones.size,[(0,0),(1024,0),(1024,650),(580,650),(570,260),(585,205),(565,165),(540,140),(460,135),(455,100),(0,100)])
upper=poly(bones.size,[(0,0),(1024,0),(1024,690),(574,690),(550,712),(518,728),(480,715),(445,729),(410,708),(390,690),(0,690)])
ulna=poly(bones.size,[(551,709),(574,736),(557,788),(511,850),(460,941),(405,1039),(362,1098),(334,1114),(322,1091),(347,1036),(385,942),(436,847),(474,777),(482,752),(503,721)])
forearm=poly(bones.size,[(0,0),(1024,0),(1024,1090),(365,1090),(350,1110),(310,1108),(275,1108),(240,1088),(0,1088)])
biceps=poly(whole.size,[(601,120),(621,125),(598,175),(538,232),(500,330),(484,505),(450,644),(421,774),(397,782),(411,652),(404,531),(405,446),(430,338),(464,250),(500,204),(575,151)])
stages=[('arm-shoulder',masked(bones,shoulder)),('arm-humerus',masked(bones,upper)),('arm-humerus-ulna',masked(bones,ImageChops.lighter(upper,ulna))),('arm-long-bones',masked(bones,forearm)),('arm-skeleton',bones)]
withbi=Image.open(P/'sources/arm-biceps-v2.png').convert('RGBA');withbi.putalpha(withbi.getchannel('A').point(lambda v:0 if v<24 else v));stages += [('arm-with-biceps',withbi),('arm-with-muscles',whole)]
M['hotspots']['4']={}
for name,im in stages:
 # Same full canvas for fixed receivers, so no stage magnification change.
 export=im.resize((900,1350),L);save(name,export,'id:'+name)
 b=export.getchannel('A').point(lambda a:255 if a>40 else 0).getbbox();x0,y0,x1,y1=b
 M['hotspots']['4']['id:'+name]={'center':[780,1010],'hitbox':{'center':[780-450+(x0+x1)/2,1010-675+(y0+y1)/2],'size':[x1-x0,y1-y0]}}
# Keep the recognizable osteoblast's scale while its extracellular matrix grows.
tissue=Image.open(P/'sources/bone-tissue.png').convert('RGBA');mid=tissue.width//2
save('soft-bone-tissue',fit(trim(tissue.crop((0,0,mid,tissue.height))),540,540),'id:arm-soft-bone')
save('mineralized-bone-tissue',fit(trim(tissue.crop((mid,0,tissue.width,tissue.height))),540,540),'id:arm-bone-tissue')
# Final neuronal family: full matched channel state avoids rectangular fitting patches.
from PIL import ImageFilter
nr=Image.open(P/'sources/neuron-family-v3.png').convert('RGBA')
channelstate=Image.open(P/'sources/neuron-channel-state-v3.png').convert('RGBA').resize(nr.size,L)
bare=Image.open(P/'sources/neuron-bare-v3.png').convert('RGBA').resize(nr.size,L)
# Only the local generated bare membrane replaces the channel; all other pixels stay shared.
patch=Image.new('L',nr.size);ImageDraw.Draw(patch).rectangle((528,293,632,390),fill=255);patch=patch.filter(ImageFilter.GaussianBlur(5))
base=Image.composite(bare,channelstate,patch)
size=(1160,round(1160*nr.height/nr.width))
save('neuron',base.resize(size,L),'id:school-neurons')
M['slotIcons']['id:school-neurons']={}
M['slotIcons']['id:school-neurons']['id:school-ion-channels']=save('neuron-channels',channelstate.resize(size,L))
m=Image.new('L',nr.size);d=ImageDraw.Draw(m)
for box in [(630,215,1018,470),(1018,215,1415,470),(1415,215,1814,470)]:d.rectangle(box,fill=255)
M['slotIcons']['id:school-neurons']['id:neural-wrapping-cells']=save('neuron-sheaths',masked(nr,m).resize(size,L))
save('ion-channel',fit(trim(nr.crop((940,475,1230,nr.height))),140,140),'id:school-ion-channels')
# One established cell may stand for each appropriately prepared descendant population.
representative=Image.open(A/'embryonic-cell.png').convert('RGBA')
save('spinal-precursor',representative,'id:neural-spinal-precursors')
save('schwann-precursor',representative,'id:neural-schwann-precursors')

(P/'map.json').write_text(json.dumps(M,indent=2)+'\n')
