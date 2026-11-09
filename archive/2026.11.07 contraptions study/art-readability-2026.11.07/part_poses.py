"""Compact, reversible inspection poses for existing flexible Builder leads.

Only curve routes and rigid placement change. Cable radii, cable lengths,
connectors, controls and all fitted geometry remain the canonical dimensions.
These are loose inventory poses; they are never used for installed machines.
"""
from contextlib import contextmanager
import math


def polyline_length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def coil_points(length, radius_hint, cord_radius, lead_in=.025, lead_out=.025,
                exit_drop=0., base_z=0.):
    """A half-turn-ended helix with the exact original polygonal arc length.

    Half turns leave the two ends on opposite sides of the bundle. Its pitch
    exceeds the cord diameter, so adjacent turns cannot intersect. Solving the
    radius from the discrete segment length avoids a smooth-arc approximation.
    """
    tail_length = lead_in + math.hypot(lead_out, exit_drop)
    available = length-tail_length
    if available <= 0:
        raise ValueError('Cord is shorter than the requested compact pose tails')
    turns = max(.5, round(available/(2*math.pi*radius_hint)-.5)+.5)
    pitch = cord_radius*2.8
    segments = int(turns*96)
    dz = pitch/96
    per_segment = available/segments
    if per_segment <= dz:
        raise ValueError('Requested compact coil has insufficient length for its pitch')
    radius = math.sqrt(per_segment**2-dz**2)/(2*math.sin(math.pi/96))
    points = [(radius, -lead_in, base_z)]
    for i in range(segments+1):
        angle = i*2*math.pi/96
        points.append((radius*math.cos(angle), radius*math.sin(angle), base_z+i*dz))
    points.append((-radius, -lead_out, base_z+turns*pitch+exit_drop))
    if abs(polyline_length(points)-length) > 1e-9:
        raise AssertionError('Compact cord route failed exact length check')
    return points


def _world_points(curve):
    if len(curve.data.splines) != 1 or curve.data.splines[0].type != 'POLY':
        raise ValueError('Compact inspection expects one canonical polyline')
    return [curve.matrix_world @ p.co.to_3d() for p in curve.data.splines[0].points]


def _find(model, prefix):
    matches = [obj for group in model['parts'].values() for obj in group if obj.name.startswith(prefix)]
    matches = list(dict.fromkeys(matches))
    if len(matches) != 1:
        raise ValueError(f'Expected exactly one source object starting {prefix!r}, got {len(matches)}')
    return matches[0]


def _exact(model, name):
    matches = list(dict.fromkeys(obj for group in model['parts'].values() for obj in group if obj.name == name))
    if len(matches) != 1:
        raise ValueError(f'Expected one source object named {name!r}, got {len(matches)}')
    return matches[0]


class Pose:
    def __init__(self, model):
        self.model = model
        self.transforms = {}
        self.curves = {}
        self.evidence = []

    def rigid_move(self, objects, before, after, angle=0., rotation=None):
        from mathutils import Matrix, Vector
        rotation = rotation if rotation is not None else Matrix.Rotation(angle, 4, 'Z')
        transform = Matrix.Translation(Vector(after)) @ rotation @ Matrix.Translation(-Vector(before))
        # Cache all original world matrices before changing any hierarchy.
        snapshots = {obj: obj.matrix_world.copy() for obj in objects}
        for obj in objects:
            self.transforms.setdefault(obj, obj.matrix_basis.copy())
        for obj, matrix in snapshots.items():
            obj.matrix_world = transform @ matrix

    def route(self, curve, points):
        from mathutils import Vector
        before = _world_points(curve)
        if curve not in self.curves:
            self.curves[curve] = curve.data
            curve.data = curve.data.copy()
        inverse = curve.matrix_world.inverted()
        curve.data.splines.clear()
        spline = curve.data.splines.new('POLY')
        spline.points.add(len(points)-1)
        for target, point in zip(spline.points, points):
            target.co = (*(inverse @ Vector(point)), 1)
        after = _world_points(curve)
        delta = abs(polyline_length(before)-polyline_length(after))
        if delta > 1e-6:
            raise ValueError(f'{curve.name}: compact pose changed length by {delta} m')
        self.evidence.append({'curve': curve.name,
                              'canonicalLengthM': polyline_length(before),
                              'inspectionLengthM': polyline_length(after),
                              'radiusM': curve.data.bevel_depth,
                              'endpointsM': [list(after[0]), list(after[-1])]})

    def restore(self):
        import bpy
        for obj, matrix in self.transforms.items():
            obj.matrix_basis = matrix
        for curve, original in self.curves.items():
            temporary = curve.data
            curve.data = original
            bpy.data.curves.remove(temporary)


@contextmanager
def apply_pose(model, identity, name):
    import bpy
    from mathutils import Vector
    pose = Pose(model)
    previous = model.get('inspection_pose_evidence')
    try:
        if name == 'coiled-brace-cord' and identity == 'whale-brace-cord':
            curve = _find(model, 'anchored diagonal brace cord.001')
            original = _world_points(curve)
            points = coil_points(polyline_length(original), .018, curve.data.bevel_depth, .015, .015)
            pose.route(curve, points)
        elif name == 'coiled-wave-cord' and identity == 'wm-cord':
            curve = model['cord']
            original = _world_points(curve)
            points = coil_points(polyline_length(original), .012, curve.data.bevel_depth, .012, .012)
            for loop, before, after in zip(model['cord_loops'], [original[0], original[-1]], [points[0], points[-1]]):
                pose.rigid_move([loop], before, after)
            pose.route(curve, points)
        elif name == 'coiled-whale-brace' and identity == 'whale-braces':
            curve = _exact(model, 'anchored diagonal brace cord.001')
            original = _world_points(curve)
            points = coil_points(polyline_length(original), .018, curve.data.bevel_depth, .015, .015)
            axis = (original[-1]-original[0]).normalized()
            first_rotation = axis.rotation_difference(Vector((0, 1, 0))).to_matrix().to_4x4()
            final_rotation = axis.rotation_difference(Vector((0, -1, 0))).to_matrix().to_4x4()
            before = [_exact(model, n) for n in ['anchored diagonal brace cord', 'brace loop tied around actual rib', 'inline brace tensioner']]
            after = [_exact(model, 'brace loop tied around actual rib.001')]
            pose.rigid_move(before, original[0], points[0], rotation=first_rotation)
            pose.rigid_move(after, original[-1], points[-1], rotation=final_rotation)
            pose.route(curve, points)
        elif name == 'coiled-harness-extension' and identity == 'whale-harness-extension':
            curve = _find(model, 'supplied 366 mm harness extension alongside strut')
            original = _world_points(curve)
            points = coil_points(polyline_length(original), .018, curve.data.bevel_depth, .015, .015)
            connectors = [_exact(model, n) for n in ['harness extension insulated inline connector', 'harness extension insulated inline connector.001']]
            axis = (original[-1]-original[0]).normalized()
            for connector, before, after, direction in zip(connectors, [original[0], original[-1]], [points[0], points[-1]], [(0, 1, 0), (0, -1, 0)]):
                rotation = axis.rotation_difference(Vector(direction)).to_matrix().to_4x4()
                pose.rigid_move([connector], before, after, rotation=rotation)
            pose.route(curve, points)
        elif name == 'coiled-control-lead' and identity == 'flight-control-lead':
            curve = model['control_lead']
            original = _world_points(curve)
            points = coil_points(polyline_length(original), .040, curve.data.bevel_depth, .025, .045)
            controls = [_find(model, 'long-lead lift hand control'), _find(model, 'lift hand control dial')]
            pose.rigid_move(controls, original[-1], points[-1])
            pose.route(curve, points)
        elif name == 'coiled-stop-cord' and identity == 'flight-stop-cord':
            curve = model['stop_cord']
            original = _world_points(curve)
            points = coil_points(polyline_length(original), .040, curve.data.bevel_depth, .045, .025)
            grip = _find(model, 'stop cord hand grip')
            mechanism = [obj for obj in model['parts']['flight-stop-cord']
                         if obj.type in {'MESH', 'CURVE'} and obj not in {grip, curve}]
            pose.rigid_move(mechanism, original[0], points[0], math.pi)
            pose.rigid_move([grip], original[-1], points[-1])
            pose.route(curve, points)
        elif name == 'coiled-tether' and identity == 'flight-long-tether':
            curve = model['tethers'][0]
            original = _world_points(curve)
            points = coil_points(polyline_length(original), .065, curve.data.bevel_depth,
                                 .050, .045, exit_drop=-.035, base_z=.060)
            clip = [_find(model, 'separated frame tether clip 1'), _find(model, 'tether clip 1 rigid rib bracket')]
            anchor = [_find(model, 'separate weighted garden anchor 1'), _find(model, 'garden anchor eye 1')]
            pose.rigid_move(clip, original[0], points[0], math.pi)
            pose.rigid_move(anchor, original[-1], points[-1])
            pose.route(curve, points)
        elif name == 'coiled-rehearsal-remote' and identity == 'flight-rehearsal-remote':
            curve = model['remote_lead']
            original = _world_points(curve)
            points = coil_points(polyline_length(original), .050, curve.data.bevel_depth, .025, .115)
            panel = [obj for obj in model['parts']['flight-rehearsal-remote']
                     if obj.type in {'MESH', 'CURVE'} and obj != curve]
            pose.rigid_move(panel, original[-1], points[-1])
            pose.route(curve, points)
        else:
            raise ValueError(f'{identity}: unsupported compact inspection pose {name!r}')
        model['inspection_pose_evidence'] = pose.evidence
        bpy.context.view_layer.update()
        yield pose.evidence
    finally:
        pose.restore()
        model['inspection_pose_evidence'] = previous
        bpy.context.view_layer.update()
