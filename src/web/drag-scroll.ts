const edgeSize = 55;
const holdTime = 250;
const pixelsPerSecond = 480;

/** One eligible item gesture owns its edge hold until release, exit or cancellation. */
export class DragEdgeScroll {
  private direction = 0;
  private frame = 0;
  private previousTime = 0;
  private activeBoundary = 0;

  constructor(
    private viewport: HTMLElement,
    private artworkEdges: () => {left: number; right: number},
    private scrollArtwork: (distance: number) => void,
    private leaveEdge: (direction: number) => void,
  ) {}

  update(clientX: number) {
    // A changing artwork width must not move the edge out from under a hold.
    if ((this.direction < 0 && clientX < this.activeBoundary) ||
        (this.direction > 0 && clientX > this.activeBoundary)) return;
    const previous = this.direction;
    if (previous) {
      this.stop();
      this.leaveEdge(previous);
    }
    const {left, right} = this.artworkEdges();
    const threshold = Math.min(edgeSize, (right - left) / 2);
    const direction = clientX < left + threshold ? -1 : clientX > right - threshold ? 1 : 0;
    if (!direction || direction === previous || !this.canScroll(direction)) return;
    this.direction = direction;
    this.activeBoundary = direction < 0 ? left + threshold : right - threshold;
    this.previousTime = performance.now() + holdTime;
    this.frame = requestAnimationFrame(this.tick);
  }

  stop() {
    cancelAnimationFrame(this.frame);
    this.frame = 0;
    this.direction = 0;
  }

  private canScroll(direction: number) {
    return direction < 0 ? this.viewport.scrollLeft > 0
      : this.viewport.scrollLeft < this.viewport.scrollWidth - this.viewport.clientWidth;
  }

  private tick = (time: number) => {
    this.frame = 0;
    if (!this.viewport.isConnected || !this.canScroll(this.direction)) { this.stop(); return; }
    if (time > this.previousTime) {
      // Cap a delayed frame so a busy tab cannot jump across a chapter.
      const elapsed = Math.min(32, time - this.previousTime);
      this.previousTime = time;
      this.scrollArtwork(this.direction * pixelsPerSecond * elapsed / 1000);
    }
    this.frame = requestAnimationFrame(this.tick);
  };
}
