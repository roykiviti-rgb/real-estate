# Batch 5 — Phase B report (iteration 1)

Builder: Phase B batch 5. Date: 2026-11-10. Protocol: `work\PIPELINE.md` §0–§13 + `work\phaseB-conventions.md`.
Scope: 11 companies / 21 reports — 341, 425, 1193, 1703 (Q2 only), 1928, 1979, 2371, 2385, 2456, 2478, 2520.

**Result:** all 21 reports verified against rendered images; all 11 companies built without `--draft`.
`checks.py` over the 11 issuers: C1 82 OK + 1 MISMATCH (explained), C2 17 OK + 3 MISMATCH (explained),
C2-item 8 INFO (all explained), C3 160 OK, **unexplained mismatches: 0**.
`validate.py --issuers <iss> --no-master`: **FAIL 0 for 10 companies**. 2478 has **FAIL 1**: the per-column AC6
check of a documented ±1 source-rounding column. validate.py ignores C1 explanations there, so this cannot be
cleared without a plug value (SCRIPT-ISSUE 1).

Verification method (as originally written; **superseded – see the section "Re-check after the image-cap issue" at
the end**: in the first pass the `view` tool did not display the images of 19 of the 21 reports): `tool_review.py`.
- The 220-DPI `fin_*.png` (header strip + financing section, numbered line frames) was compared against
  `lines_*.txt` line by line and digit by digit. This covered the line text, every value and sign, dashes and blank
  cells, the column headers (period, length, end date, audit status) and the units/currency.
- The 100-DPI `page_*.png` of every statement page was read for (*) lines outside financing and for the statement
  boundaries.
- `outside_*.png` 220-DPI crops were checked for every (*) line.
- Text-layer searches (own helper scripts in `%TEMP%\fcf_run\341\`) were used only to locate notes, balance-sheet
  classifications and bboxes. Every value was confirmed on the image.
- After each build, the screenshots PDF was rendered with `tool_shots.py` and viewed: captions, orange/blue/red
  boxes, zoom legibility and units in the crop.

---------------------------------------------------------------------------------------------------------------

## 341 שדה נדל"ן-י.ש. בע"מ — USD

- **Sources:**
  - Q1: `341_שדה נדל_ן-י.ש. בע_מ_2026_Q1_1745548.pdf` (59 pp). Consolidated statement 'דוחות על תזרימי המזומנים ביניים מאוחדים' pp. 41–42; financing p. 42.
  - Q2: `..._Q2_1767508.pdf` (83 pp). pp. 47–48; financing p. 48.
  - Separate data (Q1 p. 56, Q2 p. 62) not used.
- **Columns:** Q1 3M 31.3.2026 / 3M 31.3.2025 / FY 2025. Q2 6M/6M/3M (אפריל–יוני)/3M (אפריל–יוני)/FY. None restated.
- **Units/currency:** `אלפי דולר` → דולר ארה"ב, אלפים. USD presentation confirmed in the notes ("אלפי דולר ארה"ב").
- **Mapping:**
  - `תקבולים מגיוס משקיעים בניכוי הוצאות גיוס` → **6**. The extractor left it as אחר. The investors are the limited partners of the group's raising partnerships (definitions, Q1 p. 4); the statements of changes in equity credit the raising to the NCI column (conv. §2). In Q1 and in all 2025 columns the equity amounts equal the cash-flow line; in the Q2 2026 columns the equity statements show 7,233 (6M) / 4,447 (3M) against 8,239 / 5,453 in the cash-flow line, a difference of 1,006 that the report does not explain. This was found in the re-check; the Q2 line note now says so. The first-pass note wrongly said "entirely to NCI".
  - `קבלת (פרעון) הלוואה לזמן קצר מבעל שליטה` → 5.
  - `פרעון התחייבות אחרת` and `תשלום התחייבות אחרת` → **אחר**. This is an undescribed non-current "התחייבות אחרת" (balance 32 at 31.3.2025/30.6.2025, 0 at 31.12.2025). It is not presented as a loan, bond or lease. The same payment (67) appears on two different lines (2025 interim vs FY column).
  - `פרעון הלוואות בערבות מדינה` → **7** (state-guaranteed loans, gross repayment).
  - Bank LT loans (net of costs) → 4/7.
  - ST loans, both lines → 5.
  - Warrant exercise → 2. Share issue → 1. Bond issue (Q2 36,326) → 3. Lease → 10. NCI distributions → 12.
- **(*):** `ריבית ששולמה במזומן` in operating (Q1 p. 41, Q2 p. 47) → info row 'פעילות שוטפת'. No dividends paid to owners.
- **Overrides:**
  - `line_items` and `line_notes` as above.
  - Q1 `header_page: 41` + `boxes.41.header`. The financing page p. 42 repeats the headers without the units line, so the zoomed crop now carries `אלפי דולר` (R7.2).
  - Q2 `columns.c2/c4.header_text` (the auto text was truncated).
  - `report_notes`.
- **Checks:** C1 8 OK, C2 2 OK, C3 16 OK.
- **Source issues:** none. Blank cell in Q1 `תשלום התחייבות אחרת` (3M 2026) → 0, confirmed on the image.
- **validate:** PASS 337 / FAIL 0.

## 425 צבי צרפתי ובניו השקעות ובנין (1992) בע"מ

- **Sources:**
  - Q1: `..._Q1_1744485.pdf` (100 pp). Consolidated statement 'דוחות מאוחדים על תזרימי המזומנים' pp. 73–74; financing p. 73.
  - Q2: `..._Q2_1766510.pdf` (113 pp). pp. 84–86; financing p. 85.
  - **Confirmed consolidated (Phase A's correction is right):** the separate 38D data 'נתונים על תזרימי המזומנים' (Q1 pp. 91–92, Q2 pp. 104–105, footer 'המידע הכספי הנפרד') is not used.
- **Columns:** 3 / 5 standard, none restated. Columns c2 (Q1) and c2/c4 (Q2) carry a column note: '(*) הוצג מחדש' (note 2ד, staff position 11-6 on urban renewal) marks only operating cells.
- **Units:** אלפי ש"ח.
- **Mapping:** all standard. Share issue → 1. Bond issue/repayment → 3/8. Dividend → 11. `קבלת הלוואה לזמן ארוך` → 4. `אשראי לזמן קצר, נטו` → 5.
- **(*):**
  - Interest paid is not a line in any section. It is disclosed only in 'נספח ב' – מידע נוסף' of the consolidated statement (Q1 p. 74: 5,296 / 4,354 / 41,717; Q2 p. 86), as positive amounts as printed.
  - Info note per conv. §1: `גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)`.
  - A report note records that the identical disclosure in the separate-company data is titled 'מידע נוסף על תזרימי מזומנים מפעילות שוטפת' (see mapping decision M8).
- **Overrides:** `line_notes`, `info_notes`, `column_notes`, `report_notes`. `columns.*.header_text` normalised in all columns: letter-spaced '2 0 2 6' and a stray '(המשך)' prefix in Q2 c2.
- **Checks:** C1 8, C2 2, C3 16 OK.
- **validate:** PASS 323 / FAIL 0.

## 1193 י.ח.דמרי בניה ופיתוח בע"מ

- **Sources:**
  - Q1: `..._Q1_1744429.pdf` (68 pp). 'דוחות תמציתיים מאוחדים על תזרימי המזומנים' pp. 39–41 (financing p. 40; p. 41 = non-cash appendix).
  - Q2: `..._Q2_1764665.pdf` (73 pp). pp. 42–44 (financing p. 43).
  - Separate data (Q1 pp. 61–63, Q2 pp. 66–68) not used.
- **Columns:** 3 / 5 standard. **Units:** אלפי ש"ח.
- **Mapping:**
  - `תמורה מהנפקת מניות ואופציות ומימושי אופציות למניות, בניכוי הוצאות הנפקה` → **1**. The extractor suggested 2. This is an unsplit shares + options line (conv. §6). Appendix A states that option exercises were net, with no proceeds.
  - Others standard: ST bank credit net → 5, LT loans → 4/7, bonds → 3/8, dividend → 11.
- **(*):** **the extractor missed** `תשלומי ריבית` in operating (Q1 p. 39: (44,497)/(39,467)/(213,780); Q2 p. 42: 5 columns). Added via `outside_add` with bboxes from the text layer and confirmed on the image. No dividend paid outside financing.
- **Overrides:**
  - `line_items`, `line_notes`, `outside_add`, `report_notes`.
  - `context_sections`: the appendix pages 41/44 were captioned 'פעילות השקעה'. They are now 'פעילויות שלא במזומן'.
- **Checks:** C1 8, C2 2, C3 16 OK.
- **validate:** PASS 326 / FAIL 0.

## 1703 קבוצת אחים יעקובי (ואי.אס.בי) בע"מ — Q2 only

- **Sources:** Q2 `..._Q2_1767724.pdf` (43 pp). 'דוחות מאוחדים תמציתיים ביניים על תזרימי המזומנים' pp. 31–32; financing p. 32.
  - `-01` (67 pp) = BDO valuation of YSB's holding in BlueGen. Not a source (`מקורות` role 'נספח – שומה/הערכת שווי').
  - Workbook header: 'דוח Q1 2026 אינו קיים בתיקייה'.
- **Columns:** 6M 30.6.2026 / 6M 30.6.2025 / FY 2025. The statement has no 3-month columns. **Units:** אלפי ש"ח.
- **Mapping:**
  - `אשראי לזמן קצר מתאגידים בנקאיים ומאחרים, נטו` → 5.
  - `קבלת הלוואה מצד קשור` → **4**: gross receipt, no term, no separate balance-sheet line; R3 includes related parties.
  - LT loans → 4/7. Lease → 10.
- **(*):** `ריבית ששולמה` in operating (p. 31) → info row. No dividends paid. Investing 'דיבידנד מחברה המטופלת…' is a receipt.
- **Overrides:** `line_notes`, `report_notes`, `columns.*.header_text` (letter spacing).
- **Checks:** C1 3 OK (C2/C3 not applicable).
- **validate:** PASS 136 / FAIL 0.

## 1928 רימון שירותי ייעוץ וניהול בע"מ — repaired font

- **Sources:**
  - Q1: `..._Q1_1743933.pdf` (59 pp). 'דוחות תמציתיים מאוחדים על תזרימי המזומנים' pp. 32–33; financing p. 33.
  - Q2: `..._Q2_1766226.pdf` (64 pp). pp. 36–37; financing p. 37.
  - Separate data not used.
- **Columns:** confirmed on the image. Q1 c1 (3M 31.3.2026) and c3 (FY 2025) had been inferred, flag `הוסקו`/`הונח`.
- **Units:** `אלפי ש"ח` in every column header. The auto units text had lost its quotes (`אלפי שח`) and was fixed; one column read `אלפי ח"ש` (mirrored) and was fixed.
- **Text layer:** broken `נ` glyph. Every repaired label was compared with the image; all match.
- **Mapping:**
  - `רכישת מניות מהמיעוט` → 14.
  - `תמורה ממימוש אופציות לעובדים` → 2.
  - `דיבידנד ששולם לבעלי זכויות המיעוט` → 12.
  - ST bank loans net → 5. LT bank loans → 4/7. Bonds → 8.
  - `קבלת הלוואה מנותני אשראי אחרים` → **4** (the extractor suggested 5). Gross receipt, no term. On the balance sheet, other credit providers appear only in non-current loans ('הלוואות מתאגידים בנקאיים ונותני אשראי אחרים'); current credit is from banks only.
- **(*):** `ריבית ששולמה` in operating → info row.
- **Overrides:** `units`, `columns.*.header_text`, `line_items`, `line_notes`, `report_notes`, `text_layer: usable (repaired)`.
- **Checks:** C1 8, C2 2, C3 16 OK. Blank cells in Q2 bond repayment (2025 columns) → 0, confirmed.
- **validate:** PASS 328 / FAIL 0.

## 1979 אפי קפיטל נדל"ן בע"מ — C2 differences

- **Sources:**
  - Q1: `..._Q1_1742790.pdf` (74 pp). 'תמצית דוחות על תזרימי המזומנים ביניים מאוחדים' pp. 52–53; financing p. 53.
  - Q2: `..._Q2_1763668.pdf` (79 pp). pp. 55–56; financing p. 56.
  - The earlier block (Q1 pp. 20–21, Q2 pp. 22–23) is the board-report liquidity table. Separate data (pp. 67–68 / 72–73) not used.
- **Columns:** standard. **Units:** אלפי ש"ח.
- **Mapping:**
  - Banks and financial institutions loans, gross receipt/repayment with no term → 4/7. The balance sheet has both current and non-current balances.
  - Bonds → 3/8. Options → 2. Lease → 10. Interest → 13. Dividend → 11.
  - `פירעון הלוואות מצדדים קשורים ומאחרים` (Q2) → 7.
  - Text-layer artefact `יפרעון` → `פירעון`, fixed by `line_text` (Q1 line 2; Q2 lines 2 and 4).
- **(*):** interest and dividends paid only in financing → info rows 0.
- **C2 (genuine differences between the reports, values re-read on both images):**
  - **2026: −4,872.**
    - Q1 total 11,486 vs Q2-derived 16,358 (41,513 − 25,155).
    - Loans received: Q1 76,933 vs derived 80,317, a difference of −3,384.
    - Interest: Q1 (32,217) vs derived (30,729), a difference of −1,488.
    - The Q2 report also shows different Q1-2026 operating/investing figures and closing cash at 31.3.2026 of 87,561 (Q1: 87,549).
  - **2025: +3,732.**
    - Q1 total 256,726 vs derived 252,994 (295,508 − 42,514).
    - The whole difference is interest paid (Q1 (29,521) vs derived (33,253)). It is offset in operating (Q1 (155,339) vs derived (151,607)), i.e. a reclassification of interest between operating and financing.
    - Items 4/7 also differ by ±1,580 (a related-party repayment shown in the Q2 report's Apr–Jun 2025 column only); the net is identical.
  - No note in either report explains this. Explained in `overrides\1979_checks.json` (2 C2 + 5 C2-item keys) and in column notes c1/c2 of both reports.
- **Checks:** C1 8 OK, C2 2 MISMATCH explained, C2-item 5 INFO explained, C3 16 OK.
- **validate:** PASS 326 / FAIL 0.

## 2371 בית וגג יזמות ונדל"ן בע"מ

- **Sources:** Q1 `..._Q1_1742688.pdf` p. 45 (one-page statement 'תמצית דוחות על תזרימי המזומנים ביניים מאוחדים'). Q2 `..._Q2_1765823.pdf` p. 52.
- **Columns:** standard. 2025 columns: '*' restatement marks (note 3ב) on operating lines only → column notes, not restated.
- **Units:** אלפי ש"ח.
- **Mapping:** `הנפקת אגרות חוב, נטו` → 3. `קבלת (פרעון) אשראי לזמן קצר` / `קבלת אשראי לזמן קצר` → 5. `פרעון חכירה` → 10. `חלוקות לזכויות שאינן מקנות שליטה` → 12.
- **(*):** `ריבית ששולמה` in operating → info row.
- **Overrides:** `line_notes`, `column_notes`, `report_notes`, header texts (Q1 c1 truncated, Q2 c5 spacing).
- **Checks:** C1 8, C2 2, C3 16 OK.
- **validate:** PASS 316 / FAIL 0.

## 2385 עמרם אברהם חברה לבנין בע"מ

- **Sources:**
  - Q1: `..._Q1_1745346.pdf` (104 pp). 'דוחות מאוחדים ביניים על תזרימי המזומנים' pp. 67–69; financing p. 68.
  - Q2: `..._Q2_1767833.pdf` (107 pp). pp. 73–76; financing p. 74.
  - **Q2 `-01` (PPA valuation) is not a source.** Separate data not used.
- **Columns:** standard. **Units:** אלפי ש"ח.
- **Mapping:**
  - `שינוי באשראי לזמן קצר מבנקים ואחרים, נטו` → 5.
  - Bonds → 3/8. Share issue → 1. LT loans → 4/7.
  - `השקעות בעלי זכויות שאינן מקנות שליטה` → 6.
  - Loans **from** equity-accounted companies (gross receipt / repayment lines) → 4/7. Balance-sheet line 'הלוואות מחברות המטופלות בשיטת השווי המאזני' is non-current.
  - `קבלת (פרעון) הלוואה מבעלי זכויות שאינן מקנות שליטה` → **5** (the extractor suggested 6). It is a loan, not equity, and is presented net with no term in the line (R3). The balance sheet shows it as non-current; this is noted (see M3).
  - Q2 `חלוקת תשואה לזכויות שאינן מקנות שליטה` → **12** (the extractor suggested 6).
- **(*):** `ריבית ששולמה` in operating (adjustments section) → info row. Appendices (non-cash, first consolidation, disposal, loss of control) are not financing.
- **Overrides:** `line_items`, `line_notes`, `report_notes`, header texts (letter spacing, '(המשך)').
- **Checks:** C1 8, C2 2, C3 16 OK.
- **validate:** PASS 335 / FAIL 0.

## 2456 שמואל ברוך יזמות ובניה בע"מ — title without 'מאוחד'

- **Sources:** Q1 `..._Q1_1742581.pdf` (49 pp) pp. 40–41, financing p. 41. Q2 `..._Q2_1766214.pdf` (59 pp) pp. 50–51, financing p. 51.
- **Consolidated:** the title is 'דוח תמציתי על תזרימי המזומנים'. It is the consolidated statement:
  - the board report refers to 'דוחות על תזרימי המזומנים המאוחדים';
  - the notes refer to 'הדוחות הכספיים ביניים תמציתיים / מאוחדים אלה';
  - the company has subsidiaries;
  - the file has no other cash-flow statement (no separate data).
  Recorded in `report_notes`.
- **Columns:** standard. **Units:** `אלפי ₪` → ש"ח, אלפים.
- **Mapping:**
  - Banks and financial institutions loans, gross → 4/7. The balance sheet has current and non-current balances.
  - `קבלת הלוואות מצדדים קשורים` → **5**. Every printed value in this "receipt" line is negative ((200), (565), (365)), so the line is the net movement of related-party loans. It has no term and there is no such balance on the balance sheet (R3: net without term).
  - Bonds → 3, Q2 `(פרעון) אגרות חוב` → 8. Shares → 1. Lease → 10. `ריבית ששולמה במזומן` → 13.
  - Mirrored apostrophe in `(סדרה א')` fixed.
- **(*):** interest paid only in financing; no dividends.
- **Checks:** C1 8, C2 2, C3 16 OK.
- **validate:** PASS 325 / FAIL 0.

## 2478 רייסדור יזמות בע"מ — C2 14,540, C3 4/5, C1 ±1

- **Sources:**
  - Q1: `..._Q1_1743625.pdf` (95 pp). 'דוחות מאוחדים על תזרימי המזומנים' pp. 37–38; financing p. 38.
  - Q2: `..._Q2_1766702.pdf` (47 pp). pp. 38–39; financing p. 39. Separate data p. 41 not used.
- **Columns:** standard, none flagged restated (conv. §10):
  - Q1: note 1ו (restructuring under common control, pooling) marks '(*) הוצג מחדש' only on the balance sheet and equity statements (pp. 32–36). Column note on c2.
  - Q2: '(*) הוצג מחדש' marks only two operating line labels. Column notes on c2/c4/c5.
- **Units:** אלפי ש"ח.
- **Mapping:**
  - **C3 4/5 aligned:** `קבלת הלוואות מתאגידים בנקאיים ואחרים, נטו` (Q1) and `קבלת (פירעון) הלוואות מתאגידים בנקאיים ואחרים, נטו` (Q2) → both **5** (net, no stated term, banks and others; R3 / PIPELINE §7). C3 is now 16 OK.
  - `הנפקת אג"ח, נטו` → 3. Dividend → 11. Lease → 10. Interest → 13.
- **(*):** interest and dividends only in financing; operating shows taxes only under 'מזומנים ששולמו…'.
- **C1:** Q2 c3 (3M Apr–Jun 2026) lines sum to −76,054 vs printed total −76,053. This is source rounding; the printed values are kept. Recorded in `issues`, the c3 column note and `2478_checks.json`. Lease c4 = **+186** printed without parentheses, kept as printed (= (861) − (1,047)).
- **C2 2025: +14,540.**
  - Q1 75,953 vs Q2-derived 61,413 (281,707 − 220,294).
  - Loans: 88,177 vs 74,954 (13,223). Interest: (11,177) vs (12,494) (1,317).
  - The cash change for the quarter is identical ((21,449)). The difference is offset in operating (−14,298) and investing (−242).
  - The Q2 report re-presents the 2025 comparatives ('(*) הוצג מחדש'); the reports give no detail for financing. Explained in `2478_checks.json` and column notes.
  - C2-item 2026 interest −1 follows from the c3 rounding.
- **Checks:** C1 7 OK + 1 MISMATCH explained. C2 1 OK + 1 MISMATCH explained. C2-item 3 INFO explained. C3 16 OK. 0 unexplained.
- **validate:** **PASS 319 / FAIL 1**: `AC6 C1 דוח Q2 2026 | 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני)`, which is the documented source rounding (SCRIPT-ISSUE 1). The aggregate check line passes: 'AC6/AC8 C1–C3 … unexplained mismatches=0'.

## 2520 איסתא נכסים בע"מ

- **Sources:**
  - Q1: `..._Q1_1742735.pdf` (56 pp). 'דוחות תמציתיים מאוחדים על תזרימי מזומנים' pp. 30–31; financing p. 30.
  - Q2: `..._Q2_1765451.pdf` (61 pp). pp. 32–33; financing p. 32.
  - **Q2 confirmed consolidated (Phase A's correction is right):** separate data 38D pp. 55–56 not used. Q1 separate data pp. 50–51 not used.
  - **`-01` files (both quarters) = statements of the investee סלע איסתא נדל"ן ישראלי → not a source.**
- **Columns:** standard. **Units:** אלפי ש"ח.
- **Mapping:**
  - Bank ST credit net → 5. LT bank loans → 4/7.
  - `קבלת הלוואות מאחרים` → 4. Balance sheet: non-current 'הלוואות מאחרים'.
  - `ריבית ששולמה` → 13. Bonds → 3. `תשלומים בגין חכירה` → 10. NCI dividend → 12.
  - `קבלת/פירעון אשראי מהחברה האם ובעלי מניות אחרים` → **4/7** (the extractor suggested 5). Gross receipt/repayment lines; the balance sheet presents 'הלוואות מהחברה האם ובעלי מניות אחרים' as non-current.
  - Q2 c3 repayment line printed **positive 14,913**, kept as printed in item 7 (column note).
- **(*):** interest in financing only; investing 'ריבית שהתקבלה' is a receipt → info rows 0.
- **Overrides:**
  - `line_items`, `line_notes`, `column_notes`, `report_notes`.
  - `context_sections`: captions of p. 31/33 and p. 30/32.
  - `boxes.<p>.header` with a tightened bottom edge: the auto header strip included a sliver of the first operating heading.
- **Checks:** C1 8, C2 2, C3 16 OK.
- **validate:** PASS 332 / FAIL 0.

---------------------------------------------------------------------------------------------------------------

## Mapping decisions (cross-company judgement calls for Phase C to align)

- **M1 – unsplit shares + options line** (1193 'תמורה מהנפקת מניות ואופציות ומימושי אופציות למניות, בניכוי הוצאות הנפקה') → 1 (conv. §6), with a note.
- **M2 – gross loan lines with no stated term → 4/7, decided from the balance sheet:**
  - 2520 'קבלת/פירעון **אשראי** מהחברה האם ובעלי מניות אחרים'. The line says "אשראי" but the balance is a non-current loan.
  - 1928 'קבלת הלוואה מנותני אשראי אחרים'. Others appear only in non-current loans.
  - 2385 loans from equity-accounted companies (non-current).
  - 1703 'קבלת הלוואה מצד קשור'.
  - 1979 and 2456 bank and financial-institution loans, where the balance is partly current (construction loans).
  - Other batches may have sent similar gross lines to 5; Phase C should align.
- **M3 – net loan lines with no stated term → 5 even when the balance sheet shows the balance as non-current:**
  - 2385 'קבלת (פרעון) הלוואה מבעלי זכויות שאינן מקנות שליטה' (not 6 – it is a loan);
  - 2456 'קבלת הלוואות מצדדים קשורים' (all printed values negative, i.e. a net movement);
  - 2478 banks-and-others net line (also needed to align C3).
  - R3 wording followed literally; noted in each line note.
- **M4 – investor/partner capital in subsidiaries:** 341 'תקבולים מגיוס משקיעים בניכוי הוצאות גיוס' → 6. The investors are limited partners in the group's raising partnerships (conv. §2); the equity statement credits the raising to NCI (in the Q2 2026 columns 1,006 less than the cash-flow line – unexplained in the report, noted).
- **M5 – undescribed "other liability" payments:** 341 'פרעון התחייבות אחרת' / 'תשלום התחייבות אחרת' → אחר. Not presented as a loan, bond or lease.
- **M6 – state-guaranteed loans:** 341 'פרעון הלוואות בערבות מדינה' → 7.
- **M7 – NCI distributions labelled 'חלוקת תשואה'** (2385 Q2) → 12.
- **M8 – interest paid disclosed only in an appendix that does not name the section** (425 'נספח ב' – מידע נוסף'):
  - Used conv. §1 'הסעיף לא צוין (לא בפעילות מימון)'.
  - Evidence that it is operating: the same disclosure in the separate data is titled '…מפעילות שוטפת', and the consolidated statement has no interest line in investing or financing. Recorded in a report note.
  - Phase C may prefer 'נכלל בפעילות שוטפת'.
- **M9 – restatement marks outside the financing section** (2371, 425, 2478 Q2) or only in other statements (2478 Q1, note 1ו) → column notes, no '(מוצג מחדש)' (conv. §10).
- **M10 – consolidated statement whose title lacks 'מאוחד'** (2456): accepted on the evidence of the board report and notes, and because the file has no other statement; noted.

## Source irregularities (also in the overrides' `issues` / notes)

- 2478 Q2, 3M Apr–Jun 2026: printed lines sum to −76,054 vs printed total −76,053 (±1 rounding).
- 2478 Q2, 3M Apr–Jun 2025: lease repayment printed as +186.
- 2520 Q2, 3M Apr–Jun 2026: parent-loan repayment printed as +14,913.
- 2456: a "receipt" line printed with negative values in every column.
- 1979 and 2478: Q1-2025 / Q1-2026 figures differ between the Q1 and the Q2 report (C2), with no explanation in the reports.

## SCRIPT-ISSUEs

```
SCRIPT-ISSUE 1
  script:     validate.py (company_checks, line 90: ok(abs(sum(vals)+vo-vt) < 1e-6, "AC6 C1 ..."))
  report:     2478 Q2, column 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני)
  symptom:    validate.py --issuers 2478 --no-master → PASS 319 / FAIL 1
              "FAIL: [2478] AC6 C1 דוח Q2 2026 | 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני)".
              The source itself does not add up (lines −76,054 vs printed total −76,053).
              checks.py accepts the explanation (C1|2478|Q2 2026|…|total in 2478_checks.json) and the aggregate
              AC6/AC8 line passes with 0 unexplained mismatches, but the per-column AC6 check ignores explanations.
              Evidence: %TEMP%\fcf_run\_runs\validate_20261110-105658_4704\validate.txt
  expected:   goal AC6 allows a non-zero check when the source does not add up and it is documented.
              The per-column AC6 check should pass (or report INFO) when checks.explain() finds an explanation
              for that column. Phase A listed the same columns (715 ×4, 719 Q1, 2417 Q1, 2483 Q2, 2533 ×2, 531 Q2),
              so other batches will hit it too.
  workaround: none possible without a plug value (forbidden). Printed values kept; documented in issues, a
              column note and 2478_checks.json.
  severity:   blocks a clean validate (FAIL 1) for 2478 only; the deliverable itself is complete and correct.

SCRIPT-ISSUE 2
  script:     fcf_extract.py ((*) detection)
  report:     1193 Q1 and Q2
  symptom:    the operating line 'תשלומי ריבית' (interest payments) was not recognised as interest paid.
              The auto (*) info row was 0 with the note 'לא מוצג בנפרד בדוח תזרים המזומנים', which would have been
              wrong. No flag was raised.
  expected:   'תשלומי ריבית' (and probably 'תשלומי ריבית ומימון' etc.) should be detected like 'ריבית ששולמה'.
  workaround: outside_add with values and bbox from the text layer, confirmed on the image.
              Phase C may want to grep every report's operating/investing pages for 'תשלומי ריבית'.
  severity:   data (fixed in batch 5); possibly present in other batches' reports.

SCRIPT-ISSUE 3
  script:     fcf_extract.py (column header_text) → build_company.py row 'כותרת העמודה בדוח (מילולית)'
  report:     2371 Q1 c1, 2478 Q1 c1, 341 Q2 c2/c4, 1928 Q1/Q2, 425 Q2 c2, 2385 Q2 c1/c2, 2371 Q2 c5,
              letter-spaced headers in 425/1703/2385
  symptom:    the verbatim header shown in the workbook was truncated, for example
              'לתקופה של שלושה חודשים 2026', 'ל-3 החודשים שהסתיימו 2026', 'לתקופה של שישה חודשים שהסתיימה 2025'.
              Others carried the page's '(המשך)' title fragment, mirrored quotes 'אלפי ח"ש', missing spaces
              'לשנהשהסתיימה', or letter-spaced '2 0 2 6' / 'ל ש נ ה'. Months, end date and label were correct.
  expected:   complete header text per column.
  workaround: columns.cN.header_text overrides (checked against the page text and image).
  severity:   cosmetic, but visible in the deliverable.

SCRIPT-ISSUE 4
  script:     fcf_extract.py (units / header page choice) → fcf_render.py zoom crop
  report:     341 Q1 (units), 1928 Q1/Q2 (units text)
  symptom:    (a) 341 Q1: header_page = the financing page (p. 42), whose repeated column headers have no units
              line, so the zoomed crop showed no units (R7.2). The units 'אלפי דולר' are only on p. 41.
              (b) 1928: units_text 'אלפי שח' (quotes lost by the broken font).
  expected:   use the statement page that carries the units line; keep the quotes.
  workaround: (a) header_page 41 + boxes.41.header (y1 just above the first body heading);
              (b) units override 'אלפי ש"ח'.
  severity:   cosmetic / R7 compliance.

SCRIPT-ISSUE 5
  script:     fcf_extract.py (context_sections) and finalize_report.auto_geometry (header strip)
  report:     1193 Q1/Q2, 2520 Q1/Q2
  symptom:    (a) appendix pages with no cash-flow section (1193 p. 41 / p. 44, 'נספח א' – פעילות השקעה שאינה כרוכה
              בתזרים מזומנים') were captioned 'פעילות השקעה' in the screenshots PDF.
              (b) 2520: the blue header strip included the top sliver of the first operating heading.
  expected:   non-cash appendix pages captioned 'פעילויות שלא במזומן'; the header strip ends above the first body row.
  workaround: context_sections overrides; boxes.<p>.header with a tightened y1.
  severity:   cosmetic.

SCRIPT-ISSUE 6
  script:     fcf_extract.py (label text)
  report:     1979 Q1 line 2, Q2 lines 2 and 4; 2456 Q1 line 5
  symptom:    'יפרעון' instead of 'פירעון' (a stray glyph joined to the word); '(סדרה א)'' with a mirrored apostrophe.
  expected:   'פירעון …'; '(סדרה א')'.
  workaround: line_text overrides (checked against the image).
  severity:   cosmetic (verbatim text).
```

## Hygiene

- Only own files were written: `overrides\<iss>_Q1/Q2.json` (21), `overrides\1979_checks.json`,
  `overrides\2478_checks.json`, `data\<iss>_*.json` through `finalize_report.py`, the 2 × 11 company outputs through
  `build_company.py`, and this report and the progress file.
- No scripts or shared files were edited. No git. No Excel COM. No `build_master.py`.
- `validate.py` (scoped integrity) passed AC12 for every company: source PDFs unchanged, no stray files.
- `%TEMP%\fcf_run\<iss>\` deleted for the 11 issuers at the end. `_runs` was left for Phase C.

## Final status

| issuer | company | reports | status | validate (--no-master) |
|---|---|---|---|---|
| 341 | שדה נדל"ן-י.ש. | Q1, Q2 | verified + built | PASS 337 / FAIL 0 |
| 425 | צבי צרפתי ובניו | Q1, Q2 | verified + built | PASS 323 / FAIL 0 |
| 1193 | י.ח.דמרי | Q1, Q2 | verified + built | PASS 326 / FAIL 0 |
| 1703 | קבוצת אחים יעקובי | Q2 | verified + built | PASS 136 / FAIL 0 |
| 1928 | רימון | Q1, Q2 | verified + built | PASS 328 / FAIL 0 |
| 1979 | אפי קפיטל נדל"ן | Q1, Q2 | verified + built (C2 explained) | PASS 326 / FAIL 0 |
| 2371 | בית וגג | Q1, Q2 | verified + built | PASS 316 / FAIL 0 |
| 2385 | עמרם אברהם | Q1, Q2 | verified + built | PASS 335 / FAIL 0 |
| 2456 | שמואל ברוך | Q1, Q2 | verified + built | PASS 325 / FAIL 0 |
| 2478 | רייסדור | Q1, Q2 | verified + built (C1/C2 explained) | PASS 319 / FAIL 1 (documented source rounding – SCRIPT-ISSUE 1) |
| 2520 | איסתא נכסים | Q1, Q2 | verified + built | PASS 332 / FAIL 0 |

21 / 21 reports verified; 11 / 11 companies built (no draft).

---------------------------------------------------------------------------------------------------------------

## Re-check after the image-cap issue (orchestrator follow-up, 2026-11-10 11:16–11:50)

### 1. What my own tool results show

I re-read every `view` result of the first pass.
- From the first image view (1193 Q1 `fin_*.png`, ≈10:14) to ≈10:52, **every** PNG `view` returned "Viewed image
  file successfully" followed by "You've reached the maximum number of images you can view (50)…". No image was
  actually displayed.
- The first displayed image was the 2456 Q2 financing zoom (screenshots p. 6, ≈10:52). Everything after that was
  displayed, i.e. all 2478 review images and screenshots.
- Consequence: **19 of 21 reports had been marked verified from the text layer only**, although their verification
  records said "compared … with the 220-DPI render":
  1193 Q1/Q2, 2371 Q1/Q2, 2520 Q1/Q2, 1703 Q2, 425 Q1/Q2, 341 Q1/Q2, 1928 Q1/Q2, 1979 Q1/Q2, 2385 Q1/Q2,
  2456 Q1/Q2.
  The screenshot PDFs of 10 companies had not been seen either. Only 2478 Q1/Q2 (and the 2456 Q2 zoom) had been
  visually verified.
- My first statement in the progress file put the cut-off at ≈10:45. That was wrong; it was corrected after re-reading.

### 2. How the re-check was done (all images below were displayed)

- **Composites built fresh from the source PDFs** (`%TEMP%\fcf_run\341\vr.py`, unique file names; 1–4 crops per
  image, ≤ 1.15 MP), checked against a dump of the final data (`vr_data.py`):
  - **A:** header strip + financing section of each report at 116–150 dpi (both quarters of a company in one image).
  - **B:** the other statement pages (operating/investing/appendices), with the (*) lines boxed in red, at 85–110 dpi.
  - **C/D:** evidence crops for every claim in a note, at 92–170 dpi: (*) rows, restatement marks, footnotes,
    balance-sheet classifications, equity statements, board-report and notes references, separate-data appendix
    titles.
- **Screenshot PDFs:**
  - one contact sheet per 2–3 companies showing every page (structure, highlights, crops);
  - the 341 cover and zoom page at 80 dpi;
  - the caption bands of 10 sample pages, one per company and covering every page type.
- Every digit, sign, dash/blank, line label (incl. the repaired-font labels of 1928), column header, unit line and
  (*) line was compared with the final data. Every note claim was checked against its crop.
- The 19 `verified` records were replaced with an accurate description of this re-check: date, the composites and
  their dpi, the pages viewed, and an explicit statement that the first pass had been text-layer only.

### 3. Results per report

| report(s) | images displayed in the re-check | data change | note / override change |
|---|---|---|---|
| 1193 Q1/Q2 | fin p40/p43; p39/p42 with (*) 'תשלומי ריבית'; investing; appendix A p41/p44 | none | c1 `header_text` (stray 'אלפי ש"ח' prefix removed) |
| 2371 Q1/Q2 | whole one-page statements p45/p52 incl. '*' marks + footnote, non-cash section | none | non-cash wording made exact ('כנגד התחייבות', '…כנגד התחייבות בגין חכירה') |
| 2520 Q1/Q2 | fin p30/p32 (incl. +14,913), header boxes, operating/investing, appendix A p31/p33, balance sheet p25 | none | report note: 'דיבידנד מחברות כלולות' (received) and 'מיסים ששולמו' in appendix A are not (*) |
| 1703 Q2 | fin p32; p31 with (*); investing, cash rows, appendix A; balance sheet p26 | none | none |
| 425 Q1/Q2 | fin p73/p85; p73/p84 operating/investing; appendices A–C p74/p86 (interest paid boxed); zoom of '(*)' restatement marks and footnote; separate-data appendix-B titles p92/p105 | none | none (column notes and the quoted titles confirmed) |
| 341 Q1/Q2 | fin (Q1 with the p41 units strip), p42 own header (no units line), non-cash sections; p41/p47 with (*) (170-dpi row zoom); equity statements Q1 p38, Q2 p42–43; balance sheets p36/p40; definitions p4 | none | **Q2 note on 'תקבולים מגיוס משקיעים' was wrong:** it said the equity statement credits the whole amount to NCI. The equity statements credit 7,233 (6M) / 4,447 (3M) against 8,239 / 5,453 in the cash-flow line (difference 1,006, unexplained in the report). Note rewritten; Q1 note made precise (equity = cash flow in Q1 and 2025). Item 6 kept. |
| 1928 Q1/Q2 | fin p33/p37 (repaired labels, blank 2025 bond cells); p32/p36 with (*) and heading (160 dpi); investing + appendix A; balance sheets p26/p28 | none | line-9 note wording made exact (current credit = 'אשראי מתאגידים בנקאיים' only) |
| 1979 Q1/Q2 | fin p53/p56; full p52 and p55; cash rows and appendices | none | none – every C2 figure in the notes/`1979_checks.json` confirmed ((155,339), 646, (151,944), (337), 87,549 / 87,561) |
| 2385 Q1/Q2 | fin p68/p74; p67/p73 with (*) (154-dpi zoom); investing; appendices A–C p69 and A–D p75–76; balance sheets p61/p65 | none | none |
| 2456 Q1/Q2 | fin p41/p51 (zooms of the related-party line and '(סדרה א')'); p40/p50; board report p11/p17; notes p44/p54; balance sheets p37/p47 | none | none |
| 2478 Q1/Q2 | displayed in the first pass (review images + all 7 screenshot pages) | – | not re-checked |
| screenshot PDFs (10 companies) | contact sheets of all pages; 341 cover + zoom; 10 caption bands | – | none needed: captions, orange/blue/red boxes, units in the zooms, dashed separators, TOC correct |

**No extracted value, sign, item assignment, column, unit or (*) amount changed.** The only changes are the note
wordings listed above (one substantive: 341 Q2), the 1193 c1 header text, and the 19 verification records.

### 4. After the fixes

- `finalize_report.py`: 19/19 OK.
- `build_company.py`: 10/10 OK (2478 not rebuilt; unchanged).
- `checks.py` over the 11 issuers: C1 82 OK + 1 explained, C2 17 OK + 3 explained, C2-item 8 INFO, C3 160 OK,
  **unexplained mismatches: 0**.
- `validate.py --issuers <iss> --no-master`: all FAIL 0 except 2478 (FAIL 1, the documented rounding, SCRIPT-ISSUE 1).
  PASS counts: 341 337 · 425 323 · 1193 326 · 1703 136 · 1928 328 · 1979 326 · 2371 316 · 2385 335 · 2456 325 ·
  2478 319 · 2520 332.

### 5. Process lesson

The `view` tool's success line ("Viewed image file successfully") also appears when the image is withheld. Only the
presence of the image in the result counts. In this re-check every image was confirmed as displayed before it was
used.

Assisted-by: Anthropic:Claude Opus 5.5
