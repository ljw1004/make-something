import {readFileSync,writeFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname,resolve} from 'node:path';
import {parseStory} from '../../../../src/story/parser.ts';
const root=dirname(fileURLToPath(import.meta.url));
const original=readFileSync(resolve(root,'../../anatomy.md'),'utf8');
const story=parseStory(original);
const files={};
for(const id of ['prelude-phospholipids','prelude-water','opening-dna','opening-nuclear-envelope','opening-nucleus','opening-cell','prelude-myoblasts','school-bone-mineral']) files['id:'+id]=id;
files['id:arm-front-tendons']='arm-front-base';files['id:arm-back-tendons']='arm-back-base';
const names=['Outer ears and canals','Eardrums','Outer ears with eardrums','Middle-ear bones','Sound-conducting ears','Coiled inner-ear chambers and fluid','Hearing cells with tiny hairs','Vibration-sensitive inner ears','Sound-receiving ears','Hearing pathways','Inner ears with hearing pathways','Ears'];
const ear=['outer-ear','eardrum','ear-drum','ear-bones','conducting-ear','cochlea','hair-cells','sensing-ear','receiving-ear','hearing-pathways','inner-pathways','ears'];
names.forEach((n,i)=>files['name:'+n]=ear[i]);
['Starchy food','Saliva','Shorter starch chains','Digestive enzymes','Meal glucose','Protein food','Meal amino acids','Fat food','Bile','Small fat droplets','Fat digestion products'].forEach((n,i)=>files['name:'+n]=['starch','saliva','short-starch','enzymes','glucose','protein-food','amino-acids','fat','bile','small-droplets','fat-products'][i]);
function identity(text){
  const id=text.match(/^`([^`]+)`/); if(id)return 'id:'+id[1];
  return 'name:'+text.replace(/ \((?:compound|exclusive with .*?)\)$/,'').trim();
}
let section='',chapter=0,owner;const seen=new Set();const out=[];
for(let line of original.split('\n')){
  line=line.replaceAll('(placeholder.svg)','(../../placeholder.svg)');
  if(line.startsWith('## ')){chapter++;section='';owner=undefined;}
  if(line.startsWith('background:')&&[1,4,8,18].includes(chapter))line=line.replace('../../placeholder.svg','assets/background-'+({1:'cell',4:'arm',8:'hearing',18:'meal'}[chapter])+'.png');
  if(/^\*\*[^*]+\*\*$/.test(line)){section=line;owner=undefined;}
  if(section==='**Hotspots**'&&chapter===4&&line.startsWith('- `arm-')){
    const front=line.includes('front');
    out.push(line+' (center 780px, 1170px)');
    out.push(front?'  - hitbox: (center 535px, 900px) (size 540px, 1360px)':'  - hitbox: (center 1090px, 900px) (size 500px, 1360px)');
    continue;
  }
  if(section==='**Items**'&&line.startsWith('- ')){
    owner=identity(line.slice(2));out.push(line);
    if(story.items[owner]&&!seen.has(owner)){
      out.push(`  - icon: ![${story.items[owner].name}](assets/${files[owner]||'neutral'}.png)`);seen.add(owner);
    }
    continue;
  }
  if(section==='**Items**'&&/^  - (?:unnamed )?slot:/.test(line)){
    let file='neutral-overlay';
    if(owner==='id:opening-cell')file=line.includes('`opening-nucleus`')?'cell-nucleus-overlay':'cell-neutral-overlay';
    if(owner==='id:arm-front-tendons'||owner==='id:arm-back-tendons'){
      const side=owner.includes('front')?'front':'back';
      file=`arm-${side}-${line.includes('school-bone-mineral')?'mineral':'muscle'}-overlay`;
    }
    line+=`, icon: ![Fitted part](assets/${file}.png)`;
  }
  out.push(line);
}
writeFileSync(resolve(root,'anatomy.md'),out.join('\n'));
console.log(JSON.stringify({icons:seen.size,items:Object.keys(story.items).length,missing:Object.keys(story.items).filter(id=>!seen.has(id))}));
