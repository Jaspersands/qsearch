# Goppa Holdout: Native Task And Quantum Access Audit

Date: 2026-10-30. Status: exact classical mechanism recovered from primary
sources; a naive complex-linear-algebra translation falsified. No quantum
algorithm, general quantum lower bound, or full-size key recovery is claimed.

## Sources And Scope

The complete primary PDFs were obtained through their ordinary browser download
links, after direct automated PDF requests failed. Local snapshots:

| Source | Snapshot | SHA-256 |
| --- | --- | --- |
| [GIJS, 2026/1630](https://eprint.iacr.org/2026/1630) | August 27, 89 PDF pages; `literature_cache/eprint_2026_1630.pdf` | `0de9deb8bfc00c9479e666476df4e71415d5dbcf24b06c9ce5cc5ae5b9af0a8c` |
| [Weis, 2026/1984](https://eprint.iacr.org/2026/1984) | v0.5, October 6, 37 PDF pages; `literature_cache/eprint_2026_1984_v05.pdf` | `822d2cd3cc515143072a543f1bb743ea9b29651d5be03dd56f948e157d196652` |

GIJS Theorems 3.2 and 4.1 prove distinguishers, not key recovery. For binary
Goppa public matrices Y with k rows, set D=n-2t-1. Their basic sufficient
conditions include s(n-1)>dD and

    (n-1) binom(k+s-1,s-1) < binom(k,d).

The structured case is always accepted. The elementary random-case rejection
probability is at least 2^-d, not automatically constant. Stronger kernel-size
conditions, a Reed-Muller weight bound, and genuinely independent held-out
columns give the asymptotic amplification in Corollary 4.2. The public-key
regime is m=Theta(log n), t=Theta(n/log n), k=Theta(n), with the theorem's
other feasibility conditions retained. A failed finite parameter condition
does not refute the asymptotic theorem.

The proof uses homogeneous polynomials to cancel column multipliers, Hasse
derivatives for characteristic-two multiplicity, and univariate interpolation
on an unknown curve. For the random binary case it uses **multilinear**
polynomials and Reed-Muller distance, not a field-size argument over the
extension field. The automatic independent review found no fatal gap in
these stated proofs; this is not external peer review or formal certification.

GIJS Claim 6.2 proves acceptance of clean ciphertext coordinates; rejecting
dirty, correlated coordinates is the missing heuristic step. Its binary
decryption invokes Hypotheses A.2, A.3, A.5. Key recovery in Theorem 7.2
additionally assumes Conjectures C.2 and C.3. These are not consequences of
the proven distinguisher.

## Exact Public Operator

Input: an explicit binary public matrix Y, degree d, multiplicity s<d, and
held-out coordinate tau. No support, Goppa polynomial, hidden parameterization,
private code, or secret-derived intermediate subcode is supplied to the test.

Rows of E are d-element subsets B of the k variables. Columns are pairs (j,A),
j != tau, with |A|<s. With y_j the j-th public column,

    E[B,(j,A)] = 1[A subset B] product_{i in B\A} y_j[i],
    b[B] = product_{i in B} y_tau[i].

The decision is b in im_GF(2)(E). Equivalently, every h with E^T h=0
satisfies h dot b=0. The polynomial coefficient vector belongs to the LEFT
kernel of E. A right-kernel vector is a relation among jet conditions, a
different object used by the later extraction algorithms.

Every jet at the held-out point is excluded from training, while the tested
functional is its value only. Accidentally including its derivatives changes
the experiment. A nonzero training kernel alone is not a distinguisher;
neither is a zero holdout increment after rank saturation.

For d>s, all training jet columns at a systematic unit point are zero.
The unit points still contribute multiplicity zeros in the proof. Changing
the public generator basis must be an explicit operation: the homogeneous
multilinear coefficient space must not silently be replaced by a different
space through Boolean reduction after substitution.

## Matched Classical Baseline

Weis v0.5 improves the lift, removes redundant jet orders and local relations,
and provides matrix-free tiled multiplication. The comparison is no longer
dense elimination or generic decoding alone. Proposition 7's top-order tile is

    (hE)[j,S] = sum_{i<i', i,i' notin S} y_j[i] y_j[i'] h[S union {i,i'}].

The optimized full-size estimates use d=7,s=6 and N=binom(k_short,7).
In Tables 4-5, log2(N) ranges from 38.1 to 42.1; bit-operation exponents
89.4 to 98.4 become 107.3 to 117.2 with the stated per-access square-root
memory charge. These are conditional costs, not measured attacks. The
remaining sequential Krylov iteration counts are still enormous.

Assumption 1 concerns the predicted kernel dimension; Assumption 2 concerns
gradient spanning for the gradient route; Assumption 3 concerns exhaustion
of the column kernel by local and canonical relations for the single-run
route; Assumption 4 concerns the preconditioned solver's defect and output.
The routes do not require exactly the same assumptions. Full-size finishing
tests using secret-generated intermediate data are not end-to-end public-key
recoveries. The demonstrated small TII-253 recovery does not validate standard
parameter practicality. Appendix H retracts an older no-extra-work storage
claim; compare operation, traffic, and storage figures from the SAME version.

### Characteristic-Two Jet Compression

For |A|=r and any t>=1, coefficient counting gives

    sum_{B superset A, |B|=r+t} y^(B\A) D_B F(y)
        = binom(d-r,t) D_A F(y).

The smallest positive t for which the binomial coefficient is odd is the
least significant set bit of d-r. If r+t<s, eliminate order r using higher
orders; otherwise retain it. Descending substitution proves equality of the
full and retained column spans over GF(2), for every point, including zero.
For d=s+1 the retained orders are nonnegative d-2^j, j>=1:
(d,s)=(7,6) retains 3,5; (8,7) retains 0,4,6. This is a classical shortcut,
not a new quantum mechanism, and is not a valid identity over the rationals
after reducing the binomial coefficients modulo two.

## Actual-Operator Counterexample To The Complex Lift

Take k=6,d=3,s=2 and the full-rank public matrix

    Y = [I_6 | a | c | z], held-out coordinate 8 (zero based),
    a = (0,0,1,1,1,0),
    c = (1,1,0,0,1,0),
    z = (1,1,1,1,0,0).

Use one-based polynomial subscripts in the identities below. Removing the
identically zero unit-point blocks leaves E of size 20 by 14. Order each
point's columns by empty derivative, then derivatives 1 through 6. The four
columns at zero-based non-unit indices 1,2,10,11 sum over the integers to

    b + 2 (u_135 + u_145 + u_235 + u_245).

Hence they solve E x=b over GF(2). Over Q, the polynomial

    h = X1 X3 X5 - X1 X3 X4 - X1 X2 X3

satisfies h^T E=0 but h^T b=-2. The exact ranks are:

| Field | rank(E) | rank([E,b]) | Holdout |
| --- | ---: | ---: | --- |
| GF(2) | 8 | 8 | accepts |
| Q, R, C | 8 | 9 | rejects |

This is not a tiny-singular-value artifact. The exact Gram characteristic
polynomial is

    lambda^12 (lambda-1) (lambda-3)^4 (lambda-4)^2 (lambda-5).

The nonzero singular-value condition number is sqrt(5). The normalized target
b/||b|| has squared overlap 4/5 with the COMPLEX left kernel. A precise
complex kernel-projector measurement therefore confidently returns the wrong
answer to the binary task. Improving QSVT accuracy or state normalization
cannot fix this translation.

This matrix is an algebraic regression for the actual jet operator, NOT a
claimed Goppa key or an asymptotically separating distribution. It refutes
an unqualified operator replacement. It does not rule out a specially proved
promise-dependent lifting or a different quantum algorithm.

## Constructive Question And Kill Criteria

The worthwhile unresolved task is to extract a finite-field relation, or
directly extract useful support/locator information, from the compact public
input without enumerating N coefficient coordinates. A circuit for a single
entry of E is not such an algorithm.

1. A characteristic-preserving encoding must reproduce the exact holdout
   decision, including the counterexample above. A real rank or spectral
   proxy without this proof is rejected before scaling experiments.
2. A coefficient-basis quantum implementation of x -> E x over GF(2) uses
   one qubit per binary coefficient, not log2(N) qubits. An amplitude-encoded
   vector uses log2(N) index qubits but does not implement XOR-linear algebra
   by ordinary complex matrix multiplication. A replacement must bridge this
   difference explicitly and pay preparation, workspace and cleanup.
3. A quantum kernel state is not the classical kernel vectors expected by
   the known recovery algorithms. Either charge readout or derive a direct
   observable recovering a consistently labeled locator. Uniform nullity
   estimates must retain their actual normalized signal and precision cost.
4. Compare against shortened, reduced-jet, tiled classical block-Krylov
   algorithms and local-relation quotients. If a proposed compression works
   classically on the same public input, record it as a classical improvement,
   not evidence of quantum advantage.
5. The next useful mathematical experiment is a compact parity-preserving
   representation of the **quotient by local jet relations**, with a direct
   output map to locator data. Merely implementing another complex block
   encoding, counting lifted dimensions, or replacing a search with Grover
   does not answer that question. No such representation is established here.

## Reproduction

`python qsearch.py holdout-jets --write` writes only a scoped algebraic report.
Custom input has exactly `generator`, `degree`, `multiplicity`, `holdout`.
Use `--input input.json --rational` for a bounded exact field comparison,
or `--reduced` for binary jet compression. Writing a supplied input requires
an explicit different `--output` path. No candidate or negative-result row is
automatically admitted, and no cryptographic theorem is inferred from controls.

The core and independent tests verify exact membership/nonmembership
certificates, Hasse expansion, field mismatch, and the spectral certificate.
The finite Goppa fixture supplies only its public matrix to the auditor;
its small dimensions are not an asymptotic GIJS experiment.
Its sufficient interpolation inequality fails (30 is not greater than 33),
its training space saturates, and both it and the matched random control
accept the held-out evaluation. No distinguishing conclusion is drawn.
