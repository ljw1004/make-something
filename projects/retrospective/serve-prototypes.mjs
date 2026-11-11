/** Local retrospective playback; never loads the active game's Vite config. */
import { fileURLToPath } from 'node:url';
import { join } from 'node:path';
import { createServer } from 'vite';

const repository = fileURLToPath(new URL('../../', import.meta.url));
const port = Number(process.env.RETROSPECTIVE_PORT ?? 4187);
if (!Number.isInteger(port) || port < 1 || port > 65535) {
  throw new Error('RETROSPECTIVE_PORT must be an integer from 1 to 65535.');
}

const server = await createServer({
  configFile: false,
  root: join(repository, 'archive/2026.10.30 initial experiments'),
  cacheDir: join(repository, 'runs/retrospective-vite-cache'),
  optimizeDeps: { noDiscovery: true, include: [] },
  server: { host: '127.0.0.1', port, strictPort: true },
});
await server.listen();
server.printUrls();
console.log('Prototype routes and the separate text-story server: projects/retrospective/prototype-history.md');

for (const signal of ['SIGINT', 'SIGTERM']) {
  process.once(signal, async () => {
    await server.close();
    process.exit(0);
  });
}
