/** Shared by the catalogue and its player, including installations in subdirectories. */
const selectionKey = (page: URL) => `make-something-carousel-v1:${new URL('./', page).pathname}`;

export function selectedStory(page: URL): string | null {
  try { return localStorage.getItem(selectionKey(page)); }
  catch { return null; }
}

export function selectStory(page: URL, path: string | null) {
  try {
    if (path === null) localStorage.removeItem(selectionKey(page));
    else localStorage.setItem(selectionKey(page), path);
  } catch { /* The carousel still works without persistent storage. */ }
}

export function carouselStoryPath(catalogue: URL, manuscript: string): string | null {
  if (!manuscript) return null;
  const root = new URL('./', catalogue), story = new URL(manuscript);
  if (story.origin !== root.origin || !story.pathname.startsWith(root.pathname)) return null;
  try { return decodeURIComponent(story.pathname.slice(root.pathname.length)); }
  catch { return null; }
}
