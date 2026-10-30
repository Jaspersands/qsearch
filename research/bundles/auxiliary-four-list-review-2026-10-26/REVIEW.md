# Independent Adversarial Review: Small-Bias Four Lists

Date: 2026-10-26.

## 1. Verdict And Scope

**ACCEPT the abstract four-list lemma and its conditional native
degree-budget application at every existing dyadic level e >= 64.**
No blocking mathematical error or matcher correctness error was found.
No revision of the success constant, list exponent, or degree cutoff is
needed in the reviewed version. This is not an unconditional native solver.

| Claim | Decision | Exact scope |
| --- | --- | --- |
| Small-bias four-list success > 1/8000 after the stated cap | Accept | Independent samples at every list index, all nontrivial character biases <= 1/(4L), fixed arbitrary target |
| Shared-index second moment and all 1296 inequalities | Accept | Independently proved below without the parent's elimination routine |
| O(L poly(r)) join time and space | Accept | Default cap; latest sorted/binary-search matcher; label operations charged in bit complexity |
| Expected total search cost | Accept conditionally | Fresh attempts and the inherited charged, exact access contract |
| Four prime divisors with total degree 2e-9, e >= 64 | Accept conditionally | Worst-case r_2 <= 2g, not a measured or typical small rank |
| Preservation of Bz=s and every original coordinate nonzero | Accept as composition | The previously reviewed auxiliary reduction remains a premise; label matching is not native verification |
| Implemented native solver, matrix-only efficiency, hardness, or quantum advantage | Reject as an inference | None follows from this audit |

I read the three requested target files first, then the access and reduction
reviews. All created files, copies, and test output are confined to
`/Users/jaspersands/Developer/qsearch-research-work/auxiliary-four-list-review-2026-10-26`.
No parent files, main repository, Git state, or UI were changed; no agents
were spawned. The matrix-lift/geometry-access review, the separate ongoing
sampler-access review, and a new proof of halving are expressly excluded.

The parent supplied a sorted-matcher update during this review. I reread
the fresh files, froze them in `reviewed/`, and reran both test suites.
The earlier hash-matcher snapshot is preserved in `snapshots/` for provenance.
The final verdict concerns the sorted version identified in Section 10.

## 2. Fourier Normalization, Targets, And Different Laws

Use the probability normalization

```text
mu_hat(w) = E[(-1)^(w dot X)] = sum_x mu(x)(-1)^(w dot x),
mu(x) = 2^(-r) sum_w mu_hat(w)(-1)^(w dot x).
```

In particular mu_hat(0)=1. There is no additional 2^(-r) in the first
line. An affine binary constraint system of rank R has indicator expansion
with denominator 2^R, one term per element of its row space, and a sign
for the affine target. Dependent equations do not create extra row-space
terms. This is the normalization used by the parent.

Write r=3t+s with s in {0,1,2}, delta=1_{s>0}, and L=2^(t+delta).
For one tuple, the low coordinates impose two pair equations and the
high coordinates one four-way equation. Thus R=r+t and p_u=2^(-r-t).
The frequency vectors at the four variables have the form

```text
((alpha,gamma), (alpha,gamma), (beta,gamma), (beta,gamma)),
alpha,beta in F_2^t, gamma in F_2^(r-t).
```

Their target phase is
`(-1)^(beta dot tau_low + gamma dot tau_high)`.
Exactly `2(2^t-1)` nonzero assignments have support two, and
`2^(r+t)-2^(t+1)+1` have support four. There are no support-one or
support-three terms. Hence, even for four different laws,

```text
|p/p_u-1| <= 2(2^t-1) epsilon^2
             + (2^(r+t)-2^(t+1)+1) epsilon^4
          <= 17/256 < 1/8.
```

This uses absolute values of products, not positivity or equality of the
four Fourier transforms. Coordinates within one sampled vector need not
be independent. Its full vector frequency is charged once by epsilon,
not once for every nonzero bit.

The uniform expected tuple counts for s=0,1,2 are respectively 1,8,4,
since `L^4 p_u=2^(4delta-s)`. Thus `E Z >= 7/8` in all three residues;
there is no missing ceiling factor when r is not divisible by three.

There is also a direct check on arbitrary targets: translate every entry
of list 3 by tau. This turns both join constraints into their zero-target
versions, preserves index-sharing relationships, and preserves all Fourier
magnitudes. It proves consistency of every overlap system, including full
overlap, without assuming its affine signs are positive.

An admissible adverse-sign control at r=3 uses
`mu_1(x)=(1+chi(x)/8)/8`, `mu_2(x)=(1-chi(x)/8)/8`, where
`chi(x)=(-1)^(low_bit(x))`, and uniform laws in lists 3 and 4.
Direct rational summation gives `p=63/1024 < p_u=1/16` for every target.
This would break a positivity shortcut, but not the stated bound.

## 3. A Proof Of The Rank Inequality Without Elimination

For an overlap set H, identify variables only at shared indices of the
same list. Let v=8-|H|. Regard each low constraint as the incidence vector
of an edge. The resulting graph is the disjoint union of the blocks for
lists (1,2) and (3,4). Let c be its number of connected components.

The edge span of a connected component is its even-weight subspace:
summing edges along a path gives the vector supported at its endpoints,
and such endpoint pairs generate every even-weight vector. Therefore

```text
R_low = v-c,
D_low(A) = |A|-c_A,
```

where c_A is the number of components meeting A. Put
`k=c-c_A` and `d=rank(C_high projected onto A-complement)=R_high-D_high(A)`.
The parent's entire left side (*) becomes simply

```text
v-R_low-2R_high+D_low(A)+2D_high(A)-|A| = k-2d.
```

Use the two original high equations as rows. A variable's column is
`10` if it belongs only to tuple 1, `01` if only to tuple 2, and `11`
if shared. Within either low block the possibilities are:

| Shared indices within that block | Low components and high-column types |
| --- | --- |
| 0 | Two separate edges, one entirely type 10 and one entirely type 01 |
| 1 | One three-vertex path with types 10, 11, 01 |
| 2 | One duplicated edge, entirely type 11 |

If d=0, the complement contains no vertex, since every high column is
nonzero; hence k=0. If d=1, all complement columns have the same nonzero
type. At most one whole low component per block can consist of that
type, so k<=2. If d=2, there are at most four components in total, so
k<=4. These cases prove `k<=2d` for every H and A.

This proves all 1296 inequalities, for all ranks, independently of the
parent's certificate or any nonuniform-moment fixtures. Equality occurs
at A equal to all vertices, explaining the maximum zero for every H.
The independent finite control also enumerates row spans as sets using
symmetric differences, not Gaussian elimination, and obtains all the
parent's rank patterns and maxima.

## 4. Exact Support Versus Confined Support

Let `n_H(A)` count combined Fourier assignments with EXACT variable
support A. Kernel dimension gives the exact confined-support count

```text
q_H(A) = #{assignments supported inside A}
       = 2^(t D_low(A)+(r-t)D_high(A)).
```

An exact-support assignment contributes at most `epsilon^|A|` in absolute
value, by independence of the v distinct sample variables. Therefore the
joint event probability is at most

```text
2^(-t R_low-(r-t)R_high) sum_A n_H(A) epsilon^|A|
<= 2^(-t R_low-(r-t)R_high) sum_A q_H(A) epsilon^|A|.
```

This inequality is valid term by term because `n_H(A)<=q_H(A)`. It does
NOT claim that an assignment with smaller actual support is bounded by
`epsilon^|A|` for an arbitrary larger A. Each assignment is already paid
for in its own exact-support term; replacing that term's count only adds
nonnegative slack. The apparent support-overcount objection does not
break this proof.

For fixed H the ordered index-pair count is exactly
`L^4(L-1)^(4-|H|)`, at most `L^v`. Equal values drawn at different indices
are still independent variables. Equal values must not be used to merge
columns in this calculation.

Substitute epsilon<=1/(4L). For each H,A the coefficient of t in the
exponent is exactly (*), now proved nonpositive. The remaining factor is

```text
2^(delta(v-|A|)+s(D_high-R_high)) 4^(-|A|)
<= 2^v 8^(-|A|).
```

Summing over supports and overlaps consequently gives

```text
E Z^2 <= sum_H (9/4)^(8-|H|) = (117/16)^4,
Pr(Z>0) >= (E Z)^2 / E Z^2
         >= 50176/187388721 > 1/4000.
```

The second inequality follows directly from Cauchy-Schwarz applied to
`Z 1_{Z>0}`. No independent-tuple, Poisson, or uniform-class assumption
has entered. The support argument also tolerates different laws at each
independent index, if each satisfies the same bias bound, although the
stated application only needs one law per list.

## 5. Cap, Sorted Matcher, And Las Vegas Accounting

Let M be the total number of eligible pairs in both complete filtered
joins, including duplicates, whether or not the algorithm stops early.
Pairwise Fourier inversion gives the slightly sharper bound

```text
E M <= 2 L^2 2^(-t) (1+(2^t-1)/(16L^2))
    = 2^(1+delta)L + (1-2^(-t))/8
    < 5L.
```

Thus `Pr(M>40000L)<1/8000`. On the event `Z>0` and `M<=40000L`, the
matcher must find a witness before an abort. No independence between
success and overflow is necessary. Subtracting the overflow bound gives

```text
Pr(success before cap) > 50176/187388721 - 1/8000
                      = 214019279/1499109768000
                      > 1/8000.
```

The displayed exact lower bound corresponds to fewer than 7005 attempts
in expectation; the parent's simpler bound of fewer than 8000 is valid.
An early success may occur even when M exceeds the cap, which only helps.

The sorted implementation now retains every left pair up to the cap,
sorts `(full_xor,i,j)`, and searches its keys for each eligible right pair.
It stores at most 40000L left triples; retaining duplicates is safe.
The low-key binary searches enumerate exactly the eligible pairs, and the
full-key search returns an actual stored pair. There is no disjointness
restriction that could make one representative of a full XOR insufficient.

Sorting and binary searches cost `O(L log L)` comparisons up to the fixed
cap multiplier. Keys and indices have O(r) bits and log L=O(r), giving
`O(L poly(r))` bit cost and `O(L r)` label/index storage per attempt.
No hash-table worst-case assumption is now needed. The counter reports
cap+1 when it detects overflow, but it aborts before storing or processing
that pair further. This extra constant inspection does not violate the
resource bound. A custom smaller cap is not covered by the 1/8000 theorem.

**Cost boundary, not a new sampler audit:** the cap bounds join work and
stored lists, not the running time or workspace of a prime sampler or an
arbitrary geometric backend. Preserve the inherited per-call expected
polynomial cost and bounded-representation/workspace premises. In
particular, read an O(L poly) native attempt cost as expected when its
primitive calls are Las Vegas, not as a hard wall-clock bound.

Writing P_i for the charged expected prime-generation, representation and
label cost at degree n_i, the accounting is

```text
E T <= T_pre + (L sum_i P_i + O(L poly(r_2)))/p_* + T_finish,
p_* = 1/8000,
```

where T_finish retains halving, moving, RR/evaluation/residue work, the
common-basis solve, and native verification. Storage also retains the
primitive workspace and stored divisor representations. This is the
claimed exponential bound only when those recurring costs and sizes are
polynomial in the advertised parameters.

Success and cost within an attempt need not be independent. With fresh
attempts, reaching attempt j is independent of that attempt's random
work, so summing `E[1_{reach j} cost_j]` gives the expected attempt cost
divided by its success probability. Independent restart tails also prove
almost-sure termination. Exact output checks make the search Las Vegas;
a capped failure is UNKNOWN, not an infeasibility certificate.

## 6. Native Degree Budget And Composition

Accepting the supplied prime-character estimate and access contract, put

```text
g=5e+1, a=2e-9, n=e/2-3,
(n_1,n_2,n_3,n_4)=(n,n+1,n+1,n+1).
```

These are positive integers for the range in question and sum to a.
They are degrees of prime divisors; the integers themselves need not be
prime. The four laws are allowed to differ, as they do here.

Squaring the desired bias cutoff gives exactly

```text
2 C_n q^(-n/2) <= 1/(4L)
iff q^n >= 64 C_n^2 L^2.
```

It also implies `q^(n/2)>=8 C_n L>=2 C_n`, so the premise used to derive
the bias estimate and nonempty prime sets is satisfied. I did not replace
this estimate by uniformity of prime classes or by empirical list balance.

At e=64, worst rank is 642, L=2^214, and the degrees are (29,30,30,30).
The integer part of the weakest ratio is independently verified as

```text
floor(100003^29 / (64*(322*35)^2*2^428)) = 1776281.
```

For all even e>=64, define the weakest worst-rank ratio R(e). Its constant
is `C(e)=(5e+2)(e/2+3)`, with

```text
C(e+2)/C(e) = ((5e+12)/(5e+2))*((e+8)/(e+6)) < 2.
```

The ceiling `ceil((10e+2)/3)` increases by at most seven. Consequently
`R(e+2)/R(e)>100003/(4*2^14)=100003/65536>1`. The initial exact check
therefore proves the entire even range, not merely tested tower levels.
At fixed e, increasing n by one increases the ratio by
`100003*((n+6)/(n+7))^2>1`, so the other three degrees are easier.
All existing dyadic levels e>=64 are covered. The criterion fails at
e=8,16,32 at worst rank; this is not a failure theorem for those instances.

Small actual ranks r_2<=2 cause no mathematical gap in the headline bound,
although the control functions intentionally reject them. Draw one prime
of each of the four degrees and test their total label without a filter.
For N=2^r_2<=4 and epsilon<=1/4, ordinary fourfold Fourier inversion gives
success at least `(1-(N-1)epsilon^4)/N >= 253/1024`. This is a constant
expected-cost branch. For r_2=0 the label condition is automatic.

For a successful match set `A=P_1+P_2+P_3+P_4`. Repeated primes are
permitted in an effective divisor, and

```text
[A-aO] = sum_i [P_i-n_i O] = tau in J(F_q)/2J(F_q).
```

Thus `[C-A-2dO]` is a rational degree-zero class in 2J(F_q), exactly the
input promised to the existing halving reduction. At e>=64 all n_i>1,
so these primes also cannot be any rational evaluation place in D.
Nothing here supplies a half, an RR basis, or a residue vector for free.

Under the previously reviewed downstream reduction this yields a witness
to the SAME original relation `Bz=s`, with `z_i!=0` at all m original
coordinates, for every syndrome s. There is no puncturing, altered target,
typical-G restriction, or substitution of a class-label witness for z.
I checked this interface, not a new proof or implementation of that
downstream algebra. Final verification against B remains charged.

## 7. Counterexample Attempts And Remaining Boundaries

The audited proof survives adverse Fourier signs, unequal laws, all three
rank residues, duplicate values, every shared-index pattern, target shifts,
and heavy eligible-pair counts. No counterexample within its hypotheses
was found. These are proof conclusions; finite tests below are controls.

There is a simple counterexample to weakening independence to unbiased
marginals: at r=12 let each list repeat one independent uniform vector
sixteen times. Every entry has zero nontrivial bias and the four lists are
independent, but entries within a list are not. Success is then only
`2^(-r-floor(r/3))=1/65536 < 1/8000`, without cap interference.
The parent explicitly requires the missing within-list independence.

Reusing the same failed lists for retries also does not get the fresh
attempt guarantee. An empirical Fourier check on a short list does not
certify a sampler's underlying law. Unverified labels invalidate the
native composition even if the binary matcher is correct. These are
boundaries already respected by the conditional statement, not discovered
counterexamples to it.

The only presentation clarification worth retaining is the expected
primitive-cost qualification in Section 5. There is no remaining
hash-runtime objection after the sorted update. No claims about the
separate sampler-access follow-on are made here.

## 8. Independent Controls And Results

The independent script is
[audit_controls.py](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-four-list-review-2026-10-26/audit_controls.py),
with exact integer/rational output in
[controls.json](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-four-list-review-2026-10-26/controls.json).
It does not call the parent's rank, overlap-certificate, or moment routines.
Only implementation comparisons import the frozen matcher.

| Independent control | Result |
| --- | --- |
| Explicit row-span enumeration and component identity | All 1296 H,A cases pass; maximum exponent zero for each H |
| Direct truth-table Walsh transforms for low/high affine systems | All 5184 coefficients match their exact signed row-space formula |
| Exact-support histograms, ranks 3 through 18 | All 20736 confined-support identities pass |
| Absolute-value second-moment envelopes using exact support counts | All below (117/16)^4; no distribution-independence approximation |
| Opposite-sign character-tilted laws at r=3 | Direct first moment 63/1024 for all eight targets |
| First-moment and pair-count constants | Exact rational checks for ranks 3 through 300, covering every residue |
| Sorted matcher versus exhaustive filtered search | 7104 target/fixture comparisons at ranks 3 through 11; 5506 matches, all valid |
| Duplicate-count cap boundary | Four identical length-two lists abort at cap 4 with count 5; succeed at cap 5 with count 5 |
| Worst-rank degree checks | Fail sufficient test at e=8,16,32; pass at 64,128,256,512,1024 |

The exact-support envelope calculations are combinatorial upper bounds,
not exact nonuniform moments and not claims that every chosen coefficient
sign pattern is realizable by a probability law. The all-r proof is in
Sections 2-5; the all-level degree proof is in Section 6.

Separately, **36 parent tests passed on the refreshed sorted snapshot**.
These include the parent's new `mixture_joint_probability` and
`exact_mixture_moments` controls. Their conditioned uniform/atom branch
calculation is consistent with their intended fixtures, but the review's
general proof and independent certificates do not rely on those routines.
No native prime samples, Jacobian labels, auxiliary divisors, or Bz=s
witnesses were constructed. In particular 2^214 entries were not allocated.

Reproduction, from this review directory:

```sh
python3 -B audit_controls.py > controls.json
env PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -B -m pytest -q -p no:cacheprovider reviewed/test_four_list.py
```

## 9. Borrowed Claims And Sources

The generalized-birthday mechanism is established prior work;
[Wagner's author page](https://people.eecs.berkeley.edu/~daw/papers/genbday.html)
also directs readers to Camion and Patarin's antecedents. This review
makes no originality assertion and imports no uniform-input birthday
theorem as a substitute for the small-bias proof.

The named geometric algorithms have explicit representation hypotheses;
see [Bruin, Computing in Picard groups of projective curves over finite
fields](https://arxiv.org/html/1003.2563). Their operational access contract
is taken from the supplied construction review, not newly established
here. The prime-character estimate and downstream auxiliary-code theorem
are inherited from the two supplied reviews. This audit changes neither
their provenance nor their unresolved access obligations.

## 10. Frozen Inputs And Integrity

The following are SHA-256 hashes of the actual refreshed files tested and
reviewed, not a claim that a concurrently edited parent will remain unchanged:

```text
reviewed/FOUR_LIST.md
de33dec9d652b3fda754e16f4445dcae29b6b78d926a186cfaab1f68f593b5fd
reviewed/four_list.py
633e087113c58b6057217b33910f7e5f79d58eba6581dfe584616977db59d9bb
reviewed/test_four_list.py
93db683d97f6566f398edda512706124024229c863e9920b695621b84a722142
snapshots/ACCESS_REVIEW.md
5bd6a59b7d99c6d3db8bfd9814f419d1f6d3a2b0aa477ed5628aa7073807882b
snapshots/REDUCTION_REVIEW.md
cf78bdd6b8aaa4f13548ce990a29a7c6a90d76b0f0afb49c88611d0535629a5c
audit_controls.py
25e41caf7d1834b5992ca51be42c9b693a6400a1c5ef860685d5e9d4c5952930
controls.json
60e6e9ffdf8d6e5a22a3b72dd292947b84cad8fdd96e2bc828ce58f80b8b2c51
```

Original target directory:
`/Users/jaspersands/Developer/qsearch-research-work/auxiliary-four-list-2026-10-26`.
The earlier hash-matcher snapshot hashes were respectively
`037db970f8d8bca1e0a9429b4cbbf0001ab3bccf8126862e2af4302e1385323b`,
`56223a365e9aee3da03bd0913386e91a832397faefb6c633d006710e039e7f52`, and
`ea3206b94a58c3e38c29109117b0f3ec5877c766e5834f12776fb0b6aacc77e0`.

**Bottom line:** the 1/3 exponent improvement survives this adversarial
audit under the stated access contract. It is a conditional classical
constructor with explicit exponential list length, not an implemented
native attack, a uniform polynomial-time result, or a hardness conclusion.
