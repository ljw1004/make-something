import { escape } from './markdown.ts';
import {observeStandalone, setHomeScreenIdentity} from './home-screen.ts';
import {viewportBoard} from './board-geometry.ts';
import {legacyProgressKey, storyProgressKey} from './progress-keys.ts';

const app = document.querySelector<HTMLDivElement>('#app')!;
const root = new URL('./', location.href);
setHomeScreenIdentity({
  name: 'Make Something', icon: new URL('icon.png', root).href,
  id: new URL('index.html', root).href, startURL: root.href, scope: root.href, themeColor: '#000000',
});
const carousel = app.querySelector<HTMLElement>('.story-carousel');
const frame = app.querySelector<HTMLElement>('.carousel-frame');
const slides = [...app.querySelectorAll<HTMLElement>('.carousel-slide')];
const storyLinks = [...app.querySelectorAll<HTMLAnchorElement>('a[data-story]')];
const originalLinks = storyLinks.map(link => link.getAttribute('href')!);
let standalone = false;
observeStandalone(value => { standalone = value; refreshLinks(); });

function storyLink(index: number, launch?: string) {
  const url = new URL(originalLinks[index], location.href);
  if (standalone) url.searchParams.set('home', 'show');
  if (launch) url.searchParams.set('launch', launch);
  return url;
}
function refreshLinks() {
  storyLinks.forEach((link, index) => {
    link.href = storyLink(index, 'mouse').href;
    const manuscript = new URL(link.dataset.story!, root).href;
    const legacy = legacyProgressKey(manuscript);
    let started = false;
    try { started = !!(localStorage.getItem(storyProgressKey(manuscript)) ?? (legacy ? localStorage.getItem(legacy) : null)); }
    catch { /* A blocked storage area should not block access to the stories. */ }
    link.querySelector('[data-launch-label]')!.textContent = started ? 'Continue' : 'Start';
  });
}
window.addEventListener('pageshow', refreshLinks);
window.addEventListener('storage', refreshLinks);

const bookmark = location.hash.slice(1);
if (bookmark) {
  // Legacy bookmarks still open the old direct-story route.
  const matches = storyLinks.filter(link => link.dataset.story!.split('/').at(-1)!.replace(/\.md$/i, '') === bookmark);
  const link = storyLinks.find(link => link.dataset.story === bookmark || link.dataset.story === `stories/${bookmark}`)
    ?? (matches.length === 1 ? matches[0] : undefined);
  if (link) location.replace(storyLink(storyLinks.indexOf(link)).href);
  else app.innerHTML = `<main class="chooser"><h1>Stories unavailable</h1><p>Unknown story: ${escape(bookmark)}.</p></main>`;
} else if (carousel && frame && slides.length) {
  const chooser = new URL(location.href);
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

  function show(index: number, remember = true) {
    clearTimeout(settling); settling = 0; incoming = undefined;
    current = wrap(index);
    slides.forEach((slide, position) => {
      slide.hidden = slide.inert = position !== current;
      slide.style.removeProperty('transform');
      slide.classList.remove('is-settling');
    });
    // Ask the browser for the immediate neighbors before the player swipes.
    for (const index of [wrap(current - 1), wrap(current + 1)]) {
      const art = slides[index].querySelector<HTMLImageElement>('.carousel-art');
      if (art) art.loading = 'eager';
    }
    measure();
    if (remember) {
      chooser.searchParams.set('slide', storyLinks[current].dataset.story!);
      history.replaceState(history.state, '', chooser);
    }
  }

  function translate(index: number, pixels: number) {
    slides[index].style.transform = `translateX(${pixels}px)`;
  }
  function track(delta: number) {
    const width = frame!.clientWidth;
    const direction = delta < 0 ? 1 : -1;
    const next = wrap(current + direction);
    if (!width || next === current) return;
    if (incoming !== next) {
      if (incoming !== undefined) slides[incoming].hidden = true;
      incoming = next;
      slides[next].hidden = false;
    }
    const offset = Math.max(-width, Math.min(width, delta));
    translate(current, offset);
    translate(next, offset + direction * width);
  }
  function settle(advance: boolean, delta: number) {
    if (incoming === undefined) return;
    const next = incoming, direction = delta < 0 ? 1 : -1;
    const destination = advance ? next : current;
    if (reducedMotion.matches) { show(destination, advance); return; }
    for (const index of [current, next]) slides[index].classList.add('is-settling');
    // Commit the finger-tracked position before applying the settle target.
    void frame!.offsetWidth;
    const travel = direction * frame!.clientWidth;
    translate(current, advance ? -travel : 0);
    translate(next, advance ? 0 : travel);
    settleDestination = destination;
    settling = window.setTimeout(() => show(destination, advance), 240);
  }

  const initial = storyLinks.findIndex(link => link.dataset.story === chooser.searchParams.get('slide'));
  show(Math.max(0, initial), false);
  slides.forEach(slide => slide.querySelector('img.carousel-art')?.addEventListener('load', measure));
  new ResizeObserver(measure).observe(app);
  slides.forEach(slide => {
    for (const [name, step] of [['prev', -1], ['next', 1]] as const) {
      const selector = `.carousel-${name}`;
      const button = slide.querySelector<HTMLButtonElement>(selector)!;
      button.addEventListener('click', () => {
        const focused = document.activeElement === button;
        show(current + step);
        if (focused) slides[current].querySelector<HTMLButtonElement>(selector)?.focus();
      });
    }
  });
  slides.forEach(slide => slide.querySelectorAll<HTMLButtonElement>('.carousel-dots button').forEach((dot, index) => {
    dot.addEventListener('click', () => {
      const focused = document.activeElement === dot;
      show(index);
      if (focused) slides[current].querySelector<HTMLButtonElement>('.carousel-dots [aria-current]')?.focus();
    });
  }));
  carousel.addEventListener('keydown', event => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    const previousFocus = document.activeElement;
    show(current + (event.key === 'ArrowLeft' ? -1 : 1));
    const replacement = previousFocus?.matches('.carousel-dots button') ? '.carousel-dots [aria-current]'
      : previousFocus?.matches('.carousel-prev') ? '.carousel-prev'
      : previousFocus?.matches('.carousel-next') ? '.carousel-next' : 'a[data-story]';
    slides[current].querySelector<HTMLElement>(replacement)?.focus();
  });
  let press: { id: number; x: number; y: number; control: Element | null; axis?: 'x' | 'y'; delta: number } | undefined;
  let cancelledClick: Element | null = null;
  carousel.addEventListener('pointerdown', event => {
    if (!event.isPrimary || event.button !== 0) return;
    if (settling) {
      // A fresh interaction can interrupt the tail of an animation.
      show(settleDestination, settleDestination !== current);
      if ((event.target as Element).closest('.carousel-slide[hidden]')) return;
    }
    cancelledClick = null;
    const link = (event.target as Element).closest<HTMLAnchorElement>('a[data-story]') ?? undefined;
    if (link) link.href = storyLink(storyLinks.indexOf(link), event.pointerType === 'touch' ? 'touch' : 'mouse').href;
    press = {id: event.pointerId, x: event.clientX, y: event.clientY, delta: 0, control: (event.target as Element).closest('button, a[data-story]')};
  });
  window.addEventListener('pointermove', event => {
    if (press?.id !== event.pointerId) return;
    const dx = event.clientX - press.x, dy = event.clientY - press.y;
    if (!press.axis) {
      if (Math.max(Math.abs(dx), Math.abs(dy)) < 8) return;
      press.axis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
    }
    if (press.axis === 'x') {
      press.delta = dx;
      track(dx);
    }
  });
  window.addEventListener('pointerup', event => {
    if (press?.id !== event.pointerId) return;
    const dx = event.clientX - press.x, dy = event.clientY - press.y;
    const advance = Math.abs(dx) >= 45 && (press.axis === 'x' || !press.axis && Math.abs(dx) > 1.35 * Math.abs(dy));
    if (press.axis === 'x' || advance) {
      cancelledClick = press.control;
      if (advance) track(dx);
      settle(advance, advance ? dx : press.delta);
    } else if (event.pointerType === 'touch' && Math.hypot(dx, dy) < 12 && press.control?.contains(event.target as Node)) {
      // Commit a touch tap on release, even when the browser withholds its
      // compatibility click immediately after a swipe. Do not double-activate.
      cancelledClick = press.control;
      if (press.control instanceof HTMLAnchorElement) location.assign(press.control.href);
      else if (press.control instanceof HTMLButtonElement) press.control.click();
    }
    press = undefined;
  });
  window.addEventListener('pointercancel', event => {
    if (press?.id !== event.pointerId) return;
    settle(false, press.delta);
    press = undefined;
  });
  carousel.addEventListener('click', event => {
    if (cancelledClick?.contains(event.target as Node) && event.detail > 0) { event.preventDefault(); event.stopPropagation(); cancelledClick = null; return; }
    const link = (event.target as Element).closest<HTMLAnchorElement>('a[data-story]');
    if (link && event.detail === 0) link.href = storyLink(current, 'mouse').href;
  }, true);
}
