import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { storyIds, loadStory } from '../src/story/load.ts';
import { lintStoryImages } from '../src/lint/images.ts';

test('discovery and CLI loading support shared artwork and ambiguous short names', () => {
  const root = mkdtempSync(join(tmpdir(), 'combination-manuscripts-'));
  try {
    mkdirSync(join(root, 'stories/shared/assets'), {recursive: true});
    mkdirSync(join(root, 'contrib/other'), {recursive: true});
    writeFileSync(join(root, 'stories/shared/assets/bg.svg'), '<svg xmlns="http://www.w3.org/2000/svg"/>');
    writeFileSync(join(root, 'stories/shared/first.md'), '# First\n\n## Opening\nbackground: ![scene](assets/bg.svg)');
    writeFileSync(join(root, 'stories/shared/second.md'), '# Second\n\n## Opening\nbackground: ![scene](assets/bg.svg)');
    writeFileSync(join(root, 'stories/shared/design-brief.md'), '# Design brief\n\nAuthor guidance, not a playable story.');
    assert.deepEqual(storyIds(root), ['stories/shared/first.md', 'stories/shared/second.md']);
    assert.throws(() => loadStory('stories/shared/design-brief.md', root), /Unknown story/);
    for (const name of ['first', 'second']) {
      const {story, markdown, path} = loadStory(name, root);
      assert.equal(path, `stories/shared/${name}.md`);
      assert.deepEqual(lintStoryImages(story, markdown), []);
    }
    writeFileSync(join(root, 'contrib/other/first.md'), '# Other first\n\n## Opening');
    assert.throws(() => loadStory('first', root), /Ambiguous story first/);
    assert.equal(loadStory('shared/first.md', root).story.title, 'First');
    assert.equal(loadStory('stories/shared/first.md', root).story.title, 'First');
    assert.equal(loadStory('contrib/other/first.md', root).story.title, 'Other first');
    assert.throws(() => loadStory('../outside.md', root), /Unknown story/);
  } finally {
    rmSync(root, {recursive: true, force: true});
  }
});
