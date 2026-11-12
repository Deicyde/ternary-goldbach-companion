# Mapping proof steps and displays of Helfgott's text to the Lean

You link each record of one batch (a proof step or a display of Helfgott's book [H],
arXiv:1501.05438v2, or of his 2013 paper, arXiv:1312.7748v2) to the place in the Lean
formalization [L] that carries it, or record that a search found it absent.

## Inputs

- **Packet** (path in your prompt): JSON with `records` (id, kind, LaTeX, TeX file and lines,
  printed page), and either `proofs` (the item each proof proves, its status from an earlier
  item-level audit, its statement, note, and key Lean declarations with file and full line
  range) or, for displays, `section_items` and `enclosing_items` (a display inside a theorem's
  statement has `inside_item`).
- **TeX source**: `tex_source_dir` in the packet. Read the proof (or the section around a
  display) in the source so you know what each step claims in context, and what the numbered
  displays between steps say.
- **Lean source**: `~/tg-companion/tg` (calr3/ternary-goldbach, pinned commit
  192ca57362fa3ee737cd83205cb9ea99526c4553). `BLUEPRINT.md` and `NOTES.md` there map [H] to
  files; module headers often name the [H] passages they cover. Mathlib is in
  `~/tg-companion/tg/.lake/packages/mathlib`.
- **Helper**: `python3 ~/tg-companion/scratch/steps2/decl.py NAME` prints a declaration's full
  name, file and full line range; `decl.py FILE:LINE` prints the declaration containing a line.
  Use it for every `declaration` and `decl_lines` you write. Do not run `lake` or `lean`.
- Use Read and Grep (or `rg`) on the sources. Do not modify any file except your output.

## Method

A `noMatch` is only valid after you have read the record's TeX in context and the full Lean
proofs of the enclosing item's key declarations (and their helpers): constant greps alone are
not a search, and neither is reading one file: grep the whole of `TernaryGoldbach/` for the
quantities, constants and names. Absence claims are re-checked by a judge.


1. Read the packet, then the TeX of the whole proof or section.
2. Read the Lean proofs of the enclosing item's key declarations, and the helper lemmas they
   call. Then align: for each step, find the lines that establish the step's claim. Search
   more widely (grep for the quantities, constants, equation numbers like `(4.12)` or
   `4.12`, lemma numbers, names) when the key declarations do not carry it.
3. For each record decide the relation by comparing the step's claim with what those lines
   establish. Never claim a relation stronger than you verified by reading the lines.

## What a step claims

- A display step claims its formula (in context: an identity, a bound, a definition).
- A prose step claims what its sentences assert: an inference ("by (4.3) and Lemma 2.1, …"),
  a bound, a case split, or a set-up ("Let $M = …$", "Assume $q$ odd"). For a set-up step,
  link the Lean lines that make the same set-up (a binder or hypothesis of the declaration, a
  `set`/`let`/`obtain`/`rcases`, a case split) if they exist.
- A connective step ("By Poisson summation," / "Hence") claims the use of that tool at that
  point: link the lines that use it.
- A short connective step ("Hence", "and so", "Now", "is at most", "This follows because")
  takes the relation of the claim it introduces or concludes (usually the next display),
  linked to the Lean lines that make that inference. Do not mark it `relatedMatch` merely
  because it is short.
- A step that is pure signposting with no mathematical content ("We now turn to the second
  case") is linked to the Lean lines that make the same move (the case split), or `noMatch` if
  [L] makes no such move.

## Relations (subject = the text's record, object = the Lean lines)

- `exactMatch`: the lines establish the same fact, up to notation (e.g. `Finset.sum` over
  `Finset.Icc 1 N` for $\sum_{n\le N}$, real vs. extended notation, junk values).
- `closeMatch`: the same fact, with a difference a reader should know that does not change
  the mathematics materially: an interval's endpoint open vs closed, $n\ge 1$ vs $n\ge 0$,
  a normalisation constant, an equivalent rearranged form. The note names the difference.
- `broadMatch`: [L] establishes more: a stronger conclusion or weaker hypotheses (e.g. [L]
  proves the bound for all $q$, the text for odd $q$; or a smaller constant).
- `narrowMatch`: [L] establishes less: stronger hypotheses, a special case, a weaker
  constant or bound (e.g. the text claims $\le 1.05$, [L] proves $\le 1.1$).
- `hasPart`: the lines establish one part of a step that claims several things. Name the part.
- `relatedMatch`: [L] does this step at this place, but by a different argument, or with a
  different quantity (a different weight, a different decomposition, a repaired version
  of a false claim). The note says what differs.
- **Analogue rule.** When the Lean lines carry out the same argument for a *different
  object* (odd $m$ in place of all $m$, $W-W'+1$ in place of $W/2$, $\eta_2$ in place of a
  general $\eta$, a different weight or decomposition), the relation is `relatedMatch`, even
  if the shape is the same, unless that difference does not enter the step's own claim (then
  judge the claim alone). `closeMatch` is for conventions: a constant rounded in the safe
  direction, strict vs non-strict inequality, an endpoint, an equivalent rearrangement.
- `broadMatch` applies when the Lean statement covers the text's case and more (a wider
  range, weaker hypotheses); check the text's range is inside the Lean's before using it.
- `noMatch`: searched and absent: no Lean lines establish this claim or a broader one. Ends
  name the declarations you checked (full range, no conclusion needed), and `searched` lists
  them and your grep patterns with the directories searched. `ends` must not be empty for
  `noMatch`: list each declaration you checked, full name, `lines` = its full range.

Expository displays outside proofs (history, heuristics, statements of other authors'
results [L] does not use, an illustrative example) are usually `noMatch`; still search.
A display defining a quantity [L] defines is linked to that definition.

Mathlib declarations may be ends when [L] uses that Mathlib fact for this step (file path
starting `.lake/packages/mathlib/`).

When a step spans several Lean places (e.g. one bound proved by two `have`s in different
lemmas), give several ends in logical order and set `proof_kind: "chain"`. Use `"helper"`
when the end is a separate helper lemma's statement or proof, `"direct"` when it is lines
inside the enclosing item's own Lean proof.

## Lines

- `lines: [first, last]` are 1-based line numbers in the Lean file, the smallest range that
  establishes the fact (a `have … := by …` block, one `calc` step, a lemma statement). Not
  the whole proof unless the whole proof is the step.
- `decl_lines` is the enclosing declaration's full range from `decl.py`; `lines` lies inside it.
- `declaration` is the full name as `decl.py` prints it.
- `conclusion`: one sentence saying what fact these lines establish, combining the
  mathematics with the essential Lean correspondence. Inline LaTeX and backticked names allowed.
  A `have` that starts an argument must not be described as completing the proof.
- `notation`: optional rows `{"math": "...", "lean": "..."}`, only where the Lean's notation
  needs them to be read.

## Text errors

If you believe the text's claim is false (not merely absent from [L] or done differently),
put it in `text_error_claim` with your evidence (a counterexample, a computation, a Lean
comment or NOTES.md passage). Otherwise `null`. A typo is a typo: say "typo" in it.

## Output

Write exactly one JSON file (path in your prompt):

```json
{"batch": "<batch>", "role": "<mapper|verifier>", "records": [
  {"id": "<record id>",
   "relation": "exactMatch|closeMatch|broadMatch|narrowMatch|hasPart|relatedMatch|noMatch",
   "proof_kind": "direct|helper|chain",
   "ends": [{"declaration": "TernaryGoldbach.MinorArcs.foo",
             "file": "TernaryGoldbach/MinorArcs/Foo.lean",
             "lines": [120, 131], "decl_lines": [101, 180],
             "conclusion": "…", "notation": []}],
   "note": "one or two sentences; required unless exactMatch",
   "searched": {"declarations": ["…"], "greps": ["pattern in dir", "…"]},
   "text_error_claim": null}
]}
```

One entry per record, in packet order, every record present. `searched` is required for
`noMatch` and optional otherwise. Notes are terse and exact: no hedges.
Your final reply is at most two lines: the output path and the relation counts.

Do all the work yourself: do not launch subagents or tasks.
