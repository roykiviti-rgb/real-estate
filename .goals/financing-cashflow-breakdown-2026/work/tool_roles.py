# -*- coding: utf-8 -*-
"""Build work/roles.json: the role of every source PDF (goal R1 / R6.3) and the data source of every
company x quarter report. Company-specific decisions are listed in DECISIONS below (verified by
reading the files); every main file is additionally checked automatically for the company name and
the period end date on its first pages (evidence stored in roles.json).

Usage: python tool_roles.py            (rewrites work/roles.json; read-only on the PDFs)
"""
import sys

sys.dont_write_bytecode = True
import os  # noqa: E402
import re  # noqa: E402

import pymupdf  # noqa: E402

import fcf_lib as L  # noqa: E402

ROLE_MAIN = L.ROLE_MAIN                                   # "מקור הנתונים – דוח רבעוני"
ROLE_ALT = "גרסה חלופית – לא בשימוש"
ROLE_APPRAISAL = "נספח – שומה/הערכת שווי"
ROLE_INVESTEE = "נספח – דוחות כספיים של חברה מוחזקת"
ROLE_LETTER = "מכתב נלווה/תמצית"

# file-name suffix decisions: (issuer, quarter, suffix) -> (role, used, note)
DECISIONS = {
    ("1829", "Q1", ""): (ROLE_LETTER, False,
                         "מכתב שמאי (עמוד אחד, יוסי דהאן, 20.5.2026) המאשר שלא חל שינוי מהותי בשווי מקרקעין \"עיר כנרת\" – "
                         "אינו דוח כספי. הדוח הרבעוני המלא הוא קובץ -01."),
    ("1829", "Q1", "-01"): (ROLE_MAIN, True,
                            "הדוח הרבעוני המלא של אב-גד החזקות בע\"מ ליום 31.03.2026 (דוח דירקטוריון, דוחות כספיים מאוחדים "
                            "תמציתיים, מידע כספי נפרד) – צורף כנספח -01 לדיווח; משמש כמקור הנתונים."),
    ("1829", "Q2", ""): (ROLE_LETTER, False,
                         "מכתב שמאי (עמוד אחד, יוסי דהאן, 30.8.2026) המאשר שלא חל שינוי מהותי בשווי מקרקעין \"עיר כנרת\" – "
                         "אינו דוח כספי. הדוח הרבעוני המלא הוא קובץ -01."),
    ("1829", "Q2", "-01"): (ROLE_MAIN, True,
                            "הדוח הרבעוני המלא של אב-גד החזקות בע\"מ ליום 30.06.2026 (\"דוח רבעוני 30 ביוני 2026\": דוח "
                            "דירקטוריון, דוחות כספיים מאוחדים תמציתיים ומידע כספי נפרד) – צורף כנספח -01; משמש כמקור הנתונים."),
    ("2559", "Q1", ""): (ROLE_LETTER, False,
                         "תמצית בת 3 עמודים: באור 2ב' (הצגה מחדש בגין טעות מהותית – יתרות בעלי עניין) לדוחות ליום 31.03.2026; "
                         "אינו כולל את הדוח על תזרימי המזומנים. הדוחות המלאים (\"דוח מתקן\") בקבצים -01/-02."),
    # 2559 Q1 -01 / -02: decided in DECISIONS_2559 below (filled after comparing the two files)
    ("2520", "Q1", "-01"): (ROLE_INVESTEE, False,
                            "דוחות כספיים תמציתיים מאוחדים של החברה המוחזקת סלע איסתא נדל\"ן ישראלי בע\"מ ליום 31.03.2026 – "
                            "מחוץ להיקף (לא הדוחות של החברה המדווחת)."),
    ("2520", "Q2", "-01"): (ROLE_INVESTEE, False,
                            "דוחות כספיים תמציתיים של החברה המוחזקת סלע איסתא נדל\"ן ישראלי בע\"מ ליום 30.06.2026 – "
                            "מחוץ להיקף (לא הדוחות של החברה המדווחת)."),
    ("1331", "Q2", "-01"): (ROLE_APPRAISAL, False,
                            "שומת מקרקעין מקיפה – מרכז מסחרי ומשרדים \"MORE בעיר\", חריש (גוש 9070 חלקה 44), ליום 30.06.2026."),
    ("1490", "Q2", "-01"): (ROLE_APPRAISAL, False,
                            "חוות דעת של מומחה (שמאות) – פרויקט \"ורטיקל סיטי\", משולש הבורסה רמת גן."),
    ("1703", "Q2", "-01"): (ROLE_APPRAISAL, False,
                            "הערכת שווי (BDO) של החזקת YSB ב-BlueGen Waste Management ליום 30.06.2026."),
    ("2384", "Q2", "-01"): (ROLE_APPRAISAL, False,
                            "נספח א – הערכות שווי (עדכון הערכת שווי מבנה \"בית רנו\", תל אביב) ליום 30.06.2026."),
    ("2385", "Q2", "-01"): (ROLE_APPRAISAL, False,
                            "הקצאת עלות רכישה (PPA, BDO) – עמרם את נידם התחדשות עירונית בע\"מ, ליום 30.06.2026."),
    ("2464", "Q1", "-01"): (ROLE_APPRAISAL, False,
                            "שומת מקרקעין מקיפה – מבנה מלונאות ומסחר, סמטת בית הבד 3 ת\"א (גוש 7421 חלקה 11)."),
    ("2557", "Q2", "-01"): (ROLE_APPRAISAL, False,
                            "שומת מקרקעין מקיפה ליום 30.06.2026 – מגדל תעסוקה דרומי וקומות הפודיום בפרויקט \"Beyond\", גבעתיים."),
    ("539", "Q2", "-01"): (ROLE_APPRAISAL, False,
                           "שומת מקרקעין מקיפה – מרכז מסחרי \"רוטשטיינס\", צורן, ליום 30.06.2026."),
    ("771", "Q2", "-01"): (ROLE_APPRAISAL, False,
                           "שומת מקרקעין מקיפה – בית מלון \"רוקסון דזרט\", ערד."),
    ("823", "Q2", "-01"): (ROLE_APPRAISAL, False,
                           "הערכת שווי (BDO) של החזקות בחג'ג' צים נדל\"ן בע\"מ ליום 31.05.2026 (IFRS 3)."),
}

PERIOD_RX = {
    "Q1": r"31\s*ב?(?:מרס|מרץ)\s*,?\s*2026|31[./]0?3[./]2026",
    "Q2": r"30\s*ב?יוני\s*,?\s*2026|30[./]0?6[./]2026",
}


def norm(s):
    s = s.replace("״", '"').replace("”", '"').replace("׳", "'").replace("’", "'")
    return re.sub(r"[\s\"'\-–_.,()]", "", s)


def first_text(doc, n=4):
    out = []
    for p in range(min(n, doc.page_count)):
        lines = L.group_lines(L.page_words(doc[p]))
        out.append(" | ".join(ln.text_all() for ln in lines))
    return "\n".join(out)


def main():
    import json
    decisions_2559 = {}
    p2559 = os.path.join(L.WORK, "roles_2559.json")
    if os.path.exists(p2559):
        decisions_2559 = L.load_json(p2559)
    base = L.baseline_files()
    files, sources = {}, {}
    for rel in sorted(base, key=lambda r: (int(r.split(" - ")[0]), r)):
        folder = rel.split("\\")[0]
        f = os.path.basename(rel.replace("\\", "/"))
        m = re.search(r"_2026_(Q[12])_(\d+)(-\d+)?\.pdf$", f)
        iss, q, rid, suf = folder.split(" - ")[0], m.group(1), m.group(2), (m.group(3) or "")
        with pymupdf.open(os.path.join(L.WORKSPACE, rel)) as doc:
            npages = doc.page_count
            txt = first_text(doc, 4)
        key = (iss, q, suf)
        if key in DECISIONS:
            role, used, note = DECISIONS[key]
        elif iss == "2559" and q == "Q1" and suf in ("-01", "-02"):
            dd = decisions_2559.get(suf)
            if not dd:
                raise SystemExit("2559 Q1 decision missing (roles_2559.json)")
            role, used, note = dd["role"], dd["used"], dd["note"]
        elif suf == "":
            role, used, note = ROLE_MAIN, True, "דוח רבעוני מלא (קובץ הדיווח הראשי)."
        else:
            raise SystemExit(f"no decision for extra file {rel}")
        name = L.restore_quotes(folder.split(" - ", 1)[1])
        core = norm(re.sub(r'\s*בע"?מ\s*$', "", name))
        ntxt = norm(txt)
        ev = []
        if used:
            ev.append("שם החברה נמצא בעמודים 1–4" if core and core in ntxt else "שם החברה לא נמצא כלשונו בעמודים 1–4 (לבדיקה ידנית)")
            ev.append(f"תאריך סוף התקופה ({'31.03.2026' if q == 'Q1' else '30.06.2026'}) נמצא בעמודים 1–4"
                      if re.search(PERIOD_RX[q], txt) else "תאריך סוף התקופה לא נמצא בעמודים 1–4 (לבדיקה ידנית)")
        files[rel] = {"issuer": iss, "folder": folder, "file": f, "quarter": q, "report_id": rid, "suffix": suf,
                      "pages": npages, "role": role, "used": used, "note": note, "evidence": "; ".join(ev),
                      "first_text": txt[:300]}
        if used:
            k = f"{iss}_{q}"
            if k in sources:
                raise SystemExit(f"two sources for {k}")
            sources[k] = rel
    out = {"_doc": "Role of every source PDF (goal R1/R6.3) and the data source of every issuer_quarter. "
                   "Generated by tool_roles.py from verified decisions; read by extract_report.py, build_company.py, "
                   "build_master.py. Shared file: batch builders must NOT edit it (report a SCRIPT-ISSUE instead).",
           "sources": sources, "files": files}
    L.save_json(out, L.ROLES_PATH)
    n_used = sum(1 for v in files.values() if v["used"])
    print(f"files={len(files)} used={n_used} sources={len(sources)}")
    bad = [(r, v["evidence"]) for r, v in files.items() if v["used"] and "לבדיקה" in v["evidence"]]
    for r, e in bad:
        print("CHECK:", r, e)
    json.dump([r for r, _ in bad], open(os.path.join(L.temp_dir("_roles"), "roles_check.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
