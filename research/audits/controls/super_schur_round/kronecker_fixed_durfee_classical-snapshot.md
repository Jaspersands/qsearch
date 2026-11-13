# Fixed-Durfee native Kronecker computation: proposed classical match

Native input: three explicit partitions lambda, mu, nu of numerical n (unary n is charged), with Durfee(lambda)<=d and Durfee(mu)<=e for fixed positive constants d,e. No restriction on nu. Output exact integer g(lambda,mu,nu). No character table, multiplicity, tableau enumeration or oracle advice is supplied. No quantum implementation is proposed.

External motivation: Panova2502.20253v2 section7.5 explicitly leaves polynomial-time exact fixed-Durfee computation open, including one-hook cases. Existing Larocca-Havlicek2407.17649v5 quantum projection estimates exact g with public partitions in O(n^4 R^2) gates, R=f_lambda*f_mu/f_nu, with dimension/precision and finite gate details owed by that source; its formerly conjectured min-dimension-polynomial advantage was classically matched by Panova Theorem1.1. The full ratio promise is not classically closed. This pass tests a concrete additional classical competitor, not a quantum novelty claim.

Proposed operation: use even variables x_1..x_d,y? CONVENTION below is authoritative: X=(x_1..x_d | y_1..y_d), Z=(u_1..u_e | v_1..v_e). p_r(X)=sum x_i^r+(-1)^(r-1)sum y_i^r. The tensor alphabet has even entries x_i*u_j and y_i*v_j, odd entries x_i*v_j and y_i*u_j. Hence p_r(XtensorZ)=p_r(X)*p_r(Z). The universal coproduct identity is
 hs_nu(XtensorZ)=sum_(a,b partitions n) g(a,b,nu)*hs_a(X)*hs_b(Z).
Outside(d,d) and(e,e) hooks the corresponding hook Schur polynomial is identically zero. The surviving hs_a form a linearly independent basis, so coefficients in the product basis should be exactly the desired Kronecker coefficients, with no folded contributions.

Computation: enumerate hook partitions by their first d rows and residual first d column heights (similarly e), at most(n+1)^(2d) and(n+1)^(2e) choices, never all p(n) partitions. Compute hs by Jacobi-Trudi with h_r(X)=sum_j h_(r-j)(x)*e_j(y); generating function prod(1+y_j*t)/prod(1-x_i*t). Compute determinant by polynomial-time exact arithmetic, not permutation enumeration. All polynomials have only 2d+2e variables, degree at most2n; a dense coefficient vector therefore has polynomial size for fixed d,e. Solve exact rectangular coefficient system, or use triangular leading monomials, to extract g. Need rigorous polynomial BIT bounds for intermediates, determinant, basis construction, coefficient solve, and arbitrary nu with length up to n. No unit-cost large integer or free rational-function determinant assumption.

Potential independent proof of basis injection: a hook partition a has lexicographically highest monomial x_1^(a_1)..x_d^(a_d)*prod_j y_j^(max(a'_j-d,0)), coefficient1, from greedy semistandard supertableau. The exponent vector determines a. Check whether this lex-leading statement really holds and triangular extraction is valid; not an axiom.

Corpus been-tried for precise super-Schur/fixed-Durfee mechanism found only unrelated commutant/recoupling records; baseline keyword lookup returned none, which is not evidence of absence. Actual primary source excerpts attached, with locators. Strong classical alternatives: Panova Theorem1.1 and Proposition5.1, fixed-row polytope algorithms, generic character expansion. Newer Campbell2604.23286 introduces Giambelli/Littlewood/hook expansions; source-priority remains unresolved. Do not assert novelty. Do not extrapolate to growing d,e, all ratio-promised triples, binary-size poly time, coherent multiplicity transforms, hidden-subgroup decoders, or hardness.

Current STATE context: bosonic parent GLOBAL-gap certificate refuted; no runtime lower bound. Community and quadratic-tower endpoints closed. This is a distinct explicit classical operation aimed at a published remaining quantum-comparison regime. Goal is decisive analysis, no infrastructure or numerical evidence of scalability.

STATUS: CLOSED WRITTEN after full parent checks of the independent proof and both terminal paid reports. Parent
read and checked the entire 204-line independent proof in
`audits/reviews/2026-11-13-super-schur-native-audit.md`. All 51 finite target
identities across 14 small parameter cases passed the independent Sage
Kronecker comparison; the deliberately wrong tensor parity was detected.
Those controls check signs and coefficient aliasing only, not scalability.

## Exact theorem and checked compiler

For every fixed positive d,e there is a deterministic exact algorithm for
all supplied partitions lambda,mu,nu of numerical n, with Durfee(lambda)<=d
and Durfee(mu)<=e, that computes g(lambda,mu,nu) in
C_(d,e)*(n+1)^(6(d+e)+12) bit operations and polynomial storage. This is an
unoptimized written upper bound, not a benchmark or implemented full solver.

The universal identity follows directly from Frobenius characters and
p_r(X tensor Z)=p_r(X)p_r(Z), without a supermodule semisimplicity premise.
Hook vanishing and the distinct unit-leading monomials follow from
hs_alpha(x|y)=sum_(rho subset alpha) s_rho(x)s_(alpha'/rho')(y).
The lexicographically largest rho is exactly the first d rows; the remaining
skew shape is a translate of the residual column partition. The resulting
exponent vector reconstructs alpha. Therefore extraction preserves each
individual ordinary Kronecker coefficient.

There are at most M=(n+1)^(2d+2e) basis pairs and dense monomials. The tensor
polynomial has bidegree(n,n), hence every individual variable exponent<=n.
Integer evaluation on {0,...,n}^(2d+2e), truncated complete-function
recurrences and a pivoted exact determinant compute its values. All required
h indices are <=n, since alpha_1+length(alpha)-1<=n. Hadamard bounds give
O_(d,e)(n^2 log(n+1))-bit determinant minors. Tensor interpolation has
common denominator dividing (n!)^(2d+2e), so every intermediate is paid.

Peel the largest remaining monomial, decode its unique hook pair, and
subtract its coefficient times that product basis polynomial. At most M
iterations occur. The exact Kronecker expansion has nonnegative coefficients;
each residual is the sum of its remaining positive terms. All coefficients
are bounded by the original polynomial's value at ones, at most(4de)^n.
Thus neither the interpolation nor the subtraction conceals exponential bit
length. A loose per-polynomial compiler bound C*M^2*(n+1)^10 gives the
stated total bit clock. Arbitrary nu is read and handled by its own at-most-
n determinant; no full character table or p(n)-partition enumeration occurs.

## Source and claim boundaries

The parent inspected actual Panova2502.20253v2 LF1065-1078: section7.5 calls
the bounded-Durfee computation unclear, and section7.6 explicitly separates
unary/numerical n from binary input. The algorithm above addresses that
stated scope, but priority remains unverified. No publication or novelty
claim is made. Moens/Van der Jeugt retained proceedings section3 equations
15/16 supply the complete-function and determinant conventions; Pragacz
Theorem3 supplies an independent basis statement, with its difference-
alphabet convention converted by B=-y. The elementary proof also verifies
these needed interfaces directly.

Packet correction: the two paid briefs' source selection stopped at Panova
LF1063 and omitted the actual section7.5 paragraph, although the contract
accurately described it. Their algebra/bit reviews do not depend on that
paragraph and must not be used as source-priority verification. The parent
read the actual paragraph separately. Preserve exact submitted packets.

The native exact control is `audits/controls/super_schur/exact_identity.py`
and its neighboring JSON. It uses Sage ordinary Kronecker products only as
finite reference values; those operations are NOT supplied to the proposed
algorithm. No quantum implementation, growing-Durfee polynomial algorithm,
full dimension-ratio match, binary-size polynomial clock, coherent transform,
hardness or speedup follows.



## Terminal Claude algebra review

The complete 189-line report was parent-read and its session reaped; saved
usage estimate USD0.521544. Core parity, homomorphism, hook vanishing and
leading-monomial arguments agree and were checked directly. The detailed
204-line compiler closes its O1/O2/O6 cost obligations. Separable matrix
back-substitution is optional: the charged product-peeling algorithm already
proves exact extraction. Its Durfee(nu)>2de early exit is a valid optional
corollary, not a necessary missing operation. Convention consistency and
zero final residual are justified by the formal identity and checked by the
finite control; no implementation is claimed from that control.

The report correctly noticed the omitted source paragraph. Its conditional
warning about ONE hook and TWO arbitrary partitions is correct, but the
actual Panova section7.5 assumes bounded Durfee for the other two partitions,
so it is covered. The report's opening suggestion that the cited one-hook
case is uncovered is not adopted. Its rough bit exponent is not substituted
for the explicitly checked conservative bound. No report label is evidence
for novelty or a quantum speedup. OpenAI's separate full-clock review is now terminal and fully checked below.


## Closed pass and independent exact compiler

OpenAI's entire 327-line report was parent-read and reaped, saved estimate
USD1.312230. It independently proves the same identity and basis extraction,
and gives a different exact determinant compiler: compute tr(A^i), then
c_k=-(1/k)*sum_(i=1)^k c_(k-i)*tr(A^i). The numerator is coefficientwise
divisible by k, since these are coefficients of det(I-tA). Singular matrices
are included. Intermediate degree is O(n^2), coefficient bits are
O_de(n^2 log(n+2)), and dense fixed-variable arithmetic gives its looser
clock O_de((n+1)^(8(d+e)+2max(d,e)+10)). Parent checked that argument; it
corroborates existence but does not replace the earlier grid bound.

Both reports found the missing primary paragraph; the actual source was
checked separately. All jobs are terminal, full-read and reaped. Total new
round estimate USD1.833774, not billing or remaining balance.

Parent also read the entire 175-line post-bosonic selection note. Its
positive-multiplicity counterfamily mu=nu=(n-k,k), lambda=(n-2k,k,k),
n=k^3 has exact g=1, R between k+1 and4e(k+1), but min aft=k. The
permutation-module/Kostka proof and hook-factorial estimates were checked.
Thus the discarded ratio-to-small-tail shortcut is false even with positive
multiplicity; this fixed-row example was already classically tractable.

Established: an exact classical polynomial-BIT comparator for two fixed
Durfee bounds and numerical n. Not established: novelty, optimality, a
practical implementation, full dimension-ratio classical matching, quantum
advantage, or any lower bound. The next candidate may address the compact
binary input only with a new explicit coefficient operation; the current
dense polynomial grid cannot be relabelled polynomial in log n.
