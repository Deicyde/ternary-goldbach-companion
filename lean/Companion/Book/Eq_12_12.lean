import TernaryGoldbach

/-!
# [H, (12.12)]: Ramaré's estimate for `G_d(R) = ∑_{r ≤ R, (r,d)=1} μ²(r)/φ(r)`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, §12.2
("Bounding the quotient in the large sieve for primes"), equation (12.12) (label `eq:malito`),
p. 232, <https://arxiv.org/pdf/1501.05438v2#page=242>. Quoting Ramaré [Ram95, Lemma 3.4]:

  `G_d(R) = (φ(d)/d) (log R + c_E + ∑_{p ∣ d} log p/p) + O*(7.284 R^{−1/3} f₁(d))`

for all `d ∈ ℤ⁺` and all `R ≥ 1`, where `G_d(R) = ∑_{r ≤ R, (r,d)=1} μ²(r)/φ(r)` ((12.2)),
`f₁(d) = ∏_{p ∣ d} (1 + p^{−2/3}) (1 + (p^{1/3} + p^{2/3})/(p(p−1)))^{−1}` (12.13), and
`c_E = γ + ∑_{p ≥ 2} log p/(p(p−1)) = 1.3325822…` (12.14). `O*(c)` means a quantity of absolute
value `≤ c`. The statement is identical to (5.12) of arXiv:1312.7748v2 (p. 36). [H] gives no
proof. The source, O. Ramaré, *On Šnirel'man's constant*, Ann. Scuola Norm. Sup. Pisa (4) 22
(1995), 645–706, Lemma 3.4 (p. 658), states the same formula for all real `X > 0` (checked
against the page images of [Ram95], pp. 658–659).

**What the formalization proves.** `TernaryGoldbach.Prelim.RamPf.ramare_bound`
(`TernaryGoldbach/Prelim/RamareLog.lean:347`): for `d ≥ 1` and `R > 0`,
`|GqP d R − (φ(d)/d)(log R + cR + SqP d)| ≤ 7.284 R^{−1/3} f1qP d`, where `cR` is `c_E`. That is
[Ram95]'s range, which contains [H]'s `R ≥ 1`. Inside the proof the error is in fact
`≤ 7.04 R^{−1/3} f₁(d)` (`Prelim.RamPf.abs_E_le`; restated here as `eq_12_12_seven_04`). The
headline theorem `TernaryGoldbach.Prelim.ramare_Gq` (`Prelim/Ramare.lean:27`) is a weaker
packaging: there is *some* `c ∈ [1.3325822, 1.3325823]` with the estimate for `R ≥ 1`. The proof is
not Ramaré's. It writes `G_d = h_d ∗ [n odd]/n`, uses an explicit `O*(0.64 x^{−1/3})` for the odd
harmonic sum and `∑_a |h_d(a)| a^{1/3} ≤ 11 f₁(d)`, which gives `0.64 · 11 = 7.04`.

**Relation: proved.** `eq_12_12` below transcribes the printed statement. It is proved outright:
`eq_12_12_holds`, obtained from `eq_12_12_of_formal : type_of% @Prelim.RamPf.ramare_bound →
eq_12_12`. In the other direction, `eq_12_12_implies_formal : eq_12_12 → type_of%
@Prelim.ramare_Gq` shows that the headline theorem follows from [H]'s statement. None of
`ramare_bound`, `ramare_Gq`, `cR_bounds`, `abs_E_le`, `GqP_decomp`, `tsum_hD` and `tsum_hD_log`
takes a `Fact` hypothesis, so these results take none either.

**[Ram95, (3.9)] is false; refuted here.** Ramaré's proof (p. 659) ends by applying his Lemma 3.2
together with the claim (3.9) `∏_{p ≥ 2} (1 + (p^{1/3} + p^{2/3})/(p(p−1))) ≤ 8`. His constant is
`7.284 = 0.9105 · 8`, where `0.9105` comes from his Lemma 3.3. The product exceeds `8`. This file
proves it by computations that the kernel itself evaluates (`decide +kernel`; no compiled code is
trusted):
* `eq_12_12_ram95_threshold`: the partial product over the primes `p ≤ P` is `> 8` **iff**
  `P ≥ 14629`. `eq_12_12_ram95_partial` gives `∏_{p ≤ 14629} > 8` (the certified rational lower
  bound is `≈ 8.0000062`). `eq_12_12_ram95_partial_prev` gives `∏_{p ≤ 14628} < 8`, where `14627`
  is the prime before `14629` (the certified rational upper bound is `≈ 7.999983`).
* `eq_12_12_ram95_3_9_false`: (3.9) as printed, with the infinite product as Mathlib's `tprod`
  over `Nat.Primes`, is false. The product converges (`eq_12_12_ram95_summable`), so `tprod` is
  the genuine value.

Numerically (double precision, not part of the proof), the partial products over `p ≤ 10⁴, 10⁵,
10⁶, 10⁷, 10⁸, 10⁹` are `7.98552, 8.04603, 8.06870, 8.07754, 8.08108, 8.08252`. With the tail
`∑_{p > N} ≈ ∫_N^∞ (t^{−4/3} + t^{−5/3}) dt/log t`, every cutoff `N ∈ [10⁸, 10⁹]` gives the full
product as `8.083559` (spread `< 10⁻⁷`). The value `8.0845` quoted in the repo's notes matches the
cruder tail `3N^{−1/3}/log N` at `N = 10⁷`, which overestimates the tail. With `8.08356` in place
of `8`, Ramaré's argument gives `0.9105 · 8.08356 ≈ 7.360` instead of `7.284`. So [Ram95]'s proof
does not give the printed constant, but the printed statement is true: the Lean proof gives `7.04`.

**Non-vacuity.** `eq_12_12_nontrivial`: with `0.2` in place of `7.284` the printed statement is
false, whatever the value of `c_E`. At `d = 1` and `R ∈ {1, e^{1/2}}` one has `G_1(R) = 1`, so
both errors cannot be `≤ 0.2`. So the conclusion is a genuine constraint. Moreover
`eq_12_12_holds` proves the statement itself, so it is not vacuously false either.
-/

open TernaryGoldbach
open TernaryGoldbach.Prelim (GqP SqP f1pP f1qP)
open TernaryGoldbach.Prelim.RamPf (cR)
open scoped ArithmeticFunction.Moebius

namespace Companion.Book

/-! ### The book's objects -/

/-- [H, (12.14)]: `c_E = γ + ∑_{p ≥ 2} log p/(p(p−1))`, transcribed literally. `γ` is Mathlib's
`Real.eulerMascheroniConstant`, and the sum runs over the type `Nat.Primes` of all primes. It equals
the repo's `Prelim.RamPf.cR` (`eq_12_12_cE_eq`). The series is summable (`eq_12_12_cE_summable`),
so the `tsum` is the genuine sum. `Prelim.RamPf.cR_bounds` gives `1.3325822 ≤ c_E ≤ 1.3325823`,
which matches the printed `1.3325822…` and [Ram95, (3.6)] `1.33258227533221…`. -/
noncomputable def eq_12_12_cE : ℝ :=
  Real.eulerMascheroniConstant + ∑' p : Nat.Primes, Real.log p / ((p : ℝ) * ((p : ℝ) - 1))

/-- [H, (12.13)]: `f₁(d) = ∏_{p ∣ d} (1 + p^{−2/3}) (1 + (p^{1/3} + p^{2/3})/(p(p−1)))^{−1}`,
transcribed literally, with the printed `(·)^{−1}`. The product runs over the prime divisors of
`d`, i.e. over `d.primeFactors` (for `d ≥ 1`, `p ∈ d.primeFactors ↔ p prime ∧ p ∣ d`).
The powers are real powers `Real.rpow` of `(p : ℝ) > 0`. It equals the repo's `Prelim.f1qP`
(`eq_12_12_f1_eq`), which writes the inverse as a division. -/
noncomputable def eq_12_12_f1 (d : ℕ) : ℝ :=
  ∏ p ∈ d.primeFactors, (1 + (p : ℝ) ^ (-(2 / 3 : ℝ))) *
    (1 + ((p : ℝ) ^ (1 / 3 : ℝ) + (p : ℝ) ^ (2 / 3 : ℝ)) / ((p : ℝ) * ((p : ℝ) - 1)))⁻¹

/-- **[H, (12.12)] as printed** (= [Ram95, Lemma 3.4] restricted to `R ≥ 1`): for every positive
integer `d` and every real `R ≥ 1`,
`G_d(R) = (φ(d)/d)(log R + c_E + ∑_{p ∣ d} log p/p) + O*(7.284 R^{−1/3} f₁(d))`.

Transcription choices:
* `d ∈ ℤ⁺` is `d : ℕ` with `1 ≤ d`; `R` is real with `1 ≤ R`, as printed.
* `O*(7.284 R^{−1/3} f₁(d))` is read as "`|G_d(R) − main term| ≤ 7.284 R^{−1/3} f₁(d)`". The
  bound is a product of nonnegative reals, and `R^{−1/3}` is `R ^ (-(1/3 : ℝ))` (real power, `R > 0`).
* `G_d(R)` is the repo's `Prelim.GqP d R`, which is [H, (12.2)] (`eq_12_12_GqP_eq`, by `rfl`): the
  sum over `r ∈ [1, ⌊R⌋₊]` with `Nat.Coprime r d` of `μ(r)²/φ(r)`. That is the sum over the positive
  integers `r ≤ R` with `(r, d) = 1`, with Mathlib's `μ` and `φ` (real division).
* `φ(d)/d` is the real quotient `(φ d : ℝ) / d`; `log` is `Real.log`.
* `∑_{p ∣ d} log p/p` is written inline as a sum over `d.primeFactors`. It is the repo's
  `Prelim.SqP d` by definition (`eq_12_12_SqP_eq`).
* `c_E` is `eq_12_12_cE` ((12.14), literal) and `f₁` is `eq_12_12_f1` ((12.13), literal). -/
def eq_12_12 : Prop :=
  ∀ d : ℕ, 1 ≤ d → ∀ R : ℝ, 1 ≤ R →
    |GqP d R - ((Nat.totient d : ℝ) / d) *
        (Real.log R + eq_12_12_cE + ∑ p ∈ d.primeFactors, Real.log p / p)|
      ≤ 7.284 * R ^ (-(1 / 3 : ℝ)) * eq_12_12_f1 d

/-- [H, (12.2)]: the repo's `Prelim.GqP` is `G_q(R) = ∑_{r ≤ R, (r,q)=1} μ²(r)/φ(r)`, by
definition: `r` runs over `[1, ⌊R⌋₊]`, i.e. over the positive integers `r ≤ R`. -/
theorem eq_12_12_GqP_eq (d : ℕ) (R : ℝ) :
    GqP d R = ∑ r ∈ (Finset.Icc 1 ⌊R⌋₊).filter (fun r => Nat.Coprime r d),
      ((μ r : ℝ)) ^ 2 / Nat.totient r :=
  rfl

/-- The repo's `Prelim.SqP d` is `∑_{p ∣ d} log p/p`, by definition. -/
theorem eq_12_12_SqP_eq (d : ℕ) : SqP d = ∑ p ∈ d.primeFactors, Real.log p / p := rfl

/-- The book's `f₁` ((12.13), with `(·)^{−1}`) is the repo's `Prelim.f1qP` (with `/`). -/
theorem eq_12_12_f1_eq (d : ℕ) : eq_12_12_f1 d = f1qP d := by
  unfold eq_12_12_f1 f1qP f1pP
  exact Finset.prod_congr rfl fun p _ => (div_eq_mul_inv _ _).symm

/-- The book's `c_E` ((12.14), a sum over `Nat.Primes`) is the repo's `Prelim.RamPf.cR`
(`γ` plus a sum over `ℕ` with the indicator of the primes). -/
theorem eq_12_12_cE_eq : eq_12_12_cE = cR := by
  unfold eq_12_12_cE cR Prelim.RamPf.sumP
  congr 1
  have hs : Function.support
      (fun q : ℕ => if q.Prime then Real.log q / ((q : ℝ) * ((q : ℝ) - 1)) else 0) ⊆
        {p : ℕ | p.Prime} := by
    intro q hq
    by_contra h
    exact hq (ite_eq_right h)
  rw [← tsum_subtype_eq_of_support_subset hs]
  refine tsum_congr fun p => ?_
  rw [ite_eq_left p.2]

/-! ### The relation with the formalization -/

/-- **The formalization's statement implies [H, (12.12)].** The hypothesis is the statement of
`Prelim.RamPf.ramare_bound` (taken via `type_of%`): the estimate with `c = cR` for all `R > 0`.
[H]'s range `R ≥ 1` is a special case. -/
theorem eq_12_12_of_formal
    (h : type_of% @TernaryGoldbach.Prelim.RamPf.ramare_bound) : eq_12_12 := by
  intro d hd R hR
  rw [eq_12_12_cE_eq, eq_12_12_f1_eq, ← eq_12_12_SqP_eq]
  exact h hd (by linarith)

/-- **[H, (12.12)] holds**: the formalization proves the book's statement itself
(`Prelim.RamPf.ramare_bound`). -/
theorem eq_12_12_holds : eq_12_12 :=
  eq_12_12_of_formal @TernaryGoldbach.Prelim.RamPf.ramare_bound

/-- **[H, (12.12)] implies the headline theorem `Prelim.ramare_Gq`**. That theorem only asserts
that *some* constant `c ∈ [1.3325822, 1.3325823]` works (for `R ≥ 1`). [H]'s statement gives it
with `c = c_E`, and `Prelim.RamPf.cR_bounds` puts `c_E` in that interval. So the headline theorem
is a weaker packaging of (12.12); the exact statement is `eq_12_12_holds`. -/
theorem eq_12_12_implies_formal : eq_12_12 → type_of% @TernaryGoldbach.Prelim.ramare_Gq := by
  intro h
  refine ⟨cR, Prelim.RamPf.cR_bounds.1, Prelim.RamPf.cR_bounds.2, fun d hd R hR => ?_⟩
  have := h d hd R hR
  rwa [eq_12_12_cE_eq, eq_12_12_f1_eq, ← eq_12_12_SqP_eq] at this

/-- What the formalization actually proves: the error in (12.12) is `≤ 7.04 R^{−1/3} f₁(d)` for
every real `R > 0` (`Prelim.RamPf.abs_E_le`, applied to the decomposition
`Prelim.RamPf.GqP_decomp`, exactly as in the proof of `ramare_bound`). This is stronger than [H]'s
`7.284` and `R ≥ 1`, and also gives [Ram95, Lemma 3.4] in its own range `X > 0`. -/
theorem eq_12_12_seven_04 {d : ℕ} (hd : 1 ≤ d) {R : ℝ}
    (hR : 0 < R) :
    |GqP d R - ((Nat.totient d : ℝ) / d) *
        (Real.log R + eq_12_12_cE + ∑ p ∈ d.primeFactors, Real.log p / p)|
      ≤ 7.04 * R ^ (-(1 / 3 : ℝ)) * eq_12_12_f1 d := by
  have hE := Prelim.RamPf.abs_E_le hd hR
  have hdec := Prelim.RamPf.GqP_decomp hd hR
  rw [Prelim.RamPf.tsum_hD hd, Prelim.RamPf.tsum_hD_log hd] at hdec
  rw [eq_12_12_cE_eq, eq_12_12_f1_eq, ← eq_12_12_SqP_eq]
  have e : GqP d R - ((Nat.totient d : ℝ) / d) * (Real.log R + cR + SqP d) =
      ∑' a, Prelim.RamPf.hD d a * Prelim.RamPf.Fo (R / a) := by
    rw [hdec, cR, Prelim.RamPf.Cg]; ring
  rw [e]
  exact hE

/-- `G_1(R) = 1` for `1 ≤ R < 2` (only the term `r = 1`). -/
theorem eq_12_12_G_one {R : ℝ} (h1 : 1 ≤ R) (h2 : R < 2) : GqP 1 R = 1 := by
  have hfl : ⌊R⌋₊ = 1 :=
    (Nat.floor_eq_iff (by linarith)).2 ⟨by simpa using h1, by norm_num; linarith⟩
  rw [eq_12_12_GqP_eq, hfl]
  simp

/-- **Non-vacuity**: with `0.2` in place of `7.284` the printed statement is false, whatever the
value of `c_E`. At `d = 1` (`φ(1)/1 = 1`, no prime divisors, `f₁(1) = 1`) and `R = 1`,
`R = e^{1/2}` (both `< 2`, so `G_1(R) = 1`), the two errors are `|1 − c_E|` and `|1/2 − c_E|`.
They differ by `1/2`, so they cannot both be `≤ 0.2` (note `e^{−1/6} ≤ 1`). So the conclusion of
`eq_12_12` is a genuine constraint. -/
theorem eq_12_12_nontrivial :
    ¬ ∀ d : ℕ, 1 ≤ d → ∀ R : ℝ, 1 ≤ R →
      |GqP d R - ((Nat.totient d : ℝ) / d) *
          (Real.log R + eq_12_12_cE + ∑ p ∈ d.primeFactors, Real.log p / p)|
        ≤ 0.2 * R ^ (-(1 / 3 : ℝ)) * eq_12_12_f1 d := by
  intro h
  have hR1 : (1 : ℝ) ≤ Real.exp (1 / 2) := Real.one_le_exp (by norm_num)
  have hR2 : Real.exp (1 / 2) < 2 := by
    calc Real.exp (1 / 2) < Real.exp (Real.log 2) :=
          Real.exp_lt_exp.2 (by linarith [Real.log_two_gt_d9])
      _ = 2 := Real.exp_log (by norm_num)
  have h1 := h 1 le_rfl 1 le_rfl
  have h2 := h 1 le_rfl (Real.exp (1 / 2)) hR1
  have hf : eq_12_12_f1 1 = 1 := by simp [eq_12_12_f1]
  rw [eq_12_12_G_one le_rfl (by norm_num), hf] at h1
  rw [eq_12_12_G_one hR1 hR2, hf] at h2
  simp only [Nat.totient_one, Nat.cast_one, div_one, one_mul, Real.log_one, Real.log_exp,
    Nat.primeFactors_one, Finset.sum_empty, add_zero, zero_add, mul_one, Real.one_rpow] at h1 h2
  have h3 : Real.exp (1 / 2) ^ (-(1 / 3 : ℝ)) ≤ 1 :=
    Real.rpow_le_one_of_one_le_of_nonpos hR1 (by norm_num)
  have h4 := abs_le.1 h1
  have h5 := abs_le.1 h2
  nlinarith

/-! ### [Ram95, (3.9)] is false

Ramaré's last step is (3.9): `∏_{p ≥ 2} (1 + (p^{1/3} + p^{2/3})/(p(p−1))) ≤ 8`. We show that the
partial products over `p ≤ P` exceed `8` exactly from `P = 14629` on.

Method (every computation is evaluated by the kernel itself, via `decide +kernel`):
* primes: `n ≤ 14629 < 121²` is prime iff it is one of the 30 primes `≤ 120`
  (`eq_12_12_smallPrimes`, checked by the kernel in `eq_12_12_smallPrimes_spec`), or `n > 120`
  and `gcd(n, 120!) = 1` (`eq_12_12_cert_iff`; a composite `n < 121²` has a prime factor `≤ 120`);
* factors: with `M = 2³⁰` and an integer `c` with `c³ ≤ n M³` (binary search; only this inequality
  is used), `n^{1/3} ≥ c/M` and `n^{2/3} ≥ (c/M)²`, so the factor at `n` is
  `≥ (n(n−1)M² + cM + c²)/(n(n−1)M²)`; with `u³ ≥ n M³` the same expression in `u` is an upper
  bound;
* the kernel multiplies these rationals (numerators of about `1.4·10⁵` bits) over all `1713`
  (resp. `1712`) primes and compares with `8`.
-/

/-- The factor of [Ram95, (3.9)]: `1 + (p^{1/3} + p^{2/3})/(p(p−1))`. -/
noncomputable def eq_12_12_ramFactor (p : ℕ) : ℝ :=
  1 + ((p : ℝ) ^ (1 / 3 : ℝ) + (p : ℝ) ^ (2 / 3 : ℝ)) / ((p : ℝ) * ((p : ℝ) - 1))

/-- **[Ram95, (3.9)] as printed**: `∏_{p ≥ 2} (1 + (p^{1/3} + p^{2/3})/(p(p−1))) ≤ 8`, the
product over all primes being Mathlib's `tprod` over `Nat.Primes`. The product converges
(`eq_12_12_ram95_summable` and `Real.rexp_tsum_eq_tprod`), so `tprod` is its genuine value. -/
def eq_12_12_ram95_3_9 : Prop :=
  ∏' p : Nat.Primes, eq_12_12_ramFactor p ≤ 8

/-- Binary search for `⌊m^{1/3}⌋` on `[lo, hi)` with `fuel` steps. We only use that the result
`c` satisfies `c³ ≤ m` when `lo³ ≤ m` (`eq_12_12_cbrtAux_cube_le`). Optimality only affects the
quality of the bounds, never their correctness. -/
def eq_12_12_cbrtAux (m : ℕ) : ℕ → ℕ → ℕ → ℕ
  | 0, lo, _ => lo
  | fuel + 1, lo, hi =>
    if lo + 1 < hi then
      if ((lo + hi) / 2) ^ 3 ≤ m then eq_12_12_cbrtAux m fuel ((lo + hi) / 2) hi
      else eq_12_12_cbrtAux m fuel lo ((lo + hi) / 2)
    else lo

/-- An integer `c` with `c³ ≤ n M³`, `M = 2³⁰` (`eq_12_12_cb_cube_le`). For `n < 2¹⁵` the search
returns `⌊n^{1/3} M⌋`, but only `c³ ≤ n M³` is used. -/
def eq_12_12_cb (n : ℕ) : ℕ := eq_12_12_cbrtAux (n * (2 ^ 30) ^ 3) 40 0 (2 ^ 35)

/-- An integer `u` with `n M³ ≤ u³` (`eq_12_12_cube_le_cbUp`): `c + 1` if that works, otherwise
the crude `n M`. Only the inequality `n M³ ≤ u³` is used. -/
def eq_12_12_cbUp (n : ℕ) : ℕ :=
  if n * (2 ^ 30) ^ 3 ≤ (eq_12_12_cb n + 1) ^ 3 then eq_12_12_cb n + 1 else n * 2 ^ 30

/-- Numerator of the lower bound `1 + (c/M + (c/M)²)/(n(n−1))` for the factor at `n`. -/
def eq_12_12_num (n : ℕ) : ℕ :=
  n * (n - 1) * (2 ^ 30) ^ 2 + eq_12_12_cb n * 2 ^ 30 + eq_12_12_cb n ^ 2

/-- Numerator of the upper bound `1 + (u/M + (u/M)²)/(n(n−1))` for the factor at `n`. -/
def eq_12_12_numUp (n : ℕ) : ℕ :=
  n * (n - 1) * (2 ^ 30) ^ 2 + eq_12_12_cbUp n * 2 ^ 30 + eq_12_12_cbUp n ^ 2

/-- The common denominator `n(n−1)M²`. -/
def eq_12_12_den (n : ℕ) : ℕ := n * (n - 1) * (2 ^ 30) ^ 2

/-- The primes `≤ 120`. -/
def eq_12_12_smallPrimes : List ℕ :=
  [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89,
    97, 101, 103, 107, 109, 113]

/-- The integers `n ≤ P` passing the primality certificate (a kernel-friendly filter). -/
def eq_12_12_certSet (P : ℕ) : Finset ℕ :=
  (Finset.Iic P).filter fun n =>
    (n ≤ 120 ∧ n ∈ eq_12_12_smallPrimes) ∨ (120 < n ∧ Nat.Coprime n (Nat.factorial 120))

theorem eq_12_12_cbrtAux_cube_le (m : ℕ) :
    ∀ fuel lo hi : ℕ, lo ^ 3 ≤ m → eq_12_12_cbrtAux m fuel lo hi ^ 3 ≤ m
  | 0, lo, hi, h => by simpa [eq_12_12_cbrtAux] using h
  | fuel + 1, lo, hi, h => by
    rw [eq_12_12_cbrtAux]
    split_ifs with h1 h2
    · exact eq_12_12_cbrtAux_cube_le m fuel _ hi h2
    · exact eq_12_12_cbrtAux_cube_le m fuel lo _ h
    · exact h

theorem eq_12_12_cb_cube_le (n : ℕ) : eq_12_12_cb n ^ 3 ≤ n * (2 ^ 30) ^ 3 :=
  eq_12_12_cbrtAux_cube_le _ 40 0 _ (by simp)

theorem eq_12_12_cube_le_cbUp (n : ℕ) : n * (2 ^ 30) ^ 3 ≤ eq_12_12_cbUp n ^ 3 := by
  unfold eq_12_12_cbUp
  split_ifs with h
  · exact h
  · rw [mul_pow]
    exact Nat.mul_le_mul_right _ (Nat.le_self_pow (by norm_num) n)

/-- If `0 ≤ x` and `x³ ≤ y` then `x ≤ y^{1/3}`. -/
theorem eq_12_12_le_rpow_third {x y : ℝ} (hx : 0 ≤ x) (h : x ^ 3 ≤ y) :
    x ≤ y ^ (1 / 3 : ℝ) := by
  have h3 : (x ^ 3) ^ (1 / 3 : ℝ) = x := by
    rw [show (1 / 3 : ℝ) = ((3 : ℕ) : ℝ)⁻¹ by norm_num]
    exact Real.pow_rpow_inv_natCast hx (by norm_num)
  calc x = (x ^ 3) ^ (1 / 3 : ℝ) := h3.symm
    _ ≤ y ^ (1 / 3 : ℝ) := Real.rpow_le_rpow (by positivity) h (by norm_num)

/-- If `0 ≤ y ≤ x³` then `y^{1/3} ≤ x`. -/
theorem eq_12_12_rpow_third_le {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (h : y ≤ x ^ 3) :
    y ^ (1 / 3 : ℝ) ≤ x := by
  have h3 : (x ^ 3) ^ (1 / 3 : ℝ) = x := by
    rw [show (1 / 3 : ℝ) = ((3 : ℕ) : ℝ)⁻¹ by norm_num]
    exact Real.pow_rpow_inv_natCast hx (by norm_num)
  calc y ^ (1 / 3 : ℝ) ≤ (x ^ 3) ^ (1 / 3 : ℝ) := Real.rpow_le_rpow hy h (by norm_num)
    _ = x := h3

theorem eq_12_12_rpow_two_thirds {y : ℝ} (hy : 0 ≤ y) :
    y ^ (2 / 3 : ℝ) = (y ^ (1 / 3 : ℝ)) ^ 2 := by
  rw [← Real.rpow_natCast, ← Real.rpow_mul hy]
  norm_num

/-- Every factor of (3.9) is `≥ 1`. -/
theorem eq_12_12_one_le_ramFactor (p : ℕ) : 1 ≤ eq_12_12_ramFactor p := by
  unfold eq_12_12_ramFactor
  have hpp : 0 ≤ (p : ℝ) * ((p : ℝ) - 1) := by
    rcases Nat.eq_zero_or_pos p with rfl | hp
    · simp
    · have : (1 : ℝ) ≤ p := by exact_mod_cast hp
      nlinarith
  have : 0 ≤ ((p : ℝ) ^ (1 / 3 : ℝ) + (p : ℝ) ^ (2 / 3 : ℝ)) / ((p : ℝ) * ((p : ℝ) - 1)) :=
    div_nonneg (by positivity) hpp
  linarith

theorem eq_12_12_den_pos {n : ℕ} (hn : 2 ≤ n) : (0 : ℝ) < eq_12_12_den n := by
  have : 0 < eq_12_12_den n := by
    unfold eq_12_12_den
    have : 0 < n - 1 := by omega
    positivity
  exact_mod_cast this

/-- `(n(n−1)M² + vM + v²)/(n(n−1)M²) = 1 + (v/M + (v/M)²)/(n(n−1))` for `n ≥ 2`. -/
theorem eq_12_12_ratio_eq {n : ℕ} (hn : 2 ≤ n) (v : ℕ) :
    ((n * (n - 1) * (2 ^ 30) ^ 2 + v * 2 ^ 30 + v ^ 2 : ℕ) : ℝ) / eq_12_12_den n =
      1 + ((v : ℝ) / 2 ^ 30 + ((v : ℝ) / 2 ^ 30) ^ 2) / ((n : ℝ) * ((n : ℝ) - 1)) := by
  have hn' : (2 : ℝ) ≤ n := by exact_mod_cast hn
  have hn0 : (n : ℝ) ≠ 0 := (by linarith : (0 : ℝ) < n).ne'
  have hn1 : (n : ℝ) - 1 ≠ 0 := (by linarith : (0 : ℝ) < (n : ℝ) - 1).ne'
  have hcast : ((n - 1 : ℕ) : ℝ) = (n : ℝ) - 1 := by
    rw [Nat.cast_sub (by omega), Nat.cast_one]
  simp only [eq_12_12_den, Nat.cast_add, Nat.cast_mul, Nat.cast_pow, hcast, Nat.cast_ofNat]
  field_simp
  ring

/-- Lower bound for the factor at `n ≥ 2`, from `c³ ≤ n M³`. -/
theorem eq_12_12_num_div_den_le {n : ℕ} (hn : 2 ≤ n) :
    (eq_12_12_num n : ℝ) / eq_12_12_den n ≤ eq_12_12_ramFactor n := by
  have hc := eq_12_12_cb_cube_le n
  have hn' : (2 : ℝ) ≤ n := by exact_mod_cast hn
  have hpp : 0 < (n : ℝ) * ((n : ℝ) - 1) := by nlinarith
  have hx0 : 0 ≤ (eq_12_12_cb n : ℝ) / 2 ^ 30 := by positivity
  have hx3 : ((eq_12_12_cb n : ℝ) / 2 ^ 30) ^ 3 ≤ n := by
    rw [div_pow, div_le_iff₀ (by positivity)]
    exact_mod_cast hc
  have h1 := eq_12_12_le_rpow_third hx0 hx3
  have h2 : ((eq_12_12_cb n : ℝ) / 2 ^ 30) ^ 2 ≤ (n : ℝ) ^ (2 / 3 : ℝ) := by
    rw [eq_12_12_rpow_two_thirds (by positivity)]
    exact pow_le_pow_left₀ hx0 h1 2
  rw [eq_12_12_num, eq_12_12_ratio_eq hn, eq_12_12_ramFactor]
  have := div_le_div_of_nonneg_right (add_le_add h1 h2) hpp.le
  linarith

/-- Upper bound for the factor at `n ≥ 2`, from `n M³ ≤ u³`. -/
theorem eq_12_12_ramFactor_le_numUp {n : ℕ} (hn : 2 ≤ n) :
    eq_12_12_ramFactor n ≤ (eq_12_12_numUp n : ℝ) / eq_12_12_den n := by
  have hu := eq_12_12_cube_le_cbUp n
  have hn' : (2 : ℝ) ≤ n := by exact_mod_cast hn
  have hpp : 0 < (n : ℝ) * ((n : ℝ) - 1) := by nlinarith
  have hx0 : 0 ≤ (eq_12_12_cbUp n : ℝ) / 2 ^ 30 := by positivity
  have hx3 : (n : ℝ) ≤ ((eq_12_12_cbUp n : ℝ) / 2 ^ 30) ^ 3 := by
    rw [div_pow, le_div_iff₀ (by positivity)]
    exact_mod_cast hu
  have h1 := eq_12_12_rpow_third_le hx0 (by positivity) hx3
  have h2 : (n : ℝ) ^ (2 / 3 : ℝ) ≤ ((eq_12_12_cbUp n : ℝ) / 2 ^ 30) ^ 2 := by
    rw [eq_12_12_rpow_two_thirds (by positivity)]
    exact pow_le_pow_left₀ (by positivity) h1 2
  rw [eq_12_12_numUp, eq_12_12_ratio_eq hn, eq_12_12_ramFactor]
  have := div_le_div_of_nonneg_right (add_le_add h1 h2) hpp.le
  linarith

/-- The primes `≤ 120` are exactly the entries of `eq_12_12_smallPrimes` (kernel check). -/
theorem eq_12_12_smallPrimes_spec : ∀ n < 121, (n.Prime ↔ n ∈ eq_12_12_smallPrimes) := by
  decide +kernel

/-- The primality certificate is exact below `121²`: a composite `n < 121²` has its least prime
factor `≤ 120`, which divides `120!`. -/
theorem eq_12_12_cert_iff {n : ℕ} (hn : n < 14641) :
    ((n ≤ 120 ∧ n ∈ eq_12_12_smallPrimes) ∨ (120 < n ∧ Nat.Coprime n (Nat.factorial 120))) ↔
      n.Prime := by
  constructor
  · rintro (⟨h1, h⟩ | ⟨h1, h2⟩)
    · exact (eq_12_12_smallPrimes_spec n (by omega)).2 h
    · by_contra hnp
      have hmp := Nat.minFac_prime (show n ≠ 1 by omega)
      have hsq := Nat.minFac_sq_le_self (show 0 < n by omega) hnp
      have hle : n.minFac ≤ 120 := by
        by_contra hgt
        have : 121 ^ 2 ≤ n.minFac ^ 2 := Nat.pow_le_pow_left (by omega) 2
        omega
      have hd : n.minFac ∣ Nat.gcd n (Nat.factorial 120) :=
        Nat.dvd_gcd (Nat.minFac_dvd n) (Nat.dvd_factorial hmp.pos hle)
      rw [Nat.Coprime.gcd_eq_one h2] at hd
      exact hmp.one_lt.ne' (Nat.dvd_one.1 hd)
  · intro hp
    by_cases h : n ≤ 120
    · exact Or.inl ⟨h, (eq_12_12_smallPrimes_spec n (by omega)).1 hp⟩
    · refine Or.inr ⟨by omega, (Nat.Prime.coprime_iff_not_dvd hp).2 ?_⟩
      rw [hp.dvd_factorial]
      omega

theorem eq_12_12_certSet_eq {P : ℕ} (hP : P < 14641) :
    eq_12_12_certSet P = (Finset.Iic P).filter Nat.Prime :=
  Finset.filter_congr fun n hn => eq_12_12_cert_iff (by simp only [Finset.mem_Iic] at hn; omega)

/-- Kernel computation: the lower bounds multiply to more than `8` over the primes `≤ 14629`
(the quotient is `≈ 8.00000624`). -/
theorem eq_12_12_kernel_lower :
    8 * ∏ n ∈ eq_12_12_certSet 14629, eq_12_12_den n <
      ∏ n ∈ eq_12_12_certSet 14629, eq_12_12_num n := by
  decide +kernel

/-- Kernel computation: the upper bounds multiply to less than `8` over the primes `≤ 14628`
(the quotient is `≈ 7.99998298`). -/
theorem eq_12_12_kernel_upper :
    ∏ n ∈ eq_12_12_certSet 14628, eq_12_12_numUp n <
      8 * ∏ n ∈ eq_12_12_certSet 14628, eq_12_12_den n := by
  decide +kernel

/-- **The partial product of (3.9) over the primes `p ≤ 14629` exceeds `8`.** -/
theorem eq_12_12_ram95_partial :
    8 < ∏ p ∈ (Finset.Iic 14629).filter Nat.Prime, eq_12_12_ramFactor p := by
  rw [← eq_12_12_certSet_eq (by norm_num)]
  have hprime : ∀ n ∈ eq_12_12_certSet 14629, n.Prime := fun n hn => by
    rw [eq_12_12_certSet_eq (by norm_num)] at hn
    exact (Finset.mem_filter.1 hn).2
  have hB : (0 : ℝ) < ∏ n ∈ eq_12_12_certSet 14629, (eq_12_12_den n : ℝ) :=
    Finset.prod_pos fun n hn => eq_12_12_den_pos (hprime n hn).two_le
  have hk : (8 : ℝ) * ∏ n ∈ eq_12_12_certSet 14629, (eq_12_12_den n : ℝ) <
      ∏ n ∈ eq_12_12_certSet 14629, (eq_12_12_num n : ℝ) := by
    exact_mod_cast eq_12_12_kernel_lower
  calc (8 : ℝ) < (∏ n ∈ eq_12_12_certSet 14629, (eq_12_12_num n : ℝ)) /
        ∏ n ∈ eq_12_12_certSet 14629, (eq_12_12_den n : ℝ) := by
        rw [lt_div_iff₀ hB]; linarith
    _ = ∏ n ∈ eq_12_12_certSet 14629, (eq_12_12_num n : ℝ) / eq_12_12_den n :=
        (Finset.prod_div_distrib _ _).symm
    _ ≤ ∏ n ∈ eq_12_12_certSet 14629, eq_12_12_ramFactor n :=
        Finset.prod_le_prod₀ (fun n hn => by positivity)
          (fun n hn => eq_12_12_num_div_den_le (hprime n hn).two_le)

/-- **The partial product of (3.9) over the primes `p ≤ 14627` (equivalently `≤ 14628`) is less
than `8`.** -/
theorem eq_12_12_ram95_partial_prev :
    ∏ p ∈ (Finset.Iic 14628).filter Nat.Prime, eq_12_12_ramFactor p < 8 := by
  rw [← eq_12_12_certSet_eq (by norm_num)]
  have hprime : ∀ n ∈ eq_12_12_certSet 14628, n.Prime := fun n hn => by
    rw [eq_12_12_certSet_eq (by norm_num)] at hn
    exact (Finset.mem_filter.1 hn).2
  have hB : (0 : ℝ) < ∏ n ∈ eq_12_12_certSet 14628, (eq_12_12_den n : ℝ) :=
    Finset.prod_pos fun n hn => eq_12_12_den_pos (hprime n hn).two_le
  have hk : ∏ n ∈ eq_12_12_certSet 14628, (eq_12_12_numUp n : ℝ) <
      (8 : ℝ) * ∏ n ∈ eq_12_12_certSet 14628, (eq_12_12_den n : ℝ) := by
    exact_mod_cast eq_12_12_kernel_upper
  calc ∏ n ∈ eq_12_12_certSet 14628, eq_12_12_ramFactor n
      ≤ ∏ n ∈ eq_12_12_certSet 14628, (eq_12_12_numUp n : ℝ) / eq_12_12_den n :=
        Finset.prod_le_prod₀ (fun n _ => zero_le_one.trans (eq_12_12_one_le_ramFactor n))
          (fun n hn => eq_12_12_ramFactor_le_numUp (hprime n hn).two_le)
    _ = (∏ n ∈ eq_12_12_certSet 14628, (eq_12_12_numUp n : ℝ)) /
        ∏ n ∈ eq_12_12_certSet 14628, (eq_12_12_den n : ℝ) := Finset.prod_div_distrib _ _
    _ < 8 := by rw [div_lt_iff₀ hB]; linarith

/-- The partial products of (3.9) increase with `P` (every factor is `≥ 1`). -/
theorem eq_12_12_ram95_mono {P Q : ℕ} (h : P ≤ Q) :
    ∏ p ∈ (Finset.Iic P).filter Nat.Prime, eq_12_12_ramFactor p ≤
      ∏ p ∈ (Finset.Iic Q).filter Nat.Prime, eq_12_12_ramFactor p :=
  Finset.prod_le_prod_of_subset_of_one_le₀
    (Finset.filter_subset_filter _ (Finset.Iic_subset_Iic.2 h))
    (fun n _ => zero_le_one.trans (eq_12_12_one_le_ramFactor n))
    (fun n _ _ => eq_12_12_one_le_ramFactor n)

/-- **The partial product of (3.9) over the primes `p ≤ P` exceeds `8` iff `P ≥ 14629`.** -/
theorem eq_12_12_ram95_threshold (P : ℕ) :
    8 < ∏ p ∈ (Finset.Iic P).filter Nat.Prime, eq_12_12_ramFactor p ↔ 14629 ≤ P := by
  constructor
  · intro h
    by_contra hlt
    have := eq_12_12_ram95_mono (show P ≤ 14628 by omega)
    linarith [eq_12_12_ram95_partial_prev]
  · intro h
    exact lt_of_lt_of_le eq_12_12_ram95_partial (eq_12_12_ram95_mono h)

/-- The terms `(p^{1/3} + p^{2/3})/(p(p−1))` are summable over the primes (they are
`≤ 4 p^{−4/3}`), so the product in (3.9) converges. -/
theorem eq_12_12_ram95_summable :
    Summable fun p : Nat.Primes =>
      ((p : ℝ) ^ (1 / 3 : ℝ) + (p : ℝ) ^ (2 / 3 : ℝ)) / ((p : ℝ) * ((p : ℝ) - 1)) := by
  have hs : Summable fun n : ℕ => 4 * (n : ℝ) ^ (-(4 / 3) : ℝ) :=
    (Real.summable_nat_rpow.2 (by norm_num)).mul_left 4
  refine Summable.of_nonneg_of_le (fun p => ?_) (fun p => ?_) (hs.subtype Nat.Prime)
  · have h2 : (2 : ℝ) ≤ (p : ℕ) := by exact_mod_cast p.2.two_le
    have : 0 < (p : ℝ) * ((p : ℝ) - 1) := by nlinarith
    positivity
  · have h2 : (2 : ℝ) ≤ (p : ℕ) := by exact_mod_cast p.2.two_le
    set x : ℝ := ((p : ℕ) : ℝ) with hx
    have hx0 : 0 < x := by linarith
    have hpp : 0 < x * (x - 1) := by nlinarith
    have h13 : x ^ (1 / 3 : ℝ) ≤ x ^ (2 / 3 : ℝ) :=
      Real.rpow_le_rpow_of_exponent_le (by linarith) (by norm_num)
    have hneg : x ^ (-(4 / 3) : ℝ) = x ^ (2 / 3 : ℝ) / x ^ 2 := by
      rw [show (-(4 / 3) : ℝ) = 2 / 3 - (2 : ℕ) by norm_num, Real.rpow_sub hx0, Real.rpow_natCast]
    show (x ^ (1 / 3 : ℝ) + x ^ (2 / 3 : ℝ)) / (x * (x - 1)) ≤ 4 * x ^ (-(4 / 3) : ℝ)
    rw [hneg, div_le_iff₀ hpp]
    have hpos : 0 < x ^ (2 / 3 : ℝ) := by positivity
    have : 4 * (x ^ (2 / 3 : ℝ) / x ^ 2) * (x * (x - 1)) =
        x ^ (2 / 3 : ℝ) * (4 * (x - 1) / x) := by
      field_simp
    rw [this]
    have h4 : 2 ≤ 4 * (x - 1) / x := by
      rw [le_div_iff₀ hx0]; linarith
    nlinarith

/-- **[Ram95, (3.9)] is false**: the infinite product over all primes exceeds `8` (it is
`≥ ∏_{p ≤ 14629} > 8`; numerically it is `≈ 8.08356`). -/
theorem eq_12_12_ram95_3_9_false : ¬ eq_12_12_ram95_3_9 := by
  intro h
  unfold eq_12_12_ram95_3_9 at h
  have hpos : ∀ p : Nat.Primes, 0 < eq_12_12_ramFactor p := fun p =>
    lt_of_lt_of_le one_pos (eq_12_12_one_le_ramFactor p)
  have hsum : Summable fun p : Nat.Primes => Real.log (eq_12_12_ramFactor p) :=
    Real.summable_log_one_add_of_summable eq_12_12_ram95_summable
  rw [← Real.rexp_tsum_eq_tprod hpos hsum] at h
  have key : ∀ s : Finset Nat.Primes, ∏ p ∈ s, eq_12_12_ramFactor p ≤ 8 := by
    intro s
    have h1 := hsum.sum_le_tsum s (fun p _ => Real.log_nonneg (eq_12_12_one_le_ramFactor p))
    have h2 : Real.exp (∑ p ∈ s, Real.log (eq_12_12_ramFactor p)) =
        ∏ p ∈ s, eq_12_12_ramFactor p := by
      rw [Real.exp_sum]
      exact Finset.prod_congr rfl fun p _ => Real.exp_log (hpos p)
    rw [← h2]
    exact (Real.exp_le_exp.2 h1).trans h
  exact absurd ((Finset.prod_subtype_eq_prod_filter _).symm.trans_le
    (key ((Finset.Iic 14629).subtype Nat.Prime))) (not_le.2 eq_12_12_ram95_partial)

/-- The series in `c_E` ((12.14)) converges: `log p ≤ (3/2) p^{2/3}` (`Real.log_le_rpow_div`), so
its terms are at most `3/2` times those of (3.9) (`eq_12_12_ram95_summable`). So the `tsum` in
`eq_12_12_cE` is the genuine sum. -/
theorem eq_12_12_cE_summable :
    Summable fun p : Nat.Primes => Real.log p / ((p : ℝ) * ((p : ℝ) - 1)) := by
  refine Summable.of_nonneg_of_le (fun p => ?_) (fun p => ?_)
    (eq_12_12_ram95_summable.mul_left (3 / 2))
  · have h2 : (2 : ℝ) ≤ (p : ℕ) := by exact_mod_cast p.2.two_le
    have : 0 < (p : ℝ) * ((p : ℝ) - 1) := by nlinarith
    exact div_nonneg (Real.log_natCast_nonneg _) this.le
  · have h2 : (2 : ℝ) ≤ (p : ℕ) := by exact_mod_cast p.2.two_le
    have hpp : 0 < (p : ℝ) * ((p : ℝ) - 1) := by nlinarith
    have hlog : Real.log p ≤ (p : ℝ) ^ (2 / 3 : ℝ) / (2 / 3) :=
      Real.log_le_rpow_div (by positivity) (by norm_num)
    have h13 : 0 ≤ (p : ℝ) ^ (1 / 3 : ℝ) := by positivity
    rw [mul_div_assoc']
    exact div_le_div_of_nonneg_right (by linarith) hpp.le

end Companion.Book
