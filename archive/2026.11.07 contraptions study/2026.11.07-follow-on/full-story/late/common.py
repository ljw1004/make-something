"""Authoring helpers private to the rover, projector and carrier families."""
from pathlib import Path
import math
import sys

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'src/story/parser.ts').is_file())
BASE = ROOT/'archive/2026.11.07 builder study/art'
for path in (BASE, ROOT/'projects/builder-study'):
    if str(path) not in sys.path: sys.path.insert(0, str(path))


def geometry():
    import scene_parts as S
    import materials
    materials.apply(S)
    return S


def visible(model, parts):
    allowed = set(parts)
    for key, objects in model['parts'].items():
        for obj in objects:
            obj.hide_render = key not in allowed
            obj.hide_set(key not in allowed)


def bounds(model):
    import bpy
    from mathutils import Vector
    bpy.context.view_layer.update()
    points = [obj.matrix_world@Vector(p) for objects in model['parts'].values()
              for obj in objects if obj.type in {'MESH','CURVE','FONT'} and not obj.hide_render
              for p in obj.bound_box]
    if not points: raise ValueError('Empty construction stage')
    return [[min(p[i] for p in points), max(p[i] for p in points)] for i in range(3)]


def inspection(model, direction=(.6,-.8,.55), minimum=.04):
    lohi = bounds(model)
    target = tuple((p[0]+p[1])/2 for p in lohi)
    diagonal = math.sqrt(sum((p[1]-p[0])**2 for p in lohi))
    return dict(location=tuple(target[i]+direction[i] for i in range(3)),
                target=target, scale=max(minimum,diagonal*1.12))


class Author:
    def __init__(self):
        self.plan = {}; self.items = {}; self.recipes = []; self.pages = []

    def item(self, identity, name, parts, group, css=110, image=None, note='', **pose):
        if group.endswith('-loose'): group=image or identity
        self.plan[identity] = dict(parts=list(parts), group=group, css=css, **pose)
        if image: self.plan[identity]['image'] = image
        line=f'- `{identity}` {name}\n  - icon: ![{name}](assets/items/{image or identity}.webp)\n'
        if note: line+='\n  ---\n\n  '+note+'\n'
        self.items[identity]=line
        return identity

    def add(self, part, owner, result):
        self.recipes.append((result, f'- `{part}` [consume] + `{owner}` [transform] -> `{result}`\n'))

    def process(self, owner, process, result):
        self.recipes.append((result, f'- `{owner}` [transform] @ `{process}` -> `{result}`\n'))

    def page(self, identity, title, reference, supplies, derived, goals, processes=(), prose=''):
        self.pages.append(dict(identity=identity,title=title,reference=reference,supplies=supplies,
                               derived=derived,goals=goals,processes=processes,prose=prose))

    def markdown(self):
        pages=[]; declared=set(); emitted=set()
        for p in self.pages:
            reference_name=self.items[p["reference"]].splitlines()[0].split("` ",1)[1]
            text=f'## `{p["identity"]}` {p["title"]}\nbackground: ![White instruction page](assets/backgrounds/white.svg)\nreference: ![{reference_name}](assets/items/{p["reference"]}.webp)\n\n'
            if p['prose']: text+=p['prose']+'\n\n'
            text+='**Goals**\n'
            for i,(instruction, refs) in enumerate(p['goals']):
                text+='- '+('next: ' if i else '')+instruction
                if isinstance(refs,str): text+=' -- `'+refs+'`\n'
                else:
                    both=isinstance(refs,dict)
                    refs=refs['both'] if both else refs
                    text+='\n'+''.join('  - '+(('both: ' if j==0 else 'and: ') if both else ('either: ' if j==0 else 'or: '))+'`'+ref+'`\n' for j,ref in enumerate(refs))
            if p['processes']:
                text+='\n**Hotspots**\n'
                for i,(identity,label,art) in enumerate(p['processes']):
                    x=390 if len(p['processes'])==1 else 130+260*i
                    text+=f'- `{identity}` (center {x}px, 216px)\n  - icon: ![{label}](assets/actions/{art}.svg)\n  - hitbox: (center {x}px, 216px) (size 236px, 248px)\n'
            text+='\n**Items**\n'
            for identity in p['supplies']+p['derived']:
                if identity not in declared: text+=self.items[identity];declared.add(identity)
            for identity,label,art in p['processes']:
                if identity not in declared: text+=f'- `{identity}` {label}\n';declared.add(identity)
            text+='\n**Combinations**\n'
            for index,(result,recipe) in enumerate(self.recipes):
                if result in p['derived'] and index not in emitted:
                    text+=recipe;emitted.add(index)
            pages.append(text)
        if len(emitted)!=len(self.recipes): raise ValueError('Recipe not assigned to a chapter')
        return '\n\n'.join(pages)+'\n'
