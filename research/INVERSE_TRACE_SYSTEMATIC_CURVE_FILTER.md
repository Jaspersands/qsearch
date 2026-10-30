# Systematic Artin-Schreier Curves: A Sampling Filter

29 October 2026. Local constructive/adversarial deduction with exact finite
controls. Independently reviewed by Kierkegaard (automated review), with the
requested stopping-rule wording correction incorporated. This is not human
peer review, formal verification, or a novelty claim. It rejects one explicit
proposal distribution, not general classical sampling, search, or a quantum
advantage. No production sampler, module, registry entry, or UI is proposed.

## 1. Fixed Input And Proposal

Keep the supplied polynomial-basis field F_q, q=2^n, distinct supplied
alpha_i, target bits b_i, and H[j,i]=alpha_i^j for 0<=j<K. Define

    A_i = {x : Tr(inv0(x))=b_i},  B_i = {y : Tr(y)=b_i},
    a = q/2,  Omega = {x : Hx=s, x_i in A_i for every i}.

The native syndrome is s=0. The identities below also hold for any fixed s,
1<=K<N<=q, and either parity of n. Every inverse is totalized by inv0(0)=0.
Assume Omega is nonempty whenever its uniform distribution is discussed.

Fix K pivot positions I and let J be their complement, r=N-K. The MDS
property makes H_I invertible. This is the same systematic elimination used
by [inverse_trace_smt.py](../theorems/inverse_trace_smt.py), not a replacement
of the input points or code. Choose slopes sigma_j in F_q and offsets c_j,
then for t in F_q set

    AS(z) = z^2+z,
    y_j(t) = c_j + AS(sigma_j*t),                  j in J,
    x_j(t) = inv0(y_j(t)),
    x_I(t) = H_I^(-1) * (s-H_J*x_J(t)).

Draw the offsets independently and uniformly from their B_j. Since
Tr(AS(z))=0, every free-coordinate predicate holds for every parameter.
Every parity equation holds by elimination. Only the K pivot predicates
remain. Legal zero coordinates are included, not discarded as poles.

This is a globally correlated curve, not independent small coordinate
menus: a nonzero sigma_j makes y_j(t) cover its entire trace hyperplane.
It also differs from the earlier affine-AS formal-identity filter: parity
here holds by systematic elimination, and the pivot reciprocals are not
assumed to have affine AS parametrizations.

## 2. Exact Source Contract

Slopes need not be random, nonzero, distinct, or full rank. The proof holds
for EVERY fixed slope vector. It consequently permits any distribution on
slopes, and slopes chosen adaptively from the public input and previous
trials, subject to this conditional law at each new raw proposal:

    Law(c | complete prior history, current slopes)
        = product_(j in J) Uniform(B_j).                    (1)

Fresh independent offsets after choosing the slopes satisfy (1). So does
applying, for each fixed history and slope vector, a bijection of the
product of trace hyperplanes to a fresh uniform vector. Mere chronological
dependence on slopes is not forbidden; changing the conditional law is.

Marginally uniform offsets alone DO NOT suffice. Choosing offsets to force
a favorable output, choosing slopes after inspecting offsets, retaining only
productive offsets, or anchoring an offset at a known witness generally
violates (1). Such sources require their own paid construction and output-law
proof. Screening cannot erase the cost of discarded raw proposals. Past
outputs may inform the next slopes, but the next offsets must still obey
(1) conditional on that entire history.

An explicit countercontrol appears below: with independent uniform slopes,
offsets can be individually independent and uniform MARGINALLY yet force a
known native word at t=1 on every curve. This violates (1), not the theorem.
The known word is used only to test the necessity of the source contract;
no witness initializer is supplied to the proposed sampler.

## 3. Incidence Proof And Productivity Bound

Put p=|Omega|/a^r. For any fixed slopes and fixed t, translation by
AS(sigma_j*t) preserves Uniform(B_j). The total inverse bijects B_j with
A_j. Therefore x_J(t) is exactly a uniform accepted information assignment.
Every native word has a unique such assignment and unique pivot completion:

    Pr_c[x(t)=x] = a^(-r)                 for every x in Omega,
    Pr_c[x(t) in Omega] = p.

Let Z(c,sigma) count VALID PARAMETER VALUES, including different parameters
which produce the same word. Linearity of expectation gives the exact identity

    E_c Z = q*p,
    Pr_c[Z>0] <= min(1,q*p).                              (2)

Neither parameter independence nor an efficient curve solver is assumed.
The bound even grants complete parameter enumeration and perfect recognition
of productive curves for free. Increasing the complexity of parameter
selection inside an already drawn curve cannot make an empty curve productive.

For the native family N=n^2, K=floor(N/8), the existing pointwise fiber
certificate gives

    |Omega| = (1+e)*q^(N-K)/2^N,  |e|<=eta,
    p = (1+e)*2^(-K),
    Pr[productive curve] <= min(1,(1+eta)*2^(n-K)).          (3)

The exact identities preceding (3) do not require a small eta. The imported
count is the same Kloosterman/MDS estimate recorded in
[INVERSE_TRACE_NORM_ATTACK.md](INVERSE_TRACE_NORM_ATTACK.md) and implemented
by reciprocal_bound in
[inverse_trace_gibbs_target.py](../theorems/inverse_trace_gibbs_target.py).
Its character-sum input is not reproved here. A directly reproducible bound is

    beta = min(1,(1+2*ceil(sqrt(q)))/q),
    eta = min((q^K-1)*beta^(N-K+1),
              q^K*(beta+(1-beta)/q)^N).

Exact rational evaluation gives:

| n | N | K | Certified eta upper bound | Productivity upper bound |
| --- | --- | --- | --- | --- |
| 17 | 289 | 36 | 2^-1553 | (1+2^-1553)*2^-19 |
| 31 | 961 | 120 | 2^-10214 | (1+2^-10214)*2^-89 |
| 61 | 3721 | 465 | 2^-81404 | (1+2^-81404)*2^-404 |

These bounds are uniform in the supplied points, targets, and syndrome.
They are certificate evaluations, not native-size sampler executions.

## 4. Unconditional ABORT Law

Consider at most L raw curves obeying (1), with adaptive slopes permitted.
The algorithm may choose any verified native word appearing on those curves;
if it finds none it outputs ABORT. It has no separate fallback source of
witnesses. Applying (2) conditional on the prior history and taking a union
bound gives

    Pr[non-ABORT] <= min(1,L*q*p),
    TV(Law(output), Uniform(Omega))
        >= Pr[ABORT] >= max(0,1-L*q*p).                    (4)

The comparison space is Omega union {ABORT}; the target assigns ABORT zero
mass. Additional solver failures can only reduce success. Verification and
clock exhaustion must not be suppressed by reporting only successful runs.

For native parameters, polynomially many curves therefore give unconditional
TV at least 1-2^(-Omega(n^2)). This is a first-hit/proposal bound for this
explicit source, not an inference from worst-start mixing. It does NOT
bound conditional-on-success TV: conditioning can remove all abort mass,
but its acquisition cost remains. For independent repeated raw proposals,
the expected number before productivity is at least 1/(q*p), or infinite
if their actual productivity is zero.

## 5. Naive Selection And An Exact Correction

Let D_x(c,sigma) be the number of parameter values producing a particular
native x. Choosing a uniform valid parameter on each nonempty curve has
unconditional mass E[1_(Z>0)*D_x/Z] at x. Equal expected incidence
E D_x=q/a^r does not make these inverse-count weights equal. The GF8 control
below gives a nonzero conditional TV, despite nearly all curves being
productive in that small instance.

One explicit exact correction is:

1. Draw a raw curve according to (1) and compute its exact Z.
2. Accept with probability Z/q; otherwise output ABORT.
3. On acceptance, choose uniformly among the Z valid PARAMETER VALUES,
   evaluate the word, and independently verify the native relation.

This grants exact counting and uniform parameter selection only to derive
the law; their computational cost is not assumed polynomial. Repeated
parameter preimages are retained. For every x in Omega,

    Pr[out=x] = E[(Z/q)*(D_x/Z)] = E[D_x]/q = a^(-r),
    Pr[success] = p.

Thus, writing U for Uniform(Omega), the ideal one-trial law is EXACTLY

    p*U + (1-p)*delta_ABORT.                               (5)

Conditional output is exactly uniform, while unconditional TV is 1-p.
Repeat until the first success or L completed corrected trials, returning
ABORT only if all L trials fail. This stopping rule gives

    [1-(1-p)^L]*U + (1-p)^L*delta_ABORT,
    TV = (1-p)^L.                                         (6)

Equation (6) also permits adaptive slopes: (1) makes the per-word mass and
success probability the same after every unsuccessful history. It assumes
exact completed trials, fresh correction/selection coins, and a fixed input.
An arbitrary policy running at most L trials, possibly aborting earlier,
need not have the exact law (6).
Nor does (6) assert that selective backend timeouts preserve conditional
uniformity. If a whole-run clock interrupts the ideal execution with
probability at most delta, coupling gives actual unconditional TV at most
min(1,(1-p)^L+delta); the interrupted conditional output may be biased.

The correction is not claimed optimal. It simply recovers the exact accepted
Prange success p=(1+e)*2^-K, with additional curve-processing work. Even a
better correction cannot exceed the raw productivity bound (2) per trial.

## 6. Several Field Parameters And Cost

For d>=1 and t in F_q^d, fix an arbitrary slope matrix and replace the free
coordinates by

    y_j(t) = c_j + sum_(ell=1)^d AS(sigma[j,ell]*t_ell).

Every summand has trace zero. For every fixed parameter vector the same
uniform-information-assignment argument applies. With M=q^d,

    E Z = M*p,  Pr[Z>0] <= min(1,M*p),
    TV_after_at_most_L_raw_patches >= max(0,1-L*M*p).

Count parameters, not distinct image words. Zero or dependent slope columns
can cause repetitions and only make the productivity envelope less sharp.
Accepting with probability Z/M followed by uniform valid-parameter selection
again gives (5)-(6), with success p independent of d.

In the native family, inverse-polynomial raw productivity requires

    n*d >= K-O(log n).

For polynomially many patches the same necessary threshold holds, after
absorbing their number into O(log n). Thus constant or O(log n) field
dimension fails asymptotically; d must be Omega(n). This is NECESSARY, not
sufficient. No hardness assertion is made for the surviving d=Theta(n)
regime, and q^d expected incidence need not be a polynomial-size root list.

Conservative preprocessing costs O(K^3+K^2*r) field operations for inversion
and systematic coefficients. Uniform trace-hyperplane offsets use r*(n-1)
unbiased bits after a paid trace-basis computation. Random slopes, if used,
cost r*d*n bits; fixed slopes need no randomness. Per parameter, direct
evaluation and complete native verification cost O(r*d+N*K+N*n) field
operations with elementary inversion/trace arithmetic, hence polynomial
bit work in n,N,d.

Exhausting parameters costs M such evaluations. For independent full scans,
M/Pr[productive] >= 1/p, so this scan-based method does not improve the
Prange candidate-evaluation exponent. A polynomial complete-curve solver is
not supplied: systematic pivot elimination leaves reciprocal-trace
conditions, not merely low-degree polynomial root finding. Even granting
such a solver free, d=1 still needs at least 2^(K-n)/(1+eta) expected raw
proposals. The missing inverse-polynomial-productivity lemma for this source
is therefore FALSE, independently of the missing solver lemma.

A successful replacement must instead solve genuinely high-dimensional
patches, or construct solution-enriched patches with a paid source and an
explicit output law. Near-flat fiber counts alone supply neither. This
note does not replace the unresolved conditional sampler in
[INVERSE_TRACE_COMPLETION_TRANSFER.md](INVERSE_TRACE_COMPLETION_TRANSFER.md)
or the complete-cell primitive in
[INVERSE_TRACE_HASH_HEATBATH.md](INVERSE_TRACE_HASH_HEATBATH.md).

## 7. Exact Finite Controls And Reproduction

The main fixture uses F8=F2[z]/(z^3+z+1), with integer labels encoding
polynomial-basis coefficients, points (0,1,2,3,4,5), K=2, targets
(1,1,1,1,1,1), and syndrome (0,0). Pivots are positions (0,1); free
positions are (2,3,4,5). The slopes on those free positions are FIXED at
(1,2,3,4), not averaged over random slopes. Offsets are independent uniform
draws from B_1={1,3,5,7}; all 4^4=256 offset vectors are exhausted.

There are 68 native-relation words. The valid-parameter-count histogram is

    Z:                 0   1   2   3   4   5   6
    offset vectors:    8  88  80  48  16   8   8.

Every word has exactly eight incidences across these offsets and parameters.
E Z=17/8=q*p. Naive productive-curve selection has success 31/32 and
conditional TV 467/2108. The correction has success p=17/64 and conditional
TV zero. Its unconditional TV is 47/64, not zero.

A second all-one fixture uses points (0,1,2,3,4,5,6,7), K=4, syndrome zero,
the first four positions as pivots, and the same fixed four slopes. Its
fiber has four words and histogram {0:224,1:32}. Naive conditional output
is exactly uniform but abort probability is 7/8. This is a direct control
against confusing conditional and unconditional uniformity.

On that SAME second fixture, a separate deliberately invalid-source control
draws each slope independently uniformly from F8 and sets

    c_j = 1 + AS(sigma_j).

The offsets are marginally independent Uniform(B_1), but are deterministic
given the slopes. At t=1 every free reciprocal is 1, and the full word is
(1,1,1,1,1,1,1,1), which satisfies the original four checks. Every curve is
productive, exceeding q*p=1/8 because source contract (1) is violated.
All 8^4 slope vectors are exhausted; no distributional inference is based
on a seed. The word is an explicit premise counterexample, not a supplied
initializer for the proposed algorithm.

These are exact instances of the SAME inverse-trace/Vandermonde relation,
not arbitrary Boolean predicates. They are NOT the native asymptotic
parameter family N=n^2, K=floor(N/8): at n=3 that length would be 9>q.
The native-size table above evaluates a uniform theorem bound only. No
native-size curve sampler is executed. The command also checks legal zeros
on an all-zero six-coordinate fixture and a two-parameter repeated-column
patch, without changing the inputs of either all-one comparison.

Run this self-contained, standard-library-only control from any directory.
It writes no files, imports no repository code, and needs no installation.
Its exhaustive finite loops are calibration only, not scalable algorithms.

```sh
python3 -B - <<'PY'
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import isqrt

q = 8
def mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & q:
            a ^= 0b1011
    return out

def power(a, k):
    out = 1
    while k:
        if k & 1:
            out = mul(out, a)
        a = mul(a, a)
        k >>= 1
    return out

def inv(a):
    return power(a, 6) if a else 0

def tr(a):
    return a ^ power(a, 2) ^ power(a, 4)

def AS(a):
    return mul(a, a) ^ a

def xor(values):
    out = 0
    for value in values:
        out ^= value
    return out

def solve(matrix, rhs):
    rows = [list(row) + [v] for row, v in zip(matrix, rhs)]
    for j in range(len(rows)):
        i = next(i for i in range(j, len(rows)) if rows[i][j])
        rows[i], rows[j] = rows[j], rows[i]
        scale = inv(rows[j][j])
        rows[j] = [mul(scale, v) for v in rows[j]]
        for i in range(len(rows)):
            if i != j:
                scale = rows[i][j]
                rows[i] = [v ^ mul(scale, w)
                           for v, w in zip(rows[i], rows[j])]
    return tuple(row[-1] for row in rows)

def fixture(N, K, target):
    points = tuple(range(N))
    H = [[power(alpha, j) for alpha in points] for j in range(K)]
    B = tuple(y for y in range(q) if tr(y) == target)
    offsets = tuple(product(B, repeat=N-K))
    words = {}
    for y in offsets:
        free = tuple(map(inv, y))
        rhs = [xor(mul(c, x) for c, x in zip(row[K:], free)) for row in H]
        word = solve([row[:K] for row in H], rhs) + free
        assert all(xor(mul(c, x) for c, x in zip(row, word)) == 0 for row in H)
        if all(tr(inv(x)) == target for x in word):
            words[y] = word
    return offsets, words

def audit(N, K, target, d=1):
    offsets, words = fixture(N, K, target)
    slopes = (1, 2, 3, 4)
    assert N-K == len(slopes)
    # Repeated columns when d=2 deliberately test repeated preimages.
    shifts = [tuple(xor(AS(mul(a, t)) for t in ts) for a in slopes)
              for ts in product(range(q), repeat=d)]
    M, R = len(shifts), len(offsets)
    histogram, incidence, naive, repaired = (Counter() for _ in range(4))
    for c in offsets:
        good = [y for shift in shifts
                if (y := tuple(v ^ w for v, w in zip(c, shift))) in words]
        Z = len(good)
        histogram[Z] += 1
        for y in good:
            incidence[y] += 1
            naive[y] += F(1, R*Z)
            repaired[y] += F(1, R*M)
    p = F(len(words), R)
    success = sum(naive.values())
    tv = sum(abs(naive[y]/success-F(1, len(words))) for y in words)/2
    assert set(incidence.values()) == {M}
    assert set(repaired.values()) == {F(1, R)}
    assert sum(repaired.values()) == p
    assert sum(z*F(count, R) for z, count in histogram.items()) == M*p
    print((N, K, target, d), 'words', len(words),
          'histogram', dict(sorted(histogram.items())),
          'naive_success', success, 'naive_conditional_TV', tv,
          'corrected_success', p, 'corrected_unconditional_TV', 1-p)
    return histogram, success, tv, p

assert tuple(y for y in range(q) if tr(y) == 1) == (1, 3, 5, 7)
for t in range(1, q):
    assert Counter(AS(mul(a, t)) for a in range(q)) == Counter(
        {v: 2 for v in range(q) if tr(v) == 0})
h, s, tv, p = audit(6, 2, 1)
assert h == {0:8, 1:88, 2:80, 3:48, 4:16, 5:8, 6:8}
assert (s, tv, p) == (F(31,32), F(467,2108), F(17,64))
h2, s2, tv2, p2 = audit(6, 2, 1, d=2)
assert h2 == {q*z:count for z, count in h.items()}
assert (s2, tv2, p2) == (s, tv, p)
h, s, tv, p = audit(8, 4, 1)
assert h == {0:224, 1:32}
assert (s, tv, p) == (F(1,8), F(0), F(1,64))
audit(6, 2, 0)

offsets, words = fixture(8, 4, 1)
assert words[(1,1,1,1)] == (1,)*8
counts = Counter()
for slopes in product(range(q), repeat=4):
    c = tuple(1 ^ AS(a) for a in slopes)
    counts[c] += 1
    assert tuple(v ^ AS(a) for v, a in zip(c, slopes)) == (1,)*4
assert set(counts) == set(offsets) and set(counts.values()) == {16}
print('dependent-offset countercontrol: all 4096 curves productive; PASS')

for n, exponent in ((17,-1553), (31,-10214), (61,-81404)):
    Q, N = 1 << n, n*n
    K = N//8
    root = isqrt(Q)
    root += root*root != Q
    beta = F(1+2*root, Q)
    eta = min((Q**K-1)*beta**(N-K+1),
              Q**K*(beta+(1-beta)/Q)**N)
    assert eta <= F(1, 1 << -exponent)
    print('native bound only:', n, 'K', K,
          'eta <= 2^', exponent, 'productivity <= (1+eta)*2^', n-K)
print('ALL EXACT CONTROLS PASS')
PY
```

Verification in this pass: executed the embedded command directly from this
note with python3 -B. All exact finite controls and the three rational native
certificate inequalities passed in approximately 0.43 seconds on this machine.
Parent-reported follow-up: both inline commands were replayed with all checks
passing, and 15 new parent tests also passed. The GF8 fixture is identical to
the parent's independent production-backed test. Those parent checks were
reported to this reviewer, not rerun here. These results are not a
whole-repository test or a native-size sampling experiment. Only this note
was written in this assignment.
