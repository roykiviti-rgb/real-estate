# -*- coding: utf-8 -*-
"""Review helper: render a clip (fractions of the page) of a PDF page at a given DPI.

Usage: python tool_pdfclip.py <pdf> <page> <fx0> <fy0> <fx1> <fy1> <dpi> <out.png>
"""
import sys

sys.dont_write_bytecode = True
import pymupdf  # noqa: E402


def main():
    pdf, pno = sys.argv[1], int(sys.argv[2])
    fx0, fy0, fx1, fy1 = (float(v) for v in sys.argv[3:7])
    dpi, out = int(sys.argv[7]), sys.argv[8]
    doc = pymupdf.open(pdf)
    r = doc[pno - 1].rect
    clip = pymupdf.Rect(r.x0 + fx0 * r.width, r.y0 + fy0 * r.height, r.x0 + fx1 * r.width, r.y0 + fy1 * r.height)
    doc[pno - 1].get_pixmap(dpi=dpi, clip=clip).save(out)
    print(out)


if __name__ == "__main__":
    main()
