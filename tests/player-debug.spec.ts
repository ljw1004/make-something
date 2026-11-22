import { resolve } from 'node:path';
import { expect, test } from '@playwright/test';

test('debug icon is present in the development player but absent from the built player', async ({page}) => {
  const manuscript = '# Debug fixture\n\n## First chapter\n\n**Items**\n- Frame\n';
  await page.route('**/debug-fixture.md', route => route.fulfill({contentType:'text/markdown',body:manuscript}));

  await page.setViewportSize({width:1100,height:800});
  await page.goto('/index-dev.html?story=debug-fixture.md');
  await expect(page.getByRole('button', {name:'Start',exact:true})).toBeVisible();
  await expect(page.getByRole('button', {name:'Toggle debug panel'})).toBeVisible();

  await page.evaluate(() => {
    const storyUrl = new URL('debug-fixture.md', location.href).href;
    localStorage.setItem('combination-editor-open-v1:' + encodeURIComponent(storyUrl), 'true');
  });

  // Read the checked-in build directly instead of Vite's template alias.
  await page.route(/\/index\.html\?story=debug-fixture\.md$/, route =>
    route.fulfill({path:resolve('index.html'),contentType:'text/html'}));
  await page.goto('/index.html?story=debug-fixture.md');
  await expect(page.getByRole('button', {name:'Start',exact:true})).toBeVisible();
  await expect(page.getByRole('button', {name:'Toggle debug panel'})).toHaveCount(0);
  await expect(page.locator('.story-editor')).toHaveCount(0);
});
