import TernaryGoldbach

/-!
# [H, Proposition 7.1.5]: the sum `Σ Λ(n) (log n) η₊²(n/x)`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2,
Proposition 7.1.5 (p. 140, label `prop:malheur`;
<https://arxiv.org/pdf/1501.05438v2#page=150>). Let `η(t) = η₊(t) = h_H(t) t e^{-t²/2}`, with `h_H`
as in (7.6) and `H = 200`, and let `x ≥ 10¹²` be real. Then

```
Σ_{n=1}^∞ Λ(n) (log n) η²(n/x) = x · ∫₀^∞ η₊²(t) log(xt) dt + E₁ · x log x
                               = 0.640206 x log x − 0.021095 x + E₂ · x log x,
|E₁| ≤ 5.123·10⁻¹⁵ + 366.91/√x,        |E₂| ≤ 2·10⁻⁶ + 366.91/√x.
```

The proposition carries no hypothesis on the zeros of `ζ`. [H, §9.6] derives it from
[H, Prop 9.5.1] at `T₀ = 450`, using the known verification of RH up to that height. The `E₁` bound is
[H, (9.93)], and the `E₂` line follows from it with the value of the integral, [H, (9.94)].

**What the formalization proves.**
* `TernaryGoldbach.MajorArcs.prop_7_1_5'` (`MajorArcs/Prop715.lean:356`; re-exported verbatim as
  `TernaryGoldbach.MinorArcs.prop_7_1_5`, the form the minor-arc total uses) proves the `E₂` line with
  [H]'s constants `0.640206`, `0.021095` and `2·10⁻⁶ + 366.91/√x`, but only for `x ≥ 4.9·10²⁶`
  ([H]: `x ≥ 10¹²`). It uses the hypothesis `PlattGRH`, which gives RH up to height 500 through
  `platt_odd` at `q = 1`.
* `TernaryGoldbach.MajorArcs.prop_9_5_1` (`MajorArcs/Prop715.lean:299`) proves the `E₁` line in a weaker
  form: `|Σ − x ∫₀^∞ η₊²(t) log(xt) dt| ≤ 10⁻⁸ · x log x` for `x ≥ 4.9·10²⁶`, assuming RH up to
  height 500 (`GRHUpTo 1 500`). For such `x`, [H]'s bound on `|E₁|` is below `1.7·10⁻¹¹`.

**Relation: implied.** [H]'s statement implies the formal ones. The formal ones are weaker in two
respects, so they do not give [H]'s statement back: the range (`10¹² ≤ x < 4.9·10²⁶` is not covered)
and the size of `E₁` (`10⁻⁸` against `5.123·10⁻¹⁵ + 366.91/√x`). The direction is certified against the
actual Lean statements:
* `prop_7_1_5_implies_formal : prop_7_1_5 → type_of% @TernaryGoldbach.MajorArcs.prop_7_1_5'`;
* `prop_7_1_5_implies_formal_cited : prop_7_1_5 → type_of% @TernaryGoldbach.MinorArcs.prop_7_1_5`;
* `prop_7_1_5_implies_formal_E1 : prop_7_1_5 → type_of% @TernaryGoldbach.MajorArcs.prop_9_5_1`.

Auxiliary results:
* `prop_7_1_5_iff_bounds` shows the existential error terms are real constraints. Since `x log x > 0`,
  the definition is equivalent to two explicit inequalities.
* `prop_7_1_5_iff_line1` shows the `E₂` line follows from the `E₁` line for every `x ≥ 10¹²`. The proof
  uses the formalized (9.94), `TernaryGoldbach.MajorArcs.integral_etaPlus_sq_log`, which is proved and
  has no hypotheses. So [H]'s proposition is equivalent to its first line alone, and that line (in [H]'s
  range and with [H]'s constants) is exactly what the formalization lacks.

**A note on [H]'s proof.** [H] derives (9.94) on p. 197 by splitting off a cross term
`2 ∫ (η₊ − η∘) η∘ log(xt) dt`. It then bounds `∫ (η₊ − η∘) η∘ log(xt) dt` by Cauchy–Schwarz,
getting `1.944·10⁻⁶ log x + 5.2·10⁻⁷`, and carries that bound forward without the factor `2`. With the
factor, the same pieces give about `3.89·10⁻⁶ log x + 1.26·10⁻⁶`, and at `x = 10¹²` only
`|E₂| ≲ 3.94·10⁻⁶ + 366.91/√x`. Even without the factor, the listed pieces give a constant of about
`7.4·10⁻⁷` rather than `5.3·10⁻⁷`, because the `2.2·10⁻⁷` from rounding `−0.0210947786…` to `−0.021095`
is left out. That slip alone does not affect the `2·10⁻⁶`. The repository proves (9.94) with [H]'s
printed constants anyway, using a sharper (Parseval) argument (`integral_etaPlus_sq_log`).
`prop_7_1_5_iff_line1` goes through that theorem, not through [H]'s argument.
-/

open Real Set MeasureTheory
open scoped ArithmeticFunction.vonMangoldt

namespace Companion.Book

open TernaryGoldbach.Helfgott (etaPlus)

/-- **[H, Proposition 7.1.5]**, as printed (p. 140).

How the statement is transcribed:
* `η = η₊` is the repository's `TernaryGoldbach.Helfgott.etaPlus`, `η₊(t) = h₂₀₀(t) · t · e^{−t²/2}`. We
  checked it against [H, (7.4)–(7.6)]:
  - `hBase` is the `h` of (7.5);
  - `F H y = sin(H log y)/(π log y)` is the `F_H` of (7.6). (7.6) writes `F_H(t)` and `(h *_M F_H)(y)`,
    typos for `F_H(y)` and `(h *_M F_H)(t)`; we read it as a function of `y`;
  - `hH H t = ∫_{y>0} h(t/y) F_H(y) dy/y`, an absolutely convergent integral for every `t`;
  - `H = 200` is fixed inside `etaPlus`.

  At `y = 1`, Lean's `F` takes the value `0/0 = 0` rather than the limit `H/π`. This is a single point
  and does not change the integral.
* "`x` a real number `≥ 10¹²`" becomes `∀ x : ℝ, 1e12 ≤ x → …`. Both displayed equalities are claimed
  for every such `x`, so they are joined by `∧`.
* `Σ_{n=1}^∞ Λ(n) (log n) η²(n/x)` becomes `∑' n : ℕ, Λ n * Real.log n * etaPlus (n / x) ^ 2`, reading
  `η²(n/x)` as `(η(n/x))²`. The extra `n = 0` term is zero because `Λ 0 = 0`. For every `x > 0` the
  series converges absolutely. Termwise it is `log x` times the series for `η₊²` plus the series for
  `η₊² log`, and both are absolutely convergent by `TernaryGoldbach.Explicit.summable_SsumG` (as used
  in `MajorArcs.prop_9_5_1`). So the `tsum` is the true sum.
* `∫₀^∞ η₊²(t) log x t dt` becomes `∫ t in Ioi 0, etaPlus t ^ 2 * Real.log (x * t)`. Here `log x t`
  means `log(xt)`, as in [H, §9.5], where `η₊²(t) log xt = (log x) η₊²(t) + η₊²(t) log t`. Both `η₊²`
  and `η₊² log` are integrable on `(0, ∞)` (shown in the proof of `MajorArcs.prop_9_5_1`), so the
  Bochner integral is the true integral.
* [H] defines `E₁` and `E₂` through the displayed equalities. Each becomes
  `∃ Eᵢ, |Eᵢ| ≤ bound ∧ equality`. Because `x log x > 0`, the equality determines `Eᵢ`, so this is [H]'s
  claim and not a weakening (see `prop_7_1_5_iff_bounds`). `Eᵢ · x log x` is written
  `Eᵢ * x * Real.log x`, as in the repository's `prop_7_1_5'`.
* The constants are copied verbatim: `0.640206`, `0.021095`, `5.123·10⁻¹⁵` (`5.123e-15`), `366.91`,
  `2·10⁻⁶` (`2e-6`). `√x` is `Real.sqrt x`.
* There is no hypothesis on zeros, on Platt's verification or on any other input, because the printed
  proposition is unconditional. -/
def prop_7_1_5 : Prop :=
  ∀ x : ℝ, 1e12 ≤ x →
    (∃ E₁ : ℝ, |E₁| ≤ 5.123e-15 + 366.91 / √x ∧
      ∑' n : ℕ, Λ n * Real.log n * etaPlus (n / x) ^ 2 =
        x * (∫ t in Ioi 0, etaPlus t ^ 2 * Real.log (x * t)) + E₁ * x * Real.log x) ∧
    (∃ E₂ : ℝ, |E₂| ≤ 2e-6 + 366.91 / √x ∧
      ∑' n : ℕ, Λ n * Real.log n * etaPlus (n / x) ^ 2 =
        0.640206 * x * Real.log x - 0.021095 * x + E₂ * x * Real.log x)

/-- `27 ≤ log x` for `x ≥ 10¹²`. This repeats the proof of `TernaryGoldbach.MajorArcs.log_ge_1e12`. -/
theorem prop_7_1_5_log_ge {x : ℝ} (hx : 1e12 ≤ x) : 27 ≤ Real.log x := by
  have h : (27 : ℝ) ≤ Real.log 1e12 := by
    rw [Real.le_log_iff_exp_le (by norm_num)]
    have h1 := Real.exp_one_lt_d9
    have : Real.exp 27 = Real.exp 1 ^ 27 := by rw [← Real.exp_nat_mul]; norm_num
    rw [this]
    calc Real.exp 1 ^ 27 ≤ (2.7182818286 : ℝ) ^ 27 := pow_le_pow_left₀ (Real.exp_pos 1).le h1.le 27
      _ ≤ 1e12 := by norm_num
  exact h.trans (Real.log_le_log (by norm_num) hx)

/-- When `x log x > 0`, an error term `E` with `|E| ≤ B` and `S = M + E · x log x` exists if and only if
`|S − M| ≤ B · x log x`. -/
theorem prop_7_1_5_err_iff {S M B x : ℝ} (hc : 0 < x * Real.log x) :
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

/-- **Non-vacuity check.** The existential error terms of `prop_7_1_5` are real constraints. Since
`x log x > 0` for `x ≥ 10¹²`, the definition is equivalent to two explicit inequalities. -/
theorem prop_7_1_5_iff_bounds : prop_7_1_5 ↔ ∀ x : ℝ, 1e12 ≤ x →
    |∑' n : ℕ, Λ n * Real.log n * etaPlus (n / x) ^ 2 -
        x * ∫ t in Ioi 0, etaPlus t ^ 2 * Real.log (x * t)| ≤
      (5.123e-15 + 366.91 / √x) * (x * Real.log x) ∧
    |∑' n : ℕ, Λ n * Real.log n * etaPlus (n / x) ^ 2 -
        (0.640206 * x * Real.log x - 0.021095 * x)| ≤
      (2e-6 + 366.91 / √x) * (x * Real.log x) := by
  unfold prop_7_1_5
  refine forall_congr' fun x => imp_congr_right fun hx => ?_
  have hc : 0 < x * Real.log x :=
    mul_pos (by linarith) (by linarith [prop_7_1_5_log_ge hx])
  rw [prop_7_1_5_err_iff hc, prop_7_1_5_err_iff hc]

/-- **The `E₂` line follows from the `E₁` line.** With the formalized value of the integral, [H, (9.94)]
(`TernaryGoldbach.MajorArcs.integral_etaPlus_sq_log`, proved and without hypotheses), the second line
of [H, Prop 7.1.5] follows from the first for every `x ≥ 10¹²`. So [H]'s proposition is equivalent to
its first line. Writing `L = log x ≥ 27`, the resulting `E₂` satisfies
`|E₂| ≤ |E₁| + (1.95·10⁻⁶ L + 5.3·10⁻⁷)/L ≤ 5.123·10⁻¹⁵ + 366.91/√x + 1.95·10⁻⁶ + 5.3·10⁻⁷/27`, and the
right side is at most `2·10⁻⁶ + 366.91/√x`. This is [H]'s step to (9.95). -/
theorem prop_7_1_5_iff_line1 : prop_7_1_5 ↔ ∀ x : ℝ, 1e12 ≤ x →
    ∃ E₁ : ℝ, |E₁| ≤ 5.123e-15 + 366.91 / √x ∧
      ∑' n : ℕ, Λ n * Real.log n * etaPlus (n / x) ^ 2 =
        x * (∫ t in Ioi 0, etaPlus t ^ 2 * Real.log (x * t)) + E₁ * x * Real.log x := by
  refine ⟨fun h x hx => (h x hx).1, fun h x hx => ⟨h x hx, ?_⟩⟩
  obtain ⟨E₁, hE₁, hS⟩ := h x hx
  have hx0 : 0 < x := by linarith
  have hlx := prop_7_1_5_log_ge hx
  have hxl : 0 < x * Real.log x := mul_pos hx0 (by linarith)
  have hI := TernaryGoldbach.MajorArcs.integral_etaPlus_sq_log (by linarith : (1 : ℝ) ≤ x)
  rw [prop_7_1_5_err_iff hxl, hS]
  set I := ∫ t in Ioi 0, etaPlus t ^ 2 * Real.log (x * t)
  calc |x * I + E₁ * x * Real.log x - (0.640206 * x * Real.log x - 0.021095 * x)|
      = |E₁ * (x * Real.log x) + x * (I - (0.640206 * Real.log x - 0.021095))| := by
        congr 1; ring
    _ ≤ |E₁ * (x * Real.log x)| + |x * (I - (0.640206 * Real.log x - 0.021095))| := abs_add_le _ _
    _ = |E₁| * (x * Real.log x) + x * |I - (0.640206 * Real.log x - 0.021095)| := by
        rw [abs_mul E₁, abs_of_pos hxl, abs_mul x, abs_of_pos hx0]
    _ ≤ (5.123e-15 + 366.91 / √x) * (x * Real.log x) + x * (1.95e-6 * Real.log x + 5.3e-7) :=
        add_le_add (mul_le_mul_of_nonneg_right hE₁ hxl.le) (mul_le_mul_of_nonneg_left hI hx0.le)
    _ ≤ (2e-6 + 366.91 / √x) * (x * Real.log x) := by
        nlinarith [mul_nonneg hx0.le (sub_nonneg.2 hlx)]

/-- **[H, Prop 7.1.5] ⟹ the formal `E₂` statement.** [H]'s second line, at any `x ≥ 4.9·10²⁶ ≥ 10¹²`,
is `TernaryGoldbach.MajorArcs.prop_7_1_5'`. Lean's theorem has a narrower range and adds the
`Fact PlattGRH` hypothesis, which is simply not needed here. -/
theorem prop_7_1_5_implies_formal :
    prop_7_1_5 → type_of% @TernaryGoldbach.MajorArcs.prop_7_1_5' := by
  intro h _ x hx
  exact (h x (by linarith)).2

/-- **[H, Prop 7.1.5] ⟹ the cited `E₂` statement** `TernaryGoldbach.MinorArcs.prop_7_1_5`, the verbatim
re-export of `MajorArcs.prop_7_1_5'` that the minor-arc total (`MinorArcs.T_le`) consumes. -/
theorem prop_7_1_5_implies_formal_cited :
    prop_7_1_5 → type_of% @TernaryGoldbach.MinorArcs.prop_7_1_5 := by
  intro h _ x hx
  exact (h x (by linarith)).2

/-- **[H, Prop 7.1.5] ⟹ the formal `E₁` statement.** [H]'s first line implies
`TernaryGoldbach.MajorArcs.prop_9_5_1`. For `x ≥ 4.9·10²⁶` we have `√x ≥ 10¹³`, so
`|E₁| ≤ 5.123·10⁻¹⁵ + 366.91·10⁻¹³ < 10⁻⁸`. The hypothesis `GRHUpTo 1 500` of the Lean theorem is not
needed. -/
theorem prop_7_1_5_implies_formal_E1 :
    prop_7_1_5 → type_of% @TernaryGoldbach.MajorArcs.prop_9_5_1 := by
  intro h x hx _
  obtain ⟨⟨E₁, hE₁, hS⟩, -⟩ := h x (by linarith)
  have hx0 : 0 < x := by linarith
  have hxl : 0 < x * Real.log x :=
    mul_pos hx0 (by linarith [prop_7_1_5_log_ge (by linarith : (1e12 : ℝ) ≤ x)])
  have hs : (1e13 : ℝ) ≤ √x := Real.le_sqrt_of_sq_le (by norm_num; linarith)
  have hq : 366.91 / √x ≤ 366.91 / 1e13 :=
    div_le_div_of_nonneg_left (by norm_num) (by norm_num) hs
  have hq' : 366.91 / √x ≤ 3.7e-11 := hq.trans (by norm_num)
  refine ((prop_7_1_5_err_iff hxl).1 ⟨E₁, hE₁, hS⟩).trans (mul_le_mul_of_nonneg_right ?_ hxl.le)
  linarith

end Companion.Book
