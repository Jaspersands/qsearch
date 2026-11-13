# Post-balanced-Kerr selection: homogeneous folded-chain full Born law

13 November 2026. Independent direction comparison, **not admission of a new
full sampler**. Read current STATE/TRAPS/GOAL. No network, API, Git, archives,
tests, implementation, or shared-status edits. The previous balanced Kerr
component proofs are not reopened; general passive angles remain a distinct
interior-caustic problem.

## Recommendation

Choose one bounded native classical challenge to the already written folded
XXZ fast-forwarding endpoint: **sample its full physical computational-basis
output from every homogeneous product input, at binary rational time.**
The concrete new operation is number projection of an explicit Gaussian with
polynomial acceptance, after sampling the native conserved fragment. This
extends neither the old arbitrary-input quantum theorem nor its classical
basis/Slater readout theorem by assumption. The projected Gaussian construction
below is the reason to reopen this particular physical input/output question.

The other independently compared mechanisms are expanded algebraic module
output and growing-component Gaussian-mixture learning. They have external
motivation, but no equally concrete new operation is currently supplied.
No novelty, hardness, practical runtime, or quantum separation is asserted.

Corpus `been-tried`, THEN `baselines`, were run for each exact candidate:
- `folded chain homogeneous product Dicke number projected Gaussian Pfaffian sampling`;
- `expanded central simple algebra splitting isomorphism compact minimal module height`;
- `growing mixtures fermionic Gaussian states randomized moment contractions learning`.
The catalog suggests tensor-network simulation for the two physical tasks,
and index-calculus/quaternion-norm methods for the algebra task. Most negative
hits are lexical; their broad barrier labels are not adopted as theorems.

## 1. Selected physical question and the new operation

**Native input/output.** Use EXACTLY H_N and the all-sector reversible basis map
in `FOLDED_CHAIN_COHERENT_TRANSFORM.md` LF50–99: N+2 physical spins, open
boundaries, binary rational time t. The initial state is

    (sqrt(1-p)|0> + exp(i phi)sqrt(p)|1>)^(tensor N+2),

with rational p in [0,1]; phi does not affect this output law. Output one FULL
physical spin string within epsilon TV of its evolved Born law. Charge N,
all input/time bits, accuracy, confidence, and all N+2 output bits. No unknown
input state, state-preparation oracle, sector advice, or final smoothing.

**Quantum mechanism and conditional advantage hypothesis.** The existing
coherent fragment encoder, free-fermion sine transform and binary-time phases
already implement evolution in poly(N,bitlength(t),log(1/epsilon)) gates.
Direct time stepping is not the strongest classical comparator. A possible
advantage for this full coherent product quench must survive the operation
below; it would not follow from exponentially many fragments or large t.

**Exact native sector reduction.** The label (s0,w,d,m) and effective chain
length ell are computed from one physical bitstring by the established greedy
bond parse. Every label block contains all weight-m strings of length ell.
Adjacent allowed moves exchange physical 01 and10, hence preserve physical
magnetization. The free exclusion graph within a label is connected, so that
magnetization is constant throughout the entire label block. Thus every
physical homogeneous-product amplitude has the SAME complex value within
that block. Conditional on its label, the input is exactly

    |D_{ell,m}>=C(ell,m)^(-1/2) sum_{|x|=m}|x>.

Sample an IID Bernoulli(p) physical string only to obtain its label, discard
its effective occupation positions, and prepare/simulate this conditional
uniform state. This samples the correct label weight including its dimension.
Dephasing labels is legal here because both evolution and the final physical
basis measurement are block diagonal. It is not legal for arbitrary output
observables or arbitrary unknown quantum input.

**Projected Gaussian mechanism.** Let J be the skew matrix with J_ij=1 for
i<j. Every even principal Pfaffian equals1: expansion in the first row gives
the alternating sum of an odd number of ones, and induction finishes.
Consequently the normalized pure Gaussian

    |G_z> proportional to exp(z sum_{i<j} c_i†c_j†)|vac>

has amplitude z^(|S|/2) on every even occupied subset S. Use ell physical
modes plus ONE spectator mode. For 0<m<ell choose z=m/(ell-m)>0.
Its squared occupation law before evolution is independent Bernoulli(q)
conditioned on even total parity, with q=z/(1+z)=m/ell.
Condition the spectator occupation to m mod2 and the physical count to m.
The resulting physical pure state is exactly |D_{ell,m}>; no unknown sign
or relative phase remains in its Fock coefficients.

The conditioning probability is at least

    min(q,1-q) Pr[Bin(ell,q)=m] >=1/[ell(ell+1)].

Indeed m is a binomial mode at q=m/ell, so its probability is at least
1/(ell+1), while conditioning the initial Gaussian on even total parity
divides by a number at most1. The cases m=0,ell are fixed Slater states.
The free evolution on the physical modes, with identity on the spectator,
commutes with both conditioning projectors. Therefore evolve ONE known
Gaussian, classically sample its occupations, reject unless the two tests
hold, then decode the physical string. This retains all within-fragment
coherence; it is not a mixture of the original effective basis inputs.

**Actual primary evidence checked.** Ruiz et al., retained
`bethe_transform_selection/folded.txt` LF1426–1508, explicitly discusses
hard-rod deformations of Dicke states, fragment superpositions and correlation
applications. That passage does not itself supply this full homogeneous-product
sampler. Bravyi, quant-ph/0404180v2, newly retained as
`2026-11-13-folded-gaussian/bravyi_flo.txt`, was read at LF371–420,
666–695 and845–906: Gaussian closure, trace/covariance formulas and
single-mode number measurements. It pays the Gaussian algebra/statistics,
not a uniform finite-bit clock through exponentially rare conditional branches.

**Precise next constructive obligation.** Prove that clock without following
an unstable sequence of rounded covariance divisions. Use the existing exact
unitary approximation U=S diag(d_j)S^T in one polynomial-degree cyclotomic
field, with rational-unit-circle d_j approximating the binary-time phases.
The initial pairing matrix zJ is rational; compute the evolved covariance
algebraically. Evaluate each prefix JOINT occupation probability directly by
Wick/Pfaffian formulas. Determinant-height bounds and algebraic zero tests
should pay conditional ratio coins, including zero and tiny prefixes.
Then allocate proposal accuracy before polynomial-probability conditioning,
cap O(ell^2 log(1/epsilon)) attempts, and charge all label/phase/coin errors.
This is a specified construction to prove, not an imported arithmetic-operation
claim. The source equations with squared traces must retain the correct positive
probability/sign; do not choose an arbitrary square root or assume invertibility.

**Cheapest falsifiers.** A label that changes physical magnetization, a basis-map
phase, a nonuniform conditional product amplitude, or a principal-Pfaffian sign
would kill the proposed reduction immediately. The elementary identities above
exclude these at the stated scope; the decisive remaining target is finite-BIT
prefix probability computation and its all-branch error budget. An exact small
symbolic control is useful only to detect convention errors, never as the
asymptotic proof. Ordinary Gaussian simulation already matches the supplied
Gaussian proposal; it does not remove the need to prove the native reduction.

## 2. Independent comparator: expanded CSA minimal modules

**Problem.** Growing-degree explicit number field and central simple algebra;
output an EXPANDED primitive idempotent/minimal left ideal and action matrices.
This would serve computational representation theory and algebra-system users,
who cannot substitute an unevaluated arithmetic DAG for every coordinate.
**Mechanism/target.** Reuse the admitted GRH quantum class/unit/norm backend,
then find a simultaneous bounded-height module basis by lattice reduction and
descent; target polynomial native-BIT output, including maximal orders, maps,
root extraction and basis conditioning. The existing compact result alone is
not this contract. Classical factoring-paid index/maximal-order algorithms,
split-map constructions and the SAME S-unit reduction remain comparators.
**Source gate actually read.** Retained `global_isotropy/amitsur.txt`
Theorems3.10,4.12,4.13 (LF727–744,1135–1173) gives the Amitsur/coboundary
algorithm and asserts the GRH quantum split-algebra result. It does not in
those passages provide the new simultaneous expanded-height normalization.
**Missing operation/falsifier.** Scalar norm-witness exponent reduction does
not automatically preserve all coboundary and module equations: extracting
a root of the discrepancy in the target tensor algebra still leaves a
compatible cochain lift to find. An actual compact-to-expanded basis proof
must address that compatibility and intermediate coordinate sums.
No such proof is proposed here. An exact source-backed expanded coordinate
bound, or a concrete height-normalization construction, would change this
ranking. Another compact arithmetic closure alone would not. Not selected.

## 3. Independent comparator: growing Gaussian-mixture learning

**Problem.** Fresh IID copies of rho=sum_{i=1}^k p_i rho_G(Gamma_i), known
physical Majoranas, growing k; output a polynomial-size physical preparation
within trace distance epsilon, in poly(n,k,1/epsilon,log(1/eta)) copies/gates/BIT.
No components, weights, separation, covariance frame or inverse are supplied.
This models latent switching among quadratic-fermion preparations; a general
interacting state is not promised to have such a representation.
**Possible operation.** Random contractions of Wick moment-generating functions
could replace the n^O(k) full moment tensor by polynomially many measurable
matrix pencils, followed by stable latent-component recovery and physical
merge rules. This is a proposed operation, not a uniform inverse theorem.
**Baseline and source boundary.** Known-component Wick/Pfaffian computation,
ordinary latent product-mixture learning in a known basis, and the admitted
two-component learner apply on their actual domains. Mele–Herasymenko's actual
retained `two_fock_learning/compressible.txt` LF242–305 concerns a pure state
with a small non-Gaussian core; it does not identify arbitrary growing mixtures.
The required new source statement would be a uniformly conditioned recovery
theorem for these RANDOM contractions, or a concrete collective measurement
that avoids that requirement—not generic tensor identifiability.
**Cheapest falsifier.** Uniform mixtures of even and odd occupation strings on
s modes each have k=2^(s-1) Gaussian components. They have identical moments
below Majorana degree2s but orthogonal supports. Thus retaining only degree2/4/6
cannot extend the old learner uniformly. This does not refute higher-order or
collective algorithms. Even a positive learner would primarily improve quantum
tomography, not yet separate it from classical processing of matched data.
No paid recovery operation or stronger external-value case is presently given.

## Why this next pass, rather than general-angle Kerr

General-angle Kerr moves caustics to interior counts of order K; the endpoint
polynomial-degree compiler does not cover them, and a coherent revival can
retain sqrt(K) count fluctuations there. A new uniform Airy/kernel compiler
would be needed. The folded proposal instead has an exact finite-dimensional
identity and inverse-polynomial success bound for a natural full spin-chain
quench. It can decisively settle an end-to-end use of the complete binary-time
quantum transform. Its next task is the explicit prefix-probability BIT proof,
not another source search, asymptotic fit, or implementation campaign. Preserve
the arbitrary-quantum-input exclusion, perturbation exclusion, and all unmatched
inhomogeneous-product/coherent-readout cases; no general dequantization follows.
