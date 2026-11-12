# Absence audit: re-check `noMatch` verdicts

Two agents linked proof steps and displays of Helfgott's book to the Lean formalization [L]
by `~/tg-companion/scratch/steps2/MAPPER.md`; read it first (records, relations, output schema,
the `decl.py` helper). Both agents called the records in your audit file `noMatch`, but some
of their searches were shallow, and earlier re-checks overturned a few such verdicts
(e.g. a zero sum the Lean bounds by a different method, which is `relatedMatch`, not absent).

For each record: read its TeX in context (`tex_source_dir`, file, lines), read the Lean proofs of
the enclosing item's key declarations (listed in the audit file) and their helpers, and grep
all of `~/tg-companion/tg/TernaryGoldbach/` for the step's quantities, constants and names.
Then rule:
- `confirmed`: no Lean lines establish the claim, a broader one, part of it, or the same step by
  another argument. Keep the record (you may add declarations you checked to its ends).
- `overturned`: you found lines; write the full record with the right relation (often
  `relatedMatch`, `narrowMatch` or `hasPart`), ends with exact `lines` inside `decl_lines` from
  `decl.py`, and a `conclusion` per end.

Do not run `lake` or `lean`. Do all the work yourself: do not launch subagents.

Write the output path in your prompt:

```json
{"audit": "<name>", "rulings": [
  {"id": "...", "kind": "absence_audit", "ruling": "confirmed|overturned",
   "reason": "one sentence: where you looked, or what you found",
   "record": { full record in the MAPPER.md schema }}]}
```

One ruling per record. Reply with at most two lines.
