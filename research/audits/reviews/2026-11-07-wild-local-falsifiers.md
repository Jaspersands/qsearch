# Scoped review of the wild-local admission falsifiers

7 November 2026. **ACCEPT sections 1--3 and the false claim gates** of
`WILD_LOCAL_SELMER_ADMISSION.md` at the stated scope. I read the actual
`audits/controls/wild_local_selmer/control.py`; I did not execute it or read
a possibly changing result. The control is a finite classical consistency
check, not the proof of either quantified claim. No Git, network or API.

The native general Selmer algorithm remains unadmitted. The two negative
results concern, respectively, generation by unramified curve-point traces
and the specified uniform polynomial sampler. They are not obstructions to
all regular-model constructions, local-image algorithms or quantum methods.

## All unramified curve-point traces vanish

The genus-two example and its sign are correct. Over any finite unramified
F/Q3, the normalized value group is Z. For v(x)>=1, the two factor
valuations are 1 and 2, making f(x) nonsquare. For v(x)<=0,
f(x)/x^5 is a principal unit and therefore square. Hence x is square.
Each x-root factor is x times a principal unit in the corresponding root
extension and is square there. The branch roots have fractional valuation,
so are absent from F; infinity has trivial label. Norm compatibility then
makes every such trace zero.

The degree-two branch divisor has the exact representative

    (9-3 alpha, beta^2-3), alpha^2=3, beta^3=9.

Stoll's factor-divisor formula is (-1)^deg(h)(h(theta)-k(theta)), which
explains the minus sign in the first component. Both normalized valuations
are three and both norms are 54. This gives a nonzero label of square
total norm and spans the one-dimensional image supplied by Lemma 4.4.

The phrase about multiplicity-one components is valid for a method that
ONLY lifts curve points from their smooth multiplicity-one loci over
unramified extensions. It should not be read as excluding a model method
that separately constructs ramified horizontal divisors or other Picard
generators.

## The same proof works at every genus and every odd prime

For every g>=2 and every odd prime p, put m=2g-2 and

    h=X^m-p, k=X^3-p^2, f=h*k.

This is monic separable of degree 2g+1. The two factors cannot share a
root, since their root valuations are 1/m and 2/3. Over every finite
unramified F/Qp, h is Eisenstein, and the cubic k is irreducible because
it has no root of integral valuation. These assertions include p|m and
p=3: characteristic zero ensures separability, and wild ramification does
not change these valuation arguments. Thus the base local image has
dimension 2-1=1.

For v(x)>=1 the valuations of h(x),k(x) are again 1,2. For v(x)<=0,

    f(x)/x^(m+3)=(1-p/x^m)(1-p^2/x^3)

is square. Since m+3 is odd, x is square, and both root-coordinate factors
are square. Therefore all unramified curve-point traces vanish for this
entire family.

Let alpha^m=p and beta^3=p^2. The even-degree h branch divisor has label

    (p^2-alpha^3, beta^m-p).

The first field is totally ramified of degree m, so the competing
normalized valuations are 2m and 3. The second field is totally ramified
of degree three, with v(beta)=2 and v(p)=3, so the competing valuations
are 2m and 3. Since m>=2, both coordinates have valuation exactly three.
Their norms are equal: the first is Res(h,k), because m is even, and the
second is Res(k,h)=Res(h,k), because 3m is even. Their product is a
nonzero square. Hence this label is the missing nonzero direction.

For g=2 use the degree-two h divisor. For g>=3 use the complementary
degree-three k divisor, which satisfies degree<=g. Its formula
(-1)^3(k(theta)-h(theta)) is EXACTLY the same representative
h(theta)-k(theta). Equivalently the two divisor classes sum to div(y)
and are two-torsion. This is one general derivation; no finite sweep is
needed. It does not assert that wild extensions are necessary in every
member of the family, only that unramified point traces are insufficient.

## Uniform Mumford sampling has an exponential rare event

For the separate f_N of section 3, all roots are rational, giving image
dimension four. A nonbranch prime-divisor point with v_3(x)<N has its four
cluster coordinates in one common squareclass before taking norms. Their
norms remain equal, and the square total-norm condition forces the fifth
coordinate to be square. Thus these labels span dimension at most two.
The outer branchpoint has only principal-unit coordinates and adds zero.

A complete source must therefore supply a prime-divisor point with
v_3(x)>=N. Every root of a monic integral h is integral. Such a root forces
v_3(h(0))>=N, including the h(0)=0 case. Each fresh uniform coefficient
draw modulo 3^M, M>=N, has probability exactly 3^-N of this necessary
event. A union bound gives T*3^-N for T raw attempts, even with adaptive
stopping and subsequent rejection of invalid divisors. This does not
cover an adaptively changed nonuniform sampling law. The coefficient
length of f_N is O(N), so ordinary amplitude amplification of this same
rare-event source retains an exponential cost. The explicit input might
enable a different structured algorithm, as the note correctly says.

## Control and claim scope

The script correctly checks the genus-two squarefreeness, exact norms,
prime-ideal normalized valuations and ramification indices. Its Qp factor
calculation is finite precision; the preceding Eisenstein/Newton argument
supplies exact irreducibility independently. The f_N rows check exact
factorization, discriminant valuation, coefficient size and the specified
counting fraction. The local-image dimension is explicitly attributed to
Stoll, not reported as a computed Jacobian group. No finite control is
used to establish the all-extension or all-N statements.

The general polynomial wild/dyadic source, construction clock and full
Selmer endpoint remain UNPROVED; their false gates record non-admission,
not mathematical impossibility. No source theorem for regular-model
construction or complete Picard-to-divisor generation is accepted by
this scoped review.
