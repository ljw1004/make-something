"""One quiet exchange after the last construction; no extra game recipes.

The whale crosses the actual opening with the original pinwheel in its actual
socket. Two hands exchange it for a paper star with a matching wooden tongue.
This one-shot scene holds its last frame; each completed toy has its own loop.
"""
import math
import sys
from pathlib import Path
from types import SimpleNamespace
import bpy
from mathutils import Vector
import core
import carrier
import window
from future_scene import Hand, far_bench, portal_masks, paper_star, smooth
sys.path.insert(0,str(Path(__file__).parents[1]/"animation"))
from mechanisms import Mechanisms


def mix(a,b,t):
    return Vector(a).lerp(Vector(b),smooth(t))


def bob(phase):
    return .003*math.sin(math.tau*3*phase)


class Ending:
    def __init__(self):
        self.window=window.build();window.stage(self.window,'open-window')
        self.masks=portal_masks(self.window['root']);far_bench(self.window['root'])
        self.whale=carrier.build();carrier.stage(self.whale,'flying-whale')
        self.drive=SimpleNamespace(model=self.whale,module=carrier,controls={})
        Mechanisms.prepare_carrier(self.drive)
        self.pinwheel=self.whale['pinwheel'];self.pinwheel['root'].parent=None
        self.rotor=self.drive.controls['cargo_pinwheel']
        self.star=paper_star(None)
        # The taking arm exits left and the giving arm exits right, keeping the
        # two hands and their gifts distinct throughout the exchange.
        self.right=Hand(self.window['root'],'maker taking');self.right.root.scale.x=-1
        self.left=Hand(self.window['root'],'maker giving')
        # A pale work surface is scene context, never an added machine component.
        self.table=core.S.box('near white work surface',(0,-.70,-.025),(1.60,1.40,.050),'paper')
        material=bpy.data.materials.new('white instruction tabletop');material.use_nodes=True
        material.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.93,.93,.91,1)
        self.table.data.materials.clear();self.table.data.materials.append(material)
        # Match the white instruction page's portrait framing. Keep the exchange
        # in its upper working area so short phones retain the complete handoff.
        self.view=dict(location=(-.35,-2.40,.50),target=(0,-.12,.16),scale=2.05)
        self.pose(0)

    def pose(self,p):
        start=Vector((-.080,-.590,.240));far=Vector((0,.340,.205))
        cruise=Vector((far.x,far.y,start.z))
        # The lower exchange height cannot clear the Window's battery, block
        # and captive screws. Cross at cruise height; lower only after the
        # complete whale is beyond the frame, and rise there before returning.
        if p<.12:position=start.copy()
        elif p<.24:position=mix(start,cruise,(p-.12)/.12)
        elif p<.28:position=mix(cruise,far,(p-.24)/.04)
        elif p<.78:position=far.copy()
        elif p<.82:position=mix(far,cruise,(p-.78)/.04)
        elif p<.94:position=mix(cruise,start,(p-.82)/.12)
        else:position=start.copy()
        # Hold still while fingers and wooden tongues engage the blind socket.
        # Ease the flight bob to zero on arrival and restore it on departure.
        flight=1-smooth((p-.24)/.04) if p<.28 else smooth((p-.78)/.04)
        position.z+=bob(p)*flight
        Mechanisms.pose_carrier(self.drive,p)
        self.whale['root'].location=position
        self.whale['root'].rotation_euler=(0,0,0)
        mount=position+Vector(carrier.PINWHEEL_MOUNT)
        # The old pinwheel rises out of the blind socket before travelling sideways.
        above=far+Vector(carrier.PINWHEEL_MOUNT)+Vector((0,0,.040))
        clear=above+Vector((-.090,.090,0))
        held=Vector((-.075,.620,.310))
        if p<.32:pin=mount
        elif p<.39:pin=mount+Vector((0,0,.040*smooth((p-.32)/.07)))
        elif p<.415:pin=mix(above,clear,(p-.39)/.025)
        elif p<.47:pin=mix(clear,held,(p-.415)/.055)
        else:pin=held
        self.pinwheel['root'].location=pin
        self.pinwheel['root'].rotation_euler=(0,0,0)
        # A short turn settles before the star is lowered into the empty socket.
        self.rotor.rotation_euler.z=math.tau*.75*smooth((p-.39)/.26)
        # Wait for the pinwheel to reach its separate holding place. Introduce
        # the star slowly from the opposite edge, entirely below the top rail.
        star_start=Vector((.480,above.y,above.z))
        if p<.47:star=star_start
        elif p<.62:star=mix(star_start,above,(p-.47)/.15)
        elif p<.65:star=above
        elif p<.71:star=mix(above,mount,(p-.65)/.06)
        else:star=mount
        self.star.location=star;self.star.rotation_euler=(0,0,0)
        # The shared grip leaves the socket exposed and stays below the rotor.
        grip=Vector(Hand.GRIP)
        if p<.26:r=mix((-.650,.430,.510),mount+grip,(p-.19)/.07)
        else:r=pin+grip
        self.right.root.location=r;self.right.pose(smooth((p-.26)/.04))
        if p<.71:
            self.left.root.location=star+grip;self.left.pose(1)
        else:
            # Open completely before withdrawing sideways. Every articulated
            # joint has the same transform at the release boundary.
            retreat=smooth((p-.75)/.04)
            self.left.root.location=far+Vector(carrier.PINWHEEL_MOUNT)+grip+Vector((.75*retreat,0,0))
            self.left.pose(1-smooth((p-.71)/.04))
        bpy.context.view_layer.update()
        return self.view

    def passage_bounds(self):
        """Conservative mesh bounds while the complete loaded whale crosses."""
        self.pose(.32);points=[]
        for objects in self.whale['parts'].values():
            for obj in objects:
                if obj.type in {'MESH','CURVE'} and not obj.hide_render:
                    points.extend(obj.matrix_world@Vector(c) for c in obj.bound_box)
        return dict(minimum=[min(v[i] for v in points) for i in range(3)],
                    maximum=[max(v[i] for v in points) for i in range(3)],
                    aperture=window.OPENING,
                    limit='Nominal rigid geometry; no aerodynamic or material-force simulation.')
