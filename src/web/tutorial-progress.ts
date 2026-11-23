export interface TutorialCompletion { dragDone: boolean; hotspotDone: boolean; goalsDone: boolean; encyclopediaDone: boolean }
type Advanced = Omit<TutorialCompletion, 'dragDone'>;
const initialAdvanced: Advanced = {hotspotDone: false, goalsDone: false, encyclopediaDone: false};
const initialCompletion: TutorialCompletion = {dragDone: false, ...initialAdvanced};
type StorageAccess = () => Pick<Storage, 'getItem' | 'setItem' | 'removeItem'>;
const advancedKey = (url: string) => `combination-tutorial-v1:${encodeURIComponent(url)}`;
const dragKey = (url: string) => `combination-tutorial-drag-v2:${encodeURIComponent(url)}`;
const load = (raw: string | null): Partial<TutorialCompletion> | null => JSON.parse(raw ?? 'null');

const tutorialKinds = ['drag', 'hotspot', 'goals', 'encyclopedia'] as const;
type TutorialKind = typeof tutorialKinds[number];
const shownKey = (manuscript: string, kind: TutorialKind) => `combination-tutorial-shown-v1:${encodeURIComponent(manuscript)}:${kind}`;

/** Count a visible hint independently of the action that completes the lesson. */
export function recordTutorialShown(manuscript: string, kind: TutorialKind) {
  try { localStorage.setItem(shownKey(manuscript, kind), 'true'); }
  catch { /* An unavailable display history must not interrupt the tutorial. */ }
}

export function catalogueTutorialCount(manuscripts: readonly string[]) {
  const shown = tutorialKinds.filter(kind => manuscripts.some(url => localStorage.getItem(shownKey(url, kind)) === 'true'));
  return {shown: shown.length, total: tutorialKinds.length};
}

export function resetCatalogueTutorials(catalogue: string, manuscripts: readonly string[]) {
  localStorage.removeItem(advancedKey(catalogue));
  for (const manuscript of manuscripts) {
    localStorage.removeItem(advancedKey(manuscript));
    localStorage.removeItem(dragKey(manuscript));
    for (const kind of tutorialKinds) localStorage.removeItem(shownKey(manuscript, kind));
  }
}

/** Opening drag always follows the manuscript. Only advanced lessons may be shared. */
export class TutorialProgress {
  readonly key: string;
  readonly dragKey: string;
  completion: TutorialCompletion = {...initialCompletion};
  private readonly storyKey: string;
  private readonly report: (message: string) => void;
  private readonly storage: StorageAccess;
  private warning = '';

  constructor(scope: {manuscript: string; catalogue?: string}, report: (message: string) => void,
    storage: StorageAccess = () => localStorage) {
    this.report = report;
    this.storage = storage;
    this.storyKey = advancedKey(scope.manuscript);
    this.key = scope.catalogue ? advancedKey(scope.catalogue) : this.storyKey;
    this.dragKey = dragKey(scope.manuscript);
    try {
      const saved = load(storage().getItem(this.key));
      const drag = storage().getItem(this.dragKey);
      // A previous per-story drag is attributable; a shared v1 drag isn't.
      this.completion = {
        dragDone: drag === null ? load(storage().getItem(this.storyKey))?.dragDone === true : drag === 'true',
        hotspotDone: saved?.hotspotDone === true,
        goalsDone: saved?.goalsDone === true,
        encyclopediaDone: saved?.encyclopediaDone === true,
      };
    } catch { this.notify('Tutorial progress could not be restored. Tutorials will be remembered for this session.'); }
  }
  private notify(message: string) {
    if (this.warning === message) return;
    this.warning = message; this.report(message);
  }
  finish(step: keyof TutorialCompletion) {
    if (this.completion[step]) return;
    this.completion[step] = true;
    try {
      const storage = this.storage();
      if (step === 'dragDone') storage.setItem(this.dragKey, 'true');
      else {
        // Merge with disk so independently open stories don't erase each other's lessons.
        const saved = load(storage.getItem(this.key));
        storage.setItem(this.key, JSON.stringify({...saved, [step]: true}));
      }
      this.notify('');
    } catch { this.notify('Tutorial progress could not be saved. Completed tutorials may reappear after reloading.'); }
  }
  reset() {
    const shared = this.key !== this.storyKey;
    if (shared) this.completion.dragDone = false;
    else this.completion = {...initialCompletion};
    try {
      const storage = this.storage();
      if (shared) {
        // A false override prevents the attributable legacy flag from returning.
        storage.setItem(this.dragKey, 'false');
      } else {
        storage.removeItem(this.storyKey);
        storage.removeItem(this.dragKey);
      }
      this.notify('');
    } catch { this.notify('Tutorial progress could not be reset in browser storage. It has been reset for this session.'); }
  }
}
