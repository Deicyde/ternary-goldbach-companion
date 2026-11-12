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
is a checked absence (`noMatch`).

A second overlay, in `paper-2013/`, shows H. A. Helfgott, *The ternary Goldbach conjecture is true*,
arXiv:1312.7748v2 (2014, 79 pp.). Each of its 244 numbered items is matched to its counterpart in the
book and takes that item's Lean links: with the book's relation where the two statements are the
same up to notation, and as `relatedMatch` at most where the book changed it (the note says what
changed). A further link points to the book's item on the book's PDF.

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

778 items, 2256 annotations: 2227 link calr3/ternary-goldbach, 29 the statements in `lean/`. By
item (the relation of its key links to calr3/ternary-goldbach; a link that only supports the item
is `relatedMatch`):

| Relation | Items |
|---|---|
| `exactMatch` (alone or with others) | 108 |
| `narrowMatch`: the book's item is more general (weaker constants or ranges in Lean) | 80 alone, 112 in all |
| `broadMatch`: the Lean statement is more general | 7 |
| `relatedMatch` only: a variant, a different definition, a step inside a proof, or a replacement argument | 430 |
| `noMatch`: searched for at the pin and absent | 131 |

By status (vocabulary of `data/items.json`): replaced 198, variant 142, not formalized (not needed) 132,
weaker 94, inlined 75, definition match 64, exact 47, definition differs 17, stronger 8, hypothesis 1.

The paper: 244 items (26 theorem-like, 218 equations), 953 annotations. 181 items state what their
book counterpart states up to notation, 60 were changed in the book (constants, ranges, redefined
functions, rewritten steps), and 3 have no counterpart in the book. Two matches by LaTeX label were
wrong (the book reused the label) and were replaced by the counterpart found by reading. By item:
`exactMatch` 31, `narrowMatch` 26, `broadMatch` 3, `relatedMatch` only 149, `noMatch` 31, no link 4.

## Formal statements

`lean/` states 28 results of the book as printed, in a Lake package that requires
calr3/ternary-goldbach at the pin (`lean/README.md`). At the pin each file proves, about its
statement: the statement itself, 8 (Thm 1.1.1 and (14.7) from the formalization's hypotheses);
that it implies a theorem of the formalization, 13, or is equivalent to its hypothesis
`RamareMoebius`, 1 ((2.21)); its negation, 4 ((5.32), (5.36), Prop 11.2.3, Prop D.0.3), and for
Thm 7.1.1 the negation of the remark printed after it; nothing, 2 (Thm 7.1.1, Thm 13.2.1). Each
such item of `book/` links its statement (`exactMatch`), and the note says what the file proves.
These links name `https://github.com/Deicyde/ternary-goldbach-companion`, a placeholder for where
this repository will be published, at the commit that added `lean/`.

## Errata

145 claims that [H] errs are confirmed (6 of them typos): 140 by a numerical check in
`scripts/checks/`, re-run on 2026-11-12, and 5 by a Lean proof in `lean/` that the printed
statement is false: (5.32), (5.36), Prop 11.2.3, the remark after Thm 7.1.1, and Prop D.0.3, whose
range should start at 5 < n (a typo). `docs/errata.md` lists them; each annotation's note gives its
item's. No other erratum claim appears here.

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
- Not checked: 196 other erratum claims, the typo claims among them, have no re-run check and are
  left out.

## Layout

- `data/items.json`: the items, their status, declarations at the pin, and how each verdict was
  checked (`verification`). `data/repin.json`: each item's declarations at `ce82a5b` and at the pin.
  `data/regions-book.json`: the items' regions on the PDF.
- `scripts/mapping/`: the merge of the mapping, the re-pin, the item list. `scripts/regions/`: the
  regions. `scripts/checks/`: the numerical checks behind the errata. `scripts/produce.py`: the
  annotations.
- `book/annotations/`: the annotations; `book/pdf-overlay/`: generated by formal-companion's
  `cf overlay sync`.
- `lean/`: the formal statements. `data/statements.json`: what each file proves, the links'
  source. `scripts/mapping/formal_errata.py`, `statements.py`: their records.
- `paper-2013/`: the same for the paper. `data/items-paper-2013.json` (its items),
  `data/regions-paper-2013.json`, `data/matches-paper-2013.json` (each item's counterpart in the book
  and how it was checked); `scripts/paper/`.

Apache License 2.0; see `NOTICE`.
