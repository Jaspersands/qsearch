# Unit-Power Cancellation In Mixed-Order Modules

30 October 2026. Local arithmetic construction and conditional source-tree
analysis; independent automated adversarial review found no fatal error.
This is not human peer review or formal verification. This is NOT an all-prime
ring HSP theorem, emitted quantum receiver, native application or novelty
certificate.

## Question

Can the random-column argument remove a whole mixed-order central grade
with linearly many source slots in the combined rank/class parameter,
without losing the regularity needed for lifting beyond the residue field?

The proposed answer is to reject every kernel vector with even ONE zero
coordinate. A full-support power vector makes the original-degree Jacobian
have the full rank of its label bank. Existing certified pilot coordinates
and regular Hensel lifting then handle non-free, obliquely embedded character
subgroups without assuming an unknown hidden-subgroup basis.

This trades potentially enormous CLASSICAL rejection work for fewer quantum
source slots. It is not uniformly faster than the existing spanning-block
method and does not improve the fixed-degree, growing-rank regime to
polynomial classical time. The latter regime should retain its older solver.

## 1. Unit-Cube Counting

For d dividing p-1, let H=(F_p^*)^d and h=(p-1)/d. Use S=H^M, with NO
zero coordinates. Every projective line meeting S contains exactly h
elements of S, so there are D=h^(M-1) represented directions. For an IID
uniform a-by-M intrinsic matrix A, distinct directions have pairwise
independent kernel events. Consequently

    mu = E[X] = h^(M-1)/p^a,
    Var(X) = mu*(1-p^-a).

Except on probability at most `4/mu+2*p^(a-M)`, the bank has full row rank
and at least mu/2 annihilated directions. Uniform sampling of its full
kernel then hits S with probability at least

    h^M/(2*p^M) >= 1/(2*(2d)^M).

Thus K=2*(2d)^M*B CLASSICAL trials on the SAME bank miss with probability
at most exp(-B)<=2^-B. Root extraction and fair-bit rejection have separate
bounded failure budgets. A smaller execution cap retains its actual, possibly
vacuous probability bound; it is not silently enlarged to K.

The projective argument is the same elementary second-moment method as in
the [field follow-up](RANDOM_COLUMN_REES_PARAMETER_BOUND.md). It is not
claimed as new probability theory. Fixed full-rank banks such as [I|0]
can have NO full-support kernel vector. The success bound requires the
specified random-bank law, not merely a rank check.
The low-count event is analytical, never an operational instruction to
enumerate or count projective directions in the kernel.

## 2. Original Degree And Regular Lifting

Let the original grade exponent be e, with 1<=e<p, and d=gcd(e,p-1).
First obtain nonzero s_i with sum lambda_i*s_i^d=0 in F_p^a. Choose b with

    b*(e/d)=1 mod ((p-1)/d),

and put t_i=s_i^b. Then t_i^e=s_i^d, and all t_i remain nonzero. Do not
pass the reduced-degree witness unchanged to the original-degree lift.
The Jacobian is

    J = e*A*diag(t_i^(e-1)).

Since p does not divide e and every t_i is nonzero, rank J=rank A=a.
The existing pivot-minor lift corrects the witness successively modulo
p^2,...,p^E, solving the stronger full-modulus equations for all rows.
Every scale stays a unit. Finally verify the actual mixed moduli p^a_j.
This is ordinary multivariate Hensel lifting, not a new lifting theorem.
Work is polynomial in matrix sizes, e, E and log p; there is no ring,
support or minor enumeration.

The original exponent condition cannot be dropped just because its reduced
degree is coprime to p. For e=p and labels (1,p-1) in Z/p^2, every nonzero
residue pair (x,x) solves the field equation. A unit lift would require
z^p=1-p mod p^2. Reduction modulo p forces z=1 mod p, whose pth power
is 1 mod p^2, a contradiction. Exact controls retain this failure.

Even d=1 must use a FULL-SUPPORT dependence in this policy. Taking the
first kernel basis vector can leave inactive columns and destroy regularity.
For a zero bank, the all-ones vector is valid; a coordinate-unit vector
does not meet this strengthened contract.

## 3. Paid Intrinsic Coordinates

Let the ambient grade's character module be a direct sum of R cyclic
p-power factors, and C its unknown true character support. Supply no basis
of C. Take P independent pilot labels and use the existing
[certified subgroup compiler](PILOT_SUBMODULE_COORDINATES.md) to construct
the EXACT generated subgroup C', its intrinsic coordinates, embedding and
membership map. Only then reduce fresh bank coordinates modulo p.

If C has cyclic rank r<=R, the incomplete-pilot probability is bounded by

    Pr[C' != C] <= p^(r-P)/(p-1) <= p^(R-P)/(p-1).

This follows from the spanning probability on C/pC and the finite-module
generation criterion. Conditional on complete pilots, the fresh bank is
uniform in C in every resulting frame. An incomplete frame may still
accept, but only after membership and the ORIGINAL ambient cancellation
are checked; acceptance never certifies C'=C.

In particular pZ/p^2 must not be reduced in ambient coordinates before
compiling C': that would erase its nonzero intrinsic residue. A zero frame
requires an entirely zero fresh bank. Nonmembers and intrinsic rank-deficient
banks explicitly abort. Pilots are discarded but still counted as sources.

## 4. Linear Source Arity And Conditional Trees

Let u>=max(c,R+1,2), use P=M=4u and assume p>=16u^2. Every central grade
has original degree e<=c and intrinsic rank a<=R<=u-1. The unit-cube mean
satisfies the same envelope

    mu >= 2^(8u+1)*u^(2u+1).

One grade consumes W=P+M=8u predecessor sources, including all pilots.
A depth c-1 output tree has W^(c-1) leaves and at most that many nodes.
Relative to the field construction, use

    B=ceil(log2(64*W^(c-1))).

The sum over all nodes of bad-bank and incomplete-pilot bounds is at most
1/64. Explicit envelopes for its three summands are

    2^(-5u-2)*u^(-u-2),
    2^(-9u-6)*u^(-5u-3),
    2^(-9u-7)*u^(-5u-3)/(p-1),

respectively for low projective count, deficient bank rank, and incomplete
pilots. The three bounded arithmetic failures contribute at most 3/64.
Hence the ideal tree abort bound is at most 1/16. Classical work and raw
predecessor count are `2^O(u log(u+2))*poly(module bit lengths)`.

This tree argument still REQUIRES pointwise legal conversion and independent
child states conditional on all prior records. It does not establish that
physical source or implement a quantum channel. The executable tree report
deliberately omits complete mixed-ring quantum error/readout accounting and
does not label this an end-to-end HSP bound. In particular:

- Tree leaves are lifted predecessor sources, NOT original oracle queries.
  Installing the existing c-evaluation Rees source construction multiplies
  this leaf count by c; the source-tree report does not include that layer.
- Derived CYCLIC rank over p-power rings does not bound nilpotency class
  as field derived DIMENSION did. Descending subgroups can shrink by powers
  of p while retaining the same number of generators. For example, on
  (Z/p^E)^2 with [x,y]=p*y and 2<=E<p, gamma_j is generated by p^(j-1)*y;
  derived cyclic rank is one but class is E.
- The prime-field small-commutator fallback does not eliminate exponent
  dependence here: commutator order may be p^(sum a_j), not p^R.
  A class-two Heisenberg Lie ring over Z/p^E already has derived cyclic
  rank one and commutator order p^E.
- No all-prime ring parameter theorem follows from the large-field guard.
- Classical source-table enumeration and hidden-coordinate advice remain
  forbidden shortcuts. Original oracle construction is still unpaid unless
  supplied by a justified application.

The modulus cost means the full E*log(p) bits, NOT merely log(E) bits
describing a compressed exponent. Independent reviewer Chandrasekhar
checked the moment and density identities on 1,060 small matrices and
the constants above, and supplied the original-degree and class/rank
counterexamples. Those temporary counts are not a replacement for the
persisted regression suite. The reviewer did not certify physical source
preparation, the full receiver, or novelty.

## Executable Scope

`python qsearch.py prime-power-sde --unit-kernel --write` runs bounded
classical public-label controls and regenerates
`research/reductions/unit_power_module.json`. The command does not execute
the potentially enormous recommended trial caps in the resource example.
Seeded fixtures have known generators solely to supply test labels, not
as advice to the pilot controller. Every successful result is checked in
the original ambient module.

The general earlier approach using an arbitrary-instance diagonal solver
remains available; [Ivanyos--Santha](https://arxiv.org/html/1503.09016v2)
provide polynomial-time fixed-degree field SDE solving with sufficiently
many columns. This new policy makes a different random-input/resource
tradeoff, not a refutation or unconditional improvement of that theorem.
