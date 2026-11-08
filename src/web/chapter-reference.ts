import type {Chapter} from '../story/types.ts';
import type {BoardRect} from './board-geometry.ts';
import {escape} from './markdown.ts';

/** The right-hand third of the instruction row, near the top of the visible board. */
export function chapterReferenceRect(bounds: BoardRect): BoardRect {
  const width = Math.min(130, Math.max(44, bounds.width / 3));
  return {x: bounds.x + bounds.width - width - 6, y: bounds.y + 36, width, height: 112};
}

export function chapterTitleRect(bounds: BoardRect): BoardRect {
  return {x: bounds.x + 8, y: bounds.y + 4, width: Math.max(0, bounds.width - 52), height: 26};
}

export function chapterTitleHTML(chapter: Chapter, bounds: BoardRect): string {
  const {x, y, width, height} = chapterTitleRect(bounds);
  return `<h2 class="chapter-title" style="left:calc(${x-bounds.x}px + var(--title-inset,0px));top:${y}px;max-width:calc(${width}px - var(--title-inset,0px));height:${height}px" title="${escape(chapter.name)}">${escape(chapter.name)}</h2>`;
}

export function chapterReferenceHTML(chapter: Chapter, bounds: BoardRect, asset: (path: string) => string): string {
  if (!chapter.reference) return '';
  const {x, y, width, height} = chapterReferenceRect(bounds), {alt, url} = chapter.reference;
  return `<button class="chapter-reference" data-command="reference" data-reference-chapter="${escape(chapter.id)}" style="left:${x-bounds.x}px;top:${y}px;width:${width}px;height:${height}px" aria-label="View build reference: ${escape(alt)}"><span class="reference-caption">${escape(alt)}</span><img src="${escape(asset(url))}" alt="" draggable="false"></button>`;
}

export function chapterReferenceReading(chapter: Chapter, asset: (path: string) => string): string {
  const {alt, url} = chapter.reference!;
  return `<header class="chapter-popup-header"><button class="chapter-close" data-command="close" aria-label="Close" title="Close"><span aria-hidden="true">×</span></button></header><figure class="reference-reading"><figcaption><strong>${escape(alt)}</strong></figcaption><img src="${escape(asset(url))}" alt="${escape(alt)}" draggable="false"></figure>`;
}
