# Partial-Frequency Phase Echo On Original Native Samples

LOCAL CONSTRUCTION / REVIEW PENDING. No novelty, efficient decoder or
algorithmic speedup is claimed. This is an actual measurement on the native
input, not a circuit-search target or a supplied fiber oracle.

## Source And Measurement

At even native level 2r, set q=3^r. An original M-copy integer-secret batch is

    psi_s = 3^(-M/2) sum_x chi_q(s . F(x)) |x>,
    F(x) = sum_i (0,a_i,c_i)[x_i],    s in Z_q^n.

The full IID source has independent uniform a_i,c_i in Z_q^n. The producer
reconstructs the actual native ring labels using the existing exact coordinate
bijection. This source law is not automatically valid at odd native levels.

Split m=M-w A wires and w B mediator wires. For a known public n-by-n matrix K,
apply committed per-copy settings chi_q(-eta_i[x_i]), followed by

    D_K |x,y> = chi_q(F_A(x)^T K F_B(y)) |x,y>,
    receiver = inverse_F3_B D_K^dagger inverse_F3_A D_K.

This is a partial-block chirp separated by a noncommuting transform. It is NOT
the initial polynomial of total frequency removed by the earlier syndrome
compiler. It can interfere distinct simultaneous-rotation word orbits; the
one-copy orbit-preserving channel cut does not cover it.

Compute F_A,F_B, apply D_K, uncompute F_A, transform A, recompute F_A of the
UPDATED A word, undo the bilinear phase, uncompute BOTH frequency registers,
then transform B. Leaving F_A through the A transform, or F_B through the B
transform, changes the channel. The arithmetic ledger charges 4nm+2nw modular
frequency additions and 2n^2 bilinear terms, 2nr frequency scratch trits and
an r-trit accumulator. Arithmetic workspace, finite-precision phase synthesis
and a hardware gate export still need compilation. No unknown source inverse,
cloning, reuse, fiber counts or rank/unrank oracle is used.

## Conditional Output Law

For measured words a,b, let

    delta_y = K F_B(y),       correction = K^T F_A(a),
    A(a,u) = product_(i in A)
        [1 + chi_q(u.a_i-eta_i1) omega_3^(-a_i)
           + chi_q(u.c_i-eta_i2) omega_3^(-2a_i)] / 3.

Then, with W=3^w,

    amp_s(a,b) = W^(-1) sum_y A(a,s+delta_y)
        chi_q((s-correction).F_B(y)-eta_B(y)) omega_3^(-b.y).

The streaming evaluator costs O(W(nM+n^2)) arithmetic/phase work per supplied
secret and outcome. At w=O(log(nr)) this likelihood evaluation is polynomial.
It does NOT supply efficient unknown-secret inference. Reported MAP scores
enumerate all q^n secret hypotheses and all 3^M outcomes. The evaluator uses
floating-point phases and is not a certified large-size log-likelihood
implementation. Complete-reference budgets fail rather than returning a
selected or partially normalized score.

## A Stronger Same-Copy Baseline

Draw a classical y uniformly, apply the known +K F_B(y) phase to A, measure
every A and B copy with the committed product Fourier settings, retain y and
all outcomes. This uses the SAME M original quantum samples and only
single-copy quantum gates. It is LOCC, not a classical simulation of the
input quantum states. Its MAP decoder also pays exponential enumeration.

For the dirty echo with F_B left in scratch, group words into classes
C_z={y:F_B(y)=z}. Tracing out that scratch gives

    P_dirtyFB(a,b|s) = sum_z |A(a,s+Kz)|^2 / W^2
        * |sum_(y in C_z) chi_q(-eta_B(y)) omega_3^(-b.y)|^2.

Equal-frequency words keep coherence. The public class kernel can be sampled
classically: choose y uniformly and hence z with probability |C_z|/W, then
sample b from its normalized class Fourier kernel. Recording y and the A
readout is at least as informative as this garbled channel. The stronger LOCC
baseline additionally reads B. With R distinct frequency classes, Cauchy gives
the pointwise inequality P_clean <= R P_dirtyFB, with R<=W. This factor is not
a useful general clean-echo dequantization statement.

Leaving a FULL B-WORD tag is different: b is uniform and the A likelihood is
W^(-1) sum_y |A(a,s+delta_y)|^2. In the extreme F_B=0 example, frequency scratch
dephases nothing, while a word tag still destroys B interference. Tests replay
actual orthogonal scratch tags and verify both channels, including collisions.

## What The Experiment Says

Twelve predeclared source cohorts use (q,n,M,w) equal to (9,1,4,1), (9,2,6,2),
(27,1,5,2), (81,1,6,2), with three seeds each. Two setting policies and four
coupling policies are retained: product, positive, negative, and full-A
preconditioning. All echo policies lose to the best tested product policy in
each cohort; the mean best-echo minus best-product full-secret MAP difference
is approximately -0.280883. They also lose to the best tested LOCC baseline.
Every one of the72 non-product policy/cohort records also loses to its OWN
matched LOCC baseline for both full-secret and least-trit MAP. Thus the
negative comparison is not only selection of a better baseline from a menu.
These are conditional finite diagnostics, NOT a population theorem, a
proof of dominance by one committed policy, or an unrestricted no-go result.

The preconditioner greedily selects n independent first A rows modulo3 and
inverts their row matrix over Z_q. A unit determinant permits an exact
adjugate/inverse-determinant implementation despite the composite modulus.
Rank failure returns K=0 without rejecting the source. The inverse depends
on FULL A labels and therefore escapes the A-independent shifted-probe bound.
This escape is legal but supplies no demonstrated advantage.

An independent Q(zeta9) checker verifies the complete bounded q9,n1,M3
control: 1,944 exact clean probabilities, 1,944 exact winner comparisons and
1,944 pointwise frequency-class domination checks, plus normalization and
clean/dirty/LOCC MAP scores. Other cohorts remain numerical references.

## Research Decision

Do not tune a small fixed coupling menu as the main research program. The
[shifted-probe gate](NATIVE_ECHO_SHIFTED_PROBE_GATE.md) also obstructs a fixed
small-mediator single echo near the information threshold. Full-label
calibration, multiple interleaved echoes, wider mediators and larger sample
surplus remain outside that theorem, but none is a positive result. A next
proposal must explain how it exploits full-label structure, preserve original
source access, and include an efficient informative decoder, not merely a
fast likelihood or an exponentially computed optimal score.

```
python theorems/native_partial_phase_echo.py --write
node research/certificates/native_partial_phase_echo_crosscheck.js
python -m pytest -q tests/test_native_partial_phase_echo.py
```
