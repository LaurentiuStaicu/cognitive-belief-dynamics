/**
 * Canonical user-facing names shared by every view.
 *
 * Before 0.3.5a0 the four reference scenarios were named independently in
 * main.ts, comparison.ts and visual-stage.ts, so the same run appeared under
 * three different Romanian names. Views must import from here instead of
 * declaring their own copies.
 *
 * This module contains presentation strings only. It does not affect the
 * Python core, the exported runs or any numerical result.
 */
export type Lang = 'ro' | 'en';

/** Scenario identifiers exported by scripts/export_web.py. */
export type ScenarioId = 'repetition' | 'correction' | 'source' | 'accuracy';

const SCENARIO_NAMES: Record<ScenarioId, Record<Lang, string>> = {
  repetition: {ro: 'Repetiție simplă', en: 'Repetition only'},
  correction: {ro: 'Corecție și diminuarea accesibilității', en: 'Correction and accessibility decay'},
  source: {ro: 'Feedback despre sursă', en: 'Source feedback'},
  accuracy: {ro: 'Indiciu de acuratețe', en: 'Accuracy cue'}
};

/** Shorter forms for narrow controls; same concept, same order of words. */
const SCENARIO_SHORT_NAMES: Record<ScenarioId, Record<Lang, string>> = {
  repetition: {ro: 'Repetiție simplă', en: 'Repetition only'},
  correction: {ro: 'Corecție și diminuare', en: 'Correction and decay'},
  source: {ro: 'Feedback despre sursă', en: 'Source feedback'},
  accuracy: {ro: 'Indiciu de acuratețe', en: 'Accuracy cue'}
};

/** Guided routes through the computational map. Distinct from scenarios. */
const TOUR_NAMES: Record<ScenarioId, Record<Lang, string>> = {
  repetition: {ro: 'Traseul repetiției', en: 'Repetition route'},
  correction: {ro: 'Traseul corecției', en: 'Correction route'},
  source: {ro: 'Traseul sursei', en: 'Source route'},
  accuracy: {ro: 'Traseul acurateții', en: 'Accuracy route'}
};

export const scenarioName = (id: string, lang: Lang) =>
  SCENARIO_NAMES[id as ScenarioId]?.[lang] ?? id;

export const scenarioShortName = (id: string, lang: Lang) =>
  SCENARIO_SHORT_NAMES[id as ScenarioId]?.[lang] ?? id;

export const tourName = (id: string, lang: Lang) =>
  TOUR_NAMES[id as ScenarioId]?.[lang] ?? id;
