# Inspection 1, batch 5: independent verification

Inspector: batch 5 of 8, iteration 1. Date: 2026-11-10.

Companies: 341, 425, 1193, 1703 (Q2 only), 1928, 1979, 2371, 2385, 2456, 2478, 2520. That is 11 companies, 21 reports, 83 period columns.

References:
- `goal.md`
- `goal-amendment-1.md` (T1 and T2 apply)
- `goal-amendment-2.md` (T3 is cancelled)
- `work/phaseB-conventions.md` and PIPELINE §7, including the Phase C rules A and B

I formed every finding below myself. I did not read the builder or batch reports.

## Verdict: **PASS**

- **Blocking issues:** 0.
- **Minor observations:** 6 (M1–M6, below). None of them affects a number, a column or an item assignment.

---

## 1. How I verified (what I saw and how)

### 1.1 Source location

- **Own scan of every PDF.** I scanned all 25 PDFs in the 11 company folders myself with PyMuPDF and located each report's consolidated cash-flow statement.
- **Statement boundaries.** I checked that the page before each statement is the statement of changes in equity and the page after it is note 1. So no page of the statement is missing.
- **Statements I excluded.** I identified the separate (38D) statements and the board-report liquidity tables, and did not use them.
- **The `-01` files.** I read the first pages of each:
  - 1703 Q2 `-01`: BDO valuation of YSB's holding in BlueGen.
  - 2385 Q2 `-01`: BDO purchase-price allocation for עמרם את נידם.
  - 2520 Q1 and Q2 `-01`: statements of the investee סלע איסתא נדל"ן ישראלי.
  - None of them is a source. This matches R1.

### 1.2 Independent extraction

- **My own parser.** I wrote my own parser (`rows.py` / `compare.py`) over the PyMuPDF word layer:
  - It groups words into rows and merges split tokens such as `4,` + `909`.
  - Parentheses mean a negative value; `-` means 0.
  - It assigns columns by the x-position of the total row.
- **What it extracted.** For each of the 21 reports: every financing line × every column, the reported total, and every interest-paid or dividend-paid line outside financing.
- **Comparison with the workbook.** I compared this programmatically with each company workbook:
  - the `מיפוי שורות` sheet: line count, order, page and value per column;
  - in `פירוט מימון`: item value = sum of the mapped lines, the total, both (*) rows, and C1.
- **Result.** All 21 reports are identical to my extraction. The only C1 difference is 2478 Q2, April–June 2026: −1, a source rounding (see §3).

### 1.3 Visual confirmation of every value

**11 composites.** I rendered 11 per-company composite PNGs (one per company) from the source PDFs at 150 DPI and viewed each one; every image displayed. Each composite holds:
- the page title, the column headers and the units line;
- the whole financing section;
- every (*) row with its columns.

**Values read on the images.** On these images I read every value of every line × column, every header year and period, and every units line, and compared them with the workbook:
- 341 Q1 and Q2
- 425 Q1 and Q2
- 1193 Q1 and Q2
- 1703 Q2
- 1928 Q1 and Q2
- 1979 Q1 and Q2
- 2371 Q1 and Q2
- 2385 Q1 and Q2
- 2456 Q1 and Q2
- 2478 Q1 and Q2
- 2520 Q1 and Q2

**One extra crop (130–200 DPI).** It covers two points:
- the year and units rows of 425 Q2 page 85 (the column order 2026 | 2025 | 2026 | 2025 | 2025);
- the verbatim lease-line wording of 1928, which differs between the reports and is correctly kept: Q1 has `פירעון קרן התחייבות בגין חכירה`, Q2 has `פירעון קרן בגין התחייבות בגין חכירה`.

**Images in my own context.** I used 14 images in total, and every one displayed:
- the 11 composites and the extra crop;
- the screenshot pages 1193 p3 and 425 p4.

### 1.4 Screenshots PDFs

**Structure, checked by script:**
- table of contents, page list, captions (text layer);
- embedded image sizes;
- the renderer constants: full page 150 DPI, context 120 DPI, zoom 220 DPI, inserted without resampling. This meets the R7 minimums of 110 and 200 DPI.

**Visual review.** I rendered all 80 non-cover pages at 100 DPI. Two read-only sub-agents read them visually:
- One saw 39 images and the other 41. Each confirmed that every image displayed.
- They compared the pages against an expected-content list I derived from my own extraction: file, pages, line counts, totals and (*) values.
- They read every zoom total and every (*) value digit by digit, and all matched.

**My own spot-checks:**
- the 1193 Q1 zoom: header strip with `אלפי ש"ח` and all three periods, a dashed separator, all 7 lines and the total, no column cut off;
- the 425 Q1 (*) crop: header strip with periods and units, then the red frame on `ריבית ששולמה` 5,296 | 4,354 | 41,717.

### 1.5 Master workbook (`סיכום פירוט תזרים מימון 2026 - כל החברות.xlsx`)

- **`נתונים`:** 83 rows for my issuers, equal to the 83 company columns. For each row, these are identical to the company workbook:
  - items 1–14, `אחר`, the total, both (*) amounts;
  - months, end date, file, page and restated flag.
- **T1:** `לא` only on the Q1-report FY-2025 rows; `כן` everywhere else; 1703 is `כן` on all three rows. Correct.
- **Check column:** 0 everywhere except 2478 Q2, April–June 2026: −1, which is documented.
- **`מיפוי שורות`:** 798 rows, equal to the 798 company line × period entries. There are 0 differences in text, value, item and page.
- **`אינדקס קבצים`:** the 25 PDFs, each with the correct role and used flag.
- **`הסבר`:** explains T1 (row 39), T2 (row 40) and the restated rule.

### 1.6 Quality gate and hygiene

- **Quality gate.** `validate.py --issuers <11> --no-master` gives PASS 3391, FAIL 0, INFO 1 (the explained C1 of 2478) and exits 0. See M6 on the subset mode with the master checks.
- **Baseline hashes.** All 25 source PDFs of my companies are byte-identical to `baseline_files_sha256.csv`. Each folder has exactly the two new output files. There are no `~$*` files and no `__pycache__`.

---

## 2. Per company and report

**Legend:**
- **Src:** right file, consolidated statement, cited pages correct.
- **Per:** columns, labels including T2, months, end dates, restated flag.
- **Val:** every value against the image.
- **Map:** R3 and the conventions.
- **(\*):** info rows, sign and section note.
- **Lay:** header block, source and page rows, units, notes, `מקורות`, RTL, numeric cells.
- **Shots:** screenshots PDF.

| Company | Report | Source file, CF pages / financing page | Src | Per | Val | Map | (\*) | Lay | Shots |
|---|---|---|---|---|---|---|---|---|---|
| 341 שדה נדל"ן (thousand USD) | Q1 | `_Q1_1745548` p41–42 / 42 | PASS | PASS | PASS | PASS (M1) | PASS (M3) | PASS | PASS |
| | Q2 | `_Q2_1767508` p47–48 / 48 | PASS | PASS | PASS | PASS (M1) | PASS (M3) | PASS | PASS |
| 425 צבי צרפתי | Q1 | `_Q1_1744485` p73–74 / 73 | PASS | PASS | PASS | PASS | PASS | PASS (M4) | PASS |
| | Q2 | `_Q2_1766510` p84–86 / 85 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 1193 י.ח. דמרי | Q1 | `_Q1_1744429` p39–41 / 40 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| | Q2 | `_Q2_1764665` p42–44 / 43 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 1703 אחים יעקובי | Q2 only | `_Q2_1767724` p31–32 / 32 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 1928 רימון | Q1 | `_Q1_1743933` p32–33 / 33 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| | Q2 | `_Q2_1766226` p36–37 / 37 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 1979 אפי קפיטל | Q1 | `_Q1_1742790` p52–53 / 53 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| | Q2 | `_Q2_1763668` p55–56 / 56 | PASS | PASS | PASS | PASS (M2) | PASS | PASS | PASS |
| 2371 בית וגג | Q1 | `_Q1_1742688` p45 / 45 | PASS | PASS | PASS | PASS | PASS | PASS | PASS (M5) |
| | Q2 | `_Q2_1765823` p52 / 52 | PASS | PASS | PASS | PASS | PASS | PASS | PASS (M5) |
| 2385 עמרם אברהם | Q1 | `_Q1_1745346` p67–69 / 68 | PASS | PASS | PASS | PASS | PASS | PASS | PASS (M5) |
| | Q2 | `_Q2_1767833` p73–76 / 74 (not `-01`) | PASS | PASS | PASS | PASS | PASS | PASS | PASS (M5) |
| 2456 שמואל ברוך (`אלפי ₪`) | Q1 | `_Q1_1742581` p40–41 / 41 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| | Q2 | `_Q2_1766214` p50–51 / 51 | PASS | PASS | PASS | PASS | PASS | PASS | PASS (M5) |
| 2478 רייסדור | Q1 | `_Q1_1743625` p37–38 / 38 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| | Q2 | `_Q2_1766702` p38–39 / 39 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 2520 איסתא נכסים | Q1 | `_Q1_1742735` p30–31 / 30 (not `-01`) | PASS | PASS | PASS | PASS | PASS | PASS | PASS (M5) |
| | Q2 | `_Q2_1765451` p32–33 / 32 (not `-01`) | PASS | PASS | PASS | PASS | PASS | PASS (M4) | PASS (M5) |

### 2.1 What I confirmed per company

Values are given in statement order, right to left. Totals were confirmed on the image.

**341** (`אלפי דולר`)
- Columns:
  - Q1: 3M to 31.03.2026, 3M to 31.03.2025, FY 2025.
  - Q2: 6M 2026 and 2025, then 3M (אפריל–יוני) 2026 and 2025, then FY.
- Lines:
  - Q1 has 13 financing lines plus the total 4,909 | 25,809 | 87,769.
  - Q2 has 14 lines plus the total 153,121 | 38,060 | 148,212 | 12,251 | 87,769.
- Units: page 42 prints no units line. The zoom therefore uses the page 41 header strip, which has the same columns, and this is documented.
- Blank cell: Q1 `תשלום התחייבות אחרת` has a blank in the 3M-2026 cell, recorded as 0 with a note.
- (\*) interest, operating section, `ריבית ששולמה במזומן`:
  - Q1: (922) | (122) | (2,190).
  - Q2: (4,374) | (461) | (3,069) | (339) | (2,190).

**425** (`אלפי ש"ח`)
- Lines and totals:
  - Q1: 6 lines, total 397,432 | 39,667 | 42,576.
  - Q2: 6 lines, total 209,703 | 38,260 | (187,729) | (1,407) | 42,576.
- Dividend: in financing, item 11.
- (\*) interest: appears only in `נספח ב' – מידע נוסף` and is printed without parentheses.
  - Q1: 5,296 | 4,354 | 41,717.
  - Q2: 24,042 | 21,319 | 18,746 | 16,965 | 41,717.
  - They are recorded positive as printed, with the canonical note `גילוי בנספח ... – הסעיף לא צוין (לא בפעילות מימון)` and the remark that the amounts are printed without parentheses.
- Restatement marks `(*) הצגה מחדש ... ביאור 2ד'`:
  - Q1: next to the 3M-2025 operating values.
  - Q2: next to the 6M-2025 and 3M-2025 operating values.
  - No mark is on a financing value, so the restated flag stays `לא` and there is a column note. This follows convention §10.

**1193**
- Lines and totals:
  - Q1: 7 lines, total 484,083 | (156,924) | 348,012.
  - Q2: 7 lines, total 637,920 | (79,039) | 153,837 | 77,885 | 348,012.
- Combined line: `תמורה מהנפקת מניות ואופציות ומימושי אופציות...` goes to item 1 with a note, per convention §6.
- (\*) interest, operating section, `תשלומי ריבית`:
  - Q1: (44,497) | (39,467) | (213,780).
  - Q2: (106,592) | (100,774) | (62,095) | (61,307) | (213,780).

**1703**
- Q2 only. The statement shows only 6M 2026, 6M 2025 and FY 2025, and the workbook has these 3 columns.
- `דוח Q1 2026 אינו קיים בתיקייה` appears in the header block and in the master `חסרים והערות`.
- 5 lines, total (31,243) | 5,980 | (1,020).
- (\*) interest, operating section: (6,105) | (4,708) | (13,558).
- `קבלת הלוואה מצד קשור` goes to item 4. It is a gross receipt with no separate balance-sheet line, so rule A applies and the note says so.

**1928**
- The text layer has a broken `נ` glyph. The labels were rebuilt, and I checked them against the image.
- Lines and totals:
  - Q1: 9 lines, total 38,103 | 22,804 | 87,834.
  - Q2: 9 lines, total 82,781 | 47,776 | 44,678 | 24,972 | 87,834.
- Q2 `פירעון אגרות חוב` has blank cells for 6M 2025 and 3M 2025, recorded as 0 with a note.
- Mapping:
  - `רכישת מניות מהמיעוט` → 14.
  - Dividend to the minority → 12.
  - `קבלת הלוואה מנותני אשראי אחרים` → 4, rule A with the balance-sheet evidence (p26 / p28) in the note.
- (\*) interest, operating section:
  - Q1: (10,394) | (7,394) | (44,656).
  - Q2: (26,229) | (22,951) | (15,835) | (15,557) | (44,656).

**1979**
- Interest paid and dividends paid are inside financing, items 13 and 11. The (\*) info rows are 0, with a note.
- Lines and totals:
  - Q1: 7 lines, total 11,486 | 256,726 | 297,920.
  - Q2: 9 lines, total 41,513 | 295,508 | 25,155 | 42,514 | 297,920.
- The text layer reads `יפרעון`; the image shows `פירעון`, and the workbook has the corrected label.
- Bank and institutional loans, gross → 4 / 7, rule A. The note cites the balance sheet, which shows both current and non-current balances.

**2371**
- The whole statement is on one page.
- Lines and totals:
  - Q1: 4 lines, total 2,397 | (9,001) | 128,839.
  - Q2: 4 lines, total 11,099 | 12,232 | 8,702 | 21,233 | 128,839.
- (\*) interest, operating section:
  - Q1: (5,207) | (1,199) | (4,272).
  - Q2: (6,098) | (2,337) | (891) | (1,138) | (4,272).
- `*` restatement marks: only on the comparative operating values (Q1: 3M 2025; Q2: 6M and 3M 2025). The flag stays `לא`, with column notes, per §10.

**2385**
- Lines and totals:
  - Q1: 10 lines, total 975,019 | 840,661 | 1,132,277.
  - Q2: 11 lines, total 1,350,760 | 829,583 | 375,741 | (11,078) | 1,132,277.
- Mapping:
  - The net loan line from NCI holders → 5 (R3: a net line with no stated term).
  - Loans from equity-accounted companies, gross → 4 / 7, rule A with the non-current balance-sheet evidence in the note.
  - `חלוקת תשואה לזכויות שאינן מקנות שליטה` → 12.
- (\*) interest, operating section:
  - Q1: (70,265) | (63,006) | (273,461).
  - Q2: (160,138) | (132,561) | (89,873) | (69,555) | (273,461).

**2456**
- Units: `אלפי ₪`.
- The statement title is `דוח תמציתי על תזרימי המזומנים`, without the word `מאוחד`.
  - It is the only cash-flow statement in each file.
  - The notes say `הדוחות הכספיים ביניים תמציתיים/מאוחדים אלה` (Q1 p44, Q2 p54).
  - This is documented as R1.2 requires.
- Lines and totals:
  - Q1: 7 lines, total 67,258 | 25,763 | 111,700.
  - Q2: 8 lines, total 80,021 | 20,529 | 12,763 | (5,234) | 111,700.
- Interest paid is in financing, item 13.
- `קבלת הלוואות מצדדים קשורים` is printed negative only, so it is a net movement and goes to item 5. This is noted and listed as a source irregularity.
- Q2 `(פרעון) אגרות חוב` → 8, with the verbatim text including the parentheses.

**2478**
- Lines and totals:
  - Q1: 5 lines, total 425,138 | 75,953 | 187,073.
  - Q2: 5 lines, total 349,085 | 281,707 | (76,053) | 220,294 | 187,073.
- Interest and dividends are in financing.
- Q2, 3M April–June 2025: the lease line is printed +186, recorded as printed with a note.
- Q2 page 38 marks two operating lines `(*) הוצג מחדש`. No column or financing value is marked, so the flag stays `לא` with column notes.
- Q1 pages 37–38 have no `*` mark (checked in the text layer).

**2520**
- Interest is in financing, item 13. Dividends to NCI → 12.
- Lines and totals:
  - Q1: 10 lines, total (25,520) | 46,877 | 19,561.
  - Q2: 10 lines, total 202,781 | (132,577) | 228,301 | (179,454) | 19,561.
- Credit from the parent company and other shareholders, gross → 4 / 7, rule A. The balance sheet (p25) shows the balance as non-current.
- Q2, April–June 2026: the repayment line is printed +14,913, recorded as printed with a note.
- The `-01` files are correctly listed in `מקורות` as investee statements, not used.

---

## 3. Cross-report checks (recomputed from the verified workbooks)

**C3 (FY 2025, total and each item):** equal in Q1 and Q2 for all 10 companies with both reports.

**C2 (totals):**
- Equal for 341, 425, 1193, 1928, 2371, 2385, 2456 and 2520.
- Mismatches, all genuine differences between the two source reports. I confirmed each on the images, and each is explained in the master `חסרים והערות`:

| Company | Period | Q1 report | Q2 6M − 3M | Difference | Made of | Master row |
|---|---|---|---|---|---|---|
| 1979 | 3M 2026 | 11,486 | 16,358 | 4,872 | loans received 3,384 + interest 1,488 | r116 (items: r114, r115) |
| 1979 | 3M 2025 | 256,726 | 252,994 | 3,732 | all interest; reclassified against operating | r120 (items: r117–r119) |
| 2478 | 3M 2025 | 75,953 | 61,413 | 14,540 | net loans 13,223 + interest 1,317 | r143 (items: r141, r142) |

- In the 2478 item r140, the −1 on interest in 2026 follows from the source rounding.

**C1:** 2478 Q2, April–June 2026: the sum of the lines is −76,054 and the printed total is −76,053.
- This is a source rounding, kept as printed.
- It is documented in the column note, in master r139 (C1) and r179 (`בדיקה לא אפס`), and in `<iss>_checks.json` (validate shows it as an explained INFO).
- All other 82 columns are 0.

---

## 4. Issues found (none blocking)

**M1 – 341 Q1 and Q2: rule-A evidence missing from a line note (minor documentation).**
- **Line:** `פרעון הלוואות בערבות מדינה` → 7.
- **Problem:** the note (mapping sheet, row 8 in the Q1 block and row 28 in the Q2 block) says `הלוואות לזמן ארוך (ללא ציון תקופה בדוח; מוצג ברוטו)`. It cites no balance-sheet evidence, which PIPELINE §7 rule A asks for.
- **Assignment is right:** the consolidated balance sheet (Q1 p36) has no separate line for these loans, so the line cannot be attributed. Rule A's default is then 4/7 with a note, so 7 is correct.
- **Suggestion:** add the balance-sheet reference.

**M2 – 1979 Q2: rule-A evidence missing from a line note (minor documentation).**
- **Line:** `פירעון הלוואות מצדדים קשורים ומאחרים` → 7.
- **Problem:** the note cites no balance-sheet evidence.
- **Assignment is right:** the balance sheet (Q2 p52) shows `הלוואות מצדדים קשורים ובעל עניין` both as current (1,202) and as non-current (14,308). Under rule A, mixed balances go to 4/7.
- **Suggestion:** add the reference.

**M3 – 341: Q1-2026 (\*) interest differs between the two reports, with no note (informational).**
- **The figures:**
  - Q1 report, page 41: (922).
  - Q2 report, page 47: (4,374) − (3,069) = (1,305).
  - Difference: 383.
- **Why it is not a failure:**
  - Both values are as printed; I confirmed them on the images.
  - C2 covers only the financing totals and items, and the (\*) row is information only.
- **Suggestion:** add a `לידיעה` note, in the spirit of A1 (item-level differences between reports recorded as notes).

**M4 – 425 Q1 and 2520 Q2: process remarks in the deliverable (cosmetic).**
- The general notes contain process remarks: `שנבחרו בטעות בשלב מוקדם ותוקנו`.
- **Where:**
  - 425 workbook, `פירוט מימון` B42.
  - 2520 workbook, `פירוט מימון` B45.
- **Suggestion:** drop them.

**M5 – Screenshots PDFs (cosmetic; content and legibility are fine).**
- The red (\*) crops of 2371 Q1/Q2 (pages 4 and 7) and 2385 (pages 4 and 9) show thin slivers of the neighbouring rows at their top and bottom edges.
- The 2520 context pages (Q1 p4 / Q2 p7) are captioned `(פעילות שוטפת)`. They actually show `נספח א'`, the operating adjustments. The caption is acceptable but imprecise.
- In the 2456 Q2 full page (screenshots page 5), the blue frame's left edge sits tight against the FY column. The text is still inside the frame.

**M6 – Quality gate: subset mode reports false failures (not a deliverable defect).**
- **The symptom:** with `--issuers <subset>` but without `--no-master`, `validate.py` reports 787 AC11 failures and 1 T1 failure.
- **The cause:** both are artifacts of comparing the master by row position.
  - Lines 205–211 enumerate the subset's expected rows from row 2 of the full 648-row `נתונים`.
  - The run also prints `rows 648 == periods 83`.
- **No real defect:** my own key-based comparison of the master against the company workbooks found 0 differences, and the T1 flags are correct.
- **Recommendation:** the final Inspector should run the full `validate.py` (no `--issuers`) for the master checks.

## 5. Overall batch verdict

**PASS.** For all 21 reports:
- the right source file and consolidated statement;
- every period column;
- every value (confirmed on images I saw);
- every line mapped plausibly per R3 and the conventions, with C1 reconciled;
- the (\*) info rows, layout and screenshots are correct;
- C2/C3 mismatches are genuine and explained;
- the master rows equal the company workbooks, including T1.

The 6 observations above are minor and optional.
