"""Check evaluated geometry of every existing part across additive recipes.

Blender -b --python verify_additions.py -- --family NAME --output SCRATCH.json
Process recipes are excluded: a real fold/flip deliberately changes geometry.
This checks continuity, not insertion clearance, strength, or visual readability.
"""
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import math
import re
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import bpy
import core

p=argparse.ArgumentParser();p.add_argument('--family',required=True);p.add_argument('--output',required=True)
args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
module=importlib.import_module(args.family)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
model=module.build();snapshots={};local_snapshots={};views={}
for identity,info in module.PLAN.items():
    view=module.stage(model,identity);bpy.context.view_layer.update()
    actual={key for key,objects in model['parts'].items() if any(not obj.hide_render for obj in objects)}
    if actual!=set(info['parts']):raise AssertionError((identity,'unexpected visible parts',actual^set(info['parts'])))
    signature=json.dumps(view,sort_keys=True)
    if info['group'] in views and views[info['group']]!=signature:raise AssertionError((identity,'changed camera inside shared crop group'))
    views[info['group']]=signature
    deps=bpy.context.evaluated_depsgraph_get();parts={};local_parts={}
    for key in info['parts']:
        objects=[];local_objects={}
        for obj in model['parts'][key]:
            if obj.type not in {'MESH','CURVE','FONT'}:continue
            evaluated=obj.evaluated_get(deps);mesh=evaluated.to_mesh()
            coords=[tuple(round(v,7) for v in evaluated.matrix_world@vertex.co) for vertex in mesh.vertices]
            faces=[tuple(poly.vertices) for poly in mesh.polygons]
            objects.append((obj.name,coords,faces,[m.name for m in mesh.materials if m]))
            local_geometry=([tuple(round(v,7) for v in vertex.co) for vertex in mesh.vertices],faces,[m.name for m in mesh.materials if m])
            local_objects[obj.name]=(hashlib.sha256(json.dumps(local_geometry,separators=(',',':')).encode()).hexdigest(),evaluated.matrix_world.copy())
            evaluated.to_mesh_clear()
        parts[key]=hashlib.sha256(json.dumps(sorted(objects),separators=(',',':')).encode()).hexdigest()
        local_parts[key]=local_objects
    snapshots[identity]=parts
    local_snapshots[identity]=local_parts

def rigid_settling(before,after,keys):
    """Diagnose a shared rigid turn; it is not an exception to continuity."""
    objects={name:record for key in keys for name,record in before[key].items()}
    fitted={name:record for key in keys for name,record in after[key].items()}
    if objects.keys()!=fitted.keys() or any(objects[n][0]!=fitted[n][0] for n in objects):return None
    anchor=next(iter(objects));delta=fitted[anchor][1]@objects[anchor][1].inverted()
    rotation=delta.to_3x3()
    if max(abs(v-1) for v in delta.to_scale())>1e-6 or abs(rotation.determinant()-1)>1e-6:return None
    for name,(_,matrix) in objects.items():
        expected=delta@matrix;actual=fitted[name][1]
        if max(abs(expected[i][j]-actual[i][j]) for i in range(4) for j in range(4))>2e-7:return None
    angle=math.degrees(rotation.to_quaternion().angle)
    return angle if angle<=20 else None

checks=[];failures=[]
for line in (HERE/(args.family+'.md')).read_text().splitlines():
    match=re.match(r'^- `([^`]+)` \[(transform|consume)\] \+ `([^`]+)` \[(transform|consume)\] -> `([^`]+)`',line)
    if not match:continue
    a,af,b,bf,result=match.groups()
    if {af,bf}!={'consume','transform'}:raise AssertionError(('ambiguous physical workpiece',line))
    workpiece,incoming=(a,b) if af=='transform' else (b,a)
    if workpiece not in snapshots or result not in snapshots:raise AssertionError(('unmapped illustrated workpiece',line))
    before,after=snapshots[workpiece],snapshots[result]
    missing=set(before)-set(after)
    changed=[key for key in before.keys()&after.keys() if before[key]!=after[key]]
    added=set(after)-set(before)
    settling=None
    if changed and not missing:
        settling=rigid_settling(local_snapshots[workpiece],local_snapshots[result],before.keys())
    if missing or changed or not added:failures.append(dict(workpiece=workpiece,incoming=incoming,result=result,missing=sorted(missing),changed=changed,added=sorted(added)))
    checks.append(dict(workpiece=workpiece,incoming=incoming,result=result,retained=len(before),added=sorted(added),rigidSettlingDegrees=settling))
sources={str(Path(m.__file__).resolve().relative_to(core.ROOT)):hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and str(Path(m.__file__).resolve()).startswith(str(core.ROOT)) and str(m.__file__).endswith('.py')}
out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(dict(family=args.family,sources=sources,stages=len(snapshots),checks=checks,failures=failures),indent=2)+'\n')
print(json.dumps(dict(family=args.family,stages=len(snapshots),additions=len(checks),failures=failures)))
if failures:raise AssertionError('Additions changed existing geometry; see scratch outcome')
