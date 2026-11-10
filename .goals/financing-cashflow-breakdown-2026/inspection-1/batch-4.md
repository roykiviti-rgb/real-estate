# Inspection 1 – Batch 4 of 8

Inspector: batch-4 Inspector, iteration 1, 2026-11-10.

Companies: 111 (Q2 only), 400, 539, 1083, 1502, 1553, 1622, 2481, 2483, 2488, 2524. That is 21 reports.

References: `goal.md`, `goal-amendment-1.md`, `goal-amendment-2.md` and `work/phaseB-conventions.md`. Builder and batch reports were read only after my findings were formed, and only to cross-check that the C1/C2 explanations are also in `builder-report-1.md`. They are.

## Verdict: **PASS**

- Blocking issues: 0.
- Minor or documentation issues: 3 (M1–M3).
- Cosmetic screenshot remarks: C1–C4.
- Tooling note: T1.

Details are below.

---

## 1. How I verified (independent of the Builders)

1. **Inventory and hygiene.**
   - I listed all 11 company folders. Each holds only its source PDFs and the two outputs; there are no lock files and no `__pycache__`.
   - I computed the SHA-256 of all 22 source PDFs and compared them with `baseline_files_sha256.csv`. Result: 22/22 identical.
2. **Source and page selection.**
   - I ran my own PyMuPDF scan of every page of every source PDF for cash-flow, consolidated, financing, separate-data (38D), operating, investing, interest-paid and dividends-paid keywords.
   - Every cited page set is the consolidated statement (`דוחות (תמציתיים) מאוחדים על תזרימי המזומנים`). None is a 38D page, a board-report table or an investee statement:
     - 1622: EX/CPS, Smitell II and Extell Holdings I.
     - 1553: גוב אלמוגים.
     - 111: פסגת מרים.
   - 539 `…_1765452-01.pdf` (25 pp.) is an appraisal: page 1 reads "שומת מקרקעין מקיפה – מרכז מסחרי רוטשטיינס" (Haushner). It is correctly marked `נספח – שומה/הערכת שווי`, לא בשימוש.
3. **Independent extraction.**
   - I dumped every row of every cash-flow page from the text layer, using words and char-level number grouping with parenthesis detection.
   - I re-derived every sign from the column arithmetic, for every column of every report.
   - Example: for 2483 Q2, April–June 2026, the lines sum to (67,724) against a printed total of (67,729).
4. **Automated comparison.** Every line of every `מיפוי שורות` block was matched to its PDF row (values per column with sign; blank and `-` = 0) and its text was compared. All matched. The only automatic "mismatches" came from my tool:
   - hidden line-number digits at x≈265 in the 2481 Q1 text layer;
   - different column x-positions on 1553 p.46.

   Both were re-checked manually and on the images.
5. **Visual confirmation of every value.**
   - I built 14 composites with my own script: header strip, financing section and (\*) lines of each report, rendered from the source PDFs at 150 DPI.
   - I viewed them myself; all 14 images displayed.
   - On them I compared every line text, every value of every column, the column headers and the units against the workbook values:
     - 111: 24 values;
     - 400: 61;
     - 539: 88;
     - 1083: 72 + 16 (\*);
     - 1502: 3 + 10;
     - 1553: 69;
     - 1622: 122;
     - 2481: 96;
     - 2483: 88;
     - 2488: 64;
     - 2524: 72;
     - plus all (\*) lines.

   All 18 images I viewed displayed.
6. **Workbook internal checks** (my script, applied to each company workbook):
   - every item equals the sum of its mapped lines, per column;
   - `אחר` and the total equal the mapping sheet;
   - C1 per column;
   - both (\*) info rows equal the sum of their (\*) lines;
   - column labels in `פירוט מימון` equal `דוח Qn 2026 | <mapping-sheet label>`;
   - months, end dates, restated flags, verbatim header texts, units/currency, page rows, header block, `מקורות` rows, RTL on all three sheets, numeric cells with `#,##0;-#,##0;0` format.
7. **Master workbook** (my comparison scripts, all fields):
   - `נתונים`: 83 rows for my companies, which is 3 + 10 × 8 periods. All 36 columns equal the company workbooks: 0 differences, including the T1 flag, which I recomputed. FY-2025 rows of Q1 reports are `לא`; all other rows are `כן`; all 111 rows are `כן`.
   - `מיפוי שורות`: 820 rows, 0 differences in file, page, line, verbatim text, period, value, item, label and note. The net 4/7 line of 1553 is resolved per sign, as designed.
   - `אינדקס קבצים`: 22 rows, roles and pages as in `מקורות`.
   - `חסרים והערות` explains every mismatch (section 4).
8. **Screenshots PDFs.**
   - With PyMuPDF I read every page's caption text and every embedded image's pixel size. Full pages are 1241×1754 px for A4, about 150 DPI against the source. Zoom crops are about 1,420–1,713 px wide over the about 500–560 pt section width, about 200 DPI. Context pages are about 120 DPI. These are the pilot settings (T3 cancelled).
   - All 93 pages were rendered at 130 DPI and visually reviewed by three read-only sub-agents with a fresh image budget each. 29 + 32 + 32 = 93 images displayed; none was capped.
   - One sub-agent suspicion, reversed Hebrew on 1553 pages 2 and 6, was **disproved** by my own checks:
     - the embedded raster extracted at native pixels reads correctly;
     - a close crop of the same PNG reads correctly;
     - the page has no mirroring transform, and its text direction is (1, 0).

     It was a misreading of the downscaled full page.
9. **Quality gate.** `validate.py --issuers <11> --no-master --out %TEMP%\fcf_insp\4\…` gave `PASS 3396  FAIL 0  INFO 1`. The INFO is the explained C1 of 2483 Q2.

---

## 2. Per company × report

Legend: ✔ = PASS.

| Company | Report | Source (file / CF pp / fin p) | Periods | Values | Mapping | (\*) | Layout | Screenshots |
|---|---|---|---|---|---|---|---|---|
| 111 | Q2 | ✔ `…_Q2_1767282.pdf` / 16–17 / 16 | ✔ 6M-26, 6M-25 (מוצג מחדש), FY-25 | ✔ 7 lines + total | ✔ | ✔ | ✔ (Q1 missing stated) | ✔ (5 pp) |
| 400 | Q1 | ✔ `…_Q1_1745054.pdf` / 33–34 / 33 | ✔ 3 cols | ✔ 6 + total | ✔ | ✔ | ✔ (M2) | ✔ (C1) |
| 400 | Q2 | ✔ `…_Q2_1767345.pdf` / 37–38 / 37 | ✔ 5 cols, T2 | ✔ 7 + total | ✔ | ✔ | ✔ (M2) | ✔ (C1, C3) |
| 539 | Q1 | ✔ `…_Q1_1744508.pdf` / 55–56 / 56 | ✔ | ✔ 10 + total | ✔ | ✔ | ✔ | ✔ |
| 539 | Q2 | ✔ `…_Q2_1765452.pdf` / 58–60 / 59 (`-01` = appraisal) | ✔ T2 | ✔ 10 + total | ✔ | ✔ | ✔ | ✔ |
| 1083 | Q1 | ✔ `…_Q1_1742346.pdf` / 48–50 / 49 | ✔ | ✔ 8 + total | ✔ | ✔ (M1) | ✔ | ✔ (C2) |
| 1083 | Q2 | ✔ `…_Q2_1763408.pdf` / 49–51 / 50 | ✔ T2 | ✔ 8 + total | ✔ | ✔ (M1) | ✔ | ✔ (C2) |
| 1502 | Q1 | ✔ `…_Q1_1744791.pdf` / 38–40 / 39 | ✔ | ✔ heading row `-`×3 used as total 0 (documented) | ✔ | ✔ (`-` → 0) | ✔ | ✔ (C2, C4) |
| 1502 | Q2 | ✔ `…_Q2_1767654.pdf` / 39–41 / 40 | ✔ T2 | ✔ 1 line + total, all `-` | ✔ | ✔ | ✔ | ✔ (C2) |
| 1553 | Q1 | ✔ `…_Q1_1745440.pdf` / 46–47 / 47 | ✔ | ✔ 7 + total | ✔ | ✔ | ✔ | ✔ (C2) |
| 1553 | Q2 | ✔ `…_Q2_1763612.pdf` / 49–50 / 50 | ✔ T2 | ✔ 8 + total | ✔ | ✔ | ✔ | ✔ (C2) |
| 1622 | Q1 | ✔ `…_Q1_1745241.pdf` / 51–52 / 52 | ✔ | ✔ 13 + total | ✔ | ✔ (none outside) | ✔ (M2) | ✔ (C4) |
| 1622 | Q2 | ✔ `…_Q2_1766453.pdf` / 56–58 / 57 | ✔ T2 | ✔ 15 + total | ✔ | ✔ | ✔ (M2) | ✔ |
| 2481 | Q1 | ✔ `…_Q1_1744517.pdf` / 35–36 / 36 | ✔ | ✔ 11 + total | ✔ (M3) | ✔ (interest in fin.) | ✔ | ✔ |
| 2481 | Q2 | ✔ `…_Q2_1766407.pdf` / 40–41 / 41 | ✔ T2 | ✔ 11 + total | ✔ (M3) | ✔ | ✔ | ✔ |
| 2483 | Q1 | ✔ `…_Q1_1745002.pdf` / 60–61 / 60 | ✔ | ✔ 10 + total | ✔ | ✔ | ✔ | ✔ |
| 2483 | Q2 | ✔ `…_Q2_1764242.pdf` / 65–67 / 65 | ✔ T2 | ✔ 10 + total; C1 = 5 is a documented source defect | ✔ | ✔ | ✔ | ✔ |
| 2488 | Q1 | ✔ `…_Q1_1745649.pdf` / 35–36 / 36 | ✔ | ✔ 7 + total (labels repaired from broken `נ` glyph, match image) | ✔ | ✔ | ✔ | ✔ |
| 2488 | Q2 | ✔ `…_Q2_1766252.pdf` / 80–82 / 81 | ✔ T2 | ✔ 7 + total | ✔ | ✔ | ✔ | ✔ |
| 2524 | Q1 | ✔ `…_Q1_1744218.pdf` / 29 / 29 | ✔ | ✔ 8 + total | ✔ | ✔ | ✔ | ✔ |
| 2524 | Q2 | ✔ `…_Q2_1765965.pdf` / 31 / 31 | ✔ T2 | ✔ 8 + total | ✔ | ✔ | ✔ | ✔ |

### Evidence highlights, value by value (all read on my own images)

**111 Q2, p.16**
- Lines:
  - 1,410 | – | 1,136
  - 613 | \*23 | 281
  - 1,109 | \*702 | 775
  - – | \*422 | 422
  - – | \*(250) | (642)
  - (1,562) | blank | –
  - (93) | (145) | (254)
- Total 1,477 | 752 | 1,718.
- (\*) `ריבית ששולמה` (operating): blank | – | (181).
- Footnote `* סיווג לא מהותי במספרי השוואה` is attached to the 6M-2025 values, which justifies `(מוצג מחדש)` under conventions §10.

**400**
- Q1 total 94,769 | 102,330 | 231,590. Credit 42,608 | (45,991) | 48,111.
- Q2 total 224,519 | 163,447 | 129,750 | 61,117 | 231,590.
- (\*) interest:
  - Q1: (7,626) | (8,646) | (43,106);
  - Q2: (25,149) | (20,099) | (17,523) | (11,454) | (43,106).

**539**
- Q1 total (305) | 73,424 | 187,216.
- Q2 total 85,298 | 145,422 | 85,603 | 71,997 | 187,216. Treasury-share blanks in the 2025 columns are 0.
- Mapping of `הנפקת מניות` → **2** verified in the report:
  - statement of changes in equity, p.52: `מימוש אופציות שהונפקו בחבילה` 26,050 + `מימוש אופציות תשלום מבוסס מניות` 25 = 26,075;
  - consolidated notes, p.58, item ג: exercise of the package warrants by Clal, about 26 million ש"ח.
- `הנפקת חבילה` → 1 (conventions §6).

**1083**
- Q1 total 32,469 | 126,680 | 254,247; ST credit 12,501 | (47,800) | (249).
- Q2 total 13,805 | 97,244 | (18,664) | (29,436) | 254,247.
- (\*) operating interest:
  - Q1: (2,478) | (1,374) | (17,849);
  - Q2: (18,591) | (8,844) | (16,113) | (7,470) | (17,849).
- Appendix `ב) ריבית ששולמה והוונה למלאי`, printed positive:
  - Q1: 2,709 | 3,798 | 23,751;
  - Q2: 9,476 | 11,686 | 6,767 | 7,888 | 23,751.
- Info-row sums checked: −5,187, −5,172, −41,600, −28,067, −20,530, −22,880, −15,358, −41,600.

**1502**
- All financing and interest cells are `-`.
- Units `אלפי דולר ארה"ב`.

**1553**
- Q1: project loans 93,594 | (157,926) | 250,082; total 110,097 | 83,200 | 434,780.
- Q2: total 44,125 | 147,375 | (65,972) | 64,175 | 434,780; dividend (5,000) in 6M-26 and 3M-26.

**1622**
- Q1 total (67,874) | (88,489) | (62,271).
- Q2 total (78,280) | (172,833) | (10,406) | (84,344) | (62,271).
- `החזר הון לזשמ"ש` in Q2 April–June 2026 is printed **+1,500** and recorded as printed; it is documented in חסרים והערות.

**2481**
- Q1 total 190,336 | 24,982 | 8,951.
- Q2 total 235,772 | 137,994 | 45,436 | 113,012 | 8,951.

**2483**
- Q1 total (221,931) | 86,478 | 483,669.
- Q2 total (289,660) | 178,093 | (67,729) | 91,614 | 483,669.
- Q2 April–June 2026: ST credit printed (18,489); the lines sum to (67,724).

**2488**
- Q1 total 4,063 | 11,677 | 27,745.
- Q2 total 13,621 | 18,641 | 9,558 | 6,962 | 27,745.

**2524**
- Q1 total 185,631 | 17,198 | 62,201.
- Q2 total 178,115 | 57,097 | (7,515) | 39,899 | 62,201.
- `שינוי בבעלי עניין` → `אחר` verified: in the consolidated balance sheet (Q1 p.24) `בעלי עניין` appears **only in assets** (current 2,807; non-current 2,001), so the line is lending to interested parties and fits none of items 1–14.

### Mapping decisions reviewed (all acceptable, all documented)

**Gross lines without a stated term (rule A / R3)**
- 111: `קבלת/פירעון הלוואה מאחרים` → 5, because the balance sheet shows `הלוואות לזמן קצר`.
- 111: `פירעון הלוואה מצד קשור` → 7, a 78-month owner loan (note 3א).
- 1622: `קבלת/פרעון הלוואות מבעל שליטה` → 5, a current liability.
- 1622: `קבלת הלוואות מ-Extell Holdings I LLC` → 4, note 7ט, due 2033.
- 2488: bank/other loans → 4/7.

**Net borrowing lines and related-party advances (R3 / conventions §5)**
- 1553: project loans net → 5; LT bank loans net → 4/7 by sign.
- 1622: Extell Holdings I advances → 5.
- 2483: controlling-shareholder loans net → 5.
- 2488: related-party loans net → 5.
- 2524: `שינוי בהלוואה מאחרים` → 5.

**Other conventions**
- 1622: EB-5 → 7 (§3).
- 1622: NCI capital return → 12.
- 1622: derivatives → אחר (§7).
- 2483: purchase of shares of a consolidated company from the controlling shareholder → 14.
- 1622: interest and loan costs → 13, with a note.

**Consistency across reports:** the same line gets the same item in Q1 and Q2 for every company.

---

## 3. Issues

None of these is blocking.

**M1 – 1083 Q1 and Q2: appendix (\*) line recorded with flipped sign, line-level note missing (minor, documentation).**
- Where: `מיפוי שורות` line `ב) ריבית ששולמה והוונה למלאי`.
  - Q1, p.50: −2,709 | −3,798 | −23,751.
  - Q2, p.51: −9,476 | −11,686 | −6,767 | −7,888 | −23,751.
- Printed: positive (no parentheses).
- R5 and conventions §1 say "sign as printed". The deviation is deliberate, so that the (\*) info row (operating + appendix) is a meaningful total.
- It is documented in:
  - the (\*) row note of `פירוט מימון` ("…מודפס ללא סוגריים ונרשם כאן בסימן תשלום (שלילי)…");
  - master `הסבר` B34, which names 121 and 1083.
- The note on the mapping-sheet line itself (and on the master `מיפוי שורות` rows) says only "גילוי בנספח… הסעיף לא צוין". A reader comparing that line with the PDF sees a sign mismatch with no explanation on the line.
- Recommendation: append the sign remark to that line's note. No value change is needed. I accept the design (a literal "as printed" sum would give a meaningless +231).

**M2 – Notes in `מקורות` and the master `אינדקס קבצים` mislabel board-report pages as 38D separate data (minor, documentation).**
- 400 Q1: "נתונים כספיים נפרדים (תקנה 38ד) – עמ' 16, 44–45". p.16 is the board report's §3 "נזילות".
- 400 Q2: "עמ' 19, 48–49". p.19 is likewise the board report.
- 1622 Q1/Q2: "עמ' 11" and "עמ' 13" are the board report's §4 "גילוי בהתאם לסעיף 10(ב)(14)". This one is borderline.
- These are not-used pages, so there is no data impact.

**M3 – 2481: `פירעון הלוואות מבעל/י עניין` → 7 while `קבלת הלוואות מבעל עניין לזמן קצר` → 5 (judgment call, documented; flagged for Phase-C awareness only).**
- Q1 FY: (73,255). Q2: (40,000) 6M-25, (30,000) 3M-25, (73,255) FY.
- The evidence given for 7 is:
  - the solo statements present these repayments as `פירעון הלוואות מצדדים קשורים לזמן ארוך`;
  - the balance sheet classifies the lender balances long-term.
- If part of the repayment repays the 58,973 short-term receipt, items 5 and 7 are both overstated in FY-2025 and 2025 Q2. The totals are unaffected.
- This is consistent with rule A as written, so it is not a defect.

**Cosmetic screenshot remarks (no action required; pilot design A1).**
- **C1:** the (\*) interest line on full-page images 111 s02, 400 s02 and 400 s06 (and on 539 context pages s05/s09) is not red-framed. The captions point to the dedicated red (\*) crops, which exist and are correct.
- **C2:** the (\*) crops for 1083 (s04, s10), 1502 (s04, s09) and 1553 (s04, s08) show a sliver of the neighbouring row.
- **C3:** 400 s07: the second label line of the total is slightly clipped; the digits are unaffected.
- **C4:** the edge of the blue frame:
  - 1502 Q1 (s02/s03): it runs through the units line;
  - 1622 Q1 (s02): it runs through the `מבוקר` row.

**T1 – Tooling note for Phase C / the final Inspector.** `validate.py --issuers <subset>` **without** `--no-master` gives ~778 AC11 FAILs: "נתונים rows 648 == periods 83", followed by row-by-row misalignment. Master mode compares the whole master with the subset. This is a tool artefact, not a deliverable defect. My own field-by-field comparison of master versus company workbooks for these 11 issuers found 0 differences. Run master checks without `--issuers`.

---

## 4. Cross-report checks (C2/C3)

I recomputed them from the PDFs.

| Issuer | C2 2026 | C2 2025 | C3 (FY-2025, total + each item) | Explanation in `חסרים והערות` |
|---|---|---|---|---|
| 400 | 94,769 = 224,519 − 129,750 ✔ | 102,330 = 163,447 − 61,117 ✔ | ✔ | (\*) interest 6M-25 rounding 1, info row only: ROW33 ✔ |
| 539 | (305) = 85,298 − 85,603 ✔ | 73,424 vs 73,425: **−1** | ✔ | ROW85 (total) + ROW84 (item 5) ✔ |
| 1083 | 32,469 = 13,805 + 18,664 ✔ | 126,680 = 97,244 + 29,436 ✔ | ✔ | – |
| 1502 | 0 ✔ | 0 ✔ | ✔ | Q1 heading-as-total: ROW45 ✔ |
| 1553 | 110,097 = 44,125 + 65,972 ✔ | 83,200 = 147,375 − 64,175 ✔ | ✔ | – |
| 1622 | (67,874) ✔ | (88,489) ✔ | ✔ | +1,500 printed: ROW49 ✔ |
| 2481 | 190,336 = 235,772 − 45,436 ✔ | 24,982 = 137,994 − 113,012 ✔ | ✔ | – |
| 2483 | (221,931) ✔ (item 5 diff 5 explained) | 86,478 vs 86,479: **−1** | ✔ | ROW62/144/180 (C1 = 5), ROW145–147 ✔ |
| 2488 | 4,063 ✔ | 11,677 vs 11,679: **−2** (related-party loans +31, interest −30, credit +1) | ✔ | ROW154–156 ✔; 2025 comparatives updated outside financing: ROW64 ✔ |
| 2524 | 185,631 vs 185,630: **+1** | 17,198 ✔ | ✔ | ROW166–167 ✔ |

111 has no Q1 report, so C2/C3 are not applicable; this is listed in ROW2.

Every mismatch is explained in the master `חסרים והערות` and also in `builder-report-1.md`.

---

## 5. Conclusion

**Batch 4 verdict: PASS.**

- All 21 reports use the correct source file and the consolidated statement, with correct pages.
- Every period, value, sign, unit and (\*) amount was confirmed on images I actually saw.
- The company workbooks, the master rows (including the T1 flag) and the screenshots PDFs are consistent with each other and with the sources.
- The minor items M1–M3 and the cosmetic remarks C1–C4 do not affect any number.

Assisted-by: Anthropic:Claude Opus 5.5
