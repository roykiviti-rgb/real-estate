# -*- coding: utf-8 -*-
"""validate.py — independent re-check of all outputs (goal AC13).

Usage (from any directory):
  python validate.py [--issuers 1618 1039 ...] [--pilot] [--no-master] [--out <file>]
  default scope = every company folder in the WORKSPACE (full run, Phase C);
  --issuers limits the company checks; --pilot also limits the master file-index and the expected
  new-file list to those issuers; --no-master (batch use) skips the master workbook and only requires the
  given issuers' own output files. Results: per-invocation file (printed), never a shared file.
Checks: AC2 files/names/open, AC3 period counts+labels (T2 month ranges), AC4/AC5 values & sums (workbook
vs final data, mapping sums), AC6 C1, AC8 C2/C3 (unexplained mismatches), AC9 layout basics, AC10 screenshot
PDF basics, AC11 master equality + T1 'תקופה עיקרית', AC12 baseline hashes + hygiene, AC13 verification
records. Exit 0 only when all pass.
Iteration 2 (S9): the master comparison is key-based – 'נתונים' by (issuer, report, period label) with every field,
'מיפוי שורות' by (issuer, report, line no., period label) with every field; with --issuers only those issuers' master
rows are compared (no false positional failures); the console summary prints the unexplained-mismatch count.
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import hashlib  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402

import openpyxl  # noqa: E402
import pymupdf  # noqa: E402

import build_company as BC  # noqa: E402
import checks as CK  # noqa: E402
import fcf_lib as L  # noqa: E402

FAIL = []
PASS = []
INFO = []          # explained source inconsistencies etc. (reported, not failures)
EXPL = None        # check explanations (loaded once)


def ok(cond, msg):
    (PASS if cond else FAIL).append(msg)
    return cond


def c1_explanation(issuer, d, col):
    """The documented explanation of a non-zero C1 column (same lookup as checks.py: report-specific key first)."""
    global EXPL
    if EXPL is None:
        EXPL = CK.explanations()
    r = {"check": "C1", "issuer": issuer, "report": d["report_label"], "period": col["label"], "key": "total"}
    return CK.explain(EXPL, r)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def company_checks(issuer, folder, reps):
    tag = f"[{issuer}]"
    xlsx = os.path.join(L.WORKSPACE, folder, BC.xlsx_name(issuer))
    pdf = os.path.join(L.WORKSPACE, folder, BC.pdf_name(issuer))
    if not ok(os.path.exists(xlsx), f"{tag} AC2 workbook exists") or not ok(os.path.exists(pdf), f"{tag} AC2 PDF exists"):
        return
    wb = openpyxl.load_workbook(xlsx)
    ok(wb.sheetnames == ["פירוט מימון", "מיפוי שורות", "מקורות"], f"{tag} AC9 sheet names {wb.sheetnames}")
    ok(all(ws.sheet_view.rightToLeft for ws in wb.worksheets), f"{tag} AC9 all sheets RTL")
    ws = wb["פירוט מימון"]
    cols = [(d, k, c) for d in reps for k, c in enumerate(d["columns"])]
    hdr = next(r for r in range(1, 40) if ws.cell(r, 2).value == "סעיף")
    got = []
    c = 3
    while ws.cell(hdr, c).value and str(ws.cell(hdr, c).value).startswith("דוח "):
        got.append(ws.cell(hdr, c).value)
        c += 1
    ok(got == [x[2]["label_full"] for x in cols], f"{tag} AC3 column headers ({len(got)} periods)")
    for d in reps:
        for cc in d["columns"]:
            ok(cc["months"] in (3, 6, 9, 12) and cc["end"], f"{tag} AC3 {d['quarter']} {cc['label']} months/end")
    rows = {ws.cell(r, 2).value: r for r in range(hdr, ws.max_row + 1) if ws.cell(r, 2).value}
    have_q1 = any(d["quarter"] == "Q1" for d in reps)
    if not have_q1:
        ok(any(ws.cell(r, 3).value == L.MISSING_Q1_TEXT for r in range(1, hdr)), f"{tag} AC3 missing-Q1 statement")
    order = [L.GROUP_IN] + [L.ITEM_LABEL[i] for i in range(1, 7)] + [L.GROUP_OUT] + \
            [L.ITEM_LABEL[i] for i in range(7, 15)] + [L.OTHER_LABEL, L.TOTAL_LABEL, L.CHECK_LABEL,
                                                       L.INFO_INT_LABEL, L.INFO_DIV_LABEL, "הערות"]
    pos = [rows.get(x) for x in order]
    ok(None not in pos and pos == sorted(pos) and pos[-1] - pos[0] == len(order) - 1,
       f"{tag} AC9 row order & exact labels")
    if None in pos:
        return
    for j, (d, k, cc) in enumerate(cols):
        col = 3 + j
        vals = {}
        for i in range(1, 15):
            v = ws.cell(rows[L.ITEM_LABEL[i]], col).value
            vals[i] = v
            ok(isinstance(v, (int, float)) and v == d["items"][str(i)][k], f"{tag} AC4 {cc['label_full']} item {i}")
        vo = ws.cell(rows[L.OTHER_LABEL], col).value
        vt = ws.cell(rows[L.TOTAL_LABEL], col).value
        ok(vo == d["other"][k] and vt == d["total"][k], f"{tag} AC4 {cc['label_full']} other/total")
        diff = round(sum(vals.values()) + vo - vt, 6)
        if abs(diff) < 1e-6:
            ok(True, f"{tag} AC6 C1 {cc['label_full']}")
        else:
            # goal AC6: a non-zero check is allowed only when the source statement itself does not add up and it is
            # documented -> it passes when checks.py finds the explanation, and is listed as INFO; otherwise FAIL
            ex = c1_explanation(issuer, d, cc)
            if ok(bool(ex), f"{tag} AC6 C1 {cc['label_full']} diff={diff:g} "
                            f"{'explained source inconsistency' if ex else 'UNEXPLAINED'}"):
                INFO.append(f"{tag} C1 {cc['label_full']} diff={diff:g} (explained): {ex}")
        f = ws.cell(rows[L.CHECK_LABEL], col).value
        ok(isinstance(f, str) and f.startswith("=SUM(") or f == 0, f"{tag} AC9 check cell present")
        ok(ws.cell(rows[L.INFO_INT_LABEL], col).value == d["info"]["interest"]["values"][k] and
           ws.cell(rows[L.INFO_DIV_LABEL], col).value == d["info"]["dividend"]["values"][k],
           f"{tag} AC7 info rows {cc['label_full']}")
        ok(ws.cell(hdr + 1, col).value == d["source_file"], f"{tag} AC9 source file under header")
    # mapping sheet: every line × period present; per-item sums equal the items
    ws2 = wb["מיפוי שורות"]
    texts = [ws2.cell(r, 3).value for r in range(1, ws2.max_row + 1)]
    for d in reps:
        for ln in d["lines"]:
            ok(ln["text"] in texts, f"{tag} AC5 mapping line present: {ln['text'][:30]}")
        for k in range(len(d["columns"])):
            sums = {}
            for ln in d["lines"]:
                it = ln["resolved"][k]
                if it not in ("total", "subtotal", "text"):
                    sums[str(it)] = sums.get(str(it), 0) + (ln["values"][k] or 0)
            for i in range(1, 15):
                ok(abs(sums.get(str(i), 0) - d["items"][str(i)][k]) < 1e-6,
                   f"{tag} AC5 {d['quarter']} c{k + 1} item {i} = sum of lines")
            ok(abs(sums.get("other", 0) - d["other"][k]) < 1e-6, f"{tag} AC5 {d['quarter']} c{k + 1} other = sum of lines")
        ok(bool(d.get("verified")) and d["verified"].get("status") == "verified",
           f"{tag} AC13 verification record {d['quarter']}")
    ok(not (ws.cell(1, 3).value and "טיוטה" in str(ws.cell(1, 3).value)) or not all(d.get("verified") for d in reps),
       f"{tag} no draft marker in a verified workbook")
    # sources sheet = baseline PDFs of the folder, roles as in roles.json
    ws3 = wb["מקורות"]
    listed = sorted(ws3.cell(r, 1).value for r in range(4, ws3.max_row + 1) if ws3.cell(r, 1).value)
    base = sorted(os.path.basename(rel.replace("\\", "/")) for rel in L.baseline_files()
                  if rel.split("\\")[0] == folder)
    ok(listed == base, f"{tag} AC1 מקורות lists exactly the folder's PDFs ({len(listed)})")
    used = [ws3.cell(r, 1).value for r in range(4, ws3.max_row + 1) if ws3.cell(r, 6).value == "כן"]
    ok(sorted(used) == sorted(d["source_file"] for d in reps), f"{tag} AC1 used files = data sources")
    rfiles = {os.path.basename(rel.replace("\\", "/")): v for rel, v in L.load_roles()["files"].items()
              if rel.split("\\")[0] == folder}
    for r in range(4, ws3.max_row + 1):
        f = ws3.cell(r, 1).value
        if not f:
            continue
        exp_role = L.ROLE_MAIN if f in used else rfiles.get(f, {}).get("role")
        ok(ws3.cell(r, 5).value == exp_role and (f in used) == bool(rfiles.get(f, {}).get("used")),
           f"{tag} AC1 role of {f[-30:]} = roles.json")
    # screenshots PDF
    with pymupdf.open(pdf) as doc:
        n_img = sum(1 for pg in doc if pg.get_images())
        ok(doc.page_count >= 1 + 2 * len(reps) and n_img >= 2 * len(reps), f"{tag} AC10 screenshots pages ({doc.page_count})")
        txt = "".join(pg.get_text() for pg in doc)
        for d in reps:
            ok(d["report_id"] in txt, f"{tag} AC10 captions cite {d['source_file']}")
            for p in d["cf_pages"]:
                ok(f"{p}" in txt, f"{tag} AC10 page {p} cited in captions")
    # AC10 (R7.2, Phase C S3/S4): the zoom's header and every red (*) crop show the period headers and the units –
    # re-derived from the source PDF text inside the exact clip regions the renderer uses
    import fcf_render as R
    for d in reps:
        with pymupdf.open(os.path.join(L.WORKSPACE, folder, d["source_file"])) as src:
            ct = R.crop_texts(d, src)
        ok(R.has_units(ct["zoom"]) and R.has_periods(ct["zoom"]),
           f"{tag} AC10 {d['quarter']} zoom header shows periods and units")
        for p, t in ct["stars"].items():
            ok(R.has_units(t) and R.has_periods(t), f"{tag} AC10 {d['quarter']} (*) crop p{p} shows periods and units")
        # AC7: (*) lines – canonical section, numeric values, bbox
        for o in d.get("outside", []):
            ok(o["section"] in L.STAR_SECTIONS and all(isinstance(v, (int, float)) for v in o["values"])
               and bool(o.get("bbox")), f"{tag} AC7 {d['quarter']} (*) line '{o['text'][:25]}' canonical/numeric/bbox")
    return True


def master_checks(data, issuers, pilot):
    """Master workbook vs final data, key-based (iteration 2, S9): 'נתונים' rows keyed by (issuer, report, period label)
    with every field compared; 'מיפוי שורות' rows keyed by (issuer, report, line no., period label) with every field
    compared; only the given issuers' rows are checked (a subset run compares the subset only – no positional
    comparison against the full master)."""
    path = os.path.join(L.WORKSPACE, L.MASTER_NAME)
    if not ok(os.path.exists(path), "AC2 master exists"):
        return
    wb = openpyxl.load_workbook(path)
    ok(wb.sheetnames == ["נתונים", "מיפוי שורות", "אינדקס קבצים", "חסרים והערות", "הסבר"], f"AC11 master sheets {wb.sheetnames}")
    ok(all(ws.sheet_view.rightToLeft for ws in wb.worksheets), "AC11 master RTL")
    want = set(int(i) for i in issuers)
    full = set(int(i) for i in data)
    # ---------------- נתונים
    ws = wb["נתונים"]
    hdr = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
    idx = {h: i for i, h in enumerate(hdr)}
    rows = {}
    dup = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[idx["מספר מנפיק"]] is None:
            continue
        key = (int(r[idx["מספר מנפיק"]]), r[idx["דוח"]], r[idx["תקופה"]])
        if key[0] not in want:
            continue
        if key in rows:
            dup.append(key)
        rows[key] = r
    ok(not dup, f"AC11 נתונים no duplicate keys {dup[:3]}")
    exp = {}
    for iss in issuers:
        for q in ("Q1", "Q2"):
            d = data.get(iss, {}).get(q)
            if d:
                for k, c in enumerate(d["columns"]):
                    exp[(int(iss), d["report_label"], c["label"])] = (iss, d, k, c)
    ok(set(rows) == set(exp), f"AC11 נתונים rows = report periods ({len(rows)} vs {len(exp)}); "
                              f"missing={sorted(set(exp) - set(rows))[:3]} extra={sorted(set(rows) - set(exp))[:3]}")
    if want == full:
        ok(ws.max_row - 1 == len(exp), f"AC11 נתונים row count {ws.max_row - 1} == periods {len(exp)}")
    prim = None
    try:
        import build_master as BM
        prim = BM.primary_flags(data)
    except Exception as e:   # pragma: no cover
        ok(False, f"T1 primary flags could not be computed: {e}")
    for key, (iss, d, k, c) in sorted(exp.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[1][2])):
        r = rows.get(key)
        if r is None:
            continue
        q = d["quarter"]
        notes = [d.get("column_notes", {}).get(c["key"], "")]
        if q == "Q2" and "Q1" not in data[iss]:
            notes.append(L.MISSING_Q1_TEXT)
        if not d.get("verified"):
            notes.append("טיוטה – טרם אומת")
        expect = {"שם החברה": d["company_name"], "תיקיית החברה": d["company_folder"], "קובץ מקור": d["source_file"],
                  "עמודי PDF (פעילות מימון)": L.page_range_text(d["fin_pages"]), "חודשים": c["months"],
                  "תאריך סוף התקופה": BC.iso_to_date(c["end"]), "מטבע": d["units"]["currency"],
                  "יחידות": d["units"]["units"], L.OTHER_LABEL: d["other"][k], L.TOTAL_LABEL: d["total"][k],
                  L.CHECK_LABEL: d["check"][k], L.INFO_INT_LABEL: d["info"]["interest"]["values"][k],
                  "(*) ריבית – סיווג / הערה": d["info"]["interest"]["note"],
                  L.INFO_DIV_LABEL: d["info"]["dividend"]["values"][k],
                  "(*) דיבידנד – סיווג / הערה": d["info"]["dividend"]["note"],
                  "מוצג מחדש": "כן" if c["restated"] else "לא", "הערות": " ".join(n for n in notes if n),
                  "קובץ צילומי מסך (נתיב יחסי)": os.path.join(d["company_folder"], BC.pdf_name(iss))}
        for i in range(1, 15):
            expect[L.ITEM_LABEL[i]] = d["items"][str(i)][k]
        if prim is not None:
            expect["תקופה עיקרית"] = prim[(iss, q, c["key"])]
        bad = []
        for h, v in expect.items():
            got = r[idx[h]] if h in idx else "<missing column>"
            if isinstance(v, (int, float)) and isinstance(got, (int, float)):
                same = abs(v - got) < 1e-6
            else:
                same = (got if got is not None else "") == (v if v is not None else "")
            if not same:
                bad.append(f"{h}: {got!r} != {v!r}")
        ok(not bad, f"AC11 נתונים {key[0]} {key[1]} {key[2]}: all fields equal the data {bad[:2]}")
    # ---------------- מיפוי שורות
    ws2 = wb["מיפוי שורות"]
    h2 = [ws2.cell(1, c).value for c in range(1, ws2.max_column + 1)]
    j = {h: i for i, h in enumerate(h2)}
    got_map, dup2 = {}, []
    for r in ws2.iter_rows(min_row=2, values_only=True):
        if r[j["מספר מנפיק"]] is None or int(r[j["מספר מנפיק"]]) not in want:
            continue
        key = (int(r[j["מספר מנפיק"]]), r[j["דוח"]], str(r[j["מס' שורה"]]), r[j["תקופה"]],
               f"{r[j['טקסט השורה המקורי (מילולית)']]}|p{r[j['עמוד PDF']]}" if r[j["מס' שורה"]] == "*" else "")
        if key in got_map:
            dup2.append(key)
        got_map[key] = r
    exp_map = {}
    for iss in issuers:
        for q in ("Q1", "Q2"):
            d = data.get(iss, {}).get(q)
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
                    exp_map[(int(iss), d["report_label"], str(ln["n"]), c["label"], "")] = {
                        "שם החברה": d["company_name"], "קובץ מקור": d["source_file"], "עמוד PDF": ln["page"],
                        "טקסט השורה המקורי (מילולית)": ln["text"], "ערך": ln["values"][k], "מס' סעיף": num,
                        "שם הסעיף": lab, "הערת סיווג / נימוק": ln.get("note", "")}
            for o in d.get("outside", []):
                for k, c in enumerate(d["columns"]):
                    exp_map[(int(iss), d["report_label"], "*", c["label"], f"{o['text']}|p{o['page']}")] = {
                        "שם החברה": d["company_name"], "קובץ מקור": d["source_file"], "עמוד PDF": o["page"],
                        "טקסט השורה המקורי (מילולית)": o["text"], "ערך": o["values"][k], "מס' סעיף": "לידיעה",
                        "שם הסעיף": L.OUTSIDE_TAG, "הערת סיווג / נימוק": L.star_mapping_note(o)}
    ok(not dup2, f"AC11 master mapping no duplicate keys {dup2[:3]}")
    ok(set(got_map) == set(exp_map), f"AC11 master mapping rows = data lines x periods ({len(got_map)} vs "
                                     f"{len(exp_map)}); missing={sorted(set(exp_map) - set(got_map))[:2]} "
                                     f"extra={sorted(set(got_map) - set(exp_map))[:2]}")
    bad_rows = []
    for key, e in exp_map.items():
        r = got_map.get(key)
        if r is None:
            continue
        for h, v in e.items():
            g = r[j[h]]
            if isinstance(v, (int, float)) and isinstance(g, (int, float)) and not isinstance(v, bool):
                same = abs(v - g) < 1e-6
            else:
                same = (g if g is not None else "") == (v if v is not None else "")
            if not same:
                bad_rows.append(f"{key[:4]} {h}: {g!r} != {v!r}")
                break
    ok(not bad_rows, f"AC11 master mapping: every row equals the data by key ({len(exp_map)} rows; "
                     f"{len(bad_rows)} differ) {bad_rows[:3]}")
    if want == full:
        ok(ws2.max_row - 1 == len(exp_map), f"AC11 master mapping row count {ws2.max_row - 1} == {len(exp_map)}")
    # T1: 'תקופה עיקרית' – each company x period (months, end) exactly once 'כן', on the latest report
    if "תקופה עיקרית" in idx:
        seen = {}
        for key, (iss, d, k, c) in exp.items():
            r = rows.get(key)
            if r is not None:
                seen.setdefault((iss, c["months"], c["end"]), []).append((d["quarter"], r[idx["תקופה עיקרית"]]))
        bad = [k for k, v in seen.items() if sorted(x for _, x in v) != sorted(["כן"] + ["לא"] * (len(v) - 1))
               or dict(v).get(max(q for q, _ in v)) != "כן"]
        ok(not bad, f"T1 'תקופה עיקרית' one 'כן' per company x period, latest report ({len(seen)} periods; bad={bad[:3]})")
    else:
        ok(False, "T1 column 'תקופה עיקרית' missing in נתונים")
    ws3 = wb["אינדקס קבצים"]
    listed = sorted(ws3.cell(r, 1).value for r in range(2, ws3.max_row + 1))
    base = L.baseline_files()
    exp_files = sorted(rel for rel in base if (not pilot) or rel.split("\\")[0].split(" - ")[0] in issuers)
    ok(listed == exp_files, f"AC1 master file index lists {len(listed)} PDFs (expected {len(exp_files)})")


def integrity(issuers, pilot, scoped=False):
    """Baseline hashes + hygiene. scoped=True (batch use): only the given issuers' own new files are
    required, other new files are tolerated (other batches may be building theirs)."""
    base = L.baseline_files()
    bad = [rel for rel, (size, sha) in base.items()
           if not os.path.exists(os.path.join(L.WORKSPACE, rel)) or sha256(os.path.join(L.WORKSPACE, rel)) != sha]
    ok(not bad, f"AC12 baseline files unchanged ({len(base)} files, {len(bad)} changed/missing)")
    expected = set() if scoped else {L.MASTER_NAME}
    folders = {rel.split("\\")[0] for rel in base}
    for f in folders:
        iss = f.split(" - ")[0]
        if (not pilot and not scoped) or iss in issuers:
            expected |= {os.path.join(f, BC.xlsx_name(iss)), os.path.join(f, BC.pdf_name(iss))}
    new, forbidden = set(), []
    for root, dirs, files in os.walk(L.WORKSPACE):
        rel_root = os.path.relpath(root, L.WORKSPACE)
        top = rel_root.split(os.sep)[0]
        for dname in dirs:
            if dname in ("__pycache__", ".git"):
                forbidden.append(os.path.join(rel_root, dname))
        if top == ".goals":
            continue
        for fn in files:
            rel = os.path.normpath(os.path.join(rel_root, fn))
            if rel not in base:
                new.add(rel)
            if fn.startswith("~$") or fn.endswith((".tmp", ".log", ".pyc")):
                forbidden.append(rel)
    if scoped:
        ok(expected <= new, f"AC12 the issuers' output files exist ({len(expected & new)}/{len(expected)}); "
                            f"missing={sorted(expected - new)[:5]}")
        stray = [n for n in new if not re.search(r"\\\d+ - (?:פירוט תזרים מימון 2026\.xlsx|צילומי מסך תזרים מימון 2026\.pdf)$",
                                                 n) and n != L.MASTER_NAME]
        ok(not stray, f"AC12 no unexpected new files {stray[:5]}")
    else:
        ok(new == expected, f"AC12 new files == expected ({len(new)} vs {len(expected)}); "
                            f"unexpected={sorted(new - expected)[:5]} missing={sorted(expected - new)[:5]}")
    ok(not forbidden, f"AC12 no forbidden artefacts {forbidden[:5]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issuers", nargs="*")
    ap.add_argument("--pilot", action="store_true",
                    help="limit the master file index and the expected new files to --issuers")
    ap.add_argument("--no-master", action="store_true", help="skip the master workbook checks (batch use)")
    ap.add_argument("--out", help="result file (default: %%TEMP%%\\fcf_run\\_runs\\validate_*\\validate.txt)")
    a = ap.parse_args()
    ok(not L.check_labels_against_goal(), "labels identical to goal.md")
    data = CK.load_all()
    folders = sorted({rel.split("\\")[0] for rel in L.baseline_files()}, key=lambda f: int(f.split(" - ")[0]))
    issuers = a.issuers or [f.split(" - ")[0] for f in folders]
    for iss in issuers:
        folder = [f for f in folders if f.split(" - ")[0] == iss]
        if not ok(len(folder) == 1 and iss in data, f"[{iss}] has company folder and final data"):
            continue
        reps = [data[iss][q] for q in ("Q1", "Q2") if q in data[iss]]
        exp_q = sorted(k.split("_")[1] for k in L.load_roles()["sources"] if k.split("_")[0] == iss)
        ok(sorted(d["quarter"] for d in reps) == exp_q, f"[{iss}] AC3 final data for every report {exp_q}")
        company_checks(iss, folder[0], reps)
    res = CK.run_checks({i: data[i] for i in issuers if i in data})
    expl = CK.explanations()
    unexpl = [r for r in res if r["status"] == "MISMATCH" and not CK.explain(expl, r)]
    ok(not unexpl, f"AC6/AC8 C1–C3: {CK.summary(res)}; unexplained mismatches={len(unexpl)} "
                   f"{[CK.expl_key(r) for r in unexpl[:5]]}")
    if not a.no_master:
        master_checks(data, [i for i in issuers if i in data], a.pilot)
        integrity(issuers, a.pilot)
    else:
        integrity(issuers, a.pilot, scoped=True)
    lines = [f"PASS {len(PASS)}  FAIL {len(FAIL)}  INFO {len(INFO)}",
             f"unexplained mismatches: {len(unexpl)}"] + ["FAIL: " + f for f in FAIL] + ["INFO: " + i for i in INFO]
    out = a.out or os.path.join(L.run_dir("validate"), "validate.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines + ["", "passed checks:"] + PASS))
    print("\n".join(lines[:60]))
    print("details:", out)
    sys.exit(0 if not FAIL else 1)


if __name__ == "__main__":
    main()
