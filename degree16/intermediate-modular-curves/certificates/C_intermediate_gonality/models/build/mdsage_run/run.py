"""Enumerate strict X_Delta(N), N <= 50, and build canonical models with MD Sage.

Usage (Sage's Python, MD Sage on PYTHONPATH):
    python run.py --mdsage /path/to/mdsage --out results --workers 8

MD Sage calls: intermediate_modular_groups, vanishing_quadratic_forms,
subhyperelliptic_primes, trigonal_or_plane_quintic_primes.
Models use MD Sage's LLL option (small coefficients).
Independent check added here: every quadric vanishes on the cusp-form basis
to precision floor(4*index/12)+2, beyond the Sturm bound for weight 4.
"""
import argparse, json, os, sys, time
from multiprocessing import Pool


def work(task):
    N, gens = task
    import sage.all as S
    from mdsage import (vanishing_quadratic_forms, subhyperelliptic_primes,
                        trigonal_or_plane_quintic_primes)
    G = S.GammaH(N, gens)
    delta = sorted(int(h) for h in G._list_of_elements_in_H())
    g = int(G.genus())
    rec = dict(N=N, gens=[int(x) for x in gens], delta=delta, order=len(delta),
               index=int(G.projective_index()), genus=g, cusps=len(G.cusps()))
    t = time.time()
    if g <= 2:
        rec["model"] = "none (genus <= 2)"
        return rec
    hyp = subhyperelliptic_primes(G)
    rec["subhyperelliptic_primes"] = [int(p) for p in hyp]
    if hyp == [0]:
        rec["model"] = "none (hyperelliptic over Q)"
        return rec
    if g <= 4:
        rec["model"] = "none (genus 3 or 4: quadrics do not cut out the curve)"
        return rec
    tri = trigonal_or_plane_quintic_primes(G)
    rec["trigonal_or_plane_quintic_primes"] = [int(p) for p in tri]
    if tri == [0]:
        rec["model"] = "none (trigonal over Q)"
        return rec
    Q = vanishing_quadratic_forms(G, minimize_strategy="LLL")
    rec["quadrics"] = len(Q)
    rec["quadrics_expected"] = (g - 2) * (g - 3) // 2
    # Sturm-bound check: products of two weight-2 forms are weight-4 forms on G.
    prec = (4 * rec["index"]) // 12 + 2
    basis = [f.qexp(prec) for f in S.CuspForms(G, 2).integral_basis()]
    R = Q[0].parent()
    ok = all(q(*basis).truncate(prec) == 0 for q in Q)
    rec["sturm_check_precision"] = prec
    rec["sturm_check"] = bool(ok)
    rec["model"] = "quadrics"
    rec["equations"] = [str(q) for q in Q]
    rec["seconds"] = round(time.time() - t, 2)
    return rec


def tasks(Nmax):
    import sage.all as S
    from mdsage import intermediate_modular_groups
    out = []
    for N in range(2, Nmax + 1):
        phi = int(S.euler_phi(N))
        for G in intermediate_modular_groups(N):
            H = G._list_of_elements_in_H()
            if len(H) in (min(2, phi), phi):  # drop {+-1} (X1) and all units (X0)
                continue
            out.append((N, [int(x) for x in G._generators_for_H()]))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mdsage", required=True)
    ap.add_argument("--out", default="results")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--nmax", type=int, default=50)
    a = ap.parse_args()
    sys.path.insert(0, a.mdsage)
    os.environ["PYTHONPATH"] = a.mdsage + os.pathsep + os.environ.get("PYTHONPATH", "")
    os.makedirs(a.out, exist_ok=True)
    T = tasks(a.nmax)
    print(f"{len(T)} strict curves with N <= {a.nmax}", flush=True)
    T.sort(key=lambda t: -t[0])  # large levels first
    recs = []
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(work, T):
            recs.append(r)
            print(f"N={r['N']} gens={r['gens']} g={r['genus']} model={r['model']}"
                  + (f" quadrics={r['quadrics']}/{r['quadrics_expected']} sturm={r['sturm_check']}"
                     if r['model'] == 'quadrics' else ""), flush=True)
    recs.sort(key=lambda r: (r["N"], r["order"], r["delta"]))
    json.dump(recs, open(os.path.join(a.out, "curves.json"), "w"), indent=1)
    print("DONE", flush=True)
