"""Shared geometry/presentation utilities for the revised construction families."""
from pathlib import Path
import math
import sys
import bpy
from mathutils import Vector

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'src/story/parser.ts').is_file())
BASE=ROOT/'archive/2026.11.07 builder study/art'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import scene_parts as S
from construction import Assembly, special_material, surface, bolt, ring_z
import materials
materials.apply(S)


def select(model, plan, identity):
    info=plan[identity];allowed=set(info['parts'])
    missing=allowed-set(model['parts'])
    if missing:raise ValueError(f'{identity}: unknown geometry parts {sorted(missing)}')
    for key,objects in model['parts'].items():
        for obj in objects:
            obj.hide_render=key not in allowed;obj.hide_set(obj.hide_render)
    bpy.context.view_layer.update()
    return info


def frame(target, scale, direction=(.6,-.8,.55), roll=0):
    centre=Vector(target)
    return dict(location=tuple(centre+Vector(direction)),target=tuple(centre),scale=scale,roll=roll)


def world_bounds(objects):
    points=[obj.matrix_world@Vector(p) for obj in objects if obj.type in {'MESH','CURVE'} for p in obj.bound_box]
    if not points:raise ValueError('Cannot frame an empty part')
    return [min(p[i] for p in points) for i in range(3)],[max(p[i] for p in points) for i in range(3)]


def inspect_view(model, parts=None, direction=(.6,-.8,.55), roll=-.35, padding=1.55):
    objects=[obj for key,group in model['parts'].items() if parts is None or key in parts for obj in group if not obj.hide_render]
    lo,hi=world_bounds(objects);centre=[(a+b)/2 for a,b in zip(lo,hi)]
    return frame(centre,max(hi[i]-lo[i] for i in range(3))*padding,direction,roll)


def reset_root(model):
    model['root'].location=(0,0,0);model['root'].rotation_euler=(0,0,0);model['root'].scale=(1,1,1)


def assign(model, old_key, new_key, objects):
    """Move actual component ownership, never crop a representative from a pile."""
    chosen=set(objects)
    model['parts'][old_key]=[obj for obj in model['parts'][old_key] if obj not in chosen]
    model['parts'][new_key]=list(objects)
    for obj in objects:obj['part_id']=new_key
