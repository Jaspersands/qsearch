# Projected Slater Born sampling: a narrow Gaussian-feedback test

2026-11-13. REVIEWED WRITTEN architecture falsifier; parent verified the full independent attack. This is
an architecture falsifier, not a general sampling lower bound.

## Native problem and mechanism selected for one decisive test

An explicit rational complex 2s-by-s isometry V specifies an s-particle
Slater state Phi. Partition modes into s pairs, and let Q retain exactly one
particle in each pair. Promise Z=||Q Phi||^2>0. The output is a spin word
with Born probability |det V_(chosen modes)|^2/Z, within TV epsilon. All
matrix bits are native input; no normalizer, conditional marginal, source
state, gap or inverse oracle is supplied. Initial Slater preparation is
polynomial; bare postselection/amplification pays 1/Z or 1/sqrt(Z).

The tested operation prepares Phi, measures every pair's parity coarsely,
retains ALL records, applies arbitrary outcome-conditioned possibly randomized
Gaussian unitaries on the SAME modes, then measures physical occupations.
Gaussian includes number-nonconserving quadratic fermionic unitaries. It
includes changing successful as well as failed branches. No ancillas, further
intermediate measurements, rejection, or arbitrary classical outcome
relabeling is part of this specific architecture. Target probabilities are
embedded in the full occupation alphabet, with zero on invalid records.
A polynomial clock for this operation would bypass normalization, but its
correctness is the decisive first gate.

Corpus and baseline lookups are in the independent selection review. Classical
comparators include exact determinants, ordinary DPP sampling followed by
rejection, and product/bounded-width contraction cases. General constrained-
DPP mixing and complexity are not declared settled. The actual retained
Bravyi quant-ph/0404180v2 Eq4/5 (LF117-139) was inspected: Gaussian unitaries
rotate Majorana operators by a real orthogonal matrix. Thus covariance
conjugates orthogonally for ANY state, even a non-Gaussian parity branch.
No Gaussian-state update theorem is applied to a coarse two-mode projector.

## An earlier counterexample had an important sampling repair

For u=(3a+4c)/5,v=(3b+4d)/5, pairs (a,b),(c,d), the successful projected
state is the singlet with a fair two-word Born law. The even branch is
(9|ab>+16|cd>)/sqrt337. Covariance prevents coherently mapping it to the
singlet by a Gaussian unitary. That does NOT refute Born sampling: swapping
b,d gives (9|ad>-16|bc>)/sqrt337, and randomly swapping both spin pairs
makes the measured two-word law exactly fair. This parent correction is
accepted in the revised independent selection report. The block product of
this example is classically trivial and Gaussian-feedforward samplable.

## Opposite-angle counterexample for the stated sampling architecture

Instead use rational orthonormal orbitals

    u=(3a+4c)/5, v=(4b+3d)/5,
    Phi=(12|ab>+9|ad>-16|bc>+12|cd>)/25.

Coarse parity measurement gives

    O=(9|ad>-16|bc>)/sqrt337, probability337/625;
    E=(|ab>+|cd>)/sqrt2, probability288/625.

The target is the occupation law of O and has P(a occupied)=81/337.
E has one-body density I/2, zero anomalous two-point functions, and therefore
zero Majorana covariance. O has covariance operator norm lambda=175/337.
For any state with covariance norm at most lambda, every physical mode has
occupation expectation in [(1-lambda)/2,(1+lambda)/2], since the relevant
covariance entry is bounded by its operator norm. Gaussian unitaries preserve
this norm; convex mixtures preserve the resulting expectation inequalities.

Consequently every allowed feedback on E leaves P(a)=1/2, and every allowed
feedback on O has P(a)>=(1-lambda)/2=81/337. The UNCONDITIONED output obeys

    P_out(a occupied)>=(337/625)*(81/337)+(288/625)/2=9/25.
    TV(P_out,P_target)>=9/25-81/337=1008/8425.

This argument covers randomized feedback, feedback on both records, and
number-nonconserving Gaussian unitaries. It makes no assumption that feedback
already yields valid occupations; the marginal-event bound holds on the
full physical occupation alphabet. It does not apply if arbitrary classical
output remapping is permitted, or to ancillary/instrument/non-Gaussian
strategies. In particular a classical algorithm trivially samples this
four-mode target; no hardness or universal quantum no-go follows.

## Review, control and next action

The exact Sage covariance control is in
`audits/controls/slater_gaussian_feedforward/`; it uses explicit16-dimensional
fermionic matrices to check branch norms and covariance, not a finite scan
over unitaries. The universal feedback bound is the analytic norm argument.
Independent Opus/high attack completed/end_turn, session3527 reaped exit0.
The full report was read; its covariance/marginal proof was independently
checked, and the exact Sage run completed with the stated rational values.
Packet: `audits/api_inputs/2026-11-13-slater-moment/`; bundle:
`audits/claude_runs/2026-11-13-slater-moment-attack/`. Reported usage2239 input,
6890 output, runner estimate0.146756USD. This is neither an invoice nor a
remaining-balance measurement. No OpenAI call or retry.

Disposition of material report claims:

- ACCEPT the expansion, branch weights, covariance norm, unconditioned
  marginal bound, convex-randomness argument and TV>=1008/8425. Identity
  feedback attains the marginal lower bound, not a proved tight TV bound.
- ACCEPT the general record-wise inequality
  sum_r p_r(1-sigma_r)/2 <= P(n_j=1) <= sum_r p_r(1+sigma_r)/2,
  where sigma_r is each post-measurement covariance's operator norm.
  Eq5's operator identity was checked in the actual retained primary source.
- REPAIR the sentence saying every quadratic expectation of E vanishes:
  number expectations are1/2. Off-diagonal and anomalous correlators vanish,
  and CENTERED covariance is zero, which is the property the proof needs.
- REJECT the report's exclusion of Gaussian-rotated mode readout: a final
  Gaussian rotation is already absorbed into the permitted feedback. The
  report's description of the first singlet repair as classical relabeling
  is also wrong; it uses allowed physical Gaussian permutations and a coin.
  These errors do not affect the new opposite-angle marginal obstruction.
- REPAIR the outside-scope Gaussian-channel explanation: a channel with a
  fresh covariance-bearing environment can have Gamma -> A Gamma A^T+B,
  not merely orthogonal conjugation or contraction. Thus zero covariance
  need not stay zero with ancillas, reset or loss. No claim about such
  channels, more parity measurements, or non-Gaussian correction is made.

The revised176-line independent selection report was fully parent checked.
Its other candidate, same-component tensor lifting, has two scoped failures:
a rational quartic tensor with rotated real decompositions can give different
latent eighth moments (9/32 versus17/64), and literal q-copy label equality
has success r^(1-q) for uniform weights. The former blocks recovering a
prescribed latent moment without identifiability, not finding ANY valid
decomposition; the latter blocks only that filter. No tensor hardness or
quantum lower bound is inferred; unread decomposition sources remain UNKNOWN.

This pass closes the named Gaussian-feedback architecture at its actual
Born-output contract. The general projected-Slater sampler remains OPEN.
Next concrete admission check: corpus lookup then actual literature on
partition-conditioned DPPs with every part of size TWO and exactly one
chosen element, equivalently mixed-discriminant weights from rank-two PSD
summands. Compare their native representation, accuracy and dependence on
the NUMBER of parts before proposing any new quantum correction. No generic
sampler prompt or adjacent normalization sweep is queued.
