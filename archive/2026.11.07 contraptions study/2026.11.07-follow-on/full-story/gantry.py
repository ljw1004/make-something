"""320×240 mm gantry hoist, with a 300 mm high beam and a clear central bay.

Prepared triangular side frames are each a single connected glued/pegged unit.
Separate retained pulley/fork units and a ratchet winch form the hoist. The rope
runs up the outside, across the beam, then down into the bay. Geometry describes
connections and travel, not load rating, pawl durability or child operation.
"""
from pathlib import Path
import math
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from middle.routes import Route

R=Route()
def item(i,n,p,g=None,s=110,e=''):return R.item(i,n,p,g,s,e)
base=item('gh-base','Base',['base'],'gh-frame',235)
for i in (1,2):item(f'gh-side-{i}','Side frame',['side-left'],s=175,e='A prepared triangular frame with joined braces and captive foot pegs. Either frame fits either side of the base.')
item('gh-crossbeam','Beam',['beam'],s=165,e='The beam has two end sockets and separate sockets underneath for the pulley forks.')
item('gh-one-side','Frame',['base','side-left'],'gh-frame',235)
item('gh-two-sides','Frame',['base','side-left','side-right'],'gh-frame',235)
item('gh-frame','Frame',['base','side-left','side-right','beam'],'gh-frame',235)
for i,n in [('drum','Winch'),('ratchet','Ratchet'),('crank','Crank')]:item('gh-'+i,n,[i],s=110,e='The winch drum comes with its axle, two bearing cheeks, captive base fasteners and a sprung cord clamp.' if i=='drum' else '')
R.plan['gh-drum'].update(group='gh-winch-work',css=150)
winch={(): 'gh-drum',('ratchet',):'gh-ratchet-winch',('crank',):'gh-crank-winch',('ratchet','crank'):'gh-winch'}
for extras,i in winch.items():
    if extras:item(i,'Winch',['drum',*extras],'gh-winch-work',150)
item('gh-rear-drum','Winch',['drum'],'gh-winch-rear',150)
item('gh-rear-ratchet-winch','Winch',['drum','ratchet'],'gh-winch-rear',150)
item('gh-rear-winch','Winch',['drum','ratchet','crank'],'gh-winch-rear',150)
item('gh-front-crank-winch','Winch',['drum','crank'],'gh-winch-work',150)
R.plan['gh-crank-winch']['group']='gh-winch-rear'
frameparts=['base','side-left','side-right','beam','drum','ratchet','crank']
item('gh-mounted','Gantry',frameparts,'gh-hoist',265)
recipes=[('gh-base',f'gh-side-{i}','gh-one-side') for i in (1,2)]
recipes += [('gh-one-side',f'gh-side-{i}','gh-two-sides') for i in (1,2)]
recipes += [('gh-two-sides','gh-crossbeam','gh-frame')]
recipes += [('gh-drum','gh-ratchet','gh-ratchet-winch'),
            ('gh-front-crank-winch','gh-ratchet','gh-winch'),
            ('gh-drum','gh-winch-flip','gh-rear-drum'),
            ('gh-ratchet-winch','gh-winch-flip','gh-rear-ratchet-winch'),
            ('gh-rear-drum','gh-crank','gh-crank-winch'),
            ('gh-rear-ratchet-winch','gh-crank','gh-rear-winch'),
            ('gh-crank-winch','gh-winch-flip','gh-front-crank-winch'),
            ('gh-rear-winch','gh-winch-flip','gh-winch')]
recipes += [('gh-frame','gh-winch','gh-mounted')]
first=list(R.items)
R.page('c-gantry-frame','A lifting frame','gh-mounted',first,[('Fit a side frame','gh-one-side'),('Fit the other side frame','gh-two-sides'),('Join the frames with the beam','gh-frame'),('Fit the ratchet to the winch',['gh-ratchet-winch','gh-winch']),('Turn the winch toward its crank end',['gh-rear-drum','gh-rear-ratchet-winch']),('Fit the crank',['gh-crank-winch','gh-rear-winch']),('Turn the winch back toward the ratchet',['gh-front-crank-winch','gh-winch']),('Mount the winch','gh-mounted')],recipes,processes={'gh-winch-flip':'flip'})
for position,label in [('side','Side fork'),('drop','Drop fork')]:
    item('gh-'+position+'-fork',label,[position+'-fork'],s=95,e='An open pulley bracket with a split snap axle and a barbed mounting stem. Press a pulley over the axle tip, then push the stem through the beam until its head opens above the wood.')
    item('gh-'+position+'-pulley','Pulley unit',[position+'-fork',position+'-wheel'],'gh-'+position+'-unit',125)
for i in (1,2):item(f'gh-pulley-{i}','Pulley',['side-wheel'],s=80,e='A grooved pulley that turns on either fork axle. The split axle tip retains it.')
item('gh-pawl','Pawl',['pawl'],s=95,e='A spring pawl and its connected mounting foot. Its tooth rests in the ratchet so the drum cannot freely unwind.')
item('gh-rope','Rope and hook',['rope'],s=160,e='One continuous cord, already tied to its hook. Push its free end under the drum’s prepared spring clamp, wind one turn, then thread it over the two pulleys.')
item('gh-basket','Basket',['basket'],s=135,e='A small rigid basket with a connected lifting handle. It hangs directly on the hook.')
ready={0:'gh-mounted'}
for mask in range(1,8):
    ready[mask]='gh-fitted-'+str(mask)
    parts=frameparts+[p for bit,group in [(1,['side-fork','side-wheel']),(2,['drop-fork','drop-wheel']),(4,['pawl'])] if mask&bit for p in group]
    item(ready[mask],'Gantry',parts,'gh-hoist',265)
recipes=[]
for position in ('side','drop'):
    recipes += [('gh-'+position+'-fork',f'gh-pulley-{i}','gh-'+position+'-pulley') for i in (1,2)]
for mask,i in ready.items():
    for bit,part in [(1,'gh-side-pulley'),(2,'gh-drop-pulley'),(4,'gh-pawl')]:
        if not mask&bit:recipes.append((i,part,ready[mask|bit]))
item('gh-roped','Hoist',R.plan[ready[7]]['parts']+['rope'],'gh-hoist',265)
item('gantry-hoist','Gantry hoist',R.plan['gh-roped']['parts']+['basket'],'gh-finished',345,e='Two fixed pulleys guide the cord; they change its direction without multiplying the lifting force. Turning the crank winds the drum. The pawl holds the drum between turns.')
recipes += [(ready[7],'gh-rope','gh-roped'),('gh-roped','gh-basket','gantry-hoist')]
second=[i for i in R.items if i not in first]
R.page('c-gantry-rope','Over the beam','gantry-hoist',second,[('Fit a pulley into the side fork','gh-side-pulley'),('Fit the other pulley into its fork','gh-drop-pulley'),('Mount the side pulley',[ready[m] for m in ready if m&1]),('Mount the drop pulley',[ready[m] for m in ready if m&2]),('Fit the pawl',[ready[m] for m in ready if m&4]),('Thread the rope over both pulleys','gh-roped'),('Hang the basket on the hook','gantry-hoist')],recipes)
PLAN=R.plan


def rope_path():
    # The short tail enters the spring clamp beside the first winding.
    pts=[(-.1259,y,.058) for y in (-.0108,-.010,-.008,-.006)]
    # One drum turn joins the vertical run tangentially at the left edge.
    for j in range(65):
        angle=-math.pi+2*math.pi*j/64
        pts.append((-.112+.014*math.cos(angle),-.0045+.0045*j/64,.058+.014*math.sin(angle)))
    pts.append((-.126,0,.258))
    pts += [(-.112+.014*math.cos(math.pi-math.pi*j/64),0,.258+.014*math.sin(math.pi-math.pi*j/64)) for j in range(1,33)]
    pts.append((0,0,.272))
    pts += [(.014*math.cos(math.pi/2-math.pi*j/64),0,.258+.014*math.sin(math.pi/2-math.pi*j/64)) for j in range(1,33)]
    pts.append((.014,0,.135))
    return pts


def build():
    import bpy
    import core
    from mathutils import Vector
    S=core.S;a=core.Assembly('compact gantry hoist')
    box=a.box;cyl=a.cylinder
    def bore(o,c,r,l,axis='Z'):S.bore(o,c,r,l,axis)
    def cut_box(obj,c,size):
        cutter=S.box('temporary receiving cut',c,size)
        bpy.context.view_layer.objects.active=obj;mod=obj.modifiers.new('actual receiving cut','BOOLEAN');mod.object=cutter;mod.operation='DIFFERENCE';bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    def bar(part,name,start,end,width=.014):
        v=Vector(end)-Vector(start)
        obj=box(part,name,(Vector(start)+Vector(end))/2,(width,width,v.length),'birch')
        obj.rotation_euler=v.to_track_quat('Z','Y').to_euler();return obj
    board=box('base','broad gantry base',(0,0,.009),(.320,.240,.018),'birch')
    for x in (-.140,.140):
        for y in (-.090,.090):
            bore(board,(x,y,.009),.0033,.030)
            # Positive receiver in the board, not an invented detachable support.
    for side,x in [('left',-.140),('right',.140)]:
        key='side-'+side
        for label,y in [('front',-.090),('rear',.090)]:
            diagonal=bar(key,label+' diagonal',(x,y,.025),(x,0,.289))
            # Flat prepared receiving ends seat against the beam underside.
            cut_box(diagonal,(x,0,.340),(.040,.100,.104))
        bar(key,'joined lower brace',(x,-.085,.040),(x,.085,.040))
        for y in (-.090,.090):
            cyl(key,'captive foot peg',(x,y,.022),.003,.036,'ink')
            cyl(key,'foot shoulder',(x,y,.021),.006,.004,'teal')
        cyl(key,'beam locating peg',(x,0,.294),.003,.024,'ink')
    beam=box('beam','crossbeam',(0,0,.300),(.304,.024,.024),'birch')
    for x in (-.140,.140):bore(beam,(x,0,.300),.0033,.030)
    for tag,x in [('side',-.112),('drop',0)]:
        bore(beam,(x,.006,.300),.0023,.035)
        part=tag+'-fork'
        box(part,'pulley bracket bridge',(x,0,.2845),(.024,.028,.007),'teal')
        mount=cyl(part,'split bracket mounting stem',(x,.006,.2985),.002,.031,'ink')
        bpy.ops.mesh.primitive_cone_add(vertices=48,radius1=.0029,radius2=.0016,depth=.004,location=(x,.006,.31405))
        head=a.add(part,bpy.context.object);head.name='barbed bracket mounting head';head.data.materials.append(S.material('ink'))
        head.scale.y=.002/.0029
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        for obj in (mount,head):cut_box(obj,(x,.006,.306),(.0015,.010,.024))
        box(part,'open bracket back',(x,.011,.266),(.026,.004,.040),'teal')
        axle=cyl(part,'split pulley axle',(x,.0015,.258),.002,.023,'teal','Y')
        bpy.ops.mesh.primitive_cone_add(vertices=48,radius1=.0026,radius2=.0016,depth=.003,location=(x,-.0115,.258),rotation=(math.pi/2,0,0))
        tip=a.add(part,bpy.context.object);tip.name='tapered snap tip';tip.data.materials.append(S.material('teal'))
        # Only X carries retaining barbs: the unsplit Z span fits the bore.
        tip.scale.y=.0020/.0026
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        # Two connected cantilever prongs, genuinely open from the insertion end.
        for obj in (axle,tip):cut_box(obj,(x,-.0055,.258),(.0011,.019,.009))
        for y,r,th in [(0,.0128,.007),(-.005,.017,.003),(.005,.017,.003)]:
            wheel=cyl(tag+'-wheel','grooved pulley',(x,y,.258),r,th,'orange','Y')
            bore(wheel,(x,y,.258),.0022,th+.004,'Y')
    # Prepared winch includes a real bearing frame; its separate crank and ratchet
    # key onto the two exposed shaft ends before the frame is mounted.
    foot=box('drum','winch mounting foot',(-.112,0,.024),(.050,.052,.012),'teal')
    for y in (-.022,.022):
        cheek=box('drum','winch bearing cheek',(-.112,y,.043),(.040,.006,.038),'teal')
        bore(cheek,(-.112,y,.058),.0033,.012,'Y')
    cyl('drum','drum axle',(-.112,0,.058),.003,.052,'ink','Y')
    for sign,shoulder in [(-1,.035),(1,.041)]:
        tip=shoulder+.0035
        stub=box('drum','keyed split shaft end',(-.112,sign*(.025+shoulder)/2,.058),(.0045,shoulder-.025,.0045),'ink')
        verts=[(-.112+x,sign*y,.058+z) for y,h in [(shoulder,.0027),(tip,.0020)] for x,z in [(-h,-.00225),(h,-.00225),(h,.00225),(-h,.00225)]]
        mesh=bpy.data.meshes.new('square snap head');mesh.from_pydata(verts,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);mesh.update()
        import bmesh
        bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
        head=bpy.data.objects.new('tapered keyed retaining head',mesh);bpy.context.collection.objects.link(head);head.data.materials.append(S.material('ink'));a.add('drum',head)
        for obj in (stub,head):cut_box(obj,(-.112,sign*(.027+tip+.002)/2,.058),(.0011,tip+.002-.027,.010))
    cyl('drum','cord drum',(-.112,0,.058),.0128,.024,'birch','Y')
    for y in (-.014,.014):cyl('drum','drum flange',(-.112,y,.058),.019,.003,'orange','Y')
    # Factory-fitted spring clamp. Its 2.2 mm radial throat compresses the
    # 2.4 mm cord locally; the short tail and winding are one continuous curve.
    box('drum','spring cord clamp pressure pad',(-.128,-.008,.058),(.002,.004,.004),'ink')
    for sign in (-1,1):
        a.line('drum','connected spring clamp leaf',[
            (-.1237,-.008,.058+sign*.004),
            (-.127,-.008,.058+sign*.004),
            (-.128,-.008,.058+sign*.0015)],.0007,'ink')
    for x in (-.128,-.096):
        bore(board,(x,0,.009),.002,.030)
        core.bolt(a,'drum','captive winch screw',(x,0,.021),.0018,.032)
    # Sawtooth profile, not a smooth disc labeled as a ratchet.
    points=[]
    for j in range(16):
        angle=2*math.pi*j/16
        points.extend([(-.112+.019*math.cos(angle),.058+.019*math.sin(angle)),(-.112+.016*math.cos(angle+.34),.058+.016*math.sin(angle+.34))])
    wheel=a.add('ratchet',S.profile('ratchet teeth',points,.004,y=-.032,color='orange',edge='orange'))
    cut_box(wheel,(-.112,-.032,.058),(.0046,.012,.0046))
    crank=box('crank','crank arm',(-.112,.037,.072),(.009,.006,.033),'orange')
    cut_box(crank,(-.112,.037,.058),(.0046,.014,.0046))
    cyl('crank','turning crank grip',(-.112,.049,.086),.005,.020,'teal','Y')
    # The pawl's preloaded leaf is connected to its mounting foot and tooth.
    box('pawl','pawl mounting foot',(-.082,-.036,.023),(.020,.016,.010),'teal')
    a.line('pawl','spring pawl',[(-.081,-.032,.025),(-.079,-.032,.046),(-.085,-.032,.062),(-.088,-.032,.066)],.002,'ink')
    root_contact=(-.112+.016*math.cos(.34),.058+.016*math.sin(.34))
    tooth_peak=(-.112+.019*math.cos(math.pi/8),.058+.019*math.sin(math.pi/8))
    # The pawl face shares the actual locking flank, without overlapping it.
    pawl_top=root_contact[1]+(-.088-root_contact[0])*(tooth_peak[1]-root_contact[1])/(tooth_peak[0]-root_contact[0])
    a.add('pawl',S.profile('pawl tooth seated in ratchet notch',[root_contact,(-.088,.061),(-.088,pawl_top)],.004,y=-.032,color='ink',edge='ink'))
    bore(board,(-.082,-.036,.009),.0018,.025)
    core.bolt(a,'pawl','pawl captive screw',(-.082,-.036,.017),.0015,.025)
    cord=a.line('rope','one continuous hoist cord',rope_path(),.0012,'ink')
    for point in cord.data.splines[0].points[:4]:point.radius=1.1/1.2
    hookroot=S.empty('tied hook pose');hookroot.parent=a.root;hookroot.location=(.014,0,.135)
    hookpoints=[(0,0,0),(0,0,-.010)]+[(.009+.009*math.cos(t),0,-.019+.009*math.sin(t)) for t in [math.pi+1.4*math.pi*i/32 for i in range(33)]]
    a.line('rope','hook with tied shank',hookpoints,.002,'ink',hookroot)
    # Rigid handle joins both sides of an actual open basket.
    box('basket','basket floor',(.022,0,.044),(.074,.066,.008),'birch')
    for y in (-.031,.031):box('basket','basket side',(.022,y,.062),(.074,.004,.036),'teal')
    for x in (-.013,.057):box('basket','basket end',(x,0,.062),(.004,.058,.036),'teal')
    a.line('basket','connected lifting bail',[(.022,-.031,.076),(.022,-.031,.102),(.022,0,.111),(.022,.031,.102),(.022,.031,.076)],.002,'ink')
    model=a.result(cord=cord,hook=hookroot)
    bpy.context.view_layer.update();return model


def stage(model,identity):
    import bpy
    from middle.views import stage_view,curve_points
    if identity not in PLAN:raise KeyError(identity)
    points=rope_path();model['hook'].location=(.014,0,.135)
    if identity=='gh-rope':
        length=sum(math.dist(a,b) for a,b in zip(points,points[1:]))
        def spiral(outer):
            return [((.016+(outer-.016)*i/360)*math.cos(6*math.pi*i/360),0,.10+(.016+(outer-.016)*i/360)*math.sin(6*math.pi*i/360)) for i in range(361)]
        lo,hi=.017,.12
        for _ in range(32):
            mid=(lo+hi)/2;candidate=spiral(mid)
            if sum(math.dist(a,b) for a,b in zip(candidate,candidate[1:]))>length:hi=mid
            else:lo=mid
        points=spiral((lo+hi)/2)
        model['hook'].location=points[-1]
    curve_points(model['cord'],points)
    # Compression under the prepared clamp is local to the fitted tail.
    for index,point in enumerate(model['cord'].data.splines[0].points):
        point.radius=(1.1/1.2 if identity!='gh-rope' and index<4 else 1)
    bpy.context.view_layer.update()
    rear=PLAN[identity]['group']=='gh-winch-rear' or identity=='gh-crank'
    return stage_view(model,PLAN,identity,direction=(-.8,1,.6) if rear else (.8,-1,.6))


if __name__=='__main__':R.write(__file__)
