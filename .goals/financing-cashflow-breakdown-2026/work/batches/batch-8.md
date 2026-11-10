# Batch 8 report — Phase B (iteration 1)

Builder: Phase B batch 8 · 2026-11-10 · goal `financing-cashflow-breakdown-2026` (goal.md + amendments 1–2; T1/T2 apply, T3 cancelled).
Issuers: 573 · 584 · 719 · 771 · 1680 · 2389 · 2396 · 2440 · 2464 · 2503 · 2570 — **20 reports, all verified, 11 companies built (final)**.
Checkpoint: `batches/batch-8-progress.md`. No git. Only my own overrides / `_checks.json` / data (through the scripts) /
company outputs were written.

---------------------------------------------------------------------------------------------------------------

## 0. Image cap — what was seen, and the re-check (orchestrator alert, 11:15)

From 10:14 to about 11:02 **every** `view` of an image in this session returned "You've reached the maximum number of
images you can view (50)" and **no image**. I first treated those calls as views and marked 15 reports verified on that
basis; I noticed it at ~11:15 (before the orchestrator alert arrived) and redid the visual check:

* **Re-checked on real images (11:18–11:36):** 573 Q1, 573 Q2, 584 Q2, 719 Q1, 719 Q2, 771 Q1, 771 Q2, 1680 Q1, 1680 Q2,
  2389 Q1, 2389 Q2, 2396 Q1, 2396 Q2, 2440 Q1, 2440 Q2, and 2464 Q1 (operating page / (*) scan; its financing section had
  been seen at 11:06 on the screenshots zoom page).
  * Method: one **composite PNG per company** rendered directly from the source PDF (115–120 DPI) containing, for each
    report, the column-header strip with the units, the whole financing section, every (*) line with its page's header
    strip, and crops of **every** line on the statement pages containing ריבית / דיביד / ששולמ / שולם (text-layer scan).
    Each output was confirmed to display (an image block came back) before use.
  * Every line text, every digit, every header and unit was compared with the final data; then the screenshots PDFs of
    573, 584, 719, 771, 1680, 2389, 2396, 2440 were checked on two contact sheets (orange/blue/red boxes) and their
    captions read back from the PDF text.
* **Seen correctly the first time (after 11:03):** 2464 Q2, 2503 Q1, 2503 Q2, 2570 Q2.
* Every claim in my notes that had come from an unseen page (note texts, appendix titles, page roles) was re-checked on the
  text layer; the wrong ones were fixed (§1, "re-check corrections").
* All `verified.method` texts were rewritten to say exactly what was seen, on which image and when, and that the earlier
  views are not relied on.
* Result of the re-check: **no value, sign, column or item was wrong**. Only texts were corrected:
  * the 2396 Q1 total-line label;
  * the 2389 Q2 c2/c4 column notes;
  * the report notes of 2396 Q1/Q2, 2440 Q2 and 2464 Q1/Q2;
  * two captions (2440 Q2 p53, 2464 Q2 p94);
  * the wording of the 719 C1 explanation.

  All are listed under the companies below.

---------------------------------------------------------------------------------------------------------------

## 1. Per company

### 573 משולם לוינשטין הנדסה וקבלנות בע"מ
* **Sources:** Q1 `…_2026_Q1_1744074.pdf` pp. 37–39 (fin p37, header p37); Q2 `…_2026_Q2_1764868.pdf` pp. 39–41 (fin p39).
  pp. 15–16 (board report table) and 56–58 / 59–61 (separate data) not used.
* **Columns:** Q1 3M 31.03.2026, 3M 31.03.2025, FY 2025. Q2 6M 30.06.2026/2025, 3M Apr–Jun 2026/2025, FY 2025.
  **Units:** אלפי ש"ח.
* **Mapping (13 lines + total):**
  * option exercise → 2; bonds net → 3; commercial paper (נע"מ) → 3; share-issue costs (347) → 1;
  * NCI dividend → 12; parent dividend → 11;
  * LT bank loans → 4/7; loan from an equity-accounted investee → 4/7 (Q2 label says "לזמן ארוך"); ST bank credit net → 5;
  * **1,425 sale of 10.1% of MRPL to its CEO without loss of control → 6** (Q2 labels it "רכישה עצמית של מניות על ידי בעלי
    זכויות שאינן מקנות שליטה בחברה מאוחדת"; note 6ה confirms a sale, so item 6 in both reports).
* **(\*):** interest paid only in appendix C "מזומנים ששולמו במהלך התקופה עבור: ריבית" (p39 / p41).
  * Printed positive: 11,994 / 13,100 / 72,738 and 37,379 / 37,442 / 25,385 / 24,342 / 72,738.
  * Note per conventions §1: "גילוי בנספח … – הסעיף לא צוין (לא בפעילות מימון)".
  * The appendix C dividend rows equal the financing dividend lines, so the dividend (\*) row = 0.
* **Overrides:**
  * `line_text`: note numbers 6ג'/6ה' removed, and a fixed text for the 1,425 line.
  * all items set; notes.
  * `outside` replaced: bbox widened to include the heading.
  * `context_sections`: p38/p40 = appendix A (SCRIPT-ISSUE 2 workaround), p39/p41 = appendices B–C.
  * c2/c4 column notes: "(\*) התאמה לא מהותית" marks the operating values only, so not flagged restated.
* **Checks:** C1 0 everywhere; C2 OK (total and every item); C3 16 OK.
* **Validate:** PASS 338 / FAIL 0.

### 584 א.ליבנטל אחזקות בע"מ (Q2 only)
* **Source:** `…_2026_Q2_1767534.pdf` pp. 30–32 (fin p30).
  * p67 = statements of the investee מגדל סיפולוקס, not used.
  * Text layer "usable (repaired)" (broken נ); every label was compared with the image.
* **Columns:** 6M 30.06.2026, 6M 30.06.2025, FY 2025 (no 3M columns). **Units:** אלפי ש"ח.
* **Mapping:** the loan lines state no term, so they were decided by reconciling them with the balance sheet, the board
  report and notes 1/3יא (text layer):
  * "קבלת (פירעון) הלוואה מבעל שליטה" (net) → 5.
  * "קבלת הלוואות מאחרים" → 4 (2026 = LT loans from the investee מגדל סיפולוקס, balance 26,106 → 41,527).
  * "פירעון הלוואות מאחרים" → 5 (2026 = repayment of the short-term loan from נאוי גרופ; ST loans from others 31,842 → 10,016).
  * "קבלת הלוואות מתאגידים פיננסיים" → 5 (a 22M revolving short-term bank facility 28.5.2026–30.3.2027; "אשראי מתאגידים
    פיננסיים", current, 18,432 → 40,793).
  * Other lines: shares → 1 (the 6M-2025 cell is blank, so 0); bonds of the then-consolidated associate → 3; lease → 10;
    ST bank credit net → 5; "תשלום ריבית" (financing) → 13.
* **(\*):** appendix C "מזומנים ששולמו במשך התקופה עבור: ריבית ששולמה" 2,386 / 5,194 / 10,375 (positive as printed).
  The report does not say whether the 2025 appendix figures include the financing-section interest; this is in the c2/c3
  column notes.
* **Overrides:** items and notes; `outside` replaced (bbox includes the heading); `context_sections` p31 (appendix A,
  SCRIPT-ISSUE 2 workaround) and p32 (appendices B–C); report notes.
* **Checks:** C1 0 (Q1 report missing, so no C2/C3).
* **Validate:** PASS 140 / FAIL 0.

### 719 א.לוי השקעות ובנין בע"מ
* **Sources:** Q1 `…_1745275.pdf` pp. 37–39 (fin p38); Q2 `…_1767607.pdf` pp. 118–120 (fin p119, header p118).
  * The earlier blocks (Q1 pp. 19–20, Q2 pp. 103–104) are investee HADAR S.A.R.L.
  * pp. 50–51 and 132–133 are separate data. The statement pick is confirmed.
* **Columns:** standard 3 (Q1) and 5 (Q2). **Units:** אלפי ש"ח.
* **Mapping:**
  * bonds → 3/8; "אשראי בעלי עניין" net (no term) → 5;
  * LT loans → 4/7; project loans "הלוואת/הלוואה בגין פרויקטים בביצוע" (gross, project finance) → 4/7;
  * ST credit from banks and others, gross receipt/repayment lines → 5.
* **(\*):** operating "ריבית ששולמה" (5,073)/(3,815)/(20,910) and (10,175)/(11,190)/(5,102)/(7,375)/(20,909).
  The FY interest differs by 1 between the reports (20,910 vs 20,909); this is in the column notes (info rows are not part
  of C3).
* **Source issue:** Q1 3M-2025 lines sum to 7,911 but the printed total is 7,903 (+8), confirmed on the image.
  * Q2-derived figures match 7,903; the difference sits in the LT-loan lines: Q1 receipt (392) + repayment (27) vs Q2
    receipt 0 + repayment (427).
  * Kept as printed; `issues` + C1 explanation + C2-item 4/7 explanations in `719_checks.json`.
* **Overrides:** items, notes, Q2 `line_text` (parentheses), context_sections (appendix B), report and column notes, issues.
* **Re-check correction:** the C1 explanation no longer claims a 300-DPI zoom (that image was never displayed).
* **Validate:** PASS 329 / FAIL 1. The FAIL is AC6 C1 for this documented source inconsistency (SCRIPT-ISSUE 1).

### 771 גבאי מניבים ופיתוח בע"מ
* **Sources:** Q1 `…_1744961.pdf` pp. 60–61 (fin p60); Q2 `…_1763641.pdf` pp. 62–63 (fin p62).
  Q2 `-01` = appraisal of hotel "רוקסון דזרט", ערד (K.S שמאות), not used.
* **Columns:** Q2 c1/c2 headers set explicitly to 6M (the extractor had inferred them; the image says "לשישה חודשים").
  **Units:** "(באלפי ש"ח)" in the title.
* **Mapping:**
  * bonds → 3/8; "ריבית ששולמה" (financing) → 13; LT loans from banks and others → 4/7; ST credit net → 5;
  * **"קבלת הלוואה מחברת האם" → 4**: owner's loan back-to-back with the parent's Series B bonds, ~390M, 5.43%, repaid per
    the bonds' schedule (note 3ב).
* **(\*):** interest in financing only; investing shows interest received only, so (\*) = 0.
* **Checks:** C2-item 4/7 (195): Q1 shows a separate repayment line, Q2 nets it into receipts. Presentation difference,
  explained in `771_checks.json`.
* **Validate:** PASS 324 / FAIL 0.

### 1680 לסיכו בע"מ
* **Sources:** Q1 `…_1745093.pdf` pp. 31–33 (fin p32); Q2 `…_1764623.pdf` pp. 36–38 (fin p37).
  * The extractor missed Q2 p38 (appendices B–C). I added it to `cf_pages` and re-extracted; the lines were unchanged.
  * Q2 pp. 36–38 carry the wrong running header "באורים לדוחות הכספיים ביניים מאוחדים". The content is the consolidated
    statement, so this is recorded in `issues`.
  * pp. 60–62 / 73–75 = separate data.
* **Mapping:**
  * parent dividend → 11; NCI dividend → 12; bonds → 3; lease principal → 10; LT loans → 7; ST loans net → 5;
  * **"תשלום תמורה מותנית בגין צירוף עסקים" (1,000) → אחר** (conventions §7).
* **(\*):** operating "ריבית ששולמה" (1,537)/(1,362)/(9,730) and (6,100)/(4,274)/(4,563)/(2,912)/(9,730), inside the
  operating total. "דיבידנד שהוכרז וטרם חולק" 4,000 is non-cash and not a (\*) line.
* **Overrides:**
  * Q1 `boxes.31.header` so the (\*) crop shows that page's headers (SCRIPT-ISSUE 3);
  * Q2 `cf_pages`; context_sections; column notes ("(\*) הצגה מחדש … באור 1-ד" marks operating values only).
* **Checks:** C1/C2/C3 all OK.
* **Validate:** PASS 326 / FAIL 0.

### 2389 פרופדו בע"מ
* **Sources:** Q1 `…_1745138.pdf` pp. 38–41 (fin p39); Q2 `…_1766465.pdf` pp. 50–53 (fin p51).
  pp. 56–57 / 71–72 = separate data.
* **Mapping:**
  * lease → 10;
  * "קבלת/פירעון הלוואות מתאגידים בנקאיים ואחרים" (gross, no term; mostly project credit) → 4/7;
  * loans from NCI holders in subsidiaries → 4/7 (the auto suggestion was 6);
  * **"תקבולים בגין הנפקת אגרות חוב ואופציות, נטו" → 3** (auto: 2). In 2025 it was a bonds + warrants package where the
    warrant component is only 915 of 58,751 per the equity statement; in Q2-2026, 17,761 is the Series A expansion of
    20.4.2026 (note 6י). Conventions §6, dominant instrument.
  * "הנפקות הון" → 1; warrant exercises → 2.
* **(\*):** operating interest paid (3,327)/(1,370)/(7,806) and (4,684)/(1,486)/(1,357)/(116)/(7,806).
* **Re-check correction:** Q2 c2/c4 column notes no longer quote a footnote that is not printed on the cash-flow pages.
  The equity statement's footnote "הצגה מחדש של מספרי השוואה, ראו ביאור 2ג'" is now cited.
* **Checks:** C1/C2/C3 all OK.
* **Validate:** PASS 330 / FAIL 0.

### 2396 אשל הירדן יזום ובנין בע"מ
* **Sources:** Q1 `…_1744629.pdf` pp. 34–35 (fin p35); Q2 `…_1767492.pdf` pp. 36–37 (fin p37).
  * pp. 47–49 / 52–54 are the condensed statements of another company, "דיורים בע"מ", not used.
* **Columns:** the Q1 headers print only "ליום 31 במרס 2026/2025" and "ליום 31 בדצמבר 2025". Set as 3M / 3M / FY with
  column notes; C2 confirms them.
* **Mapping:**
  * **"פירעון התחייבות קרן וריבית בגין זכות שימוש" → 10** (auto 7; principal + interest unsplit);
  * **"רכישה עצמית של אג"ח סדרה ב' ו-ג'" → 8** (auto 9; a bond buy-back, not shares);
  * "קבלת/פירעון הלוואות מבעלי עניין ואחרים" → 4/7. In 2026 the 233,270 receipt is mainly the institutional ליווי loan for
    מבואות דרומיים (note 5ג: facility up to 250M until 30.11.2029).
  * bonds and issue costs → 3; LT bank loans → 7; "קבלה (פירעון) הלוואות בגין פרויקטים, נטו" → 5; interest (financing) → 13.
* **(\*):** none outside financing (only dividends and interest received there).
* **Re-check corrections:**
  * the Q1 total label is now verbatim "מזומנים נטו, (ששימשו) שנבעו מפעילות מימון";
  * the report notes now name pp. 47–49 / 52–54 correctly ("דיורים בע"מ", not separate data).
* **Checks:** C2 ±1 rounding in both quarters, explained in `2396_checks.json`:
  * 2026: bank-loan repayment (67) vs Q2-derived (66);
  * 2025: interested-party repayment (8,638) vs (8,637).
* **Validate:** PASS 328 / FAIL 0.

### 2440 גשם למשתכן בע"מ
* **Sources:** Q1 `…_1745527.pdf` pp. 47–48 (fin p48); Q2 `…_1767784.pdf` pp. 51–53 (fin p52).
  pp. 64–65 / 73–74 = separate data.
* **Mapping:**
  * controlling-holder liability net (no term) → 5; ST credit from banks and others net → 5;
  * interest (financing) → 13; lease principal → 10; bonds → 3/8.
* **(\*):** none outside financing; operating shows only taxes paid and investing interest received.
* **Re-check correction:** the Q2 p53 caption now quotes both appendices exactly. Both are printed "נספח ב".
* **Checks:** C1/C2/C3 all OK.
* **Validate:** PASS 323 / FAIL 0.

### 2464 יוזמות - פיתוח נדל"ן בע"מ
* **Sources:** Q1 `…_1746287.pdf` pp. 92–93 (fin p93); Q2 `…_1767804.pdf` pp. 92–94 (fin p93).
  Q1 `-01` = comprehensive appraisal by Naor / Katz / Axelrod (hotel and retail building, סמטת בית הבד 3, ת"א), not used.
* **Mapping:**
  * ST credit net → 5; bonds net → 3. In Q2 the 3M-2025 bond line prints (573), issue costs paid in the quarter; kept as
    printed, with a note.
  * bank loans and related-party loans (both non-current on the balance sheet) → 4; lease → 10;
    interest (financing, 2026 only) → 13.
  * **"פרעון הלוואות ושטר הון מצדדים קשורים" (1,310) → 7**: 1,000 repays a capital note (equity; 869 owners + 131 NCI) and
    310 repays loans (note 5ג3, equity statement). The line is unsplit. Mapping decision; the alternative is 11 for the
    capital-note part.
* **(\*):** none outside financing.
* **Re-check correction:** appendix labels quoted as "(א)/(ב)", as printed.
* **Checks:** C1/C2/C3 all OK.
* **Validate:** PASS 325 / FAIL 0.

### 2503 לנטרה קנדה אנטרפרייזס לימיטד פרטנרשיפ (CAD, limited partnership)
* **Sources:** Q1 `…_1743729.pdf` pp. 48–49 (fin p49); Q2 `…_1765098.pdf` pp. 51–52 (fin p52).
  * The NIS translation of the same statement (Q1 pp. 63–64, Q2 pp. 69–70) and the separate data (CAD Q1 p78 / Q2 p86;
    NIS Q1 p85 / Q2 p94) are not used.
* **Units:** "באלפי דולר קנדי, למעט אם צוין אחרת", currency דולר קנדי; no conversion.
* **Mapping (conventions §2):**
  * "השקעות בעלים" → 1; "חלוקות לבעלים" → 11.
  * **"הלוואות ללא מועד פרעון לבעלי השליטה" → 11** (auto 7). It is a loan given TO the controlling holder with no repayment
    date, booked directly in equity ("קרן הון עם בעל שליטה"), i.e. a distribution in substance. Mapping decision; the
    alternative is אחר.
  * NCI receipts → 6; purchase of NCI (825) → 14; loans from financial institutions and others → 4/7;
    related-party loans → 4/7; bonds → 3; interest (financing) → 13.
* **(\*):** interest in financing only.
* **Checks:** C2 2026 total −1,793, explained in `2503_checks.json`:
  * the whole difference is interest paid: Q1 (3,231) vs Q2-derived (1,438);
  * operating "ספקים וזכאים ויתרות זכות" differs by the same amount (11,454 vs 9,661), so the cash change is identical.
    This is a classification difference between the reports.
  * 2025 items 4 / 11 differ by ±1 and offset each other (explained).
* **Validate:** PASS 332 / FAIL 0.

### 2570 ס.י לאונרדו התחדשות עירונית בע"מ (Q2 only)
* **Source:** `…_2026_Q2_1767187.pdf` pp. 41–42.
  * The title "דוחות תמציתיים מאוחדים של תזרימי המזומנים" confirms the Phase A correction.
  * pp. 59–60 "תמצית נתונים על תזרימי המזומנים ביניים" = separate data with different figures (viewed).
* **Mapping:**
  * bank-loan repayment → 7;
  * "קבלת/פירעון הלוואות מאחרים" (project finance from financial institutions, note 3) → 4/7;
  * related-party loans → 4/7; interest (financing) → 13; lease principal → 10.
* **(\*):** none outside financing.
* **Checks:** C1 0.
* **Validate:** PASS 207 / FAIL 0.

---------------------------------------------------------------------------------------------------------------

## 2. Mapping decisions (cross-batch judgement calls for Phase C)

1. **Loan lines without a stated term** (batches decide differently; please align):
   * Batch 8 rule:
     * a term printed on the line decides;
     * a **net** line without a term → 5 (R3);
     * a **gross** line without a term → by economic nature from the balance sheet and notes: short-term facilities or
       short-term loans → 5; long-term loans and project/land finance (ליווי, even if current by operating cycle) → 4/7.
   * Applied to 584 (receipts "מאחרים" → 4, repayments "מאחרים" → 5, "מתאגידים פיננסיים" → 5), 719 (project loans 4/7),
     2389 (banks and others 4/7), 2396 (institutional ליווי loan 4), 2570 (project finance 4/7).
   * Other batches' progress files differ:
     * gross lines without a term → 4/7 by default in batches 1 and 2, and batch 3 for 2486;
     * → 5 when the balance-sheet balance is current in batches 4, 6 and 7, and batch 3 for 2567;
     * batch 5 decided by the balance sheet (non-current → 4/7).
2. **Loans from NCI holders in subsidiaries** → 4/7 (2389; R3 lists NCI holders under item 4), not 6/12.
3. **Loan given TO the controlling holder, booked in equity** (2503 "הלוואות ללא מועד פרעון לבעלי השליטה") → 11
   (distribution in substance); alternative: אחר.
4. **Unsplit repayment of loans + capital note to related parties** (2464 Q2, 1,310) → 7; alternative: split is
   impossible, or 11 for the capital-note part.
5. **Bonds + warrants package not split** (2389, warrants 915 of 58,751) → 3 (dominant instrument, conventions §6).
6. **Sale of subsidiary shares to an NCI holder labelled "רכישה עצמית של מניות על ידי בעלי זשמ"ש"** (573 Q2) → 6, by the
   note, not by the label.
7. **Lease line "קרן וריבית"** (2396) → 10 (principal + interest unsplit); bond buy-back "רכישה עצמית של אג"ח" → 8.
8. **Appendix-only interest without a stated section** (573, 584): positive as printed, note per conventions §1
   ("הסעיף לא צוין"). For 584 the appendix may also include the financing-section interest (2025); noted, not netted.
9. **Owner's loan from the parent, back-to-back with the parent's bonds** (771) → 4/7, not 5 (it has a schedule).
10. **Contingent consideration paid** (1680) → אחר (conventions §7).

---------------------------------------------------------------------------------------------------------------

## 3. SCRIPT-ISSUEs

```
SCRIPT-ISSUE 1
  script:     validate.py (AC6, line 90: ok(abs(sum(items)+other-total) < 1e-6, "... AC6 C1 ..."))
  report:     719 Q1 (3 חודשים שהסתיימו ב-31.03.2025)
  symptom:    FAIL "[719] AC6 C1 דוח Q1 2026 | 3 חודשים שהסתיימו ב-31.03.2025" although the C1 difference (+8) is a printed
              source inconsistency, kept as printed per conventions §9 and explained in 719_checks.json (checks.py:
              unexplained mismatches 0). Evidence: %TEMP%\fcf_run\_runs\validate_20261110-113535_24544\validate.txt.
              Batch 2 reports the same for 715.
  expected:   AC6 should accept a C1 difference that has an explanation (as AC8 does via checks.explain).
  workaround: none possible without a plug value; values kept as printed. Validate result 329 PASS / 1 FAIL.
  severity:   blocks validate FAIL 0 for 719 only (the deliverable itself is correct and final).

SCRIPT-ISSUE 2
  script:     fcf_render.py (context pages, lines 352/394: `outs` is the report-wide (*) list)
  report:     573 Q1 p38, 573 Q2 p40, 584 Q2 p31
  symptom:    every operating/investing context page is captioned "שורות ה-(*) שבעמוד זה מוצגות בהגדלה בתמונה ייעודית"
              when the report has any (*) line, even if that page has none (the (*) line is on the appendix page).
  expected:   the note should test the (*) lines of that page only.
  workaround: context_sections with the exact appendix title for those pages → accurate "עמוד המשך" caption.
  severity:   cosmetic.

SCRIPT-ISSUE 3
  script:     fcf_render.py / auto geometry ((*) crop header strip)
  report:     1680 Q1 (p31)
  symptom:    the (*) crop showed only the page title, without the column headers, because the extractor did not box that
              page's header (same as batch 7 SCRIPT-ISSUE 1).
  expected:   a header strip covering the column headers on every page that carries a (*) line.
  workaround: boxes.31.header [55, 46, 546, 171] (verified on the composite image).
  severity:   cosmetic (legibility of the (*) crop).

SCRIPT-ISSUE 4 (minor)
  script:     fcf_extract.py (statement pages; context section labels)
  report:     1680 Q2; 573, 584, 719, 771, 2389, 2440, 2464
  symptom:    (a) cf_pages of 1680 Q2 missed the appendix page 38; (b) appendix-only pages are labelled 'פעילות שוטפת' or
              'פעילויות שלא במזומן' in the screenshot captions.
  workaround: (a) cf_pages override + extract_report.py (lines unchanged); (b) context_sections with the printed
              appendix titles.
  severity:   cosmetic.
```

Environment issue (not a script): the `view` tool returned no image from 10:14 to ~11:02 (cap of 50). Handled as in §0.

---------------------------------------------------------------------------------------------------------------

## 4. Final status

| issuer | reports | status | validate |
|---|---|---|---|
| 573 משולם לוינשטין | Q1, Q2 | verified (re-checked on images 11:18) + built | PASS 338 / FAIL 0 |
| 584 א.ליבנטל | Q2 | verified (re-checked 11:23) + built | PASS 140 / FAIL 0 |
| 719 א.לוי | Q1, Q2 | verified (re-checked 11:24) + built | PASS 329 / FAIL 1 (SCRIPT-ISSUE 1, documented source C1 +8) |
| 771 גבאי מניבים | Q1, Q2 | verified (re-checked 11:24) + built | PASS 324 / FAIL 0 |
| 1680 לסיכו | Q1, Q2 | verified (re-checked 11:25) + built | PASS 326 / FAIL 0 |
| 2389 פרופדו | Q1, Q2 | verified (re-checked 11:26) + built | PASS 330 / FAIL 0 |
| 2396 אשל הירדן | Q1, Q2 | verified (re-checked 11:26) + built | PASS 328 / FAIL 0 |
| 2440 גשם | Q1, Q2 | verified (re-checked 11:27) + built | PASS 323 / FAIL 0 |
| 2464 יוזמות | Q1, Q2 | verified (Q2 seen 11:03–11:06; Q1 completed 11:27) + built | PASS 325 / FAIL 0 |
| 2503 לנטרה קנדה | Q1, Q2 | verified (seen 11:07–11:12) + built | PASS 332 / FAIL 0 |
| 2570 לאונרדו | Q2 | verified (seen 11:12–11:14) + built | PASS 207 / FAIL 0 |

`checks.py --issuers 573 584 719 771 1680 2389 2396 2440 2464 2503 2570`: unexplained mismatches 0. The 20 reports have
C1 = 0 in every column except 719 Q1 3M-2025 (+8, source). C2 mismatches (all explained): 2396 ×2 (±1), 2503 2026
(1,793). C3: 144 OK. `tool_integrity.py`: CLEAN.

Assisted-by: Anthropic:Claude Opus 5.5
