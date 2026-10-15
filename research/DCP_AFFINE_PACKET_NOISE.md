# Original-Register Noise In Adaptive Carry Packets

Exact conditional product-noise law and bounded policy benchmark. No new
algorithm, efficient decoder, actual lattice-noise certificate or novelty claim.

Run `python qsearch.py dcp-affine-packet-noise` and
`node research/certificates/dcp_affine_packet_noise_crosscheck.js`.
Regenerate the affine receiver artifact FIRST if its producer changes; this
artifact binds its exact bytes by SHA256, and the checker replays both layers.

## Source Promise, Not A Marginal Assumption

The ORIGINAL supplied m-register state, conditional on the entire public A
and secret, must be a PRODUCT of balanced phase-depolarized inputs:

    rho_i = (1/2) [[1, v_i exp(-i theta_i)],
                  [v_i exp(i theta_i), 1]],
    theta_i = 2 pi <s,A_i>/q, 0<=v_i<=1.

The workbench accepts exact dyadic v_i. This promise is not inferred from
ownership receipts, distinct labels, similar marginal densities, or an
unconditioned independence argument after selection. The actual lattice
source's joint noise is NOT established by this workflow. Arbitrary phase
errors, biased populations, mixtures and correlated bad registers need their
own source law. Every output reports that restriction explicitly.

The existing sine source ALREADY has a conditional balanced template under
its geometric/correct-trial/full-QFT premises. A new bridge test constructs
its PUBLIC exact instrument at B=((17,0),(16,1)),p7,g1,M2,K4, then separately
checks every label against visibility1/4 using a private forward audit.
That audit never enters policy selection. Independent fresh preparations
then give conditional tensor products even after fixing the full public label
tuple. This does not certify the geometric premises, independent physical
resupply, truncated-QFT source, or a growing hard-family trial selector.

Public conservative visibility LOWER bounds can suffice for a fixed policy:
all its utility coefficients are nonnegative, so increasing any actual v_i
cannot reduce expected useful retained visibility. One must not then call the
lower-weight arbitrary-pairing comparator an upper bound for the true source;
all matching comparisons in this artifact concern their specified exact model.

## Exact Physical Pair Law

For computational assignments x,y, product structure gives

    rho[x,y] = 2^-m exp(i(phi(x)-phi(y)))
               * product_(i:x_i != y_i) v_i.

Every allowed chart operation is a basis permutation, and every measurement
projects onto a subset of computational assignments. The diagonal is uniform,
so each initial syndrome has its actual rank-determined mass and every
subsequent binary chart measurement has probability1/2. This remains true
under the specified noise model, with ANY public feedback policy.

A final branch retains exactly the pair (x,x XOR u). Its probability is
2/2^m after accounting for initial syndrome and all complement measurements.
After normalization, the retained density is

    (1/2) [[1, V(u) exp(-i theta_out)],
           [V(u) exp(i theta_out), 1]],
    V(u)=product_(i:u_i=1) v_i,
    theta_out=2 pi <s,a'(x)>/(q/2).

Thus the label is the SAME original signed label difference as in the pure
workbench. Visibility depends on the PHYSICAL XOR mask between the two
surviving assignments, not on how many qubits were originally supplied,
how many measurements were made, how the logical direction was named, or
2^(merge depth). A global trace-distance union estimate misses this structure.

The policy never evaluates theta_out or any secret-dependent mean. Those
angles appear only in separate original-density conformance tests.

## Noise-Aware Objective And Baselines

Use the original useful-descent test: all output-label components even and
at least one nonzero modulo q/2. Score a retained pair by V(u) if useful,
otherwise zero. This is expected USEFUL RETAINED VISIBILITY, not probability
of secret recovery, an efficient likelihood decoder, or quantum advantage.

At a leaf, replace the Bellman score2*useful by2*useful*V(u). Both child
scores still add, with probability charged by2^-m. Input dyadic visibilities
allow exact INTEGER weights at a common binary denominator. No floating-point
optimizer is used. The inherited affine geometry and its exponential policy
discovery cost remain unchanged.

Three comparators prevent favorable-policy reporting:

1. Freeze the PURE-optimal public-feedback policy and evaluate its real noise
   weights. Optimizing labels alone can choose physically long, fragile masks.
2. Optimize ALL static directions separately for each initial syndrome using
   the SAME original-register noise weights.
3. Optimize arbitrary useful computational-basis pairings with edge weight
   V(x XOR y). NetworkX blossom uses EXACT INTEGER-scaled weights. Independent
   JS uses a different exact subset-DP matching algorithm on current controls.
   This is not a general quantum POVM optimum or an efficient growing receiver.

The chosen noisy policy is executable through the same opaque-state port;
the controller only changes public chart choices. Returned visibility is a
prediction UNDER THE PRODUCT PROMISE, not a measurement of an unknown state.

## Live Controls And What Survives

The workflow reuses two unfiltered native controls with pure feedback gains
and the explicitly selected affine-gap counterexample. These are mechanism
controls, not a random-source success estimate. Each is tested at uniform
v=1,15/16,3/4,1/2,0 and a heterogeneous public pattern(1,1/2,3/4,...).

- Unfiltered seed2 at v3/4: useful retained visibility63/128 versus best
  static9/32. The pure-optimized policy happens to remain optimal here.
- The same source under heterogeneous noise: noise-aware7/8, frozen pure3/4,
  best static1/2. Noise can change which public strategy is preferable.
- Selected gap seed94 at v1/2: noise-aware65/512, frozen pure51/512,
  best static64/512. The feedback gain is only1/512, not a major result.
- At v0 every visibility score is ZERO, regardless of apparently useful
  label production. Labels without phase coherence do not imply progress.

The report also gives the EXACT trace distance from the original noisy product
to its ideal pure product:

    D(rho_product, |psi><psi|) = 1 - product_i (1+v_i)/2.

The ideal pure product is an eigenvector with the displayed product weight;
all other orthogonal eigenvectors carry the remaining mass. This identity is
checked against the original tensor-product density spectrum, not assumed
as a generic bound for correlated inputs.

## Falsifying Product Noise From The Same Marginals

Consider the equal mixture of |+>^m and Z^tensor_m|+>^m at m3. Every individual
qubit is I/2, so every marginal visibility is ZERO. The joint diagonal is
still flat. But the retained pair(000,011) has visibility ONE: the common
phase flip cancels on an even-weight difference. The false product-of-marginals
prediction is zero.

The artifact contains the actual joint density with rational entries; the JS
checker reconstructs it and Python independently traces every marginal and
conditions the pair. Therefore flat diagonals preserve branch uniformity but
DO NOT imply product visibility. Conversely, biased input populations destroy
even branch uniformity; an explicit parity-measurement control gives mass0.82,
not0.5. Neither violation is admitted under this conditional model.

## Verification And Remaining Research

Tests replay EVERY final noisy-policy outcome from ORIGINAL mixed product
density matrices, keeping private matrices/secrets in closures outside the
controller interface. Initial syndrome masses, every branch probability,
conditional label phases and visibility are independently checked. Other tests
check exact input trace distances, weighted optimizer comparisons, real
correlation counterexamples, source SHA256, independent weighted matching,
read-only CLI provenance and forged-certificate rejection.

Next high-impact task is the actual source's JOINT noise law, or a compact
correlated-noise model with a proved physical promise. For a known diagonal
Pauli-Z noise distribution p(e), the natural replacement is its characteristic
function E_e[(-1)^(e dot u)], not a product of marginals. Establish its availability
and dependence on public conditioning before treating it as a receiver resource.
Separately, nonlinear fibre pairing and growing-n/growing-t composition still
require efficient constructions. None of these are resolved by this benchmark.
