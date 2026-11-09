# Local saturation: finite-quotient invariant and precision boundary

2026-11-07. CLOSED scoped mathematical review; full finite-precision
local-image algorithm remains OPEN. Read current STATE/TRAPS,
LOCAL_HALVING_SATURATION.md and the core/index reviews. No implementation,
new finite control, network or API action.

## 1. Independent selection

The local Kummer-image route remains the stronger admitted next question:
the native output is complete and finite, the iteration count is now paid,
and the following finite-quotient operation removes a specific exact
presentation requirement. Its external use is the complete wild-local
condition in growing-genus two-descent. The operation is classical; the
matched baseline remains classical Stoll descent plus classical global
class/unit arithmetic. A full quantum endpoint would reuse the already
charged global arithmetic, and is not established here.

Focused corpus been-tried checks covered local finite-precision halving
and explicit semisimple-algebra Fourier/Wedderburn transforms; baselines
checks were also run. The semisimple alternative did not supply a new
native endpoint. For a dense explicit algebra, polynomial work in its
dimension is already polynomial in the expanded input; for succinct
diagram families, the retained large-loop QFT lead is not a native
decoder or a paid source-mass theorem. The existing multiplicity-source
gate explicitly retains that distinction. The catalogue's irrelevant
keyword matches are not evidence of classical hardness or absence of
prior art. No new semisimple operation is admitted from this comparison.

## 2. Dyadic finite quotient: exact lemma

Let G be the maximal pro-2 subgroup of J(Q_2). Let L be the closed
Z_2-span of the explicit independent formal seeds from the core review.
It is open and torsion-free. Put

    E=2L,    A=G/E,    H0=L+G[2].

A is a finite abelian 2-group. The entire 2-torsion of A is known:

    A[2]=(L+G[2])/E=H0/E.

Indeed if 2q belongs to E, write 2q=2l with l in L. Then q-l belongs
to G[2]. The converse is immediate. Since L intersects G[2] trivially,
the seed presentation is exactly

    H0/E = (Z/2Z)^g plus G[2].

The usual Kummer map descends to A, because E is contained in 2G, and
its kernel is 2A. Thus A/2A has dimension g+t,
t=dim_F2 G[2]. No basis of the unknown group A is supplied.

Maintain an explicitly presented finite subgroup B of A, initially A[2].
Because A[2] is contained in B, one has B[2]=A[2] and
dim B/2B=g+t at every stage. If a nonzero h in B/2B has zero Kummer
label, take any q in A with 2q=h. Then q is not in B and

    B'=B+<q>,    [B':B]=2.

Adjoining a generator q and the single relation 2q=h gives the exact
new presentation. Any additional relation can be reduced to an old
relation or an odd coefficient of q; the latter would put q in B.
All half choices differ by A[2], already contained in B, so they give
the same subgroup. Integer Smith/Hermite operations can keep a bounded
presentation; there are only polynomially many enlargements, and the
total relation exponent bit size is bounded by log_2 |A|.

If B is proper, the multiplication-by-2 exact sequence injects
(A/B)[2] into the kernel of B/2B -> A/2A, since A[2] is already in B.
Hence the label-rank stopping test is correct. The exact number of
enlargements is

    log_2[A:H0/E]=log_2[G:H0]=kappa,

the quantity bounded polynomially in the index review. In particular
log_2 |A|=kappa+g+t is polynomial too; A need never be enumerated.

The same proof works for E=2^s L, s>=1. The initial presentation is
(Z/2^sZ)^g plus G[2], and A[2] is still contained in it. The choice
s=1 already suffices algebraically and permits the coarsest errors.

## 3. Approximate halves and perturbations

Suppose a numerical routine returns an actual point representative q
such that

    2q-h belongs to E.

Then it has returned an exact half in A. Likewise one may perturb h
to h+r for any r in E, halve that perturbed point, and retain the
resulting exact relation modulo E. One no longer needs the point
representatives themselves to satisfy 2q=h exactly or to remain a
free-plus-finite subgroup with a known exact point presentation.

This matters for a torsion kernel vector: an approximate half may have
a small non-torsion component. It can nevertheless be a perfectly
valid finite-order coset in A. The finite presentation describes the
cosets, not the possibly infinite-order representatives.

The error subgroup is essential. Merely preserving a Kummer label is
not enough. Already in G=Z_2, take L=H0=2Z_2 and h=2. The class of h
is nonzero in H0/2H0 and has trivial image in G/2G. Perturb by r=-2,
which lies in L and in 2G but not in E=2L=4Z_2. The perturbed point is
zero, whose half q=0 gives no enlargement at all. Thus perturbations
inside the initial formal subgroup must be restricted to twice that
subgroup, or to another explicitly justified subgroup of 2H.

This lemma assumes correctness of the finite-coset arithmetic; it does
not grant an exact E-membership oracle. It would suffice instead to
prove that the chosen representation and error schedule always make
the displayed residual lie in E. Arbitrary rounded Mumford coefficients
are not automatically coordinates of an actual point of J(Q_2), so
even this representative/lifting requirement must be accounted for.

## 4. Odd primes

For odd p choose an open pro-p subgroup E of J(Q_p), for example the
analysis lattice specified by the explicit formal seeds in the index
review, provided its finite-coset representation is paid. Multiplication
by 2 is an automorphism on E. Consequently

    (J(Q_p)/E)[2] = image(J(Q_p)[2]).

For the nontrivial direction, if 2q belongs to E, there is a unique
e in E with 2e=2q, and q-e belongs to J(Q_p)[2]. Start the finite
presentation with those rational 2-torsion classes and adjoin halves.
The generated quotient subgroups stay in the 2-primary part, even if
the actual representatives have nonzero pro-p components. The same
one-relation update and rank-t stopping test apply. The number of
enlargements is the already bounded kappa_odd. The proof does not
assume that E or the full quotient has been enumerated.

## 5. What this removes and the decisive next obligation

The finite-quotient formulation removes the need to preserve an actual
free/torsion point basis and to certify exact point relations after
every approximate half. It also explains exactly which perturbations
preserve saturation. It does not itself remove the numerical rank,
degree-drop or gcd branches inside a halving implementation.

A sufficient remaining interface is a polynomial-size representation
of the needed point cosets, with a proved polynomial precision schedule
for addition and exact finite Kummer labels, and a ONE-HALF routine
returning q with 2q-h in E whenever the label vanishes. The known
polynomial step cap pays a polynomial accumulation of one-bit losses
at 2, but does not pay an unbounded condition number in a birational
Mumford chart. Over Q_p the differential of [2] is intrinsically 2I;
its etaleness alone supplies neither that chart nor a native uniform
coordinate-error bound at bad reduction.

The concrete next test is therefore a chart/representation lemma for
this weaker modulo-E ONE-HALF contract. A proposed perturbation method
must show both that its shifts lie in E and that a polynomial-size,
polynomial-bit sampling or deterministic rule avoids ill-conditioned
Stoll/KM branches with a proved success probability. The existence of
generic points in an open coset is insufficient. Exact exceptional
branches may be bypassed only after this bounded conditioning/lifting
claim is established. The explicit Z_2 counterexample above rejects
any repair that controls only the Kummer label or permits arbitrary
initial-lattice perturbations.

No finite-precision halving theorem is inferred from an exact-field
linear-algebra algorithm, and no full native local or global Selmer
algorithm is promoted by this review.

## 6. Finite kernels, monic normalization and Stoll kernel shape

This addendum audits the completed Claude Howell report at
`audits/claude_runs/2026-11-07-local-precision-howell/response.md` against
Smith normal form and actual Stoll Proposition 5.1. The report's finite
kernel lemma is accepted; its normalization assertion needs two repairs.
Its generic rank-drop examples are not counterexamples to the actual
saturation input family or to a representative-selection algorithm.

### Finite-kernel statement

Let M be an integral m-by-n matrix over Z_p. Let e_* be its largest
nonzero Smith exponent, with e_*=0 if its rank is zero. Suppose a proved
bound e_*<=k<N is available. Put

    K=ker_(Q_p) M intersect Z_p^n,
    K_N=ker(M mod p^N).

Then the image of K_N modulo p^(N-k) is exactly K modulo p^(N-k).
In Smith coordinates every constrained component of K_N is divisible
by p^(N-e_i), hence vanishes modulo p^(N-k); the unconstrained
coordinates are free. Conversely every true kernel vector reduces to
a finite-kernel vector. Computing a finite Smith form and taking the
last n-r columns of the inverse column transformation gives a basis
of this reduced saturated kernel. The output columns are not asserted
to be exact kernel vectors under arbitrary lifts; they approximate
some genuine integral kernel basis at the stated precision.

The bound also makes the exact rank visible: every nonzero invariant
has valuation less than N. It cannot be certified merely from the
observed residue; a missed invariant p^N is indistinguishable from
zero. The example M=(p^k,0) versus M'=(p^k,p^N), N>k, gives kernels
(0,1) and (-p^(N-k),1), proving that the precision loss k is sharp.

For a nonzero maximal-rank minor mu the correct inequality is

    e_* <= sum_i e_i <= v_p(mu).

It does not say that an arbitrarily chosen upper bound k is at most
v_p(mu). A supplied bound on that valuation is sufficient. Denominator
clearing changes Smith exponents and the effective input precision;
the lemma applies after that scaling has been charged.

### The minimal monic augmented matrix is injective

Fix the exact squarefree Stoll data a,b,s and the degree bounds (5.2).
Let M_j impose (5.1) and w_(j+1)=...=w_g=0, and let j be the least
index with a nonzero kernel. The source proves that a solution with
w=0 is zero. Therefore the linear functional lc_j extracting w_j is
injective on ker M_j: a nonzero vector annihilated by it would have
lower-degree w. Hence dim ker M_j=1. The augmented matrix

    B_j = [ M_j ; lc_j ]

has full column rank. This conclusion concerns the minimal j, not
every truncated system.

If v is a primitive integral generator of ker M_j and
lambda=v_p(lc_j(v)), then lambda<=e_*(B_j). Indeed B_j v has all
entries zero except its last, of valuation lambda. In Smith coordinates
v remains primitive, so at least one coordinate is a unit; injectivity
ensures its corresponding Smith entry is nonzero, bounding lambda by
the largest exponent. Without injectivity this assertion is false:
B=diag(0,1), v=(1,p^lambda) has e_*(B)=0 but Bv=(0,p^lambda).
Thus one needs a bound for this augmented matrix, not just M_j.

### Absolute normalization loses twice the leading valuation

Suppose the kernel generator is known as v_hat congruent to v modulo
p^P, with P>lambda, and put a=lc_j(v), a_hat=lc_j(v_hat). Then

    v_hat/a_hat - v/a
      = (a(v_hat-v)-v(a_hat-a))/(a a_hat)

has absolute valuation at least P-2lambda in every coordinate.
The second loss is real because v is primitive while a can be
nonunit. For instance the matrices (p^lambda,-1) and
(p^lambda+p^P,-1) have primitive kernels (1,p^lambda) and
(1,p^lambda+p^P). Normalizing the second coordinate gives first
coordinates differing with valuation exactly P-2lambda. This is an
abstract normalization example, not an asserted Stoll route input.

Consequently, if e_*(M_j)<=k_M and e_*(B_j)<=k_B, a sufficient
matrix accuracy for absolute monic-vector accuracy p^b, b>=1, is

    N >= b+k_M+2k_B.

The primitive generator is then known to P=N-k_M, the valuation of
its leading coefficient is visible, and division gives the required
accuracy. Direct affine solving does not automatically improve this:
even scalar B=p^k versus p^k+p^N gives inverses differing with
valuation N-2k. A loss of only k would need additional assumptions,
such as an integral solution or an exact matrix with only RHS error.

### Exact shape of the bounded Stoll kernel

The report left this shape unresolved. It follows from (5.3) and the
degree bounds. Put n=deg a and e=deg d, d=gcd(a,f), and let t0=(u0,v0,w0)
be the minimal monic solution, with deg w0=j. Every bounded solution
annihilates the nondegenerate ternary quadratic form over Q_p(x)

    Q(u,v,w)=f1 u^2-d v^2+(-c)^n a1 w^2.

All sums of bounded solutions are bounded solutions. Polarization
therefore makes their Q_p(x)-span totally isotropic. A nondegenerate
ternary form in characteristic not 2 has maximal totally isotropic
dimension at most one. Hence every bounded triple is rationally
proportional to t0.

To pass to polynomial multiples, divide t0 by the gcd of its three
components, obtaining a primitive polynomial vector t*. Any polynomial
triple on its rational line is h t* with polynomial h, by the Bezout
identity for its coprime components. The congruences impose divisibility
conditions on h, whose intersection is a principal polynomial ideal
(h0). Since h0 divides the multiplier for t0, h0 t* is still bounded.
Minimality of deg w0 makes t0 a scalar multiple of h0 t*. Thus every
bounded solution is a polynomial multiple of t0. This does NOT say
that the entire unbounded congruence module has rank one: that module
contains common-modulus multiples in all three coordinate directions.

Finally the first two terms of Q have opposite degree parity. If
n=2m, comparison with the degree of a1 w0^2 gives

    deg v0=m+j-e,    deg u0<=m+j-g-1.

If n=2m+1, it gives

    deg u0=m+j-g,    deg v0<=m+j-e.

A zero component is interpreted as degree minus infinity; the component
whose degree is an equality cannot be zero. These bounds show that
every h with deg h<=g-j still satisfies all original degree bounds,
and w requires that inequality. Therefore, for this fixed square-root
branch s,

    ker M = t0 * Q_p[x]_(degree<=g-j),
    dim ker M_k = max(0,k-j+1),   0<=k<=g.

This proves the minimal-system injectivity used above and the entire
truncated nullity pattern. It does not bound the nonzero Smith
exponents near a change of j.

### Actual applicability remains conditional

The report's missing-conditioning obligation must include the
minimal augmented B_j, as well as the integrally normalized truncated
systems and the rank/gcd computations used to construct them. The
square-root input accuracy and subsequent gcd/CRT construction of r
also require their own bounds; repeated-factor handling cannot be
replaced silently by an exact p-adic equality oracle. A proof could
instead choose a representative in the permitted error coset and
avoid these unstable branches, but must pay that selection and its
success probability.

The kernel shape is now exact, while the uniform conditioning of the
actual saturation inputs remains unproved. A matrix family approaching
a rank-drop locus demonstrates why arbitrary rank knowledge or
etaleness is insufficient. It does not establish that this saturation
algorithm must encounter such a family, nor rule out a stable
finite-quotient halving method. The completed report is advisory with
the above accepted, repaired and still-unpaid dispositions.
