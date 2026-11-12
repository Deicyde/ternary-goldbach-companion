import TernaryGoldbach

/-!
# [H, Theorem 3.1.1]: the main minor-arc bound for `|S_η(α, x)|`

**Source.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2 ("[H]"),
Theorem 3.1.1 (label `thm:minmain`), §3.1, book page 44 = PDF page 54:
<https://arxiv.org/pdf/1501.05438v2#page=54>. Its proof is [H, §6.4] (book p. 133).

**What [H] states.** Let `x ≥ x₀ = 2.16·10²⁰`, let `S_η(α, x) = ∑ₙ Λ(n) e(αn) η(n/x)` (3.1) with
`η = η₂`, `η₂(t) = 4 max(log 2 - |log 2t|, 0)` (3.4), and let `2α = a/q + δ/x` with `q ≤ Q`,
`gcd(a, q) = 1`, `|δ/x| ≤ 1/qQ`, where `Q = (3/4) x^{2/3}`. If `q ≤ x^{1/3}/6`, then (3.2)

`|S_η(α,x)| ≤ (R_{x,δ₀q} log δ₀q + 0.5)/√(δ₀ φ(q)) · x + 2.5 x/√(δ₀q) + 2x/(δ₀q) · L_{x,δ₀q,q} + 3.36 x^{5/6}`,

where (3.3) `δ₀ = max(2, |δ|/4)`,
`R_{x,t} = 0.27125 log(1 + log 4t / (2 log (9 x^{1/3}/(2.004 t)))) + 0.41415` and
`L_{x,t,q} = (q/φ(q)) (13/4 log t + 7.82) + 13.66 log t + 37.55`. If `q > x^{1/3}/6`, then
`|S_η(α,x)| ≤ 0.276 x^{5/6} (log x)^{3/2} + 1234 x^{2/3} log x`.

**What the formalization proves.** `TernaryGoldbach.MinorArcs.theorem_3_1_1`
(`TernaryGoldbach/MinorArcs/PointwiseBound.lean`), from the inputs `[Fact PlattGRH]` and
`[Fact RamareMoebius]`, proves the same statement: the same hypotheses (bundled as
`MinorArcs.Approx2 α x δ a q ((3/4) x^{2/3})`, i.e. `1 ≤ q`, `IsCoprime a q`,
`∃ k : ℤ, 2α = a/q + δ/x + k`, `|δ/x| ≤ 1/(qQ)`, `q ≤ Q`), the same `δ₀`, `R` (`MinorArcs.R`), `L`
(`MinorArcs.L`), the same second case with `0.276` and `1234` — except that the three constants
`0.5`, `2.5`, `3.36` of the first case are `0.8764`, `2.526`, `3.8`.

Why `0.8764` (documented in the docstring of `MinorArcs.theorem_3_1_1`): in [H, (6.76)–(6.77)] the
AM–GM step `√A·√B ≤ A/(2√ρ) + (√ρ/2)B` with `B = 0.30214 log δ₀q + 0.67506`, `ρ = 3.397962…`, has
constant term `log 2/(2√ρ) + (√ρ/2)·0.67506 = 0.81020…`, but [H] writes
`(1/2)(log 2/√ρ + (√ρ/2)·0.67506) = 0.49911`. With `0.5` the printed bound (3.2) therefore does not
follow from [H]'s own intermediate bound (6.63): at some admissible parameters (6.63) is larger than
(3.2). The excess is about 2.65% when `φ(q)/q ≈ 1` (e.g. `x = 10²⁵`, `δ₀ = 2`, `q ≈ 9·10⁴` prime;
this is the "~2.6%" in the repo's docstring). It reaches about 3.2% when `φ(q)/q` is small: 3.18% at
`x = 10²⁵`, `δ₀ = 2`, `q = 60060` (`φ(q) = 11520`), and 3.19% at `x = 10²⁴`, `q = 30030`
(`φ(q) = 5760`), `δ₀ ≈ 3.5` (so `|δ| ≈ 14`, well inside the allowed `|δ| ≤ (4/3) x^{1/3}/q ≈ 4440`).
Both bounds depend on `(x, δ, q)` only through `x`, `δ₀q` and `φ(q)/q`. A grid scan over
`2.16·10²⁰ ≤ x ≤ 10³⁰⁰`, all `q ≤ x^{1/3}/6` and `δ₀q ∈ [2q, x^{1/3}/3]` finds a maximum excess of
about 3.2% (3.1955%, near `x = 10^{23.6}`, `δ₀q ≈ 9.5·10⁴`, `q = 30030`). (`ρ`, `0.81020`,
`0.49911` and these percentages were re-computed for this file.) The repo also corrects
[H, (5.36)], which raises the constant to `0.87639`. For the other two constants [H]'s proof ends
with `2.492` and `3.36`; the formal theorem states the looser `2.526` and `3.8`.

**Relation (status: implied, [H] ⇒ formal).** The three changed constants multiply the nonnegative
quantities `x/√(δ₀ φ(q))`, `x/√(δ₀ q)` and `x^{5/6}`, so [H]'s first-case bound is at most the formal
one, and everything else coincides. `thm_3_1_1_implies_formal` proves
`thm_3_1_1 → type_of% @TernaryGoldbach.MinorArcs.theorem_3_1_1`. More precisely,
`thm_3_1_1_with c₁ c₂ c₃` is [H]'s statement with `0.5, 2.5, 3.36` replaced by `c₁, c₂, c₃`
(`thm_3_1_1_eq_with : thm_3_1_1 = thm_3_1_1_with 0.5 2.5 3.36` holds by `rfl`), and
`thm_3_1_1_with_formal_iff` shows that the formal theorem *is* `thm_3_1_1_with 0.8764 2.526 3.8`
under the two `Fact`s. In particular [H]'s second case is proved verbatim
(`thm_3_1_1_with_formal`).

The printed first case (with `0.5, 2.5, 3.36`) is neither proved nor refuted here: the erratum is a
gap in [H]'s proof, not a counterexample to (3.2), and `|S_η(α, x)|` cannot be evaluated for
`x ≥ 2.16·10²⁰`.

**Transcription checks.** `thm_3_1_1_R_eq`, `thm_3_1_1_L_eq` (both `rfl`), `thm_3_1_1_eta2_eq` and
`thm_3_1_1_S_eq` check that the repo's `R`, `L`, `η₂` and `S` are [H]'s objects, and
`thm_3_1_1_hyp_satisfiable` shows that the hypotheses can be met in each of the two cases, so
neither half of `thm_3_1_1` is vacuous.

The 2013 preprint (arXiv:1205.5252v4, Main Theorem) states the theorem with another `L` and the
constants `3.2` (for `x^{5/6}`), `0.2727`, `1218`; this file follows the book.
-/

namespace Companion.Book

open TernaryGoldbach

/-- The standing hypotheses of [H, Theorem 3.1.1] on `(x, α, δ, a, q)`:
`x ≥ x₀ = 2.16·10²⁰`, and `2α = a/q + δ/x` with `q ≤ Q`, `gcd(a, q) = 1`, `|δ/x| ≤ 1/qQ`,
where `Q = (3/4) x^{2/3}`.

Transcription choices:
* `x`, `δ` are real, `a` is an integer and `q` a positive integer (`q : ℕ`, `0 < q`; [H] leaves this
  implicit: `q` is the denominator of `a/q` and appears in `φ(q)`, `log δ₀q`).
* [H] takes `α ∈ ℝ/ℤ` ((3.1)), so `2α = a/q + δ/x` is an identity in `ℝ/ℤ`; with a real
  representative `α` it reads `2α = a/q + δ/x + k` for some `k ∈ ℤ`. (Reading it in `ℝ` instead gives
  an equivalent theorem: replace `a` by `a + kq`, which keeps `gcd(a, q) = 1`.)
* `gcd(a, q) = 1` is `Int.gcd a q = 1`; `1/qQ` is `1/(q·Q)`; `x^{2/3}` is the real power `rpow`. -/
def thm_3_1_1_hyp (x α δ : ℝ) (a : ℤ) (q : ℕ) : Prop :=
  let Q : ℝ := 3 / 4 * x ^ (2 / 3 : ℝ)
  2.16 * 10 ^ 20 ≤ x ∧ 0 < q ∧ (∃ k : ℤ, 2 * α = a / q + δ / x + k) ∧ (q : ℝ) ≤ Q ∧
    Int.gcd a q = 1 ∧ |δ / x| ≤ 1 / (q * Q)

/-- **[H, Theorem 3.1.1]**, as printed (book p. 44). Under the standing hypotheses
`thm_3_1_1_hyp x α δ a q` (`x ≥ 2.16·10²⁰`, `2α = a/q + δ/x` in `ℝ/ℤ`, `q ≤ Q`, `gcd(a, q) = 1`,
`|δ/x| ≤ 1/qQ`, `Q = (3/4) x^{2/3}`), with `δ₀ = max(2, |δ|/4)`:
* if `q ≤ x^{1/3}/6`, then (3.2)
  `|S_η(α,x)| ≤ (R_{x,δ₀q} log δ₀q + 0.5)/√(δ₀φ(q)) · x + 2.5x/√(δ₀q) + 2x/(δ₀q) · L_{x,δ₀q,q} + 3.36 x^{5/6}`;
* if `q > x^{1/3}/6`, then `|S_η(α,x)| ≤ 0.276 x^{5/6} (log x)^{3/2} + 1234 x^{2/3} log x`.

Transcription choices:
* `S_η(α, x)` of (3.1) with `η = η₂` of (3.4) is `Helfgott.S Helfgott.eta2 x α` (note the argument
  order `x, α`): `∑' n : ℕ, Λ(n) η₂(n/x) e(nα)` with `e(t) = exp(2πit)` and Mathlib's von Mangoldt
  function. The `n = 0` term vanishes (`Λ(0) = 0`), `Helfgott.eta2` is `η₂` on `t > 0` (it is `0`
  for `t ≤ 0`, where [H]'s `η₂ : ℝ⁺ → ℝ` is undefined and which no `n ≥ 1` reaches), and
  `η₂(n/x) = 0` for `n ≥ x`, so the `tsum` is [H]'s finite sum: see `thm_3_1_1_eta2_eq`,
  `thm_3_1_1_S_eq`. The absolute value `|·|` on `ℂ` is the norm `‖·‖`.
* `R_{x,t}` and `L_{x,t,q}` of (3.3) are the repo's `MinorArcs.R x t` and `MinorArcs.L t q`, which
  are literally [H]'s formulas (`thm_3_1_1_R_eq`, `thm_3_1_1_L_eq`, by `rfl`; `L_{x,t,q}` does not
  depend on `x` despite its subscript, so `MinorArcs.L` has no `x` argument; `q/φ(q)` is a real
  quotient). `log` is the natural logarithm `Real.log`; `log δ₀q` is `log (δ₀ q)`, `log 4t` is
  `log (4t)`. In the first case all logarithms have arguments `> 1` (`δ₀q ≥ 2`, and
  `δ₀q ≤ x^{1/3}/3` because `|δ| ≤ x/(qQ) = (4/3) x^{1/3}/q`, so `9x^{1/3}/(2.004 δ₀q) ≥ 13.4`), so
  the junk values of `Real.log` and of division by `0` never enter.
* `δ₀ = max(2, |δ|/4)` is a `let`; `x^{1/3}`, `x^{2/3}`, `x^{5/6}`, `(log x)^{3/2}` are real powers
  (`rpow`, with positive bases since `x ≥ 2.16·10²⁰`); `φ` is `Nat.totient`.
* The two cases "if `q ≤ x^{1/3}/6`" and "if `q > x^{1/3}/6`" are the two conjuncts. -/
def thm_3_1_1 : Prop :=
  ∀ (x α δ : ℝ) (a : ℤ) (q : ℕ), thm_3_1_1_hyp x α δ a q →
    let δ₀ : ℝ := max 2 (|δ| / 4)
    ((q : ℝ) ≤ x ^ (1 / 3 : ℝ) / 6 →
      ‖Helfgott.S Helfgott.eta2 x α‖ ≤
        (MinorArcs.R x (δ₀ * q) * Real.log (δ₀ * q) + 0.5) / √(δ₀ * Nat.totient q) * x +
          2.5 * x / √(δ₀ * q) + 2 * x / (δ₀ * q) * MinorArcs.L (δ₀ * q) q +
          3.36 * x ^ (5 / 6 : ℝ)) ∧
    (x ^ (1 / 3 : ℝ) / 6 < q →
      ‖Helfgott.S Helfgott.eta2 x α‖ ≤
        0.276 * x ^ (5 / 6 : ℝ) * Real.log x ^ (3 / 2 : ℝ) + 1234 * x ^ (2 / 3 : ℝ) * Real.log x)

/-- [H, Theorem 3.1.1] with the three constants `0.5`, `2.5`, `3.36` of the first case (3.2) replaced
by parameters `c₁`, `c₂`, `c₃`; everything else (hypotheses, `δ₀`, `R`, `L`, the second case) is as
printed. -/
def thm_3_1_1_with (c₁ c₂ c₃ : ℝ) : Prop :=
  ∀ (x α δ : ℝ) (a : ℤ) (q : ℕ), thm_3_1_1_hyp x α δ a q →
    let δ₀ : ℝ := max 2 (|δ| / 4)
    ((q : ℝ) ≤ x ^ (1 / 3 : ℝ) / 6 →
      ‖Helfgott.S Helfgott.eta2 x α‖ ≤
        (MinorArcs.R x (δ₀ * q) * Real.log (δ₀ * q) + c₁) / √(δ₀ * Nat.totient q) * x +
          c₂ * x / √(δ₀ * q) + 2 * x / (δ₀ * q) * MinorArcs.L (δ₀ * q) q +
          c₃ * x ^ (5 / 6 : ℝ)) ∧
    (x ^ (1 / 3 : ℝ) / 6 < q →
      ‖Helfgott.S Helfgott.eta2 x α‖ ≤
        0.276 * x ^ (5 / 6 : ℝ) * Real.log x ^ (3 / 2 : ℝ) + 1234 * x ^ (2 / 3 : ℝ) * Real.log x)

/-- The printed statement is the instance `(c₁, c₂, c₃) = (0.5, 2.5, 3.36)`. -/
theorem thm_3_1_1_eq_with : thm_3_1_1 = thm_3_1_1_with 0.5 2.5 3.36 := rfl

/-- Larger first-case constants give a weaker statement: the constants multiply
`x/√(δ₀φ(q)) ≥ 0`, `x/√(δ₀q) ≥ 0` and `x^{5/6} ≥ 0`. -/
theorem thm_3_1_1_with_mono {c₁ c₂ c₃ c₁' c₂' c₃' : ℝ} (h₁ : c₁ ≤ c₁') (h₂ : c₂ ≤ c₂')
    (h₃ : c₃ ≤ c₃') : thm_3_1_1_with c₁ c₂ c₃ → thm_3_1_1_with c₁' c₂' c₃' := by
  intro H x α δ a q hyp
  have hx : 0 ≤ x := by
    have h := hyp.1
    norm_num at h
    linarith
  obtain ⟨H₁, H₂⟩ := H x α δ a q hyp
  refine ⟨fun hq => (H₁ hq).trans ?_, H₂⟩
  gcongr

/-- **The formalization proves exactly [H, Theorem 3.1.1] with the constants `(0.8764, 2.526, 3.8)`.**
Under the inputs `PlattGRH`, `RamareMoebius`, `thm_3_1_1_with 0.8764 2.526 3.8` is
equivalent to the statement of `TernaryGoldbach.MinorArcs.theorem_3_1_1`: the two differ only in the
packaging of the hypotheses (`Approx2` lists `1 ≤ q`, `IsCoprime a q`, the congruence,
`|δ/x| ≤ 1/(qQ)`, `q ≤ Q` in another order, with `IsCoprime a q` for `gcd(a, q) = 1`; the literal
`216e18` is `2.16 * 10 ^ 20`). -/
theorem thm_3_1_1_with_formal_iff :
    (Fact PlattGRH → Fact RamareMoebius → thm_3_1_1_with 0.8764 2.526 3.8) ↔
      type_of% @TernaryGoldbach.MinorArcs.theorem_3_1_1 := by
  constructor
  · rintro H h₁ h₂ α x δ a q hx ⟨hq, hcop, hα, hδ, hqQ⟩
    exact H h₁ h₂ x α δ a q
      ⟨by norm_num at hx ⊢; linarith, hq, hα, hqQ, Int.isCoprime_iff_gcd_eq_one.mp hcop, hδ⟩
  · rintro H h₁ h₂ x α δ a q ⟨hx, hq, hα, hqQ, hgcd, hδ⟩
    exact @H h₁ h₂ α x δ a q (by norm_num at hx ⊢; linarith)
      ⟨hq, Int.isCoprime_iff_gcd_eq_one.mpr hgcd, hα, hδ, hqQ⟩

/-- The formalization's [H, Theorem 3.1.1]: the printed statement with the first-case constants
`0.5, 2.5, 3.36` weakened to `0.8764, 2.526, 3.8`; in particular the second case
(`q > x^{1/3}/6`, constants `0.276`, `1234`) is proved as printed. -/
theorem thm_3_1_1_with_formal [Fact PlattGRH] [Fact RamareMoebius] :
    thm_3_1_1_with 0.8764 2.526 3.8 :=
  thm_3_1_1_with_formal_iff.mpr @TernaryGoldbach.MinorArcs.theorem_3_1_1 inferInstance
    inferInstance

/-- **[H, Theorem 3.1.1] implies the formal `TernaryGoldbach.MinorArcs.theorem_3_1_1`** (the formal
first-case bound is weaker: `0.8764 ≥ 0.5`, `2.526 ≥ 2.5`, `3.8 ≥ 3.36`; the hypotheses and the second
case are the same). -/
theorem thm_3_1_1_implies_formal :
    thm_3_1_1 → type_of% @TernaryGoldbach.MinorArcs.theorem_3_1_1 := by
  intro h
  have h' : thm_3_1_1_with 0.5 2.5 3.36 := h
  apply thm_3_1_1_with_formal_iff.mp
  intro _ _
  exact thm_3_1_1_with_mono (by norm_num) (by norm_num) (by norm_num) h'

/-! ### Transcription checks -/

/-- `MinorArcs.R x t` is [H, (3.3)]'s
`R_{x,t} = 0.27125 log(1 + log 4t / (2 log (9 x^{1/3}/(2.004 t)))) + 0.41415`. -/
theorem thm_3_1_1_R_eq (x t : ℝ) :
    MinorArcs.R x t =
      0.27125 * Real.log (1 + Real.log (4 * t) / (2 * Real.log (9 * x ^ (1 / 3 : ℝ) / (2.004 * t)))) +
        0.41415 :=
  rfl

/-- `MinorArcs.L t q` is [H, (3.3)]'s `L_{x,t,q} = (q/φ(q)) (13/4 log t + 7.82) + 13.66 log t + 37.55`
(a real quotient `q/φ(q)`; no dependence on `x`). -/
theorem thm_3_1_1_L_eq (t : ℝ) (q : ℕ) :
    MinorArcs.L t q =
      (q : ℝ) / (Nat.totient q : ℝ) * (13 / 4 * Real.log t + 7.82) + 13.66 * Real.log t + 37.55 :=
  rfl

/-- `Helfgott.eta2` is [H, (3.4)]'s `η₂(t) = 4 max(log 2 - |log 2t|, 0)` on `t > 0`. -/
theorem thm_3_1_1_eta2_eq {t : ℝ} (ht : 0 < t) :
    Helfgott.eta2 t = 4 * max (Real.log 2 - |Real.log (2 * t)|) 0 :=
  ite_eq_left ht

/-- `Helfgott.S Helfgott.eta2 x α` is [H, (3.1)]'s `S_η(α, x) = ∑ₙ Λ(n) e(αn) η(n/x)` for `η = η₂`:
for `x > 0` the terms with `n > x` vanish, and it is the finite sum over `1 ≤ n ≤ x`. -/
theorem thm_3_1_1_S_eq {x : ℝ} (hx : 0 < x) (α : ℝ) :
    Helfgott.S Helfgott.eta2 x α =
      ∑ n ∈ Finset.Icc 1 ⌊x⌋₊,
        (ArithmeticFunction.vonMangoldt n : ℂ) * e (α * n) * (Helfgott.eta2 (n / x) : ℂ) := by
  rw [MinorArcs.S_eq_sum hx ⌊x⌋₊ le_rfl]
  refine Finset.sum_congr rfl fun n _ => ?_
  simp only [MinorArcs.wt]
  ring

/-- **Non-vacuity.** The hypotheses of `thm_3_1_1` can be met in each of its two cases. At
`x = x₀ = 2.16·10²⁰` (so `x^{1/3} = 6·10⁶`, `x^{1/3}/6 = 10⁶`, `Q = 2.7·10¹³`):
`(α, δ, a, q) = (1/(2·10⁵), 0, 1, 10⁵)` is in the first case and `(1/(2·10⁷), 0, 1, 10⁷)` in the
second. (There the two bounds are about `0.040 x` and `0.046 x`, far below the trivial size `≈ x` of
`|S_η(α, x)|`, since `∫ η₂ = 1`: both conclusions are genuine constraints.) -/
theorem thm_3_1_1_hyp_satisfiable :
    (thm_3_1_1_hyp (2.16 * 10 ^ 20) (1 / (2 * 10 ^ 5)) 0 1 (10 ^ 5) ∧
        ((10 ^ 5 : ℕ) : ℝ) ≤ (2.16 * 10 ^ 20 : ℝ) ^ (1 / 3 : ℝ) / 6) ∧
      (thm_3_1_1_hyp (2.16 * 10 ^ 20) (1 / (2 * 10 ^ 7)) 0 1 (10 ^ 7) ∧
        (2.16 * 10 ^ 20 : ℝ) ^ (1 / 3 : ℝ) / 6 < ((10 ^ 7 : ℕ) : ℝ)) := by
  have hT : (2.16 * 10 ^ 20 : ℝ) ^ (1 / 3 : ℝ) = 6 * 10 ^ 6 := by
    rw [show (2.16 * 10 ^ 20 : ℝ) = (6 * 10 ^ 6) ^ (3 : ℕ) by norm_num,
      show (1 / 3 : ℝ) = ((3 : ℕ) : ℝ)⁻¹ by norm_num]
    exact Real.pow_rpow_inv_natCast (by norm_num) (by norm_num)
  have hQ : (2.16 * 10 ^ 20 : ℝ) ^ (2 / 3 : ℝ) = (6 * 10 ^ 6) ^ 2 := by
    rw [show (2 / 3 : ℝ) = 1 / 3 * ((2 : ℕ) : ℝ) by norm_num, Real.rpow_mul (by norm_num),
      Real.rpow_natCast, hT]
  refine ⟨⟨⟨by norm_num, by norm_num, ⟨0, by norm_num⟩, ?_, by norm_num, ?_⟩, ?_⟩,
    ⟨⟨by norm_num, by norm_num, ⟨0, by norm_num⟩, ?_, by norm_num, ?_⟩, ?_⟩⟩
  all_goals (try rw [hQ]); (try rw [hT]); norm_num

end Companion.Book
