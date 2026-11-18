#!/bin/bash
# Build the GitHub Pages site in _site/: a landing page and both overlays, whose viewers fetch
# their PDF from arxiv.org (scripts/pages/remote_pdf.py). Run from the repository root.
set -euo pipefail
rm -rf _site
mkdir -p _site
for pair in book:https://arxiv.org/pdf/1501.05438v2 paper-2013:https://arxiv.org/pdf/1312.7748v2; do
  overlay=${pair%%:*}
  url=${pair#*:}
  ( cd "$overlay" && python3 pdf-overlay/tools/serve.py --build-only )
  python3 scripts/pages/remote_pdf.py "$overlay/site" "$url"
  cp -R "$overlay/site" "_site/$overlay"
done
cp pages/index.html _site/index.html
touch _site/.nojekyll
