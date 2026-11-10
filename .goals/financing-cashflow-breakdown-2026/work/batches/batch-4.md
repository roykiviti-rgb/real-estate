# Phase B — Batch 4 report (iteration 1)

Builder: Phase B batch 4. Date: 2026-11-10 (10:13–11:35).
Issuers (exclusive): 111 (Q2 only) · 400 · 539 · 1083 · 1502 · 1553 · 1622 · 2481 · 2483 · 2488 · 2524 — 11 companies, 21 reports.
Protocol: `work\PIPELINE.md` §0–§13 + `work\phaseB-conventions.md`. Checkpoint: `work\batches\batch-4-progress.md`.

## Summary

| issuer | company | reports | final status | checks | `validate.py --issuers <iss> --no-master` |
|---|---|---|---|---|---|
| 111 | י.ב התחדשות הארץ- מתחמי מגורים | Q2 (Q1 missing) | verified + built | C1 OK | PASS 137 / FAIL 0 |
| 400 | אחים דוניץ | Q1, Q2 | verified + built | all OK | PASS 323 / FAIL 0 |
| 539 | רוטשטיין נדל"ן | Q1, Q2 | verified + built | C2 −1 explained | PASS 332 / FAIL 0 |
| 1083 | קרדן נדל"ן יזום ופיתוח | Q1, Q2 | verified + built | all OK | PASS 328 / FAIL 0 |
| 1502 | מירלנד (USD) | Q1, Q2 | verified + built | all OK | PASS 313 / FAIL 0 |
| 1553 | אלמוגים החזקות | Q1, Q2 | verified + built | all OK | PASS 325 / FAIL 0 |
| 1622 | אקסטל (USD) | Q1, Q2 | verified + built | all OK | PASS 339 / FAIL 0 |
| 2481 | אלמוג (כ.ד.א.י.) | Q1, Q2 | verified + built | all OK | PASS 332 / FAIL 0 |
| 2483 | קבוצת גבאי | Q1, Q2 | verified + built | C1 +5 (source) and C2 −1 explained | PASS 330 / **FAIL 1** = SCRIPT-ISSUE 1 (not a data error) |
| 2488 | קבוצת אופק | Q1, Q2 | verified + built | C2 −2 explained | PASS 325 / FAIL 0 |
| 2524 | אי.אס.איי אחזקות | Q1, Q2 | verified + built | C2 +1 explained | PASS 324 / FAIL 0 |

- `checks.py --issuers` (all 11): C1 82 OK + 1 MISMATCH, C2 16 OK + 4 MISMATCH, C2-item 6 INFO, C3 160 OK. **Unexplained mismatches: 0.** Explanations: `overrides\539_checks.json`, `2483_checks.json`, `2488_checks.json`, `2524_checks.json`.
- Final build at 11:31 (`build_company.py`, no `--draft`): 11/11 companies. A text scan found no draft marker (`טיוטה`) in any of the 11 screenshot PDFs or 11 workbooks.
- Each company folder holds exactly its source PDFs plus the 2 outputs.
- `tool_integrity.py`: **CLEAN**.

## How the numbers were verified, and the image-cap incident

**What went wrong.** The `view` tool shows at most about 50 images per context window. Beyond that it answers "Viewed image file successfully … You've reached the maximum number of images (50)" and displays nothing. I only spotted this partway through, and at first I misjudged where it stopped. A strict audit of my own tool results gives this picture:

- **Not displayed (none of these count as evidence):** every image I viewed from the start up to and including the 1553 screenshot pages s3/s4 (about 10:41). That covers:
  - every image of 111, 400, 539, 1083 and 1502 (fin renders, full pages, grids, screenshot pages);
  - the 1553 fin render, full pages, and screenshot pages s3/s4.
  - In-session notes such as "re-verified visually at 10:30" and "displayed again from 1083 s3" were wrong. The checkpoint now says so.
- **Displayed:**
  - 1553 screenshot pages s2, s6, s7 and s8 (10:41);
  - 1622 Q1 and Q2: fin renders, full pages 51, 52, 56, 57 and 58, note page 67, the EX/CPS note on p.85, and screenshot pages s2, s3, s5 and s6 (10:42–10:47);
  - 2481 Q1 and Q2: fin renders and pages 35, 36, 38, 40 and 41 (10:48–10:52).

Every `verified` record therefore rests on images that were **actually displayed**, in three independent layers:

1. **Read-only sub-agent check (11:05–11:12)**, one agent per company or pair of companies, each with a fresh image budget. Each agent compared every header, unit, label, digit and (*) line, plus all screenshot pages, against the images, zooming to 300/600 DPI where a digit was uncertain. Each listed the images it actually saw, and every list had "NOT SEEN: none".
   - Result: 21/21 PASS, except one defect: 1622 Q1 line 10 is printed `מ-Extell` without a space. Fixed through `line_text`.
2. **Builder re-check on composite images**, after the orchestrator alert. `compose.py` stacks several crops into one PNG. I confirmed each composite displayed before relying on it, and compared every digit, label, header, unit and (*) line:

   | time | reports | composite (`%TEMP%\fcf_run\111\b4\`) |
   |---|---|---|
   | 11:17 | 111 Q2 (fin p.16 + (*) crop) | `comp_111Q2_111748` |
   | 11:19 | 400 Q1 / 400 Q2 (fin + (*)) | `comp_400Q1_111836`, `comp_400Q2_111837` |
   | 11:19 | 539 Q1 / 539 Q2 (fin + (*)) | `comp_539Q1_111838`, `comp_539Q2_111838` |
   | 11:20 | 1083 Q1 (*) crops [1] + [2]; 1622 Q1 line-10 label at 400 DPI | `comp_1083Q1x_111839` |
   | 11:20 | 2483 Q1 + Q2 (fin) | `comp_2483_111839` |
   | 11:21 | 2488 Q1 + Q2 (fin) | `comp_2488_111840` |
   | 11:21 | 2524 Q1 + Q2 (fin) | `comp_2524_111841` |
   | 11:21 | 1083 Q2 (fin + both (*) lines) | `comp_1083Q2_112148` |
   | 11:22 | 1083 Q1 (fin); 1553 Q1 (fin + (*)) | `comp_1083Q1_1553Q1_112218` |
   | 11:22 | 1502 Q1 + Q2 (fin + (*)) | `comp_1502_112219` |
   | 11:28 | final screenshot pages (1083 p.5, 539 p.2, 2483 p.6) | `comp_finalshots_112832` |

   - Everything matched; no data change was needed. These composites were deleted from TEMP at the end (temp hygiene), so the table records which crops each one contained.
   - Not re-done with composites, because my own earlier views were displayed: 1553 Q2 (s6/s7/s8), 1622 Q1/Q2, and 2481 Q1/Q2.
3. **Automated:**
   - C1 = 0 in every column, except the one documented source inconsistency.
   - C2/C3 run against the other report.
   - A text-layer scan (`star_scan`) of every statement page for interest and dividend rows. Every row of interest or dividends *paid* is recorded, either in financing (items 11/12/13) or as a (*) line. Only receipts and non-cash items are excluded.

The `verified.method` text of every report states which displayed images it rests on, and that my first views were not displayed.

**Lesson for later work:** use composite images, check that each image actually displayed, and give each sub-agent a fresh context for its image views.

---------------------------------------------------------------------------------------------------------------

## Per company

Values below are in the report's own units. Payments are negative. "fin" means the page that holds the financing section.

### 111 — י.ב התחדשות הארץ- מתחמי מגורים בע"מ (Q2 only; Q1 missing, stated in the workbook)

**Source, columns, units**
- Source: `111_..._2026_Q2_1767282.pdf` (32 pp). The statement is on pp.16–17: p.16 holds operating, investing and financing; p.17 holds appendices A and B. fin = p.16.
- Columns: 6M-30.06.2026, 6M-30.06.2025 **(מוצג מחדש)**, FY-2025.
- Units: אלפי ש"ח.

**Restated column**
- In the 6M-2025 column the values 23, 702, 422 and (250) carry `*`, with the footnote `* סיווג לא מהותי במספרי השוואה` (an immaterial reclassification of comparatives).
- Per conventions §10, a note attached to the column says it is reclassified, so the column is flagged `restated` and carries a column note. The flag does not affect any amount.
- See mapping decision M10.

**Mapping**

| line | item | reason |
|---|---|---|
| תמורה מהנפקת מניות | 1 | |
| תמורה ממימוש אופציות | 2 | |
| תמורה מהנפקת אופציות | 2 | warrants on their own line, per R3 |
| קבלת הלוואה מאחרים / פירעון הלוואה מאחרים | 5 | gross lines with no stated term; the balance sheet at 30.06.2025 shows them as current `הלוואות לזמן קצר` (561) |
| פירעון הלוואה מצד קשור | 7 | early repayment of a 78-month owner loan, 1,562 in cash (note 3א) |
| פירעון התחייבויות בגין חכירה | 10 | |

**(*) lines:** `ריבית ששולמה` in operating: 6M-2026 blank (0), 6M-2025 `-`, FY (181).

**Overrides:** columns (restated, header_text), line_items, line_notes, column_notes, report_notes, text_layer, verified.

**Checks:** C1 0 in all 3 columns. C2/C3 are not applicable (no Q1 report).

**Validate:** PASS 137 / FAIL 0.

### 400 — אחים דוניץ בע"מ

**Sources, columns, units**
- Q1: `400_..._Q1_1745054.pdf` (51 pp), pp.33–34, fin p.33.
- Q2: `400_..._Q2_1767345.pdf` (55 pp), pp.37–38, fin p.37.
- Columns: 3 in Q1, 5 in Q2.
- Units: `(באלפי ש"ח)` in the title.

**Mapping**

| line | item | reason |
|---|---|---|
| אשראי מתאגידים בנקאיים, נטו | 5 | |
| פרעון התחייבות בגין חכירה | 10 | |
| הנפקה אגרות חוב (Q1, as printed) / הנפקה אגרת חוב, נטו (Q2) | 3 | `נטו` = net of issue costs; repayments are on a separate line |
| פרעון אגרות חוב (Q1) / פרעון אגרות חוב, נטו (Q2) | 8 | |
| רכישת מניות באוצר | 9 | |
| דיבידנד ששולם | 11 | |
| מימוש אופציות לעובדים (Q2) | 2 | |

**(*) lines:** interest paid in operating.
- Q1: (7,626) / (8,646) / (43,106).
- Q2: (25,149) / (20,099) / (17,523) / (11,454) / (43,106).
- `הכרזה על דיבידנד שטרם חולק` (p.34) is non-cash and was excluded.

**Checks:** C1 8/8, C2 2/2, C3 16/16 OK.

**Source note (information only):** interest paid in operating for 6M-2025 is printed (20,099), while Q1 + Q2-3M gives 20,100. This is a 1-unit rounding difference in a (*) row, not a financing item.

**Validate:** PASS 323 / FAIL 0.

### 539 — רוטשטיין נדל"ן בע"מ

**Sources, columns, units**
- Q1: `539_..._Q1_1744508.pdf` (85 pp), pp.55–56, fin p.56.
- Q2: `539_..._Q2_1765452.pdf` (95 pp), pp.58–60, fin p.59.
- The Q2 file `-01` is an appraisal and is not a data source (also stated in the report notes).
- Units: אלפי ש"ח.

**Mapping**

| line | item | reason |
|---|---|---|
| פירעון אגרות חוב של החברה | 8 | |
| הנפקת אגרות חוב (בניכוי הוצאות הנפקה) | 3 | |
| פירעון אשראי לזמן ארוך מתאגידים בנקאיים | 7 | |
| קבלת הלוואה לזמן ארוך מתאגידים בנקאיים ואחרים | 4 | |
| פירעון התחייבות בגין חכירה | 10 | |
| קבלת (פירעון) אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו | 5 | |
| דיבידנד ששולם לבעלי מניות החברה | 11 | |
| **הנפקת חבילה** | 1 | shares plus warrants issued to Clal institutions; the statement of changes in equity shows 484 + 27,150 + 2,702 options reserve = 30,336; no bonds in the package (conventions §6) |
| **הנפקת מניות** | **2** | see M3 |
| רכישת מניות באוצר | 9 | |

`הנפקת מניות` → 2 (M3): per the statement of changes in equity (Q1 pp.52–54, Q2 pp.55–57) every amount on this line is an option or warrant exercise:
- 2026: 26,050 from exercise of the package warrants (note 4ג) plus 25 from employee options, = 26,075.
- 2025: employee options.

**(*) lines:** interest paid in operating.

**Overrides**
- `boxes.<p>.header` with x0 = 51 on pp.55, 56, 58 and 59. The auto header box cut the company logo, a vector drawing at x 57.3–160, y 31–53.5; the auto box started at x0 61.3 / y0 38.7 on Q1 (SCRIPT-ISSUE 3).
- header_text, line_items {9: 2}, notes.

**Checks:** C1 OK. C3 16/16 OK.
- C2 3M-2025 total −1 (Q1 73,424; Q2 145,422 − 71,997 = 73,425) is rounding in item 5 (48,266 vs 48,267). Explained in `539_checks.json`.

**Validate:** PASS 332 / FAIL 0.

### 1083 — קרדן נדל"ן יזום ופיתוח בע"מ

**Sources, columns, units**
- Q1: `1083_..._Q1_1742346.pdf` (71 pp), pp.48–50, fin p.49.
- Q2: `1083_..._Q2_1763408.pdf` (73 pp), pp.49–51, fin p.50.
- The tables on pp.32 (Q1) and 31–32 (Q2) are the board report's liquidity tables and were not used.
- Units: אלפי ש"ח.

**Text layer:** words of each line are stored in reverse order; Q2 also has the broken `נ` font ("usable (repaired)"). Every label was compared with the image.

**Mapping**

| line | item |
|---|---|
| קבלת הלוואות לזמן ארוך מתאגידים בנקאיים | 4 |
| אשראי לזמן קצר מתאגידים בנקאיים, נטו | 5 |
| פרעון אגרות חוב | 8 |
| פרעון התחייבויות בגין חכירות | 10 |
| תמורה ממימוש אופציות לעובדים | 2 |
| הנפקת אגרות חוב (בניכוי הוצאות הנפקה) | 3 |
| חלוקה לבעלי זכויות שאינן מקנות שליטה | 12 |
| דיבידנד ששולם לבעלי מניות החברה | 11 |

**(*) interest:** two lines per report.
- Operating `ריבית ששולמה`: Q1 (2,478) / (1,374) / (17,849); Q2 (18,591) / (8,844) / (16,113) / (7,470) / (17,849).
- Below the statement, item `ב) ריבית ששולמה והוונה למלאי`, printed **without parentheses**:
  - Q1 (p.50): 2,709 / 3,798 / 23,751.
  - Q2 (p.51): 9,476 / 11,686 / 6,767 / 7,888 / 23,751.
- It is recorded as **negative** so the info row shows the total interest paid outside financing (Q1 −5,187 / −5,172 / −41,600). The note explains this, and it matches batch 2's treatment of the parent 121 (see M9).
- `דיבידנד ... שהוכרז וטרם שולם` is non-cash and was excluded.

**Source note:** the Q2 total 6M-2026 reads `1,3805` in the text layer; the image shows 13,805, which equals the sum of the lines and the board-report table.

**Checks:** C1 / C2 / C3 all OK.

**Validate:** PASS 328 / FAIL 0.

### 1502 — מירלנד דיוולופמנט קורפריישן פי אל סי (USD thousands)

**Sources, columns, units**
- Q1: `1502_..._Q1_1744791.pdf` (83 pp), pp.38–40, fin p.39.
- Q2: `1502_..._Q2_1767654.pdf` (84 pp), pp.39–41, fin p.40.
- Units: אלפי דולר ארה"ב.

**Content**
- Q1: the financing section is only the heading line `תזרימי מזומנים מפעילות מימון`, with `-` in all 3 columns and no detail lines. The heading line serves as the reported total (0).
- Q2: one line, `פירעון הלוואות מתאגידים בנקאיים ואחרים`, `-` in all columns → item 7 (by nature; the balance sheet shows only bonds). The total `מזומנים נטו ששימשו לפעילות מימון` is `-` in all columns.
- Every item and every total is 0.

**(*) lines:** `ריבית ששולמה` in operating is `-` in all columns. The info note says so explicitly.

**Not cash flows:** p.40 / p.41 show the conversion of bonds into shares, a non-cash item.

**Checks:** all OK (zero).

**Validate:** PASS 313 / FAIL 0.

### 1553 — אלמוגים החזקות בע"מ

**Sources, columns, units**
- Q1: `1553_..._Q1_1745440.pdf` (72 pp), pp.46–47, fin p.47.
- Q2: `1553_..._Q2_1763612.pdf` (76 pp), pp.49–50, fin p.50.
- Units: אלפי ש"ח (printed per column).

**Mapping**

| line | item | reason |
|---|---|---|
| פירעון אגרות חוב | 8 | |
| תמורה מהנפקת הון, נטו | 1 | |
| תמורה מהנפקת אגרות חוב, נטו | 3 | |
| קבלת (פירעון) אשראי לזמן קצר מתאגידים בנקאיים, נטו | 5 | |
| **קבלת (פירעון) הלוואות בגין פרויקטים, נטו** | 5 | project-finance loans presented net with no term; current liabilities in the balance sheet (909,889) – M2 |
| קבלת (פירעון) הלוואות מתאגידים בנקאיים לזמן ארוך | `net_loans` | all values ≤ 0, so item 7 |
| דיבידנד ששולם (Q2) | 11 | |
| פירעון התחייבות בגין חכירה | 10 | |

**(*) lines:** interest paid in operating.
- Q1: (15,719) / (11,695) / (72,756).
- Q2: (44,987) / (29,941) / (29,268) / (18,246) / (72,756).

**Overrides:** `line_text` corrects the text layer's `יפרעון` to `פירעון` on the lease line.

**Checks:** all OK.

**Validate:** PASS 325 / FAIL 0.

### 1622 — אקסטל לימיטד / Extell Limited (USD thousands)

**Sources, columns, units**
- Q1: `1622_..._Q1_1745241.pdf` (107 pp), pp.51–52, fin p.52.
- Q2: `1622_..._Q2_1766453.pdf` (117 pp), pp.56–58, fin p.57.
- Not used: p.44 is the cash-flow statement of the investee Smitell II LLC; the English pages are the statements of EX/CPS Holding LLC and of Extell Holdings I LLC.
- Units: `באלפי דולר ארה"ב, למעט אם צוין אחרת`.

**Mapping** (Q1: 13 lines, Q2: 15 lines)

| line | item | reason |
|---|---|---|
| השקעות הון על ידי בעל שליטה | 1 | |
| השקעות הון על ידי בעלי זכויות שאינן מקנות שליטה | 6 | |
| **החזר הון לבעלי זכויות שאינן מקנות שליטה** | 12 | NCI capital withdrawals tied to EB-5 investors (conventions §2); Q2 3M-2026 printed **+1,500**, kept as printed |
| דיבידנדים ששולמו לבעלי זכויות שאינן מקנות שליטה | 12 | |
| קבלת / פרעון הלוואות ממוסדות פיננסיים ואחרים | 4 / 7 | |
| תקבולים מהנפקת אגרות חוב בניכוי הוצאות הנפקה | 3 | |
| פרעון אגרות חוב | 8 | |
| **קבלת / פרעון הלוואות מבעל שליטה** | 5 | no term; current liability in the balance sheet; repaid April–May 2026 (note 7ח) – M1 |
| **קבלת הלוואות מ- Extell Holdings I LLC** (Q2) | 4 | note 7ט: 12% interest, due 2.7.2033 – M1 |
| **מקדמות (החזר מקדמות) מ-Extell Holdings I LLC** | 5 | net advances from a controlling-holder entity, no term (conventions §5) |
| **תשלומים למשקיעי EB-5** | 7 | conventions §3; note `הלוואות EB-5` |
| נגזרים פיננסיים | אחר | conventions §7 |
| ריבית ועלויות הלוואה ששולמו / תשלומי ריבית ועלויות הלוואה | 13 | in financing; includes loan costs, noted |

**(*) lines:** none outside financing. Operating and investing show only receipts (dividends received, interest received).

**Overrides**
- Q1 `line_text` for line 10: `מ-Extell` without a space, as printed (sub-agent finding; confirmed on a displayed 400-DPI crop).
- header_text, line_items, notes.

**Checks:** all OK (C2 also OK per item).

**Validate:** PASS 339 / FAIL 0.

### 2481 — אלמוג (כ.ד.א.י.) בע"מ

**Sources, columns, units**
- Q1: `2481_..._Q1_1744517.pdf` (53 pp), pp.35–36, fin p.36.
- Q2: `2481_..._Q2_1766407.pdf` (59 pp), pp.40–41, fin p.41.
- Units: אלפי ש"ח.

**Mapping** (11 lines)

| line | item | reason |
|---|---|---|
| קבלת (פירעון/פרעון) הלוואות ואשראי מתאגידים בנקאיים לזמן קצר, נטו | 5 | |
| קבלת (פירעון) הלוואות מאחרים לזמן קצר | 5 | |
| קבלת הלוואת (Q1, as printed) / הלוואות לזמן ארוך מתאגידים בנקאיים ואחרים | 4 | |
| פירעון הלוואה מתאגידים בנקאיים לזמן ארוך | 7 | |
| הנפקת אגרות חוב, נטו | 3 | |
| קבלת הלוואות מבעל עניין לזמן קצר | 5 | the line states short term |
| פירעון הלוואות מבעלי/מבעל עניין | 7 | no term on the line, but the separate company data (Q1 p.51) shows `פירעון הלוואות מצדדים קשורים לזמן ארוך` ((76,529) = (73,255) + (3,274)); Harel loans are long-term after reclassification – M1 |
| פירעון הלוואות מצדדים קשורים | 7 | |
| פירעון התחייבויות בגין חכירה | 10 | |
| השקעות בעלי זכויות שאינן מקנות שליטה | 6 | |
| ריבית ששולמה | 13 | |

**Restatement**
- Note 2 (retrospective application of a staff position on combination deals) restates the comparatives of the balance sheet, P&L and equity statements, which are marked `הוצג מחדש`.
- The cash-flow columns are **not** marked, so no column is flagged; a column note says so (conventions §10).
- For Q1-2025, the Q2 report puts (10,000) under `מבעל עניין` and (808) under `מצדדים קשורים`, while Q1 shows `-` and (10,808). Both lines are item 7, so C2 is unaffected (column note).

**(*) lines:** none outside financing. Interest paid is in financing; investing shows only `ריבית שהתקבלה`.

**Checks:** all OK.

**Validate:** PASS 332 / FAIL 0.

### 2483 — קבוצת גבאי-בניה,יזום,ניהול ואחזקות נדל"ן בע"מ

**Sources, columns, units**
- Q1: `2483_..._Q1_1745002.pdf` (79 pp), pp.60–61, fin p.60.
- Q2: `2483_..._Q2_1764242.pdf` (87 pp), pp.65–67, fin p.65.
- Units: `(באלפי ש"ח)` in the title.
- Q1 column c1 had months and end date inferred by the extractor; confirmed on the image as 3M to 31.03.2026.
- The FY-2025 column has no audit label (`ל ש נ ה שהסתיימה ביום 31 בדצמבר 2025`). Years are letter-spaced in the PDF.

**Mapping** (10 lines)

| line | item | reason |
|---|---|---|
| הנפקת אגרות חוב (לאחר ניכוי הוצאות הנפקה) | 3 | Q1 c1 printed (3,271) = issue costs paid in the quarter, netted in 3 |
| ריבית ששולמה | 13 | |
| פירעון אגרות חוב | 8 | |
| **רכישת מניות חברה מאוחדת מבעל השליטה בחברה** | **14** | purchase of more shares in the already-controlled subsidiary גבאי מניבים from the controlling holder; the non-cash appendix shows `...רכישת מניות של בעל השליטה בגבאי במניבים`; not treasury shares – M7 |
| הנפקת הון (ראה ביאור 3ד') | 1 | |
| פירעון הלוואות מבעלי שליטה, נטו | 5 | net, no term – conventions §5 |
| קבלת / פירעון הלוואות לזמן ארוך מתאגידים בנקאיים ומאחרים | 4 / 7 | |
| חלוקת דיבידנד לבעלי זכויות שאינן מקנות שליטה | 12 | |
| עליה (ירידה) באשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו | 5 | |

**Source issue (C1)**
- Q2, 3M Apr–Jun 2026 column: the printed lines sum to (67,724), but the printed total is (67,729), a difference of 5.
- Every value was read at 300 DPI by the sub-agent and confirmed by me on a displayed composite.
- The difference sits in the short-term credit line, printed (18,489). By Q2 6M (49,305) minus Q1 3M (30,811) it should be (18,494); with (18,494) the column would sum to (67,729).
- The printed values are kept (conventions §9), with an `issues` entry, a column note and a C1 explanation.

**C2 explanations**
- C2 3M-2025 total −1 is rounding.
- C2-item 5, 3M-2026 (+5) is the same source issue.
- C2-item 5, 3M-2025 (−1): Q2 moves (2,638) into `פירעון הלוואות מבעלי שליטה, נטו`; that line is item 5 too, so this is presentation plus rounding.
- All in `2483_checks.json`.

**(*) lines:** none outside financing. `חלוקת דיבידנד כנגד הלוואה לצד קשור` is non-cash and was excluded.

**Validate:** PASS 330 / **FAIL 1**. The single failure is `AC6 C1 דוח Q2 2026 | 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני)`, the documented source inconsistency (SCRIPT-ISSUE 1). The explanation-aware check `AC6/AC8 C1–C3` passes with unexplained mismatches = 0.

### 2488 — קבוצת אופק (פ.ה.א.) השקעות בע"מ

**Sources, columns, units**
- Q1: `2488_..._Q1_1745649.pdf` (49 pp), pp.35–36, fin p.36. Broken `נ` font, so "usable (repaired)"; every label was compared with the image.
- Q2: `2488_..._Q2_1766252.pdf` (99 pp), pp.80–82, fin p.81.
- Units: אלפי ש"ח.

**Mapping** (7 lines)

| line | item | reason |
|---|---|---|
| קבלת אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו | 5 | |
| תמורה מהנפקת אגרות חוב (בניכוי הוצאות הנפקה) | 3 | |
| קבלת / פרעון הלוואות מתאגידים בנקאיים ואחרים | 4 / 7 | no term stated, but short-term credit is on its own line, so these are long-term loans – M1 |
| קבלת (החזר) הלוואות מצדדים קשורים, נטו | 5 | net, no term |
| פרעון התחייבויות בגין חכירה | 10 | |
| ריבית ששולמה | 13 | |

**(*) lines:** none outside financing.

**C2:** 3M-2025 total: Q1 11,677 vs Q2 18,641 − 6,962 = 11,679 (−2). Breakdown:
- related-party loans 2,989 vs 3,020 (+31);
- interest (695) vs (725) (−30);
- short-term credit 9,842 vs 9,843 (+1).

This is a reclassification between the two reports plus rounding; explained in `2488_checks.json`.

**Source notes:** the sub-agent found that the company also revised its 2025 comparatives outside financing without a restatement mark. The Apr–Jun 2025 opening cash is 1,590, against 1,701 closing at 31.03.2025 in the Q1 report. The p.82 appendix `חברות קשורות` shows (2,668) vs (2,688). Both are outside our scope.

**Validate:** PASS 325 / FAIL 0.

### 2524 — אי.אס.איי אחזקות בע"מ

**Sources, columns, units**
- Q1: `2524_..._Q1_1744218.pdf` (50 pp). The whole statement is on p.29.
- Q2: `2524_..._Q2_1765965.pdf` (111 pp). The whole statement is on p.31.
- The pp.10–11 tables are the board report's liquidity analysis and were not used.
- Units: אלפי ש"ח (per column).
- The Q1 FY header year was not read by the text layer (the extractor assumed 2025); confirmed on the image as 2025, `מבוקר`.

**Mapping** (8 lines)

| line | item | reason |
|---|---|---|
| הנפקת אגרות חוב | 3 | |
| אשראי מתאגידים בנקאיים, נטו | 5 | |
| **שינוי בבעלי עניין** | **אחר** | the balance sheet shows `בעלי עניין` only among **assets** (current 2,807, non-current 2,001), so these are balances the company lends or owes from interested parties, not borrowing; none of items 1–14 fits – M8 |
| שינוי בהלוואה מאחרים | 5 | net, no term |
| פירעון התחייבות בגין חכירה | 10 | |
| ריבית ששולמה | 13 | |
| השקעות מהזשמ"ש | 6 | |
| דיבידנד ששולם | 11 | |

**(*) lines:** none outside financing. Operating shows only `קבלת דיבידנד וחלוקות…` (dividends received). `דיבידנד שחולק לזכויות שאינן מקנות שליטה שלא במזומן` is non-cash and was excluded.

**C2:** 3M-2026 total +1 is rounding in item 5 (81,274 vs 103,458 − 22,185 = 81,273). Explained in `2524_checks.json`.

**Validate:** PASS 324 / FAIL 0.

---------------------------------------------------------------------------------------------------------------

## Mapping decisions (cross-company judgement calls for Phase C to align)

- **M1 – Borrowing lines from others, related parties or controlling holders with no term on the line.**
  - Gross receipt/repayment lines are classified by the balance sheet and the notes:
    - current, with no long-term terms → 5 (111 `מאחרים`; 1622 `מבעל שליטה`);
    - long-term by note or terms → 4 / 7 (111 `מצד קשור`, a 78-month loan prepaid; 1622 Extell Holdings I LLC loan due 2033; 2481 interested-party repayments, long-term in the separate data);
    - 2488 `מתאגידים בנקאיים ואחרים` with short-term credit shown separately → 4 / 7.
  - Lines presented net with no term → 5 (R3).
- **M2 – Project-finance (ליווי) loans presented net with no term → 5** (1553). The balance sheet shows them as current liabilities.
- **M3 – `הנפקת מניות` that is wholly option/warrant exercises (per the statement of changes in equity) → 2** (539). The `הנפקת חבילה` of shares plus warrants → 1 (conventions §6).
- **M4 – NCI capital returns `החזר הון לבעלי זכויות שאינן מקנות שליטה` → 12** (1622, conventions §2).
- **M5 – EB-5 payments → 7; advances (net) from an entity of the controlling holder → 5** (1622, conventions §3 and §5).
- **M6 – `ריבית ועלויות הלוואה ששולמו` (interest plus loan costs, not split) → 13 with a note** (1622).
- **M7 – Purchase of shares of a consolidated subsidiary from the controlling shareholder → 14, not 9** (2483).
- **M8 – `שינוי בבעלי עניין` when interested-party balances are assets → אחר** (2524). Please align if another batch has this line.
- **M9 – (*) interest capitalised to inventory, disclosed below the statement and printed positive, combined with an operating `ריבית ששולמה` line in the same info row → recorded negative** so the info row is the total interest paid outside financing (1083 Q1/Q2). This is the same treatment batch 2 gave the parent company **121** קרדן ישראל.
  - Conventions §1 says appendix amounts keep the sign "as printed". That rule covers amounts disclosed *only* in an appendix; here the amount is added to an operating line printed negative.
  - Keeping +2,709 would give a meaningless info-row total (Q1-2026: −2,478 + 2,709 = +231 instead of −5,187).
  - **Phase C please confirm** (alternatives: keep the printed sign and list only the operating line in the info row, or keep it as is).
- **M10 – `restated` flag from a column footnote `* סיווג לא מהותי במספרי השוואה`** (111 Q2 6M-2025): flagged per conventions §10 (a note attached to the column says it is reclassified), with a column note.
  - Conversely, 2481's note-2 restatement does not mark the cash-flow columns, so they are not flagged (column note only).
  - Phase C may want one rule for "immaterial reclassification" footnotes.
- **M11 – Empty financing section** (1502 Q1): the heading line with dashes is the reported total (0), with no item lines and a report note.
- **M12 – Column `header_text`.** The auto header text was polluted (see SCRIPT-ISSUE 2). For all 21 reports I set a clean verbatim `columns.cN.header_text`: period wording, day and month, year, and audit status as printed, without units. Batches that keep the auto text will show inconsistent `כותרת העמודה בדוח (מילולית)` rows.

## SCRIPT-ISSUEs

```
SCRIPT-ISSUE 1
  script:     validate.py (line 90, company_checks: ok(abs(sum(items)+other-total) < 1e-6, "AC6 C1 ..."))
  report:     2483 Q2 (column 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני))
  symptom:    validate.py --issuers 2483 --no-master → PASS 330 / FAIL 1:
              "FAIL: [2483] AC6 C1 דוח Q2 2026 | 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני)". The per-column AC6
              check ignores the C1 explanations. The explanation-aware summary check (line 252) passes:
              unexplained mismatches = 0. Evidence: %TEMP%\fcf_run\_runs\validate_20261110-112706_8028\validate.txt
  expected:   a non-zero C1 that has an explanation key C1|<iss>|<report>|<period>|total should pass (goal AC6:
              "a non-zero value is allowed only when the source statement itself does not add up, and then it is
              documented"; conventions §9: keep printed values and explain C1).
  workaround: none legitimate. Changing the printed (18,489) or adding a plug would break R3/R4 and conventions §9.
              Documented with an issues entry, a column note and a C1 explanation.
              Other batches will hit the same: 719 Q1, 2533 FY, 531 Q2, ±1 rounding in 715 / 2417 / 2478.
  severity:   blocks "FAIL 0" for 2483 only; the deliverable itself is complete, verified and built.

SCRIPT-ISSUE 2
  script:     fcf_extract.py column-header parsing → data columns[].header_text → build_company.py row 'כותרת העמודה בדוח (מילולית)'
  report:     most reports. Examples: 2481 Q1 'לשלושה חודשים שהסתיימו 1 ביום 31 במרס, 2026 2 3 בלתי מבוקר 4 אלפי ש"ח'
              (row numbers of the page grid); 2483 Q1 'שלה המזומנים (באלפי ש"ח) חודשים שהסתיימו ...' (title words);
              'ל-3 החודשים שהסתיימו 2026' (day and month missing when the date phrase spans two columns);
              letter-spaced years '2 0 2 6'; units mixed in.
  expected:   the verbatim column header (period wording + date + year + audit status).
  workaround: columns.cN.header_text set by hand for all 21 batch-4 reports, compared with the images.
  severity:   cosmetic, but visible to the user in every company workbook.

SCRIPT-ISSUE 3
  script:     finalize_report.py auto_geometry (header box from text extents only)
  report:     539 Q1/Q2 (pp.55, 56, 58, 59)
  symptom:    the blue header box and the zoom header strip start right of and below the company logo (a vector
              drawing at x 57.3–160, y 31–53.5; auto box x0 61.3, y0 38.7 on Q1), so the logo is cut.
  workaround: boxes.<p>.header = [51.0, 24.0/24.4, 542.7/542.8, y1] in the overrides; verified on a displayed final page.
  severity:   cosmetic.

SCRIPT-ISSUE 4
  script:     fcf_render.py captions
  symptom:    (a) context pages without (*) lines still say "שורות ה-(*) שבעמוד זה מוצגות בהגדלה בתמונה ייעודית"
              (111 p.17); (b) the p.4 caption mentions notes in the (*) rows when those notes are empty (2481);
              (c) context-page captions say "(פעילויות שלא במזומן)" for pages that also hold appendix A
              (2483 p.61/p.66). Reported by the verification sub-agents.
  workaround: none needed; the content is correct.
  severity:   cosmetic.
```

**Process issue (not a script):** the `view` tool silently stops displaying images after about 50 per context window (see above).
- Workaround: composite PNGs (`%TEMP%\fcf_run\111\b4tools\compose.py`, PIL), confirming every image actually displayed, and read-only sub-agents with fresh contexts.
- Recommend Phase C and the Inspector check every `verified.method` claim against this.

## Overrides and files written by this batch

- `work\overrides\{111_Q2, 400_Q1, 400_Q2, 539_Q1, 539_Q2, 1083_Q1, 1083_Q2, 1502_Q1, 1502_Q2, 1553_Q1, 1553_Q2, 1622_Q1, 1622_Q2, 2481_Q1, 2481_Q2, 2483_Q1, 2483_Q2, 2488_Q1, 2488_Q2, 2524_Q1, 2524_Q2}.json`
  - Each contains: columns.header_text (plus months/end where the extractor inferred them; plus restated for 111), line_items, line_text, line_notes, outside_add, info_notes, boxes, report_notes, column_notes, issues, text_layer, verified.
- `work\overrides\{539, 2483, 2488, 2524}_checks.json`.
- `work\data\<iss>_<Q>.json`, written only by `finalize_report.py`.
- Company outputs: the two files in each of the 11 company folders, written only by `build_company.py` (final build 11:31).
- Batch files: `work\batches\batch-4.md` (this report) and `work\batches\batch-4-progress.md`.
- Temp: `%TEMP%\fcf_run\<iss>\` for the 11 issuers was deleted at the end. The `_runs` folders are left for Phase C.

## Final status

| issuer | status |
|---|---|
| 111 | verified + built (Q2; Q1 missing) |
| 400 | verified + built |
| 539 | verified + built |
| 1083 | verified + built |
| 1502 | verified + built |
| 1553 | verified + built |
| 1622 | verified + built |
| 2481 | verified + built |
| 2483 | verified + built; validate FAIL 1 = SCRIPT-ISSUE 1 (documented source inconsistency; not a data error) |
| 2488 | verified + built |
| 2524 | verified + built |

Assisted-by: Anthropic:Claude Opus 5.5
