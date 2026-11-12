import TernaryGoldbach

/-!
# [H, Lemma 4.1.3]: sums of `min(B/|sin παn|, C/|sin παn|²)` over `y₁ < n ≤ y₂`, `q ∤ n`

H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, Lemma 4.1.3 (`lem:thina`),
§4.1, p. 55, equation (4.6): <https://arxiv.org/pdf/1501.05438v2#page=65>.
(The 2013 preprint arXiv:1205.5252v4 has it as Lemma 3.3, identical up to notation.)

## What [H] states

Let `α = a/q + β/qQ`, `(a, q) = 1`, `|β| ≤ 1`, `q ≤ Q`. Let `y₂ > y₁ ≥ 0`. If `y₂ - y₁ ≤ q` and
`y₂ ≤ Q/2`, then for any `B, C ≥ 0`

  `∑_{y₁ < n ≤ y₂, q ∤ n} min(B/|sin(παn)|, C/|sin(παn)|²) ≤ 2B (q/π) max(2, log(Ce³q/(Bπ)))`
  (4.6),

and "the upper bound `≤ (2Bq/π) log(2e²q/π)` is also valid". `lemma_4_1_3` below is this
statement, with both bounds.

## What the formalization proves

`TernaryGoldbach.MinorArcs.lemma_4_1_3` (`TernaryGoldbach/MinorArcs/TrigSums.lean`) proves both
bounds under the same hypotheses. `Approx α a q Q` packs `1 ≤ q`, `IsCoprime a q` and
`∃ β, |β| ≤ 1 ∧ α = a/q + β/(qQ) ∧ q ≤ Q`. The other hypotheses are `0 ≤ y₁`, `y₁ < y₂`,
`y₂ - y₁ ≤ q`, `y₂ ≤ Q/2`, `0 ≤ B`, `0 ≤ C`. The Lean sum runs over all of
`Finset.Ioc ⌊y₁⌋ ⌊y₂⌋`, with the terms where `q ∣ n` set to `0`. It writes `sin²` where [H] writes
`|sin|²`, and `2Bq/π` where (4.6) writes `2B(q/π)`. The theorem uses only `propext`,
`Classical.choice` and `Quot.sound`, and it is in the dependency cone of the main theorem.

## Relation, as certified here: proved

* `lemma_4_1_3_iff_formal : lemma_4_1_3 ↔ type_of% @TernaryGoldbach.MinorArcs.lemma_4_1_3`. The
  printed statement and the Lean statement are the same proposition up to encoding. The proof uses
  neither theorem. It repacks the hypotheses (`Int.gcd a q = 1 ↔ IsCoprime a q`, `0 < q ↔ 1 ≤ q`)
  and rewrites the sum (`lemma_4_1_3_lhs_eq`) and the constant `2B(q/π) = 2Bq/π`.
* `lemma_4_1_3_holds : lemma_4_1_3` follows from the Lean theorem through that equivalence.

Checks on the transcription:
* `lemma_4_1_3_mem_index`: the range of summation is exactly `{n ∈ ℤ : y₁ < n ≤ y₂, q ∤ n}`.
* `lemma_4_1_3_sin_ne_zero`: under the hypotheses no summand divides by zero, so Lean's convention
  `x / 0 = 0` never applies on the left side.
* `lemma_4_1_3_hypotheses_satisfiable`: the hypotheses can all hold with a non-empty sum, so the
  statement is not vacuous.
* `lemma_4_1_3_example`: at those parameters the left side is `min(B, C)`
  (`lemma_4_1_3_example_lhs`), so the statement contains a concrete inequality there.

## On [H]'s proof (not used here; recorded for the reader)

The printed statement is true, but [H]'s proof does not cover small `C`. Write
`h(t) = min(B/sin(πt/q), C/sin²(πt/q))`. [H] first bounds the left side by
`2 ∑_{1 ≤ r ≤ q/2} h(r - 1/2)`, "as in the proof of Lemma 4.1.2". It then proves the bound for
`B sin(π/q) ≤ C ≤ B` and reduces `C > B` to `C = B`. For `C < B sin(π/q)` it "relaxes the input to
`C = B sin π/q`".

That last step is the gap. For `C ≤ Bπ/(eq)`, which lies inside this range, (4.6) claims the
constant `max(2, log(Ce³q/(Bπ))) = 2` in front of `2Bq/π`. The relaxed argument only gives
`log(e³ q sin(π/q)/π)`, which is at least `log(2e³/π) ≈ 2.548`. Stopping before [H]'s last
simplification gives `π/(q sin(π/2q)) + cos(π/q)`, which is at least `2.221`. The case cannot be
rescued after the first step either. Take `q = 140` and `C = Bπ/(2q)`, so that the right side of
(4.6) is `(2Bq/π) log(e³/2)`. The intermediate sum `2 ∑ h(r - 1/2)` is then about `1.0696` times
that right side. The ratio is already about `1.0088` for `q = 2`, `C = B/√2`. On the range
`B sin(π/q) ≤ C ≤ B` the intermediate sum stayed below the right side on every grid we tried. All
these numbers were recomputed in double precision for this file.

The formalization proves (4.6) by a sharper first step. In units of `1/q`, the distances from the
points `αn` (`q ∤ n`) to the nearest integer are bounded below by distinct elements of
`{1/2, 1, 3/2, …}`. Hence the sum is at most `∑_{1 ≤ j ≤ q-1} h(j/2)`, where [H] has
`2 ∑_{r ≤ q/2} h(r - 1/2)`. The module docstring of `TernaryGoldbach/MinorArcs/TrigSums.lean`
describes this argument and reports the same issue with [H]'s proof.
-/

open Real

namespace Companion.Book

/-- **[H, Lemma 4.1.3]**, p. 55, equation (4.6) and the sentence after it, as printed.

Transcription choices:
* The letters of the statement, `α, a, q, β, Q, y₁, y₂, B, C`, are universally quantified.
  `α, β, Q, y₁, y₂, B, C` are real, `a` is an integer, and `q` is a natural number with `0 < q`.
  [H] leaves `q ≥ 1` implicit, since `q` is the denominator of `a/q`.
* "Let `α = a/q + β/qQ`" becomes the hypothesis `α = a / q + β / (q * Q)`: in [H], `β/qQ` means
  `β/(qQ)`. `(a, q) = 1` becomes `Int.gcd a q = 1`. `|β| ≤ 1` and `q ≤ Q` are copied as they
  stand.
* "`y₂ > y₁ ≥ 0`" becomes `0 ≤ y₁` and `y₁ < y₂`. `y₂ - y₁ ≤ q` and `y₂ ≤ Q/2` are copied as
  they stand.
* `∑_{y₁ < n ≤ y₂, q ∤ n}` is the sum over the integers `n` in `(y₁, y₂]` with `q ∤ n`. It is
  written as the `Finset` sum over `Finset.Ioc ⌊y₁⌋ ⌊y₂⌋` filtered by `¬ (q : ℤ) ∣ n`, which is
  exactly that set (`lemma_4_1_3_mem_index`).
* The summand is copied as printed, `min (B / |sin (π α n)|) (C / |sin (π α n)| ^ 2)`. Under the
  hypotheses `sin (π α n) ≠ 0` for every `n` in the range (`lemma_4_1_3_sin_ne_zero`), so no
  division by zero occurs on the left.
* The right side of (4.6) is `2 * B * (q / π) * max 2 (log (C * exp 3 * q / (B * π)))`. Here
  `log` is the natural logarithm `Real.log`, and `e³ = Real.exp 3`.
* "The upper bound `≤ (2Bq/π) log(2e²q/π)` is also valid" holds under the same hypotheses. It is
  the second conjunct, `2 * B * q / π * log (2 * exp 2 * q / π)`.
* Degenerate inputs, where Lean's junk values replace expressions that [H] leaves undefined:
  - `B = 0`: [H]'s `Ce³q/(Bπ)` is undefined, and Lean reads it as `0`. The right side is then
    `0`, and so is the left side, since every term is `min 0 (C / sin²) = 0`. The bound reads
    `0 ≤ 0`.
  - `C = 0 < B`: [H]'s `log 0 = -∞` gives `max(2, log 0) = 2`. Lean's `Real.log 0 = 0` gives
    `max 2 0 = 2` as well.
  - In all other cases the argument of every `log` is positive, so no junk value appears.

The repository's definitions are not reused here: the statement involves only real arithmetic,
`sin`, `exp` and `log`. -/
def lemma_4_1_3 : Prop :=
  ∀ (α : ℝ) (a : ℤ) (q : ℕ) (β Q : ℝ),
    0 < q → Int.gcd a q = 1 → |β| ≤ 1 → (q : ℝ) ≤ Q → α = a / q + β / (q * Q) →
    ∀ y₁ y₂ : ℝ, 0 ≤ y₁ → y₁ < y₂ → y₂ - y₁ ≤ q → y₂ ≤ Q / 2 →
    ∀ B C : ℝ, 0 ≤ B → 0 ≤ C →
      (∑ n ∈ Finset.Ioc ⌊y₁⌋ ⌊y₂⌋ with ¬ (q : ℤ) ∣ n,
          min (B / |Real.sin (π * α * n)|) (C / |Real.sin (π * α * n)| ^ 2)) ≤
        2 * B * (q / π) * max 2 (Real.log (C * Real.exp 3 * q / (B * π))) ∧
      (∑ n ∈ Finset.Ioc ⌊y₁⌋ ⌊y₂⌋ with ¬ (q : ℤ) ∣ n,
          min (B / |Real.sin (π * α * n)|) (C / |Real.sin (π * α * n)| ^ 2)) ≤
        2 * B * q / π * Real.log (2 * Real.exp 2 * q / π)

/-- Transcription check: the range of summation in `lemma_4_1_3` is
`{n ∈ ℤ : y₁ < n ≤ y₂, q ∤ n}`. -/
theorem lemma_4_1_3_mem_index {y₁ y₂ : ℝ} {q : ℕ} {n : ℤ} :
    n ∈ {n ∈ Finset.Ioc ⌊y₁⌋ ⌊y₂⌋ | ¬ (q : ℤ) ∣ n} ↔
      y₁ < n ∧ (n : ℝ) ≤ y₂ ∧ ¬ (q : ℤ) ∣ n := by
  simp only [Finset.mem_filter, Finset.mem_Ioc, Int.floor_lt, Int.le_floor, and_assoc]

/-- Transcription check: under the hypotheses of `lemma_4_1_3`, `sin(παn) ≠ 0` for every `n` in
the range of summation. So the summands of (4.6) are genuine real numbers, and Lean's `x / 0 = 0`
does not enter the left side. -/
theorem lemma_4_1_3_sin_ne_zero {α : ℝ} {a : ℤ} {q : ℕ} {β Q : ℝ} (hq : 0 < q)
    (hgcd : Int.gcd a q = 1) (hβ : |β| ≤ 1) (hqQ : (q : ℝ) ≤ Q) (hα : α = a / q + β / (q * Q))
    {y₁ y₂ : ℝ} (hy : 0 ≤ y₁) (hy₂ : y₂ ≤ Q / 2) {n : ℤ}
    (hn : n ∈ {n ∈ Finset.Ioc ⌊y₁⌋ ⌊y₂⌋ | ¬ (q : ℤ) ∣ n}) :
    Real.sin (π * α * n) ≠ 0 := by
  obtain ⟨h1, h2, h3⟩ := lemma_4_1_3_mem_index.mp hn
  refine TernaryGoldbach.MinorArcs.sin_ne_zero_of_approx
    ⟨hq, Int.isCoprime_iff_gcd_eq_one.mpr hgcd, β, hβ, hα, hqQ⟩ h3 ?_
  rw [abs_of_nonneg (by linarith)]
  linarith

/-- Non-vacuity: all hypotheses of `lemma_4_1_3` can hold with a non-empty range of summation.
Take `q = 2`, `a = 1`, `β = 0`, `Q = 2`, `α = 1/2`, `y₁ = 0`, `y₂ = 1`. The sum is then the single
term `n = 1`, namely `min(B, C)`. -/
theorem lemma_4_1_3_hypotheses_satisfiable :
    ∃ (α : ℝ) (a : ℤ) (q : ℕ) (β Q y₁ y₂ : ℝ),
      0 < q ∧ Int.gcd a q = 1 ∧ |β| ≤ 1 ∧ (q : ℝ) ≤ Q ∧ α = a / q + β / (q * Q) ∧
      0 ≤ y₁ ∧ y₁ < y₂ ∧ y₂ - y₁ ≤ q ∧ y₂ ≤ Q / 2 ∧
      ({n ∈ Finset.Ioc ⌊y₁⌋ ⌊y₂⌋ | ¬ (q : ℤ) ∣ n}).Nonempty := by
  refine ⟨1 / 2, 1, 2, 0, 2, 0, 1, by norm_num, by decide, by norm_num, le_refl _, by norm_num,
    le_refl _, by norm_num, by norm_num, by norm_num, ⟨1, ?_⟩⟩
  rw [lemma_4_1_3_mem_index]
  refine ⟨by norm_num, by norm_num, by decide⟩

/-- Take the parameters of `lemma_4_1_3_hypotheses_satisfiable` (`q = 2`, `α = 1/2`, `y₁ = 0`,
`y₂ = 1`). The left side of (4.6) is then `min B C`. -/
theorem lemma_4_1_3_example_lhs (B C : ℝ) :
    (∑ n ∈ Finset.Ioc ⌊(0 : ℝ)⌋ ⌊(1 : ℝ)⌋ with ¬ ((2 : ℕ) : ℤ) ∣ n,
        min (B / |Real.sin (π * (1 / 2) * n)|) (C / |Real.sin (π * (1 / 2) * n)| ^ 2)) =
      min B C := by
  rw [Int.floor_zero, Int.floor_one]
  have hs : {n ∈ Finset.Ioc (0 : ℤ) 1 | ¬ ((2 : ℕ) : ℤ) ∣ n} = {1} := by
    ext n
    simp only [Finset.mem_filter, Finset.mem_Ioc, Finset.mem_singleton]
    constructor
    · rintro ⟨⟨h0, h1⟩, -⟩
      omega
    · rintro rfl
      exact ⟨⟨by norm_num, le_refl _⟩, by decide⟩
  have hsin : Real.sin (π * (1 / 2) * ((1 : ℤ) : ℝ)) = 1 := by
    rw [show π * (1 / 2) * ((1 : ℤ) : ℝ) = π / 2 by push_cast; ring]
    exact Real.sin_pi_div_two
  rw [hs, Finset.sum_singleton, hsin, abs_one, one_pow, div_one, div_one]

/-- Non-vacuity of the conclusion. At the parameters of `lemma_4_1_3_hypotheses_satisfiable`
(`q = 2`, `a = 1`, `β = 0`, `Q = 2`, `α = 1/2`, `y₁ = 0`, `y₂ = 1`), `lemma_4_1_3` yields two
concrete claims. They are `min(B, C) ≤ 2B(2/π) max(2, log(2Ce³/(Bπ)))` and
`min(B, C) ≤ (4B/π) log(4e²/π)`. -/
theorem lemma_4_1_3_example (h : lemma_4_1_3) {B C : ℝ} (hB : 0 ≤ B) (hC : 0 ≤ C) :
    min B C ≤ 2 * B * (2 / π) * max 2 (Real.log (C * Real.exp 3 * 2 / (B * π))) ∧
    min B C ≤ 2 * B * 2 / π * Real.log (2 * Real.exp 2 * 2 / π) := by
  have := h (1 / 2) 1 2 0 2 (by norm_num) (by decide) (by norm_num) (le_refl _) (by norm_num)
    0 1 le_rfl (by norm_num) (by norm_num) (by norm_num) B C hB hC
  rwa [lemma_4_1_3_example_lhs, Nat.cast_ofNat] at this

/-- The left side of (4.6) as printed (a sum over `q ∤ n`, with `|sin|²`) equals the left side of
`TernaryGoldbach.MinorArcs.lemma_4_1_3` (the terms with `q ∣ n` set to `0`, with `sin²`). -/
theorem lemma_4_1_3_lhs_eq (α B C : ℝ) (q : ℕ) (y₁ y₂ : ℝ) :
    (∑ n ∈ Finset.Ioc ⌊y₁⌋ ⌊y₂⌋ with ¬ (q : ℤ) ∣ n,
        min (B / |Real.sin (π * α * n)|) (C / |Real.sin (π * α * n)| ^ 2)) =
      ∑ n ∈ Finset.Ioc ⌊y₁⌋ ⌊y₂⌋, (if (q : ℤ) ∣ n then 0 else
        min (B / |Real.sin (π * α * n)|) (C / Real.sin (π * α * n) ^ 2)) := by
  rw [Finset.sum_filter]
  refine Finset.sum_congr rfl fun n _ => ?_
  by_cases h : (q : ℤ) ∣ n <;> simp [h, sq_abs]

/-- **Relation: [H, Lemma 4.1.3] as printed is exactly the formal statement.** The statement
`lemma_4_1_3` is equivalent to the statement of `TernaryGoldbach.MinorArcs.lemma_4_1_3`. The proof
uses neither theorem. It repacks the hypotheses, matching `Approx α a q Q` with `0 < q`,
`(a, q) = 1`, `|β| ≤ 1`, `α = a/q + β/(qQ)` and `q ≤ Q`, and it rewrites the sum and the constant.
So the formalization states the printed lemma itself, neither weaker nor stronger. -/
theorem lemma_4_1_3_iff_formal :
    lemma_4_1_3 ↔ type_of% @TernaryGoldbach.MinorArcs.lemma_4_1_3 := by
  constructor
  · intro hb α Q a q h y₁ y₂ hy hy₁₂ hlen hy₂ B C hB hC
    obtain ⟨hq1, hcop, β, hβ, hα, hqQ⟩ := h
    obtain ⟨h1, h2⟩ := hb α a q β Q hq1 (Int.isCoprime_iff_gcd_eq_one.mp hcop) hβ hqQ hα
      y₁ y₂ hy hy₁₂ hlen hy₂ B C hB hC
    rw [lemma_4_1_3_lhs_eq] at h1 h2
    rw [← mul_div_assoc] at h1
    exact ⟨h1, h2⟩
  · intro hf α a q β Q hq hgcd hβ hqQ hα y₁ y₂ hy hy₁₂ hlen hy₂ B C hB hC
    obtain ⟨h1, h2⟩ := hf ⟨hq, Int.isCoprime_iff_gcd_eq_one.mpr hgcd, β, hβ, hα, hqQ⟩
      hy hy₁₂ hlen hy₂ hB hC
    rw [lemma_4_1_3_lhs_eq, ← mul_div_assoc]
    exact ⟨h1, h2⟩

/-- **[H, Lemma 4.1.3] holds as printed**, both (4.6) and the bound `(2Bq/π) log(2e²q/π)`. It is
proved by `TernaryGoldbach.MinorArcs.lemma_4_1_3`, through `lemma_4_1_3_iff_formal`. -/
theorem lemma_4_1_3_holds : lemma_4_1_3 :=
  lemma_4_1_3_iff_formal.mpr @TernaryGoldbach.MinorArcs.lemma_4_1_3

end Companion.Book
