import { resolve } from 'node:path';
import { expect, test, type Page } from '@playwright/test';

const storyPath = 'contrib/ideas/ideas.md';
const storyURL = '/index.html?story=' + storyPath;
const manuscript = `# ![Ideas](icon.png) Debug fixture
## Workshop
background: ![room](icon.png)
**Goals**
- Make A -- A
**Items**
- Seed
- Brush
- A
- B
- Tool
- Paint
**Combinations**
- Seed [preserve] + Brush [preserve] -> Paint (tutorial)
- A [preserve] + Tool [preserve] -> B
- B [preserve] + Tool [preserve] -> A
`;

async function serveBuild(page: Page) {
  // Bypass Vite's alias to exercise the self-contained production document.
  await page.route(/\/index\.html(?:\?|$)/, route => route.fulfill({path:resolve('index.html'), contentType:'text/html'}));
  await page.route('**/' + storyPath, route => route.fulfill({contentType:'text/markdown', body:manuscript}));
}

test('carousel debug resets only this catalogue’s tutorials without opening a story', async ({page}) => {
  await serveBuild(page);
  const fetched: string[] = [];
  page.on('request', request => { if (request.url().endsWith('.md')) fetched.push(request.url()); });
  await page.goto('/index.html');
  await page.getByRole('button', {name:'History of ideas', exact:true}).click();
  const keys = await page.evaluate(path => {
    const prefix = 'combination-tutorial-v1:';
    const url = (value: string) => encodeURIComponent(new URL(value, location.href).href);
    const clear = [prefix + url('index.html'), prefix + url(path),
      'combination-tutorial-drag-v2:' + url('stories/cookbook/cookbook.md')];
    const keep = [prefix + url('another-site/index.html'), 'combination-draft-v1:' + url(path),
      'combination-progress-v2:' + url(path)];
    for (const key of [...clear, ...keep]) localStorage.setItem(key, 'saved');
    for (const [story, kind] of [[path, 'drag'], [path, 'goals'], ['stories/cookbook/cookbook.md', 'goals'], [path, 'hotspot']]) {
      localStorage.setItem('combination-tutorial-shown-v1:' + url(story) + ':' + kind, 'true');
    }
    return {clear, keep};
  }, storyPath);
  const open = page.getByRole('button', {name:'Toggle carousel debug panel'});
  await open.click();
  const panel = page.getByRole('dialog', {name:'Carousel debug'});
  await expect(panel.getByRole('status')).toHaveText('3/4 tutorials shown');
  const close = panel.getByRole('button', {name:'Close', exact:true});
  await expect(close).toBeFocused();
  const reset = panel.getByRole('button', {name:'Reset', exact:true});
  expect((await close.boundingBox())!.y).toBeGreaterThan((await reset.boundingBox())!.y);
  await reset.click();
  await expect(panel.getByRole('status')).toHaveText('0/4 tutorials shown');
  expect(await page.evaluate(({clear, keep}) => ({
    cleared:clear.every(key => localStorage.getItem(key) === null),
    preserved:keep.every(key => localStorage.getItem(key) === 'saved'),
  }), keys)).toEqual({cleared:true, preserved:true});
  await close.click();
  await expect(open).toBeFocused();
  await expect(page.locator('.carousel-slide:visible h2')).toHaveText('History of ideas');
  await expect(page).toHaveURL('/index.html');
  expect(fetched).toEqual([]);
});

test('the right-hand pane fits beside a working carousel and adapts to a modal on resize', async ({page}) => {
  await serveBuild(page);
  await page.setViewportSize({width:1100, height:800});
  await page.goto('/index.html');
  const toggle = page.getByRole('button', {name:'Toggle carousel debug panel'});
  const panel = page.getByRole('dialog', {name:'Carousel debug'});
  await toggle.click();
  await expect(page.locator('.story-carousel')).toHaveCSS('width', '390px');
  expect((await panel.boundingBox())!.x).toBe(390);
  await page.getByRole('button', {name:'History of ideas', exact:true}).click();
  await expect(page.locator('.carousel-slide:visible h2')).toHaveText('History of ideas');
  await page.setViewportSize({width:899, height:800});
  await expect(page.locator('.catalogue-debug-panel:modal')).toBeVisible();
  await page.setViewportSize({width:900, height:800});
  await expect(panel.getByRole('button', {name:'Close debug panel'})).toBeVisible();
  await toggle.click();
  await expect(panel).toHaveCount(0);
  await expect(page.locator('.story-carousel')).toHaveCSS('width','900px');
  await toggle.click();
  await page.locator('.carousel-slide:visible a[data-story]').click();
  await expect(page.getByRole('button', {name:'Begin',exact:true})).toBeVisible();
  await expect(panel).toHaveCount(0);
  await page.getByRole('button', {name:'Begin',exact:true}).click();
  await expect(page.locator('.tutorial-overlay[data-tutorial="drag"]')).toBeVisible();
  await page.goBack();
  await toggle.click();
  await expect(panel.getByRole('status')).toHaveText('1/4 tutorials shown');
});

for (const reload of [false, true]) {
  test(`Home keeps an open story sidebar on its carousel card${reload ? ' after reload' : ''}`, async ({page}) => {
    await serveBuild(page);
    await page.setViewportSize({width:1100, height:800});
    if (reload) await page.emulateMedia({reducedMotion:'reduce'});
    await page.goto('/index.html');
    await page.getByRole('button', {name:'History of ideas', exact:true}).click();
    await page.locator('.carousel-slide:visible a[data-story]').click();
    await page.getByRole('button', {name:'Begin', exact:true}).click();
    await page.getByRole('button', {name:'Toggle debug panel'}).click();
    if (reload) await page.reload();
    await expect(page.getByRole('textbox', {name:'Story Markdown'})).toBeVisible();
    await page.getByRole('button', {name:'Read this chapter'}).click();
    await page.getByRole('link', {name:'Home', exact:true}).click();
    await expect(page).toHaveURL('/index.html');
    const sidebar = page.getByRole('dialog', {name:'Carousel debug'});
    await expect(sidebar.getByRole('button', {name:'Reset'})).toBeVisible();
    await expect(page.locator('.story-carousel')).toHaveCSS('width','390px');
    await expect(page.locator('.carousel-slide:visible h2')).toHaveText('History of ideas');
  });
}

test('an ordinary browser story offers the desktop editor with inline diagnostics and the mobile chapter picker', async ({page}) => {
  await serveBuild(page);
  await page.setViewportSize({width:1100, height:800});
  await page.goto(storyURL);
  const toggle = page.getByRole('button', {name:'Toggle debug panel'});
  await toggle.click();
  await expect(page.getByRole('textbox', {name:'Story Markdown'})).toContainText('Debug fixture');
  await expect(page.locator('.editor-diagnostic').filter({hasText:'[no-continuation]'})).toBeVisible();
  await page.getByRole('button', {name:'Close debug panel'}).click();
  await page.setViewportSize({width:390, height:844});
  await toggle.click();
  await expect(page.getByRole('dialog', {name:'Jump to chapter'}).getByRole('button', {name:'1. Workshop'})).toBeFocused();
});

for (const mode of ['standalone', 'iOS standalone']) {
  test(`${mode} hides debug on the carousel, in a story and from its own pinned start URL`, async ({page}) => {
    await serveBuild(page);
    await page.setViewportSize({width:1100, height:800});
    if (mode === 'standalone') {
      await page.addInitScript(() => {
        const match = window.matchMedia.bind(window);
        window.matchMedia = query => match(query === '(display-mode: standalone)' ? 'all' : query);
      });
    } else {
      await page.addInitScript(() => Object.defineProperty(navigator, 'standalone', {value:true}));
    }
    await page.goto('/index.html');
    await expect(page.locator('link[rel=manifest]')).toHaveCount(1);
    await expect(page.locator('.debug-button')).toHaveCount(0);
    await page.evaluate(path => {
      const url = new URL(path, location.href);
      localStorage.setItem('combination-editor-open-v1:' + encodeURIComponent(url.href), 'true');
    }, storyPath);
    await page.getByRole('button', {name:'History of ideas', exact:true}).click();
    await page.locator('.carousel-slide:visible a[data-story]').click();
    await expect(page.getByRole('button', {name:'Begin', exact:true})).toBeVisible();
    await expect(page.locator('.debug-button, .story-editor')).toHaveCount(0);
    const manifest = await page.locator('link[rel=manifest]').evaluate(async link => (await fetch((link as HTMLLinkElement).href)).json());
    expect(manifest.name).toBe('Debug fixture');
    expect(manifest.start_url).toBe(page.url());
    await page.goto(manifest.start_url);
    await expect(page.locator('link[rel=manifest]')).toHaveCount(1);
    await expect(page.locator('.debug-button, .story-editor')).toHaveCount(0);
  });
}

test('Start and Continue keep the sidebar boundary while the story loads at iPad size', async ({page}) => {
  await serveBuild(page);
  await page.setViewportSize({width:1100,height:800});
  let release: () => void;
  const gate = new Promise<void>(resolve => { release = resolve; });
  await page.route('**/' + storyPath, async route => {
    await gate;
    await route.fulfill({contentType:'text/markdown', body:manuscript + '- Paint + Tool -> A\n'});
  });
  await page.goto('/index.html');
  await page.getByRole('button', {name:'History of ideas', exact:true}).click();
  await page.getByRole('button', {name:'Toggle carousel debug panel'}).click();
  await page.getByLabel('Screen dimensions').selectOption('ipad-portrait');
  const cover = page.locator('.story-carousel');
  const app = page.locator('#app');
  const editor = page.getByRole('textbox', {name:'Story Markdown'});
  const card = page.locator('.carousel-slide:visible a[data-story]');
  const size = (el: HTMLElement) => [el.clientWidth, el.clientHeight];
  const pane = await cover.boundingBox();
  expect(pane!.width).toBeCloseTo(550, 1);
  expect(await cover.evaluate(size)).toEqual([1024,1366]);
  await expect(card).toContainText('Start');
  await card.click();
  await expect(page.locator('.story-entry-loading')).toBeVisible();
  expect(await app.boundingBox()).toEqual(pane);
  await expect(page.locator('#carousel-debug-panel')).toBeVisible();
  release!();
  await expect(editor).toBeVisible();
  expect(await app.boundingBox()).toEqual(pane);
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  await page.locator('[data-item="name:Seed"]').dragTo(page.locator('[data-item="name:Brush"]'));
  await expect(page.locator('[data-item="name:Paint"]')).toBeVisible();
  await page.getByRole('button',{name:'Read this chapter'}).click();
  await page.getByRole('link',{name:'Home',exact:true}).click();
  await expect(card).toContainText('Continue');
  expect(await cover.boundingBox()).toEqual(pane);
  await card.click();
  await expect(editor).toBeVisible();
  expect(await app.boundingBox()).toEqual(pane);
  await page.getByRole('button',{name:'Close debug panel'}).click();
  expect(await app.evaluate(size)).toEqual([1024,1366]);
  expect((await app.boundingBox())!.height).toBeCloseTo(800,1);
  await page.reload();
  await expect(page.locator('.chapter-panel')).toBeVisible();
  expect(await app.evaluate(size)).toEqual([1024,1366]);
  await expect(editor).toHaveCount(0);
});

test('the carousel popup remembers device dimensions across close and reload and can restore Auto', async ({page}) => {
  await serveBuild(page);
  await page.goto('/index.html');
  const toggle = page.getByRole('button',{name:'Toggle carousel debug panel'});
  const choice = page.getByLabel('Screen dimensions');
  const cover = page.locator('.story-carousel');
  const size = () => cover.evaluate(el => [el.clientWidth,el.clientHeight]);
  await toggle.click();
  await choice.selectOption('iphone');
  expect(await size()).toEqual([390,844]);
  await choice.selectOption('ipad-landscape');
  expect(await size()).toEqual([1366,1024]);
  await page.getByRole('button',{name:'Close',exact:true}).click();
  await page.reload();
  expect(await size()).toEqual([1366,1024]);
  await toggle.click();
  await expect(choice).toHaveValue('ipad-landscape');
  await page.setViewportSize({width:1000,height:700});
  await expect(page.locator('.catalogue-debug-panel:not(:modal)')).toBeVisible();
  expect((await cover.boundingBox())!.width).toBeCloseTo(500,1);
  await choice.selectOption('auto');
  expect(await size()).toEqual([390,700]);
  await toggle.click();
  expect(await size()).toEqual([1000,700]);
});

test('the scaled Creation opening preserves item placement and goal size at iPad portrait dimensions', async ({page, browser}) => {
  const reference = await browser.newPage({viewport:{width:1024,height:1366}});
  try {
    await page.setViewportSize({width:1100,height:800});
    async function opening(view: Page, pinned: boolean) {
      await view.goto('/index.html');
      await view.getByRole('button',{name:'Creation',exact:true}).click();
      if (pinned) {
        await view.getByRole('button',{name:'Toggle carousel debug panel'}).click();
        await view.getByLabel('Screen dimensions').selectOption('ipad-portrait');
      }
      await view.locator('.carousel-slide:visible a[data-story]').click();
      await view.getByRole('button',{name:'Begin',exact:true}).click();
      await expect(view.locator('#workspace')).toHaveClass(/entry-settled/);
      return view.locator('#app').evaluate(app => {
        const bounds = app.getBoundingClientRect(), scale = bounds.width / app.clientWidth;
        return [...app.querySelectorAll('[data-item], [data-hotspot], .objective-line')].map(el => {
          const r = el.getBoundingClientRect();
          return {id:el.getAttribute('aria-label') ?? el.textContent,
            box:[(r.x-bounds.x)/scale, (r.y-bounds.y)/scale, r.width/scale, r.height/scale]};
        });
      });
    }
    const actual = await opening(page, true), expected = await opening(reference, false);
    expect(actual.map(item => item.id)).toEqual(expected.map(item => item.id));
    expect(expected.length).toBeGreaterThan(3);
    actual.forEach((item, i) => item.box.forEach((value, j) => expect(value).toBeCloseTo(expected[i].box[j],1)));
  } finally { await reference.close(); }
});
