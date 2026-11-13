# Fixed-size finite-field polynomial systems: a capped SEARCH primitive

Scope: fixed numbers of variables and fixed total degree; the residue degree grows.
This is a constructive extension of Kayal's retained decision machinery, not a
claim that his Theorem 6.3.8 already states search. No Witt-coordinate or global
integral-isometry theorem is proved here.

## 1. Exact contract

Fix integers n,d. The input is an explicit field
F_q=F_2[T]/(h), q=2^f, with h irreducible of degree f, and polynomials
f_1,...,f_m in n variables of total degree at most d. Given 0<eta<1/2,
there is a capped randomized algorithm with bit cost

    poly_{n,d}(input length + log(1/eta))

which returns a verified common F_q-zero, EMPTY, or ABORT. EMPTY is correct;
if a zero exists, the probability of ABORT is at most eta. No incorrect point
is returned. Singular, reducible, nonreduced, and zero-dimensional inputs are
included. The constants can be enormous functions of fixed n,d.

First row-reduce the input coefficient vectors over F_q. At most
binom(n+d,d) independent equations remain, with exactly the same zero set.
An inconsistent constant equation returns EMPTY; no equations returns the zero
tuple. Arithmetic in the explicit field costs poly(f) bits, and a uniform
field element uses exactly f independent fair bits.

## 2. What the retained source actually provides

Locators below are physical LF in `sources/dyadic_seed_selection/kayal_thesis.txt`,
counted with split('\n'). Chapter 6, Algorithms 1--3 and Section 6.3.6 provide:

* A decomposition into equidimensional reduced components X_i represented by
  a squarefree hypersurface g_i(t_1,...,t_r,z)=0 and inverse birational maps
  over F_q; the forward map is linear and defined on every point of X_i
  (LF4215--4244, 4303--4390).
* Constructive finite-algebra primitive-element maps, with monic minimal
  polynomial, obtained by characteristic polynomials, gcds and linear algebra
  (LF4505--4621, 4646--4689). Small characteristic is included, not excluded:
  the source explicitly repairs inseparable projection by a linear change of
  coordinates (LF3865--3876, 4519--4524).
* An exact test for an absolutely irreducible F_q-factor, using the preceding
  uniform-factor decomposition (LF2987--2999, 4132--4143, 4253--4278).
* If there is no such factor, every rational point maps into the singular
  locus. Pull back all partial derivatives and recurse on a proper closed
  subset of smaller dimension (LF4797--4825).
* Degree, component-count and arithmetic bounds independent of q, for fixed
  n,d; see LF4448--4459, Lemma6.3.6 LF4755--4786, and Theorem6.3.8
  LF4829--4832. The source's small-field branch is exhaustive and its
  threshold depends only on n,d (LF4150--4163).

Instrument this exact decision algorithm to retain the first positive chart
and its maps, instead of returning a bare TRUE. A YES propagated up a recursive
call carries that descendant chart in the original coordinates. If the source
uses its small-field branch, retain the point it finds. A negative result stays
EMPTY. Thus search does not self-reduce by enumerating q possible coordinates.

The recursion handles components not defined geometrically over F_q: Frobenius
permutes their absolute components, so a rational point lies on at least two
conjugates, hence on the squarefree hypersurface's singular locus. Each branch
strictly lowers dimension. No assertion of smoothness of the original input
is used, and no rational points on a singular exceptional set are discarded.

## 3. An inverse expression with a valid denominator

One must not infer that a particular displayed fraction is evaluable at every
smooth point merely because its rational map extends there.

Use the actual finite-algebra representation from Section6.3.4. Write
F=F_q(t_1,...,t_r). The selected primitive element alpha has minimal polynomial
g(t,z), monic of degree s in z, and 1,alpha,...,alpha^(s-1) is an F-basis.
Form its basis-change matrix in the old algebra basis. Its determinant is
nonzero. Applying its inverse to each original coordinate and clearing
coefficient denominators gives

    x_j = P_j(t,z)/Delta_j(t),       Delta_j != 0.

This is exact rational-function linear algebra of bounded size/degree.
The source's Algorithm3 explicitly uses this coefficient-field form
(LF4315--4321); the primitive-element basis and its invertibility are established
at LF4535--4583. Intersect preserves monicity (LF4362--4367).
Use these algebra elements, recomputing in the final primitive-element basis
if needed, rather than evaluating an unreduced composition containing 0/0.

Put b(t)=product_j Delta_j(t). A nonzero base-variable polynomial cannot
share a factor with a monic polynomial in z: any base-only divisor would divide
its leading coefficient 1. The same argument holds over the algebraic closure.
Consequently gcd(g,b)=1 and b is a nonzerodivisor on EVERY absolute component.
This is the required generic denominator guarantee. We exclude b=0 below;
we do not claim this one expression covers the whole smooth locus.
The identities f_i(P_1/Delta_1,...)=0 modulo g can also be checked exactly.

## 4. A quantitatively dense usable locus

Consider a positive chart of dimension r>=1. Let E>=2 bound the total degrees
of g and b, and D=deg g. These are computable from the stored expressions and
bounded by functions of fixed n,d. Let P(j) be the j-th rational prime and set

    Q(r,E)=1+max(10000*r^3*E^5*P(4*ceil(log2 E)+4)^3,
                 16*E^4, 16*r*E^3, 2*E).

If q<=Q(r,E), enumerate F_q^n in the ORIGINAL system. This is a constant-size
branch in the fixed-(n,d) theorem, even though that constant is not practical.
It needs no random trial or unproved point-existence inference.

Suppose q>Q(r,E). Kayal's quoted explicit Schmidt bounds, Theorems6.3.3--4
(LF4703--4718), give at least

    q^r - D(D-1)*q^(r-1/2) - 4*r*E^3*q^(r-1) >= q^r/2

points on g=0 that are smooth and have b!=0. Indeed one absolute F_q-factor
already supplies the first two terms. The singular locus contributes at most
2*r*D^3*q^(r-1), and g=b=0 at most 2*r*E^3*q^(r-1).
No explicit absolute factor is needed for this argument or for sampling.

Minor source correction: LF4733 says squarefree g is coprime to one partial.
That statement is false for g=xy. The correct assertion is that g and ALL its
partials have no common factor over the perfect field. This follows factor by
factor from squarefreeness, and is precisely the hypothesis of Theorem6.3.4.
Thus the displayed singular-locus bound and the search argument are unchanged.

If necessary make the entire g monic in its final variable: choose a vector v
where its highest homogeneous part is nonzero, and complete v to a linear
basis. Such v is found deterministically on a grid of D+1 distinct field
elements in each coordinate, because q>D. This grid has constant size here.
Compose both maps and b with that invertible change; total degrees are unchanged.
The transformed g has nonzero CONSTANT leading coefficient in the final
variable, which is divided out. Every projected fiber now has at most D roots.

Therefore at least 1/(2D) of uniform projected t in F_q^r have a usable root.
For each trial find ALL rational roots of the monic univariate g(t,Z), discard
singular or b=0 roots, evaluate the inverse map, and verify the original input
equations. Stop at the first verified point. With

    R=2D*ceil(log2(4/eta))

trials, failure to hit a usable fiber has probability at most eta/4.

## 5. Root finding, zero dimension, and the actual finite clock

For any fiber polynomial h of degree at most D, first compute

    h_0 = gcd(h, Z^q-Z).

Compute Z^q modulo h by f squarings, not q iterations. h_0 is squarefree and
split, and contains exactly the rational roots, including roots of a possibly
nonreduced specialized fiber. For any split factor of degree >=2 choose uniform
a in F_q and split with gcd(h_0, Tr_Fq/F2(aZ)). Compute that trace by f modular
squarings/additions. Any fixed pair of distinct roots is separated with
probability 1/2, by nondegeneracy of the finite-field trace pairing. Thus each
attempt gives a nontrivial split with probability at least 1/2. Linear factors
give their roots exactly; multiplication checks certify the result.

Cap each internal split at T=ceil(log2(4*R*D/eta)) attempts. There are fewer than
R*D split nodes, so their total ABORT probability is at most eta/4. A
zero-dimensional positive chart is handled by the same root routine with R=1;
there is at least one rational root, and its inverse base denominator is a
nonzero constant. An empty rational-root list there is exact, not probabilistic.

All successful outputs are exact and verified. Exhausted random trials return
ABORT, never EMPTY. The only EMPTY output is the exact source decision or exact
small-field exhaustion. Total failure is below eta. All random choices use
fixed finite bit strings; all loops have the caps above. With n,d fixed, E,D,
the number of charts, rational-function matrix sizes and small-q thresholds
are constants. Field arithmetic, Frobenius, input reduction, and the inherited
decision/decomposition algorithm give the asserted polynomial BIT clock.

## 6. Consequence and boundary

Given the parent's fixed-length Witt-polynomial compilation, this primitive
replaces q^81 residue-field enumeration for the unramified dyadic rank-three
cluster seed modulo 2^9. A determinant-unit constraint can be expressed by
one extra inverse variable. Fixed Witt length fixes the number and degree of
the field equations; growing f is fully charged here. This review does not
verify the Witt formulas, the cluster separation proof, or the global pipeline.
It makes no polynomial claim when the variable count or degree grows.
