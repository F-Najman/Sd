# CPU time and disk space of the computations (3 November 2026)

Statement numbers refer to the paper as revised on 3 November 2026 after the review; the computations showing
that characters are not strange are those of Lemma 4.12 (Lemma 4.11 in the earlier version).

Method: `notes/cpu_time.py`, run on the original workspace
`~/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work` on Mordell. Every job writes its own `.log` file,
created when the job starts and last modified when it ends; the running time of a job is the difference of the two
(GNU `stat` `%Y - %W`). All the programs (Magma, Sage scripts, the C++ sequence engine) are single-threaded. Logs of
driver processes that only launch and wait for other jobs are excluded. Jobs without a log are not counted, and when
the machine was oversubscribed running times slightly exceed CPU times, so the totals are approximate.
The computations ran between 28 October 2026 14:43 and 3 November 2026 01:10 (CET).

| degrees | all jobs (h) | Lemma 4.12 (h) |
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

"Lemma 4.12" counts the per-character jobs in `large_orders/` and the top-level sequence checks
(`check_sequences*`, `verify_large*`, `large_*`). These totals include some exploratory and superseded runs that
are not used in the proof, and they do not include the nonic computations in `degree09/` (the second check for d = 9).
Cross-check: for d = 22 the run logs `run_characters*.log` record 5018 character jobs with a total of 675.8 hours,
not counting their independent verification.

## Disk space, and an estimate for d = 23

Sizes of the folders of the workspace (`du`, in GiB) on 3 November 2026:

| folder | total | `large_orders/` (Lemma 4.12) | rest |
|---|---|---|---|
| degree18 | 4.8 | - | 4.8 |
| degree19 | 11.3 | 0.5 | 10.8 |
| degree20 | 31.0 | 11.0 | 20.0 |
| degree21 | 84.0 | 46.9 | 37.1 |
| degree22 | 219.3 | 159.4 | 59.9 |
| whole workspace | 361.5 | | |

The rest is mostly the non-principality matrices of the mod 2 sieve (the folders `fullNNN/`, 1-8 GiB per prime for
d = 22) and the formal immersion data. `notes/disk_usage.py` measures the character jobs of Lemma 4.12. A job is a
pair (p, n), and its running time is computed from its logs as above:

    == work/degree20/large_orders: 1951 jobs, 290 primes, p up to 525313, 11.7 GB, 101.0 h
       p in [0.0, 0.5) x 10^6:   863 jobs,    2.2 MB and    0.5 min per job
       p in [0.5, 1.0) x 10^6:  1088 jobs,    9.0 MB and    5.2 min per job
    == work/degree21/large_orders: 2815 jobs, 477 primes, p up to 1050013, 50.2 GB, 154.7 h
       p in [0.0, 0.5) x 10^6:  1314 jobs,    6.6 MB and    0.3 min per job
       p in [0.5, 1.0) x 10^6:   180 jobs,   14.3 MB and    1.1 min per job
       p in [1.0, 1.5) x 10^6:  1321 jobs,   29.5 MB and    6.6 min per job
    == work/degree22/large_orders: 5018 jobs, 727 primes, p up to 2099197, 170.9 GB, 722.0 h
       p in [0.0, 0.5) x 10^6:  1876 jobs,    7.1 MB and    0.3 min per job
       p in [0.5, 1.0) x 10^6:   675 jobs,   20.0 MB and    1.8 min per job
       p in [1.0, 1.5) x 10^6:   336 jobs,   29.8 MB and    4.0 min per job
       p in [2.0, 2.5) x 10^6:  2131 jobs,   62.9 MB and   18.8 min per job

The size of a job grows linearly with p. Its running time grows faster, between quadratically and cubically in p.

**Estimate for d = 23 (nothing was computed).** Suppose that the intersection matrices of Lemma 4.1 have rank 46 mod 2
for some M, as they do for d = 20, 21, 22. Then B(23) = floor((2^{23/2}+1)^2/2) = 4197200, twice B(22). No
supersingular curve over F_{2^23} has a larger prime factor, since its order is 3·2796203, 277·30269 or 5·1013·1657.
The new admissible primes are the prime factors above 10^5 of the orders #E(F_{2^23}); the primes dividing 2^f ± 1
with f < 23 add almost nothing. The Hasse interval is √2 times as long as for d = 22, so there are about √2 times as
many new primes, and they are about twice as large. Hence:

* `large_orders/` grows by a factor of about 2√2 ≈ 2.8 (it was 3.4 from d = 21 to 22), to 450-550 GiB;
* the rest grows by the observed factor of 1.6-1.9, to about 100 GiB;
* in total that is about 600 GiB, three times d = 22. This agrees with the factors 2.7, 2.7, 2.6 of the totals
  from d = 19 to 22.

The CPU time grows faster. There would be about √2 · 2131 ≈ 3000 new jobs at p ≈ 4.2·10^6, each taking 1.25-2.5 h
(18.8 min at p ≈ 2.1·10^6, times 4 to 8). That is 3750-7500 CPU hours, plus the smaller primes: several thousand CPU
hours, 5-10 times the 722 h of the Lemma 4.12 jobs for d = 22.

The disks of Mordell on 3 November 2026 are two SSDs of 894 GB each. `/home`, which holds the workspace, is 99% full
(15 GB free), and `/` has 768 GB free.
