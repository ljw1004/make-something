"""Three literal mirrors on connected hinges and three literal colour pieces."""
import math
from early_common import libraries, owned, show, inspection, entry

PLAN={};NAMES={}
def item(identity,name,parts,group=None,css=110,fold=False):
    NAMES[identity]=name;PLAN[identity]=entry(parts,group or identity,css,fold=fold)
supplies=[('backing','Backing'),('mirror-1','First mirror'),('mirror-2','Second mirror'),('mirror-3','Third mirror'),
          ('tube','Viewing tube'),('cell','Colour cell'),('triangle','Triangle'),('crescent','Crescent'),('disc','Disc'),
          ('lid','Clear lid'),('diffuser','Light cover')]
for key,name in supplies:item('bf-ka-'+key,name,[key],css=175 if key in {'backing','tube'} else 110)
for i in range(1,4):NAMES['bf-ka-mirror-'+str(i)]='Mirror'
state=['backing'];current='bf-ka-backing';steps=[]
for i in range(1,4):
    state=state+['mirror-'+str(i)];result='bf-ka-mirrors-'+str(i)
    item(result,'Mirrors',state,group='ka-mirrors',css=240)
    steps.append((current,'bf-ka-mirror-'+str(i),result,'Fit the '+['First','Second','Third'][i-1]+' mirror'));current=result
item('bf-ka-prism','Mirror triangle',state,css=210,fold=True)
steps.append((current,'bf-ka-fold','bf-ka-prism','Fold the mirrors into a triangle'))
state+=['tube'];item('bf-ka-viewer','Viewing tube',state,css=240,fold=True)
steps.append(('bf-ka-prism','bf-ka-tube','bf-ka-viewer','Slide the triangle into the Viewing tube'))
CHAPTERS=[dict(id='bf-ka-mirrors',title='Three mirrors',reference='kaleidoscope',steps=steps,processes={'bf-ka-fold':'fold'})]
# All three actual strips are interchangeable. Their identities record which
# physical panel has been filled, without requiring a hidden numbered match.
mirror_states={0:'bf-ka-backing',1:'bf-ka-mirrors-1',2:'bf-ka-only-2',4:'bf-ka-only-3',
               3:'bf-ka-mirrors-2',5:'bf-ka-pair-13',6:'bf-ka-pair-23',7:'bf-ka-mirrors-3'}
for mask in (2,4,5,6):
    item(mirror_states[mask],'Mirrors',['backing']+['mirror-'+str(i+1) for i in range(3) if mask&(1<<i)],group='ka-mirrors',css=240)
ordinary={(a,b,c) for a,b,c,_ in steps};alternatives=[]
for mask in range(7):
    for i in range(3):
        if mask&(1<<i):continue
        recipe=(mirror_states[mask],'bf-ka-mirror-'+str(i+1),mirror_states[mask|(1<<i)])
        if recipe not in ordinary:alternatives.append((*recipe,''))
CHAPTERS[0]['extra_steps']=alternatives
CHAPTERS[0]['goals']=[([mirror_states[n] for n in (1,2,4)],'Fit a Mirror to the Backing'),
                      ([mirror_states[n] for n in (3,5,6)],'Fit another Mirror'),
                      (['bf-ka-mirrors-3'],'Fit the last Mirror'),
                      (['bf-ka-prism'],'Fold the mirrors into a triangle'),
                      (['bf-ka-viewer'],'Slide the triangle into the Viewing tube')]
cell=['cell'];current='bf-ka-cell';steps=[]
for key,result,goal in [('triangle','bf-ka-colour-1','Put the Triangle in the Colour cell'),('crescent','bf-ka-colour-2','Add the Crescent'),
                       ('disc','bf-ka-colour-3','Add the Disc'),('lid','bf-ka-lidded','Snap on the Clear lid'),
                       ('diffuser','bf-ka-covered','Fit the Light cover')]:
    cell=cell+[key];item(result,'Colour cell',cell,group='ka-cell',css=220,fold=True)
    steps.append((current,'bf-ka-'+key,result,goal));current=result
item('kaleidoscope','Kaleidoscope',state+cell,css=350,fold=True)
steps.append(('bf-ka-viewer',current,'kaleidoscope','Fit the Colour cell to the Viewing tube'))
CHAPTERS.append(dict(id='bf-ka-colours',title='A pocket full of colours',reference='kaleidoscope',steps=steps))
DESCRIPTIONS={
 'bf-ka-backing':'One continuous scored binding sheet. Its three adhesive panels hold the mirror backs; the flexible seams become hinges.',
 'bf-ka-cell':'A connected clear-bottomed cell with a rotating collar fitting. Its separate snap lid leaves space for the coloured pieces to tumble.',
 'bf-ka-tube':'A prepared protective tube with a dark eyecap, padded mirror supports and a retained turning collar.',
}

def build():
    S=libraries()
    import optical_toys as source
    import bpy
    m=source.build_kaleidoscope();old=m['parts']
    # Diagram shading: make the silver reflecting faces legible against white
    # without changing the dimensioned mirror geometry or their optical role.
    shader=m['strips'][0].data.materials[0].node_tree.nodes.get('Principled BSDF')
    shader.inputs['Metallic'].default_value=.25
    shader.inputs['Roughness'].default_value=.3
    parts={key:[] for key,_ in supplies}
    for i,obj in enumerate(m['strips']):
        # Leave 1 mm at each nominal triangle corner: finite-thickness
        # mirror edges must not intersect where their centre planes meet.
        # The 0.866 mm geometric minimum needs positive clearance. These
        # supplied strips are 38 x 180 x 1 mm in every view.
        for vertex in obj.data.vertices:vertex.co.x*=.95
        parts['mirror-'+str(i+1)]=[obj]
    parts['tube']=list(old['ka-tube']);parts['diffuser']=list(old['ka-diffuser'])
    # Both fixed neck rings must pass the actual backing and outside seam,
    # including their thickness. The 25.6 mm radius leaves positive clearance.
    for obj in parts['tube']:
        if obj.name.startswith(('fixed front neck','fixed collar retaining flange')):
            for vertex in obj.data.vertices:
                r=math.hypot(vertex.co.x,vertex.co.z)
                if abs(r-.0245)<1e-6:
                    vertex.co.x*=.0256/r;vertex.co.z*=.0256/r
    # The new physical backing sits between mirrors and their support pads.
    # Recess each pad by the backing thickness instead of intersecting it.
    for obj in parts['tube']:
        if obj.name.startswith('padded mirror support'):
            x,z=obj.location.x,obj.location.z;r=math.hypot(x,z)
            thickness=max(v.co.z for v in obj.data.vertices)-min(v.co.z for v in obj.data.vertices)
            for vertex in obj.data.vertices:vertex.co.z*= (thickness-.00035)/thickness
            obj.location.x+=x/r*.000175;obj.location.z+=z/r*.000175
    for obj in old['ka-cell']:
        if (obj.name.startswith('clear cell wall') and obj.location.y<-.115) or obj.name.startswith(('clear lid snap','clear lid retaining')):key='lid'
        else:key='cell'
        parts[key].append(obj)
    from mathutils import Vector
    bpy.context.view_layer.update()
    for obj in old['ka-chips']:
        key='triangle' if 'triangle' in obj.name else 'crescent' if 'crescent' in obj.name else 'disc'
        # All three loose pieces rest against the same clear bottom. They are
        # separated in its plane, never suspended at different chamber depths.
        current=sum((obj.matrix_world @ Vector(c)).y for c in obj.bound_box)/8
        obj.location.y+=-.10935-current
        parts[key].append(obj)
    mesh=bpy.data.meshes.new('one continuous scored backing mesh')
    mesh.from_pydata([(0,0,0)]*12,[],[(i,i+1,i+7,i+6) for i in range(5)]);mesh.update()
    backing=bpy.data.objects.new('one continuous scored adhesive backing',mesh)
    bpy.context.collection.objects.link(backing);backing.parent=m['root'];backing.data.materials.append(S.material('card'))
    solid=backing.modifiers.new('real flexible backing thickness','SOLIDIFY');solid.thickness=.00035;solid.offset=0
    parts['backing']=[backing];m['backing']=backing
    m['source']=source
    return owned(m,parts)

def stage(m,identity):
    info=PLAN[identity];fold=info['fold'];m['source'].set_kaleidoscope_triangle(m,fold)
    # Offset plane is 0.675 mm behind each mirror centre: its 0.175 mm
    # half-thickness touches the actual 0.5 mm mirror back. All folded and
    # flat panels retain the same developed width, including the closing tab.
    factor=1+.000675/(.040/(2*math.sqrt(3)))
    width=.040*factor
    if fold:
        corners=[(x*factor,z*factor) for x,z in m['vertices']]
        p,q=corners[0],corners[1]
        # The 6 mm seam tab steps 0.45 mm OUTSIDE the first panel, then
        # overlaps it for the remaining 5.55 mm. The developed length stays
        # exactly 6 mm rather than stretching or occupying the first panel.
        midpoint=((p[0]+q[0])/2,(p[1]+q[1])/2)
        r=math.hypot(*midpoint);normal=(midpoint[0]/r,midpoint[1]/r)
        lift=(p[0]+normal[0]*.00045,p[1]+normal[1]*.00045)
        end=(lift[0]+.00555/width*(q[0]-p[0]),lift[1]+.00555/width*(q[1]-p[1]))
        path=corners+[p,lift,end]
    else:
        path=[(-1.5*width+i*width,-.000675) for i in range(4)]+[(1.5*width+.00045,-.000675),(1.5*width+.006,-.000675)]
        for i,mirror in enumerate(m['strips']):mirror.location=((i-1)*width,0,0)
    for row,y in enumerate((-.09,.09)):
        for i,(x,z) in enumerate(path):m['backing'].data.vertices[row*6+i].co=(x,y,z)
    m['backing'].data.update()
    # Every lid component remains joined to the lid; only its supply visibility changes.
    show(m,info['parts'])
    if info['group']=='ka-mirrors':return {'location':(.32,-.55,.65),'target':(0,0,0),'scale':.25}
    if info['group']=='ka-cell':return {'location':(.14,-.8,.25),'target':(0,-.115,0),'scale':.082}
    return inspection(m,info['parts'],direction=(.36,-.52,.30),margin=1.22)
