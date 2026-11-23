import {browserDebugAvailable, debugGlyph, desktopDebug} from './debug-control.ts';
import {standaloneDisplay} from './home-screen.ts';
import {catalogueTutorialCount, resetCatalogueTutorials} from './tutorial-progress.ts';

export function mountCatalogueDebug(app: HTMLElement, frame: HTMLElement, catalogue: string, manuscripts: string[]) {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'debug-button catalogue-debug';
  button.title = 'Toggle carousel debug panel';
  button.setAttribute('aria-label', button.title);
  button.setAttribute('aria-controls', 'carousel-debug-panel');
  button.setAttribute('aria-expanded', 'false');
  button.innerHTML = debugGlyph;

  const panel = document.createElement('dialog');
  panel.id = 'carousel-debug-panel';
  panel.className = 'catalogue-debug-panel';
  panel.setAttribute('aria-labelledby', 'carousel-debug-title');
  panel.innerHTML = `<form method="dialog">
    <header><h2 id="carousel-debug-title">Carousel debug</h2><button aria-label="Close debug panel">×</button></header>
    <div class="tutorial-count-row"><span role="status"></span><button type="button" class="reset-tutorials">Reset</button></div>
    <p role="alert"></p>
    <footer><button autofocus>Close</button></footer>
  </form>`;
  const count = panel.querySelector<HTMLElement>('[role="status"]')!;
  const error = panel.querySelector<HTMLElement>('[role="alert"]')!;
  function refreshCount() {
    try {
      const {shown, total} = catalogueTutorialCount(manuscripts);
      count.textContent = `${shown}/${total} tutorials shown`;
    } catch {
      count.textContent = 'Tutorial count unavailable';
    }
  }
  panel.querySelector('.reset-tutorials')!.addEventListener('click', () => {
    try {
      resetCatalogueTutorials(catalogue, manuscripts);
      error.textContent = '';
    } catch {
      error.textContent = 'Could not finish resetting tutorials in browser storage.';
    }
    refreshCount();
  });
  function show() {
    // A dialog must be closed before switching between modal and nonmodal presentation.
    if (panel.open) panel.close();
    panel.setAttribute('closedby', desktopDebug.matches ? 'closerequest' : 'any');
    if (desktopDebug.matches) panel.show();
    else panel.showModal();
    button.setAttribute('aria-expanded', 'true');
  }
  button.addEventListener('click', () => {
    if (panel.open) { panel.close(); return; }
    app.append(panel);
    error.textContent = '';
    refreshCount();
    show();
  });
  panel.addEventListener('close', () => {
    if (panel.open) return;
    panel.remove();
    button.setAttribute('aria-expanded', 'false');
    if (!app.inert) button.focus({preventScroll:true});
  });
  desktopDebug.addEventListener('change', () => { if (panel.open) show(); });
  window.addEventListener('storage', () => { if (panel.open) refreshCount(); });
  function sync() {
    if (browserDebugAvailable()) frame.append(button);
    else {
      panel.close();
      button.remove();
    }
  }
  sync();
  standaloneDisplay.addEventListener('change', sync);
  return () => panel.close();
}
