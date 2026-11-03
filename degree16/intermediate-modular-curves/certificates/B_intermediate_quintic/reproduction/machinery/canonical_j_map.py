"""Construct the modular j-function on a new canonical model by exact q-series.

Use the standard-monomial basis of H0(kK), rather than all degree-k
monomials. The equation Delta*numerator = E4^3*denominator is certified
past the weight-(2k+12) Sturm bound. This avoids importing a j-map or cusp
coordinates from an external implementation. Run with Sage's Python.
"""
import argparse
import hashlib
import json
from pathlib import Path
from sage.all import CuspForms, GammaH, Matrix, PolynomialRing, PowerSeriesRing, QQ, sigma
from export_canonical import export

ROOT = Path(__file__).resolve().parent


def construct(directory):
    data = json.loads((directory/'relations.json').read_text())
    invariants = data['invariants']
    n,g,index = (invariants[key] for key in ['level','genus','index'])
    model = json.loads((directory.parent/'result.json').read_text())
    assert model['model_verified']
    assert model['id']==f'{n}:'+','.join(map(str,invariants['delta']))
    for name,digest in model['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    for name,digest in model['artifact_sha256'].items():
        assert hashlib.sha256((directory.parent/name).read_bytes()).hexdigest()==digest
    original = json.loads((directory.parent/'relations.json').read_text())
    assert data['invariants']==original['invariants']
    assert data['basis_coefficients']==original['basis_coefficients']
    assert len(data['relation_blocks'])==len(original['relation_blocks'])
    for block,old in zip(data['relation_blocks'],original['relation_blocks']):
        assert block['monomials']==old['monomials']
        assert Matrix(QQ,block['relations']).row_space()==Matrix(QQ,old['relations']).row_space()
    # deg(kK-div_infty(j)) >= g guarantees a denominator by Riemann--Roch.
    degree = (index+g+2*g-3)//(2*g-2)
    bound = (2*degree+12)*index//12
    precision = bound+16
    R = PolynomialRing(QQ,g,'x',order='degrevlex')
    equations = []
    for block in data['relation_blocks']:
        for row in block['relations']:
            equations.append(sum(QQ(c)*R.prod(R.gen(i) for i in indices)
                                 for c,indices in zip(row,block['monomials']) if QQ(c)))
    ideal = R.ideal(equations)
    monomials = list(ideal.normal_basis(degree))
    assert len(monomials)==degree*(2*g-2)+1-g
    print('standard monomials',len(monomials),'degree',degree,'precision',precision,flush=True)
    forms = CuspForms(GammaH(n,invariants['delta']),2,base_ring=QQ)
    basis = list(forms.q_expansion_basis(precision))
    assert len(basis)==g
    assert all([str(f[i]) for i in range(data['precision'])]==old
               for f,old in zip(basis,data['basis_coefficients']))
    S = PowerSeriesRing(QQ,'q',default_prec=precision)
    q = S.gen()
    E4 = S([1]+[240*sigma(i,3) for i in range(1,precision)]).add_bigoh(precision)
    discriminant = S(CuspForms(1,12).q_expansion_basis(precision)[0])
    assert discriminant[0]==0 and discriminant[1]==1
    powers = [[S(f)**i for i in range(degree+1)] for f in basis]
    exponents = [list(m.exponents()[0]) for m in monomials]
    products = [S.prod(powers[i][e] for i,e in enumerate(v)) for v in exponents]
    series = [f*discriminant for f in products]+[-f*E4**3 for f in products]
    matrix = Matrix(QQ,[[f[i] for i in range(bound+1)] for f in series])
    print('exact linear system',matrix.nrows(),matrix.ncols(),flush=True)
    kernel = matrix.left_kernel().basis_matrix()
    assert kernel.nrows()>0
    extra = Matrix(QQ,[[f[i] for i in range(bound+1,precision)] for f in series])
    assert kernel*extra==0
    length = len(monomials)
    coefficients = kernel.row(0)
    numerator = sum(c*m for c,m in zip(coefficients[:length],monomials))
    denominator = sum(c*m for c,m in zip(coefficients[length:],monomials))
    assert numerator!=0 and denominator!=0

    def magma_polynomial(values):
        terms = []
        for c,exps in zip(values,exponents):
            if c:
                term = f'({c})'
                for i,e in enumerate(exps):
                    if e:
                        term += f'*R.{i+1}^{e}'
                terms.append(term)
        return '+'.join(terms) or '0'

    output = directory/'j_map'
    output.mkdir(exist_ok=True)
    (output/'canonical_input.m').write_text(export(data))
    (output/'j_function.m').write_text(
        f'expected_j_degree := {index};\n'
        +'j_numerator := '+magma_polynomial(coefficients[:length])+';\n'
        +'j_denominator := '+magma_polynomial(coefficients[length:])+';\n')
    report = dict(id=model['id'],canonical_degree=degree,sturm_bound=bound,precision=precision,
                  relation_dimension=kernel.nrows(),status='EXACT_J_IDENTITY_BY_STURM',
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  model_relations_sha256=hashlib.sha256((directory/'relations.json').read_bytes()).hexdigest())
    (output/'j_identity.json').write_text(json.dumps(report,indent=2)+'\n')
    print('SUCCESS exact canonical j-map',model['id'],flush=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    args = parser.parse_args()
    construct(args.directory.resolve())
