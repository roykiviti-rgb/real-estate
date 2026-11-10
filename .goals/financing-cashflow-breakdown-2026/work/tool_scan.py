# -*- coding: utf-8 -*-
"""Review helper: show how the extractor sees the pages of a report (statement detection).

Usage: python tool_scan.py <issuer> <Q1|Q2> [--pages 40-60] [--file <pdf name>]
Prints, per page: cash-flow title?, solo/board/notes/TOC/consolidated flags, section headings and
totals found, numeric-line count, page title text; then the candidate statement blocks and the one
chosen. Output: %TEMP%/fcf_run/<issuer>/scan_<issuer>_<Q>.txt (UTF-8). Read-only on the PDF.
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import os  # noqa: E402

import pymupdf  # noqa: E402

import fcf_extract as X  # noqa: E402
import fcf_lib as L  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issuer")
    ap.add_argument("q", choices=["Q1", "Q2"])
    ap.add_argument("--pages", help="range to print, e.g. 40-60 (all pages are scanned anyway)")
    ap.add_argument("--file")
    a = ap.parse_args()
    folder = L.company_folder(a.issuer)
    rel = L.source_rel(a.issuer, a.q)
    fname = a.file or os.path.basename(rel.replace("\\", "/"))
    doc = pymupdf.open(os.path.join(L.WORKSPACE, folder, fname))
    scans = [X.PageScan(doc[i], i + 1) for i in range(doc.page_count)]
    lo, hi = 1, doc.page_count
    if a.pages:
        lo, hi = (int(x) for x in a.pages.split("-"))
    out = [f"{a.issuer} {a.q} {fname} pages={doc.page_count}"]
    for s in scans:
        if not (lo <= s.pno <= hi):
            continue
        sm = s.summary()
        if not (sm["cf_title"] or sm["heads"] or sm["totals"]) and not a.pages:
            continue
        out.append(f"p{s.pno:>3} cf={int(sm['cf_title'])} solo={int(sm['solo'])} board={int(sm['board'])} "
                   f"notes={int(sm['notes'])} toc={int(sm['toc'])} cons={int(sm['cons'])} integral={int(s.integral)} "
                   f"num={sm['numeric']:>3} heads={sm['heads']} totals={sm['totals']} | {sm['title'][:110]}")
    pick, cands = X.find_statement(scans, folder)
    out.append("")
    out.append("candidate blocks:")
    for c in cands:
        out.append("  " + str({k: c[k] for k in c}))
    out.append(f"chosen: {pick['pages'] if pick else None}")
    p = os.path.join(L.temp_dir(a.issuer), f"scan_{a.issuer}_{a.q}.txt")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(p)


if __name__ == "__main__":
    main()
