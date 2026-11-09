# Compact isotropy over arbitrary number fields

7 November 2026. Reviewed WRITTEN bounded-error quantum polynomial-BIT
isotropy decision and COMPACT isotropic-vector construction for every
explicit growing-degree number field and nondegenerate growing-dimension
form, under EXPLICIT GRH. Source/descent/local/composition reviews and one
focused classical/algebra control are complete. This is a deduction from
published arithmetic algorithms and the proofs below, not a human-reviewed
or formally verified theorem, implementation, novelty or speedup claim.
No algorithm is inferred from finite tests or AI acceptance labels.

## Native question and selection

Given a number field K of arbitrary charged degree n, a monic defining
polynomial, explicit maximal-order integral basis/multiplication table,
and an expanded nondegenerate symmetric d-by-d matrix Q over K, decide
isotropy and return a NONZERO isotropic vector if one exists. Both n and d
grow. The output is polynomial-size arithmetic circuits over the
supplied K basis, with a charged bounded-error classical verifier. Expanded,
short or integral points, repeated compact-input Witt decomposition, and
cryptographic short witnesses are different contracts and are not claimed.
Target: bounded-error quantum polynomial BIT time under EXPLICIT GRH.
No class group, unit basis, splitting, point, field closure or local root
is supplied as advice. Failure tolerance eta is charged logarithmically.

The mechanism reuses known quantum central-simple-algebra splitting
and supplies a paid small-dimensional descent and local-to-global reduction.
Its value is an explicit end-to-end arithmetic endpoint. Classical index
calculus/norm/S-unit methods and LLL remain competitors; factoring-oracle
algorithms already handle rational forms and special quadratic base fields.
Rational dimension >=5 has stronger algorithms avoiding factoring under GRH. No
classical hardness, separation or novelty follows from the general route.

STATE/TRAPS and corpus been-tried/baseline lookups preceded primary-literature
inspection. Independent selection also screened the full-table OPI
anchor/decoder route: |C|<=2^D and complete radius-r list cap L imply
Vol_q(m-k,r)<=L*2^D, hence r<= (D+log2 L)/log2(q-1). The existing random-table
flat bound D=O(k log t), t=log2 q, gives only vanishing relative radius for
polynomial L. This rejects importing that positive-radius decoder, not
every quantum method. Native Legendre still lacks a paid nonsplit
resultant operation. Neither supplies a constructive replacement for the
arithmetic candidate in this pass.

## Actual-source boundary and cheapest falsifiers

Retained primary texts and hashes: audits/sources/global_isotropy/source.json.
Actual Koprowski 2111.08569v2 (12 March2025) Algorithms1/2/4 construct points
using squareclasses, norms and weak approximation. AppendixA's inverse
product of bad-prime norms does NOT establish polynomial iterations in
coefficient BIT size; a B-bit prime can contribute 2^Theta(B). A weak bound
does not establish actual exponential runtime. Its numerical discriminant
bound likewise does not pay a log-discriminant clock.

AppendixC uses direct local constructions, NOT squareclass enumeration.
Two literal qualifications: Algorithm5(3a)'s local square premise need not
give an exact global square root (Q,p=3, a=d=1,b=13). Algorithm6's
2k>v(a)+v(b) is insufficient for arbitrary fractional inputs: a=1,b=1/27,
d=1/3,k=1 gives 1+(1/27)*3^2=4/3=d*2^2, the forbidden class. These are
source-interface defects, not a general isotropy impossibility. Correct
finite precision and arbitrary-sign valuations must be paid below.

Kutas--Montessinos 2307.00261v3 Theorem4.13 ALREADY gives under-GRH quantum
polynomial splitting of a promised split CSA. Its etale algebra need not be
an irreducible extension; no factorial normal closure or old IRR heuristic
is imported. AMITSUR_ARITHMETIC_REUSE_AUDIT.md gives compact cochain-to-matrix
conversion. Expanded splitting coordinates can be enormous; retain compact
output. Current source review: audits/reviews/2026-11-07-global-isotropy-sources.md.

Falsifiers: an unpaid source hypothesis, superpolynomial degree/precision,
failure of descent for an arbitrary splitting, an exponential local class
search, a compact-to-expanded conversion, or a stronger classical general
algorithm removes the proposed contribution. Cheap exact checks precede any
quantum implementation. No quantum backend is proposed here.

## Reviewed exact ternary and quaternary descent

For q4=<a,b,c,d>, put D=abcd. If D is nonsquare, use L=K(t), t^2=D;
otherwise L=K with a paid square root t of D. Set u=-b/a, v=-c/a,
h=t/(bc), B=(u,v)_L, and

    phi(x)=x1+x2*i+x3*j+h*x4*i*j;  q4(x)=a*Nrd(phi(x)).

For any splitting rho:B->M2(L), I={X:rho(X)e1=0} is a minimal LEFT ideal.
W=phi^-1(I) is an isotropic plane. If D is nonsquare, coefficient
conjugation sigma_B and reversion tau fixing i,j and negating ij satisfy
phi(sigma x)=tau(sigma_B(phi(x))). Reversion is an ANTI-automorphism;
phi(sigma W) is consequently a minimal RIGHT ideal. In M2 every minimal
left/right pair intersects in precisely one dimension (maps from a fixed
one-dimensional quotient to a fixed image line). Thus W intersect sigma W
is a sigma-stable line, for EVERY splitting rho. Divide a nonzero vector
by one of its nonzero coordinates; the resulting vector is fixed by sigma
and belongs to K. No special ruling advice or Hilbert90 solver is needed.

Explicitly stack A and sigma(A), where A has columns
e1,rho(i)e1,rho(j)e1,h*rho(ij)e1. Rank is three. A nonzero 3-by-3 minor
selects three independent rows; their signed cofactors give the kernel
vector. Normalize, then propagate each L gate as a pair of K circuits and
retain the constant component. If D is square, any nonzero kernel vector
of A suffices. Conversely any isotropic q4 gives a norm-zero element of B,
so B is split. The equivalence therefore pays the source's split promise
once local quaternion splitting is decided.

For q3=<a,b,c>, use B=(-b/a,-c/a)_K and V=span{1,i,j}. I intersect V has
dimension at least one. It cannot have dimension two, since a nondegenerate
ternary form has no two-dimensional totally isotropic subspace. The
2-by-3 matrix of first columns has rank two and signed minors give a point.
No degenerate fourth coefficient is introduced. Dimension2 is the ordinary
square test for -b/a; dimension1 is anisotropic.

Detailed independent proof, including every-sign check and compact tests:
audits/reviews/2026-11-07-global-isotropy-descent.md. This gate is established
given a correct compact splitting; it does not alone establish the native
algorithm's total clock.

## Compact arithmetic and bounded-error verification

A polynomial-size field DAG can encode exponentially many expanded bits.
Convert its operations conceptually to rational scalar gates via the
multiplication table; inverse gates use determinant/adjugate circuits, not
expanded numbers. With polynomial scalar circuit size T and H input bits,
integer numerator/denominator nodes have bit length at most 2^T(H+1).
The product of the relevant nonzero integers has log at most
O(T*2^T*(H+1)). Thus only exponentially many rational primes can be bad,
and random primes of a sufficiently large POLYNOMIAL bit length avoid them
with any prescribed inverse-exponential failure probability. Certified
prime generation and its capped retry clock are charged.

Evaluate in the FULL finite K algebra; it need not be a field. A denominator
is inverted only when its multiplication determinant is nonzero modulo p.
Outside the bad-prime set all zero tests are correct. Use FRESH primes for adaptive tests and final verification. Reusing one
prime with a union bound is allowed only for a fixed nonadaptive expression
list, not expressions selected as a function of that prime. This is randomized
EqSLP-type testing, not expansion or PosSLP. Check the splitting relations,
q(v)=0 and a declared nonzero coordinate using this same paid interface.
The source error and modular verifier error receive separate budgets.

L/K component-pair arithmetic adds only constantly many gates per relative
operation. An absolute primitive element theta+c*t can be found among
polynomially many small integer c: each pair of distinct embeddings excludes
at most one c. Krylov ranks test degree, rational linear algebra gives
compatible basis conversion, and integer factoring pays maximal-order
construction. These front-end quadratic fields have degree <=2n. The imported Amitsur
routine also uses tensor-factor fields of separately charged POLYNOMIAL
degree; the <=2n bound is not asserted for all its internal fields. No
normal closure is built.

## Reviewed local value lemma via quadratic ideal decomposition

Given F=K_p and expanded a,b,c in K*, construct expanded s,t in K with
c0=a*s^2+b*t^2 nonzero and outside c F*^2. Set delta=-b/a.
This primitive uses polynomially many degree-two field constructions and
integer factorizations. It is quantum polynomial time after Shor; it is
NOT asserted to be unconditionally classical polynomial time. It replaces
the earlier local-root proposal in the immutable Claude prompt packet.

First, a paid local square test for x in K*: factor X^2-x over K. A global
root means local square. Otherwise form Lx=K(sqrt(x)), compute its maximal
order using integer factoring, and factor p O_Lx. The element x is a square
in K_p iff p splits into TWO primes with relative e=f=1. This is the
quadratic etale decomposition of K_p[X]/(X^2-x), valid also at dyadic and
fractional x. No local root is constructed. All fields have degree <=2n
and expanded polynomial-height defining/basis data; a polynomial number
of repetitions remains paid. Voight Lemma7.16/Theorem7.2 give the uniform
ideal/maximal-order interfaces, with finite-field factoring randomized.

If a/c is already locally nonsquare, s=1,t=0 works. Otherwise a and c have
the same local class and it suffices to produce a nonsquare norm value.
Test whether delta is a GLOBAL square, via ordinary number-field polynomial
factorization. If so its expanded root r has polynomial height, and
s=(pi_F+1)/2,t=(pi_F-1)/(2r) gives a*s^2+b*t^2=a*pi_F. A uniformizer is an
integral basis element of p outside p^2, found by ideal membership.

If delta is globally nonsquare, build L=K(sqrt(delta)) and factor p O_L.
There are exactly three possibilities:

- Split P1*P2: choose pi_P1 in P1 outside P1^2, then ideal CRT gives z
  congruent to pi_P1 modulo P1^2 and to1 modulo P2. Thus v_p(N_L/K z)=1.
- Ramified P^2: a uniformizer z at P has v_p(N_L/K z)=1.
- Inert P: E=L_P/F is unramified quadratic. At odd residue characteristic,
  a lifted nonsquare residue unit has nonsquare norm. At characteristic2,
  use the generating list consisting of pi_E and 1+b_j*pi_E^i for
  i=1,...,2e_E, where b_j lift an F2 basis of the residue field. It has
  1+2e_E*f_E=1+2[E:Q2] elements. Since U_i/U_(i+1) is additive residue
  field, odd-order residue units are squares, and U_(2e_E+1) is square by
  Hensel, this list generates E*/E*^2. Unramified unit norms are surjective
  (Voight Remark5.3); F has a nonsquare unit. Hence at least one listed
  generator has nonsquare norm; find it using the paid local square test.

In every case z is a polynomial-bit expanded GLOBAL L element. Ideal HNF
basis elements have coefficients bounded by the ideal norm, quotient residue
bases use finite-ring linear algebra, and CRT is HNF-reduced. Exponents
are at most2e_E<=4n. Convert z=s+t*sqrt(delta) by the explicitly compatible
relative/absolute basis maps. Then a*N_L/K(z)=a*s^2+b*t^2 is outside the
forbidden class, with polynomial expanded coordinates. No dyadic class
enumeration, local square-root approximation, global principal generator,
unit basis or unbounded prime search is used.

For arbitrary fractional targets s0,t0 and nonzero c0=a*s0^2+b*t0^2,
it suffices to approximate both with valuation error >=M, where M>=0 and

    M > 2e+v(c0)-v(a)-min(0,v(s0)),
    M > 2e+v(c0)-v(b)-min(0,v(t0)).

For a zero target use min(0,v(0))=0. Expansion of the square difference gives
v(c-c0)>2e+v(c0), so c/c0 is a local square. All these valuations are
polynomially bounded for expanded polynomial-bit representatives. Negative
valuations must not be silently normalized away.

## Finite/real weak approximation: audited polynomial bit construction

Given expanded local targets y_p, precisions M_p with charged sum
M_p*log Np, rational targets at all real embeddings and error 2^-P, choose
a positive integer D clearing target denominators. Let
I=product p^e_p, e_p=M_p+n*v_r(D) with r the underlying rational prime.
This overestimates M_p+v_p(D), so avoids an uncharged valuation interface.
Find u0 in O_K matching D*y_p by ideal CRT, and reduce u0 modulo I.
HNF entries are bounded by Norm(I); reduce intermediate ideal products too.
All ideal bases and u0 therefore have polynomial bits. Put R equal to the product of
the underlying rational primes (R=1 for an empty set). Choose M=1+kR of
polynomial bit size large enough that the mesh of I/(DM) is <2^-P.

In the full real Minkowski embedding matrix of an ideal basis b_i, solve
for real c_i whose real-embedding targets are D*a_sigma-sigma(u0), setting
complex real/imaginary targets to zero. Approximate c_i to <1/(4M), round
M*c_i to integers k_i, and set x=u0/D+sum k_i*b_i/(DM). Finite conditions
persist because M is a local unit. Real error is bounded by the sum of
embedding magnitudes of b_i divided by DM. These magnitudes are exp(poly),
and the determinant is 2^-r2*sqrt(|disc K|)*Norm(I); inverse conditioning
therefore costs polynomial precision. In detail, if basis entries in the
power basis have <=B bits, the Cauchy root bound gives W=2^O(nB) bounding
all their embeddings. An HNF ideal basis has embedding magnitude <=n*Norm(I)*W.
A computable M>=2^(P+2)*n^2*Norm(I)*W/D suffices. Set Lambda>=||A||_2
and J=2^r2*Lambda^(n-1)>=||A^-1||_2, V>=||target||+1, all exp(poly).
Approximate target with norm error <=1/(64 M J), and A with operator error
<=1/(64 M J^2 V). Exact rational solving of the approximations then gives
coefficient error <1/(4M), by the inverse perturbation identity. This
charges BOTH target and matrix evaluation errors. Certified real/complex
root isolation/refinement costs polynomial bits; rational solving is exact.
Final rounding contributes <=3/(4M) per coefficient. All output coordinates
have polynomial bits. The integral basis is explicitly supplied in the
defining power basis, with compatible table; it is not an abstract table
with an unlabelled embedding.

Claude's completed weakapprox audit validates this construction and supplies
the HNF, root-bound and conditioning details; parent checked them and made
the target-perturbation budget explicit. The approximation operation itself
is deterministic given promised field/prime data. Field construction and
factoring in its caller retain their own randomized/quantum budgets.

## Single restriction and five-to-four reduction

Expanded rational linear algebra diagonalizes Q with polynomial bit size.
For d>=5, local finite u-invariant4 and Hasse--Minkowski imply isotropy iff
the form is indefinite at every real embedding. Root isolation/signs decide
this in polynomial bit work. If K has no real embeddings, any five diagonal
coordinates suffice. Otherwise, at each real place select five DISTINCT
coordinate units including both signs. They give a nondegenerate indefinite
local five-plane. Simultaneously approximate every entry of these d-by-5
matrices by K elements. Nonzero algebraic eigenvalue separation is
exp(-poly input), so polynomial precision preserves both nondegeneracy and
indefiniteness. Q'=M^t Q M has expanded polynomial-size coefficients and is
globally isotropic. This single restriction avoids an unproved recursively
preserved height bound. It does not show any published recursive method slow.

For q5=<a1,...,a5> indefinite everywhere real, write q1=<a1,a2,a3>.
At finite places where q1 is anisotropic it represents every nonzero
squareclass except -det(q1). Consequently q1+<c> is isotropic when
c is outside det(q1)*K_p*^2; the minus sign must not be lost. Choose a
finite set S containing primes above2 and all numerator/denominator prime
supports of a1,a2,a3. Outside S an odd-residue unimodular ternary form is
isotropic by reduction and Hensel. At EVERY p in S use the binary-value
lemma with a=a4,b=a5, forbidden c=det(q1). This is harmless even where q1
is already isotropic. Since S contains a prime over2, preserving one
nonzero local value also guarantees the eventual global c is nonzero.

At a real place where q1 is definite, at least one of a4,a5 has opposite
sign. Choose real targets (s,t)=(1,0) if a4 has the needed sign, or
(0,1) otherwise. Algebraic separation of the nonzero selected coefficient
gives polynomial required precision for preserving this sign. At places where q1 is indefinite no real sign constraint is
needed. Finite/real weak approximation gives expanded polynomial-bit s,t
with c=a4*s^2+a5*t^2. Then q4=<a1,a2,a3,c> is locally isotropic everywhere,
hence globally isotropic. The reviewed q4 route yields compact w; lift it
to (w1,w2,w3,s*w4,t*w4). No prime-enlargement loop or enumeration occurs.

The independent composition review checks these local, approximation and
source interfaces together; no remaining resource blocker was found for
this exact native compact contract. Classical prior-art scope remains
substantial and novelty UNKNOWN. A compact point must not be expanded or fed as an uncharged expanded
input to another source call.

## Reviewed native algorithm and total resource accounting

Let B_in denote the total expanded input bit length, including n,d, the
integral-to-power-basis conversion and multiplication table. Diagonalize
once, retaining the expanded basis change. The algorithm has these branches:

1. Dimension1 returns NO. Dimension2 globally factors X^2+b/a over K:
   a root gives a point, and absence gives NO.
2. In dimensions3/4 construct the displayed quaternion over K or the
   explicitly compatible quadratic extension. Decide if it splits by real
   Hilbert symbols and finite symbols at primes over2 or numerator/denominator
   supports of its two parameters. Outside this support odd unit Hilbert
   symbols are1; complex places cause no obstruction. Factor the polynomial-
   bit rational norms/discriminants and the resulting ideals with paid Shor
   calls. Actual Voight Theorem6.1 pays the local Hilbert arithmetic uniformly
   in field degree. A nonsplit result returns NO by the proved equivalence.
3. In dimension>=5 a definite real embedding returns NO. Otherwise perform
   the single five-plane restriction if needed, then the five-to-four
   construction. Both use expanded polynomial-bit data and give a promised
   isotropic nondegenerate q4. Its associated quaternion is therefore split.
4. Invoke the EXISTING under-GRH Amitsur quantum splitting algorithm on the
   expanded structure constants of this one promised split quaternion.
   Preserve its compact S-unit/cochain output and convert it to a compact
   matrix map with the established trace formulas. Extract the compact point
   by the reviewed descent, lift through the binary pair/five-plane/initial
   basis changes, and perform fresh-prime compact verification before emission.

Only ONE compact splitting is needed on a positive branch. All geometric,
local, real-sign, prime-ideal, discriminant and source inputs remain expanded
polynomial-bit before it. After it, use only field DAG operations and
bounded-error equality tests: no sign test, ideal factorization, square
root, compact-to-expanded conversion or second expanded-input source call
is applied to a potentially huge compact answer. The output DAG includes
its division-free numerator/denominator form if desired; denominators are
certified nonzero with the same bounded-error tests.

Every non-source operation uses poly(n,d,B_in) field/ideal/scalar operations
on polynomial-bit expanded data, or polynomial-size DAGs. The local chooser
uses O(n) tests per bad prime; there are polynomially many such primes.
The approximation exponents are polynomial as NUMBERS, so ideal powers
have polynomial log norm. Auxiliary quadratic degrees are <=2n; the source's
bounded tensor powers have polynomial absolute degree and polynomial input
size. There is no coherent source oracle or QRAM: the input is classical,
and quantum resources are the paid factoring and published complete-S-unit/
splitting routines. Total gates, qubits, classical bit work and output size
are polynomial in B_in and log(1/eta), with a loose inherited exponent; no
practical resource estimate or implementation is asserted.

For clocks, select explicit polynomial constant-success caps for each
randomized source/arithmetic primitive and repeat independently O(log(J/eta))
times, where J is a polynomial upper bound on all calls and equality tests.
For an expected-polynomial Las Vegas routine, cap one attempt at a constant
multiple of its polynomial expectation, then repeat; do NOT use a single
1/eta-expanded cap. Validate classical factors/ideal decompositions and
returned splitting relations where applicable. Use fresh modular primes
for adaptive and final tests, with individual failure <=eta/(cJ). Source
failure, bad modular primes and exhausted caps together have probability
<=eta after allocating a fixed fraction to each. Exhaustion returns ABORT,
never a false claim of anisotropy; ABORT counts as failure within that budget.
A positive point has an independently charged bounded-error classical verifier.

This is the reviewed written quantum polynomial-BIT COMPACT endpoint under explicit
GRH, combining known arithmetic algorithms with the written reductions. The
potential asymptotic advantage lies in the inherited general-field S-unit/
splitting step; no unconditional classical lower bound, separation, novelty
or new quantum primitive is established. Rational/special-field classical
baselines remain fully applicable on their actual inputs.

## External agents and evidence ledger

Claude local-norm request: terminal empty refusal, estimated USD0.018276;
no report, no scientific evidence, no retry. Bundle
audits/claude_runs/2026-11-07-global-isotropy-local-norm. A DISTINCT focused
finite/real weak-approximation proof audit completed in the corresponding
global-isotropy-weak-approx bundle. Accepted with the explicit HNF/input
basis and two-error conditioning details above; no whole-solver conclusion
is inferred from that report.
All four dated global-isotropy reviews are complete and were read by the
parent: source, descent, local and composition. The last two clarify the
paid integer-factoring interface, fresh adaptive primes, and the source's
polynomial internal field degrees. The useful Claude estimate is USD0.688840;
with the empty refused call this pass totals USD0.707116. Across all43
bundles with reported estimates, USD34.726816 and21 completed reports is a
usage ledger, NOT an invoice or remaining-balance estimate. No pending call
or retry remains. Full solver/quantum execution, novelty, separation,
expanded output, Witt decomposition and removal of GRH remain false gates.


## Focused exact control and classical comparison

The single CAS control is audits/controls/global_compact_isotropy/control.py
and its retained JSON. It reproduces the fractional-input failure4/3;
PARI qfsolve finds points for <1,-2,-3,4> and <1,1,1,1,-7>, and gives the
local obstruction3 for <1,1,-3>. This runs a genuine classical comparator,
not a quantum simulation or a hardness experiment.

Over Q(sqrt6), an exact zero-divisor TEST fixture generates a splitting of
(2,3), followed by an arbitrary matrix gauge change. Stacking the actual
plane and its conjugate gives rank3 and the descended point
(1,1/5,-13/5,-11/5) for <1,-2,-3,4>. Omitting the discriminant sign leaves
rank2 in the independent <1,-1,1,-2> control. The fixture's known zero
is not advice to the proposed native algorithm.

Dyadic unit generators in Q_2(sqrt5) give norms9,-1,25,-11; the value
minus one is a nonsquare in Q_2.
The explicit pair (s,t)=(2,1) gives 2^2-5*1^2=-1. Over the ramified base
Q_2(sqrt2), eight principal-unit generators in its unramified quadratic
extension again include nonsquare norm -1. Global quadratic decomposition
checks that squareclass without a supplied local square-root operation.
This is a finite algebra/branch falsifier only, not all-field evidence.

Actual Kutas1606.01053v2 Section2.2/Fact1/Fact2 and the proved quadratic-base
algorithm retain the strongest elementary comparator scopes: rational
forms admit factoring-oracle algorithms, rational indefinite dimension>=5
admits a GRH randomized polynomial algorithm without factoring, and
quadratic-base quaternion splitting is randomized polynomial with integer
factoring. Those results already cover substantial subfamilies; no claim
that every known classical method is exponential, or that growing-degree
compact isotropy is hard, is made. General norm/S-unit/index-calculus and
LLL methods remain baselines. The primary GRH Amitsur splitting is reused,
not presented as newly discovered.


## Research decision at this checkpoint

The expanded-input compact-point endpoint is now accounted for as a written
under-GRH composition. No new local backend, full solver, extension to compact
inputs/Witt decomposition, or output-expansion project is queued. Those would
need independent external motivation and a specific new falsifier. Start the
next pass from STATE/TRAPS and compare independent native mechanisms, rather
than treating an adjacent arithmetic interface as the default priority.
