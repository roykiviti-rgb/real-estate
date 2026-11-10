# Goal: Financing cash-flow breakdown (14 items) for every Q1/Q2 2026 report — real estate & construction, cycle 2

## User Request

Verbatim:

```
תעבור על כל הדוחות הכספיים בתיקייה, ולכל דוח כספי תוסיף לי פירוט מדויק של:

**התקבלויות (+)**

1. הנפקת מניות, בניכוי עלויות הנפקה
2. מימוש אופציות / כתבי אופציה
3. הנפקת אגרות חוב (כולל אג"ח להמרה)
4. קבלת הלוואות לזמן ארוך
5. אשראי לזמן קצר מתאגידים בנקאיים, נטו
6. השקעת בעלי זכויות שאינן מקנות שליטה בחברה בת

**תשלומים (−)**

7. פירעון הלוואות לזמן ארוך
8. פירעון אגרות חוב
9. רכישה עצמית של מניות
10. פירעון קרן התחייבויות בגין חכירה
11. דיבידנד ששולם לבעלי המניות (*)
12. דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה
13. ריבית ששולמה (*)
14. רכישת זכויות נוספות בחברה בת ללא שינוי בשליטה

**= סך תזרים מזומנים מפעילות מימון**

(*) סעיף שניתן לסווג גם כפעילות שוטפת, לפי מדיניות החברה.

לכל חברה.

תעבור בצורה יסודית לבדוק שאין טעויות, לכל קובץ עם נתונים תוסיף קובץ נפרד עם צילומי מסך של הנתונים מהדוחות.

use goal skill with opus 5.5
```

English: "Go over all the financial reports in the folder and, for each financial report, add a
precise breakdown of [the 14 items above] = total cash flow from financing activities.
(*) = an item that may also be classified as operating activity, per company policy. For each
company. Check thoroughly that there are no mistakes; for each file with data, add a separate
file with screenshots of the data from the reports."

Interview decisions (user-confirmed):

- **Q1 – Periods:** extract **ALL columns** of each cash-flow statement, including the 2025
  comparatives and full-year 2025 (typically Q1 report: 3M-2026, 3M-2025, FY-2025;
  Q2 report: 6M-2026, 6M-2025, 3M(Apr–Jun)-2026, 3M(Apr–Jun)-2025, FY-2025).
- **Q2 – Output layout:** per company folder: one Excel with the breakdown for all of that
  company's reports + a separate PDF with the screenshots; plus one master Excel in the
  WORKSPACE root with all companies.
- **Q3 – Lines that don't fit the 14 items:** map each original line to the closest item by
  economic nature (e.g., short-term credit from banks AND others, net → item 5; long-term loans
  from related parties → items 4/7); document every original line → item mapping; lines that fit
  no item go to an extra **"אחר" (Other)** row with the original text, so the items always sum
  to the reported total.
- **Q4 – (\*) items:** record only what appears in the financing section (so the total equals
  the reported financing total). When interest/dividends paid are classified outside financing
  (operating, or investing), items 11/13 stay 0 for that portion and a note shows the amount and
  where it was classified.
- **Q5 – Which statements:** only the reporting company's **consolidated** cash-flow statement.
  An extra attachment file is used only when it IS the company's main report (e.g., 1829 where
  the main PDF is just an appraiser letter; 2559 Q1 amended report). Document what every extra
  file is. Separate/solo (Reg. 38D) statements and investee statements are NOT extracted.
- **Q6 – Units/sign:** amounts exactly as reported (original currency and units, e.g. NIS
  thousands / USD thousands — no conversion); receipts positive, payments negative; currency and
  unit columns.
- **Q7 – Screenshots PDF:** for each report: the cash-flow page(s) with the financing section
  highlighted, plus a zoomed crop of the financing section including the column headers (periods)
  and units; every image captioned with source file + page number; also the operating/investing
  section lines for interest/dividends when they are classified there.
- **Q8 – Process tracking:** **no git**. Process files go in the hidden `.goals` folder inside the
  WORKSPACE. Do not run `git init`, do not commit.
- **Q9 – Excel layout:** company Excel: rows = items 1–14 + "אחר" + reported total + check row
  (difference = 0); columns = every report×period; extra sheet listing every original line →
  item mapping. Master Excel: one row per company×report×period with all items, plus mapping and
  file-index sheets. Hebrew labels, right-to-left sheets. FY2025 and 2025 comparatives appear in
  both Q1 and Q2 reports — record each as reported and flag any differences (restatements).

## Refined Goal

WORKSPACE = `C:\Users\רואי\OneDrive - huji.ac.il\שולחן העבודה\agent folder\פרק ד'\דוחות כספיים\בדיקה רון\נדל_ן ובינוי - מחזור 2`

The WORKSPACE holds 86 company folders (`<TASE issuer number> - <company name>`; `"` was
replaced by `_` in folder/file names) with 178 PDFs in total: 162 company×quarter quarterly
reports for the periods ended 31.03.2026 (Q1) and 30.06.2026 (Q2), plus 16 extra attachment
files (`..._<reportId>-01.pdf`, `-02.pdf`). Ten companies have no Q1 report in the folder.

For **every** one of the 162 company×quarter reports, locate the reporting company's
**consolidated statement of cash flows** (דוח תמציתי מאוחד על תזרימי המזומנים), and for **every
period column** it presents, extract the financing-activities section, classify every original
line into the user's 14 items (or "אחר"), and record the reported total. Deliver, per company, an
Excel workbook with the breakdown and a separate PDF of screenshots proving every number, plus one
master Excel for all companies. Every number must exactly match the source PDF, every period
must reconcile (items sum to the reported total), and all classification decisions must be
documented so the user can audit them.

## Normative Definitions & Rules

### R1 — Source selection

1. For each company×quarter, exactly one PDF is the **data source**: the file containing the
   company's own condensed consolidated interim financial statements for that period. Normally
   this is the main file `<issuer>_<name>_2026_Q<n>_<reportId>.pdf`. Known exceptions (verify):
   - **1829 (both quarters):** the main PDF is a 1-page appraiser letter; the report is the `-01` file.
   - **2559 Q1:** the main PDF is a 3-page excerpt (restatement note); `-01` (51 pp) and `-02`
     (54 pp) are both titled "דוח מתקן" to the 31.03.2026 statements. Determine which one is
     the complete/authoritative version, use it, state why, and state whether the financing
     section differs between the two (if it differs, flag it in the issues sheet).
   - **2520 (both quarters):** `-01` = condensed consolidated statements of the investee
     "סלע איסתא נדל"ן ישראלי בע"מ" → NOT a data source (out of scope).
   - All other `-01` files are appraisals / valuation opinions → NOT data sources.
2. Inside the source PDF use the **consolidated** cash-flow statement — NOT the separate/solo
   financial information (מידע כספי נפרד / נתונים כספיים המיוחסים לחברה עצמה, Reg. 38D), NOT the
   board-of-directors report discussion, NOT an investee's statements. If a company presents no
   consolidated statements (no subsidiaries), use its primary statement of cash flows and note it.
3. The cash-flow statement may span several pages (operating on one page, investing/financing on
   the next; 3-month columns sometimes on separate pages). All relevant pages must be used.

### R2 — Periods (columns)

1. Every column presented in the consolidated cash-flow statement of each used report is a
   **period** to extract — none may be skipped, none invented.
2. Period label format (Hebrew): `3 חודשים שהסתיימו ב-31.03.2026`,
   `6 חודשים שהסתיימו ב-30.06.2026`, `שנה שהסתיימה ב-31.12.2025`, etc. Append ` (מוצג מחדש)`
   when the report labels the column restated/amended. Record also: number of months (3/6/12)
   and period-end date.
3. In the company workbook, a column header = `דוח Q1 2026 | <period label>` or
   `דוח Q2 2026 | <period label>`; Q1-report columns first (in the statement's order), then
   Q2-report columns (in the statement's order).
4. Missing Q1 reports (no Q1 file in the folder): 111, 584, 673, 1331, 1703, 1969, 2557, 2567,
   2570, 2574. Their company workbooks state at the top of the main sheet
   `דוח Q1 2026 אינו קיים בתיקייה`, and the master issues sheet lists them. Do not fetch reports
   from the internet.

### R3 — Items and line-mapping rules

Item labels in all outputs must be exactly these Hebrew strings (in this order), under the group
headers `התקבלויות (+)` and `תשלומים (−)`:

| # | Exact label | Map here (closest economic nature; examples) |
|---|---|---|
| 1 | הנפקת מניות, בניכוי עלויות הנפקה | issuance of the reporting entity's shares/units (public, private, rights issue); receipts on account of shares; equity contributions to the reporting entity (incl. capital of partners in a reporting partnership); share-issuance costs paid (negative, netted here) |
| 2 | מימוש אופציות / כתבי אופציה | exercise of employee options / warrants; proceeds of warrants presented on their own line |
| 3 | הנפקת אגרות חוב (כולל אג"ח להמרה) | issuance of bonds of any series incl. series expansions and convertibles, net of issuance costs; issuance of commercial paper (נע"מ) — mention "נע"מ" in the mapping note |
| 4 | קבלת הלוואות לזמן ארוך | receipt of long-term loans from any lender (banks, institutions, controlling shareholder, related parties, partners/NCI holders, others), incl. long-term project/land finance; loan-raising costs (negative, netted here) |
| 5 | אשראי לזמן קצר מתאגידים בנקאיים, נטו | short-term credit/loans from banks **and** other lenders, whether presented net or as separate gross receipt/repayment lines (all summed here); any borrowing line presented **net** with no stated term |
| 6 | השקעת בעלי זכויות שאינן מקנות שליטה בחברה בת | NCI capital contributions to subsidiaries/consolidated partnerships; issuance of subsidiary shares to NCI; proceeds from selling subsidiary shares without loss of control |
| 7 | פירעון הלוואות לזמן ארוך | scheduled/early repayment of long-term loans to any lender |
| 8 | פירעון אגרות חוב | bond repayment/redemption, early redemption, buy-back of own bonds; repayment of commercial paper (note "נע"מ") |
| 9 | רכישה עצמית של מניות | purchase of treasury shares (incl. a subsidiary buying the parent's shares) |
| 10 | פירעון קרן התחייבויות בגין חכירה | lease-liability repayments (if a line mixes principal + interest without a split, put it here and note it) |
| 11 | דיבידנד ששולם לבעלי המניות (*) | dividends paid to owners of the parent; distributions to unit-holders/partners of the reporting entity — financing-section amounts only |
| 12 | דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה | dividends / distributions / withdrawals paid to NCI |
| 13 | ריבית ששולמה (*) | interest paid presented in the financing section (incl. separately presented lease interest) — financing-section amounts only |
| 14 | רכישת זכויות נוספות בחברה בת ללא שינוי בשליטה | purchase of NCI / additional shares in an already-controlled subsidiary |
| — | אחר | ONLY lines that fit none of 1–14 (e.g., restricted deposits/collateral movements, derivative/hedge settlements, government grants, contingent-consideration payments, discontinued-operations financing flows) — always with the verbatim original text |
| = | סך תזרים מזומנים מפעילות מימון | the statement's own reported financing total line, as reported |

Additional mapping rules:

- A line that **nets receipts and repayments of the same long-term instrument** (e.g., "קבלת
  (פירעון) הלוואות לזמן ארוך, נטו") goes, per period column, to the receipt item (4 loans /
  3 bonds) if the net amount is positive and to the repayment item (7 / 8) if negative; document.
- Subtotals inside the financing section are not items (mark them "סיכום ביניים – לא נכלל");
  nothing may be counted twice.
- Every original line × period value is assigned to exactly one item; an item's value = the sum
  of the original line values assigned to it. **No plug values** — "אחר" is never a balancing
  figure.
- Judgment calls must be consistent across all companies; every non-obvious assignment carries a
  short reasoning note in the mapping sheet (Hebrew or English).

### R4 — Values, sign, units, currency

- Values are copied **exactly** as printed (same digits, same units — no rounding, scaling or
  conversion). Payments shown in parentheses → negative numbers; receipts → positive.
  A dash / blank in the source → 0. Items with no line in a period → 0.
- Record per report the **currency** (e.g., ש"ח, דולר ארה"ב, אירו, זלוטי פולני, דולר קנדי) and
  **units** (e.g., אלפים, מיליונים) exactly as stated in the statement header.
- Amounts are stored as numeric Excel cells (not text) with a thousands-separator number format.

### R5 — (\*) items classified outside financing

- Items 11 and 13 contain only amounts presented in the financing section.
- Two **info rows** (not part of the sum) appear under the check row:
  `(*) ריבית ששולמה שסווגה מחוץ לפעילות מימון (לידיעה בלבד)` and
  `(*) דיבידנד ששולם שסווג מחוץ לפעילות מימון (לידיעה בלבד)` — amount per period as printed
  (sign as printed) and a note naming the section (`פעילות שוטפת` / `פעילות השקעה`). If interest
  or dividends paid are not presented as a separate line anywhere in the statement, the note says
  `לא מוצג בנפרד בדוח תזרים המזומנים`; if none were paid/presented, leave 0 with no note.

### R6 — Company workbook (one per company folder)

File: `<company folder>\<issuer> - פירוט תזרים מימון 2026.xlsx` (e.g., `1039 - פירוט תזרים מימון 2026.xlsx`).
All sheets right-to-left; Hebrew labels.

1. Sheet **`פירוט מימון`**:
   - Header block: company name (folder name with `_` restored to `"`, e.g. `אלביט נדל"ן בע"מ`),
     issuer number, currency, units, and (if applicable) `דוח Q1 2026 אינו קיים בתיקייה`.
   - Table: rows in this order — group header `התקבלויות (+)`, items 1–6, group header
     `תשלומים (−)`, items 7–14, `אחר`, `= סך תזרים מזומנים מפעילות מימון` (reported),
     `בדיקה: סכום הסעיפים פחות הסה"כ המדווח` (may be a live formula; must equal 0), the two (\*)
     info rows (R5), and a notes row. Columns = every report×period (R2.3).
   - Under the column headers (or in rows above the table): source file name and PDF page
     number(s) for each column.
2. Sheet **`מיפוי שורות`**: one block per report (rows = original financing-section lines in the
   statement's order, incl. subtotal/total lines and the (\*) lines from other sections marked
   `לידיעה – מחוץ לפעילות מימון`); columns: verbatim original line text, assigned item number,
   item label, reasoning note, then one value column per period of that report.
3. Sheet **`מקורות`**: every PDF in the company folder — file name, quarter, report ID, page
   count, role (`מקור הנתונים – דוח רבעוני`, `גרסה חלופית – לא בשימוש`, `נספח – שומה/הערכת שווי`,
   `נספח – דוחות כספיים של חברה מוחזקת`, `מכתב נלווה/תמצית`, or a similarly precise Hebrew
   description), used yes/no, and the PDF page numbers of the consolidated cash-flow statement and
   of the financing section for used files.

### R7 — Screenshots PDF (one per company folder)

File: `<company folder>\<issuer> - צילומי מסך תזרים מימון 2026.pdf`. For each used report
(Q1 then Q2):

1. Rendered image(s) (raster, ≥ 110 DPI) of every consolidated cash-flow page that contains
   financing-section lines (and the page carrying the column headers if different), with the
   financing section **highlighted** (colored box/overlay drawn on the rendered image or a
   temporary copy — never on the source PDF).
2. A **zoomed crop** (≥ 200 DPI) of the financing section **including the column-header strip
   (period titles) and the units/currency line** — a composite of header strip + section is fine
   when they are far apart or on different pages.
3. When interest/dividends paid are classified outside financing: a crop of those lines,
   highlighted.
4. Every image has a caption: company, report (Q1/Q2 2026), source file name, PDF page number
   (1-based physical page in the file), and what is shown. Digits must be legible.
5. The screenshots show exactly the files/pages cited in the company workbook.

The master workbook does not need its own screenshots file; each master data row points to the
company's screenshots PDF.

### R8 — Master workbook

File: `WORKSPACE\סיכום פירוט תזרים מימון 2026 - כל החברות.xlsx`; all sheets RTL:

1. **`נתונים`** — one row per company×report×period: issuer number, company name, company folder,
   report (`Q1 2026`/`Q2 2026`), source file, PDF pages, period label, months, period-end date,
   currency, units, items 1–14, `אחר`, reported total, check difference, the two (\*) info amounts
   + their classification notes, restated flag, notes, relative path of the company screenshots
   PDF. Row count = total number of period columns across all company workbooks; every value
   identical to the company workbook.
2. **`מיפוי שורות`** — long format: one row per company × report × original line × period, with
   verbatim text, value, assigned item, reasoning note, source file, page.
3. **`אינדקס קבצים`** — all 178 PDFs: relative path, company, quarter, report ID, pages, role,
   used yes/no, consolidated cash-flow pages (if used).
4. **`חסרים והערות`** — missing reports, special source decisions (1829, 2559, 2520), every
   consistency-check mismatch (R9) with its explanation, every non-zero check, every source
   irregularity.
5. **`הסבר`** — short legend: item definitions/mapping rules (R3), sign/units convention, (\*)
   treatment, column meanings.

### R9 — Mandatory consistency checks (all must be run and their results reported)

- **C1** every report×period: sum(items 1–14 + אחר) − reported total = 0.
- **C2** companies with both reports: Q1 report's 3M-2026 total = Q2 report's 6M-2026 total −
  Q2 report's 3M(Apr–Jun)-2026 total; same for the 2025 comparatives (when the Q2 report presents
  3-month columns).
- **C3** companies with both reports: FY-2025 column of Q1 report = FY-2025 column of Q2 report,
  for the total and each item.
- Any mismatch must be investigated: extraction errors are fixed; genuine differences
  (restatement, reclassification, source rounding) are listed with an explanation in
  `חסרים והערות` and in the builder report. No unexplained mismatch may remain.

## Acceptance Criteria

- [ ] **AC1 – Source inventory & selection:** the master `אינדקס קבצים` sheet lists all 178 PDFs
  with a correct role; for each of the 162 company×quarter reports exactly one file is marked
  used and it is the file holding that company's consolidated interim statements for that period
  (R1), including correct handling of 1829, 2559 Q1 and 2520; each company's `מקורות` sheet
  matches its folder.
- [ ] **AC2 – Files present, exact names:** each of the 86 company folders contains exactly two
  new files — `<issuer> - פירוט תזרים מימון 2026.xlsx` and
  `<issuer> - צילומי מסך תזרים מימון 2026.pdf` — and the WORKSPACE root contains the master
  workbook `סיכום פירוט תזרים מימון 2026 - כל החברות.xlsx`. All .xlsx files are valid and open in
  Excel without repair prompts.
- [ ] **AC3 – All periods captured:** for every used report, the number and identity of extracted
  periods equals the columns of its consolidated cash-flow statement (R2), with correct labels,
  months and end dates; restated columns flagged; missing Q1 reports stated (R2.4).
- [ ] **AC4 – Exact values:** every item value, `אחר`, reported total and (\*) info value equals the
  source PDF exactly (digits, sign, units); currency and units correct for every report.
- [ ] **AC5 – Complete, plug-free mapping:** every original financing-section line of every used
  report appears (verbatim) for every period in both mapping sheets, assigned to exactly one item
  per R3 with reasoning for non-obvious calls; each item equals the sum of its assigned lines;
  nothing omitted or double-counted; `אחר` holds only lines that fit no item; assignments are
  consistent across companies.
- [ ] **AC6 – Reconciliation (C1):** the check is 0 for every report×period; a non-zero value is
  allowed only when the source statement itself does not add up, and then it is documented.
- [ ] **AC7 – (\*) treatment:** items 11/13 contain financing-section amounts only; the info rows
  show the outside-financing amounts and their section for every period where applicable (R5).
- [ ] **AC8 – Cross-report checks (C2, C3):** performed for all eligible companies; every mismatch
  is either fixed (extraction error) or explained in `חסרים והערות` and the builder report.
- [ ] **AC9 – Company workbook layout:** sheets, row order, exact item labels, header block,
  column headers, source/page references, notes, RTL and numeric cells as specified in R6.
- [ ] **AC10 – Screenshots PDFs:** for every used report the PDF contains the highlighted page
  image(s), the zoomed crop with column headers and units, and (when applicable) the (\*) crops,
  all captioned and legible, matching the files/pages cited in the workbook (R7).
- [ ] **AC11 – Master workbook:** the five sheets of R8; `נתונים` has exactly one row per
  company×report×period and its values equal the company workbooks; RTL; numeric cells.
- [ ] **AC12 – Integrity & hygiene:** every pre-existing file is byte-identical to
  `.goals/financing-cashflow-breakdown-2026/baseline_files_sha256.csv` (nothing modified, deleted,
  renamed or moved); the only new items in WORKSPACE are the 2×86 company files, the master
  workbook and the hidden `.goals` folder (no temp files, renders, Excel lock files `~$*`,
  `__pycache__`, logs); no `.git` anywhere.
- [ ] **AC13 – Self-validation & report:** `.goals/financing-cashflow-breakdown-2026/work/validate.py`
  runs with `python <path>` from any directory, re-checks AC2, AC3 counts, AC5 sums, C1–C3,
  master-vs-company equality and the baseline hashes, prints a summary and exits 0 only when all
  pass. `builder-report-<N>.md` documents per company×quarter: source file and pages, periods,
  currency/units, judgment calls, (\*) classification, flags, and how every number was verified
  (automated text extraction cross-checked against rendered images; visual reading for pages
  without a usable text layer).

## Scope Boundaries

**In scope:**
- All 86 company folders / 162 company×quarter reports / 178 PDFs in WORKSPACE.
- The consolidated cash-flow statement of each report: all period columns, the full financing
  section, and the interest/dividends-paid lines located in other sections (info rows only).
- Per-company Excel + screenshots PDF, the master Excel, and process files under
  `.goals/financing-cashflow-breakdown-2026/`.

**Out of scope:**
- Separate/solo (Reg. 38D) cash-flow statements; investee statements (e.g., 2520 `-01`); the
  content of appraisal/valuation attachments; figures from the board-of-directors report.
- Currency conversion or any re-scaling; operating/investing sections other than the (\*) lines.
- Fetching missing reports from Maya / the internet.
- Modifying, renaming, moving or deleting any source PDF; anything outside WORKSPACE (parent
  folders, other cycles, the four company folders two levels up).
- git (no `git init`, no commits).

## Applicable Project Conventions

**Quality gate command:**
- `python "<WORKSPACE>\.goals\financing-cashflow-breakdown-2026\work\validate.py"` (written by the
  Builder; must exit 0). The Inspector also verifies values independently against the PDFs — the
  script alone is not sufficient evidence.

**Commit convention:**
- None — folder is not a git repository and the user chose **no git**. Instead of commits:
  Builder writes `.goals/financing-cashflow-breakdown-2026/builder-report-<N>.md` each iteration;
  Inspector writes `inspector-feedback-<N>.md` and appends the verdict to `status.json` history.
- End each report with `Assisted-by: Anthropic:Claude Opus 5.5`.

**Guidelines / environment facts (from orchestrator discovery — verify yourself):**
- Python 3.12 with PyMuPDF (`import pymupdf`, v1.28), openpyxl 3.1.5, python-docx are installed;
  pdfplumber and Tesseract/OCR are not (pip install is allowed if needed). Pages without a usable
  text layer must be read visually from rendered images.
- Hebrew text passed through PowerShell pipes gets mangled — write UTF-8 `.py` files and run them;
  set `PYTHONIOENCODING=utf-8`.
- WORKSPACE is OneDrive-synced: keep scripts and small intermediate data (JSON/CSV) in
  `.goals/financing-cashflow-breakdown-2026/work/`; put bulky renders outside WORKSPACE
  (e.g. `%TEMP%`) and clean them up.
- PyMuPDF text search for "פעילות מימון" finds hits in most reports but **none** in: 1083 Q1 & Q2,
  1331 Q2, 1644 Q1, 1905 Q1 & Q2, 341 Q1 (and in the appraisal attachments) — these likely need
  visual reading or other wording ("פעילויות מימון", "לפעילות מימון", etc.).
- Each report mentions financing in several places (board report, consolidated statement, solo
  statement) — make sure the consolidated statement is used.
- Read-only references in the parent folder: `..\_extra_attachments.csv` (the 16 attachments),
  `..\_missing_reports.csv` (the 10 missing Q1 reports).

**Rules:**
- `goal.md` is immutable. Do not modify source PDFs. No git.
