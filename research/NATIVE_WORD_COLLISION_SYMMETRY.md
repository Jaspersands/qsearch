# Constructive Two-Word Collision Symmetry Test

This is a legal collective-measurement BASELINE on known classical source
records. It is not an efficient decoder, new speedup or a granted fibre oracle.
Literal finite states execute the logical preparation, controlled SWAP and
Hadamards. Physical reversible-arithmetic compilation remains an obligation.

## Circuit And Full Branch Law

Prepare psi_y(w)=exp(i*theta_y(w))/sqrt(D) on one M-qutrit register and an
independent uniform word on another. Original response phases are known,
so preparation and its inverse are legal here. Compute both public frequency
labels reversibly, compare them, and uncompute. The equality predicate
commutes with swapping the registers. An ancilla H--controlled SWAP--H tests
symmetry while retaining equality failures. No normalized fibre is prepared.

Write C_A=sum p_sigma^2 and R_y=<psi_y,K_A psi_y> for the RAW Gram K.
All actual original phases, not secret-ideal phases, enter the circuit.

    P(equal,+) = (C_A+R_y)/2,
    P(equal,-) = (C_A-R_y)/2,
    P(equal)   = C_A.

Eliminating the uniform second register yields the actual word effect
E_+/-=(D_A +/- K_A)/2, where D_A(w,w)=p_f(w). D_A is constant on each
fibre and COMMUTES with K_A. Its expectation is C_A on both an actual
uniform-amplitude native source and the IID-null density. This diagonal
term therefore cancels in their decision gap. The joint SWAP circuit does
not supply the genuinely noncommuting effective observable needed to escape
the raw-frame bottleneck; its phase-sensitive signal is the same first moment.

For each measured word pair (w,v), the FULL joint readout probability is

    P(w,v,+/-) = (1 +/- cos(theta_w-theta_v))/(2*D^2).

Thus a polynomial-work classical readout counterpart chooses two independent
uniform words, evaluates their original-data frequencies and phases, and
draws the displayed ancilla coin. It reproduces word-pair, symmetry and
equality flags, not just the final acceptance rate. Certified finite-precision
coin sampling is not implemented in this module; its numerical/abort losses
must be paid in production. The formula is not a classical simulation of
coherent amplification or an unmeasured entangled output.

The ideal source has R=C and no antisymmetric collision mass. An IID raw-value
null has mean R=1/D conditional on public labels, so its antisymmetric
collision mass is (C-1/D)/2. Low-degree finite signals cannot bypass the
classical measured counterpart or the rare equality-event price.

## Noise-Compatible Conditional Signal, With Its Correct Price

For original errors e INDEPENDENT of IID full-root public labels, freeze e
and average over labels. Every distinct word pair collides with probability
1/N, independently of its frozen error phases. If
f_e=|D^-1 sum_w exp(i*theta_e(w))|^2, then EXACTLY

    E_A(C_A-R_y) = (1-f_e)/N,
    E_A C_A = [1+(N-1)/D]/N.

The usual native second-moment displacement bound gives
E(1-f_e)<=min(1,80*M*V/q^2). Consequently the conditional SOURCE
antisymmetric probability over source draws AND unamplified equality branches
is at most loss/[2*(1+(N-1)/D)]. The IID-null conditional probability is
(1-1/D)/[2*(1+(N-1)/D)]. For M=nr+12 this can give a large conditional gap.
It is not a per-realized-bank guarantee. Correlated label/error sources do
not inherit the factor1/N argument merely from marginal error moments.
Two complete81-bank mod3 censuses verify the distinction. Fixed errors give
E(C-R)=(1-f_e)/N exactly. With the label-dependent calibration errors e_i=-a_i,
all actual responses are0 and E(C-R)=0, whereas (1-E f_e)/N=8/27.
The independence premise is substantive, not bookkeeping.

But equality succeeds only about1/N. Ordinary two-reflection amplification
using the ACTUAL known initial preparation obeys

    E P_equal_after_t <= (2*t+1)^2 * E C_A.

Constant mean equality mass requires order sqrt(N) iterations in this
specified family. Amplification changes the weighting of public label banks;
the unamplified conditional noise guarantee is NOT automatically inherited.
Generic state/gate trace errors also cannot be divided by a rare branch
without a separate relative or appropriately small absolute bound.

## Research Decision

This is an explicit joint two-word observable, not a free abstract span
projector. Its effective word measurement still commutes with the raw Gram.
Its implementation and failure modes show why a
promising POSTSELECTED gap is insufficient. Keep it as a constructive
collective/classical comparator. Do not promote it as a breakthrough.
A useful next mechanism must avoid the rare-event price, the full measured
classical law, or both, while retaining real-source noise guarantees.

    python theorems/native_word_collision_symmetry.py --write
    node research/certificates/native_word_collision_symmetry_crosscheck.js
    python -m pytest -q tests/test_native_word_collision_symmetry.py
