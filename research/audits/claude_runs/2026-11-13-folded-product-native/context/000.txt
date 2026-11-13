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
