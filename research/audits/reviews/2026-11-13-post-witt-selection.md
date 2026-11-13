# Post-Witt selection: native one-pulse Kerr CDF compilation

13 November 2026. Independent selection, not a new algorithm theorem.
STATE/TRAPS/GOAL read. Balanced expanded Witt is closed at its written scope;
no further field variant is selected. No network, API, Git, numerical tests,
archive reads, or shared-note edits were used in this pass.

## Decision and comparison boundary

Select one concrete classical attack on an already complete quantum endpoint:
**compile the coherent photon-count CDF for one binary-large Kerr pulse.**
The new operation is a Christoffel–Darboux/displacement reduction of the
number-prefix projector, followed by a possible certified theta-sum compiler.
It retains the off-diagonal interference which a phase-density pushforward loses.
This is preferable to another quantum access primitive: success would settle
the SAME full sampling law, while failure can identify a precise analytic cost.
No speedup, novelty, hardness, or classical match is asserted.

Three independent mechanisms were compared: compressed bosonic interference,
isogeny class actions, and topological braid evaluation. The latter two have
high external value, but the operations available here do not yet improve their
known mechanisms. They are rejected as next tasks, not declared impossible.

Corpus `been-tried` and `baselines` were run for:
- `one pulse binary Fock Kerr theta Krawtchouk`;
- `supersingular isogeny quantum walk nonbacktracking`, followed by the
  more specific `ordinary elliptic curve isogeny class group vectorization hidden shift`;
- `Jones polynomial plat closure link invariant normalization`.
Most hits were lexical and unrelated. No baseline-catalog hit for Kerr/Jones
is NOT evidence of absent classical algorithms. An additional shadow-Hamiltonian
comparison was discarded: the retained compendium itself requires a native
initial shadow state and invariant operator space, and notes the fixed-dimensional
light-cone limitation (physical LF2419–2501). That offers no new operation here.

## A. Selected: exact-law one-pulse Kerr sampling

**Native contract.** Binary K, two explicitly supplied rational-turn beam-splitter
angles theta1/theta2, an exact rational Kerr phase a/b, and TV tolerance epsilon.
Start at |K,0>; apply B(theta1), exp(2 pi i (a/b) binom(N,2)), B(theta2);
output the count j in {0,...,K}. Charge all angle bits, log(K+1), output bits,
and the requested error. No loss, smoothing, hidden repeat count, or phase oracle.
The complete quantum target poly(native bits,log(K+1),log(1/epsilon)) is already
written prior art, not the proposed contribution.

Actual retained primary statements read: Prakash et al., `binary_fock_kerr/prakash.txt`
LF844–898, Theorem2.2/Corollary2.3; Iyer et al., `iyer.txt` LF1363–1395,
Theorem4.2 including coherent Hermite phases and label cleanup. The native
cutoff/error composition is in `BINARY_FOCK_KERR_SAMPLING.md`.

**Strongest matched classical attacks.** Passive/bunched circuits are binomial;
terminal Kerr does not affect counts. The written coherent-branch sampler handles
one pulse in time polynomial in the NUMERICAL period 2b, and handles several
pulses in their product period. It already retains interference and finite-bit
clocks. Direct K+1 dimensional evolution and small tensor width remain valid.
Thus only genuinely large denominators/occupations need a new operation.
Rational approximation by itself does not remove numerical branch count.

### Exact reduction, independently derived

Let U be the real orthogonal number-basis matrix of B(theta2),
N=diag(0,...,K), Pi_r=diag(1_{j<=r}), P_r=U^T Pi_r U, and
w_n=exp(2 pi i (a/b) binom(n,2)) (B(theta1))_{n,K}.
The desired CDF is exactly F(r)=w^*P_r w. Put T=U N U^T.
The spin rotation gives a tridiagonal T; its adjacent entries have absolute
value |sin(theta2)cos(theta2)| sqrt((n+1)(K-n)). Its signs are fixed by U.
For 0<=r<K put t_r=T[r,r+1], u=U^T e_r, v=U^T e_{r+1}. Then

    [N,P_r] = U^T[T,Pi_r]U = t_r (v u^T-u v^T),
    P_r[n,m] = t_r (v_n u_m-u_n v_m)/(n-m),  n!=m.

This follows by multiplying the matrices: only the two entries crossing the
prefix boundary survive [T,Pi_r]. It is an exact identity at every K, angle,
phase, and prefix. P_K=I and P_{-1}=0 are separate exact endpoints.
The projector generally has rank r+1: **rank-two displacement is not low rank.**
When t_r=0 the rotated number measurement is diagonal/permuted and is elementary.

Hence a CDF evaluation consists of its diagonal contribution plus the explicit
bilinear Cauchy-kernel sum

    t_r sum_{n!=m} conjugate(w_n) w_m
                     (v_n u_m-u_n v_m)/(n-m).

The diagonal is NOT supplied by the commutator identity. In a Krawtchouk
polynomial normalization it is the confluent CD limit, involving derivatives;
its numerical compiler must be paid along with the off-diagonal expression.
The exact identity 1/h=(1/(2 pi)) integral_0^{2 pi} i(s-pi) exp(i h s) ds
for nonzero integer h turns the latter into a bilinear Fourier integral.
This is a useful target for a theta compiler, not an efficient quadrature proof.

### Why this operation would give the actual sampler

Suppose a deterministic compiler returns every F(r) to absolute error delta in
poly(log(K+1), angle bits, log(1/delta)) bit operations, uniformly in r.
Choose delta=epsilon/[8(K+1)] and a B-bit uniform variate with
2^-B<=epsilon/[8(K+1)]. Binary-search its quantile using these CDF values.
Couple with an exact uniform real variate. Unless that variate lies within
delta+2^-B of one of the K+1 true CDF boundaries, every comparison agrees with
the exact search. The bad set has measure at most
2(K+1)(delta+2^-B)<=epsilon/2. There are only ceil(log2(K+1))+1 queries.
No monotonicity of the approximations is needed on this good event.
This proves a fixed-clock TV sampler from that compiler; allocate any compiler
failure probability separately. Merely computing F to O(epsilon) gives a
Kolmogorov guarantee and does NOT establish TV sampling. The needed precision
still has only O(log(K+1)+log(1/epsilon)) bits.

### New source and exact remaining obligation

Actual Hiary, Annals2011, retained `2026-11-13-one-pulse/hiary_theta.txt`
LF62–95, Theorem1.1, computes
K^-j sum_{k=0}^K k^j exp(2 pi i (alpha k+beta k^2)) for REAL alpha,beta mod1.
Its arithmetic count and operand bits are polynomial in
(j+1)log(K/eta), with a stated polynomial prefactor in the error.
This really can remove numerical quadratic-sum length. It does NOT directly
cover Gaussian damping, Krawtchouk weights, the CD diagonal, or the bilinear
1/(n-m) expression. Those must be reduced to its actual input format.

The proposed constructive test is therefore precise: central binomial tail
control plus certified polynomial/oscillatory expansions of the two boundary
Krawtchouk functions, including their turning points, reducing BOTH CD pieces
to polynomially many Hiary calls and explicitly controlled bilinear integrals.
The number of pieces, polynomial degrees, coefficient sizes, cancellations,
precision and integration clocks must be polynomial in the charged parameters.
Growing K^c piece count, or an exponentially small normalization, defeats this
proposed compiler even though individual theta sums are fast.

The parent's modular continuous-theta rejection envelope is a possible
alternative subroutine. Even a proved constant rejection envelope there leaves
the native number-measurement kernel unpaid. It may be used in a coherent
two-branch envelope retaining the cross term; it may not replace amplitudes
by an incoherent phase mixture.

**Cheapest decisive stress cases.** Include balanced initial/readout rotations,
prefixes crossing a Krawtchouk turning point, and rational phases arbitrarily
near low-denominator revivals. The period-four Kerr cat has two opposite
equatorial condensates: a final O(1/K) rotation about their axis can change
their relative phase by O(1), hence count parity. A smooth phase-intensity
pushforward alone misses precisely this coherence. The existing branch method
handles the rational revival; a claimed uniform compiler must match it and
nearby phases without requiring numerical b or K work. Finite success would
not prove the uniform bounds; the exact CD identity is the starting certificate.

## B. Not selected: polynomial-time native isogeny vectorization

**Problem/value.** Public ordinary curves in a specified common-order class-action
instance; recover a verified connecting isogeny as a polynomial-size sequence
of small-degree maps. Any supplied order/action data must be part of the native
cryptographic contract, not hidden End/Hom advice. This concerns post-quantum
cryptography, independently of Kerr or quadratic-form transport.
**Proposed operation.** Compile a class/ideal description into a coherently
evaluable short smooth isogeny word, then exploit hidden translation.
**Goal/resources.** Poly(log q, public input,log(1/eta)) total time, including
class-group data, action evaluation, all walk steps and the actual output maps.
**Baseline/obligation.** The retained compendium LF993–1041 explicitly gives
only subexponential hidden-shift attacks, not a polynomial method. Efficient
action evaluation alone does not improve the hidden-shift measurement. A
binary exponent in a small-prime action is not a polylog-time isogeny walk.
Classical collision/smoothing attacks must be compared under the same order,
torsion data and output contract; SIDH breaks do not settle other contracts.
**Cheapest falsifier.** Count actual small-prime steps and source-state cost
before invoking an HSP clock; a superpolynomial word or untouched Kuperberg
stage rejects this proposed full clock. No new remedy for either is supplied.
Actual Childs–Jao–Soukharev (J. Math. Cryptology8,2014) is NOT retained/read here;
the compendium is a comparison lead, not a substitute primary theorem audit.
Do not fetch it merely to repeat a known hidden-shift wrapper.

## C. Not selected: native-scale Jones discrimination

**Problem/value.** Explicit braid word, nonexceptional fixed root of unity,
and additive inverse-polynomial accuracy for the ORIGINAL Jones value of its
trace closure. This is a topological invariant problem, not circuit acceptance
renamed as an application. Input crossings, strands and accuracy are charged.
**Proposed operation.** Coherent tangle/cap elimination with normalization
bookkeeping that avoids the exponentially scaled trace-accuracy requirement.
**Goal/resources.** Poly(crossings,strands,1/epsilon), including any postselection,
scalar normalizers, state preparation and finite-gate error.
**Baseline/obligation.** Skein contraction and bounded-width tensor/path-space
methods are the strongest immediate classical attacks on structured braids.
The compendium LF2999–3073 describes the known quantum approximation with
error epsilon |d|^(n-1) for trace closure, |d|=2cos(pi/k). This does not pay the
native-scale task. Its BQP/DQC1 statements do not fix this mismatch.
**Cheapest falsifier.** Repeated Markov stabilizations present the unknot with
growing strand count: its Jones value stays1 while its normalized trace has
magnitude |d|^(1-n). Thus a blanket inverse-polynomial normalized-signal premise
already fails on an easy family. This is not a lower bound for other algorithms.
No unitary normalization operation overcoming the cost is provided here.
Actual Aharonov–Jones–Landau primary source would be required before a new
normalization claim; the old local braid-HSP note's broad barriers are not used.

## Single next action and source needs

Attempt the native Kerr CDF compiler above, with two independent obligations:
construct a bounded representation of the full CD quadratic form, and attack
its uniform precision/turning-point/near-revival cost. Hiary's actual primary
text is already available. The useful remaining primary source is a complete
uniform Krawtchouk asymptotic/error theorem (including endpoint/coalescing saddles
and derivatives), or a direct derivation replacing it. An unread abstract or
the ordinary bulk two-saddle formula is insufficient. Do not start a quantum
implementation, benchmark sweep, or another arithmetic extension. A positive
result must output the native count law; a negative result must identify the
specific failed representation/clock and leave the full law unmatched.
