import {test, expect, type CDPSession, type Page} from '@playwright/test';

type Appearance = 'text' | 'artwork' | 'hitbox';
const manuscript = `# Hotspot gestures
## Workshop
background: ![room](room.svg)
Build a kit.
**Goals**
- Build -- Kit
**Items**
- Frame
- Tool
**Combinations**
- Frame [preserve] + Tool [preserve] -> Kit
## Field
background: ![room](room.svg)
Work at the station.
**Hotspots**
- Station (center 195px, 320px)
**Goals**
- Finish -- Final
**Items**
- Kit
- Probe
- Station

  A fixed station for working.

- Final
**Combinations**
- Kit [preserve] @ Station -> Final
`;

async function enterField(page: Page, appearance: Appearance = 'text') {
  const source = manuscript.replace('- Station (center 195px, 320px)',
    '- Station (center 195px, 320px)'
    + (appearance === 'text' ? '' : '\n  - icon: ![station](station.svg)')
    + (appearance === 'hitbox' ? '\n  - hitbox: (center 195px, 320px) (size 144px, 112px)' : ''));
  await page.route('**/hotspot-gestures/story.md', route => route.fulfill({contentType: 'text/markdown', body: source}));
  await page.route('**/hotspot-gestures/*.svg', route => {
    const [width, height] = route.request().url().endsWith('room.svg') ? [390, 844] : [320, 240];
    return route.fulfill({contentType: 'image/svg+xml', body: `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}"><rect width="${width}" height="${height}" fill="tan"/></svg>`});
  });
  await page.emulateMedia({reducedMotion: 'reduce'});
  await page.goto('/make-something.html?story=hotspot-gestures/story.md');
  await page.getByRole('button', {name: 'Start', exact: true}).click();
  await page.getByRole('button', {name: 'Begin', exact: true}).click();
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await page.getByRole('button', {name: 'Continue story'}).click();
  await page.getByRole('button', {name: 'Begin', exact: true}).click();
  await expect.poll(() => scrollTop(page)).toBe(844);
}

const station = (page: Page) => page.locator('[data-hotspot="name:Station"]');
const scrollTop = (page: Page) => page.locator('.viewport').evaluate(el => el.scrollTop);
const centre = (box: {x: number; y: number; width: number; height: number}) => ({x: box.x + box.width / 2, y: box.y + box.height / 2});

async function swipe(cdp: CDPSession, page: Page, start: {x: number; y: number}) {
  await cdp.send('Input.dispatchTouchEvent', {type: 'touchStart', touchPoints: [start]});
  for (let dy = 20; dy <= 240; dy += 20) {
    await cdp.send('Input.dispatchTouchEvent', {type: 'touchMove', touchPoints: [{x: start.x, y: start.y + dy}]});
    await page.waitForTimeout(16);
  }
  await cdp.send('Input.dispatchTouchEvent', {type: 'touchEnd', touchPoints: []});
}

for (const appearance of ['text', 'artwork', 'hitbox'] as const) test(`${appearance} hotspot touch drags stay fixed while background swipes still scroll`, async ({browser}) => {
  const context = await browser.newContext({baseURL: 'http://127.0.0.1:5173', viewport: {width: 390, height: 844}, isMobile: true, hasTouch: true});
  try {
    const page = await context.newPage();
    await enterField(page, appearance);
    const hotspot = station(page), box = (await hotspot.boundingBox())!;
    // The custom receiver includes space outside the artwork; that space owns
    // the gesture too. Other variants exercise the hotspot's visible centre.
    const start = appearance === 'hitbox' ? {x: box.x + 5, y: box.y + box.height / 2} : centre(box);
    const cdp = await context.newCDPSession(page);
    await swipe(cdp, page, start);
    expect(await scrollTop(page)).toBe(844);
    expect(await hotspot.boundingBox()).toEqual(box);
    await expect(page.locator('dialog')).toHaveCount(0);
    await expect(page.locator('.dragging')).toHaveCount(0);
    // An attempted drag must not prime a double-tap; two actual taps still read.
    await hotspot.tap();
    await expect(page.locator('dialog')).toHaveCount(0);
    await hotspot.tap();
    await expect(page.locator('.encyclopedia-detail .reading-text')).toHaveText('A fixed station for working.');
    await page.getByRole('button', {name: 'Close', exact: true}).tap();
    const empty = {x: 2, y: 300};
    expect(await page.evaluate(point => !!document.elementFromPoint(point.x, point.y)?.closest('[data-item],[data-hotspot]'), empty)).toBe(false);
    await swipe(cdp, page, empty);
    await expect.poll(() => scrollTop(page)).toBeLessThan(844);
  } finally { await context.close(); }
});

test('hotspot mouse travel, including release-only and returning travel, never counts as a double-click', async ({page}) => {
  await page.clock.install({time: new Date('2026-11-07T12:00:00Z')});
  await enterField(page);
  await page.clock.pauseAt(new Date('2026-11-07T12:10:00Z'));
  const hotspot = station(page), box = (await hotspot.boundingBox())!, start = centre(box);
  const cdp = await page.context().newCDPSession(page);
  for (const travel of ['outward', 'returning', 'release-only']) {
    await hotspot.click();
    await cdp.send('Input.dispatchMouseEvent', {type: 'mousePressed', ...start, button: 'left', buttons: 1, clickCount: 1});
    if (travel !== 'release-only') await cdp.send('Input.dispatchMouseEvent', {type: 'mouseMoved', x: start.x, y: start.y + 180, button: 'left', buttons: 1});
    await cdp.send('Input.dispatchMouseEvent', {type: 'mouseReleased', x: start.x, y: start.y + (travel === 'returning' ? 0 : 180), button: 'left', buttons: 0, clickCount: 1});
    await expect(page.locator('dialog')).toHaveCount(0);
    expect(await scrollTop(page)).toBe(844);
    expect(await hotspot.boundingBox()).toEqual(box);
    // The attempted drag also clears the first click from the double-tap pair.
    await hotspot.click();
    await expect(page.locator('dialog')).toHaveCount(0);
    await page.clock.runFor(500);
  }
  await hotspot.click();
  await page.mouse.move(start.x, start.y); await page.mouse.down();
  await page.mouse.move(start.x + 2, start.y + 1); await page.mouse.up();
  await expect(page.locator('.encyclopedia-detail .reading-text')).toHaveText('A fixed station for working.');
});

for (const interruption of ['pointercancel', 'blur', 'resize', 'lostpointercapture']) test(`${interruption} releases a hotspot gesture without leaving feedback or a pending click`, async ({page}) => {
  await enterField(page);
  const hotspot = station(page), start = centre((await hotspot.boundingBox())!);
  await page.mouse.move(start.x, start.y); await page.mouse.down();
  await expect(hotspot).toHaveClass(/pressed/);
  if (interruption === 'resize') await page.setViewportSize({width: 390, height: 800});
  else if (interruption === 'blur') await page.evaluate(() => window.dispatchEvent(new Event('blur')));
  else await page.locator('#app').dispatchEvent(interruption, {pointerId: 1, pointerType: 'mouse', buttons: 1});
  await expect.poll(() => page.locator('#app').evaluate(el => el.hasPointerCapture(1))).toBe(false);
  // Resize can restore ordinary hover beneath the pointer. Leave the hotspot
  // before checking that the cancelled press has no lingering feedback.
  await page.mouse.move(2, 300); await page.mouse.up();
  await expect(hotspot).not.toHaveClass(/pressed/);
  await expect(page.locator('dialog')).toHaveCount(0);
  await hotspot.click();
  await expect(page.locator('dialog')).toHaveCount(0);
  await hotspot.click();
  await expect(page.locator('.encyclopedia-detail .reading-text')).toHaveText('A fixed station for working.');
});
