#!/bin/sh
# Segment one overlay's source into displays and proof steps, rebuild it with the step markers, check
# that the rebuild has the layout of the regionmarks.tex build, and place the regions on the arXiv PDF.
#   sh run_steps.sh book|paper-2013 <arXiv source dir> <arXiv PDF> <regionmarks.tex build dir> <scratch dir>
# Writes data/<overlay>-displays.json, data/<overlay>-steps.json and data/<overlay>-regions-steps.json.
# The regionmarks.tex build is build.sh's (the build the items' regions come from).
set -eu
overlay=$1 src=$2 pdf=$3 ref=$4 scratch=$5
here=$(cd "$(dirname "$0")" && pwd)
root=$(cd "$here/../.." && pwd)
data=$root/data
case $overlay in
  book) main=3nonpupbook id=arXiv:1501.05438v2 off=10 items=$data/items.json regs=$data/regions-book.json
        splits=$data/book-splits.json ;;
  paper-2013) main=ternvin id=arXiv:1312.7748v2 off=0 items=$data/items-paper-2013.json regs=$data/regions-paper-2013.json
        splits= ;;
esac
python3 -I "$root/scripts/steps/segment.py" "$overlay" "$src" "$items" "$data" $splits
sh "$here/build_steps.sh" "$src" "$scratch/build" "$data/$overlay-steps.json" "$main"
python3 -I "$here/layout_check.py" "$scratch/build/$main.pdf" "$ref/$main.pdf" 0.01 "$scratch/layout.json"
python3 -I "$here/steps.py" "$scratch/build" "$pdf" "$data/$overlay-displays.json" "$data/$overlay-steps.json" \
  "$regs" "$data/$overlay-regions-steps.json" "$main" "$id" "$off"
python3 -I -c '
import json, sys
r = json.load(open(sys.argv[1])); lay = json.load(open(sys.argv[2]))
lay = dict(lay, a="the build with stepmarks.tex and the step markers", b="the build with regionmarks.tex alone (build.sh)")
r["checks"]["layout"] = lay
json.dump(r, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
if lay["pages_differing"] or lay["pages"][0] != lay["pages"][1]:
    sys.exit("layout differs: " + str(lay["pages_differing"]))' "$data/$overlay-regions-steps.json" "$scratch/layout.json"
python3 -I "$root/scripts/steps/pages.py" "$data/$overlay-displays.json" "$data/$overlay-steps.json" \
  "$data/$overlay-regions-steps.json"
