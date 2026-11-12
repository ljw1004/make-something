import {test,expect} from '@playwright/test';
import type {Page} from '@playwright/test';
import {readFileSync} from 'node:fs';
import {parseStory} from '../src/story/parser.ts';
import {storyIds} from '../src/story/load.ts';
import {terminalMarkdown} from '../src/web/text-terminal-frame.ts';
import {startAdventure,choose,renderFrame} from '../src/playtest/adventure.ts';
import type {Adventure} from '../src/playtest/adventure.ts';
import {parseCommand} from '../src/playtest/commands.ts';
import type {PlayStyle} from '../src/playtest/commands.ts';
import {terminalStory} from './fixtures/text-terminal.ts';

test.use({viewport:{width:1440,height:1000}});
const story=parseStory(terminalStory,{id:'terminal'});
const output=(page:Page)=>page.locator('[data-terminal-output]').last().locator('[data-terminal-text]').evaluateAll(nodes=>nodes.map(node=>node.textContent).join(''));
const expected=(adventure:Adventure)=>terminalMarkdown(renderFrame({...adventure.frame,
  messages:adventure.frame.messages.filter(message=>message.kind!=='story').map(message=>message.kind==='chapter'?{...message,text:'\n\n'+message.text}:message),
  options:adventure.frame.options.filter(option=>option.kind==='action'),
  ...(adventure.playStyle==='detailed' && adventure.frame.prompt ? {prompt:`What will you [I]nspect or [C]ombine for step number ${adventure.frame.step}?`} : {}),
})).replace(/<[^>]*>/g,'').replace(/&(amp|lt|gt|quot|#39);/g,(_,entity:string)=>({amp:'&',lt:'<',gt:'>',quot:'"','#39':"'"}[entity]!));
async function fixture(page:Page,style:PlayStyle) {
  await page.route('**/terminal-fixture/story.md',route=>route.fulfill({contentType:'text/markdown',body:terminalStory}));
  await page.goto(`/simulator-${style==='fast'?'story':'interactions'}.html?story=terminal-fixture/story.md`);
  await expect(page.locator('#prompt')).toBeVisible();
}

for (const style of ['fast','detailed'] as const) test(`${style} terminal matches the original runner from beginning to ending`,async({page})=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await fixture(page,style);
  let adventure=startAdventure(story,{playStyle:style});
  expect(await output(page)).toBe(expected(adventure));
  const lines=style==='fast' ? ['1','1','1','1'] : ['inspect Sheet','inspect Lid','inspect Case','inspect Label'];
  for (const line of lines) {
    await page.locator('#command').fill(line);await page.locator('#command').press('Enter');
    adventure=choose(story,adventure,adventure.frame.step,style==='fast' ? Number(line) : parseCommand(line));
    await expect.poll(()=>output(page)).toBe(expected(adventure));
  }
  expect(adventure.state.completed).toBe(true);
  await expect(page.locator('#prompt')).toBeHidden();
  await expect(page.locator('#transcript img')).toHaveCount(0);
  await expect(page.locator('.command-echo')).toHaveCount(4);
  await expect(page.locator('#transcript')).toContainText('The workshop opens.');
  await expect(page.locator('#transcript')).toContainText('The van disappears around the corner.');
  expect(await page.evaluate(()=>Object.keys(localStorage))).toEqual([]);
  await expect(page).toHaveURL(new RegExp(`chapter=${adventure.state.chapter+1}$`));
  await page.reload();await expect.poll(()=>output(page)).toBe(expected(startAdventure(story,{chapter:adventure.state.chapter+1,playStyle:style})));
  expect(errors).toEqual([]);
});

test('human refreshes and errors leave decisions intact; detailed typing completes aggressively with fallback overtyping',async({page})=>{
  await fixture(page,'detailed');
  const command=page.locator('#command');
  for (let i=0;i<2;i++) {await command.press('Enter');await expect.poll(()=>output(page)).toContain('step number 1');}
  await expect(page.locator('#transcript img')).toHaveCount(0);
  await command.fill('inspect Unavailable');await command.press('Enter');
  await expect(page.getByRole('alert')).toContainText('No available item or hotspot matches');
  await command.pressSequentially('i');await expect(command).toHaveValue('Inspect ');
  await expect(page.locator('.command-line')).toContainText('Inspect');
  await command.pressSequentially('Sh');await expect(command).toHaveValue('Inspect She'); // Sheet and Shelf both match.
  await command.pressSequentially('ee');await expect(command).toHaveValue('Inspect Sheet');
  await expect(page.locator('.command-line')).toContainText('Inspect Sheet');
  await command.press('Backspace');await expect(command).toHaveValue('Inspect She');
  await command.pressSequentially('e');await expect(command).toHaveValue('Inspect Sheet');
  await command.press('Backspace');await expect(command).toHaveValue('Inspect She');
  await command.press('Backspace');await expect(command).toHaveValue('Inspect ');
  await command.press('Backspace');await expect(command).toHaveValue('');
  await command.fill('combine Sheet with ');
  await command.press('Backspace');await expect(command).toHaveValue('combine Sheet ');
  await command.fill('inspect Sheet');await command.press('ArrowLeft');
  await command.press('Backspace');await expect(command).toHaveValue('inspect Shet');
  await command.fill('inspect Sheet');await command.press('Shift+ArrowLeft');
  await command.press('Backspace');await expect(command).toHaveValue('inspect Shee');
  await command.fill('inspect Sheet');
  await command.press('Enter');
  await expect.poll(()=>output(page)).toContain('Transformed into: Case');
  await command.press('ArrowUp');await expect(command).toHaveValue('');
  await command.press('ArrowDown');await expect(command).toHaveValue('');
  await expect.poll(()=>output(page)).toContain('step number 2');

  await fixture(page,'fast');
  await command.fill('12');await command.press('Backspace');await expect(command).toHaveValue('1');
  await command.fill('999');await command.press('Enter');
  await expect(page.getByRole('alert')).toContainText('Choose an option');
  await command.fill('look');await command.press('Enter');
  await expect.poll(()=>output(page)).toContain('step number 1');
  await expect(page.locator('#transcript img')).toHaveCount(0);
});

test('100-character column stays stable on wide resize and output leaves the prompt onscreen',async({page})=>{
  await fixture(page,'fast');
  const initial=await page.locator('.terminal').boundingBox();
  const measure=await page.locator('.terminal').evaluate(node=>{
    const probe=document.createElement('span');probe.textContent='0'.repeat(100);node.append(probe);
    const width=probe.getBoundingClientRect().width;probe.remove();return width;
  });
  expect(initial!.width).toBeCloseTo(measure,0);
  await page.setViewportSize({width:1800,height:1000});
  expect((await page.locator('.terminal').boundingBox())!.width).toBeCloseTo(initial!.width,1);
  await page.setViewportSize({width:800,height:400});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await page.locator('#command').press('Enter');
  await expect(page.locator('#prompt')).toBeInViewport({ratio:1});
  const before=await page.evaluate(()=>scrollY);
  await page.keyboard.press('ArrowUp');await page.keyboard.press('ArrowDown');
  expect(await page.evaluate(()=>scrollY)).toBe(before);
  await expect(page.locator('#command')).toHaveValue('');
  await expect(page.locator('#transcript img')).toHaveCount(0);
});

test('both pages list current stories, load their unchanged runner openings, and report missing manuscripts',async({page})=>{
  const paths=storyIds();
  for (const style of ['fast','detailed'] as const) {
    await page.goto(`/simulator-${style==='fast'?'story':'interactions'}.html`);
    await expect(page.locator('#story-picker [data-story]')).toHaveCount(paths.length);
    await expect(page.locator('h1')).toHaveText(`MAKE SOMETHING WORTHWHILE [${style==='fast'?'story':'interaction'} simulator]`);
    await expect(page.locator('a,nav')).toHaveCount(0);
    await expect(page.locator('#story-picker')).toContainText('6. THEOLOGY. You are Augustine, Aquinas, Martin Luther.');
    await page.locator('#command').fill('999');await page.locator('#command').press('Enter');
    await expect(page.getByRole('alert')).toContainText('Choose a story number');
    await page.locator('#command').fill('6');await page.locator('#command').press('Enter');
    await expect.poll(()=>output(page)).toContain('Augustine');
    expect(new URL(page.url()).searchParams.get('story')).toBe('stories/theology/theology.md');
    expect(new URL(page.url()).searchParams.get('chapter')).toBe('1');
    await expect(page.locator('#story-picker')).toBeVisible();
    await expect(page.locator('.story-selection')).toHaveText('> 6');
    await page.goBack();
    await expect(page.locator('#story-picker')).toBeVisible();
    expect(new URL(page.url()).searchParams.has('story')).toBe(false);
    for (const path of paths) {
      await page.goto(`/simulator-${style==='fast'?'story':'interactions'}.html?story=stories/${path}`);
      const source=parseStory(readFileSync(`stories/${path}`,'utf8'),{id:path});
      const adventure=startAdventure(source,{playStyle:style});
      await expect.poll(()=>output(page)).toBe(expected(adventure));
      await expect(page.locator('#transcript img')).toHaveCount(0);
    }
  }
  await page.goto('/simulator-story.html?story=missing-terminal-story.md');
  await expect(page.getByRole('status')).toContainText('HTTP 404');
  await expect(page.getByRole('link',{name:'Try again'})).toBeVisible();
  await expect(page.locator('#prompt')).toBeHidden();
});

test('direct chapter URLs use original checkpoints, including skips and invalid requests',async({page})=>{
  await fixture(page,'fast');
  for (const chapter of [3,4,5]) {
    await page.goto(`/simulator-story.html?story=terminal-fixture/story.md&chapter=${chapter}`);
    const adventure=startAdventure(story,{chapter});
    await expect.poll(()=>output(page)).toBe(expected(adventure));
    expect(new URL(page.url()).searchParams.get('chapter')).toBe(String(adventure.state.chapter+1));
    await expect(page.locator('#transcript img')).toHaveCount(0);
  }
  for (const chapter of ['0','-1','1.5','cat','',String(story.chapters.length+1)]) {
    await page.goto(`/simulator-story.html?story=terminal-fixture/story.md&chapter=${chapter}`);
    await expect(page.getByRole('status')).toContainText('Chapter must be');
    await expect(page.locator('#prompt')).toBeHidden();
  }
});

for (const style of ['fast','detailed'] as const) test(`${style} chapter URL changes retain the chosen branch; reopening synthesizes a new checkpoint`,async({page})=>{
  const source=`# A choice
## Workshop
**Goals**
- Ready
  - Ticket
  - Gift
**Items**
- Paper
- Ribbon
- Gift
- Switch
- Button
- Ticket
**Combinations**
- Paper + Ribbon -> Gift
- Switch + Button -> Ticket
## Dispatch
**Goals**
- Send it -- Parcel
**Items**
- Parcel
- Stamp
**Combinations**
- Gift + Stamp -> Parcel
- Ticket + Stamp -> Parcel
`;
  const parsed=parseStory(source,{id:'optional'});
  let loads=0;
  await page.route('**/optional.md',route=>{loads++;return route.fulfill({body:source});});
  await page.goto(`/simulator-${style==='fast'?'story':'interactions'}.html?story=optional.md`);
  let adventure=startAdventure(parsed,{playStyle:style});
  await expect.poll(()=>output(page)).toBe(expected(adventure));
  const historyLength=await page.evaluate(()=>window.history.length);
  for (const item of ['Paper']) {
    const command=style==='fast' ? String(adventure.frame.options.find(option=>option.text.startsWith(item+' +'))!.choice) : `inspect ${item}`;
    await page.locator('#command').fill(command);await page.locator('#command').press('Enter');
    adventure=choose(parsed,adventure,adventure.frame.step,style==='fast'?Number(command):parseCommand(command));
    await expect.poll(()=>output(page)).toBe(expected(adventure));
  }
  expect(adventure.state.chapter).toBe(1);
  await expect.poll(()=>output(page)).toContain('- Gift');
  expect(new URL(page.url()).searchParams.get('chapter')).toBe('2');
  expect(loads).toBe(1);
  expect(await page.evaluate(()=>window.history.length)).toBe(historyLength);
  expect(await page.evaluate(()=>Object.keys(localStorage))).toEqual([]);
  await page.reload();
  const checkpoint=startAdventure(parsed,{chapter:2,playStyle:style});
  await expect.poll(()=>output(page)).toBe(expected(checkpoint));
  expect(await output(page)).not.toContain('- Gift');
  expect(loads).toBe(2);
});
