import TernaryGoldbach

/-!
# [H, (5.31)]: the bound on the triple sum `∑_{s ≤ S, (s,v)=1} (1/s) ∫_{1/2}^1 g_v(uS/s) du`

**What [H] states** (p. 91, display (5.31), <https://arxiv.org/pdf/1501.05438v2#page=101>, and its
continuation on p. 92, <https://arxiv.org/pdf/1501.05438v2#page=102>). For `v ∈ {1, 2}` let
`g_v` be as in [H, Lemma 5.1.2] (p. 84) and let `T_v(S)` be the triple sum [H, (5.28)] (p. 89),
```
  T_v(S) = ∑_{s ≤ S, (s,v)=1} (1/s) ∫_{1/2}^1 g_v(uS/s) du .
```
"Thus, for `S ≥ 100000`", (5.31) says `T_1(S) ≤ 0.36393` and `T_2(S) ≤ 0.37273`. The next
paragraph adds that "(5.31) holds not just for `S ≥ 100000` but also for `40 ≤ S < 100000`
(if `v = 1`) or `16 ≤ S < 100000` (if `v = 2`)". So [H] asserts (5.31) for `v = 1, S ≥ 40` and
for `v = 2, S ≥ 16`. This is the range the book uses later: (5.35) sets `H_1(S) = 0.22125` for
`S ≥ 40` and `H_2(S) = 0.15107 = (4/π²)·0.37273` (rounded up) for `S ≥ 16`. The 2013 preprint
(arXiv:1205.5252v4, (4.31)) has the same text; it writes `gcd(s,v)` for `(s,v)`.

**What the formalization proves.** `TernaryGoldbach.MinorArcs.T2_le'` (`MinorArcs/T2Bound.lean`):
`T2 S ≤ 0.37273` for `16 ≤ S`. This is only the case `v = 2`. The formalization uses `v = 2`
everywhere (its `S₁`, `g2` and `T2` all have odd variables), and so does the book from Chapter 6
on ("We set `v = 2`", [H, Ch. 6, introduction, p. 101]). The `v = 1` half of (5.31) is not
formalized, and neither the book's main line nor the formalization uses it. `T2_le'` takes one
`Fact` hypothesis, `RamareMoebius` (Ramaré's bound on `∑ μ(n)/n`).

**Relation (status: implied, i.e. the Lean result is weaker).**
* `TBook_two` (with `gBook_two`): the repo's `T2` (and `g2`) *is* the book's `T_v` (and `g_v`) at
  `v = 2`. The proof unfolds the definitions; `(n, 2) = 1 ↔ n odd`.
* `eq_5_31_implies_formal : eq_5_31 → type_of% @T2_le'`: the book's statement implies the formal
  theorem.
* `eq_5_31_v2_holds`: the formalization proves the whole `v = 2` half of (5.31), in the full range
  `S ≥ 16` that the book claims. `eq_5_31_iff_v1`: under the formalization's hypotheses, (5.31)
  is *equivalent* to its `v = 1` half. So the Lean result is weaker than (5.31) by exactly the
  `v = 1` case, and by nothing else.
* `eq_5_31_iff_as_printed`: the two printed range clauses ("for `S ≥ 100000`", then
  "also for `40 ≤ S < 100000` (`v = 1`) or `16 ≤ S < 100000` (`v = 2`)") combine to the ranges
  used in `eq_5_31`.

**Numerical remark (not part of the certification).** A floating-point evaluation of the
book's `T_v`, written independently of the repo, gives `max T_1(n) = 0.3634958` (at `n = 40`)
over the integers `n ∈ [40, 10⁵]`, and `max T_2(n) = 0.3712486` (at `n = 16`) over
`n ∈ [16, 10⁵]`. On `[n, n+1)`, `T_v(S) = A_n + B_n/S`, and `T_v` is continuous, so these
maxima cover all real `S` in those ranges. The large-`S` values are `T_1 ≈ 0.362485` and
`T_2 ≈ 0.360582`. The book's main terms `0.362482…` and `0.360576…` were reproduced. One step
below the thresholds the bounds fail: `T_1(39) ≈ 0.36402 > 0.36393` and
`T_2(15) ≈ 0.37494 > 0.37273`. So the `v = 1` half is very likely true (it is not refuted
here), and the thresholds `40` and `16` cannot be lowered to `39` and `15`.
-/

open Finset
open scoped ArithmeticFunction.Moebius ArithmeticFunction.sigma

namespace Companion.Book

/-- The book's `g_v(x)` [H, Lemma 5.1.2, p. 84]:
`g_v(x) = ∑_{r₁ ≤ x} ∑_{r₂ ≤ x}, (r₁,r₂)=1, (r₁r₂,v)=1, μ(r₁)μ(r₂)/(σ(r₁)σ(r₂))`.

Transcription: `r₁, r₂` run over the positive integers `≤ x`. That is `Finset.Icc 1 ⌊x⌋₊`, for
every real `x` (see `mem_Icc_one_floor`). `(a, b) = 1` is `Nat.Coprime a b`. `μ` is the Möbius
function, and `σ = σ₁` is the sum of divisors ([H, §2], "`σ(n)` the sum of the divisors of `n`").
The book only uses `v ∈ {1, 2}`; the definition makes sense for every `v : ℕ`. At `v = 2` it is
the repo's `TernaryGoldbach.MinorArcs.g2` (`gBook_two`). -/
noncomputable def gBook (v : ℕ) (x : ℝ) : ℝ :=
  ∑ r₁ ∈ Icc 1 ⌊x⌋₊, ∑ r₂ ∈ Icc 1 ⌊x⌋₊,
    if Nat.Coprime r₁ r₂ ∧ Nat.Coprime (r₁ * r₂) v then
      (μ r₁ : ℝ) * μ r₂ / ((σ 1 r₁ : ℝ) * σ 1 r₂) else 0

/-- The book's triple sum [H, (5.28), p. 89], the left side of (5.31):
`T_v(S) = ∑_{s ≤ S, (s,v)=1} (1/s) ∫_{1/2}^1 g_v(uS/s) du`.

Transcription: `s` runs over the positive integers `≤ S` (`Finset.Icc 1 ⌊S⌋₊`) with
`(s, v) = 1`. The integral is the interval integral over `[1/2, 1]`. The integrand is a step
function of `u`, so it agrees with the book's Riemann integral. At `v = 2` this is the repo's
`TernaryGoldbach.MinorArcs.T2` (`TBook_two`). -/
noncomputable def TBook (v : ℕ) (S : ℝ) : ℝ :=
  ∑ s ∈ (Icc 1 ⌊S⌋₊).filter (fun s => Nat.Coprime s v),
    (1 / s : ℝ) * ∫ u in (1 / 2 : ℝ)..1, gBook v (u * S / s)

/-- **[H, (5.31)]** as printed (p. 91, with its range extension on p. 92):
`T_1(S) ≤ 0.36393` for `S ≥ 40`, and `T_2(S) ≤ 0.37273` for `S ≥ 16`.

Transcription choices.
* Both cases of the display are kept: `v = 1` (constant `0.36393`) and `v = 2` (constant
  `0.37273`). The constants are exactly the printed decimals, as real numbers.
* The ranges: the display is introduced by "Thus, for `S ≥ 100000`". The next paragraph says it
  also holds for `40 ≤ S < 100000` if `v = 1` and for `16 ≤ S < 100000` if `v = 2`. Taken
  together, the book claims (5.31) for `S ≥ 40` (`v = 1`) and `S ≥ 16` (`v = 2`). This is what
  is stated here. `eq_5_31_iff_as_printed` proves it equivalent to the conjunction of the two
  printed clauses, each rendered literally.
* `S` is a real number (in [H] it is `x/(WU)`). `T_v` is the book's object `TBook` (with
  `gBook`), not the repo's `T2`. `TBook 2 = T2` is a theorem here (`TBook_two`), and `TBook 1`
  has no counterpart in the repo. -/
def eq_5_31 : Prop :=
  (∀ S : ℝ, 40 ≤ S → TBook 1 S ≤ 0.36393) ∧
    (∀ S : ℝ, 16 ≤ S → TBook 2 S ≤ 0.37273)

/-! ### The book's objects versus the repo's -/

/-- The encoding of "`r` a positive integer with `r ≤ x`" by `Finset.Icc 1 ⌊x⌋₊`, valid for every
real `x` (also `x < 1`, where both sides are empty). -/
theorem mem_Icc_one_floor {x : ℝ} {r : ℕ} : r ∈ Icc 1 ⌊x⌋₊ ↔ 1 ≤ r ∧ (r : ℝ) ≤ x := by
  rw [mem_Icc]
  constructor
  · rintro ⟨h1, h2⟩
    exact ⟨h1, (Nat.le_floor_iff' (by omega)).1 h2⟩
  · rintro ⟨h1, h2⟩
    exact ⟨h1, (Nat.le_floor_iff' (by omega)).2 h2⟩

/-- Sanity check that the book's `g_v` is not degenerate: `g_v(1) = μ(1)²/σ(1)² = 1`. -/
theorem gBook_one (v : ℕ) : gBook v 1 = 1 := by
  simp [gBook, ArithmeticFunction.sigma_apply]

/-- The repo's `g₂` is the book's `g_v` at `v = 2`: `(r₁r₂, 2) = 1 ↔ r₁r₂` odd. -/
theorem gBook_two : gBook 2 = TernaryGoldbach.MinorArcs.g2 := by
  funext x
  unfold gBook TernaryGoldbach.MinorArcs.g2
  refine sum_congr rfl fun r₁ _ => sum_congr rfl fun r₂ _ => ?_
  exact if_congr (and_congr Iff.rfl Nat.coprime_two_right) rfl rfl

/-- **The repo's `T₂` is the book's `T_v` at `v = 2`** ([H, (5.28)]): `(s, 2) = 1 ↔ s` odd, and
`gBook_two`. -/
theorem TBook_two : TBook 2 = TernaryGoldbach.MinorArcs.T2 := by
  funext S
  unfold TBook TernaryGoldbach.MinorArcs.T2
  rw [sum_filter, gBook_two]
  exact sum_congr rfl fun s _ => if_congr Nat.coprime_two_right rfl rfl

/-- Sanity check against the book's example on p. 92. There, the computed upper bound
`G_v(S) ≥ T_v(S)` equals `1 - 1/S` for `1 ≤ S < 2`. Here the triple sum itself has this value:
`T_v(S) = 1 - 1/S` for `1 ≤ S < 2`, because only `s = 1` contributes and `g_v(uS) = [uS ≥ 1]`.
So `TBook` is not degenerate. -/
theorem TBook_of_lt_two (v : ℕ) {S : ℝ} (h1 : 1 ≤ S) (h2 : S < 2) : TBook v S = 1 - 1 / S := by
  have hS0 : 0 < S := by linarith
  have hfl : ⌊S⌋₊ = 1 := (Nat.floor_eq_iff hS0.le).2 ⟨by simpa using h1, by norm_num; linarith⟩
  -- `g_v(y) = [1 ≤ y]` for `0 ≤ y < 2`
  have hg : ∀ y : ℝ, 0 ≤ y → y < 2 → gBook v y = if 1 ≤ y then 1 else 0 := by
    intro y hy0 hy2
    by_cases hy : 1 ≤ y
    · have : ⌊y⌋₊ = 1 := (Nat.floor_eq_iff hy0).2 ⟨by simpa using hy, by norm_num; linarith⟩
      rw [ite_eq_left hy, ← gBook_one v]
      simp only [gBook, this, Nat.floor_one]
    · have : ⌊y⌋₊ = 0 := Nat.floor_eq_zero.2 (not_le.1 hy)
      simp [gBook, this, hy]
  have hpt : ∀ u ∈ Set.uIcc (1 / 2 : ℝ) 1, gBook v (u * S / ((1 : ℕ) : ℝ)) =
      if 1 / S ≤ u then 1 else 0 := by
    intro u hu
    rw [Set.uIcc_of_le (by norm_num)] at hu
    rw [Nat.cast_one, div_one, hg (u * S) (by nlinarith [hu.1]) (by nlinarith [hu.2])]
    exact if_congr (by rw [div_le_iff₀ hS0, mul_comm]) rfl rfl
  unfold TBook
  rw [hfl, show (Icc 1 1).filter (fun s => Nat.Coprime s v) = {1} by
      rw [Icc_self, filter_singleton, ite_eq_left (Nat.coprime_one_left v)], sum_singleton,
    intervalIntegral.integral_congr hpt,
    TernaryGoldbach.MinorArcs.integral_ite_le ((div_le_one hS0).2 h1),
    max_eq_right (by rw [le_div_iff₀ hS0]; linarith)]
  simp

/-! ### Relation to the formalization -/

/-- **Book ⟹ formal.** [H, (5.31)] implies the formalization's `T2_le'` (`T₂(S) ≤ 0.37273` for
`S ≥ 16`). `T2_le'` is the `v = 2` half of (5.31), with `T2 = TBook 2` (`TBook_two`). The
`Fact` binders of `T2_le'` are not needed for this direction. -/
theorem eq_5_31_implies_formal : eq_5_31 → type_of% @TernaryGoldbach.MinorArcs.T2_le' := by
  intro h _ S hS
  rw [← TBook_two]
  exact h.2 S hS

/-- The `v = 2` half of [H, (5.31)], in the book's full range `S ≥ 16`, *is* proved by the
formalization (from `T2_le'`), under its one `Fact` hypothesis `RamareMoebius`. -/
theorem eq_5_31_v2_holds [Fact TernaryGoldbach.RamareMoebius] : ∀ S : ℝ, 16 ≤ S → TBook 2 S ≤ 0.37273 := by
  intro S hS
  rw [TBook_two]
  exact TernaryGoldbach.MinorArcs.T2_le' hS

/-- Under the formalization's hypotheses, [H, (5.31)] is equivalent to its (unformalized) `v = 1`
half. So the gap between the book's statement and the Lean result is exactly the case `v = 1`. -/
theorem eq_5_31_iff_v1 [Fact TernaryGoldbach.RamareMoebius] :
    eq_5_31 ↔ ∀ S : ℝ, 40 ≤ S → TBook 1 S ≤ 0.36393 :=
  ⟨And.left, fun h => ⟨h, eq_5_31_v2_holds⟩⟩

/-- The range clauses of [H] word for word: "for `S ≥ 100000`" (both cases), then "also for
`40 ≤ S < 100000` (if `v = 1`) or `16 ≤ S < 100000` (if `v = 2`)". Their conjunction is
`eq_5_31`. -/
theorem eq_5_31_iff_as_printed : eq_5_31 ↔
    ((∀ S : ℝ, 100000 ≤ S → TBook 1 S ≤ 0.36393 ∧ TBook 2 S ≤ 0.37273) ∧
      (∀ S : ℝ, 40 ≤ S → S < 100000 → TBook 1 S ≤ 0.36393) ∧
      (∀ S : ℝ, 16 ≤ S → S < 100000 → TBook 2 S ≤ 0.37273)) := by
  constructor
  · rintro ⟨h1, h2⟩
    exact ⟨fun S hS => ⟨h1 S (by linarith), h2 S (by linarith)⟩, fun S hS _ => h1 S hS,
      fun S hS _ => h2 S hS⟩
  · rintro ⟨hbig, h1, h2⟩
    refine ⟨fun S hS => ?_, fun S hS => ?_⟩
    · rcases lt_or_ge S 100000 with h | h
      · exact h1 S hS h
      · exact (hbig S h).1
    · rcases lt_or_ge S 100000 with h | h
      · exact h2 S hS h
      · exact (hbig S h).2

end Companion.Book
