# Inspection 1, batch 8: independent verification

Inspector: batch 8 of 8, iteration 1. Date: 2026-11-10.

Companies: 573, 584 (Q2 only), 719, 771, 1680, 2389, 2396, 2440, 2464, 2503, 2570 (Q2 only).
That is 11 companies, 20 reports and 80 period columns.

References:
- `goal.md`
- `goal-amendment-1.md` (T1 and T2 apply)
- `goal-amendment-2.md` (T3 is cancelled)
- `work/phaseB-conventions.md` and PIPELINE §7, including the Phase C rules A and B

I formed every finding below before I opened any builder or batch report. Afterwards I read only the batch-8 report, and
only to understand B1.

## Verdict: **FAIL**

- **Blocking issues:** 1 (B1).
  - The verbatim text of the 2396 Q1 total line is wrong: two words are swapped.
  - The batch-8 Builder introduced the error as a "correction" during its re-check.
- **Minor issues to fix:** 3 (M1–M3). They are note wording or a missing note only.
- **Observations, no fix required:** 3 (O1–O3).
- **Numbers:** every value, sign, column, period, unit and item assignment is correct.
  - I checked 20 reports, 80 columns and 785 line × period values.
  - Every C1/C2/C3 difference is documented.

---

## 1. How I verified (what I saw and how)

### 1.1 Source location
- **Own scan.** I scanned every PDF in the 11 folders myself with PyMuPDF; there are 22 source PDFs, excluding the 2 outputs per folder.
  - I listed every page that carries a cash-flow title or a financing section.
  - I then dumped the word layer, with coordinates, of every candidate page and the pages around it.
- **Consolidated statement and boundaries.** For each report I confirmed:
  - the consolidated statement title (`דוחות מאוחדים על תזרימי המזומנים`, `דוחות תמציתיים (ביניים) מאוחדים …`);
  - that the page before is the statement of changes in equity and the page after is note 1. So no page is missing.
- **Excluded statements.** My scan located and excluded the following:
  - separate (38D) data:
    - 573 Q1 p56;
    - 719 Q1 pp. 50–51 and Q2 pp. 132–133;
    - 1680 Q1 pp. 60–61 and Q2 pp. 73–74;
    - 2389 Q1 pp. 56–57;
    - 2440 Q1 p65 and Q2 p74;
    - 2503 Q1 pp. 78, 85;
    - 2570 Q2 p59;
    - 771 Q1 p76 and Q2 p80;
  - the board-report liquidity tables;
  - the investee statements:
    - 719 HADAR S.A.R.L, Q1 pp. 19–20 and Q2 pp. 103–104;
    - 584 מגדל סיפולוקס, p67;
    - 2396 דיורים בע"מ, Q1 p49 and Q2 p54;
  - 2503's NIS-translated copy of its statement, Q1 p64.
- **The `-01` files.** I read the first pages of each:
  - 771 Q2 `-01` (66 pp.): appraisal by S.K. (אס.קיי) שמאות of the "רוקסון דזרט" hotel.
  - 2464 Q1 `-01` (51 pp.): appraisal by עדי נאור of סמטת בית הבד 3, ת"א.
  - Neither contains a cash-flow statement, so both are correctly marked as not used.

### 1.2 Independent extraction (text layer)
- **Own tools.** I wrote my own parser (`compare.py`) and my own workbook reader (`wbparse.py`).
- **What the parser does:**
  - groups words into rows;
  - treats parentheses (both `(…)` and the reversed `)…(` forms) as negative and `-` as 0;
  - matches every workbook line, by normalised text, to the PDF row(s) on the cited page;
  - compares every value in column order;
  - lists every PDF row between the financing heading and the total that no workbook line uses.
- **Result:**
  - Every value of every line, total and (\*) line matched, except four rows where the text layer splits tokens. I confirmed those four on images (below):
    - 584 Q2 "הנפקת מניות": the 6M-2025 cell is blank;
    - 2396 Q2 "פירעון הלוואות מבעלי עניין ואחרים": `(34,625)`;
    - 2464 Q1 short-term credit: `14,939`;
    - 2396 Q1 total.
  - No financing row is unused, so no line is omitted or double-counted.
- **(\*) scan.** I listed every row containing ריבית / דיבידנד / חלוק(ות) on all statement pages, one page either side.
  - The only interest/dividend-paid lines outside financing are those the workbooks record: 573, 584, 719, 1680, 2389.
  - Everything else found is:
    - a receipt (`ריבית שהתקבלה`, `ריבית שנתקבלה`, `דיבידנד ותקבולים … מחברות המטופלות`);
    - non-cash (`דיבידנד שהוכרז וטרם שולם/חולק`, `ריבית לשלם`, `ריבית שנזקפה על הלוואות, נטו`);
    - an equity-statement row.

### 1.3 Visual confirmation
Every image below displayed; none returned the image-cap message, and I used 32 images in total. I rendered the
composites myself from the source PDFs at 130–300 DPI.

| Image | Content | What I checked on it |
|---|---|---|
| `comp_573_Q1`, `comp_573_Q2` | header strip, financing section, and the (\*) lines in appendix ג' (p39 / p41) | all lines, columns and units |
| `comp_584_Q2` | p30 header, financing, p32 header and appendix ג' interest | the blank 6M-2025 cell in "הנפקת מניות" |
| `comp_719_Q1`, `comp_719_Q2` | p38 / p119 financing, p37 / p118 operating interest | the 3M-2025 column, whose lines sum to 7,911 against a printed 7,903 |
| `pair_771`, `extra1` | both financing sections and both column-header strips | (none) |
| `comp_1680_Q1`, `comp_1680_Q2` | financing; appendix א' interest | (none) |
| `comp_2389_Q1`, `comp_2389_Q2` | financing; operating interest | (none) |
| `comp_2396_Q1`, `comp_2396_Q2`, `total2396` | financing; the total lines of both reports at 300 DPI | (none) |
| `pair_2440`, `pair_2464`, `pair_2503`, `comp_2570_Q2` | financing, headers and units | (none) |
| `zg_1`–`zg_4`, `zsg_573` | the 20 zoom images taken out of the screenshots PDFs | headers, units, financing lines and legibility |
| `sg_1`, `zsg_573` | the 9 red (\*) crops | (none) |
| contact sheets of all 11 screenshots PDFs, plus `fp_2396_2464` at 680 px | the screenshots pages | the boxes and the page structure |
| `p48_2503` | the top of 2503 Q1 p48 and p47 | the printed title of p48 (M3) |

I compared every number I read on these images with the workbook values. All of them match.

### 1.4 Workbooks, master and quality gate
- **Workbook consistency (all 11 workbooks).** My own script checked:
  - each item = Σ of its mapped lines, per column;
  - the total and the C1 value;
  - the (\*) rows equal the (\*) mapping lines;
  - labels against months, end date and T2;
  - restated flag against label;
  - column order;
  - the `מקורות` sheet against the folder: file list and page counts.
  - Result: 0 problems. The only non-zero C1 is 719 Q1 3M-2025 = +8, which is documented.
- **Master:**
  - **`נתונים`:** 80 rows for my issuers = 80 workbook columns. Every field equals the workbook:
    - identity, file, pages, label, months and end date;
    - currency, units and restated flag;
    - items 1–14, `אחר`, total and check;
    - both (\*) amounts and the screenshots path.
  - **T1:** recomputed independently; correct on all 80 rows (`לא` only on the Q1-report FY-2025 rows).
  - **`מיפוי שורות`:** 785 rows = 785 expected line × period rows, as a set-equal match.
  - **`אינדקס קבצים`:** the 22 rows match the folders and roles.
  - **`חסרים והערות`:** see §3.
- **Quality gate:** `validate.py` on the full workspace, with `--out` into my temp folder → `PASS 36751  FAIL 0  INFO 10`, exit 0.
  - A run restricted to `--issuers <mine>` but including the master shows AC11/T1 "failures".
  - These are an artefact of comparing the full 648-row master with a subset. They are not defects: the full run and my own master check are clean.

---

## 2. Per company and report

Pages are 1-based PDF pages. "Fin" is the page of the financing section.

Legend:
- **P** = PASS
- **F** = FAIL
- **m** = PASS with a minor note-wording fix
- **o** = PASS with an observation (no fix)

| Report | Source / pages | Periods (labels, months, end, T2, restated) | Values and verbatim text | Mapping | (\*) rows | Layout (header, notes, RTL, sources) | Screenshots |
|---|---|---|---|---|---|---|---|
| 573 Q1 | P – `…Q1_1744074.pdf` pp. 37–39, fin p37 | P – 3 cols; 2025 (\*) footnote handled as a column note | P – 13 lines + total | P | P – app. ג' p39: 11,994 / 13,100 / 72,738, positive as printed, "הסעיף לא צוין"; dividends app. = financing lines | P | P |
| 573 Q2 | P – `…Q2_1764868.pdf` pp. 39–41, fin p39 | P – 5 cols, T2 ✓ | P | P – 1,425 "רכישה עצמית … ע"י בעלי זשמ"ש" → 6, as Q1 (note 6ה) | P – p41: 37,379 / 37,442 / 25,385 / 24,342 / 72,738 | P | P |
| 584 Q2 | P – `…Q2_1767534.pdf` pp. 30–32, fin p30 | P – 3 cols (6M/6M/FY; no 3M columns printed) | P – 9 lines + total; blank 6M-2025 cell = 0 | P – rule A with balance-sheet evidence (receipts from others → 4, repayments → 5) | P – app. ג' p32: 2,386 / 5,194 / 10,375 (O3) | P – "דוח Q1 2026 אינו קיים בתיקייה" in C9 | P |
| 719 Q1 | P – `…Q1_1745275.pdf` pp. 37–39, fin p38 | P | P – C1 3M-2025 = +8 (source) | P – project-finance lines → 5 (balance sheet: current only) | P – p37 operating: (5,073) / (3,815) / (20,910) | P | P |
| 719 Q2 | P – `…Q2_1767607.pdf` pp. 118–120, fin p119 | P | P | P | P – p118: (10,175) / (11,190) / (5,102) / (7,375) / (20,909) | P | P |
| 771 Q1 | P – `…Q1_1744961.pdf` pp. 60–61, fin p60 | P – units in the title "(באלפי ש"ח)" | P | P – parent loan → 4 (note 3ב back-to-back LT) | P – interest only in financing | P | P |
| 771 Q2 | P – `…Q2_1763641.pdf` pp. 62–63; `-01` = appraisal | P | P | P | P | P | P |
| 1680 Q1 | P – `…Q1_1745093.pdf` pp. 31–33, fin p32 | P – (\*) "הצגה מחדש" footnote handled as a column note | P | P – contingent consideration (1,000) → אחר | P – app. א' p31 (inside operating): (1,537) / (1,362) / (9,730) | P | P |
| 1680 Q2 | P – `…Q2_1764623.pdf` pp. 36–38, fin p37 | P | P | P | P – p36: (6,100) / (4,274) / (4,563) / (2,912) / (9,730) | P – wrong running header documented | P |
| 2389 Q1 | P – `…Q1_1745138.pdf` pp. 38–41, fin p39 | P | P | P – bonds + warrants package → 3 (§6); NCI loans → 4/7 | P – p38 operating: (3,327) / (1,370) / (7,806) | P | P |
| 2389 Q2 | P – `…Q2_1766465.pdf` pp. 50–53, fin p51 | P | P | P | P – p50: (4,684) / (1,486) / (1,357) / (116) / (7,806) | **m** (M1) | P |
| 2396 Q1 | P – `…Q1_1744629.pdf` pp. 34–35, fin p35 | P – headers "ליום 31 במרס …" recorded verbatim and documented | **F (B1)** – all values correct; total-line text not verbatim | P | P | P | P |
| 2396 Q2 | P – `…Q2_1767492.pdf` pp. 36–37, fin p37 | P | P | P | P | P | P |
| 2440 Q1 | P – `…Q1_1745527.pdf` pp. 47–48, fin p48 | P | P | P | P | P | P |
| 2440 Q2 | P – `…Q2_1767784.pdf` pp. 51–53, fin p52 | P | P | P | P | P | P |
| 2464 Q1 | P – `…Q1_1746287.pdf` pp. 92–93, fin p93; `-01` = appraisal | P | P | P | P | P | **o** (O2) |
| 2464 Q2 | P – `…Q2_1767804.pdf` pp. 92–94, fin p93 | P – (573) in 3M-2025 Apr–Jun documented | P | **m** (M2) – capital-note line → 7, documented | P | P | P |
| 2503 Q1 | P – `…Q1_1743729.pdf` pp. 48–49, fin p49; CAD thousands | P | P | **m** (M2) – owners 1/11, NCI 6/14, loan to controlling owners → 11 | P | **m** (M3) | **o** (O2) |
| 2503 Q2 | P – `…Q2_1765098.pdf` pp. 51–52, fin p52 | P | P | **m** (M2) | P | P | **o** (O2) |
| 2570 Q2 | P – `…Q2_1767187.pdf` pp. 41–42, fin p41 | P | P | P – related-party loans → 5 (rule A: current only); others → 4/7 | P | P – missing-Q1 statement in C9 | P |

Screenshots, in general:
- **Structure:** for every report, the screenshots PDF has:
  - the highlighted full page of each fin page, at 150 DPI;
  - one zoom with the header strip, periods and units, at 220 DPI;
  - one red crop for each (\*) page, with that page's header strip and units;
  - context pages at 120 DPI for all other statement pages.
- **Pages:** these are exactly the pages cited in the workbook. My own TOC-versus-mapping check found 0 differences.
- **Captions:** every page's caption contains the report ID and the PDF page number.
- **Legibility:** all digits are legible.

---

## 3. Cross-report checks (C2 / C3), recomputed

| Company | C2 2026 / 2025 total | Item-level differences | C3 FY-2025 | Explained in `חסרים והערות` |
|---|---|---|---|---|
| 573 | 0 / 0 | none | equal | — |
| 719 | 0 / 0 | 2025: item 4 (−392), item 7 (+400) | equal; (\*) interest (20,910) vs (20,909), info row | r90 (C1 +8), r91–r92, r41, r177 ✓ |
| 771 | 0 / 0 | 2025: items 4/7 ±195 (netting in Q2) | equal | r93–r94 ✓ |
| 1680 | 0 / 0 | none | equal | — |
| 2389 | 0 / 0 | none | equal | — |
| 2396 | −1 / −1 (rounding) | 2026 item 7: (67) vs (66); 2025 item 7: (8,638) vs (8,637) | equal | r125–r128 ✓ |
| 2440 | 0 / 0 | none | equal | — |
| 2464 | 0 / 0 | none | equal | — |
| 2503 | **−1,793** / 0 | 2026 item 13 (3,231) vs (1,438); 2025 items 4/11 ±1 | equal | r157–r160 ✓ |
| 584, 2570 | N/A (no Q1 report) | — | — | r3, r10 (missing Q1) ✓ |

- **2503 claim verified.** I checked the 2503 explanation (r158) against the PDFs. "עלייה בספקים וזכאים ויתרות זכות":
  - Q1 3M-2026 = 11,454 (p48);
  - Q2: 21,137 − 11,476 = 9,661 (p51);
  - the difference is exactly 1,793. ✓

---

## 4. Issues

### B1 (blocking): the 2396 Q1 total-line text is not verbatim
- **Printed text.** PDF `2396_אשל הירדן יזום ובנין בע_מ_2026_Q1_1744629.pdf`, p35, total line at y≈581–593 prints:
  **`מזומנים נטו, שנבעו (ששימשו) מפעילות מימון`**
  - **Evidence:** seen at 300 DPI (`total2396.png`), at 170 DPI (`extra1.png`) and in the 2396 Q1 zoom of the screenshots PDF (p3).
  - The text layer agrees: `שנבעו`@x436 lies right of `ששימשו`@x393.
- **Workbook text.** The workbook and the master have **`מזומנים נטו, (ששימשו) שנבעו מפעילות מימון`**, with the words swapped. This wording is the Q2 report's (p37, "… (ששימשו) שנבעו לפעילות מימון"), not the Q1 report's.
- **Where it appears:**
  - `2396 - פירוט תזרים מימון 2026.xlsx`:
    - `מיפוי שורות`!C14;
    - the Q1 part of `פירוט מימון`!K35.
  - Master `מיפוי שורות`, rows 4362–4364.
- **Cause.** `work/overrides/2396_Q1.json` → `line_text` `"10": "מזומנים נטו, (ששימשו) שנבעו מפעילות מימון"`.
  - The batch-8 report lists this as a re-check "correction".
  - It turned a correct text into a wrong one.
- **Fix:**
  1. Set `line_text["10"]` to `מזומנים נטו, שנבעו (ששימשו) מפעילות מימון`, or drop the key; the auto text is correct.
  2. Run `finalize_report.py 2396 Q1`, then rebuild 2396 and the master.
  3. Values are unaffected.

### M1 (minor): the 2389 Q2 column notes are inaccurate
- **The note.** `2389 - פירוט תזרים מימון 2026.xlsx`, `פירוט מימון` notes row, columns "6 חודשים … 30.06.2025" and "3 חודשים … 30.06.2025 (אפריל–יוני)", says the (\*) marks have:
  > "ללא הערת שוליים בעמודי הדוח על תזרימי המזומנים"
- **What the statement prints.** p52, which is part of the cited statement pages 50–53, prints at y≈730:
  > "(\*) סווג מחדש, ראו ביאור 2ג'."
  - This footnote explains the (\*) marks on p50 (operating) and p52 (appendix ב').
- **Decision.** The decision itself (no `(מוצג מחדש)`: the headers are not marked and no financing value is marked) is consistent with §10 and with the other companies.
- **Fix:** correct the note wording only.

### M2 (minor): leftover process remarks in the final mapping notes
These notes read as if the decisions were still open:
- 2464 Q2, `מיפוי שורות`, line 5 ("פרעון הלוואות ושטר הון מצדדים קשורים"):
  > "החלטת מיפוי לתיאום בשלב C (חלופה: סעיף 11 לרכיב שטר ההון)"
- 2503 Q1 and Q2, line 4 ("הלוואות ללא מועד פרעון לבעלי השליטה"):
  > "(הצעת המחלץ – סעיף 7 – נדחתה). החלטת מיפוי לתיאום בשלב C (חלופה: 'אחר')"

Fix: replace each with the final reasoning. The current item choices (7, and 11) are defensible and documented.

The remarks "שונתה מסעיף 4/7 בשלב C" in 719 lines 6–7 and 2570 lines 4–5 are harmless audit trail.

### M3 (minor): an undocumented title defect on 2503 Q1 p48
- **The defect.** PDF `2503_לנטרה קנדה אנטרפרייזס לימיטד פרטנרשיפ_2026_Q1_1743729.pdf` p48 is the operating and investing page of the consolidated cash-flow statement.
  - Its content is "תזרימי מזומנים לפעילות שוטפת", starting with "הפסד נקי לתקופה (3,757) / (25) / (11,282)".
  - Yet its printed title is **"דוחות מאוחדים על השינויים בהון"**, copied from p47.
  - Evidence: seen on `p48_2503.png`, which shows the top of p48 and p47.
- **Impact.** Using p48 as a statement page is correct, and no value is affected.
- **The gap.** The 1680 Q2 running-header defect is recorded (master `חסרים והערות` r50 and workbook notes). This one is not recorded anywhere, so the user would wonder why a "changes in equity" page is cited.
- **Fix:** add an `issues` / `report_notes` entry for 2503 Q1, like the one for 1680 Q2.

### Observations (no fix required)
- **O1 – master (\*) notes.**
  - The master's `(*) … סיווג / הערה` columns are empty where nothing lies outside financing.
  - In those cases the company workbook's K-note reads "אין סכומים מחוץ לפעילות מימון (…)". This applies to the interest note of 771, 2396, 2440, 2464, 2503 and 2570, and to the dividend note of 573, 1680 and 2503.
  - This is consistent with R5 ("leave 0 with no note"); all amounts are equal.
- **O2 – unframed zooms.** Three zoom pages have no blue/orange frames or yellow fill:
  - 2464 Q1 (screenshots p3);
  - 2503 Q1 (p3);
  - 2503 Q2 (p6).

  In these three the header strip and the financing section are contiguous, so a single crop is rendered. The other 17 zooms are framed. R7.2 is met: the periods, units and every financing line are present and legible. This is a cosmetic inconsistency.
- **O3 – 584 (\*) amounts.**
  - The (\*) interest amounts (appendix ג', p32) may include the financing-section "תשלום ריבית" ((959) and (5,989) in the 2025 columns). The report does not say.
  - The workbook states this in the (\*) note and in the column notes D40 and E40. That is acceptable under conventions §1.

---

## 5. What must be fixed

1. **B1:** set the 2396 Q1 total-line text to the printed `מזומנים נטו, שנבעו (ששימשו) מפעילות מימון`. Then re-finalize, rebuild 2396 and rebuild the master.
2. **M1:** correct the wording of the two 2389 Q2 column notes; the p52 footnote "(\*) סווג מחדש, ראו ביאור 2ג'" exists.
3. **M2:** replace the "לתיאום בשלב C" / "הצעת המחלץ" remarks in 2464 Q2 line 5 and 2503 Q1/Q2 line 4 with final reasoning.
4. **M3:** document the wrong printed title on 2503 Q1 p48 ("דוחות מאוחדים על השינויים בהון" on a cash-flow page) as a source irregularity.

After the fixes, re-run `validate.py`.
