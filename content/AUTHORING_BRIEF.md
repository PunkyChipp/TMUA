# Authoring brief (for question writers)

You are writing original practice material for the TMUA (Test of Mathematics for University
Admission): two 75-minute multiple-choice papers of 20 questions, no calculator, options A–H,
no negative marking. Paper 1 = "Mathematical Thinking" (applying GCSE + AS pure maths).
Paper 2 = "Mathematical Reasoning" (same maths content plus logic, proof, and spotting errors
in proofs). Read `content/SCHEMA.md` first and follow it exactly.

## Quality bar
* Questions must feel like real TMUA questions: short stems, clever not tedious, no calculator
  needed, answers that come out cleanly, and distractors that correspond to *real* slips
  (sign errors, forgetting a case, confusing necessary/sufficient, counting endpoints, etc.).
* Use typical TMUA formats where they fit: "Which of the following is/are true? I … II … III …"
  with options like "none of them / I only / II only / III only / I and II only / I and III only /
  II and III only / I, II and III"; "How many real solutions …"; "What is the complete set of
  values of $k$ …"; "Which one of the following is a counterexample …".
* Original questions only. Do NOT copy or paraphrase questions from official TMUA/MAT/STEP papers.
* Difficulty spread per topic (18 questions): d1 ×2, d2 ×4, d3 ×6, d4 ×4, d5 ×2.
* Roughly a quarter of questions for a Paper-1 topic should be Paper-2 flavoured (`"paper": 2`):
  reasoning about statements, "must be true", conditions, "which is sufficient".
* `solution`: a clear worked solution a strong student could follow in under a minute, leading
  with the fastest method, then noting any alternative. Use Markdown paragraphs/lists.
* `insight`: one sentence — the transferable idea.
* `distractors`: explain at least the 2 most tempting wrong options (key = option index as a string).
* Options must be distinct, and exactly one must be correct. Order numeric options ascending
  (TMUA usually does) — the app does NOT shuffle options.
* LaTeX inside JSON must be escaped (`\\frac`). Generate the file with a Python script
  (json.dump with ensure_ascii=False, indent=1) rather than hand-typing JSON, then json.load it back.

## Verification (mandatory)
For EVERY question, independently verify the keyed answer with a Python/sympy check (sympy is
installed) or a brute-force enumeration, and verify every distractor is actually wrong. Keep your
verification script in `content/checks/<topic>_check.py`; it should `assert` each answer and
print "ALL OK" at the end. Run it and make it pass. If a question can't be machine-checked
(pure logic wording), re-solve it from scratch a second time, carefully, before keeping it.
If in doubt about a question, drop it and write another — a wrong key is far worse than one
fewer question.

## Notes
Also write `content/notes/<topic>.md` for each of your topics (see SCHEMA.md): concise,
exam-focused, 500–1100 words, with at least two worked examples in <details> blocks. Include
the TMUA-specific tricks (sketch before solving, test special values, eliminate options, spot
the structure) that genuinely help for that topic. No fluff, no emoji, no motivational filler.
Write in plain British English (e.g. "maths", "colour").

When done, reply with: files written, count of questions per topic by difficulty, and anything
you were unsure about.
