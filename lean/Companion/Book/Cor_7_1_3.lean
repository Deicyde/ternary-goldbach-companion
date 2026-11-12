import TernaryGoldbach

/-!
# [H, Corollary 7.1.3]: twisted prime sums with the weight `η = (t² e^{-t²/2}) *_M η₂`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §7.1
("Results"), Corollary 7.1.3 (label `cor:coprar`), printed page 139
(<https://arxiv.org/pdf/1501.05438v2#page=149>):

> Let `η(t) = t² e^{-t²/2} *_M η₂(t)`, where `η₂ = η₁ *_M η₁` and `η₁ = 2 · I_{[1/2,1]}`. Let `x` be
> a real number `≥ 10⁸`. Let `χ` be a primitive character mod `q`, `1 ≤ q ≤ r`, where `r = 300000`.
> Then, for any `δ ∈ ℝ` with `|δ| ≤ 4r/q`,
> `∑_{n=1}^∞ Λ(n) χ(n) e((δ/x) n) η(n/x) = I_{q=1} · η̂(-δ) · x + E · x`,
> where `I_{q=1} = 1` if `q = 1`, `I_{q=1} = 0` if `q ≠ 1`, and
> `|E| ≤ 2.485·10⁻¹⁹ + (1/√x) (381500/√q + 76)`.

The book proves it in §9.6 (p. 195), from Cor. 9.3.3 with `T₀ = 10⁸/q`. The input is D. Platt's
verification of GRH for conductors `q ≤ 3·10⁵` up to height `10⁸/q`, which the book quotes as
established, so the printed statement has no hypothesis. The book uses it only at `x/κ ≥ 10²⁵`
((14.16)–(14.17) and before (14.23)). The 2013 major-arcs preprint (arXiv:1305.2897v4, Cor. 1.3)
had `|E| ≤ 4.269·10⁻¹⁴/q + (1/√x) (380600/√q + 76)` instead.

**What the formalization proves.** `TernaryGoldbach.MajorArcs.cor_7_1_3'`
(`TernaryGoldbach/MajorArcs/Cor713.lean:807`; restated with the same statement as
`TernaryGoldbach.MinorArcs.cor_7_1_3`, `TernaryGoldbach/MinorArcs/PartIICited.lean:45`). For
`y ≥ 10²⁵`, `q ≤ 300000` with `[NeZero q]`, `χ` primitive mod `q` and `|δ| ≤ 4·300000/q`:
`‖Schar χ (n ↦ Λ(n) etaU(n/y)) (δ/y) - (if q = 1 then 𝓕 etaU (-δ) · y else 0)‖
  ≤ (10⁻¹⁷ + 4.7·10⁶/√q/√y) · y`.
Here `etaU` is the repo's `η₂ *_M φ` and `𝓕` is Mathlib's Fourier transform. The proof follows
the book (Cor. 9.3.3 at `T₀ = 10⁸/q` with Platt's verification). The theorem carries one `Fact`
hypothesis, `PlattGRH`, which is Platt's verification (`companion/data/hypothesis_trace.json`).

**Relation: implied.** The book's statement implies the Lean one. This is certified by
`cor_7_1_3_implies_formal : cor_7_1_3 → type_of% @TernaryGoldbach.MajorArcs.cor_7_1_3'`, and by
`cor_7_1_3_implies_formal_minorArcs` for the restatement. The Lean statement is weaker in two ways:
* range: `y ≥ 10²⁵` instead of `x ≥ 10⁸`. This is the range the book's own application needs;
* constants: `√q ≤ 548` for `q ≤ 3·10⁵`, so `(381500/√q + 76)/√x ≤ 423148/(√q √x)`. This is below
  Lean's `4.7·10⁶/(√q √x)`, and `2.485·10⁻¹⁹ ≤ 10⁻¹⁷` (`cor_7_1_3_bound_le`).

The Lean bound is more than 11 times the book's at every admissible `(q, y)`: the ratio is at
least `min(10⁻¹⁷/(2.485·10⁻¹⁹), 4.7·10⁶/(381500 + 76√q)) ≥ 11.1`. For example, at `q = 1`,
`y = 10²⁵` it is `1.486·10⁻⁶` against `1.207·10⁻⁷` (the book's value, used before (14.23)), and at
`q = 300000`, `y = 10²⁵` it is `2.714·10⁻⁹` against `2.443·10⁻¹⁰`. So the converse cannot be
obtained from the Lean theorem. The `Fact` hypothesis of the Lean theorem is a `∀ [Fact …]` binder
of the implication's target. The implication only compares the two statements, so it does not use
them. Its proof does not use the Lean theorem either.

**The book's objects, rebuilt here.** They are defined from the printed definitions and identified
with the repo's objects:
* `cor_7_1_3_eta2_eq`: `η₁ *_M η₁` equals the repo's closed form `TernaryGoldbach.Helfgott.eta2`
  (`4 max(log 2 - |log 2t|, 0)` for `t > 0`, `0` otherwise) at every real `t`. The convolution
  integral is computed exactly;
* `cor_7_1_3_eta_eq_etaU`: the book's `η` is `TernaryGoldbach.MinorArcs.etaU`;
* `cor_7_1_3_hat_eq_fourier`: the book's `η̂` (normalized `f̂(t) = ∫ e(-xt) f(x) dx`, [H, §2.3]) is
  Mathlib's `𝓕` of `etaU`;
* `cor_7_1_3_sum_eq_Schar`: the printed series over `n ≥ 1` is the repo's `Schar` at `δ/x`.

**Non-vacuity.** `cor_7_1_3_hyps_satisfiable` shows that `x = 10⁸`, `q = 1`, the trivial
character and `δ = 0` meet the hypotheses. `cor_7_1_3_eta_pos` shows that `η > 0` on `(0, ∞)`, so
the weight is not identically zero. `cor_7_1_3_eta_of_nonpos` shows that `η = 0` on `(-∞, 0]`: `η`
is a weight on `ℝ⁺` extended by zero, which is how the book takes Fourier transforms of weights on
`ℝ⁺`.
-/

open Real Set MeasureTheory FourierTransform
open scoped ArithmeticFunction.vonMangoldt

namespace Companion.Book

open TernaryGoldbach (e Schar)
open TernaryGoldbach.Helfgott (eta2 phi mellinConv)
open TernaryGoldbach.MinorArcs (etaU)

/-- The book's `η₁ = 2 · I_{[1/2,1]}` ([H, Cor. 7.1.3]; also [H, §2.4]). The indicator is taken of
the closed interval, as printed. `η₁` only enters through the convolution integral defining `η₂`,
so the endpoint convention does not matter. -/
noncomputable def cor_7_1_3_eta1 (t : ℝ) : ℝ := 2 * (Icc (1 / 2 : ℝ) 1).indicator (fun _ => 1) t

/-- The book's `η₂ = η₁ *_M η₁`. The Mellin convolution is the repo's
`TernaryGoldbach.Helfgott.mellinConv`, `(f *_M g)(t) = ∫_{(0,∞)} f(r) g(t/r) dr/r`, which is
[H, (2.7)] verbatim. -/
noncomputable def cor_7_1_3_eta2 : ℝ → ℝ := mellinConv cor_7_1_3_eta1 cor_7_1_3_eta1

/-- The book's `η(t) = t² e^{-t²/2} *_M η₂(t)`, with the factors in the printed order. It is defined
on all of `ℝ` by the convolution formula and vanishes on `(-∞, 0]` (`cor_7_1_3_eta_of_nonpos`). -/
noncomputable def cor_7_1_3_eta : ℝ → ℝ :=
  mellinConv (fun t => t ^ 2 * Real.exp (-t ^ 2 / 2)) cor_7_1_3_eta2

/-- The book's Fourier transform `f̂(t) = ∫_{-∞}^{∞} e(-xt) f(x) dx` ([H, §2.3], repeated in §7.1),
with `e(x) = e^{2πix}` (the repo's `TernaryGoldbach.e`). -/
noncomputable def cor_7_1_3_hat (f : ℝ → ℝ) (t : ℝ) : ℂ := ∫ x : ℝ, e (-(x * t)) * (f x : ℂ)

/-- **[H, Corollary 7.1.3], as printed.**

How the statement is transcribed:
* `η`, `η₂`, `η₁` are the book's objects `cor_7_1_3_eta`, `cor_7_1_3_eta2`, `cor_7_1_3_eta1`,
  built from the printed definitions. `η̂` is `cor_7_1_3_hat cor_7_1_3_eta`, with the book's
  normalization of the Fourier transform. Since `η` vanishes on `(-∞, 0]`, this is the Fourier
  transform of the weight on `ℝ⁺` extended by zero.
* "`x` a real number `≥ 10⁸`": `x : ℝ` with `10 ^ 8 ≤ x`.
* "`χ` a primitive character mod `q`, `1 ≤ q ≤ r`, where `r = 300000`": `q : ℕ` with `1 ≤ q` and
  `q ≤ 300000` (`r` is inlined), and `χ : DirichletCharacter ℂ q` with Mathlib's `χ.IsPrimitive`
  (conductor `= q`). This is the book's notion ([H, §2.2]): a character of `(ℤ/qℤ)*` lifted to `ℤ`,
  vanishing on `n` with `(n, q) ≠ 1`, and not induced by a character of smaller modulus. For `q = 1`
  it is the trivial character, which is primitive.
* "`δ ∈ ℝ` with `|δ| ≤ 4r/q`": `δ : ℝ` with `|δ| ≤ 4 * 300000 / q` in `ℝ`.
* The series `∑_{n=1}^∞` is the `tsum` over `n : ℕ+`, with the factors in the printed order
  `Λ(n) χ(n) e((δ/x) n) η(n/x)`. `Λ` is Mathlib's von Mangoldt function and `χ(n) = χ(n mod q)`.
  The series converges absolutely (`η` has Gaussian decay), so the `tsum` is its sum.
* `I_{q=1}` is `if q = 1 then 1 else 0`.
* `E` is a complex number, quantified after `x, q, χ, δ`, so it may depend on them. It satisfies
  the printed identity `sum = I_{q=1} · η̂(-δ) · x + E · x`, and its modulus `‖E‖` is at most
  `2.485e-19 + 1 / √x * (381500 / √q + 76)`. The decimal literals are exact rationals.
* No hypothesis beyond the printed ones. Platt's verification, which the book's proof uses, is not
  an assumption of the statement. -/
def cor_7_1_3 : Prop :=
  ∀ x : ℝ, 10 ^ 8 ≤ x →
    ∀ q : ℕ, 1 ≤ q → q ≤ 300000 →
      ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
        ∀ δ : ℝ, |δ| ≤ 4 * 300000 / (q : ℝ) →
          ∃ E : ℂ,
            ∑' n : ℕ+, (Λ (n : ℕ) : ℂ) * χ ((n : ℕ) : ZMod q) * e (δ / x * (n : ℕ)) *
                (cor_7_1_3_eta ((n : ℕ) / x) : ℂ) =
              (if q = 1 then 1 else 0) * cor_7_1_3_hat cor_7_1_3_eta (-δ) * x + E * x ∧
            ‖E‖ ≤ 2.485e-19 + 1 / √x * (381500 / √(q : ℝ) + 76)

/-- `η₁ = 2` on `[1/2, 1]`. -/
theorem cor_7_1_3_eta1_of_mem {t : ℝ} (h : t ∈ Icc (1 / 2 : ℝ) 1) : cor_7_1_3_eta1 t = 2 := by
  rw [cor_7_1_3_eta1, indicator_of_mem h, mul_one]

/-- `η₁ = 0` off `[1/2, 1]`. -/
theorem cor_7_1_3_eta1_of_notMem {t : ℝ} (h : t ∉ Icc (1 / 2 : ℝ) 1) : cor_7_1_3_eta1 t = 0 := by
  rw [cor_7_1_3_eta1, indicator_of_notMem h, mul_zero]

/-- The book's `η₂ = η₁ *_M η₁` is the repo's closed form `Helfgott.eta2`, that is
`4 max(log 2 - |log 2t|, 0)` for `t > 0` and `0` for `t ≤ 0`, at every real `t`. For `t > 0` the
integrand is `4/r` on `[max(1/2, t), min(1, 2t)]` and `0` elsewhere, and
`log min(1, 2t) - log max(1/2, t) = log 2 - |log 2t|`. -/
theorem cor_7_1_3_eta2_eq (t : ℝ) : cor_7_1_3_eta2 t = eta2 t := by
  rw [cor_7_1_3_eta2, mellinConv, eta2]
  by_cases ht : 0 < t
  · rw [ite_eq_left ht]
    set a := max (1 / 2 : ℝ) t with ha_def
    set b := min (1 : ℝ) (2 * t) with hb_def
    have ha : 0 < a := lt_max_of_lt_left (by norm_num)
    have hb : 0 < b := lt_min (by norm_num) (by linarith)
    have key : EqOn (fun r => cor_7_1_3_eta1 r * cor_7_1_3_eta1 (t / r) / r)
        ((Icc a b).indicator fun r => 4 / r) (Ioi 0) := by
      intro r hr
      have hr : 0 < r := hr
      simp only
      by_cases h1 : r ∈ Icc (1 / 2 : ℝ) 1
      · by_cases h2 : t / r ∈ Icc (1 / 2 : ℝ) 1
        · have h3 : r ∈ Icc a b := by
            obtain ⟨h1a, h1b⟩ := h1
            obtain ⟨h2a, h2b⟩ := h2
            rw [le_div_iff₀ hr] at h2a
            rw [div_le_iff₀ hr] at h2b
            exact ⟨max_le h1a (by linarith), le_min h1b (by linarith)⟩
          rw [cor_7_1_3_eta1_of_mem h1, cor_7_1_3_eta1_of_mem h2, indicator_of_mem h3]
          ring
        · have h3 : r ∉ Icc a b := by
            rintro ⟨h3a, h3b⟩
            apply h2
            have := min_le_right (1 : ℝ) (2 * t)
            have := le_max_right (1 / 2 : ℝ) t
            constructor
            · rw [le_div_iff₀ hr]; linarith
            · rw [div_le_iff₀ hr]; linarith
          rw [cor_7_1_3_eta1_of_notMem h2, indicator_of_notMem h3]
          ring
      · have h3 : r ∉ Icc a b := by
          rintro ⟨h3a, h3b⟩
          exact h1 ⟨(le_max_left _ _).trans h3a, h3b.trans (min_le_left _ _)⟩
        rw [cor_7_1_3_eta1_of_notMem h1, indicator_of_notMem h3]
        ring
    rw [setIntegral_congr_fun measurableSet_Ioi key, setIntegral_indicator measurableSet_Icc,
      Set.inter_eq_right.mpr (show Icc a b ⊆ Ioi 0 from fun r hr => lt_of_lt_of_le ha hr.1)]
    -- `log b - log a = log 2 - |log 2t|`
    have hid : Real.log b - Real.log a = Real.log 2 - |Real.log (2 * t)| := by
      rcases le_or_gt t (1 / 2) with h | h
      · have ha' : a = 1 / 2 := max_eq_left h
        have hb' : b = 2 * t := min_eq_right (by linarith)
        rw [ha', hb', abs_of_nonpos (Real.log_nonpos (by positivity) (by linarith)),
          show (1 / 2 : ℝ) = 2⁻¹ by norm_num, Real.log_inv]
        ring
      · have ha' : a = t := max_eq_right h.le
        have hb' : b = 1 := min_eq_left (by linarith)
        rw [ha', hb', abs_of_nonneg (Real.log_nonneg (by linarith)),
          Real.log_mul (by norm_num) ht.ne', Real.log_one]
        ring
    by_cases hab : a ≤ b
    · rw [integral_Icc_eq_integral_Ioc, ← intervalIntegral.integral_of_le hab]
      simp_rw [div_eq_mul_inv (4 : ℝ)]
      rw [intervalIntegral.integral_const_mul, integral_inv_of_pos ha hb,
        Real.log_div hb.ne' ha.ne', hid, max_eq_left]
      have := Real.log_le_log ha hab
      linarith
    · rw [Set.Icc_eq_empty hab, Measure.restrict_empty, integral_zero_measure, max_eq_right,
        mul_zero]
      have := Real.log_lt_log hb (lt_of_not_ge hab)
      linarith
  · rw [ite_eq_right ht]
    refine setIntegral_eq_zero_of_forall_eq_zero fun r hr => ?_
    have hr : 0 < r := hr
    have : t / r ∉ Icc (1 / 2 : ℝ) 1 := by
      rintro ⟨h, _⟩
      have : t / r ≤ 0 := div_nonpos_of_nonpos_of_nonneg (not_lt.mp ht) hr.le
      linarith
    rw [cor_7_1_3_eta1_of_notMem this]
    ring

/-- The book's `η = (t ↦ t² e^{-t²/2}) *_M η₂` is the repo's `TernaryGoldbach.MinorArcs.etaU`,
`etaU(u) = ∫_{(0,∞)} η₂(u/w) φ(w) dw/w` with `φ(w) = w² e^{-w²/2}` (`Helfgott.phi`), at every
real `u`. -/
theorem cor_7_1_3_eta_eq_etaU (u : ℝ) : cor_7_1_3_eta u = etaU u := by
  rw [cor_7_1_3_eta, mellinConv, etaU]
  simp_rw [cor_7_1_3_eta2_eq]
  congr 1
  funext w
  rw [phi]
  ring

/-- The book's `η̂` is Mathlib's Fourier transform `𝓕` of `etaU` (cast to `ℂ`), at every real
`t`. -/
theorem cor_7_1_3_hat_eq_fourier (t : ℝ) :
    cor_7_1_3_hat cor_7_1_3_eta t = 𝓕 (fun u => (etaU u : ℂ)) t := by
  rw [TernaryGoldbach.fourier_eq_integral_e, cor_7_1_3_hat]
  simp_rw [cor_7_1_3_eta_eq_etaU]

/-- The printed series `∑_{n=1}^∞ Λ(n) χ(n) e((δ/x) n) η(n/x)` (over `n : ℕ+`) is the repo's
`Schar χ (n ↦ Λ(n) etaU(n/x)) (δ/x) = ∑' n : ℕ, Λ(n) etaU(n/x) χ(n) e(n δ/x)`. Its `n = 0` term
vanishes because `Λ(0) = 0`. -/
theorem cor_7_1_3_sum_eq_Schar {q : ℕ} (χ : DirichletCharacter ℂ q) (δ x : ℝ) :
    ∑' n : ℕ+, (Λ (n : ℕ) : ℂ) * χ ((n : ℕ) : ZMod q) * e (δ / x * (n : ℕ)) *
        (cor_7_1_3_eta ((n : ℕ) / x) : ℂ) =
      Schar χ (fun n => ((Λ n * etaU (n / x) : ℝ) : ℂ)) (δ / x) := by
  set f : ℕ → ℂ := fun n => ((Λ n * etaU (n / x) : ℝ) : ℂ) * χ (n : ZMod q) * e (n * (δ / x))
    with hf
  have h1 : ∀ n : ℕ+, (Λ (n : ℕ) : ℂ) * χ ((n : ℕ) : ZMod q) * e (δ / x * (n : ℕ)) *
      (cor_7_1_3_eta ((n : ℕ) / x) : ℂ) = f n := by
    intro n
    rw [hf, cor_7_1_3_eta_eq_etaU, mul_comm (δ / x)]
    push_cast
    ring
  rw [tsum_congr h1, Schar]
  refine PNat.coe_injective.tsum_eq (f := f) fun n hn => ?_
  rcases Nat.eq_zero_or_pos n with rfl | hpos
  · exact absurd (by simp [hf] : f 0 = 0) hn
  · exact ⟨⟨n, hpos⟩, rfl⟩

/-- The book's error bound is at most the formalization's: for `1 ≤ q ≤ 300000` and `y > 0`,
`2.485·10⁻¹⁹ + (1/√y)(381500/√q + 76) ≤ 10⁻¹⁷ + 4.7·10⁶/√q/√y`. The proof uses `√q ≤ 548`, so
`(381500 + 76 √q)/(√q √y) ≤ 423148/(√q √y)`. -/
theorem cor_7_1_3_bound_le {q : ℕ} (hq1 : 1 ≤ q) (hq : q ≤ 300000) {y : ℝ} (hy : 0 < y) :
    2.485e-19 + 1 / √y * (381500 / √(q : ℝ) + 76) ≤ 1e-17 + 4.7e6 / √(q : ℝ) / √y := by
  have hq0 : (0 : ℝ) < q := by exact_mod_cast hq1
  have hs : 0 < √(q : ℝ) := Real.sqrt_pos.2 hq0
  have hs' : √(q : ℝ) ≤ 548 := by
    have hq' : (q : ℝ) ≤ 548 ^ 2 := by
      have : (q : ℝ) ≤ 300000 := by exact_mod_cast hq
      linarith
    calc √(q : ℝ) ≤ √(548 ^ 2) := Real.sqrt_le_sqrt hq'
      _ = 548 := Real.sqrt_sq (by norm_num)
  have ht : 0 < √y := Real.sqrt_pos.2 hy
  have key : 1 / √y * (381500 / √(q : ℝ) + 76) = (381500 + 76 * √(q : ℝ)) / √(q : ℝ) / √y := by
    field_simp
  rw [key]
  have : (381500 + 76 * √(q : ℝ)) / √(q : ℝ) / √y ≤ 4.7e6 / √(q : ℝ) / √y := by
    gcongr
    linarith
  have h2 : (2.485e-19 : ℝ) ≤ 1e-17 := by norm_num
  linarith

/-- **[H, Cor. 7.1.3] implies the formalization's version** `TernaryGoldbach.MajorArcs.cor_7_1_3'`
(its statement taken with `type_of%`). The Lean statement has the smaller range `y ≥ 10²⁵` and the
larger error bound `10⁻¹⁷ + 4.7·10⁶/(√q √y)`. Its `Fact PlattGRH` hypothesis is introduced and not
used, and the proof does not use the Lean theorem itself. -/
theorem cor_7_1_3_implies_formal :
    cor_7_1_3 → type_of% @TernaryGoldbach.MajorArcs.cor_7_1_3' := by
  intro h _ y hy q _ hq χ hχ δ hδ
  have hy0 : 0 < y := by linarith
  have hq1 : 1 ≤ q := Nat.one_le_iff_ne_zero.mpr (NeZero.ne q)
  obtain ⟨E, hE, hEb⟩ := h y (by linarith) q hq1 hq χ hχ δ hδ
  rw [cor_7_1_3_sum_eq_Schar, cor_7_1_3_hat_eq_fourier] at hE
  rw [hE]
  have key : (if q = 1 then (1 : ℂ) else 0) * 𝓕 (fun u => (etaU u : ℂ)) (-δ) * y + E * y -
      (if q = 1 then 𝓕 (fun u => (etaU u : ℂ)) (-δ) * y else 0) = E * y := by
    split_ifs <;> ring
  rw [key, norm_mul, Complex.norm_real, Real.norm_of_nonneg hy0.le]
  exact mul_le_mul_of_nonneg_right (hEb.trans (cor_7_1_3_bound_le hq1 hq hy0)) hy0.le

/-- The same implication for the restatement `TernaryGoldbach.MinorArcs.cor_7_1_3`
(`MinorArcs/PartIICited.lean`), which has the same statement as `MajorArcs.cor_7_1_3'`. -/
theorem cor_7_1_3_implies_formal_minorArcs :
    cor_7_1_3 → type_of% @TernaryGoldbach.MinorArcs.cor_7_1_3 :=
  cor_7_1_3_implies_formal

/-- Non-vacuity of the hypotheses: `x = 10⁸`, `q = 1`, the trivial character mod `1` (primitive)
and `δ = 0` meet them. -/
theorem cor_7_1_3_hyps_satisfiable :
    ∃ (x : ℝ) (q : ℕ) (χ : DirichletCharacter ℂ q) (δ : ℝ),
      10 ^ 8 ≤ x ∧ 1 ≤ q ∧ q ≤ 300000 ∧ χ.IsPrimitive ∧ |δ| ≤ 4 * 300000 / (q : ℝ) :=
  ⟨10 ^ 8, 1, 1, 0, le_rfl, le_rfl, by norm_num, DirichletCharacter.isPrimitive_one_level_one,
    by norm_num⟩

/-- The book's `η` vanishes on `(-∞, 0]`, so it is a weight on `ℝ⁺` extended by zero, and `η̂` is
the Fourier transform of that extension. -/
theorem cor_7_1_3_eta_of_nonpos {t : ℝ} (ht : t ≤ 0) : cor_7_1_3_eta t = 0 := by
  rw [cor_7_1_3_eta_eq_etaU, etaU]
  refine setIntegral_eq_zero_of_forall_eq_zero fun w hw => ?_
  have hw : 0 < w := hw
  have h0 : eta2 (t / w) = 0 := by
    rw [eta2, ite_eq_right (not_lt.mpr (div_nonpos_of_nonpos_of_nonneg ht hw.le))]
  rw [h0, zero_mul, zero_div]

/-- Non-vacuity of the weight: the book's `η` is positive on `(0, ∞)`. The integrand
`η₂(t/w) φ(w)/w` is nonnegative, continuous and supported in `[t, 4t]`, and it is positive on
`(t, 2t)`. -/
theorem cor_7_1_3_eta_pos {t : ℝ} (ht : 0 < t) : 0 < cor_7_1_3_eta t := by
  rw [cor_7_1_3_eta_eq_etaU, etaU]
  have hφ : Continuous phi := by unfold phi; fun_prop
  have hφ0 : ∀ w, 0 ≤ phi w := fun w => by unfold phi; positivity
  have hnn : ∀ w ∈ Ioi (0 : ℝ), 0 ≤ eta2 (t / w) * phi w / w := fun w hw => by
    have hw : 0 < w := hw
    have := TernaryGoldbach.Helfgott.eta2_nonneg (t / w)
    have := hφ0 w
    positivity
  have hvan : ∀ w ∈ Ioi (0 : ℝ) \ Icc t (4 * t), eta2 (t / w) * phi w / w = 0 := by
    rintro w ⟨hw, hw'⟩
    have hw : 0 < w := hw
    have h0 : eta2 (t / w) = 0 := by
      rw [eta2, ite_eq_left (by positivity), max_eq_right, mul_zero]
      rcases not_and_or.mp hw' with h | h
      · have h : w < t := not_le.mp h
        have h1 : 2 < 2 * (t / w) := by
          have : 1 < t / w := (one_lt_div hw).2 h
          linarith
        have := Real.log_lt_log (by norm_num) h1
        have := le_abs_self (Real.log (2 * (t / w)))
        linarith
      · have h : 4 * t < w := not_le.mp h
        have h1 : 2 * (t / w) < 1 / 2 := by
          have : t / w < 1 / 4 := by rw [div_lt_iff₀ hw]; linarith
          linarith
        have h2 := Real.log_lt_log (by positivity) h1
        rw [one_div, Real.log_inv] at h2
        have := neg_abs_le (Real.log (2 * (t / w)))
        linarith
    rw [h0, zero_mul, zero_div]
  have hcont : ContinuousOn (fun w => eta2 (t / w) * phi w / w) (Icc t (4 * t)) := by
    have hne : ∀ w ∈ Icc t (4 * t), w ≠ 0 := fun w hw => (ht.trans_le hw.1).ne'
    refine ContinuousOn.div (ContinuousOn.mul ?_ hφ.continuousOn) continuousOn_id hne
    exact TernaryGoldbach.Helfgott.continuous_eta2.comp_continuousOn
      (continuousOn_const.div continuousOn_id hne)
  have hint : IntegrableOn (fun w => eta2 (t / w) * phi w / w) (Ioi 0) :=
    hcont.integrableOn_Icc.of_forall_sdiff_eq_zero measurableSet_Ioi hvan
  rw [setIntegral_pos_iff_support_of_nonneg_ae
    ((ae_restrict_iff' measurableSet_Ioi).2 (Filter.Eventually.of_forall hnn)) hint]
  have hsub : Ioo t (2 * t) ⊆ Function.support (fun w => eta2 (t / w) * phi w / w) ∩ Ioi 0 := by
    rintro w ⟨h1, h2⟩
    have hw : 0 < w := ht.trans h1
    refine ⟨?_, hw⟩
    have hs1 : 1 < 2 * (t / w) := by
      have : 1 / 2 < t / w := by rw [lt_div_iff₀ hw]; linarith
      linarith
    have hs2 : 2 * (t / w) < 2 := by
      have : t / w < 1 := (div_lt_one hw).2 h1
      linarith
    have hl0 : 0 < Real.log (2 * (t / w)) := Real.log_pos hs1
    have hl2 : Real.log (2 * (t / w)) < Real.log 2 := Real.log_lt_log (by linarith) hs2
    have he : 0 < eta2 (t / w) := by
      rw [eta2, ite_eq_left (by positivity), abs_of_pos hl0, max_eq_left (by linarith)]
      linarith
    have hp : 0 < phi w := by unfold phi; positivity
    exact (div_pos (mul_pos he hp) hw).ne'
  refine lt_of_lt_of_le ?_ (measure_mono hsub)
  rw [Real.volume_Ioo]
  simp only [ENNReal.ofReal_pos]
  linarith

end Companion.Book
