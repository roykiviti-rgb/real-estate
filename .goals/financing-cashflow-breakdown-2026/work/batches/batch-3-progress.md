# Batch 3 — progress checkpoint (Phase B)

Owner: Phase B batch 3 Builder. Issuers: 200, 421, 531, 1039, 1068, 1974, 2458, 2486, 2487, 2567 (Q2 only).
Protocol: `W\PIPELINE.md` + `W\phaseB-conventions.md`. Batch report: `W\batches\batch-3.md`.
Own helper scripts: `%TEMP%\fcf_run\200\b3tools\` (deleted at the end with the issuer temp folders).

## Status per report (final, 11:19)

| issuer | Q1 | Q2 | checks | build | shots viewed | validate (single issuer) |
|---|---|---|---|---|---|---|
| 200 | verified | verified | OK (C1 8, C2 2, C3 16) | built | yes | PASS 325 / FAIL 0 |
| 421 | verified | verified | OK (C1 8, C2 2, C3 16) | built | yes | PASS 327 / FAIL 0 |
| 531 | verified | verified | OK; C2 2026 −1 explained (531_checks.json) | built | yes | PASS 322 / FAIL 0 |
| 1039 | verified | verified | OK (C1 8, C2 2, C3 16) | built | yes | PASS 324 / FAIL 0 |
| 1068 | verified | verified | OK (C1 8, C2 2, C3 16) | built | yes | PASS 330 / FAIL 0 |
| 1974 | verified | verified | OK (C1 8, C2 2, C3 16) | built | yes | PASS 327 / FAIL 0 |
| 2458 | verified | verified | OK; C2 2025 −191 explained (2458_checks.json) | built | yes | PASS 322 / FAIL 0 |
| 2486 | verified | verified | OK; C2 80 / 1,799 explained (2486_checks.json) | built | yes | PASS 324 / FAIL 0 |
| 2487 | verified | verified | OK (C1 8, C2 2, C3 16) | built | yes | PASS 323 / FAIL 0 |
| 2567 | n/a | verified | OK (C1 5; Q2 only) | built | yes | PASS 210 / FAIL 0 |

All 10 together: validate PASS 3080 / FAIL 0; checks C1 77 OK, C2 14 OK + 4 MISMATCH (all explained), C2-item 5 INFO
(explained), C3 144 OK, unexplained mismatches 0.

## Log (newest last)

- 10:15 started (fresh agent). Read goal, amendments, PIPELINE, conventions, Phase A report, triage rows.
- 10:14–10:50 first pass over all 19 reports (overrides, finalize, checks, build, validate PASS).
- 10:51 found that the `view` tool had NOT displayed images until ≈10:55 (it returned "maximum number of images").
  Every report was therefore re-verified visually afterwards (screenshots-PDF pages and composites, viewed) and every
  claim in the notes was re-checked against the text layer; wrong/unsupported note details were corrected
  (421 note 5א wording, 1068 'באור 4 סעיף 9', 1974 interest position, 2458/2486 C2 wording, 2486 line-1 note: the
  24,744 is a PUBLIC offering (IPO 25.1.2026), not a private placement; 2567 issue wording). Values were all correct.
- 11:09–11:17 re-finalized, re-built all 10, checks 0 unexplained, validate PASS (each issuer FAIL 0).
- 11:22 200 Q1 method text made exact; 200 re-built; all 10: checks unexplained 0, validate PASS 3080 / FAIL 0.
- 11:23 `batch-3.md` written. Temp folders `%TEMP%\fcf_run\<iss>\` of all 10 issuers deleted (incl. b3tools). DONE.

## Key facts / decisions (details in batch-3.md)

- 200: lease line → 10; ST gross receipt/repayment → 5; warrants exercised / issued on own line → 2; bond buy-back → 8.
- 421: securities package (Leumi Partners: shares + warrants A–C) + its issue costs → 1 (conv. 6). NCI-holder LT loans
  (Cyprus) → 4 [mapping decision]. Restatement asterisks only on operating values → column notes, no restated flag.
- 531: Q2 FY bond issuance printed '280,68' → 280,683 (conv. 9; issues + notes). Options line → 2.
- 1039: interest only in financing (13); 'הזרמת הון זשמ"ש' → 6; blank cells → 0 (noted).
- 1068: units מליוני ש"ח; subsidiary IPO 'הנפקת מניות מחברות מוחזקות' 232 → 6 [mapping decision]; derivatives → אחר.
- 1974: 'יפרעון' text fixes; warrants from bond package → 2; 'הלוואות מתאגידים פיננסים' → 4/7.
- 2458: IPO 'מניות וכתבי אופציה' 178,450 → 1 (conv. 6). C2 191 explained.
- 2486: IPO 'מניות ואופציות' 24,744 → 1 (conv. 6); shareholder/investor and 'גופים פיננסים' loans (gross) → 4/7
  [mapping decision]; Q2 FY cash-change typo 6,894 vs 7,342 (outside financing) → issue.
- 2487: interest only in appendix → outside_add (conv. §1 note); 'שינוי בהלוואות לבעלי שליטה' → 5; convertible → 3.
- 2567: 'ריבית ששולמה על שטרי הון' → 11 [mapping decision, alt. 13]; associates/related loans (no term) → 5
  [mapping decision]; right-of-use liability repayment → 10; board report p.14 differs → issue.
