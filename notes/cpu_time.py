#!/usr/bin/env python3
"""Estimate the CPU time of the S(d) computations from the log files of the individual jobs.

Usage: python3 cpu_time.py WORKDIR
where WORKDIR is the original workspace folder containing audit10, audit11, degree11, ..., degree22
(on Mordell: ~/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work).

Every job (a Magma run, a C++ sequence computation, a Sage check, ...) writes its own .log file, created when the
job starts and last modified when it ends, so the running time of a job is the difference between the
modification time and the birth time of its log (GNU stat %W and %Y). All the programs are single-threaded.
Logs of driver processes, which only launch and wait for other jobs, are excluded (names starting with run_,
finalize, resource_watch, handoff, pipeline, setup_, progress, archive, drain, resume, ...). Jobs without a log file
are not counted. Machine load (more jobs than cores) makes running times slightly larger than CPU times.
"""
import collections, re, subprocess, sys

work = sys.argv[1]
# GNU find lists the logs, GNU stat gives their birth (%W) and modification (%Y) times.
out = subprocess.run("command find . -name '*.log' -print0 | xargs -0 stat -c '%W %Y %n'", shell=True, cwd=work,
                     capture_output=True, text=True, check=True).stdout
DRV = re.compile(r'^(run_|finalize|resource_watch|handoff|pipeline|setup_|progress|archive|drain|resume|launch|'
                 r'scheduler|supervis|watch|package|background)')
deg = collections.Counter(); chars = collections.Counter()
for line in out.splitlines():
    b, m, p = line.split(' ', 2)
    try:
        dur = max(0.0, float(m) - float(b))
    except ValueError:
        continue
    parts = p.split('/')
    if len(parts) < 3:
        continue
    d = parts[1]
    if len(parts) == 3 and DRV.match(parts[2]):
        continue
    deg[d] += dur
    if (len(parts) > 3 and parts[2] == 'large_orders') or \
       (len(parts) == 3 and re.match(r'(check_sequences|verify_large|large_)', parts[2])):
        chars[d] += dur
groups = {'d<=11': ['audit10', 'audit11', 'degree11', 'continuation', 'independent_audit'],
          'd=12': ['degree12'], 'd=13-17': [f'degree{k}' for k in range(13, 18)],
          'd=18': ['degree18'], 'd=19': ['degree19'], 'd=20': ['degree20'], 'd=21': ['degree21'], 'd=22': ['degree22']}
T = C = 0.0
print(f"{'degrees':8s} {'all jobs (h)':>13s} {'Lemma 4.11 (h)':>15s}")
for g, ds in groups.items():
    t = sum(deg[x] for x in ds) / 3600; c = sum(chars[x] for x in ds) / 3600
    T += t; C += c
    print(f'{g:8s} {t:13.1f} {c:15.1f}')
print(f"{'total':8s} {T:13.1f} {C:15.1f}")
