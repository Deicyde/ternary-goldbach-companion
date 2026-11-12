import TernaryGoldbach

/-!
# [H, Proposition 5.2.4]: the type II sum `S₂` (`v = 2`) by the large sieve

H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, Proposition 5.2.4
(`prop:kraken`), §5.2, p. 99, displays (5.53)–(5.57):
<https://arxiv.org/pdf/1501.05438v2#page=109>. (The 2013 preprint arXiv:1205.5252v4 has it as
Proposition 4.6, the same up to notation.)

## What [H] states

Let `x ≥ W ≥ 1`, `W' ≥ W/2`, `U' ≥ x/2W` and `Q ≥ 3.5W`. Let `2α = a/q + δ/x`, `(a, q) = 1`,
`|δ/x| ≤ 1/qQ` and `q ≤ Q`. Let `S₂(U', W', W)` be the sum (5.38) with `v = 2`:
`S₂ = ∑_{U' < m ≤ x/W, (m,2)=1} |∑_{W' < p ≤ W} (log p) e(αmp)|²`.
Write `Σ = ∑_{W' < p ≤ W} (log p)²`.
* (5.53) If `q ≤ ρQ` with `ρ ∈ [0, 1]`: `S₂ ≤ (max(1, 2ρ)(x/8q + x/2W) + W/2 + 2q) · Σ`.
* (5.54) If `q < W/2`: `S₂ ≤ ((x/(4φ(q))) · 1/log(W/2q) + (q/φ(q)) · W/log(W/2q)) · Σ`.
* (5.55) If `W > x/4q`: `S₂ ≤ (W/2 + q/(1 - x/4Wq)) · Σ`.
* (5.56) If `δ ≠ 0` and `x/4W + q ≤ x/|δ|q`:
  `S₂ ≤ min(1, (2q/φ(q)) / log((x/|δq|)(q + x/4W)⁻¹)) · (x/|δq| + W/2) · Σ`.
* (5.57) If `δ ≠ 0` and `q ≤ ρQ` with `ρ ∈ [0, 1)`:
  `S₂ ≤ (x/|δq| + W/2 + x/(8(1-ρ)Q) + x/(4(1-ρ)W)) · Σ`.

`prop_5_2_4` below is this statement: the hypotheses are `Prop524.Hyp`, and the five displays are
`Prop524.part53`, …, `Prop524.part57`.

## What the formalization proves

All five results are in `TernaryGoldbach/MinorArcs/TypeII.lean`, and all are for `v = 2`, as in [H].
`S2` is the book's `S₂`, and `logSqSum` is `Σ` (`Prop524.S2_eq_literal`). The approximation
`2α = a/q + δ/x` is taken modulo `1`, through an integer `k`. None of the theorems has a `Fact`
hypothesis. All but `prop_5_2_4_b` are in the dependency cone of the main theorem.
* `prop_5_2_4_a` is (5.53). It also assumes `ρ > 0` (implied by `1 ≤ q ≤ ρQ`) and `W' ≤ W`
  (otherwise both sides are `0`).
* `prop_5_2_4_e` is (5.54) with **the extra hypothesis `W ≥ 50000`** (and `W' ≤ W`). The docstring
  of `lemma_5_2_3_b` explains it. In the weighted large sieve, [H]'s proof of (5.51) takes the number
  of integers in `(W', W]` to be at most `W/2`. It can be larger: it is only `< W/2 + 1`. The repo
  absorbs the `+1` only for large `W`. Its `weight_caseA` uses `R ≤ (W/2)(1 - 0.99465)`, and for
  `q = 1` that needs `W ≥ 4.2·10⁴` or so.
* `prop_5_2_4_b` is (5.55), and `prop_5_2_4_d` is (5.57). Each assumes only consequences of the
  book's hypotheses.
* `prop_5_2_4_c` is (5.56) in another form. Part (i) is the bound with factor `1`, and it has
  `W - W'` where [H] has `W/2`. Part (ii) is the gain `(φ(q)/q) log R · S₂ ≤ (W - W' + x/|δ|q) Σ`,
  for `1 ≤ R ≤ W'` and `R² ≤ X := (x/|δq|)(q + x/4W)⁻¹`. The cap `R ≤ W'` is needed for Montgomery's
  inequality (`lemma_5_2_1`). [H] omits it and takes `R = √X`.

## Relation, as certified here: implied

The Lean results are weaker than [H]'s statement, and by exactly one thing: (5.54) for `W < 50000`.
* `prop_5_2_4_implies_formal : prop_5_2_4 → type_of% @prop_5_2_4_e`: the book's statement implies
  the formal (5.54). (If `x < W`, no `m` is in range and `S₂ = 0`.)
* `Prop524.part53_holds`, `Prop524.part55_holds`, `Prop524.part57_holds`: (5.53), (5.55) and (5.57)
  as printed, from `prop_5_2_4_a`, `_b` and `_d`.
* `Prop524.part56_holds`: (5.56) as printed. If `√X ≤ W'`, it follows from `prop_5_2_4_c` (i) and
  (ii) with `R = √X`. If `√X > W'`, (ii) does not apply, and the proof uses a trivial bound
  instead. That bound is `lemma_5_2_3_a` with `q = 1`, `Q = 2`:
  `S₂ ≤ ⌈(x/W - U')/2⌉ (W - W' + 2) Σ ≤ (x/4W + 1)(√X + 2) Σ`. It is enough, because
  `log y · (y + 2) ≤ y²` for `y ≥ 1` (`Prop524.log_mul_add_two_le_sq`). So the missing cap in [H]
  is harmless here.
* `Prop524.part54_holds_of_le`: (5.54) as printed, for `W ≥ 50000`.
* `prop_5_2_4_holds_of_large_W`: the whole proposition for `W ≥ 50000`.
  `prop_5_2_4_iff_small_W`: the whole proposition is *equivalent* to (5.54) for `W < 50000`.

Checks on the transcription:
* `Prop524.S2_eq_literal`, `Prop524.mem_Ioc_intFloor` and `Prop524.mem_Ioc_natFloor`. The repo's
  `S2` is the literal sum over `m ∈ ℤ` with `U' < m ≤ x/W` and `gcd(m, 2) = 1`, of the squared norm
  of the sum over primes `p` with `W' < p ≤ W`.
* `prop_5_2_4_nonvacuous`: the hypotheses hold at `x = W = 3`, `W' = 3/2`, `U' = 1/2`,
  `Q = 21/2`, `α = δ = a = 0`, `q = 1`. There `S₂ = (log 2 + log 3)² > 0` (`Prop524.S2_example`).

## Remark on the gap (not machine-checked)

We do not know whether (5.54) can fail for some `W < 50000`, and we did not find a counterexample.
Below `43` it holds by an elementary argument. By the triangle inequality and Cauchy–Schwarz,
`S₂ ≤ N_odd · P · Σ`, where `N_odd ≤ x/4W + 1` counts the odd `m` in range and `P` counts the
primes in `(W', W]`. With `t = W/2q > 1` and `φ(q) ≤ q`, the right side of (5.54) is at least
`(x/4W + 1) · (2t/log t) · Σ ≥ (x/4W + 1) · 2e · Σ`. So (5.54) holds whenever `P ≤ 5`. Every real
`W < 43` has at most `5` primes in `(W/2, W]`, and `43` has six (`23, …, 43`).
-/

open Finset
open TernaryGoldbach.MinorArcs (S2 oddSqSum primeExpSum logSqSum logSqSum_nonneg)

namespace Companion.Book

namespace Prop524

/-- `min(1, c/ℓ)`, with the convention `c/0 = +∞` that the book's (5.56) needs.

In (5.56), `ℓ = log X` with `X ≥ 1` (by the hypothesis `x/4W + q ≤ x/|δ|q`), so `ℓ ≥ 0`. At
`X = 1`, the book's `min(1, (2q/φ(q))/log X)` has the denominator `log 1 = 0` and means `1`. Lean's
`c / 0 = 0` would make it `0`, and the right side of (5.56) would collapse to `0`. So this
definition returns `1` at `ℓ = 0` and is `min 1 (c / ℓ)` otherwise. -/
noncomputable def minOneDiv (c ℓ : ℝ) : ℝ := if ℓ = 0 then 1 else min 1 (c / ℓ)

/-- The hypotheses of [H, Prop 5.2.4] (p. 99), as printed: `x ≥ W ≥ 1`, `W' ≥ W/2`,
`U' ≥ x/2W`, `Q ≥ 3.5W`, `2α = a/q + δ/x`, `(a, q) = 1`, `|δ/x| ≤ 1/qQ`, `q ≤ Q`.

Transcription choices:
* `x, W, W', U', Q, α, δ` are real, `a` is an integer, and `q` is a positive integer (`0 < q`). The
  positivity of the denominator `q` is implicit in [H].
* `(a, q) = 1` is `Int.gcd a q = 1`.
* `2α = a/q + δ/x` is an equation of real numbers. [H] takes `α ∈ ℝ/ℤ` (as in Ch. 6: "an angle
  `α ∈ ℝ/ℤ`"), so its equation holds modulo `1`. `S₂` depends only on `α mod 1`, and nothing is
  lost: if `2α = a/q + δ/x + k` with `k ∈ ℤ`, then `2α = (a + kq)/q + δ/x` and `(a + kq, q) = 1`
  (see `prop_5_2_4_implies_formal`). The conclusions do not involve `a`.
* `1/qQ` is `1/(qQ)`, and `x/2W` is `x/(2W)`. -/
def Hyp (x W W' U' Q α δ : ℝ) (a : ℤ) (q : ℕ) : Prop :=
  W ≤ x ∧ 1 ≤ W ∧ W / 2 ≤ W' ∧ x / (2 * W) ≤ U' ∧ 3.5 * W ≤ Q ∧
    0 < q ∧ 2 * α = a / q + δ / x ∧ Int.gcd a q = 1 ∧ |δ / x| ≤ 1 / (q * Q) ∧ (q : ℝ) ≤ Q

/-- [H, (5.53)]: for `q ≤ ρQ`, `ρ ∈ [0, 1]`,
`S₂(U', W', W) ≤ (max(1, 2ρ)(x/8q + x/2W) + W/2 + 2q) · ∑_{W'<p≤W} (log p)²`. -/
def part53 (x W W' U' Q α : ℝ) (q : ℕ) : Prop :=
  ∀ ρ : ℝ, 0 ≤ ρ → ρ ≤ 1 → (q : ℝ) ≤ ρ * Q →
    S2 α x U' W' W ≤
      (max 1 (2 * ρ) * (x / (8 * q) + x / (2 * W)) + W / 2 + 2 * q) * logSqSum W' W

/-- [H, (5.54)]: if `q < W/2`,
`S₂(U', W', W) ≤ ((x/(4φ(q))) · 1/log(W/2q) + (q/φ(q)) · W/log(W/2q)) · ∑_{W'<p≤W} (log p)²`.
`φ` is Euler's `Nat.totient`. As `q < W/2`, `log(W/2q) > 0`, so no division by zero occurs. -/
def part54 (x W W' U' α : ℝ) (q : ℕ) : Prop :=
  (q : ℝ) < W / 2 →
    S2 α x U' W' W ≤
      (x / (4 * q.totient) * (1 / Real.log (W / (2 * q))) +
        q / q.totient * (W / Real.log (W / (2 * q)))) * logSqSum W' W

/-- [H, (5.55)]: if `W > x/4q`, `S₂(U', W', W) ≤ (W/2 + q/(1 - x/4Wq)) · ∑_{W'<p≤W} (log p)²`.
(`W > x/4q` gives `x/4Wq < 1`, so the denominator is positive.) -/
def part55 (x W W' U' α : ℝ) (q : ℕ) : Prop :=
  x / (4 * q) < W →
    S2 α x U' W' W ≤ (W / 2 + q / (1 - x / (4 * W * q))) * logSqSum W' W

/-- [H, (5.56)]: if `δ ≠ 0` and `x/4W + q ≤ x/|δ|q`,
`S₂(U', W', W) ≤ min(1, (2q/φ(q))/log((x/|δq|)(q + x/4W)⁻¹)) · (x/|δq| + W/2) · ∑ (log p)²`.

The condition's `x/|δ|q` is `x/(|δ|q)`, the same number as `x/|δq|`. The book's proof of (5.56)
writes the condition as `x/4W + q ≤ x/|δq|`. The displays keep the printed `x/|δq|` (`x / |δ * q|`).
The `min` is `minOneDiv`, which reads `c/0` as `+∞`. -/
def part56 (x W W' U' α δ : ℝ) (q : ℕ) : Prop :=
  δ ≠ 0 → x / (4 * W) + q ≤ x / (|δ| * q) →
    S2 α x U' W' W ≤
      minOneDiv (2 * q / q.totient) (Real.log (x / |δ * q| * (q + x / (4 * W))⁻¹)) *
        (x / |δ * q| + W / 2) * logSqSum W' W

/-- [H, (5.57)]: if `δ ≠ 0` and `q ≤ ρQ`, `ρ ∈ [0, 1)`,
`S₂(U', W', W) ≤ (x/|δq| + W/2 + x/(8(1-ρ)Q) + x/(4(1-ρ)W)) · ∑_{W'<p≤W} (log p)²`. -/
def part57 (x W W' U' Q α δ : ℝ) (q : ℕ) : Prop :=
  δ ≠ 0 → ∀ ρ : ℝ, 0 ≤ ρ → ρ < 1 → (q : ℝ) ≤ ρ * Q →
    S2 α x U' W' W ≤
      (x / |δ * q| + W / 2 + x / (8 * (1 - ρ) * Q) + x / (4 * (1 - ρ) * W)) * logSqSum W' W

end Prop524

open Prop524 in
/-- **[H, Proposition 5.2.4]** (p. 99), as printed: under the hypotheses `Prop524.Hyp`, the five
bounds (5.53)–(5.57) on `S₂(U', W', W)` hold.

Transcription choices:
* `S₂(U', W', W)` is the repo's `TernaryGoldbach.MinorArcs.S2 α x U' W' W`. This is the book's
  (5.38) with `v = 2`: the sum over integers `U' < m ≤ x/W` with `(m, 2) = 1` of
  `|∑_{W' < p ≤ W} (log p) e(αmp)|²`, where `e(t) = exp(2πit)`. `Prop524.S2_eq_literal` and the
  two membership lemmas check this. `∑_{W'<p≤W} (log p)²` is the repo's `logSqSum W' W`.
* Each display is a conjunct, with its own extra hypotheses (`Prop524.part53` … `part57`). The
  parameter `ρ` of (5.53) and of (5.57) is universally quantified in each, with its printed range.
* `O*`-notation does not occur. All constants are the printed ones, and `3.5` is the real `7/2`.
* Inline fractions follow the book's convention `a/bc = a/(bc)`. For example `x/4Wq` is
  `x/(4Wq)`, `W/2q` is `W/(2q)` and `1/qQ` is `1/(qQ)`. -/
def prop_5_2_4 : Prop :=
  ∀ (x W W' U' Q α δ : ℝ) (a : ℤ) (q : ℕ), Hyp x W W' U' Q α δ a q →
    part53 x W W' U' Q α q ∧ part54 x W W' U' α q ∧ part55 x W W' U' α q ∧
      part56 x W W' U' α δ q ∧ part57 x W W' U' Q α δ q

namespace Prop524

/-! ### The book's objects versus the repo's -/

/-- `(m, 2) = 1` is `m` odd. -/
theorem gcd_two_eq_one_iff_odd (m : ℤ) : Int.gcd m 2 = 1 ↔ Odd m := by
  rw [show Int.gcd m 2 = Nat.gcd m.natAbs 2 from rfl, ← Nat.Coprime, Nat.coprime_two_right,
    Int.natAbs_odd]

/-- The range `Ioc ⌊A⌋ ⌊B⌋` of the outer sum of `S2` is `{m ∈ ℤ : A < m ≤ B}`, for all real
`A, B`. -/
theorem mem_Ioc_intFloor {A B : ℝ} {m : ℤ} : m ∈ Ioc ⌊A⌋ ⌊B⌋ ↔ A < m ∧ (m : ℝ) ≤ B := by
  rw [mem_Ioc, Int.floor_lt, Int.le_floor]

/-- The range `Ioc ⌊A⌋₊ ⌊B⌋₊` of the prime sums is `{p ∈ ℕ : A < p ≤ B}`, for real `A ≥ 0`. (In
[H, Prop 5.2.4], `A = W' ≥ 1/2`.) -/
theorem mem_Ioc_natFloor {A B : ℝ} (hA : 0 ≤ A) {p : ℕ} :
    p ∈ Ioc ⌊A⌋₊ ⌊B⌋₊ ↔ A < p ∧ (p : ℝ) ≤ B := by
  rw [mem_Ioc, Nat.floor_lt hA]
  constructor
  · rintro ⟨h1, h2⟩
    have hp : p ≠ 0 := by rintro rfl; simp at h1; linarith
    exact ⟨h1, (Nat.le_floor_iff' hp).1 h2⟩
  · rintro ⟨h1, h2⟩
    have hp : p ≠ 0 := by rintro rfl; simp at h1; linarith
    exact ⟨h1, (Nat.le_floor_iff' hp).2 h2⟩

/-- **The repo's `S2` is the book's `S₂` [H, (5.38)] with `v = 2`.** It is the sum over
`m ∈ (U', x/W] ∩ ℤ` with `(m, 2) = 1` of `|∑_{p ∈ (W', W], p prime} (log p) e(αmp)|²`. -/
theorem S2_eq_literal (α x U' W' W : ℝ) :
    S2 α x U' W' W = ∑ m ∈ (Ioc ⌊U'⌋ ⌊x / W⌋).filter (fun m : ℤ => Int.gcd m 2 = 1),
      ‖∑ p ∈ (Ioc ⌊W'⌋₊ ⌊W⌋₊).filter Nat.Prime,
        (Real.log p : ℂ) * TernaryGoldbach.e (α * m * p)‖ ^ 2 := by
  rw [S2, oddSqSum, sum_filter]
  refine sum_congr rfl fun m _ => ?_
  rw [if_congr (gcd_two_eq_one_iff_odd m) rfl rfl]
  rfl

/-- `∑_{W'<p≤W} (log p)²` is the repo's `logSqSum W' W` (by definition). -/
theorem logSqSum_eq_literal (W' W : ℝ) :
    logSqSum W' W = ∑ p ∈ (Ioc ⌊W'⌋₊ ⌊W⌋₊).filter Nat.Prime, Real.log p ^ 2 := rfl

/-- If `W ≤ W'` there are no primes in `(W', W]`, so `S₂ = 0`. -/
theorem S2_eq_zero_of_le {α x U' W' W : ℝ} (h : W ≤ W') : S2 α x U' W' W = 0 := by
  have hE : Ioc ⌊W'⌋₊ ⌊W⌋₊ = ∅ := Ioc_eq_empty (not_lt.2 (Nat.floor_mono h))
  simp [S2, oddSqSum, primeExpSum, hE]

/-- If `W ≤ W'`, then `∑_{W'<p≤W} (log p)² = 0`. -/
theorem logSqSum_eq_zero_of_le {W' W : ℝ} (h : W ≤ W') : logSqSum W' W = 0 := by
  have hE : Ioc ⌊W'⌋₊ ⌊W⌋₊ = ∅ := Ioc_eq_empty (not_lt.2 (Nat.floor_mono h))
  simp [logSqSum, hE]

/-- If no integer lies in `(U', x/W]`, then `S₂ = 0`. -/
theorem S2_eq_zero_of_floor_le {α x U' W' W : ℝ} (h : ⌊x / W⌋ ≤ ⌊U'⌋) : S2 α x U' W' W = 0 := by
  have hE : Ioc ⌊U'⌋ ⌊x / W⌋ = ∅ := Ioc_eq_empty (not_lt.2 h)
  simp [S2, oddSqSum, hE]

/-- What the formal theorems need, derived from the book's hypotheses. The approximation is
`2α = a/q + δ/x + k` with `k = 0`. -/
theorem Hyp.formal {x W W' U' Q α δ : ℝ} {a : ℤ} {q : ℕ} (h : Hyp x W W' U' Q α δ a q) :
    1 ≤ q ∧ IsCoprime a (q : ℤ) ∧ |2 * α - a / q - ((0 : ℤ) : ℝ)| ≤ 1 / (q * Q) ∧
      2 * α = a / q + δ / x + ((0 : ℤ) : ℝ) ∧ 0 < x ∧ 0 < W ∧ 0 < Q ∧ 0 ≤ W' := by
  obtain ⟨hWx, hW1, hW', -, hQ, hq, h2α, hgcd, hδ, -⟩ := h
  refine ⟨hq, Int.isCoprime_iff_gcd_eq_one.2 hgcd, ?_, ?_, by linarith, by linarith, by linarith,
    by linarith⟩
  · rw [Int.cast_zero, sub_zero, h2α, add_sub_cancel_left]
    exact hδ
  · rw [Int.cast_zero, add_zero]
    exact h2α

/-- `log y · (y + 2) ≤ y²` for `y ≥ 1`. It is used for (5.56) when `√X > W'`. -/
theorem log_mul_add_two_le_sq {y : ℝ} (hy : 1 ≤ y) : Real.log y * (y + 2) ≤ y ^ 2 := by
  have hy0 : 0 < y := by linarith
  have h1 : Real.log y ≤ y - 1 := Real.log_le_sub_one_of_pos hy0
  have h2 : Real.log y ≤ y / 2 := by
    have h := Real.log_le_sub_one_of_pos (show 0 < y / 2 by positivity)
    rw [Real.log_div hy0.ne' two_ne_zero] at h
    have := Real.log_two_lt_d9
    linarith
  have hy2' : 0 ≤ y + 2 := by linarith
  rcases le_total y 2 with hy2 | hy2
  · nlinarith [mul_le_mul_of_nonneg_right h1 hy2']
  · nlinarith [mul_le_mul_of_nonneg_right h2 hy2', mul_nonneg hy0.le (sub_nonneg.2 hy2)]

/-! ### The parts proved by the formalization -/

/-- **[H, (5.53)] as printed**, from `prop_5_2_4_a`. -/
theorem part53_holds
    {x W W' U' Q α δ : ℝ} {a : ℤ} {q : ℕ} (h : Hyp x W W' U' Q α δ a q) :
    part53 x W W' U' Q α q := by
  obtain ⟨hq, hcop, hα, -, hx, hW, hQ, -⟩ := h.formal
  obtain ⟨-, -, hW', hU', -⟩ := h
  intro ρ hρ0 hρ1 hqρ
  rcases le_or_gt W W' with hWW | hWW
  · rw [S2_eq_zero_of_le hWW, logSqSum_eq_zero_of_le hWW, mul_zero]
  · have hρ : 0 < ρ := by
      rcases eq_or_lt_of_le hρ0 with h0 | h0
      · rw [← h0, zero_mul] at hqρ
        have : (1 : ℝ) ≤ q := by exact_mod_cast hq
        linarith
      · exact h0
    exact TernaryGoldbach.MinorArcs.prop_5_2_4_a hq hcop hα hρ hρ1 hqρ hx hW hW' hWW.le hU'

/-- **[H, (5.55)] as printed**, from `prop_5_2_4_b`. -/
theorem part55_holds
    {x W W' U' Q α δ : ℝ} {a : ℤ} {q : ℕ} (h : Hyp x W W' U' Q α δ a q) :
    part55 x W W' U' α q := by
  obtain ⟨hq, hcop, hα, -, hx, hW, -, -⟩ := h.formal
  obtain ⟨-, -, hW', hU', -, -, -, -, -, hqQ⟩ := h
  intro hWq
  exact TernaryGoldbach.MinorArcs.prop_5_2_4_b hq hcop hα hqQ hx hW hWq hW' hU'

/-- **[H, (5.57)] as printed**, from `prop_5_2_4_d` (`|δq| = |δ| q`). -/
theorem part57_holds
    {x W W' U' Q α δ : ℝ} {a : ℤ} {q : ℕ} (h : Hyp x W W' U' Q α δ a q) :
    part57 x W W' U' Q α δ q := by
  obtain ⟨hq, hcop, -, h2α, hx, hW, -, -⟩ := h.formal
  obtain ⟨-, -, hW', hU', -, -, -, -, hδ, -⟩ := h
  intro hδ0 ρ _ hρ1 hqρ
  rw [abs_mul, Nat.abs_cast]
  exact TernaryGoldbach.MinorArcs.prop_5_2_4_d hq hcop h2α hδ hρ1 hqρ hx hW hδ0 hW' hU'

/-- **[H, (5.54)] as printed, for `W ≥ 50000`**, from `prop_5_2_4_e`. That theorem needs
`W ≥ 50000`, so this is the only range in which the formalization gives (5.54). -/
theorem part54_holds_of_le
    {x W W' U' Q α δ : ℝ} {a : ℤ} {q : ℕ} (h : Hyp x W W' U' Q α δ a q) (hW5 : 50000 ≤ W) :
    part54 x W W' U' α q := by
  obtain ⟨hq, hcop, hα, -, hx, -, -, -⟩ := h.formal
  obtain ⟨-, -, hW', hU', hQ, -⟩ := h
  intro hqW
  rcases le_or_gt W W' with hWW | hWW
  · rw [S2_eq_zero_of_le hWW, logSqSum_eq_zero_of_le hWW, mul_zero]
  · have e : x / (4 * (q.totient : ℝ)) * (1 / Real.log (W / (2 * q))) =
        x / (4 * q.totient * Real.log (W / (2 * q))) := by
      rw [div_mul_div_comm, mul_one]
    rw [e]
    exact TernaryGoldbach.MinorArcs.prop_5_2_4_e hq hcop hα hx (by linarith) hQ hW5 hW' hWW.le hU'

/-- **[H, (5.56)] as printed.** Write `Q' = x/|δq|`, `X = Q'(q + x/4W)⁻¹ ≥ 1`, `c = 2q/φ(q)` and
`B = (Q' + W/2) Σ`. The proof shows `S₂ ≤ B` and `log X · S₂ ≤ c B`; together these give
`S₂ ≤ min(1, c/log X) B`.
* `S₂ ≤ B` is `prop_5_2_4_c` (i), since `W - W' ≤ W/2`.
* If `√X ≤ W'`, then `prop_5_2_4_c` (ii) with `R = √X` gives `log X · S₂ ≤ c B`, since
  `log √X = (1/2) log X`.
* If `√X > W'`, then (ii) is not available (Montgomery's inequality needs `R ≤ W'`). Instead,
  `lemma_5_2_3_a` with `q = 1`, `Q = 2` (valid for every `α`) gives
  `S₂ ≤ ⌈(x/W - U')/2⌉ (W - W' + 2) Σ ≤ (x/4W + 1)(√X + 2) Σ`. Then
  `log X · (√X + 2) = 2 log √X · (√X + 2) ≤ 2X` (`log_mul_add_two_le_sq`), and
  `2X(x/4W + 1) ≤ c Q'`. -/
theorem part56_holds
    {x W W' U' Q α δ : ℝ} {a : ℤ} {q : ℕ} (h : Hyp x W W' U' Q α δ a q) :
    part56 x W W' U' α δ q := by
  obtain ⟨hq, hcop, -, h2α, hx, hW, -, hW'0⟩ := h.formal
  obtain ⟨-, -, hW', hU', -⟩ := h
  intro hδ0 hcond
  rw [abs_mul, Nat.abs_cast]
  have hq0 : (0 : ℝ) < q := by exact_mod_cast hq
  have hq1 : (1 : ℝ) ≤ q := by exact_mod_cast hq
  have hφ : (0 : ℝ) < q.totient := by exact_mod_cast Nat.totient_pos.2 hq
  have hφq : (q.totient : ℝ) ≤ q := by exact_mod_cast Nat.totient_le q
  have hδ : 0 < |δ| := abs_pos.2 hδ0
  obtain ⟨hi, hii⟩ :=
    TernaryGoldbach.MinorArcs.prop_5_2_4_c hq hcop h2α hx hW hδ0 hcond hU' hW'0
  set Q' := x / (|δ| * q) with hQ'
  set T := (q : ℝ) + x / (4 * W) with hT
  have hT0 : 0 < T := by positivity
  set X := Q' * T⁻¹ with hX
  set c := 2 * (q : ℝ) / q.totient with hc
  set L := logSqSum W' W with hLdef
  have hL : 0 ≤ L := logSqSum_nonneg W' W
  have hc2 : 2 ≤ c := by rw [hc, le_div_iff₀ hφ]; linarith
  have hc0 : 0 ≤ c := by linarith
  have hTQ' : T ≤ Q' := by rw [hT]; linarith
  have hX1 : 1 ≤ X := by rw [hX, ← div_eq_mul_inv, one_le_div hT0]; exact hTQ'
  have hX0 : 0 ≤ X := by linarith
  have hQ'X : Q' = X * T := by rw [hX, inv_mul_cancel_right₀ hT0.ne']
  have hlogX : 0 ≤ Real.log X := Real.log_nonneg hX1
  have hB : 0 ≤ (Q' + W / 2) * L := mul_nonneg (by positivity) hL
  -- `S₂ ≤ B`.
  have h1 : S2 α x U' W' W ≤ (Q' + W / 2) * L :=
    hi.trans (mul_le_mul_of_nonneg_right (by linarith) hL)
  -- `log X · S₂ ≤ c B`.
  have h2 : Real.log X * S2 α x U' W' W ≤ c * ((Q' + W / 2) * L) := by
    rcases le_or_gt (√X) W' with hR | hR
    · -- Montgomery's gain, `R = √X ≤ W'`.
      have hR2 : √X ^ 2 ≤ Q' / T := by rw [Real.sq_sqrt hX0, hX, div_eq_mul_inv]
      have h3 := hii (√X) (Real.one_le_sqrt.2 hX1) hR hR2
      rw [Real.log_sqrt hX0] at h3
      have h4 : (q.totient : ℝ) / q * (Real.log X / 2) * S2 α x U' W' W ≤ (Q' + W / 2) * L :=
        h3.trans (mul_le_mul_of_nonneg_right (by linarith) hL)
      have e : Real.log X * S2 α x U' W' W =
          c * ((q.totient : ℝ) / q * (Real.log X / 2) * S2 α x U' W' W) := by
        rw [hc]; field_simp
      rw [e]
      exact mul_le_mul_of_nonneg_left h4 hc0
    · -- The trivial bound, `√X > W'`.
      rcases le_or_gt W W' with hWW | hWW
      · rw [S2_eq_zero_of_le hWW, mul_zero]
        exact mul_nonneg hc0 hB
      · have hα1 : |2 * α - ((round (2 * α) : ℤ) : ℝ) / ((1 : ℕ) : ℝ) - ((0 : ℤ) : ℝ)| ≤
            1 / (((1 : ℕ) : ℝ) * 2) := by
          simpa using abs_sub_round (2 * α)
        have hS := TernaryGoldbach.MinorArcs.lemma_5_2_3_a (q := 1) (Q := 2) (a := round (2 * α))
          (k := 0) le_rfl isCoprime_one_right hα1 (by norm_num) hW'0 hWW.le U' (x / W)
        simp only [Nat.cast_one, mul_one, min_self] at hS
        have hceil : (⌈(x / W - U') / 2⌉₊ : ℝ) ≤ x / (4 * W) + 1 := by
          have hD : (x / W - U') / 2 ≤ x / (4 * W) := by
            have e1 : x / W - x / (2 * W) = 2 * (x / (4 * W)) := by field_simp; ring
            linarith
          rcases le_or_gt ((x / W - U') / 2) 0 with h0 | h0
          · rw [Nat.ceil_eq_zero.2 h0, Nat.cast_zero]; positivity
          · have := Nat.ceil_lt_add_one h0.le; linarith
        have hS' : S2 α x U' W' W ≤ (x / (4 * W) + 1) * ((√X + 2) * L) :=
          hS.trans (mul_le_mul hceil (mul_le_mul_of_nonneg_right (by linarith) hL)
            (mul_nonneg (by linarith) hL) (by positivity))
        have hkey := log_mul_add_two_le_sq (Real.one_le_sqrt.2 hX1)
        rw [Real.sq_sqrt hX0] at hkey
        have hlog2 : Real.log X = 2 * Real.log √X := by rw [Real.log_sqrt hX0]; ring
        have hXT : X * (x / (4 * W) + 1) ≤ Q' + W / 2 := by
          have : X * (x / (4 * W) + 1) ≤ X * T :=
            mul_le_mul_of_nonneg_left (by rw [hT]; linarith) hX0
          rw [hQ'X]; linarith
        have hXT0 : 0 ≤ X * (x / (4 * W) + 1) := by positivity
        calc Real.log X * S2 α x U' W' W
            ≤ Real.log X * ((x / (4 * W) + 1) * ((√X + 2) * L)) :=
              mul_le_mul_of_nonneg_left hS' hlogX
          _ = 2 * (Real.log √X * (√X + 2)) * (x / (4 * W) + 1) * L := by rw [hlog2]; ring
          _ ≤ 2 * X * (x / (4 * W) + 1) * L := by gcongr
          _ = 2 * (X * (x / (4 * W) + 1)) * L := by ring
          _ ≤ c * (Q' + W / 2) * L := by gcongr
          _ = c * ((Q' + W / 2) * L) := by ring
  -- The `min`.
  unfold minOneDiv
  split_ifs with hℓ
  · rw [one_mul]; exact h1
  · have hℓpos : 0 < Real.log X := lt_of_le_of_ne hlogX (Ne.symm hℓ)
    rw [mul_assoc, min_mul_of_nonneg _ _ hB, one_mul]
    refine le_min h1 ?_
    rw [div_mul_eq_mul_div, le_div_iff₀ hℓpos]
    linarith [h2]

/-! ### Sanity check: the hypotheses are satisfiable with `S₂ > 0` -/

/-- At `x = W = 3`, `W' = 3/2`, `U' = 1/2`, `α = 0`: only `m = 1` and `p ∈ {2, 3}` occur, so
`S₂ = (log 2 + log 3)²`. -/
theorem S2_example : S2 0 3 (1 / 2) (3 / 2) 3 = (Real.log 2 + Real.log 3) ^ 2 := by
  have h1 : ⌊(1 / 2 : ℝ)⌋ = 0 := by norm_num [Int.floor_eq_iff]
  have h2 : ⌊(3 : ℝ) / 3⌋ = 1 := by norm_num
  have h3 : ⌊(3 / 2 : ℝ)⌋₊ = 1 := by norm_num [Nat.floor_eq_iff]
  have h4 : ⌊(3 : ℝ)⌋₊ = 3 := by norm_num
  have h5 : (Ioc (1 : ℕ) 3).filter Nat.Prime = {2, 3} := by decide
  have h6 : Ioc (0 : ℤ) 1 = {1} := by decide
  have he : TernaryGoldbach.e 0 = 1 := by simp [TernaryGoldbach.e]
  simp only [S2, oddSqSum, primeExpSum, h1, h2, h3, h4, h5, h6, sum_singleton, zero_mul, he,
    mul_one, odd_one, ↓reduceIte]
  rw [sum_pair (by norm_num)]
  push_cast
  rw [← Complex.ofReal_add, Complex.norm_real, Real.norm_eq_abs, sq_abs]

end Prop524

open Prop524

/-- The book's hypotheses can all hold with `S₂ > 0`, so `prop_5_2_4` is not vacuous. The witness
is `x = W = 3`, `W' = 3/2`, `U' = 1/2`, `Q = 21/2 = 3.5W`, `α = δ = a = 0`, `q = 1`. -/
theorem prop_5_2_4_nonvacuous :
    ∃ (x W W' U' Q α δ : ℝ) (a : ℤ) (q : ℕ), Hyp x W W' U' Q α δ a q ∧ 0 < S2 α x U' W' W := by
  refine ⟨3, 3, 3 / 2, 1 / 2, 21 / 2, 0, 0, 0, 1, ?_, ?_⟩
  · refine ⟨le_rfl, by norm_num, by norm_num, by norm_num, by norm_num, one_pos, by norm_num,
      by norm_num, by norm_num, by norm_num⟩
  · rw [S2_example]; positivity

/-! ### Relation to the formalization -/

/-- **Book ⟹ formal.** [H, Prop 5.2.4] implies the formalization's (5.54), `prop_5_2_4_e`, which
has the extra hypothesis `W ≥ 50000`. The Lean approximation `|2α - a/q - k| ≤ 1/qQ` becomes the
book's with `a + kq` for `a` and `δ = x(2α - a/q - k)`. If `x < W`, no integer `m` satisfies
`x/2W ≤ U' < m ≤ x/W < 1`, so `S₂ = 0`, and the book's hypothesis `x ≥ W` is not needed. -/
theorem prop_5_2_4_implies_formal :
    prop_5_2_4 → type_of% @TernaryGoldbach.MinorArcs.prop_5_2_4_e := by
  intro h α x Q U' W' W a k q hq hcop hα hx hqW hQW hW hW'W hWW hU'
  have hq0 : (0 : ℝ) < q := by exact_mod_cast hq
  have hW0 : 0 < W := by linarith
  have hφ : (0 : ℝ) < q.totient := by exact_mod_cast Nat.totient_pos.2 hq
  have hlog : 0 < Real.log (W / (2 * q)) :=
    Real.log_pos (by rw [lt_div_iff₀ (by positivity)]; linarith)
  rcases lt_or_ge x W with hxW | hxW
  · have hfl : ⌊x / W⌋ ≤ ⌊U'⌋ := by
      have h1 : ⌊x / W⌋ < 1 := Int.floor_lt.2 (by
        rw [Int.cast_one, div_lt_one hW0]; exact hxW)
      have h2 : 0 ≤ ⌊U'⌋ := Int.floor_nonneg.2 (le_trans (by positivity) hU')
      omega
    rw [S2_eq_zero_of_floor_le hfl]
    exact mul_nonneg (by positivity) (logSqSum_nonneg W' W)
  · have hyp : Hyp x W W' U' Q α (x * (2 * α - a / q - k)) (a + k * q) q := by
      refine ⟨hxW, by linarith, hW'W, hU', hQW, hq, ?_, ?_, ?_, by linarith⟩
      · push_cast
        field_simp
        ring
      · exact Int.isCoprime_iff_gcd_eq_one.1 (hcop.add_mul_right_left k)
      · rw [mul_div_cancel_left₀ _ hx.ne']; exact hα
    have h54 := (h x W W' U' Q α _ _ q hyp).2.1 (by linarith)
    have e : x / (4 * (q.totient : ℝ)) * (1 / Real.log (W / (2 * q))) =
        x / (4 * q.totient * Real.log (W / (2 * q))) := by
      rw [div_mul_div_comm, mul_one]
    rw [e] at h54
    exact h54

/-- The formalization proves [H, Prop 5.2.4] in full for `W ≥ 50000`. -/
theorem prop_5_2_4_holds_of_large_W
    (x W W' U' Q α δ : ℝ) (a : ℤ) (q : ℕ) (hyp : Hyp x W W' U' Q α δ a q) (hW : 50000 ≤ W) :
    part53 x W W' U' Q α q ∧ part54 x W W' U' α q ∧ part55 x W W' U' α q ∧
      part56 x W W' U' α δ q ∧ part57 x W W' U' Q α δ q :=
  ⟨part53_holds hyp, part54_holds_of_le hyp hW, part55_holds hyp, part56_holds hyp,
    part57_holds hyp⟩

/-- **The gap, exactly.** [H, Prop 5.2.4] is equivalent to its
display (5.54) restricted to `W < 50000`. The other four displays, and (5.54) for `W ≥ 50000`, are
proved here. -/
theorem prop_5_2_4_iff_small_W :
    prop_5_2_4 ↔ ∀ (x W W' U' Q α δ : ℝ) (a : ℤ) (q : ℕ), Hyp x W W' U' Q α δ a q →
      W < 50000 → part54 x W W' U' α q := by
  constructor
  · intro h x W W' U' Q α δ a q hyp _
    exact (h x W W' U' Q α δ a q hyp).2.1
  · intro h x W W' U' Q α δ a q hyp
    refine ⟨part53_holds hyp, ?_, part55_holds hyp, part56_holds hyp, part57_holds hyp⟩
    rcases lt_or_ge W 50000 with hW | hW
    · exact h x W W' U' Q α δ a q hyp hW
    · exact part54_holds_of_le hyp hW

end Companion.Book
