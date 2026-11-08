import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, writeFileSync, rmSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {parseStory} from '../src/story/parser.ts';
import {StoryLanguageDocument} from '../src/story/language-service.ts';
import {background} from '../src/engine/analysis.ts';
import {backgroundAnimation} from '../src/engine/presentation.ts';
import {newGame} from '../src/engine/game.ts';
import {presentationDiagnostics} from '../src/lint/presentations.ts';
import {lintStoryImages} from '../src/lint/images.ts';
import {coverArtwork, currentArtwork, lookaheadArtwork, scrollbackArtwork} from '../src/web/artwork-plan.ts';

const manuscript = `# Scenes
background: ![cover](cover.svg)
## First
background: ![settled scene](poster.svg)
background animation: ![moving scene](scene.webp)
reference: ![Wind cart](cart.svg)
Opening words.
**Goals**
- Build -- C
**Items**
- A
- B
- C
**Combinations**
- A + B -> C
## Inherited
Same scene.
## Still
background animation: none
reference: ![Wind cart](cart.svg)
Pause.
## New room
background: ![new room](new.svg)
## New movement
background animation: ![new movement](new.webp)
## Fresh reset
background: ![fresh room](fresh.svg)`;

test('scene animation inherits with its poster, supports still/animation overrides and resets on a fresh background', () => {
  const story = parseStory(manuscript);
  assert.deepEqual(story.diagnostics, []);
  assert.deepEqual(story.chapters.map((_, i) => background(story, i)), ['poster.svg', 'poster.svg', 'poster.svg', 'new.svg', 'new.svg', 'fresh.svg']);
  assert.deepEqual(story.chapters.map((_, i) => backgroundAnimation(story, i)?.url), ['scene.webp', 'scene.webp', undefined, undefined, 'new.webp', undefined]);
  assert.equal(story.chapters[0].intro, 'Opening words.');
  assert.equal(story.chapters[2].intro, 'Pause.');
  assert.equal(story.chapters[0].reference?.url, 'cart.svg');
  assert.equal(story.chapters[2].reference?.url, 'cart.svg');
  const source = story.chapters[0].backgroundAnimation!.source;
  assert.equal(manuscript.slice(source.span!.from, source.span!.to), 'background animation: ![moving scene](scene.webp)');
  assert.deepEqual(Object.keys(story.items), ['name:C', 'name:A', 'name:B']);
});

test('malformed, misplaced, duplicate, cover and posterless animations are diagnosed and excluded from prose', () => {
  for (const text of ['background animation: no.webp', 'background animation: ![scene]()', 'background animation: ![scene](scene.webp) tail', 'background animation : ![scene](scene.webp)']) {
    const story = parseStory(manuscript.replace('background animation: ![moving scene](scene.webp)', text));
    assert(story.diagnostics.some(d => d.code === 'background-animation-syntax'), text);
    assert(!story.chapters[0].intro.includes('animation'));
  }
  for (const prefix of ['Words first.\n', '> NOTE: a note\n', 'background animation: none\n']) {
    const story = parseStory(manuscript.replace('background animation: ![moving scene](scene.webp)', prefix + 'background animation: ![moving scene](scene.webp)'));
    assert(story.diagnostics.some(d => d.code === 'background-animation-position'));
  }
  const cover = parseStory('# Scenes\nbackground: ![poster](p.svg)\nbackground animation: ![loop](l.webp)\n## One\nWords.');
  assert(cover.diagnostics.some(d => d.code === 'background-animation-context'));
  assert.equal(cover.description, '');
  const noPoster = parseStory('# Scenes\n## One\nbackground animation: ![loop](l.webp)');
  assert(presentationDiagnostics(noPoster).some(d => d.code === 'background-animation-poster'));
});

test('scene preparation includes animations at the same chapter frontier while covers and geometry keep the poster', () => {
  const story = parseStory(manuscript), state = newGame(story);
  assert.deepEqual(coverArtwork(story), ['cover.svg']);
  assert.deepEqual(coverArtwork({...story, cover: undefined}), ['poster.svg']);
  assert(currentArtwork(story, state).includes('scene.webp'));
  assert(lookaheadArtwork(story, state, true).includes('scene.webp'));
  assert(scrollbackArtwork(story, {...state, chapter: 2, visited: [0, 1, 2]}).includes('scene.webp'));
  assert(!currentArtwork(story, {...state, chapter: 2}).includes('scene.webp'));
  assert(!currentArtwork(story, {...state, chapter: 3}).includes('scene.webp'));
  assert.equal(background(story, 0), 'poster.svg');
});

test('scene animation paths participate in image lint and generic editor image hover', () => {
  const directory = mkdtempSync(join(tmpdir(), 'background-animation-'));
  try {
    for (const image of ['cover.svg', 'poster.svg', 'cart.svg', 'new.svg', 'fresh.svg']) writeFileSync(join(directory, image), '<svg/>');
    const story = parseStory(manuscript, {file: join(directory, 'story.md')});
    assert.deepEqual(lintStoryImages(story, manuscript).map(d => manuscript.slice(d.span.from, d.span.to)), ['scene.webp', 'new.webp']);
    const document = new StoryLanguageDocument(manuscript), hover = document.hover(manuscript.indexOf('scene.webp'));
    assert.equal(hover?.kind === 'image' && hover.url, 'scene.webp');
    assert.deepEqual(document.references(manuscript.indexOf('scene.webp'), {includeDeclaration: true}), []);
  } finally {rmSync(directory, {recursive: true, force: true});}
});
