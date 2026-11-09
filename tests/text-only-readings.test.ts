import {test} from 'node:test';
import assert from 'node:assert/strict';
import {browserItemText,textOnlyPassages} from '../src/story/text-only.ts';
import {parseStory} from '../src/story/parser.ts';
import {act,newGame,replay} from '../src/engine/game.ts';
import {browserReadings,dismissTextOnlyWonders} from '../src/web/item-readings.ts';
import {encyclopediaEntries} from '../src/web/encyclopedia.ts';
import {encyclopediaBook} from '../src/web/encyclopedia-book.ts';
import {readItem} from '../src/playtest/observe.ts';
import {choose,renderFrame,startAdventure} from '../src/playtest/adventure.ts';
import {itemPictureDescription} from '../src/playtest/picture-descriptions.ts';

const manuscript=(description:string)=>`# Pictures
## Make
**Goals**
- Finish -- C
**Items**
- A
- B
- C
${description.split('\n').map(line=>'  '+line).join('\n')}
**Combinations**
- A [transform] + B [consume] -> C
`;
const combination={type:'combine' as const,a:'name:A',b:'name:B'};

test('braced passages omit only complete prose spans, preserving links, images, code and escaped braces',()=>{
 assert.equal(browserItemText('Visible. {A red disc with {two} holes.}\n\nStill visible.'),'Visible. \n\nStill visible.');
 assert.equal(browserItemText('{First.}\n\n{Second.}'),'');
 const literal='[a {label}](https://example.com/{path}) ![a {caption}](image.svg) `{code}` \\{literal\\}';
 assert.equal(browserItemText(literal),literal);
 assert.equal(browserItemText('Unfinished {description'),'Unfinished {description');
 assert.equal(browserItemText('Unfinished {outer {inner}'),'Unfinished {outer {inner}');
 assert.deepEqual(textOnlyPassages('Unfinished {outer {inner}'),[]);
 assert.equal(browserItemText('An unmatched } remains.'),'An unmatched } remains.');
 for(const picture of ['A label reads `}` here.','A label [close](https://example.com/}) sits here.','A mark ![opening {](image.svg) sits here.']){
  assert.equal(browserItemText(`{${picture}} Visible.`),'Visible.');
  assert.deepEqual(textOnlyPassages(`{${picture}} Visible.`),[picture]);
 }
});

test('hidden-only wonders remain in text play but auto-dismiss through replayable browser actions',()=>{
 const story=parseStory(manuscript('{A red wheel on a wooden axle.}'));
 assert.deepEqual(story.diagnostics,[]);
 const made=act(story,newGame(story),combination);
 assert.equal(made.pending[0].markdown,'{A red wheel on a wooden axle.}');
 assert.equal(readItem(story,made,'name:C').text,'{A red wheel on a wooden axle.}');
 assert.equal(browserReadings(story,made,'name:C')[0].encyclopedia,'');
 assert.deepEqual(encyclopediaEntries(story,made),[]);
 const browser=dismissTextOnlyWonders(story,made);
 assert.equal(browser.pending.length,0);assert.equal(made.pending.length,1);
 assert.equal(browser.actions.at(-1)?.type,'dismiss');
 assert.deepEqual(replay(story,browser.actions),browser);
 for(const playStyle of ['fast','detailed'] as const){
  const initial=startAdventure(story,{playStyle});
  const after=choose(story,initial,initial.frame.step,playStyle==='fast'?1:{combine:'A',with:'B'});
  assert.match(renderFrame(after.frame),/A red wheel on a wooden axle/);
 }
});

test('mixed and split readings keep visible prose and ordinary conditional slot readings',()=>{
 const story=parseStory(manuscript('Finished. {A red wheel.}\n---\n{A brown axle.}\n\nRead the [source](https://example.com).'));
 const state=act(story,newGame(story),combination),readings=browserReadings(story,state,'name:C');
 assert.equal(readings[0].popup,'Finished.');
 assert.equal(readings[0].encyclopedia,'Read the [source](https://example.com).');
 assert.equal(dismissTextOnlyWonders(story,state),state);
 const html=encyclopediaBook(story,state,'name:C',true,p=>p);
 assert.match(html,/href="https:\/\/example.com"/);assert.doesNotMatch(html,/brown axle/);
 const compound=parseStory(`# Fittings
## Build
**Goals**
- Finish -- Box[Motor]
**Items**
- Box (compound)
  - slot: drive, accepts Motor

  [Motor] {A motor sits inside the box.} It runs.
- Motor
`);
 assert.deepEqual(compound.diagnostics,[]);
 const fitted=act(compound,newGame(compound),{type:'combine',a:'name:Motor',b:'name:Box'});
 assert.equal(browserReadings(compound,fitted,'name:Box')[0].popup,'It runs.');
});

test('text boards and creation results describe present pictures without exposing future prose',()=>{
 const story=parseStory(`# Pictures
## Build
**Goals**
- Make cart -- Cart
**Items**
- Wood
  {A flat brown board with four round holes.}
- Wheels
- Cart
  - icon: ![Cart](cart.svg)

  {A brown board above four red wheels.}
  ---
  Hidden future explanation about how the drive works.
**Combinations**
- Wood + Wheels -> Cart
## Later
**Goals**
- Finish -- Future
**Items**
- Part
- Future
  - icon: ![Future](future.svg)

  {Unseen future picture.}
**Combinations**
- Cart + Part -> Future
`);
 const state=newGame(story);
 assert.equal(itemPictureDescription(story,state,'name:Wood'),'A flat brown board with four round holes.');
 for(const playStyle of ['fast','detailed'] as const){
  const initial=startAdventure(story,{playStyle});
  const frame=renderFrame(initial.frame);
  assert.match(frame,/Picture: A flat brown board/);
  assert.doesNotMatch(frame,/A brown board above four red wheels/);
  const after=choose(story,initial,initial.frame.step,playStyle==='fast'?1:{combine:'Wood',with:'Wheels'});
  assert.match(renderFrame(after.frame),/Picture: A brown board above four red wheels/);
  assert.doesNotMatch(frame,/Hidden future|Unseen future/);
 }
});
