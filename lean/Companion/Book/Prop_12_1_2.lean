import TernaryGoldbach

/-!
# [H, Proposition 12.1.2]: the large sieve for primes on the major arcs `𝔐_{δ₀,Q₀}`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §12.1,
Proposition 12.1.2 (`prop:bellen`), p. 230 of the book
(https://arxiv.org/pdf/1501.05438v2#page=240); identical to [H13 = arXiv:1312.7748v2, Prop. 5.2].
Let `{aₙ}_{n ≥ 1} ⊂ ℂ` be supported on the primes, in `ℓ¹ ∩ ℓ²`, with `aₙ = 0` for `n ≤ √x`.
Let `Q₀ ≥ 1`, `δ₀ ≥ 1` with `δ₀ Q₀² ≤ x/2`, and set `Q = √(x/2δ₀) (≥ Q₀)`. Let
`𝔐 = 𝔐_{δ₀,Q₀}` be the major arcs of (10.5) and `S(α) = Σₙ aₙ e(αn)` on `ℝ/ℤ`. Then
`∫_𝔐 |S(α)|² dα ≤ (max_{q ≤ 2Q₀, q even} max_{s ≤ 2Q₀/q} G_q(2Q₀/sq) / G_q(2Q/sq)) Σₙ |aₙ|²`,
where `G_q(R) = Σ_{r ≤ R, (r,q) = 1} μ²(r)/φ(r)` (12.2).

**What the formalization proves.** `TernaryGoldbach.MinorArcs.prop_12_1_2`
(`TernaryGoldbach/MinorArcs/LargeSieveProof.lean:295`) proves the inequality with two changes:
1. it assumes `δ₀ ≥ 2` instead of `δ₀ ≥ 1`;
2. the double maximum is replaced by any `C` with `G_q(2Q₀/sq) ≤ C · G_q(2Q/sq)` for all even
   `1 ≤ q ≤ 2Q₀` and all real `1 ≤ s ≤ 2Q₀/q`.

**Relation, and how it is certified here.** Status: the book's statement is *proved*
(`prop_12_1_2_holds`); the repo's own theorem is a weaker special case
(`prop_12_1_2_implies_formal`).
* `prop_12_1_2_implies_formal : prop_12_1_2 → type_of% @TernaryGoldbach.MinorArcs.prop_12_1_2`.
  The Lean theorem is *weaker* than the book: change 1 narrows the range of `δ₀`; change 2 is an
  equivalent reformulation (`quotMax_12_1_2_le_iff`: the book's maximum is `≤ C` iff `C`
  satisfies the Lean hypothesis).
* `prop_12_1_2_holds : prop_12_1_2`: the book's statement itself, for every `δ₀ ≥ 1`, is proved
  here from the formalization's own lemmas (`integral_majorArcs_le`, `sum_arcs_eq_integral_Farc`,
  `Farc_le`, `sum_arcs_le_integral`, Plancherel). The restriction `δ₀ ≥ 2` in the repo is an artefact of its proof, which takes the
  common modulus `L = ∏_{q ≤ 2Q} q`: an odd `q ∈ (Q, 2Q]` may be a prime `p ∈ (√x, 2Q]` when
  `δ₀ < 2`. Only the moduli of `Qset Q` (odd `q ≤ Q`, even `q ≤ 2Q`) are needed, and an odd prime
  `p > √x` divides none of them once `δ₀ ≥ 1` (`p ∣ q` with `q̃ ≤ 2Q` forces `2p ≤ q̃ ≤ 2Q`, so
  `p ≤ Q < √x`); we take `L = ∏_{q ∈ Qset Q} q`. The prime `2` exceeds `√x` only if `x < 4`; then
  `1 ≤ Q₀ ≤ Q < 2`, the quotient at `q = 2`, `s = 1` is `1`, and Plancherel suffices. (The
  book's proof also needs coprimality only with these moduli; it justifies it for moduli
  `≤ √x`, which for `δ₀ < 2` leaves out the even moduli in `(√x, 2Q]`, but these are covered by
  the remark just made.)
* `prop_12_1_2_holds` takes no `Fact` hypothesis: none of the repo lemmas it calls (nor
  `TernaryGoldbach.MinorArcs.prop_12_1_2`) takes one.
* Non-vacuity: `prop_12_1_2_nontrivial` exhibits data satisfying every hypothesis with
  `Σ |aₙ|² > 0` and constant `≤ 2/3 < 1` (`x = 18`, `δ₀ = Q₀ = 1`, `a = 𝟙_{5}`), so the printed
  bound is strictly stronger than the trivial Plancherel bound `∫_𝔐 |S|² ≤ Σ |aₙ|²`.

In the main line [H] applies the proposition through Cor. 12.2.5 (`eq:pensat`, used in §13 with
`δ₀ = 8`; Lean: `TernaryGoldbach.MinorArcs.cor_12_2_5`, also with `δ₀ ≥ 2`), so the Lean
restriction `δ₀ ≥ 2` is harmless for the main theorem.
-/

open MeasureTheory Set

namespace Companion.Book

open TernaryGoldbach.MinorArcs (Gq)

/-! ## The book's constant -/

/-- The quotient `G_q(2Q₀/sq) / G_q(2Q/sq)` of [H, Prop. 12.1.2], with `Q = √(x/2δ₀)` read as
`√(x / (2δ₀))` and `2Q₀/sq`, `2Q/sq` read as `2Q₀/(s q)`, `2Q/(s q)`.
`Gq` is the repo's `G_q(R) = Σ_{1 ≤ r ≤ ⌊R⌋, (r, q) = 1} μ(r)²/φ(r)`, which agrees with [H, (12.2)]. -/
noncomputable def ratio_12_1_2 (x δ₀ Q₀ : ℝ) (q : ℕ) (s : ℝ) : ℝ :=
  Gq q (2 * Q₀ / (s * q)) / Gq q (2 * √(x / (2 * δ₀)) / (s * q))

/-- The values of the quotient over the range of the book's double maximum: `q` even with
`1 ≤ q ≤ 2Q₀`, and `s` real with `1 ≤ s ≤ 2Q₀/q`.

The printed subscript is `s ≤ 2Q₀/q`; the lower bound `s ≥ 1` is implicit: in the proof (via
Prop. 12.1.1) `s = max(1, |α|x/δ₀)`, and Prop. 12.2.4, which bounds this quotient, quantifies over
`s ∈ [1, Q₀/q]`. Without `s ≥ 1` the supremum would be `1` (each quotient is `≤ 1` and it tends to
`1` as `s → 0⁺`), not attained in general, and the statement would collapse to Plancherel. `s` is
real (not an integer), as in the proof. -/
def ratioSet_12_1_2 (x δ₀ Q₀ : ℝ) : Set ℝ :=
  {t | ∃ q : ℕ, 1 ≤ q ∧ Even q ∧ (q : ℝ) ≤ 2 * Q₀ ∧
    ∃ s : ℝ, 1 ≤ s ∧ s ≤ 2 * Q₀ / q ∧ t = ratio_12_1_2 x δ₀ Q₀ q s}

/-- The book's constant `max_{q ≤ 2Q₀, q even} max_{s ≤ 2Q₀/q} G_q(2Q₀/sq)/G_q(2Q/sq)`, written as
the supremum of `ratioSet_12_1_2`. The set is finite and, for `Q₀ ≥ 1`, nonempty, so the supremum
is attained (`quotMax_12_1_2_isGreatest`): it is the book's maximum. -/
noncomputable def quotMax_12_1_2 (x δ₀ Q₀ : ℝ) : ℝ := sSup (ratioSet_12_1_2 x δ₀ Q₀)

/-! ## The statement as printed -/

/-- **[H, Proposition 12.1.2]**, as printed (book p. 230).

Transcription:
* `x : ℝ` is the book's (implicit) real parameter; the hypotheses force `x ≥ 2`.
* The sequence `{aₙ}_{n ≥ 1}` is `a : ℕ → ℂ`; the extra value `a 0` is forced to be `0` by
  "supported on the primes", rendered `∀ n, a n ≠ 0 → n.Prime`.
* "`{aₙ}` is in `ℓ₁ ∩ ℓ₂`": `Summable (‖aₙ‖)` and `Summable (‖aₙ‖²)` (the second follows from the
  first; both are kept as printed).
* "`aₙ = 0` for `n ≤ √x`": `∀ n : ℕ, (n : ℝ) ≤ √x → a n = 0`.
* `Q₀ ≥ 1`, `δ₀ ≥ 1`, `δ₀ Q₀² ≤ x/2` verbatim. `Q = √(x/2δ₀)` is `√(x / (2 * δ₀))` (the proof
  uses `δ₀Q/(qx) = 1/(2qQ)`, i.e. `Q² = x/(2δ₀)`); the parenthetical "`≥ Q₀`" is a consequence
  (`le_sqrt_12_1_2`), not an extra hypothesis.
* `𝔐_{δ₀,Q₀} ⊂ ℝ/ℤ` is the book's (10.5) (`eq:majdef`): arcs `(a/q ∓ δ₀Q₀/(2qx))` for odd `q ≤ Q₀`
  and `(a/q ∓ δ₀Q₀/(qx))` for even `q ≤ 2Q₀`, `(a, q) = 1`. The repo's
  `TernaryGoldbach.Helfgott.majorArcs δ₀ Q₀ x` is exactly its preimage in `ℝ` (union over all
  integers `a` coprime to `q`, which is `1`-periodic), so the integral over `𝔐` for the Haar
  probability measure of `ℝ/ℤ` is the Lebesgue integral over `(0, 1] ∩ majorArcs δ₀ Q₀ x`.
* `S(α) = Σ aₙ e(αn)` is `TernaryGoldbach.expTsum a α = ∑' n, a n * e (n * α)` with
  `e t = exp(2πit)` (the book's `e`); `|S(α)|²` is `‖·‖ ^ 2` and `Σ |aₙ|²` is `∑' n, ‖a n‖ ^ 2`.
* The double maximum is `quotMax_12_1_2 x δ₀ Q₀` (see `ratioSet_12_1_2` for the range of `q, s`).
  Every denominator `G_q(2Q/sq)` is `≥ 1` on that range (`one_le_den_12_1_2`), so no division by
  zero occurs. -/
def prop_12_1_2 : Prop :=
  ∀ (x δ₀ Q₀ : ℝ) (a : ℕ → ℂ),
    (∀ n, a n ≠ 0 → n.Prime) →
    Summable (fun n => ‖a n‖) → Summable (fun n => ‖a n‖ ^ 2) →
    (∀ n : ℕ, (n : ℝ) ≤ √x → a n = 0) →
    1 ≤ Q₀ → 1 ≤ δ₀ → δ₀ * Q₀ ^ 2 ≤ x / 2 →
    ∫ α in Ioc (0 : ℝ) 1 ∩ TernaryGoldbach.Helfgott.majorArcs δ₀ Q₀ x,
        ‖TernaryGoldbach.expTsum a α‖ ^ 2 ≤
      quotMax_12_1_2 x δ₀ Q₀ * ∑' n, ‖a n‖ ^ 2

/-! ## Elementary facts about `G_q`

Restated here; the repo's versions are `Gq_mono` and `one_le_Gq_two`. -/

private theorem Gq_mono_aux {q : ℕ} {R R' : ℝ} (h : ⌊R⌋₊ ≤ ⌊R'⌋₊) : Gq q R ≤ Gq q R' := by
  unfold Gq
  refine Finset.sum_le_sum_of_subset_of_nonneg ?_ fun r _ _ => by positivity
  intro r hr
  simp only [Finset.mem_filter, Finset.mem_Icc] at hr ⊢
  exact ⟨⟨hr.1.1, hr.1.2.trans h⟩, hr.2⟩

private theorem one_le_Gq_aux (q : ℕ) {R : ℝ} (hR : 1 ≤ R) : 1 ≤ Gq q R := by
  unfold Gq
  have h1 : 1 ∈ (Finset.Icc 1 ⌊R⌋₊).filter (fun r => Nat.Coprime r q) := by
    simp only [Finset.mem_filter, Finset.mem_Icc]
    exact ⟨⟨le_rfl, Nat.le_floor (by exact_mod_cast hR)⟩, Nat.coprime_one_left q⟩
  refine le_trans ?_ (Finset.single_le_sum (fun r _ => by positivity) h1)
  simp

private theorem Gq_natFloor_aux (q : ℕ) (R : ℝ) : Gq q (⌊R⌋₊ : ℝ) = Gq q R := by
  simp only [Gq, Nat.floor_natCast]

private theorem Gq_two_one : Gq 2 1 = 1 := by
  unfold Gq
  rw [show ⌊(1 : ℝ)⌋₊ = 1 by norm_num]
  rw [show (Finset.Icc 1 1).filter (fun r => Nat.Coprime r 2) = {1} by decide]
  simp

private theorem Gq_two_three : Gq 2 3 = 3 / 2 := by
  unfold Gq
  rw [show ⌊(3 : ℝ)⌋₊ = 3 by norm_num]
  rw [show (Finset.Icc 1 3).filter (fun r => Nat.Coprime r 2) = {1, 3} by decide]
  rw [Finset.sum_insert (by decide), Finset.sum_singleton]
  simp [ArithmeticFunction.moebius_apply_prime Nat.prime_three, Nat.totient_prime Nat.prime_three]
  norm_num

/-! ## The book's maximum exists, and equals the `C` of the Lean statement -/

/-- The parenthetical `Q = √(x/2δ₀) ≥ Q₀` of [H] follows from `δ₀ Q₀² ≤ x/2`. -/
theorem le_sqrt_12_1_2 {x δ₀ Q₀ : ℝ} (hδ₀ : 0 < δ₀) (hx : δ₀ * Q₀ ^ 2 ≤ x / 2) :
    Q₀ ≤ √(x / (2 * δ₀)) := by
  apply Real.le_sqrt_of_sq_le
  rw [le_div_iff₀ (by positivity)]
  nlinarith

/-- On the range of the maximum, every denominator `G_q(2Q/sq)` is at least `1`. -/
theorem one_le_den_12_1_2 {x δ₀ Q₀ : ℝ} (hδ₀ : 0 < δ₀) (hx : δ₀ * Q₀ ^ 2 ≤ x / 2) {q : ℕ}
    (hq : 1 ≤ q) {s : ℝ} (hs1 : 1 ≤ s) (hs2 : s ≤ 2 * Q₀ / q) :
    1 ≤ Gq q (2 * √(x / (2 * δ₀)) / (s * q)) := by
  apply one_le_Gq_aux
  have hq' : (0 : ℝ) < q := by exact_mod_cast hq
  have hsq : 0 < s * q := mul_pos (by linarith) hq'
  rw [le_div_iff₀ hsq, one_mul]
  have h1 := (le_div_iff₀ hq').1 hs2
  have h2 := le_sqrt_12_1_2 hδ₀ hx
  linarith

theorem ratioSet_12_1_2_nonempty {x δ₀ Q₀ : ℝ} (hQ₀ : 1 ≤ Q₀) :
    (ratioSet_12_1_2 x δ₀ Q₀).Nonempty :=
  ⟨_, 2, by norm_num, even_two, by push_cast; linarith, 1, le_rfl,
    by rw [le_div_iff₀ (by norm_num)]; push_cast; linarith, rfl⟩

/-- The quotient takes finitely many values: `G_q(R)` depends only on `⌊R⌋`, and `q`, `⌊2Q₀/sq⌋`,
`⌊2Q/sq⌋` range over bounded sets of naturals. -/
theorem ratioSet_12_1_2_finite (x δ₀ Q₀ : ℝ) : (ratioSet_12_1_2 x δ₀ Q₀).Finite := by
  classical
  refine Set.Finite.subset ((Finset.Icc 1 ⌊2 * Q₀⌋₊ ×ˢ (Finset.range (⌊2 * Q₀⌋₊ + 1) ×ˢ
    Finset.range (⌊2 * √(x / (2 * δ₀))⌋₊ + 1))).image
      (fun p : ℕ × ℕ × ℕ => Gq p.1 p.2.1 / Gq p.1 p.2.2)).finite_toSet ?_
  rintro t ⟨q, hq1, -, hq2, s, hs1, hs2, rfl⟩
  have hq1' : (1 : ℝ) ≤ q := by exact_mod_cast hq1
  have hsq : 1 ≤ s * q := one_le_mul_of_one_le_of_one_le hs1 hq1'
  have h2Q₀ : 0 ≤ 2 * Q₀ := by linarith
  rw [Finset.coe_image]
  refine ⟨(q, ⌊2 * Q₀ / (s * q)⌋₊, ⌊2 * √(x / (2 * δ₀)) / (s * q)⌋₊), ?_, ?_⟩
  · rw [Finset.mem_coe, Finset.mem_product, Finset.mem_product, Finset.mem_Icc, Finset.mem_range,
      Finset.mem_range]
    exact ⟨⟨hq1, Nat.le_floor hq2⟩, Nat.lt_succ_of_le (Nat.floor_le_floor (div_le_self h2Q₀ hsq)),
      Nat.lt_succ_of_le (Nat.floor_le_floor (div_le_self (by positivity) hsq))⟩
  · simp only [ratio_12_1_2, Gq_natFloor_aux]

/-- **The book's `max` exists**: for `Q₀ ≥ 1`, `quotMax_12_1_2 x δ₀ Q₀` is the greatest value of the
quotient over the book's range. -/
theorem quotMax_12_1_2_isGreatest {x δ₀ Q₀ : ℝ} (hQ₀ : 1 ≤ Q₀) :
    IsGreatest (ratioSet_12_1_2 x δ₀ Q₀) (quotMax_12_1_2 x δ₀ Q₀) :=
  ⟨(ratioSet_12_1_2_nonempty hQ₀).csSup_mem (ratioSet_12_1_2_finite x δ₀ Q₀),
    fun _ ht => le_csSup (ratioSet_12_1_2_finite x δ₀ Q₀).bddAbove ht⟩

/-- **The maximum versus the hypothesis bound `C`**: under the book's hypotheses on `δ₀, Q₀`, the
book's maximum is `≤ C` iff `C` satisfies the hypothesis `hC` of
`TernaryGoldbach.MinorArcs.prop_12_1_2`. So replacing the maximum by such a `C` is an equivalent
reformulation. -/
theorem quotMax_12_1_2_le_iff {x δ₀ Q₀ C : ℝ} (hQ₀ : 1 ≤ Q₀) (hδ₀ : 0 < δ₀)
    (hx : δ₀ * Q₀ ^ 2 ≤ x / 2) :
    quotMax_12_1_2 x δ₀ Q₀ ≤ C ↔
      ∀ q : ℕ, 1 ≤ q → Even q → (q : ℝ) ≤ 2 * Q₀ → ∀ s : ℝ, 1 ≤ s → s ≤ 2 * Q₀ / q →
        Gq q (2 * Q₀ / (s * q)) ≤ C * Gq q (2 * √(x / (2 * δ₀)) / (s * q)) := by
  constructor
  · intro hle q hq1 hqe hq2 s hs1 hs2
    have hden := one_le_den_12_1_2 hδ₀ hx hq1 hs1 hs2
    have hmem : ratio_12_1_2 x δ₀ Q₀ q s ∈ ratioSet_12_1_2 x δ₀ Q₀ :=
      ⟨q, hq1, hqe, hq2, s, hs1, hs2, rfl⟩
    have h := ((quotMax_12_1_2_isGreatest hQ₀).2 hmem).trans hle
    rwa [ratio_12_1_2, div_le_iff₀ (by linarith)] at h
  · intro hC
    refine csSup_le (ratioSet_12_1_2_nonempty hQ₀) ?_
    rintro t ⟨q, hq1, hqe, hq2, s, hs1, hs2, rfl⟩
    rw [ratio_12_1_2, div_le_iff₀ (by linarith [one_le_den_12_1_2 hδ₀ hx hq1 hs1 hs2])]
    exact hC q hq1 hqe hq2 s hs1 hs2

/-- `ℓ¹ ⊆ ℓ²`: the book's `ℓ₁ ∩ ℓ₂` hypothesis is equivalent to the Lean `ℓ¹` hypothesis. -/
theorem summable_sq_of_summable_12_1_2 {a : ℕ → ℂ} (ha : Summable fun n => ‖a n‖) :
    Summable fun n => ‖a n‖ ^ 2 := by
  refine Summable.of_nonneg_of_le (fun n => by positivity) (fun n => ?_)
    (ha.mul_left (∑' m, ‖a m‖))
  have h := ha.le_tsum n (fun j _ => norm_nonneg (a j))
  rw [sq]
  exact mul_le_mul_of_nonneg_right h (norm_nonneg _)

/-! ## Relation to the formalization -/

/-- **The book's statement implies the Lean theorem** `TernaryGoldbach.MinorArcs.prop_12_1_2`
(which assumes `δ₀ ≥ 2` and an explicit bound `C` for the quotients). The Lean hypothesis
`PrimeSupported x a` bundles "supported on primes `> √x`" and `ℓ¹`; `ℓ²` follows from `ℓ¹`
(`summable_sq_of_summable_12_1_2`), `δ₀ ≥ 2` gives `δ₀ ≥ 1`, and the book's maximum is `≤ C` by
`quotMax_12_1_2_le_iff`. -/
theorem prop_12_1_2_implies_formal :
    prop_12_1_2 → type_of% @TernaryGoldbach.MinorArcs.prop_12_1_2 := by
  intro h x δ₀ Q₀ C a ha hδ₀ hQ₀ hx hC
  obtain ⟨hsupp, hsum⟩ := ha
  have hbook := h x δ₀ Q₀ a (fun n hn => (hsupp n hn).1) hsum
    (summable_sq_of_summable_12_1_2 hsum)
    (fun n hn => by
      by_contra h0
      exact absurd (hsupp n h0).2 (not_lt.2 hn)) hQ₀ (by linarith) hx
  refine hbook.trans (mul_le_mul_of_nonneg_right ?_ (tsum_nonneg fun n => by positivity))
  exact (quotMax_12_1_2_le_iff hQ₀ (by linarith) hx).2 hC

open TernaryGoldbach.MinorArcs (Qset Bset arc Farc qt two_le_qt even_qt expTsum_periodic
  integral_majorArcs_le sum_arcs_eq_integral_Farc integrable_Farc Farc_le sum_arcs_le_integral) in
/-- **[H, Prop. 12.1.2] holds as printed** (all `δ₀ ≥ 1`), by the formalization's argument with the
smaller common modulus `L = ∏_{q ∈ Qset Q} q` (see the module docstring); the case `x < 4`, where
the prime `2` may exceed `√x`, follows from Plancherel since the maximum is then `≥ 1`. -/
theorem prop_12_1_2_holds : prop_12_1_2 := by
  intro x δ₀ Q₀ a hprime hsum _ hsmall hQ₀ hδ₀ hx
  have hδ0 : 0 < δ₀ := by linarith
  have hC := (quotMax_12_1_2_le_iff hQ₀ hδ0 hx).1 le_rfl
  set C := quotMax_12_1_2 x δ₀ Q₀ with hCdef
  set Q := √(x / (2 * δ₀)) with hQdef
  have hx0 : 0 < x := by nlinarith
  have hQsq : Q ^ 2 = x / (2 * δ₀) := Real.sq_sqrt (by positivity)
  have hQ0 : 0 < Q := Real.sqrt_pos.2 (by positivity)
  have hδQ2 : δ₀ * Q ^ 2 = x / 2 := by rw [hQsq]; field_simp
  have hQ₀Q : Q₀ ≤ Q := le_sqrt_12_1_2 hδ0 hx
  have hδx : δ₀ ≤ x / 2 := by
    have : δ₀ * 1 ≤ δ₀ * Q₀ ^ 2 := mul_le_mul_of_nonneg_left (by nlinarith) hδ0.le
    linarith
  have hδQ : δ₀ * Q ≤ x := by
    have hsq : (δ₀ * Q) ^ 2 ≤ x ^ 2 := by
      rw [mul_pow, hQsq, show δ₀ ^ 2 * (x / (2 * δ₀)) = δ₀ * x / 2 by field_simp]
      nlinarith
    nlinarith [mul_pos hδ0 hQ0]
  -- the quotient at `q = 2`, `s = 1`, and `C ≥ 0`
  have hC2 := hC 2 (by norm_num) even_two (by push_cast; linarith) 1 le_rfl
    (by rw [le_div_iff₀ (by norm_num)]; push_cast; linarith)
  have e1 : 2 * Q₀ / (1 * ((2 : ℕ) : ℝ)) = Q₀ := by push_cast; ring
  have e2 : 2 * Q / (1 * ((2 : ℕ) : ℝ)) = Q := by push_cast; ring
  rw [e1, e2] at hC2
  have hG₀ : 1 ≤ Gq 2 Q₀ := one_le_Gq_aux 2 hQ₀
  have hGQ : 1 ≤ Gq 2 Q := one_le_Gq_aux 2 (hQ₀.trans hQ₀Q)
  have hC0 : 0 ≤ C := by nlinarith
  -- the integrand
  set g : ℝ → ℝ := fun α => ‖TernaryGoldbach.expTsum a α‖ ^ 2 with hgdef
  have hg : Continuous g := (TernaryGoldbach.continuous_expTsum hsum).norm.pow 2
  have hper : Function.Periodic g 1 := fun α => by simp only [g, expTsum_periodic a α]
  have hg0 : ∀ α, 0 ≤ g α := fun α => by positivity
  have hparseval : ∫ α in Ioc (0 : ℝ) 1, g α = ∑' n, ‖a n‖ ^ 2 :=
    TernaryGoldbach.setIntegral_norm_sq_expTsum hsum
  rcases lt_or_ge x 4 with hx4 | hx4
  · -- `x < 4`: then `1 ≤ Q₀ ≤ Q < 2`, so `C ≥ G_2(Q₀)/G_2(Q) = 1`, and Plancherel suffices
    have hQ2 : Q < 2 := by
      have : x / (2 * δ₀) ≤ x / 2 :=
        div_le_div_of_nonneg_left hx0.le (by norm_num) (by linarith)
      nlinarith
    have hfl : ⌊Q⌋₊ ≤ ⌊Q₀⌋₊ := by
      have h1 : ⌊Q⌋₊ < 2 := (Nat.floor_lt hQ0.le).2 (by exact_mod_cast hQ2)
      have h2 : 1 ≤ ⌊Q₀⌋₊ := Nat.le_floor (by exact_mod_cast hQ₀)
      omega
    have hmono : Gq 2 Q ≤ Gq 2 Q₀ := Gq_mono_aux hfl
    have hC1 : 1 ≤ C := by nlinarith
    calc ∫ α in Ioc (0 : ℝ) 1 ∩ TernaryGoldbach.Helfgott.majorArcs δ₀ Q₀ x,
          ‖TernaryGoldbach.expTsum a α‖ ^ 2
        ≤ ∫ α in Ioc (0 : ℝ) 1, g α :=
          setIntegral_mono_set (hg.integrableOn_Icc.mono_set Ioc_subset_Icc_self)
            (ae_of_all _ hg0) (LE.le.eventuallySubset inter_subset_left)
      _ = ∑' n, ‖a n‖ ^ 2 := hparseval
      _ ≤ C * ∑' n, ‖a n‖ ^ 2 :=
          le_mul_of_one_le_left (tsum_nonneg fun n => by positivity) hC1
  · -- `x ≥ 4`: every prime in the support is odd and coprime to every modulus of `Qset Q`
    have hsqx : 2 ≤ √x := by
      rw [show (2 : ℝ) = √4 by
        rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]]
      exact Real.sqrt_le_sqrt hx4
    have hQx : Q < √x := Real.sqrt_lt_sqrt (by positivity) (by
      rw [div_lt_iff₀ (by positivity)]
      nlinarith)
    have hQset1 : ∀ R, ∀ q ∈ Qset R, 1 ≤ q := fun R q hq =>
      (Finset.mem_Icc.1 (Finset.mem_filter.1 hq).1).1
    -- the common modulus: the product of the moduli of `𝔐_{δ₀,Q}`
    set L := ∏ q ∈ Qset Q, q with hL
    have hL0 : L ≠ 0 := Finset.prod_ne_zero_iff.2 fun q hq => by
      have := hQset1 Q q hq
      omega
    have : NeZero L := ⟨hL0⟩
    have hsub : ∀ R, R ≤ Q → Qset R ⊆ Qset Q := by
      intro R hR q hq
      simp only [Qset, Finset.mem_filter, Finset.mem_Icc] at hq ⊢
      exact ⟨⟨hq.1.1, hq.1.2.trans (Nat.floor_le_floor (by linarith))⟩, by linarith [hq.2]⟩
    have hqL : ∀ R, R ≤ Q → ∀ q ∈ Qset R, q ∣ L := fun R hR q hq =>
      Finset.dvd_prod_of_mem _ (hsub R hR hq)
    have hcop : ∀ n, a n ≠ 0 → Nat.Coprime n L := by
      intro n hn
      have hp := hprime n hn
      have hnx : √x < n := by
        by_contra hle
        exact hn (hsmall n (not_lt.1 hle))
      have hn2 : n ≠ 2 := by
        rintro rfl
        push_cast at hnx
        linarith
      refine Nat.Coprime.prod_right fun q hq => ?_
      have hq1 := hQset1 Q q hq
      have hqt : (qt q : ℝ) ≤ 2 * Q := (Finset.mem_filter.1 hq).2
      refine (Nat.coprime_or_dvd_of_prime hp q).resolve_right fun hdvd => ?_
      have h1 : n ∣ qt q := hdvd.trans (by unfold qt; split_ifs <;> simp)
      have h2 : 2 ∣ qt q := even_iff_two_dvd.1 (even_qt q)
      have h3 : 2 * n ∣ qt q :=
        Nat.Coprime.mul_dvd_of_dvd_of_dvd ((Nat.coprime_primes Nat.prime_two hp).2 hn2.symm) h2 h1
      have h4 : 2 * n ≤ qt q := Nat.le_of_dvd (by have := two_le_qt hq1; omega) h3
      have h5 : ((2 * n : ℕ) : ℝ) ≤ 2 * Q := le_trans (by exact_mod_cast h4) hqt
      push_cast at h5
      linarith
    have hδQ₀ : δ₀ * Q₀ ≤ x := by nlinarith
    calc ∫ α in Ioc (0 : ℝ) 1 ∩ TernaryGoldbach.Helfgott.majorArcs δ₀ Q₀ x,
          ‖TernaryGoldbach.expTsum a α‖ ^ 2
        ≤ ∑ q ∈ Qset Q₀, ∑ b ∈ Bset q, ∫ y in arc δ₀ Q₀ x q b, g y :=
          integral_majorArcs_le hg hper hg0 hx0 (by positivity) hδQ₀
      _ = ∫ β, Farc a δ₀ Q₀ x β := sum_arcs_eq_integral_Farc hsum δ₀ Q₀ x
      _ ≤ ∫ β, C * Farc a δ₀ Q x β :=
          integral_mono (integrable_Farc hsum _ _ _) ((integrable_Farc hsum _ _ _).const_mul C)
            fun β => Farc_le hx0 hQ₀ hQ₀Q hC0 hC (hqL Q₀ hQ₀Q) (hqL Q le_rfl) hsum hcop
      _ = C * ∑ q ∈ Qset Q, ∑ b ∈ Bset q, ∫ y in arc δ₀ Q x q b, g y := by
          rw [integral_const_mul, sum_arcs_eq_integral_Farc hsum δ₀ Q x]
      _ ≤ C * ∫ α in Ioc (0 : ℝ) 1, g α :=
          mul_le_mul_of_nonneg_left
            (sum_arcs_le_integral hg hper hg0 hx0 hδ0 hQ0 hδQ2.le hδQ) hC0
      _ = C * ∑' n, ‖a n‖ ^ 2 := by rw [hparseval]

/-! ## Non-vacuity -/

/-- For `x = 18`, `δ₀ = Q₀ = 1` (so `Q = 3`) the book's maximum is `G_2(1)/G_2(3) = 2/3`; we show
`≤ 2/3`. -/
theorem quotMax_12_1_2_example : quotMax_12_1_2 18 1 1 ≤ 2 / 3 := by
  rw [quotMax_12_1_2_le_iff le_rfl one_pos (by norm_num)]
  intro q hq1 hqe hq2 s hs1 hs2
  have hq : q = 2 := by
    have : q ≤ 2 := by exact_mod_cast (show (q : ℝ) ≤ 2 by linarith)
    obtain ⟨k, hk⟩ := hqe
    omega
  subst hq
  have hs : s = 1 := le_antisymm (by norm_num at hs2; linarith) hs1
  subst hs
  have h9 : √((18 : ℝ) / (2 * 1)) = 3 := by
    rw [show ((18 : ℝ) / (2 * 1)) = 3 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  rw [h9, show (2 : ℝ) * 1 / (1 * ((2 : ℕ) : ℝ)) = 1 by norm_num,
    show (2 : ℝ) * 3 / (1 * ((2 : ℕ) : ℝ)) = 3 by norm_num, Gq_two_one, Gq_two_three]
  norm_num

/-- **Non-vacuity of `prop_12_1_2`**: its hypotheses are satisfiable with `Σ |aₙ|² > 0` and a
constant `< 1`, so the printed bound is strictly stronger than Plancherel there. -/
theorem prop_12_1_2_nontrivial :
    ∃ (x δ₀ Q₀ : ℝ) (a : ℕ → ℂ), (∀ n, a n ≠ 0 → n.Prime) ∧ Summable (fun n => ‖a n‖) ∧
      Summable (fun n => ‖a n‖ ^ 2) ∧ (∀ n : ℕ, (n : ℝ) ≤ √x → a n = 0) ∧
      1 ≤ Q₀ ∧ 1 ≤ δ₀ ∧ δ₀ * Q₀ ^ 2 ≤ x / 2 ∧ 0 < ∑' n, ‖a n‖ ^ 2 ∧
      quotMax_12_1_2 x δ₀ Q₀ < 1 := by
  have hsum : Summable fun n : ℕ => ‖(if n = 5 then (1 : ℂ) else 0)‖ :=
    summable_of_ne_finset_zero (s := {5}) fun n hn => by
      rw [Finset.mem_singleton] at hn
      simp [hn]
  refine ⟨18, 1, 1, fun n => if n = 5 then 1 else 0, ?_, hsum,
    summable_sq_of_summable_12_1_2 hsum, ?_, le_rfl, le_rfl, by norm_num, ?_,
    lt_of_le_of_lt quotMax_12_1_2_example (by norm_num)⟩
  · intro n hn
    by_cases h : n = 5
    · subst h; norm_num
    · simp [h] at hn
  · intro n hn
    have h5 : n ≠ 5 := by
      rintro rfl
      have : √(18 : ℝ) < 5 := by rw [Real.sqrt_lt' (by norm_num)]; norm_num
      push_cast at hn
      linarith
    simp [h5]
  · have : (fun n : ℕ => ‖(if n = 5 then (1 : ℂ) else 0)‖ ^ 2) =
        fun n => if n = 5 then (1 : ℝ) else 0 := by
      funext n
      split_ifs <;> simp
    rw [this, tsum_ite_eq]
    norm_num

end Companion.Book
