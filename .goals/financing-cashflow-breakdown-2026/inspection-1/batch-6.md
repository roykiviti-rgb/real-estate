# Inspection 1, batch 6: findings

**Companies (20 reports):** 373, 434, 444, 673 (Q2 only), 823, 1484, 1561, 1724, 2417, 2441, 2574 (Q2 only)

**Inspector:** batch-6 Inspector, iteration 1 (2026-11-10)

**References:** `goal.md`, `goal-amendment-1.md` (T1, T2), `goal-amendment-2.md` (T3 cancelled), `work/phaseB-conventions.md` and `PIPELINE.md` §7 (mapping rules).

## Overall verdict: **PASS**

- **Blocking issues: 0.**
- **Non-blocking observations: 5** (O1–O5 below). None of them changes a number, an item, or a check.

---------------------------------------------------------------------------------------------------

## 1. Method: what I saw and how

I formed my findings first. Only afterwards did I read the builder report, and only to confirm AC8 coverage.

1. **Source scan (PyMuPDF).**
   - I scanned every PDF in the 11 folders for cash-flow, financing, consolidated and separate (38D) markers.
   - I dumped the text layer with coordinates for every cited cash-flow page and the pages next to it.
   - I listed the other candidate statements and confirmed that they were rejected:
     - 38D separate data: 434 Q2 p93; 823 Q1 pp80–81 and Q2 pp93–94; 1724 Q1 pp69–70 and Q2 pp75–76.
     - Investee statements inside 823's board-report section: p37–38 (רג'נסי) and p41 (חג'ג' סומייל).
     - Board-report pages.
   - For the 4 reports with a broken font (373 Q1/Q2, 2441 Q1/Q2), I normalised the `ð` glyph to `נ`.
2. **Independent visual confirmation.** I rendered 13 composite PNGs (150–170 DPI) of the source PDFs, each containing:
   - the title, column headers and units strip;
   - the whole financing section;
   - every interest/dividend-paid line outside financing (operating section or appendix).

   All images displayed; I used 28 images in total, under the cap. On them I read:
   - every line × every column of all 20 financing sections, including the totals;
   - every (\*) value.
3. **Company workbooks (openpyxl).** I dumped all three sheets and checked them with my own scripts:
   - every item equals the sum of its mapped lines, for every column; net-by-sign codes `6/14` were resolved per column;
   - the totals and the (\*) rows equal the mapping sheet;
   - C1 recomputed: zero everywhere except 2417 Q1 3M-2025 = −1, which the source itself causes and which is documented;
   - every mapping line's verbatim text matches the PDF text layer. The only exception is 1561 Q1 line 2, where the text layer reads `יפרעון`; I confirmed `פירעון` on the image, as the builder's note says.
4. **Screenshots PDFs.**
   - Image inventory: zoom crops are 220 DPI, full pages 150 DPI, context pages 120 DPI (consistent with `fcf_render` DPI_ZOOM/PAGE/CTX).
   - Captions were parsed (report ID, Q, PDF page) and mapped to the source pages.
   - Visual checks:
     - all 18 zoom pages, rendered at 88–100 DPI;
     - all 16 red (\*) crops, at 78 DPI; 373's 2 in its overview at thumbnail scale, the other 14 at legible size;
     - a 36-DPI grid of the other 18 full pages (373's 2 seen in its overview).
5. **Master workbook.**
   - `נתונים`:
     - all 80 rows of my companies compared field by field with the company workbooks, including file, page, months, end date, T1, restated flag, (\*) values and the screenshot path;
     - the T1 flag was recomputed from (months, end date).
   - `מיפוי שורות`:
     - all 778 long-format rows compared with the company mapping sheets;
     - the only difference is 434's net-NCI line: `6/14` in the company sheet, resolved to `6` or `14` per period in the master, which is correct.
   - `חסרים והערות`, `אינדקס קבצים` and `הסבר` (T1/T2 legend) were read for my companies.
6. **validate.py.** I ran `validate.py --issuers 373 434 444 673 823 1484 1561 1724 2417 2441 2574 --no-master --out %TEMP%\fcf_insp\6\…`.
   - Result: `PASS 3273  FAIL 0  INFO 1`. The INFO is the explained C1 of 2417.
   - Exit code 0. No `__pycache__` was created.

Hygiene of the 11 folders: each contains only its source PDFs plus the 2 output files. There are no `~$` lock files.

---------------------------------------------------------------------------------------------------

## 2. Per company × report

**Column legend for the tables below:**

| Abbreviation | Means |
|---|---|
| Src | right file, consolidated statement, correct pages |
| Per | columns, labels, months, end dates, restated flag, T2 |
| Val | every line value equals the PDF (confirmed on the image) |
| Map | items against R3 and the conventions |
| (\*) | info rows and their notes |
| Lay | workbook layout: header block, rows, notes, `מקורות`, RTL, numeric cells |
| Shot | screenshots PDF |

### 373 אאורה השקעות

| Report | Src | Per | Val | Map | (\*) | Lay | Shot |
|---|---|---|---|---|---|---|---|
| Q1 (pp53–54, fin p54) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Q2 (pp57–58, fin p58) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**Q1 values:**
- 11 lines and the total confirmed, e.g. ST credit 78,817 / 151,112 / 564,276 and total 576,612 / 361,356 / 1,220,542.
- The dividend cell for 3M-2026 is blank in the source; it was recorded as 0, with a note.

**Q2 values:**
- 12 lines confirmed, including רכישה עצמית (12,223) → 9 and the total 722,708 / 645,756 / 146,096 / 284,400 / 1,220,542.
- The total line is printed as `מעילות`; it was kept verbatim, with a note.

**Mapping:**
- עסקאות עם בעלי זשמ"ש (5,756) → 14. Verified: Q1 p7 and p58 say 776,380 Megido shares were bought for about 5.76M.
- Megido share and option issues to NCI → 6.

**(\*):** interest paid in operating:
- Q1 p53: (54,473) / (32,660) / (167,395).
- Q2 p57: (101,995) / (79,161) / (47,522) / (46,501) / (167,395).

**Restatement marks:** the 2025 operating amounts carry (\*) "הצגה מחדש" marks. These are column notes only, which is correct per convention 10.

**Cross-report:** C2 and C3 match exactly.

### 434 ישראל קנדה (ט.ר)

| Report | Src | Per | Val | Map | (\*) | Lay | Shot |
|---|---|---|---|---|---|---|---|
| Q1 (pp53–56, fin p53) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Q2 (pp58–61, fin p58) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**Values:** 13 lines and the total in both reports, e.g. Q1 total 488,955 / (31,886) / 347,119 and Q2 total 459,479 / (85,518) / (29,477) / (53,633) / 347,119.

**Mapping:**
- מיזוג חברה בת – נספח ה' (69,692 FY) → אחר (merger flow).
- עסקאות עם זשמ"ש → net_nci (6/14), per PIPELINE §7.
- פירעון הלוואות מאחרים → 7. Balance sheet p47 shows mixed classification: current 3,583 and non-current 14,000, so 4/7 under rule A.
- פירעון אג"ח ורכישה עצמית → 8.

**(\*):** interest disclosed only in appendix ב' ("מידע נוסף על תזרימי המזומנים מפעילות שוטפת"), positive as printed:
- Q1 p55: 74,802 / 67,935 / 341,471.
- Q2 p60: 213,285 / 179,042\* / 128,219 / 107,136\* / 378,178\*.
- The reclassified FY value (378,178 in Q2 vs 341,471 in Q1) is listed as a source irregularity in the master.

**Cross-report:**
- C2 total differs by 1 in both 2026 and 2025. These are source rounding differences, explained in the master (`חסרים והערות` r77 and r81, plus item rows r72–r80) and in builder-report-1.
- C3 matches on the total and on every item.

### 444 מרדכי אביב

| Report | Src | Per | Val | Map | (\*) | Lay | Shot |
|---|---|---|---|---|---|---|---|
| Q1 (pp35–36, fin p35) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Q2 (pp37–38, fin p37) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**Units:** Q1 is in באלפי ₪, Q2 in באלפי ש"ח. Both are recorded per column.

**Values:**
- Q1: 6 lines, total (170,257) / (47,788) / (118,397).
- Q2: 4 lines, total (187,214) / (54,859) / (16,957) / (7,071) / (118,397).

**Mapping:** gross bank-loan receipt and repayment lines without a stated term → 4/7. Balance sheet p32 supports this: non-current bank loans 64,500, and current maturities are mixed with credit.

**(\*):** interest is in "מידע נוסף" of appendix א'.
- Q1 p36: 10,199 / 12,504 / 37,715.
- Q2 p38: 13,075 / 16,834 / 2,876 / 4,330 / 37,715.

**Cross-report:** C2 and C3 match exactly.

### 673 קבוצת ריי טי.אל.וי (Q2 only)

| Report | Src | Per | Val | Map | (\*) | Lay | Shot |
|---|---|---|---|---|---|---|---|
| Q2 (p31) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**Periods:** the statement presents only 6M-2026, 6M-2025 and FY-2025. There are no 3-month columns, and all 3 columns are captured.

**Values:** 7 lines and the total, 13,901 / 9,574 / 9,915.

**Mapping:**
- Gross related-party, bank and other loan lines → 5. Balance sheet p28 shows the loans as current; non-current loans from others are 0 at 30.06.2026. This follows rule A.
- Interest in financing → 13.
- מניות + כתבי אופציה → 1 (convention 6).

**(\*):** both rows are 0, with the correct note.

**Missing Q1:** the header block states `דוח Q1 2026 אינו קיים בתיקייה`, and the master lists 673 as a missing report.

### 823 קבוצת חג'ג' ייזום נדל"ן

| Report | Src | Per | Val | Map | (\*) | Lay | Shot |
|---|---|---|---|---|---|---|---|
| Q1 (pp59–61, fin p60) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Q2 (pp68–70, fin p69) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**Source:** the `…1767825-01.pdf` file is a BDO valuation (p1 confirmed). It is marked as an appendix, not used, in both `מקורות` and `אינדקס`.

**Values:**
- Q1: 8 lines, total 65,106 / 391,870 / 985,719.
- Q2: 9 lines, total 404,967 / 1,082,438 / 339,861 / 690,568 / 985,719.

**Units:** p60 has no units line; the zoom header strip was taken from p59, as documented.

**Mapping:**
- הנפקת אופציות → 2.
- Loans "מתאגידים בנקאיים, מוסדות פיננסיים ואחרים" (gross, mixed) → 4/7.
- חלוקת דיבידנד (33,000) → 11.

**(\*):** appendix ב' "…מפעילות שוטפת", positive as printed:
- Q1 p61: 50,997 / 57,003 / 234,755.
- Q2 p70: 85,960 / 94,563 / 34,963 / 37,560 / 234,755.

**Cross-report:**
- C2 totals match. Two C2-item rounding differences of ±1 (items 4 and 7, 2025) are explained.
- C3 matches exactly.

### 1484 מצלאוי חברה לבנין

| Report | Src | Per | Val | Map | (\*) | Lay | Shot |
|---|---|---|---|---|---|---|---|
| Q1 (pp33–34, fin p34) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Q2 (pp35–36, fin p36) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**Source:** the statements are not consolidated ("דוחות על תזרימי המזומנים"; the company has no subsidiaries). The primary statement was used, with a note, per R1.2.

**Values:**
- Q1: 4 lines, total (4,089) / 15,617 / 63,181.
- Q2: 5 lines, total 32,940 / 21,278 / 37,006 / 28,973 / 63,181.
- Positive amounts printed in repayment lines are kept as printed: FY 23,659 in פירעון הלוואות לזמן ארוך, and Q2 lease 1,854 / 2,342. Each column's total confirms the sign.

**(\*):** interest in operating:
- Q1 p33: (1,679) / (3,082) / (11,808).
- Q2 p35: (5,900) / (4,855) / (4,221) / (1,773) / (11,808).

**Cross-report:**
- C2 2026 differs by 23 (bonds (34,210) vs (34,187)).
- C2 2025 differs by 23,312 (the Q2 2025 comparatives are internally inconsistent).
- Both are source differences, explained in detail in the master (r97–r102, r42–r44) and in builder-report-1.
- C3 matches exactly.

### 1561 הכשרת הישוב התחדשות עירונית

| Report | Src | Per | Val | Map | (\*) | Lay | Shot |
|---|---|---|---|---|---|---|---|
| Q1 (pp22–23, fin p22) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Q2 (pp26–27, fin p26) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**Values:**
- Q1: 6 lines, total 30,289 / (29,577) / 24,158.
- Q2: 6 lines, total 32,571 / (29,581) / 2,282 / (4) / 24,158.

**Mapping:**
- Amounts from the pinui-binui partner → 4. Balance sheet p19 shows a non-current liability to the partner of 47,298.
- קיטון בהלוואה מהחברה האם → 5 (PIPELINE §7).
- תקבולים מזשמ"ש → 6.
- הנפקת מניות (shares and warrants) → 1.

**(\*):** interest is in appendix א', inside the operating reconciliation.
- Q1 p23: (116) / (181) / (653).
- Q2 p27: (229) / (315) / (113) / (134) / (653).

**Cross-report:** C2 and C3 match exactly.

### 1724 רמות בעיר

| Report | Src | Per | Val | Map | (\*) | Lay | Shot |
|---|---|---|---|---|---|---|---|
| Q1 (pp49–50, fin p49) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Q2 (pp53–54, fin p53) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**Values:**
- Q1: 6 lines, total (94,345) / 105,742 / 65,753.
- Q2: 8 lines, total (202,364) / 72,767 / (108,020) / (32,976) / 65,753.

**Mapping:** הנפקת שטרי הון לבעלי שליטה (10,000) → 1 (convention 4). The notes are in equity: p45 shows שטרי הון 75,319 and p48 shows an equity column.

**(\*):** interest is in appendix "מידע נוסף".
- Q1 p50: (5,415) / (7,948) / (50,630).
- Q2 p54: (15,598) / (25,561) / (10,183) / (17,613) / (50,630).

**Cross-report:**
- C2 total differs by 1 in both years (rounding). This is explained in the master (r110–r113) and in builder-report-1.
- C3 matches exactly.

### 2417 אנשי העיר מקבוצת רוטשטיין

| Report | Src | Per | Val | Map | (\*) | Lay | Shot |
|---|---|---|---|---|---|---|---|
| Q1 (p66) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Q2 (p71) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**Values:**
- Q1: 8 lines, total 18,644 / 45,943 / 120,227.
- Q2: 8 lines, total 28,260 / 101,967 / 9,617 / 56,024 / 120,227.

**C1:** Q1 3M-2025 = −1, because the printed lines sum to 45,942 against a printed total of 45,943. This is documented in:
- the column note;
- the master: C1 row r129 and the "בדיקה לא אפס" row r178;
- validate.py, as INFO (explained).

**(\*):** interest in operating:
- Q1 p66: (2,158) / (2,865) / (16,153).
- Q2 p71: (7,442) / (8,322) / (5,284) / (5,457) / (16,153).

**Cross-report:**
- C2 2026 total differs by 1 (rounding), explained in the master (r130–r132).
- C3 matches exactly.

### 2441 שובל הנדסה ובניין

| Report | Src | Per | Val | Map | (\*) | Lay | Shot |
|---|---|---|---|---|---|---|---|
| Q1 (pp50–51, fin p50) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Q2 (pp55–56, fin p55) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**Values:**
- Q1: 9 lines, total (5,567) / 125,713 / 162,851.
- Q2: 9 lines, total 11,730 / 112,207 / 17,297 / (13,506) / 162,851.

**Mapping:**
- Interest paid in financing → 13.
- Gross ST credit receipt and repayment → 5.
- פרעון הלוואה מאחרים (1,000 per quarter) → 7. The balance sheet p47 is mixed, so 4/7 under rule A.
- מניות ואופציות → 1.

**(\*):** both rows are 0.
- Investing contains only interest *received*.
- p51/p56 show capitalised interest that is non-cash, correctly not counted as (\*).

**Cross-report:** C2 and C3 match exactly.

### 2574 עמים יזמות (Q2 only)

| Report | Src | Per | Val | Map | (\*) | Lay | Shot |
|---|---|---|---|---|---|---|---|
| Q2 (p30) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**Units:** אלפי ₪.

**Values:** 6 lines, total 259,390 / (17,680) / 128,876 / 31,287 / 302,023.

**Mapping:**
- Related-party gross loans → 5. Balance sheet p27 shows the related-party balance as current only.
- Banks and financial institutions (current 1,222,580 and non-current 242,751, so mixed) → 4/7.
- Interest in financing → 13.

**Missing Q1:** the header block states `דוח Q1 2026 אינו קיים בתיקייה`, and the master lists 2574 as a missing report.

---------------------------------------------------------------------------------------------------

## 3. Screenshots PDFs (all 11 PASS)

**Structure and sizes:** the same structure for every report.
- Cover with TOC.
- Full page with a yellow/orange highlight of the financing section and a blue header box, at 150 DPI.
- Zoom crop of the header strip and the financing section, at 220 DPI.
  - It includes the period headers and the units line.
  - A dashed separator marks any omitted part.
- A red (\*) crop for every (\*) line (with header and units).
- Context pages of the statement, at 120 DPI.

**Caption-to-page mapping, from the parsed captions:**

| Company | Q1 pages | Q2 pages |
|---|---|---|
| 373 | 54 / 54 / 53\* / 53 | 58 / 58 / 57\* / 57 |
| 434 | 53 / 53 / 55\* / 54, 55, 56 | 58 / 58 / 60\* / 59, 60, 61 |
| 444 | 35 / 35 / 36\* / 36 | 37 / 37 / 38\* / 38 |
| 673 | — | 31 / 31 |
| 823 | 60 / 59 + 60 / 61\* / 59, 61 | 69 / 69 / 70\* / 68, 70 |
| 1484 | 34 / 34 / 33\* / 33 | 36 / 36 / 35\* / 35 |
| 1561 | 22 / 22 / 23\* / 23 | 26 / 26 / 27\* / 27 |
| 1724 | 49 / 49 / 50\* / 50 | 53 / 53 / 54\* / 54 |
| 2417 | 66 / 66 / 66\* | 71 / 71 / 71\* |
| 2441 | 50 / 50 / 51 | 55 / 55 / 56 |
| 2574 | — | 30 / 30 |

These pages equal the pages cited in the workbooks and in `אינדקס קבצים`. Every caption names the company, the report, the correct report-ID file and the PDF page. Digits are crisp in every zoom and (\*) crop I viewed.

---------------------------------------------------------------------------------------------------

## 4. Cross-report and master (all PASS)

- **Recomputed C2/C3 mismatches:** 434 (2026: 1, 2025: 1), 1484 (2026: 23, 2025: 23,312), 1724 (2026: 1, 2025: 1), 2417 (2026: 1).
  - Every one is a source-level difference.
  - Each has an explanation row in `חסרים והערות` and is listed in builder-report-1.
  - No C3 mismatch exists in this batch.
- **`נתונים`:** 80 rows (8 per two-report company, 3 for 673, 5 for 2574). Each equals the company workbook in every value and descriptive field.
- **T1 flag:** `לא` only on each two-report company's Q1 FY-2025 row; `כן` on every other row. This is correct.
- **`מיפוי שורות`:** 778 rows for my companies (373: 109, 434: 120, 444: 54, 673: 24, 823: 85, 1484: 53, 1561: 64, 1724: 74, 2417: 80, 2441: 80, 2574: 35). Each equals the company mapping sheets.
- **`אינדקס קבצים`:** roles, used flags and pages are correct for all 21 PDFs of my companies.

---------------------------------------------------------------------------------------------------

## 5. Non-blocking observations (no fix required for PASS)

**O1 – 1484, wording.** The statement is not consolidated. The screenshot captions, the mapping-block headers, the `מקורות` notes and the generic `סימון` line still call it "הדוח המאוחד על תזרימי המזומנים". The workbook's general notes (rows 42 and 45) correctly explain that the company has no subsidiaries. This is cosmetic.

**O2 – 1484, sign in repayment lines.** These positive amounts are kept in items 7 and 10 as printed:
- FY-2025 `פירעון הלוואות לזמן ארוך` +23,659 (both reports);
- Q2 `פירעון התחייבות בגין חכירה` +1,854 (6M-2026) and +2,342 (Apr–Jun 2026).

The totals confirm that the signs are intended. The case is documented as a source irregularity, and the treatment is consistent across Q1 and Q2 (C3 = 0).

One could argue that R3's net-line rule would put +23,659 in item 4. However, the line is labelled as a repayment, not as a net line, so this is a judgment call. Phase C may want to align it with any similar case in other batches.

**O3 – 444 and 1724, (\*) section label.** Interest appears only in a "מידע נוסף" block, which in 444 sits inside appendix א' (the operating reconciliation). The label used is `…הסעיף לא צוין (לא בפעילות מימון)`. By elimination the amount is in operating. The conservative label is allowed by convention 1, but 434 and 823 use `נכלל בפעילות שוטפת` where the appendix title says so explicitly. Consistent with the rule; noted for awareness.

**O4 – 823, dividend (\*) row note.** The note is empty, while 373, 434 and 444 carry `אין סכומים מחוץ לפעילות מימון (דיבידנד ששולם מוצג בדוח בפעילות מימון)` for the same situation (823 Q2 pays 33,000 in financing). R5 is still met (value 0), and the general notes say the dividend is in financing. Cosmetic inconsistency.

**O5 – page cells stored as text.** The page numbers under the column headers (row `עמוד PDF (פעילות מימון)`) are text cells. R4 requires numeric cells only for amounts, and this matches the approved pilot layout.

---------------------------------------------------------------------------------------------------

## 6. Batch verdict

**PASS.**

All 20 reports of the 11 companies:
- use the correct source and statement;
- capture all periods with correct T2 labels;
- reproduce every value exactly, confirmed on images;
- are fully mapped (plug-free and consistent with R3 and the conventions);
- record the (\*) amounts correctly;
- have correct layout, screenshots and master rows.

Every C1/C2 deviation is a documented source effect. There is no C3 mismatch.

Temporary files were written only to `%TEMP%\fcf_insp\6\` and are deleted at the end of this inspection.
