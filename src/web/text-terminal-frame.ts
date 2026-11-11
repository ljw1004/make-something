import type {Story} from '../story/types.ts';
import {background} from '../engine/analysis.ts';
import {board, renderFrame} from '../playtest/adventure.ts';
import type {Adventure, Frame} from '../playtest/adventure.ts';

/** The human CLI's display conventions, without Node's readline or file loader. */
export function terminalFrame(story:Story, adventure:Adventure, refresh=false):Frame {
  return {...adventure.frame,
    options:adventure.frame.options.filter(option => option.kind === 'action'),
    ...(adventure.playStyle === 'detailed' && adventure.frame.prompt
      ? {prompt:`What will you [I]nspect or [C]ombine for step number ${adventure.frame.step}?`} : {}),
    ...(refresh ? {messages:[{kind:'board' as const,text:board(story,adventure.state)}]} : {}),
  };
}

export type TerminalPart = {kind:'text'; text:string}|{kind:'image'; chapter:number; url:string};

/** Match chapter messages without parsing titles or replaying the engine.
 * The initial frame recounts every chapter before the checkpoint (including skips),
 * followed by actual arrivals. Later frames contain only new arrivals.
 */
export function terminalParts(story:Story, adventure:Adventure, previousVisits:number, refresh=false, startingChapter=1):TerminalPart[] {
  const frame = terminalFrame(story,adventure,refresh), text = renderFrame(frame);
  const visited=adventure.state.visited;
  const first=visited.find(chapter=>chapter >= startingChapter-1) ?? adventure.state.chapter;
  const chapters = refresh ? [] : previousVisits ? visited.slice(previousVisits)
    : [...Array.from({length:first},(_,chapter)=>chapter),...visited.filter(chapter=>chapter >= first)];
  const parts:TerminalPart[] = [];
  let offset=0, start=0, arrival=0;
  for (const [index,message] of frame.messages.entries()) {
    if (index) offset += message.kind === 'wonder' ? 1 : 2;
    if (message.kind === 'chapter') {
      const chapter = chapters[arrival++];
      // A completed run may announce a final skipped chapter without entering it.
      // Keep all runner text, but only actual visits receive scenery.
      const image = chapter === undefined || !visited.includes(chapter) ? undefined : background(story,chapter);
      if (image && chapter !== undefined) {
        if (offset > start) parts.push({kind:'text',text:text.slice(start,offset)});
        parts.push({kind:'image',chapter,url:image});
        start=offset;
      }
    }
    offset += message.text.length;
  }
  if (start < text.length) parts.push({kind:'text',text:text.slice(start)});
  return parts;
}
