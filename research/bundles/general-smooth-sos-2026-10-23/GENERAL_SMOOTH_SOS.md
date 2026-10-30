# Constructive Smooth Sums Of Squares Beyond The Surface Case

2026-10-23. PROPOSED LEMMA; INDEPENDENT REVIEW PENDING.

This is an exact algebraic extension candidate, not an implemented
higher-dimensional quantum algorithm. The eight-copy surface construction
remains preferable for dimension two. The generic construction below has
astronomical stabilization dimension even in small higher dimensions.

## 1. The Specific Blocker

The surface source uses the quadratic identity H^2-tH+I=0 to construct
commuting integral polynomials c_i(H) with sum c_i(H)^2=D^2 H, where D is
squarefree and has only small auxiliary prime factors. A general positive
integral symmetric unit H need not satisfy a quadratic identity.

An abstract four-square representation over a number field does NOT solve
the source problem: its denominators may contain large primes, and points
at those primes are not free. Nor may one simply clear denominators by a
huge power of 2 and treat that entire prime-power torsion as accessible.

The following proposed constructive argument instead uses a rational
positive cone, exact rounding, and a correction lattice. It yields an
integral certificate with a freely chosen sufficiently large EVEN D. D can
therefore be squarefree, smooth, common to every input in a height class,
and coprime to prescribed odd primes. No factoring of the polynomial's
discriminant or of its values is needed.

## 2. Precise Algebraic Statement

Let f be monic in Z[x], squarefree, of degree n, with constant term +1 or
-1 and all roots strictly positive and real. Let n<=d and coefficient
height at most h, where d,h are public uniform bounds. Set R=1+h.

The proposed algorithm constructs, in polynomial bit time in d and log h
apart from the standard integer four-square step, nonnegative integers w_i
and integral polynomials p_i of degree below n such that

    sum_i w_i p_i(x)^2 = D^2 x mod f,
    number of weights = 3n-1.

The bit length of D and every coefficient is polynomial in d and log h.
D is one squarefree product of small primes shared across the whole height
class. Avoid any supplied finite list of odd primes, paying for that list.
Writing each w_i as four integer squares turns this into at most 12n-4
UNWEIGHTED squares in Z[x]/f, without altering D.

The implementation executes and verifies the weighted certificate. It does
NOT implement an asymptotically certified four-square algorithm or execute
the enormous matrix stabilization. Four-square expansion must retain the
unconditional expected-polynomial variant required by the earlier source
audit, not silently import an ERH-dependent algorithm. The arithmetic
dependency is described in [Pollack and Trevino, Finding the Four Squares
in Lagrange's Theorem](https://math.colgate.edu/~integers/sjs15/sjs15.pdf),
abstract and introduction; its unconditional algorithm is distinct from
the simpler ERH-dependent alternative. This is an imported algorithmic
existence result, not a benchmark of the implementation here.

## 3. A Positive Rational Cone With Explicit Precision

All roots alpha_i lie in [1/R,R]. The upper bound is Cauchy's root bound;
the lower bound applies it to the reciprocal polynomial, using f(0)=+/-1.
The nonzero integral discriminant gives root separation at least

    delta = (2R)^(-d^2).

Indeed its absolute value is the product of squared root differences and
is at least one; bound every difference except the smallest by 2R. The
displayed bound is deliberately weaker than the resulting exponent.

Choose a power of two Q strictly greater than

    96 d^2 R^2 (6R/delta)^d.

Isolate all roots exactly to width at most 1/(4Q), and round interval
midpoints to beta_i=b_i/Q. Then |beta_i-alpha_i|<1/Q. Form the rational
Lagrange interpolation polynomials

    l_i(x) = product_(j!=i) (x-beta_j)/(beta_i-beta_j).

For eta=1/Q, elementary product estimates give

    |l_i(alpha_j)-indicator(i=j)| <= e,
    e = 4d eta (6R/delta)^d <= 1/(24d R^2).

For an off-diagonal value, one numerator factor is at most eta, the
others at most 3R, and all denominator factors are at least delta/2.
For a diagonal value, write each factor as 1+z with |z|<=2eta/delta;
eta<=delta/(4d) bounds the product's deviation by 4d eta/delta.
Both estimates are covered by the displayed conservative e.

Let B_(j,i)=l_i(alpha_j)^2. Its infinity-norm distance from the identity is
at most 2e+d e^2 <= 3d e <= 1/(8R^2).

Include the fixed integral polynomials

    1, 1+x^j, 1-x^j  for 1<=j<n,

and let T be their sum of squares. For every positive root,
T(alpha)<=4d R^(2d). Set epsilon=1/(8d R^(2d+1)). Thus

    1/(2R) <= alpha_j-epsilon T(alpha_j) <= R.

Solving B z=(alpha_j-epsilon T(alpha_j)) gives strictly positive z:
the inverse perturbation changes each component by at most 1/(4R).
This is an existence/conditioning argument. No algebraic root arithmetic
is needed to solve for the ACTUAL coefficients below.

Clear denominators in the l_i with the common positive integer

    M = product_i |product_(j!=i) (b_i-b_j)|,
    q_i = M l_i in Z[x].

The square columns q_i^2 mod f are an invertible rational matrix in the
coefficient basis 1,x,...,x^(n-1): evaluating at the distinct roots converts
it to M^2 B. Solve the rational coefficient system exactly. The solution
has positive entries z_i/M^2. Together with weight epsilon on EVERY fixed
polynomial, this produces a strictly positive rational weight vector w
with A w=x, where A contains the reduced square columns.

This works in the monogenic order Z[x]/f, including reducible squarefree f.
It does not assume that the order is maximal or compute its discriminant
factorization, unit group or ideal classes.

## 4. Removing All Uncontrolled Denominators

This is the important step. Do NOT clear the denominators of w directly.
For the desired even D, initially set

    v_i = 4 floor(D^2 w_i / 4).

The residual Rvec=D^2 x-A v is in 4 Z^n, and each coefficient satisfies

    |Rvec_j| <= 4 sum_i |A_(j,i)|.

Correct its constant coefficient by adding Rvec_0 to the weight of 1.
For j>=1 use the exact identity

    (1+x^j)^2-(1-x^j)^2 = 4x^j.

Add Rvec_j/4 to the weight of 1+x^j and subtract it from that of 1-x^j.
The corrected vector has EXACT image D^2 x. Negative corrections are
bounded independently of D. Since every fixed polynomial started with
weight epsilon, all corrected weights remain nonnegative once

    D^2 epsilon > 4 max_j sum_i |A_(j,i)| + 4.

This explains both the even-D requirement and why arbitrary rational
denominators in the intermediate cone computation do not create expensive
torsion primes. The procedure checks all weights and the final identity
with exact arithmetic. It does not infer equality from root approximations.

## 5. A Query-Independent Denominator Bound

The following deliberately loose bounds are implemented. Since the beta_i
lie in [-R-1,R+1], the integer polynomial q_i coefficients are bounded by

    P = (3RQ)^(d^2-1).

Bounding reduction modulo f with its companion matrix gives the entry bound

    Amax = max(4, 4d^2 P^2 (dR)^(2d)).

There are at most 3d-1 columns, so put

    C = 4(3d-1) Amax,
    Theta = (C+8)/epsilon.

Choose D as a product of successive allowed primes, including 2, until
D>Theta. This is overkill relative to the square-root threshold, but gives
a simple uniform certificate. Its bit length is polynomial in d and log h;
standard bounds on primes also bound the largest auxiliary prime
polynomially in that bit length and the number of excluded primes.

The SAME D works for every n<=d and height<=h, not merely the polynomials
seen in a sample sweep. Tests explicitly include different degrees sharing
one denominator. The real-root approximations are internal arithmetic,
not advice or quantum access to spectral data.

## 6. Conditional Repolarization Consequence

Suppose H is an integral positive Rosati-symmetric UNIT. Its minimal
polynomial is squarefree with positive real roots; integrality of H and
H^(-1) gives unit constant term. If it has degree n and a public height
bound as above, substitute H into the certificate and expand the integer
weights into four squares. This yields commuting symmetric c_i(H) with

    sum c_i(H)^2 = D^2 H.

For k commuting coefficients, a recursive integral orthogonal design gives
a matrix C of size 2^(k-1) with C^dagger C=C C^dagger=(sum c_i^2)I.
One explicit recursion, starting with [c_1], adds c via

    [[C, c I], [-c I, C^dagger]].

Its two norm identities follow by block multiplication. Polynomial entries
commute, and the involution fixes the coefficients. Pad the coefficient
list with zeros to the SAME k=12d-4 for every input; otherwise geometric
dimension would depend on the query.

Writing H_N for N copies, F=H_N^(-1) C^dagger is integral and satisfies

    F^dagger H_N F=D^2 I,       FC=CF=D^2 I.

This has exactly the algebraic form needed by the preceding stabilized
source. Squarefree D only requires small prime-square kernel data. The
prime-square flag bundle handles non-free local kernels and proves their
field stability under the paid common-definition-field promise.

CAUTION: this does not supply a full higher-dimensional source/receiver
theorem. The lift compiler, uniform height bound over its domain, marking
rigidity, coherent resource bound and a suitable hidden-subgroup receiver
must all be checked for the intended dimension. The present implementation
does not call any geometric quotient primitive.

For H conjugate to S=sigma^dagger sigma of quaternionic size g, one possible
height bound is (1+T)^g when T bounds its positive trace over EVERY query;
the distinct eigenvalues of the minimal polynomial are among those of S.
This is a route to a uniform bound, not a replacement for verifying the
actual lift compiler. Do not use an observed maximum from finite inputs.

## 7. Severe Limitations And Falsifiers

- Existing arithmetic: this is NOT the first theorem about totally positive
  elements and sums of squares. Kala and Yatsyna, Theorem 1 and Corollary 2
  of [Sums of squares in S-integers](https://arxiv.org/html/2005.06566v2),
  give strong existence results, including five squares after inverting an
  even integer and sufficiently large integral multiples. Their existence
  statements alone do not provide the particular monogenic, explicit
  uniform bit bound and algorithm asserted here. These distinctions need
  specialist prior-art review, not a novelty declaration.
- Positivity is essential. The implementation rejects nonreal, negative,
  repeated-root, nonmonic and nonunit inputs. It cannot certify arbitrary
  self-adjoint operators or an unproved polarization.
- Approximation is not evidence. Precision is bounded explicitly, all
  rational weights are checked positive, and the final identity is exact.
  A failed positivity check is an implementation/theorem failure, not a
  reason to report an approximate certificate as success.
- The four-square step is NOT executed here. Its bit complexity requires
  the separate number-theoretic algorithm already identified in the source
  audit. Certificates currently have nonnegative integer weights.
- Dimension is prohibitive. At d=3, the stated bound is k=32 and N=2^31
  copies. Fixed-dimension polynomial-time language must not hide this cost.
  The generic construction does not replace the eight-copy surface method.
- No classical hardness, cryptographic attack, secret recovery, geometric
  implementation or quantum speedup follows from these certificates.
- Most important falsifiers: a uniform-bound counterexample, a missing
  integral correction, failure of field descent, or a classical algorithm
  recovering the same kernel from the same weak source. Finite controls
  address only the first two, not all of these obligations.

## Decision

Retain this as a proposed general algebraic source lemma with explicit
resource debt. Its leverage is removing a potentially artificial quadratic
restriction, not making the current surface implementation faster. The next
principal-investigator task is independent proof/prior-art review and the
same-input classical attack, not building a gigantic geometric backend.

## Exact Source-Algebra Control

The tests also evaluate the certificate in M_3(O), where O is the full
maximal order of the (-1,-11) quaternion algebra. Let sigma be upper
unitriangular, with entries 3i and 3(1+j)/2 immediately above the diagonal.
Those entries do not commute. Its inverse is checked by nilpotent expansion,
and S=sigma^dagger sigma is congruent to I modulo 3. Exact linear algebra
gives the minimal polynomial

    x^3 - 39x^2 + 282x - 1.

The weighted certificate is evaluated using quaternion multiplication and
verified to equal D^2 S exactly. This is not just a real-matrix example,
but it remains a source-algebra control, not a modeled geometric quotient.
