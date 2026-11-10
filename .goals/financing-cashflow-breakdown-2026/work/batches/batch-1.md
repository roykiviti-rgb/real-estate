# Batch 1 report — Phase B, iteration 1

Builder: Phase B batch 1 (Claude Opus 5.5). Date: 2026-11-10.
Scope: 10 issuers / 19 reports: 486, 1096, 1338, 1490, 1532, 1797, 1829, 1969 (Q2 only), 2360, 2533.
Protocol: `work\PIPELINE.md` §0–§13 + `work\phaseB-conventions.md`; goal R1–R9 + amendments (T1, T2; T3 cancelled).
No git was used. No script or shared file was edited. Only my own `overrides\<iss>_*.json`, the data files (via `finalize_report.py`), and the company outputs (via `build_company.py`) were written.

## Summary

| issuer | reports | verified | C1 | C2 | C3 | built (no draft) | `validate.py --issuers <iss> --no-master` |
|---|---|---|---|---|---|---|---|
| 486 | Q1, Q2 | 2/2 | 8 OK | 2 OK | 16 OK | yes | PASS 323 / FAIL 0 |
| 1096 | Q1, Q2 | 2/2 | 8 OK | 2 OK | 16 OK | yes | PASS 320 / FAIL 0 |
| 1338 | Q1, Q2 | 2/2 | 8 OK | 2 OK | 16 OK | yes | PASS 326 / FAIL 0 |
| 1490 | Q1, Q2 | 2/2 | 8 OK | 1 OK + 1 explained (−2, rounding) | 16 OK | yes | PASS 328 / FAIL 0 |
| 1532 | Q1, Q2 | 2/2 | 8 OK | 2 OK | 16 OK | yes | PASS 322 / FAIL 0 |
| 1797 | Q1, Q2 | 2/2 | 8 OK | 2 OK | 16 OK | yes | PASS 328 / FAIL 0 |
| 1829 | Q1, Q2 (`-01` files) | 2/2 | 8 OK | 2 OK | 16 OK (5/7 aligned) | yes | PASS 328 / FAIL 0 |
| 1969 | Q2 only | 1/1 | 5 OK | n/a | n/a | yes | PASS 205 / FAIL 0 |
| 2360 | Q1, Q2 | 2/2 | 8 OK | 1 OK + 1 explained (+1, rounding) | 16 OK | yes | PASS 330 / FAIL 0 |
| 2533 | Q1, Q2 | 2/2 | 6 OK + 2 explained (FY −1,000, source) | 2 OK | 16 OK | yes | PASS 318 / **FAIL 2** = SCRIPT-ISSUE 1 |

Batch totals (`checks.py --issuers` on all 10): C1 75 OK + 2 MISMATCH (both explained); C2 16 OK + 2 MISMATCH (both explained); C2-item 5 INFO (all explained); C3 144 OK; **unexplained mismatches: 0**.
`tool_integrity.py` → **CLEAN** (178 baseline PDFs unchanged, no stray files).

**19 of 19 reports verified.**

## How the numbers were verified

1. **Data and review.** For every report I read the `tool_review.py` package:
   - `lines_*.txt`: extracted lines, values, items, (*) candidates, flags;
   - the 220-DPI `fin` image and the page renders.
   I searched the text layer with my own helper (`b1_find.py`, read-only) to locate pages and to read supporting pages for mapping decisions: balance sheet, notes, equity statement, board report.
2. **Image check (authoritative).** Every value was compared digit by digit on rendered images:
   - the pages of each company's final screenshots PDF, rendered by `tool_shots.py`;
   - the 220-DPI zoomed header strip + financing section;
   - the 150-DPI full pages with the orange/blue boxes;
   - the 120-DPI context pages: operating, investing and appendices;
   - every red (*) crop.

   This covered every line text, every value digit by digit, the column headers (periods and audit status), the units and currency, the mapping, and the presence or absence of (*) lines in the operating and investing sections and the appendices. For blank-cell questions (1969) I zoomed with `tool_grid.py --clip … --dpi 250`.
   - **Note on process:** during the first pass the image viewer stopped displaying images after its 50-image limit, though the tool reported each view as successful. When I noticed, I re-did the complete visual check on freshly rendered images. Where needed, I combined two pages into one image (side-by-side or stacked montages of the same renders) to stay within the limit.
   - Every report listed here was then checked on images that were actually displayed. The `verified.method` text of each override describes this check.
3. **Arithmetic.** C1 in every column; C2/C3 and C2 per item via `checks.py`; I re-added the 2533 FY column by hand.
4. **Outputs.**
   - `build_company.py` without `--draft` for all 10 companies.
   - Every screenshots PDF was rendered and inspected: captions, blue/orange boxes, red (*) crops, legible zoom.
   - The workbook of 2533 was dumped read-only with openpyxl: header block, column headers, check formulas, notes, mapping and sources sheets.
   - No Excel COM was used (conventions §11).

---------------------------------------------------------------------------------------------------------------

## 486 וויי-בוקס נדל"ן בע"מ

- **Sources:**
  - Q1 `486_..._2026_Q1_1745702.pdf` (78 pp): consolidated statement pp. 58–59, financing p. 58, appendix A (additional information) p. 59.
  - Q2 `486_..._2026_Q2_1767297.pdf` (83 pp): pp. 63–64, financing p. 63, appendix A p. 64.
  - Not used:
    - pp. 20–22 are the board report's forecast cash-flow (warning-signs disclosure);
    - Q1 pp. 69–70 / Q2 pp. 75–76 are the separate (38D) data.
- **Columns:** Q1 3M-31.03.2026, 3M-31.03.2025, FY-2025. Q2 6M/6M/3M (אפריל–יוני)/3M (אפריל–יוני) to 30.06.2026/2025, FY-2025. Units `אלפי ש"ח`.
- **Lines:** Q1 has 6 lines + total; Q2 has 7 lines + total. Cells printed `-,-` are recorded as 0, and the blank FY cell of the Q2 bond line as 0.
- **Mapping:**
  - Convertible bonds → 3; bonds → 3; option exercise → 2; lease principal → 10; bond repayment → 8.
  - `קבלת/פירעון הלוואות מתאגידים בנקאיים ואחרים` (gross lines with no stated term) → **4 / 7**, with a note. The balance sheet shows both long-term loans and short-term loans/current maturities, and the line is not split (see *Mapping decisions* 1).
- **(*):** interest paid appears **only in appendix A** ("מידע נוסף על תזרימי המזומנים"):
  - It is printed **positive**: Q1 15,847 / 19,653 / 68,193; Q2 38,979 / 37,508 / 23,132 / 17,855 / 68,193.
  - The section in which it is included is not stated.
  - Recorded as printed in the (*) interest row. Note per conventions §1: `גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)`.
  - No dividends were paid.
- **Overrides:**
  - `line_notes`;
  - `outside` (the appendix line, re-stated with an explicit section text and the original bbox);
  - `info_notes`;
  - `context_sections` for the appendix page (caption);
  - `report_notes`, `text_layer`, `verified`.
- **Checks:** C1 0 in all 8 columns; C2 2 OK (every line and the (*) interest also reconcile); C3 16 OK.
- **Source issues:** none.

## 1096 דניה סיבוס בע"מ

- **Sources:**
  - Q1 `..._1742403.pdf` (38 pp): consolidated pp. 29–30, financing p. 30.
  - Q2 `..._1762282.pdf` (41 pp): pp. 30–31, financing p. 31.
  - Title: `תמצית דוחות על תזרימי המזומנים ביניים מאוחדים`.
- **Columns:** standard 3 / 5. Units `אלפי ש"ח`.
- **Lines:** 5 lines + total in each report.
- **Mapping:**
  - `פרעון הלוואות לזמן ארוך והתחייבויות בגין חכירה` → **10**. The consolidated balance sheet (all 3 dates of each report) has no long-term loans, only a lease liability. Note added (*Mapping decisions* 4).
  - `שינוי באשראי מתאגידים בנקאיים ונותני אשראי אחרים לזמן קצר, נטו` → 5.
  - Dividend → 11; share issue → 1; interest → 13.
- **(*):** interest and dividends are paid in financing only. Operating has taxes paid and a non-cash finance-income adjustment; investing has only dividends and interest received. Info rows = 0.
- **Overrides:** `line_notes`, `report_notes`, Q2 `columns.header_text` (full header text), `text_layer`, `verified`.
- **Checks:** C1 8 OK; C2 2 OK (every line); C3 16 OK.
- **Source issues:** none.

## 1338 אפריקה ישראל מגורים בע"מ

- **Sources:**
  - Q1 `..._1742497.pdf` (79 pp): pp. 57–58, financing p. 58.
  - Q2 `..._1763151.pdf` (81 pp): pp. 57–58, financing p. 58.
  - Not used:
    - pp. 39–42 (Q1) / 35–39 (Q2) are the board report's cash-flow review;
    - p. 72 (Q1) / pp. 74–75 (Q2) are the separate data (`tool_scan` candidates checked).
- **Columns:**
  - Q1 c1 printed only `2026` under the shared heading `לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס`. Confirmed on the image; `columns.c1` set explicitly, plus a column note.
  - Units `אלפי ש"ח`.
- **Lines:** 8 lines + total.
- **Mapping:** all 1:1 — 3, 8, 5 (ST bank credit, net), 4, 11, 12 (NCI dividend), 7, 13.
- **(*):** in financing only; operating has taxes, investing has interest received. Info rows = 0.
- **Overrides:** `columns.c1`, `column_notes`, `report_notes`, `text_layer`, `verified`.
- **Checks:** C1 8 OK; C2 2 OK (every line); C3 16 OK.
- **Observation:** in this company the header strip and the financing section are contiguous, so `fcf_render` draws the zoom as one crop without the blue/orange frames. This is the pilot design, not a defect; the full page carries the boxes.

## 1490 ב.ס.ר הנדסה ופיתוח בע"מ

- **Sources:**
  - Q1 `..._1741954.pdf` (72 pp): pp. 36–38, financing p. 37.
  - Q2 `..._1764944.pdf` (89 pp): pp. 48–50, financing p. 49.
  - p. 38 / p. 50 is the first-consolidation appendix (not a cash flow).
  - Not used:
    - pp. 15–16 / 18–19 are the board report's liquidity analysis;
    - pp. 57–58 / 73–74 are the separate data;
    - pp. 67–68 / 84–85 are the investee ורטיקל סיטי בע"מ's statements.
  - Q2 `-01` = appraisal ("ורטיקל סיטי"); `roles.json` is correct, not a source.
- **Columns:** standard. Units `אלפי ש"ח`.
- **Lines:** Q1 7 lines; Q2 8 lines (incl. `פרעון אגרות חוב להמרה`, all dashes).
- **Mapping:**
  - `קבלת (פרעון) אשראי לזמן קצר מתאגידים בנקאיים, (אחרים וצדדים קשורים), נטו` → 5.
  - `קבלת (פרעון) הלוואות לזמן ארוך …, נטו` → `net_loans` (4 if ≥ 0, 7 if < 0, per column; FY-2025 −4,456 → 7).
  - Bonds → 3 / 8; dividend → 11; share issue → 1; interest → 13; leases (no split) → 10.
- **(*):** in financing only; operating has taxes and dividends received, investing has interest received. Info rows = 0.
- **Overrides:** `line_notes`, `column_notes` (Q1, C2 rounding), Q1 c1 `header_text`, `report_notes`, `text_layer`, `verified`; `1490_checks.json`.
- **Checks:** C1 8 OK. C2 2026 OK. C2 2025 total: Q1 25,891 vs Q2-derived 25,893 (−2) = **source rounding**:
  - interest (1,248) vs (1,247);
  - leases (570) vs (569).

  4 C2-item INFO (±1 in items 10/13, both years) explained. C3 16 OK.
- **Source issues:** ±1 rounding of the derived quarters between the reports (explained).

## 1532 גפן מגורים והתחדשות בע"מ

- **Sources:**
  - Q1 `..._1742408.pdf` (65 pp): pp. 32–34, financing p. 32; appendices A–B p. 33, appendix C p. 34.
  - Q2 `..._1763377.pdf` (69 pp): pp. 36–38, financing p. 36; appendices A–B p. 37, appendix C p. 38.
  - Not used: pp. 50–51 / 54–55 (separate data).
- **Columns:**
  - The Q1 headers print `לתקופה שהסתיימה יום 31 במרץ 2026/2025` without the number of months. The auditor's review report (p. 25) states "שלושה חודשים", so they are recorded as 3M, with column notes.
  - Q2 standard. Units `אלפי ש"ח`.
- **Lines:** Q1 4 lines; Q2 6 lines.
- **Mapping:**
  - `קבלת/פירעון אשראי מנותני אשראי אחרים` and `קבלת אשראי מתאגיד בנקאי` (gross) → **5**. On the balance sheet, `אשראי מתאגידים בנקאיים ונותני אשראי אחרים` is a current liability, and the 5,200 non-bank loan was repaid (*Mapping decisions* 3).
  - The Q1 20,000 receipt from "other lenders" is shown in Q2 as "from a bank"; both → 5, so C2 is exact.
  - `הנפקת מניות ואופציות לצד קשור / למנכ"ל החברה / למשקיע` → **1** (the extractor suggested 2). These are private placements of shares + options not split in the statement (conventions §6; *Mapping decisions* 5).
  - Leases → 10 (lease interest is disclosed separately in appendix B).
- **(*):** interest paid is disclosed **only in appendix B** ("מידע נוסף בגין תזרימי המזומנים מפעילות שוטפת"), printed positive:
  - `ריבית ששולמה`: Q1 1,748 / 1,751 / 3,603; Q2 2,377 / 1,751 / 629 / – / 3,603.
  - `ריבית ששולמה בגין חכירות`: Q1 3 / – / 13; Q2 5 / 8 / 2 / 4 / 13.
  - Q1 also prints `ריבית ששולמה בגין חכירות` 4 for 1/2025 in **appendix C** (non-cash activities).
  - All are recorded in the (*) interest row as printed. Note `גילוי בנספח … – נכלל בפעילות שוטפת (נספח ב')`, plus an `issues` entry for the appendix-C anomaly.
  - The Q2 lease-interest line was missed by the extractor; I added it with its bbox (SCRIPT-ISSUE 2).
  - `boxes.header` was set on the appendix pages so the red crops show the appendices' own column headers.
  - No dividends were paid.
- **Overrides:**
  - Q1 `columns` c1/c2 (months, end, header text) and c3 header text; `column_notes`;
  - `line_items`, `line_notes`;
  - `outside` (full list), `info_notes`;
  - `context_sections`, `boxes`;
  - `report_notes`, `issues`, `text_layer`, `verified`.
- **Checks:** C1 8 OK; C2 2 OK (every item, and also the (*) interest incl. the appendix-C 4); C3 16 OK.
- **Source issues:**
  - The 1/2025 lease interest is printed in the non-cash appendix C (Q1).
  - The statement references `נספח ד'` (first consolidation), which does not exist in either report; no effect on financing.

## 1797 רותם שני יזמות והשקעות בע"מ

- **Sources:**
  - Q1 `..._1742449.pdf` (62 pp): pp. 44–45, financing p. 45.
  - Q2 `..._1764008.pdf` (64 pp): pp. 45–46, financing p. 46.
  - Not used: pp. 55–56 / 57–58 (separate data).
- **Columns:** standard. Units `אלפי ש"ח`.
- **Lines:** 9 lines + total.
- **Mapping:**
  - `קבלת הלוואות מתאגידים בנקאיים (ואחרים)` → **4**, `פירעון הלוואות מתאגידים בנקאיים ואחרים` → **7**. These are gross lines with no stated term. The balance sheet has both LT loans from banks and others and current bank credit, and the line is not split (*Mapping decisions* 1).
  - Option exercise → 2; treasury shares → 9; leases (no split) → 10; bonds → 3 / 8; dividend → 11; interest → 13.
- **(*):** in financing only; operating shows only taxes paid, investing shows interest received from deposits. Info rows = 0.
- **Overrides:** `line_notes`, `report_notes`, `text_layer`, `verified`.
- **Checks:** C1 8 OK; C2 2 OK (every line); C3 16 OK.
- **Source issues:** none.

## 1829 אב-גד החזקות בע"מ

- **Sources (R1 exception):**
  - The main files are one-page appraiser letters (role `מכתב נלווה/תמצית`, correct in `roles.json`).
  - The data source is `-01` in both quarters:
    - Q1 `1829_..._1745375-01.pdf` (84 pp): pp. 64–65, financing p. 64, appendix A p. 65;
    - Q2 `1829_..._1767116-01.pdf` (90 pp): pp. 65–66, financing p. 65, appendix A p. 66.
  - Title: `אב-גד החזקות בע"מ והחברות המאוחדות שלה – דוחות מאוחדים תמציתיים על תזרימי המזומנים`.
  - Not used: pp. 76–77 / 78–79 (separate data).
- **Columns:** Q2 c1/c3 headers set explicitly (the extractor had inferred them; confirmed on the image). Units `אלפי ש"ח`.
- **Lines:** 8 lines + total.
- **Mapping — C3 5/7 aligned:**
  - Q1 prints `פירעון הלוואות מתאגידים בנקאיים ואחרים`. Q2 prints the same line as `קבלת (פירעון) הלוואות מתאגידים בנקאיים ואחרים`, a **net** line with no stated term, positive (+6,682) in Apr–Jun 2026.
  - Per R3, this line → **5** in both reports. On the balance sheet the bank credit is mostly current (project-finance credit). The FY-2025 (11,877) is now item 5 in both reports, so C3 is 16/16 OK.
  - C2 per line is exact: Q1 3M-2026 (8,525) = Q2 (1,843) − 6,682.
  - `קבלת הלוואות מתאגידים בנקאיים ואחרים` (gross) → 4.
  - `מימוש אופציה` → 2: the company's own options, per the equity statement (3,721 to share capital/premium).
  - `השקעת המיעוט בישות מאוחדת` and `הקצאת מניות בחברת בת` → 6 (the equity statement credits a reserve for transactions with NCI).
  - Bonds → 3 / 8; interest → 13.
- **(*):** in financing only; operating and appendix A show only income tax paid; no dividends. Info rows = 0.
- **Overrides:** `line_items` (5 → 5), `line_notes`, Q2 `columns` c1/c3, `context_sections` (Q2 p. 66), `report_notes`, `text_layer`, `verified`.
- **Checks:** C1 8 OK; C2 2 OK (every line); C3 16 OK.
- **Source issues:** none (the 5/7 difference was an extraction-mapping difference, now aligned).

## 1969 קבוצת אביב ושות' נדל"ן 1963 בע"מ (Q2 only)

- **Source:** Q2 `..._1767211.pdf` (68 pp): pp. 36–37, financing p. 37.
  - Not used:
    - p. 13 is the board report;
    - pp. 54–56 are the separate data;
    - p. 65 is the investee רוטשילד 22 מבנים בע"מ.
  - No Q1 report in the folder; the workbook states `דוח Q1 2026 אינו קיים בתיקייה`.
- **Columns:** standard 5. Units `אלפי ש"ח`.
- **Lines:** 5 lines + total.
- **Mapping:** ST credit from banks and others, net → 5; LT loans → 4 / 7; bond proceeds → 3 (FY cell blank in the source → 0, zoomed); interest → 13.
- **(*):** in financing only; operating shows taxes paid, investing shows interest and dividends received. Info rows = 0.
- **Overrides:** `columns.header_text`, `line_notes`, `report_notes`, `text_layer`, `verified`.
- **Checks:** C1 5 OK; C2/C3 n/a (no Q1).

## 2360 קבוצת אקרו בע"מ

- **Sources:**
  - Q1 `..._1742743.pdf` (68 pp): pp. 45–46, financing p. 45, appendix A p. 46.
  - Q2 `..._1764403.pdf` (77 pp): pp. 49–50, financing p. 49, appendix A p. 50.
  - Not used:
    - pp. 16–18 / 19 are the board report;
    - pp. 59–61 / 67–69 are the separate data.
- **Columns:** headers cleaned (`columns.header_text`; Q1 c2 was flagged ambiguous, then confirmed on the image). Units `אלפי ש"ח`.
- **Lines:** 10 lines + total.
- **Mapping:**
  - `תמורה מהנפקת מניות ואופציות` → **1**. It is a share + option package; the equity statement shows `הנפקת מניות ואופציות` 99,356. The extractor suggested 2 (*Mapping decisions* 5).
  - `השקעות המיעוט בישויות מאוחדות` → 6; `משיכות המיעוט` → 12.
  - `קבלת/פירעון הלוואות מתאגידים בנקאיים` (gross, no term; the balance sheet has bank credit in both current and non-current) → 4 / 7.
  - Lease principal → 10; bonds → 3 / 8; dividend → 11; interest → 13.
- **(*):** in financing only. `דיבידנד שהוכרז` (4,000, in the non-cash information) is not a payment. Info rows = 0.
- **Restatement:**
  - Note 2ב is a retrospective policy change (staff position on urban renewal) for the 2025 comparatives.
  - In the statement only appendix-A (operating) cells carry `(*)`; financing is not marked and the column headers do not say restated.
  - Per conventions §10 these columns are **not** flagged `(מוצג מחדש)`; column notes were added instead.
- **Overrides:** `columns.header_text`, `column_notes`, `line_items` (1 → 1), `line_notes`, `context_sections`, `report_notes`, `text_layer`, `verified`; `2360_checks.json`.
- **Checks:** C1 8 OK. C2 2025 OK. C2 2026 total: Q1 293,345 vs Q2-derived 293,344 (+1) = **source rounding** in interest paid ((31,154) vs (31,155)); explained, plus a C2-item INFO entry. C3 16 OK.

## 2533 אל עד יו אס קפיטל הולדינגס לימיטד (USD, difficulty C)

- **Sources:**
  - Q1 `..._1742828.pdf` (51 pp): single-page consolidated statement p. 36.
  - Q2 `..._1766889.pdf` (56 pp): p. 38.
  - Not used: board report pp. 9–10 / 11–12; separate data p. 50 / 55.
- **Units:** `באלפי דולר ארה"ב` → currency `דולר ארה"ב`, units `אלפים`.
- **Column dates (conventions §9):**
  - The Q1 column headers print `לשלושה חודשים שהסתיימו ביום 30 במרס` (2026 and 2025).
  - Everything else in the report says 31 March: the cover (`31 במרץ 2026`), the balance sheet, the P&L, the equity statement (`יתרה ליום 31 במרס 2026/2025`), and note 1א (`ליום 31 במרס, 2026 ולתקופה של שלושה חודשים`).
  - So the period end is recorded as **31.03.2026 / 31.03.2025**. Column notes quote the printed header, plus an `issues` entry.
  - C2 therefore runs and is OK in both years, line by line.
- **Lines:** 6 lines + total.
- **Mapping (conventions §2):**
  - The company (BVI, set up 12/2025) is 100% owned by El-Ad Ventures; the statements use pooling of interests.
  - `השקעות בעלים` → **1** and `חלוקות בעלים` → **11**. Owner flows of the reporting entity: the equity statement credits them to share capital/premium and retained earnings attributable to the owners, not to NCI.
  - Loans from financial institutions, net of transaction costs → 4; their repayment → 7.
  - Bonds → 3. The Apr–Jun 2026 bond amount (70) is additional issue costs (6M 76,869 = Q1 76,939 − 70); it stays in item 3 (*Mapping decisions* 8).
  - Interest → 13.
- **(*):** in financing only; operating shows only a non-cash finance-expense adjustment, investing has no interest or dividend line. Info rows = 0.
- **C1 (source defect, conventions §9):**
  - In the FY-2025 column of **both** reports the printed lines sum to −268,919, but the printed total is −267,919 (−1,000).
  - The equity statement shows `השקעות בעלים` for 2025 = **66,529**, against 65,529 printed in the cash-flow line: exactly 1,000.
  - The printed total matches the change in cash (306,836 − 44,808 − 267,919 = −5,891).
  - Printed values kept; explained in `2533_checks.json` (`C1|2533|Q1 2026|…` and `C1|2533|Q2 2026|…`), column notes and `issues`.
- **Overrides:** Q1 `columns` c1/c2 (end 31.03, header text); `column_notes`; `line_notes`; `report_notes`; `issues`; `text_layer`; `verified`; `2533_checks.json`.
- **Checks:** C1 6 OK + 2 MISMATCH (explained); C2 2 OK; C3 16 OK; `checks.py` unexplained 0.
- **validate:** PASS 318 / FAIL 2. The 2 FAILs are `AC6 C1 דוח Q1/Q2 2026 | שנה שהסתיימה ב-31.12.2025`, i.e. exactly the explained source defect → SCRIPT-ISSUE 1.

---------------------------------------------------------------------------------------------------------------

## Mapping decisions (cross-company judgement calls for Phase C to align)

1. **Gross loan lines with no stated term** (`קבלת הלוואות מתאגידים בנקאיים (ואחרים)`, `פירעון הלוואות …`):
   - Mapped to **4 / 7** by wording ("הלוואות", gross receipt/repayment), with a note, even where the balance sheet holds both LT loans and current bank credit (1797, 486, 2360, 1829 receipts).
   - The alternative reading (credit that is partly short-term → 5) was rejected because the lines are presented gross and not as "אשראי".
   - Please align with the other batches.
2. **Net borrowing line without a stated term** (1829 Q2 `קבלת (פירעון) הלוואות מתאגידים בנקאיים ואחרים`) → **5** (R3).
   - The same line in the Q1 report is labelled `פירעון …`. It was mapped to 5 as well, so that C3 compares like with like.
3. **Gross short-term credit lines** (`קבלת/פירעון אשראי מנותני אשראי אחרים`, `קבלת אשראי מתאגיד בנקאי`, 1532) → **5**. On the balance sheet this credit is a current liability.
4. **`פרעון הלוואות לזמן ארוך והתחייבויות בגין חכירה`** (one mixed line, 1096) → **10**, because the balance sheet has no long-term loans at all. If a company has both, the line would need a different decision.
5. **Unsplit share + option packages** (`הנפקת מניות ואופציות …`, 1532 ×3 lines, 2360) → **1** (conventions §6). **The extractor suggests item 2 for these lines**, so other batches should check theirs.
6. **Owners of the reporting entity** (2533 `השקעות בעלים` / `חלוקות בעלים`) → **1 / 11** (conventions §2).
7. **Subsidiary equity flows:**
   - `השקעת/השקעות המיעוט`, `הקצאת מניות בחברת בת` → 6;
   - `משיכות המיעוט` → 12;
   - `מימוש אופציה` of the company itself → 2 (checked on the equity statement).
8. **A negative amount on a bond-issue line** (issue costs in a later quarter, 2533 Q2 (70)) → stays in **3** (costs netted in the receipt item), not 8.
9. **(*) interest disclosed only in an appendix:**
   - Recorded **as printed (positive)** in the (*) row, per R5 "sign as printed".
   - 486: the section is not stated → `… – הסעיף לא צוין (לא בפעילות מימון)`.
   - 1532: the appendix is titled "מידע נוסף בגין תזרימי המזומנים מפעילות שוטפת" → `… – נכלל בפעילות שוטפת`.
   - Lease interest disclosed in the same appendix is included in the (*) interest row.
   - Phase C may want one sign convention for appendix amounts across batches (they are printed positive here, whereas operating-section lines are printed negative).
10. **A (*) amount printed in a non-cash appendix** (1532 Q1: lease interest 4 in appendix C) is included as printed, with an `issues` note. The Q2 report shows the same amount in the operating appendix B.
11. **A header date typo** (2533 `30 במרס`) → 31.03, with column notes (conventions §9).
12. **Retrospective policy change affecting only operating cells** (2360 note 2ב) → column notes, not `(מוצג מחדש)` (conventions §10).
13. **Header without the number of months** (1532 Q1 `לתקופה שהסתיימה יום 31 במרץ`) → 3M, per the auditor's review report, with a column note.

## SCRIPT-ISSUEs

```
SCRIPT-ISSUE 1
  script:     validate.py (company_checks, line 90: ok(abs(sum(items)+other-total) < 1e-6, "AC6 C1 <column>"))
  report:     2533 Q1 and Q2 (FY-2025 column); the same applies to every explained C1 column of other batches
              (Phase A listed 719 Q1, 2483 Q2, 715, 2417 Q1, 2478 Q2)
  symptom:    validate.py --issuers 2533 --no-master → PASS 318 / FAIL 2:
              "FAIL: [2533] AC6 C1 דוח Q1 2026 | שנה שהסתיימה ב-31.12.2025" and the same for Q2.
              The per-column AC6 check requires C1 = 0 and ignores the explanations in overrides/<iss>_checks.json,
              although the global AC6/AC8 check (line 253) accepts them (checks.py: unexplained mismatches 0).
              Evidence: %TEMP%\fcf_run\_runs\validate_20261110-112712_23664\validate.txt
  expected:   AC6 allows a non-zero C1 "only when the source statement itself does not add up, and then it is documented"
              (goal AC6; conventions §9 explicitly lists 2533 FY: keep printed values, explain C1) → an explained C1
              column should PASS (or be reported as INFO).
  workaround: none possible without a plug value (forbidden by R3); printed values kept and explained in
              2533_checks.json, column notes and issues. Company outputs are built (no draft).
  severity:   blocks "validate FAIL 0" for 2533 (and the other source-defect columns) – needs a Phase C fix of validate.py
```

```
SCRIPT-ISSUE 2
  script:     fcf_extract.py (outside (*) detection)
  report:     1532 Q2
  symptom:    in appendix B p. 37 the extractor found 'ריבית ששולמה' but not the next line 'ריבית ששולמה בגין חכירות'
              (5 / 8 / 2 / 4 / 13), which it did find in the Q1 report (p. 33).
  expected:   both interest-paid lines of the appendix are (*) candidates.
  workaround: override "outside" with both lines (bbox read from the text layer, checked on the image); C2 of the (*) row
              now reconciles with Q1.
  severity:   cosmetic (worked around)
```

```
SCRIPT-ISSUE 3
  script:     fcf_render.py (context-page captions) / fcf_extract.py (context_sections)
  report:     1829 Q2 p. 66, 2360 Q1 p. 46 / Q2 p. 50, 486 p. 59 / p. 64, 1532 pp. 33–34 / 37–38
  symptom:    statement pages that carry only an appendix to the operating section ("נספח א' – התאמות …", "מידע נוסף …")
              get the caption "המשך הדוח" / generic text instead of naming the appendix.
  expected:   the caption names the appendix (relevant because it proves the (*) rows).
  workaround: "context_sections" set in the overrides (caption text only).
  severity:   cosmetic
```

Other observations, not script issues:
- **Item suggestion 2 for unsplit share-and-option packages:** the extractor suggests item 2 (option exercise) for `הנפקת מניות ואופציות` lines; conventions §6 says 1. It is only a suggestion, but other batches should check their lines.
- **Default (*) appendix note:** the extractor's default text for appendix-only (*) lines is `נספח לדוח תזרים המזומנים (מחוץ לפעילות מימון)`, while conventions §1 prescribes different wording. I used `info_notes`.
- **Zoom crops without frames:** when the header strip and the financing section are contiguous (1338), the zoom crop has no blue/orange frames. This is the pilot design.

## Temp hygiene

- My helper scripts and scratch outputs (`b1_*.py`, `find_*`, `keys_*`, `final_dump_*`, `xlsx_*`, `mont_*`, `roles_*` files) lived only in `%TEMP%\fcf_run\<iss>\`.
- These folders are deleted at the end for all 10 issuers; `_runs` is left for Phase C.
- `tool_integrity.py` → CLEAN.

## Final status

| issuer | status |
|---|---|
| 486 וויי-בוקס נדל"ן | verified (Q1, Q2) + built; validate FAIL 0 |
| 1096 דניה סיבוס | verified (Q1, Q2) + built; validate FAIL 0 |
| 1338 אפריקה ישראל מגורים | verified (Q1, Q2) + built; validate FAIL 0 |
| 1490 ב.ס.ר הנדסה ופיתוח | verified (Q1, Q2) + built; validate FAIL 0 |
| 1532 גפן מגורים והתחדשות | verified (Q1, Q2) + built; validate FAIL 0 |
| 1797 רותם שני | verified (Q1, Q2) + built; validate FAIL 0 |
| 1829 אב-גד החזקות (source `-01`) | verified (Q1, Q2) + built; validate FAIL 0 |
| 1969 קבוצת אביב (Q2 only) | verified (Q2) + built; validate FAIL 0 |
| 2360 קבוצת אקרו | verified (Q1, Q2) + built; validate FAIL 0 |
| 2533 אל עד יו אס (USD) | verified (Q1, Q2) + built; validate FAIL 2 = SCRIPT-ISSUE 1 (explained source defect: FY-2025 printed total vs lines −1,000; no plug possible) |

Assisted-by: Anthropic:Claude Opus 5.5
