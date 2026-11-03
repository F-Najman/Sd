# An independent proof of S(9) = Primes(31)

These folders are copied from the repository of the classification of torsion over nonic fields
(<https://github.com/F-Najman/nonic-torsion>, commit `8b895ea`), where they prove that a prime `p` is the order of a
point on an elliptic curve over a number field of degree 9 if and only if `p <= 31`. In the paper this is used only as
an independent check of the case `d = 9` (Section 7), except for `P37/rational_isogeny_fibers.m`, which is used in
Proposition 6.1, and `realizations/verify_nonic_examples.m`, which verifies the examples of order 29 and 31.

| Folder | Contents |
|---|---|
| `prime_bound/` | Oesterlé's bound, Derickx–Stoll Corollary 7.5 for `127 <= p < 19965`, Proposition 4.1 for `103 <= p <= 113`, formal immersion at the cusps for `37 <= p <= 101` |
| `P41_P47_P59/`, `P43_P53_P61/`, `P37/`, `P67/`, `P71/`, `P73/`, `P79_P89/`, `P83/` | the local arguments at each prime, partly on quotients of `X_1(p)` |
| `realizations/` | the nonic examples, including points of order 29 and 31 |
| `common/` | shared code (`finite_field_prime_orders.m`, `prime_good_branches*.m`, `rational_two_diamond.m`, ...) and logs |

The scripts use the folder layout of the nonic repository (`AttachSpec` of `mdmagma` and relative paths). The 15 data
files larger than 1 MB are not copied here; they are in the nonic repository:
`P67/data/quotient45/*`, `P71/data/special7_two_matrices.m`, `P73/data/deck/N73_matrices.m`,
`P79_P89/data/P89/quotient27/*`, `P83/data/FI_rows.txt`, `P83/data/canonical_units/*`, `P41_P47_P59/data/P59/FI_rows.txt`.
