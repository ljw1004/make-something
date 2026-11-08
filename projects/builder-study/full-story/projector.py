"""One reusable 180 × 130 × 130 mm star projector, including its real optics.

The independent lid and connected U liner replace the old disconnected supply
presentation. The grooved handwheel is retained when the same toy is motorized.
"""
from pathlib import Path
from late.common import Author, geometry, visible, inspection

A=Author()
I=lambda identity,name,parts,group='projector-loose',css=110,**kw:A.item(identity,name,parts,group,css,**kw)
for identity,name,key,note in [
    ('pj-box','Box','box','An open prepared box with two upward-opening bearing cradles. Prepared loading slots let the complete star wheel lower into them; the lid closes those slots and retains the shaft.'),
    ('pj-liner','Reflector','liner','One folded U-shaped reflector joins its floor and side faces. It leaves the electrical contacts clear.'),
    ('pj-lamp','Lamp','lamp','A cool-running diffused LED module, holder, current-limiting resistor and attached lead.'),
    ('pj-battery','Battery pack','battery','An enclosed compatible switched low-voltage pack with its connected holder and fused lead. Connect with the switch off.'),
    ('pj-card','Card disc','blank','The flat-sided centre hole matches the spindle.'),
    ('pj-spindle','Spindle','spindle','The flat continues from the free front end to the disc seat. Slide the disc along it until it reaches the fixed rear shoulder. The two rear flanges locate the shaft in its bearing.'),
    ('pj-collar','Disc collar','collar','Slide this flat-sided collar along the same free end, then tighten its captive screw against the shaft flat. It holds the disc against the fixed shoulder.'),
    ('pj-lens','Lens','lens','A single convex lens forms an inverted image of the lit holes.'),
    ('pj-holder','Lens holder','holder','A connected sliding carriage retained on its rails. Move it along the rails to focus.'),
    ('pj-hood','Hood','hood','The dark tube surrounds the lens without covering its clear aperture.'),
    ('pj-handle','Handle','handle','The handwheel has a real belt groove behind its grip. It can be turned by hand now and driven by a belt later.'),
    ('pj-lid','Lid','lid','One connected lid with locating tabs, shaft retainers and two downward tongues. The inner tongue carries the real projection window. Fit the lid before the external lens rails, which pass through its prepared openings.'),
]: I(identity,name,[key],css=210 if key=='box' else 115,group='projector-open' if key=='box' else 'projector-loose',note=note)
A.plan['pj-card'].update(group='projector-disc',css=155)
I('pj-stars','Star disc',['stars'],'projector-disc',155)
A.process('pj-card','pj-punch','pj-stars')
I('pj-disc-shaft','Star wheel',['stars','spindle'],'projector-wheel',185)
A.add('pj-stars','pj-spindle','pj-disc-shaft')
I('pj-wheel','Star wheel',['stars','spindle','collar'],'projector-wheel',185)
A.add('pj-collar','pj-disc-shaft','pj-wheel')
states=[('pj-lined','pj-box','pj-liner',['box','liner']),
        ('pj-loaded','pj-lined','pj-wheel',['box','liner','stars','spindle','collar']),
        ('pj-lamped','pj-loaded','pj-lamp',['box','liner','stars','spindle','collar','lamp']),
        ('pj-wheel-box','pj-lamped','pj-battery',['box','liner','stars','spindle','collar','lamp','battery'])]
for identity,owner,part,keys in states:
    I(identity,'Projector',keys,'projector-open',210);A.add(part,owner,identity)
I('pj-focus','Lens holder',['lens','holder'],'projector-lens',150)
A.add('pj-lens','pj-holder','pj-focus')
base=A.plan['pj-wheel-box']['parts']
I('pj-closed','Projector',base+['lid'],'projector-work',210)
A.add('pj-lid','pj-wheel-box','pj-closed')
base=base+['lid']
for identity,owner,part,keys in [
    ('pj-focused','pj-closed','pj-focus',base+['lens','holder']),
    ('pj-hooded','pj-focused','pj-hood',base+['lens','holder','hood']),
    ('star-projector','pj-hooded','pj-handle',base+['lens','holder','hood','handle']),
]:
    I(identity,'Star projector' if identity=='star-projector' else 'Projector',keys,
      'projector-finished' if identity=='star-projector' else 'projector-work',340 if identity=='star-projector' else 210,
      note='Turning the disc brings new holes past the fixed aperture. Sliding the lens brings their projected image into focus. The optical model uses one ideal thin lens; brightness and real component tolerances are not measured.' if identity=='star-projector' else '')
    A.add(part,owner,identity)
A.page('c-projector-box','A box of stars','pj-wheel-box',
       ['pj-box','pj-liner','pj-lamp','pj-battery','pj-card','pj-spindle','pj-collar'],
       ['pj-lined','pj-loaded','pj-lamped','pj-stars','pj-disc-shaft','pj-wheel','pj-wheel-box'],
       [('Fit the reflector inside the box','pj-lined'),('Punch stars around the disc','pj-stars'),
        ('Slide the disc onto the spindle','pj-disc-shaft'),('Fit the disc collar','pj-wheel'),
        ('Lower the star wheel into the bearings','pj-loaded'),('Fit the lamp','pj-lamped'),
        ('Connect the battery pack','pj-wheel-box')],
       [('pj-punch','Punch','punch')])
A.page('c-projector-lens','Bring the stars into focus','star-projector',
       ['pj-lens','pj-holder','pj-hood','pj-handle','pj-lid'],
       ['pj-closed','pj-focus','pj-focused','pj-hooded','star-projector'],
       [('Close the box with its lid','pj-closed'),('Fit the lens into its holder','pj-focus'),
        ('Fit the holder to the box','pj-focused'),('Fit the hood around the lens','pj-hooded'),
        ('Fit the handle to the spindle','star-projector')])
PLAN=A.plan


def build():
    """The same factory is used without rescaling by carrier.build()."""
    import bpy
    S=geometry()
    import shadow_theatre as T
    model=T.build_model()
    # Keep the opaque card distinct from the opaque black baffle behind it,
    # so its punched holes remain readable in the high construction view.
    card_material=S.material('ink').copy();card_material.name='opaque charcoal projector card'
    card_material.diffuse_color=(.16,.17,.15,1)
    card_material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.16,.17,.15,1)
    for disc in [model['disc'],model['blank_disc']]:
        disc.data.materials.clear();disc.data.materials.append(card_material)
    # Diagram glass: real transparent coverage avoids the black-film refraction
    # artefact while the existing convex surface supplies its visible rim.
    lens_material=bpy.data.materials.new('clear pale diagram lens');lens_material.use_nodes=True
    nodes=lens_material.node_tree.nodes;nodes.clear();links=lens_material.node_tree.links
    output=nodes.new('ShaderNodeOutputMaterial');mix=nodes.new('ShaderNodeMixShader')
    transparent=nodes.new('ShaderNodeBsdfTransparent')
    surface=nodes.new('ShaderNodeBsdfPrincipled')
    surface.inputs['Base Color'].default_value=(.48,.72,.78,1)
    surface.inputs['Roughness'].default_value=.16
    surface.inputs['IOR'].default_value=1.49
    fresnel=nodes.new('ShaderNodeFresnel');fresnel.inputs['IOR'].default_value=1.49
    opacity=nodes.new('ShaderNodeMath');opacity.operation='MULTIPLY_ADD';opacity.inputs[1].default_value=.55;opacity.inputs[2].default_value=.10
    links.new(fresnel.outputs['Fac'],opacity.inputs[0]);links.new(opacity.outputs[0],mix.inputs[0])
    links.new(transparent.outputs[0],mix.inputs[1]);links.new(surface.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],output.inputs[0])
    lens_material.diffuse_color=(.48,.72,.78,.22)
    model['lens'].data.materials.clear();model['lens'].data.materials.append(lens_material)
    def cut(obj,cutter):
        bpy.context.view_layer.objects.active=obj
        mod=obj.modifiers.new('actual receiving clearance','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
        bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    def add(key,obj,parent=None):
        obj.parent=parent or model['root'];parts.setdefault(key,[]).append(obj);return obj
    original=model['parts'];parts={}
    for new,old in [('lamp','theatre-lamp'),('battery','theatre-power'),('blank','theatre-card'),
                    ('stars','theatre-stars'),('spindle','theatre-spindle'),('lens','theatre-lens'),
                    ('holder','theatre-slider'),('hood','theatre-hood'),('handle','theatre-handwheel')]:
        parts[new]=list(original[old])
    parts['lid']=[o for o in original['theatre-box'] if o.name.startswith('removable box lid')]
    # A real 0.2 mm edge clearance lets the inset lid descend between the walls.
    parts['lid'][0].dimensions=(.1756,.1256,.002)
    parts['box']=[o for o in original['theatre-box'] if o not in parts['lid']]
    for obj in model['root'].children_recursive:
        if obj.type in {'MESH','CURVE','FONT'}:obj.hide_render=True;obj.hide_set(True)
    # The new spindle has no obstructing front bearing or flange. Both the
    # closed D-hole disc and its separate collar can slide on from the free end.
    # All original spindle meshes stay hidden; only its motion root is reused.
    parts['spindle']=[model['spindle']]
    shaft=S.cylinder('continuous-flat loading spindle',(0,-.0535,0),.003,.231,'ink','Y')
    cut(shaft,S.box('continuous spindle flat',(.0040,-.072,0),(.0036,.200,.014)))
    S.bore(shaft,(0,-.166,0),.0009,.014,'Z')
    add('spindle',shaft,model['spindle'])
    add('spindle',T.d_socket('fixed disc rear shoulder',(0,.0271,0),outer=.008,depth=.003,color='teal'),model['spindle'])
    for y in [.043,.057]:
        add('spindle',S.annulus('integral rear bearing locating flange',(0,y,0),.006,.003,.004,'orange'),model['spindle'])
    collar=T.d_socket('separate disc retaining collar',(0,.0229,0),outer=.008,depth=.003,color='teal')
    S.bore(collar,(.0052,.0229,0),.0011,.012,'X')
    add('collar',collar,model['spindle'])
    add('collar',S.cylinder('collar captive clamp screw',(.0046,.0229,0),.001,.0048,'ink','X'),model['spindle'])
    front=next(o for o in parts['box'] if o.name.startswith('prepared front wall'))
    rear=next(o for o in parts['box'] if o.name.startswith('rear wall and spindle'))
    baffle=next(o for o in parts['box'] if o.name.startswith('fixed black window'))
    cut(front,S.box('upward front shaft loading slot',(0,-.064,.095),(.0068,.012,.076)))
    cut(baffle,S.box('receiving slot for aperture tongue',(0,.020,.093),(.0204,.012,.082)))
    # The battery has a real side compartment beyond the aperture. The opening
    # does not approach the 12 × 8 mm optical window at the centre of the baffle.
    cut(baffle,S.box('battery compartment clearance',(.079,.020,.027),(.050,.012,.058)))
    for x in [-.010,.010]:S.bore(rear,(x,.064,T.DIMS.led_z),.0021,.012,'Y')
    for obj in parts['battery']:
        if obj.name.startswith('retained connector floor support') and abs(obj.location.x-.064)<.0001:obj.location.x=.068
    for y in [-.059,.050]:
        clip=S.annulus('upward opening shaft bearing',(0,0,0),.0052,.0033,.008,'teal',gap=2.4)
        clip.rotation_euler.y=-1.5707963267948966;clip.location=(0,y,.058);add('box',clip)
        add('box',S.box('bearing pedestal tied to wall',(0,y,.043),(.021,.012 if y<0 else .008,.020),'teal'))
        if y>0:add('box',S.box('rear pedestal low wall bridge',(0,.0555,.033),(.021,.019,.010),'teal'))
    # Opaque lid tongues descend through the loading slots, with genuine open
    # lower forks around the shaft. Their window is the original optical window.
    for y,width,key in [(-.0656,.040,'front'),(.020,.020,'aperture')]:
        tongue=S.box('lid '+key+' loading-slot tongue',(0,y,.091), (width,.001,.078),'card' if key=='front' else 'ink')
        S.bore(tongue,(0,y,.058),.0033,.008,'Y')
        cut(tongue,S.box('open lower shaft fork',(0,y,.053),(.0066,.008,.010)))
        if key=='aperture':
            cut(tongue,S.box('actual lid projection window',(0,y,T.DIMS.window_z),(.012,.008,.008)))
        else:
            S.bore(tongue,(0,y,.1152),.0122,.008,'Y')
            for x in [-.015,.015]:
                cut(tongue,S.box('front tongue rail passage',(x,y,.1122),(.0080,.008,.0122)))
        add('lid',tongue)
    add('lid',S.box('front tongue connected lid return',(0,-.0645,.131),(.040,.006,.002),'card'))
    # Side uprights leave a 32 mm optical opening. Only the low crossbar
    # crosses the centre line, 40 mm below the lamp/disc/lens ray bundle.
    for x in [-.018,.018]:
        add('lid',S.box('rear shaft retention side upright',(x,.050,.0955),(.004,.006,.067),'teal'))
    add('lid',S.box('low rear shaft retaining crossbar',(0,.050,.0635),(.040,.006,.003),'teal'))
    for x in [-.0865,.0865]:
        add('box',S.box('integral lid support ledge',(x,0,.1275),(.003,.124,.001),'card'))
    # The original bridge crossed the lens rim. The lower bridge and two narrow
    # side webs leave its complete 16 mm optical face and insertion cylinder free.
    old_mount_prefixes=('focus rail wall attachment foot','focus rail rear cantilever arm',
                        'focus rail rear support post','focus rail mounting screw')
    parts['holder']=[obj for obj in parts['holder'] if not obj.name.startswith(old_mount_prefixes)]
    for obj in parts['holder']:
        if obj.name.startswith('lens holder cross bridge'):obj.location.z=-.0145
    for x in [-.009,.009]:
        add('holder',S.box('lens ring to lower bridge web',(x,0,-.0083),(.002,.003,.013),'orange'),model['focus'])
    for x in [-.015,.015]:
        add('holder',S.box('lower bridge to guide cheek',(x,0,-.0105),(.004,.004,.007),'orange'),model['focus'])
        # Only the narrow rail/stop assembly passes through the prepared wall
        # opening. The real support frame and its screw heads remain outside.
        cut(front,S.box('full-travel lens rail passage',(x,-.064,.1122),(.0080,.012,.0122)))
        add('holder',S.box('retained rear focus-rail stop',(x,.024,-.003),(.006,.003,.006),'teal'),model['rails'][0].parent)
    for sign in [-1,1]:
        x=sign*.028
        foot=S.box('external lens frame mounting foot',(x,-.0676,.104),(.012,.0052,.010),'teal')
        S.bore(foot,(x,-.0676,.104),.0011,.012,'Y');add('holder',foot)
        S.bore(front,(x,-.064,.104),.0011,.012,'Y')
        add('holder',S.box('external focus-rail side arm',(sign*.023,-.0805,.110),(.006,.027,.006),'teal'))
        add('holder',S.box('external focus-rail front crossarm',(sign*.020,-.090,.112),(.013,.006,.006),'teal'))
        add('holder',S.cylinder('external lens mounting screw',(x,-.0656,.104),.001,.0112,'ink','Y'))
        add('holder',S.cylinder('accessible lens mounting screw head',(x,-.0712,.104),.002,.002,'orange','Y'))
    add('holder',S.annulus('lens holder front seating spigot',(0,-.00625,0),.0093,.0082,.0075,'teal'),model['focus'])
    parts['hood']=[]
    add('hood',S.annulus('clearance hood main tube',(0,-.0175,0),.0128,.0105,.015,'ink'),model['focus'])
    add('hood',S.annulus('hood receiving neck',(0,-.008,0),.011,.0095,.008,'ink'),model['focus'])
    add('hood',S.annulus('hood compliant socket lining',(0,-.007,0),.0095,.0093,.006,'ink'),model['focus'])
    # The supplied lamp's resistor sits on the same connected PCB extension.
    add('lamp',S.box('lamp PCB resistor extension',(.019,.059,.100),(.014,.005,.008),'teal'),model['lamp'])
    add('lamp',S.stroke('PCB resistor contact trace',[(.010,.0563,.099),(.020,.0563,.099)],.0004,'ink'),model['lamp'])
    # Three faces physically meet along their full edges: one folded sheet.
    parts['liner']=[]
    for name,centre,size in [('reflector floor',(-.0185,-.0202,.0024),(.137,.0776,.0006)),
                             ('reflector left side',(-.0867,-.0202,.064),(.0006,.0776,.124)),
                             ('reflector right side',(.0497,-.0202,.064),(.0006,.0776,.124))]:
        ob=S.box(name,centre,size,'paper')
        if name=='reflector floor':S.bore(ob,(-.060,-.045,.0024),.0056,.012,'Z')
        ob.parent=model['root'];parts['liner'].append(ob)
    # Locating lip is integral with the lid, not separate loose hardware.
    for x,y,sx,sy in [(-.0825,-.050,.002,.014),(.0825,-.050,.002,.014),(-.0825,.050,.002,.014),(.0825,.050,.002,.014)]:
        ob=S.box('lid integral locating lip',(x,y,.1265),(sx,sy,.005),'card');ob.parent=model['root'];parts['lid'].append(ob)
    # The original wheel rim forms the groove floor. Two connected flanges
    # retain the later 2 mm round belt clear of the front hand grip.
    for y in [-.182,-.174]:
        ob=S.annulus('handwheel belt-groove flange',(0,y,0),.025,.003,.0015,'orange')
        ob.parent=model['spindle'];parts['handle'].append(ob)
    for key,objects in parts.items():
        for obj in objects:obj['part_id']=key
    model['parts']=parts;model['_projector_source']=T
    return model


def pose(model,angle=0.,focus=0.):
    """Apply motion without changing visibility or an external mounting pose."""
    model['_projector_source'].apply_pose(model,angle,focus_offset=focus)


def stage(model,identity):
    info=PLAN[identity]
    model['root'].location=(0,0,0);model['root'].rotation_euler=(0,0,0)
    pose(model);visible(model,info['parts'])
    if info['group']=='projector-open':
        return dict(location=(.10,.18,1.10),target=(0,-.025,.065),scale=.36)
    if info['group'] in {'projector-work','projector-finished'}:
        return dict(location=(.38,-.60,.39),target=(0,-.045,.065),scale=.36)
    if identity in {'pj-card','pj-stars'}:
        return dict(location=(.10,-.875,.258),target=(0,.025,.058),scale=.174)
    if identity in {'pj-disc-shaft','pj-wheel'}:return inspection(model,(.10,-.9,.20))
    if identity=='pj-lens':return inspection(model,(.15,-.9,.25),minimum=.04)
    return inspection(model)


if __name__=='__main__':
    Path(__file__).with_suffix('.md').write_text(A.markdown())
    print(f'Projector: {len(PLAN)} images; {len(A.recipes)} recipes; two chapters.')
