import type {Story, Wonder} from '../story/types.ts';
import type {State} from '../engine/types.ts';
import {readings} from '../engine/game.ts';
import {backgroundAnimation,hotspotPresentation,itemPresentation} from '../engine/presentation.ts';
import {background} from '../engine/analysis.ts';
import {isFixed} from '../engine/fixed-items.ts';
import {textOnlyPassages} from '../story/text-only.ts';

function passages(wonders: Pick<Wonder,'popup'|'encyclopedia'>[]): string {
  return [...new Set(wonders.flatMap(w=>[...textOnlyPassages(w.popup),...textOnlyPassages(w.encyclopedia)]))].join(' ');
}

export function itemPictureDescription(story: Story, state: State, id: string): string {
  return passages(readings(story,state,id));
}

/** Describe only the normal-motion artwork selected for a present board object. */
export function itemMotionDescription(story: Story, state: State, id: string): string {
  const token=state.tokens[id],item=story.items[id];
  if(!token || token.status!=='available' || token.chapter!==state.chapter || !item)return '';
  const appearance=itemPresentation(story,state.chapter,id);
  if(!appearance.icon || !appearance.animation || item.slots.some(slot=>token.slots.includes(slot.accepts)&&!slot.icon))return '';
  if(isFixed(story,token) && hotspotPresentation(story,state,token.chapter,id).icon!==appearance.icon)return '';
  return appearance.animation.alt.trim();
}

export function sceneMotionDescription(story: Story, state: State): string {
  return background(story,state.chapter) ? backgroundAnimation(story,state.chapter)?.alt.trim() ?? '' : '';
}

/** Faithful visual proxies for a current object, shared by boards and creations. */
export function itemArtworkDescription(story: Story, state: State, id: string): string {
  const token=state.tokens[id];
  if(!token || token.status!=='available' || token.chapter!==state.chapter)return '';
  const picture=itemPictureDescription(story,state,id),motion=itemMotionDescription(story,state,id);
  return [picture ? `Picture: ${picture}` : '',motion ? `Motion: ${motion}` : ''].filter(Boolean).join('\n');
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
