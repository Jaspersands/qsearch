# A Classical Baseline For Finite-Time Diffusion Readout

30 October 2026. A constructive comparison proposed by the parent during
Rawls the 2nd's independent direction search. This is a scoped application
of standard Girsanov/Pinsker techniques, not a new stochastic algorithm,
a refutation of every quantum diffusion advantage, or a mixing theorem.

## Target And Decision

The [2026 Gaussian-LCHS paper](https://arxiv.org/html/2601.15523v2) supplies
a quantum matrix-element estimator for dissipative dynamics without the
usual evolved-state postselection loss. That is existing machinery, not
our contribution. Its large worst-case classical comparison is not a
lower bound on the same observable for a particular native family.

First consider the finite-time endpoint question on a flat torus:

```
dX_t = b(X_t) dt + sqrt(2/beta) dW_t,
b=-gradient(V),       X_0 distributed as mu_R,
target = Pr[X_T in P].
```

Assume a smooth periodic potential with global bounds `||b||<=B` and
L-Lipschitz drift, D coordinates, positive beta, and an independently
charged classical sampler for mu_R. The exact process is the one being
estimated; this does NOT replace it by its equilibrium distribution.
Periodic boundary conditions alone do not imply a smooth periodic drift.
For example, V(x)=x^4-x^2 on [-2,2] has V'(2)=28 and V'(-2)=-28;
wrapping this force does not satisfy our global Lipschitz assumption.
Transfer from an unbounded physical system, or replacement by a smooth
periodic model, needs its own finite-time error budget. Small equilibrium
mass near a seam is not by itself such a budget.

When B,L,D,T,beta,1/epsilon and the required arithmetic/sampling costs
are polynomially bounded, the following classical trajectory estimator
has polynomial cost. An exponential-dimensional PDE representation or
an `exp(L*T)` Gronwall estimate cannot establish an exponential gap in
this regime. Other regimes and polynomial quantum improvements remain
open to separate comparison.

### Match The Normalized Overlap, Not Just Endpoint Probability

The paper's principal target is the normalized propagator overlap nu_RP,
not p_RP=Pr[X_T in P | X_0 distributed as mu_R]. For restricted Gibbs
initial laws, write Z_R=integral_R exp(-beta*V) and analogously Z_P.
For the SAME reversible gradient diffusion,

```
p_RP = sqrt(Z_P/Z_R)*nu_RP,
Z_R*p_RP = Z_P*p_PR,
nu_RP = sqrt(p_RP*p_PR).
```

The second identity is detailed balance integrated over R times P; the
last follows by substitution and positivity. Thus additive accuracies
for p_RP and nu_RP are NOT automatically interchangeable. If classical
restricted-Gibbs samplers for BOTH regions are explicitly available, run
the endpoint algorithm twice, from R and from P. This is also the sampling
access stipulated in the paper's classical comparison (Section II.2).
It does not follow from arbitrary supplied quantum input states.

For clipped estimates a,b in [0,1] of p_RP,p_PR with each absolute error
at most alpha, the elementary product and square-root inequalities give

```
|sqrt(a*b)-nu_RP| <= sqrt(|a*b-p_RP*p_PR|) <= sqrt(2*alpha).
```

Set alpha=epsilon^2/4 and the two failure probabilities to delta/2, leaving
room for arithmetic rounding. The total cost is still polynomial in
1/epsilon and the earlier parameters, without estimating Z_P/Z_R.
This deliberately conservative bound is NOT an optimal epsilon exponent.
Both initial samplers, both regions' finite-bit contracts, and all
trajectory costs are charged. It does not estimate a time derivative,
first-passage distribution, or a rate divided by an uncharged small T.

## Path-Space Error Without A Gronwall Factor

Let K be a positive integer, h=T/K, and interpolate Euler continuously:

```
Y_(kh+u) = Y_(kh) + u*b(Y_(kh))
           + sqrt(2/beta)*(W_(kh+u)-W_(kh)),       0<=u<=h.
```

Lift the periodic drift to R^D and use the same initial law for X,Y.
Bounded drift ensures the Novikov condition. Girsanov gives, with
expectation under the EULER law,

```
KL(Law(Y_[0,T]) || Law(X_[0,T]))
 = (beta/4) integral_0^T E||b(Y_(h*floor(t/h)))-b(Y_t)||^2 dt.
```

Conditional Brownian increments have zero mean and are independent of
Y_(kh), so

```
E||Y_(kh+u)-Y_(kh)||^2 <= u^2*B^2 + (2D/beta)*u.
```

Apply Lipschitz continuity and integrate each interval, obtaining

```
KL <= L^2*D*T*h/4 + beta*L^2*B^2*T*h^2/12
    = A/K + C/K^2,
A = L^2*D*T^2/4,       C = beta*L^2*B^2*T^3/12.
```

Pinsker and endpoint data processing give TV at most `sqrt(KL/2)`.
This controls an arbitrary measurable endpoint indicator in the ideal
arithmetic model, not just Lipschitz observables. No convexity, mixing
rate, spectral gap or stationary initialization is used. The same-law
initialization and bounded global drift are essential to THIS proof.

For endpoint bias at most epsilon/4 it suffices to take

```
K >= max(1, 16*A/epsilon^2, 4*sqrt(C)/epsilon).
```

Each term in the KL bound is then at most epsilon^2/16. Independent
bounded-indicator trajectories estimate the Euler expectation within
epsilon/4 using O(epsilon^-2*log(1/delta)) samples. All K steps of each
trajectory and every initialization are charged. This is polynomial
in NUMERICAL time T, not in log(T).

The method is standard; for primary context on entropy analysis of Euler
with additive noise see [Yuan Yu 2024](https://doi.org/10.3390/e26030232).
The explicit constants and input-matched comparison here follow directly
from the displayed bounded-drift calculation, not a claim that a different
paper establishes this whole application.

## Finite Precision Is A Separate Gate

A finite-support numerical distribution has TV one from a continuous
law. Therefore do NOT claim a finite-bit sampler approximates the latter
in TV directly. Compare the distributions after the SAME quantization.

Use a periodic nearest-grid map Q_eta whose grid fits the torus, with
coordinate spacing eta, so
the distance to a cell representative is at most eta*sqrt(D)/2. Let the
implemented drift have uniform Euclidean error at most zeta at grid
points. The implementable rounded chain takes

```
Z_next = Q_eta(Z + h*b_tilde(Z) + sqrt(2h/beta)*xi),
xi standard D-dimensional Gaussian.
```

Conditional on any rounded exact-Euler history, its current real point x
lies in the representative z's cell. Choose consistent torus lifts. The
two pre-rounding Gaussian means differ by at most

```
a = (1+h*L)*eta*sqrt(D)/2 + h*zeta.
```

Equal-covariance Gaussian KL is `beta*||mean_difference||^2/(4h)`.
Pinsker, wrapping and quantization therefore bound one-step TV by
`a*sqrt(beta/(8h))`. This bound holds for every possible x in the cell,
so also for its conditional mixture; the rounded exact-Euler history
need not itself be Markov. Sequential coupling then bounds total error by

```
tau_initial + K*(a*sqrt(beta/(8h)) + tau_transition).
```

Here tau_transition pays numerical generation of the rounded Gaussian
kernel and tau_initial pays the rounded initial distribution. Choose
these terms to sum to at most epsilon/4. Polynomial BIT LENGTHS suffice
when numerical parameters have polynomial encodings and the stated
numerical upper bounds hold, with arithmetic and oracle costs charged.
Inverse-polynomial tolerances additionally need suitable lower bounds:
T=h=2^-n can require eta=O(epsilon*2^(-n/2)), still only O(n+log(1/epsilon))
precision bits. Coordinate Gaussian CDFs with charged coordinatewise
error, tails and precision generate rounded transitions without grid
enumeration; gradient evaluation, modulo operations and coordinate bit
length remain part of the computational contract.

The grid must refine the FIXED input region, not redefine the target. If
P is an efficiently decidable union of its cells, membership agrees
with that of the exact endpoint except on null boundaries. Otherwise
pay a bound on mass near the classification boundary or specify a
smoothed observable. A black-box arbitrary measurable region is not
an automatic finite-bit input model. The same caveat applies to sampling
the restricted initial law, not only to final readout.

## Many-Particle Scaling And Falsifiers

For eta_particles particles in s spatial dimensions, D=s*eta_particles.
Suppose each smooth periodic difference interaction w_ij(x_i-x_j) has
relative-coordinate force norm <=G and Hessian operator norm <=J. Then
one can use

```
B <= sqrt(eta_particles)*(eta_particles-1)*G,
L <= eta_particles*J.
```

The Hessian bound follows from the complete-graph identity
`sum_(i<j)||v_i-v_j||^2 <= eta_particles*sum_i||v_i||^2`, and also
holds for nonconvex pair Hessians by taking absolute quadratic forms.
For radial interactions J includes tangential curvature v'(r)/r, not
just v''(r). One-body walls add their own force and Hessian bounds.
Thus pairwise coupling does not force an exponential discretization
cost merely because the Lipschitz constant grows with particle count.
Potential evaluation costs, typically quadratic in particle count, remain
explicit. There is no enumeration of a D-dimensional configuration grid.

This baseline does NOT cover singular forces, an unpaid smoothing scale,
reflecting/absorbing boundary dynamics without an additional proof,
exponential T or precision, or an inaccessible initial law. Coherent
preparation alone does not imply classical sample access to mu_R. An
exponentially rare probability at constant relative accuracy asks for
exponentially small additive epsilon; the displayed polynomial in
1/epsilon then costs exponentially. It also gives no fast equilibrium
sampler, first-passage algorithm, or nonlinear function of full trajectories.

Re-entry for a superpolynomial quantum claim requires a native target
outside this proved classical window, with its quantum state preparation,
normalization, observable precision and actual time cost all paid. Do not
build a Gaussian-LCHS demo or promote the dimension of a discretized PDE
as evidence of advantage. The new tests check algebra and budget scope,
not a quantum implementation or convergence by numerical experiment.

## Independent Review

Rawls the 2nd independently verified the KL direction, constants, rounded
history comparison, and many-particle bounds. The review caught the
endpoint/normalized-overlap distinction, periodic-seam assumption,
bit-length versus inverse-tolerance distinction, and a wrong author
attribution. All are corrected above. This is automated mathematical
review, not peer review or proof-assistant certification.
