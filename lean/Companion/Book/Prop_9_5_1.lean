import TernaryGoldbach

/-!
# [H, Proposition 9.5.1]: the sum `Σ Λ(n) (log n) η₊²(n/x)` under RH up to height `T₀`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §9.5
("A sum for `η₊(t)²`"), Proposition 9.5.1 (label `prop:konechno`), printed page 188
(<https://arxiv.org/pdf/1501.05438v2#page=198>):

> Let `η = η₊` be as in (9.63), `H ≥ 25`. Let `x ≥ 10⁸`. Assume that all non-trivial zeros `ρ` of
> the Riemann zeta function `ζ(s)` with `|ℑ(ρ)| ≤ T₀` lie on the critical line, where
> `T₀ ≥ max(2H + 25, 200)`. Then
> `Σ_{n=1}^∞ Λ(n) (log n) η₊²(n/x) = x · ∫₀^∞ η₊²(t) log xt dt + O*(err_{ℓ₂,η₊}) · x log x`
> (9.72), where
> `err_{ℓ₂,η₊} = ((0.462 (log T₁)²/log x + 0.909 log T₁) T₁ + 1.71 (1 + log T₁/log x) H) e^{−(π/4) T₁}
>             + (2.445 √T₀ log T₀ + 50.04) · x^{−1/2}` (9.73)
> and `T₁ = T₀ − 2H`.

Here (9.63) is `η₊(t) = h_H(t) · t e^{−t²/2}`, with `h_H` as in (7.6). So `η₊` depends on the
parameter `H`. The book uses the proposition once, in §9.6 (p. 197, (9.93)). There it takes
`H = 200`, `T₀ = 450` (so `T₁ = 50`) and `x ≥ 10¹²`, and gets
`err_{ℓ₂,η₊} ≤ 5.123·10⁻¹⁵ + 366.91/√x`, the `E₁` bound of [H, Prop 7.1.5]. The 2013 major-arcs
preprint (arXiv:1305.2897v4, Prop. 4.12) had `H ≥ 50`, `T₀ ≥ 2H + max(H/4, 50)` and a different
`err_{ℓ₂,η₊}`. §9.6 still picks `T₀ = 2H + max(50, H/4) = 450` by that older rule, and the 2015
hypothesis `T₀ ≥ max(2H + 25, 200) = 425` allows it.

**What the formalization proves.** `TernaryGoldbach.MajorArcs.prop_9_5_1`
(`TernaryGoldbach/MajorArcs/Prop715.lean:299`). For `x ≥ 4.9·10²⁶`, if `GRHUpTo 1 500` holds (every
zero of `L(·, 1) = ζ` with `0 < ℜρ < 1` and `|ℑρ| ≤ 500` has `ℜρ = 1/2`), then
`|Σ Λ(n) (log n) η₊²(n/x) − x ∫₀^∞ η₊²(t) log(xt) dt| ≤ 10⁻⁸ · x log x`. Here `η₊` is the repo's
`etaPlus`, which has `H = 200`. The proof does not go through [H]'s `err_{ℓ₂,η₊}`. It splits
`log n = log x + log(n/x)` and applies the repository's own explicit formulas for `η₊²` and
`η₊² log` with `T₀ = 500` (`Explicit/EtaPlusSqBound.lean`), with its own constants. The theorem
carries no `Fact` binders, and its only hypothesis on zeros is the explicit `GRHUpTo 1 500`.

**Relation: implied.** [H]'s statement implies the formal one. This is certified by
`prop_9_5_1_implies_formal : prop_9_5_1 → type_of% @TernaryGoldbach.MajorArcs.prop_9_5_1`. Its proof
specializes [H] to:
* `H = 200`. The book's `η₊` at `H = 200` is the repo's `etaPlus` by `rfl` (`prop_9_5_1_etaPlus_200`);
* `T₀ = 500`. This is allowed, since `max(2·200 + 25, 200) = 425 ≤ 500`. The zero hypothesis is
  `GRHUpTo 1 500`, read through `L(·, 1) = ζ` (`prop_9_5_1_RH_iff`).

It then bounds `err_{ℓ₂,η₊}(H = 200, T₀ = 500, x) ≤ 1.8·10⁻¹¹` for `x ≥ 4.9·10²⁶`
(`prop_9_5_1_err_200_500_le`). The formal statement is weaker in four ways:
* it covers only `H = 200` ([H]: every `H ≥ 25`);
* it covers only `x ≥ 4.9·10²⁶` ([H]: `x ≥ 10⁸`);
* it covers only `T₀ = 500` ([H]: every `T₀ ≥ max(2H + 25, 200)`, with an error depending on `T₀`);
* its error is `10⁻⁸`. [H]'s `err_{ℓ₂,η₊}(200, 500, x)` is `1.761·10⁻¹¹` at `x = 4.9·10²⁶` and
  decreases like `389.80/√x` (its `e^{−25π}` part is `6.2·10⁻³²`). The Lean constant is about 570
  times larger. At `T₀ = 450`, the book's own choice, `err_{ℓ₂,η₊}` is `1.658·10⁻¹¹` at
  `x = 4.9·10²⁶`.
So the book's statement cannot be recovered from the Lean theorem.

Auxiliary results:
* `prop_9_5_1_at_200_500` is what [H] gives at the formal parameters:
  `|Σ − x ∫| ≤ 1.8·10⁻¹¹ · x log x` for `x ≥ 4.9·10²⁶` under RH up to `500`;
* `prop_9_5_1_iff_bound` shows the existential error term is a real constraint. Since `x log x > 0`,
  the definition is equivalent to the explicit inequality `|Σ − x ∫| ≤ err_{ℓ₂,η₊} · x log x`;
* `prop_9_5_1_err_pos` shows `err_{ℓ₂,η₊} > 0` in the whole range, so the statement is not
  trivially false;
* `prop_9_5_1_hyps_satisfiable` shows the statement is not vacuous. Under the repository's
  hypothesis `PlattGRH` (which gives RH up to height `10⁸`, `Explicit.rh_upto_1e8`), `H = 200`,
  `x = 10⁸`, `T₀ = 500` meet all the hypotheses.
-/

open Real Set MeasureTheory
open scoped ArithmeticFunction.vonMangoldt

namespace Companion.Book

open TernaryGoldbach.Helfgott (etaPlus hH)

/-- The book's `η₊` with parameter `H`, [H, (9.63)]: `η₊(t) = h_H(t) · t e^{−t²/2}`.

`h_H` is the repository's `TernaryGoldbach.Helfgott.hH H`, which takes `H` as an argument. We
checked it against [H, (7.5)–(7.6)]:
* `hBase` is the `h` of (7.5), `h(t) = t²(2 − t)³ e^{t − 1/2}` on `[0, 2]` and `0` elsewhere;
* `F H y = sin(H log y)/(π log y)` is the `F_H` of (7.6). (7.6) prints `F_H(t)` and
  `(h *_M F_H)(y)`, typos for `F_H(y)` and `(h *_M F_H)(t)`. At `y = 1`, Lean's `F` takes the value
  `0/0 = 0` instead of the limit `H/π`. This is one point and does not change the integral;
* `hH H t = ∫_{y>0} h(t/y) F_H(y) dy/y`, as printed in (7.6).

The repository's `etaPlus` fixes `H = 200` inside the definition. [H, Prop 9.5.1] is stated for
every `H ≥ 25`, so the book's object is defined here with `H` free, and `prop_9_5_1_etaPlus_200`
identifies the case `H = 200` with `etaPlus`. -/
noncomputable def prop_9_5_1_etaPlus (H t : ℝ) : ℝ := hH H t * t * Real.exp (-t ^ 2 / 2)

/-- At `H = 200` the book's `η₊` is the repository's `etaPlus`, by definition. -/
theorem prop_9_5_1_etaPlus_200 : prop_9_5_1_etaPlus 200 = etaPlus := rfl

/-- The zero hypothesis of [H, Prop 9.5.1] at height `T₀`: all non-trivial zeros `ρ` of `ζ` with
`|ℑ(ρ)| ≤ T₀` lie on the critical line. `ζ` is Mathlib's `riemannZeta`. "Non-trivial zero" is read
as a zero in the open critical strip `0 < ℜρ < 1`, as in the repository's `Explicit.RHBelow` and `GRHUpTo`.
Mathematically this is the same as reading it as "a zero other than `−2, −4, …`": `ζ` has no zeros
with `ℜs ≥ 1`, and its only zeros with `ℜs ≤ 0` are `−2, −4, …`. That equivalence is not formalized
here. -/
def prop_9_5_1_RH (T₀ : ℝ) : Prop :=
  ∀ ρ : ℂ, riemannZeta ρ = 0 → 0 < ρ.re → ρ.re < 1 → |ρ.im| ≤ T₀ → ρ.re = 1 / 2

/-- `err_{ℓ₂,η₊}` of [H, (9.73)], with `T₁ = T₀ − 2H`. The constants `0.462`, `0.909`, `1.71`,
`2.445`, `50.04` are copied verbatim (decimal literals are exact rationals). `(log T₁)²` is
`Real.log T₁ ^ 2`, `e^{−(π/4) T₁}` is `Real.exp (-(π / 4) * T₁)`, `√T₀` is `Real.sqrt T₀`, and
`x^{−1/2}` is the real power `x ^ (-(1 / 2 : ℝ))`. In the range of the proposition, `T₁ ≥ 25` and
`x ≥ 10⁸`, so every logarithm is positive. -/
noncomputable def prop_9_5_1_err (H T₀ x : ℝ) : ℝ :=
  let T₁ := T₀ - 2 * H
  ((0.462 * Real.log T₁ ^ 2 / Real.log x + 0.909 * Real.log T₁) * T₁ +
      1.71 * (1 + Real.log T₁ / Real.log x) * H) * Real.exp (-(π / 4) * T₁) +
    (2.445 * √T₀ * Real.log T₀ + 50.04) * x ^ (-(1 / 2 : ℝ))

/-- **[H, Proposition 9.5.1]**, as printed (p. 188).

How the statement is transcribed:
* "`η = η₊` as in (9.63), `H ≥ 25`": `H : ℝ` with `25 ≤ H`, and `η₊ = prop_9_5_1_etaPlus H`, the
  book's `h_H(t) · t e^{−t²/2}` with `H` free (see `prop_9_5_1_etaPlus`). The repository's `etaPlus`
  is the case `H = 200` only.
* "`x ≥ 10⁸`": `x : ℝ` with `10 ^ 8 ≤ x`.
* The zero hypothesis is `prop_9_5_1_RH T₀`, with "`T₀ ≥ max(2H + 25, 200)`" as
  `max (2 * H + 25) 200 ≤ T₀`, `T₀ : ℝ`. `T₀` is universally quantified: the statement holds for
  every admissible `T₀` up to which RH is known, with an error depending on `T₀`.
* `Σ_{n=1}^∞ Λ(n) (log n) η₊²(n/x)` becomes
  `∑' n : ℕ, Λ n * Real.log n * prop_9_5_1_etaPlus H (n / x) ^ 2`, reading `η₊²(n/x)` as
  `(η₊(n/x))²`. The extra `n = 0` term is zero because `Λ 0 = 0`.
* `∫₀^∞ η₊²(t) log xt dt` becomes `∫ t in Ioi 0, prop_9_5_1_etaPlus H t ^ 2 * Real.log (x * t)`.
  Here `log xt` means `log(xt)`, as the proof says: `η₊,₂ = (log x) η₊² + η₊² log = η₊²(t) log xt`.
* The series converges absolutely and the integrand is integrable, for every `H > 0`. Indeed
  `|F_H| ≤ H/π`, so `|h_H(t)| ≤ (H/π) ∫₀² h(u) du/u` is bounded, and `η₊` has Gaussian decay. So
  the `tsum` and the Bochner integral are the true sum and integral. For `H = 200`, the case the
  formal comparison uses, the proof of `MajorArcs.prop_9_5_1` establishes both facts for the two
  pieces `η₊²` and `η₊² log` (`Explicit.summable_SsumG` with `Explicit.goodSmoothing_phi1`/`phi2`,
  and `MajorArcs.integrableOn_of_mellinConvergent_one`). For other `H` they are not formalized
  here.
* `O*(err_{ℓ₂,η₊}) · x log x` ([H, §2.1]: `O*(R)` is a quantity of absolute value at most `R`)
  becomes `∃ E, |E| ≤ prop_9_5_1_err H T₀ x ∧ … = … + E * x * Real.log x`. `E` is quantified after
  `H, x, T₀`, so it may depend on them. Because `x log x > 0`, the equation determines `E`, so this
  is the printed claim and not a weakening (`prop_9_5_1_iff_bound`).
* There are no other hypotheses. In particular nothing is assumed about Platt's verification or
  about the repository's `Fact` inputs. -/
def prop_9_5_1 : Prop :=
  ∀ H : ℝ, 25 ≤ H → ∀ x : ℝ, 10 ^ 8 ≤ x → ∀ T₀ : ℝ, max (2 * H + 25) 200 ≤ T₀ →
    prop_9_5_1_RH T₀ →
      ∃ E : ℝ, |E| ≤ prop_9_5_1_err H T₀ x ∧
        ∑' n : ℕ, Λ n * Real.log n * prop_9_5_1_etaPlus H (n / x) ^ 2 =
          x * (∫ t in Ioi 0, prop_9_5_1_etaPlus H t ^ 2 * Real.log (x * t)) + E * x * Real.log x

/-- The book's zero hypothesis at height `T₀` is the repository's `GRHUpTo 1 T₀` for the trivial
character mod `1`, whose `L`-function is `ζ` (`TernaryGoldbach.Explicit.LFunction_one_mod_one`). -/
theorem prop_9_5_1_RH_iff (T₀ : ℝ) :
    prop_9_5_1_RH T₀ ↔ TernaryGoldbach.MajorArcs.GRHUpTo (1 : DirichletCharacter ℂ 1) T₀ := by
  unfold prop_9_5_1_RH TernaryGoldbach.MajorArcs.GRHUpTo
  rw [TernaryGoldbach.Explicit.LFunction_one_mod_one]

/-- `1 ≤ log x` for `x ≥ 10⁸`, since `e < 10⁸`. -/
theorem prop_9_5_1_log_ge_one {x : ℝ} (hx : 10 ^ 8 ≤ x) : 1 ≤ Real.log x := by
  rw [Real.le_log_iff_exp_le (by linarith)]
  have := Real.exp_one_lt_d9
  linarith

/-- When `x log x > 0`, an error term `E` with `|E| ≤ B` and `S = M + E · x log x` exists if and only if
`|S − M| ≤ B · x log x`. -/
theorem prop_9_5_1_err_iff {S M B x : ℝ} (hc : 0 < x * Real.log x) :
    (∃ E : ℝ, |E| ≤ B ∧ S = M + E * x * Real.log x) ↔ |S - M| ≤ B * (x * Real.log x) := by
  constructor
  · rintro ⟨E, hE, rfl⟩
    rw [show M + E * x * Real.log x - M = E * (x * Real.log x) by ring, abs_mul, abs_of_pos hc]
    exact mul_le_mul_of_nonneg_right hE hc.le
  · intro h
    refine ⟨(S - M) / (x * Real.log x), ?_, ?_⟩
    · rw [abs_div, abs_of_pos hc, div_le_iff₀ hc]
      exact h
    · have e : (S - M) / (x * Real.log x) * x * Real.log x =
          (S - M) / (x * Real.log x) * (x * Real.log x) := by ring
      rw [e, div_mul_cancel₀ _ hc.ne']
      ring

/-- **Non-vacuity check (conclusion).** The existential error term of `prop_9_5_1` is a real
constraint. Since `x log x > 0` for `x ≥ 10⁸`, the definition is equivalent to the explicit
inequality `|Σ − x ∫| ≤ err_{ℓ₂,η₊} · x log x`. -/
theorem prop_9_5_1_iff_bound : prop_9_5_1 ↔
    ∀ H : ℝ, 25 ≤ H → ∀ x : ℝ, 10 ^ 8 ≤ x → ∀ T₀ : ℝ, max (2 * H + 25) 200 ≤ T₀ →
      prop_9_5_1_RH T₀ →
        |∑' n : ℕ, Λ n * Real.log n * prop_9_5_1_etaPlus H (n / x) ^ 2 -
            x * ∫ t in Ioi 0, prop_9_5_1_etaPlus H t ^ 2 * Real.log (x * t)| ≤
          prop_9_5_1_err H T₀ x * (x * Real.log x) := by
  unfold prop_9_5_1
  refine forall_congr' fun H => imp_congr_right fun _ => forall_congr' fun x =>
    imp_congr_right fun hx => forall_congr' fun T₀ => imp_congr_right fun _ =>
      imp_congr_right fun _ => ?_
  have hc : 0 < x * Real.log x :=
    mul_pos (by linarith) (by linarith [prop_9_5_1_log_ge_one hx])
  exact prop_9_5_1_err_iff hc

/-- **Non-vacuity check (error term).** `err_{ℓ₂,η₊} > 0` throughout the range of the proposition, so
the bound `|E| ≤ err_{ℓ₂,η₊}` can be met and the statement is not trivially false. -/
theorem prop_9_5_1_err_pos {H x T₀ : ℝ} (hH : 25 ≤ H) (hx : 10 ^ 8 ≤ x)
    (hT : max (2 * H + 25) 200 ≤ T₀) : 0 < prop_9_5_1_err H T₀ x := by
  have hT1 : 25 ≤ T₀ - 2 * H := by have := le_max_left (2 * H + 25) 200; linarith
  have hT0 : 200 ≤ T₀ := (le_max_right _ _).trans hT
  have hx0 : 0 < x := by linarith
  have hL : 0 < Real.log x := by linarith [prop_9_5_1_log_ge_one hx]
  have hl : 0 < Real.log (T₀ - 2 * H) := Real.log_pos (by linarith)
  have hl0 : 0 < Real.log T₀ := Real.log_pos (by linarith)
  simp only [prop_9_5_1_err]
  have hA : 0 ≤ ((0.462 * Real.log (T₀ - 2 * H) ^ 2 / Real.log x + 0.909 * Real.log (T₀ - 2 * H)) *
      (T₀ - 2 * H) + 1.71 * (1 + Real.log (T₀ - 2 * H) / Real.log x) * H) := by
    have h1 : 0 ≤ 0.462 * Real.log (T₀ - 2 * H) ^ 2 / Real.log x := div_nonneg (by positivity) hL.le
    have h2 : 0 ≤ Real.log (T₀ - 2 * H) / Real.log x := div_nonneg hl.le hL.le
    have h3 : 0 ≤ 0.462 * Real.log (T₀ - 2 * H) ^ 2 / Real.log x + 0.909 * Real.log (T₀ - 2 * H) := by
      linarith
    have h4 : 0 ≤ 1.71 * (1 + Real.log (T₀ - 2 * H) / Real.log x) := by linarith
    exact add_nonneg (mul_nonneg h3 (by linarith)) (mul_nonneg h4 (by linarith))
  have hB : 0 < 2.445 * √T₀ * Real.log T₀ + 50.04 := by
    have := mul_nonneg (mul_nonneg (by norm_num : (0 : ℝ) ≤ 2.445) (Real.sqrt_nonneg T₀)) hl0.le
    linarith
  exact add_pos_of_nonneg_of_pos (mul_nonneg hA (Real.exp_pos _).le)
    (mul_pos hB (Real.rpow_pos_of_pos hx0 _))

/-- **Non-vacuity check (hypotheses).** Under the repository's hypothesis `TernaryGoldbach.PlattGRH`
(which gives RH up to height `10⁸`, `TernaryGoldbach.Explicit.rh_upto_1e8`), the hypotheses of
[H, Prop 9.5.1] are met, for instance by `H = 200`, `x = 10⁸`, `T₀ = 500`. -/
theorem prop_9_5_1_hyps_satisfiable [Fact TernaryGoldbach.PlattGRH] :
    ∃ H x T₀ : ℝ, 25 ≤ H ∧ 10 ^ 8 ≤ x ∧ max (2 * H + 25) 200 ≤ T₀ ∧ prop_9_5_1_RH T₀ := by
  refine ⟨200, 10 ^ 8, 500, by norm_num, le_rfl, max_le (by norm_num) (by norm_num), ?_⟩
  intro ρ h0 h1 h2 h3
  exact TernaryGoldbach.Explicit.rh_upto_1e8 ρ h0 h1 h2 (h3.trans (by norm_num))

/-- [H]'s error term at the formal parameters `H = 200`, `T₀ = 500` (so `T₁ = 100`): for
`x ≥ 4.9·10²⁶`, `err_{ℓ₂,η₊} ≤ 1.8·10⁻¹¹` (the true value at `x = 4.9·10²⁶` is `1.761·10⁻¹¹`).
The bounds used are `log 100 ≤ 7 log 2 ≤ 4.86`, `log 500 ≤ 9 log 2 ≤ 6.24`, `√500 ≤ 22.37`,
`e^{−25π} ≤ e^{−75} ≤ 10⁻³⁰` and `x^{−1/2} ≤ 1/(2.2135·10¹³)`. -/
theorem prop_9_5_1_err_200_500_le {x : ℝ} (hx : 4.9e26 ≤ x) :
    prop_9_5_1_err 200 500 x ≤ 1.8e-11 := by
  have hx0 : 0 < x := by linarith
  have hL : 1 ≤ Real.log x := prop_9_5_1_log_ge_one (by linarith)
  simp only [prop_9_5_1_err]
  rw [show (500 : ℝ) - 2 * 200 = 100 by norm_num]
  have h2 := Real.log_two_lt_d9
  have hl0 : 0 ≤ Real.log 100 := Real.log_nonneg (by norm_num)
  have hl1 : Real.log 100 ≤ 4.86 := by
    have h : Real.log 100 ≤ Real.log (2 ^ 7) := Real.log_le_log (by norm_num) (by norm_num)
    rw [Real.log_pow] at h
    push_cast at h
    linarith
  have hm0 : 0 ≤ Real.log 500 := Real.log_nonneg (by norm_num)
  have hm1 : Real.log 500 ≤ 6.24 := by
    have h : Real.log 500 ≤ Real.log (2 ^ 9) := Real.log_le_log (by norm_num) (by norm_num)
    rw [Real.log_pow] at h
    push_cast at h
    linarith
  have hs1 : √(500 : ℝ) ≤ 22.37 := by
    rw [Real.sqrt_le_left (by norm_num)]
    norm_num
  have he0 : 0 ≤ Real.exp (-(π / 4) * 100) := (Real.exp_pos _).le
  have he1 : Real.exp (-(π / 4) * 100) ≤ 1e-30 := by
    have hpi := Real.pi_gt_three
    have h1 : Real.exp (-(π / 4) * 100) ≤ Real.exp (-75) := Real.exp_le_exp.2 (by linarith)
    have h75 : (1e30 : ℝ) ≤ Real.exp 75 := by
      have e75 : Real.exp 75 = Real.exp 1 ^ 75 := by rw [← Real.exp_nat_mul]; norm_num
      rw [e75]
      have he := Real.exp_one_gt_d9
      calc (1e30 : ℝ) ≤ 2.7 ^ 75 := by norm_num
        _ ≤ Real.exp 1 ^ 75 := pow_le_pow_left₀ (by norm_num) (by linarith) 75
    rw [Real.exp_neg] at h1
    calc Real.exp (-(π / 4) * 100) ≤ (Real.exp 75)⁻¹ := h1
      _ ≤ (1e30 : ℝ)⁻¹ := inv_anti₀ (by norm_num) h75
      _ = 1e-30 := by norm_num
  have hr0 : 0 ≤ x ^ (-(1 / 2 : ℝ)) := (Real.rpow_pos_of_pos hx0 _).le
  have hr1 : x ^ (-(1 / 2 : ℝ)) ≤ 4.52e-14 := by
    rw [Real.rpow_neg hx0.le, ← Real.sqrt_eq_rpow]
    have hs : (2.2135e13 : ℝ) ≤ √x := Real.le_sqrt_of_sq_le (by norm_num; linarith)
    calc (√x)⁻¹ ≤ (2.2135e13 : ℝ)⁻¹ := inv_anti₀ (by norm_num) hs
      _ ≤ 4.52e-14 := by norm_num
  have hA : (0.462 * Real.log 100 ^ 2 / Real.log x + 0.909 * Real.log 100) * 100 +
      1.71 * (1 + Real.log 100 / Real.log x) * 200 ≤ 4000 := by
    have h1 : Real.log 100 ^ 2 / Real.log x ≤ Real.log 100 ^ 2 := div_le_self (sq_nonneg _) hL
    have h2 : Real.log 100 / Real.log x ≤ Real.log 100 := div_le_self hl0 hL
    have h3 : Real.log 100 ^ 2 ≤ 4.86 ^ 2 := pow_le_pow_left₀ hl0 hl1 2
    have e1 : 0.462 * Real.log 100 ^ 2 / Real.log x = 0.462 * (Real.log 100 ^ 2 / Real.log x) := by
      ring
    rw [e1]
    nlinarith
  have hB : 2.445 * √(500 : ℝ) * Real.log 500 + 50.04 ≤ 391.5 := by
    have := mul_le_mul hs1 hm1 hm0 (by norm_num)
    nlinarith
  calc ((0.462 * Real.log 100 ^ 2 / Real.log x + 0.909 * Real.log 100) * 100 +
          1.71 * (1 + Real.log 100 / Real.log x) * 200) * Real.exp (-(π / 4) * 100) +
        (2.445 * √(500 : ℝ) * Real.log 500 + 50.04) * x ^ (-(1 / 2 : ℝ))
      ≤ 4000 * 1e-30 + 391.5 * 4.52e-14 :=
        add_le_add (mul_le_mul hA he1 he0 (by norm_num)) (mul_le_mul hB hr1 hr0 (by norm_num))
    _ ≤ 1.8e-11 := by norm_num

/-- **What [H, Prop 9.5.1] gives at the formal parameters.** Specializing [H] to `H = 200` (the
repository's `etaPlus`) and `T₀ = 500`: for `x ≥ 4.9·10²⁶`, under RH up to height `500`,
`|Σ Λ(n) (log n) η₊²(n/x) − x ∫₀^∞ η₊²(t) log(xt) dt| ≤ 1.8·10⁻¹¹ · x log x`. The formal theorem
`TernaryGoldbach.MajorArcs.prop_9_5_1` proves this with `10⁻⁸` in place of `1.8·10⁻¹¹`. -/
theorem prop_9_5_1_at_200_500 (h : prop_9_5_1) {x : ℝ} (hx : 4.9e26 ≤ x)
    (hRH : prop_9_5_1_RH 500) :
    |∑' n : ℕ, Λ n * Real.log n * etaPlus (n / x) ^ 2 -
        x * ∫ t in Ioi 0, etaPlus t ^ 2 * Real.log (x * t)| ≤ 1.8e-11 * (x * Real.log x) := by
  have hx0 : 0 < x := by linarith
  have hxl : 0 < x * Real.log x :=
    mul_pos hx0 (by linarith [prop_9_5_1_log_ge_one (x := x) (by linarith)])
  have h1 := h 200 (by norm_num) x (by linarith) 500 (max_le (by norm_num) (by norm_num)) hRH
  rw [prop_9_5_1_etaPlus_200, prop_9_5_1_err_iff hxl] at h1
  exact h1.trans (mul_le_mul_of_nonneg_right (prop_9_5_1_err_200_500_le hx) hxl.le)

/-- **[H, Prop 9.5.1] ⟹ the formal statement** `TernaryGoldbach.MajorArcs.prop_9_5_1`. Take `H = 200`
and `T₀ = 500` in [H]. The Lean hypothesis `GRHUpTo 1 500` is [H]'s zero hypothesis at height `500`
(`prop_9_5_1_RH_iff`). Then `prop_9_5_1_at_200_500` gives the bound `1.8·10⁻¹¹ · x log x`, which is
below Lean's `10⁻⁸ · x log x`. -/
theorem prop_9_5_1_implies_formal :
    prop_9_5_1 → type_of% @TernaryGoldbach.MajorArcs.prop_9_5_1 := by
  intro h x hx hG
  have hx' : (4.9e26 : ℝ) ≤ x := by linarith
  have hxl : 0 < x * Real.log x :=
    mul_pos (by linarith) (by linarith [prop_9_5_1_log_ge_one (x := x) (by linarith)])
  refine (prop_9_5_1_at_200_500 h hx' ((prop_9_5_1_RH_iff 500).2 hG)).trans ?_
  exact mul_le_mul_of_nonneg_right (by norm_num) hxl.le

end Companion.Book
