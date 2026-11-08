"""Working poses over the canonical Builder assemblies; metres, radians.

Each adapter starts at the final still's actual pose. Animation groups preserve
world transforms when assigning existing rigid components to their real shafts.
"""
from pathlib import Path
import importlib
import math
import sys

import bpy
from mathutils import Matrix, Vector

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = next(p for p in HERE.parents if (p / 'src/story/parser.ts').is_file())
for folder in (STUDY / 'full-story', STUDY, ROOT / 'archive/2026.11.07 builder study/art'):
    sys.path.insert(0, str(folder))
import scene_parts as S
import materials
materials.apply(S)
from mechanisms import Mechanisms

FAMILIES = {
    'pinwheel': 'pinwheel', 'racer': 'wind-racer', 'pinball': 'pinball-table',
    'dragon': 'crank-dragon', 'gantry': 'gantry-hoist',
    'carousel': 'electric-carousel', 'claw': 'pneumatic-claw',
    'drum': 'animation-drum', 'rover': 'drawing-rover',
    'projector': 'star-projector', 'carrier': 'flying-whale',
    'window': 'open-window', 'spinner': 'ribbon-spinner',
}


def group(name, objects, parent, centre=(0, 0, 0)):
    """Add a rotation control without moving or rescaling its mesh children."""
    if parent in objects or any(obj in set(ancestors(parent)) for obj in objects):
        raise ValueError('A motion group cannot contain its own parent or ancestor: '+name)
    root = S.empty(name)
    root.parent = parent
    root.location = centre
    bpy.context.view_layer.update()
    members = set(objects)
    for obj in objects:
        if any(ancestor in members for ancestor in ancestors(obj)):
            continue
        matrix = obj.matrix_world.copy()
        obj.parent = root
        obj.matrix_world = matrix
    bpy.context.view_layer.update()
    return root


def ancestors(obj):
    while obj.parent:
        obj = obj.parent
        yield obj


class Adapter(Mechanisms):
    def __init__(self, family):
        self.family = family
        self.identity = FAMILIES[family]
        if family == 'pinwheel':
            sys.path.insert(0, str(STUDY / 'chapter-one-art'))
            self.module = importlib.import_module('pinwheel')
            self.model = self.module.make()
            self.view = self.module.view(self.model, self.module.set_state(self.model, self.identity))
        elif family == 'racer':
            sys.path.insert(0, str(STUDY / 'racer-art'))
            self.module = importlib.import_module('build')
            self.model = self.module.build()
            self.view = self.module.view(self.model, self.module.set_stage(self.model, self.identity))
        else:
            self.module = importlib.import_module(family)
            self.model = self.module.build()
            self.view = self.module.stage(self.model, self.identity)
        self.controls = {}
        getattr(self, 'prepare_' + family)()
        self.pose(0)

    def pose(self, phase):
        getattr(self, 'pose_' + self.family)(phase)
        bpy.context.view_layer.update()

    def camera_offset(self, phase):
        # A complete small excursion, with the original view at the seam.
        angle = math.radians(9) * math.sin(math.tau * phase) if self.family == 'pinwheel' else 0
        return Matrix.Rotation(angle, 3, 'Z')

    def camera_view(self, phase):
        if self.family == 'projector':
            return self.projector_camera(phase)
        view = dict(self.view)
        centre = Vector(view['target'])
        if self.family == 'rover':
            # Follow its small rolling circle without changing the view angle.
            # The separate ink trace stays in world space and makes the travel
            # visible; camera tracking avoids a large empty motion envelope.
            shift = self.model['vehicle'].location.copy()
            view['target'] = tuple(centre+shift)
            view['location'] = tuple(Vector(view['location'])+shift)
            return view
        view['location'] = tuple(centre + self.camera_offset(phase) @ (Vector(view['location'])-centre))
        return view

    def prepare_pinwheel(self):
        m = self.model
        objects = [obj for obj in m['parts']['pw-paper'] + m['parts']['pw-hub']
                   if obj.type in {'MESH', 'CURVE'}]
        # Boolean cutters belonging to those moving parts must follow them.
        objects += [mod.object for obj in list(objects) for mod in obj.modifiers
                    if mod.type == 'BOOLEAN' and mod.object]
        self.controls['rotor'] = group('working paper and hub about stationary axle',
                                       list(set(objects)), m['rotor'])
        # The diagonal paper tips sweep farther than the finished resting
        # silhouette. Recenter without changing the view direction and allow
        # that actual swept radius, rather than clipping a turning blade.
        shift = m['rotor'].matrix_world.to_3x3() @ Vector((0, .015, 0))
        self.view['location'] = tuple(Vector(self.view['location'])+shift)
        self.view['target'] = tuple(Vector(self.view['target'])+shift)
        self.view['scale'] = .345

    def pose_pinwheel(self, p):
        self.controls['rotor'].rotation_euler.z = math.tau * 2 * p
