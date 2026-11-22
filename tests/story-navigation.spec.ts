import {expect, test, type CDPSession, type Page} from '@playwright/test';

const fixture = `# Workshop
## First chapter
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

const storyURL = /index.html\?story=stories\/cookbook\/cookbook\.md$/;
const catalogue = (page: Page) => page.locator('#catalogue-app');
const board = (page: Page) => page.locator('.game-surface');
const begin = (page: Page) => page.getByRole('button', {name:'Begin', exact:true});
const card = (page: Page) => page.locator('a[data-story="stories/cookbook/cookbook.md"]');
const spinner = (page: Page) => page.locator('.story-entry-loading');
const offset = (locator: ReturnType<Page['locator']>) => locator.evaluate(node => Math.round(node.getBoundingClientRect().y));

async function serveStory(page: Page, body = fixture) {
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType:'text/markdown',body}));
}
async function touch(client: CDPSession, type: 'touchStart'|'touchMove'|'touchEnd', x = 0, y = 0, timestamp?: number) {
  await client.send('Input.dispatchTouchEvent', {type, touchPoints:type === 'touchEnd' ? [] : [{x,y}], timestamp});
}
async function verticalFlick(client: CDPSession, y: number, delta: number, x = 20) {
  const start = Date.now() / 1000;
  await touch(client, 'touchStart', x, y, start);
  await touch(client, 'touchMove', x, y + delta / 2, start + .016);
  await touch(client, 'touchMove', x, y + delta, start + .032);
  await touch(client, 'touchEnd', 0, 0, start + .036);
}

test('a Start swipe previews the introduction and a Continue swipe opens the board directly', async ({browser}) => {
  const context = await browser.newContext({viewport:{width:390,height:844}, isMobile:true, hasTouch:true});
  try {
    const page = await context.newPage();
    await serveStory(page);
    await page.goto('/');
    const client = await context.newCDPSession(page);
    await touch(client,'touchStart',20,690);
    await touch(client,'touchMove',20,390);
    await expect.poll(() => offset(catalogue(page))).toBe(-300);
    await expect(page.locator('dialog')).toHaveCount(0);
    await expect(page.locator('[data-item="name:Frame"]')).toHaveCount(1);
    await expect.poll(() => offset(board(page))).toBe(544);
    await touch(client,'touchMove',20,225);
    await expect(page.locator('dialog[open]')).toBeVisible();
    const pinned = await page.locator('dialog[open]').boundingBox();
    await touch(client,'touchMove',20,140);
    await expect.poll(() => offset(board(page))).toBe(294);
    expect(await page.locator('dialog[open]').boundingBox()).toEqual(pinned);
    await touch(client,'touchMove',20,640);
    await expect(page.locator('dialog')).toHaveCount(0);
    await touch(client,'touchMove',20,676);
    await touch(client,'touchEnd');
    await expect(board(page)).toHaveCount(0);
    expect(await page.evaluate(() => Object.keys(localStorage).some(key => key.startsWith('combination-progress-v2:')))).toBe(false);
    await expect(page).toHaveURL('/');

    await verticalFlick(client, 690, -40);
    await expect(page).toHaveURL(storyURL);
    await expect(begin(page)).toBeFocused();
    await begin(page).tap();
    await expect.poll(() => offset(board(page))).toBe(0);
    await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
    await expect(page.locator('[data-item="name:Kit"]')).toBeVisible();
    await verticalFlick(client, 110, 40);
    await expect(page).toHaveURL(/\/index.html$/);
    await expect(board(page)).toHaveCount(0);
    await expect(card(page)).toBeFocused();
    await expect(card(page)).toContainText('Continue');
    await touch(client,'touchStart',20,690);
    await touch(client,'touchMove',20,225);
    await expect(page.locator('dialog')).toHaveCount(0);
    await touch(client,'touchEnd');
    await expect(page).toHaveURL(storyURL);
    await expect.poll(() => offset(board(page))).toBe(0);
    await expect(page.locator('[data-item="name:Kit"]')).toBeVisible();
    await expect(page.locator('dialog')).toHaveCount(0);
  } finally { await context.close(); }
});

test('backdrop swipes leave and resume chapter readings without taking over gestures inside them', async ({browser}) => {
  const context = await browser.newContext({viewport:{width:390,height:844}, isMobile:true, hasTouch:true});
  try {
    const page = await context.newPage();
    const prose = Array.from({length:20}, (_, i) => `Workshop instruction ${i + 1}. Read the plans carefully.`).join('\n\n');
    await serveStory(page, fixture.replace('Make a kit.', prose));
    await page.goto('/');
    await card(page).tap();
    const reading = page.getByRole('dialog');
    await expect(begin(page)).toBeFocused();
    await expect(page.locator('.catalogue-player')).toHaveClass(/entry-settled/);
    const client = await context.newCDPSession(page);

    const readingTop = await offset(reading);
    await touch(client, 'touchStart', 7, 220);
    await touch(client, 'touchMove', 7, 340);
    await expect.poll(() => offset(reading)).toBe(readingTop + 120);
    await expect.poll(() => offset(board(page))).toBe(120);
    await client.send('Input.dispatchTouchEvent', {type:'touchCancel',touchPoints:[]});
    await expect.poll(() => offset(reading)).toBe(readingTop);
    await expect(page).toHaveURL(storyURL);

    await verticalFlick(client, 220, 110, 7);
    await expect(card(page)).toBeFocused();
    await verticalFlick(client, 690, -110);
    await expect(begin(page)).toBeFocused();
    await begin(page).tap();
    await expect(page.locator('.catalogue-player')).toHaveClass(/entry-settled/);
    await page.getByRole('button', {name:'Read this chapter'}).tap();
    const close = reading.getByRole('button', {name:'Close',exact:true});
    await expect(close).toBeFocused();
    const proseScroll = reading.locator('.reading-text');
    await verticalFlick(client, 520, -170, 160);
    await expect.poll(() => proseScroll.evaluate(node => node.scrollTop)).toBeGreaterThan(0);
    const scrollTop = await proseScroll.evaluate(node => node.scrollTop);
    await touch(client, 'touchStart', 7, 110);
    await touch(client, 'touchMove', 127, 110);
    await touch(client, 'touchEnd');
    await expect(close).toBeFocused();
    await expect.poll(() => offset(board(page))).toBe(0);

    await verticalFlick(client, 220, 110, 7);
    await expect(card(page)).toBeFocused();
    await verticalFlick(client, 690, -110);
    await expect(close).toBeFocused();
    await expect.poll(() => proseScroll.evaluate(node => node.scrollTop)).toBeGreaterThanOrEqual(scrollTop);
    await expect(page.locator('.catalogue-player')).toHaveClass(/entry-settled/);
    await page.touchscreen.tap(7, 220);
    await expect(reading).toHaveCount(0);
    await verticalFlick(client, 110, 110, 7);
    await expect(card(page)).toBeFocused();
    await verticalFlick(client, 690, -110);
    await expect(page).toHaveURL(storyURL);
    await expect.poll(() => offset(board(page))).toBe(0);
    // The card still says Start because no combination has been made.
    await expect(reading).toHaveCount(0);
  } finally { await context.close(); }
});

test('tap slides in both directions and Back and Forward restore the corresponding view', async ({page}) => {
  // Slow rAF so both halves can be observed without depending on machine load.
  await page.addInitScript(() => {
    const frame = window.requestAnimationFrame;
    window.requestAnimationFrame = callback => frame(time => callback(time - 120));
  });
  await serveStory(page);
  await page.goto('/');
  await card(page).focus();
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(storyURL);
  await expect(begin(page)).toBeFocused();
  const reading = page.getByRole('dialog'), pinned = await reading.boundingBox();
  expect(await offset(board(page))).toBeGreaterThan(0);
  await expect.poll(() => offset(board(page))).toBe(0);
  expect(await reading.boundingBox()).toEqual(pinned);
  await begin(page).click();
  await page.getByRole('button',{name:'Read this chapter'}).click();
  await page.getByRole('link',{name:'Home',exact:true}).click();
  await expect.poll(() => offset(board(page))).toBeGreaterThan(0);
  await expect(page).toHaveURL(/\/index.html$/);
  await expect(card(page)).toBeFocused();
  await page.goBack();
  await expect(page.locator('[data-item="name:Frame"]')).toBeVisible();
  await expect(page.locator('dialog')).toHaveCount(0);
  expect(await offset(board(page))).toBe(0);
  await page.goForward();
  await expect(board(page)).toHaveCount(0);
  await expect(card(page)).toBeVisible();
});

test('entering with slow artwork reaches the black loading view before revealing the board and popup', async ({page}) => {
  let release!: () => void;
  const pending = new Promise<void>(resolve => {release = resolve;});
  await serveStory(page, fixture.replace('Make a kit.', 'background: ![Room](room-fixture.svg)\nMake a kit.'));
  await page.route('**/stories/cookbook/room-fixture.svg', async route => {
    await pending;
    await route.fulfill({contentType:'image/svg+xml',body:'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844"/>'});
  });
  try {
    await page.goto('/');
    await card(page).click();
    await expect(page).toHaveURL(storyURL);
    await expect.poll(() => offset(board(page))).toBe(0);
    await expect(spinner(page)).toBeVisible();
    await expect(board(page)).toHaveCSS('background-color','rgb(0, 0, 0)');
    await expect(page.locator('.story-loading, dialog')).toHaveCount(0);
  } finally {release();}
  await expect(begin(page)).toBeFocused();
  await expect(spinner(page)).toHaveCount(0);
  await expect(page.locator('.chapter-panel [data-item="name:Frame"]')).toHaveCount(1);
});

for (const resource of ['bundle', 'manuscript'] as const) {
  test(`swipe down can leave a story while its ${resource} is loading`, async ({browser}) => {
    const context = await browser.newContext({viewport:{width:390,height:844}, isMobile:true, hasTouch:true});
    let release!: () => void;
    const pending = new Promise<void>(resolve => {release = resolve;});
    try {
      const page = await context.newPage();
      if (resource === 'bundle') {
        await serveStory(page);
        await page.route('**/src/web/main.ts*', async route => {await pending; await route.continue();});
      } else {
        await page.route('**/stories/cookbook/cookbook.md', async route => {
          await pending;
          await route.fulfill({contentType:'text/markdown',body:fixture}).catch(() => {});
        });
      }
      await page.goto('/');
      const client = await context.newCDPSession(page);
      await touch(client,'touchStart',20,690);
      await touch(client,'touchMove',20,440);
      await expect.poll(() => offset(catalogue(page))).toBe(-250);
      await touch(client,'touchEnd');
      await expect(page).toHaveURL(storyURL);
      await expect(spinner(page)).toBeVisible();
      await expect.poll(() => offset(board(page))).toBe(0);
      await touch(client,'touchStart',20,200);
      await touch(client,'touchMove',20,264);
      await expect.poll(() => offset(board(page))).toBe(64);
      await page.waitForTimeout(80);
      await touch(client,'touchEnd');
      await expect.poll(() => offset(board(page))).toBe(0);
      await expect(page).toHaveURL(storyURL);

      await verticalFlick(client, 200, 40);
      await expect(page).toHaveURL(/\/index.html$/);
      await expect(board(page)).toHaveCount(0);
      expect(await page.evaluate(() => Object.keys(localStorage).some(key => key.startsWith('combination-progress-v2:')))).toBe(false);
    } finally {release(); await context.close();}
  });
}

test('reduced motion enters and returns immediately, and a direct story still starts on its cover', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await serveStory(page);
  await page.goto('/index.html?story=stories/cookbook/cookbook.md');
  await expect(page.getByRole('button',{name:'Start',exact:true})).toBeVisible();
  await page.goto('/');
  await card(page).click();
  await expect(begin(page)).toBeVisible();
  expect(await offset(board(page))).toBe(0);
  await begin(page).click();
  await page.getByRole('button',{name:'Read this chapter'}).click();
  await page.getByRole('link',{name:'Home',exact:true}).click();
  await expect(page).toHaveURL(/\/index.html$/);
  await expect(board(page)).toHaveCount(0);
});

test('Home after a story reload restores the same card without showing the default card first', async ({page}) => {
  await page.route('**/stories/mars/mars.md', route => route.fulfill({contentType:'text/markdown', body:fixture}));
  await page.goto('/');
  await page.getByRole('button',{name:'Mission to Mars',exact:true}).click();
  const mars = page.locator('a[data-story="stories/mars/mars.md"]');
  await mars.click();
  await begin(page).click();
  await page.reload();
  await page.getByRole('button',{name:'Read this chapter'}).click();

  let release!: () => void;
  const pending = new Promise<void>(resolve => {release = resolve;});
  await page.route('**/src/web/catalogue.ts', async route => {await pending; await route.continue();});
  try {
    await page.getByRole('link',{name:'Home',exact:true}).click();
    await page.waitForURL(/\/index.html$/, {waitUntil:'commit'});
    await expect(page.locator('html')).toHaveClass(/carousel-home-bootstrap/);
    await expect(card(page)).toBeHidden();
  } finally {release();}
  await expect(mars).toBeVisible();
  await expect(page.locator('html')).not.toHaveClass(/carousel-home-bootstrap/);
});

test('vertical mouse drags snap back at 64 CSS pixels and complete at 65', async ({page}) => {
  await serveStory(page);
  await page.goto('/');
  await page.mouse.move(20,650);
  await page.mouse.down();
  await page.mouse.move(20,586,{steps:4});
  await expect.poll(() => offset(catalogue(page))).toBe(-64);
  await page.waitForTimeout(80);
  await page.mouse.up();
  await expect.poll(() => offset(catalogue(page))).toBe(0);
  await expect(board(page)).toHaveCount(0);
  await expect(page).toHaveURL('/');

  await page.mouse.move(20,650);
  await page.mouse.down();
  await page.mouse.move(20,585,{steps:4});
  await expect.poll(() => offset(catalogue(page))).toBe(-65);
  await page.waitForTimeout(80);
  await page.mouse.up();
  await expect(page).toHaveURL(storyURL);
  await begin(page).click();
  await expect.poll(() => offset(board(page))).toBe(0);
  await expect(page.locator('[data-item="name:Frame"]')).toBeVisible();
  await expect(page.locator('dialog')).toHaveCount(0);

  await page.mouse.move(20,120);
  await page.mouse.down();
  await page.mouse.move(20,184,{steps:4});
  await expect.poll(() => offset(board(page))).toBe(64);
  await page.waitForTimeout(80);
  await page.mouse.up();
  await expect.poll(() => offset(board(page))).toBe(0);
  await expect(page).toHaveURL(storyURL);

  await page.mouse.move(20,120);
  await page.mouse.down();
  await page.mouse.move(20,185,{steps:4});
  await expect.poll(() => offset(board(page))).toBe(65);
  await page.waitForTimeout(80);
  await page.mouse.up();
  await expect(page).toHaveURL(/\/index.html$/);
  await expect(board(page)).toHaveCount(0);
  await expect(card(page)).toBeFocused();
});

test('wheel input scrolls a cover description and leaves the current page in place', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await serveStory(page);
  await page.goto('/');
  const description = page.locator('.carousel-slide:not([hidden]) .carousel-description');
  await description.evaluate(node => { node.textContent = 'The description continues. '.repeat(300); });
  await description.hover();
  await page.mouse.wheel(0,140);
  await expect.poll(() => description.evaluate(node => node.scrollTop)).toBeGreaterThan(0);
  await expect(page).toHaveURL('/');

  await page.mouse.move(20,160);
  await page.mouse.wheel(0,120);
  await page.evaluate(() => new Promise(resolve => requestAnimationFrame(resolve)));
  await expect(page).toHaveURL('/');
  await expect(board(page)).toHaveCount(0);
  await card(page).click();
  await begin(page).click();
  await page.mouse.move(20,160);
  await page.mouse.wheel(0,-120);
  await page.evaluate(() => new Promise(resolve => requestAnimationFrame(resolve)));
  await expect(page).toHaveURL(storyURL);
  await expect(page.locator('[data-item="name:Frame"]')).toBeVisible();
});

test('advancing after a Continue swipe still opens the next chapter introduction on reload', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await serveStory(page, fixture + '\n## Next chapter\nA new introduction.\n');
  await page.goto('/');
  await card(page).click();
  await begin(page).click();
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await page.mouse.move(20,150);
  await page.mouse.down();
  await page.mouse.move(20,410,{steps:4});
  await page.mouse.up();
  await expect(page).toHaveURL(/\/index.html$/);
  await expect(card(page)).toContainText('Continue');
  await page.mouse.move(20,420);
  await page.mouse.down();
  await page.mouse.move(20,150,{steps:4});
  await page.mouse.up();
  await expect(page.locator('[data-item="name:Kit"]')).toBeVisible();
  await expect(page.locator('dialog')).toHaveCount(0);
  await page.getByRole('button',{name:'Continue story'}).click();
  await expect(page.getByRole('dialog')).toContainText('A new introduction.');
  await page.reload();
  await expect(page.getByRole('dialog')).toContainText('A new introduction.');
});
