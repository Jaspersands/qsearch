# Large-Prime Source: Input Audit And Projective Calibration

2026-10-25. Conditional source repair with exact supplied-map controls.
No native curve backend, unknown-isogeny recovery, independent review or
quantum execution. This is not a first quantum IsERP algorithm or a novelty
claim. Earlier hashed bundles are retained; the contract below supersedes
their common-scalar INPUT requirement only when bridge queries are available.

## Primary-Source Comparison

The accepted Chen--Petit EUROCRYPT 2025 manuscript is now retained with its
institutional provenance and hash in SOURCE_MANIFEST.md. Printed pagination
is one less than PDF pagination. Its Definition 13 (p.9) permits a generator
of each point-image subgroup, not a common scalar across a basis. Theorem 3
(p.3) already covers general-degree quantum IsERP heuristically. Proposition
26 and Remark 27 (p.16) introduce heuristic norm-solving in the upstream
suborder-to-weak-evaluator step. Theorem 30 and Remark 31 (pp.21-22) separately
analyze powersmooth lifting. Some auxiliary heuristic details are deferred
to an external appendix, not included in this accepted manuscript. Section 7
(p.27) leaves heuristic removal open. Therefore bypassing powersmooth lifting
alone does not establish an unconditional full-suborder result.

[Accepted manuscript](https://pure-oai.bham.ac.uk/ws/portalfiles/portal/259384467/suborder_to_endomorphism_ring_2_.pdf)
and [publication record](https://research.birmingham.ac.uk/en/publications/computing-the-endomorphism-ring-of-a-supersingular-elliptic-curve/).

## The Mismatch In Our Input Contract

The double-level source and native membership baseline currently use a
single scalar on an ordered small-prime torsion basis. Raw pointwise weak
answers do not guarantee that. If T is the true torsion action, raw columns
give T*diag(a_i), so conjugating a source operator by those columns can
compute the wrong target operator. Preserving the Weil pairing up to a scalar
in dimension two does not repair this. The earlier per-column counterexample
remains a valid falsifier of that naive procedure.

Here is a conversion using only the ORIGINAL weak evaluator on small-prime
points. It neither grants a stronger oracle nor reconstructs a large-order
torsion point. The conversion is standard projective-frame linear algebra;
its role here is to make the input comparison exact.

## Projective-Frame Calibration

Assume one genuine global isogeny phi, and a prime r at which its torsion
action is invertible. Let P_0,...,P_(d-1) be an actual ordered basis, where
d=2 for an elliptic curve or d=4 for a surface. Point operations, equality,
fields and basis generation are paid inputs. Query the weak evaluator:

    R_i = a_i phi(P_i),  a_i in F_r^*.

For every j>0, query P_0+P_j, obtaining B_j=c_j phi(P_0+P_j).
Find its coordinates in the raw target basis:

    B_j = x_j R_0 + y_j R_j,
    x_j = c_j/a_0,  y_j = c_j/a_j.

All other coordinates vanish and x_j,y_j are nonzero. Replace R_j by
(y_j/x_j) R_j, and retain R_0. The resulting tuple is exactly

    (a_0 phi(P_0), ..., a_0 phi(P_(d-1))).

This proves the conversion for every mask assignment, including fresh masks
on repeated inputs. No consistency of the evaluator's scalar choices is
needed. It uses 2d-1 weak point calls: THREE for an elliptic basis, SEVEN
for a surface basis. The common scalar remains unknown and need not be
learned. Calibration may differ between primes, which the previous source
already permits.

Cache this tuple ONCE at each auxiliary prime and reuse it across all copies
and all coherent group queries. In particular, phi x phi uses two copies of
the SAME calibrated elliptic tuple, not independently calibrated copies.
Then scalar cancellation in conjugation and the common marking masks used
in the previous proofs hold exactly. This is classical preprocessing before
coherent evaluation, not an uncontrolled oracle call inside a superposition.

## Explicit Cost And Limits

The implementation takes actual point-operation callbacks. Its coordinate
finder enumerates r^d points, charging O(d*r^d) group operations and O(r^d)
storage; it also checks source and target bases. The receipt records both
tables, totaling 2*r^d entries. Point equality/hash and arithmetic costs are
additional. These costs are polynomial only because all requested r are
bounded polynomially in the paid input length and d is fixed. They are NOT
polynomial in log(r) for arbitrary large torsion. The budget guard rejects
large tables before weak queries. No discrete-log shortcut is assumed.

This conversion applies to the auxiliary prime transcript in the current
source, including the native classical membership baseline. It does not
turn an insufficient basis-only transcript into an evaluator, support
arbitrary composite torsion, prove a global isogeny promise from a few calls,
or remove field/geometry/canonicalization obligations. A malicious function
can agree on every queried frame point and disagree elsewhere; a test makes
that limit explicit.

## Falsifiers And Executed Controls

- Exhaust all nonzero masks for frames at (r,d)=(3,2),(5,2),(3,4): 200
  mask assignments. Each produces exactly the first mask times the supplied
  invertible linear map, with the claimed calls and table counts.
- In the known characteristic-11 order, use the SUPPLIED phi=1+i and
  alpha=(1+j)/2. At primes 3,5,7,13,17 raw independently masked columns
  give wrong conjugation; calibrated columns give the exact rational
  conjugate and can be reused across both copies. No curve point is made.
- Two distinct invertible linear maps at r=5 have identical weak basis
  answers but different sum-point lines. This proves why basis-only data
  do not suffice, without claiming two independently instantiated curves.
- Reject zero masks, dependent bases, degenerate bridges, extra bridge
  coordinates, nonprime levels and unaffordable coordinate tables.

Passing these controls is not an independent proof review, geometric source
execution, classical-hardness result or algorithmic speedup. The unchanged
central risks are dimension-16 source realization, uniform canonical marked
outputs, exact field descent, reversible cleanup, and a matched classical
attack exploiting actual geometric data rather than Boolean equality only.

## Next Scientific Question

Can a full evaluable suborder provide the required SMALL-prime projective
transcript directly by intertwining its two torsion representations, without
first constructing a weak evaluator for arbitrary-order points? Linear
intertwining is straightforward locally. Its link to one globally oriented
isogeny of the promised degree is not automatic. Prove that link, or falsify
it, before replacing any upstream heuristic in the overall algorithm.
