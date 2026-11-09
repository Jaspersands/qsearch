# Monomial descent: integrated endpoint review

7 November 2026. Reviewed the current rewritten
`CYCLIC_SUPPORT_MONOMIAL_DESCENT.md`, support review, coordinate review,
and the retained LS source statements. No network/Git/API, implementation,
or finite-control evidence was used. The earlier elementary support and
atom-coordinate derivations were checked for compatibility, not treated as
proof merely because another review accepted them.

**ACCEPT at the stated boundary:** under the class-generator GRH assumption
and the published complete compact S-unit algorithm, the explicit native
input admits a bounded-error quantum polynomial-BIT algorithm returning NO
or a polynomial-size compact solution. Every emitted positive witness can
be verified deterministically in polynomial BIT time without GRH or source
unit completeness. No mathematical/resource blocker remains in this
composition. The single exact control remains pending and is not theorem
evidence. No practical runtime, novelty, classical separation, succinct
splitting-field input, expanded-height, integral-point, or short-point
conclusion is accepted.

## Native contract and support

The input explicitly pays the degree-N Galois field, maximal-order table,
all N automorphisms, growing-rank binary integer action matrices, and
expanded nonzero cocycle coordinates. Group/action/cocycle consistency is
a promise. The monomial action and the residual system use the same
column-vector convention: the exponent of g(u_j) in coordinate i is
`sum_k A_g[i,k] Z_kj`. The support review's left-coset construction is
compatible with this convention and proves that EVERY existing solution
has an S-unit representative. No hidden solution's divisor is computed.

Ordinary class groups suffice; ramified primes are deliberately excluded
from the primitive-valuation step. No narrow class group, Hasse principle,
averaging division, or invariant-lattice saturation enters. The existence
of a unique prime P of E above its restriction q to E^D is correctly used
only for the unramified decomposition subgroup D.

For every needed F=E^C the tower discriminant bound gives
`log|D_F| <= log|D_E|`. The numerical cutoff
`48*max(1,bit_length(|D_E|))^2` dominates the source's natural-log bound,
including discriminant1. Under GRH for the relevant number-field Dedekind
zeta functions, primes of norm at most the source bound generate Cl(F).
Their underlying rational primes are included. No cyclic fixed field or
class group is constructed. Denominator clearing followed by factoring
the denominator and the integral numerator's norm safely covers ALL
coordinate support; rational norm cancellation has not been reintroduced.

## Polynomial-bit accounting

Let L be the full native binary input length. Computing the discriminant
and the numerator norms uses polynomial-size rational/integer determinants,
so their bit lengths are polynomial in L. The numerical cutoff is
polynomial in L; listing its primes by sieving is therefore polynomial.
The additional distinct primes from the factored integers number at most
their total bit length. Their individual log sizes are polynomial in L.
There are at most N primes of E above each rational prime, with
`log Norm(P) <= N log p`. Thus all parameters in BS Theorem1 are polynomial
in L. Maximal-order prime decomposition is paid by the stated checked,
capped finite-field input routines; integer factoring is paid by Shor.
An arbitrary supplied basis does not receive a free encoding: its entries,
all rational coordinate conversions, and automorphism matrices are in L.

The torsion construction is valid in growing degree. Since phi(w)<=N and
phi(w)^2>=w/2, enumeration up to2N^2 contains the exact order w. The algebra
`E[T]/Phi_m` has dimension `N phi(m)<=2N^3`, polynomial coefficient bit
length, and a polynomial-size explicit multiplication table. LS1.10
(retained text212--219) gives all residue fields and projection maps.
Every such factor contains an embedded copy of E; Q-dimension N is
equivalent to degree1 over E. Inverting that embedding recovers an actual
primitive mth root. The largest successful m is w. No factoring oracle
for number-field polynomials or torsion discrete-log advice is hidden here.

BS's complete-generation event, sufficient-precision basis extraction,
and compact recovery provide a COMPLETE free list modulo torsion; adjoining
the computed root makes the list complete in E-S-units. Redundancy is
permitted. Atoms include rational denominator corrections for nonintegral
S-units. Source clocks and output sizes are capped by their polynomial
bounds, including polynomial dependence on log(1/eta).

There are polynomially many expanded atoms and N times as many images;
each image is a rational matrix-vector product of polynomial bit length.
LS1.11(i)/Proposition8.2 acts on THIS expanded tuple, not on huge expanded
unit products. It returns the FULL integral kernel with polynomial-size
basis. Torsion relations are retained; neither rational span nor saturation
is substituted. The direct residual equations therefore form a polynomial
integer matrix with polynomial-bit entries. Integer HNF/SNF produces a
polynomial-bit particular solution when feasible, even when its integer
values are exponentially large. Multiplying binary exponent encodings
preserves compact output length; no large power is expanded.

## Error, verifier, and classical scope

Allocate eta/2 to the actual COMPLETE BS event and eta/2 jointly to all
factoring/finite-field preparation calls, using per-call budgets and fixed
polynomial caps. LS, cyclotomic enumeration, exact integer solving and
positive verification are deterministic. On the joint success event the
computed S is sufficient, the unit list is complete, and infeasibility is
equivalent to no native solution. Detected failure or timeout may produce
NO and is charged to the same aggregate event, not retried indefinitely.
Rank-zero and degree1/torsion-only cases introduce no missing inverse.

Before emitting a positive result, check every residual by recomputing the
full atom-relation lattice from the compact output atoms and input data.
This check needs neither a trusted unit basis nor the support computation.
It also handles arbitrary capped faulty unit output: a verified point is
still a point. Zero/malformed atoms must be rejected before forming powers;
LS already tests units. A claimed relation-basis certificate alone is not
trusted. Consequently a bad randomized branch can cause a false NO within
eta, but cannot cause emission of a false positive after this exact check.

Minor wording clarifications only: the main text's general-Q-algebra
description should say "units" rather than merely "nonzero elements";
here E is a field, so its native application is already correct. Read
"independently check" as occurring BEFORE returning/emitting the solution.

The strongest matched generic classical comparator is the same support
reduction, classical complete S-units, and the SAME deterministic LS and
integer-linear-algebra back end. Classical Hilbert90/permutation cases and
low-degree conic methods remain substantial special-case baselines.
Kutas--Montessinos already supplies quantum S-unit Amitsur-coboundary
trivialization; arbitrary monomial G-actions are not a checked consequence
of its theorem. No failure of a classical implementation or successful
finite control establishes hardness, advantage, or priority.
