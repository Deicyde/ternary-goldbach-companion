"""The numbered items of arXiv:1312.7748v2 (H. A. Helfgott, *The ternary Goldbach conjecture is true*).

New code.  The LaTeX build of the arXiv source with `companionhook.tex` writes, at every
`\\refstepcounter`, `\\companionitem{<counter>}{<number>}{<page>}{<input line>}` to `ternvin.aux`.
The numbered items are the steps of the counters `prop` (shared by Proposition, Theorem, Corollary
and Lemma) and `equation`; `section`, `subsection`, `subsubsection` and `enumi` steps are not items,
and the paper has no numbered figure, table, definition or example.  Each step's environment is
found at its input line of `ternvin.tex`, with its label, its last line and its source; lines
are those of the arXiv source.

Usage: python3 -I items.py <build dir> <out items json>
"""
import json
import os
import re
import sys

ENVS = {'prop': 'proposition', 'thm': 'theorem', 'cor': 'corollary', 'lem': 'lemma', 'equation': 'equation'}
BEGIN = re.compile(r'\\begin\{(prop|thm|cor|lem|equation)\}')


def section_of(number):
    return number.split('.')[0]


def main():
    build, out = sys.argv[1:3]
    aux = open(os.path.join(build, 'ternvin.aux'), encoding='latin-1').read()
    src = open(os.path.join(build, 'ternvin.tex'), encoding='latin-1').read().split('\n')
    # the build's ternvin.tex is the arXiv source plus one line, `\input{companionhook}`: lines are
    # given in the arXiv source
    hook = next(k for k, l in enumerate(src) if l.strip() == '\\input{companionhook}')
    arxiv_line = lambda k: k + 1 if k < hook else k
    steps = re.findall(r'\\companionitem\{(prop|equation)\}\{([^}]*)\}\{(\d+)\}\{(\d+)\}', aux)
    items, seen = [], set()
    for counter, number, page, line in steps:
        ln = int(line)
        # the environment opens on the step's input line or shortly before it (an optional argument)
        j = next((k for k in range(ln - 1, max(ln - 6, -1), -1) if BEGIN.search(src[k])
                  and not src[k].lstrip().startswith('%')), None)
        if j is None:
            sys.exit(f'{counter} {number}: no environment at line {ln}')
        env = BEGIN.search(src[j]).group(1)
        if (env == 'equation') != (counter == 'equation'):
            sys.exit(f'{counter} {number}: environment {env} at line {j + 1}')
        k = next(k for k in range(j, len(src)) if f'\\end{{{env}}}' in src[k])
        body = '\n'.join(src[j:k + 1])
        body = body[body.index(f'\\begin{{{env}}}'):body.index(f'\\end{{{env}}}') + len(env) + 6]
        label = re.search(r'\\label\{([^}]*)\}', body)
        kind = ENVS[env]
        iid = f"Eq {number}" if kind == 'equation' else f"{kind.capitalize()} {number}"
        if iid in seen:
            sys.exit(f'{iid} twice')
        seen.add(iid)
        items.append(dict(id=iid, kind=kind, number=number, page=int(page), phys_page=int(page),
                          section=section_of(number), chapter_file='ternvin', line=arxiv_line(j), end_line=arxiv_line(k),
                          label=label.group(1) if label else None, source=body,
                          arxiv_url=f'https://arxiv.org/pdf/1312.7748v2#page={page}'))
    json.dump(dict(paper='arXiv:1312.7748v2', source='ternvin.tex', items=items), open(out, 'w'),
              indent=1, ensure_ascii=False)
    kinds = {}
    for it in items:
        kinds[it['kind']] = kinds.get(it['kind'], 0) + 1
    print(len(items), kinds)


main()
