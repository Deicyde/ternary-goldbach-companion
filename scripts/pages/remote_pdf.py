"""Point a built overlay site's viewer at the PDF on arxiv.org.

The PDFs of Helfgott's book and 2013 paper are under arXiv's non-exclusive licence, so this
repository cannot publish them, and formal-companion publishes a PDF with a site only under an
open licence. arXiv serves both with `Access-Control-Allow-Origin: *`, so the reader's browser can
fetch the PDF from arxiv.org itself. The viewer still checks the bytes against the sha256 the
annotations pin before PDF.js renders them.

This edits only the built copy under <site>/pdf-overlay/viewer/, never the committed
pdf-overlay/:
- the PDF's URL: the arXiv URL, not the loopback route;
- the page's Content-Security-Policy: `connect-src` also allows https://arxiv.org;
- the status note and error wording: where the PDF comes from.

It refuses to run if any text it replaces is missing, so a formal-companion upgrade that changes
the viewer fails the Pages build rather than shipping a viewer that cannot load its PDF.

    python3 scripts/pages/remote_pdf.py <overlay>/site https://arxiv.org/pdf/1501.05438v2
"""
import json, sys
from pathlib import Path
from urllib.parse import urlsplit

ARXIV = 'https://arxiv.org'


def replace_once(path, old, new):
    text = path.read_text(encoding='utf-8')
    if text.count(old) != 1:
        sys.exit(f'{path}: expected exactly one {old!r}, found {text.count(old)}')
    path.write_text(text.replace(old, new), encoding='utf-8')


def main(site, url):
    parts = urlsplit(url)
    if f'{parts.scheme}://{parts.netloc}' != ARXIV or not parts.path.startswith('/pdf/'):
        sys.exit(f'not an arxiv.org PDF URL: {url}')
    viewer = Path(site) / 'pdf-overlay' / 'viewer'
    replace_once(viewer / 'viewer-core.js',
                 'return new URL(config.pdfUrl, pageUrl).href;',
                 f'return {json.dumps(url)};')
    replace_once(viewer / 'index.html', "connect-src 'self';", f"connect-src 'self' {ARXIV};")
    replace_once(viewer / 'index.html',
                 'The PDF is served only on loopback from a local cache.',
                 'The PDF is not hosted here: your browser fetches it from arxiv.org.')
    replace_once(viewer / 'index.html', 'It is never uploaded\n          or published.',
                 'This site never stores\n          or republishes it.')
    replace_once(viewer / 'viewer.js', '"loopback PDF"', '"arXiv PDF"')
    print(f'{viewer}: the PDF comes from {url}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
