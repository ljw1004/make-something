import './text-terminal.css';
import {parseStory} from '../story/parser.ts';
import type {Story} from '../story/types.ts';
import {choose, startAdventure} from '../playtest/adventure.ts';
import type {Adventure} from '../playtest/adventure.ts';
import {isLook, parseCommand} from '../playtest/commands.ts';
import {detailedObjects} from '../playtest/detailed.ts';
import {completeCommandLine} from '../playtest/terminal-input.ts';
import {resolveStoryAsset, resolveStoryURL} from './story-document.ts';
import {terminalParts} from './text-terminal-frame.ts';

const requestedStyle = document.body.dataset.playStyle;
if (requestedStyle !== 'fast' && requestedStyle !== 'detailed') throw new Error('Unknown terminal play style.');
const style = requestedStyle;
const transcript = document.querySelector<HTMLDivElement>('#transcript')!;
const form = document.querySelector<HTMLFormElement>('#prompt')!;
const input = document.querySelector<HTMLInputElement>('#command')!;
const status = document.querySelector<HTMLParagraphElement>('#status')!;
const picker = document.querySelector<HTMLElement>('#story-picker')!;
let story:Story, adventure:Adventure, storyURL:string, visits=0;
let ready=false;
const history:string[]=[];
let historyIndex=0, draft='';

function appendText(parent:HTMLElement,text:string,kind:string) {
  const span=document.createElement('span');
  span.dataset[kind]='';span.textContent=text;parent.append(span);
}
function display(refresh=false):HTMLElement {
  const output=document.createElement('pre');output.dataset.terminalOutput='';
  for (const part of terminalParts(story,adventure,visits,refresh)) {
    if (part.kind === 'text') {appendText(output,part.text,'terminalText');continue;}
    const picture=document.createElement('span');
    picture.className='chapter-picture';picture.dataset.chapter=String(part.chapter);
    picture.setAttribute('aria-hidden','true');
    const image=document.createElement('img');image.alt='';image.draggable=false;
    const fallback=document.createElement('span');fallback.className='picture-error';
    fallback.textContent='[Chapter image unavailable]';fallback.hidden=true;
    image.onerror=()=>{image.hidden=true;fallback.hidden=false;};
    try {image.src=resolveStoryAsset(part.url,storyURL);}
    catch {image.hidden=true;fallback.hidden=false;}
    picture.append(image,fallback);output.append(picture);
  }
  visits=adventure.state.visited.length;
  transcript.append(output);
  form.hidden=adventure.frame.phase !== 'choose';
  return output;
}

form.addEventListener('submit',event=>{
  event.preventDefault();
  if (!ready || adventure.frame.phase !== 'choose') return;
  const line=input.value;input.value='';
  if (line.trim()) history.push(line);
  historyIndex=history.length;draft='';
  const echo=document.createElement('pre');echo.className='command-echo';echo.textContent=`> ${line}`;
  transcript.append(echo);
  let response:HTMLElement;
  try {
    let refresh=false;
    if (style === 'detailed') {
      const command=parseCommand(line);
      if (isLook(command)) refresh=true;
      else adventure=choose(story,adventure,adventure.frame.step,command);
    } else {
      const choice=line.trim() ? Number(line.trim()) : NaN;
      if (!Number.isFinite(choice)) refresh=true;
      else adventure=choose(story,adventure,adventure.frame.step,choice);
    }
    response=display(refresh);
  } catch (error) {
    response=document.createElement('pre');response.className='command-error';
    response.setAttribute('role','alert');response.textContent=(error as Error).message;
    transcript.append(response);
  }
  if (!form.hidden) input.focus({preventScroll:true});
  response.scrollIntoView({block:'start',behavior:'instant'});
});

input.addEventListener('input',event=>{
  const edit=event as InputEvent;
  if (!ready || style !== 'detailed' || edit.isComposing || edit.inputType !== 'insertText' ||
    input.selectionStart !== input.value.length || input.selectionEnd !== input.value.length) return;
  const completed=completeCommandLine(input.value,detailedObjects(story,adventure.state));
  if (completed !== input.value) {
    input.value=completed;input.setSelectionRange(completed.length,completed.length);
  }
});
input.addEventListener('keydown',event=>{
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || event.isComposing ||
    !['ArrowUp','ArrowDown'].includes(event.key)) return;
  event.preventDefault();
  if (historyIndex === history.length) draft=input.value;
  historyIndex=Math.max(0,Math.min(history.length,historyIndex+(event.key === 'ArrowUp' ? -1 : 1)));
  input.value=history[historyIndex] ?? draft;
  input.setSelectionRange(input.value.length,input.value.length);
});

async function open() {
  if (!new URL(location.href).searchParams.has('story')) return;
  picker.hidden=true;status.hidden=false;status.textContent='Loading story…';
  try {
    storyURL=resolveStoryURL(location.href);
    const response=await fetch(storyURL);
    if (!response.ok) throw new Error(`Could not load the story (HTTP ${response.status}).`);
    story=parseStory(await response.text(),{id:storyURL,file:storyURL});
    adventure=startAdventure(story,{playStyle:style,mode:'story'});
    display();ready=true;status.hidden=true;
    document.title=`${story.title} · --${style} · Text engine`;
    const other=document.querySelector<HTMLAnchorElement>('[data-other-mode]')!;
    const otherURL=new URL(other.href);
    otherURL.search=new URL(location.href).search;
    other.href=otherURL.href;
    if (!form.hidden) input.focus({preventScroll:true});
  } catch (error) {
    status.textContent=(error as Error).message+' ';
    const retry=document.createElement('a');retry.href=location.href;retry.textContent='Try again';status.append(retry);
  }
}
void open();
