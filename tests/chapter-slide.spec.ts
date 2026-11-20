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
  top: document.querySelector('.viewport')!.scrollTop,
  height: document.querySelector('#app')!.clientHeight,
  panels: document.querySelectorAll('.chapter-panel').length,
  sliding: document.querySelector('.game-surface')!.classList.contains('chapter-sliding'),
  locked: document.querySelector<HTMLElement>('.game-surface')!.inert,
  popup: !document.querySelector<HTMLElement>('.game-dialog-layer')!.hidden,
}));

test('advance scrolls the real viewport behind an immediate stationary popup and ignores repeated activation', async ({page}) => {
  await open(page); await advance(page);
  expect(await view(page)).toMatchObject({sliding:true,popup:true,panels:2});
  const dialog=page.getByRole('dialog'), initial=await dialog.boundingBox();
  await expect.poll(async () => (await view(page)).top).toBeGreaterThan(0);
  const middle=await view(page); expect(middle.top).toBeGreaterThan(0); expect(middle.top).toBeLessThan(middle.height);
  expect(await dialog.boundingBox()).toEqual(initial);
  await advance(page); // current chapter is already complete, but cannot advance again
  const repeat = await page.getByRole('button',{name:'Begin',exact:true}).evaluate(button => ({
    keyboard: button.dispatchEvent(new KeyboardEvent('keydown', {key:'Enter',repeat:true,bubbles:true,cancelable:true})),
    pointer: button.dispatchEvent(new MouseEvent('click', {detail:2,bubbles:true,cancelable:true})),
  }));
  expect(repeat).toEqual({keyboard:false,pointer:false});
  await expect.poll(async () => (await view(page)).sliding).toBe(false);
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  const end=await view(page); expect(end).toMatchObject({sliding:false,popup:true,panels:2}); expect(end.top).toBe(end.height);
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  await expect(page.locator('[data-item="name:B"]')).toBeVisible();
  await expect(page.locator('[data-command="advance"]')).toHaveClass(/right/);
  await advance(page); expect(await view(page)).toMatchObject({sliding:true,popup:true,panels:3});
  await expect.poll(async () => (await view(page)).sliding).toBe(false);
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  expect((await view(page)).top).toBe(2*(await view(page)).height);
});

test('resize during arrival keeps its destination and reload does not replay the slide', async ({page}) => {
  await open(page); await advance(page);
  await page.setViewportSize({width:430,height:700});
  await expect.poll(async () => (await view(page)).sliding).toBe(false);
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  const arrived=await view(page); expect(arrived.top).toBe(arrived.height); expect(arrived.panels).toBe(2);
  await page.reload();
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  const reloaded=await view(page); expect(reloaded.sliding).toBe(false); expect(reloaded.top).toBe(reloaded.height);
});

test('reload mid-slide restores committed destination and pending introduction', async ({page}) => {
  await open(page); await advance(page); expect((await view(page)).sliding).toBe(true);
  await page.reload();
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  const restored=await view(page); expect(restored.sliding).toBe(false); expect(restored.panels).toBe(2); expect(restored.top).toBe(restored.height);
});

test('reduced motion arrives immediately with no animated wait', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'}); await open(page); await advance(page);
  const arrived=await view(page); expect(arrived).toMatchObject({sliding:false,popup:true,panels:2}); expect(arrived.top).toBe(arrived.height);
});

test('artwork wait holds the outgoing board, then slides once after loading', async ({page}) => {
  let release!: () => void;
  const artwork = new Promise<void>(resolve => { release=resolve; });
  await open(page, artwork); await advance(page); await advance(page);
  expect(await view(page)).toMatchObject({sliding:false,popup:false,panels:1,top:0});
  release();
  await expect(page.locator('.game-surface')).toHaveClass(/chapter-sliding/);
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  expect((await view(page)).sliding).toBe(true);
  await expect.poll(async () => (await view(page)).sliding).toBe(false);
  const arrived=await view(page); expect(arrived.panels).toBe(2); expect(arrived.top).toBe(arrived.height);
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
    const arrived=await view(page); expect(arrived).toMatchObject({locked:false,popup:false,panels:2}); expect(arrived.top).toBe(arrived.height);
    await page.reload();
    await expect(page.locator('[data-item="name:B"]')).toBeVisible();
    const restored=await view(page); expect(restored).toMatchObject({sliding:false,popup:false,panels:2}); expect(restored.top).toBe(restored.height);
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
    return {moving, settled:!surface.classList.contains('chapter-sliding'), pending:saved.state.pending, atDestination:saved.anchor.scrollTop === document.querySelector('#app')!.clientHeight};
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
