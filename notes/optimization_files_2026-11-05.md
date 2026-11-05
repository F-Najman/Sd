# The folders `optimization/` of degrees 20, 21 and 22 (5 November 2026)

Michael Stoll (whose Claude looked at the repository) reported that `degree22/run_characters_simd.py` calls
files in `degree22/optimization/` that were not in the repository: `export_graph_fast.m`, `prepare_graph.cpp`,
`prepare_free.py`, `verify_graph.py`, `verify_free.py`, `check_graph_prefix.m`. The same was true of
`degree20/optimization/` and `degree21/optimization/`. These folders had not been copied when the repository was put
together. They are in the Dataverse deposit (`campaign/work/degreeNN/optimization/` in its file inventory).

## What was added

The three folders from the campaign workspace (`work/degreeNN/optimization/`), without the 11 compiled binaries:
353 files, 4.4 MB.

- 344 of them are in `proof_manifest.json.gz`, all with the same SHA256.
- The other 9 are the inputs that `degree21/optimization/check_free_fixtures.py` writes (`free_fixtures/*.graph`,
  `*.plan`, `*.prepared`).
- 21 files in the manifest had been deleted locally after the Dataverse upload (benchmark graphs and sequences). They
  are only in the deposit.

## Check

Each check was run on a copy of the repository files only, with the binaries rebuilt with the `g++` commands of
`REPLAY.txt`:
- `degree21/optimization/check_free_fixtures.py` (`prepare_graph`, `krylov_free`): PASS. Its
  `free_fixtures_verified.json` and the three sequences are identical to those in the repository.
- `degree22/optimization/check_simd_fixtures.py` (`prepare_graph`, `krylov_simd` with AVX-512): 21 tests PASS. The
  folder `simd_fixtures/` is identical. `simd_fixtures_verified.json` differs only in `binary_sha256`, the hash of the
  newly compiled binary.

Other files missing from the repository are generated data (for example the `*_data.m`, `sources*.m`, `hecke_jets*.m` and
`*_sequence.m` files) and superseded copies in `degree22/archive/`. The exception is
`degree12/large_orders/strange_primes_export.magma`, which is Derickx and Stoll's program and is not ours to publish.
