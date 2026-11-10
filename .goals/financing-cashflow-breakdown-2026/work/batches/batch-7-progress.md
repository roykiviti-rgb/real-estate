# Batch 7 — progress checkpoint (Phase B)

Issuers: 473, 1330, 1618 (pilot – rebuild check only), 1903, 1905, 2384, 2386, 2429, 2449, 2522, 2559.

Status legend: todo / in-progress / verified (report) / built (company: checks 0 unexplained + build + shots viewed + validate FAIL 0).

| issuer | Q1 | Q2 | company | notes |
|---|---|---|---|---|
| 473 | verified | verified | DONE (checks 0 unexpl., built, shots viewed, validate PASS 336 FAIL 0) | items: loan from NCI→4, warrant buy-back→9 |
| 1330 | verified | verified | DONE (checks 0, built, shots viewed, validate PASS 325 FAIL 0) | appendix (*) interest via outside_add + boxes.header on appendix page |
| 1618 | pilot-verified | pilot-verified | DONE: checks unexplained 0 (C1 OK 8, C2 OK 2, C2-item INFO 2, C3 OK 16); validate PASS 338 FAIL 0; shots 9 pages viewed (T2 label in Q2 caption OK) | do NOT re-verify |
| 1903 | verified | verified | DONE (checks 0, built, shots viewed, validate PASS 330 FAIL 0) | parent loans→5 (current balance), fin. institution credit→5, restated 2025 cols (*) |
| 1905 | verified | verified | DONE (checks 0, built, shots viewed, validate PASS 321 FAIL 0) | no heading – visual; restated (*) 2025 cols; issue: 280,000 gross in Q2 interim cols only |
| 2384 | verified | verified | DONE (checks 0, built, shots viewed, validate PASS 325 FAIL 0) | Q1-2025 395,555 printed on shares line → assigned to bonds line (§9) + issue; appendix-B interest |
| 2386 | verified | verified | DONE (C2 2025 ±1 rounding explained, C3 aligned, built, shots viewed, validate PASS 333 FAIL 0) | partner & interested-party loans →5 both reports; private placement shares+options →1 |
| 2429 | verified | verified | DONE (checks 0, built, shots viewed, validate PASS 326 FAIL 0) | NCI loan →4 (Q2 net_loans), lease +53 Apr–Jun 2026 as printed |
| 2449 | verified | verified | DONE (checks 0, built, shots viewed, validate PASS 318 FAIL 0) | 2025 interim cols restated (header 2025*) |
| 2522 | verified | verified | DONE (C2-item 4/7 ±123,001 explained, built, shots viewed, validate PASS 321 FAIL 0) | Q1 cf_pages +27 (re-extracted); appendix-A interest = operating |
| 2559 | verified | verified | DONE (checks 0 unexpl.: C2 2025 −2 + 4 C2-item ±1 explained; built; shots viewed (thumbnail sheet D); validate PASS 330 FAIL 0) | Q1 = -01 amended; line 'פירעון הלוואות מתאגידים מוחזקים ובעלי עניין' →5 both (C3 OK); 52,500 IPO price-adjustment to הפניקס →1 (neg.) |

## IMPORTANT (10:55): image-viewer limit
The view tool refused images at the start (limit 50 reached) – the first visual checks of 473, 1330, 1903, 1905,
2384, 2386 and the 1618/473/1330/1903/1905/2384/2386 screenshots were NOT actually seen. Re-done 10:50–11:00 with
composite images (compose.py): review fin+(*) crops of 473, 1330, 1903, 1905, 2384, 2386 now SEEN – all values,
labels, headers, units match (no change needed). Screenshot layout checks DONE 11:08 (thumbnail sheets A–D for
1618/473/1330/1903/1905/2384/2386/2559 + numeric geometry check + caption text check) – all OK.
- 11:10 2384 Q1: 395,555 (Q1-2025, printed on shares line) re-assigned to the bonds line via line_values
  (conventions §9); 2384_checks.json now only _doc; header box tidied (boxes.47.header). Rebuilt, PASS 325.
- 11:12 FINAL: checks (11 issuers) unexplained 0 (C1 OK 88, C2 OK 20 + 2 explained, C2-item INFO 9, C3 OK 176);
  validate --issuers (11) --no-master PASS 3543 FAIL 0. Batch report batch-7.md COMPLETE.
- Remaining: none. 11:14 deleted %TEMP%\fcf_run\<iss>\ for all 11 issuers (other batches' folders and _runs untouched).
  BATCH 7 COMPLETE.

## Log
- 2026-11-10 10:15 started (fresh agent, no previous progress file).
- SCRIPT-ISSUE 1 (cosmetic, worked around): (*) crop on an appendix-only page (1330 p54/p58) showed only the
  company name, no column headers (auto geometry finds no header on that page) -> override `boxes.<p>.header`.
- Helpers in %TEMP%\fcf_run\473\: search.py (query json), words.py (<iss> <Q> pages), dumpdata.py, dump_triage.py.
