import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, writeFileSync, rmSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {parseStory} from '../src/story/parser.ts';
import {StoryLanguageDocument} from '../src/story/language-service.ts';
import {itemPresentation} from '../src/engine/presentation.ts';
import {newGame, legalActions} from '../src/engine/game.ts';
import {presentationDiagnostics} from '../src/lint/presentations.ts';
import {lintStoryImages} from '../src/lint/images.ts';
import {currentArtwork, resultArtwork, lookaheadArtwork, scrollbackArtwork} from '../src/web/artwork-plan.ts';

const manuscript = `# Workshop
## First
background: ![room](https://example.com/room.svg)
**Goals**
- Build -- \`cart\`
**Items**
- A
- B
- \`cart\` Wind cart
  - icon: ![cart](poster.svg)
  - animation: ![turning wheels](loop.webp)
  - from chapter "Second" animation: ![spinning wheels](fast.webp)
  - from chapter "Third" animation: none
**Combinations**
- A [consume] + B [transform] -> \`cart\`
## Second
**Items**
- D
**Goals**
- Continue -- E
**Combinations**
- \`cart\` [preserve] + D [transform] -> E
**Items**
- E
## Third
Done.`;

test('loop metadata stays out of logical identity and supports ordered chapter changes and still overrides', () => {
  const story = parseStory(manuscript), item = story.items['id:cart'];
  assert.deepEqual(story.diagnostics, []);
  assert.equal(item.animation?.url, 'loop.webp');
  assert.equal(manuscript.slice(item.animation!.source.span!.from, item.animation!.source.span!.to), 'animation: ![turning wheels](loop.webp)');
  assert.equal(itemPresentation(story, 0, item.id).animation?.url, 'loop.webp');
  assert.equal(itemPresentation(story, 1, item.id).animation?.url, 'fast.webp');
  assert.equal(itemPresentation(story, 2, item.id).animation, undefined);
  item.presentations.reverse();
  assert.equal(itemPresentation(story, 1, item.id).animation?.url, 'fast.webp');
  assert.equal(itemPresentation(story, 2, item.id).icon?.url, 'poster.svg');
  const plain = parseStory(manuscript.replace(/^  - .*animation:.*\n/gm, ''));
  assert.deepEqual(Object.keys(story.items), Object.keys(plain.items));
  assert.deepEqual(legalActions(story, newGame(story)), legalActions(plain, newGame(plain)));
});

test('loops join only the current/result/frontier artwork and restored scrollback', () => {
  const story = parseStory(manuscript), initial = newGame(story);
  assert(!currentArtwork(story, initial).includes('loop.webp'));
  assert(resultArtwork(story, initial, {type: 'combine', a: 'name:A', b: 'name:B'}).includes('loop.webp'));
  const state = {...initial, tokens: {...initial.tokens, 'id:cart': {id: 'id:cart', slots: [], status: 'available' as const, chapter: 0, x: 20, y: 100}}};
  assert(currentArtwork(story, state).includes('loop.webp'));
  assert(lookaheadArtwork(story, state, true).includes('fast.webp'));
  assert(scrollbackArtwork(story, {...state, chapter: 1, visited: [0, 1]}).includes('fast.webp'));
});

test('loop syntax, placement, poster and conflicting chapter variants have explicit diagnostics', () => {
  for (const declaration of ['animation: bad.webp', 'animation: ![empty]()', 'animation: ![loop](a.webp) (circular)', 'animation : ![loop](a.webp)', 'animation: ![loop](a.webp)\n    Extra prose.']) {
    assert(parseStory(manuscript.replace('animation: ![turning wheels](loop.webp)', declaration)).diagnostics.some(d => d.code === 'animation-syntax'), declaration);
  }
  assert(parseStory(manuscript.replace('  - animation: ![turning wheels](loop.webp)', '- animation: ![turning wheels](loop.webp)')).diagnostics.some(d => d.code === 'animation-placement'));
  assert(parseStory(manuscript.replace('  - animation: ![turning wheels](loop.webp)', '  - animation: ![turning wheels](loop.webp)\n  - animation: ![other](other.webp)')).diagnostics.some(d => d.code === 'conflicting-animation'));
  const withoutPoster = parseStory(manuscript.replace('  - icon: ![cart](poster.svg)\n', ''));
  assert(presentationDiagnostics(withoutPoster).some(d => d.code === 'animation-poster'));
  const conflict = parseStory(manuscript.replace('  - from chapter "Third" animation: none', '  - from chapter "Second" animation: none'));
  assert(presentationDiagnostics(conflict).some(d => d.code === 'conflicting-presentation'));
});

test('image lint and editor hover include base and chapter loop paths without inventing references', () => {
  const directory = mkdtempSync(join(tmpdir(), 'animation-'));
  try {
    const story = parseStory(manuscript, {file: join(directory, 'story.md')});
    writeFileSync(join(directory, 'poster.svg'), '<svg/>');
    const missing = lintStoryImages(story, manuscript);
    assert.deepEqual(missing.map(d => manuscript.slice(d.span.from, d.span.to)), ['loop.webp', 'fast.webp']);
    const document = new StoryLanguageDocument(manuscript);
    const image = document.hover(manuscript.indexOf('loop.webp'));
    assert.equal(image?.kind, 'image');
    assert.equal(image?.kind === 'image' && image.url, 'loop.webp');
    assert.deepEqual(document.references(manuscript.indexOf('loop.webp'), {includeDeclaration: true}), []);
    const item = document.hover(manuscript.indexOf('`cart` Wind'));
    assert(item?.kind === 'symbol' && item.properties.includes('Animation: loop.webp'));
    assert(item?.kind === 'symbol' && item.properties.includes('Animation: fast.webp from chapter Second'));
  } finally {rmSync(directory, {recursive: true, force: true});}
});
