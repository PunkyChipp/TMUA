import { QUESTIONS, NOTES } from '../generated/content.js';
import { genQuestion, parseGenId, GENERATORS } from '../gen/index.js';
import { TOPIC, DEFAULT_TIME } from '../data/topics.js';

export const BANK = QUESTIONS.filter(q => TOPIC[q.topic]);
export const BY_ID = Object.fromEntries(BANK.map(q => [q.id, q]));
export const BY_TOPIC = {};
for (const q of BANK) (BY_TOPIC[q.topic] ||= []).push(q);
// Twin families: questions testing the same idea with different numbers and set-up.
export const FAMILY = {};
for (const q of BANK) if (q.family) (FAMILY[q.family] ||= []).push(q.id);
export const familyOf = q => (q?.family ? FAMILY[q.family] || [q.id] : q ? [q.id] : []);
export { NOTES };

export function getQuestion(id) {
  if (id.startsWith('g:')) {
    const p = parseGenId(id);
    return p ? genQuestion(p.genId, p.level, p.seed) : null;
  }
  return BY_ID[id] || null;
}

export const targetMs = q => 1000 * (q.time || DEFAULT_TIME[q.difficulty] || 200);

// SRS key: bank questions review themselves; generated ones review the skill (fresh variant).
export const srsKey = q => (q.gen ? `g:${q.gen}:${q.difficulty}` : q.family ? `f:${q.family}` : q.id);

export const bankStats = () => ({
  questions: BANK.length,
  generators: GENERATORS.length,
  byTopic: Object.fromEntries(Object.entries(BY_TOPIC).map(([k, v]) => [k, v.length])),
});
