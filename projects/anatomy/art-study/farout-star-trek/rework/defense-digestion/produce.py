"""Mechanical extraction/compositing only. Run: uv run --with pillow python produce.py."""
from pathlib import Path
import json, re
from PIL import Image, ImageDraw, ImageChops

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'assets'; OUT.mkdir(exist_ok=True)
PREFIX='rework/defense-digestion/assets/'
mapping={'itemIcons':{},'slotIcons':{},'hotspots':{}}
sources={}
def src(name):
    filename='20-storage-final' if name=='20-storage' else name
    if name not in sources:
        sources[name]=Image.open(ROOT/'sources'/f'{filename}.png').convert('RGBA')
        if name=='20-storage':
            # The molecular edit retained registration but added background
            # alpha; restore the chosen master's exact anatomical matte.
            sources[name].putalpha(Image.open(ROOT/'sources'/'20-storage.png').getchannel('A'))
    return sources[name]
def crop(name,box):
    im=src(name).crop(box)
    # Generated transparency is preserved, including soft object edges.
    bounds=im.getchannel('A').point(lambda a:255 if a>10 else 0).getbbox()
    return im.crop(bounds) if bounds else im
def fit(im,width):
    return im.resize((round(width),round(im.height*width/im.width)),Image.Resampling.LANCZOS)
def save(identity,im,width=None,pad=14):
    if width:im=fit(im,width)
    canvas=Image.new('RGBA',(im.width+pad*2,im.height+pad*2))
    canvas.alpha_composite(im,(pad,pad))
    stem=re.sub(r'[^a-z0-9]+','-',identity.split(':',1)[1].lower()).strip('-')
    canvas.save(OUT/f'{stem}.png')
    mapping['itemIcons'][identity]=PREFIX+stem+'.png'
    return canvas
def item(name,im,width=None):return save('name:'+name,im,width)
def combine(parts,size):
    im=Image.new('RGBA',size)
    for part,pos in parts:im.alpha_composite(part,pos)
    return im
def grid(name,cols,rows,index,box=None):
    im=src(name); w=im.width//cols;h=im.height//rows
    x=index%cols*w;y=index//cols*h
    inspected={
      '16-lymph':[(8,35,493,464),(526,70,998,405),(1020,35,1504,463),(72,517,443,1005),(504,546,991,943),(1003,546,1494,1005)],
      '17-immune':[(20,20,357,328),(388,8,744,329),(788,25,1122,329),(1155,8,1520,333),(10,350,379,640),(422,373,709,622),(778,365,1123,624),(1168,348,1525,648),(8,650,377,1015),(384,651,763,1015),(769,652,1141,1016),(1153,653,1532,1016)],
      '18-food':[(8,30,361,316),(431,30,704,315),(786,48,1100,285),(1132,110,1530,307),(21,375,354,646),(416,402,732,614),(763,352,1119,650),(1130,474,1530,645),(1,751,381,1004),(390,755,758,1004),(768,751,1134,1004),(1199,672,1476,1019)],
      '19-villi':[(12,36,477,432),(517,20,975,435),(1026,15,1522,435),(4,583,439,983),(447,493,951,986),(969,496,1534,994)],
      '20-storage':[(25,20,489,326),(519,22,993,328),(1025,18,1521,328),(8,352,493,649),(510,350,994,651),(1001,427,1520,589),(1,754,500,923),(508,668,994,989),(1019,666,1516,990)]
    }
    if name in inspected:box=inspected[name][index]
    return crop(name,box or (x,y,x+w,y+h))
def masked(name,poly,holes=()):
    im=src(name).copy();m=Image.new('L',im.size);d=ImageDraw.Draw(m);d.polygon(poly,fill=255)
    for hole in holes:d.polygon(hole,fill=0)
    im.putalpha(ImageChops.multiply(im.getchannel('A'),m));return im

# Airway family: shared physical size, layer supplies remain thin.
names15=['Airway mucus','Airway lining with sweeping hairs','Mucus-covered airway lining','Mucus with trapped particles','Inhaled particles and bacteria','Lung white blood cells','Bacteria in a lung air sac','Lung white cells containing bacteria']
for n,i in zip(names15,range(8)):item(n,grid('15-airway',4,2,i))

# Tissue entry and remote neck return retain their distinct scales.
names16=['Tissue beside blood capillaries','Tiny lymph vessels','Tissue with lymph capillaries','Larger lymph vessels','Neck vein segment','Lymph return route']
for n,i in zip(names16,range(6)):item(n,grid('16-lymph',3,2,i),450)
tissue=fit(grid('16-lymph',3,2,2),430)
neck=fit(grid('16-lymph',3,2,5),330)
locator=crop('16-lymph',(506,725,770,936));locator=fit(locator,160)
lymph=combine([(tissue,(10,90)),(neck,(460,30)),(locator,(485,365))],(810,540))
d=ImageDraw.Draw(lymph);d.line([(426,275),(477,300),(545,395)],fill=(129,230,186,210),width=3)
item('Lymph drainage network',lymph)

# Immune population: node is an organ cutaway, not a cell-sized symbol.
immune={'Bacterial fragments with antigens':0,'Resting lymphocytes':1,'Activated matching lymphocyte':2,'Antibody-making and memory cells':3,'Living lymph node':4,'Amino acids':5,'Matching antibodies':6,'Bacteria':7,'Antibody-coated bacteria':8,'Engulfing white blood cells':9,'White blood cells containing bacterial remains':11}
for n,i in immune.items():
    width=800 if n=='Living lymph node' else (100 if n=='Matching antibodies' else None)
    if n in ['Bacteria','Antibody-coated bacteria','Bacterial fragments with antigens']:width=180
    if n in ['Engulfing white blood cells','White blood cells containing bacterial remains']:width=520
    # Reuse the same unlinked amino-acid units as the digestive family.
    picture=grid('18-food',4,3,5) if n=='Amino acids' else grid('17-immune',4,3,i)
    if n=='Matching antibodies':
        picture.putalpha(picture.getchannel('A').point(lambda a:0 if a<200 else a))
        protein_group=fit(picture,100)
        picture=combine([(protein_group,(x*110,y*(protein_group.height+10))) for y in range(2) for x in range(3)],(320,protein_group.height*2+10));width=None
    item(n,picture,width)
mapping['hotspots']['17']={'name:Living lymph node':{'center':[780,900],'icon':mapping['itemIcons']['name:Living lymph node'],'hitbox':{'center':[780,900],'size':[740,580]}}}

# Molecular digestion: repeated rings/beads keep their source-sheet size.
food={'Starchy food':0,'Shorter starch chains':1,'Meal glucose':2,'Saliva':3,'Protein food':4,'Meal amino acids':5,'Digestive enzymes':6,'Bile':7,'Fat food':8,'Small fat droplets':9,'Fat digestion products':10}
locator=fit(grid('18-food',4,3,11),70)
for n,i in food.items():
    part=grid('18-food',4,3,i)
    plate=combine([(part,(0,0)),(locator,(0,part.height+16))],(max(part.width,320),part.height+locator.height+24))
    d=ImageDraw.Draw(plate);d.line([(60,part.height+40),(100,part.height+12),(140,part.height-4)],fill=(122,216,231,200),width=2)
    item(n,plate)

# Villi with supplied cell coat and capillary loops at one scale.
villus={'Fingerlike intestinal folds':0,'Thin intestinal lining':1,'Folded absorbing lining':2,'Intestinal capillaries':3,'Lining with intestinal capillaries':4,'Vein from intestine to liver':5}
for n,i in villus.items():item(n,grid('19-villi',3,2,i),480)
vein=fit(grid('19-villi',3,2,5),260)
for name,index in [('Blood route from the intestine',3),('Intestinal absorbing surface',4)]:
    panel=fit(grid('19-villi',3,2,index),480)
    result=combine([(panel,(0,30)),(vein,(510,0))],(780,max(panel.height+40,vein.height)))
    d=ImageDraw.Draw(result);d.line([(475,panel.height+15),(510,vein.height-25)],fill=(122,216,231,210),width=2)
    item(name,result)

# The stored glucose stays inside the same liver/muscle tissues.
store_names=['Liver cells','Liver carbohydrate store','id:meal-released-glucose','Muscle fibres beside a blood vessel','Muscle carbohydrate store','Insulin in blood','Glucagon in blood','id:meal-insulin-cells','id:meal-glucagon-cells']
for i,n in enumerate(store_names):
    ident=n if n.startswith('id:') else 'name:'+n
    save(ident,grid('20-storage',3,3,i),570 if i>=7 else 450)
mapping['hotspots']['20']={}
for ident,x in [('id:meal-insulin-cells',410),('id:meal-glucagon-cells',1150)]:
    mapping['hotspots']['20'][ident]={'center':[x,920],'icon':mapping['itemIcons'][ident],'hitbox':{'center':[x,920],'size':[590,450]}}

# Colon wall is decomposed from ONE completed slab: exact registered edges,
# cell shapes, layer thicknesses and vessels retained in every partial.
wallbox=(640,265,1520,784)
wall=src('21-organs').crop(wallbox)
def wall_layer(poly):
    m=Image.new('L',wall.size);ImageDraw.Draw(m).polygon(poly,fill=255)
    im=wall.copy();im.putalpha(ImageChops.multiply(im.getchannel('A'),m));return im
mucus=wall_layer([(0,0),(880,0),(880,45),(817,100),(17,95)])
lining=wall_layer([(17,95),(817,100),(880,45),(880,148),(807,200),(15,193)])
support=wall_layer([(15,193),(807,200),(880,148),(880,306),(799,341),(11,333)])
muscle=wall_layer([(11,333),(799,341),(880,306),(880,519),(0,519)])
def wc(*layers):
    result=Image.new('RGBA',wall.size)
    for layer in layers:result.alpha_composite(layer)
    return result
def wall_item(name,*layers):
    # Common canvas and scale preserve layer correspondence without normalizing height.
    item(name,wc(*layers),600)
wall_item('Colon lining',lining)
wall_item('Colon mucus',mucus)
wall_item('Colon supporting tissue and vessels',support)
wall_item('Mucus-covered colon lining',mucus,lining)
wall_item('Colon lining with supporting tissue',lining,support)
wall_item('Colon inner wall',mucus,lining,support)

tract=src('21-organs').crop((0,0,625,1000))
# Generator isolation edits reveal surfaces concealed by the colon while
# retaining the selected master's organ positions and canvas registration.
colon=src('21-colon').crop((0,0,625,1000))
upper=src('21-upper').crop((0,0,625,1000))
item('Upper digestive tract',upper.crop((0,0,625,810)),560)
item('Digestive tract',tract,560)
# Retain exact colon contour in muscle and completed states; wall closeup
# occupies existing empty central space at a clearly enlarged cutaway scale.
for name,detail in [('Colon muscle wall',wc(muscle)),('Colon',wall)]:
    form=colon.copy();small=fit(detail,300);form.alpha_composite(small,(170,550));item(name,form.crop((0,345,625,1000)),560)
for n,i in [('Wet food remainder',0),('Resident gut microbes',1),('Small fatty acids and gas',2)]:item(n,grid('21-microbes',1,3,i),520)

(ROOT/'map.json').write_text(json.dumps(mapping,indent=2)+'\n')
print(f"Wrote {len(mapping['itemIcons'])} identity exports, 3 fixed receivers.")
