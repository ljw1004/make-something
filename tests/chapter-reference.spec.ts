import {test, expect, type Page} from '@playwright/test';

const manuscript = `# Plans
## First
background: ![room](room.svg)
reference: ![A wind cart](assets/cart.svg)
Fit the first assembly.
**Goals**
- Build -- C
**Items**
- A
- B
- C
**Combinations**
- A + B -> C
## Second
reference: ![A flying cart](assets/flying.svg)
Add the next part.
**Goals**
- Finish -- E
**Items**
- D
- E
**Combinations**
- C + D -> E`;

async function open(page: Page) {
  await page.route('**/reference-fixture/story.md', r => r.fulfill({contentType: 'text/markdown', body: manuscript}));
  await page.route('**/reference-fixture/**/*.svg', r => r.fulfill({contentType: 'image/svg+xml', body: `<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844"><rect width="390" height="844" fill="#e5eee4"/><circle cx="195" cy="220" r="80" fill="#c9704a"/></svg>`}));
  await page.goto('/make-something.html?story=reference-fixture/story.md');
  await page.getByRole('button', {name: 'Start', exact: true}).click();
  await page.getByRole('button', {name: 'Begin', exact: true}).click();
}

const saved = (page: Page) => page.evaluate(() => JSON.parse(Object.entries(localStorage).find(([key]) => key.startsWith('combination-progress-v2:'))![1]).state);
async function clearOfReference(page: Page, chapter: number) {
  const panel = page.locator(`.chapter-panel[data-chapter="${chapter}"]`), card = (await panel.locator('.chapter-reference').boundingBox())!;
  for (const item of await panel.locator('[data-item]').all()) {
    const box = (await item.boundingBox())!;
    expect(Math.min(box.x + box.width, card.x + card.width) <= Math.max(box.x, card.x) + .1 || Math.min(box.y + box.height, card.y + card.height) <= Math.max(box.y, card.y) + .1).toBe(true);
  }
}

test('reference picture is a non-draggable reading control with relative assets and no gameplay side effects', async ({page}) => {
  await page.setViewportSize({width: 390, height: 664});
  await open(page);
  const card = page.getByRole('button', {name: 'View build reference: A wind cart'});
  await expect(card).toBeVisible();
  await expect(card.locator('img')).toHaveAttribute('src', /reference-fixture\/assets\/cart.svg$/);
  await expect(card.locator('img')).toHaveAttribute('draggable', 'false');
  expect(await card.getAttribute('data-item')).toBeNull();
  expect(await card.getAttribute('data-hotspot')).toBeNull();
  await clearOfReference(page, 0);
  const before = await saved(page), bounds = await card.boundingBox();
  await page.mouse.move(bounds!.x + 45, bounds!.y + 44);
  await page.mouse.down();
  await page.mouse.move(bounds!.x - 80, bounds!.y + 170, {steps: 5});
  await page.mouse.up();
  expect(await card.boundingBox()).toEqual(bounds);
  expect(await saved(page)).toEqual(before);
  await card.click();
  await expect(page.getByRole('dialog', {name: 'Build reference'})).toBeVisible();
  await expect(page.locator('.reference-reading img')).toHaveAttribute('alt', 'A wind cart');
  expect((await page.locator('.reference-reading img').boundingBox())!.width).toBeGreaterThan(250);
  await page.getByRole('button', {name: 'Close', exact: true}).click();
  expect(await saved(page)).toEqual(before);
  expect(await card.boundingBox()).toEqual(bounds);
  await page.reload();
  await expect(card).toBeVisible();
  expect(await saved(page)).toEqual(before);
});

test('carried arrivals avoid the next reference and scrollback opens its own picture', async ({page}) => {
  await open(page);
  await page.locator('[data-item="name:A"]').dragTo(page.locator('[data-item="name:B"]'));
  await page.getByRole('button', {name: 'Continue story'}).click();
  await page.getByRole('button', {name: 'Begin', exact: true}).click();
  await clearOfReference(page, 1);
  await expect(page.locator('[data-item="name:C"]')).toBeVisible();
  await page.getByRole('button', {name: 'View build reference: A flying cart'}).click();
  await expect(page.locator('.reference-reading img')).toHaveAttribute('src', /assets\/flying.svg$/);
  await page.getByRole('button', {name: 'Close', exact: true}).click();
  await page.locator('.viewport').evaluate(el => {el.scrollTop = 0;});
  await page.getByRole('button', {name: 'View build reference: A wind cart'}).click();
  await expect(page.locator('.reference-reading img')).toHaveAttribute('src', /assets\/cart.svg$/);
  expect((await saved(page)).chapter).toBe(1);
});

test('reference framing follows the fitted scene on a desktop editor layout', async ({page}) => {
  await page.setViewportSize({width: 1280, height: 800});
  await open(page);
  const panel = (await page.locator('.chapter-panel').boundingBox())!, card = (await page.locator('.chapter-reference').boundingBox())!;
  const scale = panel.width / 390;
  expect(card.width).toBeCloseTo(196 * scale, 1);
  expect(card.x - panel.x).toBeCloseTo(146 * scale, 1);
  expect(card.y - panel.y).toBeCloseTo(12 * scale, 1);
  await clearOfReference(page, 0);
});

test.describe('touch reference reading', () => {
  test.use({viewport: {width: 320, height: 740}, isMobile: true, hasTouch: true});
  test('tap enlarges the card without picking up an item on a narrow cropped scene', async ({page}) => {
    await open(page);
    const before = await saved(page);
    await clearOfReference(page, 0);
    await page.getByRole('button', {name: 'View build reference: A wind cart'}).tap();
    await expect(page.getByRole('dialog', {name: 'Build reference'})).toBeVisible();
    await page.getByRole('button', {name: 'Close', exact: true}).tap();
    expect(await saved(page)).toEqual(before);
  });
});
