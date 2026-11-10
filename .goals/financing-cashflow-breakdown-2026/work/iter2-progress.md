# Iteration 2 — progress checkpoint (Builder)

Resume rule: read this file first. Items are done in the order below; "done" items have their evidence in
`builder-report-2.md` (draft notes in this file until the report is written).

Snapshot (taken before any change, 2026-11-10 ~14:50): `%TEMP%\fcf_run\_iter2\snapshot\`
(data 324, overrides 192, xlsx 87, pdf 86, manifest.json with SHA-256). Do NOT retake it.

Helper scripts (temp): `%TEMP%\fcf_run\_iter2\tools\` (dump_lines, show, search2, crops, edge_diag, solo_scan,
solo_classify, solo_composites). Evidence composites: `%TEMP%\fcf_run\_iter2\ev\e1..e8*.png` (viewed by me, all
displayed).

## Evidence already confirmed on images (by me)
- e1 1905: Q1 p37 BS current 'אשראי מתאגידים בנקאיים ואחרים' 485,967 / non-current 'הלוואות מתאגידים בנקאיים ומנותני
  אשראי אחרים' 103,947 (784 at 31.12.25); p42 באור 3 bank loan 86.1M prime+0.7% principal 26.3.2028 (+17M financial
  body); Q2 p39 current 503,156 / non-current 104,442 (784); p46 באור 3 same loan.
- e2/e3 2386: Q1 p26 current 'אשראי מגופים פיננסיים ונותני אשראי אחרים' 56,850 / non-current 'הלוואה מתאגיד בנקאי'
  48,490 (4,699 at 31.12.25); p35 ביאור 4א(1) 43,424 from a financial body (Jan 2026), repayable at completion, no later
  than 30.6.2030, presented as non-current; Q2 p29 current 60,711 / non-current 'אשראי מגופים פיננסיים (ראה ביאור
  4א(1))' 49,318; p32 receipt line cites ביאור 4א(1).
- e4 341: Q1 p36 / Q2 p40 balance sheets have no separate line for state-guaranteed loans (current 'הלוואות לזמן קצר'
  49,068 / Q2 'הלוואות לזמן קצר וחלויות שוטפות של הלוואות' 155,995; non-current 'הלוואות מתאגידים בנקאיים' 16,334 /
  16,342).
- e5 1979 Q2 p52: current 'הלוואות מצדדים קשורים ובעל עניין' 1,202; non-current 'הלוואות מצדדים קשורים ובעלי ענין'
  14,308. 2418 Q2 p45: non-current 'הלוואה מבעלי זכויות שאינן מקנות שליטה' 4,779 at 30.6.26 (no current line).
- e6 486: Q1 p53 current 345,107 / non-current 371,399; Q2 p57 current 657,455 / non-current 179,689.
- e7 1797: Q1 p40 current 'אשראי מתאגידים בנקאיים' 133,910 / non-current 'הלוואות שהתקבלו מבנקים ואחרים' 200,050;
  Q2 p40 current 'אשראי מתאגידים בנקאיים ואחרים' 178,771 / non-current 'הלוואות מתאגידים בנקאיים ואחרים' 165,050.
- e8 2360: Q1 p39 current 755,648 / non-current 2,680,817; Q2 p41 current 891,308 / non-current 2,619,555
  ('אשראי והלוואות מתאגידים בנקאיים').

## M8 (38D) – visual verification by 2 read-only sub-agents (27 composites vis_solo\solo_01..27, all displayed)
267 claims: 254 SEP, 13 NOT. NOT (to drop): 400 Q1 p16, 400 Q2 p19, 486 Q2 p18, 1039 Q1 p12, 1622 Q1 p11,
1622 Q2 p13, 1680 Q2 p55, 2371 Q2 p37, 2418 Q1 p51, 2440 Q1 p22, 2464 Q2 p49, 2474 Q2 p10, 2478 Q2 p41.

## Status

| item | status | notes |
|---|---|---|
| snapshot | done | 14:50 |
| read code + diagnostics | done | edge_diag_before.txt (slivers), blanks |
| M8 verification | done | see above |
| code changes | done | fcf_lib (STAR_SIGN_REMARK, cf_statement_name), finalize (other_cf_pages, consolidated, zoom_blank_cells), build_company (S4, M10), fcf_render (S7 snapping/frames/red frames/captions, M10), validate (S9) |
| override changes | done (~16:40) | tools\apply_iter2.py applied ONCE – DO NOT RE-RUN (S3 c4 append is not idempotent). Change list: %TEMP%\fcf_run\_iter2\override_changes.json (199 changes, 104 files); copy in work\iter2_override_changes.json (delete at end or keep as record) |
| build_master הסבר | done | מקור (1484 non-consolidated), כלל A label, D1–D3 row |
| finalize all 162 | done | checks unexplained 0; 1905/2386 vectors OK |
| build all 86 + master | done (15:30 run) | master rows (648, 6190, 178, 188) |
| S7 render rework | done (16:17 build) | padded frames (framed/hpad), contiguous zoom split, (*) line crops at row gaps, red frames on full/ctx pages centred on gaps, full-page frame lines via clear_band (glyph_profile), header graphics (graphic_top / snap_header_rect / widen_for_graphic: 1193 Q1 widened, 1083 Q2 + 121 Q2 icon excluded, 1193 Q2 logo whole), box_off_crossing_rows (2417 Q2 legend: units in zoom strip). Visual QA: sub-agents A (33 imgs), B (32), C (39) – all PASS/MINOR after fixes; edge_diag_final.txt: no text slivers at crop edges (only 200 Q2 star top tight rows, 1083 Q2 3-px icon tip) |
| caption checks | done | S7e/S7f/S7g/M9/M10 captions OK (captions_all.json, caption_checks.txt) |
| next | | change-log diff vs snapshot; verified.iteration2 records; re-finalize; gates; PIPELINE; reports; cleanup |

