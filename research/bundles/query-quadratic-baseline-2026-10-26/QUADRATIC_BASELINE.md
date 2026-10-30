# Strengthen The Classical Gate Before Counting Geometric Hits

2026-10-26. Parent deductions and exact arithmetic controls. No independent
review or native execution. This applies known endomorphism division and
primitivisation to the SAME native full-suborder/source-query input. It is
not a new algorithmic endpoint or a quantum candidate.

## Decision

The previous active-coset lemma remains valid for its specified sampler.
Its NEXT-experiment instruction was too weak: geometric successes outside
H=dO/dR can still be explained by inexpensive known classical operations.
Exclude success of the stronger gates below, not just direct beta/d division.

In the native prime-degree non-Bass family with d=q^3, the direct test has
success probability about q^-9. A prime-division test instead has exact
probability (q^2-1)/q^3, about q^-1, on the SAME uniform query distribution.
That is still exponential in log(q), not a classical polynomial solver.
Comparing geometry only with the q^-9 test would be an unfair benchmark.

More importantly, known native quadratic primitivisation can recover every
integral map commuting with the query beta. With the full-rank R available,
only factorization of the ALREADY KNOWN index d is needed for this gate;
factoring the full new discriminant of every beta is unnecessary. After a
query passes this no-growth gate, any genuinely new automorphism corner
must fail to commute with beta. Neither existence nor frequency of such
transverse corners has been proved.

## 1. Input And Classical Resources

Keep actual E, a native full-rank unital R subset O=End(E), its paid basis
evaluators, trace/multiplication data, and d=[O:R]. Apply the existing easy
unit, ramified, small-prime and Bass baselines where their hypotheses hold.
In particular d is odd after 2-saturation. This note does not declare every
remaining non-Bass order hard.

For the prime-local gate, factorization of d is supplied or explicitly
charged to BOTH competitors. No O basis or unknown geometric comparison
map is input. Given a query beta in R, each proposed division starts from
an actually evaluable map. The published native isogeny-division algorithm
must return the quotient or a certified negative; timeout/UNKNOWN is not
negative evidence. Norm prechecks, map equality, finite fields, compact
representations and compression are paid as in the existing source audit.

This is a specialization of the known method in
[Herledan Le Merdy--Wesolowski, Section5, Algorithm2 and Corollary5.3](https://arxiv.org/html/2309.11912v4#S5).
That theorem states its own discriminant-factorization and efficient-map
requirements. The full-rank intersection argument below is why our narrower
gate needs only the index primes; do not silently relax the published theorem
on arbitrary one-endomorphism input.

## 2. Even Scalar Recentering Beats Full-Index Division

For any odd integer d and beta in R, let

    t = (2^-1 Trd(beta)) mod d,  0<=t<d,
    x = (beta-[t])/d.

Test the native integrality of x. If integral and x is outside R, enlarge
the order. Outside-R testing uses exact trace coordinates, not unknown-O
coordinates. The shift is unique modulo d if beta is scalar modulo dO:
Trd(beta-[t])=0 mod d forces the displayed value of t.

Thus division succeeds exactly for beta in Z+dO, modulo dR. The d scalar
classes modulo dO are distinct because O intersect Q = Z. Each has d
preimages modulo dR. Precisely d of these d^2 queries give a quotient in R,
namely the scalar queries beta=[t] modulo dR. Hence

    useful centered queries = d(d-1),
    Pr[centered division grows R] = (d-1)/d^3.

Direct beta/d division instead has d-1 useful queries and probability
(d-1)/d^4. The centered gate is a factor d stronger and requires no
factorization. Its successful nonintegral cosets are NOT geometric leverage.
This is still only a lower baseline; do not elevate it to the strongest one.

## 3. Recover The Entire Query-Quadratic Intersection

Assume beta is nonscalar and write K=Q(beta). Compute S0=R intersect K
from the known R table by integer linear algebra. This is a quadratic order
and does not require access to O. In a unit-adapted basis (1,r2,r3,r4), if

    beta = b0 + b1*r2+b2*r3+b3*r4,
    g = gcd(b1,b2,b3)>0,
    theta = (b1/g)*r2+(b2/g)*r3+(b3/g)*r4,

then S0=Z+Z*theta. Indeed a rational multiple of the primitive integer
triple (b1/g,b2/g,b3/g) is integral in all three coordinates only when its
multiplier is an integer. The scalar coordinate is independent. theta is
constructed as an INTEGER linear combination of the original native basis,
not by assuming that division of a supplied map by g is available.

Let Smax=O intersect K. The natural map Smax/S0 -> O/R is injective, so

    [Smax:S0] divides d.

This is the critical factorization saving. All possible missing primes are
already in d, even if disc(S0) has many unrelated large prime factors.
Starting from Z[beta] instead of S0 would invalidate this argument.
For scalar beta, K=Q and O intersect Q=Z; there is nothing to saturate.

### One Odd-Prime Step

Suppose the current quadratic order is S=Z+Z*theta, theta is genuinely
native, T=Trd(theta), N=Norm(theta), and Delta=T^2-4N<0. For an odd prime
ell dividing d, an index-ell quadratic overorder exists precisely when
ell^2 divides Delta. In that case put

    r = (2^-1 T) mod ell,
    eta = (theta-[r])/ell.

Its integral polynomial invariants are

    Trd(eta) = (T-2r)/ell,
    Norm(eta) = (N-r*T+r^2)/ell^2,
    disc(Z[eta]) = Delta/ell^2.

The integrality of the norm follows from
4*(N-r*T+r^2)=(T-2r)^2-Delta. The lattice generated by 1,eta is a quadratic
order containing S with index ell. It is the UNIQUE such overorder, by
the conductor classification of quadratic orders. Therefore one actual
native division decides the step: success adjoins eta; a certified failure
proves no further native enlargement at this ell. Algebraic integer trace
and norm alone do NOT establish that eta belongs to the native O.

At each ell, repeat until failure, the discriminant obstruction, or
v_ell(d) successful steps. Primes other than ell cannot alter this local
maximality. At the cap the index injection proves that no ell-part remains.
There are at most sum_ell v_ell(d) native division calls. Their coefficients
have polynomial bit length; compact successful representations must be
retained, as in the imported division theorem. The routine ends at Smax.
One uniform original-input cost bound is still required when repeating
this gate through adaptive full-order enlargements; use the existing
normalization/compression argument, not unbounded evaluator nesting.

The local helper only constructs arithmetic proposals. It does not call
the native division algorithm or certify any proposed map as native.

## 4. Consequence For The Geometric Harvest

Run the query-quadratic gate before the expensive geometric source.
If Smax is not contained in R, the CLASSICAL gate has already found a new
native map. Adjoin it, close/normalize R, recompute d and restart with the
new order. Do not credit a later equivalent geometry output as unexplained.

If the gate makes no change, Smax is contained in R. The centralizer of
nonscalar beta in the definite quaternion algebra is exactly K. Therefore

    w_ij in O and [w_ij,beta]=0  implies  w_ij in Smax subset R.

Any new corner returned by a complete unmarked automorphism computation
must now be TRANSVERSE: it does not commute with beta. Noncommutation is
necessary, not sufficient, because R already contains many noncommuting
maps. The actual outside-R check is still mandatory.

For scalar beta the necessary commutator conclusion does not apply; all
maps commute with a scalar. Scalar queries must be recorded separately.

The earlier active-coset probability theorem applies to the UNFILTERED
uniform distribution. The quadratic no-growth filter need not be constant
within a hidden coset: K changes with beta. Its conditional distribution
cannot inherit the 1/3 bound without a new proof. Keep the original query
denominator and separately record classical successes, residual geometric
successes and unresolved/UNKNOWN calls. Do not quietly renormalize away
the rejected classical portion.

## 5. Exact Stronger Baseline On The Native Non-Bass Family

Use the existing prime-degree IsERP realization, not a new oracle problem:
source O0 is known, phi:E0->E has prime degree q, and

    R = Z+q*theta(O0),  theta(a)=phi*a*phi^dagger/q,  d=q^3.

All native maps q*theta(a) are available; theta(a) need not be integral.
In proof-only source coordinates M=M2(Z_q), the true target is the neighbor
M'=End(diag(1,q) Z_q^2) after a suitable GL2(Z_q) coordinate change. Every
uniform beta in R/dR can be written a+qX, and the noncentral residue class
of X is uniform in M2(F_q)/F_q*I.

Test the native quotient (beta-[t])/q with
t=2^-1*Trd(beta) mod q. It differs from theta(X) only by a known integral
scalar. Thus it is integral exactly when X preserves the hidden line.
It gives a map outside R exactly when X is nonscalar modulo q as well.

In coordinates X=[[b,c],[e,0]], preservation of the line e1 is e=0.
There are q^2-1 nonzero triples with e=0 among q^3 total triples. This
description is invariant under changing the hidden line. Consequently

    Pr[prime-division growth on uniform beta] = (q^2-1)/q^3.

For the same distribution compare:

    direct divide by d=q^3:   (q^3-1)/q^12,
    scalar-center, divide d: (q^3-1)/q^9,
    scalar-center, divide q: (q^2-1)/q^3.

One successful nonscalar X has at most two eigenlines modulo q. The known
source algebra therefore narrows the true neighbor to at most two, with
the remaining constant number of native tests separating them. This agrees
with the existing linear-in-q classical baseline, not a new speedup. See
[Eisentrager--Scullard v2, Theorem1.1 and Sections6-7](https://arxiv.org/html/2402.05059v2).

The p=103,q=5 supplied-order control has only the two scalar target units,
so its prime-division growth is not just recovery of a missing cheap unit.
It is nevertheless small and fully supplied, NOT a hard native instance
or a native execution. The analytic probability is proved by the residue
count, not inferred from finite timing or success data.

## 6. Self-Attack And What Remains Open

- Starting from Z[beta] without intersecting R can miss known saturation
  at primes outside d. The tests include a maximal input order with an
  imprimitive query; the intersection step must remove this artifact.
- Oddness is essential to the single-shift formula. Do not silently apply
  it at2. Existing native 2-saturation removes that index component first.
- Integral quadratic polynomial coefficients do not choose the native
  maximal quaternion order. A proposed step can pass EVERY arithmetic
  invariant yet fail native division. A wrong-center control enforces this.
- Factoring d remains charged. This gate saves factorization of additional
  query discriminants; it does not give free classical integer factoring.
- No-growth of one query field is not full-order saturation or classical
  hardness. The native hard family can have rare invariant-line hits.
- Isogeny representation may itself leak the secret; no restricted Boolean
  query lower bound substitutes for inspecting actual native input data.
- Noncommuting geometric corners are not automatically useful or novel.
  Test actual order growth and all existing baselines on the same input.
- Filtering changes the probability model. Preserve unconditional counts
  and do not reuse the old active-coset lower bound after conditioning.

NEXT: the open geometric question is useful transverse automorphisms on
queries that survive the FULL query-quadratic no-growth gate, on the native
large-prime non-Bass regime. Do not build a dimension128 backend merely to
rediscover these classical successes. A density theorem still needs an
actual native distribution and all adaptive stages. If no constructive
mechanism beyond these filters emerges, compare a genuinely different
source direction instead of indefinitely adding neighboring controls.
