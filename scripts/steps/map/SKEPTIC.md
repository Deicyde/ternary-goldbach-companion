# Skeptic: claims that Helfgott's text is wrong

Agents mapping proof steps and displays of Helfgott's book (arXiv:1501.05438v2) and 2013 paper
(arXiv:1312.7748v2) to the Lean formalization flagged the claims in your group file as errors in
the text. You are one of two independent skeptics. Your job is to try to refute each claim.

Sources: the group file gives each record's LaTeX, TeX file and lines, and `tex_source_dir`.
Read the TeX in context (the surrounding proof, the definitions it uses). The Lean is in
`~/tg-companion/tg` (pinned; `NOTES.md` and `BLUEPRINT.md` record known errata of [H]); do not
run `lake` or `lean`. Do all the work yourself: do not launch subagents.

For each claim decide one verdict:
- `confirmed_error`: the text as printed is mathematically false (a counterexample, a wrong
  constant, a false inequality), not a mere misprint.
- `confirmed_typo`: a misprint whose intended reading is clear from context (wrong letter,
  missing factor that the next line restores, wrong label).
- `refuted`: the text is right as printed (explain why the claimant misread it).
- `unclear`: you cannot settle it.

Where a numerical computation can settle a claim (a constant, an inequality at a point, a
value), write a self-contained Python 3 script (standard library and mpmath only) to
`~/tg-companion/scratch/steps/skeptic/scripts/<slug>.py` that prints the computed values and
exits 0 when it confirms the claim and 1 when it refutes it, and run it. Name the script in your
verdict. If [L] contains a compiled proof that the printed statement is false or that a
corrected one holds (a Lean comment or NOTES.md entry pointing at a theorem), name the file and
declaration.

Write `~/tg-companion/scratch/steps/skeptic/<group>-<letter>.json` (letter given in your prompt):

```json
[{"id": "...", "verdict": "confirmed_error|confirmed_typo|refuted|unclear",
  "reason": "two sentences at most", "script": "path or null", "lean": "file:decl or null",
  "corrected": "the corrected statement, if any"}]
```

One entry per claim record. Reply with at most two lines.
