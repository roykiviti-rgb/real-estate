# Inspection 1, batch 2 (iteration 1): findings

Companies: 121 · 155 · 715 · 1331 (Q2 only) · 1644 · 1722 · 2392 · 2418 · 2474 · 2521 · 2557 (Q2 only). That is 20 reports and 80 period columns.

References: `goal.md`, `goal-amendment-1.md` (T1, T2), `goal-amendment-2.md` (T3 cancelled), `work/phaseB-conventions.md`. I read the batch report only after I had formed my own findings.

## Verdict: **FAIL**

All 80 columns are numerically correct. I confirmed every financing value, total and (\*) value on images that I viewed myself. The batch fails on one rule violation that the source itself proves: the (\*) section note of 2418 (issue I1). There are also two cosmetic issues (I2, I3) and four observations (O1–O4).

---------------------------------------------------------------------------------------------------------------

## 1. What I did and saw

1. **Source location (text layer, PyMuPDF).** I scanned every page of all 22 source PDFs in the 11 folders for cash-flow statement titles and financing headings.
   - For every report I identified the consolidated statement independently and separated it from the following, which were not used:
     - separate / 38D data (121 p66/71, 155 p145/153, 715 p62/68, 1644 p61/70, 1722 p84, 2418 p64–65/70–71, 2474 p43/49, 2557 p91);
     - investee statements (155 p27–31: "368 THIRD Owners LLC" and "427 E 90 Owner LLC"; 1722 p98–110: P West, Fazenda and Pallani; 2418 p76–77/83–84: "רם אדרת-סלעית גני איילון");
     - board-report analyses.
   - I then dumped every word, with its coordinates, of every cash-flow page of the 20 reports.
2. **Images I viewed myself.** I viewed 16 images, and every one displayed.
   - Images 1–13 are composites at 150 DPI from the source PDFs. Each holds, for each report, the title, the column headers and units strip, and the whole financing section from heading to total. It also holds every (\*) line outside financing with its page's header strip: 121 p46/p48/p50/p52, 1331 p32 and 2418 p47/p51.
     - The composites were `121_Q1`, `121_Q2`, `155`, `715`, `1331`, `1644`, `1722`, `2392`, `2418_Q1`, `2418_Q2`, `2474`, `2521` and `2557`.
     - Every line text, every value in every column, the column headers and the units were compared one by one with the `מיפוי שורות` and `פירוט מימון` sheets.
   - Image 14: zoom page 3 of the 2418 screenshots PDF.
   - Image 15: (\*) crop page 5 of the 121 screenshots PDF.
   - Image 16: crops of the 2418 interest-classification sentence, from Q1 p51 and Q2 p52 (evidence for I1).
3. **Screenshots PDFs (82 pages).**
   - Captions and the table of contents were read from the text layer. Every caption names the correct file and PDF page.
   - The embedded image sizes were checked. Full pages are 1241×1754, i.e. 150 DPI. Context pages are 120 DPI.
   - I measured the line pitch of 4 of the 20 zoom images (2418, 121, 1722 and 155): 217–228 DPI, so ≥ 200. All zooms are rendered through the same path at 220 DPI and embedded as PNG without resizing.
   - All 82 rendered pages (120 DPI) were viewed by two read-only sub-agents with a checklist. They viewed 40 and 42 images, all displayed, and transcribed every total and every (\*) value; all match. I spot-checked two of their pages myself (images 14 and 15), and their findings agree with mine.
4. **Automated checks (my scripts, read-only).** All pass:
   - company workbooks against the master `נתונים` and `מיפוי שורות` sheets, keyed by issuer, report and period;
   - item labels and order, column labels, T2 suffix, restated flag;
   - numeric cells with format `#,##0`, live check formulas, RTL on every sheet;
   - T1;
   - C1, C2 (total and per item) and C3 (total and per item).
5. **Source integrity.** The SHA-256 of all 22 source PDFs of these companies equals `baseline_files_sha256.csv`.
6. **Hygiene.** No stray files, `~$*` lock files or `__pycache__`.
7. **Quality gate.** `validate.py --issuers <the 11> --no-master` gives PASS 3263, FAIL 0, INFO 4; the 4 INFO lines are the explained 715 C1 differences.
   - With the master checks enabled and an issuer subset, `validate.py` reports false AC11/T1 failures, because it compares master rows by position (see O4). The master rows themselves are correct; see §4.

---------------------------------------------------------------------------------------------------------------

## 2. Results per company and report

Legend: ✔ = PASS; ✖ = FAIL; (m) = minor or cosmetic remark. "Values" covers every line × column, the reported total, the check row and the (\*) values. Each check was confirmed on an image.

| Company / report | Source (file, consolidated, pages) | Periods | Values | Mapping | (\*) | Layout | Screenshots |
|---|---|---|---|---|---|---|---|
| 121 Q1 `_1744790` | ✔ cash flows p46–48, financing p47 | ✔ 3 | ✔ 10 lines + total | ✔ (734 → 6, documented) | ✔ (O1) | ✔ | ✔ |
| 121 Q2 `_1766447` | ✔ p50–52, financing p51 | ✔ 5 | ✔ | ✔ | ✔ (O1) | ✔ | ✔ |
| 155 Q1 `_1742331` | ✔ p125–126, financing p126 | ✔ 3 | ✔ 8 + total | ✔ (62,559 → 14, documented) | ✔ none | ✔ | ✔ |
| 155 Q2 `_1764162` | ✔ p129–130, financing p130 | ✔ 5 | ✔ | ✔ | ✔ none | ✔ | ✔ |
| 715 Q1 `_1744611` | ✔ p46–47, financing p47 | ✔ 3 | ✔ (C1 −1 is source rounding, documented) | ✔ (O2) | ✔ none | ✔ | ✔ |
| 715 Q2 `_1765211` | ✔ p50–51, financing p51 | ✔ 5 | ✔ (C1 ±1 in 3 columns, documented) | ✔ (O2) | ✔ none | ✔ | ✔ |
| 1331 Q2 `_1766504` (`-01` = appraisal) | ✔ p30–32, financing p30 | ✔ 3 (no 3-month columns) | ✔ | ✔ | ✔ appendix ד, +as printed | ✔ (Q1 missing stated) | ✔ |
| 1644 Q1 `_1741690` | ✔ p47–48, financing p48 | ✔ 3 | ✔ | ✔ | ✔ none | ✔ | ✔ |
| 1644 Q2 `_1763699` | ✔ p52–53, financing p53 | ✔ 5 (restated: column notes, §10) | ✔ (blank cell → 0, noted) | ✔ | ✔ none | ✔ | ✔ |
| 1722 Q1 `_1745698` (EUR) | ✔ p66 (single page) | ✔ 3 | ✔ (blank cells → 0, noted) | ✔ | ✔ none | ✔ | ✔ |
| 1722 Q2 `_1767756` (EUR) | ✔ p65 (single page) | ✔ 5 | ✔ | ✔ | ✔ none | ✔ | ✔ |
| 2392 Q1 `_1742520` | ✔ p49–50, financing p49 | ✔ 3 | ✔ | ✔ | ✔ none | ✔ | ✔ (m) I2 |
| 2392 Q2 `_1763248` | ✔ p50–51, financing p50 | ✔ 5 | ✔ | ✔ | ✔ none | ✔ | ✔ (m) I2 |
| 2418 Q1 `_1744896` | ✔ p45–47, financing p46 | ✔ 3 | ✔ (FY column shift realigned, documented) | ✔ | **✖ I1** | ✔ (m) I3 | ✔ (caption inherits I1) |
| 2418 Q2 `_1766843` | ✔ p49–51, financing p50 | ✔ 5 | ✔ | ✔ (O3) | **✖ I1** | ✔ | ✔ (caption inherits I1) |
| 2474 Q1 `_1745084` | ✔ p31–32, financing p32 | ✔ 3 | ✔ | ✔ (rule A → 5) | ✔ none | ✔ | ✔ |
| 2474 Q2 `_1764180` | ✔ p37–38, financing p38 | ✔ 5 | ✔ | ✔ | ✔ none | ✔ (m) I3 | ✔ |
| 2521 Q1 `_1745082` | ✔ p34–35, financing p35 | ✔ 3 | ✔ | ✔ | ✔ none | ✔ | ✔ |
| 2521 Q2 `_1764973` | ✔ p37–38, financing p38 | ✔ 5 | ✔ | ✔ | ✔ none | ✔ | ✔ |
| 2557 Q2 `_1765408` (`-01` = appraisal) | ✔ p52–54, financing p53 | ✔ 5 | ✔ | ✔ | ✔ none | ✔ (Q1 missing stated) | ✔ |

### Values confirmed on images: totals per column (all lines were checked the same way)

- **121**
  - Q1: 47,796 | 158,465 | 418,346.
  - Q2: 28,359 | 155,578 | (19,437) | (2,887) | 418,346.
  - (\*) Q1: operating (10,512) | (6,464) | (41,447), plus appendix ב 2,709 | 3,798 | 23,751, which is printed without parentheses.
  - (\*) Q2: operating (36,292) | (20,488) | (25,780) | (14,024) | (41,447), plus appendix 9,476 | 11,686 | 6,767 | 7,888 | 23,751.
- **155**
  - Q1: 292,219 | (80,750) | (294,589).
  - Q2: 92,825 | (175,657) | (199,394) | (94,907) | (294,589).
- **715**
  - Q1: 829,387 | (144,405) | 549,279.
  - Q2: 826,840 | 5,657 | (2,547) | 150,062 | 549,279.
  - The printed line digits really do not add up to the printed totals:
    - 3M-2025: (147,602) + 39,006 + (35,810) = (144,406), against a printed (144,405).
    - 6M-26: 826,841, against 826,840.
    - 6M-25: 5,656, against 5,657.
    - 3M-26: (2,546), against (2,547).
- **1331**: 25,500 | (34,653) | (74,821). (\*) appendix ד 'ריבית': 5,006 | 5,468 | 21,749.
- **1644**
  - Q1: 83,352 | 101,822 | 49,593.
  - Q2: 123,780 | 154,295 | 40,428 | 52,473 | 49,593.
- **1722**
  - Q1: 3,848 | 27,368 | 56,188.
  - Q2: 53,453 | 25,142 | 49,605 | (2,226) | 56,188.
- **2392**
  - Q1: (18,796) | 2,136 | 107,527.
  - Q2: (41,131) | (2,714) | (22,335) | (4,850) | 107,527.
- **2418**
  - Q1: 148,648 | 31,825 | 70,825.
  - Q2: 134,008 | 91,845 | (14,640) | 60,020 | 70,825.
  - (\*) appendix B: Q1 10,277 | 12,484 | 65,057; Q2 30,104 | 33,279 | 19,827 | 20,795 | 65,057.
  - In the Q1 FY column, from the second line on, each value is printed one row below its label because an unlabelled bond-repayment value was inserted: 7 values against 6 labels, with a lone '-' under the rule. The builder's realignment matches the Q2 FY column line by line: 111,258; (85,000) bond repayment; 54,100; −; (1,625); (7,908); −.
- **2474**
  - Q1: (4,260) | 5,648 | 52,172.
  - Q2: (13,808) | 101,303 | (9,548) | 95,656 | 52,172.
- **2521**
  - Q1: 14,920 | 11,746 | (80,606).
  - Q2: 3,088 | (66,174) | (11,833) | (77,920) | (80,606).
- **2557**: 1,047,103 | (97,297) | 1,050,683 | 8,717 | 328,871.

### Mapping review (R3 + conventions). Every line was judged; the noteworthy calls:

- **121 `תמורה ממימוש אופציות בחברה מאוחדת` → 6.** The exercise creates subsidiary shares held by NCI. The decision is documented and acceptable.
- **155 `מימוש אופציה` (62,559, FY-25) → 14.** The board report (Q2 p11) mentions the put-option liability on the shares of the subsidiary דרך עפר held by NCI. Documented.
- **715 combined line `פרעון התחייבויות לזמן ארוך לבנקים, אגרות חוב ואחרים` → 7** in every column; see O2.
- **715 `תמורה מהנפקת מניות`, which includes unsplit options → 1** (§6).
- **1722**
  - `הלוואות מתאגיד בנקאי, נטו` → 4 (rule B). The repayments are on a separate line.
  - `תקבולים בגין הלוואות לרוכשי דירות, נטו` → `אחר`. I verified that `הלוואות לרוכשי דירות` is an asset on the balance sheet (Q2 p60).
  - `החזר השקעה לזכויות שאינן מקנות שליטה` → 12.
- **2392 `הלוואות שהתקבלו מחברה האם ומבעל השליטה` → 5 (rule A).** I verified that on the Q1 balance sheet (p46) this item is a current liability only: – | 19,677 | –.
- **2392 `הלוואות שהתקבלו מתאגידי מימון חוץ בנקאיים, אחרים וצדדים קשורים` → 4, and its repayment line → 7.** The lenders' balances are mixed: current, plus a non-current `הלוואות מאחרים` of 13,586.
- **2474 bank-and-others lines → 5.** On the Q2 balance sheet (p33) `אשראי מתאגידים בנקאיים ואחרים` (93,649) is a current liability only. The related-party loan lines → 7, because those loans have both a current and a non-current part.
- **2557 related-party loans → 4/7.** `הלוואות לזמן ארוך מצדדים קשורים` is a non-current liability (p45). The unsplit `תשלומים בגין חכירה` → 10.
- **Cross-report consistency.** The same line gets the same item in Q1 and Q2 in every company, and C3 per item holds.

---------------------------------------------------------------------------------------------------------------

## 3. Issues

### I1: 2418, Q1 and Q2: the (\*) interest row names "section not stated", but the report states the section (must fix)

- **Rule.** R5 says the (\*) row must carry "a note naming the section". `phaseB-conventions.md` §1 says: when the report states the section where an appendix amount is included, use `גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת`. The same wording rule is restated in the master `הסבר` row "(\*) נוסח ההערה". This also bears on AC7.
- **What the source says.** I confirmed the sentence on image 16 and in the text layer: "כמו כן, החברה מסווגת ריבית ששולמה בדוח על תזרימי המזומנים כחלק מהפעילות השוטפת".
  - Q1 `2418_רם אדרת הנדסה אזרחית בע_מ_2026_Q1_1744896.pdf`: PDF p51 (ביאור 5 – סיכון נזילות, in the notes to the condensed consolidated statements) and p13 (board report).
  - Q2 `..._Q2_1766843.pdf`: PDF p52 (ביאור 1ג – סיכון נזילות) and p14.
- **What the deliverable says instead:**
  - `2418 - פירוט תזרים מימון 2026.xlsx`, sheet `פירוט מימון`, cell K37: "Q1 2026: גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)…" and the same for Q2.
  - Sheet `מיפוי שורות`, F14 (Q1 p47 `ריבית ששולמה`) and F27 (Q2 p51): "גילוי בנספח … – הסעיף לא צוין (לא בפעילות מימון)".
  - General notes B42 and B45: "ריבית ששולמה אינה מוצגת כשורה בדוח עצמו…". They do not mention the stated classification.
  - Master `נתונים`, column `(*) ריבית – סיווג / הערה`, all 8 rows of 2418. Master `מיפוי שורות`, the notes of the 8 (\*) rows of 2418.
  - Screenshots PDF `2418 - צילומי מסך…pdf`: the captions of pages 4 and 9 (the red crops) and pages 6 and 11 (context) carry the same "הסעיף לא צוין" wording.
- **Expected.** `גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת`, with the source of the statement quoted (Q1 p51/p13, Q2 p52/p14). The general notes should be adjusted to match, the company outputs and the master rows rebuilt, and the values left unchanged.
- **Scope.** I swept all 25 report files in the master whose (\*) note says "הסעיף לא צוין" for a "מסווגת ריבית … פעילות שוטפת/השקעה/מימון" sentence. Only 2418 Q1 and Q2 hit, so the defect does not appear to recur elsewhere. This sweep used the text layer only, as a hint for the other batches.

### I2: 2392, screenshots: the context pages are captioned "פעילות השקעה" but show only the non-cash appendix (minor)

- **Where:** `2392 - צילומי מסך תזרים מימון 2026.pdf`, pages 4 and 7, their captions ("עמוד נוסף של הדוח המאוחד על תזרימי המזומנים (פעילות השקעה)"), and the TOC and cover entries "דוח Q1 2026 – עמוד PDF 50 – פעילות השקעה" and "דוח Q2 2026 – עמוד PDF 51 – פעילות השקעה".
- **Source.** Q1 p50 and Q2 p51 contain only "נספח - פעילויות השקעה ומימון שאינן כרוכות בתזרימי מזומנים" plus a footnote. The investing section is on p49 (Q1) and p50 (Q2).
- **Expected.** The caption should name the non-cash appendix (R7.4: "what is shown").

### I3: the `מקורות` notes list pages that are not separate (38D) data as "נתונים כספיים נפרדים (תקנה 38ד)" (minor)

- **2418 Q1, `מקורות` I4:** "…38ד – עמ' 51, 63–65". p51 is ביאור 5 of the consolidated statements, the very page that holds the classification sentence of I1.
- **2474 Q2, `מקורות` I5:** "…38ד – עמ' 10, 48–49". p10 is section 8 of the board report (the Reg. 10(b)(14) disclosure).
- **Expected.** List only the 38D pages, or describe these pages correctly. This is cosmetic; the source choice is correct.

---------------------------------------------------------------------------------------------------------------

## 4. Cross-report checks and master rows

- **C1.** 0 in every column except 715. The 715 exceptions are 4 columns at ±1 from source rounding, which I confirmed on the image. They are documented in the notes row, in `חסרים והערות` (C1 rows 86–89, `בדיקה לא אפס` rows 175–176, `חריגה בדוח המקור` rows 38–39) and in `715_checks.json`.
- **C2 (recomputed from the workbooks).**
  - Totals:
    - 0 difference for 121, 155, 715, 1644, 1722, 2392 and 2418, in both years.
    - 2474, 3M-25: +1, explained in `חסרים והערות` R138 (rounding in interest paid).
    - 2521, 3M-26: −1, explained in R163.
  - Per-item differences, all listed and explained:
    - 2418, 3M-26, items 4/5: ±360. R133/R134; both reports confirmed on images (76,370 against 76,730).
    - 2474, 3M-25, item 13: R137.
    - 2521, 3M-26, items 4 and 13: R161/R162.
- **C3.** The FY-2025 total and all 15 items are identical in Q1 and Q2 for all 9 companies with both reports. The master `סיכום בדיקה C3` row says 0 mismatches. 1331 and 2557 have no Q1 report, so C2/C3 do not apply; `חסרים והערות` R5/R8 list them as missing reports and R15/R27 record the `-01` appraisal decisions.
- **Master `נתונים`.**
  - The 80 rows for my issuers equal the company workbooks in every compared field:
    - items 1–14, `אחר`, total and check;
    - both (\*) values;
    - months, end date, source file, pages and restated flag.
  - **T1 is correct:** the 9 Q1 FY-2025 rows are `לא`, and every other row is `כן`. Label and T2 suffixes are correct.
- **Master `מיפוי שורות`.** The 768 rows for my issuers equal the company `מיפוי שורות` sheets: text, value, item, page, source and note.
- **Master `אינדקס קבצים`.** The 22 rows for my issuers carry the correct roles: the `-01` files of 1331 and 2557 are appraisals, verified on their first pages, with 26 and 62 pages.

## 5. Observations (no action required unless the orchestrator decides otherwise)

- **O1: 121, sign of the (\*) appendix component.**
  - The appendix line `ריבית ששולמה והוונה למלאי` is printed without parentheses (2,709 | 3,798 | 23,751; 9,476 | 11,686 | 6,767 | 7,888 | 23,751). It is stored as negative in `מיפוי שורות` (row 18 for Q1 and row 35 for Q2, value columns G onwards) and summed as negative into the (\*) row: −13,221 | −10,262 | −65,198 and −45,768 | −32,174 | −32,547 | −21,912 | −65,198.
  - This departs from the literal "sign as printed" of R5, AC4 and conventions §1. However, it is documented in the row note, in the master note column and in the master `הסבר` row "(\*) סימן" (the Phase C rule for rows that combine a body line in parentheses with a positive appendix amount). I accept it as a documented decision; the orchestrator may want to confirm it.
- **O2: 715, combined repayment line → item 7.** The builder's own note says the 2026 amounts (13,405) are probably mostly bond principal, i.e. item 8 in substance. The single line keeps item 7 in every column and both reports, which is defensible because the line cannot be split. I accept it as a judgment call; it is documented.
- **O3: 2418 Q2 `קבלת הלוואה מזכויות שאינן מקנות שליטה` (266) → 4.** Rule A asks for balance-sheet evidence in the line note; the note cites R3 only. The amount is immaterial.
- **O4: the quality-gate script.** `validate.py --issuers <subset>` without `--no-master` compares master rows by position. It therefore reports false AC11 and T1 failures, e.g. "rows 648 == periods 80" and "T1 bad=[('121',12,…)]". The final inspector should run the full `validate.py` without `--issuers`.

## 6. What must be fixed (FAIL)

1. **2418 Q1 and Q2 (I1).**
   - Set the (\*) interest section to `גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת` for both reports, through the override (`outside_sections` / `info_note_extra`). Quote the statement: Q1 p51 ביאור 5 and p13; Q2 p52 ביאור 1ג and p14.
   - Update general notes B42 and B45.
   - Rebuild `2418 - פירוט תזרים מימון 2026.xlsx`, `2418 - צילומי מסך תזרים מימון 2026.pdf` (captions) and the master rows (`נתונים` and `מיפוי שורות`).
2. **Recommended in the same rebuild:**
   - I2: correct the 2392 captions and TOC entries for Q1 p50 and Q2 p51.
   - I3: correct the `מקורות` notes for 2418 Q1 (p51) and 2474 Q2 (p10).

Temp files: `%TEMP%\fcf_insp\2\`, deleted at the end of this inspection.
