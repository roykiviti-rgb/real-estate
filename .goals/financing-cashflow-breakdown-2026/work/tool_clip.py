# -*- coding: utf-8 -*-
"""Review helper: render a clip of a page of the company's screenshots PDF at high DPI.

Usage: python tool_clip.py <issuer> <page> <x0> <y0> <x1> <y1> [dpi]
Output: %TEMP%/fcf_run/<issuer>/clip_<issuer>_<page>_<hhmmss>.png (time-stamped: viewers cache by path)
"""
import sys

sys.dont_write_bytecode = True
import os  # noqa: E402
import time  # noqa: E402

import pymupdf  # noqa: E402

import fcf_lib as L  # noqa: E402


def main():
    issuer, pno = sys.argv[1], int(sys.argv[2])
    x0, y0, x1, y1 = (float(v) for v in sys.argv[3:7])
    dpi = int(sys.argv[7]) if len(sys.argv) > 7 else 200
    folder = L.company_folder(issuer)
    p = os.path.join(L.WORKSPACE, folder, f"{issuer} - צילומי מסך תזרים מימון 2026.pdf")
    with pymupdf.open(p) as doc:
        pix = doc[pno - 1].get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1))
    out = os.path.join(L.temp_dir(issuer), f"clip_{issuer}_{pno}_{time.strftime('%H%M%S')}.png")
    pix.save(out)
    print(out)


if __name__ == "__main__":
    main()
