/** Presentation-only full-book exporter; run from repository root with Node22+. */
import {readFileSync,writeFileSync,existsSync} from 'node:fs';
import {resolve} from 'node:path';
import {parseStory} from '../../../src/story/parser.ts';
const root=resolve(import.meta.dirname,'..');
let source=readFileSync(resolve(root,'anatomy.md'),'utf8');
// Re-running updates presentation only: remove this exporter's prior metadata
// and restore names before parsing package maps keyed to the source identities.
const aliasFile=resolve(root,'atlas/identity-aliases.json');
const priorAliases:Record<string,string>=existsSync(aliasFile)?JSON.parse(readFileSync(aliasFile,'utf8')):{};
if(existsSync(aliasFile))for(const [newId,oldId] of Object.entries(priorAliases)){
 const token='`'+newId.slice(3)+'`',name=oldId.slice(5);
 source=source.replaceAll(token+' '+name,token).replaceAll(token,name);
}
source=source.split('\n').filter(l=>!/^  - (icon:|from chapter .* icon:|hitbox:)/.test(l)).map(l=>l.replace(/, icon: !\[[^\]]*\]\([^)]+\)/g,'').replace(/ \(center [^)]+\)$/,'')).join('\n');
const story=parseStory(source);
const packages=['opening','circulation','arm-food','body',...['opening','senses','circulation','nervous','blood','immune','body','finale'].map(x=>'composition-review/'+x).filter(x=>existsSync(resolve(root,'atlas',x,'map.json')))];
const art:any={itemIcons:{},slotIcons:{},hotspots:{},placements:{}};
const appearances:Record<string,Array<{chapter:string,path:string}>>={};
for(const pkg of packages){
 const canonicalKeys=(value:any):any=>Array.isArray(value)?value.map(canonicalKeys):value&&typeof value==='object'?Object.fromEntries(Object.entries(value).map(([k,v])=>[priorAliases[k]??k,canonicalKeys(v)])):value;
 const m=canonicalKeys(JSON.parse(readFileSync(resolve(root,'atlas',pkg,'map.json'),'utf8')));
 Object.assign(art.itemIcons,m.itemIcons??{});Object.assign(art.placements,m.placements??{});
 for(const k of ['slotIcons','hotspots'])for(const [id,v] of Object.entries(m[k]??{}))art[k][id]={...(art[k][id]??{}),...(v as any)};
 for(const [id,v] of Object.entries(m.presentations??{}))for(const a of v as any[]){
  appearances[id]=[...(appearances[id]??[]).filter(old=>old.chapter!==a.chapter),a];
 }
}
const aliases:Record<string,string>={};
for(const id of Object.keys(appearances))if(id.startsWith('name:'))aliases[id]='id:art-'+id.slice(5).toLowerCase().replace(/[^a-z0-9]+/g,'-');
const missing=Object.keys(story.items).filter(id=>!art.itemIcons[id]);
const missingSlots=Object.entries(story.items).flatMap(([id,i])=>i.slots.filter(s=>!art.slotIcons[id]?.[s.accepts]).map(s=>[id,s.accepts]));
if(missing.length||missingSlots.length)throw new Error(JSON.stringify({missing,missingSlots}));
for(const path of [...Object.values(art.itemIcons),...Object.values(art.slotIcons).flatMap((v:any)=>Object.values(v)),...Object.values(appearances).flatMap(v=>v.map(x=>x.path))] as string[])if(!existsSync(resolve(root,path)))throw new Error('Missing '+path);
const lines=source.split('\n'),declarations=new Map<string,number>();let section='',chapter=0;
const after=new Map<number,string[]>(),replace=new Map<number,string>();
const identify=(s:string)=>{const match=s.match(/^`([^`]+)`/);return match?'id:'+match[1]:'name:'+s.replace(/ \(compound\)$/,'');};
const image=(path:string)=>`![Anatomical illustration](${path})`;
const append=(n:number,s:string)=>after.set(n,[...(after.get(n)??[]),s]);
for(let n=0;n<lines.length;n++){
 const line=lines[n];if(line.startsWith('## ')){chapter++;section='';}if(line.startsWith('**'))section=line;
 if(section==='**Items**'&&line.startsWith('- ')){const id=identify(line.slice(2));if(story.items[id]&&!declarations.has(id))declarations.set(id,n);}
 if(line.startsWith('# '))replace.set(n,line.replace(/!\[[^\]]*\]\([^)]+\)/,image('atlas/opening/assets/heading.png')));
 if(line.startsWith('background:'))replace.set(n,`background: ![Blank atlas paper](atlas/${chapter===28?'blank-paper-tall.svg':'blank-paper.png'})`);
 if(section==='**Hotspots**'&&line.startsWith('- ')){
  const id=identify(line.slice(2)),h=art.hotspots[String(chapter)]?.[id];
  if(!h)throw new Error(`Missing hotspot ${chapter} ${id}`);
  replace.set(n,`${line} (center ${h.center[0]}px, ${h.center[1]}px)`);
  if(h.icon)append(n,`  - icon: ${image(h.icon)}`);
  if(h.hitbox)append(n,`  - hitbox: (center ${h.hitbox.center[0]}px, ${h.hitbox.center[1]}px) (size ${h.hitbox.size[0]}px, ${h.hitbox.size[1]}px)`);
 }
}
for(const [id,item] of Object.entries(story.items)){
 const n=declarations.get(id);if(n===undefined)throw new Error('No declaration '+id);
 append(n,`  - icon: ${image(art.itemIcons[id])}${art.placements[id]?` (center ${art.placements[id][0]}px, ${art.placements[id][1]}px)`:''}`);
 for(const a of appearances[id]??[])append(n,`  - from chapter \`${a.chapter}\` icon: ${image(a.path)}`);
 for(const slot of item.slots){const i=slot.source.line-1;replace.set(i,`${lines[i]}, icon: ${image(art.slotIcons[id][slot.accepts])}`);}
}
let out=lines.flatMap((l,n)=>[replace.get(n)??l,...(after.get(n)??[])]);
// Existing syntax requires an explicit identifier for chapter-dependent art.
// Give only these named objects stable IDs in this illustrated copy. Rewrite
// grammatical references, never player prose, and verify via canonical aliases.
const names=Object.keys(aliases).sort((a,b)=>b.length-a.length);
const escaped=(s:string)=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
function refs(s:string){for(const id of names){const name=id.slice(5);s=s.replace(new RegExp(`(^|[\\s+,\\[@>])${escaped(name)}(?=$|[\\s+,\\]@\\[])`,'g'),(_m,p)=>p+'`'+aliases[id].slice(3)+'`');}return s;}
section='';const defined=new Set<string>();
out=out.map(line=>{
 if(line.startsWith('## '))section='';if(line.startsWith('**'))section=line;
 if(section==='**Items**'){
  if(line.startsWith('- '))for(const id of names){const name=id.slice(5),body=line.slice(2);if(body===name||body.startsWith(name+' (compound)')||body.startsWith(name+'[')){
   const suffix=body.slice(name.length),ident='`'+aliases[id].slice(3)+'`';
   const text='- '+ident+(defined.has(id)?'':' '+name)+refs(suffix);defined.add(id);return text;
  }}
  if(/^\s+- (unnamed slot:|slot:)/.test(line)){const at=line.indexOf('accepts ');return line.slice(0,at+8)+refs(line.slice(at+8));}
  if(/^\s+\[/.test(line)){const at=line.indexOf(']');return refs(line.slice(0,at+1))+line.slice(at+1);}
 }
 if(section==='**Combinations**'&&line.startsWith('- '))return refs(line);
 if(section==='**Hotspots**'&&line.startsWith('- '))return refs(line);
 if(section==='**Goals**'){
  const sep=line.indexOf(' -- ');if(sep>=0)return line.slice(0,sep+4)+refs(line.slice(sep+4));
  if(/^\s+- (both|and|or|either):/.test(line))return refs(line);
 }
 return line;
});
const output=out.join('\n');
const parsed=parseStory(output);
if(Object.keys(parsed.items).length!==Object.keys(story.items).length||parsed.recipes.length!==story.recipes.length)throw new Error('Presentation integration changed story identities or recipes');
writeFileSync(resolve(root,'anatomy.md'),output);
writeFileSync(resolve(root,'atlas/identity-aliases.json'),JSON.stringify(Object.fromEntries(Object.entries(aliases).map(([a,b])=>[b,a])),null,2)+'\n');
writeFileSync(resolve(root,'atlas/coverage.json'),JSON.stringify({items:Object.keys(story.items).length,slots:Object.values(story.items).reduce((n,i)=>n+i.slots.length,0),packages,background:'blank-paper.png',finaleBackground:'blank-paper-tall.svg',chapterAppearances:appearances},null,2)+'\n');
console.log(`Integrated ${Object.keys(story.items).length} illustrated identities and ${Object.values(story.items).reduce((n,i)=>n+i.slots.length,0)} fitted parts`);
