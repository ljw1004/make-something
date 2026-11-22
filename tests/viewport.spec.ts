import {test, expect, type Page} from '@playwright/test';

const manuscript = `# Viewport
## Workshop
background: ![room](room.svg)

An opening reading.
**Goals**
- Build -- Kit
**Items**
- Frame
- Tool
**Combinations**
- Frame [preserve] + Tool [preserve] -> Kit
## Field
background: ![field](field.svg)

A second reading.
**Goals**
- Finish -- Final
**Items**
- Kit
- Probe
**Combinations**
- Kit [preserve] + Probe [preserve] -> Final
- Frame [preserve] + Probe [preserve] -> Offcut
## Home
A last reading.
**Goals**
- Pack -- Packed
**Items**
- Final
- Bag
**Combinations**
- Final [preserve] + Bag [preserve] -> Packed
`;

async function openFixture(page: Page) {
  await page.route('**/viewport/story.md', route => route.fulfill({contentType: 'text/markdown', body: manuscript}));
  await page.route('**/viewport/*.svg', route => route.fulfill({contentType: 'image/svg+xml', body: `<svg xmlns="http://www.w3.org/2000/svg" width="780" height="1688"><defs><pattern id="grid" width="78" height="84.4" patternUnits="userSpaceOnUse"><rect width="78" height="84.4" fill="#d6dbc2"/><path d="M0 84.4V0H78" fill="none" stroke="#345" stroke-width="5"/></pattern></defs><rect width="780" height="1688" fill="url(#grid)"/><circle cx="390" cy="120" r="80" fill="#e8b465"/></svg>`}));
  await page.goto('/index.html?story=viewport/story.md');
  await expect(page.getByRole('button', {name: 'Start', exact: true})).toBeVisible();
}

async function expectCurrentFits(page: Page, count: number) {
  const {width,height} = page.viewportSize()!;
  await expect.poll(() => page.locator('.viewport').evaluate(el => ({width: el.clientWidth, total: el.scrollWidth, left: el.scrollLeft})))
    .toEqual({width, total: count * width, left: (count - 1) * width});
  // CSS resizes the viewport before the resize handler updates the chapter scene.
  const panel = page.locator('.chapter-panel').last();
  await expect.poll(async () => (await panel.boundingBox())?.height).toBeCloseTo(height, 1);
  expect((await panel.boundingBox())!.y).toBeCloseTo(0, 1);
  expect(await page.evaluate(() => document.documentElement.scrollHeight <= innerHeight && document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  // The viewport ends at the active scene.
  expect(await page.locator('.viewport').evaluate(el => { el.scrollLeft += 1000; return el.scrollLeft; })).toBe((count - 1) * width);
}

async function enterField(page: Page) {
  await page.emulateMedia({reducedMotion: 'reduce'});
  await openFixture(page);
  await page.getByRole('button', {name:'Start',exact:true}).click();
  await page.getByRole('button', {name:'Begin',exact:true}).click();
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await page.getByRole('button', {name:'Continue story'}).click();
  await page.getByRole('button', {name:'Begin',exact:true}).click();
  await expectCurrentFits(page, 2);
}

async function pickup(page: Page, id: string) {
  const box = (await page.locator(`[data-item="name:${id}"]`).boundingBox())!;
  await page.mouse.move(box.x + 10, box.y + 10);
  await page.mouse.down();
}

const scrollLeft = (page: Page) => page.locator('.viewport').evaluate(el => el.scrollLeft);
async function scrollTo(page: Page, top: number) {
  await page.locator('.viewport').evaluate((el, top) => { el.scrollLeft = top; }, top);
  await expect.poll(() => scrollLeft(page)).toBe(top);
}

async function timedField(page: Page) {
  await page.setViewportSize({width:390,height:664});
  await page.clock.install({time: new Date('2026-11-01T12:00:00Z')});
  await enterField(page);
  await page.clock.pauseAt(new Date('2026-11-01T12:10:00Z'));
}

test('latest-chapter pickups follow the pointer past the top, fit on release and never change chapters', async ({page}) => {
  await timedField(page);
  const kit = page.locator('[data-item="name:Kit"]');
  await pickup(page, 'Kit');
  await page.mouse.move(150, 1, {steps: 8});
  await page.clock.runFor(1000);
  expect(await scrollLeft(page)).toBe(390);
  expect((await kit.boundingBox())!.y).toBeCloseTo(-9, 1);
  await page.mouse.up();
  expect((await kit.boundingBox())!.y).toBeCloseTo(0, 1);

  // Release coordinates still obey the pickup restriction when no move arrives
  // after a deliberate scroll exposes the older panel.
  await pickup(page, 'Kit');
  await page.mouse.move(170, 100);
  await scrollTo(page, 300);
  await page.mouse.up();
  await expect(page.locator('.chapter-panel[data-chapter="1"] [data-item="name:Kit"]')).toHaveCount(1);
  await scrollTo(page, 390);
  expect((await kit.boundingBox())!.y).toBeCloseTo(90, 1);
  await page.clock.resume();
  // Let the native scroll event save the final position before navigating away.
  await expect.poll(()=>page.evaluate(()=>{
    const key=Object.keys(localStorage).find(key=>key.startsWith('combination-progress-v2:'));
    return key?JSON.parse(localStorage.getItem(key)!).anchor.chapterView:undefined;
  })).toBe(1);
  await page.reload();
  await expectCurrentFits(page, 2);
  expect((await kit.boundingBox())!.y).toBeCloseTo(90, 1);
});

test('older pickups scroll after an edge hold, remain free until dropped, then lock on pickup and reset with the chapter', async ({page}) => {
  await timedField(page);
  await scrollTo(page, 0);
  await pickup(page, 'Frame');
  await page.mouse.move(389, 380);
  await page.clock.runFor(200);
  expect(await scrollLeft(page)).toBe(0);
  // Leaving the edge resets the hold, even when returning to the same edge.
  await page.mouse.move(120, 400);
  await page.clock.runFor(500);
  expect(await scrollLeft(page)).toBe(0);
  await page.mouse.move(389, 380);
  await page.clock.runFor(200);
  expect(await scrollLeft(page)).toBe(0);
  await page.clock.runFor(400);
  expect(await scrollLeft(page)).toBeGreaterThan(0);
  // No extra move events are needed to keep scrolling or update the dragged tile.
  await page.clock.runFor(1800);
  expect(await scrollLeft(page)).toBe(390);
  const frame = page.locator('[data-item="name:Frame"]');
  const atRight = (await frame.boundingBox())!;
  expect(atRight.x).toBeCloseTo(379, 1);
  expect(atRight.x + atRight.width).toBeGreaterThan(390);
  // Visiting the latest panel mid-gesture does not lock an older pickup.
  await page.mouse.move(1, 380);
  await page.clock.runFor(200);
  expect(await scrollLeft(page)).toBe(390);
  await page.clock.runFor(1800);
  expect(await scrollLeft(page)).toBe(0);
  await page.mouse.move(389, 380);
  await page.clock.runFor(2000);
  expect(await scrollLeft(page)).toBe(390);
  await page.mouse.move(70, 180);
  const preview = await frame.boundingBox();
  await page.mouse.up();
  await expect(page.locator('.chapter-panel[data-chapter="1"] [data-item="name:Frame"]')).toHaveCount(1);
  expect(await frame.boundingBox()).toEqual(preview);
  await page.clock.runFor(1000);
  expect(await scrollLeft(page)).toBe(390);
  await page.clock.resume();
  await page.reload();
  await expectCurrentFits(page, 2);
  await pickup(page, 'Frame');
  await page.mouse.move(1, 200, {steps: 4});
  await page.waitForTimeout(400);
  expect(await scrollLeft(page)).toBe(390);
  await page.mouse.up();
  await expect(page.locator('.chapter-panel[data-chapter="1"] [data-item="name:Frame"]')).toHaveCount(1);
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Probe"]'));
  await expect(page.locator('[data-item="name:Offcut"]')).toBeVisible();
  await page.getByRole('button', {name:'Read this chapter'}).click();
  await page.getByRole('button', {name:'Restart chapter'}).click();
  await page.getByRole('button', {name:'Begin',exact:true}).click();
  await expectCurrentFits(page, 2);
  await expect(page.locator('.chapter-panel[data-chapter="0"] [data-item="name:Frame"]')).toHaveCount(1);
});

test('leaving either edge settles by distance while the item stays held', async ({page}) => {
  await timedField(page);
  await page.emulateMedia({reducedMotion:'no-preference'});
  await scrollTo(page, 0);
  await pickup(page, 'Frame');
  const held = page.locator('[data-item="name:Frame"].dragging');
  for (const {edge, from, to} of [{edge:389, from:0, to:390}, {edge:1, from:390, to:0}]) {
    for (const {hold, commits} of [{hold:350, commits:false}, {hold:420, commits:true}]) {
      await page.mouse.move(edge, 380);
      await page.clock.runFor(hold);
      const distance = Math.abs((await scrollLeft(page)) - from);
      expect(distance).toBeGreaterThan(commits ? 65 : 0);
      expect(distance).toBeLessThan(commits ? 97.5 : 65);
      await page.mouse.move(200, 380);
      await page.clock.runFor(95);
      const settling = Math.abs((await scrollLeft(page)) - from);
      expect(commits ? settling > distance : settling < distance).toBe(true);
      await page.clock.runFor(400);
      expect(await scrollLeft(page)).toBe(commits ? to : from);
      const tile = (await held.boundingBox())!;
      expect(tile.x).toBeCloseTo(190, 1);
      expect(tile.y).toBeCloseTo(370, 1);
    }
  }
  await page.mouse.up();
  await expect(page.locator('.chapter-panel[data-chapter="0"] [data-item="name:Frame"]')).toBeVisible();
});

for (const interruption of ['release', 'pointercancel', 'blur', 'resize']) test(`${interruption} stops an older item's ongoing edge scroll`, async ({page}) => {
  await timedField(page);
  await scrollTo(page, 0);
  await pickup(page, 'Frame');
  await page.mouse.move(389, 380);
  await page.clock.runFor(500);
  const scrolling = await scrollLeft(page);
  expect(scrolling).toBeGreaterThan(0);
  expect(scrolling).toBeLessThan(390);
  if (interruption === 'release') await page.mouse.up();
  else {
    if (interruption === 'resize') await page.setViewportSize({width:390,height:650});
    else if (interruption === 'blur') await page.evaluate(() => window.dispatchEvent(new Event('blur')));
    else await page.locator('#app').dispatchEvent('pointercancel', {pointerId: 1, pointerType: 'mouse'});
    // Viewport resizing schedules the browser's resize event; wait for its
    // cancellation before delivering a release that could otherwise win the race.
    await page.clock.runFor(50);
    await expect(page.locator('.is-dragging')).toHaveCount(0);
    await page.mouse.up();
  }
  await page.clock.runFor(50); // Let resize/scroll observers finish before checking for a leaked loop.
  const stopped = await scrollLeft(page);
  await page.clock.runFor(1000);
  expect(await scrollLeft(page)).toBe(stopped);
  await expect(page.locator('.is-dragging,.dragging')).toHaveCount(0);
  if (interruption !== 'release') await expect(page.locator('.chapter-panel[data-chapter="0"] [data-item="name:Frame"]')).toHaveCount(1);
});

test('cover and chapter use identical pixels and cannot scroll at short, reference and tall phone sizes', async ({page}) => {
  const sceneryOnly = '.story-start,.thing,.hud-stack,.debug-toggle,.tutorial-overlay {visibility:hidden!important}';
  for (const viewport of [{width:390,height:664}, {width:390,height:844}, {width:320,height:740}]) {
    await page.setViewportSize(viewport);
    await openFixture(page);
    await page.locator('.scene-art').evaluate((el: HTMLImageElement) => el.decode());
    await expectCurrentFits(page, 1);
    const image = await page.locator('.scene-art').elementHandle();
    const before = await page.locator('.world').screenshot({style: sceneryOnly});
    await page.getByRole('button', {name:'Start',exact:true}).click();
    await page.getByRole('button', {name:'Begin',exact:true}).click();
    expect(await image!.evaluate(el => el === document.querySelector('.scene-art'))).toBe(true);
    await expectCurrentFits(page, 1);
    const after = await page.locator('.world').screenshot({style: sceneryOnly});
    // PNG encodings may differ; compare pixels, allowing one colour level for raster rounding.
    const difference = await page.evaluate(async images => {
      const pixels = await Promise.all(images.map(async data => {
        const image = new Image(); image.src = `data:image/png;base64,${data}`; await image.decode();
        const canvas = document.createElement('canvas'); canvas.width = image.width; canvas.height = image.height;
        const context = canvas.getContext('2d')!; context.drawImage(image, 0, 0);
        return context.getImageData(0, 0, image.width, image.height).data;
      }));
      return pixels[0].reduce((max, value, i) => Math.max(max, Math.abs(value - pixels[1][i])), 0);
    }, [before.toString('base64'), after.toString('base64')]);
    expect(difference).toBeLessThanOrEqual(1);
    await page.evaluate(() => localStorage.clear());
  }
});

test('advancing and resizing keep the latest chapter at the right while scrollback remains available', async ({page}) => {
  await page.setViewportSize({width:390,height:664});
  await openFixture(page);
  await page.getByRole('button', {name:'Start',exact:true}).click();
  await page.getByRole('button', {name:'Begin',exact:true}).click();
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await page.getByRole('button', {name:'Continue story'}).click();
  await expectCurrentFits(page, 2);
  // Browser chrome changing height must also work with the chapter reading open.
  await page.setViewportSize({width:390,height:760});
  await expectCurrentFits(page, 2);
  await page.getByRole('button', {name:'Begin',exact:true}).click();
  await page.locator('[data-item="name:Kit"]').dragTo(page.locator('[data-item="name:Probe"]'));
  await page.getByRole('button', {name:'Continue story'}).click();
  await page.getByRole('button', {name:'Begin',exact:true}).click();
  await expectCurrentFits(page, 3);
  await page.setViewportSize({width:320,height:740});
  await expectCurrentFits(page, 3);
  await page.reload(); await expectCurrentFits(page, 3);
  await page.evaluate(() => {
    const key = Object.keys(localStorage).find(key => key.startsWith('combination-progress-v2:'))!;
    const saved = JSON.parse(localStorage.getItem(key)!);
    delete saved.anchor.chapterView; saved.anchor.viewportHeight = 740; saved.anchor.scrollTop = 740;
    localStorage.setItem(key, JSON.stringify(saved));
  });
  await page.reload();
  await expect.poll(() => scrollLeft(page)).toBe(320); // A saved vertical offset converts by its original panel height.
  await page.keyboard.press('ArrowLeft');
  await expect.poll(() => scrollLeft(page)).toBe(0);
  await expect(page.locator('.game-surface')).not.toHaveClass(/chapter-sliding/);
  await page.keyboard.press('ArrowRight');
  await expect.poll(() => page.locator('.viewport').evaluate(el => el.scrollLeft)).toBe(320);
  // Confirm the history view was recorded before resizing.
  await expect.poll(() => page.evaluate(() => {
    const key = Object.keys(localStorage).find(key => key.startsWith('combination-progress-v2:'))!;
    return JSON.parse(localStorage.getItem(key)!).anchor.chapterView;
  })).toBe(1);
  await page.setViewportSize({width:390,height:664});
  await expect.poll(() => page.locator('.viewport').evaluate(el => el.scrollLeft)).toBe(390);
  await page.reload();
  await expect.poll(() => page.locator('.viewport').evaluate(el => el.scrollLeft)).toBe(390);
  await page.keyboard.press('ArrowRight');
  await expectCurrentFits(page, 3);
  const final = page.locator('[data-item="name:Final"]'), source = (await final.boundingBox())!;
  await page.mouse.move(source.x+10,source.y+10); await page.mouse.down();
  await page.locator('.viewport').evaluate(el => { el.scrollLeft = 390; });
  await page.mouse.move(200,450,{steps:4}); await page.mouse.up();
  // Deliberately scrolling mid-gesture cannot move a latest-chapter item backwards.
  await expect(page.locator('.chapter-panel[data-chapter="2"] [data-item="name:Final"]')).toHaveCount(1);
  await page.locator('.viewport').evaluate(el => { el.scrollLeft = el.scrollWidth; });
  const moved = (await final.boundingBox())!;
  expect(moved.x).toBeCloseTo(0,1); expect(moved.y).toBeCloseTo(440,1);
});

test('wide movable artwork fits a cropped panel without changing its aspect ratio', async ({page}) => {
  await page.route('**/wide/story.md', route => route.fulfill({contentType:'text/markdown',body: manuscript.replace('- Frame\n','- Frame\n  - icon: ![frame](wide.svg)\n')}));
  await page.route('**/wide/wide.svg', route => route.fulfill({contentType:'image/svg+xml',body:'<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="240"><rect width="1440" height="240" fill="#765"/></svg>'}));
  await page.setViewportSize({width:320,height:844});
  await page.goto('/index.html?story=wide/story.md');
  await page.getByRole('button',{name:'Start',exact:true}).click();
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  const rect = (await page.locator('[data-item="name:Frame"]').boundingBox())!;
  expect(rect.x).toBeCloseTo(0,1); expect(rect.width).toBeCloseTo(320,1);
  expect(rect.width/rect.height).toBeCloseTo(6,2);
  await expectCurrentFits(page,1);
});

test('a tall narrow viewport keeps automatic text rows separate and unpositioned hotspots visible', async ({page}) => {
  await page.route('**/text-rows/story.md', route => route.fulfill({contentType:'text/markdown',body:`# Text rows
## Workshop
Fit the cabinet.
**Goals**
- Fit the cabinet -- Fitted cabinet @ Workshop wall
**Hotspots**
- Workshop wall
**Items**
- Workshop wall
- Wooden panel
- Cutting tool
- Metal fasteners
- Wooden shelf
- Cabinet frame
- Cabinet
- Fitted cabinet
**Combinations**
- Wooden panel [transform] + Cutting tool [preserve] -> Cabinet frame
- Cabinet frame [transform] + Metal fasteners [consume] -> Cabinet
- Cabinet [transform] + Wooden shelf [consume] -> Fitted cabinet
`}));
  await page.setViewportSize({width:320,height:844});
  await page.goto('/index.html?story=text-rows/story.md');
  await page.getByRole('button',{name:'Start',exact:true}).click();
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  const cards = await page.locator('[data-item]').evaluateAll(elements => elements.map(el => {
    const box = el.getBoundingClientRect(); return {left:box.left,right:box.right,top:box.top,bottom:box.bottom};
  }));
  const goals=(await page.locator('.hud-stack').boundingBox())!;
  for(const [i,card] of cards.entries()){
    expect(card.left).toBeGreaterThanOrEqual(0);expect(card.right).toBeLessThanOrEqual(320);
    expect(card.bottom).toBeLessThan(goals.y);
    for(const other of cards.slice(i+1))expect(card.right<=other.left||other.right<=card.left||card.bottom<=other.top||other.bottom<=card.top).toBe(true);
  }
  const hotspot = (await page.locator('[data-hotspot]').boundingBox())!;
  expect(hotspot.x).toBeGreaterThanOrEqual(0);
  expect(hotspot.x+hotspot.width).toBeLessThanOrEqual(320);
  await expectCurrentFits(page,1);
});

test('short-screen drops and resized saved items stay reachable without adding downward scroll', async ({page}) => {
  await page.setViewportSize({width:390,height:844});
  await openFixture(page);
  await page.getByRole('button', {name:'Start',exact:true}).click();
  await page.getByRole('button', {name:'Begin',exact:true}).click();
  const frame = page.locator('[data-item="name:Frame"]');
  await frame.dragTo(page.locator('.viewport'), {targetPosition:{x:389,y:843}});
  const original = (await frame.boundingBox())!;
  await page.setViewportSize({width:390,height:600});
  await expectCurrentFits(page, 1);
  const fitted = (await frame.boundingBox())!;
  expect(fitted.y + fitted.height).toBeCloseTo(600, 1);
  await page.setViewportSize({width:390,height:844});
  await expectCurrentFits(page, 1);
  expect(await frame.boundingBox()).toEqual(original);
  await page.setViewportSize({width:320,height:600});
  await expectCurrentFits(page, 1);
  await frame.dragTo(page.locator('.viewport'), {targetPosition:{x:1,y:599}});
  const moved = (await frame.boundingBox())!;
  expect(moved.x).toBeCloseTo(0, 1); expect(Math.abs(moved.y + moved.height - 600)).toBeLessThan(1);
  await page.reload(); await expectCurrentFits(page, 1);
  expect(await frame.boundingBox()).toEqual(moved);
});

test('phone swipes can revisit history but stop at the current chapter', async ({browser}) => {
  const context = await browser.newContext({viewport:{width:390,height:664},isMobile:true,hasTouch:true});
  try {
    const page = await context.newPage(); await openFixture(page);
    await page.getByRole('button', {name:'Start',exact:true}).tap();
    await page.getByRole('button', {name:'Begin',exact:true}).tap();
    const cdp = await context.newCDPSession(page);
    async function swipe(from: number, to: number) {
      await cdp.send('Input.dispatchTouchEvent', {type:'touchStart',touchPoints:[{x:from,y:110}]});
      for (let i = 1; i <= 12; i++) {
        await cdp.send('Input.dispatchTouchEvent', {type:'touchMove',touchPoints:[{x:from+(to-from)*i/12,y:110}]});
        await page.waitForTimeout(16);
      }
      await cdp.send('Input.dispatchTouchEvent', {type:'touchEnd',touchPoints:[]});
    }
    await swipe(350,60); await expectCurrentFits(page, 1);
    await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
    await page.getByRole('button', {name:'Continue story'}).tap();
    await page.getByRole('button', {name:'Begin',exact:true}).tap();
    await expectCurrentFits(page, 2);
    const kit = page.locator('[data-item="name:Kit"]'), box = (await kit.boundingBox())!;
    await cdp.send('Input.dispatchTouchEvent', {type:'touchStart',touchPoints:[{x:box.x+10,y:box.y+10}]});
    await cdp.send('Input.dispatchTouchEvent', {type:'touchMove',touchPoints:[{x:150,y:1}]});
    await page.waitForTimeout(400);
    await expectCurrentFits(page, 2);
    expect((await kit.boundingBox())!.y).toBeCloseTo(-9, 1);
    await cdp.send('Input.dispatchTouchEvent', {type:'touchEnd',touchPoints:[]});
    expect((await kit.boundingBox())!.y).toBeCloseTo(0, 1);
    await expect(page.locator('.chapter-panel[data-chapter="1"] [data-item="name:Kit"]')).toHaveCount(1);
    await swipe(350,60); await expectCurrentFits(page, 2);
    await swipe(60,350);
    await expect.poll(() => page.locator('.viewport').evaluate(el => el.scrollLeft)).toBeLessThan(390);
    await swipe(350,60); await swipe(350,60);
    await expectCurrentFits(page, 2);
  } finally { await context.close(); }
});

test('desktop chapter browsing keeps a full viewport and ignores both wheel axes', async ({page}) => {
  await page.setViewportSize({width:1440,height:790});
  await enterField(page);
  const viewport = page.locator('.viewport');
  expect(await viewport.evaluate(el => ({
    scrollbar: getComputedStyle(el).scrollbarWidth,
    gutter: (el as HTMLElement).offsetWidth - el.clientWidth,
  }))).toEqual({scrollbar:'none',gutter:0});
  await page.mouse.move(1320,350);
  await page.mouse.wheel(0,-400);
  await page.mouse.wheel(-400,0);
  await page.evaluate(() => new Promise(resolve => requestAnimationFrame(resolve)));
  expect(await scrollLeft(page)).toBe(1440);
  await page.keyboard.press('ArrowLeft');
  await expect.poll(() => scrollLeft(page)).toBe(0);
});
