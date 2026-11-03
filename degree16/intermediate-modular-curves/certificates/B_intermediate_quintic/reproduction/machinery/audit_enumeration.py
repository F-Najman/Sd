"""Independent cross-check against Sage's standard GammaH implementation.

Run: sage -python audit_enumeration.py --max-level 50
No pre-existing curve catalogue is read. Output is a fresh JSON certificate.
"""
import argparse
import json
from pathlib import Path
from sage.all import GammaH, Integers, version
from enumeration import subgroups, signature


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-level", type=int, default=50)
    parser.add_argument("--output", default="enumeration_audit.json")
    args = parser.parse_args()
    rows = []
    for n in range(1, args.max_level+1):
        groups = subgroups(n)
        # A second subgroup enumeration uses Sage's abstract unit group.
        ring = Integers(n)
        abstract = ring.unit_group()
        expected = set()
        for h in abstract.subgroups():
            # Sage subgroup elements do not carry the ambient value map.
            # Test membership of ambient elements instead of coercing them.
            elements = tuple(sorted(int(a.value()) % n for a in abstract if a in h))
            if (-1) % n in elements:
                expected.add(elements)
        assert set(groups) == expected, (n, "subgroup mismatch")
        for delta in groups:
            row = signature(n, delta)
            gamma = GammaH(n, list(delta))
            assert row["index"] == gamma.index(), (n, delta, "index")
            assert row["genus"] == gamma.genus(), (n, delta, "genus")
            assert row["cusps"] == gamma.ncusps(), (n, delta, "cusps")
            assert row["elliptic2"] == gamma.nu2(), (n, delta, "nu2")
            assert row["elliptic3"] == gamma.nu3(), (n, delta, "nu3")
            rows.append(row)
        print(f"PASS level {n}: {len(groups)} subgroups", flush=True)
    report = {"sage": str(version()), "max_level": args.max_level,
              "total": len(rows), "strict": sum(r["strict"] for r in rows),
              "status": "PASS", "curves": rows}
    Path(args.output).write_text(json.dumps(report, indent=2)+"\n")
    print(f"SUCCESS: {len(rows)} curves, {report['strict']} strict")


if __name__ == "__main__":
    main()
