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
  await page.goto('/');
  await page.getByRole('button', {name:'Mission to Mars', exact:true}).click();
  await expect(active.getByRole('link')).toContainText('Start');
  await active.getByRole('link').click();
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
  await expect(active.getByRole('link')).toContainText('Continue');
  await active.getByRole('link').click();
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
  await expect(active.getByRole('link')).toContainText('Continue');
  const tutorialKey = await page.evaluate(() => 'combination-tutorial-v1:' + encodeURIComponent(new URL('index.html', location.href).href));
  expect(await page.evaluate(key => JSON.parse(localStorage.getItem(key)!).goalsDone, tutorialKey)).toBe(true);
  const dragKeys = await page.evaluate(() => ['mars/mars', 'cookbook/cookbook'].map(path =>
    'combination-tutorial-drag-v2:' + encodeURIComponent(new URL('stories/' + path + '.md', location.href).href)));
  expect(await page.evaluate(keys => keys.map(key => localStorage.getItem(key)), dragKeys)).toEqual(['true', null]);
  await page.getByRole('button', {name:'Cookbook', exact:true}).click();
  await active.getByRole('link').click();
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
  await expect(active.getByRole('link')).toContainText('Continue');
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
    await expect(page.getByRole('button', {name:'Creation', exact:true})).toBeFocused();
    await page.keyboard.press('ArrowLeft');
    await expect(page.getByRole('button', {name:first!, exact:true})).toBeFocused();
    await page.getByRole('button', {name:'Previous story'}).click();
    await expect(title).not.toHaveText(first!);
    await page.getByRole('button', {name:'Next story'}).click();
    await expect(title).toHaveText(first!);
    await expect(page).toHaveURL(address);
    const client = await context.newCDPSession(page);
    await client.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[{x:290,y:220}]});
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:230,y:220}]});
    const translated = () => page.locator('.carousel-slide:not([hidden])').evaluateAll(slides => slides.map(slide =>
      ['.carousel-art','.carousel-bar','.carousel-dots','.carousel-description'].map(selector => {
        const node = slide.querySelector<HTMLElement>(selector)!;
        return node.getBoundingClientRect().x - (selector === '.carousel-bar' ? parseFloat(getComputedStyle(node).marginLeft) : 0);
      })));
    await expect.poll(translated).toEqual([[-60,-60,-60,-60],[330,330,330,330]]);
    expect(await page.locator('.carousel-slide:not([hidden]) .carousel-dots [aria-current="true"]').evaluateAll(dots =>
      dots.map(dot => dot.getAttribute('aria-label')))).toEqual([first, 'Creation']);
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:90,y:220}]});
    await expect.poll(translated).toEqual([[-200,-200,-200,-200],[190,190,190,190]]);
    await client.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[]});
    await expect(active).toHaveCount(1);
    await expect(title).not.toHaveText(first!);
    await expect.poll(translated).toEqual([[0,0,0,0]]);
    await expect(page).toHaveURL(address);
    await page.reload();
    await expect(title).toHaveText('Creation');
    const second = await title.textContent();
    await client.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[{x:160,y:380}]});
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:186,y:380}]});
    await expect.poll(translated).toEqual([[-364,-364,-364,-364],[26,26,26,26]]);
    await client.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[]});
    await expect(active).toHaveCount(1);
    await expect(title).toHaveText(second!);
    await client.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[{x:100,y:220}]});
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:250,y:220}]});
    await expect.poll(translated).toEqual([[-240,-240,-240,-240],[150,150,150,150]]);
    await client.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[]});
    await expect(active).toHaveCount(1);
    await expect(title).toHaveText(first!);
    await page.getByRole('button', {name:'Cookbook', exact:true}).tap();
    await expect(title).toHaveText('Cookbook');
    await expect(page).toHaveURL(address);
    await active.getByRole('link').tap();
    await expect(page).toHaveURL(/\/make-something.html\?story=stories\/cookbook\/cookbook\.md$/);
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
  const mark = await page.evaluate(() => {
    history.replaceState({testMarker:true}, '');
    return history.length;
  });
  await page.getByRole('button', {name:'Previous story'}).click();
  await expect(active.getByRole('heading')).toHaveText('Theology');
  await expect(page).toHaveURL(address);
  await page.getByRole('button', {name:'History of ideas', exact:true}).click();
  await expect(active.getByRole('heading')).toHaveText('History of ideas');
  expect(await page.evaluate(() => [history.length, history.state])).toEqual([mark,{testMarker:true}]);
  await expect(page).toHaveURL(address);
  await page.reload();
  await expect(active.getByRole('heading')).toHaveText('History of ideas');
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
  await expect(active.getByRole('heading')).toHaveText('Creation');
  await expect(page).toHaveURL(/\/$/);
});

test('the direct ending offers only End, which dismisses and stays in the story', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.route('**/stories/mars/mars.md', route => route.fulfill({contentType:'text/markdown', body:story}));
  await page.goto('/make-something.html?story=stories/mars/mars.md');
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
  await expect(active).toHaveText('History of ideas');
  await expect(visible).toHaveCount(1);
  await expect(next).toBeFocused();

  const previous = page.getByRole('button', {name:'Previous story'});
  await previous.focus();
  const reverse = sample(1);
  await page.keyboard.press('Enter');
  expect(await reverse).toBe(true);
  await expect(active).toHaveText('Creation');
  await expect(visible).toHaveCount(1);
  await expect(previous).toBeFocused();
  await expect(page.locator('.carousel-slide.is-settling')).toHaveCount(0);
  await expect(page).toHaveURL(/\/$/);
});

test('the single carousel backdrop follows the visible abstract and stays below white text', async ({page}) => {
  await page.setViewportSize({width:320,height:568});
  await page.goto('/');
  const active = page.locator('.carousel-slide:not([inert])');
  const layer = () => active.evaluate(slide => {
    const panel = slide.querySelector<HTMLElement>('.carousel-panel')!;
    const backdrop = getComputedStyle(panel, '::before');
    const abstract = slide.querySelector<HTMLElement>('.carousel-description')!;
    const panelBox = panel.getBoundingClientRect();
    const coveredHeight = parseFloat(backdrop.height);
    return {
      bounded: panelBox.top + parseFloat(backdrop.top) > 0 && panelBox.bottom < innerHeight,
      height: coveredHeight,
      panelHeight: panelBox.height,
      lowerEdge: backdrop.bottom,
      actual: {
        aboveArt: getComputedStyle(panel).isolation,
        behindText: [backdrop.zIndex, getComputedStyle(abstract).zIndex],
        noPointerInterception: backdrop.pointerEvents,
        gradient: backdrop.backgroundImage.startsWith('linear-gradient('),
        textColor: getComputedStyle(abstract).color,
        extraBarShadow: getComputedStyle(slide.querySelector('.carousel-bar')!).boxShadow,
      },
    };
  });
  const short = await layer();
  expect(short.bounded).toBe(true);
  expect(short.lowerEdge).toBe('0px');
  expect(short.height).toBeCloseTo(short.panelHeight + 14, 0);
  await page.getByRole('button', {name:'Theology',exact:true}).click();
  await expect(active.getByRole('heading')).toHaveText('Theology');
  await page.addStyleTag({content:'.carousel-frame{--carousel-backdrop-color:#000}'});
  const long = await layer();
  expect(long.bounded).toBe(true);
  expect(long.height).toBeGreaterThan(short.height + 45);
  expect(long.height).toBeCloseTo(long.panelHeight + 14, 0);
  expect(long.actual).toEqual({
    aboveArt:'isolate', behindText:['-1','1'], noPointerInterception:'none', gradient:true,
    textColor:'rgb(255, 255, 255)', extraBarShadow:'none',
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
  expect(constrained.height).toBeCloseTo(constrained.panelHeight + 14, 0);
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

test('Continue reopens an acknowledged later chapter before any saved discovery', async ({page}) => {
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

  await launch();
  await expect(reading).toContainText('The workshop is behind you.');
  await begin.click();
  await expect(reading).toContainText('You found a sample.');
  await page.getByRole('button', {name:'Continue', exact:true}).click();
  await expect(page.locator('[data-item="name:Sample"]')).toBeVisible();
  await page.reload();
  await expect(page.locator('[data-item="name:Sample"]')).toBeVisible();
  await expect(reading).toHaveCount(0);
});
