"""Run Phase 1 (phase1.m) for one curve in parallel shards, then merge the shards into the FFJETS
input of the Phase 2 search. Usage: python3 run_phase1.py MODEL p d SHARDS OUTDIR"""
import os, subprocess, sys, pathlib

model, p, d, shards, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), pathlib.Path(sys.argv[5]).resolve()
here = pathlib.Path(__file__).resolve().parent
out.mkdir(parents=True, exist_ok=True)
# Magma reads a script while it runs, so every run uses its own frozen copy of phase1.m.
import shutil
if not os.environ.get("MERGE_ONLY"):
    shutil.copy(here / "phase1.m", out / "phase1.m")
procs = []
# MERGE_ONLY=1: the shard outputs already exist (e.g. a shard was rerun on its own); only merge them.
for s in ([] if os.environ.get("MERGE_ONLY") else range(shards)):
    drv = out / f"shard_{s}.m"
    drv.write_text(f'A<x, y> := PolynomialRing(Rationals(), 2);\nload "{pathlib.Path(model).resolve()}";\n'
                   f'p := {p}; d := {d}; Shard := {s}; Shards := {shards}; Out := "{(out / f"shard_{s}.txt").resolve()}";\n'
                   + (f'MemGB := {os.environ["MEMGB"]};\n' if os.environ.get("MEMGB") else '')
                   + f'load "{out / "phase1.m"}";\n')
    procs.append(subprocess.Popen(["magma", "-b", str(drv)], cwd=here, stdout=open(out / f"shard_{s}.log", "w"), stderr=subprocess.STDOUT))
codes = [q.wait() for q in procs]
assert all("PHASE1_DONE" in (out / f"shard_{s}.log").read_text() for s in range(shards)), "a shard failed"

# Merge. All shards must agree on the curve, the place counts and the basis of differentials; the shards'
# places of each degree must add up to the count of that degree (they are disjoint by construction).
blocks, headers, checks = {}, set(), []
for s in range(shards):
    lines = (out / f"shard_{s}.txt").read_text().split("\n")
    headers.add(tuple(l.rsplit(" ", 1)[0] if l.startswith("PHASE1") else l for l in lines[:3]))
    i = 3
    while lines[i] != "END":
        if lines[i].startswith("CHECK"):
            checks.append((s, lines[i].split())); i += 1; continue
        _, deg, jj, prec, key = lines[i].split()
        deg, jj, prec = int(deg), int(jj), int(prec)
        assert (int(key) * 2654435761 % 2**32) * shards // 2**32 == s
        blocks[(deg, s, jj)] = (prec, lines[i + 1:i + 1 + prec * deg])
        i += 1 + prec * deg
assert len(headers) == 1, "shards disagree on the curve, the places or the basis"
(h1, counts, _), = headers
_, p_, g, d_, rational, n, maxdeg = h1.split()
counts = [int(c) for c in counts.split()[1:]]
for deg in range(1, len(counts) + 1):
    assert sum(1 for k in blocks if k[0] == deg) == counts[deg - 1], f"degree {deg}: shards do not cover all places"
# Global indices: by degree, then shard, then index within the shard.
order = sorted(blocks)
index = {k: i for i, k in enumerate(order)}
res = [f"FFJETS 1 {p_} 1 {p_} {g} {d_} {rational} {maxdeg} {sum(counts)}", "POLY 0 1",
       "COUNTS " + " ".join(map(str, counts))]
for k in order:
    prec, rows = blocks[k]
    res.append(f"PLACE {index[k]} {k[0]} {prec}")
    res += rows
for s, c in checks:
    terms = c[3:]
    triples = sorted((index[(int(terms[3*t]), s, int(terms[3*t+1]))], int(terms[3*t+2])) for t in range(len(terms) // 3))
    res.append(f"CHECK {c[1]} {c[2]} " + " ".join(f"{a} {m}" for a, m in triples))
res.append("END")
(out / "curve.ffjets").write_text("\n".join(res) + "\n")
print(f"merged {len(order)} places and {len(checks)} Magma checks from {shards} shards into {out / 'curve.ffjets'}")
