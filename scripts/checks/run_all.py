"""Re-run the erratum checks in scripts/checks/ (and any other that data/items.json cites), and record their decision lines.

New code, standard library only.  Each check ends with one line `CONFIRMED: ...` or
`NOT CONFIRMED: ...`, decided by its computation.  Python checks run with `python3 -I`, or, for
those that import mpmath, `python3 -s` with PYTHONPATH set to the mpmath directory given; C checks
are compiled with `gcc -O2` and run.

Usage: python3 -I run_all.py <repository root> <mpmath dir> <out checks-run.json>
"""
import concurrent.futures
import datetime
import json
import os
import subprocess
import sys
import tempfile
import time


def run(path, mpmath_dir):
    t0 = time.time()
    if path.endswith('.c'):
        with tempfile.TemporaryDirectory() as t:
            exe = os.path.join(t, 'check')
            subprocess.run(['gcc', '-O2', '-o', exe, path, '-lm'], check=True, capture_output=True)
            p = subprocess.run([exe], capture_output=True, text=True, timeout=900)
    else:
        uses = 'mpmath' in open(path, encoding='utf-8').read()
        env = dict(os.environ, PYTHONPATH=mpmath_dir) if uses else None
        cmd = [sys.executable, '-s' if uses else '-I', os.path.basename(path)]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=900, cwd=os.path.dirname(path), env=env)
    lines = [l for l in p.stdout.splitlines() if l.startswith(('CONFIRMED:', 'NOT CONFIRMED:'))]
    return dict(exit=p.returncode, decision=lines[-1] if lines else '', seconds=round(time.time() - t0, 1))


def main():
    root, mpmath_dir, out = sys.argv[1:4]
    items = json.load(open(os.path.join(root, 'data', 'items.json')))['items']
    here = os.path.relpath(os.path.dirname(os.path.abspath(__file__)), root)
    committed = {os.path.join(here, f) for f in os.listdir(os.path.join(root, here))
                 if f.endswith(('.py', '.c')) and f != 'run_all.py'}
    todo = sorted({x['erratum']['check']['script'] for x in items
                   if x['erratum'].get('check', {}).get('script', '').startswith('scripts/')} | committed)
    results = {}
    with concurrent.futures.ThreadPoolExecutor(6) as pool:
        futures = {pool.submit(run, os.path.join(root, s), mpmath_dir): s for s in todo}
        for f in concurrent.futures.as_completed(futures):
            s = futures[f]
            try:
                results[s] = f.result()
            except Exception as e:  # a check that does not run is recorded as such
                results[s] = dict(exit=None, decision='', error=str(e)[:300])
            print(s, results[s].get('decision', '')[:100], flush=True)
    json.dump(dict(run_at=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                   python=sys.version.split()[0], checks=dict(sorted(results.items()))),
              open(out, 'w'), indent=1, ensure_ascii=False)


main()
