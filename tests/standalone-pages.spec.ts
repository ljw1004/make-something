import {expect, test} from '@playwright/test';
import {resolve} from 'node:path';

test('production pages work beneath a prefix with only HTML, icons and story files', async ({page}) => {
  const requests: string[] = [];
  const unexpected: string[] = [];
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.route('**/standalone/**', async route => {
    const file = new URL(route.request().url()).pathname.slice('/standalone/'.length);
    requests.push(file);
    if (['index.html', 'simulator.html', 'assets/appicon.png', 'assets/homescreen.png'].includes(file) || file.startsWith('stories/') || file.startsWith('contrib/')) {
      await route.fulfill({path: resolve(file)});
    } else {
      unexpected.push(file);
      await route.abort();
    }
  });
  await page.goto('/standalone/index.html');
  await expect(page.locator('.carousel-slide:visible h2')).toHaveText('Cookbook');
  const card = page.locator('.carousel-slide:visible a[data-story]');
  expect(requests.filter(path => path.endsWith('.md'))).toEqual([]);
  await card.click();
  await expect(page.getByRole('button', {name: 'Begin', exact: true})).toBeVisible();
  await expect(page).toHaveURL(/\/standalone\/index\.html\?story=stories\/cookbook\/cookbook\.md$/);
  expect(requests.filter(path => path.endsWith('.md'))).toEqual(['stories/cookbook/cookbook.md']);
  await page.reload();
  await expect(page.getByRole('button', {name: 'Begin', exact: true})).toBeVisible();

  for (const [title, slug] of [['Anatomy', 'anatomy'], ['History of ideas', 'ideas']]) {
    await page.goto('/standalone/index.html');
    await page.getByRole('button', {name: title, exact: true}).click();
    await card.click();
    await expect(page.getByRole('button', {name: 'Begin', exact: true})).toBeVisible();
    expect(new URL(page.url()).searchParams.get('story')).toBe(`contrib/${slug}/${slug}.md`);
  }

  for (const mode of ['fast', 'detailed']) {
    await page.goto(`/standalone/simulator.html?mode=${mode}&story=stories/cookbook/cookbook.md&chapter=2`);
    await expect(page.locator('[data-terminal-output]').last()).toBeVisible();
    await expect(page).toHaveURL(/chapter=2$/);
    await expect(page.locator('h1')).toContainText(mode === 'fast' ? '[story simulator]' : '[interaction simulator]');
  }
  expect(unexpected).toEqual([]);
  expect(errors).toEqual([]);
});
