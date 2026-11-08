import type {Diagnostic, Source, Story} from '../story/types.ts';
import {chapterIndex} from '../story/chapters.ts';
import {itemPresentation} from '../engine/presentation.ts';
import {background} from '../engine/analysis.ts';

export function presentationDiagnostics(story: Story): Diagnostic[] {
  const diagnostics: Diagnostic[] = [];
  const error = (code: string, message: string, source: Source, earlier?: Source) => diagnostics.push({
    severity: 'error', code, message, source, span: source.span!, stage: 'fast',
    ...(earlier ? {related: [{...earlier, span: earlier.span!, message: 'Earlier declaration.'}]} : {}),
  });
  const chapters = new Map<string, Source>();
  story.chapters.forEach((chapter, index) => {
    if (chapter.backgroundAnimation && !background(story, index)) error('background-animation-poster', 'A background animation requires an explicit or inherited static background for geometry and the still fallback.', chapter.backgroundAnimation.source);
  });
  for (const reference of story.sourceReferences.filter(ref => ref.kind === 'chapter' && ref.declaration && ref.id.startsWith('id:'))) {
    if (chapters.has(reference.id)) error('duplicate-chapter-id', 'Chapter identifiers must be unique, including chapters with the same title.', reference.source, chapters.get(reference.id));
    else chapters.set(reference.id, reference.source);
    const entity = story.items[reference.id] ?? story.hotspots[reference.id];
    if (entity) error('namespace-clash', `Chapter identifier ${reference.id.slice(3)} is also used by an item or hotspot. All backtick identifiers share one namespace.`, reference.source, entity.source);
  }
  for (const item of Object.values(story.items)) {
    const changes = new Map<string, {value: string; source: Source}>();
    const missingPosters = new Set<Source>();
    for (let chapter = 0; chapter < story.chapters.length; chapter++) {
      const appearance = itemPresentation(story, chapter, item.id);
      if (appearance.animation && !appearance.icon && !missingPosters.has(appearance.animation.source)) {
        missingPosters.add(appearance.animation.source);
        error('animation-poster', `${item.name}'s animation requires a static icon for its display dimensions and still fallback.`, appearance.animation.source);
      }
    }
    for (const change of item.presentations) {
      const chapter = chapterIndex(story, change.chapter);
      if (chapter < 0) continue;
      const property = change.icon ? 'icon' : change.animation !== undefined ? 'animation' : 'name';
      const key = `${chapter}:${property}`;
      const value = change.icon ? JSON.stringify([change.icon.url, change.icon.circular]) : change.animation !== undefined ? change.animation?.url ?? 'none' : change.name!;
      const previous = changes.get(key);
      if (previous && previous.value !== value) error('conflicting-presentation', `${item.name} has conflicting ${property}s from the same chapter.`, change.source, previous.source);
      else if (!previous) changes.set(key, {value, source: change.source});
    }
  }
  return diagnostics;
}
