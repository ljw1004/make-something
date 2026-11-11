// Run after build-prototypes.mjs. Uses a plain static server, never Vite or the story API.
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {dirname, extname, resolve, sep} from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from 'playwright';
import {LOGICAL_GAMES, replayLogical} from '../../archive/2026.10.30 initial experiments/experiments/logical-games.ts';
import {screenBellOrchard} from '../../archive/2026.10.30 initial experiments/experiments/logical-bell-orchard.ts';
import {screenMneme} from '../../archive/2026.10.30 initial experiments/experiments/logical-mneme.ts';
import {screenMneme as screenMneme2} from '../../archive/2026.10.30 initial experiments/experiments/logical-mneme-2.ts';

const repository = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const output = resolve(repository, 'archive/prototypes');
const prefix = '/make-something/archive/prototypes/';
const inventory = JSON.parse(await readFile(resolve(output, 'build-files.json'), 'utf8'));
assert(inventory.files.length > 0);
for (const file of inventory.files) await readFile(resolve(output, file));

// Match Jekyll 3.10 EntryFilter's glob/prefix exclusion semantics using Ruby itself.
// Check every archive sibling, including any newly added folder, and every export.
execFileSync('ruby', ['-r', 'yaml', '-e', `
  config = YAML.load_file('_config.yml')
  excluded = ->(path) { config['exclude'].any? { |pattern| File.fnmatch?(pattern, path) || path.start_with?(pattern) } }
  abort 'Archive root excluded' if excluded.call('archive')
  Dir.children('archive').each do |name|
    path = "archive/#{name}"
    abort "Unexpected published archive entry: #{path}" if name != 'prototypes' && !excluded.call(path)
  end
  Dir.glob('archive/prototypes/**/*').each do |path|
    abort "Prototype export excluded: #{path}" if excluded.call(path)
  end
`], {cwd: repository});

const mime = {'.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.webp': 'image/webp', '.json': 'application/json'};
const server = createServer(async (request, response) => {
  try {
    let path = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    if (!path.startsWith(prefix)) throw Error('Outside export');
    path = path.slice(prefix.length) || 'index.html';
    const file = resolve(output, path);
    if (!file.startsWith(output + sep)) throw Error('Outside export');
    response.setHeader('Content-Type', mime[extname(file)] || 'application/octet-stream');
    response.end(await readFile(file));
  } catch {
    response.statusCode = 404;
    response.end('Not found');
  }
});
await new Promise(done => server.listen(0, '127.0.0.1', done));
const base = `http://127.0.0.1:${server.address().port}${prefix}`;
let browser;
const problems = [];
let endings = 0;
try {
  browser = await chromium.launch();
  const context = await browser.newContext({viewport: {width: 1100, height: 900}});
  const page = await context.newPage();
  page.on('pageerror', error => problems.push(error.message));
  page.on('response', response => {if (response.status() >= 400) problems.push(`${response.status()} ${response.url()}`);});
  page.on('requestfailed', request => problems.push(`${request.failure()?.errorText} ${request.url()}`));
  page.on('request', request => {if (new URL(request.url()).pathname.includes('/api/')) problems.push('Unexpected API request');});

  await page.goto(base);
  const routes = await page.locator('ol a').evaluateAll(links => [...new Set(links.map(link => link.getAttribute('href')))]);
  assert.equal(routes.length, 13); // Nine prototypes, plus two v1 readers and two extra canvas modes.
  for (const route of routes) {
    await context.clearCookies();
    await page.goto(base + route);
    await page.waitForFunction(() => document.body.innerText.trim().length > 40);
    if (await page.locator('#error').count()) assert.equal(await page.locator('#error').textContent(), '');
    await page.waitForFunction(() => [...document.images].every(image => image.complete && image.naturalWidth > 0));
  }

  // Every original Bell ending, and every complete Mneme branch, through the adapted UI.
  // Downloaded observations and state hashes must replay in the unmodified Node runner.
  const bellPaths = screenBellOrchard().endings.map(ending => ending.path);
  const paths = {
    bell: bellPaths, bell2: bellPaths,
    mneme: screenMneme().endings.map(ending => ending.path),
    mneme2: screenMneme2().endings.map(ending => ending.path),
  };
  for (const [id, branches] of Object.entries(paths)) {
    const game = LOGICAL_GAMES[id];
    await page.goto(base + 'story.html?game=' + id);
    await page.locator('#controls button').first().waitFor();
    for (const path of branches) {
      await page.locator('#restart').click();
      let state = game.create(game.scenarios[0], 0);
      for (const action of path) {
        const actions = game.observe(state).legalActions;
        const index = actions.findIndex(candidate => JSON.stringify(candidate) === JSON.stringify(action));
        assert(index >= 0);
        assert.equal(await page.locator('#controls button').count(), actions.length);
        await page.locator('#controls button').nth(index).click();
        state = game.step(state, action);
        assert.equal(await page.locator('#error').textContent(), '');
      }
      const downloadReady = page.waitForEvent('download');
      await page.locator('#download').click();
      const download = await downloadReady;
      const run = JSON.parse(await readFile(await download.path(), 'utf8'));
      assert.deepEqual(replayLogical(run), state);
      assert.equal(run.decisions.length, path.length);
      await download.delete();
      endings++;
    }
    await page.reload();
    await page.locator('#controls button').first().waitFor();
    assert.equal(await page.locator('#controls button').count(), game.observe(game.create(game.scenarios[0], 0)).legalActions.length);
  }

  async function drag(from, to) {
    await from.scrollIntoViewIfNeeded();
    const a = await from.boundingBox(), b = await to.boundingBox();
    assert(a && b);
    await page.mouse.move(a.x + a.width / 2, a.y + a.height / 2);
    await page.mouse.down();
    await page.mouse.move(b.x + b.width / 2, b.y + b.height / 2, {steps: 15});
    await page.mouse.up();
  }
  await page.goto(base + 'elements-discovery.html');
  await page.getByRole('button', {name: 'Begin', exact: true}).click();
  await drag(page.getByRole('button', {name: 'Earth', exact: true}), page.getByRole('button', {name: 'Water', exact: true}));
  await page.getByRole('button', {name: 'Clay', exact: true}).waitFor();
  await page.reload();
  await page.getByRole('button', {name: 'Clay', exact: true}).waitFor();

  await page.goto(base + 'campaign.html?world=food');
  await page.locator('#close').click();
  await drag(page.getByRole('button', {name: 'Grain', exact: true}), page.getByRole('button', {name: 'Millstone', exact: true}));
  await page.getByRole('button', {name: 'Flour', exact: true}).waitFor();
  await page.waitForFunction(() => document.querySelector('#save-status')?.dataset.state === 'saved');
  await page.reload();
  await page.getByRole('button', {name: 'Flour', exact: true}).waitFor();
  const keys = await page.evaluate(() => Object.keys(localStorage));
  assert(keys.length > 0 && keys.every(key => key.startsWith('retrospective-prototypes-1:')));

  // All exported artwork decodes, including pictures reached only in later chapters.
  const images = inventory.files.filter(file => file.endsWith('.webp'));
  const decoded = await page.evaluate(async paths => {
    await Promise.all(paths.map(path => new Promise((done, reject) => {
      const image = new Image();
      image.onload = () => image.naturalWidth ? done() : reject(Error(path));
      image.onerror = () => reject(Error(path));
      image.src = path;
    })));
    return paths.length;
  }, images);
  assert.equal(decoded, images.length);

  await page.setViewportSize({width: 390, height: 844});
  await page.goto(base);
  assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  await page.goto(base + 'story.html?game=mneme2');
  await page.locator('#controls button').first().waitFor();
  assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  await page.goto(base + 'story.html?game=unknown');
  await page.getByText('Unknown prototype', {exact: true}).waitFor();
  assert.deepEqual(problems, []);
  console.log(`PASS: ${routes.length} launch routes; ${endings} complete text-story branches replay in the original runner; Elements/Food drags and reloads; ${decoded} illustrations; mobile reader/gallery; Pages exclusions.`);
} finally {
  if (browser) await browser.close();
  await new Promise(done => server.close(done));
}
