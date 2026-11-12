import TernaryGoldbach

/-!
# [H, Lemma B.1.2]: `|η̂₂''|_∞ ≤ 31.521`, equation (B.6)

H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, Appendix B, §B.1 ("The
Fourier transform of `η₂''`"), Lemma B.1.2 (label `lem:camelo`), equation (B.6), printed page 292:
<https://arxiv.org/pdf/1501.05438v2#page=302>. The 2013 minor-arcs preprint arXiv:1205.5252v4 has
the same statement as Lemma A.2.

## What [H] states

Let `η₂ : ℝ⁺ → ℝ` be as in (3.4), `η₂(t) = 4 max(log 2 - |log 2t|, 0)`. Then
`|η̂₂''|_∞ ≤ 31.521` (B.6).

The Fourier transform is `f̂(t) = ∫ e(-xt) f(x) dx` with `e(x) = e^{2πix}` ([H, §2.3]). `η₂` is
continuous, but `η₂'` jumps at `1/4`, `1/2` and `1`, so `η₂''` is a distribution. [H]'s proof
writes it out: `η₂'' = 4(4δ_{1/4} - 4δ_{1/2} + δ₁) + f` (B.7). Here `f = -4x⁻²` on `[1/4, 1/2)`,
`f = 4x⁻²` on `[1/2, 1)` and `f = 0` elsewhere. So `η̂₂''(t) = 4g(t) + f̂(t)` with
`g(t) = 4e(-t/4) - 4e(-t/2) + e(-t)` (B.2). `lemma_B_1_2` below is the printed statement.

## What the formalization proves

`TernaryGoldbach.MinorArcs.eta2_fourier_bound'` (`TernaryGoldbach/MinorArcs/InnerSums.lean:80`)
states that `(2πt)² ‖𝓕 η₂ (t)‖ ≤ c₀` for every real `t`, with `c₀ = 32`
(`TernaryGoldbach.MinorArcs.c₀`). Since `|η̂₂''(t)| = (2πt)² |η̂₂(t)|`, this is (B.6) with `32` in
place of `31.521`. It comes from `TernaryGoldbach.MinorArcs.norm_eta2DD_le`
(`TernaryGoldbach/MinorArcs/Eta2DDBound.lean:63`), which says `‖eta2DD t‖ ≤ 32` for `t ≥ 0`. Here
`eta2DD t = (2πt)² η̂₂(t)` is the closed form obtained by integrating by parts twice
(`TernaryGoldbach.MinorArcs.eta2DD_eq`). The Lean proof of `32` does not use [H]'s
interval-arithmetic run. For `t ≥ 2` it uses an expansion in `1/(2πt)` (three integrations by
parts) and a kernel-checked grid, and for `0 ≤ t ≤ 2` Taylor polynomials and a kernel-checked
bisection. Neither theorem carries a `Fact` hypothesis. Both are in the dependency cone of the
main theorem and use only `propext`, `Classical.choice` and `Quot.sound`. Downstream, the
repository's minor-arc files use `c₀ = 32` where [H] uses `c₀ = 31.521` (for instance
`TernaryGoldbach/MinorArcs/Eta2Log.lean`, the analogue of [H, (B.11)]).

The repository also proves the analytic half of [H]'s proof:
`TernaryGoldbach.MinorArcs.norm_eta2DD_large` (`‖eta2DD t‖ ≤ 31.521` for `|t| ≥ 655`; not in the
cone).

## Relation, as certified here: implied

* `lemma_B_1_2_implies_formal :
  lemma_B_1_2 → type_of% @TernaryGoldbach.MinorArcs.eta2_fourier_bound'` and
  `lemma_B_1_2_implies_norm_eta2DD_le :
  lemma_B_1_2 → type_of% @TernaryGoldbach.MinorArcs.norm_eta2DD_le`.
  Neither proof uses the Lean bound. They use only `31.521 ≤ 32` and the identities
  `‖η̂₂''(t)‖ = (2πt)² ‖𝓕 η₂ (t)‖` and `η̂₂''(t) = -eta2DD t`.
* `lemma_B_1_2_formal_iff`: the Lean statement is equivalent to `∀ t, ‖η̂₂''(t)‖ ≤ 32`. So it is the
  book's statement with `32` for `31.521`, and nothing else differs. `lemma_B_1_2_le_32` is that
  bound for the book's object.
* `lemma_B_1_2_iff_Ico`: (B.6) is equivalent to its restriction to `0 ≤ t < 655`. The rest is
  covered by `lemma_B_1_2_of_le_abs` (`|t| ≥ 655`, from `norm_eta2DD_large`) and by symmetry
  (`lemma_B_1_2_norm_eta2DDhat_neg`). What the formalization lacks is exactly [H]'s numerical
  check on `[0, 655)`.

The printed constant is true but tight. We recomputed `|η̂₂''(t)| = |eta2DD t|` in double
precision, using the closed form through `Si` and `Ci`, checked against direct quadrature. We
sampled `[0, 655]` with step `0.0005` and refined the 40 largest sampled maxima by golden-section
search. The maximum is `31.5206521` at `t ≈ 17.41478`. The next local maxima are `31.519215` at
`t ≈ 21.416` and `31.517562` at `t ≈ 13.413`. For `|t| ≥ 655` the analytic bound
`31.4821 + 80/(π|t|) ≤ 31.521` applies (`norm_eta2DD_large`). So (B.6) holds with margin about
`3.5·10⁻⁴`. This agrees with [H]'s `31.52065…`, reported with error at most `4.5·10⁻⁵`, plus a
sampling error below `0.000237`. The Lean constant `32` has margin `0.479`. The repository's
expansion for `t ≥ 2` has remainder `6120/(2πt)³`. That is about `0.0047` at `t ≈ 17.4`, more
than ten times the margin of (B.6), so the method used for `32` does not give `31.521` as it
stands. No proof of `lemma_B_1_2` is given here, and the status is "implied".

## Transcription checks

* `lemma_B_1_2_hat_eq_fourier`: the book's `f̂` is Mathlib's `𝓕`.
* `lemma_B_1_2_eta2_of_pos`, `lemma_B_1_2_eta2_of_nonpos`: the repository's `eta2` is (3.4) on
  `ℝ⁺` and `0` on `(-∞, 0]`.
* `lemma_B_1_2_eta2DDhat_eq_measure`: the definition `η̂₂''(t) = (2πit)² η̂₂(t)` agrees at every
  `t` with the Fourier transform of the measure (B.7), `4g(t) + f̂(t)`, where `f` is the printed
  piecewise function. `lemma_B_1_2_g_eq_dirac` writes `g` as the Fourier transform of
  `4δ_{1/4} - 4δ_{1/2} + δ₁`.
* `lemma_B_1_2_iff_ae`: reading `|·|_∞` as an essential supremum gives the same statement, since
  `η̂₂''` is continuous (`lemma_B_1_2_continuous_eta2DDhat`).
* `lemma_B_1_2_witness`: `‖η̂₂''(1972/3)‖ > 31.1` (numerically `31.244`). So the bound is not
  slack: `|η̂₂''|` provably exceeds `31.1`, within `1.4%` of `31.521`.

## On [H]'s proof (not used here)

The arithmetic of the analytic part checks out: `31.521 - 4 · 7.87052 = 0.03892` and
`80/(π · 0.03892) ≈ 654.3 < 655`. One sentence is misprinted. The proof says "the largest value
of `f̂(t)` we find is `31.52065…`", but the quantity is `|4g(t) + f̂(t)| = |η̂₂''(t)|`, because
`|f̂(t)| ≤ |f|₁ = 12` for every `t`. The statement is not affected.
-/

open Real Complex MeasureTheory FourierTransform

namespace Companion.Book

open TernaryGoldbach (e e_add e_zero e_intCast e_eq_cos_sin fourier_eq_integral_e)
open TernaryGoldbach.Helfgott (eta2)
open TernaryGoldbach.MinorArcs (eta2DD Jq c₀)

/-- The book's Fourier transform [H, §2.3]: `f̂(t) = ∫_{-∞}^{∞} e(-xt) f(x) dx`, with
`e(x) = e^{2πix}` (the repository's `TernaryGoldbach.e`). It is Mathlib's `𝓕`
(`lemma_B_1_2_hat_eq_fourier`). It is only applied here to `η₂` and to `f`, which are integrable,
so the Bochner integral's junk value `0` for non-integrable functions never arises. -/
noncomputable def lemma_B_1_2_hat (f : ℝ → ℝ) (t : ℝ) : ℂ := ∫ x : ℝ, e (-(x * t)) * (f x : ℂ)

/-- `η̂₂''(t) = (2πit)² η̂₂(t)`: the Fourier transform of the distributional second derivative of
`η₂`, with the book's normalization. It is [H, §2.3]'s rule `f̂(t) = f̂'(t)/(2πit)`, applied twice.
The explicit form in [H]'s proof, `4g(t) + f̂(t)` from (B.7), is the same function
(`lemma_B_1_2_eta2DDhat_eq_measure`). It is `-eta2DD t` in the repository's notation
(`lemma_B_1_2_eta2DDhat_eq_neg_eta2DD`). -/
noncomputable def lemma_B_1_2_eta2DDhat (t : ℝ) : ℂ := (2 * π * I * t) ^ 2 * lemma_B_1_2_hat eta2 t

/-- **[H, Lemma B.1.2], equation (B.6), as printed**: `|η̂₂''|_∞ ≤ 31.521`.

Transcription choices:
* "`η₂ : ℝ⁺ → ℝ` as in (3.4)" is the repository's `TernaryGoldbach.Helfgott.eta2`. On
  `ℝ⁺ = (0, ∞)` it is the printed `4 max(log 2 - |log 2t|, 0)` (`lemma_B_1_2_eta2_of_pos`). On
  `(-∞, 0]` it is `0` (`lemma_B_1_2_eta2_of_nonpos`). Extending by zero is how [H] takes Fourier
  transforms of functions on `ℝ⁺` (`supp η₂ = (1/4, 1)`, [H, proof of Lemma B.2.1]).
* `η̂₂''` is `lemma_B_1_2_eta2DDhat`, that is `(2πit)² η̂₂(t)`, with the book's
  `f̂(t) = ∫ e(-xt) f(x) dx` (`lemma_B_1_2_hat`). `η₂'` jumps at `1/4`, `1/2` and `1`, so `η₂''`
  exists only as a distribution, and `(2πit)² η̂₂` is its Fourier transform. [H]'s explicit form
  `η̂₂''(t) = 4g(t) + f̂(t)` from (B.7) is the same function (`lemma_B_1_2_eta2DDhat_eq_measure`).
* "`|·|_∞ ≤ 31.521`" is `∀ t : ℝ, ‖η̂₂''(t)‖ ≤ 31.521`, for every real `t` of either sign. The
  bound is not written with `⨆`, whose junk value `0` for an unbounded family would make it
  vacuous. Reading `|·|_∞` as an essential supremum gives the same proposition
  (`lemma_B_1_2_iff_ae`). The literal `31.521` is the exact rational `31521/1000`.
* There are no hypotheses: the lemma is one numerical inequality. -/
def lemma_B_1_2 : Prop := ∀ t : ℝ, ‖lemma_B_1_2_eta2DDhat t‖ ≤ 31.521

/-- `g(t) = 4e(-t/4) - 4e(-t/2) + e(-t)`, [H, (B.2)], as printed. It is the Fourier transform of
`4δ_{1/4} - 4δ_{1/2} + δ₁` (`lemma_B_1_2_g_eq_dirac`), and [H]'s proof of Lemma B.1.2 uses it
through `η̂₂''(t) = 4g(t) + f̂(t)`. -/
noncomputable def lemma_B_1_2_g (t : ℝ) : ℂ := 4 * e (-t / 4) - 4 * e (-t / 2) + e (-t)

/-- The function `f` of [H, (B.7)], as printed: `0` if `x < 1/4` or `x ≥ 1`, `-4x⁻²` if
`1/4 ≤ x < 1/2`, and `4x⁻²` if `1/2 ≤ x < 1`. It is the absolutely continuous part of the
measure `η₂''`. -/
noncomputable def lemma_B_1_2_f (x : ℝ) : ℝ :=
  if x < 1 / 4 ∨ 1 ≤ x then 0 else if x < 1 / 2 then -4 * x ^ (-2 : ℤ) else 4 * x ^ (-2 : ℤ)

/-! ### The book's objects and the repository's -/

/-- Transcription check: the book's Fourier transform is Mathlib's `𝓕`. -/
theorem lemma_B_1_2_hat_eq_fourier (f : ℝ → ℝ) (t : ℝ) :
    lemma_B_1_2_hat f t = 𝓕 (fun x => (f x : ℂ)) t :=
  (fourier_eq_integral_e _ t).symm

/-- Transcription check: on `ℝ⁺` the repository's `eta2` is [H, (3.4)] as printed. -/
theorem lemma_B_1_2_eta2_of_pos {t : ℝ} (ht : 0 < t) :
    eta2 t = 4 * max (Real.log 2 - |Real.log (2 * t)|) 0 := by
  rw [TernaryGoldbach.Helfgott.eta2, ite_eq_left ht]

/-- Transcription check: the repository's `eta2` vanishes on `(-∞, 0]`. This is the extension by
zero of a function on `ℝ⁺`. -/
theorem lemma_B_1_2_eta2_of_nonpos {t : ℝ} (ht : t ≤ 0) : eta2 t = 0 := by
  rw [TernaryGoldbach.Helfgott.eta2, ite_eq_right (not_lt.mpr ht)]

theorem lemma_B_1_2_two_pi_I_sq (t : ℝ) :
    (2 * π * I * t) ^ 2 = -(((2 * π * t) ^ 2 : ℝ) : ℂ) := by
  push_cast; ring_nf; rw [I_sq]; ring

/-- `|η̂₂''(t)| = (2πt)² |η̂₂(t)|`: the left side of (B.6) at `t` is the left side of the Lean
statement `eta2_fourier_bound'`. -/
theorem lemma_B_1_2_norm_eta2DDhat (t : ℝ) :
    ‖lemma_B_1_2_eta2DDhat t‖ = (2 * π * t) ^ 2 * ‖𝓕 (fun u => (eta2 u : ℂ)) t‖ := by
  rw [lemma_B_1_2_eta2DDhat, lemma_B_1_2_hat_eq_fourier, norm_mul, lemma_B_1_2_two_pi_I_sq,
    norm_neg, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]

/-- `J(a, b, 0) = ∫_a^b u⁻² du = a⁻¹ - b⁻¹`. -/
theorem lemma_B_1_2_Jq_zero {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) :
    Jq a b 0 = ((a⁻¹ - b⁻¹ : ℝ) : ℂ) := by
  rw [Jq]
  simp only [mul_zero, neg_zero, e_zero, one_mul]
  rw [intervalIntegral.integral_ofReal]
  congr 1
  have hd : ∀ x ∈ Set.uIcc a b, HasDerivAt (fun u : ℝ => -u⁻¹) ((x ^ 2)⁻¹) x := by
    intro x hx
    rw [Set.uIcc_of_le hab] at hx
    have hx0 : x ≠ 0 := (ha.trans_le hx.1).ne'
    convert (hasDerivAt_inv hx0).neg using 1
    ring
  have hc : ContinuousOn (fun u : ℝ => (u ^ 2)⁻¹) (Set.uIcc a b) := by
    have := TernaryGoldbach.MinorArcs.continuousOn_inv_sq ha hab 1
    simpa using this
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hd hc.intervalIntegrable]
  ring

/-- `eta2DD 0 = 16 - 16 - 4 + 4 · 2 - 4 · 1 = 0`. -/
theorem lemma_B_1_2_eta2DD_zero : eta2DD 0 = 0 := by
  rw [eta2DD, lemma_B_1_2_Jq_zero (by norm_num) (by norm_num),
    lemma_B_1_2_Jq_zero (by norm_num) (by norm_num)]
  simp only [mul_zero, neg_zero, e_zero]
  push_cast
  norm_num

/-- `η̂₂''(t) = -eta2DD t` for every `t`, from `TernaryGoldbach.MinorArcs.eta2DD_eq` (an
identity, not the bound) for `t ≠ 0`, and by direct evaluation at `t = 0`. -/
theorem lemma_B_1_2_eta2DDhat_eq_neg_eta2DD (t : ℝ) : lemma_B_1_2_eta2DDhat t = -eta2DD t := by
  rcases eq_or_ne t 0 with rfl | ht
  · rw [lemma_B_1_2_eta2DD_zero, lemma_B_1_2_eta2DDhat]; simp
  · rw [← TernaryGoldbach.MinorArcs.eta2DD_eq ht, lemma_B_1_2_eta2DDhat,
      lemma_B_1_2_hat_eq_fourier]
    ring_nf; rw [I_sq]; ring

/-! ### The second reading: the measure (B.7) -/

theorem lemma_B_1_2_f_eq (t x : ℝ) :
    e (-(x * t)) * (lemma_B_1_2_f x : ℂ) =
      (Set.Ico (1 / 4 : ℝ) (1 / 2)).indicator
          (fun x => e (-(x * t)) * ((-4 * (x ^ 2)⁻¹ : ℝ) : ℂ)) x +
        (Set.Ico (1 / 2 : ℝ) 1).indicator
          (fun x => e (-(x * t)) * ((4 * (x ^ 2)⁻¹ : ℝ) : ℂ)) x := by
  rcases lt_or_ge x (1 / 4) with h1 | h1
  · rw [Set.indicator_of_notMem (fun h => by linarith [h.1]),
      Set.indicator_of_notMem (fun h => by linarith [h.1]), lemma_B_1_2_f,
      ite_eq_left (Or.inl h1)]
    simp
  rcases lt_or_ge x (1 / 2) with h2 | h2
  · rw [Set.indicator_of_mem (show x ∈ Set.Ico (1 / 4 : ℝ) (1 / 2) from ⟨h1, h2⟩),
      Set.indicator_of_notMem (fun h => by linarith [h.1]), lemma_B_1_2_f,
      ite_eq_right (by rintro (h | h) <;> linarith), ite_eq_left h2]
    simp [zpow_neg]
  rcases lt_or_ge x 1 with h3 | h3
  · rw [Set.indicator_of_notMem (fun h => by linarith [h.2]),
      Set.indicator_of_mem (show x ∈ Set.Ico (1 / 2 : ℝ) 1 from ⟨h2, h3⟩), lemma_B_1_2_f,
      ite_eq_right (by rintro (h | h) <;> linarith), ite_eq_right (not_lt.mpr h2)]
    simp [zpow_neg]
  · rw [Set.indicator_of_notMem (fun h => by linarith [h.2]),
      Set.indicator_of_notMem (fun h => by linarith [h.2]), lemma_B_1_2_f,
      ite_eq_left (Or.inr h3)]
    simp

/-- `f̂(t) = -4 J(1/4, 1/2, t) + 4 J(1/2, 1, t)`, where `J(a, b, t) = ∫_a^b e(-ut)/u² du` is the
repository's `Jq`. -/
theorem lemma_B_1_2_hat_f (t : ℝ) :
    lemma_B_1_2_hat lemma_B_1_2_f t = -4 * Jq (1 / 4) (1 / 2) t + 4 * Jq (1 / 2) 1 t := by
  have hc : ∀ (k a b : ℝ), 0 < a → a ≤ b →
      IntegrableOn (fun x : ℝ => e (-(x * t)) * ((k * (x ^ 2)⁻¹ : ℝ) : ℂ)) (Set.Ico a b) := by
    intro k a b ha hab
    have h1 := TernaryGoldbach.MinorArcs.continuousOn_inv_sq ha hab k
    rw [Set.uIcc_of_le hab] at h1
    exact (((TernaryGoldbach.MinorArcs.continuous_E t).continuousOn).mul
      (continuous_ofReal.comp_continuousOn h1)).integrableOn_Icc.mono_set Set.Ico_subset_Icc_self
  rw [lemma_B_1_2_hat]
  simp_rw [lemma_B_1_2_f_eq t]
  rw [integral_add ((hc _ _ _ (by norm_num) (by norm_num)).integrable_indicator measurableSet_Ico)
      ((hc _ _ _ (by norm_num) (by norm_num)).integrable_indicator measurableSet_Ico),
    integral_indicator measurableSet_Ico, integral_indicator measurableSet_Ico,
    integral_Ico_eq_integral_Ioc, integral_Ico_eq_integral_Ioc,
    ← intervalIntegral.integral_of_le (by norm_num),
    ← intervalIntegral.integral_of_le (by norm_num), Jq, Jq,
    ← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_const_mul]
  congr 1 <;> (congr 1; ext x; push_cast; ring)

/-- Transcription check: the two readings of `η̂₂''` agree. For every `t`,
`(2πit)² η̂₂(t) = 4g(t) + f̂(t)`, which is the Fourier transform of the measure
`4(4δ_{1/4} - 4δ_{1/2} + δ₁) + f(x) dx` of [H, (B.7)] (with `lemma_B_1_2_g_eq_dirac`). -/
theorem lemma_B_1_2_eta2DDhat_eq_measure (t : ℝ) :
    lemma_B_1_2_eta2DDhat t = 4 * lemma_B_1_2_g t + lemma_B_1_2_hat lemma_B_1_2_f t := by
  rw [lemma_B_1_2_eta2DDhat_eq_neg_eta2DD, lemma_B_1_2_hat_f, eta2DD, lemma_B_1_2_g]
  have h1 : e (-t / 4) = e (-(1 / 4 * t)) := by congr 1; ring
  have h2 : e (-t / 2) = e (-(1 / 2 * t)) := by congr 1; ring
  have h3 : e (-t) = e (-(1 * t)) := by congr 1; ring
  rw [h1, h2, h3]
  ring

/-- `g` is the Fourier transform of the point masses `4δ_{1/4} - 4δ_{1/2} + δ₁` of (B.7):
`g(t) = 4 ∫ e(-xt) dδ_{1/4} - 4 ∫ e(-xt) dδ_{1/2} + ∫ e(-xt) dδ₁`. -/
theorem lemma_B_1_2_g_eq_dirac (t : ℝ) :
    lemma_B_1_2_g t =
      4 * ∫ x, e (-(x * t)) ∂(Measure.dirac (1 / 4 : ℝ)) -
        4 * ∫ x, e (-(x * t)) ∂(Measure.dirac (1 / 2 : ℝ)) +
        ∫ x, e (-(x * t)) ∂(Measure.dirac (1 : ℝ)) := by
  rw [integral_dirac, integral_dirac, integral_dirac, lemma_B_1_2_g]
  have h1 : e (-t / 4) = e (-(1 / 4 * t)) := by congr 1; ring
  have h2 : e (-t / 2) = e (-(1 / 2 * t)) := by congr 1; ring
  have h3 : e (-t) = e (-(1 * t)) := by congr 1; ring
  rw [h1, h2, h3]

/-! ### Relation to the formalization -/

/-- **The book's statement implies the Lean statement** `eta2_fourier_bound'`
(`(2πt)² ‖𝓕 η₂ (t)‖ ≤ c₀ = 32`). The proof uses `‖η̂₂''(t)‖ = (2πt)² ‖𝓕 η₂ (t)‖` and
`31.521 ≤ 32`, not the Lean theorem. -/
theorem lemma_B_1_2_implies_formal :
    lemma_B_1_2 → type_of% @TernaryGoldbach.MinorArcs.eta2_fourier_bound' := by
  intro h t
  rw [← lemma_B_1_2_norm_eta2DDhat]
  exact (h t).trans (by norm_num [c₀])

/-- **The book's statement implies the Lean statement** `norm_eta2DD_le`
(`‖eta2DD t‖ ≤ 32` for `t ≥ 0`). The proof uses `η̂₂''(t) = -eta2DD t` and `31.521 ≤ 32`, not the
Lean theorem. -/
theorem lemma_B_1_2_implies_norm_eta2DD_le :
    lemma_B_1_2 → type_of% @TernaryGoldbach.MinorArcs.norm_eta2DD_le := by
  intro h t _
  have := h t
  rw [lemma_B_1_2_eta2DDhat_eq_neg_eta2DD, norm_neg] at this
  linarith

/-- The Lean statement `eta2_fourier_bound'` is (B.6) with the constant `32` in place of
`31.521`, and nothing else changed. -/
theorem lemma_B_1_2_formal_iff :
    type_of% @TernaryGoldbach.MinorArcs.eta2_fourier_bound' ↔
      ∀ t : ℝ, ‖lemma_B_1_2_eta2DDhat t‖ ≤ 32 := by
  refine ⟨fun h t => ?_, fun h t => ?_⟩
  · rw [lemma_B_1_2_norm_eta2DDhat]; exact h t
  · rw [← lemma_B_1_2_norm_eta2DDhat]; exact h t

/-- What the formalization proves about the book's object: `|η̂₂''|_∞ ≤ 32`. -/
theorem lemma_B_1_2_le_32 (t : ℝ) : ‖lemma_B_1_2_eta2DDhat t‖ ≤ 32 :=
  lemma_B_1_2_formal_iff.mp TernaryGoldbach.MinorArcs.eta2_fourier_bound' t

/-- (B.6) for `|t| ≥ 655`. This is the analytic half of [H]'s proof (Lemma B.1.1 and (B.8)), from
the repository's `norm_eta2DD_large`. -/
theorem lemma_B_1_2_of_le_abs {t : ℝ} (ht : 655 ≤ |t|) : ‖lemma_B_1_2_eta2DDhat t‖ ≤ 31.521 := by
  rw [lemma_B_1_2_eta2DDhat_eq_neg_eta2DD, norm_neg]
  exact TernaryGoldbach.MinorArcs.norm_eta2DD_large ht

/-- `|η̂₂''(-t)| = |η̂₂''(t)|` ([H]: "it suffices to consider `t` non-negative"). -/
theorem lemma_B_1_2_norm_eta2DDhat_neg (t : ℝ) :
    ‖lemma_B_1_2_eta2DDhat (-t)‖ = ‖lemma_B_1_2_eta2DDhat t‖ := by
  rw [lemma_B_1_2_norm_eta2DDhat, lemma_B_1_2_norm_eta2DDhat,
    TernaryGoldbach.MinorArcs.norm_fourier_eta2_neg]
  ring

/-- (B.6) is equivalent to its restriction to `0 ≤ t < 655`. This is the range of [H]'s
interval-arithmetic computation, and the only part of the printed statement the formalization
does not establish. -/
theorem lemma_B_1_2_iff_Ico :
    lemma_B_1_2 ↔ ∀ t ∈ Set.Ico (0 : ℝ) 655, ‖lemma_B_1_2_eta2DDhat t‖ ≤ 31.521 := by
  refine ⟨fun h t _ => h t, fun h t => ?_⟩
  rcases le_or_gt 655 |t| with ht | ht
  · exact lemma_B_1_2_of_le_abs ht
  · rcases le_or_gt 0 t with h0 | h0
    · exact h t ⟨h0, by rwa [abs_of_nonneg h0] at ht⟩
    · rw [← lemma_B_1_2_norm_eta2DDhat_neg]
      exact h (-t) ⟨by linarith, by rwa [abs_of_neg h0] at ht⟩

/-! ### Further transcription checks -/

/-- `η̂₂''` is continuous: `η₂` is integrable, so `η̂₂` is continuous. -/
theorem lemma_B_1_2_continuous_eta2DDhat : Continuous lemma_B_1_2_eta2DDhat := by
  have hint : Integrable (fun u => (eta2 u : ℂ)) :=
    (continuous_ofReal.comp
      TernaryGoldbach.Helfgott.continuous_eta2).integrable_of_hasCompactSupport
      (TernaryGoldbach.Helfgott.hasCompactSupport_eta2.comp_left (g := fun t : ℝ => (t : ℂ))
        (by simp))
  have hc : Continuous (𝓕 (fun u => (eta2 u : ℂ))) :=
    VectorFourier.fourierIntegral_continuous Real.continuous_fourierChar (by fun_prop) hint
  have h : lemma_B_1_2_eta2DDhat = fun t => (2 * π * I * t) ^ 2 * 𝓕 (fun u => (eta2 u : ℂ)) t := by
    funext t; rw [lemma_B_1_2_eta2DDhat, lemma_B_1_2_hat_eq_fourier]
  rw [h]
  exact (by fun_prop : Continuous fun t : ℝ => (2 * π * I * (t : ℂ)) ^ 2).mul hc

/-- Transcription check: reading `|·|_∞` in (B.6) as the essential supremum (for Lebesgue
measure) gives the same proposition as the pointwise supremum used in `lemma_B_1_2`. -/
theorem lemma_B_1_2_iff_ae :
    lemma_B_1_2 ↔ ∀ᵐ t ∂(volume : Measure ℝ), ‖lemma_B_1_2_eta2DDhat t‖ ≤ 31.521 := by
  refine ⟨fun h => Filter.Eventually.of_forall h, fun h t => ?_⟩
  have hc : Continuous fun t => ‖lemma_B_1_2_eta2DDhat t‖ := lemma_B_1_2_continuous_eta2DDhat.norm
  have h' : (fun t => min ‖lemma_B_1_2_eta2DDhat t‖ 31.521) =ᵐ[volume]
      fun t => ‖lemma_B_1_2_eta2DDhat t‖ := by
    filter_upwards [h] with t ht using min_eq_left ht
  have h'' := congr_fun ((Continuous.ae_eq_iff_eq volume (hc.min continuous_const) hc).mp h') t
  rw [← h'']
  exact min_le_right _ _

/-- Non-triviality: `‖η̂₂''(1972/3)‖ > 31.1`. At `t = 1972/3` the point-mass part is
`16e(1/3) - 20e(-1/3)`, whose imaginary part is `18√3 > 31.17`. The integral part is at most
`80/(π t) < 0.04` in norm (`TernaryGoldbach.MinorArcs.norm_Jq_le`). Numerically
`‖η̂₂''(1972/3)‖ ≈ 31.244`. So (B.6) is not slack: `|η̂₂''|` provably exceeds `31.1`, within
`1.4%` of `31.521`. -/
theorem lemma_B_1_2_witness : 31.1 < ‖lemma_B_1_2_eta2DDhat (1972 / 3)‖ := by
  rw [lemma_B_1_2_eta2DDhat_eq_neg_eta2DD, norm_neg]
  set t : ℝ := 1972 / 3 with ht
  have ht0 : t ≠ 0 := by norm_num [ht]
  have hz1 : e (-(1 / 2 * t)) = e (1 / 3) := by
    rw [show -(1 / 2 * t) = ((-329 : ℤ) : ℝ) + 1 / 3 by rw [ht]; push_cast; norm_num, e_add,
      e_intCast, one_mul]
  have hz2 : e (-(1 / 4 * t)) = e (-(1 / 3)) := by
    rw [show -(1 / 4 * t) = ((-164 : ℤ) : ℝ) + -(1 / 3) by rw [ht]; push_cast; norm_num, e_add,
      e_intCast, one_mul]
  have hz3 : e (-(1 * t)) = e (-(1 / 3)) := by
    rw [show -(1 * t) = ((-657 : ℤ) : ℝ) + -(1 / 3) by rw [ht]; push_cast; norm_num, e_add,
      e_intCast, one_mul]
  have hs : Real.sin (2 * π * (1 / 3)) = √3 / 2 := by
    rw [show 2 * π * (1 / 3) = π - π / 3 by ring, Real.sin_pi_sub, Real.sin_pi_div_three]
  have him1 : (e (1 / 3)).im = √3 / 2 := by
    rw [e_eq_cos_sin, hs]
    simp only [add_im, ofReal_im, mul_im, ofReal_re, I_re, I_im]
    ring
  have him2 : (e (-(1 / 3))).im = -(√3 / 2) := by
    rw [e_eq_cos_sin, show 2 * π * -(1 / 3) = -(2 * π * (1 / 3)) by ring, Real.sin_neg, hs]
    simp only [add_im, ofReal_im, mul_im, ofReal_re, I_re, I_im]
    ring
  set T : ℂ := 16 * e (-(1 / 2 * t)) - 16 * e (-(1 / 4 * t)) - 4 * e (-(1 * t)) with hT
  have hTim : T.im = 18 * √3 := by
    rw [hT, hz1, hz2, hz3]
    simp only [sub_im, mul_im, him1, him2]
    norm_num
    ring
  have hT' : 18 * √3 ≤ ‖T‖ := by
    rw [← hTim]; exact (le_abs_self _).trans (Complex.abs_im_le_norm T)
  have hJ1 := TernaryGoldbach.MinorArcs.norm_Jq_le (a := 1 / 4) (b := 1 / 2) (by norm_num)
    (by norm_num) ht0
  have hJ2 := TernaryGoldbach.MinorArcs.norm_Jq_le (a := 1 / 2) (b := 1) (by norm_num)
    (by norm_num) ht0
  have heq : eta2DD t = T + (4 * Jq (1 / 4) (1 / 2) t - 4 * Jq (1 / 2) 1 t) := by
    rw [eta2DD, hT]; ring
  have hR : ‖4 * Jq (1 / 4) (1 / 2) t - 4 * Jq (1 / 2) 1 t‖ ≤
      4 * ‖Jq (1 / 4) (1 / 2) t‖ + 4 * ‖Jq (1 / 2) 1 t‖ := by
    refine (norm_sub_le _ _).trans ?_
    rw [norm_mul, norm_mul]; norm_num
  have hsq3 : (1.732 : ℝ) < √3 := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  have hpi := Real.pi_gt_d2
  have habs : |t| = 1972 / 3 := by rw [ht, abs_of_pos (by norm_num)]
  rw [habs] at hJ1 hJ2
  have hsmall : 4 * (1 / (π * (1972 / 3) * (1 / 4) ^ 2)) + 4 * (1 / (π * (1972 / 3) * (1 / 2) ^ 2))
      ≤ 0.04 := by
    rw [show 4 * (1 / (π * (1972 / 3) * (1 / 4) ^ 2)) + 4 * (1 / (π * (1972 / 3) * (1 / 2) ^ 2)) =
      240 / (1972 * π) by field_simp; ring, div_le_iff₀ (by positivity)]
    nlinarith
  have hdiff := norm_sub_norm_le T (-(4 * Jq (1 / 4) (1 / 2) t - 4 * Jq (1 / 2) 1 t))
  rw [norm_neg, sub_neg_eq_add, ← heq] at hdiff
  nlinarith

end Companion.Book
