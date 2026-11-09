"""Physical loop adapters shared by the completed ordinary toys.

Rigid motion follows existing controls or explicit shaft pivots. The cord and
elastic returns have prescribed geometric envelopes, not force simulations.
"""
import math
import bpy
from mathutils import Quaternion, Vector


def curve_points(obj, points):
    obj.data.splines.clear()
    spline = obj.data.splines.new('POLY')
    spline.points.add(len(points) - 1)
    for point, co in zip(spline.points, points):
        point.co = (*co, 1)


class Mechanisms:
    def prepare_window(self):
        from future_scene import WindowView
        self.controls['scene'] = WindowView(self.model)

    def pose_window(self, p):
        self.controls['scene'].pose(p)

    def prepare_spinner(self):
        pass

    def pose_spinner(self, p):
        self.module.set_motion(self.model, math.tau*p)

    def prepare_racer(self):
        from adapters import group
        m = self.model
        for side, x in (('front', .075), ('rear', -.075)):
            objects = sum((m['parts'][side + suffix] for suffix in ('-axle', '-wheel-near', '-wheel-far')), [])
            self.controls[side] = group('working ' + side + ' straw axle', objects, m['root'], (x, 0, .030))

    def pose_racer(self, p):
        # A short back-and-forth roll keeps the finished view compact. Reversing
        # wind is prescribed; wheel rotation comes from travelled distance.
        travel = .038 * math.sin(math.tau * p)
        self.model['root'].location.x = travel
        for key in ('front', 'rear'):
            self.controls[key].rotation_euler.y = travel / .030

    def prepare_dragon(self):
        pass

    def pose_dragon(self, p):
        self.model['source'].apply_pose(self.model, .6 + 2 * math.tau * p)

    def prepare_claw(self):
        pass

    def pose_claw(self, p):
        travel = self.model['dimensions'].travel
        self.module.apply_pose(self.model, travel * .5 * (1 - math.cos(2 * math.tau * p)))

    def prepare_carousel(self):
        pass

    def pose_carousel(self, p):
        self.module.set_rotation(self.model, math.tau * p)

    def prepare_drum(self):
        from adapters import group
        m = self.model
        moving = sum((m['parts'][key] for key in ('wall-round', 'tape', 'floor', 'strip-round')), [])
        moving += [obj for obj in m['parts']['bearing']
                   if obj.name.startswith(('turning sleeve', 'rotating support', 'floor socket'))]
        self.controls['drum'] = group('working drum about fixed upright spindle', moving, m['root'])

    def pose_drum(self, p):
        # Three revolutions in 6.4 s; a twelve-slit drum remains visibly turning
        # rather than sampling at exactly one picture pitch per video frame.
        self.controls['drum'].rotation_euler.z = math.tau * 3 * p

    def prepare_pinball(self):
        pass

    def pose_pinball(self, p):
        m = self.model
        # A repeatable rally up the open centre of the second arch. The real
        # right flipper supplies the return at the bottom of each trajectory.
        # Motion is a prescribed demonstration, not a restitution simulation.
        # Contact falls on frames 41 and 89 of the 96-frame loop. The near
        # point is 50 micrometres clear of the evaluated raised paddle surface.
        q = (p * 2 + 7/48) % 1
        distance = min(q, 1-q)
        impact = .5 * (1 + math.cos(math.pi * distance / .065)) if distance < .065 else 0
        m['source'].apply_pose(m, pull=0, flippers=(0, impact), long=False)
        x = .040
        low = -.0938254
        y = low + (.255-low) * 4 * q * (1-q)
        m['marble'].location = (x, y, m['source'].marble_support_height(m, x, y))
        m['marble'].rotation_euler.x = -(y-low) / m['dimensions'].marble_radius

    def prepare_gantry(self):
        from adapters import group
        m = self.model
        rotating_names = ('drum axle', 'keyed split shaft', 'tapered keyed retaining', 'cord drum',
                          'drum flange', 'spring cord clamp', 'connected spring clamp')
        rotating = [obj for obj in m['parts']['drum'] if obj.name.startswith(rotating_names)]
        rotating += m['parts']['ratchet'] + m['parts']['crank']
        self.controls['winch'] = group('working winch shaft and keyed crank', rotating, m['root'], (-.112, 0, .058))
        for key, x in (('side', -.112), ('drop', 0)):
            self.controls[key] = group('working ' + key + ' pulley', m['parts'][key + '-wheel'], m['root'], (x, 0, .258))
        self.controls['basket'] = group('basket hanging on hook', m['parts']['basket'], m['root'])
        self.controls['pawl'] = group('pawl release at real spring leaf',
                                      [obj for obj in m['parts']['pawl'] if obj.name.startswith('pawl tooth')], m['root'])
        self.controls['pawl_leaf'] = next(obj for obj in m['parts']['pawl'] if obj.name.startswith('spring pawl'))
        self.controls['pawl_leaf_rest'] = [tuple(point.co[:3]) for point in self.controls['pawl_leaf'].data.splines[0].points]
        self.controls['rope_rest'] = self.module.rope_path()

    def pose_gantry(self, p):
        m = self.model
        theta = 1.5 * (1 - math.cos(math.tau * p))
        # Helix's fixed 4.5 mm transverse span also counts toward cord length.
        extra = math.hypot(.014 * (math.tau + theta), .0045) - math.hypot(.014 * math.tau, .0045)
        self.controls['winch'].rotation_euler.y = theta
        for key in ('side', 'drop'):
            self.controls[key].rotation_euler.y = -extra / .014
        base = self.controls['rope_rest']
        points = []
        for x, y, z in base[:4]:
            dx, dz = x + .112, z - .058
            points.append((-.112 + dx*math.cos(theta) + dz*math.sin(theta), y,
                           .058 - dx*math.sin(theta) + dz*math.cos(theta)))
        for j in range(129):
            angle = -math.pi - theta + (math.tau + theta) * j / 128
            points.append((-.112 + .014*math.cos(angle), -.0045 + .0045*j/128, .058 + .014*math.sin(angle)))
        points.extend(base[69:-1])
        points.append((.014, 0, .135 + extra))
        curve_points(m['cord'], points)
        for point in m['cord'].data.splines[0].points[:4]:
            point.radius = 1.1 / 1.2
        m['hook'].location.z = .135 + extra
        self.controls['basket'].location.z = extra
        # Release the sprung tooth before lowering. The fixed mounting foot
        # remains fixed; only the spring leaf flexes and its tooth translates.
        def smooth(value):
            value = min(1, max(0, value))
            return value*value*(3-2*value)
        release = .006 * smooth((p-.48)/.02) * smooth((1-p)/.02)
        # The tooth rides each real sawtooth flank on ascent. Intersect its
        # radial contact ray with the same sixteen-tooth polygon as the model.
        angle = .34+theta
        ray = (math.cos(angle), math.sin(angle))
        outline = []
        for j in range(16):
            t = math.tau*j/16
            outline += [(.019*math.cos(t), .019*math.sin(t)),
                        (.016*math.cos(t+.34), .016*math.sin(t+.34))]
        radii = []
        def cross(a, b):
            return a[0]*b[1]-a[1]*b[0]
        for a, b in zip(outline, outline[1:]+outline[:1]):
            edge = (b[0]-a[0], b[1]-a[1])
            denominator = cross(ray, edge)
            if abs(denominator) > 1e-12:
                r = cross(a, edge)/denominator
                t = cross(a, ray)/denominator
                if r > 0 and -1e-8 <= t <= 1+1e-8:
                    radii.append(r)
        lift = max(release, max(radii, default=.016)-.016)
        # A point-contact estimate is insufficient for the finite triangular
        # pawl. Resolve the complete tooth profile against the rotated ratchet,
        # allowing its elastic leaf to lift until the two polygons just clear.
        rotated = [(x*math.cos(theta)+z*math.sin(theta), -x*math.sin(theta)+z*math.cos(theta)) for x, z in outline]
        root = (.016*math.cos(.34), .016*math.sin(.34))
        peak = (.019*math.cos(math.pi/8), .019*math.sin(math.pi/8))
        top = root[1]+(.024-root[0])*(peak[1]-root[1])/(peak[0]-root[0])
        pawl = [root, (.024, .003), (.024, top)]
        def subtract(a, b):
            return (a[0]-b[0], a[1]-b[1])
        def inside(point, polygon):
            result = False
            for a, b in zip(polygon, polygon[1:]+polygon[:1]):
                edge = subtract(b, a)
                relative = subtract(point, a)
                if abs(cross(edge, relative)) < 1e-12 and min(a[0],b[0])-1e-10 <= point[0] <= max(a[0],b[0])+1e-10 and min(a[1],b[1])-1e-10 <= point[1] <= max(a[1],b[1])+1e-10:
                    return False
                if (a[1]>point[1]) != (b[1]>point[1]) and point[0] < a[0]+(point[1]-a[1])*edge[0]/edge[1]:
                    result = not result
            return result
        def overlap(distance):
            points = [(x+math.cos(.34)*distance, z+math.sin(.34)*distance) for x, z in pawl]
            if any(inside(point, rotated) for point in points):
                return True
            for a, b in zip(points, points[1:]+points[:1]):
                edge = subtract(b, a)
                for c, d in zip(rotated, rotated[1:]+rotated[:1]):
                    other = subtract(d, c)
                    denominator = cross(edge, other)
                    if abs(denominator) > 1e-12:
                        first = cross(subtract(c, a), other)/denominator
                        second = cross(subtract(c, a), edge)/denominator
                        if 1e-7 < first < 1-1e-7 and 1e-7 < second < 1-1e-7:
                            return True
            return False
        if overlap(lift):
            lo, hi = lift, .006
            for _ in range(24):
                mid = (lo+hi)/2
                if overlap(mid):
                    lo = mid
                else:
                    hi = mid
            lift = hi+.00002
        displacement = Vector((math.cos(.34)*lift, 0, math.sin(.34)*lift))
        self.controls['pawl'].location = displacement
        rest = self.controls['pawl_leaf_rest']
        curve_points(self.controls['pawl_leaf'], [(x + displacement.x*(i/(len(rest)-1))**2, y,
                                                  z + displacement.z*(i/(len(rest)-1))**2)
                                                  for i, (x, y, z) in enumerate(rest)])

    def prepare_rover(self):
        from adapters import S
        # The line is use context on the work surface, never attached to the
        # vehicle. The real pen retraces it, so the loop has no disappearing ink.
        # 70 mm radius gives +5 / -1 whole wheel turns over this circle. The
        # visible spokes meet exactly at the seam and ink emerges by the deck.
        radius = .070
        self.controls['radius'] = radius
        m = self.model
        m['caster_ball'].rotation_mode = 'QUATERNION'
        bpy.context.view_layer.update()
        nib = m['pen_nib'].matrix_world.translation.copy()
        axle_x = m['dimensions'].axle_x
        self.controls['nib_offset'] = nib.x - axle_x
        points = []
        for i in range(129):
            angle = math.tau * i / 128
            x = axle_x + radius * math.sin(angle) + self.controls['nib_offset'] * math.cos(angle)
            y = radius * (1 - math.cos(angle)) + self.controls['nib_offset'] * math.sin(angle)
            points.append((x, y, .00012))
        self.controls['trace'] = S.stroke('existing pen circle on work surface', points, .00045, 'ink')

    def pose_rover(self, p):
        m = self.model
        d = m['dimensions']
        angle = math.tau * p
        radius = self.controls['radius']
        # Source stores the −Y axle first and negates its angle in apply_pose.
        # On this positive-yaw circle that first wheel is the outer wheel.
        wheels = (-(radius+d.wheel_track/2)*angle/d.wheel_radius,
                  -(radius-d.wheel_track/2)*angle/d.wheel_radius)
        m['_rover_source'].apply_pose(m, wheel_angles=wheels, pen_angle=0,
                                     axle_xy=(d.axle_x+radius*math.sin(angle), radius*(1-math.cos(angle))), yaw=angle)
        # A free ball caster has no steering hinge; its spherical surface rolls.
        caster_axis = Vector((-(d.caster_x-d.axle_x), radius, 0))
        m['caster_ball'].rotation_quaternion = Quaternion(caster_axis.normalized(), angle*caster_axis.length/d.caster_radius)

    def prepare_projector(self):
        from adapters import S
        self.lighting_view = dict(self.view)
        self.cinematic = True
        # A tighter equivalent crop preserves the finished camera direction,
        # while letting the camera visit a separate real image plane. No giant
        # common world-space bounding box is reserved around the finished toy.
        view = self.view
        forward = (Vector(view['target'])-Vector(view['location'])).normalized()
        right = forward.cross(Vector((0, 0, 1))).normalized()
        up = right.cross(forward).normalized()
        points = [obj.matrix_world @ Vector(corner) for objects in self.model['parts'].values()
                  for obj in objects if obj.type in {'MESH', 'CURVE'} and not obj.hide_render
                  for corner in obj.bound_box]
        spans = [(min(point.dot(axis) for point in points), max(point.dot(axis) for point in points)) for axis in (right, up)]
        target = Vector(view['target'])
        shift = sum((axis*((lo+hi)/2-target.dot(axis)) for axis, (lo, hi) in zip((right, up), spans)), Vector())
        view['target'] = tuple(target+shift)
        view['location'] = tuple(Vector(view['location'])+shift)
        view['scale'] = max(hi-lo for lo, hi in spans)*1.055
        source = self.model['_projector_source']
        d = self.model['dimensions']
        centre_z = d.lens_z+(d.lens_y-d.screen_y)*d.optical_slope
        self.controls['screen_target'] = Vector((0, d.screen_y, centre_z))
        # A separate translucent rear-projection sheet sits at the optical
        # model's actual image distance. The camera visits its transmitted
        # image face; this is neither an opaque wall nor a fitted toy component.
        screen = S.box('separate rear-projection diffuser', (0, d.screen_y+.001, centre_z), (.23, .002, .17), 'ink')
        dark = bpy.data.materials.new('thin grey transmitting diffuser')
        dark.use_nodes = True
        nodes = dark.node_tree.nodes
        nodes.clear()
        output = nodes.new('ShaderNodeOutputMaterial')
        diffuse = nodes.new('ShaderNodeBsdfDiffuse')
        diffuse.inputs['Color'].default_value = (.022, .038, .055, 1)
        diffuse.inputs['Roughness'].default_value = 1
        transmitted = nodes.new('ShaderNodeBsdfTranslucent')
        transmitted.inputs['Color'].default_value = (.12, .16, .20, 1)
        mix = nodes.new('ShaderNodeMixShader')
        mix.inputs[0].default_value = .6
        dark.node_tree.links.new(diffuse.outputs[0], mix.inputs[1])
        dark.node_tree.links.new(transmitted.outputs[0], mix.inputs[2])
        dark.node_tree.links.new(mix.outputs[0], output.inputs[0])
        screen.data.materials.clear()
        screen.data.materials.append(dark)
        material = bpy.data.materials.new('projected warm white light')
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        output = nodes.new('ShaderNodeOutputMaterial')
        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = (1, .91, .64, 1)
        emission.inputs['Strength'].default_value = 5
        material.node_tree.links.new(emission.outputs[0], output.inputs[0])
        self.controls['projections'] = []
        for i in range(len(source.star_holes())):
            mesh = bpy.data.meshes.new('chief-ray image polygon')
            mesh.from_pydata([(0, 0, 0)]*10, [], [tuple(range(10))])
            mesh.update()
            obj = bpy.data.objects.new('light from punched hole '+str(i), mesh)
            bpy.context.collection.objects.link(obj)
            obj.data.materials.append(material)
            obj.hide_render = True
            obj['motion_role'] = 'light_projection'
            self.controls['projections'].append(obj)

    def pose_projector(self, p):
        angle = math.tau*p
        self.module.pose(self.model, angle)
        images = self.model['_projector_source'].projected_stars(angle)
        for obj in self.controls['projections']:
            obj.hide_render = True
        for star in images:
            obj = self.controls['projections'][star['hole_index']]
            obj.hide_render = False
            for vertex, co in zip(obj.data.vertices, star['polygon_m']):
                # Transmitted image on the camera-facing side of the diffuser.
                vertex.co = (co[0], co[1]-.0002, co[2])
            obj.data.update()

    def projector_camera(self, p):
        def smooth(x):
            x = min(1, max(0, x))
            return x*x*(3-2*x)
        progress = smooth((p-.12)/.23) if p <= .5 else smooth((.88-p)/.23)
        target = Vector(self.view['target']).lerp(self.controls['screen_target'], progress)
        offset = Vector(self.view['location'])-Vector(self.view['target'])
        # A modest pullback during travel reveals the distance; the endpoint
        # close-ups retain readable toy and star sizes in the same raster canvas.
        scale = self.view['scale'] + .60 * math.sin(math.pi*progress)**2
        return dict(location=tuple(target+offset), target=tuple(target), scale=scale)

    def prepare_carrier(self):
        from adapters import group
        m = self.model
        objects = m['parts']['pulley'] + [obj for obj in m['parts']['motor'] if obj.name.startswith('flat-sided motor output')]
        self.controls['driver'] = group('working projector drive shaft', objects, m['root'], (self.module.DRIVER[0], 0, self.module.DRIVER[1]))
        if 'pinwheel' in m:
            pw = m['pinwheel']
            objects = [obj for key in ('pw-paper', 'pw-hub') for obj in pw['parts'][key] if obj.type in {'MESH', 'CURVE'}]
            objects += [mod.object for obj in list(objects) for mod in obj.modifiers if mod.type == 'BOOLEAN' and mod.object]
            self.controls['cargo_pinwheel'] = group('working carried paper and hub', list(set(objects)), pw['rotor'])

    def pose_carrier(self, p):
        # 11 projector turns / 24 motor turns meet the 24:11 pitch-radius ratio
        # and return both keyed, asymmetric shafts to the same seam orientation.
        angle = math.tau * 11 * p
        self.model['root'].location.z = .018 * (1 - math.cos(math.tau * p))
        self.module.projector.pose(self.model['projector'], angle)
        ratio = (self.module.BIG_RADIUS+self.module.BELT_RADIUS)/(self.module.SMALL_RADIUS+self.module.BELT_RADIUS)
        self.controls['driver'].rotation_euler.y = -angle * ratio
        if 'cargo_pinwheel' in self.controls:
            self.controls['cargo_pinwheel'].rotation_euler.z = math.tau * 2 * p
