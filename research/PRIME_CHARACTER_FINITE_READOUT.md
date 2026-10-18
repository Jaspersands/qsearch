# Finite Character-DQI Readout: Mean And Tail Certificates

2026-10-18. Known DQI mechanism, LOCAL APPLICATION REVIEW PENDING.
CONDITIONAL on an exact source and exact verified unique decoder. This is
not a new quantum algorithm, a large quantum execution or a speedup claim.

## Question And Result

Does the fixed-input source ambiguity bound certify a finite useful score,
not just closeness to an unanalyzed ideal state? Yes, when an EXTRA observable
radius gives a sufficiently small radial Gram error. Source normalization
alone is insufficient, and the new certifier retains a counterexample.

At N127,K39,p=2^61-1, radius32, the certified normalized mean is about
0.9028547353515506, or114.66255 accepted positions. Conditional on the stated
receiver, one attempt has probability at least0.314586 of reaching110/127,
and0.050965 of reaching115/127. No binomial full-score law is assumed.

The saved same-input classical witness has109/127, but no matched runtime
comparison exists. The required finite decoder is still missing and the
published generic fixed-gap implementation has prohibitive-looking bounds.
It would be misleading to report this finite score certificate as an
implemented quantum advantage or to infer classical hardness from it.

## Problem, Algorithm And Costs

Reuse [the character source](PRIME_CHARACTER_CAPACITY_SOURCE.md): fixed public
quadratic-coset lists over p=3 mod4, strict or including zero; prime field,
distinct points1,...,N, degree<K. Local centered Fourier magnitudes are flat
away from zero. A radial superposition of sparse errors is mapped by the
K-row Vandermonde H to a coefficient-space syndrome. Verified unique decoding
and conditional erasure are followed by a finite-field Fourier readout.

The kernel is dual GRS of dimension N-K. Decoder rate is (N-K)/N and gap is
(K-ell)/N. The source, decoder, arithmetic, work-space uncomputation, QFT and
rotation errors all require actual compilation/resource accounting. Their
errors are NOT asserted to be zero for a physical implementation. An exact
mathematical receiver is the premise of the present certificates.

The proposed asymptotic gain remains known code-intersection sampling. The
new contribution to this repository is finite, fixed-input evaluation and
explicit rejection of invalid proof shortcuts, not an algorithmic novelty.

## Radial Near-Isometry

Let |j> be the normalized ambient sparse-error source of weight j. Its
nonzero entries on each support are products of the exact local ghat_i.
These radial states are orthonormal BEFORE syndrome coalescing. Their supports
at different j are disjoint, even with arbitrary public-shift phases.

Take the whole error ball of radius L<K and let A map |e> to |H e>, adding
amplitudes on collisions. This A is a mathematical coalescing map, NOT a free
quantum unitary. Put

    epsilon = max_(j<=L) epsilon_j,
    M = sum_(r<=L) C(N,r),
    delta = max(1,M-1)*epsilon.

For any unit radial superposition u, its bad mass b<=epsilon. Unique-good
and ambiguous-bad syndrome images have disjoint supports. The good image has
norm squared1-b and the bad image has norm squared at most M*b. Therefore

    1-epsilon <= ||A u||^2 <= 1+(M-1)*epsilon.

Writing G for the Gram matrix of the coalesced radial states proves

    ||G-I||_operator <= delta.

This is UNIFORM over radial coefficients, not a bound for only the particular
numerical filter that happened to look favorable. All source phases are
allowed; no random-input premise or favorable source selection is inserted.

## The Score Reaches One Extra Radius

Let q_j(x) be the elementary-symmetric degree-j polynomial in the centered
native predicates g_i(Q(a_i)), and phi_j=q_j/sqrt(C(N,j)). The known identity

    q1*q_j = (j+1)*q_(j+1) + (N-j+1)*q_(j-1) + beta*j*q_j,
    beta=(1-2rho)/sqrt(rho*(1-rho)),

is [Sun-Wootters, Lemma5.4](https://arxiv.org/html/2610.12357).
The normalized score operator in the AMBIENT radial basis has Jacobi matrix

    T[j,j] = rho+(1-2rho)*j/N,
    T[j,j+1] = sqrt(rho*(1-rho)*(j+1)*(N-j))/N.

The full matrix is the restriction of multiplication by a score in[0,1],
so it is a positive contraction. A source supported through ell is sent by
this observable through ell+1. Thus the near-isometry proof needs L=ell+1,
not just ell. With u supported through ell and ||u||=1,

    mu_ideal = (u^* G T u)/(u^* G u),
    mu0 = u^* T u,
    |mu_ideal-mu0| <= 2delta/(1-delta),  provided delta<1.

Here T*u is taken in the extended space through ell+1; no last-row term is
dropped. We use |u^*(G-I)T*u|<=delta and |u^*G*u-1|<=delta. We do NOT assume
that a truncated G*T commutes or is Hermitian on the entire extended space.
Only the stated source/observable bilinear identity is needed.

When 2ell+1<=K, the older exact RS-moment argument already determines every
needed term. That branch uses exact moments, not a false assertion that the
ENTIRE extended Gram matrix is identity. The artifact labels the two proof
methods separately. Outside that regime, ell+1>=K or delta>=1 is UNKNOWN,
even if a numerical Rayleigh quotient looks excellent.

## Rational Evaluation, Not A Floating Eigenvalue Claim

NumPy proposes positive radial weights from a tridiagonal eigenvector. The
actual filter uses saved DYADIC RATIONAL weights, normalized by their exact
squared norm. Each square-root matrix entry has an integer-isqrt rational
enclosure; signed weights use the correct interval direction. The certificate
is for that filter, not a formally certified optimum or eigenpair.

The native density rho=(p+eta)/(2p), eta+1 including zero and eta-1 strict,
is retained exactly. Neither is silently rounded to the balanced1/2 model.

The source pass separately bounds trace distance from the normalized full
ideal pushforward to the actual unique-herald output. Subtract its rational
square-root UPPER enclosure from the ideal mean lower bound. At radius32:

- Extended L33 Gram operator error<=1.027e-49.
- Ideal-mean correction<=2.054e-49.
- Herald-output TV<=7.257e-35, which dominates that correction.

These are exact mathematical-source guarantees-under-premises, NOT measured
gate errors. Any actual synthesis/decoder/QFT trace error must be added.

## Finite Tail Without Inventing A Distribution

Accepted count S takes integer values0,...,N. Given a normalized mean lower
bound mu, its threshold-k tail obeys

    Pr[S>=k] >= max(0,(N*mu-(k-1))/(N-(k-1))).

This is sharp given only that mean: failed mass can sit at k-1 and success
at N. Multiply by the source's herald-success floor for a per-attempt bound.
For fresh independent receiver preparations, repetition uses1-(1-p_success)^m.
Those repetitions are probabilities, not empirical confidence statements.
Serialized repeated bounds are conservative128-bit dyadic lower enclosures,
avoiding enormous decimal fractions without changing Python's global limits.

At ell32, reaching110 has floors0.314586 per attempt,0.779295 for4 attempts,
and0.997627 for16. Reaching115 has floor0.0509655 per attempt. There is no
matched cost certificate for any of these attempts. A zero lower tail at
another radius does NOT prove its actual tail is zero.

## Decisive Controls And Classical Comparison

| Radius | Conditional Normalized Mean | Saved Same-Input Classical Score |
| --- | --- | --- |
|19|0.816830|109/127|
|22|0.840571|109/127|
|24|0.854932|109/127|
|32|0.902855|109/127|

The easier radius22/24 means do NOT exceed the saved classical word. Radius32
does, but its decoder/resource debt is not erased by this table. The strict
siblings have certificates too, with NO matched classical witness imported
from the zero-including task. Saved input specifications are compared exactly.

Two adversarial checks are especially important:

1. At p7,N4,K2,ell1, the source ball has ZERO ambiguity and the ideal filter
   norm is exactly1. Its native mean is0.760829 rather than the ambient
   Jacobi value0.801007. The new certifier refuses the unsupported score claim:
   the extra observable radius reaches capacity. Normalization alone is not
   a score proof.
2. At p10007,N5,K4,ell2, independent sums over the ONE-dimensional dual code
   give the extra correlation and all extended Gram entries. No p^4 native
   coefficient space is enumerated. Both zero conventions obey the Gram and
   mean enclosures; this is a nontrivial check beyond the generic K-moment
   cutoff, not just replay of the certificate's own formulas.

Radius37 is UNKNOWN because its Gram bound is too weak; radius38 is UNKNOWN
because the score reaches capacity. Neither is promoted from its attractive
numerical eigenvalue. Independent tests also retain signed radial weights,
exact square-root enclosures, integer-tail saturation and artifact provenance.

## Attempts To Prove It Wrong

- A bound on one radial state would not bound a Gram operator. The source
  lemma applies to EVERY radial coefficient vector because bad preimage mass
  is a weighted average of per-sphere probabilities. This uniformity is an
  essential proof obligation, not a numerical-eigenvector observation.
- Paying only ell instead of ell+1 gives a false finite mean. The p7
  counterexample demonstrates the failure with exact normalization.
- Delta may exceed1 even for a well-defined source. The quotient bound is
  then not used; no finite mean is certified by this method.
- Coalescing A is not physically supplied for free. The receiver uses an
  actual unique decoder/flag, with separately charged herald error. That
  decoder and its gate/space budget remain unimplemented at large size.
- The proof uses flat character magnitudes, MDS independence and native
  two-valued predicate recurrence. General lists or p=1 mod4 do not inherit it.
- A matched classical attack could erase the apparent finite score gap.
  Stored109/127 is a witnessed score, not an optimum, tail upper bound or
  classical lower bound. No asymptotic separation follows.
- Published decoder polynomiality has a gap-dependent exponent and huge
  finite conditions. It is not a finite operational resource bound here.

The next question is now the decoder/runtime, or a genuinely different
constructive mechanism, NOT another ideal-score/source mesh. In particular,
any interleaved-decoder shortcut must preserve the original single-polynomial
objective rather than preparing a joint product/parity task in extra registers.

```text
python theorems/prime_character_finite_readout.py --write
python -m pytest -q tests/test_prime_character_finite_readout.py
```
