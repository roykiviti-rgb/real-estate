# Inspection 1, batch 3: independent verification

- **Inspector:** batch 3 of 8, iteration 1.
- **Date:** 2026-11-10.
- **Companies:** 200, 421, 531, 1039, 1068, 1974, 2458, 2486, 2487, and 2567 (Q2 only).
- **Scope:** 10 companies, 19 reports, 77 period columns.

**References:**
- `goal.md`;
- `goal-amendment-1.md` (T1 and T2 apply);
- `goal-amendment-2.md` (T3 is cancelled);
- `work/phaseB-conventions.md`, together with PIPELINE §7 and the Phase C rules A and B.

I formed every finding below myself before I opened any builder or batch report. Afterwards I read only `work/batches/batch-3.md` §0 and §2–§6, to compare its mapping decisions with mine. That reading did not change any finding.

## Verdict: **PASS**

- **Blocking issues:** 0.
- **Minor observations:** 4 (M1–M4, §4). None of them changes a number, a column, an item assignment or a check result.

---

## 1. How I verified (what I saw and how)

### 1.1 Source location

- **Own page scan.** I scanned all 19 PDFs in the 10 folders with my own PyMuPDF script. Before searching I repaired the broken glyph `ð`/`ª` = `נ` in 200, 2486 Q1 and 2567, and I dumped every candidate page with word coordinates.
- **Consolidated statement located.** In each report I found the consolidated statement (`דוחות מאוחדים על תזרימי המזומנים` / `תמצית דוחות על תזרימי המזומנים ... מאוחדים`).
- **Pages I excluded.** I set aside:
  - the 38D pages (`נתונים כספיים ... המיוחסים לחברה`, `מידע כספי נפרד`), which are present in 421, 531, 1039, 1068, 1974, 2458, 2487 and 2567;
  - the board-report CF tables (for example 200 pp. 24–28, 421 p. 22, 2567 p. 14);
  - the investee statements in 1974 (pp. 82, 92, 102, 113 and others).
- **Attachments.** None of my folders has a `-01` or `-02` file. Each company has exactly one main file per quarter, and 2567 has only Q2.

### 1.2 Independent extraction

- **Own transcription.** I wrote my own expected values for every line × column of all 19 financing sections, together with the totals and every (\*) line. The source was my own word dump (`ext_*.txt`).
- **Recovered signs and garbled numbers.** Where the text layer splits parentheses or numbers, I recovered the sign or digits by solving each column against the printed total:
  - signs in 421, 1068, 1974, 2487, 531 Q2 and others;
  - garbled numbers such as 2458 `8,91`/`8`, which is 8,918, and 1974 `16,`/`701`, which is 16,701.
- **Every value confirmed on an image.** I then confirmed all of it on rendered images I actually saw: 19 composites at 170 DPI, one per report. Each composite holds:
  - the header strip (title, period headers, audited/unaudited line, units);
  - the whole financing section, from the heading to the total;
  - the header strip of the operating/appendix page;
  - the (\*) lines.
- **Image budget.** I viewed 30 images in total: the 19 composites, 10 screenshot contact sheets and one embedded zoom image. Every one displayed; none returned the "maximum number of images" message.
- **Results.**
  - Every line value, sign, dash/blank and total in the workbooks equals my transcription. My script compared them automatically: 0 mismatches out of 19 reports.
  - Every value was also seen on an image.
  - C1 = 0 in all 77 columns, both in my own data and in the workbook sums.

### 1.3 Workbooks

I copied each company workbook to TEMP and read it with openpyxl, both with formulas and with cached values. I checked:
- `פירוט מימון`:
  - the header block;
  - the source rows: file, page, verbatim header, months, end date, restated flag and units;
  - the item values: each must equal the sum of the lines mapped to it in `מיפוי שורות` (0 mismatches);
  - the reported total;
  - the live check formulas: their ranges cover items 1–6, 7–14, `אחר` and the total in all 10 files;
  - the (\*) rows and their notes, and the column notes;
- `מיפוי שורות`: verbatim texts against the images, and the per-block SUMPRODUCT ranges;
- `מקורות`: page counts, report IDs, roles and pages;
- RTL on all sheets.

### 1.4 Master workbook

- **`נתונים`.** My company rows are 77 = 9 × 8 + 5. Every field equals the company workbook (0 mismatches over all 36 columns):
  - item values, total and check;
  - the (\*) values and their notes;
  - label, months, end date, restated flag, source file, pages, currency and units;
  - the T1 flag `תקופה עיקרית`. It is `לא` only on the Q1 rows for FY-2025 of the 9 two-report companies, and `כן` everywhere else, including all 2567 rows.
- **`מיפוי שורות`.** The row counts per issuer equal Σ (lines + total + (\*) lines) × periods: 77, 85, 64, 61, 88, 85, 56, 64, 69 and 50.
- **`אינדקס קבצים`.** The rows for my 19 PDFs are correct.
- **`חסרים והערות`.**
  - It holds every C2 mismatch in my batch, each with an explanation (§3).
  - It holds the source irregularities.
  - It holds the missing-Q1 row for 2567.
- **`הסבר`.** It explains T1 and T2.

### 1.5 Screenshots PDFs

- **Structure.** I read the TOC and caption text of all 10 PDFs programmatically. Every image page cites:
  - the correct report ID and quarter;
  - the same PDF page number as its TOC entry and as the workbook. My regex found the page number in every caption.
- **Image resolution.** I checked the embedded image sizes: 150 DPI for full pages, 120 DPI for context pages and 220 DPI for zooms. These are the pilot settings, and they meet the R7 minimum of ≥110 DPI for pages and ≥200 DPI for zooms.
- **Visual check.** I viewed a contact sheet of every PDF.
  - Highlights: the orange/yellow box spans the financing section from heading to total, the blue box covers the title, headers and units, and the red boxes mark the (\*) lines.
  - Zooms: they contain the header strip and the units line.
  - (\*) crops: they exist for 200, 421, 531, 1974 and 2487.
  - Context pages: the operating and appendix pages are included.
- **Source of truth.** Separately, I confirmed every number on my own source renders (§1.2).

### 1.6 Other checks

- **Integrity.** The SHA-256 of all 19 source PDFs matches `baseline_files_sha256.csv`. My folders contain no unexpected or forbidden files.
- **Quality gate.** I ran `validate.py --issuers 200 421 531 1039 1068 1974 2458 2486 2487 2567 --no-master --out %TEMP%\fcf_insp\3\validate.txt`. Result: `PASS 3119 FAIL 0 INFO 0`.

---

## 2. Per company and report

Legend: P = PASS, F = FAIL.

**Column meanings:**
- **Source:** the right file, the consolidated statement and the cited pages.
- **Periods:** the number of columns, labels, months, end date, T2 suffix and restated flag.
- **Values:** every line, total and (\*) value against the image.
- **Mapping:** the items under R3 and the conventions.
- **(\*):** the info rows and their notes.
- **Layout:** header block, rows, sources sheet and RTL.
- **Shots:** the screenshots PDF.

### 2.1 Check results

| Company | Report | Source (file / CF pp / fin p) | Periods | Values | Mapping | (\*) | Layout | Shots |
|---|---|---|---|---|---|---|---|---|
| 200 | Q1 | P (1745686 / 33–34 / 34) | P (3) | P | P | P | P | P |
| 200 | Q2 | P (1766476 / 36–37 / 37) | P (5) | P | P | P | P | P |
| 421 | Q1 | P (1745074 / 35–36 / 36) | P (3) | P | P | P | P | P |
| 421 | Q2 | P (1764607 / 44–45 / 45) | P (5) | P | P | P | P | P |
| 531 | Q1 | P (1744302 / 29–30 / 30) | P (3) | P | P | P | P | P |
| 531 | Q2 | P (1766963 / 33–34 / 34) | P (5) | P | P | P | P | P |
| 1039 | Q1 | P (1743815 / 49–51 / 50) | P (3) | P | P | P | P (M1) | P |
| 1039 | Q2 | P (1764263 / 54–55 / 55) | P (5) | P | P | P | P | P (M3) |
| 1068 | Q1 | P (1744574 / 45–46 / 46) | P (3) | P | P | P | P | P |
| 1068 | Q2 | P (1764659 / 58–59 / 59) | P (5) | P | P | P | P | P |
| 1974 | Q1 | P (1742794 / 53–54 / 54) | P (3) | P | P | P | P | P (M3) |
| 1974 | Q2 | P (1764536 / 58–59 / 59) | P (5) | P | P | P | P | P (M3) |
| 2458 | Q1 | P (1743908 / 44–45 / 45) | P (3) | P | P | P | P | P |
| 2458 | Q2 | P (1767000 / 44–45 / 45) | P (5) | P | P | P | P | P |
| 2486 | Q1 | P (1744097 / 40–41 / 41) | P (3) | P | P | P | P | P |
| 2486 | Q2 | P (1766260 / 44–45 / 45) | P (5) | P | P | P | P | P |
| 2487 | Q1 | P (1744311 / 32–33 / 32) | P (3) | P | P | P | P | P |
| 2487 | Q2 | P (1766830 / 35–36 / 35) | P (5) | P | P | P | P | P |
| 2567 | Q2 | P (1767289 / 53–55 / 54) | P (5) | P | P (M2) | P | P (missing-Q1 statement at C9) | P |

### 2.2 What I verified per company

Values are in thousands of NIS unless stated otherwise. Payments are shown as negatives.

- **200**
  - Q1, p. 34:
    - Short-term loans from banks and others, gross: receipt 3,500/8,862/17,456 and repayment –/(2,624)/(10,490). Both go to item 5.
    - Lease (136)/(180) → item 10.
    - Warrant exercise, series 1, FY 145 → item 2.
    - Bonds 3,000/58,014 → item 3.
    - Share capital 19,682 → item 1.
    - Proceeds from issuing series 2 warrants, own line, 4,071 → item 2.
    - Total: 3,500 / 9,102 / 88,698.
  - Q2 adds:
    - a purchase of own bonds of (8,672) → item 8;
    - shares of 26,811 / 19,682 → item 1.
  - The Q2 totals are 22,899 / 34,819 / 19,399 / 25,717 / 88,698.
  - (\*) interest paid in operating:
    - Q1, p. 33: (2,677)/(3,111)/(10,059);
    - Q2, p. 36: (5,600)/(4,327)/(2,921)/(1,216)/(10,059).
  - The 2-unit Q1/Q2 difference on the (\*) row is documented.
- **421**
  - Q1 lines:
    - short-term credit, net: (38,661)/27,636/42,451;
    - bonds 196,719 and repaid (130,000)/(176,163);
    - securities 45,000 and costs (1,068) → item 1. Note 5א, p. 40, confirms 3,024,194 shares at 14.88 NIS (45 million) plus warrants A–C, so convention 6 applies.
    - long-term loans 86,362/8,000/68,097 and repaid (6,905)/(11,405)/(39,008);
    - lease.
    - Total: 84,431 / 90,183 / 89,419.
  - Q2 adds:
    - long-term loans from minority holders of 10,548 → item 4 (R3 names NCI holders);
    - totals 105,723 / 155,367 / 21,292 / 65,184 / 89,419.
  - (\*) `ריבית ועמלות ששולמו` in operating: Q1 (13,825)/(28,202)/(94,207) and Q2 (52,123)/(63,383)/(38,298)/(36,011)/(94,207).
- **531**
  - Lines: lease; bonds net of costs; bond repayment; `קבלת (פירעון) אשראי מתאגידים בנקאיים, נטו` → item 5 (net, no term); options 1,301 → item 2 (own line); shares 18,552 → item 1.
  - The Q2 FY bond line prints `280,68`, which is recorded as 280,683. That value reconciles to the total of 308,912 and to Q1, and it is documented in the notes, issues and master.
  - The Q2 3M-2025 total is (8,551).
  - (\*) interest in operating is confirmed.
- **1039**
  - Lines: bonds 66,416/59,024; shares 11,769; short-term loans including overdraft → item 5; non-bank long-term repayment → item 7; NCI capital 4,124 → item 6; interest paid in financing → item 13.
  - In Q2, the blank cells (not `-`) on the shares line and on the 2,000 non-bank long-term loan line are recorded as 0 and noted.
  - There is no (\*) outside financing.
- **1068** (units: מליוני ש"ח, millions)
  - Lines: shares 450; subsidiary shares 232 → item 6 (note 4(9), p. 55: the Shikun & Binui Energy IPO, ~232 million net, 66.79% held); long-term loans; bonds; derivatives 11/7/49 → `אחר` (convention 7); short-term credit, net, 181/289/(467), and in Q2 (50)/258/(231)/(31)/(467); interest → item 13; NCI dividends → item 12.
  - Totals: 93/(50)/937 and (210)/127/(303)/177/937.
- **1974** (units: באלפי ש"ח)
  - Q1:
    - short-term credit, net, 689/(24)/21,979;
    - financial-corporations loans 6,081 and (206) → items 4 and 7. This is a gross line; the balance sheet on p. 49 shows bank loans in both current and non-current, so rule A treats it as mixed.
    - bonds 80,644/36,405/93,527;
    - warrants 1,626 → item 2;
    - dividend (3,000) → item 11;
    - shares 12 → item 1. The equity statement on p. 51 shows `הבשלת מניות חסומות` with a total of 12, so this is not an option exercise.
  - Q2 adds bond redemption (13,485) → item 8, and a negative receipt of (46) recorded as printed and noted.
  - (\*) interest paid in operating: (420)/(212)/(16,701) and (9,961)/(7,246)/(9,541)/(7,034)/(16,701).
- **2458**
  - Lines: long-term bank credit; bonds; shares + warrants 178,450 → item 1; long-term repayment; `קבלה (פירעון) ... לזמן קצר, נטו` 8,918/(80,904)/(178,918) → item 5; interest → item 13.
  - Totals: 443,396 / 149,307 / 194,928 and 361,451 / 125,269 / (81,945) / (24,229) / 194,928.
- **2486**
  - Shares + options 24,744 → item 1.
  - Shareholder, related-party and investor loans → items 4 and 7. Under rule A this is right: the balance sheet on p. 37 shows current 3,492 and non-current 1,386.
  - Financial-bodies loans → item 5. Under rule A this is right: the p. 37 balance sheet shows only a current line, 22,988 / 30,634 / 23,721, and no non-current one.
  - Bonds; interest → item 13.
  - Totals: 47,043 / 7,423 / 41,217 and 38,558 / 5,611 / (8,405) / (13) / 41,217.
- **2487**
  - Lines: short-term credit from banks and others, net (2,268)/7,167/2,108; long-term loans; bonds; `שינוי בהלוואות לבעלי שליטה` 29/–/(2,129) → item 5 (net, no term); lease.
  - Q2 adds convertible bonds of 17,272 → item 3.
  - (\*) interest paid is disclosed only in appendix A: Q1 p. 33 5,936/4,639/22,717 and Q2 p. 36 13,533/10,187/7,597/5,548/22,717. It is recorded as printed (positive) with the canonical note `... הסעיף לא צוין (לא בפעילות מימון)`, under convention 1.
- **2567**
  - All 9 lines are correct.
  - Total: 76,050 / 21,130 / 67,292 / 11,908 / 63,577.
  - `קבלת הלוואות מחברות כלולות, צדדים קשורים ואחרים` 2,532/565 → item 5. The p. 49 balance sheet has no non-current liability for these loans; the only non-current lines are the long-term shareholder loans of 123,500, bonds of 74,144, leases of 376 and deferred taxes.
  - `פרעון הלוואות לזמן קצר מבעלי מניות` (47,394) → item 5. See M2 for the capital-note interest line.

**Restated flags.**
- All 77 columns are `לא`.
- In 421, 531, 1068 and 1974, restatement markers appear only on operating/investing values of the 2025 comparatives. The column headers carry no marker and no financing line is marked.
- Under convention 10 each such column therefore has a column note instead of `(מוצג מחדש)`. I checked the placement on the image for 1974 Q2: the `(*)` markers appear only in the 3M Apr–Jun 2025 column, and the note sits in column I, which is that column.

---

## 3. Cross-report checks (C2/C3) and master

**C3.** I recomputed C3 from the workbooks for the 9 two-report companies: FY-2025, Q1 against Q2, gives 0 difference for every item and for the total.

**C2.** I recomputed C2: Q1 3M equals Q2 6M minus Q2 3M, for both 2026 and 2025. The results:
- **0** for 200, 421, 1039, 1068, 1974 and 2487.
- **531, 3M-2026:** Q2 gives 42,212 against 42,211 in Q1, a difference of 1. All of it is in item 5: 118,208 − 95,200 = 23,008 against 23,007, which is source rounding.
- **2458, 3M-2025:** a difference of 191, all in item 13. Q1 shows interest of (8,870); Q2 gives (22,148) − (13,469) = (8,679).
  - I verified the explanation on the images. Q1 shows `ריבית שהתקבלה` of 191 in operating for Q1-2025. Q2 shows `-` in that cell.
- **2486, 3M-2026:** a difference of −80 in item 13. Q1 shows (61); Q2 gives (3,846) − (3,705) = (141).
  - Q2 adds `ריבית שהתקבלה` in investing (205 and 104), which I saw on the image.
- **2486, 3M-2025:** a difference of −1,799, made up of:
  - item 4: −1,800 (4,205 against 2,405);
  - item 5: −1 (7,232 against 7,231);
  - item 13: +2.

**Master entries.** All of these are explained in the master `חסרים והערות`:
- 531: rows R82–R83;
- 2458: rows R135–R136;
- 2486: rows R148–R153;
- each one is also explained in the company workbook column notes.

**Other master `חסרים והערות` entries.** The sheet also lists:
- the missing Q1 for 2567 (R9);
- the source irregularities: 200 (R31), 421 (R34), 531 `280,68` (R37), 1974 (R52), 2486 (R63) and 2567 (R71).

**Master `נתונים`.** The rows equal the company workbooks exactly, and the T1 flag is correct (§1.4).

---

## 4. Minor observations (non-blocking)

### M1 — 1039 Q1 note: p. 12 is labelled as 38D

**Where:** the `מקורות` sheet, cell I4, and master `אינדקס קבצים` row R46.

**What it says:** "לא בשימוש (מחוץ להיקף): נתונים כספיים נפרדים (תקנה 38ד) – עמ' 12, 68–69".

**What the page is:** PDF p. 12 is a page of the board-of-directors report (printed p. 8, §6 `תזרים מזומנים שלילי מתמשך`). It only refers to the solo report; it is not 38D data. Only pp. 68–69 are the 38D statement.

**Impact:** text only.

**Suggested wording:** "עמ' 68–69 (עמ' 12 – דוח הדירקטוריון)".

### M2 — 2567 Q2: capital-note interest mapped to item 11

**The line:** line 1, `ריבית ששולמה על שטרי הון`: –/(1,183)/–/(588)/(2,379). It is mapped to item 11 (dividend to shareholders).

**Why item 11 is defensible:**
- The capital notes are equity.
- The FY-2025 equity statement on p. 52 debits `ריבית ששולמה על שטרי הון (2,379)` to retained earnings, so the payment is in substance a distribution to owners.
- This is consistent with convention 4, under which capital notes issued to owners are equity (item 1).

**The alternative:** item 13, by the wording of the line. The line note records this alternative.

**What Phase C should do:** check that any other `שטרי הון` interest line in other batches gets the same item.

**Cosmetic point:** the user-facing note refers to `ראו דוח האצווה`, which is a process file.

### M3 — Some zoom images have no blue/orange frames

**Where:** the zoom pages for 1039 Q2 (screenshots p. 7), 1974 Q1 (p. 3) and 1974 Q2 (p. 7).

**Why:** in these reports the header strip and the financing section are contiguous, so the renderer draws a single crop without frames.

**Why it is not an R7 breach:**
- The crop contains the title, the period headers, the units line and every financing line.
- It is legible at 220 DPI. I viewed the 1039 Q2 one at full size.
- The full-page images of these reports do carry both frames.
- R7.2 does not require frames.

### M4 — 200 has no note on the repaired glyphs

**The gap:** the 200 Q1/Q2 text layer has the same `ð`-for-`נ` glyph defect as 2486 Q1 and 2567, but the 200 workbook has no general note on the repaired text layer. The other two workbooks do.

**Impact:** none on the data. I checked every 200 label against the image, and all are correct.

---

## 5. Batch verdict

**PASS.**
- **Values:** all 19 reports, 77 columns, every line, total and (\*) value match the source images.
- **Mapping:** every mapping follows R3 and the conventions. Each non-obvious call carries a note, and I checked the evidence for the rule A calls on the balance sheets.
- **Checks:** C1 = 0 everywhere. Every C2 mismatch is genuine, explained and listed in the master, and C3 = 0.
- **Master:** the rows equal the company workbooks, and the T1 flags are correct.
- **Screenshots:** they are complete, correctly captioned and legible.
- **Quality gate:** the scoped `validate.py` gives `FAIL 0`.
- **Issues:** 4 minor, non-blocking observations (M1–M4).

Assisted-by: Anthropic:Claude Opus 5.5
