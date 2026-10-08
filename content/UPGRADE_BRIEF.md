# Upgrade brief: October 2026 readiness + twins

The bank must be ready for the October 2026 TMUA, at real-paper difficulty, in the current style.
Read first: `content/SPEC_2026.md` (official spec digest: rules you must not break),
`content/SCHEMA.md`, `content/AUTHORING_BRIEF.md` (quality bar, verification rules).

## Part A: audit and upgrade every existing question in your topic files
For each question decide KEEP / REVISE / REPLACE:
* REPLACE anything off-spec (see SPEC_2026 exclusions: change of base, inflexion as the point of the
  question, symbolic logic notation in stems/options, formal truth tables, unstated sphere/cone/
  pyramid formulae, etc.) and anything too routine for the TMUA (one-step textbook recall).
* REVISE wording to current style: precise, unambiguous, exam-like; the stem must state every
  convention it relies on. About a third of each topic should use a short applied/scenario framing
  where natural (a rate, a game, a design constraint, a data context), not artificially.
* OPTIONS: five options (A–E) is the norm. Use 6–8 only for "which of I, II, III" combination
  questions or where the structure genuinely needs it. Numeric options stay ascending. Every
  distractor must be the result of a specific, plausible slip, explained in `distractors`
  (cover at least 3 wrong options).
* DIFFICULTY: no difficulty 1. Target spread per 18 originals: d2 ×2, d3 ×6, d4 ×6, d5 ×4
  (logic's 24: d2 ×2, d3 ×8, d4 ×8, d5 ×6). Calibrate to real papers: a d3 is a typical mid-paper
  TMUA question (2–3 ideas chained, ~3–4 min), d5 is among the hardest questions on a paper.
* Cover the spec items listed for your topics below that the bank currently misses.
* Keep ids stable for kept/revised questions; a replaced question keeps its id (same topic slot).

## Part B: write a twin for every question
For every question `X` (after Part A) write a twin with id `Xb`:
* Same skill and same difficulty, but a genuinely different question: different numbers AND a
  different surface (different function, configuration, context, or statements), so knowing
  X's answer gives nothing away. Not a copy with one number changed.
* Its correct answer must be at a DIFFERENT option letter from X's.
* Full independent solution, insight and distractor notes, same quality bar.
* Add `"family": "X"` to BOTH X and Xb.
The app uses twins for spaced-repetition reviews: when a student gets X wrong, the review shows
Xb (and vice versa), so they relearn the method instead of memorising an answer.

## Verification (mandatory, as in AUTHORING_BRIEF)
Machine-check every original and every twin (sympy / brute force / truth-table checker) in
`content/checks/<topic>_check.py`; it must assert every key, that no other option is also correct,
and print ALL OK. Then run `node tools/validate.mjs <topics>`: it must report 0 errors.
Regenerate the JSON with a Python script (json.dump ensure_ascii=False, indent=1).
Update `content/notes/<topic>.md` so it matches the spec (remove/flag anything not examined,
add short sections for newly covered spec items).

Reply with: per topic, the count kept/revised/replaced (with one-line reasons for replacements),
the difficulty spread, the new spec items covered, and anything you were unsure about.
