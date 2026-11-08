"""Generate the independent sail and racer draft from explicit construction states."""
from pathlib import Path
import json

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'src/story/parser.ts').is_file())
HERE = Path(__file__).parent
plan = {}


def item(identity, name, parts, view, image=None, explanation=''):
    plan[identity] = dict(name=name, parts=parts, view=view, image=image or identity)
    text = f'- `{identity}` {name}\n  - icon: ![{name}](assets/items/{image or identity}.webp)\n'
    if identity == 'wr-sail':
        text += '  - from chapter `c-racer-body` icon: ![Sail](assets/items/wr-sail-carried.webp)\n'
    if explanation:
        text += '\n  ---\n\n  '+explanation+'\n'
    return text


def goal(text, identities, next=False, both=False):
    prefix = '- '+('next: ' if next else '')+text
    if len(identities) == 1:
        return prefix+' -- `'+identities[0]+'`\n'
    return prefix+'\n'+''.join('  - '+(('both: ' if i == 0 else 'and: ') if both else ('either: ' if i == 0 else 'or: '))+'`'+identity+'`\n' for i, identity in enumerate(identities))


def recipe(a, b, result, process=False):
    if process: return f'- `{a}` [transform] @ `{b}` -> `{result}`\n'
    return f'- `{b}` [consume] + `{a}` [transform] -> `{result}`\n'


mast_ids = {
    (0,0): 'wr-mast-wood', (0,1): 'wr-mast-foot',
    (1,0): 'wr-mast-joint', (1,1): 'wr-mast-joint-foot',
    (2,0): 'wr-frame', (2,1): 'wr-ready',
    (3,0): 'wr-frame-sail', (3,1): 'wr-sail',
}
mast_items = []
for (level, foot), identity in mast_ids.items():
    parts = ['mast']+(['connector'] if level >= 1 else [])+(['crossbar'] if level >= 2 else [])+(['cloth'] if level >= 3 else [])+(['foot'] if foot else [])
    mast_items.append(item(identity, 'Sail' if level == 3 else 'Mast', parts, 'mast'))
for identity, name, part, description in [
    ('wr-connector','Connector','connector','Two offset sockets keep the wooden rods from crossing through each other. Flexible ribs grip both rods.'),
    ('wr-crossbar','Crossbar','crossbar','A short wooden rod that supports the bottom of the sail.'),
    ('wr-foot','Foot','foot','The mast pushes into the top socket. The split legs underneath will snap into the chassis.'),
    ('wr-sailcloth','Sail','cloth','Three small open clips are attached to the cloth. They press onto the mast and crossbar.'),
]:
    mast_items.append(item(identity, name, [part], 'loose', explanation=description))
mast_items.append(item('wr-crossbar-joint','Crossbar',['crossbar','connector'],'loose'))
mast_recipes = []
for level in range(4):
    mast_recipes.append(recipe(mast_ids[level,0], 'wr-foot', mast_ids[level,1]))
for level, supply in [(0,'wr-connector'),(1,'wr-crossbar'),(2,'wr-sailcloth')]:
    for foot in (0,1):
        mast_recipes.append(recipe(mast_ids[level,foot], supply, mast_ids[level+1,foot]))
mast_recipes += [recipe('wr-crossbar','wr-connector','wr-crossbar-joint'),
                 recipe('wr-mast-wood','wr-crossbar-joint','wr-frame'),
                 recipe('wr-mast-foot','wr-crossbar-joint','wr-ready')]
mast = '## `c02` A sail\nbackground: ![White instruction page](assets/backgrounds/white.svg)\nreference: ![Completed sail](assets/items/wr-sail.webp)\n\n**Goals**\n'
mast += goal('Fit the connector to the mast',[id for (level,foot),id in mast_ids.items() if level>=1])
mast += goal('Fit the crossbar into the connector',[id for (level,foot),id in mast_ids.items() if level>=2],True)
mast += goal('Push the foot onto the mast',[id for (level,foot),id in mast_ids.items() if foot],True)
mast += goal('Clip the sail onto the mast',['wr-sail'],True)
mast += '\n**Items**\n'+''.join(mast_items)+'\n**Combinations**\n'+''.join(mast_recipes)

body_ids = {(0,0):'wr-chassis',(1,0):'wr-front-bearing-chassis',(0,1):'wr-rear-bearing-chassis',
            (1,1):'wr-bearing-chassis',(2,0):'wr-front-rolling-chassis',(0,2):'wr-rear-rolling-chassis',
            (2,1):'wr-front-wheel-chassis',(1,2):'wr-rear-wheel-chassis',(2,2):'wr-rolling-chassis'}
body_items = []
for (front,rear),identity in body_ids.items():
    parts = ['chassis']
    for side,level in [('front',front),('rear',rear)]:
        if level: parts += [side+'-bearing']
        if level==2: parts += [side+'-axle',side+'-wheel-near',side+'-wheel-far']
    body_items.append(item(identity,'Chassis',parts,'underside'))
full_body = plan['wr-rolling-chassis']['parts']
body_items.append(item('wr-upright','Chassis',full_body,'upright'))
body_items.append(item('wind-racer','Wind racer',full_body+['mast','connector','crossbar','foot','cloth'],'complete',explanation='The wheels turn together with each straw axle inside the bearings. Outdoors, moving air can push against the sail.'))
body_items.append('- `wr-flip` Flip\n')
for side in ('front','rear'):
    body_items.append(item('wr-'+side+'-bearing','Bearing',[side+'-bearing'],'loose','wr-bearing', 'An open bearing clips beneath the chassis. Its spring lips let the axle snap into the channel.'))
    body_items.append(item('wr-'+side+'-axle',side.title()+' straw',[side+'-axle'],'loose','wr-straw','A stiff hollow plastic axle. Push one wheel onto each end.'))
    body_items.append(item('wr-'+side+'-one-wheel',side.title()+' axle',[side+'-axle',side+'-wheel-near'],'axle','wr-one-wheel'))
    body_items.append(item('wr-'+side+'-wheels',side.title()+' wheels',[side+'-axle',side+'-wheel-near',side+'-wheel-far'],'axle','wr-wheels'))
for n in range(1,5):
    body_items.append(item(f'wr-wheel-{n}','Wheel',['front-wheel-near'],'loose','wr-wheel','The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.'))
body_recipes = []
for side in ('front','rear'):
    for n in range(1,5):
        body_recipes += [recipe('wr-'+side+'-axle',f'wr-wheel-{n}','wr-'+side+'-one-wheel'),
                        recipe('wr-'+side+'-one-wheel',f'wr-wheel-{n}','wr-'+side+'-wheels')]
for front in range(3):
    for rear in range(3):
        for side,value,other in [('front',front,rear),('rear',rear,front)]:
            if value==2: continue
            dest=(front+1,rear) if side=='front' else (front,rear+1)
            body_recipes.append(recipe(body_ids[front,rear],'wr-'+side+('-bearing' if value==0 else '-wheels'),body_ids[dest]))
body_recipes += [recipe('wr-rolling-chassis','wr-flip','wr-upright',True),recipe('wr-upright','wr-sail','wind-racer')]
body = '## `c-racer-body` Wheels for the sail\nbackground: ![White instruction page](assets/backgrounds/white.svg)\nreference: ![Wind racer](assets/items/wind-racer.webp)\n\n**Goals**\n'
body += goal('Push a wheel onto the front straw',['wr-front-one-wheel'])
body += goal('Push another wheel onto the front axle',['wr-front-wheels'],True)
body += goal('Push a wheel onto the rear straw',['wr-rear-one-wheel'],True)
body += goal('Push another wheel onto the rear axle',['wr-rear-wheels'],True)
body += goal('Fit a bearing to the chassis',[identity for key,identity in body_ids.items() if key!=(0,0)],True)
body += goal('Fit the other bearing',[identity for (f,r),identity in body_ids.items() if f and r],True)
body += goal('Snap wheels into a bearing',[identity for key,identity in body_ids.items() if 2 in key],True)
body += goal('Snap on the other wheels',['wr-rolling-chassis'],True)
body += goal('Flip the chassis upright',['wr-upright'],True)
body += goal('Fit the sail to the chassis',['wind-racer'],True)
body += '\n**Hotspots**\n- `wr-flip` (center 390px, 216px)\n  - icon: ![Turn the chassis over](assets/actions/flip.svg)\n\n**Items**\n'+''.join(body_items)+'\n**Combinations**\n'+''.join(body_recipes)
source=(ROOT/'stories/builder/builder.md').read_text()
start=source.index('## `c02`');end=source.index('## `c03`',start)
source=source[:start]+mast+'\n\n'+body+'\n\n'+source[end:]
source=source.replace('  - from chapter `c02` icon: ![Pinwheel](assets/items/pinwheel-carried.webp)\n','')
source=source.replace('An orange paper pinwheel','A brick-red paper pinwheel').replace('The orange sheet','The paper sheet').replace('background: ![An invitation on the garden workbench](assets/cover.webp)','background: ![White instruction page](assets/backgrounds/white.svg)')
draft=source.replace('(assets/','(../../stories/builder/assets/').replace('(icon.png)','(../../stories/builder/icon.png)')
(ROOT/'projects/builder-study/builder-v36.md').write_text(draft)
(HERE/'construction-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
print(f'{len(mast_recipes)} sail recipes, {len(body_recipes)} body recipes; {len(plan)} illustrated identities')
