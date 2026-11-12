# Explicit logarithmic-precision Jack compiler candidate

Question: replace ONLY the two inverse-accuracy bottlenecks in the already reviewed fixed-alpha3 full clean Jack transform (principal half phase and first-order simulation) to obtain poly(D,log(1/epsilon)) BIT/gate cost on arbitrary input superpositions, including all workspace and reference. This is a constructive resource improvement of the SAME end-to-end algorithm, not a new state source or application. No implementation/novelty/speedup claim. Standard classical attacks already run: downset sampler poly(D)*M², row/column quench z-laws, new exact creation/prefix attacks supplied no unrestricted sampler; none proves hardness.

Existing B/C branching and positive phase agreement are already checked. For W=(2P0-I)(2Pc-I), valid spectral phases avoid the cut at -1 by g0=1/[2(D+1)], while global W remains unitary. Principal W^(1/2) sends each valid Lax corner vector to its Jack parent with POSITIVE phase. Need a unitary circuit clean on this promised subspace, uniformly (no unknown lambda/tau). Existing ordinary QPE half phase costs poly(1/epsilon); explicit recipe below might replace it.

Parent construction, now independently checked: N=D+1; H=(2I+W+W^dagger)/4. On promised phase support, eigenvalues x=cos²(phi/2) >= a=1/(64N²). Define b_k=binom(2k,k)/4^k, q_K(x)=sum_(k=0)^K b_k(1-x)^k,
 P_K(W)=(I+W)q_K(H)/2.
For x>0, P_K=e^(i phi/2)*t_K(x), t_K=sqrt(x)q_K(x) in[0,1], and 1-t_K<=exp(-a(K+1))/a for x>=a. Thus choose K=ceil(a^-1 log(1/(a delta))) for desired relative defect delta; K=poly(D,log1/delta). This uses neither eigenvalue nor overlap advice. At x=0 P_K=0; a unitary extension outside promise is allowed.

Explicit small LCU with no exponential term enumeration: R=I-H=(2I-W-W^dagger)/4 has a block encoding using an exactly uniform four-label selector for I,I,-W,-W^dagger. Products of k encodings with FRESH signal registers give top block R^k. Prepare k=0..K with weights b_k/s, s=sum b_k (positive rational, s<=K+1); coherently select k repeated R gadgets with unary clock. All-good block is q_K(H)/s. Append the (I+W)/2 block encoding. Result V has top block P_K(W)/s, O(K) W calls, polynomial qubits and polynomial-bit rational coefficient prep. Retain all signal ancillas coherently.

Known-normalization amplification: m=4(K+1), theta*=pi/(4m+2), d=s sin(theta*)<1. Add a known ancilla dilution with clean amplitude d; top block becomes sin(theta*)P_K(W). Use m standard oblivious Grover iterations with reflections ONLY about known all-zero signal ancillas (minus signs kept). On each W-eigenvector, output clean amplitude is
 f(phi) sin((2m+1)arcsin(sin(theta*) t_K(x))).
At t_K=1 this is exactly f(phi); when t in[1-delta,1], the angle error is O(delta) since (2m+1)theta*=pi/2. Hence total clean-isometry error O(delta), not merely projected-block error. This differs from forbidden known-TAU amplification: the normalization s and chosen theta* are known globally, no unknown lambda. Need verify this identity/phase and uniform reference error, including direct sums over c. Total W calls O(K²); finite arithmetic and controlled-W errors must be allocated to actual gate count, preserving logarithmic precision.

Second bottleneck: reuse the existing explicit native L simulation via Taylor LCU + half-block OAA (previous native-measurement report §§4.3,5), instead of first-order Trotter. L degree d has known parity matchings, weights sqrt(3k m_k), diagonal2l. Block encode L/Gamma with Gamma=O((d+1)²), using native endpoints/canonical metadata; no sparse oracle. With Rseg=O(Gamma), short-time Taylor Ksim=O(log(Rseg/rho)) and exact-normalization-1/2 padded LCU, half-block OAA gives whole clean-isometry error rho with poly(D,log1/rho) gates/BIT. Actual BCCKS1412.4687 uses discarding ancillas: here KEEP all signals, use the O(sqrt(delta)) clean-isometry bound and square internal tolerance. No measurement/abort/postselection in the coherent transform. Inverses are the actual circuits.

Content projector reflection uses coherent integer-grid QPE of exp(2pi i L/M0), M0 power2>8(D+1), then phase flip c, then uncompute. All controlled times<2pi; approximate simulation/reference-norm and inverse-on-range errors paid. All complete branching stages O(D), per-stage target O(epsilon/D). Finite gate set must implement coefficient rotations to polylog precision without unit-cost real gates or unverified QSP phase compiler. Existing half-block finite-gate compiler or a proved standard finite-gate synthesis route may be used, with all global controlled phases retained.

Falsifiers: wrong branch-cut phase; missing positive phase across lambda; hidden exponential word expansion; unknown overlap passed to amplification; projected error substituted for clean error; intermediate discard; nonclean matching label; recursive error choice forcing inverse-epsilon work; bit computation/rotation failure. A proof of these two paid replacements would upgrade full Jack transform and BO quench work sampler to poly(D,log1/epsilon); no classical separation follows.

## Parent composition addenda (now checked)

Use integer accuracy b>=1 with target2^-b, avoiding an uncharged redundant
rational encoding of epsilon. Select polar K first, then its polynomial W
call cap, then simulation tolerance/degrees, then lowest gate precision.
W simulation must be valid on the WHOLE degree sector and every content
label, while the half-phase approximation itself only needs the promised
cut-gapped subspace. Approximate leakage outside that subspace is controlled
by unitary hybrid bounds, not by extending the phase promise.

The same V workspace banks must be used by V and its actual inverse in
oblivious amplification. Fresh signals implement polynomial PRODUCTS within
V; they are not replacements for the banks on which Vdagger must act.
Ideal lower-level work remains zero even when upper LCU signals are arbitrary.

For BO work, S needs the same polylog-accuracy simulation upgrade. Use
unordered i<=j, i+j<=D. Canonical endpoint has larger m_(i+j). Weights:
 i<j: 2sqrt[i*j*(i+j)*(m_i+1)*(m_j+1)*m_(i+j)];
 i=j: sqrt[i²*(2i)*(m_i+1)*(m_i+2)*m_(2i)].
For each pair, split edges by parity of this larger merged-mode occupation;
each class is a matching. O(D²) terms, each norm<=8(D+1)² safely, so
uniform padded term selection gives Gamma_S=O(D^4). Exact native labels
and algebraic weights have polynomial BIT cost. The same Taylor/half-block
argument then applies for bounded QPE times. No generic sparse oracle.

A safe fixed finite gate palette may include H,S,X,Z,CNOT,Toffoli,CH,CS.
Compile higher Boolean controls into a single flag with exact Toffoli/AND
work; no arbitrary real rotation is added to the palette. Known global
minus signs become controlled phases and must be kept. An alternative
standard finite palette needs its phase-preserving controlled synthesis
explicitly charged.


## Reviewed written result and report dispositions

Parent fully read and independently checked the300line proof in
`audits/reviews/2026-11-13-jack-logprecision-independent.md`, including
all scalar inequalities, controlled phases, preserved valid sectors,
finite-bit rotation compiler, inverse-on-range identity and native S weights.
The poly(D,log(1/epsilon)) full clean transform and BO work sampler are now
admitted as WRITTEN constructions. Accuracy can be specified by integer b,
with error2^-b and cost poly(D,b); input representation is charged. Existing
algebraic prerequisites and classical baselines are unchanged. No circuit
implementation, novelty, useful/Shor-level speedup or hardness follows.

Explicit constants: polar clean error<4delta and W query cap32(K+1)^2;
retained-signal Taylor J=ceil(log2(2^14 Rseg²/rho²)); native S normalization
Gamma_S<=64(D+1)^4. Allocate zeta=epsilon/[128(D+1)], delta=zeta/16,
then K, query count Q, rho=zeta/[64(Q+1)(ell+1)], then simulation degrees,
then count T variable rotations and choose bottom precision
b>=2log2(128T/epsilon). Entire output scratch is within epsilon of zero,
uniformly over superpositions and reference. No number-of-partitions factor.
Read actual BCCKS1412.4687v1 Eqs13-16 and compact Taylor construction;
the source's ancilla-discard conclusion is replaced by the direct squared
clean-isometry norm identity. Finite palette and same-bank inverse rule in
the review are essential, not optional implementation details.

Claude jack-log-simulation completed17581bytes/340lines, fully parent-read.
Its additional dyadic signed-selector construction provides a useful native
alternative: round matching coefficients directly, avoiding rotations inside
Taylor blocks; fold controls into exact permutation/phase flags; use shifted-
Hamiltonian Hadamard tests for content REFLECTIONS without inverse QFT.
Parent verified its half-block expansion and clean error sqrt(6rho), the
pair-symmetric endpoint uncomputation, bounded-error Hermitian matrix,
Duhamel allocation, and same-pool unitary hybrid. F1-F3 are supplied native
facts already proved; its F4 corner-weight interface is supplied by our
existing exact hook/residue formulas, not a new missing oracle. Only specified
efficiently computable times (here rational multiples of pi) are used;
an arbitrary real time has no free representation. Do not adopt its exact
gate exponent or use the reflection-only construction as a full content
readout. Our reviewed finite-palette QPE still pays the latter. No finite
sweep is needed to support these algebraic deductions.

OpenAI jack-binomial-polar completed26530bytes/832splitlines, fully parent
read and checked. Its explicit two-projector rotation proves the stronger
clean bound2delta; coefficient arithmetic, same-bank signal products and
phase sign are valid. At W=-1 it explicitly fails cleanliness, as allowed
outside the promise. One interface is STRONGER than we supply: its Eq2
assumes a global native-workspace operator norm bound. Do NOT import that
as a paid prerequisite or claim we supplied it. Our independently proved
whole-logical-sector CLEAN bound, same-bank inverses and unitary ideal-prefix
hybrid suffice, even with dirty upper signals. Its optional Solovay--Kitaev
synthesis route and exact aggregate exponents are not relied on; the fully
checked threshold finite-gate compiler already pays that task. Both reports
terminal and sessions reaped, no retry. Freeze their usage at this milestone,
excluding all newer Macdonald work.
