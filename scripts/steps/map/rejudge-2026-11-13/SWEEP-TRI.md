# Sweep: relatedMatch and exactMatch relations judged from their notes

You re-judge records of a companion that links Helfgott's ternary Goldbach book/paper (LaTeX given) to the
Lean repository at `~/tg-companion/tg` (read-only). Do not read or write anything under `~/tg-companion/repo`,
`~/tg-companion/out` or `~/tg-companion/scratch` except your packet and your output file.

Vocabulary (subject = the text's step/display, object = the Lean lines):
- `exactMatch`: the Lean lines establish exactly this fact.
- `closeMatch`: the same fact, by the same argument, up to a difference the note names (notation, a
  constant written as a literal instead of a named symbol, a free parameter that contains the text's
  choice, an equivalent reformulation).
- `relatedMatch`: the Lean does this step here, but by a *different argument* or with a *different quantity*.

Two known mistakes to find:
1. A `relatedMatch` whose note itself says the Lean uses the same argument and same quantity (e.g. "Same
   argument", "identical", "the same bound"), differing only in a named detail that does not change the
   fact → should be `closeMatch`. Example: the text chooses R = 1/√((ν+υ)q); the Lean leaves R free under
   qR²(ν+υ) ≤ 1, which contains that choice: closeMatch.
2. An `exactMatch` where the note says the Lean differs in a named way (e.g. the text's symbol κ₀ = 1.27
   does not exist in the Lean, only the literal 1.27 inside another bound; a different normalization;
   extra hypotheses) → should be `closeMatch`.

Judge from the note and the declaration names; open the Lean (given `L a-b` ranges in
`~/tg-companion/tg`) only when the note is ambiguous. Be conservative: change a record only when the note
clearly supports the change. A relatedMatch whose Lean argument or quantity really differs stays.

Write your output file as a JSON list containing ONLY the records you would change:
```
{"id": "...", "overlay": "...", "old": "relatedMatch", "new": "closeMatch",
 "note": "one or two sentences naming the difference", "reason": "one short sentence"}
```
Return at most two lines: the file written and the count.
