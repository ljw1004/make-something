"""A 200 mm electric carousel with a vertical belt drive and three real horses.

The motor's 32 mm body/shaft/cradle construction follows the retained wave
machine; its tangent-belt calculation is reused in the horizontal plane. A
separate transparent guard closes before the deck is fitted. The drive remains
accessible from below the removable deck. No speed, torque or safety rating is
implied by the dimensioned geometry.
"""
from pathlib import Path
import math
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from middle.routes import Route
R=Route()
def item(i,n,p,g=None,s=110,e=''):return R.item(i,n,p,g,s,e)
item('ca-base','Base',['base'],'ca-drive',230,e='A broad prepared base with sockets for the bearing, motor and battery. The motor and controller are matching low-voltage modules.')
for p,n in [('spindle','Spindle'),('motor','Motor'),('belt','Belt'),('guard','Guard'),('battery','Battery and dial'),('deck','Deck')]:
    explanations={'spindle':'A vertical spindle and pulley retained inside a bearing block. The square upper end drives the deck; a shoulder supports its hub above the guard.', 'motor':'A small enclosed geared motor, its pulley, retaining strap, mounting foot and plugged lead form one supplied module.', 'guard':'A clear cover with a real shaft opening, cable opening and attached locating feet.', 'battery':'The battery holder, switch and speed dial share one case. Its connected lead plugs into the motor.', 'deck':'A round deck with a central drive socket and three prepared pole sockets.'}
    item('ca-'+p,n,[p],s=170 if p in ('deck','guard') else 115,e=explanations.get(p,''))
start={0:'ca-base',1:'ca-spindle-base',2:'ca-motor-base',3:'ca-drive-base'}
for mask,i in start.items():
    if mask:item(i,'Base',['base']+(['spindle'] if mask&1 else [])+(['motor'] if mask&2 else []),'ca-drive',230)
recipes=[]
for mask,i in start.items():
    for bit,p in [(1,'spindle'),(2,'motor')]:
        if not mask&bit:recipes.append((i,'ca-'+p,start[mask|bit]))
ready={0:'ca-belted',1:'ca-guarded',2:'ca-wired',3:'ca-ready'}
for mask,i in ready.items():item(i,'Base',['base','spindle','motor','belt']+(['guard'] if mask&1 else [])+(['battery'] if mask&2 else []),'ca-drive',230)
recipes.append(('ca-drive-base','ca-belt','ca-belted'))
for mask,i in ready.items():
    for bit,p in [(1,'guard'),(2,'battery')]:
        if not mask&bit:recipes.append((i,'ca-'+p,ready[mask|bit]))
platform=['base','spindle','motor','belt','guard','battery','deck']
item('ca-platform','Carousel',platform,'ca-horses',265)
recipes.append(('ca-ready','ca-deck','ca-platform'))
first=list(R.items)
R.page('c-carousel-drive','A turning deck','ca-platform',first,[('Fit the spindle',['ca-spindle-base','ca-drive-base']),('Fit the motor','ca-drive-base'),('Loop the belt around both pulleys','ca-belted'),('Set the guard over the drive',['ca-guarded','ca-ready']),('Plug in the battery','ca-ready'),('Fit the deck onto the spindle','ca-platform')],recipes)
for j,name in enumerate(('Red horse','Green horse','Cream horse'),1):
    item(f'ca-horse-{j}',name,[f'horse-{j}'],g=f'ca-rider-{j}',s=175,e='A single connected horse with a through socket in its back. Any of the three poles fits it.')
    item(f'ca-pole-{j}','Pole',['pole-1'],s=140,e='A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.')
    item(f'ca-rider-{j}',name,[f'horse-{j}',f'pole-{j}'],f'ca-rider-{j}',175)
mounted={0:'ca-platform'}
for mask in range(1,8):
    mounted[mask]='ca-horses-'+str(mask)
    item(mounted[mask],'Carousel',platform+[p for j in range(1,4) if mask&(1<<(j-1)) for p in (f'horse-{j}',f'pole-{j}')],'ca-horses',265)
item('ca-roofpost','Roof post',['roofpost'],s=150)
item('ca-canopy','Canopy',['canopy'],s=180,e='A small moulded canopy with a centre socket. It sits high enough to leave the horses visible.')
item('ca-posted','Carousel',R.plan[mounted[7]]['parts']+['roofpost'],'ca-roof',290)
item('electric-carousel','Electric carousel',R.plan['ca-posted']['parts']+['canopy'],'ca-finished',345,e='The small motor pulley drives the larger spindle pulley through the belt. All three horses turn with the deck. The roof, poles and horses keep their actual sizes throughout the build.')
recipes=[]
for j in range(1,4):
    recipes += [(f'ca-horse-{j}',f'ca-pole-{p}',f'ca-rider-{j}') for p in range(1,4)]
for mask,i in mounted.items():
    for j in range(1,4):
        bit=1<<(j-1)
        if not mask&bit:recipes.append((i,f'ca-rider-{j}',mounted[mask|bit]))
recipes += [(mounted[7],'ca-roofpost','ca-posted'),('ca-posted','ca-canopy','electric-carousel')]
goals=[]
for j,n in enumerate(('red','green','cream'),1):
    goals += [(f'Fit a pole through the {n} horse',f'ca-rider-{j}'),(f'Fit the {n} horse onto the deck',[mounted[m] for m in mounted if m&(1<<(j-1))])]
goals += [('Fit the roof post','ca-posted'),('Fit the canopy','electric-carousel')]
R.page('c-carousel-horses','Three horses','electric-carousel',[i for i in R.items if i not in first],goals,recipes)
PLAN=R.plan


def belt_path():
    from types import SimpleNamespace
    root=next(p for p in Path(__file__).resolve().parents if (p/'src/story/parser.ts').is_file())
    sys.path.insert(0,str(root/'archive/2026.11.07 builder study/art'))
    from wave_machine import belt_path as original
    dims=SimpleNamespace(motor_y=-.063,motor_z=0,driver_z=0,driver_x=.063,motor_radius=.009,driver_radius=.034)
    return [(y,z,x) for x,y,z in original(dims)]


def build():
    import bpy
    import core
    from mathutils import Vector
    S=core.S;a=core.Assembly('tabletop electric carousel');box=a.box;cyl=a.cylinder
    def bore(o,c,r,l,axis='Z'):S.bore(o,c,r,l,axis)
    def cut_box(obj,c,size):
        cutter=S.box('prepared rectangular receiver',c,size)
        bpy.context.view_layer.objects.active=obj;mod=obj.modifiers.new('actual receiving pocket','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    base=cyl('base','broad round base',(0,0,.0075),.100,.015,'birch')
    # Receiving holes are part of the prepared base, including the spindle bearing.
    for x,y in [(0,0),(-.063,0),(.037,-.063)]:bore(base,(x,y,.0075),.0053 if (x,y)==(0,0) else .0025,.025)
    bearing=box('spindle','retained spindle bearing block',(0,0,.027),(.032,.032,.024),'teal')
    bore(bearing,(0,0,.027),.0033,.035)
    for x in (-.011,.011):
        bore(base,(x,0,.0075),.0018,.030)
        core.bolt(a,'spindle','bearing captive screw',(x,0,.021),.0015,.032)
    rotating=S.empty('deck and spindle rotation about Z');rotating.parent=a.root
    cyl('spindle','driven shaft',(0,0,.0455),.003,.069,'ink',parent=rotating)
    for z in (.013,.041):cyl('spindle','bearing shaft retaining collar',(0,0,z),.005,.003,'ink',parent=rotating)
    box('spindle','square deck drive',(0,0,.082),(.006,.006,.020),'ink',rotating)
    # The hub lands on this shaft shoulder, 2 mm above the guard roof. The
    # 10 mm shoulder still passes through the guard's 11 mm shaft opening.
    cyl('spindle','deck axial seating shoulder',(0,0,.079),.005,.002,'ink',parent=rotating)
    for z,r,th in [(.063,.0333,.005),(.059,.037,.002),(.067,.037,.002)]:cyl('spindle','driven belt pulley',(0,0,z),r,th,'teal',parent=rotating)
    # The wave machine's motor body, concave seat, strap and shaft, rotated to Z.
    cyl('motor','enclosed geared motor',(-.063,0,.036),.016,.040,'ink')
    foot=box('motor','motor mounting foot',(-.063,0,.019),(.043,.042,.008),'teal')
    bore(foot,(-.063,0,.046),.0162,.060)
    for x in (-.080,-.046):
        bore(base,(x,0,.0075),.0018,.030)
        core.bolt(a,'motor','motor captive screw',(x,0,.017),.0015,.026)
    a.line('motor','connected retaining strap',[(-.080,0,.022),(-.081,0,.047),(-.076,0,.056),(-.050,0,.056),(-.045,0,.047),(-.046,0,.022)],.002,'teal')
    motor=S.empty('motor output rotation about Z');motor.parent=a.root;motor.location=(-.063,0,0)
    cyl('motor','motor output shaft',(0,0,.059),.0015,.016,'ink',parent=motor)
    for z,r,th in [(.063,.0083,.005),(.059,.011,.002),(.067,.011,.002)]:cyl('motor','motor pulley',(0,0,z),r,th,'orange',parent=motor)
    a.line('motor','motor plugged lead',[(-.063,-.015,.031),(-.064,-.039,.023),(-.025,-.053,.023)],.0013,'ink')
    socket=box('motor','motor keyed socket',(-.023,-.053,.023),(.010,.012,.008),'teal')
    cut_box(socket,(-.018,-.053,.023),(.0024,.0104,.0074))
    a.line('belt','continuous tangent belt',belt_path(),.0007,'ink')
    glass=core.special_material('carousel clear guard',(.94,.97,1),roughness=.10,transmission=1)
    # One connected open-bottom shell; no fake translucent opaque mechanism.
    walls=[((-.023,0,.077),(.128,.090,.002)),((-.086,0,.0465),(.002,.090,.063)),((.040,0,.0465),(.002,.090,.063)),((-.023,-.044,.0465),(.128,.002,.063)),((-.023,.044,.0465),(.128,.002,.063))]
    for j,(c,s) in enumerate(walls):
        wall=box('guard','clear guard wall',c,s,'paper')
        if j==0:bore(wall,(0,0,.077),.0055,.008)
        if j==3:
            # Open below, so the guard can lower over an already connected lead.
            cutter=S.box('open bottom cable slot',(-.050,-.044,.019),(.013,.010,.020))
            bpy.context.view_layer.objects.active=wall;mod=wall.modifiers.new('cable insertion slot','BOOLEAN');mod.object=cutter;mod.operation='DIFFERENCE';bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
        core.surface(wall,glass)
    for x in (-.080,.034):
        for y in (-.039,.039):
            box('guard','integral locating foot',(x,y,.017),(.008,.008,.010),'teal')
            cut_box(base,(x,y,.014),(.0084,.0084,.0044))
    battery=box('battery','battery and controller case',(.037,-.068,.029),(.071,.041,.028),'battery')
    cyl('battery','speed dial',(.050,-.068,.047),.009,.008,'orange')
    box('battery','power switch',(.018,-.068,.046),(.012,.014,.006),'ink')
    a.line('battery','connected controller lead',[(.0015,-.068,.027),(-.007,-.068,.024),(-.013,-.053,.023)],.0013,'ink')
    box('battery','keyed controller plug',(-.015,-.053,.023),(.008,.010,.007),'orange')
    for x in (.010,.065):
        bore(base,(x,-.068,.0075),.0018,.025)
        core.bolt(a,'battery','case captive screw',(x,-.068,.019),.0015,.014)
    deck=cyl('deck','round rotating deck',(0,0,.096),.090,.010,'birch',parent=rotating)
    # Square through socket provides actual torque coupling to the upper shaft.
    hub=cyl('deck','deck underside drive hub',(0,0,.086),.010,.012,'teal',parent=rotating)
    cutter=S.box('temporary square drive socket',(0,0,.086),(.0063,.0063,.030));cutter.parent=rotating
    bpy.context.view_layer.objects.active=hub;mod=hub.modifiers.new('square drive socket','BOOLEAN');mod.object=cutter;mod.operation='DIFFERENCE';bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    horse_profile=[(-.024,.130),(-.018,.130),(-.014,.145),(.013,.145),(.018,.130),(.024,.130),(.020,.150),(.027,.164),(.022,.174),(.012,.174),(.009,.162),(-.017,.161),(-.026,.154),(-.027,.145)]
    for j,color in enumerate(('orange','teal','paper'),1):
        angle=2*math.pi*(j-1)/3+.35;x=.060*math.cos(angle);y=.060*math.sin(angle)
        unit=S.empty('horse and pole '+str(j));unit.parent=rotating;unit.location=(x,y,0);unit.rotation_euler.z=angle+math.pi/2
        # Drill before parenting so the prepared through-hole is truly vertical.
        horse=S.profile('connected horse silhouette '+str(j),horse_profile,.010,color=color,edge=color)
        bore(horse,(0,0,.155),.0026,.060)
        a.add('horse-'+str(j),horse,unit)
        cyl('pole-'+str(j),'single horse pole',(0,0,.145),.0024,.106,'ink',parent=unit)
        cyl('pole-'+str(j),'horse support collar',(0,0,.143),.004,.004,'teal',parent=unit)
        cyl('pole-'+str(j),'deck locating shoulder',(0,0,.103),.004,.004,'teal',parent=unit)
        bore(deck,(x,y,.096),.0026,.025)
    cyl('roofpost','central roof post',(0,0,.177),.004,.148,'birch',parent=rotating)
    cyl('roofpost','post foot socket',(0,0,.105),.007,.008,'teal',parent=rotating)
    cyl('roofpost','post locating peg',(0,0,.100),.004,.010,'teal',parent=rotating)
    bore(deck,(0,0,.096),.0045,.025)
    # The post's lower socket surrounds the keyed drive, rather than replacing it.
    # A single thin conical shell with an actual central opening.
    n=64;verts=[]
    for dz in (0,-.0015):
        for radius,z in ((.0043,.270),(.052,.246)):
            verts += [(radius*math.cos(2*math.pi*i/n),radius*math.sin(2*math.pi*i/n),z+dz) for i in range(n)]
    faces=[]
    for i in range(n):
        k=(i+1)%n
        faces += [(i,k,n+k,n+i),(2*n+i,3*n+i,3*n+k,2*n+k),(i,2*n+i,2*n+k,k),(n+i,n+k,3*n+k,3*n+i)]
    mesh=bpy.data.meshes.new('thin canopy');mesh.from_pydata(verts,[],faces);mesh.update();roof=bpy.data.objects.new('one conical canopy',mesh);bpy.context.collection.objects.link(roof);roof.data.materials.append(S.material('orange'));a.add('canopy',roof,rotating)
    hub=cyl('canopy','connected canopy socket',(0,0,.257),.007,.028,'teal',parent=rotating);bore(hub,(0,0,.244),.0042,.014)
    model=a.result(rotating=rotating,motor=motor)
    bpy.context.view_layer.update();return model


def set_rotation(model,angle):
    model['rotating'].rotation_euler.z=angle;model['motor'].rotation_euler.z=angle*.034/.009


def stage(model,identity):
    from middle.views import stage_view
    if identity not in PLAN:raise KeyError(identity)
    set_rotation(model,0)
    # Align the view with one horse's broad face. The other two then retain
    # half-width profiles instead of making the red horse almost edge-on.
    return stage_view(model,PLAN,identity,direction=(.77,-.64,.65))


if __name__=='__main__':R.write(__file__)
