# Copies-Only Flat Subspace Symmetry Through Exterior States

29 October 2026. Conditional source reduction and exact resource plan.
Not a quantum execution, established novelty, or a classical-input speedup.

Follow-up: [spectral flags](REES_MIXED_SPECTRAL_SOURCE.md) give a separate
written reduction for general polynomial-rank mixed inputs. The flat
source module and promises in THIS note are unchanged.

## 1. Question And Input Contract

Can the existing projective Rees source learn the conjugation symmetries
of an unknown mixed state, rather than merely the subgroup acting as a
scalar on its support? For **exact flat states of known polynomial rank**,
the following composition answers the source-conversion question positively.
It does not settle the general mixed-state problem.

The input consists of:

- Fresh IID copies of rho=Pi_V/r, where V is an unknown r-dimensional
  subspace of C^d. The integer r is supplied and correct; q=ceil(log2 d)
  measures the size of one physical input register.
- An explicit exponent-p Lazard group G of class c<p, with the public
  arithmetic and fixed-class resource contract of the existing Rees work.
- An efficiently controlled **linear** unitary representation R(g) on
  the input registers. Its gate cost and approximation error are charged.
- A supplied gap delta>0 such that, for EVERY g outside
  H={g:R(g)Pi_V R(g)^dagger=Pi_V},

      TD(rho,R(g)rho R(g)^dagger) >= delta,
      TD(a,b) := ||a-b||_1/2.

Rank, flatness, independence and the global gap are promises, not outputs
of the budget calculator. No preparation inverse, conjugate copies,
classical basis of V, projector oracle for V, or oracle revealing H is given.
The task is to return generators of H, subject to the remaining correctness
and implementation obligations of the [Rees receiver](REES_HSP_REDUCTION.md).

## 2. Literature And What Is Actually Added

Bene Watts et al., [*Anti-symmetrization is cheap and useful*,
arXiv:2610.06737v1](https://arxiv.org/html/2610.06737v1), Algorithms 1--2,
Theorem 5 and Remark 6, provide the streaming preparation primitive used
here. It needs copies and public controlled swaps, not knowledge of the
support. This is **prior art**, not a new primitive of this repository.
The independent related [arXiv:2610.02103](https://arxiv.org/abs/2610.02103)
also develops antisymmetric growth for Schur sampling.

The addition here is the explicit flat-state conjugation-to-ray-symmetry
bridge, its separation-gap conversion, and its composition with the
whole-run [projective Rees source](REES_PROJECTIVE_STATE_SOURCE.md).
[Holt--Subramanian, Section 10.4](https://arxiv.org/html/2609.38085v2#S10.SS4)
motivates subspace and mixed-conjugation symmetry learning. The checked
section does not itself supply the present exterior-state/Rees composition.
This targeted comparison is not an exhaustive novelty certification.

The naive projection of r raw copies onto their top exterior power succeeds
with probability r^-r for flat rho. That exponential rank cost is NOT the
implemented plan. The streaming construction removes that particular cost.

## 3. Exact Target And Separation Gap

For any orthonormal frame (u_1,...,u_r) of V, define the normalized state

    Omega_V = u_1 wedge ... wedge u_r in (C^d)^(tensor r).

Changing the frame changes only its global phase. A nonzero decomposable
top wedge determines its subspace: V={v:v wedge Omega_V=0}. Consequently

    R(g)^(tensor r) Omega_V is a phase times Omega_V
      iff R(g)V=V iff g in H.

On H the phase is det(R(g)|_V), which need not be one. This is ray
stabilization, NOT vector stabilization; feeding these states directly to
a source requiring trivial phases would be wrong. The existing public
zero-moment Rees design removes this determinant character. There is no
new restriction r<p: the exterior representation is over C, not F_p.
Generic projective representations R are not included in this argument.

For U=R(g), let theta_1,...,theta_r be the principal angles of V and UV.
The difference of their projectors has singular values sin(theta_i),
each repeated twice, with zeros filling the remaining dimensions. Thus

    TD(Pi_V/r,U Pi_V U^dagger/r) = (1/r) sum_i sin(theta_i),
    gamma = 1-Tr(Pi_V U Pi_V U^dagger)/r
          = (1/r) sum_i sin(theta_i)^2 >= delta^2.

The determinant overlap and AM--GM then give

    |<Omega_V|U^(tensor r)|Omega_V>|
      = product_i cos(theta_i)
      <= (1-gamma)^(r/2)
      <= sqrt(1-delta^2) <= 1-delta^2/2.

The conservative rational overlap gap delta^2/2 is therefore valid for
EVERY nonsymmetry. This avoids an unnecessary rank loss. Each controlled
exterior action costs r controlled calls to the original R(g); neither
its large Hilbert-space dimension nor its tensor action is treated as free.

## 4. Streaming Preparation And A Hard Clock

Use the cited growth instrument on a retained antisymmetric k-register
block and ONE fresh copy. Let P_k^V project onto wedge^k V. On its support,

    Tr_(k+1) P_(k+1)^V = ((r-k)/(k+1)) P_k^V.

For any normalized retained density in wedge^k V, the flat fresh input
therefore gives success probability

    p_k = (r-k)/(r(k+1)) >= (r-k)/r^2,  1<=k<r.

Success increases k. Rejection preserves antisymmetry but can change the
retained state; the fresh register is discarded. The controller must use
the **updated** retained token on both branches. The invariant also ensures
that reaching k=r yields the same pure Omega_V on every successful history.
The completed state decouples from its herald record. Distinct outputs
use disjoint fresh IID input streams.

For T required output states, whole-stream abort budget beta and r>=2, set

    B = ceil(log2(rT/beta)),   N = r^2 B.

Initialize one copy per output and permit at most N further growth attempts
for that output, without resetting the clock at an intermediate success.
Comparison with collecting r coupons, each of probability 1/r^2 per round,
gives a failure bound r exp(-N/r^2) <= r 2^-B per output. Union bounding:

    Pr(any timeout) <= rT 2^-B <= beta,
    raw copies <= T(N+1),    growth instruments <= TN.

The first timeout aborts the WHOLE run. A caller cannot use previously
delivered partial outputs as a successful full answer. For r=1, the plan
uses exactly T raw copies and no growth measurement or ideal timeout.

The source holds at most r live input registers, plus growth ancilla and
control workspace. This is a **preparer-only** memory count; stored receiver
leaves and group registers must be added. At most 2(r-1) controlled
register swaps per attempt covers both growth and rejection recovery.
Each register swap costs O(q) elementary controlled bit swaps, plus
ancilla preparation, equality controls and precision synthesis. The report's
register-swap count is not a complete compiled gate count.

### The Rejection Instrument Is Part Of The Claim

In the cited LCU realization, retain a coherent two-outcome ancilla
measurement: zero versus its entire orthogonal complement. Apply the
prescribed recovery on rejection before discarding ancilla or fresh input.
On the antisymmetric-prefix domain this gives the complement Lueders
instrument (I-P_(k+1)) rather than a mixture of resolved ancilla branches.
Omitting recovery or measuring every ancilla basis value first can destroy
the required invariant. Finite controls test these distinctions; they do
not constitute a physical scalable backend.

## 5. Whole-Rees Composition And Error Allocation

Let epsilon be the requested whole-run error. Call the existing
`projective_source_budget` with gap delta^2/2 and error epsilon/2. Let T be
its `total_fresh_copies`, INCLUDING all moment-design factors, label
amplification, failed leaves and receiver source preparations. T is not
the number of successful final samples.

Set beta=epsilon/8 and use the cap above for ALL T exterior states. Reserve
epsilon/8 for raw acquisition and growth implementation errors, spread
over C=T(N+1)+TN complete calls. Each call must have error at most
epsilon/(8C), including its flags and rejection branches. The precision
notion is complete-instrument distance stable under composition (diamond
distance for operations), not distance after conditioning on a rare branch.

The older source budget already includes its own copy/action accuracy
reserve; it is not added twice. Its controlled actions now mean a complete
r-fold exterior action. Allocating its per-use action allowance over r
base-R calls is conservative. Then

    total_error <= ideal_source_bound + rT/2^B + epsilon/8 <= epsilon,
    base controlled-R calls <= rT.

This is polynomial in r,q,1/delta and the charged group input for fixed
class, subject to the existing receiver bounds. It is NOT polynomial in
q if r is exponential in q. For example, a code subspace encoding Theta(q)
logical qubits has exponential r. No hidden fixed-rank assumption licenses
an efficient algorithm for that regime.

## 6. Decisive Falsifiers And Classical Boundaries

- Nonflat source: diag(3/4,1/4,0) and the swap of its first two basis states
  have identical support but different density matrices. The top wedge
  reports a support symmetry that is NOT a conjugation symmetry. This
  construction deliberately does not solve arbitrary mixed-state symmetry.
- Wrong rank: stopping below the true rank generally leaves a mixed
  exterior state. Requesting a rank above the true one makes completion
  impossible; the hard clock must abort. Rank estimation is not supplied.
- Non-IID input: a correlated bank mixing |u_j>^(tensor L) has correct
  flat one-copy marginals but never grows past one. Marginals are inadequate.
- Lost herald/coherent recovery: averaging incompatible ancilla outcomes
  does not implement the required growth channel. Test the entire branch.
- Missing gap: continuous subspaces can have arbitrarily close distinct
  orbit points. Efficient action alone does not give inverse-polynomial
  delta. No concrete hard family with the required promise is established.
- Access mismatch: unknown quantum copies are the input. A quantum-input
  reduction is not automatically a speedup for a classical description.
  If an explicit basis/projector or small invariant coefficient module is
  supplied, classical stabilizer methods may apply; run those before
  declaring an application hard. Failure of tomography on exponentially
  large ambient dimension is not a classical lower bound.

There is also a cheap **quantum-assisted membership baseline**, which must
not be confused with finding generators. For a fixed supplied g, a SWAP
test on independent rho and R(g)rho R(g)^dagger has mean
Tr(rho R(g)rho R(g)^dagger). It is exactly 1/r on H and at most
(1-delta^2)/r off H, by the gamma identity above. Thresholding at
1/r-delta^2/(2r) uses at most
ceil(8 r^2 delta^-4 ln(2/eta)) repetitions for error eta by Hoeffding,
with two fresh copies and one original action per repetition. Charge
operation precision separately. Exhausting this test over G costs |G|
membership tests; that is a baseline, NOT a lower bound against better
classical inference. A claimed application must beat stronger inference
from these same paid measurements, not just compare against tomography.

The primitive does not accelerate the receiver's diagonal solving or remove
the group-class dependence. The source and receiver quantum circuits remain
unimplemented. A separate [instrument obstruction](REES_PREMATURE_GRADE_MEASUREMENT.md)
rules out one premature-measurement shortcut, not all coherent alternatives.

## 7. Reproduction And Next Decisive Work

`theorems/rees_subspace_source.py` contains the exact plan, opaque herald
controller and resource composition. `tests/test_rees_subspace_source.py`
checks finite projectors, determinant/gap identities, lineage, caps,
updated rejection states and the counterexamples above.

Run `python qsearch.py subspace-source --write` for a deterministic resource
report. The rank/gap profiles are HYPOTHETICAL promises, not measured source
instances or receiver executions. No candidate or proof status is promoted.

Next useful work is to exhibit an explicit efficiently controlled family
with polynomial rank, a proved global gap, nontrivial H, and a matched
classical access analysis. Do not replace that task with more synthetic
budget profiles. Separately, a scalable complete receiver and coherent
growth backend would remove implementation debt, not establish novelty.
