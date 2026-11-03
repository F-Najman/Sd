#!/bin/sh
# Theorem D for one level:  ./run.sh N
# The prime p, the degree d to exclude, the number of Phase 1 processes and the memory cap per process (GB)
# are read from levels.csv (an empty limit means none). Each Phase 1 process enumerates all places, so the
# memory per process does not shrink with more processes; make sure the machine has (processes x memory) GB available.
set -e
cd "$(dirname "$0")"
line=$(grep "^$1," levels.csv)
p=$(echo $line | cut -d, -f2); d=$(echo $line | cut -d, -f3); s=$(echo $line | cut -d, -f4); m=$(echo $line | cut -d, -f5)
make -C phase2 search
MEMGB=${MEMGB:-$m} python3 phase1/run_phase1.py models/X1_$1.txt $p $d $s runs/x1_$1
phase2/search runs/x1_$1/curve.ffjets --degree $d --threads ${THREADS:-8} | tee runs/x1_$1/phase2.json
