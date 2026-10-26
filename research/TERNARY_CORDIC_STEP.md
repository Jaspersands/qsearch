# Reversible Variable-Weight Ternary Rotation

Status: LOCAL CONSTRUCTION REVIEW PENDING. Actual compute/rotate/uncompute
gates are implemented. No full LDPC decoder, physical-device run,
fault-tolerant synthesis or speedup is claimed.

Producer: `python theorems/ternary_cordic_step.py --write`.
Tests: `tests/test_ternary_cordic_step.py`.
Artifact: `research/phase_workbench/ternary_cordic_step.json`.
Mathematical convention, prior art and uniform error proof:
TERNARY_COHERENT_RELIABILITY.md.

## What This Removes

The preceding pass supplied exact message-header gates but left its
weight-to-CORDIC-digit computation classical. This pass removes that local
interface gap. Unknown/coherent headers are not measured and the classical
reference is not injected as advice. No truth table indexed by weights or
upstream heralds is generated.

`step_program(m,w,i)` takes two's-complement P,Q, unsigned a,b and clean
outputs. It computes sigma=sign(P sqrt(b)-Q sqrt(a)), with equality choosing +,
then outputs a retained sign digit and

```
Pnext = 2^i P - sigma Q
Qnext = 2^i Q + sigma P.
```

It retains original P,Q,a,b. Output coefficient width m+i+2 excludes overflow
even on the entire arbitrary clean-input domain, not just reachable CORDIC
histories. The total unitary is defined on dirty inputs too, but its numerical
contract requires clean outputs/scratch.

## Actual Arithmetic

- Compute unsigned abs(P),abs(Q) using controlled complement and CDKM addition
  of one. The minimum negative two's-complement input is handled correctly.
- Square each magnitude by the existing exact multiplier, then multiply by
  b or a respectively. Zero padding is charged and retained clean.
- Compute both unsigned >= comparisons using the carry of U+complement(V)+1.
  Every comparator uncomputes its difference/carry/constant scratch.
- Determine the signs of the ACTUAL products, folding in exact zero terms.
  Merely using P,Q sign bits is WRONG when a or b vanishes.
- Toggle the output decision through three disjoint sign/comparison cases.
  Reverse the complete predicate computation, leaving only the decision.
- Copy shifted/sign-extended inputs into new coefficient outputs, then perform
  sign-controlled CDKM addition/subtraction. Clean extended-input scratch.

Multi-control zero tests explicitly use AND chains and their inverses, not an
unpriced gate with a growing number of controls. Every arithmetic gate has
at most three positive X controls. No resets, measurements, discarded
failures, divisions, floating-point decisions or square-root arithmetic.

The small exhaustive domain has 64 cases (m=2,w=1,i=0), including P,Q signs,
minimum negative integers, ties and zero products. Additional parameterized
tests check larger words/iterations and complex superpositions. An independent
full-statevector test validates the sparse X/Ry evaluator on a small circuit;
the many-work-qubit runs are sparse gate execution, not dense statevector
simulation or actual hardware execution.

## Complete Local Interface

`variable_rotation(w,B,pair)` constructs the whole operation:

1. Initialize public P=1,Q=0, compute B decisions/updates, retaining history.
2. Reversibly compute enabled=(a+b !=0).
3. Apply actual digit-controlled constant-angle rotations on the encoded
   qutrit pair 01 or 02. The unused |11> and disabled blocks are fixed.
4. Uncompute enabled and EVERY coefficient, digit and scratch bit.

On clean work, the result is

```
|a,b> |z> |0_work> -> |a,b> R_B(a,b)|z> |0_work>.
```

The circuit is coherent across a,b as well as z. Its uniform ideal-angle
operator error is the preceding note's bound 2^(1-B) for one Givens rotation.
Ry constants remain numerical logical gates, and universal synthesis/rounding
errors must receive the separate whole-program operator-error budget.

The live artifact runs both pairs at w=2,B=3, across 16 complex-weighted
source basis words including all qutrit encodings and a=b=0. Each program has
268 qubits and 27,834 actual logical gates. Observed reference/inverse norm
residuals are below 2e-16 and arithmetic garbage probability is exactly zero.
These are component checks, not evidence for scalable CSP hardness.

## Cost Is A Serious Limitation

The resource formulas count the actual program, not an abstract arithmetic
oracle, and are checked against compiled circuits. For one iteration let
n=m+i+2, k=max(2m,w), and M(r)=r(6r+1). Define

```
predicate = 20m + 12 + 2 M(m) + 2 M(k) + 80k
step gates = 2 predicate + 30n - 2i + 19
step qubits = 8m + w + 7 + 4n + 10k
step scratch = 6m + 10k - w + 6 + 2n.
```

All counts include clean scratch and retained inputs/outputs. The full history
shares a clean workspace between iterations, retains old coefficients, and
is reversed after rotation. Its simple recurrence m_(i+1)=m_i+i+2 gives
m_B=2+B(B+3)/2. This implementation costs O(B*(w+B^2)^2) gates and
O(w+B^3) qubits, before finite universal-gate synthesis.

Harsh check: a 64-bit, 52-step local rotation predicts **5,048,480,990 logical
gates and 91,545 qubits**. That prediction is analytical, not an allocated or
executed giant circuit. It makes the polynomial existence argument concrete,
but does not make this layout useful on a physical machine. The explicit
compiler refuses requests above its reference cap before allocating them;
the cap is an engineering refusal, not a complexity lower bound.

Do NOT infer that any efficient ternary rotation requires these resources.
Known fixed-precision/CORDIC methods may do much better. Conversely, do not
hide this implementation's overhead behind the word polynomial or multiply
its tiny test's fidelity into an unproved whole-code success probability.

## Remaining Scientific Work

The next decisive gap is instantiating the global mechanism, not another
arithmetic table. The known
[q-ary block construction, Theorem 30](https://arxiv.org/html/2609.05857v1#S6)
already treats cyclic neighborhoods as erasures and uses minimum distance for
recovery after tree-root measurements. Do not reinvent or claim that method
as a new theorem. Its ensemble/entry-condition assumptions and its coherent
implementation must be checked for this exact signed-trine application.

- Identify distinct-leaf neighborhoods at the required depth and mark other
  coordinates as erasures using the known two-stage method. Do not require
  every random-graph root to be a tree or clone reused channel outputs.
- Instantiate its full offset-INDEPENDENT coherent word decoder, charging
  root readout/uncomputation, erasure recovery, adjoints and arithmetic error.
  Ideal-tree density evolution alone is not a finite implementation.
- Compose integer fiber weights and these two Givens pairs at actual qutrit
  nodes, then validate their changed dark-space completion in the full
  unconditional sampler. Prior Householder output laws cannot be assumed.
- Continue matched classical conditional-sampling attacks. Exact pools already
  solve the saved finite examples. Local quantum arithmetic supplies no
  classical hardness assumption or separation.

Independent mathematical review is still required. No candidate, central
proof, negative result or preprint claim is promoted automatically.
