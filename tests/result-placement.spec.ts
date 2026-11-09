import {test, expect} from '@playwright/test';

test('a result overlaps its preserved receiver while avoiding another fixed receiving area', async ({page}) => {
    await page.emulateMedia({reducedMotion:'reduce'});
    const manuscript=`# A clear place for the result
## Work
background: ![room](room.svg)
Use the paper at the machine.
**Goals**
- Print -- Result
**Hotspots**
- Whole setup (center 295px, 250px)
  - icon: ![whole setup](setup.svg)
  - hitbox: (center 240px, 240px) (size 100px, 100px)
**Items**
- Whole setup
- Paper
  - icon: ![paper](part.svg) (center 50px, 550px)
- Machine
  - icon: ![machine](part.svg) (center 160px, 150px)
- Result
  - icon: ![result](part.svg)
**Combinations**
- Paper [consume] + Machine [preserve] -> Result`;
    await page.route('**/result-space/story.md', route => route.fulfill({contentType:'text/markdown',body:manuscript}));
    await page.route('**/result-space/*.svg', route => {
      const file=new URL(route.request().url()).pathname.split('/').at(-1);
      const [width,height]=file==='room.svg'?[390,844]:file==='setup.svg'?[800,400]:[320,320];
      return route.fulfill({contentType:'image/svg+xml',body:`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}"><rect width="${width}" height="${height}" fill="${file==='room.svg'?'#efe9da':'#518794'}"/></svg>`});
    });
    await page.goto('/make-something.html?story=result-space/story.md');
    await page.getByRole('button',{name:'Start',exact:true}).click();
    await page.getByRole('button',{name:'Begin',exact:true}).click();
    const receiver=page.locator('[data-item="name:Machine"]'), before=(await receiver.boundingBox())!;
    const paper=(await page.locator('[data-item="name:Paper"]').boundingBox())!;
    await page.mouse.move(paper.x+paper.width/2,paper.y+paper.height/2);
    await page.mouse.down();
    await page.mouse.move(before.x+before.width/2,before.y+before.height/2,{steps:8});
    await page.mouse.up();
    const result=page.locator('[data-item="name:Result"]');
    await expect(result).toBeVisible();
    const created=(await result.boundingBox())!;
    expect(await receiver.boundingBox()).toEqual(before);
    for(const obstacle of [page.locator('[data-hotspot="name:Whole setup"]')]){
      const box=(await obstacle.boundingBox())!;
      expect(Math.min(created.x+created.width,box.x+box.width)<=Math.max(created.x,box.x)+.1||Math.min(created.y+created.height,box.y+box.height)<=Math.max(created.y,box.y)+.1).toBe(true);
    }
    expect(Math.min(created.x+created.width,before.x+before.width)-Math.max(created.x,before.x)).toBeGreaterThan(0);
    expect(Math.min(created.y+created.height,before.y+before.height)-Math.max(created.y,before.y)).toBeGreaterThan(0);
    await page.reload();
    await expect(result).toBeVisible();
    expect(await result.boundingBox()).toEqual(created);
    expect(await receiver.boundingBox()).toEqual(before);
  });

for (const authored of [false,true]) test(`a transformed result stays at ${authored ? 'its authored hotspot position' : 'the receiving hotspot centre'}`, async ({page}) => {
  await page.setViewportSize({width:390,height:664});
  await page.emulateMedia({reducedMotion:'reduce'});
  const manuscript=`# Baking
## Work
background: ![page](page.svg)
**Goals**
- Bake -- Bread
**Hotspots**
- Oven (center 280px, 200px)
${authored ? '  - place: Bread (center 300px, 220px)' : ''}
**Items**
- Oven
- Dough
  - icon: ![dough](dough.svg) (center 100px, 420px)
- Bread
  - icon: ![bread](bread.svg)
**Combinations**
- Dough [transform] @ Oven -> Bread`;
  await page.route('**/hotspot-result/story.md',r=>r.fulfill({contentType:'text/markdown',body:manuscript}));
  await page.route('**/hotspot-result/*.svg',r=>{
    const file=new URL(r.request().url()).pathname.split('/').at(-1);
    const [w,h]=file==='page.svg'?[390,844]:file==='bread.svg'?[320,240]:[160,160];
    return r.fulfill({contentType:'image/svg+xml',body:`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><rect width="100%" height="100%" fill="${file==='page.svg'?'white':'orange'}"/></svg>`});
  });
  await page.goto('/make-something.html?story=hotspot-result/story.md');
  await page.getByRole('button',{name:'Start',exact:true}).click();
  const oven=page.locator('[data-hotspot="name:Oven"]'), target=(await oven.boundingBox())!;
  await page.locator('[data-item="name:Dough"]').dragTo(oven);
  const result=page.locator('[data-item="name:Bread"]');
  await expect(result).toBeVisible();
  await expect(page.locator('[data-item="name:Dough"]')).toHaveCount(0);
  const bounds=(await result.boundingBox())!,offset=authored?20:0;
  expect(bounds.x+bounds.width/2).toBeCloseTo(target.x+target.width/2+offset,1);
  expect(bounds.y+bounds.height/2).toBeCloseTo(target.y+target.height/2+offset,1);
  expect(await oven.boundingBox()).toEqual(target);
  await expect(page.getByRole('dialog')).toHaveCount(0);
  await page.reload();await expect(result).toBeVisible();expect(await result.boundingBox()).toEqual(bounds);
});
