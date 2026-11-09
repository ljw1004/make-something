"""Author geometry checks; run with Blender --background --python verify.py.

The snap envelopes are prescribed small-angle tongue deflections, not an
elastic simulation. They establish geometric room for insertion. Material
strain, stress, forces and manufacturing tolerance remain unvalidated.
"""
from pathlib import Path
import hashlib
import json
import math
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import pinwheel as P

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
model=P.make();P.set_state(model,'pinwheel')

def geometry(obj):
    evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh=evaluated.to_mesh();mesh.calc_loop_triangles()
    matrix=model['rotor'].matrix_world.inverted()@obj.matrix_world
    vertices=[matrix@v.co for v in mesh.vertices]
    faces=[tuple(t.vertices) for t in mesh.loop_triangles]
    evaluated.to_mesh_clear()
    return vertices,faces

def snap_envelope(objects, hinge_z, hinge_x, degrees, upper):
    angle=math.radians(degrees)
    vertices=[v for obj in objects for v in geometry(obj)[0]]
    posed=[];half_clearances=[]
    for v in vertices:
        active=v.z>hinge_z+1e-8 if upper else v.z<hinge_z-1e-8
        if not active:
            posed.append(v);continue
        sign=1 if v.x>=0 else -1
        theta=angle*sign*(-1 if upper else 1)
        center=Vector((hinge_x*sign,0,hinge_z))
        d=v-center
        q=center+Vector((d.x*math.cos(theta)+d.z*math.sin(theta),d.y,
                         -d.x*math.sin(theta)+d.z*math.cos(theta)))
        posed.append(q)
        half_clearances.append(sign*q.x)
    return {'max_radius_m':max(math.hypot(v.x,v.y) for v in posed),
            'half_to_midplane_min_m':min(half_clearances),
            'degrees':degrees,'hinge_z_m':hinge_z,'hinge_x_m':hinge_x,
            'vertex_count':len(vertices)}

hub=snap_envelope([o for o in model['parts']['pw-hub'] if o.name.startswith(('front-fitting hollow hub stem','tapered rear flexible'))],.0065,.00205,5.3,False)
axle=snap_envelope([o for o in model['parts']['pw-axle'] if o.name.startswith(('continuous blunt axle','tapered resilient axle'))],.010,.001125,4.8,True)
assert hub['max_radius_m']<.0032,hub
assert axle['max_radius_m']<.0018,axle
assert hub['half_to_midplane_min_m']>0,hub
assert axle['half_to_midplane_min_m']>0,axle

paper=[]
for obj,uv,height in model['paper']:
    vertices,faces=geometry(obj)
    paper.append((vertices,faces,BVHTree.FromPolygons(vertices,faces,all_triangles=True)))
crossings=[]
for i,(a,af,at) in enumerate(paper):
    for j,(b,bf,bt) in enumerate(paper[i+1:],i+1):
        for ai,bi in at.overlap(bt):
            # Shared web seams are intentional co-located boundaries at z=0.
            # Any folded-layer crossing is a failure.
            centers=[sum((vv[k] for k in ff[t]),Vector())/3 for vv,ff,t in [(a,af,ai),(b,bf,bi)]]
            if max(p.z for p in centers)>.001:crossings.append([i+1,j+1,[list(p) for p in centers]])
assert not crossings,crossings[:5]

fingerprints={}
for identity in ['pw-loose-rotor','pw-folded-rotor','pw-rear-rotor','pw-bearing-rotor','pw-mounted','pinwheel']:
    P.set_state(model,identity)
    fingerprints[identity]={obj.name:hashlib.sha256(repr(geometry(obj)).encode()).hexdigest()
        for objects in model['parts'].values() for obj in objects if obj.type=='MESH' and not obj.hide_render}
order=list(fingerprints)
for before,after in zip(order,order[1:]):
    assert all(fingerprints[after].get(name)==digest for name,digest in fingerprints[before].items()),(before,after)

clip_gap=2*.0042*math.sin(2.30/2)
print(json.dumps({'source_sha256':hashlib.sha256(Path(P.__file__).read_bytes()).hexdigest(),
                  'hub_insertion_envelope':hub,'axle_insertion_envelope':axle,
                  'folded_paper_crossings':len(crossings),'state_continuity':'all5transitions preserve every existing evaluated mesh',
                  'handle_nominal_mouth_m':clip_gap,'handle_total_required_mouth_expansion_m':.008-clip_gap,
                  'limits':'Prescribed geometric snap deflections, not elastic/force/manufacturing validation; finite mesh checks.'},indent=2))
