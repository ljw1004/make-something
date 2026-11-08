"""Check per-blade identity continuity and partial-fold mesh clearances."""
from pathlib import Path
import hashlib
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import pinwheel as P
import fold_stages as F

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
model=P.make()

def geometry(obj):
    evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh=evaluated.to_mesh();mesh.calc_loop_triangles()
    matrix=model['rotor'].matrix_world.inverted()@obj.matrix_world
    vertices=[matrix@v.co for v in mesh.vertices]
    faces=[tuple(t.vertices) for t in mesh.loop_triangles]
    evaluated.to_mesh_clear()
    return vertices,faces

def blade_geometries():return [geometry(obj) for obj,uv,height in model['paper']]
def digest(geometry):return hashlib.sha256(repr(geometry).encode()).hexdigest()

P.set_state(model,'pw-paper');flat=[digest(g) for g in blade_geometries()]
P.set_state(model,'pw-loose-rotor');folded=[digest(g) for g in blade_geometries()]
assert all(a!=b for a,b in zip(flat,folded))
records=[]
for identity,count in F.FOLDS.items():
    F.set_stage(model,identity)
    geometries=blade_geometries()
    hashes=[digest(g) for g in geometries]
    assert hashes==folded[:count]+flat[count:],identity
    trees=[BVHTree.FromPolygons(v,f,all_triangles=True) for v,f in geometries]
    crossings=[]
    for i in range(4):
        for j in range(i+1,4):
            for ai,bi in trees[i].overlap(trees[j]):
                centers=[]
                for k,face in ((i,ai),(j,bi)):
                    vertices,faces=geometries[k]
                    centers.append(sum((vertices[index] for index in faces[face]),Vector())/3)
                if max(p.z for p in centers)>.001:crossings.append((i+1,j+1))
    assert not crossings,(identity,crossings[:10])
    assert all(obj.hide_render for part in ('pw-hub','pw-axle','pw-handle') for obj in model['parts'][part])
    records.append({'id':identity,'completedBlades':count,'exactBladeStates':True,'foldedCrossings':0})
print(json.dumps({'baseSha256':hashlib.sha256(Path(P.__file__).read_bytes()).hexdigest(),
                  'adapterSha256':hashlib.sha256(Path(F.__file__).read_bytes()).hexdigest(),
                  'stages':records,'limits':'Finite evaluated mesh comparisons; no paper elasticity or folding motion simulation.'},indent=2))
