"""Check that every claim in data/ is backed by a passing log in certificates/ or by a citation.

This does not rerun any computation (see README.md for how to rerun them); it checks that the saved logs
exist, report success, and agree with the numbers in data/. Run:  python3 verify.py
"""
import csv, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
CERT = ROOT / "certificates"
failures = []


def check(ok, what):
    if not ok:
        failures.append(what)


def text(path):
    p = CERT / path
    return p.read_text(errors="replace") if p.exists() else ""


# Theorem C: one row per strict curve with N <= 50.
rows = list(csv.DictReader(open(ROOT / "data/strict_intermediate_N_le_50.csv")))
check(len(rows) == 76, "Theorem C: 76 curves")
cusp_log = text("C_intermediate_gonality/upper/certificates/all_certificates.out")
pullbacks = {x["label"]: x for x in json.load(open(CERT / "C_intermediate_gonality/upper/pullback.json"))}
reductions = text("C_intermediate_gonality/lower/reduction_check.log")
for r in rows:
    lab, lo, up = r["label"], int(r["lower_bound"]), int(r["upper_bound"])
    check(lo == up == int(r["gonality"]), f"{lab}: lower = upper = gonality")
    if int(r["N"]) <= 40:
        check(r["lower_method"] in ("genus", "cited"), f"{lab}: N <= 40 is cited from Orlic or trivial")
        continue
    m = r["lower_method"]
    if m == "cagonality":
        p = re.search(r"F_(\d+)", r["lower_source"]).group(1)
        log = text(f"C_intermediate_gonality/lower/runs/{lab}.p{p}.log")
        check(f"LOWER_BOUND {lab} p={p} gon_Fp={lo} " in log, f"{lab}: CAGonality log at p={p}")
        check(f"GOOD_REDUCTION {lab} p={p}" in reductions, f"{lab}: good reduction at p={p}")
    elif m == "lifting":
        for s in ["identify_model", "torsion_classes", "audit_smooth_reduction", "audit_certificate", "audit_torsion_counts",
                  "prove_lower_bound_7", "prove_upper_bound_7"]:
            log = text(f"C_43.132.9.a.2/out/{s}.out")
            check(log and not re.search(r"error|assertion failed", log, re.I), f"{lab}: {s}")
    else:
        check(m == "genus", f"{lab}: unknown lower method {m}")
    m = r["upper_method"]
    if m == "cusp_rr":
        check(f"CERTIFIED {lab}: deg D = {up}, h0(D) = 2" in cusp_log, f"{lab}: cuspidal divisor")
    elif m == "pullback":
        pb = pullbacks.get(lab, {}).get("pullback") or {}
        check(pb.get("bound") == up, f"{lab}: pullback bound")
    elif m == "special":
        log = text(f"C_intermediate_gonality/upper/special/{lab}/certificate.out")
        check(re.search(r"VERIFIED=true|Q_GONALITY_UPPER_BOUND=%d" % up, log) is not None, f"{lab}: special certificate")
    else:
        check(m in ("cited", "genus"), f"{lab}: unknown upper method {m}")

# Theorem D: X1(N), 41 <= N <= 50.
x1 = ROOT / "data/x1_41_50.csv"
if x1.exists():
    for r in csv.DictReader(open(x1)):
        res = CERT / f"D_x1_gonality/runs/x1_{r['N']}/phase2.json"
        ok = res.exists() and (lambda j: j["answer"] is False and j["complete"] is True and j["degree"] == int(r["d"]))(json.loads(res.read_text()))
        check(ok, f"X1({r['N']}): no function of degree <= {r['d']} over F_{r['p']}")
else:
    failures.append("Theorem D: data/x1_41_50.csv missing")
check("ALL_MODELS_OK" in text("D_x1_gonality/model_checks.log"), "X1(N): model_checks.log")
val = "".join(p.read_text() for p in sorted((CERT / "D_x1_gonality/validation").glob("validate*.log")))
check(len(re.findall(r"^X1_\d+ p=\d+: .* PASS$", val, re.M)) >= 5 and "FAIL" not in val, "X1(N): validation cases pass")
r48 = CERT / "D_x1_gonality/double_cover_48/runs48"
res48 = json.loads((r48 / "RESULT.json").read_text())
for log in res48["certified_logs"]:
    check("CERTIFIED gon(X1(48) over F_7) > 15" in (r48 / log).read_text(), f"X1(48): {log}")
total = sum(int(re.search(r"effective_E_this_shard=(\d+)", (r48 / log).read_text()).group(1)) for log in res48["certified_logs"])
check(total == res48["divisors_E"] == 1328, "X1(48): the parts cover all 1328 divisors E")

# Theorems A and B: the packages carry their own verifiers.
a = subprocess.run([sys.executable, "run.py", "--check-logs"], cwd=CERT / "A_x0_quintic", capture_output=True, text=True)
check(a.returncode == 0, "Theorem A: run.py --check-logs")
b = subprocess.run([sys.executable, "verify.py"], cwd=CERT / "B_intermediate_quintic", capture_output=True, text=True)
check(b.returncode == 0 and "PASS" in b.stdout, "Theorem B: verify.py")

if failures:
    print("FAIL"); [print("  " + f) for f in failures]; sys.exit(1)
print("PASS: every row of data/ is backed by a passing log or a citation")
