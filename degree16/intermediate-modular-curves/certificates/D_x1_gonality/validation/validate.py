"""Validation: on small curves, the two-phase search (phase1 + phase2) must give exactly the gonality over F_p
computed by CurveArith's unmodified CAGonality. Usage: python3 validate.py [X1_29:5 ...]"""
import json, pathlib, subprocess, sys
here = pathlib.Path(__file__).resolve().parent
root = here.parent
cases = [(n, int(p)) for n, p in (a.split(":") for a in sys.argv[1:])] or [("X1_26", 3), ("X1_26", 5), ("X1_26", 7), ("X1_29", 2), ("X1_29", 3), ("X1_29", 5)]
ok = True
for name, p in cases:
    model = (root / "models" / f"{name}.txt").resolve()
    # CurveArith's own answer.
    drv = here / f"ca_{name}_{p}.m"
    drv.write_text(f'SetQuitOnError(true); AttachSpec("{root.parents[1]}/third_party/CurveArith/CurveArith.spec");\n'
                   f'A<x, y> := PolynomialRing(Rationals(), 2);\nload "{model}";\n'
                   f'R<t> := FunctionField(GF({p})); S<Y> := PolynomialRing(R);\n'
                   f'den := LCM([Denominator(c) : c in Coefficients(X)]);\n'
                   f'FF := FunctionField(Evaluate(ChangeRing(den * X, GF({p})), [t, Y]));\n'
                   f'printf "CAGONALITY %o\\n", CAGonality(FF); quit;\n')
    out = subprocess.run(["magma", "-b", str(drv)], capture_output=True, text=True).stdout
    gca = int(out.split("CAGONALITY")[1].split()[0])
    # Two-phase search: d = gca - 1 must be false, d = gca must be true.
    answers = {}
    for d in (gca - 1, gca):
        o = here / f"run_{name}_{p}_{d}"
        subprocess.run([sys.executable, str(root / "phase1/run_phase1.py"), str(model), str(p), str(d), "2", str(o)],
                       check=True, capture_output=True)
        r = json.loads(subprocess.run([str(root / "phase2/search"), str(o / "curve.ffjets"), "--degree", str(d)],
                                      capture_output=True, text=True).stdout)
        answers[d] = (r["answer"], r["complete"])
    good = answers[gca - 1] == (False, True) and answers[gca] == (True, True)
    ok &= good
    print(f"{name} p={p}: CAGonality={gca}  phase2(d={gca-1})={answers[gca-1]}  phase2(d={gca})={answers[gca]}  {'PASS' if good else 'FAIL'}")
print("ALL PASS" if ok else "SOME FAILED")
