export const storyProgressKey = (manuscript: string) => `combination-progress-v2:${encodeURIComponent(manuscript)}`;

export function legacyProgressKey(manuscript: string) {
  const path = new URL(manuscript).pathname;
  return path.endsWith('/story.md') ? `combination-markdown-v1:${path.split('/').at(-2) || 'story'}` : '';
}
