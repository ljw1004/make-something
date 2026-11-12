import './text-terminal.css';
import {parseStory} from '../story/parser.ts';
import type {Story} from '../story/types.ts';
import {choose, itemName, startAdventure} from '../playtest/adventure.ts';
import {label} from '../engine/game.ts';
import type {Adventure} from '../playtest/adventure.ts';
import {isLook, parseCommand} from '../playtest/commands.ts';
import {detailedObjects} from '../playtest/detailed.ts';
import {terminalCommandInput} from './terminal-command-input.ts';
import {resolveStoryURL} from './story-document.ts';
import {highlightTerminalObjects, terminalFrame, terminalFrameMarkdown} from './text-terminal-frame.ts';

const requestedStyle = document.body.dataset.playStyle;
if (requestedStyle !== 'fast' && requestedStyle !== 'detailed') throw new Error('Unknown terminal play style.');
const style = requestedStyle;
const transcript = document.querySelector<HTMLDivElement>('#transcript')!;
const form = document.querySelector<HTMLFormElement>('#prompt')!;
const input = document.querySelector<HTMLInputElement>('#command')!;
const status = document.querySelector<HTMLParagraphElement>('#status')!;
const picker = document.querySelector<HTMLElement>('#story-picker')!;
let story:Story, adventure:Adventure;
let ready=false, selecting=true;
const commandInput=terminalCommandInput(input,()=>ready && !selecting && style==='detailed' ? detailedObjects(story,adventure.state) : undefined);
const stories=[...picker.querySelectorAll<HTMLElement>('[data-story]')].map(node=>node.dataset.story!);
function showStorySelection(storyURL:string) {
  let choice=stories.findIndex(path=>new URL(path,location.href).href === storyURL)+1;
  if (!choice) {
    // A direct manuscript outside the published catalogue still gets a menu choice.
    const path=new URL(location.href).searchParams.get('story')!;
    choice=stories.push(path);
    const entry=document.createElement('span');entry.dataset.story=path;
    const title=document.createElement('span');title.className='terminal-story-title';
    title.textContent=story.title.toUpperCase().replace(/\.$/,'');
    const description=story.description.replace(/!\[[^\]]*\]\([^)]+\)/g,'').replace(/\s+/g,' ').trim();
    entry.append(`${choice}. `,title,`.${description ? ` ${description}` : ''}`);
    picker.append('\n\n',entry);
  }
  const selection=document.createElement('pre');selection.className='story-selection';
  selection.textContent=`> ${choice}`;
  transcript.append(selection);
}
function colorObjects(element:HTMLElement) {
  highlightTerminalObjects(element,Object.keys(adventure.state.tokens).flatMap(id=>[
    label(story,adventure.state,id),itemName(story,adventure.state,id),
  ]));
}
function revealPrompt() {
  if (!form.hidden) {
    input.focus({preventScroll:true});
    form.scrollIntoView({block:'nearest',behavior:'instant'});
    commandInput.refresh();
  } else transcript.lastElementChild?.scrollIntoView({block:'end',behavior:'instant'});
}
function display(refresh=false):HTMLElement {
  const output=document.createElement('pre');output.dataset.terminalOutput='';
  const text=document.createElement('span');text.dataset.terminalText='';
  text.innerHTML=terminalFrameMarkdown(terminalFrame(story,adventure,refresh));
  colorObjects(text);
  output.append(text);
  transcript.append(output);
  form.hidden=adventure.frame.phase !== 'choose';
  const url=new URL(location.href);
  url.searchParams.set('chapter',String(adventure.state.chapter+1));
  if (url.href !== location.href) window.history.replaceState(null,'',url);
  return output;
}

form.addEventListener('submit',event=>{
  event.preventDefault();
  if (!ready || (!selecting && adventure.frame.phase !== 'choose')) return;
  const line=commandInput.submission();commandInput.setValue('');
  const echo=document.createElement('pre');echo.className='command-echo';echo.textContent=`> ${line}`;
  if (!selecting) {echo.dataset.terminalObjects='';colorObjects(echo);}
  transcript.append(echo);
  try {
    if (selecting) {
      const choice=/^[1-9]\d*$/.test(line.trim()) ? Number(line.trim()) : NaN;
      if (!Number.isInteger(choice) || choice > stories.length) throw new Error(`Choose a story number from 1 to ${stories.length}.`);
      const url=new URL(location.href);
      url.searchParams.set('story',stories[choice-1]);url.searchParams.delete('chapter');
      // A real page navigation gives Back/Forward their ordinary browser behavior.
      echo.remove();location.assign(url.href);return;
    } else {
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
      display(refresh);
    }
  } catch (error) {
    const response=document.createElement('pre');response.className='command-error';
    response.setAttribute('role','alert');response.textContent=(error as Error).message;
    transcript.append(response);
  }
  revealPrompt();
});

input.addEventListener('input',()=>{
  if (promptAvailable()) revealPrompt();
});
function promptAvailable() {return ready && !form.hidden && !input.disabled;}
function otherControl(target:EventTarget|null) {
  return target instanceof Element && target !== input && !!target.closest('a,button,input,textarea,select,[contenteditable]');
}
document.addEventListener('click',event=>{
  if (!promptAvailable() || otherControl(event.target) || !window.getSelection()?.isCollapsed) return;
  input.focus({preventScroll:true});
});
document.addEventListener('keydown',event=>{
  if (!promptAvailable() || otherControl(event.target) || event.isComposing) return;
  if (!event.altKey && !event.ctrlKey && !event.metaKey && ['ArrowUp','ArrowDown'].includes(event.key)) {
    event.preventDefault();return;
  }
  const outside=document.activeElement !== input;
  const paste=(event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'v';
  const commandKey=!event.altKey && !event.ctrlKey && !event.metaKey &&
    (event.key.length === 1 || ['Enter','Backspace','Delete','ArrowLeft','ArrowRight','Home','End','Dead','Process'].includes(event.key));
  if (commandKey || paste) revealPrompt();
  if (commandInput.accept(event)) {revealPrompt();return;}
  // Enter's original target may be the transcript rather than the form.
  if (outside && commandKey && event.key === 'Enter') {
    event.preventDefault();form.requestSubmit();return;
  }
},true);

async function openStory(url:URL):Promise<HTMLElement> {
  ready=false;input.disabled=true;status.hidden=false;status.textContent='Loading story…';
  try {
    const chapter=url.searchParams.get('chapter');
    if (chapter !== null && !/^[1-9]\d*$/.test(chapter)) throw new Error('Chapter must be a positive whole number.');
    const startingChapter=chapter === null ? 1 : Number(chapter);
    const storyURL=resolveStoryURL(url.href);
    const response=await fetch(storyURL);
    if (!response.ok) throw new Error(`Could not load the story (HTTP ${response.status}).`);
    story=parseStory(await response.text(),{id:storyURL,file:storyURL});
    adventure=startAdventure(story,{chapter:startingChapter,playStyle:style,mode:'story'});
    showStorySelection(storyURL);
    window.history.replaceState(null,'',url);
    selecting=false;
    input.setAttribute('aria-label','Command');
    return display();
  } finally {ready=true;input.disabled=false;status.hidden=true;commandInput.refresh();}
}

async function open() {
  const url=new URL(location.href);
  if (!url.searchParams.has('story')) {
    ready=true;form.hidden=false;input.setAttribute('aria-label','Story number');revealPrompt();
    return;
  }
  try {
    await openStory(url);
    revealPrompt();
  } catch (error) {
    ready=false;status.hidden=false;
    status.textContent=(error as Error).message+' ';
    const retry=document.createElement('a');retry.href=location.href;retry.textContent='Try again';status.append(retry);
  }
}
void open();
