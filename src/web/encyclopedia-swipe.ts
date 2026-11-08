type BookPage = 'index' | 'detail' | 'spread';

interface Swipe {
  pointer: number;
  x: number;
  y: number;
  time: number;
  page: BookPage;
  track: HTMLElement;
  distance: number;
  origin: number;
  claimed: boolean;
}

/** Touch page navigation and outward dismissal; vertical scrolling stays native. */
export class EncyclopediaSwipe {
  private swipe?: Swipe;
  private dismissal?: { track: HTMLElement; animation: Animation };
  private suppressClick = false;
  private reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

  constructor(private root: HTMLElement, private page: () => BookPage | undefined,
    private turn: (detail: boolean) => void, private close: () => void) {
    document.addEventListener('pointerdown', event => {
      if (this.swipe && event.pointerId !== this.swipe.pointer) { this.cancel(); return; }
      if (event.isPrimary) this.suppressClick = false;
    }, true);
    root.addEventListener('pointerdown', this.begin);
    document.addEventListener('pointermove', this.move);
    document.addEventListener('pointerup', this.end);
    document.addEventListener('pointercancel', event => {
      if (event.pointerId === this.swipe?.pointer) this.cancel();
    });
    root.addEventListener('lostpointercapture', event => {
      // A touched descendant loses its implicit capture when the book claims it.
      // Only loss from our own capture is an interruption.
      if (event.target === root && event.pointerId === this.swipe?.pointer && event.buttons !== 0) this.cancel();
    });
    // The release must not activate a link or the game revealed by dismissal.
    document.addEventListener('click', event => {
      if (!this.suppressClick || event.detail === 0) return;
      this.suppressClick = false;
      event.preventDefault(); event.stopPropagation();
    }, true);
    root.addEventListener('click', event => {
      if (this.dismissal) { event.preventDefault(); event.stopPropagation(); }
    }, true);
    // A native selection or callout takes precedence over an undecided swipe.
    root.addEventListener('selectstart', () => this.cancel());
    root.addEventListener('contextmenu', () => this.cancel());
    window.addEventListener('blur', () => this.cancel());
    window.addEventListener('resize', () => this.cancel());
    document.addEventListener('visibilitychange', () => { if (document.hidden) this.cancel(); });
    this.reducedMotion.addEventListener('change', () => this.cancel());
  }

  cancel() {
    const dismissal = this.dismissal;
    this.dismissal = undefined;
    dismissal?.animation.cancel();
    const swipe = this.swipe;
    this.swipe = undefined;
    const track = swipe?.track ?? dismissal?.track;
    track?.style.removeProperty('transform');
    track?.style.removeProperty('transition');
    if (swipe && this.root.hasPointerCapture(swipe.pointer)) this.root.releasePointerCapture(swipe.pointer);
  }

  private hasSelection() {
    const selection = getSelection();
    return selection && !selection.isCollapsed &&
      (this.root.contains(selection.anchorNode) || this.root.contains(selection.focusNode));
  }

  private begin = (event: PointerEvent) => {
    if (event.pointerType !== 'touch' || !event.isPrimary || event.button !== 0 || this.swipe || this.dismissal) return;
    const page = this.page(), target = event.target instanceof Element ? event.target : undefined;
    const track = target?.closest<HTMLElement>('.encyclopedia-track');
    if (page === undefined || !track || this.hasSelection() || target?.closest('button, input, textarea, select, [contenteditable]')) return;
    const index = track.querySelector('.encyclopedia-index')!, reading = track.querySelector('.encyclopedia-detail')!;
    this.swipe = {
      pointer: event.pointerId, x: event.clientX, y: event.clientY, time: event.timeStamp,
      page, track, distance: reading.getBoundingClientRect().left - index.getBoundingClientRect().left,
      origin: new DOMMatrixReadOnly(getComputedStyle(track).transform).m41, claimed: false,
    };
  };

  private move = (event: PointerEvent) => {
    const swipe = this.swipe;
    if (!swipe || event.pointerId !== swipe.pointer) return;
    if (this.page() !== swipe.page || !swipe.track.isConnected || this.hasSelection()) { this.cancel(); return; }
    const dx = event.clientX - swipe.x, dy = event.clientY - swipe.y;
    if (!swipe.claimed) {
      // Leave holds to native text selection and reject diagonal/vertical intent
      // before taking capture. Never prevent the initial press or ordinary taps.
      if (event.timeStamp - swipe.time > 400) { this.cancel(); return; }
      if (Math.hypot(dx, dy) < 10) return;
      if (Math.abs(dx) < Math.abs(dy) * 1.5) { this.cancel(); return; }
      swipe.claimed = true;
      this.suppressClick = true;
      this.root.setPointerCapture(swipe.pointer);
    }
    event.preventDefault();
    if (!this.reducedMotion.matches) {
      // An inward drag stops on the facing page. It cannot also dismiss the
      // book in the same gesture, even if it crosses that page's resting point.
      let position = swipe.origin + dx;
      if (swipe.page === 'index') position = Math.max(-swipe.distance, position);
      if (swipe.page === 'detail') position = Math.min(0, position);
      swipe.track.style.transition = 'none';
      swipe.track.style.transform = `translateX(${position}px)`;
    }
  };

  private end = (event: PointerEvent) => {
    if (event.pointerId !== this.swipe?.pointer) return;
    // Fast releases can carry travel that was never delivered in a move event.
    this.move(event);
    const swipe = this.swipe;
    if (!swipe) return;
    const dx = event.clientX - swipe.x;
    const commit = swipe.claimed && Math.abs(dx) >= Math.min(80, swipe.distance * .22);
    // Resolve the last dragged position before restoring the CSS transition.
    // Reconciliation can then change pages without snapping to an intermediate end.
    if (swipe.claimed) swipe.track.getBoundingClientRect();
    if (commit && (swipe.page === 'spread' || (dx > 0) === (swipe.page === 'index'))) {
      this.slideOut(swipe, dx > 0 ? 1 : -1);
      return;
    }
    this.cancel();
    if (commit) this.turn(swipe.page === 'index');
  };

  private slideOut(swipe: Swipe, direction: number) {
    const { track } = swipe;
    const from = getComputedStyle(track).transform;
    const book = track.getBoundingClientRect(), viewport = this.root.getBoundingClientRect();
    const destination = new DOMMatrixReadOnly(from).m41 +
      (direction > 0 ? viewport.right - book.left : viewport.left - book.right);
    this.cancel();
    if (this.reducedMotion.matches) { this.close(); return; }
    // Keep the dialog's input barrier until the whole book has left the pane.
    // Refresh/resize/Close can cancel this animation without a stale callback.
    track.style.transition = 'none';
    track.style.transform = from;
    const animation = track.animate([{ transform: from }, { transform: `translateX(${destination}px)` }],
      { duration: 220, easing: 'ease-out', fill: 'forwards' });
    this.dismissal = { track, animation };
    void animation.finished.then(() => {
      if (this.dismissal?.animation !== animation) return;
      this.cancel();
      this.close();
    }, () => {});
  }
}
