import {workshop} from './adventure.ts';

// Exercise several arrivals in one frame, inherited pictures, and a skipped chapter.
export const terminalStory=workshop
  .replace('## Make a case', '## Opening\nbackground: ![Workshop](opening.svg)\nThe workshop opens.\n\n## Make a case\nbackground: ![Bench](bench.svg)')
  .replace('## Dispatch', '## Already ready\nbackground: ![Never entered](skipped.svg)\n[If skipped] The closed case is already ready.\n**Goals**\n- Already closed -- Case[Lid]\n\n## Dispatch');
