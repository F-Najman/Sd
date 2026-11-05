# Check of all the references (3 November 2026)

All 42 entries of `paper/refs.bib` and every citation in the paper were checked against the sources. Each entry was
checked for its bibliographic data, against Crossref, zbMATH, MathSciNet, Numdam or the publisher, and each
pinpoint (theorem, section, table) against the text of the cited work. Afterwards 2 entries were added, so there
are now 44. The work was split into six groups (DKSS; Derickx-Stoll and the software; Parent, Kamienny, Merel;
Mazur, Katz, Kato, Abramovich; the gonality and quadratic-points papers; the rest), and every reported error was
checked again in the source before the paper was changed. No computation was rerun.

## Errors found and corrected

Mathematical attributions:

1. Lemma 2.5 a), `l = 2` (02_notation). The proof cited only Katz [Appendix], which covers odd `l` only
   (`e < p - 1`). The `l = 2` statement (the kernel of reduction on `A(Q)_tors` is killed by 2) is now cited as
   Parent, AIF 2000, Lemme 1.7 (p. 729): "si l = 2 et P != 0, alors P engendre un mu_2". It is applied to the Néron
   model over `Z_(2)`. The plan had been to cite "Proposition 2.4" of that paper, but there is no such proposition:
   2.4 is the subsection "Preuve de 1.8". The general form of Lemme 1.7, over an unramified discrete valuation ring,
   is Proposition 2.3.
2. Lemma 2.5 c), cusp formulas (02_notation). These were cited as Derickx-Stoll [Proposition 2.1], which is about
   torsion killed by `T_q - <q> - q` and contains nothing on cusps. The citation is now:
   - the remark after DKSS Proposition 2.4 (p. 279: rational cusps killed by `T_q - <q> - q`, the others by
     `T_q - q<q> - 1`);
   - Parent 2000, Sections 1.5 (the `mu_p` model) and 2.4 (the formulas);
   - the Atkin-Lehner translation (discussion after DKSS Lemma 8.6), which holds up to a diamond operator.
3. Proposition 2.6 a), second bound (02_notation). Abramovich's Theorem 0.1 states only `gon >= (7/800) D_Gamma`.
   The bound `gon_C >= (lambda/24) D_Gamma` (for `lambda <= 1/4` below the non-zero spectrum) comes from its proof
   (Sections 1.5-1.7). The constant `1/96` under Selberg's conjecture is in Section 0.2, and also in Derickx-Stoll,
   Remark 3.4. The proof is now written out:
   - Derickx-Stoll's Theorem 3.3 uses `lambda = 975/4096`;
   - Booker-Lee-Strömbergsson, Theorem 1.1, proves Selberg's conjecture for `Gamma_1(N)`, `N <= 880` (any `N`, all
     even characters);
   - this gives `lambda = 1/4`.
4. Section 4 (04_global). "See the proof of [DKSS, Corollary 6.6]" is now "the proofs of Corollaries 6.4 and 6.6".
   The inclusion `(T_2 - 3)Te in H_1` is in the proof of 6.4. The matrix entries are intersection numbers only
   "up to sign", because DKSS's winding element is `pi(-{0,oo})`.
5. Silverberg's bound (02_notation). The form used (`delta = 1/2`) is not in Silverberg 1988. It is now cited as
   "the sharper form stated in [PY, Section 1] and [BC, Theorem 1.1]". BC is the new entry Bourdon-Clark, Pacific J.
   Math. 305 (2020), 43-88.
6. Sutherland's models (03_lower, Section 7). The `(x,y)` models of `X_1(p)` for `p >= 31`, and the map to Tate
   normal form, are on his web page "Defining equations for X_1(N)", not in the Math. Comp. paper, whose tables stop
   at `N = 30`. New entry `sutherlandX1`.
7. Introduction:
   - "Kamienny, building on work of Kenku and Momose, proved `S(2) = Primes(13)`" over-credited Kenku-Momose. They
     treat the orders built from 2, ..., 13 only. Rephrased.
   - Kamienny-Mazur define `S(d)` for degree `<= d` (p. 81). The exact-degree `S(d)` of the paper is DKSS
     Definition 1.1, which is now cited, with a parenthetical on KM's version.
   - Derickx-Stoll's Corollary 7.8 assumes sparsity of strange *newforms*, not characters.
8. Proposition 6.17, `p = 127` (06_exceptions). [AKMNOV, Table 16] lists only the quadratic points. The rational
   points are now covered by Mazur [Theorem 1], as was already done at 113, where the citation was also added.
9. `mdmagma` has moved to `github.com/nt-lib/mdmagma`. It is credited to Derickx and Sutherland (bib, Section 7,
   README); revision `d1c019c` exists there.

Bibliographic:

- `siam.bst` does not print the `number` field of an `@article`. Entries that had only `number` printed an empty
  volume. Fixed:
  - `mazur` (vol. 47);
  - `kato` (Astérisque 295, pp. 117-290);
  - `abramovich` (IMRN 1996, no. 20);
  - `KamiennyMazur` (Astérisque 228);
  - `khawaja` ("Paper No. 48" moved from `pages` to `note`).
- Other bibliographic corrections:
  - `BLS`: pages 1067-1134 added;
  - `mazur78`: "With an appendix by D. Goldfeld";
  - `parentformal`: primary DOI `10.1515/crll.1999.506.85` (the old one is an alias);
  - `parent2003` and `ARS`: DOIs added;
  - `Box`: en dash in the title.
- Pinpoints added:
  - DKSS Definition 1.1 and Lemma 5.5;
  - Mazur 1978, Theorem 1 (five bare citations);
  - Najman-Vukorepa, Theorem 1.1;
  - Siksek, Section 4;
  - Derickx-Stoll, Proposition 5.2 with Table 2.
- Wording made exact:
  - DKSS Proposition 5.3 gives only "if";
  - DKSS Lemma 4.2 is over `Z_(l)`, ours over `W` ("a slight generalization");
  - Derickx-Stoll Remark 4.4.

## Checked and correct

- DKSS: 22 of 23 sites were already correct (published MSP version).
- Derickx-Stoll: 19 of 21 were correct. Only v1 exists (arXiv 2505.14109, submitted), so its numbering is final.
- Correct as cited:
  - Kato, Corollary 14.3;
  - Mazur-Swinnerton-Dyer, Section 5;
  - Liu-Lorenzini, Corollary 4.10 (verbatim);
  - Kamienny, Theorem 3.1;
  - Parent 2003, Theorem 5.1;
  - Khawaja, Theorem 1.2;
  - Jeon, Theorem 3.2;
  - Varivoda, Theorem D (Hexagon);
  - van Hoeij's data (`N = 43`);
  - Agashe-Ribet-Stein, Section 4.4;
  - Abbes-Ullmo, Appendix A Theorem A.1 (Raynaud) and Lemma 2.1;
  - AKMNOV, Tables 14 and 16;
  - Box, Section 4.7 (11 `j`-invariants: 3 quadratic non-CM, 8 rational CM);
  - Derickx-van Hoeij, Table 1 and Section 2;
  - DEHMZ, DN, N5, N69, Merel.

Addendum of 5 November 2026: **Parent, Crelle 506 (1999)** (`parentformal`) was checked in the published text
(the PDF supplied by the author). All three citations (04_global) are correct:
- Proposition 1.9 (p. 88, proved in Section 5) is the independence of `T_i{0,oo}`, `1 <= i <= sd`, for
  `p^n >= C_p^2 (s_p d)^6`, where `C_p^2 = 65` for `p != 2` and `C_2^2 = 129` (p. 109). This gives the
  `65(4d)^6` of the remark after Corollary 4.7.
- Theorem 4.18 (p. 108) is Kamienny's criterion, with Oesterlé's condition (3).
- Section 4.12 (pp. 105-108), "Preuve de la proposition 'critère de Kamienny'", contains Lemme 4.16
  (Kamienny): `f_d^*(omega) = a_1 dsigma_1 - a_2 dsigma_2 + ... + (-1)^{d-1} a_d dsigma_d`, and Corollaire 4.17.
  The citation of the cotangent map was sharpened from [Section 4.12] to [Lemma 4.16].

The published Lemme 4.14 is the specialization lemma (`v(l) < l - 1`), which matches the citation "lemme 4.14 de
[22]" in Parent 2000.

## UNVERIFIED

These could not be checked in the published text, because of paywalls or bot checks, which were not bypassed:

- **Abramovich, IMRN 1996**: Theorem 0.1 and Section 0.2 are the numbers of arXiv alg-geom/9609012v1.
- **Numbering in the published versions**: Booker-Lee-Strömbergsson Theorem 1.1, AKMNOV Tables 14 and 16, Box
  Section 4.7, and Derickx-van Hoeij Table 1 and Section 2. All arXiv versions agree, and for AKMNOV so does the
  accepted manuscript. Pan-Yang, Section 1 (arXiv v1).
- **Hindry-Silverman (Acta Arith. 88)**: the full text was not reachable. The claim is cited together with Jeon,
  which was verified, and Najman-Orlić credits it to them as well.
- **Silverberg 1992** (Contemp. Math. 133): Pan-Yang credit the sharper form to it. Not checked, and not cited.
- **Merel**: only the zbMATH review and DKSS were read, not the paper itself.
- **N10**: the title is as given by the author.
- **DN**: volume 829 and pages 123-156 are from zbMATH only (Crossref has the online-first record).

Noted, not affecting the paper: the header of AKMNOV Table 14 says `J_0(127)(Q)`, which is a misprint for
`J_0(113)(Q)`. Parent's Proposition 1.8 needs the modification that DKSS describe (which operator kills the rational
torsion), but the cusp formulas of his Section 2.4 that we cite are not affected.
