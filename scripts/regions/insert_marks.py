"""Insert the step markers into a scratch copy of the arXiv source (build_steps.sh).

New code.  For the n-th prose step of the steps file (0-based, in file order), `\\rmS{n}` goes
before its first character and `\\rmE{n}` after its last, with no space added; the main file gets
`\\input{regionmarks}\\input{stepmarks}` on a line of its own before `\\begin{document}`.

Usage: python3 -I insert_marks.py <build dir> <steps json> <main>
"""
import collections
import json
import os
import sys

build, steps_path, main = sys.argv[1:4]
steps = json.load(open(steps_path))['steps']
per = collections.defaultdict(list)
for n, st in enumerate(steps):
    if st['kind'] == 'prose':
        per[st['file']] += [(st['end'], f'\\rmE{{{n}}}'), (st['start'], f'\\rmS{{{n}}}')]
for f, ins in per.items():
    p = os.path.join(build, f)
    s = open(p, encoding='ascii').read()
    # from the back, so offsets stay valid; at one offset an end goes before a start
    for off, mark in sorted(ins, key=lambda x: (x[0], x[1].startswith('\\rmS')), reverse=True):
        s = s[:off] + mark + s[off:]
    open(p, 'w', encoding='ascii').write(s)
p = os.path.join(build, main + '.tex')
s = open(p, encoding='ascii').read()
k = '\\begin{document}'
s = s.replace(k, '\\input{regionmarks}\\input{stepmarks}\n' + k, 1)
open(p, 'w', encoding='ascii').write(s)
