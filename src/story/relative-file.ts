/** Validate the author's spelling before URL normalizes dot segments away. */
export function resolveRelativeFile(reference: string, documentURL: URL): URL {
  const path = reference.split(/[?#]/, 1)[0];
  const directory = new URL('./', documentURL);
  const invalid = () => new Error('Use a relative file path without a leading slash or consecutive dots.');
  let decoded: string;
  try { decoded = decodeURIComponent(path); } catch { throw invalid(); }

  // Encoded separators and nested escapes give URL and filesystem consumers
  // different interpretations of the same path. Ordinary escaped spaces work.
  if (!path || reference !== reference.trim() || path.startsWith('/') ||
      /%(?:2f|5c|25)/i.test(path) || decoded.includes('..') || reference.includes('..') ||
      /[:\\\u0000-\u001f\u007f]/.test(decoded)) throw invalid();
  const file = new URL(reference, directory);
  if (file.protocol !== directory.protocol || file.host !== directory.host ||
      !file.pathname.startsWith(directory.pathname) || file.pathname.endsWith('/')) throw invalid();
  return file;
}
