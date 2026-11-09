"""A 240 × 200 mm belt-driven string spinner, in metres.

The motor and driven spindle have real bearings, keyed pulleys, a tangent belt,
a removable clear belt guard and retained drive wheel. The pink wheel alone
supplies the fictional constraint keeping the ordinary continuous cord aloft.
Dark string with contrasting surface bands makes its circulation visible.
Its finished pose is the first frame of set_motion(); shaft angles and the
moving joined cord remain available independently for a later 3D renderer.
"""
from pathlib import Path
import math
from late.common import Author

A=Author()
def item(identity,name,parts,group='spinner-loose',css=130,**pose):
    return A.item(identity,name,parts,group,css,**pose)

for key,name,size in [('base','Base',250),('motor','Motor',145),('bearing','Spindle',145),
                      ('motor-pulley','Small pulley',115),('driven-pulley','Large pulley',130),
                      ('belt','Belt',165),('guard','Guard',175),('wheel','Wheel',145),('collar','Collar',110)]:
    item('sp-'+key,name,[key],'spinner-drive' if key=='base' else 'spinner-loose',size)
# Motor and spindle pulleys can be fitted before or after mounting their units.
item('sp-motor-unit','Motor',['motor','motor-pulley'],'spinner-motor',235)
item('sp-bearing-unit','Spindle',['bearing','driven-pulley'],'spinner-bearing',235)
A.add('sp-motor-pulley','sp-motor','sp-motor-unit')
A.add('sp-driven-pulley','sp-bearing','sp-bearing-unit')
ready={0:'sp-base'}
for motor in (0,1,5):
    for bearing in (0,2,10):
        mask=motor|bearing
        if not mask:continue
        identity='sp-drive' if mask==15 else 'sp-drive-'+str(mask)
        ready[mask]=identity
        item(identity,'Base',['base']+[p for bit,p in [(1,'motor'),(2,'bearing'),(4,'motor-pulley'),(8,'driven-pulley')] if mask&bit],'spinner-drive',250)
for mask,owner in ready.items():
    for bit,part,required in [(1,'motor',0),(2,'bearing',0),(4,'motor-pulley',1),(8,'driven-pulley',2)]:
        if not mask&bit and (not required or mask&required):A.add('sp-'+part,owner,ready[mask|bit])
    if not mask&1:A.add('sp-motor-unit',owner,ready[mask|5])
    if not mask&2:A.add('sp-bearing-unit',owner,ready[mask|10])
base=A.plan['sp-drive']['parts']
for identity,owner,part,parts in [
    ('sp-belted','sp-drive','sp-belt',base+['belt']),
    ('sp-guarded','sp-belted','sp-guard',base+['belt','guard']),
    ('sp-wheeled','sp-guarded','sp-wheel',base+['belt','guard','wheel']),
    ('sp-drive-ready','sp-wheeled','sp-collar',base+['belt','guard','wheel','collar'])]:
    item(identity,'Drive',parts,'spinner-drive',250);A.add(part,owner,identity)
first=list(A.items)
A.page('c-spinner-drive','Two pulleys','sp-drive-ready',
       ['sp-base','sp-motor','sp-bearing','sp-motor-pulley','sp-driven-pulley','sp-belt','sp-guard','sp-wheel','sp-collar'],
       [i for i in first if i not in ['sp-base','sp-motor','sp-bearing','sp-motor-pulley','sp-driven-pulley','sp-belt','sp-guard','sp-wheel','sp-collar']],
       [('Mount the motor',[ready[m] for m in ready if m&1]),('Mount the spindle',[ready[m] for m in ready if m&2]),
        ('Fit the small pulley',['sp-motor-unit']+[ready[m] for m in ready if m&4]),
        ('Fit the large pulley','sp-drive'),('Loop the belt around both pulleys','sp-belted'),
        ('Fit the guard','sp-guarded'),('Fit the wheel','sp-wheeled'),('Fit the collar','sp-drive-ready')])
for key,name,size in [('battery','Battery',145),('switch','Switch',115),('fork','Fork',155),
                      ('string','String',170),('joiner','Joiner',105)]:
    item('sp-'+key,name,[key],css=size)
A.plan['sp-string'].update(group='spinner-string',css=250)
item('sp-string-loop','Loop',['string','joiner'],'spinner-string',250,closed=True)
A.add('sp-joiner','sp-string','sp-string-loop')
base=A.plan['sp-drive-ready']['parts']
fitted={0:'sp-drive-ready'}
for mask in range(1,8):
    fitted[mask]='sp-fitted-'+str(mask)
    item(fitted[mask],'Spinner',base+[p for bit,p in [(1,'battery'),(2,'switch'),(4,'fork')] if mask&bit],'spinner-assembly',270)
for mask,owner in fitted.items():
    for bit,part in [(1,'battery'),(2,'switch'),(4,'fork')]:
        if not mask&bit:A.add('sp-'+part,owner,fitted[mask|bit])
item('ribbon-spinner','String spinner',A.plan[fitted[7]]['parts']+['string','joiner'],'spinner-finished',350,closed=True)
A.add('sp-string-loop',fitted[7],'ribbon-spinner')
second=[i for i in A.items if i not in first]
A.page('c-spinner-ribbon','A loop of string','ribbon-spinner',
       ['sp-battery','sp-switch','sp-fork','sp-string','sp-joiner'],
       [i for i in second if i not in ['sp-battery','sp-switch','sp-fork','sp-string','sp-joiner']],
       [('Fit the battery',[fitted[m] for m in fitted if m&1]),('Fit the switch',[fitted[m] for m in fitted if m&2]),
        ('Fit the fork',[fitted[m] for m in fitted if m&4]),('Join the ends of the string','sp-string-loop'),
        ('Thread the loop over the wheel','ribbon-spinner')])
PLAN=A.plan
WHEEL_CENTER=(.040,-.079,.105)
WHEEL_RADIUS=.039
MOTOR_RADIUS=.012
DRIVEN_RADIUS=.032


def belt_path(samples=80):
    """Exterior tangent belt in XZ, with common pulley plane y=-.006."""
    x0,z0=-.068,.050;x1,z1=.040,.105;r0=MOTOR_RADIUS;r1=DRIVEN_RADIUS
    dx=x1-x0;dz=z1-z0;distance=math.hypot(dx,dz);phi=math.atan2(dz,dx)
    alpha=math.acos((r0-r1)/distance)
    upper=phi+alpha;lower=phi-alpha
    points=[]
    # Smaller pulley outer arc faces away from the larger pulley.
    for j in range(samples//2+1):
        angle=upper+(lower+2*math.pi-upper)*j/(samples//2)
        points.append((x0+r0*math.cos(angle),-.006,z0+r0*math.sin(angle)))
    # Larger pulley outer arc faces away from the small pulley.
    for j in range(samples//2+1):
        angle=lower+(upper-lower)*j/(samples//2)
        points.append((x1+r1*math.cos(angle),-.006,z1+r1*math.sin(angle)))
    points.append(points[0]);return points


def string_path(phase=0.,samples=160):
    """Closed centreline; fixed lower wrap, gently moving upper string envelope.

    The radius and wheel contact arc never change. The free part bows in the
    same plane; the small lateral motion is continuous at both tangent exits.
    This prescribed flexible envelope is not a material-dynamics simulation.
    """
    cx,cy,cz=WHEEL_CENTER;r=WHEEL_RADIUS
    points=[]
    # Upper return is a broad oval arch. Its first and last derivatives are
    # vertical, tangential to the circular drive contact beneath the wheel.
    for j in range(samples+1):
        t=j/samples;angle=math.pi*t
        x=cx+r*math.cos(angle)+.100*math.sin(2*angle)*math.sin(angle)
        z=cz+.21938249779957764*math.sin(angle)
        # Keep the endpoints, their tangents and the entire lower wheel wrap fixed.
        x += .011*math.sin(phase)*math.sin(angle)**3
        y=cy+.007*math.sin(phase+2*angle)*math.sin(angle)**3
        points.append((x,y,z))
    for j in range(1,samples//3+1):
        angle=math.pi+math.pi*j/(samples//3)
        points.append((cx+r*math.cos(angle),cy,cz+r*math.sin(angle)))
    return points


def path_position(points,fraction):
    lengths=[math.dist(a,b) for a,b in zip(points,points[1:])]
    target=(fraction%1)*sum(lengths)
    for index,length in enumerate(lengths):
        if target<=length or index==len(lengths)-1:
            weight=target/max(length,1e-12);a,b=points[index],points[index+1]
            return tuple(a[i]+weight*(b[i]-a[i]) for i in range(3)),tuple(b[i]-a[i] for i in range(3))
        target-=length


def build():
    import bpy
    import core
    from mathutils import Vector
    S=core.S;a=core.Assembly('compact string spinner');box=a.box;cyl=a.cylinder
    def cut(obj,center,size):
        cutter=S.box('prepared keyed opening',center,size);bpy.context.view_layer.objects.active=obj
        mod=obj.modifiers.new('actual receiving opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
        bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    def bore(obj,c,r,depth,axis='Z'):S.bore(obj,c,r,depth,axis)
    def bolt(part,name,c,r=.0018,depth=.020,axis='Z',parent=None):core.bolt(a,part,name,c,r,depth,axis,parent)
    base=box('base','broad wooden spinner base',(0,0,.009),(.240,.200,.018),'birch')
    motor= S.empty('motor shaft angle');motor.parent=a.root;motor.location=(-.068,0,.050)
    driven=S.empty('driven shaft angle');driven.parent=a.root;driven.location=(.040,0,.105)
    # The ordinary geared motor is one connected retained mechanism. Its shaft
    # projects toward the viewer; the separately supplied pulley slides onto it.
    cyl('motor','enclosed geared motor',(-.068,.041,.050),.023,.058,'ink','Y')
    motorfoot=box('motor','motor mounting foot',(-.068,.038,.024),(.067,.070,.012),'teal')
    bore(motorfoot,(-.068,.041,.050),.0232,.085,'Y')
    a.line('motor','connected motor retaining strap',[(-.094,.015,.027),(-.094,.015,.055),(-.084,.015,.071),(-.052,.015,.071),(-.042,.015,.055),(-.042,.015,.027)],.003,'teal')
    for x in (-.094,-.042):
        bore(base,(x,.038,.009),.0019,.030);bolt('motor','captive motor mounting screw',(x,.038,.0207),depth=.020)
    cyl('motor','motor output shaft',(0,-.003,0),.0024,.030,'ink','Y',motor)
    box('motor','motor shaft flat',(0,-.013,0),(.0048,.011,.0048),'ink',motor)
    # The bearing frame has a real continuous bore, axial collars, base foot
    # and bracing webs. Only its spindle rotates, around the same Y axis.
    foot=box('bearing','spindle bearing foot',(.040,.039,.024),(.070,.060,.012),'teal')
    pedestal=box('bearing','spindle bearing upright',(.040,.046,.074),(.058,.020,.090),'teal')
    bore(pedestal,(.040,.046,.105),.0042,.030,'Y')
    for x in (.015,.065):
        bore(base,(x,.020,.009),.0019,.030);bolt('bearing','captive spindle mounting screw',(x,.020,.0207),depth=.020)
    cyl('bearing','continuous driven shaft',(0,-.016,0),.0034,.180,'ink','Y',driven)
    for y in (.032,.060):cyl('bearing','retained bearing shaft collar',(0,y,0),.008,.006,'ink','Y',driven)
    # Square drive sleeves terminate at the free front ends. Both supplied
    # pulley and wheel have matching actual sockets and captive clamp screws.
    box('bearing','square driven pulley seat',(0,-.006,0),(.007,.018,.007),'ink',driven)
    box('bearing','square wheel seat',(0,-.085,0),(.007,.035,.007),'ink',driven)
    # Boolean cutters use each object's local coordinates before parenting;
    # temporarily clear parent transforms for accurate square local sockets.
    # Each pulley is created at local origin under its existing parent;
    # the boolean helper below compensates for that parent's full transform.
    def local_pulley(part,parent,radius,plane,color,hole):
        saved=parent.location.copy();parent.location=(0,0,0);bpy.context.view_layer.update()
        for y,r,th in [(plane,radius-.0012,.006),(plane-.004,radius+.003,.002),(plane+.004,radius+.003,.002)]:
            disk=cyl(part,'grooved '+part,(0,y,0),r,th,color,'Y',parent)
            cut(disk,(0,y,0),(hole,th+.006,hole))
        hub=cyl(part,part+' keyed hub',(0,plane-.007,0),.010,.008,color,'Y',parent)
        cut(hub,(0,plane-.007,0),(hole,.020,hole))
        cyl(part,'captive hub clamp screw',(.008,plane-.007,0),.0015,.007,'ink','X',parent)
        parent.location=saved;bpy.context.view_layer.update()
    local_pulley('motor-pulley',motor,MOTOR_RADIUS,-.006,'orange',.0052)
    local_pulley('driven-pulley',driven,DRIVEN_RADIUS,-.006,'teal',.0074)
    belt=a.line('belt','one continuous tangent belt',belt_path(),.0012,'ink')
    # A real open-bottom clear shell can descend over the fitted belt. Its
    # front spindle slot is open below, then the wheel retains the cover.
    clear=bpy.data.materials.new('clear spinner guard');clear.use_nodes=True
    nodes=clear.node_tree.nodes;nodes.clear();links=clear.node_tree.links
    output=nodes.new('ShaderNodeOutputMaterial');mix=nodes.new('ShaderNodeMixShader')
    transparent=nodes.new('ShaderNodeBsdfTransparent');surface=nodes.new('ShaderNodeBsdfPrincipled')
    surface.inputs['Base Color'].default_value=(.48,.72,.78,1)
    surface.inputs['Roughness'].default_value=.15
    mix.inputs[0].default_value=.10
    links.new(transparent.outputs[0],mix.inputs[1]);links.new(surface.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],output.inputs[0])
    clear.diffuse_color=(.48,.72,.78,.10)
    walls=[((-.013,-.033,.086),(.193,.002,.130)),((-.013,.013,.149),(.193,.094,.004)),
           ((-.108,.013,.084),(.003,.094,.132)),((.082,.013,.084),(.003,.094,.132))]
    for index,(center,size) in enumerate(walls):
        obj=box('guard','connected clear belt guard',center,size,'paper')
        if index==0:
            bore(obj,(.040,-.033,.105),.005,.008,'Y')
            cut(obj,(.040,-.033,.061),(.010,.008,.088))
        core.surface(obj,clear)
    for x in (-.096,.058):
        box('guard','integral guard locating foot',(x,-.026,.021),(.012,.010,.010),'teal')
        box('guard','integral foot to shell bridge',(x,-.0275,.024),(.012,.017,.006),'teal')
        cut(base,(x,-.026,.016),(.0124,.0104,.0044))
    # Pink driven wheel has a real open-front cord groove. The forward flange
    # is shallow enough that the 2.4 mm cord and its small flexible joiner pass.
    saved=driven.location.copy();driven.location=(0,0,0);bpy.context.view_layer.update()
    wheel=cyl('wheel','pink driven wheel',(0,-.070,0),.0378,.028,'future','Y',driven)
    cut(wheel,(0,-.070,0),(.0074,.040,.0074))
    back=cyl('wheel','pink wheel rear retaining flange',(0,-.063,0),.043,.004,'future','Y',driven)
    cut(back,(0,-.063,0),(.0074,.020,.0074))
    lip=cyl('wheel','shallow front cord retaining lip',(0,-.085,0),.0385,.003,'future','Y',driven)
    cut(lip,(0,-.085,0),(.0074,.010,.0074))
    # A cream radial mark makes actual wheel rotation legible.
    box('wheel','wheel rotation mark',(.023,-.087,0),(.025,.001,.004),'paper',driven)
    collar=cyl('collar','drive wheel retaining collar',(0,-.094,0),.015,.012,'orange','Y',driven)
    cut(collar,(0,-.094,0),(.0074,.025,.0074))
    cyl('collar','captive collar clamp screw',(.012,-.094,0),.002,.009,'ink','X',driven)
    driven.location=saved;bpy.context.view_layer.update()
    # Battery and switch stay below the drive, on the visible near corners.
    battery=box('battery','blue battery case',(-.067,-.072,.038),(.080,.048,.040),'battery')
    switch=box('switch','separate power switch',(.083,-.085,.034),(.048,.026,.032),'teal')
    box('switch','wide power rocker',(.083,-.085,.055),(.029,.012,.010),'orange')
    for key,center,span in [('battery',(-.067,-.072),.028),('switch',(.083,-.085),.018)]:
        for dx in (-span,span):
            x=center[0]+dx;y=center[1]-(.009 if key=='switch' else 0)
            tongue_depth=.006 if key=='switch' else .012
            cut(base,(x,y,.016),(.0094,tongue_depth+.0004,.0044))
            box(key,'integral mounting tongue',(x,y,.020),(.009,tongue_depth,.008),'ink')
            bore(base,(x,y,.009),.0016,.025)
            body=battery if key=='battery' else switch
            top=.0586 if key=='battery' else .0506
            bore(body,(x,y,.036),.0016,.060)
            bolt(key,'captive case screw',(x,y,(.012+top)/2),.0015,top-.012)
    # Each lead is retained by its source module and fits a literal keyed socket.
    a.line('battery','battery lead',[(-.027,-.072,.036),(-.008,-.089,.029),(.043,-.089,.029),(.056,-.085,.034)],.0018,'ink')
    box('battery','battery lead plug',(.058,-.085,.034),(.010,.011,.009),'orange')
    # The underside-open keyed receiver lets the switch lower over a
    # battery plug already present; a later battery plug also enters from X.
    cut(switch,(.059,-.085,.028),(.012,.0114,.022))
    a.line('switch','switch motor lead',[(.107,-.085,.034),(.114,-.085,.034),(.114,-.032,.030),(.114,.074,.030),(-.068,.078,.040)],.0018,'ink')
    box('switch','motor lead plug',(-.068,.079,.045),(.012,.013,.012),'orange')
    # Socket belongs to motor so it is visible before the plugged lead arrives.
    socket=box('motor','motor power socket',(-.068,.073,.045),(.018,.011,.018),'teal')
    cut(socket,(-.068,.077,.045),(.0124,.009,.0124))
    # One connected open fork. Short rear arcs steer the cord without a closed
    # eye that would obstruct its joiner; there is no hidden floating guide.
    box('fork','connected fork foot',(.040,-.057,.026),(.125,.025,.016),'birch')
    for sign in (-1,1):
        x=.040+sign*.060
        box('fork','fork side upright',(x,-.057,.092),(.014,.018,.132),'birch')
        box('fork','joined guide arm',(.040+sign*.050,-.050,.149),(.034,.026,.014),'teal')
        # The guide is a shallow rear saddle open towards the viewer.
        guide_x=.040+sign*.04605
        points=[(guide_x+.006*math.cos(t),-.079+.006*math.sin(t),.149)
                for t in [math.pi*j/32 for j in range(33)]]
        a.line('fork','open string guide saddle',points,.0018,'ink')
        for dx in (-.006,.006):
            a.line('fork','joined guide side support',[(guide_x+dx,-.079,.149),(guide_x+dx,-.061,.149)],.0018,'ink')
        screw_x=.040+sign*.040
        bore(base,(screw_x,-.057,.009),.0019,.030);bolt('fork','captive fork screw',(screw_x,-.057,.0207),depth=.028)
    cord=a.line('string','one ordinary continuous cord',string_path(),.0012,'ink')
    # Colour belongs to the cord's own surface, with no extra marker geometry.
    # The curve's U coordinate runs along equally spaced material points from
    # one real end, so these six dyed sections travel with the string itself.
    striped=S.material('ink').copy();striped.name='spinner cord with dyed bands'
    nodes=striped.node_tree.nodes;links=striped.node_tree.links
    uv=nodes.new('ShaderNodeTexCoord');axes=nodes.new('ShaderNodeSeparateXYZ')
    repeat=nodes.new('ShaderNodeMath');repeat.operation='MULTIPLY';repeat.inputs[1].default_value=6
    fraction=nodes.new('ShaderNodeMath');fraction.operation='FRACT'
    band=nodes.new('ShaderNodeMath');band.operation='LESS_THAN';band.inputs[1].default_value=.26
    colour=nodes.new('ShaderNodeMixRGB');colour.blend_type='MIX'
    colour.inputs[1].default_value=S.PALETTE['ink'];colour.inputs[2].default_value=S.PALETTE['paper']
    links.new(uv.outputs['UV'],axes.inputs[0]);links.new(axes.outputs['X'],repeat.inputs[0])
    links.new(repeat.outputs[0],fraction.inputs[0]);links.new(fraction.outputs[0],band.inputs[0])
    links.new(band.outputs[0],colour.inputs[0]);links.new(colour.outputs[0],nodes.get('Principled BSDF').inputs['Base Color'])
    core.surface(cord,striped)
    joiner=S.empty('moving string joiner');joiner.parent=a.root
    # One soft split sleeve follows the joined string ends. Its annular wall,
    # open seam and 40 mm length remain real geometry in every motion pose.
    # The profile rises only 2 mm above the cord, tapering at both ends.
    rings=33;around=12;verts=[(0,0,0)]*(rings*around*2);faces=[]
    for side in range(2):
        offset=side*rings*around
        for j in range(rings-1):
            for k in range(around-1):
                u=offset+j*around+k;v=u+around
                faces.append((u,u+1,v+1,v) if side==0 else (u,v,v+1,u+1))
    for j in (0,rings-1):
        for k in range(around-1):
            u=j*around+k;v=rings*around+u
            faces.append((u,v,v+1,u+1))
    for k in (0,around-1):
        for j in range(rings-1):
            u=j*around+k;v=u+around
            faces.append((u,v,v+rings*around,u+rings*around))
    sleeve_mesh=bpy.data.meshes.new('one flexible split joining sleeve')
    sleeve_mesh.from_pydata(verts,[],faces);sleeve_mesh.update()
    sleeve=bpy.data.objects.new('soft string joining sleeve',sleeve_mesh)
    bpy.context.collection.objects.link(sleeve);sleeve.data.materials.append(S.material('orange'));a.add('joiner',sleeve,joiner)
    model=a.result(motor=motor,driven=driven,cord=cord,joiner=joiner,joiner_mesh=sleeve_mesh,
                   wheel_radius=WHEEL_RADIUS,motor_radius=MOTOR_RADIUS,driven_radius=DRIVEN_RADIUS)
    set_motion(model,0)
    bpy.context.view_layer.update();return model


def set_motion(model,phase=0.,travel=None):
    """One seamless visual period in radians, with one actual string lap.

    One period gives three pink-wheel turns and eight motor turns. The sleeve
    bends with the string and its thickness makes a small local lift over the
    wheel, preserving the floor clearance. This is a prescribed flexible pose,
    not a material or traction simulation. Optional `travel` is in metres.
    """
    import bisect
    import bpy
    from mathutils import Vector
    from middle.views import curve_points
    points=string_path(phase);target=6*math.pi*WHEEL_RADIUS
    travelled=target*phase/(2*math.pi) if travel is None else travel
    fraction=(.18+travelled/target)%1
    def radius_at(distance):
        return .00145+.00175*(1+math.cos(math.pi*distance/.020))/2
    # Arc-length lookup is reused for physical motion and the sleeve's sweep.
    def lookup(path):
        values=[0.]
        for a,b in zip(path,path[1:]):values.append(values[-1]+math.dist(a,b))
        return values
    def sample(path,distances,distance):
        distance%=distances[-1];index=min(len(path)-2,bisect.bisect_right(distances,distance)-1)
        a,b=path[index],path[index+1];f=(distance-distances[index])/max(1e-12,distances[index+1]-distances[index])
        return Vector(tuple(a[i]+f*(b[i]-a[i]) for i in range(3))),Vector(b)-Vector(a),index
    original=lookup(points)
    for index in range(len(points)):
        x,y,z=points[index]
        distance=(original[index]-fraction*target+target/2)%target-target/2
        extent=abs(distance)
        if extent<.024:
            # Ends taper back onto the bare cord, so there is no rigid jump.
            if extent<=.020:raise_by=radius_at(distance)-.0012
            else:raise_by=.00025*(1+math.cos(math.pi*(extent-.020)/.004))/2
            radius=math.hypot(x-WHEEL_CENTER[0],z-WHEEL_CENTER[2])
            factor=max(1.,(WHEEL_RADIUS+raise_by+.00016)/radius)
            points[index]=(WHEEL_CENTER[0]+(x-WHEEL_CENTER[0])*factor,y,WHEEL_CENTER[2]+(z-WHEEL_CENTER[2])*factor)
    # Correct the free arch to retain a constant total loop length. The lower
    # contact shape and both tangent exits remain fixed by that correction.
    def length_at(factor):
        adjusted=[(x,y,WHEEL_CENTER[2]+(z-WHEEL_CENTER[2])*factor if j<160 else z)
                  for j,(x,y,z) in enumerate(points)]
        return sum(math.dist(a,b) for a,b in zip(adjusted,adjusted[1:])),adjusted
    lo,hi=.97,1.03
    for _ in range(30):
        factor=(lo+hi)/2;length,adjusted=length_at(factor)
        if length>target:hi=factor
        else:lo=factor
    _,points=length_at((lo+hi)/2);distances=lookup(points)
    position,direction,cut_index=sample(points,distances,fraction*target)
    tangent=direction.normalized()
    # The sleeve bridges an 8 mm gap between the actual string ends. Supplied
    # string and joined loop use precisely the same visible centreline.
    start=fraction*target
    # Equal material intervals keep the curve's longitudinal UV coordinate
    # proportional to real cord length, including while its sleeve circulates.
    joined=[tuple(sample(points,distances,start+.004+(target-.008)*j/768)[0]) for j in range(769)]
    curve_points(model['cord'],joined)
    model['joiner'].location=position;model['joiner'].rotation_euler=(0,0,0)
    vertices=[];rings=33;around=12
    for side in range(2):
        for j in range(rings):
            offset=-.020+.040*j/(rings-1)
            center,direction,_=sample(points,distances,fraction*target+offset)
            tangent=direction.normalized();u=Vector((0,1,0));u=(u-tangent*u.dot(tangent)).normalized();v=tangent.cross(u).normalized()
            radius=radius_at(offset) if side==0 else .00125
            # Keep a narrow actual split along the sleeve's forward side.
            for k in range(around):
                angle=.12+(2*math.pi-.24)*k/(around-1)
                vertices.append(center-position+radius*(u*math.cos(angle)+v*math.sin(angle)))
    for vertex,co in zip(model['joiner_mesh'].vertices,vertices):vertex.co=co
    model['joiner_mesh'].update()
    angle=travelled/WHEEL_RADIUS
    model['driven'].rotation_euler.y=-angle
    model['motor'].rotation_euler.y=-angle*DRIVEN_RADIUS/MOTOR_RADIUS
    bpy.context.view_layer.update()
    return dict(length=target,travel=travelled,driven_angle=-angle,motor_angle=-angle*DRIVEN_RADIUS/MOTOR_RADIUS)


def stage(model,identity):
    import bpy
    import core
    from middle.views import stage_view,curve_points
    info=PLAN[identity];set_motion(model,0)
    view=stage_view(model,PLAN,identity,direction=(.48,-1,.58))
    group=info['group']
    if group in {'spinner-drive','spinner-assembly'}:
        view=core.frame((0,-.020,.080),.37,(.35,-1,.64))
    elif group=='spinner-finished':
        view=core.frame((.030,-.018,.170),.47,(.36,-1,.42))
    elif identity in {'sp-string','sp-string-loop'}:
        view=core.frame((.040,-.079,.195),.40,(.10,-1,.18))
    bpy.context.view_layer.update();return view


def markdown():
    text=A.markdown()
    for reference,name in [('sp-drive-ready','Drive'),('ribbon-spinner','String spinner')]:
        text=text.replace('reference: ![Build reference](assets/items/'+reference+'.webp)',
                          'reference: !['+name+'](assets/items/'+reference+'.webp)')
    return text.replace('(center 130px, 216px)','(center 390px, 216px)')


if __name__=='__main__':
    Path(__file__).with_suffix('.md').write_text(markdown())
    print(f'Spinner: {len(PLAN)} pictures; {len(A.recipes)} recipes; 13 actions in two chapters.')
