# Independent composition review: two arbitrary Gaussian branches

7 November 2026. **ACCEPT the written uniform polynomial-copy/BIT
composition**, with the exact IID-copy, known-Majorana, even-branch and
ordinary-qubit-circuit scope of `TWO_GAUSSIAN_PAIR_LEARNING.md`. This verdict
is based on the bounds below, not on an agent label or the finite control.
It does not assert execution, practical resource bounds, priority, a
classical-input separation, or learning arbitrary Gaussian rank.

Read STATE/TRAPS and the current complete composition, including the
merge-before-projection ordering, explicit polar intertwiners, and corrected
sequential compilation budget. The exact equal-angle RDM and small-nu
lemmas were reviewed separately in `2026-11-07-two-gaussian-core.md`; this
review closes their quantitative composition. No Git, network, API, sweep,
or implementation was used. No previously closed review was edited.

## The collision dichotomy is simultaneous and cancellation-uniform

For normalized coefficients a,b, modifying the smaller branch incurs vector
error at most twice its coefficient magnitude times the branch-vector
error. The same smaller branch can be used for every angle modification.
Swapping the reference branch preserves the physical pair subspaces and
relative angles, which is all the argument requires.

The two squared-error upper bounds are pi^2 A|x_j-x_k| for merging one pair
angle and 8A(1-R_jk) for retaining only two active pairs. If the input is
farther than a0 from the entire four-mode-compressible class, the latter
upper bound must exceed a0^2 for every pair. Therefore

    A |x_j-x_k| <= 2 |nu_j^2-nu_k^2| / a0^2.

Product-branch vector error squared is bounded by the sum of the squared
individual angle changes. A cluster width O(nw) therefore gives total
state error O(n sqrt(w)/a0), with no iterative choice of a new branch or
coefficient at each pair. A=0 and at most two active pairs lie in Candidate
1. The merging is correctly performed before the sentinel projection, so
this inequality uses the original coefficients throughout.

Candidate 1 does not require a covariance eigengap. Its discarded canonical
occupations have total expected impurity O(n^2(a0+delta)) by Weyl and the
covariance perturbation bound. The measured canonical frame, rather than
an estimated individual eigenvector of a degenerate reference, defines
these occupations. A union bound gives the stated projection failure and
O(n sqrt(a0)+n sqrt(delta)) disturbance. Projection of a pure state onto
fixed spectator occupations leaves a pure four-mode conditional state;
success is at least one half in the promised case. Capped conditional
tomography is consequently paid.

## Explicit dimension factors fit the precision hierarchy

Put d=2n. The following elementary bounds suffice; they are independent of
branch normalization, overlap, or a choice of degenerate eigenbasis.

* State trace distance s changes any degree-at-most-four Majorana mean by
  at most 2s. Thus covariance Frobenius error is O(d s), and full fourth
  tensor Frobenius error is O(d^2 s). Entrywise estimation error delta has
  the same bounds with s replaced by delta.
* Orthogonal coordinate changes preserve the full tensor Frobenius norm.
  Passing from Majoranas to creation/annihilation operators is a bounded
  tensor-coordinate map. Hence assembling a two-particle matrix costs at
  most O(d^2) in these bounds, not an exponential expansion.
* The connected fourth tensor subtracts three products of covariances.
  Since ||C||F<=sqrt(d), its perturbation is still O(d^2(s+delta)) when
  s+delta is small.
* Polar rounding at minimum singular value h costs O(1/h). Rounding a
  nearly unitary skew matrix costs a constant. The real and quaternionic
  intertwiners in the note give transporters with Frobenius error bounded
  by a constant times the structure error.
* A near-identity real mode rotation has a Gaussian lift whose operator
  error is O(sqrt(d)) times the mode Frobenius error. This follows by
  summing its canonical plane angles and applying Cauchy--Schwarz. At most
  n disjoint group errors are added; their condition numbers are not
  multiplied over groups.

For a concrete loose common envelope one can use

    K(n)=10^9 (2n)^10.

The powers below are below ten and the finite products of the elementary
constants are below this prefactor. For n>=5, K/B<1/8: the weaker bound
K/B<=1.024*10^6/n^10 already suffices. This makes explicit why the chosen B
dominates the calculation; B is not a substitute for a missing continuity
theorem.

For the initial covariance grouping, ||Htilde-H||op=O(d delta).
A true fourfold value cannot be split because d delta<<w. True adjacent
cluster gaps are at least w/2, cluster widths are O(nw), and common pure
modes enter the sentinel cluster. Projector perturbation, simultaneous
subspace alignment and its Gaussian lift give respectively fixed powers
of n bounded by O(n^(7/2) delta/w) at the state level. Sentinel projection
costs O(n sqrt(w)). The three relevant substitutions are

    sqrt(w)/a0 = b/B,
    delta/w = b/B^2,
    sqrt(w) = a0 b/B.

Their combined dimension factors fit below b, with room for finite matrix
arithmetic. Comparing normalized projected vectors uses contraction before
normalization and the constant success probability; it is linear in the
model error and does not introduce sqrt(b). Projection of the sentinel
branch factors preserves the two-product-branch form on the retained
groups. Thus the asserted b-close equal-angle model in the learned group
spaces is justified.

For a high-nu group, a conservative chain is

    covariance error:                       O(d b),
    polar and real transport:               O(d b/h),
    Gaussian lift:                          O(d^(3/2) b/h),
    assembled R2 comparison:                O(d^4 b/h),
    top vector, reshape, polar, lift:       O(d^5 b/(h tau)),
    sum over groups:                        O(d^6 b/(h tau)).

The reshape includes sqrt(k), and the top-vector estimate divides by tau
only once. Thus K b/(h tau) is a valid generous aggregate bound, certainly
below the note's B^4 b/(h tau)=t/B^2. The R2 matrix error is much smaller
than tau, and the covariance error much smaller than h, validating the
2tau and 2h tests and their respective tau/3tau and h/3h conclusions.

For low-nu groups, c<=9h. Simultaneous orthogonal-branch replacement costs
O(sqrt(n)h); normalized coefficients are bounded because the full branch
overlap is at most c^k. The resulting cat has covariance O(poly(n)h), so
its fourth-tensor top gap is at least k-1. Tensor assembly, top-vector
perturbation, rescaling, polar transport, Gaussian lift and summation over
groups cost at most O(d^6 h), covered by K h<Bh=t. This uses the constant
gap of a nearby cat model, not a constant-gap assertion about arbitrary
estimated fourth tensors.

## Cross-stage ordering and basis ambiguity

The current proof order is sufficient. Apply the high-nu covariance and
high-gap pairing transports on their disjoint groups first. Then apply the
commuting small-gap cat projections. Each loses probability at most 3tau;
their total disturbance is at most sqrt(3n tau). Operations on other groups
do not change the relevant reduced probability. Low-nu replacements come
afterward. Outside projections can change branch coefficients and turn
other factors into local GHZ factors, but do not change a low group's
relative angle or its branch-defined complex structure. Normalizing those
outside factors still leaves their overlap modulus at most one. Thus the
coefficient bound from overlap at most c^k remains valid. There is no
recursive condition-number cost or extra square-root loss at this stage.

The cat and sentinel projections can be comparison-state operations: the
sequential endpoint runs on the actual rotated copies and only needs their
distance from the resulting MPS. If performed operationally during
learning, their high success probability permits charged capped sampling;
neither interpretation supplies a conditioned oracle for free.

The explicit polar intertwiners close a genuine basis-choice issue.
Continuity of a selected degenerate eigensolver basis is unnecessary. A
nearby complex structure is transported to the learned one; similarly,
the antiunitary structures defined by nearby unitary skew forms are
intertwined. After transport, all exact pairing bases differ by a compact
symplectic transformation preserving both equal-pair Gaussian branches.
The normalized R2 eigenvector must be multiplied by sqrt(k) before polar
rounding, as the current text states. Overall phase of that form is a
pairing-basis gauge. Determinant-minus-one frames require the explicitly
allowed known Majorana reflection; the ordinary qubit circuit contract
pays it and its inverse.

Order recovered pairs adjacently and every other retained block
contiguously. At a block boundary the two global product branches give
rank at most two. Inside a pair each branch has rank at most two; inside a
four-mode block at most four; inside a projected cat block at most two.
Hence bond eight follows, including global coherent phase. Charged
fermionic swaps implement the ordering. The preceding errors leave
d0<=10t with substantial slack.

## Endpoint, validation and bit costs

The actual-gate contraction argument in the current text is the correct
one. An actually applied prefix and zero projection are contractions on
the original phase-aligned vectors. When actual success is at least one
half, the normalized conditional states are within 4d0. The reference
conditional state retains rank at most eight across each remaining cut.
Ky Fan therefore gives discarded mass at most 4d0+Delta, regardless of
degeneracy or small Schmidt weights. Compiling the next four-qubit unitary
adds 2kappa, even though using its exact reversed compiled adjoint removes
an additional inverse mismatch.

With Delta<=2t and kappa<=t, total failure is at most 44nt<1/2. This proves
the prefix-success induction used for the capped sampling schedule. The
final successful branch is one projection of a fixed unitary applied to
the original pure state, so disturbance is the square root of total
failure. Final coherent-memory tomography recovers the relative phase;
proper marginal tomography alone is never invoked. The specified t makes
the result, including final-memory error, less than epsilon/10. A fixed
polynomial number of attempts yields the needed conditional samples with
exponentially small cap-failure probability in the allocated logarithmic
budget. No factor 1/eta is required.

Final fresh-copy inverse-preparation tests estimate the two squared
overlaps to a sufficiently small constant times epsilon^2. Since one
candidate has trace error at most epsilon/10, choosing the larger estimate
gives trace error at most epsilon. The known candidate inverse is paid;
the unknown preparation inverse is never input. A union bound composes
moment, tomography, sampling and validation failures without requiring
independence of their adaptive events.

The exponents b=t^4/B^9, w=t^12/B^24 and delta=t^16/B^35 check directly.
The raw moment count is O(n^4 B^70 t^-32 log(n/eta)). All matrices have
polynomial dimension, and their admitted inverse singular values/gaps are
bounded by explicit powers of 1/h,1/tau,1/w. Hermitian eigensolvers, polar
operations and the explicit paired Gram--Schmidt recursion consequently
need only polynomial bit precision and work. Finite arithmetic and gate
synthesis can be allocated errors smaller than delta divided by the
polynomial operation count. Their extra precision is logarithmic in that
count. Known Gaussian plane rotations, fermionic swaps and constant-window
unitaries have polynomial gate decompositions. Ill-conditioned or failed
off-case candidate computations must retain the stated clock caps/default
output; their success is not needed for the dichotomy.

No minimum amplitude, overlap, spectral gap, exact kernel, exact real
input, branch description or supplied Gaussian inverse has entered this
accounting. The new frame argument and the reused paid sequential endpoint
therefore establish the stated written learner. Actual source/priority
scope and the finite control remain separate evidence; neither implies a
new quantum computational separation or executed asymptotic algorithm.
