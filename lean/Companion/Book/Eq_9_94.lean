import TernaryGoldbach

/-!
# [H, (9.94)]: `∫₀^∞ η₊²(t) log(xt) dt = (0.640206 + O*(1.95·10⁻⁶)) log x − 0.021095 + O*(5.3·10⁻⁷)`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §9.6,
display (9.94) (label `eq:kokord`), p. 197 (<https://arxiv.org/pdf/1501.05438v2#page=207>):
```
∫₀^∞ η₊²(t) log xt dt = (0.640206 + O*(1.95·10⁻⁶)) log x − 0.021095 + O*(5.3·10⁻⁷).
```
Here `η₊(t) = h_H(t) t e^{−t²/2}` with `H = 200` ([H, (7.4)–(7.6)] and (9.63)). `O*(R)` means "a
quantity at most `R` in absolute value" ([H, §2.1], p. 31). The display gives no range for `x`.
It is part of the last step of §9.6, the derivation of [H, Prop 7.1.5]. Shortly before it, [H]
says "We make, again, the assumption `x ≥ 10¹²`" (p. 197). Right after it, [H] uses that
assumption to pass to (9.95) (p. 198), which gives Prop 7.1.5. The 2013 preprint
(arXiv:1305.2897v4, (4.88), p. 60) has the same display and the same derivation.

**How [H] derives it, and two slips.** [H] writes `η₊² = η∘² + 2(η₊ − η∘)η∘ + (η₊ − η∘)²` and
bounds the three integrals against `log xt`:
* the main term, `(0.64020599736635 + O(10⁻¹⁴)) log x − 0.021094778698867 + O(10⁻¹⁵)`, computed
  with VNODE-LP;
* `∫ (η₊ − η∘)η∘ log xt ≤ 1.944·10⁻⁶ log x + 5.2·10⁻⁷`, by Cauchy–Schwarz and (A.23);
* the square term, `≤ 5.903·10⁻¹² log x + 2.143·10⁻¹²`.

The conclusion then has two slips:
* The cross term is counted once, although it appears with a factor `2`. With the factor, the same
  pieces give only about `3.89·10⁻⁶ log x + 1.26·10⁻⁶`.
* Even without the factor `2`, the constant term needs the `2.21·10⁻⁷` that is lost when
  `−0.021094778698867` is rounded to `−0.021095`. The pieces then give `≈ 7.41·10⁻⁷`, not
  `5.3·10⁻⁷`. (The `log x` coefficient, `≈ 1.9466·10⁻⁶ ≤ 1.95·10⁻⁶`, does include its own rounding
  error of `2.6·10⁻⁹`.)

So the printed proof does not establish the printed constants. The printed statement is still
true, and the formalization proves it. (The factor-2 slip is recorded in the repo's `AXIOMS.md`,
Finding 3, and in `companion/ERRATA.md` under Prop 7.1.5. The figures above were recomputed
here.)

**What the formalization proves.** `TernaryGoldbach.MajorArcs.integral_etaPlus_sq_log`
(`MajorArcs/EtaPlusSqLog.lean:886`) states that for every real `x ≥ 1`,
`|∫_{(0,∞)} η₊(t)² log(xt) dt − (0.640206 log x − 0.021095)| ≤ 1.95·10⁻⁶ log x + 5.3·10⁻⁷`.
These are exactly [H]'s constants. The theorem has no hypotheses: it has no `Fact` binders, and its
mask in `companion/data/hypothesis_trace.json` is empty. It depends only on `propext`,
`Classical.choice` and `Quot.sound`. The proof uses the same splitting, written in `u = log t`.
For the cross terms it uses Parseval instead of Cauchy–Schwarz (`abs_integral_Dg_mul_le`), which
gives `O(H⁻⁴)` instead of `O(H^{−7/2})`. It proves the two `η∘` integrals itself
(`etaO_numerics`). With the bounds used in that proof, its pieces add up to about
`8.8·10⁻⁷ log x + 5.0·10⁻⁷`.

**Relation: proved.** The formal theorem implies [H]'s statement. This is certified against the
theorem's actual type:
* `eq_9_94_of_formal : type_of% @TernaryGoldbach.MajorArcs.integral_etaPlus_sq_log → eq_9_94`.
  The formal range `x ≥ 1` contains [H]'s `x ≥ 10¹²`. For `log x ≥ 0`, the pair of `O*` terms says
  the same thing as the single inequality (`eq_9_94_iff_bound`).
* `eq_9_94_holds : eq_9_94`.

Auxiliary results:
* `eq_9_94_oStar_iff` and `eq_9_94_iff_bound` show that the existential error terms are a real
  constraint: `eq_9_94` is equivalent to an explicit two-sided bound.
* `eq_9_94_integrableOn`: for every `x > 0` the integrand is Lebesgue integrable on `(0, ∞)`. So the
  integral in `eq_9_94` is the true integral, not Lean's junk value `0`. The proof uses the formal
  theorem: at `x = 1` or `x = e`, the value `0` would violate it.
* `eq_9_94_integral_eq`, `eq_9_94_coeffs` and `eq_9_94_uniform`: write `A = ∫η₊²` and
  `B = ∫η₊² log t`. Then `∫η₊² log(xt) = A log x + B`, `|A − 0.640206| ≤ 1.95·10⁻⁶` and
  `|B + 0.021095| ≤ 5.3·10⁻⁷`. Hence (9.94) holds for every `x > 0`, with error terms that do not
  depend on `x`. How one reads the range (`x ≥ 10¹²`, `x ≥ 1` or `x > 0`) therefore does not matter.

**Numerical remark (not part of the certification).** We redid the float computation of the repo's
`scripts/eta_plus_check.py` (FFT low-pass in `log t`) without numpy. It gives
`A ≈ 0.6402059974` and `B ≈ −0.0210947787`. So the actual error terms are `E₁ ≈ −2.6·10⁻⁹` and
`E₂ ≈ +2.21·10⁻⁷`, and almost all of `E₂` comes from rounding the constant. The `η∘` integrals
`0.64020599736635` and `−0.021094778698867` were reproduced by Simpson's rule.
-/

open Real Set MeasureTheory

namespace Companion.Book

open TernaryGoldbach.Helfgott (etaPlus)

/-- **[H, (9.94)]** as printed (p. 197): for every real `x ≥ 10¹²`,
`∫₀^∞ η₊²(t) log xt dt = (0.640206 + O*(1.95·10⁻⁶)) log x − 0.021095 + O*(5.3·10⁻⁷)`.

Transcription choices.
* `η₊` is the repository's `TernaryGoldbach.Helfgott.etaPlus`, `η₊(t) = h₂₀₀(t) · t · e^{−t²/2}`.
  We checked it against [H, (7.4)–(7.6)] and against (9.63), "`η(t) = η₊(t) = h_H(t) · t e^{−t²/2}`,
  where `h_H` is as in (7.6)":
  - `hBase` is the `h` of (7.5): `t²(2 − t)³ e^{t−1/2}` on `[0, 2]`, `0` elsewhere;
  - `F H y` is `F_H(y) = sin(H log y)/(π log y)`;
  - `hH H t = ∫_{y>0} h(t/y) F_H(y) dy/y` is the `h_H(t)` of (7.6). (7.6) prints `F_H(t)` and
    `(h *_M F_H)(y)`, typos for `F_H(y)` and `(h *_M F_H)(t)`.

  `H = 200` is fixed inside `etaPlus`, as in §9.6 ("where, as before, `H = 200`", p. 196); the
  bound `274.86/H^{7/2}` just above (9.94) is also evaluated at `H = 200`. At `y = 1`, Lean's
  `F H 1` is `0/0 = 0` rather than the limit `H/π`. This changes the integrand defining `h_H` at
  one point only, so it does not change `h_H`.
* `η₊²(t)` is `etaPlus t ^ 2`. `log xt` is `Real.log (x * t)`, that is `log(xt)`. [H] reads it the
  same way in §9.5: "`η₊,₂ = (log x) η₊,₀ + η₊,₁ = η₊²(t) log xt`" (p. 189), where `η₊,₀ = η₊²` and
  `η₊,₁ = η₊² log t`.
* `∫₀^∞ … dt` is the Lebesgue (Bochner) integral over `Ioi 0`. The integrand is integrable for
  every `x > 0` (`eq_9_94_integrableOn`), so this is the true integral.
* `O*(R)` is "a quantity at most `R` in absolute value" ([H, §2.1]). The two `O*` terms become
  `∃ E₁ E₂, |E₁| ≤ 1.95·10⁻⁶ ∧ |E₂| ≤ 5.3·10⁻⁷ ∧ …`, quantified after `x`. This is the usual
  reading, in which they may depend on `x`; in fact they can be chosen independent of `x`
  (`eq_9_94_uniform`). As printed, `E₁` sits inside the coefficient of `log x`.
* The range: the display states none. The text around it assumes `x ≥ 10¹²` ("We make, again,
  the assumption `x ≥ 10¹²`", p. 197, used again on p. 198). This is the hypothesis of
  [H, Prop 7.1.5], the result being proved there. So `x` is a real number `≥ 10¹²`. The
  derivation itself only needs `log x ≥ 0`. The formal theorem covers `x ≥ 1`, and
  `eq_9_94_uniform` covers every `x > 0`.
* The constants are the printed decimals `0.640206`, `0.021095`, `1.95·10⁻⁶` (`1.95e-6`),
  `5.3·10⁻⁷` (`5.3e-7`) and `10¹²` (`1e12`), taken as exact real numbers.
* The display assumes nothing about the zeros of `ζ` or any other input, so the definition has no
  hypotheses either. -/
def eq_9_94 : Prop :=
  ∀ x : ℝ, 1e12 ≤ x →
    ∃ E₁ E₂ : ℝ, |E₁| ≤ 1.95e-6 ∧ |E₂| ≤ 5.3e-7 ∧
      ∫ t in Ioi 0, etaPlus t ^ 2 * Real.log (x * t) =
        (0.640206 + E₁) * Real.log x - 0.021095 + E₂

/-! ### The pair of `O*` terms as one inequality -/

/-- **`(c + O*(a)) L − d + O*(b)` as one inequality.** Let `L ≥ 0`, `a ≥ 0` and `b > 0`. Then error
terms `E₁`, `E₂` with `|E₁| ≤ a`, `|E₂| ≤ b` and `I = (c + E₁) L − d + E₂` exist if and only if
`|I − (cL − d)| ≤ aL + b`. For the converse direction, take `E₁ = s·a` and `E₂ = s·b`, where
`s = (I − (cL − d))/(aL + b) ∈ [−1, 1]`. -/
theorem eq_9_94_oStar_iff {I c d a b L : ℝ} (hL : 0 ≤ L) (ha : 0 ≤ a) (hb : 0 < b) :
    (∃ E₁ E₂ : ℝ, |E₁| ≤ a ∧ |E₂| ≤ b ∧ I = (c + E₁) * L - d + E₂) ↔
      |I - (c * L - d)| ≤ a * L + b := by
  constructor
  · rintro ⟨E₁, E₂, h₁, h₂, rfl⟩
    calc |(c + E₁) * L - d + E₂ - (c * L - d)| = |E₁ * L + E₂| := by congr 1; ring
      _ ≤ |E₁ * L| + |E₂| := abs_add_le _ _
      _ = |E₁| * L + |E₂| := by rw [abs_mul, abs_of_nonneg hL]
      _ ≤ a * L + b := add_le_add (mul_le_mul_of_nonneg_right h₁ hL) h₂
  · intro h
    have hpos : 0 < a * L + b := by positivity
    have hne : a * L + b ≠ 0 := hpos.ne'
    have hs : |(I - (c * L - d)) / (a * L + b)| ≤ 1 := by
      rw [abs_div, abs_of_pos hpos, div_le_one hpos]; exact h
    refine ⟨(I - (c * L - d)) / (a * L + b) * a, (I - (c * L - d)) / (a * L + b) * b, ?_, ?_, ?_⟩
    · rw [abs_mul, abs_of_nonneg ha]; exact mul_le_of_le_one_left ha hs
    · rw [abs_mul, abs_of_pos hb]; exact mul_le_of_le_one_left hb.le hs
    · field_simp
      ring

/-- **Non-vacuity check.** The existential error terms of `eq_9_94` are a real constraint. Since
`log x ≥ 0` for `x ≥ 10¹²`, the definition is equivalent to the explicit two-sided bound
`|∫₀^∞ η₊²(t) log(xt) dt − (0.640206 log x − 0.021095)| ≤ 1.95·10⁻⁶ log x + 5.3·10⁻⁷`. This is the
shape of the formal theorem. -/
theorem eq_9_94_iff_bound : eq_9_94 ↔ ∀ x : ℝ, 1e12 ≤ x →
    |(∫ t in Ioi 0, etaPlus t ^ 2 * Real.log (x * t)) - (0.640206 * Real.log x - 0.021095)| ≤
      1.95e-6 * Real.log x + 5.3e-7 := by
  unfold eq_9_94
  refine forall_congr' fun x => imp_congr_right fun hx => ?_
  exact eq_9_94_oStar_iff (Real.log_nonneg (by linarith)) (by norm_num) (by norm_num)

/-! ### Relation to the formalization -/

/-- **Formal ⟹ book.** The formalization's `integral_etaPlus_sq_log` implies [H, (9.94)]. It has
[H]'s constants and holds for every `x ≥ 1`, a range that contains [H]'s `x ≥ 10¹²`. The two
statements differ only in how the error is written (`eq_9_94_iff_bound`). This proof does not
use the formal theorem itself, only the hypothesis `h`. -/
theorem eq_9_94_of_formal :
    type_of% @TernaryGoldbach.MajorArcs.integral_etaPlus_sq_log → eq_9_94 := by
  intro h
  rw [eq_9_94_iff_bound]
  intro x hx
  exact h (x := x) (by linarith)

/-- **[H, (9.94)] holds**, as printed, with [H]'s constants and in [H]'s range. This follows from
`TernaryGoldbach.MajorArcs.integral_etaPlus_sq_log`, which has no hypotheses. -/
theorem eq_9_94_holds : eq_9_94 :=
  eq_9_94_of_formal @TernaryGoldbach.MajorArcs.integral_etaPlus_sq_log

/-! ### The integral is genuine, and the error terms can be taken independent of `x` -/

/-- For `x, t > 0`: `η₊²(t) log(xt) = (log x) η₊²(t) + η₊²(t) log t`. -/
theorem eq_9_94_integrand_eq {x t : ℝ} (hx : 0 < x) (ht : 0 < t) :
    etaPlus t ^ 2 * Real.log (x * t) = Real.log x * etaPlus t ^ 2 + etaPlus t ^ 2 * Real.log t := by
  rw [Real.log_mul hx.ne' ht.ne']; ring

/-- `η₊² log t` is integrable on `(0, ∞)`. Otherwise its integral would be Lean's junk value `0`,
and the formal theorem at `x = 1` would read `0.021095 ≤ 5.3·10⁻⁷`. -/
theorem eq_9_94_integrableOn_log :
    IntegrableOn (fun t => etaPlus t ^ 2 * Real.log t) (Ioi 0) := by
  by_contra hni
  have h := TernaryGoldbach.MajorArcs.integral_etaPlus_sq_log (x := 1) le_rfl
  simp only [one_mul, Real.log_one] at h
  rw [integral_undef hni] at h
  norm_num at h

/-- `η₊²` is integrable on `(0, ∞)`. At `x = e`, the junk value `0` would violate the formal
theorem (`0.619111 ≤ 2.48·10⁻⁶`). So `η₊² log(et) = η₊² + η₊² log t` is integrable, and hence so
is `η₊²`. -/
theorem eq_9_94_integrableOn_sq :
    IntegrableOn (fun t => etaPlus t ^ 2) (Ioi 0) := by
  have he : IntegrableOn (fun t => etaPlus t ^ 2 * Real.log (Real.exp 1 * t)) (Ioi 0) := by
    by_contra hni
    have h := TernaryGoldbach.MajorArcs.integral_etaPlus_sq_log (x := Real.exp 1)
      (Real.one_le_exp zero_le_one)
    rw [integral_undef hni, Real.log_exp] at h
    norm_num at h
  refine (he.sub eq_9_94_integrableOn_log).congr_fun (fun t ht => ?_) measurableSet_Ioi
  simp only [Pi.sub_apply]
  rw [eq_9_94_integrand_eq (Real.exp_pos 1) ht, Real.log_exp]; ring

/-- **The integral in (9.94) is a true Lebesgue integral.** For every `x > 0` the integrand
`η₊²(t) log(xt)` is integrable on `(0, ∞)`, so the Bochner integral in `eq_9_94` is not the junk
value `0`. -/
theorem eq_9_94_integrableOn {x : ℝ} (hx : 0 < x) :
    IntegrableOn (fun t => etaPlus t ^ 2 * Real.log (x * t)) (Ioi 0) := by
  have h : IntegrableOn (fun t => Real.log x * etaPlus t ^ 2 + etaPlus t ^ 2 * Real.log t)
      (Ioi 0) :=
    (eq_9_94_integrableOn_sq.integrable.const_mul (Real.log x)).add
      eq_9_94_integrableOn_log.integrable
  exact h.congr_fun (fun t ht => (eq_9_94_integrand_eq hx ht).symm) measurableSet_Ioi

/-- `∫₀^∞ η₊²(t) log(xt) dt = A log x + B` for every `x > 0`, where `A = ∫₀^∞ η₊²` and
`B = ∫₀^∞ η₊² log t`. [H] uses the same splitting in §9.5 (`η₊,₂ = (log x) η₊,₀ + η₊,₁`). -/
theorem eq_9_94_integral_eq {x : ℝ} (hx : 0 < x) :
    ∫ t in Ioi 0, etaPlus t ^ 2 * Real.log (x * t) =
      Real.log x * (∫ t in Ioi 0, etaPlus t ^ 2) + ∫ t in Ioi 0, etaPlus t ^ 2 * Real.log t := by
  have e : ∫ t in Ioi 0, etaPlus t ^ 2 * Real.log (x * t) =
      ∫ t in Ioi 0, (Real.log x * etaPlus t ^ 2 + etaPlus t ^ 2 * Real.log t) :=
    setIntegral_congr_fun measurableSet_Ioi fun t ht => eq_9_94_integrand_eq hx ht
  rw [e, integral_add (eq_9_94_integrableOn_sq.integrable.const_mul _)
    eq_9_94_integrableOn_log.integrable, integral_const_mul]

/-- **The two coefficients of (9.94).** `∫₀^∞ η₊² = 0.640206 + O*(1.95·10⁻⁶)` and
`∫₀^∞ η₊² log t = −0.021095 + O*(5.3·10⁻⁷)`. Both follow from the formal theorem at `x = e^L` for
all `L ≥ 0`. The second is its case `L = 0`. The first follows by letting `L → ∞`: if
`|A − 0.640206| > 1.95·10⁻⁶`, the bound fails at
`L = 2·5.3·10⁻⁷/(|A − 0.640206| − 1.95·10⁻⁶) + 1`. -/
theorem eq_9_94_coeffs :
    |(∫ t in Ioi 0, etaPlus t ^ 2) - 0.640206| ≤ 1.95e-6 ∧
      |(∫ t in Ioi 0, etaPlus t ^ 2 * Real.log t) + 0.021095| ≤ 5.3e-7 := by
  set A := ∫ t in Ioi 0, etaPlus t ^ 2
  set B := ∫ t in Ioi 0, etaPlus t ^ 2 * Real.log t
  have key : ∀ L : ℝ, 0 ≤ L →
      |(A - 0.640206) * L + (B + 0.021095)| ≤ 1.95e-6 * L + 5.3e-7 := by
    intro L hL
    have h := TernaryGoldbach.MajorArcs.integral_etaPlus_sq_log (x := Real.exp L)
      (Real.one_le_exp hL)
    rw [eq_9_94_integral_eq (Real.exp_pos L), Real.log_exp] at h
    convert h using 2; ring
  have hB : |B + 0.021095| ≤ 5.3e-7 := by simpa using key 0 le_rfl
  refine ⟨?_, hB⟩
  by_contra hlt
  rw [not_le] at hlt
  have hδ : 0 < |A - 0.640206| - 1.95e-6 := by linarith
  set L := 2 * 5.3e-7 / (|A - 0.640206| - 1.95e-6) + 1 with hLdef
  have hL : 0 ≤ L := by positivity
  have h1 := key L hL
  have h2 : |A - 0.640206| * L ≤ |(A - 0.640206) * L + (B + 0.021095)| + |B + 0.021095| := by
    calc |A - 0.640206| * L = |(A - 0.640206) * L + (B + 0.021095) + -(B + 0.021095)| := by
          rw [add_neg_cancel_right, abs_mul, abs_of_nonneg hL]
      _ ≤ |(A - 0.640206) * L + (B + 0.021095)| + |-(B + 0.021095)| := abs_add_le _ _
      _ = _ := by rw [abs_neg]
  have h3 : (|A - 0.640206| - 1.95e-6) * L = 2 * 5.3e-7 + (|A - 0.640206| - 1.95e-6) := by
    rw [hLdef]; field_simp
  nlinarith

/-- **(9.94) in its strongest reading.** There are numbers `E₁`, `E₂` with `|E₁| ≤ 1.95·10⁻⁶` and
`|E₂| ≤ 5.3·10⁻⁷` (namely `E₁ = ∫η₊² − 0.640206` and `E₂ = ∫η₊² log t + 0.021095`) such that,
for every `x > 0`,
`∫₀^∞ η₊²(t) log(xt) dt = (0.640206 + E₁) log x − 0.021095 + E₂`. So the error terms do not
depend on `x`, and the range `x ≥ 10¹²` of `eq_9_94` can be widened to all `x > 0`. -/
theorem eq_9_94_uniform :
    ∃ E₁ E₂ : ℝ, |E₁| ≤ 1.95e-6 ∧ |E₂| ≤ 5.3e-7 ∧ ∀ x : ℝ, 0 < x →
      ∫ t in Ioi 0, etaPlus t ^ 2 * Real.log (x * t) =
        (0.640206 + E₁) * Real.log x - 0.021095 + E₂ := by
  obtain ⟨hA, hB⟩ := eq_9_94_coeffs
  refine ⟨_, _, hA, hB, fun x hx => ?_⟩
  rw [eq_9_94_integral_eq hx]; ring

end Companion.Book
