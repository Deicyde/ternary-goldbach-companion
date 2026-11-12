import TernaryGoldbach

/-!
# [H, Theorem 13.2.1]: the minor-arc total, from ℓ² bounds over arcs and ℓ∞ bounds

**What [H] states.** Theorem 13.2.1 (`\label{thm:ostop}`, §13.2 "The minor-arc total", book
pp. 248–249, PDF pp. 258–259, <https://arxiv.org/pdf/1501.05438v2#page=258>; it is Thm. 6.3 of the
2013 preprint arXiv:1312.7748v2, which has `c₊ = 2.3912`, `c₋ = 0.6294` and `C_{φ,3}(log x)`).
Let `x ≥ 10²⁵ κ` with `κ ≥ 1`, `S_η(α,x) = Σₙ Λ(n) e(αn) η(n/x)` (13.9),
`η_*(t) = (η₂ *_M φ)(κt)` with `φ : [0,∞) → [0,∞)` continuous and in `ℓ¹`, and
`η₊ : [0,∞) → [0,∞)` bounded, piecewise differentiable, `η₊(t) → 0`. Let `𝔐_{8,r}` be the arcs
(10.5) with `δ₀ = 8`, `10⁵ ≤ r₀ < r₁ = (3/8)(x/κ)^{4/15}`, and `g = g_{x/κ,φ}` with
`K = log(x/κ)/2`, where (13.10)
`g_{y,φ}(r) = ((R_{y,K,φ,2r} log 2r + 0.5)√Ϝ(r) + 2.5)/√(2r) + L_{2r}/r + 3.36 K^{1/6} y^{-1/6}`.
Then
`Z_{r₀} = ∫_{(ℝ/ℤ) \ 𝔐_{8,r₀}} |S_{η_*}(α,x)| |S_{η₊}(α,x)|² dα
        ≤ (√(|φ|₁ x (M + T)/κ) + √(S_{η_*}(0,x) · E))²`,
with `S`, `T`, `J`, `E` as in (13.11), the constants `C_{η₊,0}`, `C_{η₊,1}`, `C_{η₊,2}`,
`C_{φ,3}(K)` of (13.12), `M` as in (13.13), `c₊ = 2.0532` and `c₋ = 0.6394`. Every object is
transcribed below (`thm_13_2_1_l1` … `thm_13_2_1_Z`); the statement is `thm_13_2_1`.

The proof combines an ℓ∞ bound off the arcs (13.14)–(13.17) (from Prop. 11.2.3), the ℓ² bound
(12.42) of Cor. 12.2.5 with `δ₀ = 8`, and the summation-by-parts Prop. 13.1.2, after splitting
off the non-prime and `n ≤ √x` part of `S_{η₊}` (bounded by `E`, via [RS62, Thms. 12, 13]).

**What the formalization proves.** No Lean declaration states this theorem's conclusion, or a
weakening or strengthening of it. The closed forms `M`, `T`, `E` (with `C_{η₊,0}`, `C_{η₊,1}`,
`C_{η₊,2}`), `g_{y,φ}`, `C_{φ,3}`, and a general `φ`, `κ`, `η₊` occur nowhere in the repo. The
repo's `E` (`MinorArcs/EBound.lean`) is the sum `Σ Λ(n)² η₊(n/x)²` itself, and `J` appears only
in the Part II bound `TernaryGoldbach.MinorArcs.l2_major_14_7` for the specific `η₊`. The related
declarations are:
* `TernaryGoldbach.MinorArcs.thm_13_2_1_conditional` (`MinorArcs/Thm1321.lean:41`, not in the
  main theorem's dependency cone): for an arbitrary sequence `aₙ` supported on primes `> √x` and
  an arbitrary `g`, *assuming* `|S_{η_*}(α,x)| ≤ g(n)` off `𝔐_{8,n}` (scale `x`) for
  `r₀ ≤ n ≤ r₁`, it proves the discrete form of (13.6),
  `∫_{(0,1] \ 𝔐_{8,r₀}} |Σaₙe(nα)|² |S_{η_*}|
     ≤ g(r₀)(H(r₀) − I₀) + Σ_{r₀<n≤r₁} g(n)(H(n) − H(n−1))`,
  with the ℓ² majorant `H = Hl2` from the formal Cor. 12.2.5 (`c₊ = 2`, `c_E ↦ 1.33258`);
* `TernaryGoldbach.MinorArcs.thm_13_2_1_repaired` (`Thm1321.lean:148`, in the cone): the same
  for the mixed family `𝔐_{8,r₀}(x)`, `𝔐_{8,n}(x/κ)` (`n > r₀`), with `H = Hl2y` (`δ₀ = 392`);
* `TernaryGoldbach.MinorArcs.minor_total` (`MinorArcs/MinorTotal.lean:320`): the end result
  (14.49), `Z_{r₀} ≤ 1.0376 x²/κ` for the specific `φ(t) = t²e^{-t²/2}`, `κ = 49`, `η₊`,
  `r₀ = 150000`, `x ≥ 4.9·10²⁶`, obtained by "repair 3" (repo `NOTES.md`, "Ch. 13: scale
  erratum"). All three take or build their ℓ∞ inputs with the repo's own constants.

**Relation: stated-only.** The book's statement is transcribed, and no relation with a formal
theorem is provable in either direction.
* *Book ⇒ formal* carries no information: every formal theorem above is proved outright, so
  `thm_13_2_1 → type_of% @…` would hold by discarding the hypothesis. None of them is a
  specialization of the book's conclusion. `thm_13_2_1_conditional`/`_repaired` concern an
  arbitrary prime-supported `aₙ` and an arbitrary *hypothesized* majorant `g`, and conclude a
  Prop. 13.1.2-type sum; the book's statement says nothing about them. `minor_total` bounds the
  same `Z_{r₀}` for special data, but the book's statement yields a numerical bound only together
  with the estimates of §14.3 for `S`, `J`, `E` and `∫ g(r)/r dr`, (14.29)–(14.48); that
  implication is item (14.49), certified in `Companion/Book/Eq_14_49.lean`.
* *Formal ⇒ book* is out of reach, for four independent reasons.
  1. The ℓ∞ input at scale `x` off `𝔐_{8,n}(x)`, `n > r₀`, is never proved. [H]'s proof derives
     it only off the arcs at scale `y = x/κ` ("`y` is used instead of `x` to define `𝔐_{8,r}`",
     p. 249), while its ℓ² input and `Z_{r₀}` use scale `x` (`NOTES.md`, "Ch. 13: scale
     erratum"); `thm_13_2_1_conditional` keeps that input as a hypothesis, and the repair changes
     the arcs.
  2. The formal ℓ² majorants are strictly larger than [H]'s `H(r) = (log(r+1)+c⁺)/(log √x + c⁻)`
     at every level (`thm_13_2_1_bookH_lt_Hl2`: e.g. `0.4828` against `0.4611` at `r = 10⁵`,
     `x = 10²⁵`). With `g` non-increasing, a larger `H` below the top level gives a larger
     Prop. 13.1.2 bound (Abel summation), so even with the ℓ∞ input granted, the formal ℓ² input
     is weaker than the one from which [H] computes `M`. [H]'s `c±` do come from (12.42) with
     `c₊ = 1.36` and `c_E = 1.3325822` (`thm_13_2_1_cpm_check`).
  3. The formal ℓ∞ constants are weaker: Theorem 3.1.1 with `0.8764`, `2.511`, `3.8`
     (`MinorArcs.gx`) in place of [H]'s `0.5`, `2.5`, `3.36` ([H]'s `0.5` does not follow from its
     own proof, see `MinorArcs/PointwiseBound.lean`). The repaired ℓ∞ majorant `ghatY` multiplies
     it by a further `1.398` (Prop. 11.2.3′, needed for the Prop. 11.2.3 erratum).
  4. Only the special `φ(t) = t²e^{-t²/2}`, `κ = 49` and `η₊` of Ch. 14 are treated. The
     book's `η_*` specializes to the repo's (`thm_13_2_1_etaStar_repo`).
* [H]'s own argument does not give the printed `M` either, so the truth of the printed statement
  is open. It is not refuted here: since `|S_{η_*}(α,x)| ≤ S_{η_*}(0,x)`, Parseval gives
  `Z_{r₀} ≤ S_{η_*}(0,x) Σ Λ(n)² η₊(n/x)²`, while the right side is `≥ S_{η_*}(0,x) E` and
  `E ≥ 0.51942 |η₊|²_∞ √x log x`. So a counterexample needs an `η₊` whose `S_{η₊}` has of the
  order of `√x/log x ≥ 10¹⁰` terms, together with a lower bound for its minor-arc integral.
  On p. 252 the jump of `H` at `r₁` is bounded by
  `7/15 + (−2.14938 + (8/15) log κ)/(log x + 2c⁻)`. With the printed `c±` that bound is false for
  every admissible `x`, `κ` (`thm_13_2_1_jump_slip`): the argument gives `−1.46271` in place of
  `−2.14938`, and `−2.14938` is the 2013 value, computed with `c₊ = 2.3912`, `c₋ = 0.6294`. So
  the printed `M` is smaller than what the argument yields, by
  `0.68666 g(r₁) S/(log x + 2c⁻)`. Separately, `I₀S ≥ (√J − √E)²` (p. 253) squares
  `√(I₀S) ≥ √J − √E`, which is only valid when `J ≥ E`. In [H]'s application `J ≈ 8.7x ≫ E`.
  (Downstream, Ch. 14 replaces the coefficient by `7/15`, which with `κ = 49` is valid for
  `−2.14938` but not for `−1.46271`. Our float recomputation then gives `M ≤ 0.8115x` and
  `Z_{r₀} ≤ 1.0175 x²/κ` instead of `0.80508x` and `1.00948`, still below the `1.058259` that
  §14.4 needs.)

Auxiliary results: `thm_13_2_1_hyps_satisfiable` (the hypotheses hold for the book's own
`κ = 49`, `φ = t²e^{-t²/2}`, `r₀ = 150000` and the tent `η₊(t) = max(0, 1 − t)`, so `thm_13_2_1`
is not vacuous), `thm_13_2_1_Z_integrableOn` (for those `φ`, `κ` the integral `Z_{r₀}` is a
genuine Lebesgue integral), `thm_13_2_1_S_zero_re` (`S_{η_*}(0,x)` is the real sum
`Σ Λ(n) η_*(n/x)`) and `thm_13_2_1_Z_formal_bound` (for the Ch. 14 data the book's `Z_{r₀}` is
`minor_total`'s left side, so the formalization bounds it by `1.0376 x²/κ`).
-/

open MeasureTheory Set Filter Topology

namespace Companion.Book

open TernaryGoldbach

/-! ## The objects of the statement -/

/-- `|φ|₁ = ∫₀^∞ |φ(w)| dw`, the `ℓ¹` (i.e. `L¹`) norm of `φ : [0,∞) → [0,∞)`. The integral is
over `(0,∞)`, which differs from `[0,∞)` by a null set. -/
noncomputable def thm_13_2_1_l1 (φ : ℝ → ℝ) : ℝ :=
  ∫ w in Ioi (0:ℝ), |φ w|

/-- `η_*(t) = (η₂ *_M φ)(κt)`, with `η₂ = 4 max(log 2 − |log 2t|, 0)` of [H, (11.10)]
(`TernaryGoldbach.Helfgott.eta2`, `0` for `t ≤ 0`) and the Mellin convolution
`(f *_M g)(t) = ∫₀^∞ f(w) g(t/w) dw/w` of [H, (2.7)] (`TernaryGoldbach.Helfgott.mellinConv`).
Both repo definitions agree with [H]. For `φ = t²e^{-t²/2}` and `κ = 49` this is the repo's
`TernaryGoldbach.Helfgott.etaStar` (`thm_13_2_1_etaStar_repo`). -/
noncomputable def thm_13_2_1_etaStar (φ : ℝ → ℝ) (κ t : ℝ) : ℝ :=
  Helfgott.mellinConv Helfgott.eta2 φ (κ * t)

/-- `C_{φ,2,K} = −∫_{1/K}^1 φ(w) log w dw` [H, (11.20)], an interval integral. -/
noncomputable def thm_13_2_1_Cphi2 (φ : ℝ → ℝ) (K : ℝ) : ℝ :=
  -∫ w in (1 / K)..1, φ w * Real.log w

/-- `C_{φ,3}(K) = (1.04488/|φ|₁) ∫₀^{1/K} |φ(w)| dw` [H, (13.12)]. -/
noncomputable def thm_13_2_1_Cphi3 (φ : ℝ → ℝ) (K : ℝ) : ℝ :=
  1.04488 / thm_13_2_1_l1 φ * ∫ w in (0:ℝ)..(1 / K), |φ w|

/-- `R_{y,K,φ,t} = R_{y,t} + (R_{y/K,t} − R_{y,t}) · (C_{φ,2,K}/|φ|₁)/log K` [H, (11.19)].
`R_{y,t} = 0.27125 log(1 + log 4t/(2 log(9y^{1/3}/(2.004t)))) + 0.41415` [H, (11.13)] is the
repo's `TernaryGoldbach.MinorArcs.R`, which agrees with [H] symbol for symbol. -/
noncomputable def thm_13_2_1_R (φ : ℝ → ℝ) (y K t : ℝ) : ℝ :=
  MinorArcs.R y t +
    (MinorArcs.R (y / K) t - MinorArcs.R y t) * (thm_13_2_1_Cphi2 φ K / thm_13_2_1_l1 φ) /
      Real.log K

/-- `g_{y,φ}(r) = ((R_{y,K,φ,2r} log 2r + 0.5) √Ϝ(r) + 2.5)/√(2r) + L_{2r}/r
  + 3.36 K^{1/6} y^{-1/6}`
[H, (13.10)] (= (11.19) with `x ↦ y`), with [H]'s constants `0.5`, `2.5`, `3.36`. Here
`Ϝ(r) = e^γ log log r + 2.50637/log log r` [H, (C.19)] is `TernaryGoldbach.MinorArcs.Fr`, and
`L_t = Ϝ(t/2)(13/4 log t + 7.82) + 13.66 log t + 37.55` [H, (11.13)] is
`TernaryGoldbach.MinorArcs.Lg`; both agree with [H]. This is *not* the repo's
`TernaryGoldbach.MinorArcs.gx` (constants `0.8764`, `2.511`, `3.8`, no `φ`, `K`). -/
noncomputable def thm_13_2_1_g (φ : ℝ → ℝ) (y K r : ℝ) : ℝ :=
  ((thm_13_2_1_R φ y K (2 * r) * Real.log (2 * r) + 0.5) * √(MinorArcs.Fr r) + 2.5) /
      √(2 * r) +
    MinorArcs.Lg (2 * r) / r + 3.36 * K ^ (1 / 6 : ℝ) * y ^ (-1 / 6 : ℝ)

/-- The sup-envelope `η̄(t) = sup_{r ≥ t} η(r)` used in [H, (13.12)] (the proof calls it
`\overline{η₊}`). For `η` bounded above on `[0,∞)` and `t ≥ 0` this `sSup` is the true
supremum. -/
noncomputable def thm_13_2_1_etaBar (η : ℝ → ℝ) (t : ℝ) : ℝ :=
  sSup (η '' Ici t)

/-- `|η|_∞ = sup_{t ≥ 0} |η(t)|`, the pointwise sup norm on `[0,∞)` (the proof uses it
pointwise: `η₊(n/x) ≤ |η₊|_∞`). -/
noncomputable def thm_13_2_1_supNorm (η : ℝ → ℝ) : ℝ :=
  sSup ((fun t => |η t|) '' Ici 0)

/-- `C_{η₊,0} = 0.7131 ∫₀^∞ (1/√t) (sup_{r≥t} η₊(r))² dt` [H, (13.12)]. -/
noncomputable def thm_13_2_1_C0 (η : ℝ → ℝ) : ℝ :=
  0.7131 * ∫ t in Ioi (0:ℝ), 1 / √t * thm_13_2_1_etaBar η t ^ 2

/-- `C_{η₊,1} = 0.7131 ∫₁^∞ (log t/√t) (sup_{r≥t} η₊(r))² dt` [H, (13.12)]. -/
noncomputable def thm_13_2_1_C1 (η : ℝ → ℝ) : ℝ :=
  0.7131 * ∫ t in Ioi (1:ℝ), Real.log t / √t * thm_13_2_1_etaBar η t ^ 2

/-- `C_{η₊,2} = 0.51942 |η₊|_∞²` [H, (13.12)]. -/
noncomputable def thm_13_2_1_C2 (η : ℝ → ℝ) : ℝ :=
  0.51942 * thm_13_2_1_supNorm η ^ 2

/-- `S = Σ_{p > √x} (log p)² η₊²(p/x)` [H, (13.11)], over primes `p`. [H] prints `η₊²(n/x)`, a
misprint for `η₊²(p/x)` (no `n` is bound there). -/
noncomputable def thm_13_2_1_Ssum (η : ℝ → ℝ) (x : ℝ) : ℝ :=
  ∑' n : ℕ, if n.Prime ∧ √x < n then Real.log n ^ 2 * η (n / x) ^ 2 else 0

/-- `J = ∫_{𝔐_{8,r₀}} |S_{η₊}(α,x)|² dα` [H, (13.11)], with the arcs (10.5) at scale `x`
(`TernaryGoldbach.Helfgott.majorArcs 8 r₀ x`) intersected with the fundamental domain `(0,1]`. -/
noncomputable def thm_13_2_1_J (η : ℝ → ℝ) (x r₀ : ℝ) : ℝ :=
  ∫ α in Ioc (0:ℝ) 1 ∩ Helfgott.majorArcs 8 r₀ x, ‖Helfgott.S η x α‖ ^ 2

/-- `E = ((C_{η₊,0} + C_{η₊,2}) log x + (2C_{η₊,0} + C_{η₊,1})) · x^{1/2}` [H, (13.11)]. -/
noncomputable def thm_13_2_1_E (η : ℝ → ℝ) (x : ℝ) : ℝ :=
  ((thm_13_2_1_C0 η + thm_13_2_1_C2 η) * Real.log x + (2 * thm_13_2_1_C0 η + thm_13_2_1_C1 η)) *
    x ^ (1 / 2 : ℝ)

/-- `r₁ = (3/8)(x/κ)^{4/15}`. -/
noncomputable def thm_13_2_1_r₁ (κ x : ℝ) : ℝ :=
  3 / 8 * (x / κ) ^ (4 / 15 : ℝ)

/-- `K = log(x/κ)/2`. -/
noncomputable def thm_13_2_1_K (κ x : ℝ) : ℝ :=
  Real.log (x / κ) / 2

/-- `T = C_{φ,3}(½ log(x/κ)) · (S − (√J − √E)²)` [H, (13.11)]. -/
noncomputable def thm_13_2_1_T (φ η : ℝ → ℝ) (κ x r₀ : ℝ) : ℝ :=
  thm_13_2_1_Cphi3 φ (1 / 2 * Real.log (x / κ)) *
    (thm_13_2_1_Ssum η x - (√(thm_13_2_1_J η x r₀) - √(thm_13_2_1_E η x)) ^ 2)

/-- `M` [H, (13.13)]:
`M = g(r₀)·((log(r₀+1) + c⁺)/(log √x + c⁻) · S − (√J − √E)²)
   + ((2/(log x + 2c⁻)) ∫_{r₀}^{r₁} g(r)/r dr
      + (7/15 + (−2.14938 + (8/15) log κ)/(log x + 2c⁻)) g(r₁)) · S`
with `g = g_{x/κ,φ}`, `K = log(x/κ)/2`, `c⁺ = 2.0532`, `c⁻ = 0.6394` (printed as `c₊`, `c₋`
below the display). The integral is an interval integral. -/
noncomputable def thm_13_2_1_M (φ η : ℝ → ℝ) (κ x r₀ : ℝ) : ℝ :=
  let g := thm_13_2_1_g φ (x / κ) (thm_13_2_1_K κ x)
  let r₁ := thm_13_2_1_r₁ κ x
  let S := thm_13_2_1_Ssum η x
  let J := thm_13_2_1_J η x r₀
  let E := thm_13_2_1_E η x
  let cplus : ℝ := 2.0532
  let cminus : ℝ := 0.6394
  g r₀ * ((Real.log (r₀ + 1) + cplus) / (Real.log √x + cminus) * S - (√J - √E) ^ 2) +
    (2 / (Real.log x + 2 * cminus) * (∫ r in r₀..r₁, g r / r) +
      (7 / 15 + (-2.14938 + 8 / 15 * Real.log κ) / (Real.log x + 2 * cminus)) * g r₁) * S

/-- `Z_{r₀} = ∫_{(ℝ/ℤ) \ 𝔐_{8,r₀}} |S_{η_*}(α,x)| |S_{η₊}(α,x)|² dα`, over the fundamental
domain `(0,1]`. -/
noncomputable def thm_13_2_1_Z (φ η : ℝ → ℝ) (κ x r₀ : ℝ) : ℝ :=
  ∫ α in Ioc (0:ℝ) 1 \ Helfgott.majorArcs 8 r₀ x,
    ‖Helfgott.S (thm_13_2_1_etaStar φ κ) x α‖ * ‖Helfgott.S η x α‖ ^ 2

/-- **[H, Theorem 13.2.1]**, as printed.

Transcription choices:
* `κ x r₀ : ℝ`, `φ ηp : ℝ → ℝ` are universally quantified (`ηp` is [H]'s `η₊`; Lean does not
  accept `₊` in identifiers). `r₀` is real, since the theorem does not say it is an integer ([H]
  applies it with `r₀ = 150000`). Values of `φ`, `η₊` on `(−∞,0)` never enter: all arguments
  (`κn/(xw)`, `n/x`, `w ∈ (0, 1]`, `r ≥ t ≥ 0`) are `≥ 0`.
* `x ≥ 10²⁵·κ`, `κ ≥ 1`, `10⁵ ≤ r₀ < r₁ = (3/8)(x/κ)^{4/15}` (`thm_13_2_1_r₁`) are verbatim.
* "`φ : [0,∞) → [0,∞)` continuous and in `ℓ¹`" is `ContinuousOn φ (Ici 0)`, `φ ≥ 0` on
  `[0,∞)` and `IntegrableOn φ (Ici 0)` (Prop. 11.2.3, which the proof invokes, says `L¹`).
* "`η₊ : [0,∞) → [0,∞)` bounded, piecewise differentiable, `lim_{t→∞} η₊(t) = 0`" is: `η₊ ≥ 0`
  on `[0,∞)`; `BddAbove (η₊ '' Ici 0)`; differentiable at every `t > 0` outside a finite set of
  break points (our reading of "piecewise", which the proof never uses: its integration by parts
  is applied to the monotone envelope `η̄₊`); `Tendsto η₊ atTop (𝓝 0)`.
* *Added, not printed:* the integrands of `C_{η₊,0}` and `C_{η₊,1}` are integrable, i.e. `E < ∞`.
  When either integral diverges, [H]'s right side is `+∞` (or undefined), so the book's statement
  is void there. Lean's Bochner integral would instead return the junk value `0`, making `E` too
  small, so without these hypotheses the def would assert more than [H].
* `S_η(α,x) = Σₙ Λ(n) e(αn) η(n/x)` (13.9) is `TernaryGoldbach.Helfgott.S η x α`, a `tsum` over
  `ℕ` (`Λ(0) = 0`), with `e(t) = exp(2πit)`. If `Σ Λ(n) η₊(n/x)` diverges, the book's `S_{η₊}` is
  undefined, while Lean's `tsum` is `0`. Then `Z_{r₀} = 0` and the def holds trivially there, so no
  convergence hypothesis is needed. `S_{η_*}(0,x)` is `(S η_* x 0).re`, which is the real sum
  `Σ Λ(n) η_*(n/x)` (`thm_13_2_1_S_zero_re`).
* `𝔐_{8,r}` is (10.5) with `δ₀ = 8`, defined with the theorem's `x` ("as in (10.5)"):
  `TernaryGoldbach.Helfgott.majorArcs 8 r x` (radius `δ₀r/2qx` around `a/q` for odd `q ≤ r`,
  `δ₀r/qx` for even `q ≤ 2r`, `(a,q) = 1`, open intervals, lifted to `ℝ`), which agrees with
  (10.5). The proof uses arcs at scale `x/κ` for its ℓ∞ input; that concerns the proof, not the
  statement.
* Integrals over subsets of `ℝ/ℤ` (`Z_{r₀}`, `J`) are Lebesgue integrals over `(0,1] ∩ 𝔐̃` or
  `(0,1] \ 𝔐̃`, `𝔐̃ ⊆ ℝ` the `1`-periodic lift. `(0,1]` is a fundamental domain, so this is the
  Haar probability measure that [H] uses.
* `g = g_{x/κ,φ}` with `K = log(x/κ)/2` (`thm_13_2_1_g`, `thm_13_2_1_K`). [H] writes
  `K = log(x/\kappa)/2` with `\kappa` for `\varkappa`, read as the same `κ`.
  `C_{φ,3}(½ log(x/κ))` takes the argument as printed (it equals `K`).
* `S`, `T`, `J`, `E`, the `C`'s and `M` are `thm_13_2_1_Ssum`, `thm_13_2_1_T`, `thm_13_2_1_J`,
  `thm_13_2_1_E`, `thm_13_2_1_C0`/`C1`/`C2`/`Cphi3` and `thm_13_2_1_M`, each verbatim; see their
  docstrings (`η₊²(n/x)` in `S` is read as `η₊²(p/x)`). `x^{1/2}` is `x ^ (1/2 : ℝ)`, and all
  logarithms are natural.
* The conclusion `Z_{r₀} ≤ (√(|φ|₁ x(M+T)/κ) + √(S_{η_*}(0,x)·E))²` uses `Real.sqrt`. When
  `M + T < 0` (possible in degenerate cases, e.g. `S = 0` and `J ≠ E`), the book's first root is
  undefined, and Lean reads it as `0`.
* If `|φ|₁ = 0`, [H]'s quotients by `|φ|₁` are undefined and Lean's are `0`. But then `φ ≡ 0` on
  `[0,∞)` (it is continuous and `≥ 0`), so `η_* ≡ 0`, `Z_{r₀} = 0`, and the def holds trivially.
* Not vacuous: the hypotheses hold for the book's own `κ = 49`, `φ(t) = t²e^{-t²/2}`,
  `r₀ = 150000` with `η₊(t) = max(0, 1 − t)` (`thm_13_2_1_hyps_satisfiable`), and for these
  `φ`, `κ` the integral `Z_{r₀}` is genuine (`thm_13_2_1_Z_integrableOn`). -/
def thm_13_2_1 : Prop :=
  ∀ (κ x : ℝ) (φ ηp : ℝ → ℝ) (r₀ : ℝ),
    1 ≤ κ → (10 : ℝ) ^ 25 * κ ≤ x →
    ContinuousOn φ (Ici 0) → (∀ t, 0 ≤ t → 0 ≤ φ t) → IntegrableOn φ (Ici 0) →
    (∀ t, 0 ≤ t → 0 ≤ ηp t) → BddAbove (ηp '' Ici 0) →
    (∃ F : Finset ℝ, ∀ t, 0 < t → t ∉ F → DifferentiableAt ℝ ηp t) →
    Tendsto ηp atTop (𝓝 0) →
    IntegrableOn (fun t => 1 / √t * thm_13_2_1_etaBar ηp t ^ 2) (Ioi 0) →
    IntegrableOn (fun t => Real.log t / √t * thm_13_2_1_etaBar ηp t ^ 2) (Ioi 1) →
    (10 : ℝ) ^ 5 ≤ r₀ → r₀ < thm_13_2_1_r₁ κ x →
    thm_13_2_1_Z φ ηp κ x r₀ ≤
      (√(thm_13_2_1_l1 φ * x / κ * (thm_13_2_1_M φ ηp κ x r₀ + thm_13_2_1_T φ ηp κ x r₀)) +
        √((Helfgott.S (thm_13_2_1_etaStar φ κ) x 0).re * thm_13_2_1_E ηp x)) ^ 2

/-! ## Sanity checks on the transcription -/

/-- The book's `η_*` with the Ch. 14 choices `φ(t) = t²e^{-t²/2}` and `κ = 49` is the repo's
`TernaryGoldbach.Helfgott.etaStar`, by definition. -/
theorem thm_13_2_1_etaStar_repo :
    thm_13_2_1_etaStar Helfgott.phi Helfgott.κ = Helfgott.etaStar :=
  funext fun _ => rfl

/-- `S_η(0,x)`, read as `(S η x 0).re`, is the real sum `Σₙ Λ(n) η(n/x)` (as `e(0) = 1`). -/
theorem thm_13_2_1_S_zero_re (η : ℝ → ℝ) (x : ℝ) :
    (Helfgott.S η x 0).re = ∑' n : ℕ, ArithmeticFunction.vonMangoldt n * η (n / x) := by
  unfold Helfgott.S
  simp only [mul_zero, e_zero, mul_one]
  rw [← Complex.ofReal_tsum, Complex.ofReal_re]

/-- For the Ch. 14 data `φ(t) = t²e^{-t²/2}`, `κ = 49`, and any `η₊` for which `S_{η₊}(α,x)`
converges absolutely, the integrand of `Z_{r₀}` is integrable on the minor arcs. So `Z_{r₀}` is
a genuine Lebesgue integral there, not Lean's junk value `0`. -/
theorem thm_13_2_1_Z_integrableOn {x : ℝ} (hx : 0 < x) {η : ℝ → ℝ} (r₀ : ℝ)
    (hη : Summable fun n : ℕ => ‖((ArithmeticFunction.vonMangoldt n * η (n / x) : ℝ) : ℂ)‖) :
    IntegrableOn
      (fun α => ‖Helfgott.S (thm_13_2_1_etaStar Helfgott.phi Helfgott.κ) x α‖ *
        ‖Helfgott.S η x α‖ ^ 2)
      (Ioc 0 1 \ Helfgott.majorArcs 8 r₀ x) := by
  rw [thm_13_2_1_etaStar_repo]
  have h1 : Continuous fun α => Helfgott.S Helfgott.etaStar x α :=
    continuous_expTsum (Helfgott.summable_etaStar hx)
  have h2 : Continuous fun α => Helfgott.S η x α := continuous_expTsum hη
  exact ((h1.norm.mul (h2.norm.pow 2)).integrableOn_Icc (a := 0) (b := 1)).mono_set
    (sdiff_subset.trans Ioc_subset_Icc_self)

/-- **What the formalization proves about the same `Z_{r₀}`.** For the Ch. 14 data
`φ(t) = t²e^{-t²/2}`, `κ = 49`, `η₊` the repo's `etaPlus`, `r₀ = 150000`, the book's `Z_{r₀}`
(`thm_13_2_1_Z`) is the left side of `TernaryGoldbach.MinorArcs.minor_total`, which bounds it by
`1.0376 x²/κ` for `x ≥ 4.9·10²⁶` (with `numerics_M`). [H]'s Theorem 13.2.1 bounds it instead by
`(√(|φ|₁x(M+T)/κ) + √(S_{η_*}(0,x)E))²`, which becomes a number only with the estimates of
§14.3 (item (14.49)). -/
theorem thm_13_2_1_Z_formal_bound [Fact PlattGRH] [Fact RamareMoebius] {x : ℝ} (hx : (4.9e26 : ℝ) ≤ x) :
    thm_13_2_1_Z Helfgott.phi Helfgott.etaPlus Helfgott.κ x Helfgott.r₀ ≤
      1.0376 * x ^ 2 / Helfgott.κ := by
  have hx' : (49e25 : ℝ) ≤ x := by norm_num at hx ⊢; linarith
  unfold thm_13_2_1_Z
  rw [thm_13_2_1_etaStar_repo]
  exact MinorArcs.minor_total hx' (MinorArcs.numerics_M hx')

/-! ## The constants of the proof: why neither [H]'s argument nor the formalization gives `M` -/

/-- [H]'s `c±` come from (12.42) with `c₊ = 1.36` and `c_E = 1.3325822` (proof of Thm. 13.2.1,
p. 252): `c⁺ = 2.0532 > log 2 + 1.36` and `c⁻ = 0.6394 < log(1/√(2·8)) + log 2 + 1.3325822`. -/
theorem thm_13_2_1_cpm_check :
    Real.log 2 + 1.36 < 2.0532 ∧
      0.6394 < Real.log (1 / √(2 * 8)) + Real.log 2 + 1.3325822 := by
  have h1 := Real.log_two_lt_d9
  have h2 := Real.log_two_gt_d9
  refine ⟨by linarith, ?_⟩
  have h16 : √(2 * 8 : ℝ) = 2 ^ 2 := by
    rw [show (2 * 8 : ℝ) = (2 ^ 2) ^ 2 by norm_num]
    exact Real.sqrt_sq (by norm_num)
  have hl : Real.log (1 / √(2 * 8)) = -(2 * Real.log 2) := by
    rw [h16, one_div, Real.log_inv, Real.log_pow]
    push_cast; ring
  rw [hl]
  linarith

/-- **The jump bound in [H]'s proof is false as printed** (p. 252). For every admissible
`x ≥ 10²⁵κ`, `κ ≥ 1`, the jump `1 − H(r₁⁻) = 1 − (log(r₁ + 1) + c⁺)/(log √x + c⁻)` of [H]'s ℓ²
majorant at `r₁ = (3/8)(x/κ)^{4/15}` exceeds the printed bound
`7/15 + (−2.14938 + (8/15) log κ)/(log x + 2c⁻)`. With `c⁺ = 2.0532`, `c⁻ = 0.6394` the argument
gives `−2(log(3/8) + c⁺ − (8/15)c⁻) = −1.46271…`, not `−2.14938`; the latter is the value for the
2013 constants `c₊ = 2.3912`, `c₋ = 0.6294`. Hence the printed `M` (13.13) is smaller than what
the proof yields. (Float check: the gap is `0.0109` at `x = 4.9·10²⁶`, `κ = 49`.) -/
theorem thm_13_2_1_jump_slip {κ x : ℝ} (hκ : 1 ≤ κ) (hx : (10 : ℝ) ^ 25 * κ ≤ x) :
    7 / 15 + (-2.14938 + 8 / 15 * Real.log κ) / (Real.log x + 2 * 0.6394) <
      1 - (Real.log (thm_13_2_1_r₁ κ x + 1) + 2.0532) / (Real.log √x + 0.6394) := by
  have hκ0 : 0 < κ := by linarith
  have hx0 : 0 < x := lt_of_lt_of_le (by positivity) hx
  have hy : (10 : ℝ) ^ 15 ≤ x / κ := by
    rw [le_div_iff₀ hκ0]
    have : (10 : ℝ) ^ 15 * κ ≤ 10 ^ 25 * κ := by nlinarith
    linarith
  have hy0 : 0 < x / κ := by positivity
  have hpow : (10 : ℝ) ^ 4 ≤ (x / κ) ^ (4 / 15 : ℝ) := by
    have h := Real.rpow_le_rpow (by positivity : (0 : ℝ) ≤ 10 ^ 15) hy
      (by norm_num : (0 : ℝ) ≤ 4 / 15)
    have e : ((10 : ℝ) ^ 15) ^ (4 / 15 : ℝ) = 10 ^ 4 := by
      rw [← Real.rpow_natCast, ← Real.rpow_mul (by norm_num)]
      norm_num
    rw [e] at h
    exact h
  set r₁ := thm_13_2_1_r₁ κ x with hr₁
  have hr₁3750 : 3750 ≤ r₁ := by
    simp only [hr₁, thm_13_2_1_r₁]
    nlinarith
  have hr₁0 : 0 < r₁ := by linarith
  have hlogr₁ : Real.log r₁ = Real.log (3 / 8) + 4 / 15 * (Real.log x - Real.log κ) := by
    simp only [hr₁, thm_13_2_1_r₁]
    rw [Real.log_mul (by norm_num) (by positivity), Real.log_rpow hy0,
      Real.log_div hx0.ne' hκ0.ne']
  have hlog1 : Real.log (r₁ + 1) ≤ Real.log r₁ + 1 / r₁ := by
    have h := Real.log_le_sub_one_of_pos (show 0 < (r₁ + 1) / r₁ by positivity)
    rw [Real.log_div (by positivity) hr₁0.ne'] at h
    have e : (r₁ + 1) / r₁ - 1 = 1 / r₁ := by field_simp; ring
    linarith
  have hlog38 : Real.log (3 / 8) < -0.69 := by
    have h1 : Real.log (3 / 8) < Real.log (1 / 2) := Real.log_lt_log (by norm_num) (by norm_num)
    have h2 : Real.log (1 / 2) = -Real.log 2 := by rw [one_div, Real.log_inv]
    have h3 := Real.log_two_gt_d9
    linarith
  have hinv : 1 / r₁ ≤ 1 / 3750 := one_div_le_one_div_of_le (by norm_num) hr₁3750
  have hk : 0 ≤ Real.log κ := Real.log_nonneg hκ
  have hL : 0 ≤ Real.log x := Real.log_nonneg (by nlinarith)
  rw [Real.log_sqrt hx0.le]
  set L := Real.log x
  set k := Real.log κ
  set A := Real.log (r₁ + 1) + 2.0532
  set B := -2.14938 + 8 / 15 * k
  have hD : 0 < L / 2 + 0.6394 := by linarith
  have hkey : 2 * A + B < 16 / 15 * (L / 2 + 0.6394) := by
    simp only [A, B]
    linarith
  have hsplit : A / (L / 2 + 0.6394) + B / (L + 2 * 0.6394) =
      (2 * A + B) / (2 * (L / 2 + 0.6394)) := by
    rw [show L + 2 * 0.6394 = 2 * (L / 2 + 0.6394) by ring]
    field_simp
  have hlt : (2 * A + B) / (2 * (L / 2 + 0.6394)) < 8 / 15 := by
    rw [div_lt_iff₀ (by positivity)]
    linarith
  linarith

/-- **The formal ℓ² majorants are weaker than [H]'s.** At every level `n < r₁` (with
`n + 1 ≤ √x`), [H]'s `H(n) = (log(n+1) + c⁺)/(log √x + c⁻)` (from (12.42) with `c₊ = 1.36`) is
strictly smaller than `TernaryGoldbach.MinorArcs.Hl2` (the majorant of `thm_13_2_1_conditional`,
from the formal Cor. 12.2.5 with `c₊ = 2`, `c_E ↦ 1.33258`), which is at most
`TernaryGoldbach.MinorArcs.Hl2y` (the majorant of `thm_13_2_1_repaired`, `δ₀ = 392`). E.g. at
`n = 10⁵`, `x = 10²⁵`: `0.4611 < 0.4828 < 0.5170`. -/
theorem thm_13_2_1_bookH_lt_Hl2 {x T : ℝ} {r₁ n : ℕ} (hx : 784 ≤ x) (hT : 0 < T)
    (hn : n < r₁) (hnx : (n : ℝ) + 1 ≤ √x) :
    (Real.log ((n : ℝ) + 1) + 2.0532) / (Real.log √x + 0.6394) * T <
        MinorArcs.Hl2 x T r₁ n ∧
      MinorArcs.Hl2 x T r₁ n ≤ MinorArcs.Hl2y x T r₁ n := by
  unfold MinorArcs.Hl2 MinorArcs.Hl2y MinorArcs.cE
  rw [ite_eq_left hn, ite_eq_left hn]
  have hx0 : 0 < x := by linarith
  have hl1 := Real.log_two_lt_d9
  have hl2 := Real.log_two_gt_d9
  have hsx : (28 : ℝ) ≤ √x := by
    rw [show (28 : ℝ) = √784 by
      rw [show (784 : ℝ) = 28 ^ 2 by norm_num]; exact (Real.sqrt_sq (by norm_num)).symm]
    exact Real.sqrt_le_sqrt hx
  have h16 : 2 * √(x / 16) = √x / 2 := by
    rw [Real.sqrt_div' x (by norm_num : (0 : ℝ) ≤ 16),
      show √(16 : ℝ) = 4 by
        rw [show (16 : ℝ) = 4 ^ 2 by norm_num]; exact Real.sqrt_sq (by norm_num)]
    ring
  have h784 : 2 * √(x / 784) = √x / 14 := by
    rw [Real.sqrt_div' x (by norm_num : (0 : ℝ) ≤ 784),
      show √(784 : ℝ) = 28 by
        rw [show (784 : ℝ) = 28 ^ 2 by norm_num]; exact Real.sqrt_sq (by norm_num)]
    ring
  rw [h16, h784]
  set D := Real.log √x with hD
  set a := Real.log ((n : ℝ) + 1) with ha
  have hn0 : (0 : ℝ) ≤ n := Nat.cast_nonneg n
  have ha0 : 0 ≤ a := Real.log_nonneg (by linarith)
  have haD : a ≤ D := Real.log_le_log (by linarith) hnx
  have hlog2n : Real.log (2 * ((n : ℝ) + 1)) = Real.log 2 + a :=
    Real.log_mul (by norm_num) (by linarith)
  have hd2 : Real.log (√x / 2) = D - Real.log 2 := Real.log_div (by positivity) (by norm_num)
  have hd14 : Real.log (√x / 14) ≤ Real.log (√x / 4) :=
    Real.log_le_log (by positivity) (by linarith)
  have hd4 : Real.log (√x / 4) = D - 2 * Real.log 2 := by
    rw [Real.log_div (by positivity) (by norm_num),
      show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]
    push_cast; ring
  have hd14' : 0 < Real.log (√x / 14) := Real.log_pos (by linarith)
  have hD0 : 0 ≤ D := by
    have : Real.log 28 ≤ D := Real.log_le_log (by norm_num) hsx
    have h28 : 0 < Real.log 28 := Real.log_pos (by norm_num)
    linarith
  rw [hlog2n, hd2]
  constructor
  · refine mul_lt_mul_of_pos_right ?_ hT
    rw [div_lt_div_iff₀ (by linarith) (by linarith)]
    nlinarith [mul_nonneg (sub_nonneg.2 haD) (show (0 : ℝ) ≤ 0.69318 - Real.log 2 by linarith),
      mul_nonneg hD0 (show (0 : ℝ) ≤ 2 * Real.log 2 - 0.74638 by linarith)]
  · refine mul_le_mul_of_nonneg_right ?_ hT.le
    exact div_le_div_of_nonneg_left (by linarith) (by linarith) (by linarith)

/-! ## The hypotheses are satisfiable (the statement is not vacuous) -/

private theorem tent_antitone : Antitone fun t : ℝ => max 0 (1 - t) :=
  fun _ _ hab => max_le_max le_rfl (by linarith)

private theorem etaBar_tent (t : ℝ) :
    thm_13_2_1_etaBar (fun s : ℝ => max 0 (1 - s)) t = max 0 (1 - t) := by
  unfold thm_13_2_1_etaBar
  refine IsGreatest.csSup_eq ⟨⟨t, self_mem_Ici, rfl⟩, ?_⟩
  rintro _ ⟨s, hs, rfl⟩
  exact tent_antitone hs

private theorem tent_differentiableAt {t : ℝ} (ht : t ≠ 1) :
    DifferentiableAt ℝ (fun s : ℝ => max 0 (1 - s)) t := by
  rcases lt_or_gt_of_ne ht with h | h
  · have hev : (fun s : ℝ => max 0 (1 - s)) =ᶠ[𝓝 t] fun s => 1 - s :=
      (eventually_lt_nhds h).mono fun s hs => max_eq_right (by linarith)
    exact ((differentiableAt_const _).sub differentiableAt_id).congr_of_eventuallyEq hev
  · have hev : (fun s : ℝ => max 0 (1 - s)) =ᶠ[𝓝 t] fun _ => (0 : ℝ) :=
      (eventually_gt_nhds h).mono fun s hs => max_eq_left (by linarith)
    exact (differentiableAt_const _).congr_of_eventuallyEq hev

private theorem tent_tendsto : Tendsto (fun s : ℝ => max 0 (1 - s)) atTop (𝓝 0) :=
  tendsto_const_nhds.congr'
    ((eventually_ge_atTop 1).mono fun s hs => (max_eq_left (by linarith)).symm)

private theorem tent_C0_integrable :
    IntegrableOn (fun t => 1 / √t * thm_13_2_1_etaBar (fun s : ℝ => max 0 (1 - s)) t ^ 2)
      (Ioi 0) := by
  simp only [etaBar_tent]
  rw [← Ioc_union_Ioi_eq_Ioi zero_le_one]
  refine IntegrableOn.union ?_ ?_
  · have hint : IntegrableOn (fun t : ℝ => t ^ (-(1 / 2) : ℝ)) (Ioc 0 1) :=
      (intervalIntegrable_iff_integrableOn_Ioc_of_le zero_le_one).1
        (intervalIntegral.intervalIntegrable_rpow' (by norm_num))
    refine hint.mono' ?_ ?_
    · exact (by fun_prop : Measurable fun t : ℝ => 1 / √t * max 0 (1 - t) ^ 2).aestronglyMeasurable
    · filter_upwards [ae_restrict_mem measurableSet_Ioc] with t ht
      have ht0 : 0 < t := ht.1
      have hm1 : max 0 (1 - t) ≤ 1 := max_le (by norm_num) (by linarith)
      have hsq : max 0 (1 - t) ^ 2 ≤ 1 := by
        have hm0 : 0 ≤ max 0 (1 - t) := le_max_left _ _
        nlinarith
      have he : t ^ (-(1 / 2) : ℝ) = 1 / √t := by
        rw [Real.rpow_neg ht0.le, ← Real.sqrt_eq_rpow, one_div]
      rw [Real.norm_eq_abs, abs_of_nonneg (by positivity), he]
      have : 0 < 1 / √t := by positivity
      nlinarith
  · refine integrableOn_zero.congr_fun (fun t ht => ?_) measurableSet_Ioi
    have ht1 : 1 < t := ht
    simp [max_eq_left (by linarith : 1 - t ≤ 0)]

private theorem tent_C1_integrable :
    IntegrableOn
      (fun t => Real.log t / √t * thm_13_2_1_etaBar (fun s : ℝ => max 0 (1 - s)) t ^ 2)
      (Ioi 1) := by
  refine integrableOn_zero.congr_fun (fun t ht => ?_) measurableSet_Ioi
  have ht1 : 1 < t := ht
  simp [etaBar_tent, max_eq_left (by linarith : 1 - t ≤ 0)]

private theorem integrable_phi' : Integrable Helfgott.phi := by
  have h := integrable_rpow_mul_exp_neg_mul_sq (b := 1 / 2) (by norm_num) (s := 2) (by norm_num)
  refine h.congr (Filter.Eventually.of_forall fun t => ?_)
  simp only [Helfgott.phi, Real.rpow_two]
  ring_nf

/-- **The hypotheses of `thm_13_2_1` are consistent**, for the book's own data of Ch. 14:
`κ = 49` (`TernaryGoldbach.Helfgott.κ`), `φ(t) = t²e^{-t²/2}` (`TernaryGoldbach.Helfgott.phi`,
so `η_*` is the repo's `etaStar`, `thm_13_2_1_etaStar_repo`), `r₀ = 150000`
(`TernaryGoldbach.Helfgott.r₀`), `x = 49·10³⁰` (so `r₁ = 3.75·10⁷`), and the tent
`η₊(t) = max(0, 1 − t)` (with `η₊(0) = 1`, `φ(1) > 0`). So `thm_13_2_1` is not vacuous. -/
theorem thm_13_2_1_hyps_satisfiable :
    ∃ (κ x : ℝ) (φ ηp : ℝ → ℝ) (r₀ : ℝ),
      1 ≤ κ ∧ (10 : ℝ) ^ 25 * κ ≤ x ∧
      ContinuousOn φ (Ici 0) ∧ (∀ t, 0 ≤ t → 0 ≤ φ t) ∧ IntegrableOn φ (Ici 0) ∧
      (∀ t, 0 ≤ t → 0 ≤ ηp t) ∧ BddAbove (ηp '' Ici 0) ∧
      (∃ F : Finset ℝ, ∀ t, 0 < t → t ∉ F → DifferentiableAt ℝ ηp t) ∧
      Tendsto ηp atTop (𝓝 0) ∧
      IntegrableOn (fun t => 1 / √t * thm_13_2_1_etaBar ηp t ^ 2) (Ioi 0) ∧
      IntegrableOn (fun t => Real.log t / √t * thm_13_2_1_etaBar ηp t ^ 2) (Ioi 1) ∧
      (10 : ℝ) ^ 5 ≤ r₀ ∧ r₀ < thm_13_2_1_r₁ κ x ∧
      0 < φ 1 ∧ ηp 0 = 1 := by
  refine ⟨Helfgott.κ, 49 * 10 ^ 30, Helfgott.phi, fun s => max 0 (1 - s), Helfgott.r₀,
    ?_, ?_, ?_, ?_, integrable_phi'.integrableOn, fun t _ => le_max_left _ _, ?_,
    ⟨{1}, fun t _ ht => tent_differentiableAt (by simpa using ht)⟩, tent_tendsto,
    tent_C0_integrable, tent_C1_integrable, ?_, ?_, ?_, ?_⟩
  · norm_num [Helfgott.κ]
  · norm_num [Helfgott.κ]
  · exact (by unfold Helfgott.phi; fun_prop : Continuous Helfgott.phi).continuousOn
  · intro t _; unfold Helfgott.phi; positivity
  · exact ⟨1, by rintro _ ⟨t, ht, rfl⟩; exact max_le (by norm_num) (by linarith [ht.out])⟩
  · norm_num [Helfgott.r₀]
  · have e : ((49 : ℝ) * 10 ^ 30 / Helfgott.κ) ^ (4 / 15 : ℝ) = 10 ^ 8 := by
      rw [show (49 : ℝ) * 10 ^ 30 / Helfgott.κ = 10 ^ 30 by norm_num [Helfgott.κ],
        ← Real.rpow_natCast, ← Real.rpow_mul (by norm_num)]
      norm_num
    simp only [thm_13_2_1_r₁, e, Helfgott.r₀]
    norm_num
  · unfold Helfgott.phi; positivity
  · norm_num

end Companion.Book
