// Run from the repository root. Selected imagegen masters are untreated.
// Export to the existing scene coordinate frame and apply the brief's cream once.
import { readFileSync, writeFileSync } from 'node:fs';
import { chromium } from '@playwright/test';

const names = ['art-studio', 'binding-studio', 'weather-beach', 'cooking-room', 'waterworks', 'settlement-record'];
const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  for (const name of names) {
    const input = readFileSync(`archive/2026.11.06 settlement study/artwork/backgrounds/${name}.master.png`);
    const result = await page.evaluate(async source => {
      const image = new Image();
      image.src = source;
      await image.decode();
      const canvas = document.createElement('canvas');
      canvas.width = 780;
      canvas.height = 1688;
      const context = canvas.getContext('2d');
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
      context.fillStyle = 'rgba(255,250,240,0.22)';
      context.fillRect(0, 0, canvas.width, canvas.height);
      return { width: image.width, height: image.height, output: canvas.toDataURL('image/webp', 0.95).split(',')[1] };
    }, `data:image/png;base64,${input.toString('base64')}`);
    writeFileSync(`stories/settlement/assets/backgrounds/${name}.webp`, Buffer.from(result.output, 'base64'));
    console.log(`${name}: ${result.width}x${result.height} master -> 780x1688, 22% #fffaf0`);
  }
} finally {
  await browser.close();
}
