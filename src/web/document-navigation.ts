const key = 'make-something-home-slide-v1';
const duration = 160;
const supportsMotion = () => !matchMedia('(prefers-reduced-motion: reduce)').matches &&
  typeof HTMLElement.prototype.animate === 'function';
const clean = (address: string) => { const url = new URL(address); url.hash = ''; return url.href; };

export function plainNavigation(event: MouseEvent, link: HTMLAnchorElement) {
  return !event.defaultPrevented && event.button === 0 && !event.altKey && !event.ctrlKey &&
    !event.metaKey && !event.shiftKey && (!link.target || link.target === '_self') && !link.hasAttribute('download');
}

/** Carry the visible layout across a full-document Home navigation, with or without motion. */
export function rememberCatalogueReturn(href: string, sidebarOpen: boolean) {
  try {
    sessionStorage.setItem(key, JSON.stringify({source:clean(location.href), destination:clean(href), expires:Date.now()+15_000, sidebarOpen}));
  } catch { /* Home navigation also works without session storage. */ }
}

/** A story loaded as its own document has no live cover underneath it. */
export function leaveForCatalogue(face: HTMLElement, board: HTMLElement, href: string, offset: number, sidebarOpen: boolean) {
  rememberCatalogueReturn(href, sidebarOpen);
  if (!supportsMotion()) return false;
  let animation: Animation;
  try {
    animation = face.animate([{transform:`translateY(${offset}px)`}, {transform:'translateY(100dvh)'}],
      {duration, easing:'ease-in', fill:'both'});
  } catch {
    return false;
  }
  board.style.removeProperty('transform');
  face.inert = true;
  document.documentElement.classList.add('catalogue-document-slide');
  let navigated = false;
  const navigate = () => {
    if (navigated) return;
    navigated = true;
    clearTimeout(timeout);
    location.assign(href);
  };
  const timeout = window.setTimeout(navigate, duration + 100);
  void animation.finished.then(navigate, navigate);
  window.addEventListener('pageshow', event => {
    if (!event.persisted) return;
    animation.cancel(); face.inert = false;
    document.documentElement.classList.remove('catalogue-document-slide');
  }, {once:true});
  return true;
}

/** Consume the marker once; Back, reload and direct links restore without motion. */
export function takeCatalogueReturn() {
  try {
    const raw = sessionStorage.getItem(key);
    if (!raw) return;
    sessionStorage.removeItem(key);
    const marker = JSON.parse(raw);
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming | undefined;
    if (navigation?.type === 'reload' || navigation?.type === 'back_forward' ||
        marker?.destination !== clean(location.href) || !(marker.expires > Date.now()) ||
        (document.referrer ? marker.source !== clean(document.referrer) : location.protocol !== 'msw:')) return;
    return {animate: supportsMotion(), sidebarOpen: marker.sidebarOpen === true};
  } catch { return; }
}

export async function revealCatalogue(face: HTMLElement) {
  if (face.dataset.homeSlide !== 'waiting') return;
  delete face.dataset.homeSlide;
  face.inert = true;
  let animation: Animation | undefined;
  try {
    if (!supportsMotion()) return;
    animation = face.animate([{transform:'translateY(-100dvh)'}, {transform:'translateY(0)'}],
      {duration, easing:'ease-out'});
    await animation.finished;
  } catch { /* Restore the settled cover if animation is interrupted. */ }
  finally { face.inert = false; }
}
