"""Render explicit single-unit standalone inspections from canonical models.

Blender --background --factory-startup --python render_parts.py --
  --catalogue FILE --output DIR --ids pw-axle,wr-bearings
  [--presentations FILE] [--resolution 640] [--samples 24] [--threads 2]

The optional presentation file is a list of item entries, {'items': [...]}, or
an object keyed by identity. Entries must supply an explicit selection, even
when it is {}. Without that file only the documented pilot identities exist.
"""
import argparse
from contextlib import nullcontext
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import part_views as V
import bpy
import scene_parts as S
import presentation as P
from construction_lighting import frame_lights
LOADED_SOURCE_HASHES = {}


def assembly_stage(model, item, key, plan, canonical_item):
    if (HERE/'assembly_views.py').is_file():
        import assembly_views
        assembly_views.stage(model, item, key, plan, canonical_item=canonical_item)


def prepare_assembly(model):
    if (HERE/'assembly_views.py').is_file():
        import assembly_views
        assembly_views.prepare(model)


def source_hashes():
    paths = {Path(module.__file__).resolve() for module in tuple(sys.modules.values())
             if getattr(module, '__file__', None)
             and Path(module.__file__).resolve().parent in {HERE, V.BASE_ART}}
    paths.add(Path(__file__).resolve())
    for path in sorted(paths):
        name = str(path.relative_to(V.repository_root()))
        if name not in LOADED_SOURCE_HASHES:
            LOADED_SOURCE_HASHES[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(LOADED_SOURCE_HASHES)


def render_image(scene, key, identity, view, output):
    camera = S.camera('registered construction camera' if args.fixed else 'standalone inspection camera',
                      view['location'], view['target'], view['scale'])
    scene.camera = camera
    bpy.context.view_layer.update()
    scene.render.filepath = str(output/(identity+'.png'))
    context = nullcontext()
    if key == 'theatre':
        from theatre_presentation import inspection_render
        context = inspection_render(scene, identity)
    try:
        with context:
            bpy.ops.render.render(write_still=True)
    finally:
        bpy.data.objects.remove(camera, do_unlink=True)
    return {'pixels': [scene.render.resolution_x, scene.render.resolution_y],
            'lighting': [{'name': light.name, 'location': list(light.location),
                          'rotationEuler': list(light.rotation_euler), 'scale': list(light.scale),
                          'energy': light.data.energy, 'size': light.data.size}
                         for light in scene.objects if light.type == 'LIGHT'],
            'colorManagement': {'viewTransform': scene.view_settings.view_transform,
                                'exposure': scene.view_settings.exposure},
            'sourceHashes': source_hashes(),
            'sha256': hashlib.sha256((output/(identity+'.png')).read_bytes()).hexdigest()}


def render_compound(scene, model, item, canonical_item, key, plan, original_view, output):
    """Owner and all slots share one camera fitted around the completed owner."""
    slots = [slot['accepts'] for slot in item['slots']]
    if key != 'rover' or item['id'] != 'rover-deck' or len(slots) != 5:
        raise ValueError('Registered compound pass expects the five-slot rover deck')
    module = model['stage_module']
    module.set_state(model, canonical_item['id'], slots=slots)
    complete_objects = V.visible_geometry(model)
    view = V.inspection_view(complete_objects, original_view, fill=.85)
    V.inspection_lights(scene, view)
    fitted_names = [obj.name for obj in complete_objects]
    images = []
    module.set_state(model, canonical_item['id'])
    assembly_stage(model, item, key, plan, canonical_item)
    owner_render = render_image(scene, key, item['id'], view, output)
    images.append({'id': item['id'], 'key': key, 'view': view, 'registeredCompound': True,
                   'fitObjects': fitted_names, 'canonicalIdentity': canonical_item['id'], **owner_render})
    for slot in slots:
        # prepare_assembly already reassigned the real stationary support to
        # the owner. The canonical holdout masks therefore include it here.
        module.set_overlay(model, slot)
        identity = item['id']+'--'+slot
        slot_render = render_image(scene, key, identity, view, output)
        images.append({'id': identity, 'key': key, 'owner': item['id'], 'slot': slot,
                       'overlay': True, 'registeredCompound': True, 'view': view, **slot_render})
    proof = output/'proof';proof.mkdir(exist_ok=True)
    module.set_state(model, canonical_item['id'], slots=slots)
    render_image(scene, key, item['id']+'--all-slots', view, proof)
    return images


def plans_from_file(path):
    if not path:
        return dict(V.PILOTS)
    data = json.loads(Path(path).read_text())
    if isinstance(data, dict) and 'items' in data:
        data = data['items']
    if isinstance(data, list):
        data = {entry['id']: entry for entry in data}
    if not isinstance(data, dict):
        raise ValueError('Presentation file must contain entries keyed by identity')
    return data


def write_manifests():
    grouped = {}
    for record in records:
        grouped.setdefault(Path(record.get('outputDirectory', out)), []).append(record)
    for directory, images in grouped.items():
        directory.mkdir(parents=True, exist_ok=True)
        path = directory/(('inventory-' if args.inventory_only else 'manifest-')+batch+'.json')
        path.write_text(json.dumps({'storyHash': catalogue['storyHash'], 'images': images}, indent=2)+'\n')


parser = argparse.ArgumentParser()
parser.add_argument('--catalogue', required=True)
parser.add_argument('--source-catalogue', help='Original catalogue for canonical_id aliases introduced by split recipes')
parser.add_argument('--output', required=True)
parser.add_argument('--presentations')
parser.add_argument('--ids', required=True)
parser.add_argument('--inventory-only', action='store_true', help='Write canonical visible-object names and bounds instead of rendering')
parser.add_argument('--fixed', action='store_true', help='Use canonical registered construction camera, canvas and lighting without loose-part selectors or poses')
parser.add_argument('--fixed-ids', default='', help='Render these IDs in registered mode while sharing family models with other inspection IDs')
parser.add_argument('--fixed-output', help='Separate output directory for --fixed-ids')
parser.add_argument('--compound', action='store_true', help='Render rover deck and five registered overlays using one fully-fitted bounds camera')
parser.add_argument('--resolution', type=int, help='Default 640 for inspections; canonical 960/1200 for fixed views')
parser.add_argument('--samples', type=int, default=24)
parser.add_argument('--threads', type=int, default=2)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
catalogue = json.loads(Path(args.catalogue).read_text())
source_catalogue = json.loads(Path(args.source_catalogue).read_text()) if args.source_catalogue else catalogue
source_items = {item['id']: item for item in source_catalogue['items']}
plans = plans_from_file(args.presentations)
ids = {item['id'] for item in catalogue['items'] if args.ids == 'all' or item['primitive']} if args.ids in {'all', 'primitive'} else set(args.ids.split(','))
fixed_ids = set(args.fixed_ids.split(',')) if args.fixed_ids else set()
if fixed_ids-ids:
    raise ValueError('--fixed-ids must be a subset of --ids')
if fixed_ids and not args.fixed_output:
    raise ValueError('Mixed fixed views require --fixed-output')
items = [item for item in catalogue['items'] if item['id'] in ids]
if {item['id'] for item in items} != ids:
    raise ValueError('Unknown catalogue identities: '+str(sorted(ids-{i['id'] for i in items})))
if not args.inventory_only and ids-set(plans):
    raise ValueError('Missing explicit presentation plans: '+str(sorted(ids-set(plans))))
unresolved = [identity for identity in ids if plans.get(identity, {}).get('status') == 'requires-author-resolution']
if not args.inventory_only and unresolved:
    raise ValueError('Unresolved presentations cannot be rendered: '+str(sorted(unresolved)))
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
batch = hashlib.sha256('\n'.join(sorted(ids)).encode()).hexdigest()[:12]
groups = {}
for item in items:
    canonical_id = plans.get(item['id'], {}).get('canonical_id', item['id'])
    if canonical_id not in source_items:
        raise ValueError(f'{item["id"]}: canonical identity {canonical_id!r} is missing from source catalogue')
    groups.setdefault(P.factory_key(source_items[canonical_id]), []).append((item, source_items[canonical_id]))
records = []
source_hashes()
for key, family in groups.items():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    resolution = args.resolution or ((1200 if key == 'whale' else 960) if args.fixed else 960 if args.compound else 640)
    scene = S.configure_render(resolution)
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = args.threads
    scene.cycles.samples = args.samples
    default_exposure = scene.view_settings.exposure
    # Newly created light matrix_world values remain stale until dependency
    # evaluation. Save the authored transform properties themselves so a
    # later fixed pass cannot restore identity matrices at the world origin.
    bpy.context.view_layer.update()
    studio = [(light, light.location.copy(), light.rotation_euler.copy(), light.scale.copy(),
               light.data.energy, light.data.size)
              for light in scene.objects if light.type == 'LIGHT']
    model = P.build(key)
    prepare_assembly(model)
    source_hashes()
    for item, canonical_item in family:
        # Restore all canonical selection/poses before applying this icon's
        # independent visibility and camera. No fitted model is exported here.
        original_view = P.stage(model, canonical_item, key)
        plan = plans.get(item['id'], {})
        assembly_stage(model, item, key, plan, canonical_item)
        fixed = args.fixed or item['id'] in fixed_ids
        item_output = Path(args.fixed_output) if item['id'] in fixed_ids else out
        item_output.mkdir(parents=True, exist_ok=True)
        resolution = args.resolution or ((1200 if key == 'whale' else 960) if fixed else 960 if args.compound else 640)
        scene.render.resolution_x = scene.render.resolution_y = resolution
        scene.view_settings.exposure = default_exposure if fixed else plan.get('exposure', default_exposure)
        for light, location, rotation, scale, power, size in studio:
            light.location = location
            light.rotation_euler = rotation
            light.scale = scale
            light.data.energy = power
            light.data.size = size
        if args.compound:
            records.extend(render_compound(scene, model, item, canonical_item, key, plan, original_view, out))
            write_manifests()
            print('COMPOUND', item['id'], 'owner and five overlays', flush=True)
            continue
        if args.inventory_only:
            records.append({'id': item['id'], 'key': key, 'objects': V.geometry_inventory(model), 'modelKeys': sorted(model), 'outputDirectory': str(item_output)})
            write_manifests()
            print('INVENTORIED', item['id'], flush=True)
            continue
        if fixed:
            selected = [obj for obj in scene.objects if obj.type in {'MESH', 'CURVE', 'FONT'} and not obj.hide_render]
            view = original_view
            frame_lights(scene, view['scale'])
            selection_record = {'selectedObjects': len(selected), 'selectedNames': [obj.name for obj in selected],
                                'selectedParts': sorted({obj.get('part_id', 'presentation fixture') for obj in selected}),
                                'selection': None, 'pose': None, 'registered': True}
            render_record = render_image(scene, key, item['id'], view, item_output)
        else:
            with V.inspection_pose(model, item['id'], plan):
                selected, selection_record = V.select(model, item['id'], plan)
                view = V.inspection_view(selected, original_view, plan.get('view_direction'), plan.get('fill', .85))
                V.inspection_lights(scene, view)
                render_record = render_image(scene, key, item['id'], view, item_output)
        records.append({'id': item['id'], 'key': key, 'view': view, **selection_record,
                        'originalView': original_view, 'canonicalMaterials': canonical_item['materials'],
                        'canonicalIdentity': canonical_item['id'],
                        'canonicalState': model.get('state', canonical_item['id']),
                        'assembly': model.get('_builder_assembly_record'),
                        'exposure': scene.view_settings.exposure, 'outputDirectory': str(item_output),
                        **render_record})
        print('RENDERED', item['id'], len(selected), 'objects', flush=True)
        write_manifests()
write_manifests()
print('Rendered', len(records), 'explicit standalone part views', flush=True)
