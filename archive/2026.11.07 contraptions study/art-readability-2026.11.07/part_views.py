"""Explicit standalone inspection views of the unchanged Builder models.

These selectors change presentation only. They never resize fitted geometry or
quietly replace a supply with a generic drawing. A representative repeated part
must be selected explicitly; heterogeneous supplies need an authored decision.
"""
from pathlib import Path
from contextlib import contextmanager
import math
import re
import sys


def repository_root():
    for parent in Path(__file__).resolve().parents:
        if (parent / 'src/story/parser.ts').is_file():
            return parent
    raise RuntimeError('Cannot locate the Combination Challenge repository')


BASE_ART = repository_root() / 'archive/2026.11.07 builder study/art'
if str(BASE_ART) not in sys.path:
    sys.path.insert(0, str(BASE_ART))


# These small pilots are explicit authored selections, not heuristic fallbacks.
PILOTS = {
    'pw-axle': {'selection': {}, 'representation': 'The actual axle with its on-shaft washers and retaining caps.'},
    'wr-bearings': {'selection': {'center_region': {'axis': 'x', 'max': 0}},
                    'representation': 'One complete bearing tube with its attached saddles, representing the identical pair.'},
    'wr-wheelset': {'selection': {'subtree': {'key': 'axles', 'index': 0}},
                    'representation': 'One captive axle with its two attached wheels, representing the identical axle units.'},
    'cd-bearing-frames': {'selection': {'center_region': {'axis': 'y', 'max': 0}},
                          'representation': 'One bearing frame with its captive mounting screws, representing the pair.'},
    'cd-shaft': {'selection': {'exclude_prefixes': ['shaft cap parking']},
                 'representation': 'The original shaft with its seated collars and retained end cap; parking fixture omitted.'},
    'cd-double-cam': {'selection': {'exclude_prefixes': ['cam parking']},
                      'representation': 'The actual double cam and attached split hub, without its separate parking clip.'},
    'drawing-rover': {'selection': {'subtree': {'key': 'vehicle'}},
                       'representation': 'The complete connected rover; detached drawing paper and test fixtures stay in their use scenes.'},
}


def visible_geometry(model):
    return list(dict.fromkeys(obj for group in model['parts'].values() for obj in group
                              if obj.type in {'MESH', 'CURVE', 'FONT'} and not obj.hide_render))


def corners_world(obj):
    from mathutils import Vector
    return [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]


def _under(obj, ancestor):
    while obj:
        if obj == ancestor:
            return True
        obj = obj.parent
    return False


@contextmanager
def inspection_pose(model, identity, plan):
    """Apply a named reversible physical pose without changing canonical state.

    A supplied removable lid may be closed for its inventory view. This is an
    existing permitted motion, not a new part or a change to fitted dimensions.
    The original transform is restored before the next item in the batch.
    """
    import bpy
    pose = plan.get('pose')
    changed = []
    try:
        if pose == 'closed-empty-cell':
            if identity != 'ka-cell':
                raise ValueError('closed-empty-cell is only defined for ka-cell')
            lids = [o for o in model['parts']['ka-cell'] if 'closed_y' in o]
            if len(lids) != 1:
                raise ValueError('Expected exactly one canonical cell lid')
            for lid in lids:
                changed.append((lid, lid.matrix_basis.copy()))
                lid.location.y = lid['closed_y']
        elif pose == 'closed-empty-remote':
            if identity != 'rover-remote':
                raise ValueError('closed-empty-remote is only defined for rover-remote')
            hatch = model['hatch']
            changed.append((hatch, hatch.matrix_basis.copy()))
            hatch.location.z = -.0015
        elif pose:
            from part_poses import apply_pose
            from inspection_v2_poses import SUPPORTED, apply_pose as refined_pose
            pose_handler = refined_pose if pose in SUPPORTED else apply_pose
            with pose_handler(model, identity, pose):
                bpy.context.view_layer.update()
                yield
            return
        bpy.context.view_layer.update()
        yield
    finally:
        for obj, matrix in changed:
            obj.matrix_basis = matrix
        bpy.context.view_layer.update()


def select(model, identity, plan):
    """Apply an explicit visibility selector after canonical state selection."""
    import bpy
    if 'selection' not in plan:
        raise ValueError(f'{identity}: explicit selection is required (use {{}} to retain all visible geometry)')
    selection = plan['selection']
    allowed_keys = {'include_parts', 'exclude_parts', 'include_prefixes', 'exclude_prefixes',
                    'include_regex', 'exclude_regex', 'center_region', 'subtree'}
    unknown = set(selection) - allowed_keys
    if unknown:
        raise ValueError(f'{identity}: unsupported selection keys {sorted(unknown)}')
    bpy.context.view_layer.update()
    original = visible_geometry(model)
    keep = list(original)
    for field, negate in [('include_parts', False), ('exclude_parts', True)]:
        if field in selection:
            values = set(selection[field])
            keep = [o for o in keep if (o.get('part_id') in values) != negate]
    for field, negate in [('include_prefixes', False), ('exclude_prefixes', True)]:
        if field in selection:
            prefixes = tuple(selection[field])
            keep = [o for o in keep if o.name.startswith(prefixes) != negate]
    for field, negate in [('include_regex', False), ('exclude_regex', True)]:
        if field in selection:
            patterns = [re.compile(s) for s in selection[field]]
            keep = [o for o in keep if any(p.search(o.name) for p in patterns) != negate]
    if 'subtree' in selection:
        sub = selection['subtree']
        ancestor = model[sub['key']]
        if 'index' in sub:
            ancestor = ancestor[sub['index']]
        keep = [o for o in keep if _under(o, ancestor)]
    if 'center_region' in selection:
        region = selection['center_region']
        axis = 'xyz'.index(region['axis'])
        lower, upper = region.get('min', -math.inf), region.get('max', math.inf)
        def inside(obj):
            coordinates = [p[axis] for p in corners_world(obj)]
            return lower <= (min(coordinates)+max(coordinates))/2 <= upper
        keep = [o for o in keep if inside(o)]
    if not keep:
        raise ValueError(f'{identity}: selector removed every visible object')
    keep_set = set(keep)
    for obj in original:
        obj.hide_render = obj not in keep_set
    bpy.context.view_layer.update()
    return keep, {'beforeObjects': len(original), 'selectedObjects': len(keep),
                  'selectedNames': [o.name for o in keep],
                  'selectedParts': sorted({o.get('part_id', '') for o in keep}),
                  'selection': selection, 'pose': plan.get('pose'),
                  'poseEvidence': model.get('inspection_pose_evidence'),
                  'representation': plan.get('representation', '')}


def geometry_inventory(model):
    """Expose model names and evaluated bounds for authoring exact selectors."""
    import bpy
    bpy.context.view_layer.update()
    records = []
    for obj in visible_geometry(model):
        corners = corners_world(obj)
        entry = {'name': obj.name, 'part': obj.get('part_id'), 'parent': obj.parent.name if obj.parent else None,
                 'bounds': [[min(p[i] for p in corners), max(p[i] for p in corners)] for i in range(3)]}
        if obj.type == 'CURVE':
            entry['curveLength'] = sum(spline.calc_length() for spline in obj.data.splines)
        records.append(entry)
    return records


def inspection_view(objects, original_view, direction=None, fill=.85):
    """Fit projected bounds at constant object dimensions into a square view."""
    from mathutils import Vector
    if not .5 <= fill <= .92:
        raise ValueError('Inspection fill must stay between .5 and .92')
    forward = Vector(direction) if direction else Vector(original_view['location'])-Vector(original_view['target'])
    forward.normalize()
    rotation = (-forward).to_track_quat('-Z', 'Y')
    right, up = rotation @ Vector((1, 0, 0)), rotation @ Vector((0, 1, 0))
    points = [p for obj in objects for p in corners_world(obj)]
    basis_bounds = [[min(p.dot(axis) for p in points), max(p.dot(axis) for p in points)]
                    for axis in (right, up, forward)]
    centre = sum((axis*((bound[0]+bound[1])/2) for axis, bound in zip((right, up, forward), basis_bounds)), Vector())
    spans = [bound[1]-bound[0] for bound in basis_bounds]
    scale = max(spans[:2]) / fill
    distance = max(.25, max(spans)*3)
    return {'location': tuple(centre+forward*distance), 'target': tuple(centre),
            'scale': scale, 'projectedSpans': spans, 'fill': fill}


def inspection_lights(scene, view):
    """Move and scale the two studio lights around the inspected real object."""
    from mathutils import Vector
    import scene_parts as S
    target = Vector(view['target'])
    scale = max(.10, view['scale']/.35)
    for name, offset, power, size in [
        ('large soft key', (-.5, -.6, .65), 28, .7),
        ('soft fill', (.4, .2, .35), 16, .5),
    ]:
        light = scene.objects.get(name)
        if light is None:
            raise ValueError('Canonical studio light is missing: '+name)
        light.location = target + Vector(offset)*scale
        light.data.energy = power*scale*scale
        light.data.size = size*scale
        S.look_at(light, target)
