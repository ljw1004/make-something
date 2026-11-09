"""Explicit physical refinements requested by the final native-size review."""
from contextlib import contextmanager
import math
import part_poses as K

SUPPORTED = frozenset({'coiled-crane-rope', 'coiled-power-divider',
                       'readable-stop-cord', 'single-dragon-section', 'underside-caster'})


def _coil(length, radius, wire_radius, before=.035, after=.035, pitch=None):
    if pitch is None:
        return K.coil_points(length, radius, wire_radius, before, after)
    available = length-before-after
    turns = max(.5, round(available/(math.tau*radius)-.5)+.5)
    segments = int(turns*96)
    dz = pitch/96
    radius = math.sqrt((available/segments)**2-dz*dz)/(2*math.sin(math.pi/96))
    points = [(radius, -before, 0.)]
    points += [(radius*math.cos(i*math.tau/96), radius*math.sin(i*math.tau/96), i*dz)
               for i in range(segments+1)]
    points.append((-radius, -after, turns*pitch))
    if abs(K.polyline_length(points)-length) > 1e-8:
        raise ValueError('Refined coil did not preserve line length')
    return points


def _along(points, distance):
    for a, b in zip(points, points[1:]):
        length = (b-a).length
        if distance <= length:
            return a+(b-a)*(distance/length), (b-a).normalized()
        distance -= length
    return points[-1], (points[-1]-points[-2]).normalized()


def _nearest_distance(points, point):
    best, answer, travelled = math.inf, None, 0.
    for a, b in zip(points, points[1:]):
        delta = b-a
        fraction = max(0., min(1., (point-a).dot(delta)/delta.length_squared))
        error = (a+fraction*delta-point).length
        if error < best:
            best, answer = error, travelled+fraction*delta.length
        travelled += delta.length
    if best > 1e-5:
        raise ValueError('A supplied grommet is not on its canonical cable centreline')
    return answer


def _components(mesh):
    adjacent = {v.index: set() for v in mesh.vertices}
    for edge in mesh.edges:
        a, b = edge.vertices
        adjacent[a].add(b)
        adjacent[b].add(a)
    unseen, result = set(adjacent), []
    while unseen:
        found, queue = set(), [next(iter(unseen))]
        while queue:
            vertex = queue.pop()
            if vertex in found:
                continue
            found.add(vertex)
            queue.extend(adjacent[vertex]-found)
        unseen.difference_update(found)
        result.append(found)
    return result


@contextmanager
def apply_pose(model, identity, name):
    import bpy
    from mathutils import Matrix, Vector
    pose = K.Pose(model)
    meshes, visibility = [], []
    previous = model.get('inspection_pose_evidence')
    extra = []
    try:
        if identity == 'rover-caster' and name == 'underside-caster':
            objects = list(dict.fromkeys(model['parts']['rover-caster']))
            pivot = Vector((.080, 0., .025))
            pose.rigid_move(objects, pivot, pivot, rotation=Matrix.Rotation(math.pi, 4, 'X'))
            extra.append({'rigidInspectionTurnDegrees': 180, 'axis': 'X',
                          'objects': len(objects), 'dimensionsAndMaterialsUnchanged': True})
        elif identity == 'lc-rope' and name == 'coiled-crane-rope':
            curve = model['rope']
            original = K._world_points(curve)
            points = _coil(K.polyline_length(original), .028, curve.data.bevel_depth, .018, .035)
            anchor = K._find(model, 'closed cord anchor loop and fixed tail')
            pose.rigid_move([anchor], original[0], points[0])
            pose.rigid_move([model['hook']], original[-1], points[-1])
            pose.route(curve, points)
        elif identity == 'flight-stop-cord' and name == 'readable-stop-cord':
            curve = model['stop_cord']
            original = K._world_points(curve)
            points = _coil(K.polyline_length(original), .040, curve.data.bevel_depth, .022, .025)
            grip = K._find(model, 'stop cord hand grip')
            mechanism = [obj for obj in model['parts']['flight-stop-cord']
                         if obj.type in {'MESH', 'CURVE'} and obj not in {grip, curve}]
            pose.rigid_move(mechanism, original[0], points[0], math.pi)
            pose.rigid_move([grip], original[-1], points[-1])
            pose.route(curve, points)
        elif identity == 'fair-power-divider' and name == 'coiled-power-divider':
            for index, label in enumerate(['clipped motor output cable', 'theatre lamp lead through prepared deck and floor bores']):
                curve = K._exact(model, label)
                original = K._world_points(curve)
                points = _coil(K.polyline_length(original), .025, curve.data.bevel_depth, pitch=.022)
                rotation = Matrix.Rotation(math.pi, 4, 'X' if index == 0 else 'Z')
                transformed = [rotation @ Vector(p) for p in points]
                offset = original[0]-transformed[0]
                transformed = [p+offset for p in transformed]
                suffix = '' if index == 0 else '.001'
                grommet = K._exact(model, 'cable through-hole retaining grommet'+suffix)
                arm = K._exact(model, 'grommet bearing arm to deck underside'+suffix)
                old_centre = grommet.matrix_world.translation.copy()
                distance = _nearest_distance(original, old_centre)
                _, old_tangent = _along(original, distance)
                new_centre, new_tangent = _along(transformed, distance)
                turn = old_tangent.rotation_difference(new_tangent).to_matrix().to_4x4()
                pose.rigid_move([grommet, arm], old_centre, new_centre, rotation=turn)
                if index == 1:
                    plug = [K._exact(model, 'lamp matching plug into retained socket'), K._exact(model, 'lamp plug strain relief')]
                    turn = (original[-1]-original[-2]).normalized().rotation_difference((transformed[-1]-transformed[-2]).normalized()).to_matrix().to_4x4()
                    pose.rigid_move(plug, original[-1], transformed[-1], rotation=turn)
                pose.route(curve, transformed)
                extra.append({'grommet': grommet.name, 'distanceAlongCableM': distance,
                              'clipAndArmMovedRigidly': True, 'coilPitchM': .022})
        elif identity == 'fair-dragon-bracket' and name == 'single-dragon-section':
            for obj in model['parts']['fair-dragon-bracket']:
                if obj.name.startswith('dragon mounting spreader'):
                    components = _components(obj.data)
                    if len(components) != 2:
                        raise ValueError('Expected the two actual sections left by the canonical relief cut')
                    selected = [component for component in components
                                if sum((obj.matrix_world @ obj.data.vertices[i].co).x for i in component)/len(component) > -.245]
                    if len(selected) != 1:
                        raise ValueError('Cannot identify the actual long mounting section')
                    selected = selected[0]
                    old = obj.data
                    mesh = bpy.data.meshes.new(old.name+' single actual mounting section')
                    order = sorted(selected)
                    lookup = {old_index: new_index for new_index, old_index in enumerate(order)}
                    faces = [[lookup[i] for i in face.vertices] for face in old.polygons if set(face.vertices).issubset(selected)]
                    mesh.from_pydata([old.vertices[i].co[:] for i in order], [], faces)
                    mesh.update()
                    for material in old.materials:
                        mesh.materials.append(material)
                    meshes.append((obj, old))
                    obj.data = mesh
                    extra.append({'mesh': obj.name, 'sourceComponents': 2, 'retainedComponents': 1,
                                  'retainedVerticesUnchanged': True, 'sourceReliefCentreX': -.245})
                elif obj.matrix_world.translation.x < -.245:
                    visibility.append((obj, obj.hide_render))
                    obj.hide_render = True
        else:
            raise ValueError(f'{identity}: unsupported reviewed refinement pose {name}')
        model['inspection_pose_evidence'] = pose.evidence+extra
        bpy.context.view_layer.update()
        yield
    finally:
        pose.restore()
        for obj, old in meshes:
            temporary = obj.data
            obj.data = old
            bpy.data.meshes.remove(temporary)
        for obj, hidden in visibility:
            obj.hide_render = hidden
        model['inspection_pose_evidence'] = previous
        bpy.context.view_layer.update()
