import TernaryGoldbach

/-!
# [H, Proposition 12.2.4]: the quotient in the large sieve for primes

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2,
§12.2, Proposition 12.2.4 (printed at the top of p. 236, PDF page 246:
<https://arxiv.org/pdf/1501.05438v2#page=246>). Let `Q ≥ 20000 Q₀` and `Q₀ ≥ Q_{0,min} = 10⁵`,
and let `ρ = (log Q₀)/log Q ≤ 0.6`. Then, for every `1 ≤ q ≤ Q₀` and every `s ∈ [1, Q₀/q]`,

  `G_q(Q₀/sq) / G_q(Q/sq) ≤ (log Q₀ + c₊)/(log Q + c_E)`,    (12.23)

where `G_q(R) = ∑_{r ≤ R, (r,q)=1} μ²(r)/φ(r)` (12.2),
`c_E = γ + ∑_p log p/(p(p−1)) = 1.3325822…` (12.14), and `c₊ = 1.36`. The statement is the same
as in the 2013 version ([arXiv:1312.7748v2](https://arxiv.org/abs/1312.7748v2), Prop. 5.6).

**What the formalization proves.** `TernaryGoldbach.MinorArcs.prop_12_2_4`
(`TernaryGoldbach/MinorArcs/LSQuot6.lean:69`), under `[Fact PlattGRH]` (really used,
through `regionS`): in the same range of `Q, Q₀, q, s`,

  `G_q(Q₀/(sq)) ≤ (log Q₀ + 2)/(log Q + cE) · G_q(Q/(sq))`,

that is, (12.23) with two weaker constants:
* `c₊ = 2` in place of `1.36`: a larger numerator, so a weaker bound;
* `cE = 1.33258` (`MinorArcs.cE`) in place of `c_E = 1.3325822…`: `c_E` rounded *down*, so a
  smaller denominator and again a weaker bound (`prop_12_2_4_cE_round_down`, from the repo's
  `1.3325822 ≤ c_E ≤ 1.3325823`, `Prelim.RamPf.cR_bounds`).
It also multiplies out the quotient, and writes `ρ ≤ 0.6` as `log Q₀ ≤ 0.6 log Q` and `10⁵` as
`1e5`; these are equivalent in this range, because `log Q > 0` and `G_q(Q/sq) ≥ 1`.
For `q ≥ 2.2·10¹⁰` the Lean proof follows [H] and reaches `1.36` (still with `cE`), then weakens
it (`MinorArcs.weaken_136`). For `q < 2.2·10¹⁰` it uses a reduction to the divisors of `30030`
and kernel checks (`checkC2_suffices`, `Phi2_small`, `Phi2_reduce`, `Phi2_base`), which need the
room that `c₊ = 2` gives. [H]'s constant `1.36` is not proved in Lean.

**Relation: [H]'s statement implies the formal one** (`prop_12_2_4_implies_formal`, stated
against `type_of% @TernaryGoldbach.MinorArcs.prop_12_2_4`), so the formal result is weaker. The
proof does not use the `Fact`. It uses only `G_q(Q/sq) ≥ 1` (the term `r = 1`) and the crude
bound `c_E > 1/2` (`γ > 1/2`, and the prime sum is `≥ 0`). The room from `c₊ = 2` absorbs the
rest: `(l + 1.36)(L + 1.33258) ≤ (l + 2)(L + c)` whenever `c ≥ 1/2`, `0 ≤ l ≤ 0.6 L`, `L ≥ 6`.

(Two slips in [H]'s *proof*, recorded in the repo's `AXIOMS.md`, Finding 4, and checked again
here: the proof applies Lemma 12.2.3 with `σ = c₊`, but that lemma's denominator is
`log Q + 1.312 < log Q + c_E`, so it gives (12.23) only for `σ ≲ 1.3477`; and (12.15) follows from
(12.12) only for `R ≥ (7.284/(c_E − 1.312))³ ≈ 4.43·10⁷`, not from `4·10⁷`. Neither changes the
printed statement transcribed here.)

**Non-vacuity.** `prop_12_2_4_base_point` specialises [H]'s statement to `Q = 10¹⁰`, `Q₀ = 10⁵`,
`q = s = 1`, discharging every hypothesis. There it says
`G(10⁵)/G(10¹⁰) ≤ (log 10⁵ + 1.36)/(log 10¹⁰ + c_E)`. Numerically (not checked in Lean):
`G(10⁵) = 12.84551…` by a float computation, and `G(10¹⁰) = log 10¹⁰ + c_E + O*(0.0034)` by
(12.12), so the left side is in `[0.52728, 0.52743]` and the right side is `0.52848`. The claim is
true there, with little room. The formal bound at the same point is about `0.55475`.
-/

open TernaryGoldbach
open TernaryGoldbach.MinorArcs (Gq cE)
open TernaryGoldbach.Prelim.RamPf (cR)
open scoped ArithmeticFunction.Moebius

namespace Companion.Book

/-- **[H, Proposition 12.2.4]**, as printed (p. 236):
for `Q ≥ 20000 Q₀`, `Q₀ ≥ 10⁵`, `ρ = (log Q₀)/log Q ≤ 0.6`, every integer `1 ≤ q ≤ Q₀` and every
real `s ∈ [1, Q₀/q]`, `G_q(Q₀/sq)/G_q(Q/sq) ≤ (log Q₀ + 1.36)/(log Q + c_E)`.

Transcription choices:
* `Q`, `Q₀`, `s` are real, `q` is a natural number (a modulus: `G_q` needs `(r, q) = 1`).
  `Q₀ ≥ Q_{0,min}` is written with the printed value `Q_{0,min} = 10⁵`, and `c₊` with its value
  `1.36`.
* `ρ ≤ 0.6` is kept as the printed quotient `log Q₀ / log Q ≤ 0.6`. Under the other hypotheses
  `Q ≥ 2·10⁹`, so `log Q > 0` and Lean's `x / 0 = 0` never matters.
* `Q₀/sq` is read as `Q₀/(s q)`, the usual reading (and the one [H]'s proof uses: `R = Q₀/sq`).
* The quotient is a real division, as printed. Its denominator is `≥ 1` (`Q/(sq) ≥ Q/Q₀ ≥ 20000`
  and the term `r = 1`; see `prop_12_2_4_one_le_Gq`), so the division is genuine.
* `G_q` is the repo's `MinorArcs.Gq`, which is [H, (12.2)]: a sum over `r ∈ [1, ⌊R⌋₊]` with
  `Nat.Coprime r q` of `μ(r)²/φ(r)`, i.e. over the positive integers `r ≤ R`
  (`prop_12_2_4_Gq_eq`).
* `c_E` is the repo's `Prelim.RamPf.cR = γ + ∑' p, [p prime] log p/(p(p−1))`, which is
  [H, (12.14)] (`prop_12_2_4_cE_eq`). The series is summable (`Prelim.RamPf.summable_sumP`), so
  the `tsum` is the true sum, and `Prelim.RamPf.cR_bounds` gives `1.3325822 ≤ cR ≤ 1.3325823`,
  matching the printed `1.3325822…`. It is *not* the formalization's rounded
  `MinorArcs.cE = 1.33258`. -/
def prop_12_2_4 : Prop :=
  ∀ Q Q₀ : ℝ, 20000 * Q₀ ≤ Q → (10 : ℝ) ^ 5 ≤ Q₀ → Real.log Q₀ / Real.log Q ≤ 0.6 →
    ∀ q : ℕ, 1 ≤ q → (q : ℝ) ≤ Q₀ → ∀ s : ℝ, 1 ≤ s → s ≤ Q₀ / q →
      Gq q (Q₀ / (s * q)) / Gq q (Q / (s * q)) ≤ (Real.log Q₀ + 1.36) / (Real.log Q + cR)

/-- [H, (12.2)]: the repo's `MinorArcs.Gq` is `G_q(R) = ∑_{r ≤ R, (r,q)=1} μ²(r)/φ(r)`
(definitionally; `r` runs over `[1, ⌊R⌋₊]`, i.e. over the positive integers `r ≤ R`). -/
theorem prop_12_2_4_Gq_eq (q : ℕ) (R : ℝ) :
    Gq q R =
      ∑ r ∈ (Finset.Icc 1 ⌊R⌋₊).filter (fun r => Nat.Coprime r q),
        ((μ r : ℝ)) ^ 2 / Nat.totient r :=
  rfl

/-- [H, (12.14)]: the repo's `Prelim.RamPf.cR` is `c_E = γ + ∑_p log p/(p(p−1))`
(definitionally; the sum over primes is written as a `tsum` over `ℕ` with an indicator). -/
theorem prop_12_2_4_cE_eq :
    cR = Real.eulerMascheroniConstant +
      ∑' p : ℕ, if p.Prime then Real.log p / ((p : ℝ) * ((p : ℝ) - 1)) else 0 :=
  rfl

/-- `G_q(R) ≥ 1` for `R ≥ 1` (the term `r = 1`). -/
theorem prop_12_2_4_one_le_Gq (q : ℕ) {R : ℝ} (hR : 1 ≤ R) : 1 ≤ Gq q R := by
  rw [prop_12_2_4_Gq_eq]
  have h1 : 1 ∈ (Finset.Icc 1 ⌊R⌋₊).filter (fun r => Nat.Coprime r q) := by
    simp only [Finset.mem_filter, Finset.mem_Icc]
    exact ⟨⟨le_rfl, Nat.le_floor (by exact_mod_cast hR)⟩, Nat.coprime_one_left q⟩
  refine le_trans ?_ (Finset.single_le_sum (fun r _ => by positivity) h1)
  simp

/-- The crude bound `c_E > 1/2`: `γ > 1/2` and every term of the prime sum is `≥ 0`.
(No `Fact` is needed; this is all `prop_12_2_4_implies_formal` uses about `c_E`.) -/
theorem prop_12_2_4_half_lt_cE : (1 / 2 : ℝ) < cR := by
  have hγ := Real.one_half_lt_eulerMascheroniConstant
  have hS : 0 ≤ ∑' p : ℕ, if p.Prime then Real.log p / ((p : ℝ) * ((p : ℝ) - 1)) else 0 := by
    refine tsum_nonneg fun p => ?_
    split_ifs with hp
    · have hp1 : (1 : ℝ) < p := by exact_mod_cast hp.one_lt
      exact div_nonneg (Real.log_natCast_nonneg p) (by nlinarith)
    · exact le_rfl
  rw [prop_12_2_4_cE_eq]
  linarith

/-- The formalization's `cE = 1.33258` is [H]'s `c_E = 1.3325822…` rounded **down**, so using it
in the denominator of (12.23) weakens the bound. This uses the repo's `Prelim.RamPf.cR_bounds`,
which has no hypotheses. -/
theorem prop_12_2_4_cE_round_down : cE < cR := by
  have h := Prelim.RamPf.cR_bounds.1
  unfold cE
  linarith

/-- **[H, Prop 12.2.4] implies the formalization's `MinorArcs.prop_12_2_4`** (which has `c₊ = 2`
and `cE = 1.33258`), so the formal result is weaker. The `Fact PlattGRH` argument of the formal
statement is not used. -/
theorem prop_12_2_4_implies_formal :
    prop_12_2_4 → type_of% @TernaryGoldbach.MinorArcs.prop_12_2_4 := by
  intro h _ Q Q₀ hQ hQ₀ hρ q hq hqQ s hs hsQ
  have h5 : (100000 : ℝ) ≤ Q₀ := by norm_num at hQ₀; exact hQ₀
  have hQ₀' : (10 : ℝ) ^ 5 ≤ Q₀ := by norm_num; exact h5
  have hQ9 : (2 : ℝ) ^ 9 ≤ Q := by norm_num; linarith
  have hL : 0 < Real.log Q := Real.log_pos (by linarith)
  have hL6 : 6 ≤ Real.log Q := by
    have h1 := Real.log_le_log (by norm_num) hQ9
    rw [Real.log_pow] at h1
    have := Real.log_two_gt_d9
    push_cast at h1
    linarith
  have hρ' : Real.log Q₀ / Real.log Q ≤ 0.6 := (div_le_iff₀ hL).2 hρ
  have hb := h Q Q₀ hQ hQ₀' hρ' q hq hqQ s hs hsQ
  have hq0 : (0 : ℝ) < q := by exact_mod_cast hq
  have hsq : 0 < s * q := mul_pos (by linarith) hq0
  have hsqQ₀ : s * q ≤ Q₀ := (le_div_iff₀ hq0).1 hsQ
  have hR1 : 1 ≤ Q / (s * q) := by rw [le_div_iff₀ hsq, one_mul]; linarith
  have hG0 : 0 < Gq q (Q / (s * q)) := lt_of_lt_of_le one_pos (prop_12_2_4_one_le_Gq q hR1)
  refine ((div_le_iff₀ hG0).1 hb).trans (mul_le_mul_of_nonneg_right ?_ hG0.le)
  have hc := prop_12_2_4_half_lt_cE
  have hl0 : 0 ≤ Real.log Q₀ := Real.log_nonneg (by linarith)
  have hd1 : 0 < Real.log Q + cR := by linarith
  have hd2 : 0 < Real.log Q + cE := by unfold cE; linarith
  rw [div_le_div_iff₀ hd1 hd2]
  unfold cE
  nlinarith [mul_nonneg (sub_nonneg.2 hc.le) hl0]

/-- Non-vacuity: the hypotheses of [H, Prop 12.2.4] can all be met. At `Q = 10¹⁰`, `Q₀ = 10⁵`,
`q = s = 1` (where `ρ = 1/2`), the book's statement gives
`G(10⁵)/G(10¹⁰) ≤ (log 10⁵ + 1.36)/(log 10¹⁰ + c_E)`, numerically `≈ 0.52735 ≤ 0.52848`. -/
theorem prop_12_2_4_base_point (h : prop_12_2_4) :
    Gq 1 (10 ^ 5) / Gq 1 (10 ^ 10) ≤
      (Real.log (10 ^ 5) + 1.36) / (Real.log (10 ^ 10) + cR) := by
  have hl : Real.log ((10 : ℝ) ^ 10) = 2 * Real.log ((10 : ℝ) ^ 5) := by
    rw [Real.log_pow, Real.log_pow]; push_cast; ring
  have hl0 : 0 < Real.log ((10 : ℝ) ^ 5) := Real.log_pos (by norm_num)
  have hρ : Real.log ((10 : ℝ) ^ 5) / Real.log ((10 : ℝ) ^ 10) ≤ 0.6 := by
    rw [hl]
    generalize Real.log ((10 : ℝ) ^ 5) = x at hl0 ⊢
    rw [div_le_iff₀ (by linarith)]
    linarith
  have := h (10 ^ 10) (10 ^ 5) (by norm_num) le_rfl hρ 1 le_rfl (by norm_num) 1 le_rfl
    (by norm_num)
  have e1 : (10 : ℝ) ^ 5 / (1 * ((1 : ℕ) : ℝ)) = 10 ^ 5 := by norm_num
  have e2 : (10 : ℝ) ^ 10 / (1 * ((1 : ℕ) : ℝ)) = 10 ^ 10 := by norm_num
  rwa [e1, e2] at this

end Companion.Book
