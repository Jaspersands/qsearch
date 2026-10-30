# A direct learner for finite-support noisy polynomial phases

Date: 2026-10-30. Status: reviewed mathematical reduction, public coefficient
adapter and bounded measurement controls. Not a physical mixed-source learner,
human-reviewed theorem, novelty certification, classical hardness result, or
reduction from standard LWE. Three independent automated reviewers checked the
core determinant identity and learner compatibility.

## Decision

This is a concrete application of low-rank antisymmetrization, but **not an
application that needs the Rees HSP receiver**. Relative-coordinate measurement
turns the exterior state directly into polynomial-phase packets accepted by
known phase elimination. An orbit-gap proof and the larger group construction
are unnecessary here. Do not use this family to claim a new hard HSP instance.

The useful output is an explicit learning reduction and a sharper filter on
future applications. Whether this exact composition is new remains open.

## Input and task

Let p be prime, n variable, and D fixed with 2 <= D < p. Define

    |psi_P> = p^(-n/2) sum_(x in F_p^n) omega_p^P(x) |x>.

The uniform-source contract supplies IID copies of

    rho = (1/r) sum_(b in B) |psi_(F+b.x)><psi_(F+b.x)|,

where F has total degree <= D and B has r distinct elements. Rank r is
polynomially bounded and known, with p not dividing r. Both F and B are unknown.
The components are orthonormal: their common F cancels in their inner products.

Recover the degree >= 2 coefficients of F. Constants are global phase, and
linear terms can be absorbed by translating B, so recovering all of F would
be an ill-posed task. Keep the unknown linear terms as nuisance parameters in
the learner; they cannot simply be dropped from the states.

There is NO evaluator, preparation circuit/inverse, chosen-coordinate source,
conjugate-state source, promise of repeated latent errors, or hiding oracle.
Classical samples of x from rho are uniform and reveal nothing about F. This
observation alone is not a meaningful general classical lower bound.

## Exterior measurement lemma

Published streaming antisymmetrization prepares the unique top exterior state
of the r-dimensional support. For its normalized amplitude,

    Omega(x_1,...,x_r)
      = omega^(sum_i F(x_i)) det[omega^(b_j.x_i)] / sqrt(r! p^(nr)).

Apply the public reversible coordinate map

    x_i = t + u_i (i < r),    x_r = t,    u_r = 0,

and measure u. Factoring a character from each determinant column gives

    det[omega^(b_j.(t+u_i))]
      = omega^((sum_j b_j).t) det[omega^(b_j.u_i)].

Consequently

    Pr[u] = |det[omega^(b_j.u_i)]|^2 / (r! p^(n(r-1))),

and every positive-probability outcome leaves the normalized pure state

    p^(-n/2) sum_t omega^(sum_i F(t+u_i) + (sum_b b).t) |t>.

The u distribution depends on B but not on F. It need not be uniform.
Determinant-zero outcomes never occur; no determinant is evaluated and no
outcome is postselected. The retained coordinate has uniform computational
probabilities. Approximation is charged to the full instrument/run, never
divided by the probability of a rare individual u.

Set s = sum_b b, J(x) = F(x) + r^(-1)s.x, and A_u = sum_i T_(u_i), where
T_u P(x) = P(x+u). The retained state is |psi_(A_u J)> up to global phase.
J is one fixed unknown polynomial for the entire run.

## Public-map learner compatibility

On degree <= D polynomials, A_u = r I + N_u, where N_u lowers total degree
strictly and N_u^(D+1) = 0. Since r != 0 mod p,

    A_u^-1 = r^-1 sum_(k=0..D) (-N_u/r)^k.

Modulo constants, D terms suffice. This inverse is a classical coefficient
map, NOT a quantum operation assumed to invert a hidden phase transformation.

Maintain the original common frame

    J = G + sum_k eta_k B_k    (mod constants).

For every new wedge and its measured u, compute the PUBLIC polynomials A_u G
and A_u B_k. Measure all but a fixed axis j, obtaining uniform y. Remove the
known restricted phase A_u G. The resulting univariate packet has public
coefficient rows Y_(u,y)[s,k] multiplying the SAME unknown eta in every leaf.
Existing elimination accepts different public Y matrices; there is no need
to repeat u or to learn a separate polynomial for each u.

Why no arbitrary-u obstruction occurs:

1. A_u is invertible, so independent coefficient-frame directions remain
   independent modulo constants.
2. It commutes with partial derivatives. If a basis polynomial depends on
   axis j, then so does its image under every A_u. On the full polynomial
   space the derivative remains nonzero since D < p.
3. Some nonzero coefficient polynomial in the other coordinates has degree
   at most D-1. Schwartz-Zippel gives acceptance at least
   a = 1-(D-1)/p for EVERY u, regardless of B's outcome distribution.
4. Translation never increases any coordinate exponent. Therefore the row
   of retained-axis power s belongs to the original fixed-axis space
   W_(j,s) = span{b_alpha: alpha_j >= s}, of dimension at most
   binomial(n+D-s,D-s). Restriction, shear merges, and affine frame updates
   preserve this invariant. Frame and axis stay fixed within each tree.

Apply the existing public-map SDE elimination with local retries, obtain a
nonzero Fourier equation in eta, and update the ORIGINAL J-frame. Repeating
recovers J modulo constants, hence the desired nonlinear part of F.

## Resources and error accounts

Let M = binomial(n+D,D)-1. A conservative expected number of wedge-derived
leaves from the existing pure-copy argument is

    E <= (M/a) product_(s=2..D) [B_s(M) p/(p-1)],

where B_s is the published diagonal-equation arity. The sharper fixed-axis
argument replaces M inside B_s by binomial(n+D-s,D-s); reviewers checked
that it survives this adapter. The implemented certificate deliberately uses
the conservative bound. The symmetric-SDE schedule has additional field
guards; D < p alone does NOT authorize that alternative implementation.

For total error epsilon, cap leaves at T = ceil(4E/epsilon), charging at most
epsilon/4 to exhaustion. Use the flat-source `SubspacePlan(r,T,epsilon/4)`.
With b = ceil(log2(4rT/epsilon)) it allows r^2 b growth attempts per wedge,
plus its initial copy. Raw noisy copies are bounded by T(1+r^2 b).
For r=1 there is no growth and exactly T copies suffice.

Every failed growth and rejected coordinate slice is paid. Reserve another
epsilon/4 for bounded SDE failure and epsilon/4 for the COMPLETE quantum
instrument implementation error. At most T SDE calls occur because each
merge has at least two leaf descendants; allocate <= epsilon/(4T) abort
probability per call and check every returned algebraic witness. This is a
backend obligation, not an implemented solver runtime bound in this module.

The register size is O(n log p). Each multiplexed SWAP costs that many
elementary swaps, not one gate. Coordinate subtraction, public polynomial
translation, correction, and approximate Fourier transforms have polynomial
cost in n, r, log p and precision at FIXED D. No ambient p^n table or r!
enumeration belongs to the algorithm. Determinants/statevectors below exist
only in bounded reference tests.

If r is unknown but an upper bound R is supplied for a flat source, estimate
Tr(rho^2)=1/r with SWAP tests to error <1/(4R^2), then round among 1,...,1/R.
O(R^4 log(1/epsilon)) tests suffice. Its training/error costs are NOT included
in `noisy_copy_envelope`, which explicitly requires exact known rank.

## Nonuniform weights: separate mathematical extension

**Follow-up:** the [peak-weight extension](PEAKED_PHASE_NOISE_LEARNING.md)
removes the input-rank restriction entirely when one error weight is at
least1/R with supplied R<p. The support-bounded argument below remains
valid, but is no longer the broadest stated source contract.

For rho = sum_b w_b |psi_(F+b.x)><...| with support at most R < p, a fixed
spectral threshold can select a nonempty subset B' without assuming a lower
bound on the original positive weights. Choose among M equally spaced
midpoints in [1/(2R),1/R], M >= 8R/beta. At most R choices lie within
Delta = 1/(8RM) of an eigenvalue, so bad-grid probability is <= beta/8.

Fix this one threshold for the ENTIRE run. Its retained mass is >= 1/R,
retained rank is in [1,R], and normalized minimum eigenvalue is >= 1/(2R).
The existing [copy spectral-filter/rank construction](REES_MIXED_SPECTRAL_SOURCE.md)
and nonflat streaming theorem prepare repeated wedges of this same support.
The preceding proof then uses J = F + mean(B').x. Neither a global orbit gap
nor an original minimum-weight promise is needed.

This paragraph is not a coded nonuniform budget. Rank training, unsuccessful
filter targets, all density-matrix-exponentiation program copies, growth
aborts, and full-run approximation must be charged. Changing the threshold
between leaves can change J and invalidates the common-frame argument.

A fourth reviewer (Locke) supplied explicit uniform clocks. Let
L(z)=min{k>=0:2^k>=z}, beta=epsilon/16, w=1/(2R), M=2^L(8R/beta), and
tau=(2M+2a+1)/(4RM) for one uniform a in {0,...,M-1}. Set Delta=1/(8RM).
The bad-threshold event has probability <= beta/8 and is not heralded.
Use h=min(Delta/2,w^2/128), ideal eigenvalue-estimation tail kappa=w/128,
and implemented output-TV error zeta=w/128. For
m=128 w^-2 L(2/beta) independent target/program banks, clip the estimate Y
to [0,1] and average Z=1_(Y>=tau)/Y (zero below tau). Eigenvalues are
sampled with their own weights, so the ideal mean of Z is the retained
RANK, including multiplicities, not its probability mass. Its bias is
<=2h/w^2+(kappa+zeta)/w<=1/32, and Hoeffding error >1/8 has probability
<=beta. Round the mean to an integer and abort outside [1,R]. Passing that
range check does not certify the grid or rank.

For a deterministic maximum T of wedge requests, choose

    b=L(RT/beta), N=2R^2 b, S=T(N+1),
    C=2R L(S/beta), A=S C.

Allow at most N growth attempts per wedge and C filter trials per required
input. Growth and filter timeouts each total <=beta; abort the entire run
on either. Give every complete threshold instrument error beta/(2A) and
all growth-gate synthesis together beta/2. The complete preparation error
is <=beta, including failures and rejected branches. Program copies cost

    O(m h^-2 zeta^-1 log^2(2/kappa))       [training]
    + O(A^2 Delta^-2 beta^-1 log^2(2A/beta)) [preparation],

in addition to m training targets and A filtering targets. Fresh programs
are charged for negative-time cleanup too. Allocate epsilon/2 to the
core learner, including its circuit precision: total error is at most
epsilon/2+5beta<epsilon. Every displayed quantity is polynomial in
R,T,n,log p,1/epsilon, with the imported primitives' gate overhead.

The key simplification is structural: discarded spectral mass need not be
small. Every retained label still has the SAME nonlinear F, so there is
no nonlinear truncation bias. These clocks were mathematically reviewed,
not executed as a quantum rank learner/filter.

## Identifiability and decisive counterexamples

For equal flat sources with rank r, conjugate out F and work in the Fourier
basis. Multiplication by omega^(F'-F) has convolution support C. Equality of
the two coordinate support subspaces implies B+C is contained in B'. Since
|B|=|B'|=r, each c in C gives B+c=B'. Two distinct c's imply a nonzero period
of B; its cycles have length p, forcing p to divide r. When p does not divide
r, C is a singleton and F'-F is affine as a polynomial (degree < p prevents
polynomial/function aliases). Thus the stated gauge is exact.

- Divisible-rank obstruction: for odd p, B=F_p e_1 produces identical rho
  for F=0 and F=x_1^2. Universal nonlinear recovery is impossible there.
  This is not a claim that every p-divisible support is unlearnable.
- Nearly periodic weighted obstruction: put mass 1-epsilon uniformly on
  F_p e_1 and epsilon on one additional label. Rank p+1 is nonzero mod p,
  yet the two preceding phases give states at trace distance <= epsilon.
  There is no rank-only, arbitrary-weight robustness for general R >= p.
  More strongly, k copies have distance <=1-(1-epsilon)^k<=k epsilon;
  success >=2/3 on both nonlinear phases requires k>=1/(3epsilon).
- Omitting u generally leaves a mixed state; replacing A_u by rI loses
  lower-degree coefficients. Applying the coordinate measurement to r raw
  copies without antisymmetrization does not produce the claimed pure state.
- D >= p permits coefficient aliases; growing D or exponentially large r
  invalidates the stated polynomial-resource claim.

For quadratics there is an important exception to the need to retain u.
Write F=x^T A x/2+ell.x+c and set v=t+r^-1 sum_i u_i. The phase becomes
r v^T A v/2+(r ell+s).v plus a constant. Thus the centroid register is one
fixed pure quadratic-phase state and decouples from all relative registers.
Known pure-qudit learning is a stronger specialization than generic SDE
elimination. A [direct noisy-quadratic competitor](NOISY_QUADRATIC_PHASE_FILTER.md)
also avoids wedge preparation entirely: a paid four-copy instrument yields
vector regression samples and a separate verifier identifies correct ones.
Exact uniform noise permits entirely classical validation AFTER that quantum
instrument. This is not a classical simulation of the original input source.

## Executable scope and follow-up

Run:

    python qsearch.py phase-copy-baseline --phase-noise --write
    python -m pytest -q tests/test_exterior_phase_learning.py

The artifact binds source hashes and records conservative caps. Tests verify
the actual determinant-state coordinate permutation, conditional phases,
outcome probabilities, common-frame corrections, inverse maps, fixed-axis
filtration, and the counterexamples. The code does NOT create a top wedge
on a device or feed it into the existing opaque quantum-source controller.
That controller needs a measured-u front end and a separate raw-copy ledger;
its current `draw()` interface supplies neither. No candidate is promoted.

Next scientific question: does this exact noisy learning problem have a
useful native source or a prior published direct learner? Prioritize that
question over implementing a large finite simulation. General low-degree
noise, nonorthogonal error families, and exponentially large error support
are NOT covered and need new identifiability and resource analyses.

## Attribution

- [Bene Watts et al., 2610.06737v1, Theorem 5 and Remark 6](https://arxiv.org/html/2610.06737v1#S3):
  streaming antisymmetrization and known-rank stopping are prior art.
- [Ivanyos and Santha, 1503.09016v2, Section 5](https://arxiv.org/html/1503.09016v2#S5):
  varying-public-map phase elimination and diagonal-equation machinery are
  prior art; this source front end and local-retry composition are the local
  deductions under review.
- [Decker et al., 1107.2189v2, Section 5.3](https://arxiv.org/html/1107.2189v2#S5.SS3):
  multivariate HPGP uses different oracle access and does not automatically
  supply the copy-only front end.
- [Allcock et al., 2405.06357v1, Section 4.2](https://arxiv.org/html/2405.06357v1#S4.SS2):
  pure-qudit stabilizer learning is an established quadratic competitor.

Independent automated reviews: Boole (identity/identifiability), Archimedes
(varying frames, fixed-axis bounds, primary-source comparison), and Beauvoir
(quadratic alternatives). Agreement and finite controls are not peer review.
