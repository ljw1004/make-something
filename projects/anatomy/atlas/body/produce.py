"""Extract builtin-generated atlas specimens and register their physical constituents.
Run: uv run --with pillow --with numpy --with scipy python projects/anatomy/atlas/body/produce.py
No anatomical strokes are synthesized; masks crop existing specimen pixels.
"""
from pathlib import Path
import json,re,itertools
from PIL import Image,ImageDraw,ImageChops
import numpy as np
from scipy import ndimage
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
PREFIX='atlas/body/assets/'
items={};slots={};hotspots={};presentations={};placements={}
def canvas(w=900,h=650):return Image.new('RGBA',(w,h))
def clean(im):
 a=np.array(im.convert('RGBA'));a[:,:,3][a[:,:,3]<20]=0
 return Image.fromarray(a)
def source(n):return clean(Image.open(ROOT/'sources'/f'{n}.png'))
def crop(im,box=None):
 im=im.crop(box) if box else im.copy();bb=im.getbbox();return im.crop(bb) if bb else im

def tile(n,c,r,nc=4,nr=3):
 im=source(n);w,h=im.size
 boxes={('repair',0,1):(0,341,384,640),('repair',0,2):(0,683,365,1024),('urinary',0,0):(0,80,384,435),('urinary',1,0):(480,0,690,510),('metabolism',1,2):(390,683,739,1024),('repair',1,1):(390,345,765,659),('repair',3,1):(1154,345,1536,650),('repair',1,2):(405,660,752,1024),('repair',2,2):(768,665,1120,1024)}
 out=crop(im,boxes.get((n,c,r),(round(c*w/nc),round(r*h/nr),round((c+1)*w/nc),round((r+1)*h/nr))))
 if (n,c,r) in [('metabolism',0,1),('metabolism',1,1),('metabolism',2,1),('repair',0,1),('repair',0,2),('repair',1,2),('repair',2,2)]:
  a=np.asarray(out.getchannel('A')).copy();lab,count=ndimage.label(ndimage.binary_dilation(a>20,iterations=2));counts=np.bincount(lab.ravel());counts[0]=0;keep=counts>=max(60,counts.max()*.06);a[~keep[lab]]=0;out.putalpha(Image.fromarray(a));out=crop(out)
 return out
def size(im,w,h=None):return im.resize((round(w),round(h or im.height*w/im.width)),Image.Resampling.LANCZOS)
def put(base,im,x,y,w=None,h=None):
 if w:im=size(im,w,h)
 base.alpha_composite(im,(round(x),round(y)));return base

def mask(im,pts,keep=True):
 m=Image.new('L',im.size,0 if keep else 255);ImageDraw.Draw(m).polygon(pts,fill=255 if keep else 0)
 im=im.copy();im.putalpha(ImageChops.multiply(im.getchannel('A'),m));return im

def save(n,im,identity=None):
 im.save(OUT/f'{n}.png')
 if identity:items[identity]=PREFIX+n+'.png'
 return im

def item(key,im,n=None):return save(n or re.sub('[^a-z0-9]+','-',key.split(':',1)[1].lower()).strip('-'),im,key)
def slot(owner,accepted,n,im):save(n,im);slots.setdefault(owner,{})[accepted]=PREFIX+n+'.png'
def ext(n,c,r,w,nc=4,nr=3,h=None):return size(tile(n,c,r,nc,nr),w,h)
def combo(*ims):
 out=ims[0].copy()
 for im in ims[1:]:out.alpha_composite(im)
 return out

# Intestinal tissue family. Three cores/capillary loops retain the same geometry.
lining=ext('intestine',0,0,650);cores=ext('intestine',1,0,650);caps=ext('intestine',2,0,540);vein=ext('intestine',3,0,420)
fold=ext('intestine',0,1,700)
item('name:Thin intestinal lining',lining);item('name:Fingerlike intestinal folds',cores)
item('name:Intestinal capillaries',caps);item('name:Vein from intestine to liver',vein)
foldcanvas=put(canvas(800,800),fold,50,20,700,650)
caplayer=put(canvas(800,800),caps,115,95,570,570)
veinlayer=put(canvas(800,800),vein,180,610,440,170)
item('name:Folded absorbing lining',foldcanvas)
item('name:Blood route from the intestine',crop(combo(caplayer,veinlayer)))
item('name:Lining with intestinal capillaries',combo(foldcanvas,caplayer))
absorbing=item('name:Intestinal absorbing surface',combo(foldcanvas,caplayer,veinlayer))

# Cells and physically stored carbohydrate, rather than organ-purpose emblems.
metab=[('name:Liver cells',0,0,400),('name:Liver carbohydrate store',1,0,400),('id:meal-insulin-cells',2,0,390),('id:meal-glucagon-cells',3,0,390),('name:Insulin in blood',0,1,300),('name:Glucagon in blood',1,1,300),('name:Muscle fibres beside a blood vessel',2,1,520),('name:Muscle carbohydrate store',3,1,520),('id:meal-released-glucose',0,2,260),('name:Small fatty acids and gas',1,2,290)]
for key,c,r,w in metab:item(key,ext('metabolism',c,r,w))
hotspots['20']={'id:meal-insulin-cells':{'center':[400,750]},'id:meal-glucagon-cells':{'center':[1160,750]}}

# Colon wall layers share a common physical sectional registration.
cl=ext('intestine',2,1,650,h=280);muc=ext('intestine',3,1,650,h=70)
cs=ext('intestine',0,2,650,h=200);cm=ext('intestine',1,2,650,h=180)
for key,im in [('Colon lining',cl),('Colon mucus',muc),('Colon supporting tissue and vessels',cs),('Colon muscle wall',cm)]:item('name:'+key,im)
clin=put(canvas(750,600),cl,50,50);cmuc=put(canvas(750,600),muc,50,25);csup=put(canvas(750,600),cs,50,300)
item('name:Mucus-covered colon lining',crop(combo(clin,cmuc)))
item('name:Colon lining with supporting tissue',crop(combo(clin,csup)))
item('name:Colon inner wall',crop(combo(clin,csup,cmuc)))
item('name:Wet food remainder',ext('intestine',2,2,280));item('name:Resident gut microbes',ext('intestine',3,2,320))
upper=tile('gut-organs',0,0,2,1);colon=tile('gut-organs',1,0,2,1)
# The colon surrounds the small intestine, below the original liver and stomach.
gutbase=put(canvas(950,1380),upper,130,10,690,1210)
gutcolon=put(canvas(950,1380),colon,65,660,820,690)
gut=item('name:Digestive tract',combo(gutbase,gutcolon))
item('name:Upper digestive tract',gutbase);item('name:Colon',size(colon,650))

# Registered paired kidneys, ureters and bladder. Liquids have no anatomical badge.
kidneys=ext('urinary',0,0,650,4,2);ureters=tile('urinary',1,0,4,2);bladder=tile('urinary',2,0,4,2)
urobase=put(canvas(760,1110),kidneys,55,10,650,485)
ur=source('urinary')
lefttube=crop(ur,(480,0,590,510));righttube=crop(ur,(590,0,690,510))
ul=put(put(canvas(760,1110),lefttube,290,358,60,480),righttube,395,358,60,480)
bl=put(canvas(760,1110),bladder,247,800,266,300)
item('name:Urinary system',urobase)
item('name:Ureters',crop(ul));item('name:Bladder',size(bladder,266,300))
slot('name:Urinary system','name:Ureters','urinary-ureters-fitted',ul);slot('name:Urinary system','name:Bladder','urinary-bladder-fitted',bl)
ucomplete=save('urinary-complete',combo(urobase,ul,bl))
item('name:Kidney filter',ext('urinary',3,0,530,4,2))
item('name:Kidney recovery tube',ext('urinary',0,1,500,4,2))
item('name:Filtered kidney fluid',ext('urinary',1,1,260,4,2))
item('name:Urine',ext('urinary',2,1,245,4,2));item('name:Concentrated urine',ext('urinary',3,1,210,4,2))
item('name:Drinking water',ext('renewal',1,0,260,2,2))
# One continuous gut-wall specimen, with physical capillaries inside its villi.
item('id:water-gut-capillary',size(absorbing,650))
hotspots['22']={'name:Kidney filter':{'center':[370,1180]},'name:Kidney recovery tube':{'center':[1160,1170]}}
hotspots['23']={'name:Urinary system':{'center':[430,900]},'id:water-gut-capillary':{'center':[1160,1050],'hitbox':{'center':[1135,1130],'size':[300,240]}}}
placements['name:Urinary system']=[780,650]

# Skin construction: all constituent dimensions anticipate a common 720px section.
outer=ext('skinparts',0,0,720,h=160);lipids=ext('skinparts',1,0,720,h=30)
tissue=ext('skinparts',2,0,720,h=320);vessels=ext('skinparts',3,0,680,h=220)
coil=ext('skinparts',0,1,100,h=95);duct=ext('skinparts',1,1,28,h=360);nerves=ext('skinparts',2,1,260,h=250)
for key,im in [('Outer skin cells',outer),('Lipids between skin cells',lipids),('Supporting skin tissue',tissue),('Skin blood vessels',vessels),('Sweat gland coil',coil),('Sweat gland duct',duct),('Skin nerve endings',nerves)]:item('name:'+key,im)
outerlayer=put(canvas(),outer,90,70);lipidlayer=put(canvas(),lipids,90,77)
surface=combo(outerlayer,lipidlayer)
tissuelayer=put(canvas(),tissue,90,200);vessellayer=put(canvas(),vessels,110,310)
glandlayer=put(put(canvas(),coil,135,410),duct,172,75)
nervelayer=put(canvas(),nerves,545,245)
base=combo(tissuelayer,surface,vessellayer)
item('name:Water-resistant skin surface',crop(surface));item('name:Living deeper skin',crop(combo(tissuelayer,vessellayer)))
item('name:Skin layers awaiting blood vessels',combo(tissuelayer,surface));item('name:Skin segment',base)
item('name:Sweat gland and duct',crop(glandlayer))
slot('name:Skin segment','name:Sweat gland and duct','skin-gland-fitted',glandlayer)
slot('name:Skin segment','name:Skin nerve endings','skin-nerves-fitted',nervelayer)
complete=save('skin-completed',combo(base,glandlayer,nervelayer))
# Remove only a narrow central cut; preserve every surrounding source pixel.
gap=[(440,65),(480,65),(472,160),(485,230),(470,295),(481,390),(440,390),(445,300),(433,225),(444,150)]
cutclean=mask(complete,gap,False)
# Broken pieces of the same epidermal cells occupy the open cut before clearance.
debris=size(crop(outer,(260,110,310,153)),24,22)
cut=put(put(cutclean.copy(),debris,444,260),debris.rotate(25,expand=True),446,305)
platelets=ext('skinparts',0,2,95,h=65);threads=ext('skinparts',3,2,115,h=80)
plug=put(cut.copy(),platelets,413,358);clot=put(plug.copy(),threads,405,350)
item('name:Skin with a cut',cut);item('name:Skin with a platelet plug',plug);item('name:Skin with a reinforced clot',clot)
item('name:Rough edge',ext('repair',0,0,320));item('name:Platelets at the cut',platelets)
item('name:Dissolved clotting protein',ext('skinparts',1,2,220));item('name:Clotting enzymes',ext('skinparts',2,2,230));item('name:Clotting protein threads',threads)
hotspots['25']={'name:Rough edge':{'center':[1170,700]}}
white=ext('repair',1,0,260);cap=ext('repair',2,0,340);sprout=ext('repair',3,0,340)
item('name:Debris-clearing white blood cells',white);item('name:Nearby capillary',cap);item('name:Capillary sprout',sprout)
item('name:Protein messengers from the wound',ext('repair',0,1,210));item('name:Support-building skin cells',ext('repair',1,1,300))
item('id:school-repair-protein-blocks',ext('metabolism',3,2,240));item('id:school-repair-fuel',ext('metabolism',2,2,260))
newcells=ext('repair',2,1,200);fibres=ext('repair',3,1,260)
item('name:Skin cells at the cut\'s edge',crop(outer,(270,50,450,160)))
item('name:New skin cells',newcells);item('name:New supporting protein fibres',fibres)
item('name:Clot-clearing enzymes',ext('repair',0,1,210))
cleared=put(put(cutclean.copy(),platelets,413,358),threads,405,350)
cleared=put(cleared,white,490,250,60,65);item('name:Skin with a cleared wound',cleared)
# Fittings occupy the original cut, not detached detail panels.
cellsfit=mask(outerlayer,[(425,60),(490,60),(490,235),(425,235)])
fibrefit=put(canvas(),size(fibres,65,145),430,220)
sproutfit=put(canvas(),sprout,410,310,105,85)
slot('name:Skin with a cleared wound','name:Capillary sprout','wound-sprout-fitted',sproutfit)
slot('name:Skin with a cleared wound','name:New skin cells','wound-cells-fitted',cellsfit)
slot('name:Skin with a cleared wound','name:New supporting protein fibres','wound-fibres-fitted',fibrefit)
repaired=combo(complete,fibrefit);item('name:Repaired skin segment',repaired)

# Renewal: physical cell populations and materials only.
for key,c,r,w in [('id:rf-worn-red-cells',0,2,300),('id:rf-spleen-recyclers',1,2,360),('id:rf-recovered-iron',2,2,260),('id:rf-blood-forming-marrow',3,2,500)]:item(key,ext('repair',c,r,w))
item('id:rf-new-red-cells',ext('renewal',0,0,300,2,2))
item('id:rf-skin-base',ext('renewal',0,1,600,2,2));item('id:rf-new-skin-cells',ext('renewal',1,1,600,2,2));item('id:rf-skin-materials',ext('metabolism',2,2,260))

# Finale lower region: same completed gut and kidneys at regional-model scale.
lower=tile('body-regions',0,0,2,1)
lowerbase=put(canvas(760,1520),lower,110,0,540,1500)
lowergut=put(canvas(760,1520),gut,215,-135,330,490)
loweruro=put(canvas(760,1520),ucomplete,255,105,250,365)
item('name:Lower body',lowerbase)
slot('name:Lower body','id:final-urinary-organs','lower-urinary-fitted',loweruro)
slot('name:Lower body','name:Digestive tract','lower-gut-fitted',lowergut)
item('id:final-urinary-organs',size(ucomplete,270))
lowcomplete=save('lower-complete',combo(lowerbase,loweruro,lowergut))
# Loose supplies return at the same scale as their fitted appearances.
presentations['name:Digestive tract']=[{'chapter':'full-assembly-regions','path':PREFIX+'gut-finale-loose.png'}]
save('gut-finale-loose',size(gut,330,490))
skin=tile('body-regions',1,0,2,1)
skincover=put(canvas(1100,2200),skin,60,0,980,2180)
item('name:Skin covering',skincover)
patchlayer=put(canvas(1100,2200),repaired,211,810,43,31)
slot('name:Skin covering','name:Repaired skin segment','skin-patch-fitted',patchlayer)
finishedskin=save('skin-cover-complete',combo(skincover,patchlayer))
presentations['name:Repaired skin segment']=[{'chapter':'full-assembly-regions','path':PREFIX+'repaired-skin-finale-loose.png'}]
save('repaired-skin-finale-loose',size(repaired,150))

# Shared earlier-chapter constituents are registered by the finale extension.
exec((ROOT/'finale.py').read_text())
items['name:Blood']='atlas/circulation/assets/blood.png'
items['id:meal-released-glucose']='atlas/opening/assets/glucose.png'
mapdata={'itemIcons':items,'slotIcons':slots,'hotspots':hotspots,'placements':placements,'presentations':presentations}
(ROOT/'map.json').write_text(json.dumps(mapdata,indent=2)+'\n')
# Disposable contact sheets and all fitted partial states for visual inspection.
diag=ROOT.parents[3]/'runs'/'anatomy-atlas';diag.mkdir(parents=True,exist_ok=True)
entries=[]
for key,path in items.items():
 p=ROOT.parents[1]/path
 if p.exists():entries.append((key,Image.open(p).convert('RGBA')))
for owner,layers in slots.items():
 basepath=ROOT.parents[1]/items.get(owner,'atlas/opening/assets/nervous-system.png')
 b=Image.open(basepath).convert('RGBA')
 for count in range(1,len(layers)+1):
  for subset in itertools.combinations(layers,count):
   out=b.copy()
   for k in subset:out.alpha_composite(Image.open(ROOT.parents[1]/layers[k]).convert('RGBA'))
   entries.append((owner+' + '+','.join(subset),out))
for start in range(0,len(entries),30):
 page=Image.new('RGBA',(1250,1500),'#f6f1e5');d=ImageDraw.Draw(page)
 for j,(key,im) in enumerate(entries[start:start+30]):
  x=(j%5)*250;y=(j//5)*250;im.thumbnail((230,200));page.alpha_composite(im,(x+(250-im.width)//2,y+5));d.text((x+8,y+211),key[:34],fill='#322d26')
 page.convert('RGB').save(diag/f'body-review-{start//30+1}.jpg')
print(f'{len(items)} identities, {sum(map(len,slots.values()))} fitted layers; {len(entries)} review images')
