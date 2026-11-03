"""Bounded integer-coordinate points; positive witnesses only, no completeness.

This avoids expensive general point-search setup on high-dimensional models.
"""
import argparse
from fractions import Fraction
from functools import reduce
from itertools import product
from math import gcd, lcm
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('directory',type=Path)
parser.add_argument('--bound',type=int,default=1)
args = parser.parse_args()
data = json.loads((args.directory/'relations.json').read_text())
g = data['invariants']['genus']
equations = []
for block in data['relation_blocks']:
    for row in block['relations']:
        values = [Fraction(c) for c in row]
        denominator = lcm(*(c.denominator for c in values))
        equations.append([(int(c*denominator),indices)
                          for c,indices in zip(values,block['monomials']) if c])
equations.sort(key=len)
points = []
for first in range(g):
    for head in range(1,args.bound+1):
        for tail in product(range(-args.bound,args.bound+1),repeat=g-first-1):
            v = (0,)*first+(head,)+tail
            if reduce(gcd,v) != 1:
                continue
            if all(sum(c*reduce(lambda x,i:x*v[i],indices,1) for c,indices in equation)==0
                   for equation in equations):
                points.append(v)
assert points
output = 'small_points := [\n'+',\n'.join('['+','.join(map(str,v))+']' for v in points)+'\n];\n'
(args.directory/'small_points.m').write_text(output)
print('SUCCESS verified small-coordinate points',len(points),points,flush=True)
