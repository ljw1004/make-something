/** Resolve the actual chapter presentations for contact-sheet inventories. */
import {readFileSync,writeFileSync,existsSync} from 'node:fs';
import {resolve} from 'node:path';
import {parseStory} from '../../../../src/story/parser.ts';
import {itemPresentation} from '../../../../src/engine/presentation.ts';
const root=resolve(import.meta.dirname,'..');
const inventory=JSON.parse(readFileSync(resolve(import.meta.dirname,'comparison-inventory.json'),'utf8'));
for(const theme of process.argv.slice(2)){
 const dir=resolve(root,theme),s=parseStory(readFileSync(resolve(dir,'anatomy.md'),'utf8'));
 const chapters=[];
 for(const [number,expected] of Object.entries(inventory) as [string,any][]){
  const n=Number(number),c=s.chapters[n-1],ids=expected.items.map((i:any)=>i.id);
  const assets:any[]=[];
  for(const id of ids){
   const p=itemPresentation(s,n-1,id),h=c.hotspotDefinitions?.[id];
   const icon=h?.icon??p.icon;
   if(!icon||!existsSync(resolve(dir,icon.url)))throw Error(`${theme} chapter ${n}: missing ${id}`);
   if(/unillustrated|placeholder|neutral|default-icon/.test(icon.url))throw Error(`${theme} chapter ${n}: placeholder ${id}`);
   assets.push({id,label:p.name,path:icon.url,kind:c.hotspots.includes(id)?'receiver':'item'});
   const slots=s.items[id].slots.filter(q=>ids.includes(q.accepts));
   for(const q of slots){if(!q.icon||!existsSync(resolve(dir,q.icon.url)))throw Error(`Missing fitting ${theme} ${id} ${q.accepts}`);assets.push({id:`${id}[${q.accepts}]`,label:`${p.name}: ${s.items[q.accepts].name} fitting`,path:q.icon.url,kind:'fitting'});}
   for(let bits=1;bits<(1<<slots.length);bits++){
    const included=slots.filter((_,j)=>bits&(1<<j));
    assets.push({id:`${id}:state-${bits}`,label:`${p.name} + ${included.map(q=>s.items[q.accepts].name).join(' + ')}`,layers:[icon.url,...included.map(q=>q.icon!.url)],kind:'assembled'});
   }
  }
  chapters.push({number:n,title:c.name,background:c.image,assets});
 }
 writeFileSync(resolve(dir,'comparison-assets.json'),JSON.stringify({theme,chapters},null,2)+'\n');
 console.log(`${theme}: ${chapters.map(c=>`${c.number}=${c.assets.length}`).join(', ')} images/states`);
}
