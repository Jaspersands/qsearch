# Next Compiler Pass: Scalable QFT Precision And Postselection Debt

Implemented by lattice_qft_precision.py and the public source compiler;
see LATTICE_QFT_PRECISION.md for verified scope and remaining obligations.
It is not a certified full hardware/source error bound. The former
exact-QFT compiler's128-wire safety cap prevented growing-family use:
the Regev position register has ell=n*(4n+1) wires.
Do not treat cap failure as hardness, and do not silently underflow its tiny
rotation angles. Approximate QFT has a principled polynomial-precision route.

## Logical Approximation Bound

In the usual positive ell-wire QFT, separation d has ell-d controlled-phase
gates with angle pi/2^d. Keep separations d<=b and omit larger ones, with
0<=b<=ell-1. There are

    kept controlled phases = b*ell-b*(b+1)/2;
    Hadamards = ell; swaps = floor(ell/2).

For a removed gate CP(theta), operator norm ||CP(theta)-I|| is
2|sin(theta/2)|<=|theta|. Telescoping the two unitary products gives

    ||F_ell - F_ell,b|| <= pi * sum_(d=b+1..ell-1) (ell-d)/2^d
                        <= 4*ell/2^b.

The exact sum is (ell-b-2)/2^b+1/2^(ell-1), including0 at b=ell-1.
Use the conservative bound capped by2 for unitary operator difference;
when all gates are retained the approximation term is EXACTLY0. Do not
materialize 2^ell decimal JSON to encode these bounds.

For any input including arbitrary entangled cell/work ancillas, output
density trace distance is at most the operator bound, capped by1. Measuring
cell/label and retaining the colour qubit is CPTP, so the COMPLETE joint
classical-quantum source instrument inherits that distance. This does not
certify every normalized conditional qubit individually.

## Query Budget And Precision Selection

For T total uses of the approximate QFT or its inverse in an adaptive quantum
experiment, a hybrid argument bounds the final unconditional output trace
distance by T times the single-use bound. Count EVERY approximate operation,
including inverse/reflection/amplification calls, not only fresh source shots.
Given exact rational target delta in(0,1], choose

    b >= ceil(log2(4*ell*T/delta)), capped at ell-1.

Then the logical approximation contribution is at most delta, or exactly0
if the full QFT is required. This is a conditional resource certificate:
the receiver's actual query bound T must be proved/charged. It does not
establish a polynomial-time receiver or erase exponential amplification.

Rounding and synthesis errors for the KEPT rotations add separate terms
sum_j eta_j under the same telescoping argument. Qiskit floating-point gate
angles are not formal eta_j certificates or fault-tolerant implementation
costs. The ideal logical approximation bound must not certify those by fiat.

## Rare Conditional States Can Still Be Wrong

Suppose two complete accept/reject instruments have trace distance delta,
accept probabilities p,q>0, and accepted normalized payloads rho,tau.
Writing their success subnormalized blocks A,B gives

    D(rho,tau) <= (||A-B||1+|p-q|)/(2p) <= delta/p.

The last inequality uses the FAILURE block, whose norm is at least |p-q|.
The symmetric inequality with q also holds; using either supplied positive
probability gives a safe bound capped by1. A success probability lower bound
p_min permits the conservative delta/p_min guarantee. Without it there is
NO unconditional-to-conditional accuracy certificate.

Counterexample for every p=2^-k: both instruments reject with the same
probability1-p and identical reject state. On acceptance, the first returns
|0> and the second|1>. Full trace distance is p, but conditional distance1.
This is an exact calibration counterexample, not an algorithm candidate.

For ordinary DCP sampling, bound the ENTIRE unconditioned labelled-register
experiment. Do not require accuracy of a specified exponentially rare label
by pretending it is freely prepared. For genuinely postselected algorithms,
retain success/failure outcomes, source work and conditional precision debt.

## Proposed Modules And Tests

Check current files before creating:

    theorems/lattice_qft_precision.py
    research/LATTICE_QFT_PRECISION.md
    research/reductions/lattice_qft_precision.json
    research/hypotheses/lattice_qft_precision_contract.json
    research/certificates/lattice_qft_precision_crosscheck.js
    tests/test_lattice_qft_precision.py

Use installed Qiskit QFT synthesis and VERIFY its approximation-degree to
separation-cutoff mapping against actual decomposed gate counts. Do not assume
the mapping from a flag name. Integrate a precision plan into the public phase
source without changing the default exact finite controls. Replace arbitrary
compiler caps with explicit user/resource policies and cheap resource-only
ledgers where appropriate; simulator caps remain separate UNKNOWN outcomes.

Tests must cover dense operator norms, ancilla-entangled complete instruments,
exact gate counts, exact rational cutoff selection, cumulative query bounds,
the rare-event counterexample and inverse/amplification accounting. The
independent checker must derive sums and integer inequalities without using
the producer's success flags. Large ell profiles need factored bounds and
polynomial resource counts, not dense simulation or giant phase tables.

A sparse approximate circuit is not a quantum breakthrough. Its contribution
is to remove an artificial source-precision bottleneck while keeping honest
noise, rare-event and receiver obligations.
