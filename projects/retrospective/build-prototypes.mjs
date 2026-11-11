// A separate export of preserved experiments; never part of the current game's build.
import {cp, mkdir, mkdtemp, readFile, readdir, rm, symlink, writeFile} from 'node:fs/promises';
import {join, relative, resolve, dirname, sep} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {build} from 'vite';

const project = dirname(fileURLToPath(import.meta.url));
const repository = resolve(project, '../..');
const archive = join(repository, 'archive/2026.10.30 initial experiments');
const output = join(repository, 'archive/prototypes');
const source = join(project, 'static');
await mkdir(join(repository, 'runs'), {recursive: true});
const scratch = await mkdtemp(join(repository, 'runs/prototypes-build-'));
const page = (title, script) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title></head><body><div id="app"></div><script type="module" src="${script}"></script></body></html>`;
const selectedIds = ['food', 'elements-basket-continuity-v10', 'kitchen-caravan-small-sessions-v8'];
const legacyImport = path => import(pathToFileURL(join(archive, path)).href);
const read = path => readFile(path, 'utf8');
function between(text, start, end) {
  const from = text.indexOf(start), to = end ? text.indexOf(end, from) : text.length;
  if (from < 0 || to < from) throw Error(`Archived source boundary changed: ${start}`);
  return text.slice(from, to);
}
async function files(directory) {
  const result = [];
  for (const entry of await readdir(directory, {withFileTypes: true})) {
    const path = join(directory, entry.name);
    result.push(...entry.isDirectory() ? await files(path) : [path]);
  }
  return result;
}

try {
  // Link read-only inputs into the scratch build, keeping relative legacy imports intact.
  await symlink(join(archive, 'src'), join(scratch, 'src'), 'dir');
  await symlink(join(archive, 'experiments'), join(scratch, 'experiments'), 'dir');
  await cp(source, scratch, {recursive: true});
  await writeFile(join(scratch, 'board.html'), page('Combination · Prototypes', '/src/main.ts'));
  await writeFile(join(scratch, 'elements-discovery.html'), page('Elements · A World to Make', '/src/elements-discovery-main.ts'));
  await writeFile(join(scratch, 'campaign.html'), page('Combination journeys · Prototypes', '/experiments/tangible-campaign/ui/campaign-main.ts'));

  // Keep the original reader's presentation; replace only its HTTP transport and navigation.
  const reader = await read(join(archive, 'experiments/story-player.html'));
  const readerShell = between(reader, '<!doctype html>', '<script>')
    .replace('<nav>', '<nav><a href="index.html">All prototypes</a>')
    .replace('href="/bell"', 'href="story.html?game=bell2"')
    .replace('href="/mneme"', 'href="story.html?game=mneme2"')
    .replace('Sessions stay in this local server’s memory;', 'Sessions stay in this page’s memory;');
  await writeFile(join(scratch, 'story.html'), readerShell + '<script type="module" src="./text-player.js"></script></html>');
  await writeFile(join(scratch, 'text-player.js'), between(reader, 'let session=', 'async function start()') + await read(join(source, 'text-session.js')));

  // Reuse the archived run format, hashing, action recording and replay verbatim.
  const runner = await read(join(archive, 'experiments/logical-games.ts'));
  await writeFile(join(scratch, 'text-runner.ts'),
    "import {LOGICAL_GAMES} from './text-games.ts';\nexport {LOGICAL_GAMES};\n" +
    between(runner, 'export const logicalHash=', 'function grid(') +
    between(runner, 'export interface LogicalDecision {'));

  const {scenarios} = await legacyImport('experiments/tangible-campaign/ui/current-scenarios.ts');
  const {applyMilestones} = await legacyImport('experiments/tangible-campaign/ui/current-campaign.ts');
  const selected = selectedIds.map(id => {
    const scenario = scenarios.find(s => s.id === id);
    if (!scenario) throw Error(`Missing preserved scenario: ${id}`);
    return scenario;
  });
  const artwork = [...new Set(JSON.stringify(selected.map(applyMilestones)).match(/\/assets\/locations\/[^"\\]+/g))];
  const selectedCatalogue = `export const scenarios=${JSON.stringify(selected)};\nexport const featuredScenarioIds=${JSON.stringify(selectedIds)};\nexport const presentationFor=s=>({title:s.title,premise:s.premise});`;
  const textModels = new Set(['logical-bell-orchard.ts', 'logical-bell-orchard-2.ts', 'logical-mneme.ts', 'logical-mneme-2.ts']);

  await build({
    configFile: false, root: scratch, base: './', publicDir: false,
    resolve: {alias: {legacy: archive}},
    plugins: [{
      name: 'retrospective-static-adapters', enforce: 'pre',
      transform(code, id) {
        if (!id.startsWith(archive + sep)) return;
        const name = relative(archive, id);
        if (name === 'experiments/tangible-campaign/ui/campaign-page-catalogue.ts') code = selectedCatalogue;
        if (textModels.has(name.replace('experiments/', ''))) {
          // Remove the Node-only screening CLI, leaving all game functions unchanged.
          code = code.replace(/^import .* from 'node:(?:fs|url)';\r?\n/gm, '')
            .replace(/^import .*from 'node:(?:fs|url)';\r?\n/gm, '');
          code = between(code, code.split('\n')[0], 'if(process.argv[1]');
          if (/node:|process\.|mkdirSync|writeFileSync/.test(code)) throw Error(`Node code remains in ${name}`);
        }
        if (name.endsWith('.ts')) {
          // Do not load or overwrite saves made in other editions on this origin.
          code = code.replace(/localStorage\.(getItem|setItem|removeItem)\(/g, "localStorage.$1('retrospective-prototypes-1:'+");
        }
        if (name === 'src/elements-discovery-main.ts') {
          code = code.replace('<a href="index.html">Mars</a><a href="history.html">Ideas</a>', '<a href="index.html">All prototypes</a>');
        }
        if (name === 'src/ui.ts') {
          // Blank HTML-template lines otherwise survive minification as trailing whitespace.
          code = code.replace(/^[\t ]+$/gm, '');
        }
        if (name === 'experiments/tangible-campaign/ui/save-autosave.ts') {
          // This writer accesses localStorage through an injected storage alias.
          code = code.replace('storage.setItem(options.key, encoded)', "storage.setItem('retrospective-prototypes-1:'+options.key, encoded)");
        }
        if (name === 'experiments/tangible-campaign/ui/campaign-main.ts') {
          // Preserve validated model paths; resolve them relative to the exported page only at rendering.
          for (const expression of ['setting.background.asset', 'milestone.artwork.src']) {
            code = code.replaceAll(`esc(${expression})`, `esc(${expression}.replace(/^\\/assets\\//, './assets/'))`);
          }
          code = code.replace(/<a href="mars-expedition.html">[^<]*<\/a>/g, '<a href="index.html">All prototypes</a>')
            .replace('Six development focuses, including a short purpose workshop. Try them, then tell me where discovery turns into guesswork or busywork.', 'Selected campaigns from the prototype collection.');
        }
        return {code, map: null};
      },
    }],
    build: {
      outDir: join(scratch, 'dist'), emptyOutDir: true,
      rolldownOptions: {input: ['index', 'board', 'elements-discovery', 'campaign', 'story'].map(name => join(scratch, name + '.html'))},
    },
  });
  for (const asset of artwork) {
    if (!asset.startsWith('/assets/locations/') || asset.includes('..')) throw Error('Unexpected artwork path');
    const target = join(scratch, 'dist', asset.slice(1));
    await mkdir(dirname(target), {recursive: true});
    await cp(join(archive, 'public', asset.slice(1)), target);
  }
  const generated = (await files(join(scratch, 'dist'))).map(path => relative(join(scratch, 'dist'), path)).sort();
  let previous = [];
  try { previous = JSON.parse(await read(join(output, 'build-files.json'))).files; }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  // Only files recorded in the prior generated inventory may be removed.
  for (const file of previous) {
    if (file.startsWith('/') || file.split('/').includes('..')) throw Error('Invalid generated inventory');
  }
  await mkdir(output, {recursive: true});
  await cp(join(scratch, 'dist'), output, {recursive: true});
  for (const file of previous) if (!generated.includes(file)) await rm(join(output, file), {force: true});
  await writeFile(join(output, 'build-files.json'), JSON.stringify({
    sourceCommit: '1e8567d3', builder: 'projects/retrospective/build-prototypes.mjs',
    scenarios: selectedIds, files: generated,
  }, null, 2) + '\n');
  console.log(`Exported ${generated.length} files, including ${artwork.length} illustrations, to archive/prototypes/`);
} finally {
  await rm(scratch, {recursive: true, force: true});
}
