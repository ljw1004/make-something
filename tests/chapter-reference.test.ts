import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, mkdirSync, writeFileSync, rmSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {parseStory} from '../src/story/parser.ts';
import {lintStoryImages} from '../src/lint/images.ts';
import {newGame, legalActions} from '../src/engine/game.ts';
import {currentArtwork, lookaheadArtwork, scrollbackArtwork} from '../src/web/artwork-plan.ts';
import {chapterReferenceRect} from '../src/web/chapter-reference.ts';
import {arrivalLayout, type ArrivalTile} from '../src/web/arrival-layout.ts';
import {overlapsHotspot} from '../src/web/hotspot-view.ts';
import {restoreDialogContext} from '../src/web/dialog-context.ts';

const reference = 'reference: ![Wind cart](assets/cart.svg)';
const storyText = (metadata = reference) => `# Reference workshop
## First
background: ![room](https://example.com/room.svg)
${metadata}
Opening words.
**Goals**
- Build -- C
**Items**
- A
- B
- C
**Combinations**
- A [preserve] + B [preserve] -> C
## Second
${reference}
Another stage.
**Goals**
- Build -- D
**Items**
- D
**Combinations**
- C [preserve] + B [preserve] -> D
## Third
The same room, without a picture.`;

test('reference metadata is chapter-local, source-located and separate from prose and logical play', () => {
  const source = storyText().replaceAll('\n', '\r\n'), story = parseStory(source), plain = parseStory(storyText(''));
  assert.equal(story.chapters[0].intro, 'Opening words.');
  assert.equal(story.chapters[1].intro, 'Another stage.');
  assert.equal(story.chapters[0].reference?.url, 'assets/cart.svg');
  assert.equal(story.chapters[0].reference?.alt, 'Wind cart');
  assert.equal(story.chapters[1].reference?.url, 'assets/cart.svg');
  assert.equal(story.chapters[2].reference, undefined);
  const span = story.chapters[0].reference!.source.span!;
  assert.equal(source.slice(span.from, span.to), reference);
  assert.deepEqual(story.diagnostics, []);
  assert.deepEqual(Object.keys(story.items), Object.keys(plain.items));
  assert.deepEqual(story.hotspots, plain.hotspots);
  assert.equal(story.recipes.length, plain.recipes.length);
  assert.deepEqual(legalActions(story, newGame(story)), legalActions(plain, newGame(plain)));
});

test('invalid, duplicate, misplaced and cover references are diagnosed without leaking into readings', () => {
  for (const prefix of ['Words first.\n', '> NOTE: earlier comment\n', `${reference}\n`]) {
    const story = parseStory(storyText(prefix + reference));
    assert(story.diagnostics.some(d => d.code === 'reference-position'));
    assert(!story.chapters[0].intro.includes('reference:'));
    assert.equal(story.chapters[0].reference?.url, prefix.startsWith('reference:') ? 'assets/cart.svg' : undefined);
  }
  for (const text of ['reference: ![](x.svg)', 'reference: ![Cart]()', 'reference: ![Cart](x.svg) words', 'reference : ![Cart](x.svg)', 'reference:![Cart](x.svg)', 'reference: ![A](a.svg) ![B](b.svg)']) {
    const story = parseStory(storyText(text));
    assert(story.diagnostics.some(d => d.code === 'reference-syntax'), text);
    assert.equal(story.chapters[0].reference, undefined);
    assert(!story.chapters[0].intro.includes('reference'));
  }
  const cover = parseStory(`# Cover\n${reference}\n\n## First\nWords.`);
  assert(cover.diagnostics.some(d => d.code === 'reference-context'));
  assert.equal(cover.description, '');
});

test('reference assets use manuscript-relative image lint and chapter preload frontiers', () => {
  const directory = mkdtempSync(join(tmpdir(), 'chapter-reference-'));
  try {
    const source = storyText(), story = parseStory(source, {file: join(directory, 'story.md')}), state = newGame(story);
    const missing = lintStoryImages(story, source);
    assert.equal(missing.length, 2);
    assert(missing.every(d => source.slice(d.span!.from, d.span!.to) === 'assets/cart.svg'));
    mkdirSync(join(directory, 'assets'));
    writeFileSync(join(directory, 'assets/cart.svg'), '<svg/>');
    assert.deepEqual(lintStoryImages(story, source), []);
    assert(currentArtwork(story, state).includes('assets/cart.svg'));
    assert(lookaheadArtwork(story, state, true).includes('assets/cart.svg'));
    assert(scrollbackArtwork(story, {...state, chapter: 1, visited: [0, 1]}).includes('assets/cart.svg'));
  } finally {rmSync(directory, {recursive: true, force: true});}
});

test('automatic arrivals reserve only the reference rectangle for fresh and carried objects on a short crowded board', () => {
  const bounds = {x: 0, y: 0, width: 390, height: 664}, reserved = chapterReferenceRect(bounds);
  const tiles: ArrivalTile[] = Array.from({length: 9}, (_, i) => ({id: String(i), x: 146, y: 12, width: i % 3 === 0 ? 110 : 80, height: 80, fresh: i > 3, fromChapter: 0}));
  const options = {bounds, goalsTop: 630, previousChapter: 0, hotspots: [{x: 79, y: 180, width: 232, height: 220}], reserved: [reserved]};
  const result = arrivalLayout(tiles, options);
  for (const tile of tiles) assert(!overlapsHotspot({...tile, ...result.positions.get(tile.id)!}, reserved), `${tile.id} obscures reference`);
  assert([...result.positions.values()].some(p => p.x < reserved.x && p.y < reserved.y + reserved.height), 'top-left pocket remains usable');
  assert.deepEqual(arrivalLayout(tiles, {...options, reserved: []}), arrivalLayout(tiles, {...options, reserved: undefined}));
});

test('reference reader anchors retain chapter identity and reject malformed saved values', () => {
  assert.deepEqual(restoreDialogContext({kind: 'reference', chapter: 'cart'}), {kind: 'reference', chapter: 'cart'});
  assert.equal(restoreDialogContext({kind: 'reference', chapter: 1}), undefined);
});
