# -*- coding: utf-8 -*-
"""Review helper: render all pages of the PDFs in a TEMP folder (e.g. Excel exports) to PNGs.

Usage: python tool_pdf2png.py <dir> [dpi]
"""
import glob
import os
import sys

sys.dont_write_bytecode = True
import pymupdf  # noqa: E402


def main():
    d = sys.argv[1]
    dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 90
    for pdf in sorted(glob.glob(os.path.join(d, "*.pdf"))):
        doc = pymupdf.open(pdf)
        for i, pg in enumerate(doc):
            pg.get_pixmap(dpi=dpi).save(pdf[:-4] + f"_p{i + 1}.png")
        print(os.path.basename(pdf), doc.page_count)


if __name__ == "__main__":
    main()
