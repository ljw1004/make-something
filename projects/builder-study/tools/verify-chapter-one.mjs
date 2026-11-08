#!/usr/bin/env node
// Exercise the actual movable build at several viewport sizes, then continue.
// Usage: node THIS_FILE STORY_FILE SCRATCH_OUTPUT [BASE_URL]
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {chromium,expect} from '@playwright/test';
let root=path.dirname(fileURLToPath(import.meta.url));
while(!fs.existsSync(path.join(root,'src/story/parser.ts'))) {const parent=path.dirname(root);if(parent===root)throw new Error('Repository root missing');root=parent;}
const mod=relative=>import(pathToFileURL(path.join(root,relative)).href);
const [{parseStory},{checkpoint},{newGame,act,recipeFor}]=await Promise.all([mod('src/story/parser.ts'),mod('src/debug/checkpoint.ts'),mod('src/engine/game.ts')]);
const [file,out,base='http://127.0.0.1:5173']=process.argv.slice(2);
if(!file||!out)throw new Error('Expected STORY_FILE SCRATCH_OUTPUT [BASE_URL]');
fs.mkdirSync(out,{recursive:true});
const source=fs.readFileSync(file,'utf8'),story=parseStory(source,{id:file,file});
let state=newGame(story);const route=[];
expect(state.pending).toHaveLength(0);
for(const action of checkpoint(story,1).actions){const recipe=action.type==='combine'?recipeFor(story,state,action):null;state=act(story,state,action);if(recipe)route.push({action,result:recipe.result.id});}
expect(route).toHaveLength(9);
const browser=await chromium.launch(),outcomes=[];
try {
 for(const viewport of [{width:390,height:844},{width:390,height:664},{width:320,height:568},{width:1280,height:900}]){
  const label=`${viewport.width}x${viewport.height}`,dir=path.join(out,label);fs.mkdirSync(dir,{recursive:true});
  const page=await browser.newPage({viewport}),errors=[],failed=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)failed.push([r.status(),r.url()]);});
  await page.emulateMedia({reducedMotion:'reduce'});
  const saved=()=>page.evaluate(()=>{const entry=Object.entries(localStorage).find(([k])=>k.startsWith('combination-progress-v2:'));return entry?JSON.parse(entry[1]).state:null;});
  const item=id=>page.locator(`[data-item="${id}"],[data-hotspot="${id}"]`).last();
  const measured=[];
  async function capture(step){
   await expect(page.getByRole('dialog')).toHaveCount(0);
   const bad=await page.locator('img').evaluateAll(async imgs=>{await Promise.all(imgs.map(i=>i.decode().catch(()=>{})));return imgs.filter(i=>!i.naturalWidth).map(i=>i.src);});expect(bad).toEqual([]);
   measured.push({step,items:await page.locator('.chapter-panel[data-chapter="0"] [data-item],.chapter-panel[data-chapter="0"] [data-hotspot]').evaluateAll(nodes=>nodes.map(el=>{const r=el.getBoundingClientRect();return{id:el.getAttribute('data-item')??el.getAttribute('data-hotspot'),fixed:el.hasAttribute('data-hotspot'),x:r.x,y:r.y,width:r.width,height:r.height};}))});
   await page.screenshot({path:path.join(dir,`${step}.png`)});
  }
  try {
   await page.goto(`${base}/make-something.html?story=${file}`);await page.getByRole('button',{name:'Start',exact:true}).click();
   await expect(item('id:pw-paper')).toBeVisible();await capture('00-start');
   expect(await page.locator('[data-hotspot="id:pw-paper"]').count()).toBe(0);
   // Repositioning is independent of recipe execution, including a large sheet.
   const paper=item('id:pw-paper'),before=await paper.boundingBox();
   await page.mouse.move(before.x+before.width/2,before.y+before.height/2);await page.mouse.down();await page.mouse.move(before.x+before.width/2-12,before.y+before.height/2-16,{steps:6});await page.mouse.up();
   expect(await paper.boundingBox()).not.toEqual(before);expect((await saved()).actions.filter(a=>a.type==='combine')).toHaveLength(0);
   for(let i=0;i<route.length;i++){
    const {action,result}=route[i];
    const target=action.b??action.hotspot;
    // Both assembly directions must work: move the workpiece onto its hub.
    const reverse=viewport.width===1280&&result==='id:pw-folded-rotor';
    const a=reverse?item(action.b):item(action.a),b=reverse?item(action.a):item(target);
    // A large dragged item naturally covers its destination. Real pointer
    // events avoid Playwright's target-actionability check during that drag.
    const to=await b.boundingBox();
    const pickup=await a.evaluate(el=>{
      const r=el.getBoundingClientRect();
      for(const [u,v] of [[.5,.5],[.5,.1],[.5,.25],[.5,.75],[.5,.9],[.1,.1],[.9,.1],[.1,.9],[.9,.9]]){
        const x=r.x+r.width*u,y=r.y+r.height*v;
        if(el.contains(document.elementFromPoint(x,y)))return{x,y};
      }
      return null;
    });
    expect(pickup,'Needed piece has an exposed pickup point').not.toBeNull();
    await page.mouse.move(pickup.x,pickup.y);await page.mouse.down();
    await page.mouse.move(to.x+to.width/2,to.y+to.height/2,{steps:10});await page.mouse.up();
    await expect(item(result)).toBeVisible();
    await expect.poll(async()=>(await saved())?.actions.filter(a=>a.type==='combine').length).toBe(i+1);
    expect((await saved()).pending).toEqual([]);
    expect(await page.locator(`[data-hotspot="${result}"]`).count()).toBe(0);
    await capture(`${String(i+1).padStart(2,'0')}-${result.slice(3)}`);
   }
   const final=await saved();await page.reload();await expect(item('id:pinwheel')).toBeVisible();expect((await saved()).actions).toEqual(final.actions);
   await page.getByRole('button',{name:'Continue story',exact:true}).click();await page.getByRole('button',{name:'Begin',exact:true}).click();
   await expect(item('id:pinwheel')).toBeVisible();expect((await saved()).chapter).toBe(1);
   await page.screenshot({path:path.join(dir,'07-next-chapter.png')});
   expect(errors).toEqual([]);expect(failed).toEqual([]);outcomes.push({viewport,passed:true,measured});
  } catch(e) {await page.screenshot({path:path.join(dir,'failure.png')});fs.writeFileSync(path.join(dir,'failure.json'),JSON.stringify({error:String(e),state:await saved(),measured,errors,failed},null,2));throw e;}
  finally {await page.close();}
 }
 fs.writeFileSync(path.join(out,'outcome.json'),JSON.stringify({sourceSha256:createHash('sha256').update(source).digest('hex'),outcomes},null,2));
 console.log(JSON.stringify({viewports:outcomes.map(o=>o.viewport),actions:route.length,popups:0,reload:true,nextChapter:true}));
} finally {await browser.close();}
