export type DialogContext = { kind: 'pending' | 'entry' | 'chapter' | 'confirm' | 'error' }
  | { kind: 'encyclopedia'; item?: string; detail?: boolean };

export type CarouselResume = {kind: 'board'} | {kind: 'entry' | 'chapter'; scrollTop: number}
  | {kind: 'pending'; key: string; scrollTop: number};

export function restoreCarouselResume(value: unknown, pendingKey?: string): CarouselResume | undefined {
  if (!value || typeof value !== 'object' || !('kind' in value)) return;
  if (value.kind === 'board' && pendingKey === undefined) return {kind: 'board'};
  const scrollTop = 'scrollTop' in value && typeof value.scrollTop === 'number' && Number.isFinite(value.scrollTop)
    ? Math.max(0, value.scrollTop) : 0;
  if (value.kind === 'pending' && pendingKey !== undefined && 'key' in value && value.key === pendingKey) {
    return {kind: 'pending', key: pendingKey, scrollTop};
  }
  if ((value.kind === 'entry' || value.kind === 'chapter') && pendingKey === undefined) {
    return {kind: value.kind, scrollTop};
  }
}

/** Saved authoring anchors may predate direct item reads opening the book. */
export function restoreDialogContext(value: unknown): DialogContext | undefined {
  if (!value || typeof value !== 'object' || !('kind' in value)) return undefined;
  if (value.kind === 'reading') {
    return 'item' in value && typeof value.item === 'string'
      ? { kind: 'encyclopedia', item: value.item, detail: true } : undefined;
  }
  if (value.kind === 'encyclopedia') return {
    kind: 'encyclopedia',
    item: 'item' in value && typeof value.item === 'string' ? value.item : undefined,
    detail: 'detail' in value && value.detail === true,
  };
  if (value.kind === 'pending' || value.kind === 'entry' || value.kind === 'chapter' || value.kind === 'confirm' || value.kind === 'error') return { kind: value.kind };
  return undefined;
}
