# Inspection 1 – batch 7 of 8 (Inspector, iteration 1)

Companies: 473, 1330, 1618, 1903, 1905, 2384, 2386, 2429, 2449, 2522, 2559 (22 reports, 88 period columns).
References used: `goal.md`, `goal-amendment-1.md` (T1, T2), `goal-amendment-2.md` (T3 cancelled), `work/phaseB-conventions.md`,
and the mapping rules in `PIPELINE.md` §7 (rule A for gross lines with no stated term). I formed the findings below **before**
reading `work/batches/batch-7.md`, `phaseC-progress.md` and `builder-report-1.md`. I read them afterwards only to check
whether the two mapping problems in §4 were decided on purpose. They were, and the rationale does not hold (see §4).

## Verdict: **FAIL**

All 22 reports have the right source and pages, every period, and every value (digits, sign, units) correct. C1 is 0
everywhere, C2/C3 are clean or explained, the master rows match the company workbooks, and the screenshots are complete.
**Two companies have a wrong item mapping:**

- **1905:** `קבלת אשראי` / `פירעון אשראי`.
- **2386:** `קבלת אשראי והלוואות מגופים פיננסיים` / `פירעון ...`.

Both lines contain long-term land loans and have mixed current and non-current balances, yet both are mapped to item 5.
By R3 (item 4 explicitly includes "long-term project/land finance") and by rule A ("mixed or not attributable → 4/7 with a
note"), which was applied to every other mixed case (1829, 486, 1797, 2360, …), they belong in 4/7. As a result, items
4, 5 and 7 are wrong in all 16 columns of these two companies, in the company workbooks and in the master.

Issues: **2 blocking** (B1, B2), **1 open decision** (D1), **5 non-blocking observations** (O1–O5).

---------------------------------------------------------------------------------------------------------------

## 1. What I did and what I saw

1. **Independent extraction.** My own PyMuPDF scripts (in `%TEMP%\fcf_insp\7`) did the following:
   - scanned every PDF in the 11 folders for cash-flow statement pages (consolidated vs separate/38D vs investee vs board
     report);
   - rebuilt each statement row from character positions, attaching parenthesis glyphs to numbers to get the sign;
   - assigned each value to a column by its x position;
   - matched every workbook mapping line (value vector + text) to a PDF row;
   - listed every PDF row with numbers inside the financing section that matched no workbook line (there were none, apart
     from the 2384 Q1 case in O3);
   - listed every row on the statement pages that mentions interest or dividends.
2. **Visual confirmation, 34 images, all actually displayed (below the 50-image cap).**
   - **22 composites, one per report**, rendered from the source PDF at 180 DPI: the header strip (title, column headers,
     audit status, units), the full financing section from heading to total, and every (*) line with the row above it.
     I read every label and value of every column on these images and compared them with the workbooks. Every value
     below was confirmed on an image, not only on the text layer.
   - **11 screenshots-PDF composites:** the zoom pages of both reports and the (*) crop pages, at 0.95 scale.
   - **1 contact sheet** of 12 full-page highlight pages.
   - **Pixel analysis of the frames** in all 87 embedded screenshot images: the orange, blue and red frame positions were
     converted to source points and compared with my financing-section coordinates.
3. **Workbooks.** I read all three sheets of all 11 workbooks (from copies) with openpyxl and checked:
   - item sums per column against the mapping lines;
   - C1, recomputed;
   - labels, months, end dates, restated flags and the T2 suffix;
   - file/page rows, header block, number formats, RTL;
   - the sources sheet against the folder contents and real page counts.
4. **Master.** I compared the 88 `נתונים` rows of my issuers field by field with the company workbooks, including the T1
   flag; the 889 `מיפוי שורות` rows by count and value; and the `אינדקס קבצים`, `חסרים והערות` and `הסבר` (T1) entries.
5. **Quality gate.** I ran `validate.py` with TEMP redirected to my temp folder, so nothing was written to `%TEMP%\fcf_run`
   or WORKSPACE:
   - `--issuers <my 11> --no-master`: **PASS 3589 / FAIL 0**.
   - Full run with the master: **PASS 36751 / FAIL 0 / INFO 10, exit 0**.
   - Tool note: `--issuers` *without* `--no-master` reports about 860 AC11/T1 "failures". These are an artefact of
     subset mode (it compares the whole master with a subset), not defects.
6. **Hygiene.** No `__pycache__`, no lock files, nothing new in the company folders other than the two outputs, and
   `%TEMP%\fcf_run` was not recreated.

---------------------------------------------------------------------------------------------------------------

## 2. Per company × report

Legend: Src = right file, consolidated statement, cited pages. Per = columns, labels, months, end dates, restated flag, T2.
Val = every line value, total and units. Map = item assignment. (*) = info rows and notes. Lay = workbook layout.
Shots = screenshots PDF.

| Co. | Rep | Src | Per | Val | Map | (*) | Lay | Shots | Evidence (all pages are 1-based PDF pages) |
|---|---|---|---|---|---|---|---|---|---|
| 473 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p55–56 consolidated (38D at p92–93 not used); 13 lines + total (4,849)/47,463/1,236,869; (*) interest in operating, p55 (39,353)/(21,218)/(101,793) |
| 473 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p60–61; total 597,788/902,727/602,637/855,264/1,236,869; (*) p60 (66,956)…(101,793) |
| 1330 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p53 statement + p54 appendices; total 385,908/359,013/1,060,465; (*) appendix B "עלויות מימון (כולל עלויות שהוונו)" 49,718/42,490/196,235, printed positive, section not stated |
| 1330 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p57–58; total 234,394/777,658/(151,514)/418,645/1,060,465; dividend (6,000) → 11 |
| 1618 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p55–57; 13 lines; total 810,572/127,744/427,605; interest and dividends in financing only |
| 1618 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p66–68; total 1,247,856/128,517/437,284/773/427,605 |
| 1903 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p57 (+58 appendices); "(*)46,142"/"(*)(31,276)" are restatement markers, read as +46,142/(31,276); 3M-2025 restated |
| 1903 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p57; total (177,385)/124,695/(133,814)/34,433/(43,099); 6M/3M-2025 restated |
| 1905 | Q1 | PASS | PASS | PASS | **FAIL** (B1) | PASS | PASS | PASS | p40 single page; values correct; mapping of lines 2–3 wrong (see B1) |
| 1905 | Q2 | PASS | PASS | PASS | **FAIL** (B1) | PASS | PASS | PASS | p43–44; values correct; mapping of lines 2–3 wrong |
| 2384 | Q1 | PASS | PASS | PASS (O3) | PASS | PASS | PASS | PASS (O4) | p46–47; 395,555 printed on the shares row in 3M-2025, moved to the bonds row with documentation (O3); (*) appendix B 15,605/13,751/130,043 |
| 2384 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS (O4) | p55–56; total 243,349/302,514/158,318/75,127/473,134; -01 file = appraisal, correctly not used |
| 2386 | Q1 | PASS | PASS | PASS | **FAIL** (B2) | PASS | PASS | PASS | p29–30; values correct; mapping of lines 5–6 wrong (see B2) |
| 2386 | Q2 | PASS | PASS | PASS | **FAIL** (B2) | PASS | PASS | PASS | p32–33; values correct; mapping of lines 5–6 wrong |
| 2429 | Q1 | PASS | PASS | PASS | PASS (O1) | PASS | PASS | PASS | p32–33; total (12,418)/41,600/1,165,735; (*) interest in operating, p32 |
| 2429 | Q2 | PASS | PASS | PASS | PASS (O1) | PASS | PASS | PASS | p34–35; lease printed +53 in Apr–Jun 2026, recorded as printed and documented |
| 2449 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p44–45; "*2025" column header → restated; `קבלת אשראי` line effectively net (negative values) → 5, correct under R3 |
| 2449 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p45–46 |
| 2522 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p25–27; the page running head prints "באורים…", content is the consolidated statement (documented in the master); (*) appendix A, included in operating |
| 2522 | Q2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | p27–29; Q2 line without a term → 4/7 as in Q1 (same line) |
| 2559 | Q1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | **-01** p24–25 (corrected report); the -02 p27 financing section is identical row by row (9/9); main file = 3-page excerpt |
| 2559 | Q2 | PASS | PASS | PASS | PASS (D1) | PASS | PASS | PASS | p31–32; (30,547) printed in an item-4 receipt line, recorded as printed and documented; `התאמת תמורה` → 1 (see D1) |

Common to all 22 reports:
- **Source:** the consolidated statement was used, not the separate/38D statement, the board report or an investee. 2559
  Q1 is -01; 2384's -01 and 2559's -02 and main file are correctly not data sources.
- **Periods and layout:**
  - Column order follows the statement, read right to left.
  - The T2 suffix is present on every April–June column.
  - The header block is correct: names with `"` restored, issuer, currency and units.
  - Item labels match exactly.
  - The check row is a live formula and computes to 0 in all 88 columns.
  - Numbers are numeric cells with the format `#,##0;-#,##0;0`.
  - All three sheets are RTL.
  - Every `מקורות` sheet matches its folder and the real page counts.
- **Screenshots:**
  - The orange and blue frames on every full page cover the financing section and the header block. Example: 473 Q1, frame
    313–523 pt, my section 318–518 pt.
  - Every zoom shows the period headers, the units and every financing line legibly.
  - There is a red (*) crop for each (*) line (473, 1330, 1905, 2384, 2429, 2522).
  - Captions name the file, the PDF page and the printed page. The pages shown match those the workbook cites.

---------------------------------------------------------------------------------------------------------------

## 3. Cross-report checks and master

**C3.** For all 11 companies, FY-2025 in Q1 equals FY-2025 in Q2 for the total, every item and both (*) rows.

**C2 total.** Equal everywhere except:

| Company | Column | Q1 | Q2 6M − 3M | Diff | Explained in `חסרים והערות` |
|---|---|---|---|---|---|
| 2386 | 3M-2025 | 32,013 | 32,012 | 1 | r124: interest rounding |
| 2559 | 3M-2025 | (23,897) | (23,895) | −2 | r174: rounding in lines 7 and 5 |

**C2 per item (information only).** All are listed with explanations:

| Company | Items | Diff | Master row |
|---|---|---|---|
| 1618 | 4 / 7, 2025 | ±1,267 | r108–109 |
| 2386 | 13, 2025 | 1 | r123 |
| 2522 | 4 / 7, 2026 | ±123,001 (Q2 report nets the loans) | r164–165 |
| 2559 | 4 / 5, 2026 and 5 / 7, 2025 | ±1 | r170–173 |

My independent recomputation found exactly these differences and no others.

**Master `נתונים`.** 88/88 rows equal the company workbooks: items, אחר, total, check, both (*) amounts, months, end date,
restated flag, file, page and currency. **T1** is `לא` only on the 11 Q1 FY-2025 rows and `כן` on the rest. T1 is
explained in `הסבר`, row 39.

**Master `מיפוי שורות`.** 889/889 rows of my issuers match by text, period and value.

**Master `חסרים והערות`.** It also lists these source irregularities: 473 `פינסיים`, 1905 Q2 6M>FY gross presentation,
2384 Q1 misprint, 2429 +53, 2522 running head and 2559 (30,547). It also records the source decisions for 2384 -01 and for
2559 main/-01/-02.

---------------------------------------------------------------------------------------------------------------

## 4. Issues

### B1 (blocking) – 1905: gross "credit" lines that contain long-term land loans mapped to item 5

Lines: Q1 p40 lines 2–3 and Q2 p44 lines 2–3, `קבלת אשראי` / `פירעון אשראי` (gross lines, no stated term). Both are
mapped to **5**.

Evidence:
- **Q1 balance sheet, p37:**
  - current `אשראי מתאגידים בנקאיים ואחרים`: 485,967 at 31.3.2026;
  - **non-current** `הלוואות מתאגידים בנקאיים ומנותני אשראי אחרים`: **103,947** at 31.3.2026, against 784 at 31.12.2025.
- **Q1 note, p42:** in March 2026 the bank lent **86.1 M NIS to buy land, repayable in full on 26.3.2028.** The builder's
  own line note says the same.
- At least 86.1 M of the 186,911 received in Q1 2026 is therefore long-term land finance. The non-current balance rose
  by about 103 M in the quarter.
- R3 item 4 explicitly covers "long-term project/land finance". Rule A (PIPELINE §7 and builder-report-1 §3-A) says
  "current and non-current balances for the same lenders → **4/7 with a note**". The same rule was applied to 1829 ("bank
  and other credit, current + non-current") and to 486, 1797, 2360, 2389, 2396, 2503 and 2533.
- Phase C kept 5 by labelling 1905 "gross `אשראי` lines, current". That label is factually wrong, and it contradicts
  builder-report-1 §8.2. The result breaks AC5 (consistent assignments).

Expected (4/7) vs found in `פירוט מימון` and the master. Columns, in order: Q1 3M-26, Q1 3M-25, Q1 FY25, Q2 6M-26,
Q2 6M-25, Q2 AJ-26, Q2 AJ-25, Q2 FY25.

| Item | Expected | Found |
|---|---|---|
| 4 | 186,911 / 2,312 / 179,203 / 186,911 / 282,312 / 0 / 280,000 / 179,203 | 0 everywhere |
| 7 | (64,803) / 0 / (204,120) / (64,803) / (280,000) / 0 / (280,000) / (204,120) | 0 everywhere |
| 5 | (10,687) / (28,197) / 14,453 / (7,044) / (2,563) / 3,643 / 25,634 / 14,453 | 111,421 / (25,885) / (10,464) / 115,064 / (251) / 3,643 / 25,634 / (10,464) |

Totals are unchanged.

### B2 (blocking) – 2386: `קבלת אשראי והלוואות מגופים פיננסיים` / `פירעון ...` mapped to item 5

Lines: Q1 p29 lines 5–6 and Q2 p32 lines 5–6. In Q2 the receipt line itself reads "(ראה ביאור 4א(1))".

Evidence:
- **Q1 note 4א(1), p35:** in January 2026 the company received loans of **43,424** from a financial body to buy the land of
  the Nes Ziona (Resort 2) project. They are **repayable at completion of the works and no later than 30.6.2030**, and
  are **"presented as a non-current liability"**. That is 43,424 of the 50,574 received in Q1 2026 (86%).
- **Q1 balance sheet, p26:**
  - current `אשראי מגופים פיננסיים ונותני אשראי אחרים`: 56,850;
  - **non-current** `הלוואה מתאגיד בנקאי`: **48,490**, against 4,699 at 31.12.2025.
- **Q2 balance sheet, p29:** current 60,711 and non-current 49,318.
- The balances are about half and half, so they are not "predominantly current" as Phase C claimed. Under R3 (item 4 "incl.
  long-term project/land finance") and rule A (mixed → 4/7) these lines should be **4/7**.

Expected vs found, same column order as B1. Item 5 keeps the interested-party and partner net lines.

| Item | Expected | Found |
|---|---|---|
| 4 | 50,574 / 4,817 / 12,959 / 55,704 / 6,986 / 5,130 / 2,169 / 12,959 | 0 everywhere |
| 7 | (8,539) / (4,163) / (27,033) / (8,539) / (16,969) / 0 / (12,806) / (27,033) | 0 everywhere |
| 5 | (220) / 112 / (496) / 264 / (1,332) / 484 / (1,444) / (496) | 41,815 / 766 / (14,570) / 47,429 / (11,315) / 5,614 / (12,081) / (14,570) |

Totals are unchanged.

### D1 (open decision) – 2559 Q2: `תשלום לבעל עניין בגין התאמת תמורה` (52,500) → item 1, negative

- Source: p32, 6M-26 and AJ-26 columns. The note on p46 says this is an IPO "event compensation" to Phoenix, a 20% holder:
  5% of the increase in value, capped at 52.5 M, charged to equity and financed by a 52.5 M draw on the Phoenix credit
  line (the 52,500 in the `קבלת הלוואות מבעלי עניין` line).
- Netting it into item 1 cuts the IPO proceeds shown from 387,219 to 334,719.
- R3 lists "contingent-consideration payments" under `אחר`.
- The batch builder asked Phase C to align this ("Please align"). I found no Phase C decision.
- Item 1 is defensible and well documented, but the orchestrator should confirm it or move the line to `אחר`, applying the
  same rule to any similar case in other batches. Not blocking on its own.

### Observations (non-blocking)

- **O1 – 473 vs 2429.** The same flow, `קבלת הלוואה מהמיעוט` with identical Q1 values 1,676 / 31,746 / 111,453, is item
  **4** in 473 and item **5** in 2429. 2429 Q2 nets it (`קבלת (פירעון)…`, rule B → 5) and Q1 was aligned to Q2. 473 shows
  the line gross in both reports (rule A, balance mainly non-current → 4). The difference follows the rules, but a user
  comparing parent and subsidiary will see it. A cross-reference in both line notes would help.
- **O2 – restated flag.**
  - Set when the column header is starred (2449) or when the restatement markers sit on financing values (1903, 1905).
  - Only a column note when the markers are on operating values (2384, 2559).
  - This is a reasonable and consistent reading of conventions §10, and it is documented in builder-report-1 §8.5.
- **O3 – 2384 Q1, 3M-2025.**
  - On the image, the bonds row prints `-` and the shares row prints 395,555.
  - The workbook records the bonds row as 395,555 and the shares row as 0, under conventions §9.
  - The evidence supports it: Q2 6M−3M gives bonds 395,555 and shares 0; the 38D data on p61; the statement of changes in
    equity.
  - It is documented in both line notes, the column note and master r53.
  - Accepted, but it is the one place in this batch where a line value differs from the printed row.
- **O4 – cosmetic, 2384 zooms.** The zoom pages (screenshots p3, p7) have no blue/orange frames, while every other
  company's zoom has them. The header strip and section are contiguous, so this does not breach R7.
- **O5 – cosmetic, (*) crops.** Several (*) crops show half-cut neighbouring rows above and below the red line (473 p4/p8,
  1905 p7, 2429 p4/p8). The values are legible.

---------------------------------------------------------------------------------------------------------------

## 5. What must be fixed

1. **1905:** set `line_items` for `קבלת אשראי` → 4 and `פירעון אשראי` → 7 in **both** `1905_Q1.json` and `1905_Q2.json`.
   The note should cite balance sheet p37 (current 485,967 / non-current 103,947) and note p42 (86.1 M land loan, 2028),
   and say "mixed – rule A".
2. **2386:** set `line_items` for `קבלת אשראי והלוואות מגופים פיננסיים` → 4 and `פירעון אשראי והלוואות מגופים פיננסיים`
   → 7 in **both** reports. The note should cite note 4א(1) (43,424, due by 30.6.2030, non-current) and the balance
   sheets: Q1 p26 56,850 / 48,490; Q2 p29 60,711 / 49,318.
3. Then:
   - re-run `finalize_report.py` and `checks.py` for 1905 and 2386; the C2 per-item rows may change and must be
     explained;
   - run `build_company.py 1905` and `build_company.py 2386`;
   - rebuild the master;
   - correct builder-report-1 §3-A, which wrongly lists 1905 and 2386 as "gross `אשראי` lines, current";
   - re-run `validate.py`.
4. Orchestrator decision on **D1** (2559 `התאמת תמורה`: item 1, negative, or `אחר`), recorded in the conventions and in
   `הסבר`.

Temp files: `%TEMP%\fcf_insp\7\` deleted at the end of this inspection.
