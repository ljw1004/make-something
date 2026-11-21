import { posix } from 'node:path';
import { escape, markdown } from '../web/markdown.ts';
import { resolveStoryAsset } from '../web/story-document.ts';

export interface CatalogueEntry { path: string; title: string; description: string; cover?: string }

/** Catalogue prose still belongs to its manuscript, not the catalogue directory. */
function catalogueAsset(storyPath: string): (reference: string) => string {
  const storyURL = new URL(storyPath, 'https://catalogue.invalid/site/index.html').href;
  return reference => {
    try {
      const resolved = new URL(resolveStoryAsset(reference, storyURL));
      if (/^[a-z][a-z\d+.-]*:/i.test(reference) || resolved.origin !== 'https://catalogue.invalid') return resolved.href;
      if (reference.startsWith('/')) return reference;
      // Keep generated HTML portable beneath any hosting prefix.
      return posix.relative('/site/', resolved.pathname) + resolved.search + resolved.hash;
    }
    catch { return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg"/%3E'; }
  };
}

export function catalogueDescription(description: string, storyPath: string): string {
  return markdown(description, catalogueAsset(storyPath));
}

const carouselOrder = [
  'stories/cookbook/cookbook.md',
  'stories/settlement/settlement.md',
  'stories/creation/creation.md',
  'stories/mars/mars.md',
  'stories/theology/theology.md',
  'stories/ideas/ideas.md',
];

export function renderCatalogue(entries: CatalogueEntry[]): string {
  if (!entries.length) return '<main class="chooser"><h1>Make Something Worthwhile</h1><p>No stories are available.</p></main>';
  const rank = (path: string) => {
    const index = carouselOrder.indexOf(path);
    return index < 0 ? carouselOrder.length : index;
  };
  // The stable sort preserves manuscript discovery order for unlisted stories.
  const orderedEntries = entries.toSorted((a, b) => rank(a.path) - rank(b.path));
  const arrow = (left: boolean) => `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="${left ? 'm15 4-8 8 8 8' : 'm9 4 8 8-8 8'}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  const enter = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="none" stroke="currentColor"/><path d="M12 6v11m-5-5 5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>';
  return `<main class="story-carousel" aria-label="Make Something Worthwhile stories"><h1 class="sr-only">Make Something Worthwhile</h1><div class="carousel-frame">
    ${orderedEntries.map((entry, index) => {
      const href = `make-something.html?story=${encodeURIComponent(entry.path).replaceAll('%2F', '/')}`;
      const cover = entry.cover ? catalogueAsset(entry.path)(entry.cover) : '';
      return `<section class="carousel-slide"${index ? ' hidden' : ''} aria-label="${escape(entry.title)}">
        ${cover ? `<img class="carousel-art" ${index ? 'loading="lazy"' : 'fetchpriority="high"'} src="${escape(cover)}" alt="" draggable="false">` : ''}
        <nav class="carousel-dots" aria-label="Choose a story">${orderedEntries.map((destination, dot) => `<button type="button" aria-label="${escape(destination.title)}" ${dot === index ? 'aria-current="true"' : ''}></button>`).join('')}</nav>
        <div class="carousel-panel">
          <div class="carousel-bar"><a href="${escape(href)}" data-story="${escape(entry.path)}"><h2 class="story-title">${escape(entry.title)}</h2><span class="carousel-action"><span data-launch-label>Start</span>${enter}</span></a>
            <button type="button" class="carousel-arrow carousel-prev" aria-label="Previous story">${arrow(true)}</button>
            <button type="button" class="carousel-arrow carousel-next" aria-label="Next story">${arrow(false)}</button>
          </div>
          <div class="carousel-description-frame"><div class="carousel-description">${catalogueDescription(entry.description, entry.path)}</div></div>
        </div>
        <nav class="carousel-footer" aria-label="App information" hidden>
          <a href="https://unto.me/make-something/support.html" target="_blank" rel="noopener noreferrer"><span>Support</span></a>
          <a href="https://unto.me/make-something/privacy.html" target="_blank" rel="noopener noreferrer"><span>Privacy</span></a>
        </nav>
      </section>`;
    }).join('')}</div></main>`;

}

/** Numbered terminal choices share the catalogue's manuscripts and authored prose. */
export function renderTerminalCatalogue(entries:CatalogueEntry[]):string {
  return entries.map((entry,index) => {
    const prose=entry.description.replace(/!\[[^\]]*\]\([^)]+\)/g,'').replace(/\s+/g,' ').trim();
    const title=escape(entry.title.toUpperCase().replace(/\.$/,''));
    return `<span data-story="${escape(entry.path)}">${index+1}. <span class="terminal-story-title">${title}</span>.${prose ? ` ${escape(prose)}` : ''}</span>`;
  }).join('\n\n');
}
