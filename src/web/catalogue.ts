import { escape } from './markdown.ts';
import {setHomeScreenIdentity} from './home-screen.ts';
import {watchCarouselContrast} from './carousel-contrast.ts';
import {plainNavigation, revealCatalogue, takeCatalogueSlide} from './document-navigation.ts';
import {connectCataloguePlayer} from './catalogue-player.ts';
import {viewportBoard} from './board-geometry.ts';
import {catalogueStoryStarted} from './chapter-recovery.ts';
import {legacyProgressKey, storyProgressKey} from './progress-keys.ts';
import {selectedStory, selectStory} from './carousel-selection.ts';
import {completesSwipe, SwipeMotion} from './swipe.ts';

const app = document.querySelector<HTMLDivElement>('#catalogue-app')!;
const root = new URL('./', location.href);
const catalogueIdentity = () => setHomeScreenIdentity({
  name: 'Make Something', icon: new URL('assets/homescreen.png', root).href,
  id: new URL('index.html', root).href, startURL: root.href, scope: root.href, themeColor: '#000000',
});
catalogueIdentity();
const carousel = app.querySelector<HTMLElement>('.story-carousel');
const frame = app.querySelector<HTMLElement>('.carousel-frame');
const slides = [...app.querySelectorAll<HTMLElement>('.carousel-slide')];
const storyLinks = [...app.querySelectorAll<HTMLAnchorElement>('a[data-story]')];
function refreshLinks() {
  storyLinks.forEach(link => {
    const manuscript = new URL(link.dataset.story!, root).href;
    const legacy = legacyProgressKey(manuscript);
    let started = false;
    try { started = catalogueStoryStarted(localStorage.getItem(storyProgressKey(manuscript)) ?? (legacy ? localStorage.getItem(legacy) : null)); }
    catch { /* A blocked storage area should not block access to the stories. */ }
    link.querySelector('[data-launch-label]')!.textContent = started ? 'Continue' : 'Start';
  });
}
refreshLinks();
window.addEventListener('pageshow', refreshLinks);
window.addEventListener('storage', refreshLinks);

const bookmark = location.hash.slice(1);
if (bookmark) {
  // Legacy bookmarks still open the old direct-story route.
  const matches = storyLinks.filter(link => link.dataset.story!.split('/').at(-1)!.replace(/\.md$/i, '') === bookmark);
  const link = storyLinks.find(link => link.dataset.story === bookmark || link.dataset.story === `stories/${bookmark}`)
    ?? (matches.length === 1 ? matches[0] : undefined);
  if (link) location.replace(link.href);
  else app.innerHTML = `<main class="chooser"><h1>Stories unavailable</h1><p>Unknown story: ${escape(bookmark)}.</p></main>`;
} else if (carousel && frame && slides.length) {
  const standalone = matchMedia('(display-mode: standalone)').matches;
  const native = location.protocol === 'msw:';
  if (import.meta.env.DEV || native || standalone) {
    frame.querySelectorAll<HTMLElement>('.carousel-footer').forEach(footer => { footer.hidden = false; });
    if (standalone && !native) {
      // Let the browser apply its out-of-scope navigation behavior.
      frame.querySelectorAll('.carousel-footer a').forEach(link => link.removeAttribute('target'));
    }
  }
  const contrast = watchCarouselContrast(frame);

  let current = 0;
  function measure() {
    const art = slides[current].querySelector<HTMLImageElement>('.carousel-art');
    const dimensions = art?.naturalWidth ? {width: art.naturalWidth, height: art.naturalHeight} : undefined;
    const geometry = viewportBoard(app.clientWidth, app.clientHeight, dimensions);
    frame!.style.width = `${geometry.width}px`;
    frame!.style.height = `${geometry.height}px`;
  }
  const wrap = (index: number) => (index + slides.length) % slides.length;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let incoming: number | undefined;
  let settling = 0;
  let settleDestination = 0;
  const repeatArrows = document.createElement('div');
  repeatArrows.className = 'carousel-repeat-arrows';
  repeatArrows.setAttribute('aria-hidden', 'true');
  repeatArrows.hidden = true;
  frame.append(repeatArrows);
  const pendingSteps: {step: number; focus?: string}[] = [];

  function show(index: number, remember = true) {
    clearTimeout(settling); settling = 0; incoming = undefined; repeatArrows.hidden = true;
    current = wrap(index);
    slides.forEach((slide, position) => {
      slide.hidden = slide.inert = position !== current;
      slide.style.removeProperty('transform');
      slide.classList.remove('is-settling', 'is-arrow-settling');
    });
    // Ask the browser for the immediate neighbors before the player swipes.
    for (const index of [wrap(current - 1), wrap(current + 1)]) {
      const art = slides[index].querySelector<HTMLImageElement>('.carousel-art');
      if (art) art.loading = 'eager';
    }
    measure();
    contrast.schedule();
    if (remember) selectStory(root, storyLinks[current].dataset.story!);
  }

  function translate(index: number, pixels: number) {
    slides[index].style.transform = `translateX(${pixels}px)`;
  }
  function track(delta: number, direction = delta < 0 ? 1 : -1) {
    const width = frame!.clientWidth;
    const next = wrap(current + direction);
    if (!width || next === current) return;
    if (incoming !== next) {
      if (incoming !== undefined) slides[incoming].hidden = true;
      incoming = next;
      slides[next].hidden = false;
      contrast.schedule();
    }
    const offset = Math.max(-width, Math.min(width, delta));
    translate(current, offset);
    translate(next, offset + direction * width);
  }
  function settle(advance: boolean, delta: number, after?: () => void, releaseOffset?: number) {
    const direction = delta < 0 ? 1 : -1;
    if (releaseOffset !== undefined) track(releaseOffset, direction);
    if (incoming === undefined) return;
    const next = incoming;
    const destination = advance ? next : current;
    if (reducedMotion.matches) { show(destination, advance); after?.(); return; }
    const travel = direction * frame!.clientWidth;
    const other = wrap(current - direction);
    const reversing = releaseOffset !== undefined && releaseOffset * delta < 0 && other !== next && other !== current;
    if (reversing) {
      // Keep the previously exposed card alongside the cover until it crosses center.
      slides[other].hidden = false;
      translate(other, Math.max(-Math.abs(travel), Math.min(Math.abs(travel), releaseOffset)) - travel);
      slides[other].classList.add('is-settling');
    }
    for (const index of [current, next]) slides[index].classList.add('is-settling', ...(after ? ['is-arrow-settling'] : []));
    // Commit the finger-tracked position before applying the settle target.
    void frame!.offsetWidth;
    translate(current, advance ? -travel : 0);
    translate(next, advance ? 0 : travel);
    if (reversing) translate(other, -2 * travel);
    settleDestination = destination;
    // Use the CSS duration so the end of the slide stays in sync when tuned.
    const duration = getComputedStyle(slides[current]).transitionDuration.split(',')[0].trim();
    const milliseconds = parseFloat(duration) * (duration.endsWith('ms') ? 1 : 1000);
    settling = window.setTimeout(() => { show(destination, advance); after?.(); }, milliseconds);
  }

  function advanceByArrow(step: number, focus?: string) {
    if (settling) { pendingSteps.push({step, focus}); return; }
    const width = frame!.clientWidth;
    const target = wrap(current + step);
    if (!width || target === current) return;
    if (!reducedMotion.matches) {
      // The arrows travel with their cards. Retain the resting hit areas
      // during the short transition so a quick second press is not lost.
      const origin = frame!.getBoundingClientRect();
      repeatArrows.replaceChildren();
      for (const [name, repeatStep] of [['prev', -1], ['next', 1]] as const) {
        const selector = `.carousel-${name}`;
        const source = slides[current].querySelector<HTMLButtonElement>(selector)!;
        const box = source.getBoundingClientRect();
        const repeat = document.createElement('button');
        repeat.type = 'button'; repeat.tabIndex = -1;
        Object.assign(repeat.style, {left:`${box.x - origin.x}px`,top:`${box.y - origin.y}px`,width:`${box.width}px`,height:`${box.height}px`});
        repeat.addEventListener('mousedown', event => event.preventDefault());
        repeat.addEventListener('click', () => advanceByArrow(repeatStep, document.activeElement === source ? selector : focus));
        repeatArrows.append(repeat);
      }
      repeatArrows.hidden = false;
    }
    const direction = -step;
    track(direction);
    // Start at zero displacement; track() used the sign to select the neighbor.
    translate(current, 0);
    translate(target, step * width);
    settle(true, direction, () => {
      if (focus) slides[current].querySelector<HTMLElement>(focus)?.focus({preventScroll: true});
      const next = pendingSteps.shift();
      if (next) advanceByArrow(next.step, next.focus);
    });
  }

  function restoreSlide() {
    pendingSteps.length = 0;
    const find = (path: string | null) => storyLinks.findIndex(link => link.dataset.story === path);
    const saved = find(selectedStory(root));
    // Old links can seed a fresh carousel without mutating their address.
    const legacy = saved < 0 ? find(new URL(location.href).searchParams.get('slide')) : -1;
    show(Math.max(0, saved, legacy), legacy >= 0);
  }
  const returning = takeCatalogueSlide();
  if (returning) frame.dataset.homeSlide = 'waiting';
  restoreSlide();
  const player = connectCataloguePlayer(app, storyLinks, link => {
    if (link) show(storyLinks.indexOf(link));
    else restoreSlide();
    refreshLinks(); catalogueIdentity();
  });
  if (returning) {
    const art = slides[current].querySelector<HTMLImageElement>('.carousel-art');
    if (art) art.loading = 'eager';
    // Bound the wait if the selected cover is still decoding.
    const reveal = () => {
      contrast.refresh();
      void revealCatalogue(frame).then(contrast.schedule);
    };
    const timeout = window.setTimeout(reveal, 750);
    void (art?.decode().catch(() => {}) ?? Promise.resolve()).then(() => {
      clearTimeout(timeout);
      // The timeout may already have started (or completed) this animation.
      if (frame.dataset.homeSlide === 'waiting') reveal();
    });
  }
  window.addEventListener('pageshow', event => { if (event.persisted) restoreSlide(); });
  slides.forEach(slide => slide.querySelector('img.carousel-art')?.addEventListener('load', measure));
  new ResizeObserver(measure).observe(app);
  slides.forEach(slide => {
    for (const [name, step] of [['prev', -1], ['next', 1]] as const) {
      const selector = `.carousel-${name}`;
      const button = slide.querySelector<HTMLButtonElement>(selector)!;
      button.addEventListener('click', () => {
        advanceByArrow(step, document.activeElement === button ? selector : undefined);
      });
    }
  });
  slides.forEach(slide => slide.querySelectorAll<HTMLButtonElement>('.carousel-dots button').forEach((dot, index) => {
    dot.addEventListener('click', () => {
      const focused = document.activeElement === dot;
      pendingSteps.length = 0;
      show(index);
      if (focused) slides[current].querySelector<HTMLButtonElement>('.carousel-dots [aria-current]')?.focus();
    });
  }));
  carousel.addEventListener('keydown', event => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    const previousFocus = document.activeElement;
    const replacement = previousFocus?.matches('.carousel-dots button') ? '.carousel-dots [aria-current]'
      : previousFocus?.matches('.carousel-prev') ? '.carousel-prev'
      : previousFocus?.matches('.carousel-next') ? '.carousel-next' : 'a[data-story]';
    advanceByArrow(event.key === 'ArrowLeft' ? -1 : 1, replacement);
  });
  let press: { id: number; x: number; y: number; motion: SwipeMotion; control: Element | null; axis?: 'x' | 'y'; repeat?: boolean; delta: number; canEnter: boolean } | undefined;
  let cancelledClick: Element | null = null;
  function swipeActivation(link: HTMLAnchorElement) {
    return link.querySelector('[data-launch-label]')?.textContent === 'Continue' ? 'swipe-continue' : 'swipe-start';
  }
  function scrollableDescription(target: Element) {
    const description = target.closest<HTMLElement>('.carousel-description');
    return !!description && description.scrollHeight > description.clientHeight;
  }
  function cancelPress() {
    if (!press) return;
    if (press.axis === 'x' && !press.repeat) settle(false, press.delta);
    else player.cancel();
    press = undefined;
  }
  carousel.addEventListener('pointerdown', event => {
    if (press && event.pointerId !== press.id) { cancelPress(); return; }
    if (!event.isPrimary || event.button !== 0 || player.busy) return;
    const target = event.target as Element;
    const repeatingArrow = target.closest('.carousel-repeat-arrows button');
    if (settling && !repeatingArrow) {
      pendingSteps.length = 0;
      // A fresh interaction can interrupt the tail of an animation.
      show(settleDestination, settleDestination !== current);
      if ((event.target as Element).closest('.carousel-slide[hidden]')) return;
    }
    cancelledClick = null;
    press = {id:event.pointerId, x:event.clientX, y:event.clientY, motion:new SwipeMotion(event), delta:0, repeat:!!repeatingArrow,
      control:target.closest('button, a[data-story], .carousel-footer a'),
      canEnter:!scrollableDescription(target)};
  });
  window.addEventListener('pointermove', event => {
    if (press?.id !== event.pointerId || press.repeat) return;
    press.motion.track(event);
    const dx = event.clientX - press.x, dy = event.clientY - press.y;
    if (!press.axis) {
      if (Math.max(Math.abs(dx), Math.abs(dy)) < 8) return;
      press.axis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
    }
    if (press.axis === 'x') {
      press.delta = dx;
      track(dx);
    } else if (press.canEnter) {
      press.delta = dy;
      const link = storyLinks[current];
      player.track(link, -dy, event.pointerType === 'mouse' ? 'mouse' : 'touch', swipeActivation(link));
    }
  });
  window.addEventListener('pointerup', event => {
    if (press?.id !== event.pointerId) return;
    const dx = event.clientX - press.x, dy = event.clientY - press.y;
    if (press.repeat) {
      cancelledClick = press.control;
      if (Math.hypot(dx, dy) < 12 && press.control instanceof HTMLButtonElement) press.control.click();
      press = undefined;
      return;
    }
    const axis = press.axis ?? (Math.abs(dx) > 1.35 * Math.abs(dy) ? 'x' : Math.abs(dy) > 1.35 * Math.abs(dx) ? 'y' : undefined);
    const projected = axis ? press.motion.project(event, axis) : 0;
    const advance = axis === 'x' && completesSwipe(projected);
    if (press.axis === 'x' || advance) {
      cancelledClick = press.control;
      settle(advance, advance ? projected : press.delta, undefined, advance ? dx : undefined);
    } else if (axis === 'y' && press.canEnter && projected < 0 && completesSwipe(projected)) {
      cancelledClick = press.control;
      const link = storyLinks[current];
      player.enter(link, event.pointerType === 'mouse' ? 'mouse' : 'touch', swipeActivation(link));
    } else if (press.axis === 'y' && press.canEnter) {
      cancelledClick = press.control;
      player.cancel();
    } else if (event.pointerType === 'touch' && Math.hypot(dx, dy) < 12 &&
      press.control?.matches('button, a[data-story]') && press.control.contains(event.target as Node)) {
      // Commit a touch tap on release, even when the browser withholds its
      // compatibility click immediately after a swipe. Do not double-activate.
      cancelledClick = press.control;
      if (press.control instanceof HTMLAnchorElement) {
        player.enter(press.control, 'touch');
      }
      else if (press.control instanceof HTMLButtonElement) press.control.click();
    }
    press = undefined;
  });
  window.addEventListener('pointercancel', event => {
    if (press?.id === event.pointerId) cancelPress();
  });
  window.addEventListener('blur', cancelPress);
  document.addEventListener('visibilitychange', () => { if (document.hidden) cancelPress(); });
  carousel.addEventListener('click', event => {
    if (cancelledClick?.contains(event.target as Node) && event.detail > 0) { event.preventDefault(); event.stopPropagation(); cancelledClick = null; return; }
    const link = (event.target as Element).closest<HTMLAnchorElement>('a[data-story]');
    if (link && plainNavigation(event, link)) {
      event.preventDefault();
      player.enter(link, event instanceof PointerEvent && event.pointerType === 'touch' ? 'touch' : 'mouse');
    }
  }, true);
}

// The correct card is now selected; its own waiting marker keeps it hidden.
document.documentElement.classList.remove('carousel-home-bootstrap');
