import {test,expect,type Page} from '@playwright/test';

const story=`# Responsive scenes
## First
background: ![portrait](portrait.svg)
**Goals**
- Build -- Kit
**Items**
- Frame
- Tool
**Combinations**
- Frame [preserve] + Tool [preserve] -> Kit
## Second
background: ![wide](wide.svg)
**Goals**
- Finish -- Final
**Items**
- Kit
- Probe
- Station
**Hotspots**
- Station (center 768px, 192px)
**Combinations**
- Kit [preserve] + Probe [preserve] -> Final
`;
async function open(page:Page,wide=false,source=story){
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.route('**/responsive/story.md',r=>r.fulfill({contentType:'text/plain',body:wide?source.replace('portrait.svg','wide.svg'):source}));
  await page.route('**/responsive/*.svg',r=>{
    const file = new URL(r.request().url()).pathname.split('/').at(-1);
    const [width,height] = file === 'wide.svg' ? [1024,768] : file === 'frame.svg' ? [160,160] : [780,1688];
    return r.fulfill({contentType:'image/svg+xml',body:`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}"><rect width="100%" height="100%" fill="#567"/><path d="M0 0H${width}V${height}H0Z" fill="none" stroke="#fc0" stroke-width="12"/></svg>`});
  });
  await page.goto('/index.html?story=responsive/story.md');
  await page.getByRole('button',{name:'Start',exact:true}).click();
}
const box=(page:Page,selector:string)=>page.locator(selector).last().boundingBox();

test('the carousel uses a full-height phone scene and centered black desktop gutters', async ({page}) => {
  await page.goto('/index.html');
  await expect.poll(async () => (await box(page, '.carousel-frame'))?.width).toBe(390);
  await expect.poll(async () => (await box(page, '.carousel-frame'))?.height).toBe(844);
  await page.setViewportSize({width: 1600, height: 1000});
  await expect.poll(async () => (await box(page, '.carousel-frame'))?.x).toBeGreaterThan(0);
  const frame = (await box(page, '.carousel-frame'))!;
  expect(frame.x + frame.width / 2).toBeCloseTo(800, 0);
  expect(await page.locator('#catalogue-app').evaluate(el => getComputedStyle(el).backgroundColor)).toBe('rgb(0, 0, 0)');
});

test('phone and tablet proportions fill, landscape panes fit the full scene and scale its cards',async({page})=>{
  await open(page);
  for(const size of [{width:390,height:664},{width:440,height:956},{width:484,height:1112},{width:512,height:683},{width:1024,height:1366}]){
    await page.setViewportSize(size);
    await expect.poll(async()=>Math.round((await box(page,'.chapter-panel'))!.width)).toBe(size.width);
    await expect.poll(async()=>(await box(page,'.chapter-panel'))!.height).toBeCloseTo(size.height,1);
    expect((await box(page,'.chapter-panel'))!.x).toBeCloseTo(0,1);
  }
  await page.setViewportSize({width:1024,height:1080});
  await expect.poll(async()=>(await box(page,'.chapter-panel'))!.width).toBeCloseTo(390*1080/844,1);
  expect((await box(page,'.scene-art'))!.height).toBeCloseTo(1080,1);
  await page.setViewportSize({width:1920,height:1200});
  await expect.poll(async()=>(await box(page,'.chapter-panel'))!.width).toBeCloseTo(390*1200/844,1);
  const scene=(await box(page,'.chapter-panel'))!,image=(await box(page,'.scene-art'))!;
  expect(image.width).toBeCloseTo(scene.width,1); expect(image.height).toBeCloseTo(scene.height,1);
  expect(scene.x).toBeCloseTo((1920-scene.width)/2,1);
  expect((await box(page,'[data-item="name:Frame"]'))!.width).toBeCloseTo(112*1200/844,1);
  expect(await page.locator('#app').evaluate(el=>getComputedStyle(el).backgroundColor)).toBe('rgb(0, 0, 0)');
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await expect(page.locator('[data-item="name:Kit"]')).toBeVisible();
  await page.setViewportSize({width:844,height:390});
  await expect.poll(async()=>(await box(page,'.scene-art'))!.height).toBeCloseTo(390,1);
  expect((await box(page,'.chapter-panel'))!.width).toBeCloseTo(390*390/844,1);
  expect((await box(page,'[data-item="name:Tool"]'))!.width).toBeCloseTo(112*390/844,1);
});

test('landscape artwork always fits and places background-pixel centers on the image',async({page})=>{
  await open(page,true);
  for(const size of [{width:390,height:844},{width:1200,height:800}]){
    await page.setViewportSize(size);
    const width=Math.min(size.width,size.height*4/3),height=width*3/4;
    await expect.poll(async()=>(await box(page,'.chapter-panel'))!.height).toBeCloseTo(height,1);
    const scene=(await box(page,'.chapter-panel'))!,image=(await box(page,'.scene-art'))!;
    expect(scene.width).toBeCloseTo(width,1);expect(image.width/image.height).toBeCloseTo(4/3,3);
    expect(scene.y).toBeCloseTo((size.height-height)/2,1);
  }
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await page.getByRole('button',{name:'Continue story'}).click();
  const scene=(await box(page,'.chapter-panel'))!,station=(await box(page,'[data-hotspot="name:Station"]'))!;
  expect(station.x+station.width/2).toBeCloseTo(scene.x+scene.width*.75,1);
  expect(station.y+station.height/2).toBeCloseTo(scene.y+scene.height*.25,1);
  const kit=page.locator('[data-item="name:Kit"]');
  await kit.dragTo(page.locator('[data-item="name:Probe"]'));
  await expect(page.locator('[data-item="name:Final"]')).toBeVisible();
});

test('the desktop editor narrows its game pane into phone framing',async({page})=>{
  await page.setViewportSize({width:1600,height:1000});
  await open(page);
  await expect.poll(async()=>(await box(page,'.chapter-panel'))!.width).toBeCloseTo(390*1000/844,1);
  await page.locator('.debug-toggle').click();
  await expect(page.locator('.story-editor')).toBeVisible();
  await expect.poll(async()=>(await box(page,'#app'))!.width).toBe(390);
  expect((await box(page,'.chapter-panel'))!.width).toBeCloseTo(390,1);
  expect((await box(page,'.scene-art'))!.width).toBeGreaterThan(390);
  await page.locator('.debug-toggle').click();
  await expect.poll(async()=>(await box(page,'.chapter-panel'))!.width).toBeCloseTo(390*1000/844,1);
});

for (const finishScroll of [true, false]) test(
  `an older item crosses touching chapters when released ${finishScroll ? 'after scrolling' : 'during scrolling'}`, async ({page}) => {
  const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
  await page.setViewportSize({width:1600,height:1000});
  const source = story.replace('- Frame\n','- Frame\n  - icon: ![Frame](frame.svg)\n')
    .replace('- Kit [preserve] + Probe [preserve] -> Final',
      '- Kit [preserve] + Probe [preserve] -> Final\n- Frame [preserve] + Probe [preserve] -> Offcut');
  await open(page,false,source);
  await page.locator('[data-item="name:Frame"]').dragTo(page.locator('[data-item="name:Tool"]'));
  await page.getByRole('button',{name:'Continue story'}).click();
  const viewport=page.locator('.viewport');
  const probe = page.locator('[data-item="name:Probe"]');
  const board = page.locator('.chapter-panel');
  const activeBoard = (await board.last().boundingBox())!;
  await probe.dragTo(viewport,{targetPosition:{x:activeBoard.x + 500,y:400}});
  await viewport.evaluate(el=>{el.scrollLeft=0;});
  const tool = page.locator('[data-item="name:Tool"]');
  const olderBoard = (await board.first().boundingBox())!;
  await tool.dragTo(viewport,{targetPosition:{x:olderBoard.x + 5,y:450}});
  const tutorial = page.locator('.tutorial-overlay[data-tutorial="goals"]');
  await expect(tutorial.locator('.tutorial-label')).toBeVisible();
  const clockStart = new Date('2026-11-20T12:00:00Z');
  await page.clock.install({time:clockStart});
  await page.clock.pauseAt(new Date(clockStart.getTime() + 1000));
  const frame=page.locator('[data-item="name:Frame"]'),first=(await frame.boundingBox())!;
  await page.mouse.move(first.x+first.width/2,first.y+first.height/2);await page.mouse.down();
  const pointerX = olderBoard.x + olderBoard.width - 5;
  await page.mouse.move(pointerX,220);
  await page.clock.runFor(500);
  const scenes = page.locator('.scene-panel');
  const earlier = (await scenes.first().boundingBox())!, next = (await scenes.last().boundingBox())!;
  expect(earlier.x + earlier.width).toBeCloseTo(next.x,1);
  await expect(frame).toBeVisible();
  const held = (await frame.boundingBox())!;
  const name = (await frame.locator('.icon-name').boundingBox())!;
  // Pointer rounding at pickup is magnified on the wider destination board.
  expect(Math.abs(held.x + held.width/2 - pointerX)).toBeLessThan(2);
  expect(Math.abs(name.x + name.width/2 - (held.x + held.width/2))).toBeLessThan(1);
  expect(Math.abs(name.y + name.height - held.y)).toBeLessThan(1);

  const inset = await viewport.evaluate(el => parseFloat(getComputedStyle(el).getPropertyValue('--chapter-motion-inset')));
  const clip = await tutorial.evaluate(el => getComputedStyle(el).clipPath);
  const [topClip, rightClip = topClip, , leftClip = rightClip] = clip.match(/[\d.]+(?=px)/g)!.map(Number);
  expect(leftClip).toBeGreaterThanOrEqual(inset - .01);
  expect(rightClip).toBeGreaterThanOrEqual(inset - .01);
  const toolBox = (await tool.boundingBox())!, probeBox = (await probe.boundingBox())!;
  for (const [item, x, y] of [
    ['name:Tool',toolBox.x + 4,toolBox.y + toolBox.height/2],
    ['name:Probe',probeBox.x + probeBox.width/2,probeBox.y + probeBox.height/2],
  ] as const) {
    expect(item === 'name:Tool' ? x < inset : x > 1600 - inset).toBe(true);
    expect(x).toBeGreaterThan(0);
    expect(x).toBeLessThan(1600);
    expect(await page.evaluate(({x,y}) => document.elementFromPoint(x,y)?.closest('[data-item]')?.getAttribute('data-item'),{x,y})).not.toBe(item);
  }
  await page.mouse.move(probeBox.x + probeBox.width/2,probeBox.y + probeBox.height/2);
  await expect(probe).not.toHaveClass(/will-create/);
  await page.mouse.move(pointerX,220);
  if (finishScroll) {
    await page.clock.runFor(2600);
    await expect.poll(() => viewport.evaluate(el => el.scrollLeft)).toBe(1600);
    await page.mouse.move(400,220);
    await expect(frame).toBeVisible();
  } else {
    expect(await viewport.evaluate(el => el.scrollLeft)).toBeLessThan(800);
    expect(next.x).toBeLessThan(pointerX);
  }
  expect((await frame.boundingBox())!.width).toBeCloseTo(Math.min(2 * 160 / 4, first.width * activeBoard.width / olderBoard.width),1);
  await page.mouse.up();
  await expect.poll(() => viewport.evaluate(el => el.scrollLeft)).toBe(1600);
  await expect(page.locator('.chapter-panel[data-chapter="1"] [data-item="name:Frame"]')).toBeVisible();
  expect((await frame.boundingBox())!.width).toBeCloseTo(Math.min(2 * 160 / 4, first.width * activeBoard.width / olderBoard.width),1);
  expect(errors).toEqual([]);
});

test('the iPad Creation opening caps the movable elements and keeps a row clear of the water and goals', async ({page}) => {
  await page.setViewportSize({width:1024,height:1366});
  await page.goto('/index.html?story=stories/creation/creation.md');
  await page.getByRole('button',{name:'Start',exact:true}).click();
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  const items = page.locator('.chapter-panel [data-item]');
  await expect(items).toHaveCount(3);
  const row = await items.evaluateAll(elements => elements.map(el => el.getBoundingClientRect().toJSON()));
  const water = (await page.locator('[data-hotspot="name:Waters of the deep"]').boundingBox())!;
  const goals = (await page.locator('.hud-stack').boundingBox())!;
  for (const item of row) {
    expect(item.width).toBeCloseTo(128,1);
    expect(item.height).toBeCloseTo(128,1);
    expect(item.y).toBeCloseTo(row[0].y,1);
    expect(item.bottom).toBeLessThanOrEqual(water.y + 1);
    expect(item.bottom).toBeLessThan(goals.y);
  }
  await page.setViewportSize({width:390,height:844});
  await expect.poll(async () => (await items.first().boundingBox())!.width).toBeCloseTo(64,1);
});
