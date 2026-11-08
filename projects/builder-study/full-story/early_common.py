"""Shared ownership, framing and fragment authoring for the five early builds.

Blender is loaded only by geometry functions; PLAN and manuscripts remain usable
from ordinary Python. Archived factories are geometry sources, never story rules.
"""
from pathlib import Path
import sys
import math

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'src/story/parser.ts').is_file())
ART = ROOT / 'archive/2026.11.07 builder study/art'
for directory in (ART, HERE.parent):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))


def libraries():
    import scene_parts as S
    import materials
    materials.apply(S)
    return S


def descendants(obj, ancestor):
    while obj:
        if obj == ancestor:
            return True
        obj = obj.parent
    return False


def owned(model, parts):
    """Retain every source drawable so staging can also hide retired fixtures."""
    import bpy
    all_objects = set(o for values in model['parts'].values() for o in values)
    all_objects.update(o for values in parts.values() for o in values)
    # Pose empties remain in the hierarchy and model handles, but are not
    # drawable ownership. Their visibility must not make a hidden part active.
    parts={key:[o for o in values if o.type in {'MESH','CURVE','FONT'}] for key,values in parts.items()}
    model['_source_drawables'] = [o for o in all_objects if o.type in {'MESH', 'CURVE', 'FONT'}]
    # The renderer audits unowned geometry before its first stage() call.
    # Retired canonical fixtures must already be hidden at that boundary.
    for obj in model['_source_drawables']:
        obj.hide_render=True;obj.hide_set(True)
    model['parts'] = parts
    for key, objects in parts.items():
        if not objects:
            raise ValueError('Empty physical part: ' + key)
        for obj in objects:
            obj['builder_part'] = key
    bpy.context.view_layer.update()
    return model


def show(model, keys):
    chosen = set(o for key in keys for o in model['parts'][key])
    for obj in model['_source_drawables']:
        obj.hide_render = obj not in chosen
        obj.hide_set(obj not in chosen)


def inspection(model, keys, direction=(.7, -1., .65), margin=1.23):
    """Fit a loose connected supply without changing any physical dimension."""
    import bpy
    from mathutils import Vector
    bpy.context.view_layer.update()
    points = [o.matrix_world @ Vector(c) for key in keys for o in model['parts'][key]
              if o.type in {'MESH', 'CURVE', 'FONT'} for c in o.bound_box]
    low = Vector(tuple(min(p[i] for p in points) for i in range(3)))
    high = Vector(tuple(max(p[i] for p in points) for i in range(3)))
    centre = (low + high) / 2
    view = Vector(direction).normalized()
    right = view.cross(Vector((0, 0, 1))).normalized()
    up = right.cross(view).normalized()
    span = max(max(p.dot(axis) for p in points) - min(p.dot(axis) for p in points) for axis in (right, up))
    return {'location': tuple(centre + view), 'target': tuple(centre), 'scale': max(.025, span * margin)}


def entry(parts, group, css=230, **kwargs):
    return dict(parts=list(parts), group=group, css=css, **kwargs)


def write_fragment(module):
    """Render the authored route data; no artwork or runtime modifications."""
    lines = []
    for chapter in module.CHAPTERS:
        lines += [f"## `{chapter['id']}` {chapter['title']}",
                  'background: ![White instruction page](assets/backgrounds/white.svg)',
                  f"reference: ![{module.NAMES[chapter['reference']]}](assets/items/{chapter['reference']}.webp)", '', '**Goals**']
        goals=chapter.get('goals', [([result],goal) for a,b,result,goal in chapter['steps']])
        for i, (results, goal) in enumerate(goals):
            lead=f"- {'next: ' if i else ''}{goal}"
            if len(results)==1:lines.append(lead+f' -- `{results[0]}`')
            else:
                lines.append(lead)
                for j,result in enumerate(results):lines.append(f"  - {'either' if j==0 else 'or'}: `{result}`")
        processes = chapter.get('processes', {})
        if processes:
            lines += ['', '**Hotspots**']
            for i, (identity, action) in enumerate(processes.items()):
                lines += [f'- `{identity}` (center {130 + i * 260}px, 216px)',
                          f'  - icon: ![{action.title()}](assets/actions/{action}.svg)',
                          f'  - hitbox: (center {130 + i * 260}px, 216px) (size 236px, 248px)']
        recipes=chapter['steps']+chapter.get('extra_steps',[])
        identities = list(dict.fromkeys(x for step in recipes for x in step[:3]))
        lines += ['', '**Items**']
        for identity in identities:
            if identity in processes:
                action = processes[identity]
                lines += [f'- `{identity}` {action.title()}', f'  - icon: ![{action.title()}](assets/actions/{action}.svg)']
                continue
            name = module.NAMES[identity]
            lines += [f'- `{identity}` {name}', f'  - icon: ![{name}](assets/items/{identity}.webp)']
            description = getattr(module, 'DESCRIPTIONS', {}).get(identity)
            if description:
                lines += ['', '  ---', '', '  ' + description]
        lines += ['', '**Combinations**']
        for a, b, result, _ in recipes:
            if b in processes:
                lines.append(f'- `{a}` [transform] @ `{b}` -> `{result}`')
            else:
                lines.append(f'- `{a}` [transform] + `{b}` [consume] -> `{result}`')
        lines += ['', '']
    (HERE / (module.__name__.split('.')[-1] + '.md')).write_text('\n'.join(lines))
