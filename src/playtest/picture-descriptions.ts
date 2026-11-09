import type {Story} from '../story/types.ts';
import type {State} from '../engine/types.ts';
import {readings} from '../engine/game.ts';
import {textOnlyPassages} from '../story/text-only.ts';

export function itemPictureDescription(story: Story, state: State, id: string): string {
  return [...new Set(readings(story,state,id).flatMap(w=>[...textOnlyPassages(w.popup),...textOnlyPassages(w.encyclopedia)]))].join(' ');
}

/** Authored descriptions of current pictures, shared by boards and creations. */
export function itemArtworkDescription(story: Story, state: State, id: string): string {
  const token=state.tokens[id];
  if(!token || token.status!=='available' || token.chapter!==state.chapter)return '';
  const picture=itemPictureDescription(story,state,id);
  return picture ? `Picture: ${picture}` : '';
}
