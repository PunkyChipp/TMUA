# TMUA Fortnight

An adaptive revision app for the TMUA (Test of Mathematics for University Admission), built for
the two weeks before the October 2026 sitting (12–16 October).

It works out what you're weakest at, then plans each day around that: short notes, drills pitched
at your level, mistakes brought back on a spaced schedule, and full papers at exam pace.

**To use it:** open `dist/index.html` in any browser. It's one self-contained file, so it works
offline and on a phone. Or use the GitHub Pages site once it's deployed (see below). Progress is
saved in your browser; use *Settings → Copy backup code* to move it between devices.

## What's in it

| | |
|---|---|
| **Diagnostic** | 16 questions, one per topic, to seed your ability estimates. |
| **Today** | Countdown, predicted marks for each paper, and a day-by-day plan that re-plans itself as your weaknesses change (build → sharpen → exam simulation → taper). |
| **Smart practice** | Picks topics by weakness × exam weight × staleness, and pitches each question at the difficulty you have roughly a 65% chance of getting right. |
| **Topic drills** | 10 questions on one topic, at your level. |
| **Speed round** | Quick-fire fluency questions against a tight clock. |
| **Timed sets and mocks** | 10 questions in 37½ min, or a full 20 questions in 75 min, with a question navigator, flagging, a pace line and a per-question time breakdown. |
| **Mistakes** | Spaced repetition (1, 3, 7, 14 days). Generated questions come back as fresh variants so you relearn the method rather than the answer. Tag why you missed each one; the app spots your pattern (careless, misread, traps, time…). |
| **Learn** | Exam-focused notes for all 14 topics, plus *Exam strategy* and *Facts to know cold*. |
| **Past papers** | Log official papers (free from the [UAT-UK preparation page](https://esat-tmua.ac.uk/tmua-preparation-materials/)), tap the ones you got wrong, and tag their topics. That feeds the plan too. |
| **Progress** | Topic mastery, pace by difficulty against target, activity over 14 days, and session history. |

Keyboard: `A`–`H` answer, `Enter` check/next, `Shift`+letter (or right-click) crosses out an
option, `G` marks a guess, `F` flags (in timed modes).

### The content

- **258 original questions** across 14 topics, each with a worked solution, a one-line key idea,
  and an explanation of why the tempting wrong answers are tempting.
- **41 question generators** (`src/gen/`) that produce unlimited variants with exact arithmetic,
  so drills never run out.
- **Every answer key has been checked twice.** The authoring pass verified each question with
  sympy or brute-force enumeration (`content/checks/`). A separate review pass then re-solved
  every question blind. Generators are fuzz-tested over thousands of seeds.

If you still find a question you think is wrong, press *Report a problem*. It will be hidden from
practice, and you can restore it in Settings.

### How the adaptivity works

Each answer updates a small ability model (`src/engine/model.js`): a global ability plus a
per-topic offset on a logit scale, Elo-style. A correct answer counts for less if you flagged it
as a guess or took much longer than the target time, because TMUA is a speed test. From that the
app estimates your mastery of each topic and predicts marks out of 20 for each paper. The more
you answer, the narrower the range gets.

## Developing

```bash
npm install
npm run build        # → dist/index.html
npm run watch        # rebuild on change
npm run check        # validate content, run sympy answer checks, run tests
```

- `content/questions/<topic>.json` holds the question bank (schema in `content/SCHEMA.md`).
- `content/notes/<topic>.md` holds the notes.
- `src/` holds the app: plain ES modules bundled by esbuild. No framework.
- `tools/validate.mjs` checks schema, KaTeX, plot expressions and answer-position balance.
- `tools/run_checks.py` runs every `content/checks/*_check.py`.

### Deploying to GitHub Pages

In the repo on GitHub, go to **Settings → Pages → Source: GitHub Actions**. Every push to `main`
then runs the checks and publishes `dist/index.html`.

## Adding questions with Claude Code

The bank was written with Claude Code from the briefs in `content/`, and you can grow it the same
way. Good prompts are specific about **where**, **what**, and **how to verify**:

> Read `content/AUTHORING_BRIEF.md` and `content/SCHEMA.md`. Add 6 new questions to
> `content/questions/trig.json` (ids trig-19 to trig-24), all difficulty 4–5, on counting
> solutions of equations like sin(ax) = cos(bx) on an interval. Verify each answer in
> `content/checks/trig_check.py`, then run `npm run check` and fix anything that fails.

> I got logic-12 wrong and think the key is wrong: I'd say C because … Re-solve it from scratch
> without looking at the key, then tell me who's right before changing anything.

> I keep mixing up the converse and contrapositive. Add a worked example to
> `content/notes/logic.md` that makes the difference obvious, and 4 practice questions on it.

What makes these work: name the files, give the ids and difficulty, point at the brief so it
follows the house style, and ask it to run `npm run check` so it proves its work. For anything
you're unsure about, ask it to explain first and change second.
