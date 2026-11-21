/** Verify the retained gallery's complete inventories, recipe strips and local links. */
import {chromium} from '@playwright/test';
const base='http://127.0.0.1:5173/projects/anatomy-study/atlas/review.html';
const browser=await chromium.launch(),page=await browser.newPage();
const errors=[];page.on('pageerror',e=>errors.push(e.message));
try {
 await page.goto(base);
 await page.locator('details').evaluateAll(nodes=>nodes.forEach(n=>n.open=true));
 await page.locator('img').evaluateAll(async nodes=>{
  await Promise.all(nodes.map(async img=>{img.loading='eager';await img.decode().catch(()=>{});}));
 });
 const broken=await page.locator('img').evaluateAll(nodes=>nodes.filter(n=>!n.naturalWidth).map(n=>n.src));
 const sections=await page.locator('section').count(),recipes=await page.locator('figure').count();
 const links=await page.locator('a[href]').evaluateAll(nodes=>[...new Set(nodes.map(n=>n.href).filter(h=>!h.includes('#')))]);
 const failed=[];
 for (const url of links){const response=await page.request.get(url);if(!response.ok())failed.push({url,status:response.status()});}
 const result={sections,recipes,links:links.length,broken,failed,errors};console.log(JSON.stringify(result));
 if(sections!==28||recipes!==132||broken.length||failed.length||errors.length)process.exitCode=1;
} finally {await browser.close();}
