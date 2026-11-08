"""Single-bearing stages cut from the unchanged canonical wind-racer model."""
from pathlib import Path
import sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'src/story/parser.ts').is_file())
BASE=ROOT/'archive/2026.11.07 builder study/art'
sys.path.insert(0,str(BASE))
import bpy
from mathutils import Vector
import presentation as C

STATES=('wr-chassis','wr-front-bearing-chassis','wr-rear-bearing-chassis','wr-bearing-chassis')


def make():return C.build('wr')


def set_stage(model,identity):
    if identity not in STATES:raise ValueError('Unknown bearing stage '+identity)
    materials=['wr-chassis']+([] if identity=='wr-chassis' else ['wr-bearings'])
    view=C.stage(model,{'id':'wr-bearing-chassis' if len(materials)>1 else 'wr-chassis','materials':materials},'wr')
    if identity in ('wr-front-bearing-chassis','wr-rear-bearing-chassis'):
        front=identity=='wr-front-bearing-chassis'
        for obj in model['parts']['wr-bearings']:
            # Every member of a complete tube/saddle unit is centred at one of
            # the two axle stations. +X is forward in the canonical rolling pose.
            xs=[(obj.matrix_world@Vector(corner)).x for corner in obj.bound_box]
            center=(min(xs)+max(xs))/2
            assert abs(center)>.05,obj.name
            obj.hide_render=(center>0)!=front
            obj.hide_set(obj.hide_render)
    bpy.context.view_layer.update()
    return view
