// Browser adapters to the preserved models. Rules and observations stay in the archive.
import * as bell from 'legacy/experiments/logical-bell-orchard.ts';
import * as bell2 from 'legacy/experiments/logical-bell-orchard-2.ts';
import * as mneme from 'legacy/experiments/logical-mneme.ts';
import * as mneme2 from 'legacy/experiments/logical-mneme-2.ts';

export const LOGICAL_GAMES = {
  bell: {id: 'bell', version: bell.BELL_VERSION, scenarios: bell.BELL_SCENARIO_IDS,
    create: bell.createBellOrchard, observe: bell.observeBellOrchard, step: bell.stepBellOrchard},
  bell2: {id: 'bell2', version: bell2.BELL2_VERSION, scenarios: bell2.BELL2_SCENARIO_IDS,
    create: bell2.createBellOrchard2, observe: bell2.observeBellOrchard2, step: bell2.stepBellOrchard2},
  mneme: {id: 'mneme', version: mneme.MNEME_VERSION, scenarios: mneme.SCENARIO_IDS,
    create: mneme.createMneme, observe: mneme.observeMneme, step: mneme.stepMneme},
  mneme2: {id: 'mneme2', version: mneme2.MNEME_VERSION, scenarios: mneme2.SCENARIO_IDS,
    create: mneme2.createMneme, observe: mneme2.observeMneme, step: mneme2.stepMneme},
};
