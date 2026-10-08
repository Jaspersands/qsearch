# Public Phase Feedback: Exact Compilation And Source Cost

LOCAL DERIVATIONS / REVIEW PENDING. A constructive classical-record simulator
for a specified readout pipeline, NOT a classical DCP algorithm or simulator
for the original unknown quantum states. No candidate or speedup is claimed.

## Causal Full-Covariant Feedback Is A Relabeling

The native full-root covariant effect is E_y=v_y*v_y^dagger/q^2 with
v_y=(1,chi_q(y1),chi_q(y2)). On a fresh input apply a public phase correction
D_(alpha,beta)=diag(1,chi_q(-alpha),chi_q(-beta)) and then this POVM. Directly

    D^dagger E_y D = E_(y1+alpha,y2+beta).

Thus one already-supplied raw record Y can produce exactly the corrected
outcome y=Y-(alpha,beta) modq. This identity holds for EVERY input density
matrix, not only phase states. The choice of phases may use public labels
and earlier reported outcomes, but must not see the current/future outcomes
or unknown secret. Public random coins can be conditioned on and retained.

Induct over original copies. Given the same earlier transcript, the same
causal rule selects the same phases, and the translated next-outcome law is
identical. Conversely, the public phases and reported outcome recover Y.
Both complete-transcript maps are polynomial if the public policy itself is
polynomial. They use exactly the same original source records, no guessed
secret, preparation inverse, repeat measurements or new copies.

The implementation has auditable zero, known-offset and nonlinear quadratic-
feedback policies; policy inputs contain ONLY current frequency rows and
prior reported outcomes. Arbitrary Python callbacks with secret/future-data
closures are not accepted. The known offset is public, not a discovered secret.
The general argument is wider than these examples, but relies on the same
causal/public-data contract. Public policy runtime is classical and charged.
The existing exact joint posterior, including budget and precision failures,
is replayed on recovered raw records without importing a different model.

This does not prove raw records are classically available from DCP. They still
require the lawful quantum measurement source. A polynomial classical decoder
for these quantum-produced records could still be a meaningful quantum
algorithm. The result only removes phase feedback as an additional information
source or an indispensable quantum processing step BEFORE FULL covariant
measurement. Non-diagonal/collective operations and retained quantum memory
are outside the compilation.

## Fixed Trine Is Not The Same Readout

For prescribed phases alpha,beta, take the three covariant outcomes

    O_(alpha,beta)={(alpha+Qz,beta+2Qz) modq:z in F3}, Q=q/3.

These v_y/sqrt3 form an orthonormal qutrit basis. Hence EXACTLY

    sum_(y in O) E_y = (3/q^2)*I.

Filter a covariant record to this orbit. Acceptance is3/q^2 for EVERY input,
including zero and nonprimitive native secrets. Conditional on acceptance,
the extracted z has the same Born law as the prescribed phase correction
followed by inverse F3. No hidden phase or planted secret enters the filter.
Phases MUST be chosen before inspecting the outcome; letting the policy choose
an orbit through the observed Y would grant acceptance1 but produce the wrong
measurement. All failed records are consumed, never retried as fresh data.

For IID native inputs, constant acceptance preserves the fresh label law even
when the rule uses current labels and past accepted outputs. A finite stream
can fail to provide the target number of records. It must return SOURCE CAP
EXHAUSTED, not a normalized partial stream masquerading as the requested one.
Stopped unused records and every rejected ancestor are recorded separately.
Policies see prior fixed-readout outputs as the canonical post-correction
points (Qz,2Qz), not future or rejected raw measurement outcomes.

Obtaining T such records has uncapped expected cost T*q^2/3 covariant source
records. With cap K, expected accepted count is3K/q^2 and Markov gives

    Pr(fill T) <= min(1,3K/(q^2*T)), for T>0.

For T=0 the empty target succeeds without consuming a record. This upper bound
is not a success guarantee. Exact geometric/negative-binomial supply bounds
can sharpen a production ledger; no source factory is granted here.

The overhead is polynomial in q, NOT in logq. In the q=poly(n) regime it can
be a polynomial-cost emulation if the upstream source budget permits it.
At fixed n and growing r with q=3^r it is exponential. Therefore neither
"fixed trine is always freely classically simulated" nor "this filtering is
always exponentially expensive" is a correct statement across regimes.
An efficient ONE-PASS fixed-trine policy using current labels and past accepted
outcomes could be compiled into a covariant-record decoder with this overhead
in suitable regimes. This does NOT compile a policy that chooses every basis
from the entire eventual accepted label batch: reselecting accepted labels
can change the prescribed phases. Conditioning a whole preselected batch
instead can cost (q^2/3)^T; matching chosen labels from fresh IID records is
not free. Such batch-label lookahead is outside this resampling reduction.
Full-covariant relabeling itself does allow known whole-batch label dependence,
because it uses the same originals without filtering. Neither result makes
the original DCP quantum data classically available.

## Evidence And Failure Modes

Dense controls exhaust all covariant outcomes through q27, with actual native
phase inputs, zero/nonprimitive/full secrets and prescribed phase pairs.
They compare both translated physical probabilities and conditional fixed-F3
probabilities. Exact effect-entry certificates verify the identities without
floating transcendental evaluations. Causal transcript controls and joint
posterior comparisons preserve every original record ID. Nonlinear feedback
is a countercontrol to the claim that public label dependence alone removes
covariance; it is not an algorithm candidate or IID population experiment.

Falsifiers: causal transcripts are not invertible; a physical full-covariant
probability changes after the correct translation; orbit acceptance depends
on the input; accepted outcomes disagree with the actual fixed basis; or
finite emulation hides failed records, reused ancestors or missing data.
Approximate phases, correlated source errors and upstream sample availability
require separate channel/error contracts before any algorithm claim.

## Next Research Decision

Do not pursue diagonal phase feedback plus FULL covariant measurement as a
new quantum information mechanism. Instead seek a genuinely different
measurement or a polynomial decoder of the resulting lawful records. For
fixed-basis policies, account for the q^2/3 emulation and actual source regime
before claiming an access separation or dequantization. Collective observable
access and sample-efficient source transformations remain the higher-risk
constructive targets; this compiler is their baseline, not their replacement.

```
python theorems/ternary_phase_feedback.py --write
node research/certificates/ternary_phase_feedback_crosscheck.js
python -m pytest -q tests/test_ternary_phase_feedback.py
```
