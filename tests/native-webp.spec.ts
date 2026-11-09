import {test, expect, type Page, type Locator} from '@playwright/test';

// Lossless 195×422 WebP: red for 1s, green for 1s, loop count 1.
const once = Buffer.from('UklGRpwAAABXRUJQVlA4WAoAAAACAAAAwgAApQEAQU5JTQYAAAD/////AQBBTk1GNAAAAAAAAAAAAMIAAKUBAOgDAAJWUDhMGwAAAC/CQGkAB1CPctej/wEBSdL//2RE/zP+83+bAABBTk1GNAAAAAAAAAAAAMIAAKUBAOgDAABWUDhMGwAAAC/CQGkAB1DaepSn/wEBSdL//2RE/zP+83+bAAA=', 'base64');

async function pixel(page: Page, target: Locator) {
  const box = (await target.boundingBox())!;
  const screenshot = await page.screenshot({clip:{x:Math.floor(box.x+box.width/2),y:Math.floor(box.y+box.height/2),width:1,height:1}});
  return page.evaluate(async base64 => {
    const image = await createImageBitmap(new Blob([Uint8Array.from(atob(base64), c=>c.charCodeAt(0))],{type:'image/png'}));
    const canvas=document.createElement('canvas');canvas.width=canvas.height=1;
    const context=canvas.getContext('2d')!;context.drawImage(image,0,0);
    return [...context.getImageData(0,0,1,1).data].slice(0,3);
  },screenshot.toString('base64'));
}

for (const kind of ['icon','background'] as const) test(`ordinary ${kind} images play WebP frames and retain the final frame through redraw`, async ({page}) => {
  // This only suppresses the application's arrival effects; image playback is native.
  await page.emulateMedia({reducedMotion:'reduce'});
  const manuscript=`# Native images
## Work
background: ![room](room.svg)
**Goals**
- Finish -- C
**Items**
- A
- B
- C
${kind==='icon'?'  - icon: ![moving object](once.webp)':''}
**Combinations**
- A [consume] + B [transform] -> C
## Ending
background: ![moving scene](${kind==='background'?'once.webp':'room.svg'})`;
  await page.route('**/native-webp/story.md',r=>r.fulfill({contentType:'text/markdown',body:manuscript}));
  await page.route('**/native-webp/room.svg',r=>r.fulfill({contentType:'image/svg+xml',body:'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844"><rect width="100%" height="100%" fill="white"/></svg>'}));
  await page.route('**/native-webp/once.webp',r=>r.fulfill({contentType:'image/webp',body:once}));
  await page.goto('/make-something.html?story=native-webp/story.md');
  await page.getByRole('button',{name:'Start',exact:true}).click();
  await page.waitForTimeout(2100); // Speculative decoding must not exhaust the displayed animation.
  await page.locator('[data-item="name:A"]').dragTo(page.locator('[data-item="name:B"]'));
  if(kind==='background') await page.getByRole('button',{name:'Continue story'}).click();
  const target=page.locator(kind==='icon'?'[data-item="name:C"] .item-icon':'.scene-panel[data-chapter="1"] .scene-art');
  await expect(target).toHaveAttribute('src',/once.webp$/);
  if(kind==='icon') {
    const box=(await target.boundingBox())!;
    expect(box.width).toBeCloseTo(195/4,1);expect(box.height).toBeCloseTo(422/4,1);
  }
  expect(await pixel(page,target)).toEqual([220,30,30]);
  await expect.poll(()=>pixel(page,target)).toEqual([30,180,60]);
  await page.waitForTimeout(1200);
  const image=await target.elementHandle();
  await page.setViewportSize({width:400,height:844});
  expect(await image!.evaluate(el=>el.isConnected)).toBe(true);
  expect(await pixel(page,target)).toEqual([30,180,60]);
});
