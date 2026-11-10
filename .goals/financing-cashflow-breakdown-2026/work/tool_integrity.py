# -*- coding: utf-8 -*-
"""Integrity / hygiene check: baseline hashes of all source files, new files in the WORKSPACE
(outside .goals), forbidden artefacts (__pycache__, ~$ lock files, .git, temp files).

Usage: python tool_integrity.py [--expect <relpath> ...]
Writes %TEMP%/fcf_run/_runs/integrity_*/integrity.txt (per invocation) and exits 0 only when everything is clean.
"""
import sys

sys.dont_write_bytecode = True
import hashlib  # noqa: E402
import os  # noqa: E402

import fcf_lib as L  # noqa: E402


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    expect = set(sys.argv[sys.argv.index("--expect") + 1:]) if "--expect" in sys.argv else None
    base = L.baseline_files()
    out, ok = [], True
    bad = []
    for rel, (size, sha) in base.items():
        p = os.path.join(L.WORKSPACE, rel)
        if not os.path.exists(p):
            bad.append(f"MISSING {rel}")
        elif os.path.getsize(p) != size or sha256(p) != sha:
            bad.append(f"CHANGED {rel}")
    out.append(f"baseline files: {len(base)}; problems: {len(bad)}")
    out += bad
    ok &= not bad
    new, forbidden = [], []
    for root, dirs, files in os.walk(L.WORKSPACE):
        rel_root = os.path.relpath(root, L.WORKSPACE)
        if rel_root.split(os.sep)[0] == ".goals":
            for d in dirs:
                if d in ("__pycache__", ".git"):
                    forbidden.append(os.path.join(rel_root, d))
            continue
        for d in dirs:
            if d in ("__pycache__", ".git") or d.startswith("~"):
                forbidden.append(os.path.join(rel_root, d))
        for f in files:
            rel = os.path.normpath(os.path.join(rel_root, f))
            if rel not in base:
                new.append(rel)
            if f.startswith("~$") or f.endswith((".tmp", ".log", ".pyc")):
                forbidden.append(rel)
    out.append(f"new files outside .goals: {len(new)}")
    out += ["  " + n for n in sorted(new)]
    if expect is not None:
        missing = expect - set(new)
        extra = set(new) - expect
        out.append(f"expected new files missing: {sorted(missing)}")
        out.append(f"unexpected new files: {sorted(extra)}")
        ok &= not missing and not extra
    out.append(f"forbidden artefacts: {forbidden}")
    ok &= not forbidden
    out.append("RESULT: " + ("CLEAN" if ok else "PROBLEMS"))
    with open(os.path.join(L.run_dir("integrity"), "integrity.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("RESULT:", "CLEAN" if ok else "PROBLEMS")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
