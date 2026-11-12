import TernaryGoldbach

/-!
# [H, (14.49)]: the total minor-arc bound

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §14.3,
equation (14.49), p. 275 (https://arxiv.org/pdf/1501.05438v2#page=285). Inserting the bounds
(14.29) `S_{η_*}(0,x)·E ≤ 1.05315·10⁻¹¹ x²/κ`, (14.32) `T ≤ 3.5776·10⁻⁴ x` and (14.48)
`M ≤ 0.80508 x` into Theorem 13.2.1, [H] concludes that the minor-arc total
`Z_{r₀} = ∫_{(ℝ/ℤ) \ 𝔐_{8,r₀}} |S_{η_*}(α,x)| |S_{η₊}(α,x)|² dα` satisfies

`Z_{r₀} ≤ (√(|φ|₁ x (M + T)/κ) + √(S_{η_*}(0,x) · E))²`
`      ≤ (√(|φ|₁ (0.80508 + 3.5776·10⁻⁴)) x/√κ + √(1.0532·10⁻¹¹) x/√κ)²`
`      ≤ 1.00948 x²/κ`

"for `r₀ = 150000`, `x ≥ 4.9·10²⁶`", using `|φ|₁ = √(π/2)` (and `κ = 49`). This is the bound
that §14.4 combines with the major-arc bound (14.27).

**What the formalization proves.** `TernaryGoldbach.MinorArcs.minor_total`
(`MinorArcs/MinorTotal.lean`): for every real `x ≥ 4.9·10²⁶` satisfying `NumericsGoal x`,
`∫_{(0,1] \ 𝔐_{8,r₀}} |S_{η_*}(α,x)| |S_{η₊}(α,x)|² dα ≤ 1.0376 x²/κ`; the hypothesis
`NumericsGoal x` holds for every `x ≥ 4.9·10²⁶` (`TernaryGoldbach.MinorArcs.numerics_M`).
`TernaryGoldbach.Helfgott.minor_arcs_input` (`Helfgott/Inputs.lean`) is the specialization to
`x = xOf N = N/(2 + 9/(196√(2π)))`, `N ≥ 10²⁷`, the form the main theorem uses. Both carry (and,
by the repo's hypothesis trace, really use) the hypotheses `PlattGRH`, `RamareMoebius`.

**Relation: the book's statement implies the formal one (weaker constant).** The arcs
(`𝔐_{8,r₀}` of (10.5) at scale `x`, `r₀ = 150000`), the integrand, the smoothings `η₊`, `η_*` and
the range `x ≥ 4.9·10²⁶` agree with [H] (see the docstring of `eq_14_49`); only the constant
differs, `1.0376 > 1.00948`. Certified here by

* `eq_14_49_implies_formal : eq_14_49 → type_of% @TernaryGoldbach.MinorArcs.minor_total`;
* `eq_14_49_implies_minor_arcs_input :
    eq_14_49 → type_of% @TernaryGoldbach.Helfgott.minor_arcs_input`.

The book's constant `1.00948` is neither proved nor refuted by the formalization. (According to
the repo's `NOTES.md`, "Ch. 13: scale erratum", [H]'s proof of Theorem 13.2.1 derives its ℓ∞
input only off the arcs at scale `x/κ`, while `Z_{r₀}` is defined with the arcs at scale `x`; the
repo proves (14.49) by a repaired argument, with its own constants, ending at `1.0376`.)

Auxiliary results:
* `eq_14_49_formal_bound`: (14.49) with `1.0376` in place of `1.00948`, for every real
  `x ≥ 4.9·10²⁶` (from `minor_total` and `numerics_M`), i.e. what the formalization proves at the
  book's full range;
* `eq_14_49_last_step`: the last inequality of the printed chain is correct arithmetic;
  `eq_14_49_middle` (first member `≤` second member, also asserted by the chain) implies
  `eq_14_49` (`eq_14_49_middle_implies`);
* `eq_14_49_integrableOn`: the integrand is integrable on the minor arcs, so the integral in
  `eq_14_49` is a genuine Lebesgue integral (not Lean's junk value `0`), and `eq_14_49` is a
  substantive statement;
* `eq_14_49_S_add_one`, `eq_14_49_majorArcs_add_one`: `S_η(·,x)` and `majorArcs δ₀ r x` are
  `1`-periodic, which is why `(0,1] \ majorArcs 8 r₀ x` represents `(ℝ/ℤ) \ 𝔐_{8,r₀}`.
-/

namespace Companion.Book

open MeasureTheory
open TernaryGoldbach.Helfgott (S etaStar etaPlus majorArcs r₀ κ)

/-- **[H, (14.49)]** as printed, first member against last member:
for `r₀ = 150000` and every real `x ≥ 4.9·10²⁶`,
`Z_{r₀} = ∫_{(ℝ/ℤ) \ 𝔐_{8,r₀}} |S_{η_*}(α,x)| |S_{η₊}(α,x)|² dα ≤ 1.00948 x²/κ`.

Transcription choices.
* `x` is a real number with `x ≥ 4.9·10²⁶` (`x₊` of the Ch. 14 preamble; Theorem 13.2.1 asks for
  `x ≥ 10²⁵ κ`, the same number). (14.49) does not involve `N`.
* `S_η(α,x) = ∑ₙ Λ(n) e(αn) η(n/x)` ([H, (10.1)], (13.9)) is `TernaryGoldbach.Helfgott.S`, a
  `tsum` over `ℕ` (`Λ(0) = 0`); for `η₊`, `η_*` and `x > 0` the series is absolutely summable
  (`summable_etaPlus`, `summable_etaStar`), so the `tsum` is the book's sum.
* `η₊(t) = h₂₀₀(t) t e^{-t²/2}`, `h_H(t) = ∫₀^∞ h(t/y) F_H(y) dy/y`, `h(t) = t²(2-t)³e^{t-1/2}`
  on `[0,2]` (`0` elsewhere), `F_H(y) = sin(H log y)/(π log y)` ([H, (7.4)–(7.6)], Ch. 14
  preamble, `H = 200`) is `TernaryGoldbach.Helfgott.etaPlus`, definition for definition
  (`hBase`, `F`, `hH`).
* `η_*(t) = (η₂ *_M φ)(κt)` with `φ(t) = t² e^{-t²/2}`, `κ = 49`,
  `η₂ = η₁ *_M η₁ = 4 max(log 2 - |log 2t|, 0)`, `η₁ = 2·1_{[1/2,1]}` ([H, (11.10)], which
  Theorem 13.2.1 cites) is `TernaryGoldbach.Helfgott.etaStar` (`mellinConv eta2 phi (κ * t)`, with
  `(f *_M g)(t) = ∫₀^∞ f(r) g(t/r) dr/r` as in [H, (2.7)]). The Ch. 14 preamble prints
  `η₁ = 2·1_{[-1/2,1/2]}`, a misprint for (11.10)'s `2·1_{[1/2,1]}` (a Mellin convolution only
  sees `(0,∞)`, and Theorem 13.2.1 refers to (11.10)); we follow (11.10).
* `𝔐_{8,r₀}` is (10.5) with `δ₀ = 8`, `r = r₀ = 150000`, defined with the same `x` as in
  `S_η(α,x)`: arcs of radius `δ₀r/(2qx)` around `a/q` for odd `q ≤ r` and of radius `δ₀r/(qx)`
  for even `q ≤ 2r`, `(a,q) = 1`. `TernaryGoldbach.Helfgott.majorArcs 8 r₀ x` is exactly this,
  lifted to `ℝ` (all `a ∈ ℤ` coprime to `q`, i.e. the preimage of the book's subset of `ℝ/ℤ`).
  Reading chosen: the arcs are at scale `x`, as (10.5) and Theorem 13.2.1's "`𝔐_{δ₀,r}` as in
  (10.5) with `δ₀ = 8`" literally say, and as §14.4 needs (the minor arcs must be the complement
  of the major arcs of (14.27), which are at scale `x`). The proof of Theorem 13.2.1 uses arcs at
  scale `x/κ` for its ℓ∞ input (repo `NOTES.md`, "Ch. 13: scale erratum"); that concerns the
  proof, not the printed statement. (With arcs at scale `x/κ` the minor arcs would be smaller and
  the statement would no longer imply the formal one.)
* `∫_{(ℝ/ℤ) \ 𝔐}` (Haar probability measure) is written `∫ α in (0,1] \ majorArcs 8 r₀ x`
  (Lebesgue measure): `(0,1]` is a fundamental domain, and the lifted arcs
  (`eq_14_49_majorArcs_add_one`) and the integrand (`eq_14_49_S_add_one`) are `1`-periodic. The
  integrand is integrable there (`eq_14_49_integrableOn`), so Lean's Bochner integral is the
  book's integral.
* `|S_{η_*}(α,x)| |S_{η₊}(α,x)|²` is `‖S etaStar x α‖ * ‖S etaPlus x α‖ ^ 2`, in the book's order.
* `1.00948 x²/κ` is `1.00948 * x ^ 2 / κ` with `κ = TernaryGoldbach.Helfgott.κ = 49`.
* Only the end-to-end inequality is transcribed: the intermediate members involve the
  quantities `M`, `T`, `E`, `S_{η_*}(0,x)` of Theorem 13.2.1 and §14.3, which are separate items;
  the last step of the chain is checked in `eq_14_49_last_step`. -/
def eq_14_49 : Prop :=
  ∀ x : ℝ, (4.9e26 : ℝ) ≤ x →
    ∫ α in Set.Ioc (0:ℝ) 1 \ majorArcs 8 r₀ x,
        ‖S etaStar x α‖ * ‖S etaPlus x α‖ ^ 2 ≤ 1.00948 * x ^ 2 / κ

/-- `1.00948 x²/κ ≤ 1.0376 x²/κ`. -/
private theorem eq_14_49_const_le (x : ℝ) : 1.00948 * x ^ 2 / κ ≤ 1.0376 * x ^ 2 / κ := by
  have hκ : (0:ℝ) ≤ κ := by norm_num [TernaryGoldbach.Helfgott.κ]
  rw [mul_div_assoc, mul_div_assoc]
  exact mul_le_mul_of_nonneg_right (by norm_num) (div_nonneg (sq_nonneg x) hκ)

/-- **The book's (14.49) implies `minor_total`** (weaker constant `1.0376 > 1.00948`; same arcs,
integrand and range `x ≥ 4.9·10²⁶`; the extra hypothesis `NumericsGoal x` of `minor_total` is not
needed). -/
theorem eq_14_49_implies_formal :
    eq_14_49 → type_of% @TernaryGoldbach.MinorArcs.minor_total := by
  intro h _ _ x hx _
  exact (h x hx).trans (eq_14_49_const_le x)

/-- **The book's (14.49) implies `minor_arcs_input`**, the form used by the main theorem:
specialize to `x = xOf N`, which is `≥ 4.9·10²⁶` for `N ≥ 10²⁷`
(`TernaryGoldbach.Helfgott.xOf_ge`), and use `1.00948 ≤ 1.0376`. -/
theorem eq_14_49_implies_minor_arcs_input :
    eq_14_49 → type_of% @TernaryGoldbach.Helfgott.minor_arcs_input := by
  intro h _ _ N hN
  exact (h _ (TernaryGoldbach.Helfgott.xOf_ge N hN)).trans (eq_14_49_const_le _)

/-- What the formalization proves at the book's full range: (14.49) with `1.0376` in place of
`1.00948`, for every real `x ≥ 4.9·10²⁶` (`minor_total`, with its numerical hypothesis
discharged by `numerics_M`). -/
theorem eq_14_49_formal_bound [Fact TernaryGoldbach.PlattGRH] [Fact TernaryGoldbach.RamareMoebius]
    (x : ℝ) (hx : (4.9e26 : ℝ) ≤ x) :
    ∫ α in Set.Ioc (0:ℝ) 1 \ majorArcs 8 r₀ x,
        ‖S etaStar x α‖ * ‖S etaPlus x α‖ ^ 2 ≤ 1.0376 * x ^ 2 / κ :=
  TernaryGoldbach.MinorArcs.minor_total hx (TernaryGoldbach.MinorArcs.numerics_M hx)

/-- The last inequality of the printed chain (14.49) is correct arithmetic: with
`|φ|₁ = √(π/2)`,
`(√(|φ|₁ (0.80508 + 3.5776·10⁻⁴)) x/√κ + √(1.0532·10⁻¹¹) x/√κ)² ≤ 1.00948 x²/κ`
for every real `x` (the left side is `≈ 1.0094731 x²/κ`). -/
theorem eq_14_49_last_step (x : ℝ) :
    (√(√(Real.pi / 2) * (0.80508 + 3.5776e-4)) * (x / √κ) + √(1.0532e-11) * (x / √κ)) ^ 2 ≤
      1.00948 * x ^ 2 / κ := by
  have hκ : (0:ℝ) ≤ κ := by norm_num [TernaryGoldbach.Helfgott.κ]
  have hs : √(Real.pi / 2) ≤ 1.2533157 := by
    rw [Real.sqrt_le_left (by norm_num)]
    linarith [Real.pi_lt_d4]
  have hA : √(√(Real.pi / 2) * (0.80508 + 3.5776e-4)) ≤ 1.0047228 := by
    rw [Real.sqrt_le_left (by norm_num)]
    calc √(Real.pi / 2) * (0.80508 + 3.5776e-4) ≤ 1.2533157 * (0.80508 + 3.5776e-4) :=
          mul_le_mul_of_nonneg_right hs (by norm_num)
      _ ≤ 1.0047228 ^ 2 := by norm_num
  have hB : √(1.0532e-11 : ℝ) ≤ 3.2454e-6 := by
    rw [Real.sqrt_le_left (by norm_num)]
    norm_num
  have hAB : (√(√(Real.pi / 2) * (0.80508 + 3.5776e-4)) + √(1.0532e-11)) ^ 2 ≤ 1.00948 := by
    have h0 : 0 ≤ √(√(Real.pi / 2) * (0.80508 + 3.5776e-4)) + √(1.0532e-11) := by positivity
    calc (√(√(Real.pi / 2) * (0.80508 + 3.5776e-4)) + √(1.0532e-11)) ^ 2
        ≤ (1.0047228 + 3.2454e-6) ^ 2 := pow_le_pow_left₀ h0 (add_le_add hA hB) 2
      _ ≤ 1.00948 := by norm_num
  rw [← add_mul, mul_pow, div_pow, Real.sq_sqrt hκ, mul_div_assoc]
  exact mul_le_mul_of_nonneg_right hAB (div_nonneg (sq_nonneg x) hκ)

/-- The first member against the second member of the printed chain (14.49), with
`|φ|₁ = √(π/2)`: for every real `x ≥ 4.9·10²⁶`,
`Z_{r₀} ≤ (√(|φ|₁ (0.80508 + 3.5776·10⁻⁴)) x/√κ + √(1.0532·10⁻¹¹) x/√κ)²`.
The chain asserts this too; it is slightly stronger than `eq_14_49` (`≈ 1.0094731 x²/κ` in place
of `1.00948 x²/κ`) and implies it (`eq_14_49_middle_implies`). -/
def eq_14_49_middle : Prop :=
  ∀ x : ℝ, (4.9e26 : ℝ) ≤ x →
    ∫ α in Set.Ioc (0:ℝ) 1 \ majorArcs 8 r₀ x, ‖S etaStar x α‖ * ‖S etaPlus x α‖ ^ 2 ≤
      (√(√(Real.pi / 2) * (0.80508 + 3.5776e-4)) * (x / √κ) + √(1.0532e-11) * (x / √κ)) ^ 2

/-- The second member of (14.49) bounds the first, so the last step gives `eq_14_49`. -/
theorem eq_14_49_middle_implies : eq_14_49_middle → eq_14_49 :=
  fun h x hx => (h x hx).trans (eq_14_49_last_step x)

/-- `S_η(·, x)` is continuous when `∑ₙ |Λ(n) η(n/x)| < ∞`. -/
private theorem eq_14_49_continuous_S {η : ℝ → ℝ} {x : ℝ}
    (h : Summable fun n : ℕ => ‖(((ArithmeticFunction.vonMangoldt n * η (n / x) : ℝ)) : ℂ)‖) :
    Continuous (S η x) :=
  TernaryGoldbach.continuous_expTsum h

/-- Non-vacuity check for `eq_14_49`: for `x > 0` the integrand `|S_{η_*}(α,x)| |S_{η₊}(α,x)|²`
is continuous, hence integrable on the minor arcs `(0,1] \ 𝔐_{8,r₀}`; so the integral in
`eq_14_49` is the book's Lebesgue integral and not Lean's default value `0`. -/
theorem eq_14_49_integrableOn {x : ℝ} (hx : 0 < x) :
    IntegrableOn (fun α => ‖S etaStar x α‖ * ‖S etaPlus x α‖ ^ 2)
      (Set.Ioc (0:ℝ) 1 \ majorArcs 8 r₀ x) :=
  have hc : Continuous fun α => ‖S etaStar x α‖ * ‖S etaPlus x α‖ ^ 2 :=
    (eq_14_49_continuous_S (TernaryGoldbach.Helfgott.summable_etaStar hx)).norm.mul
      ((eq_14_49_continuous_S (TernaryGoldbach.Helfgott.summable_etaPlus hx)).norm.pow 2)
  (hc.integrableOn_Icc (a := 0) (b := 1)).mono_set
    (Set.sdiff_subset.trans Set.Ioc_subset_Icc_self)

/-! ### `(0,1]` stands for `ℝ/ℤ`

The two facts that make `∫ α in (0,1] \ majorArcs 8 r₀ x` the book's `∫_{(ℝ/ℤ) \ 𝔐_{8,r₀}}`:
the integrand and the lifted arcs are `1`-periodic. -/

/-- `e(n) = 1` for `n ∈ ℕ`. -/
private theorem eq_14_49_e_nat (n : ℕ) : TernaryGoldbach.e n = 1 := by
  unfold TernaryGoldbach.e
  have : (2 * Real.pi * Complex.I * ((n : ℝ) : ℂ)) = n * (2 * Real.pi * Complex.I) := by
    push_cast; ring
  rw [this]
  exact Complex.exp_nat_mul_two_pi_mul_I n

/-- `S_η(α + 1, x) = S_η(α, x)`: the integrand of (14.49) is a function on `ℝ/ℤ`. -/
theorem eq_14_49_S_add_one (η : ℝ → ℝ) (x α : ℝ) : S η x (α + 1) = S η x α := by
  unfold TernaryGoldbach.Helfgott.S
  congr 1
  funext n
  rw [mul_add, mul_one, TernaryGoldbach.e_add, eq_14_49_e_nat, mul_one]

/-- A union of arcs `(a/q - w_q, a/q + w_q)` over all `a ∈ ℤ` coprime to `q` is `1`-periodic. -/
private theorem eq_14_49_arcs_add_one (P : ℕ → Prop) (w : ℕ → ℝ) (α : ℝ) :
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

/-- `majorArcs δ₀ r x` is `1`-periodic, i.e. it is the preimage in `ℝ` of a subset of `ℝ/ℤ`
(the book's `𝔐_{δ₀,r}` of (10.5)). -/
theorem eq_14_49_majorArcs_add_one (δ₀ r x α : ℝ) :
    α + 1 ∈ majorArcs δ₀ r x ↔ α ∈ majorArcs δ₀ r x := by
  unfold TernaryGoldbach.Helfgott.majorArcs
  simp only [Set.mem_union]
  exact Iff.or
    (eq_14_49_arcs_add_one (fun q => (q : ℝ) ≤ r ∧ Odd q) (fun q => δ₀ * r / (2 * q * x)) α)
    (eq_14_49_arcs_add_one (fun q => (q : ℝ) ≤ 2 * r ∧ Even q) (fun q => δ₀ * r / (q * x)) α)

end Companion.Book
