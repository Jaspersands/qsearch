# Latent Error Coincidence Is Not A Supplied Quantum Instrument

EXACT ACCESS FALSIFIERS / EXTERNAL REVIEW PENDING. No novelty or general
purification no-go is claimed. Run `python qsearch.py dcp-latent-error-access`
and `node research/certificates/dcp_latent_error_access_audit_crosscheck.js`.

## Why This Review Is Urgent

UPDATE 2026-10-16: the target module/contract/artifact now explicitly reports
CONDITIONAL_CLASSICAL_IDENTITIES_PHYSICAL_ACCESS_NOT_SUPPLIED, neutral endpoints,
and the exact q3 critical tie. Its universal strict-dominance assertion has
been removed. The discussion below records the original issue and its exact
falsifiers; it does not assert that the corrected artifact still claims access.

The concurrent `DCP_INTERLEAVED_TREE_MERGE_SYNDROME_PRUNING_AUDIT.md` treats
conditioning on hidden error equality as a syndrome-pruning operation on DCP
leaves. Its classical probability identities may be useful, but they are NOT
a construction of that operation on the supplied phase qubits. Keep such
results conditional on an extra error-label oracle until access is proved.
Do not promote them to physical-receiver evidence or a general negative result.

This review does not overwrite those concurrently edited files. It supplies
independent exact access/density countercontrols and a receipt that refuses to
grant the latent predicate on bare phase qubits.

## Exact Span Certificate

Fix secret s=0, which any secret-independent instrument must also handle.
For a possible error e the phase qubit is
|psi_e>=(|0>+z_e|1>)/sqrt2. Suppose three distinct phases z0,z1,z2 are possible
(nearest-neighbor errors0,+1,-1 have this property for q>=3 and0<p<1).
The source must allow the four unequal product inputs below, as independent
errors with nonzero probabilities do. Three marginal error values alone do
not establish that joint-support promise.

Four UNEQUAL input pairs are(0,1),(1,0),(0,2),(1,2). Their unnormalized product
vectors are(1,z_f,z_e,z_e*z_f). Their determinant is

```text
-(z0-z1)^2 * (z0-z2) * (z1-z2),
```

which is nonzero for three distinct phases. Thus the unequal inputs already
span the entire four-dimensional two-qubit Hilbert space. For a physical
accept effect E>=0, rejecting all unequal inputs with zero probability implies
E^(1/2) kills that spanning set, hence E=0. It therefore cannot accept an equal
input with positive probability. This excludes even an UNAMBIGUOUS equality
herald with a possible inconclusive outcome, not just deterministic comparison.
Known ancillary qubits and adaptive processing still induce a POVM effect on
the same input space; they do not evade this argument.
Arbitrary signal phase rotations preserve the span, so restricting the secret
to nonzero values does not help either.

The module exports exact normalized vectors and Gram matrices in the quadratic
cyclotomic fields for q3 and q4. Their Gram determinants are81/256 and1/8,
respectively. No floating eigenvalue threshold is used. With additional
independent phase qubits, tensor the four unequal pair vectors with any two
independent one-qubit phase states. Every resulting tuple is still not all
equal, and the set spans the whole larger input space. For q4 the squared-norm
Gram determinant at K input qubits is2^(-[3+2(K-2)]*2^(K-2)).

This is a narrow exact-predicate obstruction. It does NOT exclude purification
that allows false-positive syndromes, different encoded/redundant inputs,
orthogonal accessible error registers, multiple source queries or other
quantum algorithms. Two distinct possible errors alone lie outside this
three-state argument. At p0 or p1 the three-error support premise fails.
A different instrument might reproduce an ensemble-level noise law while
accepting unequal hidden errors. It must be derived as an actual channel;
this exact-predicate obstruction does not exclude that possibility.
Correlated sources promising equal errors also lie outside this input class;
the receipt returns UNKNOWN rather than extending the span argument to them.

## A CNOT Does Not Read Error Equality

On phase angles theta1,theta2, a CNOT followed by target Z measurement yields
sum and difference phase branches, each with Born probability1/2. This
probability is independent of whether errors coincide. Exact matrix tests
cover all nine q4 error pairs. The outcome does NOT herald latent equality.

Even IF equality were supplied by an extra oracle, the CNOT sum branch's error
is2e, not e. For q4,p1/2, classical coincidence has probability3/8 and retained
kernel(2/3 at0,1/6 at+1,1/6 at-1). Its retained-error visibility is2/3, whereas
the actual CNOT SUM error distribution has2/3 at0 and1/3 at2: visibility1/3.
Replacing the latter by the former silently changes the physical operation.
The difference branch and its changed signal label must also be accounted for;
they are not free unchanged copies or a general noise-cancellation algorithm.

## A Separate Exact Boundary Counterexample

For q3,p2/3 the error law is uniform over all three residues. Its fundamental
visibility is EXACTLY zero. Repeated classical coincidence squaring leaves it
uniform, so both the pruned and direct-leaf SNR proxies are zero at every depth.
The original claim of STRICT leaf dominance for every p in(0,2/3] is false
at this boundary. Floating cosine residuals must not turn0=0 into strict
dominance. At p0 and p1 the formal retained-kernel visibility gain is also zero,
not strictly purifying/degrading.

The classical inequalities SNR_pruned<=survival<=1 remain different from a
universal dominance theorem, and neither is a complete secret-decoding metric.

## Required Follow-Up

Reclassify classical coincidence-power identities as conditional classical
latent-error calculations, repair the strict endpoint claim and ratio-by-zero
cases, and require an explicit source-access receipt before calling the filter
a DCP instrument. An orthogonal error register is a stronger source assumption,
not something a simulator's private error arrays grant. It would also enable
correction strategies beyond coincidence, so baselines must share that access.

Primary context: [Barnett, Chefles and Jex, Comparison of two unknown pure
quantum states](https://arxiv.org/abs/quant-ph/0202087). The finite phase-family
span proof above is self-contained; it is not a novelty claim or a substitute
for independently reviewing any broader comparison protocol.
