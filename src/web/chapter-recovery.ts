/** Legacy movement flags are not evidence of a combination in this chapter. */
export function hasChapterCombination(state: {actions?: unknown}, saved?: {combined?: unknown}): boolean {
  if (typeof saved?.combined === 'boolean') return saved.combined;
  if (!Array.isArray(state.actions)) return false;
  const arrival = state.actions.findLastIndex(action => action?.type === 'advance');
  return state.actions.slice(arrival + 1).some(action => action?.type === 'combine');
}

export function chapterRecovery(session: {combined: boolean}): 'chapter'|'story' {
  return session.combined ? 'chapter' : 'story';
}

/** Inspect the saved snapshot without loading the manuscript or validating its game replay. */
export function catalogueStoryStarted(raw: string | null): boolean {
  try {
    const saved = JSON.parse(raw ?? 'null');
    const state = saved?.state;
    if (!state || !Number.isInteger(state.chapter) || state.chapter < 0) return false;
    return state.completed === true || state.chapter > 0 ||
      chapterRecovery({combined:hasChapterCombination(state, saved?.chapterSession)}) === 'chapter';
  } catch { return false; }
}
