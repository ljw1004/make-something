import {test, expect, type Page} from '@playwright/test';
import {jumpToChapter} from './debug-helpers.ts';

const manuscript = `# Wind workshop
## Assembly
background: ![room](assets/room.svg)
reference: ![Wind cart](assets/cart.svg)
Build the cart.
**Goals**
- Finish -- \`cart\`
**Items**
- Rod
  - icon: ![rod](assets/rod.svg) (center 130px, 260px)
- Axle
  - icon: ![axle](assets/axle.svg) (center 260px, 260px)
- \`cart\` Wind cart
  - icon: ![cart](assets/cart.svg)
  - animation: ![turning cart](assets/loop.svg)
  - from chapter "Faster" animation: ![faster cart](assets/fast.svg)
  - from chapter "Rest" animation: none
**Combinations**
- Rod [consume] + Axle [transform] -> \`cart\`
## Faster
**Goals**
- Add the flag -- Flagged
**Items**
- Flag
  - icon: ![flag](assets/axle.svg)
- Flagged
  - icon: ![flagged](assets/cart.svg)
**Combinations**
- \`cart\` [preserve] + Flag [transform] -> Flagged
## Rest
All done.`;

async function open(page: Page, options: {missing?: boolean; waitForLoop?: Promise<void>; fitted?: boolean; text?: string} = {}) {
  await page.route('**/animation-fixture/story.md', route => route.fulfill({contentType: 'text/markdown', body: options.text ?? manuscript}));
  await page.route('**/animation-fixture/assets/*.svg', async route => {
    const file = new URL(route.request().url()).pathname.split('/').at(-1)!;
    if (file === 'loop.svg') {
      await options.waitForLoop;
      if (options.missing) return route.fulfill({status: 404, body: 'Missing loop'});
    }
    const [width, height] = file === 'room.svg' ? [390, options.fitted ? 320 : 844] : file === 'cart.svg' ? [400, 240] : file === 'rod.svg' ? [16, 240] : file === 'axle.svg' ? [176, 80] : [80, 48];
    return route.fulfill({contentType: 'image/svg+xml', body: `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}"><rect width="${width}" height="${height}" fill="${file === 'room.svg' ? '#fff' : '#b67c3b'}"/></svg>`});
  });
  await page.goto('/make-something.html?story=animation-fixture/story.md');
  await page.getByRole('button', {name: 'Start', exact: true}).click();
  await page.getByRole('button', {name: 'Begin', exact: true}).click();
}

const cart = (page: Page) => page.locator('[data-item="id:cart"]');
const make = (page: Page) => page.locator('[data-item="name:Rod"]').dragTo(page.locator('[data-item="name:Axle"]'));

test('completed loops decode before the result appears, keep poster size and leave reference pictures still', async ({page}) => {
  let release!: () => void;
  const waitForLoop = new Promise<void>(resolve => {release = resolve;});
  await open(page, {waitForLoop});
  await make(page);
  await expect(cart(page)).toHaveCount(0);
  await expect(page.locator('[data-item="name:Rod"]')).toBeVisible();
  release();
  await expect(cart(page).locator('.item-icon')).toHaveAttribute('src', /\/loop.svg$/);
  expect(await cart(page).evaluate(element => [element.clientWidth, element.clientHeight])).toEqual([100, 60]);
  expect(await cart(page).locator('img').evaluate(image => [(image as HTMLImageElement).naturalWidth, (image as HTMLImageElement).naturalHeight])).toEqual([80, 48]);
  await expect(page.getByRole('button', {name: 'Continue story'})).toBeVisible();
  await expect(page.locator('.chapter-reference img')).toHaveAttribute('src', /\/cart.svg$/);
  await page.getByRole('button', {name: 'View build reference: Wind cart'}).click();
  await expect(page.locator('.reference-reading img')).toHaveAttribute('src', /\/cart.svg$/);
  await page.getByRole('button', {name: 'Close', exact: true}).click();
  await page.reload();
  await expect(cart(page).locator('.item-icon')).toHaveAttribute('src', /\/loop.svg$/);
  expect(await cart(page).evaluate(element => [element.clientWidth, element.clientHeight])).toEqual([100, 60]);
});

test('reduced motion swaps the connected image to its still poster without moving a held object', async ({page}) => {
  await open(page);
  await make(page);
  await expect(cart(page).locator('.item-icon')).toHaveAttribute('src', /\/loop.svg$/);
  const image = await cart(page).locator('.item-icon').elementHandle();
  const box = (await cart(page).boundingBox())!;
  await page.mouse.move(box.x + 10, box.y + 10); await page.mouse.down();
  await page.mouse.move(190, 500, {steps: 5});
  const held = await cart(page).boundingBox();
  await page.emulateMedia({reducedMotion: 'reduce'});
  await expect(cart(page).locator('.item-icon')).toHaveAttribute('src', /\/cart.svg$/);
  expect(await cart(page).boundingBox()).toEqual(held);
  expect(await image!.evaluate(element => element.isConnected)).toBe(true);
  await page.mouse.up();
  await page.reload();
  await expect(cart(page).locator('.item-icon')).toHaveAttribute('src', /\/cart.svg$/);
  await page.emulateMedia({reducedMotion: 'no-preference'});
  await expect(cart(page).locator('.item-icon')).toHaveAttribute('src', /\/loop.svg$/);
});

test('unavailable loops keep the static poster and a usable completed result', async ({page}) => {
  await open(page, {missing: true});
  await make(page);
  await expect(cart(page).locator('.item-icon')).toHaveAttribute('src', /\/cart.svg$/);
  await expect(cart(page)).toHaveClass(/icon-thing/);
  expect(await cart(page).evaluate(element => [element.clientWidth, element.clientHeight])).toEqual([100, 60]);
  await expect(page.getByRole('button', {name: 'Continue story'})).toBeVisible();
});

test('chapter loop selection and explicit still overrides update carried items and earlier checkpoints', async ({page}) => {
  await open(page);
  await make(page);
  await page.getByRole('button', {name: 'Continue story'}).click();
  await expect(cart(page).locator('.item-icon')).toHaveAttribute('src', /\/fast.svg$/);
  await jumpToChapter(page, 'Rest');
  await page.getByRole('button', {name: 'Begin', exact: true}).click();
  await expect(cart(page).locator('.item-icon')).toHaveAttribute('src', /\/cart.svg$/);
  await jumpToChapter(page, 'Faster');
  await expect(cart(page).locator('.item-icon')).toHaveAttribute('src', /\/fast.svg$/);
});

for (const local of [false, true]) test(`fixed results ${local ? 'honour chapter-local artwork even when its URL matches the poster' : 'animate their default item artwork'}`, async ({page}) => {
  const text = manuscript.replace('**Goals**', `**Hotspots**\n- \`cart\` (center 195px, 500px)\n${local ? '  - icon: ![still cart](assets/cart.svg)\n' : ''}**Goals**`);
  await open(page, {text});
  await make(page);
  const fixed = page.locator('[data-hotspot="id:cart"]');
  await expect(fixed.locator('.item-icon')).toHaveAttribute('src', local ? /\/cart.svg$/ : /\/loop.svg$/);
  expect(await fixed.evaluate(element => [element.clientWidth, element.clientHeight])).toEqual([100, 60]);
  await expect(cart(page)).toHaveCount(0);
});

test.describe('thin parts on narrow touch screens', () => {
  test.use({viewport: {width: 320, height: 740}, isMobile: true, hasTouch: true, reducedMotion: 'reduce'});
  for (const fitted of [false, true]) test(`a rod keeps a 44px hit width in a ${fitted ? 'fitted' : 'cropped'} scene without growing its drawing`, async ({page}) => {
    await open(page, {fitted});
    const rod = page.locator('[data-item="name:Rod"]'), axle = page.locator('[data-item="name:Axle"]');
    const box = (await rod.boundingBox())!, target = (await axle.boundingBox())!;
    expect(box.width).toBeLessThan(4);
    const hit = await rod.evaluate(element => {
      const box = element.getBoundingClientRect(), style = getComputedStyle(element, '::before'), scale = box.width / element.clientWidth;
      return {width: parseFloat(style.width) * scale, height: parseFloat(style.height) * scale,
        left: document.elementFromPoint(box.x + box.width/2 - 21, box.y + box.height/2)?.closest('[data-item]') === element,
        right: document.elementFromPoint(box.x + box.width/2 + 21, box.y + box.height/2)?.closest('[data-item]') === element};
    });
    expect(hit.width).toBeGreaterThanOrEqual(43.9); expect(hit.height).toBeGreaterThanOrEqual(43.9);
    expect(hit.left && hit.right).toBe(true);
    const session = await page.context().newCDPSession(page);
    const start = {x: box.x + box.width/2 + 20, y: box.y + box.height/2};
    await session.send('Input.dispatchTouchEvent', {type: 'touchStart', touchPoints: [start]});
    for (let step = 1; step <= 6; step++) await session.send('Input.dispatchTouchEvent', {type: 'touchMove', touchPoints: [{x: start.x + (target.x + target.width/2 - start.x)*step/6, y: start.y + (target.y + target.height/2 - start.y)*step/6}]});
    await session.send('Input.dispatchTouchEvent', {type: 'touchEnd', touchPoints: []});
    await expect(cart(page)).toBeVisible();
  });
});
