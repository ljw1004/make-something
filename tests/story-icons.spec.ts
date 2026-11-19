import {test, expect} from '@playwright/test';
import {mkdtempSync, writeFileSync, rmSync} from 'node:fs';
import {resolve, join} from 'node:path';
import {parseStory} from '../src/story/parser.ts';
import {ArtworkBrowser} from '../src/lint/artwork-browser.ts';
import {openDebugPanel} from './debug-helpers.ts';

test('CLI decodes square, non-square and broken heading artwork without requiring placements', async () => {
  test.setTimeout(30000);
  const directory = mkdtempSync(resolve('runs/story-icons-'));
  const checker = new ArtworkBrowser();
  try {
    const story = (file: string) => parseStory(`# ![icon](${file}) Story\n## First`, {file: join(directory, 'story.md')});
    writeFileSync(join(directory, 'small.svg'), '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"/>');
    writeFileSync(join(directory, 'large.svg'), '<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024"/>');
    writeFileSync(join(directory, 'wide.svg'), '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="256"/>');
    writeFileSync(join(directory, 'broken.png'), 'not an image');
    for (const file of ['small.svg', 'large.svg']) expect(await checker.lint(story(file))).toEqual([]);
    expect((await checker.lint(story('wide.svg'))).map(d => d.code)).toEqual(['story-icon-square']);
    expect((await checker.lint(story('broken.png'))).map(d => d.code)).toEqual(['story-icon-image']);
  } finally { await checker.close(); rmSync(directory, {recursive: true, force: true}); }
});

test('catalogue cover images and story titles render without JavaScript', async ({browser}) => {
  const context = await browser.newContext({javaScriptEnabled: false});
  try {
    const page = await context.newPage();
    await page.goto('/');
    const cookbook = page.locator('.carousel-slide').filter({has: page.getByRole('heading', {name:'Cookbook', exact:true})});
    await expect(cookbook).toBeVisible();
    await expect.poll(() => cookbook.locator('.carousel-art').evaluate((image: HTMLImageElement) => image.naturalWidth)).toBeGreaterThan(0);
  } finally { await context.close(); }
});

test('live authoring measures heading art and clears old shape diagnostics after editing', async ({page}) => {
  await page.setViewportSize({width: 1280, height: 844});
  const text = '# ![icon](wide.svg) Icon draft\n## Start\nbackground: ![room](room.svg)\n\nAn opening.\n\n**Items**\n- A\n- B\n- C\n**Goals**\n- Make C -- C\n**Combinations**\n- A [preserve] + B [preserve] -> C (tutorial)';
  await page.route('**/icon-draft/story.md', route => route.fulfill({contentType: 'text/markdown', body: text}));
  await page.route('**/icon-draft/*.svg', route => {
    const width = route.request().url().endsWith('/wide.svg') ? 512 : 256;
    return route.fulfill({contentType: 'image/svg+xml', body: `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="256"/>`});
  });
  await page.goto('/make-something.html?story=icon-draft/story.md');
  await openDebugPanel(page);
  const shapeError = page.locator('.editor-diagnostic-text').filter({hasText: 'Story icons must be square'});
  await expect(shapeError).toHaveCount(1);
  const editor = page.getByRole('textbox', {name: 'Story Markdown'});
  const edit = async (value: string) => {
    await editor.focus(); await page.keyboard.press('ControlOrMeta+A'); await page.keyboard.insertText(value);
  };
  await edit(text.replace('wide.svg', 'square.svg'));
  await expect(shapeError).toHaveCount(0);
  await edit(text.replace('![icon](wide.svg) ', ''));
  await expect(page.locator('.editor-diagnostic-text').filter({hasText: 'Include a square Markdown image'})).toHaveCount(1);
  await expect(page.getByRole('button', {name: 'Start', exact: true})).toBeVisible();
});
