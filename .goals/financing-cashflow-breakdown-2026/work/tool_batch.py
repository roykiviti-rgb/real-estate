# -*- coding: utf-8 -*-
"""Run a pipeline step for many reports/companies in parallel (each task in its own subprocess, so a
crash in one report never affects another). Results go to a per-invocation folder
%TEMP%\\fcf_run\\_runs\\batch_<step>_<time>_<pid>\\ (summary.txt + summary.json + one log per task).

Usage (from any directory):
  python tool_batch.py extract  --issuers 1039 1618 ... [--workers 8]
  python tool_batch.py finalize --issuers ...
  python tool_batch.py build    --issuers ... [--draft] [--no-pdf]
  python tool_batch.py review   --issuers ...             (tool_review.py for every report)
  ... --all   instead of --issuers: every company (Phase A / Phase C only – a batch builder must always
              pass its own issuers, otherwise it would overwrite other batches' data).
Quarters = the reports that exist for the issuer (roles.json).
"""
import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import argparse  # noqa: E402
import json  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ThreadPoolExecutor  # noqa: E402

import fcf_lib as L  # noqa: E402


def reports(issuers=None):
    roles = L.load_roles()
    keys = sorted(roles["sources"], key=lambda k: (int(k.split("_")[0]), k))
    out = [tuple(k.split("_")) for k in keys]
    if issuers:
        out = [x for x in out if x[0] in issuers]
    return out


def run_task(args, log_path):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    t0 = time.time()
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env, cwd=L.WORK)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(" ".join(args) + "\n--- stdout\n" + (p.stdout or "") + "\n--- stderr\n" + (p.stderr or ""))
    last = [x for x in ((p.stdout or "") + "\n" + (p.stderr or "")).splitlines() if x.strip()]
    return {"args": args[1:], "rc": p.returncode, "secs": round(time.time() - t0, 1),
            "last": last[-1][:300] if last else "", "log": log_path}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["extract", "finalize", "build", "review"])
    ap.add_argument("--issuers", nargs="*")
    ap.add_argument("--all", action="store_true", help="every company (Phase A/C only)")
    ap.add_argument("--workers", type=int, default=max(2, (os.cpu_count() or 4) - 2))
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--allow-unverified", action="store_true")
    a = ap.parse_args()
    if not a.issuers and not a.all:
        raise SystemExit("give --issuers <your issuers> (or --all for every company – Phase A/C only)")
    if a.issuers and a.all:
        raise SystemExit("use either --issuers or --all")
    known = {iss for iss, _ in reports()}
    unknown = [i for i in (a.issuers or []) if i not in known]
    if unknown:
        raise SystemExit(f"unknown issuer(s): {unknown}")
    rd = L.run_dir(f"batch_{a.step}")
    tasks = []
    if a.step in ("extract", "finalize", "review"):
        script = {"extract": "extract_report.py", "finalize": "finalize_report.py", "review": "tool_review.py"}[a.step]
        for iss, q in reports(a.issuers):
            args = [os.path.join(L.WORK, script), iss, q]
            if a.step == "finalize" and a.allow_unverified:
                args.append("--allow-unverified")
            tasks.append((args, os.path.join(rd, f"{iss}_{q}.log")))
    else:
        issuers = sorted({iss for iss, _ in reports(a.issuers)}, key=int)
        for iss in issuers:
            args = [os.path.join(L.WORK, "build_company.py"), iss]
            if a.draft:
                args.append("--draft")
            if a.no_pdf:
                args.append("--no-pdf")
            tasks.append((args, os.path.join(rd, f"{iss}.log")))
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        res = list(ex.map(lambda t: run_task(*t), tasks))
    ok = [r for r in res if r["rc"] == 0]
    bad = [r for r in res if r["rc"] != 0]
    lines = [f"step={a.step} tasks={len(res)} ok={len(ok)} failed={len(bad)}  ({rd})"]
    for r in res:
        lines.append(f"{'OK ' if r['rc'] == 0 else 'ERR'} {' '.join(r['args']):<22} {r['secs']:>6}s  {r['last']}")
    txt = "\n".join(lines)
    with open(os.path.join(rd, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    with open(os.path.join(rd, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(lines[0])
    print("summary:", os.path.join(rd, "summary.txt"))
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
