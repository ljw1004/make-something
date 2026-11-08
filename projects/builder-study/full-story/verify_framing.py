"""Check every current-stage camera against evaluated visible mesh vertices."""
from pathlib import Path
import argparse
import importlib
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix
import core

p = argparse.ArgumentParser()
p.add_argument('--families', required=True)
p.add_argument('--output', required=True)
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
records, failures = [], []
for family in args.families.split(','):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = core.S.configure_render(480)
    module = importlib.import_module(family)
    model = module.build()
    for identity, info in module.PLAN.items():
        view = module.stage(model, identity)
        camera = core.S.camera(identity, view['location'], view['target'], view['scale'])
        camera.rotation_euler = (camera.rotation_euler.to_matrix() @ Matrix.Rotation(view.get('roll', 0), 3, 'Z')).to_euler()
        scene.camera = camera
        bpy.context.view_layer.update()
        graph = bpy.context.evaluated_depsgraph_get()
        points = []
        for obj in {obj for objects in model['parts'].values() for obj in objects}:
            if obj.hide_render or obj.type not in {'MESH', 'CURVE'}:
                continue
            evaluated = obj.evaluated_get(graph)
            mesh = evaluated.to_mesh()
            points.extend(world_to_camera_view(scene, camera, evaluated.matrix_world @ v.co)
                          for v in mesh.vertices)
            evaluated.to_mesh_clear()
        if not points:
            failures.append(dict(family=family, identity=identity, error='empty geometry'))
        else:
            bounds = [min(p.x for p in points), min(p.y for p in points),
                      max(p.x for p in points), max(p.y for p in points)]
            row = dict(family=family, identity=identity, bounds=bounds)
            records.append(row)
            if min(bounds[:2]) <= .008 or max(bounds[2:]) >= .992:
                failures.append(row)
        bpy.data.objects.remove(camera, do_unlink=True)
    print(f'FRAMING {family}: {len(module.PLAN)} states', flush=True)
out = Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(dict(states=len(records), failures=failures, records=records,
    limit='Evaluated geometry framing only; actual rendered alpha, crop and phone-size recognition still need review.'), indent=2)+'\n')
print(json.dumps(dict(states=len(records), failures=failures)), flush=True)
if failures:
    raise RuntimeError('Current-stage geometry crosses a camera margin')
