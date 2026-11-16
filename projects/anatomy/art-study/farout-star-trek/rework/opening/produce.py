"""Extract and compose generated anatomical pixels; never draws anatomy.
Run: uv run --with pillow --with numpy python .../opening/produce.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFilter, ImageOps
import numpy as np
import json
R=Path(__file__).resolve().parent;S=R/'sources';A=R/'assets';A.mkdir(exist_ok=True)
PREFIX='rework/opening/assets/'
icons={};slots={};hotspots={};registration={}
def read(name):return Image.open(S/(name+'.png')).convert('RGBA')
def clean(im):
 a=im.getchannel('A').point(lambda x:0 if x<36 else x);im.putalpha(a);return im

def tight(im):
 im=clean(im.copy());box=im.getbbox();return im.crop(box) if box else im

def fit(im,size):return ImageOps.contain(im,size,Image.Resampling.LANCZOS)
def save(im,name):im.save(A/(name+'.png'));return PREFIX+name+'.png'
def item(key,im,name):icons[key]=save(im,name);return im
def layer(part,size,xy):
 im=Image.new('RGBA',size);im.alpha_composite(part,xy);return im

def composite(size,parts):
 im=Image.new('RGBA',size)
 for part,xy in parts:im.alpha_composite(part,xy)
 return im

def atlas(name,boxes):
 im=read(name);return [tight(im.crop(b)) for b in boxes]
# A single cell image supplies all membrane/water pixels, at one shared scale.
master=clean(read('cell-master'));box=(60,35,1230,1165);cell=master.crop(box).resize((800,773),Image.Resampling.LANCZOS)
item('id:opening-cell',cell,'cell')
inner=Image.new('L',master.size);ImageDraw.Draw(inner).ellipse((185,165,1108,1040),fill=255)
water=master.copy();water.putalpha(ImageChops.multiply(master.getchannel('A'),inner))
water=water.crop(box).resize(cell.size,Image.Resampling.LANCZOS)
item('id:prelude-water',water,'cell-water')
membrane=master.copy();membrane.putalpha(ImageChops.multiply(master.getchannel('A'),ImageChops.invert(inner)))
# Four matching membrane arcs: split at clean gutters and separate slightly. This
# is the same phospholipid population as the finished wall, not enlarged symbols.
lipids=Image.new('RGBA',master.size)
for b,offset in [((0,0,630,585),(-12,-12)),((658,0,1312,585),(12,-12)),((0,615,630,1199),(-12,12)),((658,615,1312,1199),(12,12))]:
 p=membrane.crop(b);lipids.alpha_composite(p,(b[0]+offset[0],b[1]+offset[1]))
item('id:prelude-phospholipids',lipids.crop(box).resize(cell.size,Image.Resampling.LANCZOS),'membrane-material')
parts=atlas('cell-parts',[(15,15,410,415),(420,15,830,415),(837,15,1254,415),(15,425,410,820),(420,425,830,820),(837,425,1254,820),(15,835,410,1254),(420,835,830,1254),(837,835,1254,1254)])
envelope=fit(parts[0],(228,228));dna=fit(parts[1],(142,142))
item('id:opening-nuclear-envelope',envelope,'nuclear-envelope');item('id:opening-dna',dna,'dna')
nucleus=composite((240,240),[(envelope,(6,6)),(dna,(63,45))]);item('id:opening-nucleus',nucleus,'nucleus')
mito=fit(parts[2],(190,170));carrier=fit(parts[3],(80,110));ribo=fit(parts[4],(112,112))
for key,im,name in [('id:opening-mitochondria',mito,'mitochondria'),('id:school-sugar-carrier',carrier,'sugar-carrier'),('id:school-ribosome',ribo,'ribosomes'),('id:school-glucose',fit(parts[5],(210,140)),'glucose'),('id:school-atp',fit(parts[6],(200,180)),'atp'),('id:school-protein',fit(parts[7],(215,215)),'protein'),('id:school-amino-acids',fit(parts[8],(200,165)),'amino-acids')]:item(key,im,name)
slots['id:opening-cell']={}
for key,part,xy,name in [('id:opening-nucleus',nucleus,(280,230),'nucleus'),('id:opening-mitochondria',mito,(205,470),'mitochondria'),('id:school-sugar-carrier',carrier,(691,340),'carrier'),('id:school-ribosome',ribo,(510,475),'ribosomes')]:
 slots['id:opening-cell'][key]=save(layer(part,cell.size,xy),'cell-fit-'+name)
complete=cell.copy()
for path in slots['id:opening-cell'].values():complete.alpha_composite(Image.open(R.parent.parent/path))
save(complete,'cell-complete')
heading=Image.new('RGBA',(512,512));h=fit(complete,(470,470));heading.alpha_composite(h,((512-h.width)//2,(512-h.height)//2));save(heading,'heading')
registration['cell']={'source':box,'canvas':cell.size,'method':'The exact finished membrane and aqueous interior produce the loose materials. Four separated membrane arcs retain the finished wall’s molecular scale; all fitted parts use their loose dimensions.'}
# Development uses measured atlas cells. Molecules are small relative to the cells
# they signal; before/after cells retain the same source population and style.
dev=atlas('development',[(10,20,421,410),(426,20,832,410),(840,20,1240,410),(10,426,420,810),(427,426,831,810),(840,426,1240,810),(10,833,420,1235),(427,833,832,1235),(840,833,1240,1235)])
for key,idx,size,name in [('id:prelude-daughters',0,(430,260),'embryonic-cells'),('id:school-young-muscle',1,(430,330),'muscle-rna'),('id:prelude-myoblasts',2,(430,330),'muscle-cells'),('id:school-young-support',3,(430,330),'tendon-rna'),('id:prelude-matrix',4,(430,330),'tendon-tissue'),('id:school-muscle-signals',5,(174,150),'shh'),('id:school-support-signals',6,(174,150),'tgf-beta2'),('id:school-bone-mineral',7,(210,115),'bone-mineral')]:item(key,fit(dev[idx],size),name)

# One shared arm is drawn by interactive layers, never by the blank background.
arm=read('arm-master');armbox=(48,62,785,965);full=arm.crop(armbox)
ar=np.array(full);rgb=ar[:,:,:3].astype(float);lum=rgb.max(axis=2)
ar[:,:,3]=(np.clip((lum-48)/30,0,1)*255).astype('uint8')
yy,xx=np.indices(ar.shape[:2]);gx=xx+48;gy=yy+62
def poly(points):
 m=Image.new('L',full.size);ImageDraw.Draw(m).polygon([(x-48,y-62) for x,y in points],fill=255);return np.array(m)>0
front=poly([(264,220),(290,220),(313,262),(341,307),(362,357),(369,410),(358,468),(335,516),(325,557),(306,557),(296,514),(271,468),(251,411),(246,355),(250,299)])
back=poly([(136,230),(156,246),(182,232),(200,264),(217,311),(221,379),(216,446),(198,504),(187,573),(165,573),(152,530),(122,479),(101,432),(91,370),(98,311),(112,270)])
pink=(rgb[:,:,0]>rgb[:,:,1]*1.32)&(rgb[:,:,0]>rgb[:,:,2]*.85)&(rgb[:,:,0]>70)
front|=pink&(gx>238)&(gx<374)&(gy>205)&(gy<559)
back|=pink&(gx>87)&(gx<224)&(gy>215)&(gy<580)
gold=(rgb[:,:,0]>rgb[:,:,2]*1.5)&(rgb[:,:,0]>rgb[:,:,1]*1.07)&(rgb[:,:,0]>80)
radius=gold&(gx>393)&(gx<483)&(gy>626)&(gy<693);ulna=gold&(gx>325)&(gx<418)&(gy>669)&(gy<730)
ar[((gx>281)&(gy<184))|((gx>650)&(gy<650)),3]=0
base=ar.copy();base[front|back,3]=0
for mask in [radius,ulna]:
 brightness=rgb[mask].max(axis=1);base[mask,0]=(brightness*.3).astype('uint8');base[mask,1]=(brightness*.7).astype('uint8');base[mask,2]=(brightness*.9).astype('uint8')
arm_size=(737,903)
# Partition the shared visible skeleton into registered front/back receivers.
left=base.copy();left[gx>=238,3]=0;right=base.copy();right[gx<238,3]=0
item('id:arm-front-tendons',Image.fromarray(right),'arm-front-base');item('id:arm-back-tendons',Image.fromarray(left),'arm-back-base')
for owner,muscle,mineral,label in [('id:arm-front-tendons',front,radius,'front'),('id:arm-back-tendons',back,ulna,'back')]:
 slots[owner]={}
 for key,mask,name in [('id:prelude-myoblasts',muscle,'muscle'),('id:school-bone-mineral',mineral,'mineral')]:
  la=ar.copy();la[~mask,3]=0;slots[owner][key]=save(Image.fromarray(la),'arm-'+label+'-'+name)
hotspots['4']={'id:arm-front-tendons':{'center':[780,1100],'hitbox':{'center':[687,1100],'size':[230,750]}},'id:arm-back-tendons':{'center':[780,1100],'hitbox':{'center':[520,1100],'size':[125,750]}}}
save(Image.fromarray(ar),'arm-complete')
registration['arm']={'canvas':arm_size,'center':[780,1100],'method':'Two visible registered skeleton partitions form ONE arm. Fittings preserve shared pixels and independent muscle/mineral masks. No background anatomy.'}
# A continuous neuron, with sleeves registered along the same unbroken axon.
neu=atlas('neuron',[(0,110,690,485),(701,170,1060,390),(1070,160,1536,395),(0,520,455,940),(467,520,1009,940),(1012,535,1536,905)])
nb=neu[0].resize((900,480),Image.Resampling.LANCZOS);item('id:school-neurons',nb,'neuron')
sleeve=fit(neu[1],(150,80));channel=fit(tight(read('neuron').crop((1225,185,1352,350))),(24,40))
# Portable counterparts keep the same component pixels and dimensions as fitted.
item('id:neural-wrapping-cells',layer(sleeve,(210,130),(30,25)),'schwann-cell')
item('id:school-ion-channels',composite((160,100),[(channel,(25,30)),(channel,(68,30)),(channel,(111,30))]),'ion-channels')
myelin=Image.new('RGBA',nb.size)
for x in [300,475,650]:myelin.alpha_composite(sleeve,(x,202))
chan=Image.new('RGBA',nb.size)
for x in [270,450,625]:chan.alpha_composite(channel,(x,222))
slots['id:school-neurons']={'id:neural-wrapping-cells':save(myelin,'neuron-myelin-fit'),'id:school-ion-channels':save(chan,'neuron-channels-fit')}
for key,idx,size,name in [('id:neural-spinal-precursors',3,(280,250),'spinal-precursors'),('id:neural-schwann-precursors',4,(320,230),'schwann-precursors'),('id:neural-wrapping-messengers',5,(290,190),'neuregulin')]:item(key,fit(neu[idx],size),name)
hotspots['5']={'id:neural-wrapping-messengers':{'center':[780,1150]}}
registration['neuron']={'canvas':nb.size,'axon_y':242,'sleeve_x':[300,475,650],'method':'Continuous generated neuron persists under independent myelin and channel layers.'}
# Frontal nervous construction; crop components from the one full master.
nm=clean(read('nervous-master'));na=np.array(nm);nY,nX=np.indices(na.shape[:2])
brain_mask=nY<190;cord_mask=(nY>=175)&(nY<645)&(nX>494)&(nX<535)
def nlayer(mask):
 a=na.copy();a[~mask,3]=0;return Image.fromarray(a)
brain=tight(nlayer(brain_mask));cord=tight(nlayer(cord_mask));peripheral=nlayer(~(brain_mask|((nY>=175)&(nY<755)&(nX>494)&(nX<535))))
# Locate every neural pixel on the same800×1600 anatomical extent.
def onbody(im):return im.crop((148,0,876,1536)).resize((800,1600),Image.Resampling.LANCZOS)
brain_layer=layer(fit(brain,(132,102)),(800,1600),(334,18));cord_layer=onbody(nlayer(cord_mask));periph_layer=onbody(peripheral)
npieces=atlas('nervous-parts',[(30,25,600,900),(775,10,1060,930),(10,958,620,1254),(640,950,1254,1254)])
skull=fit(npieces[0],(250,310));vertebrae=fit(npieces[1],(140,650))
skull_layer=layer(skull,(800,1600),((800-skull.width)//2,0));spine_layer=layer(vertebrae,(800,1600),((800-vertebrae.width)//2,180))
# Portable source parts and results use one common0.625 scale; transparent margin
# is cropped for loose parts without changing physical component scale.
FA=.625
small=lambda im:im.resize((round(im.width*FA),round(im.height*FA)),Image.Resampling.LANCZOS)
item('id:brain-model',tight(small(brain_layer)),'brain');item('id:spinal-cord-model',tight(small(cord_layer)),'spinal-cord');item('id:school-skull',tight(small(skull_layer)),'skull');item('id:school-backbone',tight(small(spine_layer)),'backbone')
protected_brain=skull_layer.copy();protected_brain.alpha_composite(brain_layer)
protected_cord=spine_layer.copy();protected_cord.alpha_composite(cord_layer)
central=protected_brain.copy();central.alpha_composite(protected_cord)
item('id:school-protected-brain',tight(small(protected_brain)),'protected-brain');item('id:school-protected-cord',tight(small(protected_cord)),'protected-cord');item('id:central-nervous-system-model',tight(small(central)),'central-nervous-system')
complete_nervous=central.copy();complete_nervous.alpha_composite(periph_layer)
item('id:nervous-system-model',small(complete_nervous),'nervous-system');save(complete_nervous,'nervous-system-registration')
sensory=fit(npieces[2],(270,100));motor=fit(npieces[3],(270,100))
item('id:sensory-routes',sensory,'sensory-root');item('id:motor-routes',motor,'motor-root')
spinal_nerve=composite((300,170),[(sensory,(5,5)),(motor,(20,60))]);item('id:school-peripheral-nerves',spinal_nerve,'spinal-nerve')
# One connected completed globe yields every eye part and intermediate.
# Masks assign every source pixel to exactly one physical contribution.
em=clean(read('eye-complete-master'));arE=np.array(em);ey,ex=np.indices(arE.shape[:2])
def epolygon(points):
 m=Image.new('L',em.size);ImageDraw.Draw(m).polygon(points,fill=255);return np.array(m)>0
lensmask=epolygon([(461,280),(510,321),(548,419),(570,526),(548,660),(499,750),(459,763),(420,722),(391,640),(369,524),(391,398),(423,312)])
irismask=epolygon([(353,269),(395,243),(415,292),(377,422),(367,523),(383,658),(412,761),(377,794),(338,740),(302,628),(294,509),(310,375)])&~lensmask
corneamask=(ex<295)&(ey>200)&(ey<830)&~(lensmask|irismask)
# The retinal layer follows the posterior inner edge. The supporting globe,
# vitreous and connected optic-nerve route belong to the retinal-neuron receiver.
retinamask=epolygon([(415,164),(595,73),(805,67),(1002,164),(1144,318),(1200,455),(1189,649),(1105,800),(934,923),(715,971),(516,926),(403,828),(380,779),(463,840),(622,890),(798,892),(953,824),(1050,707),(1094,552),(1080,407),(1007,270),(877,167),(716,124),(545,145),(440,211)])
retinamask&=~(lensmask|irismask|corneamask)
other=~(lensmask|irismask|corneamask|retinamask)
E=(800,534); eyeLayers={}
for name,mask in [('cornea',corneamask),('iris',irismask),('lens',lensmask),('retina',retinamask),('nerves',other)]:
 a=arE.copy();a[~mask,3]=0;eyeLayers[name]=Image.fromarray(a).resize(E,Image.Resampling.LANCZOS)
for key,name in [('name:Clear dome (cornea)','cornea'),('name:Coloured muscle ring (iris)','iris'),('name:Clear lens','lens'),('name:Light-sensitive cells','retina'),('name:Retinal nerve cells','nerves')]:item(key,tight(eyeLayers[name]),'eye-part-'+name)
def ecomp(names):return composite(E,[(eyeLayers[k],(0,0)) for k in names])
for key,names,name in [('name:Focusing eye front',['cornea','lens'],'focusing-eye'),('name:Cornea and iris',['cornea','iris'],'cornea-iris'),('name:Light-controlling eye front',['cornea','iris','lens'],'eye-front'),('name:Retina with optic nerve',['retina','nerves'],'retina-nerve'),('name:Eye with optic nerve',['cornea','iris','lens','retina','nerves'],'eye-complete')]:item(key,tight(ecomp(names)),name)
# Final sensory parts are located at the skull's own assembly scale.
eye_small=fit(tight(ecomp(['cornea','iris','lens','retina','nerves'])),(42,30));save(layer(eye_small,(112,88),(35,29)),'final-eye-supply')
eye_fit=layer(eye_small,(500,1000),(207,87))
ears_path=R.parent/'skin-finale/assets/final-ears.png'
if not ears_path.exists():raise RuntimeError('Awaiting final ears source')
ears=Image.open(ears_path).convert('RGBA');w,h=ears.size
left_ear=fit(tight(ears.crop((0,0,w//2,h))),(28,45));right_ear=fit(tight(ears.crop((w//2,0,w,h))),(28,45))
ears_fit=composite((500,1000),[(left_ear,(170,85)),(right_ear,(302,85))])
slots['id:nervous-system-model']={'name:Eye with optic nerve':save(eye_fit,'nervous-eyes-fit'),'id:final-ears':save(ears_fit,'nervous-ears-fit')}
finaln=small(complete_nervous);finaln.alpha_composite(eye_fit);finaln.alpha_composite(ears_fit);save(finaln,'nervous-system-complete')
# Later muscle supplies show a population at the arm's fibre scale.
population=Image.new('RGBA',(150,350));smallcells=fit(dev[2],(95,79))
for y in [12,94,176,258]:population.alpha_composite(smallcells,(27,y))
save(population,'muscle-cells-arm')
registration['nervous-system']={'source':'nervous-master.png','registrationCanvas':[800,1600],'exportCanvas':[500,1000],'scale':FA}
registration['eye']={'canvas':E,'source':'eye-complete-master.png','method':'Disjoint physical masks partition one connected globe. All stages use unchanged registered source pixels.'}

(R/'map.json').write_text(json.dumps({'itemIcons':icons,'slotIcons':slots,'hotspots':hotspots},indent=2)+'\n')
(R/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
