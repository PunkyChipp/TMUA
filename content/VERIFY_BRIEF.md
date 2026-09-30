# Verification brief (independent reviewer)

You are an independent checker for a TMUA revision question bank. Another author wrote these
questions; your job is to catch anything wrong before a student relies on it. A wrong answer
key is the worst possible defect.

For EVERY question in your assigned `content/questions/<topic>.json` files:
1. Read only the stem, figure and options first. Solve it yourself, from scratch, and decide
   which option is correct. Use Python/sympy (installed) or brute force to confirm wherever
   possible. Only then look at `answer`.
2. If your answer differs from the key, work out who is right, carefully. If the key is wrong,
   fix `answer` (and the solution/distractor notes to match).
3. Check that exactly one option is correct (no second defensible answer), that the stem is
   unambiguous, that the worked `solution` is correct and complete, and that each `distractors`
   note describes the option it is keyed to (keys are 0-based option indexes).
4. Check the maths renders: run `node tools/validate.mjs <topic> [...]` from /home/user/TMUA —
   it must report 0 errors for your topics.
5. Read `content/notes/<topic>.md` for mathematical errors and fix any you find.

Rules
* Edit only your assigned topic files (questions JSON and notes). Keep ids, schema and field
  order. Rewrite the JSON with Python: json.load → modify → json.dump(ensure_ascii=False, indent=1).
* Numeric options stay in ascending order. Don't make stylistic rewrites; fix real problems:
  wrong keys, ambiguity, second correct option, errors in solutions, broken LaTeX, unclear wording.
* If a question is unfixable, replace it with a new original question of the same topic,
  difficulty and id, verified as above.
* If a topic's answers pile up on one letter (see validator warnings), you may re-order
  NON-numeric options (e.g. statement combos, sentences) to spread the keys, updating `answer`
  and `distractors` indexes to match. Never reorder "I only / II only / …" lists though — those
  keep the conventional order.

Reply with: per topic, the ids you changed and a one-line reason each, and the final validator line.
