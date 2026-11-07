"""Developable open-coil inspections of the existing animation-strip paper.

The paper's neutral long edges keep their original length, and every short edge
keeps its original width. Original drawing strokes are transported onto that
same surface in their original order. No enlarged inset or duplicate panel is
introduced. Installed drum states never use this pose.
"""
import math

STRIP_IDS = ('film-blank-strip', 'film-key-poses', 'film-drawn-strip', 'film-coloured-strip')
PAPER_RADIUS = .0892
PICTURE_LENGTH = math.tau*PAPER_RADIUS
TAB_LENGTH = .008
LENGTH = PICTURE_LENGTH+TAB_LENGTH
BOTTOM, TOP = .044, .095
WIDTH = TOP-BOTTOM


def spiral_route(length=LENGTH, inner_radius=.030, growth=.0035, phase=-.8, step=.0004):
    """Piecewise developable route with exactly the requested edge length.

    Arc-length inversion chooses each segment's heading on an Archimedean
    spiral. Integration uses unit tangents and fixed chord lengths, avoiding
    the length loss of substituting chords for a continuous arc afterward.
    """
    def integral(theta):
        radius = inner_radius+growth*theta
        return (radius*math.sqrt(radius*radius+growth*growth)+growth*growth*math.asinh(radius/growth))/(2*growth)
    start = integral(0.)
    def theta_at(distance):
        lo, hi = 0., length/inner_radius
        for _ in range(45):
            mid = (lo+hi)/2
            if integral(mid)-start < distance:
                lo = mid
            else:
                hi = mid
        return (lo+hi)/2
    count = math.ceil(length/step)
    pitch = length/count
    points = [(inner_radius*math.sin(phase), inner_radius*math.cos(phase))]
    for i in range(count):
        theta = theta_at((i+.5)*pitch)
        radius = inner_radius+growth*theta
        angle = theta+phase
        dx = growth*math.sin(angle)+radius*math.cos(angle)
        dy = growth*math.cos(angle)-radius*math.sin(angle)
        norm = math.hypot(dx, dy)
        points.append((points[-1][0]+pitch*dx/norm, points[-1][1]+pitch*dy/norm))
    return {'points': points, 'pitch': pitch, 'length': length,
            'innerRadius': inner_radius, 'radialGrowthPerTurn': math.tau*growth,
            'phase': phase, 'segments': count}


def mapped_point(route, flat):
    """Flat source coordinates to neutral surface plus original face offset."""
    x, offset, z = flat
    distance = x+math.pi*PAPER_RADIUS
    if not -1e-6 <= distance <= LENGTH+1e-6:
        raise ValueError('Source drawing lies outside the original paper length')
    distance = min(LENGTH, max(0., distance))
    index = min(route['segments']-1, int(distance/route['pitch']))
    fraction = (distance-index*route['pitch'])/route['pitch']
    a, b = route['points'][index:index+2]
    tx = (b[0]-a[0])/route['pitch']
    ty = (b[1]-a[1])/route['pitch']
    return (a[0]+fraction*(b[0]-a[0])-offset*ty,
            a[1]+fraction*(b[1]-a[1])+offset*tx, z)


def _clip_print(polygon):
    """Clip the original stroke footprint to the real paper, like printed ink."""
    for axis, bound, lower in [(0, -math.pi*PAPER_RADIUS, True),
                               (0, LENGTH-math.pi*PAPER_RADIUS, False),
                               (1, BOTTOM, True), (1, TOP, False)]:
        if not polygon:
            break
        result = []
        for a, b in zip(polygon, polygon[1:]+polygon[:1]):
            inside_a = a[axis] >= bound if lower else a[axis] <= bound
            inside_b = b[axis] >= bound if lower else b[axis] <= bound
            if inside_a:
                result.append(a)
            if inside_a != inside_b:
                fraction = (bound-a[axis])/(b[axis]-a[axis])
                result.append(tuple(a[j]+fraction*(b[j]-a[j]) for j in range(2)))
        polygon = result
    return polygon


def _printed_stroke(model, original, polylines, route):
    """Same centreline/width as the source tube, printed on its intended face.

    Tube radii in the canonical illustration are wider than half the paper
    thickness. Converting their footprint to ink avoids drawing through both
    faces or leaving strokes floating beyond an edge in the close inspection.
    """
    import bpy
    vertices, faces = [], []
    radius = original.data.bevel_depth
    def polygon(points):
        clipped = _clip_print(points)
        if len(clipped) < 3:
            return
        start = len(vertices)
        vertices.extend(mapped_point(route, (x, -.00026, z)) for x, z in clipped)
        faces.append(tuple(range(start, len(vertices))))
    for points in polylines:
        for a, b in zip(points, points[1:]):
            dx, dz = b.x-a.x, b.z-a.z
            distance = math.hypot(dx, dz)
            if distance < 1e-10:
                continue
            nx, nz = -dz*radius/distance, dx*radius/distance
            count = max(1, math.ceil(abs(dx)/route['pitch']))
            for j in range(count):
                p = a+(b-a)*(j/count)
                q = a+(b-a)*((j+1)/count)
                polygon([(p.x+nx, p.z+nz), (q.x+nx, q.z+nz),
                         (q.x-nx, q.z-nz), (p.x-nx, p.z-nz)])
        for p in points:
            polygon([(p.x+radius*math.cos(t*math.tau/16), p.z+radius*math.sin(t*math.tau/16)) for t in range(16)])
    mesh = bpy.data.meshes.new(original.name+' printed footprint')
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    ink = bpy.data.objects.new(original.name+' printed on paper', mesh)
    bpy.context.collection.objects.link(ink)
    ink.parent = model['rotor']
    ink['part_id'] = 'film-blank-strip'
    for material in original.data.materials:
        mesh.materials.append(material)
    model['parts']['film-blank-strip'].append(ink)
    model['generated'].append(ink)
    original.hide_render = True
    original.hide_set(True)


def apply(model, identity, route=None):
    import bpy
    from mathutils import Matrix
    if identity not in STRIP_IDS:
        raise ValueError('Only the four loose strip states have an open-coil pose')
    route = route or spiral_route()
    objects = [o for o in model['generated'] if o.get('part_id') == 'film-blank-strip']
    paper = next(o for o in objects if o.name.startswith('picture strip paper'))
    tab = next(o for o in objects if o.name.startswith('picture strip overlap tab'))
    if paper.parent != model['rotor'] or tab.parent != model['rotor']:
        raise ValueError('Unexpected canonical paper hierarchy')
    # The two adjacent source patches are one real paper strip, including its
    # 8 mm overlap tab. Their shared neutral surface becomes one continuous
    # mesh so the inspection cannot create a fictitious seam or overlap.
    points = route['points']
    n = len(points)
    vertices = [(x, y, z) for z in (BOTTOM, TOP) for x, y in points]
    faces = [(i, i+1, n+i+1, n+i) for i in range(n-1)]
    paper.data.clear_geometry()
    paper.data.from_pydata(vertices, [], faces)
    paper.data.update()
    paper.matrix_basis = Matrix.Identity(4)
    tab.hide_render = True
    tab.hide_set(True)
    mark_names = []
    source_point_counts = {}
    for obj in objects:
        if obj.type != 'CURVE':
            continue
        if obj.parent != model['rotor']:
            raise ValueError('Unexpected canonical drawing hierarchy')
        matrix = obj.matrix_local.copy()
        original_splines = []
        for spline in obj.data.splines:
            if spline.type != 'POLY':
                raise ValueError('Expected the canonical polygonal drawing strokes')
            original_splines.append([matrix @ p.co.to_3d() for p in spline.points])
        source_point_counts[obj.name] = sum(len(p) for p in original_splines)
        _printed_stroke(model, obj, original_splines, route)
        mark_names.append(obj.name)
    bpy.context.view_layer.update()
    # Read back the rendered mesh coordinates, including Blender float storage.
    actual = [paper.data.vertices[i].co for i in range(n)]
    measured = sum((b-a).length for a, b in zip(actual, actual[1:]))
    measured_widths = [(paper.data.vertices[i+n].co-paper.data.vertices[i].co).length for i in range(n)]
    if abs(measured-LENGTH) > 1e-6 or max(abs(w-WIDTH) for w in measured_widths) > 1e-7:
        raise ValueError('Paper inspection failed its physical length/width check')
    return {'identity': identity, 'neutralLengthM': LENGTH, 'meshEdgeLengthM': measured,
            'widthM': WIDTH, 'measuredWidthRangeM': [min(measured_widths), max(measured_widths)],
            'originalTabLengthM': TAB_LENGTH, 'originalFrameCount': 12,
            'transportedMarks': mark_names, 'sourcePointCounts': source_point_counts,
            'route': {k: v for k, v in route.items() if k != 'points'},
            'inkTreatment': 'Original stroke footprints and widths printed on intended paper face and clipped at real edges',
            'paperSurfaceObjects': 1, 'installedStatesChanged': False}
