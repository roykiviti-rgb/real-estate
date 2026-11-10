# Pilot progress — 1618 קבוצת אשטרום (attempt 2)

Started 2026-11-09 18:40 (attempt 2). Attempt 1 left only explore_*.py (now deleted) + %TEMP%\fcf_pilot renders.

## STATUS: pilot outputs DONE (xlsx, screenshots PDF, master, checks, integrity) — report written.

## Key facts (verified)
- Q1 file `1618_קבוצת אשטרום בע_מ_2026_Q1_1743867.pdf` (81 pp): consolidated CF statement PDF pp 55–57
  (printed 10–12); financing section p56 (printed 11); solo 38D CF = pp 74–75 (not used); board report CF summary p29.
  Columns: 3M-31.03.2026 (unaudited), 3M-31.03.2025 (unaudited), FY-31.12.2025 (audited). Units אלפי ש"ח.
- Q2 file `1618_קבוצת אשטרום בע_מ_2026_Q2_1766160.pdf` (97 pp): consolidated CF pp 66–68 (printed 12–14);
  financing p67 (printed 13); solo CF pp 90–91; board summary pp 36–37. Columns: 6M-30.06.2026, 6M-30.06.2025,
  3M-30.06.2026, 3M-30.06.2025 (all unaudited), FY-31.12.2025 (audited). Units אלפי ש"ח.
- 13 financing lines + total in both reports, same wording; mapping 1:1 (3,1,8,4,7,5,10,13,2,6,14,11,12,total).
- Totals: Q1 810,572 / 127,744 / 427,605 ; Q2 1,247,856 / 128,517 / 437,284 / 773 / 427,605. C1 = 0 everywhere.
- Interest paid & dividends paid only in financing → (*) info rows = 0.
- C2 totals OK; item-level INFO: Q1-2025 LT loans received/repaid differ by ±1,267 between the reports (net 0)
  → check_explanations.json + column notes. C3 OK (16/16).
- Values verified: text layer + visual check of 200-DPI renders (p56, p67).

## Pipeline (work\) — reusable for the full run
1. `python extract_report.py <issuer> <Q>` → data\<issuer>_<Q>.auto.json + %TEMP%\fcf_pilot\review_<issuer>_<Q>.txt
2. review renders; write overrides\<issuer>_<Q>.json (verified record, notes, fixes)
3. `python finalize_report.py <issuer> <Q>` → data\<issuer>_<Q>.json (FINAL)
4. `python build_company.py <issuer>` → company xlsx + screenshots PDF (fcf_render.py)
5. `python checks.py [issuers]` (C1–C3; explanations in check_explanations.json)
6. `python build_master.py [--pilot]` → master xlsx
7. `python tool_integrity.py` → baseline hashes + new-file list (%TEMP%\fcf_pilot\integrity.txt)
Review helpers: tool_shots.py, tool_clip.py, tool_pdf2png.py, tool_pdfclip.py, tool_excel_check.ps1 (Excel COM on a TEMP copy),
tool_dump.py, tool_md_tables.py, tool_integrity.py. validate.py written (scoped: --issuers/--pilot): pilot 473 PASS / 0 FAIL.

## Milestones
- [x] pages found (Q1, Q2)
- [x] values extracted + verified (data\1618_Q1.json, data\1618_Q2.json)
- [x] mapping decided
- [x] company xlsx written (opened via Excel COM copy: OK, formulas = 0, RTL)
- [x] screenshots PDF written (9 pages, reviewed)
- [x] master xlsx written (--pilot; 5 sheets; opened via Excel COM copy: OK)
- [x] checks C1–C3 run (C1 8/8, C2 2/2, C3 16/16, 2 INFO)
- [x] integrity: 178 baseline files unchanged; 3 new files only
- [x] pilot-report.md written
- [x] %TEMP%\fcf_pilot cleaned (last step) — deleted; explore_*.py deleted
