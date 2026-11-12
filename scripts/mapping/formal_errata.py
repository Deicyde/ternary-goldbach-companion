"""Settle the errata of 2026-11-06 that were pending a formal check, by their compiled refutations.

New code.  Each claim below is confirmed by a theorem of lean/Companion/Book/ that proves the printed
statement false, built at the pin with `lake build` (lean/), whose axioms are only propext,
Classical.choice and Quot.sound (lean/Axioms.lean).  Its Lean statement was compared with the printed
statement in the LaTeX before it was recorded here.  What a claim of 2026-11-06 said beyond what the
theorem proves is not confirmed and stays out of the note.

Writes the `check` of each item's erratum in data/items.json.

Usage: python3 -I formal_errata.py <repository root>
"""
import json
import os
import sys

# item -> (kind, Lean file, refuting theorem, what it confirms)
SETTLED = {
    'Eq 5.32': ('statement-false', 'lean/Companion/Book/Eq_5_32.lean', 'Companion.Book.eq_5_32_each_case_false',
                'Both cases fail with G_v the exact sum (5.28), the least function the text allows: for v = 1, '
                '∫₁⁵ G₁(S)dS/S = (2/3)log 2 + (1/3)log 5 − 2/5 ≈ 0.59858 > 0.3698 log 5, and for v = 2, '
                '∫₁⁴ G₂(S)dS/S = (7/6)log 2 + (1/6)log 3 − 11/24 ≈ 0.53344 > 0.37273 log 4.'),
    'Eq 5.36': ('statement-false', 'lean/Companion/Book/Eq_5_36.lean', 'Companion.Book.eq_5_36_false',
                'The case v = 2 fails, inherited from (5.32): ∫₁⁴ H₂(S)dS/S = (4/π²)((7/6)log 2 + (1/6)log 3 − 11/24) '
                '≈ 0.21620 > 0.15107 log 4 ≈ 0.20943.'),
    'Theorem 7.1.1': ('statement-false', 'lean/Companion/Book/Thm_7_1_1.lean', 'Companion.Book.thm_7_1_1_remark_false',
                      'The remark after the theorem is false: η♡ is the one-sided Gaussian, so η̂♡(−δ) = '
                      '∫₀^∞ e(δt)e^{−t²/2}dt, whose real part is half of √(2π)e^{−2π²δ²}; at δ = 0 it is √(π/2), '
                      'not √(2π). The theorem itself is not refuted.'),
    'Proposition 11.2.3': ('statement-false', 'lean/Companion/Book/Prop_11_2_3.lean', 'Companion.Book.prop_11_2_3_false',
                           'The first case (11.18)–(11.19) omits the term C_{φ,0,K} = 1.04488∫₀^{1/K}φ that its proof '
                           'produces and the second case keeps; for a continuous φ concentrated near w = 2.75/x '
                           '(x = 10³⁰, K = 8, q = 8·10⁸, δ = 0), |S_{η*}(α,x)| ≥ 0.18|φ|₁x while '
                           'g_{x,φ}(q)|φ|₁x ≤ 0.01|φ|₁x.'),
    'Proposition D.0.3': ('typo', 'lean/Companion/Book/Prop_D_0_3.lean', 'Companion.Book.prop_D_0_3_upTo_false',
                          'The range should read 5 < n: 5 is odd and at most n₀, but it is not a sum of three primes.'),
}


def main():
    root = sys.argv[1]
    path = os.path.join(root, 'data', 'items.json')
    doc = json.load(open(path, encoding='utf-8'))
    done = 0
    for it in doc['items']:
        if it['id'] not in SETTLED:
            continue
        kind, lean, thm, note = SETTLED[it['id']]
        er = it['erratum']
        if er.get('check', {}).get('state') not in ('pending formal check', 'confirmed'):
            sys.exit(f"{it['id']}: erratum is not pending a formal check")
        er['check'] = {'state': 'confirmed', 'kind': kind, 'how': 'compiled Lean refutation at the pin',
                       'script': lean, 'theorem': thm, 'note': note}
        done += 1
    if done != len(SETTLED):
        sys.exit(f'settled {done} of {len(SETTLED)}')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)
    print(done, 'errata settled by compiled refutations')


main()
