import {test} from 'node:test';
import assert from 'node:assert/strict';
import {catalogueStoryStarted} from '../src/web/chapter-recovery.ts';

const hasStarted = (state: unknown, chapterSession?: unknown) => catalogueStoryStarted(JSON.stringify({state,chapterSession}));

test('carousel labels new, move-only and legacy first-chapter saves by actual combinations', () => {
  const move = {type:'move'}, combo = {type:'combine'};
  assert.equal(catalogueStoryStarted(null), false);
  assert.equal(catalogueStoryStarted('invalid JSON'), false);
  assert.equal(hasStarted(null), false);
  assert.equal(hasStarted({chapter:-1, actions:[combo]}), false);
  assert.equal(hasStarted({chapter:0, actions:[move]}, {movement:true}), false);
  assert.equal(hasStarted({chapter:0, actions:[move]}, {combined:false}), false);
  assert.equal(hasStarted({chapter:0, actions:[move]}, {combined:true}), true);
  assert.equal(hasStarted({chapter:0, actions:[move, combo]}, {moved:true}), true);
  assert.equal(hasStarted({chapter:0, actions:[combo, {type:'advance'}, move]}), false);
});
test('later or completed chapters continue even without a current chapter combination', () => {
  assert.equal(hasStarted({chapter:1, completed:false, actions:[]}, {combined:false}), true);
  assert.equal(hasStarted({chapter:0, completed:true, actions:[]}, {combined:false}), true);
});
