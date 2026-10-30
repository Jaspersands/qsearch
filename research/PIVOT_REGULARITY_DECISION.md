# Nonzero Pivots: Valid Lemma, No New Backend Priority

30 October 2026. Conditional mathematical lemma and exact countercontrols.
Kierkegaard independently checked the regularity/moment/source argument;
Ohm compared primary literature and simpler classical alternatives. No
new regular-pivot solver, receiver, native hard problem or speedup is claimed.

## 1. Precise Regular Variant

Assume an odd prime p and original exponent 1<=e<p. Measured labels are
conditionally IID uniform in a fixed unknown finite abelian p-subgroup C
of cyclic rank a<=R. Use the paid two-pilot-layer contract already present
in SMALL_PRIME_REGULAR_SUBSET.md: compile an exact subgroup frame from a
fixed outer pilot bank, then acquire a separate fixed residue prefix and
independent suffix. Verify membership before intrinsic reduction modulo p.

Require residue-prefix rank to equal the NUMBER OF INTRINSIC CYCLIC FACTORS,
not merely to equal the rank of the observed full residue bank. Choose the
basis using only that prefix. Conditional on complete outer pilots and
a spanning prefix, suffix coordinates C0 are an IID uniform a-by-ell matrix.
Incomplete outer pilots are charged; a safely verified success does not
certify their completeness or the unobserved support rank.

Write d=gcd(e,p-1), h=(p-1)/d, H_d=(F_p^*)^d, S={0} union H_d,
Q=h+1 and beta=h/p. Sample anchored free coefficients

    x in {1} x S^(ell-1), uniformly; y=-C0*x.

Accept only if EVERY pivot coefficient lies in H_d, not just S. Set
unselected prefix coefficients to exact zero. Uniform S sampling must give
zero probability1/Q and each nonzero power the same probability. Retain
the suffix roots produced during sampling; extract at most a pivot roots.

For D=Q^(ell-1) anchored candidates, let X count accepted candidates. Then

    E[X]=D*beta^a,
    Var(X)=D*beta^a*(1-beta^a).

Distinct anchored candidates are linearly independent, giving pairwise
independent uniform images under C0. This is NOT a binomial-law assertion.
Cantelli gives, with q=beta^a,

    Pr[X<Dq/2] <= 4(1-q)/(Dq+4(1-q)) <= 4/(Dq).

On a good fixed bank, K independent trials miss with probability at most
(1-q/2)^K<=exp(-Kq/2). The inverse-density overhead relative to allowing
zero pivots is exactly((h+1)/h)^a<=2^a. The same fixed bank is reused;
classical rejections consume no new quantum source states.

## 2. Regularity And Frozen-Zero Lifting

For a reduced root z, choose b with b*(e/d)=1 mod h, and set t=z^b.
Then t^e=z^d. Handle zero separately rather than interpreting 0^0 or
inverting zero. Let B0 be the full intrinsic residue basis. Because all
its scales are nonzero and p does not divide e, its active Jacobian minor

    e*B0*diag(t_j^(e-1))

is invertible. Ordinary multivariate Hensel lifting therefore applies.
For intrinsic exponents b_j, solve the stronger equations modulo p^E,
E=max b_j, using canonical integer label representatives. At each level
correct only the active pivots. They remain units; every inactive variable
stays EXACT zero, including at e=1. Verify the final original mixed-order
ambient equations after decoding through the subgroup frame.

This invokes the existing lift in PRIME_POWER_REGULAR_SDE.md. No new
Hensel method is proposed. Source-law, dilation-invariance, pointwise
accepted-output and complete-channel precision premises are unchanged.

## 3. Two Important Implementation Traps

**Observed pivot rank is insufficient.** In a supplied full intrinsic
frame (Z/25)^2, take e2, residue-prefix columns (1,0),(0,0), and suffix
(4,5). Coefficients/scales(1,0,1) give nonzero values on every OBSERVED
pivot and solve the residue equations. Yet F(t)=(5,5) and

    J_active mod5 = [[2,3],[0,0]], rank1<2.

For every unit suffix scale s, 5*s^2 is nonzero modulo25. No legal lift
with this active suffix exists. If those displayed prefix columns were
instead used as the OUTER subgroup frame, suffix(4,5) must first fail
membership. Neither interpretation licenses a regular lift.

**The existing d=1 shortcut is not a regular policy.** For p5, e1,
field columns [1|0,1], the current deterministic witness is(0,1,0), with
zero pivot. For module columns(1),(5),(1) modulo25 it is singular and
does not cancel. Another residue witness(4,1,1) lifts to(19,1,1).
Thus a future regular variant must keep stochastic nonzero-pivot search
even when no nonlinear root extraction is needed. Current production code
correctly disclaims regularity and has NOT been modified into such a policy.

Other decisive controls:

- p3,e2,bank[1|1,2] has regular witness(1,0,1), but every anchored proposal
  yields pivot0 or2, neither in H_2={1}. Fixed-bank exhaustion is not UNSAT.
- Removing zero from the suffix alphabet leaves a SINGLE candidate when
  d=p-1, regardless of suffix length; the growing-bank moment bound is lost.
- Original e=p is outside the lift contract. Residues(1,1) for labels
  (1,p-1) modulo p^2 cannot lift: every such lifted equation remains p
  modulo p^2. Reducing the power index does not repair the zero derivative.

## 4. Conditional Uniform Schedule

One loose schedule, sufficient without optimizing constants, is

    u>=max(c,R+1,2), t=ceil(log2(u+2)),
    outer pilots P=residue prefix N=suffix ell=6*u*t,
    W=18*u*t, T=W^(c-1).

Keep c<p. There are at most T merge nodes; c1 has none. Each pilot layer
has failure at most(p^a-1)/((p-1)*p^P). Since Q>=2, beta>=1/(2u),
a<=u-1 and p>=3, the combined tree bank failure is at most

    W^(u-1) * [3^(u-1-6ut) + 4*(2u)^(u-1)/2^(6ut-1)]
      < 2^-15 + 2^-10.

For all u>=2, t>=2 and log2(W)<2t+4. The two summands' logarithms are
strictly below -u*(4t-5)-2t-5<=-15 and
-u*(3t-5)-3t-2<=-10, respectively. These are analytic inequalities, not
extrapolation from a finite sweep.

Take B=ceil(log2(64T)), K=ceil(2*(2u)^(u-1)*B), with combined bounded
root/bit failure at most2^-B per node. Search and auxiliary failures each
contribute at most1/64 across the tree, so total abort is below1/16.
Correctly accounting for zero-rank branches and complete pilots can only
reduce these conservative bounds. Work remains2^O(u log(u+2)) times
polynomial explicit-input cost; node arithmetic is SUMMED, not multiplied
into recursive source arity. Full E*log p lift precision remains paid.

This is a written conditional schedule, not an implemented planner or a
new ring HSP guarantee. In particular the class c is NOT bounded by R+1
in the original mixed-order ring.

## 5. Why We Declined Another Backend

The strongest simple comparison is not the existing p^a-state DP alone.
Its small-prime suffix has L=O(u log u), including confidence. Exhaustive
Boolean-mask enumeration uses polynomial workspace and2^L work, succeeds
on the same bank-existence event as complete DP, and keeps the same
regular reserved prefix. Total tree work is still2^O(u log u). The pivot
variant can improve finer constants/search bases when d is much smaller
than p, but it does not uniquely establish polynomial space.

More decisively, REES_STREAMING_SPACE_BOUND.md shows how the existing
all-prime FIELD solver and outer ring-to-field recursion give the same
rank-FPT time with polynomial working space. This also supports streamed
coset copies through the known one-copy transport channel. No direct
mixed-order backend is required for that stated input model.

For fixed d and growing rank, the published arbitrary-input solver of
[Ivanyos--Santha, Theorem11/Section3.3](https://arxiv.org/html/1503.09016v2#S3.SS3)
has a sufficient arity polynomial in rank, unlike rank-exponential pivot
rejection. Its applicability and bank size differ; neither bound is a
lower bound or universal dominance statement. Its existence does not
license applying the IID pivot method to biased spanning-block atoms.

Decision: preserve this lemma and the failure controls, but DO NOT build
or wire a new regular-pivot backend merely to claim workspace progress.
The meaningful unresolved target is a useful native conversion/reduction
with affordable access and no stronger-input classical attack.

## 6. Verification Scope

tests/test_pivot_regularity_boundary.py checks exact finite regular-pivot
moments, the intrinsic-rank and linear-shortcut counterexamples, frozen-
zero original-degree lifts, the anchor failure, collapsed alphabet and
characteristic guard. These are algebraic controls for the stated lemma
and existing interfaces. They do not execute the proposed source tree or
certify the full mathematical argument, IID sources or quantum advantage.
