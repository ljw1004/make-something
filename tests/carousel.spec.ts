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

test('Start skips the cover, final Home preserves progress, and Restart clears shared tutorial flags', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.route('**/stories/cookbook/cookbook.md', route => route.fulfill({contentType:'text/markdown', body:story}));
  await page.route('**/stories/mars/mars.md', route => route.fulfill({contentType:'text/markdown', body:story}));
  const active = page.locator('.carousel-slide:visible');
  await page.goto('/');
  await page.getByRole('button', {name:'Cookbook', exact:true}).click();
  await expect(active.getByRole('link')).toContainText('Start');
  await active.getByRole('link').click();
  await expect(page.getByRole('button', {name:'Begin'})).toBeVisible();
  await page.getByRole('button', {name:'Begin'}).click();
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await page.getByRole('button', {name:'Continue story'}).click();
  await expect(page.getByText('The kit is ready.', {exact:true})).toBeVisible();
  await expect(page.getByRole('button', {name:'Begin'})).toHaveCount(0);
  await page.getByRole('link', {name:'Home', exact:true}).click();
  await expect(active.getByRole('heading')).toHaveText('Cookbook');
  await expect(active.getByRole('link')).toContainText('Continue');
  await active.getByRole('link').click();
  await expect(page.getByText('The End', {exact:true})).toBeVisible();
  await page.getByRole('button', {name:'Read this chapter'}).click();
  const home = page.getByRole('link', {name:'Home', exact:true});
  const restart = page.getByRole('button', {name:'Restart', exact:true});
  await expect(home).toBeVisible();
  await expect(restart).toBeVisible();
  expect((await home.boundingBox())!.x).toBeLessThan((await restart.boundingBox())!.x);
  await home.click();
  const tutorialKey = await page.evaluate(() => 'combination-tutorial-v1:' + encodeURIComponent(new URL('index.html', location.href).href));
  expect(await page.evaluate(key => JSON.parse(localStorage.getItem(key)!).dragDone, tutorialKey)).toBe(true);
  await page.getByRole('button', {name:'Mission to Mars', exact:true}).click();
  await active.getByRole('link').click();
  await page.getByRole('button', {name:'Begin'}).click();
  await page.getByRole('button', {name:'Read this chapter'}).click();
  await page.getByRole('button', {name:/Restart this story/}).click();
  await page.getByRole('button', {name:'Restart story', exact:true}).click();
  await expect(page.getByRole('button', {name:'Start', exact:true})).toBeVisible();
  expect(await page.evaluate(key => localStorage.getItem(key), tutorialKey)).toBeNull();
  await page.reload();
  await expect(page.getByRole('button', {name:'Start', exact:true})).toBeVisible();
  await page.goto('/?slide=stories/cookbook/cookbook.md');
  await expect(active.getByRole('link')).toContainText('Continue');
});

test('carousel wraps, swipes across the artwork, and launches a touch tutorial', async ({browser}) => {
  const context = await browser.newContext({isMobile:true, hasTouch:true, viewport:{width:390,height:844}});
  try {
    const page = await context.newPage();
    await page.goto('/');
    const active = page.locator('.carousel-slide:visible');
    const title = active.getByRole('heading');
    const first = await title.textContent();
    await page.getByRole('button', {name:'Previous story'}).click();
    await expect(title).not.toHaveText(first!);
    await page.getByRole('button', {name:'Next story'}).click();
    await expect(title).toHaveText(first!);
    const client = await context.newCDPSession(page);
    await client.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[{x:290,y:220}]});
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:230,y:220}]});
    const translated = () => page.locator('.carousel-slide:not([hidden])').evaluateAll(slides => slides.map(slide =>
      ['.carousel-art','.carousel-bar','.carousel-description'].map(selector => slide.querySelector(selector)!.getBoundingClientRect().x)));
    await expect.poll(translated).toEqual([[-60,-60,-60],[330,330,330]]);
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:90,y:220}]});
    await expect.poll(translated).toEqual([[-200,-200,-200],[190,190,190]]);
    await client.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[]});
    await expect(active).toHaveCount(1);
    await expect(title).not.toHaveText(first!);
    await expect.poll(translated).toEqual([[0,0,0]]);
    const second = await title.textContent();
    await client.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[{x:160,y:220}]});
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:186,y:220}]});
    await expect.poll(translated).toEqual([[-364,-364,-364],[26,26,26]]);
    await client.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[]});
    await expect(active).toHaveCount(1);
    await expect(title).toHaveText(second!);
    await client.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[{x:100,y:220}]});
    await client.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{x:250,y:220}]});
    await expect.poll(translated).toEqual([[-240,-240,-240],[150,150,150]]);
    await client.send('Input.dispatchTouchEvent', {type:'touchEnd', touchPoints:[]});
    await expect(active).toHaveCount(1);
    await expect(title).toHaveText(first!);
    await page.getByRole('button', {name:'Cookbook', exact:true}).tap();
    await expect(title).toHaveText('Cookbook');
    await active.getByRole('link').tap();
    await expect(page).toHaveURL(/launch=touch/);
    await expect(page.locator('.tutorial-overlay')).toHaveAttribute('data-modality', 'touch');
    await expect(page.getByRole('button', {name:'Begin'})).toBeVisible();
  } finally { await context.close(); }
});

test('theology banner sits near mid-screen and the full smaller abstract is readable', async ({page}) => {
  await page.goto('/?slide=stories/theology/theology.md');
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
        compactType: parseFloat(getComputedStyle(abstract).fontSize) <= 17,
      };
    })).toEqual({nearMiddle:true,fullAbstract:true,compactType:true});
  }
});
