# Phase A progress (Builder, iteration 1)

Started 2026-11-10 08:05. Resume from here if the app restarts.

## Milestones
- [x] 0. Read goal, amendments, pilot report, scripts (08:10)
- [x] 1. Inventory of all 178 PDFs (tool_inventory.py -> %TEMP%\fcf_run\_inventory\inventory.json)
- [x] 2. roles.json written by tool_roles.py (DECISIONS dict + roles_2559.json); 162 sources. 2559 Q1: -01 = clean amended
       report (source), -02 = redlined/marked version (alt, not used); financing section identical (visual compare p25 vs p27).
       1829: -01 = full quarterly report (source), main = 1-page appraiser letter. 2520 -01 = investee statements.
- [x] 3. Temp layout: fcf_lib.TEMP_BASE=%TEMP%\fcf_run, temp_dir(issuer), run_dir(tag), temp_path(name, issuer) pid-unique.
- [ ] 4. T1 (תקופה עיקרית) + T2 (month range suffix)  -> T2 in fcf_lib.period_label + finalize; T1 in build_master
- [ ] 5. Manual-entry override schema (finalize) + geometry/boxes (render) + tool_grid.py + tool_review.py
- [~] 6. Extraction engine rewritten: work\fcf_extract.py (engine) + extract_report.py (CLI). Iterating on failures.
- [ ] 7. Auto finalize all + draft company outputs + 1618 rebuilt (verified)
- [ ] 8. triage.csv (tool_triage.py) + C1/C2/C3 on auto data
- [ ] 9. PIPELINE.md
- [ ] 10. builder-phaseA-report.md
- [ ] 11. Cleanup temp, integrity check

## Tools written so far (work\)
tool_inventory.py, tool_roles.py, tool_batch.py (parallel extract/finalize/build/review), tool_triage.py, tool_scan.py,
fcf_extract.py (engine). Exploration scripts live in %TEMP%\fcf_run\_explore (not in WORKSPACE).
Backup of pilot data: %TEMP%\fcf_run\_backup_pilot (data + overrides of 1618).

## Key findings
- Text layer: 'ð' (U+00F0) = nun (cp1255 0xF0 decoded as cp1252) in ~15 reports (1083 Q2, 1680 Q2, 1703 Q2, 1928, 200,
  2441, 2486, 2488, 2559, 373, 584, ...). Fixed generically in fcf_lib.page_words (fix_glyph_text + visual_rtl_order:
  chars of such words re-ordered by x). Numbers can be split into separate spans ('164' ',' '896') -> lone ',' tokens
  accepted as value tokens.
- "no פעילות מימון hit" reports (1083, 1331 Q2, 1644 Q1, 1905, 341 Q1): cause = get_text('text') returns words in
  reversed order (visual) for these PDFs + wrapped headings ('תזרימי מזומנים מפעילות' / 'השקעה') and 1905 has no
  financing heading at all. Text layers ARE usable; our coordinate-based line rebuild handles them.
- Statement detection: blocks of CF-titled pages; board report tables excluded via 'integral part' footer
  (הבאורים המצורפים מהווים חלק בלתי נפרד) + formal title 'על תזרימי' preference; solo 38D separate blocks.
- Footnote markers '3,643)*' handled (remove star + one adjacent paren before sign).

## Next step
Rerun tool_batch.py extract + tool_triage.py; fix remaining C cases (444 Q1, 1068 units, 1622 Q2, 1680 Q2, 2385 Q2,
2481 Q1, 2483 Q2, 2520 Q2, 2521 Q1, 2522 Q1, 2567 Q2, 2574 Q2), then B list review, then finalize/render refactor.

## Update 09:03
- DONE: extraction 162/162 (no hard failures); finalize 162/162 (1618 verified, others unverified drafts).
- DONE: finalize_report.py rewritten (auto+overrides incl. line_values/drop/add/outside/boxes; manual mode; geometry;
  T2 labels via fcf_lib.period_label(quarter_range)); fcf_render uses d["geometry"] (pilot formulas reproduced: 1618
  output identical – same 9 pages, same image sizes); build_company --draft (marked drafts), roles.json new format;
  checks.py (--issuers, per-invocation output in %TEMP%\fcf_run\_runs, explanations per issuer in
  overrides\<issuer>_checks.json – 1618's migrated; global check_explanations.json removed); build_master T1 column
  'תקופה עיקרית' + legend + source-decision rows + --draft; validate.py (--issuers, --no-master, per-invocation out,
  T1 + roles checks); tool_review.py, tool_grid.py, tool_scan.py written.
- NOTE: the `view` tool caches files by path – always write review outputs with unique names (time stamps).
- NEXT: build drafts for all (tool_batch.py build --draft), checks on auto data, triage.csv (with C2/C3), sample
  screenshot review, PIPELINE.md, builder-phaseA-report.md, cleanup.

## Update 09:16
- DONE: drafts built for all 86 companies (before the latest extractor fixes – rebuild at the end).
- FIXED (generic, fcf_extract.py): separate-company (38D) pages recognised by title 'נתונים על תזרימי' and by page
  phrases ('הדוחות הכספיים הנפרדים', 'המידע הכספי הנפרד' ...) -> SOLO_PAGE_RX; among strong blocks a 'מאוחד'-titled
  block wins. Picks changed: 425 Q1 (91-92 solo -> 73-74), 2520 Q2 (55-56 solo -> 32-33), 2570 Q2 (59-60 -> 41-42).
  infer_missing_periods: partner = neighbour that does not duplicate an existing period; uses periods inferred earlier
  in the pass; months-known/end-missing handled (2486 Q2 c3 now 3m; 771 Q2 c2 now 6m 2025).
  malformed_number(): flags irregular digit grouping ('280,68' in 531 Q2 – the source misses a digit).
- Checks on auto data now: C1 MISMATCH 11 (OK 637); C2 MISMATCH 27, N/A 2 (2533: header prints 30 במרס), OK 123;
  C3 MISMATCH 21 (item-level mapping differences Q1/Q2), OK 1195. Reviewed: 1484, 1979, 2458, 2478, 2486, 2503 C2
  diffs are genuine differences between the reports (values read correctly); 719 Q1 2025 column sums 7,911 vs printed
  7,903 (source); 2533 FY -1000 (source, both reports); 2418 Q1 FY column misaligned in the source itself.
- NEXT: triage_notes.json + refine tool_triage difficulty (C2/C3 -> B; C1>2 / empty-label rows -> C), rebuild drafts,
  build_master --draft, validate, manual-override end-to-end test, PIPELINE.md, report, cleanup.

## Update 09:40
- FIXED (generic): label hyphen/comma touching a word is label text, not a value (2384 Q2 wrapped labels now
  correct; 15 labels regained their comma); day numbers next to month words are not values (2487 Q1 extra-column
  regression avoided); letter words reaching beyond the value area stay in the label; suggest_item extended
  (אופציה, הלוואת, ריביות, תקבולים, זשמ"ש=NCI, הנפקות הון, הנפקת חבילה, מניות באוצר, השקעות/חלוקות בעלים,
  shares allotted in a subsidiary -> 6, net-change loan lines -> 5/net_loans). 'other' lines 77 -> 28.
- DONE: triage_notes.json (Phase A findings per report) merged by tool_triage.py; difficulty now A=55 B=103 C=4
  (C: 531 Q2, 2533 Q1, 2533 Q2, 2418 Q1). tool_batches.py -> work/batches.json (8 batches, 20-21 reports each).
- DONE: drafts rebuilt 86/86; master --draft built (648 data rows, T1: 572 כן / 76 לא); validate full run:
  PASS 36245 / FAIL 173 (all expected: 160 missing verification records, C1 on auto data, 2418 empty-label row);
  AC12 integrity PASS. validate --issuers 1618 --no-master: 338/0.
- DONE: manual-mode end-to-end test (x_manual_test.py in TEMP): manual override built from 1484 Q1 auto data ->
  identical items/totals; geometry identical after apply_boxes fix (header box = header x ± 4).
- DONE: checks.explain(): report-specific C1 key 'C1|<iss>|Q1 2026|<label>|total' tried first.
- NEXT: PIPELINE.md, builder-phaseA-report.md, final re-run (extract/finalize/build/master/triage/batches),
  cleanup TEMP, integrity.

## Update 09:55
- FIXED: (*) detection – declared/unpaid wording excluded (573 Q1), nearest 'ששולמו'/'שהתקבלו' heading decides
  (434 Q1), interest/dividends paid disclosed only in an appendix of the statement offered as flagged candidates
  (19 reports, section 'נספח לדוח תזרים המזומנים (מחוץ לפעילות מימון)'); mirrored parentheses in Hebrew labels fixed
  in fcf_lib.normalize_label (35 labels). tool_batch.py now requires --issuers or --all; tool_triage --issuers writes
  to TEMP (never a partial triage.csv); tool_review shows the auto line key + (*) info rows + verified record.
- DONE: work/PIPELINE.md written. Auto-mode override keys tested in isolation (x_auto_ov_test.py in TEMP): OK.
- NEXT: final chain (finalize all, checks, triage, batches, builds, master, validate), builder-phaseA-report.md,
  cleanup TEMP (keep nothing), integrity.

## Update 10:10 – PHASE A COMPLETE
- Final chain run with the final scripts: extract 162/162, finalize 162/162, drafts 86/86, draft master (648 rows,
  T1 572/76). checks (auto data): C1 11 / C2 27 (+2 N/A) / C3 18 item rows; triage A=46 B=112 C=4; batches.json
  (8 batches, 19–22 reports). validate full: PASS 36245 / FAIL 173 (expected); 1618 scoped 338/0.
- (*) crops always cover the whole (*) line; boxes.content key; tool_selftest.py (manual + auto override keys,
  isolated) PASS on 1484 Q1, 2384 Q2, 1618 Q2. 1618 final data identical to the pilot (values, texts, items, checks).
- Written: work/PIPELINE.md, ../builder-phaseA-report.md. %TEMP%\fcf_run deleted (73 MB); tool_integrity CLEAN.
- Phase B starts from PIPELINE.md + triage.csv + batches.json.
