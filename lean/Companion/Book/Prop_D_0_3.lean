import TernaryGoldbach

/-!
# [H, Proposition D.0.3]: odd `5 ≤ n ≤ n₀` are sums of three primes (RH to `H`) — false at `n = 5`

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2,
Appendix D ("Checking small `n` by checking zeros of `ζ(s)`"), printed page 306
(<https://arxiv.org/pdf/1501.05438v2#page=316>), label `prop:gosto`. A local LaTeX build numbers
it D.0.1; the arXiv PDF prints D.0.3. It is Prop. C.1 of arXiv:1312.7748v2, identical up to
punctuation (a dash before the first `H` became a pair of parentheses).

> **Proposition D.0.3.** Every odd integer `5 ≤ n ≤ n₀` is the sum of three primes, where
> `n₀ = 5.90698·10²⁹` if [GD04] is used (`H = 2.44·10¹²`),
> `n₀ = 6.15697·10²⁸` if ZetaGrid results are used (`H = 2.419·10¹¹`),
> `n₀ = 1.23163·10²⁷` if [Plaa] (Platt) is used (`H = 3.061·10¹⁰`).

`H` is the height up to which the cited computation verified the Riemann hypothesis. Earlier in
the appendix (p. 305) the book defines such a verification: every non-trivial zero `z` of `ζ` with
`ℑz ≤ H` has `ℜz = 1/2`. The proof calls the case `n ≤ 4·10¹⁸ + 3` immediate from binary Goldbach
up to `4·10¹⁸` [OeSHP14] (that is, `n = 3 + (n − 3)`). Above that it finds a prime `p` in
`[n − 4 − (n − 4)/Δ, n − 4]`, so that `n − p` is even and lies in `[4, 4·10¹⁸]`. The values of `Δ`
come from Ramaré–Saouter [RS03] and from Ramaré's tables [Ramd] for the height `H`. The book then
remarks that Platt's rigorous results suffice for all odd `n ≤ 10²⁷`.

**The printed statement is false at `n = 5`.** `5` is odd and `5 ≤ n₀` in all three cases, but a
sum of three primes is at least `2 + 2 + 2 = 6`. The proof's first step also needs `n ≥ 7`, since
`n − 3 = 2` is not a sum of two primes. The intended range is `5 < n`, as in Theorem 1.1.1
("greater than `5`"). This is a typo, and it is already in the 2013 version. Each case's conclusion
is false outright, whatever is assumed. So each case of the printed statement amounts to saying that
the cited verification is wrong, and the whole statement is equivalent to the failure of RH below
height `3.061·10¹⁰` (`prop_D_0_3_iff_not_rh`).

**What the formalization proves.** `TernaryGoldbach.Helfgott.ternaryGoldbachUpTo_1e27`
(`TernaryGoldbach/Helfgott/SmallCases.lean`, re-exported as
`TernaryGoldbach.Helfgott.ternaryGoldbachUpTo`) proves `TernaryGoldbachUpTo (10 ^ 27)`: every odd
`5 < n ≤ 10²⁷` is a sum of three primes. Its only hypothesis is `[Fact BinaryGoldbachInput]`
([OeSHP14]). The route starts as in Appendix D: `n = 3 + (n − 3)` up to `4·10¹⁸ + 3`, then a prime
in `[n − 4·10¹⁸, n − 4]`. That prime comes from a ladder of Proth primes up to `10²⁷`, checked by the
Lean kernel (`TernaryGoldbach.Ladder.ladder_prime`), as in [H, §1.6]. The ladder replaces [RS03],
[Ramd] and the RH verification. So the Lean theorem gives the book's closing remark (all odd
`n ≤ 10²⁷`) with `5 < n`, and without any RH input (`prop_D_0_3_remark_iff_formal`). It does not
reach the part `(10²⁷, 1.23163·10²⁷]` of case (c).
The formalization covers that range by the circle method instead
(`TernaryGoldbach.Helfgott.ternaryGoldbachFrom`), and its main theorem gives the corrected
proposition (`prop_D_0_3_corrected_holds`).

**Relation: refuted.** This is certified here by three theorems.
* `prop_D_0_3_upTo_iff`. For every `n₀`, the printed conclusion "every odd integer `5 ≤ n ≤ n₀` is
  the sum of three primes" holds iff the corrected conclusion (`5 < n`) holds and `n₀ < 5`. So
  `n = 5` is the only defect, and the printed conclusion fails for each printed `n₀`
  (`prop_D_0_3_upTo_false`), whatever is assumed. Under a reading of "if [GD04] is used" etc. as
  mere provenance, with no hypothesis, this already refutes the statement unconditionally.
* `prop_D_0_3_iff_not_rh : prop_D_0_3 ↔ ¬ prop_D_0_3_rhUpTo 3.061e10`.
* `prop_D_0_3_false : ¬ prop_D_0_3`, given as a `Fact` that RH holds up to `3.061·10¹⁰`, the
  printed height of case (c). This is Platt's verification, which the book uses and calls rigorous.
  By the previous item, `¬ prop_D_0_3` is equivalent to this hypothesis, so it cannot be weakened.
  The repository's hypotheses do not provide it: `PlattGRH` gives RH only up to height `10⁸`
  (`TernaryGoldbach.Explicit.rh_upto_1e8`).
  `prop_D_0_3_rhUpTo_of_RH` checks that it follows from Mathlib's `RiemannHypothesis`.

Three further theorems concern the corrected statement `prop_D_0_3_corrected` (`5 < n`, otherwise
as printed).
* `prop_D_0_3_corrected_holds`: it holds given the repository's three hypotheses. By the main theorem
  `ternary_goldbach_of_hypotheses` every odd `n > 5` is a sum of three primes, so the case
  hypotheses are not even needed.
* `prop_D_0_3_corrected_implies_formal`: its case (c), with its own input (RH up to `3.061·10¹⁰`),
  implies the statement of `ternaryGoldbachUpTo_1e27`, taken with `type_of%`, because
  `10²⁷ ≤ 1.23163·10²⁷`. Conversely, the Lean theorem does not give case (c): it stops at `10²⁷`.
  So neither conditional statement contains the other. The book's case (c) has an RH input and the
  larger range, and its conclusion contains the Lean one; the Lean theorem needs no RH input.
* `prop_D_0_3_remark_iff_formal`: the Lean statement is exactly "[OeSHP14] implies that every odd
  `5 < n ≤ 10²⁷` is a sum of three primes".

**Numerics (Python, not part of the proof).** The printed `n₀` agree with the proof. Take the last
`Δ` of each case (`147674531294`, `15392435100`, `307908668`). Then `(4·10¹⁸ − 4)·Δ + 4` is
`5.906981…·10²⁹`, `6.156974…·10²⁸` and `1.231634…·10²⁷`, and the printed `n₀` are these values
rounded down to six significant figures. The intermediate claims of the proof also hold:
`e⁶⁷/52211882224`, `e⁶⁸/146869130682`, `e⁶⁶/13861486834` and `e⁶²/307779681` are all
`≤ 4·10¹⁸ − 4`, and `(4·10¹⁸ − 4)·28314000 ≥ 1.1325·10²⁶ > e⁵⁹`.

**Removed at P (192ca57):** `prop_D_0_3_RHUpTo_of_platt` (RH up to `3.061·10¹⁰` implies the
repository's `RHUpTo`) was removed, and `prop_D_0_3_rhUpTo_iff_RHUpTo` became
`prop_D_0_3_rhUpTo_iff_RHBelow`: at P the repository has no hypothesis `RHUpTo`.
-/

namespace Companion.Book

open TernaryGoldbach

/-- **RH verified up to height `H`**, as defined in [H, App. D, p. 305]: every non-trivial zero `ρ`
of the Riemann zeta function with `|ℑρ| ≤ H` lies on the critical line `ℜρ = 1/2`.

Transcription choices:
* "non-trivial zeros": the zeros of Mathlib's `riemannZeta` in the critical strip `0 < ℜρ < 1`, as
  in the repository's `TernaryGoldbach.Explicit.RHBelow`. (`ζ` has no zeros with `ℜs ≥ 1`, and
  its zeros with `ℜs ≤ 0` are the trivial zeros `−2, −4, …`.)
* "up to a height `H` (meaning: `ℑz ≤ H`)": we read `|ℑρ| ≤ H`. Taken literally, `ℑz ≤ H` would
  also cover every zero below the real axis. The zeros are symmetric under complex conjugation, so
  the condition would then be the full Riemann hypothesis, which is not what a numerical
  verification checks. By the same symmetry, `|ℑρ| ≤ H` is equivalent to the usual `0 ≤ ℑρ ≤ H`.
* This is the repository's `RHBelow H` (`prop_D_0_3_rhUpTo_iff_RHBelow`). -/
def prop_D_0_3_rhUpTo (H : ℝ) : Prop :=
  ∀ ρ : ℂ, riemannZeta ρ = 0 → 0 < ρ.re → ρ.re < 1 → |ρ.im| ≤ H → ρ.re = 1 / 2

/-- The conclusion of [H, Prop. D.0.3] for a given `n₀`, as printed: *every odd integer
`5 ≤ n ≤ n₀` is the sum of three primes.*

Transcription choices (as for [H, Theorem 1.1.1] in `Companion/Book/Thm_1_1_1.lean`):
* "odd integer": `n : ℤ` with Mathlib's `Odd n`. The lower bound is `5 ≤ n`, with `≤` as printed.
  The upper bound `n ≤ n₀` is compared in `ℝ`, because `n₀` is given as a real number (all three
  printed values are in fact integers).
* "the sum of three primes": `n = p + q + r` for primes `p q r : ℕ` (`Nat.Prime`, i.e. the
  positive primes `2, 3, 5, …`), not necessarily distinct, cast to `ℤ`. -/
def prop_D_0_3_upTo (n₀ : ℝ) : Prop :=
  ∀ n : ℤ, Odd n → 5 ≤ n → (n : ℝ) ≤ n₀ →
    ∃ p q r : ℕ, p.Prime ∧ q.Prime ∧ r.Prime ∧ n = p + q + r

/-- **[H, Proposition D.0.3]** as printed: *every odd integer `5 ≤ n ≤ n₀` is the sum of three
primes, where `n₀ = 5.90698·10²⁹` if [GD04] is used (`H = 2.44·10¹²`), `6.15697·10²⁸` if ZetaGrid
results are used (`H = 2.419·10¹¹`), and `1.23163·10²⁷` if [Plaa] is used (`H = 3.061·10¹⁰`).*

Transcription choices:
* The three cases are joined by `∧`. In each case, "if [ref] is used (`H = …`)" becomes the
  hypothesis that RH holds up to that height (`prop_D_0_3_rhUpTo H`), since that is the result of
  the cited computation; each `n₀` goes with its own `H`. The heights are the ones printed in the
  statement. For [GD04] the text before the statement gives `2.44599·10¹²`, but the statement
  prints `2.44·10¹²`; that hypothesis is weaker, and it is the one used here.
* The conclusion is `prop_D_0_3_upTo n₀`, with the printed lower bound `5 ≤ n`.
* The proof also uses binary Goldbach up to `4·10¹⁸` [OeSHP14], the short-interval theorem of
  [RS03] and Ramaré's tables [Ramd]. The statement does not mention them, so they are not hypotheses
  here; the book treats them as established. This does not affect the refutation, because each
  conclusion fails at `n = 5` and no further input can change that (`prop_D_0_3_upTo_false`).
* The constants are as printed: `2.44e12`, `2.419e11`, `3.061e10`, `5.90698e29`, `6.15697e28` and
  `1.23163e27`, all real numbers. -/
def prop_D_0_3 : Prop :=
  (prop_D_0_3_rhUpTo 2.44e12 → prop_D_0_3_upTo 5.90698e29) ∧
    (prop_D_0_3_rhUpTo 2.419e11 → prop_D_0_3_upTo 6.15697e28) ∧
    (prop_D_0_3_rhUpTo 3.061e10 → prop_D_0_3_upTo 1.23163e27)

/-- The corrected conclusion: `prop_D_0_3_upTo` with `5 < n` in place of the printed `5 ≤ n`. This
is the range of [H, Theorem 1.1.1] and of the repository's `TernaryGoldbachUpTo`. -/
def prop_D_0_3_upTo' (n₀ : ℝ) : Prop :=
  ∀ n : ℤ, Odd n → 5 < n → (n : ℝ) ≤ n₀ →
    ∃ p q r : ℕ, p.Prime ∧ q.Prime ∧ r.Prime ∧ n = p + q + r

/-- [H, Proposition D.0.3] **corrected**: `prop_D_0_3` with `5 < n` in place of `5 ≤ n`, and
otherwise as printed. This is what the book's proof establishes. -/
def prop_D_0_3_corrected : Prop :=
  (prop_D_0_3_rhUpTo 2.44e12 → prop_D_0_3_upTo' 5.90698e29) ∧
    (prop_D_0_3_rhUpTo 2.419e11 → prop_D_0_3_upTo' 6.15697e28) ∧
    (prop_D_0_3_rhUpTo 3.061e10 → prop_D_0_3_upTo' 1.23163e27)

/-! ### The printed statement is false -/

/-- `5` is not the sum of three primes: every prime is at least `2`, and `2 + 2 + 2 = 6 > 5`. -/
theorem prop_D_0_3_five_not_sum :
    ¬ ∃ p q r : ℕ, p.Prime ∧ q.Prime ∧ r.Prime ∧ (5 : ℤ) = p + q + r := by
  rintro ⟨p, q, r, hp, hq, hr, h⟩
  have := hp.two_le
  have := hq.two_le
  have := hr.two_le
  omega

/-- The printed conclusion is the corrected one (`5 < n`) plus the case `n = 5`. Since `5` is not a
sum of three primes, it holds exactly when the corrected conclusion holds and `n₀ < 5`. So `n = 5`
is the only defect of the printed conclusion. -/
theorem prop_D_0_3_upTo_iff (n₀ : ℝ) : prop_D_0_3_upTo n₀ ↔ prop_D_0_3_upTo' n₀ ∧ n₀ < 5 := by
  constructor
  · intro h
    refine ⟨fun n hn h5 hle => h n hn h5.le hle, ?_⟩
    by_contra h5
    exact prop_D_0_3_five_not_sum (h 5 ⟨2, by norm_num⟩ le_rfl (by exact_mod_cast not_lt.1 h5))
  · rintro ⟨h, h5⟩ n hn hn5 hle
    rcases hn5.lt_or_eq with hlt | rfl
    · exact h n hn hlt hle
    · exfalso
      have : ((5 : ℤ) : ℝ) < 5 := hle.trans_lt h5
      norm_num at this

/-- Each printed conclusion is false whatever is assumed: for every `n₀ ≥ 5`, in particular for
`5.90698·10²⁹`, `6.15697·10²⁸` and `1.23163·10²⁷`, the counterexample being `n = 5`. -/
theorem prop_D_0_3_upTo_false {n₀ : ℝ} (h : 5 ≤ n₀) : ¬ prop_D_0_3_upTo n₀ := fun hu =>
  absurd ((prop_D_0_3_upTo_iff n₀).1 hu).2 (not_lt.2 h)

/-- RH up to height `H` implies RH up to any lower height. -/
theorem prop_D_0_3_rhUpTo_mono {H H' : ℝ} (hH : H' ≤ H) (h : prop_D_0_3_rhUpTo H) :
    prop_D_0_3_rhUpTo H' :=
  fun ρ hz h0 h1 him => h ρ hz h0 h1 (him.trans hH)

/-- RH up to height `H` is the repository's `TernaryGoldbach.Explicit.RHBelow H`. -/
theorem prop_D_0_3_rhUpTo_iff_RHBelow (H : ℝ) : prop_D_0_3_rhUpTo H ↔ Explicit.RHBelow H :=
  Iff.rfl

/-- Sanity check of the case hypotheses: Mathlib's `RiemannHypothesis` implies RH up to every
height `H`. So the hypotheses of `prop_D_0_3` are weakenings of the Riemann hypothesis; in
particular none of them can be refuted unless RH itself can. -/
theorem prop_D_0_3_rhUpTo_of_RH (hRH : RiemannHypothesis) (H : ℝ) : prop_D_0_3_rhUpTo H := by
  intro ρ hz h0 h1 _
  refine hRH ρ hz ?_ ?_
  · rintro ⟨n, rfl⟩
    have : (-2 * ((n : ℂ) + 1)).re = -2 * ((n : ℝ) + 1) := by simp
    rw [this] at h0
    have : (0 : ℝ) ≤ n := Nat.cast_nonneg n
    linarith
  · rintro rfl
    simp at h1

/-- **The printed statement is equivalent to the failure of RH below height `3.061·10¹⁰`.** Each
case's conclusion is false (`prop_D_0_3_upTo_false`), so each case says that the cited verification
is wrong. RH up to `2.44·10¹²` or up to `2.419·10¹¹` implies RH up to `3.061·10¹⁰`. -/
theorem prop_D_0_3_iff_not_rh : prop_D_0_3 ↔ ¬ prop_D_0_3_rhUpTo 3.061e10 := by
  constructor
  · rintro ⟨-, -, hc⟩ hrh
    exact prop_D_0_3_upTo_false (by norm_num) (hc hrh)
  · intro hn
    exact ⟨fun ha => absurd (prop_D_0_3_rhUpTo_mono (by norm_num) ha) hn,
      fun hb => absurd (prop_D_0_3_rhUpTo_mono (by norm_num) hb) hn, fun hc => absurd hc hn⟩

/-- **[H, Proposition D.0.3] is false as printed**, given RH up to the height `3.061·10¹⁰` of its
case (c). That is Platt's verification [Plaa], which the book uses and calls rigorous. The
counterexample is `n = 5`. By `prop_D_0_3_iff_not_rh` the hypothesis is necessary. -/
theorem prop_D_0_3_false [Fact (prop_D_0_3_rhUpTo 3.061e10)] : ¬ prop_D_0_3 := fun h =>
  prop_D_0_3_iff_not_rh.1 h Fact.out

/-! ### The corrected statement and the formalization -/

/-- The corrected conclusion up to a natural number `N` is the repository's `TernaryGoldbachUpTo N`,
which is stated over `ℕ`. -/
theorem prop_D_0_3_upTo'_iff (N : ℕ) : prop_D_0_3_upTo' N ↔ TernaryGoldbachUpTo N := by
  constructor
  · intro h n hn h5 hle
    obtain ⟨p, q, r, hp, hq, hr, hs⟩ :=
      h n ((Int.odd_coe_nat n).2 hn) (by exact_mod_cast h5) (by exact_mod_cast hle)
    exact ⟨p, q, r, hp, hq, hr, by exact_mod_cast hs.symm⟩
  · intro h n hn h5 hle
    lift n to ℕ using (by omega)
    obtain ⟨p, q, r, hp, hq, hr, hs⟩ :=
      h n ((Int.odd_coe_nat n).1 hn) (by exact_mod_cast h5) (by exact_mod_cast hle)
    exact ⟨p, q, r, hp, hq, hr, by exact_mod_cast hs.symm⟩

/-- **The corrected statement holds**, given the repository's three hypotheses as `Fact` instances.
The proof is the Lean main theorem `TernaryGoldbach.ternary_goldbach_of_hypotheses`: every odd
`n > 5` is a sum of three primes, so each case holds even without its RH hypothesis. The
App. D-style theorem `ternaryGoldbachUpTo_1e27` alone would not do, because it stops at
`10²⁷ < 1.23163·10²⁷`. -/
theorem prop_D_0_3_corrected_holds [Fact PlattGRH] [Fact BinaryGoldbachInput]
    [Fact RamareMoebius] : prop_D_0_3_corrected := by
  have hS : Statement :=
    ternary_goldbach_of_hypotheses Fact.out Fact.out Fact.out
  have key : ∀ n₀ : ℝ, prop_D_0_3_upTo' n₀ := by
    intro n₀ n hn h5 _
    lift n to ℕ using (by omega)
    obtain ⟨p, q, r, hp, hq, hr, hs⟩ := hS n ((Int.odd_coe_nat n).1 hn) (by exact_mod_cast h5)
    exact ⟨p, q, r, hp, hq, hr, by exact_mod_cast hs.symm⟩
  exact ⟨fun _ => key _, fun _ => key _, fun _ => key _⟩

/-- **The corrected case (c), with its own input, implies the Lean theorem's statement** (taken with
`type_of%`), because `10²⁷ ≤ 1.23163·10²⁷`. The proof uses only case (c) and RH up to `3.061·10¹⁰`,
not the `Fact` hypotheses of the Lean statement. -/
theorem prop_D_0_3_corrected_implies_formal :
    prop_D_0_3_corrected → prop_D_0_3_rhUpTo 3.061e10 →
      type_of% @TernaryGoldbach.Helfgott.ternaryGoldbachUpTo_1e27 := by
  rintro ⟨-, -, hc⟩ hrh _
  refine (prop_D_0_3_upTo'_iff (10 ^ 27)).1 fun n hn h5 hle => hc hrh n hn h5 (hle.trans ?_)
  norm_num

/-- **The Lean theorem is the book's closing remark**, "the rigorous results in [Plaa] are enough
to show the result for all odd `n ≤ 10²⁷`", with `5 < n` and with its one input made explicit:
[OeSHP14] (`BinaryGoldbachInput`). It needs no RH input. The statement of
`ternaryGoldbachUpTo_1e27` is taken with `type_of%`. -/
theorem prop_D_0_3_remark_iff_formal :
    (BinaryGoldbachInput → prop_D_0_3_upTo' 1e27) ↔
      type_of% @TernaryGoldbach.Helfgott.ternaryGoldbachUpTo_1e27 := by
  have e : prop_D_0_3_upTo' 1e27 ↔ TernaryGoldbachUpTo (10 ^ 27) := by
    rw [← prop_D_0_3_upTo'_iff, show ((10 ^ 27 : ℕ) : ℝ) = 1e27 by norm_num]
  constructor
  · intro h h1
    exact e.1 (h h1.out)
  · intro h a
    exact e.2 (@h ⟨a⟩)

end Companion.Book
