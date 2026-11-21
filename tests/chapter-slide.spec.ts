import {test, expect, type Page} from '@playwright/test';

const manuscript = `# Slide fixture
## First
background: ![room](room.svg)
First introduction.
**Goals**
- Have A -- A
**Items**
- A
## Second
background: ![other](other.svg)
Second introduction.
**Goals**
- Have B -- B
**Items**
- B
## Same scene
Third introduction.
**Goals**
- Have C -- C
**Items**
- C
`;
async function open(page: Page, otherArtwork?: Promise<void>, body = manuscript) {
  await page.route('**/slide-fixture/story.md', r => r.fulfill({contentType:'text/markdown',body}));
  await page.route('**/slide-fixture/*.svg', async r => {
    if (r.request().url().endsWith('/other.svg')) await otherArtwork;
    await r.fulfill({contentType:'image/svg+xml',body:'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844"><rect width="390" height="844" fill="tan"/></svg>'});
  });
  await page.goto('/make-something.html?story=slide-fixture/story.md');
  await page.getByRole('button',{name:'Start',exact:true}).click();
  await page.getByRole('button',{name:'Begin',exact:true}).click();
}
async function advance(page: Page) {
  // Synchronous dispatch allows observation before Playwright's animation waits.
  await page.locator('[data-command="advance"]').evaluate(el => (el as HTMLElement).click());
}
const view = (page: Page) => page.evaluate(() => ({
  left: document.querySelector('.viewport')!.scrollLeft,
  width: document.querySelector('#app')!.clientWidth,
  panels: document.querySelectorAll('.chapter-panel').length,
  sliding: document.querySelector('.game-surface')!.classList.contains('chapter-sliding'),
  locked: document.querySelector<HTMLElement>('.game-surface')!.inert,
  popup: !document.querySelector<HTMLElement>('.game-dialog-layer')!.hidden,
}));

test('advance scrolls the real viewport behind an immediate stationary popup and ignores repeated activation', async ({page}) => {
  await open(page); await advance(page);
  expect(await view(page)).toMatchObject({sliding:true,popup:true,panels:2});
  const dialog=page.getByRole('dialog'), initial=await dialog.boundingBox();
  await expect.poll(async () => (await view(page)).left).toBeGreaterThan(0);
  const middle=await view(page); expect(middle.left).toBeGreaterThan(0); expect(middle.left).toBeLessThan(middle.width);
  expect(await dialog.boundingBox()).toEqual(initial);
  await advance(page); // current chapter is already complete, but cannot advance again
  const repeat = await page.getByRole('button',{name:'Begin',exact:true}).evaluate(button => ({
    keyboard: button.dispatchEvent(new KeyboardEvent('keydown', {key:'Enter',repeat:true,bubbles:true,cancelable:true})),
    pointer: button.dispatchEvent(new MouseEvent('click', {detail:2,bubbles:true,cancelable:true})),
  }));
  expect(repeat).toEqual({keyboard:false,pointer:false});
  await expect.poll(async () => (await view(page)).sliding).toBe(false);
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  const end=await view(page); expect(end).toMatchObject({sliding:false,popup:true,panels:2}); expect(end.left).toBe(end.width);
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  await expect(page.locator('[data-item="name:B"]')).toBeVisible();
  await expect(page.locator('[data-command="advance"]')).toHaveText('→');
  await advance(page); expect(await view(page)).toMatchObject({sliding:true,popup:true,panels:3});
  await expect.poll(async () => (await view(page)).sliding).toBe(false);
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  expect((await view(page)).left).toBe(2*(await view(page)).width);
});

test('resize during arrival keeps its destination and reload does not replay the slide', async ({page}) => {
  await open(page); await advance(page);
  await page.setViewportSize({width:430,height:700});
  await expect.poll(async () => (await view(page)).sliding).toBe(false);
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  const arrived=await view(page); expect(arrived.left).toBe(arrived.width); expect(arrived.panels).toBe(2);
  await page.reload();
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  const reloaded=await view(page); expect(reloaded.sliding).toBe(false); expect(reloaded.left).toBe(reloaded.width);
});

test('reload mid-slide restores committed destination and pending introduction', async ({page}) => {
  await open(page); await advance(page); expect((await view(page)).sliding).toBe(true);
  await page.reload();
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  const restored=await view(page); expect(restored.sliding).toBe(false); expect(restored.panels).toBe(2); expect(restored.left).toBe(restored.width);
});

test('reduced motion arrives immediately with no animated wait', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'}); await open(page); await advance(page);
  const arrived=await view(page); expect(arrived).toMatchObject({sliding:false,popup:true,panels:2}); expect(arrived.left).toBe(arrived.width);
});

test('artwork wait holds the outgoing board, then slides once after loading', async ({page}) => {
  let release!: () => void;
  const artwork = new Promise<void>(resolve => { release=resolve; });
  await open(page, artwork); await advance(page); await advance(page);
  expect(await view(page)).toMatchObject({sliding:false,popup:false,panels:1,left:0});
  release();
  await expect(page.locator('.game-surface')).toHaveClass(/chapter-sliding/);
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  expect((await view(page)).sliding).toBe(true);
  await expect.poll(async () => (await view(page)).sliding).toBe(false);
  const arrived=await view(page); expect(arrived.panels).toBe(2); expect(arrived.left).toBe(arrived.width);
});

test('turning on reduced motion mid-slide finishes and releases input immediately', async ({page}) => {
  await open(page); await advance(page);
  await page.emulateMedia({reducedMotion:'reduce'});
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  await expect.poll(async () => (await view(page)).sliding).toBe(false);
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  await advance(page);
  expect(await view(page)).toMatchObject({sliding:false,popup:true,panels:3});
});

for (const dismissal of ['Begin', 'Escape'] as const) {
  test(`${dismissal} dismisses the reading mid-slide but the board stays locked until arrival`, async ({page}) => {
    await open(page);
    const during = await page.locator('[data-command="advance"]').evaluate((arrow, method) => {
      (arrow as HTMLElement).click();
      const begin = document.querySelector<HTMLButtonElement>('dialog [data-command="dismiss"]')!;
      if (method === 'Begin') begin.click();
      else begin.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true,cancelable:true}));
      document.querySelector<HTMLElement>('[data-command="advance"]')?.click();
      const surface = document.querySelector<HTMLElement>('.game-surface')!;
      return {locked:surface.inert, sliding:surface.classList.contains('chapter-sliding'), popup:!!document.querySelector('dialog'), panels:document.querySelectorAll('.chapter-panel').length};
    }, dismissal);
    expect(during).toEqual({locked:true,sliding:true,popup:false,panels:2});
    await expect.poll(async () => (await view(page)).sliding).toBe(false);
    const arrived=await view(page); expect(arrived).toMatchObject({locked:false,popup:false,panels:2}); expect(arrived.left).toBe(arrived.width);
    await page.reload();
    await expect(page.locator('[data-item="name:B"]')).toBeVisible();
    const restored=await view(page); expect(restored).toMatchObject({sliding:false,popup:false,panels:2}); expect(restored.left).toBe(restored.width);
  });
}

test('Home from the immediate ending reading settles the board before navigation', async ({page}) => {
  await page.addInitScript(() => {
    if (new URL(location.href).searchParams.get('story') !== 'slide-fixture/story.md') return;
    history.replaceState({makeSomethingCarouselEntry:{
      entry:'carousel', modality:'mouse', destination:location.href, manuscript:new URL('slide-fixture/story.md',location.href).href,
    }}, '');
  });
  await open(page, undefined, manuscript.split('## Second')[0] + '## Ending\nThe finale.');
  const settled = await page.locator('[data-command="advance"]').evaluate(arrow => {
    (arrow as HTMLElement).click();
    const surface = document.querySelector('.game-surface')!;
    const moving = surface.classList.contains('chapter-sliding');
    document.querySelector<HTMLElement>('[data-command="ending-home"]')!.click();
    const saved = JSON.parse(Object.entries(localStorage).find(([key]) => key.startsWith('combination-progress-v2:'))![1]);
    return {moving, settled:!surface.classList.contains('chapter-sliding'), pending:saved.state.pending, atDestination:saved.anchor.chapterView === 1};
  });
  expect(settled).toEqual({moving:true, settled:true, pending:[], atDestination:true});
  await expect(page).toHaveURL(/\/index.html$/);
});

test('chapter slide packs new supplies at the same coordinates as reduced motion', async ({page}) => {
  const story = manuscript.split('## Second')[0] + `## Second
background: ![other](other.svg)
Build a kit in the next room.
**Goals**
- Build the kit -- Kit
**Items**
- Panel
- Tool
- Glue
**Combinations**
- A [preserve] + Panel [preserve] -> Kit
- Tool [preserve] + Glue [preserve] -> Spare
`;
  for (const viewport of [{width:390,height:844},{width:1458,height:1080}]) {
    await page.setViewportSize(viewport);
    const sample = async (mode:'reduce'|'no-preference') => {
      await page.emulateMedia({reducedMotion:mode});
      await open(page, undefined, story);
      await advance(page);
      await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
      await expect.poll(async () => (await view(page)).sliding).toBe(false);
      const names = ['Panel','Tool','Glue'];
      const positions = await page.locator('.chapter-panel').last().locator('[data-item]').evaluateAll((items,names) =>
        Object.fromEntries(items.filter(item => names.includes(item.getAttribute('data-item')!.slice(5)))
          .map(item => {
            const {left,top} = (item as HTMLElement).style;
            return [item.getAttribute('data-item'),[parseFloat(left),parseFloat(top)]];
          })), names);
      expect(Object.keys(positions)).toHaveLength(3);
      // Reset only this isolated browser context's progress before replaying.
      await page.evaluate(() => Object.keys(localStorage)
        .filter(key => key.startsWith('combination-progress-v2:'))
        .forEach(key => localStorage.removeItem(key)));
      return positions;
    };
    const reduced = await sample('reduce');
    expect(await sample('no-preference'), `supply positions at ${viewport.width}px`).toEqual(reduced);
  }
});

test('a left swipe advances a ready chapter and shows its pinned intro, while visiting history opens no popup', async ({browser}) => {
  const context = await browser.newContext({isMobile:true,hasTouch:true,viewport:{width:390,height:844}});
  try {
    const page = await context.newPage();
    await open(page);
    const input = await context.newCDPSession(page);
    async function swipe(from: number, to: number) {
      await input.send('Input.dispatchTouchEvent', {type:'touchStart',touchPoints:[{x:from,y:70}]});
      await input.send('Input.dispatchTouchEvent', {type:'touchMove',touchPoints:[{x:to,y:70}]});
      await input.send('Input.dispatchTouchEvent', {type:'touchEnd',touchPoints:[]});
    }
    await expect(page.getByRole('button',{name:'Continue story'})).toHaveText('→');
    await swipe(280,120);
    const dialog = page.getByRole('dialog');
    await expect(dialog).toContainText('Second introduction.');
    const pinned = await dialog.boundingBox();
    const moving = await view(page);
    expect(moving.left).toBeGreaterThan(0);
    expect(moving.left).toBeLessThan(moving.width);
    await expect.poll(async () => (await view(page)).left).toBe(390);
    expect(await dialog.boundingBox()).toEqual(pinned);
    await page.getByRole('button',{name:'Begin',exact:true}).tap();
    await swipe(120,280);
    await expect.poll(async () => (await view(page)).left).toBe(0);
    await expect(dialog).toHaveCount(0);
    await swipe(280,120);
    await expect.poll(async () => (await view(page)).left).toBe(390);
    await expect(dialog).toHaveCount(0);
  } finally { await context.close(); }
});

test('chapter drags complete at 65 CSS pixels and flicks can travel less', async ({page}) => {
  await page.setViewportSize({width:1000,height:800});
  await page.emulateMedia({reducedMotion:'reduce'});
  await open(page);
  await advance(page);
  await page.getByRole('button',{name:'Begin',exact:true}).click();

  for (const dx of [-60,60]) {
    await page.mouse.move(450,70);
    await page.mouse.down();
    await page.mouse.move(450+dx,70,{steps:4});
    await page.waitForTimeout(80);
    await page.mouse.up();
    expect(await view(page)).toMatchObject({left:1000,panels:2,popup:false});
  }

  await page.mouse.move(450,70);
  await page.mouse.down();
  await page.mouse.move(515,70,{steps:4});
  await page.waitForTimeout(80);
  await page.mouse.up();
  expect((await view(page)).left).toBe(0);

  const client = await page.context().newCDPSession(page);
  async function flick(delta: number) {
    const start = Date.now() / 1000;
    await client.send('Input.dispatchMouseEvent', {type:'mousePressed', x:450,y:70,button:'left',buttons:1,clickCount:1,timestamp:start});
    await client.send('Input.dispatchMouseEvent', {type:'mouseMoved', x:450+delta/2,y:70,button:'left',buttons:1,timestamp:start+.016});
    await client.send('Input.dispatchMouseEvent', {type:'mouseMoved', x:450+delta,y:70,button:'left',buttons:1,timestamp:start+.032});
    await client.send('Input.dispatchMouseEvent', {type:'mouseReleased', x:450+delta,y:70,button:'left',buttons:0,clickCount:1,timestamp:start+.036});
  }
  await flick(-60);
  await expect.poll(async () => (await view(page)).left).toBe(1000);
  expect(await view(page)).toMatchObject({panels:2,popup:false});

  await flick(-60);
  await expect(page.getByRole('dialog')).toContainText('Third introduction.');
  expect(await view(page)).toMatchObject({left:2000,panels:3});
});

test('wide chapter swipes move adjacent artwork and keep the goals visible', async ({page}) => {
  await page.setViewportSize({width:1200,height:844});
  const source = manuscript.replace('- Have B -- B\n**Items**\n- B',
    '- Finish -- Result\n**Items**\n- B\n- C\n**Combinations**\n- B + C -> Result');
  await open(page, undefined, source);
  await advance(page);
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  await expect.poll(async () => (await view(page)).left).toBe(1200);
  const goals = page.locator('.location-hud');
  const goalPosition = await goals.boundingBox();

  await page.mouse.move(480,90);
  await page.mouse.down();
  await page.mouse.move(675,90,{steps:5});
  const art = page.locator('.scene-art');
  const earlier = (await art.nth(0).boundingBox())!;
  const later = (await art.nth(1).boundingBox())!;
  expect(earlier.x + earlier.width).toBeCloseTo(600, 1);
  expect(later.x).toBeCloseTo(earlier.x + earlier.width, 1);
  await expect(page.locator('.viewport')).toHaveCSS('clip-path', 'inset(0px 405px)');
  expect(await goals.boundingBox()).toEqual(goalPosition);
  await page.mouse.up();
  expect(await goals.evaluate(node => ({
    sliding: node.closest('.game-surface')!.classList.contains('chapter-sliding'),
    visibility: getComputedStyle(node).visibility,
  }))).toEqual({sliding:true, visibility:'visible'});
  await expect.poll(async () => (await view(page)).left).toBe(0);
  await expect(page.locator('.viewport')).not.toHaveClass(/chapter-motion/);
});
