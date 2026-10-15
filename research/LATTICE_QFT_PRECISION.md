# QFT Precision, Query Accounting And Rare-Event Debt

This implements the earlier precision specification. It is a source/compiler
subsystem, NOT a quantum algorithm discovery. Its certificate applies to the
QFT component and the complete joint instrument; it does not certify source
arithmetic, hardware faults, a growing unique-SVP promise or a receiver.

## Cutoff And Encoded Rotations

For ell wires, retain controlled-phase separation d<=b. There are ell-d gates
with angle pi/2^d at each separation. The retained count is
b*ell-b*(b+1)/2. Qiskit's actual synthesis uses approximation_degree=ell-1-b;
the compiler checks ALL gate counts, separation multiplicities and angles.
It does not assume that mapping merely from the parameter name.

Telescoping the unitary products and ||CP(theta)-I||<=|theta| give

    ||F-F_b|| <= pi*sum_(d=b+1..ell-1)(ell-d)/2^d
               <= min(2,4*ell/2^b).

If b=ell-1 the truncation contribution is EXACTLY0. The omitted sum has
symbolic form (ell-b-2)*2^-b+2^-(ell-1); huge exponents are not expanded.
For bounded exponents the implementation uses this exact sum times the
Machin pi upper endpoint. For large exponents it uses the tighter safe
4*(ell-b-1)*2^-b upper bound instead of allocating a2^ell denominator.

The installed library encodes retained angles as binary64 pi scaled by2^-d.
For d<=1022 this scale is exact and normal. A rational Machin interval with
alternating remainders bounds |pi_encoded-pi|. The retained weight is

    sum_(d=1..b)(ell-d)/2^d = ell-2+(b+2-ell)*2^-b.

Multiplying it by the rational pi-error upper bound gives a SEPARATE bound
for encoded CP parameters. Unsupported normal-angle ranges are rejected,
not silently underflowed. This is an ideal gate-parameter certificate, not
a bound for statevector/MPS floating-point evolution or physical devices.

## Full Experiment And Postselection

The operator bound applies with arbitrary entangled ancillas. Density trace
distance is at most that bound, capped by1. Cell/label measurement and
retaining a colour qubit is CPTP, so the COMPLETE joint source instrument
inherits it. A hybrid argument bounds an adaptive experiment by T times the
single-use error. Every QFT/inverse counts; a phase-parent reflection uses
both a forward and inverse QFT. The usage bound is a declared external
receiver assumption, not a proof that the receiver is efficient.

Automatic cutoff selection reserves half of an exact rational target delta
for retained-angle error: b>=ceil(log2(8*ell*T/delta)), capped at ell-1.
Targets are checked independently for ideal truncation and encoded parameters.
A huge-query profile meets the former but FAILS the latter. The tool must
report that failure. Optional external logical-gate error bounds are added
conditionally; supplying a number does not prove it for hardware or arithmetic.

For success probability bounded below by p_min, normalized conditional payload
trace distance is at most min(1,delta/p_min). With no mass bound it is UNKNOWN.
The proof uses both success AND failure subnormalized blocks: the failure
block norm is at least the change in success probability. Exact controls
give identical rejection states and accepted orthogonal payloads with
probability p=2^-k. Full distance is p but conditional distance1. Small
joint error therefore does not grant a correct rare-label state or inverse.

## Source Integration And Resource Policies

The public cube compiler now exposes cheap CLOSED exact resource estimates.
Positive coefficient shifts preserve popcount; for a negative coefficient c,
the two's-complement shifted popcount is w-h-popcount(|c|-1). Summing over
input bits gives exact instruction/addition counts without gates or preimages.
Compiled circuits check those counts. Resource policies limit qubits, adder
bits, additions and QFT instructions explicitly and can be overridden. A
policy rejection is UNKNOWN, not a source failure or complexity lower bound.

The old128-wire QFT ceiling is removed. A264-wire position QFT is actually
compiled with its precision plan and in-place cube source. That identity-
basis calibration is CLASSICALLY EASY and does NOT meet a two-point promise;
it validates resource scaling only, never a candidate or quantum signal.
Much larger plans use symbolic resource ledgers, not dense state simulation.

Actual source sampling charges an attached forward-QFT ledger before running.
Inverse and reflection budgets have their own counters. Copies/resets and
budget overrun are rejected. Manual untracked circuit calls are outside the
accuracy contract; circuit construction alone is not evidence of execution.

An approximate-QFT sample is NOT automatically an exact DCP register. Its
metadata marks the difference and the old exact-model backend refuses it.
A future robust receiver must use the JOINT channel-error budget, not claim
that every conditional state satisfies the exact phase formula. Default
exact finite source controls keep their old mathematical instrument.

## Verification And Open Work

Tests compare dense full-QFT matrices, installed synthesis counts, entangled
joint instruments, rare-event counterexamples, query budgets, exact signed
resource estimates and actual source compilation. The independent JS replay
derives Machin intervals, sums, integer cutoff inequalities and counters.
Numerical controls are diagnostics, not formal proofs of generic circuits.

Arithmetic gate parameter/synthesis errors, fault-tolerant costs, source
geometry, actual receiver query bounds and robust decoding remain open.
Source precision is not the missing breakthrough. This pass removes an
artificial compiler bottleneck and prevents false accuracy claims from it.

Run `python qsearch.py lattice-qft-precision` or the standalone module `--write`.
