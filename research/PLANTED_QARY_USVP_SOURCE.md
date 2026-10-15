# Planted Q-Ary Lattice Source And Classical Falsification

This implements the previous source specification. It is NOT a hardness
theorem, new lattice reduction, quantum algorithm or hard-instance claim.
It supplies actual public integer lattices instead of chosen phase oracles
or random-looking unimodular disguises of diagonal lattices.

## Public Problem And Exact Basis

A private dense primitive ternary vector u is planted in the modular kernel
of H over an odd prime field q. In the ideal distribution rows are independent
uniform on u^perp; the reproducible implementation uses private seeded PRNG
fixtures, not a formally certified IID sampler. The generator
accepts the FIRST full row rank matrix. It never rejects on uniqueness tests
or classical attack success. Every attempted matrix/rank and both PRNG seeds
are private calibration records. They are not algorithm inputs.

The solver receives q,H and a public integer basis for Lambda=ker(H modq).
The typed public lattice and private generator result have distinct interfaces;
classical attacks reject the latter as input. Knowing that this benchmark
has a low-alphabet plant is an exploitable FAMILY PRIOR, not a generic-SVP
claim. Private solution lengths/coordinates and seeds are not passed.

FLINT's arbitrary-modulus prime-field RREF supports q beyond a machine word.
Every admitted q now has a recursive Lucas q-1 order certificate. A probable
prime test is only a quick rejection filter, never the field proof. The
independent checker uses modular powers/gcd and already-certified factors
to establish each prime exactly. Factoring q-1 and finding the witness are
benchmark/certificate generation costs, not an uncharged solver primitive.
For pivots P and free columns F, the basis rows are q*e_P and e_F-C*e_P,
where C is the public RREF free block, optionally centred moduloq. Every
row is checked for kernel membership, and absolute determinant equals q^m.
Since full rank H makes the kernel index q^m, this is the FULL lattice,
not a hidden sublattice. No planted vector is used to construct the basis.

## Distributional Uniqueness Certificate

For a primitive ternary u, any integer v with ||v||2<=R<q/2 that is not
parallel to u is also not in span_Fq(u): centred lifting of alpha*u has
the SAME signed scalar on every nonzero coordinate of u. Consequently
each unconditioned row of u^perp annihilates such v with probability1/q.
The union bound over its enclosing box gives (2R+1)^n/q^m.

Conditioning on full rank cannot be ignored. The exact probability is

    P_rank=product_(i=0..m-1)(1-q^(-(n-1-i))).

The ledger stores this FACTORED, not as a giant decimal fraction. For q>=3
and m<n-1, the rank failure union is less than
1/((q-1)*q^(n-m-1))<=1/6. Thus P_rank>=5/6 and a conservative accepted-
distribution uniqueness failure bound is

    min(1, (6/5)*count_bound/q^m).

The integer-point count uses the tighter of the box and a proved Gaussian
volume bound. Disjoint unit cubes around integer points lie inside radius
R+sqrt(n)/2; the Gaussian integral bounds unit-ball volume by
(sqrt(2*pi*e/n))^n. Since sqrt(2*pi*e)<5, an exact integer upper bound is
(5*ceil(R/sqrt(n))+3)^n. The ceiling uses integer square comparisons.
Unlike an oversized fixed q near n^12, the default prime is selected BEFORE
attack outcomes as the smallest prime above the exact conditional-bound
threshold for failure target2^-16, also requiring q>2R. Statistical uniqueness
does not get silently strengthened just to make the plant easier to recover.

R is the exact ceiling of G*sqrt(support(u)), computed by integer squares.
If R<q/2 and no nonparallel vector has norm<=R, primitive u is shortest and
the lattice is G-unique up to sign. Invalid radius/scope yields UNKNOWN.
A replayable integer inequality yields a dyadic failure upper bound; no
floating underflow or decimal probability expansion is used. Rank-attempt
abort probability is separately bounded by6^(-max_attempts).

These are distributional source statements, not certification of a specific
large H or computational hardness. A separate complete finite radius census
can certify an individual calibration ONLY after enumerating the whole
sphere-containing box and checking EVERY nonparallel kernel vector. A cap
never licenses absence, uniqueness, hardness or quantum advantage.

## Serious Public-Data Attacks

Implemented baselines:

- Zero-column and equal/opposite-column recovery of support1/2 vectors.
- Public FLINT LLL with exact Gram mode, exact T*B=R verification, unimodular
  transform, output membership/norm and elapsed time.
- Complete meet-in-the-middle ternary kernel search. The two shortest left
  representatives per syndrome retain the zero-vector exception, so the
  returned nonzero vector has minimum ternary norm when the search completes.
  Input states and modular dot-product work are recorded. Over-cap is UNKNOWN.
- Public centred modular nullspace basis construction, not a planted-basis
  disguise. Its full index/membership certificate is checked independently.
- Complete radius enumeration only in bounded calibration controls.

Outputs are compared with the private plant ONLY after the public attacks
finish. A nonparallel short vector falsifies that instance's uniqueness event;
recovering the plant falsifies the tested regime as a quantum signal. Neither
is a no-go for unique-SVP or all classical algorithms. Exact quality factors
are retained; observed LLL quality is not a general algorithm guarantee.

BKZ/fpylll is unavailable in the current runtime, so it is explicitly NOT RUN.
General MILP/bounded-SIS attacks remain NOT IMPLEMENTED. Do not interpret
those omissions or a work cap as classical failure or hardness.

The current sweep covers dense planted dimensions4,8,12,16,32,64,128 and a prime
above2^80. Conservative polynomial-gap promises often make these small
instances easy for LLL. That is a falsifier to preserve, not a reason to
filter generated instances until they look promising.
The initial larger probes also recover the plant publicly with LLL at64
and128 dimensions. This is not a universal asymptotic LLL guarantee: retain
the exact public transformation and the individual finite-regime falsifier.

## Connection To The Quantum Source

Public bases can be fed to the existing clean cube/DCP compiler, but this
pass does not benchmark a quantum receiver. Cube uniqueness/width constants,
LLL coordinate bounds, bad-register budget, and paid outer residue/coordinate/
length guesses remain separate obligations. Correct guesses inferred from
the private plant would be calibration advice, not a discovered algorithm.
If public LLL already finds the short direction, an ensuing phase-state
calibration is not evidence of quantum advantage.

Run `python qsearch.py planted-qary-source` and
`node research/certificates/planted_qary_usvp_source_crosscheck.js`.

No speedup candidate, broad active negative or novelty is admitted. This
family is a more controlled search substrate, not a result.
