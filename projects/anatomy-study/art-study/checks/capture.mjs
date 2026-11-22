import {chromium} from '@playwright/test';
import {mkdir,writeFile} from 'node:fs/promises';

// --sample follows all four chapters consecutively through ordinary Continue.
const sample=process.argv.includes('--sample');
const themes=process.argv.slice(2).filter(arg=>arg!=='--sample');
const viewport={width:Number(process.env.CAPTURE_WIDTH||390),height:Number(process.env.CAPTURE_HEIGHT||844)};
const captureFolder=process.env.CAPTURE_HEIGHT||process.env.CAPTURE_WIDTH?`captures-${viewport.width}x${viewport.height}`:'captures';
const chapters=[
  {n:1,name:'An inside of its own',actions:[['id:prelude-phospholipids','id:prelude-water'],['id:opening-dna','id:opening-nuclear-envelope'],['id:opening-nucleus','id:opening-cell']]},
  {n:4,name:'Hard bones and pulling muscles',actions:[['id:school-bone-mineral','id:arm-front-tendons'],['id:prelude-myoblasts','id:arm-front-tendons'],['id:prelude-myoblasts','id:arm-back-tendons'],['id:school-bone-mineral','id:arm-back-tendons']]},
  {n:8,name:'Vibration into signals',actions:[['name:Eardrums','name:Outer ears and canals'],['name:Middle-ear bones','name:Outer ears with eardrums'],['name:Hearing cells with tiny hairs','name:Coiled inner-ear chambers and fluid'],['name:Hearing pathways','name:Vibration-sensitive inner ears'],['name:Inner ears with hearing pathways','name:Sound-conducting ears']]},
  {n:18,name:'Breaking down a meal',actions:[['name:Starchy food','name:Saliva'],['name:Shorter starch chains','name:Digestive enzymes'],['name:Protein food','name:Digestive enzymes'],['name:Fat food','name:Bile'],['name:Small fat droplets','name:Digestive enzymes']]},
];
const browser=await chromium.launch();
const results=[];
async function settle(page){
  await page.waitForTimeout(250);
  await page.evaluate(async()=>{await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});
}
async function dismiss(page){
  await settle(page);
  for(let k=0;k<8;k++){
    const b=page.getByRole('button',{name:/^(Begin|Continue|Close)$/,exact:true});
    if(!await b.count()) break;
    await b.first().click();await settle(page);
  }
}
for(const theme of themes){
  const out=`runs/${sample?'anatomy-sample-flow':'anatomy-style-refresh'}/${captureFolder}/${theme}`;await mkdir(out,{recursive:true});
  const continuous=sample?await browser.newContext({viewport,deviceScaleFactor:2,reducedMotion:'reduce'}):null;
  const continuousPage=continuous?await continuous.newPage():null;
  for(const chapter of chapters.filter(c=>!process.env.CAPTURE_CHAPTERS||process.env.CAPTURE_CHAPTERS.split(',').includes(String(c.n)))){
    const context=continuous??await browser.newContext({viewport,deviceScaleFactor:2,reducedMotion:'reduce'});
    const page=continuousPage??await context.newPage();const errors=[];
    const onError=e=>errors.push(e.message);page.on('pageerror',onError);
    try{
      if(!sample||chapter.n===1){
        await page.goto(`http://127.0.0.1:5173/index.html?story=projects/anatomy-study/art-study/${theme}/${sample?'sample':'anatomy'}.md`);
        await page.getByRole('button',{name:'Start',exact:true}).click();
        await page.getByRole('button',{name:'Begin',exact:true}).click();await dismiss(page);
      }
      if(!sample&&chapter.n!==1){
        await page.getByRole('button',{name:'Toggle debug panel'}).click();
        if(viewport.width>=900){
          await page.getByRole('button',{name:'Chapter',exact:true}).click();
          await page.getByRole('option',{name:`${chapter.n}. ${chapter.name}`,exact:true}).click();
          await page.getByRole('button',{name:'Close debug panel',exact:true}).click();
        }else await page.getByRole('button',{name:`${chapter.n}. ${chapter.name}`,exact:true}).click();
        await page.getByRole('button',{name:'Begin',exact:true}).click();
        await dismiss(page);
      }
      await settle(page);
      await page.screenshot({path:`${out}/chapter-${chapter.n}-entry.png`});
      const panel=page.locator('.chapter-panel').last();
      if(sample&&Number(await panel.getAttribute('data-chapter'))!==chapters.indexOf(chapter))throw Error('Wrong chapter after ordinary Continue');
      const missing=await panel.locator('[data-item], [data-hotspot]').evaluateAll(els=>els.filter(el=>!el.querySelector('img')).map(el=>el.dataset.item??el.dataset.hotspot));
      if(missing.length)throw Error(`Items without artwork: ${missing.join(', ')}`);
      for(const [a,b] of chapter.actions){
        let from=panel.locator(`[data-item=${JSON.stringify(a)}]`);
        let to=panel.locator(`[data-item=${JSON.stringify(b)}], [data-hotspot=${JSON.stringify(b)}]`);
        let ab=await from.boundingBox(),bb=await to.boundingBox();
        if(!ab||!bb) throw new Error(`Missing drag ${a} -> ${b}`);
        if(await to.getAttribute('data-item') && ab.width*ab.height>bb.width*bb.height){[from,to]=[to,from];[ab,bb]=[bb,ab];}
        const pick=await from.evaluate(el=>{const box=el.getBoundingClientRect();for(const [u,v] of [[.5,.5],[.85,.5],[.15,.5],[.5,.15],[.5,.85],[.85,.15],[.85,.85],[.15,.15],[.15,.85]]){const x=box.x+box.width*u,y=box.y+box.height*v,h=document.elementFromPoint(x,y);if(h&&(h===el||el.contains(h)))return{x,y};}return null;});
        if(!pick)throw Error(`Covered source ${a}`);
        await page.mouse.move(pick.x,pick.y);
        await page.mouse.down();await page.mouse.move(bb.x+bb.width/2,bb.y+bb.height/2,{steps:15});await page.mouse.up();
        await dismiss(page);await settle(page);
      }
      await page.getByRole('button',{name:'Continue story',exact:true}).waitFor({state:'visible',timeout:5000});
      // Frame any newly grown movable result that extends beyond the page.
      // This is an ordinary pointer move, also available to the player.
      const scene=await panel.boundingBox();
      for(const el of await panel.locator('[data-item]').all()){
        if(await el.getAttribute('data-hotspot'))continue;
        const id=await el.getAttribute('data-item');
        if(['id:arm-front-tendons','id:arm-back-tendons'].includes(id))continue;
        const box=await el.boundingBox();if(!box||!scene)continue;
        const left=Math.max(0,scene.x)+8,right=Math.min(viewport.width,scene.x+scene.width)-8;
        let dx=box.x<left?left-box.x:box.x+box.width>right?right-box.x-box.width:0;
        if(!dx||box.width>right-left)continue;
        const pick=await el.evaluate(e=>{const b=e.getBoundingClientRect();for(const u of [.5,.2,.8,.05,.95]){const x=b.x+b.width*u,y=b.y+b.height*.5,h=document.elementFromPoint(x,y);if(h&&(h===e||e.contains(h)))return{x,y};}return null;});
        if(pick){await page.mouse.move(pick.x,pick.y);await page.mouse.down();await page.mouse.move(pick.x+dx,pick.y,{steps:12});await page.mouse.up();await settle(page);}
      }
      const complete=true;
      if(!complete) throw new Error('Chapter completion control not visible after actions');
      await page.mouse.move(viewport.width-1,viewport.height-1);await page.waitForTimeout(1800);
      await page.screenshot({path:`${out}/chapter-${chapter.n}.png`});
      const broken=await page.evaluate(()=>[...document.images].filter(i=>i.getAttribute('src')&&(!i.complete||i.naturalWidth===0)).map(i=>i.src));
      await page.reload();await settle(page);
      await page.getByRole('button',{name:'Continue story',exact:true}).waitFor({state:'visible',timeout:10000});
      const restored=await page.getByRole('button',{name:'Continue story',exact:true}).isVisible();
      if(sample){
        await page.getByRole('button',{name:'Continue story',exact:true}).click();
        await page.getByRole('button',{name:'Begin',exact:true}).waitFor({state:'visible'});
        if(chapter.n===18)await page.getByText('This is the end of the four-chapter artwork sample.',{exact:false}).waitFor({state:'visible'});
        await dismiss(page);
        if(chapter.n===18&&Number(await page.locator('.chapter-panel').last().getAttribute('data-chapter'))!==4)throw Error('Sample did not reach its ending');
      }
      results.push({theme,chapter:chapter.n,complete,restored,broken,errors});
      console.log(JSON.stringify(results.at(-1)));
    }catch(e){
      await page.screenshot({path:`out-error.png`.replace('out-error',`${out}/chapter-${chapter.n}-error`)}).catch(()=>{});
      results.push({theme,chapter:chapter.n,error:String(e),errors});console.log(JSON.stringify(results.at(-1)));
    }finally{await writeFile(`${out}/chapter-${chapter.n}-result.json`,JSON.stringify(results.at(-1),null,2));page.off('pageerror',onError);if(!continuous)await context.close();}
    if(sample&&results.at(-1)?.error)break;
  }
  await continuous?.close();
}
await browser.close();
if(results.some(r=>r.error||r.broken?.length||r.errors?.length||!r.restored))process.exitCode=1;
