type Modality = 'mouse' | 'touch';
interface CarouselLaunch { entry: 'carousel'; source?: string; manuscript: string; destination: string; modality: Modality }
const stateKey = 'makeSomethingCarouselEntry';
const pendingKey = 'make-something-entry-v1';

const valid = (value: unknown, manuscript: string, destination: string): value is CarouselLaunch => {
  const candidate = value as Partial<CarouselLaunch> | undefined;
  return candidate?.entry === 'carousel' && candidate.manuscript === manuscript && candidate.destination === destination &&
    (candidate.modality === 'mouse' || candidate.modality === 'touch');
};

/** Transfer click-only context within this tab without adding it to the story URL. */
export function cacheCarouselLaunch(manuscript: string, destination: string, modality: Modality) {
  const launch: CarouselLaunch = {entry:'carousel', source:location.href, manuscript, destination, modality};
  try { sessionStorage.setItem(pendingKey, JSON.stringify({launch, expires:Date.now() + 30_000})); }
  catch { /* The real link still opens the normal story route. */ }
}

export function readCarouselLaunch(manuscript: string, catalogue: URL) {
  const destination = location.href;
  let pending: {launch?: unknown; expires?: number} | null = null;
  try {
    const stored = sessionStorage.getItem(pendingKey);
    // Consume mismatches too so an abandoned click cannot affect a later visit.
    if (stored !== null) {
      sessionStorage.removeItem(pendingKey);
      pending = JSON.parse(stored);
    }
  } catch { /* Storage may be unavailable or damaged. */ }

  const remembered = history.state?.[stateKey];
  if (valid(remembered, manuscript, destination)) return {fromCarousel:true, modality:remembered.modality};
  if (!pending || !Number.isFinite(pending.expires) || pending.expires! < Date.now() ||
    !valid(pending.launch, manuscript, destination)) return {fromCarousel:false};
  // WebKit omits the HTTP referrer on app-scheme navigation. The in-tab
  // launch record already identifies the catalogue that initiated this click.
  const source = document.referrer || (catalogue.protocol === 'msw:' ? pending.launch.source : '');
  if (!source) return {fromCarousel:false};
  let referrer: URL;
  try { referrer = new URL(source); } catch { return {fromCarousel:false}; }
  const root = new URL('./', catalogue);
  if (referrer.protocol !== root.protocol || referrer.host !== root.host || ![root.pathname, catalogue.pathname, new URL('index-dev.html', root).pathname].includes(referrer.pathname)) return {fromCarousel:false};

  try { history.replaceState({...history.state, [stateKey]:pending.launch}, ''); }
  catch { /* Preserve context for the current page even if history is unavailable. */ }
  return {fromCarousel:true, modality:pending.launch.modality, skipCover:true};
}
