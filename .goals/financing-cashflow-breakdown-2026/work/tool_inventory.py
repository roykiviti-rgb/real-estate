# -*- coding: utf-8 -*-
"""Inventory of all source PDFs (baseline list): pages, text-layer quality, cash-flow keyword hits,
first-page text. Read-only on the PDFs. Runs in parallel processes.

Usage: python tool_inventory.py [--issuers 1039 1618 ...] [--out <json>]
Default output: work/inventory.json  (small summary, safe to keep in .goals)
"""
import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import argparse  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402

import pymupdf  # noqa: E402

import fcf_lib as L  # noqa: E402

KW = {
    "cf": ["תזרימי מזומנים", "תזרימי המזומנים", "תזרים מזומנים", "תזרים המזומנים"],
    "fin": ["פעילות מימון", "פעילויות מימון", "פעילות המימון", "פעילויות המימון"],
    "cons": ["מאוחד", "מאוחדים"],
    "solo": ["המיוחסים לחברה", "מידע כספי נפרד", "38ד", "נפרדים", "הנפרד"],
    "en_cf": ["cash flows", "cash flow", "CASH FLOWS"],
    "en_fin": ["financing activities", "FINANCING ACTIVITIES", "Financing activities"],
    "en_cons": ["consolidated", "CONSOLIDATED", "Consolidated"],
}
COMMON = ["של", "החברה", "מזומנים", "דוח", "על", "בע\"מ", "הכספיים", "ליום", "אלפי"]


def rev(s):
    return s[::-1]


def page_stats(page):
    txt = page.get_text("text")
    heb = len(re.findall(r"[\u05D0-\u05EA]", txt))
    lat = len(re.findall(r"[A-Za-z]", txt))
    dig = len(re.findall(r"\d", txt))
    pua = len(re.findall(r"[\uE000-\uF8FF]", txt))
    fffd = txt.count("\ufffd")
    ext = len(re.findall(r"[\u00C0-\u024F]", txt))  # Latin-1 supplement/extended (typical of mis-encoded Hebrew)
    words = re.findall(r"[\u05D0-\u05EA\"']+", txt)
    fwd = sum(1 for w in words if w in COMMON)
    bwd = sum(1 for w in words if w in [rev(c) for c in COMMON])
    hits = {}
    for k, lst in KW.items():
        n = sum(txt.count(x) for x in lst)
        if k in ("cf", "fin", "cons", "solo"):
            nr = sum(txt.count(rev(x)) for x in lst)
            if nr:
                hits[k + "_rev"] = nr
        if n:
            hits[k] = n
    img_area = 0.0
    try:
        for info in page.get_image_info():
            b = pymupdf.Rect(info["bbox"]) & page.rect
            img_area += b.width * b.height
    except Exception:
        pass
    cover = img_area / max(1.0, page.rect.width * page.rect.height)
    first = " | ".join(x.strip() for x in txt.splitlines() if x.strip())[:220]
    return {"chars": len(txt), "heb": heb, "lat": lat, "dig": dig, "pua": pua, "fffd": fffd, "ext": ext,
            "fwd": fwd, "bwd": bwd, "img": round(cover, 2), "hits": hits, "first": first,
            "w": round(page.rect.width, 1), "h": round(page.rect.height, 1), "rot": page.rotation}


def one(rel):
    path = os.path.join(L.WORKSPACE, rel)
    f = os.path.basename(rel.replace("\\", "/"))
    m = re.search(r"_2026_(Q[1-4])_(\d+)(-\d+)?\.pdf$", f)
    out = {"rel": rel, "file": f, "folder": rel.split("\\")[0], "issuer": rel.split(" - ")[0],
           "quarter": m.group(1) if m else None, "report_id": m.group(2) if m else None,
           "suffix": (m.group(3) or "") if m else None}
    with pymupdf.open(path) as doc:
        out["pages"] = doc.page_count
        pages = []
        for i, pg in enumerate(doc):
            st = page_stats(pg)
            st["p"] = i + 1
            pages.append(st)
    tot = {k: sum(p[k] for p in pages) for k in ("chars", "heb", "lat", "dig", "pua", "fffd", "ext", "fwd", "bwd")}
    out["totals"] = tot
    out["first_pages"] = [p["first"] for p in pages[:3]]
    out["no_text_pages"] = [p["p"] for p in pages if p["chars"] < 40]
    out["image_pages"] = [p["p"] for p in pages if p["img"] > 0.5]
    out["kw_pages"] = [{k: p[k] for k in ("p", "hits", "first", "chars", "heb", "fwd", "bwd", "img", "ext", "pua")}
                       for p in pages if p["hits"]]
    out["all_pages"] = [{k: p[k] for k in ("p", "chars", "heb", "lat", "dig", "fwd", "bwd", "img", "ext", "pua", "fffd")}
                        for p in pages]
    out["page_sizes"] = sorted({(p["w"], p["h"], p["rot"]) for p in pages})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issuers", nargs="*")
    ap.add_argument("--out", default=os.path.join(L.TEMP_BASE, "_inventory", "inventory.json"))
    ap.add_argument("--workers", type=int, default=10)
    a = ap.parse_args()
    rels = sorted(L.baseline_files())
    if a.issuers:
        rels = [r for r in rels if r.split(" - ")[0] in a.issuers]
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        res = list(ex.map(one, rels, chunksize=1))
    L.save_json(res, a.out)
    print("files:", len(res), "->", a.out)


if __name__ == "__main__":
    main()
