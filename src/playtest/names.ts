import type {Story} from '../story/types.ts';
import type {State} from '../engine/types.ts';
import {label} from '../engine/game.ts';

const normalized = (text:string) => text.trim().replace(/\s+/g,' ').toLocaleLowerCase('en');
export function hasCopyHandle(name:string):boolean {return / \(#[1-9]\d*\)$/.test(normalized(name.replace(/\[.*\]$/,'')));}

/** Copy handles belong to the text interface, never the story's item names.
 * Encounter order keeps a known copy's handle stable after another retires.
 * Looking only at encountered tokens avoids revealing future identities.
 * The (#n) suffix is reserved: a literal name ending that way gets its own
 * suffix, so a later authored name cannot steal an earlier selection handle. */
export function itemSelection(story:Story,state:State,id:string):{name:string;aliases:string[]} {
  const base = label(story,state,id);
  const full = (name:string) => story.items[id]?.compound ? `${name}[${(state.tokens[id]?.slots ?? []).map(part => label(story,state,part)).join(',')}]` : name;
  const tokens = Object.values(state.tokens);
  const known = tokens.map((token,index)=>({token,order:token.firstSeen?.order??index}))
    .filter(({token})=>normalized(label(story,state,token.id))===normalized(base))
    .sort((a,b)=>a.order-b.order||a.token.id.localeCompare(b.token.id));
  const index = known.findIndex(({token})=>token.id===id);
  if (index < 0) return {name:full(base),aliases:[base,full(base)]};
  const reserved = hasCopyHandle(base), numbered = `${base} (#${index+1})`;
  const active = known.filter(({token})=>token.status==='available'&&token.chapter===state.chapter);
  return {
    name: full(reserved || active.length>1&&active.some(({token})=>token.id===id) ? numbered : base),
    aliases: [...(reserved ? [] : [base,full(base)]),numbered,full(numbered)],
  };
}

export function itemName(story:Story,state:State,id:string):string {return itemSelection(story,state,id).name;}
