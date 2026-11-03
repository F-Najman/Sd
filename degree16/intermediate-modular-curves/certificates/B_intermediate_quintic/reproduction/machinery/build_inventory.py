"""Build the new classification ledger from the independently audited census.

Only explicitly named theorems are imported. No home-directory status is read.
"""
import hashlib
import json
from pathlib import Path
from enumeration import generated, signature, units
from published_gonality import at_least_six
from export_canonical import export as export_canonical

X0_POSITIVE = set(range(1, 46)) | set(range(47, 59)) | {
    61,63,64,65,67,68,72,73,75,80,81,91,109,121,125}
NEW_X0_NEGATIVE = {74,77,79,82,83,85,86,88,89,92,96,98,99,100,101,103,
                   107,111,118,123,128,131,141,142,143,145,155,159,167,191}


def checked_rankzero(root, row, endpoint=False):
    identifier = f'X1({row["level"]})' if endpoint else row['id']
    key = hashlib.sha256(identifier.encode()).hexdigest()[:16]
    path = root/'rankzero_replays'/key/'certificate.json'
    certificate = json.loads(path.read_text())
    assert certificate['id'] == identifier
    assert certificate['status'] == 'RANK_ZERO_BY_EXACT_CENTRAL_VALUE'
    for filename,digest in certificate['source_sha256'].items():
        assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
    for filename,digest in certificate['artifact_sha256'].items():
        assert hashlib.sha256((path.parent/filename).read_bytes()).hexdigest() == digest
    recorded = json.loads((path.parent/'input.json').read_text())
    assert recorded['kind'] == ('endpoint' if endpoint else 'intermediate')
    keys = ['level'] if endpoint else ['id','level','delta','genus']
    assert all(recorded['row'][k] == row[k] for k in keys)
    return str(path.relative_to(root))


def checked_elliptic_input(root, level):
    path = root/'elliptic_input_replays'/f'N{level}'/'certificate.json'
    certificate = json.loads(path.read_text())
    assert certificate['level'] == level and certificate['status'] == 'EXACT_ELLIPTIC_INPUT'
    for filename,digest in certificate['source_sha256'].items():
        assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
    for filename,digest in certificate['artifact_sha256'].items():
        assert hashlib.sha256((path.parent/filename).read_bytes()).hexdigest() == digest
    expected = ({'minimum_positive_elliptic_degree':12 if level==37 else 8}
                if level in [37,57] else {'no_positive_rank_elliptic_factors':True})
    assert certificate['conclusion'] == expected
    return str(path.relative_to(root))


def checked_last_positive(root, identifier):
    level = int(identifier.split(':')[0])
    assert level in [40,48]
    path = root/'last_positive_replays'/f'N{level}'/'certificate.json'
    certificate = json.loads(path.read_text())
    assert certificate['id'] == identifier
    assert certificate['status'] == 'INFINITE_BY_NEW_EXACT_FUNCTION'
    for filename,digest in certificate['source_sha256'].items():
        assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
    for filename,digest in certificate['artifact_sha256'].items():
        assert hashlib.sha256((path.parent/filename).read_bytes()).hexdigest() == digest
    return str(path.relative_to(root))


def main():
    root = Path(__file__).resolve().parent
    source = root/'enumeration_audit_191.json'
    census = json.loads(source.read_text())
    assert census['status'] == 'PASS' and census['max_level'] == 191
    census_certificate = json.loads((root/'enumeration_replay/certificate.json').read_text())
    assert census_certificate['status'] == 'INDEPENDENT_CENSUS_REPLAY'
    assert census_certificate['max_level'] == 191
    for filename,digest in census_certificate['source_sha256'].items():
        assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
    for filename,digest in census_certificate['artifact_sha256'].items():
        assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
    curves = census['curves']
    x0 = {r['level']: r for r in curves if r['degree_to_x0'] == 1}
    # Finiteness of rational points on every negative target is essential
    # for the prime-degree projection argument.
    assert all(x0[n]['genus'] > 1 for n in range(1,192) if n not in X0_POSITIVE)
    pentagonal = {
        (31, generated(31, [-1,5,6])),
        (31, generated(31, [-1,2,4,8,15])),
        (44, generated(44, [-1,5,7,9,19])),
        (125, generated(125, [-1,4])),
    }
    # JKS Theorem 0.2 and Table 6: the only bielliptic strict curves
    # of genus >6. Coprime degrees 2 and 5 give the CS bound g <= 6.
    bielliptic_obstruction = {
        (35,tuple(sorted({a % 35 for b in [1,6,8,13] for a in [b,-b]}))): 7,
        (55,tuple(sorted({a % 55 for b in [1,4,6,9,14,16,19,21,24,26] for a in [b,-b]}))): 9,
    }
    rows = []
    low_canonical = {r['id']:r for r in json.loads((root/'low_genus_certificates.json').read_text())}
    low_certificate = json.loads((root/'low_genus_certificate.json').read_text())
    assert low_certificate['status'] == 'EXACT_LOW_GENUS_CANONICAL_CERTIFICATES'
    for filename,digest in low_certificate['source_sha256'].items():
        assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
    for filename,digest in low_certificate['artifact_sha256'].items():
        assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
    rank_zero = json.loads((root/'central_values.json').read_text())
    intermediate_path = root/'intermediate_central.json'
    intermediate_rank = json.loads(intermediate_path.read_text()) if intermediate_path.exists() else {}
    batch_positive = {}
    for path in (root/'genus5_jobs').glob('*/result.json'):
        result = json.loads(path.read_text())
        if not result['quintic_witness']:
            continue
        assert result['model_verified']
        for name,digest in result['source_sha256'].items():
            assert hashlib.sha256((root/name).read_bytes()).hexdigest() == digest
        geometry = (path.parent/'geometry.log').read_text()
        assert 'SUCCESS: smooth genus-five' in geometry and 'error' not in geometry.lower()
        witness = [p.read_text() for p in path.parent.glob('*.log')
                   if p.name in ('effective.log','residual.log')]
        assert any('SUCCESS EXACT DEGREE FIVE' in s and 'error' not in s.lower() for s in witness)
        level = int(result['id'].split(':')[0])
        replay_path = root/'batch_positive_replays'/f'N{level}'/'certificate.json'
        replay = json.loads(replay_path.read_text())
        assert replay['id'] == result['id']
        assert replay['status'] == 'INFINITE_BY_NEW_EXACT_FUNCTION'
        for filename,digest in replay['source_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
        for filename,digest in replay['artifact_sha256'].items():
            assert hashlib.sha256((replay_path.parent/filename).read_bytes()).hexdigest() == digest
        batch_positive[result['id']] = str(replay_path.relative_to(root))
    for path in (root/'genus5_jobs').glob('*/closed_support_result.json'):
        result = json.loads(path.read_text())
        if not result['exact_function_found']:
            continue
        assert result['source_sha256'] == hashlib.sha256(
            (root/'search_closed_support.m').read_bytes()).hexdigest()
        for filename, digest in result['artifact_sha256'].items():
            assert hashlib.sha256((path.parent/filename).read_bytes()).hexdigest() == digest
        model = json.loads((path.parent/'result.json').read_text())
        assert model['id'] == result['id'] and model['model_verified']
        for filename, digest in model['source_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
        relations = json.loads((path.parent/'relations.json').read_text())
        assert (path.parent/'canonical_input.m').read_text() == export_canonical(relations)
        geometry = (path.parent/'geometry.log').read_text()
        assert 'SUCCESS: smooth genus-five' in geometry and 'error' not in geometry.lower()
        witness = (path.parent/'closed_support.log').read_text()
        assert 'SUCCESS EXACT DEGREE FIVE from closed support' in witness
        assert 'error' not in witness.lower()
        batch_positive[result['id']] = checked_last_positive(root,result['id'])
    for r in curves:
        if not r['strict']:
            continue
        n = r['level']
        row = dict(r)
        row['id'] = f"{n}:"+','.join(map(str,r['delta']))
        row['model_status'] = 'NOT_CONSTRUCTED'
        row['degree5_function'] = 'UNKNOWN'
        if n not in X0_POSITIVE:
            row['quintic_status'] = 'FINITE_BY_PROJECTION'
            row['source'] = 'x0_final' if n in NEW_X0_NEGATIVE else 'DHJO_1_10'
        elif (n, tuple(r['delta'])) in pentagonal:
            row['quintic_status'] = 'INFINITE_BY_PUBLISHED_GONALITY_5'
            row['degree5_function'] = 'EXISTS_BY_PUBLISHED_THEOREM'
            row['source'] = 'Orlic_1_4_1_5'
        elif r['genus'] <= 2:
            # The mu-model Tate cusp is rational; duality transfers it to
            # the intended curve. Degree 5 >= 2g+1 gives a very ample
            # rational line bundle. A general rational pencil is basepoint
            # free, so Hilbert irreducibility gives exact-degree-5 points.
            row['quintic_status'] = 'INFINITE_BY_LOW_GENUS'
            row['degree5_function'] = 'EXISTS_BY_RIEMANN_ROCH'
            row['source'] = 'low_genus_lemma'
        elif (n,tuple(r['delta'])) in {(33,generated(33,[-1,2])),
                                      (34,generated(34,[-1,9])),
                                      (35,generated(35,[-1,4])),
                                      (41,generated(41,[-1,2]))}:
            path = root/'positive_replays'/f'N{n}'/'certificate.json'
            certificate = json.loads(path.read_text())
            assert certificate['id'] == row['id']
            assert certificate['status'] == 'INFINITE_BY_NEW_EXACT_FUNCTION'
            for filename,digest in certificate['source_sha256'].items():
                assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
            for filename,digest in certificate['artifact_sha256'].items():
                assert hashlib.sha256((path.parent/filename).read_bytes()).hexdigest() == digest
            row['quintic_status'] = 'INFINITE_BY_NEW_EXACT_FUNCTION'
            row['degree5_function'] = 'EXPLICIT_CERTIFIED'
            row['source'] = str(path.relative_to(root))
        elif 119*r['index'] > 120000:
            row['quintic_status'] = 'FINITE_BY_GONALITY_ABOVE_10'
            row['degree5_function'] = 'DOES_NOT_EXIST'
            row['source'] = 'spectral_bound_and_Frey'
        elif row['id'] in low_canonical and low_canonical[row['id']]['passed']:
            low_row = low_canonical[row['id']]
            assert low_row['level'] == n and tuple(low_row['delta']) == tuple(r['delta'])
            assert low_row['genus'] == r['genus'] and r['genus'] in (3,4)
            row['quintic_status'] = 'INFINITE_BY_CANONICAL_LOW_GENUS'
            row['degree5_function'] = 'EXISTS_BY_CANONICAL_CERTIFICATE'
            row['source'] = 'low_genus_certificate.json'
        elif row['id'] in batch_positive:
            row['quintic_status'] = 'INFINITE_BY_NEW_EXACT_FUNCTION'
            row['degree5_function'] = 'EXPLICIT_CERTIFIED'
            row['source'] = batch_positive[row['id']]
        elif (n,tuple(r['delta'])) in bielliptic_obstruction:
            assert r['genus'] == bielliptic_obstruction[(n,tuple(r['delta']))] > 6
            row['rank_zero_certificate'] = checked_rankzero(root,row)
            evidence = intermediate_rank[row['id']]
            assert evidence['rank_zero_proved'] and evidence['genus_checked'] == r['genus']
            log = (root/evidence['log']).read_text()
            assert 'central_zero=false' in log and 'SUCCESS' in log and 'error' not in log.lower()
            row['quintic_status'] = 'FINITE_BY_BIELLIPTIC_AND_RANK_ZERO'
            row['degree5_function'] = 'DOES_NOT_EXIST'
            row['source'] = 'bielliptic_obstruction'
            row['central_value_log'] = evidence['log']
        elif rank_zero.get(str(n),{}).get('rank_zero_proved',False) and at_least_six(r):
            row['rank_zero_certificate'] = checked_rankzero(root,row,endpoint=True)
            log = (root/'central_values'/f'{n}.log').read_text()
            assert 'central_zero=false' in log and 'SUCCESS' in log and 'error' not in log.lower()
            row['quintic_status'] = 'FINITE_BY_RANK_ZERO_AND_GONALITY'
            row['degree5_function'] = 'DOES_NOT_EXIST'
            row['source'] = 'rank_zero_gonality_lemma'
        elif intermediate_rank.get(row['id'],{}).get('rank_zero_proved',False) and at_least_six(r):
            row['rank_zero_certificate'] = checked_rankzero(root,row)
            evidence = intermediate_rank[row['id']]
            assert evidence['genus_checked'] == r['genus']
            log = (root/evidence['log']).read_text()
            assert 'central_zero=false' in log and 'SUCCESS' in log and 'error' not in log.lower()
            row['quintic_status'] = 'FINITE_BY_INTERMEDIATE_RANK_ZERO'
            row['degree5_function'] = 'DOES_NOT_EXIST'
            row['source'] = 'intermediate_rank_zero_lemma'
            row['central_value_log'] = evidence['log']
        elif n == 43 and r['genus'] == 9 and at_least_six(r):
            directory = root/'hilbert_jobs/d0a49dd94f1144df/integral_model'
            certificate = json.loads((directory/'certificate.json').read_text())
            assert certificate['id'] == row['id']
            assert certificate['status'] == 'FINITE_BY_ELLIPTIC_TRANSLATE_OBSTRUCTION'
            for filename,digest in certificate['source_sha256'].items():
                assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
            for filename,digest in certificate['artifact_sha256'].items():
                assert hashlib.sha256((directory/filename).read_bytes()).hexdigest() == digest
            row['quintic_status'] = certificate['status']
            row['degree5_function'] = 'DOES_NOT_EXIST'
            row['source'] = 'case43_elliptic_translate'
        elif ((n,r['genus'],r['degree_to_x0']) in {(37,10,6),(57,9,2),(73,9,2)}
              and at_least_six(r)):
            row['elliptic_input_certificate'] = checked_elliptic_input(root,n)
            logname = f'elliptic_factors_{n}.log' if n == 73 else f'small_density_{n}.log'
            log = (root/logname).read_text()
            if n == 73:
                assert 'CERTIFIED: no positive-rank elliptic factors' in log
                assert 'SUCCESS elliptic factor census' in log
            else:
                bound = 12 if n == 37 else 8
                assert f'CERTIFIED minimum_positive_elliptic_degree={bound}' in log
                assert 'SUCCESS small-density elliptic obstruction' in log
            assert 'error' not in log.lower()
            row['quintic_status'] = 'FINITE_BY_DEBARRE_FAHLAOUI_OBSTRUCTION'
            row['degree5_function'] = 'DOES_NOT_EXIST'
            row['source'] = 'debarre_fahlaoui_obstruction'
        elif n in {109,125} and r['genus'] >= 12 and at_least_six(r):
            row['elliptic_input_certificate'] = checked_elliptic_input(root,n)
            log = (root/f'elliptic_factors_{n}.log').read_text()
            assert 'CERTIFIED: no positive-rank elliptic factors' in log
            assert 'SUCCESS elliptic factor census' in log and 'error' not in log.lower()
            row['quintic_status'] = 'FINITE_BY_NO_ELLIPTIC_FACTORS_AND_DENSITY'
            row['degree5_function'] = 'DOES_NOT_EXIST'
            row['source'] = 'elliptic_degree_density_lemma'
        elif (n in {37,43,53,55,57,58,61,65,67,73,91,121}
              and r['genus'] >= 12 and at_least_six(r)):
            # Published elliptic-factor/optimality inputs; see the complete
            # minimum-density and prime-degree argument in this document.
            assert signature(n, units(n))['genus'] > 1
            row['quintic_status'] = 'FINITE_BY_ELLIPTIC_DEGREE_AND_DENSITY'
            row['degree5_function'] = 'DOES_NOT_EXIST'
            row['source'] = 'elliptic_degree_density_lemma'
        else:
            row['quintic_status'] = 'UNRESOLVED'
            row['source'] = None
        rows.append(row)
    # Model verification is independent of the density classification.
    # Never infer a positive or negative answer merely from having a model.
    by_id = {row['id']: row for row in rows}
    model_paths = (sorted((root/'canonical_jobs').glob('*/result.json'))
                   + sorted((root/'hilbert_jobs').glob('*/result.json')))
    for path in model_paths:
        result = json.loads(path.read_text())
        assert result['model_verified']
        for filename, digest in result['source_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
        for filename, digest in result.get('artifact_sha256',{}).items():
            assert hashlib.sha256((path.parent/filename).read_bytes()).hexdigest() == digest
        metadata = json.loads((path.parent/'curve.json').read_text())
        relations = json.loads((path.parent/'relations.json').read_text())
        row = by_id[result['id']]
        assert metadata['id'] == row['id']
        for key in ['level','delta','genus','index']:
            assert relations['invariants'][key] == row[key]
        log = (path.parent/'geometry.log').read_text()
        if path.parent.parent.name == 'hilbert_jobs':
            assert 'SUCCESS: canonical model identified by Hilbert polynomial' in log
            assert (path.parent/'canonical_input.m').read_text() == export_canonical(relations)
        else:
            assert 'SUCCESS: geometrically integral canonical model' in log
        assert 'error' not in log.lower()
        row['model_status'] = 'CANONICAL_MODEL_VERIFIED'
        row['model_certificate'] = str(path.parent.relative_to(root))
        search_file = path.parent/'search_result.json'
        if search_file.exists():
            search = json.loads(search_file.read_text())
            assert search['id'] == row['id']
            if search['exact_function_found']:
                assert search['search_source_sha256'] == hashlib.sha256(
                    (root/'search_quintic_canonical.m').read_bytes()).hexdigest()
                log = (path.parent/'quintic_search.log').read_text()
                assert 'SUCCESS EXACT DEGREE FIVE' in log and 'error' not in log.lower()
                assert not row['quintic_status'].startswith('FINITE')
                row['quintic_status'] = 'INFINITE_BY_NEW_EXACT_FUNCTION'
                row['degree5_function'] = 'EXPLICIT_CERTIFIED'
                row['source'] = checked_last_positive(root,row['id'])
    case40 = root/'hilbert_jobs/82f731393c98cb7c/case40_certificate.json'
    if case40.exists():
        certificate = json.loads(case40.read_text())
        assert certificate['status'] == 'FINITE_BY_COMPLETE_RATIONAL_CLASS_SIEVE'
        assert certificate['rational_torsion_order'] == 4032
        assert certificate['special_classes_checked'] == 12
        for filename,digest in certificate['source_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
        for filename,digest in certificate['artifact_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
        row = by_id[certificate['id']]
        assert row['model_status'] == 'CANONICAL_MODEL_VERIFIED'
        assert not row['quintic_status'].startswith('INFINITE')
        row['quintic_status'] = certificate['status']
        row['degree5_function'] = 'DOES_NOT_EXIST'
        row['source'] = str(case40.relative_to(root))
    for key,order,count in [('2fea1fad025e6bab',2304,4),('efd0600330b90e51',12800,24)]:
        path = root/'hilbert_jobs'/key/'case48_certificate.json'
        if not path.exists():
            continue
        certificate = json.loads(path.read_text())
        assert certificate['status'] == 'FINITE_BY_COMPLETE_RATIONAL_CLASS_SIEVE'
        assert certificate['rational_torsion_order'] == order
        assert certificate['special_classes_checked'] == count
        for filename,digest in certificate['source_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
        for filename,digest in certificate['artifact_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
        row = by_id[certificate['id']]
        assert row['level'] == 48 and row['genus'] == 7
        assert row['model_status'] == 'CANONICAL_MODEL_VERIFIED'
        assert not row['quintic_status'].startswith('INFINITE')
        row['quintic_status'] = certificate['status']
        row['degree5_function'] = 'DOES_NOT_EXIST'
        row['source'] = str(path.relative_to(root))
    case64 = root/'hilbert_jobs/d6111b7c56067f5a/case64_certificate.json'
    if case64.exists():
        certificate = json.loads(case64.read_text())
        assert certificate['status']=='INFINITE_BY_NEW_EXACT_FUNCTION'
        for filename,digest in certificate['source_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest()==digest
        for filename,digest in certificate['artifact_sha256'].items():
            assert hashlib.sha256((case64.parent/filename).read_bytes()).hexdigest()==digest
        row = by_id[certificate['id']]
        assert row['model_status']=='CANONICAL_MODEL_VERIFIED'
        assert not row['quintic_status'].startswith('FINITE')
        row['quintic_status']=certificate['status']
        row['degree5_function']='EXPLICIT_CERTIFIED'
        row['source']=str(case64.relative_to(root))
    for path in sorted((root/'hilbert_jobs').glob('*/integral_model/petri_certificate.json')):
        certificate = json.loads(path.read_text())
        assert certificate['status'] == 'FINITE_BY_PETRI_LIFTING_AND_RANK_ZERO'
        for filename,digest in certificate['source_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
        for filename,digest in certificate['artifact_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
        row = by_id[certificate['id']]
        assert row['model_status'] == 'CANONICAL_MODEL_VERIFIED'
        assert not row['quintic_status'].startswith('INFINITE')
        row['quintic_status'] = certificate['status']
        row['degree5_function'] = 'DOES_NOT_EXIST'
        row['source'] = str(path.relative_to(root))
    # A finite-field family count is not sufficient by itself. Only the
    # full replay (including immersion and the lifting proof) is accepted.
    family_certificates = (list((root/'family_jobs').glob('*/certificate.json'))
                           + list((root/'family3_jobs').glob('*/certificate.json')))
    for path in sorted(family_certificates):
        certificate = json.loads(path.read_text())
        assert certificate['status'] == 'FINITE_BY_REDUCIBLE_ELLIPTIC_FAMILIES'
        for filename,digest in certificate['source_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
        for filename,digest in certificate['artifact_sha256'].items():
            assert hashlib.sha256((root/filename).read_bytes()).hexdigest() == digest
        row = by_id[certificate['id']]
        assert row['model_status'] == 'CANONICAL_MODEL_VERIFIED'
        assert at_least_six(row)
        assert not row['quintic_status'].startswith('INFINITE')
        row['quintic_status'] = certificate['status']
        row['degree5_function'] = 'DOES_NOT_EXIST'
        row['source'] = str(path.relative_to(root))
    # Iterate over the rational forgetting maps: if M divides N and the
    # image of Delta_N modulo M lies in Delta_M, the map of moduli curves
    # is defined over Q. Target genus >1 is required for rational finiteness.
    changed = True
    while changed:
        changed = False
        targets = [r for r in rows if r['quintic_status'].startswith('FINITE') and r['genus'] > 1]
        for row in rows:
            if row['quintic_status'].startswith('FINITE'):
                continue
            for target in targets:
                m = target['level']
                if row['level'] % m or row['id'] == target['id']:
                    continue
                if {a % m for a in row['delta']} <= set(target['delta']):
                    assert not row['quintic_status'].startswith('INFINITE'), (row['id'],target['id'])
                    row['quintic_status'] = 'FINITE_BY_INTERMEDIATE_PROJECTION'
                    row['degree5_function'] = 'DOES_NOT_EXIST'
                    row['source'] = 'intermediate_projection_lemma'
                    row['projection_target'] = target['id']
                    changed = True
                    break
    # Record function nonexistence even when positive rank leaves the
    # degree-five point question unresolved. These are distinct questions.
    for row in rows:
        if row['quintic_status'].startswith('FINITE'):
            row['degree5_function'] = 'DOES_NOT_EXIST'
        elif row['quintic_status'] == 'UNRESOLVED' and at_least_six(row):
            row['degree5_function'] = 'DOES_NOT_EXIST'
            row['degree5_function_source'] = 'published_gonality.py, gonality at least six'
    report = dict(
        census_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        sources={
            'DHJO_1_10': 'https://arxiv.org/html/2503.08975v2 (Theorem 1.10)',
            'x0_final': '../final/quintic_points.tex and its 36 certificates',
            'Orlic_1_4_1_5': 'https://arxiv.org/abs/2407.14512 (Theorems 1.4, 1.5)',
            'low_genus_lemma': 'RATIONAL_MODELS.md, low-genus consequence',
            'spectral_bound_and_Frey': 'AUDIT.md, spectral gonality filter',
            'quintic_33.m': 'quintic_33.m, model_33.m, relations_33.json, RATIONAL_MODELS.md',
            'quintic_34.m': 'quintic_34.m, model_34.m, relations_34.json, RATIONAL_MODELS.md',
            'quintic_35.m': 'quintic_35.m, model_35.m, relations_35.json, RATIONAL_MODELS.md',
            'quintic_41.m': 'quintic_41.m, model_41.m, relations_41.json, RATIONAL_MODELS.md',
            'low_genus_certificates.py': 'LOW_GENUS.md, low_genus_certificates.json',
            'low_genus_certificate.json': 'LOW_GENUS.md; run_low_genus_audit.py; low_genus_certificate.json',
            'rank_zero_gonality_lemma': 'UNIFORM_EXCLUSIONS.md, published_gonality.py, central_values/',
            'intermediate_projection_lemma': 'UNIFORM_EXCLUSIONS.md, rational forgetting maps',
            'intermediate_rank_zero_lemma': 'UNIFORM_EXCLUSIONS.md, intermediate_central_value.m',
            'elliptic_degree_density_lemma': 'ELLIPTIC_DEGREE_EXCLUSIONS.md; Derickx-Orlic Corollaries 2.5, 4.10 and proof of 4.12',
            'debarre_fahlaoui_obstruction': 'DEBARRE_FAHLAOUI_OBSTRUCTION.md; Kadets-Vogt Proposition 6.3 and Theorem 5.8',
            'case43_elliptic_translate': 'CASE43.md; run_43_certificate.py; hilbert_jobs/d0a49dd94f1144df/integral_model/certificate.json',
            'bielliptic_obstruction': 'BIELLIPTIC_OBSTRUCTION.md; Jeon-Kim-Schweizer Theorem 0.2 and Table 6, https://arxiv.org/pdf/1709.00510',
        },
        all_level_boundary='N >= 192 excluded by DHJO and prime-degree projection; X0 has genus > 1',
        strict_curves_through_191=len(rows),
        retained=sum(r['level'] in X0_POSITIVE for r in rows),
        curves=rows)
    (root/'classification_inventory.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Strict curves through 191:', len(rows))
    print('Retained over positive X0 levels:', report['retained'])
    for status in sorted({r['quintic_status'] for r in rows}):
        print(status, sum(r['quintic_status'] == status for r in rows))


if __name__ == '__main__':
    main()
