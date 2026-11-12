import TernaryGoldbach

/-!
# [H, Theorem 7.1.1] and the remark after it: `η̂♥(-δ) = √(2π) e^{-2π²δ²}`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §7.1
("Results"), Theorem 7.1.1 (label `thm:gowo1`), printed page 138
(<https://arxiv.org/pdf/1501.05438v2#page=148>). With `η♥(t) = e^{-t²/2}`:

> Let `x` be a real number `≥ 10⁸`. Let `χ` be a primitive Dirichlet character mod `q`,
> `1 ≤ q ≤ r`, where `r = 300000`. Then, for any `δ ∈ ℝ` with `|δ| ≤ 4r/q`,
> `∑_{n=1}^∞ Λ(n) χ(n) e((δ/x) n) e^{-(n/x)²/2} = I_{q=1} · η̂♥(-δ) · x + E · x`,
> where `I_{q=1} = 1` if `q = 1`, `I_{q=1} = 0` if `q ≠ 1`, and
> `|E| ≤ 4.306·10⁻²² + (1/√x) (650400/√q + 112)`.

Right after the theorem, [H] fixes the normalization `f̂(t) = ∫_{-∞}^{∞} e(-xt) f(x) dx` (as in
[H, §2.3]) and remarks:

> Of course, `η̂♥(-δ)` is just `√(2π) e^{-2π²δ²}`.

The remark also appears in Ch. 1, after (1.11)–(1.12) (p. 14,
<https://arxiv.org/pdf/1501.05438v2#page=24>), glossed as "self-duality of the Gaussian". It was
already in the 2013 major-arcs preprint (arXiv:1305.2897v4, after Thm. 1.1). This file is about
that remark (`thm_7_1_1_remark`). It also states the theorem itself (`thm_7_1_1`).

**The book's convention: `η♥` is one-sided.** The book's weights live on `ℝ⁺`, and their Fourier
transforms are taken after extending them by `0` to the negative axis:
* (7.1) (p. 137): the weights are `η : ℝ⁺ → ℂ`;
* §7.2 (p. 141): "smoothing functions based on the (one-sided) Gaussian `η♥(t) = e^{-t²/2}`";
* §9.2 (p. 177, just before (9.43)): "Recall we are working with the one-sided Gaussian, i.e., we
  set `η♥(t) = 0` for `t < 0`". (9.43) then computes `|η♥|₂² = ∫₀^∞ e^{-t²} dt = √π/2`;
* Lemma 9.1.1 (pp. 163–164) takes `η : ℝ₀⁺ → ℝ`. Its proof (p. 166) identifies the main term as
  `G_δ(1) = ∫₀^∞ η(t) e(δt) dt = η̂(-δ)`. Theorem 7.1.1 comes from that explicit formula, through
  Prop. 9.2.2 (p. 177, `η(t) = e^{-t²/2}`, main term `η̂(-δ) x`) and §9.6 (p. 194).

So `η̂♥(-δ) = ∫₀^∞ e(δt) e^{-t²/2} dt`. Its value is `√(π/2) e^{-2π²δ²} + i √2 D(√2 π δ)`, where
`D` is Dawson's integral: the real part is half the remark's value, and for `δ ≠ 0` there is also
an imaginary part. (Numerically, at `δ = 0.1` it is `1.028806 + 0.551811 i`, against the remark's
`2.057613`.) The remark's `√(2π) e^{-2π²δ²}` is the transform of the *two-sided* Gaussian. Under
that reading, though, Theorem 7.1.1 is false (see below). So no single reading makes both the remark
and the theorem true. The book's convention is the one under which the theorem can hold, and the
remark is the error.

**What the formalization proves.** Nothing about this item. The repository has no counterpart of
Theorem 7.1.1, nor of the Gaussian explicit formula Prop. 9.2.2 it is derived from, and nothing uses
them. For the major arcs, the book's Part III needs Cor. 7.1.3, Thm. 7.1.4 and Prop. 7.1.5. The
repository proves versions of these for its own weights (`TernaryGoldbach.MajorArcs.cor_7_1_3'`,
`TernaryGoldbach.MajorArcs.thm_7_1_4_one` and its siblings,
`TernaryGoldbach.MajorArcs.prop_7_1_5'`). Where it states main terms of this kind, it
Fourier-transforms the weight extended by zero to `(-∞, 0]` (for example
`TernaryGoldbach.MajorArcs.phiPos` in `TernaryGoldbach.MajorArcs.prop_9_3_2`). So the slip in the
remark cannot enter the formalization.

**Relation: refuted.** `thm_7_1_1_remark` is the remark as printed, read with the book's
convention: the one-sided `η♥` (`thm_7_1_1_etaHeart`) and the book's normalization of the
Fourier transform (`thm_7_1_1_hat`, which is Mathlib's `𝓕` by `thm_7_1_1_hat_eq_fourier`).
* `thm_7_1_1_remark_false : ¬ thm_7_1_1_remark`. At `δ = 0` (which satisfies `|δ| ≤ 4r/q` for every
  `q`) the book's `η̂♥(0)` is `∫₀^∞ e^{-t²/2} dt = √(π/2)` (`thm_7_1_1_hat_etaHeart_zero`, from
  Mathlib's `integral_gaussian_Ioi`). The remark says `√(2π)`.

Further results, all proved here without hypotheses:
* `thm_7_1_1_remark_ne`: the remark fails at *every* `δ ∈ ℝ`, so no restriction of the range of `δ`
  rescues it. The reason is `thm_7_1_1_re_hat_etaHeart`: `Re η̂♥(-δ) = √(2π) e^{-2π²δ²}/2`
  exactly. It is proved from the evenness of `t ↦ cos(2πδt) e^{-t²/2}` (Mathlib's
  `integral_comp_abs`) and Mathlib's `fourierIntegral_gaussian`.
* `thm_7_1_1_hat_gaussian`: the remark's formula holds for the two-sided Gaussian
  `t ↦ e^{-t²/2}` on `ℝ`. This is the "self-duality" of Ch. 1. It also shows that the falsity of
  `thm_7_1_1_remark` comes from the one-sided convention alone, and not from a transcription slip.
* `thm_7_1_1`: Theorem 7.1.1 as printed, with the book's one-sided `η̂♥`. It is only stated: it is
  not proved here or in the repository. `thm_7_1_1_main M` is the same statement with the main
  term `I_{q=1} · M(δ) · x` for an arbitrary function `M`. `thm_7_1_1_eq_main` (by `rfl`) shows
  that `thm_7_1_1` is `thm_7_1_1_main (fun δ => η̂♥(-δ))`.
* `thm_7_1_1_main_false_of_eq`: if `M(0) = √(2π)`, then `thm_7_1_1_main M` is false, at
  `x = 10³⁰`, `q = 1`, `χ` trivial, `δ = 0`. The input is the Chebyshev-type bound
  `∑_{n≥1} Λ(n) e^{-(n/x)²/2} ≤ 1.387 · x√(π/2) + 4·10²⁷` (`thm_7_1_1_gauss_sum_le`), which uses the
  repository's unconditional `TernaryGoldbach.Helfgott.psi_le` and
  `TernaryGoldbach.Explicit.psi_le_four` with Abel summation. The sum is about `1.2533 x`
  (`→ √(π/2)` by the prime number theorem), against the `√(2π) x ≈ 2.5066 x` the remark predicts.
  Consequences:
  - `thm_7_1_1_main_remark_false`: the theorem with the remark's main term is false;
  - `thm_7_1_1_twoSided_false`: the theorem read with the two-sided Gaussian is false;
  - `thm_7_1_1_remark_imp_not : thm_7_1_1_remark → ¬ thm_7_1_1`: the remark and the theorem
    cannot both hold.
* `thm_7_1_1_hyps_satisfiable`: the theorem's hypotheses can be met.
-/

open Real Set MeasureTheory FourierTransform
open scoped ArithmeticFunction.vonMangoldt

namespace Companion.Book

open TernaryGoldbach (e)

/-- The book's one-sided Gaussian `η♥`: `η♥(t) = e^{-t²/2}` for `t ≥ 0` and `η♥(t) = 0` for `t < 0`
([H, §7.1]: "Write `η♥(t) = e^{-t²/2}`"; [H, §9.2, p. 177]: "we set `η♥(t) = 0` for `t < 0`"). It
takes the value `η♥(0) = 1`, as in [H]. A single point does not affect the Fourier transform. -/
noncomputable def thm_7_1_1_etaHeart (t : ℝ) : ℝ := if t < 0 then 0 else Real.exp (-t ^ 2 / 2)

/-- The book's Fourier transform `f̂(t) = ∫_{-∞}^{∞} e(-xt) f(x) dx` ([H, §2.3], repeated after
Theorem 7.1.1), with `e(x) = e^{2πix}` (the repository's `TernaryGoldbach.e`). It is Mathlib's `𝓕`
(`thm_7_1_1_hat_eq_fourier`). -/
noncomputable def thm_7_1_1_hat (f : ℝ → ℝ) (t : ℝ) : ℂ := ∫ x : ℝ, e (-(x * t)) * (f x : ℂ)

/-- **The remark after [H, Theorem 7.1.1]**, as printed (p. 138; also after (1.11)–(1.12), p. 14):
"`η̂♥(-δ)` is just `√(2π) e^{-2π²δ²}`".

How the statement is transcribed:
* `η♥` is the book's one-sided Gaussian `thm_7_1_1_etaHeart`, which is `0` on `(-∞, 0)`. This is
  the book's convention for its weights on `ℝ⁺` ([H, §9.2, p. 177], [H, Lemma 9.1.1] and its proof,
  p. 166), and the reading under which Theorem 7.1.1 can hold. Under the two-sided reading the
  remark is true (`thm_7_1_1_hat_gaussian`) and the theorem is false (`thm_7_1_1_twoSided_false`).
* `η̂` is `thm_7_1_1_hat`, with the book's normalization `f̂(t) = ∫ e(-xt) f(x) dx`, evaluated
  at `-δ`.
* The identity is claimed for every `δ ∈ ℝ`: the remark states a formula for the function
  `δ ↦ η̂♥(-δ)`. Restricting `δ` to the theorem's range `|δ| ≤ 4r/q` would not change the verdict,
  since `thm_7_1_1_remark_ne` refutes the identity at every single `δ`.
* `√(2π) e^{-2π²δ²}` is the real number `√(2 * π) * Real.exp (-2 * π ^ 2 * δ ^ 2)`, viewed in
  `ℂ`. -/
def thm_7_1_1_remark : Prop :=
  ∀ δ : ℝ, thm_7_1_1_hat thm_7_1_1_etaHeart (-δ) =
    ((√(2 * π) * Real.exp (-2 * π ^ 2 * δ ^ 2) : ℝ) : ℂ)

/-- The book's normalization of the Fourier transform is Mathlib's `𝓕` (the repository's
convention). The proof uses the repository's `TernaryGoldbach.fourier_eq_integral_e`. -/
theorem thm_7_1_1_hat_eq_fourier (f : ℝ → ℝ) (t : ℝ) :
    thm_7_1_1_hat f t = 𝓕 (fun x => (f x : ℂ)) t :=
  (TernaryGoldbach.fourier_eq_integral_e _ t).symm

/-- With the one-sided `η♥`, `η̂♥(-δ) = ∫₀^∞ e(δt) e^{-t²/2} dt`. This is the main term
`G_δ(1) = ∫₀^∞ η(t) e(δt) dt` of [H, Lemma 9.1.1] (proof, p. 166). -/
theorem thm_7_1_1_hat_etaHeart (δ : ℝ) :
    thm_7_1_1_hat thm_7_1_1_etaHeart (-δ) =
      ∫ t in Ioi 0, e (δ * t) * (Real.exp (-t ^ 2 / 2) : ℂ) := by
  unfold thm_7_1_1_hat
  have h : (fun x : ℝ => e (-(x * -δ)) * ((thm_7_1_1_etaHeart x : ℝ) : ℂ)) =
      (Ici (0 : ℝ)).indicator (fun t => e (δ * t) * (Real.exp (-t ^ 2 / 2) : ℂ)) := by
    funext x
    by_cases hx : x < 0
    · rw [indicator_of_notMem (by simpa using hx)]
      simp [thm_7_1_1_etaHeart, hx]
    · rw [indicator_of_mem (by simpa using hx)]
      simp [thm_7_1_1_etaHeart, hx, mul_comm]
  rw [h, integral_indicator measurableSet_Ici, integral_Ici_eq_integral_Ioi]

/-- `η̂♥(0) = ∫₀^∞ e^{-t²/2} dt = √(π/2)`, from Mathlib's `integral_gaussian_Ioi`. -/
theorem thm_7_1_1_hat_etaHeart_zero :
    thm_7_1_1_hat thm_7_1_1_etaHeart 0 = ((√(π / 2) : ℝ) : ℂ) := by
  have h := thm_7_1_1_hat_etaHeart 0
  rw [neg_zero] at h
  rw [h]
  have h1 : ∀ t : ℝ, e (0 * t) * ((Real.exp (-t ^ 2 / 2) : ℝ) : ℂ) =
      ((Real.exp (-(1 / 2) * t ^ 2) : ℝ) : ℂ) := by
    intro t
    rw [zero_mul, show e 0 = 1 by simp [TernaryGoldbach.e], one_mul]
    congr 2
    ring
  simp_rw [h1]
  rw [integral_complex_ofReal, integral_gaussian_Ioi]
  congr 1
  rw [show π / (1 / 2) = 2 * π by ring, show π / 2 = (2 * π) / 2 ^ 2 by ring,
    Real.sqrt_div' _ (by positivity), Real.sqrt_sq (by norm_num)]

/-- **The remark is false** (refutation at `δ = 0`). The book's `η̂♥(0)` is `√(π/2) ≈ 1.2533`. The
remark gives `√(2π) e⁰ = √(2π) ≈ 2.5066`. -/
theorem thm_7_1_1_remark_false : ¬ thm_7_1_1_remark := by
  intro h
  have h0 := h 0
  rw [neg_zero, thm_7_1_1_hat_etaHeart_zero] at h0
  have h0' : √(π / 2) = √(2 * π) * Real.exp (-2 * π ^ 2 * 0 ^ 2) := by exact_mod_cast h0
  simp only [ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, zero_pow, mul_zero, Real.exp_zero,
    mul_one] at h0'
  rw [Real.sqrt_inj (by positivity) (by positivity)] at h0'
  linarith [Real.pi_pos]

/-- **The remark's formula is right for the two-sided Gaussian** ("self-duality of the Gaussian",
[H, Ch. 1]): `∫_{-∞}^{∞} e(δx) e^{-x²/2} dx = √(2π) e^{-2π²δ²}`. The proof uses Mathlib's
`fourierIntegral_gaussian`. -/
theorem thm_7_1_1_hat_gaussian (δ : ℝ) :
    thm_7_1_1_hat (fun t => Real.exp (-t ^ 2 / 2)) (-δ) =
      ((√(2 * π) * Real.exp (-2 * π ^ 2 * δ ^ 2) : ℝ) : ℂ) := by
  unfold thm_7_1_1_hat
  have hG := fourierIntegral_gaussian (b := (1 / 2 : ℂ)) (by norm_num) (2 * π * δ)
  have h1 : ∀ x : ℝ, e (-(x * -δ)) * ((Real.exp (-x ^ 2 / 2) : ℝ) : ℂ) =
      Complex.exp (Complex.I * (2 * π * δ) * x) * Complex.exp (-(1 / 2) * x ^ 2) := by
    intro x
    simp only [TernaryGoldbach.e, Complex.ofReal_exp]
    congr 1
    · congr 1; push_cast; ring
    · congr 1; push_cast; ring
  simp_rw [h1, hG]
  have h2 : (π : ℂ) / (1 / 2) = ((2 * π : ℝ) : ℂ) := by push_cast; ring
  have h3 : -((2 : ℂ) * π * δ) ^ 2 / (4 * (1 / 2)) = ((-2 * π ^ 2 * δ ^ 2 : ℝ) : ℂ) := by
    push_cast; ring
  rw [h2, h3, show (1 / 2 : ℂ) = ((1 / 2 : ℝ) : ℂ) by push_cast; ring,
    ← Complex.ofReal_cpow (by positivity), ← Real.sqrt_eq_rpow, ← Complex.ofReal_exp]
  push_cast
  ring

/-- **The real part of the book's `η̂♥(-δ)` is exactly half the remark's value**:
`Re η̂♥(-δ) = ∫₀^∞ cos(2πδt) e^{-t²/2} dt = √(2π) e^{-2π²δ²}/2`. The integrand is even
(`integral_comp_abs`), so this is half the two-sided integral (`thm_7_1_1_hat_gaussian`). -/
theorem thm_7_1_1_re_hat_etaHeart (δ : ℝ) :
    (thm_7_1_1_hat thm_7_1_1_etaHeart (-δ)).re =
      √(2 * π) * Real.exp (-2 * π ^ 2 * δ ^ 2) / 2 := by
  set g : ℝ → ℂ := fun t => e (δ * t) * ((Real.exp (-t ^ 2 / 2) : ℝ) : ℂ) with hg
  have hgi : Integrable g := by
    have := integrable_cexp_quadratic (b := (1 / 2 : ℂ)) (by norm_num) (2 * π * δ * Complex.I) 0
    refine this.congr (Filter.Eventually.of_forall fun t => ?_)
    simp only [g, TernaryGoldbach.e, Complex.ofReal_exp, ← Complex.exp_add]
    congr 1; push_cast; ring
  have hre : ∀ t : ℝ, (g t).re = Real.cos (2 * π * δ * t) * Real.exp (-t ^ 2 / 2) := by
    intro t
    simp only [g, TernaryGoldbach.e]
    rw [Complex.re_mul_ofReal,
      show (2 * (π : ℂ) * Complex.I * ((δ * t : ℝ) : ℂ)) = ((2 * π * δ * t : ℝ) : ℂ) * Complex.I by
        push_cast; ring,
      Complex.exp_ofReal_mul_I_re]
  have hfull : ∫ t, g t = ((√(2 * π) * Real.exp (-2 * π ^ 2 * δ ^ 2) : ℝ) : ℂ) := by
    rw [← thm_7_1_1_hat_gaussian δ, thm_7_1_1_hat]
    congr 1
    funext x
    simp only [g]
    congr 2
    ring
  have hre_int : ∀ s : Set ℝ, ∫ t in s, (g t).re = (∫ t in s, g t).re := fun s => by
    have := integral_re (𝕜 := ℂ) (hgi.integrableOn (s := s))
    simpa using this
  have habs : ∫ t, Real.cos (2 * π * δ * t) * Real.exp (-t ^ 2 / 2) =
      2 * ∫ t in Ioi 0, Real.cos (2 * π * δ * t) * Real.exp (-t ^ 2 / 2) := by
    rw [← integral_comp_abs (f := fun t => Real.cos (2 * π * δ * t) * Real.exp (-t ^ 2 / 2))]
    congr 1
    funext t
    rcases abs_cases t with ⟨h, _⟩ | ⟨h, _⟩
    · rw [h]
    · rw [h, neg_sq, show 2 * π * δ * -t = -(2 * π * δ * t) by ring, Real.cos_neg]
  have hfull_re : ∫ t, Real.cos (2 * π * δ * t) * Real.exp (-t ^ 2 / 2) =
      √(2 * π) * Real.exp (-2 * π ^ 2 * δ ^ 2) := by
    have := hre_int univ
    simp only [Measure.restrict_univ] at this
    simp_rw [← hre, this, hfull, Complex.ofReal_re]
  rw [thm_7_1_1_hat_etaHeart, ← hre_int]
  simp_rw [hre]
  linarith

/-- **The remark fails at every `δ ∈ ℝ`**: `η̂♥(-δ) ≠ √(2π) e^{-2π²δ²}`, because the real parts
differ by a factor `2` (`thm_7_1_1_re_hat_etaHeart`) and `√(2π) e^{-2π²δ²} > 0`. -/
theorem thm_7_1_1_remark_ne (δ : ℝ) :
    thm_7_1_1_hat thm_7_1_1_etaHeart (-δ) ≠
      ((√(2 * π) * Real.exp (-2 * π ^ 2 * δ ^ 2) : ℝ) : ℂ) := by
  intro h
  have h1 := thm_7_1_1_re_hat_etaHeart δ
  rw [h, Complex.ofReal_re] at h1
  have : 0 < √(2 * π) * Real.exp (-2 * π ^ 2 * δ ^ 2) :=
    mul_pos (Real.sqrt_pos.mpr (by positivity)) (Real.exp_pos _)
  linarith

/-- **[H, Theorem 7.1.1] with its main term abstracted**: the printed statement (see `thm_7_1_1`)
with `I_{q=1} · M(δ) · x` in place of `I_{q=1} · η̂♥(-δ) · x`, for a function `M : ℝ → ℂ`. It lets
us compare readings of `η̂♥(-δ)`: `thm_7_1_1 = thm_7_1_1_main (fun δ => η̂♥(-δ))`
(`thm_7_1_1_eq_main`). Every other part of the statement is transcribed as in `thm_7_1_1`. -/
def thm_7_1_1_main (M : ℝ → ℂ) : Prop :=
  ∀ x : ℝ, 10 ^ 8 ≤ x →
    ∀ q : ℕ, 1 ≤ q → q ≤ 300000 →
      ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
        ∀ δ : ℝ, |δ| ≤ 4 * 300000 / (q : ℝ) →
          ∃ E : ℂ,
            ∑' n : ℕ+, (Λ (n : ℕ) : ℂ) * χ ((n : ℕ) : ZMod q) * e (δ / x * (n : ℕ)) *
                (Real.exp (-((n : ℕ) / x) ^ 2 / 2) : ℂ) =
              (if q = 1 then 1 else 0) * M δ * x + E * x ∧
            ‖E‖ ≤ 4.306e-22 + 1 / √x * (650400 / √(q : ℝ) + 112)

/-- **[H, Theorem 7.1.1]**, as printed (p. 138). It is stated only: neither this file nor the
repository proves it, and the repository does not use it.

How the statement is transcribed:
* "`x` a real number `≥ 10⁸`": `x : ℝ` with `10 ^ 8 ≤ x`.
* "`χ` a primitive Dirichlet character mod `q`, `1 ≤ q ≤ r`, where `r = 300000`": `q : ℕ` with
  `1 ≤ q` and `q ≤ 300000` (`r` is inlined), and `χ : DirichletCharacter ℂ q` with Mathlib's
  `χ.IsPrimitive` (conductor `= q`). This is the book's notion ([H, §2.2]): a character of
  `(ℤ/qℤ)*` lifted to `ℤ`, not induced from a smaller modulus. For `q = 1` it is the trivial
  character, which is primitive.
* "`δ ∈ ℝ` with `|δ| ≤ 4r/q`": `δ : ℝ` with `|δ| ≤ 4 * 300000 / q` in `ℝ`.
* The series `∑_{n=1}^∞` is the `tsum` over `n : ℕ+`, with the factors in the printed order
  `Λ(n) χ(n) e((δ/x) n) e^{-(n/x)²/2}`. `Λ` is Mathlib's von Mangoldt function and
  `χ(n) = χ(n mod q)`. The weight is written as printed, `e^{-(n/x)²/2}`; for `n ≥ 1` it equals
  `η♥(n/x)` under either reading of `η♥`. The terms are bounded by `log n · e^{-(n/x)²/2}`, so the
  series converges absolutely and the `tsum` is its sum.
* `I_{q=1}` is `if q = 1 then 1 else 0`.
* `η̂♥(-δ)` is `thm_7_1_1_hat thm_7_1_1_etaHeart (-δ)`: the book's Fourier normalization applied
  to the one-sided Gaussian, which is the book's convention (see `thm_7_1_1_remark`). It equals
  `∫₀^∞ e(δt) e^{-t²/2} dt` (`thm_7_1_1_hat_etaHeart`), the main term `G_δ(1)` of
  [H, Lemma 9.1.1]. It is *not* the remark's `√(2π) e^{-2π²δ²}` (`thm_7_1_1_remark_ne`). With that
  value the statement is false (`thm_7_1_1_main_remark_false`).
* `E` is a complex number, quantified after `x, q, χ, δ`, so it may depend on them. It satisfies
  the printed identity `sum = I_{q=1} · η̂♥(-δ) · x + E · x`, and `|E|` becomes `‖E‖ ≤
  4.306e-22 + 1 / √x * (650400 / √q + 112)`. The decimal literals are exact rationals.
* There is no hypothesis beyond the printed ones. Platt's GRH verification, which the book's
  proof uses (§9.6, `T₀ = 10⁸/q`), is not an assumption of the statement. -/
def thm_7_1_1 : Prop :=
  ∀ x : ℝ, 10 ^ 8 ≤ x →
    ∀ q : ℕ, 1 ≤ q → q ≤ 300000 →
      ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
        ∀ δ : ℝ, |δ| ≤ 4 * 300000 / (q : ℝ) →
          ∃ E : ℂ,
            ∑' n : ℕ+, (Λ (n : ℕ) : ℂ) * χ ((n : ℕ) : ZMod q) * e (δ / x * (n : ℕ)) *
                (Real.exp (-((n : ℕ) / x) ^ 2 / 2) : ℂ) =
              (if q = 1 then 1 else 0) * thm_7_1_1_hat thm_7_1_1_etaHeart (-δ) * x + E * x ∧
            ‖E‖ ≤ 4.306e-22 + 1 / √x * (650400 / √(q : ℝ) + 112)

/-- `thm_7_1_1` is `thm_7_1_1_main` at the book's main term `δ ↦ η̂♥(-δ)`. -/
theorem thm_7_1_1_eq_main :
    thm_7_1_1 = thm_7_1_1_main (fun δ => thm_7_1_1_hat thm_7_1_1_etaHeart (-δ)) := rfl

/-- Non-vacuity of the hypotheses of `thm_7_1_1`: `x = 10⁸`, `q = 1`, the trivial character mod
`1` (primitive) and `δ = 0` meet them. -/
theorem thm_7_1_1_hyps_satisfiable :
    ∃ (x : ℝ) (q : ℕ) (χ : DirichletCharacter ℂ q) (δ : ℝ),
      10 ^ 8 ≤ x ∧ 1 ≤ q ∧ q ≤ 300000 ∧ χ.IsPrimitive ∧ |δ| ≤ 4 * 300000 / (q : ℝ) :=
  ⟨10 ^ 8, 1, 1, 0, le_rfl, le_rfl, by norm_num, DirichletCharacter.isPrimitive_one_level_one,
    by norm_num⟩

/-- Abel summation in the form used below. Let `f ≥ 0` be antitone, and let the partial sums of `a`
satisfy `∑_{n ≤ N} a(n) ≤ αN + β` for every `N`. Then
`∑_{n ≤ N} a(n) f(n) ≤ α ∑_{1 ≤ n ≤ N} f(n) + β f(0)`. -/
theorem thm_7_1_1_abel {a f : ℕ → ℝ} {α β : ℝ} (hf : Antitone f) (hf0 : ∀ n, 0 ≤ f n)
    (hA : ∀ N : ℕ, ∑ n ∈ Finset.range (N + 1), a n ≤ α * N + β) (N : ℕ) :
    ∑ n ∈ Finset.range (N + 1), a n * f n ≤ α * ∑ n ∈ Finset.range N, f (n + 1) + β * f 0 := by
  have key : ∀ N : ℕ, ∑ n ∈ Finset.range (N + 1), a n * f n +
      (α * N + β - ∑ n ∈ Finset.range (N + 1), a n) * f N ≤
        α * ∑ n ∈ Finset.range N, f (n + 1) + β * f 0 := by
    intro N
    induction N with
    | zero => simp; linarith
    | succ N ih =>
      rw [Finset.sum_range_succ (fun n => a n * f n), Finset.sum_range_succ a,
        Finset.sum_range_succ (fun n => f (n + 1))]
      have h2 : f (N + 1) ≤ f N := hf (Nat.le_succ N)
      have h3 : 0 ≤ α * N + β - ∑ n ∈ Finset.range (N + 1), a n := by linarith [hA N]
      have h4 := mul_le_mul_of_nonneg_left h2 h3
      push_cast
      linarith
  have h5 : 0 ≤ (α * N + β - ∑ n ∈ Finset.range (N + 1), a n) * f N :=
    mul_nonneg (by linarith [hA N]) (hf0 N)
  linarith [key N]

/-- **A Chebyshev-type upper bound for the Gaussian-weighted prime sum**: for `x > 0`,
`∑_{n≥1} Λ(n) e^{-(n/x)²/2} ≤ 1.387 · x√(2π)/2 + 4·10²⁷`. Note that `x√(2π)/2 = x√(π/2)`.

The proof has three steps.
* `ψ(N) ≤ 1.387 N + 4·10²⁷` for every `N`. For `N ≥ 10²⁷` this is the repository's
  `TernaryGoldbach.Helfgott.psi_le`; below that, `TernaryGoldbach.Explicit.psi_le_four` gives
  `ψ(N) ≤ 4N`. Both are unconditional.
* Abel summation (`thm_7_1_1_abel`).
* `∑_{n≥1} e^{-(n/x)²/2} ≤ ∫₀^∞ e^{-(t/x)²/2} dt = x√(π/2)`. -/
theorem thm_7_1_1_gauss_sum_le {x : ℝ} (hx : 0 < x) :
    ∑' n : ℕ+, Λ (n : ℕ) * Real.exp (-((n : ℕ) / x) ^ 2 / 2) ≤
      1.387 * (x * √(2 * π) / 2) + 4 * 10 ^ 27 := by
  set f : ℕ → ℝ := fun n => Real.exp (-((n : ℝ) / x) ^ 2 / 2) with hf_def
  have hf : Antitone f := by
    intro m n hmn
    simp only [f]
    apply Real.exp_le_exp.mpr
    have : (m : ℝ) / x ≤ n / x := div_le_div_of_nonneg_right (by exact_mod_cast hmn) hx.le
    have h0 : 0 ≤ (m : ℝ) / x := by positivity
    nlinarith
  have hf0 : ∀ n, 0 ≤ f n := fun n => (Real.exp_pos _).le
  have hA : ∀ N : ℕ, ∑ n ∈ Finset.range (N + 1), Λ n ≤ 1.387 * N + 4 * 10 ^ 27 := by
    intro N
    have hpsi : ∑ n ∈ Finset.range (N + 1), Λ n = TernaryGoldbach.Helfgott.psi N := rfl
    rw [hpsi]
    by_cases hN : 10 ^ 27 ≤ N
    · have := TernaryGoldbach.Helfgott.psi_le N hN
      have : (0 : ℝ) ≤ N := N.cast_nonneg
      linarith
    · have := TernaryGoldbach.Explicit.psi_le_four N
      have hN' : (N : ℝ) ≤ 10 ^ 27 := by exact_mod_cast (Nat.lt_of_not_le hN).le
      have : (0 : ℝ) ≤ N := N.cast_nonneg
      linarith
  have hint : ∀ N : ℕ, ∑ n ∈ Finset.range N, f (n + 1) ≤ x * √(2 * π) / 2 := by
    intro N
    set F : ℝ → ℝ := fun t => Real.exp (-(1 / (2 * x ^ 2)) * t ^ 2) with hF
    have hFf : ∀ n : ℕ, f n = F n := by
      intro n; simp only [f, F]; congr 1; field_simp
    have hb : 0 < 1 / (2 * x ^ 2) := by positivity
    have hanti : AntitoneOn F (Icc 0 (0 + N)) := by
      intro s hs t ht hst
      simp only [F]
      apply Real.exp_le_exp.mpr
      nlinarith [mul_le_mul_of_nonneg_left (pow_le_pow_left₀ hs.1 hst 2) hb.le]
    have h1 := hanti.sum_le_integral
    have h2 : ∑ n ∈ Finset.range N, f (n + 1) =
        ∑ i ∈ Finset.range N, F (0 + ((i + 1 : ℕ) : ℝ)) := by
      refine Finset.sum_congr rfl fun i _ => ?_
      rw [hFf, zero_add]
    have hFi : IntegrableOn F (Ioi 0) := (integrable_exp_neg_mul_sq hb).integrableOn
    have h3 : ∫ t in (0 : ℝ)..0 + N, F t ≤ ∫ t in Ioi 0, F t := by
      rw [zero_add, intervalIntegral.integral_of_le (by positivity)]
      exact setIntegral_mono_set hFi (Filter.Eventually.of_forall fun t => (Real.exp_pos _).le)
        Ioc_subset_Ioi_self.eventuallyLE
    have h4 : ∫ t in Ioi 0, F t = x * √(2 * π) / 2 := by
      rw [integral_gaussian_Ioi]
      congr 1
      rw [show π / (1 / (2 * x ^ 2)) = x ^ 2 * (2 * π) by field_simp,
        Real.sqrt_mul (by positivity), Real.sqrt_sq hx.le]
    linarith
  have hpart : ∀ N : ℕ, ∑ n ∈ Finset.range N, Λ (n + 1) * f (n + 1) ≤
      1.387 * (x * √(2 * π) / 2) + 4 * 10 ^ 27 := by
    intro N
    have h1 := thm_7_1_1_abel (a := fun n => Λ n) hf hf0 hA N
    have h2 : ∑ n ∈ Finset.range (N + 1), Λ n * f n =
        ∑ n ∈ Finset.range N, Λ (n + 1) * f (n + 1) := by
      rw [Finset.sum_range_succ']; simp
    have hf00 : f 0 = 1 := by simp [f]
    rw [h2, hf00] at h1
    have := hint N
    linarith
  have hts : (∑' n : ℕ+, Λ (n : ℕ) * Real.exp (-((n : ℕ) / x) ^ 2 / 2)) =
      ∑' n : ℕ, Λ (n + 1) * f (n + 1) := tsum_pnat_eq_tsum_succ (f := fun n => Λ n * f n)
  rw [hts]
  exact Real.tsum_le_of_sum_range_le
    (fun n => mul_nonneg ArithmeticFunction.vonMangoldt_nonneg (hf0 _)) hpart

/-- **Theorem 7.1.1 fails for any main term with `M(0) = √(2π)`.** The witness is `x = 10³⁰`,
`q = 1`, the trivial character and `δ = 0`. The statement would give
`∑_{n≥1} Λ(n) e^{-(n/x)²/2} ≥ (√(2π) − 4.306·10⁻²² − 650512·10⁻¹⁵) x ≈ 2.5066 x`. But
`thm_7_1_1_gauss_sum_le` bounds the sum by `1.387 · x√(2π)/2 + 4·10²⁷ ≈ 1.7423 x`. -/
theorem thm_7_1_1_main_false_of_eq {M : ℝ → ℂ} (hM : M 0 = ((√(2 * π) : ℝ) : ℂ)) :
    ¬ thm_7_1_1_main M := by
  intro h
  obtain ⟨E, hE, hEb⟩ := h (10 ^ 30) (by norm_num) 1 le_rfl (by norm_num) 1
    DirichletCharacter.isPrimitive_one_level_one 0 (by norm_num)
  have hterm : ∀ n : ℕ+, (Λ (n : ℕ) : ℂ) * (1 : DirichletCharacter ℂ 1) ((n : ℕ) : ZMod 1) *
      e (0 / 10 ^ 30 * (n : ℕ)) * (Real.exp (-((n : ℕ) / (10 ^ 30 : ℝ)) ^ 2 / 2) : ℂ) =
      ((Λ (n : ℕ) * Real.exp (-((n : ℕ) / (10 ^ 30 : ℝ)) ^ 2 / 2) : ℝ) : ℂ) := by
    intro n
    rw [Subsingleton.elim ((n : ℕ) : ZMod 1) 1, map_one, zero_div, zero_mul,
      show e 0 = 1 by simp [TernaryGoldbach.e]]
    push_cast
    ring
  rw [tsum_congr hterm, ← Complex.ofReal_tsum, hM] at hE
  have hre := congrArg Complex.re hE
  simp only [Complex.ofReal_re, ↓reduceIte, Complex.add_re, Complex.mul_re, Complex.ofReal_im,
    mul_zero, sub_zero, one_mul] at hre
  have hsum := thm_7_1_1_gauss_sum_le (x := 10 ^ 30) (by norm_num)
  have hsq : √((10 : ℝ) ^ 30) = 10 ^ 15 := by
    rw [show (10 : ℝ) ^ 30 = (10 ^ 15) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  rw [hsq, Nat.cast_one, Real.sqrt_one] at hEb
  have hEre := abs_le.mp ((Complex.abs_re_le_norm E).trans hEb)
  have hs2 : (2 : ℝ) ≤ √(2 * π) := Real.le_sqrt_of_sq_le (by nlinarith [Real.pi_gt_three])
  nlinarith

/-- **Theorem 7.1.1 with the remark's main term `√(2π) e^{-2π²δ²}` is false.** So the remark and
the theorem are inconsistent, however `η̂♥` is read. -/
theorem thm_7_1_1_main_remark_false :
    ¬ thm_7_1_1_main (fun δ => ((√(2 * π) * Real.exp (-2 * π ^ 2 * δ ^ 2) : ℝ) : ℂ)) :=
  thm_7_1_1_main_false_of_eq (by simp)

/-- **Theorem 7.1.1 read with the two-sided Gaussian is false.** With `η♥(t) = e^{-t²/2}` on all
of `ℝ`, the remark holds (`thm_7_1_1_hat_gaussian`) and the theorem fails. This is why the book's
one-sided convention is the reading used in `thm_7_1_1` and `thm_7_1_1_remark`. -/
theorem thm_7_1_1_twoSided_false :
    ¬ thm_7_1_1_main (fun δ => thm_7_1_1_hat (fun t => Real.exp (-t ^ 2 / 2)) (-δ)) :=
  thm_7_1_1_main_false_of_eq (by rw [neg_zero, ← neg_zero, thm_7_1_1_hat_gaussian]; simp)

/-- **The remark and Theorem 7.1.1 cannot both hold**: if the remark were true, Theorem 7.1.1 (with
the book's `η̂♥`) would be false. The proof goes through `thm_7_1_1_main_false_of_eq` and does not
use `thm_7_1_1_remark_false`. -/
theorem thm_7_1_1_remark_imp_not : thm_7_1_1_remark → ¬ thm_7_1_1 := by
  intro hr
  rw [thm_7_1_1_eq_main]
  refine thm_7_1_1_main_false_of_eq ?_
  show thm_7_1_1_hat thm_7_1_1_etaHeart (-0) = _
  rw [hr 0]
  simp

end Companion.Book
