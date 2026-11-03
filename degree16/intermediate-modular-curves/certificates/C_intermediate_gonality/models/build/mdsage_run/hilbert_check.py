"""Write a Magma script checking that each MD Sage quadric model has the
Hilbert polynomial (2g-2)t + 1-g of a canonical curve of genus g."""
import json, sys
recs = json.load(open(sys.argv[1]))
out = ['SetQuitOnError(true);']
for r in recs:
    if r.get("model") != "quadrics":
        continue
    g = r["genus"]
    vs = ",".join(f"x{i}" for i in range(g))
    eqs = ",".join(r["equations"])
    tag = f"N={r['N']} gens={r['gens']} g={g}"
    out.append(f'P<{vs}>:=ProjectiveSpace(Rationals(),{g-1}); R:=CoordinateRing(P);'
               f' I:=ideal<R|[{eqs}]>; h,d:=HilbertPolynomial(I); t:=Parent(h).1;'
               f' ok := h eq {2*g-2}*t+{1-g}; printf "HILBERT %o %o\\n", "{tag}", ok;'
               f' assert ok;')
out.append('print "ALL_HILBERT_CHECKS_PASSED"; quit;')
open(sys.argv[2], "w").write("\n".join(out) + "\n")
