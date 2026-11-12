import type {NamedObject} from '../playtest/commands.ts';
import {backspaceCommand,commandNames,commandState,submissionText,typeCommand} from './terminal-completion.ts';
import type {CommandState} from './terminal-completion.ts';

/** Keep a real input for selection, clipboard and accessibility. Completion advances
 * its insertion point; a separate underline appears only during fallback overtyping. */
export function terminalCommandInput(input:HTMLInputElement,getObjects:()=>NamedObject[]|undefined) {
  const host=document.createElement('span');host.className='command-entry';
  input.before(host);host.append(input);
  const display=document.createElement('span');display.className='command-rendered';display.setAttribute('aria-hidden','true');
  const line=document.createElement('span');line.className='command-line';display.append(line);host.append(display);
  let composing=false, state=commandState(input.value);
  function refresh() {
    const objects=getObjects(), start=input.selectionStart ?? input.value.length, end=input.selectionEnd ?? start;
    if (state.text!==input.value || start!==end || end!==input.value.length) state=commandState(input.value);
    const names=objects && !composing ? commandNames(input.value,objects) : [];
    const text=input.value;
    const fragment=document.createDocumentFragment();let position=0;
    for (const character of text+' ') {
      const span=document.createElement('span');span.textContent=character;
      if (names.some(range=>position>=range.start && position<range.end)) span.classList.add('command-item');
      if (position===state.overtype) span.classList.add('command-overtype');
      if (start!==end && position>=start && position<end) span.classList.add('command-selection');
      if (start===end && position===start) span.classList.add('command-cursor');
      fragment.append(span);position+=character.length;
    }
    line.replaceChildren(fragment);line.style.transform=`translateX(${-input.scrollLeft}px)`;
    input.setAttribute('aria-autocomplete',objects ? 'inline' : 'none');
    host.classList.toggle('is-composing',composing);
  }
  function setValue(text:string,notify=false) {
    state=commandState(text);
    input.value=text;input.setSelectionRange(text.length,text.length);refresh();
    if (notify) input.dispatchEvent(new Event('input',{bubbles:true}));
  }
  function apply(next:CommandState) {
    state=next;input.value=next.text;input.setSelectionRange(next.text.length,next.text.length);refresh();
    input.dispatchEvent(new Event('input',{bubbles:true}));
  }
  input.addEventListener('beforeinput',event=>{
    const edit=event as InputEvent, objects=getObjects();
    if (!objects || composing || edit.isComposing || edit.inputType!=='insertText' || !edit.data ||
      [...edit.data].length!==1 || input.selectionStart!==input.value.length || input.selectionEnd!==input.value.length) return;
    if (state.text!==input.value) state=commandState(input.value);
    const next=typeCommand(state,edit.data,objects);
    if (next===undefined) return;
    event.preventDefault();apply(next);
  });
  for (const event of ['input','select','keyup','click','focus','blur','scroll']) input.addEventListener(event,refresh);
  document.addEventListener('selectionchange',()=>{if(document.activeElement===input) refresh();});
  input.addEventListener('compositionstart',()=>{composing=true;refresh();});
  input.addEventListener('compositionend',()=>{composing=false;refresh();});
  refresh();
  return {
    refresh,setValue,
    submission() {const objects=getObjects();return objects ? submissionText(input.value,objects) : input.value;},
    accept(event:KeyboardEvent) {
      if (!['Tab','Backspace'].includes(event.key) || event.shiftKey || event.altKey || event.ctrlKey || event.metaKey || composing ||
        input.selectionStart!==input.value.length || input.selectionEnd!==input.value.length) return false;
      if (state.text!==input.value) state=commandState(input.value);
      const objects=getObjects(), next=objects
        ? event.key==='Backspace' ? backspaceCommand(state,objects) : typeCommand(state,'Tab',objects)
        : undefined;
      if (next===undefined) return false;
      event.preventDefault();apply(next);return true;
    },
  };
}
