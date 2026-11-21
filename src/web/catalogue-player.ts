import {cacheCarouselLaunch, carouselEntryState, readCarouselLaunch, type CarouselActivation} from './carousel-launch.ts';
import type {mountPlayer} from './main.ts';
import type {DraftStore} from './story-document.ts';
import {completesSwipe, SwipeMotion} from './swipe.ts';

type Player = ReturnType<typeof mountPlayer>;
type Modality = 'mouse' | 'touch';
interface Visit {
  link: HTMLAnchorElement;
  modality: Modality;
  activation?: CarouselActivation;
  workspace: HTMLElement;
  player?: Player;
  progress: number;
  frame: number;
  committed: boolean;
  settled: boolean;
  leaving: boolean;
  loading: number;
}

/** Keep both live surfaces in one viewport during the vertical transition. */
export function connectCataloguePlayer(cover: HTMLElement, links: HTMLAnchorElement[], restoreCover: (link?: HTMLAnchorElement) => void) {
  const home = new URL('index.html', location.href).href;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let visit: Visit | undefined;
  let module: Promise<typeof import('./main.ts')> | undefined;
  const drafts = new Map<string, DraftStore>();
  window.addEventListener('beforeunload', event => {
    if ([...drafts.values()].some(draft => draft.unsaved)) event.preventDefault();
  });

  function position(entry: Visit, progress: number) {
    entry.progress = progress;
    const y = reducedMotion.matches
      ? (entry.committed && !entry.leaving ? 1 : 0) : progress;
    cover.style.transform = `translateY(${-100 * y}%)`;
    entry.workspace.style.setProperty('--entry-board-offset', `${100 * (1 - y)}%`);
    if (!entry.leaving) {
      if (y >= .5) entry.player?.previewEntryReading();
      else entry.player?.hideEntryReadingPreview();
    }
  }

  function stop(entry: Visit) { cancelAnimationFrame(entry.frame); entry.frame = 0; }

  function clear(entry: Visit) {
    if (visit !== entry) return;
    stop(entry); visit = undefined;
    clearTimeout(entry.loading);
    entry.player?.dispose();
    entry.workspace.remove();
    cover.inert = false;
    cover.style.removeProperty('transform');
  }

  function animate(entry: Visit, to: number, done: () => void) {
    stop(entry);
    const from = entry.progress, start = performance.now();
    const duration = Math.max(100, 320 * Math.abs(to - from));
    const tick = (now: number) => {
      const t = reducedMotion.matches || document.hidden ? 1 : Math.min(1, (now - start) / duration);
      position(entry, from + (to - from) * (t * t * (3 - 2 * t)));
      if (t >= 1) { entry.frame = 0; done(); }
      else entry.frame = requestAnimationFrame(tick);
    };
    if (reducedMotion.matches || document.hidden || from === to) tick(start + duration);
    else entry.frame = requestAnimationFrame(tick);
  }

  function finish(entry: Visit) {
    entry.settled = true;
    entry.workspace.classList.add('entry-settled');
    entry.player?.finishEntry();
    entry.player?.focusEntry();
  }

  function open(link: HTMLAnchorElement, modality: Modality, activation?: CarouselActivation) {
    const workspace = document.createElement('main');
    workspace.id = 'workspace';
    workspace.className = 'catalogue-player';
    workspace.innerHTML = '<div id="app" aria-label="Game"><div class="game-surface"></div></div>';
    cover.after(workspace);
    const entry: Visit = {link, modality, activation, workspace, progress:0, frame:0, committed:false, settled:false, leaving:false, loading:0};
    visit = entry;
    workspace.inert = true;
    const status = document.createElement('div');
    status.className = 'story-entry-loading';
    status.setAttribute('role', 'status');
    status.innerHTML = '<span class="sr-only">Loading story…</span>';
    entry.loading = window.setTimeout(() => workspace.append(status), 240);
    permitReturnWhileMounting(entry);
    module ??= import('./main.ts');
    void module.then(({mountPlayer}) => {
      if (visit !== entry || entry.leaving) return;
      const player = entry.player = mountPlayer(workspace, {
        url:link.href, modality, activation, drafts,
        home: () => leave(entry),
        trackHome: (offset, settling) => {
          if (visit !== entry || entry.leaving) return;
          if (settling) animate(entry, 1, () => {});
          else { stop(entry); position(entry, 1 - offset / workspace.clientHeight); }
        },
      });
      player.setEntryOverlay(!entry.committed);
      if (entry.committed) player.commitEntry();
      if (entry.settled) player.finishEntry();
      void player.ready.then(() => {
        if (visit !== entry) return;
        clearTimeout(entry.loading); status.remove();
        position(entry, entry.progress);
        if (entry.committed && entry.progress >= .5) player.focusEntry();
      });
    }).catch(() => {
      module = undefined;
      if (visit !== entry) return;
      const committed = entry.committed;
      clear(entry);
      if (committed) location.reload();
    });
    return entry;
  }

  function permitReturnWhileMounting(entry: Visit) {
    let press: {id:number; x:number; y:number; progress:number; motion:SwipeMotion} | undefined;
    const surface = entry.workspace.querySelector<HTMLElement>('.game-surface')!;
    surface.addEventListener('pointerdown', event => {
      if (entry.player || !entry.committed || !event.isPrimary || event.button !== 0) return;
      stop(entry);
      press = {id:event.pointerId, x:event.clientX, y:event.clientY, progress:entry.progress, motion:new SwipeMotion(event)};
      surface.setPointerCapture(event.pointerId);
    });
    surface.addEventListener('pointermove', event => {
      if (press?.id !== event.pointerId) return;
      press.motion.track(event);
      position(entry, Math.max(0, press.progress - Math.max(0, (event.clientY - press.y) / surface.clientHeight)));
    });
    surface.addEventListener('pointerup', event => {
      if (press?.id !== event.pointerId) return;
      const down = event.clientY - press.y;
      const projected = press.motion.project(event, 'y');
      if (Math.abs(down) > Math.abs(event.clientX - press.x) && projected > 0 && completesSwipe(projected)) leave(entry);
      else animate(entry, 1, () => finish(entry));
      press = undefined;
    });
    surface.addEventListener('pointercancel', () => {
      if (!press) return;
      press = undefined;
      animate(entry, 1, () => finish(entry));
    });
  }

  function leave(entry: Visit) {
    if (visit !== entry || entry.leaving) return;
    entry.leaving = true;
    entry.workspace.inert = true;
    animate(entry, 0, () => {
      clear(entry);
      try { history.pushState(null, '', home); }
      catch { location.assign(home); return; }
      restoreCover(entry.link);
      entry.link.focus({preventScroll:true});
    });
  }

  function commit(entry: Visit, push: boolean) {
    const {link, modality, activation} = entry;
    const manuscript = new URL(link.dataset.story!, home).href;
    try {
      if (push) history.pushState(carouselEntryState(manuscript, link.href, modality, activation), '', link.href);
    } catch {
      clear(entry);
      cacheCarouselLaunch(manuscript, link.href, modality, activation);
      location.assign(link.href);
      return;
    }
    entry.committed = true;
    entry.workspace.inert = false; cover.inert = true;
    entry.player?.setEntryOverlay(false);
    entry.player?.commitEntry();
    if (entry.progress >= .5) entry.player?.focusEntry();
    if (push) animate(entry, 1, () => finish(entry));
    else { position(entry, 1); finish(entry); }
  }

  window.addEventListener('popstate', () => {
    if (visit) clear(visit);
    const link = links.find(candidate => candidate.href === location.href);
    const remembered = link && readCarouselLaunch(new URL(link.dataset.story!, home).href, new URL(home));
    if (link && remembered?.fromCarousel && remembered.modality) {
      restoreCover(link);
      commit(open(link, remembered.modality, remembered.activation), false);
    } else restoreCover();
  });

  return {
    get busy() { return !!visit?.committed; },
    track(link: HTMLAnchorElement, offset: number, modality: Modality, activation: CarouselActivation) {
      if (visit?.committed) return;
      if (!visit && offset <= 0) return;
      const entry = visit ?? open(link, modality, activation);
      stop(entry);
      position(entry, Math.max(0, Math.min(1, offset / cover.clientHeight)));
    },
    cancel() {
      const entry = visit;
      if (!entry || entry.committed) return;
      animate(entry, 0, () => clear(entry));
    },
    enter(link: HTMLAnchorElement, modality: Modality, activation: CarouselActivation = 'tap') {
      if (visit?.committed) return;
      if (visit && (visit.link !== link || visit.activation !== activation)) clear(visit);
      commit(visit ?? open(link, modality, activation), true);
    },
  };
}
