import TernaryGoldbach

/-!
# [H, (14.7)]: the `ℓ₂` norm of `S_{η₊}` over the major arcs

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §14.1,
equation (14.7), p. 261 (label `eq:celine`; https://arxiv.org/pdf/1501.05438v2#page=271).
[H] applies Lemma 10.3.1 with `η = η₊`, `δ₀ = 8` and `r = r₀ = 150000`, and concludes

```
∫_{𝔐_{8,r₀}} |S_{η₊}(α,x)|² dα = (8.70524 + O*(0.00007)) x + O*(0.075273) x
                               = (8.7052 + O*(0.0754)) x ≤ 8.7806 x
```

for every `x ≥ x₊ = 4.9·10²⁶`. The range comes from the preamble of Ch. 14: "our results will have
to be valid for any `x ≥ x₊`". In the first member, `8.70524 + O*(0.00007)` is the main-term
constant `L_{r,δ₀}`, which p. 261 places in `[8.70517, 8.70531]` using (10.28)–(10.29). The term
`O*(0.075273) x` collects the two error terms of (10.26), bounded on p. 260 by `0.075272` and
`1.00393·10⁻⁸`.

**What the formalization proves.** `TernaryGoldbach.MajorArcs.l2_major_bounds`
(`MajorArcs/L2Major.lean:309`) proves, for every real `x ≥ 4.9·10²⁶`,
`8.6296 x ≤ ∫_{(0,1] ∩ 𝔐_{8,r₀}} |S_{η₊}(α,x)|² dα ≤ 8.79 x`. It uses the same arcs, integrand and
range. The theorem carries the `Fact` hypothesis `PlattGRH`.
`TernaryGoldbach.MinorArcs.l2_major_14_7` (`MinorArcs/PartIICited.lean:64`) restates the result as `|∫ − 8.7098 x| ≤ 0.0802 x`, and this is the form the minor-arc total consumes.

The proof follows Lemma 10.3.1 modulus by modulus but bounds the error terms differently: each
pointwise square is split as `|u + v|² = (1 ± t)|u|² + O((1 + 1/t)|v|²)` with `t = 10⁻⁴`, instead of
using [H]'s `5.19 δ₀ r · ET · (|η|₁ + ET/2)` term. For each modulus `q ∈ Qset r₀`,
`MajorArcs.Jq_bounds` (`L2Major.lean:100`) puts the integral over the arcs of modulus `q` between
`(0.63907 − 0.000962) μ²(q)/φ(q) x − 3.6·10⁻⁹ x` and
`(0.64034 + 0.000962) μ²(q)/φ(q) x + 2.17·10⁻⁷ x`.
`MajorArcs.sum_Qset_mPhi_bounds` puts `Σ_q μ²(q)/φ(q)` in `[13.597558, 13.59756]`. The additive
per-modulus errors `3.6·10⁻⁹ x` and `2.17·10⁻⁷ x` are multiplied by the number of moduli, which
`MajorArcs.card_Qset_le` (`L2Major.lean:295`) bounds crudely by `#Qset r₀ ≤ 300000`. Before
rounding, this gives `8.6756 x ≤ ∫ ≤ 8.7852 x`. The upper constant is
`(0.64034 + 0.000962)·13.59756 + 2.17·10⁻⁷·300000 = 8.785242…`, that is, the per-modulus constant
`2.17·10⁻⁷` times the crude count `300000` from `card_Qset_le`, added to the main term.

**Relation: (14.7) holds.** Under the `Fact` hypothesis `PlattGRH`, [H]'s statement as printed is
a theorem, `eq_14_7_holds`. The hypothesis is used through `Jq_bounds`. The proof is the proof of
`l2_major_bounds` with one change, the count of moduli. `Qset r₀` is the set of `q ≥ 1` with
`q̃ ≤ 2r₀ = 300000`, where `q̃ = q` for even `q` and `q̃ = 2q` for odd `q`. So it consists of
the `75000` odd `q ≤ 150000` and the `150000` even `q ≤ 300000`, `225000` in all
(`eq_14_7_card_Qset_le`). With this count, the same sums give
`(0.63907 − 0.000962)·13.597558 − 3.6·10⁻⁹·225000 = 8.675900…` and
`(0.64034 + 0.000962)·13.59756 + 2.17·10⁻⁷·225000 = 8.768967…`, so
`8.6759 x ≤ ∫ ≤ 8.769 x` (`eq_14_7_sharp_bounds`). This interval lies inside
`[8.629897 x, 8.780583 x]`, to which the printed chain is equivalent (`eq_14_7_iff_bounds`). Besides
the count and this file's continuity and periodicity lemmas, the proof uses only in-cone repository
lemmas: `Jq_bounds`, `sum_Qset_mPhi_bounds`, `MinorArcs.integral_majorArcs_le` and
`MinorArcs.sum_arcs_le_integral_majorArcs` (and, for continuity, `Helfgott.summable_etaPlus` and
`continuous_expTsum`).

The declared Lean statement `l2_major_bounds` is weaker than (14.7): its `[8.6296 x, 8.79 x]`
contains [H]'s `[8.629897 x, 8.780583 x]`. At the lower end this is only the choice of the declared
constant, since the proof reaches `8.6756`. At the upper end, `l2_major_bounds` misses [H]'s
`8.780583` only because `card_Qset_le` bounds `#Qset r₀` by `300000` rather than `225000`. The
comparison with the declared statements is certified by

* `eq_14_7_implies_formal : eq_14_7 → type_of% @TernaryGoldbach.MajorArcs.l2_major_bounds`;
* `eq_14_7_implies_formal_cited : eq_14_7 → type_of% @TernaryGoldbach.MinorArcs.l2_major_14_7`.

Auxiliary results:
* `eq_14_7_iff_bounds` shows that the existential error terms are real constraints. Since `x > 0`,
  the definition is equivalent to the explicit bounds `8.629897 x ≤ ∫ ≤ 8.780583 x`.
* `eq_14_7_iff_line1` shows that the later members of the chain follow from the first. So [H]'s
  arithmetic from the first member onwards is correct, and the definition is equivalent to its
  first member alone.
* `eq_14_7_integrableOn` shows that the integrand is integrable on `(0,1] ∩ 𝔐_{8,r₀}`. So the
  integral is a genuine Lebesgue integral, not Lean's default value `0`.
* `eq_14_7_S_add_one` and `eq_14_7_majorArcs_add_one` show that `S_η(·,x)` and `majorArcs δ₀ r x`
  are `1`-periodic. This is why `(0,1] ∩ majorArcs 8 r₀ x` represents `𝔐_{8,r₀} ⊂ ℝ/ℤ`.
* `eq_14_7_card_Qset_le` (the count `#Qset r₀ ≤ 225000`) and `eq_14_7_sharp_bounds`
  (`8.6759 x ≤ ∫ ≤ 8.769 x`) are the two steps of `eq_14_7_holds`.
* `eq_14_7_slip` checks the numbers in the note below.

**A slip in [H]'s arithmetic.** On p. 260, [H] bounds
`5.19 δ₀ r · ET_{η₊,δ₀r/2} · (|η₊|₁ + ET_{η₊,δ₀r/2}/2)` by `0.075272`. [H]'s own inputs are
`δ₀ = 8`, `r = 150000`, `ET_{η₊,δ₀r/2} ≤ 1.1405·10⁻⁸` from (14.1) and `|η₊|₁ ≤ 1.062319` from
(14.3). With these, the product is `0.0754568…`, which lies between `0.075456` and `0.075457`.
Using the unrounded `4.772·10⁻¹¹ + 251400/√x₊ = 1.14048·10⁻⁸` instead still gives `0.0754556…`.

The printed `0.075272` is the value of the same product with `ET ≤ 1.1377·10⁻⁸`. That is the
earlier preprint's figure (arXiv:1312.7748v2, (7.1), p. 56). The book updated it to `1.1405·10⁻⁸`
in (14.1), but the product was not recomputed. (The preprint's version of (14.7), its (7.8), has the
same `0.0754` and `8.7806`.)

Carried through, the chain becomes
`(8.70524 + O*(0.00007)) x + O*(0.075457) x = (8.7052 + O*(0.0756)) x ≤ 8.7808 x`. The first member
would then give `[8.629713 x, 8.780767 x]`, which sticks out of `(8.7052 ± 0.0754) x` at both ends.
So the printed `0.0754` and `8.7806` do not follow from [H]'s own inputs. They are still true, as
`eq_14_7_holds` certifies: the formalization treats the error terms differently and gets
`8.6759 x ≤ ∫ ≤ 8.769 x`. The second error term, printed `1.00393·10⁻⁸`, evaluates to
`≈ 1.0093·10⁻⁸` with `E_{η₊,r,δ₀} ≤ 2.3992·10⁻⁸` from (14.2). This is a separate slip, and a
negligible one.

The formal lower constant `8.6296` is exactly `8.7052 − 0.0756`, the lower end of the corrected
chain. The corrected first member still implies the formal bounds, since `8.6296 ≤ 8.629713` and
`8.780767 ≤ 8.79`. The repository's docstrings (the header of `MajorArcs/L2Major.lean`, and both
the module header and `l2_major_14_7` in `MinorArcs/PartIICited.lean`) quote [H, (14.7)] as
`(8.7052 + O*(0.0756)) x`. That `0.0756` is the constant of the corrected chain, not what [H]
prints, which is `O*(0.0754)`.
-/

namespace Companion.Book

open MeasureTheory
open TernaryGoldbach.Helfgott (S etaPlus majorArcs r₀)

/-- **[H, (14.7)]** as printed (p. 261). For every real `x ≥ x₊ = 4.9·10²⁶`,
`∫_{𝔐_{8,r₀}} |S_{η₊}(α,x)|² dα = (8.70524 + O*(0.00007)) x + O*(0.075273) x
= (8.7052 + O*(0.0754)) x ≤ 8.7806 x`.

How the statement is transcribed:
* **Range.** (14.7) prints no range of its own. The preamble of Ch. 14 fixes `x₊ = 4.9·10²⁶` and
  says the results must hold for every `x ≥ x₊`. The inputs of (14.7) are stated for that range:
  (14.1) is evaluated at `x₊`, and the bound on `K_{r,2}` is stated "for `x ≥ x₊`". So the range
  becomes `∀ x : ℝ, 4.9e26 ≤ x → …`, with `x` real. (In §14.4, `x = N/(2 + 9/(196√(2π)))`.)
* **Parameters.** `δ₀ = 8`: §14.1 says "Recall that `δ₀ = 8`". `r₀ = 150000`: the Ch. 14 preamble
  fixes `r = 150000`, (14.7) writes it as the subscript `r₀`, and §14.3 restates `r₀ = 150000`.
  So `𝔐_{8,r₀}` is `majorArcs 8 r₀ x`, with `TernaryGoldbach.Helfgott.r₀ = 150000`.
* **Major arcs.** `𝔐_{δ₀,r}` is the subset of `ℝ/ℤ` defined in (10.5). It is the union, over
  `a mod q` with `(a,q) = 1`, of the arcs `(a/q − δ₀r/(2qx), a/q + δ₀r/(2qx))` for odd `q ≤ r` and
  `(a/q − δ₀r/(qx), a/q + δ₀r/(qx))` for even `q ≤ 2r`. `TernaryGoldbach.Helfgott.majorArcs δ₀ r x`
  is the same union lifted to `ℝ`: `q ≥ 1` and all `a ∈ ℤ` with `IsCoprime a q`, which over `ℤ`
  means `gcd(a,q) = 1`. That is exactly the preimage of [H]'s set under `ℝ → ℝ/ℤ`. The arcs use
  the same `x` as `S_{η₊}(α,x)`, as in (10.5) and Lemma 10.3.1.
* **The integral.** [H]'s `∫_{𝔐} … dα` is over `ℝ/ℤ` with its Haar probability measure. It becomes
  `∫ α in Set.Ioc 0 1 ∩ majorArcs 8 r₀ x` with Lebesgue measure. This works because `(0,1]` is a
  fundamental domain and both the integrand and the lifted arcs are `1`-periodic
  (`eq_14_7_S_add_one`, `eq_14_7_majorArcs_add_one`). The integrand is continuous, hence
  integrable on this set (`eq_14_7_integrableOn`), so the Bochner integral is [H]'s integral.
  This is the same set expression as in `l2_major_bounds`.
* **Exponential sum.** (10.1) defines `S_η(α,x) = Σ_n Λ(n) e(αn) η(n/x)`. This is
  `TernaryGoldbach.Helfgott.S η x α` (note the argument order), the series
  `∑' n : ℕ, Λ(n) η(n/x) e(nα)` with `e(t) = exp(2πit)`. The extra `n = 0` term is zero because
  `Λ 0 = 0`. For `x > 0` the series converges absolutely
  (`TernaryGoldbach.Helfgott.summable_etaPlus`), so the `tsum` is the true sum. `|S|²` is written
  `‖S etaPlus x α‖ ^ 2`.
* **Smoothing.** [H] defines `η₊(t) = h₂₀₀(t) t e^{−t²/2}`, with `h_H(t) = ∫₀^∞ h(t/y) F_H(y) dy/y`,
  `h(t) = t²(2−t)³ e^{t−1/2}` on `[0,2]` (zero elsewhere) and `F_H(y) = sin(H log y)/(π log y)`
  ((7.4)–(7.6), restated in the Ch. 14 preamble; both print `F_H(t)` on the left of a formula in
  `y`, which we read as `F_H(y)`). `TernaryGoldbach.Helfgott.etaPlus` matches this
  definition for definition (`hBase`, `F`, `hH`, with `H = 200`). At `y = 1`, Lean's `F` takes the
  value `0/0 = 0` instead of the limit `H/π`. This is a single point and does not change the
  integral.
* **`O*`.** `O*(c)` stands for a quantity of absolute value at most `c`. Each `O*` becomes an
  existential `E` with `|E| ≤ c`. The first member has two of them: `E₁` in the main-term constant
  `8.70524 + O*(0.00007)` (that is, `L_{r,δ₀}`) and `E₂` in the error term `O*(0.075273) x`.
  Because `x > 0`, these existentials amount to explicit two-sided bounds (`eq_14_7_iff_bounds`).
* **The chain.** Each of the three members is asserted of the integral, and the three claims are
  joined by `∧`. The first claim implies the other two (`eq_14_7_iff_line1`).
* **Constants.** They are copied verbatim: `8.70524`, `0.00007`, `0.075273`, `8.7052`, `0.0754`,
  `8.7806`.
* **No hypotheses.** (14.7) is stated unconditionally ([H] treats Platt's GRH verification as a
  theorem), so the definition has no hypotheses. The formalization's `Fact` hypotheses appear only
  in `eq_14_7_holds`. -/
def eq_14_7 : Prop :=
  ∀ x : ℝ, (4.9e26 : ℝ) ≤ x →
    (∃ E₁ E₂ : ℝ, |E₁| ≤ 0.00007 ∧ |E₂| ≤ 0.075273 ∧
      ∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x, ‖S etaPlus x α‖ ^ 2 =
        (8.70524 + E₁) * x + E₂ * x) ∧
    (∃ E : ℝ, |E| ≤ 0.0754 ∧
      ∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x, ‖S etaPlus x α‖ ^ 2 = (8.7052 + E) * x) ∧
    ∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x, ‖S etaPlus x α‖ ^ 2 ≤ 8.7806 * x

/-- The first member of (14.7), for any real `I` and `x > 0`. There exist `E₁`, `E₂` with
`|E₁| ≤ 0.00007`, `|E₂| ≤ 0.075273` and `I = (8.70524 + E₁) x + E₂ x` if and only if
`8.629897 x ≤ I ≤ 8.780583 x`. Here `8.70524 ∓ (0.00007 + 0.075273) = 8.629897, 8.780583`. -/
theorem eq_14_7_line1_iff {I x : ℝ} (hx : 0 < x) :
    (∃ E₁ E₂ : ℝ, |E₁| ≤ 0.00007 ∧ |E₂| ≤ 0.075273 ∧ I = (8.70524 + E₁) * x + E₂ * x) ↔
      8.629897 * x ≤ I ∧ I ≤ 8.780583 * x := by
  constructor
  · rintro ⟨E₁, E₂, h₁, h₂, rfl⟩
    obtain ⟨h₁l, h₁u⟩ := abs_le.1 h₁
    obtain ⟨h₂l, h₂u⟩ := abs_le.1 h₂
    have a1 := mul_le_mul_of_nonneg_right h₁l hx.le
    have a2 := mul_le_mul_of_nonneg_right h₁u hx.le
    have a3 := mul_le_mul_of_nonneg_right h₂l hx.le
    have a4 := mul_le_mul_of_nonneg_right h₂u hx.le
    constructor <;> nlinarith
  · rintro ⟨hl, hu⟩
    have hpos : (0:ℝ) < 0.075343 * x := by positivity
    set t := (I - 8.70524 * x) / (0.075343 * x) with ht
    have htI : t * (0.075343 * x) = I - 8.70524 * x := div_mul_cancel₀ _ hpos.ne'
    have htab : |t| ≤ 1 := by
      rw [ht, abs_div, abs_of_pos hpos, div_le_one hpos, abs_le]
      constructor <;> linarith
    refine ⟨0.00007 * t, 0.075273 * t, ?_, ?_, ?_⟩
    · rw [abs_mul, abs_of_pos (by norm_num : (0:ℝ) < 0.00007)]
      nlinarith [abs_nonneg t]
    · rw [abs_mul, abs_of_pos (by norm_num : (0:ℝ) < 0.075273)]
      nlinarith [abs_nonneg t]
    · linear_combination -htI

/-- The second member of (14.7), for any real `I` and `x > 0`. There exists `E` with
`|E| ≤ 0.0754` and `I = (8.7052 + E) x` if and only if `8.6298 x ≤ I ≤ 8.7806 x`. -/
theorem eq_14_7_line2_iff {I x : ℝ} (hx : 0 < x) :
    (∃ E : ℝ, |E| ≤ 0.0754 ∧ I = (8.7052 + E) * x) ↔ 8.6298 * x ≤ I ∧ I ≤ 8.7806 * x := by
  constructor
  · rintro ⟨E, hE, rfl⟩
    obtain ⟨hl, hu⟩ := abs_le.1 hE
    have a1 := mul_le_mul_of_nonneg_right hl hx.le
    have a2 := mul_le_mul_of_nonneg_right hu hx.le
    constructor <;> nlinarith
  · rintro ⟨hl, hu⟩
    refine ⟨I / x - 8.7052, ?_, ?_⟩
    · rw [abs_le]
      constructor
      · rw [le_sub_iff_add_le, le_div_iff₀ hx]; linarith
      · rw [sub_le_iff_le_add, div_le_iff₀ hx]; linarith
    · have e : (8.7052 + (I / x - 8.7052) : ℝ) = I / x := by ring
      rw [e, div_mul_cancel₀ _ hx.ne']

/-- **Non-vacuity check.** The existential error terms of `eq_14_7` are real constraints. Since
`x > 0`, the printed chain is equivalent to the explicit bounds
`8.629897 x ≤ ∫_{𝔐_{8,r₀}} |S_{η₊}(α,x)|² dα ≤ 8.780583 x` for every `x ≥ 4.9·10²⁶`. -/
theorem eq_14_7_iff_bounds : eq_14_7 ↔ ∀ x : ℝ, (4.9e26 : ℝ) ≤ x →
    8.629897 * x ≤ ∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x, ‖S etaPlus x α‖ ^ 2 ∧
      ∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x, ‖S etaPlus x α‖ ^ 2 ≤ 8.780583 * x := by
  unfold eq_14_7
  refine forall_congr' fun x => imp_congr_right fun hx => ?_
  have hx0 : (0:ℝ) < x := by linarith
  rw [eq_14_7_line1_iff hx0, eq_14_7_line2_iff hx0]
  constructor
  · exact fun h => h.1
  · rintro ⟨hl, hu⟩
    exact ⟨⟨hl, hu⟩, ⟨by linarith, by linarith⟩, by linarith⟩

/-- **The chain's arithmetic is correct.** In (14.7), the second and third members follow from the
first: `[8.629897, 8.780583] ⊂ [8.7052 − 0.0754, 8.7052 + 0.0754] = [8.6298, 8.7806]`. So
`eq_14_7` is equivalent to its first member alone. The slip in (14.7) lies in an input of the
first member (see the module docstring), not in the chain. -/
theorem eq_14_7_iff_line1 : eq_14_7 ↔ ∀ x : ℝ, (4.9e26 : ℝ) ≤ x →
    ∃ E₁ E₂ : ℝ, |E₁| ≤ 0.00007 ∧ |E₂| ≤ 0.075273 ∧
      ∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x, ‖S etaPlus x α‖ ^ 2 =
        (8.70524 + E₁) * x + E₂ * x := by
  rw [eq_14_7_iff_bounds]
  refine forall_congr' fun x => imp_congr_right fun hx => ?_
  rw [eq_14_7_line1_iff (by linarith)]

/-- **[H, (14.7)] implies `l2_major_bounds`.** [H]'s bounds `8.629897 x ≤ ∫ ≤ 8.780583 x` (or the
printed `[8.6298 x, 8.7806 x]`) lie inside the formal `[8.6296 x, 8.79 x]`. The arcs, integrand
and range `x ≥ 4.9·10²⁶` are the same. The `Fact` hypotheses of the Lean theorem are not needed
for this implication. So the declared Lean statement is weaker than (14.7); the stronger
statement itself is `eq_14_7_holds`. -/
theorem eq_14_7_implies_formal :
    eq_14_7 → type_of% @TernaryGoldbach.MajorArcs.l2_major_bounds := by
  intro h _ x hx
  obtain ⟨hl, hu⟩ := eq_14_7_iff_bounds.1 h x (by linarith)
  exact ⟨by linarith, by linarith⟩

/-- **[H, (14.7)] implies `MinorArcs.l2_major_14_7`**, the restatement `|∫ − 8.7098 x| ≤ 0.0802 x`
that the minor-arc total consumes. From [H]'s bounds, `|∫ − 8.7098 x| ≤ 0.079903 x`. -/
theorem eq_14_7_implies_formal_cited :
    eq_14_7 → type_of% @TernaryGoldbach.MinorArcs.l2_major_14_7 := by
  intro h _ x hx
  obtain ⟨hl, hu⟩ := eq_14_7_iff_bounds.1 h x (by linarith)
  rw [abs_le]
  constructor <;> linarith

/-- **The slip in the error term of (14.7)**, as plain arithmetic.
* With [H]'s inputs `δ₀ = 8`, `r = 150000`, `ET_{η₊,δ₀r/2} ≤ 1.1405·10⁻⁸` (14.1) and
  `|η₊|₁ ≤ 1.062319` (14.3), the product `5.19 δ₀ r · ET · (|η₊|₁ + ET/2)` lies in
  `(0.075456, 0.075457]`, not below the printed `0.075272`.
* With the 2013 preprint's `ET ≤ 1.1377·10⁻⁸`, the same product is `≤ 0.075272`.
* With `0.075457` in place of `0.075273`, the first member gives
  `(8.70524 ∓ 0.075527) x = [8.629713 x, 8.780767 x]`. This interval sticks out of the printed
  `(8.7052 ± 0.0754) x` at both ends, but it fits in `(8.7052 ± 0.0756) x`, below `8.7808 x`, and
  inside the formal `[8.6296 x, 8.79 x]`.

The slip is in [H]'s derivation only: the printed bounds are nevertheless true (`eq_14_7_holds`). -/
theorem eq_14_7_slip :
    ((0.075456 : ℝ) < 5.19 * 8 * 150000 * (1.1405e-8 * (1.062319 + 1.1405e-8 / 2)) ∧
      (5.19 : ℝ) * 8 * 150000 * (1.1405e-8 * (1.062319 + 1.1405e-8 / 2)) ≤ 0.075457) ∧
    (5.19 : ℝ) * 8 * 150000 * (1.1377e-8 * (1.062319 + 1.1377e-8 / 2)) ≤ 0.075272 ∧
    ((8.70524 : ℝ) - 0.00007 - 0.075457 < 8.7052 - 0.0754 ∧
      (8.7052 : ℝ) + 0.0754 < 8.70524 + 0.00007 + 0.075457) ∧
    ((8.7052 : ℝ) - 0.0756 ≤ 8.70524 - 0.00007 - 0.075457 ∧
      (8.70524 : ℝ) + 0.00007 + 0.075457 ≤ 8.7052 + 0.0756 ∧
      (8.70524 : ℝ) + 0.00007 + 0.075457 ≤ 8.7808) ∧
    ((8.6296 : ℝ) ≤ 8.70524 - 0.00007 - 0.075457 ∧ (8.70524 : ℝ) + 0.00007 + 0.075457 ≤ 8.79) := by
  norm_num

/-- `S_η(·, x)` is continuous when `∑ₙ |Λ(n) η(n/x)| < ∞`. -/
private theorem eq_14_7_continuous_S {η : ℝ → ℝ} {x : ℝ}
    (h : Summable fun n : ℕ => ‖(((ArithmeticFunction.vonMangoldt n * η (n / x) : ℝ)) : ℂ)‖) :
    Continuous (S η x) :=
  TernaryGoldbach.continuous_expTsum h

/-- For `x > 0`, the integrand `|S_{η₊}(α,x)|²` of (14.7) is continuous in `α`. -/
private theorem eq_14_7_continuous_sq {x : ℝ} (hx : 0 < x) :
    Continuous fun α => ‖S etaPlus x α‖ ^ 2 :=
  (eq_14_7_continuous_S (TernaryGoldbach.Helfgott.summable_etaPlus hx)).norm.pow 2

/-- **Non-vacuity check.** For `x > 0`, the integrand `|S_{η₊}(α,x)|²` is continuous, hence
integrable on `(0,1] ∩ 𝔐_{8,r₀}`. So the integral in `eq_14_7` is the book's Lebesgue integral,
not Lean's default value `0`. -/
theorem eq_14_7_integrableOn {x : ℝ} (hx : 0 < x) :
    IntegrableOn (fun α => ‖S etaPlus x α‖ ^ 2) (Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x) :=
  ((eq_14_7_continuous_sq hx).integrableOn_Icc (a := 0) (b := 1)).mono_set
    (Set.inter_subset_left.trans Set.Ioc_subset_Icc_self)

/-! ### `(0,1]` stands for `ℝ/ℤ`

Two facts make `∫ α in (0,1] ∩ majorArcs 8 r₀ x` the book's `∫_{𝔐_{8,r₀}}` over `ℝ/ℤ`: the
integrand and the lifted arcs are both `1`-periodic. -/

/-- `e(n) = 1` for `n ∈ ℕ`. -/
private theorem eq_14_7_e_nat (n : ℕ) : TernaryGoldbach.e n = 1 := by
  unfold TernaryGoldbach.e
  have : (2 * Real.pi * Complex.I * ((n : ℝ) : ℂ)) = n * (2 * Real.pi * Complex.I) := by
    push_cast; ring
  rw [this]
  exact Complex.exp_nat_mul_two_pi_mul_I n

/-- `S_η(α + 1, x) = S_η(α, x)`, so the integrand of (14.7) is a function on `ℝ/ℤ`. -/
theorem eq_14_7_S_add_one (η : ℝ → ℝ) (x α : ℝ) : S η x (α + 1) = S η x α := by
  unfold TernaryGoldbach.Helfgott.S
  congr 1
  funext n
  rw [mul_add, mul_one, TernaryGoldbach.e_add, eq_14_7_e_nat, mul_one]

/-- A union of arcs `(a/q − w_q, a/q + w_q)`, taken over all `a ∈ ℤ` coprime to `q`, is
`1`-periodic. -/
private theorem eq_14_7_arcs_add_one (P : ℕ → Prop) (w : ℕ → ℝ) (α : ℝ) :
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

/-- `majorArcs δ₀ r x` is `1`-periodic, so it is the preimage in `ℝ` of a subset of `ℝ/ℤ`, namely
the book's `𝔐_{δ₀,r}` of (10.5). -/
theorem eq_14_7_majorArcs_add_one (δ₀ r x α : ℝ) :
    α + 1 ∈ majorArcs δ₀ r x ↔ α ∈ majorArcs δ₀ r x := by
  unfold TernaryGoldbach.Helfgott.majorArcs
  simp only [Set.mem_union]
  exact Iff.or
    (eq_14_7_arcs_add_one (fun q => (q : ℝ) ≤ r ∧ Odd q) (fun q => δ₀ * r / (2 * q * x)) α)
    (eq_14_7_arcs_add_one (fun q => (q : ℝ) ≤ 2 * r ∧ Even q) (fun q => δ₀ * r / (q * x)) α)

/-! ### (14.7) holds

`l2_major_bounds` sums the per-modulus bounds of `MajorArcs.Jq_bounds` over `q ∈ Qset r₀` and
multiplies the additive per-modulus errors `3.6·10⁻⁹ x` and `2.17·10⁻⁷ x` by the crude count
`#Qset r₀ ≤ 300000` of `MajorArcs.card_Qset_le`. The moduli of `𝔐_{8,r₀}` number `225000`, and
with that count the same sums give (14.7) as printed. -/

open TernaryGoldbach.MinorArcs (Qset qt)

/-- **The number of moduli of `𝔐_{8,r₀}`.** `Qset r₀` is the set of `q ≥ 1` with
`q̃ ≤ 2r₀ = 300000`, where `q̃ = q` for even `q` and `q̃ = 2q` for odd `q`. So it consists of the
`75000` odd `q ≤ 150000` (`q = 2k + 1`, `k < 75000`) and the `150000` even `q ≤ 300000`
(`q = 2k`, `1 ≤ k ≤ 150000`), and `#Qset r₀ ≤ 225000`. (Equality holds, but only the bound is
needed.) The repository's `MajorArcs.card_Qset_le` uses only `Qset r₀ ⊆ [1, 300000]` and gets
`300000`. -/
theorem eq_14_7_card_Qset_le : ((Qset r₀).card : ℝ) ≤ 225000 := by
  have hsub : Qset r₀ ⊆ (Finset.range 75000).image (fun k => 2 * k + 1) ∪
      (Finset.Icc 1 150000).image (fun k => 2 * k) := by
    intro q hq
    unfold Qset at hq
    rw [Finset.mem_filter, Finset.mem_Icc] at hq
    obtain ⟨⟨h1, _⟩, h2⟩ := hq
    have h2' : qt q ≤ 300000 := by
      have h3 : (2 * r₀ : ℝ) = 300000 := by norm_num [r₀]
      have h4 : (qt q : ℝ) ≤ 300000 := h3 ▸ h2
      exact_mod_cast h4
    unfold qt at h2'
    rw [Finset.mem_union, Finset.mem_image, Finset.mem_image]
    split_ifs at h2' with he
    · obtain ⟨k, hk⟩ := he
      right; exact ⟨k, Finset.mem_Icc.2 ⟨by omega, by omega⟩, by omega⟩
    · obtain ⟨k, hk⟩ := Nat.not_even_iff_odd.1 he
      left; exact ⟨k, Finset.mem_range.2 (by omega), by omega⟩
  have hcard := (Finset.card_le_card hsub).trans (Finset.card_union_le _ _)
  have h1 := Finset.card_image_le (s := Finset.range 75000) (f := fun k => 2 * k + 1)
  have h2 := Finset.card_image_le (s := Finset.Icc 1 150000) (f := fun k => 2 * k)
  rw [Finset.card_range] at h1
  rw [Nat.card_Icc] at h2
  exact_mod_cast (by omega : (Qset r₀).card ≤ 225000)

/-- **Sharper bounds from the formalization's own lemmas.** For `x ≥ 4.9·10²⁶`,
`8.6759 x ≤ ∫_{(0,1] ∩ 𝔐_{8,r₀}} |S_{η₊}(α,x)|² dα ≤ 8.769 x`.

This is the proof of `l2_major_bounds` with `eq_14_7_card_Qset_le` in place of `card_Qset_le`.
The integral equals the sum of the integrals over the arcs `J_{q,b}` of `𝔐_{8,r₀}`: it is at least
that sum by disjointness (`MinorArcs.sum_arcs_le_integral_majorArcs`) and at most that sum by
covering (`MinorArcs.integral_majorArcs_le`). Summing
`MajorArcs.Jq_bounds` over the moduli, with `Σ_q μ²(q)/φ(q) ∈ [13.597558, 13.59756]`
(`MajorArcs.sum_Qset_mPhi_bounds`) and `#Qset r₀ ≤ 225000`, gives
`(0.63907 − 0.000962)·13.597558 − 3.6·10⁻⁹·225000 = 8.675900…` from below and
`(0.64034 + 0.000962)·13.59756 + 2.17·10⁻⁷·225000 = 8.768967…` from above. -/
theorem eq_14_7_sharp_bounds [Fact TernaryGoldbach.PlattGRH] {x : ℝ}
    (hx : (4.9e26 : ℝ) ≤ x) :
    8.6759 * x ≤ ∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x, ‖S etaPlus x α‖ ^ 2 ∧
      ∫ α in Set.Ioc (0:ℝ) 1 ∩ majorArcs 8 r₀ x, ‖S etaPlus x α‖ ^ 2 ≤ 8.769 * x := by
  have hx0 : 0 < x := by linarith
  have hr₀ : r₀ = 150000 := rfl
  set g : ℝ → ℝ := fun α => ‖S etaPlus x α‖ ^ 2 with hg
  have hgc : Continuous g := eq_14_7_continuous_sq hx0
  have hper : Function.Periodic g 1 := fun α => by
    simp only [hg, eq_14_7_S_add_one]
  have hg0 : ∀ α, 0 ≤ g α := fun α => by positivity
  -- the integral over `(0,1] ∩ 𝔐_{8,r₀}` against the sum over the arcs `J_{q,b}`
  have hle := TernaryGoldbach.MinorArcs.integral_majorArcs_le hgc hper hg0 hx0 (δ₀ := 8) (R := r₀)
    (by rw [hr₀]; norm_num) (by rw [hr₀]; linarith)
  have hge := TernaryGoldbach.MinorArcs.sum_arcs_le_integral_majorArcs hgc hper hg0 hx0
    (δ₀ := 8) (Q := r₀) (by norm_num) (by rw [hr₀]; norm_num) (by rw [hr₀]; linarith)
    (by rw [hr₀]; linarith)
  -- the per-modulus bounds, summed over `q ∈ Qset r₀`
  have hlo := Finset.sum_le_sum fun q (hq : q ∈ Qset r₀) =>
    (TernaryGoldbach.MajorArcs.Jq_bounds hx hq).1
  have hhi := Finset.sum_le_sum fun q (hq : q ∈ Qset r₀) =>
    (TernaryGoldbach.MajorArcs.Jq_bounds hx hq).2
  rw [Finset.sum_sub_distrib, Finset.sum_sub_distrib, ← Finset.sum_mul, ← Finset.sum_mul,
    ← Finset.mul_sum, ← Finset.mul_sum, Finset.sum_const, nsmul_eq_mul] at hlo
  rw [Finset.sum_add_distrib, Finset.sum_add_distrib, ← Finset.sum_mul, ← Finset.sum_mul,
    ← Finset.mul_sum, ← Finset.mul_sum, Finset.sum_const, nsmul_eq_mul] at hhi
  obtain ⟨hm1, hm2⟩ := TernaryGoldbach.MajorArcs.sum_Qset_mPhi_bounds
  have hm1' : 13.597558 ≤ ∑ q ∈ Qset r₀, TernaryGoldbach.MajorArcs.mPhi q := hm1
  have hm2' : ∑ q ∈ Qset r₀, TernaryGoldbach.MajorArcs.mPhi q ≤ 13.59756 := hm2
  -- the count of moduli, `225000` instead of `card_Qset_le`'s `300000`
  have hc := eq_14_7_card_Qset_le
  have hc0 : (0 : ℝ) ≤ (Qset r₀).card := Nat.cast_nonneg _
  constructor
  · refine le_trans ?_ (hlo.trans hge)
    nlinarith
  · refine (hle.trans hhi).trans ?_
    nlinarith

/-- **[H, (14.7)] holds as printed**, under the `Fact` hypothesis `PlattGRH` of the formalization,
used through `MajorArcs.Jq_bounds`.
It follows from `eq_14_7_sharp_bounds` and `eq_14_7_iff_bounds`, since
`[8.6759, 8.769] ⊂ [8.629897, 8.780583]`. -/
theorem eq_14_7_holds [Fact TernaryGoldbach.PlattGRH] : eq_14_7 :=
  eq_14_7_iff_bounds.2 fun _ hx =>
    have h := eq_14_7_sharp_bounds hx
    ⟨by linarith [h.1], by linarith [h.2]⟩

end Companion.Book
