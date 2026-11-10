# -*- coding: utf-8 -*-
"""Build the per-company outputs from final data (data/<issuer>_<Q>.json):
  <company folder>/<issuer> - פירוט תזרים מימון 2026.xlsx
  <company folder>/<issuer> - צילומי מסך תזרים מימון 2026.pdf

Usage: python build_company.py <issuer> [--draft] [--no-pdf]
  --draft   allow unverified (auto) reports; the outputs are then marked as drafts ('טיוטה'). Without it,
            every report of the company must carry a verification record (override "verified").
Writes only the two files of this company (temp files: %TEMP%/fcf_run/<issuer>/, unique per process).
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import datetime as dt  # noqa: E402
import glob  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402

import openpyxl  # noqa: E402
import pymupdf  # noqa: E402
from openpyxl.formatting.rule import CellIsRule  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

import fcf_lib as L  # noqa: E402

NUMFMT = '#,##0;-#,##0;0'
DATEFMT = "DD.MM.YYYY"
F_BOLD = Font(name="Arial", bold=True)
F_TITLE = Font(name="Arial", bold=True, size=14)
F_NORM = Font(name="Arial")
F_SMALL = Font(name="Arial", size=9, color="404040")
F_RED = Font(name="Arial", bold=True, color="C00000")
FILL_HDR = PatternFill("solid", fgColor="D9E1F2")
FILL_META = PatternFill("solid", fgColor="F2F2F2")
FILL_GRP = PatternFill("solid", fgColor="FFF2CC")
FILL_TOT = PatternFill("solid", fgColor="E2EFDA")
FILL_INFO = PatternFill("solid", fgColor="FBE5D6")
FILL_RED = PatternFill("solid", fgColor="FFC7CE")
THIN = Side(style="thin", color="A6A6A6")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
TOPB = Border(top=Side(style="medium", color="000000"), bottom=THIN, left=THIN, right=THIN)
WRAP = Alignment(wrap_text=True, vertical="top", horizontal="right", readingOrder=2)
RIGHT = Alignment(horizontal="right", vertical="top", readingOrder=2)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True, readingOrder=2)


def xlsx_name(issuer):
    return f"{issuer} - פירוט תזרים מימון 2026.xlsx"


def pdf_name(issuer):
    return f"{issuer} - צילומי מסך תזרים מימון 2026.pdf"


def load_reports(issuer):
    out = []
    for q in ("Q1", "Q2"):
        p = os.path.join(L.DATA_DIR, f"{issuer}_{q}.json")
        if os.path.exists(p):
            out.append(L.load_json(p))
    return out


def iso_to_date(s):
    y, m, d = (int(x) for x in s.split("-"))
    return dt.datetime(y, m, d)


def file_inventory(folder, reports, roles=None):
    """Rows for the 'מקורות' sheet / master file index for one company folder (source PDFs only,
    taken from the baseline list so that our own outputs are never listed). roles = roles.json."""
    rfiles = (roles or {}).get("files", {})
    rows = []
    base = L.baseline_files()
    srcs = sorted(rel for rel in base if rel.split("\\")[0] == folder and rel.lower().endswith(".pdf"))
    for rel in srcs:
        path = os.path.join(L.WORKSPACE, rel)
        f = os.path.basename(rel.replace("\\", "/"))
        m = re.search(r"_2026_(Q[1-4])_(\d+)(-\d+)?\.pdf$", f)
        q, rid, suf = (m.group(1), m.group(2), m.group(3)) if m else ("", "", None)
        rinfo = rfiles.get(rel, {})
        npages = rinfo.get("pages")
        if npages is None:
            with pymupdf.open(path) as doc:
                npages = doc.page_count
        used = [d for d in reports if d["source_file"] == f]
        if used:
            d = used[0]
            role = L.ROLE_MAIN
            cf = L.page_range_text(d["cf_pages"])
            fin = L.page_range_text(d["fin_pages"])
            printed = [(d.get("geometry", {}).get(str(p)) or {}).get("printed_page") for p in d["cf_pages"]]
            pr = f" (עמודים מודפסים {L.page_range_text([x for x in printed if x])})" if all(printed) else ""
            other = d.get("other_cf_pages", {})
            extra = []
            if other.get("solo"):
                extra.append(f"נתונים כספיים נפרדים (תקנה 38ד) – עמ' {L.page_range_text(other['solo'])}")
            if other.get("board"):
                extra.append(f"סיכום תזרים בדוח הדירקטוריון – עמ' {L.page_range_text(other['board'])}")
            lead = "דוח רבעוני מלא" if not suf else rinfo.get("note", "דוח רבעוני מלא (צורף כנספח)").rstrip(".")
            note = (f"{lead}; {L.cf_statement_name(d)} בעמודי PDF {cf}{pr}; פעילות המימון בעמוד {fin}."
                    + (" לא בשימוש (מחוץ להיקף): " + "; ".join(extra) + "." if extra else ""))
        else:
            role = rinfo.get("role", "לבדיקה")
            cf = fin = ""
            note = rinfo.get("note", "")
        rows.append({"file": f, "rel": rel, "quarter": f"{q} 2026" if q else "",
                     "report_id": rid + (suf or ""), "pages": npages, "role": role,
                     "used": "כן" if used else "לא", "cf_pages": cf, "fin_pages": fin, "note": note})
    return rows


def lines_for_item(reports, item):
    seen = []
    for d in reports:
        for ln in d["lines"]:
            if item in ln["resolved"] or ln["item"] == item:
                tag = d["quarter"]
                hit = [s for s in seen if s[0] == ln["text"]]
                if hit:
                    if tag not in hit[0][1]:
                        hit[0][1].append(tag)
                else:
                    seen.append([ln["text"], [tag]])
    return "; ".join(f"{t} ({', '.join(q)})" for t, q in seen)


def set_cell(ws, r, c, v, font=None, fill=None, fmt=None, align=None, border=None):
    cell = ws.cell(row=r, column=c, value=v)
    if font:
        cell.font = font
    if fill:
        cell.fill = fill
    if fmt:
        cell.number_format = fmt
    if align:
        cell.alignment = align
    if border:
        cell.border = border
    return cell


def build_xlsx(issuer, reports, out_path, roles=None, draft=False):
    d0 = reports[0]
    cols = [(d, k, c) for d in reports for k, c in enumerate(d["columns"])]
    ncol = len(cols)
    C0 = 3  # first period column
    NOTE_C = C0 + ncol
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "פירוט מימון"
    ws.sheet_view.rightToLeft = True
    # ---------------- header block
    set_cell(ws, 1, 1, "פירוט תזרים מזומנים מפעילות מימון – דוחות 2026", F_TITLE, align=RIGHT)
    if draft:
        set_cell(ws, 1, 3, "טיוטה – חילוץ אוטומטי שטרם אומת ויזואלית; אין להשתמש בנתונים לפני אימות", F_RED,
                 align=Alignment(horizontal="right", vertical="top", wrap_text=False, readingOrder=2))
    curs = sorted({d["units"]["currency"] for d in reports})
    units = sorted({d["units"]["units"] for d in reports})
    utext = sorted({d["units"]["units_text"] for d in reports})
    have_q1 = any(d["quarter"] == "Q1" for d in reports)
    cons_all = all(d.get("consolidated", True) for d in reports)
    stmt = L.CF_NAME_CONS if cons_all else (L.CF_NAME_SOLE if not any(d.get("consolidated", True) for d in reports)
                                           else "הדוח (המאוחד) על תזרימי המזומנים")
    meta = [
        ("שם החברה", d0["company_name"]),
        ("מספר מנפיק", int(issuer)),
        ("מטבע", " / ".join(curs)),
        ("יחידות", " / ".join(units) + f" (כפי שמופיע בדוח: {', '.join(utext)})"),
        ("דוחות בתיקייה", ", ".join(f"{d['report_label']}" for d in reports)),
        ("סימון", f"הסכומים הועתקו כפי שדווחו ב{stmt[1:]} (ללא עיגול, המרה או שינוי יחידות); "
                  "תקבולים בחיוב, תשלומים בשלילה (בדוח – בסוגריים); \"-\" בדוח = 0."),
        ("צילומי מסך", pdf_name(issuer)),
    ]
    r = 2
    for k, v in meta:
        set_cell(ws, r, 2, k, F_BOLD, align=RIGHT)
        set_cell(ws, r, 3, v, F_NORM, align=Alignment(horizontal="right", vertical="top", wrap_text=False, readingOrder=2))
        r += 1
    if not have_q1:
        set_cell(ws, r, 2, "הערה", F_BOLD, align=RIGHT)
        set_cell(ws, r, 3, L.MISSING_Q1_TEXT, F_RED, align=RIGHT)
        r += 1
    r += 1
    # ---------------- column header rows
    HDR = r
    set_cell(ws, HDR, 1, "מס'", F_BOLD, FILL_HDR, align=CENTER, border=BOX)
    set_cell(ws, HDR, 2, "סעיף", F_BOLD, FILL_HDR, align=CENTER, border=BOX)
    for j, (d, k, c) in enumerate(cols):
        set_cell(ws, HDR, C0 + j, c["label_full"], F_BOLD, FILL_HDR, align=CENTER, border=BOX)
    set_cell(ws, HDR, NOTE_C, "הערות / שורות המקור שמופו לסעיף", F_BOLD, FILL_HDR, align=CENTER, border=BOX)
    meta_rows = [
        ("קובץ מקור", lambda d, k, c: d["source_file"], None),
        ("עמוד PDF (פעילות מימון)", lambda d, k, c: L.page_range_text(d["fin_pages"]), None),
        ("כותרת העמודה בדוח (מילולית)", lambda d, k, c: c["header_text"], None),
        ("חודשים", lambda d, k, c: c["months"], "0"),
        ("תאריך סוף התקופה", lambda d, k, c: iso_to_date(c["end"]), DATEFMT),
        ("מוצג מחדש", lambda d, k, c: "כן" if c["restated"] else "לא", None),
        ("יחידות ומטבע (כפי שבדוח)", lambda d, k, c: d["units"]["units_text"], None),
    ]
    r = HDR + 1
    F_TINY = Font(name="Arial", size=8, color="404040")
    for lab, fn, fmt in meta_rows:
        set_cell(ws, r, 2, lab, F_SMALL, FILL_META, align=RIGHT, border=BOX)
        set_cell(ws, r, 1, None, None, FILL_META, border=BOX)
        for j, (d, k, c) in enumerate(cols):
            set_cell(ws, r, C0 + j, fn(d, k, c), F_TINY if lab == "קובץ מקור" else F_SMALL, FILL_META, fmt=fmt,
                     align=CENTER, border=BOX)
        set_cell(ws, r, NOTE_C, None, None, FILL_META, border=BOX)
        if lab == "קובץ מקור":
            ws.row_dimensions[r].height = 36
        r += 1
    # ---------------- table
    rows_idx = {}

    def group_row(label):
        nonlocal r
        set_cell(ws, r, 1, None, None, FILL_GRP, border=BOX)
        set_cell(ws, r, 2, label, F_BOLD, FILL_GRP, align=RIGHT, border=BOX)
        for j in range(ncol + 1):
            set_cell(ws, r, C0 + j, None, None, FILL_GRP, border=BOX)
        r += 1

    def value_row(num, label, values, note, font=F_NORM, fill=None, border=BOX, key=None):
        nonlocal r
        set_cell(ws, r, 1, num, font, fill, align=CENTER, border=border)
        set_cell(ws, r, 2, label, font, fill, align=RIGHT, border=border)
        for j, v in enumerate(values):
            set_cell(ws, r, C0 + j, v, font, fill, fmt=NUMFMT, align=Alignment(horizontal="right"), border=border)
        set_cell(ws, r, NOTE_C, note, F_SMALL, fill, align=WRAP, border=border)
        if key is not None:
            rows_idx[key] = r
        r += 1

    group_row(L.GROUP_IN)
    for i in range(1, 7):
        value_row(i, L.ITEM_LABEL[i], [d["items"][str(i)][k] for d, k, c in cols], lines_for_item(reports, i), key=i)
    group_row(L.GROUP_OUT)
    for i in range(7, 15):
        value_row(i, L.ITEM_LABEL[i], [d["items"][str(i)][k] for d, k, c in cols], lines_for_item(reports, i), key=i)
    value_row("\u2014", L.OTHER_LABEL, [d["other"][k] for d, k, c in cols],
              lines_for_item(reports, "other") or "אין שורות שאינן מתאימות לסעיפים 1–14", key="other")
    value_row("=", L.TOTAL_LABEL, [d["total"][k] for d, k, c in cols],
              "הסה\"כ כפי שדווח בדוח: " + lines_for_item(reports, "total"), font=F_BOLD, fill=FILL_TOT,
              border=TOPB, key="total")
    # check row (live formula)
    CHK = r
    set_cell(ws, r, 1, None, border=BOX)
    set_cell(ws, r, 2, L.CHECK_LABEL, Font(name="Arial", italic=True, color="375623"), align=RIGHT, border=BOX)
    for j in range(ncol):
        col = get_column_letter(C0 + j)
        f = (f"=SUM({col}{rows_idx[1]}:{col}{rows_idx[6]})+SUM({col}{rows_idx[7]}:{col}{rows_idx[14]})"
             f"+{col}{rows_idx['other']}-{col}{rows_idx['total']}")
        set_cell(ws, r, C0 + j, f, Font(name="Arial", italic=True, color="375623"), fmt=NUMFMT,
                 align=Alignment(horizontal="right"), border=BOX)
    set_cell(ws, r, NOTE_C, "חייב להיות 0 בכל עמודה (נוסחה חיה)", F_SMALL, align=WRAP, border=BOX)
    ws.conditional_formatting.add(f"{get_column_letter(C0)}{CHK}:{get_column_letter(C0 + ncol - 1)}{CHK}",
                                  CellIsRule(operator="notEqual", formula=["0"], fill=FILL_RED))
    r += 1
    # (*) info rows
    for kind, label in (("interest", L.INFO_INT_LABEL), ("dividend", L.INFO_DIV_LABEL)):
        notes = []
        for d in reports:
            inf = d["info"][kind]
            if inf["note"]:
                notes.append(f"{d['report_label']}: {inf['note']}")
        if not notes:
            fin_txt = "ריבית ששולמה מוצגת" if kind == "interest" else "דיבידנד ששולם מוצג"
            sentence = f"אין סכומים מחוץ לפעילות מימון ({fin_txt} בדוח בפעילות מימון)"
            pres = [d for d in reports if d["info"][kind]["presented_in_financing"]]
            if pres and len(pres) == len(reports):
                notes.append(sentence)
            else:   # iteration 2, S4: presented in financing in some reports only (none paid in the others)
                notes += [f"{d['report_label']}: {sentence}" for d in pres]
        value_row("(*)", label, [d["info"][kind]["values"][k] for d, k, c in cols], " | ".join(n for n in notes if n),
                  font=F_NORM, fill=FILL_INFO)
    # notes row (per column)
    set_cell(ws, r, 1, None, border=BOX)
    set_cell(ws, r, 2, "הערות", F_BOLD, align=RIGHT, border=BOX)
    for j, (d, k, c) in enumerate(cols):
        set_cell(ws, r, C0 + j, d.get("column_notes", {}).get(c["key"], ""), F_SMALL, align=WRAP, border=BOX)
    set_cell(ws, r, NOTE_C, "הערות כלליות – ראו מטה", F_SMALL, align=WRAP, border=BOX)
    NOTES_ROW = r
    r += 2
    set_cell(ws, r, 2, "הערות כלליות:", F_BOLD, align=RIGHT)
    r += 1
    general = []
    for d in reports:
        for n in d.get("report_notes", []):
            general.append(f"דוח {d['report_label']}: {n}")
    general.append("שורות (*) הן לידיעה בלבד ואינן נכללות בסכום הסעיפים ובשורת הבדיקה.")
    general.append("פירוט המיפוי של כל שורה מקורית לסעיף – בגיליון 'מיפוי שורות'; רשימת הקבצים בתיקייה – בגיליון 'מקורות'.")
    for n in general:
        set_cell(ws, r, 2, n, F_NORM, align=Alignment(horizontal="right", vertical="top", wrap_text=False, readingOrder=2))
        r += 1
    # widths / heights / freeze
    ws.column_dimensions["A"].width = 6
    ws.column_dimensions["B"].width = 50
    for j in range(ncol):
        ws.column_dimensions[get_column_letter(C0 + j)].width = 24
    ws.column_dimensions[get_column_letter(NOTE_C)].width = 70
    ws.row_dimensions[HDR].height = 48
    ws.row_dimensions[HDR + 3].height = 54
    ws.row_dimensions[NOTES_ROW].height = 120
    ws.freeze_panes = ws.cell(row=HDR + 1, column=C0)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    # ---------------- sheet 2: line mapping
    ws2 = wb.create_sheet("מיפוי שורות")
    ws2.sheet_view.rightToLeft = True
    r = 1
    set_cell(ws2, r, 1, "מיפוי כל שורה מקורית בסעיף פעילות המימון (ושורות (*) מחוץ לו) לסעיפי הפירוט", F_TITLE, align=RIGHT)
    r += 2
    maxv = max(len(d["columns"]) for d in reports)
    for d in reports:
        title = (f"דוח {d['report_label']} – קובץ: {d['source_file']} – {L.cf_statement_name(d)} בעמודי PDF "
                 f"{L.page_range_text(d['cf_pages'])}; פעילות המימון בעמוד {L.page_range_text(d['fin_pages'])}")
        set_cell(ws2, r, 1, title, F_BOLD, FILL_GRP, align=RIGHT)
        for c in range(2, 7 + maxv):
            set_cell(ws2, r, c, None, None, FILL_GRP)
        r += 1
        heads = ["מס' שורה", "עמוד PDF", "טקסט השורה המקורי (מילולית)", "מס' סעיף", "שם הסעיף", "הערת סיווג / נימוק"]
        heads += [c["label"] for c in d["columns"]]
        for j, h in enumerate(heads):
            set_cell(ws2, r, 1 + j, h, F_BOLD, FILL_HDR, align=CENTER, border=BOX)
        r += 1
        first = r
        for ln in d["lines"]:
            it = ln["item"]
            if it == "total":
                num, lab = "=", L.TOTAL_LABEL
            elif it == "subtotal":
                num, lab = "סיכום ביניים", L.SUBTOTAL_TAG
            elif it == "other":
                num, lab = "\u2014", L.OTHER_LABEL
            elif it == "net_loans":
                num, lab = "4/7", f"{L.ITEM_LABEL[4]} / {L.ITEM_LABEL[7]} (לפי סימן בכל תקופה)"
            elif it == "net_bonds":
                num, lab = "3/8", f"{L.ITEM_LABEL[3]} / {L.ITEM_LABEL[8]} (לפי סימן בכל תקופה)"
            elif it == "net_nci":
                num, lab = "6/14", f"{L.ITEM_LABEL[6]} / {L.ITEM_LABEL[14]} (לפי סימן בכל תקופה)"
            elif it == "text":
                num, lab = "", "שורת טקסט"
            else:
                num, lab = it, L.ITEM_LABEL[it]
            fnt = F_BOLD if it == "total" else F_NORM
            fill = FILL_TOT if it == "total" else None
            vals = [ln["page"], ln["text"], num, lab, ln.get("note", "")]
            for j, v in enumerate([ln["n"]] + vals):
                set_cell(ws2, r, 1 + j, v, fnt, fill, align=WRAP if j in (2, 4, 5) else CENTER, border=BOX)
            for j, v in enumerate(ln["values"]):
                set_cell(ws2, r, 7 + j, v, fnt, fill, fmt=NUMFMT, align=Alignment(horizontal="right", vertical="top"),
                         border=BOX)
            r += 1
        last = r - 1
        # check row: mapped lines (excluding total/subtotal) minus total
        set_cell(ws2, r, 3, "בדיקה: סכום השורות שמופו לסעיפים (ללא סה\"כ/סיכומי ביניים) פחות הסה\"כ המדווח",
                 Font(name="Arial", italic=True, color="375623"), align=WRAP, border=BOX)
        for j in range(len(d["columns"])):
            col = get_column_letter(7 + j)
            rng_i = f"D{first}:D{last}"
            rng_v = f"{col}{first}:{col}{last}"
            f = (f'=SUMPRODUCT(({rng_i}<>"=")*({rng_i}<>"סיכום ביניים")*({rng_v}))'
                 f'-SUMPRODUCT(({rng_i}="=")*({rng_v}))')
            set_cell(ws2, r, 7 + j, f, Font(name="Arial", italic=True, color="375623"), fmt=NUMFMT,
                     align=Alignment(horizontal="right"), border=BOX)
        r += 1
        # (*) lines outside financing
        for o in d.get("outside", []):
            vals = [o["page"], o["text"], "לידיעה", L.OUTSIDE_TAG, L.star_mapping_note(o)]
            for j, v in enumerate(["*"] + vals):
                set_cell(ws2, r, 1 + j, v, F_NORM, FILL_INFO, align=WRAP if j in (2, 4, 5) else CENTER, border=BOX)
            for j, v in enumerate(o["values"]):
                set_cell(ws2, r, 7 + j, v, F_NORM, FILL_INFO, fmt=NUMFMT, border=BOX)
            r += 1
        if not d.get("outside"):
            set_cell(ws2, r, 3, "שורות (*) מחוץ לפעילות מימון: אין – ריבית ששולמה ודיבידנד ששולם מוצגים בדוח בפעילות "
                                "המימון בלבד" if all(d["info"][k]["presented_in_financing"] for k in ("interest", "dividend"))
                     else "שורות (*) מחוץ לפעילות מימון: אין", F_SMALL, align=RIGHT)
            r += 1
        r += 1
    widths = [8, 9, 48, 9, 34, 46] + [19] * maxv
    for j, w in enumerate(widths):
        ws2.column_dimensions[get_column_letter(1 + j)].width = w

    # ---------------- sheet 3: sources
    ws3 = wb.create_sheet("מקורות")
    ws3.sheet_view.rightToLeft = True
    set_cell(ws3, 1, 1, f"קבצי PDF בתיקיית החברה: {d0['company_folder']}", F_TITLE, align=RIGHT)
    heads = ["קובץ", "רבעון", "מספר דיווח", "מספר עמודים", "תפקיד", "בשימוש",
             "עמודי הדוח המאוחד על תזרימי המזומנים" if all(d.get("consolidated", True) for d in reports)
             else "עמודי הדוח על תזרימי המזומנים", "עמוד/י פעילות המימון", "הערות"]
    for j, h in enumerate(heads):
        set_cell(ws3, 3, 1 + j, h, F_BOLD, FILL_HDR, align=CENTER, border=BOX)
    inv = file_inventory(d0["company_folder"], reports, roles)
    for i, row in enumerate(inv):
        vals = [row["file"], row["quarter"], row["report_id"], row["pages"], row["role"], row["used"],
                row["cf_pages"], row["fin_pages"], row["note"]]
        for j, v in enumerate(vals):
            set_cell(ws3, 4 + i, 1 + j, v, F_NORM, align=WRAP, border=BOX)
    for j, w in enumerate([46, 10, 13, 10, 28, 9, 22, 14, 80]):
        ws3.column_dimensions[get_column_letter(1 + j)].width = w

    wb.properties.creator = "fcf pipeline"
    wb.properties.title = f"{issuer} - פירוט תזרים מימון 2026"
    wb.calculation.fullCalcOnLoad = True
    tmp = L.temp_path(os.path.basename(out_path), issuer)
    wb.save(tmp)
    L.move_into_place(tmp, out_path)
    return inv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issuer")
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--draft", action="store_true",
                    help="allow unverified (auto) data; outputs are marked as drafts")
    a = ap.parse_args()
    reports = load_reports(a.issuer)
    if not reports:
        raise SystemExit("no final data for " + a.issuer + " – run finalize_report.py first")
    unverified = [d["quarter"] for d in reports if not d.get("verified")]
    if unverified and not a.draft:
        raise SystemExit(f"{a.issuer} {unverified}: data not verified (use --draft for a marked draft build)")
    draft = bool(unverified)
    folder = os.path.join(L.WORKSPACE, reports[0]["company_folder"])
    roles = L.load_roles()
    build_xlsx(a.issuer, reports, os.path.join(folder, xlsx_name(a.issuer)), roles, draft=draft)
    if not a.no_pdf:
        import fcf_render
        fcf_render.build_screenshots(a.issuer, reports, os.path.join(folder, pdf_name(a.issuer)), draft=draft)
    print("built", a.issuer, "(DRAFT – unverified: " + ",".join(unverified) + ")" if draft else "")


if __name__ == "__main__":
    main()
