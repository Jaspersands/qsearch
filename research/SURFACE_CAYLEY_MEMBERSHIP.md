# A Paid Classical Membership Test From Polarized Interpolation

31 October 2026. Constructive mathematical deduction under the recovered
weak-surface input and published PPAV interpolation contract. Independent
automated mathematical review accepted the lemma with the fixed-pool
normalization and non-strict intermediate inequality corrected below.
No native geometric interpolation,
target-ring saturation, hidden-kernel recovery, or quantum execution occurred.

## Scientific Result

The restriction in `bundles/ppav-source-2026-10-23/PPAV_SOURCE_DECISION.md`
section 5 to a supplied POLARIZED source endomorphism can be removed, at
fixed additional dimension. Every supplied integral `a in End(A)`, where
`A=E^2`, has a polynomial-cost classical test for

    a K subseteq K,       K=ker(phi),

under the SAME paid weak-input/access contract below. A Cayley dilation
turns this predicate into descent of a known polarized endomorphism on
`A^2`, so the imported polarized interpolator applies. It supplies an
arbitrary-matrix membership oracle for the hidden parabolic algebra; it
does not supply that algebra's basis or a saturated target order.

Separately, in the strictly BOOLEAN membership-oracle model, even this
stronger test requires Omega(ell) classical queries to recover a uniformly
random hidden graph Lagrangian with constant probability. This scoped
query statement is proved below. It is NOT a lower bound for the native
weak-PPAV problem, which supplies geometric coordinates and other operations.

## Input And Paid Operations

Use `SURFACE_SOURCE_RECONCILIATION.md`: p>3, distinct odd prime ell,
full known evaluable source quaternion order, original modeled polarized B,
one genuine ell-polarized `phi:A->B`, and one common unit mask per complete
odd-prime source torsion basis. The full order and phi are defined over one
paid common field. All fields, compatible embeddings, torsion generation,
point/model operations, source coefficient heights and evaluator lengths
are charged. No target End/Hom lattice or geometric ell-torsion is supplied.

The lemma here assumes `ell>=11`. It does not make an unproved claim about
the same ten-choice construction at the finitely many smaller primes.

The new auxiliary primes must be covered by the genuine weak-evaluation
access contract. A fixed insufficient table of earlier markings is not
silently enlarged. Section 4 gives a single polynomially bounded prime
pool fixed before all bounded source queries, so adaptive weak queries or
coherent access to phi are unnecessary.

The prior-art primitive is Corte-Real Santos--Piasecki--Wesolowski,
ePrint 2026/1142, Theorem 7.1 / Algorithm 6, in the retained full PDF at
`/Users/jaspersands/Developer/qsearch-research-work/ppav-source-2026-10-23/2026-1142.pdf`.
It interpolates a polarized map of specified multiplier between already
modeled PPAVs, or returns failure if none matches the supplied assignments.
Here both PPAVs are the already modeled `B^2`; no repolarization is needed.

## 1. Integral Cayley Dilation Of An Arbitrary Source Map

Adjoints use the ORIGINAL product polarizations. For any integral a on A,
put, on the four-dimensional abelian variety `A^2`,

    X = p [[0,a],[-a^dagger,0]],       X^dagger=-X.

The source algebra is `M4(O)`, of reduced degree eight over Q. For
`z=0,...,9`, try

    m=1+p z,       Y=mI+X,       d=Nrd(Y).

The polynomial `m*Nrd(mI+X)` is monic of degree nine in m over F_ell.
The ten candidate m's are distinct modulo ell because ell>=11 and
ell!=p. Therefore at least one choice satisfies `ell∤m d`. Modulo p,
`Y=I`, so `d=1 mod p` for every choice. Select the first successful one.

Over a complex splitting of the definite quaternion algebra, X is
skew-Hermitian. Thus Y is invertible for positive m, and d is positive.
The reduced characteristic polynomial of Y has integral coefficients:
Y belongs to the integral order `M4(O)`. Cayley--Hamilton consequently gives

    d Y^-1 in M4(O).

Define

    U=(mI-X)(mI+X)^-1,       F=dU.

The factors are polynomials/rational functions in X and commute. From
`X^dagger=-X` one obtains `U^dagger U=I`. Hence

    F in End(A^2),       F^dagger F=[d^2].

F is a known, evaluable polarized endomorphism of multiplier d squared,
with multiplier coprime to p and ell. Its integral polynomial expression
uses source maps only. Computing a fixed-degree characteristic polynomial,
its integral adjugate, and these bounded-length compositions has polynomial
bit cost in the charged source data. It does not require evaluating a
rational inverse on geometric points.

### Why This Tests The Original Predicate

Reduce modulo ell and write `W=K direct_sum K`. Since m, d and 2 are units,

    I+U=2m(mI+X)^-1

is invertible. Stability of W under X implies stability under U. Conversely,
stability under U implies stability under `(I+U)^-1`, because its restriction
to W is invertible; using

    X=m(I-U)(I+U)^-1

then gives stability under X. Scaling by d or p does not change stability.
Finally,

    XW subseteq W
      iff aK subseteq K AND a^dagger K subseteq K
      iff aK subseteq K.

The last equivalence uses the Lagrangian promise: if a preserves K, then
for v,w in K, `<a^dagger v,w>=<v,a w>=0`; hence
`a^dagger v in K^perp=K`. This implication is not valid for an arbitrary
non-Lagrangian subspace without the extra adjoint condition.

## 2. Exact Descent Test Without Target-Order Advice

Put `Phi=phi direct_sum phi:A^2->B^2`, still ell-polarized, and define the
rational endomorphism

    gamma=Phi F Phi^-1 = Phi F Phi^dagger / ell.

The quotient universal property gives

    gamma integral iff F W subseteq W iff aK subseteq K.

Moreover `gamma^dagger gamma=[d^2]`. At every auxiliary prime r avoiding
p*ell*d, duplicate the original weak image basis across the two factors.
Its one common unit mask is unchanged. In this actual full basis of
`B^2[r]`, the predicted action of gamma is exactly the known matrix F_r;
the unknown scalar cancels. Thus the required candidate point assignments
are computed by ordinary group arithmetic, with no mask recovery or
target endomorphism coordinates.

Choose a squarefree product M of those auxiliary primes satisfying

    M>d^2,       M^2>32 ell^2 d^2.

Apply the published interpolator on the old modeled `B^2`, with multiplier
`d^2`. If gamma is integral, it returns that map. For the converse, suppose
it returns an integral polarized gamma0 matching the assignments. The
integral map

    Delta=ell*gamma0-Phi F Phi^dagger

kills `B^2[M]`, so `Delta=[M]theta` for an integral theta. In dimension four,
each summand has squared Rosati norm `8 ell^2 d^2`; therefore

    ||Delta|| <= sqrt(32) ell d < M.

A nonzero integral theta has squared Rosati norm a positive integer, so
`||theta||>=1`. The strict inequality forces theta=0 and gamma0=gamma.
Thus interpolation has no false positive for descent at the stated M.
The interpolator's own `M>d^2` threshold alone is insufficient; the older
finite-level false-positive counterexample still applies in principle.

This produces a Las Vegas classical membership test, conditional on the
imported expected-polynomial geometric primitive and recognizable success.
Its internal interpolation construction has dimension `8*4=32`. That is
a fixed but severe resource constant; it must not be hidden as a cheap
surface computation. The construction returns a represented map when
successful, but the lower bound below concerns Boolean answers ONLY.

## 3. Uniform Bit Bounds

Let `h=max(1,sum_ij Nrd(a_ij))` in the supplied quaternion coordinates.
The operator norm of a is at most sqrt(h), hence at most h. In the complex
splitting of `M4(O)`, each singular value of `mI+X` is at most `m+p h`.
Since its reduced degree is eight and `m<=1+9p`,

    1 <= d <= (1+9p+p h)^8.

All arithmetic and norm bounds therefore have polynomial bit length in
the original charged data and the coefficients of a.

For a fixed auxiliary pool covering ALL queries, first replace any supplied
a by the centered quaternion-basis lift a0 of its reduction in the public
split algebra `M4(F_ell)`. Containment of K depends only on this reduction,
so `aK subseteq K` is equivalent to `a0 K subseteq K`. Apply the Cayley
construction to a0, not to an arbitrarily large original integral lift.
This normalization is required before using the following uniform bound.
With
`B0=sum_i Nrd(b_i)` for the supplied full order basis, one uniform bound is

    h <= H=max(1,4(ell-1)^2 B0),
    d <= D=(1+9p+p H)^8.

This uses Cauchy--Schwarz in the definite norm and the known split-basis
linear system. It does not assume that the arbitrary source map is itself
polarized, a unit, or of small geometric degree in ell.

## 4. One Fixed Auxiliary Pool Suffices

Choose P as the squarefree product of successive small odd primes,
excluding p and ell, until

    P > max(D^3,6 ell D^2).

Obtain the paid weak phi data at ALL these primes once. For a particular
query, normalize to a0 as in section 3, compute d from that bounded lift,
discard the primes dividing d and put

    M=P/gcd(P,d).

Because P is squarefree, `gcd(P,d)<=d<=D`. Thus

    M>=P/D>max(D^2,6 ell D),

which implies both requirements in section 2. No factorization of d is
needed: test divisibility by the retained known primes. Primorial growth
makes log(P), the number of primes, and the largest prime polynomial in
the public bit input. All corresponding point fields and weak evaluations
remain paid, using the original scalar-Frobenius and compatible-field
contract. A larger source-evaluator input cost must be included rather
than treated as free preprocessing.

## 5. Boolean Membership Alone Does Not Recover The Algebra Cheaply

This is a separate oracle-model theorem, not a native geometric lower bound.
Let `k=F_ell`, with odd ell, and choose a symmetric two-by-two matrix T
uniformly from its three-dimensional k-vector space. Set

    K_T={(v,Tv):v in k^2}.

The unknown is T, and the oracle accepts a query
`a=[[A,B],[C,D]] in M4(k)` precisely when a preserves K_T. The answer is
equivalent to

    C+DT-TA-TBT=0.

Each entry is a polynomial of total degree at most two in the three
independent entries of T. If ALL these polynomials vanish identically,
the constant coefficient gives C=0; setting `T=tI` gives B=0 and D=A;
commutation with every symmetric T then forces A scalar. Thus scalar
queries give the same answer for every T, and every nonscalar query has
some nonzero degree-at-most-two equation. By the elementary polynomial
zero bound, its acceptance probability is at most `2/ell`.

Fix the coins of an adaptive classical algorithm making at most Q queries.
Follow its transcript on which every nonscalar query fails; scalar queries
are predetermined and carry no information. The list of queries on this
path is fixed. A union bound gives probability at most `2Q/ell` that any
informative positive answer occurs. If none occurs, the algorithm's output
is fixed and can equal at most one of the ell cubed possible T's. Hence

    Pr[recover T] <= 2Q/ell + ell^-3.

Averaging over the algorithm's coins preserves this bound. Constant success
requires Omega(ell) Boolean membership queries, exponential in log(ell).
The theorem permits arbitrary matrices as queries, so restricting them to
polarized source maps cannot improve this Boolean-only model.

This does NOT account for original B coordinates, detailed interpolator
transcripts, successful map encodings, intermediate quotients, geometric
isomorphisms, or any other native operation. It must never be cited as
classical hardness for the actual source. It identifies the precise invalid
inference: a polynomial-cost membership test does not by itself provide a
polynomial-cost basis or saturation algorithm for the hidden algebra.

## 6. Exact Controls, Falsifiers And Remaining Operation

A one-shot Sage computation using the toolbox interpreter checked 60 split
finite-field cases at ell in `{13,17,19,31,61}`, p=11. Each used an arbitrary
four-by-four a and graph Lagrangian, checked an allowed m among the ten
choices, the polarized identity for F, and equivalence of the two stability
predicates. All passed. These supplied split controls are not native geometry
or evidence of asymptotic success; the proofs above supply the quantifiers.

The exact control and the following wrong-adjoint falsifier are retained in
`classical_baselines/surface_cayley_membership.sage`. Reproduce from the repo
root with:

    /opt/anaconda3/envs/qsearch-cas/bin/sage research/classical_baselines/surface_cayley_membership.sage

The orientation countercontrol used ell=13, p=11, `a=E12`, m=1. Replacing
the lower block `-a^dagger` by `-a` gave `d=1 mod 13` but a polarization
defect of rank four. Thus an ordinary block rotation without the Rosati
adjoint does not meet the interpolator's input contract.

The exact remaining classical operation is to obtain enough nontrivial
elements of the hidden stabilizer algebra, or an equivalent geometric
certificate determining K, using information beyond Boolean descent
membership. A full evaluable target lattice is not an allowed input.
An algorithm deriving such information from native interpolator outputs,
inter-query isomorphisms, or paid ell-primary division would be a substantive
advance; merely renaming membership as saturation would not.

No mechanical backend, registry promotion, broad test suite, geometric
interpolation, saturated order, or recovered hidden kernel is claimed here.
