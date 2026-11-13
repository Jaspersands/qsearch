# Independent physical selection after ballistic sampling

2026-11-14. Current STATE/TRAPS/GOAL read. No tests, network/API/Git,
archives or shared-status changes. Decision: no NEW quantum mechanism is admitted. Actual primary comparison
selects one bounded classical full-Born challenge in the weakly perturbed
product phase; see section3. This is independent of BCS/Gaudin/scattering
and the matched matroid spectrum.

Corpus `been-tried` was run BEFORE `baselines` on both:
“infinite temperature dynamical structure factor Choi Liouvillian spectral
sampling” and “dissipative preparation coherent Gibbs Rokhsar Kivelson quantum
heat bath”. The former had mostly lexical/quarantined hits; a targeted check
found the exact prior Choi proposal in post-wave-opportunity-selection §3.
The latter returned the existing Gibbs-parent/heat-bath comparison. Neither
baseline query found a catalog keyword match; that is not absence evidence.

## 1. Normalized non-diagonal dynamical response: reject as a new operation

Native input: rational bounded nearest-neighbor XXZ couplings and fields on
an N-site chain, H=sum[J_i(XX+YY)+Delta_i ZZ]+sum h_i Z_i, plus frequency
resolution delta and TV accuracy epsilon. Output a sample from the smoothed,
normalized infinite-temperature local-spin response

 mu_A = 2^-N sum_(a,b) |<E_a|A|E_b>|^2 delta_(E_a-E_b), A=Z_1.

Use a specified positive smoothing kernel, avoiding promises about spectral
mass exactly at hard bin boundaries. This is a physical spin-response law,
not a normalized density of all many-body energy levels.

Bell pairs plus A prepare the normalized vectorization |A>> with no rare
source or thermal advice. The Liouvillian H tensor I-I tensor H^T has the
displayed spectral measure. Simulating the explicit local terms and phase
estimation cost poly(N,input bits,1/delta,1/epsilon); no ground state, inverse
of an unknown source or hidden eigenbasis is required. But this is the SAME
standard simulation/QPE construction already screened in the prior note,
not a newly derived operation or a new asymptotic algorithm.

At Delta_i=0, exact one-particle diagonalization supplies a classical sampler:
draw a,b independently with weights |v_a(1)|^2 and |v_b(1)|^2, and return
their energy difference with the prescribed smoothing. At nonzero interaction,
Krylov/KPM, tensor-network dynamics, short-time expansions and hydrodynamic
approximations are serious competitors; no universal classical match follows.
The retained compendium §6.4, LF2298--2347, motivates this response and discusses
those methods, but it is not evidence of a separation for this native family.

Cheapest decision is already decisive: compare the circuit to the prior
Choi construction. They are identical. A new native fast-forwarding or
classically unmatched output-specific operation would be needed to reopen;
generic BQP encoding, changed observable names or bigger evolution times do
not supply it. No extra response-source request is justified this pass.

## 2. Actual dissipative theorem: a restricted preparation clock is paid

Primary read: `audits/sources/dissipative_selection/rapid.txt`,
arXiv:2503.15827v3, Zhan–Ding–Huhn–Gray–Preskill–Chan–Lin, “Rapid quantum
ground state preparation via dissipative dynamics”. The retained source
record identifies published DOI **10.1103/wzb3-dbg9**; the compendium's
plausible-looking 10.1103/PhysRevX.16.011004 must not be reused.

Eq.(4), LF123–167, defines filtered couplings

 K_i=∫ f(t)e^(itH) X_i e^(-itH) dt,

not an eigenbasis oracle. A fixed negative-frequency filter annihilates the
ground state. Quadrature, Hamiltonian simulation and Lindblad simulation
are charged in Eqs.(9)–(11), LF249–291; its cited compiler sources are not
independently re-proved here. The source states end-to-end cost
~O(τ_mix Δ^-1 poly(N) polylog(1/η)) for the higher-order implementation.

Theorem8 and proof, LF2103–2223, concern H_λ=−Σ_i Z_i+λΣ_e h_e,
||h_e||≤1, fixed spatial dimension, range and per-site incidence, and λ
below a system-size-independent threshold. Couplings are all X_i, and the
Lindbladian has NO coherent Hamiltonian term. The fixed Gevrey filter has
fhat(−2)=1. This is an ALL-initial-state result, not an overlap promise:

 ||exp(tL)ρ−|ψ_0><ψ_0|||_1 ≤8N exp(−t/4).

Thus the coupling window is independent of N AND requested η; choose
t=4 log(8N/η). The quasi-free case is already classically tractable.
Theorem11's fermionic extension assumes positive-definite one-particle M,
not an arbitrary interacting Fermi surface. The MPO/TEBD method,
LF394–445, uses compression without a general polynomial bond/error theorem.
The numerical ANNNI comparison, LF831–889, does not rule out a better
adiabatic path. Neither theorem proves arbitrary-gap ground preparation.

One proof-rate repair is necessary. H17 bounds the local tail by
O(2^-r+exp(−c r^(1/α))), α>1, but LF2382 calls its summed tail Γ(r)
O(2^-r). For the QUALITATIVE fixed-locality theorem this is repairable:
Σ_m (m+1)^(2D+2) Γ(m) converges, so first choose a sufficiently large
fixed cutoff R in H26, then λ small enough for the near-field term.
The contraction remains <1/4. Do not import the displayed quantitative
R or λ_* scaling without this repair. No independent full compiler theorem
or polynomial dependence on growing dimension/range is admitted here.

The generic-gap inference still has an exact scoped falsifier. On an L×L
square torus, L≥3,N=L², let H=−Σ_<ij>Z_iZ_j−N^-1Σ_iZ_i.
A down-spin set S has excess energy 2|∂S|+2|S|/N. All-up is unique ground;
all-down has excess2; every nonempty proper S has excess≥8. The gap is2.
Every sum of terms supported on fewer than N sites has zero matrix element
between those two states. All-down has no other lower-energy state, hence
is stationary for every strictly downward filtered such coupling. This
refutes all-start mixing from the gap alone, NOT Theorem8, nor a fixed-source
algorithm: maximally mixed input puts only2^-N mass there. No general
nonlocal-jump, heating or coherent-drive obstruction follows.

## 3. Classical scope and single selected operation

All following PRIMARY texts were read in the same retained source directory.
`weak_ground.txt` is Bravyi–DiVincenzo–Loss, arXiv:0707.1894. For a
bounded-degree graph, H_0=Σ_u Δ_u|1><1|_u and arbitrary bounded two-site V,
Theorem1 gives unique gap≥Δ/2 for |λ|≤2λ_0, λ_0=2^-18 Δ/(dJ).
Theorems2–4, LF123–236, give polynomial-time energy and two-site-observable
approximation within constant weaker coupling windows. Linked-cluster
Kirkwood–Thomas coefficients through order p cost N exp(O(p)); LF1074–1076
charges precision overhead. These are LOCAL observables, not arbitrary
occupation-prefix probabilities. The source notes its unnormalized
wavefunction issue at LF229–232. The same uniform gap along
s↦H_0+sλV pays ordinary quantum adiabatic preparation; dissipative mixing
is not the first polynomial quantum algorithm in this restricted phase.

`weak_classical.txt`, Mann–Waite arXiv:2601.21140v2, Theorems1/5,
LF124–174, DOES give full diagonal Gibbs sampling and relative prefixes,
but requires |λ|≤exp(−2rβ)/(e^4 β Δ_graph 2^r).
“Arbitrary temperature” does NOT mean fixed weak coupling as β→∞.
Even the elementary sufficient ground-approximation
β=O((N+log(1/η))/gap) leaves this window at fixed λ. This is a scope
mismatch, not a lower bound on its method.
`low_temperature.txt`, Helmuth–Mann arXiv:2201.06533v2, Theorem15,
LF361–376, has a β-independent window but proves a partition-function
FPTAS for stable phases with pure spatial boundary conditions and specified
Peierls assumptions. It does not state a uniform FPTAS for arbitrary
imaginary-time-slice prefix insertions. Even when a product-phase subclass
meets its assumptions, that change of observable must be proved.
No full-Born match is imported automatically from a partition FPTAS.

The new CLASSICAL operation worth one bounded construction attempt is a
temperature-uniform measurement-conditioned cluster contraction, or an
equivalent sampler avoiding tiny-prefix division. Exact native contract:
N listed qubits on a fixed-dimensional bounded-degree lattice; rational
Hermitian two-site h_e of norm≤1 and B-bit coefficients;
H=−ΣZ_i+λΣh_e; λ in a fixed sufficiently small common window above;
requested η>0. Output x∈{0,1}^N within TV η of |<x|ψ_0>|² in
poly(N,B,1/η) BIT time. No ground energy, wavefunction, marginal oracle,
source inverse, tensor-bond bound or sign condition is supplied. Full
spin snapshots, rather than already-matched local expectations, are the
externally meaningful output; no hardness/separation is assumed.

Concretely the chain-rule primitive is
Z_x(β)=Tr(P_x exp(−βH)), P_x=|x><x|_S⊗I, with normalization Z.
Uniform relative prefix estimates suffice; an average-case sequential bound
with explicit rare-prefix handling may suffice instead. The existing
linked-cluster wavefunction is a concrete input to this contraction problem,
not its solution. Frozen zeroth-order amplitude damping or correlation
decay does not supply these measurement-conditioned probabilities.

Cheapest decisive falsifier of a tempting shortcut: take
H=−Z_1−Z_2+λX_1X_2, λ≠0, and P=|1><1|_1⊗I. The exact ground probability
is (1−2/sqrt(4+λ²))/2>0. In contrast,
Tr_(ran P)(exp(−β PHP))/Tr(exp(−βH))→0 as β→∞: PHP has eigenvalues0,2,
while the full ground energy is −sqrt(4+λ²). Prefix insertion cannot be
replaced by exponentiating the spatially compressed Hamiltonian. The same
model has zero ground probabilities for 01 and10; any claimed uniformly
positive ground-prefix denominator is false.

The older coherent-Gibbs/RK parent I−D_π^(1/2)KD_π^(-1/2) has exactly the
native reversible classical-chain gap. Local ratios plus inverse-polynomial
gap and polynomial log(1/π_min) already give the SAME classical Born sampler
(`GIBBS_ORBIT_PARENT.md` LF138–165). This does not cover general Lindbladians,
but prevents recycling that old mechanism as the missing operation.

Disposition: select the stated weak-phase FULL-BORN classical challenge,
not an unproved quantum advantage, generic gap conjecture or new transform.
It can change whether a source-backed quantum endpoint has an unmatched
native readout. First test any proposed contraction against the two-qubit
pinning identity, then require full TV and finite-bit control for all inputs
in its stated constant-coupling window. No novelty, hardness, classical
impossibility or classical coherent-state preparation follows.

## Addendum: global creation truncation and native negative activity

2026-11-14. Independently checked the new topic's representation lemma.
BDL Lemma5, LF591–600, gives ||C_q||_1≤2^-15/(2λ_0)^q. Hence at
|λ|≤λ_0, D=C−C_k obeys ||D||≤Σ_M|D(M)|≤N2^-15 2^-k.
All creation monomials commute (overlapping products are zero), so
u=e^-C|0>, v=e^-C_k|0>=e^D u and ||v−u||/||u||≤e^||D||−1.
For nonzero vectors, normalization costs at most twice this relative error;
computational-basis TV is at most normalized Euclidean distance. No vacuum
probability lower bound or factor e^||C|| is needed. The stated
k=ceil(log2(8N/η)) is more than sufficient for 0<η≤1.

The native finite-bit claim also has an exact proof. Let q_h multiply all
real/imaginary input-entry denominators and let q_λ be λ's denominator.
Set Q=48 q_h q_λ lcm(1,...,k+1). BDL recurrence(27),(28)/(57) divides
only by E0(M)=2|M| and j! with j≤4. Its order-q terms have total input
degree q; induction shows every coefficient λ^q C_q(M), q≤k, has
denominator dividing Q^q. Thus log denominator=O(k(NB+B+k log k)).
Lemma5 bounds numerator magnitudes as well; intermediate products/sums
have polynomial bit length. N exp(O(k)) coefficient operations are
therefore polynomial BIT work. Rounding T retained complex coefficients
to error≤η/(32T) adds ≤η/32 to the operator error; the SAME commuting
argument pays global normalized error. This remains a succinct state
representation, not normalization, contraction or sampling advice.

For the negative-activity construction take rational 0<a≤1/4. With
s=1+2a², ψ=(1,−a,−a,0), E=−2/s, w=(H0−E)ψ, one has
ψᵀw=0, ||w||²=8a²/s. Therefore V=−(wψᵀ+ψwᵀ)/s satisfies
Vψ=−w and ||V||=sqrt(8)a/s. Weyl gives λ_2(H0+V)≥−||V||>E,
so ψ is the unique ground. With λ=4a and h=V/λ, ||h||<1;
choose also a≤λ_0/4 and embed on one lattice edge with other edges zero.
The squared norm is 1+2a², whereas the two singleton activities contribute
(1+a²)^2, leaving connected activity −a^4. This exactly refutes only
that positive connected-activity interpretation, not all positive samplers.
