import TernaryGoldbach

/-!
# [H, Theorem 7.1.4]: the sum `Σ Λ(n) χ(n) e(δn/x) η₊(n/x)` for primitive `χ` of small modulus

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2,
Chapter 7 ("Major arcs: overview and results"), §7.1, Theorem 7.1.4 (printed p. 140, label
`thm:malpor`; <https://arxiv.org/pdf/1501.05438v2#page=150>). Let `η = η₊`,
`η₊(t) = h_H(t) t e^{-t²/2}`, with `h_H` as in (7.6) and `H = 200`. Let `x ≥ 10¹²` be real, and let
`χ` be a primitive character mod `q`, where `1 ≤ q ≤ 150000` if `q` is odd and `1 ≤ q ≤ 300000` if
`q` is even. Then for every real `δ` with `|δ| ≤ 600000 · gcd(q, 2)/q`

```
Σ_{n=1}^∞ Λ(n) χ(n) e(δn/x) η(n/x) = I_{q=1} · η̂(−δ) · x + E · x,
|E| ≤ 1.3482·10⁻¹⁴ + 1.617·10⁻¹⁰/q + (1/√x)(499900/√q + 52),
```

where `I_{q=1}` is `1` if `q = 1` and `0` otherwise. For `q = 1` there is also the sharper bound
`|E| ≤ 4.772·10⁻¹¹ + 251400/√x`. [H] proves the theorem in §9.6, from Prop. 9.4.2 and Platt's GRH
verification for these moduli. The 2013 preprint (arXiv:1305.2897v4, Thm 1.4) has the same
statement with the bounds `6.18·10⁻¹²/√q + 1.14·10⁻¹⁰/q + (499100/√q + 52)/√x` and
`3.34·10⁻¹¹ + 251100/√x`.

**What the formalization proves.** `TernaryGoldbach/MajorArcs/Thm714.lean` proves three
theorems. Each one is derived from `prop_9_4_2` (the formal [H, Prop 9.4.2], with its own
constants) and from Platt's verification `PlattGRH`. `PlattGRH` is the only `Fact` binder in
their signatures (`companion/data/hypothesis_trace.json`). All three assume `x ≥ 4.9·10²⁶`. They write the sum as `Schar χ (n ↦ Λ(n) η₊(n/x)) (δ/x)` and `η̂₊` as
Mathlib's `𝓕`:
* `MajorArcs.thm_7_1_4_odd`: odd `q ≤ 150000`, `|δ| ≤ 6·10⁵/q`,
  `|E| ≤ (7.5·10⁻⁸ + 7.7·10⁶/√x)/√q`;
* `MajorArcs.thm_7_1_4_even`: even `q ≤ 300000`, `|δ| ≤ 1.2·10⁶/q`, the same bound;
* `MajorArcs.thm_7_1_4_one`: `q = 1`, `|δ| ≤ 6·10⁵`, `|E| ≤ 10⁻¹⁸ + 6.24·10⁶/√x`.

All three are used downstream by `TernaryGoldbach.MajorArcs.arc_chars`.

**Relation: implied (the Lean theorems are weaker).** The odd and even theorems have [H]'s `q`-
and `δ`-ranges (`gcd(q, 2)` is `1` for odd `q` and `2` for even `q`), a narrower `x`-range, and a
larger bound. Their constant term is between 464 times [H]'s (at `q = 1`) and about `2.5·10⁴`
times it (at `q ≈ 12000`), and their `1/√x` coefficient is about 15 times [H]'s. This is
certified by
* `thm_7_1_4_implies_formal_odd : thm_7_1_4 → type_of% @TernaryGoldbach.MajorArcs.thm_7_1_4_odd`;
* `thm_7_1_4_implies_formal_even : thm_7_1_4 → type_of% @TernaryGoldbach.MajorArcs.thm_7_1_4_even`.

Together they cover every `q` of [H], including `q = 1` (which is odd). The arithmetic is
`Thm_7_1_4.book_bound_le`: if `1 ≤ √q ≤ 548`, then `√q` times [H]'s bound is at most
`7.39·10⁻¹² + 1.617·10⁻¹⁰ + 528396/√x ≤ 7.5·10⁻⁸ + 7.7·10⁶/√x`.

Since the Lean theorems are proved, an implication into them could be proved by quoting them. That
is not done here. The work is done by `Thm_7_1_4.implies_odd_core` and
`Thm_7_1_4.implies_even_core`, which are stated with no `Fact` instance in scope. So they use only
`thm_7_1_4`, and not the Lean theorems or any hypothesis. The `type_of%` theorems only discard the
`PlattGRH` instance binder, and they check that the hand-written statements of the cores are,
definitionally, the Lean statements.

**The `q = 1` theorem is incomparable with [H]'s sharper `q = 1` bound.** The bounds
`4.772·10⁻¹¹ + 251400/√x` and `10⁻¹⁸ + 6.24·10⁶/√x` cross at
`√x = 5988600/(4.772·10⁻¹¹ − 10⁻¹⁸) ≈ 1.25495·10¹⁷`, that is at `x ≈ 1.5749·10³⁴`, which lies in
the common range `x ≥ 4.9·10²⁶`. `thm_7_1_4_one_bounds_incomparable` proves two witnesses:
* at `x = 10²⁸`, [H] gives `2.56172·10⁻⁹` and Lean gives `6.24·10⁻⁸`, so [H] is sharper;
* at `x = 10³⁶`, [H] gives `4.79714·10⁻¹¹` and Lean gives `6.240001·10⁻¹²`, so Lean is sharper.

So neither bound implies the other, and `thm_7_1_4 → type_of% @thm_7_1_4_one` cannot be obtained
by comparing bounds. (Since `thm_7_1_4_one` is proved, the implication holds trivially by quoting
it, but that certifies nothing.) Two partial results hold:
* `thm_7_1_4_implies_formal_one_of_le`. [H] implies the conclusion of `thm_7_1_4_one` for
  `4.9·10²⁶ ≤ x ≤ 1.5·10³⁴`. That conclusion is written `Thm_7_1_4.formalOneAt x`, and
  `thm_7_1_4_formal_one_iff` proves by `Iff.rfl` that, quantified over `x ≥ 4.9·10²⁶` and the
  `Fact PlattGRH` instance, it is the statement of `thm_7_1_4_one`.
* `thm_7_1_4_holds_one_of_ge`. Conversely, `thm_7_1_4_one` proves [H]'s statement for `q = 1`,
  with both bounds, for `x ≥ 1.6·10³⁴`.

(At `q = 1`, `thm_7_1_4_odd` gives `7.5·10⁻⁸ + 7.7·10⁶/√x`, which [H] implies.)

**Checks on the transcription.**
* `Thm_7_1_4.fourierHat_eq_fourier` and `Thm_7_1_4.sum_eq_Schar` show that the book's `η̂` and the
  book's series are the repository's.
* `Thm_7_1_4.summable_norm` and `Thm_7_1_4.integrable_integrand` show that the series and the
  Fourier integral converge absolutely. So the `tsum` and the Bochner integral are the true sum
  and integral.
* `thm_7_1_4_concl_iff` shows that the existential `E` is a real constraint.
* `thm_7_1_4_hyps_satisfiable` and `thm_7_1_4_hyps_satisfiable_ge_two` show that the hypotheses
  can be met, with `q = 1` and with some `q ≥ 2`.
-/

open Real MeasureTheory FourierTransform
open scoped ArithmeticFunction.vonMangoldt

namespace Companion.Book

open TernaryGoldbach (e Schar PlattGRH)
open TernaryGoldbach.Helfgott (etaPlus)

namespace Thm_7_1_4

/-- The Fourier transform with the normalization of [H, §2.3]: `f̂(t) = ∫_{−∞}^{∞} e(−xt) f(x) dx`,
where `e(u) = exp(2πiu)` is `TernaryGoldbach.e`. It agrees with Mathlib's `𝓕`
(`fourierHat_eq_fourier`). -/
noncomputable def fourierHat (f : ℝ → ℂ) (t : ℝ) : ℂ :=
  ∫ y : ℝ, e (-(y * t)) * f y

/-- [H]'s Fourier transform is Mathlib's `𝓕`, for every `f` (both are the same Bochner integral). -/
theorem fourierHat_eq_fourier (f : ℝ → ℂ) (t : ℝ) : fourierHat f t = 𝓕 f t := by
  rw [Real.fourier_real_eq_integral_exp_smul]
  unfold fourierHat
  congr 1
  ext y
  rw [smul_eq_mul, TernaryGoldbach.e]
  congr 2
  push_cast
  ring

end Thm_7_1_4

open Thm_7_1_4

/-- The conclusion of [H, Theorem 7.1.4] for given `x`, `q`, `χ`, `δ`:
`Σ_{n=1}^∞ Λ(n) χ(n) e(δn/x) η(n/x) = I_{q=1} · η̂(−δ) · x + E · x` with
`|E| ≤ 1.3482·10⁻¹⁴ + 1.617·10⁻¹⁰/q + (1/√x)(499900/√q + 52)`, and also
`|E| ≤ 4.772·10⁻¹¹ + 251400/√x` if `q = 1`.

How it is transcribed:
* The series is `∑' n : ℕ+` (that is, `n = 1, 2, …`) of `Λ(n) χ(n) e(δ/x · n) η₊(n/x)`. Here `Λ`
  is Mathlib's `ArithmeticFunction.vonMangoldt`, `e(u) = exp(2πiu)` is `TernaryGoldbach.e` and
  `χ(n)` is `χ (n : ZMod q)`. The series converges absolutely (`Thm_7_1_4.summable_norm`), so the
  `tsum` is its sum. It is the repository's `Schar χ (n ↦ Λ(n) η₊(n/x)) (δ/x)`
  (`Thm_7_1_4.sum_eq_Schar`).
* `η̂` is `Thm_7_1_4.fourierHat`, the normalization `f̂(t) = ∫ e(−xt) f(x) dx` of [H, §2.3],
  evaluated at `−δ`. Its integrand is integrable (`Thm_7_1_4.integrable_integrand`).
* `I_{q=1}` is `if q = 1 then 1 else 0`.
* [H] defines `E` through the identity, so `E` becomes `∃ E : ℂ, identity ∧ ‖E‖ ≤ …`. `E` is
  complex, because the sum is, and `|E|` is its modulus `‖E‖`. Since `x > 0`, the identity
  determines `E`, so this is [H]'s claim and not a weakening (`thm_7_1_4_concl_iff`). The sharper
  `q = 1` bound is the clause `q = 1 → ‖E‖ ≤ …` on the same `E`.
* The constants are copied verbatim: `1.3482e-14`, `1.617e-10`, `499900`, `52`, `4.772e-11`,
  `251400`. `√` is `Real.sqrt`. -/
def thm_7_1_4_concl (x : ℝ) (q : ℕ) (χ : DirichletCharacter ℂ q) (δ : ℝ) : Prop :=
  ∃ E : ℂ,
    ∑' n : ℕ+, (Λ n : ℂ) * χ n * e (δ / x * n) * (etaPlus (n / x) : ℂ) =
        (if q = 1 then 1 else 0) * fourierHat (fun t => (etaPlus t : ℂ)) (-δ) * x + E * x ∧
      ‖E‖ ≤ 1.3482e-14 + 1.617e-10 / q + 1 / √x * (499900 / √q + 52) ∧
      (q = 1 → ‖E‖ ≤ 4.772e-11 + 251400 / √x)

/-- **[H, Theorem 7.1.4]**, as printed (p. 140).

How the statement is transcribed:
* `η = η₊` is the repository's `TernaryGoldbach.Helfgott.etaPlus`,
  `η₊(t) = h₂₀₀(t) · t · e^{−t²/2}`. We checked it against [H, (7.4)–(7.6)]:
  - `hBase` is the `h` of (7.5);
  - `F H y = sin(H log y)/(π log y)` is the `F_H` of (7.6). (7.6) writes `F_H(t)` and
    `(h *_M F_H)(y)`, typos for `F_H(y)` and `(h *_M F_H)(t)`;
  - `hH H t = ∫_{y>0} h(t/y) F_H(y) dy/y` is `h_H`;
  - `H = 200` is fixed inside `etaPlus`.

  The integral defining `h_H(t)` converges absolutely, because `|F_H| ≤ H/π` and
  `∫₀² |h(u)| du/u < ∞`. So Lean's Bochner integral is [H]'s integral. At `y = 1`, Lean's `F` takes
  the value `0/0 = 0` rather than the limit `H/π`; this is a single point and does not change the
  integral.
* "Let `x` be a real number `≥ 10¹²`" becomes `∀ x : ℝ, 10 ^ 12 ≤ x → …`.
* "Let `χ` be a primitive character mod `q`, where `1 ≤ q ≤ 150000` if `q` is odd, and
  `1 ≤ q ≤ 300000` if `q` is even" becomes the following. `q : ℕ`, with the two conditions as the
  implications `Odd q → 1 ≤ q ∧ q ≤ 150000` and `Even q → 1 ≤ q ∧ q ≤ 300000` (so `q = 0` is
  excluded). `χ : DirichletCharacter ℂ q` with Mathlib's `χ.IsPrimitive` (conductor `q`). Then
  `χ(n) = χ (n : ZMod q)`, which is `0` when `gcd(n, q) > 1`.
* "for any `δ ∈ ℝ` with `|δ| ≤ 600000 · gcd(q,2)/q`" becomes
  `∀ δ : ℝ, |δ| ≤ 600000 * (Nat.gcd q 2 : ℝ) / q → …`.
* The identity, `E`, `I_{q=1}` and the two bounds are `thm_7_1_4_concl x q χ δ` (see there).

The hypotheses can be met, with `q = 1` (`thm_7_1_4_hyps_satisfiable`) and with some `q ≥ 2`
(`thm_7_1_4_hyps_satisfiable_ge_two`). The conclusion is a real bound on a specific complex number
(`thm_7_1_4_concl_iff`). -/
def thm_7_1_4 : Prop :=
  ∀ x : ℝ, 10 ^ 12 ≤ x →
    ∀ q : ℕ, (Odd q → 1 ≤ q ∧ q ≤ 150000) → (Even q → 1 ≤ q ∧ q ≤ 300000) →
      ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
        ∀ δ : ℝ, |δ| ≤ 600000 * (Nat.gcd q 2 : ℝ) / q →
          thm_7_1_4_concl x q χ δ

namespace Thm_7_1_4

/-- The book's series is the repository's `Schar χ (n ↦ Λ(n) η₊(n/x)) (δ/x)`. The `n = 0` term of
`Schar` is `0`, because `Λ(0) = 0`. -/
theorem sum_eq_Schar (x : ℝ) {q : ℕ} (χ : DirichletCharacter ℂ q) (δ : ℝ) :
    ∑' n : ℕ+, (Λ n : ℂ) * χ n * e (δ / x * n) * (etaPlus (n / x) : ℂ) =
      Schar χ (fun n => ((Λ n * etaPlus (n / x) : ℝ) : ℂ)) (δ / x) := by
  rw [tsum_pnat_eq_tsum_of_eq_zero
    (f := fun n : ℕ => (Λ n : ℂ) * χ n * e (δ / x * n) * (etaPlus (n / x) : ℂ)) (by simp)]
  unfold Schar
  congr 1
  ext n
  push_cast
  rw [mul_comm (δ / x) (n : ℝ)]
  ring

/-- The book's series converges absolutely for `x > 0`, so its `tsum` is its sum. This follows from
`TernaryGoldbach.Helfgott.summable_etaPlus`, which has no hypotheses. -/
theorem summable_norm {x : ℝ} (hx : 0 < x) {q : ℕ} (χ : DirichletCharacter ℂ q) (δ : ℝ) :
    Summable fun n : ℕ+ => ‖(Λ n : ℂ) * χ n * e (δ / x * n) * (etaPlus (n / x) : ℂ)‖ := by
  have h := (TernaryGoldbach.Helfgott.summable_etaPlus hx).comp_injective PNat.coe_injective
  refine Summable.of_nonneg_of_le (fun _ => norm_nonneg _) (fun n => ?_) h
  simp only [Function.comp_apply, norm_mul, TernaryGoldbach.norm_e, mul_one, Complex.norm_real]
  exact mul_le_mul_of_nonneg_right (mul_le_of_le_one_right (norm_nonneg _) (χ.norm_le_one _))
    (norm_nonneg _)

/-- The integrand of `η̂₊(t)` is integrable, so `fourierHat` of `η₊` is a true integral. This
follows from `TernaryGoldbach.MajorArcs.integrable_etaPlus`, which has no hypotheses. -/
theorem integrable_integrand (t : ℝ) : Integrable fun y : ℝ => e (-(y * t)) * (etaPlus y : ℂ) :=
  TernaryGoldbach.MajorArcs.integrable_etaPlus.ofReal.bdd_mul
    (TernaryGoldbach.continuous_e.comp (by fun_prop)).aestronglyMeasurable
    (Filter.Eventually.of_forall fun y => (TernaryGoldbach.norm_e _).le)

/-- An error term `E` with `S = M + E · x`, `‖E‖ ≤ B` and (if `P`) `‖E‖ ≤ B'` exists if and only if
`‖S − M‖ ≤ B · x` and (if `P`) `‖S − M‖ ≤ B' · x`, when `x > 0`. -/
theorem err_iff {S M : ℂ} {x B B' : ℝ} {P : Prop} (hx : 0 < x) :
    (∃ E : ℂ, S = M + E * x ∧ ‖E‖ ≤ B ∧ (P → ‖E‖ ≤ B')) ↔
      ‖S - M‖ ≤ B * x ∧ (P → ‖S - M‖ ≤ B' * x) := by
  have hn : ‖(x : ℂ)‖ = x := by rw [Complex.norm_real, Real.norm_of_nonneg hx.le]
  constructor
  · rintro ⟨E, rfl, h1, h2⟩
    rw [add_sub_cancel_left, norm_mul, hn]
    exact ⟨mul_le_mul_of_nonneg_right h1 hx.le, fun hP => mul_le_mul_of_nonneg_right (h2 hP) hx.le⟩
  · rintro ⟨h1, h2⟩
    have hx0 : (x : ℂ) ≠ 0 := by exact_mod_cast hx.ne'
    have hE : ‖(S - M) / (x : ℂ)‖ = ‖S - M‖ / x := by rw [norm_div, hn]
    refine ⟨(S - M) / x, by rw [div_mul_cancel₀ _ hx0]; ring, ?_, fun hP => ?_⟩
    · rw [hE, div_le_iff₀ hx]; exact h1
    · rw [hE, div_le_iff₀ hx]; exact h2 hP

/-- The book's series minus the book's main term `I_{q=1} η̂(−δ) x` is the formalization's
`Schar … − (if q = 1 then 𝓕 η₊ (−δ) · x else 0)`. -/
theorem book_sub_eq (x : ℝ) {q : ℕ} (χ : DirichletCharacter ℂ q) (δ : ℝ) :
    (∑' n : ℕ+, (Λ n : ℂ) * χ n * e (δ / x * n) * (etaPlus (n / x) : ℂ)) -
        (if q = 1 then 1 else 0) * fourierHat (fun t => (etaPlus t : ℂ)) (-δ) * x =
      Schar χ (fun n => ((Λ n * etaPlus (n / x) : ℝ) : ℂ)) (δ / x) -
        (if q = 1 then 𝓕 (fun u => (etaPlus u : ℂ)) (-δ) * x else 0) := by
  rw [sum_eq_Schar, fourierHat_eq_fourier]
  split_ifs <;> ring

/-- [H]'s general bound, for `1 ≤ q ≤ 300000` and `x > 0`, is at most the formalization's
`(7.5·10⁻⁸ + 7.7·10⁶/√x)/√q`. Multiplied by `√q ∈ [1, 548]`, the left side is
`1.3482·10⁻¹⁴ √q + 1.617·10⁻¹⁰/√q + (499900 + 52 √q)/√x`. -/
theorem book_bound_le {q x : ℝ} (hq1 : 1 ≤ q) (hq : q ≤ 300000) (hx : 0 < x) :
    1.3482e-14 + 1.617e-10 / q + 1 / √x * (499900 / √q + 52) ≤ (7.5e-8 + 7.7e6 / √x) / √q := by
  have hs1 : 1 ≤ √q := Real.one_le_sqrt.mpr hq1
  have hs2 : √q ≤ 548 := (Real.sqrt_le_left (by norm_num)).mpr (by linarith)
  have hsq : √q * √q = q := Real.mul_self_sqrt (by linarith)
  have ht : 0 < √x := Real.sqrt_pos.mpr hx
  have hq' : 1.617e-10 / q = 1.617e-10 / (√q * √q) := by rw [hsq]
  rw [hq']
  set s := √q
  set t := √x
  have hs0 : 0 < s := by linarith
  have key : (7.5e-8 + 7.7e6 / t) / s -
      (1.3482e-14 + 1.617e-10 / (s * s) + 1 / t * (499900 / s + 52)) =
      ((7.5e-8 * s - 1.3482e-14 * s * s - 1.617e-10) * t + (7.7e6 - 499900 - 52 * s) * s) /
        (s * s * t) := by
    field_simp
    ring
  have h1 : 0 ≤ 7.5e-8 * s - 1.3482e-14 * s * s - 1.617e-10 := by nlinarith
  have h2 : 0 ≤ 7.7e6 - 499900 - 52 * s := by linarith
  have : 0 ≤ ((7.5e-8 * s - 1.3482e-14 * s * s - 1.617e-10) * t + (7.7e6 - 499900 - 52 * s) * s) /
      (s * s * t) := by positivity
  linarith

/-- **[H] ⇒ `thm_7_1_4_odd`**, stated by hand with no `Fact` instance in scope. So the proof cannot
use the Lean theorem or any hypothesis. `thm_7_1_4_implies_formal_odd` checks that this statement is
the Lean one. -/
theorem implies_odd_core (h : thm_7_1_4) {x : ℝ} (hx : 4.9e26 ≤ x) {q : ℕ} [NeZero q]
    (hodd : Odd q) (hq : q ≤ 150000) (χ : DirichletCharacter ℂ q) (hχ : χ.IsPrimitive) {δ : ℝ}
    (hδ : |δ| ≤ 600000 / q) :
    ‖Schar χ (fun n => ((Λ n * etaPlus (n / x) : ℝ) : ℂ)) (δ / x) -
        (if q = 1 then 𝓕 (fun u => (etaPlus u : ℂ)) (-δ) * x else 0)‖ ≤
      ((7.5e-8 + 7.7e6 / √x) / √q) * x := by
  have hx0 : 0 < x := by linarith
  have hq1 : 1 ≤ q := Nat.one_le_iff_ne_zero.mpr (NeZero.ne q)
  have hg : Nat.gcd q 2 = 1 := hodd.coprime_two_right
  have hc := h x (by linarith) q (fun _ => ⟨hq1, hq⟩) (fun _ => ⟨hq1, by omega⟩) χ hχ δ
    (by rw [hg]; simpa using hδ)
  obtain ⟨hb, -⟩ := (err_iff hx0).mp hc
  rw [book_sub_eq] at hb
  refine hb.trans (mul_le_mul_of_nonneg_right ?_ hx0.le)
  exact book_bound_le (by exact_mod_cast hq1) (by exact_mod_cast hq.trans (by norm_num)) hx0

/-- **[H] ⇒ `thm_7_1_4_even`**, stated by hand with no `Fact` instance in scope (see
`implies_odd_core`). `thm_7_1_4_implies_formal_even` checks that this statement is the Lean one. -/
theorem implies_even_core (h : thm_7_1_4) {x : ℝ} (hx : 4.9e26 ≤ x) {q : ℕ} [NeZero q]
    (heven : Even q) (hq : q ≤ 300000) (χ : DirichletCharacter ℂ q) (hχ : χ.IsPrimitive) {δ : ℝ}
    (hδ : |δ| ≤ 1200000 / q) :
    ‖Schar χ (fun n => ((Λ n * etaPlus (n / x) : ℝ) : ℂ)) (δ / x) -
        (if q = 1 then 𝓕 (fun u => (etaPlus u : ℂ)) (-δ) * x else 0)‖ ≤
      ((7.5e-8 + 7.7e6 / √x) / √q) * x := by
  have hx0 : 0 < x := by linarith
  have hq1 : 1 ≤ q := Nat.one_le_iff_ne_zero.mpr (NeZero.ne q)
  have hg : Nat.gcd q 2 = 2 := Nat.gcd_eq_right (even_iff_two_dvd.mp heven)
  have hc := h x (by linarith) q (fun hodd => absurd heven (Nat.not_even_iff_odd.mpr hodd))
    (fun _ => ⟨hq1, hq⟩) χ hχ δ (by rw [hg]; convert hδ using 1; push_cast; ring)
  obtain ⟨hb, -⟩ := (err_iff hx0).mp hc
  rw [book_sub_eq] at hb
  refine hb.trans (mul_le_mul_of_nonneg_right ?_ hx0.le)
  exact book_bound_le (by exact_mod_cast hq1) (by exact_mod_cast hq) hx0

/-- The conclusion of `TernaryGoldbach.MajorArcs.thm_7_1_4_one` at a fixed `x`. It is copied by
hand, and `thm_7_1_4_formal_one_iff` proves by `Iff.rfl` that it is the Lean statement. -/
def formalOneAt (x : ℝ) : Prop :=
  ∀ (χ : DirichletCharacter ℂ 1) {δ : ℝ}, |δ| ≤ 600000 →
    ‖Schar χ (fun n => ((Λ n * etaPlus (n / x) : ℝ) : ℂ)) (δ / x) -
        𝓕 (fun u => (etaPlus u : ℂ)) (-δ) * x‖ ≤ (1e-18 + 6.24e6 / √x) * x

/-- For `4.9·10²⁶ ≤ x ≤ 1.5·10³⁴`, [H]'s sharper `q = 1` bound is at most the formalization's. -/
theorem one_bound_le_formal_of_le {x : ℝ} (hx : 4.9e26 ≤ x) (hx' : x ≤ 1.5e34) :
    4.772e-11 + 251400 / √x ≤ 1e-18 + 6.24e6 / √x := by
  have ht : 0 < √x := Real.sqrt_pos.mpr (by linarith)
  have ht' : √x ≤ 1.2248e17 := (Real.sqrt_le_left (by norm_num)).mpr (by linarith)
  have : 4.772e-11 - 1e-18 ≤ 5988600 / √x := by
    rw [le_div_iff₀ ht]; nlinarith
  have e : 6.24e6 / √x - 251400 / √x = 5988600 / √x := by rw [← sub_div]; norm_num
  linarith

/-- For `x ≥ 1.6·10³⁴`, the formalization's `q = 1` bound is at most [H]'s sharper one. -/
theorem formal_le_one_bound_of_ge {x : ℝ} (hx : 1.6e34 ≤ x) :
    1e-18 + 6.24e6 / √x ≤ 4.772e-11 + 251400 / √x := by
  have ht' : 1.26e17 ≤ √x := (Real.le_sqrt (by norm_num) (by linarith)).mpr (by linarith)
  have ht : 0 < √x := by linarith
  have : 5988600 / √x ≤ 4.772e-11 - 1e-18 := by
    rw [div_le_iff₀ ht]; nlinarith
  have e : 6.24e6 / √x - 251400 / √x = 5988600 / √x := by rw [← sub_div]; norm_num
  linarith

end Thm_7_1_4

/-! ## Non-vacuity -/

/-- **Non-vacuity check.** The existential error term of `thm_7_1_4_concl` is a real constraint.
For `x > 0` the conclusion is equivalent to two explicit inequalities on the book's series minus its
main term. -/
theorem thm_7_1_4_concl_iff {x : ℝ} (hx : 0 < x) (q : ℕ) (χ : DirichletCharacter ℂ q) (δ : ℝ) :
    thm_7_1_4_concl x q χ δ ↔
      ‖(∑' n : ℕ+, (Λ n : ℂ) * χ n * e (δ / x * n) * (etaPlus (n / x) : ℂ)) -
          (if q = 1 then 1 else 0) * fourierHat (fun t => (etaPlus t : ℂ)) (-δ) * x‖ ≤
        (1.3482e-14 + 1.617e-10 / q + 1 / √x * (499900 / √q + 52)) * x ∧
      (q = 1 → ‖(∑' n : ℕ+, (Λ n : ℂ) * χ n * e (δ / x * n) * (etaPlus (n / x) : ℂ)) -
          (if q = 1 then 1 else 0) * fourierHat (fun t => (etaPlus t : ℂ)) (-δ) * x‖ ≤
        (4.772e-11 + 251400 / √x) * x) :=
  err_iff hx

/-- **Non-vacuity check.** The hypotheses of `thm_7_1_4` can be met: `x = 10¹²`, `q = 1`, the
trivial character (which is primitive), `δ = 0`. -/
theorem thm_7_1_4_hyps_satisfiable :
    (10 : ℝ) ^ 12 ≤ 10 ^ 12 ∧ (Odd 1 → 1 ≤ 1 ∧ 1 ≤ 150000) ∧ (Even 1 → 1 ≤ 1 ∧ 1 ≤ 300000) ∧
      (1 : DirichletCharacter ℂ 1).IsPrimitive ∧ |(0 : ℝ)| ≤ 600000 * (Nat.gcd 1 2 : ℝ) / 1 :=
  ⟨le_rfl, fun _ => ⟨le_rfl, by norm_num⟩, fun _ => ⟨le_rfl, by norm_num⟩,
    DirichletCharacter.isPrimitive_one_level_one, by norm_num⟩

/-- **Non-vacuity check for `q ≥ 2`.** Some `q ≥ 2` in [H]'s range carries a primitive character,
so the part of `thm_7_1_4` with `I_{q=1} = 0` is not vacuous either. The witness is the conductor
`q` of the character `χ₄` mod `4` (as a `ℂ`-valued character), with its primitive character
`χ₄.primitiveCharacter`; since `χ₄ ≠ 1` and `q ∣ 4`, `2 ≤ q ≤ 4`. -/
theorem thm_7_1_4_hyps_satisfiable_ge_two :
    ∃ q : ℕ, 2 ≤ q ∧ (Odd q → 1 ≤ q ∧ q ≤ 150000) ∧ (Even q → 1 ≤ q ∧ q ≤ 300000) ∧
      ∃ χ : DirichletCharacter ℂ q, χ.IsPrimitive := by
  let χ : DirichletCharacter ℂ 4 := ZMod.χ₄.ringHomComp (Int.castRingHom ℂ)
  have h3 : χ 3 = -1 := by
    simp only [χ, MulChar.ringHomComp_apply]
    have : ZMod.χ₄ ((3 : ℕ) : ZMod 4) = -1 := ZMod.χ₄_nat_three_mod_four rfl
    simp only [Nat.cast_ofNat] at this
    rw [this]; simp
  have hne : χ ≠ 1 := by
    intro h
    have hu : IsUnit (3 : ZMod 4) := IsUnit.of_mul_eq_one (3 : ZMod 4) (by decide)
    have := congrArg (fun ψ : DirichletCharacter ℂ 4 => ψ 3) h
    simp only [MulChar.one_apply hu, h3] at this
    norm_num at this
  have hc1 : χ.conductor ≠ 1 := fun h => hne (DirichletCharacter.eq_one_iff_conductor_eq_one.mpr h)
  have hc0 : χ.conductor ≠ 0 := DirichletCharacter.conductor_ne_zero χ
  have hle : χ.conductor ≤ 4 :=
    Nat.le_of_dvd (by norm_num) (DirichletCharacter.conductor_dvd_level χ)
  exact ⟨χ.conductor, by omega, fun _ => ⟨by omega, by omega⟩, fun _ => ⟨by omega, by omega⟩,
    χ.primitiveCharacter, DirichletCharacter.primitiveCharacter_isPrimitive χ⟩

/-! ## [H] implies the formal theorems for odd and even `q` -/

/-- **[H, Thm 7.1.4] ⇒ `TernaryGoldbach.MajorArcs.thm_7_1_4_odd`.** For odd `q ≤ 150000` (`q = 1`
included), [H]'s bound `1.3482·10⁻¹⁴ + 1.617·10⁻¹⁰/q + (499900/√q + 52)/√x` (for `x ≥ 10¹²`) gives
the Lean bound `(7.5·10⁻⁸ + 7.7·10⁶/√x)/√q` (for `x ≥ 4.9·10²⁶`). The `δ`-ranges agree, because
`gcd(q, 2) = 1`. The proof is `Thm_7_1_4.implies_odd_core`, which has no `Fact` instance in
scope. -/
theorem thm_7_1_4_implies_formal_odd :
    thm_7_1_4 → type_of% @TernaryGoldbach.MajorArcs.thm_7_1_4_odd :=
  fun h _ => implies_odd_core h

/-- **[H, Thm 7.1.4] ⇒ `TernaryGoldbach.MajorArcs.thm_7_1_4_even`.** The same bound comparison for
even `q ≤ 300000`. The `δ`-ranges agree, because `600000 · gcd(q, 2)/q = 1200000/q`. The proof is
`Thm_7_1_4.implies_even_core`, which has no `Fact` instance in scope. -/
theorem thm_7_1_4_implies_formal_even :
    thm_7_1_4 → type_of% @TernaryGoldbach.MajorArcs.thm_7_1_4_even :=
  fun h _ => implies_even_core h

/-! ## The `q = 1` theorem: incomparable bounds -/

/-- `Thm_7_1_4.formalOneAt x` is the conclusion of `TernaryGoldbach.MajorArcs.thm_7_1_4_one` at `x`.
The statement of the Lean theorem is taken with `type_of%` and the two sides agree by `Iff.rfl`. -/
theorem thm_7_1_4_formal_one_iff :
    (∀ [Fact PlattGRH] {x : ℝ},
        4.9e26 ≤ x → formalOneAt x) ↔
      type_of% @TernaryGoldbach.MajorArcs.thm_7_1_4_one :=
  Iff.rfl

/-- **Incomparability witness for `q = 1`.** [H]'s sharper bound `4.772·10⁻¹¹ + 251400/√x` and the
formal `10⁻¹⁸ + 6.24·10⁶/√x` (from `thm_7_1_4_one`) cross inside the common range `x ≥ 4.9·10²⁶`.
At `x = 10²⁸` (`√x = 10¹⁴`), [H]'s is smaller: `2.56172·10⁻⁹ < 6.24·10⁻⁸`. At `x = 10³⁶`
(`√x = 10¹⁸`), the formal one is smaller: `6.240001·10⁻¹² < 4.79714·10⁻¹¹`. So neither bound implies
the other. -/
theorem thm_7_1_4_one_bounds_incomparable :
    (4.772e-11 + 251400 / √(1e28 : ℝ) < 1e-18 + 6.24e6 / √(1e28 : ℝ)) ∧
      (1e-18 + 6.24e6 / √(1e36 : ℝ) < 4.772e-11 + 251400 / √(1e36 : ℝ)) := by
  have h28 : √(1e28 : ℝ) = 1e14 := by
    rw [show (1e28 : ℝ) = (1e14) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  have h36 : √(1e36 : ℝ) = 1e18 := by
    rw [show (1e36 : ℝ) = (1e18) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  rw [h28, h36]
  constructor <;> norm_num

/-- **[H] implies `thm_7_1_4_one` below the crossover.** For `4.9·10²⁶ ≤ x ≤ 1.5·10³⁴`, [H]'s
sharper `q = 1` bound gives the conclusion of `TernaryGoldbach.MajorArcs.thm_7_1_4_one` (that is,
`formalOneAt x`; see `thm_7_1_4_formal_one_iff`). The bounds cross at `x ≈ 1.5749·10³⁴`. The proof
uses no `Fact` instance. -/
theorem thm_7_1_4_implies_formal_one_of_le :
    thm_7_1_4 → ∀ x : ℝ, 4.9e26 ≤ x → x ≤ 1.5e34 → formalOneAt x := by
  intro h x hx hx' χ δ hδ
  have hx0 : 0 < x := by linarith
  have hχ : χ.IsPrimitive := by
    rw [Subsingleton.elim χ 1]; exact DirichletCharacter.isPrimitive_one_level_one
  have hc := h x (by linarith) 1 (fun _ => ⟨le_rfl, by norm_num⟩) (fun _ => ⟨le_rfl, by norm_num⟩)
    χ hχ δ (by simpa using hδ)
  obtain ⟨-, hb⟩ := (err_iff hx0).mp hc
  have hb := hb rfl
  rw [book_sub_eq, ite_eq_left rfl] at hb
  exact hb.trans (mul_le_mul_of_nonneg_right (one_bound_le_formal_of_le hx hx') hx0.le)

/-- **The formalization proves [H, Thm 7.1.4] for `q = 1` above the crossover.** Given the `Fact`
hypothesis `PlattGRH` of `TernaryGoldbach.MajorArcs.thm_7_1_4_one`, [H]'s statement
holds for `q = 1`, with both of its bounds, for all `x ≥ 1.6·10³⁴`. The binders are those of
`thm_7_1_4` at `q = 1`, except that `χ.IsPrimitive` is dropped because it always holds mod `1`. -/
theorem thm_7_1_4_holds_one_of_ge [Fact PlattGRH] :
    ∀ x : ℝ, 1.6e34 ≤ x → ∀ χ : DirichletCharacter ℂ 1,
      ∀ δ : ℝ, |δ| ≤ 600000 * (Nat.gcd 1 2 : ℝ) / 1 → thm_7_1_4_concl x 1 χ δ := by
  intro x hx χ δ hδ
  have hx0 : 0 < x := by linarith
  have hF := TernaryGoldbach.MajorArcs.thm_7_1_4_one (by linarith : (4.9e26 : ℝ) ≤ x) χ
    (by simpa using hδ)
  have hS := book_sub_eq x χ δ
  have hite : (if (1 : ℕ) = 1 then 𝓕 (fun u => (etaPlus u : ℂ)) (-δ) * x else 0) =
      𝓕 (fun u => (etaPlus u : ℂ)) (-δ) * x := ite_eq_left rfl
  rw [hite] at hS
  rw [← hS] at hF
  have hE := hF.trans (mul_le_mul_of_nonneg_right (formal_le_one_bound_of_ge hx) hx0.le)
  refine (err_iff hx0).mpr ⟨hE.trans (mul_le_mul_of_nonneg_right ?_ hx0.le), fun _ => hE⟩
  have ht : 0 < √x := Real.sqrt_pos.mpr hx0
  simp only [Nat.cast_one, Real.sqrt_one, div_one]
  have h1 : 1 / √x * (499900 + 52) = 499952 / √x := by ring
  have h2 : 251400 / √x ≤ 499952 / √x := div_le_div_of_nonneg_right (by norm_num) ht.le
  linarith

end Companion.Book
