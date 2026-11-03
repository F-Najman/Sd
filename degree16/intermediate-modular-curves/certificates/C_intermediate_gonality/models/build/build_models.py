"""Build ../ (the models/ folder) from the MD Sage run and the verified LMFDB labels.

Inputs:
    mdsage_run/results/curves.json  (MD Sage output)
    label_check/labels.json  (label per (N, Delta), verified by conjugacy)
Output:
    models/<label>.m   one Magma file per curve with a canonical model (genus >= 5)
    models/index.csv   all strict curves X_Delta(N), N <= 50
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..")   # the models/ folder
MDSAGE_COMMIT = "602242974e6edc01e7466c46949d40ff589a6fbf"

curves = json.load(open(os.path.join(HERE, "mdsage_run/results/curves.json")))
labels = json.load(open(os.path.join(HERE, "label_check/labels.json")))
os.makedirs(OUT, exist_ok=True)

REASON = {
    "none (genus <= 2)": "genus <= 2",
    "none (hyperelliptic over Q)": "hyperelliptic",
    "none (genus 3 or 4: quadrics do not cut out the curve)": "genus 3 or 4",
}


def pm_gens(r):
    """Canonical generators of Delta as <-1, g1, ...>: the fewest generators with 1 < g_i < N/2,
    and among those the lexicographically smallest list."""
    from itertools import combinations
    N, delta = r["N"], set(r["delta"])
    reps = sorted({min(a, N - a) for a in delta} - {1})

    def span(gs):
        S = {1, N - 1}
        while True:
            T = S | {(s * g) % N for s in S for g in gs}
            if T == S:
                return S
            S = T

    for k in range(len(reps) + 1):
        for gs in combinations(reps, k):
            if span(gs) == delta:
                return "<" + ",".join(["-1"] + [str(g) for g in gs]) + ">"
    raise ValueError(r)


def pm_elements(r):
    """Delta written as {±a, ±b, ...} with 1 <= a < N/2."""
    N = r["N"]
    reps = sorted({min(a, N - a) for a in r["delta"]})
    return "{" + ",".join(f"±{a}" for a in reps) + "}"


rows = []
for r in curves:
    key = f"{r['N']}:{','.join(map(str, r['delta']))}"
    label = labels[key]
    has_model = r["model"] == "quadrics"
    rows.append({
        "label": label, "N": r["N"], "Delta_generators": pm_gens(r),
        "Delta": pm_elements(r), "order_Delta": r["order"], "index": r["index"],
        "genus": r["genus"], "cusps": r["cusps"],
        "model": f"{label}.m" if has_model else "",
        "no_model_reason": "" if has_model else REASON[r["model"]],
    })
    if not has_model:
        continue
    g = r["genus"]
    vs = ",".join(f"x{i}" for i in range(g))
    eqs = ",\n  ".join(r["equations"])
    sage_gens = "[" + ", ".join(map(str, r["gens"])) + "]"
    text = f"""// X_Delta(N) for N = {r['N']}, Delta = {pm_gens(r)} = {pm_elements(r)}
// LMFDB label {label}; index {r['index']}, genus {g}, {r['cusps']} cusps.
//
// Canonical model: {len(r['equations'])} quadrics in P^{g-1} over Q, computed with MD Sage
// (github.com/koffie/mdsage, commit {MDSAGE_COMMIT[:7]}) as
//   vanishing_quadratic_forms(GammaH({r['N']}, {sage_gens}), minimize_strategy="LLL")
// sage-group: GammaH({r['N']}, {sage_gens})
// Coordinates x0, ..., x{g-1} are Sage's integral (echelon) basis of weight-2 cusp forms for
// GammaH({r['N']}, {sage_gens}): x0 vanishes to order 1 at infinity and x1, ..., x{g-1} to higher order,
// so the cusp at infinity is the rational point (1:0:...:0).

N := {r['N']};
Delta := {r['delta']};
g := {g};
P<{vs}> := ProjectiveSpace(Rationals(), {g - 1});
X := Curve(P, [
  {eqs}
]);
"""
    open(os.path.join(OUT, f"{label}.m"), "w").write(text)

rows.sort(key=lambda x: (x["N"], x["index"], x["label"]))
files = [x["model"] for x in rows if x["model"]]
with open(os.path.join(OUT, "check.m"), "w") as f:
    f.write("// Magma check of every model file: Hilbert polynomial (2g-2)t + 1-g of a canonical\n"
            "// curve of genus g, and the cusp at infinity (1:0:...:0) lies on the curve.\n"
            "// Run from this directory:  magma -b check.m\nSetQuitOnError(true);\n")
    for m in files:
        f.write(f'load "{m}"; I := Ideal(X); h := HilbertPolynomial(I); t := Parent(h).1;\n'
                f'assert h eq (2*g-2)*t + 1-g; pt := [1] cat [0 : i in [2..g]];\n'
                f'assert forall{{f : f in DefiningEquations(X) | Evaluate(f, pt) eq 0}};\n'
                f'printf "OK %o\\n", "{m}";\n')
    f.write(f'printf "ALL %o MODELS PASSED\\n", {len(files)}; quit;\n')
import shutil
shutil.copy(os.path.join(HERE, "check.sage"), os.path.join(OUT, "check.sage"))
with open(os.path.join(OUT, "index.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print(len(rows), "curves;", sum(1 for x in rows if x["model"]), "model files")
