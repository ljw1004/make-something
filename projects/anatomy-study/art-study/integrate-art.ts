/** Study-only presentation exporter. Uses the shared parser; never changes rules.
 * Usage: node projects/anatomy-study/art-study/integrate-art.ts THEME/art-map.json
 * All image paths in the map are relative to THEME/anatomy.md.
 */
import {readFileSync,writeFileSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {parseStory} from '../../../src/story/parser.ts';

type HotspotArt={center:[number,number];icon?:string;hitbox?:{center:[number,number];size:[number,number]}};
type ArtMap={
  headingIcon:string; defaultIcon:string; defaultOverlay:string; defaultBackground:string;
  chapterBackgrounds:Record<string,string>; itemIcons:Record<string,string>;
  slotIcons:Record<string,Record<string,string>>;
  hotspots?:Record<string,Record<string,HotspotArt>>;
  itemPositions?:Record<string,[number,number]>;
};
const mapPath=resolve(process.argv[2]??'');
if(!process.argv[2])throw new Error('Supply THEME/art-map.json');
const map:ArtMap=JSON.parse(readFileSync(mapPath,'utf8'));
for(const key of ['headingIcon','defaultIcon','defaultOverlay','defaultBackground'] as const)if(!map[key])throw new Error(`Missing ${key}`);
const source=readFileSync(resolve(import.meta.dirname,'../anatomy.md'),'utf8');
const story=parseStory(source);
if(Object.values(story.items).some(i=>i.icon))throw new Error('Source now contains artwork; reconcile the exporter before regenerating.');
const lines=source.split('\n'),declarations=new Map<string,number>();
const after=new Map<number,string[]>(),replace=new Map<number,string>();
let section='',chapter=0;
const identity=(text:string)=>{
  const id=text.match(/^`([^`]+)`/);
  return id?'id:'+id[1]:'name:'+text.replace(/ \(compound\)$/,'');
};
const image=(url:string)=>`![Illustration](${url})`;
const append=(line:number,text:string)=>after.set(line,[...(after.get(line)??[]),text]);
for(let n=0;n<lines.length;n++){
  const line=lines[n];
  if(line.startsWith('## ')){chapter++;section='';}
  if(line.startsWith('**'))section=line;
  if(section==='**Items**'&&line.startsWith('- ')){
    const id=identity(line.slice(2));
    if(story.items[id]&&!declarations.has(id))declarations.set(id,n);
  }
  if(line.startsWith('# '))replace.set(n,line.replace(/!\[[^\]]*\]\([^)]+\)/,image(map.headingIcon)));
  if(line.startsWith('background:'))replace.set(n,`background: ${image(map.chapterBackgrounds[String(chapter)]??map.defaultBackground)}`);
  if(section==='**Hotspots**'&&line.startsWith('- ')){
    const art=map.hotspots?.[String(chapter)]?.[identity(line.slice(2))];
    if(!art)continue;
    replace.set(n,`${line} (center ${art.center[0]}px, ${art.center[1]}px)`);
    if(art.icon)append(n,`  - icon: ${image(art.icon)}`);
    if(art.hitbox)append(n,`  - hitbox: (center ${art.hitbox.center[0]}px, ${art.hitbox.center[1]}px) (size ${art.hitbox.size[0]}px, ${art.hitbox.size[1]}px)`);
  }
}
for(const [id,item] of Object.entries(story.items)){
  const line=declarations.get(id);
  if(line===undefined)throw new Error(`No standalone Items declaration for ${id}`);
  const pos=map.itemPositions?.[id];
  append(line,`  - icon: ${image(map.itemIcons[id]??map.defaultIcon)}${pos?` (center ${pos[0]}px, ${pos[1]}px)`:''}`);
  for(const slot of item.slots){
    const index=slot.source.line-1;
    replace.set(index,`${lines[index]}, icon: ${image(map.slotIcons[id]?.[slot.accepts]??map.defaultOverlay)}`);
  }
}
const output=lines.flatMap((line,n)=>[replace.get(n)??line,...(after.get(n)??[])]).join('\n');
const destination=resolve(dirname(mapPath),'anatomy.md');
writeFileSync(destination,output);
console.log(destination);
