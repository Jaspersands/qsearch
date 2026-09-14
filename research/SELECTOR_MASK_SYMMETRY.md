# A Radial Pure-Mask Search Reduction

Status: derived, review pending. A search-space reduction, not an algorithm,
an all-mask obstruction, a classical dequantization, or a novelty certificate.

## Claim and Scope

Keep the common-query architecture in [the quantum-selector note](SOURCE_SELECTOR_QUANTUM_BOUND.md):
identical standard mixed coset inputs, one shared hidden involution, one fixed
common group-algebra unitary, a common source-irrep partition, classical
source records, and physical discard. The mask is fixed independently of
the inputs AND source records. The final joint measurement on source records
and selector is unrestricted. This last qualification concerns information,
not an efficient measurement compiler.

For a fixed query U and k participating inputs, optimize the class-decision
trace distance over ANY normalized fixed pure mask alpha. The derived reduction
is that a mask with positive radial amplitudes attains at least the same value:

    alpha_radial(s) = sqrt(w_|s| / binomial(k,|s|)),
    w_m >= 0, sum_(m=0)^k w_m = 1.

Thus k+1 weight probabilities replace 2^k complex amplitudes. Relative phases
are unnecessary for the optimal information objective, but coherence BETWEEN
different weights remains essential. This is neither a classical mixture
of fixed-weight states nor a claim that the uniform mask is optimal.

The reduction preserves each weight probability and therefore every exact
lower-tail probability used in [the fidelity bound](MASK_TAIL_FIDELITY_OBSTRUCTION.md).
It does not preserve a particular efficient implementation or final readout.
There is no supplied efficient algorithm for evaluating the objective at
large n,k or finding its globally optimal value.

Subsequent restrictions are in the [vacuum-coherence bound](VACUUM_COHERENCE_BOUND.md)
and [low-occupation support bound](LOW_OCCUPATION_SELECTOR_BOUND.md).
The latter still charges the physical selector support rank, not this
K+1 parameter count. Neither permits discarding arbitrary cross-sector
coherences to combine separate low/high bounds.

Prior-work check (2026-09-14): [Jencova and Plavala, section 4.1](https://arxiv.org/html/1603.01437)
study optimal discrimination of covariant channels and distinguish the
irreducible-input-representation case. Copy permutations here act reducibly;
their maximally-entangled-input proposition does not by itself establish
our particular pure radial reduction. Nevertheless the instrument and
symmetry tools here are standard, and their specialization may already be
known. This limited comparison does NOT establish novelty. The immediate
value is reducing this repository's search space, not claiming a new
general channel-discrimination theorem.

## Source-Record-Valued Schur Channel

Let C_(eta,J)(s,t) be the trace of U_t^dagger U_s against the naturally
weighted source-J input, for eta=0 or h. The output for a selector density
matrix X is

    Phi_eta(X) = direct-sum_J [ C_(eta,J) entrywise-multiplied-by X ].

Each C_(eta,J) is positive semidefinite, its diagonal is the natural source
mass, and these masses sum to one. Hence Phi_eta is a channel. Average the
SAME hidden h only after forming all k-copy products:

    A_J = E_h C_(h,J) - C_(0,J).

For p_s=|alpha_s|^2 define

    f(p) = (1/2) sum_J || diag(sqrt(p)) A_J diag(sqrt(p)) ||_1.

The output for alpha differs from that for sqrt(p) only by a diagonal
unitary, identical for both hypotheses, so it has distance f(p). Zero
amplitudes require no phase choice. Natural source masses stay inside A_J;
conditioning or independently normalizing rare blocks changes the problem.

## Concavity by a Physical Instrument

Let p=sum_l v_l p_l, with v_l a probability distribution. Define diagonal
Kraus operators

    D_l(s) = sqrt(v_l p_l(s)/p(s)) when p(s)>0.

On p(s)=0 coordinates choose D_0(s)=1 and all other D_l(s)=0. These coordinates
have zero weight in every positively weighted input, but the extension is
necessary to make the instrument trace preserving on the entire space.
Then sum_l D_l^dagger D_l=I, and on the source/selector output,

    D_l Phi_eta(|sqrt(p)><sqrt(p)|) D_l^dagger
        = v_l Phi_eta(|sqrt(p_l)><sqrt(p_l)|).

Retain l as a classical outcome. The same channel acts on both hypotheses,
and the trace norm of a classical direct sum is additive. Contractivity gives

    f(sum_l v_l p_l) >= sum_l v_l f(p_l).                  (1)

Thus f is CONCAVE in the probability vector. Do not invoke ordinary convexity
in density matrices in the opposite direction: p -> |sqrt(p)><sqrt(p)| is
not affine. There is no rare-outcome postselection or discarded branch in (1).

These are standard channel/trace-distance tools; this note derives their
specialization rather than claiming a new general channel-discrimination
principle. General channels can benefit from ancillary entanglement; see
[Matthews, Piani and Watrous](https://cs.uwaterloo.ca/~watrous/Papers/LOCCDiscrimination.pdf).
No claim about all channels or restricted final measurements follows here.

## Joint Permutation Covariance

Permuting input positions permutes both the selector bits and the ordered
source records. Because the inputs are identical, the query unitary is COMMON
to all subsets, and the source partition is common, the physical traces obey

    C_(eta,pi J)(pi s,pi t) = C_(eta,J)(s,t).

This holds for each fixed h, not only after class averaging. Unitary
invariance and reindexing the full source sum imply f(pi p)=f(p). Average p
over all k! permutations and use (1):

    f(p_radial) >= average_pi f(pi p) = f(p).

The orbit of a selector string is its Hamming-weight sector, so this average
is exactly p_radial(s)=w_|s|/binomial(k,|s|). The radial mask remains a PURE
superposition. We do not physically dephase weight sectors or average their
density matrices. Enumeration of k! permutations is only a proof device;
the numerical radialization computes weight sums directly.

Optimizing the concave objective over the weight simplex is a convex
optimization problem in the mathematical sense. This does not make its
evaluation oracle efficient: current physical tables still grow exponentially
in copies and factorially in group degree. Floating-point solver convergence
is not an optimality certificate, especially at nonsmooth boundary points.

## Checks and Deliberate Countercontrols

The finite implementation extracts the whole Schur channel independently
from regular-basis U_t^dagger U_s effects for a dense noncentral S3 unitary.
Both k=2 and k=3 retain all ordered source tuples and all three hidden members.
The physical model agrees with the preceding arbitrary-mask channel controls.
It checks positivity, trace preservation, all copy permutations, phase
invariance, the diagonal instrument on both hypotheses, and concavity.
Twenty-six mask probes include strictly positive radialization gains.

Essential countercontrols are not research candidates or oracle problems:

- A non-permutation-covariant diagonal-unitary channel pair has distance 1
  for a chosen mask but sqrt(3)/2 for its radialization. Covariance cannot
  be dropped from the contract.
- A permutation-covariant diagonal-unitary pair distinguishes even and odd
  weights. A coherent radial mask has distance 1; every single-weight mask
  and weight-dephased input has distance zero. Dephasing destroys the result.
- Instruments with zero-probability coordinates still satisfy the full
  Kraus completeness identity, including when one mixture weight is zero.

Finite S3 search supplies actual feasible radial weight vectors, NOT globally
certified optima. At k=2 the best observed distance is about 0.364681,
versus 0.349742 for the uniform mask and 0.334357 for the best single weight.
At k=3 the values are about 0.468169, 0.458166, and 0.446897 respectively.
Classical source-only information already gives 0.305556 and 0.421296.
Those source labels require the quantum front end; this is not a classical
oracle attack or a claim that the quantum inputs are classically available.
These are finite quantum-state discrimination calibrations. The ideal final
Helstrom measurement is not compiled, no growing-degree separation is shown,
and the small improvements do not constitute candidate quantum algorithms.

## Research Consequence

Do not spend search effort on arbitrary position-asymmetric masks or phase
decoration for this fixed common-query information objective. Search exact
weight-distribution families and evaluate their lower tails. Preserve coherent
couplings between weight sectors. The existing high-occupation obstruction
still applies; low-occupation masks and coherent mixtures with substantial
low-weight mass remain unresolved.

`radial_mask_specification` produces an exact O(k)-size normalized state
description and rational lower-tail probabilities without materializing
2^k amplitudes. It is not a circuit compiler. The finite optimizer is a
calibration tool, not a proof-search replacement or a scalable objective oracle.

Source-adaptive masks, position-dependent operations, nonidentical source
partitions, retained physical data, and restricted final measurements need
separate arguments. Any application outside the stated Schur/covariance
contract must supply one rather than changing an assumption flag.

Independent mathematical and novelty review remain outstanding. A failed
instrument identity or physical covariance check must retract this reduction,
not be treated as an optimizer tolerance to relax.
