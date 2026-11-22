import {resolve} from 'node:path';
import { defineConfig } from 'vite';
import { sitePages } from './src/build/site.ts';

export default defineConfig(({command}) => ({
  base: './',
  appType: 'mpa',
  publicDir: false,
  plugins: [sitePages()],
  builder: {},
  environments: command === 'build' ? {
    client: {build: {rolldownOptions: {input: 'index-dev.html'}}},
    simulator: {consumer: 'client', build: {rolldownOptions: {input: 'simulator-dev.html'}}},
  } : undefined,
  build: {
    outDir: '.',
    emptyOutDir: false,
    modulePreload: false,
    rolldownOptions: {output: {codeSplitting: false}},
  },
  server: {watch: {ignored: ['**/archive/**', '**/runs/**', resolve('index.html'), resolve('simulator.html')]}},
}));
