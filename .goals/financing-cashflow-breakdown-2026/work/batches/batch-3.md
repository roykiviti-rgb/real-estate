# Batch 3 report — Phase B (financing cash-flow breakdown 2026)

Builder: Phase B batch 3. Issuers: 200 · 421 · 531 · 1039 · 1068 · 1974 · 2458 · 2486 · 2487 · 2567 (Q2 only) — 19 reports.
Protocol: `work\PIPELINE.md` (§0 loop, §3 checklist) + `work\phaseB-conventions.md`. Goal: `goal.md` + amendments 1–2
(T1/T2 apply, T3 cancelled). No git. Only my own overrides (`overrides\<iss>_Q1/Q2.json`, `<iss>_checks.json`), data
(through the scripts) and the two outputs per company (through `build_company.py`) were written.

**Result: all 19 reports verified, all 10 companies built without `--draft`; `checks.py` → unexplained mismatches 0;
`validate.py --issuers <iss> --no-master` → FAIL 0 for every issuer (all 10 together: PASS 3080 / FAIL 0).**

## 0. How the verification was done (and a process incident)

* For every report: `tool_review.py` (lines/values table, 220-DPI financing crop, (*) crops, statement pages), `tool_scan.py`
  where the statement pick was flagged, the text layer of every statement page dumped with word coordinates (own helper
  in `%TEMP%\fcf_run\200\b3tools`), and the rendered images.
* **Incident:** during the first pass (≈10:14–10:50) the `view` tool did not actually display images (it answered
  "maximum number of images reached"). All 19 reports were therefore **re-verified visually afterwards**: every financing
  line, value, column header, unit and (*) line was compared digit by digit with the rendered images actually viewed — the
  220-DPI zoom pages and full pages of the company screenshots PDFs (rendered with `tool_shots.py` / PyMuPDF composites),
  plus `tool_review` renders for 200. Every claim in notes (note references, appendix titles, restatement markers, printed
  page numbers, C2 explanations) was re-checked against the text layer; wrong or unsupported details were corrected
  (listed per company under "corrections after re-check"). **No value had to be changed by the re-check**; only notes.
  The `verified.method` text of every override now states exactly which images/pages were used.
* Zoom pages: when the header strip and the financing section are contiguous on one page (1974 Q1/Q2, 1039 Q2) the
  renderer draws one crop without the blue/orange frames (by design, `fcf_render.py` "contiguous"); the full-page image of
  those reports carries both frames — checked.

---------------------------------------------------------------------------------------------------------------

## 1. Per company

### 200 – לוינסקי עופר בע"מ
* **Sources:** Q1 `200_..._2026_Q1_1745686.pdf` (42 pp), statement PDF pp. 33–34 (printed 31–32), financing p. 34, header p. 34.
  Q2 `200_..._2026_Q2_1766476.pdf` (47 pp), pp. 36–37 (printed 34–35), financing p. 37. Earlier candidate blocks (Q1 pp. 24–25,
  Q2 pp. 25–28) are the forecast cash flow (תזרים מזומנים חזוי) in the board report — not used (tool_scan).
* **Columns:** Q1 3 (3M-2026, 3M-2025, FY-2025); Q2 5 (6M-26, 6M-25, 3M-26 (אפריל–יוני), 3M-25 (אפריל–יוני), FY-25). Units
  `אלפי ש"ח` (Q2 header: `אלפי ש"ח (למעט נתוני רווח למניה)`).
* **Mapping:** ST loans from banks and others, gross receipt and repayment lines → 5 (R3: all ST credit, gross or net);
  lease repayment → 10 (no principal/interest split); `תמורה ממימוש כתבי אופציה (סדרה 1)` → 2; `תמורה מהנפקת כתבי
  אופציה (סדרה 2)` (warrants issued on their own line) → 2; bonds issued → 3; `רכישת אגרות חוב` (buy-back of own bonds,
  Q2) → 8; `הנפקת הון מניות` / `הנפקת מניות` → 1.
* **(\*):** interest paid in operating (`מזומנים ששולמו והתקבלו במהלך התקופה עבור: ריבית ששולמה`) → info row, note
  `פעילות שוטפת`; interest received is not (*); no dividends.
* **Overrides:** full printed `header_text` for every column (the auto text missed day/month); Q2 `line_text` 4/8
  (text layer of the repaired font lost `(סדרה 1)` / `(סדרה 2)`); line notes; report notes; Q2 c3 column note.
* **Checks:** C1 0 everywhere; C2 OK (2026 and 2025); C3 OK (16). Info only: operating interest Q1-2026 (2,677) vs Q2-derived
  5,600 − 2,921 = 2,679 (2 difference in the reports) → Q2 c3 column note.
* **Text layer:** usable (repaired font) – labels compared with the image.
* **validate:** PASS 325 / FAIL 0.

### 421 – נתנאל גרופ בע"מ
* **Sources:** Q1 `421_..._2026_Q1_1745074.pdf` (55 pp), pp. 35–36 (printed 8–9), financing p. 36. Q2 `..._Q2_1764607.pdf`
  (69 pp), pp. 44–45 (printed 9–10), financing p. 45. 38D data at Q1 pp. 50–51 / Q2 pp. 64–65 not used.
* **Columns:** 3 / 5 as standard; c3 of Q2 (flagged ambiguous) confirmed on the image (3M to 30.06.2026). Units `אלפי ש"ח`.
* **Mapping:** `אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו` → 5; bonds → 3/8; `תמורה מהנפקת ניירות ערך` 45,000 and
  `עלויות הנפקת ניירות ערך` (1,068) → **1** (Phase A had `אחר`): exceptional private placement to Leumi Partners (note 5א,
  approved 6.1.2026) of 3,024,194 shares at 14.88 NIS (45 m NIS) with warrants series א–ג; shares + warrants not split →
  item 1 (convention 6), issue costs netted in 1 (R3). LT loans from bank and financial/other lenders → 4/7. Q2 `קבלת
  הלוואות לזמן ארוך מבעלי זכויות המיעוט` 10,548 → **4** (Phase A suggested 6) – a loan (non-current liability `הלוואות
  מבעלי מניות זכויות מיעוט` 12,100, Cyprus activity), not an equity contribution; R3 lists NCI holders among lenders of item 4.
  Lease → 10.
* **(\*):** `ריבית ועמלות ששולמו` in operating (`מזומנים שהתקבלו (ששולמו):`) → info row `פעילות שוטפת` (includes fees –
  noted). Dividend received (investing) is not (*); no dividends paid.
* **Restatement:** the pages carry `* הוצג מחדש...` (Q2 also `**`); the markers sit only on operating values of the 2025
  columns, column headers are unmarked and no financing value is marked → no `(מוצג מחדש)` flag (convention 10), column
  notes on Q1 c2 and Q2 c2/c4.
* **Checks:** C1/C2/C3 all OK. Info only: Q2 c4 note – operating interest Q1-2025 per Q2 (63,383 − 36,011 = 27,372) vs Q1
  report (28,202): 830.
* **Corrections after re-check:** note of the package line rewritten from the note text (exceptional private placement,
  approval date, total 45 m NIS, series ב/ג warrants classified as a financial liability).
* **validate:** PASS 327 / FAIL 0.

### 531 – בוני התיכון הנדסה אזרחית ותשתיות בע"מ (difficulty C)
* **Sources:** Q1 `531_..._2026_Q1_1744302.pdf` (51 pp), pp. 29–30 (printed 9–10), financing p. 30. Q2 `..._Q2_1766963.pdf`
  (58 pp), pp. 33–34 (printed 10–11), financing p. 34 (tool_scan: pp. 21–22 = board-report discussion, pp. 49–50 = 38D).
* **Columns:** 3 / 5; units `(אלפי ש"ח)` in the statement title. Q2 FY column has no audit label (as printed).
* **Source defect (convention 9):** Q2 p. 34, `הנפקת אגרות חוב (בניכוי הוצאות הנפקה)`, FY-2025 prints **`280,68`** (text
  layer and image). Recorded **280,683** = statement arithmetic (308,912 + 2,448 + 96,500 − 127,177) = Q1 report FY-2025.
  Documented in `line_values` + line note + `issues` + c5 column note. C1 = 0 after the correction, C3 OK.
* **Mapping:** lease → 10; bonds → 3/8; `קבלת (פירעון) אשראי מתאגידים בנקאיים, נטו` (Q2 `קבלת אשראי ... נטו`) → 5 (net,
  no term); `הנפקת אופציות` 1,301 → 2 (warrants of the Feb-2026 private placement of 635,240 shares + 317,620 warrants,
  presented on their own line); `הנפקת מניות` 18,552 → 1.
* **(\*):** interest paid in operating (`מזומנים ששולמו והתקבלו במהלך השנה עבור:`) → info row `פעילות שוטפת`.
* **Restatement:** `(*) יישום למפרע - שינוי מדיניות חשבונאית` markers only on operating values of 2025 columns → column notes,
  no flag.
* **Checks:** C1 OK; C3 OK; **C2 2026 total −1** (Q2: 101,757 − 59,545 = 42,212 vs Q1 42,211; entirely in the bank-credit line
  23,008 vs 23,007 – rounding in the reports) → `531_checks.json` (C2 total + C2-item 5). C2 2025 OK.
* **validate:** PASS 322 / FAIL 0.

### 1039 – אלביט נדל"ן בע"מ
* **Sources:** Q1 `1039_..._2026_Q1_1743815.pdf` (80 pp), pp. 49–51 (printed 9–11; p. 51 = appendix (א) newly consolidated
  company), financing p. 50. Q2 `..._Q2_1764263.pdf` (92 pp), pp. 54–55 (printed 11–12), financing p. 55.
* **Columns:** 3 / 5; units `אלפי ש"ח`.
* **Mapping:** bonds → 3; shares → 1; `שינוי בהלוואות לזמן קצר (כולל משיכת יתר)` → 5; LT loans from non-bank and other
  lenders → 4/7; `הזרמת הון זשמ"ש` → 6; `ריבית ששולמה במזומן` (in financing) → 13.
* **(\*):** interest paid only in financing; operating shows only taxes; investing interest received → info rows 0.
* **Empty cells:** Q2 lines `הנפקת מניות` and `קבלת הלוואה מתאגיד חוץ בנקאי לזמן ארוך` have blank (not `-`) cells in the
  2025/FY columns → 0, noted on the lines (confirmed on the image).
* **Checks:** all OK. **validate:** PASS 324 / FAIL 0.

### 1068 – שיכון ובינוי בע"מ (units מיליוני ש"ח)
* **Sources:** Q1 `1068_..._2026_Q1_1744574.pdf` (108 pp), pp. 45–46 (printed 9–10), financing p. 46. Q2 `..._Q2_1764659.pdf`
  (130 pp), pp. 58–59 (printed 11–12), financing p. 59.
* **Units:** printed `מליוני ש"ח` (kept verbatim; currency ש"ח, units מיליונים) – report note added.
* **Mapping:** `הנפקת מניות` → 1; **`הנפקת מניות מחברות מוחזקות` 232 → 6** (Phase A suggested 1): IPO of the subsidiary
  שיכון ובינוי אנרגיה (note 4 item 9: 62,662,900 shares + 31,331,450 warrants, ≈232 m NIS net; the company keeps ≈66.79%) –
  issuance of subsidiary shares to NCI without loss of control (R3 item 6). LT loans banks and others → 4/7; bonds → 3/8;
  **`תמורה (סילוק) מנגזרים, נטו` → אחר** (convention 7, derivatives); `שינוי באשראי לזמן קצר, נטו` → 5; interest → 13;
  NCI dividend → 12.
* **(\*):** interest and NCI dividends only in financing; no dividend to owners in the periods → info rows 0.
* **Restatement:** `(*) יישום למפרע, ראו באור 2.ד.` only on operating values of 2025 columns → column notes, no flag.
* **Checks:** all OK. **Corrections after re-check:** note reference fixed to `באור 4 סעיף 9`. **validate:** PASS 330 / FAIL 0.

### 1974 – סופרין אחזקות בע"מ
* **Sources:** Q1 `1974_..._2026_Q1_1742794.pdf` (107 pp), pp. 53–54 (printed 8–9), financing p. 54. Q2 `..._Q2_1764536.pdf`
  (118 pp), pp. 58–59 (printed 10–11), financing p. 59. Units `באלפי ש"ח` in the title.
* **Mapping:** `אשראי לזמן קצר, נטו` → 5; `קבלת/פירעון הלוואות מתאגידים פיננסים` → 4/7 (no term in the CF; gross lines next
  to a separate ST-credit line; board report: a long-term loan for income-producing assets); lease → 10; bonds (series ג
  2026, series ב expansions 2025) → 3, `פדיון אג"ח` → 8; `הנפקת כתבי אופציה` 1,626 → 2 (warrants series 1 issued in a
  package with bonds series ג, presented on their own line); `תשלום דיבידנד` → 11; `תמורה בגין הנפקת מניות, נטו` → 1.
* **Text fixes:** the text layer reads `יפרעון` (stray י) – `line_text` Q1 line 3, Q2 lines 3–4.
* **Printed as is:** Q2 3M-2026 receipt line `קבלת הלוואות מתאגידים פיננסים` prints **(46)** (6M 6,035 vs Q1 6,081) – kept, noted.
* **(\*):** interest paid in operating → info row `פעילות שוטפת`; dividends paid in financing (11).
* **Restatement:** Q2 `(*) סווג מחדש` markers located by word coordinates on c4 (3M-2025) operating/investing values →
  column note, no flag.
* **Checks:** all OK. **validate:** PASS 327 / FAIL 0.

### 2458 – מגידו י.ק. בע"מ
* **Sources:** Q1 `2458_..._2026_Q1_1743908.pdf` (65 pp), pp. 44–45 (printed 8–9), financing/header p. 45 (p. 44 headers print
  `ליום 31 במרס` – columns taken from p. 45, noted). Q2 `..._Q2_1767000.pdf` (68 pp), pp. 44–45, financing p. 45.
* **Mapping:** LT bank credit → 4/7; bonds → 3; **`תמורה מהנפקת מניות וכתבי אופציה, נטו` 178,450 (FY-2025) → 1** (Phase A
  suggested 2): IPO of shares + warrants, statement of changes in equity 154,440 + 24,010, not split in the CF (convention 6);
  ST bank credit net → 5; interest (in financing) → 13.
* **(\*):** interest only in financing; interest received in operating; dividend received in investing → info rows 0.
* **C2 2025 −191 (explained, `2458_checks.json` + column notes):** interest paid Q1-2025 (8,870) in Q1 vs Q2-derived
  22,148 − 13,469 = (8,679). The Q1 report shows `ריבית שהתקבלה` 191 in operating for Q1-2025, the Q2 report shows `-` for
  2025 and its operating Q1-2025 is lower by exactly 191 (investing and cash change equal) – consistent with interest received
  netted against interest paid in the Q2 report. Values as printed in each report. C2 2026 OK, C3 OK.
* **validate:** PASS 322 / FAIL 0.

### 2486 – מותג עירוני בע"מ
* **Sources:** Q1 `2486_..._2026_Q1_1744097.pdf` (45 pp), pp. 40–41 (printed 8–9), financing p. 41, **header_page set to 41**
  (the financing page has its own headers). Q2 `..._Q2_1766260.pdf` (50 pp), pp. 44–45 (printed 10–11), financing p. 45; c3
  (inferred by the extractor) confirmed on the image.
* **Mapping:** **`תקבולים מהנפקת מניות ואופציות, נטו` 24,744 → 1** (Phase A suggested 2): public offering at first listing
  (25.1.2026) of 5,120,000 shares + 1,920,000 warrants (series 1) + 1,280,000 warrants (series 2); equity statement: shares
  22,151 (51 + 22,100), warrants 2,593 (1,502 + 1,091); not split (convention 6). Gross loans from shareholders/related parties/
  investors and from `גופים פיננסים` (project finance) → **4/7** (see mapping decisions). Bonds → 3; interest → 13.
* **(\*):** interest only in financing (operating has only the non-cash adjustment; Q2 investing interest received) → 0.
* **C2 (explained, `2486_checks.json` + column notes):** 2026 total +80 – interest paid (61) in Q1 vs (141) Q2-derived; the Q2
  report adds `ריבית שהתקבלה` in investing (205 / 104), its Q1-2026 investing is higher by 79 and operating by 1, cash change
  identical (34,302). 2025 total +1,799 – shareholder/investor loans received 4,205 (Q1) vs 2,405 (Q2), financial bodies
  7,232 vs 7,231, interest (535) vs (533); the Q2 report's Q1-2025 investing is higher by 1,902 (associates line (1,903) in Q1,
  `-` in Q2) and operating lower by 103; cash change identical ((3,116)). C2-item rows (4, 13) explained. C3 OK.
* **Source irregularity outside financing:** Q2 p. 45 FY-2025 `עלייה (ירידה) במזומנים` prints 6,894, but operating + investing +
  financing = 7,342 (= Q1 report; 6,804 → 14,146) → `issues` + report note (no effect on recorded data).
* **Text layer:** Q1 usable (repaired font, labels compared with the image).
* **Corrections after re-check:** line-1 note (first pass wrongly said "private placement"); line-4 balance-sheet wording.
* **validate:** PASS 324 / FAIL 0.

### 2487 – אריה פרשקובסקי גרופ בע"מ
* **Sources:** Q1 `2487_..._2026_Q1_1744311.pdf` (52 pp), pp. 32–33 (printed 6–7), financing p. 32; p. 33 = appendices א
  (additional information), ב (non-cash), ג (newly consolidated company). Q2 `..._Q2_1766830.pdf` (57 pp), pp. 35–36 (printed
  7–8), financing p. 35, appendices on p. 36.
* **Mapping:** ST credit banks and others net → 5; LT loans banks and others → 4/7; bonds → 3; Q2 `תמורה מאגרות חוב ניתנות
  להמרה` 17,272 → 3 (convertibles); `שינוי בהלוואות לבעלי שליטה` (net, no term) → 5; lease → 10.
* **(\*) – extractor miss:** interest paid is disclosed **only** in `נספח א - מידע נוסף על תזרימי המזומנים` (`מזומנים ששולמו
  במהלך התקופה – ריבית`): Q1 5,936 / 4,639 / 22,717; Q2 13,533 / 10,187 / 7,597 / 5,548 / 22,717 (printed without
  parentheses – sign kept as printed). The extractor found nothing (info note would have been `לא מוצג בנפרד`); added with
  `outside_add` + bbox from word coordinates; note per convention §1: `גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא
  בפעילות מימון)`. Red crops checked. (*) C2 consistent (13,533 − 7,597 = 5,936; 10,187 − 5,548 = 4,639).
* **Checks:** all OK. **validate:** PASS 323 / FAIL 0.

### 2567 – רם מוגרבי ארדיטי בע"מ (Q2 only – Q1 not in the folder)
* **Source:** `2567_..._2026_Q2_1767289.pdf` (69 pp), pp. 53–55 (printed 8–10), financing p. 54; p. 55 = non-cash activities.
  38D at pp. 64–65 not used. Text layer: repaired font (`ª` = נ), labels compared with the image.
* **Columns:** 5; units `אלפי ש"ח`. Workbook states `דוח Q1 2026 אינו קיים בתיקייה`.
* **Mapping:** **`ריבית ששולמה על שטרי הון` → 11** (Phase A suggested 13): the shareholders' capital notes were equity (column
  `שטר הון` in the statements of changes in equity, reclassified to ST shareholder loans in 2025), and the payment is charged
  to retained earnings in the equity statements (pp. 51–52) – a distribution on an equity instrument, not interest expense
  (alternative 13 by wording – mapping decision). LT loans from shareholders → 4/7; `פרעון הלוואות לזמן קצר מבעלי מניות`
  (47,394; the ST owner loans converted from capital notes, repaid 30.3.2026) → 5; **`קבלת הלוואות מחברות כלולות, צדדים
  קשורים ואחרים` → 5** (no term; no non-current liability for them – the ST loans balance moves exactly by the separate ST-loan
  line, so these are current balances; convention 5); **`פרעון התחייבות בגין נכסי זכות שימוש` → 10** (Phase A suggested 7 –
  it is the lease liability); `קבלת הלוואות לזמן קצר` → 5; interest → 13; bonds (series א) → 3.
* **(\*):** interest paid in financing; operating has only the non-cash adjustment; investing interest received → 0.
* **Source irregularity:** the board report's cash-flow table (p. 14) differs from the statement: financing 73,519 / 64,761 vs
  76,050 / 67,292 (2,531), investing (77,420) / (63,137) vs (79,952) / (65,669) (2,532) for the 2026 periods; ±1 elsewhere →
  `issues` (data taken from the statement).
* **Checks:** C1 OK (5); C2/C3 not applicable. **validate:** PASS 210 / FAIL 0.

---------------------------------------------------------------------------------------------------------------

## 2. Mapping decisions (cross-company – for Phase C alignment)

| # | case (issuer) | decision | reasoning / alternative |
|---|---|---|---|
| M1 | LT loans received from NCI holders in a subsidiary (421 Q2 `קבלת הלוואות לזמן ארוך מבעלי זכויות המיעוט`) | **4** | a loan (non-current liability), not equity; R3 item 4 names partners/NCI holders. Alternative 6 rejected. |
| M2 | IPO of a consolidated subsidiary, control kept (1068 `הנפקת מניות מחברות מוחזקות`) | **6** | R3 item 6 "issuance of subsidiary shares to NCI". Extractor suggested 1. |
| M3 | Interest paid on shareholders' capital notes classified as equity (2567 `ריבית ששולמה על שטרי הון`) | **11** | charged to retained earnings in the equity statement → distribution to owners. **Alternative 13** by wording – please align with any other `שטרי הון` interest case. |
| M4 | Loans from associates/related parties/others, receipt line, no term, no non-current liability (2567) | **5** | ST/current balances (convention 5). |
| M5 | Gross loan lines without a stated term – project finance from `גופים פיננסים` and owner/investor loans repaid at project completion, classified mostly as current liabilities by operating cycle (2486); `הלוואות מתאגידים פיננסים` next to a separate ST-credit line (1974) | **4 / 7** | R3 item 4 "incl. long-term project/land finance"; gross, not net. **Alternative 5** (current-liability classification) – align with other batches' treatment of ליווי loans without a stated term. |
| M6 | Shares + warrants in one CF line (421 private package + its issue costs; 2458 IPO; 2486 IPO) | **1** | convention 6. Extractor suggested 2 or אחר. |
| M7 | Warrants/options issued presented on their own line (200 `תמורה מהנפקת כתבי אופציה (סדרה 2)`, 531 `הנפקת אופציות`, 1974 `הנפקת כתבי אופציה`) | **2** | R3 item 2 "proceeds of warrants presented on their own line". |
| M8 | Buy-back of own bonds (200 `רכישת אגרות חוב`) | **8** | R3 item 8. |
| M9 | Interest paid disclosed only in a CF appendix, section not stated (2487) | info row, note `גילוי בנספח ... – הסעיף לא צוין (לא בפעילות מימון)` | convention §1; values positive as printed. |
| M10 | Restatement markers only on operating/investing values of comparative columns (421, 531, 1068, 1974) | no `(מוצג מחדש)`, column note | convention 10. |
| M11 | `ריבית ועמלות ששולמו` in operating (421) | (*) interest info row, fees noted | the only interest-paid line. |

Extractor suggestions corrected in this batch (for Phase C's statistics): 421 lines 4–5 (אחר → 1), 421 Q2 line 8 (6 → 4), 1068
line 2 (1 → 6), 2458 line 3 (2 → 1), 2486 line 1 (2 → 1), 2567 line 1 (13 → 11), line 5 (4 → 5), line 6 (7 → 10).

## 3. Source issues (all documented in the overrides)

* 531 Q2 p. 34: FY bond issuance printed `280,68` → 280,683 (issues, notes).
* 2486 Q2 p. 45: FY-2025 cash change printed 6,894 instead of 7,342 (outside financing; issues).
* 2567 Q2 p. 14: board-report CF table differs from the statement by 2,531/2,532 for 2026 (issues).
* 1974 Q2: negative amount (46) on a receipt line in 3M-2026 (kept as printed, noted).
* Reporting differences between Q1 and Q2 explained in `_checks.json`: 531 (−1 rounding), 2458 (191 interest netting),
  2486 (80 interest gross-up; 1,799 2025 comparatives).
* Info-only (*) differences between reports (column notes): 200 (2), 421 (830).

## 4. SCRIPT-ISSUEs

```
SCRIPT-ISSUE 1
  script:     fcf_extract.py (extract_report.py 2487)
  report:     2487 Q1, 2487 Q2
  symptom:    interest paid disclosed only in the statement appendix 'נספח א - מידע נוסף על תזרימי המזומנים'
              (heading 'מזומנים ששולמו במהלך התקופה', sub-line 'ריבית'; Q1 p.33, Q2 p.36) was not offered as a (*)
              candidate; the info row defaulted to 'לא מוצג בנפרד בדוח תזרים המזומנים'.
  expected:   appendix-only interest paid proposed as a (*) line (as for 1724, 2384 …).
  workaround: outside_add with values and bbox from the word coordinates; info_notes per convention §1.
  severity:   data completeness of the (*) info rows (silent if not reviewed) – no effect on items/totals.

SCRIPT-ISSUE 2
  script:     fcf_extract.py (column header text)
  report:     most of my reports (e.g. 200, 531, 1039, 2567: 'ל-3 חודשים שהסתיימו 2026')
  symptom:    columns[].header_text often lacks the day/month or mixes neighbouring columns; it is printed verbatim
              in the workbook row 'כותרת העמודה בדוח (מילולית)'.
  expected:   the full printed header of each column.
  workaround: columns.cN.header_text set from the image for every column of all 19 reports.
  severity:   cosmetic.

SCRIPT-ISSUE 3
  script:     fcf_lib.fix_glyph_text / label assembly
  report:     200 Q2 (labels 'תמורה ממימוש כתבי אופציה)סדרה' – lost '1)'), 1974 Q1/Q2 ('יפרעון', stray 'י')
  symptom:    label text differs from the printed label.
  workaround: line_text.
  severity:   cosmetic.
```

Environment note (not a script issue): the `view` tool silently stopped displaying images for the first ≈40 minutes (see §0);
all verification was redone after images displayed again.

## 5. Temp hygiene

My helper scripts and renders lived in `%TEMP%\fcf_run\<iss>\` (helpers in `%TEMP%\fcf_run\200\b3tools\`); all ten issuer
folders are deleted at the end of the batch (`_runs` left for Phase C). Nothing was written into WORKSPACE except the two
outputs per company (via `build_company.py`) and my overrides / data / batch files under `.goals`.

## 6. Final status

| issuer | company | reports | status |
|---|---|---|---|
| 200 | לוינסקי עופר | Q1, Q2 | verified + built (validate FAIL 0) |
| 421 | נתנאל גרופ | Q1, Q2 | verified + built (validate FAIL 0) |
| 531 | בוני התיכון | Q1, Q2 | verified + built (validate FAIL 0) – source digit defect handled |
| 1039 | אלביט נדל"ן | Q1, Q2 | verified + built (validate FAIL 0) |
| 1068 | שיכון ובינוי | Q1, Q2 | verified + built (validate FAIL 0) – מיליוני ש"ח |
| 1974 | סופרין אחזקות | Q1, Q2 | verified + built (validate FAIL 0) |
| 2458 | מגידו י.ק. | Q1, Q2 | verified + built (validate FAIL 0) – C2 191 explained |
| 2486 | מותג עירוני | Q1, Q2 | verified + built (validate FAIL 0) – C2 80 / 1,799 explained |
| 2487 | אריה פרשקובסקי גרופ | Q1, Q2 | verified + built (validate FAIL 0) – appendix (*) added |
| 2567 | רם מוגרבי ארדיטי | Q2 only | verified + built (validate FAIL 0) |

19 / 19 reports verified, 10 / 10 companies built; no blocked issuer.

Assisted-by: Anthropic:Claude Opus 5.5
