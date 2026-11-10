# -*- coding: utf-8 -*-
"""Self-test of the override paths (isolated – never touches work/overrides, work/data or the WORKSPACE).

Usage (from any directory):  python tool_selftest.py [<issuer> <Q>]      (default: 1484 Q1)

1. manual mode: builds a fully manual override from the report's auto extraction (columns, lines with printed values,
   (*) lines, boxes taken from the automatic geometry), finalizes it in a temp data folder and asserts that items,
   other, totals and the page geometry equal the automatic finalize;
2. auto mode: applies columns/restated, line_items (net_loans), line_text, drop_lines, add_lines, outside_drop,
   outside_add, info_notes, boxes, report/column notes and issues, and asserts the expected results;
   2b. Phase C keys: line_items net_nci (6/14 by sign), outside_sections, info_note_extra, and the rejection of
   info_notes for a kind that has (*) lines and of a non-canonical (*) section;
   2c. iteration-2 keys: other_cf_pages in auto mode (and the rejection of a malformed one), consolidated=false
   (statement name), zoom_blank_cells, sign_flipped (D3 sign remark in the (*) mapping note);
3. renders the company workbook and screenshots PDF of both variants into the temp folder.
Prints PASS/FAIL per assertion and the output folder (%TEMP%/fcf_run/_runs/selftest_*). Exit 0 = all passed.
"""
import sys

sys.dont_write_bytecode = True
import json  # noqa: E402
import os  # noqa: E402
import shutil  # noqa: E402

import fcf_lib as L  # noqa: E402

RES = []


def check(cond, msg):
    RES.append(("PASS" if cond else "FAIL") + ": " + msg)
    return cond


def run(iss, q):
    real_data = L.DATA_DIR
    real_over = L.OVERRIDES_DIR
    out = L.run_dir("selftest")
    auto = L.load_json(os.path.join(real_data, f"{iss}_{q}.auto.json"))
    import finalize_report as F
    # reference = finalize of the auto data without overrides, in an isolated folder
    os.makedirs(os.path.join(out, "ref", "data"))
    os.makedirs(os.path.join(out, "ref", "overrides"))
    shutil.copy(os.path.join(real_data, f"{iss}_{q}.auto.json"), os.path.join(out, "ref", "data"))
    L.DATA_DIR, L.OVERRIDES_DIR = os.path.join(out, "ref", "data"), os.path.join(out, "ref", "overrides")
    ref = F.finalize(iss, q)
    # ---------------- 1. manual mode
    boxes = {}
    for p, g in ref["geometry"].items():
        b = {}
        if g.get("fin_y") and g.get("content_x"):
            b["fin"] = [g["content_x"][0] - 5, g["fin_y"][0], g["content_x"][1] + 5, g["fin_y"][1]]
        if g.get("hdr_box"):
            b["header"] = g["hdr_box"]
        if not g.get("fin_y") and g.get("content_x"):
            b["content"] = g["content_x"]          # pages without a financing box: explicit x-range
        if g.get("printed_page") is not None:
            b["printed_page"] = g["printed_page"]
        if b:
            boxes[p] = b
    ov = {"manual": True, "source_file": auto["source_file"], "cf_pages": auto["cf_pages"],
          "fin_pages": auto["fin_pages"], "header_page": auto["header_page"], "units": auto["units"],
          "columns": [{"months": c["months"], "end": c["end"], "restated": c.get("restated", False),
                       "header_text": c.get("header_text", "")} for c in ref["columns"]],
          "lines": [{"text": ln["text"], "item": ln["item"], "page": ln["page"], "bbox": ln.get("bbox"),
                     "values": [(ln.get("raw") or [None] * len(ln["values"]))[k] or ln["values"][k]
                                for k in range(len(ln["values"]))]} for ln in auto["lines"]],
          "outside": auto.get("outside", []), "context_sections": auto.get("context_sections", {}),
          "boxes": boxes, "text_layer": "none – self-test"}
    os.makedirs(os.path.join(out, "manual", "data"))
    os.makedirs(os.path.join(out, "manual", "overrides"))
    L.save_json(ov, os.path.join(out, "manual", "overrides", f"{iss}_{q}.json"))
    L.DATA_DIR, L.OVERRIDES_DIR = os.path.join(out, "manual", "data"), os.path.join(out, "manual", "overrides")
    man = F.finalize(iss, q)
    check(man["mode"] == "manual", "manual: mode = manual")
    check(man["items"] == ref["items"] and man["other"] == ref["other"] and man["total"] == ref["total"],
          "manual: items, other and totals equal the automatic result")
    check([c["label"] for c in man["columns"]] == [c["label"] for c in ref["columns"]], "manual: column labels equal")
    for p in ref["geometry"]:
        a, b = ref["geometry"][p], man["geometry"].get(p, {})
        same = all(a.get(k) == b.get(k) for k in ("fin_y", "hdr_box", "hdr_strip"))
        close = all(abs(x - y) < 1e-6 for x, y in zip(a.get("content_x") or [], b.get("content_x") or []))
        check(same and close, f"manual: geometry of page {p} equals the automatic geometry")
    # ---------------- 2. auto mode with every correction key
    ln = auto["lines"]
    second = ln[1]
    # a (*) kind that the financing section does not present (R5: only then is an info note used) and that gets no
    # (*) line here (Phase C: info_notes is rejected for a kind with (*) lines); the added (*) line uses the other kind
    div_in_fin = any(x["item"] in (11, 12) for x in ref["lines"])
    int_in_fin = any(x["item"] == 13 for x in ref["lines"])
    nk = "dividend" if not div_in_fin else ("interest" if not int_in_fin else None)
    sk = "dividend" if nk == "interest" else "interest"
    ov2 = {"columns": {"c2": {"restated": True}}, "line_items": {"1": "net_loans"}, "line_text": {"1": "טקסט בדיקה"},
           "drop_lines": [2],
           "add_lines": [{"after": 1, "page": second["page"], "text": second["text"] + " (ידני)",
                          "item": second["item"], "values": second["values"], "bbox": second["bbox"]}],
           "outside_drop": list(range(1, len(auto.get("outside", [])) + 1)),
           "outside_add": [{"info": sk, "section": "פעילות שוטפת", "page": ln[0]["page"],
                            "text": "ריבית ששולמה (בדיקה)" if sk == "interest" else "דיבידנד ששולם (בדיקה)",
                            "values": [-1] * len(ref["columns"]), "bbox": ln[0]["bbox"]}],
           "boxes": {str(auto["fin_pages"][0]): {"printed_page": 999}},
           "report_notes": ["r"], "column_notes": {"c1": "c"}, "issues": ["i"]}
    if nk:
        ov2["info_notes"] = {nk: "הערת בדיקה"}
    os.makedirs(os.path.join(out, "auto", "data"))
    os.makedirs(os.path.join(out, "auto", "overrides"))
    shutil.copy(os.path.join(real_data, f"{iss}_{q}.auto.json"), os.path.join(out, "auto", "data"))
    L.save_json(ov2, os.path.join(out, "auto", "overrides", f"{iss}_{q}.json"))
    L.DATA_DIR, L.OVERRIDES_DIR = os.path.join(out, "auto", "data"), os.path.join(out, "auto", "overrides")
    d = F.finalize(iss, q)
    check(d["columns"][1]["label"].endswith("(מוצג מחדש)"), "auto: restated column label")
    check(d["lines"][0]["text"] == "טקסט בדיקה" and d["lines"][0]["item"] == "net_loans", "auto: line_text, line_items")
    check(d["lines"][0]["resolved"] == [4 if (v or 0) >= 0 else 7 for v in d["lines"][0]["values"]],
          "auto: net_loans resolved per column by sign")
    check(d["lines"][1].get("added") and d["lines"][1]["auto_n"] is None and len(d["lines"]) == len(ln),
          "auto: drop_lines + add_lines (renumbered, same count)")
    check(d["check"] == ref["check"], "auto: C1 unchanged after replacing a line by the same values")
    check(len(d["outside"]) == 1 and d["info"][sk]["values"] == [-1] * len(ref["columns"]),
          f"auto: outside_drop + outside_add -> (*) {sk} info row")
    if nk:
        check(d["info"][nk]["note"] == "הערת בדיקה", f"auto: info_notes ({nk})")
    check(d["geometry"][str(auto["fin_pages"][0])]["printed_page"] == 999, "auto: boxes.printed_page")
    check(d["report_notes"] == ["r"] and d["column_notes"] == {"c1": "c"} and d["issues"] == ["i"],
          "auto: report_notes, column_notes, issues")
    # ---------------- 2b. Phase C keys: net_nci, outside_sections, info_note_extra; info_notes + (*) lines rejected
    k3 = next(str(x["n"]) for i, x in enumerate(ln) if i >= 2 and x["item"] not in ("total", "subtotal", "text"))
    ov3 = {"line_items": {k3: "net_nci"},
           "outside_drop": list(range(1, len(auto.get("outside", [])) + 1)),
           "outside_add": [{"info": "interest", "section": "פעילות שוטפת", "page": ln[0]["page"],
                            "text": "ריבית ששולמה (בדיקה)", "values": [-1] * len(ref["columns"]),
                            "bbox": ln[0]["bbox"]}],
           "outside_sections": {"1": L.SECTION_APPX_OPERATING},
           "info_note_extra": {"interest": "הערה ספציפית"}}
    os.makedirs(os.path.join(out, "auto3", "data"))
    os.makedirs(os.path.join(out, "auto3", "overrides"))
    shutil.copy(os.path.join(real_data, f"{iss}_{q}.auto.json"), os.path.join(out, "auto3", "data"))
    L.save_json(ov3, os.path.join(out, "auto3", "overrides", f"{iss}_{q}.json"))
    L.DATA_DIR, L.OVERRIDES_DIR = os.path.join(out, "auto3", "data"), os.path.join(out, "auto3", "overrides")
    d3 = F.finalize(iss, q)
    l3 = next(x for x in d3["lines"] if str(x.get("auto_n")) == k3)
    check(l3["item"] == "net_nci" and l3["resolved"] == [6 if (v or 0) >= 0 else 14 for v in l3["values"]],
          "auto: net_nci resolved per column by sign (6 / 14)")
    check(d3["outside"][0]["section"] == L.SECTION_APPX_OPERATING, "auto: outside_sections sets a canonical section")
    check(d3["info"]["interest"]["note"] == f"{L.SECTION_APPX_OPERATING}; הערה ספציפית",
          "auto: (*) note = canonical section(s) + info_note_extra")
    ov3["info_notes"] = {"interest": "x"}
    L.save_json(ov3, os.path.join(out, "auto3", "overrides", f"{iss}_{q}.json"))
    try:
        F.finalize(iss, q)
        rejected = False
    except SystemExit:
        rejected = True
    check(rejected, "auto: info_notes for a kind with (*) lines is rejected")
    ov3.pop("info_notes")
    ov3["outside_sections"] = {"1": "נספח כלשהו"}
    L.save_json(ov3, os.path.join(out, "auto3", "overrides", f"{iss}_{q}.json"))
    try:
        F.finalize(iss, q)
        rejected = False
    except SystemExit:
        rejected = True
    check(rejected, "auto: a non-canonical (*) section is rejected")
    # ---------------- 2c. iteration-2 keys: other_cf_pages (auto mode), consolidated, zoom_blank_cells, sign_flipped
    ov4 = {"other_cf_pages": {"solo": [1], "board": []}, "consolidated": False, "zoom_blank_cells": True,
           "outside_drop": list(range(1, len(auto.get("outside", [])) + 1)),
           "outside_add": [{"info": "interest", "section": L.SECTION_APPX_UNSTATED, "page": ln[0]["page"],
                            "text": "ריבית ששולמה (בדיקה)", "values": [-1] * len(ref["columns"]),
                            "bbox": ln[0]["bbox"], "sign_flipped": True}]}
    os.makedirs(os.path.join(out, "auto4", "data"))
    os.makedirs(os.path.join(out, "auto4", "overrides"))
    shutil.copy(os.path.join(real_data, f"{iss}_{q}.auto.json"), os.path.join(out, "auto4", "data"))
    L.save_json(ov4, os.path.join(out, "auto4", "overrides", f"{iss}_{q}.json"))
    L.DATA_DIR, L.OVERRIDES_DIR = os.path.join(out, "auto4", "data"), os.path.join(out, "auto4", "overrides")
    d4 = F.finalize(iss, q)
    check(d4["other_cf_pages"] == {"solo": [1], "board": []}, "auto: other_cf_pages accepted in auto mode")
    check(d4.get("consolidated") is False and L.cf_statement_name(d4) == L.CF_NAME_SOLE
          and L.cf_statement_name(ref) == L.CF_NAME_CONS, "auto: consolidated=false -> statement named CF_NAME_SOLE")
    check(d4.get("zoom_blank_cells") is True and "zoom_blank_cells" not in d3, "auto: zoom_blank_cells only when set")
    check(L.STAR_SIGN_REMARK["interest"] in L.star_mapping_note(d4["outside"][0])
          and L.STAR_SIGN_REMARK["interest"] not in L.star_mapping_note(d3["outside"][0]),
          "auto: sign_flipped -> D3 sign remark in the (*) mapping note")
    ov4["other_cf_pages"] = {"solo": ["x"]}
    L.save_json(ov4, os.path.join(out, "auto4", "overrides", f"{iss}_{q}.json"))
    try:
        F.finalize(iss, q)
        rejected = False
    except SystemExit:
        rejected = True
    check(rejected, "auto: a malformed other_cf_pages is rejected")
    # ---------------- 3. render both variants (temp outputs only)
    L.DATA_DIR, L.OVERRIDES_DIR = real_data, real_over
    other_q = "Q2" if q == "Q1" else "Q1"
    op = os.path.join(real_data, f"{iss}_{other_q}.json")
    import build_company as B
    import fcf_render as R
    for tag, dd in (("manual", man), ("auto", d)):
        reps = sorted([dd] + ([L.load_json(op)] if os.path.exists(op) else []), key=lambda r: r["quarter"])
        B.build_xlsx(iss, reps, os.path.join(out, f"{tag}.xlsx"), L.load_roles(), draft=True)
        R.build_screenshots(iss, reps, os.path.join(out, f"{tag}.pdf"), draft=True)
        check(os.path.getsize(os.path.join(out, f"{tag}.pdf")) > 10000, f"render: {tag} workbook + screenshots built")
    return out


def main():
    iss, q = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("1484", "Q1")
    out = run(iss, q)
    with open(os.path.join(out, "selftest.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(RES))
    print("\n".join(RES))
    print("output:", out)
    sys.exit(0 if all(r.startswith("PASS") for r in RES) else 1)


if __name__ == "__main__":
    main()
