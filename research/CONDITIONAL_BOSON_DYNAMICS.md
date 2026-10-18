# Independent Dynamics Track: Cheap Evolution Is Not A Hard Readout

Local baseline derivation / review pending. Known polaron mechanism, no novelty,
accepted speedup, general interacting-model dequantization or paper refutation.

## Why This Direction Was Selected

The DCP/finite-field receivers have no surviving constructive shortcut here.
Independent comparisons found that scalar semidirect/state-isomorphism routes
already have transfer audits and still lack the hard-group receiver. Repeating
those audits would not supply it. Natural many-body dynamics offers a different
mechanism: efficient structural diagonalization instead of hidden-group decoding.

[Apel and Sahinoglu](https://arxiv.org/html/2601.17732v1) identify the polaron
transform for fast-forwarding a fermion-boson sector, improving quantum simulation
dependence on bosonic cutoff. Their full algorithm RETAINS a noncommuting
remainder. This pass tests whether the easily evolved sector ALONE gives a
classically hard accessible observable. It does not refute their algorithm.

The general probabilistic-simulation perspective is prior art; see
[Van den Nest](https://arxiv.org/abs/0911.1624). We derive and implement the
specific infinite-oscillator overlap rather than assume a finite-state theorem
supplies an unbounded bosonic sampler for free.

## Explicit Problem And Input Model

Public exact rational data specifies n logical two-level controls, M independent
oscillators, positive frequencies w_mu, affine real forces F_mu(z), and a
quadratic diagonal control energy E(z):

    H0 = sum_z |z><z| tensor [E(z)+sum_mu
                         (w_mu*a_mu^dagger*a_mu+F_mu(z)*(a_mu+a_mu^dagger))].

Initial state is |+>^n tensor bosonic vacuum. Estimate a PRESELECTED control
Pauli-string expectation at t=pi*time_pi to additive epsilon. All coefficients
and time_pi are exact rationals, not hidden evaluator or floating-angle oracles.
Non-diagonal hopping is not silently included in this source contract.

For fermionic interpretation, each logical bit may be a dual-rail pair with
one fermion, initially the equal rail superposition. Occupation-controlled
forces and logical Pauli measurements then preserve fermion number/parity.
This avoids assuming forbidden single-mode fermionic |0>+|1> superpositions.
It is not an arbitrary many-electron initial state or ground-state source.

Candidate upside: structural fast-forwarding might have exposed a natural
classically difficult coherence observable even at large bosonic occupation.
Required proof: a source-valid measured task, paid precision/state preparation,
and a gap over strong classical methods, not just a smaller quantum gate bound.
The following classical estimator falsifies that candidate in this model.

## Exact Phase-Aware Evolution

For each z, write r_mu(z)=F_mu(z)/w_mu, theta_mu=w_mu*t. The actual branch is

    U_z(t)|vac> = exp(i*phi_z) |alpha_z>,
    alpha_mu(z)=r_mu(z)*(exp(-i*theta_mu)-1),
    phi_z=-t*E(z)+sum_mu r_mu(z)^2*(theta_mu-sin(theta_mu)).

The geometric phase is CONTROLLED, not a disposable common phase. At one
control, w1,F(z)=z/2,t2*pi, both bosonic branches return to vacuum but the
control becomes |+i>. Y expectation is1 and X expectation0; ignoring phi
instead predicts |+>. Actual Fock-space evolution verifies this contrast.

For a Pauli P=i^(a.b) X^a Z^b, put z'=z XOR a. Its expectation is the real
uniform average over z of

    i^(a.b)*(-1)^(b.z) * exp[-D(z,z')+i*(phi_z-phi_z')],
    D=sum_mu (r_mu(z)-r_mu(z'))^2*(1-cos(theta_mu)).

Since forces are real and each oscillator frequency is configuration-independent,
the coherent overlap has no additional imaginary phase. Every summand has
absolute value <=1. Sampling z and evaluating this expression is polynomial
in the public input size; no 2^n configuration table or Fock vector is needed.
It covers any ONE specified Pauli, not the joint distribution of exponentially
many measurement outcomes or a reusable quantum output state.

There is a STRONGER local baseline. Condition on the k bits flipped by X/Y.
F(z)-F(z') then depends only on those bits, so D is fixed. Since E is quadratic
and F affine, phi_z-phi_z' is AFFINE in every remaining unflipped bit. If its
phase increment is q_j, summing that bit contributes
`(1+(-1)^(Pauli_has_Z_at_j)*exp(i*q_j))/2`. Thus all unflipped bits sum
analytically, leaving only2^k assignments. The implementation constructs these
increments directly, without unstable division of exponentially small overlaps.
The64-control local readout needs TWO assignments and no sampling; general
high-weight strings retain the additive Monte Carlo alternative. Tests cover
all64 three-control Paulis and forbid enumeration of unflipped large systems.

## Precision And Statistical Costs Are Paid

`certified_pair` uses Arb enclosures. Rational differences are formed EXACTLY
before rounding. Rational multiples of pi use certified trigonometry; rational
phase turns are reduced modulo2 before exponentiation. Precision increases
until the requested enclosure width is obtained, or returns operational UNKNOWN.

With F(0)=2^80,F(1)=2^80+1, binary64 erases the entire force difference. The
true coherence is not1. A64-bit precision cap refuses to certify;128 bits
suffice in the recorded control, checked with independent180-digit branch
arithmetic. A clock-rescaled reference also multiplies exact duration and
Hamiltonian coefficients BEFORE converting to binary64, avoiding fake
overflow/underflow at frequency2^1200 and inverse duration.

For failure target2^-b, use N=ceil(8*(b+1)/epsilon^2) configuration samples.
Hoeffding on real summands in[-1,1] bounds statistical error epsilon/2;
per-sample certified arithmetic error <=epsilon/8 is included separately.
N*n logical binary draws and maximum arithmetic precision are recorded.
These are logical coins, not a claim to count OS entropy bytes exactly.
Confidence requires the declared IID uniform-bit model. A fixed-seed run is
a reproducibility control, NOT a certified IID source or a proof its realized
interval must contain the answer. Simultaneous/adaptive collections of
observables need their own failure allocation.

Runtime has no Fock-cutoff materialization. Precision still depends on
coefficient/time BIT LENGTH and epsilon; large physical phases are not free.
Relative accuracy for exponentially tiny observables may require exponential
work. Unknown caps, poor precision or a failed estimator do not prove hardness.

## Actual Hamiltonian And Cutoff Checks

The independent numerical reference constructs sparse Fock Hamiltonians and
uses SciPy expm_multiply, without importing the coherent-state formula. A dense
matrix-exponential replay checks the noncommuting one-control model as well.
Every two-control Pauli and multimode/sign controls are included. Sparse/dense
floating exponentials are NOT formal numerical certificates.

An actual cutoff certificate is needed: finite annihilation matrices obey
[a_Lambda,a_Lambda^dagger]=I-Lambda*|Lambda-1><Lambda-1|, not the infinite CCR.
Returning to vacuum at the FINAL time does not control intermediate boundary
leakage. A dimension2 oscillator at a strong-force revival gives the wrong
control readout despite zero ideal endpoint tail.

For each mode, uniformly bound |F(z)| by Fmax and put nu=4*(Fmax/w)^2.
Coherent occupation is Poisson with mean <=nu at EVERY time. Both its cutoff
tail and the boundary occupation at level Lambda are bounded by

    q=min(1,nu^Lambda/Lambda!).

Projecting the exact Schrodinger equation gives a boundary forcing of norm
<=Fmax*sqrt(Lambda*q). Duhamel bounds the finite evolution vs projected exact
state by |t| times this quantity. Adding the missing endpoint tail gives

    state distance <= (1+|t|*Fmax*sqrt(Lambda))*sqrt(q).

Sum mode bounds by a product-state telescope; take the uniform force envelope
across orthogonal control branches and cap distance at2. A norm-one Pauli
expectation differs by at most twice that distance, capped at2. This is a
VACUUM-INPUT cutoff bound for H0, not a global oscillator operator-norm bound,
and does not certify floating sparse-exponential errors or added hopping.

## Noncommuting Escape Is Real, Not Automatically Solved

Adding V=sum_j J_j X_j changes the actual readout. At w1,F=z/2,t=pi/2,J=2/3,
X expectation changes from about0.770885 to0.723902. The H0 formula no longer
applies. This countercontrol prevents promoting the classical baseline to the
full Hubbard-Holstein, Dicke, or arbitrary interacting many-body model.

For genuinely weak hopping, Duhamel still gives the PAID task bound
`|<P>_(H0+V)-<P>_H0|<=min(2,2*|t|*sum_j |J_j|)`.
The code computes a certified upper bound and subtracts it from the requested
error budget before licensing H0 as a sufficient baseline. When this bound
is too large it proves neither classical hardness nor quantum advantage.

Another considered route is low-energy polaron-band projection. It must pay
virtual-transition errors accumulating like |t|*||V||^2/gap, preparation and
coherent decoding. A huge gap can make the projection accurate, but merely
encoding an already-known spin Hamiltonian at an exponentially slow clock
does not discover a new computational algorithm. Schrieffer-Wolff quantum
algorithms are [prior art](https://arxiv.org/abs/2201.13304). No separate band-
projection subsystem is justified until a new physical/computational mechanism
and parameter regime survives that comparison. This is deprioritization, not
a claim that all low-energy fast-forwarding is impossible.

## Result And Next Gate

Reject large cutoff, entanglement, or cheap controlled displacement ALONE as
evidence for a breakthrough in this measured task. Do not repeat density-only
scaling scans. Full joint sampling, hard initial-state preparation, relative
accuracy, ground-state problems and noncommuting dynamics remain outside the
baseline; each needs an actual source/cost argument, not a relabeling.

The next dynamics idea must identify a genuine noncommuting mechanism and
target observable, beat this baseline where legal, and face tensor-network,
semiclassical, Gaussian and perturbative competitors in its exact regime.
Do not reflexively return to DCP or manufacture a broad physics no-go instead.

    PYTHONPATH=theorems python -m pytest -q tests/test_conditional_boson_dynamics_physics.py
    python theorems/conditional_boson_dynamics.py --write
