"""Draw the regions of regions-book.json (or of several region files) on rendered pages of the arXiv PDF, for a visual check.

New code; standard library and poppler's pdftoppm.  Each region is outlined: red for a theorem-like
item, blue for a numbered display, green for a float; from a steps regions file (steps.py), orange
for a display outside proofs, magenta for a prose step and cyan for a display step, each quad of a
region drawn.  Regions of adjacent steps alternate between two shades.

Usage: python3 -I render_samples.py <arXiv PDF> <regions json>[,<regions json>...] <out dir> <page> [<page> ...]
"""
import json
import os
import struct
import subprocess
import sys
import tempfile
import zlib

DPI = int(os.environ.get('DPI', '80'))
COLORS = {'Eq': (40, 90, 220), 'Figure': (0, 150, 60), 'Table': (0, 150, 60)}
STEP_COLORS = {'display': [(240, 140, 0)], 'prose': [(200, 0, 200), (120, 0, 120)], 'step-display': [(0, 180, 200), (0, 110, 130)]}


def load(paths):
    """[(color, region)] of the region files."""
    out = []
    for path in paths.split(','):
        d = json.load(open(path))
        for iid, regs in d.get('items', {}).items():
            out += [(COLORS.get(iid.split()[0], (210, 30, 30)), r) for r in regs]
        for k, (iid, regs) in enumerate(d.get('displays', {}).items()):
            out += [(STEP_COLORS['display'][0], r) for r in regs]
        for k, (iid, regs) in enumerate(d.get('steps', {}).items()):
            kind = 'step-display' if all('quads' not in r for r in regs) and d.get('printed_lines', {}).get(iid) is None else 'prose'
            cs = STEP_COLORS[kind]
            out += [(cs[k % len(cs)], r) for r in regs]
    return out


def read_ppm(path):
    data = open(path, 'rb').read()
    parts, pos = [], 0
    while len(parts) < 4:
        while data[pos:pos + 1].isspace():
            pos += 1
        end = pos
        while not data[end:end + 1].isspace():
            end += 1
        parts.append(data[pos:end])
        pos = end
    w, h = int(parts[1]), int(parts[2])
    return w, h, bytearray(data[pos + 1:pos + 1 + 3 * w * h])


def write_png(path, w, h, px):
    raw = b''.join(b'\x00' + bytes(px[3 * w * r:3 * w * (r + 1)]) for r in range(h))
    chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
                + chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b''))


def rect(px, w, h, x0, y0, x1, y1, color, t=2):
    for y in range(max(0, y0), min(h, y1 + 1)):
        for x in range(max(0, x0), min(w, x1 + 1)):
            if x - x0 < t or x1 - x < t or y - y0 < t or y1 - y < t:
                i = 3 * (w * y + x)
                px[i:i + 3] = bytes(color)


def main():
    pdf, reg_path, out, pages = sys.argv[1], sys.argv[2], sys.argv[3], [int(p) for p in sys.argv[4:]]
    regions = load(reg_path)
    os.makedirs(out, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        for p in pages:
            stem = os.path.join(t, f'p{p}')
            subprocess.run(['pdftoppm', '-r', str(DPI), '-f', str(p), '-l', str(p), '-singlefile', pdf, stem], check=True)
            w, h, px = read_ppm(stem + '.ppm')
            for color, r in regions:
                if r['page'] != p:
                    continue
                if 'quads' in r:
                    for q in r['quads']:
                        rect(px, w, h, int(q[0] * w), int(q[1] * h), int(q[2] * w), int(q[5] * h), color)
                    continue
                x, y, rw, rh = r['rect']
                rect(px, w, h, int(x * w), int(y * h), int((x + rw) * w), int((y + rh) * h), color)
            write_png(os.path.join(out, f'page-{p:03d}.png'), w, h, px)
            print('wrote', p)


main()
