"""Upper bounds by pullback:  gon_Q(X) <= deg(X -> Y) * gon_Q(Y).

For M | N and Delta mod M contained in Delta', the forgetful map X_Delta(N) -> X_Delta'(M),
(E, P) -> (E, (N/M) P), is defined over Q; its degree is the ratio of the indices.
The targets Y are all curves X_Delta'(M) with M <= 50, including X0(M) and X1(M). Only
targets with a self-evident Q-rational pencil are used. Each has the rational cusp at infinity:
    genus 0             -> gon_Q(Y) = 1
    genus 1 or 2        -> gon_Q(Y) <= 2
    hyperelliptic       -> gon_Q(Y) <= 2   (the canonical map is 2:1 onto a conic with a rational point)
    genus 3, not hyp.   -> gon_Q(Y) <= 3   (projection from the rational cusp)
Hyperellipticity is decided by MD Sage's subhyperelliptic_primes (output [0]).
If no such target is sharp, targets with a published gonality are also used (cited_gonalities.json:
Orlic Thm 1.2 for strict N <= 40, Derickx-van Hoeij for X1(N), N <= 40, Najman-Orlic for X0(N)).
A curve's own self-evident bound counts as the degree-1 case.

Run with Sage's Python:  python pullback.py  (MD Sage from ../../../third_party/mdsage)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../third_party/mdsage"))
import sage.all as S
from mdsage import intermediate_modular_groups, subhyperelliptic_primes

NMAX = 50
curves = []
for M in range(1, NMAX + 1):
    for G in intermediate_modular_groups(M):
        D = frozenset(int(a) for a in G._list_of_elements_in_H()) if M > 1 else frozenset([0])
        curves.append(dict(N=M, D=D, index=int(G.projective_index()), g=int(G.genus()), G=G))


def evident(c):
    """(bound, reason) for a self-evident upper bound on gon_Q, or None."""
    if c["g"] == 0:
        return 1, "genus 0"
    if c["g"] <= 2:
        return 2, f"genus {c['g']}"
    if c["g"] <= 10 and subhyperelliptic_primes(c["G"]) == [0]:
        return 2, "hyperelliptic"
    if c["g"] == 3:
        return 3, "genus 3, not hyperelliptic"
    return None


for c in curves:
    c["evident"] = evident(c)
cited = {(x["N"], frozenset(x["Delta"])): x for x in json.load(open(os.path.join(HERE, "cited_gonalities.json")))}
for c in curves:
    x = cited.get((c["N"], c["D"]))
    c["cited"] = (x["gon"], x["source"]) if x else None


def maps_to(c, t):
    M, N = t["N"], c["N"]
    if N % M or c["index"] % t["index"] or t["index"] >= c["index"]:
        return False
    return M == 1 or {a % M for a in c["D"]} <= t["D"]


def candidates(c):
    """(bound, is_cited, record) for c itself and every target of a map from c."""
    for t in [c] + [t for t in curves if maps_to(c, t)]:
        deg = c["index"] // t["index"]
        for kind in ("evident", "cited"):
            if t[kind]:
                yield (deg * t[kind][0], kind == "cited",
                       dict(bound=deg * t[kind][0], degree=deg, target_N=t["N"], target_Delta=sorted(t["D"]),
                            target_genus=t["g"], target_reason=t[kind][1], cited=(kind == "cited")))


labels = json.load(open(os.path.join(HERE, "../../../data/labels.json")))
out = []
for c in curves:
    phi = int(S.euler_phi(c["N"]))
    if c["N"] <= 40 or len(c["D"]) in (min(2, phi), phi):
        continue  # only strict curves with 41 <= N <= 50
    best = min(candidates(c), key=lambda x: (x[0], x[1], -x[2]["target_N"]))[2]
    key = f"{c['N']}:{','.join(map(str, sorted(c['D'])))}"
    out.append(dict(label=labels[key], N=c["N"], Delta=sorted(c["D"]), genus=c["g"], pullback=best))

out.sort(key=lambda r: (r["N"], r["label"]))
json.dump(out, open(os.path.join(HERE, "pullback.json"), "w"), indent=1)
for r in out:
    p = r["pullback"]
    print(f"{r['label']:16} g={r['genus']:>2}  pullback <= {p['bound']:>2}  "
          f"(degree {p['degree']} to level {p['target_N']}, genus {p['target_genus']}, {p['target_reason']})")
print("cited targets used:", sorted({r["pullback"]["target_reason"] + f" [level {r['pullback']['target_N']}]" for r in out if r["pullback"]["cited"]}))
