#!/bin/bash
# Build the GitHub Pages site in _site/: a landing page and both overlays. Each overlay's config
# sets `pdf.remote`, so its viewer fetches the PDF from arxiv.org, and build_site.py copies no PDF
# and fetches nothing. Run from the repository root.
set -euo pipefail
rm -rf _site
mkdir -p _site
for overlay in book paper-2013; do
  ( cd "$overlay" && python3 -B pdf-overlay/tools/build_site.py )
  if find "$overlay/site" -iname '*.pdf' | grep -q .; then
    echo "$overlay/site holds a PDF; the arXiv PDFs are never published" >&2
    exit 1
  fi
  cp -R "$overlay/site" "_site/$overlay"
done
cp pages/index.html _site/index.html
touch _site/.nojekyll
