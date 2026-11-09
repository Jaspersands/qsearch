# Reduced norm witnesses: final integrated composition review

7 November 2026. **ACCEPT the written bounded-error quantum polynomial-BIT
SEARCH composition under explicit GRH and the stated expanded-input/compact-
output contract.** No fatal mathematical or resource gap was found. The two
clarifications requested during this review are now explicit in the main
note: small-atom/HNF implementation of the compact cochain search, and T0
counting all scalar circuit nodes, including leaves and output slots.

This verdict is conditional on the native field/central-simple-algebra
promises and the actual imported arithmetic theorems. Positive construction
certificates are deterministic classical polynomial-bit checks and sound
without GRH. It is not a theorem about arbitrary submitted arithmetic
circuits, expanded/integral/short witnesses, minimal modules, practical cost,
novelty, a classical separation, or an executed quantum solver.

Read current STATE/TRAPS, the actual integrated note and both scoped reviews.
Checked the relevant Goldstein--Schacher Lemma1/Theorem2, KM v3 Algorithm1
and Theorems3.10/4.12/4.13, LS1.10/1.11 and their expanded input convention,
and the corrected S-unit Theorem1, adjustable completeness Theorem5 and
compact-output Proposition7. The prior relative-norm source interface is
reused within its stated scope. No Git, network/API, implementation or
finite-control rerun was used. Acceptance does not follow from review
labels or finite examples.

## Native promise and finite support

The input includes compatible expanded K/maximal-order arithmetic, expanded
CSA structure constants and identity, and an expanded target a. Numerical
[K:Q] and degree n of A are charged. Zero and n=1 are handled directly.
The exact real-signature test supplies the only mathematical NO outcome;
source failure, a failed check or an exhausted clock must return ABORT.

The Z-order construction is valid: after choosing a rational basis starting
with1 and clearing structure-constant denominators by M, the basis
1,Mb_2,...,Mb_R is multiplication closed. Its ordinary Q-regular trace
discriminant is a nonzero integer of polynomial bit length. It is essential
to factor this actual discriminant and decompose every selected rational
prime in the supplied maximal order, rather than use a good-prime
power-basis shortcut.

The support proof is sound. Outside that discriminant the reduced regular
trace pairing is nondegenerate, so the reduction's Jacobson radical is zero.
Its simple factors are matrices over finite fields. In the complete order,
lift orthogonal idempotents; cross Peirce modules vanish by Nakayama. Lifting
matrix-unit equivalences reduces each block to a corner whose Z_p-rank is
its finite residue-field degree. A separable primitive-element polynomial
Hensel-lifts in that corner; reduction, equal ranks and Nakayama identify
it with the unramified field order. Comparing centers then shows A is
split at every K-place above this rational prime. These lifts are used in
the proof only; no noncommutative maximal order or p-adic computation is
requested from the algorithm.

The K-regular trace of x^2 is a DIFFERENT trace. Its real signature excess
is +n for M_n(R) and -n for M_(n/2)(H), proving the real ramification test.
Expanded congruence diagonalization, root isolation and sign determination
have polynomial-bit inputs and output sizes. HMS imposes positivity only
at the latter places. The elementary bound
alpha=1/(d_a U_a^([K:Q]-1)) is a valid polynomial-bit positive lower bound
for every nonzero |sigma(a)|; it requires no supplied embedding separation.

## Prescribed field: all finite and real places

The finite-field density argument is correct, including g=2,4 and composite
g>=6. On a proper maximal subfield indexed by a prime ell|g, the larger
norm is the ell-th power of the smaller norm. This gives the stated
intersection bound and at least one third full-degree elements in every
nonzero norm fibre. Consequently uniform monic degree-g polynomials with
the prescribed constant have irreducibility probability at least1/(3g).
Residue sampling, Frobenius/gcd tests and capped trials require no DLog or
finite-field norm-preimage oracle.

For a finite place, v may be NEGATIVE. Taking k=floor(v/n) still leaves
0<=v0<n, and the constructed root has valuation k+h/e. A lower or higher
valuation makes the leading or constant term uniquely minimal. Its reduced
denominator forces ramification index at least e, while the residual
degree-g irreducible polynomial forces residue degree at least g. Thus the
degree is n. This proof makes no tameness assumption and remains valid
when the residue characteristic divides e. When v0=0 it reduces to the
usual unramified residual-polynomial construction.

All valuation magnitudes are polynomial NUMERICALLY because a and the local
coefficients are expanded with polynomial bit size. A basis element of q
outside q^2 gives valuation1 without principalizing q. For a local unit
written b'/d' with a nonunit rational denominator, the HNF congruence
d'z=b' modulo q^(t+1) is valid because d'O_K+q^(t+1)=q^t. No invalid modular
inverse is used. Negative uniformizer powers are expanded only to the
polynomial numerical exponents already bounded here.

The denominator-adjusted CRT is quantitative and correct. With
E_q=v_q(D)+1+|v_q(c)|, the global numerator N_i satisfies the required
congruences. M=Norm(I) obeys M O_K subset I. The choice T=1+M2^s is a
local unit and preserves every coefficient congruence AFTER division by D.
This is why division by an arbitrary large denominator would not suffice.
The binary sizes of D,M,T,N_i and the coefficients are polynomial; there
is no loop of numerical length M or T.

The conjugate bound U and the stated polynomial-size s ensure free
coefficients are at most alpha/(4n) at every real embedding. For a
nonsplit real place, n is even and a>0; the separate |x|<=1 and |x|>=1
bounds prove P(x)>0. Adding prime2 guarantees at least one finite local
irreducibility, hence global irreducibility. Local degrees n at the
selected finite places and degree2 at nonsplit real places meet the
actual splitting criterion. All other places are already split. Therefore
F=K[X]/P is a genuine degree-n splitting field and N_F/K(theta)=a.
This construction is nonintegral in general and does not contradict
integral outlier results.

Expanded tower arithmetic for F has polynomial size. If a source requires
a single primitive-element presentation, the ordinary separating linear-
combination and linear-algebra conversion is polynomial-bit: avoid the
finitely many collisions between the [F:Q] embeddings using a grid of
polynomial numerical size, then compute the multiplication characteristic
polynomial and basis change. No normal closure is constructed.

## The split source and compact cochain search are actually paid

Apply KM to the PROMISED SPLIT algebra A tensor_K F over the constructed
number field F. Fact2.1 pays field maximal orders using charged factoring;
it does not supply a maximal A-order. Algorithm1 produces a polynomial-size
expanded auxiliary etale H, cocycle c and presentation Phi. The finite
sampling steps can be capped with verified success. Their exact linear
systems and bounded-size sampling grids keep coordinate heights polynomial.

The relevant absolute dimensions are d*n^2 for H, d*n^3 for U=H tensor H,
and d*n^4 for W=H tensor H tensor H, where d=[K:Q]. All tensor products
and coefficient maps are expanded commutative-algebra data of polynomial
size. The source's support uses ramification, class generators under GRH
and the finite support of the EXPANDED cocycle. Factor-field discriminants
and cocycle norms have polynomial bit length. The corrected S-unit theorem
is uniform in degree, discriminant bits, prime count and prime-norm bits;
its adjustable completeness budget must be distributed across all calls.
Full torsion is retained componentwise. An independent finite-index list
would not suffice.

The explicit adaptation of KM's coordinate step avoids a compact-input
misuse of LS. Retain small atoms beta_l and binary exponent columns for
every compact U S-unit generator. Lift component atoms as 1-e+e*u, map
them by the three insertion maps to W, append c, and compute the FULL LS
integer relation lattice Lambda for this expanded tuple. If E is the
integer exponent map for the coboundaries of the generators, solve

    E*z-e_c in Lambda

by integer HNF with preimages. Complete generation and KM's support theorem
guarantee a solution on the source-success event. Polynomial dimensions and
entry bit lengths give a polynomial-bit solution and final atom exponents.
Neither large unit values nor compact sums are passed to LS. This pays
FINDING alpha, not merely verifying a lucky alpha. Source failure cannot
produce a false accepted coboundary, although it can cause ABORT.

## Regular module and deterministic positive certificate

The module V=F^n has K-dimension n^2. If A=M_r(D) with deg D=m and n=rm,
its simple left module has dimension nm and its regular module has r copies.
V has exactly the same multiplicity and is therefore the regular module.
This is an existence/transport statement, not a minimal-ideal algorithm.
The determinant polynomial for w has degree n^2 and is nonzero; the grid
of size4n^2 gives cyclicity probability at least3/4 irrespective of the
possibly huge values in the compact splitting map.

The verifier must check the actual expanded compatible F/K and H/F data,
etaleness and ranks, and Phi's invertibility and multiplication identity
against the ACTUAL input CSA on basis pairs. A Brauer-class label alone is
insufficient. It recomputes LS relations on the small mapped atoms and c,
and checks c=delta(alpha). Inverse atoms are expanded and checked while
still small. The subsequent map is reconstructed canonically as

    trace_map o multiplication_by_alpha o Phi^-1.

The identity alpha_ij*c_ikj=alpha_ik*alpha_kj proves multiplicativity with
the stated orientation. Etaleness gives the untwisted trace-pairing
isomorphism. Thus no homomorphism PIT on an arbitrary submitted rho is
needed; an arbitrary alternative rho is not accepted by this format.

With B_w invertible, T_w(b)=rho(b)w is a left-module isomorphism and
T_w(1)=w. Scalar theta commutes with this left action, so its transport is
RIGHT multiplication by x=T_w^-1(theta*w). Its characteristic polynomial
is P^n, and regular right multiplication has characteristic polynomial
redchar_x^n. Monicity gives redchar_x=P and Nrd(x)=a, including the constant
term sign. No explicit embedding or minimal module is assumed.

Berkowitz/Cramer circuits are polynomial-size and division free until the
final proven-nonzero determinant inverse. Their canonical construction is
part of the output format. Exact rational reduction and any nonzero
coordinate of D_w in the FULL finite K algebra prove D_w!=0 in K. The
finite algebra need not be a field and D_w need not be a unit there:
no inverse of D_w is evaluated for this test. Field inversion in the final
output is valid because K is a field and D_w is now proven nonzero. Its
rational adjugate/norm compilation has a logically nonzero denominator.

The submitted output DAG is compared syntactically with this construction.
The verifier therefore proves the norm by exact construction identities;
it neither expands the enormous answer nor tests general additive circuit
equivalence. Certificate soundness does not require checking the search's
maximal-order computations, S-unit completeness or local field construction:
the expanded presentation, cochain relation, field norm and nonzero cyclic
determinant independently suffice.

## Prime height bound, finite clocks and final disposition

The repaired T0 counts all scalar DAG nodes, including rational leaves and
output slots. The recurrence for unreduced rational numerator/denominator
bits is b_(j+1)<=2b_j+1; hence
B0=2^(T0+2)(H0+1) is a valid EXPONENTIAL expanded bound. At most (T0+1)B0
prime divisors are bad for all needed denominators and one fixed nonzero
coordinate numerator. Only log B0 enters the chosen prime bit length.

The displayed b-bit formula dominates this count by the explicit dyadic
prime-density bound, with ample slack. Uniform b-bit integer sampling and
deterministic primality testing, capped at O(b log(1/delta_gen)) trials,
produce a uniform prime conditional on success. Atoms and w must be fixed
before choosing a fresh prime. This gives false negatives/exhaustion only,
never a false positive nonzero certificate. All expressions fit the
uniform bit bounds for the finite w grid.

With cyclicity at least3/4, prime-generation and bad-prime errors at most
1/8 each give combined success greater than1/2. The stated logarithmic
trial cap supplies the eta/4 endpoint budget. The other three eta/4
budgets cover support arithmetic, prescribed residual polynomials and the
expanded-front-end/complete-S-unit computation. Here "complete source" means full
group generation, not lattice saturation of the multiplicative relations;
the latter relation lattices must remain exact and nonsaturated.
All internal source sizes and random clocks are capped. Every failure is
ABORT; NO is issued only by the exact HMS sign criterion.

The actual amended main note now contains both requested interface repairs.
The complete conditional search theorem and its deterministic classical
positive construction certificate are accepted. Classical HMS already
settles existence; the proposed contribution is the bounded-cost compact
SEARCH composition. Retain the classical splitting/class-unit and special
quaternion comparators, and leave priority, novelty, expanded output and
any quantum/classical separation unclaimed.
