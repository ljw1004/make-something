import type {Story} from '../story/types.ts';
import {board} from '../playtest/adventure.ts';
import type {Adventure, Frame, Message} from '../playtest/adventure.ts';
import {markdownInline} from './markdown.ts';

/** The human CLI's display conventions, without Node's readline or file loader. */
export function terminalFrame(story:Story, adventure:Adventure, refresh=false):Frame {
  return {...adventure.frame,
    messages:adventure.frame.messages.filter(message=>message.kind !== 'story'),
    options:adventure.frame.options.filter(option => option.kind === 'action'),
    ...(adventure.playStyle === 'detailed' && adventure.frame.prompt
      ? {prompt:`What will you [I]nspect or [C]ombine for step number ${adventure.frame.step}?`} : {}),
    ...(refresh ? {messages:[{kind:'board' as const,text:board(story,adventure.state)}]} : {}),
  };
}

/** Small, escaped Markdown presentation with text alternatives instead of images. */
export function terminalMarkdown(text:string,kind?:Message['kind']|'action'):string {
  let goals=false, objects=false;
  return text.split('\n').map(line=>{
    if (/^Goals(?: \(complete any one\))?:$/.test(line)) goals=true;
    else if (!line.trim()) goals=false;
    if (/^(Items|Hotspots):$/.test(line)) objects=true;
    const goal=kind === 'goals' || kind === 'goal-changes' || kind === 'chapter-completed' ||
      ((!kind || kind === 'board') && (goals || /^(?:Goal completed:|New goal:|All goals completed$)/.test(line)));
    // Only engine-generated references get item color. Indented descriptions,
    // chapter introductions and wonder prose retain their authored formatting.
    const references=kind === 'action' || (kind === 'board' && objects && line.startsWith('- ')) ||
      (kind === 'result' && /^\S/.test(line));
    const heading=/^(#{1,6})\s+(.+)$/.exec(line);
    const prose=(heading?.[2] ?? line).replace(/!\[([^\]]*)\]\([^)]+\)/g,'$1');
    const html=markdownInline(prose).replace(/<img\b[^>]*>/g,'');
    const formatted=heading ? `<span class="terminal-heading" role="heading" aria-level="${heading[1].length}">${html}</span>` : html;
    return goal ? `<span class="terminal-goal">${formatted}</span>`
      : references ? `<span data-terminal-objects="">${formatted}</span>` : formatted;
  }).join('\n');
}

/** Preserve the runner's message boundaries instead of inferring meaning from prose. */
export function terminalFrameMarkdown(frame:Frame):string {
  const messages=frame.messages.map((message,index)=>
    `${index ? message.kind === 'wonder' ? '\n' : '\n\n' : ''}${message.kind === 'chapter' ? '\n\n' : ''}${terminalMarkdown(message.text,message.kind)}`).join('');
  return messages+(frame.prompt ? `\n\n${terminalMarkdown(frame.prompt)}\n${frame.playStyle === 'fast'
    ? frame.options.map(option=>terminalMarkdown(`${option.choice}. ${option.text}`,'action')).join('\n') : ''}` : '');
}

/** Decorate marked reference fields only, preserving prose, Markdown and link destinations. */
export function highlightTerminalObjects(root:HTMLElement,names:string[]) {
  const words=[...new Set(names)].filter(Boolean).sort((a,b)=>b.length-a.length);
  if (!words.length) return;
  const pattern=words.map(name=>name.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|');
  const matcher=new RegExp(`(?<![\\p{L}\\p{N}_])(?:${pattern})(?![\\p{L}\\p{N}_])`,'gu');
  const document=root.ownerDocument, walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
  const nodes:Text[]=[];
  while (walker.nextNode()) nodes.push(walker.currentNode as Text);
  for (const node of nodes) {
    if (!node.parentElement?.closest('[data-terminal-objects]')) continue;
    const text=node.data, matches=[...text.matchAll(matcher)];
    if (!matches.length) continue;
    const fragment=document.createDocumentFragment();let offset=0;
    for (const match of matches) {
      fragment.append(text.slice(offset,match.index));
      const span=document.createElement('span');span.className='terminal-object';span.textContent=match[0];
      fragment.append(span);offset=match.index!+match[0].length;
    }
    fragment.append(text.slice(offset));node.replaceWith(fragment);
  }
}
