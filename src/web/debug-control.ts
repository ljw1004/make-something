import {isHomeScreenApp} from './home-screen.ts';

/** Both catalogue and player offer debug controls only in ordinary browser tabs. */
export function browserDebugAvailable() {
  return location.protocol !== 'msw:' && !isHomeScreenApp();
}

export const debugGlyph = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M9 4 7 2m8 2 2-2M8 8V7a4 4 0 0 1 8 0v1M12 9v12M5 9H2m3 5H1m5 5-3 3m16-13h3m-3 5h4m-5 5 3 3"/><rect x="5" y="8" width="14" height="13" rx="6"/></svg>';
