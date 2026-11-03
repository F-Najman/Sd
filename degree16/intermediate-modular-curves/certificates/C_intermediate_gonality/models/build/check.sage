# Sage check of every model file (run from this directory:  sage check.sage).
# For each file: rebuild S_2(GammaH(N, gens)) with Sage, check that the basis is in echelon form
# (valuations at infinity strictly increasing, starting with 1), and that every quadric vanishes on it beyond the
# weight-4 Sturm bound floor(4*index/12). Needs only Sage (MD Sage is not required).
import glob, re
count = 0
for fn in sorted(glob.glob("*.m")):
    if fn == "check.m":
        continue
    s = open(fn).read()
    N, gens = re.search(r"sage-group: GammaH\((\d+), \[([\d, ]*)\]\)", s).groups()
    G = GammaH(int(N), [int(x) for x in gens.split(",") if x.strip()])
    g = int(re.search(r"\ng := (\d+);", s).group(1))
    body = re.search(r"Curve\(P, \[(.*)\]\);", s, re.S).group(1)
    R = PolynomialRing(QQ, g, names="x")
    quadrics = [R(q) for q in body.replace("\n", " ").split(",")]
    prec = floor(4 * G.projective_index() / 12) + 2
    basis = [f.qexp(prec) for f in CuspForms(G, 2).integral_basis()]
    assert len(basis) == g
    v = [f.valuation() for f in basis]
    assert v[0] == 1 and all(v[i] < v[i + 1] for i in range(g - 1))
    assert len(quadrics) == (g - 2) * (g - 3) // 2
    assert all(q(*basis).truncate(prec) == 0 for q in quadrics)
    count += 1
    print("OK", fn)
print("ALL", count, "MODELS PASSED")
