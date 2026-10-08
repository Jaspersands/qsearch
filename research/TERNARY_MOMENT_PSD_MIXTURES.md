# Exact Native Moment Faces And Supplied-Hull Obstructions

LOCAL DERIVATIONS / REVIEW PENDING. This tests a restricted convex hull of
certified points, not the full native degree-two SDP or a new algorithm.

## Source-Aware Facial Reduction

Zero eigenvalues from one-hot normalization and assigned arithmetic are
structural. For every source equation `sum_i a_i Xi=B`, the first and
digit-conditioned rows imply `M*(-B,a_1,...,a_s)^T=0`. One-hot normalization
similarly gives a kernel vector `(-1,1 at this block's indicators)`.

Exact rational RREF of these relations selects free indicator indices F and
a full-column-rank reconstruction map T, with identity rows at F. For every
supplied matrix check

```text
M = T * M[F,F] * T^T.
```

PSD of the full matrix is then equivalent to PSD of that principal face.
Zero rows shared by this PARTICULAR collection may reduce the face further;
they are explicitly hull-specific, not additional constraints on every native
moment point. No missing indicator is globally fixed without proof.

The live42/43-dimensional matrices reduce to faces of dimension14..21.
Every reconstruction is exact. The independent checker establishes relation
rank using an explicit nonzero integer minor and an exact full-rank rational
null map; it does not infer rank from numerical singular values or a fixed
list of convenient primes.

## Convex Mixture Probe

Each of eight winding branches supplies four verified base moment points:
the original point and three re-solved points from the PSD-cut ledger. Strip
only added cut slacks and recheck the ORIGINAL fixed-winding model. A convex
mixture of these points preserves all original source equations and nonnegative
native pair moments, but need not be PSD or globally realizable.

The denominator8 simplex grid has165 weights per branch. Numerical eigenvalues
on compressed faces rank proposals only. The top eight candidates receive
exact PSD/negative-form checks; any accepted PSD mixture needs a full exact
compressed LDL factorization, exact convex weights, and the checked face
reconstruction. An actual relaxation GAP additionally requires independent
proof that the native integer prefix is empty.

The live pilot checks1,320 numeric proposals and64 exact mixtures. ALL64 exact
mixtures are indefinite. This grid result alone proves neither hull nor full
SDP infeasibility; numerical ranking could miss an admissible mixture.

## Stronger Scoped Negative Certificates

From certified negative directions construct an exact PSD dual

```text
Z = sum_j alpha_j v_j v_j^T;
alpha_j >= 0, sum_j alpha_j=1.
```

If `trace(Z*C_i)<0` at EVERY supplied compressed matrix, the same strict
negative trace holds for every convex mixture. A PSD mixture is impossible
because PSD matrices have nonnegative trace against a PSD sum of squares.
The proof retains exact vectors, nonnegative rational weights and every
strict trace value. The small numerical LP only proposes weights; original
rational quadratic forms certify them. No square-root approximation is used.

Four of eight hulls are now exactly excluded:

| Original target | Winding |
| --- | ---: |
| 11366831 | 3 |
| 11672586 | 2 |
| 11672586 | 3 |
| 11672586 | 4 |

The other four hulls remain unknown. No exact PSD continuation was found.
These are FINITE supplied-hull obstructions, NOT full moment-LP/SDP emptiness,
native-source hardness, global inability to find a pair or a speedup. All three
prefixes remain uneliminated by this new pass. Both source reports are hash-pinned.

## Why This Could Be Unimportant

Four LP corners are a tiny subset of the full feasible moment polytope.
Its other points may contain a PSD continuation. Small-grid failure is not
complete even within that hull; the exact SOS certificates close only four
particular hulls. Hull-specific zero rows must not be imposed on a full SDP.
More selected-point averaging can waste time without answering the global
question. Even a complete degree-two exclusion of these empty prefixes need
not improve pair recovery or source-averaged cost.

The next worthwhile step is NOT larger grids or arbitrary cut inflation:
`NATIVE_TERNARY_PSD_SUPPORT_LIFT_TARGET.md` asks whether the four PSD duals
exclude the entire ORIGINAL moment relaxation, or whether an exact support
maximizer escapes them. Principal-submatrix vectors can be embedded in the
full indicator space, so their nonnegative-square functional is valid globally
WITHOUT imposing hull-specific zero rows.

```sh
python theorems/ternary_moment_psd_mixtures.py --write
python -m pytest -q tests/test_ternary_moment_psd_mixtures.py
node research/certificates/ternary_moment_psd_mixtures_crosscheck.js
```

The last command replays all upstream proofs, exact faces,64 negative mixture
forms and all four positive-SOS/negative-trace hull certificates. Human review
remains owed; no full degree-two SDP verdict is claimed.
