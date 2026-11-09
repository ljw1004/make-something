"""Truthful paired detail/setup cameras for Builder's fixed flight diagrams.

The model and all fitted dimensions/poses are unchanged. The large detail
isolates the moving assembly; the small setup camera retains the complete
ground apparatus and its real lines. Run in Blender with two render threads.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'src/story/parser.ts').exists())
BASE = ROOT/'archive/2026.11.07 builder study/art'
sys.path.insert(0, str(BASE))
import bpy
import presentation as P
import scene_parts as S
from construction_lighting import frame_lights


def under(obj, parent):
    while obj:
        if obj == parent:
            return True
        obj = obj.parent
    return False


parser = argparse.ArgumentParser()
parser.add_argument('--catalogue', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--ids', required=True)
parser.add_argument('--samples', type=int, default=24)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
catalogue = json.loads(Path(args.catalogue).read_text())
items = {i['id']: i for i in catalogue['items']}
ids = args.ids.split(',')
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = S.configure_render(1200)
scene.render.threads_mode = 'FIXED'
scene.render.threads = 2
scene.cycles.samples = args.samples
bpy.context.view_layer.update()
studio = [(light, light.location.copy(), light.rotation_euler.copy(), light.data.energy, light.data.size)
          for light in scene.objects if light.type == 'LIGHT']
model = P.build('whale')
sources = {Path(module.__file__).resolve() for module in tuple(sys.modules.values())
           if getattr(module, '__file__', None) and Path(module.__file__).resolve().parent == BASE}
sources.add(Path(__file__).resolve())
hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(sources)}
records = []


def render(identity, kind, view, track_light_height=0., dimensions=(1200, 1200), body_objects=None):
    for light, location, rotation, power, size in studio:
        light.location = location
        light.rotation_euler = rotation
        light.data.energy = power
        light.data.size = size
        for key in ('construction_light_position', 'construction_light_power', 'construction_light_size'):
            if key in light:
                del light[key]
    frame_lights(scene, view['scale'])
    for light, *_ in studio:
        light.location.z += track_light_height
    scene.render.resolution_x, scene.render.resolution_y = dimensions
    camera = S.camera('flight '+kind+' camera', view['location'], view['target'], view['scale'])
    scene.camera = camera
    bpy.context.view_layer.update()
    body_bounds = None
    if body_objects:
        from bpy_extras.object_utils import world_to_camera_view
        from mathutils import Vector
        depsgraph = bpy.context.evaluated_depsgraph_get()
        points = []
        for obj in body_objects:
            evaluated = obj.evaluated_get(depsgraph)
            points.extend(world_to_camera_view(scene, camera, evaluated.matrix_world @ Vector(corner))
                          for corner in evaluated.bound_box)
        body_bounds = [min(p.x for p in points)*dimensions[0], (1-max(p.y for p in points))*dimensions[1],
                       max(p.x for p in points)*dimensions[0], (1-min(p.y for p in points))*dimensions[1]]
    path = out/(identity+'--'+kind+'.png')
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(camera, do_unlink=True)
    print('RENDERED', identity, kind, flush=True)
    return {'file': path.name, 'camera': view, 'pixels': dimensions,
            'lightTrackingHeight': track_light_height,
            'movingBodyProjectionBounds': body_bounds,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


for identity in ids:
    P.stage(model, items[identity], 'whale')
    visible = {obj: not obj.hide_render for obj in scene.objects if obj.type in {'MESH', 'CURVE', 'FONT'}}
    original_transforms = {obj.name: tuple(tuple(row) for row in obj.matrix_world) for obj in visible}
    setup = render(identity, 'setup', dict(P.GARDEN_VIEW))
    height = model['root'].location.z
    main_view = {'location': (1.1, -2., 1.+height), 'target': (0, 0, .32+height), 'scale': 1.30}
    kept = []
    body_objects = [obj for obj, was_visible in visible.items() if was_visible and under(obj, model['root'])]
    ground_lines = [model.get(key) for key in ('control_lead', 'remote_lead', 'stop_cord', 'short_tether', 'switch_lead')]
    ground_lines.extend(model.get('tethers', []))
    ground_lines = {obj for obj in ground_lines if obj is not None and visible.get(obj, False)}
    for obj, was_visible in visible.items():
        show = was_visible and (under(obj, model['root']) or obj in ground_lines)
        obj.hide_render = not show
        if show:
            kept.append(obj.name)
    main = render(identity, 'detail', main_view, height, body_objects=body_objects)
    for obj, was_visible in visible.items():
        obj.hide_render = not was_visible
    detail_spec = model.get('whale_service_detail')
    teaching = None
    if detail_spec:
        teaching = render(identity, 'teaching', detail_spec['view'], dimensions=tuple(detail_spec.get('resolution', (960, 960))))
        teaching['label'] = detail_spec['label']
    bpy.context.view_layer.update()
    current_transforms = {obj.name: tuple(tuple(row) for row in obj.matrix_world) for obj in visible}
    if current_transforms != original_transforms:
        raise ValueError('A camera/render pass changed fitted transforms: '+identity)
    records.append({'id': identity, 'setup': setup, 'detail': main, 'teaching': teaching,
                    'detailSelection': 'Visible descendants of the unchanged moving assembly root and actual attached ground-line objects. Detail crop follows body bounds and clips outward line continuations; all ground apparatus and complete line routes remain in the separate setup view.',
                    'detailObjects': kept, 'heightMetres': height,
                    'pitchRadians': model['root'].rotation_euler.y,
                    'unchangedTransforms': True})
    (out/'render-manifest.json').write_text(json.dumps({'storyHash': catalogue['storyHash'], 'sourceHashes': hashes, 'images': records}, indent=2)+'\n')
print('Completed', len(records), 'flight diagram camera sets', flush=True)
