# A Paid Small-Parity Classical Search Branch For Complete AG Inputs

31 October 2026. Constructive classical theorem under the retained native
AG reconstruction/arithmetic contracts; independent automated review of
selection, original evaluation frames and rank conditions found no fatal
gap. Not a native backend, novelty claim, uniform sampler or general fixed-q
dequantization. The full rational parity rank is NOT known to be small in
the intended infinite tower.

## Problem, Mechanism And Decision

Input is ONLY the original B,s over fixed F_1019, with complete AG promises

    m=22e, g=5e+1, degG=10e+3=2g+1, k=5e+3, e>=8,
    d(row B)>=12e-3.

Unknown row basis, coordinate multipliers and labelled point permutation
are allowed. Output z must satisfy Bz=s with EVERY coordinate nonzero.
The argument works for every syndrome. Sampling uniformly from the native
solution set is a different question and is not established here.

The quantum comparator is the retained matrix-only ECP/truncated-DQI
sampler, already polynomial with ideal conditional uniform output. The
classical two-component norm sampler works in the proved q^2>=44e range;
NORM_SAMPLER_CLOCK_FALSIFIER.md excludes polynomial fixed-q clocks for its
fresh whole-trial family. The present mechanism bypasses that clock by
constructing a ONE-component anisotropic norm whose coordinates never
vanish. It pays for a larger auxiliary code through a small effective
representative modulo twice the Picard group.

Let J=Jac(X)(F_q), Q=J/2J, r2=dim_F2 Q and N=2^r2. The resulting expected
cost is polynomial in the native input size TIMES N, under the explicit
prime-count check below. Therefore a measured bound r2<=C log2(g), for a
FIXED constant C, gives expected-polynomial classical SEARCH. No hypothesis
that the intended tower has this rank bound is added silently.

## Access Already Paid, And Access That Must Be Carried Forward

The bounded corpus lookup did not find a prior small-degree selector.
It did recover the stronger arithmetic chain:

1. MATRIX_ONLY_BRIDGE.md and the one-point lift reconstruct the embedded
   curve, line bundle H=G+O, labelled points and original section rows.
2. The compact section-ring and one-point-plane adapters construct a
   bounded-degree original-field model, with the explicit maps retained.
3. At FIXED characteristic, Lauder--Wan gives exact Jacobian order in
   polynomial time. The retained prime-sampler/halving review uses verified
   relation lattices and order-two Frey--Rueck pairings to construct the full
   rational 2-primary group, its parity coordinates and rational halves.

These are paid theorem-level constructions, not currently executed native
backends. In particular, exact order and rational halving are no longer
unexplained oracles. The cost is polynomial in fixed p, NOT uniformly in
log p. Actual functions, divisors, original point labels and fiber frames
must survive all changes of representation.

Relevant retained contracts are
bundles/two-component-norm-2026-10-27/MATRIX_ONLY_BRIDGE.md,
bundles/one-point-plane-adapter-2026-10-26/REVIEW_RESOLUTION.md,
bundles/prime-sampler-halving-2026-10-26/REVIEW_RESOLUTION.md, and
bundles/constructive-tower-review-2026-10-27/REVIEW.md, Sections4-5.
The latter supplies normalized finite/infinity modules, RR functions, local
uniformizers and leading units with polynomial height. For a separating
coordinate x, a canonical divisor is div(dx)=Different(x)-2(x)_infinity;
the different comes from the normalized trace-dual modules. This is the
classical explicit-divisor arithmetic, not quantum class-group access.

Primary checks: [Bruin1003.2563, Algorithms3.2/3.8/3.10](https://arxiv.org/pdf/1003.2563)
give uniform CLOSED-prime sampling, pairings and verified torsion relations
under their stated inputs. The sampling correction must be kept. The
[Cascudo--Cramer--Xing RR-system theorem](https://arxiv.org/html/1207.2936)
counts classes satisfying non-effectivity conditions; it does not itself
select our small effective representative. Ordinary RR for a supplied
divisor also does not perform that selection.

## 1. A Certified Prime-Rejection Selector

Set

    n=2e-11 >=5,         C_n=(g+1)(n+6),
    tau=[K+D-G-(22e-3)O] in Q.

The reference O is any known rational point and may lie in D. This is a
degree-zero class; do not omit the degree correction in its definition.
Draw an EXACT uniform closed prime E of degree n, compute [E-nO] in Q,
and accept precisely when it equals tau.

The retained Weil/prime-character estimate, for every nontrivial character
chi of Q, is

    |n sum_(degP=n) chi([P-nO])| <= C_n q^(n/2),
    |n #Primes_n - q^n| <= C_n q^(n/2).

Characters correspond analytically to geometric unramified quadratic covers
in which O splits. This excludes a constant-field parity character; their
cover equations need not be constructed. These estimates follow by removing
proper-divisor terms from the Weil bounds, as detailed in the retained
matrix-lift-access SAMPLER_REVIEW.md, Section5.

Check the integer inequality

    q^n >=16 N^2 C_n^2.                                      (P)

It proves nonemptiness of degree-n primes and bounds every nontrivial
character bias by C_n/(q^(n/2)-C_n)<=1/(4N-1). Fourier inversion on Q gives

    Pr([E-nO]=tau) >= 1/N - C_n/(q^(n/2)-C_n) >= 1/(2N).

The final, slightly loose bound holds also for N=1. Thus expected selector
draws are at most2N. Each draw is paid: Bruin Algorithm3.2 with ell=2g+2,
i=2 permits n<=2ell-2g=2g+4 and requires truncation through6. Its residual
section degree is2ell-n=18e+19>2g-1. The existing arithmetic contract covers
this range. Under(P) the density q^n/#Primes_n is O(n), so the uniform
prime sampler's own expected cost remains polynomial.

As n>1, E is automatically disjoint from rational D. It is not a uniform
Picard-class sample: its exact prime law and explicit acceptance bound are
what are used. No target-conditioned prime sampler is granted for free.

For r2<=C log2(g), (P) holds for all sufficiently large e: its left side
is exponential in e and its right side is polynomial. Finitely many smaller
e may use exhaustive verified search (a C-dependent constant bound), or a
bounded implementation may report UNKNOWN when(P) fails. The old large-field
baseline remains preferable where applicable. No claim of practicality or
uniform polynomial dependence on an input-valued C is made.

## 2. Halving And Original Evaluation Frames

Let L=10e+4. Accepted parity makes

    [K+D-G-E-2LO] in 2J.

Compute a represented half v, and set A=LO+v. Then degA=L and
K+D-G-E~2A. RR gives r=dimL(A)=L-g+1=5e+4=k+1. The point restrictions
are base-point free since degA>=2g; every auxiliary coordinate is nonzero
as a linear functional. The required equivalence is verified, not guessed.

It is unnecessary to search for a global section nonzero at every point.
Divisors G0~G and A may have support on D. Use normalized local evaluations.
For P_i in D choose a uniformizer t_i, and put

    g_i=ord_(P_i)G0,          a_i=ord_(P_i)A,
    C_(j,i)=(t_i^g_i f_j)(P_i),  f_j a basis of L(G0),
    Aeval_(l,i)=(t_i^a_i u_l)(P_i), u_l a basis of L(A).

All are ordinary local-unit/jet operations on supplied functions. At the
one-point lift's O, passing from H to H-O uses the first jet of sections
vanishing at O. Carry the original rows through the reconstruction. In
those rows B[:,i]=lambda_i C[:,i], and a nonzero coordinate gives lambda_i.

There is also a paid fallback if RR returns a different row basis. Solve
the LINEAR equations R C_i=alpha_i B_i in R and alpha. The solution space
is one-dimensional: relative to a true solution it is the diagonal
stabilizer algebra of the complete code. A nonconstant diagonal stabilizer
would have a nontrivial spectral idempotent, splitting the code into two
nonzero disjoint-support parts. Both would have weight at least d(V)>m/2,
a contradiction. Every column is nonzero by base-point freeness. Thus any
nonzero solution has invertible R and all alpha_i nonzero. This argument
must not be applied to an arbitrary disconnected code or at d=m/2.

Choose a nonzero differential omega0 with divisor K. The degree-zero divisor
F=K+D-G0-E-2A is principal. Compute a nonzero t in L(F); degree zero forces
div(t)=-F. Hence omega=t*omega0 has

    div(omega)=G0+2A-D+E.

The local leading value

    w_i=(t_i^(1-g_i-2a_i) omega/dt_i)(P_i)

is nonzero at EVERY P_i because E avoids D. Set h_i=w_i/lambda_i when rows
are carried explicitly, or h_i=alpha_i*w_i in the fallback basis. The
residue theorem now gives

    B (h * Aeval_l * Aeval_j)=0 for every l,j.                 (M)

This constructs a full-support multiplier; choosing an arbitrary vector
of (V*Aeval^2)^perp would NOT suffice. Polynomial-height class arithmetic,
RR and local evaluation pay the entire construction. Support on D causes
no missing residue or evaluation oracle.

Conversion of original rows to actual plane-field functions is also paid.
Set ell=2g+2 and L0=ell+1. Choose the added lift section sigma, nonzero at O.
For each original section s_j solve

    sigma P(x,y)=s_j Q(x,y),       degP,degQ<=L0.

Use a basis of plane polynomials modulo its equation. If x,y are ratios of
degree-two sections with common denominator h, clear h^L0 to obtain linear
equations in R_(2L0+1)=R_(4g+7), supplied by the retained compact ALL-DEGREE
ring. Enumerating all degree-L0 monomials in the original embedding
coordinates would be exponential and is NOT the algorithm.

Existence: plane polynomials of degree<=L0 have codimension
delta=p_a-g=2g^2 in L(L0*ell*O). The subspace
L(L0*ell*O-div(sigma)) has dimension L0*ell-ell+1-g>2delta. Intersecting it
with that polynomial space and its inverse image under multiplication by
s_j/sigma leaves a nonzero Q. A nonzero solution cannot have Q=0 because
the coordinate ring is a domain and the polynomial basis was reduced
modulo its equation. Thus f_j=P/Q=s_j/sigma is explicit. The maximum pole
divisor of all lifted ratios is H0=div(sigma), by base-point freeness;
G0=H0-O represents the original code. These functions also distinguish
normalization branches at plane singularities. The required ring depth
extends the existing plane-adapter depth by three.

## 3. One-Component Norm Search

Choose a nonsquare nu in F_q and a uniform offset a in F_q^m. For t in F_q^r,
put

    y=h * ((a+Aeval^t t)^2 - nu).

Every coordinate is nonzero. By(M), By=c+Mt is affine, with

    c=B(h*(a^2-nu)),       M=2B diag(h*a) Aeval^t.

For every nonzero row combination c0 in V, its support has at least12e-3
points, strictly more than degA=10e+4 for e>=8. A nonzero section in L(A)
cannot vanish at all these points. Thus Aeval restricted to support(c0)
has rank r. For each nonzero lambda, M^t lambda is uniform in F_q^r;
a union bound gives

    Pr(rankM<k) <=(q^k-1)/q^(k+1) <1/q.

Retry offsets until rankM=k, solve M t=s-c, and verify ORIGINAL By=s and
all nonzeros. The selector is target-independent and rank success is
uniform in s, so the preprocessing serves every syndrome. No claim of
uniform output follows from this deterministic/affine completion.

The total expected cost is poly(m) times at most2N selector draws, plus
polynomial expected preprocessing and offset work at fixed q. For arbitrary
r2 this statement remains parameterized/exponential, not a full fixed-field
classical algorithm. A generic simultaneous-isotropy substitute for A would
also need the restriction-rank condition; dimension and(M) alone do not
imply it.

## 4. A Source-Matched Falsifier For Marked-Point Selectors

On the actual unramified S-split tower, let I be the degree-e pullback of
base infinity and O a marked point above it. The canonical and evaluation
divisors satisfy

    K~10I,      D~22I,       K+D~32I.

Therefore tau equals [G-(10e+3)O] in Q: their difference is twice a rational
degree-zero class. The selector is exactly small EFFECTIVE parity
representation of the original prime G, not simply generic rational halving.

At every level, a further geometric S-split quadratic cover exists by the
retained infinite-tower argument. Its nontrivial character chi annihilates
every marked-point difference P-O. Any E supported only on those marked
points consequently has chi([E-nO])=+1. Such an E is IMPOSSIBLE when
chi(tau)=-1, regardless of the number of marked points or a linear-algebra
search among them.

Under the intended uniform degree-d=10e+3 CLOSED-prime source G, the same
single-character bound gives probability in
[(1-epsilon_d)/2,(1+epsilon_d)/2] for that obstructing sign, where
epsilon_d<=2(g+1)(d+6)q^(-d/2). Subsequent full-cube rejection can change it
by at most epsilon_cube/(1-epsilon_cube). Both errors vanish exponentially.
This is not a hardness statement or a falsifier for arbitrary unmarked
closed primes. It rules out the natural all-marked-point shortcut on
approximately half of the actual source, without replacing its law.

The infinite tower supplies NO proved logarithmic bound on the full r2.
Its depth log2(e), the dimension of a chosen cover, and the rank of the
S-split quotient are not substitutes for dim J/2J. Consequently the new
small-parity branch does not close the remaining fixed-field family.

## Verification And Next Decision

Independent reviewers accepted the selector bound, paid halving chain,
intrinsic-frame multiplier and marked-point obstruction. The exact Sage
control ag_small_parity_identities.sage passed: unique frame recovery under
hidden row/column scalings, failure of uniqueness at the strict-distance
boundary, all49 original F7 syndromes with full-support outputs, and exact
offset-rank failure49/2401. These are minimal output-stage falsifiers.
It is not a native genus-growing implementation or evidence for small r2.

Next hard question is whether a NON-enumerative low-degree parity selector
exists for the remaining large-r2 inputs. Known order/halving and ordinary
RR do not answer it. No source backend, Pic/2 table, marked-point sweep or
general isotropy workbench is justified without a new constructive mechanism.
