import {resolveName} from '../playtest/commands.ts';
import type {NamedObject} from '../playtest/commands.ts';

type Verb='Inspect'|'Combine';
export interface NameRange {start:number;end:number}
interface NameContext {
  kind:'name';base:string;prefix:string;first:boolean;matches:NamedObject[];ranges:NameRange[];
}
type Context=NameContext|{kind:'verb';prefix:string;word:Verb}|{kind:'with';base:string;prefix:string;ranges:NameRange[]};
const fold=(text:string)=>text.toLocaleLowerCase('en');
const normalized=(text:string)=>fold(text.trim().replace(/\s+/g,' '));
const aliases=(object:NamedObject)=>[object.name,object.name.replace(/\[.*\]$/,'')];
function exact(text:string,objects:NamedObject[]):NamedObject|undefined {
  const matches=objects.filter(object=>aliases(object).some(name=>normalized(name)===normalized(text)));
  return matches.length===1 ? matches[0] : undefined;
}
function candidates(prefix:string,objects:NamedObject[]) {
  if (prefix.trimStart().startsWith('"')) {
    try {const object=exact(JSON.parse(prefix) as string,objects);return object ? [object] : [];}
    catch {return [];}
  }
  const query=normalized(prefix);
  return objects.filter(object=>normalized(object.name).startsWith(query) || aliases(object).some(name=>normalized(name)===query));
}
function commonPrefix(names:string[]):string {
  let prefix=names[0] ?? '';
  for (const name of names.slice(1)) {
    let length=0;
    while (length<prefix.length && fold(prefix[length])===fold(name[length] ?? '')) length++;
    prefix=prefix.slice(0,length);
  }
  return prefix;
}
function nameContext(base:string,prefix:string,first:boolean,objects:NamedObject[],ranges:NameRange[]=[]):NameContext {
  return {kind:'name',base,prefix,first,matches:candidates(prefix,objects),ranges};
}
function resolve(text:string,objects:NamedObject[]) {
  try {return resolveName(text.startsWith('"') ? JSON.parse(text) as string : text,objects);}
  catch {return undefined;}
}

/** Infer the current command atom from accepted text, never from suggested text. */
function context(text:string,objects:NamedObject[]):Context|undefined {
  if (!text) return;
  const command=/^(inspect|combine|i|c)\s+/i.exec(text);
  if (!command) {
    const word=(['Inspect','Combine'] as const).find(verb=>fold(verb).startsWith(fold(text)));
    return word ? {kind:'verb',prefix:text,word} : undefined;
  }
  const base=command[0], rest=text.slice(base.length);
  if (/^(inspect|i)$/i.test(command[1])) return nameContext(base,rest,false,objects);
  // A still-possible longer name wins over interpreting part of it as "with".
  if (candidates(rest,objects).length) return nameContext(base,rest,true,objects);
  const split=/^("(?:[^"\\]|\\.)*"|.+?)\s+(w(?:i(?:t(?:h)?)?)?)(?:\s+(.*))?$/i.exec(rest);
  if (!split || !resolve(split[1],objects)) return nameContext(base,rest,true,objects);
  const ranges=[{start:base.length,end:base.length+split[1].length}];
  if (fold(split[2])==='with' && split[3] !== undefined) {
    const second=split[3];return nameContext(text.slice(0,text.length-second.length),second,false,objects,ranges);
  }
  if (split[3] !== undefined) return;
  return {kind:'with',base:text.slice(0,text.length-split[2].length),prefix:split[2],ranges};
}

function spelling(name:string,objects:NamedObject[],first:boolean):string {
  // Preserve the CLI's quoting convention only where the command would otherwise
  // be ambiguous, including an item whose longer sibling contains the separator.
  const ambiguous=first && objects.some(object=>fold(object.name).startsWith(fold(name)+' with'));
  return /"|\bwith\b/i.test(name) || ambiguous ? JSON.stringify(name) : name;
}
function finishName(current:NameContext,object:NamedObject,objects:NamedObject[]):string {
  return current.base+spelling(object.name,objects,current.first)+(current.first ? ' with ' : '');
}
function suggestedName(current:NameContext):string {
  if (!current.prefix || !current.matches.length) return '';
  return commonPrefix(current.matches.map(object=>object.name));
}

/** Only actual names already present in the input receive item coloring. */
export function commandNames(text:string,objects:NamedObject[]):NameRange[] {
  const current=context(text,objects);
  if (!current || current.kind==='verb') return [];
  if (current.kind==='with') return current.ranges;
  let name=current.prefix.trim();
  if (name.startsWith('"')) {try {name=JSON.parse(name) as string;} catch {return current.ranges;}}
  return [...current.ranges,...(exact(name,current.matches)
    ? [{start:current.base.length,end:current.base.length+current.prefix.trimEnd().length}] : [])];
}

interface CompletionTrack {
  start:number;end:number;word:string;cursor:number;positions:number[];
}
export interface CommandState {
  text:string;completions:CompletionTrack[];overtype?:number;activeCompletion?:number;
}
interface Expansion {text:string;completions:CompletionTrack[]}
export function commandState(text=''):CommandState {return {text,completions:[]};}

/** Remember which letters a shortcut supplied. Quoting stays presentation/parser
 * syntax; fallback overtyping consumes the actual name, including literal quotes. */
function track(word:string,start:number,rendered:string,typed:string):CompletionTrack {
  if (typed.startsWith('"')) {try {typed=JSON.parse(typed) as string;} catch { /* Still editable raw text. */ }}
  const quoted=rendered.startsWith('"'), positions:number[]=[];
  let offset=start+(quoted ? 1 : 0);
  for (const character of word) {
    for (let i=0;i<character.length;i++) positions.push(offset);
    offset+=quoted ? JSON.stringify(character).slice(1,-1).length : character.length;
  }
  return {start,end:start+rendered.length,word,cursor:Math.min(typed.trimEnd().length,word.length),positions};
}
function expand(text:string,objects:NamedObject[]):Expansion|undefined {
  const current=context(text,objects);
  if (!current) return;
  if (current.kind==='verb') return {text:current.word+' ',completions:[track(current.word,0,current.word,current.prefix)]};
  if (current.kind==='with') return {text:current.base+'with ',completions:[track('with',current.base.length,'with',current.prefix)]};
  if (!current.prefix.trim() || !current.matches.length) return;
  if (current.matches.length===1) {
    const object=current.matches[0], name=spelling(object.name,objects,current.first);
    const completions=[track(object.name,current.base.length,name,current.prefix)];
    if (current.first) completions.push(track('with',current.base.length+name.length+1,'with',''));
    return {text:finishName(current,object,objects),completions};
  }
  const common=suggestedName(current);
  const boundary=/\s$/.test(current.prefix) && !/\s$/.test(common) ? ' ' : '';
  return {text:current.base+common+boundary,completions:[track(common,current.base.length,common,current.prefix)]};
}
function commitFirst(current:NameContext,object:NamedObject,objects:NamedObject[],withTyped=''):Expansion {
  const name=spelling(object.name,objects,true);
  // Accepting a boundary doesn't pretend the automatically inserted name was typed.
  const completions=current.prefix.trimEnd()===name ? [] : [track(object.name,current.base.length,name,current.prefix)];
  completions.push(track('with',current.base.length+name.length+1,'with',withTyped));
  return {text:current.base+name+' with ',completions};
}

/** Forward progress always wins. Return nothing when this key cannot contribute
 * to the current/next atom, so the caller can try an earlier completion instead. */
function forward(text:string,key:string,objects:NamedObject[]):Expansion|undefined {
  const current=context(text,objects), separator=key===' ' || key==='Tab';
  if (!current) return separator ? undefined : expand(text+key,objects);
  if (current.kind==='verb' || current.kind==='with') {
    const completed=expand(text,objects)!;
    if (separator) return completed;
    const next=forward(completed.text,key,objects);
    if (next) return {text:next.text,completions:[...completed.completions,...next.completions]};
    const word=current.kind==='verb' ? current.word : 'with';
    return fold(word).startsWith(fold(current.prefix+key)) ? expand(text+key,objects) : undefined;
  }
  if (!current.prefix.trim()) {
    if (separator) return {text,completions:[]};
    return candidates(key,objects).length ? expand(text+key,objects) : undefined;
  }
  if (!current.matches.length) return;
  const chosen=exact(current.prefix,current.matches), unique=current.matches.length===1 ? current.matches[0] : undefined;
  if (separator) {
    const object=unique ?? (/\s$/.test(current.prefix) ? chosen : undefined);
    if (object) return current.first ? commitFirst(current,object,objects)
      : {text:finishName(current,object,objects),completions:[]};
    const common=suggestedName(current), boundary=current.base+common+(/\s$/.test(common) ? '' : ' ');
    if (boundary.startsWith(text)) return {text:boundary,completions:[]};
    const completed=expand(text,objects)!;return {...completed,text:boundary};
  }
  const common=suggestedName(current);
  for (const extension of [current.prefix+key,common+key,common.trimEnd()+' '+key]) {
    if (current.matches.some(object=>fold(object.name).startsWith(fold(extension)))) return expand(current.base+extension,objects);
  }
  const object=chosen ?? unique;
  if (object && current.first) {
    if (fold(key)==='w') return commitFirst(current,object,objects,'w');
    const committed=commitFirst(current,object,objects), next=forward(committed.text,key,objects);
    if (next) return {text:next.text,completions:[...committed.completions,...next.completions]};
  }
}

export function typeCommand(state:CommandState,key:string,objects:NamedObject[]):CommandState|undefined {
  const next=forward(state.text,key,objects);
  let advanced:CommandState|undefined;
  if (next) {
    const retained=state.completions.filter(previous=>
      state.text.slice(previous.start,previous.end)===next.text.slice(previous.start,previous.end) &&
      !next.completions.some(added=>added.start===previous.start && added.end===previous.end && added.word===previous.word));
    advanced={text:next.text,completions:[...retained,...next.completions]};
    if (key!==' ' || next.text!==state.text) return advanced;
  }
  if (key==='Tab') return advanced;
  const order=state.completions.map((_,index)=>index).reverse();
  if (state.activeCompletion!==undefined) {
    const index=order.indexOf(state.activeCompletion);if(index>=0) order.splice(index,1);
    order.unshift(state.activeCompletion);
  }
  for (const index of order) {
    const previous=state.completions[index];
    if (!previous || previous.cursor>=previous.word.length ||
      fold(previous.word.slice(previous.cursor,previous.cursor+key.length))!==fold(key)) continue;
    const updated={...previous,cursor:previous.cursor+key.length};
    const completions=state.completions.map((entry,i)=>i===index ? updated : entry);
    const position=updated.positions[Math.min(updated.cursor,updated.positions.length-1)];
    return {text:state.text,completions,overtype:position,activeCompletion:index};
  }
  return advanced;
}

/** At the end of a command, remove one grammatical atom. Names step back through
 * their shared-prefix branches, independently of completion or overtyping history. */
export function backspaceCommand(state:CommandState,objects:NamedObject[]):CommandState|undefined {
  const current=context(state.text.trimEnd(),objects);
  if (!current) return;
  let text:string;
  if (current.kind==='verb') text='';
  else if (current.kind==='with') text=current.base;
  else {
    // Unrecognized text stays ordinary editable input.
    if (!current.matches.length) return;
    let name=current.prefix;
    if (name.startsWith('"')) {
      try {name=JSON.parse(name) as string;} catch {return;}
    }
    let branch='';
    for (const object of objects) {
      const shared=commonPrefix([name,object.name]);
      if (shared.length<name.length && shared.length>branch.length) branch=shared;
    }
    text=current.base+branch;
  }
  return {text,completions:state.completions.filter(previous=>previous.end<=text.length &&
    state.text.slice(previous.start,previous.end)===text.slice(previous.start,previous.end))};
}

/** Enter accepts a complete/exact name, while the existing parser still validates
 * the complete command and the existing runner resolves the chosen objects. */
export function submissionText(text:string,objects:NamedObject[]):string {
  const current=context(text,objects);
  if (current?.kind!=='name') return text;
  const object=exact(current.prefix,current.matches) ?? (current.prefix.trim() && current.matches.length===1 ? current.matches[0] : undefined);
  return object ? finishName(current,object,objects) : text;
}
