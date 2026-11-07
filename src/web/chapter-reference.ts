import type {Chapter} from '../story/types.ts';
import type {BoardRect} from './board-geometry.ts';
import {escape} from './markdown.ts';

/** Leave the top-left supply pocket and the top-right debug control available. */
export function chapterReferenceRect(bounds: BoardRect): BoardRect {
  const width = Math.min(196, Math.max(44, bounds.width - 96));
  return {x: bounds.x + bounds.width - width - 48, y: bounds.y + 12, width, height: 88};
}

export function chapterReferenceHTML(chapter: Chapter, bounds: BoardRect, asset: (path: string) => string): string {
  if (!chapter.reference) return '';
  const {x, y, width, height} = chapterReferenceRect(bounds), {alt, url} = chapter.reference;
  return `<button class="chapter-reference" data-command="reference" data-reference-chapter="${escape(chapter.id)}" style="left:${x-bounds.x}px;top:${y}px;width:${width}px;height:${height}px" aria-label="View build reference: ${escape(alt)}"><img src="${escape(asset(url))}" alt="" draggable="false"><span class="reference-caption"><span class="reference-eyebrow">Building toward</span><span>${escape(alt)}</span></span><span class="reference-expand" aria-hidden="true">↗</span></button>`;
}

export function chapterReferenceReading(chapter: Chapter, asset: (path: string) => string): string {
  const {alt, url} = chapter.reference!;
  return `<header class="chapter-popup-header"><button class="chapter-close" data-command="close" aria-label="Close" title="Close"><span aria-hidden="true">×</span></button></header><figure class="reference-reading"><figcaption><span class="reference-eyebrow">Building toward</span><strong>${escape(alt)}</strong></figcaption><img src="${escape(asset(url))}" alt="${escape(alt)}" draggable="false"></figure>`;
}
