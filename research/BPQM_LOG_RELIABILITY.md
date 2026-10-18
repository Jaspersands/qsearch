# BPQM Reliability Arithmetic: A Conditional Precision Contract

2026-10-16. Classical interval reference, locally derived error bound REVIEW
PENDING. NOT a compiled reversible circuit, new algorithm or speedup result.

## Question And Prior Art

The [actual coherent tree compiler](COHERENT_BPQM_TREE.md) fixes a physical
composition error but explicitly enumerates herald-controlled angles. Replacing
that table with coherent arithmetic needs finite registers and a whole-program
error bound, not accurate classical plots or stability on likely branches.

[Piveteau-Renes](https://arxiv.org/abs/2109.08170) already identify exponential
global controls and provide an efficient approximate message-passing scheme.
This note does not claim their result anew. It gives a directly testable
log-coordinate arithmetic/error contract for this repository's binary gates.
It does NOT implement that published efficient scheme or prove novelty.

## Signed Log Coordinates Avoid Artificial Poles

For signed overlap a in (-1,1), store L=atanh(a), not abs(a). The exact
binary operations become

    parity h=0: L_out=L_left+L_right,
    parity h=1: L_out=L_right-L_left,
    equality:  L_out=[log cosh(L_left+L_right)
                     -log cosh(L_left-L_right)]/2.

Compute log cosh(z)=|z|+log(1+exp(-2|z|))-log2. The equality output is
bounded in magnitude by min(|L_left|,|L_right|). The gate angles for message
bit z are

    theta_0=-2 atan(exp(-L_left-L_right)),
    theta_1=-2 atan(exp(L_left-L_right)).

Evaluate -2 atan(exp(t)) using -pi+2 atan(exp(-t)) for t>=0. No exp of a huge
positive number is needed. No denominators 1-ab near zero are used.
The implementation certifies dyadic approximations with FLINT Arb intervals,
including transcendental evaluation and integer rounding. This is classical
reference arithmetic at requested inputs, not a quantum resource certificate.

## Uniform Stability Derivation

Let f(x,y)=[log cosh(x+y)-log cosh(x-y)]/2. Its derivatives are

    f_x=[tanh(x+y)-tanh(x-y)]/2,
    f_y=[tanh(x+y)+tanh(x-y)]/2.

Their absolute values sum to max(|tanh(x+y)|,|tanh(x-y)|)<=1. Thus f is
1-Lipschitz in the infinity norm, globally including signed cancellations.
Parity updates sum the two input errors. Also
|d[-2 atan(exp(t))]/dt|=sech(t)<=1, so each angle changes by at most the sum
of its two input log errors. These are analytic identities; finite tests
calibrate the implementation rather than prove the uniform statement.

Suppose EVERY initialization and message/angle evaluation has absolute error
<=eta=2^-b, every internal merge has two disjoint original-channel subtrees,
and no overflow occurs. Induction bounds the log error at a subtree of n
original outputs by (2n-1)eta: parity adds child errors plus eta; equality
takes their maximum plus eta. At an equality gate with n total descendant
outputs, angle error is <=(2n-1)eta, including angle evaluation.

Each equality operation is a multiplexed Ry over ORTHOGONAL coherent herald
branches. Its operator error is bounded by HALF the maximum branch angle
error, NOT the sum over all 2^h possible herald strings. Different equality
nodes do compose sequentially, so their errors add by a hybrid argument.

Let L bound distinct original outputs per root and E be the total number of
equality multiplexers over all decoded information roots, counting EACH root
program ONCE. The full decoder/XOR/adjoint contains four occurrences of each
root program or inverse. Hence its output TV perturbation from the IDEAL
algorithm is at most

    2 E (2L-1) 2^-b + epsilon_source.

This is not itself a Gibbs error bound: add any ideal algorithm's existing
Gibbs error. Internal heralds must remain coherent; arithmetic inputs/garbage
must be retained and exactly uncomputed rather than reset. Finite universal-
gate synthesis errors, approximate arithmetic circuit implementation errors,
and source errors need their own additional budgets. The contract assumes a
uniform per-branch evaluation guarantee; checking selected inputs is not a
substitute for it. It gives no right to clone a cyclic computation tree.

## Range, Examples And What Changed

If the stored leaf log is L0_hat and every merge rounds by <=eta, all stored
messages have magnitude <=L*|L0_hat|+(L-1)eta. The helper separately allocates
signed integer bits and fractional bits; no modular wraparound is permitted.
It does not count arithmetic scratch, heralds or compute/uncompute gates.

`python theorems/bpqm_log_reliability.py --write` generates the source-bound
artifact `phase_workbench/bpqm_log_reliability.json`.

- The five-channel, three-root control has E=6. For perturbation1/1000 and
  ideal source, b=17 suffices under the stated assumptions. At c13/20 the
  conservative signed message register has21 bits, excluding scratch.
- An ILLUSTRATIVE L=1,111,111,111,111, 2^60-root budget uses152 fractional
  bits and193 bits per message. No such graph/source/circuit was constructed.
  This says precision need only be logarithmic in declared work; it does not
  remove the astronomical original-channel or circuit work.
- Near-opposite overlaps1-2^-256 and -1+2^-255, and log messages +/-1000,
  retain certified arithmetic bounds without singular direct overlap ratios.

The actionable conclusion is narrow: uncontrolled precision loss need not be
assumed inevitable merely because overlap denominators are small. The missing
work remains an actual efficient reversible implementation and a useful
algorithm/source, NOT more explicit herald enumeration.

## Implementation Handoff And Falsifiers

Implement fixed-width reversible add/subtract and a certified approximation
for logcosh/atan-exp on the bounded range, preserving old inputs for reversible
rounding. Compute the rotation angle, apply it coherently, and uncompute its
scratch. Never use a 2^h lookup table under the name arithmetic. Independently
compare its logical channel, garbage cleanup and measured task to the existing
finite compiler; charge every register and all inverses/synthesis.

Falsify the implementation by a branch exceeding eta, signed overflow,
garbage distinguishability, measured heralds, a larger-than-budget whole-output
error, exponential table compilation, or source reuse violating disjointness.
Even a successful tree implementation has a strong classical tree sampler.
An advantage needs the separate cyclic-code/native-ensemble and classical-
sampling analysis. Do not equate this arithmetic contract with that result.
