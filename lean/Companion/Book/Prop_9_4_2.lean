import TernaryGoldbach

/-!
# [H, Proposition 9.4.2]: the explicit formula for `η₊`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §9.4,
Proposition 9.4.2 (label `prop:unease`), p. 187 (<https://arxiv.org/pdf/1501.05438v2#page=197>).
Let `η = η₊` be as in (9.63), `η₊(t) = h_H(t) · t e^{-t²/2}` with `h_H` as in (7.6), for some
`H ≥ 25`. Let `x ≥ 10³`, `δ ∈ ℝ`, and let `χ` be a primitive character mod `q ≥ 1`. Assume that
every non-trivial zero `ρ` of `L(s, χ)` with `|Im ρ| ≤ T₀` lies on the critical line, where
`T₀ ≥ H + max(10π|δ|, 50)`. Then (9.69)

`Σ_{n ≥ 1} Λ(n) χ(n) e(δn/x) η₊(n/x) = [q = 1] · η̂₊(−δ) x + O*(err_{η₊,χ}(δ, x)) · x`,

where, with `T₀' = T₀ − H`, (9.70) reads

`err_{η₊,χ}(δ, x) = (11.308 √T₀' e^{−0.1598 T₀'} + 16.147 |δ| e^{−0.1065 (T₀'/(πδ))²}) log(qT₀/2π)`
`                + (1.634 √T₀ log qT₀ + 12.43 √T₀ + 1.321 log q + 34.51) x^{1/2}`
`                + (9 + 11|δ|) x^{−1} + (log q)(11 + 6|δ|) x^{−3/2}`.

**A misprint in (9.70), and what it does to the statement.** The second line of (9.70) is printed
with `x^{1/2}`, both in the LaTeX source and in the arXiv PDF. It should be `x^{−1/2}`, for three
reasons. The 2013 preprint (arXiv:1305.2897v4, Prop. 4.11) has `x^{−1/2}`. The proof bounds the
zeros with `|Im ρ| ≤ T₀` by `(…) x^{1/2}` *before* the division by `x` that turns the error into
`err · x`. And §9.6, where [H] uses (9.70), writes the term with `1/√x`. As printed, `err · x` is
at least `34.51 x^{3/2}`. The trivial bound `|Σ| ≤ Σ Λ(n) |η₊(n/x)| ≪ x log x` is far smaller, so
the printed proposition holds with no hypothesis on the zeros at all. We transcribe the statement
as printed (`prop_9_4_2`). We also state the intended version (`prop_9_4_2_corrected`, with
`x^{−1/2}`), which is a genuine explicit formula. The misprint is a typo: §9.6 only uses the
corrected bound.

**What the formalization proves.** `TernaryGoldbach.MajorArcs.prop_9_4_2`
(`MajorArcs/Prop942.lean:76`) has the same sum, the same main term, the same zero hypothesis
`GRHUpTo χ T₀` and the same condition `T₀ ≥ 200 + max(10π|δ|, 50)`. It is stated only for
`H = 200` (the repository's `etaPlus`), but for every `x ≥ 1`. Its error term is its own
`err942N q T₀ δ x`. It carries no `Fact` binders. `prop_9_4_2_formal_iff_shape` certifies, by
`Iff.rfl` against `type_of%`, that the Lean theorem is exactly `ExplicitFormulaBound 200 1 err942N`.
`prop_9_4_2_iff_shape` shows that [H]'s statement is
`∀ H ≥ 25, ExplicitFormulaBound H 10³ (err_H)`.

**Relation, as certified here: proved (printed statement), but only because of the misprint.**
* `prop_9_4_2_holds : prop_9_4_2`: the printed statement holds for every `H ≥ 25`. It is proved
  here without the zero hypothesis and without any `Fact`, by the trivial bound, and not from the
  formal theorem. The ingredients are:
  - `|h_H| ≤ 4` for `H ≥ 25`, from `TernaryGoldbach.Helfgott.abs_hH_le_eps`;
  - `Λ(n) ≤ log n`;
  - the geometric series `Σ n e^{−n/2x}`;
  - `|η̂₊(−δ)| ≤ |η₊|₁ ≤ 16`.

  They give `|Σ − main| ≤ 53.6 x^{3/2}`, while `err · x ≥ (34.51 + 12.43 √T₀) x^{3/2} ≥ 141.4 x^{3/2}`.
* `prop_9_4_2_of_corrected : prop_9_4_2_corrected → prop_9_4_2`. The corrected statement is
  stronger. It is not proved, here or in the repository, for any `H`.
* The formal theorem and the printed statement are incomparable.
  - [H] covers every `H ≥ 25`, Lean only `H = 200`.
  - Lean covers `1 ≤ x < 10³`, [H] does not.
  - At `H = 200` the two error terms cross. Take `q = 1`, `T₀ = 250`, `δ = 0`. At `x = 10³`,
    `err942N ≈ 9.1·10⁵` exceeds the printed `err ≈ 1.18·10⁴`
    (`Prop_9_4_2.errBook_lt_err942N_at_1e3`). At `x = 10²⁷`, `err942N ≈ 479.6` is below the printed
    `err ≈ 1.18·10¹⁶` (`Prop_9_4_2.err942N_lt_errBook_at_1e27`).

  So neither error term is pointwise below the other on `x ≥ 10³` (`prop_9_4_2_err_incomparable`),
  and `Prop_9_4_2.ExplicitFormulaBound.mono` cannot carry either statement to the other.
* Against the corrected (9.70), the formal theorem is the weaker one at `H = 200`, at every point
  we checked. At the same `q = 1`, `T₀ = 250`, `δ = 0`, the corrected `err` is `≈ 11.9` at
  `x = 10³` and `≈ 0.0998` at `x = 10²⁷`, against `9.1·10⁵` and `479.6` for `err942N`. These two
  comparisons are certified (`Prop_9_4_2.errBookCorr_lt_err942N_at_1e3`,
  `Prop_9_4_2.errBookCorr_lt_err942N_at_1e27`). We also sampled 20000 random parameter points in
  double precision (`q ≤ 10⁶`, `|δ| ≤ 10⁷`, `T₀` up to `10⁴` times its minimum, `10³ ≤ x ≤ 10⁶⁰`).
  There `err942N / err_corrected ≥ 9.39`; this sampling is not certified. The repository derives
  [H, Thm 7.1.4] from its own `err942N` (`MajorArcs/Thm714.lean`), not from [H]'s constants.
-/

open Real MeasureTheory FourierTransform Set
open scoped ArithmeticFunction.vonMangoldt

namespace Companion.Book

open TernaryGoldbach (Schar e)
open TernaryGoldbach.Helfgott (hH etaPlus hBase)
open TernaryGoldbach.MajorArcs (GRHUpTo)

namespace Prop_9_4_2

/-! ## The book's objects -/

/-- [H]'s smoothing (9.63) for a general band limit `H`:
`η_{+,H}(t) = h_H(t) · t · e^{−t²/2}`. Here `h_H` is the repository's
`TernaryGoldbach.Helfgott.hH H`, `h_H(t) = ∫_{y>0} h(t/y) F_H(y) dy/y`. It uses `h = hBase` of (7.5)
and `F_H(y) = sin(H log y)/(π log y)` of (7.6), as in [H]. (7.6) writes `F_H(t)` and
`(h *_M F_H)(y)`, typos for `F_H(y)` and `(h *_M F_H)(t)`; we read `h_H` as a function of `t`. At
`y = 1`, Lean's `F_H` takes the value `0/0 = 0`; this single point does not change the integral.
The repository's `etaPlus` is the case `H = 200` (`etaPlusH_200`). -/
noncomputable def etaPlusH (H t : ℝ) : ℝ := hH H t * t * Real.exp (-t ^ 2 / 2)

/-- At `H = 200`, `η_{+,H}` is the repository's `etaPlus`, definitionally. -/
theorem etaPlusH_200 : etaPlusH 200 = etaPlus := rfl

/-- `h_H(t) = 0` for `t ≤ 0`: the integrand `h(t/y)` vanishes for `y > 0`. -/
theorem hH_of_nonpos (H : ℝ) {t : ℝ} (ht : t ≤ 0) : hH H t = 0 := by
  unfold hH
  refine setIntegral_eq_zero_of_forall_eq_zero fun y (hy : 0 < y) => ?_
  have h0 : hBase (t / y) = 0 := by
    rcases ht.lt_or_eq with ht | ht
    · have : t / y < 0 := div_neg_of_neg_of_pos ht hy
      unfold hBase
      split_ifs with hm
      · exact absurd hm.1 (not_le.2 this)
      · rfl
    · subst ht; simp [hBase]
  rw [h0, zero_mul, zero_div]

/-- `η_{+,H}(t) = 0` for `t ≤ 0`. [H]'s `η₊ : [0, ∞) → ℝ` is therefore extended by zero, which is
how its Fourier transform `η̂₊` is meant. -/
theorem etaPlusH_of_nonpos (H : ℝ) {t : ℝ} (ht : t ≤ 0) : etaPlusH H t = 0 := by
  rw [etaPlusH, hH_of_nonpos H ht, zero_mul, zero_mul]

/-- [H]'s error term `err_{η₊,χ}(δ, x)` of (9.70), **as printed**, with `T₀' = T₀ − H`. The second
line carries the printed `x^{1/2}`. -/
noncomputable def errBook (H : ℝ) (q : ℕ) (T₀ δ x : ℝ) : ℝ :=
  (11.308 * √(T₀ - H) * Real.exp (-0.1598 * (T₀ - H)) +
      16.147 * |δ| * Real.exp (-0.1065 * ((T₀ - H) / (π * δ)) ^ 2)) * Real.log (q * T₀ / (2 * π)) +
    (1.634 * √T₀ * Real.log (q * T₀) + 12.43 * √T₀ + 1.321 * Real.log q + 34.51) * x ^ (1 / 2 : ℝ) +
    (9 + 11 * |δ|) * x ^ (-1 : ℝ) + Real.log q * (11 + 6 * |δ|) * x ^ (-3 / 2 : ℝ)

/-- [H]'s error term (9.70) with the misprint corrected: `x^{−1/2}` in the second line, as in the
2013 preprint and in [H, §9.6]. -/
noncomputable def errBookCorr (H : ℝ) (q : ℕ) (T₀ δ x : ℝ) : ℝ :=
  (11.308 * √(T₀ - H) * Real.exp (-0.1598 * (T₀ - H)) +
      16.147 * |δ| * Real.exp (-0.1065 * ((T₀ - H) / (π * δ)) ^ 2)) * Real.log (q * T₀ / (2 * π)) +
    (1.634 * √T₀ * Real.log (q * T₀) + 12.43 * √T₀ + 1.321 * Real.log q + 34.51) * x ^ (-1 / 2 : ℝ) +
    (9 + 11 * |δ|) * x ^ (-1 : ℝ) + Real.log q * (11 + 6 * |δ|) * x ^ (-3 / 2 : ℝ)

/-- `O*(R) · x` with `x > 0` is `‖S − M‖ ≤ R · x`: `S = M + E · x` for some complex `E` with
`|E| ≤ R` if and only if `‖S − M‖ ≤ R x`. This justifies the norm form used in `prop_9_4_2`. -/
theorem ostar_iff {S M : ℂ} {R x : ℝ} (hx : 0 < x) :
    (∃ E : ℂ, ‖E‖ ≤ R ∧ S = M + E * x) ↔ ‖S - M‖ ≤ R * x := by
  constructor
  · rintro ⟨E, hE, rfl⟩
    rw [add_sub_cancel_left, norm_mul, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hx]
    exact mul_le_mul_of_nonneg_right hE hx.le
  · intro h
    refine ⟨(S - M) / x, ?_, ?_⟩
    · rw [norm_div, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hx, div_le_iff₀ hx]
      exact h
    · have hx' : (x : ℂ) ≠ 0 := Complex.ofReal_ne_zero.2 hx.ne'
      field_simp
      ring

/-- The common shape of [H, Prop 9.4.2] and of the formal theorem, with smoothing `η_{+,H}`, range
`x ≥ x₀` and error term `E(q, T₀, δ, x)`. For every `x ≥ x₀`, `δ`, primitive `χ` mod `q ≥ 1` and
`T₀ ≥ H + max(10π|δ|, 50)` with GRH up to `T₀`, it requires
`|Σ Λ(n) χ(n) e(δn/x) η_{+,H}(n/x) − [q = 1] η̂_{+,H}(−δ) x| ≤ E(q, T₀, δ, x) · x`. -/
def ExplicitFormulaBound (H x₀ : ℝ) (E : ℕ → ℝ → ℝ → ℝ → ℝ) : Prop :=
  ∀ x : ℝ, x₀ ≤ x → ∀ δ : ℝ,
  ∀ (q : ℕ) [NeZero q] (χ : DirichletCharacter ℂ q), χ.IsPrimitive →
  ∀ T₀ : ℝ, H + max (10 * π * |δ|) 50 ≤ T₀ → GRHUpTo χ T₀ →
    ‖Schar χ (fun n => ((Λ n * etaPlusH H (n / x) : ℝ) : ℂ)) (δ / x) -
        (if q = 1 then 𝓕 (fun u => (etaPlusH H u : ℂ)) (-δ) * x else 0)‖ ≤ E q T₀ δ x * x

end Prop_9_4_2

open Prop_9_4_2

/-- **[H, Proposition 9.4.2]**, as printed (p. 187, (9.69)–(9.70)).

How the statement is transcribed:
* "Let `η = η₊` be as in (9.63) for some `H ≥ 25`" becomes `∀ H : ℝ, 25 ≤ H → …`, with `η₊` the
  book's `η_{+,H} = Prop_9_4_2.etaPlusH H`. The proposition is claimed for each such `H`. The
  repository's `etaPlus` fixes `H = 200`, so it cannot be reused directly. `etaPlusH` reuses the
  repository's `hH`, which agrees with (7.5)–(7.6).
* "`x ≥ 10³`, `δ ∈ ℝ`" becomes `∀ x : ℝ, 1e3 ≤ x → ∀ δ : ℝ, …`.
* "`χ` a primitive character mod `q`, `q ≥ 1`" becomes
  `∀ (q : ℕ) [NeZero q] (χ : DirichletCharacter ℂ q), χ.IsPrimitive → …`. For `q : ℕ`,
  `NeZero q` means `q ≥ 1`. Mathlib's `IsPrimitive` means that the conductor equals `q`.
* "all non-trivial zeros `ρ` of `L(s, χ)` with `|Im ρ| ≤ T₀` lie on the critical line" becomes the
  repository's `TernaryGoldbach.MajorArcs.GRHUpTo χ T₀`. This says that every zero of Mathlib's
  `χ.LFunction` with `0 < Re ρ < 1` and `|Im ρ| ≤ T₀` has `Re ρ = 1/2`. For primitive `χ` these are
  exactly the non-trivial zeros: there are no zeros on `Re s = 1`, and on `Re s = 0` only the
  trivial zero `s = 0` of an even `χ ≠ 1`. For `q = 1`, `χ.LFunction = ζ`.
* "where `T₀ ≥ H + max(10π|δ|, 50)`" becomes `∀ T₀ : ℝ, H + max (10 * π * |δ|) 50 ≤ T₀ → …`. `T₀`
  is quantified universally, since the error term depends on it.
* `Σ_{n=1}^∞ Λ(n) χ(n) e(δn/x) η₊(n/x)` becomes the repository's
  `Schar χ (fun n => Λ n * η(n/x)) (δ/x) = Σ' n, Λ(n) η(n/x) χ(n) e(n · δ/x)`. The `n = 0` term
  vanishes since `Λ 0 = 0`. The series converges absolutely (see
  `Prop_9_4_2.norm_Schar_etaPlusH_le`), so the `tsum` is the series.
* `η̂₊(−δ)` becomes Mathlib's Fourier transform `𝓕 (fun u => (η u : ℂ)) (−δ)`, which is
  `∫ e^{−2πiuw} f(u) du`. This is [H]'s normalization `f̂(t) = ∫ e(−xt) f(x) dx` of §2.1, applied
  to `η₊` extended by `0` to `t < 0` (`Prop_9_4_2.etaPlusH_of_nonpos`).
* The two cases `q = 1` and `q > 1` become the main term `if q = 1 then η̂₊(−δ) · x else 0`.
* `O*(err) · x` becomes `‖Σ − main‖ ≤ err · x`, which is the same thing since `x > 0`
  (`Prop_9_4_2.ostar_iff`).
* `err_{η₊,χ}(δ, x)` is `Prop_9_4_2.errBook H q T₀ δ x`, (9.70) verbatim. The constants are copied
  as printed. `log` is the natural logarithm, `log qT₀ = log(q T₀)` and `log(qT₀/2π) = log(q T₀/(2π))`.
  `√` is `Real.sqrt`, and `x^{1/2}`, `x^{−1}`, `x^{−3/2}` are real powers. At `δ = 0`, [H]'s
  `16.147 |δ| e^{−0.1065 (T₀'/(πδ))²}` is a `0 · e^{−∞}` limit with value `0`. Lean's
  `T₀'/(π · 0) = 0` gives `16.147 · 0 · e⁰ = 0`, the same value. The stray commas at the ends of the
  lines of (9.70) are ignored.
* The second line of (9.70) keeps the printed `x^{1/2}` (see the module docstring). The intended
  `x^{−1/2}` is `prop_9_4_2_corrected`. -/
def prop_9_4_2 : Prop :=
  ∀ H : ℝ, 25 ≤ H → ∀ x : ℝ, 1e3 ≤ x → ∀ δ : ℝ,
  ∀ (q : ℕ) [NeZero q] (χ : DirichletCharacter ℂ q), χ.IsPrimitive →
  ∀ T₀ : ℝ, H + max (10 * π * |δ|) 50 ≤ T₀ → GRHUpTo χ T₀ →
    ‖Schar χ (fun n => ((Λ n * etaPlusH H (n / x) : ℝ) : ℂ)) (δ / x) -
        (if q = 1 then 𝓕 (fun u => (etaPlusH H u : ℂ)) (-δ) * x else 0)‖ ≤
      errBook H q T₀ δ x * x

/-- [H, Proposition 9.4.2] with the misprint in (9.70) corrected (`x^{−1/2}` in the second line),
as in arXiv:1305.2897v4, Prop. 4.11 and as used in [H, §9.6]. Everything else is as in
`prop_9_4_2`. -/
def prop_9_4_2_corrected : Prop :=
  ∀ H : ℝ, 25 ≤ H → ∀ x : ℝ, 1e3 ≤ x → ∀ δ : ℝ,
  ∀ (q : ℕ) [NeZero q] (χ : DirichletCharacter ℂ q), χ.IsPrimitive →
  ∀ T₀ : ℝ, H + max (10 * π * |δ|) 50 ≤ T₀ → GRHUpTo χ T₀ →
    ‖Schar χ (fun n => ((Λ n * etaPlusH H (n / x) : ℝ) : ℂ)) (δ / x) -
        (if q = 1 then 𝓕 (fun u => (etaPlusH H u : ℂ)) (-δ) * x else 0)‖ ≤
      errBookCorr H q T₀ δ x * x

namespace Prop_9_4_2

/-! ## The trivial bound -/

/-- `|h_H(t)| ≤ 4` for `H ≥ 25`, `t ≥ 0`. This is `TernaryGoldbach.Helfgott.abs_hH_le_eps` with
`ε = 1/H`: `|h_H(t)| ≤ 5/(πH) + (6/π) e^{1/2} ≤ 3.25`. -/
theorem abs_hH_le_four {H : ℝ} (hH25 : 25 ≤ H) {t : ℝ} (ht : 0 ≤ t) : |hH H t| ≤ 4 := by
  rcases ht.eq_or_lt with h0 | ht
  · rw [← h0, hH_of_nonpos H le_rfl, abs_zero]; norm_num
  have hH0 : 0 < H := by linarith
  have h := TernaryGoldbach.Helfgott.abs_hH_le_eps (H := H) (ε := 1 / H) hH0 ht (by positivity)
    (by rw [div_le_one hH0]; linarith)
  have hπ : 3.1415 < π := Real.pi_gt_d4
  have he : Real.exp (1 / 2) < 1.64873 := by
    have h := Real.exp_one_lt_d9
    have hsq : Real.exp (1 / 2) ^ 2 = Real.exp 1 := by rw [← Real.exp_nat_mul]; norm_num
    nlinarith [Real.exp_pos (1 / 2)]
  have h1 : 5 * H * (1 / H) ^ 2 / π ≤ 0.1 := by
    rw [div_le_iff₀ (by linarith)]
    have : 5 * H * (1 / H) ^ 2 = 5 / H := by field_simp
    rw [this, div_le_iff₀ hH0]; nlinarith
  have h2 : 6 / π * Real.exp (1 / 2) ≤ 3.149 := by
    rw [div_mul_eq_mul_div, div_le_iff₀ (by linarith)]; nlinarith
  linarith

/-- `|η_{+,H}(t)| ≤ 4 |t| e^{−t²/2}` for `H ≥ 25` and all real `t`. -/
theorem abs_etaPlusH_le {H : ℝ} (hH25 : 25 ≤ H) (t : ℝ) :
    |etaPlusH H t| ≤ 4 * |t| * Real.exp (-t ^ 2 / 2) := by
  rcases le_or_gt t 0 with ht | ht
  · rw [etaPlusH_of_nonpos H ht, abs_zero]; positivity
  unfold etaPlusH
  rw [abs_mul, abs_mul, abs_of_pos (Real.exp_pos _)]
  have := abs_hH_le_four hH25 ht.le
  gcongr

/-- `|u| e^{−u²/2} ≤ e^{−u²/4}`, since `|u| ≤ 1 + u²/4 ≤ e^{u²/4}`. -/
theorem abs_mul_exp_le (u : ℝ) : |u| * Real.exp (-u ^ 2 / 2) ≤ Real.exp (-(1 / 4) * u ^ 2) := by
  have h1 : |u| ≤ Real.exp (u ^ 2 / 4) := by
    have := Real.add_one_le_exp (u ^ 2 / 4)
    have hsq : |u| ^ 2 = u ^ 2 := sq_abs u
    nlinarith [sq_nonneg (|u| - 2), abs_nonneg u]
  have e1 : Real.exp (-(1 / 4) * u ^ 2) = Real.exp (u ^ 2 / 4) * Real.exp (-u ^ 2 / 2) := by
    rw [← Real.exp_add]; ring_nf
  rw [e1]
  exact mul_le_mul_of_nonneg_right h1 (Real.exp_pos _).le

/-- `|η_{+,H}|₁ ≤ 4 ∫ e^{−u²/4} du = 8√π ≤ 16` for `H ≥ 25`. -/
theorem integral_abs_etaPlusH_le {H : ℝ} (hH25 : 25 ≤ H) :
    ∫ u, ‖((etaPlusH H u : ℝ) : ℂ)‖ ≤ 16 := by
  have hint : Integrable (fun u : ℝ => 4 * Real.exp (-(1 / 4) * u ^ 2)) :=
    (integrable_exp_neg_mul_sq (by norm_num : (0:ℝ) < 1 / 4)).const_mul 4
  have h := integral_mono_of_nonneg (μ := volume) (f := fun u => ‖((etaPlusH H u : ℝ) : ℂ)‖)
    (Filter.Eventually.of_forall fun u => norm_nonneg _) hint
    (Filter.Eventually.of_forall fun u => by
      simp only [Complex.norm_real, Real.norm_eq_abs]
      calc |etaPlusH H u| ≤ 4 * |u| * Real.exp (-u ^ 2 / 2) := abs_etaPlusH_le hH25 u
        _ = 4 * (|u| * Real.exp (-u ^ 2 / 2)) := by ring
        _ ≤ 4 * Real.exp (-(1 / 4) * u ^ 2) := by gcongr; exact abs_mul_exp_le u)
  refine h.trans ?_
  rw [MeasureTheory.integral_const_mul, integral_gaussian]
  have : π / (1 / 4) ≤ 16 := by rw [div_le_iff₀ (by norm_num)]; linarith [Real.pi_lt_d2]
  have hs : √(π / (1 / 4)) ≤ 4 := by
    rw [Real.sqrt_le_left (by norm_num)]; linarith
  linarith

/-- `Λ(n) · t e^{−t²/2} ≤ e^{1/2} (log x + 1) · t e^{−t/2}` at `t = n/x`, `x ≥ 1`. It uses
`Λ(n) ≤ log n = log x + log t ≤ log x + t`, `e^{−t²/2} ≤ e^{1/2} e^{−t}` and `t e^{−t/2} ≤ 2/e`. -/
theorem vonMangoldt_mul_le {x : ℝ} (hx : 1 ≤ x) (n : ℕ) :
    Λ n * ((n / x) * Real.exp (-(n / x) ^ 2 / 2)) ≤
      Real.exp (1 / 2) * (Real.log x + 1) * ((n / x) * Real.exp (-(n / x) / 2)) := by
  have hx0 : 0 < x := by linarith
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · simp
  set t : ℝ := n / x with ht_def
  have hn' : (0:ℝ) < n := by exact_mod_cast hn
  have ht : 0 < t := div_pos hn' hx0
  set L := Real.log x with hL
  have hL0 : 0 ≤ L := Real.log_nonneg hx
  have hΛ0 : 0 ≤ Λ n := ArithmeticFunction.vonMangoldt_nonneg
  have hΛ : Λ n ≤ L + t := by
    have h1 : Λ n ≤ Real.log n := ArithmeticFunction.vonMangoldt_le_log
    have h2 : (n : ℝ) = x * t := by rw [ht_def]; field_simp
    have h3 : Real.log n = L + Real.log t := by rw [h2, Real.log_mul hx0.ne' ht.ne']
    have h4 : Real.log t ≤ t - 1 := Real.log_le_sub_one_of_pos ht
    linarith
  set a := Real.exp (-t / 2) with ha
  have ha0 : 0 < a := Real.exp_pos _
  have ha1 : a ≤ 1 := by rw [ha]; exact Real.exp_le_one_iff.2 (by linarith)
  have hta : t * a ≤ 1 := by
    have h1 := Real.add_one_le_exp (t / 2 - 1)
    have h2 : Real.exp (t / 2 - 1) = Real.exp (t / 2) * Real.exp (-1) := by
      rw [← Real.exp_add]; ring_nf
    have h3 : Real.exp (t / 2) * a = 1 := by rw [ha, ← Real.exp_add]; ring_nf; exact Real.exp_zero
    have h4 : Real.exp (-1) ≤ 1 / 2 := by
      rw [Real.exp_neg, inv_le_comm₀ (Real.exp_pos 1) (by norm_num)]
      linarith [Real.exp_one_gt_d9]
    have h5 : 0 < Real.exp (t / 2) := Real.exp_pos _
    nlinarith
  have hg : Real.exp (-t ^ 2 / 2) ≤ Real.exp (1 / 2) * a ^ 2 := by
    rw [ha, ← Real.exp_nat_mul, ← Real.exp_add]
    exact Real.exp_le_exp.2 (by push_cast; nlinarith [sq_nonneg (t - 1)])
  have he0 : 0 < Real.exp (1 / 2) := Real.exp_pos _
  have hg0 : 0 ≤ Real.exp (-t ^ 2 / 2) := (Real.exp_pos _).le
  calc Λ n * (t * Real.exp (-t ^ 2 / 2)) ≤ (L + t) * (t * (Real.exp (1 / 2) * a ^ 2)) := by
        gcongr
    _ = Real.exp (1 / 2) * (t * a) * (L * a + t * a) := by ring
    _ ≤ Real.exp (1 / 2) * (t * a) * (L + 1) := by
        gcongr
        · nlinarith
    _ = Real.exp (1 / 2) * (L + 1) * (t * a) := by ring

/-- `1 − e^{−1/(2x)} ≥ 1/(2x + 1)` for `x > 0`. -/
theorem one_sub_exp_ge {x : ℝ} (hx : 0 < x) :
    1 / (2 * x + 1) ≤ 1 - Real.exp (-(1 / (2 * x))) := by
  have hu : 0 < 1 / (2 * x) := by positivity
  have h1 : 1 + 1 / (2 * x) ≤ Real.exp (1 / (2 * x)) := by
    linarith [Real.add_one_le_exp (1 / (2 * x))]
  have h2 : Real.exp (-(1 / (2 * x))) ≤ (1 + 1 / (2 * x))⁻¹ := by
    rw [Real.exp_neg]; exact inv_anti₀ (by positivity) h1
  have h3 : (1 + 1 / (2 * x))⁻¹ = 2 * x / (2 * x + 1) := by field_simp
  have h4 : 1 / (2 * x + 1) + 2 * x / (2 * x + 1) = 1 := by field_simp; ring
  linarith

/-- **The trivial bound.** For `H ≥ 25` and `x ≥ 1`,
`‖Σ_n Λ(n) η_{+,H}(n/x) χ(n) e(nδ/x)‖ ≤ 4 e^{1/2} (log x + 1) (2x + 1)²/x`. The series is absolutely
summable, with majorant `4 e^{1/2} (log x + 1) x⁻¹ · n e^{−n/(2x)}`, which is summed in closed form. -/
theorem norm_Schar_etaPlusH_le {H : ℝ} (hH25 : 25 ≤ H) {x : ℝ} (hx : 1 ≤ x) {q : ℕ}
    (χ : DirichletCharacter ℂ q) (δ : ℝ) :
    ‖Schar χ (fun n => ((Λ n * etaPlusH H (n / x) : ℝ) : ℂ)) (δ / x)‖ ≤
      4 * Real.exp (1 / 2) * (Real.log x + 1) * (2 * x + 1) ^ 2 / x := by
  have hx0 : 0 < x := by linarith
  set s := Real.exp (-(1 / (2 * x))) with hs
  have hs0 : 0 < s := Real.exp_pos _
  have hs1 : s < 1 := Real.exp_lt_one_iff.2 (by simp only [neg_lt_zero]; positivity)
  have hM : HasSum (fun n : ℕ => (n : ℝ) * s ^ n) (s / (1 - s) ^ 2) :=
    hasSum_coe_mul_geometric_of_norm_lt_one (by rw [Real.norm_eq_abs, abs_of_pos hs0]; exact hs1)
  set C := 4 * Real.exp (1 / 2) * (Real.log x + 1) / x with hC
  have hC0 : 0 ≤ C := by
    have := Real.log_nonneg hx
    positivity
  set f : ℕ → ℂ := fun n => ((Λ n * etaPlusH H (n / x) : ℝ) : ℂ) * χ (n : ZMod q) *
    e (n * (δ / x)) with hf
  have hbound : ∀ n : ℕ, ‖f n‖ ≤ C * ((n : ℝ) * s ^ n) := by
    intro n
    have hn0 : (0:ℝ) ≤ n / x := by positivity
    have h1 : ‖f n‖ ≤ |Λ n * etaPlusH H (n / x)| := by
      simp only [hf]
      rw [norm_mul, norm_mul, TernaryGoldbach.norm_e, mul_one, Complex.norm_real, Real.norm_eq_abs]
      exact mul_le_of_le_one_right (abs_nonneg _) (DirichletCharacter.norm_le_one χ _)
    have h2 : |Λ n * etaPlusH H (n / x)| ≤ Λ n * (4 * ((n / x) * Real.exp (-(n / x) ^ 2 / 2))) := by
      rw [abs_mul, abs_of_nonneg ArithmeticFunction.vonMangoldt_nonneg]
      refine mul_le_mul_of_nonneg_left ?_ ArithmeticFunction.vonMangoldt_nonneg
      have := abs_etaPlusH_le hH25 (n / x)
      rw [abs_of_nonneg hn0] at this
      linarith
    have h3 := vonMangoldt_mul_le hx n
    have h4 : (n / x) * Real.exp (-(n / x) / 2) = 1 / x * ((n : ℝ) * s ^ n) := by
      rw [hs, ← Real.exp_nat_mul]
      have : -(n / x) / 2 = (n : ℝ) * -(1 / (2 * x)) := by field_simp
      rw [this]; field_simp
    calc ‖f n‖ ≤ Λ n * (4 * ((n / x) * Real.exp (-(n / x) ^ 2 / 2))) := h1.trans h2
      _ = 4 * (Λ n * ((n / x) * Real.exp (-(n / x) ^ 2 / 2))) := by ring
      _ ≤ 4 * (Real.exp (1 / 2) * (Real.log x + 1) * ((n / x) * Real.exp (-(n / x) / 2))) := by
          gcongr
      _ = C * ((n : ℝ) * s ^ n) := by rw [h4, hC]; ring
  have hsum : Summable fun n => ‖f n‖ :=
    Summable.of_nonneg_of_le (fun n => norm_nonneg _) hbound (hM.summable.mul_left C)
  have hS : Schar χ (fun n => ((Λ n * etaPlusH H (n / x) : ℝ) : ℂ)) (δ / x) = ∑' n, f n := rfl
  rw [hS]
  refine (norm_tsum_le_tsum_norm hsum).trans ?_
  refine (hsum.tsum_le_tsum hbound (hM.summable.mul_left C)).trans ?_
  rw [tsum_mul_left, hM.tsum_eq]
  have h1s : 1 / (2 * x + 1) ≤ 1 - s := one_sub_exp_ge hx0
  have h1s0 : 0 < 1 - s := by linarith
  have key : s / (1 - s) ^ 2 ≤ (2 * x + 1) ^ 2 := by
    rw [div_le_iff₀ (by positivity)]
    have h5 : 1 ≤ (2 * x + 1) * (1 - s) := by
      rw [div_le_iff₀ (by positivity)] at h1s; linarith
    have h6 : 1 ≤ ((2 * x + 1) * (1 - s)) ^ 2 := by nlinarith
    nlinarith
  calc C * (s / (1 - s) ^ 2) ≤ C * (2 * x + 1) ^ 2 := mul_le_mul_of_nonneg_left key hC0
    _ = 4 * Real.exp (1 / 2) * (Real.log x + 1) * (2 * x + 1) ^ 2 / x := by rw [hC]; ring

/-- The printed error term is at least `(34.51 + 12.43 √T₀) √x` once `T₀ ≥ 75`. Every term of
(9.70) is nonnegative, because `q ≥ 1` and `qT₀/2π ≥ 1`. -/
theorem errBook_ge (H : ℝ) {q : ℕ} [NeZero q] {T₀ : ℝ} (δ : ℝ) {x : ℝ} (hT : 75 ≤ T₀) (hx : 0 < x) :
    (34.51 + 12.43 * √T₀) * √x ≤ errBook H q T₀ δ x := by
  have hq : (1:ℝ) ≤ q := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr (NeZero.ne q)
  have hlogq : 0 ≤ Real.log q := Real.log_nonneg hq
  have hlogqT : 0 ≤ Real.log (q * T₀) := Real.log_nonneg (by nlinarith)
  have hlog2π : 0 ≤ Real.log (q * T₀ / (2 * π)) :=
    Real.log_nonneg (by rw [le_div_iff₀ (by positivity)]; nlinarith [Real.pi_lt_d2])
  have hsx : x ^ (1 / 2 : ℝ) = √x := (Real.sqrt_eq_rpow x).symm
  unfold errBook
  rw [hsx]
  have h1 : 0 ≤ (11.308 * √(T₀ - H) * Real.exp (-0.1598 * (T₀ - H)) +
      16.147 * |δ| * Real.exp (-0.1065 * ((T₀ - H) / (π * δ)) ^ 2)) *
        Real.log (q * T₀ / (2 * π)) := mul_nonneg (by positivity) hlog2π
  have h3 : 0 ≤ (9 + 11 * |δ|) * x ^ (-1 : ℝ) := by positivity
  have h4 : 0 ≤ Real.log q * (11 + 6 * |δ|) * x ^ (-3 / 2 : ℝ) :=
    mul_nonneg (mul_nonneg hlogq (by positivity)) (by positivity)
  have h5 : 0 ≤ 1.634 * √T₀ * Real.log (q * T₀) := mul_nonneg (by positivity) hlogqT
  have h2 : (34.51 + 12.43 * √T₀) * √x ≤
      (1.634 * √T₀ * Real.log (q * T₀) + 12.43 * √T₀ + 1.321 * Real.log q + 34.51) * √x := by
    apply mul_le_mul_of_nonneg_right _ (Real.sqrt_nonneg x)
    nlinarith
  linarith

/-- The numerical comparison behind `prop_9_4_2_holds`. For `x ≥ 10³` and `T₀ ≥ 75`, the trivial
bound plus the main term, `4e^{1/2}(log x + 1)(2x+1)²/x + 16x ≤ 53.6 x^{3/2}`, is at most
`(34.51 + 12.43√T₀) √x · x`. -/
theorem trivial_numeric {x T₀ : ℝ} (hx : 1e3 ≤ x) (hT : 75 ≤ T₀) :
    4 * Real.exp (1 / 2) * (Real.log x + 1) * (2 * x + 1) ^ 2 / x + 16 * x ≤
      (34.51 + 12.43 * √T₀) * √x * x := by
  have hx0 : 0 < x := by linarith
  set r := √x with hr
  have hr0 : 0 < r := Real.sqrt_pos.2 hx0
  have hrr : r * r = x := Real.mul_self_sqrt hx0.le
  have hr31 : 31.6 ≤ r := Real.le_sqrt_of_sq_le (by nlinarith)
  have hT86 : 8.6 ≤ √T₀ := Real.le_sqrt_of_sq_le (by nlinarith)
  have hlog : Real.log x ≤ 2 * r - 2 := by
    have h1 : Real.log r = Real.log x / 2 := Real.log_sqrt hx0.le
    have h2 : Real.log r ≤ r - 1 := Real.log_le_sub_one_of_pos hr0
    linarith
  have hlog0 : 0 ≤ Real.log x := Real.log_nonneg (by linarith)
  have he : Real.exp (1 / 2) ≤ 1.64873 := by
    have h := Real.exp_one_lt_d9
    have hsq : Real.exp (1 / 2) ^ 2 = Real.exp 1 := by rw [← Real.exp_nat_mul]; norm_num
    nlinarith [Real.exp_pos (1 / 2)]
  have hA : (2 * x + 1) ^ 2 / x ≤ 4.01 * x := by
    rw [div_le_iff₀ hx0]; nlinarith
  have hA0 : 0 ≤ (2 * x + 1) ^ 2 / x := by positivity
  have hE0 : 0 ≤ Real.exp (1 / 2) := (Real.exp_pos _).le
  have e1 : 4 * Real.exp (1 / 2) * (Real.log x + 1) * (2 * x + 1) ^ 2 / x =
      4 * Real.exp (1 / 2) * (Real.log x + 1) * ((2 * x + 1) ^ 2 / x) := by ring
  rw [e1]
  have h1 : 4 * Real.exp (1 / 2) * (Real.log x + 1) * ((2 * x + 1) ^ 2 / x) ≤
      4 * 1.64873 * (2 * r - 1) * (4.01 * x) := by
    gcongr
    · nlinarith
    · linarith
  have h2 : 4 * 1.64873 * (2 * r - 1) * (4.01 * x) + 16 * x ≤ (34.51 + 12.43 * 8.6) * r * x := by
    nlinarith
  have h3 : (34.51 + 12.43 * 8.6) * r * x ≤ (34.51 + 12.43 * √T₀) * r * x := by
    gcongr
  linarith

/-- The corrected error term is at most the printed one, since `x^{−1/2} ≤ x^{1/2}` for `x ≥ 1`. -/
theorem errBookCorr_le_errBook (H : ℝ) {q : ℕ} [NeZero q] {T₀ : ℝ} (δ : ℝ) {x : ℝ} (hT : 75 ≤ T₀)
    (hx : 1 ≤ x) : errBookCorr H q T₀ δ x ≤ errBook H q T₀ δ x := by
  have hq : (1:ℝ) ≤ q := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr (NeZero.ne q)
  have hlogq : 0 ≤ Real.log q := Real.log_nonneg hq
  have hlogqT : 0 ≤ Real.log (q * T₀) := Real.log_nonneg (by nlinarith)
  have hL : 0 ≤ 1.634 * √T₀ * Real.log (q * T₀) + 12.43 * √T₀ + 1.321 * Real.log q + 34.51 := by
    have := mul_nonneg (mul_nonneg (by norm_num : (0:ℝ) ≤ 1.634) (Real.sqrt_nonneg T₀)) hlogqT
    have := Real.sqrt_nonneg T₀
    nlinarith
  have hrp : x ^ (-1 / 2 : ℝ) ≤ x ^ (1 / 2 : ℝ) := Real.rpow_le_rpow_of_exponent_le hx (by norm_num)
  unfold errBookCorr errBook
  have := mul_le_mul_of_nonneg_left hrp hL
  linarith

end Prop_9_4_2

/-- **[H, Proposition 9.4.2] holds as printed**, for every `H ≥ 25`. The proof is the trivial bound
`|Σ − [q = 1] η̂₊(−δ) x| ≤ |Σ| + |η₊|₁ x ≤ 53.6 x^{3/2}`, against the printed
`err · x ≥ 141.4 x^{3/2}`. It never uses the zero hypothesis, the primitivity of `χ` or any `Fact`,
and it does not use `TernaryGoldbach.MajorArcs.prop_9_4_2`. This is possible only because of the
misprint `x^{1/2}` in (9.70). The intended statement is `prop_9_4_2_corrected`, which is not proved
here. -/
theorem prop_9_4_2_holds : prop_9_4_2 := by
  intro H hH x hx δ q _ χ _ T₀ hT₀ _
  have hx1 : 1 ≤ x := by linarith
  have hx0 : 0 < x := by linarith
  have hT75 : 75 ≤ T₀ := by have := le_max_right (10 * π * |δ|) 50; linarith
  have hmain : ‖(if q = 1 then 𝓕 (fun u => (etaPlusH H u : ℂ)) (-δ) * x else 0)‖ ≤ 16 * x := by
    split_ifs
    · rw [norm_mul, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hx0]
      exact mul_le_mul_of_nonneg_right
        ((Real.norm_fourier_le_integral_norm _ _).trans (integral_abs_etaPlusH_le hH)) hx0.le
    · rw [norm_zero]; positivity
  have hS := norm_Schar_etaPlusH_le hH hx1 χ δ
  have herr := errBook_ge (q := q) H δ hT75 hx0
  calc _ ≤ ‖Schar χ (fun n => ((Λ n * etaPlusH H (n / x) : ℝ) : ℂ)) (δ / x)‖ +
        ‖(if q = 1 then 𝓕 (fun u => (etaPlusH H u : ℂ)) (-δ) * x else 0)‖ := norm_sub_le _ _
    _ ≤ 4 * Real.exp (1 / 2) * (Real.log x + 1) * (2 * x + 1) ^ 2 / x + 16 * x := add_le_add hS hmain
    _ ≤ (34.51 + 12.43 * √T₀) * √x * x := trivial_numeric hx hT75
    _ ≤ errBook H q T₀ δ x * x := mul_le_mul_of_nonneg_right herr hx0.le

/-- The corrected statement implies the printed one. -/
theorem prop_9_4_2_of_corrected : prop_9_4_2_corrected → prop_9_4_2 := by
  intro h H hH x hx δ q _ χ hχ T₀ hT hG
  have hT75 : 75 ≤ T₀ := by have := le_max_right (10 * π * |δ|) 50; linarith
  have hx0 : (0:ℝ) ≤ x := by linarith
  exact (h H hH x hx δ q χ hχ T₀ hT hG).trans
    (mul_le_mul_of_nonneg_right (errBookCorr_le_errBook (q := q) H δ hT75 (by linarith)) hx0)

/-- **Non-vacuity.** The hypotheses of `prop_9_4_2` can all hold at once. Take `H = 200`,
`x = 10³`, `δ = 0`, `q = 1`, `χ = 1` and `T₀ = 250`. GRH up to height `250` for `L(s, 1) = ζ(s)`
follows from the repository's hypothesis `PlattGRH` (via `rh_upto_1e8`, RH up to `10⁸`). -/
theorem prop_9_4_2_hyps_satisfiable [Fact TernaryGoldbach.PlattGRH] :
    ∃ (H x δ T₀ : ℝ) (χ : DirichletCharacter ℂ 1), 25 ≤ H ∧ 1e3 ≤ x ∧ χ.IsPrimitive ∧
      H + max (10 * π * |δ|) 50 ≤ T₀ ∧ GRHUpTo χ T₀ := by
  refine ⟨200, 1e3, 0, 250, 1, by norm_num, le_rfl, DirichletCharacter.isPrimitive_one_level_one,
    ?_, ?_⟩
  · rw [abs_zero, mul_zero, max_eq_right (by norm_num : (0:ℝ) ≤ 50)]; norm_num
  · intro ρ h0 h1 h2 h3
    have hRH : TernaryGoldbach.Explicit.RHBelow 1e8 := TernaryGoldbach.Explicit.rh_upto_1e8
    exact hRH ρ (by rwa [DirichletCharacter.LFunction_modOne_eq] at h0) h1 h2 (by linarith)

/-! ## Relation to the formal theorem -/

/-- [H]'s printed statement is `ExplicitFormulaBound H 10³ (errBook H)` for every `H ≥ 25`. -/
theorem prop_9_4_2_iff_shape :
    prop_9_4_2 ↔ ∀ H : ℝ, 25 ≤ H → ExplicitFormulaBound H 1e3 (errBook H) := Iff.rfl

/-- The corrected statement is `ExplicitFormulaBound H 10³ (errBookCorr H)` for every `H ≥ 25`. -/
theorem prop_9_4_2_corrected_iff_shape :
    prop_9_4_2_corrected ↔ ∀ H : ℝ, 25 ≤ H → ExplicitFormulaBound H 1e3 (errBookCorr H) := Iff.rfl

/-- **The formal theorem has [H]'s shape at `H = 200`.**
`TernaryGoldbach.MajorArcs.prop_9_4_2` is, definitionally, `ExplicitFormulaBound 200 1 err942N`.
So it has the same sum, main term, zero hypothesis and condition on `T₀` as [H] at `H = 200`, the
range `x ≥ 1`, and its own error term `err942N`.
Certified by `Iff.rfl` against `type_of%`. -/
theorem prop_9_4_2_formal_iff_shape :
    type_of% @TernaryGoldbach.MajorArcs.prop_9_4_2 ↔
      ExplicitFormulaBound 200 1 TernaryGoldbach.MajorArcs.err942N := Iff.rfl

namespace Prop_9_4_2

/-- An `ExplicitFormulaBound` transfers to a smaller range and a larger error term. This is the
only route between [H]'s statement and the formal one at `H = 200`, and the witnesses below show
that it is blocked in both directions. -/
theorem ExplicitFormulaBound.mono {H x₀ x₁ : ℝ} {E E' : ℕ → ℝ → ℝ → ℝ → ℝ} (hx : x₀ ≤ x₁)
    (hx₁ : 0 ≤ x₁)
    (hE : ∀ (q : ℕ) (T₀ δ x : ℝ), x₁ ≤ x → H + max (10 * π * |δ|) 50 ≤ T₀ → E q T₀ δ x ≤ E' q T₀ δ x)
    (h : ExplicitFormulaBound H x₀ E) : ExplicitFormulaBound H x₁ E' := by
  intro x hx' δ q _ χ hχ T₀ hT hG
  exact (h x (hx.trans hx') δ q χ hχ T₀ hT hG).trans
    (mul_le_mul_of_nonneg_right (hE q T₀ δ x hx' hT) (hx₁.trans hx'))

/-! ### Numerical witnesses at `H = 200`, `q = 1`, `T₀ = 250`, `δ = 0` -/

open TernaryGoldbach.Explicit (Cg aH Z3g ZLg E1g E2g c3g BPz2 EB EA rhoB rhoA VgL thP thetaD Jl)

/-- `e^{1/2} ≤ 1.64873`. -/
theorem exp_half_le : Real.exp (1 / 2) ≤ 1.64873 := by
  have h := Real.exp_one_lt_d9
  have hsq : Real.exp (1 / 2) ^ 2 = Real.exp 1 := by rw [← Real.exp_nat_mul]; norm_num
  nlinarith [Real.exp_pos (1 / 2)]

/-- `C_g ≥ 2`, from `C_g = 92 e^{−1/2} − 12 e^{3/2}` (`TernaryGoldbach.Explicit.Cg_eq`). -/
theorem Cg_ge_two : 2 ≤ Cg := by
  rw [TernaryGoldbach.Explicit.Cg_eq]
  have h1 := exp_half_le
  have h0 := Real.exp_pos (1 / 2)
  have hm : Real.exp (-(1 / 2)) * Real.exp (1 / 2) = 1 := by
    rw [← Real.exp_add]; norm_num
  have hm' : 0.6065 ≤ Real.exp (-(1 / 2)) := by nlinarith [Real.exp_pos (-(1 / 2))]
  have h32 : Real.exp (3 / 2) = Real.exp 1 * Real.exp (1 / 2) := by rw [← Real.exp_add]; norm_num
  have he := Real.exp_one_lt_d9
  have h32' : Real.exp (3 / 2) ≤ 4.4818 := by rw [h32]; nlinarith [Real.exp_pos 1]
  linarith

/-- `θ'₀ = min(0.28, 1/200) = 1/200`. -/
theorem thP_zero : thP 0 = 1 / 200 := by
  unfold thP thetaD; norm_num

/-- `log(10/r) ≥ 1` for `0 < r ≤ 3.6`. -/
theorem log_ten_div_ge {r : ℝ} (hr0 : 0 < r) (hr : r ≤ 3.6) : 1 ≤ Real.log (10 / r) := by
  rw [Real.le_log_iff_exp_le (by positivity)]
  have := Real.exp_one_lt_d9
  rw [le_div_iff₀ hr0]; nlinarith

/-- `ρ_B = e^{−0.1398·4.4} ≤ 0.62`. -/
theorem rhoB_le : rhoB ≤ 0.62 := by
  unfold TernaryGoldbach.Explicit.rhoB
  have h := Real.add_one_le_exp (0.1398 * 4.4)
  rw [Real.exp_neg]
  have h0 : 0 < Real.exp (0.1398 * 4.4) := Real.exp_pos _
  rw [inv_le_comm₀ h0 (by norm_num)]
  linarith

/-- **Witness 1** (`x = 10³`). At `H = 200`, `q = 1`, `T₀ = 250`, `δ = 0`, `x = 10³`, the printed
bound of [H] is below the formalization's: `err ≤ 1.6·10⁴` (in fact `≈ 1.18·10⁴`), while
`err942N ≥ 5·10⁵` (in fact `≈ 9.1·10⁵`, from the term `V/(2π x^{3/2})` of the line `Re s = −1/2`).
So the formal theorem does not give [H]'s printed bound at this point. -/
theorem errBook_lt_err942N_at_1e3 :
    errBook 200 1 250 0 1000 < TernaryGoldbach.MajorArcs.err942N 1 250 0 1000 := by
  -- upper bound on the printed error term
  have hπ1 := Real.pi_gt_d4
  have hπ2 := Real.pi_lt_d4
  have hs50 : √((250:ℝ) - 200) ≤ 7.1 := by rw [Real.sqrt_le_left (by norm_num)]; norm_num
  have hs250 : √(250:ℝ) ≤ 15.82 := by rw [Real.sqrt_le_left (by norm_num)]; norm_num
  have hs1000 : (1000:ℝ) ^ (1 / 2 : ℝ) ≤ 31.63 := by
    rw [← Real.sqrt_eq_rpow, Real.sqrt_le_left (by norm_num)]; norm_num
  have hexp : Real.exp (-0.1598 * ((250:ℝ) - 200)) ≤ 1 := Real.exp_le_one_iff.2 (by norm_num)
  have hl1 : Real.log ((1:ℕ) * (250:ℝ) / (2 * π)) ≤ 40 := by
    have hpos : (0:ℝ) < (1:ℕ) * 250 / (2 * π) := by positivity
    have := Real.log_le_sub_one_of_pos hpos
    have h2 : ((1:ℕ) : ℝ) * 250 / (2 * π) ≤ 41 := by
      rw [div_le_iff₀ (by positivity)]; push_cast; nlinarith
    linarith
  have hl1' : 0 ≤ Real.log ((1:ℕ) * (250:ℝ) / (2 * π)) :=
    Real.log_nonneg (by rw [le_div_iff₀ (by positivity)]; push_cast; nlinarith)
  have hl2 : Real.log ((1:ℕ) * (250:ℝ)) ≤ 6 := by
    rw [Real.log_le_iff_le_exp (by norm_num)]
    have h6 : Real.exp 6 = Real.exp 1 ^ 6 := by rw [← Real.exp_nat_mul]; norm_num
    rw [h6]
    have := Real.exp_one_gt_d9
    calc ((1:ℕ) : ℝ) * 250 ≤ (2.7182818283 : ℝ) ^ 6 := by norm_num
      _ ≤ Real.exp 1 ^ 6 := pow_le_pow_left₀ (by norm_num) this.le 6
  have hbook : errBook 200 1 250 0 1000 ≤ 16000 := by
    unfold errBook
    simp only [abs_zero, mul_zero, zero_mul, add_zero, Nat.cast_one, Real.log_one]
    simp only [Nat.cast_one] at hl1 hl2 hl1'
    have h1 : 11.308 * √((250:ℝ) - 200) * Real.exp (-0.1598 * ((250:ℝ) - 200)) ≤ 11.308 * 7.1 := by
      have := Real.sqrt_nonneg ((250:ℝ) - 200)
      have := Real.exp_pos (-0.1598 * ((250:ℝ) - 200))
      nlinarith
    have h1' : 0 ≤ 11.308 * √((250:ℝ) - 200) * Real.exp (-0.1598 * ((250:ℝ) - 200)) := by positivity
    have h2 : 1.634 * √(250:ℝ) * Real.log (1 * 250) ≤ 1.634 * 15.82 * 6 := by
      have hl0 : 0 ≤ Real.log (1 * (250:ℝ)) := Real.log_nonneg (by norm_num)
      have := mul_le_mul hs250 hl2 hl0 (by norm_num)
      nlinarith
    have hx1 : (1000:ℝ) ^ (-1 : ℝ) ≤ 1 := Real.rpow_le_one_of_one_le_of_nonpos (by norm_num) (by norm_num)
    have hx0 : 0 ≤ (1000:ℝ) ^ (1 / 2 : ℝ) := by positivity
    have h3 : 0 ≤ 1.634 * √(250:ℝ) * Real.log (1 * 250) :=
      mul_nonneg (by positivity) (Real.log_nonneg (by norm_num))
    nlinarith
  -- lower bound on the formalization's error term
  have hlow : 500000 ≤ TernaryGoldbach.MajorArcs.err942N 1 250 0 1000 := by
    unfold TernaryGoldbach.MajorArcs.err942N TernaryGoldbach.MajorArcs.errPZ
    rw [ite_eq_left rfl]
    have hCg := Cg_ge_two
    have haH := TernaryGoldbach.Explicit.aH_pos
    have hA : 0 ≤ Cg * 300 * (2 * aH) * Z3g BPz2 0 / 1000 := by
      have := TernaryGoldbach.Explicit.Z3z_nonneg
      positivity
    have hB : 0 ≤ E1g BPz2 250 (2 * π * 0.6403) (2 * π * 1.129) / √1000 := by
      unfold E1g ZLg
      have := (TernaryGoldbach.Explicit.polyDatum_zeta2.log_pos (250 + 3.48)).le
      have := (TernaryGoldbach.Explicit.log_ratio_pos (r := 2.3) (by norm_num) (by norm_num)).le
      positivity
    have hC : 0 ≤ E2g BPz2 10 250 (Cg * (2 * aH) * EB (250 - 200)) (Cg * (2 * aH) * EA (250 - 200) 0)
        rhoB (rhoA 0) := by
      have hEA : EA (250 - 200) 0 = 0 := by unfold EA; simp
      unfold E2g
      rw [hEA, mul_zero, zero_mul, add_zero]
      have hZ : 0 ≤ Z3g BPz2 250 := by
        unfold Z3g
        have := (TernaryGoldbach.Explicit.polyDatum_zeta2.log_pos 250).le
        have := (TernaryGoldbach.Explicit.log_ratio_pos (r := 3) (by norm_num) (by norm_num)).le
        positivity
      have hc : 0 ≤ c3g 10 250 := by
        unfold c3g
        have := (TernaryGoldbach.Explicit.log_ratio_pos (r := 3) (by norm_num) (by norm_num)).le
        positivity
      have hρ : 0 < 1 - rhoB := by linarith [TernaryGoldbach.Explicit.rhoB_lt_one]
      have hEB : 0 ≤ EB (250 - 200) := by unfold EB; positivity
      positivity
    have hD : 500000 ≤ VgL 3 (Cg * (300 * Real.exp 1) * (2 * aH)) (thP 0) /
        (2 * π * (1000 * √1000)) := by
      rw [thP_zero]
      unfold VgL
      have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
      have he := Real.exp_one_gt_d9
      have h2aH : 63.66 ≤ 2 * aH := by
        unfold TernaryGoldbach.Explicit.aH
        rw [show 2 * (200 / (2 * π)) = 200 / π by field_simp, le_div_iff₀ (by positivity)]
        nlinarith
      have hKv : 100000 ≤ Cg * (300 * Real.exp 1) * (2 * aH) := by
        have h1 : 2 * (300 * 2.7182818283) ≤ Cg * (300 * Real.exp 1) :=
          mul_le_mul hCg (by linarith) (by norm_num) (by linarith)
        have h2 : (2 * (300 * 2.7182818283)) * 63.66 ≤ Cg * (300 * Real.exp 1) * (2 * aH) :=
          mul_le_mul h1 h2aH (by norm_num) (by positivity)
        linarith
      have hs : √(1000:ℝ) ≤ 31.63 := by rw [Real.sqrt_le_left (by norm_num)]; norm_num
      have hden : 2 * π * (1000 * √1000) ≤ 200000 := by
        have := Real.sqrt_nonneg (1000:ℝ)
        nlinarith
      have hden0 : 0 < 2 * π * (1000 * √(1000:ℝ)) := by positivity
      rw [le_div_iff₀ hden0]
      have hbr : 4.8 * ((3 + 37) * (2 / (1 / 200)) + 2.6 * (2 / (1 / 200) ^ 2)) ≤
          (2 / Real.log 2 + 4.8) * ((3 + 37) * (2 / (1 / 200)) + 2.6 * (2 / (1 / 200) ^ 2)) := by
        have : 0 ≤ 2 / Real.log 2 := by positivity
        have : (0:ℝ) ≤ (3 + 37) * (2 / (1 / 200)) + 2.6 * (2 / (1 / 200) ^ 2) := by norm_num
        nlinarith
      have hval : (4.8:ℝ) * ((3 + 37) * (2 / (1 / 200)) + 2.6 * (2 / (1 / 200) ^ 2)) = 1075200 := by
        norm_num
      have hbr0 : 0 ≤ (2 / Real.log 2 + 4.8) * ((3 + 37) * (2 / (1 / 200)) + 2.6 * (2 / (1 / 200) ^ 2)) := by
        positivity
      calc 500000 * (2 * π * (1000 * √1000)) ≤ 500000 * 200000 := by nlinarith
        _ ≤ 100000 * 1075200 := by norm_num
        _ ≤ Cg * (300 * Real.exp 1) * (2 * aH) *
            ((2 / Real.log 2 + 4.8) * ((3 + 37) * (2 / (1 / 200)) + 2.6 * (2 / (1 / 200) ^ 2))) := by
            rw [← hval]
            exact mul_le_mul hKv hbr (by norm_num) (by linarith)
        _ = _ := by ring
    exact le_trans hD (le_add_of_nonneg_left (add_nonneg (add_nonneg hA hB) hC))
  linarith

/-- **Witness 1′** (`x = 10³`, corrected reading). The corrected bound is below the formalization's
too. -/
theorem errBookCorr_lt_err942N_at_1e3 :
    errBookCorr 200 1 250 0 1000 < TernaryGoldbach.MajorArcs.err942N 1 250 0 1000 :=
  (errBookCorr_le_errBook (q := 1) 200 0 (by norm_num) (by norm_num)).trans_lt
    errBook_lt_err942N_at_1e3

/-- **Witness 2** (`x = 10²⁷`). At `H = 200`, `q = 1`, `T₀ = 250`, `δ = 0`, `x = 10²⁷`, the
formalization's bound is below the printed bound of [H]: `err942N ≤ 3·10⁷` (in fact `≈ 479.6`,
from the zeros above `T₀`), while the printed `err ≥ 34.51 √x ≥ 10¹⁵`. So [H]'s printed statement
does not give the formal bound at this point. -/
theorem err942N_lt_errBook_at_1e27 :
    TernaryGoldbach.MajorArcs.err942N 1 250 0 1e27 < errBook 200 1 250 0 1e27 := by
  have hπ1 := Real.pi_gt_d4
  have hπ2 := Real.pi_lt_d4
  have hsx : (3e13 : ℝ) ≤ √(1e27 : ℝ) := Real.le_sqrt_of_sq_le (by norm_num)
  -- the printed bound is at least `34.51 √x ≥ 10¹⁵`
  have hbook : (1e15 : ℝ) ≤ errBook 200 1 250 0 1e27 := by
    have h := errBook_ge (q := 1) 200 0 (by norm_num : (75:ℝ) ≤ 250) (by norm_num : (0:ℝ) < 1e27)
    have h1 : 0 ≤ 12.43 * √(250:ℝ) * √(1e27 : ℝ) := by positivity
    nlinarith
  -- the formal bound is at most `3·10⁷`
  have hlow : TernaryGoldbach.MajorArcs.err942N 1 250 0 1e27 ≤ 3e7 := by
    unfold TernaryGoldbach.MajorArcs.err942N TernaryGoldbach.MajorArcs.errPZ
    rw [ite_eq_left rfl]
    have hcA := TernaryGoldbach.Explicit.cA_le
    have hcA0 := TernaryGoldbach.Explicit.cA_nonneg
    have hCg0 := TernaryGoldbach.Explicit.Cg_nonneg
    have haH := TernaryGoldbach.Explicit.aH_pos
    have hl3 : 1 ≤ Real.log (10 / 3) := log_ten_div_ge (by norm_num) (by norm_num)
    have hl23 : 1 ≤ Real.log (10 / 2.3) := log_ten_div_ge (by norm_num) (by norm_num)
    have hZ0 : Z3g BPz2 0 ≤ 37 := by
      unfold Z3g
      have h := TernaryGoldbach.Explicit.log_BPz2_lin 0
      have h0 := (TernaryGoldbach.Explicit.polyDatum_zeta2.log_pos 0).le
      rw [div_le_iff₀ (by linarith)]
      simp only [abs_zero, mul_zero, add_zero, zero_add] at h
      nlinarith
    have hZ0' : 0 ≤ Z3g BPz2 0 := TernaryGoldbach.Explicit.Z3z_nonneg
    have hZ250 : Z3g BPz2 250 ≤ 687 := by
      unfold Z3g
      have h := TernaryGoldbach.Explicit.log_BPz2_lin 250
      rw [abs_of_pos (by norm_num : (0:ℝ) < 250)] at h
      rw [div_le_iff₀ (by linarith)]
      nlinarith
    have hZ250' : 0 ≤ Z3g BPz2 250 := by
      unfold Z3g
      have := (TernaryGoldbach.Explicit.polyDatum_zeta2.log_pos 250).le
      positivity
    have hZL : ZLg BPz2 250 ≤ 700 := by
      unfold ZLg
      have h := TernaryGoldbach.Explicit.log_BPz2_lin (250 + 3.48)
      rw [abs_of_pos (by norm_num : (0:ℝ) < 250 + 3.48)] at h
      rw [div_le_iff₀ (by linarith)]
      nlinarith
    have hZL' : 0 ≤ ZLg BPz2 250 := by
      unfold ZLg
      have := (TernaryGoldbach.Explicit.polyDatum_zeta2.log_pos (250 + 3.48)).le
      positivity
    -- `A / x ≤ 1`
    have hA : Cg * 300 * (2 * aH) * Z3g BPz2 0 / 1e27 ≤ 1 := by
      rw [div_le_iff₀ (by norm_num)]
      have : Cg * 300 * (2 * aH) * Z3g BPz2 0 = 300 * (Cg * (2 * aH)) * Z3g BPz2 0 := by ring
      rw [this]
      have := mul_le_mul hcA hZ0 hZ0' (by norm_num)
      nlinarith
    -- `B / √x ≤ 1`
    have hJ : (Jl 250 : ℝ) * 3.48 ≤ 253.48 := by
      unfold Jl
      push_cast
      have := Nat.floor_le (show (0:ℝ) ≤ 250 / 3.48 by norm_num)
      have e : (250:ℝ) / 3.48 * 3.48 = 250 := by norm_num
      nlinarith
    have hJ0 : (0:ℝ) ≤ (Jl 250 : ℝ) * 3.48 := by positivity
    have hB : E1g BPz2 250 (2 * π * 0.6403) (2 * π * 1.129) / √(1e27 : ℝ) ≤ 1 := by
      unfold E1g
      have h1 : √(2 * π * 0.6403 * (2 * ((Jl 250 : ℝ) * 3.48))) ≤ 46 := by
        rw [Real.sqrt_le_left (by norm_num)]; nlinarith
      have h2 : √(2 * π * 1.129 * (2 * ((Jl 250 : ℝ) * 3.48))) ≤ 61 := by
        rw [Real.sqrt_le_left (by norm_num)]; nlinarith
      have h1' := Real.sqrt_nonneg (2 * π * 0.6403 * (2 * ((Jl 250 : ℝ) * 3.48)))
      have h2' := Real.sqrt_nonneg (2 * π * 1.129 * (2 * ((Jl 250 : ℝ) * 3.48)))
      have hbr : (1 / 3.48) * √(2 * π * 0.6403 * (2 * ((Jl 250 : ℝ) * 3.48))) +
          √(2 * π * 1.129 * (2 * ((Jl 250 : ℝ) * 3.48))) ≤ 75 := by linarith
      have hbr0 : 0 ≤ (1 / 3.48) * √(2 * π * 0.6403 * (2 * ((Jl 250 : ℝ) * 3.48))) +
          √(2 * π * 1.129 * (2 * ((Jl 250 : ℝ) * 3.48))) := by positivity
      rw [div_le_iff₀ (by positivity)]
      have := mul_le_mul hZL hbr hbr0 (by norm_num)
      nlinarith
    -- `C ≤ 2.1·10⁷`
    have hC : E2g BPz2 10 250 (Cg * (2 * aH) * EB (250 - 200)) (Cg * (2 * aH) * EA (250 - 200) 0)
        rhoB (rhoA 0) ≤ 2.1e7 := by
      have hEA : EA (250 - 200) 0 = 0 := by unfold EA; simp
      unfold E2g
      rw [hEA, mul_zero, zero_mul, add_zero]
      have hEB : EB (250 - 200) ≤ 44.6 := by
        unfold EB
        have : Real.exp (-0.1598 * ((250:ℝ) - 200)) ≤ 1 := Real.exp_le_one_iff.2 (by norm_num)
        nlinarith [Real.exp_pos (-0.1598 * ((250:ℝ) - 200))]
      have hEB0 : 0 ≤ EB (250 - 200) := by unfold EB; positivity
      have hc : c3g 10 250 ≤ 0.176 := by
        unfold c3g
        rw [div_le_iff₀ (by linarith)]
        nlinarith
      have hc0 : 0 ≤ c3g 10 250 := by unfold c3g; positivity
      have hρ := rhoB_le
      have hρ0 : 0.38 ≤ 1 - rhoB := by linarith
      have hbr : 2 * Z3g BPz2 250 / (1 - rhoB) + 2 * c3g 10 250 / (1 - rhoB) ^ 2 ≤ 3620 := by
        have h1 : 2 * Z3g BPz2 250 / (1 - rhoB) ≤ 2 * 687 / 0.38 := by
          rw [div_le_div_iff₀ (by linarith) (by norm_num)]; nlinarith
        have h2 : 2 * c3g 10 250 / (1 - rhoB) ^ 2 ≤ 2 * 0.176 / 0.38 ^ 2 := by
          rw [div_le_div_iff₀ (by positivity) (by norm_num)]
          have : (0.38:ℝ) ^ 2 ≤ (1 - rhoB) ^ 2 := pow_le_pow_left₀ (by norm_num) hρ0 2
          nlinarith
        have : (2 * 687 / 0.38 : ℝ) + 2 * 0.176 / 0.38 ^ 2 ≤ 3620 := by norm_num
        linarith
      have hbr0 : 0 ≤ 2 * Z3g BPz2 250 / (1 - rhoB) + 2 * c3g 10 250 / (1 - rhoB) ^ 2 := by
        have : 0 < 1 - rhoB := by linarith
        positivity
      have hEB' : Cg * (2 * aH) * EB (250 - 200) ≤ 129.24 * 44.6 :=
        mul_le_mul hcA hEB hEB0 (by norm_num)
      have := mul_le_mul hEB' hbr hbr0 (by norm_num)
      nlinarith
    -- `D / (2π x √x) ≤ 1`
    have hD : VgL 3 (Cg * (300 * Real.exp 1) * (2 * aH)) (thP 0) / (2 * π * (1e27 * √(1e27 : ℝ))) ≤ 1 := by
      rw [thP_zero]
      unfold VgL
      have he := Real.exp_one_lt_d9
      have hKv : Cg * (300 * Real.exp 1) * (2 * aH) ≤ 105400 := by
        have : Cg * (300 * Real.exp 1) * (2 * aH) = 300 * Real.exp 1 * (Cg * (2 * aH)) := by ring
        rw [this]
        have := mul_le_mul (show 300 * Real.exp 1 ≤ 300 * 2.7182818286 by linarith) hcA hcA0
          (by norm_num)
        linarith
      have hKv0 : 0 ≤ Cg * (300 * Real.exp 1) * (2 * aH) := by
        have := Real.exp_pos 1; positivity
      have hlog2 := Real.log_two_gt_d9
      have hl : 2 / Real.log 2 + 4.8 ≤ 7.8 := by
        rw [← le_sub_iff_add_le, div_le_iff₀ (by linarith)]; nlinarith
      have hl0 : 0 ≤ 2 / Real.log 2 + 4.8 := by
        have : 0 < Real.log 2 := by linarith
        positivity
      have hval : ((3:ℝ) + 37) * (2 / (1 / 200)) + 2.6 * (2 / (1 / 200) ^ 2) = 224000 := by norm_num
      rw [hval]
      have hden : 1e41 ≤ 2 * π * (1e27 * √(1e27 : ℝ)) := by nlinarith
      rw [div_le_iff₀ (by linarith)]
      have := mul_le_mul hKv hl hl0 (by norm_num)
      nlinarith
    have e1 : (250:ℝ) - 200 = 250 - 200 := rfl
    linarith
  linarith

/-- **Witness 3** (`x = 10²⁷`, corrected reading). At `H = 200`, `q = 1`, `T₀ = 250`, `δ = 0`,
`x = 10²⁷`, the corrected bound of [H] is below the formalization's: `err_corrected ≤ 6` (in fact
`≈ 0.0998`), while `err942N ≥ 50` (in fact `≈ 479.6`). -/
theorem errBookCorr_lt_err942N_at_1e27 :
    errBookCorr 200 1 250 0 1e27 < TernaryGoldbach.MajorArcs.err942N 1 250 0 1e27 := by
  have hπ1 := Real.pi_gt_d4
  have hπ2 := Real.pi_lt_d4
  have hsx : (3e13 : ℝ) ≤ √(1e27 : ℝ) := Real.le_sqrt_of_sq_le (by norm_num)
  have he7 : Real.exp (-0.1598 * ((250:ℝ) - 200)) ≤ 0.001 := by
    have h7 : (1000:ℝ) ≤ Real.exp (0.1598 * ((250:ℝ) - 200)) := by
      have h1 : Real.exp 7 ≤ Real.exp (0.1598 * ((250:ℝ) - 200)) := Real.exp_le_exp.2 (by norm_num)
      have h2 : Real.exp 7 = Real.exp 1 ^ 7 := by rw [← Real.exp_nat_mul]; norm_num
      have h3 := Real.exp_one_gt_d9
      have h4 : (2.7182818283 : ℝ) ^ 7 ≤ Real.exp 1 ^ 7 := pow_le_pow_left₀ (by norm_num) h3.le 7
      have h5 : (1000 : ℝ) ≤ 2.7182818283 ^ 7 := by norm_num
      linarith
    have h8 : Real.exp (-0.1598 * ((250:ℝ) - 200)) = (Real.exp (0.1598 * ((250:ℝ) - 200)))⁻¹ := by
      rw [← Real.exp_neg]; ring_nf
    rw [h8, inv_le_comm₀ (by positivity) (by norm_num)]
    linarith
  -- upper bound on the corrected error term: `≤ 6`
  have hcorr : errBookCorr 200 1 250 0 1e27 ≤ 6 := by
    have hs50 : √((250:ℝ) - 200) ≤ 7.1 := by rw [Real.sqrt_le_left (by norm_num)]; norm_num
    have hs250 : √(250:ℝ) ≤ 15.82 := by rw [Real.sqrt_le_left (by norm_num)]; norm_num
    have hl1 : Real.log ((1:ℕ) * (250:ℝ) / (2 * π)) ≤ 40 := by
      have hpos : (0:ℝ) < (1:ℕ) * 250 / (2 * π) := by positivity
      have := Real.log_le_sub_one_of_pos hpos
      have h2 : ((1:ℕ) : ℝ) * 250 / (2 * π) ≤ 41 := by
        rw [div_le_iff₀ (by positivity)]; push_cast; nlinarith
      linarith
    have hl1' : 0 ≤ Real.log ((1:ℕ) * (250:ℝ) / (2 * π)) :=
      Real.log_nonneg (by rw [le_div_iff₀ (by positivity)]; push_cast; nlinarith)
    have hl2 : Real.log ((1:ℕ) * (250:ℝ)) ≤ 6 := by
      rw [Real.log_le_iff_le_exp (by norm_num)]
      have h6 : Real.exp 6 = Real.exp 1 ^ 6 := by rw [← Real.exp_nat_mul]; norm_num
      rw [h6]
      have := Real.exp_one_gt_d9
      calc ((1:ℕ) : ℝ) * 250 ≤ (2.7182818283 : ℝ) ^ 6 := by norm_num
        _ ≤ Real.exp 1 ^ 6 := pow_le_pow_left₀ (by norm_num) this.le 6
    have hxm : (1e27 : ℝ) ^ (-1 / 2 : ℝ) ≤ 1 / 3e13 := by
      rw [show (-1 / 2 : ℝ) = -(1 / 2) by norm_num, Real.rpow_neg (by norm_num), ← Real.sqrt_eq_rpow,
        one_div]
      exact inv_anti₀ (by norm_num) hsx
    have hxm0 : 0 ≤ (1e27 : ℝ) ^ (-1 / 2 : ℝ) := by positivity
    have hx1 : (1e27 : ℝ) ^ (-1 : ℝ) ≤ 1 / 9 := by rw [Real.rpow_neg_one]; norm_num
    have hx10 : 0 ≤ (1e27 : ℝ) ^ (-1 : ℝ) := by positivity
    unfold errBookCorr
    simp only [abs_zero, mul_zero, zero_mul, add_zero, Nat.cast_one, Real.log_one]
    simp only [Nat.cast_one] at hl1 hl2 hl1'
    have h1 : 11.308 * √((250:ℝ) - 200) * Real.exp (-0.1598 * ((250:ℝ) - 200)) ≤ 11.308 * 7.1 * 0.001 := by
      have := Real.sqrt_nonneg ((250:ℝ) - 200)
      have := Real.exp_pos (-0.1598 * ((250:ℝ) - 200))
      have := mul_le_mul hs50 he7 this.le (by norm_num)
      nlinarith
    have h1' : 0 ≤ 11.308 * √((250:ℝ) - 200) * Real.exp (-0.1598 * ((250:ℝ) - 200)) := by positivity
    have hl0 : 0 ≤ Real.log (1 * (250:ℝ)) := Real.log_nonneg (by norm_num)
    have h2 : 1.634 * √(250:ℝ) * Real.log (1 * 250) ≤ 1.634 * 15.82 * 6 := by
      have := mul_le_mul hs250 hl2 hl0 (by norm_num)
      nlinarith
    have h3 : 0 ≤ 1.634 * √(250:ℝ) * Real.log (1 * 250) := mul_nonneg (by positivity) hl0
    have hL : 1.634 * √(250:ℝ) * Real.log (1 * 250) + 12.43 * √250 + 1.321 * 0 + 34.51 ≤ 400 := by
      nlinarith
    have hL0 : 0 ≤ 1.634 * √(250:ℝ) * Real.log (1 * 250) + 12.43 * √250 + 1.321 * 0 + 34.51 := by
      have := Real.sqrt_nonneg (250:ℝ); nlinarith
    have hm := mul_le_mul hL hxm hxm0 (by norm_num)
    have hl1m := mul_le_mul h1 hl1 hl1' (by norm_num)
    nlinarith
  -- lower bound on the formalization's error term: `≥ 50`
  have hlow : 50 ≤ TernaryGoldbach.MajorArcs.err942N 1 250 0 1e27 := by
    unfold TernaryGoldbach.MajorArcs.err942N TernaryGoldbach.MajorArcs.errPZ
    rw [ite_eq_left rfl]
    have hCg := Cg_ge_two
    have haH := TernaryGoldbach.Explicit.aH_pos
    have hA : 0 ≤ Cg * 300 * (2 * aH) * Z3g BPz2 0 / 1e27 := by
      have := TernaryGoldbach.Explicit.Z3z_nonneg
      positivity
    have hB : 0 ≤ E1g BPz2 250 (2 * π * 0.6403) (2 * π * 1.129) / √1e27 := by
      unfold E1g ZLg
      have := (TernaryGoldbach.Explicit.polyDatum_zeta2.log_pos (250 + 3.48)).le
      have := (TernaryGoldbach.Explicit.log_ratio_pos (r := 2.3) (by norm_num) (by norm_num)).le
      positivity
    have hD : 0 ≤ VgL 3 (Cg * (300 * Real.exp 1) * (2 * aH)) (thP 0) / (2 * π * (1e27 * √1e27)) := by
      rw [thP_zero]
      unfold VgL
      have := Real.exp_pos 1
      have : 0 < Real.log 2 := Real.log_pos (by norm_num)
      positivity
    have hC : 50 ≤ E2g BPz2 10 250 (Cg * (2 * aH) * EB (250 - 200)) (Cg * (2 * aH) * EA (250 - 200) 0)
        rhoB (rhoA 0) := by
      have hEA : EA (250 - 200) 0 = 0 := by unfold EA; simp
      unfold E2g
      rw [hEA, mul_zero, zero_mul, add_zero]
      have hρ1 := TernaryGoldbach.Explicit.rhoB_lt_one
      have hρ0 : 0 < rhoB := by unfold TernaryGoldbach.Explicit.rhoB; exact Real.exp_pos _
      have hc : 0 ≤ c3g 10 250 := by
        unfold c3g
        have := (TernaryGoldbach.Explicit.log_ratio_pos (r := 3) (by norm_num) (by norm_num)).le
        positivity
      have hZ : 25 ≤ Z3g BPz2 250 := by
        unfold Z3g
        have hl3 : Real.log (10 / 3) ≤ 7 / 3 := by
          have := Real.log_le_sub_one_of_pos (show (0:ℝ) < 10 / 3 by norm_num); linarith
        have hl3' : 0 < Real.log (10 / 3) := Real.log_pos (by norm_num)
        have hB : 60 ≤ Real.log (BPz2 250 / 0.355) := by
          rw [Real.le_log_iff_exp_le (by unfold BPz2; positivity)]
          have h60 : Real.exp 60 = Real.exp 1 ^ 60 := by rw [← Real.exp_nat_mul]; norm_num
          rw [h60]
          have he := Real.exp_one_lt_d9
          have h1 : Real.exp 1 ^ 60 ≤ (3:ℝ) ^ 60 := pow_le_pow_left₀ (Real.exp_pos 1).le (by linarith) 60
          have h2 : (3:ℝ) ^ 60 ≤ BPz2 250 / 0.355 := by unfold BPz2; norm_num
          linarith
        rw [le_div_iff₀ hl3']
        nlinarith
      have hEB : 0.0149 ≤ EB (250 - 200) := by
        unfold EB
        have h8 : (1:ℝ) / 2981 ≤ Real.exp (-0.1598 * ((250:ℝ) - 200)) := by
          have h1 : Real.exp (-8) ≤ Real.exp (-0.1598 * ((250:ℝ) - 200)) := Real.exp_le_exp.2 (by norm_num)
          have h2 : Real.exp (-8) = (Real.exp 1 ^ 8)⁻¹ := by
            rw [← Real.exp_nat_mul, ← Real.exp_neg]; norm_num
          have he := Real.exp_one_lt_d9
          have h3 : Real.exp 1 ^ 8 ≤ (2.7182818286 : ℝ) ^ 8 := pow_le_pow_left₀ (Real.exp_pos 1).le he.le 8
          have h4 : (2.7182818286 : ℝ) ^ 8 ≤ 2981 := by norm_num
          have h5 : (2981:ℝ)⁻¹ ≤ (Real.exp 1 ^ 8)⁻¹ := inv_anti₀ (by positivity) (h3.trans h4)
          rw [h2] at h1
          rw [one_div]; linarith
        nlinarith
      have h2aH : 63.66 ≤ 2 * aH := by
        unfold TernaryGoldbach.Explicit.aH
        rw [show 2 * (200 / (2 * π)) = 200 / π by field_simp, le_div_iff₀ (by positivity)]
        nlinarith
      have hEB' : 2 * 63.66 * 0.0149 ≤ Cg * (2 * aH) * EB (250 - 200) := by
        have := mul_le_mul hCg h2aH (by norm_num) (by linarith)
        exact mul_le_mul this hEB (by norm_num) (by positivity)
      have hfrac : 2 * 25 ≤ 2 * Z3g BPz2 250 / (1 - rhoB) := by
        rw [le_div_iff₀ (by linarith)]; nlinarith
      have hfrac2 : 0 ≤ 2 * c3g 10 250 / (1 - rhoB) ^ 2 := by
        have : 0 < 1 - rhoB := by linarith
        positivity
      have := mul_le_mul hEB' (le_add_of_le_of_nonneg hfrac hfrac2) (by norm_num) (by positivity)
      have hnum : (50:ℝ) ≤ 2 * 63.66 * 0.0149 * (2 * 25) := by norm_num
      linarith
    exact le_trans hC (by linarith)
  linarith

theorem T₀_ok : (200:ℝ) + max (10 * π * |(0:ℝ)|) 50 ≤ 250 := by
  rw [abs_zero, mul_zero, max_eq_right (by norm_num : (0:ℝ) ≤ 50)]; norm_num

end Prop_9_4_2

/-- **Incomparable constants at `H = 200`.** On [H]'s range `x ≥ 10³`, `T₀ ≥ 200 + max(10π|δ|, 50)`,
neither error term is pointwise below the other (witnesses 1 and 2). So
`Prop_9_4_2.ExplicitFormulaBound.mono` cannot carry the formal theorem to [H]'s printed statement at
`H = 200`, nor that statement to the formal theorem restricted to `x ≥ 10³`. -/
theorem prop_9_4_2_err_incomparable :
    (¬ ∀ (q : ℕ) (T₀ δ x : ℝ), 1e3 ≤ x → 200 + max (10 * π * |δ|) 50 ≤ T₀ →
        TernaryGoldbach.MajorArcs.err942N q T₀ δ x ≤ errBook 200 q T₀ δ x) ∧
    (¬ ∀ (q : ℕ) (T₀ δ x : ℝ), 1e3 ≤ x → 200 + max (10 * π * |δ|) 50 ≤ T₀ →
        errBook 200 q T₀ δ x ≤ TernaryGoldbach.MajorArcs.err942N q T₀ δ x) :=
  ⟨fun h => (h 1 250 0 1000 (by norm_num) T₀_ok).not_gt errBook_lt_err942N_at_1e3,
    fun h => (h 1 250 0 1e27 (by norm_num) T₀_ok).not_gt err942N_lt_errBook_at_1e27⟩

end Companion.Book
