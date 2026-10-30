# An Existing Total-Search Problem Behind This Native Relation

This is a reduction and research pointer, not a new solver or lower bound.
It helps avoid treating an unfamiliar matrix problem as automatically hard.

Given full-row-rank B in F_p^(k by m), suppose its rowspace has minimum
nonzero weight delta>k. Select any k-column basis I. Removing I leaves rank k:
otherwise a nonzero row combination would be supported entirely on I and
have weight at most k. Select a second basis J in the remaining columns.
Let R be the leftover positions, set z_R=1, and compute

    s' = s - B_R 1,  b=B_I^(-1)s',  M=B_I^(-1)B_J.

It suffices to find x with every x_i!=0 and every (Mx)_i!=b_i. Set
z_J=x and z_I=b-Mx. This is an exact polynomial reduction to the affine
Alon-Jaeger-Tarsi matrix-avoidance problem. No extra input promise is imposed
on the ORIGINAL syndrome; any s works. The native output is checked directly.

[Nagy-Pach, Theorem A](https://arxiv.org/html/2107.03956) guarantees such an x
for every invertible M when p>61 and p!=79, with arbitrary one-value exclusions
on both input and output. Thus it applies at p=100003. This is an EXISTENCE
theorem; the scoped source check did not establish a polynomial-time extractor.
Its proof uses group-ring/polynomial identities. Naively expanding those
identities has exponential dimension; no coefficient or nonzero-evaluation
oracle may be charged as a single polynomial operation.

The tower has delta>=12e-3>5e+3=k for e>=8. A constructive polynomial
algorithm for this matrix-avoidance problem would therefore dequantize all
of the current arbitrary-divisor-class search instances, not just one cube
annihilator subclass. Conversely, the current quantum decoder is NOT a
solver for arbitrary AJT matrices: its low-dimensional Schur square and
distance conditions need not survive the reverse encoding B=[I|M].

Highest-value next classical question: can the avoidance theorem be made
constructive for the special matrices M inherited from complete AG codes,
or can two-basis structure plus their product-space information provide an
efficient repair/extraction procedure? A valid proposal must supply an
explicit operation-by-operation cost and actual witness extraction, not
just another nonvanishing or solution-count proof. A failed extraction is
not hardness. Avoid duplicating the already reviewed exact systematic sampler.
