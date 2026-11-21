"""Mechanical extraction/registration of selected built-in imagegen artwork.
Run from repository root: uv run --with pillow python projects/anatomy-study/art-study/farout-macabre/produce.py
No anatomy is drawn by this script. Bounds below were inspected against each atlas.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageEnhance,ImageChops,ImageOps
import json
D=Path(__file__).parent; A=D/'assets';S=D/'sources'; A.mkdir(exist_ok=True)
W,H=1560,3376

def extend(im):
    painted=im.resize((W,2340),Image.Resampling.LANCZOS)
    out=Image.new('RGB',(W,H));out.paste(painted,(0,0))
    # This lower source region contains only blank ground. Keep its original
    # uniform scale and mirror at each join so boundary pixels match exactly.
    ground=painted.crop((0,1524,W,2340))
    y=2340; reverse=True
    while y<H:
        out.paste(ImageOps.flip(ground) if reverse else ground,(0,y))
        y+=ground.height;reverse=not reverse
    return out
# Every live surface is blank. This inspected strip has no diagram or text.
ground=Image.open(S/'arm-complete.png').crop((0,900,1024,1536))
blank=Image.new('RGB',(W,H))
strip=ground.resize((W,969),Image.Resampling.LANCZOS)
for y in range(0,H,969):blank.paste(ImageOps.flip(strip) if (y//969)%2 else strip,(0,y))
for name in ['cell','arm','hearing','digestion']:
    blank.save(A/(name+'-background.jpg'),quality=94)
Image.new('RGB',(W,H),'#f5f2e9').save(A/'unillustrated-background.png')
Image.new('RGBA',(400,400)).save(A/'unillustrated-overlay.png')

# Each atlas has independently inspected row boundaries; do not assume equal rows.
rows={'cell':[0,320,635,935,1254],'hearing':[0,315,625,945,1254],'digestion':[0,315,630,935,1254]}
cols={'cell':[0,420,845,1254],'hearing':[0,415,830,1254],'digestion':[0,414,836,1254]}
names={
'cell':['lipids','water','dna','nuclear-envelope','nucleus','cell','muscle-cells','mineral','spare-lipids','pore','tendon','spare-nucleus'],
'hearing':['outer-ear','eardrum','ear-drum','ossicles','conducting-ear','cochlea','hair-cells','sensing-ear','receiving-ear','hearing-pathway','inner-pathway','ears'],
'digestion':['starch','saliva','short-starch','enzymes','glucose','protein-food','amino-acids','fat','bile','fat-droplets','fat-products','spare-enzyme']}
manifest={}
for atlas in names:
    im=Image.open(S/(atlas+'-atlas.png')).convert('RGBA')
    for idx,name in enumerate(names[atlas]):
        if name.startswith('spare') or name in ['pore','tendon']:continue
        r,c=divmod(idx,3);box=(cols[atlas][c],rows[atlas][r],cols[atlas][c+1],rows[atlas][r+1])
        part=im.crop(box)
        # Ignore nearly invisible alpha dust when choosing tight bounds. Preserve real alpha edges.
        bbox=part.getchannel('A').point(lambda x:255 if x>40 else 0).getbbox();part=part.crop(bbox)
        maxside=460 if name in ['cell','ears','receiving-ear','inner-pathway'] else 340
        part.thumbnail((maxside,maxside),Image.Resampling.LANCZOS)
        # fixed 480 square cell extent registers the fitted nucleus; other exports crop to geometry.
        size=(480,480) if name=='cell' else (part.width+16,part.height+16)
        out=Image.new('RGBA',size);out.alpha_composite(part,((size[0]-part.width)//2,(size[1]-part.height)//2));out.save(A/(name+'.png'))
        manifest[name]={'atlas':atlas+'-atlas.png','cell_bounds':box,'alpha_bounds':bbox,'export_size':size}
# Nucleus fits entirely inside the empty cell fluid, on the same 480 square extent.
n=Image.open(A/'nucleus.png');n.thumbnail((220,220),Image.Resampling.LANCZOS)
ov=Image.new('RGBA',(480,480));ov.alpha_composite(n,((480-n.width)//2,(480-n.height)//2));ov.save(A/'cell-nucleus-overlay.png')
Image.new('RGBA',(480,480)).save(A/'cell-unused-overlay.png')
icon=Image.open(A/'nucleus.png');icon.thumbnail((224,224),Image.Resampling.LANCZOS)
heading=Image.new('RGBA',(256,256),'#25160b');heading.alpha_composite(icon,((256-icon.width)//2,(256-icon.height)//2));heading.convert('RGB').save(A/'identity.png')

# One complete arm master. All four fitting masks are registered in that exact master.
arm=Image.open(S/'arm-complete.png').convert('RGB');base=arm.copy()
polygons={
'biceps':[(342,264),(361,301),(384,356),(398,405),(397,462),(387,508),(374,550),(363,579),(349,540),(332,513),(322,475),(318,426),(320,378),(329,321)],
'triceps':[(284,266),(276,294),(252,326),(239,367),(231,409),(235,458),(245,502),(256,541),(267,570),(277,535),(286,483),(293,430),(294,374),(291,323)]}
masks={}
for name,points in polygons.items():
    mask=Image.new('L',arm.size);ImageDraw.Draw(mask).polygon(points,fill=255);mask=mask.filter(ImageFilter.GaussianBlur(1));masks[name]=mask
    # Erase only the detachable flesh. Nearby tendons, origins and insertions remain in base.
    blank=arm.crop((0,900,1024,1536)).resize(arm.size,Image.Resampling.LANCZOS)
    base.paste(blank,(0,0),mask)
for name,ellipse,poly in [
 ('radius-mineral',(595,173,762,338),[(501,548),(524,518),(565,496),(621,482),(628,492),(603,519),(552,550),(514,561)]),
 ('ulna-mineral',(712,518,874,683),[(522,594),(546,574),(582,558),(605,555),(607,566),(580,589),(545,610),(522,613)])]:
    mask=Image.new('L',arm.size);dr=ImageDraw.Draw(mask);dr.ellipse(ellipse,fill=255);dr.polygon(poly,fill=255);mask=mask.filter(ImageFilter.GaussianBlur(1));masks[name]=mask
    # Unmineralized collagen matrix retains texture but loses the luminous mineral coloration.
    matrix=ImageEnhance.Color(arm).enhance(.1);matrix=ImageEnhance.Brightness(matrix).enhance(.62);base.paste(matrix,(0,0),mask)
# The old master is now an interactive specimen, never background anatomy.
# Two complementary alpha masks preserve ONE arm while making both receivers
# visibly anatomical. Each includes its tendon/bone and its located detail.
outline=Image.new('L',arm.size);dr=ImageDraw.Draw(outline)
dr.polygon([(252,170),(354,146),(445,168),(501,149),(515,206),(494,269),(477,341),(416,354),(403,490),(423,558),(481,535),(578,478),(650,432),(707,373),(734,328),(807,297),(848,298),(898,337),(916,382),(880,400),(835,397),(788,418),(746,463),(686,507),(641,548),(632,580),(579,614),(515,650),(418,691),(328,710),(286,695),(258,662),(238,591),(221,485),(227,362),(242,284)],fill=255)
dr.polygon([(700,370),(734,315),(796,286),(864,290),(936,336),(936,417),(884,447),(799,450),(739,481)],fill=255)
for box in [(587,165,766,345),(703,509,880,691)]:dr.ellipse(box,fill=255)
for poly in [[(588,288),(545,510),(672,340)],[(560,580),(715,565),(738,655)]]:dr.polygon(poly,fill=255)
for box in [(111,405,234,459),(416,361,538,412),(445,453,550,502),(517,638,630,690)]:dr.rectangle(box,fill=255)
front=Image.new('L',arm.size);ImageDraw.Draw(front).polygon([(313,0),(1024,0),(1024,538),(690,538),(640,560),(500,587),(352,659),(314,605)],fill=255)
fd=ImageDraw.Draw(front)
fd.ellipse((703,509,880,691),fill=0)
fd.polygon([(560,580),(715,565),(738,655)],fill=0)
fd.rectangle((517,638,630,690),fill=0)
front=ImageChops.lighter(front,masks['radius-mineral'])
front=ImageChops.subtract(front,masks['ulna-mineral'])
front=ImageChops.multiply(outline,front);back=ImageChops.subtract(outline,front)
for name,mask in [('front',front),('back',back)]:
    part=base.convert('RGBA');part.putalpha(mask)
    out=Image.new('RGBA',(W,H));out.alpha_composite(part.resize((W,2340),Image.Resampling.LANCZOS));out.save(A/('arm-'+name+'-base.png'))
for name,mask in masks.items():
    layer=arm.convert('RGBA');layer.putalpha(mask);out=Image.new('RGBA',(W,H));out.alpha_composite(layer.resize((W,2340),Image.Resampling.LANCZOS));out.save(A/('arm-'+name+'.png'))
manifest['arm_registration']={'source_size':[1024,1536],'scale':1560/1024,'canvas':[W,H],'artwork_center':[780,1688],'muscle_masks':polygons,'bone_windows':'radius and ulna polygons plus their located circular enlargements; retain matrix in base','receivers':'Complementary front/back masks of the single painted arm; all anatomy removed from the background.'}

# Mechanical composition of existing generated parts. No independent per-state
# normalization: a component has exactly the same painted pixels at every step.
def tight(im,pad=8):
    box=im.getchannel('A').point(lambda v:255 if v>40 else 0).getbbox()
    cut=im.crop(box);out=Image.new('RGBA',(cut.width+pad*2,cut.height+pad*2));out.alpha_composite(cut,(pad,pad));return out
def masked(im,mask):
    out=im.copy();out.putalpha(ImageChops.multiply(im.getchannel('A'),mask));return out
def export(name,im,crop=True):
    out=tight(im) if crop else im;out.save(A/(name+'.png'));manifest[name]={'method':'registered composition from selected original raster','export_size':list(out.size)}

# Cell: the water and membrane really are the contents and wall of this bag.
bag=Image.open(A/'cell.png').convert('RGBA')
fluid=Image.new('L',bag.size);ImageDraw.Draw(fluid).ellipse((141,148,367,326),fill=255)
fluid=fluid.filter(ImageFilter.GaussianBlur(1))
export('water',masked(bag,fluid))
wall=ImageChops.invert(fluid)
segments=Image.new('L',bag.size);d=ImageDraw.Draw(segments)
d.polygon([(0,0),(225,0),(225,480),(0,480)],fill=255)
d.polygon([(258,0),(480,0),(480,480),(258,480)],fill=255)
export('lipids',masked(bag,ImageChops.multiply(wall,segments)))
# Match the nucleus fitting and portable nucleus exactly, including envelope
# and DNA; the DNA supply uses the helix at its fitted scale.
envelope=Image.open(A/'nuclear-envelope.png').convert('RGBA');envelope.thumbnail((170,170),Image.Resampling.LANCZOS)
dna=Image.open(A/'dna.png').convert('RGBA');dna.thumbnail((75,115),Image.Resampling.LANCZOS)
nc=Image.new('RGBA',(190,190));nc.alpha_composite(envelope,((190-envelope.width)//2,(190-envelope.height)//2));nc.alpha_composite(dna,((190-dna.width)//2,(190-dna.height)//2))
export('nucleus',nc);export('nuclear-envelope',envelope);export('dna',dna)
nucleus=tight(nc);ov=Image.new('RGBA',bag.size);ov.alpha_composite(nucleus,((480-nucleus.width)//2,(480-nucleus.height)//2));export('cell-nucleus-overlay',ov,False)
export('cell-with-nucleus',Image.alpha_composite(bag,ov),False)

# One additive hearing family. The inspected generated sensing-ear cell owns
# both the cochlea and its located enlargement. Split them once; thereafter
# preserve the exact components and locator through every containing state.
atlas=Image.open(S/'hearing-atlas.png').convert('RGBA')
sensing=atlas.crop((415,625,830,945))
detailmask=Image.new('L',sensing.size);d=ImageDraw.Draw(detailmask)
d.ellipse((0,0,203,200),fill=255)
d.polygon([(163,140),(284,225),(278,238),(190,181)],fill=255)
detail=masked(sensing,detailmask)
# Use the clean loose cochlea instead of leaving a triangular hole where the
# selected master draws its magnification beam. Its pixels persist thereafter.
cochlea=Image.open(A/'cochlea.png').convert('RGBA')
def scaled(im,factor):return im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS)
outer=Image.open(A/'outer-ear.png').convert('RGBA');outer=scaled(outer,.78)
drum=Image.open(A/'eardrum.png').convert('RGBA');drum.thumbnail((58,79),Image.Resampling.LANCZOS)
ossicles=Image.open(A/'ossicles.png').convert('RGBA');ossicles.thumbnail((93,70),Image.Resampling.LANCZOS)
pathway=Image.open(A/'hearing-pathway.png').convert('RGBA');pathway=scaled(pathway,.72)
cochlea=scaled(cochlea,.70);detail=scaled(detail,.70)
parts={'outer':(outer,(8,180)),'drum':(drum,(246,282)),'bones':(ossicles,(285,299)),'cochlea':(cochlea,(350,228)),'detail':(detail,(328,175)),'nerve':(pathway,(573,219))}
def hearing(name,keys):
    frame=Image.new('RGBA',(890,480))
    for key in keys:
        im,xy=parts[key];frame.alpha_composite(im,xy)
    export(name,frame)
for name,keys in {
 'outer-ear':['outer'],'eardrum':['drum'],'ear-drum':['outer','drum'],
 'ossicles':['bones'],'conducting-ear':['outer','drum','bones'],
 'cochlea':['cochlea'],'hair-cells':['detail'],
 'sensing-ear':['cochlea','detail'],
 'receiving-ear':['outer','drum','bones','cochlea','detail'],
 'hearing-pathway':['nerve'],'inner-pathway':['cochlea','detail','nerve'],
 'ears':['outer','drum','bones','cochlea','detail','nerve']}.items():hearing(name,keys)
manifest['hearing_registration']={'canvas':[890,480],'component_positions':{k:list(v[1]) for k,v in parts.items()},'rule':'Shared pixels and fixed magnification; alpha-trim changes extent only. Located hair-cell enlargement persists in sensing, receiving, inner-pathway and ears.'}
manifest['cell_registration']={'canvas':[480,480],'fluid_mask_ellipse':[141,148,367,326],'membrane':'Two sections of the same bag wall, using inverse fluid mask and a 33px separation','nucleus':'One 190px envelope/DNA composite; same pixels fitted and portable','source':'cell-atlas.png'}

# Export each independently reviewable arm partial with its registered extent.
for region,muscle,mineral in [('front','biceps','radius-mineral'),('back','triceps','ulna-mineral')]:
    base=Image.open(A/f'arm-{region}-base.png').convert('RGBA')
    ml=Image.open(A/f'arm-{muscle}.png');bl=Image.open(A/f'arm-{mineral}.png')
    for state,layers in [('muscle',[ml]),('mineral',[bl]),('complete',[ml,bl])]:
        out=base.copy()
        for layer in layers:out.alpha_composite(layer)
        export(f'arm-{region}-{state}',out,False)
(D/'extraction.json').write_text(json.dumps(manifest,indent=2)+'\n')

ids=lambda x:'id:'+x
item_icons={ids(k):'assets/'+v+'.png' for k,v in {'prelude-phospholipids':'lipids','prelude-water':'water','opening-dna':'dna','opening-nuclear-envelope':'nuclear-envelope','opening-nucleus':'nucleus','opening-cell':'cell','prelude-myoblasts':'muscle-cells','school-bone-mineral':'mineral','arm-front-tendons':'arm-front-base','arm-back-tendons':'arm-back-base'}.items()}
for k,v in {'Outer ears and canals':'outer-ear','Eardrums':'eardrum','Outer ears with eardrums':'ear-drum','Middle-ear bones':'ossicles','Sound-conducting ears':'conducting-ear','Coiled inner-ear chambers and fluid':'cochlea','Hearing cells with tiny hairs':'hair-cells','Vibration-sensitive inner ears':'sensing-ear','Sound-receiving ears':'receiving-ear','Hearing pathways':'hearing-pathway','Inner ears with hearing pathways':'inner-pathway','Ears':'ears','Starchy food':'starch','Saliva':'saliva','Shorter starch chains':'short-starch','Digestive enzymes':'enzymes','Meal glucose':'glucose','Protein food':'protein-food','Meal amino acids':'amino-acids','Fat food':'fat','Bile':'bile','Small fat droplets':'fat-droplets','Fat digestion products':'fat-products'}.items():item_icons['name:'+k]='assets/'+v+'.png'
positions={ids('prelude-phospholipids'):[400,1630],ids('prelude-water'):[1160,1630],ids('opening-dna'):[400,2310],ids('opening-nuclear-envelope'):[1160,2310],ids('school-bone-mineral'):[1080,1750]}
for items in [['Outer ears and canals','Eardrums','Middle-ear bones','Coiled inner-ear chambers and fluid','Hearing cells with tiny hairs','Hearing pathways'],['Starchy food','Saliva','Digestive enzymes','Protein food','Fat food','Bile']]:
    for idx,k in enumerate(items):positions['name:'+k]=[[300,780,1260][idx%3],1600+int(idx/3)*680]
slots={ids('opening-cell'):{ids('opening-nucleus'):'assets/cell-nucleus-overlay.png',ids('opening-mitochondria'):'assets/cell-unused-overlay.png',ids('school-sugar-carrier'):'assets/cell-unused-overlay.png',ids('school-ribosome'):'assets/cell-unused-overlay.png'},ids('arm-front-tendons'):{ids('school-bone-mineral'):'assets/arm-radius-mineral.png',ids('prelude-myoblasts'):'assets/arm-biceps.png'},ids('arm-back-tendons'):{ids('school-bone-mineral'):'assets/arm-ulna-mineral.png',ids('prelude-myoblasts'):'assets/arm-triceps.png'}}
art={'headingIcon':'assets/identity.png','defaultIcon':'../../placeholder.svg','defaultOverlay':'assets/unillustrated-overlay.png','defaultBackground':'assets/unillustrated-background.png','chapterBackgrounds':{'1':'assets/cell-background.jpg','4':'assets/arm-background.jpg','8':'assets/hearing-background.jpg','18':'assets/digestion-background.jpg'},'itemIcons':item_icons,'slotIcons':slots,'itemPositions':positions,'hotspots':{'4':{ids('arm-front-tendons'):{'center':[780,1688],'icon':'assets/arm-front-base.png','hitbox':{'center':[550,655],'size':[170,490]}},ids('arm-back-tendons'):{'center':[780,1688],'icon':'assets/arm-back-base.png','hitbox':{'center':[397,655],'size':[140,490]}}}}}
(D/'art-map.json').write_text(json.dumps(art,indent=2)+'\n')
