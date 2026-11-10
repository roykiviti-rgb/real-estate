# Pilot report — 1618 קבוצת אשטרום בע"מ (Q1 + Q2 2026)

Pilot attempt 2 (attempt 1 was lost to an app restart). Scope: only company folder
`1618 - קבוצת אשטרום בע_מ`, both reports, produced at final quality per goal rules R1–R9.
No git was used; no source PDF was modified (all 178 baseline hashes re-verified).

## 1. What was produced

| Output | Path (relative to WORKSPACE) | Notes |
|---|---|---|
| Company workbook | `1618 - קבוצת אשטרום בע_מ\1618 - פירוט תזרים מימון 2026.xlsx` | sheets `פירוט מימון`, `מיפוי שורות`, `מקורות`; RTL; 8 period columns |
| Screenshots PDF | `1618 - קבוצת אשטרום בע_מ\1618 - צילומי מסך תזרים מימון 2026.pdf` | 9 pages (cover + 4 images per report), 2.6 MB, bookmarks |
| Master workbook (pilot) | `סיכום פירוט תזרים מימון 2026 - כל החברות.xlsx` | 5 sheets (`נתונים` 8 rows, `מיפוי שורות` 112 rows, `אינדקס קבצים` 2 PDFs, `חסרים והערות`, `הסבר`); will be regenerated in the full run |

Process files (all under `.goals\financing-cashflow-breakdown-2026\work\`): reusable pipeline
(`fcf_lib.py`, `extract_report.py`, `finalize_report.py`, `build_company.py`, `fcf_render.py`,
`checks.py`, `build_master.py`, review/integrity tools), verified data `data\1618_Q1.json`,
`data\1618_Q2.json`, review records `overrides\1618_Q*.json`, `check_explanations.json`,
`checks_result.json`, `pilot-progress.md`.

## 2. Sources used, columns, units

| Report | Source file (role: מקור הנתונים – דוח רבעוני) | Pages | Consolidated CF statement | Financing section | Columns (statement order) | Units |
|---|---|---|---|---|---|---|
| Q1 2026 | `1618_קבוצת אשטרום בע_מ_2026_Q1_1743867.pdf` | 81 | PDF pp. 55–57 (printed 10–12) | PDF p. 56 (printed 11) | 3 חודשים שהסתיימו ב-31.03.2026 (בלתי מבוקר); 3 חודשים שהסתיימו ב-31.03.2025 (בלתי מבוקר); שנה שהסתיימה ב-31.12.2025 (מבוקר) | אלפי ש"ח → currency ש"ח, units אלפים |
| Q2 2026 | `1618_קבוצת אשטרום בע_מ_2026_Q2_1766160.pdf` | 97 | PDF pp. 66–68 (printed 12–14) | PDF p. 67 (printed 13) | 6 חודשים שהסתיימו ב-30.06.2026; 6 חודשים שהסתיימו ב-30.06.2025; 3 חודשים שהסתיימו ב-30.06.2026; 3 חודשים שהסתיימו ב-30.06.2025 (all בלתי מבוקר); שנה שהסתיימה ב-31.12.2025 (מבוקר) | אלפי ש"ח |

Not used (out of scope, documented in `מקורות`): solo Reg. 38D cash-flow data (Q1 pp. 74–75, Q2 pp. 90–91),
board-of-directors CF summary (Q1 p. 29, Q2 pp. 36–37). Pages 57 / 68 of the statement are the
non-cash appendix ("פעילויות מהותיות שלא במזומן") – shown in the screenshots, not extracted.
No column is labelled restated. No extra attachment files exist for 1618.

## 3. Line → item mapping (both reports) and values

The financing section has the same 13 lines + total in both reports; every line maps 1:1 to an item
(no `אחר`, no subtotals, no net-by-sign lines). Values in thousands of NIS, payments in parentheses.

#### Q1 2026 – `1618_קבוצת אשטרום בע_מ_2026_Q1_1743867.pdf` – PDF page 56

| # | Original line (verbatim) | Item | 3M→31.03.2026 | 3M→31.03.2025 | FY→31.12.2025 | Reasoning note |
|---|---|---|---|---|---|---|
| 1 | הנפקת אגרות חוב (בניכוי הוצאות הנפקה) | 3 | 0 | 0 | 959,714 | bond issuance net of issuance costs |
| 2 | הנפקת מניות (בניכוי הוצאות הנפקה) | 1 | 0 | 583,911 | 583,911 | share issuance net of costs |
| 3 | פרעון אגרות חוב | 8 | (241,336) | (235,750) | (871,732) | |
| 4 | קבלת הלוואות לזמן ארוך מתאגידים בנקאיים ואחרים | 4 | 1,161,665 | 262,547 | 1,003,180 | includes non-bank lenders ("ואחרים") – item 4 covers any lender |
| 5 | פרעון הלוואות לזמן ארוך מתאגידים בנקאיים ואחרים | 7 | (436,775) | (160,817) | (719,541) | includes non-bank lenders |
| 6 | אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו | 5 | 477,976 | (177,306) | (33,850) | **non-obvious:** includes "ואחרים" (non-bank) – per R3 item 5 takes ST credit from banks and others |
| 7 | פרעון התחייבויות בגין חכירה | 10 | (11,912) | (10,686) | (41,103) | **non-obvious:** line does not say "קרן"; no separate lease-interest line exists, treated as principal |
| 8 | ריבית ששולמה | 13 | (139,046) | (134,156) | (604,190) | interest paid is classified in financing in this statement |
| 9 | תמורה ממימוש אופציות | 2 | 0 | 1 | 1 | |
| 10 | הנפקה לבעלי זכויות שאינן מקנות שליטה | 6 | 0 | 0 | 269,916 | issuance of subsidiary equity to NCI |
| 11 | רכישה מבעלי זכויות שאינן מקנות שליטה | 14 | 0 | 0 | (29,030) | **non-obvious:** purchase from NCI = additional interest in an already-controlled subsidiary (equity transaction) |
| 12 | דיבידנד לבעלי המניות | 11 | 0 | 0 | (80,000) | dividend to owners of the parent |
| 13 | דיבידנד לבעלי זכויות שאינן מקנות שליטה | 12 | 0 | 0 | (9,671) | |
| 14 | מזומנים נטו שנבעו מפעילות מימון | = | 810,572 | 127,744 | 427,605 | reported total |

#### Q2 2026 – `1618_קבוצת אשטרום בע_מ_2026_Q2_1766160.pdf` – PDF page 67

| # | Original line (verbatim) | Item | 6M→30.06.2026 | 6M→30.06.2025 | 3M→30.06.2026 | 3M→30.06.2025 | FY→31.12.2025 |
|---|---|---|---|---|---|---|---|
| 1 | הנפקת אגרות חוב (בניכוי הוצאות הנפקה) | 3 | 0 | 156,154 | 0 | 156,154 | 959,714 |
| 2 | הנפקת מניות (בניכוי הוצאות הנפקה) | 1 | 0 | 583,911 | 0 | 0 | 583,911 |
| 3 | פרעון אגרות חוב | 8 | (262,608) | (410,517) | (21,272) | (174,767) | (871,732) |
| 4 | קבלת הלוואות לזמן ארוך מתאגידים בנקאיים ואחרים | 4 | 2,396,491 | 395,101 | 1,234,826 | 133,821 | 1,003,180 |
| 5 | פרעון הלוואות לזמן ארוך מתאגידים בנקאיים ואחרים | 7 | (981,346) | (393,869) | (544,571) | (234,319) | (719,541) |
| 6 | אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו | 5 | 539,300 | (66,363) | 61,324 | 110,943 | (33,850) |
| 7 | פרעון התחייבויות בגין חכירה | 10 | (25,534) | (21,366) | (13,622) | (10,680) | (41,103) |
| 8 | ריבית ששולמה | 13 | (318,447) | (275,992) | (179,401) | (141,836) | (604,190) |
| 9 | תמורה ממימוש אופציות | 2 | 0 | 1 | 0 | 0 | 1 |
| 10 | הנפקה לבעלי זכויות שאינן מקנות שליטה | 6 | 0 | 262,957 | 0 | 262,957 | 269,916 |
| 11 | רכישה מבעלי זכויות שאינן מקנות שליטה | 14 | 0 | (21,500) | 0 | (21,500) | (29,030) |
| 12 | דיבידנד לבעלי המניות | 11 | (100,000) | (80,000) | (100,000) | (80,000) | (80,000) |
| 13 | דיבידנד לבעלי זכויות שאינן מקנות שליטה | 12 | 0 | 0 | 0 | 0 | (9,671) |
| 14 | מזומנים נטו שנבעו מפעילות מימון | = | 1,247,856 | 128,517 | 437,284 | 773 | 427,605 |

Reasoning notes are the same as in Q1 (they are stored per line in both mapping sheets). Item 9
(רכישה עצמית של מניות) and `אחר` are 0 in every period.

**(\*) treatment:** interest paid and dividends paid appear only in the financing section; the
operating section shows only "דיבידנד שהתקבל" and the investing section "ריבית שהתקבלה" (receipts).
Both (\*) info rows are therefore 0 in all 8 periods (master note empty, per R5); the company sheet's
notes column says so explicitly, and the screenshots include the operating page as evidence.

## 4. Consistency checks

| Check | Result |
|---|---|
| C1 (items + אחר − reported total, every report×period) | **0 in all 8 columns** (3 Q1 + 5 Q2) |
| C2 totals 2026 | Q1 3M 810,572 = Q2 6M 1,247,856 − Q2 3M 437,284 ✔ |
| C2 totals 2025 | Q1 3M 127,744 = Q2 6M 128,517 − Q2 3M 773 ✔ |
| C3 FY-2025 Q1 vs Q2 | identical for the total and all 14 items + אחר (16/16) ✔ |
| C2 item level (informational, not required) | 2 differences, both explained: in the Q1-2025 comparative, LT loans received (item 4) and repaid (item 7) are each **1,267 higher in the Q1 report** (262,547 / (160,817)) than implied by the Q2 report (395,101 − 133,821 = 261,280; (393,869) − (234,319) = (159,550)). Net and total identical → a gross-vs-net presentation difference in the comparatives, not an extraction error. Values kept as reported; listed in `חסרים והערות` (type "לידיעה") and as column notes. |

No unexplained mismatch remains.

## 5. How the numbers were verified

1. **Automated text extraction with coordinates** (`extract_report.py`): words rebuilt from PyMuPDF
   characters, grouped into visual rows, value groups assigned to the statement's columns by
   x-position, parentheses → negative, dash → 0; wrapped labels merged; section boundaries from the
   statement's own headings/totals. Column headers parsed into months / end date / audit status.
2. **Visual check**: the financing sections of p. 56 and p. 67 were rendered at 200 DPI and every one of
   the 13 lines × 8 columns + totals was compared digit-by-digit with the extracted values (all equal);
   the operating pages (55, 66) were viewed to confirm no interest/dividend-paid lines there.
3. **Arithmetic**: C1 = 0 in every column, C2/C3 as above.
4. **Outputs reviewed**: the workbooks were opened (copies in %TEMP%) via Excel COM – no errors, live
   check formulas evaluate to 0, sheets RTL; Excel PDF exports and all 9 pages of the screenshots PDF
   were rendered and inspected (captions, highlights, legibility).
5. **Integrity**: all 178 baseline files re-hashed – unchanged; the only new files outside `.goals` are
   the 3 outputs; no `__pycache__`, lock or temp files in the WORKSPACE.
6. **Independent re-check script**: `python work\validate.py --issuers 1618 --pilot` (run from `C:\`)
   re-reads both workbooks and the screenshots PDF and compares them with the verified data, re-runs
   C1–C3, master-vs-data equality, baseline hashes and hygiene: **473 checks passed, 0 failed (exit 0)**.

## 6. Design choices / open questions for the user (שאלות להערות)

1. **פריסת הגיליון `פירוט מימון`:** שורות = סעיפים 1–14, אחר, סה"כ מדווח, בדיקה, שתי שורות (\*); עמודות = 8 תקופות
   (קודם 3 של Q1 ואז 5 של Q2). מתחת לכותרת כל עמודה: קובץ מקור, עמוד PDF, כותרת העמודה המילולית מהדוח, חודשים,
   תאריך סוף, "מוצג מחדש", יחידות. בעמודה האחרונה – אילו שורות מקור הרכיבו כל סעיף. מתאים, או עדיף גיליון לכל דוח?
2. **תצוגת מספרים:** תשלומים מוצגים כמספר שלילי עם מינוס (‎-436,775) ואפס כ-0. להעדיף סוגריים כמו בדוח, או "-" במקום 0?
3. **כפילות תקופות:** שנת 2025 (והשוואתיים של 2025) מופיעים גם בדוח Q1 וגם בדוח Q2 – נרשמו פעמיים כפי שדווחו
   (בקובץ המרכז 8 שורות לאשטרום). להוסיף עמודה "תקופה עיקרית" כדי שסינון/Pivot לא יספור כפול?
4. **סעיף 5 ו"אחרים":** לפי הכלל, "אשראי לזמן קצר מתאגידים בנקאיים **ואחרים**" נכנס לסעיף 5 (וכך גם הלוואות ארוכות
   מ"אחרים" בסעיפים 4/7) – עם הערה. מקובל?
5. **חכירה:** "פרעון התחייבויות בגין חכירה" סווג לסעיף 10 (קרן) אף שהשורה לא מפרידה קרן/ריבית. מקובל?
6. **שורות (\*):** כשאין ריבית/דיבידנד מחוץ למימון – 0, ובעמודת ההערות "אין סכומים מחוץ לפעילות מימון".
7. **הפרשים ברמת סעיף בין הדוחות** (כמו 1,267 באשטרום – ברוטו/נטו בהשוואתיים): לרכז אותם בהרצה המלאה כ"לידיעה"
   (עלול להיות רועש), או לדווח רק הפרשים בסה"כ כפי שנדרש ב-C2?
8. **קובץ צילומי המסך:** שער + לכל דוח: (1) עמוד מלא עם הדגשה (צהוב/כתום = מימון, כחול = כותרות ויחידות),
   (2) הגדלה ב-220 DPI של רצועת הכותרות + סעיף המימון (פעילות ההשקעה שביניהם הושמטה וסומנה בקו מקווקו),
   (3) שאר עמודי הדוח המאוחד (שוטפת – להוכחת (\*) = 0; עמוד "שלא במזומן" – לשלמות). להשאיר את עמודי ההקשר
   (3), או להסתפק ב-(1)+(2) (קובץ קטן יותר)? להעדיף הגדלה רציפה (כולל פעילות ההשקעה) על פני הרכבה?
9. **שמות התקופות:** עמודות ה-3 חודשים בדוח Q2 נקראות "3 חודשים שהסתיימו ב-30.06.2026" (= אפריל–יוני). להוסיף
   "(אפריל–יוני)"?
10. **שורת הסה"כ:** בעמודת "מס'" מופיע "=" ובתווית "סך תזרים מזומנים מפעילות מימון" (הנוסח שלך); הנוסח המקורי
    ("מזומנים נטו שנבעו מפעילות מימון") מופיע בגיליון המיפוי ובהערות.

**Mapping edge cases expected in the other 85 companies (planned handling, per R3):** net LT-loan/bond
lines → 4/7 or 3/8 by sign per period; gross ST-credit receipt/repayment lines → both to 5; loans from
controlling shareholder / related parties / partners → 4/7 (or 5 if short-term/net without term);
partnership capital contributions / distributions → 1/11 (reporting entity) or 6/12 (NCI); נע"מ → 3/8
with a note; restricted/pledged deposits, hedge settlements, contingent consideration, grants → `אחר`
with verbatim text; interest paid inside "מזומנים ששולמו והתקבלו במשך התקופה עבור" (operating) or capitalised
interest in investing → (\*) info rows + red-highlighted crop; foreign issuers' statements kept in USD/EUR/
CAD/PLN; PDFs without a usable text layer (1083, 1905, 1644 Q1, 341 Q1, 1331 Q2 per discovery) → values
read visually from renders and validated by C1; statements split over pages / 3-month columns on separate
pages → handled by multi-page segments (code supports it; to be exercised in the full run).

## 7. Notes for the full run

- Pipeline is generic: `extract_report.py` (auto) → visual review + `overrides\*.json` → `finalize_report.py`
  → `build_company.py` → `checks.py` → `build_master.py` (without `--pilot`) → `validate.py` (without `--pilot`).
  Still to do: roles for the 16 attachments (`roles.json`), statements without a text layer,
  possible English/LTR statements, and statements whose columns differ between pages.
- The master `אינדקס קבצים` currently lists only Ashtrom's 2 PDFs (pilot mode).

Assisted-by: Anthropic:Claude Opus 5.5
