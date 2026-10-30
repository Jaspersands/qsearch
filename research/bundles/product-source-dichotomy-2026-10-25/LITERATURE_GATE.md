# Splitting Literature: Do Not Import A Withdrawn Reduction

2026-10-25. Dependency audit and a conditional composition, not a new
isogeny algorithm or a peer-reviewed repair of either paper.

## Checked Versions

[Kutas--Shen, A Note on Splittings and Endomorphisms](https://eprint.iacr.org/2026/1198),
PDF dated 2026-10-12, 14 pages. Read the whole paper; visually checked page
10. The PDF is retained in sources/2026-1198-revised-2026-10-12.pdf with SHA256
cb5c7617557e12a843f34781172898a90c847453cf09adcf468b76348e7b4852.
Its page-1 changes notice and page-10 warning withdraw Section 4.1 because
the cross-factor Hom modules were not obtained. The abstract and conclusion
still advertise the equivalence. Do not cite those as an established
reduction. Their Splitting problem also excludes certain trivial outputs;
it is stronger than returning any map to a product. The warning retains
the reverse direction subject to its imported assumptions.

[Herledan Le Merdy--Wesolowski, arXiv:2502.17010v2](https://arxiv.org/html/2502.17010v2),
dated 2026-02-02. Checked Sections 2.4, 4 and the input requirements of
Section 6. Proposition 10 reduces HomModule to a GLOBAL Isogeny oracle.
Its construction uses actual full endpoint endomorphism rings, one actual
connecting isogeny, lattice generation and efficient division. The
separable case's double-sided span can be m Hom, not Hom; scalar division
is essential. The output is an efficiently evaluable basis, not merely an
abstract isomorphic lattice. These are imported known algorithms. They
are not implemented or independently re-proved in this pass.

## What A Qualified Global Splitter Would Supply

Here is a sufficient oracle contract, stated explicitly to avoid relying
on the ambiguous application of a same-source matrix formula to different
elliptic curves. On every pair C,D, build a bounded-degree gluing
f:C x D -> A and query a splitter that returns g:A -> F1 x F2 such that
T=g f is polarized and NOT monomial. All maps must have polynomial-size
efficient evaluators, including the required adjoints and degree data.
This is a GLOBAL oracle on new instances, not one supplied split target.

Write T=[[a,b],[c,d]]. If a or b is zero, the equations T^dagger T=[N]
and T T^dagger=[N] force T to be monomial: the nonzero entry in its first
row forces the cross-entry in the other row to vanish. Thus nonmonomiality
makes both a,b nonzero, and b^dagger a:C -> D is a nonzero elliptic isogeny.
Its degree has polynomial bit length in the oracle output. No fixed
smoothness of this connector is needed for the general Hom routine.

Consequently this qualified GLOBAL splitter simulates an Isogeny oracle.
Compose that simulation with the known HomModule reduction on (E1,E2),
(E1,E1), and (E2,E2). Duality supplies the reverse Hom basis. Inserting
these four rank-four modules into matrix corners gives the full rank-16
End(E1 x E2) with actual evaluators. Thus the specifically missing
cross-Hom step is not justified by factor rings alone, but it does have
a candidate repair with the stronger global oracle contract and known
elliptic algorithms. This composition makes polynomially many new queries.

This is NOT a certification of the full withdrawn Section 4.1. Its exact
Splitting promise, initial surface splitting call, good-representation
metadata (including differentials), IKO conversion and downstream
heuristic/GRH assumptions still require their own audit. In particular,
no claim here silently restores the paper's final equivalence.

## What This Does Not Supply To Our Native Candidate

Our candidate supplies a known source order and weak auxiliary values of
ONE hidden isogeny. It supplies neither a global splitter nor arbitrary
elliptic Isogeny/OneEnd oracles, full target factor rings, a full Hom module,
or a target decomposition for a general Jacobian. Applying the oracle
composition to that input would be circular.

The new product-projector dichotomy in PRODUCT_DICHOTOMY.md instead uses
only actual product projections and the existing weak source. It does
not depend on either of the papers above or repair their proofs. The
literature audit and the same-input classical reduction must remain
separate evidence records. Neither establishes general classical hardness
or a quantum advantage for the remaining modeled Jacobian problem.

## Follow-On Division Check: No New Solver

Checked Sections 3.6-3.8 and 4.3 of
[Eisentraeger's AWS 2026 notes](https://swc-math.github.io/aws/2026/2026EisentraegerNotes.pdf)
(updated 2026-02-20). Efficient endomorphism division does not make the
displayed tree search polylogarithmic in its local prime q: Algorithm
3.8.2 tries q+1 first branches and q subsequent branches. Its individual
containment tests are efficient, but the number of tests is not polylog(q).
Applying it at our potentially large ell therefore does not automatically
eliminate the weak elliptic residual. This is a scope check of that
algorithm, NOT a lower bound or a rejection of all division-based attacks.
No new experiment or module was justified by this follow-on check.
