# Mixed Gaussian pair: exact algebra and low-rank review

2026-11-07. Independent review of `MIXED_GAUSSIAN_PAIR_LEARNING.md`.
Scope: exact moment/Gram identities, the shared Gaussian channel, common
attenuation and the low-rank fallback. The complete high-rank perturbation
ledger is assigned to a separate reviewer. No implementation or new finite
experiment was run for this review; no quantum learner was executed.

**Verdict:** the reviewed exact and low-rank mechanisms are valid. After
truncation, use a strict physical margin of at least `tau/2`, rather than
reusing the original `tau` without adjusting its constant. This does not
change the proposed precision exponents. A full uniform learner still needs
the separately assigned numerical/resource and preparation-interface checks.

## Native scope and moment identifiability

“Even” means that odd Majorana moments vanish, equivalently that the density
operator commutes with parity. It does not mean support only in the even
parity sector. General mixed Gaussian states satisfy the former condition;
the latter would force every covariance singular value to have modulus one.
The known Majoranas and ordinary qubit circuits in the contract are needed.

With `omega=sum_{i<j} Gamma_ij e_i wedge e_j`, the stated Hermitian monomials
`(-i)^k c_i1 ... c_i(2k)` have Gaussian moments `Pf(Gamma_I)`. Thus the
generating form is `exp(omega)`, and, with `q=1-p`,

    M = exp(omega) [p exp(q Delta)+q exp(-p Delta)],
    H = 2 M4-omega^2 = pq Delta^2 = E^2,
    J = 6 M6-6 omega M4+2 omega^3 = pq(q-p) Delta^3.

The factors two and six matter: the raw connected quartic coefficient is
`H_I/2`, not `H_I`. When `H=0`, either a mixture weight vanishes or
`rank(Delta)<=2`; the entire state is then the Gaussian of mean covariance.
When `rank(E)<=4`, the entire generating form is
`exp(omega)(1+H/2)`. This statement includes arbitrary correlations of the
mean covariance between the active subspace and its complement.

For rank at least six, the six-dimensional Pfaffian-cofactor reconstruction
in the note determines `E` up to one global sign. In a Darboux restriction,
`B=diag(bc J,ac J,ab J)`, so `B=-Pf(A) A^-1`, including its sign. The map
`alpha -> A wedge alpha` is injective, with each squared component norm the
sum of the other two squared skew singular values. The subsequent formula
recovers every entry of `E`. Then `J` recovers `(q-p)/sqrt(pq)`; the one sign
choice only swaps the two branches. Consequently there is no exact pair of
different states in this native family with identical degree-two, four and
six moments. This exact fact alone is not a stability theorem.

## Contraction Gram

For `E=sum_j a_j u_j wedge v_j`, direct contraction gives

    lambda_j(G_H)=4 a_j^2 (S-a_j^2), each twice,
    ||H||^2=4 sum_{j<k} a_j^2 a_k^2,  S=sum_j a_j^2.

The ordering follows from
`lambda_i-lambda_j=4(a_i^2-a_j^2)(S-a_i^2-a_j^2)`. Thus the fifth Gram
eigenvalue really controls the third skew pair; no hidden choice of frame
is used by this test. The random six-column restriction also has the stated
exact second moment: independent signs kill distinct index-set terms and
give `6! sum Pf(E_I)^2`. The degree-six hypercontractive and Paley-Zygmund
steps yield the displayed constant success probability. This checks the
exact random restriction mechanism, not its full finite-precision ledger.

## Shared channel and constant-dimensional core

For common blocks `Gamma_j=[A_j,C;-C^T,B]`, write
`D=(I+B^2)^-1`, `R=I-C D C^T`, `A0=-C B D C^T`. Since
`(I+iB)^-1=(I-iB)D`, the Schur complement of `I+i Gamma_j` is exactly
`R+i(A_j-A0)`. Its conjugate supplies the other sign. If
`I +/- i Gamma_j >= tau I`, the variational characterization of the Schur
complement gives the same lower bound on it, hence `R>=tau I`.
Also `I+B^2>=tau I`; the required inverses have polynomial conditioning.

The matrices `G_j=R^-1/2(A_j-A0)R^-1/2` are physical core covariances.
For `L=[sqrt(R);0]` and `Z=[A0,C;-C^T,B]`, the matrix
`I-LL^T+iZ` has zero Schur complement and is positive semidefinite.
The opposite convention is its conjugate. This verifies the Gaussian
channel's CP condition and its exact covariance action on both branches.
The resulting trace-preserving map sends their mixture to the target state.

Only a two-mode even core is needed. Its identity, six quadratic moments
and one quartic moment determine its density matrix. The core quartic is
`(omega_core^2+H_core)/2`, with
`H_core=(R^-1/2)^(wedge4) H|V`. No mixture weights or physical decomposition
of that density matrix have to be solved for. Parity-block PSD clipping
and normalization are constant-dimensional operations.

## Regularization and low-rank truncation

The actual mixed-Gaussian continuity bound in 2409.17953, Theorem 1 Eq. (9),
is `||rho_G(Gamma)-rho_G(Gamma')||_1 <= ||Gamma-Gamma'||_1/2`, where the
right norm is the matrix Schatten norm. It has no spectral-gap assumption.
Applying it separately to the two Gaussian branches proves common
attenuation costs at most `n tau`. It must not be applied directly to an
arbitrary nonGaussian density matrix. The attenuation's degree-`2k` moment
rescaling is `(1-tau)^k`, so the proposed classical rescaling is paid.

The SMALL H argument is valid. A small mixture weight costs
`O(n sqrt(h))`; otherwise `sqrt(pq)>=Omega(h^1/4)` and `a2=O(sqrt(h))`.
Keeping one skew pair changes each covariance by `O(h^1/4)<<tau` and yields
an exactly Gaussian mixture of the same mean. Weighted branch continuity
bounds the state error without recovering the unknown weights.

For the LOW THIRD branch, the stated bounds follow from the Gram identities:
`pq=Omega(h/n)`, `a1^2=Omega(h/n)`, and
`a3^2=O(n ell/h)`. Thus removing the skew tail changes Delta in operator
norm by `O(n sqrt(ell)/h)<<tau`. Weighted Gaussian continuity gives
`O(n^(3/2) sqrt(ell/h))` density error. Moreover
`lambda_2>=4a1^2 a2^2>=2||H||^2/n^2`, giving the claimed top-four support
gap when the third pair is small. These are output-side thresholds, not
input gap or minimum-weight promises.

For the estimated projector P, define the nearby reference by `Delta'=P
Delta P` and keep the mean covariance fixed. Its physical margin is at
least `tau/2` once the combined truncation/alignment error is below
`tau/2`; use that margin in the channel formulas. Crucially,
`P^(wedge4) H=pq(P Delta P)^2` exactly. The projected data describe this
nearby reference directly. Approximation error in replacing the target is
therefore not subsequently amplified by the core inverse; only estimated
moments and numerical arithmetic incur that conditioning loss.

## Preparation interface and remaining gate

The source formulas in 1604.01954 and quant-ph/0404180 supply the fermionic
Gaussian channel/CJ interface. Converting it to ordinary registers requires
the cross-parity unitary `W=(-1)^(N_output N_reference)`, implementable by
all output-reference CZ gates, plus the fixed reference correction V from
the identity CJ state. W is generally not a reference-only correction.
There are at most two reference modes, so W costs O(n) and V is constant
dimensional. With the conventions matched, the corrected normalized
ordinary Choi state and the core give the intended channel output upon the
identity Bell result, with probability `1/d_core^2>=1/16`.

Retries consume fresh known PREPARED core/Choi states. A capped retry count
and a fallback on total failure are essential to produce a finite
trace-preserving preparation circuit. They require neither an inverse of
the unknown source nor unknown-state postselection. Boundary Choi
eigenvalues are not a promised gap: preparation precision can instead be
charged using Gaussian covariance continuity. Errors in this constant-input
postselection incur only a constant amplification.

The remaining composition gate is quantitative: the independent full
ledger must pay the numerical high-rank inverse, branching tolerances,
physical clipping, Gaussian/CJ preparation and gates, and combine their
failure probabilities with the moment estimates. This review does not
certify exponent 10000 merely because it is large. It also does not infer
novelty, classical separation, off-model robustness, a many-component
extension, parity-preserving-only gates, or a completed learner from exact
identities or finite controls. Pure-state fidelity validation from the
earlier coherent-pair work does not apply to this mixed-input endpoint.

## Addendum: direct four-Gaussian endpoint supersedes CJ implementation

The following simpler endpoint is valid and removes the need to physically
implement the channel, its CJ state, parity corrections or Bell retries.
It retains the abstract CP channel proved above as a mathematical map.

Every even two-mode density matrix sigma splits into its two 2-by-2 parity
blocks. Diagonalizing each block gives

    sigma = sum_{a=1}^{at most 4} w_a |phi_a><phi_a|.

Each phi_a is a pure fermionic Gaussian state. In the even sector it is
`u|00>+v|11>`, a two-mode BCS state (including the endpoints). In the odd
sector it is `u|01>+v|10>`, a one-particle Slater determinant. Both have
vanishing odd moments and pure Gaussian covariances G_a. Odd parity of the
vector does not violate the even-density convention. Preparing an occupied
reference state before its known Gaussian rotation is allowed by the
ordinary-qubit-circuit contract; an even-parity-only gate/source restriction
must not be introduced.

Linearity and the Gaussian action of the proved channel imply exactly

    channel(sigma) = sum_a w_a rho_G(L G_a L^T+Z).

Therefore compute the at most four output covariances classically, sample
the known finite distribution of weights, and prepare the selected known
Gaussian directly. No channel oracle, unknown inverse, postselection or
growing-dimensional mixed-state decomposition is needed. The SMALL H and
HIGH THIRD branches use at most one and two Gaussian components respectively,
so every branch can output a description of at most four known Gaussians.
This is an approximate output representation, not recovery of the unknown
input components or weights.

Degeneracies of a core parity block require no eigenvector gap. A fixed-size
spectral calculation can certify the residual of a density-matrix
reconstruction; rotating eigenvectors inside a nearly degenerate subspace
does not need individual-vector accuracy. If sigma_tilde is the reconstructed
physical even density matrix, abstract channel contraction bounds its output
error by `||sigma_tilde-sigma||_1`. Ordinary finite-precision covariance
arithmetic, physical clipping, Gaussian preparation and weight sampling
still require their polynomial error budgets. The Gaussian continuity bound
applies separately to the at most four output components, and weight error
is bounded by the classical l1 distance. There is no postselection error
factor in this replacement endpoint.

Accordingly the earlier CJ source/implementation checks are no longer gates
for this chosen algorithm. The full high-rank numerical/resource ledger and
the ordinary known-Gaussian preparation costs remain separate composition
obligations. This addendum is an exact structural proof, not a finite control
or an execution of the learner.
