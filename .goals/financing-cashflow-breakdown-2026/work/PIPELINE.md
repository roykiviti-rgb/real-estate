# PIPELINE — protocol for the Phase B batch Builders

Financing cash-flow breakdown 2026 (goal: `..\goal.md`, amendments `..\goal-amendment-1.md`, `..\goal-amendment-2.md`).
Written by the Phase A Builder. **You may not edit any script** (`*.py`, `*.ps1`), `roles.json`, `triage*.`,
`batches.json` or anything outside the files listed in §2. If a script is wrong or missing something, work around it
with override files and report a `SCRIPT-ISSUE` (§12).

Paths used below:

| name | path |
|---|---|
| WORKSPACE | `C:\Users\רואי\OneDrive - huji.ac.il\שולחן העבודה\agent folder\פרק ד'\דוחות כספיים\בדיקה רון\נדל_ן ובינוי - מחזור 2` |
| GOAL DIR | `WORKSPACE\.goals\financing-cashflow-breakdown-2026` |
| W (work) | `GOAL DIR\work` – scripts, `roles.json`, `overrides\`, `data\` |
| TEMP | `%TEMP%\fcf_run\` – every render / review file / run log (never in WORKSPACE) |

---------------------------------------------------------------------------------------------------------------

## 0. The loop, per report (company × quarter)

1. `tool_review.py <iss> <Q>` → look at `fin_*.png` (header strip + financing section, lines framed and numbered) and
   `lines_*.txt` (the extracted lines and values) side by side; look at `page_*.png` for the rest of the statement.
2. Write/extend `W\overrides\<iss>_<Q>.json` for everything that is wrong or needs a decision (§4–§6).
3. `finalize_report.py <iss> <Q>` → re-run `tool_review.py` (it now shows the final data) → repeat until every
   number, label, column, unit, item and (*) line is right.
4. Add the `verified` record (§8) → `finalize_report.py` again.
5. When both reports of the company are verified: `checks.py --issuers <iss>` → fix or explain every C1/C2/C3
   difference (§9) → `build_company.py <iss>` → `tool_shots.py <iss>` (look at the pages) →
   `validate.py --issuers <iss> --no-master` must end with `FAIL 0` (§10).
6. Write the company's section in your batch report (§13).

Start with `W\triage.csv` (one row per report: pages, columns, units, number of lines, `אחר` candidates, (*) lines,
C1/C2/C3 on the auto data, text-layer status, flags, difficulty A/B/C and Phase A notes `[שלב A] ...`).
Difficulty: **A** auto-clean (still verify every digit), **B** targeted review (read the flags), **C** heavy work.

---------------------------------------------------------------------------------------------------------------

## 1. Running the scripts

PowerShell 5 (no `&&`). Every call is a fresh process that starts in WORKSPACE; the scripts find their own paths, so
they can be run from any directory. Always set the two environment variables in the same call:

```powershell
$env:PYTHONIOENCODING = 'utf-8'; $env:PYTHONDONTWRITEBYTECODE = '1'
$W = Join-Path (Get-Location) '.goals\financing-cashflow-breakdown-2026\work'      # shell starts in WORKSPACE
python "$W\tool_review.py" 1039 Q1
```

If a shell does not start in WORKSPACE, build `$W` from the absolute WORKSPACE path (in a single-quoted PowerShell
string the apostrophe of `פרק ד'` must be doubled: `'...\פרק ד''\...'`).

* Hebrew through PowerShell pipes is mangled: never pipe Hebrew text into python (`@'...'@ | python -` breaks on the
  Hebrew paths). Write UTF-8 `.py`/`.json` files with the create/edit tools, run them, write results to UTF-8 files and
  read those files with the `view` tool.
* **The `view` tool caches files by path.** All helpers write time-stamped names (`fin_<hhmmss>.png`, `lines_<hhmmss>.txt`,
  `grid_..._<hhmmss>.png`, `shots_<hhmmss>\`). If you write your own files, use new names each time.
* Never create `__pycache__` (keep `PYTHONDONTWRITEBYTECODE=1`), never open the workspace xlsx in Excel (lock files
  `~$*`); to inspect a workbook use `tool_excel_check.ps1` (it copies it to TEMP first).

### Commands (all accept `<iss>` = issuer number, `<Q>` = `Q1` | `Q2`)

| command | what it does | writes |
|---|---|---|
| `python "$W\tool_review.py" <iss> <Q> [--dpi 220] [--pages-dpi 100]` | review package for one report (uses final data if newer than the auto data) | `TEMP\<iss>\review_<Q>\fin_*.png, lines_*.txt, outside_k_*.png, page_<p>_*.png` |
| `python "$W\tool_grid.py" <iss> <Q> <page> [--clip y0 y1] [--dpi 150] [--step 10] [--file <pdf>]` | page with a labelled coordinate grid (PDF points, origin top-left) to read boxes | `TEMP\<iss>\grid_<Q>_p<page>_*.png` |
| `python "$W\tool_scan.py" <iss> <Q> [--pages 40-60] [--file <pdf>]` | how the extractor sees each page (titles, solo/board/notes flags, sections) and the candidate statements | `TEMP\<iss>\scan_<iss>_<Q>.txt` |
| `python "$W\extract_report.py" <iss> <Q> [--pages 55,56]` | re-run the automatic extraction (honours override `source_file` / `cf_pages`) | `W\data\<iss>_<Q>.auto.json` |
| `python "$W\finalize_report.py" <iss> <Q>` | auto data + override → final data (stops with a message on any inconsistency) | `W\data\<iss>_<Q>.json` |
| `python "$W\checks.py" --issuers <iss> [<iss2> ...]` | C1/C2/C3 (+ C2 per item, informational) with your explanations | `TEMP\_runs\checks_*\` (paths printed) |
| `python "$W\build_company.py" <iss> [--draft] [--no-pdf]` | the company workbook + screenshots PDF (without `--draft` both reports must be verified) | the 2 files in the company folder |
| `python "$W\tool_shots.py" <iss> [dpi] [--pages 2,3]` | render the company screenshots PDF to PNGs + info (sizes, TOC) | `TEMP\<iss>\shots_<hhmmss>\` |
| `python "$W\tool_clip.py" <iss> <page> <x0> <y0> <x1> <y1> [dpi]` | zoom into a page of the company screenshots PDF | `TEMP\<iss>\clip_*.png` |
| `python "$W\validate.py" --issuers <iss> --no-master` | independent re-check of the company outputs (AC2–AC13 without the master) | `TEMP\_runs\validate_*\validate.txt` |
| `python "$W\tool_batch.py" extract\|finalize\|build\|review --issuers <your issuers> [--draft] [--workers 4]` | the same steps for several of **your** issuers in parallel | per-run folder in `TEMP\_runs\` |
| `powershell -File "$W\tool_excel_check.ps1" -Src "<xlsx>" -OutDir "$env:TEMP\fcf_run\<iss>\excel"` | open a COPY with Excel, recalc, dump cells, export sheets to PDF (then `tool_pdf2png.py <dir>`) | that OutDir |
| `python "$W\tool_dump.py" <pdf> <out.txt> words <p>` / `tool_pdfclip.py` | low-level text/word dump, page clip (give output paths under `TEMP\<iss>\`) | the given path |
| `python "$W\tool_selftest.py" [<iss> <Q>]` | self-test of manual mode and of every override key on a temp copy (never touches overrides/data/outputs) | `TEMP\_runs\selftest_*\` |

**Do not run** (Phase A / Phase C only, they write shared files): `build_master.py`, `tool_triage.py` without
`--issuers`, `tool_batches.py`, `tool_roles.py`, `tool_inventory.py`, `tool_batch.py --all`.
Read-only and safe at any time: `tool_integrity.py`, `checks.py`, `validate.py` (use `--issuers`), `tool_scan.py`,
`tool_grid.py`, `tool_review.py`, `tool_selftest.py`.

---------------------------------------------------------------------------------------------------------------

## 2. What a batch may touch

Only for **your own issuers**:

* `W\overrides\<iss>_Q1.json`, `W\overrides\<iss>_Q2.json` – the review decisions and the verification record;
* `W\overrides\<iss>_checks.json` – explanations of C1/C2/C3 differences;
* `W\data\<iss>_*.json` – only through `extract_report.py` / `finalize_report.py` (never edit data files by hand);
* the company outputs `WORKSPACE\<company folder>\<iss> - פירוט תזרים מימון 2026.xlsx` and
  `... - צילומי מסך תזרים מימון 2026.pdf` – only through `build_company.py`;
* `%TEMP%\fcf_run\<iss>\` and the per-run folders the scripts create in `%TEMP%\fcf_run\_runs\`;
* your batch report (path given by the orchestrator).

Never: the source PDFs (open them read-only; nothing may be written into the company folders except the two outputs),
the scripts, `roles.json`, `roles_2559.json`, `triage.csv`, `triage_notes.json`, `batches.json`, `PIPELINE.md`,
`check_explanations.json` (global – Phase C), the master workbook, other batches' files, git.

---------------------------------------------------------------------------------------------------------------

## 3. Reviewing a report

`lines_*.txt` shows, in statement order: `n` (final line number = `#n` in `fin_*.png`), `key` (the line number of the
**auto** extraction – the number to use in override keys), page, item, one value per column **as printed**
(`(1,234)` = negative, `-` = 0, `·` = nothing read), the verbatim text, flags and the mapping note; then C1 per column,
the (*) lines found outside financing with their bbox, the (*) info rows as they will appear, and the report flags.

Check, in this order (tick every point before writing `verified`):

1. **Source and statement** – the file is the data source from `roles.json` (see `[שלב A]` notes for 1829, 2559, 2520);
   the pages are the **consolidated** statement of cash flows (title `מאוחד`/`consolidated`), not the separate
   company data (38D, `נתונים על תזרימי המזומנים`, `מידע כספי נפרד`, footer `...הדוחות הכספיים הנפרדים`), not the
   board report, not an investee's statements. Flags `נבחר הדוח בעמודים ... ולא דוח קודם` / `כותרת הדוח אינה כוללת
   'מאוחד'` ask you to confirm this (Phase A checked the pick in 425, 2520, 2570, 719; `tool_scan.py` lists the
   candidates). Companies without subsidiaries: use the primary statement and say so in `report_notes`.
2. **All statement pages** – `cf_pages` must contain every page of the statement (operating, investing, financing,
   continuation pages); `fin_pages` the page(s) with financing lines; `header_page` the page whose column headers are used.
3. **Columns** – every column of the statement, in the statement's order (RTL: c1 = rightmost), none skipped/invented;
   months, end date and restated flag right. The label is generated (`3 חודשים שהסתיימו ב-31.03.2026`; Q2 3-month
   columns get ` (אפריל–יוני)`; restated columns ` (מוצג מחדש)` after it). Flags `הוסקו` / `הונח` / `דו-משמעית`
   mean the header was not fully read – confirm against the image. Restated columns: the extractor only flags pages
   that mention `הוצג מחדש`; set `"restated": true` where the column header says so.
4. **Units/currency** exactly as stated (`אלפי ש"ח`, `באלפי דולר ארה"ב`, `מיליוני ש"ח`, `אלפי אירו`, `באלפי דולר קנדי`).
5. **Every line**: verbatim text (no missing words, commas, parentheses; wrapped labels joined), every value digit by
   digit against `fin_*.png` (zoom with `tool_grid.py --clip ... --dpi 300` when in doubt), sign (parentheses →
   negative), dashes → 0. Lines must be in statement order; nothing above the heading or below the total; subtotals
   marked `subtotal`; exactly one `total` (the statement's own reported total).
6. **Mapping** of every line (§7) with a note for every non-obvious decision.
7. **(*) lines outside financing** – look at the operating and investing pages (`page_*.png`) for interest paid /
   dividends paid (incl. `מזומנים ששולמו במשך התקופה עבור: ריבית`, capitalised interest paid in investing) and at
   appendices (`נספח – ריבית ששולמה`). Receipts (`ריבית שהתקבלה`, `דיבידנד שהתקבל`) and non-cash items (`דיבידנד
   שהוכרז וטרם שולם`, `ריבית לשלם`) are **not** (*) lines. Check the extractor's candidates (`outside_k_*.png`) and add
   the ones it missed (§5 `outside_add`).
8. **C1 = 0** in every column (`lines_*.txt`). A non-zero C1 is either an extraction error (fix it) or a source
   inconsistency (keep the printed values, explain it – §9).

---------------------------------------------------------------------------------------------------------------

## 4. Override file – auto mode (the normal case)

`W\overrides\<iss>_<Q>.json` (UTF-8 JSON). Line keys are the **auto** line numbers (`key` column of `lines_*.txt`)
as strings. Values may be numbers or printed strings (`"(1,234)"`, `"-"`). Only the keys you need. The example below
is illustrative – it combines keys from several reports (5- and 3-column value lists) and `{ ... }` placeholders; in a
real file every value list has exactly one entry per column of that report and the file must be valid JSON:

```json
{
  "columns":    {"c3": {"months": 3, "end": "2026-06-30", "restated": false},
                 "c2": {"restated": true}},
  "units":      {"units_text": "אלפי ש\"ח", "currency": "ש\"ח", "units": "אלפים"},
  "line_items": {"4": 5, "6": "net_loans", "9": "other", "10": "subtotal"},
  "line_notes": {"4": "אשראי מבעלי שליטה ללא ציון תקופה, מוצג נטו – סעיף 5 (R3)"},
  "line_text":  {"2": "קבלת הלוואות מתאגידים בנקאיים ואחרים - זמן ארוך"},
  "line_values":{"2": [0, "197,252", 0, 0, "280,683"]},
  "drop_lines": [7],
  "add_lines":  [{"after": 3, "page": 34, "text": "פירעון אגרות חוב", "item": 8,
                  "values": ["(35,000)", "(56,500)", 0], "bbox": [92.0, 340.1, 536.5, 352.1],
                  "note": "השורה לא נקראה מהטקסט – הוזנה ידנית מהתמונה"}],
  "outside_drop": [2],
  "outside_add": [{"info": "interest", "section": "פעילות שוטפת", "page": 33, "text": "ריבית ששולמה",
                   "values": ["(1,679)", "(3,082)", "(11,808)"], "bbox": [79.6, 598.1, 536.6, 610.1]}],
  "outside_sections": {"2": "גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת"},
  "info_note_extra": {"interest": "הסכומים כפי שמודפסים בנספח (ללא סוגריים)"},
  "info_notes": {"dividend": "לא מוצג בנפרד בדוח תזרים המזומנים"},
  "cf_pages": [33, 34], "fin_pages": [34], "header_page": 34,
  "boxes":      {"34": {"fin": [52.0, 277.9, 541.0, 384.7], "header": [52.6, 25.5, 542.6, 172.2], "printed_page": 8}},
  "report_notes": ["..."],
  "column_notes": {"c2": "..."},
  "issues":     ["בדוח המודפס חסרה ספרה: '280,68' בשורת הנפקת אג\"ח (שנה 2025); לפי הסה\"כ ודוח Q1 – 280,683"],
  "text_layer": "usable",
  "verified":   { ... see §8 ... }
}
```

| key | meaning |
|---|---|
| `columns.cN` | set `months`, `end` (YYYY-MM-DD), `restated`, `header_text`, `audit` of column cN |
| `units` | replace units/currency |
| `line_items` | item code per line: `1`–`14`, `"other"`, `"net_loans"` (4 if ≥0 else 7, per column), `"net_bonds"` (3/8 by sign), `"net_nci"` (6 if ≥0 else 14, per column – one line netting NCI sales/issues against NCI purchases; Phase C), `"subtotal"` (not counted), `"total"`, `"text"` (no values, not counted) |
| `line_notes` | the reasoning note shown in the mapping sheet (replaces the default note) |
| `line_text` | verbatim text correction |
| `line_values` | full list of values (one per column, statement order) – use for any misread value |
| `line_pages`, `line_bbox` | page / box of a line (only for review framing) |
| `drop_lines` | auto line numbers to remove (e.g. a stray row, a heading read as a line) |
| `add_lines` | lines the extractor missed: `after` = auto line number (0 = first), `page`, `text`, `item`, `values`, optional `bbox`, `note`, `raw` |
| `outside` | **replaces** the whole list of (*) lines; or use `outside_drop` (1-based index in the **auto** extraction's (*) list, i.e. `[k]` in `lines_*.txt` before any outside override) / `outside_add` |
| (*) entry | `{"info": "interest"\|"dividend", "section": <canonical section>, "page": p, "text": "...", "values": [...], "bbox": [x0,y0,x1,y1]}` – **bbox is required** (the screenshots crop it). Blank values become 0. Optional `"sign_flipped": true` (iteration 2, decision D3): the line is printed without brackets but recorded with the payment sign – `L.star_mapping_note` then appends the sign remark (`L.STAR_SIGN_REMARK`) to its mapping note |
| (*) sections (Phase C, canonical – finalize rejects anything else) | `פעילות שוטפת` / `פעילות השקעה` (a line in the body of the statement); `גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת` / `... – נכלל בפעילות השקעה` (an amount disclosed only in an appendix, when the report states – or the appendix clearly shows – the section); `גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)` (section not stated). Constants `L.SECTION_*`, tuple `L.STAR_SECTIONS`. The extractor's generic appendix label (`L.SECTION_APPX_AUTO`) is mapped to "הסעיף לא צוין" automatically |
| `outside_sections` | `{"k": <canonical section>}` – sets the section of (*) line k (1-based in the **final** (*) list, after `outside_drop`/`outside_add`) |
| `info_note_extra` | `{"interest"\|"dividend": "..."}` – report-specific remark appended to the composed (*) note after `; ` (sign remark, restatement, source irregularity) |
| `info_notes` | only for a (*) kind **without** (*) lines (e.g. dividends paid but not shown separately: `לא מוצג בנפרד בדוח תזרים המזומנים`); when interest is not presented anywhere the default is that text. With (*) lines the note is composed from the canonical sections of the lines (joined by ` + `) and `info_notes` is rejected |
| `cf_pages`, `fin_pages`, `header_page`, `fin_heading`, `context_sections` | statement geometry (after changing `cf_pages` or `source_file`, re-run `extract_report.py` – line numbers may change) |
| `boxes` | highlight geometry in PDF points per page: `fin` = the financing section box, `header` = title+column headers+units box, `content` = `[x0, x1]` explicit x-range of a page's labels + values (for pages without a `fin` box, e.g. a page that only carries (*) lines), `printed_page` = page number printed on the page. Use when the automatic boxes are wrong (check the screenshots) |
| `report_notes` | notes of the report (company workbook notes) |
| `column_notes` | note per column (company workbook + master `הערות`) |
| `issues` | source irregularities → master `חסרים והערות` (`חריגה בדוח המקור`) |
| `text_layer` | `usable` / `usable (repaired)` / `garbled – values read from the image` / `none – manual entry` |
| `other_cf_pages` | (iteration 2, accepted in auto mode too) `{"solo": [pages], "board": [pages]}` – pages of the same file that are **not** used: separate financial information under regulation 38D (`solo`) and the board report's cash-flow tables (`board`). Shown in the `מקורות` notes and the master index notes. List only pages that really are separate information (checked on the image) |
| `consolidated` | (iteration 2) `false` for a company that has no consolidated statements (1484): the statement is then named `L.CF_NAME_SOLE` ("הדוח על תזרימי המזומנים (החברה אינה מציגה דוחות מאוחדים)") in the workbook, the captions and the cover (`L.cf_statement_name`). Omitted = consolidated |
| `zoom_blank_cells` | (iteration 2) `true` when a value cell of the financing section is printed blank (not "-"): the zoom legend then says `"-" או תא ריק בדוח = 0` |
| `source_file` | must equal the auto data's file in auto mode (to switch files use `cf_pages`+`source_file` and re-extract, or manual mode) |

After every change: `finalize_report.py` (it stops with an explicit message on a missing value, a wrong number of
values, ≠ 1 total line, a column without months/end, an unknown item code) and `tool_review.py` again.

---------------------------------------------------------------------------------------------------------------

## 5. Override file – manual mode (text layer unusable, or a statement the extractor cannot read)

Phase A found **no** report without a usable text layer (14 reports have a repaired glyph defect, see the Phase A
report). Use manual mode only when the auto data cannot be corrected sensibly. Everything comes from the override:

```json
{
  "manual": true,
  "source_file": "1484_מצלאוי חברה לבנין בע_מ_2026_Q1_1743676.pdf",
  "cf_pages": [33, 34], "fin_pages": [34], "header_page": 34,
  "units": {"units_text": "אלפי ש\"ח", "currency": "ש\"ח", "units": "אלפים"},
  "columns": [
    {"months": 3,  "end": "2026-03-31", "restated": false, "header_text": "ל-3 החודשים שהסתיימו ביום 31 במרס 2026"},
    {"months": 3,  "end": "2025-03-31", "restated": false, "header_text": "ל-3 החודשים שהסתיימו ביום 31 במרס 2025"},
    {"months": 12, "end": "2025-12-31", "restated": false, "header_text": "לשנה שהסתיימה ביום 31 בדצמבר 2025"}
  ],
  "lines": [
    {"text": "פרעון התחייבות בגין חכירה", "item": 10, "page": 34, "values": ["(488)", "(592)", "(611)"],
     "bbox": [92.2, 305.9, 536.6, 317.9]},
    {"text": "פירעון אגרות חוב", "item": 8, "page": 34, "values": ["(34,210)", "(13,662)", "(13,213)"]},
    {"text": "פירעון הלוואות לזמן ארוך", "item": 7, "page": 34, "values": ["(33,362)", "(5,917)", "23,659"],
     "note": "בעמודת 2025 מודפס סכום חיובי בשורת פירעון – כמודפס"},
    {"text": "עליה באשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו", "item": 5, "page": 34,
     "values": ["63,971", "35,788", "53,346"]},
    {"text": "מזומנים נטו שנבעו מפעילות מימון", "item": "total", "page": 34, "values": ["(4,089)", "15,617", "63,181"]}
  ],
  "outside": [{"info": "interest", "section": "פעילות שוטפת", "page": 33, "text": "ריבית ששולמה",
               "values": ["(1,679)", "(3,082)", "(11,808)"], "bbox": [79.6, 598.1, 536.6, 610.1]}],
  "boxes": {"33": {"header": [52.6, 25.5, 542.6, 173.1], "printed_page": 7},
            "34": {"fin": [51.6, 277.9, 543.6, 384.7], "header": [52.6, 25.5, 542.6, 172.2], "printed_page": 8}},
  "context_sections": {"33": ["פעילות שוטפת"], "34": ["פעילות השקעה"]},
  "text_layer": "none – values entered manually from 200-DPI renders",
  "verified": { ... }
}
```

Rules: `columns` and every `values` list in statement order; one `total` line; `boxes` must give `fin` for every
`fin_pages` page and `header` for `header_page` (the screenshots need both); a `bbox` for every (*) line; line
`bbox` is optional (only for the review frames). Phase A tested this path end to end: `tool_selftest.py <iss> <Q>`
builds a manual copy of a report from its auto data and checks that items, totals, geometry and the rendered outputs
match (passes on 1484 Q1, 2384 Q2, 1618 Q2); it writes only to `%TEMP%\fcf_run\_runs\selftest_*`.

**Reading boxes:** `tool_grid.py <iss> <Q> <page>` (whole page) or `--clip y0 y1 --dpi 250` (a band). Red labels =
x, blue labels = y, in PDF points from the top-left corner. `fin` box: from just above the financing heading to just
below the total line, x across the full width of labels + all value columns. `header` box: from the top of the page
title (company name) to the bottom of the column headers/units line. Check the result in the screenshots (§10).

---------------------------------------------------------------------------------------------------------------

## 6. Typical corrections (seen in Phase A)

* **Wrong statement picked** → `"cf_pages": [...]` (+ `"fin_pages"`, `"header_page"`) and re-run `extract_report.py`.
* **Value misread / source typo** → `line_values`, plus a `line_notes` or `issues` entry when the printed value is
  itself defective (531 Q2 prints `280,68`). Keep printed values; do not "repair" source arithmetic – explain C1.
* **Comma misplaced by the text layer** (`'1,3805'` flag `מספר בפורמט חריג`): the value is usually right – confirm on
  the image.
* **Mirrored / repaired glyphs**: labels of the 14 `usable (repaired)` reports were rebuilt from a broken font
  (`ð`/`ª`/U+F8FF = `נ`); compare every label with the image and fix with `line_text`.
* **Inferred column periods** (`הוסקו`, `הונח`): confirm; fix with `columns`.
* **Empty cells set to 0** (`תא ריק – נרשם 0 (לאמת)`): confirm the cell is really `-`/blank.
* **Value row without label** / stray `-` row (2418 Q1): `drop_lines` (after confirming it carries no amount).
* **2533**: the column headers print `30 במרס`; decide (keep as printed – C2 then N/A – or 31.03 with a
  `column_notes` explanation) and document.

---------------------------------------------------------------------------------------------------------------

## 7. Mapping conventions (R3 + pilot decisions)

Items (exact labels are generated): 1 הנפקת מניות · 2 מימוש אופציות/כתבי אופציה · 3 הנפקת אג"ח · 4 קבלת הלוואות לזמן
ארוך · 5 אשראי לזמן קצר מתאגידים בנקאיים, נטו · 6 השקעת בעלי זכויות שאינן מקנות שליטה · 7 פירעון הלוואות לזמן ארוך ·
8 פירעון אג"ח · 9 רכישה עצמית של מניות · 10 פירעון קרן התחייבויות בגין חכירה · 11 דיבידנד לבעלי המניות (*) ·
12 דיבידנד לזכויות שאינן מקנות שליטה · 13 ריבית ששולמה (*) · 14 רכישת זכויות נוספות בחברה בת · `אחר`.

The extractor's item is a **suggestion**; you decide. Rules, with examples from these reports:

| original line (examples) | item | note |
|---|---|---|
| `קבלת הלוואות לזמן ארוך מתאגידים בנקאיים ואחרים` / `פרעון ...` | 4 / 7 | any lender (banks, institutions, controlling shareholder, related parties, partners); note "כולל ... אחרים" |
| `קבלת (פירעון) הלוואות לזמן ארוך, נטו` (same LT instrument, netted) | `net_loans` | 4 if positive, 7 if negative, per column; note it |
| `הנפקת (פדיון) אגרות חוב, נטו` | `net_bonds` | 3 / 8 by sign |
| one line netting NCI transactions (sale/issue to NCI vs purchase from NCI), mixed signs across columns | `net_nci` | 6 / 14 by sign, per column (Phase C: 434) |
| `אשראי לזמן קצר מתאגידים בנקאיים ואחרים, נטו`; gross ST receipt and repayment lines | 5 | all ST credit, banks and others, net or gross |
| borrowing line **net without a stated term**: `קבלת (פירעון) הלוואות מתאגידים בנקאיים, נטו`, `הלוואות מבעלי שליטה, נטו`, `שינוי בהלוואות לבעלי שליטה`, `קיטון בהלוואה מהחברה האם` | 5 | R3: "any borrowing line presented net with no stated term". `נטו` meaning *net of raising costs* with the repayments on a separate line is a gross receipt (4) – Phase C rule B (1722, 2533) |
| **gross** receipt / repayment lines **without a stated term** | 5 or 4/7 | Phase C rule A: decide by the reporting company's balance sheet and notes – the lender's balance is current short-term credit only → 5; long-term loans (incl. current maturities, project finance classified long-term) → 4/7; mixed or not attributable → 4/7 with a note. Put the evidence (balance-sheet line, page) in the line note; same line in Q1 and Q2 → same item |
| loans from controlling shareholder / related parties / partners with a term | 4 / 7 (5 if short-term) | |
| `הנפקת מניות (בניכוי הוצאות הנפקה)`, `הנפקת הון`, `תקבולים על חשבון מניות`, share-issue costs | 1 | costs netted in 1 (negative) |
| partnership / reporting entity's owners: `השקעות בעלים`, `הון שותפים`; distributions `חלוקות לבעלים`, `משיכות שותפים` | 1 / 11 | if the owners are the reporting entity's partners; NCI holders → 6 / 12 |
| `מימוש אופציות`, `כתבי אופציה` | 2 | `הנפקת חבילה` (shares + warrants) not split in the statement → 1 with a note |
| bonds incl. series expansion, convertibles; `נע"מ` | 3 / 8 | write "נע"מ" in the note for commercial paper |
| `רכישת מניות באוצר`, `רכישה עצמית` (also a subsidiary buying parent shares) | 9 | |
| `פרעון התחייבויות בגין חכירה` (no principal/interest split) | 10 | note "ללא פיצול קרן/ריבית – סעיף 10"; a separate lease-interest line → 13 |
| `דיבידנד לבעלי המניות` / `דיבידנד ששולם` | 11 | |
| `דיבידנד לבעלי זכויות שאינן מקנות שליטה`, NCI withdrawals | 12 | `זשמ"ש` = זכויות שאינן מקנות שליטה |
| `ריבית ששולמה` (in financing), `עמלות וריביות ששולמו` | 13 | note when fees are included |
| `הנפקה לבעלי זכויות שאינן מקנות שליטה`, `השקעת זשמ"ש`, `הקצאת מניות בחברה בת` to outsiders, sale of subsidiary shares without loss of control | 6 | |
| `רכישה מבעלי זכויות שאינן מקנות שליטה`, purchase of additional shares in a controlled subsidiary | 14 | equity transaction |
| derivatives / hedge settlements (`תמורה מנגזרים`), contingent consideration (`תשלום תמורה מותנית`), restricted deposits, grants, merger-related flows | `other` | always with the verbatim text and a note |
| subtotal lines inside the section (`סה"כ ...` that is not the section total) | `subtotal` | never counted twice |

Consistency rules: the **same line in Q1 and Q2 gets the same item** (C3 compares FY-2025 per item – Phase A found item
differences in 1722, 1829, 2386, 2474, 2478, 2559 that must be aligned or explained); no plug values; `אחר` only when
nothing else fits; every non-obvious decision has a note (Hebrew). Decisions that may need consistency across batches
(e.g. EB-5 investor loans in 1622, advances from a parent `מקדמות`, capital notes `שטרי הון`, `הנפקת ניירות ערך` without
a split): decide by economic nature and list them in your batch report under "mapping decisions" so Phase C can align.

---------------------------------------------------------------------------------------------------------------

## 8. Verification record

Only after every point of §3 is checked against the image (not against the text layer alone):

```json
"verified": {
  "status": "verified",
  "date": "2026-11-10",
  "by": "Phase B batch 3 Builder",
  "method": "Every line text, every value (5 columns x 9 lines + total), the column headers, the units and the (*) lines compared digit by digit with 220-DPI renders (tool_review fin/page images) of PDF pages 55-56; C1 = 0 in every column.",
  "pages_viewed": [55, 56],
  "text_layer": "usable"
}
```

`status` must be exactly `verified`. `text_layer`: `usable` / `usable (repaired)` / `garbled – values read from the
image` / `none – manual entry`. Do not mark a report verified when a value is still uncertain – leave it unverified
and report it.

Later rounds append to the record instead of rewriting it: `verified.phaseC` (Phase C) and `verified.iteration2`
(iteration 2) are lists of `{date, by, changes, why, images_seen}` entries; the batch fields stay untouched.

---------------------------------------------------------------------------------------------------------------

## 9. Check explanations (C1/C2/C3)

`W\overrides\<iss>_checks.json` – one entry per genuine difference (restatement, reclassification, source rounding,
source typo). Fix extraction errors instead of explaining them.

```json
{
  "_doc": "Explanations of C1/C2/C3 differences for issuer 2533",
  "C1|2533|Q1 2026|שנה שהסתיימה ב-31.12.2025|total": "בדוח המודפס סכום השורות בעמודת 2025 (268,919-) שונה מהסה\"כ המדווח (267,919-) ב-1,000; הנתונים נרשמו כפי שדווחו (גם בדוח Q2).",
  "C2|1484|3 חודשים שהסתיימו ב-31.03.2025|total": "...",
  "C2-item|1484|3 חודשים שהסתיימו ב-31.03.2025|5": "...",
  "C3|2474|שנה שהסתיימה ב-31.12.2025|4": "..."
}
```

Key = `<check>|<issuer>|<period>|<key>`; for C1 also `C1|<issuer>|<report>|<period>|total` (report = `Q1 2026` /
`Q2 2026`; preferred, because the FY-2025 label exists in both reports). `<period>`: C1 = the column label (with
` (אפריל–יוני)` / ` (מוצג מחדש)` if present); C2 = `3 חודשים שהסתיימו ב-31.03.2026` or `...31.03.2025`; C3 =
`שנה שהסתיימה ב-31.12.2025`. `<key>` = `total`, `1`–`14` or `other`. Copy the exact strings from
`TEMP\_runs\checks_*\checks_result.json` (`check`, `issuer`, `report`, `period`, `key`). MISMATCH rows must all be
explained (or fixed); C2-item rows are informational – explain them briefly when you can (they are listed in the master
`חסרים והערות`). `checks.py --issuers <iss>` must end with `unexplained mismatches: 0`.

---------------------------------------------------------------------------------------------------------------

## 10. Rebuild one company and check it

```powershell
$env:PYTHONIOENCODING = 'utf-8'; $env:PYTHONDONTWRITEBYTECODE = '1'
$W = Join-Path (Get-Location) '.goals\financing-cashflow-breakdown-2026\work'
python "$W\finalize_report.py" 1484 Q1; python "$W\finalize_report.py" 1484 Q2
python "$W\checks.py" --issuers 1484
python "$W\build_company.py" 1484                 # no --draft once both reports are verified
python "$W\tool_shots.py" 1484 70                 # then view TEMP\1484\shots_<hhmmss>\s*.png
python "$W\validate.py" --issuers 1484 --no-master
```

Look at the screenshots: every page has a caption; the orange box covers the whole financing section (heading to
total) and the blue box the title/headers/units; the zoomed page shows the header strip and every financing line
legibly; (*) crops (red) exist for every (*) line. `validate.py --issuers <iss> --no-master` must print `FAIL 0`
(it re-reads the workbook and the PDF and compares them with the final data, re-runs C1–C3, checks names, labels, T2,
verification records, the hashes of all 178 source PDFs, that the company's two output files exist, and the hygiene of
the whole WORKSPACE – a stray file of another batch would also show up here: report it, do not delete it). A company
with an unverified report can only be built with `--draft` (marked `טיוטה`) – that is not a deliverable.

---------------------------------------------------------------------------------------------------------------

## 11. Temp hygiene

* Everything bulky goes to `%TEMP%\fcf_run\<iss>\...` (helpers do this) – never into WORKSPACE or GOAL DIR.
* At the end of your batch delete `%TEMP%\fcf_run\<iss>\` for each of your issuers (not `_runs`, not other issuers'
  folders – other batches are running). Phase C cleans `_runs`.
* No `__pycache__`, no `~$*` lock files, no logs or scratch files anywhere in WORKSPACE; your own exploration
  scripts go to `%TEMP%\fcf_run\<iss>\`.
* `python "$W\tool_integrity.py"` (read-only) reports baseline hashes, unexpected new files and forbidden artefacts.

---------------------------------------------------------------------------------------------------------------

## 12. Reporting a script problem (`SCRIPT-ISSUE`)

Do not edit scripts. Work around the problem with the override (manual values, `line_values`, `boxes`, manual mode)
when possible, and add to your batch report:

```
SCRIPT-ISSUE <n>
  script:     fcf_render.py (build_company.py 2503)
  report:     2503 Q2
  symptom:    <what happens; exact error message / wrong output; path of the evidence in TEMP>
  expected:   <what should happen>
  workaround: <what you did in the override, or "none – company left as draft">
  severity:   blocks the deliverable | cosmetic
```

---------------------------------------------------------------------------------------------------------------

## 13. Batch report (per company)

For each company: reports and source files used (pages), columns, units/currency, mapping decisions (non-obvious ones
with reasons), (*) treatment, overrides made (what and why), C1/C2/C3 results and explanations, issues in the source,
verification method, `validate.py --issuers <iss> --no-master` result (PASS/FAIL counts), and any `SCRIPT-ISSUE`.
End with the list of your issuers and their final status (verified + built / blocked + reason).

---------------------------------------------------------------------------------------------------------------

## 14. Phase C changes (assembly, iteration 1)

Script behaviour added in Phase C (all generic; the data changes went through overrides only):

* **`finalize_report.py`** – item code `net_nci` (6 if ≥ 0 else 14, per column); canonical (*) sections only
  (`L.STAR_SECTIONS`; the extractor's generic appendix label `L.SECTION_APPX_AUTO` → "הסעיף לא צוין"); new keys
  `outside_sections` and `info_note_extra` (§4); the (*) note is composed from the sections of the (*) lines (joined
  by ` + `) plus the extra remark; `info_notes` is rejected for a kind that has (*) lines; blank (*) values → 0.
* **Verification record** – every report changed in Phase C has `verified.phaseC`: a list of
  `{date, by, changes, why, images_seen}` entries appended to the batch's record (the batch fields are untouched).
* **`fcf_render.py`** – every zoom and every red (*) crop shows the period headers **and** the units line: the header
  strip is extended down to the units line, or a units part is composed from the same page / another statement page
  (`zoom_header_parts`, `star_crop_plan`, dashed separator between composed parts). Captions are exact per page:
  a page with (*) lines lists them (verbatim text + canonical section) and names the image that enlarges them; an
  operating/investing page without (*) lines says so and points to the pages/images that hold them; a page with
  neither financing nor (*) lines is captioned "לידיעה". `crop_texts()` returns the text inside every header clip
  (used by validate).
* **`validate.py`** – AC6 C1: a non-zero check column passes only when `checks.py` has its documented explanation
  (printed as `INFO ... (explained)`); an unexplained one fails. AC10: the zoom header and every (*) crop contain
  periods and units (text inside the clip regions). AC7: every (*) line has a canonical section, numeric values and
  a bbox. Output header `PASS n  FAIL n  INFO n`.
* **`build_company.py` / `build_master.py`** – `net_nci` shown as `6/14`; (*) mapping note via `L.star_mapping_note`;
  master `הסבר` rows for net NCI lines, loans without a stated term (rules A/B), the uniform (*) note wording, the (*)
  sign rule, the restated rule and the check rule; `חסרים והערות` lists every non-zero check column (`בדיקה לא אפס`)
  with its explanation.
* **`tool_selftest.py`** – part 2b covers `net_nci`, `outside_sections`, `info_note_extra` and the two rejections.

---------------------------------------------------------------------------------------------------------------

## 15. Iteration 2 changes (inspector-feedback-1.md M1–M10, S1–S10)

All data changes went through overrides + `finalize_report.py` (no `extract_report.py` re-run); every report's record
has a `verified.iteration2` entry. Script changes (all generic):

* **`fcf_lib.py`** – `STAR_SIGN_REMARK` + `star_mapping_note` appends the D3 sign remark for a (*) entry with
  `"sign_flipped": true` (M5); `CF_NAME_CONS` / `CF_NAME_SOLE` / `cf_statement_name(d)` name the statement per report
  (M10).
* **`finalize_report.py`** – accepts `other_cf_pages` in auto mode (validated `{"solo": [int], "board": [int]}`, M8);
  writes `consolidated` (M10) and `zoom_blank_cells` (S7f) only when the override sets them (§4 table).
* **`build_company.py`** – S4: when the dividend (or interest) is presented in financing in only some reports, the
  (*) note gets `דוח Qn 2026: אין סכומים מחוץ לפעילות מימון (… מוצג בדוח בפעילות מימון)` per report; M10: the `סימון`
  row, the `מקורות` notes/header and the `מיפוי שורות` block titles use `L.cf_statement_name`.
* **`build_master.py`** – `הסבר`: `מקור` row names the non-consolidated case (1484); rule label `כלל A`; new row
  `הכרעות D1–D3` (orchestrator decisions); index header `עמודי הדוח (המאוחד) על תזרימי המזומנים` (M10).
* **`fcf_render.py`** (S7; DPI 150/220/120 and PNG/PNG/JPEG-88 unchanged, amendment 2):
  - crop edges are snapped off text rows (`snap_edge`: a row crossed by an edge – or touched by its glyphs – stays
    inside when its centre is inside, else outside; the edge goes to the least-inked pixel row between the rows);
  - zoom and (*) crops are framed **in a white margin** around the crop (`framed`, `hpad`) – a frame never covers
    text; a contiguous zoom (header strip directly above the financing section) is cut at the row gap into a
    blue-framed header part and an orange-framed financing part, without a separator (S7a);
  - each (*) line is cut at the quiet pixel rows between it and its neighbours (`row_gap_ys`) and framed red (S7b);
  - (*) lines are red-framed on full pages and context pages too, the frame lines centred on the row gaps; the
    full-page orange/blue frame lines are placed off the glyphs (`clear_band`, `glyph_profile` – printed rules do not
    count); a full-page blue frame whose vertical edge would cross a heading printed beside the units line ends above
    that row (`box_off_crossing_rows`), and the legend then says the units are in the zoom strip;
  - a header top edge through a logo/icon shows the graphic whole or leaves it out (`graphic_top`,
    `snap_header_rect`, `widen_for_graphic`: the header part is widened and every part of that image follows, so the
    columns stay aligned);
  - captions: the dashed-line remark only when a dashed line is drawn (S7c); blank cells in the zoom legend (S7f);
    the statement name per report (M10); the full-page caption states "(*) = 0" when the financing page also carries
    operating/investing sections (`context_sections` of the financing page, S7e).
* **`validate.py`** (S9) – `master_checks` is key-based: `נתונים` by (issuer, report, period label), all fields
  compared (amounts, both (*) amounts and notes, check, file, pages, months, end, primary flag (T1), currency, units,
  restated, notes, screenshot path); `מיפוי שורות` row by row by key; with `--issuers` only those issuers' master rows
  are checked (row-count checks only on full runs); the console prints `unexplained mismatches: N`.
* **`tool_selftest.py`** – part 2c covers `other_cf_pages` in auto mode (and the rejection of a malformed one),
  `consolidated: false`, `zoom_blank_cells` and `sign_flipped`.
