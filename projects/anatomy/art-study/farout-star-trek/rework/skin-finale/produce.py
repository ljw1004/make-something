"""Extract selected generated rasters and assemble registered anatomical layers.
Run from anywhere: uv run --with pillow --with numpy python produce.py
No anatomical drawing is synthesized: polygons only mask source pixels.
"""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw,ImageChops
import numpy as np
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'assets'; OUT.mkdir(exist_ok=True)
PREFIX='rework/skin-finale/assets/'
items={}; slots={}; hotspots={}
def clean(im, threshold=80):
    a=np.array(im.convert('RGBA')); a[:,:,3][a[:,:,3]<threshold]=0
    return Image.fromarray(a)
def source(name): return clean(Image.open(ROOT/'sources'/f'{name}.png'))
S=source('skin-materials'); U=source('urinary'); R=source('renewal')
def crop(im,box):
    c=im.crop(box); b=c.getbbox(); return c.crop(b) if b else c
def tile(im,col,row,nc,nr):
    if im is R:
        boxes={
          (0,0):(0,15,415,270),(1,0):(430,25,835,270),(2,0):(850,45,1325,265),
          (0,1):(0,300,415,550),(1,1):(430,300,835,550),(2,1):(850,300,1325,545),
          (0,2):(0,565,415,815),(1,2):(420,560,835,815),(2,2):(845,560,1328,815),
          (0,3):(0,840,390,1145),(1,3):(398,835,820,1150),(2,3):(840,840,1325,1150)}
        return crop(im,boxes[(col,row)])
    w,h=im.size
    return crop(im,(round(col*w/nc),round(row*h/nr),round((col+1)*w/nc),round((row+1)*h/nr)))
def size(im,w,h=None): return im.resize((w,h or round(im.height*w/im.width)),Image.Resampling.LANCZOS)
def canvas(w=800,h=650):return Image.new('RGBA',(w,h))
def put(base,im,x,y,w=None,h=None):
    if w: im=size(im,w,h)
    base.alpha_composite(im,(x,y));return base
def mask(im,points,keep=True):
    m=Image.new('L',im.size,0 if keep else 255);ImageDraw.Draw(m).polygon(points,fill=255 if keep else 0)
    out=im.copy();out.putalpha(ImageChops.multiply(im.getchannel('A'),m));return out
def save(name,im,identity=None):
    im.save(OUT/f'{name}.png')
    if identity:items[identity]=PREFIX+name+'.png'
    return im
def item(identity,im,name=None):return save(name or re.sub('[^a-z0-9]+','-',identity.split(':',1)[1].lower()).strip('-'),im,identity)
def fitting(owner,accepted,name,im):
    save(name,im);slots.setdefault(owner,{})[accepted]=PREFIX+name+'.png'
def extract(im,c,r,nc,nr,w,h=None):return size(tile(im,c,r,nc,nr),w,h)

# Skin construction: every part is sized in anticipation of the same 600px section.
outer=extract(S,0,0,4,4,600,120); lipids=extract(S,1,0,4,4,600,55)
tissue=extract(S,2,0,4,4,600,300);vessels=extract(S,3,0,4,4,570,200)
coil=extract(S,0,1,4,4,145,100);duct=extract(S,1,1,4,4,28,280)
nerves=extract(S,2,1,4,4,270,270);locator=extract(S,3,1,4,4,92,280)
def local():return put(canvas(),locator,20,245)
outer_layer=put(local(),outer,150,110)
lipid_layer=put(canvas(),lipids,150,110)
surface=outer_layer.copy();surface.alpha_composite(lipid_layer)
tissue_layer=put(local(),tissue,150,230)
vessel_layer=put(canvas(),vessels,165,310)
gland_layer=put(put(canvas(),coil,260,415),duct,320,145)
nerve_layer=put(canvas(),nerves,465,240)
base=surface.copy();base.alpha_composite(tissue_layer);base.alpha_composite(vessel_layer)
living=tissue_layer.copy();living.alpha_composite(vessel_layer)
awaiting=surface.copy();awaiting.alpha_composite(tissue_layer)
item('name:Outer skin cells',size(outer,600))
item('name:Lipids between skin cells',lipids)
item('name:Supporting skin tissue',tissue)
item('name:Skin blood vessels',vessels)
item('name:Sweat gland coil',coil)
item('name:Sweat gland duct',duct)
item('name:Skin nerve endings',nerves)
item('name:Water-resistant skin surface',surface)
item('name:Living deeper skin',living)
item('name:Skin layers awaiting blood vessels',awaiting)
item('name:Skin segment',base)
gland=crop(gland_layer,(200,100,440,540));item('name:Sweat gland and duct',gland)
fitting('name:Skin segment','name:Sweat gland and duct','skin-gland-fitted',gland_layer)
fitting('name:Skin segment','name:Skin nerve endings','skin-nerves-fitted',nerve_layer)
complete=base.copy();complete.alpha_composite(gland_layer);complete.alpha_composite(nerve_layer)
save('skin-completed',complete)

# Wound states preserve all neighboring skin pixels; masks remove only the breach.
gap=[(415,110),(455,110),(448,180),(462,245),(450,305),(462,405),(424,405),(421,310),(430,245),(415,180)]
cut=mask(complete,gap,False)
platelets=extract(S,1,2,4,4,70,48);threads=extract(S,3,2,4,4,80,50)
plug=put(cut.copy(),platelets,405,365)
clot=put(plug.copy(),threads,400,364)
item('name:Skin with a cut',cut);item('name:Skin with a platelet plug',plug);item('name:Skin with a reinforced clot',clot)
item('name:Rough edge',extract(S,0,2,4,4,340))
item('name:Platelets at the cut',platelets)
item('name:Dissolved clotting protein',extract(S,2,2,4,4,150))
item('name:Clotting protein threads',threads)
item('name:Clotting enzymes',extract(S,0,3,4,4,140))
white=extract(S,1,3,4,4,170); item('name:Debris-clearing white blood cells',white)
cleared=put(clot.copy(),size(white,75),465,280)
item('name:Skin with a cleared wound',cleared)
newcells=outer.crop((250,0,350,120));fibres=extract(S,3,3,4,4,100,125)
surfacefit=put(canvas(),newcells,390,110)
fibrefit=put(canvas(),tissue.crop((245,0,315,135)),407,225)
put(fibrefit,fibres,395,225)
# Rejoin the severed red branch with its original vascular pixels and endpoints.
sproutfit=mask(vessel_layer,[(407,355),(480,355),(480,415),(407,415)])
sprout=mask(vessel_layer,[(385,350),(450,350),(450,410),(385,410)]).crop((385,350,450,410))
fitting('name:Skin with a cleared wound','name:New skin cells','repair-surface-fitted',surfacefit)
fitting('name:Skin with a cleared wound','name:New supporting protein fibres','repair-support-fitted',fibrefit)
fitting('name:Skin with a cleared wound','name:Capillary sprout','repair-capillary-fitted',sproutfit)
item('name:New skin cells',newcells);item('name:New supporting protein fibres',fibres);item('name:Capillary sprout',sprout)
repaired=cut.copy();repaired.alpha_composite(surfacefit)
put(repaired,tissue.crop((275,0,325,180)),415,225)
repaired.alpha_composite(fibrefit);repaired.alpha_composite(sproutfit)
item('name:Repaired skin segment',repaired)
item('name:Nearby capillary',vessel_layer.crop((350,350,420,410)))
item('name:Protein messengers from the wound',extract(R,2,1,3,4,430))
item('name:Support-building skin cells',extract(R,1,0,3,4,360))
item('id:school-repair-protein-blocks',extract(R,0,1,3,4,270))
item('name:Skin cells at the cut\'s edge',extract(R,2,0,3,4,400))
item('id:school-repair-fuel',extract(R,1,1,3,4,270))
item('name:Clot-clearing enzymes',extract(R,0,2,3,4,220))

# Renewal uses the same skin cells, actual marrow, and cell-bound iron.
item('id:rf-worn-red-cells',extract(R,1,2,3,4,260))
item('id:rf-spleen-recyclers',extract(R,2,2,3,4,430))
item('id:rf-recovered-iron',extract(R,0,3,3,4,260))
marrow=extract(R,1,3,3,4,560)
item('id:rf-blood-forming-marrow',marrow)
newred=marrow.crop((110,150,560,marrow.height))
item('id:rf-new-red-cells',newred)
skinbase=put(canvas(650,380),size(tissue,600,180),25,170);put(skinbase,outer,25,50);put(skinbase,size(vessels,560,100),40,240)
item('id:rf-skin-base',skinbase)
newskin=skinbase.copy();put(newskin,size(newcells,100,65),275,130)
item('id:rf-new-skin-cells',newskin)
item('id:rf-skin-materials',extract(R,1,1,3,4,270))

# Urinary system is decomposed from ONE master, keeping outlet registration.
urinary=extract(U,0,0,3,3,540,650)
kidney=mask(urinary,[(0,0),(540,0),(540,265),(0,265)])
ureters=mask(urinary,[(0,265),(540,265),(540,462),(0,462)])
bladder=mask(urinary,[(0,462),(540,462),(540,650),(0,650)])
item('name:Urinary system',kidney)
item('name:Ureters',crop(ureters,(0,0,540,650)))
item('name:Bladder',crop(bladder,(0,0,540,650)))
fitting('name:Urinary system','name:Ureters','ureters-fitted',ureters)
fitting('name:Urinary system','name:Bladder','bladder-fitted',bladder)
save('urinary-completed',urinary)
item('name:Kidney filter',extract(U,1,0,3,3,650))
item('name:Kidney recovery tube',extract(U,2,0,3,3,650))
item('name:Filtered kidney fluid',extract(U,0,1,3,3,540))
item('name:Urine',extract(U,1,1,3,3,540))
item('name:Concentrated urine',extract(U,2,1,3,3,540))
item('id:water-gut-capillary',extract(U,0,2,3,3,650))
item('name:Drinking water',extract(U,1,2,3,3,260,110))

# Finale: supplied tissues and true organs retain scale on the 800x1600 body.
body=size(source('body'),800,1600)
arm=mask(body,[(0,260),(270,260),(275,405),(233,530),(205,600),(190,690),(160,790),(140,920),(0,920)])
# Carry the actual studied flexed-arm view through its whole-model pose handoff.
studied=Image.open(ROOT.parent/'opening/assets/arm-complete.png').convert('RGBA')
sa=np.array(studied); navy=(sa[:,:,0]<48)&(sa[:,:,1]<75)&(sa[:,:,2]<105)
sa[:,:,3][navy]=0;studied=Image.fromarray(sa)
studied=mask(studied,[(0,0),(300,0),(330,470),(735,650),(735,903),(540,903),(340,690),(150,570),(0,480)])
arm_inset=put(canvas(800,1600),size(studied,170,208),5,345)
inset_mark=ImageDraw.Draw(arm_inset)
inset_mark.rectangle((3,343,177,555),outline=(120,221,241,230),width=2)
inset_mark.line([(177,525),(190,544)],fill=(120,221,241,230),width=2)
arm.alpha_composite(arm_inset)
item('name:Arm assembly',crop(arm,(0,240,285,940)))
save('arm-on-body-canvas',arm)
lower=size(source('lower'),800,1600).crop((0,490,800,1600))
item('name:Lower body',lower)
finalurinary=size(urinary,290,330)
item('id:final-urinary-organs',finalurinary)
urfit=put(canvas(800,1110),finalurinary,255,30)
fitting('name:Lower body','id:final-urinary-organs','lower-urinary-fitted',urfit)
ears=extract(R,2,3,3,4,120,72);item('id:final-ears',ears)
cover=size(source('cover'),800,1600)
cover=mask(cover,[(116,615),(145,622),(134,673),(105,665)],False)
item('name:Skin covering',cover)
skin_only=repaired.crop((150,110,750,530))
coverfit=put(canvas(800,1600),size(skin_only,48,34),103,624)
# An enlarged forearm inset remains within the same transparent object canvas.
put(coverfit,size(repaired,245,199),0,1110)
fitting('name:Skin covering','name:Repaired skin segment','cover-skin-fitted',coverfit)
trunk=mask(body,[(0,260),(800,260),(800,1600),(0,1600)])
trunk=mask(trunk,[(270,490),(530,490),(535,695),(472,755),(340,755),(265,695)],False)
# Replace the lower regional tissue with the exact supplied lower-body component.
trunk=mask(trunk,[(270,490),(535,490),(595,780),(610,1600),(190,1600),(205,780)],False)
put(trunk,lower,0,490)
chestdir=ROOT.parent/'senses-circulation/assets'
connectedpath=chestdir/'heart-pulmonary-connected-reference.png'
if connectedpath.exists():
    # Retain the connected heart, both pulmonary arteries/veins and lung meshes as ONE raster.
    connected=clean(Image.open(connectedpath));connected=connected.crop(connected.getbbox())
    lungview=clean(Image.open(chestdir/'lungs.png')).crop((0,0,512,550))
    lungview=mask(lungview,[(0,0),(512,0),(512,550),(390,510),(270,460),(240,460),(110,510),(0,550)])
    organlayer=put(canvas(1000,1100),lungview,244,40)
    put(organlayer,size(connected,570,336),215,230)
    # Reuse only the upper actual trachea; the connected vascular group stays uncut.
    airways=clean(Image.open(chestdir/'branching-airways.png'))
    put(organlayer,airways.crop((185,0,325,230)),429,40)
    ribmaster=clean(Image.open(ROOT.parent/'senses-circulation/sources/chest.png')).crop((15,0,710,724))
    ribfront=size(ribmaster,680,710);ribfront.putalpha(ribfront.getchannel('A').point(lambda v:round(v*.25)))
    put(organlayer,ribfront,160,110)
    connected_final=size(organlayer,298,220);save('connected-chest-organs-final',connected_final)
    chest_complete=Image.open(chestdir/'final-chest-base.png').convert('RGBA')
    chest_complete.alpha_composite(connected_final)
    for n in ['diaphragm','lymph']:
        chest_complete.alpha_composite(Image.open(chestdir/f'final-chest-slot-{n}.png').convert('RGBA'))
    save('connected-chest-complete',chest_complete)
    chestpath=OUT/'connected-chest-complete.png'
else:
    chestpath=chestdir/'final-chest-complete.png'
if chestpath.exists():
    chest=clean(Image.open(chestpath))
    cavity=[(305,300),(495,300),(530,350),(528,480),(500,535),(310,535),(270,470),(275,355)]
    trunk=mask(trunk,cavity,False)
    # Actual supplied supporting tissue backs the replaced organs; preserve shoulder edges.
    support=size(source('lower'),800,1600).crop((270,420,530,710))
    support_layer=put(canvas(800,1600),size(support,300,360),250,235)
    support_layer=mask(support_layer,cavity)
    trunk.alpha_composite(support_layer)
    put(trunk,size(chest,477,352),163,203)
trunk.alpha_composite(arm_inset)
put(trunk,urfit,0,490)
gutpath=ROOT.parent/'defense-digestion/assets/digestive-tract.png'
if gutpath.exists():
    gut=clean(Image.open(gutpath)); gut=size(gut,250,360)
    gutfit=put(canvas(800,1110),gut,275,0)
else:
    # Source-only fallback waits for the sibling's final exported organ master.
    gut=crop(body,(275,470,535,760));gutfit=put(canvas(800,1110),gut,275,0)
fitting('name:Lower body','name:Digestive tract','lower-digestive-fitted',gutfit)
save('final-digestive-tract',size(gut,156,225))
save('final-repaired-skin',size(repaired,153,124))
put(trunk,gutfit,0,490)
item('name:Trunk and limbs',trunk)
neuralpath=ROOT.parent/'opening/assets/nervous-system-complete.png'
if neuralpath.exists():
    neural=size(Image.open(neuralpath).convert('RGBA'),800,1600)
    # Preserve the single body silhouette where source models differ slightly in stance.
    na=np.array(neural);ba=np.array(body.getchannel('A'))
    na[260:,:,3]=(na[260:,:,3].astype('uint16')*ba[260:,:]//255).astype('uint8')
    neural=Image.fromarray(na)
    beneath=neural.copy();beneath.alpha_composite(trunk)
    # Retain actual source nerve pixels as a translucent foreground dissection.
    a=np.array(neural);gold=(a[:,:,0]>130)&(a[:,:,1]>90)&(a[:,:,2]<a[:,:,0]*.65)
    a[:,:,3]=np.where(gold,a[:,:,3]*.25,0).astype('uint8');a[:250,:,3]=0
    beneath.alpha_composite(Image.fromarray(a))
else:
    beneath=trunk.copy();put(beneath,body.crop((0,0,800,260)),0,0)
item('name:Body beneath the skin',beneath)
# Same body, broad internal inspection opening in fitted covering.
cutcover=mask(cover,[(278,265),(535,265),(548,700),(480,780),(330,780),(250,600)],False)
cutcover=mask(cutcover,[(210,330),(250,360),(205,600),(150,650),(160,570)],False)
cutcover=mask(cutcover,[(360,35),(430,30),(450,180),(360,190)],False)
final=beneath.copy();final.alpha_composite(cutcover);final.alpha_composite(coverfit)
final.alpha_composite(arm_inset)
item('name:Body',final)

# The finale keeps one shared registration, exported at a phone-compatible scale.
final_ids=['name:Arm assembly','name:Lower body','id:final-urinary-organs','id:final-ears','name:Skin covering','name:Trunk and limbs','name:Body beneath the skin','name:Body']
final_paths={items[k] for k in final_ids}
for owner in ['name:Lower body','name:Skin covering']:
    final_paths.update(slots[owner].values())
for path in final_paths:
    target=OUT/Path(path).name; im=Image.open(target)
    size(im,round(im.width*.625),round(im.height*.625)).save(target)

# Finale chest requires a taller canvas so the arm stays at true body scale.
# Supplementary presentation only: original chest identity ownership stays unchanged.
final_breathing=None
early_presentations={}
chestdir=ROOT.parent/'senses-circulation/assets'
if (chestdir/'final-chest-base.png').exists():
    opposite=mask(body,[(530,260),(800,260),(800,940),(660,940),(620,760),(580,600),(565,520),(530,410)])
    opposite=size(opposite,500,1000).crop((0,127,500,597))
    chestbase=canvas(500,470);put(chestbase,Image.open(chestdir/'final-chest-base.png').convert('RGBA'),102,0)
    early_chestbase=chestbase.copy()
    chestbase.alpha_composite(opposite)
    save('final-breathing-base',chestbase)
    save('breathing-base-early',size(early_chestbase,1000,940))
    chestmaster=Image.open(ROOT.parent/'senses-circulation/sources/chest.png').convert('RGBA')
    for name,accepted,box in [('rib-cage','name:Rib cage',(15,0,710,724)),('intercostal-muscles','name:Muscles between the ribs',(745,0,1420,724))]:
        part=size(chestmaster.crop(box),680,710)
        if name=='intercostal-muscles':
            pa=np.array(part);r,g,b=[pa[:,:,i].astype(float) for i in range(3)]
            pa[:,:,3]=np.where((r>g*1.10)&(r>b*1.05),pa[:,:,3],0);part=Image.fromarray(pa)
        source_layer=put(canvas(1000,1100),part,160,110)
        final_layer=put(canvas(500,470),size(source_layer,298,220),102,0)
        early_layer=size(final_layer,1000,940)
        loose=early_layer.crop(early_layer.getbbox());save(f'early-loose-{name}',loose)
        early_presentations[accepted]={'path':PREFIX+f'early-loose-{name}.png','size':list(loose.size)}
    cslots={}
    eslots={}
    for name,accepted in [('diaphragm','name:Diaphragm'),('heart-and-lungs','name:Heart and lungs'),('lymph','name:Lymph drainage network')]:
        src=OUT/'connected-chest-organs-final.png' if name=='heart-and-lungs' and connectedpath.exists() else chestdir/f'final-chest-slot-{name}.png'
        layer=put(canvas(500,470),Image.open(src).convert('RGBA'),102,0)
        save(f'final-breathing-{name}',layer);cslots[accepted]=PREFIX+f'final-breathing-{name}.png'
        save(f'breathing-{name}-early',size(layer,1000,940));eslots[accepted]=PREFIX+f'breathing-{name}-early.png'
        loose=layer.crop(layer.getbbox());save(f'final-loose-{name}',loose)
        if name in ['diaphragm','heart-and-lungs']:
            loose=size(loose,loose.width*2,loose.height*2);save(f'early-loose-{name}',loose)
            early_presentations[accepted]={'path':PREFIX+f'early-loose-{name}.png','size':list(loose.size)}
    finalarm=size(arm,500,1000).crop((0,127,500,597))
    save('final-breathing-arm',finalarm);cslots['name:Arm assembly']=PREFIX+'final-breathing-arm.png'
    save('breathing-arm-early',size(finalarm,1000,940));eslots['name:Arm assembly']=PREFIX+'breathing-arm-early.png'
    item('name:Arm assembly',finalarm.crop(finalarm.getbbox()))
    lymph=Image.open(OUT/'final-breathing-lymph.png');lymph=lymph.crop(lymph.getbbox());save('final-lymph-network',lymph)
    final_breathing={'path':PREFIX+'final-breathing-base.png','size':[500,470],'slotIcons':cslots}
    early_presentations['name:Breathing apparatus']={'path':PREFIX+'breathing-base-early.png','size':[1000,940],'slotIcons':eslots}

def hotspot(ch,id,center,size_,icon=None,hitcenter=None):
    hotspots.setdefault(str(ch),{})[id]={'center':center,'icon':icon or items[id],'hitbox':{'center':hitcenter or center,'size':size_}}
hotspot(22,'name:Kidney filter',[420,1000],[600,550])
hotspot(22,'name:Kidney recovery tube',[1130,1000],[600,550])
hotspot(23,'name:Urinary system',[420,1100],[540,650])
hotspot(23,'id:water-gut-capillary',[1120,1100],[570,135],hitcenter=[1120,1300])
hotspot(25,'name:Rough edge',[780,800],[360,160])
manifest={'itemIcons':items,'slotIcons':slots,'hotspots':hotspots}
(ROOT/'map.json').write_text(json.dumps(manifest,indent=2)+'\n')
presentations={
    'name:Digestive tract':{'path':PREFIX+'final-digestive-tract.png','size':[156,225]},
    'name:Repaired skin segment':{'path':PREFIX+'final-repaired-skin.png','size':[153,124]}
}
if final_breathing:
    presentations['name:Breathing apparatus']=final_breathing
    presentations['name:Lymph drainage network']={'path':PREFIX+'final-lymph-network.png','size':list(lymph.size)}
(ROOT/'finale-presentations.json').write_text(json.dumps(presentations,indent=2)+'\n')
(ROOT/'chapter14-presentations.json').write_text(json.dumps(early_presentations,indent=2)+'\n')
print(f'{len(items)} item identities; {sum(map(len,slots.values()))} registered fittings')
