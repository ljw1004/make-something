import fs from 'node:fs';
import path from 'node:path';
import {parseStory} from '../../../../../src/story/parser.ts';

const root=path.resolve(import.meta.dirname,'..');
const original=fs.readFileSync(path.resolve(root,'../../anatomy.md'),'utf8');
const mapping={
 'prelude-phospholipids':'lipids','prelude-water':'water','opening-dna':'dna','opening-nuclear-envelope':'envelope','opening-nucleus':'nucleus','opening-cell':'cell','prelude-myoblasts':'muscle-cells','school-bone-mineral':'mineral','arm-front-tendons':'arm-front-base','arm-back-tendons':'arm-back-base',
 'Outer ears and canals':'outer-ear','Eardrums':'eardrum','Outer ears with eardrums':'outer-eardrum','Middle-ear bones':'ossicles','Sound-conducting ears':'sound-conducting','Coiled inner-ear chambers and fluid':'cochlea','Hearing cells with tiny hairs':'hair-cells','Vibration-sensitive inner ears':'sensing-cochlea','Sound-receiving ears':'sound-receiving','Hearing pathways':'hearing-nerve','Inner ears with hearing pathways':'cochlea-nerve','Ears':'ears',
 'Starchy food':'starch','Saliva':'saliva','Shorter starch chains':'short-starch','Digestive enzymes':'enzymes','Meal glucose':'glucose','Protein food':'protein-food','Meal amino acids':'amino-acids','Fat food':'fat','Bile':'bile','Small fat droplets':'small-droplets','Fat digestion products':'fat-products'
};
const backgrounds={'cell-boundary':'cell','full-strong-and-movable':'arm','full-hearing':'ear','full-nutrition-meal':'digestion'};
const lines=original.split('\n'),out=[],seen=new Set();
let section='',chapter='',owner='';
for (let line of lines) {
  const ch=line.match(/^## `([^`]+)`/); if(ch){chapter=ch[1];section='';}
  if(line.startsWith('**'))section=line;
  if(line.startsWith('# !['))line='# ![Vintage anatomical chart](assets/identity.png) Anatomy — 1950s wall chart';
  else if(line.startsWith('background:'))line=backgrounds[chapter]?`background: ![${backgrounds[chapter]} — 1950s wall chart](assets/${backgrounds[chapter]}-background.webp)`:line.replaceAll('(placeholder.svg)','(../../placeholder.svg)');
  if(section==='**Hotspots**' && chapter==='full-strong-and-movable' && /^- `arm-/.test(line)){
    const front=line.includes('front');
    out.push(line+' (center 390px, 844px)',`  - hitbox: (center ${front?285:555}px, 325px) (size 260px, 540px)`);continue;
  }
  if(section==='**Items**' && /^- /.test(line)){
    const body=line.slice(2),id=body.match(/^`([^`]+)`/);
    owner=id?id[1]:body.replace(/ \(compound\).*$/,'').trim();
    out.push(line);
    if(!seen.has(owner)){
      seen.add(owner);
      const filename=mapping[owner]??'unillustrated';
      let position='';
      const positions={'prelude-phospholipids':[170,1070],'prelude-water':[570,1070],'opening-dna':[170,1370],'opening-nuclear-envelope':[570,1370]};
      // Global primitive coordinates are checked in later placeholder scenes too;
      // let the shared arrival layout position movable pieces for this pilot.
      out.push(`  - icon: ![${owner}](assets/${filename}.png)${position}`);
    }
    continue;
  }
  if(/^  - (unnamed )?slot:/.test(line)){
    let filename='unillustrated';
    if(owner==='opening-cell')filename=line.includes('opening-nucleus')?'cell-nucleus':'cell-empty-overlay';
    if(owner.startsWith('arm-'))filename=`arm-${owner.includes('front')?'front':'back'}-${line.includes('school-bone-mineral')?'mineral':'muscle'}`;
    line+=`, icon: ![Fitted anatomy](assets/${filename}.png)`;
  }
  out.push(line);
}
let markdown=out.join('\n');
const parsed=parseStory(markdown,{id:'vintage',file:'anatomy.md'});
const missing=Object.values(parsed.items).filter(i=>!i.icon);
if(missing.length)throw Error('Missing standalone declarations: '+missing.map(i=>i.name).join(', '));
fs.writeFileSync(path.join(root,'anatomy.md'),markdown);
