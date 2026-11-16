/** Freeze independent chapter review packets; uses the native parser and legal route. */
import{readFileSync,writeFileSync,mkdirSync,copyFileSync,existsSync}from'node:fs';import{resolve,dirname}from'node:path';import{createHash}from'node:crypto';
import{parseStory}from'../../../../src/story/parser.ts';import{checkpoint}from'../../../../src/debug/checkpoint.ts';import{act,recipeFor}from'../../../../src/engine/game.ts';import{itemPresentation,hotspotPresentation}from'../../../../src/engine/presentation.ts';
const project=resolve(import.meta.dirname,'../..'),round=process.argv[2]||'round-0',out=resolve('runs/anatomy-composition-review',round);
if(existsSync(out))throw new Error('Choose a new round; frozen review packets must never be overwritten: '+out);
const retainedFile=resolve(import.meta.dirname,'outcomes.json');
if(existsSync(retainedFile)){const retained=JSON.parse(readFileSync(retainedFile,'utf8'));if(retained.chapters?.some((c:any)=>c.reviewRounds?.includes(round)))throw new Error('Choose a new round; this name already exists in retained review outcomes: '+round);}
mkdirSync(out,{recursive:true});
const source=readFileSync(resolve(project,'anatomy.md'),'utf8'),story=parseStory(source);writeFileSync(resolve(out,'source.md'),source);
const hash=createHash('sha256').update(source).digest('hex'),copied=new Set<string>();
function freeze(path:string){if(!copied.has(path)){const dest=resolve(out,'assets',path);mkdirSync(dirname(dest),{recursive:true});copyFileSync(resolve(project,path),dest);copied.add(path);}return resolve(out,'assets',path);}
function picture(id:string,chapter:number,state:any){const item=story.items[id],p=itemPresentation(story,chapter,id);const icon=story.chapters[chapter].hotspots.includes(id)?hotspotPresentation(story,state,chapter,id).icon:p.icon;const slots=state.tokens[id]?.slots??[];return{id,name:p.name,base:freeze(icon!.url),layers:item.slots.filter(s=>slots.includes(s.accepts)).map(s=>freeze(s.icon!.url)),fitted:slots.map(s=>story.items[s].name)};}
let state=checkpoint(story,0);const chunks=source.split(/^## /m).slice(1),man=[];
for(let c=0;c<28;c++){
 const folder=resolve(out,String(c+1).padStart(2,'0'));mkdirSync(folder,{recursive:true});copyFileSync(resolve(project,'atlas/chapter-sheets',`chapter-${c+1}.jpg`),resolve(folder,'inventory.jpg'));
 const end=checkpoint(story,c+1,state),operations=[];
 for(const action of end.actions.slice(state.actions.length)){
  if(action.type==='combine'){
   const r=recipeFor(story,state,action)!;const a=picture(r.a.ref.id,c,state),b=picture(r.b?.ref.id??action.hotspot!,c,state),next=act(story,state,action),result=picture(r.result.id,c,next);
   operations.push({a,b,result,type:r.installation?'fitting':'combination',fates:[r.a.fate,r.b?.fate],rule:`${a.name} + ${b.name} → ${result.name}${result.fitted.length?' [contains '+result.fitted.join(', ')+']':''}`});state=next;
  }else{state=act(story,state,action);}
 }
 const allIds=[...new Set(story.chapters[c].items.map(i=>i.id))];const packet={chapter:c+1,title:story.chapters[c].name,sourceHash:hash,operations,inventory:allIds.map(id=>picture(id,c,end)),note:'Recipe strips preserve source/4 scale. Inventory thumbnails are normalized and must not establish physical scale.'};
 writeFileSync(resolve(folder,'packet.json'),JSON.stringify(packet,null,2));
 let chunk=chunks[c];for(const [id,item]of Object.entries(story.items))if(id.startsWith('id:'))chunk=chunk.replaceAll('`'+id.slice(3)+'`',item.name);
 writeFileSync(resolve(folder,'recipes.md'),`# Chapter ${c+1}: ${story.chapters[c].name}\n\n${story.chapters[c].intro}\n\n## Native reference construction sequence\n${operations.map((o,i)=>`${i+1}. ${o.rule}. Input fates: ${o.fates.join(', ')}.`).join('\n')}\n\n## All authored combinations, goals and context\n${chunk.replace(/^.*\n/,'').replace(/^.*icon:.*\n/gm,'').replace(/^background:.*\n/gm,'')}\n`);
 man.push({chapter:c+1,folder,title:story.chapters[c].name});
}
writeFileSync(resolve(out,'manifest.json'),JSON.stringify(man,null,2));console.log(out);
