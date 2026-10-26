# Balanced Filter: Audit The Physical Composition

2026-10-22. Local derivation and independent finite implementation,
EXTERNAL REVIEW PENDING. This is a check of the existing explicit-input
inverse-trace construction, not a new quantum algorithm or speedup claim.

## Decision And Scope

The later EXACT_PREDICATE_CHANNEL.md incorporates the separate repository
review and proves the stronger exact law: native success=lambda_b*tau^2/P,
with exact uniformity conditional on native success. The executable audit
now checks every signed output amplitude against that law. The older loose
triangle estimate below remains valid but is not used by current budgets.

PRIOR-ART UPDATE: Jo arXiv2607.16541v2, Theorem5.2/Remark5.3 already gives
the fixed-padded full-list primitive and its normalization warning. Horinaga--
Yamakawa arXiv2607.14650, Theorem5.1 supplies a generic worst-case prime-power
theorem once the scalar native estimates are verified. See the primary links
and exact scope in EXACT_PREDICATE_CHANNEL.md. No new general mechanism is
claimed. The later note also extends the law to every fixed public syndrome.

The native input is a public F_(2^n) modulus/basis, distinct evaluation points
alpha_i and arbitrary target bits b_i. Find Hx=0 and Tr(inv0(x_i))=b_i for
every i, with H[j,i]=alpha_i^j. There is no hidden oracle. The proposed
ideal quantum runtime is polynomial in n,N at a fixed admissible RS rate;
no classical separation or application to a standard hard problem is known.

The previous classical Gibbs result obstructs one worst-start sampling
guarantee, not classical witness-finding. The higher-value next question was
whether the proposed quantum algorithm silently assumes the exponentially
normalized coalescing map it is supposed to implement. An exact register-level
audit finds no such error in the COMPLETE-SINGLETON, CLEAN-WORKSPACE protocol.
It also supplies a paid FULL-LIST projection variant that removes the
low-ambiguity premise; its derivation is given below. The audit finds decisive
countercontrols against superficially similar protocols
with identical source probabilities and herald statistics.

This is not independent human/theorem-prover validation of the full proof.
The support-mask tail lemma, ambiguity estimate and deterministic GS route
remain in their existing notes. No unavailable cloud source was reconstructed
or replaced; the finite audit uses installed FLINT directly and records its
public field polynomial. It does not implement large-field GS or a circuit.

## Exact Successful Branch

Write D for the low-rate decoder code, M=|D|=q^K, C=D^perp, and a(e) for
the normalized signed Fourier root-product source. M here is the CODE SIZE,
not the inverse-temperature parameter from the Gibbs note. Let U be the
radius-w errors whose complete radius-w list is a singleton.

Start with the normalized joint state

    M^(-1/2) sum_(d in D,e) a(e) |d>|e>.

Compute and measure only the threshold bit wt(e)<=w, add z=d+e, compute the
complete list payload from z, and measure only the singleton flag. The list
for z is the translate by d of the list for e. Since d is already in the
radius list, a singleton MUST equal d. XOR the decoded message/codeword
into the original register; then uncompute the list payload using unchanged z.
The resulting UNNORMALIZED successful branch is

    |0> M^(-1/2) sum_(d in D,e in U) a(e)|d+e> = |0> A(1_U a).

This equality includes the actual 1/sqrt(M) from uniform code preparation.
It is not permission to apply an arbitrary normalized linear map for free.
U contains at most one error per D-coset. Consequently the map from (d,e)
to z is injective on accepted basis branches, and

    herald_probability = ||A(1_U a)||^2 = sum_(e in U) |a(e)|^2.

The herald probability is charged, not conditioned away. Distinct rejected
flags can be retained on rejected branches. On the successful branch only
the already-fixed threshold/singleton bits may remain; the actual weight,
support, original message, decoded message and root/list history must not.

For any u, A(u)=M^(-1/2) sum_d T_d u is invariant under every D translation.
Its inverse Fourier transform is therefore supported exactly on C. This
means the correctly erased receiver NEVER violates Hx=0, even at finite
parameters where it can still violate the local inverse-trace predicates.
Native verification must check both, not just the parity equations.

The general decode/uncompute architecture is prior art; see Briaud et al.,
[quantum algorithm overview and Section4](https://arxiv.org/html/2509.07276v1).
The repository's separate issue is its deterministic per-instance source
analysis, not discovery of the architecture.

## A Retained Codeword Costs Exactly q^K On Native Answers

Let u=1_U a. If an orthogonal which-codeword/message record survives, tracing
it out gives

    rho_dirty = (1/M) sum_(d in D) |T_d u><T_d u|.

In the Fourier readout, translations only change phases. Thus for EVERY x,

    p_dirty(x AND herald) = |F^(-1)u(x)|^2.

Clean erasure instead gives

    p_clean(x AND herald) = M * 1_(x in C) * |F^(-1)u(x)|^2.

Therefore on ANY subset B of C, including the fully valid native answers,

    P_clean(B AND herald) = q^K * P_dirty(B AND herald).

The two protocols have exactly the SAME herald probability. A test of source
probabilities, decoder success, or herald rate alone cannot distinguish them.
At N=n^2,K=floor(N/8), this penalty is 2^(nK), not a harmless constant.
This is an exact register identity, not a lower bound on all classical
simulation methods or on the native search problem. A different classical
algorithm need not follow this dirty-record protocol.

## Other Faults That Herald Tests Miss

Retaining the exact weight or support splits the successful state into
incoherent branches A(1_(U intersect record) a). Each still enforces C, and
the total herald mass is unchanged, but interference between those branches
can be essential to satisfy the local predicates. There is no claim that
every such record lowers success on every input; the finite controls exhibit
explicit failures, not a universal loss factor.

Replacing source amplitudes by their magnitudes preserves the source
probabilities and singleton statistics too. It is not the Fourier transform
of the required root state. The executable control keeps that fault separate
from record retention.

An incomplete list truncated to its first valid entry can report a false
singleton. The original message then need not equal the decoded message.
The audit retains the NONZERO residual register rather than silently resetting
it, and records its exact probability. This faulty variant can even improve
some finite success scores; that does not validate the claimed clean-erasure
proof or its asymptotic guarantee.

## Exact Finite Evidence

The implementation enumerates messages, errors and complete radius lists.
It executes addition, flags, XOR erasure and retained-record branches before
Fourier readout. It then compares the clean branch to the abstract coalesced
formula, not vice versa. All amplitudes are integers times one common square
root; every reported probability is an exact rational. All target vectors
are covered for each report fixture, including targets with no finite answer.
The public trace-pairing permutation is explicitly included in the readout.

One F8,N4,K1,w2 input, b=(0,1,0,1), illustrates why the controls matter:

| Protocol | Herald probability | Full-native success per attempt |
| --- | --- | --- |
| Clean complete-singleton erasure | 19/32 | 377/1024 |
| Which-codeword record retained | 19/32 | 377/8192 |
| Exact error weight retained | 19/32 | 157/1024 |
| Exact error support retained | 19/32 | 43/1024 |
| Source phases stripped | 19/32 | 41/1024 |

These are proof regression fixtures, NOT toy-oracle candidates, practical
quantum experiments, or finite speedup evidence. The evaluator deliberately
rejects q^N>4096 or q^(N+K)>131072; its exhaustive decoder cannot be used in
the asymptotic receiver. The independent implementation can be compared to
the older finite-control artifact when public moduli and inputs match.

## Constructive Variant: Keep The Entire Bounded List

This local composition uses standard reversible lookup and Hadamard gates;
no novelty claim is made. It is different from silently treating the first
list entry as the correct message, and different from discarding a record.

Let B={e:wt(e)<=w}. Suppose a deterministic polynomial-time decoder returns
the COMPLETE radius-w message list L(z), of size at most Lmax for EVERY z.
Choose a PUBLIC fixed power of two P with Lmax<=P<2Lmax, capped by M when
necessary. For the RS case with a=N-w and a^2>N(K-1), use

    Lmax = min(M, floor(N*(a-K+1)/(a^2-N(K-1)))).

Pad L(z) to exactly P DISTINCT messages by appending the smallest unused
message labels. Checking labels0..P-1 suffices to find enough fillers; this
does not scan all M messages. Actual list entries and padding are never
measured. P must not depend on z or on the list length observed in a branch.

After the weight-threshold projection and z=e+Enc(m), the original message m
is certainly in L(z). Coherently invert the padded lookup to its index j,
clean the original message with that lookup, then apply H^log2(P) to j.
Project only onto index0, and uncompute the list/lookup workspace from z.
All P Hadamard outcomes are included in the reference probability ledger.
Since every listed message has amplitude1/sqrt(P) on index0, the accepted
UNNORMALIZED state is exactly

    h = A(1_B a) / sqrt(P).

An explicit unitary construction is to prepare the uniform index j, compute
its padded message, erase j by inverse lookup, and swap registers. Reversing
this preparation and projecting all its work onto zero gives the required
bra. On listed inputs the inverse lookup has no ambiguity. Off-list branches
can have any reversible extension; the weight-filtered state has none of
them when the list is complete. The preparation and its inverse use time
polynomial in P, nK and the complete decoder cost. All phases on the accepted
index0 branch are positive, so the signed source sums are preserved.

The probability charge is 1/P times the squared coherent ball norm, NOT
free normalization and NOT a worst-case 1/M field/code enumeration penalty.
With fixed Johnson margin, P is constant. A polynomial P would still permit
a polynomial expected runtime when the success bound below is informative.
If no polynomial list cap is available, using P=M is physically valid but
can have exponentially small success; the reference labels that regime.

### Success Without An Ambiguity Estimate

For a balanced product source, let delta=Pr[wt(e)>w], the same Bin(N,1/2)
tail as before. Let eta bound the support-mask norm error. The positive MDS
enumerator from INVERSE_TRACE_GIBBS_TARGET.md can be reused here, because
the support-mask proof bounds each nonzero codeword contribution by beta^wt:

    eta <= min((q^K-1)*beta^(N-K+1), q^K*(beta+(1-beta)/q)^N).

Let v=Aa, t=A(1_(B complement) a), and g=A(1_B a). Then v=g+t,
||v||^2>=1-eta, ||t||^2<=delta+eta, and v is entirely native-valid.
Writing Pi for the native-valid projector and using
||v||^2 <= 2||Pi g||^2+2||Pi t||^2 gives the rational bounds

    P(native valid AND list projection succeeds)
        >= max(0, (1-2*delta-3*eta)/(2P)),
    P(native INVALID AND list projection succeeds) <= (delta+eta)/P.

There is NO ambiguous-error probability, maximum nonzero-symbol probability,
or unique-decoding assumption in this derivation. A large list or a vacuous
eta is not silently discarded. Verification/restarts retain all failed mass.
The stronger exact-pattern derivation now replaces this triangle estimate:
native success is lambda_b*(1-delta)^2/P, bounded below by
max(0,1-eta)*(1-delta)^2/P. For that identity only a target-fiber lower bound
is needed, not a separate coherent-tail estimate. Source preparation,
complete lists, fixed padding and clean work remain physical requirements.

For the existing inverse-trace n17/31/61 parameters, P=8. The live artifact
records exact outward success lower bounds and a charged128-fresh-attempt
failure bound. This variant does not beat the near-unit sufficient success
of the existing unique-decoding construction on these particular families.
Its research value is removing a proof premise and widening the decoder/source
combinations that can be examined, not an incremental benchmark improvement.
Ordinary RS still imposes the same R<1/4 asymptotic radius restriction here.
Current scalar success floors exceed1/9 and approach1/8. The ideal output
conditioned on native verification is EXACTLY uniform, not merely close to
uniform. The record now retains pattern masses and per-witness probabilities.

### Falsifiers For The New Variant

The independent reference compares the projected branch to the FULL ball
coalescence and accounts for every rejected Hadamard outcome. In the F8
example above, P=2 gives herald25/64 and native success605/2048 per attempt;
the remaining weight-filtered mass19/64 is explicitly rejected by projection.

A separate finite control outside the strict GS regime has no unique branch
at all, yet full-list projection succeeds. Its UNPAID coalesced norm is13/8,
which cannot be a probability. With P=M=16 the actual herald is13/128.
This control tests normalization, not an efficient native solver.

Wrong list completeness, duplicate padding, branch-dependent normalization,
missing 1/P, leftover indices/messages, or measuring the list invalidate the
specified map. Tests check padded non-power-of-two list caps, missing-list
faults, zero singleton mass, every target in the report fixtures, and the
complete probability ledger.

## What Remains A Scientific Blocker

- State-preparation accounting was checked explicitly: a trace hyperplane is
  prepared by binary linear algebra and n-1 Hadamards, followed by reversible
  inv0; a uniform D word uses nK Hadamards and a public linear encoder. Neither
  operation enumerates q or q^K. The field Fourier transform is a trace-basis
  binary linear map plus Hadamards, not an arbitrary amplitude oracle.
- The existing ideal quantum composition has a deterministic polynomial
  route: affine trace-hyperplane preparation, reversible inv0, binary-field
  Fourier transforms, linear encoding, complete deterministic GS and clean
  uncomputation. In the ideal gate model these can use Hadamard and reversible
  classical gates; no arbitrary amplitude or rotation oracle is required.
  A scalable compiled receiver and practical gate count are NOT implemented.
- A costed circuit is engineering work, not a substitute for proving classical
  difficulty. The present audit does not discover a missing gate primitive
  that must be researched before evaluating the mathematical candidate.
- A separate repository review independently reconstructs the proof and
  supplies the exact-pattern identity now checked here. This is not formal
  verification or broader external expert review. Finite channel agreement
  alone cannot establish the asymptotic inequalities.
- A polynomial classical solver for the SAME arbitrary-target relation would
  remove the hoped-for separation. Two special finite inputs already have
  verified classical witnesses; no asymptotic hardness follows from failed
  restricted attacks or from the Gibbs obstruction.
- The native relation is manufactured. No reduction from a standard hard
  problem, cryptanalytic application, or novelty claim is supplied here.

NEXT: prioritize a constructive native classical attack or a meaningful problem
reduction. FOLDED_BALANCED_FILTER.md now supplies a local construction for a
DIFFERENT block-predicate task; it is not an improvement to this scalar input
or an executed native receiver. Do not spend another pass building generic
channel simulators or optimizing mask constants as a proxy for relevance.

Replay:

    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache python -m theorems.balanced_filter_channel_audit --write
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache python -m pytest -q tests/test_balanced_filter_channel_audit.py

The old native-backend integration suite remains unavailable while its source
is dataless. Passing this independent audit must not be reported as that suite
passing. No qsearch/UI, central registry, Git or filesystem relocation work.
