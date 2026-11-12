"""Write data/statements.json: the formal statements of lean/Companion/Book/ and what each file proves.

New code.  The table below says, for each file, which book item it states, the declaration of the
statement, and what the file proves about it at the pin: `proved` (the statement as printed, with the
formalization's hypotheses where named), `implied` (the statement implies, or is equivalent to, a
declaration of the formalization), `refuted` (its negation), or `stated` (no relation).  It was read off
each file's theorems; the declarations and lines are read from the files here and checked against the
build (lean/.lake).  `version` is the commit of this repository that added lean/.

Usage: python3 -I statements.py <repository root> <commit that added lean/>
"""
import json
import os
import re
import sys

URI = 'https://github.com/Deicyde/ternary-goldbach-companion'   # placeholder: the owner is not decided

# file: (book item, [(statement, proves, theorem, target or hypotheses)])
TABLE = {
    'Cor_7_1_3': ('Corollary 7.1.3', [('cor_7_1_3', 'implied', 'cor_7_1_3_implies_formal', 'TernaryGoldbach.MajorArcs.cor_7_1_3\'')]),
    'Cor_12_2_5': ('Corollary 12.2.5', [('cor_12_2_5', 'implied', 'cor_12_2_5_implies_formal', 'TernaryGoldbach.MinorArcs.cor_12_2_5')]),
    'Eq_2_21': ('Eq 2.21', [('eq_2_21', 'equivalent', 'eq_2_21_iff', 'TernaryGoldbach.RamareMoebius')]),
    'Eq_5_31': ('Eq 5.31', [('eq_5_31', 'implied', 'eq_5_31_implies_formal', 'TernaryGoldbach.MinorArcs.T2_le\'')]),
    'Eq_5_32': ('Eq 5.32', [('eq_5_32', 'refuted', 'eq_5_32_each_case_false', None)]),
    'Eq_5_36': ('Eq 5.36', [('eq_5_36', 'refuted', 'eq_5_36_false', None)]),
    'Eq_9_94': ('Eq 9.94', [('eq_9_94', 'proved', 'eq_9_94_holds', None)]),
    'Eq_12_12': ('Eq 12.12', [('eq_12_12', 'proved', 'eq_12_12_holds', None)]),
    'Eq_14_7': ('Eq 14.7', [('eq_14_7', 'proved', 'eq_14_7_holds', 'PlattGRH')]),
    'Eq_14_27': ('Eq 14.27', [('eq_14_27', 'implied', 'eq_14_27_implies_formal', 'TernaryGoldbach.MajorArcs.major_total')]),
    'Eq_14_49': ('Eq 14.49', [('eq_14_49', 'implied', 'eq_14_49_implies_formal', 'TernaryGoldbach.MinorArcs.minor_total')]),
    'Eq_14_51': ('Eq 14.51', [('eq_14_51', 'proved', 'eq_14_51_holds', None)]),
    'Lemma_4_1_3': ('Lemma 4.1.3', [('lemma_4_1_3', 'proved', 'lemma_4_1_3_holds', None)]),
    'Lemma_B_1_2': ('Lemma B.1.2', [('lemma_B_1_2', 'implied', 'lemma_B_1_2_implies_formal', 'TernaryGoldbach.MinorArcs.eta2_fourier_bound\'')]),
    'Prop_5_2_4': ('Proposition 5.2.4', [('prop_5_2_4', 'implied', 'prop_5_2_4_implies_formal', 'TernaryGoldbach.MinorArcs.prop_5_2_4_e')]),
    'Prop_7_1_5': ('Proposition 7.1.5', [('prop_7_1_5', 'implied', 'prop_7_1_5_implies_formal', 'TernaryGoldbach.MajorArcs.prop_7_1_5\'')]),
    'Prop_9_3_2': ('Proposition 9.3.2', [('prop_9_3_2', 'implied', 'prop_9_3_2_implies_formal', 'TernaryGoldbach.MajorArcs.prop_9_3_2')]),
    'Prop_9_4_2': ('Proposition 9.4.2', [('prop_9_4_2', 'proved', 'prop_9_4_2_holds', None)]),
    'Prop_9_5_1': ('Proposition 9.5.1', [('prop_9_5_1', 'implied', 'prop_9_5_1_implies_formal', 'TernaryGoldbach.MajorArcs.prop_9_5_1')]),
    'Prop_11_2_3': ('Proposition 11.2.3', [('prop_11_2_3', 'refuted', 'prop_11_2_3_false', None)]),
    'Prop_12_1_2': ('Proposition 12.1.2', [('prop_12_1_2', 'proved', 'prop_12_1_2_holds', None)]),
    'Prop_12_2_4': ('Proposition 12.2.4', [('prop_12_2_4', 'implied', 'prop_12_2_4_implies_formal', 'TernaryGoldbach.MinorArcs.prop_12_2_4')]),
    'Prop_D_0_3': ('Proposition D.0.3', [('prop_D_0_3', 'refuted', 'prop_D_0_3_upTo_false', None)]),
    'Thm_1_1_1': ('Theorem 1.1.1', [('thm_1_1_1', 'proved', 'thm_1_1_1_holds', 'PlattGRH, BinaryGoldbachInput, RamareMoebius')]),
    'Thm_3_1_1': ('Theorem 3.1.1', [('thm_3_1_1', 'implied', 'thm_3_1_1_implies_formal', 'TernaryGoldbach.MinorArcs.theorem_3_1_1')]),
    'Thm_7_1_1': ('Theorem 7.1.1', [('thm_7_1_1', 'stated', None, None),
                                    ('thm_7_1_1_remark', 'refuted', 'thm_7_1_1_remark_false', None)]),
    'Thm_7_1_4': ('Theorem 7.1.4', [('thm_7_1_4', 'implied', 'thm_7_1_4_implies_formal_odd', 'TernaryGoldbach.MajorArcs.thm_7_1_4_odd')]),
    'Thm_13_2_1': ('Theorem 13.2.1', [('thm_13_2_1', 'stated', None, None)]),
}


def note_of(decl, proves, thm, other):
    if proves == 'proved' and other:
        return f'Stated as printed in `{decl}`, and proved there from the hypotheses {other} (`{thm}`).'
    if proves == 'proved':
        return f'Stated as printed in `{decl}`, and proved there (`{thm}`).'
    if proves == 'implied':
        return f'Stated as printed in `{decl}`; the file proves that it implies `{other}` (`{thm}`), not the statement itself.'
    if proves == 'equivalent':
        return f'Stated as printed in `{decl}`; the file proves it equivalent to the hypothesis `{other}` (`{thm}`).'
    if proves == 'refuted':
        return f'Stated as printed in `{decl}`, and proved false there (`{thm}`).'
    return f'Stated as printed in `{decl}`; the file proves no relation to the formalization.'


def main():
    root, version = sys.argv[1:3]
    out = []
    for f, (item, stmts) in sorted(TABLE.items()):
        lines = open(os.path.join(root, 'lean', 'Companion', 'Book', f + '.lean'), encoding='utf-8').read().split('\n')
        for name, proves, thm, other in stmts:
            k = next((k for k, l in enumerate(lines) if re.match(rf'^(noncomputable )?def {re.escape(name)}\b', l)), None)
            if k is None:
                sys.exit(f'{f}: no def {name}')
            if thm and not any(re.match(rf'^theorem {re.escape(thm)}\b', l) for l in lines):
                sys.exit(f'{f}: no theorem {thm}')
            end = next((j for j in range(k, min(k + 60, len(lines))) if not lines[j].strip()), min(k + 60, len(lines)))
            decl = f'Companion.Book.{name}'
            out.append(dict(item=item, file=f'lean/Companion/Book/{f}.lean', module=f'Companion.Book.{f}', declaration=decl,
                            line=k + 1, snippet='\n'.join(lines[k:end]).rstrip(), truncated=end - k >= 60 and bool(lines[end - 1].strip()),
                            proves=proves, theorem=f'Companion.Book.{thm}' if thm else None, other=other,
                            note=note_of(decl, proves, thm and f'Companion.Book.{thm}', other)))
    doc = dict(repository=dict(uri=URI, version=version, path='lean',
                               uri_note='placeholder: the owner of the published repository is decided before publishing'),
               statements=out)
    with open(os.path.join(root, 'data', 'statements.json'), 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    print(len(out), 'statements')


main()
