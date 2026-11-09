# Exact quaternion descent to a compact isotropic vector

7 November 2026. Read STATE/TRAPS and the global-isotropy admission contract.
**The quaternary descent and its compact arithmetic interface are valid**
under the stated supplied compact splitting. The proof below does not pay
the source splitting algorithm or the higher-dimensional/local reduction;
those remain separate composition obligations. No Git, network, API, CAS
implementation, or archive read was used. This is not a novelty claim.

## Exact statement and the sign that must not be dropped

Let K have characteristic zero, let a,b,c,d be nonzero, and put

    q=<a,b,c,d>, D=abcd, L=K(t), t^2=D,
    u=-b/a, v=-c/a, h=t/(bc), B=(u,v)_L.

For the nonsquare case L/K is quadratic with sigma(t)=-t. Write i^2=u,
j^2=v, ij=-ji, and define the L-linear bijection

    phi(x)=x1+x2 i+x3 j+h x4 ij.

Since Nrd(x1+x2 i+x3 j+x4 ij)=x1^2-u x2^2-v x3^2+uv x4^2,

    a Nrd(phi(x)) = q(x).

Suppose rho:B->M2(L) is an L-algebra isomorphism and define

    I={X:rho(X)e1=0}, W=phi^(-1)(I).

I is a two-dimensional minimal LEFT ideal, so W is an isotropic L-plane.
The distinction between coordinate conjugation and coefficient conjugation
in B is essential. Let sigma_B conjugate quaternion coefficients, and let
tau be the quaternion reversion

    tau(1)=1, tau(i)=i, tau(j)=j, tau(ij)=-ij.

This tau is an anti-automorphism, not the usual reduced-norm conjugation.
Direct substitution gives

    phi(sigma(x)) = tau(sigma_B(phi(x))).

Thus phi(sigma(W))=tau(sigma_B(I)) is a two-dimensional minimal RIGHT
ideal. No compatibility of rho with sigma is assumed or needed.

In M2(L), a minimal left ideal consists of matrices killing a fixed line;
a minimal right ideal consists of matrices with image in a fixed line.
Their intersection consists of maps from the one-dimensional quotient by
the former line to the latter line. Its dimension is exactly one, for
EVERY such pair. Consequently

    dim_L(W intersect sigma(W))=1.

The intersection is sigma-stable because sigma swaps its two factors.
For any nonzero v in it, sigma(v)=lambda v. Choose j with v_j!=0 and put
y=v/v_j. Then sigma(y)=y, y_j=1, and q(y)=0. Therefore y is a nonzero
K-isotropic vector. This proves descent for every valid splitting rho,
not merely for a specially chosen splitting or a generic kernel line.

A direct sign check is q=<1,-1,1,-2> over Q. Take t^2=2,
i=diag(1,-1), j=[[0,-1],[1,0]], and h=-t. Then

    W={x1+x2=0, x3+t*x4=0},
    sigma(W)={x1+x2=0, x3-t*x4=0}.

Their intersection is span(1,-1,0,0). Conjugating only the coefficients of
the Q-defined matrix splitting and forgetting sigma(h)=-h would instead
keep the entire plane. This checks the tempting wrong operation; the
all-field result comes from the ideal proof, not this example.

## Explicit constant-size linear algebra

Form the 2-by-4 matrix A with columns

    e1, rho(i)e1, rho(j)e1, h*rho(ij)e1.

Then W=ker(A), sigma(W)=ker(sigma(A)). The stacked 4-by-4 matrix M has
rank exactly three by the preceding proof. Enumerate its four choices of
three rows. A nonzero 3-by-3 minor certifies an independent choice R.
The four signed 3-by-3 cofactors of R form a nonzero vector v in ker(R),
and rank(M)=3 implies Mv=0. Normalize a nonzero cofactor as above. Thus
only a fixed number of field operations and zero/nonzero decisions are
needed; no search over field elements, Hilbert-90 solver, or selection of
a small expanded representative is hidden here.

Applying sigma to a circuit means conjugating its input constants and
preserving its operations and DAG sharing. To return coordinates over the
SUPPLIED K basis, write each relative L element as r+s*t and propagate
component circuits. Multiplication and inversion are

    (r,s)(r',s')=(rr'+D ss', rs'+sr'),
    (r,s)^(-1)=(r,-s)/(r^2-D s^2).

The inverse denominator is nonzero for a nonzero element of the field L.
After normalization, the t component of each y_i vanishes by the descent
proof, so its constant component is the desired K circuit. The compatible
K embedding and relative/absolute basis conversion are part of the paid
construction of L, not an unlabelled abstract-field isomorphism. Each gate
adds constantly many relative operations; binary powers are expanded by
shared repeated squaring. Output may equivalently be numerator/denominator
pairs of division-free circuits with nonzero denominators. This is the
contract's compact field output, not polynomial expanded coordinates.

If D is a square in K, choose its paid square root, take L=K and any
nonzero vector in ker(A). No conjugate-plane intersection is needed. In
either case, an isotropic q gives a nonzero norm-zero element over L, so
B is split. Conversely the preceding extraction from a splitting gives
an isotropic vector over K.

## Ternary case without degenerate padding

For q3=<a,b,c>, use B=(-b/a,-c/a) over K itself. The subspace
V=span_K{1,i,j} satisfies q3=a Nrd|V. If B splits, intersect a kernel
left ideal I with V. Its dimension is at least one by dimensions 2 and 3
inside dimension 4. It cannot have dimension two: that would be a
two-dimensional totally isotropic subspace of the nondegenerate ternary
form, contrary to dim(U)<=dim(U^perp)=3-dim(U). Thus it is exactly a line.
Equivalently, the 2-by-3 matrix [e1,rho(i)e1,rho(j)e1] has rank two, and
its signed 2-by-2 minors give the required nonzero K vector. Conversely a
nonzero isotropic ternary vector gives a nonzero zero divisor in B and
therefore forces B to split. There is no fourth zero diagonal coefficient
and no weakened output relation.

## Paid compact zero tests and verification

Polynomial DAG size alone does NOT permit expansion. The appropriate
test here is bounded-error modular evaluation in the FULL finite algebra
obtained by reducing the explicit number-field multiplication table.
It does not assume a prime-field embedding or that the reduction is a
field. At every division, require the multiplication matrix of the divisor
to have nonzero determinant modulo the sampled prime. Otherwise discard
that trial and charge its cost.

For completeness, let N be the charged field degree and S the total DAG
size of the tested expressions, with H bounding input coefficient bits.
Convert field gates to rational scalar gates using the multiplication
table. An inverse uses the adjugate/determinant of its N-by-N multiplication
matrix; division-free determinant circuits have polynomial size. The
resulting scalar circuit size T is polynomial in N,S and the explicit
table size. Clear rational divisions symbolically as shared integer
numerator/denominator DAGs, without evaluating their enormous integers.
Up to an absolute constant adjustment to T, every integer node has bit
length at most 2^T(H+1). Hence the product of all relevant nonzero integer
numerators and denominators has logarithm at most

    O(T 2^T(H+1)).

In particular the number of bad rational primes is at most this quantity.
Choosing uniformly sampled primes of bit length a sufficiently large
explicit polynomial in T,H,log(1/eta) makes the bad-prime probability at
most the allocated error, by the standard interval prime-count bound.
For example taking a sufficiently padded constant multiple of
T+H+log(1/eta)+log(number_of_tests)+64 suffices. Certified random-prime
generation, finite-algebra evaluation, and determinant inversion have
polynomial bit clocks; cap independent attempts using their inverse-
polynomial prime-generation success probability. No loop through all bad
primes or factorization of an expanded enormous numerator is required.

Outside the bad set, all divisions are defined and every queried zero
test is correct. A true zero cannot become nonzero on a defined trial;
a nonzero element can be mistaken for zero only on the exceptional set.
Use fresh primes for adaptive tests and a union bound over their fixed
polynomial maximum count. The constant-size minors above also permit a
nonadaptive implementation. The splitting relations, final q(y)=0, and
the declared nonzero coordinate can be checked by the same charged
interface. Source-algorithm failure and verifier failure are separate
events in the overall error budget.

## Scope of the completed gate

This gives a uniform polynomial compact postprocessing procedure from a
correct polynomial-size splitting to a nonzero isotropic K vector in
dimensions three and four. It neither assumes expanded small splitting
coordinates nor produces short/integral points or a Witt decomposition.
The existing Amitsur source already claims under-GRH quantum polynomial
splitting; `AMITSUR_ARITHMETIC_REUSE_AUDIT.md` records the compact-output
interface and warns against silently expanding it. Admission of the whole
native solver still requires the source clock and the other dimension/local
steps under their exact hypotheses. No new implementation is justified
by this descent lemma alone.
