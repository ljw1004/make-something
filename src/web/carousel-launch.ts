type Modality = 'mouse' | 'touch';
export type CarouselActivation = 'tap' | 'swipe-start' | 'swipe-continue';
interface CarouselEntryContext {
  fromCarousel: boolean; modality?: Modality; resumeEntry?: boolean; skipCover?: boolean; activation?: CarouselActivation;
}
interface CarouselLaunch {
  entry: 'carousel'; source?: string; manuscript: string; destination: string; modality: Modality;
  inPage?: boolean; activation?: CarouselActivation; skipIntroduction?: boolean;
}
const stateKey = 'makeSomethingCarouselEntry';
const pendingKey = 'make-something-entry-v1';

const valid = (value: unknown, manuscript: string, destination: string): value is CarouselLaunch => {
  const candidate = value as Partial<CarouselLaunch> | undefined;
  return candidate?.entry === 'carousel' && candidate.manuscript === manuscript && candidate.destination === destination &&
    (candidate.modality === 'mouse' || candidate.modality === 'touch');
};

/** Preserve the carousel origin on reload, even if the first load was interrupted. */
export function carouselEntryState(manuscript: string, destination: string, modality: Modality, activation?: CarouselActivation) {
  const launch: CarouselLaunch = {entry:'carousel', source:location.href, manuscript, destination, modality, inPage:true, activation};
  return {[stateKey]:launch};
}

/** Transfer context for a full navigation when same-document history is unavailable. */
export function cacheCarouselLaunch(manuscript: string, destination: string, modality: Modality, activation?: CarouselActivation) {
  const launch: CarouselLaunch = {entry:'carousel', source:location.href, manuscript, destination, modality, activation};
  try { sessionStorage.setItem(pendingKey, JSON.stringify({launch, expires:Date.now() + 30_000})); }
  catch { /* The real link still opens the normal story route. */ }
}

export function finishCarouselLaunch() {
  const launch = history.state?.[stateKey];
  if (!launch?.activation && launch?.skipIntroduction !== true) return;
  try { history.replaceState({...history.state, [stateKey]:{...launch, activation:undefined, skipIntroduction:false}}, ''); }
  catch { /* The story can still retain its ordinary progress. */ }
}

function launchActivation(launch: CarouselLaunch): CarouselActivation | undefined {
  const {activation} = launch;
  if (activation === 'tap' || activation === 'swipe-start' || activation === 'swipe-continue') return activation;
  if (launch.skipIntroduction === true) return 'swipe-continue';
}

export function readCarouselLaunch(manuscript: string, catalogue: URL): CarouselEntryContext {
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
  if (valid(remembered, manuscript, destination)) {
    const activation = remembered.inPage ? launchActivation(remembered) : undefined;
    return {fromCarousel:true, modality:remembered.modality, resumeEntry:remembered.inPage, skipCover:!!activation, activation};
  }
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

  try { history.replaceState({...history.state, [stateKey]:{...pending.launch, inPage:true}}, ''); }
  catch { /* Preserve context for the current page even if history is unavailable. */ }
  return {fromCarousel:true, modality:pending.launch.modality, skipCover:true, activation:launchActivation(pending.launch) ?? 'swipe-start'};
}
