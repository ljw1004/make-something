import {test} from 'node:test';
import assert from 'node:assert/strict';
import {parseStory} from '../src/story/parser.ts';
import {startAdventure,choose,renderFrame} from '../src/playtest/adventure.ts';
import {terminalFrame,terminalParts} from '../src/web/text-terminal-frame.ts';
import {terminalStory} from './fixtures/text-terminal.ts';

test('terminal pictures follow real visits across automatic arrivals and skips without changing runner state or text',()=>{
  const story=parseStory(terminalStory,{id:'terminal'});
  let adventure=startAdventure(story,{playStyle:'fast'}), visits=0;
  const pictures:number[]=[];
  while (true) {
    const before=structuredClone(adventure);
    const parts=terminalParts(story,adventure,visits);
    assert.equal(parts.filter(p=>p.kind==='text').map(p=>p.text).join(''),renderFrame(terminalFrame(story,adventure)));
    pictures.push(...parts.filter(p=>p.kind==='image').map(p=>p.chapter));
    assert.deepEqual(adventure,before);
    visits=adventure.state.visited.length;
    const look=terminalParts(story,adventure,visits,true);
    assert(look.every(p=>p.kind==='text'));
    assert.deepEqual(adventure,before);
    if (adventure.frame.phase !== 'choose') break;
    adventure=choose(story,adventure,adventure.frame.step,1);
  }
  assert.deepEqual(pictures,[0,1,3,4]);
  assert(adventure.state.completed);
});

test('a final chapter completed in advance keeps the runner ending without inventing a scenery visit',()=>{
  const story=parseStory(`# Complete early
## Make
background: ![Bench](bench.svg)
**Goals**
- Make it -- C
**Items**
- A
- B
- C
**Combinations**
- A + B -> C
## Already done
background: ![Not entered](last.svg)
**Goals**
- Have it -- C
`,{id:'early'});
  const initial=startAdventure(story);
  const end=choose(story,initial,initial.frame.step,1);
  assert(end.state.completed);
  const parts=terminalParts(story,end,initial.state.visited.length);
  assert(parts.every(part=>part.kind==='text'));
  assert.equal(parts.map(part=>part.kind==='text'?part.text:'').join(''),renderFrame(terminalFrame(story,end)));
});

test('checkpoint scrollback pairs scenery with actual chapters even when its history recounts skipped chapters',()=>{
  const story=parseStory(terminalStory,{id:'terminal'});
  for (let chapter=1;chapter<=story.chapters.length;chapter++) {
    const adventure=startAdventure(story,{chapter});
    const before=structuredClone(adventure);
    const parts=terminalParts(story,adventure,0,false,chapter);
    assert.equal(parts.filter(p=>p.kind==='text').map(p=>p.text).join(''),renderFrame(terminalFrame(story,adventure)));
    assert.deepEqual(parts.filter(p=>p.kind==='image').map(p=>p.chapter),adventure.state.visited);
    assert.deepEqual(adventure,before);
  }
});
