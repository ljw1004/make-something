const swipeThreshold = 65; // One sixth of the 390 CSS pixel reference width.

export function completesSwipe(displacement: number) {
  return Math.abs(displacement) >= swipeThreshold;
}

type Sample = Pick<PointerEvent, 'clientX' | 'clientY' | 'timeStamp'>;
type PointerSample = Sample & {getCoalescedEvents?: () => Sample[]};

const velocityWindow = 60; // ms
const minimumInterval = 16; // ms
const deceleration = 0.008; // CSS pixels per ms squared

/** Estimate where a released background would coast to without moving it there. */
export class SwipeMotion {
  private readonly start: Sample;
  private readonly samples: Sample[];

  private readonly displayScale: number;

  constructor(start: Sample, displayScale = 1) {
    this.displayScale = displayScale;
    this.start = start;
    this.samples = [start];
  }

  track(event: PointerSample) {
    for (const sample of event.getCoalescedEvents?.() ?? []) this.record(sample);
    this.record(event);
  }

  private record(sample: Sample) {
    const last = this.samples.at(-1)!;
    if (sample.timeStamp < last.timeStamp) return;
    if (sample.timeStamp === last.timeStamp) this.samples[this.samples.length - 1] = sample;
    else this.samples.push(sample);
    // Retain the preceding sample so the velocity window can start mid-segment.
    while (this.samples.length > 2 && this.samples[1].timeStamp <= sample.timeStamp - velocityWindow) this.samples.shift();
  }

  project(event: PointerSample, axis: 'x' | 'y') {
    this.track(event);
    const coordinate = axis === 'x' ? 'clientX' : 'clientY';
    const end = this.samples.at(-1)!;
    const since = end.timeStamp - velocityWindow;
    let start = end[coordinate], time = end.timeStamp, direction = 0;
    for (let i = this.samples.length - 2; i >= 0 && time > since; i--) {
      const sample = this.samples[i];
      const delta = start - sample[coordinate];
      // Use the latest movement after a reversal, including any pause before release.
      if (direction * delta < 0) break;
      direction ||= Math.sign(delta);
      const earlier = Math.max(since, sample.timeStamp);
      start -= delta * (time - earlier) / (time - sample.timeStamp);
      time = earlier;
    }
    const velocity = (end[coordinate] - start) / this.displayScale / Math.max(minimumInterval, end.timeStamp - time);
    const coast = velocity * Math.abs(velocity) / (2 * deceleration);
    return (end[coordinate] - this.start[coordinate]) / this.displayScale + coast;
  }
}
