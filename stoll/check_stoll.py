"""Compare the strange characters modulo p < 400000 of M. Stoll with the proof of Proposition 4.13.

Usage, from the root of the repository:

    python3 stoll/check_stoll.py strange_characters_400000.txt > stoll/check_stoll.log

The table (private communication from M. Stoll, 4 November 2026) has one line "p order strdim"
per prime p and order n of its strange characters, and lines starting with # are comments.
It is not included in this repository; its SHA256 is printed below.

The script checks:
1. below 10^5 the table agrees with Table 2 of Derickx-Stoll (audit11/derickx_stoll_table2.txt);
2. for every prime 10^5 < p < 4*10^5, h(p) = (p-1)/(2 str(p)) > 22, where str(p) is the lcm of
   the orders of the strange characters (the order of the group they generate), and
   p^2 > kappa*22+1 with kappa = 2^19/325, and p > 3*22+1; so by Corollary 7.5 of
   Derickx-Stoll (Proposition 4.8 of the paper) p is not in S(d) for any d <= 22;
3. none of the character orders n, for which the proof of Proposition 4.13 shows that the
   characters of order n modulo p are not strange (the files large_selected_orders.json),
   is the order of a strange character in the table, for p < 4*10^5.
Only the Python standard library is used.
"""

import hashlib
import json
import math
import re
import sys
from fractions import Fraction

BOUND = 400000
LOWER = 100000
KAPPA = Fraction(2**19, 325)
SELECTIONS = {
    11: "audit11/large_selected_orders.json",
    12: "degree12/large_selected_orders.json",
    18: "degree18/large_selected_orders.json",
    19: "degree19/large_selected_orders.json",
    20: "degree20/large_selected_orders.json",
    21: "degree21/large_selected_orders.json",
    22: "degree22/large_selected_orders.json",
}


def primes_below(n):
    sieve = bytearray([1]) * n
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n - 1) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytearray(len(range(p * p, n, p)))
    return [p for p in range(n) if sieve[p]]


def read_stoll(path):
    strange = {}
    for line in open(path, encoding="utf-8"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        p, n, dim = map(int, line.split())
        strange.setdefault(p, {})
        assert n not in strange[p]
        strange[p][n] = dim
    return strange


def read_table2(path):
    """Table 2 of Derickx-Stoll, as LaTeX rows ' p&...', '\\ord(\\chi)&...', '\\sdim(p)&...'."""
    orders, dims, current = {}, {}, None
    for line in open(path, encoding="utf-8"):
        cells = [c for c in line.split("\\\\")[0].split("&")[1:] if c.strip()]
        if " p&" in line:
            current = [int(c) for c in cells]
        elif r"\ord(\chi)&" in line:
            orders.update(zip(current, [sorted(map(int, c.split(","))) for c in cells]))
        elif r"\sdim(p)&" in line:
            dims.update(zip(current, [sum(map(int, re.findall(r"\d+", c))) for c in cells]))
    return orders, dims


def main():
    table = sys.argv[1]
    print("table:", table.rsplit("/", 1)[-1])
    print("sha256:", hashlib.sha256(open(table, "rb").read()).hexdigest())
    strange = read_stoll(table)
    primes = primes_below(BOUND)
    pset = set(primes)
    for p, ords in strange.items():
        assert p in pset
        for n in ords:
            assert n > 1 and (p - 1) % (2 * n) == 0, (p, n)
    print("rows:", sum(len(v) for v in strange.values()), " strange primes:", len(strange))

    # 1. Agreement with Derickx-Stoll, Table 2, below 10^5.
    t2_orders, t2_dims = read_table2("audit11/derickx_stoll_table2.txt")
    small = {p: sorted(v) for p, v in strange.items() if p < LOWER}
    assert small == t2_orders, "disagreement with Table 2 below 10^5"
    assert {p: sum(v.values()) for p, v in strange.items() if p < LOWER} == t2_dims
    print("below 10^5: equal to Derickx-Stoll Table 2 (%d strange primes, orders and dimensions)"
          % len(t2_orders))

    # 2. The whole interval 10^5 < p < 4*10^5 via Corollary 7.5.
    interval = [p for p in primes if p > LOWER]
    hmin = None
    for p in interval:
        s = math.lcm(*strange[p]) if p in strange else 1
        h = (p - 1) // (2 * s)
        assert (p - 1) % (2 * s) == 0
        assert h > 22 and p * p > KAPPA * 22 + 1 and p > 3 * 22 + 1, p
        if hmin is None or h < hmin[0]:
            hmin = (h, p, s)
    print("primes in (10^5, 4*10^5): %d; min (p-1)/(2 str(p)) = %d (p = %d, str(p) = %d)"
          % ((len(interval),) + hmin))
    print("hence none of them is in S(d) for d <= 22 (Derickx-Stoll, Corollary 7.5)")

    # 3. The characters shown not to be strange in the proof of Proposition 4.13.
    pairs = set()
    for d, path in SELECTIONS.items():
        sel = json.load(open(path, encoding="utf-8"))
        tot_p = len(sel["primes"])
        tot_n = sum(len(r["orders"]) for r in sel["primes"])
        cov = [r for r in sel["primes"] if r["p"] < BOUND]
        for r in cov:
            assert r["p"] > LOWER and r["p"] in pset
            clash = set(r["orders"]) & set(strange.get(r["p"], {}))
            assert not clash, (d, r["p"], sorted(clash))
            pairs.update((r["p"], n) for n in r["orders"])
        print("d = %2d: %4d of %4d primes below 4*10^5, %5d of %5d character orders, no clash"
              % (d, len(cov), tot_p, sum(len(r["orders"]) for r in cov), tot_n))
    print("distinct pairs (p, n) compared: %d, at %d primes; none is strange"
          % (len(pairs), len({p for p, _ in pairs})))
    print("PASS")


if __name__ == "__main__":
    main()
