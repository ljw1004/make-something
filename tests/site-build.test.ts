import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, mkdirSync, writeFileSync, readFileSync, readdirSync, rmSync} from 'node:fs';
import {resolve, join} from 'node:path';
import {build, createServer, type InlineConfig} from 'vite';
import {sitePages} from '../src/build/site.ts';

test('root pages embed independent code and styles, and development serves fresh templates', async () => {
  mkdirSync('runs', {recursive: true});
  const root = mkdtempSync(resolve('runs/site-build-'));
  const write = (path: string, text: string) => writeFileSync(join(root, path), text);
  const read = (path: string) => readFileSync(join(root, path), 'utf8');
  const config: InlineConfig = {
    configFile: false, root, base: './', appType: 'mpa', publicDir: false, logLevel: 'silent',
    cacheDir: join(root, '.vite'), build: {outDir: '.', emptyOutDir: false, modulePreload: false},
  };
  const runBuild = (name: string, overrides: InlineConfig['build'] = {}) => build({...config, plugins: [sitePages()],
    build: {...config.build, rolldownOptions: {input: join(root, name + '-dev.html'), output: {codeSplitting: false}}, ...overrides}});
  let server: Awaited<ReturnType<typeof createServer>> | undefined;
  try {
    mkdirSync(join(root, 'stories/shared'), {recursive: true});
    write('stories/shared/story.md', '# First title\n\nbackground: ![start](start.svg)\n\n## Workshop\n');
    write('stories/shared/design-brief.md', '# Excluded brief\n');
    mkdirSync(join(root, 'contrib/example'), {recursive: true});
    write('contrib/example/example.md', '# Experimental title\n\n## Opening\n');
    write('page.css', '.chooser{display:block}');
    write('index.js', 'document.title = "graphical fixture";');
    write('simulator.js', 'document.title = "terminal fixture";');
    const template = (name: string, marker: string) => `<!doctype html><head><link rel="stylesheet" href="/page.css"></head><body>${marker}<script type="module" src="/${name}.js"></script></body>`;
    const index = template('index', '<!-- story-catalogue -->');
    write('index-dev.html', index);
    write('simulator-dev.html', template('simulator', '<!-- terminal-catalogue -->'));
    for (const name of ['index', 'simulator']) {
      await runBuild(name);
      assert.doesNotMatch(read(name + '.html'), /<script[^>]* src=|rel="stylesheet"|Excluded brief/);
      assert.match(read(name + '.html'), /<style>\.chooser\{display:block\}/);
    }
    for (const page of ['index.html', 'simulator.html']) {
      assert.deepEqual([...read(page).matchAll(/data-story="([^"]+)"/g)].map(match => match[1]),
        ['stories/shared/story.md', 'contrib/example/example.md']);
    }
    const native = read('ios/Packaging/catalogue.html');
    assert.match(native, /data-story="stories\/shared\/story.md"/);
    assert.doesNotMatch(native, /contrib\/|Experimental title/);
    assert.match(read('index.html'), /graphical fixture/);
    assert.match(read('index.html'), /href="index.html\?story=stories\/shared\/story.md"/);
    assert.match(read('index.html'), /src="stories\/shared\/start.svg"/);
    assert.doesNotMatch(read('index.html'), /terminal fixture/);
    assert.match(read('simulator.html'), /terminal fixture/);
    assert.match(read('simulator.html'), /class="terminal-story-title">FIRST TITLE</);
    assert.doesNotMatch(read('simulator.html'), /graphical fixture|<img/);
    assert(!readdirSync(root).includes('assets'));
    assert.equal(read('index-dev.html'), index);
    await assert.rejects(runBuild('index', {emptyOutDir: true}), /repository must never be emptied/);
    await assert.rejects(runBuild('index', {outDir: '..', emptyOutDir: true}), /repository must never be emptied/);
    const built = read('index.html');
    write('index.js', 'import "./does-not-exist.js";');
    await assert.rejects(runBuild('index'));
    assert.equal(read('index.html'), built);
    write('index.js', 'document.title = "updated";');
    await runBuild('index');
    assert.match(read('index.html'), /updated/);
    write('stories/shared/story.md', '# Updated title\n\n## Workshop\n');
    server = await createServer({...config, plugins: [sitePages()], server: {host: '127.0.0.1', port: 0}});
    await server.listen();
    const base = server.resolvedUrls!.local[0];
    for (const path of ['', 'index.html', 'index-dev.html', 'stories/shared/index.html?story=story.md', 'simulator.html', 'simulator-dev.html']) {
      const html = await (await fetch(new URL(path, base))).text();
      assert.match(html, /Updated title/i);
      assert.match(html, /@vite\/client/);
    }
    for (const path of ['stories/shared/missing.md', 'make-something.html', 'simulator-story.html', 'simulator-interactions.html']) {
      assert.equal((await fetch(new URL(path, base))).status, 404);
    }
    assert.match(read('index.html'), /First title/);
  } finally {
    await server?.close();
    rmSync(root, {recursive: true, force: true});
  }
});
