# Batch 7 report — Phase B (iteration 1)

Builder: Phase B batch 7. Issuers: 473, 1330, 1618 (pilot – rebuild check only), 1903, 1905, 2384, 2386, 2429,
2449, 2522, 2559. Protocol: `work\PIPELINE.md` §0–§13 + `work\phaseB-conventions.md`. No git.

Verification method (all reports): `tool_review.py` package (220-DPI header strip + financing section with numbered
line frames, statement pages at 100 DPI, (*) crops) viewed with the image viewer; every label, every value digit by
digit, column headers, units and (*) lines compared with the images; doubtful spots zoomed with
`tool_grid.py --clip … --dpi 300`; C1 per column; C2 line-by-line arithmetic between Q1 and Q2 reports where
possible; the word layer of every statement page swept for interest/dividend lines and restatement markers.
After finalising: `checks.py`, `build_company.py` (no `--draft`), `tool_shots.py` (screenshots PDF rendered and
viewed), `validate.py --issuers <iss> --no-master`.

**Process note (transparency).** At the start of the batch the image viewer refused images (its per-context limit
was exhausted), so the first "visual" pass of 473, 1330, 1903, 1905, 2384, 2386 and the first look at the 1618 /
473 / 1330 / 1903 / 1905 / 2384 / 2386 screenshots did **not** actually display. This was noticed at 2429 and fully
redone: the fin + (*) crops of every report of those six companies were composed into a few large images and
compared digit by digit (all values, labels, headers, units matched – no correction was needed), and all screenshot
PDFs (incl. 1618's) were reviewed as thumbnail sheets (boxes, zoom pages, (*) crops, context pages) plus a numeric
geometry check (orange box covers heading…total on every financing page, header box present and above the section,
every (*) line has a bbox and a header strip) and a caption text check (473 read in full; report id present on every
page of every PDF). 2429, 2449, 2522 and 2559 were verified with the images displayed from the start.

---------------------------------------------------------------------------------------------------------------

## 1618 קבוצת אשטרום בע"מ (pilot – not re-verified)

* Pilot overrides unchanged (`1618_Q1.json`, `1618_Q2.json`, `1618_checks.json`; verified 2026-11-09).
* `checks.py --issuers 1618`: C1 OK 8, C2 OK 2, C2-item INFO 2 (the explained 1,267 gross-presentation difference in
  items 4/7 of Q1-2025), C3 OK 16 → unexplained mismatches 0.
* `validate.py --issuers 1618 --no-master`: **PASS 338 / FAIL 0**.
* Screenshots PDF (9 pages) viewed: cover, Q1 p.56 full page + zoom, context pp. 55/57, Q2 p.67 full page + zoom
  (T2 label `(אפריל–יוני)` in the caption), context pp. 66/68 – as in the pilot.

---------------------------------------------------------------------------------------------------------------

## 473 קבוצת עמוס לוזון יזמות ואנרגיה בע"מ

| | Q1 2026 | Q2 2026 |
|---|---|---|
| source | `473_..._2026_Q1_1745607.pdf` (99 pp) | `473_..._2026_Q2_1767385.pdf` (109 pp) |
| statement | `דוח תמציתי מאוחד על תזרימי המזומנים`, pp. 55–56 | same title, pp. 60–61 |
| financing | p. 56 (13 lines + total) | p. 61 (13 lines + total) |
| columns | 3M-31.03.2026, 3M-31.03.2025, FY-2025 | 6M-2026, 6M-2025, 3M Apr–Jun 2026, 3M Apr–Jun 2025, FY-2025 |
| units | אלפי ש"ח | אלפי ש"ח |

* Statement pick: the flag "not the first block (p. 38 / p. 41)" – the earlier pages are board-report/other tables;
  the used pages carry the company name and the title `דוח תמציתי מאוחד` (confirmed on the images).
* Mapping decisions (same in Q1 and Q2):
  * `קבלת הלוואה מהמיעוט` → **4** (not the auto-suggested 6): loans from NCI holders of subsidiaries; the balance
    sheet shows `הלוואה מבעלי מניות המיעוט` mainly as a non-current liability; R3 lists NCI holders among the
    lenders of item 4. Item 6 is reserved for equity contributions of NCI.
  * `רכישת כתבי אופציה` (2025: (1,580)) → **9** (not 2): buy-back of the company's own warrants; in the statement of
    changes in equity it is charged to equity attributable to the owners (warrants reserve / premium). It is not an
    exercise; the nearest item by nature is the self-purchase of the company's own equity instruments.
  * `רכישת מניות מהמיעוט` → 14; `מימוש כתבי אופציה` → 2; `דיבידנד ששולם למיעוט` → 12; `דיבידנד ששולם לבעלי המניות`
    → 11; lease principal → 10; `קבלת הלוואות לזמן קצר מתאגידים בנקאיים ומוסדות פיננסיים, נטו` → 5.
* Labels: Q1 line 13 prints `פינסיים` (source typo, zoomed at 300 DPI) – kept verbatim, noted.
* Column header texts (verbatim row of the workbook) cleaned via `columns.cN.header_text` (Q1 c1/c2, Q2 c1/c3: the
  auto text had picked up the page title or the units); Q1 c1 `audit` set to `בלתי מבוקר`.
* (*): interest paid in operating activities (`מזומנים ששולמו והתקבלו במהלך התקופה עבור: ריבית ששולמה`) – Q1:
  (39,353) / (21,218) / (101,793); Q2: (66,956) / (33,104) / (27,603) / (11,886) / (101,793), note `פעילות שוטפת`.
  Dividends paid only in financing. Appendix A (non-cash: NCI dividend declared 9,980 in Q1-2025) not included.
* Checks: C1 0 everywhere; C2 OK 2 (and every line: Q1 3M + Q2 Apr–Jun = Q2 6M); C3 OK 16. No explanations needed.
* Overrides: `473_Q1.json`, `473_Q2.json` (items 4/9 for lines 4/8, notes, header texts, report notes, verified).
* Source issues: none (only the `פינסיים` spelling).
* `validate.py --issuers 473 --no-master`: **PASS 336 / FAIL 0**. Screenshots PDF: 9 pages viewed (boxes, zoom,
  (*) crops p. 55 / p. 60, captions) – OK.

---------------------------------------------------------------------------------------------------------------

## 1330 פרשקובסקי השקעות ובניין בע"מ

| | Q1 2026 | Q2 2026 |
|---|---|---|
| source | `1330_..._2026_Q1_1742648.pdf` (83 pp) | `1330_..._2026_Q2_1764951.pdf` (88 pp) |
| statement | `דוחות תמציתיים מאוחדים על תזרימי המזומנים`, p. 53 (all 3 sections) + p. 54 (appendices א'–ג') | same, p. 57 + p. 58 |
| financing | p. 53 (7 lines + total) | p. 57 (8 lines + total) |
| columns | 3M-31.03.2026, 3M-31.03.2025, FY-2025 | 6M-2026, 6M-2025, 3M Apr–Jun 2026, 3M Apr–Jun 2025, FY-2025 |
| units | אלפי ש"ח | אלפי ש"ח |

* Mapping: all straightforward (auto suggestions confirmed): bond repayment 8, bond issue net of costs 3,
  `אשראי מתאגידים בנקאיים והלוואות לזמן קצר, נטו` 5, LT loan repayment 7, lease 10, `הנפקת הון מניות ופרמיה` 1,
  `רכישת מניות באוצר` 9, `דיבידנד שחולק` (Q2) 11. Notes added on every line.
* (*): no interest line in any section; **appendix B** (`נספח ב' – מידע נוסף על תזרימי מזומנים: מזומנים ששולמו
  במשך התקופה עבור: עלויות מימון (כולל עלויות שהוונו)`) → (*) interest info row added with `outside_add`, values as
  printed (positive): Q1 49,718 / 42,490 / 196,235; Q2 114,720 / 93,435 / 65,002 / 50,945 / 196,235 (Q1 + Q2 Apr–Jun
  = 6M in both years). Note (conventions §1): `גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)`
  – the report does not say where the payments are classified (finance costs sit in profit; capitalised costs in
  inventory/investment property). No dividends paid outside financing (`דיבידנד מחברה כלולה` in investing is a receipt).
* Overrides: `1330_Q1.json`, `1330_Q2.json` (notes, header texts, the appendix (*) line with bbox incl. the appendix
  title, `boxes.<p>.header` for the appendix page so the red crop shows the column headers – see SCRIPT-ISSUE 1).
* Checks: C1 0; C2 OK 2 (line by line too); C3 OK 16.
* Source issues: none.
* `validate.py --issuers 1330 --no-master`: **PASS 325 / FAIL 0**. Screenshots PDF: 9 pages viewed – OK after the
  header-box workaround.

---------------------------------------------------------------------------------------------------------------

## 1903 קבוצת יובלים השקעות בע"מ

| | Q1 2026 | Q2 2026 |
|---|---|---|
| source | `1903_..._2026_Q1_1744226.pdf` (103 pp) | `1903_..._2026_Q2_1767412.pdf` (95 pp) |
| statement | `תמצית דוחות על תזרימי המזומנים ביניים מאוחדים`, pp. 57–58 (p. 58 = appendices) | same, pp. 57–58 |
| financing | p. 57 (10 lines + total) | p. 57 (10 lines + total) |
| columns | 3M-31.03.2026, 3M-31.03.2025 **(מוצג מחדש)**, FY-2025 | 6M-2026, 6M-2025 **(מוצג מחדש)**, 3M Apr–Jun 2026, 3M Apr–Jun 2025 **(מוצג מחדש)**, FY-2025 |
| units | אלפי ש"ח (printed in every column header) | אלפי ש"ח |

* Mapping decisions (same in Q1 and Q2):
  * `קבלת/פירעון אשראי ממוסד פיננסי` → **5** (gross lines, no term on the line; the balance sheet shows
    `אשראי מתאגידים פיננסיים` as a current liability) – auto suggestion confirmed.
  * `קבלת/פירעון הלוואות מהחברה האם` → **5** (auto: 4/7). No term on the line; in the balance sheet the parent
    balance is a current liability (`יתרות זכות לחברה האם`); the loans are on-demand/short-term (in 2025 32,000 of
    them were converted into capital notes – non-cash). Short-term borrowing from another lender, gross → 5.
  * `קבלת הלוואות מאחרים` (27 in 2025) → 4 (loan, no term, gross receipt; default for loans – immaterial).
  * `ריבית ועמלות ששולמו` → 13 (fees included – noted). Bond issue 3, bond repayment 8.
* Label: `פירעון אגרות חוב` – the text layer had glued the note reference `6(ו')` (separate `ביאור` column) to the
  label; fixed with `line_text`.
* Restatement: the 2025 comparative values of the parent-loan lines carry `(*)` = `התאמה למפרע בגין הצגה מחדש –
  ראה ביאור 2ז' לדוחות הכספיים השנתיים המאוחדים ליום 31 בדצמבר 2025` (footnote on the statement). The marker is on
  values of the financing section in those columns, so the columns were flagged `restated` (Q1 c2; Q2 c2, c4) with
  a column note quoting the footnote and the marked amounts (conventions §10 – listed under mapping decisions).
  FY-2025 is not marked.
* (*): interest paid only in financing (13); `ריבית שהתקבלה` (investing) is a receipt; no dividends paid. Info rows 0
  with no note.
* Checks: C1 0; C2 OK 2 (line by line too; the 2025 bank-credit receipt 986 of Q1-2025 appears in Q2 as an
  Apr–Jun repayment (986) – both item 5, so no item difference); C3 OK 16.
* Source issues: none.
* `validate.py --issuers 1903 --no-master`: **PASS 330 / FAIL 0**. Screenshots PDF: 7 pages viewed – OK.

---------------------------------------------------------------------------------------------------------------

## 1905 גלעד מאי חברה להשקעות בניה ופיתוח בע"מ

| | Q1 2026 | Q2 2026 |
|---|---|---|
| source | `1905_..._2026_Q1_1744780.pdf` (52 pp) | `1905_..._2026_Q2_1766777.pdf` (58 pp) |
| statement | `דוחות על תזרימי המזומנים ביניים מאוחדים`, p. 40 (whole statement on one page) | `דוחות מאוחדים על תזרימי מזומנים`, pp. 43 (operating) – 44 (investing, financing) |
| financing | p. 40 (6 lines + total) | p. 44 (6 lines + total) |
| columns | 3M-31.03.2026, 3M-31.03.2025 **(מוצג מחדש)**, FY-2025 | 6M-2026, 6M-2025 **(מוצג מחדש)**, 3M Apr–Jun 2026, 3M Apr–Jun 2025 **(מוצג מחדש)**, FY-2025 |
| units | אלפי ש"ח | אלפי ש"ח |

* **No financing heading** in either report: located visually – the section starts right below
  `מזומנים נטו שנבעו מפעילות (ששימשו לפעילות) השקעה` and ends with `מזומנים נטו שנבעו מפעילות (ששימשו לפעילות)
  מימון`; the extractor's section (investing total → financing total) matches the images exactly (6 lines). The
  orange box covers exactly these lines (checked in the screenshots).
* Mapping (same in Q1 and Q2): `אשראי מתאגידים בנקאיים ואחרים, נטו` 5; `קבלת אשראי` / `פירעון אשראי` (gross, no
  term) 5 – note: the 2026 receipts include an 86.1 M NIS long-term bank loan for a land purchase (repayable
  26.3.2028; non-current bank loans 103,947 / 104,442 in the balance sheet) that the statement does not show
  separately, so it cannot be split → stays in 5 with the note; bond issue net 3; bond repayment 8; lease 10.
* Restated columns: the 2025 comparative columns carry `(*` markers on financing values (`אשראי מתאגידים בנקאיים
  ואחרים, נטו`) with the footnote `*) סווג מחדש` (Q1) / `*) הוצג מחדש` (Q2) → Q1 c2, Q2 c2 and c4 flagged
  `restated` with column notes quoting the marked amounts (conventions §10).
* (*): interest paid in operating activities (`מזומנים ששולמו והתקבלו במהלך השנה עבור: ריבית ששולמה`) – Q1:
  (9,873) / (9,415) / (40,455); Q2: (12,868) / (25,876) / (2,995) / (16,461) / (40,455); note `פעילות שוטפת`. No
  dividends.
* **Source issue (recorded in `issues`)**: Q2 `קבלת אשראי` / `פירעון אשראי` show 280,000 / (280,000) in the
  Apr–Jun 2025 and 6M-2025 columns, but the FY-2025 column (179,203 / (204,120), same as in Q1) does not contain
  them – a gross receive-and-repay presented in the interim columns only; totals unaffected; C3 OK.
* Checks: C1 0; C2 OK 2 (line by line: e.g. 2025 `קבלת אשראי` 2,312 + 280,000 = 282,312); C3 OK 16.
* Overrides: `1905_Q1.json`, `1905_Q2.json` (header texts, restated flags + notes, line notes, report notes, issue).
* `validate.py --issuers 1905 --no-master`: **PASS 321 / FAIL 0**. Screenshots PDF: 8 pages viewed – OK.

---------------------------------------------------------------------------------------------------------------

## 2384 קרסו נדל"ן בע"מ

| | Q1 2026 | Q2 2026 |
|---|---|---|
| source | `2384_..._2026_Q1_1745641.pdf` (105 pp) | `2384_..._2026_Q2_1767254.pdf` (109 pp); `..._1767254-01.pdf` = appraisal (`נספח – שומה/הערכת שווי`), **not used** |
| statement | `דוחות תמציתיים מאוחדים על תזרימי המזומנים (באלפי ש"ח)`, pp. 46–47 | same, pp. 55–56 |
| financing | p. 47 (7 lines + total) | p. 56 (7 lines + total) |
| columns | 3M-31.03.2026, 3M-31.03.2025, FY-2025 | 6M-2026, 6M-2025, 3M Apr–Jun 2026, 3M Apr–Jun 2025, FY-2025 |
| units | באלפי ש"ח (in the statement title) | באלפי ש"ח |

* Mapping (auto suggestions confirmed, same in Q1/Q2): LT loans from banks and others 4 / 7; ST credit net 5;
  `חלוקת דיבידנד` 11; bonds 3 / 8; shares 1.
* **Source issue – misplaced value (Q1 report, Q1-2025 column):** 395,555 is printed on `הנפקת מניות (בניכוי
  הוצאות הנפקה)` and `-` on `הנפקת אגרות חוב`. The Q2 report (6M-2025 395,555 bonds / 129,686 shares; Apr–Jun 2025
  shares 129,686), the separate-company data of the same Q1 report (p. 61: bonds 395,555) and the statement of
  changes in equity (p. 44: no share issue in Q1-2025) show it was a **bond** issue. Following conventions §9
  ("assign each value to its correct line … and document how"), the printed value (digits unchanged) was assigned
  to the bonds line (item 3) and the shares line set to 0 for that column (`line_values`), documented in both line
  notes, a column note and an `issues` entry (→ master `חסרים והערות`). Totals unaffected; C2 per item now matches
  the Q2 report. (First pass kept it on the shares line with explained C2-item rows; changed for consistency with
  §9 – listed under mapping decisions.)
* (*): interest paid is not shown in any section; only in **appendix B** `ריבית ומיסים במזומן` (`ריבית ששולמה`,
  printed positive): Q1 15,605 / 13,751 / 130,043; Q2 72,824 / 59,586 / 57,219 / 45,835 / 130,043 (C2-consistent).
  Note `גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)`; the report note explains that the
  operating section only adds back `מימון נטו שלא במזומן`, so the payments are presumably in operating (capitalised
  interest within inventory/investment lines). `outside` replaced to give a bbox incl. the appendix title and its
  own column headers. Dividends paid only in financing; `דיבידנד לשלם` (appendix A) is non-cash.
* Restated: the 2025 columns carry `*` markers only on operating lines (retrospective policy change, note 2ב) →
  column notes, no restated flag (financing values not marked).
* Header texts cleaned (Q1 c1; Q2 c1, c2, c4 + `audit`); Q1 line 3 label spacing (`ואחרים, נטו`); Q1 header box
  bottom set to 157.0 pt (`boxes.47.header`) – the auto box overlapped the orange box by 2.7 pt (SCRIPT-ISSUE 3).
* Checks: C1 0; C2 OK 2; C3 OK 16 (`2384_checks.json` holds only a `_doc` note).
* Screenshots: the zoom is one continuous crop (financing heading directly under the header – pilot design: no
  boxes on the contiguous zoom; the full page carries the orange/blue boxes).
* `validate.py --issuers 2384 --no-master`: **PASS 325 / FAIL 0**. Screenshots PDF: 9 pages viewed – OK.

---------------------------------------------------------------------------------------------------------------

## 2386 ע.ע. יסודות איתנים ייזום ובניה בע"מ

| | Q1 2026 | Q2 2026 |
|---|---|---|
| source | `2386_..._2026_Q1_1744954.pdf` (70 pp) | `2386_..._2026_Q2_1767748.pdf` (126 pp) |
| statement | `דוחות תמציתיים מאוחדים על תזרימי המזומנים`, pp. 29 (all sections) – 30 (appendix A, non-cash) | same, pp. 32–33 |
| financing | p. 29 (11 lines + total) | p. 32 (12 lines + total; interest split in two lines) |
| columns | 3M-31.03.2026, 3M-31.03.2025, FY-2025 | 6M-2026, 6M-2025, 3M Apr–Jun 2026, 3M Apr–Jun 2025, FY-2025 |
| units | אלפי ש"ח | אלפי ש"ח |

* **C3 item difference 5/7 (392) resolved by aligning the mapping** (conventions §8): the two partner / interested-
  party loan lines swap their "net" wording between the reports – Q1 `פירעון הלוואות מבעלי עניין` vs Q2 `נטילת
  (פירעון) הלוואות מבעלי עניין` (FY-2025 (52) in both), and Q1 `קבלת (פירעון) הלוואה משותפים` vs Q2 `פירעון הלוואה
  משותפים` (FY-2025 (444) in both; Q2's line nets a Q1-2025 receipt of 125). Both instruments are borrowings with no
  stated term presented net in one of the reports → **5** in both reports (R3 "net, no stated term"). C3 now OK 16.
* `תמורה מהנפקה פרטית של מניות ואופציות` → **1** (auto: 2) – an unsplit share + option package (conventions §6).
* Convertible bond series ב' is presented in two lines (liability component / equity component, both net) → both 3.
* `קבלת/פירעון אשראי והלוואות מגופים פיננסיים` (gross, no term) → 5; note: the 2026 receipts include non-current
  credit (balance sheet 30.6.2026: current 60,711, non-current 49,318 – note 4א(1)) that the statement does not
  split → stays in 5 with a note (listed under mapping decisions).
* Interest paid only in financing (13; Q2: two lines – bank/financial credit and bond series ב'). No dividends paid.
  (*) info rows 0, no note.
* Labels fixed (`line_text`): apostrophes of `(סדרה א')` / `(סדרה ב')` and the note reference `(ראה ביאור 4א(1))`
  (the text layer had them mirrored); header texts completed.
* Checks: C1 0; **C2 2025: MISMATCH 1 explained** – source rounding: interest paid Q1-2025 (1,727) in Q1 vs (1,728)
  derived from Q2 → total 32,013 vs 32,012 (`2386_checks.json`, C2 total + C2-item 13); C2 2026 OK; C3 OK 16.
* `validate.py --issuers 2386 --no-master`: **PASS 333 / FAIL 0**. Screenshots PDF: 7 pages viewed – OK.

---------------------------------------------------------------------------------------------------------------

## 2429 לוזון רונסון אן.וי (Luzon Ronson N.V.)

| | Q1 2026 | Q2 2026 |
|---|---|---|
| source | `2429_..._2026_Q1_1742803.pdf` (52 pp) | `2429_..._2026_Q2_1764287.pdf` (55 pp) |
| statement | `דוח תמציתי מאוחד על תזרימי המזומנים` (Luzon Ronson N.V.), pp. 32–33 | same, pp. 34–35 |
| financing | p. 33 (8 lines + total) | p. 35 (8 lines + total) |
| columns | 3M-31.03.2026, 3M-31.03.2025, FY-2025 | 6M-2026, 6M-2025, 3M Apr–Jun 2026, 3M Apr–Jun 2025, FY-2025 |
| units | אלפי ש"ח (Hebrew statements of a foreign issuer) | אלפי ש"ח |

* Column c2 of Q1 flagged `דו-משמעית` by the extractor: confirmed on the image (3 months ended 31.3.2025, unaudited);
  header texts cleaned.
* Mapping (same in Q1/Q2; consistent with the parent 473): `קבלת הלוואה מהמיעוט` (Q1) → **4**; `קבלת (פירעון)
  הלוואה מהמיעוט` (Q2, netted) → **net_loans** (all values positive → 4). Balance sheet: `הלוואה מבעלי מניות מיעוט
  בחברות מוחזקות` mainly non-current (126,401 at 30.6.2026) → long-term loans from NCI holders, not equity (6).
  Others: dividend 11, lease 10, bonds 3/8, LT loans 4/7, ST loans from banks and others net 5.
* Lease line Q2: Apr–Jun 2026 prints **+53** (6M (2,223) − Q1 (2,276)); kept as printed (item 10) with a note.
* (*): interest paid in operating activities (`מזומנים ששולמו והתקבלו במהלך התקופה עבור: ריבית ששולמה`) – Q1:
  (32,773) / (20,823) / (70,406); Q2: (48,390) / (21,982) / (15,617) / (1,159) / (70,406). Dividends only in
  financing.
* Checks: C1 0; C2 OK 2 (line by line); C3 OK 16.
* `validate.py --issuers 2429 --no-master`: **PASS 326 / FAIL 0**. Screenshots PDF: 9 pages viewed – OK.

---------------------------------------------------------------------------------------------------------------

## 2449 קבוצת מיי טאון בע"מ

| | Q1 2026 | Q2 2026 |
|---|---|---|
| source | `2449_..._2026_Q1_1744151.pdf` (60 pp) | `2449_..._2026_Q2_1764920.pdf` (62 pp) |
| statement | `תמצית דוח על תזרימי מזומנים ביניים מאוחד`, pp. 44 (all sections) – 45 (appendix A) | same, pp. 45–46 |
| financing | p. 44 (4 lines + total) | p. 45 (4 lines + total) |
| columns | 3M-31.03.2026, 3M-31.03.2025 **(מוצג מחדש)**, FY-2025 | 6M-2026, 6M-2025 **(מוצג מחדש)**, 3M Apr–Jun 2026, 3M Apr–Jun 2025 **(מוצג מחדש)**, FY-2025 |
| units | אלפי ש"ח (in every column header) | אלפי ש"ח |

* Restated: the 2025 interim column headers print `2025*` with `(*) הוצג מחדש ראה ביאור 2 (ד)` – the column
  header itself says restated (conventions §10) → `restated` + column note (note 2(ד): retrospective application of
  the ISA staff position on urban-renewal combination transactions – inventory, payables, revenue; the financing
  values equal the Q2-derived ones). FY-2025 is not starred.
* Mapping: `קבלת אשראי מתאגידים בנקאיים` → 5 (no term; balance-sheet bank credit mainly current; prints negative
  amounts in the 2025 columns → effectively a net line); lease 10; `עמלות וריביות ששולמו` 13 (fees included –
  noted); `פירעון קרן אג"ח` 8.
* (*): interest paid only in financing; appendix A has no interest line; Q2 operating shows only `מיסים ששולמו`.
  No dividends. Info rows 0, no note.
* Checks: C1 0; C2 OK 2 (line by line); C3 OK 16.
* `validate.py --issuers 2449 --no-master`: **PASS 318 / FAIL 0**. Screenshots PDF: 7 pages viewed – OK.

---------------------------------------------------------------------------------------------------------------

## 2522 עומר הנדסה ובניה (1986) בע"מ

| | Q1 2026 | Q2 2026 |
|---|---|---|
| source | `2522_..._2026_Q1_1744985.pdf` (32 pp) | `2522_..._2026_Q2_1766495.pdf` (34 pp) |
| statement | consolidated statement of cash flows – TOC: `דוחות מאוחדים על תזרימי המזומנים` printed pp. 6–8 = PDF pp. 25 (all sections), 26 (appendix A), **27 (appendix B, added)** | `דוחות מאוחדים על תזרימי המזומנים (באלפי ש"ח)`, PDF pp. 27, 28 (appendix A), 29 (appendix B) |
| financing | p. 25 (4 lines + total) | p. 27 (5 lines + total) |
| columns | 3M-31.03.2026, 3M-31.03.2025, FY-2025 | 6M-2026, 6M-2025, 3M Apr–Jun 2026, 3M Apr–Jun 2025, FY-2025 |
| units | באלפי ש"ח | באלפי ש"ח |

* Flag `כותרת העמוד מציינת 'באורים'`: the Q1 statement pages carry the running header `באורים לדוחות הכספיים
  המאוחדים ליום 31 במרץ 2026 (באלפי ש"ח)` (a layout quirk); the TOC (p. 19) lists `דוחות מאוחדים על תזרימי
  המזומנים 6-8` and `tool_scan` finds no other cash-flow statement → confirmed as the consolidated statement.
  `cf_pages` extended to include p. 27 (appendix B, printed page 8 – part of the statement per the TOC) and re-extracted
  (lines unchanged).
* Mapping: LT bank loans 4 / 7 (Q2 prints `קבלת/פירעון הלוואות מתאגידים בנקאיים` without "לזמן ארוך" – same lines
  as Q1 (FY-2025 identical) → 4 / 7 as in Q1, noted); `דיבידנד ששולם לבעלי מניות החברה` (Q2) 11; lease 10; share
  issue 1.
* (*): interest paid is presented in **appendix A** under the operating adjustments (`מזומנים ששולמו והתקבלו במהלך
  השנה עבור: ריבית ששולמה`, part of `התאמות הדרושות להצגת מזומנים ... מפעילות שוטפת`), so the section is known →
  note `גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת` (conventions §1). Q1: (6,132) / (7,007) / (27,111);
  Q2: (12,181) / (13,905) / (6,049) / (6,898) / (27,111). `outside` replaced (bbox incl. the sub-heading) and
  `boxes.<p>.header` added on the appendix page so the red crop shows the column headers (SCRIPT-ISSUE 1).
  Dividends: paid 25,000 in Q2 (financing, item 11); the Q1 appendix B `דיבידנד שהוכרז וטרם שולם` 25,000 is
  non-cash (not (*)).
* Checks: C1 0; C2 OK 2; **C2-item INFO 2 (explained)** – Q1-2026 LT loans received / repaid 131,158 / (140,389) in
  Q1 vs 8,157 / (17,388) derived from Q2: both higher by 123,001 (gross vs net presentation of a refinancing, net
  and total identical) → `2522_checks.json` + column notes (like the pilot's 1,267 in 1618); C3 OK 16.
* `validate.py --issuers 2522 --no-master`: **PASS 321 / FAIL 0**. Screenshots PDF: 11 pages viewed – OK.

---------------------------------------------------------------------------------------------------------------

## 2559 קבוצת בסט א.ע.ו בע"מ

| | Q1 2026 | Q2 2026 |
|---|---|---|
| source | **`2559_..._2026_Q1_1771495-01.pdf`** (51 pp, `דוח מתקן`) – see below | `2559_..._2026_Q2_1767813.pdf` (57 pp) |
| statement | `דוחות מאוחדים על תזרימי המזומנים`, pp. 24–25 of `-01` | same title, pp. 31–32 |
| financing | p. 25 (8 lines + total) | p. 32 (10 lines + total) |
| columns | 3M-31.03.2026, 3M-31.03.2025, FY-2025 | 6M-2026, 6M-2025, 3M Apr–Jun 2026, 3M Apr–Jun 2025, FY-2025 |
| units | אלפי ש"ח (in the column header of the statement page; the extractor's flag "units from p. 20" is moot) | אלפי ש"ח |

* **Q1 source decision (R1):** the main file `..._1771495.pdf` (3 pp) is an excerpt/cover; `-01` (51 pp) and `-02`
  (54 pp) are the same `דוח מתקן` – an amended report to the 31.3.2026 statements included in the prospectus of
  29.5.2026, issued because of a material error (disclosure of interested-party transactions in the 31.12.2025
  statements; re-approved 15.9.2026; restatement in note 2ב). `-01` is the clean complete version → **data source**;
  `-02` is the marked-up version. The `-02` financing section (p. 27, word layer) was compared value by value with
  `-01` p. 25: **identical** (all 9 lines × 3 columns) → nothing to flag. (Phase A reached the same conclusion.)
* Q1 text layer: `usable (repaired)` (broken `נ` glyph) – every label compared with the image: correct.
* Q2: `הנפקת מניות, נטו` c1/c3 – the text layer reads `3872,19` (misplaced comma), the image shows **387,219** (=
  IPO proceeds per the note); parsed value correct, noted. Q2 pick (pp. 31–32) confirmed: the earlier block pp. 13–14
  is the board report's liquidity section (`7. נזילות`); p. 55 is the separate (38D) data.
* Mapping decisions:
  * **C3 item difference 5/7 (16,628) resolved by aligning:** Q1 `פירעון הלוואות מתאגידים מוחזקים ובעלי עניין`
    (prints +2,707 in Q1-2026, i.e. a net line) and Q2 `קבלת (פרעון) הלוואות מתאגידים מוחזקים ובעלי עניין` are the
    same line (FY-2025 (16,628) in both) – borrowings presented net with no stated term → **5** in both. C3 OK 16.
  * `קבלת הלוואות מבעלי עניין` → 4 (balance sheet: interested-party loans mainly non-current – 287,418 non-current /
    32,499 current at 30.6.2026).
  * **`תשלום לבעל עניין בגין התאמת תמורה` (Q2, (52,500))** → **1, negative**. Per the note (p. 46): investor
    הפניקס was entitled, on an IPO, to compensation of 5% of the group's value increase capped at 52.5 M NIS
    ("התאמת התמורה"); paid in June 2026 on the IPO and **charged to equity** (also a line of the statement of changes
    in equity, p. 26). An equity transaction with a shareholder that adjusts the consideration for shares issued to
    it → nearest item by nature is 1 (share issuance, net); not a dividend, not a buy-back. Alternative: `אחר`.
    → **Phase C to align** (listed below).
  * Others: LT bank loans 4 / 7 (Q2 Apr–Jun 2026 receipts print **(30,547)** – 6M 155,185 < Q1 185,733; kept as
    printed, noted), ST bank credit net 5, lease 10, dividend 11, interest 13 (all in financing).
* (*): interest and dividends paid are presented only in financing; `ריבית שהתקבלה` / `דיבידנד שהתקבל` are receipts.
  Info rows 0.
* Restatement: `(*)/(**) הוצג מחדש, ראה באור 2ב'` markers appear only on **operating** values (Q1: 2025 interim and
  FY columns; Q2: FY column) – financing values are not marked → column notes, no `(מוצג מחדש)` flag (conventions
  §10).
* Checks: C1 0; C3 OK 16; C2 2026 OK; **C2 2025 MISMATCH −2 explained** (source rounding: LT repayments (1,451) vs
  (1,450) and ST credit 4,528 vs 4,529); C2-item INFO 4 explained (±1 rounding: 2026 items 4/5 offsetting, 2025
  items 5/7) – `2559_checks.json`.
* Overrides: `2559_Q1.json`, `2559_Q2.json` (items, notes, header texts, column notes, report notes, verified),
  `2559_checks.json`.
* `validate.py --issuers 2559 --no-master`: **PASS 330 / FAIL 0**. Screenshots PDF: 7 pages – OK (thumbnail sheet).

---------------------------------------------------------------------------------------------------------------

## Mapping decisions (cross-company judgement calls for Phase C)

| # | case (issuer) | decision | reason / alternative |
|---|---|---|---|
| 1 | Loans from NCI holders of subsidiaries – `קבלת הלוואה מהמיעוט` (473 Q1/Q2, 2429 Q1); `קבלת (פירעון) הלוואה מהמיעוט` (2429 Q2) | **4** (Q2 2429: `net_loans` → 4, all positive) | R3 lists NCI holders among the lenders of item 4; balance sheet: mainly non-current liability. Item 6 kept for NCI equity contributions. |
| 2 | Buy-back of the company's own warrants – `רכישת כתבי אופציה` (473, 2025) | **9** | Self-purchase of own equity instruments (charged to equity); not an exercise (2). Alternative: 2 (negative). |
| 3 | Loans from the parent company, no term on the line, balance shown as current (`יתרות זכות לחברה האם`) – gross receipt/repayment lines (1903) | **5** | R3 "short-term credit/loans from … other lenders, net or gross". Auto had 4/7. |
| 4 | Credit from a financial institution, no term, gross lines (1903) | **5** | Balance sheet: current `אשראי מתאגידים פיננסיים`. |
| 5 | Same borrowing line presented net in one report and as a repayment in the other (2386: interested-party loans, partner loans; 2559: loans from investees and interested parties) | **5 in both reports** | R3 "net, no stated term"; conventions §8 (same line → same item); resolves the Phase-A C3 5/7 differences of 2386 (392) and 2559 (16,628). |
| 6 | Unsplit share + option private placement – `תמורה מהנפקה פרטית של מניות ואופציות` (2386) | **1** | Conventions §6. Auto had 2. |
| 7 | Convertible bonds presented as liability component + equity component lines (2386) | **3** (both lines) | R3 item 3 "incl. convertibles". |
| 8 | Gross "credit" receipts that include an unsplittable long-term loan (1905 `קבלת אשראי` incl. an 86.1 M NIS land loan; 2386 `קבלת אשראי והלוואות מגופים פיננסיים` incl. non-current credit) | **5** with a note | The statement does not split; the line is credit without a stated term. |
| 9 | Line labelled long-term in one report and without a term in the other (2522 Q2 `קבלת/פירעון הלוואות מתאגידים בנקאיים`) | **4 / 7** as in the other report | Same line (FY-2025 identical). |
| 10 | **IPO price-adjustment payment to an investor, charged to equity** – `תשלום לבעל עניין בגין התאמת תמורה` (2559 Q2, (52,500)) | **1 (negative)** | Equity transaction adjusting the consideration for shares issued to the investor. Alternative: `אחר`. Please align. |
| 11 | **Value printed on the wrong line** (2384 Q1, Q1-2025: 395,555 printed on the shares line; all other evidence says bonds) | assigned to the **bonds line (3)** via `line_values`, documented | Conventions §9 (misaligned values → correct line, documented); digits unchanged. Alternative: keep on the shares line and explain C2-item. |
| 12 | Restated flag | `(מוצג מחדש)` set only when the column header is starred (2449) or the restatement markers sit on **financing** values in that column (1903, 1905); markers on operating values only (2384, 2559) → column note only | Conventions §10. |
| 13 | (*) interest disclosed only in an appendix | appendix with no section stated (1330 `נספח ב'`, 2384 `נספח ב'`) → `… – הסעיף לא צוין (לא בפעילות מימון)`; appendix that is part of the operating reconciliation (2522 `נספח א'`) → `… – נכלל בפעילות שוטפת` | Conventions §1. Values as printed (positive in 1330/2384, negative in 2522). |
| 14 | `ריבית ועמלות ששולמו` / `עמלות וריביות ששולמו` (1903, 2449) | **13** with a note "כולל עמלות" | PIPELINE §7. |

---------------------------------------------------------------------------------------------------------------

## SCRIPT-ISSUEs

```
SCRIPT-ISSUE 1
  script:     finalize_report.py auto_geometry / fcf_render.py report_images (§3 (*) crops)
  report:     1330 Q1 (p. 54), 1330 Q2 (p. 58), 2522 Q1 (p. 26), 2522 Q2 (p. 28) – (*) lines on appendix pages
  symptom:    on a statement page that carries only (*) lines (no financing lines, no column header detected),
              the red (*) crop's header strip shows only the company name / page title – the column headers
              (periods) of the appendix are missing, so the crop does not show which value is which period.
  expected:   the (*) crop should include the page's column-header strip (as on operating pages).
  workaround: `boxes.<p>.header` (title + column headers of the appendix) in the override; for 2384/2522 also an
              `outside` bbox that includes the appendix's own sub-heading/column headers.
  severity:   cosmetic
```

```
SCRIPT-ISSUE 2
  script:     fcf_extract.py (column header text)
  report:     473 Q1/Q2, 1330 Q1/Q2, 1903 Q1/Q2, 1905 Q1/Q2, 2384 Q1/Q2, 2386 Q1/Q2, 2429 Q1/Q2, 2449 Q1/Q2,
              2522 Q1/Q2, 2559 Q1/Q2
  symptom:    `header_text` (the verbatim column-header row of the workbook) often contains fragments of the page
              title or other columns, misses the day/month, or holds mirrored units ('אלפי ח"ש'); months / end date
              / labels were nevertheless correct in every case.
  expected:   the verbatim header of each column only.
  workaround: `columns.cN.header_text` (and `audit`) set from the image.
  severity:   cosmetic
```

```
SCRIPT-ISSUE 3
  script:     finalize_report.py header_bottom / auto_geometry
  report:     2384 Q1 (p. 47)
  symptom:    the auto header box ends at header_y1 + 5 = 160.4 pt while the financing box starts at 157.7 pt
              (the financing heading follows the units row directly) – the blue and orange boxes overlap by 2.7 pt
              (white space only, no text hidden).
  expected:   header box bottom ≤ financing box top.
  workaround: `boxes.47.header` = [58.2, 39.7, 542.7, 157.0].
  severity:   cosmetic
```

```
SCRIPT-ISSUE 4
  script:     fcf_extract.py (labels)
  report:     1903 Q1/Q2 (`פירעון אגרות חוב`), 2386 Q1/Q2 (apostrophes of `(סדרה א')`/`(סדרה ב')`, `(ראה ביאור 4א(1))`)
  symptom:    the note-reference column ("6(ו')") was glued to the label (`פירעון אגרות חוב 1ו(')`); mirrored
              apostrophes / parentheses inside series names and note references.
  expected:   verbatim label without the note-reference column; parentheses/apostrophes in logical order.
  workaround: `line_text`.
  severity:   cosmetic (labels only; values unaffected)
```

---------------------------------------------------------------------------------------------------------------

## Final status (batch 7)

| issuer | company | Q1 | Q2 | company outputs | checks | validate `--no-master` |
|---|---|---|---|---|---|---|
| 473 | קבוצת עמוס לוזון יזמות ואנרגיה | verified | verified | built (no draft) | 0 unexplained | PASS 336 / FAIL 0 |
| 1330 | פרשקובסקי השקעות ובניין | verified | verified | built | 0 unexplained | PASS 325 / FAIL 0 |
| 1618 | קבוצת אשטרום (pilot) | pilot-verified | pilot-verified | rebuilt in Phase A (T1/T2) – unchanged | 0 unexplained (C2-item INFO 2) | PASS 338 / FAIL 0 |
| 1903 | קבוצת יובלים השקעות | verified | verified | built | 0 unexplained | PASS 330 / FAIL 0 |
| 1905 | גלעד מאי | verified | verified | built | 0 unexplained | PASS 321 / FAIL 0 |
| 2384 | קרסו נדל"ן | verified | verified | built | 0 unexplained | PASS 325 / FAIL 0 |
| 2386 | ע.ע. יסודות איתנים | verified | verified | built | 0 unexplained (C2 2025 ±1 explained) | PASS 333 / FAIL 0 |
| 2429 | לוזון רונסון אן.וי | verified | verified | built | 0 unexplained | PASS 326 / FAIL 0 |
| 2449 | קבוצת מיי טאון | verified | verified | built | 0 unexplained | PASS 318 / FAIL 0 |
| 2522 | עומר הנדסה ובניה (1986) | verified | verified | built | 0 unexplained (C2-item ±123,001 explained) | PASS 321 / FAIL 0 |
| 2559 | קבוצת בסט א.ע.ו | verified (`-01`) | verified | built | 0 unexplained (C2 2025 −2 + 4 C2-item ±1 explained) | PASS 330 / FAIL 0 |

20 reports verified in this batch (+ 2 pilot reports of 1618 checked), 11 companies built without `--draft`;
nothing blocked. Temp folders `%TEMP%\fcf_run\<iss>\` of the 11 issuers deleted at the end (`_runs` left for
Phase C).

Assisted-by: Anthropic:Claude Opus 5.5

