# Batch 8 progress (checkpoint) — Phase B

Batch Builder 8, iteration 1. Started 2026-11-10 10:13. **State at 11:40: all 20 reports verified (visually, see below),
all 11 companies built (final) and validated; remaining: write `batch-8.md`, clean `%TEMP%\fcf_run\<iss>\`.**
Issuers (20 reports): 573 (Q1,Q2) · 584 (Q2) · 719 (Q1,Q2) · 771 (Q1,Q2) · 1680 (Q1,Q2) · 2389 (Q1,Q2) ·
2396 (Q1,Q2) · 2440 (Q1,Q2) · 2464 (Q1,Q2) · 2503 (Q1,Q2) · 2570 (Q2)

Helper scripts (all in `%TEMP%\fcf_run\573\`, deleted at the end): `composite.py` (source-PDF composite: header strip +
financing section + (*) lines + `--scan` crops of every interest/dividend/'paid' line on the statement pages),
`shotsgrid.py` (contact sheet of screenshots-PDF pages), `pagetext.py` (page text by blocks), `captions.py`/`allcap.py`
(screenshot captions as text), `search.py`, `render.py`, `geo.py`, `ctx.py`, `summary.py`, `fix_verified.py`.

## IMPORTANT – the image cap and the re-check
- From 10:14 to ~11:02 EVERY `view` of an image returned "You've reached the maximum number of images (50)" and showed
  NOTHING. Reports first marked "verified" in that window had NOT been seen. Images display from ~11:03 on.
- Re-checked on real images (11:18–11:36), with composites (several crops per PNG) and the output confirmed displayed:
  **573 Q1, 573 Q2, 584 Q2, 719 Q1, 719 Q2, 771 Q1, 771 Q2, 1680 Q1, 1680 Q2, 2389 Q1, 2389 Q2, 2396 Q1, 2396 Q2,
  2440 Q1, 2440 Q2, 2464 Q1 (operating page / (*) scan)**; screenshots PDFs of 573, 584, 719, 771, 1680, 2389, 2396,
  2440 checked on two contact sheets (boxes) + caption text extracted from the PDFs.
- Seen properly the first time (after 11:03): 2464 Q2 (pages 92-94, p89, p111, shots s3/s5/s6), 2503 Q1/Q2, 2570 Q2.
- Images used since 11:03: ≈ 39 (29 before the composites, 8 composites, 2 contact sheets).

### Visual re-check log
- 11:18 573 Q1+Q2 `comp_573_Q1_573_Q2_111826.png` – OK (14x3, 14x5, appendix C interest + dividend rows).
- 11:23 584 Q2 + 573 scans `comp_584_Q2_573_Q1-scan_573_Q2-scan_112326.png` – OK.
- 11:24 719 Q1+Q2 `comp_719_Q1_719_Q2_112415.png` – OK (+8 C1 in Q1 3M-2025 confirmed on the image).
- 11:24 771 Q1+Q2 `comp_771_Q1_771_Q2_112447.png` – OK (Q2 c1/c2 = 6 months confirmed).
- 11:25 1680 Q1+Q2 `comp_1680_Q1_1680_Q2_112517.png` – OK (Q1 (*) crop with header box; held-for-sale line below total).
- 11:26 2389 Q1+Q2 `comp_2389_Q1_2389_Q2_112554.png` – OK; NO (*) footnote on p50 → c2/c4 notes corrected.
- 11:26 2396 Q1+Q2 `comp_2396_Q1_2396_Q2_112632.png` – OK; Q1 total label corrected ('(ששימשו) שנבעו').
- 11:27 2440 Q1+Q2 + 2464 Q1 scan `comp_2440_Q1_2440_Q2_2464_Q1-scan_112713.png` – OK.
- 11:34/11:35 screenshots contact sheets `sheet_113451.png` (573/584/719/771), `sheet_113512.png` (1680/2389/2396/2440) – boxes OK.
- Text-layer checks of every note claim that had come from an unseen image (`pagetext.py`): all confirmed except
  (fixed): 2396 pp. 47-49 / 52-54 are statements of 'דיורים בע"מ' (not separate data); 2389 Q2 '(*) סווג מחדש' quote
  (not printed; equity statement says 'הצגה מחדש של מספרי השוואה, ראו ביאור 2ג''); 2440 Q2 p53 caption wording;
  2464 appendix labels are '(א)/(ב)' (not 'נספח'); 719 C1 explanation no longer claims a 300-DPI zoom.
- All `verified.method` texts rewritten (fix_verified.py) to state exactly what was seen and when.

## Status per report (final)

| report | status | key points |
|---|---|---|
| 573 Q1 | verified + built | interest only in appendix C p39 (positive, 'הסעיף לא צוין'); (*) bbox incl. heading; MRPL sale 1,425 → 6 |
| 573 Q2 | verified + built | same; 'רכישה עצמית של מניות על ידי בעלי זשמ"ש' 1,425 = MRPL sale → 6 |
| 584 Q2 | verified + built | appendix C interest 2,386/5,194/10,375; loans: מאחרים receipt→4, repayment→5, מתאגידים פיננסיים→5 |
| 719 Q1 | verified + built | C1 +8 (3M-2025, source) explained; project loans 4/7; ST credit gross → 5 |
| 719 Q2 | verified + built | |
| 771 Q1 | verified + built | parent loan back-to-back to parent's Series B → 4; interest in financing |
| 771 Q2 | verified + built | c1/c2 periods set; C2-item (195) explained; -01 appraisal |
| 1680 Q1 | verified + built | contingent consideration → אחר; boxes.31.header |
| 1680 Q2 | verified + built | cf_pages +p38 (re-extract); wrong running header noted |
| 2389 Q1 | verified + built | bonds+warrants package → 3; NCI loans → 4/7 |
| 2389 Q2 | verified + built | Q2-2026 17,761 = Series A expansion → 3 |
| 2396 Q1 | verified + built | lease P+I → 10; bond buy-back → 8; institutional ליווי loan → 4; net project loans → 5 |
| 2396 Q2 | verified + built | C2 ±1 explained |
| 2440 Q1 | verified + built | |
| 2440 Q2 | verified + built | |
| 2464 Q1 | verified + built | -01 appraisal |
| 2464 Q2 | verified + built | 'פרעון הלוואות ושטר הון מצדדים קשורים' (1,310) → 7 (decision) |
| 2503 Q1 | verified + built | partnership: 1 / 11; 'הלוואות ללא מועד פרעון לבעלי השליטה' → 11 (decision) |
| 2503 Q2 | verified + built | C2 1,793 interest explained |
| 2570 Q2 | verified + built | consolidated pp. 41-42 confirmed (separate pp. 59-60) |

## Company status (checks / build / shots / validate) – final run 11:35–11:38

| issuer | checks | build | shots | validate |
|---|---|---|---|---|
| 573 | C1 8 OK, C2 2 OK, C3 16 OK | final | sheet + captions | PASS 338 / FAIL 0 |
| 584 | C1 3 OK | final | sheet + captions | PASS 140 / FAIL 0 |
| 719 | C1 1 MISMATCH (explained), C2 2 OK, C2-item 2 INFO (explained), C3 16 OK | final | sheet | PASS 329 / FAIL 1 (SCRIPT-ISSUE 1) |
| 771 | C1 8 OK, C2 2 OK, C2-item 2 INFO (explained), C3 16 OK | final | sheet | PASS 324 / FAIL 0 |
| 1680 | C1 8 OK, C2 2 OK, C3 16 OK | final | sheet | PASS 326 / FAIL 0 |
| 2389 | C1 8 OK, C2 2 OK, C3 16 OK | final | sheet | PASS 330 / FAIL 0 |
| 2396 | C1 8 OK, C2 2 MISMATCH ±1 (explained), C2-item 2 INFO (explained), C3 16 OK | final | sheet | PASS 328 / FAIL 0 |
| 2440 | C1 8 OK, C2 2 OK, C3 16 OK | final | sheet + captions | PASS 323 / FAIL 0 |
| 2464 | C1 8 OK, C2 2 OK, C3 16 OK | final | s3/s5/s6 seen + captions | PASS 325 / FAIL 0 |
| 2503 | C1 8 OK, C2 1 MISMATCH 1,793 (explained), C2-item 3 INFO (explained), C3 16 OK | final | s2/s3/s6 seen | PASS 332 / FAIL 0 |
| 2570 | C1 5 OK (Q2 only) | final | s1/s2/s3 seen | PASS 207 / FAIL 0 |
`checks.py --issuers <all 11>` → unexplained mismatches: 0. `tool_integrity.py` → CLEAN.

## SCRIPT-ISSUEs
1. validate.py AC6 (line 90) ignores C1 explanations → 719 Q1 3M-2025 (+8, source) always FAILs (batch 2: 715 same).
2. (cosmetic) fcf_render.py line 352/394: `outs` is report-wide, so every operating/investing context page gets
   'שורות ה-(*) שבעמוד זה מוצגות בהגדלה...' even without (*) lines → workaround: context_sections with the exact
   appendix title for 573 Q1 p38, 573 Q2 p40, 584 p31.
3. (cosmetic) (*) crop on a page whose header the extractor did not box shows only the title (1680 Q1 p31) →
   boxes.31.header (same as batch 7 SCRIPT-ISSUE 1).
4. (minor) extractor's cf_pages missed the appendix page of 1680 Q2 (p38) → cf_pages override + re-extract;
   context_sections default 'פעילות שוטפת' on appendix-only pages → explicit titles.

## Next step
DONE (11:42): `batches/batch-8.md` written. Temp folders `%TEMP%\fcf_run\<iss>\` of the 11 issuers deleted (not `_runs`).
Nothing left to do for batch 8 unless Phase C asks for changes.
