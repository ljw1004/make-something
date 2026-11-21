import {readFileSync} from 'node:fs';
import {isDeepStrictEqual} from 'node:util';
import {parseStory} from '../../../../src/story/parser.ts';

function semantics(path:string){
  const s=parseStory(readFileSync(path,'utf8'));
  const ref=(r:any)=>r&&{id:r.id,slots:r.slots};
  const ingredient=(i:any)=>i&&{ref:ref(i.ref),fate:i.fate};
  return {
    chapters:s.chapters.map(c=>({id:c.id,name:c.name,intro:c.intro,skipped:c.skipped,items:c.items,hotspots:c.hotspots,goalOperator:c.goalOperator,goals:c.goals.map(g=>({text:g.text,next:g.next,operator:g.operator,conditions:g.conditions.map(q=>({item:ref(q.item),hotspot:q.hotspot}))}))})),
    items:Object.fromEntries(Object.entries(s.items).map(([id,i])=>[id,{name:i.name,compound:i.compound,exclusiveWith:i.exclusiveWith,slots:i.slots.map(q=>({name:q.name,accepts:q.accepts})),wonders:i.wonders.map(w=>({popup:w.popup,encyclopedia:w.encyclopedia,requires:w.requires})),presentations:i.presentations.filter(p=>p.name!==undefined).map(p=>({chapter:{kind:p.chapter.kind,value:p.chapter.value},name:p.name}))}])),
    recipes:s.recipes.map(r=>({a:ingredient(r.a),b:ingredient(r.b),at:ingredient(r.at),hotspot:r.hotspot,result:ref(r.result),installation:r.installation})),
    tutorials:s.tutorials?.map(t=>({chapter:t.chapter,recipe:t.recipe})),
  };
}
const baseline=semantics('projects/anatomy-study/anatomy.md');
for(const path of process.argv.slice(2)){
  const actual=semantics(path);
  const differing=Object.keys(baseline).filter(k=>!isDeepStrictEqual(baseline[k],actual[k]));
  console.log(JSON.stringify({path,equivalent:differing.length===0,differing}));
  if(differing.length) process.exitCode=1;
}
