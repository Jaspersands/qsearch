# Coherent Tree BPQM: Actual Root Projectors And Their Composition

2026-10-16. Known binary BPQM operations, actual public gate reference and
independent physical controls. Not a new algorithm or a speedup claim.

## Question Answered

The preceding [coset experiment](COHERENT_LOCAL_GIBBS.md) found that applying
only one local parity PGM per information bit fails on overlapping checks.
Does using the WHOLE actual Tanner tree restore the correct coherent readout?
For the implemented finite trees, YES. This is the known BPQM mechanism,
not a newly discovered way to solve arbitrary quantum decoding.

[Mandal et al., Sections 3-4 and Lemma 21](https://arxiv.org/html/2609.05857v1)
describe check/bit-node operations, root projectors and their covariance.
We execute these binary operations with all conditional heralds coherent,
then compare against independently constructed exact-code density matrices.
The local compilation/PGM-span interpretation below is REVIEW PENDING.

## Actual Gate Construction

After H on the physical data, a binary channel state is

    |s_x(a)>=sqrt((1+a)/2)|0>+(-1)^x sqrt((1-a)/2)|1>.

For parity bit u=x+y, CNOT(second message -> first message) leaves the first
as herald h and the second as message. Its exact conditional overlaps are

    a_plus=(a+b)/(1+ab),  a_minus=(b-a)/(1-ab).

The minus sign is retained. Replacing overlaps with their absolute value is
valid for some error statistics but is NOT a phase-correct circuit rule.
Heralds are never measured, reset or replaced with fresh channel outputs.

For two messages carrying the SAME bit, the same CNOT separates the amplitude
parity. Controlled Ry on the second message then clears it. If the first
message bit is z, its two squared conditional weights are proportional to

    z=0: ((1+a)(1+b), (1-a)(1-b)),
    z=1: ((1-a)(1+b), (1+a)(1-b)).

Rotate by -2 atan2(sqrt(p1),sqrt(p0)), controlled by z AND every incoming
herald. The outgoing overlap is ab. These are public one-qubit rotations and
CNOTs, not an ideal Helstrom/PGM gate or a dense eigendecomposition.

Recursively fold parity children at each check and equality messages at each
variable, then H on the root. The resulting root projector is
U_root^dagger |b><b|_root U_root. To decode all information coordinates use
that projector coherently: U_root, copy root to its record, U_root^dagger.
Compose on the ACTUAL disturbed data, then feed that decoder through the
source/XOR/adjoint/sign/Fourier program from the preceding experiment.

The compiler checks actual channel identity: repeated variables/checks cause
UNKNOWN rather than unrolling a cycle with cloned quantum inputs. Optional
depth truncation uses only the real, distinct neighborhood and inherits no
global correctness theorem. Unit checks needing a fixed-bit primitive and
more than ten physical tree outputs are explicitly unsupported here. Native
readout simulation retains its separate eight-original-output cap. The later
[paid splitting experiment](COHERENT_BPQM_SPLIT.md) supplies genuinely weaker
physical outputs to an unrolled tree; ordinary tree mode still refuses reuse.

## Why This Corrects The Overlap Example

For a code orbit, normalized Fourier coset vectors v_s span a K-dimensional
space. The two root-bit conditional density matrices differ by 2x2 blocks
coupling s and s+e_i with positive off-diagonal sqrt(q_s q_(s+e_i)). Their
Helstrom signs on this span are exactly the coarsened PGM bit observables.
Consequently exact optimal root projectors preserve the span and commute ON
that span; sequential information-bit readout equals the global PGM there.
No claim of commutation on the entire ambient Hilbert space is needed.

This depends on exact root optimality for the full code ensemble. Applying
a tree-truncated root measurement in a cyclic code, or using one parity
constraint when other constraints matter, does not meet that condition.

## Results And Costs

Run `python theorems/coherent_bpqm_tree.py --write`.
Artifact: `phase_workbench/coherent_bpqm_tree.json`, with complete sign cases,
codeword errors, actual channel identities, signed reliability tables and
source/helper hashes. Source preparation and all records/adjoints are charged.

For H=(00111,11100), M=5, c=13/20, over ALL32 sign vectors:

- Depth0: mean TV0.335946, worst0.668192 (linear baseline).
- Depth1: mean TV0.156530, worst0.339807 (insufficient local measurements).
- Complete tree: mean TV2.60e-14, worst2.68e-14, without postselection.
- Complete-tree word error is still about0.118949; word recovery is not the
  universal unconditional Gibbs metric.
- One all-positive-sign execution charges4549 ideal one-qubit gates,2369
  CNOTs and11 qubits, including source and the full decoder/XOR/adjoint.
  These are unsimplified counts, not finite universal-gate synthesis costs.

Independent tests compare every root to the Helstrom optimum for parity,
overlapping, equality-chain and disconnected Tanner forests at c=0,13/20,4/5.
They check preservation/commutation only on the actual orbit span, every sign
and both information-coordinate orders, actual primitive counts, source/work
retention and rejection of channel reuse. Truncation explicitly leaks out of
the orbit span and has nonzero unconditional TV; covariance/legal support
alone is NOT enough to certify the Gibbs distribution.

## Why This Is Not An Advantage

The graph families here already have efficient classical tree sum-product
Gibbs sampling. The existing exact integer-factor reference independently
matches their whole output law. There is no quantum speedup in these controls.

No 2^M coset-weight table is built, but every possible coherent herald value
is explicitly compiled. The number of those values, and controlled angles,
can be exponential in the tree size. This is NOT the efficient approximate
quantum reliability-register implementation. It cannot be substituted into
the asymptotic LDPC certificate while pretending all gate costs are linear.
The earlier >10^12-output certificate remains a tree-level statement, not a
compiled finite cyclic-block receiver. Binary64 arithmetic is numerical, not
a certified per-gate implementation-error bound.

## Next Decisive Work

The missing algorithmic step is on CYCLIC, classically difficult explicit
families. Re-enter with a public overlap-aware/reliability-register circuit
and a whole-output guarantee, not independent root-error plots. The strongest
classical factor, cluster and replica-exchange baselines must remain matched
to that actual ensemble. Charge original outputs, reused physical identity,
all herald arithmetic, precision and all repetitions.

Useful next targets: a controlled approximate reliability arithmetic with an
accumulated coherent-error bound, or a specific loop correction that preserves
the normalized orbit span without computing classical partition tables. A
generic PGM oracle, cloned computation tree, positive-message lookup oracle,
or more blind local-order/depth scans does not supply that algorithm.

Gemini integration: expose the standalone producer in CLI/EXP only with its
conditional-table growth, classically easy-family and UNKNOWN-cycle flags.
Keep tree-local, finite-forest and asymptotic cyclic-decoder claims separate.
