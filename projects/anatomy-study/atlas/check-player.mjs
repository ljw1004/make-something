/** Consecutive ordinary browser drags; optional chapter checkpoints for focused repairs.
 * Run with Node22+ and local Vite server. All captures/logs are disposable runs/ output.
 */
import {chromium} from '@playwright/test';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {parseStory} from '../../../src/story/parser.ts';
import {checkpoint} from '../../../src/debug/checkpoint.ts';
const file='projects/anatomy-study/anatomy.md',story=parseStory(readFileSync(file,'utf8'));
const viewport={width:Number(process.env.WIDTH||390),height:Number(process.env.HEIGHT||844)};
const out=`runs/anatomy-atlas/captures-${viewport.width}x${viewport.height}`;mkdirSync(out,{recursive:true});
const selected=process.argv.slice(2).map(Number),continuous=!selected.length;
const range=continuous?Array.from({length:28},(_,i)=>i+1):selected;
const browser=await chromium.launch(),context=await browser.newContext({viewport,deviceScaleFactor:2,reducedMotion:'reduce'}),page=await context.newPage();
const errors=[],results=[];page.on('pageerror',e=>errors.push(e.message));
async function settle(){await page.waitForTimeout(160);await page.evaluate(async()=>{await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});}
async function dismiss(){for(let i=0;i<8;i++){await settle();const b=page.getByRole('button',{name:/^(Begin|Continue|Close)$/,exact:true});if(!await b.count())break;await b.first().click();}}
async function saved(){return page.evaluate(()=>Object.values(localStorage).map(v=>{try{return JSON.parse(v)}catch{return null}}).find(v=>v?.state?.actions)?.state);}
async function visiblePoint(locator){return locator.evaluate(el=>{const b=el.getBoundingClientRect();for(const [u,v] of [[.5,.5],[.85,.5],[.15,.5],[.5,.15],[.5,.85],[.85,.15],[.85,.85],[.15,.15],[.15,.85]]){const x=b.x+b.width*u,y=b.y+b.height*v,h=document.elementFromPoint(x,y);if(h&&(h===el||el.contains(h)))return{x,y};}return null;});}
for(const chapter of range){
 try{
  if(!continuous||chapter===1){await page.goto('http://127.0.0.1:5173/make-something.html?story='+file);await settle();const start=page.getByRole('button',{name:'Start',exact:true});if(await start.count())await start.click();await dismiss();}
  if(!continuous&&chapter!==1){await page.getByRole('button',{name:'Toggle debug panel'}).click();if(viewport.width>=900){await page.getByRole('button',{name:'Chapter',exact:true}).click();await page.getByRole('option',{name:`${chapter}. ${story.chapters[chapter-1].name}`,exact:true}).click();await page.getByRole('button',{name:'Close debug panel',exact:true}).click();}else await page.getByRole('button',{name:`${chapter}. ${story.chapters[chapter-1].name}`,exact:true}).click();await dismiss();}
  const panel=page.locator('.chapter-panel').last();if(Number(await panel.getAttribute('data-chapter'))!==chapter-1)throw Error('Wrong chapter after Continue');
  const start=checkpoint(story,chapter-1),end=checkpoint(story,chapter,start),actions=end.actions.slice(start.actions.length).filter(a=>a.type==='combine'||a.type==='move');
  await page.mouse.move(viewport.width-1,viewport.height-1);await settle();await page.waitForTimeout(350);await page.screenshot({path:`${out}/chapter-${chapter}-entry.png`});
  const missing=await panel.locator('[data-item],[data-hotspot]').evaluateAll(els=>els.filter(e=>!e.querySelector('img')).map(e=>e.dataset.item??e.dataset.hotspot));if(missing.length)throw Error('Missing icons: '+missing.join(', '));
  let step=0;
  for(const a of actions){
   const source=a.type==='combine'?a.a:a.item,target=a.type==='combine'?(a.b||a.hotspot):a.hotspot;if(!target)throw Error('No target');
   let from=panel.locator(`[data-item=${JSON.stringify(source)}]`),to=panel.locator(`[data-item=${JSON.stringify(target)}],[data-hotspot=${JSON.stringify(target)}]`);
   let ab=await from.boundingBox(),bb=await to.boundingBox();if(!ab||!bb)throw Error(`Missing ${source} -> ${target}`);
   if(a.type==='combine'&&a.b&&!a.hotspot&&await to.getAttribute('data-item')&&!await to.getAttribute('data-hotspot')&&ab.width*ab.height>bb.width*bb.height){[from,to]=[to,from];[ab,bb]=[bb,ab];}
   const before=await saved();let pick=await visiblePoint(from);if(!pick)throw Error(`Covered source ${source}`);
   await page.mouse.move(pick.x,pick.y);await page.mouse.down();await page.mouse.move(bb.x+bb.width/2,bb.y+bb.height/2,{steps:12});await page.mouse.up();await dismiss();
   const after=await saved();if(a.type==='combine'&&after.actions.filter(x=>x.type==='combine').length<=before.actions.filter(x=>x.type==='combine').length)throw Error(`Drag not combined ${source} -> ${target}`);
   if(++step===1)await page.screenshot({path:`${out}/chapter-${chapter}-partial.png`});
  }
  await page.getByRole('button',{name:'Continue story',exact:true}).waitFor({timeout:5000});
  await page.mouse.move(viewport.width-1,viewport.height-1);await page.waitForTimeout(1400);await page.screenshot({path:`${out}/chapter-${chapter}.png`});
  const broken=await page.evaluate(()=>[...document.images].filter(i=>i.getAttribute('src')&&(!i.complete||!i.naturalWidth)).map(i=>i.src));
  await page.reload();await settle();await page.getByRole('button',{name:'Continue story',exact:true}).waitFor({timeout:10000});
  results.push({chapter,actions:actions.length,complete:true,reloaded:true,broken,errors:[...errors]});
  if(continuous||chapter===28){await page.getByRole('button',{name:'Continue story',exact:true}).click();await page.getByRole('button',{name:'Begin',exact:true}).waitFor({timeout:30000});await dismiss();if(chapter===28&&Number(await page.locator('.chapter-panel').last().getAttribute('data-chapter'))!==28)throw Error('Did not reach epilogue');}
 }catch(e){results.push({chapter,error:String(e),errors:[...errors]});await page.screenshot({path:`${out}/chapter-${chapter}-error.png`}).catch(()=>{});}
 console.log(JSON.stringify(results.at(-1)));writeFileSync(`${out}/outcome.json`,JSON.stringify(results,null,2));
 if(continuous&&results.at(-1).error)break;
}
if(continuous&&results.length===28&&!results.at(-1).error){const c=Number(await page.locator('.chapter-panel').last().getAttribute('data-chapter'));if(c!==28)throw Error('Did not reach epilogue');}
await browser.close();if(results.some(r=>r.error||r.broken?.length||r.errors?.length))process.exitCode=1;
