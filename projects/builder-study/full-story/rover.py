"""Literal two-drive drawing rover, retaining the canonical 220 × 180 mm deck.

Source geometry includes actual D shafts, wheel sockets, captive guard clips,
motor connectors and a cam-operated pen carriage. No test scenery is supplied.
"""
from pathlib import Path
import math
import sys
from late.common import Author, BASE, ROOT, geometry, visible, inspection

A=Author()
I=lambda identity,name,parts,group='rover-loose',css=110,**kw:A.item(identity,name,parts,group,css,**kw)
I('rv-deck','Deck',['deck'],'rover-top',250,note='The prepared deck includes two bare pen guide rods and a hand-operated lift cam. Fit the carriage, then its return spring and connected guide cap.')
I('rv-under','Deck',['deck'],'rover-under',220,upside=True)
for side in ('a','b'):
    label='Left' if side=='a' else 'Right'
    I('rv-motor-'+side,label+' motor',['motor-'+side],image='rv-motor-'+side,note='An enclosed slow gearmotor, mounting flange and attached lead. Its output shaft drives one wheel.')
    I('rv-wheel-'+side,'Wheel',['wheel-a'],image='rv-wheel',note='Either wheel fits either geared motor. Its retained centre fastener locks the hub to the flat-sided shaft.')
    I('rv-drive-'+side,label+' drive',['motor-'+side,'wheel-'+side],'rover-drive-'+side,160)
    A.plan['rv-motor-'+side].update(group='rover-drive-'+side,css=160)
    for wheel in ('a','b'): A.add('rv-wheel-'+wheel,'rv-motor-'+side,'rv-drive-'+side)
for identity,name,key,note in [
    ('rv-caster','Caster','caster','The free-turning ball supports the third corner.'),
    ('rv-pack','Battery pack','pack','An enclosed compatible low-voltage pack with cells already fitted.'),
    ('rv-receiver','Receiver','receiver','The supplied receiver and motor driver control the wheels independently. Its matching ready-to-use remote needs no construction here.'),
    ('rv-harness','Switch harness','harness','A connected fused harness and switch. Fit with the power off and connect the parked battery and motor plugs to their matching sockets.'),
    ('rv-guard-a','Guard','guard-a','One hollow snap-on guard. Its open shaft slot and split cable channel fit around the already attached wheel and lead.'),
    ('rv-guard-b','Guard','guard-b','One hollow snap-on guard, fitted independently on the other drive.'),
    ('rv-pen','Pen','pen','A felt-tip pen with its cap removed.'),
    ('rv-clip','Pen carriage','carriage','One connected bridge, spring clip and follower shoe. The deck already carries the guides and lift lever.'),
    ('rv-spring','Return spring','spring','One compression spring slides down the near guide rod after the carriage. The guide cap retains its upper end.'),
    ('rv-cap','Guide cap','cap','One connected bridge with two soft lined sockets. Press it onto the two bare guide ends to retain the carriage and compress its return spring.'),
]: I(identity,name,[key],note=note)

FITTINGS=[('rv-drive-a',['motor-a','wheel-a']),('rv-drive-b',['motor-b','wheel-b']),('rv-caster',['caster']),('rv-pack',['pack']),('rv-receiver',['receiver'])]
STATE={0:'rv-under',31:'rv-mounted'}
for mask in range(1,31): STATE[mask]=f'rv-deck-{mask:02d}'
for mask in range(1,32):
    parts=['deck']+[part for bit,(_,keys) in enumerate(FITTINGS) if mask&(1<<bit) for part in keys]
    I(STATE[mask],'Rover',parts,'rover-under',220,upside=True)
for mask in range(32):
    for bit,(part,_) in enumerate(FITTINGS):
        if not mask&(1<<bit): A.add(part,STATE[mask],STATE[mask|(1<<bit)])
A.process('rv-deck','rv-flip-build','rv-under')
base=A.plan['rv-mounted']['parts']
I('rv-wired','Rover',base+['harness'],'rover-under',220,upside=True)
A.add('rv-harness','rv-mounted','rv-wired')
for mask,identity in [(1,'rv-one-guard-a'),(2,'rv-one-guard-b'),(3,'rv-guarded')]:
    I(identity,'Rover',base+['harness']+['guard-'+s for bit,s in enumerate(('a','b')) if mask&(1<<bit)],'rover-under',220,upside=True)
for side,other in [('a','b'),('b','a')]:
    A.add('rv-guard-'+side,'rv-wired','rv-one-guard-'+side)
    A.add('rv-guard-'+other,'rv-one-guard-'+side,'rv-guarded')
full=base+['harness','guard-a','guard-b']
I('rv-upright','Rover',full,'rover-pen-work',320)
A.process('rv-guarded','rv-flip-pen','rv-upright')
I('rv-pen-carriage','Pen carriage',['pen','carriage'],'rover-pen',150)
A.plan['rv-clip'].update(group='rover-pen',css=150)
A.add('rv-pen','rv-clip','rv-pen-carriage')
I('rv-pen-fitted','Rover',full+['pen','carriage'],'rover-pen-work',320)
A.add('rv-pen-carriage','rv-upright','rv-pen-fitted')
I('rv-sprung','Rover',full+['pen','carriage','spring'],'rover-pen-work',320)
A.add('rv-spring','rv-pen-fitted','rv-sprung')
I('drawing-rover','Drawing rover',full+['pen','carriage','spring','cap'],'rover-finished',340,note='Different wheel speeds steer the rover. The hand lever lifts the pen between strokes. A slight motor mismatch makes a curve; the receiver has a trim screw. These are ordinary mechanisms, not a promise of precise handwriting.')
A.add('rv-cap','rv-sprung','drawing-rover')

def states_with(bits): return [STATE[mask] for mask in range(32) if mask&bits==bits]
A.page('c-rover-drive','Two wheels, two motors','rv-mounted',
       ['rv-deck','rv-motor-a','rv-motor-b','rv-wheel-a','rv-wheel-b','rv-caster','rv-pack','rv-receiver'],
       ['rv-under','rv-drive-a','rv-drive-b']+[STATE[m] for m in range(1,32)],
       [('Flip the deck over','rv-under'),('Fit a wheel to the left motor','rv-drive-a'),
        ('Fit a wheel to the right motor','rv-drive-b'),
        ('Fit the left drive to the deck',states_with(1)),('Fit the right drive',states_with(3)),('Fit the caster',states_with(4)),
        ('Fit the battery pack',states_with(8)),('Fit the receiver','rv-mounted')],
       [('rv-flip-build','Flip','flip')])
A.page('c-rover-pen','A pen for the rover','drawing-rover',
       ['rv-harness','rv-guard-a','rv-guard-b','rv-pen','rv-clip','rv-spring','rv-cap'],
       ['rv-wired','rv-one-guard-a','rv-one-guard-b','rv-guarded','rv-upright','rv-pen-carriage','rv-pen-fitted','rv-sprung','drawing-rover'],
       [('Connect the switch harness','rv-wired'),('Fit a guard',['rv-one-guard-a','rv-one-guard-b','rv-guarded']),('Fit the other guard','rv-guarded'),
        ('Flip the rover upright','rv-upright'),('Clip the pen into its carriage','rv-pen-carriage'),
        ('Slide the carriage onto the guides','rv-pen-fitted'),('Slide on the return spring','rv-sprung'),
        ('Press on the guide cap','drawing-rover')],[('rv-flip-pen','Flip','flip')])
PLAN=A.plan

# A readable, real compression spring with room for the full 8 mm cam lift.
# The guide extension and two wider seats exist before the spring is fitted;
# no retained hardware changes shape during an additive construction step.
GUIDE_EXTENSION=.016
SPRING_RADIUS=.0052
SPRING_WIRE=.00065
SPRING_TURNS=4
SPRING_SEAT_RADIUS=.0065
SPRING_LOW=.095+SPRING_WIRE
SPRING_HIGH=.107+GUIDE_EXTENSION-SPRING_WIRE
SPRING_STEPS=192


def spring_radius(lift):
    """Let the helix widen slightly on compression, preserving its wire length."""
    chord_factor=2*SPRING_STEPS*math.sin(math.pi*SPRING_TURNS/SPRING_STEPS)
    rest_height=SPRING_HIGH-SPRING_LOW
    return math.sqrt(SPRING_RADIUS**2+(rest_height**2-(rest_height-lift)**2)/chord_factor**2)


def apply_pose(model,**kwargs):
    """Retain the canonical drive/cam motion and update the larger elastic coil."""
    import drawing_rover as R
    pose=R.apply_pose(model,**kwargs)
    low=SPRING_LOW+pose['lift'];radius=spring_radius(pose['lift'])
    points=[(-.048+radius*math.cos(math.tau*SPRING_TURNS*i/SPRING_STEPS),
             -.010+radius*math.sin(math.tau*SPRING_TURNS*i/SPRING_STEPS),
             low+(SPRING_HIGH-low)*i/SPRING_STEPS) for i in range(SPRING_STEPS+1)]
    curve=model['pressure'].data;curve.splines.clear()
    spline=curve.splines.new('POLY');spline.points.add(len(points)-1)
    for vertex,point in zip(spline.points,points):vertex.co=(*point,1)
    return pose


def build():
    import bpy
    from mathutils import Vector
    S=geometry()
    import drawing_rover as R
    sys.path.insert(0,str(BASE.parent/'art-readability-2026.11.07'))
    import assembly_views
    model=R.build_model();assembly_views.prepare(model)
    R.apply_pose(model,wheel_angles=(0,0),pen_angle=0,upside_down=False)
    R._wire_state(model,False)
    old=model['parts']; parts={}
    for new,previous in [('deck','rover-deck'),('caster','rover-caster'),('pack','rover-pack'),
                         ('harness','rover-switch'),('receiver','rover-radio'),('pen','rover-pen'),('carriage','rover-pen-clip')]:
        parts[new]=old[previous]
    for obj in parts['pack']:
        if obj.name.startswith(('closed low-voltage battery holder','battery holder mount flange')):
            obj.data.materials.clear();obj.data.materials.append(S.material('battery'))
    # The exposed slider connects to the enclosed switch through a real slot.
    flange=next(o for o in parts['harness'] if o.name.startswith('switch mounting flange'))
    cutter=S.box('switch stem travel slot',(-.080,0,.0505),(.016,.005,.008),'ink')
    bpy.context.view_layer.objects.active=flange
    modifier=flange.modifiers.new('actual actuator travel opening','BOOLEAN');modifier.operation='DIFFERENCE';modifier.object=cutter
    bpy.ops.object.modifier_apply(modifier=modifier.name);bpy.data.objects.remove(cutter,do_unlink=True)
    stem=S.box('connected switch actuator stem',(0,0,-.008),(.004,.004,.006),'ink')
    stem.parent=model['switch_handle'];parts['harness'].append(stem)
    test_props={obj for objects in model['props'].values() for obj in objects}
    parts['deck']=[obj for obj in parts['deck'] if obj not in test_props]
    # A closed carriage can now lower over bare guide rods. The compression
    # spring and the connected socket cap are subsequent actual additions.
    old_caps=[obj for obj in parts['deck'] if obj.name.startswith('guide rod captive top stop')]
    upper_seats=[obj for obj in parts['deck'] if obj.name.startswith('pen spring seat')]
    parts['deck']=[obj for obj in parts['deck'] if obj not in old_caps+upper_seats and obj!=model['pressure']]
    parts['spring']=[model['pressure']]
    # A 11.7 mm outside diameter coil is seated on real 13 mm washers. Its
    # 26.7 mm centreline height leaves distinct turns at playing size; the
    # longer bare rods and cap also leave 18.7 mm at maximum cam lift.
    # Rebuild the seats with unchanged bores rather than scaling their holes.
    for key in ('deck','carriage'):
        for old_seat in list(parts[key]):
            if not old_seat.name.startswith('pen spring seat'):continue
            seat=S.annulus('pen spring seat',(0,0,0),SPRING_SEAT_RADIUS,.0017,.001,'teal')
            seat.parent=old_seat.parent;seat.location=old_seat.location;seat.rotation_euler=old_seat.rotation_euler
            parts[key][parts[key].index(old_seat)]=seat
            bpy.data.objects.remove(old_seat,do_unlink=True)
    for index,old_seat in enumerate(upper_seats):
        seat=S.annulus('pen spring upper seat',(0,0,0),SPRING_SEAT_RADIUS,.0017,.001,'teal')
        seat.parent=old_seat.parent;seat.location=old_seat.location;seat.rotation_euler=old_seat.rotation_euler
        seat.location.z+=GUIDE_EXTENSION;upper_seats[index]=seat
        bpy.data.objects.remove(old_seat,do_unlink=True)
    for rod in parts['deck']:
        if rod.name.startswith('carriage guide rod'):
            for vertex in rod.data.vertices:
                if vertex.co.z>0:vertex.co.z+=GUIDE_EXTENSION
            rod.data.update()
    model['pressure'].data.bevel_depth=SPRING_WIRE
    model['pressure'].data.materials.clear();model['pressure'].data.materials.append(S.material('ink'))
    parts['cap']=upper_seats
    def cap_add(obj):
        obj.parent=model['vehicle'];obj.location.z+=GUIDE_EXTENSION;parts['cap'].append(obj);return obj
    cap_add(S.box('connected two-socket guide cap',(-.048,0,.1105),(.006,.026,.003),'teal'))
    for y in [-.010,.010]:
        cap=S.cylinder('guide cap blind socket',(-.048,y,.109),.003,.004,'teal','Z')
        S.bore(cap,(-.048,y,.1075),.00155,.003,'Z');cap_add(cap)
        liner=S.annulus('soft guide cap socket lining',(0,0,0),.00155,.00145,.002,'paper')
        liner.rotation_euler.x=math.pi/2;liner.location=(-.048,y,.1075);cap_add(liner)
    bpy.context.view_layer.update()
    def side(obj):
        for i,parent in enumerate(model['wheels']):
            probe=obj
            while probe:
                if probe==parent:return 'a' if i==0 else 'b'
                probe=probe.parent
        y=sum((obj.matrix_world@Vector(p)).y for p in obj.bound_box)/8 if obj.type in {'MESH','CURVE'} else obj.matrix_world.translation.y
        return 'a' if y<0 else 'b'
    for new,previous in [('motor','rover-gearmotors'),('wheel','rover-wheels'),('guard','rover-covers')]:
        for suffix in ('a','b'):parts[new+'-'+suffix]=[o for o in old[previous] if side(o)==suffix]
    for obj in model['root'].children_recursive:
        if obj.type in {'MESH','CURVE','FONT'}:obj.hide_render=True;obj.hide_set(True)
    # The animation adapter uses this same source pose function, so the still
    # and working loop share the extended spring rather than reverting to the
    # historical short coil on the first animated frame.
    model['parts']=parts;model['_rover_source']=sys.modules[__name__]
    for key,objects in parts.items():
        for obj in objects:obj['part_id']=key
    return model


def stage(model,identity):
    import drawing_rover as R
    info=PLAN[identity]
    underside=info.get('upside',False) or any(key in info['parts'] for key in ('motor-a','motor-b','wheel-a','wheel-b','caster','pack','receiver','harness','guard-a','guard-b')) and 'deck' not in info['parts']
    R.pose_guard_installation(model)
    apply_pose(model,upside_down=underside,pen_angle=0)
    # Leads are already parked at the matching connector positions. Adding
    # the harness supplies the sockets; no earlier component silently reshapes.
    R._wire_state(model,True)
    visible(model,info['parts'])
    if info['group']=='rover-under':return dict(location=(.45,-.6,.8),target=(0,0,.075),scale=.39)
    # The explicit upright Flip begins a larger pen-fitting display family.
    # Only export magnification changes; the camera and physical geometry stay fixed.
    if info['group'] in {'rover-top','rover-pen-work','rover-finished'}:return dict(location=(-.45,-.6,.705),target=(0,0,.055),scale=.39)
    # A receiving motor/carriage retains its physical scale when its wheel or
    # pen appears. Its fitting orientation also matches the destination deck.
    group=info['group']
    if group.startswith('rover-drive-') or group=='rover-pen':
        keys={key for row in PLAN.values() if row['group']==group for key in row['parts']}
        visible(model,keys);view=inspection(model,(.45,-.6,.725) if underside else (-.45,-.6,.65));visible(model,info['parts'])
        return view
    return inspection(model,(.45,-.6,.725) if underside else (-.45,-.6,.65))


if __name__=='__main__':
    Path(__file__).with_suffix('.md').write_text(A.markdown())
    print(f'Rover: {len(PLAN)} images; {len(A.recipes)} recipes; two chapters.')
