/** Shared-parser inventory used to compose the retained artwork review gallery. */
import{readFileSync}from'node:fs';import{resolve}from'node:path';
import{parseStory}from'../../../src/story/parser.ts';import{itemPresentation}from'../../../src/engine/presentation.ts';
const story=parseStory(readFileSync(resolve(import.meta.dirname,'../anatomy.md'),'utf8'));
const chapters=story.chapters.slice(0,28).map((c,n)=>{
 const ids=[...new Set(c.items.map(r=>r.id))];
 return{number:n+1,title:c.name,icons:ids.map(id=>{const p=itemPresentation(story,n,id);return{id,name:p.name,path:p.icon?.url,slots:story.items[id].slots.filter(s=>ids.includes(s.accepts)).map(s=>({name:story.items[s.accepts].name,path:s.icon?.url}))}})};
});
console.log(JSON.stringify(chapters));
