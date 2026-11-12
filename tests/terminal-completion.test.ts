import {test} from 'node:test';
import assert from 'node:assert/strict';
import {parseCommand,resolveName} from '../src/playtest/commands.ts';
import type {NamedObject} from '../src/playtest/commands.ts';
import {backspaceCommand,commandNames,commandState,typeCommand,submissionText} from '../src/web/terminal-completion.ts';
import type {CommandState} from '../src/web/terminal-completion.ts';

const objects=(...names:string[]):NamedObject[]=>names.map((name,id)=>({id:String(id),name,kind:'item'}));
const elements=objects('Earth','Air','Fire','Water');
const type=(state:CommandState,key:string,names=elements)=>
  typeCommand(state,key,names) ?? commandState(state.text+(key==='Tab' ? '' : key));
function write(keys:string,names=elements,state=commandState()) {
  for (const key of keys) state=type(state,key,names);
  return state;
}

test('verbs and unique names complete immediately, including the first operand connector',()=>{
  const verb=write('c');
  assert.equal(verb.text,'Combine ');
  const first=type(verb,'e');
  assert.equal(first.text,'Combine Earth with ');
  assert.equal(first.overtype,undefined);
  assert.equal(type(first,'Tab').text,first.text);
  assert.equal(type(first,' ').text,first.text);
  const second=type(first,'f');
  assert.equal(second.text,'Combine Earth with Fire');
  assert.deepEqual(parseCommand(submissionText(second.text,elements)),{combine:'Earth',with:'Fire'});
  assert.deepEqual(commandNames(second.text,elements).map(range=>second.text.slice(range.start,range.end)),['Earth','Fire']);
});

test('forward progress wins over matching letters in earlier completions',()=>{
  const first=write('cw');
  assert.equal(first.text,'Combine Water with ');
  const second=type(first,'a');
  assert.equal(second.text,'Combine Water with Air');
  assert.equal(second.overtype,undefined);
  // Even after fallback has started, a valid next operand wins.
  const fallback=type(first,'o');
  assert.equal(fallback.text,first.text);
  assert.notEqual(fallback.overtype,undefined);
  assert.equal(type(fallback,'f').text,'Combine Water with Fire');
  assert.equal(type(fallback,'f').overtype,undefined);
});

test('otherwise letters consume earlier completion text without changing the command',()=>{
  let state=write('iw');
  assert.equal(state.text,'Inspect Water');
  assert.equal(state.overtype,undefined);
  state=type(state,'a');
  assert.equal(state.text,'Inspect Water');
  assert.equal(state.overtype,'Inspect Wa'.length);
  for (const letter of 'ter') {
    state=type(state,letter);
    assert.equal(state.text,'Inspect Water');
    assert.notEqual(state.overtype,undefined);
  }
  assert.equal(typeCommand(state,'z',elements),undefined);
  const verb=write('co');
  assert.equal(verb.text,'Combine ');
  assert.equal(verb.overtype,2);
});

test('a shorter name and a longer sibling remain selectable at their shared boundary',()=>{
  const names=objects('Plant','Plant Fiber','Fire');
  const prefix=write('cp',names);
  assert.equal(prefix.text,'Combine Plant');
  assert.deepEqual(commandNames(prefix.text,names),[{start:8,end:13}]);
  const fallback=type(prefix,'l',names);
  assert.equal(fallback.text,prefix.text);
  assert.notEqual(fallback.overtype,undefined);
  const boundary=type(prefix,' ',names);
  assert.equal(boundary.text,'Combine Plant ');
  assert.equal(type(boundary,'f',names).text,'Combine Plant Fiber with ');
  assert.equal(type(boundary,'w',names).text,'Combine Plant with ');
  assert.equal(type(boundary,' ',names).text,'Combine Plant with ');
  assert.equal(type(boundary,'Tab',names).text,'Combine Plant with ');
  assert.equal(submissionText('Inspect Plant',names),'Inspect Plant');
});

test('an incomplete common prefix cannot be accepted as an item',()=>{
  const names=objects('Plant Alpha','Plant Beta');
  const prefix=write('cp',names);
  assert.equal(prefix.text,'Combine Plant ');
  assert.deepEqual(commandNames(prefix.text,names),[]);
  assert.equal(type(prefix,' ',names).text,prefix.text);
  assert.equal(type(prefix,'Tab',names).text,prefix.text);
  assert.equal(type(prefix,'b',names).text,'Combine Plant Beta with ');
  assert.equal(submissionText('Inspect Plant',names),'Inspect Plant');
  assert.throws(()=>resolveName('Plant',names),/Ambiguous/);
});

test('fallback remembers an earlier shared prefix after a later letter disambiguates it',()=>{
  const names=objects('Sheet','Shelf');
  let state=write('ish',names);
  assert.equal(state.text,'Inspect She');
  assert.notEqual(state.overtype,undefined);
  state=type(state,'e',names);
  assert.equal(state.text,'Inspect Sheet');
  assert.equal(state.overtype,undefined);
  for (const letter of 'et') {
    state=type(state,letter,names);
    assert.equal(state.text,'Inspect Sheet');
    assert.notEqual(state.overtype,undefined);
  }
});

test('explicit editing discards previous completion tracking and can resume forward completion',()=>{
  const original=write('iw');
  const edited=commandState(original.text);
  assert.equal(typeCommand(edited,'a',elements),undefined);
  assert.equal(edited.overtype,undefined);
  assert.equal(type(commandState('Inspect W'),'a').text,'Inspect Water');
  assert.equal(type(commandState('Combine '),'e').text,'Combine Earth with ');
});

test('completed names keep the existing parser safe when names contain with or quotes',()=>{
  const names=objects('Faith with Works','A "quoted" name','Water');
  const first=write('cf',names);
  assert.equal(first.text,'Combine "Faith with Works" with ');
  const command=type(first,'w',names);
  assert.deepEqual(parseCommand(submissionText(command.text,names)),{combine:'Faith with Works',with:'Water'});
  const quoted=write('ia',names);
  assert.deepEqual(parseCommand(submissionText(quoted.text,names)),{inspect:'A "quoted" name'});
});

test('Backspace removes each operand and keyword separately, including an automatic with',()=>{
  let state=write('cef');
  assert.equal(state.text,'Combine Earth with Fire');
  for (const expected of ['Combine Earth with ','Combine Earth ','Combine ','']) {
    state=backspaceCommand(state,elements)!;
    assert.equal(state.text,expected);
    assert.equal(state.overtype,undefined);
  }
  const withoutWith=backspaceCommand(write('ce'),elements)!;
  assert.equal(withoutWith.text,'Combine Earth ');
  assert.equal(type(withoutWith,'f').text,'Combine Earth with Fire');
  assert.equal(backspaceCommand(write('iwa'),elements)!.text,'Inspect ');
  assert.equal(backspaceCommand(commandState('Inspect Unknown'),elements),undefined);
});

test('Backspace retreats through shared name branches before removing the whole name',()=>{
  const names=objects('Plant Alpha One','Plant Alpha Two','Plant Beta','Fire');
  let state=commandState('Combine Plant Alpha One with Fire');
  for (const expected of ['Combine Plant Alpha One with ','Combine Plant Alpha One ',
    'Combine Plant Alpha ','Combine Plant ','Combine ','']) {
    state=backspaceCommand(state,names)!;
    assert.equal(state.text,expected);
  }
  const shorter=objects('Plant','Plant Fiber','Fire');
  const prefix=backspaceCommand(commandState('Inspect Plant Fiber'),shorter)!;
  assert.equal(prefix.text,'Inspect Plant');
  assert.equal(backspaceCommand(prefix,shorter)!.text,'Inspect ');
  assert.equal(type(prefix,'f',shorter).text,'Inspect Plant Fiber');
});

test('Backspace treats a multiword or quoted name as one part',()=>{
  const names=objects('Faith with Works','A "quoted" name','Water');
  let state=write('cfw',names);
  for (const expected of ['Combine "Faith with Works" with ','Combine "Faith with Works" ','Combine ']) {
    state=backspaceCommand(state,names)!;
    assert.equal(state.text,expected);
  }
  assert.equal(backspaceCommand(write('ia',names),names)!.text,'Inspect ');
});
