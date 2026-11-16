"""Final-chapter presentations: one exact whole-canvas transform for all chest layers.
Run after produce.py. Never rewrites normal chapter 14 outputs.
"""
from pathlib import Path
import json
from PIL import Image
P=Path(__file__).resolve().parent; A=P/'assets'
SIZE=(298,220)
def resize(name):
 im=Image.open(A/(name+'.png')).convert('RGBA')
 assert im.size==(1000,1100),(name,im.size)
 return im.resize(SIZE,Image.Resampling.LANCZOS)
def save(im,name):
 im.save(A/(name+'.png'));return 'rework/senses-circulation/assets/'+name+'.png'
base=resize('breathing-apparatus');basepath=save(base,'final-chest-base')
keys={'name:Heart and lungs':'heart-and-lungs','name:Diaphragm':'diaphragm','name:Arm assembly':'arm','name:Lymph drainage network':'lymph'}
paths={};images={}
for identity,suffix in keys.items():
 images[identity]=resize('breathing-slot-'+suffix)
 paths[identity]=save(images[identity],'final-chest-slot-'+suffix)
# Finale uses its bodymaster arm, so provide the chest without a second arm.
complete=base.copy()
for identity in ['name:Heart and lungs','name:Diaphragm','name:Lymph drainage network']:
 complete.alpha_composite(images[identity])
save(complete,'final-chest-complete')
complete.alpha_composite(images['name:Arm assembly']);save(complete,'final-chest-fully-equipped')
items={'name:Breathing apparatus':basepath}
for identity,suffix in [('name:Arm assembly','arm'),('name:Lymph drainage network','lymph')]:
 im=images[identity];im=im.crop(im.getchannel('A').getbbox())
 items[identity]=save(im,'final-loose-'+suffix)
(P/'finale-presentations.json').write_text(json.dumps({'chapter':28,'itemIcons':items,'slotIcons':{'name:Breathing apparatus':paths},'registration':{'sourceCanvas':[1000,1100],'canvas':list(SIZE),'transform':{'scaleX':.298,'scaleY':.2,'crop':None},'bodyCanvas':[500,1000],'bodyTopLeft':[102,127],'completeReference':'rework/senses-circulation/assets/final-chest-complete.png','fullyEquippedReference':'rework/senses-circulation/assets/final-chest-fully-equipped.png'}},indent=2)+'\n')
print('Final canvas',SIZE,'all four overlays match; loose assets use exact fitted pixels')
