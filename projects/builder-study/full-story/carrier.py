"""Compact whale carrier: 400 × 300 mm deck and the unchanged star projector.

The pink tile supplies a controlled fictional force at z=.220, supporting the
load and moving it gently. This is the module's specified impossible function.
Two rigid side arches and the upper cradle carry that force to the deck. Low
batteries and an accessible trim rail keep the assumed centre of mass below it.
No crane, external frame, service hatch or garden infrastructure is an ingredient.
"""
from pathlib import Path
import math
from late.common import Author, geometry, visible, inspection
import projector

PROJECTOR_MOUNT=(-.065,.045,.028)
DRIVEN=(-.065,.086)
DRIVER=(.125,.086)
BELT_Y=-.133
BIG_RADIUS=.023
SMALL_RADIUS=.010
BELT_RADIUS=.001
TILE_HEIGHT=.220
PINWHEEL_MOUNT=(.205,.015,.200)
A=Author()
I=lambda identity,name,parts,group='carrier-loose',css=115,**kw:A.item(identity,name,parts,group,css,**kw)
notes={
    'deck':'A 400 × 300 mm prepared plywood deck. The mounting holes and wire passages are already cut.',
    'arch-a':'One connected rigid arch with two feet and captive bolts.',
    'arch-b':'A second identical connected arch. Either arch fits either side of the deck.',
    'cradle':'One connected top cradle. Four integral saddles clip over the arches; its padded rails receive the tile.',
    'tile':'A flat pink tile with a keyed power socket and retaining holes.',
    'battery':'A compatible enclosed battery in its integral retained bracket. It mounts below the deck, keeping weight low.',
    'control':'A prepared controller and latching stop button in one pod with a connected fused harness. Keep power off while fitting it.',
    'dock':'One connected projector dock. Four feet bear on the deck and two recessed captive screws fasten it down. Four split snap studs pass through the original mounting holes; their flexible heads spring out above the box collars to retain the unchanged projector.',
    'motor':'An enclosed slow gearmotor with its integral pedestal and lead. The shaft is parallel to the projector spindle.',
    'pulley':'One small pulley with a captive screw that clamps onto the motor shaft flat.',
    'belt':'One continuous soft belt. Its small pulley drives the larger grooved handwheel more slowly.',
    'motor-pack':'An enclosed low-voltage motor supply with its own switch, lead and integral mounting bracket. The lamp keeps its original supply.',
    'side-a':'One cut whale side panel with its mounting tabs. Its top edge stays below the projector beam.',
    'side-b':'A second whale side panel, fitted separately.',
    'tail':'One continuous fixed tail with its prepared root fitting.',
    'fin-a':'One fixed fin with two integral mushroom studs and a captive centre screw. The keyhole entries sit below the deck. With the screw retracted, pass the heads through the wide openings and lower the fin into the narrow slots. Tighten the screw to retain it during flips.',
    'fin-b':'The other fixed fin.',
    'skid-a':'One connected landing skid with two upright legs and captive deck bolts.',
    'skid-b':'A second landing skid. Their feet reach below the batteries and trim weight.',
    'rail':'One slotted rail with integral mounting ears, closed travel ends and a wide keyhole entry near the right end. The weight shoe enters through that opening from below.',
    'weight':'A single sliding weight with a captive shoe, vertical clamp screw and washer. Raise the shoe through the wide rail entry, slide into the narrow track, then tighten the screw to clamp the rail between shoe and pad.',
    'guard':'One hollow clear hood, open underneath and at the rear. Lower it over the drive, then tighten the captive screws on its exposed side feet. It encloses the belt and hand grip without covering the lens.',
    'cargo':'A connected socket and open saddle. The open saddle sits over the arch and a captive side screw clamps it; the deep socket receives the wooden pinwheel handle. Soft side pads hold the handle by friction, with a small clearance above the socket floor.',
}
names={'deck':'Deck','arch-a':'Arch','arch-b':'Arch','cradle':'Tile cradle','tile':'Tile','battery':'Battery pack',
       'control':'Control','dock':'Projector dock','motor':'Gearmotor','pulley':'Small pulley','belt':'Belt',
       'motor-pack':'Battery pack','side-a':'Front side','side-b':'Back side','tail':'Tail','fin-a':'Front fin','fin-b':'Back fin',
       'skid-a':'Landing skid','skid-b':'Landing skid','rail':'Weight rail','weight':'Counterweight','guard':'Guard','cargo':'Clip'}
for key in names:
    I('fc-'+key,names[key],[key],group='carrier-work' if key=='deck' else 'carrier-loose',css=230 if key=='deck' else 125,note=notes[key])
# Present fittings in the exposed face's orientation before they are dragged.
for key in ('battery','motor-pack','skid-a','skid-b','rail','weight'):
    A.plan['fc-'+key]['upside']=True
for key in ('side-b','fin-b'):
    A.plan['fc-'+key]['rear']=True
# The two literal arches are interchangeable; whichever is fitted first occupies
# the near mounting pair. Each supply still contributes exactly one rigid arch.
I('fc-one-arch','Frame',['deck','arch-a'],'carrier-work',230)
I('fc-arches','Frame',['deck','arch-a','arch-b'],'carrier-work',230)
for side in ('a','b'):
    A.add('fc-arch-'+side,'fc-deck','fc-one-arch')
    A.add('fc-arch-'+side,'fc-one-arch','fc-arches')
def transition(identity,owner,supply,parts,group='carrier-work',css=230,name='Frame',**kw):
    I(identity,name,parts,group,css,**kw);A.add(supply,owner,identity);return parts
frame=transition('fc-top','fc-arches','fc-cradle',['deck','arch-a','arch-b','cradle'])
frame=transition('fc-tiled','fc-top','fc-tile',frame+['tile'])
I('fc-inverted','Frame',frame,'carrier-under',230,upside=True)
A.process('fc-tiled','fc-flip-lift','fc-inverted')
frame=transition('fc-powered','fc-inverted','fc-battery',frame+['battery'],'carrier-under',upside=True)
# Controller is accessible from above, and its supply is still disconnected.
I('fc-upright','Frame',frame,'carrier-work',230)
A.process('fc-powered','fc-flip-lift','fc-upright')
frame=transition('fc-lift-frame','fc-upright','fc-control',frame+['control'])

projector_parts=['projector:'+key for key in projector.PLAN['star-projector']['parts']]
I('fc-projector-carried','Star projector',projector_parts,'carrier-projector',180,image='fc-projector-carried')
frame=transition('fc-docked','fc-lift-frame','fc-dock',frame+['dock'])
frame=transition('fc-projector-aboard','fc-docked','star-projector',frame+projector_parts)
I('fc-drive','Drive motor',['motor','pulley'],'carrier-drive',175)
A.add('fc-pulley','fc-motor','fc-drive')
frame=transition('fc-motor-mounted','fc-projector-aboard','fc-drive',frame+['motor','pulley'])
frame=transition('fc-belted','fc-motor-mounted','fc-belt',frame+['belt'])
I('fc-drive-under','Frame',frame,'carrier-under',230,upside=True)
A.process('fc-belted','fc-flip-drive','fc-drive-under')
frame=transition('fc-supply-under','fc-drive-under','fc-motor-pack',frame+['motor-pack'],'carrier-under',upside=True)
I('fc-powered-show','Frame',frame,'carrier-work',230)
A.process('fc-supply-under','fc-flip-drive','fc-powered-show')

shell_base=list(frame)
# Opposite faces are exposed explicitly. The handed panels and fins have short
# distinct labels, so the instruction does not ask for an invisible identity.
frame=transition('fc-tailed','fc-powered-show','fc-tail',shell_base+['tail'],name='Whale')
frame=transition('fc-near-side','fc-tailed','fc-side-a',frame+['side-a'],name='Whale')
I('fc-side-rear','Whale',frame,'carrier-rear',230,rear=True)
A.process('fc-near-side','fc-flip-shell','fc-side-rear')
frame=transition('fc-sided','fc-side-rear','fc-side-b',frame+['side-b'],'carrier-rear',rear=True,name='Whale')
frame=transition('fc-one-fin-b','fc-sided','fc-fin-b',frame+['fin-b'],'carrier-rear',rear=True,name='Whale')
I('fc-fin-front','Whale',frame,'carrier-work',230)
A.process('fc-one-fin-b','fc-flip-shell','fc-fin-front')
frame=transition('fc-whale','fc-fin-front','fc-fin-a',frame+['fin-a'],name='Whale')

I('fc-whale-under','Whale',frame,'carrier-under',230,upside=True)
A.process('fc-whale','fc-flip-feet','fc-whale-under')
for side in ('a','b'):
    I('fc-one-skid-'+side,'Whale',frame+['skid-'+side],'carrier-under',230,upside=True)
    A.add('fc-skid-'+side,'fc-whale-under','fc-one-skid-'+side)
    A.add('fc-skid-'+('b' if side=='a' else 'a'),'fc-one-skid-'+side,'fc-skids')
frame+=['skid-a','skid-b'];I('fc-skids','Whale',frame,'carrier-under',230,upside=True)
frame=transition('fc-railed','fc-skids','fc-rail',frame+['rail'],'carrier-under',upside=True,name='Whale')
frame=transition('fc-weighted','fc-railed','fc-weight',frame+['weight'],'carrier-under',upside=True,name='Whale')
I('fc-standing','Whale',frame,'carrier-work',230)
A.process('fc-weighted','fc-flip-feet','fc-standing')
frame=transition('fc-guarded','fc-standing','fc-guard',frame+['guard'],'carrier-work',230,name='Whale',
                 note='The sliding weight balances a heavier end. Adjust it with the machine resting on its skids and the power off.')
frame=transition('fc-clipped','fc-guarded','fc-cargo',frame+['cargo'],'carrier-cargo',290,name='Whale')
pinwheel_parts=['pinwheel:'+key for key in ('pw-paper','pw-hub','pw-axle','pw-handle')]
I('fc-pinwheel-carried','Pinwheel',pinwheel_parts,'carrier-pinwheel',175)
I('fc-cargo-ready','Whale',A.plan['fc-guarded']['parts'],'carrier-cargo',290)
frame=transition('flying-whale','fc-clipped','pinwheel',frame+pinwheel_parts,'carrier-finished',350,name='Whale')

A.page('c-lift-frame','A wide frame','fc-lift-frame',
       ['fc-deck','fc-arch-a','fc-arch-b','fc-cradle','fc-tile','fc-battery','fc-control'],
       ['fc-one-arch','fc-arches','fc-top','fc-tiled','fc-inverted','fc-powered','fc-upright','fc-lift-frame'],
       [('Fit an arch to the deck','fc-one-arch'),('Fit the second arch','fc-arches'),
        ('Clip the cradle across the arches','fc-top'),('Seat the Tile','fc-tiled'),
        ('Flip the frame over','fc-inverted'),('Fit the battery underneath','fc-powered'),
        ('Flip the frame upright','fc-upright'),('Fit the Control','fc-lift-frame')],
       [('fc-flip-lift','Flip','flip')])
A.page('c-lift-projector','Stars aboard','fc-powered-show',
       ['fc-dock','fc-motor','fc-pulley','fc-belt','fc-motor-pack'],
       ['fc-docked','fc-projector-aboard','fc-drive','fc-motor-mounted','fc-belted','fc-drive-under','fc-supply-under','fc-powered-show'],
       [('Fit the projector dock','fc-docked'),('Press your projector onto the dock','fc-projector-aboard'),
        ('Fit the small pulley to the motor','fc-drive'),('Mount the drive motor','fc-motor-mounted'),
        ('Loop the belt around both pulleys','fc-belted'),('Flip to the underside','fc-drive-under'),
        ('Fit the Battery pack','fc-supply-under'),('Flip the Frame upright','fc-powered-show')],
       [('fc-flip-drive','Flip','flip')])
A.page('c-whale-shape','A whale takes shape','fc-whale',
       ['fc-tail','fc-side-a','fc-side-b','fc-fin-a','fc-fin-b'],
       ['fc-tailed','fc-near-side','fc-side-rear','fc-sided','fc-one-fin-b','fc-fin-front','fc-whale'],
       [('Fit the Tail','fc-tailed'),('Fit the Front side','fc-near-side'),('Turn to the back','fc-side-rear'),
        ('Fit the Back side','fc-sided'),('Fit the Back fin','fc-one-fin-b'),
        ('Turn to the front','fc-fin-front'),('Fit the Front fin','fc-whale')],
       [('fc-flip-shell','Flip','flip')])
A.page('c-whale-finish','Landing feet','fc-guarded',
       ['fc-skid-a','fc-skid-b','fc-rail','fc-weight','fc-guard'],
       ['fc-whale-under','fc-one-skid-a','fc-one-skid-b','fc-skids','fc-railed','fc-weighted','fc-standing','fc-guarded'],
       [('Flip the whale over','fc-whale-under'),('Fit a landing skid',['fc-one-skid-a','fc-one-skid-b','fc-skids']),('Fit the other skid','fc-skids'),
        ('Fit the weight rail','fc-railed'),('Fit the weight through the wide slot','fc-weighted'),
        ('Flip the whale upright','fc-standing'),('Fit the clear drive guard','fc-guarded')],
       [('fc-flip-feet','Flip','flip')])
A.page('c-whale-cargo','One more thing','flying-whale',['fc-cargo'],['fc-clipped','flying-whale'],
       [('Fit the Clip onto the arch','fc-clipped'),('Slide the Pinwheel into the Clip','flying-whale')])
PLAN=A.plan


def belt_points(samples=64):
    """Open belt on external tangents, in the real parallel-shaft plane."""
    x1,z1=DRIVEN;x2,z2=DRIVER;distance=x2-x1
    big=BIG_RADIUS+BELT_RADIUS;small=SMALL_RADIUS+BELT_RADIUS
    angle=math.acos((big-small)/distance)
    points=[]
    for cx,cz,r,start,end in [(x1,z1,big,angle,2*math.pi-angle),
                             (x2,z2,small,2*math.pi-angle,2*math.pi+angle)]:
        for i in range(samples+1):
            t=start+(end-start)*i/samples
            points.append((cx+r*math.cos(t),BELT_Y,cz+r*math.sin(t)))
    return points+[points[0]]


def build():
    import bpy
    from construction import Assembly, special_material
    S=geometry();a=Assembly('compact 400 by 300 whale carrier')
    def box(key,name,c,size,col='birch'):return a.box(key,name,c,size,col)
    def cyl(key,name,c,r,l,col='ink',axis='Z'):return a.cylinder(key,name,c,r,l,col,axis)
    def rod(key,name,start,end,r,col='birch'):return a.add(key,S.rod(name,start,end,r,col))
    def bore(obj,c,r,l,axis='Z'):S.bore(obj,c,r,l,axis)
    def cut(obj,centre,size):
        cutter=S.box('temporary prepared opening',centre,size)
        bpy.context.view_layer.objects.active=obj
        modifier=obj.modifiers.new('real opening','BOOLEAN');modifier.operation='DIFFERENCE';modifier.object=cutter
        bpy.ops.object.modifier_apply(modifier=modifier.name);bpy.data.objects.remove(cutter,do_unlink=True)
    def bolt(key,x,y,z,length=.014):
        cyl(key,'captive bolt shank',(x,y,z),.0015,length)
        cyl(key,'captive bolt head',(x,y,z+length/2),.003,.002,'teal')
    def underside_screw(key,x,y,bottom=-.008):
        # A captive screw enters a small prepared pilot hole from below. Its
        # head bears on the exterior fixture face, never inside the deck.
        top=.006;length=top-bottom
        cyl(key,'underside captive screw',(x,y,(top+bottom)/2),.0015,length,'ink','Z')
        cyl(key,'underside screw bearing head',(x,y,bottom-.0015),.003,.003,'teal','Z')
    deck=box('deck','prepared 400 by 300 deck',(0,0,.004),(.400,.300,.008))
    cut(deck,(.160,.020,.004),(.018,.024,.020))
    for side,x in [('a',-.175),('b',.175)]:
        key='arch-'+side
        for y in [-.120,.120]:
            foot=box(key,'arch integral foot',(x,y,.010),(.022,.028,.004),'teal')
            bore(deck,(x,y,.004),.0018,.030);bolt(key,x,y,.006)
            rod(key,'rigid arch upright',(x,y,.012),(x,y,.200),.004)
        rod(key,'rigid arch crossbar',(x,-.120,.200),(x,.120,.200),.004)
    for y in [-.085,.085]:
        box('cradle','tile cradle crossrail',(0,y,.208),(.362,.012,.008),'teal')
        for x in [-.175,.175]:
            clip=S.annulus('integral open arch saddle',(0,0,0),.006,.0042,.014,'teal',gap=1.35)
            # The opening faces down; the arch passes along the Y axis.
            clip.rotation_euler.y=math.pi/2;clip.location=(x,y,.200);a.add('cradle',clip)
    for x in [-.100,.100]:box('cradle','connected cradle side rail',(x,0,.208),(.012,.182,.008),'teal')
    tile=box('tile','pink lift tile',(0,0,TILE_HEIGHT),(.170,.170,.016),'future')
    cut(tile,(.085,.085,TILE_HEIGHT),(.0086,.0086,.0086))
    for x in [-.075,.075]:
        for y in [-.085,.085]:
            sign=1 if y>0 else -1
            box('cradle','integral tile clip upright',(x,sign*.092,.218),(.018,.004,.020),'teal')
            box('cradle','tile retaining lip',(x,sign*.087,.230),(.018,.014,.004),'teal')
    # One supplied battery assembly: case, connected mounting bracket and lead.
    box('battery','low lift battery',(.060,.035,-.025),(.110,.060,.040),'battery')
    flange=box('battery','battery integral mounting flange',(.060,.035,-.004),(.134,.074,.008),'teal')
    for x in [-.001,.121]:
        bore(deck,(x,.035,.004),.0014,.025);bore(flange,(x,.035,-.004),.00165,.020);underside_screw('battery',x,.035)
    a.line('battery','battery attached lead',[(.110,.035,-.020),(.157,.035,-.020),(.160,.020,.014)],.0011,'ink')
    box('battery','battery lead plug',(.160,.020,.014),(.010,.008,.008),'teal')
    box('control','controller and stop pod',(.112,.093,.033),(.074,.060,.040),'teal')
    box('control','controller integral deck foot',(.112,.093,.012),(.084,.070,.008),'teal')
    for x in [.078,.146]:bore(deck,(x,.093,.004),.0018,.025);bolt('control',x,.093,.008)
    cyl('control','lift control dial',(.093,.093,.057),.009,.008,'orange')
    cyl('control','latching stop button',(.132,.093,.060),.010,.014,'orange')
    a.line('control','connected battery input',[(.112,.064,.025),(.150,.064,.025),(.160,.020,.014)],.0011,'ink')
    a.line('control','connected tile harness',[(.145,.093,.038),(.167,.120,.040),(.167,.120,.185),(.167,.110,.195),(.085,.085,.220)],.0011,'ink')
    box('control','tile plug',(.085,.085,.220),(.008,.008,.008),'ink')
    # Four actual feet support the dock 4 mm above the deck. Recessed screws
    # remain accessible before the unchanged projector is pressed onto it.
    dx,dy,dz=PROJECTOR_MOUNT
    dock_fingers=[]
    for x in [dx-.060,dx+.060]:
        crossbar=box('dock','projector dock crossbar',(x,dy,.020),(.014,.108,.016),'teal')
        bore(crossbar,(x,dy,.020),.00165,.040)
        bore(crossbar,(x,dy,.027),.0032,.004)
        bore(deck,(x,dy,.004),.0014,.020)
        cyl('dock','recessed dock deck screw',(x,dy,.013),.0015,.026,'ink','Z')
        cyl('dock','recessed dock screw bearing head',(x,dy,.026),.003,.002,'teal','Z')
        for y in [dy-.045,dy+.045]:
            box('dock','dock load-bearing foot',(x,y,.010),(.014,.014,.004),'teal')
            cyl('dock','projector snap stud fixed base',(x,y,.026),.0028,.004,'teal')
            stem=cyl('dock','projector split snap stud stem',(x,y,.0301),.0028,.0042,'teal')
            bpy.ops.mesh.primitive_cone_add(vertices=64,radius1=.0035,radius2=.0026,depth=.003,location=(x,y,.0337))
            head=a.add('dock',S.finish(bpy.context.object,'projector split retaining head','teal'))
            for obj in [stem,head]:
                bore(obj,(x,y,.032),.0017,.014)
                cut(obj,(x,y,.0328),(.001,.010,.008))
                cut(obj,(x,y,.0328),(.010,.001,.008))
                dock_fingers.append((obj,[v.co.copy() for v in obj.data.vertices]))
    for y in [dy-.050,dy+.050]:box('dock','dock joining rail',(dx,y,.020),(.134,.008,.016),'teal')
    pj=projector.build();pj['root'].parent=a.root;pj['root'].location=PROJECTOR_MOUNT
    for key,objects in pj['parts'].items():
        if key=='blank':continue
        a.parts['projector:'+key]=objects
        for obj in objects:obj['part_id']='projector:'+key
    # Motor bracket fixes shaft height; its small pulley is a separate fitting.
    box('motor','integral motor pedestal',(.125,-.063,.038),(.046,.060,.060),'teal')
    box('motor','motor mounting foot',(.125,-.063,.012),(.064,.080,.008),'teal')
    for x in [.102,.148]:bore(deck,(x,-.063,.004),.0018,.025);bolt('motor',x,-.063,.010)
    cyl('motor','enclosed reduction motor',(.125,-.063,.086),.020,.060,'ink','Y')
    shaft=cyl('motor','flat-sided motor output',(.125,-.119,.086),.003,.052,'ink','Y')
    cut(shaft,(.12925,-.133,.086),(.0037,.018,.012))
    a.line('motor','motor attached lead',[(.125,-.033,.086),(.160,-.020,.060),(.160,.020,.014)],.0010,'ink')
    for y in [BELT_Y-.003,BELT_Y+.003]:
        ob=S.annulus('small pulley retaining flange',(.125,y,.086),.012,.0032,.0015,'orange');a.add('pulley',ob)
    ob=S.annulus('small pulley groove core',(.125,BELT_Y,.086),SMALL_RADIUS,.0032,.006,'orange');a.add('pulley',ob)
    cyl('pulley','pulley captive retaining screw',(.1307,BELT_Y,.086),.001,.0066,'ink','X')
    a.line('belt','continuous external-tangent belt',belt_points(),BELT_RADIUS,'ink')
    box('motor-pack','enclosed motor battery',(-.080,.055,-.025),(.100,.050,.040),'battery')
    flange=box('motor-pack','motor battery connected mounting flange',(-.080,.055,-.004),(.120,.064,.008),'teal')
    for x in [-.132,-.028]:
        bore(deck,(x,.055,.004),.0014,.025);bore(flange,(x,.055,-.004),.00165,.020);underside_screw('motor-pack',x,.055)
    a.line('motor-pack','motor supply attached switched lead',[(-.080,.080,-.020),(-.080,.095,-.020),(.160,.095,-.020),(.160,.020,-.020),(.160,.020,.014)],.001,'ink')
    box('motor-pack','integral motor switch',(-.080,.055,-.046),(.025,.020,.010),'teal')
    cyl('motor-pack','motor switch button',(-.080,.055,-.053),.005,.006,'orange')
    # Panels are connected cut profiles, each with real mounting tabs.
    profile=[(-.205,-.020),(-.190,.010),(-.145,.024),(.140,.024),(.205,-.004),(.170,-.047),(.070,-.067),(-.090,-.067),(-.175,-.052)]
    for side,sign in [('a',-1),('b',1)]:
        key='side-'+side;y=sign*.153
        panel=a.add(key,S.profile('one whale side panel',profile,.004,y,'teal','teal'))
        for x in [-.020,.025]:
            bore(panel,(x,y,-.015),.006,.020,'Y')
            cut(panel,(x,y,-.024),(.0046,.020,.018))
        bore(panel,(.0025,y,-.031),.0014,.020,'Y')
        for x in [-.145,.145]:
            box(key,'side integral deck tab',(x,sign*.146,.012),(.020,.020,.008),'teal')
            bore(deck,(x,sign*.140,.004),.0018,.025);bolt(key,x,sign*.140,.010)
        cyl(key,'whale printed eye',(-.160,y+sign*.0025,-.005),.004,.0008,'ink','Y')
    tail=[(.185,-.015),(.255,-.055),(.295,-.050),(.265,-.005),(.295,.040),(.255,.045),(.185,.015)]
    # Tail is horizontal: native profile lies in XZ and is rigidly turned.
    ob=S.profile('one connected fixed whale tail',tail,.004,0,'orange','orange')
    ob.rotation_euler.x=math.pi/2;ob.location.z=-.015;a.add('tail',ob)
    sleeve=box('tail','tail root connecting sleeve',(.192,0,-.003),(.034,.030,.034),'teal')
    cut(sleeve,(.185,0,.004),(.032,.036,.009))
    for side,sign in [('a',-1),('b',1)]:
        key='fin-'+side
        verts=[(-.035,sign*.158,-.031),(.040,sign*.158,-.031),(.075,sign*.225,-.051),(-.015,sign*.210,-.046)]
        mesh=bpy.data.meshes.new('single fin solid');mesh.from_pydata(verts,[],[(0,1,2,3)]);mesh.update()
        ob=bpy.data.objects.new('one connected fixed fin',mesh);bpy.context.collection.objects.link(ob)
        ob.data.materials.append(S.material('orange'));solid=ob.modifiers.new('actual card thickness','SOLIDIFY');solid.thickness=.003;a.add(key,ob)
        root=box(key,'integral exterior fin root',(.0025,sign*.158,-.031),(.075,.006,.008),'orange')
        bore(root,(.0025,sign*.158,-.031),.00165,.020,'Y')
        for x in [-.020,.025]:
            cyl(key,'fin integral mushroom stem',(x,sign*.154,-.031),.002,.012,'ink','Y')
            cyl(key,'fin integral mushroom head',(x,sign*.1485,-.031),.0055,.003,'teal','Y')
        cyl(key,'fin captive retaining screw',(.0025,sign*.154,-.031),.0015,.016,'ink','Y')
        cyl(key,'fin accessible retaining screw head',(.0025,sign*.162,-.031),.003,.002,'teal','Y')
    for side,y in [('a',-.110),('b',.110)]:
        key='skid-'+side
        box(key,'continuous landing skid',(0,y,-.080),(.340,.018,.012),'birch')
        for x in [-.140,.140]:
            box(key,'skid upright leg',(x,y,-.039),(.016,.018,.070),'teal')
            foot=box(key,'skid deck foot',(x,y,-.004),(.036,.026,.008),'teal')
            screw_x=x+math.copysign(.012,x)
            bore(deck,(screw_x,y,.004),.0014,.026);bore(foot,(screw_x,y,-.004),.00165,.020)
            underside_screw(key,screw_x,y)
    rail=box('rail','one slotted weight rail',(0,-.065,-.025),(.280,.024,.010),'teal')
    cut(rail,(-.009,-.065,-.025),(.282,.008,.018))
    cut(rail,(.100,-.065,-.025),(.019,.018,.018))
    for x in [-.128,.128]:
        ear=box('rail','rail mounting ear',(x,-.042,-.013),(.018,.016,.026),'teal')
        arm=box('rail','rail connected mounting arm',(x,-.051,-.025),(.018,.030,.010),'teal')
        for fixture in [ear,arm]:bore(fixture,(x,-.042,-.015),.00165,.040)
        bore(deck,(x,-.042,.004),.0014,.026);underside_screw('rail',x,-.042,bottom=-.030)
    box('rail','captive rail end stop',(-.135,-.065,-.025),(.010,.024,.012),'orange')
    slider=S.empty('accessible sliding counterweight');slider.parent=a.root
    shoe=S.box('counterweight connected T shoe',(0,-.065,-.0175),(.016,.015,.005),'teal')
    neck=S.box('counterweight T-shoe sliding neck',(0,-.065,-.0295),(.008,.007,.019),'teal')
    weight=S.box('single trim weight',(0,-.065,-.043),(.055,.030,.024),'ink')
    pad=S.box('counterweight rail clamping pad',(0,-.065,-.0305),(.032,.024,.001),'paper')
    for ob in [neck,weight,pad]:bore(ob,(0,-.065,-.038),.00165,.060,'Z')
    # The stem slides in a real pocket; the weight and pad can drop slightly
    # when the captive screw is loosened, then clamp against the rail underside.
    cut(weight,(0,-.065,-.0355),(.0084,.0074,.010))
    cut(pad,(0,-.065,-.0305),(.0084,.0074,.004))
    bore(shoe,(0,-.065,-.0175),.0014,.012,'Z')
    washer=S.cylinder('weight clamp bearing washer',(0,-.065,-.0565),.005,.003,'teal','Z')
    bore(washer,(0,-.065,-.0565),.00165,.010,'Z')
    for ob in [shoe,neck,weight,pad,washer,
               S.cylinder('vertical weight clamp screw',(0,-.065,-.0385),.0015,.045,'ink','Z'),
               S.cylinder('weight clamp finger knob',(0,-.065,-.061),.006,.006,'orange','Z')]:a.add('weight',ob,slider)
    # Open rear shell: the finished rigid hood seats over integral deck lugs.
    guard=box('guard','clear belt guard',(.028,-.139,.087),(.272,.058,.073),'paper')
    cut(guard,(.028,-.134,.082),(.267,.057,.078))
    clear=special_material('clear carrier guard',(.78,.83,.76),roughness=.12,transmission=.75)
    guard.data.materials.clear();guard.data.materials.append(clear)
    for x in [-.102,.157]:box('guard','guard integral deck leg',(x,-.123,.0315),(.012,.014,.047),'teal')
    box('guard','left exposed mounting arm',(-.112,-.123,.012),(.036,.008,.008),'teal')
    box('guard','right forward mounting arm',(.159,-.133,.012),(.006,.026,.008),'teal')
    box('guard','right outward mounting arm',(.171,-.143,.012),(.030,.006,.008),'teal')
    for x,y in [(-.121,-.123),(.181,-.143)]:
        foot=box('guard','exposed guard screw foot',(x,y,.012),(.018,.012,.008),'teal')
        bore(foot,(x,y,.012),.00165,.020);bore(deck,(x,y,.004),.0014,.024)
        bolt('guard',x,y,.009,.016)
    # One connected clamp fits the exposed right arch, away from the tile.
    # The original pinwheel's handle slides into a blind rectangular socket.
    saddle=S.annulus('cargo open arch saddle',(0,0,0),.0055,.0042,.030,'teal',gap=math.pi+.05)
    saddle.rotation_euler.y=math.pi/2;saddle.location=(.175,.015,.200)
    a.add('cargo',saddle)
    support=box('cargo','cargo socket support',(.190,.030,.200),(.058,.040,.028),'teal')
    cut(support,(.205,.039,.211),(.0156,.0096,.048))
    cut(support,(.175,.030,.194),(.0086,.050,.0208))
    bore(support,(.200,.017,.200),.0016,.060,'X')
    bore(saddle,(.190,.017,.200),.0016,.026,'X')
    # The clamp tip contacts the arch at x=.179. Its thumb wheel and exposed
    # shaft stand beyond the support's x=.219 face, clear of the handle socket.
    cyl('cargo','captive arch clamp screw',(.204,.017,.200),.0015,.050,'ink','X')
    cyl('cargo','arch clamp thumb wheel',(.225,.017,.200),.006,.009,'orange','X')
    socket=box('cargo','cargo handle socket',(.205,.039,.205),(.031,.025,.038),'teal')
    cut(socket,(.205,.039,.211),(.0156,.0096,.048))
    # The socket's bottom is 1 mm below the original handle's -12 mm tip.
    for side in (-1,1):
        box('cargo','soft handle grip pad',(.205+side*.0078,.039,.205),(.0006,.0096,.026),'ink')
    # Pads are shown at their nominal seated surface. They do not latch: a hand
    # can lift the handle straight out without an unseen screw-release action.
    import importlib.util
    import sys
    spec=importlib.util.spec_from_file_location('builder_cargo_pinwheel',Path(__file__).parents[1]/'chapter-one-art/pinwheel.py')
    pinwheel=importlib.util.module_from_spec(spec);sys.modules[spec.name]=pinwheel;spec.loader.exec_module(pinwheel)
    pw=pinwheel.make();pinwheel.set_state(pw,'pinwheel')
    pw['root'].parent=a.root;pw['root'].location=PINWHEEL_MOUNT
    for key,objects in pw['parts'].items():
        for obj in objects:
            if obj.type in {'MESH','CURVE'} and not obj.hide_render:
                a.parts.setdefault('pinwheel:'+key,[]).append(obj)
    return a.result(projector=pj,pinwheel=pw,slider=slider,deck=deck,guard=guard,dock_fingers=dock_fingers)


def stage(model,identity):
    info=PLAN[identity]
    model['root'].rotation_euler=(math.pi if info.get('upside') else 0,0,math.pi if info.get('rear') else 0)
    model['root'].location=(0,0,.23 if info.get('upside') else 0)
    model['slider'].location.x=0
    pose_dock_studs(model)
    projector.pose(model['projector'])
    visible(model,info['parts'])
    if info['group'] in {'carrier-work','carrier-cargo'}:
        return dict(location=(.65,-.85,.62),target=(.025,0,.075),scale=.64)
    if info['group']=='carrier-finished':
        return dict(location=(.70,-.95,.72),target=(.025,0,.230),scale=.78)
    if info['group']=='carrier-rear':
        return dict(location=(.65,-.85,.62),target=(-.025,0,.075),scale=.64)
    if info['group']=='carrier-under':
        return dict(location=(.65,-.85,.85),target=(.025,0,.16),scale=.64)
    if info.get('upside'): return inspection(model,(.625,-.85,.69))
    if info.get('rear'): return inspection(model,(.625,-.85,.545))
    return inspection(model)


def pose_dock_studs(model,compression=0.):
    """Geometric snap-fit access pose; no material-force prediction.

    The split fingers bend inward up to 0.6 mm while the box passes over them.
    Their unloaded 7 mm retaining lips then sit above the 6.2 mm collar bores.
    """
    if not 0<=compression<=.0006:raise ValueError('Dock finger compression must be 0..0.6 mm')
    for obj,rest in model['dock_fingers']:
        for vertex,co in zip(obj.data.vertices,rest):
            z=obj.location.z+co.z;radius=math.hypot(co.x,co.y)
            deflection=compression*max(0,min(1,(z-.0288)/.0034))
            factor=1-deflection/radius if radius else 1
            vertex.co=(co.x*factor,co.y*factor,co.z)
        obj.data.update()


def geometry_check():
    """Explicit layout assumptions, not physical strength or flight validation."""
    masses={'deck':(.30,.004),'frame':(.16,.12),'tile':(.13,TILE_HEIGHT),
            'projector':(.28,PROJECTOR_MOUNT[2]+.065),'lift battery':(.25,-.025),
            'motor battery':(.10,-.025),'counterweight':(.06,-.043),
            'drive and shell':(.08,.055),'cargo clip':(.04,.200),
            'carried pinwheel':(.03,PINWHEEL_MOUNT[2]+.180)}
    cg=sum(m*z for m,z in masses.values())/sum(m for m,z in masses.values())
    return dict(deck_m=[.4,.3],projector_dimensions_m=[.18,.13,.13],
                projector_top_m=PROJECTOR_MOUNT[2]+.132, # includes the connected lid return
                cradle_bottom_m=.204,tile_force_height_m=TILE_HEIGHT,assumed_cg_m=cg,
                assumed_masses_kg_and_height_m=masses,
                lift_above_assumed_cg_m=TILE_HEIGHT-cg,
                shaft_height_error_m=DRIVEN[1]-DRIVER[1],
                speed_ratio=(SMALL_RADIUS+BELT_RADIUS)/(BIG_RADIUS+BELT_RADIUS),
                belt_pitch_radii_m=[SMALL_RADIUS+BELT_RADIUS,BIG_RADIUS+BELT_RADIUS],
                lens_bottom_m=PROJECTOR_MOUNT[2]+.116-.008,
                guard_top_m=.087+.073/2,
                limit='Ideal geometry and explicit assumed masses; no manufactured strength, electrical performance or lift validation.')


if __name__=='__main__':
    text=A.markdown()
    # The carried original retains its exact factory; only its display size is
    # smaller on this crowded construction page, before it is physically fitted.
    marker='**Items**\n'
    start=text.index('## `c-lift-projector`')
    at=text.index(marker,start)+len(marker)
    text=text[:at]+'- `star-projector` Star projector\n  - from chapter `c-lift-projector` icon: ![Star projector](assets/items/fc-projector-carried.webp)\n  - from chapter `c-lift-projector` animation: none\n'+text[at:]
    start=text.index('## `c-whale-cargo`');at=text.index(marker,start)+len(marker)
    carried='- `fc-guarded` Whale\n  - from chapter `c-whale-cargo` icon: ![Whale](assets/items/fc-cargo-ready.webp)\n'
    carried+='- `pinwheel` Pinwheel\n  - from chapter `c-whale-cargo` icon: ![Pinwheel](assets/items/fc-pinwheel-carried.webp)\n  - from chapter `c-whale-cargo` animation: none\n'
    text=text[:at]+carried+text[at:]
    Path(__file__).with_suffix('.md').write_text(text)
    print(f'Carrier: {len(PLAN)} images; {len(A.recipes)} recipes; five chapters.')
