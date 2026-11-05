# Comparison with the strange characters of M. Stoll (5 November 2026)

Michael Stoll sent us the file `strange_characters_400000.txt` (private communication, 4 November 2026):
the orders of the strange characters modulo all primes `p < 4·10^5`.
- SHA256: `c54e845758168e690a6e6357a40332b95d1f93ee9fa2c7ae5e33baacec06c798`.
- 117 lines at 116 strange primes. Only 8713 has two orders.
- The file is not in this repository; ask the authors or Stoll for it.

Its header gives the provenance, which was not rerun here:
- below `2·10^5` it is Table 2 of Derickx-Stoll;
- above that it is a new search with `strange_primes.magma` on the Bayreuth cluster;
- the search covers all pairs `(p, n)` and was complete for `p < 409153` on 4 November 2026;
- every candidate was verified in characteristic 0.

## Results

[`stoll/check_stoll.py`](../stoll/check_stoll.py) compares the list with the paper, and
[`stoll/check_stoll.log`](../stoll/check_stoll.log) is its output.

1. Below `10^5` the list is the same as Derickx-Stoll, Table 2 (`audit11/derickx_stoll_table2.txt`). That
   table is shared by both computations, so this is a consistency check only.
2. For each of the 24268 primes `10^5 < p < 4·10^5`, `h(p) = (p-1)/(2 str(p)) >= 4787`. The minimum is
   at `p = 114889`, where `str(p) = 12`. Also `p^2 > κ·22 + 1` and `p > 3·22 + 1`, so by Derickx-Stoll,
   Corollary 7.5 (Proposition 4.8 of the paper), none of these primes is in `S(d)` for `d <= 22`. Here
   `str(p)` is the lcm of the strange orders, and 1 if `p` is not in the list.
   - This does not use the admissible-prime lists or the modular symbol computations of Lemma 4.12.
   - For `d = 11` and `d = 18`, `B(d) < 4·10^5` (177989 and 263169). So with Corollary 4.7 it is a second
     proof of Proposition 4.13 for these degrees.
   - For `d = 12` and `19 <= d <= 22` it covers only the primes below `4·10^5`.
3. Proposition 4.13 shows that the characters of order `n` modulo `p` are not strange for certain pairs
   `(p, n)`: the files `large_selected_orders.json` of `audit11`, `degree12`, `degree18`, ..., `degree22`.
   Of these pairs, 5450 (at 762 primes) have `p < 4·10^5`, and none of them is strange in Stoll's list.
   Some of the primes are strange for other orders, for example 131203 (order 3) and 299317 (order 2),
   which the proof allows.

| `d` | primes below `4·10^5` / all | character orders below `4·10^5` / all |
|---|---|---|
| 11 | 21 / 21 | 73 / 73 |
| 12 | 82 / 92 | 591 / 656 |
| 18 | 81 / 81 | 615 / 615 |
| 19 | 195 / 196 | 1139 / 1147 |
| 20 | 289 / 444 | 1924 / 3020 |
| 21 | 480 / 850 | 2881 / 5289 |
| 22 | 676 / 1488 | 4261 / 10065 |

The totals agree with the counts in the proof of Proposition 4.13.

## Validation and second check

- The script was validated on a known positive: a list with the line `104701 349 2` added (an order that the
  proof certifies) fails with `AssertionError: (20, 104701, [349])`.
- A separate checker, written by Codex independently of this one, gives the same numbers:
  `work/stoll_400000_crosscheck/check.py` and `result.json` in the campaign workspace, and
  `outputs/Stoll_400000_independent_crosscheck.txt`.

## Scope

This checks only the large-prime step (Section 4.3) for `p < 4·10^5`. It does not check:
- the characters above `4·10^5`;
- the bounds `B(d)` (Corollary 4.7);
- the local computations at 2 (Sections 5 and 6).

The list was computed with the code of Derickx and Stoll (`strange_primes.magma`). The certificates of
Lemma 4.12 come from our own implementation, so the two computations share the definitions and Corollary 7.5,
but not their code.

Files added to the repository with this note: `degree22/large_selected_orders.json`,
`degree22/large_verified.json` and `degree22/independent_sequence_results.json`. The README and
`large_primes.md` already listed them, but they had not been copied. They are identical to the files in the
campaign workspace, and their SHA256 hashes are in `degree22/proof_manifest.json.gz`.
