# -*- coding: utf-8 -*-
"""Extract the consolidated cash-flow statement's financing section from one quarterly report.

Usage (from any directory):
  python extract_report.py <issuer> <Q1|Q2> [--pages 55,56,57]

The source PDF is taken from work/roles.json (data source of <issuer>_<Q>); an override file may set
"source_file" and "cf_pages" (see PIPELINE.md) – they are honoured here too.
Writes  work/data/<issuer>_<Q>.auto.json   (machine extraction, NOT verified)
and     %TEMP%/fcf_run/<issuer>/review_<issuer>_<Q>.txt   (human-readable review text).
Exit code 0 = extracted (possibly with flags), 2 = extraction failed (an .auto.json with "error" is
still written so that the failure is visible to triage / finalize).
Source PDFs are opened read-only.
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import os  # noqa: E402

import fcf_extract as X  # noqa: E402
import fcf_lib as L  # noqa: E402


def review_text(d):
    o = []
    if d.get("error"):
        o.append(f"ERROR: {d['error']}")
        o += d.get("log", [])
        for s in d.get("scans", [])[:0]:
            o.append(str(s))
        for r in d.get("rows", []):
            o.append(f"  p{r['page']} [{r['kind']:>13}] [{r['section']}] {r['label']} | {r['values']}")
        return "\n".join(o)
    o.append(f"{d['issuer']} {d['quarter']}  file={d['source_file']}  pages={d['page_count']}  layout={d.get('layout')}")
    o.append(f"CF pages={d['cf_pages']} fin pages={d['fin_pages']} header page={d['header_page']}")
    o.append(f"units={d['units']}")
    for c in d["columns"]:
        o.append(f"  {c['key']}: {c['label']} | months={c['months']} end={c['end']} audit={c['audit']} "
                 f"restated={c['restated']} | hdr='{c['header_text']}'")
    o.append("FLAGS:")
    for f in d.get("flags", []):
        o.append("  - " + f)
    o.append("FINANCING LINES:")
    for ln in d["lines"]:
        o.append(f"  #{ln['n']:>2} p{ln['page']} item={ln['item']!s:>9} | {ln['text']} | raw={ln['raw']} | "
                 f"vals={ln['values']}" + (f" | flags={ln['flags']}" if ln.get("flags") else ""))
    o.append("C1 per column (sum of non-total lines - total):")
    tot = [ln for ln in d["lines"] if ln["item"] == "total"]
    for k, c in enumerate(d["columns"]):
        s = sum((ln["values"][k] or 0) for ln in d["lines"] if ln["item"] not in ("total", "subtotal", "text"))
        t = tot[0]["values"][k] if tot else None
        o.append(f"  {c['key']}: sum={s} total={t} diff={None if t is None else s - t}")
    o.append("OUTSIDE (*) candidates:")
    for x in d["outside"]:
        o.append(f"  [{x['info']}] p{x['page']} {x['section']}: {x['text']} | {x['values']}")
    o.append("ALL ROWS:")
    for r in d["all_rows"]:
        o.append(f"  p{r['page']} [{r['kind']:>13}] [{r['section']}] {r['label']} | {r['values']}")
    o += d["log"]
    return "\n".join(o)


def run(issuer, q, pages=None):
    folder = L.company_folder(issuer)
    ov_path = os.path.join(L.OVERRIDES_DIR, f"{issuer}_{q}.json")
    ov = L.load_json(ov_path) if os.path.exists(ov_path) else {}
    rel = L.source_rel(issuer, q)
    fname = ov.get("source_file") or (os.path.basename(rel.replace("\\", "/")) if rel else None)
    if not fname:
        raise SystemExit(f"no data source for {issuer} {q} in roles.json")
    path = os.path.join(L.WORKSPACE, folder, fname)
    pages = pages or ov.get("cf_pages")
    d = X.extract(path, issuer, q, folder, fname, pages=pages)
    if d.get("error"):
        d.update({"issuer": str(issuer), "quarter": q, "company_folder": folder, "source_file": fname})
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issuer")
    ap.add_argument("q", choices=["Q1", "Q2"])
    ap.add_argument("--pages")
    a = ap.parse_args()
    pages = [int(x) for x in a.pages.split(",")] if a.pages else None
    d = run(a.issuer, a.q, pages)
    d.pop("scans", None)
    L.save_json(d, os.path.join(L.DATA_DIR, f"{a.issuer}_{a.q}.auto.json"))
    rp = os.path.join(L.temp_dir(a.issuer), f"review_{a.issuer}_{a.q}.txt")
    with open(rp, "w", encoding="utf-8") as f:
        f.write(review_text(d))
    if d.get("error"):
        print("FAILED", a.issuer, a.q, d["error"], "| review:", rp)
        sys.exit(2)
    nfl = len(d.get("flags", []))
    print("ok", a.issuer, a.q, f"pages={d['cf_pages']} fin={d['fin_pages']} cols={len(d['columns'])} "
                               f"lines={len(d['lines'])} flags={nfl}")


if __name__ == "__main__":
    main()
