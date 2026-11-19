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
const dots = [...app.querySelectorAll<HTMLButtonElement>('.carousel-dots button')];
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
  function show(index: number, remember = true) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, position) => { slide.hidden = position !== current; });
    dots.forEach((dot, position) => {
      if (position === current) dot.setAttribute('aria-current', 'true');
      else dot.removeAttribute('aria-current');
    });
    measure();
    if (remember) {
      chooser.searchParams.set('slide', storyLinks[current].dataset.story!);
      history.replaceState(history.state, '', chooser);
    }
  }
  const initial = storyLinks.findIndex(link => link.dataset.story === chooser.searchParams.get('slide'));
  show(Math.max(0, initial), false);
  slides.forEach(slide => slide.querySelector('img.carousel-art')?.addEventListener('load', measure));
  new ResizeObserver(measure).observe(app);
  carousel.querySelector('.carousel-prev')?.addEventListener('click', () => show(current - 1));
  carousel.querySelector('.carousel-next')?.addEventListener('click', () => show(current + 1));
  dots.forEach((dot, index) => dot.addEventListener('click', () => show(index)));
  carousel.addEventListener('keydown', event => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    const oldLink = storyLinks[current];
    show(current + (event.key === 'ArrowLeft' ? -1 : 1));
    if (document.activeElement === oldLink || !carousel.contains(document.activeElement)) storyLinks[current].focus();
  });
  let press: { id: number; x: number; y: number; control: Element | null } | undefined;
  let cancelledClick: Element | null = null;
  carousel.addEventListener('pointerdown', event => {
    if (!event.isPrimary || event.button !== 0) return;
    cancelledClick = null;
    const link = (event.target as Element).closest<HTMLAnchorElement>('a[data-story]') ?? undefined;
    if (link) link.href = storyLink(current, event.pointerType === 'touch' ? 'touch' : 'mouse').href;
    press = {id: event.pointerId, x: event.clientX, y: event.clientY, control: (event.target as Element).closest('button, a[data-story]')};
  });
  window.addEventListener('pointerup', event => {
    if (press?.id !== event.pointerId) return;
    const dx = event.clientX - press.x, dy = event.clientY - press.y;
    if (Math.abs(dx) >= 45 && Math.abs(dx) > 1.35 * Math.abs(dy)) {
      cancelledClick = press.control;
      show(current + (dx < 0 ? 1 : -1));
    } else if (event.pointerType === 'touch' && Math.hypot(dx, dy) < 12 && press.control?.contains(event.target as Node)) {
      // Commit a touch tap on release, even when the browser withholds its
      // compatibility click immediately after a swipe. Do not double-activate.
      cancelledClick = press.control;
      if (press.control instanceof HTMLAnchorElement) location.assign(press.control.href);
      else if (press.control instanceof HTMLButtonElement) press.control.click();
    }
    press = undefined;
  });
  window.addEventListener('pointercancel', event => { if (press?.id === event.pointerId) press = undefined; });
  carousel.addEventListener('click', event => {
    if (cancelledClick?.contains(event.target as Node) && event.detail > 0) { event.preventDefault(); event.stopPropagation(); cancelledClick = null; return; }
    const link = (event.target as Element).closest<HTMLAnchorElement>('a[data-story]');
    if (link && event.detail === 0) link.href = storyLink(current, 'mouse').href;
  }, true);
}
