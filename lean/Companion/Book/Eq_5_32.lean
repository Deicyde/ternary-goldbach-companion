import TernaryGoldbach

/-!
# [H, (5.32)]: `∫₁ᵀ G_v(S) dS/S ≤ 0.3698 log T` (`v = 1`), `≤ 0.37273 log T` (`v = 2`) — false

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §5.1,
p. 92 (<https://arxiv.org/pdf/1501.05438v2#page=102>); unchanged from (4.32) of arXiv:1205.5252v4.
For the function `G_v` of p. 92,
`∫₁ᵀ G_v(S) dS/S ≤ 0.3698 log T` if `v = 1` and `≤ 0.37273 log T` if `v = 2`.
`G_v(S) = K_{v,1}(⌊S⌋) + K_{v,2}(⌊S⌋)/S` is what the book gets by summing the exact coefficient
(5.29) over `m`. It is a bound for the triple sum (5.28)
`∑_{s ≤ S, (s,v)=1} (1/s) ∫_{1/2}^1 g_v(uS/s) du`, with `g_v` from Lemma 5.1.2, and in exact
arithmetic it equals that sum. The book says it checks (5.32) numerically for
`T ∈ [2, 40] ∩ (1/N)ℤ`. It then uses (5.32) for (5.36) through `H_v` (5.35), which is built from
`G₁` on `[1, 40)` and from `G₂` on `[1, 16)`.

**What the formalization proves.** The repository treats `v = 2` only and never states (5.32).
Its `TernaryGoldbach.MinorArcs.T2` is the triple sum (5.28) for `v = 2`. In place of (5.32) and
(5.36) it proves the corrected `TernaryGoldbach.MinorArcs.integral_H2_le`:
`∫₁ᵀ H₂(S)/S dS ≤ 0.15107 log T + 0.0231`. `AXIOMS.md`, Finding 1, records that (5.32) is false
for `v = 2`.

**Relation, certified here: the printed statement is false, and both of its cases are.**
* `eq_5_32_false : ¬ eq_5_32` comes from `v = 2`, `T = 4`:
  `∫₁⁴ G₂(S) dS/S = (7/6) log 2 + (1/6) log 3 − 11/24 = 0.533440… > 0.516714… = 0.37273 log 4`
  (`eq_5_32_v2_integral_four`, `eq_5_32_v2_fails_at_four`). We have `G₂ = T2` (`eq_5_32_G_two`).
  On `[n, n+1)`, `T2 = α_n + β_n/S` with the repository's kernel-checked table `H2B.T2_eq'`, which
  gives `1 − 1/S`, `1/2` and `1/3 + 1/(2S)` on `[1,2)`, `[2,3)` and `[3,4)`.
* `v = 1` is not in the repository or in `AXIOMS.md`. Here
  `∫₁⁵ G₁(S) dS/S = (2/3) log 2 + (1/3) log 5 − 2/5 = 0.598577… > 0.595170… = 0.3698 log 5`
  (`eq_5_32_v1_fails_at_five`). The proof uses `G₁ = 1 − 1/S` on `[1,2)` and
  `G₁ = 1/3 + 1/(3S)` on `[2,5)`, evaluated by the kernel (`eq_5_32_G_eq`, `eq_5_32_tab1`).
  `eq_5_32_each_case_false` refutes each case on its own.
* Numerically (floating-point evaluation of the exact rational pieces `α_n + β_n/S`; not part of
  the proof), the `v = 2` bound fails for every `T ∈ [3.37, 200]`. On `[1, 40]` the ratio
  `∫₁ᵀ G₂/S ÷ log T` peaks at `0.39691` near `T ≈ 8.15`. This also contradicts [H]'s remark that
  `0.358` would do. The `v = 1` bound fails for every `T ∈ [4.52, 200]`, and its ratio peaks at
  `0.37741` near `T ≈ 10.61`. So (5.36) fails for `v = 1` too:
  `∫₁⁵ H₁/S = (6/π²)·0.598577 = 0.36389 > 0.36183 = 0.22482 log 5` (not formalized here). The
  same computation agrees with (5.31): `max_{[16,120]} T₂ = 0.371249` and
  `max_{[40,120]} T₁ = 0.363496`.
* **Robustness.** The failure does not depend on reading `G_v` as the triple sum.
  `eq_5_32_v2_majorant_fails` and `eq_5_32_v1_majorant_fails` give the same strict inequalities
  for every function `K₁(⌊S⌋) + K₂(⌊S⌋)/S` lying above the triple sum, so for any `G_v` the book
  could have computed. Nor does it depend on the range of `T`: `T = 4` and `T = 5` lie in `[2, 16]`.
  That interval sits inside both the book's checked range `[2, 40]` and the ranges (5.36) needs.
* **Non-vacuity.** Both inequalities hold at `T = 2` (`eq_5_32_holds_at_two`). The transcription
  also reproduces the book's example: `G_v = 1 − 1/S` on `[1, 2)` and `G_v = 0` for `S < 1`
  (`eq_5_32_G_lt_two`, `eq_5_32_G_lt_one`).
* **What holds instead.** From the formal `integral_H2_le`, `eq_5_32_v2_corrected` derives
  `∫₁ᵀ G₂(S) dS/S ≤ (π²/4)(0.15107 log T + 0.0231)`, about `0.37275 log T + 0.0570`, for
  `1 ≤ T < 16`.
-/

open Real Finset MeasureTheory
open ArithmeticFunction (moebius sigma)
open scoped ArithmeticFunction.Moebius ArithmeticFunction.sigma

namespace Companion.Book

open TernaryGoldbach.MinorArcs

/-- `g_v(x)` of [H, Lemma 5.1.2] (p. 84):
`∑_{r₁ ≤ x} ∑_{r₂ ≤ x}, (r₁, r₂) = 1, (r₁ r₂, v) = 1, μ(r₁) μ(r₂) / (σ(r₁) σ(r₂))`.

The book's `σ(n)` is the sum of the divisors of `n` ([H, §2.1]). That is Mathlib's `σ 1`.
The sums run over the integers `1 ≤ r ≤ ⌊x⌋`, so `g_v(x) = 0` for `x < 1`. Both coprimality
conditions are `Nat.Coprime`. For `v = 2` this is the repository's `g2` (`eq_5_32_g_two`), which
writes `(r₁ r₂, 2) = 1` as `Odd (r₁ * r₂)`. -/
noncomputable def eq_5_32_g (v : ℕ) (x : ℝ) : ℝ :=
  ∑ r₁ ∈ Icc 1 ⌊x⌋₊, ∑ r₂ ∈ Icc 1 ⌊x⌋₊,
    if Nat.Coprime r₁ r₂ ∧ Nat.Coprime (r₁ * r₂) v then
      (μ r₁ : ℝ) * μ r₂ / ((σ 1 r₁ : ℝ) * σ 1 r₂) else 0

/-- `G_v(S)` of [H, p. 92], taken to be the triple sum [H, (5.28)]
`∑_{s ≤ S, (s,v)=1} (1/s) ∫_{1/2}^1 g_v(uS/s) du`.

Why this is the book's `G_v`. For `S < 100000` the book computes `G_v` "using the exact expression
(5.29) instead of (5.30)". (5.29) is the exact coefficient of `g_v(m)` in (5.28), so summing it
over `m ≤ S` gives (5.28) itself, in the form `K_{v,1}(⌊S⌋) + K_{v,2}(⌊S⌋)/S` that the book
describes (`eq_5_32_G_eq`). We read the printed `K_{v,1}(|S|)` as `K_{v,1}(⌊S⌋)`, since the
previous sentence says the coefficients depend only on `⌊S⌋`. The book calls `G_v` "a bound of the
form", perhaps because it was computed with upward rounding. `eq_5_32_v2_majorant_fails` and
`eq_5_32_v1_majorant_fails` show that the refutation holds for every such bound. This `G_v`
reproduces the book's example, `1 − 1/S` on `[1, 2)` and `0` for `S < 1` (`eq_5_32_G_lt_two`,
`eq_5_32_G_lt_one`). For `v = 2` it is the repository's `T2` (`eq_5_32_G_two`). -/
noncomputable def eq_5_32_G (v : ℕ) (S : ℝ) : ℝ :=
  ∑ s ∈ Icc 1 ⌊S⌋₊,
    if Nat.Coprime s v then (1 / s : ℝ) * ∫ u in (1 / 2 : ℝ)..1, eq_5_32_g v (u * S / s) else 0

/-- **[H, (5.32)]** as printed:
`∫₁ᵀ G_v(S) dS/S ≤ 0.3698 log T` if `v = 1`, and `≤ 0.37273 log T` if `v = 2`.

Transcription choices:
* `G_v` is `eq_5_32_G v` (see there).
* `∫₁ᵀ … dS/S` is the interval integral `∫ S in 1..T, G_v(S) / S`. On `[1, T]` the integrand is
  bounded and measurable, so this is the ordinary integral. Integrability on `[1, 4]` and
  `[1, 5]` is proved explicitly (`eq_5_32_v2_integral_four`, `eq_5_32_v1_integral_five`), so the
  refutation is not an artefact of Lean's convention that a non-integrable function has
  integral `0`.
* The display gives no range for `T`. We take every `T ≥ 1`, because the integral starts at `1`,
  and for `0 < T < 1` the right-hand side is negative while the left-hand side is `0`. The book's
  numerical check covers `T ∈ [2, 40]`. Its use in (5.36) needs `[1, 40]` for `v = 1` and
  `[1, 16]` for `v = 2`. The counterexamples `T = 5` (`v = 1`) and `T = 4` (`v = 2`) lie in every
  one of these ranges.
* The two cases are joined by `∧`. The constants `0.3698` and `0.37273` are as printed. -/
def eq_5_32 : Prop :=
  ∀ T : ℝ, 1 ≤ T →
    (∫ S in (1 : ℝ)..T, eq_5_32_G 1 S / S) ≤ 0.3698 * Real.log T ∧
    (∫ S in (1 : ℝ)..T, eq_5_32_G 2 S / S) ≤ 0.37273 * Real.log T

/-- For `v = 2` the book's `g_v` is the repository's `g2`. -/
theorem eq_5_32_g_two : eq_5_32_g 2 = g2 := by
  funext x
  simp only [eq_5_32_g, g2, Nat.coprime_two_right]

/-- For `v = 2` the book's `G_v`, i.e. the triple sum (5.28), is the repository's `T2`. -/
theorem eq_5_32_G_two : eq_5_32_G 2 = T2 := by
  funext S
  simp only [eq_5_32_G, T2, eq_5_32_g_two, Nat.coprime_two_right]

/-- A function equal to `a + b/S` on `[p, q)` integrates against `dS/S` to
`a log(q/p) + b(1/p − 1/q)`. -/
theorem eq_5_32_piece {f : ℝ → ℝ} {a b p q : ℝ} (hp : 0 < p) (hpq : p ≤ q)
    (hf : ∀ S, p ≤ S → S < q → f S = a + b / S) :
    IntervalIntegrable (fun S => f S / S) volume p q ∧
      ∫ S in p..q, f S / S = a * Real.log (q / p) + b * (1 / p - 1 / q) := by
  set h : ℝ → ℝ := fun S => (a + b / S) / S
  have heq : Set.EqOn (fun S => f S / S) h (Set.Ioo p q) := fun S hS => by
    simp only [h, hf S hS.1.le hS.2]
  have hcont : ContinuousOn h (Set.uIcc p q) := by
    intro x hx
    rw [Set.uIcc_of_le hpq] at hx
    have hx0 : x ≠ 0 := (hp.trans_le hx.1).ne'
    apply ContinuousAt.continuousWithinAt
    simp only [h]
    fun_prop (disch := exact hx0)
  have hint : IntervalIntegrable h volume p q := hcont.intervalIntegrable
  refine ⟨?_, ?_⟩
  · rw [intervalIntegrable_iff_integrableOn_Ioo_of_le hpq]
    exact ((intervalIntegrable_iff_integrableOn_Ioo_of_le hpq).1 hint).congr_fun heq.symm
      measurableSet_Ioo
  · have hval : ∫ S in p..q, f S / S = ∫ S in p..q, h S := by
      rw [intervalIntegral.integral_of_le hpq, intervalIntegral.integral_of_le hpq,
        integral_Ioc_eq_integral_Ioo, integral_Ioc_eq_integral_Ioo]
      exact setIntegral_congr_fun measurableSet_Ioo heq
    have hderiv : ∀ x ∈ Set.uIcc p q,
        HasDerivAt (fun S => a * Real.log S - b * S⁻¹) (h x) x := by
      intro x hx
      rw [Set.uIcc_of_le hpq] at hx
      have hx0 : 0 < x := hp.trans_le hx.1
      have h1 := ((Real.hasDerivAt_log hx0.ne').const_mul a).sub
        ((hasDerivAt_inv hx0.ne').const_mul b)
      convert h1 using 1
      simp only [h]
      field_simp
      ring
    rw [hval, intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint,
      Real.log_div (hp.trans_le hpq).ne' hp.ne']
    ring

/-! ### `v = 2`, `T = 4` -/

/-- The repository's kernel table for `T₂ = α_n + β_n/S` on `[n, n+1)`, for `n = 1, 2, 3`. -/
theorem eq_5_32_tab2 : H2B.al 1 = 1 ∧ H2B.be 1 = -1 ∧ H2B.al 2 = 1 / 2 ∧ H2B.be 2 = 0 ∧
    H2B.al 3 = 1 / 3 ∧ H2B.be 3 = 1 / 2 := by decide +kernel

/-- `∫₁⁴ G₂(S) dS/S = (log 2 − 1/2) + ½ log(3/2) + ⅓ log(4/3) + 1/24
= (7/6) log 2 + (1/6) log 3 − 11/24`, with the integrand integrable on `[1, 4]`. -/
theorem eq_5_32_v2_integral_four :
    IntervalIntegrable (fun S => eq_5_32_G 2 S / S) volume 1 4 ∧
      ∫ S in (1 : ℝ)..4, eq_5_32_G 2 S / S = 7 / 6 * Real.log 2 + 1 / 6 * Real.log 3 - 11 / 24 := by
  obtain ⟨a1, b1, a2, b2, a3, b3⟩ := eq_5_32_tab2
  have p1 := eq_5_32_piece (f := eq_5_32_G 2) (a := 1) (b := -1) (p := 1) (q := 2) one_pos
    (by norm_num) fun S h1 h2 => by
      rw [eq_5_32_G_two, H2B.T2_eq' (n := 1) le_rfl (by norm_num) (by exact_mod_cast h1)
        (by norm_num; linarith), a1, b1]
      push_cast; ring
  have p2 := eq_5_32_piece (f := eq_5_32_G 2) (a := 1 / 2) (b := 0) (p := 2) (q := 3) two_pos
    (by norm_num) fun S h1 h2 => by
      rw [eq_5_32_G_two, H2B.T2_eq' (n := 2) (by norm_num) (by norm_num) (by exact_mod_cast h1)
        (by norm_num; linarith), a2, b2]
      push_cast; ring
  have p3 := eq_5_32_piece (f := eq_5_32_G 2) (a := 1 / 3) (b := 1 / 2) (p := 3) (q := 4)
    three_pos (by norm_num) fun S h1 h2 => by
      rw [eq_5_32_G_two, H2B.T2_eq' (n := 3) (by norm_num) (by norm_num) (by exact_mod_cast h1)
        (by norm_num; linarith), a3, b3]
      push_cast; ring
  obtain ⟨i1, e1⟩ := p1
  obtain ⟨i2, e2⟩ := p2
  obtain ⟨i3, e3⟩ := p3
  refine ⟨(i1.trans i2).trans i3, ?_⟩
  rw [← intervalIntegral.integral_add_adjacent_intervals (i1.trans i2) i3,
    ← intervalIntegral.integral_add_adjacent_intervals i1 i2, e1, e2, e3]
  have l32 : Real.log (3 / 2) = Real.log 3 - Real.log 2 := Real.log_div (by norm_num) (by norm_num)
  have l43 : Real.log (4 / 3) = Real.log 4 - Real.log 3 := Real.log_div (by norm_num) (by norm_num)
  have l4 : Real.log 4 = 2 * Real.log 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]; norm_num
  rw [l32, l43, l4, show (2 : ℝ) / 1 = 2 by norm_num]
  ring

/-- **The `v = 2` case of (5.32) fails at `T = 4`**:
`∫₁⁴ G₂(S) dS/S = 0.533440… > 0.516714… = 0.37273 log 4`. -/
theorem eq_5_32_v2_fails_at_four :
    0.37273 * Real.log 4 < ∫ S in (1 : ℝ)..4, eq_5_32_G 2 S / S := by
  rw [eq_5_32_v2_integral_four.2]
  have l2 := Real.log_two_gt_d9
  have l32 : 1 / 3 ≤ Real.log (3 / 2) := by
    have := Real.one_sub_inv_le_log_of_pos (show (0 : ℝ) < 3 / 2 by norm_num)
    norm_num at this ⊢; linarith
  have e32 : Real.log (3 / 2) = Real.log 3 - Real.log 2 := Real.log_div (by norm_num) (by norm_num)
  have l4 : Real.log 4 = 2 * Real.log 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]; norm_num
  rw [l4]
  linarith

/-! ### General `v`: `G_v = α_n + β_n/S` on `[n, n+1)` (used for `v = 1`) -/

/-- [H, (5.19)] for general `v`:
`∫_{1/2}^1 g_v(uy) du = ∑_{r₁,r₂ ≤ y} c_v(r₁,r₂) (1 − max(1/2, r₁/y, r₂/y))`.
(The proof is that of the repository's `integral_g2`, with `Odd (r₁ r₂)` replaced by
`(r₁ r₂, v) = 1`.) -/
theorem eq_5_32_integral_g (v : ℕ) {y : ℝ} (hy : 0 < y) :
    ∫ u in (1 / 2 : ℝ)..1, eq_5_32_g v (u * y) =
      ∑ r₁ ∈ Icc 1 ⌊y⌋₊, ∑ r₂ ∈ Icc 1 ⌊y⌋₊,
        (if Nat.Coprime r₁ r₂ ∧ Nat.Coprime (r₁ * r₂) v then
          (μ r₁ : ℝ) * μ r₂ / ((σ 1 r₁ : ℝ) * σ 1 r₂) else 0) * wM y r₁ r₂ := by
  set c : ℕ → ℕ → ℝ := fun r₁ r₂ => if Nat.Coprime r₁ r₂ ∧ Nat.Coprime (r₁ * r₂) v then
    (μ r₁ : ℝ) * μ r₂ / ((σ 1 r₁ : ℝ) * σ 1 r₂) else 0
  have hpt : ∀ u ∈ Set.uIcc (1 / 2 : ℝ) 1, eq_5_32_g v (u * y) =
      ∑ r₁ ∈ Icc 1 ⌊y⌋₊, ∑ r₂ ∈ Icc 1 ⌊y⌋₊,
        c r₁ r₂ * (if max ((r₁ : ℝ) / y) (r₂ / y) ≤ u then 1 else 0) := by
    intro u hu
    rw [Set.uIcc_of_le (by norm_num)] at hu
    have hfilt : Icc 1 ⌊u * y⌋₊ = (Icc 1 ⌊y⌋₊).filter (fun r : ℕ => (r : ℝ) ≤ u * y) := by
      ext r
      simp only [mem_Icc, mem_filter]
      constructor
      · rintro ⟨h1, h2⟩
        have h3 : (r : ℝ) ≤ u * y :=
          (Nat.cast_le.2 h2).trans (Nat.floor_le (by nlinarith [hu.1]))
        exact ⟨⟨h1, Nat.le_floor (h3.trans (by nlinarith [hu.2]))⟩, h3⟩
      · rintro ⟨⟨h1, _⟩, h3⟩; exact ⟨h1, Nat.le_floor h3⟩
    have hmax : ∀ r₁ r₂ : ℕ, max ((r₁ : ℝ) / y) (r₂ / y) ≤ u ↔
        (r₁ : ℝ) ≤ u * y ∧ (r₂ : ℝ) ≤ u * y := by
      intro r₁ r₂; rw [max_le_iff, div_le_iff₀ hy, div_le_iff₀ hy]
    rw [eq_5_32_g, hfilt, sum_filter]
    refine sum_congr rfl fun r₁ _ => ?_
    rw [sum_filter]
    simp only [hmax]
    by_cases h1 : (r₁ : ℝ) ≤ u * y
    · rw [ite_eq_left h1]
      refine sum_congr rfl fun r₂ _ => ?_
      by_cases h2 : (r₂ : ℝ) ≤ u * y
      · simp [h1, h2, c]
      · simp [h2]
    · rw [ite_eq_right h1]; symm
      exact sum_eq_zero fun r₂ _ => by simp [h1]
  have hint : ∀ r₁ r₂, IntervalIntegrable
      (fun u : ℝ => c r₁ r₂ * (if max ((r₁ : ℝ) / y) (r₂ / y) ≤ u then 1 else 0))
      volume (1 / 2) 1 := fun r₁ r₂ =>
    ((monotone_ite_le _).intervalIntegrable).const_mul _
  have hint2 : ∀ r₁, IntervalIntegrable (fun u : ℝ => ∑ r₂ ∈ Icc 1 ⌊y⌋₊,
      c r₁ r₂ * (if max ((r₁ : ℝ) / y) (r₂ / y) ≤ u then 1 else 0)) volume (1 / 2) 1 := by
    intro r₁
    have := IntervalIntegrable.sum (Icc 1 ⌊y⌋₊) (fun r₂ _ => hint r₁ r₂)
    convert this using 1; ext u; simp [Finset.sum_apply]
  rw [intervalIntegral.integral_congr hpt, intervalIntegral.integral_finsetSum
    (fun r₁ _ => hint2 r₁)]
  refine sum_congr rfl fun r₁ hr₁ => ?_
  rw [intervalIntegral.integral_finsetSum (fun r₂ _ => hint r₁ r₂)]
  refine sum_congr rfl fun r₂ hr₂ => ?_
  rw [intervalIntegral.integral_const_mul, integral_ite_le, wM]
  have h1 : (r₁ : ℝ) ≤ y := (Nat.cast_le.2 (mem_Icc.1 hr₁).2).trans (Nat.floor_le hy.le)
  have h2 : (r₂ : ℝ) ≤ y := (Nat.cast_le.2 (mem_Icc.1 hr₂).2).trans (Nat.floor_le hy.le)
  exact max_le ((div_le_one hy).2 h1) ((div_le_one hy).2 h2)

/-- The coefficient `μ(r₁)μ(r₂)/(σ(r₁)σ(r₂))` of `g_v`, from the repository's kernel-checked tables
`H2B.muZ`, `H2B.sigN` of `μ` and `σ` on `[0, 15]`. -/
def eq_5_32_cf (v r₁ r₂ : ℕ) : ℚ := if Nat.Coprime r₁ r₂ ∧ Nat.Coprime (r₁ * r₂) v then
    ((H2B.muZ.getD r₁ 0 * H2B.muZ.getD r₂ 0 : ℤ) : ℚ) /
      ((H2B.sigN.getD r₁ 0 * H2B.sigN.getD r₂ 0 : ℕ) : ℚ) else 0

/-- The real coefficient of `g_v` equals the tabulated one for `r₁, r₂ ≤ 15`. -/
theorem eq_5_32_cf_eq {v r₁ r₂ : ℕ} (h₁ : r₁ ≤ 15) (h₂ : r₂ ≤ 15) :
    (if Nat.Coprime r₁ r₂ ∧ Nat.Coprime (r₁ * r₂) v then
      (μ r₁ : ℝ) * μ r₂ / ((σ 1 r₁ : ℝ) * σ 1 r₂) else 0) = (eq_5_32_cf v r₁ r₂ : ℝ) := by
  unfold eq_5_32_cf
  split_ifs
  · rw [H2B.mu_tab r₁ (mem_range.2 (by omega)), H2B.mu_tab r₂ (mem_range.2 (by omega)),
      H2B.sig_tab r₁ (mem_range.2 (by omega)), H2B.sig_tab r₂ (mem_range.2 (by omega))]
    push_cast; ring
  · simp

/-- The `(s, r₁, r₂)` term of `α_n` (for `G_v`). -/
def eq_5_32_aT (v n s r₁ r₂ : ℕ) : ℚ :=
  eq_5_32_cf v r₁ r₂ * (if 2 * s * max r₁ r₂ ≤ n then 1 / (2 * (s : ℚ)) else 1 / (s : ℚ))

/-- The `(s, r₁, r₂)` term of `β_n` (for `G_v`). -/
def eq_5_32_bT (v n s r₁ r₂ : ℕ) : ℚ :=
  eq_5_32_cf v r₁ r₂ * (if 2 * s * max r₁ r₂ ≤ n then 0 else -((max r₁ r₂ : ℕ) : ℚ))

/-- `α_n` with `G_v = α_n + β_n/S` on `[n, n+1)`. -/
def eq_5_32_alpha (v n : ℕ) : ℚ := ∑ s ∈ Icc 1 n,
  if Nat.Coprime s v then ∑ r₁ ∈ Icc 1 (n / s), ∑ r₂ ∈ Icc 1 (n / s), eq_5_32_aT v n s r₁ r₂ else 0

/-- `β_n` with `G_v = α_n + β_n/S` on `[n, n+1)`. -/
def eq_5_32_beta (v n : ℕ) : ℚ := ∑ s ∈ Icc 1 n,
  if Nat.Coprime s v then ∑ r₁ ∈ Icc 1 (n / s), ∑ r₂ ∈ Icc 1 (n / s), eq_5_32_bT v n s r₁ r₂ else 0

/-- On `[n, n+1)`, the `(s, r₁, r₂)` term of `G_v` is `aT + bT/S`. (The proof is that of the
repository's `H2B.term_eq`.) -/
theorem eq_5_32_term_eq {v n s r₁ r₂ : ℕ} (hs : 1 ≤ s) (h₁ : r₁ ≤ 15) (h₂ : r₂ ≤ 15) {S : ℝ}
    (hn : (n : ℝ) ≤ S) (hn' : S < n + 1) (hS : 0 < S) :
    1 / (s : ℝ) * ((if Nat.Coprime r₁ r₂ ∧ Nat.Coprime (r₁ * r₂) v then
        (μ r₁ : ℝ) * μ r₂ / ((σ 1 r₁ : ℝ) * σ 1 r₂) else 0) * wM (S / s) r₁ r₂) =
      (eq_5_32_aT v n s r₁ r₂ : ℝ) + (eq_5_32_bT v n s r₁ r₂ : ℝ) / S := by
  rw [eq_5_32_cf_eq h₁ h₂]
  have hs0 : (0 : ℝ) < s := by exact_mod_cast hs
  have hw : max ((r₁ : ℝ) / (S / s)) ((r₂ : ℝ) / (S / s)) = ((max r₁ r₂ : ℕ) : ℝ) * s / S := by
    rw [max_div_div_right (div_pos hS hs0).le, Nat.cast_max]; field_simp
  unfold wM eq_5_32_aT eq_5_32_bT
  rw [hw]
  split_ifs with hc
  · have h1 : ((2 * s * max r₁ r₂ : ℕ) : ℝ) ≤ n := by exact_mod_cast hc
    have h2 : ((max r₁ r₂ : ℕ) : ℝ) * s / S ≤ 1 / 2 := by
      rw [div_le_iff₀ hS]; push_cast at h1 ⊢; linarith
    rw [max_eq_left h2]; push_cast; field_simp; ring
  · have h1 : ((n + 1 : ℕ) : ℝ) ≤ ((2 * s * max r₁ r₂ : ℕ) : ℝ) := by
      exact_mod_cast (by omega : n + 1 ≤ 2 * s * max r₁ r₂)
    have h2 : 1 / 2 < ((max r₁ r₂ : ℕ) : ℝ) * s / S := by
      rw [lt_div_iff₀ hS]; push_cast at h1 ⊢; linarith
    rw [max_eq_right h2.le]; push_cast; field_simp; ring

/-- **`G_v(S) = α_n + β_n/S` on `[n, n+1)`**, for `1 ≤ n ≤ 15` and any `v`: the book's
`K_{v,1}(⌊S⌋) + K_{v,2}(⌊S⌋)/S`. (The proof is that of the repository's `H2B.T2_eq`.) -/
theorem eq_5_32_G_eq {v n : ℕ} (hn1 : 1 ≤ n) (hn : n ≤ 15) {S : ℝ} (h1 : (n : ℝ) ≤ S)
    (h2 : S < n + 1) : eq_5_32_G v S = eq_5_32_alpha v n + eq_5_32_beta v n / S := by
  have hS : 0 < S := lt_of_lt_of_le (by exact_mod_cast hn1) h1
  have hfl : ⌊S⌋₊ = n := (Nat.floor_eq_iff hS.le).2 ⟨h1, h2⟩
  unfold eq_5_32_G eq_5_32_alpha eq_5_32_beta
  rw [hfl, Rat.cast_sum, Rat.cast_sum, sum_div, ← sum_add_distrib]
  refine sum_congr rfl fun s hs => ?_
  obtain ⟨hs1, hsn⟩ := mem_Icc.1 hs
  split_ifs with ho
  · have hs0 : (0 : ℝ) < s := by exact_mod_cast hs1
    simp_rw [mul_div_assoc]
    rw [eq_5_32_integral_g v (div_pos hS hs0), Nat.floor_div_natCast, hfl, mul_sum, Rat.cast_sum,
      Rat.cast_sum, sum_div, ← sum_add_distrib]
    refine sum_congr rfl fun r₁ hr₁ => ?_
    rw [mul_sum, Rat.cast_sum, Rat.cast_sum, sum_div, ← sum_add_distrib]
    refine sum_congr rfl fun r₂ hr₂ => ?_
    have hd : n / s ≤ 15 := (Nat.div_le_self n s).trans hn
    exact eq_5_32_term_eq hs1 ((mem_Icc.1 hr₁).2.trans hd) ((mem_Icc.1 hr₂).2.trans hd) h1 h2 hS
  · simp

/-- Kernel evaluation for `v = 1`: `G₁ = 1 − 1/S` on `[1, 2)` and `G₁ = 1/3 + 1/(3S)` on
`[2, 5)`. -/
theorem eq_5_32_tab1 : eq_5_32_alpha 1 1 = 1 ∧ eq_5_32_beta 1 1 = -1 ∧
    ∀ n ∈ Icc 2 4, eq_5_32_alpha 1 n = 1 / 3 ∧ eq_5_32_beta 1 n = 1 / 3 := by decide +kernel

/-- `∫₁⁵ G₁(S) dS/S = (log 2 − 1/2) + ⅓ log(5/2) + ⅓(1/2 − 1/5)
= (2/3) log 2 + (1/3) log 5 − 2/5`, with the integrand integrable on `[1, 5]`. -/
theorem eq_5_32_v1_integral_five :
    IntervalIntegrable (fun S => eq_5_32_G 1 S / S) volume 1 5 ∧
      ∫ S in (1 : ℝ)..5, eq_5_32_G 1 S / S = 2 / 3 * Real.log 2 + 1 / 3 * Real.log 5 - 2 / 5 := by
  obtain ⟨a1, b1, h24⟩ := eq_5_32_tab1
  obtain ⟨i1, e1⟩ := eq_5_32_piece (f := eq_5_32_G 1) (a := 1) (b := -1) (p := 1) (q := 2) one_pos
    (by norm_num) fun S h1 h2 => by
      rw [eq_5_32_G_eq (n := 1) le_rfl (by norm_num) (by exact_mod_cast h1)
        (by norm_num; linarith), a1, b1]
      push_cast; ring
  obtain ⟨i2, e2⟩ := eq_5_32_piece (f := eq_5_32_G 1) (a := 1 / 3) (b := 1 / 3) (p := 2) (q := 5)
    two_pos (by norm_num) fun S h1 h2 => by
      have hS : 0 ≤ S := by linarith
      have hn2 : 2 ≤ ⌊S⌋₊ := Nat.le_floor (by exact_mod_cast h1)
      have hn4 : ⌊S⌋₊ ≤ 4 := Nat.le_of_lt_succ ((Nat.floor_lt hS).2 (by norm_num; linarith))
      obtain ⟨ha, hb⟩ := h24 ⌊S⌋₊ (mem_Icc.2 ⟨hn2, hn4⟩)
      rw [eq_5_32_G_eq (n := ⌊S⌋₊) (by omega) (by omega) (Nat.floor_le hS)
        (Nat.lt_floor_add_one S), ha, hb]
      push_cast; ring
  refine ⟨i1.trans i2, ?_⟩
  rw [← intervalIntegral.integral_add_adjacent_intervals i1 i2, e1, e2]
  have l52 : Real.log (5 / 2) = Real.log 5 - Real.log 2 := Real.log_div (by norm_num) (by norm_num)
  rw [l52, show (2 : ℝ) / 1 = 2 by norm_num]
  ring

/-- **The `v = 1` case of (5.32) fails as well, at `T = 5`**:
`∫₁⁵ G₁(S) dS/S = (2/3) log 2 + (1/3) log 5 − 2/5 = 0.598577… > 0.595170… = 0.3698 log 5`. -/
theorem eq_5_32_v1_fails_at_five :
    0.3698 * Real.log 5 < ∫ S in (1 : ℝ)..5, eq_5_32_G 1 S / S := by
  rw [eq_5_32_v1_integral_five.2]
  have l2 := Real.log_two_gt_d9
  have l54 : Real.log (5 / 4) ≤ 1 / 4 := by
    have := Real.log_le_sub_one_of_pos (show (0 : ℝ) < 5 / 4 by norm_num)
    linarith
  have e54 : Real.log (5 / 4) = Real.log 5 - Real.log 4 := Real.log_div (by norm_num) (by norm_num)
  have l4 : Real.log 4 = 2 * Real.log 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]; norm_num
  linarith

/-- **[H, (5.32)] is false**: its `v = 2` case fails at `T = 4` (`eq_5_32_v2_fails_at_four`). -/
theorem eq_5_32_false : ¬ eq_5_32 := fun h =>
  absurd (h 4 (by norm_num)).2 (not_le.2 eq_5_32_v2_fails_at_four)

/-! ### Each case separately -/

/-- Each case of (5.32) is false on its own: `v = 1` at `T = 5`, `v = 2` at `T = 4`. -/
theorem eq_5_32_each_case_false :
    (¬ ∀ T : ℝ, 1 ≤ T → (∫ S in (1 : ℝ)..T, eq_5_32_G 1 S / S) ≤ 0.3698 * Real.log T) ∧
    (¬ ∀ T : ℝ, 1 ≤ T → (∫ S in (1 : ℝ)..T, eq_5_32_G 2 S / S) ≤ 0.37273 * Real.log T) :=
  ⟨fun h => absurd (h 5 (by norm_num)) (not_le.2 eq_5_32_v1_fails_at_five),
    fun h => absurd (h 4 (by norm_num)) (not_le.2 eq_5_32_v2_fails_at_four)⟩

/-! ### Sanity checks of the transcription -/

/-- The book's own example: `G_v(S) = 1 − 1/S` for `1 ≤ S < 2` (any `v`). -/
theorem eq_5_32_G_lt_two (v : ℕ) {S : ℝ} (h1 : 1 ≤ S) (h2 : S < 2) :
    eq_5_32_G v S = 1 - 1 / S := by
  have hS : 0 < S := by linarith
  have hfl : ⌊S⌋₊ = 1 := (Nat.floor_eq_iff hS.le).2 ⟨by exact_mod_cast h1, by norm_num; linarith⟩
  have hint := eq_5_32_integral_g v hS
  rw [hfl] at hint
  have hw : wM S 1 1 = 1 - 1 / S := by
    have : (1 : ℝ) / 2 ≤ 1 / S := by rw [div_le_div_iff₀ (by norm_num) hS]; linarith
    simp only [wM, Nat.cast_one, max_self, max_eq_right this]
  simp only [eq_5_32_G, hfl, Finset.Icc_self, Finset.sum_singleton, Nat.coprime_one_left_eq_true,
    ite_true, Nat.cast_one, div_one, one_mul] at hint ⊢
  rw [hint, hw]
  simp

/-- The book's own example: `G_v(S) = 0` for `S < 1` (any `v`). -/
theorem eq_5_32_G_lt_one (v : ℕ) {S : ℝ} (h : S < 1) : eq_5_32_G v S = 0 := by
  simp [eq_5_32_G, Nat.floor_eq_zero.2 h]

/-- Non-vacuity: both printed inequalities hold at `T = 2` (`∫₁² G_v/S = log 2 − 1/2`). -/
theorem eq_5_32_holds_at_two :
    (∫ S in (1 : ℝ)..2, eq_5_32_G 1 S / S) ≤ 0.3698 * Real.log 2 ∧
    (∫ S in (1 : ℝ)..2, eq_5_32_G 2 S / S) ≤ 0.37273 * Real.log 2 := by
  have hv : ∀ v : ℕ, ∫ S in (1 : ℝ)..2, eq_5_32_G v S / S = Real.log 2 - 1 / 2 := by
    intro v
    rw [(eq_5_32_piece (f := eq_5_32_G v) (a := 1) (b := -1) (p := 1) (q := 2) one_pos
      (by norm_num) fun S h1 h2 => by rw [eq_5_32_G_lt_two v h1 h2]; ring).2]
    norm_num
    ring
  rw [hv 1, hv 2]
  have := Real.log_two_lt_d9
  constructor <;> linarith

/-! ### Robustness: any majorant of the book's form `K₁(⌊S⌋) + K₂(⌊S⌋)/S` -/

/-- Every function of the form `K₁(⌊S⌋) + K₂(⌊S⌋)/S` is integrable against `dS/S` on `[1, m]`. -/
theorem eq_5_32_floor_form_integrable (K₁ K₂ : ℕ → ℝ) : ∀ m : ℕ, 1 ≤ m →
    IntervalIntegrable (fun S : ℝ => (K₁ ⌊S⌋₊ + K₂ ⌊S⌋₊ / S) / S) volume 1 m
  | 0, h => absurd h (by norm_num)
  | 1, _ => by rw [Nat.cast_one]
  | m + 2, _ => by
    have ih := eq_5_32_floor_form_integrable K₁ K₂ (m + 1) (by omega)
    have hp : (0 : ℝ) < ((m + 1 : ℕ) : ℝ) := by positivity
    refine ih.trans (eq_5_32_piece (f := fun S : ℝ => K₁ ⌊S⌋₊ + K₂ ⌊S⌋₊ / S) (a := K₁ (m + 1))
      (b := K₂ (m + 1)) (p := ((m + 1 : ℕ) : ℝ)) (q := ((m + 2 : ℕ) : ℝ)) hp
      (by push_cast; linarith) fun S h1 h2 => ?_).1
    have hfl : ⌊S⌋₊ = m + 1 :=
      (Nat.floor_eq_iff (hp.le.trans h1)).2 ⟨h1, by push_cast at h2 ⊢; linarith⟩
    simp only [hfl]

/-- (5.32) for `v = 2` fails at `T = 4` for **every** bound `K₁(⌊S⌋) + K₂(⌊S⌋)/S` lying above the
triple sum (5.28) on `[1, 4]`, i.e. for any `G₂` of the form the book describes. -/
theorem eq_5_32_v2_majorant_fails (K₁ K₂ : ℕ → ℝ)
    (hG : ∀ S : ℝ, 1 ≤ S → S ≤ 4 → eq_5_32_G 2 S ≤ K₁ ⌊S⌋₊ + K₂ ⌊S⌋₊ / S) :
    0.37273 * Real.log 4 < ∫ S in (1 : ℝ)..4, (K₁ ⌊S⌋₊ + K₂ ⌊S⌋₊ / S) / S := by
  have iK := eq_5_32_floor_form_integrable K₁ K₂ 4 (by norm_num)
  rw [show ((4 : ℕ) : ℝ) = 4 by norm_num] at iK
  refine eq_5_32_v2_fails_at_four.trans_le (intervalIntegral.integral_mono_on (by norm_num)
    eq_5_32_v2_integral_four.1 iK fun S hS => ?_)
  exact div_le_div_of_nonneg_right (hG S hS.1 hS.2) (by linarith [hS.1])

/-- (5.32) for `v = 1` fails at `T = 5` for every bound `K₁(⌊S⌋) + K₂(⌊S⌋)/S` lying above the
triple sum (5.28) on `[1, 5]`. -/
theorem eq_5_32_v1_majorant_fails (K₁ K₂ : ℕ → ℝ)
    (hG : ∀ S : ℝ, 1 ≤ S → S ≤ 5 → eq_5_32_G 1 S ≤ K₁ ⌊S⌋₊ + K₂ ⌊S⌋₊ / S) :
    0.3698 * Real.log 5 < ∫ S in (1 : ℝ)..5, (K₁ ⌊S⌋₊ + K₂ ⌊S⌋₊ / S) / S := by
  have iK := eq_5_32_floor_form_integrable K₁ K₂ 5 (by norm_num)
  rw [show ((5 : ℕ) : ℝ) = 5 by norm_num] at iK
  refine eq_5_32_v1_fails_at_five.trans_le (intervalIntegral.integral_mono_on (by norm_num)
    eq_5_32_v1_integral_five.1 iK fun S hS => ?_)
  exact div_le_div_of_nonneg_right (hG S hS.1 hS.2) (by linarith [hS.1])

/-! ### What the formalization proves instead -/

/-- `T₂ ≥ 0` on `[1, 16)`, from the repository's `H2B.piece_bounds`. -/
theorem eq_5_32_T2_nonneg {S : ℝ} (h1 : 1 ≤ S) (h16 : S < 16) : 0 ≤ T2 S := by
  have hn1 : 1 ≤ ⌊S⌋₊ := Nat.le_floor (by exact_mod_cast h1)
  have hn15 : ⌊S⌋₊ ≤ 15 :=
    Nat.le_of_lt_succ ((Nat.floor_lt (by linarith)).2 (by norm_num; linarith))
  have hf1 : (⌊S⌋₊ : ℝ) ≤ S := Nat.floor_le (by linarith)
  have hf2 : S < ⌊S⌋₊ + 1 := Nat.lt_floor_add_one S
  rw [H2B.T2_eq' hn1 hn15 hf1 hf2]
  exact (H2B.piece_bounds hn1 hn15 hf1 hf2.le).1

/-- The formalization's corrected (5.36) (`integral_H2_le`, with `+ 0.0231`) yields a corrected
(5.32) for `v = 2` on `[1, 16)`, where `H₂ = (4/π²) G₂`:
`∫₁ᵀ G₂(S) dS/S ≤ (π²/4)(0.15107 log T + 0.0231)`, about `0.37275 log T + 0.0570`. -/
theorem eq_5_32_v2_corrected (hH : type_of% @TernaryGoldbach.MinorArcs.integral_H2_le) {T : ℝ}
    (hT : 1 ≤ T) (hT16 : T < 16) :
    ∫ S in (1 : ℝ)..T, eq_5_32_G 2 S / S ≤ π ^ 2 / 4 * (0.15107 * Real.log T + 0.0231) := by
  have hcongr : ∫ S in (1 : ℝ)..T, eq_5_32_G 2 S / S =
      ∫ S in (1 : ℝ)..T, π ^ 2 / 4 * (H2 S / S) := by
    refine intervalIntegral.integral_congr fun S hS => ?_
    rw [Set.uIcc_of_le hT] at hS
    have h0 := eq_5_32_T2_nonneg hS.1 (by linarith [hS.2])
    have hS0 : S ≠ 0 := by linarith [hS.1]
    simp only [eq_5_32_G_two, H2, ite_eq_left (show S < 16 by linarith [hS.2]), max_eq_left h0]
    field_simp
  rw [hcongr, intervalIntegral.integral_const_mul]
  exact mul_le_mul_of_nonneg_left (hH hT) (by positivity)

/-- `eq_5_32_v2_corrected`, instantiated with the formalization's theorem. -/
theorem eq_5_32_v2_corrected' {T : ℝ} (hT : 1 ≤ T) (hT16 : T < 16) :
    ∫ S in (1 : ℝ)..T, eq_5_32_G 2 S / S ≤ π ^ 2 / 4 * (0.15107 * Real.log T + 0.0231) :=
  eq_5_32_v2_corrected TernaryGoldbach.MinorArcs.integral_H2_le hT hT16

end Companion.Book
