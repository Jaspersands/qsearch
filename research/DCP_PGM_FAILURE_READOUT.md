# Retaining PGM Failures Does Not Rescue The Same Processor

LOCAL DERIVATION / REVIEW PENDING. No novelty, independent review, accepted
algorithm or speedup. This narrows one explicit measurement architecture;
arbitrary terminal collective measurements and other encodings remain open.

## Why This Was The Next Question

The [projected-encoding audit](DCP_PGM_PROJECTED_ENCODING.md) bounded decoding
from the successful block, not all failed branches. Discarding failures is an
obvious weakness in an algorithm audit. Here every signal and auxiliary outcome
is kept, and the optimal classical decoder of that COMPLETE record is allowed.

The result is not a new algorithm. It removes generic projector-phase processing
with ordinary label readout from the list of unconstructed breakthrough
primitives. A genuinely different terminal measurement is still a real debt.

## The Full Raw Channel Is A Legal Local Baseline

Use q=2^L,G=q^n,N=2^m, public IID A and uniform independent secret u. The
supplied state is |psi_u>=N^-1/2 sum_x chi_u(A*x)|x>, x Boolean. The known
comparison unitary U prepares a uniform candidate r, applies its controlled
inverse public phase and Hadamards on the phase register. Read BOTH r and the
entire phase-register bit string y, including y!=0:

    Pr(r,y|u,A) = (1/G)*product_i
       [1+(-1)^y_i*cos(2*pi*<a_i,u-r>/q)]/2.

Because the trial-controlled phase is diagonal in r, measuring r first commutes
with it. Thus the complete channel is operationally identical to choosing a
uniform PUBLIC random trial r, applying its known local correction to each
supplied qubit and measuring each qubit individually. No secret oracle, state
clone or chosen native label appears. Unlimited classical processing of r,y
does not create a collective-measurement advantage.

This is a reduction to a LEGAL measured-data baseline, not a classical method
to synthesize or recover the unknown quantum input from public A. The bounded
compiler knows u only to verify probabilities; it supplies no classical decoder.

## The Processor Class, Including Coherent Auxiliary Memory

In the common output Hilbert space put

    P=U*Pi_in*U^dagger, Pi_in projects the candidate register onto zero,
    Q=Pi_out, projecting the phase register onto zero.

Start with v_u=U(|0>|psi_u>), which lies in P. Attach arbitrary known auxiliary
registers independent of u. The permitted processors are finite sequences of:

- Arbitrary auxiliary-only unitary gates.
- P-controlled auxiliary gates P tensor V+(I-P) tensor W.
- Q-controlled auxiliary gates Q tensor V+(I-Q) tensor W.

All V,W may depend on the ENTIRE A. They can coherently control later steps
using stored auxiliary history. There may be arbitrarily many P and auxiliary
gates, but at most k Q gates. QSP-like scalar projector phases and ordinary
known-reflection amplification are special cases. P is implemented using the
KNOWN U and its inverse; no unknown input-preparation inverse is supplied.

The terminal signal measurement reads the candidate AND phase registers in
the computational basis. Auxiliary records may also be retained and measured;
any classical guess from the complete record is allowed. More generally a
known local phase-register POVM conditional on the classical candidate/auxiliary
coins has the same baseline reduction, but the present compiler tests the
computational readout. No intervening arbitrary data gates or terminal
entangled signal measurement are granted by this theorem.

## A Source-Linked Hybrid Instead Of A Postselection Bound

For the clean input define

    h_A = ||Q*v_u||^2 = sum_t eta_t^2/N^2,
    eta_t = |{x:A*x=t}|.

It is independent of u. Replace every Q-controlled gate by I tensor W,
leaving all P-controlled and auxiliary gates in place. In this REFERENCE
execution the signal remains v_u throughout: every P gate acts only on the
auxiliary state. The reference auxiliary state may depend on A but not u.

A removed Q gate changes a reference prefix by

    Q*v_u tensor (V-W)|aux>,

whose norm is at most 2*sqrt(h_A). Telescope using actual suffix unitaries
and reference prefixes. For the entire final PURE state, INCLUDING failure
and auxiliary registers,

    ||actual-reference|| <= 2*k*sqrt(h_A).

Trace distance is no larger than this norm, and measurement cannot increase
trace distance. Therefore optimal complete-record uniform-secret correctness
obeys the common, fixed-A bound

    P_processor(A) <= P_local_reference(A)+2*k*sqrt(h_A), capped at 1.

The input-state-dependent prefix argument matters: the operator-norm distance
of a Q gate from its replacement can be 2. Do not claim a small norm for that
gate on arbitrary inputs. No minimum singular value or hypothetical fast PGM
inverse is used. The reasoning is the standard unitary hybrid pattern, exemplified
by [BBBV Theorem3.3](https://arxiv.org/html/quant-ph/9701001v1), applied here to
this supplied-state architecture. Their random-oracle lower bounds are NOT
being transferred to the native algebraic problem.

## Native Mean And Simultaneous Label Gate

Let H=(q/2)^n, C=(3/2)^m. The preceding native product-POVM theorem gives

    B = min(1, [C+(N-C)/H]/G),
    E_A[P_local_reference(A)^2] <= B.

The exact native fiber moments give E_A h_A=(N+G-1)/(N*G). Jensen yields

    E_A P_processor <= min(1, sqrt(B)+2*k*sqrt((N+G-1)/(N*G))).

These gates are simultaneous over A-dependent allowed schedules, auxiliary
circuits and record decoders: the fixed-A envelope does not depend on their
choices. Squaring the fixed-A bound before averaging gives

    E_A[P_processor(A)^2] <= min(1,2*B+8*k^2*(N+G-1)/(N*G)).

Consequently Markov bounds the probability that ANY processor in this class
has conditional uniform-secret correctness >=delta by that common expression
divided by delta^2, capped at 1. This is not a pointwise-secret theorem.
Arbitrarily many fresh input batches or selecting favorable labels needs a
separate source/input-count ledger, not a silent change of A's distribution.

The repository's [structured EDCP/RLWE small-secret lanes](STRUCTURED_EDCP_SOURCE_HARDNESS_AUDIT.md)
have different priors. This full-group uniform-secret screen does NOT establish
hardness for those natural promises or for secret-correlated public side data.
Their prior-aware decoder is a separate target, not a loophole closed by this
calculation. Any public label normalization must also push its prior forward.

At n=8,16,32,L=4n+1,m=nL+16,k=(nL+m)^2, exact conservative dyadic sums
give mean-success upper exponents49,210,850. The local-reference term dominates;
the projector processing adds exponentially little information despite keeping
every failed output. The q2 binary-width and excessive-sample regimes explicitly
remain vacuous. No high-sample local-readout algorithm is excluded.

## Correlated Physical Phase Faults: A Limited Robust Extension

For an arbitrary Z mask z, the amplitudes retain equal magnitudes. In each
fiber put eta_(z,t)=sum_(x:A*x=t)(-1)^(z*x). Then

    ||Q*U(|0>|psi_(u,z)>)||^2
       = sum_t |eta_(z,t)|^2/N^2 <= h_A.

This pointwise herald inequality does not require z to be random. A classical
mixture of such faults has the same upper bound. Purify the entire joint mask
law to extend the hybrid argument without discarding correlations.

For the LOCAL baseline source gate, however, the joint mask law must be
independent of u conditional on A. It may depend on A and have arbitrary
correlations across physical qubits. Revealing the mask only strengthens the
reference baseline; each revealed mask rotates its local POVMs, still covered
by the common product gate. This is why label dependence alone is not a breach.

Secret-dependent faults can encode extra secret data, so that source gate
cannot be borrowed in that setting. Neither a static mask schema nor numerical
agreement PROVES that an external reduction supplies an independent fault law.
General basis failures, non-flat noise and actual lattice-source composition
are not handled merely by naming them phase faults.

## Precision Floor And Attempts To Break The Claim

If a separately proved total output trace-error budget is epsilon, add epsilon
to the IDEAL mean-success upper bound. The certificate accepts an exact composed
budget, not an unverified per-gate error. Its squared/typical-label gate is
explicitly for ideal operations. At epsilon=10^-6 the claimed physical upper
bound has an inverse-polynomial error floor, not exponential precision. The
zero default denotes an ideal theorem, NOT an implemented exact circuit.

Positive small control: q4,A=(2,1), one amplification round improves complete
record correctness from3/4 to1. The source-mean native gate does not reject
this allowed fixed instance; its fixed-A hybrid bound is loose there.

Universal-claim counterexample: q2,A=I can be decoded by direct Hadamards,
or by undoing U then applying the data Hadamards. Those data gates are OUTSIDE
the projector/auxiliary algebra. An arbitrary final collective measurement
can in principle decode the original information in U's reversible output;
the hybrid bound merely compares it to the SAME measurement on the reference.
If the reference decoder itself is collective, the local source bound is gone.

Failure of the proposed falsifier would be any allowed full channel exceeding
the hybrid/common source gate, a fault law with untracked secret correlation,
a source-selected batch falsely called IID, or a terminal measurement covertly
changed to an entangled one. Retain these model distinctions in registry entries.

## Verification And Research Action

Module/test stem: `dcp_pgm_failure_readout`. Report under classical_baselines;
independent-language structured-unitary checker under certificates. The bounded
suite covers45 processors/source laws and700 pure unknown-input executions.
Every raw probability is checked against the operational local baseline;
every failure and auxiliary bit is retained. Optimal finite classifiers and
full unitaries are EXPONENTIAL calibration, not scalable implementations.

The projector formalism is sourced in
[QSVT Sections2/3.2](https://arxiv.org/html/1806.01838); the native all-record
hybrid/local-baseline application is derived here and awaits independent review.

STOP optimizing only phase schedules, auxiliary memory or failure-label
classifiers in this architecture. A candidate must supply a different terminal
collective primitive, changed costed signal representation, charged additional
input strategy or another genuinely outside-class operation. The direct verified
witness filter remains outside this class but still lacks its native finder.
Gemini owns production CLI/registry/full-validation integration; no candidate is
promoted from these audits.
