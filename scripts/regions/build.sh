#!/bin/sh
# Rebuild [H] from its arXiv source (arXiv:1501.05438v2, e-print) with the position markers of
# regionmarks.tex, then place the regions on the arXiv PDF.
#   sh build.sh <arXiv source dir> <build dir> <arXiv PDF> <items json> <out regions json> [<main> <arXiv id>]
# <main> is the source's main file without .tex (default 3nonpupbook, the book; ternvin for
# arXiv:1312.7748v2).
# Needs pdflatex (TeX Live), poppler and Python 3.  The source's Greek epigraph needs babel's
# polutonikogreek; without it pdflatex reports errors and goes on, as here.
set -eu
src=$1 build=$2 pdf=$3 items=$4 out=$5 main=${6:-3nonpupbook} id=${7:-arXiv:1501.05438v2}
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$build"
cp "$src"/* "$build"/
cp "$here/regionmarks.tex" "$build"/
python3 -I -c '
import sys
p = sys.argv[1] + "/" + sys.argv[2] + ".tex"
s = open(p).read()
k = "\\begin{document}"
if "\\input{regionmarks}" not in s:
    s = s.replace(k, "\\input{regionmarks}\n" + k, 1)
open(p, "w").write(s)' "$build" "$main"
cd "$build"
for i in 1 2 3; do pdflatex -interaction=nonstopmode "$main.tex" > "run$i.log" 2>&1 || true; done
cd - > /dev/null
python3 -I "$here/regions.py" "$build" "$pdf" "$items" "$out" "$main" "$id"
