# A Constructive Route Through The Existing Infinite Tower

Status: independent mathematical review ACCEPTED the construction with the
explicit invariant and finite-module normalization argument in ARITHMETIC.md
and REVIEW_RESOLUTION.md. This is a composition of known algorithms and scoped
deductions, not a novelty claim. NO higher tower level, Jacobian basis, prime divisor
or new parity matrix has been constructed by this bundle. Do not treat this as
an implemented generator or quantum speedup. The explicit backend contracts
below must be implemented and checked before claiming a working generator.

## Scientific Question

Can the existing existence-only S-split tower be turned into an output-polynomial
classical source, at fixed q=100003, without computing arbitrary class-group
discrete logarithms or solving the native full-support problem while generating
its inputs? This is more decisive than improving another exponential divisor join.

Use the independently reviewed genus-six seed and its23 marked split points
from ../prime-ag-tower-source-2026-10-26/TOWER_SOURCE.md. Its maximal unramified
S-split pro-2 extension is infinite. At level e=2^j keep the actual curve X,
all23e marked lifts, and one rational O above infinity. Then g=5e+1. Every
step below is over ORIGINAL F_q; internal extension arithmetic must descend.

## 1. Find An Unramified Split Quadratic Cover

Let K=F_q(X). The space of even-divisor Kummer classes fits the exact sequence

    0 -> F_q^*/F_q^{*2} -> U -> J(F_q)[2] -> 0,
    U={f in K^*: div(f) is even}/K^{*2}.

A rational O gives rational divisor representatives. For a certified basis
T_i of J(F_q)[2], choose bounded degree-zero representatives D_i and compute
f_i with div(f_i)=2D_i. This is a PRINCIPAL DIVISOR problem with the complete
divisor supplied, solved by a one-dimensional Riemann-Roch space L(-2D_i).
It is not a principal ideal problem with unknown infinite valuations, and not
an arbitrary Jacobian discrete logarithm. Add f_0=nu, a nonsquare constant.
These classes form a basis of U by the exact sequence.

For each marked rational P and f_i, compute v_P(f_i)=2a and the nonzero local
unit residue of f_i*t_P^(-2a). Record its quadratic-character bit. These bits
form a matrix M over F_2. Raw evaluation f_i(P) is INVALID when there is a
zero or pole. Changing the uniformizer changes the unit by a square, so the
bit is intrinsic. For a column combination b, M b=0 means that EVERY marked
place splits in K(sqrt(product_i f_i^b_i)).

Choose any nonzero b in ker M. The U-basis guarantees the radicand is not a
square. Nonempty marked rational S excludes a pure constant extension: the
nonsquare constant column consists entirely of ones. Thus the quadratic cover
is connected, geometric, unramified and S-split. Normalize it, lift the marked
points (two rational points each), and retain one lift of O.

The genus becomes2g-1 and the marked set doubles. There is NO claim that an
arbitrary curve with many marked points has nonzero ker M. Nontermination is
excluded here by the specific infinite-tower hypothesis, not by row counting.

## 2. Why An Arbitrary Chosen Step Can Continue

Let K_infty/K_0 be the maximal unramified S_0-split pro-2 extension certified
by the seed theorem. Every chosen quadratic step lies in it. Indeed any
finite sequence of unramified split quadratic extensions has a normal closure
over K_0 of2-power degree: conjugate quadratic extensions have elementary
abelian compositum over the preceding normal closure. Unramifiedness and
complete splitting persist under conjugation and compositum.

For any finite level K_j, Gal(K_infty/K_j) is an infinite open pro-2 subgroup.
A nontrivial pro-2 group has a continuous quotient of order2 (take a nontrivial
finite2-group quotient and then a maximal subgroup). Therefore K_j has a
further unramified split quadratic extension. Equivalently ker M is nonzero.
No renewed Golod-Shafarevich inequality is needed at each level. A decreasing
chain need not be cofinal in K_infty; it does give EVERY degree e=2^j and the
required genus/point counts. Do not claim it contains any preselected cover
unless that cover was included at the start.

## 3. Charged Arithmetic And Representation Costs

The independent review supplies the needed construction in its Sections4-6;
ARITHMETIC.md records the required invariant. The following list is not a
license to replace those constructions by unexplained oracle calls.

The following are charged subroutines, not free oracles:

1. Normalize explicit separable function fields and compute Riemann-Roch
   spaces for explicitly given divisors with polynomial degree/height bounds.
   Classical polynomial integral-basis and RR algorithms are discussed in
   [Eisentraeger-Hallgren](https://msp.org/obs/2013/1-1/obs-v1-n1-p17-p.pdf).
   Their quantum CLASS-GROUP algorithms must not be silently substituted.
2. Re-encode each resulting curve in a bounded-degree original-field model.
   The reviewed consecutive-pole construction gives a plane equation of
   degree2g+2 from L((2g+1)O) and L((2g+2)O). Choose the separating coordinate
   among those two pole orders. Compute its unique relation by function-field
   arithmetic. This reset prevents repeated tower presentations accumulating
   unchecked coefficient-height growth. Track images of all marked points.
3. Compute exact Jacobian order on this plane model by Lauder-Wan Corollary3,
   polynomial in plane degree and p. Here p=100003 is FIXED; no uniform
   polynomial-in-log(p) claim is made. See the independently reviewed
   ../one-point-plane-adapter-2026-10-26/REVIEW_RESOLUTION.md.
4. Generate and certify the full2-primary subgroup, extract J(F_q)[2], using
   the reviewed relation-lattice, small-bias prime-sample and perfect-pairing
   construction in ../prime-sampler-halving-2026-10-26/REVIEW_RESOLUTION.md.
   Exact order provides the stopping certificate. No odd-primary discrete
   logarithm is required. Construct its bounded graded algebra from RR.
5. Compute actual rational functions f_i and local units, multiply at most2g+1
   radicands, normalize the quadratic extension, and verify splitting. Bounded
   representatives D_i have degree O(g), so the product divisor has degree
   O(g^2), not exponential degree. The normalized-coordinate invariant and
   finite-module argument provide the needed polynomial height bounds.

With these reviewed polynomial contracts, each step has expected cost
poly(g) at fixed p. There are log2(e) steps, with geometric genus growth, so
the total is polynomial in the FINAL genus/output size. Encoding e in binary
does not give a polynomial-in-log(e) algorithm: the output matrix itself has
Theta(e^2) field entries. No practical-runtime claim is implied by fixed p.

## 4. Choose G Without A Uniform Picard Sampler Or Moving Lemma

Use the separate PRIME_CLASS.md argument: draw a uniformly random CLOSED
prime divisor G of degree d=2g+1 with Bruin Algorithm3.2, then compute L(G)
and evaluate at the22e finite marked points. Since d>1, G is automatically
disjoint from those rational points. No full-support word is used to move G.
Reject G unless the actual Schur cube of B has rank m. The class need not be
uniform: a direct maximum-class-mass bound makes rejection negligibly rare.

This produces the SAME explicit-input relation Bz=s, with a good square bound
and no same-code cubic annihilator. It does NOT remove the auxiliary-code norm
attack, systematic sampler, special-tower attacks or unknown better attacks.
It makes no classical-hardness assertion. The near-canonical divisor family
remains classically solved, and the tower's utility as a problem family remains
a separate reduction/novelty question.

## Falsifiers And Implementation Handoff

Reject the polynomial construction claim if: rational torsion representatives
or principal functions require uncharged work; local units cannot be obtained
in the charged model; the kernel search accidentally includes square radicands;
normalization costs or representation heights grow superpolynomially; the
new extension leaves the certified pro-2 tower; or the prime sampler loses
its exact output law through omitted acceptance correction.

Gemini should implement the native field/RR contract from this resolved audit, not
build another abstract registry. Preserve complete divisors, local uniformizers,
original-field coefficients, marked places and group-order certificates.
First material experiment: generate one cover beyond the previously explicit
elementary Kummer presentation, and a prime-degree G with verified dimensions
(k,m,w) and cube rank m. No parameter-only helper counts as that experiment.
