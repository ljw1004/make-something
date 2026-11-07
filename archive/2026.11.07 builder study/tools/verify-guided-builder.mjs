#!/usr/bin/env node
// Chapter-local branch and instruction check. No screenshots or run bundles.
// Usage: node THIS_FILE STORY BASELINE_V21 ASSEMBLY_SPLITS_JSON
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {parseStory} from '../../../src/story/parser.ts';
import {checkpoint} from '../../../src/debug/checkpoint.ts';
import {act,newGame,chapterComplete,visibleGoals,legalActions,recipeFor} from '../../../src/engine/game.ts';
import {canonicalState} from '../../../src/lint/opportunity-state.ts';
import {lintStory} from '../../../src/lint/lint.ts';

const [file,baselineFile,planFile]=process.argv.slice(2);
if(!planFile)throw new Error('Expected STORY BASELINE_V21 ASSEMBLY_SPLITS_JSON');
const source=fs.readFileSync(file,'utf8'),story=parseStory(source);
const baselineSource=fs.readFileSync(baselineFile,'utf8'),baseline=parseStory(baselineSource);
const plan=JSON.parse(fs.readFileSync(planFile,'utf8'));
const authored=s=>s.split('\n').filter(l=>/^- `.* -> `/.test(l)).map(l=>l.slice(2).replaceAll('`','').replace(/ \(tutorial\)$/, ''));
const neutral=s=>s.replace(/ \[(?:consume|preserve|transform)\]/g,'').replaceAll(' @ ',' + ');
const expected=authored(baselineSource);
for(const chapter of plan.chapters)for(const replacement of chapter.replace_recipes){
  const index=expected.findIndex(r=>neutral(r)===replacement.old);
  assert(index>=0,'Missing old mapping recipe: '+replacement.old);
  expected.splice(index,1,...replacement.new);
}
assert.deepEqual(authored(source).sort(),expected.sort(),'Recipe changes differ from the explicit split plan');
assert.deepEqual(Object.keys(story.items).filter(id=>!baseline.items[id]).sort(),
  plan.chapters.flatMap(c=>c.new_items.map(i=>'id:'+i.id)).sort(),'New identities differ from the split plan');
const compounds=s=>Object.values(s.items).filter(i=>i.compound).map(i=>({id:i.id,slots:i.slots.map(({name,accepts,icon})=>({name,accepts,icon:icon?.url}))}));
assert.deepEqual(compounds(story),compounds(baseline),'Compound acceptance changed');
assert.equal(story.chapters.length,baseline.chapters.length);
assert.equal(lintStory(story,{analysis:false}).filter(d=>d.severity==='error').length,0);
const finish=checkpoint(story,story.chapters.length);
assert(finish.completed,'Completion checkpoint failed');
let replay=newGame(story);const suffixStart=new Map();
for(const [index,action] of finish.actions.entries()){
  if(action.type==='advance')suffixStart.set(replay.chapter,index);
  replay=act(story,replay,action);assert(visibleGoals(story,replay).length<=1);
}
assert(replay.completed,'Full witness replay failed');
const key=s=>JSON.stringify({tokens:Object.values(s.tokens).map(t=>({id:t.id,status:t.status,chapter:t.chapter,slots:[...t.slots].sort(),hotspot:t.hotspot})).sort((a,b)=>a.id.localeCompare(b.id)),achieved:[...s.achieved].sort(),excluded:s.excluded});
const reached=new Set();let states=0,edges=0,terminals=0;
for(let chapter=0;chapter<story.chapters.length-1;chapter++){
  const initial=canonicalState(checkpoint(story,chapter));assert.equal(initial.chapter,chapter);
  const queue=[initial],seen=new Set();
  while(queue.length){
    const state=queue.shift(),signature=key(state);if(seen.has(signature))continue;
    seen.add(signature);assert(seen.size<=30000,'Chapter state bound reached');
    assert(visibleGoals(story,state).length<=1,'Multiple visible instructions');
    const recipes=new Set(),next=[];
    for(const action of legalActions(story,state)){
      const recipe=recipeFor(story,state,action);if(recipes.has(recipe.id))continue;
      if([action.a,action.b,action.hotspot].filter(Boolean).some(id=>state.tokens[id].chapter!==chapter))continue;
      recipes.add(recipe.id);reached.add(recipe.id);edges++;
      next.push(canonicalState(act(story,state,action)));
    }
    if(!next.length){
      assert(chapterComplete(story,state),'Unfinished terminal branch');
      let continuation=state;
      for(const action of finish.actions.slice(suffixStart.get(chapter)))continuation=act(story,continuation,action);
      assert(continuation.completed,'Alternate branch cannot finish');terminals++;
    }
    queue.push(...next);
  }
  states+=seen.size;
}
assert.equal(story.recipes.filter(r=>!reached.has(r.id)).length,0,'Unreached recipes');
console.log(JSON.stringify({recipes:story.recipes.length,goals:story.chapters.reduce((n,c)=>n+c.goals.length,0),references:story.chapters.filter(c=>c.reference).length,combinations:finish.actions.filter(a=>a.type==='combine').length,replayedActions:finish.actions.length,states,edges,continuedTerminalBranches:terminals}));
