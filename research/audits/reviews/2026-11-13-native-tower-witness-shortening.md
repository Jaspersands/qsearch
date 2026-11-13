# Native tower witness shortening — independent proof, 2026-11-13

**Accepted at the stated expanded-input/factoring scope.** An ALREADY GIVEN
nonzero ternary witness over an original quadratic-tower field can be replaced
by one whose extensive absolute height has an ABSOLUTE constant slope in the
coefficient heights. The output bound is independent of the old witness height.
This proves the postprocessing lemma in section 3 of the terminal batched-
compiler report. It does not discover a first witness or, by itself, prove the
report's full coupled tower schedule.

The entire terminal 689-LF report was read, together with STATE/TRAPS and the
stable reset proofs. The maximal-order import was checked against the actual
Buchmann--Lenstra primary theorem, proof and uniform encoding sections. No API,
network, Git, new implementation, numerical sweep or mutable report was used.

## 1. Input, output and normalization

Let K be an ORIGINAL supplied quadratic-tower field of degree n=2^i, with
maximal-order integral basis, exact field/tower conversions, and discriminant
Delta_K=abs(disc K). Every encoded bit is charged. Use natural logarithms and
  H_K(u)=n*h(u),
where h is the absolute logarithmic Weil height. Set H_K(0)=0 and sum this
height over fixed-rank tuples. In particular, the finite contribution is
  sum_P max(0,-v_P(u))*log N(P).
Complex archimedean embeddings are counted twice.

For a diagonal nonsingular ternary
  A*x^2+B*y^2+C*z^2=0,  A*B*C!=0,
put d=-B/A, a=-C/A, and H_coeff=H_K(A)+H_K(B)+H_K(C). Then
  x^2-d*y^2=a*z^2,                 H_K(a)+H_K(d)<=2*H_coeff.  (1)
The algorithm takes an EXPANDED nonzero witness of this equation as input.
It returns an expanded rational K-coordinate witness satisfying
  H_K(x0)+H_K(y0)+H_K(z0)
     <=64*(H_coeff+log Delta_K+n^2).                         (2)
Its runtime is polynomial in the CURRENT expanded field/coefficient/witness
input, with integer factoring and certified finite-field factoring charged.

The square test and root extraction over ORIGINAL K are already constructive:
section 6 of `2026-11-13-tagged-tower-conditional-composition.md` gives at most
3^i<=n^2 calls on the supplied tower, including polynomial-size arguments.
The rational leaf uses integer-square tests. This is not a new conic oracle.
If d=s^2, a binary zero (s,1,0) suffices. If a norm witness with z!=0 is needed,
use ((a+1)/2,(a-1)/(2s),1); it obeys the same bound. Hence assume d nonsquare.

Set L=K(t), t^2=d, so [L:Q]=2n. The old witness must have z!=0, since otherwise
d would be a square (or the witness would vanish). Thus
  beta=(x+y*t)/z !=0,                   N_(L/K)(beta)=a.      (3)
The auxiliary extension will only be used for explicit arithmetic and LLL,
never for a recursive U, conic, isotropy or class-group computation.

## 2. A native auxiliary order with the RIGHT discriminant bound

Factor the principal FRACTIONAL ideal (d), including denominator primes, and
form
  D_d=product_P P^floor(v_P(d)/2),
  J_d=(d)*D_d^(-2)=product_P P^(v_P(d) mod 2).                (4)
The remainder is in {0,1}, including for negative valuations. Thus J_d is
integral squarefree, while D_d can be fractional and nonprincipal.

The preferred initial order is the actual Z-lattice
  A_L=O_K direct-sum (D_d^(-1)*t) inside L.                  (5)
It contains 1 and is closed under multiplication, since
  d*D_d^(-2)=J_d subset O_K.
It is therefore an order of absolute rank 2n. This does NOT suppose that
D_d is principal or that O_L has a free relative integral basis over O_K.
Use the given Z-basis omega_1,...,omega_n of O_K and an HNF-derived Z-basis
eta_1,...,eta_n of D_d^(-1), giving the explicit basis (omega_i,eta_i*t).

The trace matrix is block diagonal: its even block is 2*Tr_K(omega_i*omega_j),
its odd block is 2*Tr_K(d*eta_i*eta_j), and its mixed blocks vanish. Changing
the ideal basis from omega to eta has absolute determinant N(D_d)^(-1).
Taking determinants gives the EXACT absolute discriminant
  abs(disc A_L)=4^n*Delta_K^2*abs(N_(K/Q)d)*N(D_d)^(-2)
              =4^n*Delta_K^2*N(J_d).                       (6)
Since disc(A_L)=disc(O_L)*[O_L:A_L]^2,
  log Delta_L<=2*log Delta_K+2n*log 2+log N(J_d)
              <=2*log Delta_K+2n*log 2+2*H_K(d).             (7)
For the last inequality, each of the positive and negative valuation masses
is at most H_K(d), by the product formula. In particular their sum is at most
2H_K(d); the odd support is bounded by that sum. This elementary order proof
is stronger than the report's 3n*log 2 version and needs no local different
formula or uncharged discriminant oracle.

Everything in (4)--(6) is constructible with polynomial bits in the expanded
input. To find principal-ideal support, choose c with c*d integral and factor
c*abs(N(c*d)); using N(d) alone would miss split numerator/denominator
cancellations. Decompose the factored primes in O_K and compute valuations.
The valuation integers have polynomial numerical size in the expanded input
length; the rational primes have polynomial BIT length, not bounded magnitude. Ideal
products/inverses and integer HNF construct D_d and its inverse. Exact field
arithmetic gives the INTEGRAL multiplication constants of the basis in (5).
No ideal is principalized.

Factor abs(disc A_L), whose bit length is bounded by (7), and use its FULL
radical, retaining primes of EVEN discriminant exponent. The actual
Buchmann--Lenstra 1994 Theorem 1.2 and proof of Theorem 1.3 compute O_L in
polynomial BIT time from this order and radical. Their order representation
uses the degree and n^3 integer structure constants; section 5.9 bounds every
overorder encoding and Theorem 6.7 pays the uniform clock. The stable source
review `2026-11-13-maximal-order-source-check.md` supplies the precise import.
I additionally read actual LF249--281, 1312--1365, 1607--1642, 1720--1730 and
1763--1778 in the retained primary text; physical LF locators are used.

Consequently a maximal-order basis of L, its multiplication table and exact
conversions to K+K*t are computed, not supplied as advice. Certified embeddings
and rational-Gram LLL use the already paid root/metric compiler in the weighted
reset proof. Their intermediate encodings can contain polynomial degree factors.
They are temporary workspace; the HEIGHT bound below uses (7), not a possibly
large monogenic discriminant or the auxiliary basis condition number.

## 3. Remove incoming witness support without finding another witness

Let S* consist of all dyadic K-primes and every numerator/denominator prime of
a and d. This set depends ONLY on the coefficients. Its mass satisfies
  w*=sum_(P in S*) log N(P)<=n*log 2+2H_K(a)+2H_K(d).         (8)
Outside S*, d is a unit and 2 is invertible, so L/K is unramified or split.
The norm identity (3) implies that the parity divisor of beta is pulled back
from a squarefree base ideal R outside S*: at a split prime the two valuations
have even sum and hence equal parity; at an inert prime there is one parity.
Here a is actually a unit outside S*, so the inert valuation is zero, though
this stronger observation is unnecessary.

Construct R by factoring the expanded principal fractional ideal of beta and
recording these parities. All numerator/denominator work is charged to the OLD
witness input length. Apply the independently proved generic ideal reset C1:
  choose w in R^(-1), M=(w)*R integral, with
  N(M)<=3^(n/2)*2^(n(n-1)/4)*sqrt(Delta_K).                  (9)
Its rational Minkowski-Gram computation and recorded LLL vector are polynomial
in the expanded input. It computes neither a class group nor a unit basis.
Outside S*, parity(w*beta) is now the pullback of odd(M), while
  N_(L/K)(w*beta)=a*w^2.                                    (10)

Apply weighted squareclass compression C2 IN L to w*beta. It constructs
  beta0=w*beta*gamma^2 in O_L, beta0!=0.                     (11)
C2 preserves the upper squareclass of w*beta. C1 generally changes the upper
squareclass of beta, which is allowed when replacing a ternary witness.
It preserves the lower norm squareclass, as required in (10).

Let J be the squarefree odd ideal of beta0. At an exceptional base prime P,
the sum of residue degrees of upper primes is at most 2. Outside S*, pullback
has ramification index one and its ideal norm is the square of the base norm.
It follows that
  log N_L(J)<=2*w*+2*log N_K(M).                             (12)
This bound is independent of the old witness height. C2 can introduce new EVEN
valuations elsewhere; these do not enlarge J and must not be mistaken for
new odd support. The dyadic primes were explicitly included in S*.

## 4. Explicit constant-slope output height

For an extension of absolute degree 2n, the proved C2 bound is
  max_sigma |sigma(beta0)|
    <=3*2^((2n-1)/2)*(Delta_L*N_L(J))^(1/(2n)).              (13)
Integrality removes every finite contribution to its height. Combining
(7)--(9), (12), and (13) gives, writing Ha=H_K(a), Hd=H_K(d),
  H_L(beta0)
    <=2n*log 3+n*(2n-1)*log 2+log Delta_L+log N_L(J)
    <=4Ha+6Hd+3*log Delta_K
       +3n*log 3+(5/2)*n*(n+1)*log 2
    <=4Ha+6Hd+3*log Delta_K+7n^2.                           (14)
The last inequality is valid even for n=1. This displays the ABSOLUTE slope;
there is no multiplying degree or coefficient-dependent polynomial in it.

The known involution tau(t)=-t gives
  x0=(beta0+tau(beta0))/2,
  y0=(beta0-tau(beta0))/(2*t).                              (15)
These elements lie in K and are computed by the exact K+K*t conversion.
Furthermore N(beta0)/a is a nonzero square in K, since by (3) and (11)
  N(beta0)/a=(w*N_(L/K)(gamma))^2.                          (16)
One may retain gamma and use w*N(gamma), or use the paid exact root routine
on ORIGINAL K. In either case take z0 with z0^2=N(beta0)/a. Then
  x0^2-d*y0^2=a*z0^2, z0!=0.
There is no search for a new conic point in this extraction.

The standard absolute-height sum/product inequalities, h(1/2)=log 2,
h(t)=h(d)/2, H_L(u)=2H_K(u) for u in K, and conjugacy invariance give
  H_K(x0)<=H_L(beta0)+2n*log 2,
  H_K(y0)<=H_L(beta0)+2n*log 2+Hd/2,
  H_K(z0)<=H_L(beta0)/2+Ha/2.                              (17)
For the last line, H_K(N beta0)<=H_L(beta0) and h(z0^2)=2h(z0).
Thus their sum is at most
  (5/2)*H_L(beta0)+(Ha+Hd)/2+4n*log 2
    <=32*(Ha+Hd+log Delta_K+n^2).                          (18)
Equation (1) proves (2). If an EXACT relative norm-a element is requested,
return (x0+y0*t)/z0; inversion adds another absolute height factor only.

A general nonsingular rank-three form can first be diagonalized by a constant
number of field operations and 3-by-3 solves. Every nonzero pivot and the
inverse coordinate change have height bounded by an absolute constant times
the original fixed-rank coefficient heights plus O(n). This yields the same
form of conclusion with another absolute constant. Formula (2) itself is
asserted for the diagonal ternaries actually used by the native recurrence.

## 5. Finite expanded coordinates, and the limits of this lemma

For the ORIGINAL supplied integral basis of K, the maximum numerator or
denominator bit height of an element u satisfies
  ell_K(u)<=2*H_K(u)/log 2+kappa_K+O(1),                    (19)
where kappa_K is polynomially bounded by the charged original field/basis
input. To see this, choose the least integer m>0 with m*u integral. Its log
is at most the denominator-ideal mass, hence at most H_K(u). Every embedding
of m*u has absolute value at most exp(2H_K(u)); trace-dual/cofactor bounds in
the fixed basis then bound all integer coordinates. This also handles a very
skew supplied basis. The TOTAL encoding has n such coordinates and can carry
an additional factor n. That runtime factor is not a propagated height slope.

The output must remain an expanded RATIONAL-coordinate vector. Unnecessarily
clearing all its denominators and then propagating that chosen integral vector
can add a degree factor to the affine tuple height; it is not part of (2).
Exact output conversion, norm computation, ideal factorization, maximal-order
setup, metric approximation and Gram-only LLL all cost polynomially many bits
in the incoming expanded input. The two stable reset proofs pay the finite
precision, LLL transformation coefficients and termination. No infinitesimal
embedding comparison, unknown condition number or free exact real operation
is being imported here. Integer factoring is still a charged resource.

The retained exact identities (11), (15), (16) and the conic equation certify
an accepted result. Probabilistic factorization routines may use their existing
bounded-clock/certified interface and an assigned failure budget. There is no
new dependence on a chosen numerical tolerance or the old witness's output
height beyond paying to READ and process that input.

Accepted: uniform constant-slope shortening of an existing expanded witness,
including rational K, complex auxiliary extensions, fractional coefficients,
nonprincipal D_d, growing degree and arbitrary charged integral bases. The
new vector need not preserve the old witness's projective point, prescribed
congruences or upper squareclass; those are not the isotropy interface here.
Neither C1 nor C2 can make an exponentially long ALREADY REQUIRED computation
of the incoming witness polynomial. A compact witness is not freely expanded.
The number/dependencies of conic/U batches and their joint original-input bit
bound remain a separate composition proof. No complete tower theorem,
implementation, novelty, hardness or quantum advantage is inferred here.

References used: the terminal `tower-batched-native-compiler/response.md`,
section 3; stable reviews `2026-11-13-squareclass-weighted-lll-compression.md`,
`2026-11-13-conic-content-support-normalization.md`,
`2026-11-13-tagged-tower-conditional-composition.md` section 6, and
`2026-11-13-maximal-order-source-check.md`; actual Buchmann--Lenstra primary
text under `audits/sources/2026-11-13-tower-native-composition/` at the LF
locators specified above. The LLL/metric proof remains the explicit rational-
Gram adaptation in the stable C1/C2 reviews, not an unqualified source import.
