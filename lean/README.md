# Formal statements of results of [H]

`Companion/Book/*.lean`: 28 results of H. A. Helfgott, *The ternary Goldbach problem*
(arXiv:1501.05438v2), each stated as printed (a `def … : Prop` and the notation it needs), with
what the file proves about it: the statement itself, its negation, or an implication to or from a
theorem of [calr3/ternary-goldbach](https://github.com/calr3/ternary-goldbach). Each file's header
says which. The files were written on 2026-11-06 against the formalization's commit `ce82a5b` and
repaired for the pin `192ca57`; no printed statement was changed.

```sh
lake build                 # the library Companion
lake env lean Axioms.lean  # the axioms of every theorem: propext, Classical.choice, Quot.sound
```

The package requires calr3/ternary-goldbach at `192ca57362fa3ee737cd83205cb9ea99526c4553`, with its
toolchain (`leanprover/lean4:v4.35.0`) and Mathlib (`56a005855ea17e0b0958f73ec801ae140b0a1679`);
`lake-manifest.json` pins all of them. A first `lake build` fetches and builds the formalization
(about an hour, with `lake exe cache get` for Mathlib).
