import {test} from 'node:test';
import assert from 'node:assert/strict';
import {parseStory} from '../src/story/parser.ts';
import {startAdventure,choose,renderFrame} from '../src/playtest/adventure.ts';
import {terminalFrame,terminalMarkdown} from '../src/web/text-terminal-frame.ts';
import {terminalStory} from './fixtures/text-terminal.ts';

test('terminal presentation omits the story introduction without changing runner state',()=>{
  const story=parseStory(terminalStory,{id:'terminal'});
  let adventure=startAdventure(story,{playStyle:'fast'});
  while (true) {
    const before=structuredClone(adventure);
    const frame=terminalFrame(story,adventure);
    assert(frame.messages.every(message=>message.kind !== 'story'));
    assert.deepEqual(frame.messages,adventure.frame.messages.filter(message=>message.kind !== 'story'));
    assert.doesNotMatch(terminalMarkdown(renderFrame(frame)),/<img/);
    assert.equal(terminalFrame(story,adventure,true).messages[0].kind,'board');
    assert.deepEqual(adventure,before);
    if (adventure.frame.phase !== 'choose') break;
    adventure=choose(story,adventure,adventure.frame.step,1);
  }
  assert(adventure.state.completed);
});

test('terminal Markdown styles text, preserves line breaks and escapes HTML without loading images',()=>{
  const html=terminalMarkdown('## Chapter 2. Arrival\n**Bold** and *italic* and `code`.\n![A workshop](workshop.svg)\n<script>unsafe</script>');
  assert.match(html,/role="heading" aria-level="2">Chapter 2\. Arrival/);
  assert.match(html,/<strong>Bold<\/strong> and <em>italic<\/em> and <code>code<\/code>/);
  assert.match(html,/\nA workshop\n&lt;script&gt;unsafe&lt;\/script&gt;/);
  assert.doesNotMatch(html,/<img|<script|workshop.svg/);
});
