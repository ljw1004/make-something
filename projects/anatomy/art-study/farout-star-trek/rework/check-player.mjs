/** Actual browser route drags, artwork decoding and completed-state reload.
 * Node22+; run from repo root with dev server active. Scratch only under runs/.
 */
import{chromium}from'@playwright/test';
import{readFileSync,mkdirSync,writeFileSync}from'node:fs';
import{parseStory}from'../../../../../src/story/parser.ts';
import{checkpoint}from'../../../../../src/debug/checkpoint.ts';
const file='projects/anatomy/art-study/farout-star-trek/anatomy.md';
const story=parseStory(readFileSync(file,'utf8'));
const viewport={width:Number(process.env.WIDTH||390),height:Number(process.env.HEIGHT||844)};
const folder=viewport.width===390&&viewport.height===844?'captures':`captures-${viewport.width}x${viewport.height}`;
const out='runs/anatomy-star-rework/'+folder;mkdirSync(out,{recursive:true});
const chapters=process.argv.slice(2).map(Number);const range=chapters.length?chapters:Array.from({length:28},(_,i)=>i+1);
const browser=await chromium.launch();const results=[];
async function settle(page){await page.waitForTimeout(160);await page.evaluate(async()=>{await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});}
async function dismiss(page){for(let i=0;i<8;i++){await settle(page);const btn=page.getByRole('button',{name:/^(Begin|Continue|Close)$/,exact:true});if(!await btn.count())break;await btn.first().click();}}
for(const chapter of range){
 const context=await browser.newContext({viewport,deviceScaleFactor:2,reducedMotion:'reduce'});const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 try{
  const start=checkpoint(story,chapter-1),end=checkpoint(story,chapter,start);const actions=end.actions.slice(start.actions.length).filter(a=>a.type==='combine'||a.type==='move');
  await page.goto('http://127.0.0.1:5173/make-something.html?story='+file);
  await page.getByRole('button',{name:'Start',exact:true}).click();await dismiss(page);
  if(chapter!==1){await page.getByRole('button',{name:'Toggle debug panel'}).click();if(viewport.width>=900){await page.getByRole('button',{name:'Chapter',exact:true}).click();await page.getByRole('option',{name:`${chapter}. ${story.chapters[chapter-1].name}`,exact:true}).click();await page.getByRole('button',{name:'Close debug panel',exact:true}).click();}else{await page.getByRole('button',{name:`${chapter}. ${story.chapters[chapter-1].name}`,exact:true}).click();}await dismiss(page);}
  await page.screenshot({path:`${out}/chapter-${chapter}-entry.png`});
  const panel=page.locator('.chapter-panel').last();let step=0;
  for(const a of actions){
   const source=a.type==='combine'?a.a:a.item,target=a.type==='combine'?(a.b||a.hotspot):a.hotspot;
   if(!target)continue;
   let from=panel.locator(`[data-item=${JSON.stringify(source)}]`),to=panel.locator(`[data-item=${JSON.stringify(target)}],[data-hotspot=${JSON.stringify(target)}]`);
   let ab=await from.boundingBox(),bb=await to.boundingBox();if(!ab||!bb)throw Error(`Missing ${source} -> ${target}`);
   // For commutative movable constructions, place the smaller part onto the
   // larger receiver. This avoids dropping a growing assembly over unused supplies.
   if(a.type==='combine'&&a.b&&!a.hotspot&&await to.getAttribute('data-item')&&ab.width*ab.height>bb.width*bb.height){[from,to]=[to,from];[ab,bb]=[bb,ab];}
   // Pick a visible part of the source when a growing neighbour overlaps it.
   const pick=await from.evaluate(el=>{const b=el.getBoundingClientRect();for(const [u,v] of [[.5,.5],[.85,.5],[.15,.5],[.5,.15],[.5,.85],[.85,.15],[.85,.85],[.15,.15],[.15,.85]]){const x=b.x+b.width*u,y=b.y+b.height*v,h=document.elementFromPoint(x,y);if(h&&(h===el||el.contains(h)))return{x,y};}return null;});
   if(!pick)throw Error(`Covered source ${source}`);
   const ty=bb.y+bb.height/2;
   await page.mouse.move(pick.x,pick.y);await page.mouse.down();await page.mouse.move(bb.x+bb.width/2,ty,{steps:12});await page.mouse.up();await dismiss(page);
   if(++step===1)await page.screenshot({path:`${out}/chapter-${chapter}-partial.png`});
  }
  await page.getByRole('button',{name:'Continue story',exact:true}).waitFor({timeout:5000});
  await page.mouse.move(viewport.width-1,viewport.height-1);await page.waitForTimeout(1700);await page.screenshot({path:`${out}/chapter-${chapter}.png`});
  const broken=await page.evaluate(()=>[...document.images].filter(i=>i.getAttribute('src')&&(!i.complete||!i.naturalWidth)).map(i=>i.src));
  await page.reload();await settle(page);await page.getByRole('button',{name:'Continue story',exact:true}).waitFor({timeout:10000});
  results.push({chapter,actions:actions.length,complete:true,reloaded:true,broken,errors});
 }catch(e){results.push({chapter,error:String(e),errors});await page.screenshot({path:`${out}/chapter-${chapter}-error.png`}).catch(()=>{});}
 console.log(JSON.stringify(results.at(-1)));writeFileSync(`${out}/chapter-${chapter}-result.json`,JSON.stringify(results.at(-1),null,2));await context.close();
}
await browser.close();writeFileSync(`${out}/outcome.json`,JSON.stringify(results,null,2));if(results.some(r=>r.error||r.broken?.length||r.errors?.length))process.exitCode=1;
