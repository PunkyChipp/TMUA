import { choices, num } from './helpers.js';

const isPrime = n => { if (n < 2) return false; for (let d = 2; d * d <= n; d++) if (n % d === 0) return false; return true; };
const digitSum = n => String(n).split('').reduce((s, c) => s + +c, 0);

// Conditions on a positive integer n.
const INT_PREDS = [
  { t: '$n$ is even', f: n => n % 2 === 0 },
  { t: '$n$ is odd', f: n => n % 2 === 1 },
  { t: '$n$ is a multiple of $3$', f: n => n % 3 === 0 },
  { t: '$n$ is a multiple of $4$', f: n => n % 4 === 0 },
  { t: '$n$ is a multiple of $6$', f: n => n % 6 === 0 },
  { t: '$n$ is a multiple of $12$', f: n => n % 12 === 0 },
  { t: '$n^2$ is a multiple of $4$', f: n => (n * n) % 4 === 0 },
  { t: '$n^2$ is a multiple of $8$', f: n => (n * n) % 8 === 0 },
  { t: '$n^2$ is a multiple of $9$', f: n => (n * n) % 9 === 0 },
  { t: '$n^2 - 1$ is a multiple of $8$', f: n => (n * n - 1) % 8 === 0 },
  { t: '$n$ is prime', f: isPrime },
  { t: '$n$ is a multiple of $10$', f: n => n % 10 === 0 },
  { t: 'the last digit of $n$ is $0$ or $5$', f: n => n % 5 === 0 },
  { t: 'the digit sum of $n$ is a multiple of $9$', f: n => digitSum(n) % 9 === 0 },
  { t: '$n(n+1)$ is a multiple of $4$', f: n => (n * (n + 1)) % 4 === 0 },
  { t: '$n^3$ is even', f: n => (n ** 3) % 2 === 0 },
];

// Conditions on a real x (checked on a fine grid that includes all boundary points used).
const REAL_PREDS = [
  { t: '$x > 2$', f: x => x > 2 },
  { t: '$x \\ge 2$', f: x => x >= 2 },
  { t: '$x^2 > 4$', f: x => x * x > 4 },
  { t: '$x^3 > 8$', f: x => x ** 3 > 8 },
  { t: '$|x| < 1$', f: x => Math.abs(x) < 1 },
  { t: '$x^2 < 1$', f: x => x * x < 1 },
  { t: '$x > 0$', f: x => x > 0 },
  { t: '$x^2 > x$', f: x => x * x > x },
  { t: '$x > 1$', f: x => x > 1 },
  { t: '$0 < x < 1$', f: x => x > 0 && x < 1 },
  { t: '$x^2 < x$', f: x => x * x < x },
  { t: '$x^2 \\ge 4$', f: x => x * x >= 4 },
];

const INTS = Array.from({ length: 5000 }, (_, i) => i + 1);
const REALS = Array.from({ length: 161 }, (_, i) => -10 + i / 8);

function relation(P, Q, domain) {
  let pq = null, qp = null; // counterexamples to P=>Q and Q=>P
  for (const v of domain) {
    if (pq === null && P.f(v) && !Q.f(v)) pq = v;
    if (qp === null && Q.f(v) && !P.f(v)) qp = v;
    if (pq !== null && qp !== null) break;
  }
  return { suff: pq === null, nec: qp === null, pq, qp };
}

const NS_OPTS = [
  { key: 'nec', text: '(P) is necessary but not sufficient for (Q)' },
  { key: 'suff', text: '(P) is sufficient but not necessary for (Q)' },
  { key: 'both', text: '(P) is necessary and sufficient for (Q)' },
  { key: 'neither', text: '(P) is neither necessary nor sufficient for (Q)' },
];

const fmtV = v => (Number.isInteger(v) ? String(v) : (v * 8) % 1 === 0 ? `${v}` : v.toFixed(3));

const necSuff = {
  id: 'nec-suff', topic: 'logic', paper: 2, levels: [2, 4], skills: ['necessary and sufficient'],
  name: 'Necessary or sufficient?',
  make(rng, level) {
    const real = level >= 3 && rng.chance(0.5);
    const preds = real ? REAL_PREDS : INT_PREDS;
    const domain = real ? REALS : INTS;
    const want = rng.pick(['nec', 'suff', 'both', 'neither', 'nec', 'suff']);
    let P, Q, rel, key, guard = 0;
    do {
      P = rng.pick(preds); Q = rng.pick(preds);
      if (P === Q) continue;
      rel = relation(P, Q, domain);
      key = rel.nec && rel.suff ? 'both' : rel.nec ? 'nec' : rel.suff ? 'suff' : 'neither';
    } while ((P === Q || key !== want) && guard++ < 400);
    if (P === Q || !rel) { P = preds[0]; Q = preds[2]; rel = relation(P, Q, domain); key = rel.nec && rel.suff ? 'both' : rel.nec ? 'nec' : rel.suff ? 'suff' : 'neither'; }
    const why = {
      nec: 'Necessary means (Q) ⇒ (P). Sufficient means (P) ⇒ (Q). You have them the wrong way round.',
      suff: 'Necessary means (Q) ⇒ (P). Sufficient means (P) ⇒ (Q). You have them the wrong way round.',
      both: 'Test both directions: find a value that satisfies one condition but not the other.',
      neither: 'One of the implications does hold. Try to find a counterexample and notice when you cannot.',
    };
    const opts = NS_OPTS.map(o => ({ ...o, why: why[o.key] }));
    const correct = opts.find(o => o.key === key);
    const ch = choices(rng, correct, opts.filter(o => o !== correct), { n: 4 });
    // Keep the canonical order A–D.
    const order = NS_OPTS.map(o => o.text);
    const distractors = {};
    order.forEach((t, i) => { if (i !== order.indexOf(correct.text)) distractors[i] = why[NS_OPTS[i].key]; });
    void ch;
    const v = real ? 'x' : 'n';
    const line1 = rel.suff ? `(P) ⇒ (Q) holds: whenever ${P.t}, also ${Q.t}. So (P) **is sufficient**.` : `(P) ⇒ (Q) fails: $${v} = ${fmtV(rel.pq)}$ satisfies (P) but not (Q). So (P) is **not sufficient**.`;
    const line2 = rel.nec ? `(Q) ⇒ (P) holds: whenever ${Q.t}, also ${P.t}. So (P) **is necessary**.` : `(Q) ⇒ (P) fails: $${v} = ${fmtV(rel.qp)}$ satisfies (Q) but not (P). So (P) is **not necessary**.`;
    return {
      stem: `Let $${v}$ be ${real ? 'a real number' : 'a positive integer'}. Consider the conditions\n\n(P) ${P.t}\n\n(Q) ${Q.t}\n\nWhich one of the following is true?`,
      options: order,
      answer: order.indexOf(correct.text),
      distractors,
      solution: `- ${line1}\n- ${line2}`,
      insight: '"P is sufficient for Q" means P ⇒ Q; "P is necessary for Q" means Q ⇒ P. Test each direction with a counterexample hunt.',
      time: 120,
    };
  },
};

const THEMES = [
  { noun: 'card', rel: 'that', A: ['has a vowel on one side', 'does not have a vowel on one side'], Q: ['has an even number on the other side', 'does not have an even number on the other side'] },
  { noun: 'student in the class', rel: 'who', A: ['revised', 'did not revise'], Q: ['passed', 'did not pass'] },
  { noun: 'positive integer', rel: 'that', A: ['is prime', 'is not prime'], Q: ['is odd', 'is not odd'] },
  { noun: 'train on this line', rel: 'that', A: ['leaves before 9am', 'does not leave before 9am'], Q: ['stops at York', 'does not stop at York'] },
  { noun: 'quadrilateral in the diagram', rel: 'that', A: ['has four equal sides', 'does not have four equal sides'], Q: ['is a square', 'is not a square'] },
  { noun: 'player in the team', rel: 'who', A: ['trained on Monday', 'did not train on Monday'], Q: ['played on Saturday', 'did not play on Saturday'] },
];

const every = (T, a, q) => `Every ${T.noun} ${T.rel} ${a} ${q}.`;
const some = (T, a, q) => `There is a ${T.noun} ${T.rel} ${a} and ${q}.`;

const negation = {
  id: 'negate-contrapositive', topic: 'logic', paper: 2, levels: [2, 3], skills: ['negation', 'contrapositive', 'quantifiers'],
  name: 'Negation and contrapositive',
  make(rng, level) {
    const T = rng.pick(THEMES);
    const [Ap, An] = T.A, [Qp, Qn] = T.Q;
    const kind = rng.pick(level >= 3 ? ['neg', 'equiv', 'negSome'] : ['neg', 'equiv']);
    const S = kind === 'negSome' ? some(T, Ap, Qp) : every(T, Ap, Qp);
    let correct, w, ask, sol;
    if (kind === 'neg') {
      ask = 'Which one of the following is the negation of this statement?';
      correct = { key: 'n', text: some(T, Ap, Qn) };
      w = [
        { key: 'c', text: every(T, Ap, Qn), why: 'Too strong: to show "every … " is false you need only one exception, not for all of them to fail.' },
        { key: 'i', text: every(T, An, Qn), why: 'That is the inverse, which is a different statement, not the negation.' },
        { key: 's', text: some(T, An, Qp), why: 'An exception must satisfy the hypothesis and fail the conclusion.' },
        { key: 'b', text: some(T, Ap, Qp), why: 'That is consistent with the original statement being true.' },
      ];
      sol = `"Every X ${T.rel} is A is Q" is false exactly when there is at least one X that is A but not Q.\n\nNegation: *${correct.text}*`;
    } else if (kind === 'equiv') {
      ask = 'Which one of the following is logically equivalent to this statement?';
      correct = { key: 'cp', text: every(T, Qn, An) };
      w = [
        { key: 'cv', text: every(T, Qp, Ap), why: 'That is the converse, which can be false when the original is true.' },
        { key: 'i', text: every(T, An, Qn), why: 'That is the inverse, which is equivalent to the converse, not to the original.' },
        { key: 'n', text: some(T, Ap, Qn), why: 'That is the negation.' },
        { key: 'c', text: every(T, Ap, Qn), why: 'That contradicts the original (unless there are no such objects).' },
      ];
      sol = `"If A then Q" is equivalent to its **contrapositive** "if not Q then not A".\n\nSo: *${correct.text}*\n\nThe converse ("if Q then A") and the inverse ("if not A then not Q") are equivalent to each other, not to the original.`;
    } else {
      ask = 'Which one of the following is the negation of this statement?';
      correct = { key: 'n', text: every(T, Ap, Qn) };
      w = [
        { key: 's', text: some(T, Ap, Qn), why: 'That can be true at the same time as the original; the negation must say it never happens.' },
        { key: 'i', text: some(T, An, Qn), why: 'Negate the whole statement: no object is both A and Q.' },
        { key: 'e', text: every(T, An, Qn), why: 'That says nothing about the objects that are A.' },
        { key: 'x', text: every(T, Ap, Qp), why: 'That is stronger than the original, not its negation.' },
      ];
      sol = `"There is an X that is A and Q" is false exactly when **no** X that is A is Q, i.e. every X that is A is not Q.\n\nNegation: *${correct.text}*`;
    }
    const opts = choices(rng, correct, w, { n: 5 });
    return {
      stem: `Consider the statement:\n\n> ${S}\n\n${ask}`,
      ...opts,
      solution: sol,
      insight: 'not (every A is Q) = some A is not Q; "if A then Q" ≡ "if not Q then not A".',
      time: 90,
    };
  },
};

// Claims about positive integers, for counterexample questions.
const CLAIMS = [
  { t: 'For every positive integer $n$, $n^2 + n + 41$ is prime.', hyp: () => true, ok: n => isPrime(n * n + n + 41), range: [1, 50], note: n => `$${n}^2 + ${n} + 41 = ${n * n + n + 41}$` },
  { t: 'For every positive integer $n$, $n^2 - n + 11$ is prime.', hyp: () => true, ok: n => isPrime(n * n - n + 11), range: [1, 16], note: n => `$${n}^2 - ${n} + 11 = ${n * n - n + 11}$` },
  { t: 'If $p$ is prime, then $2^p - 1$ is prime.', hyp: isPrime, ok: n => isPrime(2 ** n - 1), range: [2, 13], v: 'p', note: n => `$2^{${n}} - 1 = ${2 ** n - 1}$` },
  { t: 'If $n$ is odd, then $n^2 + 4$ is prime.', hyp: n => n % 2 === 1, ok: n => isPrime(n * n + 4), range: [1, 13], note: n => `$${n}^2 + 4 = ${n * n + 4}$` },
  { t: 'If $n$ is prime, then $n + 2$ or $n + 4$ is prime.', hyp: isPrime, ok: n => isPrime(n + 2) || isPrime(n + 4), range: [2, 40], note: n => `$${n + 2}$ and $${n + 4}$` },
  { t: 'If $n$ is a multiple of $3$, then $n^2 + 1$ is prime.', hyp: n => n % 3 === 0, ok: n => isPrime(n * n + 1), range: [3, 30], note: n => `$${n}^2 + 1 = ${n * n + 1}$` },
  { t: 'If $n > 1$, then $n! + 1$ is prime.', hyp: n => n > 1, ok: n => { let f = 1; for (let i = 2; i <= n; i++) f *= i; return isPrime(f + 1); }, range: [2, 7], note: n => { let f = 1; for (let i = 2; i <= n; i++) f *= i; return `$${n}! + 1 = ${f + 1}$`; } },
];

const factorStr = m => { const fs = []; let x = m; for (let d = 2; d * d <= x; d++) while (x % d === 0) { fs.push(d); x /= d; } if (x > 1) fs.push(x); return fs.join('\\times '); };

const counterexample = {
  id: 'counterexample', topic: 'proof', paper: 2, levels: [2, 3], skills: ['counterexamples'],
  name: 'Find the counterexample',
  make(rng, level) {
    let C, ce, fine, guard = 0;
    do {
      C = rng.pick(CLAIMS);
      const vals = []; for (let n = C.range[0]; n <= C.range[1]; n++) vals.push(n);
      ce = vals.filter(n => C.hyp(n) && !C.ok(n));
      fine = vals.filter(n => !(C.hyp(n) && !C.ok(n)));
    } while ((ce.length === 0 || fine.length < 4) && guard++ < 50);
    const v = C.v || 'n';
    const answer = rng.pick(ce);
    const others = rng.shuffle(fine).slice(0, 4);
    const all = [answer, ...others].sort((a, b) => a - b);
    const distractors = {};
    all.forEach((n, i) => {
      if (n === answer) return;
      distractors[i] = C.hyp(n) ? `For $${v} = ${n}$ the claim holds (${C.note(n)} is fine), so it is not a counterexample.` : `$${v} = ${n}$ does not satisfy the hypothesis, so it cannot be a counterexample.`;
    });
    const valAt = C.note(answer);
    return {
      stem: `Consider the claim:\n\n> ${C.t}\n\nWhich of the following values of $${v}$ gives a counterexample to the claim?`,
      options: all.map(n => `$${v} = ${n}$`),
      answer: all.indexOf(answer),
      distractors,
      solution: `A counterexample must satisfy the hypothesis but make the conclusion false.\n\nFor $${v} = ${answer}$: ${valAt}${/= (\d+)\$$/.test(valAt) ? `, and $${valAt.match(/= (\d+)\$$/)[1]} = ${factorStr(+valAt.match(/= (\d+)\$$/)[1])}$ is not prime` : ', and neither is prime'}.\n\nEach of the other values either fails the hypothesis or satisfies the conclusion.`,
      insight: 'A counterexample to "if P then Q" must make P true and Q false; a value where P is false proves nothing.',
      time: 100,
    };
  },
};

export default [necSuff, negation, counterexample];
