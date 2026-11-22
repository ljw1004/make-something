import {existsSync} from 'node:fs';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {resolveRelativeFile} from '../story/relative-file.ts';
import type {Diagnostic, Story} from '../story/types.ts';
import {sourceMap} from '../story/source-map.ts';

export function artworkFile(manuscript: string, reference: string): string {
  return fileURLToPath(resolveRelativeFile(reference, pathToFileURL(manuscript)));
}

/** Filesystem checks belong to CLI lint; browser diagnostics never fetch artwork. */
export function lintStoryImages(story: Story, markdown: string): Diagnostic[] {
  const items = Object.values(story.items);
  const prose = [story.description, ...story.chapters.flatMap(chapter => [chapter.intro, chapter.skipped]), ...items.flatMap(item => item.wonders.flatMap(wonder => [wonder.popup, wonder.encyclopedia]))];
  const images = new Set([
    ...(story.titleImages ?? []).map(image => image.url),
    ...(story.cover ? [story.cover] : []),
    ...(story.dialogs ? [story.dialogs] : []),
    ...story.chapters.flatMap(chapter => chapter.image ? [chapter.image] : []),
    ...prose.flatMap(text => [...text.matchAll(/!\[[^\]]*\]\(([^)]+)\)/g)].map(match => match[1])),
    ...items.flatMap(item => [item.icon, ...item.presentations.map(change => change.icon), ...item.slots.map(slot => slot.icon)].flatMap(icon => icon ? [icon.url] : [])),
    ...story.chapters.flatMap(chapter => Object.values(chapter.hotspotDefinitions ?? {})).flatMap(hotspot =>
      [hotspot.icon, ...(hotspot.iconChanges ?? []).map(change => change.icon)].flatMap(icon => icon ? [icon.url] : [])),
  ]);
  const locations = sourceMap(markdown, story.source.file), diagnostics: Diagnostic[] = [];
  for (const match of markdown.matchAll(/!\[[^\]]*\]\(([^)]+)\)/g)) {
    const image = match[1].trim();
    if (!images.has(image)) continue;
    let message: string;
    try {
      if (existsSync(artworkFile(story.source.file, image))) continue;
      message = `Image not found: ${image}`;
    } catch {
      message = `Invalid artwork path: ${image}. Use a relative file path without a leading slash or consecutive dots.`;
    }
    const from = match.index! + match[0].indexOf('](') + 2 + match[1].length - match[1].trimStart().length;
    const source = locations.range(from, from + image.length);
    diagnostics.push({severity: 'error', code: 'missing-image', message, source, span: source.span!, stage: 'fast'});
  }
  return diagnostics;
}
