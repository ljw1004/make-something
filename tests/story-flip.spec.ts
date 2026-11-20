import {expect, test, type Page} from '@playwright/test';

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

async function traceFlip(page: Page) {
  const key = 'flip-test-trace';
  await page.addInitScript(key => {
    const animate = HTMLElement.prototype.animate;
    HTMLElement.prototype.animate = function (frames, options) {
      const activeFlip = this.closest<HTMLElement>('[data-story-flip]');
      if (activeFlip) {
        const previous = JSON.parse(sessionStorage.getItem(key) ?? '[]');
        previous.push({
          phase:activeFlip.dataset.storyFlip, animations:frames, options,
          rotatingBoard:this.classList.contains('game-surface'),
          dialog:!!document.querySelector('dialog[open]'),
          gutter:getComputedStyle(document.documentElement).backgroundColor,
          item:!!this.querySelector('[data-item="name:Frame"]'),
          catalogueTitle:this.querySelector('.carousel-slide:not([inert]) h2')?.textContent ?? null,
        });
        sessionStorage.setItem(key, JSON.stringify(previous));
      }
      return animate.call(this, frames, options);
    };
  }, key);
  return () => page.evaluate(key => JSON.parse(sessionStorage.getItem(key) ?? '[]'), key);
}

test('catalogue and Home flip about a fixed center; story intro overlays the incoming board after art is ready', async ({page}) => {
  const trace = await traceFlip(page);
  let release!: () => void;
  const pending = new Promise<void>(resolve => { release = resolve; });
  await page.route('**/stories/mars/mars.md', async route => {
    await pending;
    await route.fulfill({contentType:'text/markdown', body:fixture});
  });
  await page.goto('/');
  await page.getByRole('button',{name:'Mission to Mars',exact:true}).click();
  const card = page.locator('a[data-story="stories/mars/mars.md"]');
  await card.focus();
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/make-something.html\?story=stories\/mars\/mars\.md$/);
  await expect(page.locator('#app')).toHaveAttribute('data-story-flip','waiting');
  await expect(page.locator('#app .story-loading')).toHaveCount(0);
  await expect(page.locator('html')).toHaveCSS('background-color','rgb(0, 0, 0)');
  release();
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeFocused();
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  await page.getByRole('button',{name:'Read this chapter'}).click();
  await page.getByRole('link',{name:'Home',exact:true}).click();
  await expect(page).toHaveURL(/\/index.html$/);
  await expect(page.locator('.carousel-frame')).not.toHaveAttribute('data-story-flip',/./);
  await expect(card).toBeVisible();
  const events = await trace();
  expect(events.map(({phase}: {phase: string}) => phase)).toEqual(['leaving','arriving','leaving','arriving']);
  expect(events.map((event: {animations: {transform: string}[]}) => event.animations.map(frame => frame.transform))).toEqual([
    ['perspective(1400px) rotateY(0deg)','perspective(1400px) rotateY(-90deg)'],
    ['perspective(1400px) rotateY(90deg)','perspective(1400px) rotateY(0deg)'],
    ['perspective(1400px) rotateY(0deg)','perspective(1400px) rotateY(90deg)'],
    ['perspective(1400px) rotateY(-90deg)','perspective(1400px) rotateY(0deg)'],
  ]);
  expect(events.every((event: {options: {duration: number}; animations: {transformOrigin: string}[]}) =>
    event.options.duration === 160 && event.animations.every(frame => frame.transformOrigin === '50% 50%'))).toBe(true);
  expect(events.every((event: {gutter: string}) => event.gutter === 'rgb(0, 0, 0)')).toBe(true);
  expect(events[0].catalogueTitle).toBe('Mission to Mars');
  expect(events[1]).toMatchObject({item:true,dialog:false,rotatingBoard:true});
  expect(events[2]).toMatchObject({item:true,dialog:false});
  expect(events[3].catalogueTitle).toBe('Mission to Mars');
  await page.goBack();
  await expect(page.locator('[data-item="name:Frame"]')).toBeVisible();
  expect(await trace()).toHaveLength(4);
});

test('direct entry and reduced motion never flip', async ({page}) => {
  const trace = await traceFlip(page);
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType:'text/markdown',body:fixture}));
  await page.goto('/make-something.html?story=stories/cookbook/cookbook.md');
  await expect(page.getByRole('button',{name:'Start',exact:true})).toBeVisible();
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.goto('/');
  await page.locator('a[data-story="stories/cookbook/cookbook.md"]').click();
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  await page.getByRole('button',{name:'Read this chapter'}).click();
  await page.getByRole('link',{name:'Home',exact:true}).click();
  await expect(page).toHaveURL(/\/index.html$/);
  expect(await trace()).toEqual([]);
});

test('slow chapter artwork shows only a black spinner and the ready chapter flips behind its popup', async ({page}) => {
  const trace = await traceFlip(page);
  let release!: () => void;
  const pending = new Promise<void>(resolve => { release = resolve; });
  const actual = fixture.replace('Make a kit.', '![Room](flip-fixture.svg)\nMake a kit.');
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType:'text/markdown',body:actual}));
  await page.route('**/stories/cookbook/flip-fixture.svg', async route => {
    await pending;
    await route.fulfill({contentType:'image/svg+xml',body:'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844"><rect width="390" height="844" fill="purple"/></svg>'});
  });
  try {
    await page.goto('/');
    await page.locator('a[data-story="stories/cookbook/cookbook.md"]').click();
    await expect(page.locator('#app')).toHaveAttribute('data-story-flip','waiting');
    const spinner = page.locator('.story-flip-loading');
    await expect(spinner).toBeVisible();
    await expect(spinner).toHaveCSS('background-color','rgb(0, 0, 0)');
    await expect(page.locator('.story-loading')).toHaveCount(0);
    expect((await trace()).map((event: {phase: string}) => event.phase)).toEqual(['leaving']);
  } finally { release(); }
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeFocused();
  await expect(page.locator('.story-flip-loading')).toHaveCount(0);
  const events = await trace();
  expect(events.map((event: {phase: string}) => event.phase)).toEqual(['leaving','arriving']);
  expect(events[1]).toMatchObject({item:true,dialog:false,rotatingBoard:true});
});

test('a slow player bundle does not expose the standalone cream loading screen', async ({page}) => {
  let release!: () => void;
  const pending = new Promise<void>(resolve => { release = resolve; });
  await page.route('**/src/web/main.ts*', async route => { await pending; await route.continue(); });
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType:'text/markdown',body:fixture}));
  try {
    await page.goto('/');
    await page.locator('a[data-story="stories/cookbook/cookbook.md"]').click();
    await expect(page.locator('html')).toHaveClass(/story-flip-bootstrap/);
    const bootstrap = page.locator('.story-loading');
    await expect(bootstrap).toHaveCSS('background-color','rgb(0, 0, 0)');
    await expect(bootstrap).toHaveCSS('color','rgba(0, 0, 0, 0)');
    await expect.poll(() => bootstrap.evaluate(node => getComputedStyle(node,'::after').opacity)).toBe('1');
  } finally { release(); }
  await expect(page.getByRole('button',{name:'Begin',exact:true})).toBeVisible();
  await expect(page.locator('html')).not.toHaveClass(/story-flip-bootstrap/);
});

test('an unavailable Web Animations flip falls back to usable plain navigation', async ({page}) => {
  await page.addInitScript(() => {
    const animate = HTMLElement.prototype.animate;
    HTMLElement.prototype.animate = function (frames, options) {
      if (this.closest('[data-story-flip]')) throw Error('Flip rejected');
      return animate.call(this, frames, options);
    };
  });
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType:'text/markdown',body:fixture}));
  await page.goto('/');
  await page.locator('a[data-story="stories/cookbook/cookbook.md"]').click();
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  await page.getByRole('button',{name:'Read this chapter'}).click();
  await page.getByRole('link',{name:'Home',exact:true}).click();
  await expect(page).toHaveURL(/\/index.html$/);
  await expect(page.locator('.carousel-frame')).not.toHaveAttribute('data-story-flip',/./);
});

test('an already ready board cancels the spinner before it can mount', async ({page}) => {
  await page.goto('/');
  const mounted = await page.evaluate(async () => {
    const modulePath = '/src/web/story-flip.ts';
    const {holdFlip} = await import(modulePath);
    const face = document.createElement('div');
    let mounted = false;
    const monitor = new MutationObserver(records => {
      for (const {addedNodes} of records) for (const node of addedNodes)
        if (node instanceof HTMLElement && node.matches('.story-flip-loading')) mounted = true;
    });
    monitor.observe(document.body, {childList:true});
    const launch = holdFlip(face, 'launch');
    await launch.reveal(false);
    await new Promise(resolve => setTimeout(resolve, 270));
    monitor.disconnect();
    return mounted;
  });
  expect(mounted).toBe(false);
});

test('the opening popup stays still during the board flip and Begin can dismiss it early', async ({page}) => {
  await page.addInitScript(() => {
    const animate = HTMLElement.prototype.animate;
    HTMLElement.prototype.animate = function (frames, options) {
      const animation = animate.call(this, frames, options);
      if (this.matches('.game-surface') && this.closest('[data-story-flip="arriving"]')) {
        animation.pause();
        animation.currentTime = 35;
      }
      return animation;
    };
  });
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType:'text/markdown',body:fixture}));
  await page.goto('/');
  await page.locator('a[data-story="stories/cookbook/cookbook.md"]').click();
  const app = page.locator('#app'), board = page.locator('.game-surface'), dialog = page.locator('dialog[open]');
  const begin = page.getByRole('button',{name:'Begin',exact:true});
  await expect(app).toHaveAttribute('data-story-flip','arriving');
  await expect(begin).toBeFocused();
  const initial = await dialog.boundingBox();
  expect(initial).not.toBeNull();
  const matrix = await board.evaluate(node => getComputedStyle(node).transform);
  expect(matrix).not.toBe('none');
  await board.evaluate(node => { node.getAnimations()[0].currentTime = 105; });
  await expect.poll(() => board.evaluate(node => getComputedStyle(node).transform)).not.toBe(matrix);
  expect(await dialog.boundingBox()).toEqual(initial);
  await begin.click();
  await expect(dialog).toHaveCount(0);
  await expect(app).toHaveAttribute('data-story-flip','arriving');
  await expect(board).toHaveAttribute('inert','');
  await board.locator('[data-command="story"]').evaluate((node: HTMLElement) => node.click());
  await expect(dialog).toHaveCount(0);
  await board.evaluate(node => node.getAnimations()[0].finish());
  await expect(app).not.toHaveAttribute('data-story-flip',/./);
  await expect(board).not.toHaveAttribute('inert','');
  await expect(page.getByRole('button',{name:'Read this chapter'})).toBeEnabled();
});

test('Home from a completed story popup can interrupt its incoming flip cleanly', async ({page}) => {
  await page.addInitScript(() => {
    const animate = HTMLElement.prototype.animate;
    HTMLElement.prototype.animate = function (frames, options) {
      const animation = animate.call(this, frames, options);
      if (this.matches('.game-surface') && this.closest('[data-story-flip="arriving"]') && sessionStorage.getItem('pause-next-incoming')) {
        sessionStorage.removeItem('pause-next-incoming');
        animation.pause();
        animation.currentTime = 65;
      }
      return animation;
    };
  });
  const ending = fixture + '\n## Coda\nThe kit is ready.\n';
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType:'text/markdown',body:ending}));
  await page.goto('/');
  const card = page.locator('a[data-story="stories/cookbook/cookbook.md"]');
  await card.click();
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  const source = page.locator('[data-item="name:Frame"]'), tool = page.locator('[data-item="name:Tool"]');
  await source.dragTo(tool);
  await page.getByRole('button',{name:'Continue story',exact:true}).click();
  const home = page.getByRole('link',{name:'Home',exact:true});
  await home.click();
  await expect(card).toContainText('Continue');
  await page.evaluate(() => sessionStorage.setItem('pause-next-incoming','yes'));
  await card.click();
  await expect(page.locator('#app')).toHaveAttribute('data-story-flip','arriving');
  await expect(home).toBeVisible();
  await home.click();
  await expect(page).toHaveURL(/\/index.html$/);
  await expect(card).toContainText('Continue');
  await expect(page.locator('.carousel-frame')).not.toHaveAttribute('data-story-flip',/./);
  await page.goBack();
  await expect(page.locator('#app')).not.toHaveAttribute('data-story-flip',/./);
  await expect(page.getByRole('button',{name:'Read this chapter'})).toBeEnabled();
});

test('Home hides the static default card before the catalogue module and reveals the restored Mars card', async ({page}) => {
  const trace = await traceFlip(page);
  let returning = false;
  let releaseModule!: () => void;
  const blockedModule = new Promise<void>(resolve => { releaseModule = resolve; });
  await page.route('**/src/web/catalogue.ts', async route => {
    if (returning) await blockedModule;
    await route.continue();
  });
  await page.route('**/stories/mars/mars.md', route => route.fulfill({contentType:'text/markdown',body:fixture}));
  await page.goto('/');
  await page.getByRole('button',{name:'Mission to Mars',exact:true}).click();
  const card = page.locator('a[data-story="stories/mars/mars.md"]');
  await card.click();
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  await page.getByRole('button',{name:'Read this chapter'}).click();

  returning = true;
  try {
    await page.getByRole('link',{name:'Home',exact:true}).click();
    await page.waitForURL(/\/index.html$/, {waitUntil:'commit'});
    await expect(page.locator('html')).toHaveClass(/carousel-home-bootstrap/);
    await expect(page.locator('html')).toHaveCSS('background-color', 'rgb(0, 0, 0)');
    // Without the bootstrap this is the visible static default, even though
    // the Mars selection already exists in storage.
    const cookbook = page.locator('a[data-story="stories/cookbook/cookbook.md"]');
    await expect(cookbook).toHaveCount(1);
    await expect(cookbook).toBeHidden();
    await expect(page.locator('.carousel-frame')).toBeHidden();
  } finally { releaseModule(); }
  await expect(card).toBeVisible();
  await expect(page.locator('html')).not.toHaveClass(/carousel-home-bootstrap/);
  await expect(page.locator('.carousel-frame')).not.toHaveAttribute('data-story-flip', /./);
  expect((await trace()).at(-1)).toMatchObject({
    phase:'arriving', catalogueTitle:'Mission to Mars', gutter:'rgb(0, 0, 0)',
    animations:[
      {transform:'perspective(1400px) rotateY(-90deg)'},
      {transform:'perspective(1400px) rotateY(0deg)'},
    ],
  });
});
