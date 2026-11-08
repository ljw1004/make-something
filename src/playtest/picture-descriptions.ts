import type {Story, Wonder} from '../story/types.ts';
import type {State} from '../engine/types.ts';
import {readings} from '../engine/game.ts';
import {itemPresentation} from '../engine/presentation.ts';
import {textOnlyPassages} from '../story/text-only.ts';

function passages(wonders: Pick<Wonder,'popup'|'encyclopedia'>[]): string {
  return [...new Set(wonders.flatMap(w=>[...textOnlyPassages(w.popup),...textOnlyPassages(w.encyclopedia)]))].join(' ');
}

export function itemPictureDescription(story: Story, state: State, id: string): string {
  return passages(readings(story,state,id));
}

/** Only the picture explicitly displayed as this chapter's reference is exposed.
 * Normal prose, slot conditions, recipes and future goals remain unavailable. */
export function referencePictureDescription(story: Story, state: State): string {
  const reference=story.chapters[state.chapter].reference;
  if(!reference)return '';
  for(const item of Object.values(story.items)){
    if(itemPresentation(story,state.chapter,item.id).icon?.url!==reference.url)continue;
    const description=passages(item.wonders.filter(w=>!w.requires.length));
    if(description)return `${reference.alt}: ${description}`;
  }
  return reference.alt;
}
