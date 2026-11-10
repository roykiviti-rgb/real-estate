# Builder report 1 — financing cash-flow breakdown 2026 (iteration 1: Phases A, B and C)

Goal: `goal.md` + `goal-amendment-1.md` (T1 `תקופה עיקרית`, T2 month range in 3-month labels) +
`goal-amendment-2.md` (T3 cancelled). Date: 2026-11-10. No git (none used anywhere).

**Result.** All 162 company×quarter reports of the 86 companies are extracted, mapped and verified against the
rendered report images. The deliverables are built in final mode (no draft marker):

- 86 company workbooks and 86 screenshots PDFs, two per company folder;
- the master `סיכום פירוט תזרים מימון 2026 - כל החברות.xlsx` in the WORKSPACE root: 5 sheets; `נתונים` 648 rows
  (= every report × period); `מיפוי שורות` 6,190 rows; `אינדקס קבצים` 178 rows; `חסרים והערות` 184 rows;
  `הסבר` 40 rows.

| gate | result |
|---|---|
| `checks.py` (all 86 companies) | C1 648 = 638 OK + 10 explained source inconsistencies; C2 152 = 125 OK + 27 explained; C3 1,216 OK; C2 per item 66 INFO (all explained); **unexplained mismatches: 0** |
| `validate.py` (full, no `--issuers`) | **PASS 36,751 · FAIL 0 · INFO 10** (the 10 explained C1 columns); exit 0 |
| Excel (COM, sequential, copies in TEMP), 87 workbooks | 87/87 open without repair; every sheet RTL; no error values; every formula recalculated to the value expected from the data; check rows 0 except the 10 explained source columns |
| `tool_integrity.py` | **CLEAN** (178 source PDFs byte-identical to the baseline; only the 2×86 outputs and the master are new; no stray files) |
| `tool_selftest.py` | PASS on 1484 Q1, 434 Q2, 121 Q2, 1532 Q1 and 2429 Q2 (21–23 assertions each, incl. the new Phase C keys) |

Contents: §1 how the run went (Phases A/B/C, the image-cap incident) · §2 script fixes S1–S7 · §3 cross-batch alignment
A–F · §4 what Phase C changed in the data · §5 checks C1/C2/C3 · §6 source irregularities, missing reports and source
decisions · §7 validate, Excel, integrity, hygiene · §8 known limitations · §9 per company × quarter (all 162 reports).

---------------------------------------------------------------------------------------------------------------

## 1. How the run went

### Phase A – pipeline (one Builder)

Phase A built a generic, parallel-safe pipeline in `GOAL DIR\work\`, documented in `PIPELINE.md` and summarised in
`builder-phaseA-report.md`:

- `fcf_extract.py` / `extract_report.py`: coordinate-based extraction of the consolidated statement, every column,
  the financing lines and the (*) candidates; separate (38D) and investee statements are excluded;
- `finalize_report.py`: auto and manual modes, driven by override files;
- `fcf_render.py`, `build_company.py`, `build_master.py`, `checks.py`, `validate.py`;
- review tools and `roles.json` (the role of every one of the 178 PDFs).

All 162 reports were extracted automatically. The pilot company 1618 was verified; the other 160 reports were
triaged for Phase B. Facts established in Phase A:

- every report has a usable text layer, 14 of them only after repairing a broken-font `נ`;
- 1829 Q1/Q2 use the `-01` file (the main file is an appraiser's letter);
- 2559 Q1 uses `-01`, the clean "דוח מתקן" (`-02` is the marked-up version, identical in the financing section);
- 2520's `-01` files are an investee's statements and are not used.

### Phase B – 8 parallel batch Builders (160 reports + the 1618 pilot)

Each batch verified its reports visually and fixed them only through `W\overrides\*.json`, following `PIPELINE.md` and
the orchestrator's `phaseB-conventions.md`. Each then built its company outputs without `--draft` and wrote
`W\batches\batch-N.md`.

**The image-cap incident.** The `view` tool displays at most 50 images per agent context. After that it still answers
"Viewed image file successfully", but adds "maximum number of images (50) reached" and shows nothing. Every batch hit
the cap in its first pass, roughly 10:14–11:00. Each batch noticed it, by itself or after the orchestrator's alert at
about 11:15. Each then redid its visual verification on images that were confirmed displayed, and rewrote the
`verified.method` of every affected report to cite only images actually seen. **No batch found a wrong value, sign,
column or item in the re-check.** Only texts were corrected: notes, a few labels, one header text.

| batch | issuers (reports) | first-pass views not displayed | how the batch re-verified |
|---|---|---|---|
| 1 | 486, 1096, 1338, 1490, 1532, 1797, 1829, 1969 (Q2), 2360, 2533 (19) | part of the first pass | Re-did the complete visual check on freshly rendered images. Used side-by-side or stacked montages of the same renders to stay under the cap. |
| 2 | 121, 155, 715, 1331 (Q2), 1644, 1722, 2392, 2418, 2474, 2521, 2557 (Q2) (20) | 10:13–11:01: the first pass of 121, 155, 715, 1331, 1644, 1722, 2392, 2418, 2474 Q2, 2521 and 2557 had rested on the text layer | Composite images, several pages per image: zoom pages digit by digit, the other statement pages and the (*) crops; 300/400-DPI zooms where needed. |
| 3 | 200, 421, 531, 1039, 1068, 1974, 2458, 2486, 2487, 2567 (Q2) (19) | 10:14–10:50, all 19 reports | All 19 re-verified on composites made from the screenshots PDFs (zoom and full pages) plus `tool_review` renders. Note claims were re-checked; wrong details in notes were corrected. |
| 4 | 111 (Q2), 400, 539, 1083, 1502, 1553, 1622, 2481, 2483, 2488, 2524 (21) | everything up to the 1553 pages (about 10:41) | Three layers: (1) read-only sub-agents with a fresh image budget, 21/21 PASS, which found one label defect (1622 Q1 `מ-Extell`), fixed; (2) the Builder's own composites (11:17–11:28); (3) automated C1–C3 and an interest/dividend text scan. |
| 5 | 341, 425, 1193, 1703 (Q2), 1928, 1979, 2371, 2385, 2456, 2478, 2520 (21) | 10:14–10:52: 19 of 21 reports had been text-only | Composites built from the source PDFs: (A) header strip + financing; (B) the other pages with the (*) lines boxed; (C/D) evidence crops for every note claim. Contact sheets of all screenshot pages. Notes corrected (one substantive: 341 Q2). |
| 6 | 373, 434, 444, 673 (Q2), 823, 1484, 1561, 1724, 2417, 2441, 2574 (Q2) (20) | roughly the first 70 minutes | Redone 11:10–11:25 on composites (≥ 220-DPI header strip + financing + (*) crops) and tiled overviews of every screenshots page. |
| 7 | 473, 1330, 1618 (pilot, rebuild check), 1903, 1905, 2384, 2386, 2429, 2449, 2522, 2559 (22) | the first pass of 473, 1330, 1903, 1905, 2384, 2386 | Financing and (*) crops of those six companies composed into a few large images and compared digit by digit. Screenshot PDFs checked on thumbnail sheets, with a numeric geometry check and a caption text check. 2429, 2449, 2522 and 2559 had been seen from the start. |
| 8 | 573, 584 (Q2), 719, 771, 1680, 2389, 2396, 2440, 2464, 2503, 2570 (Q2) (20) | 10:14–11:02, 15 reports | 11:18–11:36: one composite per company rendered from the source PDF. It shows the header strip with units, the financing section, every (*) line with its header strip, and every interest/dividend line found by a text scan. Screenshots checked on contact sheets; captions read back from the PDF text. |

The batches reported script problems as `SCRIPT-ISSUE`s and recorded every cross-company judgement call under
"mapping decisions". Both are dealt with in Phase C (§2 and §3).

### Phase C – assembly (this Builder)

1. **Snapshot first.** `W\data\*.json` (324 files) and `W\overrides\*.json` (192 files) were copied to
   `%TEMP%\fcf_run\_phaseC\snapshot\` before any change. At the end every final data file was diffed against the
   snapshot (§4).
2. **Scans of all 162 reports**, with read-only helper scripts kept in TEMP:
   - strips: periods and units inside every zoom and every (*) crop;
   - (*) lines: interest and dividends paid outside financing that are missing from the data;
   - label artefacts;
   - verbatim column headers;
   - context-page sections;
   - borrowing lines without a stated term, `נטו` lines, and the keyword groups of the mapping decisions;
   - balance-sheet classification of the lenders named in rule-A lines.
3. **Script changes** (§2), all generic. No data value was hand-edited; all data changes go through override keys.
4. **Visual confirmation of every change to a verified report.** This was delegated to read-only explore sub-agents,
   each with a fresh image budget, using composite images built from the source PDFs. Every sub-agent reported every
   image as displayed.

   | check | composites | what was confirmed |
   |---|---|---|
   | V1 – verbatim column headers | 26 | 252 header texts: 220 confirmed, 32 corrected exactly as the agents read them on the image |
   | V2a/V2b – evidence | 53 | balance-sheet classifications behind rule A; appendix titles behind the (*) sections; 10 claims about printed signs |
   | V3 – context pages | 24 | 48 pages: 41 sections confirmed, 7 corrected |
   | S1 – rebuilt screenshots (sample) | 23 | (*) crops of 823, 1330, 2522, 434, 444, 1680, 1532, 121, 1083; zooms of 823, 341, 2417; captions on full pages and context pages; all OK |

   I also viewed two crops myself: the 2396 Q1 header (the audit status is printed without parentheses) and 111 Q2
   p16 (the blank (*) cell that is now 0).
5. **Records.** Each changed report's override has a `verified.phaseC` entry: date, what changed, why, and which
   composites were seen. There are 122 such reports; 111 Q2 has a second entry for the blank → 0 cell.
6. **Rebuild and gates.** `finalize --all` (162/162), then `build --all` (86/86), the final master, `checks.py`,
   `validate.py`, the Excel check, `tool_integrity.py` and `tool_selftest.py` (§5, §7). `PIPELINE.md` was updated
   (§4, §7, new §14). `%TEMP%\fcf_run\` was deleted at the end.

---------------------------------------------------------------------------------------------------------------

## 2. Script fixes (generic)

| # | problem (reported by) | fix | result |
|---|---|---|---|
| S1 | `validate.py` AC6 failed every non-zero C1 column, even one with a documented source inconsistency (batches 1, 2, 4, 5, 6, 8: 715, 719, 2417, 2478, 2483, 2533) | AC6 now uses the same explanations as `checks.py` (`checks.explain`). An explained non-zero column passes and is printed as `INFO … (explained)`; an unexplained one still fails. No plug, and no printed value changed. The summary line is now `PASS n FAIL n INFO n`. | Full run: FAIL 0, INFO 10. These are the 10 C1 columns in §5, the same 10 that the master lists as `בדיקה לא אפס` and that Excel shows in the check rows. |
| S2 | Screenshot captions on pages with appendix (*) lines were generic or wrong; operating pages were captioned as holding (*) lines whenever the report had any (batches 1, 5, 6, 8) | `fcf_render.report_images` was rewritten so each caption describes its own page exactly. Image numbers are computed in advance. A page with (*) lines lists them (verbatim text and canonical section) and names the image that enlarges them. An operating/investing page without (*) lines says so, and points to the pages and images that hold them (or says they are presented in financing only). A page with neither is captioned `לידיעה`. The legend says whether the units are in the blue box or in the zoom. The section names come from `context_sections`, which were scanned in all 162 reports; 47 pages in 43 reports were corrected (V3). | All 86 PDFs rebuilt; sample S1 checked visually (23 pages, all OK). |
| S3 | Red (*) crops on appendix pages lacked the column headers (batches 6, 7, 8; worked around by hand with header boxes) | New `star_crop_plan`. Above the (*) lines it puts, in order of preference: (1) the page's own header strip; (2) the page's own column-header block above the (*) line; (3) the report's header strip. A units line from the same page or another statement page is composed in when missing, with a dashed separator between parts. | Strip test on all 162 reports: 0 failures with the final geometry, and still 0 after removing every header box the batches had set, so the fix does not depend on them. Before the fix only 823 Q1 p61 still lacked units. `validate.py` AC10 now checks all 85 (*) crops: PASS. |
| S4 | Units line missing from the zoom (batches 5, 6) | New `zoom_header_parts`: the zoom's header strip is extended down to the units line, or a units part is added from the same or another statement page. `crop_texts()` returns the text inside every clip region. | `validate.py` AC10 checks all 162 zooms (periods and units in the clip text): PASS. The mirrored `אלפי ח"ש` (584, 1928, 2441, 2559) is recognised. |
| S5 | Interest/dividend-paid lines outside financing missed by the extractor (batches 1, 2, 3, 5: `תשלומי ריבית`, appendix-only `ריבית ששולמה`, `ריבית ששולמה והוונה למלאי`) | Text scan of every statement page of all 162 reports, appendices included, for paid interest/dividends outside financing that are absent from the final data. | 39 candidate lines in 29 reports; **none is a missed (*) line**. They are receipts (`תקבולי ריבית`, dividends from associates, `חלוקות מתאגיד המטופל…`), non-cash reconciliation items (`הוצאות מימון…`, `ריבית והצמדה…`), appendix repeats of amounts already in financing (573: the appendix dividend equals items 11+12), or note text after the statement. The batches had already added the lines they reported (1193, 121, 1083, 444, 823, …). **No (*) line was added in Phase C.** The 87 (*) lines in 80 reports are all interest; no report presents dividends paid outside financing. |
| S6 | The verbatim column header (`כותרת העמודה בדוח (מילולית)`) was often polluted or truncated (batches 3, 4, 5, 7) | All 648 headers rebuilt from the page text: units and title fragments removed; letter spacing collapsed; headings shared by several columns (date, audit status) completed per column; audit parentheses kept exactly as printed. Manual fixes for 1680, 2441, 2503, 2574 and 771. Every proposal was checked on the image (V1); the 32 corrections were applied as read. | 243 columns in 79 reports changed through `columns.cN.header_text`. Five FY columns carry no audit status because none is printed (531 Q2, 771 Q1/Q2, 2483 Q1/Q2). |
| S7 | Label artefacts (`יפרעון`, `ð`, `ª`, U+F8FF, mirrored apostrophes/parentheses, labels glued to note references) | Scan of every final line text and (*) text. | No artefact left. Remaining flags are printed so: 121 Q2 (*) trailing colon (confirmed V2); 1083 `ב) …` list marker; Latin names in 1622 (`Extell Holdings I LLC`, `EB-5`); 2418 Q1 n2, a value row printed without a label, labelled from Q2 with an explicit bracket note (batch 2). |

Further generic changes:

- **`finalize_report.py`**
  - New item code `net_nci` (task C).
  - Canonical (*) sections only (task E). A non-canonical section stops finalize; the extractor's generic appendix
    label is mapped to "הסעיף לא צוין".
  - New keys `outside_sections` and `info_note_extra`. The (*) note is composed from the sections of the (*) lines;
    `info_notes` is rejected for a kind that has (*) lines.
  - Blank (*) values become 0 (111 Q2 c1 was `None`).
- **`build_company.py` / `build_master.py`**
  - `net_nci` shown as `6/14`; (*) mapping note.
  - New `הסבר` rows: net NCI lines, loans without a stated term, the (*) note wording, the (*) sign, the restated rule,
    and the check rule.
  - `חסרים והערות` lists every non-zero check column with its explanation (`בדיקה לא אפס`).
- **`validate.py`** – new AC7 check per (*) line: canonical section, numeric values, bbox present.
- **`tool_selftest.py`** – new part 2b covers the new keys and the rejection rules.

---------------------------------------------------------------------------------------------------------------

## 3. Cross-batch alignment (applied to all companies)

**A – gross receipt/repayment lines of borrowings with no stated term.** All 159 borrowing lines without a stated term
that were mapped to 4, 7 or `net_loans` were reviewed against the reporting company's own balance sheet and notes:

- lender's balance classified as current short-term credit only → **5**;
- long-term loans, including current maturities and project finance classified long-term → **4/7**;
- current and non-current balances for the same lenders, or not attributable → **4/7 with a note**.

Every balance-sheet claim was confirmed on the image (V2). The evidence (balance-sheet line and page) is in the line
note. The same line gets the same item in Q1 and Q2.

- **Changed to 5:**
  - 719: project loans, current only, Q1 and Q2;
  - 2392: loans from the parent and the controlling shareholder, Q1 and Q2;
  - 2486: loans from financial bodies (escort loans), current only, Q1 and Q2;
  - 2570 Q2: related-party loans, current only.
- **Kept 4/7 with evidence notes** (mixed or long-term balances): 1829 (bank and other credit, current + non-current),
  2392 (non-bank and other lenders), 2486 (shareholder/investor loans), 2557 Q2 (long-term related-party loans),
  1903 (other lenders, no separate balance-sheet line).
- **Kept 4/7 after review:** 486, 1797, 2360, 2389, 2396, 2503, 2533, 1974, the 2570 `מאחרים` lines, and the other
  lines of the companies above.
- ~~Kept 5 – gross `אשראי` lines, current: 1905, 2386, 2449.~~ **Corrected in iteration 2 (inspector M1/M2,
  orchestrator decision D2):** the gross lines of **1905** (n2/n3 `קבלת אשראי` / `פירעון אשראי`) and **2386** (n5/n6
  `קבלת/פירעון אשראי והלוואות מגופים פיננסיים`) are **4/7**: the same lenders have current **and** non-current balances
  (1905: current 485,967 / non-current 103,947 at 31.3.2026, a long-term 86.1M land loan due 26.3.2028, note 3;
  2386: current 56,850 / non-current 48,490 at 31.3.2026, a 43,424 January-2026 loan due by 30.6.2030, note 4א(1)),
  so the lines cannot be attributed to short-term credit only. The evidence is in the line notes. **2449** stays **5**:
  its `קבלת אשראי` line is effectively net (it shows a negative amount in 2025) – R3.
- **Already decided by the balance sheet in Phase B, kept:** batches 4, 5, 6 and 8, e.g. 111 Q2 (loans from others).

**B – lines presented net with no stated term → 5 (R3).**

- **1722** `הלוואות מתאגיד בנקאי, נטו`: here `נטו` means net of raising costs, with the repayments on a separate line,
  so it is a gross receipt and stays **4** (confirmed in the board report). 2533's analogous line is treated the same.
- **1490 and 1553:** the `נטו` lines state "לזמן ארוך", so they stay `net_loans`.
- **2429** `קבלת (פירעון) הלוואה מהמיעוט` (Q2, net, no term) → **5**. Its Q1 counterpart, the gross
  `קבלת הלוואה מהמיעוט`, is also put in **5**, so that the same line has the same item in both reports (C3 FY-2025
  111,453). This follows the precedents 1829, 2386, 2559 and 2385.

**C – net NCI transaction lines with mixed signs.** New resolver `net_nci`: per column, positive → 6, negative → 14.
It applies to **434** Q1 and Q2 line 11 (`עסקאות עם בעלי זכויות שאינן מקנות שליטה[, נטו]`), which had been 6 as a
whole. No other line nets NCI sales against NCI purchases; 373's NCI line is a pure purchase and stays 14. The resolver
is documented in the `הסבר` sheet, the mapping sheets (`6/14`) and `PIPELINE.md`.

**D – sign of the (*) info rows.**

- A row from a single source line keeps its printed sign (R5): a statement line in parentheses is negative; an
  appendix amount printed without parentheses is positive, as printed, and its note says "(ללא סוגריים)".
- A row combining components with different printed sign conventions (a statement line in parentheses plus an appendix
  amount printed positive) shows the appendix component with the payment sign, negative, so the sum means something.
  The note says so. This applies to **121** and **1083** (`ריבית ששולמה והוונה למלאי`).
- Explained in the master `הסבר` (row `(*) סימן`). All 10 printed-sign claims were confirmed on the image (V2b).
  **Iteration 2 (inspector M5, decision D3):** the mapping-sheet note of the sign-flipped (*) lines of 121 and 1083
  (Q1 and Q2) now states the sign remark itself (override flag `sign_flipped`, `L.STAR_SIGN_REMARK`).

**E – uniform (*) notes.** Every (*) line now carries one of five canonical sections. The info-row note is composed
from them (joined by ` + `), followed by an optional report-specific remark after `;`.

- `פעילות שוטפת` / `פעילות השקעה`: a line in the body of the statement.
- `גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת` (or `… השקעה`): the amount appears only in an appendix,
  and the report states the section, or the appendix clearly shows it (e.g. the appendix is the operating
  reconciliation). Used for 434, 823, 1561 and 2522 (Q1 and Q2), and for 1532 (entries 1–2 of Q1 and of Q2);
  **iteration 2 (inspector M3): also 2418 (Q1 and Q2)** – the report states that interest paid is classified in
  operating activities (Q1 p51 note 5 and p13 board report; Q2 p52 note 1ג and p14).
- `גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)`: otherwise. Used for 425, 444 (heading is
  only `מידע נוסף:`), 486, 573, 584, 1330, 1331, 1724, 2384, 2487, 1532 Q1 entry 3 (printed in non-cash
  appendix ג'), and the appendix components of 121 and 1083. (2418 was listed here in iteration 1 – corrected, see
  above.)
- 425 stays "not stated", because the report does not name the section.

Resulting distribution (after iteration 2): 50 lines operating, 14 appendix/operating, 23 appendix/not stated
(iteration 1: 50 / 12 / 25).

**F – other mapping decisions of the batch reports.** All cases were compared across batches. The following were
already consistent and were kept:

- loans from NCI holders → 4/7;
- shares + options/warrants unsplit → 1;
- own warrants on their own line → 2;
- options of a subsidiary or option exercise in a subsidiary → 6;
- purchase of NCI, including a put exercise → 14 (155);
- buy-back of own warrants → 9 (473);
- capital notes in equity → 1;
- interest on equity capital notes → 11 (2567);
- IPO price adjustment → 1 (2559);
- restated flag only when the column header or the financing values are marked, otherwise a column note.

Scan for lines with shares **and** options/warrants mapped to 2: 24 keyword lines. Those in 2 are option or warrant
**exercises** (121, 373, 1979 …); 2389's bonds + options line is in 3, its dominant instrument. **No line combines a
share issue with options and sits in 2.** No other inconsistency between batches was found.

### Lines changed by the alignment (generated from the final data vs the snapshot)

**Item changes (16 lines):**

| report | line | text | item before → after | values | note (final) |
|---|---|---|---|---|---|
| 434 Q1 | n11 (auto 11) | עסקאות עם בעלי זכויות שאינן מקנות שליטה | 6 → 6/14 לפי סימן (per column: 6, 14, 6) | 91,887, -2,700, 21,876 | עסקאות עם בעלי זכויות שאינן מקנות שליטה – שורה נטו עם סימנים מעורבים: בכל עמודה לפי הסימן (net_nci) – סכום חיובי → סעיף 6 (3 חודשים 2026 ושנת 2025: בעיקר מכירת מניות בחברות בנות ללא איבוד שליטה; בדוח על השינויים בהון לרבעון 1/2026: קרן הון 39,704 וזשמ"ש 52,183), סכום שלילי → סעיף 14 (3 חודשים 2025: תשלום נטו לזשמ"ש – רכישת זכויות). בשלב B סווגה כולה לסעיף 6; שונתה בשלב C (פתרון net_nci) |
| 434 Q2 | n11 (auto 11) | עסקאות עם בעלי זכויות שאינן מקנות שליטה, נטו | 6 → 6/14 לפי סימן (per column: 6, 14, 14, 14, 6) | 91,199, -7,960, -689, -5,260, 21,876 | עסקאות עם בעלי זכויות שאינן מקנות שליטה, נטו – שורה נטו עם סימנים מעורבים: בכל עמודה לפי הסימן (net_nci) – סכום חיובי → סעיף 6 (6 חודשים 2026 ושנת 2025: בעיקר מכירת מניות בחברות בנות ללא איבוד שליטה), סכום שלילי → סעיף 14 (6 חודשים 2025, אפריל–יוני 2026 ו-2025: תשלומים נטו לזשמ"ש – רכישת זכויות; ברבעון 2/2026 קרן הון 1,876 וזשמ"ש (2,565)). בשלב B סווגה כולה לסעיף 6; שונתה בשלב C (פתרון net_nci), כמו בדוח Q1 |
| 719 Q1 | n6 (auto 6) | קבלת הלוואת בגין פרויקטים בביצוע | 4 → 5 (per column: 5, 5, 5) | 5,740, 2,773, 20,189 | קבלת הלוואות בגין פרויקטים בביצוע (מימון פרויקטים) – שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורים): אשראי/הלוואות המסווגים כהתחייבות שוטפת – סעיף 5. במאזן המאוחד 'הלוואות בגין פרויקטים בביצוע' מוצגות בהתחייבויות השוטפות בלבד בכל המועדים (מימון פרויקטים המסווג כשוטף) ואין יתרה לא שוטפת (עמ' 32). הנוסח 'הלוואת' כמודפס. שונתה מסעיף 4 בשלב C (יישור בין-חברתי) |
| 719 Q1 | n7 (auto 7) | פרעון הלוואה בגין פרויקטים בביצוע | 7 → 5 (per column: 5, 5, 5) | -14,013, 0, -47,637 | פירעון הלוואות בגין פרויקטים בביצוע – אותן הלוואות (התחייבות שוטפת) – סעיף 5, כמו שורת הקבלה (שונתה מסעיף 7 בשלב C) |
| 719 Q2 | n6 (auto 6) | קבלת הלוואת בגין פרויקטים בביצוע | 4 → 5 (per column: 5, 5, 5, 5, 5) | 6,428, 6,364, 688, 3,591, 20,189 | קבלת הלוואות בגין פרויקטים בביצוע (מימון פרויקטים) – שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורים): אשראי/הלוואות המסווגים כהתחייבות שוטפת – סעיף 5. במאזן המאוחד 'הלוואות בגין פרויקטים בביצוע' מוצגות בהתחייבויות השוטפות בלבד בכל המועדים (מימון פרויקטים המסווג כשוטף) ואין יתרה לא שוטפת (עמ' 111). הנוסח 'הלוואת' כמודפס. שונתה מסעיף 4 בשלב C, כמו בדוח Q1 |
| 719 Q2 | n7 (auto 7) | פרעון הלוואה בגין פרויקטים בביצוע | 7 → 5 (per column: 5, 5, 5, 5, 5) | -14,013, -11,896, 0, -11,896, -47,637 | פירעון הלוואות בגין פרויקטים בביצוע – אותן הלוואות (התחייבות שוטפת) – סעיף 5, כמו שורת הקבלה ובדוח Q1 (שונתה מסעיף 7 בשלב C) |
| 2392 Q1 | n2 (auto 2) | הלוואות שהתקבלו מחברה האם ומבעל השליטה | 4 → 5 (per column: 5, 5, 5) | 0, 9,000, 16,800 | הלוואות שהתקבלו מהחברה האם ומבעל השליטה – שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורים): אשראי/הלוואות המסווגים כהתחייבות שוטפת – סעיף 5. במאזן המאוחד (עמ' 46) 'הלוואות מחברה האם ומבעל השליטה' מוצגות בהתחייבויות השוטפות בלבד (יתרה רק במועד ההשוואה של 2025) ואין יתרה לא שוטפת. בשלב A–B סווגה לסעיף 4; שונתה בשלב C (יישור בין-חברתי). ב-2025 הומרו ההלוואות לשטר הון ולפרמיה (נספח, עמ' 50) |
| 2392 Q2 | n2 (auto 3) | הלוואות שהתקבלו מחברה האם ומבעל השליטה | 4 → 5 (per column: 5, 5, 5, 5, 5) | 0, 16,800, 0, 7,800, 16,800 | הלוואות שהתקבלו מהחברה האם ומבעל השליטה – שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורים): אשראי/הלוואות המסווגים כהתחייבות שוטפת – סעיף 5. במאזן המאוחד (עמ' 46) 'הלוואות מחברה האם ומבעל השליטה' מוצגות בהתחייבויות השוטפות בלבד (יתרה רק במועד ההשוואה של 2025) ואין יתרה לא שוטפת. בשלב A–B סווגה לסעיף 4; שונתה בשלב C (יישור בין-חברתי), כמו בדוח Q1 |
| 2429 Q1 | n7 (auto 7) | קבלת הלוואה מהמיעוט | 4 → 5 (per column: 5, 5, 5) | 1,676, 31,746, 111,453 | קבלת הלוואה מבעלי זכויות שאינן מקנות שליטה (מיעוט) בחברות מוחזקות – הלוואה, לא השקעה הונית. בדוח Q2 2026 אותה שורה מוצגת נטו ('קבלת (פירעון) הלוואה מהמיעוט') ללא ציון תקופה, ולכן לפי R3 (שורת הלוואות נטו ללא ציון תקופה) – סעיף 5; כדי שאותה שורה תסווג זהה בשני הדוחות (C3, שנת 2025: 111,453) היא סווגה לסעיף 5 גם כאן (כמו 1829, 2386, 2559). במאזן ההלוואה מוצגת בעיקר כהתחייבות לא שוטפת. שונתה מסעיף 4 בשלב C |
| 2429 Q2 | n7 (auto 7) | קבלת (פירעון) הלוואה מהמיעוט | 4/7 לפי סימן → 5 (per column: 5, 5, 5, 5, 5) | 6,117, 68,786, 4,441, 37,040, 111,453 | קבלת (פירעון) הלוואה מהמיעוט – שורת הלוואה מבעלי זכויות שאינן מקנות שליטה המוצגת נטו (קבלה/פירעון) ללא ציון תקופה – סעיף 5 לפי R3 ('שורת הלוואות נטו ללא ציון תקופה'), כמו 2385; הלוואה ולא השקעה הונית (לא סעיף 6). במאזן ההלוואה מוצגת בעיקר כהתחייבות לא שוטפת. שונתה מ-net_loans (4/7) בשלב C; אותה שורה בדוח Q1 – סעיף 5 |
| 2486 Q1 | n4 (auto 4) | קבלת הלוואה מגופים פיננסים | 4 → 5 (per column: 5, 5, 5) | 0, 7,232, 13,620 | קבלת הלוואה מגופים פיננסים – הלוואות ליווי לפרויקטים מגופים חוץ-בנקאיים; שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורים): אשראי/הלוואות המסווגים כהתחייבות שוטפת – סעיף 5. במאזן המאוחד 'הלוואות מגופים פיננסיים' (הלוואות ליווי לפרויקטים) מוצגות בהתחייבויות השוטפות בלבד בכל המועדים ואין יתרה לא שוטפת (עמ' 37). שונתה מסעיף 4 בשלב C (יישור בין-חברתי) |
| 2486 Q1 | n5 (auto 5) | פירעון הלוואות מגופים פיננסיים | 7 → 5 (per column: 5, 5, 5) | -1,100, 0, -9,441 | פירעון הלוואות מגופים פיננסיים – אותן הלוואות ליווי (התחייבות שוטפת) – סעיף 5, כמו שורת הקבלה (שונתה מסעיף 7 בשלב C) |
| 2486 Q2 | n4 (auto 4) | קבלת הלוואה מגופים פיננסים | 4 → 5 (per column: 5, 5, 5, 5, 5) | 0, 9,020, 0, 1,789, 13,620 | קבלת הלוואה מגופים פיננסים – הלוואות ליווי לפרויקטים מגופים חוץ-בנקאיים; שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורים): אשראי/הלוואות המסווגים כהתחייבות שוטפת – סעיף 5. במאזן המאוחד 'הלוואות מגופים פיננסיים' (הלוואות ליווי לפרויקטים) מוצגות בהתחייבויות השוטפות בלבד בכל המועדים ואין יתרה לא שוטפת (עמ' 39). שונתה מסעיף 4 בשלב C, כמו בדוח Q1 |
| 2486 Q2 | n5 (auto 5) | פירעון הלוואות מגופים פיננסיים | 7 → 5 (per column: 5, 5, 5, 5, 5) | -5,800, 0, -4,700, 0, -9,441 | פירעון הלוואות מגופים פיננסיים – אותן הלוואות ליווי (התחייבות שוטפת) – סעיף 5, כמו שורת הקבלה ובדוח Q1 (שונתה מסעיף 7 בשלב C) |
| 2570 Q2 | n4 (auto 4) | קבלת הלוואות מצדדים קשורים | 4 → 5 (per column: 5, 5, 5, 5, 5) | 0, 2, 0, 0, 0 | קבלת הלוואות מצדדים קשורים – שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורים): אשראי/הלוואות המסווגים כהתחייבות שוטפת – סעיף 5. במאזן המאוחד (עמ' 37) 'הלוואות מצדדים קשורים' מוצגות בהתחייבויות השוטפות בלבד (ההתחייבויות הלא שוטפות כוללות 'הלוואות מחברות קשורות' ו'שטרי הון מצדדים קשורים' – פריטים אחרים); ביאור 6: פירעון קרן וריבית לפי הסכם עם צד קשור. שונתה מסעיף 4 בשלב C |
| 2570 Q2 | n5 (auto 5) | פירעון הלוואות מצדדים קשורים | 7 → 5 (per column: 5, 5, 5, 5, 5) | -456, -1,518, -405, -201, -3,052 | פירעון הלוואות מצדדים קשורים – אותן הלוואות (התחייבות שוטפת) – סעיף 5, כמו שורת הקבלה. במאזן המאוחד (עמ' 37) 'הלוואות מצדדים קשורים' מוצגות בהתחייבויות השוטפות בלבד (ההתחייבויות הלא שוטפות כוללות 'הלוואות מחברות קשורות' ו'שטרי הון מצדדים קשורים' – פריטים אחרים); ביאור 6: פירעון קרן וריבית לפי הסכם עם צד קשור. שונתה מסעיף 7 בשלב C |

**Evidence / wording notes changed without an item change (14 lines):**

| report | line | text | item | note (final) |
|---|---|---|---|---|
| 1829 Q1 | n4 | קבלת הלוואות מתאגידים בנקאיים ואחרים | 4 | קבלת הלוואות מתאגידים בנקאיים ואחרים – שורת תקבול ברוטו ללא ציון תקופה (כולל מלווים אחרים). במאזן (עמ' 60 בדוח Q2) 'אשראי מתאגידים בנקאיים ומוסדות פיננסיים' מוצג גם בהתחייבויות השוטפות וגם בלא שוטפות – לפי כלל היישור A: יתרות שוטפות ולא שוטפות של אותם מלווים – לא ניתן לשייך לאשראי לזמן קצר בלבד, ולכן סעיף 4/7 |
| 1829 Q2 | n4 | קבלת הלוואות מתאגידים בנקאיים ואחרים | 4 | קבלת הלוואות מתאגידים בנקאיים ואחרים – שורת תקבול ברוטו ללא ציון תקופה (כולל מלווים אחרים). במאזן (עמ' 60) 'אשראי מתאגידים בנקאיים ומוסדות פיננסיים' מוצג גם בהתחייבויות השוטפות (165,796 ליום 30.6.2026) וגם בלא שוטפות (17,640) – לפי כלל היישור A: יתרות שוטפות ולא שוטפות של אותם מלווים – לא ניתן לשייך לאשראי לזמן קצר בלבד, ולכן סעיף 4/7 |
| 1903 Q1 | n7 | קבלת הלוואות מאחרים | 4 | קבלת הלוואות מגורמים אחרים (לא בנקאיים), ללא ציון תקופה, שורת תקבול ברוטו; במאזן אין שורה נפרדת להלוואות מאחרים, ולכן לפי כלל היישור A לא ניתן לשייך – סעיף 4 (סכום זניח: 27) |
| 1903 Q2 | n7 | קבלת הלוואות מאחרים | 4 | קבלת הלוואות מגורמים אחרים (לא בנקאיים), ללא ציון תקופה, שורת תקבול ברוטו; במאזן אין שורה נפרדת להלוואות מאחרים, ולכן לפי כלל היישור A לא ניתן לשייך – סעיף 4 (סכום זניח: 27) |
| 2392 Q1 | n4 | הלוואות שהתקבלו מתאגידי מימון חוץ בנקאיים, אחרים וצדדים קשורים | 4 | הלוואות שהתקבלו מתאגידי מימון חוץ בנקאיים, אחרים וצדדים קשורים – שורת קבלה ברוטו ללא ציון תקופה (לפי דוח הדירקטוריון, ב-2026 בעיקר הלוואה מגורם הליווי בפרויקט Shir tower). במאזן (עמ' 46) 'אשראי מתאגידי מימון חוץ בנקאיים' שוטף, אך 'הלוואות מאחרים' כוללות הלוואות לזמן קצר וחלויות שוטפות של הלוואות לזמן ארוך (ובמועד ההשוואה גם יתרה לא שוטפת) – לפי כלל היישור A: יתרות שוטפות ולא שוטפות של אותם מלווים – לא ניתן לשייך לאש… |
| 2392 Q1 | n6 | פירעון הלוואות שהתקבלו מצדדים קשורים ואחרים | 7 | פירעון הלוואות שהתקבלו מצדדים קשורים ואחרים – שורת פירעון ברוטו; במאזן 'הלוואות מאחרים' כוללות הלוואות לזמן קצר וחלויות שוטפות של הלוואות לזמן ארוך – לפי כלל היישור A: יתרות שוטפות ולא שוטפות של אותם מלווים – לא ניתן לשייך לאשראי לזמן קצר בלבד, ולכן סעיף 4/7 |
| 2392 Q2 | n4 | הלוואות שהתקבלו מתאגידי מימון חוץ בנקאיים, אחרים וצדדים קשורים | 4 | הלוואות שהתקבלו מתאגידי מימון חוץ בנקאיים, אחרים וצדדים קשורים – שורת קבלה ברוטו ללא ציון תקופה (הלוואות ליווי/מימון פרויקטים). במאזן (עמ' 46) 'אשראי מתאגידי מימון חוץ בנקאיים' שוטף, אך 'הלוואות מאחרים' כוללות הלוואות לזמן קצר וחלויות שוטפות של הלוואות לזמן ארוך (ובמועד ההשוואה גם יתרה לא שוטפת) – לפי כלל היישור A: יתרות שוטפות ולא שוטפות של אותם מלווים – לא ניתן לשייך לאשראי לזמן קצר בלבד, ולכן סעיף 4/7; כמו בדוח Q1 |
| 2392 Q2 | n6 | פירעון הלוואות שהתקבלו מאחרים | 7 | פירעון הלוואות שהתקבלו מאחרים – שורת פירעון ברוטו; במאזן 'הלוואות מאחרים' כוללות הלוואות לזמן קצר וחלויות שוטפות של הלוואות לזמן ארוך – לפי כלל היישור A: יתרות שוטפות ולא שוטפות של אותם מלווים – לא ניתן לשייך לאשראי לזמן קצר בלבד, ולכן סעיף 4/7 (בדוח Q1: 'פירעון הלוואות שהתקבלו מצדדים קשורים ואחרים') |
| 2486 Q1 | n2 | קבלת הלוואה מבעלי מניות, צדדים קשורים ומשקיעים | 4 | קבלת הלוואה מבעלי מניות, צדדים קשורים ומשקיעים – הלוואות בעלים/משקיעים לפרויקטים; ללא ציון תקופה, ברוטו. במאזן (עמ' 37) 'הלוואות מבעלי מניות וצדדים קשורים' ו'הלוואות ממשקיעים' מוצגות גם בהתחייבויות השוטפות וגם בלא שוטפות – לפי כלל היישור A: יתרות שוטפות ולא שוטפות של אותם מלווים – לא ניתן לשייך לאשראי לזמן קצר בלבד, ולכן סעיף 4/7 |
| 2486 Q1 | n3 | פרעון הלוואות מבעלי מניות, צדדים קשורים ומשקיעים | 7 | פרעון הלוואות מבעלי מניות, צדדים קשורים ומשקיעים – ללא ציון תקופה, ברוטו; יתרות שוטפות ולא שוטפות במאזן – לפי כלל היישור A: יתרות שוטפות ולא שוטפות של אותם מלווים – לא ניתן לשייך לאשראי לזמן קצר בלבד, ולכן סעיף 4/7 |
| 2486 Q2 | n2 | קבלת הלוואה מבעלי מניות, צדדים קשורים ומשקיעים | 4 | קבלת הלוואה מבעלי מניות, צדדים קשורים ומשקיעים – הלוואות בעלים/משקיעים לפרויקטים; ללא ציון תקופה, ברוטו. במאזן (עמ' 39) 'הלוואות מבעלי מניות וצדדים קשורים' מוצגות גם בהתחייבויות השוטפות וגם בלא שוטפות – לפי כלל היישור A: יתרות שוטפות ולא שוטפות של אותם מלווים – לא ניתן לשייך לאשראי לזמן קצר בלבד, ולכן סעיף 4/7 |
| 2486 Q2 | n3 | פרעון הלוואות מבעלי מניות, צדדים קשורים ומשקיעים | 7 | פרעון הלוואות מבעלי מניות, צדדים קשורים ומשקיעים – ללא ציון תקופה, ברוטו; יתרות שוטפות ולא שוטפות במאזן – לפי כלל היישור A: יתרות שוטפות ולא שוטפות של אותם מלווים – לא ניתן לשייך לאשראי לזמן קצר בלבד, ולכן סעיף 4/7 |
| 2557 Q2 | n7 | קבלת הלוואות מבעלי מניות וצדדים קשורים | 4 | קבלת הלוואות מבעלי מניות וצדדים קשורים – שורת קבלה ברוטו ללא ציון תקופה; במאזן (עמ' 45) 'הלוואות לזמן ארוך מצדדים קשורים' מוצגות בהתחייבויות הלא שוטפות ואין יתרה שוטפת כזו – הלוואות לזמן ארוך – סעיף 4 (כלל היישור A) |
| 2557 Q2 | n8 | פירעון הלוואות מבעלי מניות וצדדים קשורים (ראה באור 7ט') | 7 | פירעון הלוואות מבעלי מניות וצדדים קשורים – שורת פירעון ברוטו; במאזן 'הלוואות לזמן ארוך מצדדים קשורים' בהתחייבויות הלא שוטפות – סעיף 7 (כלל היישור A) |

---------------------------------------------------------------------------------------------------------------

## 4. What Phase C changed in the data (diff against the snapshot)

- **Auto data (`*.auto.json`): unchanged.** `extract_report.py` was never re-run, so override keys still point to
  the same auto line numbers.
- **122 reports** have a Phase C override change, each recorded in `verified.phaseC`.
- **Amounts changed only where an item was reassigned:** 16 lines in 11 reports (§3: 434, 719, 2392, 2429, 2486,
  2570). Every printed value, total and column is unchanged; the reassignments change the item vectors only, and
  C1/C3 are still 0.
- The only value change: one blank (*) cell became 0 (111 Q2 c1, `None` → 0). The image shows the cell blank (p16
  crop, viewed by me); this is recorded in 111 Q2's `verified.phaseC`.
- **Other changes (texts only):**
  - line notes: 30 lines in 16 reports (A evidence; 434/2429 wording);
  - verbatim headers: 243 columns in 79 reports (S6);
  - context sections: 47 pages in 43 reports (S2);
  - (*) sections made canonical: 37 lines in 34 reports;
  - (*) note wording: 34 reports (E/D);
  - source-irregularity entries: 23 added, in 23 reports.
- Unintended changes: **none**. Every difference falls into one of the categories above, which were checked line by
  line in the diff listing.
- After the last script change (mapping the extractor's generic appendix label), `finalize --all` was re-run: 0 bytes
  changed in any data file.

---------------------------------------------------------------------------------------------------------------

## 5. Checks C1 / C2 / C3

C1 = items 1–14 + `אחר` − reported total, per column. C2 = the Q1 report's 3 months − (the Q2 report's 6 months − its
April–June), for 2026 and 2025. C3 = FY-2025 in the Q1 report vs the Q2 report, for the total and each item. Every
mismatch is listed in the master `חסרים והערות` with its explanation. The C1 columns also appear there as
`בדיקה לא אפס`.

(source: `checks_20261110-130724_22376`)

| check | comparisons | OK | mismatch (all explained) | INFO |
|---|---|---|---|---|
| C1 | 648 | 638 | 10 | 0 |
| C2 | 152 | 125 | 27 | 0 |
| C3 | 1216 | 1216 | 0 | 0 |
| C2-item | 66 | 0 | 0 | 66 |

Unexplained mismatches: **0**.

#### C1 – source statements that do not add up (values kept as printed, no plug): 10 mismatch(es)

| issuer | report | period | key | expected | actual | diff | explanation |
|---|---|---|---|---|---|---|---|
| 715 | Q1 2026 | 3 חודשים שהסתיימו ב-31.03.2025 | total | -144,405 | -144,406 | -1 | עיגול בדוח המקור: סכום שורות פעילות המימון המודפסות בעמודה (147,602- + 39,006 + 35,810- = 144,406-) שונה ב-1 מהסה"כ המודפס (144,405-). הספרות אומתו בהגדלה של 300 DPI; הנתונים נרשמו כפי שדווחו. |
| 715 | Q2 2026 | 6 חודשים שהסתיימו ב-30.06.2026 | total | 826,840 | 826,841 | 1 | עיגול בדוח המקור: סכום שורות פעילות המימון המודפסות בעמודה (826,841) שונה ב-1 מהסה"כ המודפס (826,840). הספרות אומתו בהגדלה של 300 DPI; הנתונים נרשמו כפי שדווחו. |
| 715 | Q2 2026 | 6 חודשים שהסתיימו ב-30.06.2025 | total | 5,657 | 5,656 | -1 | עיגול בדוח המקור: סכום שורות פעילות המימון המודפסות בעמודה (5,656) שונה ב-1 מהסה"כ המודפס (5,657). הספרות אומתו בהגדלה של 300 DPI; הנתונים נרשמו כפי שדווחו. |
| 715 | Q2 2026 | 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני) | total | -2,547 | -2,546 | 1 | עיגול בדוח המקור: סכום שורות פעילות המימון המודפסות בעמודה (2,546-) שונה ב-1 מהסה"כ המודפס (2,547-). הספרות אומתו בהגדלה של 300 DPI; הנתונים נרשמו כפי שדווחו. |
| 719 | Q1 2026 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 7,903 | 7,911 | 8 | חריגה בדוח המקור (נבדק על גבי תמונת הדוח): בדוח Q1 2026, עמודת 3 חודשים 2025, סכום שורות פעילות המימון כפי שהודפסו הוא 7,911, ואילו הסה"כ המודפס הוא 7,903 – הפרש 8. לפי דוח Q2 2026 (6 חודשים פחות 3 חודשים 2025) הסה"כ 7,903 מתאים לשורות, וההפרש נמצא בשורות ההלוואות לזמן ארוך: בדוח Q1 קבלה (392) ופירעון (27) – נטו (419), ולפי Q2 קבלה 0 ופירעון (427) – נטו (427). הנתונים נרשמו כפי שהודפסו. |
| 2417 | Q1 2026 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 45,943 | 45,942 | -1 | חריגה בדוח המקור (הפרש עיגול): בדוח Q1 2026 (עמ' 66) סכום שורות פעילות המימון בעמודת רבעון 1/2025 הוא 45,942 (19,619 − 87 − 10,000 + 31,410 + 5,000), ואילו הסה"כ המודפס 45,943. הערכים נבדקו בהגדלה של 300 DPI ונרשמו כמודפס. לפי דוח Q2 2026 האשראי לזמן קצר לרבעון זה הוא 19,620 (31,250 − 11,630) והסה"כ 45,943 – כלומר ההפרש נובע מעיגול שורת האשראי לזמן קצר בדוח Q1. |
| 2478 | Q2 2026 | 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני) | total | -76,053 | -76,054 | -1 | עיגול בדוח המקור: בעמודת 3 החודשים 4–6/2026 סכום השורות המודפסות 53,743- + 14,751 - 500 - 331 - 36,231 = 76,054- ואילו הסה"כ המודפס 76,053- (הפרש 1). הנתונים נרשמו כמודפס; הסה"כ תואם את 6 החודשים פחות רבעון 1 (349,085 - 425,138 = 76,053-). |
| 2483 | Q2 2026 | 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני) | total | -67,729 | -67,724 | 5 | חריגה בדוח המקור (נבדק מול התמונה): בדוח Q2 2026, בעמודת 3 החודשים אפריל–יוני 2026, סכום שורות פעילות המימון הוא (67,724) ואילו הסה"כ המודפס הוא (67,729) – הפרש 5. ההפרש ככל הנראה בשורת 'עליה באשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו': מודפס (18,489), ואילו לפי 6 חודשים (49,305) פחות רבעון 1 בדוח Q1 (30,811) הסכום הוא (18,494), ועם (18,494) גם סכום העמודה היה (67,729). הנתונים נרשמו כפי שהודפסו. |
| 2533 | Q1 2026 | שנה שהסתיימה ב-31.12.2025 | total | -267,919 | -268,919 | -1,000 | חריגה בדוח המקור (לא שגיאת חילוץ): בעמודת 2025 סכום שורות המימון המודפסות (180,270 - 360,311 - 23,440 + 65,529 - 130,967 = 268,919-) שונה מהסה"כ המודפס (267,919-) ב-1,000. בדוח על השינויים בהון 'השקעות בעלים' לשנת 2025 = 66,529 (לעומת 65,529 בשורת התזרים) – ההפרש זהה בדיוק, והסה"כ המודפס תואם את השינוי ביתרת המזומנים (306,836 - 44,808 - 267,919 = 5,891-). ככל הנראה טעות דפוס בשורת 'השקעות בעלים'; הנתונים נרשמו כפי שהודפסו (גם בדוח Q2). |
| 2533 | Q2 2026 | שנה שהסתיימה ב-31.12.2025 | total | -267,919 | -268,919 | -1,000 | חריגה בדוח המקור (לא שגיאת חילוץ): בעמודת 2025 סכום שורות המימון המודפסות (268,919-) שונה מהסה"כ המודפס (267,919-) ב-1,000 – כמו בדוח Q1. בדוח על השינויים בהון (עמוד 37) 'השקעות בעלים' לשנת 2025 = 66,529 לעומת 65,529 בשורת התזרים – ההפרש זהה בדיוק. ככל הנראה טעות דפוס בשורת 'השקעות בעלים'; הנתונים נרשמו כפי שהודפסו. |

#### C2 – Q1 3-month total vs Q2 (6 months − April–June): 27 mismatch(es)

| issuer | report | period | key | expected | actual | diff | explanation |
|---|---|---|---|---|---|---|---|
| 434 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | 488,956 | 488,955 | -1 | הפרש עיגול בדוחות המקור (לא שגיאת חילוץ): בדוח Q1 2026 הסה"כ לרבעון 1/2026 = 488,955; לפי דוח Q2 2026: 459,479 (6 חודשים) פחות (29,477) (אפריל–יוני) = 488,956 – הפרש 1. ברמת הסעיפים: אשראי לזמן קצר 3-, זשמ"ש 1+, חכירה 1-, חלוקות לזשמ"ש 2+ – הפרשי עיגול קטנים בין הדוחות. הערכים נבדקו מול התמונות ונרשמו כפי שדווחו. |
| 434 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | -31,885 | -31,886 | -1 | הפרש עיגול בדוחות המקור (לא שגיאת חילוץ): בדוח Q1 2026 הסה"כ לרבעון 1/2025 = (31,886); לפי דוח Q2 2026: (85,518) פחות (53,633) = (31,885) – הפרש 1. ברמת הסעיפים: הנפקת מניות 124,432 בדוח Q1 מול 124,431 בדוח Q2; הנפקת אג"ח בדוח Q2: 208,592 (6 חודשים) מול 208,591 (אפריל–יוני); אשראי לזמן קצר 77,421 מול 77,422 – הפרשי עיגול. הערכים נרשמו כפי שדווחו. |
| 531 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | 42,212 | 42,211 | -1 | הפרש עיגול של 1 בדוחות עצמם (לא שגיאת חילוץ): בדוח Q1 2026 הסה"כ לרבעון 1/2026 = 42,211, ולפי דוח Q2 2026: 101,757 (6 חודשים) פחות 59,545 (3 חודשים) = 42,212. ההפרש כולו בשורת 'קבלת אשראי מתאגידים בנקאיים, נטו' (סעיף 5): 118,208 − 95,200 = 23,008 לעומת 23,007 בדוח Q1; שאר השורות זהות. הנתונים נרשמו כפי שדווחו (נבדק מול התמונות של שני הדוחות). |
| 539 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 73,425 | 73,424 | -1 | הפרש עיגול של 1 בדוחות המקור (לא שגיאת חילוץ): בדוח Q1 2026 סך תזרים המימון לרבעון 1/2025 = 73,424, ואילו לפי דוח Q2 2026: 145,422 (6 חודשים) פחות 71,997 (3 חודשים) = 73,425. כל ההפרש בשורת 'קבלת (פירעון) אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' (סעיף 5): 48,266 בדוח Q1 מול 140,284 פחות 92,017 = 48,267 לפי דוח Q2. הנתונים נרשמו כפי שדווחו בכל דוח. |
| 1484 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | -4,066 | -4,089 | -23 | הבדל הצגה בין הדוחות (לא שגיאת חילוץ): בדוח Q1 2026 פעילות המימון לרבעון 1/2026 = (4,089); לפי דוח Q2 2026: 32,940 (6 חודשים) פחות 37,006 (אפריל–יוני) = (4,066) – הפרש 23, כולו בפירעון אגרות חוב: (34,210) בדוח Q1 מול (34,187) ל-6 חודשים בדוח Q2 (ובאפריל–יוני '-'). השינוי במזומנים זהה בשני הדוחות (19,660), כלומר ה-23 סווגו מחדש בדוח Q2 לפעילות אחרת (שוטפת: פער 58; השקעה: פער 35-). הנתונים נרשמו כפי שדווחו. |
| 1484 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | -7,695 | 15,617 | 23,312 | חריגה בדוח המקור (לא שגיאת חילוץ): בדוח Q1 2026 פעילות המימון לרבעון 1/2025 = 15,617; לפי דוח Q2 2026: 21,278 (6 חודשים 2025) פחות 28,973 (אפריל–יוני 2025) = (7,695) – הפרש 23,312 (אשראי לזמן קצר 22,834; הלוואות לזמן ארוך 604; אג"ח 126-). עמודות ההשוואה של 2025 בדוח Q2 אינן עקביות פנימית: בעמודת 6 החודשים סכום הפעילויות 10,572 מול שינוי במזומנים 11,542; בעמודת אפריל–יוני סכום הפעילויות 1,658 מול שינוי (8,862); יתרת המזומנים ליום 30.6.2025 היא 46,381 בעמודה אחת ו-55,050 באחרת; יתרת הפתיחה ליום 1.4.2025 (63,912) שונה מיתרת הסגירה ליום 31.3.2025 בדוח Q1 (65,179). פעילות ההשקעה לרבעון 1/2025 זהה בשני הדוחות (64,451). הנתונים נרשמו כפי שדווחו בכל דוח. |
| 1490 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 25,893 | 25,891 | -2 | עיגול בדוחות המקור (לא שגיאת חילוץ): הסה"כ ברבעון 1/2025 בדוח Q1 2026 = 25,891, ולפי דוח Q2 2026: 25,633 (6 חודשים) פחות (260) (3 חודשים) = 25,893 – הפרש 2, המורכב מ-1 בריבית ששולמה ((1,248) מול (3,900)-(2,653)=(1,247)) ו-1 בתשלומים בגין חכירה ((570) מול (1,086)-(517)=(569)). הנתונים נרשמו כפי שדווחו בכל דוח. |
| 1724 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | -94,344 | -94,345 | -1 | הפרש עיגול בדוחות המקור (לא שגיאת חילוץ): בדוח Q1 2026 הסה"כ לרבעון 1/2026 = (94,345); לפי דוח Q2 2026: (202,364) פחות (108,020) = (94,344) – הפרש 1, כולו בפירעון ההלוואות (סעיף 7): (13,835) בדוח Q1 מול (64,354) פחות (50,520) = (13,834). כמודפס. |
| 1724 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 105,743 | 105,742 | -1 | הפרש עיגול בדוחות המקור (לא שגיאת חילוץ): בדוח Q1 2026 הסה"כ לרבעון 1/2025 = 105,742; לפי דוח Q2 2026: 72,767 פחות (32,976) = 105,743 – הפרש 1, כולו בקבלת הלוואות לזמן ארוך (סעיף 4): 37,595 בדוח Q1 מול (5,470 − 5,470) + (38,229 − 633) = 37,596 לפי דוח Q2 (בדוח Q2 הסכומים של 2025 מוצגים בשורה נפרדת 'קבלת הלוואות לזמן ארוך מתאגידים בנקאיים'). כמודפס. |
| 1979 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | 16,358 | 11,486 | -4,872 | הבדל בין הדוחות עצמם (לא שגיאת חילוץ): בדוח Q1 2026 סך פעילות המימון לרבעון 1/2026 = 11,486, ואילו לפי דוח Q2 2026: 41,513 (6 חודשים) פחות 25,155 (3 חודשים) = 16,358 – הפרש 4,872 = קבלת הלוואות 3,384 + ריבית ששולמה 1,488 (ראו C2 לפי סעיף). דוח Q2 מציג גם פעילות שוטפת והשקעה שונות לרבעון 1/2026 ויתרת מזומנים ליום 31.3.2026 של 87,561 (בדוח Q1: 87,549). הדוחות אינם מסבירים את השינוי; הנתונים נרשמו כפי שדווחו בכל דוח. |
| 1979 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 252,994 | 256,726 | 3,732 | הבדל בין הדוחות עצמם (לא שגיאת חילוץ): בדוח Q1 2026 סך פעילות המימון לרבעון 1/2025 = 256,726, ואילו לפי דוח Q2 2026: 295,508 (6 חודשים) פחות 42,514 (3 חודשים) = 252,994 – הפרש 3,732, כולו בריבית ששולמה: בדוח Q1 (29,521), לפי דוח Q2 (61,485) פחות (28,232) = (33,253). באותו סכום שונה הפעילות השוטפת (בדוח Q1 (155,339), לפי דוח Q2 (151,944) פחות (337) = (151,607)) – הבדל סיווג של ריבית ששולמה בין שוטפת למימון. הדוחות אינם מסבירים את השינוי; הנתונים נרשמו כפי שדווחו. |
| 2360 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | 293,344 | 293,345 | 1 | עיגול בדוחות המקור (לא שגיאת חילוץ): הסה"כ ברבעון 1/2026 בדוח Q1 2026 = 293,345, ולפי דוח Q2 2026: 285,327 (6 חודשים) פחות (8,017) (3 חודשים) = 293,344 – הפרש 1, כולו בריבית ששולמה ((31,154) בדוח Q1 מול (120,468)-(89,313)=(31,155)). כל שאר השורות זהות. הנתונים נרשמו כפי שדווחו בכל דוח. |
| 2386 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 32,012 | 32,013 | 1 | הפרש עיגול בדוחות המקור (1 אלפי ש"ח): בדוח Q1 2026 סה"כ פעילות המימון ברבעון 1/2025 = 32,013, ואילו לפי דוח Q2 2026: 18,189 (6 חודשים) פחות (13,823) (אפריל–יוני) = 32,012. ההפרש כולו בשורות הריבית ששולמה (ראו C2 סעיף 13); כל שאר השורות זהות. הנתונים נרשמו כפי שדווחו. |
| 2396 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | 18,462 | 18,461 | -1 | הפרש עיגול של 1 בדוחות המקור (לא שגיאת חילוץ): סה"כ פעילות המימון ברבעון 1/2026 בדוח Q1 = 18,461, ולפי דוח Q2 (20,449-) פחות (38,911-) = 18,462. ההפרש בשורת 'פרעון הלוואות מתאגידים בנקאיים': (67) בדוח Q1 מול (136) פחות (70) = (66) בדוח Q2; כל שאר השורות זהות. הנתונים נרשמו כפי שהודפסו. |
| 2396 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | -1,830 | -1,831 | -1 | הפרש עיגול של 1 בדוחות המקור (לא שגיאת חילוץ): סה"כ פעילות המימון ברבעון 1/2025 בדוח Q1 = (1,831), ולפי דוח Q2: 2,529 פחות 4,359 = (1,830). ההפרש בשורת 'פירעון הלוואות מבעלי עניין ואחרים': (8,638) בדוח Q1 מול (23,606) פחות (14,969) = (8,637) בדוח Q2; כל שאר השורות זהות. הנתונים נרשמו כפי שהודפסו. |
| 2417 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | 18,643 | 18,644 | 1 | הפרש עיגול בדוחות המקור (לא שגיאת חילוץ): בדוח Q1 2026 הסה"כ לרבעון 1/2026 = 18,644; לפי דוח Q2 2026: 28,260 (6 חודשים) פחות 9,617 (אפריל–יוני) = 18,643 – הפרש 1, כולו באשראי לזמן קצר: 13,556 בדוח Q1 מול 44,995 − 31,440 = 13,555. כמודפס. |
| 2458 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 149,498 | 149,307 | -191 | הבדל הצגה בין הדוחות (לא שגיאת חילוץ; נבדק מול התמונות): בדוח Q1 2026 הסה"כ לרבעון 1/2025 = 149,307, ולפי דוח Q2 2026: 125,269 (6 חודשים) פחות (24,229) (3 חודשים) = 149,498 – הפרש 191, כולו בשורת 'ריבית ששולמה' (סעיף 13): (8,870) בדוח Q1 לעומת (22,148) − (13,469) = (8,679) בדוח Q2.  בדוח Q1 מוצגת בפעילות השוטפת 'ריבית שהתקבלה' 191 לרבעון 1/2025, ובדוח Q2 שורה זו ריקה ב-2025 ותזרים הפעילות השוטפת לרבעון 1/2025 נמוך ב-191 (פעילות ההשקעה והשינוי במזומנים זהים) – ההפרש מתיישב עם הצגת הריבית שהתקבלה בקיזוז מהריבית ששולמה בפעילות המימון בדוח Q2 (סיווג שונה בין שוטפת למימון). הנתונים נרשמו כפי שדווחו בכל דוח. |
| 2474 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 5,647 | 5,648 | 1 | עיגול בדוחות המקור (±1): בדוח Q1 2026 הסה"כ לרבעון 1/2025 = 5,648, ואילו לפי דוח Q2 2026: 101,303 (6 חודשים 2025) פחות 95,656 (3 חודשים אפריל–יוני 2025) = 5,647. ההפרש נובע כולו מריבית ששולמה: (2,176) בדוח Q1 מול (4,719) פחות (2,542) = (2,177) לפי דוח Q2. הספרות אומתו בתמונות שני הדוחות; הנתונים נרשמו כפי שדווחו. |
| 2478 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 61,413 | 75,953 | 14,540 | הבדל בין הדוחות עצמם (לא שגיאת חילוץ): בדוח Q1 2026 סך פעילות המימון לרבעון 1/2025 = 75,953, ואילו לפי דוח Q2 2026: 281,707 (6 חודשים) פחות 220,294 (3 חודשים) = 61,413 – הפרש 14,540 = הלוואות נטו 13,223 (88,177 לעומת 74,954) + ריבית ששולמה 1,317 ((11,177) לעומת (12,494)). השינוי במזומנים לרבעון זהה בשני הדוחות ((21,449)); ההפרש מתקזז בפעילות השוטפת (14,298-: (45,643) לעומת (31,345)) ובפעילות ההשקעה (242-: (51,759) לעומת (51,517)). בדוח Q2 שתי שורות בפעילות השוטפת מסומנות '(*) הוצג מחדש', ומספרי ההשוואה לשנת 2025 כוללים את שינוי המבנה תחת שליטה משותפת (ביאור 1ו' בדוח Q1); הדוחות אינם מפרטים את השינוי בפעילות המימון. הנתונים נרשמו כפי שדווחו בכל דוח. |
| 2483 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 86,479 | 86,478 | -1 | הפרש עיגול של 1 בדוחות המקור: סך תזרים המימון לרבעון 1/2025 = 86,478 בדוח Q1, ואילו לפי דוח Q2: 178,093 (6 חודשים) פחות 91,614 (3 חודשים) = 86,479. כל ההפרש בסעיף 5 (ראו C2-item). הנתונים נרשמו כפי שדווחו. |
| 2486 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | 46,963 | 47,043 | 80 | הבדל הצגה בין הדוחות (לא שגיאת חילוץ; נבדק מול התמונות): בדוח Q1 2026 הסה"כ לרבעון 1/2026 = 47,043, ולפי דוח Q2 2026: 38,558 (6 חודשים) פחות (8,405) (3 חודשים) = 46,963 – הפרש 80, כולו בשורת 'ריבית ששולמה' (סעיף 13): (61) בדוח Q1 לעומת (3,846) − (3,705) = (141) בדוח Q2. דוח Q2 מוסיף בפעילות ההשקעה שורת 'ריבית שהתקבלה' (205 ל-6 חודשים, 104 ל-3 חודשים → 101 לרבעון 1) שאינה מופיעה בדוח Q1, ופעילות ההשקעה לרבעון 1/2026 לפיו גבוהה ב-79 (ועוד 1 בשוטפת); השינוי במזומנים לרבעון זהה בשני הדוחות (34,302). כלומר בדוח Q2 הוצגו הריבית ששולמה והריבית שהתקבלה ברוטו. הנתונים נרשמו כפי שדווחו בכל דוח. |
| 2486 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 5,624 | 7,423 | 1,799 | הבדל הצגה בין הדוחות בהשוואתיים 2025 (לא שגיאת חילוץ; נבדק מול התמונות): בדוח Q1 2026 הסה"כ לרבעון 1/2025 = 7,423, ולפי דוח Q2 2026: 5,611 (6 חודשים) פחות (13) (3 חודשים) = 5,624 – הפרש 1,799: 'קבלת הלוואה מבעלי מניות, צדדים קשורים ומשקיעים' 4,205 בדוח Q1 לעומת 2,405 בדוח Q2 (1,800), 'קבלת הלוואה מגופים פיננסים' 7,232 לעומת 9,020 − 1,789 = 7,231 (1), 'ריבית ששולמה' (535) לעומת (2,335) − (1,802) = (533) (−2). באותה תקופה פעילות ההשקעה לפי דוח Q2 גבוהה ב-1,902 (שורת 'שינוי בהשקעה והלוואות בחברות כלולות ועסקאות משותפות': (1,903) בדוח Q1, '-' בדוח Q2) והשוטפת נמוכה ב-103; השינוי במזומנים זהה ((3,116)). כל דוח מתיישב פנימית; הנתונים נרשמו כפי שדווחו. |
| 2488 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | 11,679 | 11,677 | -2 | הבדל בין הדוחות (לא שגיאת חילוץ; הערכים אומתו מול התמונות): סך תזרים המימון לרבעון 1/2025 = 11,677 בדוח Q1, ואילו לפי דוח Q2: 18,641 (6 חודשים) פחות 6,962 (3 חודשים) = 11,679 – הפרש 2: הלוואות מצדדים קשורים נטו 3,020 לפי דוח Q2 מול 2,989 בדוח Q1 (+31), ריבית ששולמה (725) לפי דוח Q2 מול (695) בדוח Q1 (−30), ואשראי לזמן קצר 9,843 מול 9,842 (+1, עיגול). כלומר סיווג מחדש של כ-30 בין ריבית להלוואות מצדדים קשורים בדוח Q2 + עיגול. הנתונים נרשמו כפי שדווחו בכל דוח. |
| 2503 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | 8,314 | 6,521 | -1,793 | הבדל סיווג בין הדוחות (לא שגיאת חילוץ; נבדק שורה-שורה בשני הדוחות): סה"כ פעילות המימון ברבעון 1/2026 בדוח Q1 = 6,521, ולפי דוח Q2 (36,849 פחות 28,535) = 8,314 – הפרש 1,793, כולו בשורת 'ריבית ששולמה': (3,231) בדוח Q1 מול (9,170) פחות (7,732) = (1,438) בדוח Q2. באותו סכום שונה הסעיף 'עלייה בספקים וזכאים ויתרות זכות' בפעילות השוטפת (11,454 בדוח Q1 מול 21,137 פחות 11,476 = 9,661 בדוח Q2), ושאר השורות זהות, כך שהשינוי במזומנים זהה. הדוחות אינם מסבירים את ההבדל (ככל הנראה ריבית שנרשמה כשולמה בדוח Q1 וסווגה בדוח Q2 כהתחייבות שטרם נפרעה). הנתונים נרשמו כפי שדווחו בכל דוח. |
| 2521 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | 14,921 | 14,920 | -1 | עיגול בדוחות המקור: בדוח Q1 2026 הסה"כ לרבעון 1/2026 = 14,920, ואילו לפי דוח Q2 2026: 3,088 (6 חודשים) פחות (11,833) (3 חודשים אפריל–יוני) = 14,921 – הפרש 1, המורכב מ-1+ בסעיף 4 ו-2- בסעיף 13 (ראו C2-item). הספרות אומתו בתמונות שני הדוחות; הנתונים נרשמו כפי שדווחו. |
| 2524 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2026 | total | 185,630 | 185,631 | 1 | הפרש עיגול של 1 בדוחות המקור: סך תזרים המימון לרבעון 1/2026 = 185,631 בדוח Q1, ואילו לפי דוח Q2: 178,115 (6 חודשים) פחות (7,515) (3 חודשים) = 185,630. כל ההפרש בשורת 'אשראי מתאגידים בנקאיים, נטו' (סעיף 5): 81,274 בדוח Q1 מול 103,458 − 22,185 = 81,273 לפי דוח Q2. הנתונים נרשמו כפי שדווחו. |
| 2559 | Q1 vs Q2 | 3 חודשים שהסתיימו ב-31.03.2025 | total | -23,895 | -23,897 | -2 | הפרשי עיגול בדוחות המקור (2 אלפי ש"ח): בדוח Q1 2026 (המתקן) סה"כ פעילות המימון ברבעון 1/2025 = (23,897), ואילו לפי דוח Q2 2026: (23,541) (6 חודשים) פחות 354 (אפריל–יוני) = (23,895). ההפרש מורכב מ-1 בפירעון הלוואות לזמן ארוך ((1,451) מול (1,450)) ו-1 באשראי לזמן קצר נטו (4,528 מול 4,529); שאר השורות זהות. הנתונים נרשמו כפי שדווחו. |

#### C3 – FY-2025 in the Q1 vs the Q2 report: 0 mismatch(es)

None.

#### C2 per item (informational): 66 row(s), each with its explanation

| issuer | period | item | expected | actual | diff | explanation |
|---|---|---|---|---|---|---|
| 434 | 3 חודשים שהסתיימו ב-31.03.2026 | 5 | 56,501 | 56,498 | -3 | אשראי מתאגידים בנקאיים, נטו: בדוח Q1 – 56,498; לפי דוח Q2: 71,567 פחות 15,066 = 56,501 – הפרש 3 בדוחות המקור (עיגול/סיווג), כמודפס. |
| 434 | 3 חודשים שהסתיימו ב-31.03.2026 | 6 | 120,655 | 121,345 | 690 | זשמ"ש (סעיף 6): בדוח Q1 – 91,887 (עסקאות עם זשמ"ש, חיובי) + 29,458 (השקעות הוניות) = 121,345; לפי דוח Q2: 6 חודשים 91,199 + 33,654 = 124,853 פחות אפריל–יוני 4,198 (השקעות הוניות; שורת העסקאות באפריל–יוני שלילית (689) ומשויכת לפי סימן לסעיף 14) = 120,655 – הפרש 690: 689 = התשלום לזשמ"ש של אפריל–יוני 2026 שקוזז בשורת העסקאות הנטו… |
| 434 | 3 חודשים שהסתיימו ב-31.03.2026 | 10 | -7,637 | -7,638 | -1 | פירעון התחייבות בגין חכירה: בדוח Q1 – (7,638); לפי דוח Q2: (16,193) פחות (8,556) = (7,637) – הפרש 1 (עיגול), כמודפס. |
| 434 | 3 חודשים שהסתיימו ב-31.03.2026 | 12 | -164 | -162 | 2 | חלוקות לזכויות שאינן מקנות שליטה: בדוח Q1 – (162); לפי דוח Q2: (355) פחות (191) = (164) – הפרש 2 בדוחות המקור, כמודפס. |
| 434 | 3 חודשים שהסתיימו ב-31.03.2026 | 14 | 689 | 0 | -689 | רכישת זכויות (סעיף 14): בדוח Q1 – 0; לפי דוח Q2: 0 (6 חודשים, השורה הנטו חיובית → סעיף 6) פחות (689) (אפריל–יוני, שלילי → סעיף 14) = 689 – הפרש הנובע משיוך השורה הנטו 'עסקאות עם בעלי זכויות שאינן מקנות שליטה' לפי הסימן בכל עמודה (net_nci); ראו גם C2-item 6. הסכומים נרשמו כמודפס. |
| 434 | 3 חודשים שהסתיימו ב-31.03.2025 | 1 | 124,431 | 124,432 | 1 | הנפקת מניות, נטו: בדוח Q1 – 124,432 (כך גם בדוח על השינויים בהון לרבעון 1/2025); בדוח Q2 – 124,431 ל-6 חודשים 2025 (וכך גם בשנת 2025 בשני הדוחות) – הפרש עיגול 1, כמודפס. |
| 434 | 3 חודשים שהסתיימו ב-31.03.2025 | 3 | 1 | 0 | -1 | הנפקת אגרות חוב: בדוח Q2 – 208,592 ל-6 חודשים 2025 ו-208,591 לאפריל–יוני 2025, ולכן הנגזר לרבעון 1/2025 = 1; בדוח Q1 – '-' – הפרש עיגול 1, כמודפס. |
| 434 | 3 חודשים שהסתיימו ב-31.03.2025 | 5 | 77,422 | 77,421 | -1 | אשראי מתאגידים בנקאיים, נטו: בדוח Q1 – 77,421; לפי דוח Q2: 106,327 פחות 28,905 = 77,422 – הפרש עיגול 1, כמודפס. |
| 531 | 3 חודשים שהסתיימו ב-31.03.2026 | 5 | 23,008 | 23,007 | -1 | הפרש עיגול של 1 בדוחות עצמם: 'קבלת אשראי מתאגידים בנקאיים, נטו' לפי דוח Q2 (118,208 − 95,200 = 23,008) לעומת 23,007 בדוח Q1 2026; הנתונים נרשמו כפי שדווחו. |
| 539 | 3 חודשים שהסתיימו ב-31.03.2025 | 5 | 48,267 | 48,266 | -1 | הפרש עיגול של 1 בדוחות המקור: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו, לרבעון 1/2025 = 48,266 בדוח Q1 2026, ואילו לפי דוח Q2 2026: 140,284 (6 חודשים) פחות 92,017 (3 חודשים) = 48,267. הערכים נקראו נכון משני הדוחות (אומת מול התמונות). |
| 719 | 3 חודשים שהסתיימו ב-31.03.2025 | 4 | 0 | -392 | -392 | הבדל בין הדוחות (לא שגיאת חילוץ): בדוח Q1 2026 סעיף 4 ברבעון 1/2025 = (392) (שורת 'קבלת הלוואות לזמן ארוך' עם סכום שלילי מודפס); לפי דוח Q2 2026: 0. (מאז שלב C הלוואות בגין פרויקטים בביצוע משויכות לסעיף 5 בשני הדוחות ותואמות.) יחד עם סעיף 7 – ראו הסבר C1 לעמודה זו (הפרש 8 בדוח Q1 עצמו). |
| 719 | 3 חודשים שהסתיימו ב-31.03.2025 | 7 | -427 | -27 | 400 | הבדל בין הדוחות (לא שגיאת חילוץ): בדוח Q1 2026 פירעון הלוואות לזמן ארוך ברבעון 1/2025 = (27); לפי דוח Q2 2026: (515) פחות (88) = (427) – הפרש 400; יחד עם ההפרש בסעיף 4 ((392)) הנטו שונה ב-8, שהוא ההפרש בין סכום השורות לסה"כ המודפס בדוח Q1 (ראו הסבר C1). |
| 771 | 3 חודשים שהסתיימו ב-31.03.2025 | 4 | -195 | 0 | 195 | הבדל הצגה בין הדוחות (לא שגיאת חילוץ): בדוח Q1 2026 ברבעון 1/2025 קבלת הלוואות לזמן ארוך = 0 ופירעון (195) בשורה נפרדת; בדוח Q2 2026 אין שורת פירעון, וקבלת ההלוואות 133,480 (6 חודשים) פחות 133,675 (3 חודשים) = (195). הנטו והסה"כ זהים; הנתונים נרשמו כפי שדווחו. |
| 771 | 3 חודשים שהסתיימו ב-31.03.2025 | 7 | 0 | -195 | -195 | הבדל הצגה בין הדוחות (לא שגיאת חילוץ): בדוח Q1 2026 פירעון הלוואות לזמן ארוך ברבעון 1/2025 = (195); בדוח Q2 2026 אין שורת פירעון והסכום נכלל נטו בשורת קבלת ההלוואות (ראו סעיף 4). הנטו והסה"כ זהים. |
| 823 | 3 חודשים שהסתיימו ב-31.03.2025 | 4 | 279,927 | 279,928 | 1 | הפרש עיגול בין הדוחות (לא שגיאת חילוץ): קבלת הלוואות ברבעון 1/2025 – בדוח Q1 2026: 279,928; לפי דוח Q2 2026: 1,269,610 (6 חודשים) פחות 989,683 (אפריל–יוני) = 279,927 – הפרש 1, המקוזז בפירעון ההלוואות (סעיף 7); הסה"כ זהה (391,870). |
| 823 | 3 חודשים שהסתיימו ב-31.03.2025 | 7 | -344,692 | -344,693 | -1 | הפרש עיגול בין הדוחות (לא שגיאת חילוץ): פירעון הלוואות ברבעון 1/2025 – בדוח Q1 2026: (344,693); לפי דוח Q2 2026: (442,107) פחות (97,415) = (344,692) – הפרש 1, המקוזז בקבלת ההלוואות (סעיף 4); הסה"כ זהה. |
| 1484 | 3 חודשים שהסתיימו ב-31.03.2026 | 8 | -34,187 | -34,210 | -23 | פירעון אגרות חוב: (34,210) בדוח Q1 2026 מול (34,187) ל-6 חודשים בדוח Q2 2026 (אפריל–יוני '-') – הפרש 23 שסווג מחדש בדוח Q2 לפעילות אחרת; כמודפס. |
| 1484 | 3 חודשים שהסתיימו ב-31.03.2025 | 5 | 12,954 | 35,788 | 22,834 | אשראי לזמן קצר, נטו: בדוח Q1 2026 לרבעון 1/2025 – 35,788; לפי דוח Q2 2026: 42,846 פחות 29,892 = 12,954 – הפרש 22,834 הנובע מאי-העקביות של עמודות ההשוואה של 2025 בדוח Q2 (ראו C2 סה"כ); כמודפס. |
| 1484 | 3 חודשים שהסתיימו ב-31.03.2025 | 7 | -6,521 | -5,917 | 604 | פירעון הלוואות לזמן ארוך: בדוח Q1 2026 – (5,917); לפי דוח Q2 2026: (7,077) פחות (556) = (6,521) – הפרש 604, חלק מאי-העקביות של עמודות ההשוואה של 2025 בדוח Q2; כמודפס. |
| 1484 | 3 חודשים שהסתיימו ב-31.03.2025 | 8 | -13,536 | -13,662 | -126 | פירעון אגרות חוב: בדוח Q1 2026 – (13,662); לפי דוח Q2 2026: (13,536) פחות '-' = (13,536) – הפרש 126-, חלק מאי-העקביות של עמודות ההשוואה של 2025 בדוח Q2; כמודפס. |
| 1490 | 3 חודשים שהסתיימו ב-31.03.2026 | 10 | -739 | -740 | -1 | עיגול בדוחות המקור: תשלומים בגין חכירה ברבעון 1/2026 = (740) בדוח Q1, ולפי דוח Q2: (1,550) פחות (811) = (739) – הפרש 1, המקוזז בהפרש ההפוך בריבית ששולמה (סעיף 13); הסה"כ זהה (172,564). נרשם כפי שדווח. |
| 1490 | 3 חודשים שהסתיימו ב-31.03.2026 | 13 | -3,679 | -3,678 | 1 | עיגול בדוחות המקור: ריבית ששולמה ברבעון 1/2026 = (3,678) בדוח Q1, ולפי דוח Q2: (16,826) פחות (13,147) = (3,679) – הפרש 1, המקוזז בהפרש ההפוך בחכירה (סעיף 10); הסה"כ זהה (172,564). נרשם כפי שדווח. |
| 1490 | 3 חודשים שהסתיימו ב-31.03.2025 | 10 | -569 | -570 | -1 | עיגול בדוחות המקור: תשלומים בגין חכירה ברבעון 1/2025 = (570) בדוח Q1, ולפי דוח Q2: (1,086) פחות (517) = (569) – הפרש 1; נרשם כפי שדווח. |
| 1490 | 3 חודשים שהסתיימו ב-31.03.2025 | 13 | -1,247 | -1,248 | -1 | עיגול בדוחות המקור: ריבית ששולמה ברבעון 1/2025 = (1,248) בדוח Q1, ולפי דוח Q2: (3,900) פחות (2,653) = (1,247) – הפרש 1; נרשם כפי שדווח. |
| 1618 | 3 חודשים שהסתיימו ב-31.03.2025 | 4 | 261,280 | 262,547 | 1,267 | הבדל הצגה בין הדוחות (לא שגיאת חילוץ): בדוח Q1 2026 קבלת הלוואות לזמן ארוך ברבעון 1/2025 = 262,547, ואילו לפי דוח Q2 2026: 395,101 (6 חודשים) פחות 133,821 (3 חודשים) = 261,280 – הפרש 1,267. באותו סכום הוקטן גם הפירעון (ראו סעיף 7), כך שהנטו והסה"כ זהים (127,744). הנתונים נרשמו כפי שדווחו בכל דוח. |
| 1618 | 3 חודשים שהסתיימו ב-31.03.2025 | 7 | -159,550 | -160,817 | -1,267 | הבדל הצגה בין הדוחות (לא שגיאת חילוץ): בדוח Q1 2026 פירעון הלוואות לזמן ארוך ברבעון 1/2025 = (160,817), ואילו לפי דוח Q2 2026: (393,869) פחות (234,319) = (159,550) – הפרש 1,267, המקביל להפרש בסעיף 4; הנטו והסה"כ זהים. הנתונים נרשמו כפי שדווחו בכל דוח. |
| 1724 | 3 חודשים שהסתיימו ב-31.03.2026 | 7 | -13,834 | -13,835 | -1 | פירעון הלוואות מגוף מוסדי ותאגידים בנקאיים: (13,835) בדוח Q1 2026 מול (64,354) פחות (50,520) = (13,834) לפי דוח Q2 2026 – הפרש עיגול 1, כמודפס. |
| 1724 | 3 חודשים שהסתיימו ב-31.03.2025 | 4 | 37,596 | 37,595 | -1 | קבלת הלוואות לזמן ארוך: 37,595 בדוח Q1 2026 (שורת 'קבלת הלוואות מגוף מוסדי ותאגידים בנקאיים') מול 37,596 לפי דוח Q2 2026 (בעיקר שורת 'קבלת הלוואות לזמן ארוך מתאגידים בנקאיים': 38,229 פחות 633) – הפרש עיגול 1, כמודפס. |
| 1979 | 3 חודשים שהסתיימו ב-31.03.2026 | 4 | 80,317 | 76,933 | -3,384 | קבלת הלוואות מתאגידים בנקאיים ומוסדות פיננסיים לרבעון 1/2026: בדוח Q1 76,933; לפי דוח Q2: 186,814 פחות 106,497 = 80,317 – הפרש 3,384, הבדל בין הדוחות עצמם (חלק מהפרש הסה"כ 4,872). |
| 1979 | 3 חודשים שהסתיימו ב-31.03.2026 | 13 | -30,729 | -32,217 | -1,488 | ריבית ששולמה לרבעון 1/2026: בדוח Q1 (32,217); לפי דוח Q2: (53,516) פחות (22,787) = (30,729) – הפרש 1,488, הבדל בין הדוחות עצמם (חלק מהפרש הסה"כ 4,872). |
| 1979 | 3 חודשים שהסתיימו ב-31.03.2025 | 4 | 162,855 | 164,435 | 1,580 | קבלת הלוואות לרבעון 1/2025: בדוח Q1 164,435; לפי דוח Q2: 201,686 פחות 38,831 = 162,855 – הפרש 1,580, מקוזז בסעיף 7 (בדוח Q2 מוצג ברבעון 4–6/2025 פירעון הלוואות מצדדים קשורים ומאחרים (1,580) שאינו מופיע בעמודת 6 החודשים); הנטו זהה. |
| 1979 | 3 חודשים שהסתיימו ב-31.03.2025 | 7 | -113,079 | -114,659 | -1,580 | פירעון הלוואות לרבעון 1/2025: בדוח Q1 (114,659); לפי דוח Q2: (132,924) פחות (18,265) בשורת הבנקים = (114,659), ובשורת 'פירעון הלוואות מצדדים קשורים ומאחרים' 0 פחות (1,580) = 1,580 – הפרש 1,580 המקביל להפרש בסעיף 4; הנטו זהה. הבדל הצגה בין הדוחות. |
| 1979 | 3 חודשים שהסתיימו ב-31.03.2025 | 13 | -33,253 | -29,521 | 3,732 | ריבית ששולמה לרבעון 1/2025: בדוח Q1 (29,521); לפי דוח Q2: (61,485) פחות (28,232) = (33,253) – הפרש 3,732 = כל הפרש הסה"כ; מקוזז בפעילות השוטפת (הבדל סיווג בין הדוחות). |
| 2360 | 3 חודשים שהסתיימו ב-31.03.2026 | 13 | -31,155 | -31,154 | 1 | עיגול בדוחות המקור: ריבית ששולמה ברבעון 1/2026 = (31,154) בדוח Q1, ולפי דוח Q2: (120,468) פחות (89,313) = (31,155) – הפרש 1; נרשם כפי שדווח. |
| 2386 | 3 חודשים שהסתיימו ב-31.03.2025 | 13 | -1,728 | -1,727 | 1 | הפרש עיגול בדוחות המקור: בדוח Q1 2026 ריבית ששולמה ברבעון 1/2025 = (1,727), ואילו לפי דוח Q2 2026: [(2,479) + (863)] (6 חודשים) פחות [(751) + (863)] (אפריל–יוני) = (1,728). הנתונים נרשמו כפי שדווחו. |
| 2396 | 3 חודשים שהסתיימו ב-31.03.2026 | 7 | -920 | -921 | -1 | הפרש עיגול של 1 בשורת 'פרעון הלוואות מתאגידים בנקאיים' ((67) בדוח Q1 מול (66) הנגזר מדוח Q2) – ראו הסבר C2 לסה"כ. |
| 2396 | 3 חודשים שהסתיימו ב-31.03.2025 | 7 | -8,717 | -8,718 | -1 | הפרש עיגול של 1 בשורת 'פירעון הלוואות מבעלי עניין ואחרים' ((8,638) בדוח Q1 מול (8,637) הנגזר מדוח Q2) – ראו הסבר C2 לסה"כ. |
| 2417 | 3 חודשים שהסתיימו ב-31.03.2026 | 5 | 13,555 | 13,556 | 1 | אשראי לזמן קצר, נטו: 13,556 בדוח Q1 2026 מול 44,995 − 31,440 = 13,555 לפי דוח Q2 2026 – הפרש עיגול 1, כמודפס. |
| 2417 | 3 חודשים שהסתיימו ב-31.03.2025 | 5 | 19,620 | 19,619 | -1 | אשראי לזמן קצר, נטו: 19,619 בדוח Q1 2026 מול 31,250 − 11,630 = 19,620 לפי דוח Q2 2026 – הפרש עיגול 1 (גם מקור הפרש ה-C1 בעמודה זו בדוח Q1), כמודפס; הסה"כ (45,943) זהה בשני הדוחות. |
| 2418 | 3 חודשים שהסתיימו ב-31.03.2026 | 4 | 76,730 | 76,370 | -360 | הבדל בין הדוחות (לא שגיאת חילוץ; הספרות אומתו בתמונות שני הדוחות): בדוח Q1 2026 קבלת הלוואות לזמן ארוך ברבעון 1/2026 = 76,370, ואילו לפי דוח Q2 2026: 76,730 (6 חודשים) פחות 0 (3 חודשים) = 76,730 – הפרש 360, המקוזז בסעיף 5 (אשראי לזמן קצר); הנטו והסה"כ זהים (148,648). הנתונים נרשמו כפי שדווחו בכל דוח. |
| 2418 | 3 חודשים שהסתיימו ב-31.03.2026 | 5 | -31,542 | -31,182 | 360 | הבדל בין הדוחות (לא שגיאת חילוץ): בדוח Q1 2026 אשראי לזמן קצר ברבעון 1/2026 = (31,182), ואילו לפי דוח Q2 2026: (43,430) פחות (11,888) = (31,542) – הפרש 360, המקביל להפרש בסעיף 4; הנטו והסה"כ זהים. הנתונים נרשמו כפי שדווחו בכל דוח. |
| 2458 | 3 חודשים שהסתיימו ב-31.03.2025 | 13 | -8,679 | -8,870 | -191 | ריבית ששולמה לרבעון 1/2025: (8,870) בדוח Q1 2026 לעומת (8,679) לפי דוח Q2 2026 (6 חודשים (22,148) פחות 3 חודשים (13,469)) – הפרש 191 השווה ל'ריבית שהתקבלה' שהוצגה בפעילות השוטפת בדוח Q1 בלבד; ההפרש מתיישב עם קיזוז הריבית שהתקבלה מהריבית ששולמה בדוח Q2. הנתונים נרשמו כפי שדווחו. |
| 2474 | 3 חודשים שהסתיימו ב-31.03.2025 | 13 | -2,177 | -2,176 | 1 | עיגול בדוחות המקור (±1): ריבית ששולמה ברבעון 1/2025 – (2,176) בדוח Q1 2026 מול (4,719) פחות (2,542) = (2,177) לפי דוח Q2 2026. הנתונים נרשמו כפי שדווחו. |
| 2478 | 3 חודשים שהסתיימו ב-31.03.2026 | 13 | -14,603 | -14,604 | -1 | ריבית ששולמה לרבעון 1/2026: בדוח Q1 (14,604); לפי דוח Q2: (50,834) פחות (36,231) = (14,603) – הפרש 1, נובע מהעיגול בעמודת 3 החודשים 4–6/2026 בדוח Q2 (ראו C1); הסה"כ תואם. |
| 2478 | 3 חודשים שהסתיימו ב-31.03.2025 | 5 | 74,954 | 88,177 | 13,223 | הלוואות מתאגידים בנקאיים ואחרים, נטו לרבעון 1/2025: בדוח Q1 88,177; לפי דוח Q2: 126,888 פחות 51,934 = 74,954 – הפרש 13,223, חלק מהפרש הסה"כ 14,540 (הבדל בין הדוחות עצמם, ראו C2). |
| 2478 | 3 חודשים שהסתיימו ב-31.03.2025 | 13 | -12,494 | -11,177 | 1,317 | ריבית ששולמה לרבעון 1/2025: בדוח Q1 (11,177); לפי דוח Q2: (27,519) פחות (15,025) = (12,494) – הפרש 1,317, חלק מהפרש הסה"כ 14,540 (הבדל בין הדוחות עצמם, ראו C2). |
| 2483 | 3 חודשים שהסתיימו ב-31.03.2026 | 5 | -30,816 | -30,811 | 5 | אותה חריגה בדוח המקור: אשראי לזמן קצר לרבעון 1/2026 = (30,811) בדוח Q1, ואילו לפי דוח Q2: (49,305) פחות (18,489) = (30,816) – הפרש 5, הנובע מהערך (18,489) המודפס בעמודת 3 החודשים בדוח Q2 (ראו C1). הסה"כ (C2) תואם: (221,931) בשני החישובים. |
| 2483 | 3 חודשים שהסתיימו ב-31.03.2025 | 5 | 11,044 | 11,043 | -1 | הבדל הצגה + עיגול: בדוח Q1 לרבעון 1/2025 שורת האשראי לזמן קצר = 11,043 ואין סכום בשורת 'פירעון הלוואות מבעלי שליטה, נטו'; לפי דוח Q2 (6 חודשים פחות 3 חודשים): אשראי לזמן קצר 73,848 − 60,166 = 13,682 ופירעון הלוואות מבעלי שליטה (2,742) − (104) = (2,638), יחד 11,044 – שתי השורות בסעיף 5, ההפרש 1 הוא עיגול. |
| 2486 | 3 חודשים שהסתיימו ב-31.03.2026 | 13 | -141 | -61 | 80 | ריבית ששולמה לרבעון 1/2026: (61) בדוח Q1 2026 לעומת (141) לפי דוח Q2 2026 (6 חודשים (3,846) פחות 3 חודשים (3,705)) – הפרש 80; בדוח Q2 נוספה בפעילות ההשקעה 'ריבית שהתקבלה' (101 לרבעון 1) – הצגה ברוטו. הנתונים נרשמו כפי שדווחו. |
| 2486 | 3 חודשים שהסתיימו ב-31.03.2025 | 4 | 2,405 | 4,205 | 1,800 | קבלת הלוואות (סעיף 4) לרבעון 1/2025: 4,205 בדוח Q1 2026 ('קבלת הלוואה מבעלי מניות, צדדים קשורים ומשקיעים') לעומת 2,405 לפי דוח Q2 2026 – הפרש 1,800; הצגה שונה של השוואתיים 2025 בדוח Q2 (במקביל לשינוי בשורת ההשקעה בחברות כלולות בפעילות ההשקעה). הנתונים נרשמו כפי שדווחו. (מאז שלב C 'קבלת הלוואה מגופים פיננסים' משויכת לסעיף 5 – רא… |
| 2486 | 3 חודשים שהסתיימו ב-31.03.2025 | 5 | 7,231 | 7,232 | 1 | סעיף 5 לרבעון 1/2025: 'קבלת הלוואה מגופים פיננסים' 7,232 בדוח Q1 2026 לעומת 9,020 − 1,789 = 7,231 לפי דוח Q2 2026 – הפרש עיגול 1 בדוחות המקור. הנתונים נרשמו כפי שדווחו. |
| 2486 | 3 חודשים שהסתיימו ב-31.03.2025 | 13 | -533 | -535 | -2 | ריבית ששולמה לרבעון 1/2025: (535) בדוח Q1 2026 לעומת (533) לפי דוח Q2 2026 ((2,335) − (1,802)) – הפרש 2 (עיגול/הצגה בדוחות). הנתונים נרשמו כפי שדווחו. |
| 2488 | 3 חודשים שהסתיימו ב-31.03.2025 | 5 | 12,863 | 12,831 | -32 | סעיף 5 לרבעון 1/2025: 12,831 בדוח Q1 (אשראי לזמן קצר 9,842 + הלוואות מצדדים קשורים נטו 2,989) מול 12,863 לפי דוח Q2 (43,448 − 33,605 = 9,843; 2,957 − (63) = 3,020) – הפרש 32: 31 בהלוואות מצדדים קשורים (סיווג מחדש מול הריבית, ראו סעיף 13) ו-1 עיגול. |
| 2488 | 3 חודשים שהסתיימו ב-31.03.2025 | 13 | -725 | -695 | 30 | ריבית ששולמה לרבעון 1/2025: (695) בדוח Q1 מול (725) לפי דוח Q2 ((5,036) − (4,311)) – הפרש 30, מקביל להפרש בהלוואות מצדדים קשורים (סעיף 5); הבדל סיווג בין הדוחות. |
| 2503 | 3 חודשים שהסתיימו ב-31.03.2026 | 13 | -1,438 | -3,231 | -1,793 | ראו הסבר C2 לסה"כ: הריבית ששולמה ברבעון 1/2026 – (3,231) בדוח Q1 מול (1,438) לפי דוח Q2; ההפרש 1,793 מופיע בדוח Q2 בפעילות השוטפת (סעיף ספקים וזכאים). |
| 2503 | 3 חודשים שהסתיימו ב-31.03.2025 | 4 | 21,398 | 21,399 | 1 | הפרש עיגול של 1 בדוח Q1: תקבולים מהלוואות ממוסדות פיננסיים ואחרים ברבעון 1/2025 – 21,399 בדוח Q1 מול 44,331 פחות 22,933 = 21,398 לפי דוח Q2; מקוזז בהפרש של 1 בסעיף 11 (חלוקות לבעלים); הסה"כ זהה. |
| 2503 | 3 חודשים שהסתיימו ב-31.03.2025 | 11 | -3,649 | -3,650 | -1 | הפרש עיגול של 1 בדוח Q1: חלוקות לבעלים ברבעון 1/2025 – (1,141) בדוח Q1 (אך (1,140) בדוח על השינויים בהון ובעמודת השנה) מול (1,140) לפי דוח Q2; מקוזז בהפרש של 1 בסעיף 4; הסה"כ זהה. (סעיף 11 כולל גם את ההלוואה ללא מועד פירעון לבעל השליטה (2,509), זהה בשני הדוחות.) |
| 2521 | 3 חודשים שהסתיימו ב-31.03.2026 | 4 | 6,999 | 7,000 | 1 | עיגול בדוחות המקור: הלוואות שהתקבלו לזמן ארוך ברבעון 1/2026 – 7,000 בדוח Q1 2026 מול 9,449 פחות 2,450 = 6,999 לפי דוח Q2 2026. הנתונים נרשמו כפי שדווחו. |
| 2521 | 3 חודשים שהסתיימו ב-31.03.2026 | 13 | -8,026 | -8,028 | -2 | עיגול בדוחות המקור: ריבית ששולמה ברבעון 1/2026 – (7,551) + (477) ריבית חכירה = (8,028) בדוח Q1 2026, מול (21,462) פחות (13,913) = (7,549) + (948) פחות (471) = (477), סה"כ (8,026) לפי דוח Q2 2026 – הפרש 2 בשורת 'ריבית ששולמה'. הנתונים נרשמו כפי שדווחו. |
| 2522 | 3 חודשים שהסתיימו ב-31.03.2026 | 4 | 8,157 | 131,158 | 123,001 | הבדל הצגה בין הדוחות (לא שגיאת חילוץ): בדוח Q1 2026 קבלת הלוואות לזמן ארוך מתאגידים בנקאיים ברבעון 1/2026 = 131,158, ואילו לפי דוח Q2 2026: 8,158 (6 חודשים) פחות 1 (אפריל–יוני) = 8,157 – הפרש 123,001. באותו סכום קטן גם הפירעון (ראו סעיף 7), כך שהנטו והסה"כ זהים ((10,564)). הנתונים נרשמו כפי שדווחו בכל דוח. |
| 2522 | 3 חודשים שהסתיימו ב-31.03.2026 | 7 | -17,388 | -140,389 | -123,001 | הבדל הצגה בין הדוחות (לא שגיאת חילוץ): בדוח Q1 2026 פירעון הלוואות לזמן ארוך מתאגידים בנקאיים ברבעון 1/2026 = (140,389), ואילו לפי דוח Q2 2026: (18,118) פחות (730) = (17,388) – הפרש 123,001, המקביל להפרש בסעיף 4; הנטו והסה"כ זהים. הנתונים נרשמו כפי שדווחו בכל דוח. |
| 2524 | 3 חודשים שהסתיימו ב-31.03.2026 | 5 | 81,344 | 81,345 | 1 | הפרש עיגול של 1 בשורת 'אשראי מתאגידים בנקאיים, נטו': 81,274 בדוח Q1 מול 103,458 − 22,185 = 81,273 לפי דוח Q2 (שורת 'שינוי בהלוואה מאחרים' תואמת: 71 בשני החישובים). |
| 2559 | 3 חודשים שהסתיימו ב-31.03.2026 | 4 | 255,732 | 255,733 | 1 | הפרש עיגול בדוחות המקור: קבלת הלוואות לזמן ארוך מתאגידים בנקאיים ברבעון 1/2026 = 185,733 בדוח Q1 2026 מול 155,185 פחות (30,547) = 185,732 לפי דוח Q2 2026 (קבלת הלוואות מבעלי עניין זהה: 70,000). מתקזז עם הפרש של 1 בסעיף 5; הסה"כ זהה (242,118). הנתונים נרשמו כפי שדווחו. |
| 2559 | 3 חודשים שהסתיימו ב-31.03.2026 | 5 | 1,434 | 1,433 | -1 | הפרש עיגול בדוחות המקור: הלוואות מתאגידים מוחזקים ובעלי עניין, נטו ברבעון 1/2026 = 2,707 בדוח Q1 2026 מול 10,779 פחות 8,071 = 2,708 לפי דוח Q2 2026 (אשראי לזמן קצר נטו זהה: (1,274)). מתקזז עם ההפרש בסעיף 4; הסה"כ זהה. הנתונים נרשמו כפי שדווחו. |
| 2559 | 3 חודשים שהסתיימו ב-31.03.2025 | 5 | -7,732 | -7,733 | -1 | הפרש עיגול בדוחות המקור: אשראי לזמן קצר מתאגידים בנקאיים, נטו ברבעון 1/2025 = 4,528 בדוח Q1 2026 מול (10,221) פחות (14,750) = 4,529 לפי דוח Q2 2026; שורת ההלוואות מתאגידים מוחזקים ובעלי עניין זהה ((12,261)). הנתונים נרשמו כפי שדווחו. |
| 2559 | 3 חודשים שהסתיימו ב-31.03.2025 | 7 | -1,450 | -1,451 | -1 | הפרש עיגול בדוחות המקור: פירעון הלוואות לזמן ארוך מתאגידים בנקאיים ברבעון 1/2025 = (1,451) בדוח Q1 2026 מול (14,997) פחות (13,547) = (1,450) לפי דוח Q2 2026. הנתונים נרשמו כפי שדווחו. |

---------------------------------------------------------------------------------------------------------------

## 6. Source irregularities, missing reports, source decisions

**Missing Q1 reports (10; out of scope to download):** 111, 584, 673, 1331, 1703, 1969, 2557, 2567, 2570, 2574. Each
has a `דוח חסר` row in the master and a note in its workbook.

**Source decisions (`החלטת מקור`, 19 rows):**

- 1829 Q1/Q2: the `-01` full report is used; the main file is a one-page appraiser letter.
- 2559 Q1: `-01` (clean "דוח מתקן") is used; `-02` is the marked-up version; the main file is a 3-page excerpt.
- 2520 Q1/Q2: `-01` is an investee's statements, not used.
- 10 valuation/appraisal attachments, not used: 539, 771, 823, 1331, 1490, 1703, 2384, 2385, 2464, 2557.

The `אינדקס קבצים` sheet lists all 178 PDFs with their roles: 162 data sources, 10 appraisals, 3 letters/excerpts,
2 investee statements, 1 alternative version.

**Source irregularities (`חריגה בדוח המקור`):**

41 source irregularities (all also in the master `חסרים והערות`, kind `חריגה בדוח המקור`):

1. **200 Q2** (לוינסקי עופר בע"מ): שורת (*) 'ריבית ששולמה' (פעילות שוטפת) לרבעון 1/2026 לפי דוח זה: 5,600 − 2,921 = 2,679, לעומת (2,677) בדוח Q1 – הפרש 2 בין הדוחות (שורת מידע בלבד).
2. **341 Q2** (שדה נדל"ן-י.ש. בע"מ): בדוח על השינויים בהון זוקפו לזכויות שאינן מקנות שליטה 7,233 (6 חודשים 2026) / 4,447 (אפריל–יוני 2026) לעומת 8,239 / 5,453 בשורת 'תקבולים מגיוס משקיעים בניכוי הוצאות גיוס' בדוח תזרימי המזומנים – הפרש 1,006 שאינו מוסבר בדוח; הסכומים נרשמו כמודפס בדוח תזרימי המזומנים.
3. **400 Q2** (אחים דוניץ בע"מ): שורת (*) 'ריבית ששולמה' (פעילות שוטפת): 6 חודשים 2025 מודפס (20,099) לעומת (20,100) לפי רבעון 1 + אפריל–יוני – הפרש עיגול 1 (שורת מידע בלבד).
4. **421 Q2** (נתנאל גרופ בע"מ): שורת (*) 'ריבית ועמלות ששולמו' לרבעון 1/2025 לפי דוח זה: 63,383 − 36,011 = 27,372, לעומת 28,202 בדוח Q1 – הפרש 830 בין הדוחות (שורת מידע בלבד).
5. **434 Q2** (ישראל קנדה (ט.ר) בע"מ): שורת (*) – ריבית ששולמה לשנת 2025 בנספח ב': 378,178 בדוח זה (מסומן 'סווג מחדש') לעומת 341,471 בדוח Q1 (שורת מידע בלבד).
6. **473 Q1** (קבוצת עמוס לוזון יזמות ואנרגיה בע"מ): תווית שורה 13 מודפסת 'פינסיים' (טעות דפוס); נרשמה כמודפס.
7. **531 Q2** (בוני התיכון הנדסה אזרחית ותשתיות בע"מ): בדוח המודפס (עמוד 34) חסרה ספרה בשורת 'הנפקת אגרות חוב (בניכוי הוצאות הנפקה)', עמודת השנה שהסתיימה ב-31.12.2025: מודפס '280,68' (גם בשכבת הטקסט וגם בתמונה); לפי הסה"כ המדווח (308,912) ולפי דוח Q1 2026 הערך הוא 280,683 – נרשם 280,683.
8. **715 Q1** (אזורים-חברה להשקעות בפתוח ובבנין בע"מ): עמודת 3 החודשים שהסתיימו ב-31.03.2025: סכום שורות פעילות המימון המודפסות (144,406-) שונה ב-1 מהסה"כ המודפס (144,405-) – עיגול בדוח.
9. **715 Q2** (אזורים-חברה להשקעות בפתוח ובבנין בע"מ): עיגול בדוח: סכום שורות פעילות המימון המודפסות שונה ב-1 מהסה"כ המודפס בעמודות 6 חודשים 2026 (+1), 6 חודשים 2025 (1-) ו-3 חודשים אפריל–יוני 2026 (+1).
10. **719 Q1** (א.לוי השקעות ובנין בע"מ): בעמודת 3 חודשים שהסתיימו ב-31.03.2025 סכום שורות פעילות המימון המודפסות (7,911) שונה מהסה"כ המודפס (7,903) ב-8; לפי דוח Q2 2026 ההפרש נובע משורות ההלוואות לזמן ארוך (נטו (419) כאן מול (427) לפי Q2). הנתונים נרשמו כפי שהודפסו.
11. **719 Q2** (א.לוי השקעות ובנין בע"מ): שורת (*) 'ריבית ששולמה' לשנת 2025: (20,909) בדוח זה לעומת (20,910) בדוח Q1 – הפרש עיגול 1 (שורת מידע בלבד).
12. **1484 Q1** (מצלאוי חברה לבנין בע"מ): בשורת 'פירעון הלוואות לזמן ארוך' מודפס בעמודת שנת 2025 סכום חיובי 23,659 (ללא סוגריים); נרשם כמודפס (כך גם בדוח Q2).
13. **1484 Q2** (מצלאוי חברה לבנין בע"מ): דוח Q2 2026, עמודות ההשוואה לשנת 2025 בדוח תזרימי המזומנים (עמ' 35–36) אינן עקביות: (1) 6 חודשים 2025 – סכום הפעילויות השוטפת, ההשקעה והמימון 10,572 לעומת השינוי במזומנים המודפס 11,542 (פער 970); (2) אפריל–יוני 2025 – סכום הפעילויות 1,658 לעומת השינוי המודפס (8,862) (פער 10,520); (3) יתרת המזומנים ליום 30.6.2025: 46,381 בעמודת 6 החודשים מול 55,050 בעמודת 3 החודשים; יתרת הפתיחה ליום 1.4.2025 (63,912) שונה מיתרת הסגירה ליום 31.3.2025 בדוח Q1 2026 (65,179). כתוצאה מכך פעילות המימון לרבעון 1/2025 הנגזרת מדוח Q2 ((7,695)) שונה מזו שבדוח Q1 2026 (15,617) – פער 23,312 (בעיקר אשראי לזמן קצר 22,834). הנתונים נרשמו כפי שדווחו; שורות המימון עצמן מסתכמות לסה"כ המדווח בכל עמודה (C1 = 0).
14. **1484 Q2** (מצלאוי חברה לבנין בע"מ): בשורת 'פירעון הלוואות לזמן ארוך' מודפס בעמודת שנת 2025 סכום חיובי 23,659, ובשורת פירעון התחייבויות החכירה מודפסים סכומים חיוביים 1,854 (6 חודשים 2026) ו-2,342 (אפריל–יוני 2026); נרשמו כמודפס.
15. **1502 Q1** (מירלנד דיוולופמנט קורפריישן פי אל סי): סעיף המימון בדוח מורכב משורת הכותרת 'תזרימי מזומנים מפעילות מימון' עם '-' בכל העמודות וללא שורות פירוט; שורת הכותרת שימשה כסה"כ המדווח (0).
16. **1532 Q1** (גפן מגורים והתחדשות בע"מ): בנספח ג' (פעולות מהותיות שאינן במזומן, עמוד 34) מוצגת שורה 'ריבית ששולמה בגין חכירות' – 4 ברבעון 1/2025, בעוד שבנספח ב' (מידע נוסף לפעילות שוטפת, עמוד 33) התא של אותה תקופה ריק. בדוח Q2 2026 הסכום מוצג בנספח ב' (8 לשישה חודשים פחות 4 לשלושה חודשים = 4). נרשם בשורת (*) ריבית כמודפס, כחלק מהריבית שמחוץ לפעילות המימון.
17. **1532 Q1** (גפן מגורים והתחדשות בע"מ): הדוח מפנה ל'נספח ד'' (איחוד לראשונה) שאינו קיים בדוח; אין השפעה על פעילות המימון.
18. **1532 Q2** (גפן מגורים והתחדשות בע"מ): הדוח מפנה ל'נספח ד'' (איחוד לראשונה) שאינו קיים בדוח; אין השפעה על פעילות המימון.
19. **1622 Q2** (אקסטל לימיטד): בשורת 'החזר הון לבעלי זכויות שאינן מקנות שליטה' מודפס בעמודת אפריל–יוני 2026 סכום חיובי 1,500 (ללא סוגריים); נרשם כמודפס.
20. **1680 Q2** (לסיכו בע"מ): בעמודי הדוח המאוחד על תזרימי המזומנים (עמ' 36–38) הכותרת הרצה המודפסת היא 'באורים לדוחות הכספיים ביניים מאוחדים' במקום כותרת הדוח; התוכן נבדק והוא הדוח המאוחד על תזרימי המזומנים.
21. **1905 Q2** (גלעד מאי חברה להשקעות בניה ופיתוח בע"מ): בדוח Q2 2026: בשורות 'קבלת אשראי' / 'פירעון אשראי' עמודת 6 החודשים 2025 (282,312 / (280,000)) גבוהה מעמודת השנה 2025 (179,203 / (204,120)) – אשראי של 280,000 שהתקבל ונפרע ברבעון אפריל–יוני 2025 מוצג ברוטו בעמודות הרבעון וחצי השנה אך לא בעמודה השנתית (הצגה שונה בדוח המקור; סה"כ פעילות המימון אינו מושפע). הנתונים נרשמו כפי שדווחו.
22. **1974 Q2** (סופרין אחזקות בע"מ): בשורת התקבול 'קבלת הלוואות מתאגידים פיננסים' מודפס בעמודת 3 החודשים אפריל–יוני 2026 סכום שלילי (46) (6 חודשים 6,035 לעומת 6,081 ברבעון 1); נרשם כמודפס.
23. **2384 Q1** (קרסו נדל"ן בע"מ): דוח Q1 2026, עמודת 3 החודשים שהסתיימו ב-31.3.2025: הסכום 395,555 מודפס בשורת 'הנפקת מניות (בניכוי הוצאות הנפקה)' ובשורת 'הנפקת אגרות חוב' מודפס '-'. לפי דוח Q2 2026 (6 חודשים 2025: אג"ח 395,555, מניות 129,686; אפריל–יוני 2025: אג"ח -, מניות 129,686), לפי הנתונים הכספיים הנפרדים באותו דוח (עמוד 61: אג"ח 395,555, מניות -) ולפי הדוח על השינויים בהון (אין הנפקת מניות ברבעון 1/2025)   זו הנפקת אגרות חוב שהודפסה בשורה הלא נכונה. הסכום (כפי שהודפס, ללא שינוי ספרות) שויך בפירוט לשורת הנפקת אגרות החוב (סעיף 3) ובשורת הנפקת המניות נרשם 0 (מוסכמות שלב B §9); הסה"כ אינו מושפע.
24. **2417 Q1** (אנשי העיר מקבוצת רוטשטיין בע"מ): דוח Q1 2026, עמ' 66, עמודת 3 החודשים 2025: סכום שורות פעילות המימון 45,942 לעומת הסה"כ המודפס 45,943 (הפרש עיגול 1); הערכים נרשמו כמודפס.
25. **2418 Q1** (רם אדרת הנדסה אזרחית בע"מ): דוח Q1 2026, עמ' 46: עמודת השנה שהסתיימה ב-31.12.2025 בפעילות המימון מודפסת מוזזת שורה אחת ביחס לתוויות (7 ערכים מול 6 שורות; חסרה התווית 'פרעון אגרות חוב' ו-'-' בודד מודפס מתחת לקו). הערכים שויכו לשורות הנכונות לפי דוח Q2 ולפי חשבון הדוח (נוספה שורת פירעון אגרות חוב (85,000) בעמודת השנה); הסה"כ המודפס 70,825 ללא שינוי.
26. **2429 Q2** (לוזון רונסון אן.וי): בשורת פירעון התחייבויות בגין חכירות מודפס בעמודת אפריל–יוני 2026 סכום חיובי 53 ((2,223) ל-6 חודשים פחות (2,276) לרבעון 1); נרשם כמודפס.
27. **2456 Q1** (שמואל ברוך יזמות ובניה בע"מ): שורת 'קבלת הלוואות מצדדים קשורים' מודפסת בסכומים שליליים בלבד ((200) לרבעון 1/2025, (565) לשנת 2025) – בפועל תנועה נטו; נרשמה כמודפס (סעיף 5).
28. **2456 Q2** (שמואל ברוך יזמות ובניה בע"מ): שורת 'קבלת הלוואות מצדדים קשורים' מודפסת בסכומים שליליים בלבד – בפועל תנועה נטו; נרשמה כמודפס (סעיף 5).
29. **2464 Q2** (יוזמות - פיתוח נדל"ן בע"מ): בשורת 'תמורה מהנפקת אגרות חוב (בניכוי הוצאות הנפקה)' מודפס בעמודת אפריל–יוני 2025 סכום שלילי (573) (הוצאות הנפקה ששולמו ברבעון); נרשם כמודפס.
30. **2478 Q2** (רייסדור יזמות בע"מ): עמודת 3 החודשים שהסתיימו ב-30.06.2026 (אפריל–יוני): סכום שורות פעילות המימון המודפסות (76,054-) שונה מהסה"כ המודפס (76,053-) ב-1 – עיגול בדוח המקור; נרשם כמודפס.
31. **2478 Q2** (רייסדור יזמות בע"מ): בשורת 'פירעון התחייבות בגין חכירה' מודפס בעמודת 3 החודשים אפריל–יוני 2025 סכום חיובי 186 (ללא סוגריים) – (861) ל-6 חודשים פחות (1,047) לרבעון 1; נרשם כמודפס.
32. **2483 Q2** (קבוצת גבאי-בניה,יזום,ניהול ואחזקות נדל"ן בע"מ): דוח Q2 2026, עמודת 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני): סכום שורות פעילות המימון (67,724) שונה מהסה"כ המודפס (67,729) בהפרש 5; לפי דוח Q1 ההפרש בשורת האשראי לזמן קצר (מודפס (18,489), מתאים לסה"כ ולדוח Q1: (18,494)). נרשם כפי שהודפס.
33. **2486 Q2** (מותג עירוני בע"מ): בדוח Q2 (עמוד 45), בשורת 'עלייה (ירידה) במזומנים' בעמודת השנה שהסתיימה ב-31.12.2025 מודפס 6,894, ואילו סכום הפעילות השוטפת, ההשקעה והמימון באותה עמודה הוא 7,342 (כמו בדוח Q1 2026, ומתיישב עם היתרות 6,804 → 14,146). מחוץ לסעיף פעילות המימון – לא משפיע על הנתונים שנרשמו.
34. **2488 Q2** (קבוצת אופק (פ.ה.א.) השקעות בע"מ): מספרי ההשוואה של 2025 עודכנו מחוץ לפעילות המימון ללא סימון הצגה מחדש: יתרת המזומנים לתחילת אפריל–יוני 2025 = 1,590 לעומת 1,701 לסוף רבעון 1/2025 בדוח Q1, ובנספח 'חברות קשורות' (2,668) לעומת (2,688); אין השפעה על פעילות המימון.
35. **2520 Q2** (איסתא נכסים בע"מ): בשורת 'פירעון אשראי מהחברה האם ובעלי מניות אחרים' מודפס בעמודת אפריל–יוני 2026 סכום חיובי 14,913 (ללא סוגריים); נרשם כמודפס.
36. **2522 Q1** (עומר הנדסה ובניה (1986) בע"מ): בעמודי הדוח המאוחד על תזרימי המזומנים מודפסת הכותרת הרצה 'באורים לדוחות הכספיים המאוחדים' (עניין עימוד); לפי תוכן העניינים אלו עמודי הדוח המאוחד על תזרימי המזומנים.
37. **2533 Q1** (אל עד יו אס קפיטל הולדינגס לימיטד): כותרות העמודות בדוח תזרימי המזומנים (עמוד 36) מציינות '30 במרס' (2026 ו-2025), בעוד ששאר הדוח מתייחס ל-31 במרס – נרשם 31.03 (טעות דפוס בכותרת).
38. **2533 Q1** (אל עד יו אס קפיטל הולדינגס לימיטד): בעמודת השנה 2025 סכום שורות המימון המודפסות (268,919-) שונה מהסה"כ המודפס (267,919-) ב-1,000; בדוח על השינויים בהון 'השקעות בעלים' לשנת 2025 = 66,529 לעומת 65,529 בדוח תזרימי המזומנים – ככל הנראה טעות דפוס בשורת 'השקעות בעלים'. הנתונים נרשמו כפי שהודפסו (אותה טעות מופיעה גם בדוח Q2 2026).
39. **2533 Q2** (אל עד יו אס קפיטל הולדינגס לימיטד): בעמודת השנה 2025 סכום שורות המימון המודפסות (268,919-) שונה מהסה"כ המודפס (267,919-) ב-1,000; בדוח על השינויים בהון 'השקעות בעלים' לשנת 2025 = 66,529 לעומת 65,529 בדוח תזרימי המזומנים – ככל הנראה טעות דפוס בשורת 'השקעות בעלים'. הנתונים נרשמו כפי שהודפסו (כמו בדוח Q1 2026).
40. **2559 Q2** (קבוצת בסט א.ע.ו בע"מ): בשורת התקבול 'קבלת הלוואות לזמן ארוך מתאגידים בנקאיים' מודפס בעמודת אפריל–יוני 2026 סכום שלילי (30,547) (6 חודשים 155,185 לעומת 185,733 ברבעון 1); נרשם כמודפס.
41. **2567 Q2** (רם מוגרבי ארדיטי בע"מ): בדוח הדירקטוריון (עמוד 14, טבלת ניתוח תזרימי המזומנים) מוצגים לתקופות 2026 סכומים שונים מהדוח המאוחד על תזרימי המזומנים: פעילות מימון 73,519 (6 חודשים 2026) ו-64,761 (3 חודשים 2026) לעומת 76,050 ו-67,292 בדוח (הפרש 2,531), ופעילות השקעה (77,420) ו-(63,137) לעומת (79,952) ו-(65,669) (הפרש 2,532); בעמודות 2025 של פעילות המימון 21,129 ו-11,907 לעומת 21,130 ו-11,908 (הפרש 1), ובפעילות השוטפת הפרשים של 1 בכל עמודות התקופות הביניים. הנתונים נלקחו מהדוח המאוחד על תזרימי המזומנים (עמוד 54).

---------------------------------------------------------------------------------------------------------------

## 7. validate.py, Excel, integrity, hygiene

**`validate.py` (full, final mode): PASS 36,751 · FAIL 0 · INFO 10; exit 0.** Details:

- AC1: roles and `מקורות` match the folders;
- AC2: names and files;
- AC3: periods, T2;
- AC4/AC5: every value and line in both mapping sheets, master = companies;
- AC6: C1, with the 10 explained columns as INFO;
- AC7: (*) rows; 87 (*) lines with canonical section, numbers and bbox;
- AC9: layout, RTL, labels;
- AC10: 162 zooms and 85 (*) crops show periods and units, plus captions and pages;
- AC11: master, T1 572 `כן` / 76 `לא`;
- AC12: baseline hashes of the 178 PDFs, workspace hygiene;
- AC13: verification records.

**Excel (COM).** All 87 workbooks (86 companies + master) were opened one at a time, read-only, on copies in TEMP. A
repair was ruled out two ways: no new `error*.xml` repair log in TEMP, and no `[Repaired]` in the window caption.
After `CalculateFull` every sheet was scanned:

- 87/87 open without repair;
- every sheet RTL (3 per company, 5 in the master);
- 0 error values;
- the formula cells match `openpyxl`'s count;
- every formula's value equals the expected check from the data. Each company sheet 1 has a check row with one
  formula per column; sheet 2 has one check formula per report column.
- The check rows are 0 everywhere except the 10 explained source columns: 715 (−1, +1, −1, +1), 719 (+8), 2417 (−1),
  2478 (−1), 2483 (+5) and 2533 (−1,000 ×2).
- The master holds values only (0 formulas).

The pipeline's `tool_excel_check.ps1` was also run on all 87 workbooks in sequence: open a copy, recalculate, dump
cells, export every sheet to PDF. Result: 87/87 without any `ERROR`, every sheet RTL and exported to PDF; in every company workbook the check row read back from Excel after recalculation equals the data (0, or the explained source difference).

**Integrity: `tool_integrity.py` → CLEAN.** The 178 source PDFs are byte-identical to `baseline_files_sha256.csv`.
The only new files outside `.goals` are the 2×86 company outputs and the master. There are no `~$*`, `__pycache__`,
logs or temp files, and no `.git`.

**Hygiene.**

- All Phase C helper scripts, composites, snapshots and Excel copies lived in `%TEMP%\fcf_run\_phaseC\`.
- The whole `%TEMP%\fcf_run\` was deleted at the end, including the batches' leftovers and the `_runs` folders. Three
  Phase A scratch files in the TEMP root (`fcfA_*.txt`) were also deleted.
- Every Python run used `PYTHONDONTWRITEBYTECODE=1`.

---------------------------------------------------------------------------------------------------------------

## 8. Known limitations

1. **Verbatim column headers.** `כותרת העמודה בדוח (מילולית)` reproduces the printed header of one column. Headings
   shared by several columns (e.g. one `ליום 31 בדצמבר` or one `(בלתי מבוקר)` over two columns) are repeated for each
   column, and the units line is left out because it has its own field. It is therefore a faithful per-column reading,
   not a copy of the page layout.
2. **Rule A depends on the balance sheet at the reporting dates.** When the same lenders have current and non-current
   balances, the line stays 4/7 even though part of the flow may be short-term. The reasoning is in each line note.
3. **Source defects are recorded as printed,** with no balancing value: the 10 C1 columns in §5; the 27 C2 rows and the
   66 C2 per-item rows, which are explained, not changed. One deliberate exception follows conventions §9: 531 Q2,
   FY-2025 bond issuance, printed `280,68` (a digit missing in print) is recorded as 280,683. That value follows from
   the statement's own total and from the Q1 report, and is documented as a source irregularity.
4. **(*) appendix amounts** keep their printed (positive) sign, except in the two combined rows (121, 1083), as in
   §3-D. The (*) rows are 0 when interest or dividends paid are presented only in financing. When a report shows no
   dividend paid anywhere, the dividend row is 0 without a note.
5. **Restated flag:** set on 10 columns only (111 Q2 c2; 1903, 1905, 2449, the 2025 comparatives), where the column
   header or the financing values are marked. Other restatement marks are column notes.
6. **Visual verification** of Phase B rests on the batches' re-checks after the image cap (§1). Their first-pass
   views are not relied on. Phase C confirmed each of its own changes on displayed composites; it did not re-verify
   every unchanged value a second time.
7. **The 1618 pilot reports** were verified in the pilot (2026-11-09). Phase B only checked the rebuild. Phase C
   changed their header texts and context sections, both confirmed on images.
8. **Zoom crops.** When the header strip and the financing section are contiguous on one page, the zoom is a single
   crop without the blue/orange frames, by design. The full-page image of those reports carries both frames.

---------------------------------------------------------------------------------------------------------------

## 9. Per company × quarter (all 162 reports)

Generated from the final data (`W\data\<iss>_<Q>.json`), the overrides' verification records and the checks, after
the Phase C rebuild. Each report shows:

- source file and PDF pages (physical page numbers, starting at 1);
- the periods (column key, months → end date, in statement order; "Apr–Jun" marks the quarter column of a Q2 report;
  `[restated]` marks a restated column);
- currency/units and text layer;
- the financing lines and the vectors of `אחר` and check;
- **judgement calls**: lines whose item was a decision rather than the wording (items 2, 5, 6, 9, 12, 14, `אחר`,
  `net_*`, subtotals, or a change from the extractor's suggestion), each with its reasoning note, abbreviated. Every
  line's full note is in the workbook's `מיפוי שורות`;
- the (*) classification;
- flags: restated columns, column notes, C1 ≠ 0, source irregularities, report notes, Phase C changes;
- how the numbers were verified: the batch's record, abbreviated (full text in `W\overrides\<iss>_<Q>.json` →
  `verified.method`), plus the Phase C entries.

"(composites …)" in a Phase C entry names the composite images (in `%TEMP%\fcf_run\_phaseC\vis`, deleted since)
that read-only sub-agents checked, every image displayed. The 111 Q2 crop was viewed by me.

**Common verification basis for every report:**

1. Automatic text extraction (coordinates).
2. Every line text, every value digit by digit, the column headers, the units and the (*) lines compared with
   rendered images of the source pages (≥ 220-DPI zoom of header strip + financing, full pages, red (*) crops, context
   pages; 300–600 DPI for doubtful digits), on images confirmed displayed (§1).
3. C1 per column; C2/C3 against the other report.
4. A text scan of every statement page for interest and dividends paid.
5. After the build, the screenshots PDF and workbook were re-checked; `validate.py` re-reads both files and compares
   them with the data.

No report needed manual (image-only) entry: all 162 are in auto mode with overrides.

### 111 – י.ב התחדשות הארץ- מתחמי מגורים בע"מ

- **Q1 2026: not in the folder** (listed in `חסרים והערות` as `דוח חסר`; not downloaded – out of scope).
- **Q2 2026** – `111_י.ב התחדשות הארץ- מתחמי מגורים בע_מ_2026_Q2_1767282.pdf` (report 1767282, 32 pp.) · cash-flow statement PDF pp. 16, 17 · financing p. 16 · column headers p. 16.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 [restated] · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n2 'תמורה ממימוש אופציות' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · n3 'תמורה מהנפקת אופציות' → 2: תמורה מהנפקת אופציות (כתבי אופציה) המוצגת בשורה נפרדת – סעיף 2 (R3: תמורת כתבי אופציה בשורה נפרדת) · n4 'קבלת הלוואה מאחרים' → 5: הלוואה ממלווים אחרים ללא ציון תקופה בדוח התזרים; במאזן ליום 30.06.2025 ההלוואות ממלווים שאינם צד קשור מוצגות כ'הלוואות… · n5 'פירעון הלוואה מאחרים' → 5: פירעון הלוואה ממלווים אחרים – אותה הלוואה לזמן קצר כמו בשורת הקבלה (במאזן: 'הלוואות לזמן קצר') – סעיף 5 · (+3 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p16, פעילות שוטפת: 0, 0, -181) · dividends paid: no line in the statement → (*) row 0.
  - Flags: restated: 6 חודשים שהסתיימו ב-30.06.2025 (מוצג מחדש) · column notes: c2 · report notes: 2 · Phase C: context sections (captions); (*) blank→0 1.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (tool_review). Builder's own first image views (10:15-10:20) were NOT displayed (image cap) and are not relied on. Visual verification: (1) read-only sub-agent with a fres… Phase C: context_sections p17: ['פעילות שוטפת', 'פעילויות שלא במזומן'] -> ['פעילות שוטפת', "נספח א' – התאמות לפעילות השוטפת", "נספח ב' – מידע נוסף על תזרימי ה… (composites v3_00.png). Phase C: (*) line 1 'ריבית ששולמה' (p16) c1: blank (None) -> 0 – generic finalize rule (blank (*) value = 0); the (*) info row was already 0, only the mapping… (composites crop_111_Q2_p16_130802.png – source PDF p16 at 170 DPI (col…).

### 121 – קרדן ישראל בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `121_קרדן ישראל בע_מ_2026_Q1_1744790.pdf` (report 1744790, 74 pp.) · cash-flow statement PDF pp. 46, 47, 48 · financing p. 47 · column headers p. 47.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'דיבידנד לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n8 'תמורה ממימוש אופציות למניות החברה' → 2: מימוש אופציות למניות החברה (המדווחת) – סעיף 2 · n9 'תמורה ממימוש אופציות בחברה מאוחדת' → 6: מימוש אופציות בחברה מאוחדת = הנפקת מניות של החברה הבת למממשי האופציות (בעלי זכויות שאינן מקנות שליטה) – סעיף 6 (R3: iss… · n10 'אשראי לזמן קצר מתאגידים בנקאיים ומוסדות פיננסיים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ומוסדות פיננסיים, מוצג נטו – סעיף 5 (כולל מוסדות פיננסיים ולא רק תאגידים בנקאיים) · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p46, פעילות שוטפת: -10,512, -6,464, -41,447); 'ריבית ששולמה והוונה למלאי' (p48, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): -2,709, -3,798, -23,751) → row [-13,221, -10,262, -65,198]; remark: הרכיב שבנספח ('ריבית ששולמה והוונה למלאי') מודפס ללא סוגריים ונרשם כאן בסימן תשלום (שלילי), כדי שסכום השורה יציג את סך הריבית ששולמה מחוץ לפעילות המימון · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: context sections (captions); (*) section canonical 2; (*) note wording.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (3 columns x 10 lines + total), the column headers (3M to 31.03.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) and the (*) lines (operating 'ריבית ששולמה' p.46, appendix ב 'ריבית ששולמה והוונה למלאי'… Phase C: outside_sections {'2': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_39.png, v3_00.png).
- **Q2 2026** – `121_קרדן ישראל בע_מ_2026_Q2_1766447.pdf` (report 1766447, 80 pp.) · cash-flow statement PDF pp. 50, 51, 52 · financing p. 51 · column headers p. 51.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'דיבידנד לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n7 'תמורה ממימוש אופציות למניות החברה' → 2: מימוש אופציות למניות החברה (המדווחת) – סעיף 2 · n8 'תמורה ממימוש אופציות בחברה מאוחדת' → 6: מימוש אופציות בחברה מאוחדת = הנפקת מניות של החברה הבת למממשי האופציות (בעלי זכויות שאינן מקנות שליטה) – סעיף 6 (R3: iss… · n10 'אשראי לזמן קצר מתאגידים בנקאיים ומוסדות פיננסיים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ומוסדות פיננסיים, מוצג נטו – סעיף 5 (כולל מוסדות פיננסיים ולא רק תאגידים בנקאיים) · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p50, פעילות שוטפת: -36,292, -20,488, -25,780, -14,024, -41,447); 'ריבית ששולמה והוונה למלאי:' (p52, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): -9,476, -11,686, -6,767, -7,888, -23,751) → row [-45,768, -32,174, -32,547, -21,912, -65,198]; remark: הרכיב שבנספח ('ריבית ששולמה והוונה למלאי') מודפס ללא סוגריים ונרשם כאן בסימן תשלום (שלילי), כדי שסכום השורה יציג את סך הריבית ששולמה מחוץ לפעילות המימון · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: context sections (captions); (*) section canonical 2; (*) note wording.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (5 columns x 10 lines + total), the column headers (6M/3M to 30.06.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) and the (*) lines (operating 'ריבית ששולמה' p.50, appendix ב 'ריבית ששולמה והוונה למל… Phase C: outside_sections {'2': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_40.png, v3_01.png).

### 155 – קבוצת מנרב בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `155_קבוצת מנרב בע_מ_2026_Q1_1742331.pdf` (report 1742331, 150 pp.) · cash-flow statement PDF pp. 125, 126 · financing p. 126 · column headers p. 126.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר, נטו' → 5: אשראי לזמן קצר, מוצג נטו (ללא פירוט המלווה) – סעיף 5 · n2 'מימוש אופציה' → 14: תשלום (סכום שלילי) במימוש אופציה – לא תקבול ממימוש אופציות (סעיף 2). לפי דוח הדירקטוריון (דוח Q2 2026, עמ' 11) הייתה לח… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (3 columns x 8 lines + total), the column headers (3M to 31.03.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with the rendered zoom page (header strip + financing section) of…
- **Q2 2026** – `155_קבוצת מנרב בע_מ_2026_Q2_1764162.pdf` (report 1764162, 160 pp.) · cash-flow statement PDF pp. 129, 130 · financing p. 130 · column headers p. 130.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר, נטו' → 5: אשראי לזמן קצר, מוצג נטו (ללא פירוט המלווה) – סעיף 5 · n2 'מימוש אופציה' → 14: תשלום (סכום שלילי) במימוש אופציה – לא תקבול ממימוש אופציות (סעיף 2). לפי דוח הדירקטוריון (עמ' 11 בקובץ זה) הייתה לחברה… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 1.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (5 columns x 8 lines + total), the column headers (6M/3M to 30.06.2026/2025 – c4 confirmed on the image as 3 months to 30.06.2025 –, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with t…

### 200 – לוינסקי עופר בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `200_לוינסקי עופר בע_מ_2026_Q1_1745686.pdf` (report 1745686, 42 pp.) · cash-flow statement PDF pp. 33, 34 · financing p. 34 · column headers p. 34.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת הלוואות לזמן קצר מתאגידים בנקאיים ואחרים' → 5: הלוואות לזמן קצר מתאגידים בנקאיים ואחרים – שורת קבלה ברוטו; כל האשראי לזמן קצר (בנקים ואחרים, נטו או ברוטו) מסוכם בסעיף… · n2 'פירעון הלוואות לזמן קצר מתאגידים בנקאיים ואחרים' → 5: הלוואות לזמן קצר מתאגידים בנקאיים ואחרים – שורת פירעון ברוטו; כל האשראי לזמן קצר (בנקים ואחרים, נטו או ברוטו) מסוכם בסע… · n4 'תמורה ממימוש כתבי אופציה (סדרה 1)' → 2: תמורה ממימוש כתבי אופציה (סדרה 1) – סעיף 2 · n7 'תמורה מהנפקת כתבי אופציה (סדרה 2)' → 2: תמורה מהנפקת כתבי אופציה (סדרה 2) המוצגת בשורה נפרדת – סעיף 2 (R3: תמורת כתבי אופציה בשורה נפרדת) · (+3 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p33, פעילות שוטפת: -2,677, -3,111, -10,059) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (7 lines + total), every value (3 columns), the column headers, the units (אלפי ש"ח) compared digit by digit with the 220-DPI zoom of the financing section (screenshots PDF p.3) and the 100-DPI render of page 34 (…
- **Q2 2026** – `200_לוינסקי עופר בע_מ_2026_Q2_1766476.pdf` (report 1766476, 47 pp.) · cash-flow statement PDF pp. 36, 37 · financing p. 37 · column headers p. 37.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת הלוואות לזמן קצר מתאגידים בנקאיים ואחרים' → 5: הלוואות לזמן קצר מתאגידים בנקאיים ואחרים – שורת קבלה ברוטו; כל האשראי לזמן קצר (בנקים ואחרים, נטו או ברוטו) מסוכם בסעיף… · n2 'פירעון הלוואות לזמן קצר מתאגידים בנקאיים ואחרים' → 5: הלוואות לזמן קצר מתאגידים בנקאיים ואחרים – שורת פירעון ברוטו; כל האשראי לזמן קצר (בנקים ואחרים, נטו או ברוטו) מסוכם בסע… · n4 'תמורה ממימוש כתבי אופציה (סדרה 1)' → 2: תמורה ממימוש כתבי אופציה (סדרה 1) – סעיף 2 · n8 'תמורה מהנפקת כתבי אופציה (סדרה 2)' → 2: תמורה מהנפקת כתבי אופציה (סדרה 2) המוצגת בשורה נפרדת – סעיף 2 (R3: תמורת כתבי אופציה בשורה נפרדת) · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p36, פעילות שוטפת: -5,600, -4,327, -2,921, -1,216, -10,059) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c3 · source irregularities: 1 (see §6) · report notes: 2 · Phase C: issues +1.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (8 lines + total; labels of lines 4 and 8 corrected from the image – the repaired text layer had dropped '(סדרה 1)'/'(סדרה 2)'), every value (5 columns), the column headers, the units (אלפי ש"ח) and the (*) intere… Phase C: issues += 1 (composites no new image needed (rule-based change / note wording only)).

### 341 – שדה נדל"ן-י.ש. בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `341_שדה נדל_ן-י.ש. בע_מ_2026_Q1_1745548.pdf` (report 1745548, 59 pp.) · cash-flow statement PDF pp. 41, 42 · financing p. 42 · column headers p. 41.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי דולר (דולר ארה"ב, אלפים). Text layer: usable.
  - Lines: 13 + total; אחר [0, -67, -67]; check 0 in every column.
  - Judgement calls: n1 'תקבולים מגיוס משקיעים בניכוי הוצאות גיוס' → 6: גיוס הון ממשקיעים – השותפים המוגבלים ב'תאגידים המגייסים' (שותפויות ייעודיות שהשותף הכללי בהן הוא חברה בת של שדה השקעות,… · n2 'קבלת (פרעון) הלוואה לזמן קצר מבעל שליטה' → 5: הלוואה לזמן קצר מבעל השליטה, קבלה (פירעון) נטו – סעיף 5 · n3 'פרעון התחייבות אחרת' → אחר: פירעון 'התחייבות אחרת' – התחייבות לא שוטפת במאזן (עמ' 36: יתרה 32 ליום 31.3.2025, אפס ליום 31.12.2025 וליום 31.3.2026);… · n5 'חלוקות לזכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n8 'קבלת הלוואות לזמן קצר מתאגידים בנקאיים ואחרים' → 5: קבלת הלוואות לזמן קצר מתאגידים בנקאיים ואחרים (בדוח Q2 2026: 'קבלת הלוואות לזמן קצר מתאגידים בנקאיים, נטו מהוצאות') – ס… · n9 'פרעון הלוואות לזמן קצר' → 5: פירעון הלוואות לזמן קצר (ברוטו) – סעיף 5 · n10 'תמורת מתוספת מימוש כתבי אופציה' → 2: תמורה ממימוש כתבי אופציה – סעיף 2 · n12 'תשלום התחייבות אחרת' → אחר: תשלום 'התחייבות אחרת' – אותה התחייבות לא שוטפת כמו בשורה 'פרעון התחייבות אחרת' (מוצגת בעמודת השנה 2025 בשורה נפרדת); מה… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה במזומן' (p41, פעילות שוטפת: -922, -122, -2,190) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 3 · Phase C: verbatim header c1.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס 2026' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס 2026 לא מבוקר' (composites v1_00.png).
- **Q2 2026** – `341_שדה נדל_ן-י.ש. בע_מ_2026_Q2_1767508.pdf` (report 1767508, 83 pp.) · cash-flow statement PDF pp. 47, 48 · financing p. 48 · column headers p. 48.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי דולר (דולר ארה"ב, אלפים). Text layer: usable.
  - Lines: 14 + total; אחר [0, -67, 0, 0, -67]; check 0 in every column.
  - Judgement calls: n2 'תקבולים מגיוס משקיעים בניכוי הוצאות גיוס' → 6: גיוס הון ממשקיעים – השותפים המוגבלים ב'תאגידים המגייסים' (שותפויות ייעודיות שהשותף הכללי בהן הוא חברה בת של שדה השקעות,… · n3 'קבלת (פרעון) הלוואה לזמן קצר מבעל שליטה' → 5: הלוואה לזמן קצר מבעל השליטה, קבלה (פירעון) נטו – סעיף 5 · n4 'פרעון התחייבות אחרת' → אחר: פירעון 'התחייבות אחרת' – התחייבות לא שוטפת במאזן (עמ' 40: יתרה 32 ליום 30.6.2025, אפס ליום 31.12.2025 וליום 30.6.2026);… · n6 'חלוקות לזכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n9 'קבלת הלוואות לזמן קצר מתאגידים בנקאיים, נטו מהוצאות' → 5: קבלת הלוואות לזמן קצר מתאגידים בנקאיים, נטו מהוצאות (בדוח Q1 2026: 'קבלת הלוואות לזמן קצר מתאגידים בנקאיים ואחרים') – ס… · n10 'תמורה מתוספת מימוש כתבי אופציה' → 2: תמורה ממימוש כתבי אופציה – סעיף 2 · n12 'פרעון הלוואות לזמן קצר' → 5: פירעון הלוואות לזמן קצר (ברוטו) – סעיף 5 · n14 'תשלום התחייבות אחרת' → אחר: תשלום 'התחייבות אחרת' – אותה התחייבות לא שוטפת כמו בשורה 'פרעון התחייבות אחרת' (מוצגת בעמודת השנה 2025 בשורה נפרדת); מה… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה במזומן' (p47, פעילות שוטפת: -4,374, -461, -3,069, -339, -2,190) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: source irregularities: 1 (see §6) · report notes: 3 · Phase C: verbatim header c1, c3; issues +1.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני, 2026' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני, 2026 לא מבוקר'; header_text c3… (composites v1_00.png).

### 373 – אאורה השקעות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `373_אאורה השקעות בע_מ_2026_Q1_1743923.pdf` (report 1743923, 77 pp.) · cash-flow statement PDF pp. 53, 54 · financing p. 54 · column headers p. 54.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 11 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר מתאגידים בנקאיים ומאחרים, נטו' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 לפי כלל המיפוי · n5 'מימוש כתבי אופציה למניות, נטו' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · n8 'עסקאות עם בעלי זכויות שאינן מקנות שליטה' → 14: רכישת מניות נוספות של חברת הבת מגידו י.ק. בע"מ מהציבור (776,380 מניות בעלות כ-5.76 מיליון ש"ח – ביאור 5; בדוח על השינוי… · n9 'תקבולים מהנפקת מניות בחברה בת לזכויות שאינן מקנות שליט…' → 6: הנפקת מניות של חברת בת (מגידו) לבעלי זכויות שאינן מקנות שליטה – סעיף 6; בעמודת 3 החודשים 2025 התא ריק בדוח – נרשם 0 · n10 'תקבולים מהנפקת אופציות בחברה בת לזכויות שאינן מקנות של…' → 6: הנפקת אופציות של חברת בת (מגידו) לבעלי זכויות שאינן מקנות שליטה – השקעת זשמ"ש בחברה בת – סעיף 6 (סעיף 2 מיועד לאופציות… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p53, פעילות שוטפת: -54,473, -32,660, -167,395) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · report notes: 2 · Phase C: verbatim header c1, c2.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (11 lines + total; labels of the repaired-font text layer compared word by word with the image), every value (3 columns x 12 lines), the column headers, the units (אלפי ש"ח) and the (*) interest line (p.53, operat… Phase C: header_text c1: 'לשלושה החודשים 2026' -> 'לשלושה החודשים שהסתיימו ביום 31 במרץ 2026 בלתי מבוקר'; header_text c2: 'לשלושה החודשים שהסתיימו ביום 31 במר… (composites v1_00.png).
- **Q2 2026** – `373_אאורה השקעות בע_מ_2026_Q2_1767006.pdf` (report 1767006, 83 pp.) · cash-flow statement PDF pp. 57, 58 · financing p. 58 · column headers p. 58.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 12 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר מתאגידים בנקאיים ומאחרים, נטו' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 לפי כלל המיפוי · n5 'מימוש כתבי אופציה למניות, נטו' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · n8 'רכישה עצמית של מניות' → 9: רכישה עצמית של מניות החברה (ביאור 6: 725,893 מניות בסך 12,223 אלפי ש"ח) – סעיף 9 · n9 'עסקאות עם בעלי זכויות שאינן מקנות שליטה' → 14: רכישת מניות נוספות של חברת הבת מגידו י.ק. בע"מ מהציבור (בדוח על השינויים בהון: קרן הון (3,392) וזשמ"ש (2,364)) – עסקה ע… · n10 'תקבולים מהנפקת מניות בחברה בת לזכויות שאינן מקנות שליט…' → 6: הנפקת מניות של חברת בת (מגידו) לבעלי זכויות שאינן מקנות שליטה – סעיף 6 · n11 'תקבולים מהנפקת אופציות בחברה בת לזכויות שאינן מקנות של…' → 6: הנפקת אופציות של חברת בת (מגידו) לבעלי זכויות שאינן מקנות שליטה – השקעת זשמ"ש בחברה בת – סעיף 6 (סעיף 2 מיועד לאופציות… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p57, פעילות שוטפת: -101,995, -79,161, -47,522, -46,501, -167,395) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c4, c5 · report notes: 2 · Phase C: verbatim header c1, c3.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (12 lines + total; labels of the repaired-font text layer compared word by word with the image; total label printed 'מעילות'), every value (5 columns x 13 lines), the column headers, the units (אלפי ש"ח) and the (… Phase C: header_text c1: 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026' -> 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026 בלתי מבוקר'; header_text c3: 'לשלושה חודשים ש… (composites v1_01.png, v3_01.png).

### 400 – אחים דוניץ בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `400_אחים דוניץ בע_מ_2026_Q1_1745054.pdf` (report 1745054, 51 pp.) · cash-flow statement PDF pp. 33, 34 · financing p. 33 · column headers p. 33.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: none beyond the wording of the lines (6).
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p33, פעילות שוטפת: -7,626, -8,646, -43,106) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: context sections (captions).
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (tool_review / word rows). Builder's own first image views (10:18-10:31) were NOT displayed (image cap) and are not relied on. Visual verification: (1) read-only sub-agent… Phase C: context_sections p34: ['פעילויות שלא במזומן'] -> ['פעילות שוטפת', "נספח א' – התאמות לפעילות השוטפת", "נספח ב' – פעילות שלא במזומן"] (composites v3_02.png).
- **Q2 2026** – `400_אחים דוניץ בע_מ_2026_Q2_1767345.pdf` (report 1767345, 55 pp.) · cash-flow statement PDF pp. 37, 38 · financing p. 37 · column headers p. 37.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'מימוש אופציות לעובדים' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p37, פעילות שוטפת: -25,149, -20,099, -17,523, -11,454, -43,106) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: source irregularities: 1 (see §6) · report notes: 2 · Phase C: context sections (captions); issues +1.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (tool_review / word rows). Builder's own first image views (10:18-10:31) were NOT displayed (image cap) and are not relied on. Visual verification: (1) read-only sub-agent… Phase C: context_sections p38: ['פעילויות שלא במזומן'] -> ['פעילות שוטפת', "נספח א' – התאמות לפעילות השוטפת", "נספח ב' – פעילות שלא במזומן"]; issues += 1 (composites v3_02.png).

### 421 – נתנאל גרופ בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `421_נתנאל גרופ בע_מ_2026_Q1_1745074.pdf` (report 1745074, 55 pp.) · cash-flow statement PDF pp. 35, 36 · financing p. 36 · column headers p. 36.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, מוצג נטו – סעיף 5 (כולל מלווים אחרים, R3) · n4 'תמורה מהנפקת ניירות ערך' → 1: הקצאה פרטית חריגה של מניות וכתבי אופציה ללאומי פרטנרס (באור 5א; אושרה בדירקטוריון ב-6.1.2026): 3,024,194 מניות רגילות ב… · n5 'עלויות הנפקת ניירות ערך' → 1: עלויות הנפקת חבילת ניירות הערך (מניות + כתבי אופציה, באור 5א) – עלויות הנפקה מקוזזות בסעיף 1 (R3) · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ועמלות ששולמו' (p35, פעילות שוטפת: -13,825, -28,202, -94,207) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2 · report notes: 2.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (8 lines + total), every value (3 columns), the column headers, the units (אלפי ש"ח) compared digit by digit with the 220-DPI zoom of the financing section (screenshots PDF p.3) and the 120-DPI render of page 35 (…
- **Q2 2026** – `421_נתנאל גרופ בע_מ_2026_Q2_1764607.pdf` (report 1764607, 69 pp.) · cash-flow statement PDF pp. 44, 45 · financing p. 45 · column headers p. 45.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, מוצג נטו – סעיף 5 (כולל מלווים אחרים, R3) · n4 'תמורה מהנפקת ניירות ערך' → 1: הקצאה פרטית חריגה של מניות וכתבי אופציה ללאומי פרטנרס (באור 5א בדוח Q1; אושרה בדירקטוריון ב-6.1.2026): 3,024,194 מניות… · n5 'עלויות הנפקת ניירות ערך' → 1: עלויות הנפקת חבילת ניירות הערך (מניות + כתבי אופציה) – עלויות הנפקה מקוזזות בסעיף 1 (R3) · n8 'קבלת הלוואות לזמן ארוך מבעלי זכויות המיעוט' → 4: הלוואות לזמן ארוך מבעלי זכויות המיעוט (בעלי זכויות שאינן מקנות שליטה) בפעילות בקפריסין – מוצגות במאזן כהתחייבות לא שוטפ… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ועמלות ששולמו' (p44, פעילות שוטפת: -52,123, -63,383, -38,298, -36,011, -94,207) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2, c4 · source irregularities: 1 (see §6) · report notes: 2 · Phase C: issues +1.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (9 lines + total), every value (5 columns), the column headers (c3 = 3 months ended 30.06.2026 confirmed on the image), the units (אלפי ש"ח) compared digit by digit with the 220-DPI zoom of the financing section (… Phase C: issues += 1 (composites no new image needed (rule-based change / note wording only)).

### 425 – צבי צרפתי ובניו השקעות ובנין (1992) בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `425_צבי צרפתי ובניו השקעות ובנין (1992) בע_מ_2026_Q1_1744485.pdf` (report 1744485, 100 pp.) · cash-flow statement PDF pp. 73, 74 · financing p. 73 · column headers p. 73.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'אשראי לזמן קצר, נטו' → 5: אשראי לזמן קצר, נטו (ללא ציון המלווה) – סעיף 5 · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p74, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 5,296, 4,354, 41,717); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · report notes: 3 · Phase C: verbatim header c1, c2, c3; context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 (בלתי… (composites v1_01.png, v2_21.png, v3_03.png).
- **Q2 2026** – `425_צבי צרפתי ובניו השקעות ובנין (1992) בע_מ_2026_Q2_1766510.pdf` (report 1766510, 113 pp.) · cash-flow statement PDF pp. 84, 85, 86 · financing p. 85 · column headers p. 85.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'אשראי לזמן קצר, נטו' → 5: אשראי לזמן קצר, נטו (ללא ציון המלווה) – סעיף 5 · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p86, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 24,042, 21,319, 18,746, 16,965, 41,717); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c4 · report notes: 3 · Phase C: verbatim header c1, c2, c3, c4, c5; context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי… (composites v1_01.png, v2_22.png, v3_03.png).

### 434 – ישראל קנדה (ט.ר) בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (-1), C2 3 חודשים שהסתיימו ב-31.03.2025 total (-1); C2 per-item INFO rows (explained): 8.
- **Q1 2026** – `434_ישראל קנדה (ט.ר) בע_מ_2026_Q1_1744562.pdf` (report 1744562, 118 pp.) · cash-flow statement PDF pp. 53, 54, 55, 56 · financing p. 53 · column headers p. 53.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 13 + total; אחר [0, 0, 69,692]; check 0 in every column.
  - Judgement calls: n1 'אשראי מתאגידים בנקאיים, נטו' → 5: אשראי מתאגידים בנקאיים מוצג נטו ללא ציון תקופה – סעיף 5 · n4 'פירעון אגרות חוב ורכישה עצמית' → 8: פירעון אגרות חוב ורכישה עצמית שלהן – סעיף 8 (בדוחות על השינויים בהון אין רכישה עצמית של מניות בתקופות אלה, ולכן 'רכישה… · n7 'מיזוג חברה בת - ראה נספח ה'' → אחר: מיזוג חברה בת – נספח ה' (עמ' 56) מפרט את רכיבי התזרים נטו מהמיזוג: הון חוזר, נכסים פיננסיים בשווי הוגן, השקעה בכלולות,… · n10 'חלוקות לזכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n11 'עסקאות עם בעלי זכויות שאינן מקנות שליטה' → 6/14 לפי סימן: עסקאות עם בעלי זכויות שאינן מקנות שליטה – שורה נטו עם סימנים מעורבים: בכל עמודה לפי הסימן (net_nci) – סכום חיובי → סעיף… · n13 'השקעות הוניות של בעלי זכויות שאינן מקנות שליטה' → 6: השקעות הוניות של בעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 6 · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'מזומנים ששולמו במשך התקופה עבור: ריבית' (p55, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: 74,802, 67,935, 341,471); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · report notes: 2 · Phase C: item n11 6→6/14 לפי סימן; verbatim header c1, c2, c3; (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (13 lines + total), every value (3 columns x 14 lines), the column headers, the units (אלפי ש"ח per column) and the (*) interest line (appendix B, p.55, positive as printed) compared digit by digit with the 220-DP… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2 0 2 6 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 (ב… (composites v1_02.png, v2_09.png).
- **Q2 2026** – `434_ישראל קנדה (ט.ר) בע_מ_2026_Q2_1766574.pdf` (report 1766574, 132 pp.) · cash-flow statement PDF pp. 58, 59, 60, 61 · financing p. 58 · column headers p. 58.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 13 + total; אחר [0, 0, 0, 0, 69,692]; check 0 in every column.
  - Judgement calls: n1 'אשראי מתאגידים בנקאיים, נטו' → 5: אשראי מתאגידים בנקאיים מוצג נטו ללא ציון תקופה – סעיף 5 · n4 'פירעון אגרות חוב ורכישה עצמית' → 8: פירעון אגרות חוב ורכישה עצמית שלהן – סעיף 8 (בדוחות על השינויים בהון אין רכישה עצמית של מניות בתקופות אלה, ולכן 'רכישה… · n7 'מיזוג חברה בת - ראה נספח ה'' → אחר: מיזוג חברה בת – נספח ה' (עמ' 61) מפרט את רכיבי התזרים נטו מהמיזוג: הון חוזר, נכסים פיננסיים בשווי הוגן, השקעה בכלולות,… · n10 'חלוקות לזכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n11 'עסקאות עם בעלי זכויות שאינן מקנות שליטה, נטו' → 6/14 לפי סימן: עסקאות עם בעלי זכויות שאינן מקנות שליטה, נטו – שורה נטו עם סימנים מעורבים: בכל עמודה לפי הסימן (net_nci) – סכום חיובי →… · n13 'השקעות הוניות של בעלי זכויות שאינן מקנות שליטה' → 6: השקעות הוניות של בעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 6 · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'מזומנים ששולמו במשך התקופה עבור: ריבית' (p60, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: 213,285, 179,042, 128,219, 107,136, 378,178); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים); סכומי 2025 בנספח מסומנים (*) 'סווג מחדש' ושונים מדוח Q1 (שנת 2025: 378,178 כאן, 341,471 בדוח Q1) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c4, c5 · source irregularities: 1 (see §6) · report notes: 2 · Phase C: item n11 6→6/14 לפי סימן; verbatim header c1, c2, c3, c4, c5; (*) section canonical 1; (*) note wording; issues +1.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (13 lines + total), every value (5 columns x 14 lines), the column headers, the units (אלפי ש"ח per column) and the (*) interest line (appendix B, p.60, positive, with '(*)' marks on c2/c4/c5) compared digit by di… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2 0 2 6 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 (ב… (composites v1_02.png, v2_10.png).

### 444 – מרדכי אביב תעשיות בניה (1973) בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `444_מרדכי אביב תעשיות בניה (1973) בע_מ_2026_Q1_1745537.pdf` (report 1745537, 54 pp.) · cash-flow statement PDF pp. 35, 36 · financing p. 35 · column headers p. 35.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: באלפי ₪ (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: none beyond the wording of the lines (6).
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p36, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 10,199, 12,504, 37,715); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2; (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (6 lines + total), every value (3 columns x 7 lines), the column headers, the units ('(באלפי ₪)' in the title) and the (*) interest line (appendix A, p.36, positive as printed) compared digit by digit with the 220… Phase C: header_text c1: 'על תזרימי המזומנים (באלפי)₪ לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 בלתי מבוקר' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 3… (composites v1_02.png, v2_11.png).
- **Q2 2026** – `444_מרדכי אביב תעשיות בניה (1973) בע_מ_2026_Q2_1763129.pdf` (report 1763129, 58 pp.) · cash-flow statement PDF pp. 37, 38 · financing p. 37 · column headers p. 37.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 4 + total; אחר 0; check 0 in every column.
  - Judgement calls: none beyond the wording of the lines (4).
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p38, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 13,075, 16,834, 2,876, 4,330, 37,715); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (4 lines + total), every value (5 columns x 5 lines), the column headers, the units ('(באלפי ש"ח)' in the title) and the (*) interest line (appendix A, p.38, positive as printed) compared digit by digit with the 2… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_12.png).

### 473 – קבוצת עמוס לוזון יזמות ואנרגיה בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `473_קבוצת עמוס לוזון יזמות ואנרגיה בע_מ_2026_Q1_1745607.pdf` (report 1745607, 99 pp.) · cash-flow statement PDF pp. 55, 56 · financing p. 56 · column headers p. 56.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 13 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'דיבידנד ששולם למיעוט' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n4 'קבלת הלוואה מהמיעוט' → 4: הלוואה מבעלי זכויות שאינן מקנות שליטה (מיעוט) בחברות מוחזקות; במאזן מוצגת בעיקר כהתחייבות לא שוטפת ('הלוואה מבעלי מניות… · n6 'רכישת מניות מהמיעוט' → 14: רכישת זכויות נוספות בחברה בת מאוחדת מבעלי זכויות שאינן מקנות שליטה (עסקה הונית, ללא שינוי בשליטה) – סעיף 14 · n7 'מימוש כתבי אופציה' → 2: מימוש כתבי אופציה של החברה – סעיף 2 · n8 'רכישת כתבי אופציה' → 9: רכישה חוזרת של כתבי אופציה של החברה (מכשיר הוני; בדוח על השינויים בהון נזקפה להון המיוחס לבעלי מניות החברה) – אינה מימו… · n13 'קבלת הלוואות לזמן קצר מתאגידים בנקאיים ומוסדות פינסיים…' → 5: אשראי לזמן קצר מתאגידים בנקאיים ומוסדות פיננסיים, נטו – סעיף 5 (בדוח המודפס: 'פינסיים' – כך במקור) · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p55, פעילות שוטפת: -39,353, -21,218, -101,793) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: source irregularities: 1 (see §6) · report notes: 2 · Phase C: issues +1.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (13 lines + total), every value (3 columns), the column headers, the units (אלפי ש"ח) and the (*) interest line (operating, p. 55) compared digit by digit with 220-DPI renders (tool_review fin/page/outside images)… Phase C: issues += 1 (composites no new image needed (rule-based change / note wording only)).
- **Q2 2026** – `473_קבוצת עמוס לוזון יזמות ואנרגיה בע_מ_2026_Q2_1767385.pdf` (report 1767385, 109 pp.) · cash-flow statement PDF pp. 60, 61 · financing p. 61 · column headers p. 61.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 13 + total; אחר 0; check 0 in every column.
  - Judgement calls: n2 'דיבידנד ששולם למיעוט' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n4 'קבלת הלוואה מהמיעוט' → 4: הלוואה מבעלי זכויות שאינן מקנות שליטה (מיעוט) בחברות מוחזקות; במאזן מוצגת בעיקר כהתחייבות לא שוטפת ('הלוואה מבעלי מניות… · n6 'רכישת מניות מהמיעוט' → 14: רכישת זכויות נוספות בחברה בת מאוחדת מבעלי זכויות שאינן מקנות שליטה (עסקה הונית, ללא שינוי בשליטה) – סעיף 14 · n7 'מימוש כתבי אופציה' → 2: מימוש כתבי אופציה של החברה – סעיף 2 · n8 'רכישת כתבי אופציה' → 9: רכישה חוזרת של כתבי אופציה של החברה (מכשיר הוני; בדוח על השינויים בהון נזקפה להון המיוחס לבעלי מניות החברה) – אינה מימו… · n13 'קבלת הלוואות לזמן קצר מתאגידים בנקאיים ומוסדות פיננסיי…' → 5: אשראי לזמן קצר מתאגידים בנקאיים ומוסדות פיננסיים, נטו – סעיף 5 · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p60, פעילות שוטפת: -66,956, -33,104, -27,603, -11,886, -101,793) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (13 lines + total), every value (5 columns), the column headers, the units (אלפי ש"ח) and the (*) interest line (operating, p. 60) compared digit by digit with 220-DPI renders (tool_review fin/page/outside images)…

### 486 – וויי-בוקס נדל"ן בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `486_וויי-בוקס נדל_ן בע_מ_2026_Q1_1745702.pdf` (report 1745702, 78 pp.) · cash-flow statement PDF pp. 58, 59 · financing p. 58 · column headers p. 58.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n2 'תמורה ממימוש אופציות' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p59, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 15,847, 19,653, 68,193); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 4 · Phase C: verbatim header c1, c2; (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: '3 חודשים שהסתיימו ב-31 במרס 2026' -> '3 חודשים שהסתיימו ב-31 במרס 2026 (בלתי מבוקר)'; header_text c2: '3 חודשים שהסתיימו ב-31 במרס 2… (composites v1_03.png, v2_23.png).
- **Q2 2026** – `486_וויי-בוקס נדל_ן בע_מ_2026_Q2_1767297.pdf` (report 1767297, 83 pp.) · cash-flow statement PDF pp. 63, 64 · financing p. 63 · column headers p. 63.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'תמורה ממימוש אופציות' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p64, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 38,979, 37,508, 23,132, 17,855, 68,193); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 4 · Phase C: verbatim header c1, c3, c4; (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: '6 חודשים שהסתיימו ביום 30 ביוני 2026' -> '6 חודשים שהסתיימו ביום 30 ביוני 2026 (בלתי מבוקר)'; header_text c3: '3 חודשים שהסתיימו ביו… (composites v1_03.png, v2_24.png).

### 531 – בוני התיכון הנדסה אזרחית ותשתיות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (-1); C2 per-item INFO rows (explained): 1.
- **Q1 2026** – `531_בוני התיכון הנדסה אזרחית ותשתיות בע_מ_2026_Q1_1744302.pdf` (report 1744302, 51 pp.) · cash-flow statement PDF pp. 29, 30 · financing p. 30 · column headers p. 30.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'קבלת (פירעון) אשראי מתאגידים בנקאיים, נטו' → 5: קבלת (פירעון) אשראי מתאגידים בנקאיים, נטו – שורת אשראי המוצגת נטו ללא ציון תקופה → סעיף 5 (R3) · n5 'הנפקת אופציות' → 2: הנפקת אופציות: 317,620 כתבי אופציה לא סחירים שהוקצו בהקצאה פרטית (19.2.2026) יחד עם 635,240 מניות; התמורה שיוחסה לכתבי… · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p29, פעילות שוטפת: -4,284, -7,495, -57,448) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2 · report notes: 2.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (6 lines + total), every value (3 columns), the column headers, the units ((אלפי ש"ח) in the statement title) compared digit by digit with the 220-DPI zoom of the financing section (screenshots PDF p.3) and the 12…
- **Q2 2026** – `531_בוני התיכון הנדסה אזרחית ותשתיות בע_מ_2026_Q2_1766963.pdf` (report 1766963, 58 pp.) · cash-flow statement PDF pp. 33, 34 · financing p. 34 · column headers p. 34.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'קבלת אשראי מתאגידים בנקאיים, נטו' → 5: קבלת אשראי מתאגידים בנקאיים, נטו – שורת אשראי המוצגת נטו ללא ציון תקופה → סעיף 5 (R3); בדוח Q1: 'קבלת (פירעון) אשראי מת… · n5 'הנפקת אופציות' → 2: הנפקת אופציות: כתבי אופציה לא סחירים שהוקצו בהקצאה פרטית (פברואר 2026) יחד עם מניות; התמורה שיוחסה לכתבי האופציה מוצגת… · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p33, פעילות שוטפת: -32,021, -26,813, -27,736, -19,318, -57,448) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2, c3, c4, c5 · source irregularities: 1 (see §6) · report notes: 2.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (6 lines + total), every value (5 columns), the column headers, the units ((אלפי ש"ח) in the statement title) compared digit by digit with the 220-DPI zoom of the financing section (screenshots PDF p.7 – the print…

### 539 – רוטשטיין נדל"ן בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2025 total (-1); C2 per-item INFO rows (explained): 1.
- **Q1 2026** – `539_רוטשטיין נדל_ן בע_מ_2026_Q1_1744508.pdf` (report 1744508, 85 pp.) · cash-flow statement PDF pp. 55, 56 · financing p. 56 · column headers p. 56.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'קבלת אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 לפי כלל המיפוי · n9 'הנפקת מניות' → 2: לפי הדוח על השינויים בהון (עמ' 52–54) כל הסכומים בשורה 'הנפקת מניות' הם מימוש אופציות: 2026 – מימוש כתבי האופציה שהונפק… · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p55, פעילות שוטפת: -19,338, -21,124, -61,671) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (tool_review / word rows). Builder's own first image views (10:20-10:28) were NOT displayed (image cap) and are not relied on. Visual verification: (1) read-only sub-agent…
- **Q2 2026** – `539_רוטשטיין נדל_ן בע_מ_2026_Q2_1765452.pdf` (report 1765452, 95 pp.) · cash-flow statement PDF pp. 58, 59, 60 · financing p. 59 · column headers p. 59.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'קבלת (פירעון) אשראי לזמן קצר מתאגידים בנקאיים ואחרים,…' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 לפי כלל המיפוי · n9 'הנפקת מניות' → 2: לפי הדוח על השינויים בהון (עמ' 55–57) כל הסכומים בשורה 'הנפקת מניות' הם מימוש אופציות: 2026 – מימוש כתבי האופציה שהונפק… · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p58, פעילות שוטפת: -25,391, -32,421, -6,053, -11,297, -61,671) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 3 · Phase C: context sections (captions).
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (tool_review / word rows). Builder's own first image views (10:21-10:28) were NOT displayed (image cap) and are not relied on. Visual verification: (1) read-only sub-agent… Phase C: context_sections p60: None -> ['פעילות מהותית שלא במזומן', 'תמורה ממימוש השקעות בחברות מאוחדות שאוחדו בעבר'] (composites v3_04.png).

### 573 – משולם לוינשטין הנדסה וקבלנות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `573_משולם לוינשטין הנדסה וקבלנות בע_מ_2026_Q1_1744074.pdf` (report 1744074, 63 pp.) · cash-flow statement PDF pp. 37, 38, 39 · financing p. 37 · column headers p. 37.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 13 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'תמורה בגין מימוש אופציות' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · n4 'דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות (ביאור 6ג') · n6 'מכירת מניות לבעלי זכויות שאינן מקנות שליטה בחברה מאוחדת' → 6: מכירת כ-10.1% ממניות MRPL (חברה מאוחדת) למנכ"ל MRPL בתמורה ל-1,425 אלפי ש"ח, ללא איבוד שליטה (ביאור 6ה') – סעיף 6 (מכיר… · n13 'גידול (קיטון) באשראי לזמן קצר מתאגידים בנקאיים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים, מוצג נטו – סעיף 5 · (+9 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'מזומנים ששולמו במהלך התקופה עבור: ריבית' (p39, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 11,994, 13,100, 72,738); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · report notes: 4 · Phase C: verbatim header c1, c2, c3; (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:18 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'שלושה חודשים שהסתיימה ביום 2026 אלפי ש"ח' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס 2026 (בלתי מבוקר)'; header_text c2: 'לתקו… (composites v1_03.png, v2_25.png).
- **Q2 2026** – `573_משולם לוינשטין הנדסה וקבלנות בע_מ_2026_Q2_1764868.pdf` (report 1764868, 66 pp.) · cash-flow statement PDF pp. 39, 40, 41 · financing p. 39 · column headers p. 39.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 13 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'תמורה בגין מימוש אופציות' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · n4 'דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות (ביאור 6ג') · n6 'רכישה עצמית של מניות על ידי בעלי זכויות שאינן מקנות של…' → 6: למרות הנוסח 'רכישה עצמית', זהו תקבול (1,425) ממכירת כ-10.1% ממניות MRPL (חברה מאוחדת) למנכ"ל MRPL ללא איבוד שליטה, לפי… · n13 'גידול (קיטון) באשראי לזמן קצר מתאגידים בנקאיים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים, מוצג נטו – סעיף 5 · (+9 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'מזומנים ששולמו במהלך התקופה עבור: ריבית' (p41, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 37,379, 37,442, 25,385, 24,342, 72,738); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c4 · report notes: 4 · Phase C: verbatim header c1, c2, c3, c4, c5; (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:18 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'שישה חודשים שהסתיימה 2026' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי מבוקר)'; header_text c2: 'לתקופה של שישה חודש… (composites v1_04.png, v2_26.png).

### 584 – א.ליבנטל אחזקות בע"מ

- **Q1 2026: not in the folder** (listed in `חסרים והערות` as `דוח חסר`; not downloaded – out of scope).
- **Q2 2026** – `584_א.ליבנטל אחזקות בע_מ_2026_Q2_1767534.pdf` (report 1767534, 70 pp.) · cash-flow statement PDF pp. 30, 31, 32 · financing p. 30 · column headers p. 30.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת (פירעון) הלוואה מבעל שליטה' → 5: הלוואה מבעל השליטה, מוצגת נטו (קבלה/פירעון) ללא ציון תקופה (במאזן: 'הלוואות מבעל שליטה' בהתחייבויות השוטפות; 9,304 → 8,… · n3 'פירעון הלוואות מאחרים' → 5: ללא ציון תקופה בדוח; לפי המאזן ודוח הדירקטוריון הפירעונות ב-2026 (22,278) הם בעיקר פירעון אשראי לזמן קצר מאחרים – הלווא… · n4 'קבלת הלוואות מתאגידים פיננסיים' → 5: הלוואות מתאגידים פיננסיים – לפי ביאור 3יא מסגרת אשראי בנקאית של 22 מיליון ש"ח (28.5.2026–30.3.2027) של 'הלוואות המתחדשו… · n8 'קבלת (פירעון) אשראי לזמן קצר מתאגידים בנקאיים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים, מוצג נטו – סעיף 5 · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'מזומנים ששולמו במשך התקופה עבור: ריבית ששולמה' (p32, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 2,386, 5,194, 10,375); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים); הדוח אינו מציין אם סכומי הנספח כוללים גם את הריבית המוצגת בפעילות המימון · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2, c3 · report notes: 5 · Phase C: verbatim header c1, c2; (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:23 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'לששת החודשים שהסתיימו ביום 2026' -> 'לששת החודשים שהסתיימו ביום 30 ביוני 2026 בלתי מבוקר'; header_text c2: 'לששת החודשים שהסתיימו בי… (composites v1_04.png, v2_27.png).

### 673 – קבוצת ריי טי.אל.וי בע"מ

- **Q1 2026: not in the folder** (listed in `חסרים והערות` as `דוח חסר`; not downloaded – out of scope).
- **Q2 2026** – `673_קבוצת ריי טי.אל.וי בע_מ_2026_Q2_1767512.pdf` (report 1767512, 42 pp.) · cash-flow statement PDF pp. 31 · financing p. 31 · column headers p. 31.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת הלוואות מבעלי עניין וצדדים קשורים' → 5: הלוואות מבעלי עניין וצדדים קשורים (ברוטו, ללא ציון תקופה); במאזן המאוחד היתרה לצדדים קשורים מוצגת בהתחייבויות השוטפות (… · n4 'קבלת הלוואות מתאגידים בנקאיים' → 5: הלוואה מתאגיד בנקאי (ביאור 3(1)ד': כ-1 מיליון ש"ח, נטלה בינואר 2026, לפירעון ביום 31.12.2026) – הלוואה לזמן קצר; במאזן… · n5 'קבלת הלוואות מאחרים' → 5: הלוואות ממלווים אחרים (ברוטו, ללא ציון תקופה; למשל ביאור 3(1)ב': כ-2.7 מיליון ש"ח ממלווה חוץ בנקאי לפירעון ב-15.2.2027)… · n6 'פרעון הלוואות מאחרים' → 5: פירעון הלוואות ממלווים אחרים – בעיקר הלוואת אשטרום (ביאור 3(1)ו': נפרעה במלואה, כ-12.4 מיליון ש"ח קרן וריבית), שהוצגה כ… · n7 'תמורה מהנפקת מניות וכתבי אופציה, נטו' → 1: תמורה מהנפקת מניות וכתבי אופציה (הקצאה פרטית של מניות וכתבי אופציה, ללא פיצול בדוח) – לפי מוסכמות שלב ב' §6: מניות + או… · (+2 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (7 lines + total), every value (3 columns x 8 lines), the column headers (6M 2026, 6M 2025, FY 2025) and the units (אלפי ש"ח) compared digit by digit with the 220-DPI review render of the header strip + financing… Phase C: header_text c1: 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026' -> 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026 (בלתי מבוקר)'; header_text c2: 'לשישה חודשים… (composites v1_04.png).

### 715 – אזורים-חברה להשקעות בפתוח ובבנין בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `715_אזורים-חברה להשקעות בפתוח ובבנין בע_מ_2026_Q1_1744611.pdf` (report 1744611, 67 pp.) · cash-flow statement PDF pp. 46, 47 · financing p. 47 · column headers p. 47.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check [0, -1, 0].
  - Judgement calls: n1 'קבלת (פרעון) אשראי לזמן קצר מבנקים ואחרים, נטו' → 5: אשראי לזמן קצר מבנקים ואחרים, מוצג נטו – סעיף 5 (כולל מלווים אחרים ולא רק תאגידים בנקאיים) · n5 'פרעון התחייבויות לזמן ארוך לבנקים, אגרות חוב ואחרים' → 7: שורה משולבת: פירעון התחייבויות לזמן ארוך לבנקים, אגרות חוב ואחרים – הדוח אינו מפצל בין הלוואות לאג"ח. סווגה כולה לסעיף… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · C1 ≠ 0 (source does not add up, explained): 3 חודשים שהסתיימו ב-31.03.2025 (-1) · source irregularities: 1 (see §6) · report notes: 3.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (3 columns x 7 lines + total), the column headers (3M to 31.03.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with the rendered zoom page (header strip + financing section) of…
- **Q2 2026** – `715_אזורים-חברה להשקעות בפתוח ובבנין בע_מ_2026_Q2_1765211.pdf` (report 1765211, 120 pp.) · cash-flow statement PDF pp. 50, 51 · financing p. 51 · column headers p. 51.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check [1, -1, 1, 0, 0].
  - Judgement calls: n1 'קבלת (פרעון) אשראי לזמן קצר מבנקים ואחרים, נטו' → 5: אשראי לזמן קצר מבנקים ואחרים, מוצג נטו – סעיף 5 (כולל מלווים אחרים ולא רק תאגידים בנקאיים) · n5 'תקבולים מבעלי זכויות שאינן מקנות שליטה' → 6: תקבולים מבעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 6 · n6 'פרעון התחייבויות לזמן ארוך לבנקים, אגרות חוב ואחרים' → 7: שורה משולבת: פירעון התחייבויות לזמן ארוך לבנקים, אגרות חוב ואחרים – הדוח אינו מפצל בין הלוואות לאג"ח. סווגה כולה לסעיף… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c1, c2, c3 · C1 ≠ 0 (source does not add up, explained): 6 חודשים שהסתיימו ב-30.06.2026 (1); 6 חודשים שהסתיימו ב-30.06.2025 (-1); 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני) (1) · source irregularities: 1 (see §6) · report notes: 3.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (5 columns x 8 lines + total), the column headers (6M/3M to 30.06.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with the rendered zoom page (header strip + financing section)…

### 719 – א.לוי השקעות ובנין בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `719_א.לוי השקעות ובנין בע_מ_2026_Q1_1745275.pdf` (report 1745275, 58 pp.) · cash-flow statement PDF pp. 37, 38, 39 · financing p. 38 · column headers p. 38.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check [0, 8, 0].
  - Judgement calls: n3 'ירידה באשראי בעלי עניין' → 5: אשראי מבעלי עניין, מוצג נטו (ירידה) ללא ציון תקופה – סעיף 5 (R3: שורת אשראי/הלוואות נטו ללא תקופה) · n6 'קבלת הלוואת בגין פרויקטים בביצוע' → 5: קבלת הלוואות בגין פרויקטים בביצוע (מימון פרויקטים) – שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורי… · n7 'פרעון הלוואה בגין פרויקטים בביצוע' → 5: פירעון הלוואות בגין פרויקטים בביצוע – אותן הלוואות (התחייבות שוטפת) – סעיף 5, כמו שורת הקבלה (שונתה מסעיף 7 בשלב C) · n8 'פרעון אשראי לזמן קצר מתאגידים בנקאיים ואחרים' → 5: פירעון אשראי לזמן קצר מתאגידים בנקאיים ואחרים (מוצג ברוטו) – כל האשראי לזמן קצר, מבנקים ומאחרים, בסעיף 5 (R3) · n9 'קבלת אשראי לזמן קצר מתאגידים בנקאיים ואחרים' → 5: קבלת אשראי לזמן קצר מתאגידים בנקאיים ואחרים (מוצג ברוטו) – כל האשראי לזמן קצר, מבנקים ומאחרים, בסעיף 5 (R3) · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p37, פעילות שוטפת: -5,073, -3,815, -20,910) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2, c3 · C1 ≠ 0 (source does not add up, explained): 3 חודשים שהסתיימו ב-31.03.2025 (8) · source irregularities: 1 (see §6) · report notes: 3 · Phase C: item n6 4→5, n7 7→5; verbatim header c1, c2.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:24 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה 2026' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ, 2026 בלתי מבוקר'; header_text c2: 'לתקופה של… (composites v1_05.png, v2_04.png).
- **Q2 2026** – `719_א.לוי השקעות ובנין בע_מ_2026_Q2_1767607.pdf` (report 1767607, 140 pp.) · cash-flow statement PDF pp. 118, 119, 120 · financing p. 119 · column headers p. 118.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'עליה (ירידה) באשראי בעלי עניין' → 5: אשראי מבעלי עניין, מוצג נטו (עליה/ירידה) ללא ציון תקופה – סעיף 5 (R3: שורת אשראי/הלוואות נטו ללא תקופה); טקסט השורה תוק… · n6 'קבלת הלוואת בגין פרויקטים בביצוע' → 5: קבלת הלוואות בגין פרויקטים בביצוע (מימון פרויקטים) – שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורי… · n7 'פרעון הלוואה בגין פרויקטים בביצוע' → 5: פירעון הלוואות בגין פרויקטים בביצוע – אותן הלוואות (התחייבות שוטפת) – סעיף 5, כמו שורת הקבלה ובדוח Q1 (שונתה מסעיף 7 בש… · n8 'פרעון אשראי לזמן קצר מתאגידים בנקאיים ואחרים' → 5: פירעון אשראי לזמן קצר מתאגידים בנקאיים ואחרים (מוצג ברוטו) – כל האשראי לזמן קצר, מבנקים ומאחרים, בסעיף 5 (R3) · n9 'קבלת אשראי לזמן קצר מתאגידים בנקאיים ואחרים' → 5: קבלת אשראי לזמן קצר מתאגידים בנקאיים ואחרים (מוצג ברוטו) – כל האשראי לזמן קצר, מבנקים ומאחרים, בסעיף 5 (R3) · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p118, פעילות שוטפת: -10,175, -11,190, -5,102, -7,375, -20,909) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c5 · source irregularities: 1 (see §6) · report notes: 2 · Phase C: item n6 4→5, n7 7→5; verbatim header c1, c3; issues +1.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:24 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'לתקופה של ששה חודשים שהסתיימה 2026' -> 'לתקופה של ששה חודשים שהסתיימה ביום 30 ביוני, 2026 בלתי מבוקר'; header_text c3: 'לתקופה של של… (composites v1_05.png, v2_05.png).

### 771 – גבאי מניבים ופיתוח בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `771_גבאי מניבים ופיתוח בע_מ_2026_Q1_1744961.pdf` (report 1744961, 84 pp.) · cash-flow statement PDF pp. 60, 61 · financing p. 60 · column headers p. 60.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n7 'עליה (ירידה) באשראי לזמן קצר מתאגידים בנקאיים ומאחרים,…' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2 · report notes: 2 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:24 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'שלה המזומנים (באלפי ש"ח) חודשים שהסתיימו ביום 31 במרץ 2 0 2 6' -> 'לשלושה חודשים שהסתיימו ביום 31 במרץ 2026 בלתי מבוקר'; header_text… (composites v1_05.png).
- **Q2 2026** – `771_גבאי מניבים ופיתוח בע_מ_2026_Q2_1763641.pdf` (report 1763641, 88 pp.) · cash-flow statement PDF pp. 62, 63 · financing p. 62 · column headers p. 62.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'עליה באשראי לזמן קצר מתאגידים בנקאיים ומאחרים, נטו' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2, c4 · report notes: 2 · Phase C: verbatim header c1, c2, c3, c4, c5.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:24 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026 (בלתי מבוקר)' -> 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026 בלתי מבוקר'; header_text c2: 'לש… (composites v1_06.png).

### 823 – קבוצת חג'ג' ייזום נדל"ן בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `823_קבוצת חג'ג' ייזום נדל_ן בע_מ_2026_Q1_1745710.pdf` (report 1745710, 87 pp.) · cash-flow statement PDF pp. 59, 60, 61 · financing p. 60 · column headers p. 59.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'הנפקת אופציות' → 2: הנפקת אופציות (כתבי אופציה) של החברה – בדוח על השינויים בהון נזקפה לפרמיה על מניות בהון המיוחס לבעלי מניות החברה (21,15… · n5 'מימוש אופציות' → 2: מימוש אופציות של החברה – סעיף 2 · n6 'רכישת מניות באוצר' → 9: רכישת מניות באוצר – סעיף 9 · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p61, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: 50,997, 57,003, 234,755); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2, c3; context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (8 lines + total), every value (3 columns x 9 lines), the column headers, the units (אלפי ש"ח, printed on p.59 – header strip taken from p.59) and the (*) interest line (appendix B, p.61, positive as printed) comp… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 (בלתי מבוקר)'; header_text… (composites v1_06.png, v2_13.png, v3_04.png).
- **Q2 2026** – `823_קבוצת חג'ג' ייזום נדל_ן בע_מ_2026_Q2_1767825.pdf` (report 1767825, 100 pp.) · cash-flow statement PDF pp. 68, 69, 70 · financing p. 69 · column headers p. 69.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'הנפקת אופציות' → 2: הנפקת אופציות (כתבי אופציה) של החברה – בדוח על השינויים בהון נזקפה לפרמיה על מניות בהון המיוחס לבעלי מניות החברה – תמור… · n5 'מימוש אופציות' → 2: מימוש אופציות של החברה – סעיף 2 · n6 'רכישת מניות באוצר' → 9: רכישת מניות באוצר – סעיף 9 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p70, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: 85,960, 94,563, 34,963, 37,560, 234,755); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2, c3, c4; (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (9 lines + total), every value (5 columns x 10 lines), the column headers, the units (אלפי ש"ח) and the (*) interest line (appendix B, p.70, positive as printed) compared digit by digit with the 220-DPI review ren… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי מבוקר)'; header_text… (composites v1_06.png, v2_14.png).

### 1039 – אלביט נדל"ן בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1039_אלביט נדל_ן בע_מ_2026_Q1_1743815.pdf` (report 1743815, 80 pp.) · cash-flow statement PDF pp. 49, 50, 51 · financing p. 50 · column headers p. 50.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'שינוי בהלוואות לזמן קצר (כולל משיכת יתר) (ראה באור 4.ז…' → 5: שינוי בהלוואות לזמן קצר (כולל משיכת יתר), מוצג נטו – אשראי לזמן קצר → סעיף 5 (R3) · n5 'הזרמת הון זשמ"ש' → 6: הזרמת הון של בעלי זכויות שאינן מקנות שליטה (זשמ"ש) לחברה בת – סעיף 6 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: context sections (captions).
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (6 lines + total), every value (3 columns), the column headers, the units (אלפי ש"ח) compared digit by digit with the 220-DPI zoom of the financing section (screenshots PDF p.3); operating page 49 and investing se… Phase C: context_sections p51: None -> ['נספח (א) – חברה שאוחדה לראשונה'] (composites v3_05.png).
- **Q2 2026** – `1039_אלביט נדל_ן בע_מ_2026_Q2_1764263.pdf` (report 1764263, 92 pp.) · cash-flow statement PDF pp. 54, 55 · financing p. 55 · column headers p. 55.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'שינוי בהלוואות לזמן קצר (כולל משיכת יתר)' → 5: שינוי בהלוואות לזמן קצר (כולל משיכת יתר), מוצג נטו – אשראי לזמן קצר → סעיף 5 (R3) · n6 'הזרמת הון זשמ"ש' → 6: הזרמת הון של בעלי זכויות שאינן מקנות שליטה (זשמ"ש) לחברה בת – סעיף 6 · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (7 lines + total), every value (5 columns; blank cells of lines 2 and 5 confirmed blank on the image – line 2 has '-' only in the 3-months-2026 column), the column headers, the units (אלפי ש"ח) compared digit by d…

### 1068 – שיכון ובינוי בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1068_שיכון ובינוי בע_מ_2026_Q1_1744574.pdf` (report 1744574, 108 pp.) · cash-flow statement PDF pp. 45, 46 · financing p. 46 · column headers p. 46.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: מליוני ש"ח (ש"ח, מיליונים). Text layer: usable.
  - Lines: 10 + total; אחר [11, 7, 49]; check 0 in every column.
  - Judgement calls: n2 'הנפקת מניות מחברות מוחזקות' → 6: הנפקת מניות של חברה מאוחדת (שיכון ובינוי אנרגיה) לציבור – ינואר 2026: 62,662,900 מניות ו-31,331,450 כתבי אופציה (סדרה 1… · n7 'תמורה מנגזרים, נטו' → אחר: תמורה מנגזרים, נטו (סילוק נגזרים) – אינה מתאימה לאף סעיף 1–14 → 'אחר' (מוסכמה 7: סילוק נגזרים/גידור) · n8 'שינוי באשראי לזמן קצר, נטו' → 5: שינוי באשראי לזמן קצר, נטו – סעיף 5 · n10 'דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה בחברה מאו…' → 12: דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה בחברה מאוחדת – סעיף 12 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · report notes: 3.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (10 lines + total), every value (3 columns), the column headers, the units (מליוני ש"ח) compared digit by digit with the 220-DPI zoom of the financing section (screenshots PDF p.3); operating page 45 viewed (scree…
- **Q2 2026** – `1068_שיכון ובינוי בע_מ_2026_Q2_1764659.pdf` (report 1764659, 130 pp.) · cash-flow statement PDF pp. 58, 59 · financing p. 59 · column headers p. 59.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: מליוני ש"ח (ש"ח, מיליונים). Text layer: usable.
  - Lines: 10 + total; אחר [11, 7, 0, 0, 49]; check 0 in every column.
  - Judgement calls: n2 'הנפקת מניות מחברות מוחזקות' → 6: הנפקת מניות של חברה מאוחדת (שיכון ובינוי אנרגיה) לציבור – ינואר 2026: מניות וכתבי אופציה (סדרה 1) בתמורה לכ-232 מליון ש… · n7 'תמורה (סילוק) מנגזרים, נטו' → אחר: תמורה (סילוק) מנגזרים, נטו – אינה מתאימה לאף סעיף 1–14 → 'אחר' (מוסכמה 7: סילוק נגזרים/גידור); בדוח Q1: 'תמורה מנגזרים,… · n8 'שינוי באשראי לזמן קצר, נטו' → 5: שינוי באשראי לזמן קצר, נטו – סעיף 5 · n10 'דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה בחברה מאו…' → 12: דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה בחברה מאוחדת – סעיף 12 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c4 · report notes: 3.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (10 lines + total), every value (5 columns), the column headers, the units (מליוני ש"ח) compared digit by digit with the 220-DPI zoom of the financing section (screenshots PDF p.6); operating page 58 and the inves…

### 1083 – קרדן נדל"ן יזום ופיתוח בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1083_קרדן נדל_ן יזום ופיתוח בע_מ_2026_Q1_1742346.pdf` (report 1742346, 71 pp.) · cash-flow statement PDF pp. 48, 49, 50 · financing p. 49 · column headers p. 49.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'תמורה ממימוש אופציות לעובדים' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · n7 'חלוקה לבעלי זכויות שאינן מקנות שליטה' → 12: חלוקה (דיבידנד) לבעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 12 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p48, פעילות שוטפת: -2,478, -1,374, -17,849); 'ב) ריבית ששולמה והוונה למלאי' (p50, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): -2,709, -3,798, -23,751) → row [-5,187, -5,172, -41,600]; remark: הרכיב שבנספח ('ריבית ששולמה והוונה למלאי') מודפס ללא סוגריים ונרשם כאן בסימן תשלום (שלילי), כדי שסכום השורה יציג את סך הריבית ששולמה מחוץ לפעילות המימון · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 3 · Phase C: context sections (captions); (*) section canonical 2; (*) note wording.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (word rows rebuilt from coordinates because each line's words are stored reversed). Builder's own first image views (10:31-10:36) were NOT displayed (image cap) and are no… Phase C: outside_sections {'2': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_41.png, v3_05.png).
- **Q2 2026** – `1083_קרדן נדל_ן יזום ופיתוח בע_מ_2026_Q2_1763408.pdf` (report 1763408, 73 pp.) · cash-flow statement PDF pp. 49, 50, 51 · financing p. 50 · column headers p. 50.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'תמורה ממימוש אופציות לעובדים' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · n7 'חלוקה לבעלי זכויות שאינן מקנות שליטה' → 12: חלוקה (דיבידנד) לבעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 12 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p49, פעילות שוטפת: -18,591, -8,844, -16,113, -7,470, -17,849); 'ב) ריבית ששולמה והוונה למלאי' (p51, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): -9,476, -11,686, -6,767, -7,888, -23,751) → row [-28,067, -20,530, -22,880, -15,358, -41,600]; remark: הרכיב שבנספח ('ריבית ששולמה והוונה למלאי') מודפס ללא סוגריים ונרשם כאן בסימן תשלום (שלילי), כדי שסכום השורה יציג את סך הריבית ששולמה מחוץ לפעילות המימון · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 3 · Phase C: context sections (captions); (*) section canonical 2; (*) note wording.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (repaired font; words rebuilt from coordinates). Builder's own first image views (10:34-10:37) were NOT displayed (image cap) and are not relied on. Visual verification: (… Phase C: outside_sections {'2': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_42.png, v3_06.png).

### 1096 – דניה סיבוס בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1096_דניה סיבוס בע_מ_2026_Q1_1742403.pdf` (report 1742403, 38 pp.) · cash-flow statement PDF pp. 29, 30 · financing p. 30 · column headers p. 30.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 5 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'שינוי באשראי מתאגידים בנקאיים ונותני אשראי אחרים לזמן…' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 לפי כלל המיפוי · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 1 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס 2026 (בלתי מבוקר) אלפי ש"ח' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס 2026 (בלתי… (composites v1_07.png).
- **Q2 2026** – `1096_דניה סיבוס בע_מ_2026_Q2_1762282.pdf` (report 1762282, 41 pp.) · cash-flow statement PDF pp. 30, 31 · financing p. 31 · column headers p. 31.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 5 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'שינוי באשראי מתאגידים בנקאיים ונותני אשראי אחרים לזמן…' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 לפי כלל המיפוי · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 1 · Phase C: verbatim header c1, c2, c3, c4, c5.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לתקופה של ששה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי מבוקר) אלפי ש"ח' -> 'לתקופה של ששה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי מ… (composites v1_07.png).

### 1193 – י.ח.דמרי בניה ופיתוח בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1193_י.ח.דמרי בניה ופיתוח בע_מ_2026_Q1_1744429.pdf` (report 1744429, 68 pp.) · cash-flow statement PDF pp. 39, 40, 41 · financing p. 40 · column headers p. 40.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'תמורה מהנפקת מניות ואופציות ומימושי אופציות למניות, בנ…' → 1: שורה משולבת (הנפקת מניות ואופציות ומימושי אופציות, בניכוי הוצאות הנפקה) שאינה מפוצלת בדוח – סווגה לסעיף 1 לפי המוסכמה (… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'תשלומי ריבית' (p39, פעילות שוטפת: -44,497, -39,467, -213,780) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla…
- **Q2 2026** – `1193_י.ח.דמרי בניה ופיתוח בע_מ_2026_Q2_1764665.pdf` (report 1764665, 73 pp.) · cash-flow statement PDF pp. 42, 43, 44 · financing p. 43 · column headers p. 43.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'תמורה מהנפקת מניות ואופציות ומימושי אופציות למניות, בנ…' → 1: שורה משולבת (הנפקת מניות ואופציות ומימושי אופציות, בניכוי הוצאות הנפקה) שאינה מפוצלת בדוח – סווגה לסעיף 1 לפי המוסכמה (… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'תשלומי ריבית' (p42, פעילות שוטפת: -106,592, -100,774, -62,095, -61,307, -213,780) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla…

### 1330 – פרשקובסקי השקעות ובניין בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1330_פרשקובסקי השקעות ובניין בע_מ_2026_Q1_1742648.pdf` (report 1742648, 83 pp.) · cash-flow statement PDF pp. 53, 54 · financing p. 53 · column headers p. 53.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'אשראי מתאגידים בנקאיים והלוואות לזמן קצר, נטו' → 5: אשראי מתאגידים בנקאיים והלוואות לזמן קצר, נטו – סעיף 5 · n7 'רכישת מניות באוצר' → 9: רכישת מניות באוצר – סעיף 9 · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'נספח ב' – מידע נוסף על תזרימי מזומנים: מזומנים ששולמו במשך…' (p54, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 49,718, 42,490, 196,235); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (7 lines + total), every value (3 columns), the column headers, the units (אלפי ש"ח) and the appendix (*) line (נספח ב', p. 54: finance costs paid incl. capitalised) compared digit by digit with 220-DPI renders (t… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_28.png, v3_06.png).
- **Q2 2026** – `1330_פרשקובסקי השקעות ובניין בע_מ_2026_Q2_1764951.pdf` (report 1764951, 88 pp.) · cash-flow statement PDF pp. 57, 58 · financing p. 57 · column headers p. 57.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'אשראי מתאגידים בנקאיים והלוואות לזמן קצר נטו' → 5: אשראי מתאגידים בנקאיים והלוואות לזמן קצר, נטו – סעיף 5 · n7 'רכישת מניות באוצר' → 9: רכישת מניות באוצר – סעיף 9 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'נספח ב' – מידע נוסף על תזרימי מזומנים: מזומנים ששולמו במשך…' (p58, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 114,720, 93,435, 65,002, 50,945, 196,235); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (8 lines + total), every value (5 columns), the column headers, the units (אלפי ש"ח) and the appendix (*) line (נספח ב', p. 58: finance costs paid incl. capitalised) compared digit by digit with 220-DPI renders (t… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_29.png, v3_07.png).

### 1331 – קבוצת צילו-בלו בע"מ

- **Q1 2026: not in the folder** (listed in `חסרים והערות` as `דוח חסר`; not downloaded – out of scope).
- **Q2 2026** – `1331_קבוצת צילו-בלו בע_מ_2026_Q2_1766504.pdf` (report 1766504, 46 pp.) · cash-flow statement PDF pp. 30, 31, 32 · financing p. 30 · column headers p. 30.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 5 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'רכישת מניות באוצר' → 9: רכישת מניות באוצר – סעיף 9 · n5 'אשראי והלוואות מתאגידים בנקאיים, נטו' → 5: אשראי והלוואות מתאגידים בנקאיים, מוצג נטו ללא ציון תקופה – סעיף 5 (R3: שורת אשראי נטו ללא תקופה) · (+3 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'מזומנים ששולמו במשך התקופה עבור: ריבית' (p32, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 5,006, 5,468, 21,749); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3 · Phase C: context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 2 Builder (2026-11-10): The text layer returns the words of each line in reversed order, so every label was read from the image: every line text, every value (3 columns x 5 lines + total), the column headers (6M to 30.06.2026/2025, FY 31.12.2025; no 3-m… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_30.png, v3_07.png).

### 1338 – אפריקה ישראל מגורים בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1338_אפריקה ישראל מגורים בע_מ_2026_Q1_1742497.pdf` (report 1742497, 79 pp.) · cash-flow statement PDF pp. 57, 58 · financing p. 58 · column headers p. 58.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c1 · report notes: 2 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס 2026 (בלתי… (composites v1_07.png).
- **Q2 2026** – `1338_אפריקה ישראל מגורים בע_מ_2026_Q2_1763151.pdf` (report 1763151, 81 pp.) · cash-flow statement PDF pp. 57, 58 · financing p. 58 · column headers p. 58.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 3 · Phase C: verbatim header c1, c2, c3, c4, c5.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 אלפי ש"ח' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי מבוקר)'; hea… (composites v1_08.png).

### 1484 – מצלאוי חברה לבנין בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (-23), C2 3 חודשים שהסתיימו ב-31.03.2025 total (23,312); C2 per-item INFO rows (explained): 4.
- **Q1 2026** – `1484_מצלאוי חברה לבנין בע_מ_2026_Q1_1743676.pdf` (report 1743676, 44 pp.) · cash-flow statement PDF pp. 33, 34 · financing p. 34 · column headers p. 34.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 4 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'עליה באשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: עליה באשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו – כולל אשראי ממלווים אחרים – סעיף 5 · (+3 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p33, פעילות שוטפת: -1,679, -3,082, -11,808) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2 · source irregularities: 1 (see §6) · report notes: 3 · Phase C: verbatim header c1, c2; issues +1.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (4 lines + total), every value (3 columns x 5 lines), the column headers, the units (אלפי ש"ח) and the (*) interest line (p.33, operating) compared digit by digit with the 220-DPI review render of the header strip… Phase C: header_text c1: 'ל-3 החודשים שהסתיימו 2026' -> 'ל-3 החודשים שהסתיימו ביום 31 במרס 2026 בלתי מבוקר'; header_text c2: 'ל-3 החודשים שהסתיימו ביום 31 במר… (composites v1_08.png, v2_47.png).
- **Q2 2026** – `1484_מצלאוי חברה לבנין בע_מ_2026_Q2_1767668.pdf` (report 1767668, 48 pp.) · cash-flow statement PDF pp. 35, 36 · financing p. 36 · column headers p. 36.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 5 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'רכישת מניות באוצר, נטו' → 9: רכישת מניות באוצר, נטו – סעיף 9 · n5 'עליה (ירידה) באשראי לזמן קצר מתאגידים בנקאיים ואחרים,…' → 5: עליה (ירידה) באשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו – כולל אשראי ממלווים אחרים – סעיף 5 · (+3 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p35, פעילות שוטפת: -5,900, -4,855, -4,221, -1,773, -11,808) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2, c4 · source irregularities: 2 (see §6) · report notes: 3 · Phase C: verbatim header c1, c2, c3, c4; issues +1.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (5 lines + total), every value (5 columns x 6 lines), the column headers, the units (אלפי ש"ח) and the (*) interest line (p.35, operating) compared digit by digit with the 220-DPI review render of the header strip… Phase C: header_text c1: 'ל-6 החודשים שהסתיימו 2026' -> 'ל-6 החודשים שהסתיימו ביום 30 ביוני 2026 בלתי מבוקר'; header_text c2: 'ל-6 החודשים שהסתיימו ביום 30 בי… (composites v1_08.png, v2_48.png).

### 1490 – ב.ס.ר הנדסה ופיתוח בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2025 total (-2); C2 per-item INFO rows (explained): 4.
- **Q1 2026** – `1490_ב.ס.ר הנדסה ופיתוח בע_מ_2026_Q1_1741954.pdf` (report 1741954, 72 pp.) · cash-flow statement PDF pp. 36, 37, 38 · financing p. 37 · column headers p. 37.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת (פרעון) אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נ…' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, מוצג נטו – סעיף 5 (כולל מלווים אחרים ולא רק תאגידים בנקאיים) · n2 'קבלת (פרעון) הלוואות לזמן ארוך מתאגידים בנקאיים ואחרים' → 4/7 לפי סימן: קבלת (פירעון) הלוואות לזמן ארוך מתאגידים בנקאיים ואחרים – שורה נטו של אותו מכשיר: בכל עמודה בנפרד, סכום חיובי → סעיף 4,… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c1, c2 · report notes: 3 · Phase C: verbatim header c1, c2; context sections (captions).
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'ל-3 החודשים שהסתיימו ביום 31 במרס 2026 בלתי מבוקר אלפי ש"ח' -> 'ל-3 החודשים שהסתיימו ביום 31 במרס 2026 בלתי מבוקר'; header_text c2:… (composites v1_09.png, v3_08.png).
- **Q2 2026** – `1490_ב.ס.ר הנדסה ופיתוח בע_מ_2026_Q2_1764944.pdf` (report 1764944, 89 pp.) · cash-flow statement PDF pp. 48, 49, 50 · financing p. 49 · column headers p. 49.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת (פרעון) אשראי לזמן קצר מתאגידים בנקאיים, אחרים וצ…' → 5: אשראי לזמן קצר מתאגידים בנקאיים, אחרים וצדדים קשורים, מוצג נטו – סעיף 5 (כולל מלווים אחרים וצדדים קשורים ולא רק תאגידים… · n2 'קבלת (פרעון) הלוואות לזמן ארוך מתאגידים בנקאיים, אחרים…' → 4/7 לפי סימן: קבלת (פירעון) הלוואות לזמן ארוך מתאגידים בנקאיים, אחרים וצדדים קשורים, נטו – שורה נטו של אותו מכשיר: בכל עמודה בנפרד, ס… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 3 · Phase C: verbatim header c1, c2, c3, c4; context sections (captions).
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'ל-6 החודשים שהסתיימו ביום 30 ביוני 2026' -> 'ל-6 החודשים שהסתיימו ביום 30 ביוני 2026 בלתי מבוקר'; header_text c2: 'ל-6 החודשים שהסתי… (composites v1_09.png, v3_08.png).

### 1502 – מירלנד דיוולופמנט קורפריישן פי אל סי

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1502_מירלנד דיוולופמנט קורפריישן פי אל סי_2026_Q1_1744791.pdf` (report 1744791, 83 pp.) · cash-flow statement PDF pp. 38, 39, 40 · financing p. 39 · column headers p. 39.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי דולר ארה"ב (דולר ארה"ב, אלפים). Text layer: usable.
  - Lines: 0 + total; אחר 0; check 0 in every column.
  - Judgement calls: none beyond the wording of the lines (0).
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p38, פעילות שוטפת: 0, 0, 0); remark: השורה מוצגת עם '-' (0) בכל התקופות · dividends paid: no line in the statement → (*) row 0.
  - Flags: source irregularities: 1 (see §6) · report notes: 3 · Phase C: context sections (captions); (*) note wording; issues +1.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer. Builder's own first image views (10:37-10:39) were NOT displayed (image cap) and are not relied on. Visual verification: (1) read-only sub-agent with a fresh image budget… Phase C: info_notes.interest removed (uniform note composed from sections); info_note_extra.interest; context_sections p40: None -> ['פעילות מהותית שלא במזומן… (composites v3_09.png).
- **Q2 2026** – `1502_מירלנד דיוולופמנט קורפריישן פי אל סי_2026_Q2_1767654.pdf` (report 1767654, 84 pp.) · cash-flow statement PDF pp. 39, 40, 41 · financing p. 40 · column headers p. 40.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי דולר ארה"ב (דולר ארה"ב, אלפים). Text layer: usable.
  - Lines: 1 + total; אחר 0; check 0 in every column.
  - Judgement calls: none beyond the wording of the lines (1).
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p39, פעילות שוטפת: 0, 0, 0, 0, 0); remark: השורה מוצגת עם '-' (0) בכל התקופות · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3 · Phase C: context sections (captions); (*) note wording.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer. Builder's own first image views (10:38-10:39) were NOT displayed (image cap) and are not relied on. Visual verification: (1) read-only sub-agent with a fresh image budget… Phase C: info_notes.interest removed (uniform note composed from sections); info_note_extra.interest; context_sections p41: None -> ['פעילות מהותית שלא במזומן… (composites v3_09.png).

### 1532 – גפן מגורים והתחדשות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1532_גפן מגורים והתחדשות בע_מ_2026_Q1_1742408.pdf` (report 1742408, 65 pp.) · cash-flow statement PDF pp. 32, 33, 34 · financing p. 32 · column headers p. 32.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 4 + total; אחר 0; check 0 in every column.
  - Judgement calls: n2 'קבלת אשראי מנותני אשראי אחרים' → 5: קבלת אשראי מנותני אשראי אחרים (ברוטו) – אשראי לזמן קצר: במאזן 'אשראי מתאגידים בנקאיים ונותני אשראי אחרים' מוצג בהתחייבו… · n3 'הנפקת מניות ואופציות לצד קשור' → 1: הקצאה פרטית של מניות ואופציות (חבילה) לצד קשור – מנכ"ל החברה (ביאור: 14,195,200 ש"ח כנגד הקצאת 22,180,000 מניות רגילות… · n4 'פירעון אשראי מנותני אשראי אחרים' → 5: פירעון אשראי מנותני אשראי אחרים (ברוטו) – אשראי לזמן קצר (התחייבות שוטפת; ההלוואה מגוף חוץ בנקאי בסך 5,200 נפרעה) – סעי… · (+1 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p33, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: 1,748, 1,751, 3,603); 'ריבית ששולמה בגין חכירות' (p33, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: 3, 0, 13); 'ריבית ששולמה בגין חכירות' (p34, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 0, 4, 0) → row [1,751, 1,755, 3,616]; remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים); כולל ריבית ששולמה בגין חכירות; הסכום של ינואר–מרץ 2025 (4) מודפס בדוח זה בנספח ג' (פעולות מהותיות שאינן במזומן) ובדוח Q2 בנספח… · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c1, c2 · source irregularities: 2 (see §6) · report notes: 3 · Phase C: verbatim header c1, c2, c3; (*) section canonical 1,2,3; (*) note wording; issues +1.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לתקופה שהסתיימה יום 31 במרץ 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה שהסתיימה יום 31 במרץ 2026 (בלתי מבוקר)'; header_text c2: 'לתקופה… (composites v1_09.png, v2_19.png).
- **Q2 2026** – `1532_גפן מגורים והתחדשות בע_מ_2026_Q2_1763377.pdf` (report 1763377, 69 pp.) · cash-flow statement PDF pp. 36, 37, 38 · financing p. 36 · column headers p. 36.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n2 'קבלת אשראי מתאגיד בנקאי' → 5: קבלת אשראי מתאגיד בנקאי (ברוטו) – אשראי לזמן קצר: במאזן 'אשראי מתאגידים בנקאיים ונותני אשראי אחרים' מוצג בהתחייבויות שו… · n3 'קבלת אשראי מנותני אשראי אחרים' → 5: קבלת אשראי מנותני אשראי אחרים (ברוטו) – אשראי לזמן קצר (התחייבות שוטפת) – סעיף 5 · n4 'הנפקת מניות ואופציות למנכ"ל החברה' → 1: הקצאה פרטית של מניות ואופציות (חבילה) למנכ"ל החברה – צד קשור (ביאור: 14,195,200 ש"ח כנגד הקצאת 22,180,000 מניות רגילות… · n5 'הנפקת מניות ואופציות למשקיע' → 1: הקצאה פרטית של מניות וכתבי אופציה (חבילה) למשקיע (לאומי פרטנרס – 50,000,000 ש"ח בתמורה כוללת, כולל כתבי אופציה לא סחירי… · n6 'פירעון אשראי מנותני אשראי אחרים' → 5: פירעון אשראי מנותני אשראי אחרים (ברוטו) – אשראי לזמן קצר (התחייבות שוטפת; ההלוואה מגוף חוץ בנקאי בסך 5,200 נפרעה) – סעי… · (+1 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p37, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: 2,377, 1,751, 629, 0, 3,603); 'ריבית ששולמה בגין חכירות' (p37, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: 5, 8, 2, 4, 13) → row [2,382, 1,759, 631, 4, 3,616]; remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים); כולל ריבית ששולמה בגין חכירות · dividends paid: no line in the statement → (*) row 0.
  - Flags: source irregularities: 1 (see §6) · report notes: 3 · Phase C: verbatim header c1, c2, c3, c4, c5; (*) section canonical 1,2; (*) note wording; issues +1.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה יום 30 ביוני 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שישה חודשים שהסתיימה יום 30 ביוני 2026 (בלתי מ… (composites v1_10.png, v2_20.png).

### 1553 – אלמוגים החזקות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1553_אלמוגים החזקות בע_מ_2026_Q1_1745440.pdf` (report 1745440, 72 pp.) · cash-flow statement PDF pp. 46, 47 · financing p. 47 · column headers p. 47.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'קבלת (פירעון) הלוואות בגין פרויקטים, נטו' → 5: הלוואות ליווי בנקאי לפרויקטים, מוצגות נטו ללא ציון תקופה; במאזן הן מסווגות בהתחייבויות השוטפות ('הלוואות מתאגידים בנקאי… · n6 'קבלת (פירעון) הלוואות מתאגידים בנקאיים לזמן ארוך' → 4/7 לפי סימן: קבלה ופירעון של אותן הלוואות לזמן ארוך מוצגים נטו בשורה אחת: סעיף 4 אם הנטו חיובי, סעיף 7 אם שלילי (כאן בכל העמודות שלי… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p46, פעילות שוטפת: -15,719, -11,695, -72,756) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer. Builder's first views of the fin render, pages 46-47 and screenshots s3/s4 (10:39-10:41) were NOT displayed (image cap) and are not relied on. Visual verification: (1) bu…
- **Q2 2026** – `1553_אלמוגים החזקות בע_מ_2026_Q2_1763612.pdf` (report 1763612, 76 pp.) · cash-flow statement PDF pp. 49, 50 · financing p. 50 · column headers p. 50.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'קבלת (פירעון) הלוואות בגין פרויקטים, נטו' → 5: הלוואות ליווי בנקאי לפרויקטים, מוצגות נטו ללא ציון תקופה; במאזן הן מסווגות בהתחייבויות השוטפות ('הלוואות מתאגידים בנקאי… · n6 'קבלת (פירעון) הלוואות מתאגידים בנקאיים לזמן ארוך' → 4/7 לפי סימן: קבלה ופירעון של אותן הלוואות לזמן ארוך מוצגים נטו בשורה אחת: סעיף 4 אם הנטו חיובי, סעיף 7 אם שלילי (כאן בכל העמודות שלי… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p49, פעילות שוטפת: -44,987, -29,941, -29,268, -18,246, -72,756) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer. Builder's first views of the fin render and pages 49-50 (10:40) were NOT displayed (image cap) and are not relied on. Visual verification: (1) builder, on screenshots pag…

### 1561 – הכשרת הישוב התחדשות עירונית בישראל בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1561_הכשרת הישוב התחדשות עירונית בישראל בע_מ_2026_Q1_1741645.pdf` (report 1741645, 28 pp.) · cash-flow statement PDF pp. 22, 23 · financing p. 22 · column headers p. 22.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר מתאגיד בנקאי, נטו' → 5: אשראי לזמן קצר מתאגיד בנקאי, נטו – סעיף 5 · n3 'סכומים שהתקבלו משותף בעסקת פינוי בינוי' → 4: כספים שהתקבלו משותף בעסקת פינוי-בינוי; במאזן המאוחד מוצגים כהתחייבות לא שוטפת ('התחייבות לשותף בעסקת פינוי ובינוי' – 45… · n4 'קיטון בהלוואה מהחברה האם' → 5: קיטון בהלוואה מהחברה האם (בעלת השליטה, הכשרת הישוב מקבוצת נמרודי) – שינוי נטו ללא ציון תקופה – סעיף 5 (R3 + מוסכמות שלב… · n5 'תקבולים מזכויות שאינן מקנות שליטה' → 6: תקבולים מבעלי זכויות שאינן מקנות שליטה בחברה בת (עסקת מנורה 1) – סעיף 6 · (+2 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p23, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: -116, -181, -653) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 1 · Phase C: (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (6 lines + total; line 2 label corrected from the image), every value (3 columns x 7 lines), the column headers, the units ('(באלפי ש"ח)' in the title) and the (*) interest line (appendix A, p.23) compared digit b… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת'}; info_notes.interest removed (uniform note composed from sections) (composites v2_15.png).
- **Q2 2026** – `1561_הכשרת הישוב התחדשות עירונית בישראל בע_מ_2026_Q2_1762505.pdf` (report 1762505, 33 pp.) · cash-flow statement PDF pp. 26, 27 · financing p. 26 · column headers p. 26.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר מתאגיד בנקאי, נטו' → 5: אשראי לזמן קצר מתאגיד בנקאי, נטו – סעיף 5 · n2 'סכומים שהתקבלו משותף בעסקת פינוי בינוי' → 4: כספים שהתקבלו משותף בעסקת פינוי-בינוי; במאזן המאוחד מוצגים כהתחייבות לא שוטפת ('התחייבות לשותף בעסקת פינוי בינוי' – 45,… · n4 'קיטון בהלוואה מהחברה האם' → 5: קיטון בהלוואה מהחברה האם (בעלת השליטה, הכשרת הישוב מקבוצת נמרודי) – שינוי נטו ללא ציון תקופה – סעיף 5 (R3 + מוסכמות שלב… · n5 'תקבולים מזכויות שאינן מקנות שליטה' → 6: תקבולים מבעלי זכויות שאינן מקנות שליטה בחברה בת (עסקת מנורה 1) – סעיף 6 · (+2 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p27, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: -229, -315, -113, -134, -653) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 1 · Phase C: verbatim header c1; (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (6 lines + total), every value (5 columns x 7 lines), the column headers, the units ('(באלפי ש"ח)' in the title) and the (*) interest line (p.27) compared digit by digit with the 220-DPI review render of the heade… Phase C: header_text c1: 'המזומנים (באלפי ש"ח) לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 בלתי מבוקר' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני… (composites v1_10.png, v2_16.png).

### 1618 – קבוצת אשטרום בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `1618_קבוצת אשטרום בע_מ_2026_Q1_1743867.pdf` (report 1743867, 81 pp.) · cash-flow statement PDF pp. 55, 56, 57 · financing p. 56 · column headers p. 56.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (Hebrew in logical order).
  - Lines: 13 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 לפי כלל המיפוי · n9 'תמורה ממימוש אופציות' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · n10 'הנפקה לבעלי זכויות שאינן מקנות שליטה' → 6: הנפקת זכויות בחברה בת מאוחדת לבעלי זכויות שאינן מקנות שליטה – סעיף 6 · n11 'רכישה מבעלי זכויות שאינן מקנות שליטה' → 14: רכישת זכויות נוספות בחברה בת מאוחדת מבעלי זכויות שאינן מקנות שליטה (עסקה הונית, ללא שינוי בשליטה) – סעיף 14 · n13 'דיבידנד לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · report notes: 2 · Phase C: context sections (captions).
  - Verification: Builder (pilot attempt 2) (2026-11-09): Values parsed from the PDF text layer with coordinates (extract_report.py: words grouped into rows, value groups assigned to columns by x-position, parentheses -> negative, dash -> 0) and cross-checked digit by digit against a 20… Phase C: context_sections p57: None -> ['פעילויות מהותיות שלא במזומן'] (composites v3_10.png).
- **Q2 2026** – `1618_קבוצת אשטרום בע_מ_2026_Q2_1766160.pdf` (report 1766160, 97 pp.) · cash-flow statement PDF pp. 66, 67, 68 · financing p. 67 · column headers p. 67.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (Hebrew in logical order).
  - Lines: 13 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 לפי כלל המיפוי · n9 'תמורה ממימוש אופציות' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · n10 'הנפקה לבעלי זכויות שאינן מקנות שליטה' → 6: הנפקת זכויות בחברה בת מאוחדת לבעלי זכויות שאינן מקנות שליטה – סעיף 6 · n11 'רכישה מבעלי זכויות שאינן מקנות שליטה' → 14: רכישת זכויות נוספות בחברה בת מאוחדת מבעלי זכויות שאינן מקנות שליטה (עסקה הונית, ללא שינוי בשליטה) – סעיף 14 · n13 'דיבידנד לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · report notes: 2 · Phase C: context sections (captions).
  - Verification: Builder (pilot attempt 2) (2026-11-09): Values parsed from the PDF text layer with coordinates (extract_report.py: words grouped into rows, value groups assigned to columns by x-position, parentheses -> negative, dash -> 0) and cross-checked digit by digit against a 20… Phase C: context_sections p68: None -> ['פעילויות מהותיות שלא במזומן'] (composites v3_10.png).

### 1622 – אקסטל לימיטד

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1622_אקסטל לימיטד_2026_Q1_1745241.pdf` (report 1745241, 107 pp.) · cash-flow statement PDF pp. 51, 52 · financing p. 52 · column headers p. 52.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: באלפי דולר ארה"ב (דולר ארה"ב, אלפים). Text layer: usable.
  - Lines: 13 + total; אחר [0, 0, -316]; check 0 in every column.
  - Judgement calls: n2 'השקעות הון על ידי בעלי זכויות שאינן מקנות שליטה' → 6: השקעות הון של בעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 6 · n3 'החזר הון לבעלי זכויות שאינן מקנות שליטה' → 12: החזר הון (משיכת הון) לבעלי זכויות שאינן מקנות שליטה – חלוקה לזשמ"ש בקשר עם משקיעי EB-5 (דוח הדירקטוריון: קיטון בהון 9,0… · n4 'דיבידנדים ששולמו לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n9 'קבלת הלוואות מבעל שליטה' → 5: הלוואה מבעל השליטה ללא ציון תקופה; במאזן מוצגת בהתחייבויות השוטפות ('הלוואות מבעל שליטה' 34,000 ליום 31.12.2025) – אשרא… · n10 'מקדמות (החזר מקדמות) מ-Extell Holdings I LLC' → 5: מקדמות מ-Extell Holdings I LLC (JV2 – ישות בשליטת בעל השליטה), מוצגות נטו (קבלה/החזר) ללא ציון תקופה; במאזן ליום 31.12.… · n11 'תשלומים למשקיעי EB-5' → 7: הלוואות EB-5: תשלומים למשקיעי EB-5 (החזר כספי השקעה/מקדמות של משקיעי EB-5; כספי משקיעים שטרם אושרו מוצגים כהתחייבות ומס… · n12 'נגזרים פיננסיים' → אחר: תשלומים בגין נגזרים פיננסיים (סילוק נגזרים) – אינו מתאים לאף אחד מסעיפים 1–14 – אחר (מוסכמות שלב B §7) · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 4 Builder (2026-11-10): Every line text (13 lines + total; line 10 spacing 'מ-Extell' corrected – confirmed by the sub-agent at 300/600 DPI and by the builder on a displayed 400-DPI crop at 11:20), every value (3 columns), the column headers (3M 31.03.2…
- **Q2 2026** – `1622_אקסטל לימיטד_2026_Q2_1766453.pdf` (report 1766453, 117 pp.) · cash-flow statement PDF pp. 56, 57, 58 · financing p. 57 · column headers p. 57.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: באלפי דולר ארה"ב (דולר ארה"ב, אלפים). Text layer: usable.
  - Lines: 15 + total; אחר [-21, -23, -21, -23, -316]; check 0 in every column.
  - Judgement calls: n2 'השקעות הון על ידי בעלי זכויות שאינן מקנות שליטה' → 6: השקעות הון של בעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 6 · n3 'החזר הון לבעלי זכויות שאינן מקנות שליטה' → 12: החזר הון (משיכת הון) לבעלי זכויות שאינן מקנות שליטה – חלוקה לזשמ"ש בקשר עם משקיעי EB-5 – סעיף 12 (מוסכמות שלב B §2: חלו… · n4 'דיבידנדים ששולמו לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n9 'קבלת הלוואות מבעל שליטה' → 5: הלוואה מבעל השליטה ללא ציון תקופה; במאזן מוצגת בהתחייבויות השוטפות ('הלוואות מבעל שליטה': 20,000 ליום 30.06.2026, 34,00… · n10 'פרעון הלוואות מבעל שליטה' → 5: פירעון הלוואה מבעל השליטה (באור 7ח: 10,000 ביום 1.4.2026 ו-4,000 ביום 5.5.2026); ההלוואה ללא ציון תקופה ומוצגת בהתחייבו… · n12 'מקדמות (החזר מקדמות) מ- Extell Holdings I LLC' → 5: מקדמות מ-Extell Holdings I LLC (JV2), מוצגות נטו (קבלה/החזר) ללא ציון תקופה; התקבלו ב-2025 (35,000) והוחזרו ברבעון 1/20… · n13 'תשלומים למשקיעי EB-5' → 7: הלוואות EB-5: תשלומים למשקיעי EB-5 (החזר כספי השקעה/מקדמות של משקיעי EB-5; כספי משקיעים שטרם אושרו מוצגים כהתחייבות ומס… · n14 'נגזרים פיננסיים' → אחר: תשלומים בגין נגזרים פיננסיים (סילוק נגזרים) – אינו מתאים לאף אחד מסעיפים 1–14 – אחר (מוסכמות שלב B §7) · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: source irregularities: 1 (see §6) · report notes: 2 · Phase C: context sections (captions); issues +1.
  - Verification: Phase B batch 4 Builder (2026-11-10): Every line text (15 lines incl. 4 wrapped labels + total), every value (5 columns, incl. the positive 1,500 in the 3M-2026 column of 'החזר הון לבעלי זכויות שאינן מקנות שליטה'), the column headers (6M and 3M 30.06.2026/2025, FY 31… Phase C: context_sections p58: None -> ['(א) פעילויות שאינן במזומן', '(ב) השקעות הון שאינן במזומן']; issues += 1 (composites v2_52.png, v3_11.png).

### 1644 – קבוצת אורון אחזקות והשקעות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1644_קבוצת אורון אחזקות והשקעות בע_מ_2026_Q1_1741690.pdf` (report 1741690, 66 pp.) · cash-flow statement PDF pp. 47, 48 · financing p. 48 · column headers p. 48.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'אשראי לזמן קצר מתאגידים בנקאיים ומאחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ומאחרים, מוצג נטו – סעיף 5 (כולל מלווים אחרים ולא רק תאגידים בנקאיים) · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 2 Builder (2026-11-10): The text layer returns the words of each line in reversed order, so every label was compared with the image: every line text, every value (3 columns x 9 lines + total), the column headers (3M to 31.03.2026/2025, FY 31.12.2025), t…
- **Q2 2026** – `1644_קבוצת אורון אחזקות והשקעות בע_מ_2026_Q2_1763699.pdf` (report 1763699, 77 pp.) · cash-flow statement PDF pp. 52, 53 · financing p. 53 · column headers p. 53.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n6 'אשראי לזמן קצר מתאגידים בנקאיים ומאחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ומאחרים, מוצג נטו – סעיף 5 (כולל מלווים אחרים ולא רק תאגידים בנקאיים) · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c4 · report notes: 1.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (5 columns x 9 lines + total; the blank 3M-2026 cell of 'הנפקת הון, נטו' confirmed), the column headers (6M/3M to 30.06.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with the…

### 1680 – לסיכו בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1680_לסיכו בע_מ_2026_Q1_1745093.pdf` (report 1745093, 68 pp.) · cash-flow statement PDF pp. 31, 32, 33 · financing p. 32 · column headers p. 32.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר [-1,000, 0, 0]; check 0 in every column.
  - Judgement calls: n2 'דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 12 · n5 'תשלום תמורה מותנית בגין צירוף עסקים' → אחר: תשלום תמורה מותנית בגין צירוף עסקים – אינו מתאים לאף אחד מסעיפים 1–14 (מוסכמות שלב B §7: תמורה מותנית → 'אחר') · n7 'קבלת (פירעון) הלוואות ואשראי לזמן קצר מתאגידים בנקאיים…' → 5: הלוואות ואשראי לזמן קצר מתאגידים בנקאיים, מוצג נטו – סעיף 5 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p31, פעילות שוטפת: -1,537, -1,362, -9,730) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · report notes: 2 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:25 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'לתקופה של שלושה חודשים שנסתיימה ביום 31 במרס 2 0 2 6' -> 'לתקופה של שלושה חודשים שנסתיימה ביום 31 במרס 2026 בלתי מבוקר'; header_text… (composites v1_10.png).
- **Q2 2026** – `1680_לסיכו בע_מ_2026_Q2_1764623.pdf` (report 1764623, 84 pp.) · cash-flow statement PDF pp. 36, 37, 38 · financing p. 37 · column headers p. 37.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר [-1,000, 0, 0, 0, 0]; check 0 in every column.
  - Judgement calls: n2 'דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 12 · n5 'תשלום תמורה מותנית בגין צירוף עסקים' → אחר: תשלום תמורה מותנית בגין צירוף עסקים – אינו מתאים לאף אחד מסעיפים 1–14 (מוסכמות שלב B §7: תמורה מותנית → 'אחר') · n7 'קבלת (פירעון) הלוואות ואשראי לזמן קצר מתאגידים בנקאיים…' → 5: הלוואות ואשראי לזמן קצר מתאגידים בנקאיים, מוצג נטו – סעיף 5 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p36, פעילות שוטפת: -6,100, -4,274, -4,563, -2,912, -9,730) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c4 · source irregularities: 1 (see §6) · report notes: 3 · Phase C: verbatim header c1, c2, c3, c4, c5.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:25 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'מאוחדים לתקופה של ששה חודשים שנסתיימה ביום 30 ביוני 2 0 2 6' -> 'לתקופה של ששה חודשים שנסתיימה ביום 30 ביוני 2026 בלתי מבוקר'; heade… (composites v1_11.png).

### 1703 – קבוצת אחים יעקובי (ואי.אס.בי)בע"מ

- **Q1 2026: not in the folder** (listed in `חסרים והערות` as `דוח חסר`; not downloaded – out of scope).
- **Q2 2026** – `1703_קבוצת אחים יעקובי (ואי.אס.בי)בע_מ_2026_Q2_1767724.pdf` (report 1767724, 43 pp.) · cash-flow statement PDF pp. 31, 32 · financing p. 32 · column headers p. 32.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 5 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר מתאגידים בנקאיים ומאחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ומאחרים, נטו – כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; סעיף 5 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p31, פעילות שוטפת: -6,105, -4,708, -13,558) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי… (composites v1_11.png).

### 1722 – חג'ג' אירופה דיוולופמנט צ.ש. בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1722_חג'ג' אירופה דיוולופמנט צ.ש. בע_מ_2026_Q1_1745698.pdf` (report 1745698, 113 pp.) · cash-flow statement PDF pp. 66 · financing p. 66 · column headers p. 66.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי אירו (אירו, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר [24, 203, 360]; check 0 in every column.
  - Judgement calls: n1 'הנפקת מניות וכתבי אופציה, נטו' → 1: הנפקת מניות וכתבי אופציה (לא רשומים) יחד, נטו – לא מפוצל בדוח; מניות + אופציות – סעיף 1 (מוסכמת שלב B §6) · n2 'מימוש כתבי אופציה' → 2: מימוש כתבי אופציה (סדרה 1 / לא רשומים) – סעיף 2; התאים בעמודות 2025 ריקים בדוח – נרשם 0 · n3 'הלוואות מתאגיד בנקאי, נטו' → 4: הלוואות מתאגיד בנקאי, נטו – לפי דוח הדירקטוריון (דוח Q2 2026, עמ' 23 ו-31): קבלת הלוואות מתאגיד בנקאי בסך כ-27.3 מיליון… · n4 'תקבולים בגין הלוואות לרוכשי דירות, נטו' → אחר: גביית הלוואות שהעמידה החברה לרוכשי דירות (נכס במאזן – 'הלוואות לרוכשי דירות'), מוצגת בדוח בפעילות מימון. אינה קבלת אשרא… · n5 'החזר השקעה לזכויות שאינן מקנות שליטה' → 12: החזר השקעה (הון) לבעלי זכויות שאינן מקנות שליטה – חלוקה/משיכה לבעלי זשמ"ש – סעיף 12 (R3: distributions/withdrawals paid… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · report notes: 2.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (3 columns x 10 lines + total; the blank 2025 cells of 'מימוש כתבי אופציה' confirmed), the column headers (3M to 31.03.2026/2025, FY 31.12.2025), the units (אלפי אירו) compared digit by digit with the…
- **Q2 2026** – `1722_חג'ג' אירופה דיוולופמנט צ.ש. בע_מ_2026_Q2_1767756.pdf` (report 1767756, 109 pp.) · cash-flow statement PDF pp. 65 · financing p. 65 · column headers p. 65.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי אירו (אירו, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר [56, 289, 32, 86, 360]; check 0 in every column.
  - Judgement calls: n1 'הנפקת מניות וכתבי אופציה, נטו' → 1: הנפקת מניות וכתבי אופציה (לא רשומים) יחד, נטו – לא מפוצל בדוח (לפי דוח הדירקטוריון: הנפקת מניות ואופציות לא רשומות למשק… · n2 'מימוש כתבי אופציה' → 2: מימוש כתבי אופציה (סדרה 1, בעיקר בהצעת רכש חליפין, ואופציות לא רשומות) – סעיף 2 · n4 'תקבולים בגין הלוואות לרוכשי דירות, נטו' → אחר: גביית הלוואות שהעמידה החברה לרוכשי דירות (נכס במאזן – 'הלוואות לרוכשי דירות', דוח הדירקטוריון עמ' 22–23), מוצגת בדוח בפ… · n5 'החזר השקעה לזכויות שאינן מקנות שליטה' → 12: החזר השקעה (הון) לבעלי זכויות שאינן מקנות שליטה – חלוקה/משיכה לבעלי זשמ"ש – סעיף 12 (R3: distributions/withdrawals paid… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c4, c5 · report notes: 2.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (5 columns x 10 lines + total), the column headers (6M/3M to 30.06.2026/2025, FY 31.12.2025), the units (אלפי אירו) compared digit by digit with the rendered zoom page (header strip + financing sectio…

### 1724 – רמות בעיר בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (-1), C2 3 חודשים שהסתיימו ב-31.03.2025 total (-1); C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `1724_רמות בעיר בע_מ_2026_Q1_1742818.pdf` (report 1742818, 74 pp.) · cash-flow statement PDF pp. 49, 50 · financing p. 49 · column headers p. 49.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר, נטו' → 5: אשראי לזמן קצר, נטו (מתאגידים פיננסיים, כולל אשראי ליווי) – סעיף 5 · n6 'הנפקת שטרי הון לבעלי שליטה' → 1: הנפקת שטרי הון לבעלי השליטה – שטרי ההון מוצגים בהון המיוחס לבעלים של החברה האם (בדוח על השינויים בהון: 'הנפקת שטרי הון… · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p50, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): -5,415, -7,948, -50,630) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2 · report notes: 1 · Phase C: verbatim header c1, c2, c3; context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (6 lines + total), every value (3 columns x 7 lines), the column headers, the units (אלפי ש"ח per column) and the (*) interest line (appendix B, p.50) compared digit by digit with the 220-DPI review render of the… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס 2026 אלפי ש"ח בלתי מבוקר' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס 2026 בלתי מב… (composites v1_11.png, v2_31.png, v3_11.png).
- **Q2 2026** – `1724_רמות בעיר בע_מ_2026_Q2_1763829.pdf` (report 1763829, 80 pp.) · cash-flow statement PDF pp. 53, 54 · financing p. 53 · column headers p. 53.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר, נטו' → 5: אשראי לזמן קצר, נטו (מתאגידים פיננסיים, כולל אשראי ליווי) – סעיף 5 · n6 'הנפקת שטרי הון לבעלי שליטה' → 1: הנפקת שטרי הון לבעלי השליטה – שטרי ההון מוצגים בהון המיוחס לבעלים של החברה האם – לפי מוסכמות שלב ב' §4 – סעיף 1 (כמו בד… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p54, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): -15,598, -25,561, -10,183, -17,613, -50,630) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2, c4 · report notes: 1 · Phase C: verbatim header c1, c2, c3, c4, c5; context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (8 lines + total), every value (5 columns x 9 lines), the column headers, the units (אלפי ש"ח per column) and the (*) interest line (appendix A, p.54) compared digit by digit with the 220-DPI review render of the… Phase C: header_text c1: 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026 אלפי ש"ח בלתי מבוקר' -> 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026 בלתי מבוקר'; header_text… (composites v1_12.png, v2_32.png, v3_12.png).

### 1797 – רותם שני יזמות והשקעות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1797_רותם שני יזמות והשקעות בע_מ_2026_Q1_1742449.pdf` (report 1742449, 62 pp.) · cash-flow statement PDF pp. 44, 45 · financing p. 45 · column headers p. 45.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'תמורה ממימוש אופציות סדרה 2' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 בלתי מבוקר'; header_text c2… (composites v1_12.png).
- **Q2 2026** – `1797_רותם שני יזמות והשקעות בע_מ_2026_Q2_1764008.pdf` (report 1764008, 64 pp.) · cash-flow statement PDF pp. 45, 46 · financing p. 46 · column headers p. 46.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'תמורה ממימוש אופציות' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2, c3, c4.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 בלתי מבוקר'; header_text c2… (composites v1_12.png).

### 1829 – אב-גד החזקות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1829_אב-גד החזקות בע_מ_2026_Q1_1745375-01.pdf` (report 1745375, 84 pp.) · cash-flow statement PDF pp. 64, 65 · financing p. 64 · column headers p. 64.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'פירעון הלוואות מתאגידים בנקאיים ואחרים' → 5: אותה שורה בדוח Q2 מוצגת כ'קבלת (פירעון) הלוואות מתאגידים בנקאיים ואחרים' – שורת הלוואות נטו ללא ציון תקופה (חיובית ברבע… · n6 'השקעת המיעוט בישות מאוחדת' → 6: השקעת בעלי זכויות שאינן מקנות שליטה (המיעוט) בישות מאוחדת – סעיף 6 · n7 'מימוש אופציה' → 2: מימוש אופציות של החברה (לפי הדוח על השינויים בהון: 'מימוש אופציות' 3,721 להון המניות והפרמיה) – סעיף 2 · n8 'הקצאת מניות בחברת בת' → 6: הקצאת מניות בחברה בת למשקיעים – עסקה עם בעלי זכויות שאינן מקנות שליטה (לפי הדוח על השינויים בהון: 'הקצאת מניות חברת בת'… · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3 · Phase C: line note n4; verbatim header c1, c2, c3; context sections (captions).
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31.3.2026 אלפי ש"ח בלתי מבוקר' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31.3.2026 בלתי מבוקר';… (composites v1_13.png, v3_12.png).
- **Q2 2026** – `1829_אב-גד החזקות בע_מ_2026_Q2_1767116-01.pdf` (report 1767116, 90 pp.) · cash-flow statement PDF pp. 65, 66 · financing p. 65 · column headers p. 65.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'קבלת (פירעון) הלוואות מתאגידים בנקאיים ואחרים' → 5: קבלת (פירעון) הלוואות מתאגידים בנקאיים ואחרים – שורת הלוואות נטו ללא ציון תקופה (חיובית ברבעון 4–6/2026, שלילית בתקופות… · n6 'השקעת המיעוט בישות מאוחדת' → 6: השקעת בעלי זכויות שאינן מקנות שליטה (המיעוט) בישות מאוחדת – סעיף 6 · n7 'מימוש אופציה' → 2: מימוש אופציות של החברה (לפי הדוח על השינויים בהון לשנת 2025: 'מימוש אופציות' 3,721 להון המניות והפרמיה) – סעיף 2 · n8 'הקצאת מניות בחברת בת' → 6: הקצאת מניות בחברה בת למשקיעים – עסקה עם בעלי זכויות שאינן מקנות שליטה – סעיף 6 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3 · Phase C: line note n4; verbatim header c1, c2, c3, c4, c5.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30.6.2026 אלפי ש"ח בלתי מבוקר' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30.6.2026 בלתי מבוקר'; he… (composites v1_13.png, v2_07.png).

### 1903 – קבוצת יובלים השקעות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1903_קבוצת יובלים השקעות בע_מ_2026_Q1_1744226.pdf` (report 1744226, 103 pp.) · cash-flow statement PDF pp. 57, 58 · financing p. 57 · column headers p. 57.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 [restated] · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת אשראי לזמן קצר מתאגידים בנקאיים' → 5: קבלת אשראי לזמן קצר מתאגידים בנקאיים (שורה ברוטו) – סעיף 5 · n2 'פירעון אשראי לזמן קצר מתאגידים בנקאיים' → 5: פירעון אשראי לזמן קצר מתאגידים בנקאיים (שורה ברוטו) – סעיף 5 · n3 'קבלת אשראי ממוסד פיננסי' → 5: אשראי ממוסד פיננסי (גורם חוץ-בנקאי) ללא ציון תקופה; במאזן 'אשראי מתאגידים פיננסיים' מוצג בהתחייבויות שוטפות – אשראי לזמ… · n4 'פירעון אשראי ממוסד פיננסי' → 5: פירעון אשראי ממוסד פיננסי – כמו שורת הקבלה: אשראי לזמן קצר, שורה ברוטו – סעיף 5 · n8 'קבלת הלוואות מהחברה האם' → 5: הלוואות מהחברה האם (בעלת השליטה) ללא ציון תקופה; במאזן היתרה מוצגת בהתחייבויות שוטפות ('יתרות זכות לחברה האם') – אשראי… · n9 'פירעון הלוואות מהחברה האם' → 5: פירעון הלוואות מהחברה האם – כמו שורת הקבלה: יתרה שוטפת – סעיף 5 (ולא 7) · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: restated: 3 חודשים שהסתיימו ב-31.03.2025 (מוצג מחדש) · column notes: c2 · report notes: 2 · Phase C: line note n7; verbatim header c1, c2, c3; context sections (captions).
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (10 lines + total), every value (3 columns, incl. the (*) restatement markers), the column headers, the units (אלפי ש"ח per column) and the absence of (*) interest/dividend lines outside financing compared with 22… Phase C: header_text c1: 'לשלושה חודשים שהסתיימו ביום 31 במרס 2026 אלפי ש"ח בלתי מבוקר' -> 'לשלושה חודשים שהסתיימו ביום 31 במרס 2026 בלתי מבוקר'; header_text… (composites v1_13.png, v3_13.png).
- **Q2 2026** – `1903_קבוצת יובלים השקעות בע_מ_2026_Q2_1767412.pdf` (report 1767412, 95 pp.) · cash-flow statement PDF pp. 57, 58 · financing p. 57 · column headers p. 57.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 [restated] · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) [restated] · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת אשראי לזמן קצר מתאגידים בנקאיים' → 5: קבלת אשראי לזמן קצר מתאגידים בנקאיים (שורה ברוטו) – סעיף 5 · n2 'פירעון אשראי לזמן קצר מתאגידים בנקאיים' → 5: פירעון אשראי לזמן קצר מתאגידים בנקאיים (שורה ברוטו) – סעיף 5 · n3 'קבלת אשראי ממוסד פיננסי' → 5: אשראי ממוסד פיננסי (גורם חוץ-בנקאי) ללא ציון תקופה; במאזן 'אשראי מתאגידים פיננסיים' מוצג בהתחייבויות שוטפות – אשראי לזמ… · n4 'פירעון אשראי ממוסד פיננסי' → 5: פירעון אשראי ממוסד פיננסי – כמו שורת הקבלה: אשראי לזמן קצר, שורה ברוטו – סעיף 5 · n8 'קבלת הלוואות מהחברה האם' → 5: הלוואות מהחברה האם (בעלת השליטה) ללא ציון תקופה; במאזן היתרה מוצגת בהתחייבויות שוטפות ('יתרות זכות לחברה האם') – אשראי… · n9 'פירעון הלוואות מהחברה האם' → 5: פירעון הלוואות מהחברה האם – כמו שורת הקבלה: יתרה שוטפת – סעיף 5 (ולא 7) · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: restated: 6 חודשים שהסתיימו ב-30.06.2025 (מוצג מחדש); 3 חודשים שהסתיימו ב-30.06.2025 (אפריל–יוני) (מוצג מחדש) · column notes: c2, c4 · report notes: 2 · Phase C: line note n7; verbatim header c1, c2, c3, c4, c5; context sections (captions).
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (10 lines + total), every value (5 columns, incl. the (*) restatement markers), the column headers, the units (אלפי ש"ח per column) and the absence of (*) interest/dividend lines outside financing compared with 22… Phase C: header_text c1: 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026 אלפי ש"ח בלתי מבוקר' -> 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026 בלתי מבוקר'; header_text… (composites v1_14.png, v3_13.png).

### 1905 – גלעד מאי חברה להשקעות בניה ופיתוח בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1905_גלעד מאי חברה להשקעות בניה ופיתוח בע_מ_2026_Q1_1744780.pdf` (report 1744780, 52 pp.) · cash-flow statement PDF pp. 40 · financing p. 40 · column headers p. 40.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 [restated] · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי מתאגידים בנקאיים ואחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, מוצג נטו – סעיף 5 · n2 'קבלת אשראי' → 5: קבלת אשראי ללא ציון תקופה (שורת תקבול ברוטו); לפי המאזן רוב האשראי שוטף ('אשראי מתאגידים בנקאיים ואחרים') – סעיף 5. ברב… · n3 'פירעון אשראי' → 5: פירעון אשראי ללא ציון תקופה (שורת תשלום ברוטו) – כמו שורת הקבלה – סעיף 5 · (+3 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p40, פעילות שוטפת: -9,873, -9,415, -40,455) · dividends paid: no line in the statement → (*) row 0.
  - Flags: restated: 3 חודשים שהסתיימו ב-31.03.2025 (מוצג מחדש) · column notes: c2 · report notes: 2.
  - Verification: Phase B batch 7 Builder (2026-11-10): Located the financing section visually (no heading: from below the investing total to the financing total) on the 220-DPI render of PDF page 40; every line text (6 lines + total), every value (3 columns, incl. the (*) reclassific…
- **Q2 2026** – `1905_גלעד מאי חברה להשקעות בניה ופיתוח בע_מ_2026_Q2_1766777.pdf` (report 1766777, 58 pp.) · cash-flow statement PDF pp. 43, 44 · financing p. 44 · column headers p. 44.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 [restated] · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) [restated] · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי מתאגידים בנקאיים ואחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, מוצג נטו – סעיף 5 · n2 'קבלת אשראי' → 5: קבלת אשראי ללא ציון תקופה (שורת תקבול ברוטו); לפי המאזן רוב האשראי שוטף ('אשראי מתאגידים בנקאיים ואחרים') – סעיף 5. בשנ… · n3 'פירעון אשראי' → 5: פירעון אשראי ללא ציון תקופה (שורת תשלום ברוטו) – כמו שורת הקבלה – סעיף 5 · (+3 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p43, פעילות שוטפת: -12,868, -25,876, -2,995, -16,461, -40,455) · dividends paid: no line in the statement → (*) row 0.
  - Flags: restated: 6 חודשים שהסתיימו ב-30.06.2025 (מוצג מחדש); 3 חודשים שהסתיימו ב-30.06.2025 (אפריל–יוני) (מוצג מחדש) · column notes: c2, c4 · source irregularities: 1 (see §6) · report notes: 2.
  - Verification: Phase B batch 7 Builder (2026-11-10): Located the financing section visually (no heading: from below the investing total to the financing total) on the 220-DPI render of PDF page 44; every line text (6 lines + total), every value (5 columns, incl. the (*) restatement…

### 1928 – רימון שירותי ייעוץ וניהול בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1928_רימון שירותי ייעוץ וניהול בע_מ_2026_Q1_1743933.pdf` (report 1743933, 59 pp.) · cash-flow statement PDF pp. 32, 33 · financing p. 33 · column headers p. 33.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'רכישת מניות מהמיעוט' → 14: רכישת מניות מבעלי זכויות שאינן מקנות שליטה ('המיעוט') בחברה בת מאוחדת – עסקה הונית ללא שינוי בשליטה, סעיף 14 · n2 'תמורה ממימוש אופציות לעובדים' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · n4 'דיבידנד ששולם לבעלי זכויות המיעוט' → 12: דיבידנד ששולם לבעלי זכויות המיעוט (זכויות שאינן מקנות שליטה) בחברה בת – סעיף 12 · n9 'קבלת הלוואה מנותני אשראי אחרים' → 4: קבלת הלוואה מנותני אשראי אחרים – קבלה ברוטו, ללא ציון תקופה; במאזן (עמ' 26) נותני אשראי אחרים מופיעים רק בשורת ההתחייבו… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p32, פעילות שוטפת: -10,394, -7,394, -44,656) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 3 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 (בלתי… (composites v1_14.png).
- **Q2 2026** – `1928_רימון שירותי ייעוץ וניהול בע_מ_2026_Q2_1766226.pdf` (report 1766226, 64 pp.) · cash-flow statement PDF pp. 36, 37 · financing p. 37 · column headers p. 37.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'רכישת מניות מהמיעוט' → 14: רכישת מניות מבעלי זכויות שאינן מקנות שליטה ('המיעוט') בחברה בת מאוחדת – עסקה הונית ללא שינוי בשליטה, סעיף 14 · n2 'תמורה ממימוש אופציות לעובדים' → 2: תמורה ממימוש אופציות (לעובדים/כתבי אופציה) – סעיף 2 · n4 'דיבידנד ששולם לבעלי זכויות המיעוט' → 12: דיבידנד ששולם לבעלי זכויות המיעוט (זכויות שאינן מקנות שליטה) בחברה בת – סעיף 12 · n9 'קבלת הלוואה מנותני אשראי אחרים' → 4: קבלת הלוואה מנותני אשראי אחרים – קבלה ברוטו, ללא ציון תקופה; במאזן (עמ' 28) נותני אשראי אחרים מופיעים רק בשורת ההתחייבו… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p36, פעילות שוטפת: -26,229, -22,951, -15,835, -15,557, -44,656) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 3 · Phase C: verbatim header c1, c2, c3, c4, c5.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימו ביום 30 ביוני 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שישה חודשים שהסתיימו ביום 30 ביוני 2026 (בלתי… (composites v1_14.png).

### 1969 – קבוצת אביב ושות' נדל"ן 1963 בע"מ

- **Q1 2026: not in the folder** (listed in `חסרים והערות` as `דוח חסר`; not downloaded – out of scope).
- **Q2 2026** – `1969_קבוצת אביב ושות' נדל_ן 1963 בע_מ_2026_Q2_1767211.pdf` (report 1767211, 68 pp.) · cash-flow statement PDF pp. 36, 37 · financing p. 37 · column headers p. 37.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 5 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'שינוי באשראי לזמן קצר מבנקים ואחרים, נטו' → 5: שינוי באשראי לזמן קצר מבנקים ואחרים, נטו – סעיף 5 (כולל מלווים אחרים ולא רק תאגידים בנקאיים) · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3 · Phase C: verbatim header c1, c2, c3, c4, c5.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי… (composites v1_15.png).

### 1974 – סופרין אחזקות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `1974_סופרין אחזקות בע_מ_2026_Q1_1742794.pdf` (report 1742794, 107 pp.) · cash-flow statement PDF pp. 53, 54 · financing p. 54 · column headers p. 54.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר, נטו' → 5: אשראי לזמן קצר, נטו – סעיף 5 · n6 'הנפקת כתבי אופציה' → 2: הנפקת כתבי אופציה (סדרה 1) שהונפקו בחבילה עם אגרות חוב סדרה ג'; התמורה שיוחסה לכתבי האופציה מוצגת בשורה נפרדת → סעיף 2… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p53, פעילות שוטפת: -420, -212, -16,701) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (8 lines + total; line 3 text corrected from the image – the text layer had a stray 'י'), every value (3 columns), the column headers, the units (באלפי ש"ח in the title) compared digit by digit with the 220-DPI zo…
- **Q2 2026** – `1974_סופרין אחזקות בע_מ_2026_Q2_1764536.pdf` (report 1764536, 118 pp.) · cash-flow statement PDF pp. 58, 59 · financing p. 59 · column headers p. 59.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'אשראי לזמן קצר, נטו' → 5: אשראי לזמן קצר, נטו – סעיף 5 · n7 'הנפקת כתבי אופציה' → 2: הנפקת כתבי אופציה (סדרה 1) שהונפקו בחבילה עם אגרות חוב סדרה ג'; התמורה שיוחסה לכתבי האופציה מוצגת בשורה נפרדת → סעיף 2… · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p58, פעילות שוטפת: -9,961, -7,246, -9,541, -7,034, -16,701) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c4 · source irregularities: 1 (see §6) · report notes: 2 · Phase C: issues +1.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (9 lines + total; texts of lines 3-4 corrected from the image – the text layer had a stray 'י'), every value (5 columns; blank cells of line 5 confirmed on the image), the column headers, the units (באלפי ש"ח in t… Phase C: issues += 1 (composites v2_43.png).

### 1979 – אפי קפיטל נדל"ן בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (-4,872), C2 3 חודשים שהסתיימו ב-31.03.2025 total (3,732); C2 per-item INFO rows (explained): 5.
- **Q1 2026** – `1979_אפי קפיטל נדל_ן בע_מ_2026_Q1_1742790.pdf` (report 1742790, 74 pp.) · cash-flow statement PDF pp. 52, 53 · financing p. 53 · column headers p. 53.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'תמורה ממימוש אופציות למניות' → 2: תמורה ממימוש אופציות למניות – סעיף 2 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c1, c2 · report notes: 2 · Phase C: verbatim header c1, c2.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 (בלתי מבוקר)'; header_text… (composites v1_15.png).
- **Q2 2026** – `1979_אפי קפיטל נדל_ן בע_מ_2026_Q2_1763668.pdf` (report 1763668, 79 pp.) · cash-flow statement PDF pp. 55, 56 · financing p. 56 · column headers p. 56.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n9 'תמורה ממימוש אופציות למניות' → 2: תמורה ממימוש אופציות למניות – סעיף 2 · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c1, c2, c4 · report notes: 2 · Phase C: verbatim header c1, c2, c3, c4.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי מבוקר)'; header_text… (composites v1_15.png).

### 2360 – קבוצת אקרו בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (1); C2 per-item INFO rows (explained): 1.
- **Q1 2026** – `2360_קבוצת אקרו בע_מ_2026_Q1_1742743.pdf` (report 1742743, 68 pp.) · cash-flow statement PDF pp. 45, 46 · financing p. 45 · column headers p. 45.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'תמורה מהנפקת מניות ואופציות' → 1: תמורה מהנפקת מניות ואופציות (חבילה; לפי הדוח על השינויים בהון: 'הנפקת מניות ואופציות' 99,356) – מניות וכתבי אופציה שאינ… · n2 'השקעות המיעוט בישויות מאוחדות' → 6: השקעות בעלי זכויות שאינן מקנות שליטה (המיעוט) בישויות מאוחדות – סעיף 6 · n3 'משיכות המיעוט בישויות מאוחדות' → 12: משיכות בעלי זכויות שאינן מקנות שליטה (המיעוט) מישויות מאוחדות – סעיף 12 · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c1, c2 · report notes: 3 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: '3 החודשים שהסתיימו ביום 31 במרס 2026 (בלתי מבוקר) אלפי ש"ח' -> '3 החודשים שהסתיימו ביום 31 במרס 2026 (בלתי מבוקר)'; header_text c2:… (composites v1_16.png).
- **Q2 2026** – `2360_קבוצת אקרו בע_מ_2026_Q2_1764403.pdf` (report 1764403, 77 pp.) · cash-flow statement PDF pp. 49, 50 · financing p. 49 · column headers p. 49.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'תמורה מהנפקת מניות ואופציות' → 1: תמורה מהנפקת מניות ואופציות (חבילה; לפי הדוח על השינויים בהון: 'הנפקת מניות ואופציות' 99,356) – מניות וכתבי אופציה שאינ… · n2 'השקעות המיעוט בישויות מאוחדות' → 6: השקעות בעלי זכויות שאינן מקנות שליטה (המיעוט) בישויות מאוחדות – סעיף 6 · n3 'משיכות המיעוט בישויות מאוחדות' → 12: משיכות בעלי זכויות שאינן מקנות שליטה (המיעוט) מישויות מאוחדות – סעיף 12 · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c4 · report notes: 2 · Phase C: verbatim header c1, c3.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לששת החודשים שהסתיימו ביום 30 ביוני 2026 (בלתי מבוקר) אלפי ש"ח' -> 'לששת החודשים שהסתיימו ביום 30 ביוני 2026 (בלתי מבוקר)'; header_t… (composites v1_16.png).

### 2371 – בית וגג יזמות ונדל"ן בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2371_בית וגג יזמות ונדל_ן בע_מ_2026_Q1_1742688.pdf` (report 1742688, 59 pp.) · cash-flow statement PDF pp. 45 · financing p. 45 · column headers p. 45.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 4 + total; אחר 0; check 0 in every column.
  - Judgement calls: n2 'קבלת (פרעון) אשראי לזמן קצר' → 5: אשראי לזמן קצר, קבלה (פירעון) נטו – סעיף 5 · n4 'חלוקות לזכויות שאינן מקנות שליטה' → 12: חלוקות לבעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 12 · (+2 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p45, פעילות שוטפת: -5,207, -1,199, -4,272) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · report notes: 3 · Phase C: verbatim header c1, c2.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 בלתי מבוקר אלפי ש"ח' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 בלתי מב… (composites v1_16.png).
- **Q2 2026** – `2371_בית וגג יזמות ונדל_ן בע_מ_2026_Q2_1765823.pdf` (report 1765823, 68 pp.) · cash-flow statement PDF pp. 52 · financing p. 52 · column headers p. 52.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 4 + total; אחר 0; check 0 in every column.
  - Judgement calls: n2 'קבלת אשראי לזמן קצר' → 5: קבלת אשראי לזמן קצר (בדוח Q1: 'קבלת (פרעון) אשראי לזמן קצר') – סעיף 5 · n4 'חלוקות לזכויות שאינן מקנות שליטה' → 12: חלוקות לבעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 12 · (+2 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p52, פעילות שוטפת: -6,098, -2,337, -891, -1,138, -4,272) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c4 · report notes: 3 · Phase C: verbatim header c1, c2, c3, c4.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של ששה חודשים שהסתיימה ביום 30 ביוני 2026' -> 'לתקופה של ששה חודשים שהסתיימה ביום 30 ביוני 2026 בלתי מבוקר'; header_text c2:… (composites v1_17.png).

### 2384 – קרסו נדל"ן בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2384_קרסו נדל_ן בע_מ_2026_Q1_1745641.pdf` (report 1745641, 105 pp.) · cash-flow statement PDF pp. 46, 47 · financing p. 47 · column headers p. 47.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו – סעיף 5 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'נספח ב' – ריבית ומיסים במזומן: ריבית ששולמה' (p47, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 15,605, 13,751, 130,043); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · source irregularities: 1 (see §6) · report notes: 2 · Phase C: (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (7 lines + total), every value (3 columns), the column headers, the units (באלפי ש"ח) and the appendix (*) line (נספח ב', p. 47) compared digit by digit with 220-DPI renders (tool_review fin/page/outside images) o… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_33.png).
- **Q2 2026** – `2384_קרסו נדל_ן בע_מ_2026_Q2_1767254.pdf` (report 1767254, 109 pp.) · cash-flow statement PDF pp. 55, 56 · financing p. 56 · column headers p. 56.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו – סעיף 5 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'נספח ב' – ריבית ומסים במזומן: ריבית ששולמה' (p56, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 72,824, 59,586, 57,219, 45,835, 130,043); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c4 · report notes: 3 · Phase C: (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (7 lines + total, wrapped labels joined), every value (5 columns), the column headers, the units (באלפי ש"ח) and the appendix (*) line (נספח ב', p. 56) compared digit by digit with 220-DPI renders (tool_review fin… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_34.png).

### 2385 – עמרם אברהם חברה לבנין בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2385_עמרם אברהם חברה לבנין בע_מ_2026_Q1_1745346.pdf` (report 1745346, 104 pp.) · cash-flow statement PDF pp. 67, 68, 69 · financing p. 68 · column headers p. 68.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'שינוי באשראי לזמן קצר מבנקים ואחרים, נטו' → 5: שינוי באשראי לזמן קצר מבנקים ואחרים, נטו – כולל אשראי ממלווים אחרים; סעיף 5 · n7 'השקעות בעלי זכויות שאינן מקנות שליטה' → 6: השקעות בעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 6 · n10 'קבלת (פרעון) הלוואה מבעלי זכויות שאינן מקנות שליטה' → 5: קבלת (פרעון) הלוואה מבעלי זכויות שאינן מקנות שליטה – הלוואה (לא השקעה הונית), מוצגת נטו ללא ציון תקופה בשורה – סעיף 5 ל… · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p67, פעילות שוטפת: -70,265, -63,006, -273,461) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2, c3; context sections (captions).
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 (בלתי… (composites v1_17.png, v3_14.png).
- **Q2 2026** – `2385_עמרם אברהם חברה לבנין בע_מ_2026_Q2_1767833.pdf` (report 1767833, 107 pp.) · cash-flow statement PDF pp. 73, 74, 75, 76 · financing p. 74 · column headers p. 74.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 11 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'שינוי באשראי לזמן קצר מבנקים ואחרים, נטו' → 5: שינוי באשראי לזמן קצר מבנקים ואחרים, נטו – כולל אשראי ממלווים אחרים; סעיף 5 · n7 'השקעות בעלי זכויות שאינן מקנות שליטה' → 6: השקעות בעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 6 · n8 'חלוקת תשואה לזכויות שאינן מקנות שליטה' → 12: חלוקת תשואה לבעלי זכויות שאינן מקנות שליטה (חלוקה/דיבידנד לזשמ"ש בחברה בת) – סעיף 12 · n11 'קבלת (פרעון) הלוואה מבעלי זכויות שאינן מקנות שליטה' → 5: קבלת (פרעון) הלוואה מבעלי זכויות שאינן מקנות שליטה – הלוואה (לא השקעה הונית), מוצגת נטו ללא ציון תקופה בשורה – סעיף 5 ל… · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p73, פעילות שוטפת: -160,138, -132,561, -89,873, -69,555, -273,461) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2, c3, c4, c5; context sections (captions).
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי… (composites v1_17.png, v3_14.png, v3_15.png).

### 2386 – ע.ע. יסודות איתנים ייזום ובניה בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2025 total (1); C2 per-item INFO rows (explained): 1.
- **Q1 2026** – `2386_ע.ע. יסודות איתנים ייזום ובניה בע_מ_2026_Q1_1744954.pdf` (report 1744954, 70 pp.) · cash-flow statement PDF pp. 29, 30 · financing p. 29 · column headers p. 29.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 11 + total; אחר 0; check 0 in every column.
  - Judgement calls: n2 'תמורה מהנפקה פרטית של מניות ואופציות' → 1: הנפקה פרטית של מניות ואופציות (חבילה) שאינה מפוצלת בדוח – סעיף 1 (מוסכמות שלב B §6: מניות + אופציות → 1); אינה מימוש או… · n5 'קבלת אשראי והלוואות מגופים פיננסיים' → 5: קבלת אשראי והלוואות מגופים פיננסיים (מלווים חוץ-בנקאיים) ללא ציון תקופה, שורת תקבול ברוטו – סעיף 5; במאזן רוב האשראי שו… · n6 'פירעון אשראי והלוואות מגופים פיננסיים' → 5: פירעון אשראי והלוואות מגופים פיננסיים, שורת תשלום ברוטו – כמו שורת הקבלה – סעיף 5 · n9 'פירעון הלוואות מבעלי עניין' → 5: הלוואות מבעלי עניין ללא ציון תקופה; בדוח Q2 2026 אותה שורה מוצגת נטו ('נטילת (פירעון) הלוואות מבעלי עניין', שנת 2025 זה… · n11 'קבלת (פירעון) הלוואה משותפים' → 5: הלוואה משותפים (בפעילות משותפת), מוצגת נטו (קבלה/פירעון) ללא ציון תקופה – סעיף 5 (R3); בדוח Q2 2026 השורה מוצגת כ'פירעו… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (11 lines + total), every value (3 columns), the column headers, the units (אלפי ש"ח) and the absence of (*) lines outside financing compared digit by digit with 220-DPI renders (tool_review fin/page images) of PD…
- **Q2 2026** – `2386_ע.ע. יסודות איתנים ייזום ובניה בע_מ_2026_Q2_1767748.pdf` (report 1767748, 126 pp.) · cash-flow statement PDF pp. 32, 33 · financing p. 32 · column headers p. 32.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 12 + total; אחר 0; check 0 in every column.
  - Judgement calls: n2 'תמורה מהנפקה פרטית של מניות ואופציות' → 1: הנפקה פרטית של מניות ואופציות (חבילה) שאינה מפוצלת בדוח – סעיף 1 (מוסכמות שלב B §6: מניות + אופציות → 1); אינה מימוש או… · n5 'קבלת אשראי והלוואות מגופים פיננסיים (ראה ביאור 4א(1))' → 5: קבלת אשראי והלוואות מגופים פיננסיים (מלווים חוץ-בנקאיים) ללא ציון תקופה, שורת תקבול ברוטו – סעיף 5; במאזן 30.6.2026: אש… · n6 'פירעון אשראי והלוואות מגופים פיננסיים' → 5: פירעון אשראי והלוואות מגופים פיננסיים, שורת תשלום ברוטו – כמו שורת הקבלה – סעיף 5 · n10 'נטילת (פירעון) הלוואות מבעלי עניין' → 5: הלוואות מבעלי עניין, מוצגות נטו (נטילה/פירעון) ללא ציון תקופה – סעיף 5 (R3); בדוח Q1 2026 אותה שורה ('פירעון הלוואות מב… · n12 'פירעון הלוואה משותפים' → 5: הלוואה משותפים (בפעילות משותפת) ללא ציון תקופה; בדוח Q1 2026 אותה שורה מוצגת נטו ('קבלת (פירעון) הלוואה משותפים', רבעון… · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (12 lines + total), every value (5 columns), the column headers, the units (אלפי ש"ח) and the absence of (*) lines outside financing compared digit by digit with 220-DPI renders (tool_review fin/page images) of PD…

### 2389 – פרופדו בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2389_פרופדו בע_מ_2026_Q1_1745138.pdf` (report 1745138, 62 pp.) · cash-flow statement PDF pp. 38, 39, 40, 41 · financing p. 39 · column headers p. 39.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'פירעון הלוואות שנתקבלו מבעלי זכויות שאינן מקנות שליטה…' → 7: פירעון הלוואות שהתקבלו מבעלי זכויות שאינן מקנות שליטה בחברות בנות (השותפים ב-GLM ובמידר, ביאור 3) – הלוואות ולא השקעה ה… · n5 'קבלת הלוואות מבעלי זכויות שאינן מקנות שליטה בחברות בנות' → 4: קבלת הלוואות מבעלי זכויות שאינן מקנות שליטה בחברות בנות (2025: הלוואה מהשותף ב-GLM, במאזן בהתחייבויות הלא שוטפות, ביאור… · n6 'תקבולים בגין הנפקת אגרות חוב ואופציות, נטו' → 3: חבילה של אגרות חוב (סדרה א') וכתבי אופציה (סדרה 4) שהונפקה ברבעון 1/2025 ולא פוצלה בדוח תזרימי המזומנים; לפי הדוח על הש… · n8 'תקבולים בגין מימוש כתבי אופציה, נטו' → 2: מימוש כתבי אופציה (סדרה 4) למניות החברה, נטו מעלויות עסקה (ביאור 6ה; הדוח על השינויים בהון) – סעיף 2 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p38, פעילות שוטפת: -3,327, -1,370, -7,806) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:26 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 בלתי מבוקר'; header_text c2… (composites v1_18.png).
- **Q2 2026** – `2389_פרופדו בע_מ_2026_Q2_1766465.pdf` (report 1766465, 77 pp.) · cash-flow statement PDF pp. 50, 51, 52, 53 · financing p. 51 · column headers p. 51.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'פירעון הלוואות שנתקבלו מבעלי זכויות שאינן מקנות שליטה…' → 7: פירעון הלוואות שהתקבלו מבעלי זכויות שאינן מקנות שליטה בחברות בנות – הלוואות ולא השקעה הונית: סעיף 7 (R3: הלוואות מכל מל… · n5 'קבלת הלוואות מבעלי זכויות שאינן מקנות שליטה בחברות בנות' → 4: קבלת הלוואות מבעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 4 (R3: הלוואות לזמן ארוך מכל מלווה, כולל בעלי זכויות שאי… · n6 'תקבולים בגין הנפקת אגרות חוב ואופציות, נטו' → 3: 2025: חבילה של אגרות חוב (סדרה א') וכתבי אופציה (סדרה 4) שלא פוצלה בדוח – לפי הדוח על השינויים בהון רכיב כתבי האופציה 9… · n8 'תקבולים בגין מימוש כתבי אופציה, נטו' → 2: מימוש כתבי אופציה למניות החברה, נטו (2026: סדרה 4 עד פברואר 2026 ומימוש נוסף ביוני 2026) – סעיף 2 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p50, פעילות שוטפת: -4,684, -1,486, -1,357, -116, -7,806) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2, c4 · report notes: 3 · Phase C: verbatim header c2, c4, c5.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:26 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c2: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2025 אלפי ש"ח בלתי מבוקר' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2025 בלתי מב… (composites v1_18.png).

### 2392 – רייק אספן בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2392_רייק אספן בע_מ_2026_Q1_1742520.pdf` (report 1742520, 58 pp.) · cash-flow statement PDF pp. 49, 50 · financing p. 49 · column headers p. 49.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 '(פירעון) קבלת אשראי לזמן קצר מתאגידים בנקאיים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים, מוצג נטו – סעיף 5 · n2 'הלוואות שהתקבלו מחברה האם ומבעל השליטה' → 5: הלוואות שהתקבלו מהחברה האם ומבעל השליטה – שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורים): אשראי/ה… · n6 'פירעון הלוואות שהתקבלו מצדדים קשורים ואחרים' → 7: פירעון הלוואות שהתקבלו מצדדים קשורים ואחרים – שורת פירעון ברוטו; במאזן 'הלוואות מאחרים' כוללות הלוואות לזמן קצר וחלויות… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2 · report notes: 3 · Phase C: item n2 4→5; line note n4, n6.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text (wrapped label of line 4 joined), every value (3 columns x 9 lines + total), the column headers (3M to 31.03.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with the rendered zoom page (hea… Phase C: line 2: item -> 5; line 4: note (A evidence); line 7: note (A evidence) (composites v2_00.png; v2_00.png (also viewed by the Phase C Builder)).
- **Q2 2026** – `2392_רייק אספן בע_מ_2026_Q2_1763248.pdf` (report 1763248, 60 pp.) · cash-flow statement PDF pp. 50, 51 · financing p. 50 · column headers p. 50.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת (פירעון) אשראי לזמן קצר מתאגידים בנקאיים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים, מוצג נטו – סעיף 5 · n2 'הלוואות שהתקבלו מחברה האם ומבעל השליטה' → 5: הלוואות שהתקבלו מהחברה האם ומבעל השליטה – שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורים): אשראי/ה… · n6 'פירעון הלוואות שהתקבלו מאחרים' → 7: פירעון הלוואות שהתקבלו מאחרים – שורת פירעון ברוטו; במאזן 'הלוואות מאחרים' כוללות הלוואות לזמן קצר וחלויות שוטפות של הלו… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3 · Phase C: item n2 4→5; line note n4, n6.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text (wrapped labels of lines 1 and 4 joined), every value (5 columns x 9 lines + total), the column headers (6M/3M to 30.06.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with the rendered zoo… Phase C: line 3: item -> 5; line 5: note (A evidence); line 8: note (A evidence) (composites v2_01.png).

### 2396 – אשל הירדן יזום ובנין בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (-1), C2 3 חודשים שהסתיימו ב-31.03.2025 total (-1); C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `2396_אשל הירדן יזום ובנין בע_מ_2026_Q1_1744629.pdf` (report 1744629, 54 pp.) · cash-flow statement PDF pp. 34, 35 · financing p. 35 · column headers p. 35.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'פירעון התחייבות קרן וריבית בגין זכות שימוש' → 10: פירעון התחייבות בגין חכירה (זכות שימוש) – קרן וריבית יחד, ללא פיצול בדוח – סעיף 10 (R3) · n6 'רכישה עצמית של אג"ח סדרה ב' ו-ג'' → 8: רכישה עצמית (פדיון) של אגרות חוב של החברה (סדרות ב' ו-ג') – סעיף 8 (R3: רכישה חוזרת של אג"ח החברה), ולא סעיף 9 (רכישה ע… · n8 'קבלה (פירעון) הלוואות בגין פרויקטים, נטו' → 5: הלוואות בגין פרויקטים, מוצג נטו (קבלה/פירעון) ללא ציון תקופה – סעיף 5 (R3: שורת הלוואות נטו ללא תקופה); ב-2026 בעיקר פי… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c1, c2, c3 · report notes: 3 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:26 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'ליום 31 במרס 2026 (בלתי מבוקר) אלפי ש"ח' -> 'ליום 31 במרס 2026 בלתי מבוקר'; header_text c2: 'ליום 31 במרס 2025 (בלתי מבוקר) אלפי ש"ח… (composites v1_18.png; crop_2396_Q1_p35 (200 DPI, Phase C Builder)).
- **Q2 2026** – `2396_אשל הירדן יזום ובנין בע_מ_2026_Q2_1767492.pdf` (report 1767492, 59 pp.) · cash-flow statement PDF pp. 36, 37 · financing p. 37 · column headers p. 37.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'פירעון התחייבות קרן וריבית בגין זכות שימוש' → 10: פירעון התחייבות בגין חכירה (זכות שימוש) – קרן וריבית יחד, ללא פיצול בדוח – סעיף 10 (R3) · n6 'רכישה עצמית של אג"ח סדרה ב' ו-ג'' → 8: רכישה עצמית (פדיון) של אגרות חוב של החברה (סדרות ב' ו-ג') – סעיף 8 (R3: רכישה חוזרת של אג"ח החברה), ולא סעיף 9 (רכישה ע… · n8 'קבלה (פירעון) הלוואות בגין פרויקטים, נטו' → 5: הלוואות בגין פרויקטים, מוצג נטו (קבלה/פירעון) ללא ציון תקופה – סעיף 5 (R3: שורת הלוואות נטו ללא תקופה) · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c3, c4 · report notes: 2 · Phase C: verbatim header c3.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:26 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c3: 'לתקופה של שלושה חודשים שהסתיימו 2026 אלפי ש"ח' -> 'לתקופה של שלושה חודשים שהסתיימו ביום 30 ביוני 2026 בלתי מבוקר' (composites v1_19.png).

### 2417 – אנשי העיר מקבוצת רוטשטיין בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (1); C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `2417_אנשי העיר מקבוצת רוטשטיין בע_מ_2026_Q1_1743889.pdf` (report 1743889, 76 pp.) · cash-flow statement PDF pp. 66 · financing p. 66 · column headers p. 66.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check [0, -1, 0].
  - Judgement calls: n1 'קבלת (פירעון) אשראי לזמן קצר מתאגידים בנקאיים ואחרים ב…' → 5: קבלת (פירעון) אשראי לזמן קצר מתאגידים בנקאיים ואחרים בחשבונות ליווי, נטו – כולל אשראי ממלווים אחרים – סעיף 5 · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p66, פעילות שוטפת: -2,158, -2,865, -16,153) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2 · C1 ≠ 0 (source does not add up, explained): 3 חודשים שהסתיימו ב-31.03.2025 (-1) · source irregularities: 1 (see §6) · report notes: 1 · Phase C: verbatim header c1, c2.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (8 lines + total), every value (3 columns x 9 lines), the column headers, the units (אלפי ש"ח) and the (*) interest line (p.66, operating) compared digit by digit with the 220-DPI review render of the header strip… Phase C: header_text c1: 'ל-3 החודשים שהסתיימו 2026' -> 'ל-3 החודשים שהסתיימו ביום 31 במרץ 2026 בלתי מבוקר'; header_text c2: 'ל-3 החודשים שהסתיימו ביום 31 במר… (composites v1_19.png).
- **Q2 2026** – `2417_אנשי העיר מקבוצת רוטשטיין בע_מ_2026_Q2_1765496.pdf` (report 1765496, 84 pp.) · cash-flow statement PDF pp. 71 · financing p. 71 · column headers p. 71.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת (פירעון) אשראי לזמן קצר מתאגידים בנקאיים ואחרים ב…' → 5: קבלת (פירעון) אשראי לזמן קצר מתאגידים בנקאיים ואחרים בחשבונות ליווי, נטו – כולל אשראי ממלווים אחרים – סעיף 5 · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p71, פעילות שוטפת: -7,442, -8,322, -5,284, -5,457, -16,153) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2, c3, c4, c5.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (8 lines + total), every value (5 columns x 9 lines), the column headers, the units (אלפי ש"ח – manual header box so the zoom strip includes them) and the (*) interest line (p.71, operating) compared digit by digi… Phase C: header_text c1: 'ל-6 החודשים שהסתיימו 2026' -> 'ל-6 החודשים שהסתיימו ביום 30 ביוני 2026 בלתי מבוקר'; header_text c2: 'ל-6 החודשים שהסתיימו ביום 30 בי… (composites v1_19.png).

### 2418 – רם אדרת הנדסה אזרחית בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `2418_רם אדרת הנדסה אזרחית בע_מ_2026_Q1_1744896.pdf` (report 1744896, 79 pp.) · cash-flow statement PDF pp. 45, 46, 47 · financing p. 46 · column headers p. 46.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n2 '[ללא תווית בדוח Q1] פרעון אגרות חוב (התווית לפי דוח Q2)' → 8: פגם בדוח המקור: בדוח Q1 אין שורת 'פרעון אגרות חוב', אך עמודת השנה 2025 הודפסה מוזזת שורה אחת (7 ערכים מול 6 תוויות). הע… · n3 'אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, מוצג נטו – סעיף 5 (כולל מלווים אחרים). עמודת השנה 2025: הערך המודפס בשורה זו (8… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p47, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 10,277, 12,484, 65,057); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c3 · source irregularities: 1 (see §6) · report notes: 3 · Phase C: context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (3 columns x 6 lines + total), the column headers (3M to 31.03.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with the 220-DPI fin image (tool_review) and a 300-DPI grid zoom… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_35.png, v3_15.png).
- **Q2 2026** – `2418_רם אדרת הנדסה אזרחית בע_מ_2026_Q2_1766843.pdf` (report 1766843, 86 pp.) · cash-flow statement PDF pp. 49, 50, 51 · financing p. 50 · column headers p. 50.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, מוצג נטו – סעיף 5 (כולל מלווים אחרים ולא רק תאגידים בנקאיים) · n7 'קבלת הלוואה מזכויות שאינן מקנות שליטה' → 4: קבלת הלוואה מבעלי זכויות שאינן מקנות שליטה – הלוואה (התחייבות), לא השקעה הונית; שורת קבלה ברוטו ללא ציון תקופה – סעיף 4… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p51, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 30,104, 33,279, 19,827, 20,795, 65,057); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3 · Phase C: context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text (wrapped labels joined), every value (5 columns x 7 lines + total), the column headers (6M/3M to 30.06.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with the 220-DPI fin image (tool_revie… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_36.png, v3_16.png).

### 2429 – לוזון רונסון אן.וי

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2429_לוזון רונסון אן.וי._2026_Q1_1742803.pdf` (report 1742803, 52 pp.) · cash-flow statement PDF pp. 32, 33 · financing p. 33 · column headers p. 33.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n7 'קבלת הלוואה מהמיעוט' → 5: קבלת הלוואה מבעלי זכויות שאינן מקנות שליטה (מיעוט) בחברות מוחזקות – הלוואה, לא השקעה הונית. בדוח Q2 2026 אותה שורה מוצג… · n8 'קבלת הלוואות לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: הלוואות לזמן קצר מתאגידים בנקאיים ואחרים, נטו – סעיף 5 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p32, פעילות שוטפת: -32,773, -20,823, -70,406) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: item n7 4→5.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (8 lines + total), every value (3 columns), the column headers (c2 header confirmed: 3 months ended 31.3.2025), the units (אלפי ש"ח) and the (*) interest line (operating, p. 32) compared digit by digit with 220-DP… Phase C: line 7: item -> 5 (composites no new image needed (rule-based change / note wording only)).
- **Q2 2026** – `2429_לוזון רונסון אן.וי._2026_Q2_1764287.pdf` (report 1764287, 55 pp.) · cash-flow statement PDF pp. 34, 35 · financing p. 35 · column headers p. 35.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n7 'קבלת (פירעון) הלוואה מהמיעוט' → 5: קבלת (פירעון) הלוואה מהמיעוט – שורת הלוואה מבעלי זכויות שאינן מקנות שליטה המוצגת נטו (קבלה/פירעון) ללא ציון תקופה – סעי… · n8 'קבלת הלוואות לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: הלוואות לזמן קצר מתאגידים בנקאיים ואחרים, נטו – סעיף 5 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'ריבית ששולמה' (p34, פעילות שוטפת: -48,390, -21,982, -15,617, -1,159, -70,406) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: source irregularities: 1 (see §6) · report notes: 2 · Phase C: item n7 4/7 לפי סימן→5; issues +1.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (8 lines + total, wrapped labels joined), every value (5 columns), the column headers, the units (אלפי ש"ח) and the (*) interest line (operating, p. 34) compared digit by digit with 220-DPI renders (tool_review fi… Phase C: line 7: item -> 5; issues += 1 (composites v2_49.png).

### 2440 – גשם למשתכן בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2440_גשם למשתכן בע_מ_2026_Q1_1745527.pdf` (report 1745527, 69 pp.) · cash-flow statement PDF pp. 47, 48 · financing p. 48 · column headers p. 48.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלה (פירעון) התחייבות מבעל שליטה' → 5: התחייבות לבעל השליטה, מוצגת נטו (קבלה/פירעון) ללא ציון תקופה – סעיף 5 (R3; מוסכמות שלב B §5) · n4 'אשראי מתאגידים בנקאיים ואחרים, נטו' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:27 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c1: 'שלושה חודשים שהסתיימה ביום 31 במרץ 2026 (בלתי מבוקר)' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 (בלתי מבוקר)'; header_te… (composites v1_20.png).
- **Q2 2026** – `2440_גשם למשתכן בע_מ_2026_Q2_1767784.pdf` (report 1767784, 78 pp.) · cash-flow statement PDF pp. 51, 52, 53 · financing p. 52 · column headers p. 52.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלה (פירעון) התחייבות מבעל שליטה' → 5: התחייבות לבעל השליטה, מוצגת נטו (קבלה/פירעון) ללא ציון תקופה – סעיף 5 (R3; מוסכמות שלב B §5) · n4 'אשראי מתאגידים בנקאיים ואחרים, נטו' → 5: כולל אשראי ממלווים אחרים ולא רק מתאגידים בנקאיים; מוצג נטו – סעיף 5 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c3.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:27 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_run\<iss>\… Phase C: header_text c3: 'שלושה חודשים שהסתיימה ביום 30 ביוני 2026 בלתי מבוקר אלפי ש"ח' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 30 ביוני 2026 בלתי מבוקר' (composites v1_20.png).

### 2441 – שובל הנדסה ובניין בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2441_שובל הנדסה ובניין בע_מ_2026_Q1_1743355.pdf` (report 1743355, 69 pp.) · cash-flow statement PDF pp. 50, 51 · financing p. 50 · column headers p. 50.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'תמורה מהנפקת הון מניות ואופציות, נטו' → 1: תמורה מהנפקת הון מניות ואופציות, נטו – מניות ואופציות ללא פיצול בדוח (בדוח על השינויים בהון: 'הנפקת מניות ואופציות' 71,… · n3 'קבלת אשראי לזמן קצר מבנקים ואחרים' → 5: קבלת אשראי לזמן קצר מבנקים ואחרים (שורה ברוטו) – כולל אשראי ממלווים אחרים – סעיף 5 · n4 'פרעון אשראי מבנקים ואחרים לזמן קצר' → 5: פרעון אשראי לזמן קצר מבנקים ואחרים (שורה ברוטו) – כולל אשראי ממלווים אחרים – סעיף 5 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2; context sections (captions).
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (9 lines + total; labels of the repaired-font text layer compared word by word with the image), every value (3 columns x 10 lines), the column headers (c2 '3 חודשים שהסתיימו ביום 31 במרס 2025'), the units (אלפי ש"… Phase C: header_text c1: 'שהסתיימה ביום 31 במרס 2026 3 חודשים שהסתיימו 2026' -> '3 חודשים שהסתיימו ביום 31 במרס 2026 (לא מבוקר)'; header_text c2: 'שהסתיימה בי… (composites v1_20.png, v3_16.png).
- **Q2 2026** – `2441_שובל הנדסה ובניין בע_מ_2026_Q2_1764196.pdf` (report 1764196, 75 pp.) · cash-flow statement PDF pp. 55, 56 · financing p. 55 · column headers p. 55.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'תמורה מהנפקת הון מניות ואופציות, נטו' → 1: תמורה מהנפקת הון מניות ואופציות, נטו – מניות ואופציות ללא פיצול בדוח – סעיף 1 (מוסכמות שלב ב' §6; כמו בדוח Q1) · n3 'קבלת אשראי לזמן קצר מבנקים ואחרים' → 5: קבלת אשראי לזמן קצר מבנקים ואחרים (שורה ברוטו) – כולל אשראי ממלווים אחרים – סעיף 5 · n4 'פרעון אשראי מבנקים ואחרים לזמן קצר' → 5: פרעון אשראי לזמן קצר מבנקים ואחרים (שורה ברוטו) – כולל אשראי ממלווים אחרים – סעיף 5 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c3, c5; context sections (captions).
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (9 lines + total; labels of the repaired-font text layer compared word by word with the image), every value (5 columns x 10 lines), the column headers and the units (אלפי ש"ח on p.55) compared digit by digit with… Phase C: header_text c1: 'שישה חודשים שהסתיימו 2026 (לא מבוקר)' -> 'שישה חודשים שהסתיימו ביום 30 ביוני 2026 (לא מבוקר)'; header_text c3: 'שלושה חודשים 2026 אל… (composites v1_21.png, v3_17.png).

### 2449 – קבוצת מיי טאון בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2449_קבוצת מיי טאון בע_מ_2026_Q1_1744151.pdf` (report 1744151, 60 pp.) · cash-flow statement PDF pp. 44, 45 · financing p. 44 · column headers p. 44.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 [restated] · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 4 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת אשראי מתאגידים בנקאיים' → 5: קבלת אשראי מתאגידים בנקאיים ללא ציון תקופה; במאזן האשראי מתאגידים בנקאיים ונותני אשראי אחרים ברובו שוטף (31.3.2026: שוט… · (+3 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: restated: 3 חודשים שהסתיימו ב-31.03.2025 (מוצג מחדש) · column notes: c2 · report notes: 1 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (4 lines + total), every value (3 columns), the column headers (incl. the restatement asterisk on 2025), the units (אלפי ש"ח per column) and the absence of (*) lines outside financing (operating page + appendix A)… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 (בלתי… (composites v1_21.png).
- **Q2 2026** – `2449_קבוצת מיי טאון בע_מ_2026_Q2_1764920.pdf` (report 1764920, 62 pp.) · cash-flow statement PDF pp. 45, 46 · financing p. 45 · column headers p. 45.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 [restated] · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) [restated] · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 4 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת אשראי מתאגידים בנקאיים' → 5: קבלת אשראי מתאגידים בנקאיים ללא ציון תקופה; במאזן האשראי מתאגידים בנקאיים ונותני אשראי אחרים ברובו שוטף; בעמודות 2025 מ… · (+3 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: restated: 6 חודשים שהסתיימו ב-30.06.2025 (מוצג מחדש); 3 חודשים שהסתיימו ב-30.06.2025 (אפריל–יוני) (מוצג מחדש) · column notes: c2, c4 · report notes: 1 · Phase C: verbatim header c1, c2, c3, c4, c5; context sections (captions).
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (4 lines + total), every value (5 columns), the column headers (incl. the restatement asterisks on the 2025 columns), the units (אלפי ש"ח per column) and the absence of (*) lines outside financing (operating page… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי… (composites v1_21.png, v3_17.png).

### 2456 – שמואל ברוך יזמות ובניה בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2456_שמואל ברוך יזמות ובניה בע_מ_2026_Q1_1742581.pdf` (report 1742581, 49 pp.) · cash-flow statement PDF pp. 40, 41 · financing p. 41 · column headers p. 41.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ₪ (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'קבלת הלוואות מצדדים קשורים' → 5: השורה מכונה 'קבלת הלוואות מצדדים קשורים' אך בכל העמודות מודפסים סכומים שליליים (יציאת מזומנים) – כלומר השורה מציגה את ה… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: source irregularities: 1 (see §6) · report notes: 2 · Phase C: verbatim header c2; issues +1.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c2: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס 2025 בלתי מבוקר אלפי ₪' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרס 2025 בלתי מבוק… (composites v1_22.png, v2_46.png).
- **Q2 2026** – `2456_שמואל ברוך יזמות ובניה בע_מ_2026_Q2_1766214.pdf` (report 1766214, 59 pp.) · cash-flow statement PDF pp. 50, 51 · financing p. 51 · column headers p. 51.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ₪ (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'קבלת הלוואות מצדדים קשורים' → 5: השורה מכונה 'קבלת הלוואות מצדדים קשורים' אך בכל העמודות מודפסים סכומים שליליים (יציאת מזומנים) – כלומר השורה מציגה את ה… · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: source irregularities: 1 (see §6) · report notes: 2 · Phase C: verbatim header c3; issues +1.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c3: 'לתקופה של שלושה חודשים שהסתיימה ביום 30 ביוני 2026 בלתי מבוקר אלפי ₪' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 30 ביוני 2026 בלתי מב… (composites v1_22.png).

### 2458 – מגידו י.ק. בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2025 total (-191); C2 per-item INFO rows (explained): 1.
- **Q1 2026** – `2458_מגידו י.ק. בע_מ_2026_Q1_1743908.pdf` (report 1743908, 65 pp.) · cash-flow statement PDF pp. 44, 45 · financing p. 45 · column headers p. 45.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'תמורה מהנפקת מניות וכתבי אופציה, נטו' → 1: הנפקת מניות וכתבי אופציה לראשונה לציבור (יולי 2025): לפי הדוח על השינויים בהון – מניות 154,440 וכתבי אופציה 24,010; שור… · n5 'קבלה (פירעון) אשראי מתאגידים בנקאיים לזמן קצר, נטו' → 5: קבלה (פירעון) אשראי מתאגידים בנקאיים לזמן קצר, נטו – סעיף 5 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2 · report notes: 2.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (6 lines + total), every value (3 columns), the column headers, the units (אלפי ש"ח per column) compared digit by digit with the 220-DPI zoom of the financing section (screenshots PDF p.3); operating page 44 viewe…
- **Q2 2026** – `2458_מגידו י.ק. בע_מ_2026_Q2_1767000.pdf` (report 1767000, 68 pp.) · cash-flow statement PDF pp. 44, 45 · financing p. 45 · column headers p. 45.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n3 'תמורה מהנפקת מניות וכתבי אופציה, נטו' → 1: הנפקת מניות וכתבי אופציה לראשונה לציבור (יולי 2025): לפי הדוח על השינויים בהון – מניות 154,440 וכתבי אופציה 24,010; שור… · n5 'פירעון אשראי מתאגידים בנקאיים לזמן קצר, נטו' → 5: פירעון אשראי מתאגידים בנקאיים לזמן קצר, נטו – סעיף 5 (בדוח Q1: 'קבלה (פירעון) ... נטו') · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2 · report notes: 2.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (6 lines + total), every value (5 columns), the column headers, the units (אלפי ש"ח per column) compared digit by digit with the 220-DPI zoom of the financing section (screenshots PDF p.6); operating page 44 viewe…

### 2464 – יוזמות - פיתוח נדל"ן בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2464_יוזמות - פיתוח נדל_ן בע_מ_2026_Q1_1746287.pdf` (report 1746287, 107 pp.) · cash-flow statement PDF pp. 92, 93 · financing p. 93 · column headers p. 93.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת (פרעון) אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נ…' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, מוצג נטו – כל האשראי לזמן קצר, מבנקים ומאחרים, בסעיף 5 (R3) · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2 · report notes: 2 · Phase C: verbatim header c1, c2.
  - Verification: Phase B batch 8 Builder (2026-11-10): Earlier views of this report (10:14-11:02) returned no image ('maximum number of images') and are NOT relied on; the visual check was redone on 11:06 / 11:27 on a composite PNG rendered directly from the source PDF (%TEMP%\fcf_ru… Phase C: header_text c1: 'ל-3 החודשים שהסתיימו 2026' -> 'ל-3 החודשים שהסתיימו ביום 31 במרץ 2026 בלתי מבוקר'; header_text c2: 'ל-3 החודשים שהסתיימו ביום 31 במר… (composites v1_22.png).
- **Q2 2026** – `2464_יוזמות - פיתוח נדל_ן בע_מ_2026_Q2_1767804.pdf` (report 1767804, 137 pp.) · cash-flow statement PDF pp. 92, 93, 94 · financing p. 93 · column headers p. 93.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת (פרעון) אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נ…' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, מוצג נטו – כל האשראי לזמן קצר, מבנקים ומאחרים, בסעיף 5 (R3) · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2, c4 · source irregularities: 1 (see §6) · report notes: 2 · Phase C: verbatim header c1, c2, c3, c4; issues +1.
  - Verification: Phase B batch 8 Builder (2026-11-10): Every line text (7 lines + total), every value (5 columns x 8 rows), the column headers (6M/3M 30.06.2026 and 2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with 100-DPI renders of PDF pages 92-94 (page_92/93/… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה 2026' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 בלתי מבוקר'; header_text c2: 'לתקופה של ש… (composites v1_23.png, v2_51.png).

### 2474 – ליאם הנדסה גרופ חריש מרכז עסקים בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2025 total (1); C2 per-item INFO rows (explained): 1.
- **Q1 2026** – `2474_ליאם הנדסה גרופ חריש מרכז עסקים בע_מ_2026_Q1_1745084.pdf` (report 1745084, 48 pp.) · cash-flow statement PDF pp. 31, 32 · financing p. 32 · column headers p. 32.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 5 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת הלוואות מתאגידים בנקאיים ואחרים' → 5: קבלת הלוואות מתאגידים בנקאיים ואחרים – ללא ציון תקופה בדוח; אותה שורה בדוח Q2 מוצגת נטו ('קבלת (פירעון) ...') – שורת הל… · n2 'פירעון הלוואות מתאגידים בנקאיים ואחרים' → 5: פירעון הלוואות מתאגידים בנקאיים ואחרים – פירעון האשראי שבשורה הקודמת, שורת פירעון ברוטו – סעיף 5. לידיעה: לפי דוח הדירק… · (+3 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (3 columns x 5 lines + total), the column headers (3M to 31.03.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with the rendered zoom page (header strip + financing section) of…
- **Q2 2026** – `2474_ליאם הנדסה גרופ חריש מרכז עסקים בע_מ_2026_Q2_1764180.pdf` (report 1764180, 53 pp.) · cash-flow statement PDF pp. 37, 38 · financing p. 38 · column headers p. 38.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת (פירעון) הלוואות מתאגידים בנקאיים ואחרים' → 5: קבלת (פירעון) הלוואות מתאגידים בנקאיים ואחרים – שורת הלוואות נטו ללא ציון תקופה = סעיף 5 (R3); לפי המאזן (עמ' 33) כל הא… · n2 'פירעון הלוואות מתאגידים בנקאים ואחרים' → 5: פירעון הלוואות מתאגידים בנקאיים ואחרים – פירעון האשראי שבשורה הקודמת, שורת פירעון ברוטו – סעיף 5. לידיעה: לפי דוח הדירק… · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text (wrapped label of line 1 joined; source spelling 'בנקאים' kept), every value (5 columns x 6 lines + total), the column headers (6M/3M to 30.06.2026/2025, FY 31.12.2025; no audit wording in this report), the units…

### 2478 – רייסדור יזמות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2025 total (14,540); C2 per-item INFO rows (explained): 3.
- **Q1 2026** – `2478_רייסדור יזמות בע_מ_2026_Q1_1743625.pdf` (report 1743625, 95 pp.) · cash-flow statement PDF pp. 37, 38 · financing p. 38 · column headers p. 38.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 5 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת הלוואות מתאגידים בנקאיים ואחרים, נטו' → 5: קבלת הלוואות מתאגידים בנקאיים ואחרים, נטו – שורת הלוואות המוצגת נטו ללא ציון תקופה (כולל מלווים אחרים) – סעיף 5 לפי R3;… · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2 · report notes: 2 · Phase C: verbatim header c2.
  - Verification: Phase B batch 5 Builder (2026-11-10): Consolidated statement (title 'דוחות מאוחדים על תזרימי המזומנים', pp. 37-38) confirmed on 100-DPI page renders. Every financing line text, every value (3 columns x 5 lines + total), the column headers (3M 31.3.2026/2025, FY 2025)… Phase C: header_text c2: 'ל-3 החודשים שהסתיימו ביום 31 במרץ 2025 בלתי מבוקר אלפי ש"ח' -> 'ל-3 החודשים שהסתיימו ביום 31 במרץ 2025 בלתי מבוקר' (composites v1_23.png).
- **Q2 2026** – `2478_רייסדור יזמות בע_מ_2026_Q2_1766702.pdf` (report 1766702, 47 pp.) · cash-flow statement PDF pp. 38, 39 · financing p. 39 · column headers p. 39.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 5 + total; אחר 0; check [0, 0, -1, 0, 0].
  - Judgement calls: n1 'קבלת (פירעון) הלוואות מתאגידים בנקאיים ואחרים, נטו' → 5: קבלת (פירעון) הלוואות מתאגידים בנקאיים ואחרים, נטו – שורת הלוואות המוצגת נטו ללא ציון תקופה (כולל מלווים אחרים) – סעיף… · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c3, c4, c5 · C1 ≠ 0 (source does not add up, explained): 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני) (-1) · source irregularities: 2 (see §6) · report notes: 2 · Phase C: verbatim header c3; issues +1.
  - Verification: Phase B batch 5 Builder (2026-11-10): Consolidated statement (title 'דוחות מאוחדים על תזרימי המזומנים', pp. 38-39) confirmed on 100-DPI page renders. Every financing line text (wrapped label joined), every value (5 columns x 5 lines + total; the positive 186 lease am… Phase C: header_text c3: 'ל-3 החודשים שהסתיימו ביום 30 ביוני 2026 בלתי מבוקר אלפי ש"ח' -> 'ל-3 החודשים שהסתיימו ביום 30 ביוני 2026 בלתי מבוקר'; issues += 1 (composites v1_23.png, v2_44.png).

### 2481 – אלמוג (כ.ד.א.י.) בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2481_אלמוג (כ.ד.א.י.) בע_מ_2026_Q1_1744517.pdf` (report 1744517, 53 pp.) · cash-flow statement PDF pp. 35, 36 · financing p. 36 · column headers p. 36.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 11 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת (פירעון) הלוואות ואשראי מתאגידים בנקאיים לזמן קצר…' → 5: אשראי והלוואות לזמן קצר מתאגידים בנקאיים, נטו – סעיף 5 · n2 'קבלת (פירעון) הלוואות מאחרים לזמן קצר' → 5: הלוואות לזמן קצר מאחרים, מוצגות נטו (קבלה/פירעון) – סעיף 5 · n6 'קבלת הלוואות מבעל עניין לזמן קצר' → 5: הלוואה לזמן קצר מבעל עניין (קבוצת הראל), כמוצג בדוח – סעיף 5 · n10 'השקעות בעלי זכויות שאינן מקנות שליטה' → 6: השקעות בעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 6 · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2 · report notes: 2.
  - Verification: Phase B batch 4 Builder (2026-11-10): Every line text (11 lines incl. a 2-line label + total; 'הלוואת' as printed), every value (3 columns; empty c1 cell of the NCI line = 0), the column headers (3M 31.03.2026/2025 'בלתי מבוקר', FY 'לשנה שהסתיימה ביום 31 בדצמבר, 2025…
- **Q2 2026** – `2481_אלמוג (כ.ד.א.י.) בע_מ_2026_Q2_1766407.pdf` (report 1766407, 59 pp.) · cash-flow statement PDF pp. 40, 41 · financing p. 41 · column headers p. 41.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 11 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת (פרעון) הלוואות ואשראי מתאגידים בנקאיים לזמן קצר,…' → 5: אשראי והלוואות לזמן קצר מתאגידים בנקאיים, נטו – סעיף 5 · n2 'קבלת (פרעון) הלוואות מאחרים לזמן קצר' → 5: הלוואות לזמן קצר מאחרים, מוצגות נטו (קבלה/פירעון) – סעיף 5 · n6 'קבלת הלוואות מבעל עניין לזמן קצר' → 5: הלוואה לזמן קצר מבעל עניין (קבוצת הראל), כמוצג בדוח – סעיף 5 · n10 'השקעות בעלי זכויות שאינן מקנות שליטה' → 6: השקעות בעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 6 · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2, c4 · report notes: 2.
  - Verification: Phase B batch 4 Builder (2026-11-10): Every line text (11 lines incl. a 2-line label + total; '(פרעון)' and 'מבעל עניין' as printed), every value (5 columns), the column headers (6M and 3M 30.06.2026/2025 'בלתי מבוקר', FY 31.12.2025 'מבוקר'), the units (אלפי ש"ח) and…

### 2483 – קבוצת גבאי-בניה,יזום,ניהול ואחזקות נדל"ן בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2025 total (-1); C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `2483_קבוצת גבאי-בניה,יזום,ניהול ואחזקות נדל_ן בע_מ_2026_Q1_1745002.pdf` (report 1745002, 79 pp.) · cash-flow statement PDF pp. 60, 61 · financing p. 60 · column headers p. 60.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'רכישת מניות חברה מאוחדת מבעל השליטה בחברה' → 14: רכישת מניות בחברה מאוחדת (גבאי מניבים) מבעל השליטה – רכישת זכויות שאינן מקנות שליטה בחברה בת שכבר בשליטה (ראו נספח פעיל… · n6 'פירעון הלוואות מבעלי שליטה, נטו' → 5: הלוואות מבעלי שליטה, מוצגות נטו ללא ציון תקופה – סעיף 5 (R3 ומוסכמות שלב B §5); כך גם בדוח Q2 · n9 'חלוקת דיבידנד לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n10 'עליה (ירידה) באשראי לזמן קצר מתאגידים בנקאיים ואחרים,…' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו – סעיף 5 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: context sections (captions).
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (word rows of pp.60-61). Visual verification: (1) read-only sub-agent with a fresh image budget, images actually displayed (220-DPI fin render, full pages 60-61, 300/600-D… Phase C: context_sections p61: ['פעילויות שלא במזומן'] -> ['פעילות שוטפת', "נספח א' – התאמות לפעילות השוטפת", "נספח ב' – רכישת חברות בנות שטופלו בעבר לפי שיטת… (composites v3_18.png).
- **Q2 2026** – `2483_קבוצת גבאי-בניה,יזום,ניהול ואחזקות נדל_ן בע_מ_2026_Q2_1764242.pdf` (report 1764242, 87 pp.) · cash-flow statement PDF pp. 65, 66, 67 · financing p. 65 · column headers p. 65.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check [0, 0, 5, 0, 0].
  - Judgement calls: n4 'רכישת מניות חברה מאוחדת מבעל השליטה בחברה' → 14: רכישת מניות בחברה מאוחדת (גבאי מניבים) מבעל השליטה – רכישת זכויות שאינן מקנות שליטה בחברה בת שכבר בשליטה (נספח ג': 'זכא… · n5 'פירעון הלוואות מבעלי שליטה, נטו' → 5: הלוואות מבעלי שליטה, מוצגות נטו ללא ציון תקופה – סעיף 5 (R3 ומוסכמות שלב B §5). בדוח Q1 הסכום לרבעון 1/2025 ((2,638) לפ… · n8 'חלוקת דיבידנד לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n10 'עליה באשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו – סעיף 5. בעמודת 3 החודשים אפריל–יוני 2026 מודפס (18,489) – ראו הערת העמודה… · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c3 · C1 ≠ 0 (source does not add up, explained): 3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני) (5) · source irregularities: 1 (see §6) · report notes: 2 · Phase C: context sections (captions).
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (word rows of pp.65-67). Visual verification: (1) read-only sub-agent with a fresh image budget, images actually displayed (220-DPI fin render, full pages 65-67, 300-DPI z… Phase C: context_sections p66: ['פעילות שוטפת', 'פעילויות שלא במזומן'] -> ['פעילות שוטפת', "נספח א' – התאמות לפעילות השוטפת", "נספח ב' – עלייה לשליטה בחברות ש… (composites v3_18.png, v3_19.png).

### 2486 – מותג עירוני בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (80), C2 3 חודשים שהסתיימו ב-31.03.2025 total (1,799); C2 per-item INFO rows (explained): 4.
- **Q1 2026** – `2486_מותג עירוני בע_מ_2026_Q1_1744097.pdf` (report 1744097, 45 pp.) · cash-flow statement PDF pp. 40, 41 · financing p. 41 · column headers p. 41.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'תקבולים מהנפקת מניות ואופציות, נטו' → 1: הנפקה לציבור (רישום ראשון של מניות החברה למסחר, 25.1.2026) של 5,120,000 מניות רגילות יחד עם 1,920,000 כתבי אופציה (סדרה… · n4 'קבלת הלוואה מגופים פיננסים' → 5: קבלת הלוואה מגופים פיננסים – הלוואות ליווי לפרויקטים מגופים חוץ-בנקאיים; שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (… · n5 'פירעון הלוואות מגופים פיננסיים' → 5: פירעון הלוואות מגופים פיננסיים – אותן הלוואות ליווי (התחייבות שוטפת) – סעיף 5, כמו שורת הקבלה (שונתה מסעיף 7 בשלב C) · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c1, c2 · report notes: 3 · Phase C: item n4 4→5, n5 7→5; line note n2, n3.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (7 lines + total; repaired-font labels compared with the image), every value (3 columns), the column headers (header taken from the financing page 41), the units (אלפי ש"ח) compared digit by digit with the 220-DPI… Phase C: line 4: item -> 5; line 5: item -> 5; line 2: note (A evidence); line 3: note (A evidence) (composites v2_02.png).
- **Q2 2026** – `2486_מותג עירוני בע_מ_2026_Q2_1766260.pdf` (report 1766260, 50 pp.) · cash-flow statement PDF pp. 44, 45 · financing p. 45 · column headers p. 45.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'תקבולים מהנפקת מניות ואופציות, נטו' → 1: הנפקה לציבור (רישום ראשון של מניות החברה למסחר, 25.1.2026) של 5,120,000 מניות רגילות יחד עם 1,920,000 כתבי אופציה (סדרה… · n4 'קבלת הלוואה מגופים פיננסים' → 5: קבלת הלוואה מגופים פיננסים – הלוואות ליווי לפרויקטים מגופים חוץ-בנקאיים; שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (… · n5 'פירעון הלוואות מגופים פיננסיים' → 5: פירעון הלוואות מגופים פיננסיים – אותן הלוואות ליווי (התחייבות שוטפת) – סעיף 5, כמו שורת הקבלה ובדוח Q1 (שונתה מסעיף 7 ב… · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c1, c2 · source irregularities: 1 (see §6) · report notes: 3 · Phase C: item n4 4→5, n5 7→5; line note n2, n3.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (7 lines + total), every value (5 columns), the column headers (c3 = 3 months ended 30.06.2026 confirmed on the image), the units (אלפי ש"ח) compared digit by digit with the 220-DPI zoom of the financing section (… Phase C: line 4: item -> 5; line 5: item -> 5; line 2: note (A evidence); line 3: note (A evidence) (composites v2_03.png).

### 2487 – אריה פרשקובסקי גרופ בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2487_אריה פרשקובסקי גרופ בע_מ_2026_Q1_1744311.pdf` (report 1744311, 52 pp.) · cash-flow statement PDF pp. 32, 33 · financing p. 32 · column headers p. 32.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'שינוי באשראי לזמן קצר מבנקים ואחרים, נטו' → 5: שינוי באשראי לזמן קצר מבנקים ואחרים, נטו – כולל מלווים אחרים – סעיף 5 · n5 'שינוי בהלוואות לבעלי שליטה' → 5: שינוי בהלוואות לבעלי שליטה – הלוואות מבעלי השליטה המוצגות נטו ללא ציון תקופה → סעיף 5 (R3) · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'מזומנים ששולמו במהלך התקופה: ריבית (נספח א - מידע נוסף על ת…' (p33, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 5,936, 4,639, 22,717); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (6 lines + total), every value (3 columns), the column headers, the units (אלפי ש"ח) compared digit by digit with the 220-DPI zoom of the financing section (screenshots PDF p.3) and the full pages 32-33 (screensho… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_37.png, v3_19.png).
- **Q2 2026** – `2487_אריה פרשקובסקי גרופ בע_מ_2026_Q2_1766830.pdf` (report 1766830, 57 pp.) · cash-flow statement PDF pp. 35, 36 · financing p. 35 · column headers p. 35.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'שינוי באשראי לזמן קצר מבנקים ואחרים, נטו' → 5: שינוי באשראי לזמן קצר מבנקים ואחרים, נטו – כולל מלווים אחרים – סעיף 5 · n6 'שינוי בהלוואות לבעלי שליטה' → 5: שינוי בהלוואות לבעלי שליטה – הלוואות מבעלי השליטה המוצגות נטו ללא ציון תקופה → סעיף 5 (R3) · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid outside financing: 'מזומנים ששולמו במהלך התקופה: ריבית (נספח א' - מידע נוסף על…' (p36, גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון): 13,533, 10,187, 7,597, 5,548, 22,717); remark: הסכומים כפי שמודפסים בנספח (ללא סוגריים) · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: context sections (captions); (*) section canonical 1; (*) note wording.
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (7 lines + total), every value (5 columns), the column headers, the units (אלפי ש"ח) compared digit by digit with the 220-DPI zoom of the financing section (screenshots PDF p.7) and the full pages 35-36 (screensho… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)'}; info_notes.interest removed (uniform note composed fro… (composites v2_38.png, v3_20.png).

### 2488 – קבוצת אופק (פ.ה.א.) השקעות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2025 total (-2); C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `2488_קבוצת אופק (פ.ה.א.) השקעות בע_מ_2026_Q1_1745649.pdf` (report 1745649, 49 pp.) · cash-flow statement PDF pp. 35, 36 · financing p. 36 · column headers p. 36.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו – סעיף 5 · n5 'קבלת (החזר) הלוואות מצדדים קשורים, נטו' → 5: הלוואות מצדדים קשורים, מוצגות נטו (קבלה/החזר) ללא ציון תקופה – סעיף 5 (R3 ומוסכמות שלב B §5) · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (repaired font; word rows of pp.35-36). Visual verification: (1) read-only sub-agent with a fresh image budget, images actually displayed (220-DPI fin render, full pages 3…
- **Q2 2026** – `2488_קבוצת אופק (פ.ה.א.) השקעות בע_מ_2026_Q2_1766252.pdf` (report 1766252, 99 pp.) · cash-flow statement PDF pp. 80, 81, 82 · financing p. 81 · column headers p. 81.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו – סעיף 5 · n5 'קבלת (החזר) הלוואות מצדדים קשורים, נטו' → 5: הלוואות מצדדים קשורים, מוצגות נטו (קבלה/החזר) ללא ציון תקופה – סעיף 5 (R3 ומוסכמות שלב B §5) · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: source irregularities: 1 (see §6) · report notes: 2 · Phase C: context sections (captions); issues +1.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (word rows of pp.80-82). Visual verification: (1) read-only sub-agent with a fresh image budget, images actually displayed (220-DPI fin render, full pages 80-82, 300-DPI z… Phase C: context_sections p82: None -> ['(ב) חברה מאוחדת שיצאה מאיחוד במסגרת שינוי מבנה', '(ג) פעילויות מהותיות שאינן במזומן']; issues += 1 (composites v3_20.png).

### 2503 – לנטרה קנדה אנטרפרייזס לימיטד פרטנרשיפ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (-1,793); C2 per-item INFO rows (explained): 3.
- **Q1 2026** – `2503_לנטרה קנדה אנטרפרייזס לימיטד פרטנרשיפ_2026_Q1_1743729.pdf` (report 1743729, 141 pp.) · cash-flow statement PDF pp. 48, 49 · financing p. 49 · column headers p. 49.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: באלפי דולר קנדי (דולר קנדי, אלפים). Text layer: usable.
  - Lines: 11 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'רכישת זכויות שאינן מקנות שליטה' → 14: רכישת זכויות שאינן מקנות שליטה בחברה מאוחדת (עסקה הונית ללא שינוי בשליטה; בדוח על השינויים בהון: 'עסקה עם בעלי זכויות ש… · n4 'הלוואות ללא מועד פרעון לבעלי השליטה' → 11: הלוואה ללא מועד פירעון שהעמידה השותפות לבעל השליטה; נזקפה ישירות להון (טור 'קרן הון עם בעל שליטה' בדוח על השינויים בהון… · n5 'תקבולים מבעלי זכויות שאינן מקנות שליטה' → 6: תקבולים מבעלי זכויות שאינן מקנות שליטה (השקעות זשמ"ש בחברות/שותפויות מאוחדות; בדוח על השינויים בהון 'השקעות' בטור זכויו… · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c1, c2 · report notes: 3 · Phase C: verbatim header c3.
  - Verification: Phase B batch 8 Builder (2026-11-10): Every line text (11 lines + total; wrapped labels joined), every value (3 columns x 12 rows), the column headers (3M 31.03.2026 / 3M 31.03.2025 / FY 31.12.2025), the units ('באלפי דולר קנדי, למעט אם צוין אחרת') compared digit by… Phase C: header_text c3: 'לשנה שהסתיימה ביום 31 2025 מבוקר' -> 'לשנה שהסתיימה ביום 31 בדצמבר 2025 מבוקר' (composites v1_24.png).
- **Q2 2026** – `2503_לנטרה קנדה אנטרפרייזס לימיטד פרטנרשיפ_2026_Q2_1765098.pdf` (report 1765098, 167 pp.) · cash-flow statement PDF pp. 51, 52 · financing p. 52 · column headers p. 52.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: באלפי דולר קנדי (דולר קנדי, אלפים). Text layer: usable.
  - Lines: 11 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'רכישת זכויות שאינן מקנות שליטה' → 14: רכישת זכויות שאינן מקנות שליטה בחברה מאוחדת (עסקה הונית ללא שינוי בשליטה) – סעיף 14 · n4 'הלוואות ללא מועד פרעון לבעלי השליטה' → 11: הלוואה ללא מועד פירעון שהעמידה השותפות לבעל השליטה; נזקפה ישירות להון (טור 'קרן הון עם בעל שליטה' בדוח על השינויים בהון… · n5 'תקבולים מבעלי זכויות שאינן מקנות שליטה' → 6: תקבולים מבעלי זכויות שאינן מקנות שליטה (השקעות זשמ"ש בחברות/שותפויות מאוחדות) – סעיף 6 · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c3, c4 · report notes: 3 · Phase C: verbatim header c4.
  - Verification: Phase B batch 8 Builder (2026-11-10): Every line text (11 lines + total), every value (5 columns x 12 rows), the column headers (6M/3M 30.06.2026 and 2025, FY 31.12.2025), the units ('באלפי דולר קנדי, למעט אם צוין אחרת') compared digit by digit with the 220-DPI tool_… Phase C: header_text c4: 'ל-3 החודשים שהסתיימו ביום 30 ביוני 2025 (בלתי מבוקר)' -> 'ל-3 החודשים שהסתיימו ביום 30 ביוני 2025 בלתי מבוקר' (composites no new image needed (rule-based change / note wording only)).

### 2520 – איסתא נכסים בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2520_איסתא נכסים בע_מ_2026_Q1_1742735.pdf` (report 1742735, 56 pp.) · cash-flow statement PDF pp. 30, 31 · financing p. 30 · column headers p. 30.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n8 'דיבידנד לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n9 'קבלת אשראי מהחברה האם ובעלי מניות אחרים' → 4: אשראי מהחברה האם ובעלי מניות אחרים: היתרה מוצגת במאזן (עמ' 25) כ'הלוואות מהחברה האם ובעלי מניות אחרים' בהתחייבויות לא ש… · n10 'פירעון אשראי מהחברה האם ובעלי מניות אחרים' → 7: פירעון אשראי מהחברה האם ובעלי מניות אחרים: היתרה מוצגת במאזן (עמ' 25) כ'הלוואות מהחברה האם ובעלי מניות אחרים' בהתחייבוי… · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2, c3.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שלושה חודשים שהסתיימה ביום 31 במרץ 2026 (בלתי… (composites v1_24.png).
- **Q2 2026** – `2520_איסתא נכסים בע_מ_2026_Q2_1765451.pdf` (report 1765451, 61 pp.) · cash-flow statement PDF pp. 32, 33 · financing p. 32 · column headers p. 32.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n8 'דיבידנד לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד לבעלי זכויות שאינן מקנות שליטה בחברות בנות · n9 'קבלת אשראי מהחברה האם ובעלי מניות אחרים' → 4: אשראי מהחברה האם ובעלי מניות אחרים: היתרה מוצגת במאזן (עמ' 25) כ'הלוואות מהחברה האם ובעלי מניות אחרים' בהתחייבויות לא ש… · n10 'פירעון אשראי מהחברה האם ובעלי מניות אחרים' → 7: פירעון אשראי מהחברה האם ובעלי מניות אחרים: היתרה מוצגת במאזן (עמ' 25) כ'הלוואות מהחברה האם ובעלי מניות אחרים' בהתחייבוי… · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c3 · source irregularities: 1 (see §6) · report notes: 2 · Phase C: verbatim header c1, c2, c3, c4, c5; issues +1.
  - Verification: Phase B batch 5 Builder (re-check after the image-cap issue) (2026-11-10): RE-VERIFIED 2026-11-10 ~11:20-11:45 after the orchestrator's image-cap follow-up: in the first pass the 'view' tool had NOT displayed the rendered images (50-image cap message), so that pass was text-layer only. This record repla… Phase C: header_text c1: 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 אלפי ש"ח (בלתי מבוקר)' -> 'לתקופה של שישה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי… (composites v1_24.png, v2_45.png).

### 2521 – קטה גרופ - גיל קטה בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (-1); C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `2521_קטה גרופ - גיל קטה בע_מ_2026_Q1_1745082.pdf` (report 1745082, 42 pp.) · cash-flow statement PDF pp. 34, 35 · financing p. 35 · column headers p. 35.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'שינוי באשראי לזמן קצר מבנקים ואחרים, נטו' → 5: שינוי באשראי לזמן קצר מבנקים ואחרים, מוצג נטו – סעיף 5 (כולל מלווים אחרים ולא רק תאגידים בנקאיים) · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (3 columns x 7 lines + total), the column headers (3M to 31.03.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with the rendered zoom page (header strip + financing section) of…
- **Q2 2026** – `2521_קטה גרופ - גיל קטה בע_מ_2026_Q2_1764973.pdf` (report 1764973, 47 pp.) · cash-flow statement PDF pp. 37, 38 · financing p. 38 · column headers p. 38.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'שינוי באשראי לזמן קצר מבנקים ואחרים, נטו' → 5: שינוי באשראי לזמן קצר מבנקים ואחרים, מוצג נטו – סעיף 5 (כולל מלווים אחרים ולא רק תאגידים בנקאיים) · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c2, c4, c5 · report notes: 2.
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text, every value (5 columns x 7 lines + total), the column headers (6M/3M to 30.06.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared digit by digit with the rendered zoom page (header strip + financing section)…

### 2522 – עומר הנדסה ובניה (1986) בע"מ

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 2.
- **Q1 2026** – `2522_עומר הנדסה ובניה (1986) בע_מ_2026_Q1_1744985.pdf` (report 1744985, 32 pp.) · cash-flow statement PDF pp. 25, 26, 27 · financing p. 25 · column headers p. 25.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 4 + total; אחר 0; check 0 in every column.
  - Judgement calls: none beyond the wording of the lines (4).
  - (*) classification: interest paid outside financing: 'נספח א' – התאמות הדרושות להצגת מזומנים ושווי מזומנים מפעילו…' (p26, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: -6,132, -7,007, -27,111) · dividends paid: no line in the statement → (*) row 0.
  - Flags: column notes: c1 · source irregularities: 1 (see §6) · report notes: 3 · Phase C: context sections (captions); (*) section canonical 1; issues +1.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (4 lines + total), every value (3 columns), the column headers, the units (באלפי ש"ח) and the appendix-A (*) interest line (p. 26, inside the operating adjustments) compared digit by digit with 220-DPI renders (to… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת'}; info_notes.interest removed (uniform note composed from sections); c… (composites v2_17.png, v3_21.png).
- **Q2 2026** – `2522_עומר הנדסה ובניה (1986) בע_מ_2026_Q2_1766495.pdf` (report 1766495, 34 pp.) · cash-flow statement PDF pp. 27, 28, 29 · financing p. 27 · column headers p. 27.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: באלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 5 + total; אחר 0; check 0 in every column.
  - Judgement calls: none beyond the wording of the lines (5).
  - (*) classification: interest paid outside financing: 'נספח א' – התאמות הדרושות להצגת מזומנים ושווי מזומנים מפעילו…' (p28, גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת: -12,181, -13,905, -6,049, -6,898, -27,111) · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c1 · report notes: 3 · Phase C: context sections (captions); (*) section canonical 1.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (5 lines + total), every value (5 columns), the column headers, the units (באלפי ש"ח) and the appendix-A (*) interest line (p. 28, inside the operating adjustments) compared digit by digit with 220-DPI renders (to… Phase C: outside_sections {'1': 'גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת'}; info_notes.interest removed (uniform note composed from sections); c… (composites v2_18.png, v3_22.png).

### 2524 – אי.אס.איי אחזקות בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2026 total (1); C2 per-item INFO rows (explained): 1.
- **Q1 2026** – `2524_אי.אס.איי אחזקות בע_מ_2026_Q1_1744218.pdf` (report 1744218, 50 pp.) · cash-flow statement PDF pp. 29 · financing p. 29 · column headers p. 29.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר [-9, -1,961, -3,215]; check 0 in every column.
  - Judgement calls: n2 'אשראי מתאגידים בנקאיים, נטו' → 5: אשראי מתאגידים בנקאיים, מוצג נטו ללא ציון תקופה – סעיף 5 · n3 'שינוי בבעלי עניין' → אחר: שינוי ביתרות בעלי עניין: במאזן 'בעלי עניין' מוצגים בנכסים בלבד (שוטפים ושאינם שוטפים) – כלומר יתרות חובה/הלוואות שהחברה… · n4 'שינוי בהלוואה מאחרים' → 5: שינוי (נטו) בהלוואות מאחרים, ללא ציון תקופה (במאזן 'הלוואות מאחרים' בהתחייבויות שוטפות ושאינן שוטפות) – סעיף 5 (R3: שור… · n7 'השקעות מהזשמ"ש' → 6: השקעות של בעלי זכויות שאינן מקנות שליטה (זשמ"ש) בחברות בנות – סעיף 6 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (word rows of p.29). Visual verification: (1) read-only sub-agent with a fresh image budget, images actually displayed (220-DPI fin render, full page 29, 300-DPI zooms of…
- **Q2 2026** – `2524_אי.אס.איי אחזקות בע_מ_2026_Q2_1765965.pdf` (report 1765965, 111 pp.) · cash-flow statement PDF pp. 31 · financing p. 31 · column headers p. 31.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 8 + total; אחר [-39, -2,723, -30, -762, -3,215]; check 0 in every column.
  - Judgement calls: n2 'אשראי מתאגידים בנקאיים, נטו' → 5: אשראי מתאגידים בנקאיים, מוצג נטו ללא ציון תקופה – סעיף 5 · n3 'שינוי בבעלי עניין' → אחר: שינוי ביתרות בעלי עניין: במאזן 'בעלי עניין' מוצגים בנכסים בלבד (שוטפים ושאינם שוטפים) – כלומר יתרות חובה/הלוואות שהחברה… · n4 'שינוי בהלוואה מאחרים' → 5: שינוי (נטו) בהלוואות מאחרים, ללא ציון תקופה (במאזן 'הלוואות מאחרים' בהתחייבויות שוטפות ושאינן שוטפות) – סעיף 5 (R3: שור… · n7 'השקעות מהזשמ"ש' → 6: השקעות של בעלי זכויות שאינן מקנות שליטה (זשמ"ש) בחברות בנות – סעיף 6 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 2.
  - Verification: Phase B batch 4 Builder (2026-11-10): Values, labels and headers first read from the text layer (word rows of p.31). Visual verification: (1) read-only sub-agent with a fresh image budget, images actually displayed (220-DPI fin render, full page 31, 300-DPI zooms of…

### 2533 – אל עד יו אס קפיטל הולדינגס לימיטד

- Cross-report checks: C2/C3 mismatches (explained): none; C2 per-item INFO rows (explained): 0.
- **Q1 2026** – `2533_אל עד יו אס קפיטל הולדינגס לימיטד_2026_Q1_1742828.pdf` (report 1742828, 51 pp.) · cash-flow statement PDF pp. 36 · financing p. 36 · column headers p. 36.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: באלפי דולר ארה"ב (דולר ארה"ב, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check [0, 0, -1,000].
  - Judgement calls: none beyond the wording of the lines (6).
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c1, c2, c3 · C1 ≠ 0 (source does not add up, explained): שנה שהסתיימה ב-31.12.2025 (-1,000) · source irregularities: 2 (see §6) · report notes: 3.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(…
- **Q2 2026** – `2533_אל עד יו אס קפיטל הולדינגס לימיטד_2026_Q2_1766889.pdf` (report 1766889, 56 pp.) · cash-flow statement PDF pp. 38 · financing p. 38 · column headers p. 38.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: באלפי דולר ארה"ב (דולר ארה"ב, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check [0, 0, 0, 0, -1,000].
  - Judgement calls: none beyond the wording of the lines (6).
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c5 · C1 ≠ 0 (source does not add up, explained): שנה שהסתיימה ב-31.12.2025 (-1,000) · source irregularities: 1 (see §6) · report notes: 3 · Phase C: verbatim header c1, c3.
  - Verification: Phase B batch 1 Builder (2026-11-10): Verified on rendered images (viewed by the builder): the pages of the company screenshots PDF rendered by tool_shots.py – the 220-DPI zoomed crop of the column-header strip + the whole financing section and the 150-DPI full page(… Phase C: header_text c1: 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026' -> 'לשישה חודשים שהסתיימו ביום 30 ביוני 2026 (בלתי מבוקר)'; header_text c3: 'לשלושה חודשים… (composites v1_25.png).

### 2557 – קבוצת תדהר בע"מ

- **Q1 2026: not in the folder** (listed in `חסרים והערות` as `דוח חסר`; not downloaded – out of scope).
- **Q2 2026** – `2557_קבוצת תדהר בע_מ_2026_Q2_1765408.pdf` (report 1765408, 94 pp.) · cash-flow statement PDF pp. 52, 53, 54 · financing p. 53 · column headers p. 53.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 12 + total; אחר 0; check 0 in every column.
  - Judgement calls: n5 'מימוש כתבי אופציה' → 2: מימוש כתבי אופציה – סעיף 2 · n6 'רכישת זכויות מבעלי זכויות שאינן מקנות שליטה' → 14: רכישת זכויות מבעלי זכויות שאינן מקנות שליטה בחברה בת (עסקה הונית, ללא שינוי בשליטה) – סעיף 14 · n10 'קבלת (פירעון) הלוואות לזמן קצר מתאגידים בנקאיים, נטו' → 5: קבלת (פירעון) הלוואות לזמן קצר מתאגידים בנקאיים, נטו – סעיף 5 · n12 'דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה' → 12: דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה בחברות בנות – סעיף 12 · (+8 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: report notes: 3 · Phase C: line note n7, n8; context sections (captions).
  - Verification: Phase B batch 2 Builder (2026-11-10): Every line text (wrapped labels joined; the note reference of line 8 read on a 400-DPI clip), every value (5 columns x 12 lines + total), the column headers (6M/3M to 30.06.2026/2025, FY 31.12.2025), the units (אלפי ש"ח) compared… Phase C: line 7: note (A evidence); line 8: note (A evidence); context_sections p54: None -> ['א. פעילויות מהותיות שלא במזומן', 'ב. רכישת חברה מאוחדת שאוחדה ל… (composites v2_08.png, v3_23.png).

### 2559 – קבוצת בסט א.ע.ו בע"מ

- Cross-report checks: C2/C3 mismatches (explained): C2 3 חודשים שהסתיימו ב-31.03.2025 total (-2); C2 per-item INFO rows (explained): 4.
- **Q1 2026** – `2559_קבוצת בסט א.ע.ו בע_מ_2026_Q1_1771495-01.pdf` (report 1771495, 51 pp.) · cash-flow statement PDF pp. 24, 25 · financing p. 25 · column headers p. 25.
  - Periods: c1 3M→31.03.2026 · c2 3M→31.03.2025 · c3 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 8 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'פירעון הלוואות מתאגידים מוחזקים ובעלי עניין' → 5: הלוואות מתאגידים מוחזקים ובעלי עניין, ללא ציון תקופה; השורה מוצגת למעשה נטו (ברבעון 1/2026 מודפס סכום חיובי 2,707 בשורת… · n6 'אשראי לזמן קצר מתאגידים בנקאיים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים, נטו – סעיף 5 · (+6 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c2, c3 · report notes: 3.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (8 lines + total), every value (3 columns), the column headers, the units (אלפי ש"ח in the statement header) and the absence of (*) lines outside financing compared digit by digit with the 220-DPI render (tool_rev…
- **Q2 2026** – `2559_קבוצת בסט א.ע.ו בע_מ_2026_Q2_1767813.pdf` (report 1767813, 57 pp.) · cash-flow statement PDF pp. 31, 32 · financing p. 32 · column headers p. 32.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 10 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'תשלום לבעל עניין בגין התאמת תמורה' → 1: תשלום להפניקס (בעל עניין, משקיע בחברה) של 52,500 בגין 'התאמת תמורה' – פיצוי אירוע IPO לפי הסכם ההשקעה (5% מעליית שווי ה… · n6 'קבלת (פרעון) הלוואות מתאגידים מוחזקים ובעלי עניין' → 5: הלוואות מתאגידים מוחזקים ובעלי עניין, מוצגות נטו (קבלה/פירעון) ללא ציון תקופה – סעיף 5 (R3); בדוח Q1 2026 אותה שורה ('פ… · n8 'אשראי לזמן קצר מתאגידים בנקאיים, נטו' → 5: אשראי לזמן קצר מתאגידים בנקאיים, נטו – סעיף 5 · (+7 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: column notes: c5 · source irregularities: 1 (see §6) · report notes: 3 · Phase C: issues +1.
  - Verification: Phase B batch 7 Builder (2026-11-10): Every line text (10 lines + total, wrapped labels joined), every value (5 columns; 387,219 confirmed on the image despite the text-layer comma error), the column headers, the units (אלפי ש"ח) and the absence of (*) lines outside… Phase C: issues += 1 (composites v2_50.png).

### 2567 – רם מוגרבי ארדיטי בע"מ

- **Q1 2026: not in the folder** (listed in `חסרים והערות` as `דוח חסר`; not downloaded – out of scope).
- **Q2 2026** – `2567_רם מוגרבי ארדיטי בע_מ_2026_Q2_1767289.pdf` (report 1767289, 69 pp.) · cash-flow statement PDF pp. 53, 54, 55 · financing p. 54 · column headers p. 54.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable (repaired).
  - Lines: 9 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'ריבית ששולמה על שטרי הון' → 11: ריבית ששולמה על שטרי הון – שטרי ההון של בעלי המניות סווגו בהון העצמי (עמודת 'שטר הון' בדוחות על השינויים בהון; ב-2025 מ… · n4 'פרעון הלוואות לזמן קצר מבעלי מניות' → 5: פרעון הלוואות לזמן קצר מבעלי מניות (הלוואות הבעלים לזמן קצר שהומרו משטרי הון ב-2025; נפרעו ב-30.3.2026) – אשראי לזמן קצ… · n5 'קבלת הלוואות מחברות כלולות, צדדים קשורים ואחרים' → 5: קבלת הלוואות מחברות כלולות, צדדים קשורים ואחרים – ללא ציון תקופה; במאזן אין התחייבות לא שוטפת בגינן (ההתחייבויות הלא שו… · n6 'פרעון התחייבות בגין נכסי זכות שימוש' → 10: פרעון התחייבות בגין נכסי זכות שימוש = פירעון התחייבות בגין חכירה; ללא פיצול קרן/ריבית בדוח → סעיף 10 · n7 'קבלת הלוואות לזמן קצר' → 5: קבלת הלוואות לזמן קצר – סעיף 5 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: in financing only (items 11/12) → (*) row 0.
  - Flags: source irregularities: 1 (see §6) · report notes: 3 · Phase C: context sections (captions).
  - Verification: Phase B batch 3 Builder (2026-11-10): Every line text (9 lines + total; repaired-font labels compared with the image), every value (5 columns), the column headers, the units (אלפי ש"ח) compared digit by digit with the 220-DPI zoom of the financing section (screenshot… Phase C: context_sections p55: None -> ['פעילויות מהותיות שאינן במזומן'] (composites v3_23.png).

### 2570 – ס.י לאונרדו התחדשות עירונית בע"מ

- **Q1 2026: not in the folder** (listed in `חסרים והערות` as `דוח חסר`; not downloaded – out of scope).
- **Q2 2026** – `2570_ס.י לאונרדו התחדשות עירונית בע_מ_2026_Q2_1767187.pdf` (report 1767187, 68 pp.) · cash-flow statement PDF pp. 41, 42 · financing p. 41 · column headers p. 41.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ש"ח (ש"ח, אלפים). Text layer: usable.
  - Lines: 7 + total; אחר 0; check 0 in every column.
  - Judgement calls: n4 'קבלת הלוואות מצדדים קשורים' → 5: קבלת הלוואות מצדדים קשורים – שורה ברוטו ללא ציון תקופה – לפי כלל היישור A (סיווג במאזן ובביאורים): אשראי/הלוואות המסווג… · n5 'פירעון הלוואות מצדדים קשורים' → 5: פירעון הלוואות מצדדים קשורים – אותן הלוואות (התחייבות שוטפת) – סעיף 5, כמו שורת הקבלה. במאזן המאוחד (עמ' 37) 'הלוואות מ… · (+5 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 3 · Phase C: item n4 4→5, n5 7→5; verbatim header c1, c2, c3, c4, c5.
  - Verification: Phase B batch 8 Builder (2026-11-10): Statement pick confirmed: pp. 41-42 are titled 'דוחות תמציתיים מאוחדים של תזרימי המזומנים' (consolidated) and pp. 59-60 'תמצית נתונים על תזרימי המזומנים ביניים' (separate, figures differ) – both viewed. Every line text (7 lines +… Phase C: header_text c1: 'לתקופה של ששה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי מבוקר) אלפי ש"ח' -> 'לתקופה של ששה חודשים שהסתיימה ביום 30 ביוני 2026 (בלתי מ… (composites v1_25.png, v2_06.png).

### 2574 – עמים יזמות בע"מ

- **Q1 2026: not in the folder** (listed in `חסרים והערות` as `דוח חסר`; not downloaded – out of scope).
- **Q2 2026** – `2574_עמים יזמות בע_מ_2026_Q2_1767720.pdf` (report 1767720, 39 pp.) · cash-flow statement PDF pp. 30 · financing p. 30 · column headers p. 30.
  - Periods: c1 6M→30.06.2026 · c2 6M→30.06.2025 · c3 3M→30.06.2026 (Apr–Jun) · c4 3M→30.06.2025 (Apr–Jun) · c5 12M→31.12.2025. Units: אלפי ₪ (ש"ח, אלפים). Text layer: usable.
  - Lines: 6 + total; אחר 0; check 0 in every column.
  - Judgement calls: n1 'קבלת הלוואות מצדדים קשורים' → 5: קבלת הלוואות מצדדים קשורים (שורה ברוטו, ללא ציון תקופה); במאזן המאוחד היתרה לצדדים קשורים מוצגת בהתחייבויות השוטפות בלב… · n2 'פרעון הלוואות מצדדים קשורים' → 5: פרעון הלוואות מצדדים קשורים (שורה ברוטו, ללא ציון תקופה; היתרה במאזן שוטפת בלבד) – אשראי לזמן קצר מאחרים – סעיף 5 · (+4 line(s) mapped by their wording)
  - (*) classification: interest paid: in financing only (item 13) → (*) row 0 · dividends paid: no line in the statement → (*) row 0.
  - Flags: report notes: 2 · Phase C: verbatim header c1, c2, c3, c4.
  - Verification: Phase B batch 6 Builder (2026-11-10): Every line text (6 lines + total), every value (5 columns x 7 lines), the column headers (6M/6M/3M/3M/FY; c2 = 6 months ended 30.06.2025 confirmed on the image), the units (אלפי ₪) and the absence of (*) lines outside financing c… Phase C: header_text c1: 'החודשים שהסתיימו ביום 30 ביוני 2026 6 החודשים שהסתיימו 30-ב ביוני 2026' -> '6 החודשים שהסתיימו ב-30 ביוני 2026 (בלתי מבוקר)'; header… (composites v1_25.png).

---------------------------------------------------------------------------------------------------------------

Assisted-by: Anthropic:Claude Opus 5.5
