"""Tabletop pneumatic claw: a 230×140 mm palm and the retained honest linkage.

The archived prototype's jaw pivots, 52 mm links, guide stroke and layer heights
are unchanged. The long handle is replaced by a broad prepared base. Its input
syringe is handheld beside the base and connected by one short U-shaped hose.
The displayed input motion is an illustrative displacement allowance, not an
air-pressure/force solution. No fruit, testing prop or 'air' ingredient is used.
"""
from pathlib import Path
import math
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from middle.routes import Route
R=Route()
def item(i,n,p,g=None,s=110,e=''):return R.item(i,n,p,g,s,e)
item('cl-base','Palm',['base'],'cl-mechanism',240,e='A broad prepared palm with pivot holes and a fixed return-band hook. The jaws reach just beyond its front edge.')
parts=[(1,'jaw-1','Left jaw'),(2,'jaw-2','Right jaw'),(4,'slider','Slider'),(8,'link-1','Link'),(16,'link-2','Link'),(32,'pad-1','Pad'),(64,'pad-2','Pad')]
for bit,part,name in parts:
    e={'jaw-1':'A single jaw with captive pivot and link pins. Its left-facing shape matches the left side of the palm.', 'jaw-2':'The reflected right jaw has its own captive pins.', 'slider':'One retained sliding shoe inside its guide, including travel stops and the moving return-band hook.', 'link-1':'A rigid 52 mm link with split eyes that snap sideways onto the captive pins. Either link fits either side.', 'link-2':'A rigid 52 mm link with split eyes. Either link fits either side.', 'pad-1':'One soft pad for the inside face of a jaw. Either pad fits either jaw.', 'pad-2':'One soft pad. Either pad fits either jaw.'}[part]
    item('cl-'+part,name,[part if part not in ('link-2','pad-2') else part[:-1]+'1'],s=160 if part.startswith('jaw') else 120,e=e)
def valid(mask):
    return (not mask&8 or mask&5==5) and (not mask&16 or mask&6==6) and (not mask&32 or mask&1) and (not mask&64 or mask&2)
states={mask:('cl-base' if not mask else 'cl-mechanical' if mask==127 else 'cl-mech-'+str(mask)) for mask in range(128) if valid(mask)}
for mask,i in states.items():
    if mask:item(i,'Claw',['base']+[p for b,p,_ in parts if mask&b],'cl-mechanism',240)
recipes=[]
for mask,i in states.items():
    for bit,part,name in parts:
        if not mask&bit and valid(mask|bit):
            supplies=['cl-'+part] if bit not in (8,16,32,64) else ['cl-link-1','cl-link-2'] if bit in (8,16) else ['cl-pad-1','cl-pad-2']
            recipes += [(i,supply,states[mask|bit]) for supply in supplies]
# Identical links/pads fill the near available mounting place first when both
# places are empty. Either physical supply fits either side. Preparing either
# jaw/guide first and fitting pads before or after the links stay legal.
unique={}
for a,b,c in recipes:unique.setdefault((a,b),c)
recipes=[(a,b,c) for (a,b),c in unique.items()]
first=list(R.items)
goals=[('Fit the left jaw',1),('Fit the right jaw',2),('Fit the slider',4),('Snap a link onto the left pins',8),('Fit the other link',16),('Fit a pad to the left jaw',32),('Fit the other pad',64)]
R.page('c-claw-jaws','A small claw','cl-mechanical',first,[(text,[states[m] for m in states if m&bit]) for text,bit in goals],recipes)
for part,name,e in [
    ('output','Output syringe','A prepared needleless syringe. Its rigid piston and stem move inside a real hollow barrel.'),
    ('rear-cup','Cup','Either identical cup fits either barrel seat. Slide the first over the nozzle to the farther seat, then slide the other onto the nearer seat. Each has a soft retaining strap and captive mounting pins.'),
    ('front-cup','Cup','Either identical cup fits either barrel seat. Slide the first over the nozzle to the farther seat, then slide the other onto the nearer seat. Each has a soft retaining strap and captive mounting pins.'),
    ('clip','Plunger clip','A connected clip that plugs into the slider and captures the syringe thumb flange.'),
    ('band','Return band','One soft elastic loop. Its two hook brackets are already attached to the palm and slider.'),
    ('input','Hand syringe','A second prepared needleless syringe. It stays beside the claw, joined by the flexible hose.'),
    ('tube','Air hose','One continuous flexible hose with an open end for each syringe nozzle.'),
]:item('cl-'+part,name,[part],s=165 if part in ('output','input','tube') else 110,e=e)
# The supplies are copies of one prepared module. Item identity never chooses
# a hidden mounting position: the first cup always occupies the farther seat.
for identity in ('cl-front-cup','cl-rear-cup'):
    R.plan[identity].update(parts=['front-cup'],group='cl-cup')
cups={0:'cl-output',2:'cl-front-supported',3:'cl-supported-output'}
for mask,i in cups.items():
    if mask:item(i,'Syringe',['output']+(['rear-cup'] if mask&1 else [])+(['front-cup'] if mask&2 else []),'cl-syringe',200)
recipes=[(before,supply,after) for before,after in [('cl-output','cl-front-supported'),('cl-front-supported','cl-supported-output')] for supply in ('cl-front-cup','cl-rear-cup')]
mounted={m:('cl-mechanical' if m==0 else 'cl-air-'+str(m)) for m in range(8) if not m&2 or m&1}
for mask,i in mounted.items():
    if mask:item(i,'Claw',R.plan['cl-mechanical']['parts']+(['clip'] if mask&1 else [])+(['output','rear-cup','front-cup'] if mask&2 else [])+(['band'] if mask&4 else []),'cl-powered',270)
for mask,i in mounted.items():
    for bit,part in [(1,'cl-clip'),(2,'cl-supported-output'),(4,'cl-band')]:
        if not mask&bit and mask|bit in mounted:recipes.append((i,part,mounted[mask|bit]))
item('cl-controller','Hand syringe',['input','tube'],'cl-control',190)
item('pneumatic-claw','Pneumatic claw',R.plan[mounted[7]]['parts']+['input','tube'],'cl-finished',345,e='Pushing the hand syringe moves air through the hose into the output syringe. The output plunger moves the slider; the two rigid links turn the jaws. The elastic loop opens them as the plunger returns. The drawings show the available mechanism travel, not a measured grip force.')
recipes += [('cl-input','cl-tube','cl-controller'),(mounted[7],'cl-controller','pneumatic-claw')]
R.page('c-claw-air','Syringes and a hose','pneumatic-claw',[i for i in R.items if i not in first],[('Slide either cup to the farther seat',['cl-front-supported','cl-supported-output']),('Fit the other cup behind it','cl-supported-output'),('Fit the plunger clip',[mounted[m] for m in mounted if m&1]),('Fit the syringe into the claw',[mounted[m] for m in mounted if m&2]),('Loop the return band over its hooks',[mounted[m] for m in mounted if m&4]),('Push the hose onto the hand syringe','cl-controller'),('Connect the hose to the claw','pneumatic-claw')],recipes)
PLAN=R.plan


def legacy():
    root=next(p for p in Path(__file__).resolve().parents if (p/'src/story/parser.ts').is_file())
    path=str(root/'archive/2026.11.07 builder study/art')
    if path not in sys.path:sys.path.insert(0,path)
    import pneumatic_grabber
    return pneumatic_grabber


def dimensions():
    return legacy().Dimensions(beam_back=-.195,beam_front=.035,beam_width=.140,control_barrel_back=-.175,control_y=-.095)


def tube_path(d):
    start=(d.output_barrel_back-.004,0,d.syringe_axis_z)
    end=(d.control_barrel_back-.004,d.control_y,d.syringe_axis_z)
    # Tangents leave both nozzles toward -X; no line passes through the barrel.
    controls=(start,(start[0]-.055,0,start[2]),(end[0]-.055,end[1],end[2]),end)
    bezier=legacy()._bezier
    return [bezier(controls,j/96) for j in range(97)]


def build():
    import bpy
    import core
    old=legacy();S=core.S;d=dimensions();m=old.build_model(d)
    root=S.empty('compact tabletop pneumatic claw')
    deleted=set()
    for obj in m['objects']:
        if obj.name=='handgrip sleeve' or obj.get('part_id')=='air-tube-clips':
            deleted.add(obj);bpy.data.objects.remove(obj,do_unlink=True)
    m['objects']=[o for o in m['objects'] if o not in deleted]
    owned={}
    def assign(obj,key):
        obj['part_id']=key;owned.setdefault(key,[]).append(obj)
        if obj.parent is None:obj.parent=root
    def cut_box(obj,center,size,parent=None):
        cutter=S.box('prepared receiving pocket',center,size);cutter.parent=parent
        bpy.context.view_layer.update()
        bpy.context.view_layer.objects.active=obj;mod=obj.modifiers.new('actual receiving pocket','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    def side(obj):
        if obj in m['jaws'] or obj.parent in m['jaws']:
            return 1+(m['jaws'].index(obj if obj in m['jaws'] else obj.parent))
        return 2 if ' -1' in obj.name else 1
    cup_positions=[d.output_barrel_back+.012,d.output_barrel_front-.012]
    for obj in m['objects']:
        key=obj.get('part_id');name=obj.name
        if key=='air-beam':key='base'
        elif key=='air-jaws':key='jaw-'+str(side(obj))
        elif key=='air-slider':key='slider'
        elif key=='air-links':
            if obj in m['links'] or obj.parent in m['links']:
                key='link-'+str(1+m['links'].index(obj if obj in m['links'] else obj.parent))
            elif obj.parent in m['jaws']:key='jaw-'+str(side(obj))
            else:key='slider'
        elif key=='air-grip-pads':key='pad-'+str(side(obj))
        elif key=='air-output-syringe':key='output'
        elif key=='air-control-syringe':key='input'
        elif key=='air-cradle':
            key='clip' if obj.parent==m['slider'] else 'front-cup' if str(cup_positions[1]) in name else 'rear-cup'
        elif key=='air-return-band':key='band' if obj==m['band'] else 'slider' if obj.parent==m['slider'] else 'base'
        elif key=='air-tube':key='tube'
        else:raise ValueError((name,key))
        assign(obj,key)
    # Each supplied link is one rod with two split eyes. Captive pins stay with
    # the jaw/slider, so a loose link never smuggles in disconnected hardware.
    for index,link in enumerate(m['links'],1):
        key='link-'+str(index)
        eyes=[o for o in owned[key] if o.name.startswith('link eye')]
        for obj in eyes:
            center=obj.location.copy();owned[key].remove(obj);m['objects'].remove(obj);bpy.data.objects.remove(obj,do_unlink=True)
            ring=S.annulus('snap link eye '+str(index),(0,0,0),.0043,.0017,d.link_thickness,'orange',samples=48,gap=2*math.pi/3)
            # Mirror the same link on the far side. Both split mouths open
            # inward, allowing an outward approach that
            # clears the prepared return-hook bracket and its overhead arms.
            # At the open pose the far link can withdraw 15 mm along its local
            # +Y, move 21 mm forward in world X, then rise above the bracket.
            # Its mouth tips need 2.5 degrees of temporary flex each to admit
            # the 3 mm pins; this models clearance, not validated snap stress.
            angle=math.radians(-90 if index==1 else 90)
            ring.rotation_euler=(math.pi/2,0,angle);ring.location=center;ring.parent=link;assign(ring,key);m['objects'].append(ring)
    # Add a bonded strap to the front cup too: both cup-on-syringe stages are
    # retained connected subassemblies before they are mounted on the palm.
    # Both copies match under translation. During insertion their soft straps
    # can open radially by 0.65 mm, with the bonded endpoints fixed, to pass
    # the raised scale strokes. The assembled geometry is the relaxed pose;
    # this clearance allowance is not a validated elastic-force model.
    x=cup_positions[1]+.0033
    points=[(x,.0112,.040)]+[(x,.0112*math.cos(t),d.syringe_axis_z+.0112*math.sin(t)) for t in [math.pi*j/32 for j in range(33)]]+[(x,-.0112,.040)]
    strap=S.stroke('front cup integral retaining strap',points,.0012,'orange');assign(strap,'front-cup');m['objects'].append(strap)
    # A rear bridge and two offset feet enter vertically. The central return
    # hook, crosshead bosses and link pins all retain their original clear space.
    for obj in list(owned['clip']):
        if obj.name in ('plunger clip bridge to crosshead','plunger clip central support'):
            owned['clip'].remove(obj);m['objects'].remove(obj);bpy.data.objects.remove(obj,do_unlink=True)
    def clip_box(name,center,size):
        obj=S.box(name,center,size,color='teal');obj.parent=m['slider'];assign(obj,'clip');m['objects'].append(obj);return obj
    clip_box('plunger clip rear bridge',(-.0135,0,.0352),(.007,.029,.0014))
    shoe=next(o for o in owned['slider'] if o.name=='captured sliding shoe')
    for sign in (1,-1):
        clip_box('plunger clip offset arm '+str(sign),(-.010,sign*.006,.0352),(.008,.0025,.0014))
        clip_box('plunger clip locating foot '+str(sign),(-.0065,sign*.006,.031),(.0025,.0025,.008))
        cut_box(shoe,(-.0065,sign*.006,.031),(.0027,.0027,.0084),m['slider'])
    # Route the prepared return-hook bracket around, rather than over, the
    # clip's vertical insertion corridor. Its band anchor stays in place.
    upright=next(o for o in owned['slider'] if o.name=='moving return hook central upright')
    upright.location.x=.006
    overhead=next(o for o in owned['slider'] if o.name=='moving return hook overhead arm')
    owned['slider'].remove(overhead);m['objects'].remove(overhead);bpy.data.objects.remove(overhead,do_unlink=True)
    for name,center,size in [
        ('moving return hook forward bridge',(.006,d.band_y/2,.047),(.006,d.band_y+.006,.004)),
        ('moving return hook outside bridge',(0,d.band_y,.047),(.018,.006,.004)),
    ]:
        obj=S.box(name,center,size,color='teal');obj.parent=m['slider'];assign(obj,'slider');m['objects'].append(obj)
    # Prepared jaw pockets receive the full pad thickness without burying soft
    # material in wood. They remain open toward each jaw's gripping face.
    for sign,jaw in zip((1,-1),m['jaws']):
        wood=next(o for o in owned['jaw-'+str(1+(sign<0))] if o.name.startswith('crab jaw'))
        cut_box(wood,(.084,-sign*.012,0),(.014,.004,.012),jaw)
    # The old narrow beam left air below the jaw bridge. The new broad palm
    # needs actual pivot holes and underside recesses for the retained heads.
    palm=next(o for o in owned['base'] if o.name=='grabber beam')
    for sign in (1,-1):
        S.bore(palm,(0,sign*d.pivot_half_spacing,.007),.0021,.030,'Z')
        S.bore(palm,(0,sign*d.pivot_half_spacing,.004),.0030,.014,'Z')
    # Prepared jaw pivots and guide/cup fasteners snap through their receiving
    # holes. A closed flange could not pass: model the split stem and tapered
    # head explicitly. Elastic insertion is not a measured material claim.
    bpy.context.view_layer.update()
    families=[('jaw pivot lower retaining head','captive jaw pivot',.0021,.0027,.023),
              ('guide lower retaining flange','guide captive clip shank',.00135,.00175,.012),
              ('cradle lower retaining head','cradle captive fastener shaft',.0011,.0015,.016)]
    for prefix,shaft_prefix,hole_radius,outer_radius,split_root in families:
        for head in [o for o in m['objects'] if o.name.startswith(prefix)]:
            key=head['part_id'];x,y,z=head.location
            shaft=next(o for o in m['objects'] if o.name.startswith(shaft_prefix) and abs(o.location.x-x)<1e-8 and abs(o.location.y-y)<1e-8)
            shoulder=z+head.dimensions.z/2-.0002;tip=shoulder-.0035
            bpy.ops.mesh.primitive_cone_add(vertices=48,radius1=hole_radius*.65,radius2=outer_radius,depth=shoulder-tip,location=(x,y,(tip+shoulder)/2))
            new=bpy.context.object;new.name=prefix+' tapered snap';new.data.materials.append(S.material('ink'));assign(new,key)
            # The unsplit transverse direction must already clear its bore.
            # Only the X barbs require flexing toward the central slit.
            new.scale.y=(hole_radius-.0002)/outer_radius
            bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
            owned[key].remove(head);m['objects'].remove(head);m['objects'].append(new)
            m['retainers']=[(new,receiver,r,outer_radius) if old_head==head else (old_head,receiver,r,outer) for old_head,receiver,r,outer in m['retainers']]
            m['guide_fasteners']=[new if o==head else o for o in m['guide_fasteners']]
            bpy.data.objects.remove(head,do_unlink=True)
            slit=2*(outer_radius-hole_radius)+.0002
            for obj in (shaft,new):
                cutter=S.box('temporary snap split',(x,y,(tip-.001+split_root)/2),(slit,.010,split_root-tip+.001))
                cutter.parent=obj.parent
                bpy.context.view_layer.objects.active=obj;mod=obj.modifiers.new('open flexible snap prongs','BOOLEAN');mod.object=cutter;mod.operation='DIFFERENCE';bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    from middle.views import curve_points
    hose=next(o for o in owned['tube'] if o.type=='CURVE');curve_points(hose,tube_path(d))
    # Dark rubber separates the actual return loop from the pale wooden palm
    # and the orange linkage/straps at the powered workpiece's display size.
    core.surface(m['band'],S.material('ink'))
    model={**m,'root':root,'parts':owned,'tube':hose}
    apply_pose(model,0)
    bpy.context.view_layer.update();return model


def apply_pose(model,stroke):
    """Move intact rigid parts through the original non-toggle linkage branch."""
    return legacy().apply_pose(model,stroke)


def stage(model,identity):
    from middle.views import stage_view
    if identity not in PLAN:raise KeyError(identity)
    apply_pose(model,0)
    if PLAN[identity]['group']=='cl-powered':
        # The return loop lies on +Y. View that side so fitting the real loop
        # remains visible beside the opaque thumb plate and return bracket.
        return stage_view(model,PLAN,identity,direction=(.70,.9,1.75),roll=.3)
    return stage_view(model,PLAN,identity,direction=(.70,-.9,1.25),roll=-.3)


if __name__=='__main__':R.write(__file__)
