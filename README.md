# Points of prime order on elliptic curves over number fields of degree 9 to 22

Code, ledgers and certificates for the paper

> F. Najman, *Points of prime order on elliptic curves over number fields of degree 9 to 22* (2026),

whose LaTeX source is in [`paper/`](paper/). Let `S(d)` be the set of primes `p` such that some elliptic
curve over some number field of degree `d` has a point of order `p`, and `Primes(x)` the set of primes `p <= x`.
The paper proves:

| `d` | `S(d)` |
|---|---|
| 9, 11 | `Primes(31)` |
| 10, 13, 16 | `Primes(37)` |
| 12, 15 | `Primes(37) ∪ {43}` |
| 14, 17, 18, 19 | `Primes(43)` |
| 20 | `Primes(47) ∪ {61}` |
| 21 | `Primes(47)` |
| 22 | `Primes(53) ∪ {67}` |

Together with Mazur, Kamienny, Parent, Derickx–Kamienny–Stein–Stoll and Khawaja this determines `S(d)` for all `d <= 22`.

## Layout

| Folder | Contents | Paper |
|---|---|---|
| `paper/` | LaTeX source (`main.tex`, `sections/`, `refs.bib`) and the compiled `main.pdf` | |
| `occurrences/` | index of the explicit points of order `p` over fields of degree `d` | Prop. 3.3, Table 1 |
| `dyadic/` | the general version of the mod-2 Oesterlé bound (note, not used in the paper) | Remark 4.6 |
| `large_primes.md` | the admissible primes above `10^5` for each `d` | Cor. 4.7, Prop. 4.13 |
| `audit10/`, `audit11/` | all computations for `d <= 11` (census through degree 11, formal immersion, Hecke obstructions, gonality of `X_1(43)` over `F_2`, the `p = 37` exceptions, large primes for `d = 11`); `audit10` checks the transfer to `d = 10` | Sections 4–6 |
| `degree12/`, …, `degree22/` | the computations for each larger degree; each one reuses the certificates of the smaller degrees after matching the closed points | Sections 4–6 |
| `degree09/` | an independent proof of `S(9) = Primes(31)` (from the nonic classification project), used as a second check | Section 7 |
| `proofs/` | the detailed account of the computations for each degree (`S10_proof_audited.txt`, …, `S22_proof.txt`), the result summaries, the independent audit of `d = 10, 11`, and the note on the correction at `p = 97` | |
| `notes/` | the mathematical review of these proofs made while writing the paper, the CPU time and disk space of the computations, and the changes made after the review of 3 November 2026 | |

In each of `audit11/`, `degree12/`, …, `degree22/`:

* `census_sources.m` enumerates the elliptic curves over `F_{2^f}` with a point of order `p` (Section 5.1);
* `full_sieve.py`, `pair_sieve.py`, `mixed_sieve.py` and `stage2*` produce the non-principality certificates of Lemma 5.2,
  and `independent_rank_checks.json` records their independent check in Sage;
* `export_FI*.m`, `check_fi.py`, `check_prefixes.cpp` and `formal_immersion.json` are the formal immersion computations at the rational cusps (Prop. 5.1);
* `relative*.m` and `check_relative*.py` are the relative formal immersion computations (Lemmas 2.12 and 2.13);
* `final_coverage.json` (or `.json.gz`) is the ledger with the reason for every prime up to the bound of Table 2,
  `support_coverage.json` the ledger with the argument for every type of reduction, and `verify_coverage.py` checks them
  (in `degree22` the final check is `verify_final.py`);
* `proof_manifest.json(.gz)` lists the SHA256 hashes of all the proof inputs, including the large files that are not in this repository, and `REPLAY.txt` lists the commands that reproduce the computations.

## Which script proves what

| Statement | Files |
|---|---|
| Prop. 2.6 b), `gon_Q X_1(53) >= 20` | `degree16/gonality53_rat.py`, `degree16/gonality53_nonrat.py` |
| Prop. 3.3 (examples) | see [`occurrences/README.md`](occurrences/README.md) |
| Cor. 4.7 (intersection matrices, admissible primes) | `audit11/verify_large_odd_bound.py` (`d = 11`), `degree12/prepare_bound.py` (`d = 12`), `degreeNN/dyadic_jets.json` with `degreeNN/verify_dyadic.py` or `verify_auxiliary.py` (`d >= 13`), `degree22/verify_prime_coverage.py` |
| Lemma 4.12, Prop. 4.13 (characters that are not strange, primes above `10^5`) | `audit11/large_order.m`, `degree12/large_order.m`, `degree12/krylov.cpp`, `degree18/large_order.m`, `degree22/verify_large_simd.py`, `degreeNN/large_selected_orders.json`, `degreeNN/independent_sequence_results.json` |
| Lemma 4.14, Prop. 4.15 (primes below `10^5`) | `degreeNN/final_coverage.json(.gz)`, `degree22/verify_prime_coverage.py`; `degree19/odd_anti163_character_norms.m`, `degree20/anti167.m`, `degree21/anti181.m` (odd-degree isogenies) |
| Lemma 4.16, Prop. 4.17 (`p = 127`, `d = 14, 16`) | `degree14/quotient127.m` |
| Prop. 4.18 (`p = 193`, `d = 16`) | `degree16/census193.m`, `degree16/quotient193.m` |
| Prop. 5.1, 5.3 | `census_sources.m`, `full_sieve.py`, `pair_sieve.py`, `mixed_sieve.py`, `formal_immersion.json`, `support_coverage.json` in each folder; `degree22/generic113_mixed_sieve.py` |
| Lemma 6.1, Prop. 6.2 (`p = 37`) | `audit11/rational_two.m`, `audit11/stabilizers.m`, `audit11/decic37.m`, `audit11/decic37_jets.m`, `degree09/P37/rational_isogeny_fibers.m` |
| Prop. 6.3 (`p = 41`) | `degree15/lift41_charzero.m`, `degree15/known41_lifting.m`, `degree16/known41_lifting.m` |
| Lemma 6.4, Prop. 6.5 (`p = 43`) | `degree16/torsion43_upper.m`, `degree16/torsion43_Q_first.m`, `degree16/torsion43_reduction.m`, `degree16/two43_h7.m`, `degree13/mixed43_lifting.m`, `degree13/mixed43_tangents.m`, `degree16/lift43_14.m`, `degree16/known43_cot.m` |
| Prop. 6.6 (`p = 53`) | `degree13/two53_verified.json`, `degree17/relative53.m` |
| Lemma 6.7, Prop. 6.8 (`p = 61`) | `degree15/quotient61/`, `degree17/relative61.m`, `degree21/relative61_ss20.m`, `degree21/relative61_o20.m` |
| Lemma 6.9, Prop. 6.10 (`p = 73`) | `audit11/rational_two.m`, `degree17/relative73.m`, `degree18/relative73_nc.m`, `degree18/quotient_quadratic.m`, `degree21/relative73_multiple.m` |
| Prop. 6.11 (`p = 89`) | `degree16/certify_anti89.m`, `degree22/check_quotient89.py`, `degree22/quotient89_cusps.m`, `degree22/argument89.txt` |
| Lemma 6.12, Prop. 6.13 (`p = 97`) | `degree16/certify_anti97.m`, `degree20/strange_eigenvalues.m`, `degree20/sharp97.m` |
| Prop. 6.14 (`p = 53, 101, 103, 131`, reductions supported on the rational cusps) | `degree19/full_cusps53.m`, `degree20/full_cusps53.m`, `degree20/strange_eigenvalues.m`, `degree20/sharp101.m`, `degree19/verify_relative_cusps_intrinsic.py` and the files `relative103*`, `relative131*`, `relative_cusps*` |
| Prop. 6.15–6.18 (`p = 109, 113, 127, 137`) | `degree20/relative109.m`, `degree20/relative113_ordinary.m`, `degree22/relative113_nc.m`, `degree17/relative127.m`, `degree21/quotient127_cusps.m`, `degree21/quotient127_ss.m`, `degree19/stabilizer137_ordinary.m` |

## Rerunning the computations

The computations were run with Magma V2.30-1, SageMath 10.7 (with FLINT, NTL and M4RI), the `mdmagma` package of
Derickx (<https://github.com/koffie/mdmagma>, revision `d1c019c`) with Sutherland's models of `X_1(N)`, and `g++`
for the `C++` programs. They were run on the server Mordell from the root of the original workspace
`/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a`, whose folder `work/` contains the folders
`degreeNN` and `audit1x` of this repository, and the scripts refer to files as `work/degreeNN/...` (or
`work/audit11/...`). Many scripts also contain absolute paths:

* the path of the workspace itself;
* `/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/` (`mdmagma` and Sutherland's models, a submodule of
  <https://github.com/F-Najman/nonic-torsion>) and a few files in the folder `common/` of that repository;
* `/home/fnajman/webpage_sporadic/` (the data of <https://x1mn-sporadic.github.io>), only in the scripts that search
  for the explicit points of Section 3.

To rerun a script elsewhere, recreate these paths (for example with symbolic links, and with `work/degreeNN -> ../degreeNN`
and `work/audit1x -> ../audit1x` in the workspace folder) or replace them in the script. We do not provide a portable
replay wrapper. The file `REPLAY.txt` in each of the folders `degree16`, …, `degree22` lists the commands in order.

The computations took about 1400 CPU hours in total, between 28 October and 3 November 2026 (see
[`notes/cpu_time.md`](notes/cpu_time.md) for how this was measured).

The complete certificates (about 360 GB, mostly matrices of the non-principality tests, exported modular symbol
spaces and Krylov sequences) are not in this repository. The files `proof_manifest.json(.gz)` record their SHA256
hashes, and they are available from the author on request.

## Notes

The proofs and almost all of the computations were produced with heavy AI assistance (OpenAI and Anthropic
models); see the AI disclosure in the paper. Files in `proofs/` are the original accounts of the computations
for each degree, written during the computations; the paper supersedes them where they differ (for example,
the paper uses Silverberg's bound for points with complex multiplication instead of several Frobenius computations).

For `d = 22` the ledgers record the local computations at `p = 163` (`degree22/full163/`, on `X_1(163)` of genus 1027)
and the odd-degree computation `degree22/anti173.m` at `p = 173`. The paper excludes 163 and 173 for `d = 22` directly
with the second gonality bound of Prop. 2.6 a) (Prop. 4.15), so these computations are not needed for the proof.
The changes made after the review of 3 November 2026 are listed in
[`notes/review_response_2026-11-03.md`](notes/review_response_2026-11-03.md).

The code is released under the MIT license (`LICENSE`), except for the files derived from the code of
Derickx–Kamienny–Stein–Stoll, which are under the GPL (see the `DKSS_LICENSE` files).
