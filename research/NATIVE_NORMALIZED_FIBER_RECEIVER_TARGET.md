# Positive Native Target: Source-Weighted Fiber Erasure

RESEARCH SPECIFICATION / NOT AN IMPLEMENTED COMPILER. This spells out ONE
constructive receiver target after the spectral access audit. It is not a
new ideal PGM principle, an accepted algorithm or a requirement imposed on
all collective receivers. Do not implement a dense table and call it progress.

## Actual Input And Operation

Use M fresh native qutrits at q=3^r with their full public IID frequency rows.
Set D=3^M, G=q^n and F(x)=sum_i(0,a_i,c_i)[x_i]. The real input is

    psi_s = sum_y sqrt(p_y) chi_q(y.s) v_y,
    p_y=C_y/D, v_y=C_y^-1/2 sum_(F(x)=y)|x>.

Compute F into a clean n-log(q) register with public reversible arithmetic.
This operation is already available. The missing operation is a public,
frequency-register-controlled clean erasure T:

    T(|y>|v_y>|0_work>) approximately |y>|0_word>|0_work>.

Every operation may use the labels, not the secret. No unknown-state inverse,
fresh psi_s preparation oracle, secret-weighted phase oracle, uniform fiber
state oracle, all-fiber count table or uncharged QRAM is granted. The compiler
must output a circuit/program, not exponentially many amplitudes.

## Demand Source-Weighted Accuracy, Not Worst-Case Fiber Ranking

Preserve y throughout the approximate erasure and prove

    sum_(occupied y) p_y ||T_y(|v_y>|0_work>)-|0_word>|0_work>||^2 <= e^2.

Because different y-registers remain orthogonal, this bounds the COMPLETE
output vector error by e for EVERY secret s; unknown secret phases cannot
change it. Thus trace distance and every final measurement's probability
error are at most e. A small per-entry operator error or agreement on a few
known words is not this certificate. Dirty scratch, flags and failures must
be included in the complete channel, not renormalized away.

This average-source target is weaker than clean rank/unrank on every word or
exact uniform preparation in every fiber. The earlier worst-case lexicographic
model-counting reduction does not automatically rule it out. Conversely a
classical conditional sampler generally leaves random-seed garbage and does
not automatically implement clean coherent erasure.

## The Receiver And Its Complete Resource Consequence

If T exists at polynomial cost, the frequency register is approximately

    sum_y sqrt(p_y) chi_q(y.s)|y>.

Inverse QFT over (Z_q)^n returns s with ideal probability
(sum_y sqrt(p_y))^2/G: the existing optimal pure-ensemble/PGM quantity.
For the true IID native label law, the existing pair calculation gives
E_labels[chi2(p,u)]=(G-1)/D, u=1/G. Squared fidelity is at least1-chi2.
Consequently the complete mean raw failure is at most

    (G-1)/D + e + eta,

where eta bounds JOINT trace-distance error of the original supplied batch.
This is mean over labels for EVERY fixed secret, provided the weighted erasure
bound is secret-independent. If the compiler can abort, its complete-channel
error or raw failure probability must appear in the bound as well.

For an all-but-h bad-label guarantee, Markov gives ideal failure<=epsilon
outside mass h when D>=(G-1)/(epsilon*h). Hence

    M >= ceil(log_3((G-1)/(epsilon*h)))

is a polynomial original-copy budget (roughly nr plus logarithmic surplus),
not a time theorem. Add e and eta AFTER retaining the raw bad-label/abort
accounting. Real upstream source supply and input approximation still need
their existing conversion/error ledgers.

## What Counts As A Positive Research Pass

Two actual local proposals have now been tested. The
[native block walk](TERNARY_NATIVE_BLOCK_WALK.md) freezes at small support;
at near-entropy copy counts its distinct full-fiber words have extensive
distance with high probability. The
[soft fiber parent](TERNARY_SOFT_FIBER_COOLING.md) allows intermediate
violations, but its binary membership-energy cooling has an exponentially
small Born-weighted population success bound at polynomial action. The
latter follows state transfer, not a global gap alone, and needs no collision
premise. Neither result covers residual-aware energies, nonlocal operations
or other collective receivers. Do not recycle these two proposals as solved
compiler steps.

The [residual-aware follow-up](TERNARY_RESIDUAL_FIBER_COOLING.md) changes
unmarked classes and therefore does not reuse the binary-energy bound.
It establishes a separate cold-evolution obstruction even with a coherent
warm Gibbs state supplied for free. Hot-stage dynamics are still open.
A useful next proposal must exhibit an actual hot/non-parent operation or
change the encoding, not claim that granting a warm state resolves the cost.

Propose a SPECIFIC implementation of T exploiting native structure, or an
alternative noncommuting instrument that bypasses T. Explicitly state its
representation, local reversible operations, workspace, error mechanism,
source copies and growing-n/root scaling. A normalized fiber transform given
as an oracle fails the access gate. Generic search takes exponential time;
the new work must remove that cost, not conceal it in state preparation.

For a fiber proposal, test original-source coherence, complete scratch cleanup
and the source-weighted error on bounded native controls. Compare against an
exact reference only at capped sizes. Search for rare fibers, conditioning
losses, exponential singular-value normalization and hidden count/rank calls.
Compare with the existing coherent-edge, collective-character, nonlinear-
cycle and prefix-Schmidt audits before asserting that their blockers disappear.

Do not spend another pass implementing generic promise checkers if no actual
candidate compiler emerges. Change the operation or research direction instead.
Failure of this ONE target is not failure of quantum algorithm discovery.
