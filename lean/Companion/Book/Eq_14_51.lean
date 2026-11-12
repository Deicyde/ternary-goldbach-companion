import TernaryGoldbach

/-!
# [H, (14.51)]: the terms with an even or non-prime `nᵢ`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §14.4
("Conclusion: proof of main theorem"), equation (14.51), p. 276
(https://arxiv.org/pdf/1501.05438v2#page=286). Having bounded the circle-method integral (14.50)
from below, [H] removes from `∑_{n₁+n₂+n₃=N} Λ(n₁)Λ(n₂)Λ(n₃) η₊(n₁) η₊(n₂) η_*(n₃)` the terms
in which some `nᵢ` is even or not prime ("Clearly"):

`∑_{n₁+n₂+n₃=N, n₁, n₂ or n₃ even or non-prime} Λ(n₁)Λ(n₂)Λ(n₃) η₊(n₁) η₊(n₂) η_*(n₃)`
`  ≤ 3 |η₊|²_∞ |η_*|_∞ ∑_{n₁+n₂+n₃=N, n₁ even or non-prime} Λ(n₁)Λ(n₂)Λ(n₃)`
`  ≤ 3 |η₊|²_∞ |η_*|_∞ · (log N) ∑_{n₁ ≤ N non-prime or n₁ = 2} Λ(n₁) ∑_{n₂ ≤ N} Λ(n₂)`.

The display contains no numerical bound (only the factor `3`). The sentences after it insert
`|η₊|_∞ ≤ 1.079955` (14.3), `|η_*|_∞ ≤ 1.414` (14.21) and, "by [RS62, Thms. 12 and 13]",
`∑_{n₁ ≤ N non-prime or n₁=2} Λ(n₁) < 1.4262 √N + log 2 < 1.4263 √N` and
`∑_{n₂ ≤ N} Λ(n₂) < 1.03883 N`, and conclude: "Hence, the sum on the first line of (14.51) is at
most `7.3306 N^{3/2} log N`." That number is what the final display of §14.4 subtracts. The
2013 version, [H13, (7.50)] (arXiv:1312.7748v2, p. 70), is identical.

**What the formalization proves.**
* `TernaryGoldbach.Helfgott.nonprime_input` (`Helfgott/Inputs.lean`): for every natural
  `N ≥ 10²⁷`, odd or even, `repSum (fun _ => True) N - repSum (fun n => n.Prime ∧ Odd n) N ≤
  6.7·10⁶ · (N √N) · log N`. The left side is exactly the first member of (14.51)
  (`eq_14_51_first_eq`). `nonprime_input` takes no `Fact` hypothesis.
* Its proof goes through `TernaryGoldbach.Helfgott.repSum_sub_le_of_bounds`
  (`Helfgott/NonPrime.lean`, "[H13, (7.50)] with the constants as parameters"). For every `N ≥ 1`
  and any bounds `A₊ ≥ |η₊|`, `A_* ≥ |η_*|` on `[0, ∞)`, it bounds the first member of (14.51) by
  `3 (A₊² A_*) (log N) (ψ(N) - θ(N) + log 2) ψ(N)`. This is the first member against the last one,
  with `A₊`, `A_*` in place of the sup norms and `ψ(N) - θ(N) + log 2` in place of the sum over
  non-prime `n₁` and `n₁ = 2`. The middle member is not stated in the repo. `nonprime_input` then
  inserts `|η₊| ≤ 400`, `|η_*| ≤ 6.2` (`Helfgott/SupNorms.lean`) and the elementary
  `ψ(N) ≤ 1.387 N`, `ψ(N) - θ(N) ≤ 1.6 √N` (`Helfgott/Chebyshev.lean`).
* The repo also proves both Rosser–Schoenfeld bounds that [H] quotes, in `Prelim/LambdaMu.lean`:
  `TernaryGoldbach.Prelim.sum_vonMangoldt_lt` ([RS62, Thm. 12]: `ψ(y) < 1.03883 y` for `y > 0`)
  and `TernaryGoldbach.Prelim.sum_vonMangoldt_nonprime_lt` ([RS62, Thm. 13]:
  `ψ(y) - θ(y) < 1.4262 √y` for `y > 0`). Both take `[Fact PlattGRH]`. `nonprime_input` does
  not use them.
* It does not prove [H]'s sharp sup norms (14.3) and (14.21). The sharpest constant bounds it
  states are `|η₊(t)| ≤ 1.94` for `t ≥ 0` (`TernaryGoldbach.Helfgott.abs_etaPlus_le_A`,
  `Helfgott/HHBound.lean`) and `|η_*(t)| ≤ 6.2` (`TernaryGoldbach.Helfgott.abs_etaStar_le_const`).

**Relation: (14.51) as printed is proved here, and the formal theorems follow from it.** Certified
by

* `eq_14_51_holds : eq_14_51`: the printed chain, both inequalities, with the actual sup norms,
  for every `N ≥ 10²⁷`. `eq_14_51_chain` proves it for every `N ≥ 1`. It is proved in this file
  from the repo's definitions and lemmas. The repo never states the middle member: it bounds the
  three unweighted sums (with `n₁`, `n₂` or `n₃` even or non-prime) separately, while the middle
  member uses that they are equal (`eq_14_51_sym2`, `eq_14_51_sym3` here);
* `eq_14_51_implies_formal : eq_14_51 → type_of% @TernaryGoldbach.Helfgott.nonprime_input`: the
  formal bound follows from the printed chain combined with the repo's crude inputs. This is the
  formalization's own route, and the proof does not call `nonprime_input`;
* `eq_14_51_chain_implies_formal`: the printed chain at every `N ≥ 1` implies
  `type_of% @TernaryGoldbach.Helfgott.repSum_sub_le_of_bounds`, the repo's parametric (14.51). Its
  hypothesis covers every `N ≥ 1`, not only `N ≥ 10²⁷`, because the repo lemma does;
  `eq_14_51_chain` proves that hypothesis.

**[H]'s numerical conclusion.** `eq_14_51_bound` (first member `≤ 7.3306 N^{3/2} log N` for
`N ≥ 10²⁷`) is stronger than `nonprime_input`: same quantity, same range, and
`7.3306 < 6.7·10⁶`. This is certified by
`eq_14_51_bound_implies_formal : eq_14_51_bound → type_of% @…nonprime_input`. The formalization
neither proves nor refutes `eq_14_51_bound`. Of the four inputs [H] uses after (14.51), it proves
the two Rosser–Schoenfeld bounds and lacks only the sharp sup norms (14.3) and (14.21):

* `eq_14_51_bound_of_supNorms`: under `[Fact PlattGRH]`, `|η₊|_∞ ≤ 1.079955` and
  `|η_*|_∞ ≤ 1.414` give `eq_14_51_bound`. The proof uses (14.51) and the repo's RS62 theorems;
* `eq_14_51_bound_of_inputs`: the same, with all four inputs as hypotheses and no `Fact`;
* `eq_14_51_first_le_repo`: with the repo's own `1.94` and `6.2` in place of (14.3) and (14.21),
  [H]'s route gives `103.73 N^{3/2} log N` (`3 · 1.94² · 6.2 · 1.4263 · 1.03883 ≈ 103.7222`),
  under `[Fact PlattGRH]`.

[H]'s arithmetic is right: `3 · 1.079955² · 1.414 · 1.4263 · 1.03883 ≈ 7.330563 ≤ 7.3306`
(`eq_14_51_bound_of_inputs`).

Auxiliary results:
* `eq_14_51_first_eq`: the first member of (14.51) is `repSum (fun _ => True) N -
  repSum (fun n => n.Prime ∧ Odd n) N`, the quantity `nonprime_input` bounds;
* `eq_14_51_sum_vonMangoldt`: `∑_{n₂ ≤ N} Λ(n₂) = ψ(N)`; `eq_14_51_sum_bad_le`:
  `∑_{n₁ ≤ N non-prime or n₁ = 2} Λ(n₁) ≤ ψ(N) - θ(N) + log 2`;
* `eq_14_51_psi_lt`, `eq_14_51_psi_sub_theta_lt`: [RS62, Thms. 12, 13] at natural `N ≥ 1`, from
  the repo's theorems;
* `eq_14_51_le_supNorm`, `eq_14_51_supNorm_le`, `eq_14_51_supNorm_nonneg`,
  `eq_14_51_abs_etaPlus_le`, `eq_14_51_abs_etaStar_le`, `eq_14_51_supNorm_etaPlus_le` (`≤ 400`),
  `eq_14_51_supNorm_etaPlus_le_A` (`≤ 1.94`), `eq_14_51_supNorm_etaStar_le` (`≤ 6.2`):
  `eq_14_51_supNorm` is a genuine supremum, not Lean's junk value `0` for unbounded families, so
  the constant `3 |η₊|²_∞ |η_*|_∞` in `eq_14_51` is the book's.
-/

namespace Companion.Book

open Finset
open scoped ArithmeticFunction.vonMangoldt
open TernaryGoldbach.Helfgott (etaPlus etaStar xOf repSum psi theta ΛBad)

/-! ### The book's objects -/

/-- **`|η|_∞`**, the sup norm on `[0, ∞)`: `sup_{t ≥ 0} |η(t)|`.

[H, §2.1] writes `|f|_r` for the `L_r` norm; the repo has no sup-norm object. The domain
`[0, ∞)` is where `η₊` and `η_*` live: Thm. 13.2.1, which the Ch. 14 preamble cites, takes
`η₊` and `φ` on `[0, ∞)`, and `η_*` is a Mellin convolution, defined for `t ≥ 0`. The rest of
this paragraph consists of mathematical remarks: they are not proved here, and no proof in this
file needs them. `η₊` vanishes on `(-∞, 0]` (`h₂₀₀(t) = 0` for `t < 0`, since `h` is supported
on `[0, 2]`). The repo's `etaStar` uses the Mellin-convolution formula for every `t ∈ ℝ`, and it
is even in `t` because `φ` is, so the supremum over `ℝ` is the same. Both functions are
continuous on `[0, ∞)`, so their `L_∞` norm equals this pointwise supremum (the repo has no
continuity lemma for `etaPlus` or `etaStar`).

The pointwise supremum is in any case the reading the first inequality of (14.51) needs, since it
bounds the values `|η₊(nᵢ/x)|` and `|η_*(n₃/x)|` one by one.

Lean's `⨆` returns `0` for a family that is not bounded above. Both functions are bounded on
`[0, ∞)` (`eq_14_51_supNorm_etaPlus_le`, `eq_14_51_supNorm_etaStar_le`), so here it is the true
supremum (`eq_14_51_le_supNorm`). -/
noncomputable def eq_14_51_supNorm (η : ℝ → ℝ) : ℝ :=
  ⨆ t : Set.Ici (0:ℝ), |η t|

/-- **The first member of (14.51)** ("the sum on the first line of (14.51)"):
`∑_{n₁+n₂+n₃=N, n₁, n₂ or n₃ even or non-prime} Λ(n₁)Λ(n₂)Λ(n₃) η₊(n₁/x) η₊(n₂/x) η_*(n₃/x)`
with `x = xOf N = N/(2 + 9/(196√(2π)))` [H, (14.15)].

The `nᵢ` are positive integers ([H, §2.1]: `∑_n` means `∑_{n ≥ 1}`). A triple with
`n₁ + n₂ + n₃ = N` has every `nᵢ ∈ [1, N]`, so the book's finite sum is the triple sum over
`Icc 1 N` cut down by the `if`. "`n₁, n₂ or n₃` even or non-prime" means that at least one `nᵢ`
is even or not prime. This is the complement of "`n₁, n₂, n₃` odd primes" in the last display of
§14.4. -/
noncomputable def eq_14_51_first (N : ℕ) : ℝ :=
  ∑ n₁ ∈ Icc 1 N, ∑ n₂ ∈ Icc 1 N, ∑ n₃ ∈ Icc 1 N,
    if n₁ + n₂ + n₃ = N ∧
        ((Even n₁ ∨ ¬ n₁.Prime) ∨ (Even n₂ ∨ ¬ n₂.Prime) ∨ (Even n₃ ∨ ¬ n₃.Prime)) then
      Λ n₁ * Λ n₂ * Λ n₃ * etaPlus (n₁ / xOf N) * etaPlus (n₂ / xOf N) * etaStar (n₃ / xOf N)
    else 0

/-- **The sum in the second member of (14.51)**:
`∑_{n₁+n₂+n₃=N, n₁ even or non-prime} Λ(n₁)Λ(n₂)Λ(n₃)`, unweighted, over positive integers as in
`eq_14_51_first`. -/
noncomputable def eq_14_51_second (N : ℕ) : ℝ :=
  ∑ n₁ ∈ Icc 1 N, ∑ n₂ ∈ Icc 1 N, ∑ n₃ ∈ Icc 1 N,
    if n₁ + n₂ + n₃ = N ∧ (Even n₁ ∨ ¬ n₁.Prime) then Λ n₁ * Λ n₂ * Λ n₃ else 0

/-- **The third member of (14.51) without the factor `3 |η₊|²_∞ |η_*|_∞`**:
`(log N) ∑_{n₁ ≤ N non-prime or n₁ = 2} Λ(n₁) ∑_{n₂ ≤ N} Λ(n₂)`, with `n₁, n₂ ≥ 1` and the
natural logarithm. -/
noncomputable def eq_14_51_third (N : ℕ) : ℝ :=
  Real.log N * (∑ n₁ ∈ Icc 1 N with (¬ n₁.Prime ∨ n₁ = 2), Λ n₁) * ∑ n₂ ∈ Icc 1 N, Λ n₂

/-- **[H, (14.51)]** as printed: for every natural number `N ≥ 10²⁷`, with
`x = N/(2 + 9/(196√(2π)))`,

`∑_{n₁+n₂+n₃=N, n₁, n₂ or n₃ even or non-prime} Λ(n₁)Λ(n₂)Λ(n₃) η₊(n₁) η₊(n₂) η_*(n₃)`
`  ≤ 3 |η₊|²_∞ |η_*|_∞ ∑_{n₁+n₂+n₃=N, n₁ even or non-prime} Λ(n₁)Λ(n₂)Λ(n₃)`
`  ≤ 3 |η₊|²_∞ |η_*|_∞ · (log N) ∑_{n₁ ≤ N non-prime or n₁ = 2} Λ(n₁) ∑_{n₂ ≤ N} Λ(n₂)`.

Transcription choices.
* The chain `A ≤ B ≤ C` is the conjunction `A ≤ B ∧ B ≤ C`. The members are `eq_14_51_first`,
  `eq_14_51_second` and `eq_14_51_third`, each multiplied by the constant
  `3 |η₊|²_∞ |η_*|_∞ = 3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar` where the
  book has it.
* Range: `N` is a natural number with `N ≥ 10²⁷`, the standing assumption of Ch. 14 (preamble:
  "we want a result valid for `N ≥ 10²⁷`"; after (14.15): "since we are assuming `N ≥ 10²⁷`").
  (14.51) is introduced by "Clearly" with no parity hypothesis. §14.4 assumes "`N` odd" in the
  display before (14.51), for the arcs, and again in the final display after it. (14.51) itself
  never uses parity. The chain holds for every `N ≥ 1` (`eq_14_51_chain`), so the reading "odd
  `N ≥ 10²⁷`" is covered too.
* The book prints `η₊(n₁) η₊(n₂) η_*(n₃)`, an abbreviation for `η₊(n₁/x) η₊(n₂/x) η_*(n₃/x)`.
  That is forced by (10.2), which writes `ηᵢ(nᵢ/x)`, and by (14.50), which equates this sum with
  `∫ S_{η₊}(α,x)² S_{η_*}(α,x) e(-Nα) dα`, where `S_η(α,x) = ∑ Λ(n) e(αn) η(n/x)`. Here
  `x = TernaryGoldbach.Helfgott.xOf N = N/(2 + 9/(196√(2π)))`, which is [H, (14.15)]
  (`N/(2 + c₁/κ)` with `c₁/κ = (9/4)/(49√(2π))`).
* `η₊(t) = h₂₀₀(t) t e^{-t²/2}` (Ch. 14 preamble, [H, (7.4)–(7.6)]) is
  `TernaryGoldbach.Helfgott.etaPlus`, definition for definition. `η_*(t) = (η₂ *_M φ)(κt)`,
  `φ(t) = t² e^{-t²/2}`, `κ = 49`, `η₂ = η₁ *_M η₁` is `TernaryGoldbach.Helfgott.etaStar`, with
  `η₁ = 2·1_{[1/2,1]}` as in (11.10). The preamble's `2·1_{[-1/2,1/2]}` is a misprint, see
  `Companion/Book/Eq_14_49.lean`. (14.21)'s `|η₂(t)/t|₁ = 4(log 2)²` also requires (11.10)'s
  `η₁`.
* `|η|_∞` is `eq_14_51_supNorm`, the supremum of `|η|` over `[0, ∞)` (see its docstring).
* The sums run over positive integers. The condition "`n₁` even or non-prime" is
  `Even n₁ ∨ ¬ n₁.Prime`. "`n₁ ≤ N` non-prime or `n₁ = 2`" is `1 ≤ n₁ ≤ N` with
  `¬ n₁.Prime ∨ n₁ = 2`. `log` is `Real.log`.

Non-vacuity: the sup norms are genuine suprema of bounded functions (`eq_14_51_le_supNorm`), not
Lean's junk value `0`, and the first member is the repo's `repSum` difference
(`eq_14_51_first_eq`). Proved: `eq_14_51_holds`. -/
def eq_14_51 : Prop :=
  ∀ N : ℕ, 10 ^ 27 ≤ N →
    eq_14_51_first N ≤
        3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_second N ∧
      3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_second N ≤
        3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_third N

/-- **[H]'s numerical conclusion from (14.51)**, the sentence after the display: "Hence, the sum
on the first line of (14.51) is at most `7.3306 N^{3/2} log N`". The range is `N ≥ 10²⁷`, as for
`eq_14_51`: the derivation uses no parity, and §14.4 re-imposes "`N` odd" only in its final
display. `N^{3/2}` is the real power `(N : ℝ) ^ (3/2 : ℝ)`.

[H] derives it from (14.51), (14.3), (14.21) and [RS62, Thms. 12, 13]; `eq_14_51_bound_of_inputs`
checks that derivation. (In the intermediate display [H] prints
`∑ Λ(n₁) ∑ Λ(n₂) = 1.4263√N · 1.03883 N`. That `=` should be `<`; the misprint is harmless.)

Not proved by the formalization. The formalization proves the two Rosser–Schoenfeld inputs but
not the sharp sup norms (14.3) and (14.21); `eq_14_51_bound_of_supNorms` derives
`eq_14_51_bound` from those two sup norms alone, under `[Fact PlattGRH]`. It
implies the formal `nonprime_input` (`eq_14_51_bound_implies_formal`). -/
def eq_14_51_bound : Prop :=
  ∀ N : ℕ, 10 ^ 27 ≤ N → eq_14_51_first N ≤ 7.3306 * (N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N

/-! ### Sup norms -/

/-- `|η(t)| ≤ |η|_∞` for `t ≥ 0`, provided `|η|` is bounded on `[0, ∞)`. Then `⨆` is the genuine
supremum. -/
theorem eq_14_51_le_supNorm {η : ℝ → ℝ} {C : ℝ} (hC : ∀ t, 0 ≤ t → |η t| ≤ C) {t : ℝ}
    (ht : 0 ≤ t) : |η t| ≤ eq_14_51_supNorm η :=
  le_ciSup (f := fun s : Set.Ici (0:ℝ) => |η s|)
    ⟨C, by rintro _ ⟨s, rfl⟩; exact hC s s.2⟩ ⟨t, ht⟩

/-- A pointwise bound on `[0, ∞)` bounds `|η|_∞`. -/
theorem eq_14_51_supNorm_le {η : ℝ → ℝ} {C : ℝ} (hC : ∀ t, 0 ≤ t → |η t| ≤ C) :
    eq_14_51_supNorm η ≤ C :=
  haveI : Nonempty (Set.Ici (0:ℝ)) := ⟨⟨0, Set.self_mem_Ici⟩⟩
  ciSup_le fun s => hC s s.2

theorem eq_14_51_supNorm_nonneg (η : ℝ → ℝ) : 0 ≤ eq_14_51_supNorm η :=
  Real.iSup_nonneg fun _ => abs_nonneg _

/-- `|η₊(t)| ≤ |η₊|_∞` for `t ≥ 0`. -/
theorem eq_14_51_abs_etaPlus_le {t : ℝ} (ht : 0 ≤ t) : |etaPlus t| ≤ eq_14_51_supNorm etaPlus :=
  eq_14_51_le_supNorm (fun _ hs => TernaryGoldbach.Helfgott.abs_etaPlus_le_400 hs) ht

/-- `|η_*(t)| ≤ |η_*|_∞` for `t ≥ 0`. -/
theorem eq_14_51_abs_etaStar_le {t : ℝ} (ht : 0 ≤ t) : |etaStar t| ≤ eq_14_51_supNorm etaStar :=
  eq_14_51_le_supNorm (fun s _ => TernaryGoldbach.Helfgott.abs_etaStar_le_const s) ht

/-- The repo's crude bound gives `|η₊|_∞ ≤ 400`, the bound `nonprime_input` uses. [H, (14.3)] has
`1.079955`. -/
theorem eq_14_51_supNorm_etaPlus_le : eq_14_51_supNorm etaPlus ≤ 400 :=
  eq_14_51_supNorm_le fun _ hs => TernaryGoldbach.Helfgott.abs_etaPlus_le_400 hs

/-- The sharpest constant bound the repo states for `η₊` (`abs_etaPlus_le_A`) gives
`|η₊|_∞ ≤ 1.94`. [H, (14.3)] has `1.079955`. -/
theorem eq_14_51_supNorm_etaPlus_le_A : eq_14_51_supNorm etaPlus ≤ 1.94 :=
  eq_14_51_supNorm_le fun _ hs => TernaryGoldbach.Helfgott.abs_etaPlus_le_A hs

/-- The sharpest constant bound the repo states for `η_*` (`abs_etaStar_le_const`) gives
`|η_*|_∞ ≤ 6.2`. [H, (14.21)] has `1.414`. -/
theorem eq_14_51_supNorm_etaStar_le : eq_14_51_supNorm etaStar ≤ 6.2 :=
  eq_14_51_supNorm_le fun s _ => TernaryGoldbach.Helfgott.abs_etaStar_le_const s

/-! ### The first inequality of (14.51) -/

/-- Pointwise step: a term with some `nᵢ` even or non-prime is at most `A₊² A_*` times the sum
over `i` of the unweighted terms with `nᵢ` even or non-prime. -/
private theorem eq_14_51_step1_pt {Ap As x : ℝ} (hx : 0 ≤ x)
    (hAp : ∀ t, 0 ≤ t → |etaPlus t| ≤ Ap) (hAs : ∀ t, 0 ≤ t → |etaStar t| ≤ As) (N a b c : ℕ) :
    (if a + b + c = N ∧
        ((Even a ∨ ¬ a.Prime) ∨ (Even b ∨ ¬ b.Prime) ∨ (Even c ∨ ¬ c.Prime)) then
      Λ a * Λ b * Λ c * etaPlus (a / x) * etaPlus (b / x) * etaStar (c / x) else 0) ≤
    Ap ^ 2 * As * ((if a + b + c = N ∧ (Even a ∨ ¬ a.Prime) then Λ a * Λ b * Λ c else 0) +
      (if a + b + c = N ∧ (Even b ∨ ¬ b.Prime) then Λ a * Λ b * Λ c else 0) +
      (if a + b + c = N ∧ (Even c ∨ ¬ c.Prime) then Λ a * Λ b * Λ c else 0)) := by
  have hΛa : 0 ≤ Λ a := ArithmeticFunction.vonMangoldt_nonneg
  have hΛb : 0 ≤ Λ b := ArithmeticFunction.vonMangoldt_nonneg
  have hΛc : 0 ≤ Λ c := ArithmeticFunction.vonMangoldt_nonneg
  have hP : 0 ≤ Λ a * Λ b * Λ c := by positivity
  have hAp0 : 0 ≤ Ap := (abs_nonneg _).trans (hAp 0 le_rfl)
  have hAs0 : 0 ≤ As := (abs_nonneg _).trans (hAs 0 le_rfl)
  have hA : 0 ≤ Ap ^ 2 * As := by positivity
  have hm : ∀ (q : Prop) [Decidable q], 0 ≤ (if q then Λ a * Λ b * Λ c else 0) := fun q _ => by
    split_ifs
    exacts [hP, le_rfl]
  have hm1 := hm (a + b + c = N ∧ (Even a ∨ ¬ a.Prime))
  have hm2 := hm (a + b + c = N ∧ (Even b ∨ ¬ b.Prime))
  have hm3 := hm (a + b + c = N ∧ (Even c ∨ ¬ c.Prime))
  have hterm : Λ a * Λ b * Λ c * etaPlus (a / x) * etaPlus (b / x) * etaStar (c / x) ≤
      Ap ^ 2 * As * (Λ a * Λ b * Λ c) := by
    have h1 := hAp (a / x) (by positivity)
    have h2 := hAp (b / x) (by positivity)
    have h3 := hAs (c / x) (by positivity)
    calc Λ a * Λ b * Λ c * etaPlus (a / x) * etaPlus (b / x) * etaStar (c / x)
        ≤ |Λ a * Λ b * Λ c * etaPlus (a / x) * etaPlus (b / x) * etaStar (c / x)| := le_abs_self _
      _ = Λ a * Λ b * Λ c * |etaPlus (a / x)| * |etaPlus (b / x)| * |etaStar (c / x)| := by
          rw [abs_mul, abs_mul, abs_mul, abs_of_nonneg hP]
      _ ≤ Λ a * Λ b * Λ c * Ap * Ap * As := by gcongr
      _ = Ap ^ 2 * As * (Λ a * Λ b * Λ c) := by ring
  by_cases h0 : a + b + c = N ∧
      ((Even a ∨ ¬ a.Prime) ∨ (Even b ∨ ¬ b.Prime) ∨ (Even c ∨ ¬ c.Prime))
  · rw [ite_eq_left h0]
    refine hterm.trans (mul_le_mul_of_nonneg_left ?_ hA)
    obtain ⟨hS, hB | hB | hB⟩ := h0
    · have e : (if a + b + c = N ∧ (Even a ∨ ¬ a.Prime) then Λ a * Λ b * Λ c else 0) =
          Λ a * Λ b * Λ c := ite_eq_left ⟨hS, hB⟩
      linarith
    · have e : (if a + b + c = N ∧ (Even b ∨ ¬ b.Prime) then Λ a * Λ b * Λ c else 0) =
          Λ a * Λ b * Λ c := ite_eq_left ⟨hS, hB⟩
      linarith
    · have e : (if a + b + c = N ∧ (Even c ∨ ¬ c.Prime) then Λ a * Λ b * Λ c else 0) =
          Λ a * Λ b * Λ c := ite_eq_left ⟨hS, hB⟩
      linarith
  · rw [ite_eq_right h0]
    exact mul_nonneg hA (add_nonneg (add_nonneg hm1 hm2) hm3)

/-- Symmetry: the unweighted sum with `n₂` even or non-prime equals the one with `n₁`. -/
private theorem eq_14_51_sym2 (s : Finset ℕ) (N : ℕ) :
    (∑ a ∈ s, ∑ b ∈ s, ∑ c ∈ s,
        if a + b + c = N ∧ (Even b ∨ ¬ b.Prime) then Λ a * Λ b * Λ c else 0) =
      ∑ a ∈ s, ∑ b ∈ s, ∑ c ∈ s,
        if a + b + c = N ∧ (Even a ∨ ¬ a.Prime) then Λ a * Λ b * Λ c else 0 := by
  calc _ = ∑ b ∈ s, ∑ a ∈ s, ∑ c ∈ s,
        (if a + b + c = N ∧ (Even b ∨ ¬ b.Prime) then Λ a * Λ b * Λ c else 0) := Finset.sum_comm
    _ = _ := sum_congr rfl fun b _ => sum_congr rfl fun a _ => sum_congr rfl fun c _ => by
        rw [Nat.add_comm a b, mul_comm (Λ a) (Λ b)]

/-- Symmetry: the unweighted sum with `n₃` even or non-prime equals the one with `n₁`. -/
private theorem eq_14_51_sym3 (s : Finset ℕ) (N : ℕ) :
    (∑ a ∈ s, ∑ b ∈ s, ∑ c ∈ s,
        if a + b + c = N ∧ (Even c ∨ ¬ c.Prime) then Λ a * Λ b * Λ c else 0) =
      ∑ a ∈ s, ∑ b ∈ s, ∑ c ∈ s,
        if a + b + c = N ∧ (Even a ∨ ¬ a.Prime) then Λ a * Λ b * Λ c else 0 := by
  calc _ = ∑ a ∈ s, ∑ c ∈ s, ∑ b ∈ s,
        (if a + b + c = N ∧ (Even c ∨ ¬ c.Prime) then Λ a * Λ b * Λ c else 0) :=
        sum_congr rfl fun a _ => Finset.sum_comm
    _ = ∑ c ∈ s, ∑ a ∈ s, ∑ b ∈ s,
        (if a + b + c = N ∧ (Even c ∨ ¬ c.Prime) then Λ a * Λ b * Λ c else 0) := Finset.sum_comm
    _ = _ := sum_congr rfl fun c _ => sum_congr rfl fun a _ => sum_congr rfl fun b _ => by
        rw [show a + b + c = c + a + b by ring, show Λ a * Λ b * Λ c = Λ c * Λ a * Λ b by ring]

/-- The first inequality of (14.51), for any finite index set `s`, any `x ≥ 0` and any bounds
`A₊ ≥ |η₊|`, `A_* ≥ |η_*|` on `[0, ∞)`. -/
private theorem eq_14_51_step1 {Ap As x : ℝ} (hx : 0 ≤ x)
    (hAp : ∀ t, 0 ≤ t → |etaPlus t| ≤ Ap) (hAs : ∀ t, 0 ≤ t → |etaStar t| ≤ As)
    (s : Finset ℕ) (N : ℕ) :
    (∑ a ∈ s, ∑ b ∈ s, ∑ c ∈ s,
      if a + b + c = N ∧
          ((Even a ∨ ¬ a.Prime) ∨ (Even b ∨ ¬ b.Prime) ∨ (Even c ∨ ¬ c.Prime)) then
        Λ a * Λ b * Λ c * etaPlus (a / x) * etaPlus (b / x) * etaStar (c / x) else 0) ≤
    3 * Ap ^ 2 * As * ∑ a ∈ s, ∑ b ∈ s, ∑ c ∈ s,
        if a + b + c = N ∧ (Even a ∨ ¬ a.Prime) then Λ a * Λ b * Λ c else 0 := by
  calc _ ≤ ∑ a ∈ s, ∑ b ∈ s, ∑ c ∈ s,
        Ap ^ 2 * As * ((if a + b + c = N ∧ (Even a ∨ ¬ a.Prime) then Λ a * Λ b * Λ c else 0) +
          (if a + b + c = N ∧ (Even b ∨ ¬ b.Prime) then Λ a * Λ b * Λ c else 0) +
          (if a + b + c = N ∧ (Even c ∨ ¬ c.Prime) then Λ a * Λ b * Λ c else 0)) :=
        sum_le_sum fun a _ => sum_le_sum fun b _ => sum_le_sum fun c _ =>
          eq_14_51_step1_pt hx hAp hAs N a b c
    _ = Ap ^ 2 * As * ((∑ a ∈ s, ∑ b ∈ s, ∑ c ∈ s,
            if a + b + c = N ∧ (Even a ∨ ¬ a.Prime) then Λ a * Λ b * Λ c else 0) +
          (∑ a ∈ s, ∑ b ∈ s, ∑ c ∈ s,
            if a + b + c = N ∧ (Even b ∨ ¬ b.Prime) then Λ a * Λ b * Λ c else 0) +
          (∑ a ∈ s, ∑ b ∈ s, ∑ c ∈ s,
            if a + b + c = N ∧ (Even c ∨ ¬ c.Prime) then Λ a * Λ b * Λ c else 0)) := by
        simp only [mul_sum, mul_add, ← sum_add_distrib]
    _ = _ := by rw [eq_14_51_sym2, eq_14_51_sym3]; ring

/-! ### The second inequality of (14.51) -/

/-- The second inequality of (14.51) without the common factor: `n₃ = N - n₁ - n₂` is
determined by `n₁, n₂`, and `Λ(n₃) ≤ log N`. -/
private theorem eq_14_51_step2 (N : ℕ) (hN : 1 ≤ N) : eq_14_51_second N ≤ eq_14_51_third N := by
  unfold eq_14_51_second eq_14_51_third
  have hlogN : 0 ≤ Real.log N := by positivity
  have key : ∀ a ∈ Icc 1 N, ∀ b ∈ Icc 1 N,
      (∑ c ∈ Icc 1 N, if a + b + c = N ∧ (Even a ∨ ¬ a.Prime) then Λ a * Λ b * Λ c else 0) ≤
        (if Even a ∨ ¬ a.Prime then Λ a else 0) * Λ b * Real.log N := by
    intro a _ b _
    have hΛa : 0 ≤ Λ a := ArithmeticFunction.vonMangoldt_nonneg
    have hΛb : 0 ≤ Λ b := ArithmeticFunction.vonMangoldt_nonneg
    by_cases hB : Even a ∨ ¬ a.Prime
    · rw [ite_eq_left hB]
      calc (∑ c ∈ Icc 1 N, if a + b + c = N ∧ (Even a ∨ ¬ a.Prime) then Λ a * Λ b * Λ c else 0)
          ≤ ∑ c ∈ Icc 1 N, if c = N - a - b then Λ a * Λ b * Real.log N else 0 := by
            refine sum_le_sum fun c hc => ?_
            rw [mem_Icc] at hc
            split_ifs with h1 h2 h2
            · exact mul_le_mul_of_nonneg_left
                (TernaryGoldbach.Helfgott.vonMangoldt_le_log_of_le hN hc.2) (mul_nonneg hΛa hΛb)
            · exact absurd (by omega) h2
            · positivity
            · exact le_rfl
        _ ≤ Λ a * Λ b * Real.log N := by
            rw [sum_ite_eq']
            split_ifs
            · exact le_rfl
            · positivity
    · rw [ite_eq_right hB]
      simp [hB]
  calc (∑ a ∈ Icc 1 N, ∑ b ∈ Icc 1 N, ∑ c ∈ Icc 1 N,
          if a + b + c = N ∧ (Even a ∨ ¬ a.Prime) then Λ a * Λ b * Λ c else 0)
      ≤ ∑ a ∈ Icc 1 N, ∑ b ∈ Icc 1 N, (if Even a ∨ ¬ a.Prime then Λ a else 0) * Λ b *
          Real.log N := sum_le_sum fun a ha => sum_le_sum fun b hb => key a ha b hb
    _ = (∑ a ∈ Icc 1 N, if Even a ∨ ¬ a.Prime then Λ a else 0) * (∑ b ∈ Icc 1 N, Λ b) *
          Real.log N := by
        rw [sum_mul_sum, sum_mul]
        refine sum_congr rfl fun a _ => ?_
        rw [sum_mul]
    _ = _ := by
        rw [sum_filter]
        have : ∀ a ∈ Icc 1 N, (if Even a ∨ ¬ a.Prime then Λ a else 0) =
            (if ¬ a.Prime ∨ a = 2 then Λ a else 0) := fun a _ => by
          by_cases hp : a.Prime
          · simp [hp, hp.even_iff]
          · simp [hp]
        rw [sum_congr rfl this]
        ring

/-! ### (14.51) holds -/

/-- **(14.51) for every `N ≥ 1`**: both inequalities of the printed chain, with the true sup
norms `|η₊|_∞`, `|η_*|_∞` and `x = xOf N`. -/
theorem eq_14_51_chain (N : ℕ) (hN : 1 ≤ N) :
    eq_14_51_first N ≤
        3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_second N ∧
      3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_second N ≤
        3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_third N := by
  have hx : 0 ≤ xOf N :=
    (div_pos (by exact_mod_cast hN) TernaryGoldbach.Helfgott.xOf_denom_bounds.1).le
  have hAp := eq_14_51_supNorm_nonneg etaPlus
  have hAs := eq_14_51_supNorm_nonneg etaStar
  refine ⟨?_, mul_le_mul_of_nonneg_left (eq_14_51_step2 N hN) (by positivity)⟩
  exact eq_14_51_step1 hx (fun _ ht => eq_14_51_abs_etaPlus_le ht)
    (fun _ ht => eq_14_51_abs_etaStar_le ht) (Icc 1 N) N

/-- **[H, (14.51)] holds**, as printed, for every `N ≥ 10²⁷` (`eq_14_51_chain` covers every
`N ≥ 1`). No hypothesis of the repo is needed. -/
theorem eq_14_51_holds : eq_14_51 :=
  fun N hN => eq_14_51_chain N (le_trans (by norm_num) hN)

/-! ### Link with the formal objects -/

/-- Summing over `[1, N]` or `[0, N]` is the same when the `0` term vanishes. -/
private theorem eq_14_51_sum_Icc {F : ℕ → ℝ} (N : ℕ) (h : F 0 = 0) :
    ∑ n ∈ Icc 1 N, F n = ∑ n ∈ range (N + 1), F n := by
  refine sum_subset (fun n hn => ?_) (fun n hn hn' => ?_)
  · rw [mem_Icc] at hn
    rw [mem_range]
    omega
  · rw [mem_range] at hn
    rw [mem_Icc] at hn'
    obtain rfl : n = 0 := by omega
    exact h

/-- The triple-sum version of `eq_14_51_sum_Icc`. -/
private theorem eq_14_51_sum3_Icc {F : ℕ → ℕ → ℕ → ℝ} (N : ℕ)
    (h₁ : ∀ b c, F 0 b c = 0) (h₂ : ∀ a c, F a 0 c = 0) (h₃ : ∀ a b, F a b 0 = 0) :
    ∑ a ∈ Icc 1 N, ∑ b ∈ Icc 1 N, ∑ c ∈ Icc 1 N, F a b c =
      ∑ a ∈ range (N + 1), ∑ b ∈ range (N + 1), ∑ c ∈ range (N + 1), F a b c := by
  have e1 := eq_14_51_sum_Icc (F := fun a => ∑ b ∈ range (N + 1), ∑ c ∈ range (N + 1), F a b c)
    N (by simp [h₁])
  rw [← e1]
  refine sum_congr rfl fun a _ => ?_
  have e2 := eq_14_51_sum_Icc (F := fun b => ∑ c ∈ range (N + 1), F a b c) N (by simp [h₂])
  rw [← e2]
  exact sum_congr rfl fun b _ => eq_14_51_sum_Icc N (h₃ a b)

/-- "Even or non-prime" is "not an odd prime". -/
private theorem eq_14_51_bad_iff (n : ℕ) : (Even n ∨ ¬ n.Prime) ↔ ¬ (n.Prime ∧ Odd n) := by
  rw [not_and_or, Nat.not_odd_iff_even]
  exact or_comm

/-- **The first member of (14.51) is what `nonprime_input` bounds**: the weighted count of all
representations minus that of the representations by three odd primes. -/
theorem eq_14_51_first_eq (N : ℕ) :
    eq_14_51_first N = repSum (fun _ => True) N - repSum (fun n => n.Prime ∧ Odd n) N := by
  unfold eq_14_51_first repSum
  simp only [← sum_sub_distrib]
  refine (eq_14_51_sum3_Icc N (fun b c => by simp) (fun a c => by simp)
    (fun a b => by simp)).trans ?_
  refine sum_congr rfl fun a _ => sum_congr rfl fun b _ => sum_congr rfl fun c _ => ?_
  have hiff : ((Even a ∨ ¬ a.Prime) ∨ (Even b ∨ ¬ b.Prime) ∨ (Even c ∨ ¬ c.Prime)) ↔
      ¬ ((a.Prime ∧ Odd a) ∧ (b.Prime ∧ Odd b) ∧ (c.Prime ∧ Odd c)) := by
    rw [eq_14_51_bad_iff, eq_14_51_bad_iff, eq_14_51_bad_iff]
    tauto
  by_cases hS : a + b + c = N
  · by_cases hG : (a.Prime ∧ Odd a) ∧ (b.Prime ∧ Odd b) ∧ (c.Prime ∧ Odd c)
    · rw [ite_eq_right (fun h => hiff.1 h.2 hG), ite_eq_left ⟨hS, trivial, trivial, trivial⟩,
        ite_eq_left ⟨hS, hG⟩, sub_self]
    · rw [ite_eq_left ⟨hS, hiff.2 hG⟩, ite_eq_left ⟨hS, trivial, trivial, trivial⟩,
        ite_eq_right (fun h => hG h.2), sub_zero]
  · rw [ite_eq_right (fun h => hS h.1), ite_eq_right (fun h => hS h.1),
      ite_eq_right (fun h => hS h.1), sub_zero]

/-- `∑_{n ≤ N} Λ(n) = ψ(N)`. -/
theorem eq_14_51_sum_vonMangoldt (N : ℕ) : ∑ n ∈ Icc 1 N, Λ n = psi N :=
  eq_14_51_sum_Icc (F := fun n => Λ n) N ArithmeticFunction.map_zero

/-- `∑_{n ≤ N non-prime or n = 2} Λ(n) ≤ ψ(N) - θ(N) + log 2` (equality for `N ≥ 2`). -/
theorem eq_14_51_sum_bad_le (N : ℕ) :
    ∑ n ∈ Icc 1 N with (¬ n.Prime ∨ n = 2), Λ n ≤ psi N - theta N + Real.log 2 := by
  rw [sum_filter, eq_14_51_sum_Icc N (by simp)]
  refine le_trans (le_of_eq (sum_congr rfl fun n _ => ?_)) (TernaryGoldbach.Helfgott.sum_ΛBad_le N)
  unfold ΛBad TernaryGoldbach.Helfgott.Good
  by_cases hp : n.Prime
  · by_cases h2 : n = 2
    · subst h2
      simp [hp]
    · simp [hp, h2, hp.odd_of_ne_two h2]
  · simp [hp]

/-! ### Relations with `nonprime_input` and `repSum_sub_le_of_bounds` -/

/-- **(14.51) implies `nonprime_input`.** Insert the repo's crude inputs into the third member:
`|η₊|_∞ ≤ 400`, `|η_*|_∞ ≤ 6.2`, `∑_{n₁ ≤ N non-prime or n₁ = 2} Λ(n₁) ≤ ψ(N) - θ(N) + log 2
≤ 1.6 √N + log 2 ≤ 1.6001 √N` and `∑_{n₂ ≤ N} Λ(n₂) = ψ(N) ≤ 1.387 N`. Then
`3·400²·6.2·1.6001·1.387 ≈ 6.6048·10⁶ ≤ 6.7·10⁶`. This is the formalization's own route to
`nonprime_input`, and the proof does not use `nonprime_input`. -/
theorem eq_14_51_implies_formal :
    eq_14_51 → type_of% @TernaryGoldbach.Helfgott.nonprime_input := by
  intro h N hN
  obtain ⟨h1, h2⟩ := h N hN
  have hNr : (10 : ℝ) ^ 27 ≤ N := by exact_mod_cast hN
  have hsq : (10 : ℝ) ^ 13 ≤ √N := Real.le_sqrt_of_sq_le (by nlinarith)
  have hlog2 : Real.log 2 ≤ 0.0001 * √N := by
    have := Real.log_two_lt_d9
    nlinarith
  have hP1 : ∑ n ∈ Icc 1 N with (¬ n.Prime ∨ n = 2), Λ n ≤ 1.6001 * √N := by
    have := eq_14_51_sum_bad_le N
    have := TernaryGoldbach.Helfgott.psi_sub_theta_le N hN
    linarith
  have hP10 : 0 ≤ ∑ n ∈ Icc 1 N with (¬ n.Prime ∨ n = 2), Λ n :=
    sum_nonneg fun _ _ => ArithmeticFunction.vonMangoldt_nonneg
  have hP2 : ∑ n ∈ Icc 1 N, Λ n ≤ 1.387 * N := by
    rw [eq_14_51_sum_vonMangoldt]
    exact TernaryGoldbach.Helfgott.psi_le N hN
  have hP20 : 0 ≤ ∑ n ∈ Icc 1 N, Λ n := sum_nonneg fun _ _ => ArithmeticFunction.vonMangoldt_nonneg
  have hAp := eq_14_51_supNorm_etaPlus_le
  have hAp0 := eq_14_51_supNorm_nonneg etaPlus
  have hAs := eq_14_51_supNorm_etaStar_le
  have hAs0 := eq_14_51_supNorm_nonneg etaStar
  rw [← eq_14_51_first_eq]
  calc eq_14_51_first N
      ≤ 3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_third N :=
        h1.trans h2
    _ ≤ 3 * 400 ^ 2 * 6.2 * (Real.log N * (1.6001 * √N) * (1.387 * N)) := by
        unfold eq_14_51_third
        gcongr
    _ = (3 * 400 ^ 2 * 6.2 * 1.6001 * 1.387) * (N * √N) * Real.log N := by ring
    _ ≤ 6.7e6 * (N * √N) * Real.log N := by gcongr; norm_num

/-- **The printed chain, at every `N ≥ 1`, implies the repo's parametric (14.51)**,
`TernaryGoldbach.Helfgott.repSum_sub_le_of_bounds` ("[H13, (7.50)] with the constants as
parameters"; [H13, (7.50)] is identical to (14.51)). Given bounds `A₊ ≥ |η₊|`, `A_* ≥ |η_*|` on
`[0, ∞)`, bound the sup norms by them (`eq_14_51_supNorm_le`), the sum over non-prime `n₁` and
`n₁ = 2` by `ψ(N) - θ(N) + log 2` (`eq_14_51_sum_bad_le`) and `∑_{n₂ ≤ N} Λ(n₂)` by `ψ(N)`
(`eq_14_51_sum_vonMangoldt`). The first member is the repo's
`repSum (fun _ => True) N - repSum Good N` (`eq_14_51_first_eq`; `Good n` is
`n.Prime ∧ Odd n` by definition).

The hypothesis is the chain of `eq_14_51` at every `N ≥ 1`, not only at `N ≥ 10²⁷`, because the
repo lemma covers every `N ≥ 1`. `eq_14_51_chain` proves this hypothesis, so
`eq_14_51_chain_implies_formal eq_14_51_chain` reproves the repo lemma; the proof does not call
`repSum_sub_le_of_bounds`. -/
theorem eq_14_51_chain_implies_formal
    (h : ∀ N : ℕ, 1 ≤ N →
      eq_14_51_first N ≤
          3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_second N ∧
        3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_second N ≤
          3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_third N) :
    type_of% @TernaryGoldbach.Helfgott.repSum_sub_le_of_bounds := by
  intro N hN Ap As hAp hAs
  obtain ⟨h1, h2⟩ := h N hN
  have hS1 := eq_14_51_supNorm_le hAp
  have hS2 := eq_14_51_supNorm_le hAs
  have hS10 := eq_14_51_supNorm_nonneg etaPlus
  have hS20 := eq_14_51_supNorm_nonneg etaStar
  have hAp0 : 0 ≤ Ap := hS10.trans hS1
  have hAs0 : 0 ≤ As := hS20.trans hS2
  have hb := eq_14_51_sum_bad_le N
  have hb0 : 0 ≤ ∑ n ∈ Icc 1 N with (¬ n.Prime ∨ n = 2), Λ n :=
    sum_nonneg fun _ _ => ArithmeticFunction.vonMangoldt_nonneg
  have hp0 : 0 ≤ psi N := by
    rw [← eq_14_51_sum_vonMangoldt]
    exact sum_nonneg fun _ _ => ArithmeticFunction.vonMangoldt_nonneg
  have hlog : 0 ≤ Real.log N := Real.log_nonneg (by exact_mod_cast hN)
  change repSum (fun _ => True) N - repSum (fun n => n.Prime ∧ Odd n) N ≤ _
  rw [← eq_14_51_first_eq]
  calc eq_14_51_first N
      ≤ 3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_third N :=
        h1.trans h2
    _ ≤ 3 * Ap ^ 2 * As * (Real.log N * (psi N - theta N + Real.log 2) * psi N) := by
        unfold eq_14_51_third
        rw [eq_14_51_sum_vonMangoldt]
        gcongr
    _ = 3 * (Ap ^ 2 * As) * Real.log N * (psi N - theta N + Real.log 2) * psi N := by ring

/-! ### [H]'s numerical conclusion -/

/-- `N^{3/2} = N √N` for `N > 0`. -/
private theorem eq_14_51_rpow_three_halves {N : ℝ} (hN : 0 < N) : N ^ ((3 : ℝ) / 2) = N * √N := by
  rw [show (3 : ℝ) / 2 = 1 + 1 / 2 by norm_num, Real.rpow_add hN, Real.rpow_one,
    Real.sqrt_eq_rpow]

/-- **[H]'s numerical conclusion implies `nonprime_input`.** The quantity and the range
`N ≥ 10²⁷` are the same, the constant is weaker (`7.3306 ≤ 6.7·10⁶`), and `N^{3/2} = N √N`. -/
theorem eq_14_51_bound_implies_formal :
    eq_14_51_bound → type_of% @TernaryGoldbach.Helfgott.nonprime_input := by
  intro h N hN
  have hN0 : (0 : ℝ) < N := by exact_mod_cast lt_of_lt_of_le (by norm_num) hN
  rw [← eq_14_51_first_eq]
  calc eq_14_51_first N ≤ 7.3306 * (N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N := h N hN
    _ = 7.3306 * (N * √N) * Real.log N := by rw [eq_14_51_rpow_three_halves hN0]
    _ ≤ 6.7e6 * (N * √N) * Real.log N := by gcongr; norm_num

/-- [H]'s computation after (14.51), with the sup-norm bounds as parameters: if
`|η₊|_∞ ≤ A₊`, `|η_*|_∞ ≤ A_*`, `ψ(N) < 1.03883 N` and `ψ(N) - θ(N) < 1.4262 √N` for a natural
`N ≥ 10²⁷`, then (14.51) bounds its first member by
`3 A₊² A_* · 1.4263 · 1.03883 · N^{3/2} log N`. -/
private theorem eq_14_51_first_le_of {Ap As : ℝ} (hAp : eq_14_51_supNorm etaPlus ≤ Ap)
    (hAs : eq_14_51_supNorm etaStar ≤ As) {N : ℕ} (hN : 10 ^ 27 ≤ N)
    (hψ : psi N < 1.03883 * N) (hψθ : psi N - theta N < 1.4262 * √N) :
    eq_14_51_first N ≤
      3 * Ap ^ 2 * As * 1.4263 * 1.03883 * ((N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N) := by
  obtain ⟨h1, h2⟩ := eq_14_51_holds N hN
  have hN0 : (0 : ℝ) < N := by exact_mod_cast lt_of_lt_of_le (by norm_num) hN
  have hNr : (10 : ℝ) ^ 27 ≤ N := by exact_mod_cast hN
  have hsq : (10 : ℝ) ^ 13 ≤ √N := Real.le_sqrt_of_sq_le (by nlinarith)
  have hlog2 : Real.log 2 ≤ 0.0001 * √N := by
    have := Real.log_two_lt_d9
    nlinarith
  have hP1 : ∑ n ∈ Icc 1 N with (¬ n.Prime ∨ n = 2), Λ n ≤ 1.4263 * √N := by
    have := eq_14_51_sum_bad_le N
    linarith
  have hP10 : 0 ≤ ∑ n ∈ Icc 1 N with (¬ n.Prime ∨ n = 2), Λ n :=
    sum_nonneg fun _ _ => ArithmeticFunction.vonMangoldt_nonneg
  have hP2 : ∑ n ∈ Icc 1 N, Λ n ≤ 1.03883 * N := by
    rw [eq_14_51_sum_vonMangoldt]
    exact hψ.le
  have hP20 : 0 ≤ ∑ n ∈ Icc 1 N, Λ n := sum_nonneg fun _ _ => ArithmeticFunction.vonMangoldt_nonneg
  have hS10 := eq_14_51_supNorm_nonneg etaPlus
  have hS20 := eq_14_51_supNorm_nonneg etaStar
  have hAp0 : 0 ≤ Ap := hS10.trans hAp
  have hAs0 : 0 ≤ As := hS20.trans hAs
  rw [eq_14_51_rpow_three_halves hN0]
  calc eq_14_51_first N
      ≤ 3 * eq_14_51_supNorm etaPlus ^ 2 * eq_14_51_supNorm etaStar * eq_14_51_third N :=
        h1.trans h2
    _ ≤ 3 * Ap ^ 2 * As * (Real.log N * (1.4263 * √N) * (1.03883 * N)) := by
        unfold eq_14_51_third
        gcongr
    _ = 3 * Ap ^ 2 * As * 1.4263 * 1.03883 * (N * √N * Real.log N) := by ring

/-- **[H]'s derivation of `7.3306 N^{3/2} log N` is correct, given its inputs.** Assume the
inputs [H] quotes after (14.51): `|η₊|_∞ ≤ 1.079955` (14.3), `|η_*|_∞ ≤ 1.414` (14.21), and the
Rosser–Schoenfeld bounds [RS62, Thms. 12, 13] `ψ(N) < 1.03883 N` and `ψ(N) - θ(N) < 1.4262 √N`,
needed here only for natural `N ≥ 10²⁷`. Then (14.51), proved above, gives `eq_14_51_bound`. The
first member is then at most `3 · 1.079955² · 1.414 · 1.4263 · 1.03883 · N^{3/2} log N`, and
`3 · 1.079955² · 1.414 · 1.4263 · 1.03883 ≈ 7.330563 ≤ 7.3306`. [H] goes through
`1.4263 · 1.03883 ≤ 1.48169` instead and gets `≈ 7.330597`, also `≤ 7.3306`.

The formalization proves the two Rosser–Schoenfeld inputs (`eq_14_51_psi_lt`,
`eq_14_51_psi_sub_theta_lt`, from the repo's `TernaryGoldbach.Prelim.sum_vonMangoldt_lt` and
`TernaryGoldbach.Prelim.sum_vonMangoldt_nonprime_lt` under `[Fact PlattGRH]`), and
`eq_14_51_bound_of_supNorms` discharges them. It does not prove the sup norms (14.3) and (14.21):
the sharpest constant bounds it states give `1.94` (`eq_14_51_supNorm_etaPlus_le_A`) and `6.2`
(`eq_14_51_supNorm_etaStar_le`) instead. -/
theorem eq_14_51_bound_of_inputs
    (hAp : eq_14_51_supNorm etaPlus ≤ 1.079955) (hAs : eq_14_51_supNorm etaStar ≤ 1.414)
    (hψ : ∀ N : ℕ, 10 ^ 27 ≤ N → psi N < 1.03883 * N)
    (hψθ : ∀ N : ℕ, 10 ^ 27 ≤ N → psi N - theta N < 1.4262 * √N) :
    eq_14_51_bound := by
  intro N hN
  have hX : 0 ≤ (N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N := by positivity
  calc eq_14_51_first N
      ≤ 3 * 1.079955 ^ 2 * 1.414 * 1.4263 * 1.03883 *
          ((N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N) :=
        eq_14_51_first_le_of hAp hAs hN (hψ N hN) (hψθ N hN)
    _ ≤ 7.3306 * ((N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N) :=
        mul_le_mul_of_nonneg_right (by norm_num) hX
    _ = 7.3306 * (N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N := by ring

/-! ### The Rosser–Schoenfeld inputs, from the repo -/

/-- `ψ(N) - θ(N) = ∑_{n ≤ N, n not prime} Λ(n)`. -/
private theorem eq_14_51_psi_sub_theta (N : ℕ) :
    psi N - theta N = ∑ n ∈ Icc 1 N, (if n.Prime then 0 else Λ n) := by
  rw [eq_14_51_sum_Icc N (by simp)]
  unfold psi theta
  rw [← sum_sub_distrib]
  refine sum_congr rfl fun n _ => ?_
  split_ifs <;> ring

/-- **[RS62, Thm. 12]** at a natural number `N ≥ 1`: `ψ(N) < 1.03883 N`. This is the repo's
`TernaryGoldbach.Prelim.sum_vonMangoldt_lt` at `y = N`. -/
theorem eq_14_51_psi_lt [Fact TernaryGoldbach.PlattGRH] {N : ℕ}
    (hN : 1 ≤ N) : psi N < 1.03883 * N := by
  have h := TernaryGoldbach.Prelim.sum_vonMangoldt_lt (y := (N : ℝ)) (by exact_mod_cast hN)
  rwa [Nat.floor_natCast, eq_14_51_sum_vonMangoldt] at h

/-- **[RS62, Thm. 13]** at a natural number `N ≥ 1`: `ψ(N) - θ(N) < 1.4262 √N`. This is the
repo's `TernaryGoldbach.Prelim.sum_vonMangoldt_nonprime_lt` at `y = N`. -/
theorem eq_14_51_psi_sub_theta_lt [Fact TernaryGoldbach.PlattGRH]
    {N : ℕ} (hN : 1 ≤ N) : psi N - theta N < 1.4262 * √N := by
  have h := TernaryGoldbach.Prelim.sum_vonMangoldt_nonprime_lt (y := (N : ℝ))
    (by exact_mod_cast hN)
  rwa [Nat.floor_natCast, ← eq_14_51_psi_sub_theta] at h

/-- **Only the sharp sup norms are missing.** Under `[Fact PlattGRH]`, the repo
proves [RS62, Thms. 12, 13] (`eq_14_51_psi_lt`, `eq_14_51_psi_sub_theta_lt`), so [H]'s
`|η₊|_∞ ≤ 1.079955` (14.3) and `|η_*|_∞ ≤ 1.414` (14.21) alone give `eq_14_51_bound`, through
(14.51) (`eq_14_51_bound_of_inputs`). -/
theorem eq_14_51_bound_of_supNorms [Fact TernaryGoldbach.PlattGRH]
    (hAp : eq_14_51_supNorm etaPlus ≤ 1.079955) (hAs : eq_14_51_supNorm etaStar ≤ 1.414) :
    eq_14_51_bound :=
  eq_14_51_bound_of_inputs hAp hAs (fun _ hN => eq_14_51_psi_lt (le_trans (by norm_num) hN))
    (fun _ hN => eq_14_51_psi_sub_theta_lt (le_trans (by norm_num) hN))

/-- **What [H]'s route gives with the formalization's own inputs.** With the repo's sup-norm
bounds `|η₊| ≤ 1.94` (`abs_etaPlus_le_A`) and `|η_*| ≤ 6.2` (`abs_etaStar_le_const`) in place of
(14.3) and (14.21), and its Rosser–Schoenfeld theorems, (14.51) bounds the first member by
`103.73 N^{3/2} log N` for `N ≥ 10²⁷`, since `3 · 1.94² · 6.2 · 1.4263 · 1.03883 ≈ 103.7222`.
This is weaker than [H]'s `7.3306` and stronger than the `6.7·10⁶` of `nonprime_input`, which
uses no `Fact`. -/
theorem eq_14_51_first_le_repo [Fact TernaryGoldbach.PlattGRH]
    (N : ℕ) (hN : 10 ^ 27 ≤ N) :
    eq_14_51_first N ≤ 103.73 * (N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N := by
  have hN1 : 1 ≤ N := le_trans (by norm_num) hN
  have hX : 0 ≤ (N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N := by positivity
  calc eq_14_51_first N
      ≤ 3 * 1.94 ^ 2 * 6.2 * 1.4263 * 1.03883 * ((N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N) :=
        eq_14_51_first_le_of eq_14_51_supNorm_etaPlus_le_A eq_14_51_supNorm_etaStar_le hN
          (eq_14_51_psi_lt hN1) (eq_14_51_psi_sub_theta_lt hN1)
    _ ≤ 103.73 * ((N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N) :=
        mul_le_mul_of_nonneg_right (by norm_num) hX
    _ = 103.73 * (N : ℝ) ^ ((3 : ℝ) / 2) * Real.log N := by ring

end Companion.Book
