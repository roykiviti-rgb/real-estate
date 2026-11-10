# Phase B — cross-batch conventions (set by the orchestrator, 2026-11-10)

All 8 batch Builders work in parallel. These rules close the open points that Phase A listed, so every
batch decides the same way. They come from `goal.md` R3–R5 and the amendments, and they **add to**
`PIPELINE.md` §7; they do not replace it.

When a case is not covered here or in PIPELINE §7:
1. Decide by economic nature (R3).
2. Write a Hebrew note on the line.
3. List the case under "mapping decisions" in your batch report. Phase C aligns these across batches.

## 1. (\*) amounts disclosed only in an appendix (נספח) to the consolidated cash-flow statement

- These amounts go in the (\*) info row (R5), for every period column, with values and sign **as
  printed**. Like every (\*) line, each needs a box so it gets a red crop.
- Note text:
  - When the report states (or the statement clearly shows) the section where the amount is
    included, name that section: `גילוי בנספח לדוח תזרימי המזומנים – נכלל בפעילות שוטפת` or
    `... – נכלל בפעילות השקעה`.
  - Otherwise use: `גילוי בנספח לדוח תזרימי המזומנים – הסעיף לא צוין (לא בפעילות מימון)`.
- These are **not** (\*) lines: receipts (`ריבית שהתקבלה`, `דיבידנד שהתקבל`) and non-cash items
  (`דיבידנד שהוכרז וטרם שולם`, `ריבית שהוונה` without a cash payment).

## 2. Owners and partners of the reporting entity (e.g. 2503 לנטרה קנדה, 2533 אל עד יו אס)

- Contributions or investments by the reporting entity's own partners or owners
  (`השקעות בעלים`, `הון שותפים`) → item **1**.
- Distributions or withdrawals to them → item **11**.
- The same flows with partners or holders in **subsidiaries** (NCI) → items **6** and **12**.

## 3. EB-5 investor loans (e.g. 1622 אקסטל)

Receipts → **4**; repayments → **7**. These are long-term loans from other lenders. Use the note
`הלוואות EB-5`. They do not go to `אחר`.

## 4. Capital notes (שטרי הון)

| Case | Item |
|---|---|
| Issued by the reporting entity to its owners or controlling shareholder | 1 |
| Issued by a subsidiary to NCI holders | 6 |
| Classified as a liability with a repayment term | 4 / 7 |
| Classified as a liability and presented net without a term | 5 |

Repayments: decide by economic nature, write a note, and list the case under "mapping decisions".

## 5. Advances and current accounts from a parent, controlling shareholder or related party

When presented net without a stated term (`מקדמות`, `חשבון שוטף`, `שינוי ביתרת ...`) → **5**. R3
treats any borrowing line presented net with no stated term this way.

## 6. Unsplit issuance of securities (`הנפקת ניירות ערך`, `הנפקת יחידות`, `הנפקת חבילה`)

- Shares plus options or warrants → **1**, with a note.
- A package that includes bonds and is not split in the statement → the item of the dominant
  instrument, according to the report's notes, with a note.

## 7. Lines that go to `אחר` (verbatim text and a note on each)

- derivative or hedge settlements;
- restricted or pledged deposits and restricted-cash movements;
- contingent consideration;
- government grants;
- transaction costs not tied to a specific instrument;
- any other line that fits none of items 1–14.

## 8. Same line in Q1 and Q2 → same item

C3 compares FY-2025 item by item. Align the mapping of every C3 item difference that Phase A flagged
(1722, 1829, 2386, 2474, 2478, 2559, 531, 2418). Explain a difference in `<iss>_checks.json` only when
the two reports themselves present the FY-2025 amounts on different lines.

## 9. Source defects

Keep the printed values and document every defect: in the override (`issues` / `line_notes` /
`column_notes`) and in the batch report.

- **A missing or garbled digit** (e.g. 531 Q2 prints `280,68`): record the value confirmed by the
  report's own arithmetic and by the identical period in the other report. Document it:
  `הערך המודפס פגום: '280,68'; נרשם <value> לפי ...`.
- **Columns misaligned in the source** (e.g. the FY column of 2418 Q1 is shifted one row): assign each
  value to its correct line using the statement's arithmetic and the Q2 report's FY-2025 column, and
  document how.
- **A typo in a header date** (e.g. 2533 prints `30 במרס`):
  - Check the cover page, the balance sheet and the other statements.
  - If the period ends 31.03.2026 everywhere else, use 31.03 for the period, and add a column note
    quoting the printed header. This lets C2 run.
  - If the whole report uses 30.03, keep it as printed.
- **A printed total that differs from the sum of the printed lines** (719 Q1, 2483 Q2, 2533 FY, ±1
  rounding): keep the printed values and explain C1.

## 10. Restated columns

Use `(מוצג מחדש)` only when the column header itself, or a note attached to that column, says the
column is restated or reclassified. If only a general note mentions a restatement, add a column note
instead.

## 11. Tools

- Do **not** use `tool_excel_check.ps1` (Excel COM) in Phase B. Phase C runs the Excel-level checks
  once for all companies, and parallel Excel instances can interfere with each other.
- Use `validate.py --issuers <iss> --no-master`.
