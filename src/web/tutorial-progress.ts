export interface TutorialCompletion { dragDone: boolean; hotspotDone: boolean; goalsDone: boolean; encyclopediaDone: boolean }
type Advanced = Omit<TutorialCompletion, 'dragDone'>;
const initialAdvanced: Advanced = {hotspotDone: false, goalsDone: false, encyclopediaDone: false};
const initialCompletion: TutorialCompletion = {dragDone: false, ...initialAdvanced};
type StorageAccess = () => Pick<Storage, 'getItem' | 'setItem' | 'removeItem'>;
const advancedKey = (url: string) => `combination-tutorial-v1:${encodeURIComponent(url)}`;
const load = (raw: string | null): Partial<TutorialCompletion> | null => JSON.parse(raw ?? 'null');

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
    this.dragKey = `combination-tutorial-drag-v2:${encodeURIComponent(scope.manuscript)}`;
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
