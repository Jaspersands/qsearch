# Pivot-Power Sampling On A Fixed Measured Bank

30 October 2026. Bounded prime-field arithmetic and a conditional IID-label
calculation. The parent supplied Euclid's independent probability audit,
which confirms the rank-exponent improvement and identifies the regularity
counterexample below. Ramanujan subsequently performed an independent
implementation/accounting review, with no concrete findings; see
audits/reviews/2026-10-30-sampling-pivot-power-round.md for its exact scope.
These are AI-agent checks, not human peer review, a formal receiver,
a novelty certificate, or a new all-prime HSP theorem.

## Improvement And Scope

The existing [random-column sampler](RANDOM_COLUMN_REES_PARAMETER_BOUND.md)
samples a uniform kernel vector and checks every coordinate for power
membership, with a sufficient classical search allowance proportional to
d^M for M labels. The construction here samples power-valued free
coordinates first, so only the a pivot coordinates are tested. Its
good-bank search allowance is proportional to d^a, where a is the true
source rank. All trials reuse the SAME saved measured bank.

The [small-prime subset method](SMALL_PRIME_REGULAR_SUBSET.md) already
provides an all-prime source-tree branch. This note does not claim new
coverage. It gives a single rejection method without a p^a-state table,
retaining polynomial working storage and explicitly paid d^a search time.
It need not outperform the published arbitrary-input solver in every regime.

This module is PRIME-FIELD-ONLY. Active support need not span the label
space, so it does not supply a regular mixed-order Hensel starting point.
The [ring-to-field outer reduction](UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md)
is unchanged. No inverse-trace diagnostic, CLI, registry, or receiver is
changed by this implementation.

## Input And Fixed-Prefix Construction

Supply an odd verified prime p, original exponent e >= 1, canonical finite
ambient field columns, fixed pilot count N, intrinsic rank bound R <= N,
at least one suffix column, and a mandatory positive attempt cap K.
N=0 is allowed only when R=0; a single zero label is then sufficient.
The arithmetic permits any positive e; Rees applications separately need
their original grade and characteristic promises. Public computation pays
for the bit length of e and for arithmetic polynomial in d, not log(d).

Let d=gcd(e,p-1), h=(p-1)/d, S={0} union (F_p^*)^d, Q=h+1, and
alpha=Q/p >= 1/d. Select an independent basis ONLY from the first N
columns using existing arbitrary-precision field RREF. The pilot length
never changes in response to its observed rank. Express EVERY suffix
column in that basis with the existing coordinate solver, verifying its
ambient reconstruction. If any suffix column is outside the pilot span,
abort; do not promote it into the basis. Charge all supplied labels.

For suffix length ell and coordinate matrix C, sample

    x = (1, x_2, ..., x_ell),  x_i uniform in S,
    y = -C*x.

Accept exactly when every entry of y belongs to S. Assign y to the
selected pilot basis, zero to all other pilot columns, and x to the suffix.
The anchored first suffix coefficient is one, so the witness is nonzero.

To sample S, first draw j uniformly in {0,...,Q-1}. If j=0 return zero.
Otherwise draw z uniformly in F_p^* and return z^d, retaining z. This uses
at most TWO uniform integer calls per nonfixed suffix coordinate. Each
nonzero power has exactly d preimages, giving probability 1/Q for every
element of S, including zero. No generator, field table, discrete logarithm,
or root extraction is used for suffix coordinates. Keeping zero is crucial
when d=p-1, since the nonzero-power subgroup then contains only one element.

Extract roots only for NONZERO pivot coefficients. Call the existing
bezout_reduced_exponent and apply its exponent with an explicit zero guard.
Compare every original e-th power to its assigned coefficient, then call
the existing original-ambient verifier. Empty ambient coordinates are the
vacuous zero-bank case. Zero-rank and d=1 cases are deterministic, but still
check all suffix memberships. Original labels are never resampled.

## Exact Conditional Probability

Assume the input labels really are IID uniform in a fixed unknown subspace
W of dimension a <= R. Execution does not certify that promise.

The N pilots fail to span W with exact probability

    1 - product_(i=0..a-1) (1-p^(i-N))
      <= (p^a-1)/((p-1)*p^N).

Conditional on any COMPLETE pilot transcript, the suffix coordinates C
are IID uniform in F_p^(a x ell). The following calculation is NOT
conditioned on suffix membership or solver acceptance. Under a complete
pilot, membership is automatic. An incomplete pilot is charged as bad
source probability, even if ambient verification later allows success.

Let X count the candidates in {1} x S^(ell-1) for which -Cx lies in S^a.
There are D=Q^(ell-1) candidates. Distinct candidates are linearly
independent because both have first coordinate one. Their images under C
are therefore independent uniforms. Exactly,

    E[X] = D*alpha^a,
    Var(X) = D*alpha^a*(1-alpha^a).

Chebyshev bounds the event X < E[X]/2 by

    min(1, 4*(1-alpha^a)/(D*alpha^a)).

Outside that bad-bank event, the fixed-bank acceptance density is at least
alpha^a/2 >= 1/(2*d^a). For a=0 or d=1, all candidates hit and the density
is one. Repeated independent classical proposals on a good FIXED bank
have failure at most (1-density)^K. Taking K >= 2*d^a*B makes this at most
exp(-B) <= 2^-B. A caller that knows only R can use 2*d^R*B. The execution
API never infers or silently installs an exponential attempt cap.

The budget reports moments evaluated at R, explicitly named as such.
They are exact moments only if a=R; the bad-bank upper bounds and density
lower bound are conservative for every a <= R. An exact actual-rank
conditional calculation is separately available through
pivot_conditional_moments(p,e,rank,suffix_count).

## Bounded Randomness And Accounting

For nonlinear positive-rank operation, with f=failure_bits, use

    A = R*(d-1),
    J = 3*(f+1+ceil(log2(max(1,A)))),
    Q_sample = 2*(ell-1)*K,
    Q_root = R*J*(d*(d+1)/2-1),
    Q_total = Q_sample+Q_root,
    L = f+1+ceil(log2(Q_total)).

J is the maximum split attempts at each root descent; L is the maximum
bit-rejection attempts at each uniform integer call. A strict root descent
visits degrees at most d,d-1,...,2. Thus the existing splitter uses at most
J*(d*(d+1)/2-1) uniform calls and J*(d-1) split trials per started root call.
This is the actual sum-of-degrees bound, not the looser d*(d-1) surrogate.
Its standard splitting primitive is
[Cantor--Zassenhaus, Algorithm 3.47 in Sutherland's notes](https://ocw.mit.edu/courses/18-783-elliptic-curves-spring-2021/b6d0aef71278ad8c1d8b5144c4138cb7_MIT18_783S21_notes3.pdf).

The separate auxiliary bounds are

    root_abort <= R*(d-1)*(2/3)^J,
    bit_abort <= Q_total/2^L,
    root_abort+bit_abort <= 2^-f.

Deterministic branches have zero planned random work when R=0 or d=1.
An observed zero bank with a loose positive R uses none of its planned caps.
All counts are upper bounds, not claims that all reserved work executes.
Fresh fair bits remain an unverified input hypothesis. A first-error
coupling justifies the bit bound without conditioning on eventual success.

The root helper does not expose its split counters when a bit draw raises
RandomnessExhausted. The wrapper therefore:

- Counts a root call and charges its FULL declared allowance before entry.
- Counts all uniform calls, bit draws and bits, including interrupted calls.
- Retains returned-call split/proper-split counters separately.
- Sets aggregate split/proper-split counts to null on interruption; it does
  not fabricate zero work or claim those aggregate counts are exact.
- Aborts immediately, never returning a partial witness or starting another
  root call after declared exhaustion.

Unexpected backend failures, malformed bits, invalid roots or coordinates,
and inconsistent accounting are errors, not statistical ABORTs. Primality
validation and deterministic arithmetic are not locally wall-clocked.

Bad-bank probability, good-bank attempt exhaustion, and auxiliary failure
are separate budget fields. In particular, failure_bits does NOT promise
that arbitrary fixed-bank search succeeds. The attempt bound is retained
as a rational base and integer exponent, without expanding an enormous
Fraction when K is large. No space proportional to K is allocated.

## Resource Consequence

Each proposal uses polynomial field work in a,ell,log(p),log(d). At most a
nonzero pivot roots are extracted after the first accepted proposal, using
arithmetic polynomial in d,log(p),failure_bits. The search factor is d^a,
not d^(N+ell); bank storage and all workspaces are polynomial in public
input sizes and log(K). Classical attempts consume no new quantum inputs.

Assume integer u>=2, a<=u-1 and d,c<=u, retaining the inherited c<p
application promise. For arity M, a depth-(c-1) one-output tree has
P=M^(c-1) leaves and at most P<=M^(u-1) merge nodes. The c=1 case has
no merge nodes. All bounds below are union bounds conditional on the
preceding required successes; they assert no independence of node failures.

For a single uniform all-prime schedule, take

    t=ceil(log2(u+2)), N=ell=4*u*t, M=8*u*t, P=M^(c-1).

Since p>=3 and the pilot failure is at most p^(a-N)/(p-1), its per-node
bound is at most 1/(2*3^(N-u+1)). Also Q>=2 and alpha>=1/u, so the
per-node tail bad-bank bound is at most 4*u^(u-1)/2^(N-1). Define

    F_pilot = M^(u-1)/(2*3^(N-u+1)),
    F_tail  = M^(u-1)*4*u^(u-1)/2^(N-1).

The following proves F_pilot+F_tail<1/64 analytically, without a sweep.

If u=2, then t=2, N=16 and M=32. Directly,

    F_tail = 1/128,
    F_pilot = 16/3^15 < 1/1024,
    F_pilot+F_tail < 9/1024 < 1/64.

If u>=3, then t>=3, log2(u)<t and log2(t)<=t-1. Consequently
log2(M)=3+log2(u)+log2(t)<2*t+2, and

    log2(F_tail)
      = (u-1)*log2(M) + 3 + (u-1)*log2(u) - 4*u*t
      < 1-u*(t-2)-3*t
      <= -11.

Using log2(3)>1 and N-u+1>0 also gives

    log2(F_pilot)
      = (u-1)*log2(M) - 1 - (4*u*t-u+1)*log2(3)
      < -2*u*t+3*u-2*t-4
      <= -19.

Thus F_pilot+F_tail<2^-11+2^-19<1/64 for every u>=3 as well.

For the prior large-prime regime p>=16u^2, retain the same M=4u source
arity and split N=ell=2u. Here Q>=p/d>=16u and alpha>=1/u. The tree
tail contribution is therefore at most

    (4*u)^(u-1)*4*u^(u-1)/(16*u)^(2*u-1)
      = 2^(4-6*u)/u
      <= 1/512.

The pilot contribution is at most (4*u)^(u-1)*p^(-u-1)/(p-1).
Using p-1>=p/2 and p>=16u^2 bounds this by

    2*(4*u)^(u-1)*(16*u^2)^(-u-2)
      = 2^(-2*u-9)*u^(-u-5)
      <= 2^-20.

Their sum is again strictly below 1/64. These estimates deliberately use
the looser tail bound 4/(D*alpha^a); the implemented sharper variance
bound can only improve them.

With B=ceil(log2(64P)), K=2*u^(u-1)*B, and auxiliary failure_bits=B,
each good-bank search fails with probability at most exp(-B)<=2^-B;
the COMBINED root/bit failure bound is also at most 2^-B per node. Each
contributes at most P*2^-B<=1/64 across the tree. Including bank failure,

    Pr[tree abort] < 1/64 + 1/64 + 1/64 = 3/64 < 1/16.

Existing pointwise conversion and paid whole-tree restart arguments then
retain 2^O(u*log(u+2)) total conditional cost. Successful ideal children
must have the same target state independently of their accepted records;
approximate execution still requires the inherited complete flagged-channel
error accounting. This is not an implementation or independent proof of
those receiver/source/compilation conditions, an optimal-arity claim, or
a novelty or new-coverage claim.

## Decisive Regularity Counterexample

At p=5, e=d=2, take pilot columns (1,0),(0,1) and suffix (1,0).
The anchored candidate gives coefficients (4,0,1), with roots (2,0,1)
(the other square root works as well). Active columns span only dimension
one although the pilot rank is two. This is a valid prime-field witness,
not a full-rank Jacobian certificate.

Over Z/25, replace the suffix by (1,5), keeping the same reductions.
Freezing the second pilot scale at zero leaves the second equation
5*s_3^2=0 modulo25. Every allowed active suffix scale is a unit, so this
is impossible. No support-preserving regular Hensel guarantee follows.
All execution/budget reports carry prime_field_only=true and
regularity_not_guaranteed=true. No nonzero-pivot variant is implemented.

The fixed field bad bank p=5,d=4,A=(1,1,1) also remains a decisive control:
no nonzero power kernel exists. Increasing attempt_cap cannot repair it.

## API And Verification

Implementation: theorems/pivot_power_sde.py. Public functions:

- pivot_power_sde(p,e,columns,*,pilot_count,rank_bound,attempt_cap,
  failure_bits=32,bit_source=None): fixed-bank arithmetic, explicit ABORTs.
- pivot_power_budget with width replacing columns: caps and conditional
  failure components, with a mandatory explicit attempt cap.
- pivot_conditional_moments: exact complete-pilot suffix moments.
- pivot_power_report(): seeded replay data, without filesystem writes.

Tests in tests/test_pivot_power_sde.py cover exhaustive moments over
136,852 matrices, exact pilot probabilities, prefix-only basis selection,
nonmembership, deterministic branches, uniform S sampling including zero,
retained suffix roots, bad banks, interrupted root/bit calls, original
exponent lifting, noncoordinate support, root/backend faults, the regularity
counterexample, and a 127-bit prime. Small-field enumeration is confined to
tests; production does not enumerate a field or candidate alphabet.

The stored research/classical_baselines/pivot_power_sde.json records four
seeded successes and the fixed bad-bank abort, with full banks, witnesses,
caps and observed counts. Seeded controls are not IID certification or a
physical source/receiver execution. No new all-prime coverage or speedup
claim is made.

A persistent regression reads that stored artifact and compares its entire
envelope with a fresh deterministic report using canonical JSON (sorted
keys, compact separators, explicit Fraction strings, and no NaN values).
It independently recomputes all seven source hashes from fixed repository
paths, including this note and the test file itself. Missing/extra report
fields, altered counts or witnesses, and stale source bindings therefore
fail the comparison. The verification metadata is an explicit frozen
checkpoint receipt, not a fresh test-count measurement by that regression.

Reproduce the focused tests without bytecode or pytest-cache writes:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider -W error tests/test_pivot_power_sde.py
```

Connected verification: 261 tests passed with warnings as
errors, disabled pytest plugin autoload, bytecode writes and pytest cache.
The five files were test_pivot_power_sde.py, test_bounded_power_roots.py,
test_power_sde_budget.py, test_random_column_power_sde.py and
test_weighted_two_erasure_cascade.py. Both new Python files also passed
AST syntax, ASCII and trailing-whitespace checks. This is not a full
repository suite, a Lean rebuild, or a receiver execution. No Git or CLI
operation was performed; writes were limited to the four assigned files.
