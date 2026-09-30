// Day-by-day plan to the exam, recomputed from the live model so it follows
// your weaknesses. Finished tasks are remembered by id.
import { TOPIC, PAST_PAPERS } from '../data/topics.js';
import { priorities } from './model.js';
import { dueReviews } from '../lib/store.js';
import { dateKey, addDays, daysBetween } from '../lib/util.js';

// Official papers, oldest first; the newest are saved for the final days.
const OFFICIAL = PAST_PAPERS.filter(p => p !== 'Specimen').flatMap(y => [`${y}:1`, `${y}:2`]);

export function phaseOf(left) {
  if (left < 0) return { key: 'done', name: 'Test taken' };
  if (left === 0) return { key: 'exam', name: 'Test day' };
  if (left === 1) return { key: 'taper', name: 'Taper' };
  if (left <= 3) return { key: 'simulate', name: 'Exam simulation' };
  if (left <= 9) return { key: 'sharpen', name: 'Sharpen' };
  return { key: 'build', name: 'Build' };
}

export function buildPlan(state, model, today = dateKey()) {
  const exam = state.settings.examDate;
  const days = [];
  const total = daysBetween(today, exam);
  if (total < 0) return { days, total, exam };
  const pri = priorities(model).map(p => p.key);
  const learned = new Set(Object.keys(state.learned || {}));
  const learnQueue = pri.filter(k => !learned.has(k)).concat(pri.filter(k => learned.has(k)));
  const logged = new Set(state.papers.map(p => `${p.year}:${p.paper}`));
  const papers = OFFICIAL.filter(p => !logged.has(p));
  let paperIdx = 0;
  let learnIdx = 0;
  const due = dueReviews().length;
  const diagDone = !!state.diag;

  for (let i = 0; i <= total; i++) {
    const key = addDays(today, i);
    const left = total - i;
    const phase = phaseOf(left);
    const tasks = [];
    const add = t => tasks.push(t);
    if (i === 0 && !diagDone) add({ id: 'diag', kind: 'diagnostic', title: 'Diagnostic test', detail: '16 questions across every topic. Seeds your plan.', mins: 45 });

    const nextLearn = () => learnQueue[learnIdx++ % learnQueue.length];
    const nextPaper = () => (paperIdx < papers.length ? papers[paperIdx++] : null);
    const pastTask = p => {
      const [year, paper] = p.split(':');
      return { id: `past:${p}`, kind: 'past', year, paper: +paper, title: `Official ${year} Paper ${paper}`, detail: 'Timed, 75 minutes, then log your score and mark every mistake.', mins: 100 };
    };

    if (phase.key === 'build') {
      const t1 = nextLearn(), t2 = nextLearn();
      add({ id: `learn:${t1}`, kind: 'learn', topic: t1, title: `Learn: ${TOPIC[t1].name}`, detail: 'Read the notes, then do the worked examples yourself.', mins: 20 });
      add({ id: `drill:${t1}`, kind: 'drill', topic: t1, title: `Drill: ${TOPIC[t1].short}`, detail: '10 questions pitched at your level.', mins: 30 });
      if (left % 3 === 1 && papers.length) { const p = nextPaper(); if (p) add(pastTask(p)); }
      else {
        add({ id: `learn:${t2}`, kind: 'learn', topic: t2, title: `Learn: ${TOPIC[t2].name}`, detail: 'Notes and worked examples.', mins: 20 });
        add({ id: `drill:${t2}`, kind: 'drill', topic: t2, title: `Drill: ${TOPIC[t2].short}`, detail: '10 questions.', mins: 30 });
      }
      add({ id: 'smart', kind: 'smart', title: 'Smart practice', detail: '15 mixed questions chosen for you.', mins: 45 });
    } else if (phase.key === 'sharpen') {
      const t1 = nextLearn();
      add({ id: `drill:${t1}`, kind: 'drill', topic: t1, title: `Drill: ${TOPIC[t1].short}`, detail: 'Your weakest area right now.', mins: 30 });
      if (left % 2 === 0) { const p = nextPaper(); add(p ? pastTask(p) : { id: 'mock:1', kind: 'mock', paper: 1, title: 'Mock Paper 1', detail: '20 questions, 75 minutes.', mins: 90 }); }
      else add({ id: 'timed', kind: 'timed', title: 'Timed set', detail: '10 questions in 37½ minutes: exam pace.', mins: 40 });
      add({ id: 'smart', kind: 'smart', title: 'Smart practice', detail: '15 mixed questions.', mins: 45 });
    } else if (phase.key === 'simulate') {
      const p = nextPaper();
      add(p ? pastTask(p) : { id: `mock:${left % 2 ? 1 : 2}`, kind: 'mock', paper: left % 2 ? 1 : 2, title: `Mock Paper ${left % 2 ? 1 : 2}`, detail: '20 questions, 75 minutes.', mins: 90 });
      add({ id: `mock:${left % 2 ? 2 : 1}`, kind: 'mock', paper: left % 2 ? 2 : 1, title: `Mock Paper ${left % 2 ? 2 : 1}`, detail: 'Back-to-back with a short break, like the real thing.', mins: 90 });
    } else if (phase.key === 'taper') {
      add({ id: 'read:strategy', kind: 'read', note: 'strategy', title: 'Read: exam strategy', detail: 'Timing, guessing and what to do when stuck.', mins: 15 });
      add({ id: 'read:facts', kind: 'read', note: 'facts', title: 'Read: facts to know cold', detail: 'One pass, no cramming.', mins: 20 });
      add({ id: 'timed', kind: 'timed', title: 'Light timed set', detail: '10 questions to keep your eye in. Then stop.', mins: 40 });
    } else if (phase.key === 'exam') {
      add({ id: 'warmup', kind: 'smart', n: 4, title: 'Warm-up', detail: 'Four quick questions, an hour or so before you leave.', mins: 10 });
    }
    if (phase.key !== 'exam' && (i === 0 ? due > 0 : true) && phase.key !== 'taper') {
      add({ id: 'review', kind: 'review', title: 'Mistake review', detail: i === 0 ? `${due} item${due === 1 ? '' : 's'} due` : 'Anything due from spaced repetition.', mins: 15 });
    }
    const done = new Set(state.plan[key] || []);
    days.push({ key, left, phase, tasks: tasks.map(t => ({ ...t, done: done.has(t.id) })) });
  }
  return { days, total, exam };
}
