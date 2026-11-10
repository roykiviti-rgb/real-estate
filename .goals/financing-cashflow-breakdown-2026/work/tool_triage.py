# -*- coding: utf-8 -*-
"""Triage of the automated extraction (Phase A): one row per company x quarter.

Usage: python tool_triage.py [--issuers ...] [--out <csv>]
Reads work/roles.json, work/triage_notes.json (Phase A findings per report: note + optional difficulty
override), work/data/<issuer>_<Q>.auto.json (and the finalized unverified data for C2/C3, if present).
Writes work/triage.csv (UTF-8 with BOM) and %TEMP%/fcf_run/_runs/triage_*/triage.txt.
Difficulty: A = auto-clean (C1 = 0, standard lines, no flags, no C2/C3 mismatch); B = targeted review;
C = manual entry or heavy work (text layer none/garbled, no total/units, |C1| > 2, value rows without label).
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import csv  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402

import pymupdf  # noqa: E402

import fcf_lib as L  # noqa: E402

FIELDS = ["issuer", "company", "quarter", "source_file", "cf_pages", "fin_pages", "n_columns", "columns",
          "currency", "units", "n_lines", "lines_other_or_unmapped", "outside_star_lines", "c1_per_column",
          "c2_auto", "c3_auto", "text_layer", "layout", "flags", "difficulty", "notes"]


def text_layer(path, pages):
    """Classify the text layer of the statement pages."""
    if not pages:
        return "unknown", ""
    with pymupdf.open(path) as doc:
        chars = eth = heb = img = 0
        for p in pages:
            pg = doc[p - 1]
            t = pg.get_text("text")
            chars += len(t.strip())
            eth += sum(t.count(c) for c in L.NUN_GLYPHS)
            heb += len(re.findall(r"[\u05D0-\u05EA]", t))
            for info in pg.get_image_info():
                b = pymupdf.Rect(info["bbox"]) & pg.rect
                img += b.width * b.height / max(1, pg.rect.width * pg.rect.height)
    if chars < 150:
        return "none", f"אין שכבת טקסט בעמודי הדוח (תמונה){' – כיסוי תמונה ' + str(round(img, 2)) if img else ''}"
    if eth:
        return "usable (repaired)", (f"גופן פגום: האות נ' מקודדת כתו חלופי (ð / ª / U+F8FF, {eth} מופעים) – תוקן "
                                     f"אוטומטית (כולל סדר האותיות); לאמת את טקסט השורות מול התמונה")
    return "usable", ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issuers", nargs="*")
    ap.add_argument("--out", help="default: work/triage.csv for the full set; a per-invocation file in "
                                  "%%TEMP%%/fcf_run/_runs/ when --issuers is given (never a partial triage.csv)")
    a = ap.parse_args()
    if not a.out:
        a.out = (os.path.join(L.run_dir("triage_part"), "triage_part.csv") if a.issuers
                 else os.path.join(L.WORK, "triage.csv"))
    roles = L.load_roles()
    keys = sorted(roles["sources"], key=lambda k: (int(k.split("_")[0]), k))
    tn_path = os.path.join(L.WORK, "triage_notes.json")
    tnotes = {k: v for k, v in (L.load_json(tn_path) if os.path.exists(tn_path) else {}).items()
              if not k.startswith("_")}
    final = {}
    try:
        import checks as CK
        data = CK.load_all(a.issuers, include_unverified=True)
        res = CK.run_checks(data)
        for r in res:
            if r["check"] in ("C2", "C3") and r["key"] == "total" or (r["check"] == "C3" and r["status"] == "MISMATCH"):
                final.setdefault((r["issuer"], r["check"]), []).append(r)
    except Exception as e:  # noqa: BLE001
        print("checks not available:", e)
    rows, lines_txt = [], []
    for k in keys:
        iss, q = k.split("_")
        if a.issuers and iss not in a.issuers:
            continue
        rel = roles["sources"][k]
        folder = rel.split("\\")[0]
        fname = os.path.basename(rel.replace("\\", "/"))
        p = os.path.join(L.DATA_DIR, f"{iss}_{q}.auto.json")
        d = L.load_json(p) if os.path.exists(p) else {"error": "no auto data"}
        row = {f: "" for f in FIELDS}
        row.update({"issuer": iss, "company": L.restore_quotes(folder.split(" - ", 1)[1]), "quarter": q,
                    "source_file": fname})
        notes, flags = [], []
        if d.get("error"):
            row["text_layer"], tl_note = text_layer(os.path.join(L.WORKSPACE, rel), d.get("pages") or [])
            row["flags"] = "חילוץ נכשל: " + d["error"]
            row["difficulty"] = "C"
            row["notes"] = "; ".join(x for x in [tl_note] if x)
            rows.append(row)
            continue
        row["cf_pages"] = L.page_range_text(d["cf_pages"])
        row["fin_pages"] = L.page_range_text(d["fin_pages"])
        row["n_columns"] = len(d["columns"])
        row["columns"] = " | ".join(c["label"] or f"?? '{c['header_text'][:40]}'" for c in d["columns"])
        u = d.get("units") or {}
        row["currency"], row["units"] = u.get("currency", ""), u.get("units", "")
        ln = d["lines"]
        row["n_lines"] = len([x for x in ln if x["item"] not in ("total", "text")])
        oth = [x for x in ln if x["item"] in ("other",)]
        row["lines_other_or_unmapped"] = len(oth)
        row["outside_star_lines"] = len(d.get("outside", []))
        tot = [x for x in ln if x["item"] == "total"]
        c1 = []
        for kk in range(len(d["columns"])):
            s = sum((x["values"][kk] or 0) for x in ln if x["item"] not in ("total", "subtotal", "text"))
            t = tot[0]["values"][kk] if tot else None
            c1.append(None if t is None else round(s - t, 6))
        row["c1_per_column"] = " | ".join("?" if v is None else (f"{v:,}" if v else "0") for v in c1)
        tl, tl_note = text_layer(os.path.join(L.WORKSPACE, rel), d["cf_pages"])
        row["text_layer"], row["layout"] = tl, d.get("layout", "")
        if tl_note:
            notes.append(tl_note)
        flags = list(d.get("flags", []))
        lf = sorted({f for x in ln for f in x.get("flags", []) if not f.startswith("תווית בשתי")})
        flags += lf
        for chk in ("C2", "C3"):
            rs = final.get((iss, chk), [])
            bad = [r for r in rs if r["status"] == "MISMATCH"]
            na = [r for r in rs if r["status"] == "N/A"]
            row[f"{chk.lower()}_auto"] = ("MISMATCH: " + ", ".join(f"{r['period'][:12]} {r['key']} diff={r.get('diff')}"
                                                                 for r in bad[:4])) if bad else (
                "N/A" if na and not [r for r in rs if r["status"] == "OK"] else ("OK" if rs else ""))
        row["flags"] = " ; ".join(flags)
        # difficulty
        #   C = manual entry / heavy work: no usable text layer, no total, no units, unlabeled columns with C1
        #       problems, C1 off by more than rounding (|diff| > 2: source error or misread to resolve), or a
        #       structural oddity (a value row without label text);
        #   A = auto-clean: C1 = 0, standard lines, usable text layer, no flags, no C2/C3 mismatch;
        #   B = everything else (targeted review).
        c1_bad = [v for v in c1 if v not in (0, 0.0)]
        c1_big = [v for v in c1 if v is not None and abs(v) > 2]
        no_label = [x for x in ln if x["item"] not in ("total", "text") and not (x.get("text") or "").strip()]
        cc_bad = "MISMATCH" in row["c2_auto"] or "MISMATCH" in row["c3_auto"]
        hard = (tl in ("none", "garbled") or not tot or len(c1_bad) == len(c1) and len(c1) > 0
                or any(not c["label"] for c in d["columns"]) and len(c1_bad) > 0 or not d.get("units")
                or bool(c1_big) or bool(no_label))
        clean = (not c1_bad and all(c["label"] for c in d["columns"]) and d.get("units") and not oth
                 and not any(x["item"] == "subtotal" for x in ln) and not lf and tl == "usable" and not cc_bad
                 and not any("לא נמצאה" in f or "לא זוהו" in f or "אין עמודה" in f or "שתי עמודות" in f
                             or "לאמת" in f for f in flags))
        row["difficulty"] = "C" if hard else ("A" if clean else "B")
        tn = tnotes.get(k) or {}
        if tn.get("difficulty") in ("A", "B", "C"):
            row["difficulty"] = tn["difficulty"]
        if no_label:
            notes.append("שורת ערכים ללא תווית – לבדוק (שורה מיותרת/מוזזת?)")
        if tn.get("note"):
            notes.insert(0, "[שלב A] " + tn["note"])
        row["notes"] = "; ".join(notes)
        rows.append(row)
    with open(a.out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    rd = L.run_dir("triage")
    cnt = {}
    for r in rows:
        cnt[r["difficulty"]] = cnt.get(r["difficulty"], 0) + 1
    with open(os.path.join(rd, "triage.txt"), "w", encoding="utf-8") as f:
        f.write(f"counts: {cnt}\n")
        for r in rows:
            f.write(f"{r['difficulty']} {r['issuer']:>5} {r['quarter']} p={r['cf_pages']:<10} fin={r['fin_pages']:<6} "
                    f"cols={r['n_columns']} [{r['columns']}] {r['currency']}/{r['units']} lines={r['n_lines']} "
                    f"oth={r['lines_other_or_unmapped']} out={r['outside_star_lines']} C1=[{r['c1_per_column']}] "
                    f"C2={r['c2_auto']} C3={r['c3_auto']} TL={r['text_layer']} :: {r['flags']}\n")
    print("rows:", len(rows), "counts:", cnt, "->", a.out)
    print("details:", os.path.join(rd, "triage.txt"))


if __name__ == "__main__":
    main()
