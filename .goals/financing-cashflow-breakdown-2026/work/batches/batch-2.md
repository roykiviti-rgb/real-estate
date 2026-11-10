# Batch 2 report — Phase B (financing cash-flow breakdown 2026)

Builder: Phase B batch 2 of 8 (2026-11-10). Protocol: `work\PIPELINE.md` + `work\phaseB-conventions.md`.
Issuers (11 companies, 20 reports): 121 קרדן ישראל · 155 מנרב · 715 אזורים · 1331 צילו-בלו (Q2 only) · 1644 אורון ·
1722 חג'ג' אירופה (EUR) · 2392 רייק אספן · 2418 רם אדרת (C) · 2474 ליאם · 2521 קטה · 2557 תדהר (Q2 only).

**Result: all 20 reports verified against the rendered images; all 11 companies built without `--draft`;
`checks.py` → unexplained mismatches 0 for all; `validate.py --issuers <iss> --no-master` → FAIL 0 for 10 companies,
FAIL 4 for 715 (SCRIPT-ISSUE 1: the validator has no exception for a documented source-rounding C1 difference).**

---------------------------------------------------------------------------------------------------------------

## 0. Verification method (all reports) and an important process finding

For every report:

- `tool_review.py`: the line table and C1;
- the screenshots PDF pages rendered with `tool_shots.py <iss> 150`. I compared the zoom page (header strip plus the
  whole financing section) digit by digit with the final data;
- 120–150-DPI renders of the other statement pages (operating, investing, appendices), to look for (*) lines and
  restatement marks;
- 300-DPI `tool_grid.py` zooms where a digit or a label needed it (715, 2418), and a 400-DPI clip for the 2557 label;
- the red (*) crops for every (*) line (121, 1331, 2418);
- composites of the full-page highlight pages of all 20 reports, to check that the orange and blue boxes cover the
  financing section and the header/units.

Interest and dividend rows on all statement pages were also listed from the text layer and reconciled with the
images. Every `verified.method` field describes what was actually viewed.

**Process finding, important for the other batches and Phase C.** After about 50 images in a session, the `view` tool
keeps answering "Viewed image file successfully" but adds "You've reached the maximum number of images you can view
(50)…", and it does not display the image. Between about 10:13 and 11:01 my image views were not displayed, so the
first verification of 121, 155, 715, 1331, 1644, 1722, 2392, 2418, 2474 Q2, 2521 and 2557 had in fact rested on the
text layer. I noticed this, re-did the visual verification for every one of these reports with composite images
(several pages per image), and rewrote the `verified.method` texts. No value had to change. **Other batches should
check that their image views really returned an image.**

---------------------------------------------------------------------------------------------------------------

## 1. Companies

### 121 קרדן ישראל בע"מ — Q1 + Q2
- **Sources:**
  - Q1: `121_..._Q1_1744790.pdf`. Consolidated statement pp. 46–48 (title `דוחות מאוחדים על תזרימי המזומנים`); financing on p. 47.
  - Q2: `..._Q2_1766447.pdf`, pp. 50–52; financing on p. 51.
  - The separate data on pp. 65–66 (Q1) and 70–72 (Q2) were not used.
- **Columns:** Q1 3M-26 / 3M-25 / FY-25. Q2 6M-26 / 6M-25 / 3M (April–June) 26 / 3M (April–June) 25 / FY-25.
- **Units:** אלפי ש"ח.
- **Mapping:** 10 lines plus the total.
  - `תמורה ממימוש אופציות בחברה מאוחדת` (734) → **6**. It is an issuance of subsidiary shares to option holders (NCI); item 2 is kept for options on the reporting company's own shares.
  - `תמורה ממימוש אופציות למניות החברה` → 2.
  - `אשראי לזמן קצר מתאגידים בנקאיים ומוסדות פיננסיים, נטו` → 5.
  - The other lines are standard.
- **(\*) interest** (two lines, both outside financing):
  - Operating `ריבית ששולמה`: p. 46 / p. 50.
  - Appendix ב `ריבית ששולמה והוונה למלאי` (capitalised interest paid): p. 48 / p. 52. The extractor missed it, so it was added with `outside_add` and a bbox.
  - The appendix prints the amount without parentheses. To keep the info-row sum meaningful, I entered it as a payment (negative) and documented this in the note (see mapping decision 10).
  - No dividends were paid outside financing. Appendix א (non-cash, including a declared NCI dividend) was excluded.
- **Overrides:** header texts, items, notes, `outside_add`, `info_notes`, report notes.
- **Checks:** C1 0 in all 8 columns; C2 OK; C3 16/16 OK.
- **validate:** PASS 332 / FAIL 0.

### 155 קבוצת מנרב בע"מ — Q1 + Q2
- **Sources:**
  - Q1: `..._Q1_1742331.pdf`, pp. 125–126; financing on p. 126.
  - Q2: `..._Q2_1764162.pdf`, pp. 129–130; financing on p. 130.
  - Title: `דוחות מאוחדים על תזרימי המזומנים ביניים`. The separate data on pp. 144–145 and 152–153 were not used.
- **Columns:** as in 121. Q2 c4 was inferred by the extractor and confirmed on the image as 3M to 30.06.2025.
- **Units:** אלפי ש"ח.
- **Mapping:**
  - `מימוש אופציה` (62,559) in FY-25 → **14**. The amount is negative, so it is a payment, not option proceeds. The Q2 board report (p. 11, rendered and read) mentions a financial liability for a put option on shares of the subsidiary דרך עפר; the payment is read as the purchase of NCI shares.
  - `הנפקת מניות*` (the IPO of 24.3.2026, note 6ו) → 1, including (232) in Q2 3M-26, which is issue costs.
  - `אשראי לזמן קצר, נטו` → 5.
  - Q1 label typo `יפרעון` (a text-layer artefact) corrected to `פירעון אגרות חוב`.
- **(\*):** interest is in financing (13); outside financing there are only receipts. No dividends.
- **Checks:** all OK.
- **validate:** PASS 326 / FAIL 0.

### 715 אזורים-חברה להשקעות בפתוח ובבנין בע"מ — Q1 + Q2
- **Sources:**
  - Q1: `..._Q1_1744611.pdf`, pp. 46–47; financing on p. 47.
  - Q2: `..._Q2_1765211.pdf`, pp. 50–51; financing on p. 51.
  - Title: `תמצית דוח על תזרימי מזומנים ביניים מאוחד`. The earlier block on pp. 18–19 / 20–21 is the board report; pp. 61–62 / 67–68 are the separate data.
- **Units:** אלפי ש"ח.
- **Mapping:**
  - The combined line `פרעון התחייבויות לזמן ארוך לבנקים, אגרות חוב ואחרים` → **7**, in both reports. The statement does not split it. From the board report (p. 24, read at 200 DPI):
    - Series 13 repays 16% and series 14 repays 15% of principal on 31.12.2025; series 15 repays 5% on 30.6 each year.
    - So bond principal is about 200 million of the 703,645 for 2025, and loans are the dominant component.
    - In the 2026 columns (13,405) most of the amount is probably the 30.6.2026 instalment of series 15, which is item 8 in substance. This is noted on the line (mapping decision 3).
  - `תמורה מהנפקת מניות, בניכוי הוצאות הנפקה` (198,038; shares plus options in a private placement per the board report) → 1 (conventions §6).
  - `תקבולים מבעלי זכויות שאינן מקנות שליטה` → 6.
  - The text-layer artefact `ריבית ששולמה (` was corrected.
- **(\*):** interest and dividend are in financing; outside there are only receipts.
- **Checks:** **C1 ±1 in 4 columns.**
  - Q1: 3M-25 is −1.
  - Q2: 6M-26 is +1, 6M-25 is −1 and 3M-26 is +1.
  - All are source rounding; the digits were confirmed on 300-DPI zooms. They are explained in `overrides\715_checks.json` and in `issues` / `column_notes`.
  - C2 OK; C3 16/16 OK.
- **validate:** **PASS 321 / FAIL 4.** The 4 failures are the per-column `AC6 C1` check at `validate.py` line 90, which ignores documented explanations (SCRIPT-ISSUE 1). `checks.py` reports 0 unexplained.

### 1331 קבוצת צילו-בלו בע"מ — Q2 only (no Q1 report in the folder)
- **Source:** `..._Q2_1766504.pdf`, pp. 30–32 (`תמצית דוחות מאוחדים על תזרימי המזומנים`); financing on p. 30. The `-01` file is an appraisal and not a source.
- **Columns:** 3 only: 6M-26 / 6M-25 / FY-25 (no 3-month columns).
- **Units:** אלפי ש"ח.
- **Text layer:** words come in reversed order, so every label was read from the image. Line 1 was corrected to `הנפקת מניות (ראה ביאור 1ב')`.
- **Mapping:** `אשראי והלוואות מתאגידים בנקאיים, נטו` → 5 (net, no term). Treasury shares → 9; lease principal → 10.
- **(\*) interest:**
  - Disclosed only in appendix ד (`מזומנים ששולמו במשך התקופה עבור: ריבית`, p. 32; bbox includes the heading). Sign as printed (positive).
  - Note per conventions §1: `גילוי בנספח ... – הסעיף לא צוין (לא בפעילות מימון)`. The operating section starts from net profit, so the interest is probably in operating.
- **Checks:** C1 OK (3 columns).
- **validate:** PASS 137 / FAIL 0.

### 1644 קבוצת אורון אחזקות והשקעות בע"מ — Q1 + Q2
- **Sources:**
  - Q1: `..._Q1_1741690.pdf`, pp. 47–48; financing on p. 48. The Q1 text layer has words in reversed order; labels were checked on the image and are correct.
  - Q2: `..._Q2_1763699.pdf`, pp. 52–53; financing on p. 53.
  - Title: `דוחות תמציתיים מאוחדים על תזרימי המזומנים`.
- **Units:** אלפי ש"ח.
- **Mapping:** standard. `הנפקת הון, נטו` → 1; `אשראי לזמן קצר מתאגידים בנקאיים ומאחרים, נטו` → 5. The blank Q2 3M-26 cell = 0 (confirmed).
- **(\*):** interest and dividends are in financing; none outside.
- **Column notes:** Q2 c2/c4 carry the operating-section marks `(*) שינוי במדיניות חשבונאית המיושם למפרע (ביאור 2ד')`. The column headers and the financing lines are not marked, so the columns are not flagged restated (conventions §10).
- **Checks:** all OK.
- **validate:** PASS 328 / FAIL 0.

### 1722 חג'ג' אירופה דיוולופמנט צ.ש. בע"מ — Q1 + Q2 (EUR)
- **Sources:**
  - Q1: `..._Q1_1745698.pdf`, a one-page statement on p. 66.
  - Q2: `..._Q2_1767756.pdf`, p. 65.
  - Title: `תמצית דוחות על תזרימי המזומנים ביניים מאוחדים`.
- **Units:** **אלפי אירו**.
- **Mapping (C3 4/5 difference aligned):**
  - `(קבלת) הלוואות מתאגיד בנקאי, נטו` (27,288 in FY-25) → **4** in both reports. Per the board report, these are bank loans of about €27.3M received in Q4-2025 for Victoriei 109 / Tudor, with current maturities. They are long-term loans; "נטו" means net of raising costs, and repayments are on a separate line. This is a deliberate exception to "net without a term → 5" (mapping decision 5).
  - `הנפקת מניות וכתבי אופציה, נטו` → 1 (unsplit package, conventions §6).
  - `מימוש כתבי אופציה` → 2.
  - `תקבולים בגין הלוואות לרוכשי דירות, נטו` → **אחר**. These are collections of loans the company granted to apartment buyers (an asset), not borrowing.
  - `החזר השקעה לזכויות שאינן מקנות שליטה` → **12** (capital returned to NCI).
  - `קבלת הלוואות מגופים פיננסיים ואחרים (, נטו)` → 4; repayments → 7.
- **(\*):** interest is in financing; none outside.
- **Column notes:** the `(*) סווג מחדש` / `(**) מיון לא מהותי` marks on operating and investing values (Q1 c2; Q2 c2/c4/c5) are explained; the columns are not restated.
- **Checks:** C1 OK; C2 OK; **C3 16/16 OK after alignment**.
- **validate:** PASS 328 / FAIL 0.

### 2392 רייק אספן בע"מ — Q1 + Q2
- **Sources:**
  - Q1: `..._Q1_1742520.pdf`, pp. 49–50; financing on p. 49. Pp. 29–32 are the board report / separate data.
  - Q2: `..._Q2_1763248.pdf`, pp. 50–51; financing on p. 50.
- **Units:** אלפי ש"ח.
- **Wrapped labels:** joined; the continuation rows were dropped (`קשורים`; `בנקאיים, נטו`, `אחרים וצדדים קשורים`).
- **Mapping:**
  - `הלוואות שהתקבלו מחברה האם ומבעל השליטה` → 4.
  - `הלוואות שהתקבלו מתאגידי מימון חוץ בנקאיים, אחרים וצדדים קשורים` → 4. These are gross receipt lines without a stated term (mapping decision 8).
  - `פירעון הלוואות שהתקבלו מצדדים קשורים ואחרים` (Q2: `...מאחרים`) → **7** (the auto mapping said 5). It is a gross repayment line, not a net line.
  - `תשלום עבור הנפקת מניות, נטו` → 1.
- **(\*):** interest is in financing; none outside.
- **Column note:** Q1 c2 has two `*` marks (immaterial adjustment of comparatives) in operating.
- **Checks:** all OK.
- **validate:** PASS 328 / FAIL 0.

### 2418 רם אדרת הנדסה אזרחית בע"מ — Q1 + Q2 (difficulty C)
- **Sources:**
  - Q1: `..._Q1_1744896.pdf`, pp. 45–47; financing on p. 46.
  - Q2: `..._Q2_1766843.pdf`, pp. 49–51; financing on p. 50.
  - Title: `דוחות מאוחדים ביניים תמציתיים על תזרימי המזומנים`.
- **Units:** אלפי ש"ח.
- **Source defect (Q1, FY-2025 column):** the column is printed shifted one row against the labels. There are 7 values against 6 labels, and a single `-` is printed below the rule. Following conventions §9, every value was assigned to its line using the statement's arithmetic and the identical Q2 FY-2025 column:
  - 111,258 bonds issued;
  - (85,000) bond repayment, an added line `[ללא תווית בדוח Q1] פרעון אגרות חוב (התווית לפי דוח Q2)`, item 8;
  - 54,100 short-term credit;
  - `-` long-term loans;
  - (1,625) long-term repayment;
  - (7,908) leases;
  - `-` loan from an associate.
  - The stray `-` row was dropped (it carries no amount). The printed total of 70,825 is unchanged.
  - Documented in `issues`, `column_notes` c3 and the line notes. C3 is now 16/16 OK.
- **Mapping:**
  - `קבלת הלוואה מחברה כלולה` → 4 (all zero once the shift is corrected).
  - Q2 `קבלת הלוואה מזכויות שאינן מקנות שליטה` (266) → **4**. It is a loan received from NCI (a liability), not an equity contribution.
- **(\*) interest:**
  - Only in appendix ב (`ריבית ששולמה`, p. 47 / p. 51). Sign as printed (positive). Note per conventions §1 ("הסעיף לא צוין").
  - Appendices א and ג (non-cash items and business combinations) were excluded.
- **Checks:** C1 OK; C2 total OK; C3 OK.
  - C2-item: in Q1 3M-26, item 4 = 76,370 and item 5 = (31,182). The Q2 derivation gives 76,730 and (31,542). The 360 difference sits in the sources; it was checked at 300 DPI in both reports, and the net amount and total are identical. Explained in `overrides\2418_checks.json`.
- **validate:** PASS 326 / FAIL 0.

### 2474 ליאם הנדסה גרופ חריש מרכז עסקים בע"מ — Q1 + Q2
- **Sources:**
  - Q1: `..._Q1_1745084.pdf`, pp. 31–32; financing on p. 32.
  - Q2: `..._Q2_1764180.pdf`, pp. 37–38; financing on p. 38. The Q2 column headers carry no audit wording.
- **Units:** אלפי ש"ח.
- **Mapping (C3 4/5 difference aligned):** the bank/others loan lines (Q1 `קבלת הלוואות מתאגידים בנקאיים ואחרים` 9,444 and its repayment line; Q2 `קבלת (פירעון) ... ` net plus the repayment line) → **5** in both reports.
  - The Q2 line is net without a term (R3).
  - The balance sheet shows all `אשראי מתאגידים בנקאיים ואחרים` as current.
  - The board report (Q2 §9.1, p. 11, rendered) shows `אשראי לזמן קצר 93,649` and `אשראי לזמן ארוך -`.
  - Caveat noted on the line: the board report gives average long-term loans of about 42M for 2025, so part of the FY-25 repayments may have been long-term; the statement does not split them.
  - Shareholder/related-party loan repayment → 7.
- **(\*):** interest is in financing; none outside.
- **Checks:** C3 16/16 OK after alignment.
  - **C2 3M-25 total ±1** (5,648 vs 5,647): the interest line (2,176) in Q1 against (4,719) − (2,542) = (2,177) in Q2. Explained in `overrides\2474_checks.json`.
- **validate:** PASS 321 / FAIL 0.

### 2521 קטה גרופ - גיל קטה בע"מ — Q1 + Q2
- **Sources:**
  - Q1: `..._Q1_1745082.pdf`, pp. 34–35; financing on p. 35.
  - Q2: `..._Q2_1764973.pdf`, pp. 37–38; financing on p. 38.
  - Title: `דוחות מאוחדים ביניים על תזרימי המזומנים`.
- **Units:** אלפי ש"ח.
- **Mapping:** standard. `תשלומי ריבית בגין חכירות` → 13 (separately presented lease interest, R3); `תשלומי קרן בגין חכירה` → 10; short-term credit from banks and others, net → 5.
- **(\*):** interest is in financing; none outside. A dividend distributed in kind (non-cash) was excluded.
- **Column notes:** Q2 c2/c4/c5 carry `(*) סווג מחדש` marks in operating ("רכישת קרקעות" now shown separately; 312,923 − 144,831 = 168,092, as in Q1).
- **Checks:** **C2 3M-26 total −1** (14,920 vs 14,921): item 4 is +1 (7,000 vs 6,999) and item 13 is −2. Source rounding, explained in `overrides\2521_checks.json`. C3 OK.
- **validate:** PASS 324 / FAIL 0.

### 2557 קבוצת תדהר בע"מ — Q2 only (no Q1 report in the folder)
- **Source:** `..._Q2_1765408.pdf`, pp. 52–54; financing on p. 53. Title: `דוחות מאוחדים על תזרימי המזומנים`. The `-01` file is an appraisal and not a source.
- **Units:** אלפי ש"ח.
- **Mapping:**
  - 12 lines plus the total.
  - `רכישת זכויות מבעלי זכויות שאינן מקנות שליטה` → 14.
  - Shareholder/related-party loans (gross) → 4/7. The label of line 8, `(ראה באור 7ט')`, was read on a 400-DPI clip.
  - `תשלומים בגין חכירה` (no principal/interest split) → 10.
  - Dividends: to shareholders → 11; to NCI → 12.
  - Short-term bank credit, net → 5.
- **(\*):** interest and dividends are in financing; none outside. The non-cash share-for-share issuance (568,505, appendix ב) was excluded.
- **Checks:** C1 OK.
- **validate:** PASS 214 / FAIL 0.

---------------------------------------------------------------------------------------------------------------

## 2. Mapping decisions (cross-company judgement calls for Phase C to align)

1. **Subsidiary option exercise:** `תמורה ממימוש אופציות בחברה מאוחדת` (121) → **6**, not 2. It is an issuance of subsidiary shares to NCI.
2. **Payment on exercise of an NCI put option:** `מימוש אופציה` (negative 62,559; 155) → **14**.
3. **Combined long-term repayment line** (`פרעון התחייבויות לזמן ארוך לבנקים, אגרות חוב ואחרים`; 715) → **7**, the dominant component (loans; bonds are about 200M of 703.6M in FY-25). The same item is used in all columns and both reports. The line note records that the 2026 amount is mostly a bond instalment.
4. **Unsplit shares + options/warrants** (715 private placement; 1722 `הנפקת מניות וכתבי אופציה, נטו`) → **1** (conventions §6).
5. **Bank-loan line labelled "נטו" with separate repayments** (1722 `(קבלת) הלוואות מתאגיד בנקאי, נטו`) → **4**, not 5. The board report identifies long-term loans and "נטו" means net of raising costs. This is an exception to R3's "net without a term → 5"; Phase C may prefer 5 (then both Q1 and Q2 must change together).
6. **Collections of loans the company granted to apartment buyers**, presented in financing (1722) → **אחר**.
7. **Return of capital to NCI** (`החזר השקעה לזכויות שאינן מקנות שליטה`; 1722) → **12**.
8. **Gross loan receipt/repayment lines with no stated term** (non-bank financiers / others / related parties / parent / controlling shareholder; 2392, 2557, 2418) → **4 / 7**. Exception: **2474 → 5**, because the report itself shows the credit is entirely short-term (board report: long-term credit "-"; all of it current).
9. **Loan received from NCI holders** (2418 `קבלת הלוואה מזכויות שאינן מקנות שליטה`) → **4** (a liability, not equity; R3 item 4 includes partners/NCI holders).
10. **(\*) interest disclosed in an appendix:**
    - Appendix only (1331, 2418): sign as printed (positive), note `גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)` plus the page.
    - **121** has an operating `ריבית ששולמה` line **and** an appendix `ריבית ששולמה והוונה למלאי` (capitalised interest paid, printed positive). Both are in the info row; the appendix amounts are entered **negative** so the row is a meaningful total of interest paid outside financing. This deviates from "sign as printed" and is documented in the info note. Phase C should decide on one rule for this mixed case (1083 has a similar appendix, per Phase A).
11. **Separately presented lease interest** (2521) → 13. A lease line without a split (2557) → 10.
12. **Restated flag:** never set. All `(*)` / `(**)` reclassification or policy-change marks in my reports are on operating/investing values only; they are recorded as column notes (1644 Q2, 1722 Q1/Q2, 2392 Q1, 2521 Q2; 715 Q1 in the report notes).

---------------------------------------------------------------------------------------------------------------

## 3. Source issues found

| report | issue | treatment |
|---|---|---|
| 2418 Q1 | FY-2025 financing column printed shifted one row (7 values / 6 labels, stray `-`) | values re-assigned per Q2 FY-2025 and the arithmetic; added bond-repayment line; `issues` + column note |
| 715 Q1 / Q2 | printed totals differ by ±1 from the sum of the printed lines in 4 columns | kept as printed; C1 explained (`715_checks.json`) |
| 2474 | Q1 3M-25 interest (2,176) vs Q2-derived (2,177) | C2 explained |
| 2521 | Q1 3M-26 items 4/13 differ by +1/−2 from the Q2 derivation | C2 explained |
| 2418 | Q1 3M-26 items 4/5 differ by ∓360 from the Q2 derivation (net identical) | C2-item explained |
| 1331 Q2, 1644 Q1 | text layer returns words in reversed order | all labels read/checked on the image |
| 155 Q1 | text layer `יפרעון אגרות חוב` (letter-spacing artefact) | label corrected to `פירעון אגרות חוב` |

---------------------------------------------------------------------------------------------------------------

## 4. SCRIPT-ISSUEs

```
SCRIPT-ISSUE 1
  script:     validate.py (line 90, company_checks: ok(abs(sum(items)+other-total) < 1e-6, "AC6 C1 ..."))
  report:     715 Q1 (3M-2025) and 715 Q2 (6M-2026, 6M-2025, 3M-2026)
  symptom:    validate.py --issuers 715 --no-master → PASS 321 / FAIL 4, "FAIL: [715] AC6 C1 דוח Q.. | <period>",
              although the 4 differences are ±1 source rounding, explained in overrides\715_checks.json, and checks.py
              reports "unexplained mismatches: 0" (validate's own AC6/AC8 line also says unexplained=0).
              Evidence: %TEMP%\fcf_run\_runs\validate_20261110-113334_22244\validate.txt
  expected:   goal AC6 allows a non-zero C1 when the source statement itself does not add up and it is documented; the
              per-column AC6 check should pass (or WARN) when CK.explain() finds an explanation for that C1 key.
  workaround: none possible without a plug (forbidden) or changing printed values (forbidden); data kept as printed.
              Other issuers with documented C1 differences (719 Q1, 2483 Q2, 2533, 2417 Q1, 2478 Q2, 531 Q2) will hit
              the same failure.
  severity:   blocks the "FAIL 0" criterion for 715 only; the deliverable itself is correct and complete
```

```
SCRIPT-ISSUE 2
  script:     fcf_extract.py ((*) detection) / finalize_report.py ((*) info-row sum)
  report:     121 Q1, 121 Q2
  symptom:    (a) the appendix line 'ב) ריבית ששולמה והוונה למלאי' (capitalised interest paid) was not offered as a (*)
              candidate; (b) the info row sums all (*) lines of a kind, so lines printed with different sign conventions
              (operating '(10,512)' vs appendix '2,709') cannot all keep "sign as printed" and still give a meaningful total.
  expected:   (a) offer appendix interest-paid lines (also 'ריבית ששולמה והוונה') as candidates; (b) a per-line sign
              normalisation option (payments negative) for the info-row sum.
  workaround: outside_add with the appendix values entered negative + an info_notes text that states the printed amounts
              and the sign treatment.
  severity:   cosmetic / convention (values correct and documented)
```

Process issue (not a script): the image cap of the `view` tool (§0). Images stop being displayed although the call
reports success. Other batches may have marked reports verified without actually seeing the images.

---------------------------------------------------------------------------------------------------------------

## 5. Files written by this batch

- **Overrides** (`work\overrides\`): `121_Q1/Q2`, `155_Q1/Q2`, `715_Q1/Q2`, `1331_Q2`, `1644_Q1/Q2`, `1722_Q1/Q2`, `2392_Q1/Q2`, `2418_Q1/Q2`, `2474_Q1/Q2`, `2521_Q1/Q2`, `2557_Q2`.
- **Check explanations:** `715_checks.json`, `2418_checks.json`, `2474_checks.json`, `2521_checks.json`.
- **Data:** `work\data\<iss>_<Q>.json`, regenerated by `finalize_report.py` (via `tool_batch.py finalize`).
- **Company outputs** (2 files per company folder, via `build_company.py` / `tool_batch.py build`, no `--draft`).
- **Batch files:** `batches\batch-2.md` (this report) and `batches\batch-2-progress.md`.
- **Temp:** `%TEMP%\fcf_run\<iss>\` for my 11 issuers, deleted at the end. The `_runs` folders were left for Phase C.

---------------------------------------------------------------------------------------------------------------

## 6. Final status

| issuer | company | reports | status | validate (--no-master) |
|---|---|---|---|---|
| 121 | קרדן ישראל | Q1, Q2 | verified + built | PASS 332 / FAIL 0 |
| 155 | קבוצת מנרב | Q1, Q2 | verified + built | PASS 326 / FAIL 0 |
| 715 | אזורים | Q1, Q2 | verified + built | PASS 321 / FAIL 4 (SCRIPT-ISSUE 1 – documented ±1 source rounding) |
| 1331 | קבוצת צילו-בלו | Q2 (no Q1 in folder) | verified + built | PASS 137 / FAIL 0 |
| 1644 | קבוצת אורון | Q1, Q2 | verified + built | PASS 328 / FAIL 0 |
| 1722 | חג'ג' אירופה (EUR) | Q1, Q2 | verified + built | PASS 328 / FAIL 0 |
| 2392 | רייק אספן | Q1, Q2 | verified + built | PASS 328 / FAIL 0 |
| 2418 | רם אדרת | Q1, Q2 | verified + built | PASS 326 / FAIL 0 |
| 2474 | ליאם | Q1, Q2 | verified + built | PASS 321 / FAIL 0 |
| 2521 | קטה גרופ | Q1, Q2 | verified + built | PASS 324 / FAIL 0 |
| 2557 | קבוצת תדהר | Q2 (no Q1 in folder) | verified + built | PASS 214 / FAIL 0 |

20 of 20 reports are verified against the images; 11 of 11 companies are built; `checks.py` shows 0 unexplained
mismatches.

Assisted-by: Anthropic:Claude Opus 5.5
