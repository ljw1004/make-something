// Appended to the original reader's rendering functions by build-prototypes.mjs.
import {LOGICAL_GAMES, createLogicalRun, logicalAct, replayLogical} from './text-runner.ts';

const gameId = new URLSearchParams(location.search).get('game') || 'bell2';
const game = Object.hasOwn(LOGICAL_GAMES, gameId) ? LOGICAL_GAMES[gameId] : null;
let run = null;

function start() {
  $('error').textContent = '';
  if (!game) {
    $('title').textContent = 'Unknown prototype';
    $('error').textContent = 'Choose Bell Orchard or Mneme from the prototype collection.';
    return;
  }
  try {
    run = createLogicalRun(game, crypto.randomUUID(), game.scenarios[0], 0, 'manual static story play');
    session = {id: run.id, game: game.id};
    $('story').replaceChildren();
    render(game.observe(replayLogical(run)));
    document.title = $('title').textContent + ' · Prototypes';
  } catch (error) {
    $('error').textContent = error.message;
  }
}

function act(action) {
  if (busy || !run) return;
  busy = true;
  $('error').textContent = '';
  try {
    const result = logicalAct(run, action);
    run = result.run;
    render(game.observe(result.state), action);
  } catch (error) {
    $('error').textContent = error.message;
  } finally {
    busy = false;
  }
}

$('restart').onclick = start;
$('download').onclick = () => {
  if (!run) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(run, null, 2)], {type: 'application/json'}));
  const link = document.createElement('a');
  link.href = url;
  link.download = run.game + '-run.json';
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};
start();
