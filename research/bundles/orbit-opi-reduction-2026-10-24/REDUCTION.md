# The Cubic Orbit Task Reduces To Known Scalar OPI

2026-10-24. LOCAL UNREVIEWED REDUCTION. No novelty, classical separation,
practical quantum execution or uniform-output claim.

## Research Decision

The preceding capacity-receiver pass conditionally reaches perfect search
at every fixed rate R>1/2 for the existing cubic-orbit task. Before building
that receiver, ask whether the SAME task already reduces to a known quantum
algorithm. This note gives a classical randomized restriction with that
effect. It also preserves partial-satisfaction scores, so it is not limited
to perfect search. The local proof remains independently unreviewed.

The external dependency is
[Sun--Wootters, Theorem1.8](https://arxiv.org/html/2610.12357v1#S1.SS2),
with its perfect-search proof in Section6.3. It supplies a quantum OPI
algorithm for fixed rate and list density, asymptotically achieving the
double-semicircle score, and perfect satisfaction when their sum exceeds
one. Its explicit-table version is sufficient here. This is published
preprint prior art, NOT a theorem or solver implemented by this project.
Its finite thresholds and decoder/circuit costs have not been instantiated.

**Decision:** deprioritize a custom cubic capacity backend as a route to
a new quantum mechanism. A natural-problem reduction, a guarantee beyond
the transferred known OPI guarantee, or a genuinely new classical attack
would justify renewed work. This reduction alone does not supply one.

## Unchanged Native Relation

Keep p=1 mod3 prime, zeta of order3, M disjoint ordered orbits
(a_i,zeta*a_i,zeta^2*a_i), public nonzero b_i, nonsquare nu, and explicit
halfsets F_i of size h=(p-1)/2. Return ONE polynomial deg P<3K. The score is

    sum_i 1[P(zeta^2*a_i)+b_i*(P(a_i)^2-nu*P(zeta*a_i)^2) in F_i].

Nothing here changes the public halfsets, ordering, multipliers, target
score, or native verification. The native dimension is always disclosed.
The algebra also works for nu!=1, but the code deliberately retains the
original nonsquare promise. The input tables already cost O(Mp); enumerating
the field is charged and is not a polynomial-bit oracle implementation.
A reversible lookup may use an explicit table-sized circuit; no free QRAM
or succinct coherent oracle is assumed, and no lookup circuit was compiled.

## Exact Restriction And Witness Lift

Every allowed P has a unique decomposition

    P(X)=Q0(X^3)+X*Q1(X^3)+X^2*Q2(X^3),   deg Qj<K.

Fix Q1,Q2; leave Q0 unknown. Set z_i=a_i^3, t=Q0(z_i), u=Q1(z_i),
v=Q2(z_i). The original three values equal t+x0,t+y0,t+z0, where

    x0=a*u+a^2*v,
    y0=zeta*a*u+zeta^2*a^2*v,
    z0=zeta^2*a*u+zeta*a^2*v.

The original residual becomes A*t^2+B*t+C, with

    A=b*(1-nu),
    B=1+2*b*(x0-nu*y0),
    C=z0+b*(x0^2-nu*y0^2),
    beta=C-B^2/(4*A).

A is nonzero. Let L_i be the EXACT preimage of F_i under this quadratic.
If every |L_i|>=ell, retain the first ell elements in canonical order.
Solving scalar OPI for Q0 on the distinct nodes z_i and these lists lifts
by coefficient interleaving to one native P. Every passed reduced constraint
passes its original constraint. The implication is coordinatewise, so a
partial scalar score is also a lower bound for the native score. Truncation
can discard good native witnesses but can never fabricate one.

## Uniform Vertex Shifts From K-Wise Randomness

Draw all coefficients of Q1,Q2 independently uniformly from F_p. At any
set of at most K nodes, their evaluations are independent uniform pairs,
by full row rank of the evaluation Vandermonde matrix.

Put d=x0-y0, w=z0-y0. The determinant of (u,v)->(d,w) is
3*a^3*(zeta-zeta^2), which is nonzero. Thus d,w are independent uniform.
Completing the square gives

    beta=w-d/(1-nu)-b*nu*d^2/(1-nu)-1/(4*b*(1-nu)).

Conditional on d, this is a translate of uniform w. Therefore the beta_i
are uniform and K-wise independent. This is an algorithm-coin statement
for EVERY fixed native input, not a promise of random halfsets. There is
no full-independence assertion across M>K nodes. The finite census includes
a case where triple independence actually fails at K=2.

## Exact Density Second Moment

Let chi be the quadratic character, chi(0)=0. For fixed A!=0 and halfset F,

    |L_beta|=h+chi(A)*sum_(s in F) chi(s-beta).

The character autocorrelation over beta is p-1 for equal s,t and -1 for
unequal s,t. Consequently

    E |L_beta|=h,
    sum_beta (|L_beta|-h)^2=h*(p-h).

For ell<=h, a bad beta with |L_beta|<ell deviates by at least h-ell+1.
Thus there are at most

    Bbad=min(p,floor(h*(p-h)/(h-ell+1)^2))

bad vertex shifts, and every bad-event marginal is at most q=Bbad/p.
For ell/p bounded a fixed distance below1/2, Bbad is O(1).

## All Lists Good: No False Independence Shortcut

Choose an ODD j<=min(K,M). Write p_i for the actual bad-event marginals.
The inclusion-exclusion partial sum through order j is a lower bound on
Pr[no bad event]. All terms in that sum agree with independent Bernoulli
events of probabilities p_i, because the actual events are j-wise independent.
For that independent comparison model, its exact no-bad probability minus
the partial sum lies between0 and the next elementary symmetric sum e_(j+1).
It follows that

    Pr[all lists good] >= max(0,(1-q)^M-binom(M,j+1)*q^(j+1)).

When j=M the remainder is zero. Crucially, the order j+1 remainder belongs
to the INDEPENDENT COMPARISON MODEL. This argument does not require actual
(j+1)-wise independence. This is a lower Bonferroni bound, not a product
estimate masquerading as an exact probability.

For fixed gap 1/2-ell/p>0, choose a constant integer B>=Bbad for sufficiently
large M. Since 3M<=p-1 and eventually p>=2B,

    (1-q)^M >= exp(-2B/3),
    binom(M,j+1)*q^(j+1) <= (B/3)^(j+1)/(j+1)!.

Choose a sufficiently large constant odd j to make the latter less than
half the former. At EVERY fixed rate R=K/M>0, eventually K>=j. Thus each
restriction succeeds with a positive constant probability depending on
the density gap, uniformly over all native inputs. Complete independent
retries have constant-in-M expected count. This constant can be enormous
as the density gap shrinks; the result is NOT uniform in shrinking gaps.
A finite zero lower bound is inconclusive, never evidence of hardness.

## Consequence And Exact Scope

For fixed R>1/2 choose a constant rho with 1-R<rho<1/2, and ell approximately
rho*p with sufficient rounding slack. Successful restrictions are scalar
OPI instances of dimension K and length M, hence rate R. Applying the
external perfect-search theorem and lifting proves the SAME asymptotic
perfect-search region as the custom cubic capacity route, conditionally
on that external theorem and this local reduction proof.

For any other fixed R>0, choose rho<1/2 sufficiently close to1/2. The known
partial-satisfaction guarantee and coordinatewise lift transfer a score
arbitrarily close to SCL_(1/2)(R), at fixed desired error. This follows by
continuity in rho; it is not an instantiated finite guarantee for the saved
p2053 input. No uniform limit in the error tolerance is asserted.

Direction matters: native cubic -> scalar OPI is an UPPER-BOUND reduction.
It does not transfer classical hardness from scalar OPI to the cubic task.
It is also not a classical dequantization: the unresolved scalar search
step is still quantum in the cited algorithm. The simpler reduction does
not by itself refute the previous capacity theorem's algebra. It removes
the argument that reaching its rate threshold requires a new mechanism.

## Adversarial Controls And Remaining Failure Modes

- Set Q1=Q2=0 and choose each F_i as the complement of the image of
  b_i*(1-nu)*t^2+t. Every halfset has the correct size, but every reduced
  list is EMPTY. Randomization is essential to this argument. This is not
  an unsatisfiable native input or evidence against random restrictions.
- Exact field controls check native residuals, vertex uniformity and all
  size3 halfsets over F7. A full13^4 coefficient census checks pairwise
  vertex uniformity and detects failure of triple independence.
- A separate low-degree evaluation census falsifies multiplication of
  event complements as an independence shortcut and checks Bonferroni.
- Failed restrictions retain their coefficients, counts, failed indices
  and work. Exhausting a retry budget is not infeasibility. Seeded controls
  are reproducibility evidence, not independent-random-coin proofs.
- Small scalar exhaustive searches test the lift and original Horner
  verifier. These are bounded reference checks, not a scalable solver.
- Frozen author-table runs retain the original public data at n204 and
  an explicitly changed n1314. They only produce reduced OPI instances.
  There is NO large Q0 solution, native perfect witness, coherent decoder,
  circuit or empirical quantum speedup in this pass.
- A separate verifier evaluates the fixed original polynomial at all three
  original orbit points, adds each possible constant t, and replays every
  native residual. It checks ALL 684*2053 preimage bits in each large run
  and the canonical hashes without using the quadratic/vertex formula.

The main theorem can fail if the vertex formula, evaluation rank, second
moment, odd Bonferroni comparison, or claimed external theorem fails.
These are explicit proof-review targets. Moving to succinct input without
paying O(Mp), changing the orbit decomposition, letting nu=1, or shrinking
the density/rate gaps invalidates this stated complexity argument.

## Next Scientific Work, Not Another Backend

Check for a natural problem reducing TO the surviving explicit OPI family
with honest input size, solution conversion and classical baselines. A
reverse mapping from arbitrary OPI must force or account for ALL Q1,Q2;
the one-way random restriction does not do that. Do not manufacture new
purpose-built predicates merely because the known decoder handles them.

Alternatively, attack the reduced structured lists classically, preserving
the same native input. They are quadratic pullbacks of arbitrary halfsets,
not automatically power cosets, intervals or the older norm-completion
family. A timeout or a coding-theory sufficient bound becoming vacuous
does not establish hardness. Do not spend a pass on larger seed campaigns
or a generic CLI for this reduction before resolving a scientific blocker.
