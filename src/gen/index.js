import algebra from './algebra.js';
import geometry from './geometry.js';
import series from './series.js';
import trig from './trig.js';
import calculus from './calculus.js';
import probability from './probability.js';
import logic from './logic.js';
import { makeRng } from '../lib/rng.js';
import { TOPIC } from '../data/topics.js';

export const GENERATORS = [...algebra, ...geometry, ...series, ...trig, ...calculus, ...probability, ...logic];
export const GEN = Object.fromEntries(GENERATORS.map(g => [g.id, g]));

// Generated question ids look like  g:<genId>:<level>:<seed>
export function genQuestion(genId, level, seed) {
  const g = GEN[genId];
  if (!g) return null;
  const lv = Math.max(g.levels[0], Math.min(g.levels[1], level));
  const q = g.make(makeRng(seed), lv);
  return {
    id: `g:${genId}:${lv}:${seed}`,
    gen: genId,
    topic: g.topic,
    paper: g.paper,
    difficulty: lv,
    skills: g.skills,
    figure: null,
    ...q,
    generated: true,
    genName: g.name,
  };
}

export function parseGenId(id) {
  const m = /^g:([\w-]+):(\d):(\d+)$/.exec(id);
  return m ? { genId: m[1], level: +m[2], seed: +m[3] } : null;
}

export const gensForTopic = topic => GENERATORS.filter(g => g.topic === topic && TOPIC[g.topic]);
