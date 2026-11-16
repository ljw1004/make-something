"""Mechanical extraction/registration of selected built-in raster generations.
Run: uv run --with pillow python projects/anatomy/art-study/farout-cozy/export.py
No anatomy is code-drawn: crops, transparency cleanup and fitted-layer registration only.
"""
from PIL import Image, ImageOps, ImageDraw, ImageChops, ImageFilter
from pathlib import Path
from collections import deque
import json, math

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'assets'
OUT.mkdir(exist_ok=True)
L=Image.Resampling.LANCZOS
images={}

def extract(source,box,name,size=280,paper=False):
    im=Image.open(ROOT/'sources'/source).convert('RGBA').crop(box)
    if paper:
        # Remove only border-connected pale generated paper, preserving enclosed detail.
        px=im.load(); w,h=im.size; seen=set(); q=deque()
        for x in range(w): q.extend(((x,0),(x,h-1)))
        for y in range(h): q.extend(((0,y),(w-1,y)))
        while q:
            x,y=q.popleft()
            if (x,y) in seen or not(0<=x<w and 0<=y<h): continue
            seen.add((x,y));r,g,b,a=px[x,y]
            if a<30 or (min(r,g,b)>198 and max(r,g,b)-min(r,g,b)<57):
                px[x,y]=(r,g,b,0)
                q.extend(((x-1,y),(x+1,y),(x,y-1),(x,y+1)))
    a=im.getchannel('A').point(lambda x:0 if x<28 else x)
    im.putalpha(a)
    bounds=im.getbbox()
    if bounds: im=im.crop(bounds)
    im.thumbnail((size,size),L)
    canvas=Image.new('RGBA',(im.width+12,im.height+12))
    canvas.alpha_composite(im,(6,6));canvas.save(OUT/(name+'.png'))
    images[name]=canvas
    return canvas

cell_names=['lipids','water','dna-old','envelope','nucleus','cell','muscle-cells','mineral','biceps','triceps','radius-mineral','ulna-mineral']
for i,n in enumerate(cell_names):
    if n=='dna-old': continue
    col=i%4;row=i//4
    ys=[(0,360),(368,710),(725,1082)][row]
    extract('cell-arm-atlas.png',(col*362+3,ys[0],(col+1)*362-3,ys[1]),n,400 if n=='cell' else 272)

ear_names=['outer-ear','eardrum','outer-eardrum','ossicles','conducting-ear','cochlea','hair-cells','sensing-ear','receiving-ear','hearing-pathways','inner-pathways','ears']
for i,n in enumerate(ear_names):
    col=i%4;row=i//4; ys=[(12,352),(375,711),(755,1041)][row]
    # Row two's sound-conducting drawing protrudes into the nominal next cell.
    xs=[(0,381),(388,714),(721,1067),(1073,1448)] if row==1 else [(0,359),(374,719),(723,1064),(1067,1448)]
    extract('hearing-atlas.png',(xs[col][0],ys[0],xs[col][1],ys[1]),n,320 if n in ['ears','receiving-ear','inner-pathways','conducting-ear'] else 272,True)

food_names=['starch','saliva','short-starch','enzymes','glucose','protein-food','amino-acids','fat','bile','droplets','fat-products','dna']
for i,n in enumerate(food_names):
    col=i%4;row=i//4;ys=[(70,352),(400,669),(704,1017)][row]
    box=(col*362+2,ys[0],(col+1)*362-2,ys[1])
    if row==1: box=[(40,410,310,650),(345,410,708,669),(730,410,1077,669),(1110,400,1435,672)][col]
    extract('digestion-atlas.png',box,n)

# Revision: all anatomy belongs to interactive sprites. Only an empty, selected
# paper crop from the original background generation is tiled for the work sheet.
bg=Image.open(ROOT/'sources/background-atlas.png').convert('RGB')
tile=bg.crop((190,475,400,585)).resize((420,220),L)
paper=Image.new('RGB',(780,1688))
for row,py in enumerate(range(0,1688,tile.height)):
    for col,px in enumerate(range(0,780,tile.width)):
        piece=ImageOps.mirror(tile) if col%2 else tile
        if row%2:piece=ImageOps.flip(piece)
        paper.paste(piece,(px,py))
for n in ['cell','arm','hearing','digestion']:
    paper.save(OUT/('background-'+n+'.jpg'),quality=94)

def save(name,im):
    images[name]=im; im.save(OUT/(name+'.png'));return im

def tight(im):
    return im.crop(im.getbbox())

def fit(im,size):
    im=tight(im).copy();im.thumbnail(size,L);return im

def masked(im,mask):
    result=im.copy();result.putalpha(ImageChops.multiply(im.getchannel('A'),mask));return result

# Derive the water volume and bilayer from the actual membrane-bag master.
# Masks divide existing pixels; they paint no new scientific content.
base=images['cell']
w,h=base.size
lumen=Image.new('L',base.size);ImageDraw.Draw(lumen).ellipse((w*.17,h*.16,w*.85,h*.83),fill=255)
water=masked(base,lumen);save('water',tight(water))
inner=Image.new('L',base.size);ImageDraw.Draw(inner).ellipse((w*.12,h*.12,w*.89,h*.88),fill=255)
wall=masked(base,ImageChops.invert(inner))
# The lipid input is a curved bilayer section, at the bag's repeating-unit scale.
section=Image.new('L',base.size);ImageDraw.Draw(section).rectangle((0,0,w//2,h),fill=255)
save('lipids',tight(masked(wall,section)))
# Nuclear material retains exactly the pixels and magnification used when fitted.
envelope=fit(images['envelope'],(158,158));save('envelope',envelope)
dna=fit(images['dna'],(65,105));save('dna',dna)
nucleus=envelope.copy();nucleus.alpha_composite(dna,((nucleus.width-dna.width)//2,(nucleus.height-dna.height)//2));save('nucleus',nucleus)
overlay=Image.new('RGBA',base.size)
overlay.alpha_composite(nucleus,((base.width-nucleus.width)//2,(base.height-nucleus.height)//2))
save('cell-nucleus',overlay)
Image.new('RGBA',base.size).save(OUT/'cell-empty-overlay.png')

# A single canonical hearing assembly. Every stage composites the SAME part
# pixels at the SAME positions; tight cropping never normalizes their scale.
parts={
 'outer':(fit(images['outer-ear'],(300,300)),(0,115)),
 'drum':(fit(images['eardrum'],(62,110)),(270,220)),
 'bones':(fit(images['ossicles'],(138,115)),(316,217)),
 'coil':(fit(images['cochlea'],(210,240)),(439,167)),
 'nerve':(fit(images['hearing-pathways'],(280,220)),(650,215)),
}
# Use the generated located magnification, not an independently redrawn stage.
inset=extract('hearing-atlas.png',(1250,377,1448,576),'hair-cells',202,True)
mask=Image.new('L',inset.size);draw=ImageDraw.Draw(mask)
draw.ellipse((31,3,inset.width-1,175),fill=255)
draw.polygon([(4,200),(50,140),(78,162)],fill=255)
inset=masked(inset,mask)
parts['hair']=(inset,(550,0))
# The pointed lower-left inset edge locates its magnified cells at the cochlea.
def ear(name,keys):
    canvas=Image.new('RGBA',(930,440))
    for key in keys:
        piece,pos=parts[key];canvas.alpha_composite(piece,pos)
    save(name,tight(canvas))
ear_states={
 'outer-ear':['outer'],'eardrum':['drum'],'outer-eardrum':['outer','drum'],
 'ossicles':['bones'],'conducting-ear':['outer','drum','bones'],
 'cochlea':['coil'],'hair-cells':['hair'],'sensing-ear':['coil','hair'],
 'receiving-ear':['outer','drum','bones','coil','hair'],
 'hearing-pathways':['nerve'],'inner-pathways':['coil','hair','nerve'],
 'ears':['outer','drum','bones','coil','hair','nerve'],
}
for n,k in ear_states.items():ear(n,k)
(ROOT/'registration.json').write_text(json.dumps({'hearing':{'canvas':[930,440],'parts':{k:{'position':list(pos),'size':list(piece.size)} for k,(piece,pos) in parts.items()},'states':ear_states,'export':'Crop alpha bounds only; never resize assembled stages.'},'cell':{'canvas':list(base.size),'nucleusPosition':[(base.width-nucleus.width)//2,(base.height-nucleus.height)//2],'water':'Selected lumen pixels from cell master','lipids':'Left curved bilayer from same cell master'},'arm':{'source':'sources/background-atlas.png','sourcePanelOrigin':[629,2],'bounds':[170,0,425,623],'scale':780/623*2,'receiverLayers':'Complementary left/right portions of one arm; same common canvas.','independentFittings':4,'legalPartialCombinations':16}},indent=2)+'\n')

# The arm was previously baked into the sheet. Extract that original arm with
# its full hand into a common registered receiver canvas, preserving its pose.
S=780/623
bounds=(170,0,425,623)
cw=round((bounds[2]-bounds[0])*S*2);ch=round((bounds[3]-bounds[1])*S*2)
arm=bg.crop((629+bounds[0],2+bounds[1],629+bounds[2],2+bounds[3])).convert('RGBA')
# Flood only border-connected cream paper. Brown anatomy outlines preserve the
# pale bone interior. Crop excludes the separate miniature arm and ginkgo.
px=arm.load();aw,ah=arm.size;seen=set();q=deque()
for x in range(aw):q.extend(((x,0),(x,ah-1)))
for y in range(ah):q.extend(((0,y),(aw-1,y)))
while q:
    x,y=q.popleft()
    if (x,y) in seen or not(0<=x<aw and 0<=y<ah):continue
    seen.add((x,y));r,g,b,a=px[x,y]
    if r>225 and g>180 and b>155:
        px[x,y]=(r,g,b,0);q.extend(((x-1,y),(x+1,y),(x,y-1),(x,y+1)))
# Close one-pixel paper leaks and discard detached flecks from the wash.
a=arm.getchannel('A').filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
ap=a.load();visited=set()
for yy in range(ah):
    for xx in range(aw):
        if (xx,yy) in visited or ap[xx,yy]<20:continue
        group=[];queue=deque([(xx,yy)]);visited.add((xx,yy))
        while queue:
            x,y=queue.popleft();group.append((x,y))
            for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if 0<=nx<aw and 0<=ny<ah and (nx,ny) not in visited and ap[nx,ny]>=20:
                    visited.add((nx,ny));queue.append((nx,ny))
        if len(group)<80:
            for x,y in group:ap[x,y]=0
arm.putalpha(a)
arm=arm.resize((cw,ch),L)
# Split complementary receiver layers so an empty owner's base cannot occlude
# the other owner's already fitted muscle. Together these show exactly one arm.
split=round((365-bounds[0])*S*2)
for name,left,right in [('arm-base',0,split),('arm-back-base',split,cw)]:
    mask=Image.new('L',(cw,ch));ImageDraw.Draw(mask).rectangle((left,0,right-1,ch),fill=255)
    save(name,masked(arm,mask))
def arm_layer(name,source,top,bottom,width,bend=0):
    canvas=Image.new('RGBA',(cw,ch));piece=tight(images[source])
    height=bottom[1]-top[1]
    piece=piece.resize((round(width*S*2),round(height*S*2)),L)
    for py in range(piece.height):
        t=py/max(1,piece.height-1)
        center=top[0]*(1-t)+bottom[0]*t+bend*math.sin(math.pi*t)
        x=round((center-bounds[0])*S*2-piece.width/2)
        y=round((top[1]-bounds[1])*S*2)+py
        canvas.alpha_composite(piece.crop((0,py,piece.width,py+1)),(x,y))
    save(name,canvas)
arm_layer('arm-biceps','biceps',(334,82),(342,302),55,-27)
arm_layer('arm-triceps','triceps',(380,65),(385,291),48,20)
arm_layer('arm-radius-mineral','radius-mineral',(350,339),(350,395),19)
arm_layer('arm-ulna-mineral','ulna-mineral',(382,337),(382,393),18)

# Neutral placeholders are explicit in every unillustrated chapter.
Image.new('RGBA',(1,1)).save(OUT/'neutral-overlay.png')
heading=Image.new('RGBA',(320,320));thumb=images['nucleus'].copy();thumb.thumbnail((280,280),L)
heading.alpha_composite(thumb,((320-thumb.width)//2,(320-thumb.height)//2));heading.save(OUT/'icon.png')

iconmap={}
for id,n in [('prelude-phospholipids','lipids'),('prelude-water','water'),('opening-dna','dna'),('opening-nuclear-envelope','envelope'),('opening-nucleus','nucleus'),('opening-cell','cell'),('prelude-myoblasts','muscle-cells'),('school-bone-mineral','mineral'),('arm-front-tendons','arm-base'),('arm-back-tendons','arm-back-base')]:iconmap['id:'+id]='assets/'+n+'.png'
ear_ids=['Outer ears and canals','Eardrums','Outer ears with eardrums','Middle-ear bones','Sound-conducting ears','Coiled inner-ear chambers and fluid','Hearing cells with tiny hairs','Vibration-sensitive inner ears','Sound-receiving ears','Hearing pathways','Inner ears with hearing pathways','Ears']
food_ids=['Starchy food','Saliva','Shorter starch chains','Digestive enzymes','Meal glucose','Protein food','Meal amino acids','Fat food','Bile','Small fat droplets','Fat digestion products']
for ids,names in [(ear_ids,ear_names),(food_ids,food_names)]:
    for id,n in zip(ids,names):iconmap['name:'+id]='assets/'+n+'.png'
center=[round(((bounds[0]+bounds[2])/2-2)*S,2),round(((bounds[1]+bounds[3])/2-2)*S,2)]
mapping={'headingIcon':'assets/icon.png','defaultIcon':'../../placeholder.svg','defaultOverlay':'assets/neutral-overlay.png','defaultBackground':'../../placeholder.svg','chapterBackgrounds':{str(c):'assets/background-'+n+'.jpg' for c,n in [(1,'cell'),(4,'arm'),(8,'hearing'),(18,'digestion')]},'itemIcons':iconmap,'slotIcons':{'id:opening-cell':{'id:opening-nucleus':'assets/cell-nucleus.png',**{'id:'+i:'assets/cell-empty-overlay.png' for i in ['opening-mitochondria','school-sugar-carrier','school-ribosome']}},'id:arm-front-tendons':{'id:school-bone-mineral':'assets/arm-radius-mineral.png','id:prelude-myoblasts':'assets/arm-biceps.png'},'id:arm-back-tendons':{'id:school-bone-mineral':'assets/arm-ulna-mineral.png','id:prelude-myoblasts':'assets/arm-triceps.png'}},'hotspots':{'4':{'id:arm-front-tendons':{'center':center,'icon':'assets/arm-base.png','hitbox':{'center':[round(315*S,2),round(230*S,2)],'size':[round(82*S,2),round(350*S,2)]}},'id:arm-back-tendons':{'center':center,'icon':'assets/arm-back-base.png','hitbox':{'center':[round(395*S,2),round(230*S,2)],'size':[round(60*S,2),round(350*S,2)]}}}}}
(ROOT/'art-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
print('Exported',len(iconmap),'item icons, four backgrounds and five selected fittings.')
