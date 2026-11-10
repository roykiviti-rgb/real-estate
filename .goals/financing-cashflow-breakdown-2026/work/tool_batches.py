# -*- coding: utf-8 -*-
"""Phase A: suggested split of the companies into N batches (whole companies), balanced by workload.

python tool_batches.py [--n 8] [--out work/batches.json]
Workload per report = {A: 1, B: 2, C: 4}[difficulty] + lines / 10 (from work/triage.csv).
Greedy longest-processing-time assignment; ties broken by fewest reports. Writes work/batches.json and
prints a summary table.
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import collections  # noqa: E402
import csv  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402

import fcf_lib as L  # noqa: E402

W_DIFF = {"A": 1.0, "B": 2.0, "C": 4.0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--out", default=os.path.join(L.WORK, "batches.json"))
    a = ap.parse_args()
    rows = list(csv.DictReader(open(os.path.join(L.WORK, "triage.csv"), encoding="utf-8-sig")))
    comp = collections.OrderedDict()
    for r in rows:
        c = comp.setdefault(r["issuer"], {"issuer": r["issuer"], "company": r["company"], "reports": 0,
                                           "A": 0, "B": 0, "C": 0, "weight": 0.0, "verified": 0})
        c["reports"] += 1
        c[r["difficulty"]] += 1
        fp = os.path.join(L.DATA_DIR, f"{r['issuer']}_{r['quarter']}.json")
        if os.path.exists(fp) and (L.load_json(fp).get("verified") or {}).get("status") == "verified":
            c["verified"] += 1          # already verified (pilot): only a rebuild is needed
            continue
        c["weight"] += W_DIFF[r["difficulty"]] + int(r["n_lines"] or 0) / 10.0
    batches = [{"batch": i + 1, "issuers": [], "reports": 0, "A": 0, "B": 0, "C": 0, "weight": 0.0}
               for i in range(a.n)]
    for c in sorted(comp.values(), key=lambda c: (-c["weight"], -c["reports"], int(c["issuer"]))):
        b = min(batches, key=lambda b: (b["weight"], b["reports"], b["batch"]))
        b["issuers"].append(c["issuer"])
        for k in ("reports", "A", "B", "C"):
            b[k] += c[k]
        b["weight"] = round(b["weight"] + c["weight"], 2)
    for b in batches:
        b["issuers"].sort(key=int)
        b["companies"] = [f"{i} {comp[i]['company']}" + (" (מאומת בפיילוט)" if comp[i]["verified"] else "")
                          for i in b["issuers"]]
    json.dump({"method": "greedy LPT on workload = {A:1,B:2,C:4}[difficulty] + lines/10 per report",
               "batches": batches}, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for b in batches:
        print(f"batch {b['batch']}: companies={len(b['issuers'])} reports={b['reports']} A={b['A']} B={b['B']} "
              f"C={b['C']} weight={b['weight']}: {' '.join(b['issuers'])}")
    print("->", a.out)


if __name__ == "__main__":
    main()
