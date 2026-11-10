/** Run from the repository root with node 'archive/2026.11.06 settlement study/verify-assembly.ts'.
 * Checks the current canonical arrival, not every possible earlier campaign history.
 */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {parseStory} from '../../src/story/parser.ts';
import {checkpoint} from '../../src/debug/checkpoint.ts';
import {presentHotspots} from '../../src/engine/fixed-items.ts';
import {act, legalActions, recipeFor, replay, chapterComplete, type State} from '../../src/engine/game.ts';

const story = parseStory(fs.readFileSync('stories/settlement/settlement.md', 'utf8'));
const id = (name: string) => `name:${name}`;
const arrive = (title: string) => checkpoint(story, story.chapters.findIndex(c => c.name === title));
function dismiss(state: State) {
  while (state.pending.length) state = act(story, state, {type: 'dismiss'});
  return state;
}
function make(state: State, name: string) {
  const action = legalActions(story, state).find(a => recipeFor(story, state, a)?.result.id === id(name));
  assert(action, `Cannot make ${name}`);
  return dismiss(act(story, state, action));
}
// Encounter order, UI positions and readings cannot affect recipe eligibility.
function logical(state: State) {
  return {
    chapter: state.chapter,
    completed: state.completed,
    achieved: [...state.achieved].sort(),
    excluded: [...state.excluded].sort(),
    tokens: Object.fromEntries(Object.entries(state.tokens).sort(([a], [b]) => a.localeCompare(b)).map(([key, t]) => [key, {
      status: t.status, chapter: t.chapter, hotspot: t.hotspot, slots: [...t.slots].sort(),
    }])),
  };
}

const end = checkpoint(story, story.chapters.length);
assert(end.completed);
assert.deepEqual(replay(story, end.actions), end);

let base = dismiss(arrive('An encyclopedia'));
base = act(story, base, {type: 'move', item: id('Planks'), chapter: base.chapter, x: 165, y: 232.5, hotspot: id('Binding table')});
base = make(base, 'Binding boards');
const components = ['Printed pages', 'Pressed plant specimen', 'Botanical drawing', 'Pond life study', 'Rain record', 'Wind record', 'Star chart'];
const states = new Map<number, State>([[0, base]]);
let edges = 0;
for (let mask = 0; mask < 128; mask++) {
  const state = states.get(mask);
  assert(state);
  assert.equal(presentHotspots(story, state, state.chapter).length, 2);
  const binding = {type: 'combine' as const, a: id('Thread'), b: id('Binding boards')};
  assert.equal(!!recipeFor(story, state, binding), mask === 127);
  for (let i = 0; i < components.length; i++) {
    if (mask & (1 << i)) continue;
    const action = {type: 'combine' as const, a: id(components[i]), b: id('Binding boards')};
    assert(recipeFor(story, state, action));
    const next = dismiss(act(story, state, action));
    const nextMask = mask | (1 << i);
    assert.equal(next.tokens[id('Binding boards')].slots.length, components.filter((_, bit) => nextMask & (1 << bit)).length);
    const previous = states.get(nextMask);
    if (previous) assert.deepEqual(logical(next), logical(previous));
    else states.set(nextMask, next);
    edges++;
  }
}
const bound = dismiss(act(story, states.get(127)!, {type: 'combine', a: id('Thread'), b: id('Binding boards')}));
assert(chapterComplete(story, bound));
assert.equal(bound.tokens[id('Binding boards')].status, 'transform');
assert.equal(presentHotspots(story, bound, bound.chapter).length, 2);
assert.deepEqual(replay(story, bound.actions), bound);

let earlyCheckpoints = 0;
for (let i = 0; i < story.chapters.length - 2; i++) {
  const state = checkpoint(story, i);
  assert(!legalActions(story, state).some(a => recipeFor(story, state, a)?.result.id === id('Binding boards')));
  earlyCheckpoints++;
}
const starRecipes = story.recipes.filter(r => r.result.id === id('Star chart'));
assert.equal(starRecipes.length, 1);
assert([starRecipes[0].a.ref.id, starRecipes[0].b?.ref.id].includes(id('Mounted telescope')));
for (const removed of ['Botanical sheets', 'Weather record', 'Pond drawings', 'Glass slide', 'Kitchen hearth', 'Gallery']) {
  assert(!story.items[id(removed)]);
}

let printRoutes = 0;
for (const first of ['Ink', 'Paper']) {
  for (const reverseFirst of [false, true]) {
    for (const reverseSecond of [false, true]) {
      let state = dismiss(arrive('The mechanical workshop'));
      state = make(state, 'Printing block');
      state = make(state, 'Printing press');
      if (!state.tokens[id('Ink')]) state = make(state, 'Ink');
      let action = {type: 'combine' as const, a: id('Printing press'), b: id(first)};
      if (reverseFirst) [action.a, action.b] = [action.b, action.a];
      state = dismiss(act(story, state, action));
      const partial = first === 'Ink' ? 'Inked press' : 'Uninked press';
      const second = first === 'Ink' ? 'Paper' : 'Ink';
      action = {type: 'combine', a: id(partial), b: id(second)};
      if (reverseSecond) [action.a, action.b] = [action.b, action.a];
      state = dismiss(act(story, state, action));
      assert(state.tokens[id('Printed pages')]);
      assert.deepEqual(replay(story, state.actions), state);
      printRoutes++;
    }
  }
}
console.log(JSON.stringify({chapters: story.chapters.length, recipes: story.recipes.length, completedReplay: true,
  bindingSubsets: states.size, convergentBindingEdges: edges, prematureBindingBlocked: 127,
  earlyCheckpoints, printRoutes, starRequiresMount: true}, null, 2));
