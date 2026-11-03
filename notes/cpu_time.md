# CPU time of the computations (3 November 2026)

Method: `notes/cpu_time.py`, run on the original workspace
`~/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work` on Mordell. Every job writes its own `.log` file,
created when the job starts and last modified when it ends; the running time of a job is the difference of the two
(GNU `stat` `%Y - %W`). All the programs (Magma, Sage scripts, the C++ sequence engine) are single-threaded. Logs of
driver processes that only launch and wait for other jobs are excluded. Jobs without a log are not counted, and when
the machine was oversubscribed running times slightly exceed CPU times, so the totals are approximate.
The computations ran between 28 October 2026 14:43 and 3 November 2026 01:10 (CET).

| degrees | all jobs (h) | Lemma 4.11 (h) |
|---|---|---|
| d <= 11 | 24.0 | 3.7 |
| d = 12 | 46.7 | 34.8 |
| d = 13-17 | 34.7 | 0.0 |
| d = 18 | 33.4 | 20.5 |
| d = 19 | 33.5 | 19.9 |
| d = 20 | 123.4 | 107.2 |
| d = 21 | 198.8 | 165.3 |
| d = 22 | 889.4 | 774.8 |
| total | 1384.0 | 1126.2 |

"Lemma 4.11" counts the per-character jobs in `large_orders/` and the top-level sequence checks
(`check_sequences*`, `verify_large*`, `large_*`). These totals include some exploratory and superseded runs that
are not used in the proof, and they do not include the nonic computations in `degree09/` (the second check for d = 9).
Cross-check: for d = 22 the run logs `run_characters*.log` record 5018 character jobs with a total of 675.8 hours,
not counting their independent verification.
