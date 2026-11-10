# -*- coding: utf-8 -*-
"""Review helper for one report: everything a reviewer needs to compare the extraction with the PDF.

Usage (from any directory):  python tool_review.py <issuer> <Q1|Q2> [--dpi 220] [--pages-dpi 100]

Uses the final data (data/<issuer>_<Q>.json – i.e. auto + overrides) when it exists, else the auto
extraction. Writes to %TEMP%/fcf_run/<issuer>/review_<Q>/ :
  fin_<hhmmss>.png  header strip (period titles + units) + the financing section at --dpi (>= 200), with every
                 extracted line framed and numbered (#n on the left margin) so it can be matched with lines.txt
  lines_<hhmmss>.txt  UTF-8 table in statement order: n | page | item | values per column (as printed) | text |
                 flags; then columns (labels, months, end, header text), units, C1 per column, (*) lines,
                 report flags, text-layer note
  outside_<k>_<hhmmss>.png  crops of the (*) interest/dividend-paid lines found outside financing (if any)
  page_<p>_<hhmmss>.png  every page of the consolidated cash-flow statement at --pages-dpi (context: find (*) lines
                 the extractor missed, check the statement's boundaries)
Read-only on the source PDF.
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import os  # noqa: E402

import pymupdf  # noqa: E402
from PIL import ImageDraw, ImageFont  # noqa: E402

import fcf_lib as L  # noqa: E402
import fcf_render as R  # noqa: E402
import finalize_report as F  # noqa: E402


def fmt(v):
    if v is None:
        return "·"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"({abs(v):,})" if v < 0 else (f"{v:,}" if v else "-")


def load(issuer, q):
    fin = os.path.join(L.DATA_DIR, f"{issuer}_{q}.json")
    auto = os.path.join(L.DATA_DIR, f"{issuer}_{q}.auto.json")
    if os.path.exists(fin) and (not os.path.exists(auto) or os.path.getmtime(fin) >= os.path.getmtime(auto)):
        return L.load_json(fin), "final (auto + overrides)"
    if not os.path.exists(auto):
        raise SystemExit("no data – run extract_report.py first")
    d = L.load_json(auto)
    if d.get("error"):
        raise SystemExit(f"auto extraction failed: {d['error']} – see review_{issuer}_{q}.txt; use tool_scan/tool_grid")
    d["geometry"] = F.auto_geometry(d)
    for c in d["columns"]:
        if c.get("months") and c.get("end"):
            c["label"] = L.period_label(c["months"], c["end"], c.get("restated"), L.is_quarter_column(c, d["columns"]))
    return d, "auto extraction (no overrides applied – run finalize_report.py to see them)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issuer")
    ap.add_argument("q", choices=["Q1", "Q2"])
    ap.add_argument("--dpi", type=int, default=220)
    ap.add_argument("--pages-dpi", type=int, default=100)
    a = ap.parse_args()
    d, src = load(a.issuer, a.q)
    out = L.temp_dir(a.issuer, f"review_{a.q}")
    for f in os.listdir(out):
        if f.endswith((".png", ".txt")):
            os.remove(os.path.join(out, f))
    import time
    st = time.strftime("%H%M%S")      # unique names: image viewers may cache files by path
    doc = pymupdf.open(os.path.join(L.WORKSPACE, d["company_folder"], d["source_file"]))
    dpi = max(200, a.dpi)
    try:
        font = ImageFont.truetype(R.FONT_BOLD, int(dpi / 72 * 7))
    except Exception:  # pragma: no cover
        font = ImageFont.load_default()
    # ---------------- fin.png: header strip + financing segments, lines framed and numbered
    segs = R.fin_segments(d)
    hp = d["header_page"]
    hg = R.geo(d, hp)
    pages_inv = sorted({hp} | {s[0] for s in segs})
    x0, x1 = R.page_x_range(d, pages_inv, pad=6)
    x0 = max(0.0, x0 - 34)          # room for the line numbers
    parts = []
    if hg.get("hdr_strip"):
        hc = pymupdf.Rect(x0, hg["hdr_strip"][0], x1, hg["hdr_strip"][1])
        parts.append(R.overlay(R.render(doc[hp - 1], hc, dpi), [(R.to_px([hc.x0 + 1, hc.y0 + 1, hc.x1 - 1, hc.y1 - 1],
                                                                           hc, dpi), R.BLUE, 3, None)]))
    for p, y0, y1 in segs:
        clip = pymupdf.Rect(x0, y0, x1, y1)
        im = R.render(doc[p - 1], clip, dpi)
        boxes = []
        for ln in d["lines"]:
            if ln["page"] == p and ln.get("bbox"):
                b = ln["bbox"]
                boxes.append((R.to_px([max(b[0], x0 + 30), b[1] - 1, b[2], b[3] + 1], clip, dpi),
                              (0, 120, 200) if ln["item"] != "total" else (0, 140, 0), 2, None))
        im = R.overlay(im, boxes)
        dr = ImageDraw.Draw(im)
        for ln in d["lines"]:
            if ln["page"] == p and ln.get("bbox"):
                b = ln["bbox"]
                px = R.to_px([x0 + 1, b[1], x0 + 30, b[3]], clip, dpi)
                dr.text((px[0] + 2, px[1]), f"#{ln['n']}", fill=(200, 0, 0), font=font)
        parts.append(im)
    R.stack(parts).save(os.path.join(out, f"fin_{st}.png"))
    # ---------------- outside crops
    for k, o in enumerate(d.get("outside", []), start=1):
        if not o.get("bbox"):
            continue
        p = o["page"]
        xa, xb = R.page_x_range(d, [p], pad=6, fallback=True)
        xa, xb = min(xa, o["bbox"][0] - 6), max(xb, o["bbox"][2] + 6)      # always the whole (*) line
        g = R.geo(d, p)
        parts = []
        if g.get("hdr_strip"):
            parts.append(R.render(doc[p - 1], pymupdf.Rect(xa, g["hdr_strip"][0], xb, g["hdr_strip"][1]), dpi))
        b = o["bbox"]
        clip = pymupdf.Rect(xa, b[1] - 6, xb, b[3] + 6)
        parts.append(R.overlay(R.render(doc[p - 1], clip, dpi),
                               [(R.to_px([clip.x0 + 1, b[1] - 3, clip.x1 - 1, b[3] + 3], clip, dpi), R.RED, 4, None)]))
        R.stack(parts).save(os.path.join(out, f"outside_{k}_{st}.png"))
    # ---------------- statement pages
    for p in d["cf_pages"]:
        doc[p - 1].get_pixmap(dpi=a.pages_dpi).save(os.path.join(out, f"page_{p}_{st}.png"))
    doc.close()
    # ---------------- lines.txt
    o = [f"{d['issuer']} {d['quarter']} – {d['company_name']} – {d['source_file']} ({d['page_count']} pp)",
         f"data: {src}; mode={d.get('mode', 'auto')}; verified={'yes' if d.get('verified') else 'NO'}",
         f"statement pages={d['cf_pages']} financing pages={d['fin_pages']} header page={hp} layout={d.get('layout')}",
         f"units={d.get('units')}", "COLUMNS (statement order, right to left):"]
    for c in d["columns"]:
        o.append(f"  {c['key']}: {c.get('label')} | months={c.get('months')} end={c.get('end')} "
                 f"restated={c.get('restated')} | header text: '{c.get('header_text')}'")
    o.append("")
    o.append("LINES (values as printed; '·' = no value read). 'key' = the number to use in override keys "
             "(line_items / line_values / drop_lines / add_lines.after ...) = the line number of the AUTO extraction; "
             "'+' = a line added by the override:")
    keys = [c["key"] for c in d["columns"]]
    o.append(" n  | key | page | item      | " + " | ".join(f"{k:>12}" for k in keys) + " | text  [flags]")
    for ln in d["lines"]:
        it = ln["item"]
        ak = "+" if ln.get("added") else ln.get("auto_n", ln["n"])
        o.append(f"{ln['n']:>3} | {str(ak):>3} | {ln['page']:>4} | {str(it):<9} | "
                 + " | ".join(f"{fmt(v):>12}" for v in ln["values"])
                 + f" | {ln['text']}" + (f"  [{'; '.join(ln.get('flags') or [])}]" if ln.get("flags") else "")
                 + (f"  {{note: {ln['note']}}}" if ln.get("note") else ""))
    tot = [ln for ln in d["lines"] if ln["item"] == "total"]
    o.append("")
    o.append("C1 (sum of mapped lines - reported total) per column: " + " | ".join(
        f"{k}={round(sum((ln['values'][i] or 0) for ln in d['lines'] if ln['item'] not in ('total', 'subtotal', 'text')) - (tot[0]['values'][i] if tot else 0), 6)}"
        for i, k in enumerate(keys)))
    o.append("")
    o.append("(*) LINES OUTSIDE FINANCING:" + ("" if d.get("outside") else " none found by the extractor – check page_*.png"))
    for k, x in enumerate(d.get("outside", []), start=1):
        o.append(f"  [{k}] {x['info']} p{x['page']} {x['section']}: {x['text']} | "
                 + " | ".join(fmt(v) for v in x["values"]) + f" | bbox={x.get('bbox')}")
    if d.get("info"):
        o.append("(*) INFO ROWS (as they will appear in the workbook): " + "; ".join(
            f"{kind}: {[fmt(v) for v in v_['values']]} note='{v_['note']}'" for kind, v_ in d["info"].items()))
    o.append("")
    o.append("REPORT FLAGS:")
    for f in d.get("flags", []):
        o.append("  - " + f)
    if d.get("verified"):
        o.append("VERIFIED: " + str(d["verified"]))
    with open(os.path.join(out, f"lines_{st}.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(o))
    print(out)


if __name__ == "__main__":
    main()
