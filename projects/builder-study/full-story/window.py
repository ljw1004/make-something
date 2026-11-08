"""An open wooden tabletop window with a 650 × 700 mm clear passage.

Dimensions use metres: opening x = ±.325, z = .105..805, frame plane y=.055.
The feet span .820 × .320 m. The pink base block is the sole fictional part;
ordinary feet, screwed joints, rear struts, wiring and controls remain literal.
No pane, image surface or decorative geometry occupies the clear passage.
"""
from pathlib import Path
import math
from late.common import Author

A = Author()
def item(identity, name, parts, group='window-loose', css=130, **pose):
    return A.item(identity, name, parts, group, css, **pose)

item('wn-base', 'Base', ['base'], 'window-foot', 255)
item('wn-foot-1', 'Left foot', ['foot-left'], css=165)
item('wn-foot-2', 'Right foot', ['foot-right'], css=165)
item('wn-one-foot', 'Base', ['base', 'foot-left'], 'window-foot', 255)
item('wn-right-foot', 'Base', ['base', 'foot-right'], 'window-foot', 255)
item('wn-two-feet', 'Base', ['base', 'foot-left', 'foot-right'], 'window-foot', 255)
A.add('wn-foot-1', 'wn-base', 'wn-one-foot')
A.add('wn-foot-2', 'wn-base', 'wn-right-foot')
A.add('wn-foot-2', 'wn-one-foot', 'wn-two-feet')
A.add('wn-foot-1', 'wn-right-foot', 'wn-two-feet')
for key, name, size in [('battery', 'Battery', 140), ('switch', 'Switch', 120),
                         ('block', 'Block', 145), ('sill', 'Sill', 180)]:
    item('wn-'+key, name, [key], css=size)
base = ['base', 'foot-left', 'foot-right']
ready = {0: 'wn-two-feet'}
for mask in range(1, 16):
    identity = 'wn-foot-ready' if mask == 15 else 'wn-fitted-'+str(mask)
    ready[mask] = identity
    item(identity, 'Window base', base+[p for bit,p in [(1,'battery'),(2,'switch'),(4,'block'),(8,'sill')] if mask&bit], 'window-foot', 255)
for mask, owner in ready.items():
    for bit, part in [(1,'battery'),(2,'switch'),(4,'block'),(8,'sill')]:
        if not mask&bit: A.add('wn-'+part, owner, ready[mask|bit])
first = list(A.items)
A.page('c-window-foot', 'A broad foot', 'wn-foot-ready',
       ['wn-base','wn-foot-1','wn-foot-2','wn-battery','wn-switch','wn-block','wn-sill'],
       [i for i in first if i not in ['wn-base','wn-foot-1','wn-foot-2','wn-battery','wn-switch','wn-block','wn-sill']],
       [('Fit a foot',['wn-one-foot','wn-right-foot']),('Fit the other foot','wn-two-feet'),
        ('Fit the battery',[ready[m] for m in ready if m&1]),
        ('Fit the switch',[ready[m] for m in ready if m&2]),
        ('Fit the block',[ready[m] for m in ready if m&4]),
        ('Fit the sill','wn-foot-ready')])
for n in (1,2):
    item(f'wn-upright-{n}', 'Upright', ['upright-left'], css=180)
    item(f'wn-strut-{n}', 'Strut', ['strut-left'], css=175, rear=True)
item('wn-top', 'Crossbar', ['top'], css=180)
item('wn-lead', 'Lead', ['lead'], css=175)
framebase = A.plan['wn-foot-ready']['parts']
for identity, parts in [('wn-one-upright',framebase+['upright-left']),
                        ('wn-uprights',framebase+['upright-left','upright-right']),
                        ('wn-frame',framebase+['upright-left','upright-right','top'])]:
    item(identity, 'Window', parts, 'window-frame', 275)
for n in (1,2):
    A.add(f'wn-upright-{n}', 'wn-foot-ready', 'wn-one-upright')
    A.add(f'wn-upright-{n}', 'wn-one-upright', 'wn-uprights')
A.add('wn-top','wn-uprights','wn-frame')
frame = A.plan['wn-frame']['parts']
item('wn-back', 'Window', frame, 'window-back', 275, rear=True)
item('wn-one-strut', 'Window', frame+['strut-left'], 'window-back', 275, rear=True)
item('wn-braced-back', 'Window', frame+['strut-left','strut-right'], 'window-back', 275, rear=True)
item('wn-braced', 'Window', frame+['strut-left','strut-right'], 'window-frame', 275)
item('open-window', 'Window', frame+['strut-left','strut-right','lead'], 'window-finished', 350)
A.process('wn-frame','wn-flip','wn-back')
for n in (1,2):
    A.add(f'wn-strut-{n}','wn-back','wn-one-strut')
    A.add(f'wn-strut-{n}','wn-one-strut','wn-braced-back')
A.process('wn-braced-back','wn-flip','wn-braced')
A.add('wn-lead','wn-braced','open-window')
second = [i for i in A.items if i not in first]
A.page('c-window-frame', 'An open frame', 'open-window',
       ['wn-upright-1','wn-upright-2','wn-top','wn-strut-1','wn-strut-2','wn-lead'],
       [i for i in second if i not in ['wn-upright-1','wn-upright-2','wn-top','wn-strut-1','wn-strut-2','wn-lead']],
       [('Fit an upright','wn-one-upright'),('Fit the other upright','wn-uprights'),
        ('Join them with the crossbar','wn-frame'),('Flip the window','wn-back'),
        ('Fit a strut','wn-one-strut'),('Fit the other strut','wn-braced-back'),
        ('Flip the window','wn-braced'),('Connect the lead','open-window')],
       [('wn-flip','Flip','flip')])
PLAN = A.plan
# Start the second page in its frame-building view, before the first upright
# lands. This render-only alias keeps that fitting's camera and scale stable.
PLAN['wn-base-carried'] = dict(PLAN['wn-foot-ready'], group='window-frame', css=275)
OPENING = dict(width=.650, height=.700, plane_y=.055, bottom=.105, top=.805)


def build():
    import bpy
    import core
    from mathutils import Vector
    S=core.S; a=core.Assembly('open tabletop window'); box=a.box; cyl=a.cylinder
    fasteners=[]
    def cut(obj, center, size):
        cutter=S.box('prepared receiving socket',center,size)
        bpy.context.view_layer.objects.active=obj
        mod=obj.modifiers.new('actual receiving socket','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
        bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    def bore(obj, center, radius, depth, axis='Z'): S.bore(obj,center,radius,depth,axis)
    def bar(part, name, start, end, width, color='birch'):
        delta=Vector(end)-Vector(start)
        obj=box(part,name,(Vector(start)+Vector(end))/2,(width,width,delta.length),color)
        obj.rotation_euler=delta.to_track_quat('Z','Y').to_euler();return obj
    def screw(part, name, center, radius=.0035, depth=.025, axis='Z'):
        # Connected captive fastening hardware belongs to the supplied component.
        core.bolt(a,part,name,center,radius,depth,axis)
    def captive_front(part,name,x,z,start,end,retraction,head_depth=.005):
        objects=[cyl(part,name+' shank',(x,(start+end)/2,z),.0035,end-start,'ink','Y'),
                 cyl(part,name+' head',(x,start-head_depth/2,z),.007,head_depth,'ink','Y')]
        fasteners.append(dict(part=part,objects=objects,offset=(0,-retraction,0),rest=[tuple(o.location) for o in objects]))
    def captive_other(part,name,center,depth,axis,offset):
        before=len(a.parts[part]);screw(part,name,center,.0035,depth,axis)
        objects=a.parts[part][before:]
        fasteners.append(dict(part=part,objects=objects,offset=offset,rest=[tuple(o.location) for o in objects]))
    board=box('base','wide wooden base',(0,0,.055),(.640,.270,.040),'birch')
    # Feet slide onto the board's prepared end tongues. All front screw heads
    # remain visible; neither foot needs an implicit underside turn.
    for side,sign in [('left',-1),('right',1)]:
        key='foot-'+side;x=sign*.360
        foot=box(key,'broad wooden stabilizing foot',(x,0,.0425),(.100,.320,.065),'birch')
        cut(foot,(sign*.315,0,.055),(.0508,.271,.0408))
        box(key,'foot front fastening plate',(x,-.163,.048),(.100,.006,.045),'teal')
        bore(board,(sign*.315,-.095,.055),.0036,.085,'Y')
        bore(foot,(sign*.315,-.1475,.055),.0036,.055,'Y')
        bore(a.parts[key][1],(sign*.315,-.163,.055),.0036,.015,'Y')
        captive_front(key,'captive front foot screw',sign*.315,.055,-.166,-.125,.025,.006)
    # The sill lowers into a shallow open rabbet across the board and feet.
    for receiver in [board,a.parts['foot-left'][0],a.parts['foot-right'][0]]:
        cut(receiver,(0,.055,.075),(.7404,.0804,.0204))
    sill=box('sill','lower frame rail',(0,.055,.085),(.740,.080,.040),'birch')
    for x in (-.26,.26):
        bore(board,(x,.055,.055),.0036,.050)
        bore(sill,(x,.055,.085),.0036,.060)
        screw('sill','captive sill screw',(x,.055,.0757),.0035,.0614)
    for side,sign in [('left',-1),('right',1)]:
        x=sign*.3475;key='upright-'+side
        cut(sill,(x,.055,.096),(.0266,.0406,.020))
        upright=box(key,'wooden frame upright',(x,.055,.455),(.045,.055,.700),'birch')
        lower=box(key,'integral lower tenon',(x,.055,.096),(.026,.040,.018),'birch')
        upper=box(key,'integral top tenon',(x,.055,.814),(.026,.040,.018),'birch')
        bore(lower,(x,.055,.096),.0036,.050,'Y')
        bore(upper,(x,.055,.814),.0036,.050,'Y')
        # A front pin retains the lower tenon; the head is a visible part of
        # the upright fitting, with a real through receiver in the sill.
        bore(sill,(x,.055,.096),.0036,.090,'Y')
        # The connected front bracket retains the withdrawn screw while the
        # tenon lowers into the sill. Its crossarm remains above the sill.
        box(key,'connected front pin bracket arm',(x,.019,.120),(.022,.026,.008),'teal')
        tab=box(key,'connected front pin retaining tab',(x,.008,.108),(.022,.004,.032),'teal')
        bore(tab,(x,.008,.096),.0036,.014,'Y')
        captive_front(key,'upright captive locking pin',x,.096,.006,.080,.066)
        bore(upright,(x,.055,.388),.0036,.065,'Y')
    top=box('top','upper crossbar',(0,.055,.8275),(.740,.080,.045),'birch')
    for sign in (-1,1):
        x=sign*.3475
        cut(top,(x,.055,.814),(.0266,.0406,.019))
        bore(top,(x,.055,.814),.0036,.100,'Y')
        captive_front('top','captive top locking pin',x,.814,.015,.080,.047)
    # The two rear struts are each one connected bar with attached mounting
    # shoes and captive screws. Their sockets can be approached from behind.
    for side,sign in [('left',-1),('right',1)]:
        key='strut-'+side;x=sign*.3475
        bar(key,'rear diagonal strut',(x,.139,.084),(x,.096,.370),.022,'teal')
        lower=box(key,'joined lower strut shoe',(x,.140,.084),(.050,.030,.018),'teal')
        upper=box(key,'joined upper strut shoe',(x,.090,.370),(.050,.015,.055),'teal')
        bore(lower,(x+.018,.140,.084),.0036,.040)
        bore(upper,(x,.090,.388),.0036,.040,'Y')
        # The foot sockets are behind the frame and visible only after Flip.
        foot=a.parts['foot-'+side][0]
        bore(foot,(x+.018,.140,.0425),.0036,.080)
        captive_other(key,'captive lower strut screw',(x+.018,.140,.0697),.0494,'Z',(0,0,.031))
        captive_other(key,'captive upper strut screw',(x,.07695,.388),.0439,'Y',(0,.030,0))
    # All electrical hardware is on the near side of the sill. The independent
    # battery, switch and pink block fit broad keyed sockets in the base.
    specs=[('battery',(-.075,-.080,.106),(.135,.080,.062),'battery'),
           ('switch',(-.230,-.080,.094),(.100,.080,.038),'teal'),
           ('block',(.160,-.080,.107),(.145,.080,.064),'future')]
    for key,center,size,color in specs:
        body=box(key,key+' case',center,size,color)
        spread=.40 if key=='switch' else .30
        for dx in (-size[0]*spread,size[0]*spread):
            x=center[0]+dx;y=center[1]
            cut(board,(x,y,.071),(.0146,.0206,.009))
            box(key,'integral keyed mounting tongue',(x,y,.074),(.014,.020,.012),'ink')
            bore(board,(x,y,.055),.0026,.050)
            bore(body,(x,y,center[2]),.0026,size[2]+.020)
            bottom=.065;top=center[2]+size[2]/2+.001
            screw(key,'captive case screw',(x,y,(bottom+top)/2),.0025,top-bottom)
        if key=='switch':
            box(key,'wide accessible power rocker',(-.230,-.082,.118),(.060,.045,.012),'orange')
    # Battery lead is a single connected part of its pack. It terminates in the
    # switch's side socket; the larger final lead connects switch to pink block.
    a.line('battery','attached battery lead',[(-.1425,-.080,.103),(-.161,-.080,.103),(-.171,-.080,.101)],.0025,'ink')
    box('battery','battery lead plug',(-.176,-.080,.101),(.012,.012,.010),'orange')
    switch=a.parts['switch'][0]
    cut(switch,(-.179,-.080,.101),(.014,.013,.011))
    cut(switch,(-.230,-.121,.095),(.014,.010,.014))
    module=a.parts['block'][0]
    cut(module,(.160,-.121,.104),(.014,.010,.014))
    a.line('lead','one flexible connected lead',[(-.230,-.123,.095),(-.230,-.146,.095),(-.160,-.150,.092),(.080,-.150,.092),(.160,-.146,.104),(.160,-.123,.104)],.003,'ink')
    for x,z in [(-.230,.095),(.160,.104)]:
        box('lead','connected keyed plug',(x,-.123,z),(.013,.014,.013),'orange')
        box('lead','plug grip',(x,-.137,z),(.022,.020,.022),'teal')
    model=a.result(opening=dict(OPENING),view_plane_y=.055,fasteners=fasteners)
    bpy.context.view_layer.update();return model


def stage(model,identity):
    import bpy
    import core
    from middle.views import stage_view
    info=PLAN[identity]
    # Loose parts show captive fasteners withdrawn along their real axes;
    # fitting seats the part and tightens only its own attached fasteners.
    for fastener in model['fasteners']:
        loose=info['parts']==[fastener['part']]
        for obj,rest in zip(fastener['objects'],fastener['rest']):
            obj.location=tuple(rest[i]+(fastener['offset'][i] if loose else 0) for i in range(3))
    # Shared cameras are determined in the canonical front orientation. Rear
    # groups explicitly turn the complete work, including supplied loose struts.
    view=stage_view(model,PLAN,identity,direction=(.40,-1.25,.58))
    if info.get('rear'): model['root'].rotation_euler.z=math.pi
    group=info['group']
    if group=='window-foot': view=core.frame((0,-.010,.087),1.03,(.28,-1.30,.90))
    elif group in {'window-frame','window-finished'}:
        view=core.frame((0,.030,.435),1.20,(.32,-1.35,.45))
    elif group=='window-back': view=core.frame((0,-.030,.435),1.20,(.32,-1.35,.45))
    elif info.get('rear'):
        objects=[obj for key in info['parts'] for obj in model['parts'][key]]
        bpy.context.view_layer.update();lo,hi=core.world_bounds(objects)
        view=core.frame(tuple((a+b)/2 for a,b in zip(lo,hi)),max(hi[i]-lo[i] for i in range(3))*1.55,(.32,-1.35,.45))
    bpy.context.view_layer.update();return view


def markdown():
    text=A.markdown()
    icon='  - icon: ![Window base](assets/items/wn-foot-ready.webp)\n'
    text=text.replace(icon,icon+'  - from chapter `c-window-frame` icon: ![Window base](assets/items/wn-base-carried.webp)\n')
    for page in A.pages:
        name='Window base' if page['reference']=='wn-foot-ready' else 'Window'
        text=text.replace('reference: ![Build reference](assets/items/'+page['reference']+'.webp)',
                          'reference: !['+name+'](assets/items/'+page['reference']+'.webp)')
    # This family has one actual process: centre it in the available middle slot.
    return text.replace('(center 130px, 216px)','(center 390px, 216px)')


if __name__=='__main__':
    Path(__file__).with_suffix('.md').write_text(markdown())
    print(f'Window: {len(PLAN)} pictures; {len(A.recipes)} recipes; 14 actions in two chapters.')
