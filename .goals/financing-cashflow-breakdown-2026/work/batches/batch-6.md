# Batch 6 — Phase B report (iteration 1)

Builder: Phase B batch 6. Issuers: 373, 434, 444, 673 (Q2 only), 823, 1484, 1561, 1724, 2417, 2441, 2574 (Q2 only).
That is 20 reports and 11 companies.
Protocol: `work\PIPELINE.md` §0–§13 plus `work\phaseB-conventions.md`. Goal: `goal.md` with amendments 1 and 2 (T1 and T2 apply; T3 is cancelled).
Checkpoint: `work\batches\batch-6-progress.md`.

## Summary

| issuer | reports | status | C1 / C2 / C3 (unexplained) | validate `--no-master` |
|---|---|---|---|---|
| 373 אאורה | Q1, Q2 | verified + built | 8 OK / 2 OK / 16 OK (0) | PASS 333 FAIL 0 |
| 434 ישראל קנדה | Q1, Q2 | verified + built | 8 OK / 2 MISMATCH −1 explained / 16 OK (0) | PASS 340 FAIL 0 |
| 444 מרדכי אביב | Q1, Q2 | verified + built | 8 OK / 2 OK / 16 OK (0) | PASS 320 FAIL 0 |
| 673 ריי | Q2 only | verified + built | 3 OK / n.a. / n.a. (0) | PASS 136 FAIL 0 |
| 823 חג'ג' | Q1, Q2 | verified + built | 8 OK / 2 OK (+2 item INFO) / 16 OK (0) | PASS 330 FAIL 0 |
| 1484 מצלאוי | Q1, Q2 | verified + built | 8 OK / 2 MISMATCH explained (23; 23,312) / 16 OK (0) | PASS 319 FAIL 0 |
| 1561 הכשרת הישוב | Q1, Q2 | verified + built | 8 OK / 2 OK / 16 OK (0) | PASS 322 FAIL 0 |
| 1724 רמות בעיר | Q1, Q2 | verified + built | 8 OK / 2 MISMATCH ±1 explained / 16 OK (0) | PASS 324 FAIL 0 |
| 2417 אנשי העיר | Q1, Q2 | verified + built | 7 OK + 1 MISMATCH −1 (source) explained / 1 OK + 1 MISMATCH +1 explained / 16 OK (0) | PASS 323 **FAIL 1** (SCRIPT-ISSUE 1) |
| 2441 שובל | Q1, Q2 | verified + built | 8 OK / 2 OK / 16 OK (0) | PASS 328 FAIL 0 |
| 2574 עמים | Q2 only | verified + built | 5 OK / n.a. / n.a. (0) | PASS 205 FAIL 0 |

Batch-wide results:
- `checks.py --issuers <all 11>`:
  - C1: 79 OK and 1 MISMATCH (explained).
  - C2: 11 OK and 7 MISMATCH (all explained).
  - C2-item: 17 INFO (all explained).
  - C3: 144 OK.
  - **Unexplained mismatches: 0.**
- `validate.py --issuers <all 11> --no-master`: **PASS 3220, FAIL 1.** The only FAIL is 2417's per-column AC6 check (SCRIPT-ISSUE 1).
  - The integrity and hygiene checks passed.
- Each company folder holds its two outputs, built without `--draft`.
- No git was used, and no scripts or shared files were changed.
- Temp folders `%TEMP%\fcf_run\<iss>\` were deleted for all 11 issuers.

### Verification method (applies to all 20 reports)

Every report was verified against rendered images, not the text layer:
- Each composite image combined two parts, both from `tool_review.py` (≥ 220 DPI):
  - the header strip (company, title, column headers, units) plus the whole financing section, with framed and numbered lines;
  - the red (\*) crop of each line outside financing.
- Every line text and every value was compared digit by digit with `lines_*.txt`.
- The pages of each company's screenshots PDF were then checked as tiled overviews:
  - the full page with the orange financing box and the blue header box;
  - the zoom page and the (\*) crops;
  - the context pages (operating and investing sections);
  - the captions.
- Extra zooms: 300 DPI on 673 Q2's lease label and 170 DPI bands on 1484's cash lines.
- A text search of every statement page for `ששולמ` / `דיבידנד` / `ריבית` confirmed that no other interest- or dividend-paid line exists.
  - Receipts and dividends received from investees were excluded.
- Each override's `verified.method` names the actual image files viewed.

**Process note:**
- During roughly the first 70 minutes, the `view` tool returned "maximum number of images" without showing anything.
- So every check made in that window was redone once images displayed (11:10–11:25). The verification records were rewritten to cite the images actually seen.
- No value had to change; every figure read earlier from the text layer matched the images.

---------------------------------------------------------------------------------------------------------------

## 373 אאורה השקעות בע"מ

- **Sources:**
  - Q1: `373_אאורה השקעות בע_מ_2026_Q1_1743923.pdf` (77 pp). Consolidated cash-flow statement pp. 53–54; financing p. 54; headers p. 54.
  - Q2: `..._Q2_1767006.pdf` (83 pp). Statement pp. 57–58; financing p. 58.
  - The separate (38D) data on pp. 69–71 (Q1) and pp. 76–77 (Q2) was not used.
- **Columns:**
  - Q1: 3M-31.03.2026, 3M-31.03.2025, FY-2025.
  - Q2: 6M-2026, 6M-2025, 3M Apr–Jun 2026, 3M Apr–Jun 2025, FY-2025.
  - All checked on the image.
- **Units/currency:** אלפי ש"ח.
- **Text layer:** usable (repaired). The broken-font `נ` was fixed and every label was compared with the image. The Q2 total prints `מזומנים, נטו - שנבעו מעילות מימון`; the source typo is kept verbatim with a note.
- **Mapping:**
  - ST credit "מתאגידים בנקאיים ומאחרים, נטו" → 5.
  - LT bank loans → 4 / 7.
  - Lease → 10.
  - Warrant exercise → 2.
  - Bonds, net → 3; bond repayment → 8.
  - Dividend → 11.
  - Buy-back (Q2, (12,223); note 6) → 9.
  - **`עסקאות עם בעלי זכויות שאינן מקנות שליטה` (5,756) → 14** (the extractor suggested 6). It is the purchase of 776,380 additional shares of the subsidiary מגידו י.ק. (note 5; equity statement: capital reserve (3,392) + NCI (2,364)).
  - Subsidiary shares issued to NCI (224,440) → 6.
  - **Subsidiary options issued to NCI (24,010) → 6**, not 2.
- **(\*):** interest paid in operating.
  - Q1 p. 53: (54,473) / (32,660) / (167,395).
  - Q2 p. 57: (101,995) / (79,161) / (47,522) / (46,501) / (167,395).
  - Dividends are paid only in financing; investing shows only dividends received.
- **Restatement:** note 2ג restates the comparatives. In the statement only some operating amounts carry (\*); no column header is marked.
  - So no `(מוצג מחדש)`; column notes on Q1 c2 and Q2 c2/c4/c5 (conventions §10).
- **Overrides:** `line_items` (Q1 8→14; Q2 9→14), notes, column notes, report notes, verification record.
- **Checks:** C1 0 everywhere; C2 OK; C3 16/16 OK.

## 434 ישראל קנדה (ט.ר) בע"מ

- **Sources:**
  - Q1: `434_ישראל קנדה (ט.ר) בע_מ_2026_Q1_1744562.pdf` (118 pp). Statement pp. 53–56; financing p. 53.
  - Q2: `..._Q2_1766574.pdf` (132 pp). Statement pp. 58–61; financing p. 58.
  - p. 23/24 is a board-report table and the later blocks are separate or investee data, so the pick is confirmed.
- **Units:** אלפי ש"ח, printed under each column.
- **Mapping:**
  - **`פירעון אגרות חוב ורכישה עצמית` → 8** (suggested 9). It is the repayment and buy-back of bonds; the equity statements show no share buy-back in these periods.
  - **`מיזוג חברה בת - ראה נספח ה'` (FY-2025 69,692) → אחר.** Appendix E breaks it into working capital, financial assets, associates, deferred taxes, NCI capital reserve and NCI: a mixed merger flow (PIPELINE §7 merger flows).
  - **`עסקאות עם בעלי זכויות שאינן מקנות שליטה(, נטו)` → 6 as one line.** It is net with mixed signs:
    - Q1-2026 +91,887 = sale of subsidiary shares without loss of control (equity: capital reserve 39,704 + NCI 52,183).
    - The negative columns (2025, Apr–Jun 2026 (689)) are net payments to NCI.
    - The tooling has no 6/14-by-sign code, so the line was kept whole with a note. **Phase C alignment item.**
  - Loans from others → 7.
  - `חלוקות לזכויות שאינן מקנות שליטה` → 12.
  - Equity investments of NCI → 6.
  - `אשראי מתאגידים בנקאיים, נטו` → 5.
- **(\*):** interest paid appears only in appendix B, "מידע נוסף על תזרימי המזומנים מפעילות שוטפת", under "מזומנים ששולמו במשך התקופה עבור: ריבית", printed as **positive** amounts.
  - Section: פעילות שוטפת. Note: `גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת` (conventions §1).
  - Q1 p. 55: 74,802 / 67,935 / 341,471.
  - Q2 p. 60: 213,285 / 179,042 / 128,219 / 107,136 / 378,178. The 2025 columns are marked `(*) סווג מחדש`, so FY-2025 interest is 378,178 in Q2 against 341,471 in Q1. This is noted in the info note and in a column note (the (\*) rows are not part of C3).
- **Overrides:**
  - `outside` replaced: text includes the heading, bbox covers heading and line.
  - `boxes.header` on p. 55 and p. 60, so the (\*) crop shows the appendix's column headers.
  - `context_sections` for the appendix pages (the extractor labelled them "פעילויות שלא במזומן").
  - Column notes for the operating `(*) סווג מחדש` marks.
- **Checks:**
  - C1 0.
  - C3 16/16 OK.
  - C2 total −1 in both 3M-2026 and 3M-2025: source rounding. Item-level ±1–3 differences in ST credit, NCI, lease, NCI distributions, shares 124,432 vs 124,431, and bonds 208,592 vs 208,591.
  - All explained in `overrides\434_checks.json`.

## 444 מרדכי אביב תעשיות בניה (1973) בע"מ

- **Sources:**
  - Q1: `..._Q1_1745537.pdf` (54 pp). Statement pp. 35–36; financing p. 35.
  - Q2: `..._Q2_1763129.pdf` (58 pp). Statement pp. 37–38; financing p. 37.
  - The pick over pp. 24–25/25–26 (separate data) is confirmed.
- **Units:** the title prints `(באלפי ₪)` in Q1 and `(באלפי ש"ח)` in Q2. Q1 `units_text` was fixed from the garbled `באלפי)₪`.
- **Mapping:**
  - Bond repayment → 8; bond issue (zero) → 3.
  - Dividend → 11.
  - Loan from an associate (zero) → 4.
  - `קבלת / פרעון הלוואות מתאגידים בנקאיים` → 4 / 7. These are gross lines without a term; the balance sheet presents the bank loans as non-current loans plus current maturities.
- **(\*):** interest paid only in "מידע נוסף" of appendix A (reconciliation to operating), positive as printed.
  - Section פעילות שוטפת; appendix note.
  - Q1 p. 36: 10,199 / 12,504 / 37,715.
  - Q2 p. 38: 13,075 / 16,834 / 2,876 / 4,330 / 37,715.
- **Overrides:**
  - `units`; notes.
  - Q2 `outside` replaced (section label).
  - `boxes.header` on p. 36 and p. 38 (the (\*) crop shows the column headers).
  - `context_sections`.
- **Checks:** C1/C2/C3 all OK, including per item and the (\*) interest.

## 673 קבוצת ריי טי.אל.וי בע"מ (Q2 only)

- **Source:** `673_..._Q2_1767512.pdf` (42 pp). One-page statement, p. 31.
- **Columns:** 6M-2026, 6M-2025, FY-2025. There are no 3-month columns.
- **Units:** אלפי ש"ח.
- **Mapping:**
  - **The gross loan lines without a term go to 5:** `קבלת הלוואות מבעלי עניין וצדדים קשורים`, `קבלת הלוואות מתאגידים בנקאיים`, `קבלת הלוואות מאחרים`, `פרעון הלוואות מאחרים`.
    - The consolidated balance sheet shows all credit and loans from banks, others and related parties as **current liabilities** (non-current from others only 0 / 347 / 485).
    - Note 3 confirms short-term loans: the bank loan of about 1 million due 31.12.2026, and the Ashtrom loan repaid in full.
  - **`תמורה מהנפקת מניות וכתבי אופציה, נטו` → 1** (conventions §6).
  - Interest paid in financing (`ריבית ששולמה לתאגידים בנקאיים ואחרים`) → 13.
  - Lease → 10.
- **(\*):** none outside financing. Operating shows only taxes paid.
- **Checks:** C1 0. C2/C3 do not apply (no Q1 report).

## 823 קבוצת חג'ג' ייזום נדל"ן בע"מ

- **Sources:**
  - Q1: `..._Q1_1745710.pdf` (87 pp). Statement pp. 59–61; financing p. 60.
  - Q2: `..._Q2_1767825.pdf` (100 pp). Statement pp. 68–70; financing p. 69.
  - The Q2 `-01` file is a valuation, not a source.
- **Units:** אלפי ש"ח.
  - In Q1 the units are printed only under the headers of p. 59, so **`header_page` was set to 59** and the zoom shows the p. 59 header strip plus the p. 60 section.
- **Mapping:**
  - Bonds, net → 3; bond repayment → 8.
  - Lease → 10.
  - **`הנפקת אופציות` → 2.** These are warrants issued by the company, credited to share premium (21,156 / 21,155), on their own line.
  - Option exercise → 2.
  - Treasury shares → 9.
  - Dividend (Q2 (33,000)) → 11.
  - `קבלת / פירעון הלוואות מתאגידים בנקאיים, מוסדות פיננסיים ואחרים` → 4 / 7. These are gross lines covering all borrowing (there is no separate ST line); classified by the nature "receipt/repayment of loans", with a note.
- **(\*):** interest paid only in appendix B, positive as printed; appendix/operating note.
  - Q1 p. 61: 50,997 / 57,003 / 234,755.
  - Q2 p. 70: 85,960 / 94,563 / 34,963 / 37,560 / 234,755.
  - The operating line "dividend from an equity-accounted company" is a receipt and is not (\*).
- **Checks:**
  - C1, C2 and C3 OK.
  - C2-item ±1 in loans received and repaid for 3M-2025 offset each other (explained in `823_checks.json`).

## 1484 מצלאוי חברה לבנין בע"מ

- **Sources:**
  - Q1: `..._Q1_1743676.pdf` (44 pp). Statement pp. 33–34; financing p. 34.
  - Q2: `..._Q2_1767668.pdf` (48 pp). Statement pp. 35–36; financing p. 36.
- **No 'מאוחד' in the title:** the company has **no subsidiaries** (note 1ג defines only joint arrangements). The statements are titled "דוחות על תזרימי המזומנים" and the file has no separate data, so the primary statement was used (report note).
- **Units:** אלפי ש"ח.
- **Mapping:**
  - Lease → 10. Q2 prints positive 1,854 / 2,342 on this repayment line; kept as printed in item 10 with a note.
  - Bonds → 8.
  - `פירעון הלוואות לזמן ארוך` → 7. FY-2025 prints **+23,659** on this repayment line in both reports; kept as printed in item 7 with a note, following the PIPELINE §5 example. **Phase C alignment item.**
  - ST credit "בנקאיים ואחרים, נטו" → 5.
  - Treasury shares, net (Q2) → 9.
- **(\*):** interest paid in operating.
  - Q1 p. 33: (1,679) / (3,082) / (11,808).
  - Q2 p. 35: (5,900) / (4,855) / (4,221) / (1,773) / (11,808).
- **Source issue (Q2, recorded in `issues`):** the 2025 comparative columns of the Q2 statement are internally inconsistent, verified on a 170-DPI render.
  - 6M-2025: the sections sum to 10,572, but the printed cash change is 11,542.
  - Apr–Jun 2025: the sections sum to 1,658, but the printed change is (8,862).
  - Closing cash at 30.6.2025 is 46,381 in one column and 55,050 in the other.
  - The opening balance at 1.4.2025 (63,912) differs from the Q1 report's closing balance at 31.3.2025 (65,179).
- **C2 (both explained in `1484_checks.json`; values as printed):**
  - 3M-2026: Q1 (4,089) vs 32,940 − 37,006 = (4,066), a difference of 23, all in bond repayment ((34,210) vs (34,187)). The cash change is identical in both reports (19,660), so the 23 was reclassified to other activities in Q2.
  - 3M-2025: Q1 15,617 vs 21,278 − 28,973 = (7,695), a difference of 23,312 (ST credit 22,834; LT loans 604; bonds −126). It comes from the inconsistent Q2 comparatives above; investing for Q1-2025 is identical in both reports (64,451).
- **Checks:** C1 0; C3 16/16 OK.

## 1561 הכשרת הישוב התחדשות עירונית בישראל בע"מ

- **Sources:**
  - Q1: `..._Q1_1741645.pdf` (28 pp). Statement pp. 22–23; financing p. 22.
  - Q2: `..._Q2_1762505.pdf` (33 pp). Statement pp. 26–27; financing p. 26.
- **Units:** `(באלפי ש"ח)` in the title.
- **Text fix:** the Q1 lease label in the text layer reads `יפרעון`; the image shows `פירעון`, corrected with `line_text`.
- **Mapping:**
  - **`סכומים שהתקבלו משותף בעסקת פינוי בינוי` → 4** (the extractor suggested אחר). The balance sheet shows "התחייבות לשותף בעסקת פינוי ובינוי" as a **non-current liability** (45,741 / 42,250 / 47,298), so this is long-term financing from another party.
  - **`קיטון בהלוואה מהחברה האם` → 5** (net, no term; conventions §5).
  - NCI receipts → 6.
  - `הנפקת מניות` → 1. It includes warrants (private placement of 2,995,587 shares and 2,995,587 warrants, note 3א; conventions §6).
  - ST bank credit, net → 5; lease → 10.
- **(\*):** interest paid only in appendix A (operating reconciliation), under "מזומנים ששולמו במהלך התקופה עבור"; section פעילות שוטפת, appendix note.
  - Q1 p. 23: (116) / (181) / (653).
  - Q2 p. 27: (229) / (315) / (113) / (134) / (653).
- **Checks:** C1/C2/C3 OK, also per item.

## 1724 רמות בעיר בע"מ

- **Sources:**
  - Q1: `..._Q1_1742818.pdf` (74 pp). Statement pp. 49–50; financing p. 49.
  - Q2: `..._Q2_1763829.pdf` (80 pp). Statement pp. 53–54; financing p. 53.
  - The separate data on p. 69/75 was not used.
- **Units:** אלפי ש"ח, printed under each column.
- **Mapping:**
  - **`הנפקת שטרי הון לבעלי שליטה` (10,000) → 1** (conventions §4). The capital notes are presented in **equity** attributable to the parent's owners (75,319), and the equity statement shows the issue.
  - Loans "מגוף מוסדי ותאגידים בנקאיים" → 4 / 7.
  - ST credit, net → 5.
  - Bonds → 3 / 8.
  - Q2 has two extra lines used only in its 2025 columns, `פירעון/קבלת הלוואות לזמן ארוך מתאגידים בנקאיים` → 7 / 4. In Q1 those amounts sit in the combined lines.
- **(\*):** interest paid only in an appendix titled "מידע נוסף על תזרימי המזומנים" (Q1 appendix B p. 50; Q2 appendix A p. 54). It does not say which section includes it, and there is no interest line in operating, investing or financing.
  - Note: `גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)` (conventions §1).
  - Q1: (5,415) / (7,948) / (50,630).
  - Q2: (15,598) / (25,561) / (10,183) / (17,613) / (50,630).
- **Restatement marks:** `*` only on operating values (staff position 11-6). Column notes only.
- **Checks:**
  - C1 0; C3 16/16 OK.
  - C2 ±1 in both 3M periods: rounding in LT loans repaid (2026) and received (2025, where Q2 shows the 2025 amount on the separate LT-bank line). Explained in `1724_checks.json`.

## 2417 אנשי העיר מקבוצת רוטשטיין בע"מ

- **Sources:**
  - Q1: `..._Q1_1743889.pdf` (76 pp). One-page statement, p. 66.
  - Q2: `..._Q2_1765496.pdf` (84 pp). One-page statement, p. 71 (page size 612×792).
- **Units:** אלפי ש"ח.
  - In Q2 the units line sits below "בלתי מבוקר", level with the operating heading, and the automatic header strip cut it off.
  - **Manual `boxes.header` [55, 33, 560, 125] on p. 71.** The zoom now shows the units (checked).
- **Mapping:**
  - ST credit "בנקאיים ואחרים בחשבונות ליווי, נטו" → 5.
  - Lease → 10.
  - LT loans from others → 7.
  - LT loans from others and banks → 4.
  - LT loan from the controlling shareholder (related party) → 4.
  - Bonds → 3 / 8.
  - Shares → 1.
- **(\*):** interest paid in operating.
  - Q1 p. 66: (2,158) / (2,865) / (16,153).
  - Q2 p. 71: (7,442) / (8,322) / (5,284) / (5,457) / (16,153).
- **Source issue:** Q1 c2 (3M-2025): the lines (19,619; (87); (10,000); 31,410; 5,000) sum to **45,942**, but the printed total is **45,943**.
  - C1 = −1. Confirmed on the 220-DPI image with crisp digits.
  - Printed values are kept (no plug), with a column note, an `issues` entry and a C1 explanation.
  - Q2 derives ST credit for Q1-2025 as 19,620, so the difference is rounding in that line.
- **Checks:**
  - C2 3M-2026 +1 (ST credit 13,556 vs 13,555); explained.
  - C3 16/16 OK.
  - validate shows **FAIL 1**: AC6 per-column C1 for this column (SCRIPT-ISSUE 1), although `checks.py` accepts the explanation.

## 2441 שובל הנדסה ובניין בע"מ

- **Sources:**
  - Q1: `..._Q1_1743355.pdf` (69 pp). Statement p. 50 plus p. 51 (non-cash activities).
  - Q2: `..._Q2_1764196.pdf` (75 pp). Statement p. 55 plus p. 56.
- **Text layer:** usable (repaired); every label compared with the image.
- **Columns:** the Q1 c2 header ("3 חודשים שהסתיימו ביום 31 במרס 2025", flagged ambiguous) was confirmed on the image.
- **Units:** אלפי ש"ח on the statement page. The Q2 flag "units from p. 53" was resolved; they are printed on p. 55.
- **Mapping:**
  - **`תמורה מהנפקת הון מניות ואופציות, נטו` → 1** (suggested 2; conventions §6).
  - Bonds → 3.
  - Gross ST receipt and repayment lines "מבנקים ואחרים" → 5.
  - LT bank loans → 4; LT loans from others → 7.
  - **`פרעון הלוואה מאחרים` → 7**: a term loan with fixed 1,000 per quarter.
  - Lease principal → 10.
  - Interest paid in financing → 13.
- **(\*):** none outside financing. Operating shows only taxes; investing shows only interest received.
- **Checks:** C1/C2/C3 OK.

## 2574 עמים יזמות בע"מ (Q2 only)

- **Source:** `2574_..._Q2_1767720.pdf` (39 pp). One-page statement, p. 30.
- **Columns:** 6M-2026, 6M-2025, 3M Apr–Jun 2026, 3M Apr–Jun 2025, FY-2025. The flagged c2 header was confirmed on the image.
- **Units:** אלפי ₪.
- **Mapping:**
  - **Related-party loans received / repaid (gross, no term) → 5.** The balance sheet shows related parties only as current liabilities, the same treatment as 673.
  - Loans from banks and financial institutions (gross, no term) → 4 / 7. The balance sheet has a sizeable non-current portion of credit from banks and others, the same treatment as 823.
  - Lease principal → 10.
  - Interest paid in financing → 13.
- **(\*):** none outside financing.
- **Checks:** C1 0. C2/C3 do not apply.

---------------------------------------------------------------------------------------------------------------

## Mapping decisions (cross-company judgement calls for Phase C)

1. **Net NCI-transactions line with mixed signs** (434 `עסקאות עם בעלי זכויות שאינן מקנות שליטה, נטו`).
   - Treated as one line → **6** (dominant flow: sale of subsidiary shares without loss of control), with a note that the negative columns are net payments to NCI (nature 14).
   - The tooling cannot split 6/14 by sign. Alternative: manual-mode split, or a new code.
2. **Line with the same label that is purely a purchase of additional subsidiary shares** (373, purchase of מגידו shares) → **14**.
3. **Subsidiary options or warrants issued to NCI** (373) → **6**, not 2. Item 2 is kept for the reporting entity's own options.
4. **Company's own warrants issued on a separate line** (823 `הנפקת אופציות`) → **2**.
   - Unsplit shares + warrants/options (673, 2441; 1561's share issue included warrants) → **1** (conventions §6).
5. **`פירעון אגרות חוב ורכישה עצמית`** (434) → **8**: buy-back of bonds, as no share buy-back appears in equity.
6. **Merger-of-subsidiary financing line** (434 FY-2025 69,692) → **אחר**: a mixed flow per appendix E.
7. **Gross borrowing lines with no stated term** (not covered by R3's "net without term" rule). Decided from the balance sheet and notes:
   - → **5** when the liability is current or short-term: 673 (all lines), 2574 related-party loans.
   - → **4 / 7** when it is long-term or mixed: 444 bank loans, 823 banks/institutions/others, 2574 banks/institutions, 434 and 2441 loans from others.
   - Other batches may have chosen differently; this needs alignment.
8. **Amounts received from a partner in an urban-renewal (פינוי-בינוי) deal, carried as a non-current liability** (1561) → **4**.
9. **Net decrease in a loan from the parent company** (1561) → **5** (conventions §5).
10. **Capital notes to controlling holders presented in equity** (1724) → **1** (conventions §4).
11. **Positive values on repayment lines:**
    - 1484 `פירעון הלוואות לזמן ארוך` FY-2025 +23,659 → kept as printed in **7**.
    - 1484 Q2 lease +1,854 / +2,342 → kept in **10**.
    - Both have notes, following the PIPELINE §5 example.
    - Alternative for the loan line: `net_loans`, which would send the positive column to 4.
12. **(\*) interest disclosed only in an appendix:**
    - The section is named when the appendix is operating information: 434 and 823 "מידע נוסף על תזרימי המזומנים מפעילות שוטפת", 444 and 1561 inside the operating-reconciliation appendix. Note: `גילוי בנספח ... – נכלל בפעילות שוטפת`.
    - Otherwise (1724) the note says `הסעיף לא צוין (לא בפעילות מימון)`.
    - Values keep their printed sign: positive in 434, 444 and 823.
    - 434 Q2 restates FY-2025 interest (378,178 vs Q1 341,471). The (\*) info rows are not covered by C3, so this is noted only.
13. **Restatement marks on individual values or in a general note only** (373, 434, 1484, 1724): no `(מוצג מחדש)`; column notes only (conventions §10).

## SCRIPT-ISSUEs

```
SCRIPT-ISSUE 1
  script:     validate.py (line ~90, company_checks: ok(abs(sum(items)+other-total) < 1e-6, "AC6 C1 <column>"))
  report:     2417 Q1, column 3 חודשים שהסתיימו ב-31.03.2025
  symptom:    validate --issuers 2417 --no-master → PASS 323 FAIL 1:
              "FAIL: [2417] AC6 C1 דוח Q1 2026 | 3 חודשים שהסתיימו ב-31.03.2025". The per-column AC6 check
              ignores the C1 explanations that checks.py accepts (checks: unexplained mismatches 0). The source itself
              does not add up (lines 45,942 vs printed total 45,943) – goal AC6 and conventions §9 require the printed values
              plus an explanation.
  expected:   the per-column C1 check passes (or warns) when the column has an explanation
              (C1|<iss>|<report>|<period>|total) in <iss>_checks.json / check_explanations.json, as validate's own
              C1–C3 summary check does.
  workaround: none (a plug value is forbidden); values kept as printed, explained in 2417_checks.json, column_notes and issues.
  severity:   blocks FAIL 0 for 2417 (and for any batch with a source C1 difference: 715, 719, 2483, 2533, 531 ...)

SCRIPT-ISSUE 2
  script:     fcf_extract.py (context_sections) + fcf_render.py (context-page captions)
  report:     434 Q1/Q2 (pp.55/60), 444 Q1/Q2 (pp.36/38), 823 Q1/Q2 (pp.61/70), 1561 Q1/Q2 (pp.23/27)
  symptom:    appendix pages that carry the (*) interest line were labelled "פעילויות שלא במזומן" (non-cash), so the
              context-page caption said the page contains no financing cash flows and is shown for completeness only.
              The renderer also needs the exact string "פעילות שוטפת" / "פעילות השקעה" in context_sections to switch
              to the (*) wording.
  expected:   pages that hold a (*) line get the operating/investing wording.
  workaround: context_sections override per page (always including the exact "פעילות שוטפת").
  severity:   cosmetic

SCRIPT-ISSUE 3
  script:     finalize_report.py auto_geometry (hdr_strip of non-header pages) / fcf_render.py (*) crops
  report:     434 (pp.55/60), 444 (pp.36/38)
  symptom:    for an appendix page, the (*) crop's header strip covered only the page title, so the crop showed no
              column headers (periods) of the appendix table.
  expected:   the (*) crop shows the column headers of the table that holds the (*) line.
  workaround: boxes.header on the appendix page (title through column headers).
  severity:   cosmetic (legibility of periods in the (*) crop)

SCRIPT-ISSUE 4
  script:     finalize_report.py header_bottom() / fcf_extract.py units detection
  report:     2417 Q2 p.71; 823 Q1 (units only on p.59)
  symptom:    2417 Q2: the automatic header strip stopped above the units line ('אלפי ש"ח' printed level with the
              operating heading), so the zoom showed no units. 823 Q1: the units are printed only on the first statement
              page, and the zoom took its header from the financing page.
  expected:   the zoom header strip always includes the units line.
  workaround: 2417 Q2 boxes.header [55,33,560,125]; 823 Q1 "header_page": 59.
  severity:   cosmetic (R7.2 requires units in the zoom – fixed by override)
```

There is one further point, which is not a script issue. The `view` tool in this session failed to display images for about 70 minutes, returning only "maximum number of images". All visual verification was redone once images displayed, and the records cite only images actually seen.

## Final status

| issuer | status |
|---|---|
| 373 | verified + built (Q1, Q2) |
| 434 | verified + built (Q1, Q2) |
| 444 | verified + built (Q1, Q2) |
| 673 | verified + built (Q2; Q1 missing from the folder) |
| 823 | verified + built (Q1, Q2) |
| 1484 | verified + built (Q1, Q2); C2 differences come from the source and are explained |
| 1561 | verified + built (Q1, Q2) |
| 1724 | verified + built (Q1, Q2) |
| 2417 | verified + built (Q1, Q2); validate FAIL 1 = SCRIPT-ISSUE 1 (source C1 −1, explained) |
| 2441 | verified + built (Q1, Q2) |
| 2574 | verified + built (Q2; Q1 missing from the folder) |

20 / 20 reports are verified and 11 / 11 companies are built without `--draft`.

Assisted-by: Anthropic:Claude Opus 5.5
