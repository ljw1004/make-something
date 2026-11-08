#!/usr/bin/env node
// Exhaust every legal assembly ordering in the two independent racer chapters.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {parseStory} from '../../../src/story/parser.ts';
import {checkpoint} from '../../../src/debug/checkpoint.ts';
import {isFixed} from '../../../src/engine/fixed-items.ts';
import {act,legalActions,recipeFor,chapterComplete,availableTokens} from '../../../src/engine/game.ts';
const file=process.argv[2];if(!file)throw new Error('Expected manuscript path');
const story=parseStory(fs.readFileSync(file,'utf8'),{id:file,file});
const outcomes=[];
for(const [chapter,expected,final] of [[1,4,'id:wr-sail'],[2,10,'id:wind-racer']]){
 const start=checkpoint(story,chapter),queue=[[start,0]],visited=new Set(),recipesSeen=new Set();let finishes=0,edges=0;
 while(queue.length){
  const [state,count]=queue.pop();
  const key=JSON.stringify([Object.values(state.tokens).filter(t=>t.chapter===chapter||t.id==='id:wr-sail').map(t=>[t.id,t.status]).sort(),[...state.achieved].sort()]);
  if(visited.has(key))continue;visited.add(key);
  assert.equal(state.pending.length,0,'No routine popups');
  const pieces=availableTokens(state).filter(t=>t.chapter===chapter&&!isFixed(story,t));
  if(chapterComplete(story,state)){
   assert.equal(count,expected);assert.deepEqual(pieces.map(t=>t.id),[final]);finishes++;continue;
  }
  assert.ok(count<expected,'No duplicate parts or redundant successful combinations');
  const actions=legalActions(story,state);assert.ok(actions.length,'Every partial build can finish');
  for(const action of actions){recipesSeen.add(recipeFor(story,state,action).id);const next=act(story,state,action);edges++;queue.push([next,count+1]);}
 }
 const authored=story.recipes.filter(r=>r.source.line>story.chapters[chapter].source.line&&r.source.line<story.chapters[chapter+1].source.line);
 for(const recipe of authored)assert.ok(recipesSeen.has(recipe.id),'Every authored recipe has an actual execution witness: '+recipe.id);
 outcomes.push({chapter:chapter+1,states:visited.size,edges,finishes,steps:expected,recipesCovered:recipesSeen.size});
}
const complete=checkpoint(story,story.chapters.length);assert.equal(complete.completed,true);
console.log(JSON.stringify({outcomes,chapters:story.chapters.length,recipes:story.recipes.length,fullRoute:complete.actions.filter(a=>a.type==='combine').length}));
