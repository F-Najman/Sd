"""Disk space and running time of the character jobs of Lemma 4.11.

Usage (on Mordell, from the original workspace):
    python3 notes/disk_usage.py work/degree20/large_orders work/degree21/large_orders work/degree22/large_orders

A job is a pair (p, n), and its files are named pNNN_nMMM_*. For each folder this prints the number of jobs and
primes and, grouped by p, the average size of the files of a job and the average running time of a job. The
running time is the sum of (last modification - creation) of the .log files of the job, as in cpu_time.py.
"""
import collections
import os
import re
import subprocess
import sys

JOB = re.compile(r'p(\d+)_n(\d+)_')


def birth_and_mtime(paths):
    """GNU stat %W (creation) and %Y (last modification) of each path."""
    out = {}
    for i in range(0, len(paths), 2000):
        res = subprocess.run(['stat', '-c', '%W %Y %n', '--', *paths[i:i + 2000]],
                             capture_output=True, text=True, check=True)
        for line in res.stdout.splitlines():
            w, y, name = line.split(' ', 2)
            out[name] = (int(w), int(y))
    return out


for folder in sys.argv[1:]:
    size = collections.defaultdict(int)
    logs = collections.defaultdict(list)
    for root, dirs, files in os.walk(folder):
        for f in files:
            m = JOB.match(f)
            if m:
                key = (int(m[1]), int(m[2]))
                path = os.path.join(root, f)
                size[key] += os.lstat(path).st_size
                if f.endswith('.log'):
                    logs[key].append(path)
    if not size:
        print(f'== {folder}: no jobs')
        continue
    times = birth_and_mtime([path for paths in logs.values() for path in paths])
    hours = collections.defaultdict(float)
    for key, paths in logs.items():
        for path in paths:
            w, y = times[path]
            if w > 0:
                hours[key] += (y - w) / 3600
    groups = collections.defaultdict(lambda: [0, 0, 0.0])
    for key in size:
        g = groups[key[0] // 500000]
        g[0] += 1
        g[1] += size[key]
        g[2] += hours[key]
    print(f'== {folder}: {len(size)} jobs, {len({p for p, n in size})} primes, p up to '
          f'{max(p for p, n in size)}, {sum(size.values()) / 1e9:.1f} GB, {sum(hours.values()):.1f} h')
    for k in sorted(groups):
        c, s, h = groups[k]
        print(f'   p in [{k / 2:.1f}, {(k + 1) / 2:.1f}) x 10^6: {c:5d} jobs, '
              f'{s / c / 1e6:6.1f} MB and {60 * h / c:6.1f} min per job')
