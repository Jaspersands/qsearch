# Copy-Only Code-Support Symmetries Via Antisymmetrization

2026-10-24. CONDITIONAL APPLICATION REDUCTION; independent review pending.
No newly invented antisymmetrization primitive, quantum execution, classical
hardness claim or demonstrated speedup. The exact task differs from learning
all conjugation symmetries of an arbitrary mixed state.

## Research Decision And Prior Art

The preceding simple-spectrum source excludes ordinary mixed code states:
rho=P/r has a positive eigenvalue of multiplicity r. That source's failure
does not exclude a different source transformation. The missing capability
is to preserve a whole subspace without fixing an arbitrary basis inside it.

Use [Bene Watts et al., arXiv:2610.06737v1](https://arxiv.org/html/2610.06737v1),
Algorithms 1-2 and Theorems 3,5. Their streaming procedure grows an
antisymmetric subsystem from independent copies, retaining it after failed
growth attempts. It needs no eigenbasis or preparation inverse. Its pure
rank-r output encodes the support, not the eigenvalues. That primitive and
its efficient controlled-SWAP implementation are PRIOR ART, not our result.
The same paper explicitly proposes support learning/testing applications.

This pass supplies the particular code-symmetry/Rees transfer, exact
access/error bookkeeping and falsifiers. Whether that composition is novel
is not established. The repository's literature audit already indexed the
related [Brahmachari et al. paper](https://arxiv.org/abs/2610.02103), but the
searched files did not contain 2610.06737. Do not infer novelty from that.
An aggregator incorrectly associated the antisymmetrization abstract with
2609.11345, which the primary arXiv record identifies as an unrelated Hecke
algebra paper. That identification was rejected, not imported as evidence.

The parallel scaling audit confirmed that the fixed-degree diagonal solver
really permits growing equation rank: [Ivanyos--Santha, Theorem 3](https://arxiv.org/html/1503.09016v2)
has polynomial arity in that rank at fixed degree. It did not uncover the
suspected hidden exponential. This is revalidation, not a new result.

## Exact Task

Given:

- Fresh independent copies of rho=P/r, where P is an unknown orthogonal
  projector on D-dimensional physical states and the rank r is supplied.
- Efficient controlled LINEAR R(g), for a public exponent-p Lazard group
  G with fixed class c<p and explicit coordinates. Charge all gate and
  coordinate costs. General Clifford groups or arbitrary gate groups do
  not automatically meet this contract.
- A supplied global promise eta>0 such that

      ||P - R(g) P R(g)^*||_op >= eta  for every g outside H_P,
      H_P = {g : R(g) P R(g)^* = P}.

Return generators of H_P. This is the full code-preserving subgroup WITHIN
the supplied gate family, allowing nontrivial action inside the code. It
does not identify that logical action in an unknown encoder basis, discover
the ambient gate family, or return an encoder or decoder.

An encoder V on arbitrary logical inputs can supply P/r by sending it a
uniform mixed logical input; one source copy costs one forward call. But
only mixed copies are required here, not V, V^*, a classical density table,
an eigenbasis or a reflection about the unknown code. If an encoder or
tableau IS supplied, classical competitors receive the same description.

For polynomial efficiency require r, eta^-1 and the receiver resource cap
to be polynomial in the actual input size. Since r=2^k for k logical qubits,
this condition is not polynomial in arbitrary k. Logical dimension, not
only logical-qubit count, is charged. Known rank is a substantive promise.

## Pure Source And Gap Transfer

Choose an orthonormal frame V=(v_1,...,v_r) for the code ONLY for analysis.
Let omega_P be the normalized antisymmetric tensor v_1 wedge ... wedge v_r.
A different frame changes its phase, not its density operator. No such
frame is supplied to the algorithm.

Under the known representation T(g)=R(g)^tensor(r), direct determinant
expansion gives

    <omega_P|T(g)|omega_P> = det(V^* R(g) V).

Let cos(theta_i) be the singular values of the compression V^*R(g)V.
They are the cosines of the principal angles between the code and its
image. Consequently

    |overlap| = product_i cos(theta_i),
    ||P - R(g)P R(g)^*||_op = max_i sin(theta_i).

Thus modulus one holds EXACTLY on H_P, including arbitrary rotations of
the code's internal basis. Off H_P the supplied gap implies

    |overlap| <= sqrt(1-eta^2) <= 1-eta^2/2.

The ray phase on H_P is its determinant character. Apply the existing
public zero-moment Rees design to cancel that character and obtain the
same hidden lift used by the checked Rees source chain. Each design factor
uses a distinct extracted omega_P, and each T(g) costs r controlled R(g)
calls. The construction does not discard the internal logical action by
requiring it to be scalar: only its determinant phase is cancelled.

The difference from the old logical-relation/Choi task is important. That
task compares a physical action with a specified logical label. This task
only asks whether the code subspace is preserved, without a logical label.
It is not a replacement for the stronger physical-to-logical relation.

## Capped Source Construction

Use the cited corrected growth instrument. If the current k targets are
antisymmetric within the code and a fresh P/r is appended, the success
probability is exactly

    p_k = (r-k)/(r(k+1)),                 1 <= k < r.

For example, expand the next antisymmetrizer on this input as
(I-sum_i SWAP_(i,k+1))/(k+1). The fresh P/r gives expectation 1/r for each
swap, even if the retained k-target state is mixed. A failure, with the
required correction, retains antisymmetry and support on the first k
targets; the last is discarded. The same p_k therefore holds after every
failure history, not just after typical ones. At k=r the target support is
the one-dimensional exterior power of the code, so its normalized density
is omega_P on EVERY successful record. No hidden basis choice remains.

This uniform final density is a stronger statement than an averaged
mixture identity: histories can be discarded without changing the source.
Use disjoint fresh input streams for different extracted sources.

Let B cap receiver leaves, ell>=log2 of the Rees-cover order, and M be the
public zero-moment design size. For a total error allowance epsilon set

    gamma = eta^2/2
    a = ceil((ell + ceil(log2(8B/epsilon)))/gamma)
    W = B*a*M                         independent extracted wedge sources
    t = ceil(log2(8W*max(1,r-1)/epsilon))
    L_k = ceil(t/p_k)                attempts allowed at size k
    S = W*sum_k L_k                  growth measurements
    N = W*(1+sum_k L_k)              raw native copies

For each stage the capped-failure mass is (1-p_k)^L_k<=exp(-t).
A union bound across W(r-1) stages is at most epsilon/8. All execution
histories obey these clocks. A timeout is ABORT, not an extra retry or a
renormalized source. In contrast to the matched spectral-mixture method,
successful records all yield the SAME pure density, so there is no remaining
spectral-weight selection bias. Abort mass still cannot be ignored.

Using sum_k 1/p_k = r*((r+1)*H_(r-1)-(r-1)), the raw cost is
O(W*r^2*log(r)*log(Wr/epsilon)), with r=1 handled directly. The planner
uses exact rational arithmetic; it never enumerates Hilbert space.

Allocate epsilon/8 each to amplification, extraction abort, growth
implementation, and original action implementation; reserve epsilon/2 for
addresses and the existing receiver. Every growth instrument has complete
half-diamond error at most epsilon/(8S), and every original controlled
action at most epsilon/(8rW). Telescope through the whole adaptive circuit;
do not divide errors by success probabilities. Rank-one sources perform
no growth measurements, so that per-measurement allocation is null.
Here the global channel comparison is with the exact physical LCU circuit,
not with an asserted projector formula on arbitrary invalid inputs. Its
projector/failure identities are used on valid ideal antisymmetric histories;
global implementation error then transports those histories through the
actual circuit. This avoids assuming imperfect retained states stay exactly
inside the valid sector.

The register-SWAP bound is 2W*sum_k kL_k. These are controlled swaps of
whole D-dimensional registers, NOT individual elementary gates. Each costs
polynomial in log D and log r; uniform ancilla preparation, negated-swap
controls and failure correction must all be compiled and charged. No
full Schur transform, factorial permutation circuit or D-by-D table is
part of the proposed implementation. The finite verifier does enumerate
tiny matrices, explicitly only as a falsification control.

The above contract assumes exact independent native sources. If each has
trace-distance error nu, add N*nu to the total error by telescoping; do not
claim the displayed epsilon still covers it for free.

## Adversarial Checks

1. OMITTING THE FAILURE CORRECTION: the state can leave the retained
   antisymmetric sector. The literal LCU control shows leakage 4/9 in a
   rank-three case. Merely remembering that growth failed is insufficient.
   Measuring the FULL ancilla index rather than just its zero/nonzero flag
   also breaks the corrected instrument: coherence inside the nonzero
   subspace is required. Keep that ancilla unmeasured during correction.
2. ONE-SHOT ANTISYMMETRY: projecting r independent P/r copies directly
   succeeds with probability r^(-r). Retaining the corrected subsystem
   across failures is what avoids this exponential restart cost.
3. WRONG RANK: stopping at k<r leaves a higher-dimensional exterior space,
   not a pure support state. The r=3, k=2 control has purity 1/3. Reaching
   the requested size does not certify that it was the true rank.
4. ARBITRARY MIXED CONJUGATION: omega_P forgets eigenvalues. A nontrivial
   rotation inside a rank-two support has wedge overlap modulus one while
   changing diag(0.6,0.4,0) by trace distance about 0.1732. This is not a
   general mixed-state solver or a contradiction of the preceding source
   note's degeneracy counterexample. The physical conversion is different.
5. GAP FROM CODE DISTANCE: not proved. One must establish the stated global
   operator gap from a motivated code/gate family. Generic perturbations
   can make exact symmetry tests arbitrarily ill-conditioned.
6. HIDDEN RANK COST: take two rank-r projectors sharing r-1 directions and
   with orthogonal remaining directions. Their flat states commute, and
   their n-copy trace distance is exactly 1-(1-1/r)^n <= n/r. A constant-gap
   C3 action can preserve the first support but not the second. Distinguishing
   their symmetry subgroups with success 2/3 therefore requires n>=r/3.
   Exponential logical dimension cannot be hidden by calling r a qubit count.

The last lower-bound control uses P_0=span(e_0,...,e_(r-1)), and P_1 sharing
the first r-1 basis vectors but replacing the last with
(e_r+e_(r+1))/sqrt(2). The public C3 generator is identity except for omega
on e_r. It fixes P_0 and moves P_1 at operator distance sqrt(3)/2. This
is a source-complexity falsifier, not a planted research candidate or a
classical hardness result.

Correct one-copy marginals do not supply independent inputs: the bank
sum_j |j,j><j,j|/r has marginals I/r but zero two-copy antisymmetric mass,
whereas independent copies have mass (r-1)/(2r). Repeated use of a frozen
unknown basis state cannot replace fresh code-state preparations.

An additional sparse left-regular control has a code-preserving subgroup
of order three and normal core of order one inside the F_3 Heisenberg group.
Every actual Rees address gives the full hidden-support indicator exactly.
That code has an easy classical basis-sampling learner; it only falsifies a
normal-core-only reinterpretation, and supplies no advantage evidence.

## Classical Baselines And Decision

Explicit projector/basis input admits ordinary linear algebra; if D is
polynomial, tomography is also a serious baseline. Stabilizer descriptions
permit tableau methods; unknown stabilizer-code copies require comparison
with existing stabilizer-learning algorithms. Low-width tensor-network
encoders permit contraction/operator-pushing baselines. A supplied encoder
circuit must not be hidden from the classical competitor. Large Hilbert
dimension alone establishes none of these methods' failure.

There is also a parameter mismatch to confront before choosing an application.
The distinctive Rees regime has growing prime p and class greater than two;
constant-prime/fixed-class HSP already has prior algorithms. A code encoding
even one p-level logical system has r>=p. If p is exponential in the input
bit length, this source reduction is not polynomial. One must either keep
the actual code rank polynomial while allowing the physical action's large
prime, or choose a growing-prime regime where r is still polynomial and
compare the full parameter dependence of prior algorithms. Relabeling
fixed-prime stabilizer codes is not evidence for the added Rees leverage.

The proposed conditional gain is compact subgroup recovery without full
tomography or enumeration of all gates. No matched general classical lower
bound is supplied. No particular nonadditive growing family with a proved
global gap and unresolved classical complexity is established by this pass.
The source conversion is useful research leverage, not Shor-level evidence.

Keep this as a conditional code-support application of the Rees theorem,
with the antisymmetrization primitive attributed. Do not open a campaign
of planted code examples. Next decisive work: identify one independently
motivated code/gate family meeting ALL promises, or compare this application
with existing state-symmetry learners and remove it if already covered.
