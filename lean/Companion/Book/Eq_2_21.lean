import TernaryGoldbach

/-!
# [H, (2.21)]: Ramaré's bound `|∑_{n ≤ x} μ(n)/n| ≤ 0.03/log x` for `x ≥ 11815`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §2.5
("Bounds on sums of `μ` and `Λ`"), equation (2.21) (label `eq:marraki`), p. 37,
<https://arxiv.org/pdf/1501.05438v2#page=47>:
`|∑_{n ≤ x} μ(n)/n| ≤ 0.03/log x` for `x ≥ 11815`.
It is quoted from O. Ramaré, *From explicit estimates for primes to explicit estimates for the
Moebius function*, Acta Arith. 157 (2013), 365–379 (cf. M. El Marraki, J. Théor. Nombres Bordeaux
7 (1995), and Bordeaux preprint 96-8); [H] gives no proof. The statement is identical to (2.8) of
the minor-arcs preprint arXiv:1205.5252v4. [H] uses it at real arguments (e.g. (5.26), in the
proof of Lemma 5.1.2, bounds `f(t) = |∑_{r ≤ t} μ(r)/r|` for real `1 ≤ t ≤ x`).

**What the formalization does.** It does not prove this bound. It takes it, in exactly this form,
as the hypothesis `TernaryGoldbach.RamareMoebius` (`TernaryGoldbach/Statement.lean`), one of the
three hypotheses of the main theorem `TernaryGoldbach.ternary_goldbach_of_hypotheses`; inside the
proof it is passed as `[Fact TernaryGoldbach.RamareMoebius]` and unpacked by
`TernaryGoldbach.Prelim.ramare_moebius`.

**Relation, certified here.** `eq_2_21_iff : eq_2_21 ↔ TernaryGoldbach.RamareMoebius`. Here
`eq_2_21` is the printed statement transcribed independently: the sum over the positive integers
`n ≤ x` is written literally as a `finsum` over `{n : ℕ | 1 ≤ n ∧ (n : ℝ) ≤ x}`, where the
formalization writes `∑ n ∈ Finset.Icc 1 ⌊x⌋₊`; `eq_2_21_finsum_eq_sum_Icc` identifies the two.
Everything else (real `x`, the range `x ≥ 11815`, the constant `0.03`, the natural logarithm,
Mathlib's Möbius function) is the same on both sides. So the book's statement *is* the
formalization's hypothesis: status **equivalent-hypothesis**.

**Auxiliary checks.**
* `eq_2_21_moebius_eq_book` and `eq_2_21_book_moebius_unique`: Mathlib's
  `ArithmeticFunction.moebius` satisfies the two clauses of the book's definition of `μ` ([H, §2.1]),
  and these clauses determine a function on the positive integers, so reusing Mathlib's `μ` is
  faithful.
* `eq_2_21_range_needed`: the printed inequality is false at `x = 2`, so the conclusion has content
  (the def is not vacuously true) and the range hypothesis `x ≥ 11815` is load-bearing.
* Numerically (Python, not part of this file; `m(N) := ∑_{n ≤ N} μ(n)/n`): with
  double-precision (Kahan-summed) partial sums, the bound holds for every real
  `x ∈ [11815, 3·10⁶)`, the largest value of `|m(x)| · log x / 0.03` there being `≈ 0.98320`
  (as `x → 11821⁻`). With exact rational partial sums near the threshold,
  `m(11814) ≈ 0.0032300058 > 0.03/log 11814 ≈ 0.0031993036`, so the bound fails for every real
  `x ∈ [11814, 11815)`, while it holds at `x = 11815` (`m(11815) ≈ 0.0031453676`). So the
  threshold `11815` is sharp, and the printed statement agrees with the computation in the range
  checked. (No proof of the bound itself is attempted here: it is a published result.)
-/

namespace Companion.Book

/-- **[H, (2.21)] as printed** (Ramaré): for `x ≥ 11815`,
`|∑_{n ≤ x} μ(n)/n| ≤ 0.03/log x`.

Transcription choices:
* `x` is a real number: the book's `x` in §2.5 is real ((2.24) is stated "for all real
  `x ≤ 10¹²`"), and [H] applies (2.21) at real arguments ((5.26)). Writing
  `m(N) = ∑_{n ≤ N} μ(n)/n`, the bound must then hold on each whole interval `[N, N + 1)`, i.e.
  `|m(N)| ≤ 0.03/log(N + 1)` for every integer `N ≥ 11815`; this is stronger than the reading with
  `x` an integer (`|m(N)| ≤ 0.03/log N`).
* The range `x ≥ 11815` is the hypothesis `11815 ≤ x`.
* `∑_{n ≤ x}` ranges over the *positive* integers `n ≤ x` ([H, §2.1]: `∑_n` means `∑_{n=1}^∞`).
  It is written literally as the `finsum` over `{n : ℕ | 1 ≤ n ∧ (n : ℝ) ≤ x}`, with the comparison
  `n ≤ x` made in `ℝ` (no floor). This set is finite, so the `finsum` is the genuine finite sum
  (`eq_2_21_finsum_eq_sum_Icc`).
* `μ` is Mathlib's `ArithmeticFunction.moebius` (`ℤ`-valued, cast to `ℝ`), which agrees with the
  book's definition on positive integers (`eq_2_21_moebius_eq_book`,
  `eq_2_21_book_moebius_unique`); `μ(n)/n` is the real quotient `(μ n : ℝ) / (n : ℝ)`.
* `log` is the natural logarithm `Real.log` (positive for `x ≥ 11815`); `0.03` is the real number
  `3/100`; `|·|` is the real absolute value. -/
def eq_2_21 : Prop :=
  ∀ x : ℝ, 11815 ≤ x →
    |∑ᶠ n ∈ {n : ℕ | 1 ≤ n ∧ (n : ℝ) ≤ x}, (ArithmeticFunction.moebius n : ℝ) / n|
      ≤ 0.03 / Real.log x

/-- The book's sum over the positive integers `n ≤ x` is the formalization's sum over
`Finset.Icc 1 ⌊x⌋₊` (for every real `x`). -/
theorem eq_2_21_finsum_eq_sum_Icc (f : ℕ → ℝ) (x : ℝ) :
    ∑ᶠ n ∈ {n : ℕ | 1 ≤ n ∧ (n : ℝ) ≤ x}, f n = ∑ n ∈ Finset.Icc 1 ⌊x⌋₊, f n := by
  have hset : {n : ℕ | 1 ≤ n ∧ (n : ℝ) ≤ x} = ↑(Finset.Icc 1 ⌊x⌋₊) := by
    ext n
    simp only [Set.mem_ofPred_eq, Finset.coe_Icc, Set.mem_Icc]
    constructor
    · rintro ⟨h1, h2⟩
      exact ⟨h1, (Nat.le_floor_iff' (by omega)).2 h2⟩
    · rintro ⟨h1, h2⟩
      exact ⟨h1, (Nat.le_floor_iff' (by omega)).1 h2⟩
  rw [hset, finsum_mem_coe_finset]

/-- **[H, (2.21)] is exactly the formalization's hypothesis** `TernaryGoldbach.RamareMoebius`. -/
theorem eq_2_21_iff : eq_2_21 ↔ TernaryGoldbach.RamareMoebius := by
  unfold eq_2_21 TernaryGoldbach.RamareMoebius
  refine forall_congr' fun x => ?_
  rw [eq_2_21_finsum_eq_sum_Icc]

/-- Mathlib's `μ` satisfies the two clauses of the book's definition ([H, §2.1]):
`μ(n) = (-1)^k` if `n = p₁ ⋯ p_k` with all `pᵢ` distinct primes (a finite set `S` of primes,
`k = |S|`), and `μ(n) = 0` if `p² ∣ n` for some prime `p`. -/
theorem eq_2_21_moebius_eq_book :
    (∀ S : Finset ℕ, (∀ p ∈ S, p.Prime) →
        ArithmeticFunction.moebius (∏ p ∈ S, p) = (-1) ^ S.card) ∧
      (∀ n p : ℕ, p.Prime → p ^ 2 ∣ n → ArithmeticFunction.moebius n = 0) := by
  refine ⟨fun S hS => ?_, fun n p hp hdvd => ?_⟩
  · rw [ArithmeticFunction.isMultiplicative_moebius.map_prod_of_prime S hS,
      Finset.prod_congr rfl fun p hp => ArithmeticFunction.moebius_apply_prime (hS p hp),
      Finset.prod_const]
  · apply ArithmeticFunction.moebius_eq_zero_of_not_squarefree
    intro hsq
    exact hp.one_lt.ne' (Nat.isUnit_iff.1 (hsq p (by rwa [← sq])))

/-- The two clauses of the book's definition of `μ` determine it on the positive integers: any
`f` satisfying them agrees there with Mathlib's `ArithmeticFunction.moebius`. -/
theorem eq_2_21_book_moebius_unique (f : ℕ → ℤ)
    (h1 : ∀ S : Finset ℕ, (∀ p ∈ S, p.Prime) → f (∏ p ∈ S, p) = (-1) ^ S.card)
    (h2 : ∀ n p : ℕ, 0 < n → p.Prime → p ^ 2 ∣ n → f n = 0) {n : ℕ} (hn : 0 < n) :
    f n = ArithmeticFunction.moebius n := by
  by_cases hsq : Squarefree n
  · have hS : ∀ p ∈ n.primeFactors, p.Prime := fun p hp => Nat.prime_of_mem_primeFactors hp
    rw [← Nat.prod_primeFactors_of_squarefree hsq, h1 _ hS, eq_2_21_moebius_eq_book.1 _ hS]
  · obtain ⟨p, hp, hdvd⟩ : ∃ p, p.Prime ∧ p * p ∣ n := by
      by_contra hcon
      exact hsq (Nat.squarefree_iff_prime_squarefree.2 fun p hp hdvd => hcon ⟨p, hp, hdvd⟩)
    rw [h2 n p hn hp (by rwa [sq]), ArithmeticFunction.moebius_eq_zero_of_not_squarefree hsq]

/-- Non-vacuity check: without the range hypothesis the printed inequality is false (at `x = 2`
the sum is `1 - 1/2 = 1/2 > 0.03/log 2 ≈ 0.0433`). So the conclusion of `eq_2_21` is a genuine
constraint and the hypothesis `x ≥ 11815` is load-bearing. -/
theorem eq_2_21_range_needed :
    ¬ ∀ x : ℝ, 1 < x →
      |∑ᶠ n ∈ {n : ℕ | 1 ≤ n ∧ (n : ℝ) ≤ x}, (ArithmeticFunction.moebius n : ℝ) / n|
        ≤ 0.03 / Real.log x := by
  intro h
  have h2 := h 2 one_lt_two
  rw [eq_2_21_finsum_eq_sum_Icc, Nat.floor_ofNat] at h2
  have hsum : ∑ n ∈ Finset.Icc 1 2, (ArithmeticFunction.moebius n : ℝ) / n = 1 / 2 := by
    rw [show Finset.Icc 1 2 = {1, 2} by decide, Finset.sum_pair (by norm_num),
      ArithmeticFunction.moebius_apply_prime Nat.prime_two, ArithmeticFunction.moebius_apply_one]
    norm_num
  rw [hsum, abs_of_pos (by norm_num)] at h2
  have hlog : (0.69 : ℝ) < Real.log 2 := lt_trans (by norm_num) Real.log_two_gt_d9
  have hlt : (0.03 : ℝ) / Real.log 2 < 1 / 2 := by
    rw [div_lt_iff₀ (by linarith)]
    linarith
  linarith

end Companion.Book
