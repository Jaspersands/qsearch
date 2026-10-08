# Native Access To Secret-Phase Spectral Generators

LOCAL DERIVATION / REVIEW PENDING. An access boundary for a SPECIFIC
nondemolition-generator proposal, not a generic receiver lower bound, new
quantum algorithm, hardness theorem or novelty claim.

## Why This Is The Next Question

Sequential spectral extraction is useful GIVEN matrices/state with certified
original moments. It does not say how native inputs supply them. Consider
the actual M-qutrit source, with public frequency map F and unknown secret s:

    psi_s = D^(-1/2) sum_x chi_q(F(x).s)|x>,
    D=3^M, G=q^n, q=3^r.

A tempting shortcut is a public generator U_d acting approximately as
U_d psi_s=chi_q(-d.s) psi_s. The minus sign comes from translating frequency
FORWARD; its spectral measurement would directly encode
a secret character. This is a STRONG nondemolition condition. General
measurements need not satisfy it, and no result below rules those out.

## Commuting With Encoding Means No Signal

Write E_s=diag(chi_q(F(x).s)). If every projector in a sequential instrument
commutes with every E_s, its path vector is E_s times the corresponding
path vector on the flat known state. Their norms agree. Every complete
outcome distribution is therefore independent of s. The statement includes
public-label-dependent operators, independent ancillas, adaptive choice from
commutant projectors, and classical processing of the paths. It does NOT
include noncommuting mixing steps or a secret-bearing extra source.

Easy public word-diagonal phase gates are in this commutant. Spectral
measurement of them cannot realize the known-support generators used by
the conditional calibrations. They are not a native learner.

## An Exact Optimum For A More Generous Shortcut

Let C_y=|F^-1(y)| and v_y=C_y^(-1/2) sum_(F(x)=y)|x> for occupied y.
These uniform fiber vectors are orthonormal. Fix a nonzero d and allow ANY
public unitary U, even exponentially expensive and chosen from all labels.
Averaging uniformly over all secrets gives

    E_s Re[chi_q(d.s) <psi_s,U psi_s>]
      = (1/D) sum_y sqrt(C_y*C_(y+d)) Re<v_(y+d),U v_y>.

Every displayed matrix element has real part at most1. Conversely the
partial assignments U v_y=v_(y+d), whenever both fibers are occupied, are
injective between orthonormal sets and extend to a complete unitary.
The optimum is therefore EXACTLY the shifted frequency Hellinger affinity

    A_d = (1/D) sum_y sqrt(C_y*C_(y+d)).

Consequently the minimum mean squared nondemolition phase error is

    min_U E_s ||U psi_s-chi_q(-d.s) psi_s||^2 = 2*(1-A_d).

This is an optimality calculation for this target, not efficient synthesis,
simultaneous commuting generators, finite-order constraints or a measurement
success probability. Relaxing those requirements only strengthens the lower
bound as an access falsifier.
Appending independent clean ancillas and conjugating by a secret-independent
isometry does not remove this norm-error boundary: the same matrix-element
upper bound holds on the orthonormal embedded fiber vectors. Source-changing
measurements, discarded outputs and differently learned moment models are
not silently reduced to this nondemolition condition.

For word PERMUTATIONS the optimum is instead

    A_d,perm = (1/D) sum_y min(C_y,C_(y+d)).

Match as many words as possible between each source and translated fiber,
then complete the leftover bijection. This proves attainability. Exact
translations exist iff counts are invariant under d. A whole unit basis
of exact translation permutations forces every fiber count to be equal;
therefore G divides D. The underfull source D=G/9 cannot have such an action.
This is not a prohibition on partial translations or another receiver.

## Population Bound On The Real Native Label Law

For any two DISTINCT words, their frequency difference contains a unit
coefficient (+/-1 or +/-2) of at least one independent full native row.
It is uniform in Z_q^n even at composite q. For a FIXED nonzero d selected
BEFORE the labels, the expected number of ordered shifted word pairs is
D*(D-1)/G. Integer counts satisfy sqrt(ab)<=ab when a,b>0. Thus

    E_labels A_d <= min(1,(D-1)/G),
    E_labels min_U mean_secret_error >= 2*(1-min(1,(D-1)/G)).

U may depend on every label: the per-label optimum is bounded BEFORE
averaging. At M=nr-2 this lower bound is strictly greater than16/9.
It rules out accurate phase generators of this form on the unchanged
underfull batch, even if their gate cost is ignored. Fixed d=e_j and
d=(q/3)e_j cover full-coordinate and least-trit nondemolition targets.
It does NOT cover a label-chosen unit-difference basis by pretending its
directions are independent of the labels. An explicit adaptive-offset
countercontrol retains that scope distinction; one instance is not by itself
an ensemble counterexample.

The obstruction correctly weakens with more copies. Put p_y=C_y/D and
u_y=1/G. The native pair law gives E[chi2(p,u)]=(G-1)/D. The triangle
inequality for sqrt(p), its shift and sqrt(u), together with
2*(1-sum sqrt(p*u))<=chi2, gives

    2*(1-A_d) <= 4*chi2(p,u),
    E[min_U mean_secret_error] <= min(2,4*(G-1)/D).

This grants the optimum at no circuit cost. A modest logarithmic surplus
in M can make good generators EXIST on average, but does not compile them.
If all fibers are occupied, translations on their UNIFORM vectors extend
to commuting q-order unitaries by making the fiber-orthogonal complement
fixed. Implementing that basis needs a coherent fiber transform; evaluating
F, sampling inputs or listing one witness is not such a transform.

## Implemented Controls And Falsifiers

The module evaluates true native ring labels at q3/9, dimensions1/2/3 and
both underfull and overfull batches. Complete bounded fiber tables are
calibration ONLY. Exact integer pair counts and rational isqrt radical
intervals certify every overlap envelope. Dense numerical unitaries attain
the optimum in the finite controls; their floating residuals are not proofs.
Optimal reference permutations and secret-averaged phase errors are replayed.
The independent checker reconstructs the true chart, full word map, counts,
radical intervals, matching counts, fixed-offset ledgers and disclosure flags.
Entire bounded native label populations (9/81/81 matrices) also replay the
two-point and chi-squared laws, rather than estimating them from a few seeds.

Falsifiers: false complete fiber counts; underclaimed radical intervals;
permutation optimum disagrees with matching; a noncommuting receiver is
incorrectly rejected by this narrow gate; an adaptive direction is promoted
to a fixed-offset population theorem; dense fiber compilation is called free.

## Revised Research Decision

Do NOT substitute public diagonal gates for the supplied spectral model.
Do NOT require the unchanged underfull source to be an accurate eigenstate
of secret-phase generators; that shortcut is obstructed. Extra copies can
remove the information/existence obstruction, but the efficient fiber
transform remains the hard part. No new generic matrix machinery is needed.

The next positive task must state an actual, costed noncommuting operation
on the native input, or an explicit classical learner from native records.
For a dense-batch fiber proposal, demand a clean algorithm for normalized
fiber-state preparation/transport, with input-dependent errors and source
costs. A compact phase formula or ideal unitary existence is insufficient.
Reuse the existing nonlinear-cycle, carry-packet and ridge machinery only
when it supplies that missing operation rather than another existence proof.

Routine CLI/registry/UI integration and full production validation belong
to Gemini/Antigravity; these derivations stay review-pending and unaccepted.
