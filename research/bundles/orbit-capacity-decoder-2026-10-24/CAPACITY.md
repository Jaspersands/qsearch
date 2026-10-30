# Capacity Lists And Source-Specific Singleton Compression

2026-10-24. LOCAL UNREVIEWED APPLICATION OF PUBLISHED DECODING RESULTS.
This changes the proposed receiver, not the existing cubic-orbit task.
It is not an implemented quantum algorithm, a separation, or a novelty claim.

## Decision And Prior-Art Audit

The previous pass closed the high-rate classical norm-flat region and
proved that enlarging any F_p-linear quadratic-zero subspace cannot extend
that mechanism. Allowing targets to vary gives an exact dense-list affine
completion problem, not automatically another norm-pencil instance. The
resident PRIME_CHARACTER_NORM_ATTACK and MOMENT_TARGET_MASKING results use
specific character predicates/moment laws; they do not solve arbitrary
explicit halfsets. No new classical solver is inferred from that rewrite.

An alternative constructive question is whether the old Prony rank gate is
a necessary quantum decoding limit. It is not, conditional on the following
existing deterministic decoder theorem. The additional mathematics here is
the source-specific ambiguity bound and its guarded perfect-search transfer.

[Brakensiek et al., Corollary5.1](https://arxiv.org/html/2609.08005#S5)
gives prime-field capacity list decoding with a field-size constant depending
on fixed slack/rate. Do not silently assume the old p approximately3M domain
meets that unspecified constant. The stronger
[Jeronimo, Theorem1.1 and Corollary8.2](https://arxiv.org/html/2609.05870v1)
states deterministic complete lists for any prescribed prime-field domain,
fixed capacity slack, and sufficiently large length, with q^O(1) field
operations and polynomial list size. Fixed interleaving is explicitly
included there. These are external preprint theorem dependencies, not
results proved or newly implemented by this project. Their constants may
be enormous. The present finite ledger does not certify their length
threshold or provide a practical decoder implementation.

Power decoding was also checked: the improved interleaved algorithm of
[Puchinger--Rosenkilde](https://arxiv.org/abs/1701.06555) has a different
probabilistic performance justification. It does not supply the complete
worst-case list needed here. We do not substitute its abstract's random-error
language for a theorem about this source.

## Same Native Relation And Access

Keep p odd prime, zeta of order3, M disjoint ordered orbits, public nonzero
b_i, public nonsquare nu and explicit F_i of size(p-1)/2. The output remains
ONE polynomial of degree<n=3K satisfying all predicates

    P(zeta^2*a_i)+b_i*(P(a_i)^2-nu*P(zeta*a_i)^2) in F_i.

Its length-N=3M evaluation code has parity-dual syndrome map

    H e = (sum_a e_a*a^j)_(0<=j<n).

The kernel is GRS_(N-n) with multipliers1/A'(a), where A vanishes on the
ORIGINAL N points. A public particular word y with H y=s is obtained by
solving a Vandermonde system; it is not a supplied error word. Divide y by
the multipliers, list-decode ordinary RS at scalar radius3C, convert each
candidate back to an error, then keep only block weight<=C. This gives the
COMPLETE burst-cap fiber. At C<=K-gamma*M with fixed gamma>0, the cited
capacity theorem applies asymptotically. The input tables have sizeO(Mp),
so polynomial dependence on p is paid. This is not poly(log p) access.

Equivalently, use the existing fold into three K-syndrome rows over the
M distinct cubes. Each row is dual to GRS_(M-K); enumerate the three
complete scalar lists and filter their Cartesian product by UNION support
size<=C. Fixed interleaving keeps this polynomial. The source never supplies
extra copies or independent row samples. This equivalence is a known
coding operation, not the new contribution.

## Collision Lemma For The Actual Source

Fix the active support S, w=|S|<=D<=C<K, and EVERY last frequency v_i!=0.
The existing Gauss-sum source law makes the two other frequencies on each
active block independent uniform elements of F_p. The v_i law need not be
uniform. Candidate competitors need not satisfy that source promise.

For a proposed competitor support T of size c<=C, put a=|S minus T|.
If S is contained in T, no distinct competitor exists: H is injective on
the3c original points. If |S union T|=c+a<=K, the same Vandermonde fact
excludes a competitor, because every omitted source block has v_i!=0.

Otherwise put

    V_T(X)=product_(j in T) product_(ell=0)^2 (X-a_j*zeta^ell).

Multiply the syndrome equations by the coefficient vectors of
V_T(X)*X^h for0<=h<3(K-c). This annihilates every competitor coordinate
and every common block. On the2a free source coordinates outside T, the
remaining coefficient matrix is a Vandermonde matrix with nonzero column
scalings. Its rank is EXACTLY min(3(K-c),2a). Therefore

    Pr[an error supported on T shares H e]
        <= p^(-min(3(K-c),2a)).

The fixed last frequencies contribute an affine right-hand side. If it
is inconsistent the probability is zero, never larger. This is a rank
argument for every fixed source input, not an IID-input or generic-rank
assumption. The annihilator rows span the full left nullspace of H_T, so
the test is also sufficient for membership in its column span.

Counting the possible T gives the exact finite union-bound expression

    epsilon_w <= sum_(c=0)^C sum_a
       binom(w,a)*binom(M-w,c-w+a)
       * p^(-min(3(K-c),2a)),

where a>=1, 0<=c-w+a<=M-w, and c+a>K. Cap the result at1. There is no
extra count of amplitude values: all such values on T were eliminated by
linear algebra. Supports containing the same error are not distinct errors.

For g=K-C>=1, every surviving term has a>=g+1 and K-c>=g. Thus uniformly
for all w<=D,

    epsilon <= min(1, 2^M / p^h),   h=min(3g,2g+2).

The2^M counts ALL competitor supports, so this loose bound does not assume
their independence. The all-zero source label has no competitor when C<K.

## Coherent Receiver And Rate Consequence

Compute the deterministic COMPLETE list from the syndrome, deduplicate
errors, and herald exactly one candidate in the WHOLE cap C=D+1. Compute
its error from the syndrome, erase the original error by subtraction, then
uncompute list/index/path work. Only the herald flag is measured. Reject
empty or ambiguous lists. No list-size-dependent amplitude normalization,
randomized incomplete list, or stored which-support record is permitted.

The old one-extra-block score-operator identity now applies unchanged.
With rho=(p-1)/(2p), let tau=Pr[Bin(M,1-rho)>D]. Pay BOTH preparation and
singleton heralds. The existing first-moment/integer-score argument gives
one-attempt perfect-search failure at most

    min(1, tau + M*(epsilon+sqrt(tau)+sqrt(epsilon))).

A separately bounded full-circuit trace/TV error must be added. This is
a first-moment conclusion, not a uniform-output or full-filter identity.

For ANY FIXED rate R=K/M>1/2, choose a constant alpha strictly between1/2
and R, D=floor(alpha*M), C=D+1. Then g=Theta(M), tau=exp(-Omega(M)) and
epsilon=exp(-Omega(M log p)). Constant-slack capacity decoding, source
preparation and reversible classical computation are polynomial in the
explicit input size. Conditional on the external decoder theorem and the
existing coherent source/guard derivation, this yields an IDEAL asymptotic
perfect-search construction with success1-o(1), improving the old sufficient
R>2/3 regime. It establishes neither practical speed nor novelty.

The new scalar ledger uses the SAME p12289,M4096,D2375,C2376 but K2621,
n7863, rate2621/4096<2/3. Here g245 and h492. The old cap recurrence has
only735 equations for2375 active columns and cannot have the required
rank. The new collision bound and source-tail calculation are numerical
certificates only; no capacity backend, circuit or native output at these
parameters has been executed. The external theorem's finite length
threshold remains uninstantiated, so the ledger is CONDITIONAL, not a
certified finite algorithm run.

## Exact Endpoint: Do Not Extrapolate Below One Half

The strict guard C<K is not just a capacity theorem convenience. If K<M,
take any NONZERO error e of block weight<=K and choose a K-block support T
that omits one of its nonzero blocks. The3K original columns on T form an
invertible square Vandermonde matrix. Hence there is an error e' supported
on T with H e'=H e. It is different from e because the omitted block is
zero in e'. Thus every nonzero source error has a competitor in the whole
cap K. At any C>=K such a source cannot be certified singleton.

For C>K even the zero fiber contains a p^(3(C-K))-element kernel on a
fixed C-block support. This is an exact algebraic obstruction to this
WHOLE-CAP singleton receiver, not to all quantum algorithms or list
projection protocols. For a truncated all-satisfying source with
R<1/2 and nonnegligible preparation probability, the required D near/above
M/2 places C beyond K. Shrinking D below K instead incurs an exponentially
small source-preparation probability. No further fixed-rate extension
below1/2 follows by merely increasing this receiver's cap.

## Decisive Controls, Failure Modes And Research Decision

The executable reference enumerates bounded scalar message spaces ONLY.
It refuses before exceeding its public enumeration/product budgets. It is
not the cited capacity algorithm and never promotes a truncated list to
complete. Small full lists test the syndrome-only conversion, inverse fold,
deduplication, union-support pruning and actual whole-cap ambiguity.

- A native p31,M7,K6,weight4 case can be singleton at cap5 even though the
  old rank certificate has at most3 rows. Recovery must match every original
  frequency and syndrome, not a support supplied to the receiver.
- A guarded collision uses a weight7 dual codeword split into supports3/4:
  source-radius3 uniqueness is real, but cap4 has another error. The guard
  must reject it. Dropping v_i!=0 is not a licensed source replacement.
- At p13,M4,K3,w2,C2, the only possible competing support is the complement.
  Exact enumeration of all13^4 free assignments gives13 collisions, hence
  1/13^3, matching the rank bound. This is a calibration, not the asymptotic
  proof or a quantum execution.
- Dense halfsets are NOT bounded-size input lists in the external theorem.
  It decodes the singleton received symbols in the Fourier receiver; it
  cannot directly solve the original halfset optimization classically.
- A published source-specialized corollary might already subsume this result.
  General DQI/list projection and fixed interleaving are known. Independent
  review of this specific collision/guard combination is still needed.
- No currently implemented classical attack is ruled out in general.
  The high-rate norm solver, intrinsic search, target completion and natural
  reduction questions remain mandatory. No oracle or ECDSA claim follows.

Do not respond with a field/seed sweep or label the unavailable large backend
as tested. The next high-reasoning step is a precise prior-art/proof review
of the resulting source-specialized theorem and a natural-problem reduction
or a stronger classical attack in1/2<R<=2/3. Bounded integration instructions
are in HANDOFF.md.
