#!/bin/sh
# gon_Q(43.132.9.a.2) = 7. Run from this folder; logs go to out/.
set -e
mkdir -p out
for s in identify_model torsion_classes audit_smooth_reduction audit_certificate audit_torsion_counts prove_lower_bound_7 prove_upper_bound_7; do
  magma -b $s.m > out/$s.out 2>&1
  grep -q -i -E "error|assertion failed" out/$s.out && { echo "FAIL $s"; exit 1; }
  echo "ok $s"
done
