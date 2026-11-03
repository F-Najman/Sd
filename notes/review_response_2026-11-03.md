# Response to the review of 3 November 2026

Review: `~/Documents/Codex/2026-10-28/on-this-computer-there-are-a/outputs/Sd_paper_review_20261103.txt`
(of the repository at a2eb87b, links pinned to 2f92a01). Every point was checked against the paper, the scripts,
their logs and the ledgers before acting. At the same time the paper was restructured following the author's
instructions of 2 and 3 November 2026 (self-contained lemmas, no running hypotheses); see the end of this note.
Statement numbers below are those of the revised paper.

## Review points

1. **Operator at 103/131 (Prop. 6.14) and in the supersingular case at 127 (Prop. 6.17).** Adopted. The paper wrote
   `T_3 - <3> - 3`, which in the paper's convention does not kill the rational cuspidal torsion: with `A_3 c = 0` one
   gets `(T_3 - <3> - 3)c = 2(<3> - 1)c`, and the review's divisor of positive degree 8 is not principal as the
   gonality of the quotient exceeds 8. Now `A_q`.
   The review's reading of the code was not right, however. The code's diamond matrix is the matrix of the inverse
   diamond operator in the paper's notation (certified as `GLOBAL_POINT_DIAMOND2_INVERSE` in every `full*/build.m`,
   e.g. `audit11/full103/build.m:63-66`), and modulo 2 the code's `T_2` is the Cartier operator, which is
   `T_2^* <2>^{*-1}` by Eichler-Shimura. So the code's `T - D^k - q` is `A_q` and its `T - 1 - q D^k` is `B_q`, both up
   to a diamond operator. The stored matrices are therefore those of `A_q` directly, for all `q` (this is also what
   makes the `q = 2` computations at 113 and 127, `degree20/relative113_ordinary.m` and `degree17/relative127.m`,
   valid). This agrees with the original account (`proofs/S21_proof.txt`, around line 440: "The first also handles the
   finite rational image"). Section 7 of the paper now states the convention.
2. **Normalization in the relative formal immersion argument.** Adopted: new Lemma 2.13 requires `f_{t,d}` to
   vanish on `L`, and every application says why (`t` kills `pi^*J_Y`, and `t[R + pi^*E_0 - d c_0] = 0` because
   `h - 1` kills the pullbacks and `A_q` kills rational cuspidal divisors, or `B_q A_q` kills all cuspidal divisors).
3. **Operator at 113.** Adopted. The code (`degree22/relative113_nc.m`, log: `q = 2, 3`) uses the two Eisenstein
   factors at the same `q`. The paper now defines `B_q = T_q - <q> - q`, proves that `A_q` kills the rational cusps
   and `B_q` the other cusps as divisors (Lemma 2.5 c)), and writes `(h_8 - 1) B_q A_q`, as also at 89 and 127.
   Link to `degree22/generic113_mixed_sieve.py` added in Prop. 5.3.
4. **Reproducibility.** Adopted: link `degree22/verify_large_simd.py` instead of `verify_large.py` (paper and
   README); `degree22/verify_final.py` named in the paper and the README; the README now lists the absolute paths in
   the scripts (the workspace, `mdmagma` as a submodule of `F-Najman/nonic-torsion` at `d1c019c`, the folder
   `common/` of that repository, and the census website data for the searches of explicit points). Not done: a
   portable replay wrapper.
5. **Small corrections.** Adopted. `76185` is the number of new source orbits of degree at most 22 at all 18 primes
   (73546 of degree 22; the 2639 of smaller degree are all in the new model at 163); without 163 there are 71224,
   all of degree 22. Lemma 4.1 is now stated for `M` an odd prime with `M > m` (all moduli in Table 2 are such).
6. **Stronger gonality bound.** Adopted for 163 and 173 at `d = 22`: `(163^2-1)/192 = 138.375 > 132 = 6*22` and
   `(173^2-1)/192 = 155.875 > 154 = 7*22`, while the weaker bound gives 131.75 and 148.4. The campaign had tried the
   argument for 163 with the weaker bound (`degree22/STATE.txt:35`). Table 3 rows extended, the row `(173,4,2,6,22)`
   deleted, 163 removed from Table 4 for `d = 22`. Hence 501 types at 17 primes (was 514 at 18), 129638 certificates
   (134762 minus the 5124 at 163) and largest curve `X_1(139)` of genus 737. `degree22/full163/` and
   `degree22/anti173.m` remain as unused extra checks (Section 7, README).
   Not adopted: the optional extensions of other rows (103 at d=11, 109 at d=12, 113 at d=13, 137 at d=19, 139 at
   d=20). Each of these curves is needed in other degrees anyway, so no computation would drop out, while several
   case ranges in the tables and propositions, and their agreement with the ledgers, would change.

## Added independently of the review

- Good reduction at primes `q != p` of the quotients `X_H` of positive genus (used for `#H` even at 53, 97 and 193):
  Liu-Lorenzini, Compositio 118 (1999), Cor. 4.10, as in the degree 6-9 paper.
- The constant `C = 2^19/325` renamed `kappa` (C is the cuspidal divisor), the Pade certificate `A/C` renamed
  `phi/psi`.

## Restructuring (author's instructions of 2 and 3 November 2026)

- No running hypotheses. The notation `Z, C', C, c` and "pullback from `X_H`" is defined in Section 2.2, and every
  statement carries its hypotheses ("Let D be the trace divisor of a point of order p over a number field of
  degree d ...").
- New or separated lemmas: Silverberg (2.1); a stabilizer lemma for any curve with an automorphism (2.8), used on
  the quotients at 61, 89 and 97; Lemmas 2.4 and 2.5 for `X_H`; Lemma 2.13 (relative); 4.4 (the 2-adic input of
  Prop. 4.5); 4.14 (odd order at 163, 167, 181); 4.16 (gonality of `X_1(127)/<2>`); 6.1 (37); 6.7 (61, now before
  Prop. 6.8); 6.9 (73); 6.12 (97). Prop. 4.15 split into 4.15, 4.17 (127) and 4.18 (193); the case `Z = 0` at 53
  moved into Prop. 6.14.

## Independent check

A separate agent compared the old and new versions and the review (no files edited). It found no mathematical error
and no lost content, verified the new lemmas, the cusp formulas, all the normalizations and the new numbers against
the ledgers, and found the code-convention point in item 1 above. Its smaller findings were all applied: the
abstract still said `p <= 163`; `37 notin S(3)` was missing at 37; "43 is not strange" was missing at 43; the odd
order of `<2>` at 89; the tuple form of the formal immersion criterion; Prop. 6.14 belongs to the excluding
propositions in the proof of Theorem 1.1; `verify_final.py` in Section 7; "`f_{t,d}` vanishes on L". Not verified
by it: the numbering of Corollary 4.10 in Liu-Lorenzini (checked in the PDF for the degree 6-9 paper).
