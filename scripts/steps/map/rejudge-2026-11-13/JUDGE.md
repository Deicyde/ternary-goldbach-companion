# Judge: noMatch or relatedMatch

You rule on records of a companion that links Helfgott's ternary Goldbach book/paper (the LaTeX is in each
record, with the previous and next step) to the Lean repository at `~/tg-companion/tg` (read-only, pinned).
Read nothing under `~/tg-companion/repo`, `~/tg-companion/out` or `~/tg-companion/scratch` except your packet
and your output file.

Each record is now `noMatch`. It was flagged because its note describes a Lean replacement, or a first
sweep proposed `relatedMatch` (`first_sweep`, with lines and snippets), or a reviewer gave a reading
(`review_reading`). These flags disagree with one another; you decide.

- `relatedMatch`: [L] does this step's job at this place (in the proof of the declaration that carries
  the item, or a helper it calls) but by a different argument or with a different quantity.
- `noMatch`: no Lean lines do this step's job; [L]'s proof does not need or perform it.

**Rule.** When the note or a search names Lean lines that do the step's job at this place, the record is
`relatedMatch`, with those lines. Otherwise it stays `noMatch`. "Does the job" means: the Lean lines reach
the same intermediate fact, or bound the same quantity, or settle the same case, at the corresponding
point of the Lean proof, by another route. A replacement that exists elsewhere in [L] but plays no role
at this point, signposting prose, a branch [L] does not have, or a definition [L] never uses: `noMatch`.

Check every `relatedMatch` against the Lean yourself (`sed -n 'a,bp' file`, `grep -n`). Give the tightest
range (usually 1–30 lines) inside one declaration; at most 3 ends; line numbers are 1-based in the pinned
file and must lie inside the declaration. Fix or replace the first sweep's lines when they are not the
right ones.

Output file: a JSON list, one object per packet record, in order:
```
{"id": "...", "overlay": "...", "verdict": "noMatch" | "relatedMatch",
 "ends": [{"declaration": "Full.Name", "file": "TernaryGoldbach/....lean", "lines": [a, b],
           "conclusion": "one sentence: what fact these lines establish"}],          // [] for noMatch
 "note": "one or two sentences. relatedMatch: what the text does here against what [L] does. noMatch: what was searched and why absent",
 "reason": "one short sentence for the ruling"}
```
Notes make no claim that the text is wrong. Return at most two lines: the file and the counts.
