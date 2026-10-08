# Next: Direct Approximate Native Quantum Input From Noisy Linear Values

Status: SUPERSEDED by the implemented, independently replayed
[copy-only input bridge](NATIVE_NOISY_PHASE_INPUT.md). Its report is
`reductions/native_noisy_phase_input.json`, producer is
`theorems/native_noisy_phase_input.py`, and the matching JS checker and tests
exist. It supplies gate recipes and a sharper20V/q^2 averaged trace bound,
not hardware execution or an efficient receiver. The text below preserves
the ORIGINAL proposal, not the current implementation's proof status.
The classical noise-degradation subsystem is complete at its stated scope,
but its forward convolution does not itself supply unknown quantum states.
A different, potentially higher-leverage construction may do so approximately.

## Construction To Verify

Given TWO independent classical noisy linear records

    b=<a,s>+E1 mod q, d=<c,s>+E2 mod q,

their VALUES are known to the reduction, though s and E1,E2 are unknown.
Prepare F3|0> and apply diag(1,omega^b,omega^d). No unknown phase oracle
is needed: b,d are public classical numbers and the local gates are known.
The native decoder receives ONLY the resulting qutrit and the original a,c,
not b,d or the reduction-side preparation inverse. A public mask can first
uniformize the secret as in the implemented classical source reduction.

For symmetric independent errors with phi=E cos(2*pi*E/q), the average
error-dephased qutrit density, in the ideal phase frame, should be

    rho_phi=(1/3)[[1,phi,phi],
                 [phi,1,phi^2],
                 [phi,phi^2,1]].

The ideal density has every entry1/3. Decompose their difference into three
Hermitian off-diagonal two-dimensional blocks. Each block's trace norm is
twice the absolute coefficient. Triangle inequality would give

    trace_distance(rho_phi,rho_ideal)
        <=[2(1-phi)+(1-phi^2)]/3 <=80V/(3q^2),

capped at1. This is an AVERAGED density bound, not the stronger false claim
that every noisy pure realization is that close. Product-source telescoping
would charge M times this plus source-rounding and actual gate errors.

## Actual Native Source Match

The existing `cyclotomic_fiber_receiver.frequency_matrix/inverse_frequency_coordinates`
already verifies even native level2r has a bijection between ring labels and
IID frequency pairs a,c in (Z/q)^n. Determinant=-1 is essential. Check this
map in the new input recipe, so the bridge supplies the ORIGINAL even native
source for integer-embedded secrets, not just a nominal three-amplitude state.
Odd levels have a frequency constraint and cannot silently inherit this route.
The source does NOT cover arbitrary full ring secrets merely by declaration.

## Critical Correlation And Access Countercontrols

Do not make unlimited copies from one pair of known b,d and call them IID
native originals. All those copies share E1,E2. For q3 and calibration
chi(0)=1/2,chi(+/-1)=1/4, phi1=phi2=1/4. On two reused copies, a coherence
whose exponent is2E1 has factor1/4, whereas independent originals have
factor(1/4)^2=1/16. The normalized two-qutrit entry differs by1/48.
This provides an exact countercontrol to the reusable-source shortcut.

One disjoint classical pair must be charged per independent native qutrit.
Keeping preparation descriptions reduction-side does not supply an inverse
or reflection about the IDEAL unknown source. Receiver promises involving
such access require separate proofs and cannot inherit a copy-only bridge.
Receiver postselection does not erase global trace/abort errors: conditional
errors may grow by inverse acceptance probability.

## Required Implementation

1. A secret-blind typed preparation recipe over known b,d, full-root labels,
   and disjoint source IDs, with no q-sized tables or group enumeration.
2. A polynomial-bit even-level frequency-to-native-label compiler or reuse
   the existing exact2x2 map, with explicit scope/caps.
3. Exact averaged density/trace-distance accounting and source-theorem
   profiles reusing the reviewed continuous-Gaussian/rounding convention.
4. Known local F3/diagonal-gate plans with precision-dependent cost. Charge
   EVERY phase/preparation approximation and do not label an unsynthesized
   hardware circuit as implemented.
5. Bounded actual phase-state controls and an independent exact cyclotomic
   checker. Include shared-error two-copy failure and all source access debts.
6. Success transfer for ANY fixed copy-only native receiver through the
   charged input-state trace distance. No receiver is supplied by this bridge.

If correct, a polynomial full-depth native receiver would have a concrete
noisy-linear/lattice problem consequence, not just an oracle benchmark.
It still would NOT be a discovered algorithm. External composition review,
novelty comparison and an efficient receiver remain required.
