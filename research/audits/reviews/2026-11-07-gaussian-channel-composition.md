# Two Gaussian channels: final composition and resource review

2026-11-07. **ACCEPT the written all-size composition with the compiler
precision clarification below.** Read STATE/TRAPS, the current complete-parent
section of `GAUSSIAN_CHANNEL_MIXTURE_ADMISSION.md`, the established mixed-state
numerical ledger, and the CLOSED continuity, low-rank and processor reviews,
including the latter's final near-TP/cutoff/robust-amplification addendum.
The rank-two repair and core-inverse reports were checked against their actual
proofs and the repository's norm conventions. No Git/network/API, new code,
new experiment or full learner execution. The finite controls do not prove
the uniform theorem.

The accepted contract is EVERY exact memoryless convex mixture of TWO full
ordinary Gaussian CPTP channels in the fixed reference-first/Stinespring
convention. No unknown environment, purification, inverse, controlled channel,
branch, weight or separation advice is used. With probability at least1-eta,
the output is an explicit usable ordinary CPTP circuit at raw diamond error
at most epsilon. The output can be improper. Complexity is polynomial in
n,1/epsilon,log(1/eta), with enormous fixed exponents. This is not a novelty,
classical-computational separation, practical-scale or executed-learner claim.

## Input model and the stronger product-experiment baseline

The source review fixes the full map, including odd input coherences. With
reference first, the known even Gaussian Omega differs from ordinary Bell
only by `V_R=product CZ_Ri,Rj`. Its full corrected Choi state is therefore
unitarily equivalent to the ordinary Choi state, not merely an even-input
surrogate. Ordinary memoryless uses would supply exact IID Choi copies.

In fact entangled references are unnecessary for the stated measurements.
Any Hermitian degree<=8 Majorana monomial is a signed ordinary Pauli
`P_R tensor Q_O`. Its corrected-Choi expectation is

`Tr[Q E((V_R^dagger P_R V_R)^T)] / D`,  D=2^n.

Clifford conjugation and transpose turn the reference factor into a KNOWN
signed Pauli P; transpose only changes the sign for odd numbers of Y factors.
For P!=I, uniform product Pauli eigenstates with total eigenvalue b have
density `(I+bP)/D`. Choose b uniformly from +/-1, query E once, and measure
the signed output Pauli Q with outcome m. Then
`E[b m]=Tr[Q E(P)]/D`. For P=I use uniform computational basis inputs,
whose ensemble is I/D. Overall signs can be absorbed in the recorded outcome.
These are bounded +/-1 estimators with the SAME Hoeffding cost as Choi copies.
Thus nonadaptive product preparations, individual ordinary channel uses,
local Pauli readout and CLASSICAL processing suffice for all acquisition.
No benefit from entangled references, coherent channel control or collective
measurements is established. The returned channel circuit remains quantum.

## Shared data event, thresholds and high branch

For n>=2 and epsilon<=1/10 use
`k=(epsilon/[10^8(2n+1)])^2`, `u=k^2`, `h=u^8`, `ell=u^40`,
`zeta=u^10000`. Constant-size ordinary CPTP tomography handles n=1;
n=0 is trivial, and larger epsilon can be capped at1/10.

There are O(n^8) measured moments. The displayed per-observable sample count
gives simultaneous coefficient error<=zeta with failure<=eta/4. Exterior
Euclidean error costs O(n^4), and every orthonormal restriction contracts it.
This ONE event controls the subsequently selected data-adaptive frame Q and
every bounded Rademacher restriction. Their selection does not require new
copies, conditional IID claims or a separate exponential union bound.

Scaling degree2j data by `(1-k)^j` is exactly the two-branch covariance
attenuation. It preserves RR=0 and supplies margin k. The full-channel
continuity theorem costs at most300n*sqrt(k); no attenuated oracle is queried.
Run the existing state reconstruction at internal parameter u on2n modes.
All its dimension factors fit `2n<u^-1`, its inverse ledger applies, and
the physical margin k>=u is stronger than that ledger requires.

The measured 2h/2ell tests allow overlapping true regimes; they require no
distance from a threshold. The high-branch lower weight and singular-value
bounds are DERIVED, not supplied. The accepted-restriction determinant and
Lefschetz/entry/E^3 guards are the distinct guards in the original ledger;
no extra demand that the B inverse itself have singular value>=u^300 is
introduced. Reused recovery gives branch covariance errors<=u^8000 and
weight error<=u^8300. Joint physical/RR-zero projection has a feasible true
branch and increases error only by polynomial dimension factors. The tiny
shrink and gap-free full-channel continuity leave the conservative
O(n*u^3000) diamond allowance. Weight errors cost their l1 error.

## Small H: no hidden small-weight or TP assumption

Here `a2(E)<=sqrt(3h/2)=sqrt(3/2)*k^8`. If min(p,q)<=k^8, comparing the
mixture and its Gaussian mean to the dominant component costs at most
`2k^8+400n*k^4`, after charging BOTH A and B parameter blocks. If instead
pq>=k^8/2, the top-pair truncation of Delta has operator tail<=sqrt(3)*k^4.
The checked reference-zero rank-two repair then costs at most a constant
times k^2, preserving margin at least k/2 for the displayed very small k.

Keep the same mean when moving the two covariances by q and -p times this
repaired difference. Its exterior square is zero, so every Pfaffian is
affine in the mixture parameter. The FULL corrected Choi mixture is exactly
the Gaussian mean, hence so is the full ordinary channel; this is not just
an even-input equality. Branchwise continuity costs O(nk). The rank-two
construction is analysis only: output the estimated, physically projected
RR-zero Gaussian mean. p=0 or1 is included without dividing by pq.

## Low third: the tail is outside the inverse

The state support estimate gives `||Delta-P Delta P||<=u^10` with slack.
Separate reference/output SVDs, a chosen guard band in[u^20,2u^20], and
padding each side to even dimension produce Q commuting with the reference
projector, rank<=8. There is no unknown principal-angle gap. Discarded
directions contribute O(u^20); only retained directions are normalized.
Thus `Delta'=Q Delta Q` retains RR=0 EXACTLY and has tail<=u^8.

Project the mean onto the strict physical RR-zero set. The analysis-only
nearby branches have this known mean and difference Delta'; both retain
margin>=k/3. Full-channel replacement costs O(n*u^4), before any inverse.
On Q, the restricted nearby covariance differs from the true restricted
covariance ONLY by the mean estimation error. The discarded tail is absent,
not subsequently multiplied by an inverse condition number.

The Schur construction gives a known exact Gaussian state map Psi from<=4
modes, R_core>=k/3, and an unknown physical even target program sigma. Its
reference support has<=4 Majoranas. All even core data are determined by
degree<=8 moments. Undo noise BEFORE core rescaling; the inverse norm is
at most a universal constant times k^-4. PSD parity-block clipping and
normalization require no density eigengap. The explicit retained-frame and
Schur inverse losses are far below the1900-power reserve between u^9900
array accuracy and the retained `||tau-sigma||1<=u^8000` claim. In particular
the tail u^8 is never amplified to become this program error.

## Near-TP repair, arbitrary inputs and actual deterministic output

The all-operator reference factorization, not a Gaussian-test-only identity,
gives r<=16, h_ref<=4 and CP program norm C<=64. Thus
`v=C||tau-sigma||1` bounds the FULL diamond error and `||F-I||`, with
F=Phi_tau^dagger(I). Its known active input block is constant-dimensional,
up to explicitly known rotations/reference gauges. The guard F>=I/2 passes
on good data. Taking B=F^-1/2 gives the exact CPTP map
`Q_tau=Phi_tau composed_with Ad_B`, at diamond distance<5v from the nearby
target (10v is a safe reserve). No unstable affine feasibility inversion.

The closed processor compiles Lambda/C with the actual-input cross-CZ,
known program PURIFICATION and normalizer B/sqrt2. Retaining every Kraus
workspace makes its successful block satisfy `K^dagger K=I/(2C)`. Coin
dilution and constant-count coherent amplification therefore act with the
same angle on every unknown input, including entangled inputs. Only the
known compiled circuit and its reverse are used. There is no source inverse,
unknown-input retry, exponential Bell outcome or final success conditioning.

For finite precision, use RECONSTRUCTION arithmetic u^12000, but request
successful-Stinespring compiler error u^1000 and a small-link cutoff u^1500.
The compiler has its OWN finite polynomial working-precision clock. Retained
links have inverse<=2u^-1500, bulk links equal1, and the residual polar step
has constant lower singular value. Choose evaluation tolerances from these
explicit operation bounds and the requested error; do not assert that one
universal u^12000 roundoff automatically pays all compiler stages. This
reevaluates only the KNOWN learned finite-description model, without new
data, increased moment accuracy or an unbounded residual-driven retry.

The cutoff compares successful Stinespring blocks directly; it never uses
dimension-amplified normalized Choi error. The closed addendum's singular-
value two-plane argument bounds amplification error even for unrelated
failure completions, by38*xi/sqrt(p), p=1/(2C). This is a constant factor.
Further approximation of the specific known circuit uses the ordinary
gate hybrid bound. The final circuit followed by discard is ALWAYS CPTP,
even with small residual flags. No exact synthesis of irrational gates,
tiny-link exact-zero decision or separated eigenbasis is assumed.

## Total resources, error and claim boundary

Attenuation300n*sqrt(k) is already less than2*10^-6 epsilon. The largest
remaining structural branch error is O(nk); the other displayed powers of
u are much smaller. With the conservative constants above and the separate
epsilon/20 gate budget, total RAW diamond error is below epsilon. The data
event and capped random restrictions have total failure<=eta/2. Numerical
guards pass on the good event; bad-data rejection/exhaustion is ABORT within
that budget. Output physicality does not depend on the data event.

Total ordinary query count is
`O(n^8 u^-20000 log(n/eta))`. Random restrictions have the stated finite
`ceil(4*3^12 log(8/eta))` clock. Every matrix dimension is polynomial or
constant, every inverse has a displayed margin/cutoff, and compiler tolerance
refinement has polynomial BIT cost. Classical processing and output circuit
size are polynomial. The guarantee is confined to the exact native two-map
memoryless promise and ordinary qubit operations. It is a written structured
channel learner; no implemented full learner, quantum execution, off-model
robustness, many-component extension, parity-restricted implementation,
novelty or separation is certified here.
