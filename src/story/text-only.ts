/** Literal Markdown spans have the same meaning inside and outside a passage. */
function literalEnd(text: string, start: number): number | undefined {
  if (text[start] === '\\') return start + 2;
  if (text[start] === '`') {
    const ticks = /^`+/.exec(text.slice(start))![0], end = text.indexOf(ticks, start + ticks.length);
    if (end >= 0) return end + ticks.length;
  }
  const link = /^!?\[[^\]]*\]\([^)]+\)/.exec(text.slice(start));
  if (link) return start + link[0].length;
}

/** A complete {...} passage, distinct from links and slot conditions. */
export function textOnlyEnd(text: string, start: number): number | undefined {
  if (text[start] !== '{') return;
  let depth = 1;
  for (let i = start + 1; i < text.length; i++) {
    const literal = literalEnd(text, i);
    if (literal !== undefined) { i = literal - 1; continue; }
    if (text[i] === '{') depth++;
    if (text[i] !== '}' || --depth !== 0) continue;
    return i + 1;
  }
}

function textOnlySpans(text: string): {start: number; end: number}[] {
  const spans: {start: number; end: number}[] = [];
  for (let i = 0; i < text.length;) {
    const literal = literalEnd(text, i);
    if (literal !== undefined) { i = literal; continue; }
    const end = text[i] === '{' ? textOnlyEnd(text, i) : undefined;
    if (end !== undefined) { spans.push({start:i,end}); i = end; continue; }
    // An unfinished outer passage owns the rest of the text. Its nested openers
    // must not be reinterpreted as independent complete descriptions.
    if (text[i] === '{') break;
    i++;
  }
  return spans;
}

/** Browser item readings omit complete passages; the authored text stays intact. */
export function browserItemText(text: string): string {
  let result = '', start = 0;
  for (const span of textOnlySpans(text)) { result += text.slice(start,span.start); start = span.end; }
  return (result + text.slice(start)).trim();
}

/** These descriptions stand in for pictures already visible on the work surface. */
export function textOnlyPassages(text: string): string[] {
  return textOnlySpans(text).map(span=>text.slice(span.start+1,span.end-1).trim()).filter(Boolean);
}
