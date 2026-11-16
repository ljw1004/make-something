"""Executed by produce.py: same source constituents, registered at regional scale."""
from PIL import ImageOps
OPEN=ROOT.parent/'opening'/'assets';CIRC=ROOT.parent/'circulation'/'assets';ARM=ROOT.parent/'arm-food'/'assets'
def shared(p):return clean(Image.open(p).convert('RGBA'))
# All chest states and later arm fittings use the same canvas and registration.
chestbase=put(canvas(1200,1400),shared(CIRC/'breathing-apparatus.png'),250,20,700)
chestdiaphragm=put(canvas(1200,1400),shared(CIRC/'chest-diaphragm-layer.png'),250,20,700)
chestorgans=put(canvas(1200,1400),shared(CIRC/'chest-organs-fitted-layer.png'),250,20,700)
item('name:Breathing apparatus',chestbase,'breathing-apparatus-registered')
slot('name:Breathing apparatus','name:Diaphragm','chest-diaphragm-registered',chestdiaphragm)
slot('name:Breathing apparatus','name:Heart and lungs','chest-organs-registered',chestorgans)
arm=shared(ARM/'arm-complete-isolated.png')
# One arm was constructed; the opposite is explicitly supplied in the final model.
armright=put(canvas(1200,1400),arm,850,75,300,1010)
armleft=put(canvas(1200,1400),ImageOps.mirror(arm),50,75,300,1010)
regionalbase=combo(chestbase,armleft)
save('chest-regional-base',regionalbase)
presentations['name:Breathing apparatus']=[{'chapter':'full-assembly-regions','path':PREFIX+'chest-regional-base.png'}]
slot('name:Breathing apparatus','name:Arm assembly','chest-arm-fitted',armright)
# Take the actual lymph tree, without carrying a tissue close-up into the body.
micro=clean(Image.open(ROOT.parent/'circulation'/'sources'/'micro.png'))
w,h=micro.size
lym=crop(micro,(round(w*.755),round(h*.668),w,h))
lymnet=put(canvas(1200,1400),lym,550,165,220,565)
# Keep the actually built lymph-to-vein junction attached at the same scale.
put(lymnet,shared(CIRC/'lymph-return-route.png'),675,35,135,205)
slot('name:Breathing apparatus','name:Lymph drainage network','chest-lymph-fitted',lymnet)
presentations['name:Lymph drainage network']=[{'chapter':'full-assembly-regions','path':PREFIX+'lymph-finale-loose.png'}]
save('lymph-finale-loose',crop(lymnet))
presentations['name:Arm assembly']=[{'chapter':'full-assembly-regions','path':PREFIX+'arm-finale-loose.png'}]
item('name:Arm assembly',size(arm,300,1010),'arm-finale-loose')
chestcomplete=save('chest-regional-complete',combo(regionalbase,chestdiaphragm,chestorgans,armright,lymnet))
# Sensory parts fit directly into the existing skull; no second head or brain.
neural=shared(OPEN/'nervous-system.png');eye=shared(OPEN/'eye.png');ear=shared(OPEN/'ear.png');balance=shared(CIRC/'balance-organs.png')
fullEar=put(canvas(1040,620),ear,0,100,1000,507)
put(fullEar,balance,775,5,250,260)
fullEar=crop(fullEar)
pair=put(canvas(440,230),fullEar,0,0,210)
put(pair,ImageOps.mirror(fullEar),230,0,210)
item('id:final-ears',crop(pair),'final-ears')
eyeFit=put(canvas(*neural.size),eye,45,195,85,68)
earFit=put(canvas(*neural.size),ImageOps.mirror(fullEar),270,245,115,76)
slot('id:nervous-system-model','name:Eye with optic nerve','head-eye-fitted',eyeFit)
slot('id:nervous-system-model','id:final-ears','head-ear-fitted',earFit)
# The near ear is visible; the far side is physically occluded by this skull view.
neuralComplete=save('head-spine-complete',combo(neural,eyeFit,earFit))
presentations['name:Eye with optic nerve']=[{'chapter':'full-assembly-regions','path':PREFIX+'eye-finale-loose.png'}]
save('eye-finale-loose',size(eye,160))
# Assemble whole-body regions without redrawing or duplicating their organs.
whole=canvas(1100,2200)
# Restore the same upper food pipe through the trunk, behind the chest organs.
esophagus=crop(source('gut-organs'),(410,0,470,310))
esophagus=size(esophagus,32,700).rotate(6,expand=True,resample=Image.Resampling.BICUBIC)
put(whole,esophagus,495,250)
put(whole,lowcomplete,270,790,560,1320)
put(whole,chestcomplete,120,330,860,1003)
item('name:Trunk and limbs',whole)
head=neuralComplete.crop((0,0,neural.width,470))
cord=neuralComplete.crop((0,455,neural.width,neural.height))
# The neural spine goes behind the chest: its thoracic bone is naturally occluded,
# with the chest's retained posterior rib attachment occupying that same position.
ns=canvas(1100,2200);put(ns,cord,425,300,250,850);put(ns,head,420,35,260,298)
beneath=combo(ns,whole)
item('name:Body beneath the skin',beneath)
# This covering was generated against the actual assembled anatomy, preserving pose.
skincover=size(source('skin-cover-registered'),1100,2200)
item('name:Skin covering',skincover)
patchlayer=put(canvas(1100,2200),repaired,245,805,21,17)
slot('name:Skin covering','name:Repaired skin segment','skin-patch-fitted',patchlayer)
finishedskin=save('skin-cover-complete',combo(skincover,patchlayer))
cover=finishedskin.copy()
# One broad dissection in the trunk, plus small continuous cranial and arm windows.
cover=mask(cover,[(410,465),(495,400),(665,405),(745,490),(722,900),(690,1200),(590,1270),(425,1190),(390,900)],False)
cover=mask(cover,[(555,65),(645,75),(680,145),(665,230),(595,260),(555,180)],False)
cover=mask(cover,[(785,465),(823,480),(840,690),(884,925),(862,975),(813,770),(780,610)],False)
# Skin naturally occludes any source dissection contour outside its physical shell.
body=beneath.copy()
silhouette=Image.fromarray((ndimage.binary_fill_holes(np.asarray(skincover.getchannel('A'))>180)*255).astype('uint8'))
body.putalpha(ImageChops.multiply(body.getchannel('A'),silhouette))
body=combo(body,cover)
item('name:Body',body)
save('body-cutaway-cover-layer',cover)

# Finale worktable magnification: keep regional receivers together on a phone.
# Base/overlay geometry remains proportional; CSS scales the common icon stack.
presentations['id:nervous-system-model']=[{'chapter':'full-assembly-regions','path':PREFIX+'nervous-finale-small.png'}]
save('nervous-finale-small',size(neural,round(neural.width*.5)))
save('chest-regional-base',size(regionalbase,600,700))
for filename in ['skin-covering','skin-patch-fitted','skin-cover-complete','lower-body','lower-gut-fitted','lower-urinary-fitted','lower-complete','trunk-and-limbs','body-beneath-the-skin','body','body-cutaway-cover-layer']:
 im=Image.open(OUT/(filename+'.png')).convert('RGBA');save(filename,size(im,round(im.width*.5),round(im.height*.5)))
# The whole-body intermediate retains the same magnification as the final shell.
save('arm-finale-loose',size(arm,180,606))
save('lymph-finale-loose',size(crop(lymnet),150))
save('gut-finale-loose',size(gut,230,342))
item('id:final-ears',size(crop(pair),280),'final-ears')
placements.update({'name:Skin covering':[1150,900],'name:Lower body':[400,1150],'id:final-ears':[350,400],'name:Arm assembly':[1410,1730]})
