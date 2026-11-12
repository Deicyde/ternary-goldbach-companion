import TernaryGoldbach

/-!
# [H, (5.36)] at `v = 2`: `∫₁ᵀ H₂(S) dS/S ≤ 0.15107 log T` is false

**What [H] states.** [H, p. 92, (5.36)] (https://arxiv.org/pdf/1501.05438v2#page=102; identical to
(4.36) of the 2013 preprint arXiv:1205.5252v4): "Hence (by (5.32))
`∫₁ᵀ H_v(S) dS/S ≤ 0.22482 log T` if `v = 1`, `≤ 0.15107 log T` if `v = 2`". Here, by [H, (5.35)],
`H₂(S) = (4/π²) G₂(S)` for `1 ≤ S < 16` and `H₂(S) = 0.15107` for `S ≥ 16`. `G₂(S)` is the triple sum
[H, (5.28)] `∑_{s ≤ S, (s,2)=1} (1/s) ∫_{1/2}^1 g₂(uS/s) du`, with `g₂` from [H, Lemma 5.1.2],
evaluated exactly by summing the exact expression [H, (5.29)] over `m`. This gives
`G₂(S) = K_{2,1}(⌊S⌋) + K_{2,2}(⌊S⌋)/S`. Only the case `v = 2` is transcribed. [H, Ch. 6] and the
formalization work with `v = 2` only.

**What the formalization proves.** `TernaryGoldbach.MinorArcs.integral_H2_le`: for `T ≥ 1`,
`∫₁ᵀ H2(S)/S dS ≤ 0.15107 log T + 0.0231`. The repo's `H2` is the book's `H₂` (`Eq_5_36.H₂_eq`).

**Relation, certified here: the printed statement is false.**
* `eq_5_36_false : ¬ eq_5_36`. At `T = 4`, `∫₁⁴ H₂(S) dS/S = (4/π²)((7/6) log 2 + (1/6) log 3 − 11/24)
  = 0.216195…` (`Eq_5_36.integral_H₂_four`), while `0.15107 log 4 = 0.209427…`
  (`Eq_5_36.bound_lt_integral_four`).
* `eq_5_36_fails_of_ge16`: the bound also fails at every `T ≥ 16`, by more than `0.02305`. So the
  failure is not limited to small `T`; [H, (6.25)] applies (5.36) with `T = x/(U W₀)` huge. With the
  repo's theorem this gives `∫₁ᵀ H₂/S − 0.15107 log T ∈ (0.02305, 0.0231]` for `T ≥ 16`, so the repo's
  additive correction `0.0231` is sharp to within `5·10⁻⁵`.
* `eq_5_36_false_of_le`: the refutation does not depend on reading `G₂` as the exact triple sum.
  [H] calls `G₂` "a bound" for the triple sum, and the statement is false for every such upper bound.
* `Eq_5_36.holds_at_two`: the inequality is true at `T = 2`, so `eq_5_36` is not false for a trivial
  reason. Numerically (outside Lean) it holds exactly for `1 ≤ T ≤ T* = 3.3673…` and fails for every
  `T > T*`.
* `eq_5_36_corrected_iff_formal`: the corrected statement (`+ 0.0231`), written in the book's notation,
  is equivalent to the formal theorem. So it holds (`eq_5_36_corrected_holds`).

The error comes from [H, (5.32)] at `v = 2`, `∫₁ᵀ G₂(S) dS/S ≤ 0.37273 log T`. (5.36) follows from it
after multiplying by `4/π²` (`4/π² · 0.37273 = 0.151062… ≤ 0.15107`). But (5.32) is false at `T = 4`:
`∫₁⁴ G₂(S) dS/S = (7/6) log 2 + (1/6) log 3 − 11/24 = 0.533440… > 0.37273 log 4 = 0.516713…`.

The values of `G₂` on `[n, n+1)`, `n ≤ 15`, used here come from the repo's kernel-checked tables
(`H2B.T2_eq'`). They were also recomputed independently, outside Lean, from the definitions of `g₂`
and (5.28) with exact rational arithmetic, and agree.
-/

open Real MeasureTheory

namespace Companion.Book

namespace Eq_5_36

open TernaryGoldbach.MinorArcs

/-- The book's `G₂(S)` [H, p. 92]: the triple sum [H, (5.28)] at `v = 2`,
`∑_{s ≤ S, (s,2)=1} (1/s) ∫_{1/2}^1 g₂(uS/s) du`. The book evaluates it exactly by summing the exact
contributions (5.29) of the `g₂(m)`, so that `G₂(S) = K_{2,1}(⌊S⌋) + K_{2,2}(⌊S⌋)/S`.

This is the repo's `TernaryGoldbach.MinorArcs.T2`. We checked that it agrees with the book:
* `T2 S = ∑ s ∈ Icc 1 ⌊S⌋₊, if Odd s then (1/s) ∫ u in 1/2..1, g2 (u S / s) else 0`. Here `s` runs
  over the positive integers `s ≤ S`, and `(s, 2) = 1 ↔ s` odd.
* The repo's `g2 x` sums `μ(r₁)μ(r₂)/(σ(r₁)σ(r₂))` over `r₁, r₂ ∈ [1, ⌊x⌋₊]` with `r₁, r₂` coprime and
  `r₁ r₂` odd. This is [H, Lemma 5.1.2]'s `g_v(x)` at `v = 2`, with `σ = σ₁` the sum of divisors.

Sanity checks against the book's own examples: `G₂(S) = 0` for `S < 1` (`G₂_eq_zero_of_lt_one`) and
`G₂(S) = 1 − 1/S` for `1 ≤ S < 2` (`G₂_eq_of_lt_two`). On `[n, n+1)`, `1 ≤ n ≤ 15`,
`G₂(S) = α_n + β_n/S` with the rationals of `H2B.T2_eq'`. -/
noncomputable def G₂ (S : ℝ) : ℝ := TernaryGoldbach.MinorArcs.T2 S

/-- The book's `H₂(S)` [H, (5.35)]: `(4/π²) G₂(S)` if `1 ≤ S < 16`, `0.15107` if `S ≥ 16`. The factor
`4/π²` is `6v/(π² σ(v))` at `v = 2`.

[H] prints the left side as `H₂(s)`, a typo for `H₂(S)`. It does not define `H₂` for `S < 1`. We use
`(4/π²) G₂(S)` there too, which is `0` by the book's remark `G₂(S) = 0` for `S < 1`. Only `[1, T]`
matters in (5.36). The repo's `H2` uses `max (T2 S) 0` instead of `G₂ S`. They agree because
`G₂ ≥ 0` (`H₂_eq`). -/
noncomputable def H₂ (S : ℝ) : ℝ := if S < 16 then 4 / π ^ 2 * G₂ S else 0.15107

theorem G₂_eq_zero_of_lt_one {S : ℝ} (hS : S < 1) : G₂ S = 0 := by
  unfold G₂ T2
  rw [Nat.floor_eq_zero.2 hS]
  simp

/-- The book's example: `G₂(S) = 1 − 1/S` for `1 ≤ S < 2`. -/
theorem G₂_eq_of_lt_two {S : ℝ} (h1 : 1 ≤ S) (h2 : S < 2) : G₂ S = 1 - 1 / S := by
  have h := H2B.T2_eq' (n := 1) le_rfl (by norm_num) (by exact_mod_cast h1) (by push_cast; linarith)
  have hab : H2B.al 1 = 1 ∧ H2B.be 1 = -1 := by simp [H2B.al, H2B.be, H2B.abT]
  rw [G₂, h, hab.1, hab.2]
  push_cast
  ring

theorem G₂_nonneg {S : ℝ} (hS : S < 16) : 0 ≤ G₂ S := by
  rcases lt_or_ge S 1 with h | h
  · rw [G₂_eq_zero_of_lt_one h]
  · have hS0 : 0 ≤ S := by linarith
    have hn1 : 1 ≤ ⌊S⌋₊ := Nat.le_floor (by exact_mod_cast h)
    have hn15 : ⌊S⌋₊ ≤ 15 :=
      Nat.le_of_lt_succ ((Nat.floor_lt hS0).2 (by norm_num; linarith))
    have h1 : (⌊S⌋₊ : ℝ) ≤ S := Nat.floor_le hS0
    have h2 : S < ⌊S⌋₊ + 1 := Nat.lt_floor_add_one S
    rw [G₂, H2B.T2_eq' hn1 hn15 h1 h2]
    exact (H2B.piece_bounds hn1 hn15 h1 h2.le).1

/-- The book's `H₂` is the repo's `TernaryGoldbach.MinorArcs.H2`. -/
theorem H₂_eq : H₂ = TernaryGoldbach.MinorArcs.H2 := by
  funext S
  unfold H₂ H2
  split_ifs with h
  · rw [max_eq_left (show 0 ≤ T2 S from G₂_nonneg h)]; rfl
  · rfl

/-- `S ↦ H₂(S)/S` is integrable on `[1, T]`. So the Lean integral in `eq_5_36` is the true integral,
not a junk value. -/
theorem intervalIntegrable_H₂_div (T : ℝ) :
    IntervalIntegrable (fun S => H₂ S / S) volume 1 T := by
  rw [H₂_eq]; exact intervalIntegrable_H2_div' 1 T

theorem log_four : Real.log 4 = 2 * Real.log 2 := by
  rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]; push_cast; ring

/-- `∫₁⁴ H₂(S) dS/S = (4/π²)((7/6) log 2 + (1/6) log 3 − 11/24) = 0.216195…`. -/
theorem integral_H₂_four :
    ∫ S in (1 : ℝ)..4, H₂ S / S =
      4 / π ^ 2 * (7 / 6 * Real.log 2 + 1 / 6 * Real.log 3 - 11 / 24) := by
  have h := H2B.integral_int 4 (by norm_num) (by norm_num)
  rw [H₂_eq]
  rw [show ((4 : ℕ) : ℝ) = 4 by norm_num] at h
  rw [h]
  have hab : H2B.al 1 = 1 ∧ H2B.be 1 = -1 ∧ H2B.al 2 = 1 / 2 ∧ H2B.be 2 = 0 ∧
      H2B.al 3 = 1 / 3 ∧ H2B.be 3 = 1 / 2 := by
    simp [H2B.al, H2B.be, H2B.abT]
  obtain ⟨a1, b1, a2, b2, a3, b3⟩ := hab
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, H2B.P]
  norm_num [a1, b1, a2, b2, a3, b3]
  rw [Real.log_div (by norm_num) (by norm_num), Real.log_div (by norm_num) (by norm_num), log_four]
  ring

/-- The witness at `T = 4`: `0.15107 log 4 = 0.209427… < 0.216195… = ∫₁⁴ H₂(S) dS/S`. -/
theorem bound_lt_integral_four : 0.15107 * Real.log 4 < ∫ S in (1 : ℝ)..4, H₂ S / S := by
  rw [integral_H₂_four, log_four]
  have hl2 := Real.log_two_gt_d9
  have hl3 : (1.098612285 : ℝ) ≤ Real.log 3 := by
    have := H2B.log_lo (j := 3) (by norm_num) (by norm_num)
    norm_num [H2B.loQ, H2B.loN] at this
    norm_num
    linarith
  have hk : (0.405 : ℝ) ≤ 4 / π ^ 2 := by
    rw [le_div_iff₀ (by positivity)]
    nlinarith [Real.pi_lt_d4, Real.pi_pos]
  have hA : 0 < 7 / 6 * Real.log 2 + 1 / 6 * Real.log 3 - 11 / 24 := by linarith
  have := mul_le_mul_of_nonneg_right hk hA.le
  linarith

/-- Non-triviality check: the book's inequality holds at `T = 2`.
`∫₁² H₂(S) dS/S = (4/π²)(log 2 − 1/2) = 0.0783… ≤ 0.1047… = 0.15107 log 2`. -/
theorem holds_at_two : ∫ S in (1 : ℝ)..2, H₂ S / S ≤ 0.15107 * Real.log 2 := by
  have h := H2B.integral_int 2 (by norm_num) (by norm_num)
  rw [H₂_eq]
  rw [show ((2 : ℕ) : ℝ) = 2 by norm_num] at h
  rw [h]
  have hab : H2B.al 1 = 1 ∧ H2B.be 1 = -1 := by simp [H2B.al, H2B.be, H2B.abT]
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, H2B.P]
  norm_num [hab.1, hab.2]
  have hl2 := Real.log_two_gt_d9
  have hl2' := Real.log_two_lt_d9
  have hk : 4 / π ^ 2 ≤ (0.406 : ℝ) := by
    rw [div_le_iff₀ (by positivity)]
    nlinarith [Real.pi_gt_d2, Real.pi_pos]
  have := mul_le_mul_of_nonneg_right hk (show (0 : ℝ) ≤ Real.log 2 + -(1 / 2) by linarith)
  linarith

/-! ### The bound fails at every `T ≥ 16` -/

/-- A rational lower bound for `H2B.P j / (4/π²) = ∫ⱼʲ⁺¹ G₂(S) dS/S`. It replaces `log(j+1)` and
`log j` by the repo's kernel-checked `10⁻⁹`-accurate bounds `H2B.loQ (j+1)` and `H2B.hiQ j`. -/
def PlQ (j : ℕ) : ℚ :=
  H2B.al j * (H2B.loQ (j + 1) - H2B.hiQ j) + H2B.be j * (1 / j - 1 / (j + 1))

/-- `∑_{j=1}^{15} PlQ j ≤ ∫₁¹⁶ G₂(S) dS/S`. -/
def PL : ℚ := ∑ i ∈ Finset.range 15, PlQ (i + 1)

/-- The rational check `c0 · hiQ 16 + 0.02305 < kLo · PL`. Here `c0 = 0.15107`, `log 16 < hiQ 16`
(`H2B.log_hi`) and `kLo ≤ 4/π²` (`H2B.k_lo`). -/
theorem PL_ok : 0 ≤ PL ∧ H2B.c0 * H2B.hiQ 16 + 2305 / 100000 < H2B.kLo * PL := by
  decide +kernel

theorem P_ge {j : ℕ} (h1 : 1 ≤ j) (h2 : j ≤ 15) : 4 / π ^ 2 * (PlQ j : ℝ) ≤ H2B.P j := by
  have hk : 0 < 4 / π ^ 2 := by positivity
  have ha : (0 : ℝ) ≤ H2B.al j := by
    exact_mod_cast (H2B.ends_ok j (Finset.mem_Icc.2 ⟨h1, h2⟩)).1
  have hj : (0 : ℝ) < j := by exact_mod_cast h1
  have hL : (H2B.loQ (j + 1) : ℝ) - H2B.hiQ j ≤ Real.log (((j : ℝ) + 1) / j) := by
    rw [Real.log_div (by positivity) hj.ne']
    have := H2B.log_lo (j := j + 1) (by omega) (by omega)
    have := H2B.log_hi h1 (by omega)
    push_cast at *
    linarith
  unfold H2B.P PlQ
  apply mul_le_mul_of_nonneg_left _ hk.le
  push_cast
  have := mul_le_mul_of_nonneg_left hL ha
  linarith

theorem bound_add_lt_integral_sixteen :
    0.15107 * Real.log 16 + 0.02305 < ∫ S in (1 : ℝ)..16, H₂ S / S := by
  have h := H2B.integral_int 16 (by norm_num) le_rfl
  rw [H₂_eq]
  rw [show ((16 : ℕ) : ℝ) = 16 by norm_num] at h
  rw [h]
  obtain ⟨hPL, hchk⟩ := PL_ok
  have hsum : 4 / π ^ 2 * (PL : ℝ) ≤ ∑ i ∈ Finset.range (16 - 1), H2B.P (i + 1) := by
    unfold PL
    push_cast
    rw [Finset.mul_sum]
    exact Finset.sum_le_sum fun i hi => P_ge (by omega) (by have := Finset.mem_range.1 hi; omega)
  have hk := mul_le_mul_of_nonneg_right H2B.k_lo (by exact_mod_cast hPL : (0 : ℝ) ≤ PL)
  have hl := H2B.log_hi (j := 16) (by norm_num) le_rfl
  have hchk' : ((H2B.c0 * H2B.hiQ 16 + 2305 / 100000 : ℚ) : ℝ) < ((H2B.kLo * PL : ℚ) : ℝ) := by
    exact_mod_cast hchk
  push_cast at hchk' hl
  rw [H2B.c0_eq] at hchk'
  have : (0.15107 : ℝ) * Real.log 16 ≤ 0.15107 * (H2B.hiQ 16 : ℝ) := by nlinarith
  linarith

end Eq_5_36

open Eq_5_36

/-- **[H, (5.36)] at `v = 2`, as printed**: for `T ≥ 1`, `∫₁ᵀ H₂(S) dS/S ≤ 0.15107 log T`.

Transcription:
* `H₂` is the book's `H₂` of (5.35) (`Eq_5_36.H₂`). It is built from the book's `G₂`, the exact
  triple sum (5.28) at `v = 2` (`Eq_5_36.G₂`; see their docstrings).
* `dS/S` is rendered as the integrand `H₂ S / S` of the interval integral `∫ S in 1..T`. `H₂/S` is
  integrable on `[1, T]` (`Eq_5_36.intervalIntegrable_H₂_div`), so this is the true integral.
* `0.15107` is the real literal. `log` is `Real.log`.
* The range of `T` is not printed. The integral starts at `1`, and [H, §6] uses (5.36) with
  `T = x/(U W₀) ≥ 1`, so we take `T ≥ 1`. The refutation does not depend on this choice: the bound
  fails at `T = 4` and at every `T ≥ 16` (`eq_5_36_fails_of_ge16`).
* Only `v = 2` is stated. The `v = 1` case (`0.22482 log T`) is not used by the formalization or by
  [H, Ch. 6], and is not transcribed. -/
def eq_5_36 : Prop :=
  ∀ T : ℝ, 1 ≤ T → ∫ S in (1 : ℝ)..T, H₂ S / S ≤ 0.15107 * Real.log T

/-- **[H, (5.36)] at `v = 2` is false.** Witness `T = 4`:
`∫₁⁴ H₂(S) dS/S = 0.216195… > 0.209427… = 0.15107 log 4`. -/
theorem eq_5_36_false : ¬ eq_5_36 := fun h =>
  absurd (h 4 (by norm_num)) (not_le.2 bound_lt_integral_four)

/-- The book's bound fails at **every** `T ≥ 16`, by more than `0.02305`. Together with the repo's
`integral_H2_le`, `∫₁ᵀ H₂(S) dS/S − 0.15107 log T ∈ (0.02305, 0.0231]` for all `T ≥ 16`. -/
theorem eq_5_36_fails_of_ge16 {T : ℝ} (hT : 16 ≤ T) :
    0.15107 * Real.log T + 0.02305 < ∫ S in (1 : ℝ)..T, H₂ S / S := by
  have h16 := bound_add_lt_integral_sixteen
  have hT0 : (0 : ℝ) < T := by linarith
  rw [H₂_eq] at h16 ⊢
  rw [← intervalIntegral.integral_add_adjacent_intervals
    (TernaryGoldbach.MinorArcs.intervalIntegrable_H2_div' 1 16)
    (TernaryGoldbach.MinorArcs.intervalIntegrable_H2_div' 16 T),
    TernaryGoldbach.MinorArcs.H2B.integral_ge16 le_rfl hT, Real.log_div hT0.ne' (by norm_num)]
  linarith

/-- **Robustness to the reading of `G₂`.** [H] obtains `G₂` as "a bound" for the triple sum (5.28).
Replacing `G₂` in (5.35) by **any** function `G ≥ G₂` (on `[1, 4]`, with `G(S)/S` integrable there)
still makes (5.36) false, at `T = 4`. -/
theorem eq_5_36_false_of_le (G : ℝ → ℝ) (hG : ∀ S ∈ Set.Icc (1 : ℝ) 4, G₂ S ≤ G S)
    (hGi : IntervalIntegrable (fun S => G S / S) volume 1 4) :
    ¬ ∀ T : ℝ, 1 ≤ T →
      ∫ S in (1 : ℝ)..T, (if S < 16 then 4 / π ^ 2 * G S else 0.15107) / S ≤
        0.15107 * Real.log T := by
  intro h
  have h4 := h 4 (by norm_num)
  have hcongr : ∫ S in (1 : ℝ)..4, (if S < 16 then 4 / π ^ 2 * G S else 0.15107) / S =
      ∫ S in (1 : ℝ)..4, 4 / π ^ 2 * (G S / S) := by
    refine intervalIntegral.integral_congr fun S hS => ?_
    rw [Set.uIcc_of_le (by norm_num)] at hS
    rw [ite_eq_left (show S < 16 by linarith [hS.2])]
    ring
  have hmono : ∫ S in (1 : ℝ)..4, H₂ S / S ≤ ∫ S in (1 : ℝ)..4, 4 / π ^ 2 * (G S / S) := by
    refine intervalIntegral.integral_mono_on (by norm_num) (intervalIntegrable_H₂_div 4)
      (hGi.const_mul _) fun S hS => ?_
    have hS0 : 0 < S := by linarith [hS.1]
    unfold H₂
    rw [ite_eq_left (by linarith [hS.2]), mul_div_assoc]
    exact mul_le_mul_of_nonneg_left (div_le_div_of_nonneg_right (hG S hS) hS0.le) (by positivity)
  rw [hcongr] at h4
  linarith [bound_lt_integral_four]

/-- The corrected [H, (5.36)] at `v = 2`, in the book's notation: `∫₁ᵀ H₂(S) dS/S ≤
0.15107 log T + 0.0231` for `T ≥ 1`. This is the form the formalization proves and uses. -/
def eq_5_36_corrected : Prop :=
  ∀ T : ℝ, 1 ≤ T → ∫ S in (1 : ℝ)..T, H₂ S / S ≤ 0.15107 * Real.log T + 0.0231

/-- The corrected statement is exactly the formalization's `integral_H2_le`, because `H₂ = H2`. -/
theorem eq_5_36_corrected_iff_formal :
    eq_5_36_corrected ↔ type_of% @TernaryGoldbach.MinorArcs.integral_H2_le := by
  -- after `H₂ = H2` the two sides agree up to the binder `{T}` vs `(T)`, which `rw` closes by `rfl`
  unfold eq_5_36_corrected
  rw [H₂_eq]

theorem eq_5_36_corrected_holds : eq_5_36_corrected :=
  eq_5_36_corrected_iff_formal.2 @TernaryGoldbach.MinorArcs.integral_H2_le

end Companion.Book
