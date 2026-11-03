"""Exact degree-five existence tests from canonical forms; no model required.

Genus 3: certify 5 is a nongap at the rational Tate cusp.
Genus 4: certify nonhyperellipticity, then K-P is basepoint free of degree 5.
See LOW_GENUS.md. Run with Sage's Python.
"""
import json
from pathlib import Path
from sage.all import CuspForms, GammaH, QQ, Matrix


def main():
    root = Path(__file__).resolve().parent
    inventory = json.loads((root/'classification_inventory.json').read_text())
    answers = []
    for row in inventory['curves']:
        if row['genus'] not in (3,4) or row['quintic_status'].startswith('FINITE'):
            continue
        n, delta, g = row['level'], row['delta'], row['genus']
        prec = max(12, (4*row['index'])//12+2)
        space = CuspForms(GammaH(n,delta),2,base_ring=QQ)
        assert space.dimension() == g
        basis = list(space.q_expansion_basis(prec))
        matrix = Matrix(QQ,[[f[i] for i in range(prec)] for f in basis])
        assert matrix.rank() == g
        gaps = list(map(int,matrix.pivots()))
        assert len(gaps) == g and all(i > 0 for i in gaps)
        result = dict(id=row['id'],level=n,delta=delta,genus=g,gaps=gaps)
        if g == 3:
            result['passed'] = 5 not in gaps
            result['method'] = '5 is a nongap at the rational Tate cusp'
        else:
            products = [basis[i]*basis[j] for i in range(g) for j in range(i,g)]
            bound = (4*row['index'])//12
            rank = Matrix(QQ,[[f[i] for i in range(bound+1)] for f in products]).rank()
            assert rank in (2*g-1,3*g-3)
            result['quadratic_product_rank'] = int(rank)
            result['passed'] = rank == 3*g-3
            result['method'] = 'nonhyperelliptic genus 4: K-P basepoint free'
        answers.append(result)
        print('PASS' if result['passed'] else 'UNRESOLVED', n, delta, result, flush=True)
    (root/'low_genus_certificates.json').write_text(json.dumps(answers,indent=2)+'\n')
    print('SUCCESS completed low-genus tests; inspect passed flags.')


if __name__ == '__main__':
    main()
