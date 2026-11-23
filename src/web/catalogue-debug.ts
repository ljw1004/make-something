import {browserDebugAvailable, debugGlyph} from './debug-control.ts';
import {standaloneDisplay} from './home-screen.ts';
import {resetCatalogueTutorials} from './tutorial-progress.ts';

export function mountCatalogueDebug(app: HTMLElement, frame: HTMLElement, catalogue: string, manuscripts: string[]) {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'debug-button catalogue-debug';
  button.title = 'Open carousel debug panel';
  button.setAttribute('aria-label', button.title);
  button.setAttribute('aria-haspopup', 'dialog');
  button.innerHTML = debugGlyph;

  const dialog = document.createElement('dialog');
  dialog.setAttribute('aria-labelledby', 'carousel-debug-title');
  dialog.setAttribute('closedby', 'any');
  dialog.className = 'catalogue-debug-panel';
  dialog.innerHTML = `<form method="dialog">
    <header><h2 id="carousel-debug-title">Carousel debug</h2><button aria-label="Close debug panel">×</button></header>
    <button type="button" class="reset-tutorials">Reset tutorials</button>
    <p role="status"></p></form>`;
  const status = dialog.querySelector<HTMLElement>('[role="status"]')!;
  dialog.querySelector('.reset-tutorials')!.addEventListener('click', () => {
    try {
      resetCatalogueTutorials(catalogue, manuscripts);
      status.textContent = 'Tutorials reset for all stories in this carousel.';
    } catch {
      status.textContent = 'Could not finish resetting tutorials in browser storage.';
    }
  });
  button.addEventListener('click', () => {
    status.textContent = '';
    app.append(dialog);
    dialog.showModal();
  });
  dialog.addEventListener('close', () => {
    if (dialog.open) return;
    dialog.remove();
    button.focus({preventScroll:true});
  });
  function sync() {
    if (browserDebugAvailable()) frame.append(button);
    else {
      if (dialog.open) dialog.close();
      button.remove();
    }
  }
  sync();
  standaloneDisplay.addEventListener('change', sync);
}
