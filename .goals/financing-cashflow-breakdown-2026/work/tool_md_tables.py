# -*- coding: utf-8 -*-
"""Generate Markdown tables (mapping + items per period) for a builder/pilot report from final data.

Usage: python tool_md_tables.py <issuer>    -> %TEMP%/fcf_run/<issuer>/md_<issuer>.md
"""
import sys

sys.dont_write_bytecode = True
import os  # noqa: E402

import checks as CK  # noqa: E402
import fcf_lib as L  # noqa: E402


def fmt(v):
    if v is None:
        return ""
    return f"({abs(v):,})" if v < 0 else f"{v:,}"


def main():
    issuer = sys.argv[1]
    data = CK.load_all([issuer])[issuer]
    out = []
    for q in ("Q1", "Q2"):
        d = data.get(q)
        if not d:
            continue
        out.append(f"#### {d['report_label']} – `{d['source_file']}` – financing section on PDF page "
                   f"{L.page_range_text(d['fin_pages'])}")
        out.append("")
        hdr = ["#", "Original line (verbatim)", "Item"] + [c["label"] for c in d["columns"]] + ["Reasoning note"]
        out.append("| " + " | ".join(hdr) + " |")
        out.append("|" + "---|" * len(hdr))
        for ln in d["lines"]:
            it = ln["item"]
            itxt = "=" if it == "total" else (str(it) if isinstance(it, int) else it)
            out.append("| " + " | ".join([str(ln["n"]), ln["text"], itxt] + [fmt(v) for v in ln["values"]]
                                         + [ln.get("note", "")]) + " |")
        out.append("")
        out.append(f"Items per period ({d['report_label']}):")
        out.append("")
        hdr = ["Item"] + [c["label"] for c in d["columns"]]
        out.append("| " + " | ".join(hdr) + " |")
        out.append("|" + "---|" * len(hdr))
        for i in range(1, 15):
            out.append("| " + " | ".join([f"{i}. {L.ITEM_LABEL[i]}"] + [fmt(v) for v in d["items"][str(i)]]) + " |")
        out.append("| " + " | ".join([L.OTHER_LABEL] + [fmt(v) for v in d["other"]]) + " |")
        out.append("| " + " | ".join([f"= {L.TOTAL_LABEL}"] + [fmt(v) for v in d["total"]]) + " |")
        out.append("| " + " | ".join(["C1 check"] + [str(v) for v in d["check"]]) + " |")
        out.append("")
    with open(os.path.join(L.temp_dir(issuer), f"md_{issuer}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("ok")


if __name__ == "__main__":
    main()
