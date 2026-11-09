# Local binary-value chooser, including wild dyadic places

7 November 2026. **ACCEPT the revised quadratic-extension/ideal version**
of the local chooser. It is a polynomial-BIT procedure with paid integer
factoring and randomized finite-field routines, hence a bounded-error
quantum polynomial-BIT subroutine using the already charged factoring
primitive. It is NOT asserted to be an unconditional randomized classical
polynomial-time algorithm. No GRH is needed for this local gate itself.

Read STATE/TRAPS, the local prompt and native contract, and the relevant
actual Voight text and errata. The empty Claude response supplies no
evidence. No API, network, Git, implementation, sweep or CAS was used.
The revised construction below supersedes the proposed local-square-root
interface, rather than presuming that interface free.

## Input and paid interfaces

Let K be an explicit number field of charged degree n with its supplied
maximal-order frame, and let p be a specified nonzero prime ideal of O_K.
Write F=K_p. Inputs a,b,c in K* have expanded polynomial-bit coordinates.
Return expanded polynomial-bit s,t in K such that

    q0=a*s^2+b*t^2 !=0 and q0/c is not a square in F.

Use the following interfaces, with all sizes charged:

1. Factor the degree-two polynomial X^2-x over explicit K to decide a
   GLOBAL square and obtain its expanded root when it exists. This is
   ordinary number-field polynomial factorization, not extraction of a
   root from a local-square promise.
2. For globally nonsquare x, construct the degree-2n algebra/field
   K(sqrt(x)), its compatible relative basis and maximal order. Integer
   factoring of the required polynomial-bit discriminant/order integers
   is explicitly charged. Voight Theorem 7.2 states the maximal-order
   algorithm with integer- and finite-field-factorization oracles; it can
   be applied with base field Q to the explicit degree-2n algebra.
3. Factor p O_L and construct residue fields and their reduction maps.
   Voight Lemma 7.16 explicitly gives ideal factorization in arbitrary
   number fields using integer factoring and finite-field factorization.
   Here the rational prime below p is already known; factoring its
   extension ideal introduces no search over rational primes.
4. Use exact HNF/linear algebra for ideal membership, powers, CRT and
   relative-coordinate conversion. Finite-field factorization/nonsquare
   sampling is randomized polynomial time with verified, capped attempts.

Each auxiliary field is quadratic OVER K. The successive square tests do
not form a tower of quadratic extensions. There are only polynomially
many fields of degree at most 2n, with polynomial-bit defining data.

Theorem 6.1 and Algorithms 6.2--6.6 of the actual Voight text also provide
uniform polynomial local Hilbert computations at dyadic primes. They are
not a substitute for constructing a local root or enumerating a table of
squareclasses. The revised chooser does not need them internally. The
provided erratum concerns Algorithm 3.22, which is not used here.

## Square testing by prime decomposition

For x in K*, first perform the global square test. If x is globally square,
it is locally square. Otherwise L_x=K(sqrt(x)) is a field, and

    x is a square in F
    iff L_x tensor_K F = F x F
    iff p splits into two primes with relative e=f=1 in L_x.

This equivalence holds at dyadic and ramified places as well: the nonsplit
completion is a quadratic field, either ramified or unramified. Thus the
paid maximal-order and prime-decomposition routines give a local square
decision without a supplied p-adic embedding or root. This is a
factorization-assisted decision procedure, not a claim that classical
factoring has been removed.

## The actual chooser

If a/c is locally nonsquare, return (s,t)=(1,0). Otherwise a and c have the
same local squareclass, so it suffices to find a nonsquare norm from

    delta=-b/a,   N(s+t sqrt(delta))=s^2-delta*t^2.

If delta=r^2 globally, choose a global element pi in p\p^2. Then

    s=(pi+1)/2,  t=(pi-1)/(2r),  a*s^2+b*t^2=a*pi.

This is the desired class because v_p(pi)=1. The root r is obtained by
the global polynomial factorization interface, not inferred from local
splitting.

If delta is globally nonsquare, build L=K(sqrt(delta)) and factor p O_L.
There are exactly the following three possibilities.

* SPLIT: p O_L=P1 P2. Choose pi1 in P1\P1^2. Ideal CRT gives a global
  integral z with z=pi1 modulo P1^2 and z=1 modulo P2. Therefore
  v_P1(z)=1, v_P2(z)=0, and v_p(N_L/K(z))=1.
* RAMIFIED: p O_L=P^2. Choose pi_E in P\P^2 and set z=pi_E. Its norm
  has valuation f(P/p)v_P(z)=1, even for wild dyadic ramification.
* INERT: p O_L=P, with relative residue degree two. The completion E/F
  is unramified quadratic. Use the finite generating set below to find
  a z whose norm is locally nonsquare.

In every case write the selected global z=s+t sqrt(delta) by exact
relative-coordinate conversion and return s,t. Global and local quadratic
norms agree at this completion (in the split case the local norm is the
product over the two factors). Thus q0=a N_L/K(z) is nonzero and has the
required class.

## The inert case needs only linearly many generators

If E has odd residue characteristic, its unit squareclasses are generated
by a lift of any nonsquare residue unit. Principal units are squares by
Hensel. A random nonzero residue element is nonsquare with probability
one half, and exponentiation tests this condition. In an unramified
quadratic extension, its residue norm is a nonsquare in the base residue
field: the norm of an odd power of a cyclic generator is an odd power of
the corresponding base generator. One such lifted unit therefore suffices.

For dyadic E, put e_E=v_E(2), and let b_1,...,b_f lift an F2-basis of its
residue field. Choose a global pi_E with v_E(pi_E)=1. The elements

    z_(i,j)=1+b_j*pi_E^i,  1<=i<=2e_E,  1<=j<=f,

generate O_E* modulo squares. Indeed the residue-unit group has odd order,
so its classes are squares. For i>=1, U_i/U_(i+1) is the additive residue
field, and products of the displayed generators realize all its elements.
Successively eliminating these layers leaves U_(2e_E+1), which consists
of squares by Hensel at X=1: v(1-u)>2v(2). Adding a uniformizer would
generate all E*/E*2, but it is unnecessary for this inert-case unit test.
The number of candidates is

    2e_E f = 2[E:Q_2] <= 4n.

This is a generating set, not a list of all its exponentially many
products. Test each displayed norm with the square decision above and
return the first nonsquare one.

Why one must succeed does not require an unpaid local-class-field
computation or the full norm-image rank formula. Norms from an unramified
quadratic extension surject onto the base units (Voight Remark 5.3).
Directly, residue norms are surjective, and each principal-unit lifting
step uses the surjective residue trace. The base dyadic field has a
nonsquare unit: choose a residue element beta of absolute trace one and
an integral lift B. Then 1+4B cannot be a square. If r^2=1+4B, the equality
v(r-1)+v(r+1)=2e implies v(r-1)>=e; hence (r-1)/2 is integral and reduces
to a solution of X^2+X=beta, contradicting trace one. Therefore the norm
image contains a nonsquare unit. Since norms send squares to squares, not
all norms of the displayed unit generators can be squares.

The usual index-two norm theorem is consistent with this argument, but
is not needed to establish the chooser or its clock. In the ramified
case, the odd valuation of a uniformizer norm already proves success.

## Expanded global representatives are paid

An integral ideal P in a known maximal-order basis has an HNF Z-basis.
At least one basis vector lies outside P^2, since otherwise P would be
contained in P^2. Testing basis vectors gives the required global
uniformizer without a principal-ideal problem. The residue field is the
explicit quotient O_L/P. Linear algebra gives the residue F2-basis and
global integral lifts in the dyadic case; the analogous quotient supports
odd-characteristic residue sampling. No local-to-global oracle is needed.

The split-case CRT uses comaximal ideals P1^2 and P2. Their norm logarithms
are polynomial, so HNF/CRT gives polynomial-bit representatives. The
dyadic powers have exponents at most 2e_E<=4n. Products and sums of this
many polynomial-height algebraic integers have polynomial expanded
coordinate height. Thus every tested z, its norm, and all subsequent
quadratic-extension defining data have polynomial bit size.

Relative coordinates can be extracted either by a known basis conversion
or by s=(z+sigma(z))/2 and t=(z-sigma(z))/(2 sqrt(delta)). The conversion
matrix and the auxiliary maximal-order basis have polynomial expanded
size by the charged construction. Exact rational linear algebra preserves
polynomial bit complexity. This does not expand a compact S-unit or an
unknown exponentially large field element: all inputs at this gate are
the explicitly constructed polynomial-height elements above.

## Precision for subsequent weak approximation

The revised chooser itself uses exact global arithmetic and finite ideal
quotients, not a numerical p-adic root. Its output s0,t0 and q0 have
polynomial expanded height. The prompt's sufficient approximation bound
is correct. Let e=v_F(2), choose M>=0 with

    M > 2e+v(q0)-v(a)-min(0,v(s0)),
    M > 2e+v(q0)-v(b)-min(0,v(t0)).

For s=s0+epsilon_s, v(epsilon_s)>=M,

    v(a(s^2-s0^2))
      >= v(a)+M+min(e+v(s0),M)
      >= v(a)+M+min(0,v(s0))
      > 2e+v(q0),

and similarly for t. For a zero target coordinate use min(0,v(0))=0.
Thus the new value q satisfies v(q/q0-1)>2e, so q/q0 is a square by
Hensel. It remains nonzero and outside the forbidden class.

These M are polynomial as NUMBERS, not merely as binary encodings.
Valuations of nonzero expanded polynomial-height elements are bounded
by the bit sizes of their cleared denominators and nonzero rational
norms. Hence the required ideal powers have polynomial norm logarithms,
and later ideal-CRT approximation stays polynomial. This establishes only
the local congruence interface; simultaneous real-place approximation is
a separate part of the global construction.

## Clock and scope

There are O(n) square/norm tests, all in fields of degree at most 2n.
Their inputs stay polynomial-bit. Charge all integer factorization,
maximal-order and finite-field factorization calls; verify returned
factorizations and cap randomized routines with independent restarts.
A union bound over the polynomial call count gives the requested error
probability with logarithmic amplification. There is no prime-enlargement
loop, squareclass enumeration, or unbounded-precision local solution.

This closes the revised local gate under the stated standard arithmetic
interfaces. It does not prove the higher-dimensional isotropy reduction,
the entire global solver, novelty, or a classical-input quantum separation.
