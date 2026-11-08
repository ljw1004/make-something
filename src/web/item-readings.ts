import type {Story} from '../story/types.ts';
import type {State} from '../engine/types.ts';
import {act, readings} from '../engine/game.ts';
import {browserItemText} from '../story/text-only.ts';

export function browserReadings(story: Story, state: State, id: string) {
  return readings(story, state, id).map(reading => ({...reading,
    popup: browserItemText(reading.popup), encyclopedia: browserItemText(reading.encyclopedia),
  }));
}

/** Use real dismiss actions so reload/checkpoint replay retains the same history. */
export function dismissTextOnlyWonders(story: Story, initial: State): State {
  let state = initial;
  while (state.pending[0]?.kind === 'wonder' && !browserItemText(state.pending[0].markdown)) {
    state = act(story, state, {type: 'dismiss'});
  }
  return state;
}
