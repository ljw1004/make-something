import {test, expect} from '@playwright/test';

test('small icons and circular hotspots keep authored hit areas through scene scaling', async ({page}) => {
  const manuscript = `# Small drawings
## Work
background: ![room](room.svg)
**Goals**
- Finish -- C
**Hotspots**
- Circle (center 250px, 300px)
  - icon: ![circle](small.svg) (circular)
**Items**
- Circle
- A
  - icon: ![part](small.svg) (center 150px, 300px)
- B
- C
**Combinations**
- A + B -> C`;
  await page.route('**/authored-targets/story.md', route => route.fulfill({contentType:'text/markdown', body:manuscript}));
  await page.route('**/authored-targets/*.svg', route => {
    const [width,height] = route.request().url().endsWith('room.svg') ? [390,844] : [40,80];
    return route.fulfill({contentType:'image/svg+xml', body:`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}"><rect width="100%" height="100%" fill="#567"/></svg>`});
  });
  await page.goto('/make-something.html?story=authored-targets/story.md');
  await page.getByRole('button',{name:'Start',exact:true}).click();
  for (const viewport of [{width:390,height:844},{width:320,height:568},{width:844,height:390}]) {
    await page.setViewportSize(viewport);
    const panel = page.locator('.chapter-panel'), item = page.locator('[data-item="name:A"]'), hotspot = page.locator('[data-hotspot="name:Circle"]');
    await expect(item).toBeVisible();
    const scale = (viewport.height > viewport.width ? Math.max : Math.min)(viewport.width/390, viewport.height/844);
    await expect.poll(() => panel.evaluate(el => Number(getComputedStyle(el).getPropertyValue('--board-scale')))).toBeCloseTo(scale,5);
    for (const target of [item,hotspot]) {
      const box = (await target.boundingBox())!;
      expect(box.width).toBeCloseTo(10*scale,1);
      expect(box.height).toBeCloseTo(20*scale,1);
      const centre = {x:box.x+box.width/2,y:box.y+box.height/2};
      const hit = (point: {x:number;y:number}) => target.evaluate((el,p) => !!document.elementFromPoint(p.x,p.y)?.closest('[data-item],[data-hotspot]')?.isSameNode(el), point);
      expect(await hit(centre)).toBe(true);
      expect(await hit({x:box.x-3,y:centre.y})).toBe(false);
      if (target === hotspot) expect(await hit({x:centre.x,y:box.y+scale})).toBe(false);
    }
  }
});
