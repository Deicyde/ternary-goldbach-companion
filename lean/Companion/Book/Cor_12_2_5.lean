import TernaryGoldbach

/-!
# [H, Corollary 12.2.5]: the `ℓ²` norm of a prime-supported exponential sum on the major arcs

**What [H] states.** Corollary 12.2.5 (`\label{cor:coeur}`, book p. 242, PDF p. 252,
<https://arxiv.org/pdf/1501.05438v2#page=252>; it is Cor. 5.7 of the 2013 preprint
arXiv:1312.7748v2, with the same statement).  Let `{aₙ}_{n ≥ 1}` be complex numbers supported
on the primes, with `{aₙ} ∈ ℓ₁ ∩ ℓ₂` and `aₙ = 0` for `n ≤ √x`.  Let `Q₀ ≥ 10⁵` and `δ₀ ≥ 1`
satisfy `(20000 Q₀)² ≤ x/2δ₀`, set `Q = √(x/2δ₀)` and `S(α) = Σₙ aₙ e(αn)` on `ℝ/ℤ`.  Then

* for the arcs `𝔐` of (12.1), if `Q₀ ≤ Q^0.6`:
  `∫_𝔐 |S(α)|² dα ≤ (log Q₀ + c₊)/(log Q + c_E) · Σₙ |aₙ|²`;
* for the major arcs `𝔐_{δ₀,Q₀}` of (10.5), if `2Q₀ ≤ (2Q)^0.6`:
  `∫_{𝔐_{δ₀,Q₀}} |S(α)|² dα ≤ (log 2Q₀ + c₊)/(log 2Q + c_E) · Σₙ |aₙ|²`  (12.42);

where `c₊ = 1.36` and `c_E = γ + Σ_{p ≥ 2} (log p)/(p(p − 1)) = 1.3325822…` (12.14).
In [H] it is "immediate" from Props. 12.1.1, 12.1.2 (the reduction to the quotients
`G_q(Q₀/sq)/G_q(Q/sq)`) and Prop. 12.2.4 (the bound on those quotients).  The printed (12.1)
has a radius `δ₀r/qx` with an undefined `r`; we read `r = Q₀` (see `cor_12_2_5_arcs`).

**What the formalization proves.** `TernaryGoldbach.MinorArcs.cor_12_2_5`
(`TernaryGoldbach/MinorArcs/LargeSieveProof.lean:378`) proves only the second display (12.42),
for the same arcs (`TernaryGoldbach.Helfgott.majorArcs δ₀ Q₀ x`, restricted to `(0,1]`), the same
`S` (`TernaryGoldbach.expTsum`) and the same hypotheses on `aₙ`
(`TernaryGoldbach.MinorArcs.PrimeSupported`, see `cor_12_2_5_coeffs_iff`), but weaker:
* `δ₀ ≥ 2` instead of `δ₀ ≥ 1`.  This comes from the formal proof of Prop. 12.1.2
  (`TernaryGoldbach.MinorArcs.prop_12_1_2`, which also assumes `δ₀ ≥ 2`): it takes the common
  modulus `L = ∏_{q ≤ 2Q} q` and so needs every prime `n > √x` to be coprime to every
  `q ≤ 2Q = √(2x/δ₀)`, odd ones included, i.e. `2Q ≤ √x`.  [H]'s argument has no such
  restriction.  The moduli in its proof of Prop. 12.1.2 are odd `q ≤ Q` (odd `q ≤ Q₀`, and odd
  `qr ≤ Q` in `Σ₁`) or even `q ≤ 2Q` (even `q ≤ 2Q₀`, and even `qr ≤ 2Q` in `Σ₁` and `Σ₂`), and
  every odd prime factor `p` of an even `q ≤ 2Q` has `2p ≤ q ≤ 2Q`, so `p ≤ Q < √x`; as
  `n > √x > 2` is odd, `n` is coprime to all of these moduli once `δ₀ ≥ 1`.  [H] justifies the
  coprimality explicitly only for moduli `≤ √x` (in the proof of Prop. 12.1.1), but the even
  moduli in `(√x, 2Q]` are covered by this remark (cf. `Companion.Book.prop_12_1_2_holds`, which
  proves [H]'s Prop. 12.1.2 for every `δ₀ ≥ 1`).  So the restriction is an artefact of the
  formal proof, not a gap in [H].  [H] applies the corollary only with `δ₀ = 8` (Ch. 13).
* `c₊ = 2` instead of `1.36`: its Prop. 12.2.4 (`TernaryGoldbach.MinorArcs.prop_12_2_4`) is
  proved with `c₊ = 2`.  [H]'s `1.36` rests on an interval-arithmetic computation
  (pp. 241–242, footnote 2 on p. 242) that checks every `q < 3.3·10⁹` and every
  `q ∈ [3.3·10⁹, 2.2·10¹⁰)` with `210 ∣ q`.  The Lean proof follows [H] only for
  `q ≥ 2.2·10¹⁰` (where it reaches `1.36`, then weakens it to `2`); for `q < 2.2·10¹⁰` it uses
  instead a reduction to the divisors of `30030` and kernel checks, which need the room that
  `c₊ = 2` gives (`TernaryGoldbach/MinorArcs/LSQuot6.lean`).
* `c_E` replaced by the smaller rational `TernaryGoldbach.MinorArcs.cE = 1.33258`, i.e. `c_E`
  rounded down (`cor_12_2_5_cE_round_down`, from the repo's `1.3325822 ≤ c_E ≤ 1.3325823`).

The first display (arcs (12.1), via Prop. 12.1.1) is not formalized.  The formal theorem also
carries the hypothesis `[Fact PlattGRH]` (its proof of Prop. 12.2.4 uses it); here it is just a
binder of the target.

**Relation, and how it is certified here.**
* `cor_12_2_5` is [H]'s statement as printed (both displays).
* `cor_12_2_5_implies_formal : cor_12_2_5 → type_of% @TernaryGoldbach.MinorArcs.cor_12_2_5`:
  the book's statement implies the formal one (verdict: the Lean result is *weaker*).  Only the
  second display is used: `δ₀ ≥ 2` gives `δ₀ ≥ 1`, and
  `(log 2Q₀ + 1.36)/(log 2Q + c_E) ≤ (log 2Q₀ + 2)/(log 2Q + 1.33258)` because
  `0 ≤ log 2Q₀ ≤ 0.6 log 2Q`, `log 2Q ≥ 6` (as `2Q ≥ 4·10⁹`) and `c_E > 1/2`
  (`cor_12_2_5_cE_gt`).  So the implication does not depend on the decimal value `1.3325822…`
  of `c_E`: the slack between `2` and `1.36` absorbs any `c_E > 1/2`.
* Sanity checks on the transcription: `cor_12_2_5_coeffs_iff` (the book's hypotheses on `aₙ`
  are exactly the repo's `PrimeSupported`), `cor_12_2_5_cE_summable` (the series in `c_E`
  converges, so the `tsum` in `cor_12_2_5_cE` is the actual sum), `cor_12_2_5_cE_eq_cR` and
  `cor_12_2_5_cE_bounds` (`cor_12_2_5_cE` is the repo's `Prelim.RamPf.cR`, so
  `1.3325822 ≤ c_E ≤ 1.3325823`, matching the printed `1.3325822…`), and
  `cor_12_2_5_hyps_satisfiable` (the hypotheses of both displays hold at once with `aₙ ≢ 0`,
  so `cor_12_2_5` is not vacuous).
-/

open MeasureTheory Set

namespace Companion.Book

open TernaryGoldbach

/-- The constant `c_E = γ + Σ_{p ≥ 2} (log p)/(p(p − 1))` of [H, (12.14)] (`eq:garno`), used in
[H, Cor. 12.2.5].  Defined by the series, as printed; the decimal value `1.3325822…` that [H]
quotes is not part of the definition.  The sum runs over the primes (`Nat.Primes`); it converges
(`cor_12_2_5_cE_summable`), so the `tsum` is the true sum.  `γ` is Mathlib's
`Real.eulerMascheroniConstant`.  It equals the repo's `TernaryGoldbach.Prelim.RamPf.cR`
(`cor_12_2_5_cE_eq_cR`), so the repo's bounds give `1.3325822 ≤ c_E ≤ 1.3325823`
(`cor_12_2_5_cE_bounds`).  This is *not* the repo's `TernaryGoldbach.MinorArcs.cE`, which is the
rounded-down rational `1.33258` (`cor_12_2_5_cE_round_down`). -/
noncomputable def cor_12_2_5_cE : ℝ :=
  Real.eulerMascheroniConstant +
    ∑' p : Nat.Primes, Real.log ((p : ℕ) : ℝ) / (((p : ℕ) : ℝ) * (((p : ℕ) : ℝ) - 1))

/-- The hypotheses of [H, Cor. 12.2.5] on the coefficients: "`{aₙ}_{n=1}^∞`, `aₙ ∈ ℂ`, supported
on the primes; `{aₙ} ∈ ℓ₁ ∩ ℓ₂`; `aₙ = 0` for `n ≤ √x`", transcribed clause by clause (the `ℓ₂`
clause is redundant, as `ℓ₁ ⊆ ℓ₂`, but is kept as printed).  The sequence is `a : ℕ → ℂ`; the
extra index `0` is harmless, since `a 0 = 0` is forced both by prime support and by
`0 ≤ √x`.  Equivalent to the repo's `TernaryGoldbach.MinorArcs.PrimeSupported x a`
(`cor_12_2_5_coeffs_iff`). -/
def cor_12_2_5_coeffs (x : ℝ) (a : ℕ → ℂ) : Prop :=
  (∀ n : ℕ, a n ≠ 0 → n.Prime) ∧
    (Summable fun n => ‖a n‖) ∧ (Summable fun n => ‖a n‖ ^ 2) ∧
    ∀ n : ℕ, (n : ℝ) ≤ √x → a n = 0

/-- The arcs `𝔐` of [H, (12.1)] (`eq:jokor`, in Prop. 12.1.1), used in the first display of
[H, Cor. 12.2.5]:
`𝔐 = ⋃_{q ≤ Q₀} ⋃_{a mod q, (a,q)=1} (a/q − δ₀r/qx, a/q + δ₀r/qx)`.

*Reading.* The printed (12.1) has a radius `δ₀r/(qx)` with an `r` that Prop. 12.1.1 never
introduces (a leftover from (10.5), where `r` is the parameter of `𝔐_{δ₀,r}`; the 2013 preprint
has the same `r`).  We read `r = Q₀`: this is what the proof of Prop. 12.1.1 integrates over
((12.3): `|α| ≤ δ₀Q₀/qx`), and it makes `𝔐` the analogue of `𝔐_{δ₀,Q₀}` without the
odd/even distinction.

*Encoding.* Not in the repo (Prop. 12.1.1 is not formalized), so defined here, in exactly the
encoding of the repo's `TernaryGoldbach.Helfgott.majorArcs`: the arcs are lifted from `ℝ/ℤ` to
`ℝ` by letting `a` run over *all* integers coprime to `q` (so the set is 1-periodic and is the
preimage of [H]'s subset of `ℝ/ℤ`), `q` runs over `1 ≤ q ≤ Q₀`, `(a, q) = 1` is
`IsCoprime (a : ℤ) q`, and the arcs are open intervals. -/
def cor_12_2_5_arcs (δ₀ Q₀ x : ℝ) : Set ℝ :=
  ⋃ (q : ℕ) (_ : 1 ≤ q ∧ (q : ℝ) ≤ Q₀) (a : ℤ) (_ : IsCoprime a (q : ℤ)),
    Set.Ioo ((a : ℝ) / q - δ₀ * Q₀ / (q * x)) ((a : ℝ) / q + δ₀ * Q₀ / (q * x))

/-- **[H, Corollary 12.2.5]**, as printed (both displays, the second being (12.42)).

Transcription choices:
* `x δ₀ Q₀ : ℝ` and `a : ℕ → ℂ` are universally quantified; the hypotheses on `{aₙ}` are
  `cor_12_2_5_coeffs x a` (see there).
* `Q₀ ≥ 10⁵`, `δ₀ ≥ 1` and `(20000 Q₀)² ≤ x/2δ₀` are verbatim, reading `x/2δ₀` as `x/(2δ₀)`
  (as in `Q = √(x/2δ₀)`).  Together they force `x > 0`, which [H] leaves implicit.
* "set `Q = √(x/2δ₀)`" is the local definition `let Q := √(x / (2 * δ₀))`.
* `S(α) = Σₙ aₙ e(αn)` is the repo's `TernaryGoldbach.expTsum a α = ∑' n, a n * e (n * α)`,
  with `TernaryGoldbach.e t = exp(2πit)`, which is [H]'s `e(t) = e^{2πit}`; the series
  converges absolutely because `a ∈ ℓ₁`.
* `∫_{𝔐} |S(α)|² dα`, for `𝔐 ⊆ ℝ/ℤ`, is the Lebesgue integral of `‖S α‖ ^ 2` over
  `(0,1] ∩ 𝔐̃`, where `𝔐̃ ⊆ ℝ` is the 1-periodic preimage of `𝔐`.  As `(0,1]` is a fundamental
  domain, this is the integral for the Haar probability measure on `ℝ/ℤ` (the measure for which
  [H] writes `∫_{ℝ/ℤ} |S|² = Σ |aₙ|²`).
* First display: `𝔐` is (12.1), `cor_12_2_5_arcs δ₀ Q₀ x` (with [H]'s undefined `r` read as
  `Q₀`, see there); the condition `Q₀ ≤ Q^{0.6}` uses the real power `Q ^ (0.6 : ℝ)`.
* Second display (12.42): `𝔐_{δ₀,Q₀}` is (10.5) with `r = Q₀`, i.e. the repo's
  `TernaryGoldbach.Helfgott.majorArcs δ₀ Q₀ x`, checked against the LaTeX of (10.5): radius
  `δ₀r/2qx` around `a/q` for odd `q ≤ r`, radius `δ₀r/qx` for even `q ≤ 2r`, `(a, q) = 1`, open
  intervals, lifted to `ℝ` as for (12.1).  The condition `(2Q₀) ≤ (2Q)^{0.6}` uses the real
  power; `log 2Q₀` and `log 2Q` are `log (2Q₀)` and `log (2Q)`.
* `c₊ = 1.36` is the literal `1.36`; `c_E` is `cor_12_2_5_cE`, defined by its series.
* `Σₙ |aₙ|²` is `∑' n, ‖a n‖ ^ 2` (a convergent series, as `a ∈ ℓ₂`). -/
def cor_12_2_5 : Prop :=
  ∀ (x δ₀ Q₀ : ℝ) (a : ℕ → ℂ), cor_12_2_5_coeffs x a →
    (10 : ℝ) ^ 5 ≤ Q₀ → 1 ≤ δ₀ → (20000 * Q₀) ^ 2 ≤ x / (2 * δ₀) →
    let Q := √(x / (2 * δ₀))
    (Q₀ ≤ Q ^ (0.6 : ℝ) →
      ∫ α in Ioc (0 : ℝ) 1 ∩ cor_12_2_5_arcs δ₀ Q₀ x, ‖expTsum a α‖ ^ 2 ≤
        (Real.log Q₀ + 1.36) / (Real.log Q + cor_12_2_5_cE) * ∑' n, ‖a n‖ ^ 2) ∧
    (2 * Q₀ ≤ (2 * Q) ^ (0.6 : ℝ) →
      ∫ α in Ioc (0 : ℝ) 1 ∩ Helfgott.majorArcs δ₀ Q₀ x, ‖expTsum a α‖ ^ 2 ≤
        (Real.log (2 * Q₀) + 1.36) / (Real.log (2 * Q) + cor_12_2_5_cE) * ∑' n, ‖a n‖ ^ 2)

/-! ## Sanity checks on the transcription -/

/-- The book's hypotheses on `{aₙ}` are exactly the repo's `PrimeSupported x a` (prime support,
`aₙ = 0` for `n ≤ √x`, `ℓ₁`; the `ℓ₂` clause follows from `ℓ₁`). -/
theorem cor_12_2_5_coeffs_iff (x : ℝ) (a : ℕ → ℂ) :
    cor_12_2_5_coeffs x a ↔ MinorArcs.PrimeSupported x a := by
  constructor
  · rintro ⟨hp, h1, -, hx⟩
    refine ⟨fun n hn => ⟨hp n hn, ?_⟩, h1⟩
    by_contra hle
    exact hn (hx n (not_lt.1 hle))
  · rintro ⟨hs, h1⟩
    refine ⟨fun n hn => (hs n hn).1, h1, summable_norm_sq_of_summable_norm h1, fun n hn => ?_⟩
    by_contra h0
    exact (not_lt.2 hn) (hs n h0).2

/-- The series `Σ_p (log p)/(p(p − 1))` in `c_E` converges (compare with `4 n^{-3/2}`, using
`log n ≤ 2√n`), so `cor_12_2_5_cE` is [H]'s constant and not a junk value of `tsum`. -/
theorem cor_12_2_5_cE_summable :
    Summable fun p : Nat.Primes =>
      Real.log ((p : ℕ) : ℝ) / (((p : ℕ) : ℝ) * (((p : ℕ) : ℝ) - 1)) := by
  have key : ∀ n : ℕ, 2 ≤ n →
      Real.log n / ((n : ℝ) * ((n : ℝ) - 1)) ≤ 4 * ((n : ℝ) ^ (3 / 2 : ℝ))⁻¹ := by
    intro n hn
    have hn' : (2 : ℝ) ≤ n := by exact_mod_cast hn
    have hs : 0 < √(n : ℝ) := Real.sqrt_pos.2 (by linarith)
    have hss : √(n : ℝ) * √(n : ℝ) = n := Real.mul_self_sqrt (by linarith)
    have hlog : Real.log n ≤ 2 * √(n : ℝ) := by
      have h := Real.log_le_rpow_div (x := (n : ℝ)) (by linarith) (by norm_num : (0 : ℝ) < 1 / 2)
      rw [← Real.sqrt_eq_rpow] at h
      linarith
    have hpow : (n : ℝ) ^ (3 / 2 : ℝ) = n * √(n : ℝ) := by
      rw [show (3 / 2 : ℝ) = 1 + 1 / 2 by norm_num, Real.rpow_add (by linarith), Real.rpow_one,
        ← Real.sqrt_eq_rpow]
    rw [hpow, div_le_iff₀ (by nlinarith)]
    have e : 4 * ((n : ℝ) * √(n : ℝ))⁻¹ * ((n : ℝ) * ((n : ℝ) - 1)) =
        4 * ((n : ℝ) - 1) / √(n : ℝ) := by
      field_simp
    rw [e, le_div_iff₀ hs]
    nlinarith
  have hg : Summable fun n : ℕ => Real.log n / ((n : ℝ) * ((n : ℝ) - 1)) := by
    refine Summable.of_nonneg_of_le (f := fun n : ℕ => 4 * ((n : ℝ) ^ (3 / 2 : ℝ))⁻¹)
      (fun n => ?_) (fun n => ?_) ((Real.summable_nat_rpow_inv.2 (by norm_num)).mul_left 4)
    · rcases Nat.lt_or_ge n 2 with hn | hn
      · interval_cases n <;> simp
      · have hn' : (2 : ℝ) ≤ n := by exact_mod_cast hn
        exact div_nonneg (Real.log_nonneg (by linarith)) (by nlinarith)
    · rcases Nat.lt_or_ge n 2 with hn | hn
      · interval_cases n <;> norm_num
      · exact key n hn
  exact hg.subtype _

/-- `c_E > 1/2` (from `γ > 1/2` and the nonnegativity of the series).  This is the only property
of `c_E` that `cor_12_2_5_implies_formal` uses. -/
theorem cor_12_2_5_cE_gt : 1 / 2 < cor_12_2_5_cE := by
  unfold cor_12_2_5_cE
  have h1 := Real.one_half_lt_eulerMascheroniConstant
  have h2 : 0 ≤ ∑' p : Nat.Primes,
      Real.log ((p : ℕ) : ℝ) / (((p : ℕ) : ℝ) * (((p : ℕ) : ℝ) - 1)) := by
    refine tsum_nonneg fun p => ?_
    have : (2 : ℝ) ≤ ((p : ℕ) : ℝ) := by exact_mod_cast p.2.two_le
    exact div_nonneg (Real.log_nonneg (by linarith)) (by nlinarith)
  linarith

/-- `cor_12_2_5_cE` is the repo's `TernaryGoldbach.Prelim.RamPf.cR`
(`γ + ∑' p : ℕ, if p.Prime then log p/(p(p − 1)) else 0`): summing over the subtype
`Nat.Primes` or over `ℕ` with an indicator gives the same `tsum` (`tsum_subtype`). -/
theorem cor_12_2_5_cE_eq_cR : cor_12_2_5_cE = Prelim.RamPf.cR := by
  unfold cor_12_2_5_cE Prelim.RamPf.cR Prelim.RamPf.sumP
  congr 1
  exact (tsum_subtype {p : ℕ | p.Prime}
    (fun n : ℕ => Real.log (n : ℝ) / ((n : ℝ) * ((n : ℝ) - 1)))).trans
    (tsum_congr fun n => by simp [Set.indicator])

/-- The printed value `c_E = 1.3325822…`: `1.3325822 ≤ c_E ≤ 1.3325823`, from the repo's
`TernaryGoldbach.Prelim.RamPf.cR_bounds` and `cor_12_2_5_cE_eq_cR`. -/
theorem cor_12_2_5_cE_bounds :
    (1.3325822 : ℝ) ≤ cor_12_2_5_cE ∧ cor_12_2_5_cE ≤ 1.3325823 :=
  cor_12_2_5_cE_eq_cR ▸ Prelim.RamPf.cR_bounds

/-- The formalization's `TernaryGoldbach.MinorArcs.cE = 1.33258` is [H]'s `c_E` rounded *down*,
so using it in the denominator of (12.42) weakens the bound.  (`cor_12_2_5_implies_formal` does
not use this; it needs only `c_E > 1/2`.) -/
theorem cor_12_2_5_cE_round_down :
    MinorArcs.cE < cor_12_2_5_cE := by
  have h := cor_12_2_5_cE_bounds.1
  unfold MinorArcs.cE
  linarith

/-- The hypotheses of `cor_12_2_5` are consistent, for both displays at once and with a non-zero
sequence: `x = 2·10³⁰`, `δ₀ = 1`, `Q₀ = 10⁵` (so `Q = 10¹⁵`) and `a = 𝟙_{p}` for a prime
`p ≥ 2·10¹⁵ > √x`.  So `cor_12_2_5` is not vacuous. -/
theorem cor_12_2_5_hyps_satisfiable :
    ∃ (x δ₀ Q₀ : ℝ) (a : ℕ → ℂ), cor_12_2_5_coeffs x a ∧ a ≠ 0 ∧
      (10 : ℝ) ^ 5 ≤ Q₀ ∧ 1 ≤ δ₀ ∧ (20000 * Q₀) ^ 2 ≤ x / (2 * δ₀) ∧
      Q₀ ≤ (√(x / (2 * δ₀))) ^ (0.6 : ℝ) ∧ 2 * Q₀ ≤ (2 * √(x / (2 * δ₀))) ^ (0.6 : ℝ) := by
  obtain ⟨p, hp, hpp⟩ := Nat.exists_infinite_primes (2 * 10 ^ 15)
  have hp' : (2 * 10 ^ 15 : ℝ) ≤ p := by exact_mod_cast hp
  have hQ : √((2 * 10 ^ 30 : ℝ) / (2 * 1)) = 10 ^ 15 := by
    rw [show (2 * 10 ^ 30 : ℝ) / (2 * 1) = (10 ^ 15) ^ 2 by norm_num]
    exact Real.sqrt_sq (by norm_num)
  -- `y ≤ √z ≤ z ^ 0.6` for `z ≥ 1`
  have hrpow : ∀ y z : ℝ, 1 ≤ z → y ^ 2 ≤ z → y ≤ z ^ (0.6 : ℝ) := fun y z hz h =>
    (Real.le_sqrt_of_sq_le h).trans <| by
      rw [Real.sqrt_eq_rpow]; exact Real.rpow_le_rpow_of_exponent_le hz (by norm_num)
  refine ⟨2 * 10 ^ 30, 1, 10 ^ 5, fun n => if n = p then 1 else 0, ⟨?_, ?_, ?_, ?_⟩, ?_,
    le_rfl, le_rfl, ?_, ?_, ?_⟩
  · intro n hn
    by_cases h : n = p
    · exact h ▸ hpp
    · simp [h] at hn
  · exact summable_of_ne_finset_zero (s := {p}) fun n hn => by
      simp only [Finset.mem_singleton] at hn; simp [hn]
  · exact summable_of_ne_finset_zero (s := {p}) fun n hn => by
      simp only [Finset.mem_singleton] at hn; simp [hn]
  · intro n hn
    by_cases h : n = p
    · exfalso
      subst h
      have hsq : √(2 * 10 ^ 30 : ℝ) < 2 * 10 ^ 15 := by
        rw [Real.sqrt_lt' (by norm_num)]; norm_num
      linarith
    · simp [h]
  · intro h
    have := congrFun h p
    simp at this
  · norm_num
  · rw [hQ]; exact hrpow _ _ (by norm_num) (by norm_num)
  · rw [hQ]; exact hrpow _ _ (by norm_num) (by norm_num)

/-! ## The relation with the formalization -/

/-- **[H, Cor. 12.2.5] implies the formal `TernaryGoldbach.MinorArcs.cor_12_2_5`** (which is the
second display (12.42) with `δ₀ ≥ 2`, `c₊ = 2` and `c_E` replaced by `1.33258`): the Lean result
is weaker.  Proof: apply the book's (12.42) (`δ₀ ≥ 2 ⇒ δ₀ ≥ 1`, `1e5 = 10⁵`, the coefficient
hypotheses by `cor_12_2_5_coeffs_iff`) and compare the factors:
with `L₀ = log 2Q₀ ∈ [0, 0.6 L]`, `L = log 2Q ≥ 6` (as `2Q ≥ 4·10⁹`) and `c_E > 1/2`,
`(L₀ + 2)(L + c_E) − (L₀ + 1.36)(L + 1.33258) ≥ (c_E − 1/2) L₀ + 0.1404 L + 2 c_E − 1.8124 ≥ 0`. -/
theorem cor_12_2_5_implies_formal :
    cor_12_2_5 → type_of% @TernaryGoldbach.MinorArcs.cor_12_2_5 := by
  intro h _ x δ₀ Q₀ a ha hQ₀ hδ₀ hx hρ
  have hQ₀' : (10 : ℝ) ^ 5 ≤ Q₀ := by norm_num at hQ₀ ⊢; linarith
  have hbook := (h x δ₀ Q₀ a ((cor_12_2_5_coeffs_iff x a).2 ha) hQ₀' (by linarith) hx).2 hρ
  refine hbook.trans (mul_le_mul_of_nonneg_right ?_ (tsum_nonneg fun n => by positivity))
  set Q := √(x / (2 * δ₀)) with hQdef
  have hQ : 20000 * Q₀ ≤ Q := Real.le_sqrt_of_sq_le hx
  have hc := cor_12_2_5_cE_gt
  have hL₀ : 0 ≤ Real.log (2 * Q₀) := Real.log_nonneg (by linarith)
  have hρ' : Real.log (2 * Q₀) ≤ 0.6 * Real.log (2 * Q) := by
    have h' := Real.log_le_log (by linarith) hρ
    rwa [Real.log_rpow (by linarith)] at h'
  have hL : 6 ≤ Real.log (2 * Q) := by
    rw [Real.le_log_iff_exp_le (by linarith)]
    have he : Real.exp 6 = Real.exp 1 ^ 6 := by
      rw [← Real.exp_nat_mul]; norm_num
    have h3 : Real.exp 1 ^ 6 ≤ 3 ^ 6 :=
      pow_le_pow_left₀ (Real.exp_pos 1).le (Real.exp_one_lt_d9.le.trans (by norm_num)) 6
    rw [he]
    nlinarith
  have hd1 : 0 < Real.log (2 * Q) + cor_12_2_5_cE := by linarith
  have hd2 : 0 < Real.log (2 * Q) + MinorArcs.cE := by unfold MinorArcs.cE; linarith
  rw [div_le_div_iff₀ hd1 hd2]
  unfold MinorArcs.cE
  nlinarith [mul_nonneg (sub_nonneg.2 hc.le) hL₀]

end Companion.Book
