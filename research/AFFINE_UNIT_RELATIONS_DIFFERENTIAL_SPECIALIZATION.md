# Growing tuples of units: differential and specialization algorithm

2026-11-06. Written constructive CLASSICAL composition; independent core,
source/cost and final integrated-text review complete. Two explicit size
lemmas below repair the initial abbreviated proof. No novelty, quantum
advantage or execution of the full algorithm is claimed.

## Native question and prior work

Fix the number m of polynomial variables. Input is a proper PRIME ideal
I=(f_1,...,f_r) in Q[X_1,...,X_m], explicitly given by generators, and an
UNBOUNDED tuple u_1,...,u_k of units of A=Q[X]/I. Polynomial representatives
of the units and their inverses are part of the charged input. The ideal is
promised prime; no prime decomposition, normalization, divisor map or target
lattice is supplied. Coefficients are binary rationals; degrees are numerical,
with dense encodings or polynomially bounded numerical degrees. Output a
Z-basis of Rel_A(u)={e in Z^k: product u_i^e_i=1}. Target: deterministic
polynomial BIT time for fixed m, including growing k. No unrestricted sparse
binary-exponent representation, positive-characteristic, integer-torsion,
nonreduced or arbitrary reducible claim.

Selection followed STATE/TRAPS, corpus been-tried and baselines, then actual
primary sources. The catalog returned no exact baseline (an unrelated LLL
hit was not applied). Independent alternatives involving explicit diagonal
forms, supersingular torsion alignment and Galois/Frobenius sampling gave
no new paid operation; no source or quantum receiver was built for them.

Miasnikov--Ushakov, arXiv2610.27250v1, actual Theorems1.1--1.2 and Section3,
give fixed-m,FIXED-k polynomial algorithms. Their algebraicity lattice basis
has numerical bound k!*D^((m+1)k), and enumeration uses fixed k. The rational
branch is already CLASSICAL; quantum work addresses finite/torsion rings.
Kreuzer--Walsh2307.09394, actual Proposition5.1/Algorithm5.3, localize using
a maximal independent variable set and repair components lost to saturation.
Lenstra--Silverberg1509.08843 Theorem1.11 is the intended classical finite-
dimensional Q-algebra relation primitive. Its actual Introduction fixes the
rational structure-constant encoding; Theorem1.11(i), Proposition8.2 and
Algorithm8.3 explicitly accept an unrestricted finite system S and even
nonreduced algebras. The parent read those passages, including the proof.

The proposed gain is removing exponential dependence on k in this rational
DOMAIN branch, not inventing quantum arithmetic. A general classical match
helps locate which native affine-ring cases still need a quantum mechanism.
This does not extend the paper's metabelian theorem to a growing number of
group generators: that also increases the number of polynomial variables.
Kreuzer--Walsh Algorithm2.6 already solves pure rational-function tuples by
factor valuations; Algorithm2.10 gives a general finitely generated-field
method using normalization and valuations, then forming products of basis
powers. Those are prior algorithms, not hardness evidence. This composition
replaces those operations with a paid differential/specialization route;
no claim that the result or method is new follows from this bounded search.

## 1. Algebraicity from logarithmic differentials

Let Omega=Omega_(A/Q). Define w_i=u_i^(-1)du_i. In characteristic zero,

 Alg_Q(u) = {e in Z^k: sum_i e_i w_i=0 in Omega}.                 (1)

Proof: d(product u_i^e_i)=product u_i^e_i sum e_i w_i. If this differential
vanishes, pass to F=Frac(A). The kernel of d:F->Omega_(F/Q) is the relative
algebraic closure of Q in F: a transcendental element can be included in a
transcendence basis, and its nonzero derivative extends through the finite
separable extension. Conversely, if v in A is algebraic over Q, its minimal
polynomial is separable. Bezout for P and P' makes P'(v) invertible in A,
so P'(v)dv=0 implies dv=0 already in Omega. Apply this to v=product u_i^e_i.
No product with a large exponent is constructed by the algorithm.

Compute (1) by fixed-variable polynomial-module linear algebra. Check every
supplied inverse modulo I first. Omega is Q[X]^m/N, where N is generated
by all f_j times coordinate vectors and the gradient rows df_j. The w_i
have representatives of degree<=2D-1 from the supplied inverses.

Here is an explicit degree bound independent of k. Introduce m auxiliary
variables Y and map a vector a(X) to a(X) dot Y. Let J be the ideal generated
by n(X) dot Y for the displayed module generators n. Then w belongs to N
if and only if w dot Y belongs to J: in an ideal representation take its
homogeneous Y-degree1 part, which uses only Y-degree0 multipliers. Hermann's
ideal bound in the FIXED 2m variables gives multipliers of degree at most
(2E)^(2^(2m)), with E bounding target/generator degrees (one may take E=2D+2).
This is polynomial in D for fixed m and does not depend on the number of
constant coefficients or module generators.

First compute N intersect (Q[X]^m)_{<=2D-1} by bounded-degree coefficient
matching, as in Lemma2.5 of2610.27250v1, using the ideal encoding above.
Map the k columns w_i into the resulting finite-dimensional quotient and
compute its rational kernel. Integer linear algebra computes its intersection
with Z^k, giving the saturated lattice L. System dimensions and coefficient
bit lengths are polynomial; growing k only adds columns. The resulting basis
may have large numerical coordinates but polynomial BIT length. No box of
exponents is enumerated and no u^e is expanded.

## 2. Build a nonzero finite specialization without hidden point advice

Find a maximal independent subset T of the original variables modulo I;
there are at most2^m subsets to test by elimination. Write Z=X\T. Since I
is prime, F0=Q(T)[Z]/I is a nonzero zero-dimensional FIELD and A->F0 is
injective. Kreuzer--Walsh Proposition5.1 gives the localization rule: an
elimination Groebner basis G remains a basis over Q(T), and its contraction
is I:h^infinity. Here h in Q[T] is nonzero, so primality and independence
force I:h^infinity=I.

Pay both degree and coefficient growth as follows. Let Gamma=D^{O_m(1)}
be a Dube bound for the original elimination Groebner basis. To construct
one with controlled heights, compute I intersect Q[X]_{<=Gamma} via
Hermann's bound and rational linear algebra, and row-reduce in monomial
order. This row basis is a Groebner basis: the bounded-degree reduced basis
lies in its span, and every leading monomial of that span is a pivot.
It generates I because it also spans the input generators. All matrix sizes
and coefficient bit lengths are polynomial in the charged input.

After passing to Q(T)[Z], zero-dimensionality implies the leading ideal
contains a pure power of every Z-variable; exponents of standard monomials
are <Gamma. Thus delta<=Gamma^m and their total degrees are <=m*Gamma.
Find normal-form coordinates of the products of two standard monomials and
of each original variable by solving bounded-degree membership systems over
Q(T), rather than charging an unspecified division trace. Hermann over the
at-most-m Z variables bounds multiplier degree by D^{O_m(1)}, independently
of unknown normal-form coefficients. Entries in the resulting systems are
polynomials in T, with polynomial degree and coefficient bit height.

Clear rational coefficient denominators, then use a rank-revealing fraction-
free solve or Cramer minors. This gives polynomial numerator/denominator
degree and height: for an N-by-N minor of entries of
T-degree<=b and bit height<=H, degree is <=N*b and coefficient bit height
is O(N*(H+logN+|T|*log(N*b+1))). Here N,b,H are polynomially bounded and
|T|<=m is fixed. Coordinates are unique, although membership multipliers
need not be. This produces delta^3 rational-function structure constants
and the m variable-coordinate vectors, all explicitly of polynomial size.

Let g(T) be the PRODUCT of their nonzero denominators. It is an explicitly
expanded nonzero polynomial of polynomial degree/height since |T| is fixed.
The Q[T,1/g]-span O of the standard monomials is closed under multiplication
and contains every original variable. Conversely those monomials lie in A;
therefore O=A[1/g]. It is FREE of rank delta>=1. Find integer a with g(a)!=0
by a grid of size deg(g)+1 in each of the fixed number of coordinates; the
search and bit lengths are polynomial. Then

                         B=O/(T-a)O

is a NONZERO delta-dimensional Q-algebra with explicit specialized structure
constants, and A->B is a unital Q-map rho. No rational point on Spec(A),
constant-field basis, factorization or primitive element was supplied.
B need not be a field or reduced; actual Lenstra--Silverberg allows this.
For dimA=0 use T empty and B=A. Finally evaluate each original unit and
inverse polynomial in the specialized variable coordinates. Polynomial
numerical degrees ensure polynomial bit cost. Unit/inverse identities hold
because rho is a ring map. In particular g need not depend on growing k.

Crucial faithfulness: C={v in A:v is algebraic over Q} is a FIELD. A is a
domain, and the inverse of a nonzero algebraic element is a polynomial in
that element over Q. Thus rho restricted to C is injective, since it is a
unital map from a field to a nonzero ring. This does not claim rho injective
on all of A, or that it preserves arbitrary unit relations by itself.

## 3. Intersect, without evaluating products of basis powers

Apply the classical finite-Q-algebra relation algorithm to the ORIGINAL
images rho(u_1),...,rho(u_k), not to products corresponding to a basis of L.
Let M=Rel_B(rho(u)). Then

                         Rel_A(u)=L intersect M.               (2)

One inclusion is immediate. If e belongs to L intersect M, v=u^e is in C
and rho(v)=1. Injectivity on C forces v=1. Compute the intersection by Smith/
Hermite linear algebra, with binary basis coordinates. This avoids the two
potential exponential steps: enumeration in k and expansion of algebraic
products whose exponents have only polynomial BIT length.

The actual Lenstra--Silverberg input theorem and the explicit degree/bit
lemmas above close those resource obligations. Its finite generating set is
converted to a Z-basis by HNF; the final relation lattice need NOT be
saturated (torsion relations must be preserved). Thus this WRITTEN
composition runs in deterministic classical polynomial time in the total
charged input, including k, for each fixed m. It solves a promise problem;
it does not certify primality. No arbitrary-m or compressed-exponent claim.
It computes relations among SUPPLIED units, not a complete unit group,
class group or principal ideal generator. The earlier quantum factorial
compositions are not dequantized. The full algorithm has not been run.

Immediate integer-domain corollary: the same bound holds for a promised
PRIME characteristic-zero affine Z-algebra in fixed variables, with units/
inverses in its charged input. It injects into its rationalization (no
nonzero integer can annihilate a nonzero element of a characteristic-zero
domain); the rationalized ideal is prime and its unit relation lattice is
unchanged. This does not cover finite-characteristic domains or arbitrary
integer torsion/nonreduced rings, and does not dequantize the paper's full
metabelian/Z-algebra result.

## 4. Cheapest tests and scope falsifiers

Use A=Q[x,y]/(xy-1), units (2x,3x^2,12x^4,x), and specialization x=y=1.
The logarithmic row is(1,2,4,1); the finite rational images are(2,3,12,1).
Exact prime valuation rows in B are(1,0,2,0) and(0,1,1,0). Their intersection
should be Z*(-2,-1,1,0). Differential-only e=(1,0,0,-1) incorrectly treats
constant2 as1; specialization-only e=(0,0,0,1) incorrectly treats x as1.
Both filters are therefore essential. The prescribed Sage control checked the inverse identities, free-differential
row, integer kernels and exact signed products. It returns exactly that
lattice and exposes both false positives. The rational finite branch uses
exact2/3 valuations only; no general Lenstra--Silverberg implementation ran.

The prime/domain promise is material: in Q[x,x^-1] times Q, the unit(1,2)
has zero logarithmic differential and becomes1 under projection to the first
component, yet it is not1. A generic localization/specialization may lose
that component. No extension to general reduced algebras is asserted.
Nonreduced inputs also require a separate algebraicity argument; e.g.
1+epsilon*x in Q[x,epsilon]/epsilon^2 is algebraic although its universal
differential need not vanish. Do not silently apply (1) there.

No quantum circuit, parameter sweep or infrastructure is queued. Passing a
finite control cannot establish this theorem; the proof and sourced bit
bounds carry the all-input claim. Final actual-text review included the explicit size lemmas and corrected
source contracts above and ACCEPTED the stated composition.

## Review dispositions

Codex independent_direction_selection accepts the core and resource proof
for the stated domain/fixed-m contract. It supplied the fixed-2m ideal
encoding and requested explicit determinant bounds; both are integrated.
Claude Opus/high independently accepted the mathematical composition
conditionally on three concrete source/bit obligations. The actual
Lenstra--Silverberg encoding, arbitrary tuple length and nonreduced scope
were checked; the two explicit size lemmas above settle the remaining
obligations. Its suggested etale-only specialization is unnecessary because
the actual theorem permits nonreduced B; no discriminant restriction was
added. Building g from structure/variables only was adopted as a simpler
valid construction. The prime promise is not claimed to be verified.

Claude bundle: audits/claude_runs/2026-11-06-affine-unit-differential-opus/;
completed usage estimate$0.393336, not invoice/account balance. The initial
invocation rejected a PDF end-of-proof control byte BEFORE any API call.
The input packet explicitly renders that byte as[QED]; no unknown-cost retry.
Sources and finite controls are separate from full algorithm execution.


The second review-directed control, A=Q[a,x,y]/(a^2-2,xy-1), keeps the
constant field Q(sqrt2) under x=y=1; it does not substitute a rational value
for a. Units(x,a,1+a,2,x^2*a) give relation basis
(-2,-1,0,0,1),(0,-2,0,1,0). Exact inverses, prime-over2 valuations and
relation products passed. Both controls live in
`audits/controls/affine_unit_differential/` as gm_units and quadratic_constants
.py/.json pairs. These use explicit elementary finite relations, not an
implementation of general Lenstra--Silverberg or the full affine algorithm.

Final actual-text Codex review ACCEPTED the completed degree/height proofs,
nonreduced-specialization allowance, nonsaturated final lattice, integer-
domain corollary and finite-control scope. Source hashes and exact excerpts:
`audits/claude_inputs/2026-11-06-affine-unit-relations/final_source_excerpts.txt`
and `source_metadata.json`; dispositions:
`audits/reviews/2026-11-06-affine-unit-differential.md`.
