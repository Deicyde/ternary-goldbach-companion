import TernaryGoldbach

/-!
# [H, Theorem 1.1.1]: the ternary Goldbach theorem

**What [H] states.** H. A. Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438v2, Chapter 1,
§1.1 "History and new developments", printed page 3
(<https://arxiv.org/pdf/1501.05438v2#page=13>):

> **Theorem 1.1.1.** Every odd integer greater than `5` can be written as the sum of three primes.

This is the main theorem of the book, and it is stated with no hypotheses. Its proof is §14.4
("Conclusion: proof of main theorem", p. 275). The circle method shows that every odd
`N ≥ 10²⁷` is a sum of three odd primes. The other odd `N` are covered by the Helfgott–Platt
computer verification up to `8.875·10³⁰` [MR3171101]. Appendix D (Prop. D.0.3) gives a second
route to the odd `n ≤ 10²⁷`: the verification of binary Goldbach up to `4·10¹⁸` by Oliveira e
Silva, Herzog and Pardi [OSHP], together with primes in short intervals derived from verifications
of RH (Ramaré–Saouter [MR1950435], and Ramaré's tables [Rpc] at Platt's height `3.061·10¹⁰`
[Plattpi]).
The book treats the numerical results it quotes from the literature (Platt's verifications of RH and
GRH, [OSHP], Ramaré's bound (2.21) for `∑ μ(n)/n`, and others) as established.

**What the formalization proves.** `TernaryGoldbach.Statement` (`TernaryGoldbach/Statement.lean`)
is the same sentence over `ℕ`: `∀ n : ℕ, Odd n → 5 < n → IsSumOfThreePrimes n`. The main theorem
`TernaryGoldbach.ternary_goldbach_of_hypotheses` (`TernaryGoldbach/MainTheorems.lean`) proves it
from three published numerical results. These are taken as hypotheses (`Prop`s passed as arguments,
not postulated), and the proof uses all three (`companion/data/hypothesis_trace.json`):

* `PlattGRH` (Platt): GRH for primitive characters of odd conductor `q ≤ 3·10⁵` up to height
  `10⁸/q`, and of even conductor `q ≤ 4·10⁵` up to height `max(10⁸/q, 200 + 7.5·10⁷/q)`;
* `BinaryGoldbachInput` ([OSHP]): every even `n` with `4 ≤ n ≤ 4·10¹⁸` is a sum of two primes;
* `RamareMoebius` (Ramaré, 2013, the book's (2.21)): `|∑_{n ≤ x} μ(n)/n| ≤ 0.03 / log x` for
  `x ≥ 11815`.

The Lean proof splits like the book's. `Helfgott.ternaryGoldbachFrom` covers the odd `N ≥ 10²⁷` by
the circle method, as in §14.4 but with weaker intermediate constants: major arcs `≥ 1.049 x²/κ` and
minor arcs `≤ 1.0376 x²/κ`, where §14.4 has `1.058259` and `1.00948`. These still leave a positive
lower bound. `Helfgott.ternaryGoldbachUpTo` covers the odd `5 < N ≤ 10²⁷` from [OSHP] and a ladder
of Proth primes up to `10²⁷` whose primality the Lean kernel checks
(`Helfgott.ternaryGoldbachUpTo_1e27`). That is the argument of §1.6, with this ladder in place of
the Helfgott–Platt ladder.

**Relation: proved**, conditionally on the three hypotheses (as is every result of the development).
It is certified here by three theorems:

* `thm_1_1_1_iff_statement : thm_1_1_1 ↔ TernaryGoldbach.Statement`. The printed sentence,
  transcribed over `ℤ` as `thm_1_1_1`, is the repo's `Statement`.
* `thm_1_1_1_holds`. Given the three hypotheses as `Fact` instances, `thm_1_1_1` holds; the proof
  applies the Lean main theorem.
* `thm_1_1_1_conditional_iff_formal`. The statement of the Lean main theorem (taken with `type_of%`,
  not copied) is equivalent to "the three hypotheses imply `thm_1_1_1`". So, apart from the
  hypotheses, the Lean theorem is neither weaker nor stronger than the book's.

Two sanity checks show that `thm_1_1_1` is not vacuous and support the reading of "three primes".
By `thm_1_1_1_five_not_sum`, the odd integer `5` is not a sum of three primes, so the threshold `5`
is sharp and the conclusion is a real constraint. By `thm_1_1_1_seven_not_distinct`, `7 = 2 + 2 + 3`
is not a sum of three *distinct* primes, so the primes must be allowed to repeat.
-/

namespace Companion.Book

open TernaryGoldbach

/-- **[H, Theorem 1.1.1]**, as printed: *every odd integer greater than `5` can be written as the
sum of three primes.*

How the statement is transcribed:
* "odd integer": `n : ℤ` with Mathlib's `Odd n` (`∃ m, n = 2 * m + 1`). The book says "integer".
  Because `n > 5`, this is the same as a natural number, and `thm_1_1_1_iff_statement` checks that
  the `ℤ` form agrees with the repo's `ℕ` form `TernaryGoldbach.Statement`.
* "greater than `5`": the strict inequality `5 < n`.
* "primes": natural-number primes `p : ℕ` with `Nat.Prime p` (`2, 3, 5, …`), cast to `ℤ` in the sum.
  Mathlib's ring-theoretic `Prime` on `ℤ` would also count `−2, −3, …` as primes (for example
  `7 = 5 + 5 + (−3)`). That is not the book's meaning, since its primes are the positive ones.
* "the sum of three primes": `n = p + q + r` for some primes `p q r`, in any order and not
  necessarily distinct. Repetition has to be allowed. Up to order, the only way to write `7` as a
  sum of three primes is `2 + 2 + 3`, and no three distinct primes sum to `7`
  (`thm_1_1_1_seven_not_distinct`), so reading "distinct" would make the printed statement false.
  The prime `2` is allowed as well. The book notes in §14.4 that for three *odd* primes the range
  becomes `N > 7`.
* No hypotheses: the book states the theorem unconditionally. The numerical results it relies on
  appear in the formalization as the three hypotheses of `thm_1_1_1_holds`. -/
def thm_1_1_1 : Prop :=
  ∀ n : ℤ, Odd n → 5 < n → ∃ p q r : ℕ, p.Prime ∧ q.Prime ∧ r.Prime ∧ n = p + q + r

/-- The book's statement (over `ℤ`) is the repo's `TernaryGoldbach.Statement` (over `ℕ`). -/
theorem thm_1_1_1_iff_statement : thm_1_1_1 ↔ TernaryGoldbach.Statement := by
  constructor
  · rintro h n hn h5
    obtain ⟨p, q, r, hp, hq, hr, hs⟩ := h n ((Int.odd_coe_nat n).2 hn) (by exact_mod_cast h5)
    exact ⟨p, q, r, hp, hq, hr, by exact_mod_cast hs.symm⟩
  · rintro h n hn h5
    lift n to ℕ using (by omega)
    obtain ⟨p, q, r, hp, hq, hr, hs⟩ := h n ((Int.odd_coe_nat n).1 hn) (by exact_mod_cast h5)
    exact ⟨p, q, r, hp, hq, hr, by exact_mod_cast hs.symm⟩

/-- **[H, Theorem 1.1.1] holds**, given the three numerical hypotheses of the development as `Fact`
instances. This is the Lean main theorem `TernaryGoldbach.ternary_goldbach_of_hypotheses`, read
through `thm_1_1_1_iff_statement`. -/
theorem thm_1_1_1_holds [Fact PlattGRH] [Fact BinaryGoldbachInput] [Fact RamareMoebius] :
    thm_1_1_1 :=
  thm_1_1_1_iff_statement.2 <|
    TernaryGoldbach.ternary_goldbach_of_hypotheses Fact.out Fact.out Fact.out

/-- The statement of the Lean main theorem (taken with `type_of%`, not copied) says exactly that the
three hypotheses imply [H, Theorem 1.1.1]. Apart from the hypotheses, it is neither weaker nor
stronger than the book's theorem. -/
theorem thm_1_1_1_conditional_iff_formal :
    (PlattGRH → BinaryGoldbachInput → RamareMoebius → thm_1_1_1) ↔
      type_of% @TernaryGoldbach.ternary_goldbach_of_hypotheses := by
  rw [thm_1_1_1_iff_statement]

/-- Sanity check: the odd integer `5` is not the sum of three primes, because every prime is at
least `2`. So the threshold of the printed statement is sharp, and `thm_1_1_1` has content. -/
theorem thm_1_1_1_five_not_sum :
    ¬ ∃ p q r : ℕ, p.Prime ∧ q.Prime ∧ r.Prime ∧ (5 : ℤ) = p + q + r := by
  rintro ⟨p, q, r, hp, hq, hr, h⟩
  have := hp.two_le
  have := hq.two_le
  have := hr.two_le
  omega

/-- Sanity check: `7` is not the sum of three *distinct* primes, so in `thm_1_1_1` the primes must
be allowed to repeat (`7 = 2 + 2 + 3`). -/
theorem thm_1_1_1_seven_not_distinct :
    ¬ ∃ p q r : ℕ, p.Prime ∧ q.Prime ∧ r.Prime ∧ p ≠ q ∧ p ≠ r ∧ q ≠ r ∧ (7 : ℤ) = p + q + r := by
  rintro ⟨p, q, r, hp, hq, hr, hpq, hpr, hqr, h⟩
  have := hp.two_le
  have := hq.two_le
  have := hr.two_le
  omega

end Companion.Book
