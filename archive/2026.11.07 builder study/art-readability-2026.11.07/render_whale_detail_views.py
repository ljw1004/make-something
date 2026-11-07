"""Render genuine whole/detail whale views without removing occluding geometry.

The JSON queue supplies named requests, canonical/revised identity, camera,
resolution and optional explicit hatch pose. A watch process reuses the costly
model while inspecting camera pilots; set queue.finish after the final request.
No standalone selectors, inspection part poses or material overrides apply.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import part_views as V
import assembly_views as A
import bpy
import presentation as P
import scene_parts as S
from mathutils import Vector

parser = argparse.ArgumentParser()
parser.add_argument('--queue', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--catalogue', required=True)
parser.add_argument('--source-catalogue', required=True)
parser.add_argument('--presentations', default=str(HERE/'part-presentations.json'))
parser.add_argument('--watch', action='store_true')
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
items = {i['id']: i for i in json.loads(Path(args.catalogue).read_text())['items']}
original = {i['id']: i for i in json.loads(Path(args.source_catalogue).read_text())['items']}
plans = {i['id']: i for i in json.loads(Path(args.presentations).read_text())['items']}
source_paths = list(HERE.glob('*.py'))+list(V.BASE_ART.glob('*.py'))+[Path(args.presentations), Path(args.catalogue), Path(args.source_catalogue)]
before = {str(p.relative_to(V.repository_root()) if p.is_absolute() else p): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = S.configure_render(960)
scene.render.threads_mode = 'FIXED'
scene.render.threads = 2
scene.cycles.samples = 24
bpy.context.view_layer.update()
model = P.build('whale')
A.prepare(model)
records, seen = [], set()
print('DETAIL MODEL READY', flush=True)
while True:
    queue = json.loads(Path(args.queue).read_text())
    for request in queue['requests']:
        name = request['name']
        if name in seen:
            continue
        if (out/(name+'.png')).exists():
            raise ValueError('Never overwrite a previous pilot or master: '+name)
        prior_lamp = scene.objects.get('exterior hatch inspection fill')
        if prior_lamp:
            data = prior_lamp.data
            bpy.data.objects.remove(prior_lamp, do_unlink=True)
            bpy.data.lights.remove(data)
        identity = request['id']
        item, plan = items[identity], plans[identity]
        canonical = original[plan.get('canonical_id', identity)]
        canonical_view = P.stage(model, canonical, 'whale')
        A.stage(model, item, 'whale', plan, canonical)
        canonical_hatch = math.degrees(model['hatch'].rotation_euler.x)
        if 'hatch_degrees' in request:
            degrees = request['hatch_degrees']
            if not 0 <= degrees <= 110:
                raise ValueError('Outside actual hatch travel')
            # Only the existing door hinge rotates. Do not change hidden
            # handles, machine settings, materials or other fitted parts.
            model['hatch'].rotation_euler.x = math.radians(degrees)
        bpy.context.view_layer.update()
        view = request['view']
        V.inspection_lights(scene, view)
        if request.get('light_side') == '+Y':
            target = Vector(view['target'])
            for light in scene.objects:
                if light.type == 'LIGHT':
                    delta = light.location-target
                    light.location = target+Vector((-delta.x, -delta.y, delta.z))
                    S.look_at(light, target)
        if request.get('inspection_light'):
            specification = request['inspection_light']
            data = bpy.data.lights.new('exterior hatch inspection fill', 'AREA')
            data.energy = specification['energy']
            data.shape = 'DISK'
            data.size = specification['size']
            lamp = bpy.data.objects.new('exterior hatch inspection fill', data)
            scene.collection.objects.link(lamp)
            lamp.location = specification['location']
            S.look_at(lamp, specification['target'])
        resolution = request.get('resolution', 640)
        scene.render.resolution_x = scene.render.resolution_y = resolution
        camera = S.camera('truthful whale detail', view['location'], view['target'], view['scale'])
        scene.camera = camera
        scene.render.filepath = str(out/(name+'.png'))
        bpy.ops.render.render(write_still=True)
        bpy.data.objects.remove(camera, do_unlink=True)
        visible = V.visible_geometry(model)
        records.append({'name': name, 'id': identity, 'canonicalIdentity': canonical['id'],
                        'request': request, 'canonicalView': canonical_view,
                        'canonicalHatchDegrees': canonical_hatch,
                        'renderedHatchDegrees': math.degrees(model['hatch'].rotation_euler.x),
                        'visibleObjects': len(visible), 'removedOccluders': False,
                        'lighting': [{'name': light.name, 'location': list(light.location),
                                      'rotationEuler': list(light.rotation_euler),
                                      'energy': light.data.energy, 'size': light.data.size}
                                     for light in scene.objects if light.type == 'LIGHT'],
                        'assembly': model['_builder_assembly_record'],
                        'sha256': hashlib.sha256((out/(name+'.png')).read_bytes()).hexdigest()})
        seen.add(name)
        (out/'manifest-detail.json').write_text(json.dumps({'images': records, 'sourceFilesBefore': before}, indent=2)+'\n')
        print('DETAIL RENDERED', name, flush=True)
    if queue.get('finish') or not args.watch:
        break
    time.sleep(1)
after = {name: hashlib.sha256((V.repository_root()/name).read_bytes()).hexdigest() for name in before}
dependencies = {str(Path(module.__file__).resolve().relative_to(V.repository_root()))
                for module in tuple(sys.modules.values()) if getattr(module, '__file__', None)
                and Path(module.__file__).resolve().parent in {HERE, V.BASE_ART}}
dependencies.update(str(Path(path).resolve().relative_to(V.repository_root()))
                    for path in [args.presentations, args.catalogue, args.source_catalogue])
changed = [name for name in before if before[name] != after[name]]
changed_dependencies = sorted(set(changed) & dependencies)
(out/'manifest-detail.json').write_text(json.dumps({'images': records, 'sourceFilesBefore': before,
                                                   'sourceFilesAfter': after,
                                                   'renderDependencyFiles': sorted(dependencies),
                                                   'changedRenderFiles': changed_dependencies,
                                                   'changedNonRenderFiles': sorted(set(changed)-dependencies)}, indent=2)+'\n')
if changed_dependencies:
    raise ValueError('Render dependencies changed during the run: '+repr(changed_dependencies))
print('DETAIL RUN COMPLETE', len(records), flush=True)
