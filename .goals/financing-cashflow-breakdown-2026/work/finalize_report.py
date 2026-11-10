# -*- coding: utf-8 -*-
"""Combine the machine extraction (data/<issuer>_<Q>.auto.json) with the reviewed override file
(overrides/<issuer>_<Q>.json) into the final data file data/<issuer>_<Q>.json used by build_company,
checks, build_master and validate.

Usage (from any directory):  python finalize_report.py <issuer> <Q1|Q2>

Two modes (full schema and examples: work/PIPELINE.md):
  * auto   (default)  the auto extraction is the base; the override file corrects it:
        columns {"c1": {"months":6,"end":"2026-06-30","restated":false,"header_text":"...","audit":"..."}}
        units {"units_text":"אלפי ש\"ח","currency":"ש\"ח","units":"אלפים"}
        line_items {"<n>": item} | line_notes {"<n>": "..."} | line_text {"<n>": "verbatim"}
        line_values {"<n>": [v1, v2, ...]} | line_pages {"<n>": p} | line_bbox {"<n>": [x0,y0,x1,y1]}
        drop_lines [n, ...] | add_lines [{"after": n, "page": p, "text": "...", "item": 4, "values": [...],
                                          "note": "...", "bbox": [x0,y0,x1,y1]}]
        outside [ {...} ]  (replaces the auto (*) lines) | outside_drop [1-based index, ...]
        outside_sections {"<k>": "<canonical section>"}  (k = 1-based index in the FINAL (*) list; Phase C)
        fin_pages [..] | header_page p | cf_pages [..] | fin_heading {"page":p,"text":"...","bbox":[...]}
        boxes {"<p>": {"fin": [x0,y0,x1,y1], "header": [x0,y0,x1,y1]}}   (highlight geometry, PDF points)
        info_notes {"interest": "...", "dividend": "..."} (full replacement, legacy) |
        info_note_extra {"interest": "..."} (appended to the uniform note, Phase C) |
        report_notes [..] | column_notes {"c1": ".."}
        text_layer "usable" | verified {...}
        other_cf_pages {"solo": [pages], "board": [pages]}  (replaces the extractor's list of other CF-like pages –
                       38D separate data / board report; iteration 2, M8)
        consolidated false  (the company presents no consolidated statements; captions/notes name the statement
                       accordingly – iteration 2, M10) | zoom_blank_cells true (a financing cell is blank in the source;
                       the zoom legend says 'תא ריק = 0' – iteration 2, S7f)
        (*) entries may carry "sign_flipped": true (printed positive, recorded with the payment sign – decision D3;
                       the mapping note then says so – iteration 2, M5)
  * manual ("manual": true)  everything comes from the override file (for statements whose text layer
        is unusable): source_file (default = roles.json), cf_pages, fin_pages, header_page, units,
        columns [list], lines [list], outside [list], boxes (required), printed_pages {"<p>": n},
        context_sections {"<p>": ["פעילות שוטפת", ...]}, text_layer, verified.
Item codes: 1..14 | "other" | "net_loans" (4/7 by sign) | "net_bonds" (3/8 by sign) |
            "net_nci" (6/14 by sign: net NCI-transaction line) | "subtotal" | "total" | "text"
(*) lines: blank values are recorded as 0 (R4); the section of every (*) line is one of L.STAR_SECTIONS (canonical,
Phase C) and the info-row note is composed uniformly from those sections (+ optional info_note_extra).
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402

import pymupdf  # noqa: E402

import fcf_lib as L  # noqa: E402

ITEM_CODES = set(range(1, 15)) | {"other", "net_loans", "net_bonds", "net_nci", "subtotal", "total", "text"}

DEFAULT_NOTES = [
    # (predicate on text, item, note)
    (lambda t: "ואחרים" in t or "אחרים" in t, 5, "כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 לפי כלל המיפוי"),
    (lambda t: "ואחרים" in t or "אחרים" in t, 4, "כולל הלוואות ממלווים אחרים ולא רק מתאגידים בנקאיים – סעיף 4"),
    (lambda t: "ואחרים" in t or "אחרים" in t, 7, "כולל פירעון הלוואות למלווים אחרים ולא רק לתאגידים בנקאיים – סעיף 7"),
    (lambda t: "בניכוי הוצאות הנפקה" in t, 3, "תמורת הנפקת אגרות חוב נטו מהוצאות ההנפקה, כפי שמוצג בדוח"),
    (lambda t: "בניכוי הוצאות הנפקה" in t, 1, "תמורת הנפקת מניות החברה נטו מהוצאות ההנפקה, כפי שמוצג בדוח"),
    (lambda t: True, 2, "תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2"),
    (lambda t: "הנפקה" in t or "השקעת" in t, 6, "הנפקת זכויות בחברה בת מאוחדת לבעלי זכויות שאינן מקנות שליטה – סעיף 6"),
    (lambda t: True, 14, "רכישת זכויות נוספות בחברה בת מאוחדת מבעלי זכויות שאינן מקנות שליטה (עסקה הונית, ללא שינוי בשליטה) – סעיף 14"),
    (lambda t: True, 11, "דיבידנד לבעלי מניות החברה (האם), מוצג בפעילות מימון"),
    (lambda t: True, 12, "דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות"),
    (lambda t: True, 13, "ריבית ששולמה – מסווגת בדוח זה בפעילות מימון"),
    (lambda t: True, 10, "פירעון התחייבויות בגין חכירה, כפי שמוצג בדוח"),
    (lambda t: True, 8, "פירעון אגרות חוב"),
]


def default_note(item, text):
    for pred, it, note in DEFAULT_NOTES:
        if it == item and pred(text):
            return note
    return ""


def resolve(item, v):
    if item == "net_loans":
        return 4 if (v or 0) >= 0 else 7
    if item == "net_bonds":
        return 3 if (v or 0) >= 0 else 8
    if item == "net_nci":
        return 6 if (v or 0) >= 0 else 14
    return item


def norm_item(it):
    if isinstance(it, str) and it.isdigit():
        it = int(it)
    if it not in ITEM_CODES:
        raise SystemExit(f"unknown item code {it!r} (allowed: 1..14, other, net_loans, net_bonds, net_nci, subtotal, "
                         f"total, text)")
    return it


def star_note(outs, extra=""):
    """Uniform note of a (*) info row (goal R5, conventions §1, Phase C alignment E): the canonical sections of its
    lines in order of appearance, joined by ' + ', then an optional report-specific remark."""
    secs = []
    for o in outs:
        if o["section"] not in secs:
            secs.append(o["section"])
    note = " + ".join(secs)
    return f"{note}; {extra}" if extra else note


def num(v):
    """Override values may be given as numbers or as printed strings ('(1,234)', '-')."""
    if v is None or isinstance(v, (int, float)):
        return v
    s = str(v).strip()
    if s in ("", "-", "\u2013", "\u2014"):
        return 0
    return L.parse_amount(s)[0]


# ----------------------------------------------------------------------------- geometry (render boxes)
def header_bottom(pi):
    yb = pi["header_y"][1] + 5
    if pi.get("first_body_y0"):
        yb = min(yb, max(pi["header_y"][1] + 0.5, pi["first_body_y0"] - 0.8))
    return yb


def auto_geometry(d):
    """Page geometry exactly as the pilot's fcf_render computed it from the auto extraction."""
    geo = {}
    for p, pi in d.get("page_info", {}).items():
        cx = [min(pi["content_x"][0], pi["header_x"][0]), max(pi["content_x"][1], pi["header_x"][1])]
        geo[p] = {"content_x": cx, "page_rect": pi["page_rect"], "printed_page": pi.get("printed_page"),
                  "hdr_box": [pi["header_x"][0] - 4, pi["title_y"][0] - 3, pi["header_x"][1] + 4, header_bottom(pi)]
                  if pi.get("ncol") else None,
                  "hdr_strip": [pi["title_y"][0] - 4, header_bottom(pi)], "header_y1": pi["header_y"][1]}
    for p in d["fin_pages"]:
        ys = [ln["bbox"] for ln in d["lines"] if ln["page"] == p and ln.get("bbox")]
        if d.get("fin_heading") and d["fin_heading"]["page"] == p and d["fin_heading"].get("bbox"):
            ys.append(d["fin_heading"]["bbox"])
        if not ys or str(p) not in geo:
            continue
        y0, y1 = min(b[1] for b in ys), max(b[3] for b in ys)
        lim = d.get("fin_limits", {}).get(str(p))
        if lim:
            y0 = max(y0 - 4, min(y0 - 0.5, lim[0] + 0.5))
            y1 = min(y1 + 6, max(y1 + 0.5, lim[1] - 0.8))
        else:
            y0, y1 = y0 - 4, y1 + 4
        geo[str(p)]["fin_y"] = [y0, y1]
    return geo


def apply_boxes(geo, boxes, page_rects):
    """Manual boxes (PDF points, origin top-left): {"<p>": {"fin": [x0,y0,x1,y1], "header": [x0,y0,x1,y1],
    "content": [x0, x1], "printed_page": n}} ('content' = explicit x-range of the page's labels + values)."""
    for p, bx in (boxes or {}).items():
        p = str(p)
        g = geo.setdefault(p, {"content_x": None, "page_rect": page_rects.get(p), "printed_page": None,
                               "hdr_box": None, "hdr_strip": None, "header_y1": None})
        if bx.get("fin"):
            x0, y0, x1, y1 = bx["fin"]
            g["fin_y"] = [y0, y1]
            g["content_x"] = [x0 + 5, x1 - 5]       # the page highlight adds 5 pt on each side
        if bx.get("header"):
            x0, y0, x1, y1 = bx["header"]
            g["hdr_box"] = [x0, y0, x1, y1]
            g["hdr_strip"] = [y0 - 1, y1]           # same relation as the auto geometry (box = strip + 1 pt)
            g["header_y1"] = y1
            if g.get("content_x") is None:
                g["content_x"] = [x0 + 4, x1 - 4]   # the header box adds 4 pt on each side
            else:
                g["content_x"] = [min(g["content_x"][0], x0 + 4), max(g["content_x"][1], x1 - 4)]
        if bx.get("printed_page") is not None:
            g["printed_page"] = bx["printed_page"]
        if bx.get("content"):
            g["content_x"] = [float(bx["content"][0]), float(bx["content"][1])]   # explicit x-range of the page content
    return geo


# ----------------------------------------------------------------------------- build final data
def load_override(issuer, q):
    p = os.path.join(L.OVERRIDES_DIR, f"{issuer}_{q}.json")
    return L.load_json(p) if os.path.exists(p) else {}


def base_from_manual(issuer, q, ov):
    folder = L.company_folder(issuer)
    rel = L.source_rel(issuer, q)
    fname = ov.get("source_file") or os.path.basename(rel.replace("\\", "/"))
    with pymupdf.open(os.path.join(L.WORKSPACE, folder, fname)) as doc:
        page_count = doc.page_count
        page_rects = {str(i + 1): [doc[i].rect.width, doc[i].rect.height] for i in range(doc.page_count)}
    for k in ("cf_pages", "fin_pages", "header_page", "units", "columns", "lines", "boxes"):
        if k not in ov:
            raise SystemExit(f"manual override for {issuer} {q} lacks '{k}'")
    cols = []
    for k, c in enumerate(ov["columns"], start=1):
        cols.append({"key": c.get("key", f"c{k}"), "header_text": c.get("header_text", ""), "months": c["months"],
                     "end": c["end"], "restated": bool(c.get("restated")), "audit": c.get("audit", "")})
    lines = []
    for n, ln in enumerate(ov["lines"], start=1):
        lines.append({"n": n, "page": ln.get("page", ov["fin_pages"][0]), "text": ln["text"],
                      "item": norm_item(ln["item"]), "note": ln.get("note", ""),
                      "values": [num(v) for v in ln.get("values", [None] * len(cols))],
                      "raw": ln.get("raw"), "bbox": ln.get("bbox"), "flags": []})
    fh = ov.get("fin_heading") or {"page": ov["fin_pages"][0], "text": "תזרימי מזומנים מפעילות מימון", "bbox": None}
    d = {"issuer": str(issuer), "company_folder": folder, "company_name": L.restore_quotes(folder.split(" - ", 1)[1]),
         "quarter": q, "report_label": f"{q} 2026", "report_id": re.search(r"_(\d+)(?:-\d+)?\.pdf$", fname).group(1),
         "source_file": fname, "page_count": page_count, "cf_pages": ov["cf_pages"], "fin_pages": ov["fin_pages"],
         "header_page": ov["header_page"], "fin_heading": fh, "units": ov["units"], "columns": cols,
         "lines": lines, "outside": ov.get("outside", []), "page_info": {}, "fin_limits": {},
         "context_sections": ov.get("context_sections", {}), "other_cf_pages": ov.get("other_cf_pages", {}),
         "layout": ov.get("layout", "rtl"), "flags": [], "mode": "manual"}
    geo = {}
    for p, n in (ov.get("printed_pages") or {}).items():
        geo.setdefault(str(p), {"content_x": None, "page_rect": page_rects.get(str(p)), "printed_page": n,
                                "hdr_box": None, "hdr_strip": None, "header_y1": None})
    d["geometry"] = apply_boxes(geo, ov["boxes"], page_rects)
    for p in [str(x) for x in d["cf_pages"]]:
        d["geometry"].setdefault(p, {"content_x": None, "page_rect": page_rects.get(p), "printed_page": None,
                                     "hdr_box": None, "hdr_strip": None, "header_y1": None})
    return d


def apply_auto_overrides(auto, ov):
    d = dict(auto)
    d.pop("all_rows", None)
    d.pop("log", None)
    d["mode"] = "auto"
    if ov.get("source_file") and ov["source_file"] != d["source_file"]:
        raise SystemExit(f"override source_file {ov['source_file']} differs from the auto extraction "
                         f"({d['source_file']}) – re-run extract_report.py first")
    if ov.get("units"):
        d["units"] = ov["units"]
    for c in d["columns"]:
        for k, v in ov.get("columns", {}).get(c["key"], {}).items():
            if k in ("months", "end", "restated", "header_text", "audit"):
                c[k] = v
    lines = [dict(ln) for ln in d["lines"]]
    for ln in lines:
        k = str(ln["n"])
        if k in ov.get("line_items", {}):
            ln["item"] = norm_item(ov["line_items"][k])
        if k in ov.get("line_text", {}):
            ln["text"] = ov["line_text"][k]
        if k in ov.get("line_values", {}):
            ln["values"] = [num(v) for v in ov["line_values"][k]]
            ln["values_overridden"] = True
        if k in ov.get("line_pages", {}):
            ln["page"] = ov["line_pages"][k]
        if k in ov.get("line_bbox", {}):
            ln["bbox"] = ov["line_bbox"][k]
        if k in ov.get("line_notes", {}):
            ln["note"] = ov["line_notes"][k]
            ln["note_overridden"] = True
    drop = {int(x) for x in ov.get("drop_lines", [])}
    out = []
    adds = sorted(ov.get("add_lines", []), key=lambda a: a.get("after", 0))
    for a in [a for a in adds if a.get("after", 0) == 0]:
        out.append(added_line(a, d))
    for ln in lines:
        if ln["n"] not in drop:
            out.append(ln)
        for a in [a for a in adds if a.get("after") == ln["n"]]:
            out.append(added_line(a, d))
    for i, ln in enumerate(out, start=1):
        ln["auto_n"] = ln.get("n")
        ln["n"] = i
    d["lines"] = out
    if "outside" in ov:
        d["outside"] = ov["outside"]
    else:
        drop_o = {int(x) for x in ov.get("outside_drop", [])}
        d["outside"] = [o for i, o in enumerate(d.get("outside", []), start=1) if i not in drop_o]
        d["outside"] += ov.get("outside_add", [])
    for k in ("fin_pages", "header_page", "cf_pages", "fin_heading", "context_sections", "other_cf_pages"):
        if k in ov:
            d[k] = ov[k]
    geo = auto_geometry(d)
    page_rects = {p: g["page_rect"] for p, g in geo.items()}
    d["geometry"] = apply_boxes(geo, ov.get("boxes"), page_rects)
    return d


def added_line(a, d):
    return {"n": None, "page": a.get("page", d["fin_pages"][0]), "text": a["text"], "item": norm_item(a["item"]),
            "note": a.get("note", ""), "values": [num(v) for v in a["values"]], "raw": a.get("raw"),
            "bbox": a.get("bbox"), "flags": ["שורה שנוספה ידנית"], "added": True}


def finalize(issuer, q):
    ov = load_override(issuer, q)
    auto_p = os.path.join(L.DATA_DIR, f"{issuer}_{q}.auto.json")
    if ov.get("manual"):
        d = base_from_manual(issuer, q, ov)
    else:
        if not os.path.exists(auto_p):
            raise SystemExit(f"no auto extraction {auto_p} – run extract_report.py (or use a manual override)")
        auto = L.load_json(auto_p)
        if auto.get("error"):
            raise SystemExit(f"auto extraction failed ({auto['error']}) – fix with cf_pages / a manual override")
        d = apply_auto_overrides(auto, ov)
    ncol = len(d["columns"])
    # ---------------- columns: labels (T2 month range for quarterly 3-month columns)
    for c in d["columns"]:
        if not (c.get("months") and c.get("end")):
            raise SystemExit(f"column {c['key']} has no months/end – add an override "
                             f"(columns.{c['key']}.months / .end); header text: {c.get('header_text')!r}")
        c["label"] = L.period_label(c["months"], c["end"], c.get("restated"), L.is_quarter_column(c, d["columns"]))
        c["label_full"] = f"דוח {d['report_label']} | {c['label']}"
    # ---------------- lines
    for ln in d["lines"]:
        if len(ln["values"]) != ncol:
            raise SystemExit(f"line {ln['n']} '{ln['text']}' has {len(ln['values'])} values, expected {ncol}")
        if ln["item"] in range(1, 15) and not ln.get("note"):
            ln["note"] = default_note(ln["item"], ln["text"])
        if ln["item"] == "total" and not ln.get("note"):
            ln["note"] = "שורת הסה\"כ המדווחת של פעילות המימון"
        if ln["item"] == "subtotal":
            ln["note"] = L.SUBTOTAL_TAG if not ln.get("note") or ln["note"] == L.SUBTOTAL_TAG else (
                ln["note"] if L.SUBTOTAL_TAG in ln["note"] else f"{L.SUBTOTAL_TAG} \u2013 {ln['note']}")
        ln["resolved"] = [resolve(ln["item"], v) for v in ln["values"]]
        if ln["item"] not in ("text", "subtotal"):
            for v in ln["values"]:
                if v is None:
                    raise SystemExit(f"line {ln['n']} '{ln['text']}' has a missing value: {ln['values']} – "
                                     f"set line_values or check the extraction")
    totals = [ln for ln in d["lines"] if ln["item"] == "total"]
    if len(totals) != 1:
        raise SystemExit(f"expected exactly one total line, got {len(totals)}")
    total = totals[0]["values"]
    items = {str(i): [0] * ncol for i in range(1, 15)}
    other = [0] * ncol
    for ln in d["lines"]:
        if ln["item"] in ("total", "subtotal", "text"):
            continue
        for k in range(ncol):
            it = ln["resolved"][k]
            v = ln["values"][k] or 0
            if it == "other":
                other[k] += v
            else:
                items[str(it)][k] += v
    rnd = (lambda x: round(x, 6)) if any(isinstance(v, float) for ln in d["lines"] for v in ln["values"] if v) else (lambda x: x)
    items = {i: [rnd(v) for v in vs] for i, vs in items.items()}
    other = [rnd(v) for v in other]
    check = [rnd(sum(items[str(i)][k] for i in range(1, 15)) + other[k] - total[k]) for k in range(ncol)]
    d["items"], d["other"], d["total"], d["check"] = items, other, total, check
    # ---------------- (*) info rows
    outs_all = d.get("outside", [])
    for i, o in enumerate(outs_all):
        if o["section"] == L.SECTION_APPX_AUTO:      # extractor's generic appendix label -> "section not stated"
            outs_all[i] = dict(o, section=L.SECTION_APPX_UNSTATED)
    for k_s, sec in (ov.get("outside_sections") or {}).items():
        i = int(k_s) - 1
        if not 0 <= i < len(outs_all):
            raise SystemExit(f"outside_sections key {k_s}: no such (*) line (have {len(outs_all)})")
        outs_all[i] = dict(outs_all[i], section=sec)
    for o in outs_all:
        if o["section"] not in L.STAR_SECTIONS:
            raise SystemExit(f"(*) line '{o.get('text')}': section {o['section']!r} is not canonical "
                             f"({L.STAR_SECTIONS}) – set outside_sections")
    info = {}
    for kind, fin_items in (("interest", (13,)), ("dividend", (11, 12))):
        outs = [o for o in outs_all if o["info"] == kind]
        for o in outs:
            o["values"] = [0 if v is None else v for v in (num(v) for v in o["values"])]   # blank -> 0 (R4)
            if len(o["values"]) != ncol:
                raise SystemExit(f"outside line '{o.get('text')}' has {len(o['values'])} values, expected {ncol}")
        vals = [rnd(sum((o["values"][k] or 0) for o in outs)) for k in range(ncol)]
        in_fin = any(ln["item"] in fin_items for ln in d["lines"])
        if outs:
            note = star_note(outs, (ov.get("info_note_extra") or {}).get(kind, ""))
        elif in_fin:
            note = ""
        else:
            note = ov.get("info_notes", {}).get(kind, L.NOT_SEPARATE_NOTE if kind == "interest" else "")
        if outs and ov.get("info_notes", {}).get(kind):
            raise SystemExit(f"info_notes.{kind} with (*) lines is no longer supported – the note is composed from the "
                             f"canonical sections; use info_note_extra for a report-specific remark")
        info[kind] = {"values": vals, "note": note, "presented_in_financing": in_fin}
    d["info"] = info
    d["report_notes"] = ov.get("report_notes", [])
    d["column_notes"] = ov.get("column_notes", {})
    d["issues"] = ov.get("issues", [])
    # iteration 2: statement kind (M10), blank source cells in the financing section (S7f), other CF-like pages (M8);
    # the keys are written only when the override sets them (absent = consolidated statement, no blank cells)
    if "consolidated" in ov:
        d["consolidated"] = bool(ov["consolidated"])
    if "zoom_blank_cells" in ov:
        d["zoom_blank_cells"] = bool(ov["zoom_blank_cells"])
    oc = d.get("other_cf_pages") or {}
    if not isinstance(oc, dict) or any(k not in ("solo", "board") or not all(isinstance(p, int) for p in v)
                                       for k, v in oc.items()):
        raise SystemExit(f"other_cf_pages must be {{'solo': [pages], 'board': [pages]}}, got {oc!r}")
    d["text_layer"] = ov.get("text_layer", d.get("text_layer"))
    d["verified"] = ov.get("verified")
    if d["verified"] and d["verified"].get("status") != "verified":
        raise SystemExit("verified.status must be 'verified' (or remove the record)")
    L.save_json(d, os.path.join(L.DATA_DIR, f"{issuer}_{q}.json"))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issuer")
    ap.add_argument("q", choices=["Q1", "Q2"])
    ap.add_argument("--allow-unverified", action="store_true", help="accepted for compatibility (no effect)")
    a = ap.parse_args()
    d = finalize(a.issuer, a.q)
    st = "VERIFIED" if d.get("verified") else "UNVERIFIED (draft)"
    print(a.issuer, a.q, st, "check:", d["check"], "total:", d["total"])


if __name__ == "__main__":
    main()
