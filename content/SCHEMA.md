# Content schema

All hand-written content lives in `content/`. The build step (`tools/build.py`) bundles it
into the app, and `tools/validate.py` checks it.

## Topics

| key      | paper | name                              |
|----------|-------|-----------------------------------|
| number   | 1     | Number & arithmetic               |
| alg      | 1     | Algebra & functions               |
| graphs   | 1     | Graphs & transformations          |
| coord    | 1     | Coordinate geometry               |
| seq      | 1     | Sequences, series & binomial      |
| trig     | 1     | Trigonometry                      |
| explog   | 1     | Exponentials & logarithms         |
| diff     | 1     | Differentiation                   |
| integ    | 1     | Integration                       |
| geom     | 1     | Geometry & measures               |
| prob     | 1     | Probability & counting            |
| logic    | 2     | Logic of arguments                |
| proof    | 2     | Mathematical proof                |
| errors   | 2     | Finding errors in proofs          |

## Questions — `content/questions/<topic>.json`

A JSON array. Each item:

```json
{
  "id": "alg-07",
  "topic": "alg",
  "paper": 1,
  "difficulty": 3,
  "skills": ["discriminant", "parameters"],
  "stem": "Markdown. Inline maths $x^2$, display maths $$\\int_0^1 x\\,dx$$",
  "figure": null,
  "options": ["$-2$", "$-1$", "$0$", "$1$", "$2$"],
  "answer": 3,
  "solution": "Markdown, step by step, as a strong tutor would write it.",
  "insight": "One sentence: the key idea that cracks it.",
  "distractors": { "1": "Why a student picks B (the specific slip)." },
  "time": 150
}
```

* `paper` — 1 = Mathematical Thinking style, 2 = Mathematical Reasoning style.
* `difficulty` — 1 (warm-up) … 5 (hardest TMUA questions).
* `options` — 4 to 8 options (A–H). Each is a Markdown string **or** a plot object `{"plot": {...}}`.
* `answer` — 0-based index into `options`.
* `time` — sensible target seconds (TMUA average is 225 s per question).
* `figure` — `null`, a plot object `{"plot": {...}}`, or `{"svg": "<svg ...>...</svg>"}`
  (use `stroke="currentColor"` / `fill="currentColor"` so dark mode works; viewBox required).

### Plot object

```json
{"plot": {
  "x": [-3, 3], "y": [-2, 4],
  "curves": [{"fn": "x^2 - 1"}, {"fn": "2*sin(x)", "domain": [0, 6.28], "dash": true}],
  "points": [[1, 0]],
  "labels": [{"at": [1, 0], "text": "P"}],
  "vlines": [], "hlines": [],
  "ticks": false
}}
```

`fn` syntax: `x`, numbers, `+ - * / ^`, parentheses, `sin cos tan exp ln log10 sqrt abs floor`, `pi`, `e`.
Always write multiplication explicitly (`2*x`, not `2x`).

## Notes — `content/notes/<topic>.md`

Markdown with `$…$` / `$$…$$` maths. Structure:

```
# Title
Short intro: what TMUA actually asks about this.
## Must-know facts
## Techniques
## Traps
## Worked examples   (use <details><summary>Show solution</summary> ... </details>)
```

Blockquotes that begin with **Trap:**, **Tip:** or **Key idea:** render as coloured callouts.
