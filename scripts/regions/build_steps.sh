#!/bin/sh
# Rebuild [H] or arXiv:1312.7748v2 from its arXiv source with the markers of regionmarks.tex and
# stepmarks.tex, and with \rmS/\rmE inserted around every prose step of <steps json> (a scratch copy;
# the arXiv source is not changed).
#   sh build_steps.sh <arXiv source dir> <build dir> <steps json> [<main>]
# <main>: 3nonpupbook (the book, default) or ternvin (arXiv:1312.7748v2).
set -eu
src=$1 build=$2 steps=$3 main=${4:-3nonpupbook}
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$build"
mkdir -p "$build"
cp "$src"/* "$build"/
cp "$here/regionmarks.tex" "$here/stepmarks.tex" "$build"/
python3 -I "$here/insert_marks.py" "$build" "$steps" "$main"
cd "$build"
for i in 1 2 3; do pdflatex -interaction=nonstopmode "$main.tex" > "run$i.log" 2>&1 || true; done
