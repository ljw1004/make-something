import {layoutRect, previewScale} from './device-preview.ts';
type ReadingView = 'popup' | 'index' | 'detail' | 'spread';

interface Swipe {
  pointer: number;
  x: number;
  y: number;
  time: number;
  page: ReadingView;
  track: HTMLElement;
  distance: number;
  origin: DOMMatrixReadOnly;
  axis?: 'X' | 'Y';
  canScrollUp: boolean;
  canScrollDown: boolean;
}

// A paragraph's box spans the paper even when its line contains only a word.
// Reserve mouse drags starting on the letters for native text selection.
function hitsText(target: Element, event: PointerEvent) {
  const range = document.createRange();
  for (const node of target.childNodes) {
    if (node.nodeType !== Node.TEXT_NODE) continue;
    range.selectNodeContents(node);
    for (const rect of range.getClientRects()) {
      if (event.clientX >= rect.left && event.clientX <= rect.right &&
          event.clientY >= rect.top && event.clientY <= rect.bottom) return true;
    }
  }
  return false;
}

function verticalDismissal(swipe: Swipe, dy: number) {
  return swipe.page === 'popup' && (dy > 0 ? !swipe.canScrollUp : !swipe.canScrollDown);
}

/** Swipe to dismiss a reading or turn an encyclopedia page. */
export class ReadingSwipe {
  private swipe?: Swipe;
  private dismissal?: { track: HTMLElement; animation: Animation };
  private suppressClick = false;
  private reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

  constructor(private root: HTMLElement, private page: () => ReadingView | undefined,
    private turn: (detail: boolean) => void, private close: () => void, signal?: AbortSignal) {
    document.addEventListener('pointerdown', event => {
      if (this.swipe && event.pointerId !== this.swipe.pointer) { this.cancel(); return; }
      if (event.isPrimary) this.suppressClick = false;
    }, {capture:true, signal});
    root.addEventListener('pointerdown', this.begin, {signal});
    // Keep the browser from cancelling the pointer for an outward swipe.
    // An inward drag on scrollable prose stays native, including momentum.
    root.addEventListener('touchmove', event => {
      const swipe = this.swipe;
      if (!swipe || swipe.page !== 'popup' || event.touches.length !== 1 || !event.cancelable) return;
      const finger = event.touches[0], dy = finger.clientY - swipe.y;
      if (swipe.axis || (Math.abs(dy) > Math.abs(finger.clientX - swipe.x) * 1.5 && verticalDismissal(swipe, dy))) event.preventDefault();
    }, {passive:false, signal});
    document.addEventListener('pointermove', this.move, {signal});
    document.addEventListener('pointerup', this.end, {signal});
    document.addEventListener('pointercancel', event => {
      if (event.pointerId === this.swipe?.pointer) this.cancel();
    }, {signal});
    root.addEventListener('lostpointercapture', event => {
      // A touched descendant loses its implicit capture when the reading claims it.
      // Only loss from our own capture is an interruption.
      if (event.target === root && event.pointerId === this.swipe?.pointer && event.buttons !== 0) this.cancel();
    }, {signal});
    // The release must not activate a link or the game revealed by dismissal.
    document.addEventListener('click', event => {
      if (!this.suppressClick || event.detail === 0) return;
      this.suppressClick = false;
      event.preventDefault(); event.stopPropagation();
    }, {capture:true, signal});
    root.addEventListener('click', event => {
      if (this.dismissal) { event.preventDefault(); event.stopPropagation(); }
    }, {capture:true, signal});
    // A native selection or callout takes precedence over an undecided swipe.
    root.addEventListener('selectstart', () => this.cancel(), {signal});
    root.addEventListener('contextmenu', () => this.cancel(), {signal});
    window.addEventListener('blur', () => this.cancel(), {signal});
    window.addEventListener('resize', () => this.cancel(), {signal});
    document.addEventListener('visibilitychange', () => { if (document.hidden) this.cancel(); }, {signal});
    this.reducedMotion.addEventListener('change', () => this.cancel(), {signal});
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
    const mouse = event.pointerType === 'mouse';
    if ((!mouse && event.pointerType !== 'touch') || !event.isPrimary || event.button !== 0 || this.swipe || this.dismissal) return;
    const page = this.page(), target = event.target instanceof Element ? event.target : undefined;
    if (!page || !target || target.closest('button, input, textarea, select, [contenteditable]')) return;
    if (page === 'popup' && target.closest('a[href], summary')) return;
    if (!mouse && this.hasSelection()) return;
    if (mouse && target.closest('.reading-text')) {
      if (page !== 'popup' || hitsText(target, event)) return;
      // Keep empty space between and beside lines from starting a selection.
      event.preventDefault();
    }
    const track = target.closest<HTMLElement>(page === 'popup' ? 'dialog' : '.encyclopedia-track');
    if (!track) return;
    const scale = previewScale(this.root);
    const distance = page === 'popup' ? layoutRect(track, scale).width
      : layoutRect(track.querySelector('.encyclopedia-detail')!, scale).left - layoutRect(track.querySelector('.encyclopedia-index')!, scale).left;
    const scroller = !mouse && page === 'popup' ? target.closest<HTMLElement>('.chapter-popup .reading-text') ?? track : undefined;
    this.swipe = {
      pointer: event.pointerId, x: event.clientX, y: event.clientY, time: event.timeStamp,
      page, track, distance,
      origin: new DOMMatrixReadOnly(getComputedStyle(track).transform),
      canScrollUp: !!scroller && scroller.scrollTop > 1,
      canScrollDown: !!scroller && scroller.scrollTop + scroller.clientHeight < scroller.scrollHeight - 1,
    };
  };

  private move = (event: PointerEvent) => {
    const swipe = this.swipe;
    if (!swipe || event.pointerId !== swipe.pointer) return;
    const touch = event.pointerType === 'touch';
    if (this.page() !== swipe.page || !swipe.track.isConnected || (touch && this.hasSelection())) { this.cancel(); return; }
    const scale = previewScale(this.root);
    const dx = (event.clientX - swipe.x) / scale, dy = (event.clientY - swipe.y) / scale;
    if (!swipe.axis) {
      // Leave long presses to native selection and lock one axis per drag.
      if (touch && event.timeStamp - swipe.time > 400) { this.cancel(); return; }
      if (Math.hypot(dx, dy) < 10) return;
      if (Math.abs(dx) >= Math.abs(dy) * 1.5) swipe.axis = 'X';
      else if (Math.abs(dy) >= Math.abs(dx) * 1.5 && verticalDismissal(swipe, dy)) swipe.axis = 'Y';
      else { this.cancel(); return; }
      if (!touch && this.hasSelection()) getSelection()?.removeAllRanges();
      this.suppressClick = true;
      this.root.setPointerCapture(swipe.pointer);
    }
    event.preventDefault();
    if (!this.reducedMotion.matches) {
      // An inward drag stops on the facing page. It cannot also dismiss the
      // book in the same gesture, even if it crosses that page's resting point.
      let position = swipe.axis === 'X' ? swipe.origin.m41 + dx : swipe.origin.m42 + dy;
      if (swipe.page === 'index') position = Math.max(-swipe.distance, position);
      if (swipe.page === 'detail') position = Math.min(0, position);
      swipe.track.style.transition = 'none';
      swipe.track.style.transform = `translate${swipe.axis}(${position}px)`;
    }
  };

  private end = (event: PointerEvent) => {
    if (event.pointerId !== this.swipe?.pointer) return;
    // Fast releases can carry travel that was never delivered in a move event.
    this.move(event);
    const swipe = this.swipe;
    if (!swipe) return;
    const travel = swipe.axis === 'Y' ? event.clientY - swipe.y : event.clientX - swipe.x;
    const commit = swipe.axis && Math.abs(travel) / previewScale(this.root) >= Math.min(80, swipe.distance * .22);
    // Resolve the last dragged position before restoring the CSS transition.
    // Reconciliation can then change pages without snapping to an intermediate end.
    if (swipe.axis) swipe.track.getBoundingClientRect();
    if (commit && (swipe.page === 'popup' || swipe.page === 'spread' || (travel > 0) === (swipe.page === 'index'))) {
      this.slideOut(swipe, travel > 0 ? 1 : -1);
      return;
    }
    this.cancel();
    if (commit) this.turn(swipe.page === 'index');
  };

  private slideOut(swipe: Swipe, direction: number) {
    const { track } = swipe;
    const from = getComputedStyle(track).transform;
    const scale = previewScale(this.root);
    const bounds = layoutRect(track, scale), viewport = layoutRect(this.root, scale);
    const matrix = new DOMMatrixReadOnly(from);
    const destination = swipe.axis === 'Y'
      ? matrix.m42 + (direction > 0 ? viewport.bottom - bounds.top : viewport.top - bounds.bottom)
      : matrix.m41 + (direction > 0 ? viewport.right - bounds.left : viewport.left - bounds.right);
    this.cancel();
    if (this.reducedMotion.matches) { this.close(); return; }
    // Keep the dialog's input barrier until the whole reading has left the pane.
    // Refresh/resize/Close can cancel this animation without a stale callback.
    track.style.transition = 'none';
    track.style.transform = from;
    const animation = track.animate([{ transform: from }, { transform: `translate${swipe.axis}(${destination}px)` }],
      { duration: 220, easing: 'ease-out', fill: 'forwards' });
    this.dismissal = { track, animation };
    void animation.finished.then(() => {
      if (this.dismissal?.animation !== animation) return;
      this.cancel();
      this.close();
    }, () => {});
  }
}
