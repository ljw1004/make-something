import {test,expect} from '@playwright/test';
import type {Page} from '@playwright/test';
import {readFileSync} from 'node:fs';
import {parseStory} from '../src/story/parser.ts';
import {storyIds} from '../src/story/load.ts';
import {background} from '../src/engine/analysis.ts';
import {startAdventure,choose,renderFrame} from '../src/playtest/adventure.ts';
import type {Adventure} from '../src/playtest/adventure.ts';
import {parseCommand} from '../src/playtest/commands.ts';
import type {PlayStyle} from '../src/playtest/commands.ts';
import {terminalStory} from './fixtures/text-terminal.ts';

test.use({viewport:{width:1440,height:1000}});
const svg='<svg xmlns="http://www.w3.org/2000/svg" width="600" height="900"><rect width="600" height="900" fill="#263b45"/></svg>';
const story=parseStory(terminalStory,{id:'terminal'});
const output=(page:Page)=>page.locator('[data-terminal-output]').last().locator('[data-terminal-text]').evaluateAll(nodes=>nodes.map(node=>node.textContent).join(''));
const expected=(adventure:Adventure)=>renderFrame({...adventure.frame,
  options:adventure.frame.options.filter(option=>option.kind==='action'),
  ...(adventure.playStyle==='detailed' && adventure.frame.prompt ? {prompt:`What will you [I]nspect or [C]ombine for step number ${adventure.frame.step}?`} : {}),
});
async function fixture(page:Page,style:PlayStyle) {
  await page.route('**/terminal-fixture/story.md',route=>route.fulfill({contentType:'text/markdown',body:terminalStory}));
  await page.route('**/terminal-fixture/*.svg',route=>route.fulfill({contentType:'image/svg+xml',body:svg}));
  await page.goto(`/text-${style}.html?story=terminal-fixture/story.md`);
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
  expect(await page.locator('.chapter-picture').evaluateAll(nodes=>nodes.map(n=>n.getAttribute('data-chapter')))).toEqual(['0','1','3','4']);
  await expect(page.locator('.command-echo')).toHaveCount(4);
  await expect(page.locator('#transcript')).toContainText('The workshop opens.');
  await expect(page.locator('#transcript')).toContainText('The van disappears around the corner.');
  expect(await page.evaluate(()=>Object.keys(localStorage))).toEqual([]);
  await page.reload();await expect.poll(()=>output(page)).toBe(expected(startAdventure(story,{playStyle:style})));
  expect(errors).toEqual([]);
});

test('human refreshes and errors leave decisions intact; detailed typing uses the existing name completer',async({page})=>{
  await fixture(page,'detailed');
  const command=page.locator('#command');
  for (let i=0;i<2;i++) {await command.press('Enter');await expect.poll(()=>output(page)).toContain('step number 1');}
  await expect(page.locator('.chapter-picture')).toHaveCount(2);
  await command.fill('inspect Unavailable');await command.press('Enter');
  await expect(page.getByRole('alert')).toContainText('No available item or hotspot matches');
  await command.pressSequentially('i');await expect(command).toHaveValue('inspect ');
  await command.pressSequentially('Sh');await expect(command).toHaveValue('inspect Sh'); // Sheet and Shelf both match.
  await command.pressSequentially('ee');await expect(command).toHaveValue('inspect "Sheet"');
  await command.press('Enter');
  await expect.poll(()=>output(page)).toContain('Transformed into: Case');
  await command.press('ArrowUp');await expect(command).toHaveValue('inspect "Sheet"');
  await command.press('ArrowDown');await expect(command).toHaveValue('');
  await expect.poll(()=>output(page)).toContain('step number 2');

  await fixture(page,'fast');
  await command.fill('999');await command.press('Enter');
  await expect(page.getByRole('alert')).toContainText('Choose an option');
  await command.fill('look');await command.press('Enter');
  await expect.poll(()=>output(page)).toContain('step number 1');
  await expect(page.locator('.chapter-picture')).toHaveCount(2);
});

test('100-character column stays stable on wide resize; delayed or failed pictures cannot shift scrollback',async({page})=>{
  let release!:()=>void;
  const gate=new Promise<void>(resolve=>{release=resolve;});
  await page.route('**/terminal-fixture/story.md',route=>route.fulfill({contentType:'text/markdown',body:terminalStory}));
  await page.route('**/terminal-fixture/*.svg',async route=>{await gate;await route.fulfill({contentType:'image/svg+xml',body:svg});});
  await page.goto('/text-fast.html?story=terminal-fixture/story.md',{waitUntil:'domcontentloaded'});
  await expect(page.locator('#command')).toBeAttached();
  await expect(page.locator('.chapter-picture')).toHaveCount(2);
  const initial=await page.locator('.terminal').boundingBox();
  const measure=await page.locator('.terminal').evaluate(node=>{
    const probe=document.createElement('span');probe.textContent='0'.repeat(100);node.append(probe);
    const width=probe.getBoundingClientRect().width;probe.remove();return width;
  });
  expect(initial!.width).toBeCloseTo(measure,0);
  await page.setViewportSize({width:1800,height:1000});
  expect((await page.locator('.terminal').boundingBox())!.width).toBeCloseTo(initial!.width,1);
  await page.evaluate(()=>window.scrollTo(0,250));
  const before=await page.evaluate(()=>({y:scrollY,height:document.documentElement.scrollHeight}));
  release();
  await expect.poll(()=>page.locator('.chapter-picture img').evaluateAll(nodes=>nodes.every(node=>(node as HTMLImageElement).complete))).toBe(true);
  expect(await page.evaluate(()=>({y:scrollY,height:document.documentElement.scrollHeight}))).toEqual(before);
  await page.setViewportSize({width:800,height:1000});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);

  await page.unroute('**/terminal-fixture/*.svg');
  await page.route('**/terminal-fixture/*.svg',route=>route.fulfill({status:404,body:'Missing picture'}));
  await page.reload();
  await expect(page.locator('.picture-error').first()).toBeVisible();
  await page.locator('#command').fill('1');await page.locator('#command').press('Enter');
  await expect.poll(()=>output(page)).toContain('Created: Case');
});

test('both pages list current stories, load their unchanged runner openings, and report missing manuscripts',async({page})=>{
  const paths=storyIds();
  for (const style of ['fast','detailed'] as const) {
    await page.goto(`/text-${style}.html`);
    await expect(page.locator('#story-picker a')).toHaveCount(paths.length);
    for (const path of paths) {
      await page.goto(`/text-${style}.html?story=stories/${path}`);
      const source=parseStory(readFileSync(`stories/${path}`,'utf8'),{id:path});
      const adventure=startAdventure(source,{playStyle:style});
      await expect.poll(()=>output(page)).toBe(expected(adventure));
      await expect(page.locator('.chapter-picture')).toHaveCount(adventure.state.visited.filter(chapter=>background(source,chapter)).length);
    }
  }
  await page.goto('/text-fast.html?story=missing-terminal-story.md');
  await expect(page.getByRole('status')).toContainText('HTTP 404');
  await expect(page.getByRole('link',{name:'Try again'})).toBeVisible();
  await expect(page.locator('#prompt')).toBeHidden();
});
