import TernaryGoldbach

/-!
# [H, Proposition 11.2.3]: from `η₂` to `η_* = η₂ *_M φ` — the printed first case is false

## What [H] states

H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, Proposition 11.2.3
(`prop:gorsh`), §11.2, p. 223, <https://arxiv.org/pdf/1501.05438v2#page=233>. (It is Prop. 4.5,
p. 28, of the preprint arXiv:1312.7748v2, with `3.2` for `3.36`; the defect below is already there.)

Let `x ≥ K x₀`, `x₀ = 2.16·10²⁰`, `K ≥ 1`, and let `S_η(α, x)` be as in (10.1). Let
`η_* = η₂ *_M φ`, where `η₂` is as in (11.10) and `φ : [0, ∞) → [0, ∞)` is continuous and in `L¹`.
Let `2α = a/q + δ/x`, `q ≤ Q`, `gcd(a, q) = 1`, `|δ/x| ≤ 1/qQ`, where `Q = (3/4) x^{2/3}`.
* If `q ≤ (x/K)^{1/3}/6`, then (11.18) `S_{η_*}(α, x) ≤ g_{x,φ}(max(1, |δ|/8) q) · |φ|₁ x`, where
  (11.19) `g_{x,φ}(r) = ((R_{x,K,φ,2r} log 2r + 0.5) √Ϝ(r) + 2.5)/√(2r) + L_{2r}/r + 3.36 K^{1/6} x^{-1/6}`,
  `R_{x,K,φ,t} = R_{x,t} + (R_{x/K,t} − R_{x,t}) (C_{φ,2,K}/|φ|₁)/log K`, `R_{x,t}` and `L_t` are as in
  (11.13), and (11.20) `C_{φ,2,K} = −∫_{1/K}^1 φ(w) log w dw`.
* If `q > (x/K)^{1/3}/6`, then `|S_{η_*}(α, x)| ≤ h_φ(x/K) · |φ|₁ x`, where (11.21)
  `h_φ(x) = h(x) + C_{φ,0,K}/|φ|₁`, `C_{φ,0,K} = 1.04488 ∫_0^{1/K} |φ(w)| dw`, and `h` is (11.15).

`prop_11_2_3` below is this statement (both cases).

## The printed first case is false (certified here)

[H]'s proof writes `S_{η_*}(α, x) = ∫₀^∞ S_{η₂}(α, wx) φ(w) dw/w` (11.9), splits at `w = 1/K`, and
bounds the part `w < 1/K` trivially by `1.04488 x ∫_0^{1/K} φ` (Cor. C.1.3). The second case keeps
this term (it is `C_{φ,0,K}` in (11.21)); the first case (11.18) drops it. Since `φ` is an arbitrary
continuous `L¹` function, it may put its mass at tiny `w`, where `S_{η₂}(α, wx)` is a sum over a few
small primes of size `≍ wx`, while `g_{x,φ}(r)` is small for large `r`.

**Counterexample** (`prop_11_2_3_counterexample`): `x = 10³⁰`, `K = 8`, `a = 1`, `q = 8·10⁸`,
`δ = 0`, `α = 1/(2q)`, and `φ(w) = max(0, (xw − 5/2)(3 − xw))` (`prop_11_2_3_bump`), a continuous bump
supported on `[5/(2x), 3/x]` with `|φ|₁ = 1/(48x)`. All hypotheses of the first case hold:
`q ≤ (x/K)^{1/3}/6 = 8.33·10⁸`. Then `η_*(n/x) = 0` for `n ≥ 3` and `Λ(1) = 0`, so
`S_{η_*}(α, x) = log 2 · η_*(2/x) · e(2α)`, and `|S_{η_*}(α, x)| ≥ log 2 · (4/15) |φ|₁ x ≈ 0.185 |φ|₁ x`
(the true value is `≈ 0.319 |φ|₁ x`). On the other side `C_{φ,2,K} = 0` (`φ` vanishes on `[1/8, 1]`),
so `R_{x,K,φ,t} = R_{x,t}`, and `g_{x,φ}(r) ≤ 1/100` at `r = q` (the true value is `≈ 0.00122`).
The printed bound is exceeded by a factor `≈ 262`.

The refutation goes through `prop_11_2_3_first_case_nondegenerate`: the first case restricted to
`q ≥ 3` (the hypothesis of (11.11)), `K > 1`, `|φ|₁ > 0` and `670 ≤ r ≤ (x/K)^{1/3}/6` (the range of
Lemma 11.2.4). On such data every quantity in (11.18)–(11.20) is a genuine real number (every
logarithm has an argument `> 1`, `Ϝ(r) > 0`, no division by zero), so no junk value of Lean
(`x/0 = 0`, `log 0 = 0`, `√` of a negative number `= 0`) is involved. This restriction is implied by
the printed statement (`prop_11_2_3_imp_first_case_nondegenerate`) and is already false
(`prop_11_2_3_first_case_nondegenerate_false`), so the counterexample is not an artifact of the
transcription.

Two further checks:
* `prop_11_2_3_counterexample_re`: even the real part of `S_{η_*}(α, x)` exceeds the bound (since
  `e(2α) = e(1/q) ≈ 1`). (11.18) is printed without absolute value bars, and `S` is complex; the
  definition reads it with `|·|`, as in the second case and in [H, (13.14)–(13.15)], but the
  refutation does not depend on that reading.
* `prop_11_2_3_counterexample_corrected`: with the dropped term restored, i.e.
  `|S_{η_*}(α, x)| ≤ (g_{x,φ}(r) + C_{φ,0,K}/|φ|₁) |φ|₁ x` (what [H]'s proof gives, and what [H] uses
  downstream: (13.17) adds `C_{φ,3}(K) = C_{φ,0,K}/|φ|₁` in all three cases), the bound holds at the
  counterexample. So the failure is exactly the omitted term.

We do not know whether the second case, as printed, is true; it is not refuted here (with mass at
`w < 1/K` it is covered by the `C_{φ,0,K}` term, and at `w ≥ 1/K` all scales are `≥ x₀`).

## The δ-scaling erratum (Helfgott's own; not used here)

[H]'s proof applies (11.11) at scale `wx` with the same `r = max(1, |δ|/8) q`. At scale `wx`, though,
`2α = a/q + (wδ)/(wx)`: for `w < 1` the parameter is `r_w = max(1, w|δ|/8) q ≤ r`, which gives the
weaker bound `g_{wx}(r_w)`, and for `w > 1` the hypothesis `|δ/x| ≤ 1/(q Q_{wx})` of Theorem 3.1.1
can fail (`Q_{wx} > Q_x`). Helfgott reported this himself (see the repository's `NOTES.md`,
"Ch. 11: Prop 11.2.3 erratum"). It invalidates the argument for both cases but is not known to make
the statement false: for the `φ` of the application, the numerics recorded there
(`r₀ ≤ r ≤ r₁`, `y ∈ [10²⁵, 10¹⁰⁰]`) indicate that the first-case bound survives the correct
scaling. The refutation above does not use this erratum.

## What the formalization proves

The repository proves two corrected variants, both for the fixed `φ(t) = t² e^{−t²/2}` and
`η_*(t) = (η₂ *_M φ)(κt)`, `κ = 49`, and both conditional on the trusted inputs of Theorem 3.1.1
(`[Fact PlattGRH] [Fact RamareMoebius]`). Their `S_{η_*}(α, x)` is [H]'s
`S_{η₂ *_M φ}(α, y)` at the scale `y = x/κ` (`prop_11_2_3_S_etaStar`), and this `φ` satisfies [H]'s
hypotheses (`prop_11_2_3_phi_admissible`).
* `TernaryGoldbach.MinorArcs.prop_11_2_3` (`MinorArcs/Prop1123.lean`): first case only. Given
  `2α = a/q + δ/y` as in Theorem 3.1.1 at scale `y`, `0 < w₀ ≤ 1 ≤ w₁`, `w₀y ≥ 2.16·10²⁰`,
  `q ≤ (w₀y)^{1/3}/6`, `w₀ r ≥ 670`, `|δ/y| ≤ 1/(q Q_{w₁y})`, and any `G` with
  `G(w) ≥ g_{wy}(min(1, w) r)` on `[w₀, w₁]` and `Gφ` integrable there, it proves
  `|S_{η_*}(α, x)| ≤ y (∫_{w₀}^{w₁} Gφ + 17 (∫_0^{w₀} φ + ∫_{w₁}^∞ φ))`. The factor `min(1, w)`
  repairs the δ-scaling erratum.
* `TernaryGoldbach.MinorArcs.prop_11_2_3'` (`MinorArcs/Prop1123b.lean`): for `α ∉ 𝔐_{8,n}(y)`,
  `0 < w₀ ≤ 1 ≤ w₁`, `w₀y ≥ 2.16·10²⁰`, `w₀ n ≥ 670`, the same conclusion for any `G` that dominates
  both cases of Theorem 3.1.1 at scale `wy` with parameter `min(1, w) n`. Its proof takes a fresh
  Dirichlet approximation at every scale `wy`, which also avoids the δ-scaling erratum.

Neither is in the dependency cone of the main theorem. The minor-arc total uses
`TernaryGoldbach.MinorArcs.norm_S_etaStar_le_ghat` (`MinorArcs/LinftyLevels.lean`), which redoes the
argument of `prop_11_2_3'` with `w₁ = ∞` through its pointwise step `norm_S_eta2_le_of_not_mem`.

## Relation: refuted

`prop_11_2_3_false : ¬ prop_11_2_3`, through the non-degenerate sub-claim
(`prop_11_2_3_imp_first_case_nondegenerate`, `prop_11_2_3_first_case_nondegenerate_false`). An
implication `prop_11_2_3 → type_of% @…` would hold vacuously and certify nothing, so none is stated.

The Lean theorems are variants. Even against [H]'s statement with the `C_{φ,0,K}` term restored, they
are incomparable: neither can be derived from the other without new analysis or numerics.
* `φ`: [H] quantifies over all continuous `L¹` functions, Lean fixes `φ(t) = t² e^{−t²/2}` (and the
  scale `x/κ`), so the Lean theorems say nothing about other `φ`.
* The shape of the bound: [H] has the closed form `g_{x,φ}(r) |φ|₁ x`, obtained from a convexity
  bound for `R_{wx,t}` (Lemma 11.2.2); Lean has `∫_{w₀}^{w₁} G φ` for any majorant `G` of
  `g_{wy}(min(1, w) r)`, plus `17 (∫_0^{w₀} φ + ∫_{w₁}^∞ φ)`.
* Constants: Lean's `g` (`gx`) has the corrected Theorem 3.1.1 constants `0.8764, 2.511, 3.8` for
  [H]'s `0.5, 2.5, 3.36`, and its trivial bound is `17 z` (Chebyshev) for [H]'s `1.04488 z`
  (Cor. C.1.3).
* Hypotheses: Lean adds `w₀ r ≥ 670` (to use the monotonicity of `g`) and `|δ/y| ≤ 1/(q Q_{w₁y})`
  (Theorem 3.1.1 at the top scale); [H]'s `K` corresponds to `1/w₀`.
For the fixed `φ`, neither bound dominates the other termwise: [H]'s closed form uses `R_{y,t}` for
every `w ≥ 1`, while Lean's integrand has the smaller `R_{wy,t}` but the larger constant `0.8764`.
-/

open Real Set MeasureTheory
open scoped ArithmeticFunction.vonMangoldt

namespace Companion.Book

open TernaryGoldbach.Helfgott (eta2 S mellinConv)
open TernaryGoldbach.MinorArcs (R Lg Fr hfun)

/-! ## [H]'s objects that the repository does not define -/

/-- `|φ|₁ = ∫₀^∞ |φ(w)| dw`, the `L¹` norm of `φ` on `[0, ∞)`. -/
noncomputable def prop_11_2_3_norm1 (φ : ℝ → ℝ) : ℝ := ∫ w in Ioi (0:ℝ), |φ w|

/-- `C_{φ,0,K} = 1.04488 ∫_0^{1/K} |φ(w)| dw` [H, (11.21)]. -/
noncomputable def prop_11_2_3_C0 (φ : ℝ → ℝ) (K : ℝ) : ℝ :=
  1.04488 * ∫ w in (0:ℝ)..1 / K, |φ w|

/-- `C_{φ,2,K} = −∫_{1/K}^1 φ(w) log w dw` [H, (11.20)]. -/
noncomputable def prop_11_2_3_C2 (φ : ℝ → ℝ) (K : ℝ) : ℝ :=
  -∫ w in 1 / K..1, φ w * Real.log w

/-- `R_{x,K,φ,t} = R_{x,t} + (R_{x/K,t} − R_{x,t}) (C_{φ,2,K}/|φ|₁)/log K` [H, (11.19)], with the
repository's `R` for [H]'s `R_{x,t}` (11.13). -/
noncomputable def prop_11_2_3_RK (x K : ℝ) (φ : ℝ → ℝ) (t : ℝ) : ℝ :=
  R x t + (R (x / K) t - R x t) * (prop_11_2_3_C2 φ K / prop_11_2_3_norm1 φ) / Real.log K

/-- `g_{x,φ}(r) = ((R_{x,K,φ,2r} log 2r + 0.5) √Ϝ(r) + 2.5)/√(2r) + L_{2r}/r + 3.36 K^{1/6} x^{-1/6}`
[H, (11.19)], with [H]'s constants `0.5, 2.5, 3.36` (the repository's `gx` has the corrected
`0.8764, 2.511, 3.8` and is not reused). -/
noncomputable def prop_11_2_3_g (x K : ℝ) (φ : ℝ → ℝ) (r : ℝ) : ℝ :=
  ((prop_11_2_3_RK x K φ (2 * r) * Real.log (2 * r) + 0.5) * √(Fr r) + 2.5) / √(2 * r) +
    Lg (2 * r) / r + 3.36 * K ^ (1 / 6 : ℝ) * x ^ (-1 / 6 : ℝ)

/-- `h_φ(x) = h(x) + C_{φ,0,K}/|φ|₁` [H, (11.21)], with the repository's `hfun` for [H]'s
`h(x) = 0.276 x^{-1/6} (log x)^{3/2} + 1234 x^{-1/3} log x` (11.15). -/
noncomputable def prop_11_2_3_hφ (K : ℝ) (φ : ℝ → ℝ) (x : ℝ) : ℝ :=
  hfun x + prop_11_2_3_C0 φ K / prop_11_2_3_norm1 φ

/-- **[H, Proposition 11.2.3]**, p. 223, as printed (both cases).

Transcription choices:
* `x, K` are real, with `1 ≤ K` and `K * 2.16e20 ≤ x` (`x ≥ K x₀`, `x₀ = 2.16·10²⁰`).
* `φ : [0, ∞) → [0, ∞)` continuous and in `L¹` becomes `φ : ℝ → ℝ` with `ContinuousOn φ (Ici 0)`,
  `∀ w ≥ 0, 0 ≤ φ w` and `IntegrableOn φ (Ici 0)`. The values of `φ` on `(−∞, 0)` never enter: the
  Mellin convolution at `t ≥ 0` evaluates `φ` at `t/w ≥ 0`, and all integrals are over subsets of
  `[0, ∞)`.
* `η_* = η₂ *_M φ` is `mellinConv eta2 φ`. The repository's `mellinConv f g t = ∫_{r>0} f(r) g(t/r) dr/r`
  is [H, (2.7)], and its `eta2 t = 4 max(log 2 − |log 2t|, 0)` (for `t > 0`, and `0` for `t ≤ 0`) is
  (11.10).
* `S_η(α, x)` is the repository's `S η x α = ∑' n, Λ(n) η(n/x) e(nα)`, which is (10.1); `α ∈ ℝ/ℤ` is
  represented by a real number (`e(nα)` is `1`-periodic in `α`). For `φ ∈ L¹` the series converges
  absolutely (`Σ Λ(n) η_*(n/x) = ∫ S_{η₂}(0, wx) φ(w) dw/w ≤ 1.04488 |φ|₁ x` by Tonelli and
  Cor. C.1.3), so the `tsum` is the genuine sum.
* `2α = a/q + δ/x` holds in `ℝ/ℤ`, so it becomes `∃ k : ℤ, 2 * α = a / q + δ / x + k`, with `a : ℤ`,
  `δ : ℝ` and `q : ℕ`, `0 < q` (implicit in [H]: `q` is a denominator). `gcd(a, q) = 1` is
  `Int.gcd a q = 1`; `Q = (3/4) x^{2/3}` is written out (`x ^ (2 / 3 : ℝ)`), and `1/qQ` means `1/(qQ)`.
* First case: the hypothesis `q ≤ (x/K)^{1/3}/6` and the conclusion
  `‖S_{η_*}(α, x)‖ ≤ g_{x,φ}(max(1, |δ|/8) q) · |φ|₁ · x`. (11.18) is printed without `|·|`, though
  `S` is complex; we read it as in the second case and as [H] uses it in (13.14)–(13.15). The
  refutation does not depend on this (`prop_11_2_3_counterexample_re`).
* `g_{x,φ}`, `R_{x,K,φ,t}`, `C_{φ,2,K}` are `prop_11_2_3_g`, `prop_11_2_3_RK`, `prop_11_2_3_C2`, copied
  from (11.19)–(11.20). Inside, the repository's `R x t` is `R_{x,t}`, its `Lg t` is `L_t` and its
  `Fr r` is `Ϝ(r) = e^γ log log r + 2.50637/log log r` ((11.13) and (C.19); we checked all three
  against [H]). `|φ|₁` is `prop_11_2_3_norm1 φ = ∫_{(0,∞)} |φ|`.
* Second case: the hypothesis `(x/K)^{1/3}/6 < q` and the conclusion
  `‖S_{η_*}(α, x)‖ ≤ h_φ(x/K) · |φ|₁ · x`, with `h_φ` and `C_{φ,0,K}` (`prop_11_2_3_hφ`,
  `prop_11_2_3_C0`) copied from (11.21) and `h` the repository's `hfun`, which is (11.15) verbatim.
* Both cases are claimed under the common hypotheses, so they are joined by `∧`.
* Degenerate inputs, where [H]'s right side is undefined and Lean substitutes junk values:
  - `K = 1`: `(R_{x/K,t} − R_{x,t}) (C_{φ,2,K}/|φ|₁)/log K` is `0 · (0/|φ|₁)/0`; Lean gives `0`, so
    `R_{x,1,φ,t} = R_{x,t}`, which is also the limit as `K → 1⁺` (`C_{φ,2,K} = O((log K)²)`).
  - `|φ|₁ = 0`: then `φ = 0` on `[0, ∞)`, `S_{η_*} = 0`, and both bounds read `0 ≤ 0`.
  - `1 ≤ r ≤ e` (possible only when `q ≤ 2`; [H]'s (11.11) assumes `q ≥ 3`): `log log r ≤ 0`, so
    `Ϝ(r)` is undefined or negative and `√Ϝ(r)` is undefined. Lean's conventions can make the bound
    negative there (e.g. `q = 1`, `|δ|` slightly above `8`), so the definition is also false at such
    points, for reasons that are not [H]'s. The refutation avoids them: it refutes the restriction
    `prop_11_2_3_first_case_nondegenerate`, on which no junk value occurs. -/
def prop_11_2_3 : Prop :=
  ∀ x K : ℝ, 1 ≤ K → K * 2.16e20 ≤ x →
  ∀ φ : ℝ → ℝ, ContinuousOn φ (Ici 0) → (∀ w, 0 ≤ w → 0 ≤ φ w) → IntegrableOn φ (Ici 0) →
  ∀ (α δ : ℝ) (a : ℤ) (q : ℕ), 0 < q → (∃ k : ℤ, 2 * α = a / q + δ / x + k) →
    (q : ℝ) ≤ 3 / 4 * x ^ (2 / 3 : ℝ) → Int.gcd a q = 1 →
    |δ / x| ≤ 1 / (q * (3 / 4 * x ^ (2 / 3 : ℝ))) →
    ((q : ℝ) ≤ (x / K) ^ (1 / 3 : ℝ) / 6 →
        ‖S (mellinConv eta2 φ) x α‖ ≤
          prop_11_2_3_g x K φ (max 1 (|δ| / 8) * q) * prop_11_2_3_norm1 φ * x) ∧
    ((x / K) ^ (1 / 3 : ℝ) / 6 < q →
        ‖S (mellinConv eta2 φ) x α‖ ≤ prop_11_2_3_hφ K φ (x / K) * prop_11_2_3_norm1 φ * x)

/-- **The first case of [H, (11.18)] on non-degenerate data** (a sub-claim of `prop_11_2_3`, not
[H]'s statement): the hypotheses of `prop_11_2_3` and `q ≤ (x/K)^{1/3}/6`, strengthened by `K > 1`,
`|φ|₁ > 0`, `q ≥ 3` (as in (11.11)) and `670 ≤ r ≤ (x/K)^{1/3}/6` for `r = max(1, |δ|/8) q` (the range
of Lemma 11.2.4, the one [H] uses in (13.14)–(13.15)).

On such data every quantity in (11.18)–(11.20) is a genuine real number: `log log r ≥ log log 670 > 0`
so `Ϝ(r) > 0`; `2r ≤ (x/K)^{1/3}/3`, so `9x^{1/3}/(2.004·2r)` and `9(x/K)^{1/3}/(2.004·2r)` are
`≥ 13.4`; `log K > 0`; `|φ|₁ > 0`. So Lean's junk values play no role, and refuting this sub-claim
refutes [H]'s printed first case on any reading in which its right side is defined. -/
def prop_11_2_3_first_case_nondegenerate : Prop :=
  ∀ x K : ℝ, 1 < K → K * 2.16e20 ≤ x →
  ∀ φ : ℝ → ℝ, ContinuousOn φ (Ici 0) → (∀ w, 0 ≤ w → 0 ≤ φ w) → IntegrableOn φ (Ici 0) →
    0 < prop_11_2_3_norm1 φ →
  ∀ (α δ : ℝ) (a : ℤ) (q : ℕ), 3 ≤ q → (∃ k : ℤ, 2 * α = a / q + δ / x + k) →
    (q : ℝ) ≤ 3 / 4 * x ^ (2 / 3 : ℝ) → Int.gcd a q = 1 →
    |δ / x| ≤ 1 / (q * (3 / 4 * x ^ (2 / 3 : ℝ))) →
    (q : ℝ) ≤ (x / K) ^ (1 / 3 : ℝ) / 6 →
    670 ≤ max 1 (|δ| / 8) * q → max 1 (|δ| / 8) * q ≤ (x / K) ^ (1 / 3 : ℝ) / 6 →
      ‖S (mellinConv eta2 φ) x α‖ ≤
        prop_11_2_3_g x K φ (max 1 (|δ| / 8) * q) * prop_11_2_3_norm1 φ * x

/-- The printed statement implies its non-degenerate sub-claim (drop the extra hypotheses). -/
theorem prop_11_2_3_imp_first_case_nondegenerate :
    prop_11_2_3 → prop_11_2_3_first_case_nondegenerate := by
  intro h x K hK hx φ hc hn hi _ α δ a q hq hk hQ hgcd hd h1 _ _
  exact (h x K hK.le hx φ hc hn hi α δ a q (by omega) hk hQ hgcd hd).1 h1

/-! ## The test function and `S_{η_*}` for it -/

/-- The test function of the counterexample: `φ(w) = max(0, (Xw − 5/2)(3 − Xw))`, a continuous bump
supported on `[5/(2X), 3/X]`. -/
noncomputable def prop_11_2_3_bump (X w : ℝ) : ℝ := max 0 ((X * w - 5 / 2) * (3 - X * w))

theorem prop_11_2_3_bump_nonneg (X w : ℝ) : 0 ≤ prop_11_2_3_bump X w := le_max_left _ _

theorem prop_11_2_3_bump_continuous (X : ℝ) : Continuous (prop_11_2_3_bump X) := by
  unfold prop_11_2_3_bump
  fun_prop

/-- The bump is supported on `5/2 < Xw < 3`. -/
theorem prop_11_2_3_bump_ne_zero {X w : ℝ} (h : prop_11_2_3_bump X w ≠ 0) :
    5 / 2 < X * w ∧ X * w < 3 := by
  unfold prop_11_2_3_bump at h
  by_contra hc
  apply h
  apply max_eq_left
  rcases not_and_or.mp hc with h1 | h1
  · push Not at h1
    nlinarith [mul_nonneg (sub_nonneg.2 h1) (by linarith : (0:ℝ) ≤ 3 - X * w)]
  · push Not at h1
    nlinarith [mul_nonneg (by linarith : (0:ℝ) ≤ X * w - 5 / 2) (sub_nonneg.2 h1)]

theorem prop_11_2_3_bump_hasCompactSupport {X : ℝ} (hX : 0 < X) :
    HasCompactSupport (prop_11_2_3_bump X) := by
  refine HasCompactSupport.intro (isCompact_Icc (a := 0) (b := 3 / X)) fun w hw => ?_
  by_contra h
  obtain ⟨h1, h2⟩ := prop_11_2_3_bump_ne_zero h
  apply hw
  constructor
  · by_contra h'
    push Not at h'
    nlinarith
  · rw [le_div_iff₀ hX, mul_comm]
    exact h2.le

theorem prop_11_2_3_bump_integrable {X : ℝ} (hX : 0 < X) : Integrable (prop_11_2_3_bump X) :=
  (prop_11_2_3_bump_continuous X).integrable_of_hasCompactSupport
    (prop_11_2_3_bump_hasCompactSupport hX)

theorem prop_11_2_3_norm1_bump (X : ℝ) :
    prop_11_2_3_norm1 (prop_11_2_3_bump X) = ∫ w in Ioi (0:ℝ), prop_11_2_3_bump X w := by
  unfold prop_11_2_3_norm1
  exact setIntegral_congr_fun measurableSet_Ioi fun w _ =>
    abs_of_nonneg (prop_11_2_3_bump_nonneg X w)

theorem prop_11_2_3_integral_bump_pos {X : ℝ} (hX : 0 < X) :
    0 < ∫ w in Ioi (0:ℝ), prop_11_2_3_bump X w := by
  rw [setIntegral_eq_integral_of_forall_compl_eq_zero]
  · refine (prop_11_2_3_bump_continuous X).integral_pos_of_hasCompactSupport_nonneg_nonzero
      (prop_11_2_3_bump_hasCompactSupport hX) (fun w => prop_11_2_3_bump_nonneg X w)
      (x := 11 / (4 * X)) ?_
    unfold prop_11_2_3_bump
    have e : X * (11 / (4 * X)) = 11 / 4 := by field_simp
    rw [e, max_eq_right (by norm_num)]
    norm_num
  · intro w hw
    by_contra h
    obtain ⟨h1, -⟩ := prop_11_2_3_bump_ne_zero h
    apply hw
    show 0 < w
    by_contra h'
    push Not at h'
    nlinarith

theorem prop_11_2_3_mellin_nonneg (φ : ℝ → ℝ) (hφ : ∀ w, 0 ≤ φ w) (t : ℝ) :
    0 ≤ mellinConv eta2 φ t := by
  unfold mellinConv
  refine setIntegral_nonneg measurableSet_Ioi fun r hr => ?_
  have hr0 : (0:ℝ) < r := hr
  exact div_nonneg (mul_nonneg (TernaryGoldbach.Helfgott.eta2_nonneg r) (hφ _)) hr0.le

/-- `η_*(n/X) = 0` for `n ≥ 3`: in `∫ η₂(r) φ(n/(Xr)) dr/r`, either `r ≥ 1` (so `η₂(r) = 0`) or
`n/r > 3` (so `φ(n/(Xr)) = 0`). -/
theorem prop_11_2_3_mellin_bump_eq_zero {X : ℝ} (hX : 0 < X) {n : ℕ} (hn : 3 ≤ n) :
    mellinConv eta2 (prop_11_2_3_bump X) (n / X) = 0 := by
  unfold mellinConv
  have hX0 := hX.ne'
  have key : ∀ r ∈ Ioi (0:ℝ), eta2 r * prop_11_2_3_bump X (n / X / r) / r = 0 := by
    intro r hr
    have hr0 : (0:ℝ) < r := hr
    by_cases h1 : r < 1
    · have hb : prop_11_2_3_bump X (n / X / r) = 0 := by
        by_contra h
        have h3 := (prop_11_2_3_bump_ne_zero h).2
        have e : X * (n / X / r) = n / r := by field_simp
        rw [e, div_lt_iff₀ hr0] at h3
        have : (3:ℝ) ≤ n := by exact_mod_cast hn
        nlinarith
      rw [hb, mul_zero, zero_div]
    · have he : eta2 r = 0 := TernaryGoldbach.Helfgott.eta2_eq_zero fun h => h1 h.2
      rw [he, zero_mul, zero_div]
  rw [setIntegral_congr_fun measurableSet_Ioi key]
  simp

/-- `S_{η_*}(α, X) = log 2 · η_*(2/X) · e(2α)`: only `n = 2` contributes. -/
theorem prop_11_2_3_S_bump {X : ℝ} (hX : 0 < X) (α : ℝ) :
    S (mellinConv eta2 (prop_11_2_3_bump X)) X α =
      ((Real.log 2 * mellinConv eta2 (prop_11_2_3_bump X) (2 / X) : ℝ) : ℂ) *
        TernaryGoldbach.e (2 * α) := by
  unfold S
  rw [tsum_eq_single 2]
  · rw [ArithmeticFunction.vonMangoldt_apply_prime Nat.prime_two, Nat.cast_ofNat]
  · intro n hn
    rcases Nat.lt_or_ge n 3 with h | h
    · interval_cases n
      · simp
      · simp
      · exact absurd rfl hn
    · rw [prop_11_2_3_mellin_bump_eq_zero hX h]
      simp

theorem prop_11_2_3_norm_S_bump {X : ℝ} (hX : 0 < X) (α : ℝ) :
    ‖S (mellinConv eta2 (prop_11_2_3_bump X)) X α‖ =
      Real.log 2 * mellinConv eta2 (prop_11_2_3_bump X) (2 / X) := by
  rw [prop_11_2_3_S_bump hX, norm_mul, Complex.norm_real, Real.norm_eq_abs,
    TernaryGoldbach.norm_e, mul_one, abs_of_nonneg]
  exact mul_nonneg (Real.log_nonneg (by norm_num))
    (prop_11_2_3_mellin_nonneg _ (prop_11_2_3_bump_nonneg X) _)

theorem prop_11_2_3_re_S_bump {X : ℝ} (hX : 0 < X) (α : ℝ) :
    (S (mellinConv eta2 (prop_11_2_3_bump X)) X α).re =
      Real.log 2 * mellinConv eta2 (prop_11_2_3_bump X) (2 / X) * Real.cos (2 * π * (2 * α)) := by
  rw [prop_11_2_3_S_bump hX, Complex.re_ofReal_mul]
  congr 1
  simp [TernaryGoldbach.e, Complex.exp_re]

theorem prop_11_2_3_eta2_ge {s : ℝ} (h1 : 2 / 3 ≤ s) (h2 : s ≤ 4 / 5) : 4 / 5 ≤ eta2 s := by
  have hs : 0 < s := by linarith
  unfold eta2
  rw [ite_eq_left hs]
  have hl0 : 0 ≤ Real.log (2 * s) := Real.log_nonneg (by linarith)
  have hl : Real.log (2 * s) ≤ Real.log 2 - 1 / 5 := by
    rw [Real.log_mul (by norm_num) hs.ne']
    have := Real.log_le_sub_one_of_pos hs
    linarith
  rw [abs_of_nonneg hl0]
  have : 1 / 5 ≤ max (Real.log 2 - Real.log (2 * s)) 0 := le_max_of_le_left (by linarith)
  linarith

/-- The integrand of `η_*(2/X) = ∫_{w>0} η₂(2/(Xw)) φ(w) dw/w` is at most `(6X/5) φ(w)`. -/
theorem prop_11_2_3_bump_integrand_le {X w : ℝ} (hw : 0 < w) :
    eta2 (2 / X / w) * prop_11_2_3_bump X w / w ≤ 6 * X / 5 * prop_11_2_3_bump X w := by
  by_cases h : prop_11_2_3_bump X w = 0
  · rw [h]; simp
  · obtain ⟨h1, h2⟩ := prop_11_2_3_bump_ne_zero h
    have hφ0 : 0 ≤ prop_11_2_3_bump X w := prop_11_2_3_bump_nonneg X w
    have hw' : 1 / w ≤ 2 * X / 5 := by rw [div_le_iff₀ hw]; linarith
    calc eta2 (2 / X / w) * prop_11_2_3_bump X w / w
        = eta2 (2 / X / w) * prop_11_2_3_bump X w * (1 / w) := by ring
      _ ≤ 3 * prop_11_2_3_bump X w * (2 * X / 5) :=
          mul_le_mul (mul_le_mul_of_nonneg_right (TernaryGoldbach.Helfgott.eta2_le _) hφ0) hw'
            (by positivity) (by positivity)
      _ = 6 * X / 5 * prop_11_2_3_bump X w := by ring

theorem prop_11_2_3_bump_integrand_integrable {X : ℝ} (hX : 0 < X) :
    IntegrableOn (fun w : ℝ => eta2 (2 / X / w) * prop_11_2_3_bump X w / w) (Ioi 0) := by
  have hmeas : Measurable fun w : ℝ => eta2 (2 / X / w) * prop_11_2_3_bump X w / w :=
    ((TernaryGoldbach.Helfgott.continuous_eta2.measurable.comp
      (measurable_const.div measurable_id)).mul
        (prop_11_2_3_bump_continuous X).measurable).div measurable_id
  refine Integrable.mono' (((prop_11_2_3_bump_integrable hX).const_mul (6 * X / 5)).integrableOn)
    hmeas.aestronglyMeasurable ?_
  refine (ae_restrict_iff' measurableSet_Ioi).2 (Filter.Eventually.of_forall fun w hw => ?_)
  have hw0 : (0:ℝ) < w := hw
  rw [Real.norm_eq_abs, abs_of_nonneg (div_nonneg (mul_nonneg
    (TernaryGoldbach.Helfgott.eta2_nonneg _) (prop_11_2_3_bump_nonneg X w)) hw0.le)]
  exact prop_11_2_3_bump_integrand_le hw0

/-- `η_*(2/X) ≥ (4X/15) |φ|₁`: on the support `5/2 < Xw < 3`, `η₂(2/(Xw)) ≥ 4/5` and `1/w > X/3`. -/
theorem prop_11_2_3_mellin_bump_ge {X : ℝ} (hX : 0 < X) :
    4 * X / 15 * ∫ w in Ioi (0:ℝ), prop_11_2_3_bump X w ≤
      mellinConv eta2 (prop_11_2_3_bump X) (2 / X) := by
  rw [TernaryGoldbach.MinorArcs.mellinConv_eq_swap _ _ (div_pos two_pos hX),
    ← integral_const_mul]
  have hpt : ∀ w ∈ Ioi (0:ℝ), 4 * X / 15 * prop_11_2_3_bump X w ≤
      eta2 (2 / X / w) * prop_11_2_3_bump X w / w := by
    intro w hw
    have hw0 : (0:ℝ) < w := hw
    by_cases h : prop_11_2_3_bump X w = 0
    · rw [h]; simp
    · obtain ⟨h1, h2⟩ := prop_11_2_3_bump_ne_zero h
      have hXw : 0 < X * w := by linarith
      have hs1 : 2 / 3 ≤ 2 / X / w := by
        rw [div_div, le_div_iff₀ hXw]; linarith
      have hs2 : 2 / X / w ≤ 4 / 5 := by
        rw [div_div, div_le_iff₀ hXw]; linarith
      have he := prop_11_2_3_eta2_ge hs1 hs2
      have hφ0 : 0 ≤ prop_11_2_3_bump X w := prop_11_2_3_bump_nonneg X w
      have hw' : X / 3 ≤ 1 / w := by rw [le_div_iff₀ hw0]; linarith
      calc 4 * X / 15 * prop_11_2_3_bump X w = 4 / 5 * prop_11_2_3_bump X w * (X / 3) := by ring
        _ ≤ eta2 (2 / X / w) * prop_11_2_3_bump X w * (1 / w) :=
            mul_le_mul (mul_le_mul_of_nonneg_right he hφ0) hw' (by linarith)
              (mul_nonneg (TernaryGoldbach.Helfgott.eta2_nonneg _) hφ0)
        _ = eta2 (2 / X / w) * prop_11_2_3_bump X w / w := by ring
  exact setIntegral_mono_on (((prop_11_2_3_bump_integrable hX).const_mul _).integrableOn)
    (prop_11_2_3_bump_integrand_integrable hX) measurableSet_Ioi hpt

/-- `η_*(2/X) ≤ (6X/5) |φ|₁`. -/
theorem prop_11_2_3_mellin_bump_le {X : ℝ} (hX : 0 < X) :
    mellinConv eta2 (prop_11_2_3_bump X) (2 / X) ≤
      6 * X / 5 * ∫ w in Ioi (0:ℝ), prop_11_2_3_bump X w := by
  rw [TernaryGoldbach.MinorArcs.mellinConv_eq_swap _ _ (div_pos two_pos hX),
    ← integral_const_mul]
  exact setIntegral_mono_on (prop_11_2_3_bump_integrand_integrable hX)
    (((prop_11_2_3_bump_integrable hX).const_mul _).integrableOn) measurableSet_Ioi
    fun w hw => prop_11_2_3_bump_integrand_le hw

/-! ## Numerics at `x = 10³⁰`, `K = 8`, `r = q = 8·10⁸` -/

theorem prop_11_2_3_log_le {y : ℝ} (k : ℕ) (hy : 0 < y) (h : y ≤ 2.7182818283 ^ k) :
    Real.log y ≤ k := by
  rw [Real.log_le_iff_le_exp hy]
  have e : Real.exp k = Real.exp 1 ^ k := by rw [← Real.exp_nat_mul, mul_one]
  rw [e]
  exact h.trans (pow_le_pow_left₀ (by norm_num) Real.exp_one_gt_d9.le k)

theorem prop_11_2_3_le_log {y : ℝ} (k : ℕ) (h : 2.7182818286 ^ k ≤ y) :
    (k : ℝ) ≤ Real.log y := by
  have hy : 0 < y := lt_of_lt_of_le (by positivity) h
  rw [Real.le_log_iff_exp_le hy]
  have e : Real.exp k = Real.exp 1 ^ k := by rw [← Real.exp_nat_mul, mul_one]
  rw [e]
  exact (pow_le_pow_left₀ (Real.exp_pos 1).le Real.exp_one_lt_d9.le k).trans h

theorem prop_11_2_3_rpow_third : (1e30 : ℝ) ^ (1 / 3 : ℝ) = 1e10 := by
  rw [show (1e30 : ℝ) = (1e10 : ℝ) ^ (3 : ℕ) by norm_num,
    show (1 / 3 : ℝ) = ((3 : ℕ) : ℝ)⁻¹ by norm_num,
    Real.pow_rpow_inv_natCast (by norm_num) (by norm_num)]

theorem prop_11_2_3_rpow_two_thirds : (1e30 : ℝ) ^ (2 / 3 : ℝ) = 1e20 := by
  rw [show (1e30 : ℝ) = (1e10 : ℝ) ^ ((3 : ℕ) : ℝ) by norm_num, ← Real.rpow_mul (by norm_num)]
  norm_num

theorem prop_11_2_3_rpow_neg_sixth : (1e30 : ℝ) ^ (-1 / 6 : ℝ) = 1e-5 := by
  rw [show (1e30 : ℝ) = (1e5 : ℝ) ^ ((6 : ℕ) : ℝ) by norm_num, ← Real.rpow_mul (by norm_num)]
  norm_num

theorem prop_11_2_3_rpow_third_div : (1e30 / 8 : ℝ) ^ (1 / 3 : ℝ) = 5e9 := by
  rw [show (1e30 / 8 : ℝ) = (5e9 : ℝ) ^ (3 : ℕ) by norm_num,
    show (1 / 3 : ℝ) = ((3 : ℕ) : ℝ)⁻¹ by norm_num,
    Real.pow_rpow_inv_natCast (by norm_num) (by norm_num)]

theorem prop_11_2_3_eight_rpow : (8 : ℝ) ^ (1 / 6 : ℝ) ≤ 2 := by
  calc (8 : ℝ) ^ (1 / 6 : ℝ) ≤ ((2 : ℝ) ^ (6 : ℕ)) ^ (1 / 6 : ℝ) :=
        Real.rpow_le_rpow (by norm_num) (by norm_num) (by norm_num)
    _ = 2 := by
        rw [show (1 / 6 : ℝ) = ((6 : ℕ) : ℝ)⁻¹ by norm_num,
          Real.pow_rpow_inv_natCast (by norm_num) (by norm_num)]

/-- `R_{x,t}` at `x = 10³⁰`, `t = 2r = 1.6·10⁹`: `0 ≤ R_{x,t} ≤ 0.95665` (true value `≈ 0.815`).
Here `x^{1/3} = 10¹⁰`, `log 4t ≤ 23`, `log(9x^{1/3}/(2.004t)) ≥ 3`. -/
theorem prop_11_2_3_R_bounds : 0 ≤ R 1e30 1600000000 ∧ R 1e30 1600000000 ≤ 0.95665 := by
  unfold R
  rw [prop_11_2_3_rpow_third]
  set A := Real.log (4 * 1600000000 : ℝ) with hA
  set B := Real.log (9 * 1e10 / (2.004 * 1600000000) : ℝ) with hB
  have h1 : A ≤ 23 := by
    have := prop_11_2_3_log_le 23 (by norm_num)
      (by norm_num : (4 * 1600000000 : ℝ) ≤ 2.7182818283 ^ 23)
    exact this.trans (by norm_num)
  have h1' : 0 ≤ A := Real.log_nonneg (by norm_num)
  have h2 : 3 ≤ B := by
    have := prop_11_2_3_le_log 3
      (by norm_num : (2.7182818286 : ℝ) ^ 3 ≤ 9 * 1e10 / (2.004 * 1600000000))
    exact (by norm_num : (3 : ℝ) = ((3 : ℕ) : ℝ)).trans_le this
  have hu0 : 0 ≤ A / (2 * B) := div_nonneg h1' (by linarith)
  have hu : A / (2 * B) ≤ 23 / 6 := by
    rw [div_le_iff₀ (by linarith)]
    linarith
  have h3 : Real.log (1 + A / (2 * B)) ≤ 2 := by
    have := prop_11_2_3_log_le 2 (by linarith)
      ((by linarith : 1 + A / (2 * B) ≤ 5).trans (by norm_num))
    exact this.trans (by norm_num)
  have h4 : 0 ≤ Real.log (1 + A / (2 * B)) := Real.log_nonneg (by linarith)
  constructor <;> linarith

theorem prop_11_2_3_expγ_le : rexp eulerMascheroniConstant ≤ 2 := by
  have h1 := Real.eulerMascheroniConstant_lt_two_thirds
  have h2 := Real.log_two_gt_d9
  calc rexp eulerMascheroniConstant ≤ rexp (Real.log 2) := Real.exp_le_exp.2 (by linarith)
    _ = 2 := Real.exp_log (by norm_num)

/-- `Ϝ(r)` at `r = 8·10⁸`: `0 < Ϝ(r) ≤ 9.3025` (true value `≈ 6.21`). Here
`log r ∈ [20, 21]`, `log log r ∈ [2, 4]`, `e^γ ≤ 2`. -/
theorem prop_11_2_3_Fr_bounds : 0 < Fr 800000000 ∧ Fr 800000000 ≤ 9.3025 := by
  unfold Fr
  have hl1 : (20 : ℝ) ≤ Real.log 800000000 := by
    exact_mod_cast prop_11_2_3_le_log 20 (by norm_num)
  have hl2 : Real.log 800000000 ≤ 21 := by
    exact_mod_cast prop_11_2_3_log_le 21 (by norm_num) (by norm_num)
  have hll1 : (2 : ℝ) ≤ Real.log (Real.log 800000000) := by
    exact_mod_cast prop_11_2_3_le_log 2 ((by norm_num : (2.7182818286 : ℝ) ^ 2 ≤ 20).trans hl1)
  have hll2 : Real.log (Real.log 800000000) ≤ 4 := by
    exact_mod_cast prop_11_2_3_log_le 4 (by linarith)
      (hl2.trans (by norm_num : (21 : ℝ) ≤ 2.7182818283 ^ 4))
  have hγ := prop_11_2_3_expγ_le
  have hγ0 : 0 < rexp eulerMascheroniConstant := Real.exp_pos _
  have t1 : rexp eulerMascheroniConstant * Real.log (Real.log 800000000) ≤ 2 * 4 :=
    mul_le_mul hγ hll2 (by linarith) (by norm_num)
  have t2 : 2.50637 / Real.log (Real.log 800000000) ≤ 2.50637 / 2 :=
    div_le_div_of_nonneg_left (by norm_num) (by norm_num) hll1
  have t3 : 0 < rexp eulerMascheroniConstant * Real.log (Real.log 800000000) :=
    mul_pos hγ0 (by linarith)
  have t4 : 0 < 2.50637 / Real.log (Real.log 800000000) := div_pos (by norm_num) (by linarith)
  constructor <;> linarith

/-- `L_t` at `t = 2r = 1.6·10⁹`: `0 ≤ L_t ≤ 1100` (true value `≈ 803`). -/
theorem prop_11_2_3_Lg_bounds : 0 ≤ Lg 1600000000 ∧ Lg 1600000000 ≤ 1100 := by
  unfold Lg
  rw [show (1600000000 : ℝ) / 2 = 800000000 by norm_num]
  obtain ⟨hF0, hF⟩ := prop_11_2_3_Fr_bounds
  have hl : Real.log 1600000000 ≤ 22 := by
    exact_mod_cast prop_11_2_3_log_le 22 (by norm_num) (by norm_num)
  have hl0 : 0 ≤ Real.log (1600000000 : ℝ) := Real.log_nonneg (by norm_num)
  have t1 : Fr 800000000 * (13 / 4 * Real.log 1600000000 + 7.82) ≤
      9.3025 * (13 / 4 * 22 + 7.82) :=
    mul_le_mul hF (by linarith) (by linarith) (by norm_num)
  have t2 : 0 ≤ Fr 800000000 * (13 / 4 * Real.log 1600000000 + 7.82) :=
    mul_nonneg hF0.le (by linarith)
  constructor <;> linarith

/-- If `C_{φ,2,8} = 0`, then `R_{x,8,φ,t} = R_{x,t}` and `g_{x,φ}(r)` at `x = 10³⁰`, `K = 8`,
`r = 8·10⁸` is the explicit expression below (`√(2r) = 4·10⁴`, `x^{-1/6} = 10⁻⁵`). -/
theorem prop_11_2_3_g_eq (φ : ℝ → ℝ) (hC2 : prop_11_2_3_C2 φ 8 = 0) :
    prop_11_2_3_g 1e30 8 φ 800000000 =
      ((R 1e30 1600000000 * Real.log 1600000000 + 0.5) * √(Fr 800000000) + 2.5) / 40000 +
        Lg 1600000000 / 800000000 + 3.36 * (8 : ℝ) ^ (1 / 6 : ℝ) * 1e-5 := by
  unfold prop_11_2_3_g prop_11_2_3_RK
  rw [hC2, zero_div, mul_zero, zero_div, add_zero, prop_11_2_3_rpow_neg_sixth,
    show (2 * 800000000 : ℝ) = 1600000000 by norm_num,
    show √(1600000000 : ℝ) = 40000 by
      rw [show (1600000000 : ℝ) = 40000 ^ 2 by norm_num]; exact Real.sqrt_sq (by norm_num)]

/-- `0 ≤ g_{x,φ}(r) ≤ 1/100` at the counterexample (true value `≈ 0.00122`). -/
theorem prop_11_2_3_g_bounds (φ : ℝ → ℝ) (hC2 : prop_11_2_3_C2 φ 8 = 0) :
    0 ≤ prop_11_2_3_g 1e30 8 φ 800000000 ∧ prop_11_2_3_g 1e30 8 φ 800000000 ≤ 1 / 100 := by
  rw [prop_11_2_3_g_eq φ hC2]
  obtain ⟨hR0, hR⟩ := prop_11_2_3_R_bounds
  obtain ⟨hF0, hF⟩ := prop_11_2_3_Fr_bounds
  obtain ⟨hL0, hL⟩ := prop_11_2_3_Lg_bounds
  have hl : Real.log 1600000000 ≤ 22 := by
    exact_mod_cast prop_11_2_3_log_le 22 (by norm_num) (by norm_num)
  have hl0 : 0 ≤ Real.log (1600000000 : ℝ) := Real.log_nonneg (by norm_num)
  have hs : √(Fr 800000000) ≤ 3.05 := by
    rw [Real.sqrt_le_left (by norm_num)]
    exact hF.trans (by norm_num)
  have hs0 : 0 ≤ √(Fr 800000000) := Real.sqrt_nonneg _
  have hK := prop_11_2_3_eight_rpow
  have hK0 : 0 ≤ (8 : ℝ) ^ (1 / 6 : ℝ) := by positivity
  have t1 : R 1e30 1600000000 * Real.log 1600000000 ≤ 0.95665 * 22 := by
    calc R 1e30 1600000000 * Real.log 1600000000
        ≤ 0.95665 * Real.log 1600000000 := mul_le_mul_of_nonneg_right hR hl0
      _ ≤ 0.95665 * 22 := mul_le_mul_of_nonneg_left hl (by norm_num)
  have t1' : 0 ≤ R 1e30 1600000000 * Real.log 1600000000 := mul_nonneg hR0 hl0
  have t2 : (R 1e30 1600000000 * Real.log 1600000000 + 0.5) * √(Fr 800000000) ≤
      (0.95665 * 22 + 0.5) * 3.05 :=
    mul_le_mul (by linarith) hs hs0 (by norm_num)
  have t2' : 0 ≤ (R 1e30 1600000000 * Real.log 1600000000 + 0.5) * √(Fr 800000000) :=
    mul_nonneg (by linarith) hs0
  have t3 : 3.36 * (8 : ℝ) ^ (1 / 6 : ℝ) * 1e-5 ≤ 3.36 * 2 * 1e-5 := by
    have := mul_le_mul_of_nonneg_left hK (by norm_num : (0 : ℝ) ≤ 3.36)
    nlinarith
  have t3' : 0 ≤ 3.36 * (8 : ℝ) ^ (1 / 6 : ℝ) * 1e-5 := by positivity
  have t4 : ((R 1e30 1600000000 * Real.log 1600000000 + 0.5) * √(Fr 800000000) + 2.5) / 40000 ≤
      ((0.95665 * 22 + 0.5) * 3.05 + 2.5) / 40000 := by
    apply div_le_div_of_nonneg_right _ (by norm_num)
    linarith
  have t4' : 0 ≤ ((R 1e30 1600000000 * Real.log 1600000000 + 0.5) * √(Fr 800000000) + 2.5) /
      40000 := div_nonneg (by linarith) (by norm_num)
  have t5 : Lg 1600000000 / 800000000 ≤ 1100 / 800000000 :=
    div_le_div_of_nonneg_right hL (by norm_num)
  have t5' : 0 ≤ Lg 1600000000 / 800000000 := div_nonneg hL0 (by norm_num)
  have : ((0.95665 * 22 + 0.5) * 3.05 + 2.5) / 40000 + 1100 / 800000000 + 3.36 * 2 * 1e-5 ≤
      (1 / 100 : ℝ) := by norm_num
  constructor <;> linarith

/-- The bump at `X = 10³⁰` vanishes on `[1/8, 1]`, so `C_{φ,2,8} = 0`. -/
theorem prop_11_2_3_C2_bump : prop_11_2_3_C2 (prop_11_2_3_bump 1e30) 8 = 0 := by
  unfold prop_11_2_3_C2
  rw [neg_eq_zero]
  have key : EqOn (fun w => prop_11_2_3_bump 1e30 w * Real.log w) (fun _ => 0)
      (uIcc (1 / 8) 1) := by
    intro w hw
    rw [uIcc_of_le (by norm_num)] at hw
    have hb : prop_11_2_3_bump 1e30 w = 0 := by
      by_contra h
      have h3 := (prop_11_2_3_bump_ne_zero h).2
      linarith [hw.1]
    simp [hb]
  rw [intervalIntegral.integral_congr key]
  simp

/-- The bump at `X = 10³⁰` is supported in `(0, 1/8]`, so `C_{φ,0,8} = 1.04488 |φ|₁`. -/
theorem prop_11_2_3_C0_bump :
    prop_11_2_3_C0 (prop_11_2_3_bump 1e30) 8 =
      1.04488 * ∫ w in Ioi (0:ℝ), prop_11_2_3_bump 1e30 w := by
  unfold prop_11_2_3_C0
  congr 1
  rw [intervalIntegral.integral_of_le (by norm_num)]
  have hsupp : ∀ w, prop_11_2_3_bump 1e30 w ≠ 0 → 0 < w ∧ w ≤ 1 / 8 := by
    intro w h
    obtain ⟨h1, h2⟩ := prop_11_2_3_bump_ne_zero h
    constructor <;> linarith
  have e1 : ∫ w in Ioc (0:ℝ) (1 / 8), |prop_11_2_3_bump 1e30 w| =
      ∫ w, prop_11_2_3_bump 1e30 w := by
    rw [setIntegral_eq_integral_of_forall_compl_eq_zero]
    · congr 1
      funext w
      exact abs_of_nonneg (prop_11_2_3_bump_nonneg _ w)
    · intro w hw
      by_contra h
      exact hw (hsupp w (abs_ne_zero.mp h))
  have e2 : ∫ w in Ioi (0:ℝ), prop_11_2_3_bump 1e30 w = ∫ w, prop_11_2_3_bump 1e30 w := by
    rw [setIntegral_eq_integral_of_forall_compl_eq_zero]
    intro w hw
    by_contra h
    exact hw (hsupp w h).1
  rw [e1, e2]

/-! ## The counterexample and the refutation -/

/-- **The counterexample.** At `x = 10³⁰`, `K = 8`, `φ = prop_11_2_3_bump 10³⁰`, `α = 1/(2q)`,
`δ = 0`, `a = 1`, `q = 8·10⁸`, the right side of (11.18) is smaller than `|S_{η_*}(α, x)|`:
`g_{x,φ}(r) |φ|₁ x ≤ |φ|₁ x/100 < log 2 · (4/15) |φ|₁ x ≤ |S_{η_*}(α, x)|`. -/
theorem prop_11_2_3_counterexample :
    prop_11_2_3_g 1e30 8 (prop_11_2_3_bump 1e30) (max 1 (|(0:ℝ)| / 8) * ((800000000 : ℕ) : ℝ)) *
        prop_11_2_3_norm1 (prop_11_2_3_bump 1e30) * 1e30 <
      ‖S (mellinConv eta2 (prop_11_2_3_bump 1e30)) 1e30 (1 / (2 * 800000000))‖ := by
  have hX : (0:ℝ) < 1e30 := by norm_num
  rw [show max 1 (|(0:ℝ)| / 8) * ((800000000 : ℕ) : ℝ) = 800000000 by norm_num,
    prop_11_2_3_norm_S_bump hX, prop_11_2_3_norm1_bump]
  have hg := (prop_11_2_3_g_bounds _ prop_11_2_3_C2_bump).2
  have hI := prop_11_2_3_integral_bump_pos hX
  have hM := prop_11_2_3_mellin_bump_ge hX
  have hlog := Real.log_two_gt_d9
  set I := ∫ w in Ioi (0:ℝ), prop_11_2_3_bump 1e30 w with hI_def
  set M := mellinConv eta2 (prop_11_2_3_bump 1e30) (2 / 1e30) with hM_def
  set g := prop_11_2_3_g 1e30 8 (prop_11_2_3_bump 1e30) 800000000 with hg_def
  have hIX : 0 < I * 1e30 := mul_pos hI hX
  have h1 : g * I * 1e30 ≤ 1 / 100 * (I * 1e30) := by
    rw [mul_assoc]
    exact mul_le_mul_of_nonneg_right hg hIX.le
  have h2 : 1 / 100 * (I * 1e30) < Real.log 2 * (4 * 1e30 / 15 * I) := by
    nlinarith [mul_pos (sub_pos.2 hlog) hI]
  have h3 : Real.log 2 * (4 * 1e30 / 15 * I) ≤ Real.log 2 * M :=
    mul_le_mul_of_nonneg_left hM (Real.log_nonneg (by norm_num))
  linarith

/-- **The real part also exceeds the bound**, so the refutation does not depend on reading (11.18)
(printed `S_{η_*}(α, x) ≤ …`) with absolute value bars: `S_{η_*}(α, x) = log 2 · η_*(2/x) · e(1/q)`
and `cos(2π/q) ≥ 0.99`. -/
theorem prop_11_2_3_counterexample_re :
    prop_11_2_3_g 1e30 8 (prop_11_2_3_bump 1e30) (max 1 (|(0:ℝ)| / 8) * ((800000000 : ℕ) : ℝ)) *
        prop_11_2_3_norm1 (prop_11_2_3_bump 1e30) * 1e30 <
      (S (mellinConv eta2 (prop_11_2_3_bump 1e30)) 1e30 (1 / (2 * 800000000))).re := by
  have hX : (0:ℝ) < 1e30 := by norm_num
  rw [show max 1 (|(0:ℝ)| / 8) * ((800000000 : ℕ) : ℝ) = 800000000 by norm_num,
    prop_11_2_3_re_S_bump hX, prop_11_2_3_norm1_bump]
  have hg := (prop_11_2_3_g_bounds _ prop_11_2_3_C2_bump).2
  have hI := prop_11_2_3_integral_bump_pos hX
  have hM := prop_11_2_3_mellin_bump_ge hX
  have hlog := Real.log_two_gt_d9
  have hcos : (0.99 : ℝ) ≤ Real.cos (2 * π * (2 * (1 / (2 * 800000000)))) := by
    have h := Real.one_sub_sq_div_two_le_cos (x := 2 * π * (2 * (1 / (2 * 800000000))))
    have hπ := Real.pi_lt_d2
    have hπ0 := Real.pi_pos
    nlinarith
  set I := ∫ w in Ioi (0:ℝ), prop_11_2_3_bump 1e30 w with hI_def
  set M := mellinConv eta2 (prop_11_2_3_bump 1e30) (2 / 1e30) with hM_def
  set g := prop_11_2_3_g 1e30 8 (prop_11_2_3_bump 1e30) 800000000 with hg_def
  set c := Real.cos (2 * π * (2 * (1 / (2 * 800000000)))) with hc_def
  have hIX : 0 < I * 1e30 := mul_pos hI hX
  have hM0 : 0 ≤ M := prop_11_2_3_mellin_nonneg _ (prop_11_2_3_bump_nonneg _) _
  have hl0 : 0 ≤ Real.log 2 := Real.log_nonneg (by norm_num)
  have h1 : g * I * 1e30 ≤ 1 / 100 * (I * 1e30) := by
    rw [mul_assoc]
    exact mul_le_mul_of_nonneg_right hg hIX.le
  have h2 : 1 / 100 * (I * 1e30) < 0.99 * (Real.log 2 * (4 * 1e30 / 15 * I)) := by
    nlinarith [mul_pos (sub_pos.2 hlog) hI]
  have h3 : 0.99 * (Real.log 2 * (4 * 1e30 / 15 * I)) ≤ 0.99 * (Real.log 2 * M) :=
    mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left hM hl0) (by norm_num)
  have h4 : 0.99 * (Real.log 2 * M) ≤ Real.log 2 * M * c := by
    have := mul_le_mul_of_nonneg_left hcos (mul_nonneg hl0 hM0)
    linarith
  linarith

/-- **The first case fails even on non-degenerate data**, at the point of
`prop_11_2_3_counterexample` (`x = 10³⁰`, `K = 8`, `q = r = 8·10⁸`). -/
theorem prop_11_2_3_first_case_nondegenerate_false : ¬ prop_11_2_3_first_case_nondegenerate := by
  intro h
  have hX : (0:ℝ) < 1e30 := by norm_num
  have h1 := h 1e30 8 (by norm_num) (by norm_num) (prop_11_2_3_bump 1e30)
    (prop_11_2_3_bump_continuous 1e30).continuousOn (fun w _ => prop_11_2_3_bump_nonneg _ w)
    (prop_11_2_3_bump_integrable hX).integrableOn
    (by rw [prop_11_2_3_norm1_bump]; exact prop_11_2_3_integral_bump_pos hX)
    (1 / (2 * 800000000)) 0 1 800000000 (by norm_num) ⟨0, by norm_num⟩
    (by rw [prop_11_2_3_rpow_two_thirds]; norm_num) (by norm_num)
    (by rw [prop_11_2_3_rpow_two_thirds]; norm_num)
    (by rw [prop_11_2_3_rpow_third_div]; norm_num) (by norm_num)
    (by rw [prop_11_2_3_rpow_third_div]; norm_num)
  exact absurd h1 (not_le.2 prop_11_2_3_counterexample)

/-- **[H, Prop. 11.2.3] as printed is false**: its first case fails at the point of
`prop_11_2_3_counterexample`, where all hypotheses hold and no junk value occurs. -/
theorem prop_11_2_3_false : ¬ prop_11_2_3 := fun h =>
  prop_11_2_3_first_case_nondegenerate_false (prop_11_2_3_imp_first_case_nondegenerate h)

/-- **The failure is exactly the dropped term.** At the counterexample, the first case with
`C_{φ,0,K}/|φ|₁` added to `g_{x,φ}` (as [H]'s proof gives, and as (13.17) uses) holds:
`|S_{η_*}(α, x)| ≤ log 2 · (6/5) |φ|₁ x ≤ C_{φ,0,K} x`, where `C_{φ,0,8} = 1.04488 |φ|₁`. -/
theorem prop_11_2_3_counterexample_corrected :
    ‖S (mellinConv eta2 (prop_11_2_3_bump 1e30)) 1e30 (1 / (2 * 800000000))‖ ≤
      (prop_11_2_3_g 1e30 8 (prop_11_2_3_bump 1e30)
          (max 1 (|(0:ℝ)| / 8) * ((800000000 : ℕ) : ℝ)) +
        prop_11_2_3_C0 (prop_11_2_3_bump 1e30) 8 / prop_11_2_3_norm1 (prop_11_2_3_bump 1e30)) *
        prop_11_2_3_norm1 (prop_11_2_3_bump 1e30) * 1e30 := by
  have hX : (0:ℝ) < 1e30 := by norm_num
  rw [show max 1 (|(0:ℝ)| / 8) * ((800000000 : ℕ) : ℝ) = 800000000 by norm_num,
    prop_11_2_3_norm_S_bump hX, prop_11_2_3_norm1_bump, prop_11_2_3_C0_bump]
  have hg := (prop_11_2_3_g_bounds _ prop_11_2_3_C2_bump).1
  have hI := prop_11_2_3_integral_bump_pos hX
  have hM := prop_11_2_3_mellin_bump_le hX
  have hlog := Real.log_two_lt_d9
  set I := ∫ w in Ioi (0:ℝ), prop_11_2_3_bump 1e30 w with hI_def
  set M := mellinConv eta2 (prop_11_2_3_bump 1e30) (2 / 1e30) with hM_def
  set g := prop_11_2_3_g 1e30 8 (prop_11_2_3_bump 1e30) 800000000 with hg_def
  rw [mul_div_assoc, div_self hI.ne', mul_one]
  have h1 : 0 ≤ g * I * 1e30 := mul_nonneg (mul_nonneg hg hI.le) hX.le
  have h2 : Real.log 2 * M ≤ Real.log 2 * (6 * 1e30 / 5 * I) :=
    mul_le_mul_of_nonneg_left hM (Real.log_nonneg (by norm_num))
  have h3 : Real.log 2 * (6 * 1e30 / 5 * I) ≤ 1.04488 * I * 1e30 := by
    nlinarith [mul_pos (sub_pos.2 hlog) hI]
  nlinarith

/-! ## Auxiliary: the formalization's `η_*` and `φ` in [H]'s terms -/

open TernaryGoldbach.Helfgott (etaStar phi κ) in
/-- The repository's `S_{η_*}(α, x)`, with `η_*(t) = (η₂ *_M φ)(κt)`, is [H]'s `S_{η₂ *_M φ}(α, y)` at
the scale `y = x/κ`. So the Lean `prop_11_2_3` and `prop_11_2_3'` bound [H]'s sum for this `φ` at
scale `y`. -/
theorem prop_11_2_3_S_etaStar (x α : ℝ) :
    S etaStar x α = S (mellinConv eta2 phi) (x / κ) α := by
  unfold S etaStar
  congr 1
  funext n
  rw [div_div_eq_mul_div, mul_comm (n : ℝ) κ, mul_div_assoc]

open TernaryGoldbach.Helfgott (phi) in
/-- The repository's `φ(t) = t² e^{−t²/2}` satisfies [H]'s hypotheses on `φ` (continuous,
nonnegative and integrable on `[0, ∞)`). -/
theorem prop_11_2_3_phi_admissible :
    ContinuousOn phi (Ici 0) ∧ (∀ w, 0 ≤ w → 0 ≤ phi w) ∧ IntegrableOn phi (Ici 0) := by
  refine ⟨(by unfold phi; fun_prop : Continuous phi).continuousOn,
    fun w _ => by unfold phi; positivity, ?_⟩
  have := integrable_rpow_mul_exp_neg_mul_sq (b := 1 / 2) (by norm_num) (s := 2) (by norm_num)
  refine (this.congr (Filter.Eventually.of_forall fun t => ?_)).integrableOn
  simp only [phi, Real.rpow_two]
  ring_nf

end Companion.Book
