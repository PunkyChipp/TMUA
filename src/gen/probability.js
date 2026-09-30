import { choices, num, nearFill, F, binom } from './helpers.js';

const fact = n => (n <= 1 ? 1 : n * fact(n - 1));

const DICE_EVENTS = [
  { t: s => `the total is ${s}`, par: () => [5, 6, 7, 8, 9], f: s => (a, b) => a + b === s },
  { t: s => `the total is at least ${s}`, par: () => [8, 9, 10], f: s => (a, b) => a + b >= s },
  { t: () => 'the product of the scores is even', par: () => [0], f: () => (a, b) => (a * b) % 2 === 0, why: 'P(product even) is 1 − P(both odd) = 1 − ¼, not ½.' },
  { t: () => 'the product of the scores is a multiple of 3', par: () => [0], f: () => (a, b) => (a * b) % 3 === 0 },
  { t: () => 'at least one six is shown', par: () => [0], f: () => (a, b) => a === 6 || b === 6, why: 'Adding ⅙ + ⅙ double-counts the double six.' },
  { t: d => `the scores differ by exactly ${d}`, par: () => [1, 2, 3], f: d => (a, b) => Math.abs(a - b) === d },
  { t: m => `the larger score is ${m}`, par: () => [3, 4, 5, 6], f: m => (a, b) => Math.max(a, b) === m },
  { t: () => 'the total is a prime number', par: () => [0], f: () => (a, b) => [2, 3, 5, 7, 11].includes(a + b) },
];

const dice = {
  id: 'two-dice', topic: 'prob', paper: 1, levels: [1, 2], skills: ['sample spaces', 'probability'],
  name: 'Two dice',
  make(rng, level) {
    const ev = rng.pick(DICE_EVENTS);
    const par = rng.pick(ev.par());
    const f = ev.f(par);
    let count = 0, unordered = 0;
    for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) { if (f(a, b)) { count++; if (a <= b) unordered++; } }
    const p = F(count, 36);
    const w = [
      num(F(unordered, 21), 'The 21 unordered pairs are not equally likely: (1, 2) and (2, 1) are different outcomes.'),
      num(F(36 - count, 36), 'That is the probability of the complement.'),
      num(F(count + 1, 36)), num(F(Math.max(0, count - 1), 36)),
    ];
    if (ev.why) w.unshift(num(ev.t(0).includes('six') ? F(1, 3) : F(1, 2), ev.why));
    const opts = choices(rng, num(p), w, { n: 5, sort: true, fill: nearFill(p, 3) });
    const list = [];
    for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) if (f(a, b)) list.push(`(${a},${b})`);
    return {
      stem: `Two fair six-sided dice are rolled. What is the probability that ${ev.t(par)}?`,
      ...opts,
      solution: `There are $36$ equally likely ordered outcomes. The favourable ones${list.length <= 12 ? ` are ${list.join(', ')}` : ''}: $${count}$ of them.\n\nProbability $= \\dfrac{${count}}{36}${p.d === 36 ? '' : ` = ${p.tex()}`}$.`,
      insight: 'List ordered outcomes in a 6 × 6 grid; unordered pairs are not equally likely.',
      time: 70,
    };
  },
};

const bag = {
  id: 'bag-no-replace', topic: 'prob', paper: 1, levels: [2, 3], skills: ['without replacement', 'tree diagrams'],
  name: 'Drawing without replacement',
  make(rng, level) {
    const r = rng.int(2, 7), b = rng.int(2, 7), n = r + b;
    const kind = rng.pick(['same', 'atleast', 'exactly']);
    const RR = F(r * (r - 1), n * (n - 1)), BB = F(b * (b - 1), n * (n - 1)), RB = F(2 * r * b, n * (n - 1));
    const ans = kind === 'same' ? RR.add(BB) : kind === 'atleast' ? F(1).sub(BB) : RB;
    const withRep = kind === 'same' ? F(r * r + b * b, n * n) : kind === 'atleast' ? F(1).sub(F(b * b, n * n)) : F(2 * r * b, n * n);
    const w = [
      num(withRep, 'That assumes replacement: after the first draw there are ' + (n - 1) + ' counters left.'),
      kind === 'same' ? num(RR, 'Both blue also counts as the same colour.') : kind === 'exactly' ? num(F(r * b, n * (n - 1)), 'Red then blue, or blue then red: two orders.') : num(F(r, n), 'P(at least one red) = 1 − P(both blue).'),
      kind === 'atleast' ? num(RB, 'That is exactly one red; at least one red also includes two reds.') : num(F(1).sub(ans), 'That is the complement.'),
    ];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 4) });
    const what = { same: 'both counters are the same colour', atleast: 'at least one counter is red', exactly: 'exactly one counter is red' }[kind];
    return {
      stem: `A bag contains ${r} red counters and ${b} blue counters. Two counters are taken at random, without replacement. What is the probability that ${what}?`,
      ...opts,
      solution: `P(RR) $= \\dfrac{${r}}{${n}}\\times\\dfrac{${r - 1}}{${n - 1}} = ${RR.tex()}$, P(BB) $= \\dfrac{${b}}{${n}}\\times\\dfrac{${b - 1}}{${n - 1}} = ${BB.tex()}$, P(one of each) $= 2\\times\\dfrac{${r}}{${n}}\\times\\dfrac{${b}}{${n - 1}} = ${RB.tex()}$.\n\n${kind === 'same' ? `Same colour $= ${RR.tex()} + ${BB.tex()}` : kind === 'atleast' ? `At least one red $= 1 - ${BB.tex()}` : `Exactly one red $= ${RB.tex()}`} = ${ans.tex()}$.`,
      insight: 'Without replacement the second fraction changes; "at least one" is 1 minus "none".',
      time: 110,
    };
  },
};

const WORDS = ['LEVEL', 'BANANA', 'LETTER', 'COFFEE', 'PEPPER', 'ALGEBRA', 'CALCULUS', 'SEQUENCE', 'TOFFEE', 'MAMMAL'];

const arrange = {
  id: 'arrangements', topic: 'prob', paper: 1, levels: [2, 3], skills: ['permutations', 'counting'],
  name: 'Arrangements',
  make(rng, level) {
    if (level >= 3 || rng.chance(0.4)) {
      const n = rng.int(5, 7);
      const together = rng.chance(0.5);
      const tog = 2 * fact(n - 1);
      const ans = together ? tog : fact(n) - tog;
      const w = [num(together ? fact(n - 1) : fact(n) - fact(n - 1), 'The pair can sit in either order: multiply by 2.'), num(together ? fact(n) - tog : tog, together ? 'That counts arrangements where they are apart.' : 'That counts arrangements where they sit together.'), num(fact(n)), num(together ? 2 * fact(n - 2) : fact(n) - 2 * fact(n - 2))];
      const opts = choices(rng, num(ans), w, { n: 5, sort: true });
      return {
        stem: `${n} people, including Ana and Ben, sit in a row of ${n} chairs. In how many arrangements do Ana and Ben sit ${together ? 'next to each other' : '**not** next to each other'}?`,
        ...opts,
        solution: `Glue Ana and Ben into one block: $${n - 1}$ units in $${n - 1}! = ${fact(n - 1)}$ orders, times $2$ for the order inside the block: $${tog}$ arrangements together.${together ? '' : `\n\nTotal arrangements $${n}! = ${fact(n)}$, so apart: $${fact(n)} - ${tog} = ${ans}$.`}`,
        insight: 'Together: treat the pair as one block (and multiply by its internal orders). Apart: total minus together.',
        time: 90,
      };
    }
    const word = rng.pick(WORDS);
    const counts = {};
    for (const ch of word) counts[ch] = (counts[ch] || 0) + 1;
    const denom = Object.values(counts).reduce((p, c) => p * fact(c), 1);
    const ans = fact(word.length) / denom;
    const w = [num(fact(word.length), 'Identical letters give identical arrangements: divide by the repeats.'), num(fact(word.length) / Math.max(...Object.values(counts).map(fact)), 'Divide by the factorial of every repeated letter, not just one.'), num(ans * 2)];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, Math.max(5, ans / 4 | 0)) });
    const reps = Object.entries(counts).filter(([, c]) => c > 1);
    return {
      stem: `How many different arrangements are there of the letters of the word **${word}**?`,
      ...opts,
      solution: `${word.length} letters, with repeats ${reps.map(([ch, c]) => `${ch}×${c}`).join(', ')}.\n\n$$\\frac{${word.length}!}{${reps.map(([, c]) => c + '!').join('\\,')}} = \\frac{${fact(word.length)}}{${denom}} = ${ans}.$$`,
      insight: 'n! over the product of factorials of the repeat counts.',
      time: 80,
    };
  },
};

export default [dice, bag, arrange];
export { binom };
