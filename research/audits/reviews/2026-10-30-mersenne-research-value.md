# Mersenne Research-Value Audit

30 October 2026. Independent bounded priority audit; no solver experiments,
code changes, Git operations, installs, outreach, or descendant agents.
Primary theorem statements checked online. Existing written constructions
are premises here, not newly verified implementations or a novelty certificate.

## Recommendation

**Shelve as a priority for a significant quantum-algorithm contribution,
after the already-running bounded classical triage.** Retain the family as
an explicit test case. Its quantum result is a legitimate characteristic-two
specialization, not an automatic prime-field corollary, but its mechanism
is published machinery. I found no credible, distinct mathematical
deliverable in the present evidence that would move it beyond that role.
This is a resource-allocation judgment, not an impossibility or hardness claim.

The absence of a compiled quantum receiver is NOT the reason: a complete
polynomial-time theoretical construction would suffice for an algorithmic
result. The missing ingredient is significance beyond the specialization.

## Exact Prior-Art Boundary

**Jo, Theorem 5.2 and Remark 5.3.** Given the prepared labeled amplitudes,
complete canonical lists, one global padding length L, and positive output
norm, uniform index projection implements exact coherent fiber sums, with
success Z_I/(L*Z_0). Its proof is the uniform-index inner product, not a
prime-field estimate. Using binary trace Fourier transforms does not create
a new projection primitive. The paper's prime-field OPI normalization and
optimization results must be distinguished from this algebraic operation.
[Primary source](https://arxiv.org/html/2607.16541v2#S5.SS2).

**Horinaga--Yamakawa, Theorem 5.1.** This theorem permits prime-power q,
log(q) polynomial in block length, a supplied normalized source, polynomial
dual lists, negligible ordinary Fourier tail, negligible coherently summed
tail, and near-unit restricted normalization. It gives inverse-polynomial
verified search success; its stated trace-distance guarantee alone is NOT
an exact conditional-uniform sampler. Section 6's stronger OPI specialization
separately requires growing characteristic. [Primary source, pp. 28-29 and
Theorem 6.1](https://arxiv.org/pdf/2607.14650v2).

The native substitution is explicit. Use their block length N, code
C=ker(H), dimension N-K, source R_b equal to the normalized product-root
state, and radius w/N, w=floor(3N/5). With a=F R_b,
h=1_[wt>w]*a and A=q^(-K/2)*sum_(d0 in D) T_d0, the existing pattern-space
bound supplies their three estimates:

```
||h||^2 = 1-tau = exp(-Omega(N)),
||A h||^2 <= (1+eta)*(1-tau),
|q^K * sum_(x in C) |R_b(x)|^2 - 1| = |lambda_b-1| <= eta.
```

Here eta<q^(-N/8), and complete decoding and clean source preparation are
already specified. Thus the generic search theorem applies at p=2.
The local exact channel calculation plus fixed padding additionally gives
the written ideal p_native=lambda_b*tau^2/8 and uniformity after native
verification. Those are useful specialization details, not a new receiver.

**Sun--Wootters, Theorem 1.8.** Its polynomial-time OPI statement is over
prime fields, with coherent list membership, fixed rate/density margins,
and perfect search when R+rho>1. Theorems 2.2-2.3 explicitly use prime-field
capacity decoding/list recovery. The oracle separation of Theorem 1.12
concerns a random oracle-list ensemble, not this succinct algebraic family.
Neither claim transfers just because q=2^n grows.
[Primary source](https://arxiv.org/html/2610.12357).

Our polynomial-intersection representation has primal rate approximately
7/8 and lists h_i*S_(b_i), with h_i fixed by the evaluation points; the
rate-1/8 code is the DUAL decoder. This is not arbitrary-list OPI. The
family-specific fiber bound genuinely avoids characteristic-two pathologies,
but proving a framework's hypotheses for one predicate is an application
unless it unlocks an independently meaningful problem or new technique.

## What The Existing Progress Does Not Supply

- [Signed Walsh evaluation](../../MERSENNE_CARRY_WALSH_DRAFT.md), polynomial
  approximate local sampling, and the signed complete-list PRE-Fourier
  sampler are already established in writing. They are not open blockers.
  The [global access note](../../MERSENNE_GLOBAL_FOURIER_ACCESS.md) correctly
  does not turn that law into native output sampling after the final Fourier
  transform. An unresolved transform is not evidence of classical hardness.
- [Completion moments](../../MERSENNE_COMPLETION_MOMENTS.md) use the existing
  MDS product inequality to obtain stronger counts, not a new quantum
  algorithm. In particular, every accepted assignment on any 6K coordinates
  extends because N=8K+1 and M>=2K+1 suffices. Consequently ordinary
  coordinate-projection gadgets on at most 6K designated coordinates cannot
  enforce equality or arithmetic beyond individual acceptance. Count pinned
  auxiliaries too. A useful reduction would need genuinely nonlocal encoding
  and witness extraction; none is supplied. The OPI restatement is not such
  a reduction.
- Near-entropy-floor average completion counts do not evaluate conditional
  masses or construct witnesses. The known quantum residual guarantee at
  M>=4K also does not become M>=2K+1 merely because existence improves.
  Stronger representation-rank obstructions, failed restricted norm families,
  or additional solver timeouts would not establish a significant algorithm.

## Parent's New Scalar Flats

The parent reports an implementable construction on the SAME predicates:
for |V|=M=2^ell<n and 0 not in a+V, solve the binary-linear equations
Tr(mu/(a+v)^d)=b, choose nonzero mu, set lambda=mu^(d^(-1) mod(q-1)),
and output (a+V)/lambda. The identity

```
f_s((a+v)/lambda) = Tr(mu/(a+v)^d)
```

checks exactly. The stated local rank-failure root bound also checks:
for each nonempty T subset V, the rational sum of (X+v)^(-d) has a
nonzero numerator of degree at most d*(|T|-1), witnessed at a pole.
Summing these degrees gives d*((M-2)*2^(M-1)+1). Dividing by q-M bounds
failure for uniform non-pole a. This is LOCAL rank, not native parity rank.

At n=17, ell=3 there are ell*N=867 binary direction variables versus
n*K=612 parity equations; at n=31, ell=4 these numbers are 3844 and 3720.
Thus full-row-rank completion is dimensionally possible on those fixtures.
Actual native parity/predicate tests are pending in the parent's implementation;
I did not execute or inspect those results. Successful runs could invalidate
the selected small benchmarks as evidence of difficulty without changing the
family. Witness construction would still not certify uniform native sampling.

The general guaranteed dimension is only ell=O(log n), while automatic
full-row-rank completion needs ell*N>=n*K, approximately ell>=n/8.
Eventually the inequality fails. This does not prove inconsistency or exclude
target-adaptive lower-rank constructions; it prevents promoting the local
method into an asymptotic solver without an additional global argument.

## Priority Decision

Do not replace the defeated local-access rationale with an unsupported
final-Fourier hardness rationale. Do not change exponent, points, or targets
to evade successful native tests. Let the existing classical agents report
their exact scope, then stop quantum receiver expansion and further barrier
cataloguing for this candidate.

I am choosing the requested SHELVE alternative, not proposing "prove
hardness" as a deliverable. No named external problem with a constructed
nonlocal reduction, or credible new algorithmic lemma beyond the published
framework, emerged from the inspected notes. Failure of the current classical
attempts would not change that assessment. Preserve the valid specialization
and the potentially useful standalone Walsh/counting mathematics, without
presenting either as evidence of a significant quantum advantage.
