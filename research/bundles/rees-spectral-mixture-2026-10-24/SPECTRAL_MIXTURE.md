# A Spectrally Promised Mixed-State Source For Rees

2026-10-24. LOCAL CONDITIONAL REDUCTION, independent review pending. This
pass does not prove novelty, implement a spectral learner or HSP receiver,
or demonstrate a classical-input speedup. It addresses the established
mixed-state conjugation-symmetry task under additional explicit promises.
It is not a planted oracle problem or a replacement for the general task.

## Decision And Input

The repository already has pure/ray and scalar-support source conversions,
including a zero-moment Rees design and a principal-state purification
route. Those do not learn the full conjugation symmetry of a mixed state.
This pass identifies a different constructive route with a paid spectral
interface. Do not relabel the old scalar-support solver as a mixed solver.

Supply fresh IID copies of rho on q qubits, a public explicit exponent-p
Lazard group G with fixed class c<p, and efficient controlled LINEAR R(g).
Define the actual target

    H = {g : R(g) rho R(g)^* = rho}.

Promises, not known eigenvector data:

- Every positive eigenvalue lambda_j of rho is simple and at least w>0.
- Distinct positive eigenvalues differ by at least Delta>0. Zero may have
  arbitrarily large multiplicity; its eigenvectors are not required.
- For every g outside H, TD(rho,R(g)rho R(g)^*)>=delta>0.

Charge w^-1, Delta^-1, delta^-1. They must be polynomially bounded for the
efficient consequence. No eigenbasis, state-preparation inverse, conjugate
copies, classical density matrix, or known symmetry subgroup is supplied.
The positive rank is at most1/w. These restrictions are substantive, not
properties that can be inferred from generic mixed-state circuit input.

## Main Source Lemma

Write rho=sum_j lambda_j |psi_j><psi_j|. Simplicity gives

    H = intersection_j {g : R(g)psi_j is a phase times psi_j}.

The zero eigenspace is automatically preserved if every positive eigenray
is preserved. For each j, the phase on its ray stabilizer is a character;
its logarithm is linear on the associated Lie subalgebra, as in the
existing REES_PROJECTIVE_STATE_SOURCE.md argument.

Use that existing public multiset S of nonzero field evaluations, with
at least c distinct points and sum_(s in S) s^d=0 for1<=d<=c. Let M=|S|.
For the actual Rees cover A, use the representation

    T(a) = tensor_(s in S) R(E_s(a)).

Prepare a MATCHED spectral packet:

    Omega = sum_j lambda_j (|psi_j><psi_j|)^tensor(M).

The packet is intentionally correlated through one common spectral label.
It is NOT rho^tensor(M). Conditional on that label, all M systems are
fresh independent filtered copies. Different packets are independently
prepared. We treat each entire packet as one source for T; we do not invoke
an independent-marginals theorem on its correlated constituent systems.

The overlap is

    F(a) = Tr(Omega T(a))
         = sum_j lambda_j product_(s in S) <psi_j|R(E_s(a))|psi_j>.

Let h=log H and H_tilde=exp(sum_d t^d(h intersect gamma_d(L))). If
a belongs to H_tilde, every evaluation belongs to H. The moment equations
cancel every eigenray's character separately, so EACH product is1 and
F(a)=1. This does not require estimating any of the hidden characters.

If a is outside H_tilde, the separating evaluations give a g=E_s(a)
outside H. Put u_j=<psi_j|R(g)|psi_j> and A_g=sum_j lambda_j |u_j|.
Choose phases on a reference purification to align these diagonal terms.
The resulting two purifications have overlap A_g and reduce to rho and
R(g)rho R(g)^*. Contractivity of trace distance gives

    delta <= TD(rho,R(g)rho R(g)^*) <= sqrt(1-A_g^2).

Consequently |F(a)|<=A_g<=sqrt(1-delta^2)<=1-delta^2/2.
The purification and its reference phases are ONLY a proof comparison;
the algorithm never prepares or computes them. No individual eigenstate
orbit-gap promise is needed. Such individual gaps may be extremely small.

Thus Omega has an exact Bose stabilizer H_tilde under T, with a globally
paid overlap gap gamma=delta^2/2. The existing orbit-source amplification
and graded Rees receiver recover H under their unchanged hypotheses.
No second Rees cover is applied. At stage1 the recovered subspace is all h.

## Preparing A Matched Packet From Copies

Use sample-based controlled density-matrix evolution to spectrally measure
a fresh rho target, retaining it. Its hidden eigen-index j is distributed
as lambda_j; record an eigenvalue estimate e. This target is the first
copy of psi_j. For each further packet member, spectrally measure another
fresh rho and retain it only if its estimate is within Delta/2 of e.
Discard all nonmatching targets. No unknown-state cloning occurs.

When each estimate has error at most Delta/8, same-eigenvalue estimates
differ by at most Delta/4 and different ones by at least3Delta/4. Thus
matching is correct without a prelearned spectrum, eigenbasis, rank,
eigenvalue advice, or coupon-collector preprocessing. The seed and all
matched targets are never fed back as density-matrix simulation programs.
Those program copies are additional fresh rho inputs.

Ideal matching succeeds per attempt with probability lambda_j>=w. A cap L
on every additional member therefore has failure probability <=exp(-wL).
The unconditioned ideal packet before caps is exactly Omega. Capping does
not preserve its normalized conditional distribution exactly; instead the
ENTIRE abort probability is bounded and paid. Rejection-history records
depend on j and must not control subsequent group actions or be treated as
independent of the quantum packet. Erase/discard them; only the fixed public
evaluation sequence acts on the prepared packet. They may be retained for
analysis of the complete hybrid, never as uncharged hidden advice.

## Controlled Density-Matrix Evolution Is Paid

This is a known primitive, not our discovery. See
[Kimmel et al., Hamiltonian Simulation with Optimal Sample Complexity, Appendix C](https://arxiv.org/html/1608.00281#A3),
including the controlled construction. To avoid depending on a normalized
branch or an unspecified norm convention, the needed bound follows directly.

Let C=|1><1| on the control, S the target/program SWAP, K=C tensor S,
and H_eff=C tensor rho. On arbitrary target/control/reference input sigma,
apply exp(-i theta K) to sigma tensor rho and trace the program. The
derivative at theta=0 is -i[H_eff,sigma]. Both this channel and the ideal
exp(-i theta H_eff) channel have second derivative of diamond norm<=4:
the commutator norm is at most2, unitary conjugation has norm1, and partial
trace/program preparation are channels. Taylor's integral remainder yields

    half_diamond(actual_step, ideal_step) <= 2 theta^2.

N fresh program copies with theta=t/N therefore simulate the CONTROLLED
evolution to half-diamond error<=2t^2/N, including coherent controls and
arbitrary references. Partial SWAP exponentials are public gates; their
synthesis errors are separately budgeted. Neither an inverse preparation
nor a spectral projector is granted for free.

For spectral estimates use binary QPE with U=exp(i*pi*rho/2), whose phases
are lambda_j/4 in[0,1/4]. Interpret measured phases in[-1/2,1/2), including
wraparound near zero. With grid P=2^t>=128/(Delta*zeta), the standard
inverse-square tail gives an eigenvalue error exceeding Delta/8 with
probability at most zeta. This bound holds for every eigenstate. On a fresh
rho input, the ideal spectral experiment is a classical mixture over its
eigen-index; union-bound bad estimates across all capped attempts. No
division by a successful matching probability is needed.

The controlled time for bitk is(pi/2)*2^k<2*2^k. Assigning DME error eta/t
per bit uses at most ceil(8*t*4^k/eta) fresh program copies at that bit.
This is polynomial in inverse promised separation and inverse accuracy,
not logarithmic in them. The numeric grid is NOT itself a free fast power:
unlike public Rees translations, density evolution pays its actual time.

## Complete Resource Schedule

Let B be a deterministic cap on all receiver leaves, ell a public upper
bound on log2|A|, and epsilon the full error allowance. Reserve epsilon/2
for public addresses, controlled representation gates, design preprocessing
and the existing Rees receiver. The new source budget is:

    gamma = delta^2/2
    k = ceil((ell + ceil(log2(8B/epsilon)))/gamma)
    Q = B*k                         matched spectral packets
    L = ceil(ceil(log2(8QM/epsilon))/w)
    S = Q*(1+(M-1)*L)              all spectral measurements
    zeta = epsilon/(8S)           bad value probability per measurement
    eta = epsilon/(16S)           DME channel error per measurement

Allocate another epsilon/(16S) to that measurement's public circuit gates.
The total new error is at most epsilon/2: source amplification epsilon/8,
matching aborts epsilon/8, bad estimates epsilon/8, and implementation
epsilon/8. On bad histories the SAME resource clocks apply; no retry loop
is allowed to escape them. Approximate filters are compared as complete
instruments; exact successful-eigenstate promises are used only in the
ideal comparison experiment.

For completeness, source amplification uses uniform public addresses in A
and k independent packets. Let N=|A|. An address-density entry is
F(b^-1 a)^k/N, with the order fixed by the chosen representation convention.
Entries within a hidden coset agree exactly with the ideal coset source;
the remaining differences have modulus at most exp(-gamma*k)/N. Hence the
Frobenius error is at most exp(-gamma*k), and half the trace-norm error is
at most sqrt(N)*exp(-gamma*k)/2, in particular at most N*exp(-gamma*k).
The displayed k makes the latter at most epsilon/(8B), since each base-two
logarithm used in the planner upper-bounds its corresponding natural log.
Summing across the capped B leaves gives the stated amplification budget.
This does not use an efficient classical enumeration of the N addresses.

Raw copies are at most S times(one target plus the sum of the controlled
evolution program budgets). The planner computes that integer cap without
enumerating Hilbert space, group elements, or source branches. It is a
loose polynomial resource certificate at fixed class and inverse-polynomial
promised gaps, not a practical estimate. M's existing fixed-class design
cost and the receiver's potentially enormous B remain visible.

## Attempts To Break The Claim

1. DEGENERATE POSITIVE EIGENVALUES: the reduction is false. For rho=I/3 and
   the Heisenberg shift, conjugation leaves rho invariant, but a packet of
   repeated computational eigenvectors has overlap zero. The source would
   discard genuine symmetries. Do not choose a basis inside a degenerate
   eigenspace and pretend those eigenrays are the target.
2. INDEPENDENT MIXED TARGETS: replacing Omega by rho^tensor(M) is false.
   In the tested rank-two source, a genuine diagonal conjugation symmetry
   has mismatched eigenphases. The balanced matched packet has overlap1;
   the independent-marginal product does not.
3. ONLY PRINCIPAL EIGENSTATE: insufficient. Other eigenvectors can break
   a symmetry of the leading state. The weighted packet covers all occupied
   eigenrays without incorrectly requiring separate global orbit gaps.
   An order-three control fixes the leading eigenvector while changing the
   mixed state by trace distance>0.08. A small public conjugation of that
   operation instead gives the leading vector an overlap gap below10^-6
   while the mixed-state distance remains>0.08.
4. SMALL WEIGHTS/SEPARATIONS: matching or density simulation can take
   superpolynomial copies. The promise parameters cannot be hidden under
   a statement about only log Hilbert dimension or the Rees group class.
5. GENERAL MIXED-STATE HARDNESS: no contradiction. The known circuit-input
   mixed StateHSP result is QSZK-hard in the worst case, not under these
   spectral promises. See [Gheorghiu et al., Section5.3](https://arxiv.org/html/2605.12615v2#S5.SS3).
   This note neither reproves that result nor claims to solve its full input.
6. CLASSICAL COMPARISON: explicit sparse, low-width tensor or tableau data
   can make these symmetries easy. Copies of an unknown exponentially large
   state are a different input model from a classical density-matrix table.
   No classical lower bound or natural hard laboratory family is established.

## Scope And Next Decisive Work

This extends a conditional SOURCE interface from scalar-support symmetry
to genuine conjugation symmetry for a restricted mixed-state task. The
existing Rees theorem and zero-moment design are reused, not rediscovered.
No novelty claim follows from the targeted literature search. The direct
full-rank/degenerate mixed-state extension is explicitly rejected.

The controls use the actual previously tested Rees evaluation maps, a
genuine nonabelian representation, literal matched tensor packets and a
literal controlled partial-SWAP channel with a reference. They do not run
the spectral preprocessing or the receiver at native scale. Known diagonal
test states are calibration only, never research candidates or hardness data.
An exact cap countercontrol also shows the bias being charged: with weights
(2/3,1/3), a six-member packet and just one attempt per member, success
conditions the seed weights to(64/65,1/65), not(2/3,1/3). Abort mass is664/729.

Next: scrutinize this precise mixed-source reduction and seek a motivated
state family with the required separations. Do not broaden it to arbitrary
noise or certify its gap from a few overlaps. Gemini may implement the
capped preprocessing controller later; no UI campaign or registry speedup
admission is warranted. This is not yet a Shor-level application.
