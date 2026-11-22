import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { resolve, join, basename, relative } from 'node:path';
import { createHash } from 'node:crypto';
import { parseStory } from './parser.ts';

const repository = resolve(import.meta.dirname, '../..');

/** Repository-relative manuscripts, ordered by collection and then by path. */
export function storyIds(root = repository): string[] {
  return ['stories', 'contrib'].flatMap(collection => {
    const directory = join(root, collection);
    if (!existsSync(directory)) return [];
    return readdirSync(directory, { withFileTypes: true, recursive: true })
      .filter(entry => entry.isFile() && /\.md$/i.test(entry.name) && entry.name.toLowerCase() !== 'design-brief.md')
      .map(entry => relative(root, join(entry.parentPath, entry.name)).replaceAll('\\', '/')).sort();
  });
}

function lookupStory(id: string, root: string): string {
  const paths = storyIds(root);
  if (paths.includes(id)) return id;
  const matches = paths.filter(path => path.slice(path.indexOf('/') + 1) === id || basename(path).replace(/\.md$/i, '') === id);
  if (!matches.length) throw new Error(`Unknown story ${id}. Choose ${paths.join(', ')}.`);
  if (matches.length > 1) throw new Error(`Ambiguous story ${id}. Choose ${matches.join(', ')}.`);
  return matches[0];
}

export function loadStory(id: string, root = repository) {
  const local = resolve(id);
  const path = existsSync(local) && statSync(local).isFile() ? local : lookupStory(id, root);
  const file = resolve(root, path);
  const markdown = readFileSync(file, 'utf8');
  return { story: parseStory(markdown, { id, file: relative(process.cwd(), file) }), path, hash: createHash('sha256').update(markdown).digest('hex'), markdown };
}
