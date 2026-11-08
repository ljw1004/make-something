import {test, expect, type Page} from '@playwright/test';

// Lossless 195×422 WebP: red for 1s, green for 1s, loop count 1.
const once = Buffer.from('UklGRpwAAABXRUJQVlA4WAoAAAACAAAAwgAApQEAQU5JTQYAAAD/////AQBBTk1GNAAAAAAAAAAAAMIAAKUBAOgDAAJWUDhMGwAAAC/CQGkAB1CPctej/wEBSdL//2RE/zP+83+bAABBTk1GNAAAAAAAAAAAAMIAAKUBAOgDAABWUDhMGwAAAC/CQGkAB1DaepSn/wEBSdL//2RE/zP+83+bAAA=', 'base64');
const manuscript = `# A gift
## Assembly
background: ![workshop](assets/room.svg)
**Goals**
- Finish -- C
**Items**
- A
- B
- C
**Combinations**
- A [consume] + B [transform] -> C
## The gift
background: ![settled final pose](assets/poster.svg)
background animation: ![the gift changes hands](assets/once.webp)`;

async function open(page: Page, options: {wait?: Promise<void>; missing?: boolean; text?: string} = {}) {
  await page.route('**/scene-animation/story.md', route => route.fulfill({contentType: 'text/markdown', body: options.text ?? manuscript}));
  await page.route('**/scene-animation/assets/*.svg', route => route.fulfill({contentType: 'image/svg+xml', body: `<svg xmlns="http://www.w3.org/2000/svg" width="780" height="1688"><rect width="780" height="1688" fill="${route.request().url().endsWith('poster.svg') ? 'rgb(30,180,60)' : '#fff'}"/></svg>`}));
  await page.route('**/scene-animation/assets/once.webp', async route => {
    await options.wait;
    return options.missing ? route.fulfill({status: 404, body: 'Missing animation'}) : route.fulfill({contentType: 'image/webp', body: once});
  });
  await page.goto('/make-something.html?story=scene-animation/story.md');
  await expect(page.locator('.scene-art')).toHaveAttribute('src', /\.svg$/);
  await page.getByRole('button', {name: 'Start', exact: true}).click();
}
async function complete(page: Page) {
  await page.locator('[data-item="name:A"]').dragTo(page.locator('[data-item="name:B"]'));
  await page.getByRole('button', {name: 'Continue story'}).click();
}
const ending = (page: Page) => page.locator('.scene-panel[data-chapter="1"] .scene-art');
async function pixel(page: Page) {
  const screenshot = await page.screenshot({clip: {x: 190, y: 180, width: 1, height: 1}});
  return page.evaluate(async base64 => {
    const image = await createImageBitmap(new Blob([Uint8Array.from(atob(base64), c => c.charCodeAt(0))], {type: 'image/png'}));
    const canvas = document.createElement('canvas'); canvas.width = canvas.height = 1;
    const context = canvas.getContext('2d')!; context.drawImage(image, 0, 0);
    return [...context.getImageData(0, 0, 1, 1).data].slice(0, 3);
  }, screenshot.toString('base64'));
}

test('a preloaded one-shot scene starts when displayed, finishes once and retains the settled frame through redraw', async ({page}) => {
  await open(page);
  // Let the speculative decode finish and exceed the complete animation duration.
  await page.waitForTimeout(2100);
  await complete(page);
  await expect(ending(page)).toHaveAttribute('src', /\/once.webp$/);
  expect(await pixel(page)).toEqual([220, 30, 30]);
  await expect.poll(() => pixel(page)).toEqual([30, 180, 60]);
  await page.waitForTimeout(1200);
  expect(await pixel(page)).toEqual([30, 180, 60]);
  const image = await ending(page).elementHandle();
  await page.setViewportSize({width: 400, height: 844});
  expect(await image!.evaluate(element => element.isConnected)).toBe(true);
  expect(await pixel(page)).toEqual([30, 180, 60]);
});

test('a delayed scene waits for decode and keeps poster geometry when its lower-resolution animation appears', async ({page}) => {
  let release!: () => void;
  const wait = new Promise<void>(resolve => {release = resolve;});
  await open(page, {wait});
  await complete(page);
  await expect(ending(page)).toHaveCount(0);
  release();
  await expect(ending(page)).toHaveAttribute('src', /\/once.webp$/);
  expect(await ending(page).evaluate(element => [(element as HTMLImageElement).naturalWidth, (element as HTMLImageElement).naturalHeight])).toEqual([195, 422]);
  const box = (await ending(page).boundingBox())!;
  expect([box.width, box.height]).toEqual([390, 844]);
  await page.emulateMedia({reducedMotion: 'reduce'});
  await expect(ending(page)).toHaveAttribute('src', /\/poster.svg$/);
  expect(await ending(page).boundingBox()).toEqual(box);
  expect(await pixel(page)).toEqual([30, 180, 60]);
  await page.emulateMedia({reducedMotion: 'no-preference'});
  await expect(ending(page)).toHaveAttribute('src', /\/once.webp$/);
  expect(await ending(page).boundingBox()).toEqual(box);
});

for (const missing of [false, true]) test(`${missing ? 'unavailable scene motion' : 'reduced motion'} presents the settled poster and survives reload`, async ({page}) => {
  if (!missing) await page.emulateMedia({reducedMotion: 'reduce'});
  await open(page, {missing});
  await complete(page);
  await expect(ending(page)).toHaveAttribute('src', /\/poster.svg$/);
  expect(await pixel(page)).toEqual([30, 180, 60]);
  const box = await ending(page).boundingBox();
  await page.reload();
  await expect(ending(page)).toHaveAttribute('src', /\/poster.svg$/);
  expect(await ending(page).boundingBox()).toEqual(box);
});

test('animated scenes keep authored hotspot pixels and scene framing tied to the static poster', async ({page}) => {
  const text = manuscript.replace('background: ![workshop](assets/room.svg)', 'background: ![settled pose](assets/poster.svg)\nbackground animation: ![moving scene](assets/once.webp)')
    .replace('**Items**', '**Hotspots**\n- Bench (center 390px, 844px)\n**Items**\n- Bench');
  await open(page, {text});
  const hotspot = page.locator('[data-hotspot="name:Bench"]'), scene = page.locator('.scene-art');
  await expect(scene).toHaveAttribute('src', /\/once.webp$/);
  const box = (await hotspot.boundingBox())!;
  expect(box.x + box.width/2).toBeCloseTo(195, 1);
  expect(box.y + box.height/2).toBeCloseTo(422, 1);
  await page.emulateMedia({reducedMotion: 'reduce'});
  await expect(scene).toHaveAttribute('src', /\/poster.svg$/);
  expect(await hotspot.boundingBox()).toEqual(box);
});
