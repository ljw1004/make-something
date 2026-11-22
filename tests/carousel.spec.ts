import {test, expect} from '@playwright/test';

const story = `# Workshop
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

## Ending
The kit is ready.
`;

test('Start skips the cover, final Home preserves progress, and Restart keeps shared tutorial flags', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType:'text/markdown', body:story}));
  await page.route('**/stories/mars/mars.md', route => route.fulfill({contentType:'text/markdown', body:story}));
  const active = page.locator('.carousel-slide:visible');
  const launch = active.locator('a[data-story]');
  await page.goto('/');
  await page.getByRole('button', {name:'Mission to Mars', exact:true}).click();
  await expect(launch).toContainText('Start');
  await launch.click();
  await expect(page.getByRole('button', {name:'Begin'})).toBeVisible();
  await page.getByRole('button', {name:'Begin'}).click();
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await page.getByRole('button', {name:'Continue story'}).click();
  await expect(page.getByText('The kit is ready.', {exact:true})).toBeVisible();
  await expect(page.getByRole('button', {name:'Begin'})).toHaveCount(0);
  const end = page.getByRole('button', {name:'End', exact:true});
  const endingLink = page.getByRole('link', {name:'Home', exact:true});
  await expect(end).toBeVisible();
  const row = (await page.locator('.ending-actions').boundingBox())!, centered = (await end.boundingBox())!, aligned = (await endingLink.boundingBox())!;
  expect(centered.x + centered.width / 2).toBeCloseTo(row.x + row.width / 2, 0);
  expect(aligned.y + aligned.height / 2).toBeCloseTo(centered.y + centered.height / 2, 0);
  expect(aligned.x + aligned.width).toBeCloseTo(row.x + row.width, 0);
  await page.evaluate(() => localStorage.setItem('make-something-carousel-v1:/', 'stories/cookbook/cookbook.md'));
  await page.getByRole('link', {name:'Home', exact:true}).click();
  await expect(page).toHaveURL(/\/index.html$/);
  await expect(active.getByRole('heading')).toHaveText('Mission to Mars');
  await expect(launch).toContainText('Continue');
  await launch.click();
  await expect(page.getByRole('dialog')).toContainText('The kit is ready.');
  await page.getByRole('button', {name:'End', exact:true}).click();
  await expect(page.getByText('The End', {exact:true})).toBeVisible();
  await page.getByRole('button', {name:'Read this chapter'}).click();
  const home = page.getByRole('link', {name:'Home', exact:true});
  const restart = page.getByRole('button', {name:'Restart story', exact:true});
  await expect(home).toBeVisible();
  await expect(restart).toBeVisible();
  expect((await restart.boundingBox())!.x).toBeLessThan((await home.boundingBox())!.x);
  await page.evaluate(() => localStorage.setItem('make-something-carousel-v1:/', 'stories/cookbook/cookbook.md'));
  await home.click();
  await expect(page).toHaveURL(/\/index.html$/);
  await expect(active.getByRole('heading')).toHaveText('Mission to Mars');
  await expect(launch).toContainText('Continue');
  const tutorialKey = await page.evaluate(() => 'combination-tutorial-v1:' + encodeURIComponent(new URL('index.html', location.href).href));
  expect(await page.evaluate(key => JSON.parse(localStorage.getItem(key)!).goalsDone, tutorialKey)).toBe(true);
  const dragKeys = await page.evaluate(() => ['mars/mars', 'cookbook/cookbook'].map(path =>
    'combination-tutorial-drag-v2:' + encodeURIComponent(new URL('stories/' + path + '.md', location.href).href)));
  expect(await page.evaluate(keys => keys.map(key => localStorage.getItem(key)), dragKeys)).toEqual(['true', null]);
  await page.getByRole('button', {name:'Cookbook', exact:true}).click();
  await launch.click();
  await page.getByRole('button', {name:'Begin'}).click();
  await page.getByRole('button', {name:'Read this chapter'}).click();
  await page.getByRole('button', {name:/Restart story/}).click();
  await page.getByRole('button', {name:'Restart story', exact:true}).click();
  await expect(page.getByRole('button', {name:'Begin', exact:true})).toBeVisible();
  expect(await page.evaluate(key => JSON.parse(localStorage.getItem(key)!).goalsDone, tutorialKey)).toBe(true);
  expect(await page.evaluate(keys => keys.map(key => localStorage.getItem(key)), dragKeys)).toEqual(['true', 'false']);
  await page.reload();
  await expect(page.getByRole('button', {name:'Begin', exact:true})).toBeVisible();
  await page.goto('/');
  await page.getByRole('button', {name:'Mission to Mars', exact:true}).click();
  await expect(launch).toContainText('Continue');
});

test('carousel wraps, swipes across the artwork, and launches a touch tutorial', async ({browser}) => {
  const context = await browser.newContext({isMobile:true, hasTouch:true, viewport:{width:390,height:844}});
  try {
    const page = await context.newPage();
    await page.emulateMedia({reducedMotion:'reduce'});
    await page.goto('/?utm_source=example');
    const address = page.url();
    const active = page.locator('.carousel-slide:visible');
    const title = active.getByRole('heading');
    const first = await title.textContent();
    await page.getByRole('button', {name:first!, exact:true}).focus();
    await page.keyboard.press('ArrowRight');
    await expect(page.getByRole('button', {name:'Settlement', exact:true})).toBeFocused();
    await page.keyboard.press('ArrowLeft');
    await expect(page.getByRole('button', {name:first!, exact:true})).toBeFocused();
    await page.getByRole('button', {name:'Previous story'}).click();
    await expect(title).not.toHaveText(first!);
    await page.getByRole('button', {name:'Next story'}).click();
    await expect(title).toHaveText(first!);
    await expect(page).toHaveURL(address);
    const client = await context.newCDPSession(page);
    for (const dx of [-60,60]) {
      await client.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[{x:170,y:220}]});
      await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:170+dx,y:220}]});
      await expect(page.locator('.carousel-slide:visible')).toHaveCount(2);
      await page.waitForTimeout(80);
      await client.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[]});
      await expect(active).toHaveCount(1);
      await expect(title).toHaveText(first!);
    }
    for (const {positions, destination} of [
      {positions:[140,110], destination:'Settlement'},
      {positions:[110,150], destination:first!},
    ]) {
      const start = Date.now() / 1000;
      await client.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[{x:170,y:220}], timestamp:start});
      for (const [index,x] of positions.entries()) {
        await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x,y:220}], timestamp:start + (index + 1) * .016});
      }
      await client.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[], timestamp:start + .036});
      await expect(active).toHaveCount(1);
      await expect(title).toHaveText(destination);
    }
    const privacy = (await active.getByRole('link', {name:'Privacy', exact:true}).boundingBox())!;
    const x = Math.round(privacy.x + privacy.width / 2);
    const y = Math.round(privacy.y + privacy.height / 2);
    await client.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[{x,y}]});
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:x-60,y}]});
    const translated = () => page.locator('.carousel-slide:not([hidden])').evaluateAll(slides => slides.map(slide =>
      ['.carousel-art','.carousel-bar','.carousel-dots','.carousel-description','.carousel-footer'].map(selector => {
        const node = slide.querySelector<HTMLElement>(selector)!;
        const bounds = node.getBoundingClientRect();
        if (selector === '.carousel-footer') return Math.round(bounds.x + (bounds.width - slide.clientWidth) / 2);
        return bounds.x - (selector === '.carousel-bar' ? parseFloat(getComputedStyle(node).marginLeft) : 0);
      })));
    await expect.poll(translated).toEqual([Array(5).fill(-60), Array(5).fill(330)]);
    expect(await page.locator('.carousel-slide:not([hidden]) .carousel-dots [aria-current="true"]').evaluateAll(dots =>
      dots.map(dot => dot.getAttribute('aria-label')))).toEqual([first, 'Settlement']);
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:x-200,y}]});
    await expect.poll(translated).toEqual([Array(5).fill(-200), Array(5).fill(190)]);
    await client.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[]});
    await expect(active).toHaveCount(1);
    await expect(title).not.toHaveText(first!);
    await expect.poll(translated).toEqual([Array(5).fill(0)]);
    expect(context.pages()).toEqual([page]);
    await expect(page).toHaveURL(address);
    await page.reload();
    await expect(title).toHaveText('Settlement');
    const second = await title.textContent();
    await client.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[{x:160,y:380}]});
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:186,y:380}]});
    await expect.poll(translated).toEqual([Array(5).fill(-364), Array(5).fill(26)]);
    await page.waitForTimeout(80);
    await client.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[]});
    await expect(active).toHaveCount(1);
    await expect(title).toHaveText(second!);
    await client.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[{x:100,y:220}]});
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:250,y:220}]});
    await expect.poll(translated).toEqual([Array(5).fill(-240), Array(5).fill(150)]);
    await client.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[]});
    await expect(active).toHaveCount(1);
    await expect(title).toHaveText(first!);
    await page.getByRole('button', {name:'Cookbook', exact:true}).tap();
    await expect(title).toHaveText('Cookbook');
    await expect(page).toHaveURL(address);
    await active.locator('a[data-story]').tap();
    await expect(page).toHaveURL(/\/index.html\?story=stories\/cookbook\/cookbook\.md$/);
    await expect(page.locator('.tutorial-overlay')).toHaveAttribute('data-modality', 'touch');
    await expect(page.getByRole('button', {name:'Begin'})).toBeVisible();
  } finally { await context.close(); }
});

test('theology banner sits near mid-screen and the full smaller abstract is readable', async ({page}) => {
  await page.goto('/');
  await page.getByRole('button', {name:'Theology', exact:true}).click();
  const carousel = page.locator('.carousel-slide:not([hidden])');
  await expect(carousel.getByRole('heading')).toHaveText('Theology');
  for (const viewport of [{width:417,height:911}, {width:320,height:568}]) {
    await page.setViewportSize(viewport);
    await expect.poll(() => carousel.evaluate(el => {
      const bar = el.querySelector('.carousel-bar')!.getBoundingClientRect();
      const abstract = el.querySelector<HTMLElement>('.carousel-description')!;
      return {
        nearMiddle: (bar.y + bar.height / 2) / innerHeight < .56 && bar.y / innerHeight > .4,
        fullAbstract: abstract.scrollHeight <= abstract.clientHeight,
        inset: bar.x > el.getBoundingClientRect().x && bar.right < el.getBoundingClientRect().right,
        compactType: parseFloat(getComputedStyle(abstract).fontSize) <= 17,
      };
    })).toEqual({nearMiddle:true,fullAbstract:true,inset:true,compactType:true});
  }
});

test('carousel selections preserve the address and history and persist by manuscript path', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.goto('/index.html?utm_source=example');
  const address = page.url();
  const active = page.locator('.carousel-slide:visible');
  expect(await active.locator('.carousel-dots button').evaluateAll(dots =>
    dots.map(dot => dot.getAttribute('aria-label')))).toEqual([
    'Cookbook', 'Settlement', 'Creation', 'Mission to Mars', 'Anatomy', 'Theology', 'History of ideas',
  ]);
  const mark = await page.evaluate(() => {
    history.replaceState({testMarker:true}, '');
    return history.length;
  });
  await page.getByRole('button', {name:'Previous story'}).click();
  await expect(active.getByRole('heading')).toHaveText('History of ideas');
  await expect(page).toHaveURL(address);
  await page.getByRole('button', {name:'Theology', exact:true}).click();
  await expect(active.getByRole('heading')).toHaveText('Theology');
  expect(await page.evaluate(() => [history.length, history.state])).toEqual([mark,{testMarker:true}]);
  await expect(page).toHaveURL(address);
  await page.reload();
  await expect(active.getByRole('heading')).toHaveText('Theology');
  await expect(page).toHaveURL(address);
  await page.evaluate(() => localStorage.setItem('make-something-carousel-v1:/', 'stories/removed/removed.md'));
  await page.reload();
  await expect(active.getByRole('heading')).toHaveText('Cookbook');
});

test('carousel continues navigating when storage is blocked', async ({page}) => {
  await page.addInitScript(() => Object.defineProperty(window, 'localStorage', {get: () => { throw new Error('storage blocked'); }}));
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.goto('/');
  const active = page.locator('.carousel-slide:visible');
  await expect(active.getByRole('heading')).toHaveText('Cookbook');
  await page.getByRole('button', {name:'Next story'}).click();
  await expect(active.getByRole('heading')).toHaveText('Settlement');
  await expect(page).toHaveURL(/\/$/);
});

test('the direct ending offers only End, which dismisses and stays in the story', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.route('**/stories/mars/mars.md', route => route.fulfill({contentType:'text/markdown', body:story}));
  await page.goto('/index.html?story=stories/mars/mars.md');
  const address = page.url();
  await page.getByRole('button', {name:'Start', exact:true}).click();
  await page.getByRole('button', {name:'Begin', exact:true}).click();
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await page.getByRole('button', {name:'Continue story'}).click();
  await expect(page.getByRole('link', {name:'Home', exact:true})).toHaveCount(0);
  await page.getByRole('button', {name:'End', exact:true}).click();
  await expect(page.locator('dialog')).toHaveCount(0);
  await expect(page.getByText('The End', {exact:true})).toBeVisible();
  await expect(page).toHaveURL(address);
  await page.getByRole('button', {name:'Read this chapter'}).click();
  await expect(page.getByRole('link', {name:'Home', exact:true})).toHaveCount(0);
  await expect(page.getByRole('button', {name:'Restart story', exact:true})).toBeVisible();
});

test('arrow buttons slide in both directions quickly, retain focus and accept repeat clicks', async ({page}) => {
  await page.goto('/');
  const visible = page.locator('.carousel-slide:not([hidden])');
  const active = page.locator('.carousel-slide:not([inert]) h2');
  const next = page.getByRole('button', {name:'Next story'});
  await next.focus();
  const hit = (await next.boundingBox())!;
  // Sample a real interpolation during the CSS transform, not just its ends.
  const sample = (direction: number) => page.evaluate(direction => new Promise<boolean>(resolve => {
    const first = document.querySelector<HTMLElement>('.carousel-slide:not([inert])')!;
    let remaining = 30;
    function frame() {
      const value = getComputedStyle(first).transform;
      const x = value === 'none' ? 0 : new DOMMatrix(value).m41;
      if (direction * x > 2 && Math.abs(x) < first.clientWidth - 2) resolve(getComputedStyle(first).transitionDuration === '0.5s');
      else if (remaining-- > 0) requestAnimationFrame(frame);
      else resolve(false);
    }
    requestAnimationFrame(frame);
  }), direction);
  const first = sample(-1);
  await page.keyboard.press('Enter');
  expect(await first).toBe(true);
  await page.mouse.click(hit.x + hit.width / 2, hit.y + hit.height / 2);
  await expect(active).toHaveText('Creation');
  await expect(visible).toHaveCount(1);
  await expect(next).toBeFocused();

  const previous = page.getByRole('button', {name:'Previous story'});
  await previous.focus();
  const reverse = sample(1);
  await page.keyboard.press('Enter');
  expect(await reverse).toBe(true);
  await expect(active).toHaveText('Settlement');
  await expect(visible).toHaveCount(1);
  await expect(previous).toBeFocused();
  await expect(page.locator('.carousel-slide.is-settling')).toHaveCount(0);
  await expect(page).toHaveURL(/\/$/);
});

test('the development carousel keeps its footer above the edge and opens links separately on touch', async ({browser}) => {
  const context = await browser.newContext({isMobile:true, hasTouch:true, viewport:{width:390,height:844}});
  try {
    const page = await context.newPage();
    await context.route('https://unto.me/make-something/*.html', route => route.fulfill({body:'App information'}));
    await page.goto('/index-dev.html');
    const address = page.url();
    const footer = page.getByRole('navigation', {name:'App information'});
    const position = await footer.boundingBox();
    expect(position).not.toBeNull();
    expect(position!.y + position!.height).toBeLessThan(844);

    await page.getByRole('button', {name:'Theology', exact:true}).tap();
    await expect(page.locator('.carousel-slide:visible h2')).toHaveText('Theology');
    expect(await footer.boundingBox()).toEqual(position);
    const active = page.locator('.carousel-slide:not([hidden])');
    await expect(active).toHaveAttribute('data-ink', /dark|light/);
    const {color, fontSize} = await active.locator('.carousel-description').evaluate(el => {
      const {color, fontSize} = getComputedStyle(el);
      return {color, fontSize};
    });
    for (const name of ['Support', 'Privacy']) {
      const link = footer.getByRole('link', {name});
      await expect(link).toHaveCSS('color', color);
      await expect(link).toHaveCSS('font-size', fontSize);
      await expect(link).toHaveCSS('text-decoration-line', 'underline');
      const [popup] = await Promise.all([page.waitForEvent('popup'), link.tap()]);
      await expect(popup).toHaveURL(`https://unto.me/make-something/${name.toLowerCase()}.html`);
      await popup.close();
      await expect(link).toHaveCSS('color', color);
    }
    await expect(page).toHaveURL(address);
  } finally { await context.close(); }
});

test('the carousel blur follows visible text and keeps long descriptions scrollable', async ({page}) => {
  await page.setViewportSize({width:320,height:568});
  await page.goto('/');
  const active = page.locator('.carousel-slide:not([inert])');
  const layer = () => active.evaluate(slide => {
    const panel = slide.querySelector<HTMLElement>('.carousel-description-frame')!;
    const backdrop = getComputedStyle(panel, '::before');
    const abstract = slide.querySelector<HTMLElement>('.carousel-description')!;
    const panelBox = panel.getBoundingClientRect();
    const clip = abstract.getBoundingClientRect();
    const range = document.createRange();
    range.selectNodeContents(abstract.querySelector('p')!);
    const lastLine = Math.max(...Array.from(range.getClientRects())
      .filter(rect => rect.top < clip.bottom && rect.bottom > clip.top)
      .map(rect => Math.min(rect.bottom, clip.bottom)));
    const coveredHeight = parseFloat(backdrop.height);
    return {
      bounded: panelBox.top + parseFloat(backdrop.top) > 0 && panelBox.bottom < innerHeight,
      height: coveredHeight,
      panelHeight: panelBox.height,
      edgeToText: panelBox.bottom - parseFloat(backdrop.bottom) - lastLine,
      actual: {
        textLayer: getComputedStyle(abstract).zIndex,
        noPointerInterception: backdrop.pointerEvents,
        feathered: backdrop.maskImage.startsWith('linear-gradient('),
        blur: backdrop.backdropFilter,
        tint: backdrop.backgroundColor,
        shadow: getComputedStyle(abstract).textShadow,
      },
    };
  });
  const short = await layer();
  expect(short.bounded).toBe(true);
  expect(Math.abs(short.edgeToText)).toBeLessThan(3);
  expect(short.height).toBeLessThan(short.panelHeight - 15);
  await page.getByRole('button', {name:'Theology',exact:true}).click();
  await expect(active.getByRole('heading')).toHaveText('Theology');
  const long = await layer();
  expect(long.bounded).toBe(true);
  expect(long.height).toBeGreaterThan(short.height + 45);
  expect(Math.abs(long.edgeToText)).toBeLessThan(3);
  expect(long.actual).toEqual({
    textLayer:'1', noPointerInterception:'none', feathered:true,
    blur:'blur(3px)', tint:'rgba(0, 0, 0, 0)', shadow:'none',
  });
  // A constrained window still scrolls the abstract and bounds the backdrop
  // by the visible panel, not by the full scrollable document.
  await page.setViewportSize({width:320,height:300});
  const prose = active.locator('.carousel-description');
  await expect.poll(() => prose.evaluate(el => el.scrollHeight - el.clientHeight)).toBeGreaterThan(0);
  await prose.hover();
  await page.mouse.wheel(0, 120);
  await expect.poll(() => prose.evaluate(el => el.scrollTop)).toBeGreaterThan(0);
  const constrained = await layer();
  expect(constrained.height).toBeLessThan(long.height);
  expect(Math.abs(constrained.edgeToText)).toBeLessThan(3);
});

test('the subtitle chooses ink for the card and the footer links have separate blurs', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  const cover = (art: string) => `<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844">${art}</svg>`;
  await page.route('**/backgrounds/breakfast.webp', route => route.fulfill({contentType:'image/svg+xml', body:cover(`
    <rect width="390" height="844" fill="white"/>
    <rect x="185" width="20" height="650" fill="black"/>
    <rect x="195" y="740" width="195" height="104" fill="black"/>`)}));
  await page.route('**/settlement/assets/backgrounds/01.webp', route => route.fulfill({contentType:'image/svg+xml', body:cover(`
    <rect width="390" height="844" fill="black"/>`)}));
  await page.goto('/');
  const active = page.locator('.carousel-slide:not([hidden])');
  const description = active.locator('.carousel-description');
  const support = active.getByRole('link', {name:'Support'});
  const privacy = active.getByRole('link', {name:'Privacy'});
  await expect(description).toHaveCSS('color', 'rgb(0, 0, 0)');
  await expect(support).toHaveCSS('color', 'rgb(0, 0, 0)');
  await expect(privacy).toHaveCSS('color', 'rgb(0, 0, 0)');
  for (const link of [support, privacy]) {
    await expect(link).toHaveCSS('text-shadow', 'none');
    expect(await link.evaluate(el => getComputedStyle(el, '::before').backdropFilter)).toBe('blur(2px)');
  }
  expect(await active.locator('.carousel-footer').evaluate(el => getComputedStyle(el, '::before').backdropFilter)).toBe('none');
  await active.getByRole('button', {name:'Settlement', exact:true}).click();
  await expect(active).toHaveAttribute('data-ink', 'light');
  await expect(description).toHaveCSS('color', 'rgb(255, 255, 255)');
  await expect(support).toHaveCSS('color', 'rgb(255, 255, 255)');
  await expect(privacy).toHaveCSS('color', 'rgb(255, 255, 255)');
});

test('a move-only first chapter says Start but keeps saved positions; combining changes it to Continue', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  const unfinished = story.replace('- Kit\n','- Kit\n- Spare\n')
    .replace('- Build -- Kit','- Build -- Kit\n- Find -- Spare')
    .replace('-> Kit','-> Kit\n- Kit [preserve] + Tool [preserve] -> Spare');
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType:'text/markdown',body:unfinished}));
  await page.goto('/');
  const card = page.locator('a[data-story="stories/cookbook/cookbook.md"]');
  await expect(card).toContainText('Start');
  await card.click();
  await page.getByRole('button',{name:'Begin',exact:true}).click();

  const item = page.locator('[data-item="name:Frame"]'), starting = (await item.boundingBox())!;
  await page.mouse.move(starting.x + starting.width / 2, starting.y + starting.height / 2);
  await page.mouse.down();
  await page.mouse.move(85, 450, {steps:5});
  await page.mouse.up();
  const moved = (await item.boundingBox())!;
  expect(Math.abs(moved.y - starting.y)).toBeGreaterThan(30);
  const goals = page.getByRole('button',{name:'Read this chapter'});
  const home = page.getByRole('link',{name:'Home',exact:true});
  await goals.click();
  await expect(page.getByRole('button',{name:'Restart story',exact:true})).toBeVisible();
  await home.click();
  await expect(card).toContainText('Start');
  await card.click();
  await expect(page.getByRole('dialog')).toContainText('Make a kit.');
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  await expect(item).toBeVisible();
  expect((await item.boundingBox())!.x).toBeCloseTo(moved.x, 0);
  expect((await item.boundingBox())!.y).toBeCloseTo(moved.y, 0);

  await item.dragTo(page.locator('[data-item="name:Tool"]'));
  await expect(page.locator('[data-item="name:Kit"]')).toBeVisible();
  await goals.click();
  await expect(page.getByRole('button',{name:'Restart chapter',exact:true})).toBeVisible();
  await home.click();
  await expect(card).toContainText('Continue');
});

test('swiping restores an open wonder and tapping Continue clears it before Begin', async ({page}) => {
  const twoChapters = story.replace('## Ending\nThe kit is ready.', `## Field
The workshop is behind you.

**Items**
- Probe
- Sample

  You found a sample.

- Spare

**Goals**
- Make the spare -- Spare

**Combinations**
- Kit [preserve] + Probe [preserve] -> Sample
- Sample [preserve] + Probe [preserve] -> Spare
`);
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.route('**/stories/mars/mars.md', route => route.fulfill({contentType:'text/markdown', body:twoChapters}));
  const launch = async () => {
    await page.goto('/');
    await page.getByRole('button', {name:'Mission to Mars', exact:true}).click();
    await page.locator('.carousel-slide:visible a[data-story]').click();
  };
  const begin = page.getByRole('button', {name:'Begin', exact:true});
  const reading = page.getByRole('dialog');
  await launch();
  await begin.click();
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await page.getByRole('button', {name:'Continue story'}).click();
  await expect(reading).toContainText('The workshop is behind you.');
  await begin.click();
  await page.locator('[data-item="name:Kit"]').dragTo(page.locator('[data-item="name:Probe"]'));
  await expect(reading).toContainText('You found a sample.');

  const drag = async (x: number, from: number, to: number) => {
    await page.mouse.move(x, from);
    await page.mouse.down();
    await page.mouse.move(x, to, {steps:5});
    await page.mouse.up();
  };
  const card = page.locator('.carousel-slide:visible a[data-story="stories/mars/mars.md"]');
  await drag(7, 190, 390);
  await expect(card).toBeFocused();
  await drag(20, 690, 390);
  await expect(reading).toContainText('You found a sample.');
  await expect(reading.getByRole('button', {name:'Continue',exact:true})).toBeFocused();

  await page.reload();
  await expect(reading).toContainText('You found a sample.');
  await drag(7, 190, 390);
  await expect(page).toHaveURL(/\/index.html$/);
  await expect(card).toBeVisible();
  await card.click();
  await expect(reading).toContainText('The workshop is behind you.');
  await begin.click();
  await expect(reading).toHaveCount(0);
  await expect(page.locator('[data-item="name:Sample"]')).toBeVisible();
  await page.locator('[data-item="name:Sample"]').dblclick();
  await expect(reading).toHaveAccessibleName('Encyclopedia');
  await expect(reading).toContainText('You found a sample.');
  await drag(7, 190, 390);
  await expect(reading).toHaveAccessibleName('Encyclopedia');
  await page.reload();
  await expect(page.locator('[data-item="name:Sample"]')).toBeVisible();
  await expect(reading).toHaveCount(0);
});
