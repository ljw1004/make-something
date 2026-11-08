"""Both orders add one whole canonical bearing unit and retain the chassis."""
from pathlib import Path
import hashlib
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
import racer_stages as R

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
model=R.make();states={}
for identity in R.STATES:
    R.set_stage(model,identity)
    entries={}
    for part,objects in model['parts'].items():
        for obj in objects:
            if obj.hide_render or obj.type!='MESH':continue
            evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
            mesh=evaluated.to_mesh()
            vertices=[tuple(obj.matrix_world@v.co) for v in mesh.vertices]
            faces=[tuple(p.vertices) for p in mesh.polygons]
            entries[obj.name]=(part,hashlib.sha256(repr((vertices,faces)).encode()).hexdigest())
            evaluated.to_mesh_clear()
    states[identity]=entries
base=states['wr-chassis'];full=states['wr-bearing-chassis']
front=states['wr-front-bearing-chassis'];rear=states['wr-rear-bearing-chassis']
for partial in (front,rear):
    assert all(partial.get(name)==value for name,value in base.items())
    assert all(full.get(name)==value for name,value in partial.items())
front_only=set(front)-set(base);rear_only=set(rear)-set(base)
assert front_only and len(front_only)==len(rear_only)
assert not front_only&rear_only
assert set(front)|set(rear)==set(full)
print(json.dumps({'sourceSha256':hashlib.sha256(Path(R.__file__).read_bytes()).hexdigest(),
                  'chassisMeshes':len(base),'frontBearingMeshes':len(front_only),'rearBearingMeshes':len(rear_only),
                  'exactExistingGeometryPreserved':True,'eitherOrderEqualsCanonicalFullAssembly':True},indent=2))
