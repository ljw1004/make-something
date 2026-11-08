import {test} from 'node:test';
import assert from 'node:assert/strict';
import {parseStory} from '../src/story/parser.ts';
import {availableTokens,replay} from '../src/engine/game.ts';
import {choose,startAdventure,renderFrame} from '../src/playtest/adventure.ts';
import {detailedObjects} from '../src/playtest/detailed.ts';
import {parseCommand,resolveName} from '../src/playtest/commands.ts';
import {completeCommandLine} from '../src/playtest/terminal-input.ts';
import {submitReply,verifyChapterSession,playerRequest} from '../src/playtest/chapter-session.ts';
import type {ChapterSession} from '../src/playtest/chapter-session.ts';
import type {DetailedChoice} from '../src/playtest/commands.ts';
import {rubric} from '../src/playtest/rubrics.ts';
import {digest} from '../src/playtest/session.ts';
import {graderPacket,validateGrade} from '../src/playtest/grading.ts';
import {workshop} from './fixtures/adventure.ts';

const station = parseStory(`# Station
## Work
**Goals**
- Finish -- Finished
**Hotspots**
- Warm hearth
**Items**
- Warm hearth
- Warm dough
- Cold water
- Starter
- Salt
- Finished
- Bread
- Salty bread
- Paste
**Combinations**
- Warm dough [transform] + Starter [preserve] @ Warm hearth -> Bread
- Warm dough [transform] + Salt [preserve] @ Warm hearth -> Salty bread
- Warm dough [transform] + Cold water [preserve] -> Paste
- Bread [transform] + Cold water [preserve] -> Finished
- Salty bread [transform] + Cold water [preserve] -> Finished
- Paste [transform] + Starter [preserve] -> Finished
`);
const start = (story=station) => startAdventure(story,{mode:'chapter',playStyle:'detailed'});
const result = (a:ReturnType<typeof start>) => a.frame.messages.map(m=>m.text).join('\n');
const redirected = "That can't be combined like that, but here's how it can:";

test('detailed hints reveal current partners without outputs or contextual third ingredients',()=>{
  const initial=start();assert.equal(initial.frame.options.length,0);
  assert.doesNotMatch(renderFrame(initial.frame),/\d+\. Warm dough|Salty bread|Can combine/);
  const inspected=choose(station,initial,1,{inspect:'Warm dough'});
  assert.equal(inspected.frame.step,2);assert.deepEqual(inspected.state,initial.state);
  assert.match(result(inspected),/Can combine with:\n- Warm hearth\n- Cold water/);
  assert.doesNotMatch(result(inspected),/Starter|Salt|Bread|Paste/);
  const hotspot=choose(station,initial,1,{inspect:'Warm hearth'});
  assert.match(result(hotspot),/- Warm dough\n- Starter\n- Salt/);
  assert.doesNotMatch(result(hotspot),/Cold water|Bread/);
  const failed=choose(station,initial,1,{combine:'Warm dough',with:'Salt'});
  assert.equal(failed.frame.step,2);assert.deepEqual(failed.state,initial.state);
  assert.equal(result(failed),`${redirected}\n${result(inspected)}`);
});

test('incompatible attempts stay with the first operand and automatically perform only one operation',()=>{
  const s=parseStory(workshop),initial=start(s);
  const unavailable=choose(s,initial,1,{combine:'Lid',with:'Sheet'});
  assert.equal(result(unavailable),'That cannot be combined with anything');
  assert.deepEqual(unavailable.state,initial.state);assert.equal(unavailable.frame.step,2);

  let a=initial;
  for (const [first,second,partner] of [['Sheet','Lid','Tool'],['Lid','Tool','Case[]'],['Case','Tool','Shelf']]) {
    const inspected=choose(s,a,a.frame.step,{inspect:first});
    const combined=choose(s,a,a.frame.step,{combine:first,with:second});
    assert.deepEqual(combined.state,inspected.state);
    assert.equal(result(combined),`${redirected}\n${result(inspected)}`);
    assert(result(combined).includes(`Combined: with ${partner}.`));
    assert.equal(combined.frame.step,a.frame.step+1);
    a=combined;
    if (first==='Sheet') {
      assert.deepEqual(a.state.tokens['name:Case'].slots,[]);
      assert.equal(a.frame.phase,'choose','creation must not automatically fit the lid');
    }
    if (first==='Lid') assert.equal(a.frame.phase,'choose','fitting must not automatically complete the placement goal');
  }
  assert.equal(a.frame.phase,'complete');assert.deepEqual(replay(s,a.state.actions),a.state);
});

test('one highlighted hotspot with multiple operations does not trigger an automatic alternative',()=>{
  const s=parseStory(`# Choices
## Work
**Goals**
- Finish -- C
**Hotspots**
- H
**Items**
- H
- A
- B
- D
- C
- E
**Combinations**
- A + B @ H -> C
- A + D @ H -> E
`);
  const initial=start(s),attempt=choose(s,initial,1,{combine:'A',with:'B'});
  assert.equal(result(attempt),`${redirected}\nCan combine with:\n- H`);
  assert.deepEqual(attempt.state,initial.state);assert.equal(attempt.frame.step,2);
});

test('a redirected contextual reaction reports its selected hotspot and actual third ingredient',()=>{
  const s=parseStory(`# Context
## Work
**Goals**
- Bake -- Bread
**Hotspots**
- Hearth
**Items**
- Hearth
- Dough
- Starter
- Bread
**Combinations**
- Dough [transform] + Starter [preserve] @ Hearth -> Bread
`);
  for (const [first,second] of [['Dough','Starter'],['Starter','Dough']]) {
    const initial=start(s),attempt=choose(s,initial,1,{combine:first,with:second});
    assert.equal(result(attempt),`${redirected}\n${result(choose(s,initial,1,{inspect:first}))}`);
    assert(result(attempt).includes(`Combined: with Hearth.\nCombined this together with: ${second}.`));
    assert.equal(attempt.frame.phase,'complete');assert.equal(attempt.frame.step,2);
    assert(availableTokens(attempt.state).every(t=>!t.hotspot));
    assert.deepEqual(replay(s,attempt.state.actions),attempt.state);
  }
});

test('either item–hotspot direction executes a complete reaction in manuscript order and clears occupancy',()=>{
  for (const command of [{combine:'Warm dough',with:'Warm hearth'},{combine:'Warm hearth',with:'Warm dough'}]) {
    const initial=start(),made=choose(station,initial,1,command);
    assert.match(result(made),/Combined this together with: Starter/);
    assert.match(result(made),/Transformed into: Bread/);
    assert.doesNotMatch(result(made),/Can combine with|That can't|Combined: with/);
    assert(!made.state.tokens['name:Salty bread']);
    assert(availableTokens(made.state).every(t=>!t.hotspot));
    assert.deepEqual(replay(station,made.state.actions),made.state);
    assert(made.state.actions.length>initial.state.actions.length+1,'automatic moves belong to one decision');
    assert.equal(made.frame.step,2);
  }
});

test('a sole inspection executes once, including contextual reactions, compounds and placement-only goals',()=>{
  const s=parseStory(workshop);let a=start(s);
  a=choose(s,a,1,{inspect:'Sheet'});assert.match(result(a),/Transformed into: Case\[\]/);
  a=choose(s,a,2,{inspect:'Lid'});assert.match(result(a),/Slotted in: Case\[Lid\]/);
  a=choose(s,a,3,{combine:'Shelf',with:'Case'});assert.match(result(a),/Placed: Case\[Lid\] at Shelf/);
  assert.equal(a.frame.phase,'complete');assert.equal(a.frame.step,4);
  assert(availableTokens(a.state).every(t=>!t.hotspot));assert.deepEqual(replay(s,a.state.actions),a.state);
  const contextual=choose(station,start(),1,{inspect:'Salt'});
  assert.match(result(contextual),/Combined this together with: Warm dough/);
  assert.match(result(contextual),/Transformed into: Salty bread/);
});

test('direct hotspot reactions take priority, report actual fates, and missing ingredients are not invented',()=>{
  const s=parseStory(`# Direct
## Work
**Goals**
- Finish -- End
**Hotspots**
- H
**Items**
- H
- A
- B
- Tool
- C
- D
- End
**Combinations**
- A [transform] + B [consume] @ H -> D
- A [transform] @ H -> C
- C [transform] + B [consume] -> End
- D [transform] + Tool [preserve] -> End
`);
  let a=choose(s,start(s),1,{combine:'H',with:'A'});
  assert.match(result(a),/Transformed into: C/);assert.doesNotMatch(result(a),/Combined this together/);
  a=choose(s,a,2,{combine:'C',with:'B'});
  assert.match(result(a),/Consumed: B\.\nTransformed into: End/);
  const missing=parseStory(`# Missing
## Work
**Goals**
- Finish -- C
**Hotspots**
- H
**Items**
- H
- A
- Tool
- B
- C
**Combinations**
- A + Tool -> B
- A + B @ H -> C
`);
  const attempt=choose(missing,start(missing),1,{combine:'A',with:'H'});
  assert(result(attempt).startsWith(redirected));assert(!attempt.state.tokens['name:C']);
  assert.match(result(attempt),/Combined: with Tool/);assert(attempt.state.tokens['name:B']);
  assert(availableTokens(attempt.state).every(t=>!t.hotspot));
});

test('joint placement goals can complete without leaving station occupancy between commands',()=>{
  const s=parseStory(`# Place
## Work
**Goals**
- Put both away
  - both: A @ H
  - and: B @ J
**Hotspots**
- H
- J
**Items**
- H
- J
- A
- B
`);
  const a=choose(s,start(s),1,{combine:'A',with:'H'});
  assert.equal(a.frame.phase,'complete');assert.match(result(a),/Placed: B at J/);
  assert(availableTokens(a.state).every(t=>!t.hotspot));assert.deepEqual(replay(s,a.state.actions),a.state);
});

test('name resolution uses full-word prefixes across objects and hotspots, and terminal completion is textual',()=>{
  const objects=detailedObjects(station,start().state);
  assert.equal(resolveName('Cold',objects).name,'Cold water');
  assert.throws(()=>resolveName('Col',objects),/No available/);
  assert.throws(()=>resolveName('Warm',objects),/Ambiguous.*Warm dough.*Warm hearth/);
  assert.equal(completeCommandLine('i',objects),'inspect ');
  assert.equal(completeCommandLine('c',objects),'combine ');
  assert.equal(completeCommandLine('combine W',objects),'combine W');
  assert.equal(completeCommandLine('combine Cold',objects),'combine "Cold water" with ');
  assert.equal(completeCommandLine('combine "Cold water" with Sa',objects),'combine "Cold water" with "Salt"');
  assert.equal(completeCommandLine('inspect Sta',objects),'inspect "Starter"');
  assert.deepEqual(parseCommand('c "Warm dough" with "Warm hearth"'),{combine:'Warm dough',with:'Warm hearth'});
  assert.deepEqual(parseCommand('inspect Cold water'),{inspect:'Cold water'});
  assert.deepEqual(parseCommand('combine "Thing with a name" with "A \\"quote\\""'),{combine:'Thing with a name',with:'A "quote"'});
  assert.deepEqual(parseCommand(''),{look:true});assert.throws(()=>parseCommand('combine A'),/Use inspect/);
});

const twoBearings = `# Two bearings
## Work
**Goals**
- Fit both bearing tubes -- \`finished\`
**Items**
- \`chassis\` Chassis
- \`front\` Bearing tube
- \`rear\` Bearing tube
- \`front-fitted\` Chassis
- \`rear-fitted\` Chassis
- \`finished\` Racer
**Combinations**
- \`front\` [consume] + \`chassis\` [transform] -> \`front-fitted\`
- \`rear\` [consume] + \`chassis\` [transform] -> \`rear-fitted\`
- \`rear\` [consume] + \`front-fitted\` [transform] -> \`finished\`
- \`front\` [consume] + \`rear-fitted\` [transform] -> \`finished\`
`;

test('identical copies have selectable text handles and either one can be fitted first',()=>{
  const s=parseStory(twoBearings);
  for(const firstNumber of [1,2]){
    const initial=start(s),objects=detailedObjects(s,initial.state),frame=renderFrame(initial.frame);
    assert.match(frame,/Items:\n[\s\S]*- Bearing tube \(#1\)\n- Bearing tube \(#2\)/);
    assert.throws(()=>choose(s,initial,1,{inspect:'Bearing tube'}),/Ambiguous.*Bearing tube \(#1\).*Bearing tube \(#2\)/);
    assert.equal(completeCommandLine('inspect Bearing tube (#',objects),'inspect Bearing tube (#');
    assert.equal(completeCommandLine(`inspect Bearing tube (#${firstNumber}`,objects),`inspect "Bearing tube (#${firstNumber})"`);
    const selected=resolveName(`Bearing tube (#${firstNumber})`,objects).id;
    let a=choose(s,initial,1,{inspect:'Chassis'});
    assert.equal(result(a),'Can combine with:\n- Bearing tube (#1)\n- Bearing tube (#2)');
    a=choose(s,a,2,{combine:`Bearing tube (#${firstNumber})`,with:'Chassis'});
    assert.equal(a.state.tokens[selected].status,'consume');
    assert.match(result(a),new RegExp(`Consumed: Bearing tube \\(#${firstNumber}\\)\\.`));
    assert.match(result(a),/Transformed into: Chassis\./,'a replacement is not presented as another simultaneous copy');
    const remainingNumber=3-firstNumber,remaining=detailedObjects(s,a.state).find(o=>o.name==='Bearing tube')!;
    assert(remaining);
    assert.equal(resolveName(`Bearing tube (#${remainingNumber})`,detailedObjects(s,a.state)).id,remaining.id,'the previously shown handle stays valid');
    const looked=choose(s,a,3,{look:true});
    assert.match(result(looked),/- Bearing tube(?:\n|$)/);
    a=choose(s,looked,3,{inspect:`Bearing tube (#${remainingNumber})`});
    assert.equal(a.frame.phase,'complete');
    assert.equal(a.state.tokens[remaining.id].status,'consume');
    assert.deepEqual(replay(s,a.state.actions),a.state);
  }
  const fast=startAdventure(s,{mode:'chapter',playStyle:'fast'});
  assert.deepEqual(fast.frame.options.map(o=>o.text),['Bearing tube (#1) + Chassis','Bearing tube (#2) + Chassis']);
});

test('copy handles cover hotspots, avoid literal numbered names, and reveal no future copies',()=>{
  const s=parseStory(`# Stations
## First
**Goals**
- Make A -- A
**Hotspots**
- \`one\`
- \`two\`
**Items**
- \`one\` Bench
- \`two\` Bench
- \`literal\` Bench (1)
- Paper
- A
- B
**Combinations**
- Paper [transform] @ \`one\` -> A
- Paper [transform] @ \`two\` -> B
## Later
**Goals**
- Finish -- Done
**Items**
- \`future\` Bench
- Done
**Combinations**
- A [transform] + \`future\` [preserve] -> Done
`);
  const initial=start(s),objects=detailedObjects(s,initial.state);
  assert.equal(resolveName('Bench (1)',objects).id,'id:literal');
  assert.equal(resolveName('Bench (#1)',objects).kind,'hotspot');
  assert.equal(resolveName('Bench (#2)',objects).kind,'hotspot');
  assert.throws(()=>resolveName('Bench (#3)',objects),/No available/);
  assert.doesNotMatch(renderFrame(initial.frame),/#3|future/);
  const inspected=choose(s,initial,1,{inspect:'Paper'});
  assert.match(result(inspected),/Can combine with:\n- Bench \(#1\)\n- Bench \(#2\)/);
  const target=objects.find(o=>o.id==='id:one')!;
  const made=choose(s,inspected,2,{combine:'Paper',with:target.name});
  assert.equal(made.frame.phase,'complete');
  assert.equal(s.items['id:one'].name,'Bench','the story/browser label is unchanged');
});

test('a later literal selector cannot steal a prior handle, including after that copy retires',()=>{
  const s=parseStory(`# Literal selectors
## Work
**Goals**
- Finish -- Done
**Items**
- \`one\` Tube
- \`two\` Tube
- Sheet
- Stamp
- \`later\` Tube (#1)
- Done
**Combinations**
- Sheet [transform] + Stamp [preserve] -> \`later\`
- \`one\` [consume] + \`later\` [preserve] -> Done
`);
  let a=start(s);
  assert.match(renderFrame(a.frame),/- Tube \(#1\)\n- Tube \(#2\)/);
  assert.doesNotMatch(renderFrame(a.frame),/Tube \(#1\) \(#1\)/,'no future literal is exposed');
  a=choose(s,a,1,{combine:'Sheet',with:'Stamp'});
  const objects=detailedObjects(s,a.state);
  assert.equal(resolveName('Tube (#1)',objects).id,'id:one');
  assert.equal(resolveName('Tube (#1) (#1)',objects).id,'id:later');
  assert.match(result(a),/Transformed into: Tube \(#1\) \(#1\)\./);
  a=choose(s,a,2,{combine:'Tube (#1)',with:'Tube (#1) (#1)'});
  assert.equal(a.frame.phase,'complete');
  assert.throws(()=>resolveName('Tube (#1)',detailedObjects(s,a.state)),/No available/,'a retired exact handle cannot become a prefix for a new literal');
  assert.equal(resolveName('Tube (#1) (#1)',detailedObjects(s,a.state)).id,'id:later');
});

function session(story=station):ChapterSession {
  const adventure=start(story);
  return {version:6,playStyle:'detailed',guidance:'',guidanceHash:digest(''),id:'fixture',story:'station',storyHash:'',runtimeHash:'',createdAt:'',chapter:1,playerRubric:rubric('player','detailed'),graderRubric:rubric('grader','detailed'),initial:adventure.frame,adventure,turns:[],pendingLook:false,requests:[]};
}
function reply(s:ChapterSession,choice:DetailedChoice) {
  return {...(s.turns.length ? {effect:'Fixture observation.',reaction:'Nothing notable.'} : {}),step:s.adventure.frame.step,choice,reason:'Fixture decision.',expectation:'Fixture expectation.',alternatives:[]};
}

test('copy selection survives saved-session replay and completed-chapter history',()=>{
  const story=parseStory(twoBearings+`## Launch
**Goals**
- Launch -- Launched
**Items**
- Ramp
- Launched
**Combinations**
- Racer [transform] + Ramp [preserve] -> Launched
`),s=session(story);
  submitReply(s,story,reply(s,{combine:'Bearing tube (#2)',with:'Chassis'}));
  submitReply(s,story,{step:2,choice:{look:true}});
  submitReply(s,story,reply(s,{combine:'Bearing tube (#1)',with:'Chassis'}));
  assert(verifyChapterSession(s,story));
  const history=renderFrame(startAdventure(story,{chapter:2,mode:'chapter',playStyle:'detailed'}).frame);
  assert.match(history,/Step 1 combination: Bearing tube \(#1\) \+ Chassis -> Chassis/);
  assert.match(history,/Step 2 combination: Bearing tube \+ Chassis -> Racer/);
});

test('detailed sessions count inspections and failed attempts, exclude errors and looks, and verify public and engine replay',()=>{
  const s=session(),before=JSON.stringify(s);
  for (const choice of [{inspect:'Warm'},{inspect:'Missing'},{combine:'Cold',with:'Warm'}]) {
    assert.throws(()=>submitReply(s,station,reply(s,choice)),/Ambiguous|No available/);assert.equal(JSON.stringify(s),before);
  }
  submitReply(s,station,reply(s,{inspect:'Warm dough'}));
  const looked=submitReply(s,station,{step:2,choice:{look:true}});assert.deepEqual(looked,{step:2,choice:{look:true}});
  assert.equal(s.turns.length,1);assert(playerRequest(s).previousResult);
  submitReply(s,station,reply(s,{combine:'Warm dough',with:'Salt'}));
  submitReply(s,station,reply(s,{combine:'Warm hearth',with:'Warm dough'}));
  submitReply(s,station,reply(s,{combine:'Bread',with:'Cold'}));
  assert.equal(s.turns.length,4);assert.deepEqual(s.turns.map(t=>t.lookedAgain),[false,true,false,false]);
  assert(verifyChapterSession(s,station));assert.equal(graderPacket(s).verification.decisions,4);
  const grade={verdict:'Fixture',decisions:s.turns.map(t=>({step:t.reply.step,meaningful:false,reason:'Fixture'})),fun:{meaningful:0,total:4,ratio:0,explanation:'Fixture'},hook:{score:null,reason:'No report',steps:[]},strongest:{text:'Fixture',steps:[]},weakest:{text:'Fixture',steps:[]},limits:'Fixture'};
  assert.equal(validateGrade(grade,s).fun.total,4);
  const damaged=structuredClone(s);damaged.turns[0].result.messages[0].text='Invented hint';
  assert.throws(()=>verifyChapterSession(damaged,station),/does not match replay/);
});

test('detailed sessions preserve redirected intentions, distinguish operand order and reject name errors before acting',()=>{
  const s=session(),before=JSON.stringify(s);
  for (const withName of ['Warm','Missing']) {
    assert.throws(()=>submitReply(s,station,reply(s,{combine:'Salt',with:withName})),/Ambiguous|No available/);
    assert.equal(JSON.stringify(s),before);
  }
  const compatible=reply(s,{combine:'Warm dough',with:'Cold water'});
  assert.throws(()=>submitReply(s,station,{...compatible,alternatives:[{choice:{combine:'Cold',with:'Warm dough'},reason:'Same valid pair.'}]}),/distinct other choices/);
  const choice={combine:'Salt',with:'Warm dough'},decision={...reply(s,choice),alternatives:[{choice:{combine:'Warm dough',with:'Salt'},reason:'Pick up the dough instead.'}]};
  submitReply(s,station,decision);
  assert.equal(s.turns.length,1);assert.equal(s.adventure.frame.step,2);
  assert.deepEqual(s.turns[0].reply,decision);
  assert.match(result(s.adventure),/Combined: with Warm hearth/);
  assert.match(result(s.adventure),/Transformed into: Salty bread/);
  assert(!s.adventure.state.tokens['name:Finished'],'the new result must wait for another decision');
  submitReply(s,station,reply(s,{combine:'Salty bread',with:'Cold'}));
  assert(verifyChapterSession(s,station));assert.equal(graderPacket(s).verification.decisions,2);
});
