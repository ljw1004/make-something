import {test} from 'node:test';
import assert from 'node:assert/strict';
import {parseStory} from '../src/story/parser.ts';
import {newGame} from '../src/engine/game.ts';
import {board,choose,renderFrame,startAdventure} from '../src/playtest/adventure.ts';
import {itemArtworkDescription,itemMotionDescription,referencePictureDescription,sceneMotionDescription} from '../src/playtest/picture-descriptions.ts';
import type {State} from '../src/engine/types.ts';

const manuscript = `# Moving pictures
## First
background: ![room](room.svg)
background animation: ![A curtain moves gently from side to side.](room.webp)
reference: ![Wheel](wheel.svg)
**Goals**
- Finish -- Future
**Hotspots**
- Bench
  - icon: ![still bench](bench.svg)
- Fan
- Panel
  - icon after creating Signal: ![still panel](panel.svg)
**Items**
- \`wheel\` Wheel
  - icon: ![wheel](wheel.svg)
  - animation: ![The red wheel turns around its central axle.](wheel.webp)
  - from chapter "Second" animation: ![The red wheel turns twice as fast.](fast.webp)
  - from chapter "Still" animation: none

  {A red wheel with four spokes.}
- Bench
  - icon: ![bench](bench.svg)
  - animation: ![The bench rocks.](bench.webp)
- Fan
  - icon: ![fan](fan.svg)
  - animation: ![The fan blades spin.](fan.webp)
- Panel
  - icon: ![panel](panel.svg)
  - animation: ![The panel turns back and forth.](panel.webp)
- Seed
- Tool
- Signal
- Future
  - icon: ![future](future.svg)
  - animation: ![Unseen future motion.](future.webp)
**Combinations**
- Seed + Tool -> Signal
- \`wheel\` + Signal -> Future
## Second
**Goals**
- Continue -- Future
## Still
background animation: none
**Goals**
- Continue -- Future
## Fresh
background: ![new room](fresh.svg)
**Goals**
- Continue -- Future
## Later scene
background animation: ![Unseen later scene motion.](later.webp)`;

const story = parseStory(manuscript);
function atChapter(state: State, chapter: number): State {
  return {...state, chapter, visited: Array.from({length: chapter+1}, (_, i) => i),
    tokens: Object.fromEntries(Object.entries(state.tokens).map(([id, token]) => [id, {...token, chapter}]))};
}

test('board motion uses current chapter variants, omits still overrides and never changes the static reference', () => {
  const initial=newGame(story);
  for(const [chapter,expected] of [[0,'The red wheel turns around its central axle.'],[1,'The red wheel turns twice as fast.'],[2,'']] as const){
    const state=atChapter(initial,chapter),text=board(story,state);
    assert.equal(itemMotionDescription(story,state,'id:wheel'),expected);
    if(expected)assert(text.includes(`  Motion: ${expected}`));
    else assert.doesNotMatch(text,/Motion: The red wheel/);
    assert.doesNotMatch(text,/Unseen future motion|Unseen later scene motion/);
  }
  assert.equal(referencePictureDescription(story,initial),'Wheel: A red wheel with four spokes.');
  assert.match(board(story,initial),/Build reference: Wheel: A red wheel with four spokes\.\n\n/);
  for(const playStyle of ['fast','detailed'] as const){
    const frame=renderFrame(startAdventure(story,{mode:'chapter',playStyle}).frame);
    assert.match(frame,/Motion: The red wheel turns around its central axle/);
    assert.match(frame,/Scene motion: A curtain moves gently/);
    assert.doesNotMatch(frame,/Unseen future motion|Unseen later scene motion/);
  }
});

test('fixed artwork precedence includes explicit same-URL icons and creation-triggered variants', () => {
  const state=newGame(story);
  assert.equal(itemMotionDescription(story,state,'name:Bench'),'');
  assert.equal(itemMotionDescription(story,state,'name:Fan'),'The fan blades spin.');
  assert.equal(itemMotionDescription(story,state,'name:Panel'),'The panel turns back and forth.');
  const changed={...state,tokens:{...state.tokens,'name:Signal':{id:'name:Signal',chapter:0,status:'consume' as const,slots:[],x:0,y:0}}};
  assert.equal(itemMotionDescription(story,changed,'name:Panel'),'');
  assert.doesNotMatch(board(story,changed),/The bench rocks|The panel turns back and forth/);
});

test('absent, retired, off-board and unrenderable objects expose no motion observation', () => {
  const state=newGame(story);
  assert.equal(itemMotionDescription(story,state,'name:Future'),'');
  for(const change of [{status:'consume' as const},{chapter:1}]){
    const hidden={...state,tokens:{...state.tokens,'id:wheel':{...state.tokens['id:wheel'],...change}}};
    assert.equal(itemArtworkDescription(story,hidden,'id:wheel'),'');
    assert.doesNotMatch(board(story,hidden),/Motion: The red wheel/);
  }
  const noPoster=parseStory(manuscript.replace('  - icon: ![wheel](wheel.svg)\n',''));
  assert.equal(itemMotionDescription(noPoster,newGame(noPoster),'id:wheel'),'');
  const blank=parseStory(manuscript.replace('![The red wheel turns around its central axle.]','![   ]'));
  assert.equal(itemMotionDescription(blank,newGame(blank),'id:wheel'),'');
  const compound=parseStory(`# Parts
## Build
**Items**
- Box (compound)
  - icon: ![box](box.svg)
  - animation: ![The box shakes.](box.webp)
  - slot: motor, accepts Motor
- Motor`);
  const boxed=newGame(compound);boxed.tokens['name:Box'].slots=['name:Motor'];
  assert.equal(itemMotionDescription(compound,boxed,'name:Box'),'');
});

test('scene motion follows background inheritance and still/reset boundaries without exposing future scenes', () => {
  const initial=newGame(story);
  assert.deepEqual(story.chapters.map((_,chapter)=>sceneMotionDescription(story,atChapter(initial,chapter))),[
    'A curtain moves gently from side to side.','A curtain moves gently from side to side.','','','Unseen later scene motion.',
  ]);
  assert.doesNotMatch(board(story,atChapter(initial,2)),/Scene motion:/);
  const noPoster=parseStory('# No poster\n## One\nbackground animation: ![A curtain moves.](room.webp)');
  assert.equal(sceneMotionDescription(noPoster,newGame(noPoster)),'');
});

const creation = `# A working toy
## Make
background: ![room](room.svg)
reference: ![Cart](cart.svg)
**Goals**
- Finish -- Cart
**Items**
- Wood
- Wheels
- Cart
  - icon: ![cart](cart.svg)
  - animation: ![The wheels turn and the cart rolls forward.](cart.webp)

  ---
  {A wooden cart with four red wheels.}
  Ordinary encyclopedia explanation stays private.
**Combinations**
- Wood [transform] + Wheels [consume] -> Cart
## The gift
background: ![settled gift](gift.svg)
background animation: ![One figure hands the cart to another.](gift.webp)`;

test('creation observations survive final chapter completion in fast and detailed play without future prose', () => {
  const story=parseStory(creation);
  for(const playStyle of ['fast','detailed'] as const){
    const initial=startAdventure(story,{mode:'chapter',playStyle});
    const result=choose(story,initial,initial.frame.step,playStyle==='fast'?1:{combine:'Wood',with:'Wheels'});
    assert.equal(result.frame.phase,'complete');
    assert.equal(result.frame.messages.some(message=>message.kind==='board'),false);
    const text=renderFrame(result.frame);
    assert.match(text,/(?:Created|Transformed into): Cart\.\n  Picture: A wooden cart with four red wheels\.\n  Motion: The wheels turn and the cart rolls forward\./);
    assert(text.indexOf('Motion:')<text.indexOf('Goal completed:'));
    assert.doesNotMatch(text,/Ordinary encyclopedia|One figure hands/);
  }
  const initial=startAdventure(story,{playStyle:'fast'});
  const ending=choose(story,initial,initial.frame.step,1);
  assert.equal(ending.frame.phase,'complete');
  assert.match(renderFrame(ending.frame),/Scene motion: One figure hands the cart to another/);
  const history=renderFrame(startAdventure(story,{chapter:2,playStyle:'fast'}).frame);
  assert.match(history,/Step 1 combination:[\s\S]*Picture: A wooden cart[\s\S]*Motion: The wheels turn/);
  assert.doesNotMatch(history,/Ordinary encyclopedia/);
});

test('a newly created fixed object keeps its static picture observation without its suppressed item motion', () => {
  const fixed=parseStory(creation.replace('**Goals**','**Hotspots**\n- Cart\n  - icon: ![still cart](cart.svg)\n**Goals**'));
  const initial=startAdventure(fixed,{mode:'chapter',playStyle:'fast'}),result=choose(fixed,initial,initial.frame.step,1);
  const text=renderFrame(result.frame);
  assert.match(text,/Created: Cart\.\n  Picture: A wooden cart with four red wheels\./);
  assert.doesNotMatch(text,/Motion:/);
});

test('creation pictures use only currently applicable readings and never reveal an unfitted configuration', () => {
  const source=creation.replace('- Cart\n','- Cart (compound)\n  - slot: ribbon, accepts Ribbon, icon: ![ribbon](ribbon.svg)\n')
    .replace('**Combinations**','- Ribbon\n  - icon: ![ribbon](ribbon.svg)\n- Cart[Ribbon]\n\n  [Ribbon] {An unseen gold ribbon wraps the axle.}\n\n**Combinations**');
  const story=parseStory(source),initial=startAdventure(story,{mode:'chapter',playStyle:'fast'});
  const choice=initial.frame.options.find(option=>option.text==='Wood + Wheels')!.choice;
  const result=choose(story,initial,initial.frame.step,choice);
  const text=renderFrame(result.frame);
  assert.match(text,/Picture: A wooden cart with four red wheels/);
  assert.match(text,/Motion: The wheels turn and the cart rolls forward/);
  assert.doesNotMatch(text,/unseen gold ribbon|Ordinary encyclopedia/);
});
