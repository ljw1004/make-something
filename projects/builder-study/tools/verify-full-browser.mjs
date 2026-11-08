#!/usr/bin/env node
// Real pointer replay, image decoding and inspection captures for every build.
// Usage: node THIS_FILE STORY_FILE SCRATCH_DIR [WIDTHxHEIGHT] [BASE_URL]
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {chromium,expect} from '@playwright/test';
import {parseStory} from '../../../src/story/parser.ts';
import {checkpoint} from '../../../src/debug/checkpoint.ts';
import {act,newGame,recipeFor} from '../../../src/engine/game.ts';
import {browserItemText} from '../../../src/story/text-only.ts';
const [file,out,shape='390x844',base='http://127.0.0.1:5173']=process.argv.slice(2);
if(!out)throw new Error('Expected STORY_FILE SCRATCH_DIR [WIDTHxHEIGHT] [BASE_URL]');
const [width,height]=shape.split('x').map(Number),viewport={width,height};
const source=fs.readFileSync(file,'utf8'),story=parseStory(source,{id:file,file});
const route=checkpoint(story,story.chapters.length).actions;
fs.mkdirSync(out,{recursive:true});
const browser=await chromium.launch(),page=await browser.newPage({viewport,hasTouch:width<640});
const errors=[],failed=[],measurements=[],rearrangements=[];let count=0,current=newGame(story);
page.on('pageerror',e=>errors.push(e.message));
page.on('response',r=>{if(r.status()>=400)failed.push([r.status(),r.url()]);});
const saved=()=>page.evaluate(()=>{const pair=Object.entries(localStorage).find(([key])=>key.startsWith('combination-progress-v2:'));return pair?JSON.parse(pair[1]).state:null;});
const panel=()=>page.locator('.chapter-panel').last();
const item=id=>panel().locator(`[data-item="${id}"],[data-hotspot="${id}"]`).last();
const cdp=width<640?await page.context().newCDPSession(page):null;
async function drag(from,to){
 if(cdp){
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[from]});
  for(let i=1;i<=10;i++)await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:from.x+(to.x-from.x)*i/10,y:from.y+(to.y-from.y)*i/10}]});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
 }else{await page.mouse.move(from.x,from.y);await page.mouse.down();await page.mouse.move(to.x,to.y,{steps:10});await page.mouse.up();}
}
async function exposed(locator){return locator.evaluate(el=>{
 const r=el.getBoundingClientRect();
 for(const [u,v] of [[.5,.5],[.5,.15],[.5,.3],[.5,.7],[.5,.85],[.15,.15],[.85,.15],[.15,.85],[.85,.85],[.15,.5],[.85,.5]]){
  const x=r.x+r.width*u,y=r.y+r.height*v;
  if(x>=0&&x<innerWidth&&y>=0&&y<innerHeight&&el.contains(document.elementFromPoint(x,y)))return{x,y};
 }
 return null;
});}
async function uncover(locator){
 // Recoverable tabletop overlap is allowed. Move the foreground piece through
 // real input, without combining it, and record how often this was necessary.
 for(let attempt=0;attempt<4;attempt++){
  const point=await exposed(locator);if(point)return point;
  const plan=await locator.evaluate(el=>{
   const r=el.getBoundingClientRect(),panel=el.closest('.chapter-panel');
   const top=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.closest('[data-item]');
   if(!top||top===el||!panel.contains(top))return null;
   const t=top.getBoundingClientRect(),all=[...panel.querySelectorAll('[data-item],[data-hotspot],.chapter-reference')];
   const overlap=(a,b)=>Math.max(0,Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x))*Math.max(0,Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y));
   const choices=[];
   for(let y=180;y<innerHeight-100;y+=24)for(let x=12;x<innerWidth-12;x+=24){
    const landing={x:x-t.width/2,y:y-t.height/2,width:t.width,height:t.height};
    if(landing.x<0||landing.x+t.width>innerWidth||landing.y<12||landing.y+t.height>innerHeight-100||overlap(landing,r)>r.width*r.height*.6)continue;
    if(all.some(n=>n!==top&&(()=>{const b=n.getBoundingClientRect();return x>=b.left&&x<=b.right&&y>=b.top&&y<=b.bottom;})()))continue;
    choices.push({x,y,score:all.filter(n=>n!==top).reduce((sum,n)=>sum+overlap(landing,n.getBoundingClientRect()),0)});
   }
   choices.sort((a,b)=>a.score-b.score);
   return choices[0]?{id:top.dataset.item,destination:choices[0]}:null;
  });
  if(!plan)return null;
  const cover=item(plan.id),pickup=await exposed(cover);if(!pickup)return null;
  const rect=await cover.boundingBox();
  // Pick up at the exposed point, then centre the piece at the chosen location.
  const drop={x:plan.destination.x+pickup.x-(rect.x+rect.width/2),y:plan.destination.y+pickup.y-(rect.y+rect.height/2)};
  const before=(await saved()).actions.filter(a=>a.type==='combine').length;
  await drag(pickup,drop);
  expect((await saved()).actions.filter(a=>a.type==='combine').length).toBe(before);
  rearrangements.push({chapter:current.chapter+1,beforeCombination:count+1,item:plan.id});
 }
 return exposed(locator);
}
async function capture(label){
 await expect(page.getByRole('dialog')).toHaveCount(0);
 await expect(panel().locator('.chapter-title')).toHaveText(story.chapters[current.chapter].name,{timeout:30_000});
 const reference=story.chapters[current.chapter].reference;
 if(reference)await expect(panel().locator('.reference-caption')).toHaveText(reference.alt);
 const bad=await page.locator('img').evaluateAll(async imgs=>{await Promise.all(imgs.map(i=>i.decode().catch(()=>{})));return imgs.filter(i=>!i.naturalWidth).map(i=>i.src);});expect(bad).toEqual([]);
 const sizes=await panel().locator('[data-item],[data-hotspot]').evaluateAll(nodes=>nodes.map(el=>{
  const r=el.getBoundingClientRect(),style=getComputedStyle(el),pseudo=getComputedStyle(el,'::before'),scale=r.width/parseFloat(style.width);
  return{id:el.dataset.item??el.dataset.hotspot,fixed:el.hasAttribute('data-hotspot'),x:r.x,y:r.y,width:r.width,height:r.height,hitWidth:el.hasAttribute('data-hotspot')?r.width:parseFloat(pseudo.width)*scale,hitHeight:el.hasAttribute('data-hotspot')?r.height:parseFloat(pseudo.height)*scale};
 }));
 for(const size of sizes){expect(size.hitWidth,size.id+' hit width').toBeGreaterThanOrEqual(43.5);expect(size.hitHeight,size.id+' hit height').toBeGreaterThanOrEqual(43.5);}
 measurements.push({label,chapter:current.chapter+1,sizes});
 await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
 await page.screenshot({path:path.join(out,label+'.png'),animations:'disabled'});
}
try{
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.goto(`${base}/make-something.html?story=${file}`);
 await page.getByRole('button',{name:'Start',exact:true}).click();
 await capture('000-start');
 // The reference has its own pale panel and opens independently of construction.
 const reference=panel().locator('.chapter-reference');
 expect(await reference.evaluate(el=>getComputedStyle(el).backgroundColor)).toBe('rgb(241, 245, 243)');
 expect(await reference.evaluate(el=>parseFloat(el.style.top))).toBe(36);
 await expect(panel().locator('.chapter-title')).toHaveText(story.chapters[0].name);
 await expect(reference.locator('.reference-caption')).toHaveText(story.chapters[0].reference.alt);
 await reference.click();await expect(page.locator('.reference-reading img')).toBeVisible();
 await page.getByRole('button',{name:'Close',exact:true}).click();
 for(const action of route){
  const recipe=action.type==='combine'?recipeFor(story,current,action):null;
  let hiddenDismiss=false;
  if(action.type==='dismiss'){
   const notice=current.pending[0];
   hiddenDismiss=notice.kind==='wonder'&&!browserItemText(notice.markdown);
   if(!hiddenDismiss)await page.getByRole('dialog').getByRole('button',{name:/^(Begin|Continue)$/}).click();
  }else if(action.type==='advance'){
   const before=await saved();await page.reload();expect((await saved()).actions).toEqual(before.actions);
   await page.getByRole('button',{name:'Continue story',exact:true}).click();
  }else if(action.type==='combine'){
   const sourceItem=item(action.a),target=item(action.b??action.hotspot);
   const pickup=await uncover(sourceItem);expect(pickup,`Exposed pickup for ${action.a}, chapter ${current.chapter+1}`).not.toBeNull();
   const rect=await target.boundingBox();expect(rect).not.toBeNull();
   // First Fold lands in the enlarged margin, outside the original icon bounds.
   const edge=recipe.result.id==='id:pw-one-blade';
   const point={x:edge?rect.x+3:rect.x+rect.width/2,y:rect.y+rect.height/2};
   await drag(pickup,point);count++;
   await expect(item(recipe.result.id),`Result after action ${count}`).toBeVisible();
   await expect.poll(async()=>(await saved()).actions.filter(a=>a.type==='combine').length).toBe(count);
   expect(await panel().locator(`[data-hotspot="${recipe.result.id}"]`).count()).toBe(0);
  }else throw new Error('Unexpected checkpoint action '+action.type);
  current=act(story,current,action);
  const visibleReading=current.pending.some(notice=>notice.kind==='chapter'||browserItemText(notice.markdown));
  if(!hiddenDismiss&&!visibleReading&&!current.completed)await capture(`${String(count).padStart(3,'0')}-${recipe?recipe.result.id.slice(3):'chapter-'+(current.chapter+1)+'-start'}`);
 }
 // The final advance waits for the ending artwork to decode before committing.
 await expect.poll(async()=>(await saved()).completed,{timeout:30_000}).toBe(true);
 await capture('completed-ending');expect(errors).toEqual([]);expect(failed).toEqual([]);
 const outcome={sourceSha256:createHash('sha256').update(source).digest('hex'),viewport,combinations:count,chapters:story.chapters.length,mobileTouch:!!cdp,chapterReloads:true,processMarginDrop:true,referencePanel:true,errors,failed,rearrangements,measurements};
 fs.writeFileSync(path.join(out,'outcome.json'),JSON.stringify(outcome,null,2)+'\n');
 console.log(JSON.stringify({viewport,combinations:count,chapters:story.chapters.length,passed:true}));
}catch(error){
 await page.screenshot({path:path.join(out,'failure.png')});
 fs.writeFileSync(path.join(out,'failure.json'),JSON.stringify({error:String(error),count,currentChapter:current.chapter+1,saved:await saved(),errors,failed,rearrangements,measurements},null,2));throw error;
}finally{await browser.close();}
