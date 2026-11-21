"""Mechanical extraction only. Run: uv run --with pillow --with numpy --with scipy python produce.py"""
from pathlib import Path
import json
import numpy as np
from scipy import ndimage as ndi
from PIL import Image, ImageDraw

ROOT=Path(__file__).parent
AS=ROOT/'assets'
AS.mkdir(exist_ok=True)
def clean(im):
    a=np.array(im.convert('RGBA'))
    lab,n=ndi.label(a[:,:,3]>90)
    counts=np.bincount(lab.ravel())
    keep=counts>30;keep[0]=False
    mask=ndi.binary_dilation(keep[lab],iterations=1)
    a[:,:,3]=np.where(mask,a[:,:,3],0)
    return Image.fromarray(a)
def fit(im,size=400):
    bb=im.getbbox()
    if bb:im=im.crop(bb)
    im.thumbnail((size-24,size-24),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(size,size))
    out.alpha_composite(im,((size-im.width)//2,(size-im.height)//2))
    return out
def export(name,im,size=400):
    out=fit(clean(im),size);out.save(AS/(name+'.png'));return out
def cut(sheet,box,name,size=400):
    return export(name,Image.open(ROOT/'sources'/sheet).convert('RGBA').crop(box),size)

bg=Image.open(ROOT/'sources/blank-paper.png')
for chapter in [1,4,8,18]:
    bg.resize((780,1170),Image.Resampling.LANCZOS).save(AS/f'chapter-{chapter}.png')

cells=[('lipids',(0,0,423,420)),('water',(436,0,811,424)),('dna',(856,0,1254,418)),('envelope',(0,426,418,817)),('nucleus',(418,426,834,817)),('cell',(834,420,1254,826)),('muscle-cells',(0,830,418,1254)),('mineral',(420,823,815,1254)),('heading',(815,827,1254,1254))]
for name,box in cells:cut('cell-parts.png',box,name,520 if name=='cell' else 400)
cell=Image.open(AS/'cell.png')
# Constituents are actual pieces of the finished drawing, at its magnification.
# The aqueous section follows the inside of the bilayer, never a droplet symbol.
mask=Image.new('L',cell.size)
ImageDraw.Draw(mask).polygon([(113,233),(132,188),(170,153),(218,131),(260,129),(300,143),(331,174),(350,214),(351,258),(333,293),(295,318),(246,327),(202,315),(159,293),(126,268)],fill=255)
water=cell.copy();ca=np.array(cell);rr,gg,bb=[ca[:,:,n].astype(float) for n in range(3)]
aqueous=(np.array(mask)>0)&(gg>rr*1.12)&(bb>rr*1.12)
aqueous=ndi.binary_fill_holes(ndi.binary_opening(aqueous,iterations=2))
mask=Image.fromarray(aqueous.astype('uint8')*255);water.putalpha(mask)
water.crop(water.getbbox()).save(AS/'water.png')
# A curved membrane section, directly sampled from the actual bag wall.
lipids=cell.crop((81,86,238,188));arr=np.array(lipids)
yy,xx=np.indices(arr.shape[:2]);rr,gg,bb=[arr[:,:,n].astype(float) for n in range(3)]
membrane=((rr>gg*1.1)&(rr>bb*1.15))|((bb>gg*1.2)&(rr>gg*1.1))
membrane=ndi.binary_closing(membrane,iterations=1)
arr[:,:,3]=np.where(membrane,arr[:,:,3],0)
lipids=clean(Image.fromarray(arr));lipids.crop(lipids.getbbox()).save(AS/'lipids.png')
# Build the nucleus from the same envelope and DNA shown separately.
envelope=Image.open(AS/'envelope.png');envelope.thumbnail((184,184),Image.Resampling.LANCZOS)
dna=Image.open(AS/'dna.png');dna.thumbnail((96,122),Image.Resampling.LANCZOS)
nucleus=Image.new('RGBA',(184,184));nucleus.alpha_composite(dna,((184-dna.width)//2,(184-dna.height)//2));nucleus.alpha_composite(envelope,((184-envelope.width)//2,(184-envelope.height)//2))
envelope.crop(envelope.getbbox()).save(AS/'envelope.png');dna.crop(dna.getbbox()).save(AS/'dna.png');nucleus.save(AS/'nucleus.png')
layer=Image.new('RGBA',cell.size)
layer.alpha_composite(nucleus,(158,150));layer.save(AS/'cell-nucleus.png')

ears=[('outer-ear',(0,0,362,372)),('eardrum',(368,0,700,370)),('ear-drum',(713,0,1086,370)),('ossicles',(0,376,337,698)),('ear-conducting',(338,376,715,699)),('cochlea',(719,370,1086,706)),('hair-cells',(0,720,347,1067)),('inner-sensitive',(348,702,699,1080)),('ear-receiving',(700,720,1086,1075)),('hearing-nerve',(0,1080,332,1448)),('inner-pathways',(332,1080,664,1448)),('ears',(664,1080,1086,1448))]
for name,box in ears:cut('hearing-parts.png',box,name,440 if name in ['ears','ear-receiving','inner-pathways'] else 400)

# One component dictionary supplies ALL twelve hearing states. Tight cropping
# changes the surrounding canvas only; no completed state is rescaled.
sheet=Image.open(ROOT/'sources/hearing-parts.png').convert('RGBA')
def component(box,bounds):
    im=clean(sheet.crop(box));im=im.crop(im.getbbox());im.thumbnail(bounds,Image.Resampling.LANCZOS);return im
parts={
 'outer':(component((0,0,362,372),(290,280)),(10,30)),
 'drum':(component((368,0,700,370),(53,89)),(269,142)),
 'bones':(component((0,376,337,698),(123,110)),(309,132)),
 'coil':(component((719,370,1086,706),(220,220)),(425,100)),
 'hair':(component((0,720,347,1067),(176,176)),(446,345)),
 'nerve':(component((0,1080,332,1448),(175,128)),(621,138)),
}
# Retain the generated cream locator wedge rather than drawing a new symbol.
locator=sheet.crop((394,856,578,932));aa=np.array(locator);rr,gg,bb=[aa[:,:,n].astype(float) for n in range(3)]
aa[:,:,3]=np.where((rr>150)&(gg>130)&(bb>100)&(rr>bb*1.06)&(rr<gg*1.4),aa[:,:,3],0)
locator=clean(Image.fromarray(aa));locator=locator.crop(locator.getbbox()).resize((156,110),Image.Resampling.LANCZOS)
parts['locator']=(locator,(470,273))
states={
 'outer-ear':['outer'],'eardrum':['drum'],'ear-drum':['outer','drum'],
 'ossicles':['bones'],'ear-conducting':['outer','drum','bones'],
 'cochlea':['coil'],'hair-cells':['hair'],
 'inner-sensitive':['coil','locator','hair'],
 'ear-receiving':['outer','drum','bones','coil','locator','hair'],
 'hearing-nerve':['nerve'],'inner-pathways':['coil','locator','hair','nerve'],
 'ears':['outer','drum','bones','coil','locator','hair','nerve'],
}
registration={}
for name,selected in states.items():
    canvas=Image.new('RGBA',(820,540))
    for key in selected:
        im,pos=parts[key];canvas.alpha_composite(im,pos)
    box=canvas.getbbox();canvas.crop(box).save(AS/(name+'.png'))
    registration[name]={'components':selected,'crop':list(box)}
(ROOT/'hearing-registration.json').write_text(json.dumps(registration,indent=2)+'\n')

# Neutral declarations for deliberately unillustrated chapters.
Image.new('RGBA',(1,1)).save(AS/'neutral-overlay.png')
Image.new('RGBA',(520,520)).save(AS/'cell-neutral-overlay.png')

foods=['starch','saliva','short-starch','enzymes','glucose','protein','amino-acids','fat','bile','small-fat','fat-products','tract']
for n,name in enumerate(foods):
    row,col=divmod(n,3)
    xs=[0,360,720,1086];ys=[0,365,735,1060,1448]
    cut('digestion-parts.png',(xs[col],ys[row],xs[col+1],ys[row+1]),name)

# Arm: every layer comes from the very same generated master, with no redrawing.
arm=Image.open(ROOT/'sources/arm-master.png').convert('RGBA')
a=np.array(arm);a[:,:,3]=np.where(a[:,:,3]>175,a[:,:,3],0)
y,x=np.indices(a.shape[:2]);r,g,b=[a[:,:,n].astype(float) for n in range(3)]
front=(x>260)&(x<465)&(y>200)&(y<710)&(r>g*1.22)&(r>b*1.13)&(b>g*.85)&(a[:,:,3]>0)
back=(x>470)&(x<650)&(y>200)&(y<720)&(b>r*1.04)&(b>g*1.22)&(a[:,:,3]>0)
front=ndi.binary_fill_holes(ndi.binary_closing(front,iterations=3))
back=ndi.binary_fill_holes(ndi.binary_closing(back,iterations=3))
for mask in [front,back]:
    labs,n=ndi.label(mask)
    counts=np.bincount(labs.ravel());counts[0]=0
    mask[:]=labs==counts.argmax()
gold=(r>g*1.1)&(g>b*1.35)&(a[:,:,3]>0)
mineral_front=gold&(x>418)&(x<488)&(y>881)&(y<1010)
mineral_back=gold&(x>494)&(x<558)&(y>851)&(y<991)
base=a.copy();base[front|back,3]=0
for mask in [mineral_front,mineral_back]:
    gray=(base[:,:,:3].mean(axis=2)*.6+90).astype('uint8')
    for c in range(3):base[:,:,c]=np.where(mask,gray,base[:,:,c])
crop=(170,8,755,1536)
canvas=(480,1240)
def arm_canvas(arr):
    part=Image.fromarray(arr).crop(crop)
    part.thumbnail(canvas,Image.Resampling.LANCZOS)
    out=Image.new('RGBA',canvas);out.alpha_composite(part,((canvas[0]-part.width)//2,(canvas[1]-part.height)//2));return out
base_out=arm_canvas(base)
base_out.save(AS/'arm-skeleton.png')
for name,mask in [('biceps',front),('triceps',back),('radius-mineral',mineral_front),('ulna-mineral',mineral_back)]:
    aa=a.copy();aa[:,:,3]=np.where(mask,aa[:,:,3],0)
    arm_canvas(aa).save(AS/(name+'.png'))
# Complementary anatomical receiver layers form ONE arm. Each target owns
# visible bone and tendon tissue, with no anatomy baked into the page.
base_arr=np.array(base_out);yy,xx=np.indices(base_arr.shape[:2])
split=206+yy*.10
for name,mask in [('arm-front',xx<split),('arm-back',xx>=split)]:
    aa=base_arr.copy();aa[:,:,3]=np.where(mask,aa[:,:,3],0)
    Image.fromarray(aa).save(AS/(name+'.png'))

def asset(s):return 'assets/'+s+'.png'
icons={
 'id:prelude-phospholipids':asset('lipids'),'id:prelude-water':asset('water'),
 'id:opening-dna':asset('dna'),'id:opening-nuclear-envelope':asset('envelope'),
 'id:opening-nucleus':asset('nucleus'),'id:opening-cell':asset('cell'),
 'id:prelude-myoblasts':asset('muscle-cells'),'id:school-bone-mineral':asset('mineral'),
 'id:arm-front-tendons':asset('arm-front'),'id:arm-back-tendons':asset('arm-back')}
ear_names=['Outer ears and canals','Eardrums','Outer ears with eardrums','Middle-ear bones','Sound-conducting ears','Coiled inner-ear chambers and fluid','Hearing cells with tiny hairs','Vibration-sensitive inner ears','Sound-receiving ears','Hearing pathways','Inner ears with hearing pathways','Ears']
icons.update({'name:'+name:asset(spec[0]) for name,spec in zip(ear_names,ears)})
food_names=['Starchy food','Saliva','Shorter starch chains','Digestive enzymes','Meal glucose','Protein food','Meal amino acids','Fat food','Bile','Small fat droplets','Fat digestion products']
icons.update({'name:'+name:asset(spec) for name,spec in zip(food_names,foods)})
mapping={
 'headingIcon':asset('heading'),'defaultIcon':'../../placeholder.svg',
 'defaultOverlay':asset('neutral-overlay'),'defaultBackground':'../../placeholder.svg',
 'chapterBackgrounds':{str(c):asset('chapter-'+str(c)) for c in [1,4,8,18]},
 'itemIcons':icons,
 'slotIcons':{'id:opening-cell':{'id:opening-nucleus':asset('cell-nucleus'),'id:opening-mitochondria':asset('cell-neutral-overlay'),'id:school-sugar-carrier':asset('cell-neutral-overlay'),'id:school-ribosome':asset('cell-neutral-overlay')},
 'id:arm-front-tendons':{'id:prelude-myoblasts':asset('biceps'),'id:school-bone-mineral':asset('radius-mineral')},
 'id:arm-back-tendons':{'id:prelude-myoblasts':asset('triceps'),'id:school-bone-mineral':asset('ulna-mineral')}},
 'hotspots':{'4':{'id:arm-front-tendons':{'center':[390,630],'icon':asset('arm-front'),'hitbox':{'center':[354,560],'size':[82,470]}},'id:arm-back-tendons':{'center':[390,630],'icon':asset('arm-back'),'hitbox':{'center':[437,560],'size':[82,470]}}}}
}
(ROOT/'art-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
