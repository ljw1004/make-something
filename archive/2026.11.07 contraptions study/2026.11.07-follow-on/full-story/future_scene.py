"""Native, texture-free use scenes for the three late crates.

The distant workbench is optically confined to the open frame. These are use-scene
props, never ingredients or hidden structural additions to a construction state.
"""
from pathlib import Path
import importlib.util
import math
import sys
import bpy
from mathutils import Vector
import core


def load_pinwheel():
    path=Path(__file__).parents[1]/'chapter-one-art/pinwheel.py'
    spec=importlib.util.spec_from_file_location('builder_scene_pinwheel',path)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    model=module.make();module.set_state(model,'pinwheel')
    return model


def parenting(obj,parent):
    matrix=obj.matrix_world.copy();obj.parent=parent;obj.matrix_world=matrix
    return obj


def moving_rotor(model):
    parent=model['rotor'];root=core.S.empty('paper and hub working rotation');root.parent=parent
    bpy.context.view_layer.update()
    objects=[o for key in ('pw-paper','pw-hub') for o in model['parts'][key]
             if o.type in {'MESH','CURVE'} and not o.hide_render]
    cutters={m.object for o in objects for m in o.modifiers if m.type=='BOOLEAN' and m.object}
    for obj in objects+list(cutters):parenting(obj,root)
    return root


def ellipsoid(name,center,dimensions,parent,color='paper'):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=center)
    obj=bpy.context.object;obj.name=name;obj.scale=tuple(d/2 for d in dimensions)
    obj.data.materials.append(core.S.material(color));obj.parent=parent
    for face in obj.data.polygons:face.use_smooth=True
    return obj


class Hand:
    """Two low fingers oppose a thumb around the unchanged wooden handle.

    The grip frame sits on the handle centreline. At grip=1 the finger pads
    touch its front face and the thumb touches its back face, 9 mm apart.
    Opening rotates the digits sideways, below the pinwheel's swept disc.
    """
    GRIP=(0,.024,.049)

    def __init__(self,parent,name='far maker'):
        S=core.S;self.root=S.empty(name+' hand');self.root.parent=parent
        # The raised heel and forearm clear the whale's top tile while the
        # fingertips keep the same low, three-point grip on either handle.
        ellipsoid(name+' palm',(.040,0,.004),(.058,.038,.046),self.root)
        ellipsoid(name+' wrist',(.078,.003,.015),(.070,.030,.037),self.root)
        # Preserve the wrist seam, then let the longer forearm recede behind
        # the jamb. Its cut end stays outside the opening even when the Window
        # gesture tips and turns the hand.
        vertices=[]
        for x,y in ((.0975,.006),(.220,.006),(.7975,.237)):
            vertices.extend((x,y+dy,.035+dz) for dy,dz in
                            ((-.025,-.0275),(.025,-.0275),(.025,.0275),(-.025,.0275)))
        faces=[(3,2,1,0),(8,9,10,11)]
        for start in (0,4):
            faces.extend((start+i,start+(i+1)%4,start+(i+1)%4+4,start+i+4) for i in range(4))
        mesh=bpy.data.meshes.new(name+' sleeve geometry');mesh.from_pydata(vertices,[],faces);mesh.update()
        self.sleeve=bpy.data.objects.new(name+' plain green sleeve',mesh);bpy.context.collection.objects.link(self.sleeve)
        self.sleeve.data.materials.append(S.material('teal'));self.sleeve.parent=self.root
        bevel=self.sleeve.modifiers.new('soft sleeve edges','BEVEL');bevel.width=.008;bevel.segments=3
        self.digits=[]
        for i,z in enumerate((-.009,.009)):
            joint=S.empty(name+' finger joint '+str(i));joint.parent=self.root;joint.location=(.040,-.013,z)
            ellipsoid(name+' finger base '+str(i),(-.012,0,0),(.039,.016,.016),joint)
            tip=S.empty(name+' finger tip joint '+str(i));tip.parent=joint;tip.location=(-.026,0,0)
            ellipsoid(name+' rounded finger '+str(i),(-.014,0,0),(.035,.017,.016),tip)
            self.digits.append((joint,tip,1))
        joint=S.empty(name+' thumb joint');joint.parent=self.root;joint.location=(.040,.013,0)
        ellipsoid(name+' thumb base',(-.012,0,0),(.039,.016,.020),joint)
        tip=S.empty(name+' thumb tip joint');tip.parent=joint;tip.location=(-.026,0,0)
        ellipsoid(name+' rounded thumb',(-.014,0,0),(.035,.017,.020),tip)
        self.digits.append((joint,tip,-1))
        self.pose(1)

    def pose(self,grip):
        opening=1-max(0,min(1,grip))
        for joint,tip,side in self.digits:
            joint.rotation_euler=(0,0,side*.35*opening)
            tip.rotation_euler=(0,0,side*.50*opening)


def smooth(t):
    t=max(0,min(1,t));return t*t*(3-2*t)


def portal_masks(parent):
    """Holdout behind the physical jambs clips only the far scene, not the frame."""
    material=bpy.data.materials.new('remote scene outside opening');material.use_nodes=True
    nodes=material.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');hold=nodes.new('ShaderNodeHoldout')
    material.node_tree.links.new(hold.outputs[0],out.inputs[0])
    from window import OPENING
    bottom,top=OPENING['bottom'],OPENING['top']
    # Mask plane is behind the real frame; the opening follows its actual model.
    rectangles=[((-1.325,.101,.405),(2,.002,3)),((1.325,.101,.405),(2,.002,3)),
                ((0,.101,bottom-1),(.650,.002,2)),((0,.101,top+1),(.650,.002,2))]
    objects=[]
    for j,(center,size) in enumerate(rectangles):
        obj=core.S.box('portal exterior mask '+str(j),center,size,'paper');obj.parent=parent
        obj.data.materials.clear();obj.data.materials.append(material);objects.append(obj)
    return objects


def far_bench(parent):
    S=core.S
    board=S.box('other workbench',(0,1.13,.025),(2.50,2.00,.025),'birch');board.parent=parent
    material=bpy.data.materials.new('pale blue distant room');material.use_nodes=True
    nodes=material.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');light=nodes.new('ShaderNodeEmission')
    light.inputs['Color'].default_value=(.79,.88,.91,1);light.inputs['Strength'].default_value=6.2
    material.node_tree.links.new(light.outputs[0],out.inputs[0])
    wall=S.box('other workshop pale wall',(0,.950,.410),(2.50,.004,2.50),'paper');wall.parent=parent
    wall.data.materials.clear();wall.data.materials.append(material)
    return board,wall


class WindowView:
    def __init__(self,model):
        self.model=model;self.root=core.S.empty('window use scene');self.root.parent=model['root']
        self.masks=portal_masks(self.root);far_bench(self.root)
        self.hold=core.S.empty('far maker holding a paper toy');self.hold.parent=self.root
        self.hand=Hand(self.hold)
        self.hand.root.location=Vector(Hand.GRIP)+Vector((0,0,-.060))
        self.pinwheel=load_pinwheel();self.pinwheel['root'].parent=self.hold
        # Both scenes use the same low grip on the original, unscaled handle.
        self.pinwheel['root'].location=(0,0,-.060)
        for obj,_,_ in self.pinwheel['paper']:
            obj.data.materials[0]=core.S.material('teal');obj.data.materials[1]=core.S.material('paper')
        self.rotor=moving_rotor(self.pinwheel)
        self.pose(0)

    def pose(self,phase):
        enter=min(smooth(phase/.20),smooth((1-phase)/.20))
        reach=math.sin(math.pi*max(0,min(1,(phase-.22)/.56)))**2
        self.hold.location=(-.090+.90*(1-enter),.250-.120*reach,.340+.012*math.sin(4*math.pi*phase)*enter)
        # Tip the pinwheel through the empty opening, then withdraw it. The
        # wrist stays on the far side; the blade crossing establishes the gap.
        self.hold.rotation_euler=(math.radians(48)*reach,0,.10*math.sin(6*math.pi*phase)*enter)
        self.rotor.rotation_euler.z=math.tau*2*phase
        self.hand.pose(1)
        bpy.context.view_layer.update()


def paper_star(parent):
    S=core.S;root=S.empty('paper star gift on a wooden tongue');root.parent=parent
    points=[]
    for i in range(10):
        angle=math.pi/2+i*math.pi/5;r=.075 if i%2==0 else .035
        points.append((r*math.cos(angle),.180+r*math.sin(angle)))
    star=S.profile('paper star',points,.0015,.019,'paper','paper');star.parent=root
    # Ordinary warm paper stays legible against the distant pale blue workshop.
    paper=S.material('paper').copy();paper.name='warm ochre gift paper'
    paper.diffuse_color=(.60,.38,.12,1)
    paper.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=paper.diffuse_color
    for i in range(len(star.data.materials)):star.data.materials[i]=paper
    stick=S.box('star wooden tongue',(0,.024,.080),(.015,.009,.184),'birch',bevel=.0005);stick.parent=root
    return root
