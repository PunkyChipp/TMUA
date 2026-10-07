# Verification brief, 2026 upgrade (independent reviewer)

Follow `content/VERIFY_BRIEF.md` (blind-solve every question before looking at its key; fix
real defects only; rewrite JSON with json.load/json.dump ensure_ascii=False indent=1; keep ids,
schema and field order), with these additions:

* The bank now has twins: every question X has a twin Xb, both with `"family": "X"`. Verify
  EVERY question, originals and twins alike. A twin must test the same idea with a genuinely
  different surface (not one number changed), and its key must be a different letter from its
  sibling's. Report any twin that fails this, and fix it.
* Check every question against `content/SPEC_2026.md`: nothing off-spec (change of base,
  inflexion as the point of a question, symbolic logic notation or truth tables in Paper 2
  stems/options, sphere/cone/pyramid formulae not stated, etc.).
* Judge difficulty honestly against real TMUA papers. Where a question labelled d4/d5 is really
  routine, or one labelled d2/d3 is very hard, correct the `difficulty` field.
* Run the topic's `content/checks/<topic>_check.py` (it must print ALL OK, updating it to match
  any fix you make) and `node tools/validate.mjs <topic>` (0 errors) before you finish.

Reply with: per topic, ids changed and a one-line reason each, any difficulty relabels, and the
final check/validator lines.
