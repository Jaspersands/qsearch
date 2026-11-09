# Gaussian channel mixture: robust low-rank reduction

2026-11-07. CLOSED mathematical review of the new reference-invariant
low-rank proposal in the current Gaussian-channel pass. Read STATE/TRAPS
and `GAUSSIAN_CHANNEL_MIXTURE_ADMISSION.md`; reuse the proved state
support/Schur identities and the exact program norm lemma in
`2026-11-07-gaussian-channel-continuity.md`. No network/API, Git, new code
or finite experiment. Small-H rank-two repair and physical processor
compilation are separate tasks and are not certified here.

**Verdict:** the proposed low-rank geometry, physical reference state,
degree-eight data identity, core inversion and near-TP normalization are
sound. Arbitrarily small principal angles require no extra input promise.
The result is a stable reduction to the separately specified deterministic
processor compilation. Applying a nonunitary normalizer by uncharged
postselection would not complete that endpoint.

## 1. Reference-invariant support without a hidden angle gap

Use Pi for the reference Majorana projector. The normalized reference-first
Choi components Gamma_j are physical real skew 4n-by-4n matrices with
`Pi Gamma_j Pi=0` and strict margin `I +/- i Gamma_j >= k I`.
Write q=1-p, Delta=Gamma_1-Gamma_2 and E=sqrt(pq) Delta. This review is
in the LOW THIRD, non-small-H branch. The previously proved moment/Gram
analysis, with internal parameter u=k^2 and h=u^8, ell=u^40, supplies an
estimated rank-four orthogonal projector P satisfying

    ||Delta-P Delta P||op <= tau0,   tau0<=u^10.            (1)

The uniform low-branch lower bound on pq is already part of that analysis;
there is no new minimum-weight premise or weight-estimation operation.

Let U be an orthonormal 4-column matrix for P. Separately take truncated
left singular spaces of Pi U and (I-Pi)U. Discard singular values of size
at most a constant times theta=u^20, and retain only values at least a
constant times theta. This can be done with a certified guard band: there
are at most four singular values in each matrix, so a constant grid of
thresholds in [theta,2 theta] contains one separated from all of them by
a constant times theta. Computing to smaller precision supplies the
decision. This is a chosen numerical separation, not a promise about
principal angles of the unknown support.

Pad each retained reference/output subspace to even dimension, at most
four each, and call the resulting orthogonal projector Q. Padding inside
each original register is always possible since that register has even
Majorana dimension. Orthogonal complements can be constructed using
ordinary stable linear algebra. Then

    Q Pi=Pi Q,  rank(Q)<=8,  ||(I-Q)P||op=O(theta).        (2)

The last estimate follows directly from the discarded singular values
of the two four-column matrices: their Frobenius residuals are O(theta).
It does not require Q to approximate a uniquely defined exact enlarged
support. Using ||Delta||op<=2, (1)--(2) give

    ||Delta-Q Delta Q||op <=2 tau0+O(theta)=:e_tail.        (3)

Thus very small projected directions can be discarded safely; inverting
their principal angles is unnecessary. The retained SVD/orthogonalization
uses inverse powers of theta only, hence polynomial resources under the
specified parameter hierarchy. Register-local rotations preserve (2)
exactly as a structural constraint even after gate approximation.

## 2. A nearby pair of proper physical channels

Let Gamma be the attenuated mean covariance. Project the measured mean in
Frobenius norm onto the real-skew matrices satisfying the reference block
zero and operator norm at most 1-k/2. Call the result Gamma_hat and let
`mu=||Gamma_hat-Gamma||op`. The true mean is feasible, so the projection
does not increase its Frobenius error. All constraints are polynomial-size
convex matrix constraints. An approximate calculation can retain the block
zero exactly and restore a small norm violation by uniform rescaling.
No ill-conditioned equality constraint involving the unknown weights is
solved. On the simultaneous moment event, mu is polynomial(n) times the
chosen mean precision and is much smaller than k.

Define the analysis-only pair

    Delta'=Q Delta Q,
    Gamma_1'=Gamma_hat+q Delta',
    Gamma_2'=Gamma_hat-p Delta'.

Since Q commutes with Pi, `Pi Delta' Pi=0` EXACTLY. Both new Choi matrices
therefore have reference block zero. Their respective operator errors are
at most mu+e_tail, uniformly in the weights. For the displayed hierarchy
this is less than k/2, so both remain physical with margin at least k/2.
They are the Choi states of proper Gaussian CPTP channels in the fixed
reference-first convention. The pair is not explicitly recovered by the
low branch and supplies no hidden advice.

Outside the at most eight-dimensional T=im(Q), the two matrices share all
blocks. The Schur construction from Gamma_hat and T therefore gives a
single standard Gaussian state map Psi and physical core Gaussian states
with a mixture sigma, such that Psi(sigma) is exactly this nearby Choi
mixture. The core has at most four modes, Hilbert dimension r<=16. The
Schur matrix R_core obeys `R_core>=k/2`; its square root is the invertible
core-to-T block. The constructed mean's strict margin also pays the
inverse of `I+B^2` in the common complement.

The single-channel continuity theorem bounds replacement of the original
attenuated channel mixture by this nearby proper mixture by
`O(n sqrt(mu+e_tail))` in raw diamond norm. This uses component covariance
closeness, not the state trace norm of their average Choi matrix. With
u=k^2 and (3), the tail contribution is O(n k^10), well within the
proposed outer error budget.

## 3. Restricted data do not incur the tail error

For each component, restriction to T gives exactly

    Gamma_j'|T - Gamma_j|T = (Gamma_hat-Gamma)|T.           (4)

The discarded part of Delta disappears upon this restriction. Every
degree-two, four, six and eight moment restricted to T is a Pfaffian of
one of these restricted component covariances, followed by the same
mixture weights. Because T has dimension at most eight and the matrices
are contractions, these Pfaffians have universal Lipschitz constants.
Thus the original measured restricted moments differ from the nearby
target's moments only by O(mu), plus measurement and arithmetic errors.
There is NO e_tail term in (4).

It is enough to estimate all even Majorana moments up to degree eight.
There are O(n^8) such moments, each a directly measurable Pauli observable
on a fresh Choi copy. If every original coefficient error is at most zeta,
their exterior Euclidean errors are O(n^4 zeta). Restriction by an
orthonormal T frame cannot increase these exterior norms. This uniform
event covers adaptively chosen T; independence from the earlier support
estimate is not required. Exact fresh memoryless channel uses pay these
copies. No coherent source inverse or branch labels are consumed.

## 4. Constant core inversion and stable physical repair

The reduced state map to T has characteristic-function action

    M_out=exp(omega_A0) * (sqrt(R_core))^(wedge) M_core.

Consequently invert it by multiplying by `exp(-omega_A0)` and applying
the exterior powers of `R_core^(-1/2)`. Its covariance noise A0 is a
contraction: it is a principal block of the physical Gaussian output
noise state. On degrees at most eight the inverse operator norm is
therefore bounded by `C k^-4`, with universal C. The finite exterior
exponential contributes only a constant factor. This argument is valid
for a general even core, not just Gaussian cores.

All even moments through degree eight determine the entire at-most-four-
mode even density matrix. Reconstruct it, project to the PSD trace-one
parity-block set, and normalize if necessary. In constant dimension this
gives a physical even tau with

    ||tau-sigma||1 <= C k^-4 (mu+n^4 zeta+e_arith).        (5)

Here e_arith is the error after converting to restricted moments and
forming the known inverse, expressed in compatible output-moment units.
No small density eigenvalue is inverted during PSD repair. In particular
the discarded support error is not multiplied by k^-4.

For completeness, forming the inverse also has a polynomial error clock.
With matrix arithmetic error b, `D=(I+B^2)^-1` has error O(b k^-2), as
do R_core and A0. On the strict-margin domain R_core^(-1/2) then has
error O(b k^-7/2); its degree-eight exterior action has error bounded by
O(b k^-7), apart from polynomial(n) coordinate factors. The thresholded
support calculation adds only fixed inverse powers of theta. These are
fixed polynomial losses, dominated by zeta=u^10000 after budgeting the
arithmetic to that scale. This is not an appeal to precision without a
conditioning bound.

## 5. Constant reference support and near-TP normalization

The range of Psi's core matrix L lies in T. Its reference projection is
therefore contained in the at-most-four-dimensional reference part of T.
Because the nearby target has zero reference covariance,
`Z_R=-L_R Gamma_sigma L_R^T` is supported there as well. The all-operator
marginal proof in the continuity review applies: after a known reference
rotation, `Psi_R(tau)=T_ref(tau) tensor I_rest/D0`. The active reference
Hilbert dimension is h<=4, while r<=16. The corrected ordinary CP program
map therefore has norm at most r h<=64. Reference gauges and the explicit
program/input cross-CZ are retained as in that review.

Let Phi_tau be the CP channel candidate from the physical core tau, and
Phi_sigma the proper nearby reference channel. Put
`d_core=||tau-sigma||1`. Then

    ||Phi_tau-Phi_sigma||diamond <=r h d_core,
    ||F-I||op<=r h d_core,  F=Phi_tau^dagger(I).

For this error below 1/2, F is invertible and the exact map

    Phi_hat=Phi_tau composed_with Ad(F^(-1/2))

is CPTP. F is a constant-dimensional positive matrix tensored with the
identity, up to the known input rotation/gauge. There is no unstable
linear feasibility inversion. Writing f=||F-I||, one has
`||F^(-1/2)-I||<=2f`, `||F^(-1/2)||<=sqrt(2)` and
`||Phi_tau||diamond=||F||<=1+f`. Thus

    ||Phi_hat-Phi_sigma||diamond <=10 r h d_core.           (6)

This proves the normalization's mathematical stability. It does NOT
authorize a standalone heralded F^(-1/2) filter followed by retrying the
consumed input. A deterministic compiled implementation of the composite
map, including its retained Kraus environment and any amplification, is
the separately reviewed physical endpoint. That endpoint and the small-H
rank-two repair remain outside this closed robustness verdict. No full
learner or quantum execution is inferred here.
