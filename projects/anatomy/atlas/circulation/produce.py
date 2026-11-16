"""Mechanical extraction and registration of selected builtin-generated atlas parts.

Requires Pillow and NumPy. No anatomy is drawn by this producer.
Run from repository root: python projects/anatomy/atlas/circulation/produce.py
"""
from pathlib import Path
import json, re
import numpy as np
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
MAP = {'itemIcons': {}, 'slotIcons': {}, 'hotspots': {}, 'placements': {}}
PARTS = {}

def trim(im, pad=8):
    box=im.getchannel('A').getbbox()
    if not box: raise ValueError('Empty extraction')
    return ImageOps.expand(im.crop(box), border=pad, fill=(0,0,0,0))

def sheet(name, cols, names, ys=None):
    im=Image.open(ROOT/'sources'/f'{name}.png').convert('RGBA')
    w,h=im.size; rows=len(names)//cols
    ys=ys or [round(h*i/rows) for i in range(rows+1)]
    for i,n in enumerate(names):
        c=i%cols; r=i//cols
        p=im.crop((round(w*c/cols),ys[r],round(w*(c+1)/cols),ys[r+1]))
        a=np.array(p); a[a[:,:,3]<24]=0
        PARTS[n]=trim(Image.fromarray(a))

def sized(im, width=None, height=None):
    if isinstance(im,str): im=PARTS[im]
    if width is not None: height=round(im.height*width/im.width)
    else: width=round(im.width*height/im.height)
    return im.resize((int(width),int(height)),Image.Resampling.LANCZOS)

def canvas(size, layers):
    im=Image.new('RGBA',size)
    for part,x,y,w in layers:
        p=sized(part,width=w) if w else (PARTS[part] if isinstance(part,str) else part)
        im.alpha_composite(p,(round(x),round(y)))
    return im

def merge(base, *layers):
    return canvas(base.size,[(base,0,0,None),*layers])

def emit(name, im, width=None, keep=False, key=True):
    if isinstance(im,str): im=PARTS[im]
    if not keep: im=trim(im)
    if width: im=sized(im,width=width)
    slug=re.sub('[^a-z0-9]+','-',name.lower()).strip('-')
    im.save(OUT/f'{slug}.png')
    PARTS[name]=im
    path=f'atlas/circulation/assets/{slug}.png'
    if key: MAP['itemIcons']['name:'+name]=path
    return im

sheet('blood-immune',4,['young','red','plasmaliquid','whiteplatelets','water','solutes','iron','oxygen','resting','active','memory','antibody'],[0,365,695,1086])
sheet('vessels',3,['arterywall','lining','veinwall','capillary','tissue','valves','pulmonary','coronaryartery','coronaryvein'],[0,345,625,1024])
sheet('chest',3,['ribs','intercostal','diaphragm','lungmacro','heart','systemic'],[0,470,1024])
sheet('micro',4,['alveoli','alveolicap','elastic','trachea','bronchi','epithelium','mucus','dust','macrophage','bacteria','node','lymph'],[0,365,715,1086])
sheet('balance-clean',3,['loops','turncells','crystals','tiltcells','sacs','gel'])
sheet('immune-clean',3,['amino','fragments','activeclean'])
# Reject a remnant from the preceding sheet cell above the capillary mesh.
PARTS['capillary']=trim(PARTS['capillary'].crop((0,22,PARTS['capillary'].width,PARTS['capillary'].height)))
# The generated blood sheet has deliberately wide specimens with irregular
# gutters. Use specimen-specific extraction rather than cutting their edges.
bloodmaster=Image.open(ROOT/'sources'/'blood-immune.png').convert('RGBA')
for name,box in {
    'young':(0,0,332,355),'red':(340,0,710,355),
    'plasmaliquid':(715,55,1067,338),'whiteplatelets':(1070,0,1448,365),
    'water':(0,385,345,660),'solutes':(355,375,710,685),
    'iron':(720,375,1070,685),'oxygen':(1090,375,1448,685),
    'resting':(0,690,317,1030),'active':(325,690,687,1040),
    'memory':(675,690,1090,1045),'antibody':(1095,690,1448,1045)
}.items():
    p=np.array(bloodmaster.crop(box));p[p[:,:,3]<24]=0
    PARTS[name]=trim(Image.fromarray(p))
# Remove the pale tissue backing of the coronary venous source; preserve its
# real blue-violet vessels instead of introducing a ghost second heart.
cv=np.array(PARTS['coronaryvein']); rgb=cv[:,:,:3].astype(int)
cv[:,:,3]=np.where((rgb[:,:,2]-rgb[:,:,0]>2)&(rgb[:,:,0]<180),cv[:,:,3],0)
PARTS['coronaryvein']=trim(Image.fromarray(cv))

# Balance: same loop master and real fitted sensory patches throughout.
loops=sized('loops',width=760)
emit('Fluid-filled loops',loops)
emit('Turning sensor cells','turncells',width=300)
emit('Tiny mineral weights','crystals',width=260)
tilt=canvas((430,350),[('gel',40,70,340),('tiltcells',20,40,390)])
emit('Tilt sensor cells',tilt)
weighted=merge(tilt,('crystals',80,20,250))
emit('Weighted balance sensors',weighted)
turn=merge(loops,('turncells',440,245,100),('turncells',290,380,95),('turncells',435,525,90))
emit('Turn-sensing canals',turn)
balance=merge(turn,(weighted,465,520,205))
emit('Balance organs',balance)

# Blood specimens retain the same liquid and cells; oxygen is small within cells.
emit('Developing red blood cells','young',width=440)
emit('Iron and amino acids','iron',width=300)
red=sized('red',width=440)
emit('Red blood cells',red)
emit('Oxygen molecules','oxygen',width=260)
# Bound oxygen is beneath the resolution of this cell view; retain the literal
# biconcave cells, without fictitious bubbles sitting on their outer surfaces.
redoxy=red.copy()
emit('Red cells carrying oxygen',redoxy)
emit('Plasma water','water',width=760)
emit('Plasma proteins, nutrients and salts','solutes',width=310)
plasma=sized('plasmaliquid',width=900)
plasma=merge(plasma,('solutes',200,170,170),('solutes',550,150,130))
emit('Plasma',plasma)
emit('White cells and platelets','whiteplatelets',width=340)
white=merge(plasma,('whiteplatelets',135,100,260))
rp=merge(plasma,(redoxy,360,110,380))
emit('Plasma with white cells and platelets',white)
emit('Plasma with oxygen-carrying red cells',rp)
blood=merge(white,(redoxy,390,130,380))
emit('Blood',blood)

# Local vessel cutaways and connected exchange bed.
emit('Blood-facing lining cells','lining',width=440)
aw=sized('arterywall',height=700); vw=sized('veinwall',height=700)
emit('Arterial wall',aw); emit('Venous wall',vw)
av=trim(Image.open(ROOT/'sources'/'arterial-lined.png').convert('RGBA')).resize(aw.size,Image.Resampling.LANCZOS)
vv=trim(Image.open(ROOT/'sources'/'venous-lined.png').convert('RGBA')).resize(vw.size,Image.Resampling.LANCZOS)
emit('Arterial vessels',av); emit('Thin-walled veins',vv)
emit('One-way valve flaps','valves',width=300)
vr=merge(vv,('valves',vv.width*.22,350,vv.width*.56))
emit('Venous return',vr)
emit('Tiny capillary tubes','capillary',width=740)
emit('Nearby body cells','tissue',width=590)
bed=canvas((800,650),[('tissue',70,110,650),('capillary',15,135,780)])
emit('Capillary bed',bed)
networksize=(1200,720)
arteryjoined=av.rotate(90,expand=True)
veinjoined=vr.rotate(90,expand=True)
dist=canvas(networksize,[(bed,190,150,810),(arteryjoined,0,440,345)])
back=canvas(networksize,[(bed,190,150,810),(veinjoined,870,335,300)])
network=canvas(networksize,[(bed,190,150,810),(arteryjoined,0,440,345),(veinjoined,870,335,300)])
emit('Distribution and exchange bed',dist)
emit('Capillaries and venous return',back)
emit('Body blood-vessel network',network)

# Heart halves are literal crops of one cutaway, reunited without redrawing.
heart=sized('heart',width=650)
right=heart.copy(); right.paste((0,0,0,0),(330,0,heart.width,heart.height))
left=heart.copy(); left.paste((0,0,0,0),(0,0,330,heart.height))
emit('Right side of heart',right);emit('Left side of heart',left)
emit('Lung blood-vessel network','pulmonary',width=900)
emit('Arteries for the heart muscle','coronaryartery',width=540)
emit('Heart-muscle capillaries and veins','coronaryvein',width=540)
coronary=canvas((600,640),[('coronaryvein',15,10,570),('coronaryartery',20,10,560)])
emit('Heart-muscle vessel network',coronary)
hsize=(1200,1800)
# Register the pump within the thorax of the actual body-scale vascular tree.
# The pulmonary roots face the heart, and overlap its attached vessel stumps.
pulmonaryjoined=PARTS['pulmonary'].rotate(180,expand=True)
right_route=canvas(hsize,[(pulmonaryjoined,360,25,480),(right,500,180,220)])
left_route=canvas(hsize,[('systemic',40,0,1120),(left,500,180,220)])
two=canvas(hsize,[('systemic',40,0,1120),(pulmonaryjoined,360,25,480),(heart,500,180,220)])
emit('Right heart and lung route',right_route)
emit('Left heart and body route',left_route)
emit('Heart and two routes',two)
complete=merge(two,(coronary,520,225,175))
emit('Heart with connected vessels',complete)
emit('body-vessels-macro','systemic',width=1000,key=False)
MAP['presentations']={'name:Body blood-vessel network':[{
    'chapter':'full-a-pump-with-two-routes',
    'path':'atlas/circulation/assets/body-vessels-macro.png'}]}

# Exchange microstructure is one continuous terminal specimen, never a zoom inset.
alv=sized('alveoli',width=660)
emit('Tiny air sacs',alv)
emit('Lung capillaries','alveolicap',width=640)
emit('Elastic supporting tissue','elastic',width=640)
ac=merge(alv,('alveolicap',10,10,640))
ae=merge(alv,('elastic',10,10,640))
ace=merge(ac,('elastic',10,10,640))
emit('Air sacs with blood vessels',ac)
emit('Elastic air sacs',ae)
emit('Elastic air sacs with blood vessels',ace)
airways=sized(trim(Image.open(ROOT/'sources'/'airway-tree.png').convert('RGBA')),width=1000)
# The isolated airway edit follows the whole-lung master's actual branch layout.
# Separate its central trachea and bronchial tree without altering either part.
cut=(int(airways.width*.42),0,int(airways.width*.57),int(airways.height*.36))
tracheapart=airways.crop(cut)
bronchipart=airways.copy();bronchipart.paste((0,0,0,0),cut)
emit('Windpipe',tracheapart)
emit('Branching air tubes',bronchipart)
emit('Branching airways',airways)
# Macro lung surface is the selected continuous cutaway; internal tissue becomes
# naturally fine at this later anatomical scale, with no detached micrographs.
lungs=sized('lungmacro',width=1000)
emit('Lungs',lungs)

# Chest: full 1200 x 1400 registration shared with the final-body package.
chsize=(1200,1400)
riblayer=canvas(chsize,[('ribs',25,0,1150)])
musclelayer=canvas(chsize,[('intercostal',70,10,1060)])
chbase=canvas(chsize,[(musclelayer,0,0,None),(riblayer,0,0,None)])
diaphragmlayer=canvas(chsize,[('diaphragm',140,730,920)])
organlayer=canvas(chsize,[(lungs,135,100,930),(heart,440,535,380)])
# The spine lies behind the organs. The upper sternum and lateral ribs remain
# in front. This mask only separates generated bone layers; it paints no bone.
ribfront=riblayer.copy()
ribfront.paste((0,0,0,0),(455,465,745,1400))
emit('Rib cage',riblayer,keep=True)
emit('Muscles between the ribs',musclelayer)
emit('Diaphragm',diaphragmlayer)
emit('Heart and lungs',organlayer)
emit('Breathing apparatus',chbase,keep=True)
dp=emit('chest-diaphragm-layer',diaphragmlayer,keep=True,key=False)
op=emit('chest-organs-layer',organlayer,keep=True,key=False)
# Organs must appear behind ribs. Overlay includes existing ribs at their exact
# registration to restore the anterior cutaway edge after the slot is painted.
organoverlay=canvas(chsize,[(organlayer,0,0,None),(ribfront,0,0,None)])
emit('chest-organs-fitted-layer',organoverlay,keep=True,key=False)
MAP['slotIcons']['name:Breathing apparatus']={
    'name:Diaphragm':'atlas/circulation/assets/chest-diaphragm-layer.png',
    'name:Heart and lungs':'atlas/circulation/assets/chest-organs-fitted-layer.png'}
MAP['hotspots']['14']={'name:Breathing apparatus':{'center':[780,1000]}}
emit('chest-front-ribs',ribfront,keep=True,key=False)
emit('chest-complete',canvas(chsize,[(chbase,0,0,None),(diaphragmlayer,0,0,None),(organlayer,0,0,None),(ribfront,0,0,None)]),keep=True,key=False)

# Airway defense: mucus output excludes the preserved living epithelial producer.
emit('Airway mucus','mucus',width=700)
emit('Airway lining with sweeping hairs','epithelium',width=850)
emit('Inhaled particles and bacteria','dust',width=360)
mc=canvas((900,850),[('epithelium',25,190,850),('mucus',60,85,780)])
emit('Mucus-covered airway lining',mc)
mp=canvas((800,500),[('mucus',0,30,780),('dust',210,90,300)])
emit('Mucus with trapped particles',mp)
emit('Lung white blood cells','macrophage',width=540)
emit('Bacteria in a lung air sac','bacteria',width=260)
mac=sized('macrophage',width=600)
inside=merge(mac,('bacteria',290,180,120))
emit('Lung white cells containing bacteria',inside)

# Lymph drainage has actual adjoining tissue and vessels, no limb locator.
emit('Tissue beside blood capillaries',bed)
lymph=sized('lymph',width=700)
emit('Tiny lymph vessels',lymph)
large=trim(lymph.crop((int(lymph.width*.55),0,lymph.width,int(lymph.height*.65))))
emit('Larger lymph vessels',large,width=400)
emit('Neck vein segment',vw,width=240)
tl=canvas((950,850),[(bed,20,180,850),(lymph,180,40,650)])
lr=canvas((950,850),[(large,360,160,400),(vw,620,0,220)])
ln=canvas((950,1000),[(bed,10,370,850),(lymph,180,230,650),(large,360,80,400),(vw,620,0,220)])
emit('Tissue with lymph capillaries',tl)
emit('Lymph return route',lr)
emit('Lymph drainage network',ln)

# Immune components. Contact and containment are shown literally.
bact=PARTS['bacteria']
fragments=PARTS['fragments']
emit('Bacterial fragments with antigens',fragments,width=250)
emit('Resting lymphocytes','resting',width=420)
emit('Living lymph node','node',width=950)
emit('Amino acids','amino',width=300)
emit('Bacteria','bacteria',width=380)
emit('Activated matching lymphocyte','activeclean',width=500)
emit('Antibody-making and memory cells','memory',width=560)
emit('Matching antibodies','antibody',width=320)
coated=sized('bacteria',width=600)
coated=merge(coated,('antibody',30,90,150),('antibody',320,180,150))
emit('Antibody-coated bacteria',coated)
emit('Engulfing white blood cells',mac)
emit('White blood cells containing bacterial remains',merge(mac,(fragments,270,180,130)))
MAP['hotspots']['17']={'name:Living lymph node':{'center':[780,1000]}}

(ROOT/'map.json').write_text(json.dumps(MAP,indent=2)+'\n')
# Inspection sheet is disposable verification output, not a shipped texture.
scratch=Path('runs/anatomy-atlas/circulation'); scratch.mkdir(parents=True,exist_ok=True)
entries=list(MAP['itemIcons'].items()); thumbw,thumbh=270,290
contact=Image.new('RGB',(thumbw*6,thumbh*((len(entries)+5)//6)),(247,243,232))
d=ImageDraw.Draw(contact)
for i,(name,path) in enumerate(entries):
    im=Image.open(ROOT/'assets'/Path(path).name);im.thumbnail((250,245))
    x=(i%6)*thumbw;y=(i//6)*thumbh
    contact.paste(im,(x+(thumbw-im.width)//2,y+10),im)
    d.text((x+8,y+257),name[5:40],fill=(45,35,25))
contact.save(scratch/'contact.jpg')
print(f'Wrote {len(entries)} mapped items, {len(list(OUT.glob("*.png")))} PNGs')
