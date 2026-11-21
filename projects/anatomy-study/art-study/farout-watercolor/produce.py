"""Mechanical atlas extraction and registered source-mask compositing; no drawn anatomy.
Run: uv run --with pillow python projects/anatomy-study/art-study/farout-watercolor/produce.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFilter, ImageOps
import json
ROOT=Path(__file__).resolve().parent
A=ROOT/'assets'; S=ROOT/'sources'
A.mkdir(exist_ok=True)
def save(im,name): im.save(A/(name+'.png')); return 'assets/'+name+'.png'
def fit(im,size):
    im=im.copy();im.thumbnail(size,Image.Resampling.LANCZOS);return im
def canvas(im,size):
    out=Image.new('RGBA',size);out.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2));return out
itemIcons={}; crops={}
names1=['id:prelude-phospholipids','id:prelude-water','id:opening-dna','id:opening-nuclear-envelope','id:opening-nucleus','id:opening-cell','id:prelude-myoblasts','id:school-bone-mineral','name:Outer ears and canals','name:Eardrums','name:Outer ears with eardrums','name:Middle-ear bones','name:Sound-conducting ears','name:Coiled inner-ear chambers and fluid','name:Hearing cells with tiny hairs','name:Vibration-sensitive inner ears']
names2=['name:Sound-receiving ears','name:Hearing pathways','name:Inner ears with hearing pathways','name:Ears','name:Starchy food','name:Saliva','name:Shorter starch chains','name:Digestive enzymes','name:Meal glucose','name:Protein food','name:Meal amino acids','name:Fat food','name:Bile','name:Small fat droplets','name:Fat digestion products','identity']
for source,names in [('atlas-cell-ear.png',names1),('atlas-ear-digestion.png',names2)]:
    master=Image.open(S/source).convert('RGBA')
    for n,key in enumerate(names):
        col=n%4; row=n//4
        bounds=(round(col*master.width/4)+5,round(row*master.height/4)+5,round((col+1)*master.width/4)-5,round((row+1)*master.height/4)-5)
        im=master.crop(bounds)
        # Remove near-transparent atlas dust without changing painted pigments.
        alpha=im.getchannel('A').point(lambda a:0 if a<20 else a)
        im.putalpha(alpha)
        if alpha.getbbox(): im=im.crop(alpha.getbbox())
        target=420 if key in ['id:opening-cell','name:Ears','name:Sound-receiving ears','name:Inner ears with hearing pathways','name:Vibration-sensitive inner ears'] else 320
        im=fit(im,(target,target))
        if key=='id:opening-cell': im=canvas(im,(440,360))
        if key=='identity': im=canvas(fit(im,(440,440)),(512,512))
        name=key.replace('id:','').replace('name:','').lower().replace(' ','-')
        itemIcons[key]=save(im,name)
        crops[key]={'source':source,'sourceCrop':bounds,'exportSize':im.size}
# Derive cell supplies from the completed bag, without changing molecular scale.
cell=Image.open(A/'opening-cell.png').convert('RGBA')
watermask=Image.new('L',cell.size); ImageDraw.Draw(watermask).ellipse((113,118,327,243),fill=255)
watermask=watermask.filter(ImageFilter.GaussianBlur(2))
water=cell.copy();water.putalpha(ImageChops.multiply(cell.getchannel('A'),watermask))
lipids=cell.copy();lipids.putalpha(ImageChops.subtract(cell.getchannel('A'),watermask))
save(water.crop(water.getbbox()),'prelude-water')
save(lipids.crop(lipids.getbbox()),'prelude-phospholipids')
# A shared envelope and DNA drawing persist into the nucleus and its fitting.
envelope=fit(Image.open(A/'opening-nuclear-envelope.png').convert('RGBA'),(150,140))
dna=fit(Image.open(A/'opening-dna.png').convert('RGBA'),(48,86))
nucleus=Image.new('RGBA',(160,150));nucleus.alpha_composite(envelope,(5,5));nucleus.alpha_composite(dna,(56,38))
save(envelope,'opening-nuclear-envelope');save(dna,'opening-dna');save(nucleus,'opening-nucleus')
overlay=Image.new('RGBA',cell.size);overlay.alpha_composite(nucleus,(140,107))
save(overlay,'cell-nucleus-fit')
save(Image.new('RGBA',cell.size),'cell-unillustrated-fit')
# Ear stages are exact compositing of one set of painted parts, at fixed scale.
# Crop current geometry only; do not normalize each stage to a square.
earSize=(700,440)
def ear_layer(im,pos):
    out=Image.new('RGBA',earSize);out.alpha_composite(im,pos);return out
outer=ear_layer(fit(Image.open(A/'outer-ears-and-canals.png').convert('RGBA'),(285,285)),(0,65))
drum=ear_layer(Image.open(A/'eardrums.png').convert('RGBA').resize((48,82),Image.Resampling.LANCZOS),(250,179))
bones=ear_layer(Image.open(A/'middle-ear-bones.png').convert('RGBA').resize((132,85),Image.Resampling.LANCZOS),(280,155))
# This selected source already contains a real cochlear locator and hair-cell inset.
sensitive=fit(Image.open(A/'vibration-sensitive-inner-ears.png').convert('RGBA'),(300,300))
sens=ear_layer(sensitive,(395,95))
coilmask=Image.new('L',earSize)
ImageDraw.Draw(coilmask).polygon([(395+x,95+y) for x,y in [(0,0),(190,0),(190,109),(160,137),(121,156),(0,174)]],fill=255)
hairmask=ImageChops.invert(coilmask)
hair=sens.copy();hair.putalpha(ImageChops.multiply(sens.getchannel('A'),hairmask))
coil=sens.copy();coil.putalpha(ImageChops.subtract(sens.getchannel('A'),hairmask))
pathways=ear_layer(fit(Image.open(A/'hearing-pathways.png').convert('RGBA'),(175,180)),(512,0))
def ear_export(name,layers):
    out=Image.new('RGBA',earSize)
    for layer in layers:out.alpha_composite(layer)
    box=out.getchannel('A').point(lambda a:255 if a>20 else 0).getbbox()
    save(out.crop(box),name)
for name,layers in {
 'outer-ears-and-canals':[outer],'eardrums':[drum],'outer-ears-with-eardrums':[outer,drum],
 'middle-ear-bones':[bones],'sound-conducting-ears':[outer,drum,bones],
 'coiled-inner-ear-chambers-and-fluid':[coil],'hearing-cells-with-tiny-hairs':[hair],
 'vibration-sensitive-inner-ears':[coil,hair], 'sound-receiving-ears':[outer,drum,bones,coil,hair],
 'hearing-pathways':[pathways],'inner-ears-with-hearing-pathways':[pathways,coil,hair],
 'ears':[pathways,outer,drum,bones,coil,hair]}.items():ear_export(name,layers)
# Extend only a verified blank paper patch, never headings or anatomy.
master=Image.open(S/'background-master.png').convert('RGBA')
bgs={}
for n,ch in enumerate([1,4,8,18]):
    x=(n%2)*627;y=(n//2)*627
    panel=master.crop((x,y,x+627,y+627))
    # Exclude the source panel's lower border so it cannot repeat across the page.
    patch=panel.crop((0,400,627,615)).resize((1560,535),Image.Resampling.LANCZOS)
    ground=Image.new('RGBA',(1560,3376))
    for ty in range(0,3376,535):ground.paste(patch if (ty//535)%2==0 else ImageOps.flip(patch),(0,ty))
    bgs[str(ch)]=ground
# One continuous arm; full-resolution source masks give exact common registration.
arm=Image.open(S/'arm-master.png').convert('RGBA')
def poly(points):
    m=Image.new('L',arm.size);ImageDraw.Draw(m).polygon(points,fill=255);return m
muscles={
 'back-muscle':[(294,290),(310,322),(316,409),(316,570),(308,642),(291,701),(279,735),(258,698),(242,635),(218,561),(206,494),(210,445),(229,392),(258,345)],
 'front-muscle':[(390,246),(411,266),(429,304),(459,356),(480,412),(493,469),(492,527),(474,587),(456,642),(449,680),(438,710),(422,677),(401,630),(378,586),(361,533),(352,474),(358,407),(372,330)]}
masks={k:poly(v).filter(ImageFilter.MaxFilter(17)) for k,v in muscles.items()}
# Select only gold mineral pigment inside each anatomical window.
for key,pts in [('back-mineral',[(347,900),(385,878),(483,1043),(447,1071)]),('front-mineral',[(451,898),(490,880),(565,1034),(523,1057)])]:
    region=poly(pts); mask=Image.new('L',arm.size)
    px=arm.load();mp=mask.load();rp=region.load()
    for yy in range(870,1080):
        for xx in range(335,575):
            r,g,b,a=px[xx,yy]
            if rp[xx,yy] and r>175 and g>110 and r>b+60 and g>b+20:mp[xx,yy]=255
    masks[key]=mask.filter(ImageFilter.MaxFilter(3))
union=Image.new('L',arm.size)
for m in masks.values():union=ImageChops.lighter(union,m)
base=arm.copy();base.putalpha(ImageChops.subtract(arm.getchannel('A'),union))
armSize=(820,1230);armCenter=(800,1330);armOrigin=(390,715)
# Both receiving identities carry the same one-arm base, registered in place.
# Its fitting holes prevent either owner's base from covering another's additions.
for key in ['front','back']:
    save(base.resize(armSize,Image.Resampling.LANCZOS),'arm-'+key+'-base')
muscleDetail=fit(Image.open(A/'prelude-myoblasts.png').convert('RGBA'),(170,120))
mineralDetail=fit(Image.open(A/'school-bone-mineral.png').convert('RGBA'),(150,150))
save(muscleDetail,'prelude-myoblasts');save(mineralDetail,'school-bone-mineral')
callouts={
 'front-muscle':{'pos':(520,240),'anchor':(345,390),'detail':muscleDetail},
 'back-muscle':{'pos':(5,270),'anchor':(210,400),'detail':muscleDetail},
 'front-mineral':{'pos':(560,700),'anchor':(420,780),'detail':mineralDetail},
 'back-mineral':{'pos':(30,700),'anchor':(330,785),'detail':mineralDetail},
}
for key,m in masks.items():
    layer=arm.copy();layer.putalpha(ImageChops.multiply(arm.getchannel('A'),m));layer=layer.resize(armSize,Image.Resampling.LANCZOS)
    c=callouts[key];x,y=c['pos'];detail=c['detail']
    # Annotation only: anatomy remains pixels from the selected generated masters.
    ImageDraw.Draw(layer).line((c['anchor'],(x+detail.width//2,y+detail.height//2)),fill=(94,64,109,255),width=2)
    layer.alpha_composite(detail,(x,y));save(layer,key+'-fit')
# Remove even resampling fringes beneath every fitting from both receiver bases.
# Thus a later owner's base cannot overpaint an earlier owner's fitted pixels.
exportMask=Image.new('L',armSize)
for key in masks:
    exportMask=ImageChops.lighter(exportMask,Image.open(A/(key+'-fit.png')).getchannel('A'))
exportMask=exportMask.point(lambda a:255 if a else 0)
for key in ['front','back']:
    receiver=Image.open(A/('arm-'+key+'-base.png')).convert('RGBA')
    receiver.putalpha(ImageChops.multiply(receiver.getchannel('A'),ImageChops.invert(exportMask)))
    save(receiver,'arm-'+key+'-base')
for ch,bg in bgs.items():save(bg.convert('RGB'),'chapter-'+ch)
save(Image.new('RGBA',(240,160),(245,242,233,255)),'unillustrated')
save(Image.new('RGBA',(240,160)),'unillustrated-fit')
itemIcons['id:arm-front-tendons']='assets/arm-front-base.png';itemIcons['id:arm-back-tendons']='assets/arm-back-base.png'
mapping={'headingIcon':itemIcons.pop('identity'),'defaultIcon':'assets/unillustrated.png','defaultOverlay':'assets/unillustrated-fit.png','defaultBackground':'../../placeholder.svg','chapterBackgrounds':{k:'assets/chapter-'+k+'.png' for k in bgs},'itemIcons':itemIcons,
 'slotIcons':{'id:opening-cell':{'id:opening-nucleus':'assets/cell-nucleus-fit.png',**{x:'assets/cell-unillustrated-fit.png' for x in ['id:opening-mitochondria','id:school-sugar-carrier','id:school-ribosome']}},'id:arm-front-tendons':{'id:school-bone-mineral':'assets/front-mineral-fit.png','id:prelude-myoblasts':'assets/front-muscle-fit.png'},'id:arm-back-tendons':{'id:school-bone-mineral':'assets/back-mineral-fit.png','id:prelude-myoblasts':'assets/back-muscle-fit.png'}},
 'hotspots':{'4':{'id:arm-front-tendons':{'center':armCenter,'icon':'assets/arm-front-base.png','hitbox':{'center':[775,1260],'size':[210,730]}},'id:arm-back-tendons':{'center':armCenter,'icon':'assets/arm-back-base.png','hitbox':{'center':[590,1260],'size':[150,730]}}}}}
(ROOT/'art-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
(S/'registration.json').write_text(json.dumps({'atlasCrops':crops,
 'cell':{'waterMask':[113,118,327,243],'maskFeather':2,'canvas':cell.size,'nucleusPosition':[140,107],'nucleusCanvas':nucleus.size,'nuclearEnvelopeSize':envelope.size,'dnaSize':dna.size,'note':'same DNA and envelope pixels compose nucleus; same nucleus pixels fitted into bag; water and lipids derived by complementary masks from bag'},
 'ear':{'workingCanvas':earSize,'outerOrigin':[0,65],'drumOrigin':[250,179],'drumSize':[48,82],'bonesOrigin':[280,155],'bonesSize':[132,85],'sensitiveOrigin':[395,95],'sensitiveSize':sensitive.size,'pathwaysOrigin':[512,0],'note':'fixed source magnification; outputs cropped to current alpha bounds with no resize; all intermediates mechanically combine the same layers'},
 'arm':{'sourceSize':arm.size,'exportSize':armSize,'center':armCenter,'origin':armOrigin,'musclePolygons':muscles,'muscleMaskDilation':8,'mineralMask':'gold pigment threshold inside documented polygon, dilated 1px','commonCanvas':'both visible anatomical arm hotspot bases and fittings 820x1230','callouts':{key:{'position':v['pos'],'anchor':v['anchor'],'size':v['detail'].size} for key,v in callouts.items()},'note':'coincident base copies have zero alpha at every nonzero pixel of any final exported fitting, including resampling fringes; all four independent additions have located supply-scale detail'},
 'background':{'size':[1560,3376],'quadrantSize':[627,627],'blankGroundPatch':[0,400,627,615],'extension':'uniform scaling then mirrored repetitions of blank paper only; no anatomy, headings, labels or examples'}},indent=2)+'\n')
