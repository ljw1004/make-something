#!/usr/bin/env node
// Exhaust each chapter's legal orders. Track the physical supplies represented
// by each result, so a protected goal witness cannot leave a second loose copy.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {parseStory} from '../../../src/story/parser.ts';
import {checkpoint} from '../../../src/debug/checkpoint.ts';
import {isFixed} from '../../../src/engine/fixed-items.ts';
import {act,legalActions,recipeFor,chapterComplete,availableTokens} from '../../../src/engine/game.ts';
import {dismissTextOnlyWonders} from '../../../src/web/item-readings.ts';
const [file,out]=process.argv.slice(2);
if(!file)throw new Error('Expected manuscript path [scratch outcome.json]');
const source=fs.readFileSync(file,'utf8'),story=parseStory(source,{id:file,file});
const results=[];
for(let chapter=0;chapter<story.chapters.length-1;chapter++){
 const start=checkpoint(story,chapter);
 while(start.pending.length){Object.assign(start,act(story,start,{type:'dismiss'}));}
 const tangible=state=>availableTokens(state).filter(t=>t.chapter===chapter&&!isFixed(story,t));
 const leaves=Object.fromEntries(tangible(start).map(t=>[t.id,[t.id]]));
 const queue=[[start,0,leaves]],visited=new Map(),recipesSeen=new Set();let finishes=0,edges=0,steps,final;
 while(queue.length){
  const [state,count,ancestry]=queue.pop();
  const occurrences=new Map();
  for(const token of tangible(state))for(const leaf of ancestry[token.id]??[token.id]){
   assert.ok(!occurrences.has(leaf),`Chapter ${chapter+1}: ${leaf} appears in both ${occurrences.get(leaf)} and ${token.id}`);
   occurrences.set(leaf,token.id);
  }
  const key=JSON.stringify([Object.values(state.tokens).filter(t=>t.chapter===chapter).map(t=>[t.id,t.status]).sort(),[...state.achieved].sort()]);
  if(visited.has(key)){assert.equal(visited.get(key),count,'Equivalent states need equal physical operations');continue;}
  visited.set(key,count);assert.ok(visited.size<50000,'Chapter search needs investigation');
  assert.equal(state.pending.length,0,'No routine result popups');
  if(chapterComplete(story,state)){
   const ids=tangible(state).map(t=>t.id).sort();
   assert.equal(ids.length,1,`Chapter ${chapter+1} leaves loose parts: ${ids}`);
   steps??=count;final??=ids;assert.equal(count,steps);assert.deepEqual(ids,final);finishes++;continue;
  }
  const actions=legalActions(story,state);assert.ok(actions.length,`Chapter ${chapter+1}: every partial build can finish`);
  for(const action of actions){
   assert.equal(action.type,'combine');const recipe=recipeFor(story,state,action);recipesSeen.add(recipe.id);
   const inputs=[action.a,action.b].filter(id=>id&&!isFixed(story,state.tokens[id]));
   const nextLeaves=inputs.flatMap(id=>ancestry[id]??[id]);
   const next=dismissTextOnlyWonders(story,act(story,state,action));edges++;queue.push([next,count+1,{...ancestry,[recipe.result.id]:nextLeaves}]);
  }
 }
 const authored=story.recipes.filter(r=>r.source.line>story.chapters[chapter].source.line&&r.source.line<story.chapters[chapter+1].source.line);
 for(const recipe of authored)assert.ok(recipesSeen.has(recipe.id),`Chapter ${chapter+1}: recipe has no execution witness: ${recipe.id}`);
 const result={chapter:chapter+1,title:story.chapters[chapter].name,states:visited.size,edges,finishes,steps,final,recipesCovered:recipesSeen.size};
 results.push(result);console.log(JSON.stringify(result));
}
const end=checkpoint(story,story.chapters.length);assert.equal(end.completed,true);
const outcome={sourceSha256:createHash('sha256').update(source).digest('hex'),chapters:story.chapters.length,recipes:story.recipes.length,route:end.actions.filter(a=>a.type==='combine').length,results};
if(out)fs.writeFileSync(out,JSON.stringify(outcome,null,2)+'\n');
console.log(JSON.stringify({chapters:outcome.chapters,recipes:outcome.recipes,route:outcome.route,states:results.reduce((n,r)=>n+r.states,0),edges:results.reduce((n,r)=>n+r.edges,0)}));
