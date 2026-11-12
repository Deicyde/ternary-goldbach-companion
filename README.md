# Formal companions of Helfgott's ternary Goldbach proof

> **Unreviewed machine audit.** AI agents produced every verdict; no mathematician has checked any
> of it.
>
> This project is not affiliated with or reviewed by H. A. Helfgott, Charlie Reams or the
> maintainers of the formalization. Corrections are welcome as issues.

A PDF overlay of H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2 (2015, 327
pp.), in `book/`. Every numbered item of the PDF (theorems, lemmas, propositions, corollaries,
numbered equations, figures and the table: 778 items) is outlined on its page and linked, by
[Literature Links](https://github.com/mathlib-initiative/literature-links) 1.0.1 annotations, to
the Lean declarations of [calr3/ternary-goldbach](https://github.com/calr3/ternary-goldbach),
which formalizes the book relative to three published numerical results taken as hypotheses.
Each link carries a relation judged statement by statement; an item searched for and not found
is a checked absence (`noMatch`). Each unnumbered display outside proofs (434) and each step of
each proof (993 steps of 55 proofs) has its own box too, linked to the Lean lines that carry it or
marked absent after a search.

A second overlay, in `paper-2013/`, shows H. A. Helfgott, *The ternary Goldbach conjecture is true*,
arXiv:1312.7748v2 (2014, 79 pp.). 241 of its 244 numbered items are matched to their counterparts in
the book and take those items' Lean links: with the book's relation where the two statements are the
same up to notation, and as `relatedMatch` at most where the book changed it (the note says what
changed). A further link points to the book's item on the book's PDF. Its 138 unnumbered displays
and the 317 steps of its 23 proofs are linked as the book's are.

## Viewing it

```sh
git clone <this repository> && cd <it>/book      # or <it>/paper-2013
python3 pdf-overlay/tools/serve.py --build
```

`serve.py` fetches the PDF from arxiv.org, checks its sha256, caches it under `book/.lake/` and
serves the viewer on `127.0.0.1` only. The PDFs are not in this repository. Python 3.11+, standard
library only. The cards show plain statements: there is no Verso build of the pinned commit, so no
`pdf-overlay/verso.json` is written and nothing has hovers.

## Pins

- Lean: calr3/ternary-goldbach at `192ca57362fa3ee737cd83205cb9ea99526c4553`; Mathlib at
  `56a005855ea17e0b0958f73ec801ae140b0a1679` (its `lake-manifest.json`).
- PDF: `https://arxiv.org/pdf/1501.05438v2`, sha256
  `fde3e2679311336346053e980a766e5ffd8a811d79fbc822dd8431170b58c30e`, 2498797 bytes, 327 pages.
- PDF of the paper: `https://arxiv.org/pdf/1312.7748v2`, sha256
  `2b40a3e0772dd30d5ff8415240b5e60da3986467aa2eabbe95588c5ac4147179`, 935821 bytes, 79 pages.

## Counts

778 items, 2256 annotations on them (3873 in all, with 624 on the 434 unnumbered displays and 993
on the proof steps): 2220 link calr3/ternary-goldbach (131 of them checked absences), 7
Mathlib, 29 the statements in `lean/`. By item, the strongest relation of its key links to
calr3/ternary-goldbach or Mathlib (a link that only supports the item is `relatedMatch`):

| Relation | Items |
|---|---|
| `exactMatch` | 36 |
| `closeMatch`: the same up to a difference the note names (a floor, a factor, a typo's sign) | 13 |
| `broadMatch`: the Lean statement is more general | 19 |
| `narrowMatch`: the book's item is more general (weaker constants, narrower ranges, fixed parameters in Lean) | 88 |
| `hasPart`: Lean states a part of the item (one clause, one step of a chain) | 34 |
| `relatedMatch` only: a variant, a different definition, a step inside a proof, or a replacement argument | 457 |
| `noMatch`: searched for at the pin and absent | 131 |

The key links of the 217 items that had an `exactMatch`, `narrowMatch` or `broadMatch` were judged
again on 2026-11-12, blind and statement by statement (`data/rejudge-2026-11-12.json`); 144 items
changed, and no relation was raised.

By status (vocabulary of `data/items.json`): replaced 198, variant 142, not formalized (not needed) 132,
weaker 94, inlined 75, definition match 64, exact 47, definition differs 17, stronger 8, hypothesis 1.

The paper: 244 items (26 theorem-like, 218 equations), 953 annotations on them (1492 in all, with
222 on the 138 unnumbered displays and 317 on the proof steps). 181 items state what their
book counterpart states up to notation, 60 were changed in the book (constants, ranges, redefined
functions, rewritten steps), and 3 have no counterpart in the book. Two matches by LaTeX label were
wrong (the book reused the label) and were replaced by the counterpart found by reading. By item:
`exactMatch` 10, `closeMatch` 5, `broadMatch` 8, `narrowMatch` 21, `hasPart` 7, `relatedMatch` only
158, `noMatch` 31, no link 4.

<!-- coverage: written by scripts/coverage.py -->
## Coverage

Each statement, display and proof step has one class (`docs/coverage.md` section 6); "formalized" is
1-to-1 + Faithful. Details, the paper's sections, the 1-to-1 list, every deviation and the absences:
[`docs/coverage.md`](docs/coverage.md).

Helfgott, *The ternary Goldbach problem* (arXiv:1501.05438v2):

| | Formalized | 1-to-1 | Deviates | Absent |
|---|---|---|---|---|
| Statements | 4/66 (6%) | 4/66 (6%) | 46/66 (70%) | 10/66 (15%) |
| Displays | 123/1142 (11%) | 58/1142 (5%) | 742/1142 (65%) | 238/1142 (21%) |
| Steps | 137/993 (14%) | 42/993 (4%) | 543/993 (55%) | 286/993 (29%) |

Of the 46 statements that deviate, 13 have a confirmed erratum; of the others, [L] proves less (`narrowMatch`) for 9 and does the work another way (`relatedMatch`) for 24.

| Chapter | Statements formalized | Displays formalized | Steps formalized | Steps absent | Deviations |
|---|---|---|---|---|---|
| 1 | 1/1 (100%) | 16/69 (23%) | — | — | 36/70 (51%) |
| 2 | 0/1 (0%) | 11/34 (32%) | 4/7 (57%) | 0/7 (0%) | 21/42 (50%) |
| 3 | 0/1 (0%) | 5/25 (20%) | — | — | 10/26 (38%) |
| 4 | 3/7 (43%) | 4/64 (6%) | 42/198 (21%) | 14/198 (7%) | 185/269 (69%) |
| 5 | 0/6 (0%) | 8/79 (10%) | 34/127 (27%) | 18/127 (14%) | 129/212 (61%) |
| 6 | — | 23/168 (14%) | 7/18 (39%) | 0/18 (0%) | 140/186 (75%) |
| 7 | 0/5 (0%) | 4/18 (22%) | — | — | 14/23 (61%) |
| 8 | 0/2 (0%) | 0/114 (0%) | — | — | 51/116 (44%) |
| 9 | 0/12 (0%) | 8/134 (6%) | 8/274 (3%) | 117/274 (43%) | 240/420 (57%) |
| 10 | 0/2 (0%) | 7/63 (11%) | — | — | 55/65 (85%) |
| 11 | 0/6 (0%) | 5/33 (15%) | 2/69 (3%) | 37/69 (54%) | 48/108 (44%) |
| 12 | 0/8 (0%) | 6/52 (12%) | 19/145 (13%) | 44/145 (30%) | 121/205 (59%) |
| 13 | 0/3 (0%) | 3/49 (6%) | 12/59 (20%) | 3/59 (5%) | 78/111 (70%) |
| 14 | — | 13/120 (11%) | — | — | 88/120 (73%) |
| A | — | 8/76 (11%) | — | — | 40/76 (53%) |
| B | 0/6 (0%) | 0/18 (0%) | 8/52 (15%) | 21/52 (40%) | 46/76 (61%) |
| C | 0/5 (0%) | 2/25 (8%) | 0/32 (0%) | 27/32 (84%) | 21/62 (34%) |
| D | 0/1 (0%) | 0/1 (0%) | 1/12 (8%) | 5/12 (42%) | 8/14 (57%) |

By statement share: most formalized chapter 1, 1/1 (100%); least chapters 2 (0/1), 3 (0/1), 5 (0/6), 7 (0/5), 8 (0/2), 9 (0/12), 10 (0/2), 11 (0/6), 12 (0/8), 13 (0/3), B (0/6), C (0/5), D (0/1), 0% each. By step share: most formalized chapter 2, 4/7 (57%); least chapter C, 0/32 (0%).

Helfgott, *The ternary Goldbach conjecture is true* (arXiv:1312.7748v2):

| | Formalized | 1-to-1 | Deviates | Absent |
|---|---|---|---|---|
| Statements | 0/26 (0%) | 0/26 (0%) | 20/26 (77%) | 4/26 (15%) |
| Displays | 38/356 (11%) | 18/356 (5%) | 245/356 (69%) | 56/356 (16%) |
| Steps | 33/317 (10%) | 7/317 (2%) | 158/317 (50%) | 118/317 (37%) |

Of the 20 statements that deviate, 0 have a confirmed erratum; of the others, [L] proves less (`narrowMatch`) for 3 and does the work another way (`relatedMatch`) for 17.

<!-- /coverage -->

## Formal statements

`lean/` states 28 results of the book as printed, in a Lake package that requires
calr3/ternary-goldbach at the pin (`lean/README.md`). At the pin each file proves, about its
statement: the statement itself, 8 (Thm 1.1.1 and (14.7) from the formalization's hypotheses);
that it implies a theorem of the formalization, 13, or is equivalent to its hypothesis
`RamareMoebius`, 1 ((2.21)); its negation, 4 ((5.32), (5.36), Prop 11.2.3, Prop D.0.3); for Thm
7.1.1, stated with the one-sided Gaussian of §9.2, that it and the remark printed after it cannot
both hold, that the remark is false, and that the theorem is false with the two-sided Gaussian;
nothing, 1 (Thm 13.2.1). Each such item of `book/` links its statement (`exactMatch`; `closeMatch`
for Thm 7.1.1, whose reading of η♡ the file fixes), and the note says what the file proves.
These links name `https://github.com/Deicyde/ternary-goldbach-companion`, a placeholder for where
this repository will be published, at the commit that added `lean/`.

## Errata

147 claims that [H] errs are confirmed (7 of them typos): 142 by a numerical check in
`scripts/checks/`, re-run on 2026-11-12 ((6.77): 2026-11-13), and 5 by a Lean proof in `lean/`: (5.32), (5.36) and
Prop 11.2.3 are false as printed; Prop D.0.3's range should start at 5 < n (a typo); Thm 7.1.1 and
the remark after it cannot both hold (the remark is false with η♡ one-sided, as in §9.2; the theorem
is false with η♡ two-sided, as §7.1 writes it). `docs/errata.md` lists them; each annotation's note
gives its item's. Notes state no other claim that [H] errs.

## What was checked

- The Lean at the pin was built (`lake build`, 9475 jobs), and `#print axioms` of the two main
  theorems gives `propext`, `Classical.choice`, `Quot.sound`.
- The mapping was made on 2026-11-06 against commit `ce82a5b` (a mapper, a verifier and a judge
  per batch). Re-pinned to `192ca57` by elaborated types: 368 items unchanged, 405 changed (mostly
  dropped `Fact` hypotheses), 5 with a declaration gone. The 462 items that changed, lost one, were
  newly cited at the pin, or whose 2026-11-06 checking was incomplete were re-judged against the
  LaTeX and the Lean at the pin; one status changed ((2.19): exact → weaker).
- A random 5% of the other items (16) was checked by hand: one verdict was wrong ((5.28)), and a
  second ((13.30)) was found wrong by the absence search.
- 131 of the 132 items judged not formalized were searched for again at the pin; (1.39), a heuristic, links its rigorous Lean form without a checked absence.
- Every linked declaration was resolved in the elaborated environment at the pin.
- `lean/` was built at the pin under `autoImplicit false`; every theorem in it uses only `propext`,
  `Classical.choice` and `Quot.sound` (`lean/Axioms.lean`). Its statements are those of 2026-11-06,
  unchanged, and the definitions of the formalization they use are the same at `ce82a5b` and at the
  pin. Each refuted statement was compared with the printed one in the LaTeX.
- The annotations pass `cf overlay check`, `pdf-overlay/tools/check_generated.py` and
  `python3 -m literature_links scan <overlay>/annotations` (the scan's target is the annotations folder: the
  overlay root also holds tracked copies, `site/pdf-overlay/verso.json` and the vendored schemas, that are
  not annotations).
- Not checked: 194 other erratum claims, the typo claims among them, have no re-run check and are
  left out.

## Layout

- `data/items.json`: the items, their status, declarations at the pin, and how each verdict was
  checked (`verification`). `data/repin.json`: each item's declarations at `ce82a5b` and at the pin.
  `data/regions-book.json`: the items' regions on the PDF.
- `scripts/mapping/`: the merge of the mapping, the re-pin, the item list; `review_fixes.py`, the
  corrections of the 2026-11-12 review, with the re-judged relations of `data/rejudge-2026-11-12.json`. `scripts/regions/`: the
  regions. `scripts/checks/`: the numerical checks behind the errata. `scripts/produce.py`: the
  annotations.
- `book/annotations/`: the annotations; `book/pdf-overlay/`: generated by formal-companion's
  `cf overlay sync`.
- `lean/`: the formal statements. `data/statements.json`: what each file proves, the links'
  source. `scripts/mapping/formal_errata.py`, `statements.py`: their records.
- `data/<overlay>-displays.json`, `data/<overlay>-steps.json`: the unnumbered displays outside proofs and the
  steps of every proof, segmented from the LaTeX (`scripts/steps/segment.py`; `data/book-splits.json`, the
  long paragraphs cut at sentences). `data/<overlay>-regions-steps.json`: their regions on the PDF
  (`scripts/regions/run_steps.sh`). `data/<overlay>-{displays,steps}-mapping.json`: their links, with how each
  was checked (`scripts/steps/map/`); `data/steps-text-claims.json`: the skeptics' verdicts on claims that the
  text is wrong, with the checks in `scripts/checks/steps/`. `scripts/coverage.py`: `docs/coverage.md`,
  `data/coverage.json` and the Coverage section above.
- `paper-2013/`: the same for the paper. `data/items-paper-2013.json` (its items),
  `data/regions-paper-2013.json`, `data/matches-paper-2013.json` (each item's counterpart in the book
  and how it was checked); `scripts/paper/`.

Apache License 2.0; see `NOTICE`.
