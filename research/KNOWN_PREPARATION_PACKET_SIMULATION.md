# Same-Original-Data Simulation Of Measured Phase Compression

LOCAL CONSTRUCTION AND SCOPED DERIVATION / EXTERNAL REVIEW PENDING.
This is an efficient classical counterpart for SPECIFIED measured compression
primitives on the existing classical-data preparation. It is not a universal
no-go for quantum LWE, hidden shift, arbitrary known-input circuits or unknown
quantum-only phase sources.

## The Previously Missing Computational Baseline

`NATIVE_PHASE_SOURCE_DOMINANCE.md` already supplies an original-data Bayes
ceiling, but explicitly does NOT prove efficient classical dequantization.
This pass fills part of that computational gap for a restricted receiver family.

Authoritative `native_noisy_phase_input.prepare_inputs` creates each qutrit
from a pair of original classical noisy-linear records and a known random mask.
Its `reduction_side_recipes` contains the KNOWN two phase values

    v_i = observed_value_i + public_label_i . mask modq.

The actual conditional input is the pure point state

    (|0>+exp(2*pi*i*v_1/q)|1>+exp(2*pi*i*v_2/q)|2>)/sqrt3.

No hidden secret or individual error is needed to compute that vector.
Noise averaging gives the earlier secret-dependent density promise, but a
classical algorithm starting from the SAME ORIGINAL records can condition on
their actual values and simulate the point preparation. The mask is its own
known preparation randomness. Withholding these values from the narrow
quantum receiver interface does not withhold them from a classical competitor
for the original classical problem.

This source distinction is essential. Ordinary HSP/hidden-shift Fourier
sampling can produce phase qubits with genuinely UNKNOWN phase. Their labels
do not reveal that phase to a classical algorithm. This simulator requires
explicit classical preparation access and does not recover phase descriptors
from quantum states, secret guesses or tomography. Such unknown sources are
outside the conclusion.

## Exact Compact Phase State

Represent a known packet by q=3^r, dimension d in{2,3}, and the d integer
phase numerators phi_t modq. Amplitudes are exp(2*pi*i*phi_t/q)/sqrt(d).
Maintain actual paid original-record ancestry. This is a CLASSICAL simulator
descriptor, not a claim that the quantum receiver can read unknown amplitudes.

Known ternary-root diagonal gates add public phase numerators. A label/outcome
policy may adapt; it chooses operations from its allowed PUBLIC history only.
The simulator uses private original values to sample the physical channel,
not to make the quantum controller more powerful.

### Common-Index Qutrit Merge

For a nonempty B-packet block, apply the existing SUM-inverse basis change,
measure offsets v_i=j_i-j_0, and retain only pivot t. For EVERY supplied
uniform-modulus point preparation, the offsets are independent uniform trits.
The retained packet has exact phases

    Phi_t = sum_i phi_i[(t+v_i) mod3] modq.

Its measured branch probability is3^(1-B). Work is O(B) phase additions,
not a3^B state table, and no division by an exponentially tiny branch
probability is used. Global phase is retained in the descriptor. Existing
public label transport/ideal division is separately classical arithmetic;
it does not manufacture missing unknown phase information.

The identity holds for actual noisy point realizations, not only ideal states
with a common hidden-secret character. It therefore simulates the real
prepared quantum experiment before its averaged-noise approximation.

### Projection And Measured Binary Merge

Project a ternary packet onto basis{0,1} at probability2/3. On success retain
the first two phase numerators; on rejection charge and discard its originals.
For two binary packets, CNOT followed by right measurement b has probability
1/2 and retains phases

    Phi_t = phi_left[t] + phi_right[t xor b] modq.

This samples an ACTUAL measured sign. It does not obtain both alternative
children or deterministically request a desired sum/difference. Original
ancestors must be disjoint. The measured steps do not leave entanglement
between the retained packet and untouched independent packets.

Different ternary-power phase moduli can be embedded into their maximum
modulus with exact integer multipliers. State size stays two or three phases;
phase bit length grows polynomially with input description and operations.

## Certified Local Readout, Not Floating Sampling

For inverse_F3, the outcome b has probability

    [3+2*sum_(t>u) cos(2*pi*(phi_t-phi_u-(q/3)*b*(t-u))/q)]/9.

For a binary packet and the endpoint anti-trine POVM it is

    [1-cos(2*pi*(phi_1-phi_0-(q/3)*b)/q)]/3.

The existing `ternary_certified_noise_sampler.cosine_box` uses exact rational
Machin/Taylor enclosures. It works on scalable phase descriptions without
enumerating q roots or any hidden-secret hypotheses. These formulas give
probability boxes of width <=2^-k at k bits. Projection/complement boxes are
exact rational constants. All stochastic calls in the live adaptive controls
use finite coin-prefix refinement; unresolved decisions ABORT explicitly.

For m<=3 outcomes, cumulative probabilities have at most two interior
boundaries. At the final precision B, a width2^-B uniform coin cell can be
ambiguous only near those boundaries. Each individual probability box has
width <=2^-B; cumulative widths are at most2^-B and2*2^-B. Expanding each
boundary interval by one coin cell on either side gives total ambiguous
uniform measure <=(1+2+4)*2^-B=7*2^-B. We use the conservative8*2^-B.
This is an UNCONDITIONAL coupling/error-or-abort budget, not an exact channel
after conditioning away aborted transcripts.

For an adaptive protocol capped at T stochastic calls, choose

    B = h + bit_length(8T-1).

Then T*8*2^-B <=2^-h by union/hybrid coupling, conditional on any public
history reached before a divergence. The physical probability at each call
is fixed BEFORE its private random coin is refined. Controller operations
cannot depend on hidden future bits or the enclosure-refinement path.

Exact phase additions have polynomial bit cost. The cosine enclosure uses
arguments of magnitude<4, O(B) Taylor/Machin terms and polynomial-size rational
arithmetic in B and logq. Overall simulation is polynomial in the original
records accessed, specified primitive work, metadata/phase bit length and
log(1/error). If a receiver in THIS class became polynomial-time for the
original noisy classical problem, this simulator would yield a polynomial-time
classical counterpart. No superpolynomial quantum processing separation for
that source can be based on these primitives alone.

## Explicit Boundaries: Do Not Overclaim

The result does NOT cover arbitrary wide unitaries simply because they end
with one qubit. A universal quantum computation may have a single final
output but wide intermediate entanglement. Nor does it cover coherent
history pointers, unmeasured cross-packet coupling, large indexed phase
vectors, unknown state preparation/inverse or unavailable classical phases.

An unmeasured CNOT on known product |+>|0> creates a Bell state. Replacing it
by the product of its marginals loses XX coherence: a concrete failure of the
product-packet representation. This is a boundary witness, not evidence that
that tiny Bell circuit is classically hard or an algorithm candidate.

The sampler implements the stated logical ideal preparation/gates. Actual
hardware/F3 error, source rounding and phase-synthesis discrepancies require
the previously declared error promises/composition. They are not certified by
this simulation or erased by conditioning on a favorable branch.

Unknown quantum-only native/DHSP phase sources remain legitimate research
inputs. The known ideal sieve literature is not dequantized in that model.
This also does not establish a general classical LWE algorithm: the receiver
must actually solve the original problem at a useful cost before its matched
classical simulator does so. A classically simulable exponential search is
still exponential and not progress toward a Shor-level speedup.

## Controls And Research Decision

The live report reconstructs actual source receipts without secret/error
access, samples adaptive workflows at roots3,9,3^16,3^64, and checks ALL72
paths of a measured-compression/feedback/projection/CNOT/anti-trine harness.
The complete path intervals contain a normalized quantum channel; independent
replay checks literal instruments and exact finite-root laws, not merely
prewritten expected outputs. The harness is a channel audit, NOT a newly
generated oracle problem or an algorithm candidate.

DEPRIORITIZE this measured, single-retained-packet family as a route to a
superpolynomial quantum advantage on the CLASSICALLY PREPARED noisy records.
Keep it as an honest reference/quantum-input baseline. The next high-upside
receiver must explain which persistent coherence or source-access mechanism
escapes this cut, pay for it, and survive its appropriate classical tensor or
original-data baseline. Being outside this cut alone is not evidence of advantage.

Falsifiers: receipt phase differs from preparation; an adaptive law differs
from physical replay; reused ancestors, secret access or omitted rejects;
uncontrolled sampling precision/abort; or any broadening to unknown source
phases/general wide circuits. No universal negative should be entered from
these scoped controls.

```
python theorems/known_preparation_packet_simulation.py --write
node research/certificates/known_preparation_packet_simulation_crosscheck.js
python -m pytest -q tests/test_known_preparation_packet_simulation.py
```
