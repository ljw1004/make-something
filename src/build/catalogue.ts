import { posix } from 'node:path';
import { escape, markdown, markdownInline } from '../web/markdown.ts';
import { resolveStoryAsset } from '../web/story-document.ts';

export interface CatalogueEntry { path: string; title: string; heading?: string; description: string }

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

export function renderCatalogue(entries: CatalogueEntry[]): string {
  return `<main class="chooser"><h1>Make Something Worthwhile</h1><nav>${entries.map(entry => {
    const href = `make-something.html?story=${encodeURIComponent(entry.path).replaceAll('%2F', '/')}`;
    const heading = markdownInline(entry.heading ?? entry.title, catalogueAsset(entry.path));
    return `<a href="${escape(href)}" data-story="${escape(entry.path)}"><h2 class="story-title">${heading}</h2>${catalogueDescription(entry.description, entry.path)}</a>`;
  }).join('')}</nav></main>`;
}

/** Text terminals use the same story inventory, with plain titles and no artwork. */
export function renderTerminalCatalogue(entries:CatalogueEntry[], style:'fast'|'detailed'):string {
  return `<nav aria-label="Stories"><ul>${entries.map(entry => {
    const href=`text-${style}.html?story=${encodeURIComponent(entry.path).replaceAll('%2F','/')}`;
    return `<li><a href="${escape(href)}">${escape(entry.title)}</a></li>`;
  }).join('')}</ul></nav>`;
}
