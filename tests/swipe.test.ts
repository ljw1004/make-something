import assert from 'node:assert/strict';
import {test} from 'node:test';
import {completesSwipe, SwipeMotion} from '../src/web/swipe.ts';

const sample = (clientX: number, timeStamp: number, clientY = 0) => ({clientX, clientY, timeStamp});

test('a swipe completes at 65 CSS pixels in either direction', () => {
  for (const sign of [-1, 1]) {
    assert(!completesSwipe(sign * 64.9));
    assert(completesSwipe(sign * 65));
  }
});

test('a flick coasts farther than a slow drag that moves the same distance', () => {
  for (const {interval, advances} of [{interval:16, advances:true}, {interval:120, advances:false}]) {
    const motion = new SwipeMotion(sample(0, 0));
    motion.track(sample(-30, interval));
    motion.track(sample(-60, interval * 2));
    const projected = motion.project(sample(-60, interval * 2 + 4), 'x');
    assert(projected < 0);
    assert.equal(completesSwipe(projected), advances);
  }
});

test('a pause leaves only the distance moved', () => {
  const motion = new SwipeMotion(sample(0, 0));
  motion.track(sample(70, 25));
  assert.equal(motion.project(sample(70, 100), 'x'), 70);
});

test('a reversal uses the last movement on the navigation axis', () => {
  const motion = new SwipeMotion(sample(0, 0));
  motion.track(sample(15, 20, 140));
  motion.track(sample(20, 40, 200));
  motion.track(sample(17, 56, 135));
  const projected = motion.project(sample(17, 59, 135), 'y');
  assert(projected < 0);
  assert(completesSwipe(projected));
});
