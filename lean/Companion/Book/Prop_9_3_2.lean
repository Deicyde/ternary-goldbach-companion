import TernaryGoldbach

/-!
# [H, Proposition 9.3.2]: the twisted prime sum with weight `η(t) = t² e^{-t²/2}`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2,
Proposition 9.3.2 (p. 182, label `prop:magoma`; <https://arxiv.org/pdf/1501.05438v2#page=192>).
Take `η(t) = t² e^{-t²/2}`, real numbers `x ≥ 1` and `δ`, and a primitive character `χ` mod `q ≥ 1`.
Suppose every non-trivial zero `ρ` of `L(s, χ)` with `|ℑρ| ≤ T₀` has `ℜρ = 1/2`, and
`T₀ ≥ max(10π|δ|, 50)`. Then, by (9.56),

```
Σ_{n≥1} Λ(n) χ(n) e(δn/x) η(n/x) = η̂(−δ) x + O*(err_{η,χ}(δ, x)) · x     (q = 1),
                                 =            O*(err_{η,χ}(δ, x)) · x     (q > 1),
```

where the error term is (9.57):

```
err_{η,χ}(δ, x) = T₀ log(qT₀/2π) · (6.11 e^{−0.1598 T₀} + 1.578 e^{−0.1065 T₀²/(πδ)²})
                + (1.22 √T₀ log qT₀ + 5.056 √T₀ + 1.423 log q + 37.19) · x^{−1/2}
                + (3 + 11|δ|) x^{−1} + (log q + 6)(1 + 6|δ|) · x^{−3/2}.
```

**What the formalization proves.** `TernaryGoldbach.MajorArcs.prop_9_3_2`
(`MajorArcs/Prop932.lean:93`) has the same weight, the same hypotheses (`x ≥ 1`, `χ` primitive mod
`q`, `GRHUpTo χ T₀`, `T₀ ≥ max(10π|δ|, 50)`) and the same main term. Its error term is the
repository's own `err932N q T₀ δ x`: `Explicit.errZ` for `q = 1` and `MajorArcs.errNew` for `q ≥ 2`.
The two halves are `MajorArcs.prop_9_3_2_one` and `MajorArcs.prop_9_3_2_ne`.

[H] bounds the sums over zeros with Lemmas 9.1.3–9.1.4 and 9.3.1, using an explicit zero-counting
estimate `N(T, χ)`. The repository instead counts the zeros in windows of height `3.48` and `4.4` by
Jensen's formula. For `|L(s, χ)|` it uses the polynomial bound
`B'_T = 1400 q⁹(q+1)(|T|+22)(1.25(|T|+11))^{10}`, and `B''_ζ` in the case of `ζ`. The resulting
constants are much larger:
* at `(q, T₀, δ, x) = (2, 50, 0, 1)`, [H]'s error is `≈ 123.6` and Lean's is `≈ 64 492`;
* as `x → ∞` with `(q, T₀, δ) = (2, 50, 0)`, they are `≈ 0.286` and `≈ 3.570`;
* in a random sample of about `2·10⁵` admissible points, the ratio [H]/Lean never exceeded
  `0.171`. It tends to about `0.19` as `q, x → ∞`.

The theorem carries no `Fact` binders.

**Relation: implied.** [H]'s statement implies the formal one. This is certified against the actual
Lean statements:
* `prop_9_3_2_implies_formal : prop_9_3_2 → type_of% @TernaryGoldbach.MajorArcs.prop_9_3_2`;
* `prop_9_3_2_implies_formal_one` and `prop_9_3_2_implies_formal_ne`, the same for the two halves.

The key step is `prop_9_3_2_err_le`: `err_{η,χ}(δ, x) ≤ err932N q T₀ δ x` for every `q ≥ 1`,
`x ≥ 1` and `T₀ ≥ max(10π|δ|, 50)`. The converse fails at the level of the constants:
`prop_9_3_2_err_lt_witness` proves `err_{η,χ}(0, 1) < err932N 2 50 0 1` for `q = 2`, `T₀ = 50`.
So the formal theorem is the weaker statement.

Auxiliary results:
* `prop_9_3_2_err_eq_err932` shows that the repository's `MajorArcs.err932`, its own transcription
  of (9.57), equals the error term transcribed here. `MajorArcs.prop_9_3_2` does not use `err932`.
* `prop_9_3_2_sum_eq` shows that the formal sum `Schar χ (Λ · φ(·/x)) (δ/x)` is the sum written
  here. `prop_9_3_2_summable` shows that this series converges absolutely.
-/

open Real MeasureTheory FourierTransform
open scoped ArithmeticFunction.vonMangoldt

namespace Companion.Book

open TernaryGoldbach (e Schar)
open TernaryGoldbach.MajorArcs (phiPos GRHUpTo)
open TernaryGoldbach.Explicit (BP BPz2 Jl ZL Z3 c3 ZLg Z3g c3g EB EA rhoA rhoB E0b E1b E2b E1g
  E2g Vb Vz DN thetaD errZ)

/-- **[H, (9.57)]**, the error term `err_{η,χ}(δ, x)` of [H, Prop 9.3.2], as printed (p. 182).

How it is transcribed:
* All constants are copied verbatim: `6.11`, `0.1598`, `1.578`, `0.1065`, `1.22`, `5.056`, `1.423`,
  `37.19`, `3`, `11`, `6`, `1`, `6`. `q` is the modulus, a natural number cast to `ℝ`.
* `log q T₀` in the second line means `log(qT₀)`, like the `log(qT₀/2π)` of the first line.
* `x^{−1/2}` and `x^{−3/2}` are real powers (`Real.rpow`). `x^{−1}` is `x⁻¹`.
* `e^{−0.1065 · T₀²/(πδ)²}` is meaningless at `δ = 0`. We read it there as its limit `0`, since
  `T₀²/(πδ)² → ∞`. [H]'s proof agrees: in Lemma 9.3.1, the function `f(τ)` of (9.48) contains
  this term only when `|τ| < (3/2)(πδ)²`, which never happens at `δ = 0`. Lean's convention
  `a/0 = 0` would give `e⁰ = 1` instead, which is a weaker and unintended reading. The repository's
  `MajorArcs.expδ` makes the same choice.
-/
noncomputable def prop_9_3_2_err (q : ℕ) (T0 δ x : ℝ) : ℝ :=
  T0 * Real.log (q * T0 / (2 * π)) *
      (6.11 * Real.exp (-0.1598 * T0) +
        1.578 * (if δ = 0 then 0 else Real.exp (-0.1065 * (T0 ^ 2 / (π * δ) ^ 2)))) +
    (1.22 * √T0 * Real.log (q * T0) + 5.056 * √T0 + 1.423 * Real.log q + 37.19) *
      x ^ (-(1 / 2) : ℝ) +
    (3 + 11 * |δ|) * x⁻¹ +
    (Real.log q + 6) * (1 + 6 * |δ|) * x ^ (-(3 / 2) : ℝ)

/-- **[H, Proposition 9.3.2]**, as printed (p. 182).

How the statement is transcribed:
* The weight `η(t) = t² e^{−t²/2}` is `TernaryGoldbach.MajorArcs.phiPos`: `t² e^{−t²/2}` for
  `t > 0` and `0` for `t ≤ 0`. In [H], `η` is a function on `ℝ₀⁺` (Lemma 9.1.1). Its Fourier
  transform is that of the extension by zero: the proof of Lemma 9.1.1 identifies the main term
  `G_δ(1) = ∫₀^∞ η(t) e(δt) dt` with `η̂(−δ)`. Both functions vanish at `t = 0`, so `phiPos` is
  exactly this extension. In the sum, only the values at `n/x > 0` matter.
* "`x ≥ 1`, `δ ∈ ℝ`" becomes `∀ x : ℝ, 1 ≤ x → ∀ δ : ℝ`.
* "`χ` a primitive character mod `q`, `q ≥ 1`" becomes `q : ℕ` with `[NeZero q]`,
  `χ : DirichletCharacter ℂ q` and `χ.IsPrimitive`, which says the conductor is `q`. Mathlib's
  `χ n` vanishes when `gcd(n, q) > 1`, as in [H]. For `q = 1` the only character is the trivial
  one, and `L(s, χ) = ζ(s)`.
* The hypothesis on zeros becomes `GRHUpTo χ T0`, the repository's definition: every zero `ρ` of
  `χ.LFunction` with `0 < ℜρ < 1` and `|ℑρ| ≤ T₀` has `ℜρ = 1/2`. [H]'s "non-trivial zeros" are
  those in the critical strip. Classically, `L(s, χ)` has no zeros on `ℜs = 1`, and none on
  `ℜs = 0` except the trivial zero at `s = 0` for even `χ ≠ 1`. So this is the same hypothesis.
  `T₀` is any real number that satisfies the next hypothesis.
* "`T₀ ≥ max(10π|δ|, 50)`" becomes `max (10 * π * |δ|) 50 ≤ T0`, as in the Lean theorem.
* `Σ_{n=1}^∞ Λ(n) χ(n) e(δn/x) η(n/x)` becomes
  `∑' n : ℕ, Λ n * χ n * e (δ / x * n) * phiPos (n / x)` in `ℂ`. Here `e t = exp(2πit)`
  (`TernaryGoldbach.e`) and `Λ` is Mathlib's von Mangoldt function. The extra `n = 0` term is zero
  because `Λ 0 = 0`. The series converges absolutely (`prop_9_3_2_summable`), so the `tsum` is the
  true sum.
* `η̂` is Mathlib's Fourier transform `𝓕 f (w) = ∫ e(−vw) f(v) dv`. This is [H]'s normalization
  `f̂(t) = ∫ e(−xt) f(x) dx` (§2.3). `phiPos` is integrable, so this is the true integral.
* `O*(E) · x` means a quantity of absolute value at most `E · x`. The two cases of (9.56) become
  two implications joined by `∧`: `q = 1 → ‖Σ − η̂(−δ) x‖ ≤ err · x` and `1 < q → ‖Σ‖ ≤ err · x`.
* `err_{η,χ}(δ, x)` is `prop_9_3_2_err q T0 δ x`, i.e. (9.57). -/
def prop_9_3_2 : Prop :=
  ∀ x : ℝ, 1 ≤ x → ∀ δ : ℝ, ∀ (q : ℕ) [NeZero q] (χ : DirichletCharacter ℂ q), χ.IsPrimitive →
    ∀ T0 : ℝ, GRHUpTo χ T0 → max (10 * π * |δ|) 50 ≤ T0 →
      (q = 1 → ‖(∑' n : ℕ, (Λ n : ℂ) * χ n * e (δ / x * n) * (phiPos (n / x) : ℂ)) -
          𝓕 (fun t : ℝ => (phiPos t : ℂ)) (-δ) * x‖ ≤ prop_9_3_2_err q T0 δ x * x) ∧
      (1 < q → ‖∑' n : ℕ, (Λ n : ℂ) * χ n * e (δ / x * n) * (phiPos (n / x) : ℂ)‖ ≤
          prop_9_3_2_err q T0 δ x * x)

/-! ## The sums and the error terms agree with the repository's -/

/-- The formal sum `Schar χ (n ↦ Λ(n) φ(n/x)) (δ/x) = Σ Λ(n) φ(n/x) χ(n) e(n δ/x)` is the sum of
`prop_9_3_2`. For `x ≥ 0`, `phiPos (n/x) = φ(n/x)` because `n/x ≥ 0` and `φ(0) = 0`. -/
theorem prop_9_3_2_sum_eq {q : ℕ} (χ : DirichletCharacter ℂ q) (δ : ℝ) {x : ℝ} (hx : 0 ≤ x) :
    Schar χ (fun n => ((Λ n * TernaryGoldbach.Helfgott.phi (n / x) : ℝ) : ℂ)) (δ / x) =
      ∑' n : ℕ, (Λ n : ℂ) * χ n * e (δ / x * n) * (phiPos (n / x) : ℂ) := by
  unfold Schar
  refine tsum_congr fun n => ?_
  have hp : phiPos (n / x) = TernaryGoldbach.Helfgott.phi (n / x) := by
    unfold phiPos
    split_ifs with h
    · rfl
    · have : (n : ℝ) / x = 0 := le_antisymm (not_lt.1 h) (div_nonneg (Nat.cast_nonneg n) hx)
      rw [this]; simp [TernaryGoldbach.Helfgott.phi]
  rw [hp, mul_comm (δ / x) (n : ℝ)]
  push_cast
  ring

/-- The series of `prop_9_3_2` converges absolutely for `x > 0`, so its `tsum` is the true sum.
Each term has norm at most `Λ(n) η(n/x)`, and `η(t) ≤ t² e^{−t²/2}`
(`TernaryGoldbach.Helfgott.summable_vonMangoldt_mul`). -/
theorem prop_9_3_2_summable {q : ℕ} (χ : DirichletCharacter ℂ q) (δ : ℝ) {x : ℝ} (hx : 0 < x) :
    Summable fun n : ℕ => ‖(Λ n : ℂ) * χ n * e (δ / x * n) * (phiPos (n / x) : ℂ)‖ := by
  have hs := TernaryGoldbach.Helfgott.summable_vonMangoldt_mul (η := phiPos) (C := 1)
    (c := 1 / 2) (k := 2) hx (by norm_num) fun t ht => by
      unfold phiPos TernaryGoldbach.Helfgott.phi
      split_ifs
      · rw [abs_of_nonneg (by positivity)]; ring_nf; exact le_rfl
      · rw [abs_zero]; positivity
  refine Summable.of_nonneg_of_le (fun n => norm_nonneg _) (fun n => ?_) hs
  rw [mul_right_comm, TernaryGoldbach.norm_mul_e, norm_mul, norm_mul, Complex.norm_real,
    Complex.norm_real, Complex.norm_real, norm_mul]
  have h1 : ‖χ n‖ ≤ 1 := DirichletCharacter.norm_le_one χ _
  have h2 : 0 ≤ ‖Λ n‖ := norm_nonneg _
  have h3 : 0 ≤ ‖phiPos (n / x)‖ := norm_nonneg _
  nlinarith [mul_le_mul_of_nonneg_left h1 h2]

/-- The repository's `MajorArcs.err932`, its own transcription of (9.57), is `prop_9_3_2_err` for
`x > 0`. It writes `x^{−1/2} = 1/√x` and `x^{−3/2} = 1/(x√x)`, and uses `MajorArcs.expδ` for the
`δ = 0` convention. -/
theorem prop_9_3_2_err_eq_err932 (q : ℕ) (T0 δ : ℝ) {x : ℝ} (hx : 0 < x) :
    prop_9_3_2_err q T0 δ x = TernaryGoldbach.MajorArcs.err932 q T0 δ x := by
  have e1 : x ^ (-(1 / 2) : ℝ) = (√x)⁻¹ := by rw [Real.rpow_neg hx.le, ← Real.sqrt_eq_rpow]
  have e3 : x ^ (-(3 / 2) : ℝ) = (x * √x)⁻¹ := by
    rw [Real.rpow_neg hx.le, show (3 / 2 : ℝ) = 1 + 1 / 2 by norm_num, Real.rpow_add hx,
      Real.rpow_one, ← Real.sqrt_eq_rpow]
  have hexp : (if δ = 0 then 0 else Real.exp (-0.1065 * (T0 ^ 2 / (π * δ) ^ 2))) =
      TernaryGoldbach.MajorArcs.expδ T0 δ := by
    unfold TernaryGoldbach.MajorArcs.expδ
    split_ifs
    · rfl
    · rw [mul_div_assoc]
  unfold prop_9_3_2_err TernaryGoldbach.MajorArcs.err932
  rw [e1, e3, hexp]
  simp only [div_eq_mul_inv]

/-! ## Comparing the error terms -/

/-- The two errors are cubic polynomials in `u = x^{−1/2} ∈ [0, 1]`. Each coefficient of [H] is
dominated by a coefficient of Lean. The middle term is absorbed by AM–GM:
`(3 + 11d) u² ≤ 8.5 u + 5.5 d² u³`, since `u(1 − u) ≥ 0` and `u(1 − du)² ≥ 0`. -/
theorem prop_9_3_2_combine {A A' B B' C' D D' d u : ℝ} (hu0 : 0 ≤ u) (hu1 : u ≤ 1)
    (hA : A ≤ A') (hB : B + 8.5 ≤ B') (hC : 0 ≤ C') (hD : D + 5.5 * d ^ 2 ≤ D') :
    A + B * u + (3 + 11 * d) * u ^ 2 + D * u ^ 3 ≤ A' + B' * u + C' * u ^ 2 + D' * u ^ 3 := by
  nlinarith [mul_nonneg hu0 (sq_nonneg (1 - d * u)), mul_nonneg hu0 (sub_nonneg.2 hu1),
    mul_le_mul_of_nonneg_right hB hu0, mul_le_mul_of_nonneg_right hD (pow_nonneg hu0 3),
    mul_nonneg hC (sq_nonneg u)]

/-- `3 ≤ log(qT₀)` for `q ≥ 1`, `T₀ ≥ 50`, because `e³ < 2.72³ < 50`. -/
theorem prop_9_3_2_log_ge {q T0 : ℝ} (hq : 1 ≤ q) (hT0 : 50 ≤ T0) : 3 ≤ Real.log (q * T0) := by
  have h50 : (50 : ℝ) ≤ q * T0 := by nlinarith
  have h3 : (3 : ℝ) ≤ Real.log 50 := by
    rw [Real.le_log_iff_exp_le (by norm_num)]
    have h1 := Real.exp_one_lt_d9
    have : Real.exp 3 = Real.exp 1 ^ 3 := by rw [← Real.exp_nat_mul]; norm_num
    rw [this]
    calc Real.exp 1 ^ 3 ≤ (2.7182818286 : ℝ) ^ 3 := pow_le_pow_left₀ (Real.exp_pos 1).le h1.le 3
      _ ≤ 50 := by norm_num
  exact h3.trans (Real.log_le_log (by norm_num) h50)

/-- A ratio `X/Y` of a logarithm `X ≥ 10ℓ` and a constant `0 < Y ≤ c` is at least `kℓ` when
`kc ≤ 10`. -/
theorem prop_9_3_2_ratio_ge {X Y ℓ k c : ℝ} (hY : 0 < Y) (hYc : Y ≤ c) (hℓ : 0 ≤ ℓ)
    (hX : 10 * ℓ ≤ X) (hk : k * c ≤ 10) (hk0 : 0 ≤ k) : k * ℓ ≤ X / Y := by
  rw [le_div_iff₀ hY]
  calc k * ℓ * Y ≤ k * ℓ * c := mul_le_mul_of_nonneg_left hYc (by positivity)
    _ = (k * c) * ℓ := by ring
    _ ≤ 10 * ℓ := mul_le_mul_of_nonneg_right hk hℓ
    _ ≤ X := hX

/-- `10 log(qT₀) ≤ log(B'_T/0.355)` once `0 < T₀ ≤ |T|`, since `B'_T ≥ 1400 q^{10} T₀^{10}`. -/
theorem prop_9_3_2_log_BP_ge {q : ℕ} [NeZero q] {T0 T : ℝ} (hT0 : 0 < T0) (hT : T0 ≤ |T|) :
    10 * Real.log (q * T0) ≤ Real.log (BP q T / 0.355) := by
  have hq1 : (1 : ℝ) ≤ q := by exact_mod_cast Nat.one_le_iff_ne_zero.2 (NeZero.ne q)
  have hpos : 0 < ((q : ℝ) * T0) ^ 10 := by positivity
  rw [show (10 : ℝ) * Real.log (q * T0) = Real.log (((q : ℝ) * T0) ^ 10) by
    rw [Real.log_pow]; norm_num]
  refine Real.log_le_log hpos ?_
  rw [le_div_iff₀ (by norm_num)]
  unfold BP
  rw [show (10 : ℝ) = ((10 : ℕ) : ℝ) by norm_num, Real.rpow_natCast]
  have h1 : T0 ^ 10 ≤ (1.25 * (|T| + 11)) ^ 10 :=
    pow_le_pow_left₀ hT0.le (by linarith) 10
  have h2 : (q : ℝ) ^ 10 ≤ (q : ℝ) ^ 9 * ((q : ℝ) + 1) := by
    rw [pow_succ]; gcongr; linarith
  have h3 : (1 : ℝ) ≤ |T| + 22 := by linarith [abs_nonneg T]
  calc ((q : ℝ) * T0) ^ 10 * 0.355 ≤ 1400 * ((q : ℝ) ^ 10 * T0 ^ 10) := by
        rw [mul_pow]; nlinarith [pow_pos hT0 10, pow_pos (by linarith : (0 : ℝ) < q) 10]
    _ ≤ 1400 * ((q : ℝ) ^ 9 * ((q : ℝ) + 1) * (|T| + 22) * (1.25 * (|T| + 11)) ^ 10) := by
        gcongr
        calc (q : ℝ) ^ 10 = (q : ℝ) ^ 10 * 1 := by ring
          _ ≤ (q : ℝ) ^ 9 * ((q : ℝ) + 1) * (|T| + 22) := by gcongr
    _ = 1400 * (q : ℝ) ^ 9 * ((q : ℝ) + 1) * (|T| + 22) * (1.25 * (|T| + 11)) ^ 10 := by ring

/-- `10 log T₀ ≤ log(B''_ζ(T)/0.355)` once `0 < T₀ ≤ |T|`, since `B''_ζ(T) ≥ 9200 T₀^{10}`. -/
theorem prop_9_3_2_log_BPz2_ge {T0 T : ℝ} (hT0 : 0 < T0) (hT : T0 ≤ |T|) :
    10 * Real.log T0 ≤ Real.log (BPz2 T / 0.355) := by
  have hpos : 0 < T0 ^ 10 := by positivity
  rw [show (10 : ℝ) * Real.log T0 = Real.log (T0 ^ 10) by rw [Real.log_pow]; norm_num]
  refine Real.log_le_log hpos ?_
  rw [le_div_iff₀ (by norm_num)]
  unfold BPz2
  have h1 : T0 ^ 9 ≤ (1.25 * (|T| + 11)) ^ 9 := pow_le_pow_left₀ hT0.le (by linarith) 9
  have h3 : T0 ≤ |T| + 22 := by linarith
  have h4 : 0 ≤ 20 * (|T| + 22) ^ 3 * (1.25 * (|T| + 11)) ^ 2 := by positivity
  calc T0 ^ 10 * 0.355 ≤ 9200 * (T0 * T0 ^ 9) := by nlinarith
    _ ≤ 9200 * ((|T| + 22) * (1.25 * (|T| + 11)) ^ 9) := by gcongr
    _ ≤ 9200 * (|T| + 22) * (1.25 * (|T| + 11)) ^ 9 +
          20 * (|T| + 22) ^ 3 * (1.25 * (|T| + 11)) ^ 2 := by linarith

/-- **The `x`-free term.** [H]'s first line is at most Lean's `E₂`, in the generic form shared by
`Explicit.E2b` (`q ≥ 2`) and `Explicit.E2g` (`q = 1`). Take `Z ≥ (30/7) log qT₀` and `c ≥ 0`.
Then:
* `6.11 T₀ log(qT₀/2π) e^{−0.1598T₀} ≤ E_B · 2Z`, as `0.892 · 2 · 30/7 > 6.11`;
* `1.578 T₀ log(qT₀/2π) e^{−0.1065(T₀/πδ)²} ≤ E_A · 2Z/(1 − ρ_A)`. This uses
  `1 − ρ_A ≤ 1.93 · 4.4/(π(|δ|+1))` and `T₀/(π|δ|) ≥ 10`. -/
theorem prop_9_3_2_term0_le {q : ℕ} {T0 δ ℓ Z c : ℝ} (hT0 : max (10 * π * |δ|) 50 ≤ T0)
    (hL : Real.log (q * T0 / (2 * π)) ≤ ℓ) (hℓ : 0 ≤ ℓ) (hZ : 30 / 7 * ℓ ≤ Z) (hc : 0 ≤ c) :
    T0 * Real.log (q * T0 / (2 * π)) *
        (6.11 * Real.exp (-0.1598 * T0) +
          1.578 * (if δ = 0 then 0 else Real.exp (-0.1065 * (T0 ^ 2 / (π * δ) ^ 2)))) ≤
      EB T0 * (2 * Z / (1 - rhoB) + 2 * c / (1 - rhoB) ^ 2) +
        EA T0 δ * (2 * Z / (1 - rhoA δ) + 2 * c / (1 - rhoA δ) ^ 2) := by
  have h50 : 50 ≤ T0 := (le_max_right _ _).trans hT0
  have h10 : 10 * π * |δ| ≤ T0 := (le_max_left _ _).trans hT0
  have hT0p : 0 < T0 := by linarith
  have hZ0 : 0 ≤ Z := by linarith
  set e1 := Real.exp (-0.1598 * T0) with he1
  have he1p : 0 < e1 := Real.exp_pos _
  set e2 := (if δ = 0 then 0 else Real.exp (-0.1065 * (T0 ^ 2 / (π * δ) ^ 2))) with he2
  have he2p : 0 ≤ e2 := by rw [he2]; split_ifs <;> positivity
  have step1 : T0 * Real.log (q * T0 / (2 * π)) * (6.11 * e1 + 1.578 * e2) ≤
      T0 * ℓ * (6.11 * e1 + 1.578 * e2) :=
    mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left hL hT0p.le) (by positivity)
  have hrB1 : rhoB < 1 := by unfold rhoB; rw [Real.exp_lt_one_iff]; norm_num
  have hrB0 : 0 < rhoB := Real.exp_pos _
  have hB1 : 2 * Z ≤ 2 * Z / (1 - rhoB) := by
    rw [le_div_iff₀ (by linarith)]; nlinarith
  have hB2 : 0 ≤ 2 * c / (1 - rhoB) ^ 2 := by positivity
  have partB : 6.11 * T0 * ℓ * e1 ≤ EB T0 * (2 * Z / (1 - rhoB) + 2 * c / (1 - rhoB) ^ 2) := by
    unfold EB
    rw [← he1]
    have hTe : 0 < T0 * e1 := mul_pos hT0p he1p
    calc 6.11 * T0 * ℓ * e1 ≤ 0.892 * T0 * e1 * (2 * Z) := by nlinarith
      _ ≤ 0.892 * T0 * e1 * (2 * Z / (1 - rhoB) + 2 * c / (1 - rhoB) ^ 2) :=
        mul_le_mul_of_nonneg_left (by linarith) (by positivity)
  have partA : 1.578 * T0 * ℓ * e2 ≤
      EA T0 δ * (2 * Z / (1 - rhoA δ) + 2 * c / (1 - rhoA δ) ^ 2) := by
    by_cases hδ : δ = 0
    · have h0 : e2 = 0 := by rw [he2, ite_eq_left hδ]
      have hEA : EA T0 δ = 0 := by unfold EA; rw [ite_eq_left hδ]
      rw [h0, hEA]; simp
    · have he2' : e2 = Real.exp (-0.1065 * (T0 / (π * |δ|)) ^ 2) := by
        rw [he2, ite_eq_right hδ, div_pow, mul_pow, mul_pow, sq_abs]
      have hEA : EA T0 δ =
          0.588 * (T0 / (π * |δ|)) ^ 2 * Real.exp (-0.1065 * (T0 / (π * |δ|)) ^ 2) := by
        unfold EA; rw [ite_eq_right hδ]
      rw [hEA, he2']
      set E := Real.exp (-0.1065 * (T0 / (π * |δ|)) ^ 2) with hE
      have hEp : 0 < E := Real.exp_pos _
      have hrA : rhoA δ = Real.exp (-(1.93 * 4.4 / (π * (|δ| + 1)))) := rfl
      set d := |δ| with hd
      have hdp : 0 < d := abs_pos.2 hδ
      have hπd : 0 < π * d := mul_pos Real.pi_pos hdp
      set w := T0 / (π * d) with hw
      have hTw : T0 = w * (π * d) := by rw [hw]; field_simp
      have hw10 : 10 ≤ w := by rw [hw, le_div_iff₀ hπd]; linarith
      set a := 1.93 * 4.4 / (π * (d + 1)) with ha
      have hap : 0 < a := by positivity
      have hrA1 : rhoA δ < 1 := by rw [hrA, Real.exp_lt_one_iff]; linarith
      have hrA2 : 1 - rhoA δ ≤ a := by rw [hrA]; linarith [Real.add_one_le_exp (-a)]
      have hK : 2 * Z / a ≤ 2 * Z / (1 - rhoA δ) :=
        div_le_div_of_nonneg_left (by linarith) (by linarith) hrA2
      have hc2 : 0 ≤ 2 * c / (1 - rhoA δ) ^ 2 := by positivity
      have h2Za : 2 * Z / a = 2 * Z * (π * (d + 1)) / (1.93 * 4.4) := by
        rw [ha]; field_simp
      have h1 : 30 / 7 * ℓ * d ≤ Z * (d + 1) := by
        nlinarith [mul_le_mul_of_nonneg_right hZ hdp.le]
      have hP : 0 ≤ w * (π * d) * ℓ := by positivity
      have key : 1.578 * T0 * ℓ ≤ 0.588 * w ^ 2 * (2 * Z / a) := by
        rw [h2Za, hTw]
        calc 1.578 * (w * (π * d)) * ℓ
            ≤ 0.588 * 2 / (1.93 * 4.4) * (30 / 7) * 10 * (w * (π * d) * ℓ) := by nlinarith
          _ ≤ 0.588 * 2 / (1.93 * 4.4) * (30 / 7) * w * (w * (π * d) * ℓ) := by gcongr
          _ = 0.588 * 2 / (1.93 * 4.4) * (w ^ 2 * π) * (30 / 7 * ℓ * d) := by ring
          _ ≤ 0.588 * 2 / (1.93 * 4.4) * (w ^ 2 * π) * (Z * (d + 1)) :=
            mul_le_mul_of_nonneg_left h1 (by positivity)
          _ = 0.588 * w ^ 2 * (2 * Z * (π * (d + 1)) / (1.93 * 4.4)) := by ring
      calc 1.578 * T0 * ℓ * E ≤ 0.588 * w ^ 2 * (2 * Z / a) * E :=
            mul_le_mul_of_nonneg_right key hEp.le
        _ = (0.588 * w ^ 2 * E) * (2 * Z / a) := by ring
        _ ≤ (0.588 * w ^ 2 * E) * (2 * Z / (1 - rhoA δ) + 2 * c / (1 - rhoA δ) ^ 2) :=
          mul_le_mul_of_nonneg_left (by linarith) (by positivity)
        _ = 0.588 * w ^ 2 * E * (2 * Z / (1 - rhoA δ) + 2 * c / (1 - rhoA δ) ^ 2) := by ring
  have hexp : T0 * ℓ * (6.11 * e1 + 1.578 * e2) =
      6.11 * T0 * ℓ * e1 + 1.578 * T0 * ℓ * e2 := by
    ring
  linarith

/-- **The `x^{−1/2}` term.** [H]'s `x^{−1/2}` coefficient, plus the `8.5` passed on by
`prop_9_3_2_combine`, is at most Lean's
`E₁ = Y · (√(2π · 0.6647 · 2J·3.48)/3.48 + √(2π · 0.1707 · 2J·3.48))` when `Y ≥ 2.9 log qT₀`. Both
forms `Explicit.E1b` and `Explicit.E1g` have this shape. Since `J · 3.48 > T₀`, we get
`E₁ ≥ 2.2 Y √T₀ ≥ 6.39 √T₀ log qT₀`. -/
theorem prop_9_3_2_term1_le {q : ℕ} [NeZero q] {T0 Y : ℝ} (hT0 : 50 ≤ T0)
    (hY : 2.9 * Real.log (q * T0) ≤ Y) :
    1.22 * √T0 * Real.log (q * T0) + 5.056 * √T0 + 1.423 * Real.log q + 37.19 + 8.5 ≤
      Y * (1 / 3.48 * √(2 * π * 0.6647 * (2 * (Jl T0 * 3.48))) +
        √(2 * π * 0.1707 * (2 * (Jl T0 * 3.48)))) := by
  have hq1 : (1 : ℝ) ≤ q := by exact_mod_cast Nat.one_le_iff_ne_zero.2 (NeZero.ne q)
  have hT0p : 0 < T0 := by linarith
  have hℓ : 3 ≤ Real.log (q * T0) := prop_9_3_2_log_ge hq1 hT0
  have hlq : Real.log q ≤ Real.log (q * T0) := Real.log_le_log (by linarith) (by nlinarith)
  have hr : 7 ≤ √T0 := Real.le_sqrt_of_sq_le (by linarith)
  have hJ : T0 < Jl T0 * 3.48 := TernaryGoldbach.Explicit.lt_Jl hT0p.le
  have hpi := Real.pi_gt_d2
  have hs1 : 2.8 * √T0 ≤ √(2 * π * 0.6647 * (2 * (Jl T0 * 3.48))) := by
    rw [Real.le_sqrt (by positivity) (by positivity), mul_pow, Real.sq_sqrt hT0p.le]
    nlinarith
  have hs2 : 1.4 * √T0 ≤ √(2 * π * 0.1707 * (2 * (Jl T0 * 3.48))) := by
    rw [Real.le_sqrt (by positivity) (by positivity), mul_pow, Real.sq_sqrt hT0p.le]
    nlinarith
  set ℓ := Real.log (q * T0) with hℓdef
  set r := √T0 with hrdef
  have hY0 : 0 ≤ Y := by linarith
  calc 1.22 * r * ℓ + 5.056 * r + 1.423 * Real.log q + 37.19 + 8.5
      ≤ 1.22 * r * ℓ + 5.056 * r + 1.423 * ℓ + 45.69 := by linarith
    _ ≤ 6.39 * r * ℓ := by nlinarith [mul_nonneg (sub_nonneg.2 hr) (sub_nonneg.2 hℓ)]
    _ ≤ Y * (70 / 87 * r + 1.4 * r) := by
      have hYr : 2.9 * ℓ * r ≤ Y * r := mul_le_mul_of_nonneg_right hY (by linarith)
      have hrl : 0 ≤ r * ℓ := mul_nonneg (by linarith) (by linarith)
      linarith
    _ ≤ Y * (1 / 3.48 * √(2 * π * 0.6647 * (2 * (Jl T0 * 3.48))) +
        √(2 * π * 0.1707 * (2 * (Jl T0 * 3.48)))) := by
      apply mul_le_mul_of_nonneg_left _ hY0
      have : 70 / 87 * r = 1 / 3.48 * (2.8 * r) := by ring
      rw [this]
      gcongr

/-- **The `x^{−3/2}` term.** [H]'s `x^{−3/2}` coefficient, plus the `5.5|δ|²` passed on by
`prop_9_3_2_combine`, is at most Lean's
`V/(2π) = 112 (2/log 2 + 4.8)(K · 2/θ_δ + 2.6 · 2/θ_δ²)/(2π)`, where `θ_δ = 0.28/(1 + |δ|)` and
`K ≥ log q + 6`. Lean takes `K = D_q + 37` for `Explicit.Vb` and `K = 40` for `Explicit.Vz`. -/
theorem prop_9_3_2_term3_le {q : ℕ} {δ K : ℝ} (hq0 : 0 ≤ Real.log q)
    (hK : Real.log q + 6 ≤ K) :
    (Real.log q + 6) * (1 + 6 * |δ|) + 5.5 * |δ| ^ 2 ≤
      112 * (2 / Real.log 2 + 4.8) * (K * (2 / thetaD δ) + 2.6 * (2 / thetaD δ ^ 2)) /
        (2 * π) := by
  have hd0 : 0 ≤ |δ| := abs_nonneg δ
  have h1 : 2 / thetaD δ = 50 / 7 * (1 + |δ|) := by unfold thetaD; field_simp; ring
  have h2 : 2 / thetaD δ ^ 2 = 1250 / 49 * (1 + |δ|) ^ 2 := by unfold thetaD; field_simp; ring
  rw [h1, h2]
  set d := |δ| with hd
  have hc1 : 4.8 ≤ 2 / Real.log 2 + 4.8 := by
    have := div_pos two_pos (Real.log_pos one_lt_two); linarith
  have hπ := Real.pi_lt_d2
  have hK0 : 0 ≤ K := by linarith
  rw [le_div_iff₀ (by positivity)]
  have hL0 : 0 ≤ (Real.log q + 6) * (1 + 6 * d) + 5.5 * d ^ 2 := by positivity
  have hLe : (Real.log q + 6) * (1 + 6 * d) + 5.5 * d ^ 2 ≤
      6 * K * (1 + d) + 5.5 * (1 + d) ^ 2 := by
    nlinarith [mul_le_mul_of_nonneg_right hK (by positivity : (0 : ℝ) ≤ 1 + 6 * d)]
  calc ((Real.log q + 6) * (1 + 6 * d) + 5.5 * d ^ 2) * (2 * π)
      ≤ (6 * K * (1 + d) + 5.5 * (1 + d) ^ 2) * 6.3 :=
        mul_le_mul hLe (by linarith) (by positivity) (by positivity)
    _ ≤ 112 * 4.8 * (K * (50 / 7 * (1 + d)) + 2.6 * (1250 / 49 * (1 + d) ^ 2)) := by
        nlinarith [mul_nonneg hK0 (by positivity : (0 : ℝ) ≤ 1 + d), sq_nonneg (1 + d)]
    _ ≤ 112 * (2 / Real.log 2 + 4.8) *
          (K * (50 / 7 * (1 + d)) + 2.6 * (1250 / 49 * (1 + d) ^ 2)) := by
        gcongr

/-- **[H]'s error term is at most Lean's**: `err_{η,χ}(δ, x) ≤ err932N q T₀ δ x` for every
`q ≥ 1`, `x ≥ 1` and `T₀ ≥ max(10π|δ|, 50)`. Write `s = √x ≥ 1`. Both sides become cubic
polynomials in `s⁻¹`, and `prop_9_3_2_combine` compares them coefficient by coefficient. The lemmas
`prop_9_3_2_term0_le`, `prop_9_3_2_term1_le` and `prop_9_3_2_term3_le` handle the coefficients.
They are fed the zero-count bounds `Z₃ ≥ (30/7) log qT₀` and `Z_L ≥ 2.9 log qT₀`, which come from
`B'_T, B''_ζ(T) ≥ 0.355 (qT₀)^{10}`, `log(10/3) ≤ 7/3` and `log(10/2.3) ≤ 3.35`. -/
theorem prop_9_3_2_err_le {q : ℕ} [NeZero q] {T0 δ x : ℝ} (hx : 1 ≤ x)
    (hT0 : max (10 * π * |δ|) 50 ≤ T0) :
    prop_9_3_2_err q T0 δ x ≤ TernaryGoldbach.MajorArcs.err932N q T0 δ x := by
  have hx0 : 0 < x := by linarith
  have h50 : 50 ≤ T0 := (le_max_right _ _).trans hT0
  have hT0p : 0 < T0 := by linarith
  have hq1 : (1 : ℝ) ≤ q := by exact_mod_cast Nat.one_le_iff_ne_zero.2 (NeZero.ne q)
  have hℓ : 3 ≤ Real.log (q * T0) := prop_9_3_2_log_ge hq1 h50
  have hL : Real.log (q * T0 / (2 * π)) ≤ Real.log (q * T0) :=
    Real.log_le_log (by positivity) (div_le_self (by positivity) (by linarith [Real.pi_gt_three]))
  have hlq0 : 0 ≤ Real.log q := Real.log_nonneg hq1
  have hl3 : 0 < Real.log (10 / 3) := Real.log_pos (by norm_num)
  have hl3' : Real.log (10 / 3) ≤ 7 / 3 := by
    have := Real.log_le_sub_one_of_pos (by norm_num : (0 : ℝ) < 10 / 3); linarith
  have hl23 : 0 < Real.log (10 / 2.3) := Real.log_pos (by norm_num)
  have hl23' : Real.log (10 / 2.3) ≤ 3.35 := by
    have := Real.log_le_sub_one_of_pos (by norm_num : (0 : ℝ) < 10 / 2.3); linarith
  have hT0abs : T0 ≤ |T0| := le_abs_self T0
  have hT0abs' : T0 ≤ |T0 + 3.48| := by rw [abs_of_pos (by linarith)]; linarith
  set s := √x with hs_def
  have hs1 : 1 ≤ s := Real.one_le_sqrt.2 hx
  have hs0 : 0 < s := by linarith
  have hxs : x = s ^ 2 := (Real.sq_sqrt hx0.le).symm
  have e1 : x ^ (-(1 / 2) : ℝ) = s⁻¹ := by rw [Real.rpow_neg hx0.le, ← Real.sqrt_eq_rpow]
  have e2 : x⁻¹ = s⁻¹ ^ 2 := by rw [hxs, inv_pow]
  have e3 : x ^ (-(3 / 2) : ℝ) = s⁻¹ ^ 3 := by
    rw [Real.rpow_neg hx0.le, inv_pow]
    congr 1
    rw [show (3 / 2 : ℝ) = 1 + 1 / 2 by norm_num, Real.rpow_add hx0, Real.rpow_one,
      ← Real.sqrt_eq_rpow, ← hs_def, hxs]
    ring
  have hform : ∀ a b c v : ℝ, a + b / s + c / x + v / (2 * π * (x * s)) =
      a + b * s⁻¹ + c * s⁻¹ ^ 2 + v / (2 * π) * s⁻¹ ^ 3 := by
    intro a b c v; rw [hxs]; field_simp
  have hu0 : 0 ≤ s⁻¹ := inv_nonneg.2 hs0.le
  have hu1 : s⁻¹ ≤ 1 := inv_le_one_of_one_le₀ hs1
  unfold prop_9_3_2_err
  rw [e1, e2, e3]
  unfold TernaryGoldbach.MajorArcs.err932N
  by_cases hq : q = 1
  · -- `q = 1`: Lean's `ζ` error term `errZ`
    rw [ite_eq_left hq]
    have hqR : (q : ℝ) = 1 := by rw [hq]; simp
    unfold errZ
    rw [← hs_def, hform]
    apply prop_9_3_2_combine hu0 hu1
    · unfold E2g
      refine prop_9_3_2_term0_le hT0 hL (by linarith) ?_
        (div_nonneg (div_nonneg (by norm_num) hT0p.le) hl3.le)
      unfold Z3g
      refine prop_9_3_2_ratio_ge hl3 hl3' (by linarith) ?_ (by norm_num) (by norm_num)
      rw [hqR, one_mul]
      exact prop_9_3_2_log_BPz2_ge hT0p hT0abs
    · unfold E1g
      refine prop_9_3_2_term1_le h50 ?_
      unfold ZLg
      refine prop_9_3_2_ratio_ge hl23 hl23' (by linarith) ?_ (by norm_num) (by norm_num)
      rw [hqR, one_mul]
      exact prop_9_3_2_log_BPz2_ge hT0p hT0abs'
    · unfold Z3g
      have : 1 ≤ BPz2 0 / 0.355 := by
        rw [le_div_iff₀ (by norm_num)]; unfold BPz2; norm_num
      exact mul_nonneg (by norm_num) (div_nonneg (Real.log_nonneg this) hl3.le)
    · unfold Vz
      exact prop_9_3_2_term3_le hlq0 (by rw [hqR, Real.log_one]; norm_num)
  · -- `q ≥ 2`: Lean's error term `errNew`
    rw [ite_eq_right hq]
    unfold TernaryGoldbach.MajorArcs.errNew
    rw [← hs_def, hform]
    apply prop_9_3_2_combine hu0 hu1
    · unfold E2b
      refine prop_9_3_2_term0_le hT0 hL (by linarith) ?_
        (div_nonneg (div_nonneg (by norm_num) hT0p.le) hl3.le)
      unfold Z3
      exact prop_9_3_2_ratio_ge hl3 hl3' (by linarith) (prop_9_3_2_log_BP_ge hT0p hT0abs)
        (by norm_num) (by norm_num)
    · unfold E1b
      refine prop_9_3_2_term1_le h50 ?_
      unfold ZL
      exact prop_9_3_2_ratio_ge hl23 hl23' (by linarith) (prop_9_3_2_log_BP_ge hT0p hT0abs')
        (by norm_num) (by norm_num)
    · unfold E0b
      exact mul_nonneg (by norm_num)
        (div_nonneg (TernaryGoldbach.Explicit.log_BP_pos q 0).le hl3.le)
    · unfold Vb
      refine prop_9_3_2_term3_le hlq0 ?_
      have : Real.log q ≤ DN q := by
        unfold DN
        apply Real.log_le_log (by linarith)
        rw [le_div_iff₀ (by norm_num)]
        have h9 : (1 : ℝ) ≤ (q : ℝ) ^ 9 := one_le_pow₀ hq1
        nlinarith [mul_nonneg (sub_nonneg.2 h9) (by linarith : (0 : ℝ) ≤ q + 1)]
      linarith

/-! ## The relation to the formal statements -/

/-- **[H, Prop 9.3.2] ⟹ the formal `TernaryGoldbach.MajorArcs.prop_9_3_2`.** The hypotheses match
one for one. The formal sum is [H]'s sum (`prop_9_3_2_sum_eq`), and both have the same main term
`𝓕 phiPos (−δ) · x` for `q = 1`. [H]'s error term is at most Lean's `err932N`
(`prop_9_3_2_err_le`). -/
theorem prop_9_3_2_implies_formal :
    prop_9_3_2 → type_of% @TernaryGoldbach.MajorArcs.prop_9_3_2 := by
  intro h x hx δ q _ χ hχ T0 hT0 hG
  have hx0 : 0 < x := by linarith
  rw [prop_9_3_2_sum_eq χ δ hx0.le]
  obtain ⟨h1, h2⟩ := h x hx δ q χ hχ T0 hG hT0
  have herr := mul_le_mul_of_nonneg_right (prop_9_3_2_err_le (q := q) hx hT0) hx0.le
  by_cases hq : q = 1
  · rw [ite_eq_left hq]
    exact (h1 hq).trans herr
  · rw [ite_eq_right hq, sub_zero]
    have : 1 < q := lt_of_le_of_ne (Nat.one_le_iff_ne_zero.2 (NeZero.ne q)) (Ne.symm hq)
    exact (h2 this).trans herr

/-- **[H, Prop 9.3.2] ⟹ the formal `q ≥ 2` half `TernaryGoldbach.MajorArcs.prop_9_3_2_ne`**,
whose error term is `MajorArcs.errNew`. This is `err932N` at `q ≠ 1`. -/
theorem prop_9_3_2_implies_formal_ne :
    prop_9_3_2 → type_of% @TernaryGoldbach.MajorArcs.prop_9_3_2_ne := by
  intro h x hx δ q _ hq χ hχ T0 hT0 hG
  have hx0 : 0 < x := by linarith
  rw [prop_9_3_2_sum_eq χ δ hx0.le]
  have herr := prop_9_3_2_err_le (q := q) hx hT0
  unfold TernaryGoldbach.MajorArcs.err932N at herr
  rw [ite_eq_right hq] at herr
  have : 1 < q := lt_of_le_of_ne (Nat.one_le_iff_ne_zero.2 (NeZero.ne q)) (Ne.symm hq)
  exact ((h x hx δ q χ hχ T0 hG hT0).2 this).trans (mul_le_mul_of_nonneg_right herr hx0.le)

/-- **[H, Prop 9.3.2] ⟹ the formal `q = 1` half `TernaryGoldbach.MajorArcs.prop_9_3_2_one`**,
whose error term is `Explicit.errZ`. This is `err932N` at `q = 1`. -/
theorem prop_9_3_2_implies_formal_one :
    prop_9_3_2 → type_of% @TernaryGoldbach.MajorArcs.prop_9_3_2_one := by
  intro h x hx δ q _ hq χ hχ T0 hT0 hG
  have hx0 : 0 < x := by linarith
  rw [prop_9_3_2_sum_eq χ δ hx0.le]
  have herr := prop_9_3_2_err_le (q := q) hx hT0
  unfold TernaryGoldbach.MajorArcs.err932N at herr
  rw [ite_eq_left hq] at herr
  exact ((h x hx δ q χ hχ T0 hG hT0).1 hq).trans (mul_le_mul_of_nonneg_right herr hx0.le)

/-- **A numerical witness that the formal error term is larger.** At `q = 2`, `T₀ = 50`, `δ = 0`,
`x = 1`, [H]'s error term (`≈ 123.6`) is smaller than Lean's `err932N 2 50 0 1` (`≈ 64 492`). The
proof uses crude bounds: [H]'s value is below `5600`, and Lean's `V/(2π)` term alone exceeds
`28 000`. So the formal bound does not give [H]'s constants. -/
theorem prop_9_3_2_err_lt_witness :
    prop_9_3_2_err 2 50 0 1 < TernaryGoldbach.MajorArcs.err932N 2 50 0 1 := by
  have hpi := Real.pi_gt_d2
  have hpi' := Real.pi_lt_d2
  -- [H]'s side
  have hbook : prop_9_3_2_err 2 50 0 1 ≤ 5600 := by
    unfold prop_9_3_2_err
    simp only [Nat.cast_ofNat, abs_zero, ite_true, Real.one_rpow, inv_one, mul_zero, add_zero,
      mul_one]
    have hl1 : Real.log (2 * 50 / (2 * π)) ≤ 15 := by
      have h := Real.log_le_sub_one_of_pos (by positivity : (0 : ℝ) < 2 * 50 / (2 * π))
      have : 2 * 50 / (2 * π) ≤ 16 := by rw [div_le_iff₀ (by positivity)]; linarith
      linarith
    have hl2 : Real.log (2 * 50) ≤ 99 := by
      have := Real.log_le_sub_one_of_pos (by norm_num : (0 : ℝ) < 2 * 50); linarith
    have hl3 : Real.log 2 ≤ 1 := by
      have := Real.log_le_sub_one_of_pos (by norm_num : (0 : ℝ) < 2); linarith
    have hl30 : 0 ≤ Real.log 2 := Real.log_nonneg (by norm_num)
    have hs : √50 ≤ 7.1 := (Real.sqrt_le_left (by norm_num)).2 (by norm_num)
    have hs0 : 0 ≤ √(50 : ℝ) := Real.sqrt_nonneg _
    have he : Real.exp (-0.1598 * 50) ≤ 1 := Real.exp_le_one_iff.2 (by norm_num)
    have he0 : 0 ≤ Real.exp (-0.1598 * 50) := (Real.exp_pos _).le
    have hl20 : 0 ≤ Real.log (2 * 50) := Real.log_nonneg (by norm_num)
    have h1 : 50 * Real.log (2 * 50 / (2 * π)) * (6.11 * Real.exp (-0.1598 * 50)) ≤
        50 * 15 * 6.11 := by
      have : 0 ≤ 50 * (6.11 * Real.exp (-0.1598 * 50)) := by positivity
      nlinarith
    have h2 : 1.22 * √50 * Real.log (2 * 50) ≤ 1.22 * 7.1 * 99 := by
      have := mul_le_mul hs hl2 hl20 (by norm_num); nlinarith
    nlinarith
  -- Lean's side: the `x^{-3/2}` term `V/(2π)` alone
  have hlean : 28000 ≤ TernaryGoldbach.MajorArcs.err932N 2 50 0 1 := by
    unfold TernaryGoldbach.MajorArcs.err932N
    rw [ite_eq_right (by norm_num : (2 : ℕ) ≠ 1)]
    unfold TernaryGoldbach.MajorArcs.errNew
    rw [Real.sqrt_one, div_one, div_one, mul_one, mul_one]
    have hE2 : 0 ≤ E2b 2 50 0 := by
      unfold E2b
      have hEA : EA 50 0 = 0 := by unfold EA; rw [ite_eq_left rfl]
      rw [hEA, zero_mul, add_zero]
      have hrB1 : rhoB < 1 := by unfold rhoB; rw [Real.exp_lt_one_iff]; norm_num
      have := TernaryGoldbach.Explicit.Z3_nonneg 2 50
      have := TernaryGoldbach.Explicit.c3_nonneg (T0 := 50) (by norm_num)
      have : 0 < 1 - rhoB := by linarith
      exact mul_nonneg (TernaryGoldbach.Explicit.EB_nonneg (by norm_num)) (by positivity)
    have hE1 : 0 ≤ E1b 2 50 := by
      unfold E1b
      exact mul_nonneg (TernaryGoldbach.Explicit.ZL_nonneg 2 50) (by positivity)
    have hE0 : 0 ≤ E0b 2 := by
      unfold E0b
      exact mul_nonneg (by norm_num) (div_nonneg (TernaryGoldbach.Explicit.log_BP_pos 2 0).le
        (Real.log_pos (by norm_num)).le)
    have hV : 28000 ≤ Vb 2 0 / (2 * π) := by
      unfold Vb thetaD
      simp only [abs_zero, add_zero]
      have hD := TernaryGoldbach.Explicit.DN_nonneg 2
      have hc1 : 4.8 ≤ 2 / Real.log 2 + 4.8 := by
        have := div_pos two_pos (Real.log_pos one_lt_two); linarith
      rw [le_div_iff₀ (by positivity)]
      have hb : (37 : ℝ) * (2 / (0.28 / 1)) + 2.6 * (2 / (0.28 / 1) ^ 2) ≤
          (DN 2 + 37) * (2 / (0.28 / 1)) + 2.6 * (2 / (0.28 / 1) ^ 2) := by
        have : (0 : ℝ) ≤ 2 / (0.28 / 1) := by norm_num
        nlinarith
      have hb0 : (0 : ℝ) ≤ (DN 2 + 37) * (2 / (0.28 / 1)) + 2.6 * (2 / (0.28 / 1) ^ 2) := by
        positivity
      calc 28000 * (2 * π) ≤ 28000 * 6.3 := by nlinarith
        _ ≤ 112 * 4.8 * ((37 : ℝ) * (2 / (0.28 / 1)) + 2.6 * (2 / (0.28 / 1) ^ 2)) := by
            norm_num
        _ ≤ 112 * (2 / Real.log 2 + 4.8) *
              ((DN 2 + 37) * (2 / (0.28 / 1)) + 2.6 * (2 / (0.28 / 1) ^ 2)) := by
            apply mul_le_mul (by linarith) hb (by norm_num) (by positivity)
    linarith
  linarith

end Companion.Book
