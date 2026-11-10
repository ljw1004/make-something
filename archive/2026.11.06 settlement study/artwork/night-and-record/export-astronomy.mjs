import { readFileSync, writeFileSync } from 'node:fs';
import { chromium } from '@playwright/test';

const master = 'archive/2026.11.06 settlement study/artwork/night-and-record/astronomy-night-v2.master.png';
const runtime = 'stories/settlement/assets/backgrounds/astronomy-night-v2.webp';
const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  const result = await page.evaluate(async source => {
    const image = new Image();
    image.src = source;
    await image.decode();
    const canvas = document.createElement('canvas');
    canvas.width = 780;
    canvas.height = 1688;
    const context = canvas.getContext('2d');
    context.drawImage(image, 0, 0, 780, 1688);
    context.fillStyle = 'rgba(255,250,240,0.22)';
    context.fillRect(0, 0, 780, 1688);
    return { width: image.width, height: image.height, output: canvas.toDataURL('image/webp', 0.95).split(',')[1] };
  }, 'data:image/png;base64,' + readFileSync(master).toString('base64'));
  writeFileSync(runtime, Buffer.from(result.output, 'base64'));
  console.log(JSON.stringify({ master, source: [result.width, result.height], runtime, export: [780, 1688], treatment: '22% #fffaf0 once', quality: 0.95 }));
} finally {
  await browser.close();
}
