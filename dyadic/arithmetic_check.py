#!/usr/bin/env python3
"""Verify the explicit crossover; no Magma computation is involved."""
from fractions import Fraction
import json
cutoff=53
polynomial=65*(4*cutoff)**6
exponential=2**cutoff
assert polynomial < exponential
ratio=Fraction(2*cutoff**6,(cutoff+1)**6)
assert ratio > 1
# 2*(d/(d+1))**6 increases with d; the preceding inequality propagates.
print(json.dumps({"cutoff":cutoff,"polynomial":polynomial,"exponential":exponential,"ratio_to_next":str(ratio),"all_d_at_least_cutoff":True},indent=2))
