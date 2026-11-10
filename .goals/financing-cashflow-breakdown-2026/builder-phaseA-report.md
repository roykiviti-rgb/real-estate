# Builder report — Phase A (iteration 1): pipeline ready for all 86 companies / 162 reports

Goal: `goal.md` + `goal-amendment-1.md` (A1 pilot = reference, T1, T2) + `goal-amendment-2.md` (T3 cancelled).
Phase A = make the pilot pipeline complete, generic and parallel-safe, run the automated pass on everything, triage.
**Only 1618 is verified** (pilot); the other 160 reports are automatic drafts waiting for Phase B.

Key files (all in `GOAL DIR\work\`): `PIPELINE.md` (Phase B protocol), `triage.csv` (one row per report),
`triage_notes.json` (Phase A findings per report, merged into `triage.csv`), `batches.json` (suggested split),
`roles.json` (role of every PDF), `phaseA-progress.md` (checkpoint log).

---------------------------------------------------------------------------------------------------------------

## 1. What changed

### Amendments
* **T1** – `build_master.py`: column `תקופה עיקרית` (כן/לא) in `נתונים` right after the period-end date. A period =
  months + end date per company; when it appears in several reports only the row from the latest report (Q2) is
  `כן`. Result on the draft master: 572 `כן` / 76 `לא` (exactly the FY-2025 column of the 76 Q1 reports whose company
  also has a Q2 report). Explained in `הסבר`; checked by `validate.py` (each company × period exactly once among `כן`).
* **T2** – `fcf_lib.period_label(..., quarter_range)` + `is_quarter_column`: a 3-month column that is not the
  year-to-date period gets ` (אפריל–יוני)`; ` (מוצג מחדש)` follows it. Applied by `finalize_report.py`, so it flows
  into the company workbook headers, both mapping sheets, master `נתונים` / `מיפוי שורות`, check labels and captions.
* **T3 cancelled** – the screenshot code is unchanged from the pilot (150/120/220 DPI, JPEG q88, same pages, boxes,
  captions); 1618's rebuilt PDF has the same 9 pages and image sizes as the pilot.

### Parallel safety
* `fcf_lib`: `TEMP_BASE = %TEMP%\fcf_run` (was `fcf_pilot`), `temp_dir(issuer, ...)`, `run_dir(tag)` = per-invocation
  `_runs\<tag>_<time>_<pid>`, `temp_path(name, issuer)` (pid-unique), JSON written via pid-unique temp + rename.
* Per-company commands write only per-company/per-report files; `checks.py` and `validate.py` take `--issuers`
  and write to per-invocation folders; per-company check explanations `overrides\<issuer>_checks.json`
  (1618's migrated; global `check_explanations.json` reserved for Phase C).
* `tool_batch.py` (parallel subprocess runner: extract / finalize / build / review) now **requires** `--issuers` or
  `--all`; `tool_triage.py --issuers` writes to TEMP, never a partial `triage.csv`.

### Roles (`roles.json`, built by `tool_roles.py`)
All 178 PDFs with role, used flag, note and evidence; `extract_report.py`, `build_company.py` (`מקורות`),
`build_master.py` (`אינדקס קבצים`, source decisions in `חסרים והערות`) and `validate.py` read it. Details in §2.

### Extraction (`fcf_extract.py` engine + `extract_report.py` CLI, rewritten)
Generic, coordinate-based, for every layout met in the 162 reports (162/162 extracted, no hard failure):
* statement detection: blocks of cash-flow pages scored by structure (operating/investing/financing headings and
  totals, closing cash), `מאוחד` title, "integral part" footer, formal title, company-name tokens; board-report pages,
  TOC, notes pages excluded; **separate-company (38D) pages recognised by the title `נתונים על תזרימי המזומנים` and by
  page phrases (`הדוחות הכספיים הנפרדים`, `המידע הכספי הנפרד` …)**; a `מאוחד`-titled block beats untitled ones;
  investee statements lose on the name score (e.g. 719 Q2 HADAR S.A.R.L.). Picks that are not the first strong block
  or lack `מאוחד` are flagged;
* multi-page statements (42 reports span 3–4 pages), header page ≠ financing page, 3 or 5 columns, column spans from
  the page with most columns, note-reference / line-number columns removed;
* column headers parsed on compacted text (letter-spaced `2 0 2 6`, `ל ש נ ה`, `1-6/2026`, English months); missing
  parts inferred from the pair partner (no duplicate periods) and flagged `לאמת`;
* values: parentheses (also mirrored `)1,234(`), footnote stars, trailing minus, numbers split into spans, dashes;
  hyphens/commas that touch label words stay in the label; day numbers next to month words are not values;
  irregular digit grouping flagged (`280,68` in 531 Q2 – the source misses a digit);
* labels: wrapped labels (before / after / centred amounts), mirrored parentheses repaired
  (`חוב)בניכוי הוצאות הנפקה(` → `חוב (בניכוי הוצאות הנפקה)`), the broken-font `נ` (`ð`, `ª`, U+F8FF) repaired;
* units incl. `מליוני ש"ח`, `באלפי דולר ארה"ב`, `אלפי אירו`, `באלפי דולר קנדי`, English unit phrases;
* item suggestions (R3 + pilot conventions; `אחר` only when nothing fits: 28 lines left), sign anomalies flagged;
* (*) lines outside financing: interest/dividends paid in operating/investing (also under `מזומנים ששולמו … עבור:`
  headings, nearest heading decides paid vs received), capitalised interest; receipts and declared/unpaid items
  excluded; interest/dividends disclosed **only in an appendix** of the statement offered as flagged candidates.

### Final data, overrides, rendering
* `finalize_report.py` (rewritten): **auto mode** (auto data + override keys: columns, units, line items/notes/text/
  values/pages/bbox, drop/add lines, (*) lines replace/drop/add, pages, boxes, notes, issues, text layer, verified) and
  **manual mode** (`"manual": true` – columns, lines, (*) lines, boxes all from the override, for unusable text layers).
  Explicit errors on missing values, wrong value counts, ≠ 1 total, missing months/end, unknown items.
* Geometry: `auto_geometry` reproduces the pilot's boxes exactly; manual `boxes` (PDF points: `fin`, `header`,
  optional `content` x-range, `printed_page`) override them and are the exact inverse. `tool_selftest.py <iss> <Q>`
  (isolated in TEMP) builds a fully manual copy of a report from its auto data and exercises every auto-mode
  correction key: items, totals, column labels, geometry and rendered outputs match (16–17 assertions; PASS on
  1484 Q1, 2384 Q2 and 1618 Q2). `fcf_render.py` draws page highlights, zoom crops and (*) crops from this geometry
  ((*) crops always cover the whole (*) line).
* `build_company.py --draft` (outputs marked `טיוטה` when a report is unverified), roles in `מקורות`.
* `checks.py` (C1, C2 + C2 per item as INFO, C3; explanations per company; report-specific C1 keys).
* `build_master.py` (T1, legend, source decisions, issues, `--draft`), `validate.py` (`--issuers`, `--no-master`,
  `--out`, T1/T2/roles/verification checks, scoped integrity).
* Review helpers: `tool_review.py` (≥ 220-DPI header strip + financing section with numbered line frames, UTF-8 line
  table with the override keys, (*) crops, statement pages), `tool_grid.py` (labelled coordinate grid for boxes),
  `tool_scan.py` (statement detection per page), `tool_shots.py`, `tool_clip.py` (time-stamped names – the view
  tool caches by path); `tool_triage.py`, `tool_batches.py`, `tool_inventory.py`, `tool_roles.py`.

---------------------------------------------------------------------------------------------------------------

## 2. Roles of the 178 PDFs

| role | files |
|---|---|
| `מקור הנתונים – דוח רבעוני` (data source) | 162 (159 main files + 1829 Q1-01, 1829 Q2-01, 2559 Q1-01) |
| `נספח – שומה/הערכת שווי` | 10: 539 Q2, 771 Q2, 823 Q2, 1331 Q2, 1490 Q2, 1703 Q2, 2384 Q2, 2385 Q2, 2464 Q1, 2557 Q2 (all `-01`; each opened and identified: real-estate appraisals, BDO valuations, a PPA) |
| `מכתב נלווה/תמצית` | 3: 1829 Q1 and Q2 main files, 2559 Q1 main file |
| `נספח – דוחות כספיים של חברה מוחזקת` | 2: 2520 Q1-01, 2520 Q2-01 |
| `גרסה חלופית – לא בשימוש` | 1: 2559 Q1-02 |

* **1829 (both quarters):** the main file is a one-page appraiser's cover letter; `-01` (84 / 90 pp) is the full
  quarterly report of אב-גד החזקות (board report, condensed consolidated statements, separate data) → `-01` is the
  data source; the consolidated cash-flow statement was confirmed visually (title `אב-גד החזקות בע"מ והחברות המאוחדות
  שלה – דוחות מאוחדים תמציתיים על תזרימי המזומנים`, columns ending 31.3.2026 / 30.6.2026).
* **2559 Q1:** the main file is a 3-page excerpt. `-01` (51 pp) and `-02` (54 pp) are the same "דוח מתקן" to the
  31.03.2026 statements: `-01` is the clean version; `-02` is the marked-up version (changes against the prospectus
  statements in red strike-through/insertions with margin bars, so its text layer contains doubled digits such as
  `7,985965`). **`-01` is the authoritative source** (clean, complete; cash-flow statement pp. 24–25). The financing
  sections (`-01` p. 25 vs `-02` p. 27) were rendered and compared line by line: **identical** in every line and
  amount – no issue to flag; the decision is recorded in `roles_2559.json` / `roles.json` and appears in the master.
* **2520 (both quarters):** `-01` = condensed consolidated statements of the investee סלע איסתא נדל"ן ישראלי – not
  used. The main file contains both the consolidated statement and the separate (38D) data; Phase A fixed the Q2
  pick (consolidated pp. 32–33, not the 38D pp. 55–56).
* Every main file was checked automatically for the company name and the period end on pp. 1–4; 25 used files did not
  contain the literal folder name/date there (English names, abbreviations, spaced or reversed text, image covers).
  All 25 were re-checked: alternative name tokens/dates on pp. 1–6, and for 200, 1096, 1829-01 and 2522 Q1 the
  statement pages were rendered and read (company and period confirmed).
* `..\_extra_attachments.csv` and `..\_missing_reports.csv` were used read-only as cross-references.

---------------------------------------------------------------------------------------------------------------

## 3. Text layers

No statement page is scanned or image-only; **all 162 reports have a usable text layer** (no OCR needed).

* **14 reports "usable (repaired)"**: a broken Hebrew font encodes `נ` as `ð` (U+00F0), `ª` (2567 Q2) or U+F8FF and
  stores those words' characters out of order → repaired in `fcf_lib.fix_glyph_text` + `visual_rtl_order`:
  200 Q1/Q2, 373 Q1/Q2, 584 Q2, 1083 Q2, 1928 Q1/Q2, 2441 Q1/Q2, 2486 Q1, 2488 Q1, 2559 Q1, 2567 Q2. Values are
  unaffected; Phase B must compare every label with the image.
* **The 7 reports where PyMuPDF found no "פעילות מימון"**:
  * 1083 Q1, 1083 Q2, 1331 Q2, 1644 Q1 – complete text layer, but `get_text()` returns the words of each line in
    reversed (visual) order (`מימון מפעילות מזומנים תזרימי`), so a literal phrase search fails; rebuilding lines from
    word coordinates gives `תזרימי מזומנים מפעילות מימון` (1644 Q1: `... לפעילות מימון`). 1083 Q2 also has the
    broken-`נ` font. Status: usable (1083 Q2: usable (repaired)).
  * 1905 Q1, 1905 Q2 – the statement has **no financing heading at all** (the section starts right after the investing
    total; in Q1 `מימון` occurs only in `הוצאות מימון נטו`). Usable; the section is taken from the investing total to
    the financing total (flagged).
  * 341 Q1 – the financing page (p. 42) does contain `תזרימי מזומנים מפעילות מימון` in logical order; usable (the
    discovery miss was a search artefact).
* Other text-layer quirks handled generically: numbers split into spans (`164` `,` `896`), mirrored parentheses,
  commas misplaced inside numbers (`1,3805`, flagged), label hyphens.

---------------------------------------------------------------------------------------------------------------

## 4. Automated pass and triage

* extract 162/162, finalize 162/162 (160 unverified + 1618 verified), draft company outputs 86/86, draft master
  (648 data rows = 76×3 + 81×5 + 5×3 columns, 6,158 mapping rows, 178 index rows). Runtime: ≈ 40 s for all
  extractions, ≈ 40 s for all builds (12 workers).
* **1618** re-finalized and rebuilt with T1/T2 from its verified pilot overrides: items, totals and checks identical
  to the pilot; Q2 3-month labels now `... (אפריל–יוני)`; no draft marker; `validate.py --issuers 1618 --no-master`
  → PASS 338 / FAIL 0.
* Sample screenshot pages viewed across layouts (1974, 373, 1622, 1484, 2384 incl. an appendix (*) crop); 1618's PDF
  compared with the pilot (same 9 pages, same image sizes): highlights, crops, captions and legibility as in the pilot.

### Triage (`work\triage.csv`, UTF-8 with BOM, 162 rows)

| difficulty | reports |
|---|---|
| **A** auto-clean (C1 = 0, labels/columns/units read, no flags, no `אחר`, usable text layer, no C2/C3 issue) | **46** |
| **B** targeted review (flags, `אחר` candidates, inferred columns, repaired text layer, (*) candidates, C2/C3 differences) | **112** |
| **C** heavy work | **4**: 531 Q2 (source prints `280,68`; C1 −252,615), 2418 Q1 (FY column misaligned by one row in the source + stray `-` row), 2533 Q1 and Q2 (headers print `30 במרס`; FY column sums differ from the printed total by 1,000 in both reports) |

Layouts and units: 76 Q1 reports with 3 columns, 81 Q2 reports with 5 columns, 5 Q2 reports with 3 columns (111, 584,
673, 1331, 1703 – no 3-month columns). Units: ש"ח/אלפים 148; **דולר ארה"ב/אלפים 8** (341, 1502, 1622, 2533); ש"ח/מיליונים
2 (1068); **אירו/אלפים 2** (1722); **דולר קנדי/אלפים 2** (2503). All statements are Hebrew RTL (the foreign issuers
1502, 1622, 1722, 2429, 2503, 2533 file Hebrew statements; English appendix pages exist but are not the source).
Lines: 1,291 financing lines (0–15 per report; 1502 Q1 has an empty financing section – confirmed visually);
28 lines still suggested `אחר`; 4 `net_loans`.

Most frequent flags: other statements in the file (133 reports – informational), pick not the first strong block (30 –
reviewed from the candidate lists: the earlier blocks are board-report tables, separate-company data or investees;
719 Q2 checked visually – Phase B confirms), negative value on a receipt line (29) / positive on a payment line (6),
empty cells set to 0 (20), `אחר` candidates (20 reports), (*) interest only in an appendix (19), inferred column
periods (11), units found on a page before the statement (5), `הוצג מחדש` on the pages (8: 421 Q1/Q2, 1905 Q2,
2449 Q1/Q2, 2478 Q2, 2559 Q1/Q2) – no column header itself says restated.

**(*) lines:** interest paid is presented in the financing section in 83 reports; interest paid outside financing was
found in the operating section of 55 reports and as an appendix-only disclosure in 19 reports (1331 Q2, 1532 Q2,
1561 Q1, 1724, 2384, 2418, 2522, 425, 434 Q2, 444 Q2, 486, 573); in 6 reports no interest-paid line was found anywhere
(default note `לא מוצג בנפרד בדוח תזרים המזומנים` – to confirm). Dividends paid outside financing: none found (a
declared-unpaid dividend in 573 Q1 and a received-interest line in 434 Q1 are correctly excluded).

**Unusual mappings expected (Phase B decides, consistently across batches):** partnership / owners' equity lines
(2503 `השקעות בעלים`/`חלוקות לבעלים`, 2533 `השקעות בעלים`/`חלוקות בעלים`, 341 `תקבולים מגיוס משקיעים`), NCI
abbreviations (`זשמ"ש` in 1039, 2524), EB-5 investor flows and advances from the parent (1622), derivatives
(1068, 1622), contingent consideration (1680), capital notes to controlling holders (1724), securities issue with
costs (421), merger flows (434), deal adjustments with an interested party (2559 Q2), urban-renewal partner receipts
(1561), `שינוי בבעלי עניין` (2524), treasury shares (9 – 400, 539, 823, 1330, 1331, 1484), `הנפקת חבילה` (539).

---------------------------------------------------------------------------------------------------------------

## 5. C1 / C2 / C3 on the automatic data (early signal only)

`checks.py` over all 162 reports (unverified data): **C1** 637 OK / 11 MISMATCH; **C2** 123 OK / 27 MISMATCH / 2 N/A;
**C2 per item** 83 INFO; **C3** 1,198 OK / 18 MISMATCH (all item-level; FY-2025 totals agree for all 76 companies).

* **C1 (11 columns):** 531 Q2 FY (source misses a digit, see C); 2533 Q1 and Q2 FY (−1,000, as printed in both);
  719 Q1 2025 (+8, printed total 7,903 vs lines 7,911 – checked on the image); 2483 Q2 3M-2026 (+5, checked on the
  image); ±1 source rounding: 715 (4 columns), 2417 Q1, 2478 Q2.
* **C2 (27):** 18 are ±1–2 rounding (434 ×2, 531, 539, 1490, 1724 ×2, 2360, 2386, 2396 ×2, 2417, 2474, 2483, 2488,
  2521, 2524, 2559). 9 are larger and were checked: values read correctly, the differences are in the reports
  themselves – 1484 (2026: 23 in bond repayment; 2025: 23,312, mostly short-term credit), 1979 (loans received 3,384
  and interest 1,488 in 2026; 3,732 in 2025), 2458 (191, interest), 2478 (14,540; the Q2 report shows `הוצג מחדש`),
  2486 (80 / 1,799), 2503 (1,793, interest). N/A: 2533 (the headers print `30 במרס`).
* **C3 (18 item rows):** the same FY-2025 line mapped differently in Q1 and Q2 or presented differently – 1722 (4/5),
  1829 (5/7), 2386 (5/7), 2474 (4/5), 2478 (4/5), 2559 (5/7, Q1 is the amended report), 531 (3, the missing digit),
  2418 (4/5/7/8/10, the Q1 misalignment). Phase B must align mappings or explain.
* All of these are listed per report in `triage.csv` (`c1_per_column`, `c2_auto`, `c3_auto`, `[שלב A]` notes).

`validate.py` (full, draft state): PASS 36,245 / FAIL 173 – all expected at this stage (160 missing verification
records, the C1 columns above, the C1–C3 summary, the stray empty-label row of 2418 Q1); AC12 passes (178 baseline
PDFs unchanged, exactly the 173 expected new files, no forbidden artefacts).

---------------------------------------------------------------------------------------------------------------

## 6. Known limitations

* Statement choice, column periods, section boundaries, (*) detection and item suggestions are heuristic; everything
  uncertain is flagged, but **every report still needs the visual check** (A only means "nothing suspicious found").
* Restated columns are detected from the column header only; 8 reports mention `הוצג מחדש` on their pages – decide.
* Interest paid disclosed only in an appendix: the extractor proposes the (*) row with the note `נספח לדוח תזרים
  המזומנים (מחוץ לפעילות מימון)`; Phase B confirms and may refine the note (e.g. `פעילות שוטפת – לפי הנספח`). This is a
  convention to keep consistent across batches.
* Labels of the 14 repaired reports and of wrapped lines must be compared with the image; numbers are reliable.
* No OCR is installed; manual mode is the fallback (tested end to end with `tool_selftest.py`, not yet needed for a
  real report).
* `validate.py` reads the workbooks with openpyxl; Excel-level checks (formula recalculation, rendering) remain
  available through `tool_excel_check.ps1` on copies in TEMP.
* The draft outputs in the company folders and the root master are drafts (`טיוטה`) and will be regenerated.

---------------------------------------------------------------------------------------------------------------

## 7. Suggested split into 8 batches (`work\batches.json`)

Whole companies; greedy balancing of workload = A 1 / B 2 / C 4 per report + lines/10 (1618 = 0, already verified).

| batch | reports | A/B/C | companies (issuer) |
|---|---|---|---|
| 1 | 19 | 5/12/2 | 486 וויי-בוקס · 1096 דניה סיבוס · 1338 אפריקה ישראל מגורים · 1490 ב.ס.ר · 1532 גפן · 1797 רותם שני · 1829 אב-גד (source `-01`) · 1969 אביב (Q2 only) · 2360 אקרו · 2533 אל עד יו אס (USD, C) |
| 2 | 20 | 6/13/1 | 121 קרדן ישראל · 155 מנרב · 715 אזורים · 1331 צילו-בלו (Q2 only) · 1644 אורון · 1722 חג'ג' אירופה (EUR) · 2392 רייק אספן · 2418 רם אדרת (C) · 2474 ליאם · 2521 קטה · 2557 תדהר (Q2 only) |
| 3 | 19 | 4/14/1 | 200 לוינסקי-עופר · 421 נתנאל · 531 בוני התיכון (C) · 1039 אלביט · 1068 שיכון ובינוי (מיליוני ש"ח) · 1974 סופרין · 2458 מגידו · 2486 מותג עירוני · 2487 א. פרשקובסקי גרופ · 2567 רם מוגרבי (Q2 only) |
| 4 | 21 | 7/14/0 | 111 י.ב התחדשות (Q2 only) · 400 דוניץ · 539 רוטשטיין נדל"ן · 1083 קרדן נדל"ן · 1502 מירלנד (USD) · 1553 אלמוגים · 1622 אקסטל (USD) · 2481 אלמוג · 2483 גבאי · 2488 אופק · 2524 אי.אס.איי |
| 5 | 21 | 7/14/0 | 341 שדה (USD) · 425 צרפתי · 1193 דמרי · 1703 יעקובי (Q2 only) · 1928 רימון · 1979 אפי קפיטל · 2371 בית וגג · 2385 עמרם אברהם · 2456 שמואל ברוך · 2478 רייסדור · 2520 איסתא |
| 6 | 20 | 4/16/0 | 373 אאורה · 434 ישראל קנדה · 444 מרדכי אביב · 673 ריי (Q2 only) · 823 חג'ג' · 1484 מצלאוי · 1561 הכשרת הישוב · 1724 רמות בעיר · 2417 אנשי העיר · 2441 שובל · 2574 עמים (Q2 only) |
| 7 | 22 | 8/14/0 | 473 עמוס לוזון · 1330 פרשקובסקי · **1618 אשטרום (verified – rebuild only)** · 1903 יובלים · 1905 גלעד מאי · 2384 קרסו · 2386 יסודות איתנים · 2429 לוזון רונסון · 2449 מיי טאון · 2522 עומר · 2559 בסט (source `-01`) |
| 8 | 20 | 5/15/0 | 573 לוינשטין · 584 ליבנטל (Q2 only) · 719 א. לוי · 771 גבאי מניבים · 1680 לסיכו · 2389 פרופדו · 2396 אשל הירדן · 2440 גשם · 2464 יוזמות · 2503 לנטרה קנדה (CAD) · 2570 לאונרדו (Q2 only) |

Total 86 companies / 162 reports; workload 50.1–52.3 per batch.

---------------------------------------------------------------------------------------------------------------

## 8. What the batch Builders must know

1. Follow `work\PIPELINE.md`; never edit scripts or shared files; only their own issuers' overrides, `_checks.json`,
   data (through the scripts) and outputs; report script problems as `SCRIPT-ISSUE`.
2. Always pass `--issuers` (tool_batch refuses otherwise); never run `build_master.py`.
3. Start from `triage.csv` and the `[שלב A]` notes; A reports also need the full visual check.
4. Override keys use the **auto** line numbers (`key` column of `lines_*.txt`).
5. Keep printed values; source errors are explained (C1/C2/C3 keys in `overrides\<iss>_checks.json`), not repaired –
   except an obvious missing digit (531 Q2), which needs a documented decision in `issues`.
6. Same line in Q1 and Q2 → same item (C3 per item). List cross-company judgement calls under "mapping decisions".
7. (*) rows: confirm candidates on the operating/investing pages and appendices; receipts and declared/unpaid items are
   not (*); every (*) line needs a bbox.
8. The `view` tool caches by path – use the time-stamped helper outputs.
9. Clean `%TEMP%\fcf_run\<iss>\` for their own issuers at the end.

For Phase C: run `checks.py`, `build_master.py` (without `--draft` once every report is verified), `validate.py`
(full), regenerate `triage.csv` if useful, add any global explanations to `work\check_explanations.json`, clean
`%TEMP%\fcf_run\`, and run `tool_integrity.py`.

---------------------------------------------------------------------------------------------------------------

## 9. Hygiene

All 178 source PDFs unchanged (validated against `baseline_files_sha256.csv`; `tool_integrity.py` → CLEAN); outside
`.goals` only the 86 × 2 draft company outputs and the draft master exist; no `__pycache__`, lock or temp files in
WORKSPACE; all renders, review files and run logs lived in `%TEMP%\fcf_run\` (≈ 73 MB) and were deleted at the end of
Phase A (the folder is recreated automatically by the scripts).

Assisted-by: Anthropic:Claude Opus 5.5
