# Batch 2 — progress checkpoint (Phase B)

Builder: Phase B batch 2 of 8 (resume from here if restarted; do not redo verified work).
Issuers: 121, 155, 715, 1331 (Q2 only), 1644, 1722, 2392, 2418, 2474, 2521, 2557 (Q2 only) = 20 reports.
Temp: `%TEMP%\fcf_run\<iss>\` (batch helper scripts in `%TEMP%\fcf_run\121\b2\`).

## Status per report

| report | status | notes |
|---|---|---|
| 121 Q1 | verified | override: header texts; line 9 (options in consolidated sub) → 6; (*) interest = operating 'ריבית ששולמה' + appendix ב 'ריבית ששולמה והוונה למלאי' p48 (entered negative, documented) |
| 121 Q2 | verified | same decisions (line 8 → 6; appendix p52) |
| 155 Q1 | verified | header texts; line 4 text fix 'פירעון אגרות חוב'; 'מימוש אופציה' (62,559) FY25 → 14 (put option on דרך עפר shares, board report Q2 p11); no (*) outside |
| 155 Q2 | verified | same; c4 months/end confirmed; (232) in Q2 3M = issue costs → 1 |
| 715 Q1 | verified | header texts; line 5 combined LT repayment (banks+bonds+others) → 7 (note; cross-batch); line 6 text fix; shares+options → 1 (note); C1 c2 −1 source rounding (explained) |
| 715 Q2 | verified | same; line 6 → 7; NCI receipts → 6; C1 ±1 in c1/c2/c3 (explained); 715_checks.json written |
| 1331 Q2 | verified | reversed text layer: line 1 text fixed from image; (*) interest only in appendix ד p32 (bbox incl. heading), note 'הסעיף לא צוין (לא בפעילות מימון)'; line 5 net bank credit+loans → 5 |
| 1644 Q1 | verified | reversed text layer – labels checked on image (all right); header texts; notes; no (*) outside |
| 1644 Q2 | verified | header texts; column notes c2/c4 ((*) retrospective policy change marks in operating section only – not restated); blank cell = 0 |
| 1722 Q1 | verified | EUR; line1 shares+warrants → 1; line3 bank loans net → 4 (board report: LT loans Q4-2025, 'נטו' = net of costs) – aligned with Q2; line4 collections of loans TO apartment buyers → other; line5 return of NCI investment → 12; column note c2 (reclassified investing value) |
| 1722 Q2 | verified | same mapping; C3 now OK; column notes c2/c4/c5 ((*)/(**) reclassification marks outside financing) |
| 2392 Q1 | verified | wrapped label line 4 joined (drop 5); parent/controlling-shareholder loans gross → 4; non-bank/others/related loans gross → 4; repayment line → 7 (auto said 5); column note c2 (* immaterial adjustment) |
| 2392 Q2 | verified | wrapped labels lines 1, 5 joined (drop 2, 6); line 8 repayment → 7; same mapping as Q1 |
| 2418 Q1 | verified | FY column shifted one row in source: re-assigned per Q2 FY & arithmetic (line_values 2-6 c3; add line '[ללא תווית בדוח Q1] פרעון אגרות חוב' (85,000) item 8; drop stray row 7); 'קבלת הלוואה מחברה כלולה' → 4 (all 0); (*) appendix ב interest (positive as printed); issues + column note c3; C2-item ±360 (items 4/5) explained in 2418_checks.json |
| 2418 Q2 | verified | 'קבלת הלוואה מזכויות שאינן מקנות שליטה' 266 → 4 (loan, not equity); (*) appendix ב interest |
| 2474 Q1 | verified | bank/others loan receipt 9,444 & repayment → 5 (ST credit per balance sheet/board report: no LT bank credit) – aligned with Q2; shareholders/related loans repayment → 7 |
| 2474 Q2 | verified | same mapping (line 1 net → 5, line 2 → 5); C2 ±1 (interest 2,176 vs 2,177) explained in 2474_checks.json |
| 2521 Q1 | verified | header texts; notes; lease interest line → 13; no (*) outside |
| 2521 Q2 | verified | same; column notes c2/c4/c5 ((*) 'סווג מחדש' in operating only); C2 −1 (items 4 +1, 13 −2) source rounding explained in 2521_checks.json |
| 2557 Q2 | verified | header texts; line 8 text '(ראה באור 7ט')' from 400-DPI clip; shareholder/related loans gross → 4/7; lease payments (no split) → 10; NCI purchase → 14 |

## Status per company (checks / build / shots / validate)

| issuer | checks | build | shots viewed | validate |
|---|---|---|---|---|
| 121 | 0 unexplained (C1 8 OK, C2 2 OK, C3 16 OK) | built (final) | yes (13 pp) | PASS 332 / FAIL 0 |
| 155 | 0 unexplained (C1 8, C2 2, C3 16 OK) | built (final) | yes (7 pp) | PASS 326 / FAIL 0 |
| 715 | 0 unexplained (C1 4 MISMATCH explained ±1 rounding) | built (final) | yes (7 pp) | PASS 321 / FAIL 4 – the 4 = validate.py line 90 per-column AC6 check ignores documented source-rounding C1 (SCRIPT-ISSUE 1) |
| 1331 | 0 unexplained (C1 3 OK; Q2 only) | built (final) | yes (6 pp) | PASS 137 / FAIL 0 |
| 1644 | 0 unexplained (C1 8, C2 2, C3 16 OK) | built (final) | yes (7 pp) | PASS 328 / FAIL 0 |
| 1722 | 0 unexplained (C1 8, C2 2, C3 16 OK after aligning 4/5) | built (final) | yes (5 pp) | PASS 328 / FAIL 0 |
| 2392 | 0 unexplained (C1 8, C2 2, C3 16 OK) | built (final) | yes (7 pp) | PASS 328 / FAIL 0 |
| 2418 | 0 unexplained (C1 8, C2 2, C3 16 OK; C2-item 2 INFO explained) | built (final) | yes (11 pp) | PASS 326 / FAIL 0 |
| 2474 | 0 unexplained (C2 1 MISMATCH ±1 explained; C3 16 OK) | built (final) | yes (7 pp) | PASS 321 / FAIL 0 |
| 2521 | 0 unexplained (C2 1 MISMATCH −1 explained; C2-item 2 INFO explained) | built (final) | yes (7 pp) | PASS 324 / FAIL 0 |
| 2557 | 0 unexplained (Q2 only) | built (final) | yes (5 pp) | PASS 214 / FAIL 0 |

## Log

- 10:15 started (fresh agent; no previous progress file).
- 10:21 121 done (both verified, built, shots viewed, validate PASS). Batch report notes for 121 kept in this file until batch-2.md is written:
  121: Q1 pp 46-48 (fin 47), Q2 pp 50-52 (fin 51); ש"ח/אלפים; 10 lines + total; C1/C2/C3 all OK.
  Mapping decisions: 'תמורה ממימוש אופציות בחברה מאוחדת' → 6 (cross-batch); (*) appendix 'ריבית ששולמה והוונה למלאי' added to the interest info row as a payment (cross-batch; 1083 has the same structure).
- 10:27 155 done. 'מימוש אופציה' (62,559) FY2025 → 14 (cross-batch: payment on exercise of NCI put option, דרך עפר).
- 10:33 715 done (validate FAIL 4 = SCRIPT-ISSUE 1: validate.py l.90 AC6 per-column C1 check has no exception for documented source rounding; goal AC6 allows documented non-zero C1). Combined LT repayment line (banks+bonds+others) → 7 (cross-batch).
- 10:36 1331 done; 10:38 1644 done; 10:41 1722 done (decisions: 'קבלת הלוואות מתאגיד בנקאי, נטו' → 4 by board report; apartment-buyer loan collections → אחר; 'החזר השקעה לזשמ"ש' → 12); 10:44 2392 done (gross loan lines without stated term → 4/7 even if balance sheet = current).
- NEXT: 2418 (difficulty C), 2474, 2521, 2557. Then write batch-2.md, cleanup TEMP.
- 10:57 2418, 2474, 2521, 2557 done (images displayed and checked for these).
- !! 10:58 DISCOVERED: for 121, 155, 715, 1331, 1644, 1722, 2392 the `view` tool returned "maximum number of images (50) reached" – the
  images were NOT actually displayed, so their visual verification is NOT yet done (verified records were written on text-layer
  evidence). NEXT: re-verify these 7 companies visually with composite images (compose.py in %TEMP%\fcf_run\121\b2: both zooms of a
  company in one image + (*) crops + context pages), fix anything wrong, rebuild, re-validate. Do not count them as visually verified
  until this line says done.
- 11:20 DONE: visual re-verification with composites for 121, 155, 715, 1331, 1644, 1722, 2392 (zoom pages of the screenshots PDFs at 150 DPI
  + (*) crops + 120-130-DPI context pages) and also for 2418 (its images had not displayed either: fin images, 300-DPI grids, (*) crops,
  pages 45/47/49/51 now viewed) and 2474 (Q1 zoom + context + balance sheet/board report). All values/labels/headers matched; no data change.
  Changes made: verified.method texts rewritten to the real method; 1331 report note reworded (operating has a lease-finance adjustment);
  715_checks/2418_checks wording; 2474 notes: 2025 average LT loans ~42M caveat. NEXT: finalize+rebuild all 11, view full-page highlight
  pages (box placement), validate all, write batch-2.md, cleanup.
- 11:23 finalize+rebuild of all 11 done (tool_batch); full-page highlight pages of all 20 reports viewed (4 composites) – boxes right.
  !! CORRECTION: images were displayed again only from 11:01 (v155z). NOT yet actually seen: 121 (all), 2474 Q2 zoom, 2521 (all),
  2557 (all). NEXT: view composites for these, then validate all, write batch-2.md, cleanup.
- 11:36 DONE: 121, 2474 Q2, 2521, 2557 now actually viewed (composites w121z/w121s/w121ctx, w2474_2521, w2521ctx, w2557z, w2557ctx);
  all values match. 715 notes refined (bond schedule p24 read: ~200M bonds of 703,645 in 2025; 2026 col mostly series 15). Method texts
  corrected. finalize+checks (0 unexplained)+build all 11 OK; validate: all FAIL 0 except 715 FAIL 4 (SCRIPT-ISSUE 1).
  NEXT: write batches/batch-2.md, then delete %TEMP%\fcf_run\<iss>\ for my 11 issuers.
- 11:40 batch-2.md written; tool_integrity → CLEAN; %TEMP%\fcf_run\<iss>\ deleted for all 11 issuers (_runs left for Phase C).
  BATCH 2 COMPLETE. Nothing left to do.
