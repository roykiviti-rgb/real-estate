# Batch 4 — progress checkpoint (Phase B, iteration 1)

Issuers (exclusive): 111 (Q2 only), 400, 539, 1083, 1502, 1553, 1622, 2481, 2483, 2488, 2524.

Resume rule: a fresh agent reads this file and continues from "Next". All 21 reports are verified (records in
`overrides\<iss>_<Q>.json`), all 11 companies are built as final outputs (no draft). Do not redo verified work.

## Status per report (11:29)

| issuer | Q1 | Q2 | checks (all issuers: unexplained 0) | final build | shots viewed | validate --no-master |
|---|---|---|---|---|---|---|
| 111 | n/a (missing) | verified | C1 OK | built 11:26 | yes | PASS 137 / FAIL 0 |
| 400 | verified | verified | C1/C2/C3 OK | built 11:26 | yes | PASS 323 / FAIL 0 |
| 539 | verified | verified | C2 3M-2025 −1 explained | built 11:26 | yes | PASS 332 / FAIL 0 |
| 1083 | verified | verified | C1/C2/C3 OK | built 11:26 | yes | PASS 328 / FAIL 0 |
| 1502 | verified | verified | C1/C2/C3 OK | built 11:26 | yes | PASS 313 / FAIL 0 |
| 1553 | verified | verified | C1/C2/C3 OK | built 11:26 | yes | PASS 325 / FAIL 0 |
| 1622 | verified | verified | C1/C2/C3 OK | built 11:26 | yes | PASS 339 / FAIL 0 |
| 2481 | verified | verified | C1/C2/C3 OK | built 11:26 | yes | PASS 332 / FAIL 0 |
| 2483 | verified | verified | C1 Q2 3M-2026 +5 (source) explained; C2 3M-2025 −1 explained | built 11:26 | yes | PASS 330 / FAIL 1 = SCRIPT-ISSUE 1 (validate AC6 per-column ignores explanations) |
| 2488 | verified | verified | C2 3M-2025 −2 explained | built 11:26 | yes | PASS 325 / FAIL 0 |
| 2524 | verified | verified | C2 3M-2026 +1 explained | built 11:26 | yes | PASS 324 / FAIL 0 |

## VISUAL-VERIFICATION HISTORY (important – orchestrator alert at ≈11:15)

The `view` tool silently stops showing images after ~50 images ("maximum number of images (50)"). Strict audit of my
own tool results:
- NOT displayed (not relied on): every image I viewed from the start up to and including 1553 shots s3/s4 (≈10:41) –
  all images of 111, 400, 539, 1083 (fin, pages, grids, shots), 1502 (fin, pages, shots), 1553 fin/page_*/s3/s4.
  Earlier log lines "shots viewed" / "RE-VERIFIED VISUALLY at 10:30-10:35" / "displayed again from 1083 shots s3"
  were WRONG – corrected here.
- DISPLAYED: 1553 shots s2, s6, s7, s8 (≈10:41); 1622 Q1+Q2 fin, pages 51/52/56/57/58, p.67, p.85, shots s2/s3/s5/s6
  (10:42–10:47); 2481 Q1+Q2 fin + pages 35/36/38/40/41 (10:48–10:52).
- Independent read-only sub-agents (11:05–11:12, 9 agents, each listed images actually seen, NOT SEEN = none):
  all 21 reports PASS, except 1622 Q1 line-10 label spacing ('מ-Extell', no space) → fixed by line_text.
- Builder re-check on DISPLAYED composite images (compose.py → %TEMP%\fcf_run\111\b4\comp_*.png), every digit /
  label / header / unit / (*) line: 111 Q2 (11:17); 400 Q1, 400 Q2, 539 Q1, 539 Q2 (11:19–11:20); 1083 Q1 (*) crops +
  1622 Q1 line-10 label (11:20); 2483 Q1+Q2, 2488 Q1+Q2, 2524 Q1+Q2 (11:20–11:21); 1083 Q2 fin + both (*) (11:21);
  1083 Q1 fin + 1553 Q1 fin + (*) (11:22); 1502 Q1+Q2 fin + (*) (11:22); final screenshot pages 1083 p5 / 539 p2 /
  2483 p6 (11:28). All matched – no data change needed.
- Text-layer scan of every statement page for interest/dividend rows (star_scan): every paid row is recorded either in
  financing (11/12/13) or as a (*) line; only receipts and non-cash items excluded.
- The `verified.method` of every report states exactly which displayed images it rests on.

## Log

- 10:15 start (fresh agent). 10:14 tool_batch review of all 21 reports.
- 10:18–10:48 first pass over 111, 400, 539, 1083, 1502, 1553, 1622 (overrides, mapping, checks, builds) – image views
  of 111…1553 were NOT displayed (see above).
- 10:48–10:58 2481 (displayed), 2483 / 2488 / 2524 overrides from text layer + mapping evidence; clean header_text for
  all 21 reports (workbook row 'כותרת העמודה בדוח (מילולית)').
- 11:00 finalize all; checks: explanations 2483/2488/2524 (+539); 11:01 draft build + review packages.
- 11:05–11:12 9 sub-agent visual checks → all PASS (1622 Q1 label fix).
- 11:13–11:16 note fixes (1083 'ב)' item wording, 2481 note quote, 2483 'בגבאי במניבים', 1553 lease note), verified
  records restored/added with exact method text.
- 11:15 orchestrator alert → 11:17–11:22 composite re-checks (all OK) → methods corrected.
- 11:26 finalize all (21 VERIFIED), checks unexplained 0, final build (no --draft) 11/11, shots rendered,
  validate per issuer: 10 × FAIL 0; 2483 FAIL 1 (SCRIPT-ISSUE 1). No draft markers in any output (text scan).
- 11:29 539 logo geometry confirmed from PDF vectors (logo x 57.3–160, y 31–53.5; auto box x0 61.3 / y0 38.7 on Q1).

## Next

- NOTHING LEFT – batch 4 complete (11:36). Report written: `batches\batch-4.md`. Temp folders %TEMP%\fcf_run\<iss>\ of
  the 11 issuers deleted (11:35; `_runs` and other batches' folders untouched). Final state: 21/21 reports verified,
  11/11 companies built (final, no draft), validate FAIL 0 for 10 companies; 2483 FAIL 1 = SCRIPT-ISSUE 1
  (validate.py per-column AC6 ignores the documented C1 explanation of the source's 5-unit difference).

## Key facts / decisions (for the report)

- 111 Q2: c2 restated=true ('*' values + footnote '* סיווג לא מהותי במספרי השוואה'); loans 'מאחרים' gross → 5 (balance
  sheet 'הלוואות לזמן קצר'); 'פירעון הלוואה מצד קשור' → 7 (78-month shareholder loan prepaid, note 3א); (*) interest (181).
- 400: straightforward; (*) interest in operating; bond lines 'נטו' = net of issue costs → 3 / 8.
- 539: 'הנפקת חבילה' → 1 (conv §6); 'הנפקת מניות' → 2 (all option/warrant exercises per equity statement); header
  box widened (logo); C2 3M-2025 −1 rounding (item 5).
- 1083: second (*) interest line 'ב) ריבית ששולמה והוונה למלאי' (printed positive, recorded negative, like 121).
- 1502: Q1 financing = heading line '-' only (total 0); Q2 one line all '-'; (*) interest '-' (note set).
- 1553: project loans net (current) → 5; LT bank loans net → net_loans (→7); lease label 'יפרעון' → 'פירעון'.
- 1622: owner equity 1; NCI 6; NCI capital returns 12; fin.-inst. loans 4/7; controlling-holder loans (current, no
  term) 5; Extell Holdings I LLC loan (note 7ט due 2033) 4; its advances (net) 5; EB-5 payments 7; derivatives other.
- 2481: ST bank/others net 5; 'מבעל עניין לזמן קצר' 5; 'פירעון הלוואות מבעלי עניין' 7; related-party LT repayments 7;
  note 2 restatement does not mark cash-flow columns (column note, not restated).
- 2483: 'רכישת מניות חברה מאוחדת מבעל השליטה' → 14; 'פירעון הלוואות מבעלי שליטה, נטו' → 5; Q2 3M-2026 C1 +5 source
  inconsistency (short-term credit printed (18,489); by Q1 it should be (18,494)); issues entry + column note + C1 expl.
- 2488: 'קבלת/פרעון הלוואות מתאגידים בנקאיים ואחרים' (no term, ST shown separately) → 4/7; related-party loans net → 5.
- 2524: 'שינוי בבעלי עניין' → other (balance sheet shows interested parties as ASSETS only); 'שינוי בהלוואה מאחרים'
  (net, no term) → 5; 'השקעות מהזשמ"ש' → 6.
