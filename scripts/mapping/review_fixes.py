"""Apply the corrections of the 2026-11-12 review to data/items.json.

New code.  Run after finalize.py and formal_errata.py, before errata_doc.py and the producers.  Each
note correction names the text it replaces, and the script stops if that text is not there.  The
re-judged relations (data/rejudge-2026-11-12.json) are written to each item as `relations_at_P`:
declaration -> the relation of the item's key link to it, which the producers use in place of the
relation of the item's status.

Usage: python3 -I review_fixes.py <repository root>
"""
import json
import os
import sys

# item -> [(where, old text, new text)]; where is `note` or `check.note` (the erratum's check)
NOTES = {
    # the re-run check (scripts/checks/lemma_5_2_1.py) does not confirm a gap for R > W'
    'Lemma 5.2.1': [('note', ' the log gain is proved for a caller-chosen R ≤ W′, which repairs the book\'s unproved case R > W′.',
                     ' the log gain is proved for a caller-chosen R ≤ W′.')],
    # no axiom eta2DD_small occurs at the pin (TernaryGoldbach/, NOTES.md, README.md)
    'Lemma B.1.2': [('note', 'Lean history (NOTES): reaching 31.521 needed the axiom eta2DD_small for |t| ≤ 655. That axiom was '
                     'removed by switching to c₀ = 32, as Helfgott suggested (README).',
                     'Lean proves (B.6) with c₀ = 32 in place of 31.521 (README at the pin).')],
    # §7.1 writes η♡(t) = e^{-t²/2} with no range; the check covers both readings
    'Eq 1.11': [('check.note', None,
                 '(1.11)–(1.12) and the remark after them cannot both hold. With η♡ one-sided, as in §9.2 (η♥(t) = 0 '
                 'for t < 0), η̂♡(−δ) = √(π/2)e^{−2π²δ²} + i√2·D(√2πδ), 1.028806 + 0.551811i at δ = 0.1 against the '
                 'remark\'s 2.057613, so the remark is false; with the two-sided value √(2π)e^{−2π²δ²}, (1.11)–(1.12) '
                 'fail at q = 1, δ = 0 for x > 2.694·10¹¹, since (1/x)ΣΛ(n)e^{−(n/x)²/2} → √(π/2).')],
}
# machine paths of the session that ran the checks -> what scripts/checks/run_all.py writes
PATHS = [(' (prior-2026-11-06/agents/C12-judge/chk445.py)', ''),
         ('PYTHONPATH=<mpmath dir>', 'PYTHONPATH=<mpmath dir>'),
         (' (scratchpad/agents/C35/check92.py)', ''), (' (check96.py)', '')]   # 2026-11-06 scripts not kept
# item -> erratum check added on 2026-11-12, confirmed only if its re-run (data/checks-run.json) says CONFIRMED
CHECKS = {
    'Eq 3.6': ('typo', 'scripts/checks/eq_3_6.py', 'python3 -I eq_3_6.py',
               'As printed, (3.6) has +μ_{≤U}∗Λ_{≤V}∗1 and fails (at n = 2, U = V = 2 the right side is 3 log 2, '
               'against Λ(2) = log 2); with −μ_{≤U}∗Λ_{≤V}∗1, the sign that (3.8) uses, it holds.'),
}
RELATIONS = {'exactMatch', 'closeMatch', 'broadMatch', 'narrowMatch', 'relatedMatch', 'hasPart'}


def main():
    root = sys.argv[1]
    path = os.path.join(root, 'data', 'items.json')
    doc = json.load(open(path, encoding='utf-8'))
    items = {x['id']: x for x in doc['items']}
    for i, edits in NOTES.items():
        for where, old, new in edits:
            obj = items[i]['erratum']['check'] if where == 'check.note' else items[i]
            if old is None:
                obj['note'] = new
            elif old in obj['note']:
                obj['note'] = obj['note'].replace(old, new)
            elif new not in obj['note']:
                sys.exit(f'{i}: {where} does not hold the text to replace')
    runs = json.load(open(os.path.join(root, 'data', 'checks-run.json'), encoding='utf-8'))['checks']
    for i, (kind, script, command, note) in CHECKS.items():
        run = runs.get(script, {})
        if run.get('exit') != 0 or not run.get('decision', '').startswith('CONFIRMED'):
            sys.exit(f'{i}: {script} was not re-run, or did not confirm')
        items[i]['erratum']['check'] = {'state': 'confirmed', 'kind': kind, 'script': script, 'command': command,
                                        'output_line': run['decision'], 'note': note}
    rj = json.load(open(os.path.join(root, 'data', 'rejudge-2026-11-12.json'), encoding='utf-8'))
    n = 0
    for i, per in rj['items'].items():
        it = items[i]
        linked = {l['decl'] for l in it['lean']}
        for d, v in per.items():
            if d not in linked or v['relation'] not in RELATIONS:
                sys.exit(f'{i}: {d} is not linked, or {v["relation"]} is not a relation')
        it['relations_at_P'] = {d: v['relation'] for d, v in per.items()}
        n += 1
    text = json.dumps(doc, indent=1, ensure_ascii=False)
    for old, new in PATHS:
        text = text.replace(json.dumps(old, ensure_ascii=False)[1:-1], json.dumps(new, ensure_ascii=False)[1:-1])
    if '/tmp/' in text or '/home/' in text:
        sys.exit('a machine path is left in items.json')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(sum(len(e) for e in NOTES.values()), 'note corrections,', len(CHECKS), 'checks added,', n, 'items re-judged')


main()
