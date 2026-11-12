# Sweep: noMatch records that should be relatedMatch

You re-judge records of a companion that links Helfgott's ternary Goldbach book/paper (LaTeX given in
each record) to the Lean repository at `~/tg-companion/tg` (read-only; pinned commit, do not change it).
Do not read or write anything under `~/tg-companion/repo`, `~/tg-companion/out` or `~/tg-companion/scratch`
except your packet and your output file.

Each record is now `noMatch` ("searched for and absent from the Lean"). Its `note`, `checked` and
`searched` say what was searched. The vocabulary:
- `relatedMatch`: the Lean does this step's job at this place (inside the proof of the declaration that
  carries this item, or a helper it calls), but by a different argument or with a different quantity.
- `noMatch`: nothing in the Lean does this step's job; the Lean's proof does not need or perform it.

**Rule.** When the note, or your own search, names Lean lines that do this step's job at this place,
the record is `relatedMatch`, and you give those lines. Otherwise it stays `noMatch`. A note saying the
Lean "replaces", "instead", "via", "handled by", "covered by" is a strong hint, but check the Lean: the
replacement must do the job of *this* step (reach the same intermediate fact, or bound the same quantity,
by another route), not merely exist somewhere. Pure prose (signposting, a definition the Lean never
needs, a branch the Lean does not have) stays `noMatch`.

Search with `grep -n` / `rg` in `~/tg-companion/tg/TernaryGoldbach`. Be economical: start from the note's
and `checked`/`item_key_declarations` names. Give the tightest line range (usually 1–25 lines) inside one
declaration that does the job; `lines` are 1-based file line numbers in the pinned file and must lie
inside that declaration. At most 3 ends.

Write your output file as a JSON list, one object per record of your packet, in packet order:
```
{"id": "...", "overlay": "...", "verdict": "noMatch" | "relatedMatch",
 "ends": [{"declaration": "Full.Name", "file": "TernaryGoldbach/....lean", "lines": [a, b],
           "conclusion": "one sentence: what fact these lines establish"}],     // [] for noMatch
 "note": "one or two sentences: for relatedMatch, what the text does against what the Lean does here; for noMatch, keep or tighten the old note",
 "reason": "one short sentence"}
```
Return at most two lines: the file written and the counts.
