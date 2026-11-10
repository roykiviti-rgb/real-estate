# -*- coding: utf-8 -*-
"""Build the master workbook  WORKSPACE/סיכום פירוט תזרים מימון 2026 - כל החברות.xlsx
from all final report data (data/<issuer>_<Q>.json) + the source-file inventory.

Usage: python build_master.py [--pilot]
  --pilot : the file index lists only the folders of companies that have data (pilot run)
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import os  # noqa: E402

import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Font  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

import build_company as BC  # noqa: E402
import checks as CK  # noqa: E402
import fcf_lib as L  # noqa: E402

F_HDR = Font(name="Arial", bold=True)
WRAP = Alignment(wrap_text=True, vertical="top", horizontal="right", readingOrder=2)
PRIMARY_COL = "תקופה עיקרית"


def write_table(ws, headers, rows, widths=None, numcols=(), datecols=(), wrapcols=()):
    ws.sheet_view.rightToLeft = True
    for j, h in enumerate(headers):
        c = ws.cell(row=1, column=1 + j, value=h)
        c.font, c.fill, c.alignment, c.border = F_HDR, BC.FILL_HDR, BC.CENTER, BC.BOX
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = ws.cell(row=2 + i, column=1 + j, value=v)
            c.font = BC.F_NORM
            if j in numcols:
                c.number_format = BC.NUMFMT
            elif j in datecols:
                c.number_format = BC.DATEFMT
            if j in wrapcols:
                c.alignment = WRAP
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{max(1, len(rows) + 1)}"
    ws.row_dimensions[1].height = 60
    for j, w in enumerate(widths or []):
        ws.column_dimensions[get_column_letter(1 + j)].width = w


def primary_flags(data):
    """T1 (goal amendment 1): a period (months + end date) presented in more than one report of a
    company is 'כן' only in the latest report (Q2 2026); every other row is 'כן'."""
    out = {}
    for iss, reps in data.items():
        seen = {}
        for q in ("Q1", "Q2"):
            for c in (reps.get(q) or {}).get("columns", []):
                seen.setdefault((c["months"], c["end"]), []).append(q)
        for q in ("Q1", "Q2"):
            for c in (reps.get(q) or {}).get("columns", []):
                qs = seen[(c["months"], c["end"])]
                out[(iss, q, c["key"])] = "כן" if q == max(qs) else "לא"
    return out


def build(pilot=False, draft=False):
    data = CK.load_all(include_unverified=True)
    unver = sorted({f"{iss} {q}" for iss, reps in data.items() for q, d in reps.items() if not d.get("verified")})
    if unver and not draft:
        raise SystemExit(f"unverified data ({len(unver)} reports, e.g. {unver[:5]}) – use --draft for a marked draft")
    issuers = sorted(data, key=int)
    res = CK.run_checks(data)
    expl = CK.explanations()
    for r in res:
        r["explanation"] = CK.explain(expl, r)
    prim = primary_flags(data)
    wb = openpyxl.Workbook()

    # ---------------- נתונים
    ws = wb.active
    ws.title = "נתונים"
    headers = (["מספר מנפיק", "שם החברה", "תיקיית החברה", "דוח", "קובץ מקור", "עמודי PDF (פעילות מימון)",
                "תקופה", "חודשים", "תאריך סוף התקופה", PRIMARY_COL, "מטבע", "יחידות"]
               + [L.ITEM_LABEL[i] for i in range(1, 15)]
               + [L.OTHER_LABEL, L.TOTAL_LABEL, L.CHECK_LABEL, L.INFO_INT_LABEL, "(*) ריבית – סיווג / הערה",
                  L.INFO_DIV_LABEL, "(*) דיבידנד – סיווג / הערה", "מוצג מחדש", "הערות",
                  "קובץ צילומי מסך (נתיב יחסי)"])
    rows = []
    for iss in issuers:
        for q in ("Q1", "Q2"):
            d = data[iss].get(q)
            if not d:
                continue
            shots = os.path.join(d["company_folder"], BC.pdf_name(iss))
            for k, c in enumerate(d["columns"]):
                notes = [d.get("column_notes", {}).get(c["key"], "")]
                if q == "Q2" and "Q1" not in data[iss]:
                    notes.append(L.MISSING_Q1_TEXT)
                if not d.get("verified"):
                    notes.append("טיוטה – טרם אומת")
                rows.append([int(iss), d["company_name"], d["company_folder"], d["report_label"], d["source_file"],
                             L.page_range_text(d["fin_pages"]), c["label"], c["months"], BC.iso_to_date(c["end"]),
                             prim[(iss, q, c["key"])], d["units"]["currency"], d["units"]["units"]]
                            + [d["items"][str(i)][k] for i in range(1, 15)]
                            + [d["other"][k], d["total"][k], d["check"][k],
                               d["info"]["interest"]["values"][k], d["info"]["interest"]["note"],
                               d["info"]["dividend"]["values"][k], d["info"]["dividend"]["note"],
                               "כן" if c["restated"] else "לא", " ".join(n for n in notes if n), shots])
    numcols = set(range(12, 12 + 17)) | {29, 31}
    write_table(ws, headers, rows,
                widths=[9, 22, 26, 9, 34, 10, 30, 8, 12, 9, 8, 9] + [14] * 17 + [14, 22, 14, 22, 8, 40, 40],
                numcols=numcols, datecols={8}, wrapcols={34})

    # ---------------- מיפוי שורות (long)
    ws2 = wb.create_sheet("מיפוי שורות")
    h2 = ["מספר מנפיק", "שם החברה", "דוח", "קובץ מקור", "עמוד PDF", "מס' שורה", "טקסט השורה המקורי (מילולית)",
          "תקופה", "ערך", "מס' סעיף", "שם הסעיף", "הערת סיווג / נימוק"]
    rows2 = []
    for iss in issuers:
        for q in ("Q1", "Q2"):
            d = data[iss].get(q)
            if not d:
                continue
            for ln in d["lines"]:
                for k, c in enumerate(d["columns"]):
                    it = ln["resolved"][k]
                    if it == "total":
                        num, lab = "=", L.TOTAL_LABEL
                    elif it == "subtotal":
                        num, lab = "סיכום ביניים", L.SUBTOTAL_TAG
                    elif it == "other":
                        num, lab = "\u2014", L.OTHER_LABEL
                    elif it == "text":
                        num, lab = "", "שורת טקסט (ללא ערכים)"
                    else:
                        num, lab = it, L.ITEM_LABEL[it]
                    rows2.append([int(iss), d["company_name"], d["report_label"], d["source_file"], ln["page"],
                                  ln["n"], ln["text"], c["label"], ln["values"][k], num, lab, ln.get("note", "")])
            for o in d.get("outside", []):
                for k, c in enumerate(d["columns"]):
                    rows2.append([int(iss), d["company_name"], d["report_label"], d["source_file"], o["page"], "*",
                                  o["text"], c["label"], o["values"][k], "לידיעה", L.OUTSIDE_TAG,
                                  L.star_mapping_note(o)])
    write_table(ws2, h2, rows2, widths=[9, 22, 9, 34, 8, 7, 46, 28, 14, 9, 36, 50], numcols={8}, wrapcols={6, 11})

    # ---------------- אינדקס קבצים
    ws3 = wb.create_sheet("אינדקס קבצים")
    h3 = ["נתיב יחסי", "מספר מנפיק", "חברה", "רבעון", "מספר דיווח", "מספר עמודים", "תפקיד", "בשימוש",
          "עמודי הדוח (המאוחד) על תזרימי המזומנים", "עמוד/י פעילות המימון", "הערות"]
    rows3 = []
    base = L.baseline_files()
    folders = sorted({rel.split("\\")[0] for rel in base}, key=lambda f: int(f.split(" - ")[0]))
    if pilot:
        folders = [f for f in folders if f.split(" - ")[0] in issuers]
    roles = L.load_roles()
    for folder in folders:
        iss = folder.split(" - ")[0]
        reps = [data[iss][q] for q in ("Q1", "Q2") if iss in data and q in data[iss]]
        for row in BC.file_inventory(folder, reps, roles):
            rows3.append([row["rel"], int(iss), L.restore_quotes(folder.split(" - ", 1)[1]), row["quarter"],
                          row["report_id"], row["pages"], row["role"], row["used"], row["cf_pages"], row["fin_pages"],
                          row["note"]])
    write_table(ws3, h3, rows3, widths=[60, 9, 26, 9, 12, 9, 28, 8, 20, 12, 90], wrapcols={10})

    # ---------------- חסרים והערות
    ws4 = wb.create_sheet("חסרים והערות")
    h4 = ["סוג", "מספר מנפיק", "חברה", "דוח", "תקופה", "סעיף", "צפוי", "בפועל", "הפרש", "תיאור", "הסבר / טיפול"]
    rows4 = []
    if pilot:
        rows4.append(["פיילוט", None, "", "", "", "", None, None, None,
                      "קובץ זה הופק בשלב הפיילוט וכולל את חברה 1618 (קבוצת אשטרום) בלבד.",
                      "ייווצר מחדש בהרצה המלאה עבור כל 86 החברות (178 קבצים)."])
    if unver:
        rows4.append(["טיוטה", None, "", "", "", "", None, None, None,
                      f"קובץ טיוטה: {len(unver)} דוחות טרם אומתו ויזואלית (חילוץ אוטומטי).",
                      "ייווצר מחדש לאחר האימות."])
    for iss in issuers:
        if "Q1" not in data[iss]:
            d = data[iss]["Q2"]
            rows4.append(["דוח חסר", int(iss), d["company_name"], "Q1 2026", "", "", None, None, None,
                          L.MISSING_Q1_TEXT, "לא הורד מהאינטרנט (מחוץ להיקף)"])
    # special source decisions (roles.json): attachments used as the report, alternative versions, letters
    for rel, f in sorted(roles["files"].items(), key=lambda kv: (int(kv[1]["issuer"]), kv[0])):
        if pilot and f["issuer"] not in issuers:
            continue
        if f["suffix"] or f["role"] != L.ROLE_MAIN:
            rows4.append(["החלטת מקור", int(f["issuer"]), L.restore_quotes(f["folder"].split(" - ", 1)[1]),
                          f"{f['quarter']} 2026", "", "", None, None, None,
                          f"{f['file']} – {f['role']} ({'בשימוש' if f['used'] else 'לא בשימוש'})", f["note"]])
    # source irregularities recorded by the reviewers (override key "issues")
    for iss in issuers:
        for q in ("Q1", "Q2"):
            d = data[iss].get(q)
            for t in (d or {}).get("issues", []):
                rows4.append(["חריגה בדוח המקור", int(iss), d["company_name"], d["report_label"], "", "", None, None,
                              None, t, ""])
    for r in res:
        if r["status"] in ("MISMATCH", "INFO", "N/A"):
            kind = {"C1": "בדיקה C1 – אי התאמה", "C2": "בדיקה C2 – אי התאמה", "C3": "בדיקה C3 – אי התאמה",
                    "C2-item": "בדיקה C2 ברמת סעיף – לידיעה"}.get(r["check"], r["check"])
            if r["status"] == "N/A":
                kind = f"בדיקה {r['check']} – לא ניתנת לביצוע"
            desc = {"C2-item": "רבעון 1 לפי דוח Q1 (3 חודשים) לעומת דוח Q2 (6 חודשים פחות 3 חודשים) – הסה\"כ תואם; "
                               "הפרש בסעיף בודד"}.get(r["check"], r.get("note", ""))
            rows4.append([kind, int(r["issuer"]), r["company"], r["report"], r["period"], CK.key_label(r["key"]),
                          r.get("expected"), r.get("actual"), r.get("diff"), desc, r.get("explanation", "")])
    for iss in issuers:
        for q in ("Q1", "Q2"):
            d = data[iss].get(q)
            if d and any(x != 0 for x in d["check"]):
                bad = [f"{c['label']}: {x:g}" for c, x in zip(d["columns"], d["check"]) if x != 0]
                rows4.append(["בדיקה לא אפס", int(iss), d["company_name"], d["report_label"], "", "", None, None, None,
                              "שורת הבדיקה אינה 0 בעמודות: " + "; ".join(bad),
                              "הערכים נרשמו כפי שהודפסו (ללא ערך איזון); הדוח המקורי עצמו אינו מתאזן – ההסבר בשורת "
                              "'בדיקה C1' של אותה עמודה"])
    # summary of checks
    for chk in ("C1", "C2", "C3"):
        rs = [r for r in res if r["check"] == chk]
        ok = sum(1 for r in rs if r["status"] == "OK")
        bad = sum(1 for r in rs if r["status"] == "MISMATCH")
        rows4.append([f"סיכום בדיקה {chk}", None, "", "", "", "", None, None, None,
                      f"{len(rs)} השוואות: {ok} תקינות, {bad} אי התאמות", ""])
    write_table(ws4, h4, rows4, widths=[26, 9, 22, 10, 28, 30, 13, 13, 11, 60, 90], numcols={6, 7, 8},
                wrapcols={9, 10})

    # ---------------- הסבר
    ws5 = wb.create_sheet("הסבר")
    ws5.sheet_view.rightToLeft = True
    legend = [
        ("מטרה", "פירוט מדויק של תזרים המזומנים מפעילות מימון בדוח המאוחד על תזרימי המזומנים בכל דוח רבעוני (Q1/Q2 2026), "
                 "לכל עמודה (תקופה) שמוצגת בדוח, ל-14 סעיפים + 'אחר' + הסה\"כ המדווח."),
        ("מקור", "הדוח התמציתי המאוחד על תזרימי המזומנים של החברה המדווחת בלבד (לא מידע כספי נפרד לפי תקנה 38ד, "
                 "לא דוח הדירקטוריון ולא דוחות של חברות מוחזקות). חברה שאינה מציגה דוחות מאוחדים (1484) – הדוח על "
                 "תזרימי המזומנים שלה, וכך הוא מכונה בקבצים."),
        ("סימן ויחידות", "הסכומים הועתקו כפי שדווחו (אותן ספרות, אותו מטבע ואותן יחידות – ללא עיגול או המרה). "
                         "תקבולים בחיוב; תשלומים (בסוגריים בדוח) בשלילה; '-' בדוח = 0; סעיף ללא שורה = 0."),
        ("כלל המיפוי", "כל שורה מקורית בסעיף המימון משויכת לסעיף אחד בלבד לפי מהותה הכלכלית; ערך הסעיף = סכום השורות "
                       "ששויכו אליו; 'אחר' רק לשורות שאינן מתאימות לאף סעיף (עם הטקסט המקורי); אין ערכי איזון."),
    ]
    rules = {
        1: "הנפקת מניות/יחידות של הישות המדווחת, תקבולים על חשבון מניות, השקעות הון בישות; עלויות הנפקה בניכוי.",
        2: "מימוש אופציות לעובדים / כתבי אופציה; תמורת כתבי אופציה בשורה נפרדת.",
        3: "הנפקת אג\"ח מכל סדרה (כולל הרחבות ואג\"ח להמרה) נטו מעלויות; הנפקת נע\"מ (מצוין בהערה).",
        4: "קבלת הלוואות לזמן ארוך מכל מלווה (בנקים, מוסדיים, בעל שליטה, צדדים קשורים, אחרים), כולל מימון פרויקטים.",
        5: "אשראי לזמן קצר מבנקים ומאחרים – נטו או ברוטו (מסוכם כאן); שורת הלוואות נטו ללא ציון תקופה.",
        6: "השקעת בעלי זכויות שאינן מקנות שליטה בחברות בנות, הנפקת מניות חברה בת לזכויות שאינן מקנות שליטה, "
           "מכירת מניות חברה בת ללא איבוד שליטה.",
        7: "פירעון הלוואות לזמן ארוך (שוטף/מוקדם) לכל מלווה.",
        8: "פירעון/פדיון אג\"ח, פדיון מוקדם, רכישה עצמית של אג\"ח; פירעון נע\"מ.",
        9: "רכישת מניות אוצר (כולל רכישת מניות האם ע\"י חברה בת).",
        10: "פירעון התחייבויות בגין חכירה (אם השורה כוללת גם ריבית ללא פיצול – כאן, עם הערה).",
        11: "דיבידנד לבעלי מניות החברה האם / חלוקות לבעלי היחידות – רק סכומים שבפעילות מימון.",
        12: "דיבידנד / חלוקות / משיכות לבעלי זכויות שאינן מקנות שליטה.",
        13: "ריבית ששולמה המוצגת בפעילות מימון (כולל ריבית חכירה בשורה נפרדת) – רק סכומים שבפעילות מימון.",
        14: "רכישת זכויות שאינן מקנות שליטה / מניות נוספות בחברה בת שכבר בשליטה.",
    }
    r = 1
    c = ws5.cell(row=r, column=1, value="הסבר – פירוט תזרים מזומנים מפעילות מימון 2026")
    c.font = BC.F_TITLE
    r += 2
    for k, v in legend:
        ws5.cell(row=r, column=1, value=k).font = F_HDR
        ws5.cell(row=r, column=2, value=v).alignment = WRAP
        ws5.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        ws5.row_dimensions[r].height = 32
        r += 1
    r += 1
    for j, h in enumerate(["מס'", "סעיף", "מה נכלל"]):
        cc = ws5.cell(row=r, column=1 + j, value=h)
        cc.font, cc.fill, cc.border = F_HDR, BC.FILL_HDR, BC.BOX
    r += 1
    ws5.cell(row=r, column=2, value=L.GROUP_IN).font = F_HDR
    r += 1
    for i in range(1, 15):
        if i == 7:
            ws5.cell(row=r, column=2, value=L.GROUP_OUT).font = F_HDR
            r += 1
        ws5.cell(row=r, column=1, value=i)
        ws5.cell(row=r, column=2, value=L.ITEM_LABEL[i])
        ws5.cell(row=r, column=3, value=rules[i]).alignment = WRAP
        r += 1
    ws5.cell(row=r, column=1, value="\u2014")
    ws5.cell(row=r, column=2, value=L.OTHER_LABEL)
    ws5.cell(row=r, column=3, value="רק שורות שאינן מתאימות לאף סעיף (פיקדונות מוגבלים/בטחונות, סליקת נגזרים, מענקים, "
                                    "תמורה מותנית, תזרימי פעילות מופסקת וכד'), עם הטקסט המקורי.").alignment = WRAP
    r += 1
    ws5.cell(row=r, column=1, value="=")
    ws5.cell(row=r, column=2, value=L.TOTAL_LABEL)
    ws5.cell(row=r, column=3, value="שורת הסה\"כ של פעילות המימון כפי שדווחה בדוח.").alignment = WRAP
    r += 2
    more = [
        ("שורה נטו של אותו מכשיר", "שורה שמקזזת קבלה ופירעון של אותו מכשיר לזמן ארוך משויכת בכל תקופה לסעיף הקבלה (4/3) "
                                    "אם הסכום חיובי ולסעיף הפירעון (7/8) אם שלילי."),
        ("שורה נטו של עסקאות עם זכויות שאינן מקנות שליטה", "שורה אחת המציגה נטו עסקאות עם בעלי זכויות שאינן מקנות שליטה "
                                    "(מכירה/הנפקה לזשמ\"ש מול רכישה מהם) משויכת בכל תקופה לפי הסימן: סכום חיובי – סעיף 6, "
                                    "סכום שלילי – סעיף 14 (בגיליון המיפוי: '6/14')."),
        ("הלוואות ללא ציון תקופה (כלל A)", "שורת הלוואות/אשראי המוצגת נטו ללא ציון תקופה – סעיף 5. שורות קבלה/פירעון ברוטו ללא ציון "
                                   "תקופה – לפי סיווג ההלוואות במאזן ובביאורים של החברה המדווחת: אשראי/הלוואות המסווגים "
                                   "כהתחייבות שוטפת לזמן קצר – סעיף 5; הלוואות לזמן ארוך (כולל חלויות שוטפות ומימון פרויקטים "
                                   "המסווג לזמן ארוך) – סעיפים 4/7; כשלא ניתן לשייך (יתרות שוטפות ולא שוטפות של אותם מלווים) – "
                                   "4/7 עם הערה. 'נטו' שפירושו בניכוי עלויות גיוס, כשהפירעונות בשורה נפרדת – קבלה ברוטו (4). "
                                   "אותה שורה בדוח Q1 ובדוח Q2 משויכת לאותו סעיף."),
        ("סיכומי ביניים", "סיכומי ביניים בתוך סעיף המימון אינם סעיפים ('סיכום ביניים – לא נכלל'); אין ספירה כפולה."),
        ("(*) סעיפים 11 ו-13", "כוללים רק סכומים המוצגים בפעילות מימון. ריבית/דיבידנד ששולמו שסווגו בפעילות שוטפת או "
                               "השקעה מוצגים בשורות (*) 'לידיעה בלבד' (לא נכללים בסכום), עם ציון הסעיף. אם לא מוצגים "
                               "בנפרד בדוח: 'לא מוצג בנפרד בדוח תזרים המזומנים'."),
        ("(*) נוסח ההערה", "הערת שורת (*) בנויה מסיווג כל שורת מקור, בנוסח אחיד: 'פעילות שוטפת' / 'פעילות השקעה' – שורה "
                           "בגוף הדוח; 'גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת' – סכום שמופיע רק בנספח, "
                           "כשהדוח מציין (או הנספח מראה בבירור) את הסעיף; 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא "
                           "צוין (לא בפעילות מימון)' – כשהסעיף אינו מצוין. כמה רכיבים – מחוברים ב-' + '; הערה ספציפית "
                           "לדוח, אם יש, באה אחרי ';'."),
        ("(*) סימן", "שורת (*) ממקור אחד שומרת את הסימן כפי שהודפס (R5): שורה בגוף הדוח בסוגריים – שלילית; סכום בנספח "
                     "שהודפס ללא סוגריים – חיובי, כמודפס. שורה המחברת רכיבים בעלי מוסכמת סימן שונה (שורה בגוף הדוח "
                     "בסוגריים + סכום בנספח שהודפס חיובי) מציגה את רכיב הנספח בסימן תשלום (שלילי) כדי שהסכום יהיה בעל "
                     "משמעות, וההערה אומרת זאת (חברות 121 ו-1083)."),
        ("הכרעות D1–D3", "הכרעות מיפוי שהתקבלו בבדיקה (ניתנות לשינוי): D1 – 2559 (דוח Q2): 'תשלום לבעל עניין בגין התאמת "
                         "תמורה' (52,500) בסעיף 1 – התאמת מחיר למשקיע בקשר עם הנפקת המניות לציבור, שנזקפה להון ומקטינה את "
                         "התמורה נטו מההנפקה (חלופה: 'אחר'). D2 – שורת קבלה/פירעון ברוטו של אשראי והלוואות שאינה ניתנת "
                         "לשיוך לאשראי לזמן קצר בלבד (יתרות שוטפות ולא שוטפות של אותם מלווים במאזן) – סעיפים 4/7, והראיות "
                         "(עמוד ויתרות במאזן ובביאורים) בהערת השורה; סעיף 5 רק כשהראיות מראות אשראי שוטף לזמן קצר. D3 – "
                         "סימן שורות (*) – ראו '(*) סימן'."),
        ("מוצג מחדש", "'מוצג מחדש' מסומן רק כשכותרת העמודה עצמה, או סימון על ערכי פעילות המימון באותה עמודה, מציינים "
                      "הצגה מחדש/סיווג מחדש; כשהסימון מופיע רק בסעיפים אחרים או בביאור כללי – הערת עמודה בלבד."),
        ("בדיקה", "בכל עמודה: סכום הסעיפים 1–14 + אחר פחות הסה\"כ המדווח = 0. ערך שונה מ-0 מותר רק כשהדוח המקורי עצמו "
                  "אינו מתאזן (למשל הפרש עיגול) – הערכים נרשמו כמודפס וההסבר בגיליון 'חסרים והערות'."),
        ("בדיקות עקביות", "C1 – התאמה לסה\"כ בכל עמודה; C2 – רבעון 1 בדוח Q1 = 6 חודשים פחות 3 חודשים בדוח Q2 (2026 ו-2025); "
                          "C3 – שנת 2025 זהה בשני הדוחות (סה\"כ וכל סעיף). אי התאמות – בגיליון 'חסרים והערות'."),
        ("עמודות גיליון 'נתונים'", "שורה לכל חברה × דוח × תקופה; 'עמודי PDF' = מספר העמוד הפיזי בקובץ (החל מ-1); "
                                   "'קובץ צילומי מסך' = הנתיב היחסי לקובץ ה-PDF עם צילומי המסך בתיקיית החברה."),
        (PRIMARY_COL, "'כן' / 'לא'. תקופה מזוהה לפי מספר החודשים ותאריך סוף התקופה. תקופה שמוצגת ביותר מדוח אחד של "
                      "אותה חברה (בדרך כלל שנת 2025, המוצגת גם בדוח Q1 וגם בדוח Q2) מסומנת 'כן' רק בשורה מהדוח המאוחר "
                      "(Q2 2026) ו'לא' בשורות מהדוחות האחרים; כל שאר השורות 'כן'. סינון על 'כן' מחזיר כל תקופה של כל "
                      "חברה פעם אחת בלבד (למשל לצורך טבלת ציר ללא ספירה כפולה)."),
        ("טווח חודשים בתווית", "לעמודה של 3 חודשים שאינה התקופה המצטברת מתחילת השנה (למשל 3 החודשים שהסתיימו ב-30.06 "
                               "בדוח Q2, לצד עמודת 6 החודשים) נוסף טווח החודשים בסוגריים, למשל "
                               "'3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני)'; בעמודה מוצגת מחדש '(מוצג מחדש)' בא אחריו."),
    ]
    for k, v in more:
        ws5.cell(row=r, column=1, value=k).font = F_HDR
        ws5.cell(row=r, column=2, value=v).alignment = WRAP
        ws5.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        ws5.row_dimensions[r].height = max(30, 15 * (len(v) // 125 + 1))
        r += 1
    ws5.column_dimensions["A"].width = 24
    ws5.column_dimensions["B"].width = 48
    ws5.column_dimensions["C"].width = 100

    wb.properties.creator = "fcf pipeline"
    wb.properties.title = "סיכום פירוט תזרים מימון 2026 - כל החברות"
    out = os.path.join(L.WORKSPACE, L.MASTER_NAME)
    tmp = L.temp_path("master.xlsx", "_master")
    wb.save(tmp)
    L.move_into_place(tmp, out)
    return len(rows), len(rows2), len(rows3), len(rows4)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true", help="file index limited to the companies that have data")
    ap.add_argument("--draft", action="store_true", help="allow unverified data (marked as draft)")
    a = ap.parse_args()
    print("master rows (data, mapping, index, issues):", build(a.pilot, a.draft))
