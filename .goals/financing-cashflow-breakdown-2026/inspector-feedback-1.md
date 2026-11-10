# Inspector Feedback — Iteration 1 (final Inspector)

Date: 2026-11-10. References: `goal.md`, `goal-amendment-1.md` (T1, T2, A1 = the pilot is the approved design),
`goal-amendment-2.md` (T3 cancelled), `work/phaseB-conventions.md`, `orchestrator-decisions-1.md` (D1–D3), and the 8 batch
inspections in `inspection-1/batch-1.md` … `batch-8.md`. Those 8 files cover the per-company values. They were read in full,
and every issue they raise is classified below (cross-reference in §4.4).

## Verdict: FAIL

The global criteria hold. Source selection, files, the master equal to the company workbooks by key, T1/T2, the screenshot
resolutions, integrity and the quality gate are all correct. Every number was confirmed against the PDFs by the batch
Inspectors.

The run still fails on **10 must-fix items**:
- 2 mapping violations of orchestrator decision D2 (1905, 2386);
- 1 (\*) section note that contradicts the report (2418);
- 1 non-verbatim line text (2396 Q1);
- 2 incomplete implementations of orchestrator decisions (D3 line notes for 121/1083; D1 notes for 2559);
- 4 statements in the deliverables that contradict the source (2389 column notes, "38ד" page labels, 2392 captions, 1484
  "מאוחד").

There are also **10 should-fix groups**: documentation, consistency, cosmetic screenshot polish and `validate.py`.

Classification rule used:
- **must fix** = violates the goal, an amendment, a convention or an orchestrator decision; or wrong data, a wrong item, or a
  non-verbatim line text; or a statement in a deliverable that contradicts the source;
- **should fix** = missing or incomplete documentation, process remarks, consistency of notes, cosmetic rendering, tooling;
- **no action** = documented judgment calls or approved pilot design.

---------------------------------------------------------------------------------------------------------------

## 1. Acceptance Criteria Check

All checks below were run by my own scripts, read-only, in `%TEMP%\fcf_insp\final\`. Per-company value checks (AC4, most of
AC7/AC9) rely on the 8 batch inspections; I re-checked internal consistency for all 86 companies.

- [x] **AC1 – Source inventory and selection: verified.**
  - The master `אינדקס קבצים` has 178 rows. Their paths equal the 178 baseline PDFs, with no duplicates.
  - Roles: 162 `מקור הנתונים – דוח רבעוני`, 10 `נספח – שומה/הערכת שווי`, 3 `מכתב נלווה/תמצית`, 2 `נספח – דוחות כספיים של חברה
    מוחזקת`, 1 `גרסה חלופית – לא בשימוש`.
  - `בשימוש=כן` on 162 files: exactly 1 per company×quarter (162 keys, none duplicated).
  - Special cases:
    - **1829 Q1/Q2:** `-01` is used; the main file is a 1-page appraiser letter.
    - **2559 Q1:** `-01` (clean "דוח מתקן") is used. `-02` is the alternative (marked-up) version. The main file is a 3-page
      excerpt. The workbook and the master state that the financing section of `-02` (p27) is identical to `-01` (p25).
    - **2520 `-01` (Q1/Q2):** investee statements of סלע איסתא, not used.
    - These roles agree with `..\_extra_attachments.csv` (16 attachments).
  - Page counts: all 178 equal the real PDF page counts (PyMuPDF). Issuer, quarter and report ID are consistent.
  - Every company `מקורות` sheet lists exactly its folder's PDFs. File, quarter, report ID, pages, role, used flag, CF pages,
    financing pages and notes are identical to the master index: 0 differences in 86 workbooks.
  - The wrong "38ד" page labels in the notes are issue **M8**; they do not affect AC1's selection.
- [x] **AC2 – Files and names: verified.**
  - The 86 folders each contain exactly the baseline PDFs plus `<iss> - פירוט תזרים מימון 2026.xlsx` and
    `<iss> - צילומי מסך תזרים מימון 2026.pdf`. The root contains the master. There is no other new file outside `.goals`:
    173 new = 172 + 1.
  - All 87 `.xlsx` load in openpyxl, and every sheet is RTL.
  - **Excel COM, on copies in `%TEMP%`.** I tested the master and 13 company workbooks (111, 121, 434, 715, 1068, 1618, 1722,
    1905, 2386, 2396, 2418, 2503, 2533). Each opened in its own fresh Excel instance with **DisplayAlerts ON** and a
    180-second watchdog. The results:
    - none blocked (5.8–10.3 s), so no prompt was shown;
    - no `[Repaired]` in any caption;
    - no new `error*.xml` repair log;
    - every sheet RTL, and 0 error cells;
    - after `CalculateFull`, every check formula is 0, except the documented C1 columns: 715 (−1, +1, −1, +1) and 2533
      (−1,000 ×2).
- [x] **AC3 – Periods: verified globally.**
  - 648 period columns across the 86 company workbooks: Q1 3M ×152, FY ×162, Q2 6M ×172, Q2 3M ×162.
  - All companies are calendar-year.
  - Labels match months and end dates in the company headers, both mapping sheets and the master.
  - **T2:** all 162 non-YTD 3-month columns carry ` (אפריל–יוני)`, and no YTD column does. `(מוצג מחדש)` follows the range and
    is consistent with the restated flag.
  - Missing-Q1 statements are present for all 10 companies, in the workbook, the master and the builder report.
  - Per-report column identity and the restated flags were confirmed on images by the batch inspectors.
- [ ] **AC4 – Exact values: verified by the 8 batch inspectors, with one text defect.**
  - All 648 columns: every value, total and (\*) value was confirmed on images.
  - The batch FAILs are not value errors.
  - Line text: the 2396 Q1 total line is not verbatim (**M4**).
- [ ] **AC5 – Mapping: FAILED.**
  - **Plug-free: verified.**
    - In all 86 workbooks, every item, `אחר`, total and (\*) row equals the sum of its `מיפוי שורות` lines, per period. Net
      lines `4/7` and `6/14` are resolved by sign. Result: 0 mismatches.
    - The master `מיפוי שורות` has 6,190 rows, equal to the company sheets by key (issuer, report, line, period) in text,
      value, page, item and note. 24 net-line rows are correctly resolved by sign.
  - **Consistency: FAILED.**
    - 1905 and 2386 violate D2 (**M1**, **M2**).
    - D3 line notes are missing (**M5**).
    - Several evidence notes are weak (**S2**).
  - The cross-company review is in §4.3.
- [x] **AC6 – C1: verified.**
  - C1 = 0 in 638 of 648 columns. The 10 non-zero columns are source inconsistencies, kept as printed and documented: 715 ×4,
    719, 2417, 2478, 2483 and 2533 ×2.
  - These are listed in `checks.py` / `validate.py` as INFO and in the master `חסרים והערות`.
- [ ] **AC7 – (\*) treatment: FAILED.**
  - The 2418 (\*) section is wrong (**M3**). The D3 sign remark is missing on the line notes (**M5**).
  - Some cross-report (\*) differences are undocumented (**S3**), and some (\*) dividend notes are inconsistent (**S4**).
  - Amounts are otherwise correct.
- [x] **AC8 – C2/C3: verified.** `checks.py` reports:
  - C2: 125 OK and 27 explained mismatches;
  - C3: 1,216 OK;
  - C2-item: 66 INFO, all explained;
  - unexplained mismatches: 0.

  I recomputed C2/C3 for 1905 and 2386 under the D2 remapping (M1/M2): no new C2 or C3 item difference arises.
- [x] **AC9 – Company workbook layout: verified globally.**
  - Sheet names and order; group headers, items 1–14, `אחר`, total, check, the two (\*) rows and `הערות` in the exact order and
    labels.
  - Header block: the name equals the folder name with `"` restored, and the issuer is correct.
  - The 7 source rows under each column.
  - Numeric amount cells, format `#,##0;-#,##0;0`. Live `=SUM(` check formulas. RTL.
  - The 1484 wording issue is **M10**.
- [ ] **AC10 – Screenshots PDFs: resolutions and captions verified; FAILED on caption text (M9, M10) and should-fix polish
  (S7).** Details in §3.
- [x] **AC11 – Master: verified.**
  - 5 sheets with the exact names, all RTL.
  - `נתונים` has 648 rows = 648 company columns. There are no duplicate keys and no missing or extra keys.
  - **Key-based comparison against all 86 company workbooks: 0 differences** in every field:
    - name, folder, file, pages, months, end date, currency, units;
    - items 1–14, `אחר`, total, check;
    - both (\*) amounts, both (\*) notes (company note of that report), restated flag, column notes, screenshot path.
  - **T1:** 572 `כן` and 76 `לא`. Each of the 572 company×(months, end date) groups has exactly one `כן`, on the latest
    report. All 76 FY-2025 rows of Q1 reports are `לא` (76 of 76 companies with Q2). No other period appears in two reports.
  - T1 and T2 are explained in `הסבר` rows 39–40.
  - Numeric cells use the thousands format.
- [x] **AC12 – Integrity and hygiene: verified.**
  - The SHA-256 and size of all 178 source PDFs equal `baseline_files_sha256.csv`.
  - The only new items outside `.goals` are the 172 company files and the master. There is no nested directory in any company
    folder.
  - Nothing anywhere in the WORKSPACE, including `.goals`, matches `~$*`, `__pycache__`, `.git`, `*.tmp`, `*.log`, `*.pyc`,
    `*.bak` or `*.lock`.
  - `.goals` holds only `.md`, `.json`, `.py`, `.csv` and `.ps1` (585 files).
  - There is no `.git` in the 4 parent folders up to `agent folder`, and `%TEMP%\fcf_run` does not exist.
- [x] **AC13 – Self-validation and report: verified, with should-fix items for the tool (S9) and report updates.**
  - `validate.py` runs with `python <full path>` from `%TEMP%\fcf_insp\final` and from `C:\`. It prints
    `PASS n FAIL n INFO n` and the details path, exits 0 on the full run, and exits 1 when a check fails (verified:
    `--issuers 1618` with the master gives `FAIL 105`, exit 1).
  - `builder-report-1.md` §9 documents **all 162** company×quarter reports. Each entry has:
    - source file, CF pages and financing page;
    - periods, units/currency and text layer;
    - judgement calls;
    - (\*) classification;
    - flags;
    - verification (abbreviated with a pointer to `verified.method`);

    and the report also gives a common verification basis.
  - The 10 missing Q1 reports are stated.
  - §3-A contains a factually wrong statement (see M1/M2).

## 2. Quality Gate

- Commands, both run with the working directory `C:\Users\רואי\AppData\Local\Temp\fcf_insp\final` (outside WORKSPACE) and
  `TEMP` redirected there:
  - `python "<WORKSPACE>\.goals\financing-cashflow-breakdown-2026\work\checks.py" --out <tmp>`
  - `python "<WORKSPACE>\.goals\financing-cashflow-breakdown-2026\work\validate.py" --out <tmp>` (full run, no `--issuers`).
- **Result: PASS.**
  - `checks.py`: C1 OK=638 MISMATCH=10, C2 OK=125 MISMATCH=27, C2-item INFO=66, C3 OK=1216, `unexplained mismatches: 0`,
    exit 0.
  - `validate.py`: `PASS 36751  FAIL 0  INFO 10` (the 10 explained C1 columns); `AC6/AC8 … unexplained mismatches=0`; exit 0;
    22 s.
- **Gate defect (should-fix S9).** `validate.py --issuers X` without `--no-master` reports false failures:
  - `--issuers 1618 2396` gives FAIL 182; `--issuers 1618` gives FAIL 105 and exit 1.
  - The cause: `master_checks()` enumerates only the subset's expected rows, then compares them **by position** from row 2 of
    the 648-row master. It also compares the row counts with the subset.
  - With `--no-master` the same subset passes (PASS 664 / FAIL 0).
  - This **is a defect of the gate's subset mode**. The full run, which is the goal's gate, is unaffected.
  - The master comparison is also partial even in the full run. It checks only the issuer, period label, items 1–14, total,
    `אחר`, T1 and the row counts. It does not check the (\*) amounts and notes, the check column, file/pages, months/end,
    currency/units, the restated flag, notes or the screenshot path, and it compares `מיפוי שורות` only by row count.
- The gate passing does not mean the goal is met. The must-fix items below are mapping decisions and texts that the gate cannot
  detect.

## 3. Screenshots PDFs (AC10 / amendment 2) – evidence

These are programmatic checks of all 86 PDFs and all 607 image pages.

- **Image formats and resolution.** All are native pixels with no resampling.

  | Kind | Count | Format | Measured DPI |
  |---|---|---|---|
  | Full pages | 162 | PNG/Flate | **150.0–150.1** (pixel size ÷ source page size) |
  | Context pages | 198 | JPEG | **120.0–120.1**, IJG quality **88** in all 198 (quantisation tables) |
  | Zooms | 162 | PNG | **220** |
  | (\*) crops | 85 | PNG | **220** |

  - How the zoom and crop DPI was established, independently of the renderer: each image was split at the dashed separators.
    Each part's ink mask was matched by FFT cross-correlation against fresh renders of the cited source pages:
    - at 220 DPI the best overlap was 0.72–1.0;
    - at 200 and 240 DPI it was 0.16–0.45 (control on 486, 823, 1618, 1722, 2533);
    - a 180–260 DPI sweep on the 8 lowest-scoring crops peaks at 220 for every part except one 157-px header part of the
      1532 Q1 (\*) crop (flat, 215 ≈ 220).
  - So **R7 is met**: full-page renders at ≥110 DPI (150 and 120), zoomed crops at ≥200 DPI (220).
- **Unchanged from the pilot (no extra compression).** The settings are 150/220/120 DPI and PNG/PNG/JPEG q88, as recorded for
  the pilot in `builder-phaseA-report.md` and in the A1 design.
  - 1618 now has 9 pages and 2,606,819 bytes; the pilot had "9 pages, 2.6 MB".
  - PDF sizes: 1.50 MB min, 2.18 MB median, 3.03 MB max.
  - **T3 is not applied (correct).**
- **Captions.** Every one of the 607 image pages has a caption. Each names:
  - the issuer and company;
  - `Q1/Q2 2026`;
  - the source file (report ID, `.pdf`) and the PDF page number;
  - the image number and description.
  - The only automatic "misses" were 59 pages of companies whose names contain parentheses; that is bidi text-extraction
    order, not a missing caption.
- **Pages shown equal the pages cited.** For all 162 reports the set of pages in the TOC (full, zoom, (\*), context) equals the
  consolidated CF pages cited in `מקורות` and the master.
- **Defects:** wrong captions (M9 2392, M10 1484) and cosmetic issues (S7, including **25 zooms without the blue/orange
  frames**, listed there).

---------------------------------------------------------------------------------------------------------------

## 4. Issues Found

### 4.1 MUST FIX (10)

**M1 – 1905: gross `קבלת אשראי` / `פירעון אשראי` mapped to item 5. This violates D2 (and R3 rule A).**
(batch 7 B1)

*Where and why*
- Lines n2 and n3: Q1 p40 lines 2–3 and Q2 p44 lines 2–3.
- The lines include an 86.1 M land loan from a bank, repayable 26.3.2028 (note p42 in Q1, p46 in Q2).
- The balance sheet is mixed:
  - Q1 p37: current `אשראי מתאגידים בנקאיים ואחרים` 485,967; non-current `הלוואות מתאגידים בנקאיים ומנותני אשראי אחרים`
    103,947 (784 at 31.12.2025);
  - 30.6.2026: non-current 104,442.
- The current note relies on "רוב האשראי שוטף", which D2 rejects.

*Fix*
- In `overrides/1905_Q1.json` and `1905_Q2.json`, set `line_items`: n2 → **4** and n3 → **7**.
- New Hebrew notes that cite the evidence above and say "יתרות שוטפות ולא שוטפות – כלל A / החלטה D2 → 4/7". Do the same in
  both reports.
- Expected vectors. Column order: Q1 3M-26, 3M-25, FY25 | Q2 6M-26, 6M-25, AJ-26, AJ-25, FY25.

  | Item | Q1 | Q2 |
  |---|---|---|
  | 4 | 186,911 / 2,312 / 179,203 | 186,911 / 282,312 / 0 / 280,000 / 179,203 |
  | 7 | (64,803) / 0 / (204,120) | (64,803) / (280,000) / 0 / (280,000) / (204,120) |
  | 5 (n1 net line only) | (10,687) / (28,197) / 14,453 | (7,044) / (2,563) / 3,643 / 25,634 / 14,453 |

- Totals are unchanged. C2/C3 stay without item differences; I recomputed them.
- Correct `builder-report-1` §3-A, which wrongly says "Kept 5 – gross אשראי lines, current: 1905, 2386, 2449", in the next
  builder report.

**M2 – 2386: `קבלת אשראי והלוואות מגופים פיננסיים` / `פירעון …` mapped to item 5. This violates D2.** (batch 7 B2)

*Where and why*
- Lines n5 and n6: Q1 p29 lines 5–6 and Q2 p32 lines 5–6. The Q2 receipt line itself cites "(ראה ביאור 4א(1))".
- Note 4א(1) (Q1 p35): 43,424 received in January 2026 from a financial body for the Nes Ziona land. It is repayable at
  completion, no later than 30.6.2030, and is presented as non-current.
- The balance sheet is mixed:
  - Q1 p26: current 56,850, non-current 48,490;
  - Q2 p29: current 60,711, non-current 49,318.

*Fix*
- n5 → **4** and n6 → **7** in both overrides, with evidence notes (D2).
- Expected vectors (same column order as M1):

  | Item | Q1 | Q2 |
  |---|---|---|
  | 4 | 50,574 / 4,817 / 12,959 | 55,704 / 6,986 / 5,130 / 2,169 / 12,959 |
  | 7 | (8,539) / (4,163) / (27,033) | (8,539) / (16,969) / 0 / (12,806) / (27,033) |
  | 5 (interest-party and partner net lines) | (220) / 112 / (496) | 264 / (1,332) / 484 / (1,444) / (496) |

- I recomputed C2: no new item difference.
- Correct builder report §3-A.

**M3 – 2418 Q1+Q2: the (\*) interest section says "הסעיף לא צוין", but the report states it.** This violates conventions §1
and R5. (batch 2 I1)

*Where and why*
- The text layer, verified by me, reads: "כמו כן, החברה מסווגת ריבית ששולמה בדוח על תזרימי המזומנים כחלק מהפעילות השוטפת".
  It appears in:
  - Q1 p51 (ביאור 5) and p13;
  - Q2 p52 (ביאור 1ג) and p14.
- The wrong text appears in:
  - `2418 - פירוט תזרים מימון 2026.xlsx` `פירוט מימון`!K37;
  - `מיפוי שורות`!F14 (Q1, p47) and F27 (Q2, p51);
  - the general notes B42 and B45;
  - the screenshot captions on pages 4/6/9/11;
  - master `נתונים` (8 rows) and `מיפוי שורות` (8 rows).

*Fix*
- Set `outside_sections` for both (\*) lines to `גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת`.
- Quote the source sentence and pages in `info_note_extra`.
- Adjust B42 and B45.
- Rebuild the workbook, the screenshots and the master.
- Move 2418 from "not stated" to "appendix/operating" in the builder report §3-E. Values are unchanged.

**M4 – 2396 Q1: the total-line text is not verbatim.** This violates AC5. (batch 8 B1)
- **Printed** (p35, verified by me on the text layer: `שנבעו`@x436 lies to the right of `ששימשו`@x393):
  `מזומנים נטו, שנבעו (ששימשו) מפעילות מימון`.
- **Recorded:** `מזומנים נטו, (ששימשו) שנבעו מפעילות מימון`, in `מיפוי שורות`!C14, `פירוט מימון`!K35 (Q1 part) and the master
  `מיפוי שורות` rows. This is the Q2 wording.
- **Fix:** in `overrides/2396_Q1.json`, set `line_text["10"]` to the printed text, or drop the key. Then re-finalize and rebuild
  2396 and the master.

**M5 – D3 not fully implemented: the line notes of the sign-flipped (\*) appendix lines do not say so.** (batch 4 M1, batch 2 O1)
- D3 requires the row note, the `מיפוי שורות` line note **and** `הסבר` to state the sign rule. The row notes and `הסבר` row 34
  do. The line notes say only `גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)`.
- The affected line notes:
  - 121: `מיפוי שורות`!F18 (Q1 p48 `ריבית ששולמה והוונה למלאי`) and F35 (Q2 p52 `ריבית ששולמה והוונה למלאי:`);
  - 1083: the `ב) ריבית ששולמה והוונה למלאי` line, Q1 p50 (row 16) and Q2 p51;
  - the corresponding master `מיפוי שורות` rows: 3 + 5 rows for each company.
- **Fix:** append to these line notes (generically, in the code that builds the (\*) mapping note, for every (\*) line whose
  sign was flipped), for example:
  `; מודפס ללא סוגריים (חיובי) ונרשם כאן בסימן תשלום (שלילי) כדי ששורת (*) הריבית תציג את סך הריבית ששולמה מחוץ לפעילות המימון (ראו 'הסבר' – (*) סימן)`.

**M6 – D1 not fully implemented in 2559 Q2.**
- D1 requires the line note to state the reasoning in Hebrew. The note on `מיפוי שורות`!F22 (`תשלום לבעל עניין בגין התאמת
  תמורה`, −52,500) argues only "עסקה הונית … הסעיף הקרוב … 1".
- The general note `פירוט מימון`!B47 still says "– החלטת מיפוי לתיאום בין החברות", as if the decision were open.
- **Fix:**
  - Rewrite the line note with D1's reasoning: a price adjustment paid to an IPO investor (הפניקס) for its participation in the
    share issuance, charged to equity. It economically reduces the net proceeds of the June-2026 share issuance, like the
    issuance costs that R3 nets into item 1. It is not business-combination contingent consideration, so it is not `אחר`.
  - Say that this is a judgment call that could be presented under `אחר`.
  - Replace B47 with the final decision.
  - Keep item 1 and the values. Rebuild 2559 and the master.

**M7 – 2389 Q2: the column notes deny a footnote that is printed.** This is wrong text. (batch 8 M1)
- `פירוט מימון`!G39 (6M-2025) and I39 (3M-2025, אפריל–יוני) say the (\*) marks have "ללא הערת שוליים בעמודי הדוח על תזרימי
  המזומנים".
- p52, at y≈736, prints `(*) סווג מחדש, ראו ביאור 2ג'` (verified by me).
- **Fix:** correct both notes to cite the p52 footnote. Keep `מוצג מחדש = לא`; the marks are on operating/appendix values only
  (§10).

**M8 – "38ד" page labels that are not separate (38D) data.** This is wrong text in `מקורות` col I and master
`אינדקס קבצים` col K. (batch 2 I3, batch 3 M1, batch 4 M2, plus my scan)

| Issuer, report | Wrong page in "38ד – עמ' …" | What the page actually is |
|---|---|---|
| 1039 Q1 | p12 | board report §6 |
| 400 Q1 | p16 | board report §3 נזילות |
| 400 Q2 | p19 | board report |
| 1622 Q1 | p11 | board report, 10(ב)(14) disclosure |
| 1622 Q2 | p13 | board report, 10(ב)(14) disclosure |
| 2418 Q1 | p51 | ביאור 5 of the consolidated statements |
| 2474 Q2 | p10 | board report §8, 10(ב)(14) |
| 1680 Q2 | p55 | `באור 6` of the consolidated interim statements |

- **Fix:** list only real 38D pages, or describe the other pages correctly (for example `עמ' 12 – דוח הדירקטוריון`).
- Re-check every `38ד – עמ'` list (267 page claims): each listed page must be the separate financial information.

**M9 – 2392: context captions say `פעילות השקעה`, but the pages show only the non-cash appendix.** This is wrong text. (batch 2 I2)
- Screenshots pages 4 and 7, their TOC entries and the cover entries "דוח Q1/Q2 2026 – עמוד PDF 50/51 – פעילות השקעה".
- Q1 p50 and Q2 p51 hold only `נספח - פעילויות השקעה ומימון שאינן כרוכות בתזרימי מזומנים` plus a footnote. The investing
  section is on p49 (Q1) and p50 (Q2).
- **Fix:** `context_sections` for these pages.

**M10 – 1484: the statement is called "מאוחד", but the company has no consolidated statements.** This is wrong text; see R1.2.
(batch 6 O1)
- The source is `דוחות על תזרימי המזומנים`, and the general notes rows 42/45 correctly say the company has no subsidiaries. But
  the following still say `הדוח המאוחד על תזרימי המזומנים`:
  - screenshot captions and the cover;
  - the `מיפוי שורות` block headers;
  - the `מקורות` notes and master index notes;
  - the generic `סימון` line.
- **Fix:** say `הדוח על תזרימי המזומנים (החברה אינה מציגה דוחות מאוחדים)` wherever 1484's statement is described.

### 4.2 SHOULD FIX (10 groups)

**S1 – Process and obsolete remarks in user-facing notes.** Replace them with final reasoning.

Required (batch 3 M2, batch 5 M4, batch 8 M2, plus my scan):

| Workbook, cell | Remove |
|---|---|
| 2464 Q2 `מיפוי שורות`!F21 | "החלטת מיפוי לתיאום בשלב C (חלופה: סעיף 11 לרכיב שטר ההון)" |
| 2503 Q1 `מיפוי שורות`!F8 and Q2 F25 | "(הצעת המחלץ – סעיף 7 – נדחתה). החלטת מיפוי לתיאום בשלב C (חלופה: 'אחר')" |
| 2567 Q2 `מיפוי שורות`!F5 | "– ראו דוח האצווה" |
| 425 `פירוט מימון`!B42 and 2520 B45 | "שנבחרו בטעות בשלב מוקדם ותוקנו" |
| 2570 `פירוט מימון`!B43 | "(שלב A תיקן בחירה שגויה קודמת שלו)" |

- Keep the items: 2464 → 7, 2503 → 11, 2567 → 11. State the reasoning and the alternative as a judgment call.

Optional: in the same pass you may rephrase:
- the 91 cells in 35 workbooks that cite internal phases ("בשלב C שונתה…", "מוסכמות שלב B §n");
- the master `חסרים והערות` K91 and K150 ("מאז שלב C…").

They are not wrong, but they cite process documents.

**S2 – Rule-A / D2 evidence missing or phrased as "by wording".** D2 requires "a note citing the evidence".

Add the balance-sheet page and amounts, or "not attributable":
- **341** Q1 n4 / Q2 n5 `פרעון הלוואות בערבות מדינה`: there is no separate balance-sheet line (Q1 p36), so the line is not
  attributable → 7. (batch 5 M1)
- **1979** Q2 n5 `פירעון הלוואות מצדדים קשורים ומאחרים`: Q2 p52 shows current 1,202 and non-current 14,308. (batch 5 M2)
- **2418** Q2 n7 `קבלת הלוואה מזכויות שאינן מקנות שליטה` (266). (batch 2 O3)

Replace "סווגה לסעיף 4/7 לפי ניסוח השורה" with the rule-A wording plus the evidence, on both receipt and repayment lines:
- **486** Q1 n5–n6 and Q2 n6–n7: the Q1 balance sheet (p53) shows long-term 371,399 and short-term and current maturities
  345,107; cite the Q2 balance sheet as well. The repayment notes have no evidence at all.
- **1797** Q1 n6–n7 and Q2 n6–n7: p40 of each report, 200,050 / 133,910 (Q1) and 165,050 / 178,771 (Q2).
- **2360** Q1/Q2 n4–n5: the balance sheet (p39) shows current 755,648 and non-current 2,680,817. Cite the page and amounts of each
  report.

**2449** n1 `קבלת אשראי מתאגידים בנקאיים`: keep item 5, but lead the note with the R3 net-presentation ground: the receipt line
prints (548) in Q1-2025, so it is in effect a net line. "ברובו שוטף" is not a valid basis under D2.

**S3 – Undocumented differences in the (\*) info rows between the two reports.** These are recorded for 200, 400, 421, 434 FY
and 719, but not for:
- **341**, Q1-2026 interest: Q1 report p41 (922); Q2 p47 (4,374) − (3,069) = (1,305); difference 383 (batch 5 M3).
- **434**, Q1-2026: Q1 p55 74,802; Q2 p60 213,285 − 128,219 = 85,066; difference 10,264.
- **434**, Q1-2025: 67,935 against 179,042 − 107,136 = 71,906; difference 3,971.

Add a `לידיעה` column note in the workbook and a master `חסרים והערות` row, as was done for the others. (531's 1-unit difference
is already in its column note H39.)

**S4 – (\*) dividend note inconsistent.**
- 823, 1330, 1553, 2385 and 2522 pay dividends in financing (items 11/12), but their (\*) dividend row note is empty.
- The other 39 companies in the same situation carry `אין סכומים מחוץ לפעילות מימון (דיבידנד ששולם מוצג בדוח בפעילות
  מימון)`.
- Add it. (batch 6 O4, extended by my scan)

**S5 – 200:** add the general note on the repaired broken-font (`ð`→`נ`) text layer, as in 2486 Q1 and 2567. (batch 3 M4)

**S6 – 2503 Q1 p48:** the printed title is `דוחות מאוחדים על השינויים בהון`, although the page is the operating/investing page of
the CF statement. This was verified by me on the text layer.
- Add an `issues` / `report_notes` entry and a master `חסרים והערות` row, as for 1680 Q2 and 2522 Q1. (batch 8 M3)

**S7 – Screenshot polish.** Keep the amendment-2 settings: same DPI and format, no compression.

a. **Zooms without the blue/orange frames** when the header strip and section are contiguous. There are 25 zooms, against the
   cover legend and the other 137 zooms:
   - 155 Q1/Q2, 341 Q2, 373 Q1/Q2, 425 Q2, 715 Q1/Q2, 1039 Q2, 1338 Q1/Q2, 1622 Q1;
   - 1974 Q1/Q2, 1979 Q1/Q2, 2384 Q1/Q2, 2456 Q1/Q2, 2464 Q1, 2488 Q1/Q2, 2503 Q1/Q2.

   Draw the frames on the single crop too. (batch 1 S1, batch 3 M3, batch 7 O4, batch 8 O2)
b. **(\*) crops that slice neighbouring rows** above or below the red frame:
   - 486 p4/p8, 1532 p5, 1083 s04/s10, 1502 s04/s09, 1553 s04/s08;
   - 2371 p4/p7, 2385 p4/p9, 473 p4/p8, 1905 p7, 2429 p4/p8;
   - also 400 s07 (clipped total label).

   Snap the crop margins to row gaps. (batch 1 S2/S3, batch 4 C2/C3, batch 5 M5, batch 7 O5)
c. The (\*) crop caption always says `קו מקווקו = קטע שהושמט`. Print it only when a separator is drawn. (batch 1 S2)
d. 2360 zooms p3/p6: a sliver of the next heading `תזרימי מזומנים מפעילויות שוטפות` shows, and the blue frame on p2/p5 touches
   that heading. (batch 1 S4)
e. Full-page captions 1829 p5 and 2360 p2/p5 lack the "(\*) = 0 on this page" sentence. (batch 1 S5)
f. The zoom legend should say that a blank source cell = 0 where blanks occur: 486 Q2 FY bond line, 1969 FY bond line, 2360 Q2
   6M/3M-2025 bond line. (batch 1 S6)
g. The 2520 context captions (Q1 p4, Q2 p7) say `(פעילות שוטפת)`. Name `נספח א'` (operating adjustments) precisely. (batch 5 M5)

**S8 – 473 and 2429 cross-reference.**
- The same flow `קבלת הלוואה מהמיעוט` (Q1 1,676 / 31,746 / 111,453) is item 4 in 473 (gross line, rule A) and item 5 in 2429
  (the net Q2 line, R3, aligned to Q1).
- Add one sentence to both line notes explaining the difference. (batch 7 O1)

**S9 – `validate.py`.**
- (a) Make `master_checks` key-based on (issuer, report, period label).
- (b) With `--issuers`, filter the master rows to those issuers, or require/auto-apply `--no-master`, so that subset runs give
  no false FAILs.
- (c) Compare all `נתונים` fields with the data: both (\*) amounts and notes, check, file, pages, months, end, currency, units,
  restated flag, notes and screenshot path.
- (d) Compare `מיפוי שורות` row by row by key, not only by count.
- (e) Print the unexplained-mismatch count on the console summary.

After the change, the full run must still give FAIL 0.

**S10 – Judgment calls for the user.** In the next builder report, add a short list of the judgment calls the user should be told
about, each with its alternative:
- D1 2559, item 1 (alternative `אחר`);
- 2464 Q2 combined loan + capital-note repayment, item 7 (alternative 11 for the capital-note component, 1,000 of 1,310);
- 2503 loan to the controlling owner charged to equity, item 11 (alternative `אחר`);
- 2567 interest on equity capital notes, item 11 (alternative 13);
- 715 combined LT-liability/bond repayment, item 7 (alternative 8);
- 155 put-option exercise, item 14;
- D3 (\*) sign for 121/1083.

### 4.3 Cross-company consistency review (AC5) – evidence for M1, M2 and S2

I grouped 1,453 unique report lines (`מיפוי שורות`) by normalised text: 12 identical-text groups have differing items. I also
grouped them into 12 keyword families (lease, interest, dividends, bonds, options, shares, NCI, short-term credit, long-term
loans, other loans, capital notes, `אחר`). 301 non-obvious lines were reviewed with their notes. Results:

- **Violations:** 1905 n2/n3 and 2386 n5/n6 (M1/M2). They are the only gross lines with mixed current/non-current balances
  still in item 5.
- **Item 5 with a mixed balance sheet, reviewed and acceptable under D2 / R3:**
  - 2449: effectively net; see S2.
  - 673 Q2 n5: at 30.6.2026 the loans are current only, and the example loan is due 15.2.2027; the non-current balances of
    347/485 in 2025 are immaterial.
  - 2474: the Q2 line is net, and the balance sheet is current only.
  - 1829 Q1 n5: the Q2 line is net, aligned under conventions §8.
  - 2559 n4: in effect net, and net in Q2.
  - 2386 n9/n11: net.
- **Same text, different items, explained by evidence:**
  - `פירעון הלוואות מאחרים`: 111/584/673 → 5 (current) against 434/2441/2570 → 7.
  - `קבלת/פירעון הלוואות מצדדים קשורים`: 2456/2570/2574 → 5 (current or net) against 2464/2503/2481 → 4/7 (non-current).
  - `קבלת הלוואות מתאגידים בנקאיים`: 673 → 5 (due 31.12.2026) against 444/1797/2360/2464/2522 → 4.
  - `פירעון הלוואות מתאגידים בנקאיים ואחרים`: 1829/2474 → 5 (net-line alignment) against 486/1502/1797/2389/2488 → 7.
  - `מימוש אופציה`: 155 → 14 (put option over NCI) against 1829 → 2.
  - `הנפקת מניות`: 539 → 2 (the equity statement shows only option exercises) against the others → 1.
  - `קבלת הלוואה מהמיעוט`: 473/2429 (S8).
- **Equity-classified owner instruments:**
  - 1724 capital notes issued → 1;
  - 2567 interest on capital notes → 11;
  - 2503 owner loan charged to equity → 11;
  - 2464 unsplit capital-note + loan repayment → 7 (S10).

  These are consistent enough when documented as judgment calls.
- **`אחר` (8 lines):** derivatives (1068, 1622), contingent consideration (1680), loans granted to home buyers (1722),
  interested-party receivables (2524), merger flow (434), other liability (341). All follow conventions §7 with notes.
- **Other families:**
  - Lease → 10, except the separately presented lease interest in 2521 → 13.
  - Interest → 13, except 2567 (capital notes).
  - Bond issuance → 3, repayment → 8 (2396 own-bond buy-back → 8).
  - Shares + options unsplit → 1; packages with bonds → 3 (2389).
  - Treasury shares → 9; 473 warrant buy-back → 9.
  - All consistent.

### 4.4 NO ACTION (observations; documented or approved design)

- **N1:** The master (\*) note columns are empty when the amounts are presented only in financing. This is the approved pilot
  design: the pilot report says "master note empty, per R5". (batch 1 O4, batch 8 O1)
- **N2:** The check formulas have no cached values (openpyxl). Excel computes them on open, and I verified this in 14
  workbooks. Pilot design. (batch 1 O5)
- **N3:** Page numbers are stored as text in the source rows. Pilot design. (batch 6 O5)
- **N4:** Receipts and repayments of the same lenders land in different items by the rules: 1829 (4/5), 2481 (5/7), 584 (4/5).
  Documented. (batch 1 O2, batch 4 M3)
- **N5:** Documented judgment calls: 715 combined line → 7; 155 → 14; 121 subsidiary option exercise → 6; 1532 Q1 (\*) lease
  interest printed in the non-cash appendix; 584 (\*) amounts. (batch 2 O2, batch 1 O1, batch 8 O3)
- **N6:** Printed sign anomalies are kept in the line's item, consistently and documented: 1484 +23,659 and the lease +1,854 /
  +2,342; 1622 +1,500; 2429 +53; 2478 +186; 2520 +14,913; 1974 (46); 2559 (30,547); 2464 (573). (batch 6 O2)
- **N7:** 2384 Q1 3M-2025: 395,555 moved to the bond line under conventions §9, documented. (batch 7 O3)
- **N8:** The restated-flag policy is consistent with §10: header or financing values marked → flag; otherwise a column note.
  (batch 1 O3, batch 7 O2)
- **N9:** The (\*) line is not red-framed on the full pages of 111, 400 and 539; the captions point to the red crops.
  Edges of the blue frame: 1502 Q1, 1622 Q1, 2456 Q2. (batch 4 C1/C4, batch 5 M5)
- **N10:** 444 and 1724 (\*) use the conservative "הסעיף לא צוין", which convention 1 allows. (batch 6 O3)
- **N11:** The full `validate.py` and `checks.py` pass. The only gate defect is S9.

**Batch-issue cross-reference:**

| Batch | Issues → classification |
|---|---|
| 1 | S1→S7a, S2→S7b/c, S3→S7b, S4→S7d, S5→S7e, S6→S7f, O1–O5→N1/N2/N4/N5/N8 |
| 2 | I1→M3, I2→M9, I3→M8, O1→M5, O2→N5, O3→S2, O4→S9 |
| 3 | M1→M8, M2→S1/S10, M3→S7a, M4→S5 |
| 4 | M1→M5, M2→M8, M3→N4, C1→N9, C2/C3→S7b, C4→N9, T1→S9 |
| 5 | M1/M2→S2, M3→S3, M4→S1, M5→S7b/S7g/N9, M6→S9 |
| 6 | O1→M10, O2→N6, O3→N10, O4→S4, O5→N3 |
| 7 | B1→M1, B2→M2, D1→M6/S10, O1→S8, O2→N8, O3→N7, O4→S7a, O5→S7b |
| 8 | B1→M4, M1→M7, M2→S1, M3→S6, O1→N1, O2→S7a, O3→N5 |

---------------------------------------------------------------------------------------------------------------

## 5. What Must Be Fixed (iteration 2)

Fix **all M and S items**. Change data only through the override keys; do not hand-edit outputs. Do not change any verified
value except the item vectors of M1/M2. Keep T1/T2 and the pilot screenshot settings (amendment 2).

1. **M1 1905 and M2 2386:** apply D2 in `line_items` for both reports, with evidence notes. Expect exactly the item vectors given
   in M1/M2.
2. **M3 2418:** `outside_sections` → `גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת`, quoting Q1 p51/p13 and Q2
   p52/p14. Update B42 and B45.
3. **M4 2396 Q1:** set `line_text["10"]` to `מזומנים נטו, שנבעו (ששימשו) מפעילות מימון`.
4. **M5 D3:** add the sign remark to the `מיפוי שורות` line notes of every sign-flipped (\*) line (121 Q1/Q2, 1083 Q1/Q2),
   generically in the build code. They then flow to the master.
5. **M6 D1 2559:** rewrite line note F22 with D1's reasoning and the judgment-call remark. Replace B47.
6. **M7 2389 Q2:** correct the G39 and I39 notes; the p52 footnote `(*) סווג מחדש, ראו ביאור 2ג'` exists.
7. **M8:** fix the "38ד" page lists (8 known pages in the table above) and verify all `38ד – עמ'` claims.
8. **M9 2392:** fix the `context_sections` of Q1 p50 and Q2 p51 (non-cash appendix), which also fixes the captions, TOC and
   cover.
9. **M10 1484:** stop calling its statement "מאוחד" in captions, cover, mapping block headers, source notes and the `סימון` line.
10. **S1–S10** as specified in §4.2.
11. **Rebuild and verify:**
    - re-finalize the changed reports and rebuild the affected companies (at least those in M1–M10 and S1–S8, and the S7a
      companies) and the master;
    - run `checks.py` and the full `validate.py` from outside WORKSPACE: expect `unexplained mismatches: 0`, FAIL 0;
    - the Excel COM check on copies;
    - `tool_integrity.py`: CLEAN;
    - delete `%TEMP%\fcf_run`.
12. **Write `builder-report-2.md`:**
    - correct §3-A (1905/2386) and §3-E (2418);
    - list every changed line and note, with before → after;
    - add the S10 judgment-call list for the user.

Assisted-by: Anthropic:Claude Opus 5.5
