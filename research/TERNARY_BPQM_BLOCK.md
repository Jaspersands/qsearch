# Ternary Block Decoding: Coherent Composition And Its Finite-Size Limits

Status: local derivation REVIEW PENDING. Known mechanism, no novelty or speedup
claim. The topology, F3 recovery, bounded coherent replay, and the uniform
header-DAG quantum circuit lowering (`compile_root_program`) are implemented.
Finite gate-set synthesis (Solovay-Kitaev / Ross-Selinger) remains separate.

Producer: `python theorems/ternary_bpqm_block.py --write`.
Report: `research/phase_workbench/ternary_bpqm_block.json`.
Tests: `tests/test_ternary_bpqm_block.py`.

## What This Pass Resolves

The previous pass compiled local exact headers and variable-weight rotations.
This pass asks whether their conventions compose into a block measurement and
the unconditional sampler, rather than merely matching a local spectrum, and
lowers `root_schedule` directly into uniform arithmetic quantum circuits
without herald-history tables or classical CORDIC digit advice.

The relevant global method is already known:
[Mandal, Piveteau, Renes and Pfister, Sections 4.3 and 6](https://arxiv.org/html/2609.05857v1#S4.SS3)
select one fixed outgoing edge at every variable, decode the corresponding
extrinsic tree neighborhoods, and recover excluded coordinates from parity
checks. Their q-ary theorem applies to the random-coefficient regular socket
ensemble, not just binary codes. Cycles are not a reason to clone outputs or
condition the input distribution on high girth.

Our implementation preserves raw sockets, coefficient sums and canceled matrix
entries. It selects the first original socket at each root, independently of
coefficient values and offsets. A user-supplied socket ordering is not itself
a certificate of an independently sampled ensemble. The saved seeded inputs
are finite controls, not an IID distribution certificate.

## Exact Topology And Recovery

For each root, a depth-l traversal excludes its chosen outgoing SOCKET. It does
not exclude every parallel edge to that check. Every subsequent variable
excludes only its parent socket. Encountering a previously visited physical
variable or check makes the root bad. A fixed unit check is instead an explicit
unsupported primitive in this compiler, never a fake topology failure.

For the resulting good set G and complement B, compute the rank of H_B over F3.
If it is deficient, return an explicit nonzero c in ker(H) with c_G=0. This is
an exact obstruction to unique erasure recovery, not a probabilistic timeout.
If it has full column rank, row-reduce [H_B | I] to obtain L H_B=I and set

    c_hat_G = r,
    c_hat_B = -L H_G r.

This is a TOTAL linear function of every readout record r. Inconsistent records
can give a vector outside ker(H); they are not postselected or repaired using
an uncharged decoder. Information coordinates are the free coordinates of the
public kernel basis. Modular SUM gates add those linear forms to the estimate
register while retaining r. Reverse SUMs invert the map on dirty records too.

## Coherent Header Cleanup Lemma And Uniform Lowering

The uniform `root_schedule` produces a topologically ordered header DAG and
physical-wire schedule. It checks every original edge, coefficient and child,
and rejects repeated physical channels. Its invariant is:

1. A check maps (i,j) to (h=i-j,j). The left wire becomes a herald and is never
   modified again in the forward tree. The right wire remains active.
2. A bit merge relabels (i,j) to (t=i+j,j), then compresses j using two Givens
   rotations controlled by t and prior heralds. The right wire is retained
   garbage, never another active message. The left wire remains active.
3. Persistent message headers are functions only of the immutable check
   heralds. Leaf headers are constants. Bit headers convolve their input
   triples and do not depend on t. Check headers use their new h.
4. A fiber header depends temporarily on t. It is uncomputed immediately after
   the Givens pair, before another physical operation can change t.

Consequently the persistent header computations are reversed in reverse
DAG order at the end of the tree WITHOUT reversing the physical operations.
Every selector and dependency still has its original value. This holds for
arbitrary physical input amplitudes, including dark branches and unused
`|11>` two-qubit qutrit encodings, not only the promised codeword states.
Zero headers select identity compression. No phase is removed and no herald
is measured or dephased.

`compile_root_program` implements this whole-tree lowering directly:
- Each physical qutrit uses two qubits, with unused `|11>` ($d=3$) fixed by
  total unitary completions (`emit_qutrit_negation`, `emit_qutrit_add_or_check`,
  and $F_3^\dagger \oplus 1$ at the root).
- Known `factor=2` permutations alias `(w0, w2, w1)` header wires with zero
  extra header qubits.
- Active header widths passed to downstream `message_program` and
  `variable_rotation` calls use the exact leaf-count capacity bound
  $C_u = \text{denominator}^{L_u}$ (`C_u.bit_length()`), while the full
  $2 w_{\text{in}} + 2$ output register of each persistent `message_program` is
  retained until reverse-DAG uncomputation.
- At every bit merge, the temporary fiber header (`message_program(..., "fiber")`)
  and the $w_0 + w_1$ CDKM adder are reversed immediately after the two
  `variable_rotation` calls (`(0, 1)` then `(0, 2)`), before `t` can change.
- At the end of the tree, persistent headers are uncomputed in reverse DAG
  order (`cleanup_order_header_ids`) without reversing physical gates, leaving
  zero probability in all work, header, fiber, and CORDIC history qubits:

    V (|psi>_data |0>_work) = (U |psi>_data) |0>_work

on the entire $4^m$ two-qubit-per-qutrit domain. Scratch can therefore be
reused between root instruments. This does not erase the READOUT RECORDS,
which remain in the environment.

## Block Instrument And Sampler

For each good root i, apply U_i, SUM its Fourier-basis root value into a fresh
record, and apply U_i-adjoint. Apply the public recovery SUMs after all roots.
This defines one fixed decoder A_H independent of the original offsets J.
Root order is fixed; outcomes do not adapt the circuit. All readout records
remain in the environment. No independence assumption is made between roots.

Both the bounded exponential-table reference (`root_transform`) and the
lowered uniform arithmetic compiler (`compile_root_program`, `BlockDecoder(..., compiled=True)`)
are tested and compared:
- On the 3-qutrit duplicate check (`steps=5`), the lowered root circuit uses
  713 qubits and 289,341 logical gates before the root Fourier transform,
  replaying full complex superpositions against `root_transform` with norm
  error $< 2 \times 10^{-16}$ and work garbage probability `0.0`.
- On the 4-qutrit cyclic graph (`depth=2, steps=3`, leaf root 2), the lowered
  root circuit uses 24 qubits and 4 logical gates, with norm error
  $< 2 \times 10^{-16}$ and work garbage probability `0.0`.
- On the 5-qutrit nested tree (`depth=2, steps=3`) with nonuniform spectrum
  $\mu = (1/7, 2/7, 4/7)$, the lowered root circuit uses 703 qubits and
  285,776 logical gates, matching the Givens reference with norm error
  $< 4 \times 10^{-16}$ and work garbage probability `0.0` across all 693 work
  qubits, as well as exact inverse recovery on superpositions including
  unused `|11>` encodings.
- In `BlockDecoder(..., compiled=True)` and `audit_case(..., compiled=True)`,
  both forward and reversed root orders match the Givens reference to
  $< 10^{-15}$ across all 27 offsets and dirty estimate/record superpositions.

The sampler prepares the known product source and public kernel-label phases,
then executes A_H, modular label subtraction and A_H-adjoint. It retains every
record and uses the previous actual Gaussian affine lift with uniform gauge
coins. EMPTY targets map to ABSTAIN. For a fixed H with successful recovery,
the previous all-offset identity remains

    E_J ||actual_J - comparison_J||^2 = 2 delta_H,
    E_J TV(output_J, target_J) <= min(1, 2 sqrt(2 delta_H)).

The comparison is UNNORMALIZED and is not an input-state oracle. The finite
tests replay every offset, all codewords and arbitrary complex dirty records.
Changing the outer adjoint preserves norm but breaks the identity by about
0.99334 in the deliberate countercontrol.

## A Conditional Asymptotic Algorithm

This is a local synthesis of existing results and the earlier repo lemmas,
NOT an independently reviewed new quantum algorithm theorem.

Input: an original (3,6) random-coefficient ternary socket graph with N even
columns and V=N/2 rows; independent uniform offsets J in F3^N. The target is
uniform over ALL original x in F3^V satisfying J+H^T x in {1,2}^N. Keep row
dependencies, parallel edges and all offsets. On an empty target use ABSTAIN.

Let R be the event rank(H_B)=|B|, and F_l the ideal-tree ensemble fidelity.
On R, Gao's sufficient bound and q=3 give

    E_H [1_R delta_H] <= 4 N P_l <= 8 N F_l.

The rank event can depend on coefficients. Do NOT condition density evolution
on passing rank. Instead drop 1_R from the nonnegative root-error sum before
using the unconditional coefficient average. Tree selection itself depends
only on the raw graph. Combining with Cauchy-Schwarz and the sampler bound,
and returning ABSTAIN when rank fails, yields

    E_(H,J) TV <= Pr[not R] + 8 sqrt(N F_l) + epsilon_implementation.

The exact, review-pending signed-trine certificate has L=13, F_L<=f and
lambda<1/3. Choose the least integer t with 3^(2^t)>=N^6 and l=13+t. Then

    F_l <= f lambda^(2^t-1) <= 3 f/N^6,
    E TV <= Pr[rank(H_B)<|B|] + sqrt(192 f/N^5) + 1/N,

provided the COMPLETE implementation error is <=1/N. `sufficient_depth_contract`
checks these integer/rational premises and budgets all four root-unitary
occurrences in A/subtract/A-adjoint. It DOES NOT set the rank-failure term to
zero. The known ensemble tree-size/minimum-distance argument makes that term
vanish asymptotically; no finite-N numerical certificate is supplied here.

Real rotations are not free advice. For a uniform finite gate-set version,
atan(2^-i) is efficiently computable to rational interval precision; for i=0
one can use atan(1)=4 atan(1/5)-atan(1/239) with rapidly convergent alternating
series. Bound the total source/gate operator errors separately. Standard
[Solovay-Kitaev compilation](https://arxiv.org/abs/quant-ph/0505030) gives
polylogarithmic precision overhead for the bounded-arity gates. This justifies
polynomial existence, but the certified interval/gate-synthesis backend is
still an implementation obligation. Numerical double-precision Ry calls do
not discharge it at arbitrary N. Bounds must include controlled relative
phases in full operator norm, not distance only up to a global phase.

## Executed Results And Falsifiers

| Original saved input | Depth | Good roots | Rank(H_B) / erased | Outcome |
|---|---:|---:|---:|---|
| 16 spins, seed711 | 0 | 32 | 0 / 0 | Recovery only; product readout |
| 16 spins, seed711 | 1 | 9 | 16 / 23 | Exact nonuniqueness witness |
| 16 spins, seed711 | 2 | 0 | 16 / 32 | Exact nonuniqueness witness |
| 32 spins, seed712 | 0 | 64 | 0 / 0 | Recovery only; product readout |
| 32 spins, seed712 | 1 | 33 | 31 / 31 | Recovery succeeds; decoder accuracy unknown |
| 32 spins, seed712 | 2 | 0 | 32 / 64 | Exact nonuniqueness witness |

No source was regenerated, SAT-filtered or modified. No quantum root circuit
was executed on these saved inputs. Both already have exact classical solution
pools from the preceding pass. Recovery rank alone is not quantum progress
over that classical baseline.

The bounded three-output control retains ten qutrits including labels, estimate
and all records. Ideal Givens: word error0.454506, mean native TV0.209877.
B5 CORDIC: error0.453062, TV0.210483. Reversing the fixed root order changes
these to0.432082 and0.194915. These are inaccurate calibration instruments,
not a parameter search or a speedup. A four-output cyclic recovery control
has word error5/9 and mean TV4/9. Parseval residuals are below2e-15.

The depth13 certificate ALONE requires11,111,111,111,111 distinct physical
outputs per tree. The stronger sufficient schedule is deeper still. At
N=32,64 and10^6 its tree size exceeds N, so no root of any corresponding
regular graph can pass that schedule. These are sufficient-bound limitations,
not lower bounds on all decoders. There is no useful finite-instance algorithm
guarantee in this report. Classical hardness remains entirely unproved.
