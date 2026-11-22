import {test, expect, type Page} from '@playwright/test';
import {openDebugPanel} from './debug-helpers.ts';

const manuscript = `# ![Story icon](icon.png) Workshop & Wonders
## Workshop
Make a kit.

**Items**
- Frame
- Tool
- Kit
**Goals**
- Build -- Kit
**Combinations**
- Frame [preserve] + Tool [preserve] -> Kit
`;

async function browserManifest(page: Page) {
  await expect(page.locator('link[rel="manifest"]')).toHaveAttribute('href', /^data:application\/manifest\+json,/);
  const client = await page.context().newCDPSession(page);
  try {
    const result = await client.send('Page.getAppManifest');
    expect(result.errors).toEqual([]);
    expect(result.manifest?.display).toBe('kStandalone');
    expect((await client.send('Page.getInstallabilityErrors')).installabilityErrors).toEqual([]);
    return result.manifest!;
  } finally { await client.detach(); }
}

test('Chromium accepts inline catalogue and story manifests with existing icons and distinct stable identities', async ({page}) => {
  await page.goto('/');
  const origin = new URL(page.url()).origin;
  const catalogue = await browserManifest(page);
  expect(catalogue).toMatchObject({name: 'Make Something', id: origin + '/index.html', startUrl: origin + '/', scope: origin + '/'});
  expect(catalogue.icons).toEqual([{url: origin + '/assets/homescreen.png', sizes: '1024x1024', type: ''}]);
  await expect(page.locator('link[rel="apple-touch-icon"]')).toHaveAttribute('href', catalogue.icons![0].url);
  await expect(page.locator('meta[name="apple-mobile-web-app-title"]')).toHaveAttribute('content', 'Make Something');

  await page.route('**/stories/cookbook/*.md', route => route.fulfill({contentType: 'text/markdown', body: manuscript}));
  await page.goto('/index.html?story=stories/cookbook/cookbook.md&home=show#chapter');
  const first = await browserManifest(page);
  expect(first.name).toBe('Workshop & Wonders');
  expect(first.id).toBe(origin + '/stories/cookbook/cookbook.md');
  expect(first.icons?.[0]?.url).toBe(origin + '/stories/cookbook/icon.png');
  const launch = new URL(first.startUrl!);
  expect(launch.search).toBe('?story=stories/cookbook/cookbook.md');
  expect(launch.searchParams.has('home')).toBe(false);
  expect(launch.hash).toBe('');
  await expect(page.locator('meta[name="apple-mobile-web-app-title"]')).toHaveAttribute('content', first.name!);
  await expect(page.locator('link[rel="apple-touch-icon"]')).toHaveAttribute('href', first.icons![0].url);
  await expect(page).toHaveTitle('Make Something Worthwhile');
  await expect(page.locator('link[rel="icon"]')).toHaveAttribute('href', './assets/appicon.png');

  await page.goto(first.startUrl!);
  expect((await browserManifest(page)).id).toBe(first.id);
  await page.goto('/index.html?story=stories/cookbook/alternate.md');
  expect((await browserManifest(page)).id).not.toBe(first.id);
});

test('ordinary carousel click gives in-progress goals a Home link that survives reload and back', async ({page}) => {
  const unfinished = manuscript
    .replace('- Kit\n', '- Kit\n- Spare\n')
    .replace('- Build -- Kit', '- Build -- Kit\n- Find -- Spare')
    + '- Kit [preserve] + Tool [preserve] -> Spare\n';
  await page.route('**/stories/mars/mars.md', route => route.fulfill({contentType: 'text/markdown', body: unfinished}));
  await page.goto('/');
  await page.getByRole('button', {name: 'Mission to Mars', exact: true}).click();
  const card = page.locator('[data-story="stories/mars/mars.md"]');
  await expect(card).toHaveAttribute('href', 'index.html?story=stories/mars/mars.md');
  await card.click();
  const clean = /\/index.html\?story=stories\/mars\/mars\.md$/;
  await expect(page).toHaveURL(clean);
  await expect(page.locator('.tutorial-overlay')).toHaveAttribute('data-modality', 'mouse');
  await page.getByRole('button', {name: 'Begin', exact: true}).click();
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await expect(page.locator('[data-item="name:Kit"]')).toBeVisible();
  await expect(page.getByRole('link', {name: 'Home', exact: true})).toHaveCount(0);
  await expect(page.locator('.story-home')).toHaveCount(0);
  const goals = page.getByRole('button', {name: 'Read this chapter'});
  await page.reload();
  await goals.click();
  const home = page.getByRole('link', {name: 'Home', exact: true});
  const restart = page.getByRole('button', {name: 'Restart chapter', exact: true});
  await expect(home).toBeVisible();
  const left = (await restart.boundingBox())!, center = (await home.boundingBox())!;
  const close = page.getByRole('button', {name:'Close', exact:true});
  await expect(close).toBeFocused();
  const top = (await close.boundingBox())!;
  expect(left.x + left.width).toBeLessThan(center.x);
  expect(left.y + left.height / 2).toBeCloseTo(center.y + center.height / 2, 0);
  expect(center.y).toBeGreaterThan(top.y);
  await page.evaluate(() => localStorage.setItem('make-something-carousel-v1:/', 'stories/cookbook/cookbook.md'));
  await home.click();
  await expect(page).toHaveURL(/\/index.html$/);
  await expect(page.locator('.carousel-slide:not([hidden]) h2')).toHaveText('Mission to Mars');
  await expect(card).toContainText('Continue');
  await page.goBack();
  await expect(page).toHaveURL(clean);
  if (!await home.isVisible()) await goals.click();
  await expect(home).toBeVisible();
  // A same-address navigation from the current document is a reload in Chromium.
  await page.goto('/');
  await page.goto('/index.html?story=stories/mars/mars.md');
  await expect(page.locator('[data-item="name:Kit"]')).toBeVisible();
  await goals.click();
  await expect(home).toHaveCount(0);
});

test('fresh direct and legacy bookmark story visits open the cover without carousel context', async ({page}) => {
  await page.route('**/stories/mars/mars.md', route => route.fulfill({contentType: 'text/markdown', body: manuscript}));
  await page.goto('/index.html?story=stories/mars/mars.md');
  await expect(page.getByRole('button', {name: 'Start', exact: true})).toBeVisible();
  await page.goto('/index.html#mars');
  await expect(page).toHaveURL(/index.html\?story=stories\/mars\/mars\.md$/);
  await expect(page.getByRole('button', {name: 'Start', exact: true})).toBeVisible();
  await page.getByRole('button', {name: 'Start', exact: true}).click();
  await page.getByRole('button', {name: 'Begin', exact: true}).click();
  await page.getByRole('button', {name: 'Read this chapter'}).click();
  await expect(page.getByRole('link', {name: 'Home', exact: true})).toHaveCount(0);
});

test('a stale launch token cannot start a fresh direct visit', async ({page}) => {
  await page.route('**/stories/mars/mars.md', route => route.fulfill({contentType: 'text/markdown', body: manuscript}));
  await page.goto('/');
  const target = '/index.html?story=stories/mars/mars.md';
  await page.evaluate(target => {
    sessionStorage.setItem('make-something-entry-v1', JSON.stringify({
      launch: {entry:'carousel', manuscript:new URL('/stories/mars/mars.md', location.href).href, destination:new URL(target, location.href).href, modality:'touch'},
      expires:Date.now() + 30_000,
    }));
  }, target);
  await page.goto(target); // No matching catalogue referrer from a direct visit.
  await expect(page.getByRole('button', {name: 'Start', exact: true})).toBeVisible();
  expect(await page.evaluate(() => sessionStorage.getItem('make-something-entry-v1'))).toBeNull();
});

test('live title edits replace installation metadata without waiting for older icon downloads', async ({page}) => {
  await page.setViewportSize({width: 1280, height: 844});
  let release!: () => void;
  const waiting = new Promise<void>(resolve => { release = resolve; });
  await page.route('**/stories/cookbook/slow.png', async route => { await waiting; await route.fulfill({path: 'stories/cookbook/icon.png'}); });
  const draft = manuscript.replace('(icon.png)', '(slow.png)');
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType: 'text/markdown', body: draft}));
  try {
    await page.goto('/index.html?story=stories/cookbook/cookbook.md', {waitUntil: 'domcontentloaded'});
    await expect(page.getByRole('button', {name: 'Start', exact: true})).toBeVisible();
    await openDebugPanel(page);
    const editor = page.getByRole('textbox', {name: 'Story Markdown'});
    await editor.fill(manuscript.replace('Workshop & Wonders', 'Revised title'));
    await expect(page.locator('meta[name="apple-mobile-web-app-title"]')).toHaveAttribute('content', 'Revised title');
    const manifest = await browserManifest(page);
    expect(manifest.name).toBe('Revised title');
    expect(manifest.icons![0].url).toMatch(/\/stories\/cookbook\/icon.png$/);
    release();
    await page.evaluate(async () => {
      const oldIcon = new Image(); oldIcon.src = '/stories/cookbook/slow.png';
      await oldIcon.decode();
    });
    await expect(page.locator('link[rel="manifest"]')).toHaveCount(1);
    expect((await browserManifest(page)).name).toBe('Revised title');
  } finally { release(); }
});

test('Goals keeps Restart, Home and Encyclopedia in one adaptive row', async ({page}) => {
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.setViewportSize({width:320,height:600});
  const library = manuscript.replace('- Frame\n- Tool\n', '- Frame\n\n  Frame explanation.\n\n- Tool\n\n  Tool explanation.\n\n- Guide\n\n  Guide explanation.\n\n');
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType:'text/markdown',body:library}));
  await page.goto('/');
  await page.locator('.carousel-slide:not([inert]) a[data-story]').click();
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  const goals = page.getByRole('button',{name:'Read this chapter'});
  await goals.click();
  const footer = page.locator('.chapter-actions');
  const restart = footer.getByRole('button',{name:'Restart story',exact:true});
  const home = footer.getByRole('link',{name:'Home',exact:true});
  const book = footer.getByRole('button',{name:'Encyclopedia',exact:true});
  for (const control of [restart, home, book]) await expect(control).toBeVisible();
  const [row, left, center, right] = (await Promise.all([footer,restart,home,book].map(el=>el.boundingBox()))).map(box=>box!);
  expect(center.x + center.width / 2).toBeCloseTo(row.x + row.width / 2, 0);
  expect(left.x + left.width).toBeLessThan(center.x);
  expect(center.x + center.width).toBeLessThan(right.x);
  const narrow = await page.addStyleTag({content:'.chapter-actions{max-width:208px;width:100%;align-self:center}'});
  await expect(footer).toHaveClass(/icons-only/);
  const boxes = (await Promise.all([restart,home,book].map(el=>el.boundingBox()))).map(box=>box!);
  for (const box of boxes) { expect(box.width).toBeGreaterThanOrEqual(44); expect(box.height).toBeGreaterThanOrEqual(44); }
  expect(boxes[1].x + boxes[1].width / 2).toBeCloseTo(row.x + row.width / 2, 0);
  for (const control of [restart,home,book]) {
    expect(await control.locator('.popup-action-label').evaluate(node=>getComputedStyle(node).clipPath)).toBe('inset(50%)');
    await expect(control.locator('svg')).toBeVisible();
  }
  await book.click();
  await expect(page.getByRole('dialog',{name:'Encyclopedia'})).toBeVisible();
  await page.getByRole('button',{name:'Close',exact:true}).click();
  await goals.click();
  await restart.click();
  await expect(page.getByText('Restart this story?',{exact:true})).toBeVisible();
  await page.getByRole('button',{name:'Cancel',exact:true}).click();
  await narrow.evaluate(node=>node.parentNode?.removeChild(node));
  await expect(footer).not.toHaveClass(/icons-only/);
  for (const control of [restart,home,book])
    expect(await control.locator('.popup-action-label').evaluate(node=>getComputedStyle(node).clipPath)).toBe('none');
  await page.addStyleTag({content:'.chapter-actions{max-width:208px;width:100%;align-self:center}'});
  await expect(footer).toHaveClass(/icons-only/);
  await home.click();
  await expect(page).toHaveURL(/\/index.html$/);
  expect(errors).toEqual([]);
});
