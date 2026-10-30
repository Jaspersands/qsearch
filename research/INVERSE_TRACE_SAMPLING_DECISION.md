# Sampling After The Classical Search Result

30 October 2026. Four-agent follow-on; mathematical deductions and exact
controls, not a quantum speedup, general classical sampler, or hardness
theorem. The concrete algorithmic improvement from this round is recorded
separately in PIVOT_POWER_SDE.md. Do not build another inverse-trace backend
merely because full-fiber sampling remains unresolved.

## 1. Randomized Block Assembly Is Detectably Biased

Retain the original relation and every K check. A two-block construction
forces H_S*x_S=0 and H_complement*x_complement=0 separately. This is an
extra constraint beyond Hx=0, even if each block were sampled perfectly.

Let Omega be the full native fiber and pi its uniform law. For odd n>=61,
N=n^2,K=floor(N/8),a=(N-n)/2, let E be the union of these events over
ALL subsets with a<=|S|<=N-a, not just trace-affine partitions. The existing
pointwise character/MDS bound gives

```
Z_S(h)=(q/2)^|S| * q^-K * (1+epsilon_S(h)),
|epsilon_S(h)| <= eta_|S|,
eta_m=(q^K-1)*beta^(m-K+1), beta=(1+2sqrt(q))/q.
```

For a fixed balanced S,

```
pi(H_S*x_S=0)=Z_S(0)*Z_complement(0)/Z_full(0)
 <= q^-K*(1+eta_a)^2/(1-eta_N) < 2*q^-K.
```

The last step follows from beta<4/sqrt(q) and
log2(eta_a)<(-n^3+16n^2-27n+36)/16<=-N. Complementary subsets define
the same event, so a union bound over at most2^(N-1) events proves

```
pi(E)<2^(N-nK),
TV(nu,pi)>1-2^(N-nK) for EVERY law nu supported on such assemblies.
```

At n61 this is TV>1-2^-24644. Random partition selection, uniform block
samplers, reweighting and extra rejection cannot enlarge this support.
This does not cover a new algorithm that changes the output coordinates
and thereby breaks the separate zero-syndrome condition.

### A Polynomial-Time Observable

Pack the columns

```
w_i=(x_i,alpha_i*x_i,...,alpha_i^(K-1)*x_i) in F_2^(nK)
```

using the ORIGINAL field basis. The binary matrix B_x always annihilates
the all-ones vector. A proper nonempty zero-syndrome subword gives another
kernel vector, hence rank(B_x)<=N-2. Gaussian elimination tests this in
polynomial time, without enumerating subsets or solving a subset-sum oracle.
The implementation returns and verifies a full binary kernel basis.

To bound the uniform false-positive rate, separate zeros. A zero can occur
only at a zero-target coordinate, and its probability is at most
(2/q)*(1+eta_(N-1))/(1-eta_N). If every coordinate is nonzero, a vanishing
proper subword must have BOTH sides larger than K by Vandermonde rank.
Choose the smaller side, K<m<=N/2. Systematic elimination gives
Z_S(0)<=(q/2)^(m-K): sample its m-K accepted free symbols, with at most
one pivot completion. Its complement has size at least ceil(N/2), where
the Fourier bound applies. Thus, with z zero-targets,

```
Pr_pi[rank(B_x)<N-1]
 <= (2z/q)*(1+eta_(N-1))/(1-eta_N)
    +2^(N-1)*(2/q)^K*(1+eta_ceil(N/2))/(1-eta_N).       (A)
```

The exact-rational API uses ceil(sqrt(q)), includes both terms and clips
only the final probability bound at one. A failed or vacuous bound is not
evidence of hardness. Pauli independently checked the argument and code.

Actual n17 artifact ranks, on the SAME original words:

| Method | Rank | Nullity | Zero coordinates |
| --- | ---: | ---: | ---: |
| Full trace-affine genus-zero witness | 288 | 1 | 0 |
| Singleton zero-extension | 144 | 145 | 144 |
| Sparse18 two-block assembly | 287 | 2 | 0 |
| Matched flat solver, singleton | 288 | 1 | 0 |
| Matched flat solver, sparse18 | 288 | 1 | 0 |

This is an executable sampling falsifier, not a new quantum challenge.
Both matched CLASSICAL flat witnesses pass the rank test. Passing is NOT
a uniformity certificate; no native hardness or quantumness claim follows.

## 2. A New Every-Syndrome Count Enclosure

For any m distinct supplied points, K<m, targets and public h in F_q^K,
let Z(h) count accepted assignments with Hx=h, and set
g(h)=q^K*Z(h)/(q/2)^m. The following is a deduction from
[Sawin--Shusterman, 2512.24080v1, Theorem1.3 and Section4](https://arxiv.org/pdf/2512.24080v1):

```
sup_h |g(h)-1| <= E_m=24^m*q^((K+1-m)/2).              (B)
```

This is pointwise, unlike the earlier L2 completion-transfer bound.
Maxwell independently audited the full derivation and sheaf hypotheses.
It imports that theorem rather than formally proving its geometry.

With psi=(-1)^Tr and epsilon_i=(-1)^b_i, the exact local transform is
[q*delta_(t=0)+epsilon_i*(1+Kl(t))]/2, INCLUDING Kl(0)=-1. Hence

```
g(h)=q^-m sum_(deg p<K) psi(L_h(p))
     prod_i [q*delta_(p_i=0)+epsilon_i*(1+Kl(p_i))].
```

Expand delta, constant and Kloosterman terms. For a delta set T of size
t>=K, p=0; after regrouping the other choices, 1+Kl(0)=0 leaves only
the all-delta term, which is exactly1. For t<K put p=P_T*f,deg f<k=K-t.
Let ell be the number of Kloosterman terms.

If k<=ell, use k evaluations to express L_h(P_T*f) as a linear combination
of those evaluations. Absorb it into local additive twists. The normalized
sheaves q^-1/2*Kl(a*x)*psi(lambda*x), a!=0, are rank-two geometrically
irreducible middle extensions. Scaling and rank-one twisting preserve
irreducibility; infinity slopes are at most1, and finite Fourier conductor
is1. Thus B=2rank+conductor=5<=8 in the imported theorem. The whole term is
at most8^m*q^((K+1-m)/2). The zero stalk must NOT be replaced by zero.

If ell<k, evaluation onto the ell coordinates is surjective. The additive
phase either kills its kernel, or factors through it. In the latter case,

```
sum_x Kl(a*x)*psi(lambda*x) = 0                 if lambda=0,
                           = q*psi(a/lambda)    otherwise.
```

The complete sum is at mostq^k, so the normalized term is at mostq^(K-m).
This fits the same bound. There are at most3^m expansion terms. The zero
polynomial cancels within each grouped non-all-delta term, so there is no
extra subtraction error or factor2. This proves(B) for EVERY syndrome.

E_m<1 gives a certified approximate-count interval around the cheaply
computable main term and proves all these fibers nonempty. It does not
give exact counts, arbitrary requested precision, a constructive witness,
or a conditional uniform sampler. For native n17,31,61, the first surplus
m-K making this conservative bound nonvacuous is45,52,84 respectively.
It is VACUOUS at the existing residual size K+ceil(4K/n). Do not silently
replace saved residuals or upgrade those experiments' UNKNOWN statuses.

## 3. Adaptive Partial Observations Can Be Simulated Classically

A classical observer may adaptively inspect at most N-m distinct symbols
of a uniform native word, at any fixed public full syndrome. Sample each
new requested symbol uniformly from its accepted alphabet using the known
trace-hyperplane/inversion bijection; cache repeated requests. This needs
no hidden advice, conditional oracle or quantum computation.

For fixed observer coins and any transcript, its queried set and values
are fixed. Counting unobserved completions gives the EXACT likelihood ratio
of the uniform-native transcript to the independent-root transcript:

```
g_remaining(h_residual)/g_N(h_full).
```

The uniformity of(B) over subsets, bits and syndromes pays for adaptive
choices and variable stopping. If E_N<1, TV is at most

```
[max(E_m,E_N)+E_N]/[2*(1-E_N)], capped at1.             (C)
```

The maximum covers all remaining lengths since E_j is geometric in j.
There is no extra query-count factor: this is a direct transcript density
comparison, not a stepwise hybrid. At n61,m560, this simulates adaptive
observation of3161 out of3721 coordinates with TV<2^-299. Arbitrary
classical postprocessing of the seen symbols cannot increase TV.
It does NOT provide the last560 coordinates, a full-word simulator,
coherent query access, or a classical implementation of the quantum state.

## 4. Prior Art, Utility And Research Decision

Euclid checked the primary coding/filter literature. The full-list coherent
summation mechanism is already present in
[Jo, Theorem5.2 and Remark5.3](https://arxiv.org/html/2607.16541v2).
That paper's stated distribution is Sun--Wootters, not uniform native
witnesses; the local uniformity deduction uses constant filter amplitude
on the exact accepted fiber. Ordinary unique-decoding DQI alone does not
cover the chosen radius. The every-target explicit inverse-trace
specialization may still warrant novelty review; the primitive is not new.

[Chatterjee--Harsha--Kumar, Theorem1.1](https://arxiv.org/html/2511.05176v2)
also supplies deterministic complete RS list decoding over every finite
field in poly(N,log q), at agreement above the Johnson threshold. The
binary-field decoder note already uses known small-characteristic methods;
neither implementation should be presented as a new decoder.

Constrained wiretap encoding is a concrete possible use: encode message y
by a uniform accepted word with Hx=y. But without an external requirement
for THAT exact decoder, classical RS coset encoding over F_(2^(n-1)),
followed coordinatewise by the accepted-alphabet bijections, carries the
same message bits and meets all local predicates with perfect wiretap-II
secrecy against about7N/8 observed symbols. The standard classical coset
construction is described in
[Cheraghchi--Didier--Shokrollahi, Remark18 and Corollary20](https://arxiv.org/pdf/0901.2120).
This comparator CHANGES the global decoder: it is not a native sampling
dequantization, but removes that proposed application-level advantage.

Membership-only proofs of quantumness also fail once classical search is
available. Honest uniformity cannot rescue a verifier that checks only
membership. No external application requiring the exact syndrome map,
local predicates AND full joint law was established in this round.

Decision: retain the ideal sampler as a scoped mathematical result, but
deprioritize new sampler backends or larger native sweeps until a useful
reduction or constructive classical full-sampling route is specified.
The Rees pivot-power subroutine is the more actionable constructive work
identified in this round. No additional hardness candidate is manufactured
by adding a rank test that existing classical witnesses already pass.
