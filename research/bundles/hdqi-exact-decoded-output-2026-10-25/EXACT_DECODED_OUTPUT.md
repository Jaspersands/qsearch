# Exact Transfer Pilots: The Actual Decoded Output

2026-10-25. Local, unreviewed composition and exact implementation. No
novelty, best-known bound or quantum-speedup claim. This pass closes a
specific gap left by the ECF pilot sampler: a classical pilot sample is NOT
automatically a sample of the actual physical HDQI output.

## Decision And What Changed

The preceding full-output rejection method required a bound on
C=Z_commuting/Z_pilot and noisy estimates of word signs. The new exact
transfer representation instead supplies both samples and unnormalized
amplitudes. This removes C entirely from two matched classical baselines:

1. Full joint physical computational output: expected 2^k trials, each
   using one exact pilot sample and at most 2^k exact amplitudes, where
   k=rank(B)-rank(X). All retained/rejected trials and decoder calls are paid.
2. Any specified physical Pauli expectation: an exact importance variable
   with second moment <=1, regardless of k or C. Median-of-means gives a
   finite accuracy/failure budget with no empirical denominator estimate.

The sample/amplitude access is CONSTRUCTED by signed tree contractions,
not supplied as a quantum or classical oracle. Costs remain exponential
in transfer-factor count and bag independence. The general ECF thermal
composition inherits the previous unreviewed quasipolynomial upper-bound
argument, not a completed thermal root compiler or a practical sampler.

This is an instance of established computationally tractable-state methods:
[Van den Nest, Theorems 1 and 3](https://arxiv.org/html/0911.1624) combine
sampling/amplitude access with efficiently computable sparse pullbacks.
The partial-permutation pullback and interference fibers already appear
in this repository's preceding decoded-observable/output notes. The new
work composes them with exact complex transfer access and tests the SAME
physical law; it is not a claim to have invented that simulation paradigm.

## 1. The Actual Physical Target

Input is an explicit list of Hermitian physical Paulis P_i on n qubits,
rational nonzero |J_i|<=1, and a total deterministic classical decoder Dec
whose runtime is charged. Let B=[X;Z] map an m-bit word to its physical
binary Pauli label. The physical and canonical generators have the same
anticommutation graph. Use the exact finite-transfer pilot

    |a> = sum_y a_y |y> / sqrt(S),    S=sum_y |a_y|^2 > 0.

Coupling signs are ALREADY included in a_y. Define the ordered physical
product P(y)=P_0^y_0 ... P_(m-1)^y_(m-1) and R(y)=y xor Dec(By).
The target output is

    |Psi> = sum_y a_y |R(y)> |P(y)> / sqrt(S),
    |P> = (P tensor I)|Bell_n>.

This is the actual HDQI construction, not a Bell-label pushforward; compare
[Hastings--Schmidhuber, Section II, Eq. 12](https://arxiv.org/html/2610.03697v1).
It is well-defined even for an unsuccessful decoder. It is NOT automatically
a Gibbs preparation: that requires separate pilot and decoder guarantees.

The map |y> -> |R(y)>|P(y)> is an isometry. Equal Bell labels imply By=By';
if residues also agree then y xor Dec(By)=y' xor Dec(By), hence y=y'.
Physical product phases do not change this orthogonality argument. This
retains all residues, including decoding failures; there is no postselection
onto a supposedly good decoder branch.

The finite-product code reuses the prior Physical record for its explicit
Pauli/graph arithmetic. That record has beta metadata in [0,1], but this
pass does not derive a thermal approximation from it. Actual finite factors
are the input, and the Gibbs/thermal certification flags stay false.

## 2. Construct Amplitudes, Do Not Assume Them

For L transfer factors, reuse the signed edge expansion and verified tree
decomposition from the ECF tree bundle. A SINGLE-copy contraction fixes
the XOR selection parity at each vertex to the requested y_i. Each bag
stores L independent subsets, with the same layer/vertex crossing signs.
It computes a_y exactly over Gaussian rationals. It does not take a square
root of |a_y|^2: doing that would erase phase information.

For bag independence <=h, this costs poly(m,B,L)*(m+1)^(hL) arithmetic
operations, with polynomial coefficient bit lengths. The existing two-copy
sampler costs poly(m,B,L)*(m+1)^(2hL). Its normalization is computed by the
same exact contraction; no amplitude table or statevector is an input.
The new adapter checks that the physical input, couplings, and pilot graph
match. Both dense reference paths are capped and excluded from production.

## 3. Exact Full-Output Rejection Without An Average-Sign Bound

For a residue r and X-syndrome u, let

    F(r,u) = {y: R(y)=r, Xy=u},   Fbar = 2^k,
    k = rank(B)-rank(X) = dim Z(ker X).

Words in a fiber have distinct full B syndromes. Enumerate the pure-Z
subspace im(B) intersect ({0} x F_2^n) by public binary linear algebra.
Given representative y0, set r=R(y0), s0=By0. For each pure-Z offset h,
compute y=r xor Dec(s0 xor (0,h)) and KEEP it only if By=s0 xor (0,h).
This lists the exact fiber with Fbar forward decoder calls; no decoder
inverse, hidden witness or classical search oracle is used. The existing
fiber implementation is reused, not replaced by a new relation.

Write P(y)=i^p_y X^x_y Z^z_y and

    theta_y(b)=i^p_y (-1)^(z_y dot b),
    Q_F=sum_(y in F) |a_y|^2,
    A_F(b)=sum_(y in F) a_y theta_y(b).

A trial samples y0 with probability |a_y0|^2/S and b uniformly from n bits,
then proposes event (r, a=b xor Xy0, b). Its probability is Q_F/(2^n S).
The target event probability is |A_F(b)|^2/(2^n S). By Cauchy--Schwarz,

    |A_F(b)|^2 <= |F| Q_F <= Fbar Q_F.

Accept with the EXACT rational probability

    |A_F(b)|^2 / (Fbar Q_F).

The accepted mass of every event is exactly its target mass divided by
Fbar. Isometry gives total target mass one, so success per trial is exactly
1/Fbar, not a lower bound containing C. Every successful sample has the
exact target distribution. Zero-probability fibers cannot be sampled;
zero-amplitude labels inside a nonzero fiber are retained harmlessly.
Complex phases and negative couplings are not replaced by sign magnitudes.

Cap trials at Fbar*r, with r=ceil(log2(1/delta)). Then the abort probability
is at most exp(-r)<=2^-r<=delta. Return explicit FAILURE after the cap;
do not manufacture a sample or silently discard failure from the experiment.
Successful outcomes are exact; the unconditional law including abort is
within delta TV of the intended no-abort law.

Let T_s be pilot sampling cost, T_a amplitude cost and T_D decoder cost.
Expected work is bounded by

    Fbar * [T_s + Fbar*(T_a + T_D + poly(m,n))].

The capped version adds O(log(1/delta)). The rank bound and the workload
cap are computed before fiber enumeration. Large k is not a hardness
certificate: independent commuting Z terms have large k and are already
handled by the prior polynomial commuting-linear shortcut.

## 4. Pauli Expectations Without ANY Fiber Enumeration

Let Q be a specified Hermitian physical Pauli with binary label q. A
nonzero matrix element between y and t requires Bt=By xor q and equal
residues. There is at most one possible partner:

    t(y)=y xor Dec(By) xor Dec(By xor q).

Reject the row if Bt(y) != By xor q. Otherwise compute the full complex
phase omega_y=tau(P(t(y))^dagger Q P(y)) in {1,-1,i,-i}.
On valid rows t is an involution, and thus injective. None of this requires
the decoder to succeed on the pilot distribution.

Sample y from |a_y|^2/S and return

    W(y)=Re[omega_y * conjugate(a_t)/conjugate(a_y)],

with zero on invalid rows. Sampled a_y is nonzero. Then

    E W = <Psi|Q_left|Psi>,
    E W^2 <= sum_valid_y |a_t|^2/S <= 1.

This estimates the actual decoded expectation, not a pilot marginal or a
surrogate sign moment. It uses two exact amplitudes, two decoder calls and
one pilot sample per draw. Taking Re(omega_y) BEFORE multiplying amplitudes
is wrong for complex pilots, even though it was valid in the predecessor's
real-sign setting. A specific exact control has a nonzero physical result
that is lost by that shortcut. The frozen predecessor is not reinterpreted
as a complex-amplitude algorithm.

Weights can be huge on rare words. They are kept exact, not clipped. Their
bit length remains polynomial because all amplitudes are Gaussian rational
contractions of bounded-bit inputs. Tiny nonzero amplitudes can have small
probability without requiring an exponentially long binary representation.

For accuracy epsilon, use b=ceil(4/epsilon^2) draws per block. Chebyshev
bounds a block's error probability by 1/4. With g=8*r+1 blocks and
r=ceil(log2(1/delta)), Hoeffding on the independent bad-block indicators
bounds median failure by exp(-g/8)<delta. Only the FINAL median is clipped
to [-1,1], which cannot increase error relative to a true Pauli expectation.
Insufficient draw budget returns no certified estimate. Independent random
bits are a premise; seeded replay is not evidence proving that premise.

Polynomial lists or weighted Pauli sums can be handled with explicit
accuracy allocation, or coefficient-weighted term sampling. Charge the
coefficient L1 norm relative to absolute requested accuracy; total energy
and energy density are different tasks. No generic non-Pauli readout or
arbitrary extra quantum computation is covered by this sparse pullback.

## 5. Approximation Transfer And The ECF Consequence

If a certified finite-transfer pilot is within vector distance eta of the
intended thermal pilot, applying the SAME decoder isometry preserves that
distance. Measurement TV is at most eta; Pauli expectation error is at most
2eta. These compare the completed output states, NOT individual proposal
probabilities, so no factor 2^k multiplies eta. Rejection's capped abort adds
delta to the sampling TV bound. Estimator sampling error adds separately.
Gibbs approximation errors, if proved, are a further separate term.

For all ECF graphs, the previous local argument gives h<=2 and
L=O(log^2 N) at polynomial beta and inverse error in explicit input length
N. Thus physical Pauli expectations admit a proposed quasipolynomial
classical algorithm for ANY efficiently computable total decoder, without
a sign bound or a small-k assumption. Full actual output has that same
quasipolynomial type of bound when k is polylogarithmic in N; k=O(log N)
adds only a polynomial fiber overhead. For constant L,h and logarithmic k,
the finite-transfer full-output algorithm is polynomial.

This is not a uniform polynomial ECF thermal algorithm, a thermal compiler
execution, a correctness guarantee for the physical Gibbs preparation, or
a classical simulation of every coherent downstream operation. The finite
tests do not prove the general thermal/root/graph-decomposition argument.

## 6. Adversarial Outcome And Next Decision

The same-native-output checks include redundant generators, arbitrary bad
decoders, complex amplitudes, Y/product phases, negative couplings, zero
coefficients, huge importance ratios, exact abort behavior and all finite
output events. The physical reference applies each Pauli directly to basis
states, rather than reusing the production ordered-phase formula.

The broader output analysis removes a potential escape route for the ECF
candidate: neither bad decoder residues nor an unfavorable sign-envelope
ratio alone defeat this baseline. The remaining large-k full-sampling gap
does NOT restore an energy/Pauli-observable advantage, since that attack is
independent of k. No current input supplies a credible major separation.

Next reasoning pass should pivot to a concrete native source/reduction with
an explicitly useful output, not add another ECF geometry, observable list,
or marginal simulator. The general high-interference-rank output remains
open but needs a useful task and constructive quantum input preparation
before receiving another pass. Mechanical integration is in HANDOFF.md.
