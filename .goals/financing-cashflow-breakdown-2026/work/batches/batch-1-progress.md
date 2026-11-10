# Batch 1 — progress checkpoint (Phase B, iteration 1)

**STATE: COMPLETE.** All 19 reports verified on images, all 10 companies built without `--draft`, report written to
`work\batches\batch-1.md`. Temp folders `%TEMP%\fcf_run\<iss>\` of the 10 issuers deleted at the end (if this line
is present and a folder still exists, delete it – nothing else is left to do). A resumed agent has nothing to redo.

Issuers (exclusive): 486, 1096, 1338, 1490, 1532, 1797, 1829, 1969 (Q2 only), 2360, 2533.

## Status per report

| issuer | Q1 | Q2 | checks | build | shots viewed | validate |
|---|---|---|---|---|---|---|
| 486 | verified | verified | C1 8 OK, C2 2 OK, C3 16 OK | built | yes | PASS 323 / FAIL 0 |
| 1096 | verified | verified | C1 8 OK, C2 2 OK, C3 16 OK | built | yes | PASS 320 / FAIL 0 |
| 1338 | verified | verified | C1 8 OK, C2 2 OK, C3 16 OK | built | yes | PASS 326 / FAIL 0 |
| 1490 | verified | verified | C1 8 OK, C2 1 OK + 1 explained (−2), 4 C2-item INFO explained, C3 16 OK | built | yes | PASS 328 / FAIL 0 |
| 1532 | verified | verified | C1 8 OK, C2 2 OK, C3 16 OK | built | yes | PASS 322 / FAIL 0 |
| 1797 | verified | verified | C1 8 OK, C2 2 OK, C3 16 OK | built | yes | PASS 328 / FAIL 0 |
| 1829 | verified | verified | C1 8 OK, C2 2 OK, C3 16 OK (5/7 aligned) | built | yes | PASS 328 / FAIL 0 |
| 1969 | n/a | verified | C1 5 OK | built | yes | PASS 205 / FAIL 0 |
| 2360 | verified | verified | C1 8 OK, C2 1 OK + 1 explained (+1), C3 16 OK | built | yes | PASS 330 / FAIL 0 |
| 2533 | verified | verified | C1 6 OK + 2 explained (FY −1,000 source), C2 2 OK, C3 16 OK | built | yes | PASS 318 / FAIL 2 = SCRIPT-ISSUE 1 |

## Log (newest last)

- 10:15 started (fresh agent).
- 10:17–10:57 per-company loop (review, overrides, finalize, checks, build, shots, validate) for all 10 issuers – details in batch-1.md.
- 11:05 header-text cleanup + top-level "text_layer" in all 19 overrides; tool_batch finalize/build (my issuers only).
- 11:14–11:25 **complete visual re-verification** on images that were actually displayed (the viewer had silently stopped
  showing images after its limit during the first pass): zooms, full pages, context pages, (*) crops of all 10 companies
  (montages of the same renders where needed). All values/labels/headers/units/(*) confirmed.
- 11:26 verified.method rewritten (accurate description), finalize 19/19, build 10/10, checks unexplained 0,
  validate per issuer (all FAIL 0 except 2533 FAIL 2 = SCRIPT-ISSUE 1), tool_integrity CLEAN.
- 11:30 batch-1.md written.
- 11:32 %TEMP%\fcf_run\<iss>\ deleted for all 10 issuers (_runs and other batches' folders untouched). **Batch 1 finished.**
