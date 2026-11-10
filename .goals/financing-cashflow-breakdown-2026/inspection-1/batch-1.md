# Inspection 1, batch 1 (iteration 1): findings

Companies: 486 · 1096 · 1338 · 1490 · 1532 · 1797 · 1829 · 1969 (Q2 only) · 2360 · 2533. That is 19 reports and 77 period columns.

References: `goal.md`, `goal-amendment-1.md` (T1, T2), `goal-amendment-2.md` (T3 cancelled) and `work/phaseB-conventions.md`. I did not read the builder or batch reports.

## Verdict: **PASS**

- **Values.** All 77 columns are numerically correct. Every financing line, every value, every reported total and every (\*) value equals the source PDF. I confirmed each one on images I viewed myself.
- **Sources.** The sources, pages, periods, units and mapping are right.
- **Cross-report checks.** C2 and C3 hold, or their mismatches are explained in the master.
- **Master.** The master rows equal the company workbooks, including T1.

I found no blocking issue. The issue count is 0 blocking, 6 cosmetic screenshot issues (S1–S6) and 5 observations on documented judgment calls (O1–O5).

---------------------------------------------------------------------------------------------------------------

## 1. What I did and saw

1. **Sources (text layer, PyMuPDF).**
   - I scanned every page of all 22 PDFs in the 10 folders for cash-flow titles and financing headings.
   - For each report I located the consolidated statement independently and separated it from:
     - the separate (38ד) data: 486 p69–72 / p75–79, 1338 p72 / p74–75, 1490 p57–58 / p73–74, 1532 p50 / p54, 1797 p55–57 / p57–59, 1829 p76–77 / p78–79, 1969 p54–56, 2360 p59–61 / p67–69, 2533 p50 / p55;
     - investee statements: 1490 "ורטיקל סיטי" p68 / p85, 1969 "רוטשילד 22 מבנים" p65;
     - the board-report analyses.
   - I then dumped every word, with coordinates, of every cash-flow page of the 19 reports, plus the balance-sheet pages needed for the mapping evidence.
2. **Images I viewed myself: 24, all displayed.**
   - **Images 1–19:** one composite per report, rendered by my own script from the source PDF. The title, column-header and units strip is at 150 DPI and the full financing section, heading to total, is at 170 DPI. 486 Q1/Q2 and 1532 Q1/Q2 also include every (\*) appendix line with that page's header strip.
   - On these composites I compared every line text, every value in every column, the column headers and the units, one by one, with `פירוט מימון` and `מיפוי שורות`.
   - **Images 20–24:** screenshot pages 486 p2 (full page), 486 p3 (zoom), 486 p4 ((\*) crop), 1096 p3 (zoom) and 1338 p3 (zoom).
3. **Sub-agents (read-only, my own renders).**
   - **Screenshots PDFs: all 74 pages rendered at 110 DPI.**
     - Captions and TOC were read from the text layer.
     - Three reviewers viewed the image pages: 37, 25 and 26 images, all displayed. They checked caption, file, page, frames, header strip, units and legibility, and transcribed every zoom.
     - Every transcription they returned matches my verified values.
   - **(\*) lines: 38 source pages rendered at 130 DPI.** These are the operating and investing pages and appendices of every report. A reviewer listed every interest, dividend, distribution or withdrawal line outside financing with its section and values. The result matches my reading of the text layer.
4. **Automated checks (my scripts, read-only).** All pass:
   - every item = sum of its mapped lines, for all 77 columns;
   - C1 per column;
   - C2 (total and per item) and C3 (total and per item);
   - item labels and order, column labels (T2), months, end dates, restated flag;
   - numeric cells with format `#,##0;-#,##0;0`, check-row formulas, RTL on every sheet;
   - the `=` in column A of the total row is a string, not a formula: an `inlineStr` in the 486 sheet XML, and read back as the string "=" with `data_only` in all 10 workbooks;
   - master `נתונים`: 77 rows equal the workbooks field by field, including T1;
   - master `מיפוי שורות`: 653 rows equal the company mapping sheets, with net lines resolved to 4 or 7 by sign;
   - `אינדקס קבצים`: 22 rows;
   - `חסרים והערות`: every mismatch is present.
5. **Quality gate.** `validate.py --issuers <10 issuers> --no-master --out <my temp>` gives `PASS 3107  FAIL 0  INFO 2`. The two INFO lines are the explained 2533 C1.
   - Running it without `--no-master` on a subset reports AC11 and T1 failures. These are an artefact: `master_checks` pairs expected rows with master rows by position from row 2. My key-based comparison of the same rows is clean.
6. **Integrity and hygiene.**
   - The SHA-256 of all 22 source PDFs equals `baseline_files_sha256.csv`.
   - Each folder holds only its PDFs and the two outputs.
   - There is no `~$*` and no `__pycache__`.

---------------------------------------------------------------------------------------------------------------

## 2. Results per company and report

Checks: **Src** = source file and consolidated statement/pages. **Per** = columns, labels (T2), months, end dates, restated flag. **Val** = every line and value, total, check. **Map** = mapping. **(\*)** = info rows and notes. **Lay** = workbook layout, header block, `מקורות`, master rows. **Shots** = screenshots PDF.

| Co. | Rep. | Src | Per | Val | Map | (\*) | Lay | Shots |
|---|---|---|---|---|---|---|---|---|
| 486 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS (S2) |
| 486 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS (S2, S6) |
| 1096 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 1096 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 1338 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS (S1) |
| 1338 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS (S1) |
| 1490 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 1490 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 1532 | Q1 | PASS | PASS | PASS | PASS (O1) | PASS (O1) | PASS | PASS (S3) |
| 1532 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 1797 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 1797 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 1829 | Q1 | PASS | PASS | PASS | PASS (O2) | PASS | PASS | PASS |
| 1829 | Q2 | PASS | PASS | PASS | PASS (O2) | PASS | PASS | PASS (S5) |
| 1969 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS (S6) |
| 2360 | Q1 | PASS | PASS (O3) | PASS | PASS | PASS | PASS | PASS (S4, S5) |
| 2360 | Q2 | PASS | PASS (O3) | PASS | PASS | PASS | PASS | PASS (S4, S5, S6) |
| 2533 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 2533 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

### Details

- **486 וויי-בוקס**
  - **Q1** (`_Q1_1745702.pdf`)
    - Statement on PDF p58–59 (printed 9–10), title "דוח תמציתי מאוחד על תזרימי המזומנים". Financing is on p58; appendix A on p59.
    - Six lines and the total match. Total: 30,590 / (70,245) / 101,169.
    - (\*) interest from appendix A: 15,847 / 19,653 / 68,193, positive as printed. The section is not stated, so the note "הסעיף לא צוין" is correct (convention 1).
    - Rule-A note checked against the balance sheet on p53: short-term loans and current maturities 345,107; long-term loans 371,399.
  - **Q2** (`_Q2_1767297.pdf`)
    - Statement on p63–64. Seven lines and the total match. Total: 179,435 / (15,761) / 148,845 / 54,484 / 101,169.
    - The FY cell of "תמורה מהנפקת אגרות חוב, נטו מהוצאות הנפקה" is blank in the source; it is recorded as 0 and noted.
    - (\*) interest: 38,979 / 37,508 / 23,132 / 17,855 / 68,193.
  - **Cross-checks.** C2 and C3 equal for the total and every item, including (\*).
- **1096 דניה סיבוס**
  - **Q1:** p29–30, financing on p30. **Q2:** p30–31, financing on p31. Five lines and the total match in both.
  - Interest and dividends are presented in financing, so (\*) = 0. Operating has only "מסים ששולמו, נטו"; investing has only receipts.
  - "פרעון הלוואות לזמן ארוך והתחייבויות בגין חכירה" is mapped to 10. This is verified: the consolidated balance sheet (Q1 p24) has no long-term loans. Its non-current liabilities are deferred tax, a derivative of 239,857, the lease liability of 108,715 and employee benefits.
  - **Cross-checks.** C2 and C3 equal.
- **1338 אפריקה ישראל מגורים**
  - **Q1:** p57–58. **Q2:** p57–58. Q2 p58 is an untitled continuation page with its own period and units strip.
  - Eight lines and the total match in both. The total label "מזומנים נטו - פעילות מימון" includes the dash.
  - (\*) = 0, because interest and dividends are presented in financing.
  - **Cross-checks.** C2 and C3 equal.
- **1490 ב.ס.ר**
  - **Q1:** p36–38, financing on p37. The signs were confirmed on the image: 26,315 and 1,394 are positive; (43,356) and (4,456) are negative.
  - **Q2:** main file, p48–50, financing on p49. The `-01` file is an expert valuation of "ורטיקל סיטי" and is not used. All lines match.
  - **Cross-checks.**
    - C2 2025: 25,891 against 25,893, a source rounding difference of interest (1,248) vs (1,247) and lease (570) vs (569). Explained in `חסרים והערות`.
    - C2 2026: offsetting ±1 differences in items 10 and 13. Explained.
    - C3 equal.
- **1532 גפן מגורים**
  - **Q1:** p32–34. Four lines and the total match. Total: 28,969 / (27) / 7,094.
  - **Q1 (\*):** appendix B on p33 ("מפעילות שוטפת"): 1,748 / 1,751 / 3,603, plus lease interest 3 / – / 13. Appendix C on p34 (non-cash): lease interest – / 4 / –. See O1.
  - **Q2:** p36–38. Six lines and the total match. (\*) on p37: 2,377 / 1,751 / 629 / – / 3,603, plus 5 / 8 / 2 / 4 / 13.
  - Item 5 is supported by the balance sheet on p27: current liabilities "אשראי מתאגידים בנקאים ונותני אשראי אחרים" 22,035 / – / 7,200.
  - **Cross-checks.** C2 equal, including (\*): 1,751 = 2,382 − 631 and 1,755 = 1,759 − 4. C3 equal.
- **1797 רותם שני**
  - **Q1:** p44–45. **Q2:** p45–46. Nine lines and the total match in both.
  - The rule-A notes were checked on the balance sheet, p40 of each report: 200,050 / 133,910 in Q1 and 165,050 / 178,771 in Q2.
  - **Cross-checks.** C2 and C3 equal, including every item.
- **1829 אב-גד**
  - **Sources.** The data come from the `-01` files: Q1 has 84 pages with the statement on p64–65; Q2 has 90 pages with the statement on p65–66. The main PDFs are one-page appraiser letters (role "מכתב נלווה/תמצית").
  - Eight lines and the total match in both reports.
  - The receipts line is mapped to 4, with balance-sheet evidence from Q2 p60: current 165,796 and non-current 17,640. See O2 for the repayments line.
  - **Cross-checks.** C2 and C3 equal.
- **1969 אביב (Q2 only)**
  - Statement on p36–37. Five lines and the total match; the FY bond cell is blank and recorded as 0.
  - "דוח Q1 2026 אינו קיים בתיקייה" appears in the workbook and in the master.
  - C2 and C3 do not apply.
- **2360 אקרו**
  - **Q1:** p45–46. **Q2:** p49–50. Ten lines and the total match in both. The Q2 bond-issue cells for 6M-2025 and 3M-2025 are blank and recorded as 0.
  - Rule A is supported by the balance sheet on p39: current 755,648 and non-current 2,680,817.
  - **Cross-checks.** C2 2026 total 293,345 against 293,344, a 1 in interest (31,154) vs (31,155). Explained. C3 equal. See O3.
- **2533 אל עד יו אס** (units: באלפי דולר ארה"ב)
  - **Q1:** single page, p36. The header prints "30 במרס"; 31.03 is used, with column notes (convention 9). Listed in `חסרים והערות`.
  - **Q2:** single page, p38. The 3M-2026 bond line is (70); it stays in item 3, as issuance costs, with a note.
  - **C1.** FY 2025 is −1,000 in both reports. This is a source inconsistency: owners' investments print 65,529 against 66,529 in the statement of changes in equity. Explained in both workbooks and in the master.
  - **Mapping.** "השקעות בעלים" → 1 and "חלוקות בעלים" → 11 (convention 2). The loans line is net of transaction costs → 4 (rule B).
  - **Cross-checks.** C2 and C3 equal.

**Master workbook (my companies).**
- `נתונים` holds 77 rows, all equal to the workbooks.
- T1 is correct: the nine Q1 FY-2025 rows are `לא`; every other row, including all five 1969 rows, is `כן`. T1 is explained in `הסבר`, and every sheet is RTL.

---------------------------------------------------------------------------------------------------------------

## 3. Issues

### Cosmetic (screenshots; non-blocking; values and digits legible everywhere)

- **S1 – 1338 zoom pages p3 (Q1) and p6 (Q2).**
  - Both are plain crops: no blue header frame, no yellow/orange financing frame and no dashed line. The header and financing are contiguous on the page.
  - Every other zoom page has the frames.
  - The content is complete: periods, units and all lines through the total.
- **S2 – 486 (\*) crops p4 (Q1) and p8 (Q2).**
  - The crop slices through the "נספח א' – מידע נוסף…" heading above the red frame and through the next row's figures below it (217/425/1,093).
  - The caption says "קו מקווקו = קטע שהושמט", but no dashed line is drawn.
- **S3 – 1532 p5 ((\*) crop of p34).** Half-cut fragments of the rows above (1,980) and below ((18,380)) the red frame are visible.
- **S4 – 2360 zooms p3 and p6.**
  - The top half of the next heading, "תזרימי מזומנים מפעילויות שוטפות", shows as a sliver between the blue header strip and the dashed line.
  - On the full pages p2 and p5, the blue frame touches or overlaps that heading.
- **S5 – full-page captions.** 1829 p5 and 2360 p2/p5 lack the "(\*) = 0 on this page" sentence that the other full pages carry. Their context pages do carry it.
- **S6 – zoom captions.** The legend explains only "-" = 0. Blank source cells are not mentioned in the caption: 486 Q2 FY bond line, 1969 FY bond line, 2360 Q2 bond line 6M/3M-2025. They are documented in the workbook mapping notes.

### Observations (documented judgment calls; no change required)

- **O1 – 1532 Q1 (\*).** The Q1 3M-2025 value 4 ("ריבית ששולמה בגין חכירות") sits in appendix C, "פעולות מהותיות שאינן במזומן".
  - It is counted in the (\*) interest row with "הסעיף לא צוין". Convention 1 excludes non-cash items, but the line is a cash payment printed in the wrong appendix.
  - Q2's appendix B shows the same 4 (8 − 4), so 1,755 is consistent.
  - Documented in the note and in `חסרים והערות` ("חריגה בדוח המקור"). Acceptable.
- **O2 – 1829, lenders split between two items.** The receipts line "קבלת הלוואות מתאגידים בנקאיים ואחרים" goes to 4 by rule A (mixed balances). The repayments line goes to 5:
  - in Q1 it is labelled "פירעון…";
  - in Q2 it is the net line "קבלת (פירעון)…", so item 5 follows from R3's net-without-term rule and convention 8 (same line in both reports; FY (11,877) in both).
  - The rules are followed and documented, but receipts and repayments of the same lenders land in different items.
- **O3 – 2360 restatement.** The 2025 interim comparatives were restated retrospectively (note 2ב). The (\*) marks appear only in appendix A (operating), so the 2025 columns are not flagged `(מוצג מחדש)` and carry column notes instead.
  - This agrees with master `הסבר` R35 and convention 10.
  - Compare 111 in another batch, where marks on financing values led to the flag. This is consistent with the stated rule.
- **O4 – master (\*) note.** For companies whose interest and dividends appear only in financing, the master "(\*) – סיווג / הערה" cells are empty. The company workbooks carry "אין סכומים מחוץ לפעילות מימון (…)".
  - The amounts are identical (0), and R5 permits no note. Cosmetic.
- **O5 – check row.** The check-row and mapping-check formulas have no cached values: openpyxl writes them and Excel computes them on open (pilot design). My own computation gives 0 everywhere except the documented 2533 FY −1,000.

---------------------------------------------------------------------------------------------------------------

## 4. Fix list

None required for this batch. Optional: S1–S6 cosmetic polish of the screenshot crops and captions.
