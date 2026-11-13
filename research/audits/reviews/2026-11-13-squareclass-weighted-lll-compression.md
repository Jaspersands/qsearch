# Weighted-LLL squareclass compression — independent proof, 2026-11-13

**Accepted with an explicit arithmetic interface.** Given an EXPANDED nonzero
alpha in F(S,2), this constructs an integral beta=alpha gamma^2 in the same
squareclass whose expanded height is bounded by the field data and S, and
is independent of alpha's incoming height. Runtime is polynomial in the
expanded INPUT length, with integer factoring charged. There is no unit
basis, ideal principalization, class group, or compact-output expansion oracle.
This is a representative-compression lemma, not the total tower clock.

STATE/TRAPS and the corpus `been-tried`/`baselines` lookup were checked. No
network, API, Git, implementation or new numerical sweep was used. The parent's
huge-unit Sage control is consistent with the proof but is not its evidence.

## 1. Exact input and conclusion

Let F be a number field of degree n, with a supplied integral basis
Omega=(omega_1,...,omega_n) of the MAXIMAL order O_F, and exact multiplication
or equivalent primitive-element/basis-conversion data. The basis may be
arbitrarily skew; its encoded size is charged. An arbitrary nonmaximal order
is not silently substituted for O_F. Computing a missing maximal order is a
separate native setup operation, not part of this lemma's input promise.

Let alpha!=0 be given in expanded rational coordinates. Let S be a finite set
of finite F-primes, and assume v_P(alpha) is even outside S. Set
  I = product_P P^(-floor(v_P(alpha)/2)),
  J = (alpha) I^2 = product_P P^(v_P(alpha) mod 2).
Here mod 2 means the remainder in {0,1}, including for NEGATIVE valuations.
Thus I is a fractional invertible ideal, J is an integral squarefree ideal
supported in S, and N(J) is a positive integer.

There is a polynomial-bit algorithm, using integer factoring and standard
finite-field factorization, returning gamma in I\{0} and beta=alpha gamma^2
in O_F with
  max_sigma |sigma(beta)| <= C_n (|disc F| N(J))^(1/n),
  C_n = 3 * 2^((n-1)/2).                                      (1)
Its finite arithmetic/precision clock is polynomial in n, the field/basis
input, and the expanded alpha length. Conditional on the factorizations, the
metric approximation and reduction below are deterministic. Factoring is
not asserted to be an unconditional classical polynomial-time operation.
The usual certified bounded-error factoring interface can be used without
changing any mathematical guarantee on an accepted output.

The OUTPUT beta height in (1) does not depend on alpha. The certificate gamma
may depend on, and have size polynomial in, alpha's expanded input length.
Reading a long alpha, or constructing gamma, is not free.

## 2. The determinant identity and the short vector

Use the Minkowski embedding into R^n with each complex pair represented by
sqrt(2) Re and sqrt(2) Im. On F tensor R define
  q_alpha(x) = sum_(real sigma) |sigma(alpha)| sigma(x)^2
              + 2 sum_(complex pairs sigma) |sigma(alpha)| |sigma(x)|^2.
It is positive definite; no choice of an algebraic square root of alpha is
involved. For an exact Z-basis eta_1,...,eta_n of I let Q be its real Gram
matrix. With this doubled complex convention the unweighted covolume is
  sqrt(|disc F|) N(I).
The determinant of the diagonal weight map is |N_(F/Q)(alpha)|^(1/2).
Consequently
  det Q = |disc F| |N(alpha)| N(I)^2
        = |disc F| N(J) >= 1.                                 (2)
The equality applies to fractional ideals and signed field norms, using the
absolute norm in (2). No extra power of 2 occurs at complex places.

For any gamma in I, (alpha gamma^2) is an integral ideal because
(alpha) I^2=J is integral. Hence beta=alpha gamma^2 belongs to O_F. Moreover,
  |sigma(beta)| = |sigma(alpha)| |sigma(gamma)|^2 <= q_alpha(gamma)
for every embedding, and beta/alpha=gamma^2 proves the squareclass assertion.

The usual delta=3/4 LLL bound for a Gram matrix G is
  G(z,z) <= 2^((n-1)/2) (det G)^(1/n)
for the first reduced nonzero integer vector z. We will apply this to a
rational Gram Qtilde satisfying Q/2 <= Qtilde <= 3Q/2. Then
  q_alpha(sum z_i eta_i)
    <= 2 Qtilde(z,z)
    <= 3 * 2^((n-1)/2) (det Q)^(1/n),
which proves (1). Exact LLL on the transcendental-looking Q is unnecessary.

## 3. Computing the fractional ideal, with its cost visible

Choose an integer c>0 for which c alpha is integral. The integer
c*|N(c alpha)| has bit length polynomial in the expanded input. Factor it,
decompose the relevant rational primes in O_F, and compute the valuations
of (alpha) by ideal containment/arithmetic. This includes denominator primes;
using only N(alpha) would miss cancellations between split valuations.

All valuations have total weighted absolute size bounded by the numerator
and denominator principal-ideal norms. In particular their numerical
magnitudes are polynomial in the input bit length. Ideal products, inverses
and HNF give I and a rational coordinate basis eta_i with polynomial bits.
For example P^(-1) is computed as {x: xP subset O_F} by rational linear
congruences; no generator of P is sought. Binary powering or sequential
multiplication with HNF both have a polynomial bound here.

Given the maximal-order multiplication table, primes above a factored p can
be computed from the finite algebra O_F/pO_F, including its nilradical and
semisimple factors. Finite-field linear algebra and factorization have cost
polynomial in n and log p. Ramified primes do not require enumerating p
residue elements. These are the ordinary native ideal-arithmetic operations,
not a class-group oracle. Alternatively, a verified principal-ideal
factorization may be supplied explicitly to this lemma.

Norms, HNF determinants and the identity (alpha)I^2=J provide exact checks.
The norm N(I)=|det C| is read from the rational change-of-basis matrix C from
Omega to eta. Thus the determinant lower bound (2) is certified arithmetic,
not a numerical estimate or an assumed condition number.

## 4. A finite rational approximation to the metric

Compute nonnegative integers A,B with
  |sigma(alpha)| <= 2^A,   |sigma(eta_i)| <= 2^B
for every i and embedding. Elementary root bounds and the rational coordinate
sizes give such A,B polynomial in the expanded input. Put
  m = ceil(log_2(max(2,n))),
  c0 = A+2B+m+1,
  K = c0+m,
  P = (n-1)K+m+4.
Every |Q_ij|<=2^c0 and lambda_max(Q)<=2^K. Since det Q>=1,
  lambda_min(Q) >= 2^(-(n-1)K).                                (3)
Compute a symmetric dyadic Qtilde with entrywise error at most 2^(-P).
Then its operator-norm error is at most n 2^(-P), at most one sixteenth of
the lower bound (3). In particular Q/2 <= Qtilde <= 3Q/2, as required.
These integers prescribe a finite precision BEFORE LLL; there is no adaptive
search for a floating pivot or sign of a nearly vanishing Lovasz comparison.

For completeness, the embedding oracle here can be compiled in polynomial
bits. If only a multiplication-table presentation is supplied, a primitive
integral theta is found by testing
  theta_t = sum_(i=1)^n t^(i-1) omega_i,
for 0<=t<=(n-1) binom(n,2). For each pair of distinct embeddings, equality
of their values on theta_t is a nonzero polynomial in t of degree <=n-1.
Thus some candidate is primitive. Rank of 1,theta,...,theta^(n-1) tests it
exactly, with polynomial coefficient growth. Rational inversion gives the
basis conversions and a monic integral minimal polynomial f, all with
polynomial bits. No number-field factorization oracle is needed for this step.

Here is one explicit finite root-approximation justification. Take R>=1 with
all roots of f in |z|<=R. For n>=2, integrality and nonvanishing of disc(f)
give separation at least delta0=(2R)^(-n^2): bound all other pairwise
root differences by 2R in the discriminant product. To approximate every
root within r<=delta0/4, require coefficient error E such that
  E (R+1)^n < r (delta0/2)^(n-1).
On each circle of radius r about a true root, Rouche's theorem then places
one approximate root inside. The required negative logarithm of E is
polynomial in n, log R and log(1/r). Actual Corollary 1 of Mehlhorn–Sagraloff–
Wang supplies this approximate factorization in polynomial BIT time, not
merely a numerical root-finder assertion. Monicity gives its leading-
coefficient hypothesis. Degree one is immediate. A permutation matching of
the roots is unnecessary because Q sums over all embeddings.

Evaluate alpha and all eta_i at those approximate roots. On |z|<=R+1 their
polynomial evaluation derivatives have explicit bounds, for example
n^2 2^H (R+1)^(n-1) when coefficient magnitudes are <=2^H. Choose the root
radius to make every evaluation accurate to 2^(-T), with
  T = P+A+2B+ceil(log_2(max(2,n)))+20.
Compute complex absolute values to the same absolute precision by rational
square-root bisection. The absolute-value map is 1-Lipschitz, even near zero.
The formula
  Q_ij = sum_(all embeddings sigma)
           |sigma(alpha)| Re(sigma(eta_i) conjugate(sigma(eta_j)))
then gives the required dyadic entry accuracy, with the displayed guards
and final rounding. This uses polynomial-sized numerical approximations;
it never constructs the compositum of all conjugates or exact algebraic
expressions for their absolute values. Real/complex sign separation of alpha
is not an additional precision assumption.

## 5. Why rational-Gram LLL has a polynomial bit clock

Set G=2^P Qtilde, an integral positive definite Gram matrix. Run the ordinary
LLL Gram–Schmidt updates with EXACT rational inner products, recording the
integer unimodular column operations U. There is no need to realize G as
B^t B with an integer matrix B; that realization need not exist.

Here is the adaptation of the original integer-basis proof. For each current
prefix U_i, the Gram minor
  d_i = det(U_i^t G U_i)
is a positive INTEGER. The potential product_(i=1)^(n-1) d_i starts with
polynomial logarithmic size, never increases under size reduction, and
shrinks by a factor <3/4 on a swap. It remains at least one. Thus there are
polynomially many swaps. Gram–Schmidt lengths are d_i/d_(i-1); Cramer's rule
for the Gram linear systems supplies the same integral denominator bounds
as in the original proof. All these statements require integral pairwise
inner products, not integral Euclidean coordinates.

For an explicit bit bound let B0=max(2,max_i G_ii). Initially d_i<=B0^i;
each d_i is nonincreasing under the relevant swaps. The original geometric
bounds on Gram–Schmidt lengths and partially reduced vectors still apply:
max |b_i^*|^2<=B0 and, at the algorithm checkpoints,
  |b_i|^2 <= n^2 (4 B0)^n.
Size-reduction intermediate bounds are of the same polynomial logarithmic
size. Together with d_i>=1 this bounds the rational Gram–Schmidt numerators
and denominators by 2^poly(n,log B0).

To pay the RECORDED transformation coefficients too, put
M_G=max(1,max_ij |G_ij|). Since det G is a positive integer,
  lambda_min(G) >= (n M_G)^(-(n-1)).
For every current integer coefficient column u,
  ||u||_2^2 <= G(u,u)/lambda_min(G).
The preceding norm bound therefore gives polynomially many bits in u.
All updates, nearest-integer choices and comparisons are exact rational
operations; deterministic tie choices suffice. A comparison near equality
in the TRUE irrational Q is irrelevant: only comparability to Q is needed.
This proves the finite bit clock for G and for gamma=sum_i U_(i1) eta_i.

Source verification: the retained `lll1982.txt` is empty and was NOT used.
I visually checked `lll-p3.png`, `lll-p7.png`, `lll-p8.png`, `lll-p9.png`
(PDF pages 3,7,8,9; printed pages 29,33,34,35). Proposition 1.6(1.9) gives
the short-vector factor; (1.23)–(1.25) give the Gram-minor potential;
Proposition 1.26 and (1.27)–(1.35) give the integer/rational bit bounds.
The Gram-only extension and the bound on U are the explicit arguments above,
not a silent extension of the source's stated integer-coordinate hypothesis.

## 6. Expanded output coordinates and the useful support bound

Let M>=1 bound every |sigma(omega_i)|; this depends only on the SUPPLIED
field/basis data. For example, if all integral multiplication-table entries
have magnitude <=2^H, the eigenvalue bound for multiplication by omega_i
allows M=n 2^H. In a primitive-element presentation the usual root and
coordinate bounds provide M of polynomial logarithmic size instead.

The integral trace matrix T_ij=Tr(omega_i omega_j) has determinant disc F.
Writing beta=sum_i b_i omega_i,
  (b_i)_i = T^(-1) (Tr(beta omega_j))_j.
Use |T_ij|<=n M^2, |Tr(beta omega_j)|<=n M B_beta, where B_beta is the
right side of (1), and the cofactor/Hadamard bound. Since |disc F|>=1,
  max_i |b_i| <= n^(2n) M^(2n-1) B_beta.                       (4)
The b_i are INTEGERS. Thus their bit length is at most
  log_2 B_beta + 2n log_2 n + (2n-1) log_2 M + O(1),
which is polynomial in field/basis data and log N(J), with NO incoming-alpha
term. Exact field multiplication computes beta, and integrality plus
beta=alpha gamma^2 can be verified with rational arithmetic.

If S contains all primes above rational primes p in S_Q, then
  N(J) <= product_(p in S_Q) p^n.
Consequently the sharper archimedean form of the reset is
  log_2 max_sigma |sigma(beta)|
    <= log_2 3 +(n-1)/2 +log_2|disc F|/n
       + sum_(p in S_Q) log_2 p.                              (5)
The output-coordinate bound adds only the field/basis term in (4).
In particular it is AFFINE in the rational support bit-mass. Also
  |N(beta)| <= 3^n 2^(n(n-1)/2) |disc F| N(J).
These bounds do not require computing units or knowing a regulator.

## 7. Exact scope of the gate removed

This pays uniform normalization of an ALREADY EXPANDED supported squareclass,
including fractional inputs, complex fields, growing degree and a poorly
conditioned integral basis. It also prevents repeated products of already
supported representatives from forcing dependence on their whole ancestry:
compress each such expanded product and retain its exact squareclass identity.

It does not discover missing classes, preserve the same algebraic element,
or preserve an exact norm value (only its norm squareclass). It does not
expand a compact unit/power-product at zero cost. It cannot make a previously
exponential computation of the incoming expanded witness polynomial. It does
not bound a conic witness's NEW odd prime support, the number of calls in the
tower DAG, or the auxiliary-prime search. The outgoing beta may have EVEN
valuations at new primes outside S; rejecting it for that reason would be an
error. The odd support J remains within S, as required.

The reusable representative-height gate is therefore closed at the written
input/oracle scope. Aggregate tower support growth and its total clock remain
separate open obligations.

Local source paths: `audits/sources/2026-11-13-tower-recurrence/lll1982.pdf`
and its four inspected page renders; root compiler
`audits/sources/sparse_torus_arch/mehlhorn_sagraloff_wang.txt`, actual
Corollary 1 LF410–418. The older compact-base-2 representative observation in
`ELLIPTIC_TWO_SELMER_COMPOSITION.md` LF131–145 is compatible but does not
supply this weighted-lattice construction for arbitrary expanded alpha.
