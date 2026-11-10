# -*- coding: utf-8 -*-
"""Review helper: render the pages of a company's screenshots PDF to PNGs for visual inspection.

Usage (from any directory): python tool_shots.py <issuer> [dpi] [--pages 2,3]
Output: %TEMP%/fcf_run/<issuer>/shots_<hhmmss>/s<i>.png + info.txt (page sizes, embedded image sizes, TOC).
(time-stamped folder: image viewers may cache files by path)
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import os  # noqa: E402
import time  # noqa: E402

import pymupdf  # noqa: E402

import fcf_lib as L  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issuer")
    ap.add_argument("dpi", nargs="?", type=int, default=100)
    ap.add_argument("--pages")
    a = ap.parse_args()
    folder = L.company_folder(a.issuer)
    p = os.path.join(L.WORKSPACE, folder, f"{a.issuer} - צילומי מסך תזרים מימון 2026.pdf")
    out = L.temp_dir(a.issuer, f"shots_{time.strftime('%H%M%S')}")
    want = {int(x) for x in a.pages.split(",")} if a.pages else None
    with pymupdf.open(p) as doc:
        lines = [f"pages {doc.page_count}", f"toc {doc.get_toc()}", f"meta {doc.metadata}"]
        for i, pg in enumerate(doc):
            imgs = [(im[2], im[3]) for im in pg.get_images()]
            lines.append(f"{i + 1} {pg.rect} images={imgs}")
            if want and i + 1 not in want:
                continue
            pg.get_pixmap(dpi=a.dpi).save(os.path.join(out, f"s{i + 1}.png"))
    with open(os.path.join(out, "info.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(out)


if __name__ == "__main__":
    main()
