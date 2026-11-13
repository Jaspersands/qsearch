# 2026-11-13 — Independent selection after the sparse-constant pass

**Decision: admit neither operation.** These are two independent, externally
motivated native problems, but neither currently has a new end-to-end quantum
route. The first has the clearer native target and higher priority IF a new
operation appears. The scoped failures below do not prove hardness of
either problem. No nearby coherent-transform, fullRel, or HSP continuation
is recommended, and no paid construction request is justified by this screen.

Read current STATE/TRAPS/GOAL. Used the required order, separately for each:
`tools/corpus/cli.py been-tried` then `baselines`, with the queries
“Gutzwiller projected Gaussian BCS state sampling local number projection”
and “overcomplete tensor decomposition coherent component locking tensor
power lifting” (shortened to their mathematical nouns for baselines).
The former returned the CLOSED folded total-number-projection note and
generic normalization precedents; the latter returned lexical tensor/HSP
hits, not an admitted overcomplete decomposition algorithm. The baseline
catalogue returned tensor contraction, plus an irrelevant decoding hit.
Those retrieval results establish neither novelty nor a classical gap.
Only the actual retained Bravyi source, specified below, is used as a
literature theorem here. No archive, network, API, Git, or finite sweep was used.

## 1. Half-filled projected Slater states: full spin Born sampling

**Native input/output.** Input a rational complex 2s-by-s isometry V,
polynomial-bit entries, and error epsilon. Its occupied Slater state is

 |Phi_V> = product_(a=1)^s (sum_(i=1)^(2s) V_ia c_i^dagger)|vac>.

Group modes into s physical spin pairs. Let Q project onto exactly one
occupied mode in every pair, and promise Z=||Q Phi_V||^2>0. Output a spin
word z in {0,1}^s within TV epsilon of

             Pr(z)=|det V_(I(z),:)|^2/Z,                       (1)

where I(z) chooses one mode per pair. Neither Z nor conditional completion
probabilities are input. This is a concrete constrained determinantal law,
motivated by half-filled projected fermion trial states; it is not the
folded-chain homogeneous total-number identity previously closed.

**Proposed operation and full resource target.** Prepare the Slater state
from the explicit isometry using ordinary Givens rotations, measure local
pair parities, and recycle every record by efficiently computed Gaussian
feedforward instead of rejecting it. If valid, this would supply a
poly(s,B,log(1/epsilon)) native sampler, without a Hamiltonian ground-state
oracle, gap promise, QRAM, or trial-state advice. Preparation/inversion of
the initial Slater circuit itself costs polynomial input size. Bare
postselection/amplification instead pays respectively 1/Z or 1/sqrt(Z).

**Exact control: coherent repair versus Born sampling.** Two sites a,b and c,d have
rational orthonormal occupied orbitals

       u=(3a+4c)/5,  v=(3b+4d)/5.

The input state is

       (9|ab>+12|ad>-12|bc>+16|cd>)/25.

The valid branch has probability 288/625 and is the singlet
O=(|ad>-|bc>)/sqrt(2). The other pair-parity branch is
E=(9|ab>+16|cd>)/sqrt(337). O has one-body density I/2 and zero Majorana
covariance. E has occupations 81/337,81/337,256/337,256/337, no anomalous
two-point correlations, and Majorana covariance singular values 175/337.
Gaussian unitaries conjugate covariance by a real orthogonal matrix.
Thus NO Gaussian unitary on these modes maps E to the COHERENT state O.
This does not exclude the native Born endpoint. Swap modes b and d in E,
giving (9|ad>-16|bc>)/sqrt(337). With a fair classical coin apply either
the identity or simultaneous swaps (a b)(c d), then measure. Each of ad,bc
has probability (81+256)/(2*337)=1/2, exactly O's Born law. The odd branch
was already fair. These permutations are Gaussian unitaries; their fermionic
signs do not affect the measured probabilities. Independent block repairs
therefore give an exact polynomial Gaussian-feedforward sampler on this family.
For b blocks bare postselection still succeeds only with (288/625)^b.
That exponential normalization cost is NOT a sampling lower bound.

There is also a direct closure obstruction: the two-particle coefficients
of O violate the Slater Pluecker equation
f_ab f_cd-f_ac f_bd+f_ad f_bc=0. Consequently the coarse odd-parity
projector is not a Gaussian-state update. Bravyi's actual retained source,
`sources/2026-11-13-folded-gaussian/bravyi_flo.txt`, Section VIII LF853–903,
provides covariance updates for SINGLE-mode projectors n_j and 1-n_j.
Here P_10+P_01 retains coherence between two alternatives. Neither that
source nor the closure obstruction decides the randomized sampling question.

**Classical comparison and remaining gate.** Unconditioned Slater sampling
and each point weight in (1) have polynomial determinant/Gaussian routines.
Rejection samples (1) with cost 1/Z. Product blocks, and bounded-width
contraction families, are additional matched cases. Measuring all modes
Gaussianly does not magically condition on future one-per-pair events.
A polynomial classical oracle for those completion probabilities would
already give a classical sequential sampler, so it cannot be free advice
in a quantum Doob/bridge proposal. General constrained-DPP or MCMC bounds
have NOT been source-checked here and are not declared inefficient.

Only deterministic Gaussian coherent branch-to-target correction is refuted.
Randomized Gaussian feedforward for Born sampling of GENERAL V remains OPEN;
the explicit repair above settles only the block family. No general sampler
or efficient conditional-completion routine is constructed here. The earlier
wording rejecting Gaussian feedforward for the Born endpoint was too strong
and is withdrawn. Do not commission another bare-postselection barrier review.

## 2. Overcomplete moment decomposition: coherent same-component lifting

**Native input/output.** Input the full rational symmetric quartic tensor
T=sum_(a=1)^r lambda_a v_a^tensor4, with r supplied, positive weights
summing to one and real unit vectors, promised to have such a representation.
Return a representation with at most r terms and prescribed small residual;
weights/vectors are NOT supplied. If recovering the original components
is intended, a precise uniqueness/stability promise must first be stated.
This is a native latent-mixture/algebraic search problem, distinct from
planted single-spike tensor PCA. Reading/preparing the explicit n^4-entry
tensor is charged; there is no free component sampler or purification.

**Candidate operation and conditional target.** A coherent lift that made
the SAME unknown component occupy q registers could turn nearly parallel
component vectors into distinguishable tensor powers, permitting spectral
separation and factor readout. The hoped-for clock is polynomial in native
input/output size and accuracy, even for q=Theta(log n), where explicit
feature coordinates number n^Theta(log n). It still must pay preparation,
normalization, whitening, eigenvector selection, and recovery of all r
classical vectors. A smaller quantum feature register alone pays none of
these. No asymptotic advantage is established by the supplied sources.

**Two exact falsifiers of the proposed lift.** First, native T does not in
general determine the requested higher latent moments. In dimension two,
take four equally weighted projective directions at angles
0,pi/4,pi/2,3pi/4. Their quartic form is

                  (3/8)(x^2+y^2)^2.

Rotating all directions by pi/8 gives the SAME rational quartic tensor.
But the eighth moment in direction (1,0) is respectively 9/32 and 17/64.
Thus no channel whose only input is this tensor's amplitude state can
output the two different prescribed latent eighth moments. Returning ANY
valid decomposition remains possible; choosing one is exactly the search
problem, rather than an available lifting oracle.

Second, grant the much STRONGER source
sum_a sqrt(lambda_a)|a>|v_a>^tensor4. On q fresh copies, literal equality
filtering of all latent labels succeeds with probability sum_a lambda_a^q.
For uniform weights this is r^(1-q), so amplification costs
r^((q-1)/2), quasipolynomial when r=n^Theta(1), q=Theta(log n).
This formula needs no orthogonality of v_a. Independent tensor powers of
the native amplitude state contain mixed component tuples; calling them a
same-component moment is incorrect. This rejects the named equality-filter
mechanism, not every nonlinear quantum lifting algorithm.

**Classical comparison.** With linearly independent v_a and r<=n, two
quartic contractions give M_x=V diag(lambda_a (v_a.x)^2)V^T and M_y
analogously. On their common column space, a generalized eigenproblem
recovers the directions when the ratios are distinct. This is a direct
classical matrix-algebra attack on the favorable spectral case. If a
high-order moment is explicitly provided, its reading/preparation size
must be compared to classical flattening at that SAME order. Actual
overcomplete tensor-decomposition theorems and their rank, conditioning,
randomness, and BIT scopes have not been read locally: that scope is
UNKNOWN, not a claimed superpolynomial classical baseline.

## Decision and precise source boundary

Neither operation currently supports an end-to-end admission or implementation.
The projected-state question ranks first by external value because (1)
is a complete native target with exact determinant formulas for unnormalized weights;
the tensor proposal additionally lacks a well-defined latent-lift input.
There is no currently admissible next quantum hypothesis from this pair.

If an explicit new operation is later supplied, the source requests are:
Gros, *Physics of projected wavefunctions*, Annals of Physics 189 (1989),
53–88, for the actual projected-state/VMC contract; and Anandkumar–Ge–Hsu–
Kakade–Telgarsky, *Tensor Decompositions for Learning Latent Variable Models*,
JMLR15 (2014), plus Ge–Ma, *Decomposing Overcomplete 3rd Order Tensors using
Sum-of-Squares Algorithms*, for the exact matched rank/accuracy premises.
These unread works are requests, not evidence or theorem imports. A
modern constrained-DPP/overcomplete baseline must also be matched before
any admission. No fetch is needed merely to reconfirm the exact controls
above, and no generic “find an efficient sampler/lift” paid prompt is proposed.
