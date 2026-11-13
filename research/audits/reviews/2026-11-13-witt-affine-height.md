# 2026-11-13 Absolute-affine fixed-rank Witt reduction

**Independent result: the proposed height lemma (W) holds**, using the already
admitted native GRH scalar-norm backend, expanded-norm postprocessor, integer
factoring, and the proved finite C1/C2 arithmetic. The local 2b repair is valid.
The constants below are explicit consequences of the subroutine bounds and
fixed arithmetic counts; no field-degree multiplier enters the propagated slope.
This proves the rank-at-most-eight operation, not the separate full balanced-tree
composition, novelty, practicality, or an integral/real-field extension.

Read: current STATE/TRAPS; `BALANCED_WITT_EXPANDED_DECOMPOSITION.md`; the full
`2026-11-13-native-tower-witness-shortening.md` and C1/C2 reviews it cites; the
maximal-order source review; the actual local-value and q3/q4 constructions in
`GLOBAL_COMPACT_ISOTROPY.md`. No live paid report, network/API/Git, or test used.

## 1. Quantitative contract and field constant

Let K be a totally imaginary number field, N=[K:Q], with the supplied compatible
maximal-order basis omega_i and expanded field arithmetic. Write H(x)=N*h(x),
H(0)=0, with natural logarithms. For a tuple or matrix, H means the sum of its
entry heights. In particular H(xy),H(x/y)<=H(x)+H(y), and
H(x+y)<=H(x)+H(y)+N log 2. All outputs remain rational K-coordinates; do not
clear their denominators merely to make integral vectors.

Let Delta=|disc K|. Choose the explicit integer W>=1 bounding every
|sigma(omega_i)|: for an integral multiplication table with largest absolute
entry M, W=N*max(1,M) suffices by the multiplication-matrix eigenvalue bound.
Let ell(m) be the binary bit length of a positive integer m. Set

    F = 10 + ell(Delta) + 4N^2 + N*ell(2NW).                 (2)

This is a computable polynomial in the charged field input. It dominates all
field-only expressions below, including 7N log 2, 2N log 6, and the original-
basis CRT constant. Its definition does not use a coefficient-dependent field.

Input is a nonsingular symmetric r-by-r matrix A, r<=8, of tuple height h.
The output is an expanded invertible P and an anisotropic C, rank(C)<=4, with

    P^t A P = H0^(orthogonal w) orthogonal C,
    H0 = [[0,1],[1,0]].

One explicit sufficient conclusion, derived in section 7, is

    H(P)+H(C) <= C_8*(h+F),
    C_8 = 128*(43,000,000 * 3^12288)^4.                    (3)

The constant is deliberately coarse. Its size comes from displayed gate counts,
not an assumed unspecified constant. The algorithm's runtime is polynomial in
the expanded native input and log(1/eta), conditional on the stated imported
backends, with capped failure/ABORT. Equations (2)–(3) give computable size caps.

## 2. Coefficient normalization and general-field conic shortening

C2 applied to a nonzero expanded a returns a'=a*gamma^2 integral. If J is its
squarefree odd ideal, then log N(J)<=2H(a), including fractional a. The exact C2
bound gives

    H(a') <= 2H(a)+log Delta+N log 3+N(N-1)log 2/2
           <= 2H(a)+F,
    H(gamma) <= (H(a')+H(a))/2 <= (3H(a)+F)/2.              (4)

Thus normalizing r<=8 diagonal coefficients has absolute slope and preserves an
explicit diagonal change of coordinates. C2's incoming-size runtime is charged.
The gamma certificate is expanded; no arbitrary compact expression is expanded.

The conic-shortening proof transfers from the original quadratic-tower setting
to EVERY expanded number field F0. Its only tower-specific step was extracting
a square root in F0; replace that by the paid polynomial number-field factoring/
root routine. Everything else uses ideal arithmetic, C1, C2, and maximal orders.
For an existing nonzero witness of A*x^2+B*y^2+C*z^2=0 it gives

    sum H_F0(x0,y0,z0)
       <=64*(H_F0(A)+H_F0(B)+H_F0(C)+log Delta_F0+[F0:Q]^2). (5)

For x^2-u*y^2=v*z^2, u nonsquare, z0!=0 automatically. For u square use the
explicit split formula with z0=1. Hence exact norm solutions X=x0/z0,Y=y0/z0
satisfy X^2-uY^2=v and H_F0(X)+H_F0(Y)<=2*sum H_F0(x0,y0,z0).

The auxiliary-order identity used in that proof is essential. For E=K(sqrt D),
D_D=product p^floor(v_p(D)/2), J_D=(D)D_D^(-2), the order
O_K plus D_D^(-1)*sqrt D has discriminant 4^N Delta^2 N(J_D). Consequently

    log Delta_E <=2log Delta+2N log 2+2H(D).                 (6)

This includes fractional D and nonprincipal D_D. Factoring that known order's
FULL discriminant radical pays maximal-order computation by the checked
Buchmann–Lenstra theorem. A monogenic/basis discriminant is not substituted in
(6). Temporary basis heights affect runtime, not the intrinsic bound (5).

A first witness is available, not advice: apply the admitted scalar norm solver
and the exponent-residue expansion to its genuine small-atom power product.
For relative degree two, reduce each exponent mod 2, expand beta0, and extract
z in the base field with z^2=N(beta0)/v; beta0/z has norm v. Then apply (5).
Its possibly larger intermediate polynomial height is never propagated past
(5). An unexpected NO or failed identity is charged failure/ABORT, not retry.

## 3. Integral local binary targets: all branches

For q5=<a1,...,a5> with all coefficients now integral and nonzero, put
q1=<a1,a2,a3>, a=a4, b=a5, delta=-b/a, and c_forbid=det(q1). Let S contain every
dyadic prime and all primes dividing a1*a2*a3. For each p in S write
alpha=v_p(a), beta=v_p(b), e=v_p(2). All three are nonnegative integers.

If a/c_forbid is locally nonsquare, (s0,t0)=(1,0) already works. Otherwise it
suffices to obtain a nonsquare norm from the quadratic algebra defined by delta.
The following choices are native, finite, and integral before CRT.

If delta=r^2 globally, choose an INTEGRAL pi in p minus p^2. Such an element is
found among an HNF basis of p by ideal membership. The initially fractional
pair ((pi+1)/2,(pi-1)/(2r)) has value a*pi. After multiplying both coordinates
by 2b, it becomes

    s0=b*(pi+1),        t0=(b/r)*(pi-1).

Here (b/r)^2=-ab is integral, so b/r lies in O_K. The value has valuation
alpha+2beta+2e+1 and retains the desired squareclass.

If delta is globally nonsquare, build L=K(sqrt delta), its maximal order, and
factor p O_L. Choose z in O_L as follows.

* Split: CRT z congruent to a P1-uniformizer modulo P1^2 and to 1 modulo P2.
  Then v_p(Nz)=1.
* Ramified: an integral P-uniformizer gives v_p(Nz)=1.
* Unramified quadratic: choose a UNIT at P with nonsquare norm. At odd residue
  characteristic a nonsquare element of the quadratic residue field has
  nonsquare norm; capped uniform residue trials find one with constant success.
  At residue characteristic two, use only the integral principal-unit list
  1+b_j*pi_P^i, 1<=i<=2v_P(2), with b_j lifting an F2 residue basis. The list
  generates units modulo squares: residue units have odd order, each filtration
  quotient is additive residue field, and level 2v_P(2)+1 consists of squares.
  Unramified unit norms are surjective, and the base has a nonsquare unit.
  Thus some listed UNIT has nonsquare norm, found by the paid local square test.
  There are at most 2[L_P:Q2]<=4N entries. No uniformizer is included in this
  branch, so v_p(Nz)=0. This is the necessary repair to the older generating list.

For completeness, unit norm surjectivity here needs no residue enumeration:
finite-field norm is onto, and on successive principal-unit quotients the norm
induces the onto residue trace. In residue characteristic two a nonsquare base
unit can be taken as 1+4rho with Tr_(k_p/F2)(rho_bar)=1; a hypothetical square
would give a root of the corresponding irreducible Artin–Schreier polynomial.
The existing ideal-decomposition local square test or this explicit filtration
implements the tests in polynomial degree/valuation/log-residue bits.

Write z=s+t*sqrt(delta). Although s,t need not be integral, let xi=a*sqrt(delta),
so xi^2=-ab and xi is integral. The exact identities

    2b*s = b*Tr_(L/K)(z),
    2b*t = -(z-bar(z))*xi                                 (7)

show that s0=2b*s and t0=2b*t belong to O_K: the right sides are integral and
fixed by the involution. Their value c0=4ab^2*Nz is nonzero and satisfies

    v_p(c0) <= alpha+2beta+2e+1.                           (8)

The trivial branch satisfies the same bound, with or without 2b scaling.
All constructed global representatives have polynomial expanded input-size
bounds by ideal HNF/CRT and the explicit quadratic conversions. Their heights
are TEMPORARY; only residues at the precisions below are propagated.

## 4. CRT modulus mass and short representatives

Choose

    M_p=4e+alpha+2beta+3,       I=product_(p in S) p^M_p.

If integral s,t equal the local targets modulo p^M_p, then
v_p(a*s^2+b*t^2-c0)>=M_p+min(alpha,beta). By (8) the relative error has
valuation at least 2e+2, so the value/c0 is a square by Hensel. It remains
nonzero and outside the forbidden squareclass. This also pays dyadic places.

Put h=sum_(i=1)^5 H(a_i). Integrality and the product formula give

    w_S=sum_(p in S)log Np <=N log2+H(a1)+H(a2)+H(a3),
    log N(I)<=4N log2+H(a)+2H(b)+3w_S <=3h+7N log2<=3h+F.   (9)

The identity sum_p v_p(2)log Np=N log2 is used here. No factor N multiplies h.

Compute arbitrary integral CRT representatives u0 for s and t. In ORIGINAL K,
ordinary Minkowski-Gram LLL produces nonzero gamma in I with

    max_sigma |sigma(gamma)|
       <=sqrt(3)*2^((N-1)/4)*Delta^(1/(2N))*N(I)^(1/N).

Express u0/gamma in the original basis omega_i and round each rational
coefficient to its nearest integer k_i. Set u=u0-gamma*sum k_i omega_i. Then
u is integral and unchanged mod I, because gamma*O_K is a sublattice of I.
Also |sigma(u)|<=(NW/2)*max_sigma|sigma(gamma)|. Therefore

    H(u)<=log N(I)+(1/2)log Delta
           +N log(max(1,NW/2))+(N/2)log3+N(N-1)log2/4
         <=log N(I)+F.

The same gamma can be used for both representatives. Thus

    H(s),H(t)<=3h+2F,
    H(c), c=a*s^2+b*t^2, <=13h+9F,
    H(a1,a2,a3,c)<=14h+9F.                                (10)

No ideal principalization or CVP oracle occurs. Exact division/rounding and
rational-Gram LLL have the proved polynomial finite-bit clock. Crucially this
short-CRT calculation is never applied in a coefficient-dependent field.

At p in S, (10)'s q4 is isotropic: an anisotropic local ternary represents every
nonzero squareclass except -det(q1), so adjoining c outside det(q1)*K_p^2 works.
Outside S the odd unimodular ternary q1 is already isotropic. There are no real
places. Hasse–Minkowski gives global isotropy. Since S contains dyadic primes,
preserving a nonzero local value also ensures c!=0 globally.

## 5. Explicit small q3/q4 vectors

For diagonal q4=<a,b,c,d> of tuple height h, set D=abcd and E=K(sqrt D), or E=K
with a square root if D is square. Let m=[E:K]<=2, u=-b/a, v=-c/a, and
kappa=sqrt D/(bc). Then

    H_E(u)+H_E(v)<=4h,
    log Delta_E+[E:Q]^2<=2h+2F,
    H_E(kappa)<=3h.

Shorten the conic X0^2-uY0^2=vZ0^2 using (5), then divide by Z0. This yields
X^2-uY^2=v with

    H_E(X)+H_E(Y)<=768h+256F.                              (11)

A concrete quaternion splitting is

    rho(i)=[[0,u],[1,0]],
    rho(j)=[[X,-uY],[Y,-X]],
    A0=[[1,0,X,kappa*u*Y],[0,1,Y,kappa*X]].

Each entry of A0 and its conjugate has H_E at most Q=775h+256F. In the
nonsquare-D case stack A0 and its coefficient conjugate. The reviewed
left/right-ideal argument proves its kernel is a conjugation-stable line and
its rank is three for EVERY such splitting. Select three independent rows;
the four signed 3-by-3 cofactors give a nonzero kernel vector. A determinant
has height at most 18Q+[E:Q]log6<=18Q+F. Divide by a nonzero coordinate.
The ratios lie in K, so H_K=H_E/2. Their summed K-height is at most
72Q+4F=55800h+18436F.

When D is square, the 2-by-4 matrix suffices; a 2-by-3 kernel gives the smaller
bound 24Q+6F. For q3 the same norm solution gives (X,Y,1) directly. Rank two
uses the exact global square test. Thus, uniformly on soluble ranks 2,3,4,

    H(isotropic vector)<=60000*(h+F).                      (12)

All zero tests/minors are exact on expanded coordinates. Conjugation and the
K+Ksqrt D extraction change no intrinsic height. An auxiliary integral basis
can be expensive in h for runtime purposes, but its conditioning is not inserted
in (11)–(12). If a quaternion is nonsplit, the complete admitted norm/local
criterion returns anisotropy; its error is charged to the bounded backend.

For integral q5 use (10), then (12), and lift w to
(w1,w2,w3,s*w4,t*w4). Its summed height is at most

    1,680,006h+1,200,004F <=1,700,000*(h+F).                (13)

For integral diagonal ranks 5 through 8, use any five coordinates and pad the
vector by zeros. Thus (13) also uniformly bounds the smaller soluble ranks.

## 6. Full fixed-rank reduction, with original-coordinate maps

For a nonsingular current core A of rank r<=8, diagonalize over K. If no diagonal
pivot is nonzero, some off-diagonal entry is nonzero; replacing e_i by e_i+e_j
provides pivot 2A_ij. Keep all coordinate changes. Normalize diagonal coefficients
by (4), find the vector by (12)/(13), and map it back by both recorded changes.
There is no claim that these coordinate changes are integral.

For a nonzero isotropic x choose j with lambda=B(x,e_j)!=0. Put y=e_j/lambda,
then replace y by y-q(y)*x/2. Now q(x)=q(y)=0 and B(x,y)=1. Project the remaining
coordinate vectors by z -> z-B(z,y)x-B(z,x)y. Their span is the nondegenerate
orthogonal complement. Exact Gaussian elimination selects r-2 independent
projected vectors and gives its Gram matrix. Accumulate the full basis matrix.
Repeat only on the remaining core. Stop on a certified anisotropic core, or
rank zero/one. A totally imaginary core of rank>=5 cannot be a stopping core.
There are at most four rounds, counting a final negative isotropy test.

## 7. A reproducible coarse constant and finite clock

Here is a scalar-height accounting rule that avoids an unspecified constant:
if every current K-register has height <=B and B>=F, one +,-,*,/ gate creates
a register of height <=3B. Copy, permutation, zero test, or branch selection
increases no height. Field-coordinate arithmetic is charged separately in bits.

One explicit rank<=8 diagonalization, with its 8-by-8 coordinate matrix, uses
fewer than 4096 scalar gates: per pivot, at most 5r+4 operations for a shear,
r divisions, 3r^2 Gram updates, and 2r^2 coordinate updates, with at most eight
pivots. Thus starting at B, all its outputs have height <=B1=3^4096 B.
Normalization (4) bounds each new coefficient by 3B1 and each gamma by 2B1.
The integral diagonal tuple therefore has height <=24B1. By (13) its vector
has summed height <=42,500,000 B1. Applying gamma_i adds at most 16B1 to the
sum; hence every resulting vector register has height <=43,000,000 B1.

Fewer than 8192 more scalar gates suffice for mapping that vector back,
computing its partner/projection, selecting complement columns, evaluating the
new Gram matrix, and multiplying the accumulated 8-by-8 basis matrix:
use 2r^2 for each matrix-vector operation, at most 4r^2 for the projection,
at most 4r^3 for elimination, 4r^3 for Z^tAZ, and 2*8^3 for basis accumulation.
The partner computations and matrix-vector operations together use <1024 further
gates, keeping this total below 8192. Consequently one whole round increases
the register bound by at most

    Q0=43,000,000*3^(4096+8192).

A negative round costs less. Four rounds give Q0^4*(h+F). There are at most
64 output basis entries and 64 Gram entries; summing yields exactly (3).
This derivation deliberately bounds all fixed-rank intermediate registers;
it is not a count of arithmetic inside the imported norm or LLL routines.
Those routines' OUTPUT heights are paid by (4)–(13), and their own uniform
polynomial BIT bounds pay their internal arithmetic.

For runtime and all-branch caps: original-basis numerator/denominator bit length
is <=2H(x)/log2+kappa_K+O(1), with computable field-only kappa_K from the reviewed
trace-dual bound. Input H may be replaced by a computable upper bound obtained
once from expanded coordinates. The deterministic formulas above propagate its
budget. Do not recompute a degree-inflated height estimate after every node.

Every local prime, ideal exponent and residue precision is bounded by the
explicit mass (9); local-generator lists have polynomial size. Every front-end
auxiliary field has degree <=4N and polynomial expanded encoding. Internal
fields of the imported scalar-norm backend retain that backend's separately
proved polynomial bound; <=4N is not claimed for them. Complete factoring,
maximal orders, root extraction, HNF and finite root/Gram approximation have
finite polynomial clocks. The raw norm expansion can be polynomially larger
than its shortened result, but is polynomial in the current input and is read
and processed at that cost. No compact sum is factored or expanded for free.

All probabilistic subcalls use explicit capped budgets and assigned failure
probabilities. Failed certificates or exhausted clocks return ABORT; a false
negative from a bounded-error decision is charged failure. Exact checks of
norm identities, integrality identities, P^tAP and determinant nonvanishing
verify positive arithmetic outputs. These facts pay this operation uniformly;
the full tree's error allocation/composition remains the separate review.

**Conclusion:** (W) is proved with absolute C_8 and field polynomial C_8 F.
The former tower restriction in conic shortening and the local-target/CRT
height issue are removed at this written scope. No dyadic lattice seed,
integral Witt basis, or statement over fields with real places follows.
