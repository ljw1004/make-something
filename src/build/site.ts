import { existsSync, statSync, readFileSync } from 'node:fs';
import { resolve, relative, isAbsolute } from 'node:path';
import type { Plugin } from 'vite';
import { loadStory, storyIds } from '../story/load.ts';
import { renderCatalogue, renderTerminalCatalogue } from './catalogue.ts';

/** Root HTML is generated output; development always reads the editable templates. */
export function sitePages(): Plugin {
  let root: string;
  let nativeCatalogue: string;
  return {
    name: 'site-pages',
    configResolved(config) {
      root = config.root;
      const output = resolve(root, config.build.outDir);
      const rootFromOutput = relative(output, root);
      const containsRoot = rootFromOutput === '' || (rootFromOutput !== '..' && !rootFromOutput.startsWith('../') && !isAbsolute(rootFromOutput));
      if (containsRoot && config.build.emptyOutDir !== false) {
        throw new Error('A root build requires emptyOutDir: false; the repository must never be emptied.');
      }
    },
    configureServer(server) {
      server.middlewares.use(async (request, response, next) => {
        const url = new URL(request.url ?? '/', 'http://localhost');
        const path = url.pathname;
        const simulator = /^\/simulator(?:-dev)?\.html$/.test(path);
        const rootPage = ['/', '/index.html', '/index-dev.html'].includes(path);
        const adjacent = !rootPage && path.endsWith('/index.html') && url.searchParams.has('story');
        if (rootPage || adjacent || simulator) {
          try {
            let html = readFileSync(resolve(root, simulator ? 'simulator-dev.html' : 'index-dev.html'), 'utf8');
            if (adjacent) {
              const prefix = '../'.repeat(path.split('/').length - 2);
              html = html.replace('data-catalogue="./index.html"', `data-catalogue="${prefix}index.html"`)
                .replaceAll('href="./assets/', `href="${prefix}assets/`);
            }
            response.setHeader('Content-Type', 'text/html');
            response.end(await server.transformIndexHtml(path, html));
          } catch (error) { next(error); }
          return;
        }
        // Missing Markdown must be a real 404, not Vite's index fallback.
        if (/\.md$/i.test(path)) {
          let decoded: string;
          try { decoded = decodeURIComponent(path); }
          catch { response.statusCode = 400; response.end('Invalid story path.'); return; }
          const file = resolve(root, `.${decoded}`), local = relative(root, file);
          if (local === '..' || local.startsWith('../') || isAbsolute(local) || !existsSync(file) || !statSync(file).isFile()) {
            response.statusCode = 404; response.end('Story not found.'); return;
          }
        }
        next();
      });
    },
    transformIndexHtml: {
      // Insert artwork after Vite's HTML processing so it stays an ordinary URL.
      order: 'post',
      handler(html, context) {
        if (!html.includes('<!-- story-catalogue -->') && !html.includes('<!-- terminal-catalogue -->')) return html;
        const entries = storyIds(root).map(path => {
          const { story } = loadStory(resolve(root, path));
          return { path, title: story.title, cover: story.cover ?? story.chapters[0]?.image, description: story.description };
        });
        if (html.includes('<!-- story-catalogue -->') && context.bundle) {
          nativeCatalogue = renderCatalogue(entries.filter(entry => entry.path.startsWith('stories/')));
        }
        return html.replace('<!-- story-catalogue -->', () => renderCatalogue(entries))
          .replace('<!-- terminal-catalogue -->', () => renderTerminalCatalogue(entries));
      },
    },
    generateBundle: {
      order: 'post',
      handler(_, bundle) {
        const page = Object.values(bundle).find(file => file.fileName.endsWith('-dev.html'));
        if (!page || page.type !== 'asset') throw new Error('Missing page template');
        let html = String(page.source);
        for (const file of Object.values(bundle)) {
          if (file.fileName === page.fileName) continue;
          const url = `./${file.fileName}`;
          if (file.type === 'chunk' && file.isEntry && !file.imports.length && file.dynamicImports.every(path => path === file.fileName)) {
            const tag = `<script type="module" crossorigin src="${url}"></script>`;
            if (!html.includes(tag)) throw new Error(`Missing entry script ${url}`);
            // An HTML parser recognizes script end tags even inside a JavaScript string.
            html = html.replace(tag, () => `<script type="module">${file.code.replace(/<\/script/gi, '<\\/script')}</script>`);
          } else if (file.type === 'asset' && file.fileName.endsWith('.css')) {
            const tag = `<link rel="stylesheet" crossorigin href="${url}">`;
            if (!html.includes(tag)) throw new Error(`Missing stylesheet ${url}`);
            html = html.replace(tag, () => `<style>${file.source}</style>`);
          } else throw new Error(`Unexpected external dependency: ${file.fileName}`);
          delete bundle[file.fileName];
        }
        delete bundle[page.fileName];
        if (page.fileName === 'index-dev.html') {
          this.emitFile({type: 'asset', fileName: 'ios/Packaging/catalogue.html', source: nativeCatalogue});
        }
        this.emitFile({type: 'asset', fileName: page.fileName.replace('-dev.html', '.html'), source: html});
      },
    },
  };
}
