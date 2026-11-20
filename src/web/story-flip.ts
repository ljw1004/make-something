type Journey = 'launch' | 'home';
const key = 'make-something-flip-v1';
const half = 160;
const spinnerDelay = 240;
const edge = (angle: number) => `perspective(1400px) rotateY(${angle}deg)`;
const supportsFlip = () => !matchMedia('(prefers-reduced-motion: reduce)').matches &&
  typeof HTMLElement.prototype.animate === 'function' && !!globalThis.CSS?.supports('transform', edge(45));
const clean = (address: string) => { const url = new URL(address); url.hash = ''; return url.href; };
let leaving = false;

function mark(face: HTMLElement, phase?: 'waiting' | 'leaving' | 'arriving') {
  if (phase) face.dataset.storyFlip = phase;
  else delete face.dataset.storyFlip;
  document.documentElement.classList.toggle('story-flip-active', !!phase);
}

function loadingSpinner(at: number) {
  const spinner = document.createElement('div');
  spinner.className = 'story-flip-loading';
  spinner.setAttribute('role', 'status');
  const label = document.createElement('span');
  label.className = 'sr-only';
  label.textContent = 'Loading story…';
  spinner.append(label);
  const timer = window.setTimeout(() => document.body.append(spinner), Math.max(0, at - Date.now()));
  return () => { clearTimeout(timer); spinner.remove(); };
}

/** Advisory only; never issues a separate fetch of the fresh Markdown. */
export function warmStoryNavigation(href: string) {
  const url = new URL(href);
  if (url.origin !== location.origin) return;
  const hint = document.createElement('link');
  if (!hint.relList?.supports?.('prefetch')) return;
  hint.rel = 'prefetch'; hint.href = url.href;
  hint.setAttribute('fetchpriority', 'low');
  document.head.append(hint);
}

export function plainNavigation(event: MouseEvent, link: HTMLAnchorElement) {
  return !event.defaultPrevented && event.button === 0 && !event.altKey && !event.ctrlKey &&
    !event.metaKey && !event.shiftKey && (!link.target || link.target === '_self') && !link.hasAttribute('download');
}

function play(face: HTMLElement, phase: 'leave' | 'arrive', journey: Journey) {
  const angle = journey === 'launch' ? -90 : 90;
  const transforms = phase === 'leave' ? [edge(0), edge(angle)] : [edge(-angle), edge(0)];
  return face.animate(transforms.map(transform => ({transform, transformOrigin:'50% 50%'})),
    {duration:half, easing:phase === 'leave' ? 'ease-in' : 'ease-out', fill:'both'});
}

/** True means the caller should prevent the ordinary link navigation. */
export function leaveWithFlip(face: HTMLElement, href: string, journey: Journey) {
  if (leaving) return true;
  if (!supportsFlip()) return false;
  try {
    sessionStorage.setItem(key, JSON.stringify({journey, source:clean(location.href), destination:clean(href), spinnerAt:Date.now()+half+spinnerDelay, expires:Date.now()+15_000}));
  } catch { return false; }
  leaving = true;
  const previousFocus = document.activeElement;
  const wasInert = face.inert;
  face.inert = true;
  mark(face, 'leaving');
  let animation: Animation;
  try { animation = play(face, 'leave', journey); }
  catch {
    leaving = false;
    face.inert = wasInert; mark(face);
    try { sessionStorage.removeItem(key); } catch { /* Storage may be unavailable. */ }
    return false;
  }
  let navigating = false;
  let removeSpinner: (() => void) | undefined;
  const navigate = () => {
    if (navigating) return;
    navigating = true;
    clearTimeout(timeout);
    if (journey === 'launch') removeSpinner = loadingSpinner(Date.now()+spinnerDelay);
    location.assign(href);
  };
  const timeout = window.setTimeout(navigate, half + 100);
  void animation.finished.then(navigate, navigate);
  window.addEventListener('pagehide', () => removeSpinner?.(), {once:true});
  window.addEventListener('pageshow', event => {
    if (!event.persisted) return;
    leaving = false;
    animation.cancel();
    face.inert = wasInert;
    mark(face);
    if (previousFocus instanceof HTMLElement && previousFocus.isConnected) previousFocus.focus({preventScroll:true});
  }, {once:true});
  return true;
}

/** A marker is consumed once; Back, reload and direct links never replay it. */
export function takeFlip(journey: Journey): {spinnerAt?: number} | undefined {
  try {
    const raw = sessionStorage.getItem(key);
    if (!raw) return;
    sessionStorage.removeItem(key);
    const marker = JSON.parse(raw);
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming | undefined;
    if (supportsFlip() && navigation?.type !== 'reload' && navigation?.type !== 'back_forward' &&
      marker?.journey === journey && marker.destination === clean(location.href) &&
      marker.expires > Date.now() && (document.referrer ? marker.source === clean(document.referrer) : location.protocol === 'msw:'))
      return {spinnerAt:typeof marker.spinnerAt === 'number' ? marker.spinnerAt : undefined};
  } catch { /* Private storage or a bad marker must not block navigation. */ }
}

/** Wait on black until the caller is ready to reveal the incoming face. */
export function holdFlip(face: HTMLElement, journey: Journey = 'home', at = Date.now()+spinnerDelay) {
  mark(face, 'waiting');
  const removeSpinner = journey === 'launch' ? loadingSpinner(at) : undefined;
  const release = () => { removeSpinner?.(); mark(face); };
  return {
    release,
    async reveal(animate = true, overlay?: {board: HTMLElement; onStart(finish: () => void): void}) {
      if (face.dataset.storyFlip !== 'waiting' || !animate || !supportsFlip()) { release(); return; }
      release();
      const wasInert = face.inert;
      if (!overlay) face.inert = true;
      mark(face, 'arriving');
      let animation: Animation | undefined, finished = false;
      const finish = () => {
        if (finished) return;
        finished = true;
        animation?.cancel();
        if (!overlay) face.inert = wasInert;
        mark(face);
      };
      try { animation = play(overlay?.board ?? face, 'arrive', journey); }
      catch { finish(); return; }
      try {
        overlay?.onStart(finish);
        await animation.finished.catch(() => {});
      } finally { finish(); }
    },
  };
}
