import TernaryGoldbach

/-!
# [H, (14.27)]: the total major-arc bound

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §14.2,
equation (14.27), p. 267 (https://arxiv.org/pdf/1501.05438v2#page=277); the display is identical to
(7.25) of the 2013 preprint arXiv:1312.7748v2. In the setting of Ch. 14 (`δ₀ = 8`, `r = 150000`,
`κ = 49`, `N` odd, `x = N/(2 + c₁/κ)` with `c₁ = (9/4)/√(2π)` as chosen in (14.15), and
`x ≥ x₊ = 4.9·10²⁶`, (14.16)), [H] concludes

`∫_{𝔐_{8,r}} S_{η₊}(α,x)² S_{η_*}(α,x) e(−Nα) dα ≥ (1.058259/κ) x²`,

"our total major-arc bound". It is derived from (14.26) (the integral is
`C₀ C_{η∘,η_*} x² + O*(3.85628·10⁻⁵ x²/κ)`, from Prop. 10.4.1 with the numerics of §§14.1–14.2,
"using the assumption `x ≥ x₊`") and `C₀ C_{η∘,η_*} ≥ 1.058298/49` (from (14.9), (14.14), (14.4)).
§14.4 combines it with the minor-arc bound (14.49).

**What the formalization proves.** `TernaryGoldbach.MajorArcs.major_total`
(`MajorArcs/MajorTotal.lean`): for odd `N` and real `x ≥ 4.9·10²⁶` with
`N/x = 2 + 9/(8√(π/2))/κ`,
`1.049 x²/κ ≤ Re ∫_{(0,1] ∩ 𝔐_{8,r₀}} S_{η₊}(α,x)² S_{η_*}(α,x) e(−Nα) dα`.
`TernaryGoldbach.Helfgott.major_arcs_input` (`Helfgott/Inputs.lean`) is its specialization to
`x = xOf N = N/(2 + 9/(196√(2π)))`, `N ≥ 10²⁷`, the form the main theorem uses. Both carry the
`Fact` hypothesis `PlattGRH`.

**Relation: the book's statement implies the formal one (weaker constant).** The integral is the
same (smoothings `η₊`, `η_*`, arcs `𝔐_{8,r₀}` at scale `x`, integrand, `e(−Nα)`; see the
docstring of `eq_14_27`), and so are the hypotheses: `N` odd, `x ≥ 4.9·10²⁶`, and (14.15), which
`eq_14_27_x_iff` shows to be `major_total`'s `N/x = 2 + 9/(8√(π/2))/κ`. Only the constant differs:
`1.049 < 1.058259`. Certified here by

* `eq_14_27_implies_formal : eq_14_27 → type_of% @TernaryGoldbach.MajorArcs.major_total`;
* `eq_14_27_implies_major_arcs_input :
    eq_14_27 → type_of% @TernaryGoldbach.Helfgott.major_arcs_input`.

The book's constant `1.058259` is neither proved nor refuted by the formalization. (The formal
proof uses cruder intermediate bounds: the singular series `≥ 1.314` (`sum_Qset_coefN_ge`) in
place of [H]'s `C₀ ≥ 1.3203236`, `C_{η∘,η_*}(N/x) ≥ 0.800689/κ` (`Cmain_ge_num`), and a larger
`η₊ → η∘` error; the repo's `NOTES.md` reports a total `≈ 1.04926`, stated as `1.049`.)

Auxiliary results:
* `eq_14_27_formal_bound`: what the formalization proves under the book's hypotheses
  (`1.049` in place of `1.058259`);
* `eq_14_27_integral_im_eq_zero`: the integral over the major arcs is a real number (the arcs are
  symmetric under `α ↦ −α` and the integrand satisfies `conj f(α) = f(−α)`), so reading [H]'s
  "`≥`" on the real part loses nothing; `eq_14_27_iff_complex_le`: `eq_14_27` is equivalent to the
  literal reading of "`≥`" in the partial order of `ℂ` (real and imaginary parts);
* `eq_14_27_N`, `eq_14_27_implies_N`, `eq_14_27_N_implies_major_arcs_input`: the alternative
  reading of the hypotheses, with the chapter's standing assumption `N ≥ 10²⁷` in place of its
  consequence `x ≥ x₊`; it is implied by `eq_14_27` and still implies `major_arcs_input` (not
  `major_total`, which also covers the odd `N ∈ [4.9·10²⁶ (2 + c₁/κ), 10²⁷) ≈ [9.8898·10²⁶, 10²⁷)`);
* `eq_14_27_hyps_satisfiable`, `eq_14_27_integrableOn`: non-vacuity — the hypotheses hold for
  `N = 10²⁷ + 1`, and the integrand is integrable on `(0,1] ∩ 𝔐_{8,r₀}`, so the integral is the
  book's Lebesgue integral and not Lean's junk value `0`;
* `eq_14_27_majorArcs_neg`, `eq_14_27_majorArcs_add_one`, `eq_14_27_S_add_one`: the lifted arcs
  are symmetric and `1`-periodic and `S_η(·,x)` is `1`-periodic, which is why
  `(0,1] ∩ majorArcs 8 r₀ x` represents `𝔐_{8,r} ⊂ ℝ/ℤ`.

*Remark on [H]'s derivation* (floating-point check, not used by any theorem here): (14.17) prints
`E_{η_*,r,8} ≤ 1.33805·10⁻⁸/κ`, but its expression `(2.485·10⁻¹⁹ + (381500 + 76√300000)/√10²⁵)/κ`
is `≈ 1.33804·10⁻⁷/κ` (also noted in the repo's `NOTES.md`). Redoing (14.26) with this value
raises the error from `3.85628·10⁻⁵` to `≈ 3.9620·10⁻⁵` (units `x²/κ`). Subtracted from [H]'s
rounded `1.058298` this leaves only `≈ 1.0582584 < 1.058259`; from the unrounded
`1.3203236 (√(π/2)·0.8001287² − 2.0002/κ²) ≈ 1.0583002` it leaves `≈ 1.0582606 ≥ 1.058259`.
So the printed constant still follows from [H]'s inputs.
-/

namespace Companion.Book

open MeasureTheory
open scoped ComplexConjugate
open TernaryGoldbach.Helfgott (S etaStar etaPlus majorArcs r₀ κ)

/-- **[H, (14.27)]** as printed: for `δ₀ = 8`, `r = r₀ = 150000`, `κ = 49`, every odd `N` and
every real `x ≥ x₊ = 4.9·10²⁶` with `x = N/(2 + c₁/κ)`, `c₁ = (9/4)/√(2π)`,
`∫_{𝔐_{8,r}} S_{η₊}(α,x)² S_{η_*}(α,x) e(−Nα) dα ≥ (1.058259/κ) x²`.

Transcription choices.
* `N : ℕ` odd: §14.2 bounds `C₀` (14.8) using only that `2 ∤ N` ("the only prime that we know
  does not divide `N` is `2`", (14.9)).
* `x : ℝ` with `x = N/(2 + c₁/κ)`, `c₁ = (9/4)/√(2π)`: (14.15) ("We have finally chosen `x` in
  terms of `N`"), written `x = N / (2 + 9 / 4 / √(2 * Real.pi) / κ)`; the lower bound (14.14) on
  `C_{η∘,η_*}` is computed for exactly this `N/x = 2 + c₁/κ`.
* `x ≥ 4.9·10²⁶`: the derivation of (14.26)–(14.27) invokes "the assumption `x ≥ x₊`" with
  `x₊ = 4.9·10²⁶` (Ch. 14 preamble: "Our results will have to be valid for any `x ≥ x₊`").
  Reading chosen: this, rather than the chapter's standing assumption `N ≥ 10²⁷` from which
  (14.16) deduces `x ≥ x₊`. The other reading is `eq_14_27_N`; `eq_14_27` implies it
  (`eq_14_27_implies_N`), and it also implies `major_arcs_input`.
* `S_η(α,x) = ∑ₙ Λ(n) e(αn) η(n/x)` (10.1) is `TernaryGoldbach.Helfgott.S`, a `tsum` over `ℕ`
  (`Λ(0) = 0`); for `η₊`, `η_*` and `x > 0` the series is absolutely summable
  (`summable_etaPlus`, `summable_etaStar`), so the `tsum` is the book's sum.
  `e(t) = exp(2πit)` is `TernaryGoldbach.e`.
* `η₊(t) = h₂₀₀(t) t e^{−t²/2}`, `h_H(t) = ∫₀^∞ h(t/y) F_H(y) dy/y`,
  `h(t) = t²(2−t)³e^{t−1/2}` on `[0,2]` (`0` elsewhere), `F_H(y) = sin(H log y)/(π log y)`
  (Ch. 14 preamble, `H = 200`) is `TernaryGoldbach.Helfgott.etaPlus`, definition for definition
  (`hBase`, `F`, `hH`; Lean's `F H 1 = 0` is a single point and does not affect `h_H`).
* `η_*(t) = (η₂ *_M φ)(κt)`, `φ(t) = t² e^{−t²/2}`, with the Mellin convolution (2.7)
  `(f *_M g)(t) = ∫₀^∞ f(w) g(t/w) dw/w`, is `TernaryGoldbach.Helfgott.etaStar`
  (`mellinConv eta2 phi (κ * t)`), with `η₂ = η₁ *_M η₁ = 4 max(log 2 − |log 2t|, 0)`,
  `η₁ = 2·1_{[1/2,1]}` as in (11.10). The Ch. 14 preamble prints `η₁ = 2·1_{[−1/2,1/2]}`, a
  misprint (a Mellin convolution only sees `(0,∞)`, and §14.2 uses that `η₂` is supported in
  `[1/4,1]`, which holds for (11.10)'s `η₂` but not for the printed one); we follow (11.10).
* `𝔐_{8,r}` is (10.5) with `δ₀ = 8`, `r = 150000`, at the same scale `x` as `S_η(α,x)`: arcs of
  radius `δ₀r/(2qx)` around `a/q` for odd `q ≤ r` and `δ₀r/(qx)` for even `q ≤ 2r`, `(a,q) = 1`.
  `TernaryGoldbach.Helfgott.majorArcs 8 r₀ x` is this set lifted to `ℝ` (all `a ∈ ℤ` coprime to
  `q`: the preimage of the book's subset of `ℝ/ℤ`).
* `∫_{𝔐_{8,r}} … dα` over `ℝ/ℤ` (Haar probability measure) is
  `∫ α in (0,1] ∩ majorArcs 8 r₀ x, …` (Lebesgue measure): `(0,1]` is a fundamental domain, and
  the lifted arcs (`eq_14_27_majorArcs_add_one`) and the integrand (`eq_14_27_S_add_one`) are
  `1`-periodic. The integrand is integrable there (`eq_14_27_integrableOn`).
* The integrand `S_{η₊}(α,x)² S_{η_*}(α,x) e(−Nα)` is
  `S etaPlus x α ^ 2 * S etaStar x α * TernaryGoldbach.e (-(N * α))`, literally the body of the
  repo's `TernaryGoldbach.MajorArcs.fI N x α`.
* "`≥`" between the complex-valued integral and a real number is read on the real part. This is
  no loss: the integral is real (`eq_14_27_integral_im_eq_zero`), and `eq_14_27_iff_complex_le`
  proves `eq_14_27` equivalent to the literal statement in `ℂ`'s partial order.
* `(1.058259/κ) x²` is `1.058259 / κ * x ^ 2` with `κ = TernaryGoldbach.Helfgott.κ = 49`. -/
def eq_14_27 : Prop :=
  ∀ N : ℕ, Odd N → ∀ x : ℝ, (4.9e26 : ℝ) ≤ x → x = N / (2 + 9 / 4 / √(2 * Real.pi) / κ) →
    1.058259 / κ * x ^ 2 ≤
      (∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x,
        S etaPlus x α ^ 2 * S etaStar x α * TernaryGoldbach.e (-(N * α))).re

/-! ### The hypotheses -/

/-- `κ = 49 > 0`. -/
private theorem eq_14_27_kappa_pos : (0:ℝ) < κ := by
  norm_num [TernaryGoldbach.Helfgott.κ]

/-- (14.15) in the form used by `major_total`: for `x > 0`, `x = N/(2 + c₁/κ)` with
`c₁ = (9/4)/√(2π)` iff `N/x = 2 + 9/(8√(π/2))/κ` (because `√(2π) = 2√(π/2)`). -/
theorem eq_14_27_x_iff (N : ℕ) {x : ℝ} (hx : 0 < x) :
    x = N / (2 + 9 / 4 / √(2 * Real.pi) / κ) ↔
      (N : ℝ) / x = 2 + 9 / (8 * √(Real.pi / 2)) / κ := by
  have hs : √(2 * Real.pi) = 2 * √(Real.pi / 2) := by
    rw [show 2 * Real.pi = 2 ^ 2 * (Real.pi / 2) by ring, Real.sqrt_mul (by positivity),
      Real.sqrt_sq (by norm_num)]
  have hs0 : 0 < √(Real.pi / 2) := Real.sqrt_pos.2 (by positivity)
  have hc : (9:ℝ) / 4 / √(2 * Real.pi) / κ = 9 / (8 * √(Real.pi / 2)) / κ := by
    rw [hs, div_div]
    ring
  have hd : 0 < 2 + 9 / (8 * √(Real.pi / 2)) / κ := by
    have := eq_14_27_kappa_pos
    positivity
  rw [hc, eq_div_iff hd.ne', div_eq_iff hx.ne']
  constructor <;> intro h <;> linarith

/-- The denominator `2 + c₁/κ` of (14.15) lies in `(0, 2.02]`. -/
private theorem eq_14_27_denom :
    0 < 2 + 9 / 4 / √(2 * Real.pi) / κ ∧ 2 + 9 / 4 / √(2 * Real.pi) / κ ≤ 2.02 := by
  have hκ := eq_14_27_kappa_pos
  have hs : (2.5:ℝ) ≤ √(2 * Real.pi) :=
    Real.le_sqrt_of_sq_le (by nlinarith [Real.pi_gt_d2])
  have hs0 : (0:ℝ) < √(2 * Real.pi) := by linarith
  refine ⟨by positivity, ?_⟩
  have h : (9:ℝ) / 4 / √(2 * Real.pi) / κ ≤ 0.02 := by
    rw [div_div, div_le_iff₀ (by positivity)]
    have : (49:ℝ) = κ := rfl
    nlinarith
  linarith

/-- `xOf N` (the repo's `x`, [H13, (7.14)]) is (14.15)'s `N/(2 + c₁/κ)`. -/
theorem eq_14_27_xOf_eq (N : ℕ) :
    TernaryGoldbach.Helfgott.xOf N = N / (2 + 9 / 4 / √(2 * Real.pi) / κ) := by
  unfold TernaryGoldbach.Helfgott.xOf
  congr 2
  rw [div_div, div_div]
  norm_num [TernaryGoldbach.Helfgott.κ]
  ring

/-- `1.049 x²/κ ≤ (1.058259/κ) x²` (left side shaped as in the formal statements, right side as in
`eq_14_27`). -/
private theorem eq_14_27_const_le (x : ℝ) : 1.049 * x ^ 2 / κ ≤ 1.058259 / κ * x ^ 2 := by
  have hκ := eq_14_27_kappa_pos
  rw [mul_div_right_comm]
  exact mul_le_mul_of_nonneg_right (div_le_div_of_nonneg_right (by norm_num) hκ.le)
    (sq_nonneg x)

/-! ### The relation with the formalization -/

/-- **The book's (14.27) implies `major_total`** (weaker constant `1.049 < 1.058259`; same
integral; same hypotheses `N` odd, `x ≥ 4.9·10²⁶` and (14.15), the last one in the equivalent
form `N/x = 2 + 9/(8√(π/2))/κ`, `eq_14_27_x_iff`). -/
theorem eq_14_27_implies_formal :
    eq_14_27 → type_of% @TernaryGoldbach.MajorArcs.major_total := by
  intro h _ N hN x hx hNx
  have hx0 : 0 < x := lt_of_lt_of_le (by norm_num) hx
  exact (eq_14_27_const_le x).trans (h N hN x hx ((eq_14_27_x_iff N hx0).2 hNx))

/-- The alternative reading of (14.27)'s hypotheses: the chapter's standing assumption
`N ≥ 10²⁷` (Ch. 14 preamble, (14.16)) in place of its consequence `x ≥ x₊ = 4.9·10²⁶`; otherwise
as `eq_14_27` (odd `N`, `x = N/(2 + c₁/κ)` with `c₁ = (9/4)/√(2π)`). -/
def eq_14_27_N : Prop :=
  ∀ N : ℕ, Odd N → 10 ^ 27 ≤ N → ∀ x : ℝ, x = N / (2 + 9 / 4 / √(2 * Real.pi) / κ) →
    1.058259 / κ * x ^ 2 ≤
      (∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x,
        S etaPlus x α ^ 2 * S etaStar x α * TernaryGoldbach.e (-(N * α))).re

/-- `eq_14_27` implies the `N ≥ 10²⁷` reading: `N ≥ 10²⁷` gives `x = N/(2 + c₁/κ) ≥ 4.9·10²⁶`
(14.16). -/
theorem eq_14_27_implies_N : eq_14_27 → eq_14_27_N := by
  intro h N hN hN27 x hxN
  refine h N hN x ?_ hxN
  obtain ⟨h0, h1⟩ := eq_14_27_denom
  have hNr : (10:ℝ) ^ 27 ≤ N := by exact_mod_cast hN27
  rw [hxN, le_div_iff₀ h0]
  nlinarith

/-- **The `N ≥ 10²⁷` reading of (14.27) implies `major_arcs_input`** (weaker constant; the same
hypotheses `N` odd, `N ≥ 10²⁷`, with `x = xOf N`, which is (14.15)'s `N/(2 + c₁/κ)`). -/
theorem eq_14_27_N_implies_major_arcs_input :
    eq_14_27_N → type_of% @TernaryGoldbach.Helfgott.major_arcs_input := by
  intro h _ N hN hN27
  exact (eq_14_27_const_le _).trans (h N hN hN27 _ (eq_14_27_xOf_eq N))

/-- **The book's (14.27) implies `major_arcs_input`**, the form used by the main theorem
(through `eq_14_27_N`). -/
theorem eq_14_27_implies_major_arcs_input :
    eq_14_27 → type_of% @TernaryGoldbach.Helfgott.major_arcs_input :=
  fun h => eq_14_27_N_implies_major_arcs_input (eq_14_27_implies_N h)

/-- What the formalization proves under the book's hypotheses: (14.27) with `1.049` in place of
`1.058259` (`major_total`). -/
theorem eq_14_27_formal_bound [Fact TernaryGoldbach.PlattGRH]
    (N : ℕ) (hN : Odd N) (x : ℝ) (hx : (4.9e26 : ℝ) ≤ x)
    (hxN : x = N / (2 + 9 / 4 / √(2 * Real.pi) / κ)) :
    1.049 / κ * x ^ 2 ≤
      (∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x,
        S etaPlus x α ^ 2 * S etaStar x α * TernaryGoldbach.e (-(N * α))).re := by
  have hx0 : 0 < x := lt_of_lt_of_le (by norm_num) hx
  have h := TernaryGoldbach.MajorArcs.major_total hN hx ((eq_14_27_x_iff N hx0).1 hxN)
  calc 1.049 / κ * x ^ 2 = 1.049 * x ^ 2 / κ := by ring
    _ ≤ _ := h

/-! ### `(0,1] ∩ majorArcs` stands for `𝔐_{8,r} ⊂ ℝ/ℤ`; the integral is real -/

/-- `e(n) = 1` for `n ∈ ℕ`. -/
private theorem eq_14_27_e_nat (n : ℕ) : TernaryGoldbach.e n = 1 := by
  have h := TernaryGoldbach.e_intCast (n : ℤ)
  rwa [Int.cast_natCast] at h

/-- `e(−N(α + 1)) = e(−Nα)` for `N ∈ ℕ`. -/
private theorem eq_14_27_e_shift (N : ℕ) (α : ℝ) :
    TernaryGoldbach.e (-(N * (α + 1))) = TernaryGoldbach.e (-(N * α)) := by
  rw [show -((N : ℝ) * (α + 1)) = -(N * α) + ((-(N : ℤ) : ℤ) : ℝ) by push_cast; ring,
    TernaryGoldbach.e_add, TernaryGoldbach.e_intCast, mul_one]

/-- `conj e(t) = e(−t)`. -/
private theorem eq_14_27_conj_e (t : ℝ) : conj (TernaryGoldbach.e t) = TernaryGoldbach.e (-t) := by
  unfold TernaryGoldbach.e
  rw [← Complex.exp_conj]
  congr 1
  simp only [map_mul, Complex.conj_ofReal, Complex.conj_I, map_ofNat, Complex.ofReal_neg]
  ring

/-- `S_η(α + 1, x) = S_η(α, x)`: the integrand of (14.27) is a function on `ℝ/ℤ`. -/
theorem eq_14_27_S_add_one (η : ℝ → ℝ) (x α : ℝ) : S η x (α + 1) = S η x α := by
  unfold TernaryGoldbach.Helfgott.S
  congr 1
  funext n
  rw [mul_add, mul_one, TernaryGoldbach.e_add, eq_14_27_e_nat, mul_one]

/-- `conj S_η(α, x) = S_η(−α, x)` for real `η` (real coefficients). -/
private theorem eq_14_27_conj_S (η : ℝ → ℝ) (x α : ℝ) : conj (S η x α) = S η x (-α) := by
  unfold TernaryGoldbach.Helfgott.S
  rw [Complex.conj_tsum]
  congr 1
  funext n
  rw [map_mul, Complex.conj_ofReal, eq_14_27_conj_e, mul_neg]

/-- A union of arcs `(a/q − w_q, a/q + w_q)` over all `a ∈ ℤ` coprime to `q` is `1`-periodic. -/
private theorem eq_14_27_arcs_add_one (P : ℕ → Prop) (w : ℕ → ℝ) (α : ℝ) :
    α + 1 ∈ (⋃ (q : ℕ) (_ : 1 ≤ q ∧ P q) (a : ℤ) (_ : IsCoprime a (q : ℤ)),
      Set.Ioo ((a : ℝ) / q - w q) (a / q + w q)) ↔
    α ∈ (⋃ (q : ℕ) (_ : 1 ≤ q ∧ P q) (a : ℤ) (_ : IsCoprime a (q : ℤ)),
      Set.Ioo ((a : ℝ) / q - w q) (a / q + w q)) := by
  simp only [Set.mem_iUnion, Set.mem_Ioo, exists_prop]
  constructor
  · rintro ⟨q, hq, a, ha, h1, h2⟩
    have hq0 : (q : ℝ) ≠ 0 := by exact_mod_cast (by omega : q ≠ 0)
    have hsh : ((a - q : ℤ) : ℝ) / q = a / q - 1 := by
      push_cast; rw [sub_div, div_self hq0]
    refine ⟨q, hq, a - q, ?_, ?_, ?_⟩
    · convert ha.add_mul_left_left (-1) using 1; ring
    · rw [hsh]; linarith
    · rw [hsh]; linarith
  · rintro ⟨q, hq, a, ha, h1, h2⟩
    have hq0 : (q : ℝ) ≠ 0 := by exact_mod_cast (by omega : q ≠ 0)
    have hsh : ((a + q : ℤ) : ℝ) / q = a / q + 1 := by
      push_cast; rw [add_div, div_self hq0]
    refine ⟨q, hq, a + q, ?_, ?_, ?_⟩
    · convert ha.add_mul_left_left 1 using 1; ring
    · rw [hsh]; linarith
    · rw [hsh]; linarith

/-- A union of arcs `(a/q − w_q, a/q + w_q)` over all `a ∈ ℤ` coprime to `q` is symmetric under
`α ↦ −α`. -/
private theorem eq_14_27_arcs_neg (P : ℕ → Prop) (w : ℕ → ℝ) (α : ℝ) :
    -α ∈ (⋃ (q : ℕ) (_ : 1 ≤ q ∧ P q) (a : ℤ) (_ : IsCoprime a (q : ℤ)),
      Set.Ioo ((a : ℝ) / q - w q) (a / q + w q)) ↔
    α ∈ (⋃ (q : ℕ) (_ : 1 ≤ q ∧ P q) (a : ℤ) (_ : IsCoprime a (q : ℤ)),
      Set.Ioo ((a : ℝ) / q - w q) (a / q + w q)) := by
  simp only [Set.mem_iUnion, Set.mem_Ioo, exists_prop]
  constructor
  · rintro ⟨q, hq, a, ha, h1, h2⟩
    refine ⟨q, hq, -a, (IsCoprime.neg_left_iff a q).2 ha, ?_, ?_⟩ <;>
      simp only [Int.cast_neg, neg_div] <;> linarith
  · rintro ⟨q, hq, a, ha, h1, h2⟩
    refine ⟨q, hq, -a, (IsCoprime.neg_left_iff a q).2 ha, ?_, ?_⟩ <;>
      simp only [Int.cast_neg, neg_div] <;> linarith

/-- `majorArcs δ₀ r x` is `1`-periodic, i.e. it is the preimage in `ℝ` of a subset of `ℝ/ℤ`
(the book's `𝔐_{δ₀,r}` of (10.5)). -/
theorem eq_14_27_majorArcs_add_one (δ₀ r x α : ℝ) :
    α + 1 ∈ majorArcs δ₀ r x ↔ α ∈ majorArcs δ₀ r x := by
  unfold TernaryGoldbach.Helfgott.majorArcs
  simp only [Set.mem_union]
  exact Iff.or
    (eq_14_27_arcs_add_one (fun q => (q : ℝ) ≤ r ∧ Odd q) (fun q => δ₀ * r / (2 * q * x)) α)
    (eq_14_27_arcs_add_one (fun q => (q : ℝ) ≤ 2 * r ∧ Even q) (fun q => δ₀ * r / (q * x)) α)

/-- `majorArcs δ₀ r x` is symmetric under `α ↦ −α`. -/
theorem eq_14_27_majorArcs_neg (δ₀ r x α : ℝ) :
    -α ∈ majorArcs δ₀ r x ↔ α ∈ majorArcs δ₀ r x := by
  unfold TernaryGoldbach.Helfgott.majorArcs
  simp only [Set.mem_union]
  exact Iff.or
    (eq_14_27_arcs_neg (fun q => (q : ℝ) ≤ r ∧ Odd q) (fun q => δ₀ * r / (2 * q * x)) α)
    (eq_14_27_arcs_neg (fun q => (q : ℝ) ≤ 2 * r ∧ Even q) (fun q => δ₀ * r / (q * x)) α)

/-- If `g` is `1`-periodic and `conj g(α) = g(−α)`, then `∫₀¹ g` is real. -/
private theorem eq_14_27_im_intervalIntegral {g : ℝ → ℂ} (hper : Function.Periodic g 1)
    (hc : ∀ α, conj (g α) = g (-α)) : (∫ α in (0:ℝ)..1, g α).im = 0 := by
  rw [← Complex.conj_eq_iff_im]
  calc conj (∫ α in (0:ℝ)..1, g α) = ∫ α in (0:ℝ)..1, conj (g α) := by
        rw [intervalIntegral.integral_of_le zero_le_one,
          intervalIntegral.integral_of_le zero_le_one, integral_conj]
    _ = ∫ α in (0:ℝ)..1, g (-α) := by simp_rw [hc]
    _ = ∫ α in (-1:ℝ)..(-0), g α := intervalIntegral.integral_comp_neg g
    _ = ∫ α in (-1:ℝ)..(-1 + 1), g α := by norm_num
    _ = ∫ α in (0:ℝ)..(0 + 1), g α := hper.intervalIntegral_add_eq (-1) 0
    _ = ∫ α in (0:ℝ)..1, g α := by norm_num

/-- **The integral of (14.27) is real**: for every `N`, `δ₀`, `r`, `x`,
`Im ∫_{(0,1] ∩ 𝔐_{δ₀,r}} S_{η₊}(α,x)² S_{η_*}(α,x) e(−Nα) dα = 0`. (The arcs are symmetric and
`1`-periodic, and `conj f(α) = f(−α)` for the integrand `f`, since `η₊`, `η_*` are real.) Hence
reading [H]'s "`≥`" on the real part, as `eq_14_27` does, loses nothing. -/
theorem eq_14_27_integral_im_eq_zero (N : ℕ) (δ₀ r x : ℝ) :
    (∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs δ₀ r x,
        S etaPlus x α ^ 2 * S etaStar x α * TernaryGoldbach.e (-(N * α))).im = 0 := by
  rw [← setIntegral_indicator (TernaryGoldbach.Helfgott.measurableSet_majorArcs δ₀ r x),
    ← intervalIntegral.integral_of_le zero_le_one]
  apply eq_14_27_im_intervalIntegral
  · intro α
    by_cases h : α ∈ majorArcs δ₀ r x
    · rw [Set.indicator_of_mem h,
        Set.indicator_of_mem ((eq_14_27_majorArcs_add_one δ₀ r x α).2 h)]
      simp only [eq_14_27_S_add_one, eq_14_27_e_shift]
    · rw [Set.indicator_of_notMem h,
        Set.indicator_of_notMem fun h' => h ((eq_14_27_majorArcs_add_one δ₀ r x α).1 h')]
  · intro α
    by_cases h : α ∈ majorArcs δ₀ r x
    · rw [Set.indicator_of_mem h, Set.indicator_of_mem ((eq_14_27_majorArcs_neg δ₀ r x α).2 h)]
      simp only [map_mul, map_pow, eq_14_27_conj_S, eq_14_27_conj_e, mul_neg, neg_neg]
    · rw [Set.indicator_of_notMem h,
        Set.indicator_of_notMem fun h' => h ((eq_14_27_majorArcs_neg δ₀ r x α).1 h'), map_zero]

open scoped ComplexOrder in
/-- **The literal reading of "`≥`".** In `ℂ`'s partial order (`z ≤ w` iff `Re z ≤ Re w` and
`Im z = Im w`), "the integral is `≥ (1.058259/κ) x²`" says that the integral is real and its
value is at least `(1.058259/κ) x²`. Since the integral is real
(`eq_14_27_integral_im_eq_zero`), this is equivalent to `eq_14_27`. -/
theorem eq_14_27_iff_complex_le :
    eq_14_27 ↔ ∀ N : ℕ, Odd N → ∀ x : ℝ, (4.9e26 : ℝ) ≤ x →
      x = N / (2 + 9 / 4 / √(2 * Real.pi) / κ) →
      (((1.058259 / κ * x ^ 2 : ℝ)) : ℂ) ≤
        ∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x,
          S etaPlus x α ^ 2 * S etaStar x α * TernaryGoldbach.e (-(N * α)) := by
  refine forall_congr' fun N => imp_congr_right fun _ => forall_congr' fun x =>
    imp_congr_right fun _ => imp_congr_right fun _ => ?_
  rw [Complex.le_def, Complex.ofReal_re, Complex.ofReal_im, eq_14_27_integral_im_eq_zero]
  exact (and_iff_left rfl).symm

/-! ### Non-vacuity -/

/-- The hypotheses of `eq_14_27` are satisfiable: `N = 10²⁷ + 1` is odd and
`x = N/(2 + c₁/κ) ≥ 4.9·10²⁶`. -/
theorem eq_14_27_hyps_satisfiable :
    ∃ N : ℕ, Odd N ∧ ∃ x : ℝ, (4.9e26 : ℝ) ≤ x ∧ x = N / (2 + 9 / 4 / √(2 * Real.pi) / κ) := by
  refine ⟨10 ^ 27 + 1, ⟨5 * 10 ^ 26, by norm_num⟩, _, ?_, rfl⟩
  obtain ⟨h0, h1⟩ := eq_14_27_denom
  rw [le_div_iff₀ h0]
  push_cast
  nlinarith

/-- `S_η(·, x)` is continuous when `∑ₙ |Λ(n) η(n/x)| < ∞`. -/
private theorem eq_14_27_continuous_S {η : ℝ → ℝ} {x : ℝ}
    (h : Summable fun n : ℕ => ‖(((ArithmeticFunction.vonMangoldt n * η (n / x) : ℝ)) : ℂ)‖) :
    Continuous (S η x) :=
  TernaryGoldbach.continuous_expTsum h

/-- Non-vacuity check for `eq_14_27`: for `x > 0` the integrand
`S_{η₊}(α,x)² S_{η_*}(α,x) e(−Nα)` is continuous, hence integrable on `(0,1] ∩ 𝔐_{δ₀,r}`; so the
integral in `eq_14_27` is the book's Lebesgue integral and not Lean's default value `0`. -/
theorem eq_14_27_integrableOn (N : ℕ) {x : ℝ} (hx : 0 < x) (δ₀ r : ℝ) :
    IntegrableOn (fun α => S etaPlus x α ^ 2 * S etaStar x α * TernaryGoldbach.e (-(N * α)))
      (Set.Ioc (0:ℝ) 1 ∩ majorArcs δ₀ r x) := by
  have hc : Continuous
      (fun α => S etaPlus x α ^ 2 * S etaStar x α * TernaryGoldbach.e (-(N * α))) :=
    (((eq_14_27_continuous_S (TernaryGoldbach.Helfgott.summable_etaPlus hx)).pow 2).mul
      (eq_14_27_continuous_S (TernaryGoldbach.Helfgott.summable_etaStar hx))).mul
      (TernaryGoldbach.continuous_e.comp (by fun_prop))
  exact (hc.integrableOn_Icc (a := 0) (b := 1)).mono_set
    (Set.inter_subset_left.trans Set.Ioc_subset_Icc_self)

end Companion.Book
