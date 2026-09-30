// Topic taxonomy. `w1`/`w2` are rough shares of marks on Paper 1 / Paper 2,
// used for prioritising practice and for the predicted-score estimate.
export const TOPICS = [
  { key: 'number', name: 'Number & arithmetic', short: 'Number', paper: 1, w1: 0.06, w2: 0.03 },
  { key: 'alg', name: 'Algebra & functions', short: 'Algebra', paper: 1, w1: 0.16, w2: 0.07 },
  { key: 'graphs', name: 'Graphs & transformations', short: 'Graphs', paper: 1, w1: 0.11, w2: 0.06 },
  { key: 'coord', name: 'Coordinate geometry', short: 'Coordinates', paper: 1, w1: 0.08, w2: 0.03 },
  { key: 'seq', name: 'Sequences, series & binomial', short: 'Sequences', paper: 1, w1: 0.09, w2: 0.04 },
  { key: 'trig', name: 'Trigonometry', short: 'Trig', paper: 1, w1: 0.10, w2: 0.04 },
  { key: 'explog', name: 'Exponentials & logarithms', short: 'Exp & logs', paper: 1, w1: 0.08, w2: 0.03 },
  { key: 'diff', name: 'Differentiation', short: 'Differentiation', paper: 1, w1: 0.10, w2: 0.04 },
  { key: 'integ', name: 'Integration', short: 'Integration', paper: 1, w1: 0.09, w2: 0.04 },
  { key: 'geom', name: 'Geometry & measures', short: 'Geometry', paper: 1, w1: 0.07, w2: 0.02 },
  { key: 'prob', name: 'Probability & counting', short: 'Probability', paper: 1, w1: 0.06, w2: 0.02 },
  { key: 'logic', name: 'Logic of arguments', short: 'Logic', paper: 2, w1: 0, w2: 0.27 },
  { key: 'proof', name: 'Mathematical proof', short: 'Proof', paper: 2, w1: 0, w2: 0.18 },
  { key: 'errors', name: 'Finding errors in proofs', short: 'Errors in proofs', paper: 2, w1: 0, w2: 0.13 },
];

export const TOPIC = Object.fromEntries(TOPICS.map(t => [t.key, t]));

// Weight of a topic across the whole test.
export const topicWeight = key => (TOPIC[key].w1 + TOPIC[key].w2) / 2;

// Difficulty levels on the logit scale used by the ability model.
export const LEVEL_B = { 1: -1.6, 2: -0.8, 3: 0, 4: 0.8, 5: 1.6 };

// TMUA: 20 questions in 75 minutes.
export const EXAM = { questions: 20, minutes: 75, perQ: 225 };

// Default target seconds by difficulty when a question does not state one.
export const DEFAULT_TIME = { 1: 90, 2: 140, 3: 200, 4: 260, 5: 320 };

export const PAST_PAPERS = [
  'Specimen', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023',
];
export const PREP_URL = 'https://esat-tmua.ac.uk/tmua-preparation-materials/';
