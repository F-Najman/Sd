#!/usr/bin/env python3
"""Run the 36 exact Magma certificates; no third-party Python packages needed.

Examples: python3 run.py --jobs 8
          python3 run.py --check-logs
          python3 run.py --only translates_145
Magma can exit with status zero after an assertion failure. Check its text too.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parent
GROUPS = {
    "translates": [74,77,82,86,99,111,118,123,128,141,142,143,145,155,159],
    "quotient_sieve": [79,83,89,101,103,107,131,167,191],
    "empty_cosets": [85,88,92],
    "local_pencils": [77,85,88],
    "rank_zero": [96,98,100],
}
PREFIX = {"quotient_sieve": "quotient", "empty_cosets": "empty",
          "local_pencils": "local"}
TASKS = {}
for script, levels in GROUPS.items():
    for level in levels:
        name = f"{PREFIX.get(script, script)}_{level}"
        TASKS[name] = [f"N:={level}", f"{script}.m"]
for script in ["arithmetic", "pencils74", "cubic83"]:
    TASKS[script] = [f"{script}.m"]
ERROR = re.compile(r"Runtime error|User error|Assertion failed|syntax error|"
                   r"Error:|Internal error|Segmentation fault", re.IGNORECASE)


def check(name):
    path = ROOT / "logs" / f"{name}.log"
    if not path.exists():
        return False
    text = path.read_text(errors="replace")
    return "SUCCESS" in text and not ERROR.search(text)


def run(name, magma):
    start = time.monotonic()
    with (ROOT / "logs" / f"{name}.log").open("w") as log:
        result = subprocess.run([magma, "-b", *TASKS[name]],
                                cwd=ROOT / "code", stdout=log,
                                stderr=subprocess.STDOUT)
    return name, result.returncode == 0 and check(name), time.monotonic()-start


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=8,
                        help="independent Magma processes (default: 8)")
    parser.add_argument("--magma", default="magma")
    parser.add_argument("--only", nargs="+", choices=sorted(TASKS))
    parser.add_argument("--check-logs", action="store_true",
                        help="audit saved logs without rerunning Magma")
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    names = args.only or list(TASKS)
    (ROOT / "logs").mkdir(exist_ok=True)
    results = {}
    if args.check_logs:
        for name in names:
            results[name] = {"passed": bool(check(name))}
    else:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            pending = [pool.submit(run, name, args.magma) for name in names]
            for future in as_completed(pending):
                name, passed, seconds = future.result()
                results[name] = {"passed": bool(passed), "seconds": round(seconds, 2)}
                print(f"{'PASS' if passed else 'FAIL'} {name}: {seconds:.1f}s", flush=True)
    for name in sorted(results):
        print(f"{'PASS' if results[name]['passed'] else 'FAIL'} {name}")
    # Bind the audit to the supplied source and output, rather than claiming
    # that a SUCCESS marker alone authenticates an arbitrary future edit.
    paths = sorted((ROOT / "code").glob("*.m"))
    paths += [ROOT / "logs" / f"{name}.log" for name in sorted(names)]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in paths if p.exists()}
    report = {"mode": "saved-log audit" if args.check_logs else "fresh run",
              "tasks": results, "sha256": hashes}
    (ROOT / "verification.json").write_text(json.dumps(report, indent=2)+"\n")
    good = sum(item["passed"] for item in results.values())
    print(f"{good}/{len(names)} certificates passed")
    raise SystemExit(0 if good == len(names) else 1)


if __name__ == "__main__":
    main()
