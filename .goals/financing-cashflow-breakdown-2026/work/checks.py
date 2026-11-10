# -*- coding: utf-8 -*-
"""Consistency checks C1–C3 (goal R9) over final report data (data/<issuer>_<Q>.json).

Usage (from any directory):
  python checks.py [--issuers 1618 1039 ...] [--verified-only] [--out <result.json>]
Default scope: every issuer with final data. Results are written to a per-invocation folder
%TEMP%\\fcf_run\\_runs\\checks_<time>_<pid>\\ (checks_result.json + checks_summary.txt) unless --out is
given; the paths are printed. Exit code 0 when no unexplained MISMATCH.

Explanations of genuine differences (restatement, reclassification, source rounding) live in
  work/overrides/<issuer>_checks.json   {"<check>|<issuer>|<period label>|<key>": "explanation", ...}
(one file per company – batch builders write only their own issuers' files) and, for Phase C,
  work/check_explanations.json          (same format, global).
For C1 a report-specific key is also accepted (and tried first), because the same column label can occur
in both reports:  "C1|<issuer>|Q1 2026|<period label>|total".
C2-item rows are informational (INFO): item-level differences when the totals agree.
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import glob  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402

import fcf_lib as L  # noqa: E402

KEYS = [str(i) for i in range(1, 15)] + ["other", "total"]


def load_all(issuers=None, include_unverified=True):
    out = {}
    for p in sorted(glob.glob(os.path.join(L.DATA_DIR, "*_Q[12].json"))):
        m = re.match(r"(\d+)_(Q[12])\.json$", os.path.basename(p))
        if not m or (issuers and m.group(1) not in issuers):
            continue
        d = L.load_json(p)
        if not include_unverified and not d.get("verified"):
            continue
        out.setdefault(m.group(1), {})[m.group(2)] = d
    return out


def col_values(d, k):
    v = {i: d["items"][i][k] for i in d["items"]}
    v["other"] = d["other"][k]
    v["total"] = d["total"][k]
    return v


def find_col(d, months, end):
    hits = [k for k, c in enumerate(d["columns"]) if c["months"] == months and c["end"] == end]
    return hits[0] if hits else None


def key_label(key):
    if key == "total":
        return L.TOTAL_LABEL
    if key == "other":
        return L.OTHER_LABEL
    return f"{key}. {L.ITEM_LABEL[int(key)]}"


def eq(a, b):
    return abs((a or 0) - (b or 0)) < 1e-6


def run_checks(data):
    res = []
    for issuer, reps in sorted(data.items(), key=lambda kv: int(kv[0])):
        name = next(iter(reps.values()))["company_name"]
        ver = {q: bool(d.get("verified")) for q, d in reps.items()}
        # C1
        for q, d in sorted(reps.items()):
            for k, c in enumerate(d["columns"]):
                s = sum(d["items"][i][k] for i in d["items"]) + d["other"][k]
                diff = round(s - d["total"][k], 6)
                res.append({"check": "C1", "issuer": issuer, "company": name, "report": d["report_label"],
                            "period": c["label"], "key": "total", "expected": d["total"][k], "actual": s,
                            "diff": diff, "status": "OK" if eq(diff, 0) else "MISMATCH", "verified": ver[q]})
        if "Q1" not in reps or "Q2" not in reps:
            continue
        q1, q2 = reps["Q1"], reps["Q2"]
        both = ver["Q1"] and ver["Q2"]
        # C2 (totals = mandatory; items = informational)
        for year in (2026, 2025):
            a = find_col(q1, 3, f"{year}-03-31")
            b6 = find_col(q2, 6, f"{year}-06-30")
            b3 = find_col(q2, 3, f"{year}-06-30")
            if a is None or b6 is None or b3 is None:
                res.append({"check": "C2", "issuer": issuer, "company": name, "report": "Q1 vs Q2",
                            "period": f"{year}", "key": "total", "status": "N/A", "verified": both,
                            "note": "חסרה עמודה מתאימה (3 חודשים בדוח Q1 / 6 ו-3 חודשים בדוח Q2)"})
                continue
            va, v6, v3 = col_values(q1, a), col_values(q2, b6), col_values(q2, b3)
            for key in KEYS:
                derived = round(v6[key] - v3[key], 6)
                diff = round(va[key] - derived, 6)
                mandatory = key == "total"
                if not mandatory and eq(diff, 0):
                    continue
                res.append({"check": "C2" if mandatory else "C2-item", "issuer": issuer, "company": name,
                            "report": "Q1 vs Q2", "period": f"3 חודשים שהסתיימו ב-31.03.{year}",
                            "key": key, "expected": derived, "actual": va[key], "diff": diff, "verified": both,
                            "status": ("OK" if eq(diff, 0) else "MISMATCH") if mandatory else "INFO"})
        # C3
        a = find_col(q1, 12, "2025-12-31")
        b = find_col(q2, 12, "2025-12-31")
        if a is None or b is None:
            res.append({"check": "C3", "issuer": issuer, "company": name, "report": "Q1 vs Q2",
                        "period": "שנה שהסתיימה ב-31.12.2025", "key": "total", "status": "N/A", "verified": both,
                        "note": "עמודת שנת 2025 חסרה באחד הדוחות"})
        else:
            va, vb = col_values(q1, a), col_values(q2, b)
            for key in KEYS:
                diff = round(va[key] - vb[key], 6)
                res.append({"check": "C3", "issuer": issuer, "company": name, "report": "Q1 vs Q2",
                            "period": "שנה שהסתיימה ב-31.12.2025", "key": key, "expected": vb[key],
                            "actual": va[key], "diff": diff, "verified": both,
                            "status": "OK" if eq(diff, 0) else "MISMATCH"})
    return res


def explanations(issuers=None):
    """Global work/check_explanations.json + per-company work/overrides/<issuer>_checks.json."""
    out = {}
    p = os.path.join(L.WORK, "check_explanations.json")
    if os.path.exists(p):
        out.update(L.load_json(p))
    for f in sorted(glob.glob(os.path.join(L.OVERRIDES_DIR, "*_checks.json"))):
        iss = os.path.basename(f).split("_")[0]
        if issuers and iss not in issuers:
            continue
        out.update({k: v for k, v in L.load_json(f).items() if not k.startswith("_")})
    return out


def expl_key(r):
    return f"{r['check']}|{r['issuer']}|{r['period']}|{r['key']}"


def expl_key_report(r):
    """Report-specific key, e.g. 'C1|2533|Q1 2026|שנה שהסתיימה ב-31.12.2025|total' (C1 only: the same column
    label can occur in both reports)."""
    return f"{r['check']}|{r['issuer']}|{r.get('report', '')}|{r['period']}|{r['key']}"


def explain(expl, r):
    """Explanation of a check row: the report-specific key first, then the generic key."""
    return expl.get(expl_key_report(r)) or expl.get(expl_key(r), "")


def summary(res):
    out = []
    for chk in ("C1", "C2", "C2-item", "C3"):
        rs = [r for r in res if r["check"] == chk]
        if not rs:
            continue
        cnt = {}
        for r in rs:
            cnt[r["status"]] = cnt.get(r["status"], 0) + 1
        out.append(f"{chk}: " + ", ".join(f"{k}={v}" for k, v in sorted(cnt.items())))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issuers", nargs="*")
    ap.add_argument("--verified-only", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("issuers_pos", nargs="*", help=argparse.SUPPRESS)   # backward compatible: checks.py 1618 1039
    a = ap.parse_args()
    issuers = (a.issuers or []) + (a.issuers_pos or []) or None
    data = load_all(issuers, include_unverified=not a.verified_only)
    res = run_checks(data)
    expl = explanations(issuers)
    unexplained = []
    for r in res:
        r["explanation"] = explain(expl, r)
        if r["status"] == "MISMATCH" and not r["explanation"]:
            unexplained.append(r)
    out = a.out or os.path.join(L.run_dir("checks"), "checks_result.json")
    L.save_json(res, out)
    lines = summary(res)
    unver = sorted({r["issuer"] for r in res if not r.get("verified")}, key=int)
    if unver:
        lines.append(f"NOTE: unverified (auto/draft) data included for issuers: {' '.join(unver)}")
    for r in res:
        if r["status"] in ("MISMATCH", "INFO", "N/A"):
            lines.append(f"  {r['check']} {r['issuer']} {r['period']} {key_label(r['key'])}: expected={r.get('expected')} "
                         f"actual={r.get('actual')} diff={r.get('diff')} [{r['status']}] {r.get('explanation', '')}")
    lines.append(f"unexplained mismatches: {len(unexplained)}")
    txt = "\n".join(lines)
    sp = os.path.splitext(out)[0] + "_summary.txt"
    with open(sp, "w", encoding="utf-8") as f:
        f.write(txt)
    print("\n".join(lines[:6]))
    print(f"unexplained mismatches: {len(unexplained)}")
    print("result:", out)
    print("summary:", sp)
    sys.exit(1 if unexplained else 0)


if __name__ == "__main__":
    main()
