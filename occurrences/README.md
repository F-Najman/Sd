# Explicit points of prime order (Proposition 3.3, Table 1)

For each pair `(d, p)` of Table 1 of the paper, the table below gives the script that verifies an explicit point of
order `p` on an elliptic curve over a number field of degree `d` (irreducibility of the defining polynomial,
non-singularity of the curve, `pP = 0` and `P != 0`), the log of its run, and the file with the data.
All other primes in `S(d)` follow from `S(d') ⊆ S(d)` for `d' | d` (Lemma 3.1), from Lemma 3.2
(`11, 13, 17` for `d >= 10` and `19` for `d >= 14`), and from Najman–Varivoda for `17, 19, 23` in degree 9.

| `d` | `p` | verification | log | data |
|---|---|---|---|---|
| 9 | 29, 31 | `degree09/realizations/verify_nonic_examples.m` | `degree09/realizations/logs/verify_nonic_examples.log` | in the script |
| 10 | 23, 29, 31 | `audit10/verify_witnesses.m` | `audit10/occurrence.log` | in the script |
| 10 | 37 | `audit10/verify37_witness.m` | `audit10/occurrence37.log` | in the script |
| 11 | 19, 23, 29, 31 (and 11, 13, 17) | `audit11/verify_occurrence.m` | `audit11/occurrence.log` | in the script |
| 12 | 23, 29, 31 | `degree12/verify_small_witnesses.m` | `degree12/verify_small_witnesses.log` | `degree12/small_witnesses.json` |
| 12 | 43 | `degree12/occurrence43.m` | `degree12/occurrence43.log` | in the script |
| 13 | 19, 23, 29, 31, 37 (and 11, 13, 17) | `degree13/verify_occurrences.m` | `degree13/verify_occurrences.log` | `degree13/occurrences.json` |
| 14 | 29, 31, 37, 41, 43 | `degree14/verify_occurrences.m` | `degree14/verify_occurrences.log` | `degree14/occurrences.json` |
| 15 | 23, 29, 31, 37, 43 | `degree15/verify_occurrences.m` | `degree15/verify_occurrences.log` | `degree15/occurrences.json` |
| 16 | 29, 31, 37 | `degree16/verify_occurrences.m` | `degree16/verify_occurrences.log` | `degree16/occurrences.json` |
| 17 | 23 | `degree17/verify_occurrence23.m` | `degree17/verify_occurrence23.log` | `degree17/occurrence23.json` |
| 17 | 29, 31, 37 | `degree17/verify_occurrences.m` | `degree17/verify_occurrences.log` | `degree17/occurrences.json` |
| 17 | 41, 43 | `degree17/verify_occurrences41_43.m` | `degree17/verify_occurrences41_43.log` | `degree17/occurrences41_43.json` |
| 18 | 41, 43 | `degree18/verify_occurrences.m` | `degree18/verify_occurrences.log` | `degree18/occurrences.json` |
| 19 | 23, 29, 31, 37, 41, 43 | `degree19/verify_occurrences.m` | `degree19/verify_occurrences.log` | `degree19/occurrences.json` |
| 20 | 41, 43, 47, 61 | `degree20/verify_occurrences.m` | `degree20/verify_occurrences.log` | `degree20/occurrences.json` |
| 21 | 29, 31, 37, 41, 43, 47 | `degree21/verify_occurrences.m` | `degree21/verify_occurrences.log` | `degree21/occurrences.json` |
| 22 | 37, 41, 43, 47, 53, 67 | `degree22/verify_occurrences.m` | `degree22/verify_occurrences.log` | `degree22/table_occurrences.json`, `degree22/occurrence41.json`, `degree22/cm67.json` |

The degree 18, 19, 20 and 22 folders also contain direct checks of examples for the primes that follow from smaller
degrees (`verify_extension_occurrences.m`, `verify_small_occurrences.m`); these are not needed for the proof.

Most of the examples are points `(x, y)` on Sutherland's models of `X_1(p)`, converted to the Tate normal form
`E(b, c): Y^2 + (1 - c)XY - bY = X^3 - bX^2` with the point `(0, 0)` of order `p` by
`r = (x^2 y - x y + y - 1)/(x^2 y - x)`, `s = (x y - y + 1)/(x y)`, `b = r s (r - 1)`, `c = s (r - 1)`.
The example for `(d, p) = (22, 67)` is a point of order 67 on a twist of `y^2 = x^3 + 1` (see `degree22/make_cm67.py`).
