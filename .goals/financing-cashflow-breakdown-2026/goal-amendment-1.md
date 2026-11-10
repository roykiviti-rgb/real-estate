# Goal amendment 1 — pilot approved with three tweaks (2026-11-10)

This amendment is authoritative where it differs from `goal.md` (which stays unchanged).

## User decision

On 2026-11-10 the user was asked for comments on the pilot (1618 קבוצת אשטרום, Q1 + Q2 2026: company
workbook, screenshots PDF, master workbook in pilot mode). The user selected (verbatim):

> Approve with the suggested tweaks — don't start yet, I'll write תתחיל (Recommended)

The full run starts only after the user writes `תתחיל`.

## A1 — The pilot is the approved reference design

Unless T1–T3 below change it, the full run keeps the pilot's design exactly:

- the company workbook: sheets, header block, the source rows under each column header, item rows,
  check row, the two (\*) info rows, notes column, general notes, and the mapping/sources sheets;
- how numbers look: payments are negative numbers with a minus sign, and zero is shown as `0`;
- how the screenshots PDF is built: a cover page, then for each report:
  - the full page with the financing section and the column headers/units highlighted;
  - a zoomed crop of the header strip plus the financing section, with any omitted section in
    between marked by a dashed line;
  - the other pages of the consolidated cash-flow statement as context, including the operating
    page, which proves whether the (\*) info rows are 0;
- the mapping conventions:
  - "from banks and others" credit lines go to items 4/5/7, with a note;
  - a lease-repayment line that doesn't split principal and interest goes to item 10, with a note;
- item-level differences between reports (like the 1,267 in Ashtrom) are recorded as notes
  ("לידיעה"), in addition to the C2/C3 checks the goal requires.

## T1 — "Primary period" flag in the master workbook

Add a column `תקופה עיקרית` (values `כן` / `לא`) to the master sheet `נתונים`. Within a company, a
period may be presented in more than one report; a period is identified by its number of months plus
its period-end date. For such a period:

- the row from the latest report (Q2 2026) is `כן`;
- the rows from the other reports are `לא` (typically the FY-2025 column of the Q1 report).

Every other row is `כן`. Filtering on `כן` returns each company × period exactly once. Explain the
column in sheet `הסבר`.

## T2 — Month range in the labels of quarterly 3-month columns

A 3-month column that is not the year-to-date period gets the month range as a suffix. For
calendar-year companies these are the 3-month columns ending 30.06, for example
`3 חודשים שהסתיימו ב-30.06.2026 (אפריל–יוני)`. Apply it in:

- the column headers of the company workbook;
- the mapping sheets;
- the master workbook (`נתונים`, `מיפוי שורות`).

If a column is also restated, `(מוצג מחדש)` comes after the month range.

## T3 — Smaller screenshots PDFs

Compress the images embedded in each company's screenshots PDF. The pilot is about 2.5 MB per
company; aim for about 1 MB or less per company where possible. Two things must not be sacrificed:

- the R7 minimum resolutions: ≥ 110 DPI for full-page renders and ≥ 200 DPI for zoomed crops;
- legibility: every digit stays crisp and readable. If size and legibility conflict, legibility
  wins.

## Effect on the pilot outputs

The full run regenerates Ashtrom's outputs (company workbook, screenshots PDF, master rows) with
T1–T3, together with all other companies.
