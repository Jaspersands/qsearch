# Average-Robust Low-Rank Mixed-State Symmetry Source

2026-10-25. NEW LOCAL CONDITIONAL COMPOSITION; independent review pending.
This is not a new antisymmetrization primitive, implemented quantum learner,
novelty certificate, classical separation, or natural hard application.
The completed independent review of the PURE dilation source does not cover
this new composition or certify its coarse-spectrum dependency.

## The Actual Improvement

The earlier low-rank mixed-state construction requires a minimum displacement
for every individual nonsymmetry. That can vanish exponentially in log(p).
The reviewed random-dilation construction removes that requirement for PURE
states. A covariant decoding channel connects the two constructions: spectral
wedge packets retain subgroup-averaged robustness of the mixed input.

The task is unchanged: recover the EXACT conjugation stabilizer of rho
inside the supplied group. No new hiding oracle or artificial search problem
is introduced. The low-rank restriction and paid coherent action remain.

Input:

- Fresh IID copies of an unknown rho on q qubits, with rank(rho)<=R supplied.
- An explicit prime-field Lazard group G=exp(L), class<=3, prime p>=131.
- A uniform coherent SELECT(U), implementing a LINEAR unitary representation
  U of G, with native width and gate cost C_U(eta) explicitly charged.
- delta>0 such that, for every subgroup K not contained in
  H={g:U(g)rho U(g)^*=rho},

      TD(rho,T_K(rho)) >= delta,
      T_K(X)=|K|^-1 sum_(g in K) U(g) X U(g)^*.             (P_avg)

No twirling oracle, H, eigenbasis, spectrum, exact rank, inverse preparation,
or conjugate copies are supplied. Polynomial efficiency is conditional on
polynomial R, inverse delta, and the charged source/action/receiver costs.
The promise is not certified by the finite controls or resource planner.

## 1. Coarsening Without A Pointwise Promise

Reuse the coarse-spectrum construction, but set h=delta/(128R). For its
finite random offset u in [0,h), discard eigenvalues below c=h+u, and round
each remaining bin down to its distinct positive endpoint a_j. Write

    A = sum_j a_j P_j,  m=Tr(A),  e=||rho-A||_1.

The old rounding proof is purely spectral and gives

    0<=A<=rho,  e<=2Rh=delta/64,  m=1-e>=63/64.

The matrix and projectors are analysis objects, not algorithm inputs.
Every symmetry of rho fixes A. If g fixes A, its entire cyclic subgroup
K=<g> fixes A. Contractivity and the triangle inequality give

    TD(rho,T_K(rho)) <= TD(rho,A)+TD(A,T_K(A))
                         +TD(T_K(A),T_K(rho)) <= e < delta.

Therefore (P_avg) forces g in H: Stab(A)=H exactly. This replaces the
earlier pointwise argument. It does NOT infer a pointwise displacement gap.

For ANY subgroup K not contained in H, the same triangle inequality yields

    TD(A,T_K(A)) >= delta-e.                              (1)

Trace distance here means half the trace norm, also for the subnormalized A.
No normality assumption on K or H enters this calculation.

## 2. The Covariant Decoder

For each retained bin of rank r_j, let omega_j be its normalized top wedge,
and let sigma=|Psi><Psi| for Psi=tensor_j omega_j. Use the representation
V(g)=U(g)^tensor(sum_j r_j), padded by identity on unused registers if needed.
The existing capped spectral filtering and corrected growth construction
prepares these packets without learning any frame.

Define a channel Lambda on the ENTIRE packet Hilbert space. With probability
w_j=a_j*r_j/m, keep one specified register of wedge block j and trace out
every other register. All w_j are nonnegative and sum to one, so this is CPTP.
The definition uses only bin endpoints and ranks, not hidden eigenvectors.
The algorithm need not execute this channel; it is a proof witness.

The one-register reduced state of a normalized rank-r_j wedge is P_j/r_j.
Consequently

    Lambda(sigma)=sum_j w_j P_j/r_j = A/m.                 (2)

Partial trace commutes with identical unitary actions on every active factor.
For EVERY packet operator X, not just sigma,

    Lambda(V(g) X V(g)^*)=U(g) Lambda(X) U(g)^*.

It follows that Lambda commutes with averaging over ANY subgroup. Combining
contractivity, (1), and (2),

    TD(sigma,T_K^V(sigma))
      >= TD(A/m,T_K(A/m))
       = TD(A,T_K(A))/m
      >= (delta-e)/m >= delta/2.                          (3)

The loose final constant deliberately leaves slack. The normalization m is
essential: A is not a density matrix before division. There is no factor
depending on Hilbert dimension, minimum eigenvalue, spectral separation,
or number of subgroup elements in (3).

The ray stabilizer of Psi is exactly Stab(A)=H. One direction follows from
(2) and covariance. Conversely, each g fixing A preserves every distinct
positive eigenspace P_j, and acts on its top wedge by a determinant phase.
Their product is a character on H. Internal degenerate rotations are kept;
we do not require chosen eigenvectors to be fixed.

This channel argument applies to any finite group with the supplied unitary
action. The efficient receiver consequence below is only for the stated
class-three, odd-prime regime, not arbitrary finite-group HSP.

## 3. Apply The Existing Pure Dilation Compiler

Use (3) as the input robustness of the reviewed pure-state source. The
existing universal Rees curve has conservative walk gap 1/8. Its forward-only
zero-moment packet, with a fresh uniform scale per packet, has overlap exactly
one on the SAME lifted H and off-subgroup overlap at most

    1 - gamma,  gamma = (delta/2)^2/16 = delta^2/64.

No second Rees cover is introduced. All original copies are mixed rho copies;
the pure packets are acquired by the existing paid extraction, not granted.
The useful new deduction is the mixed-to-pure average-promise transfer.
The spectral filtering, antisymmetrization and pure dilation results are reused.

## 4. Shared Grid Is Not Shared Dilation Randomness

Choose ONE public finite random spectral grid and infer its ranks once using
the old capped preprocessing. Reuse that metadata for all source packets.
Conditional on a good grid and correct metadata, each successful ideal
extraction produces exactly the same pure density sigma, regardless of its
growth/fetch record. Disjoint fresh input streams give independent copies
conditional on that grid. Different grids can produce different sigma and V.

There is NO claim that packets are IID after averaging away the grid.
Instead, (1)-(3) and the receiver bounds hold uniformly for every good grid,
with the same original H. Analyze the entire computation conditional on the
grid, then average its full output/error bound. Charge the probability of a
bad grid or incorrect preprocessing record once. The old complete-instrument
hybrid accounts for aborts and imperfect operations without renormalizing
successful branches.

Within each zero-moment packet the M extracted pure copies MUST use the same
grid and metadata; otherwise their determinant characters can differ and fail
to cancel even on H. The supplied countercontrol demonstrates that failure.

Dilation scales have the opposite rule: sample a FRESH independent scale for
each complete M-copy moment packet. The previous exact shared-scale control
already disproves substituting one random scale for the whole source bank.
Both requirements must survive any later circuit/controller implementation.

## 5. Charged Schedule And Scope

Reuse ONLY the old coarse-source planner's arithmetic with its numeric gap
argument set to delta/4. This sets h=delta/(128R) and charges amplification
using gamma_clock=delta^2/128, smaller than the proved delta^2/64. Its old
pointwise-gap theorem is NOT used. Remove its pointwise gap fields from the
new public report; they would be false under the new contract.

Let B be the supplied receiver-leaf cap, M the valid moment-design size,
k the returned amplification count, and W=B*k*M extracted pure packets.
All old growth, filtering, QPE, density-evolution and abort clocks are
recomputed at the new grid and W. The source may be extremely expensive.
Polynomial is not a practical gate estimate; the receiver cap and design
validity remain external obligations.

There are S_scale=B*k fresh field scalars. Rejection sampling uses b=bitlen(p)
random bits per attempt and at most L=ceil_log2(32*S_scale/epsilon) attempts.
Each trial accepts with probability >1/2, so total timeout probability is
at most S_scale*2^-L<=epsilon/32. A timeout is ABORT. Uniformity conditional
on acceptance is exact; u=0 is allowed in this source compiler.

Add this epsilon/32 category to the old 7epsilon/8 budget: total allocation
is 29epsilon/32, leaving 3epsilon/32 slack. All other old budgets are retained,
including the epsilon/2 reserve for the existing receiver/public operations.

Each pure packet has at most R physical registers, so original SELECT(U)
queries are bounded by Q=R*W. Allocate eta_U=epsilon/(32Q) per original call.
Its gate contribution is Q*C_U(eta_U), NOT Q elementary gates. Also charge:
all raw rho acquisition; q-qubit partial SWAPs; spectral/growth public gates;
the complete design, arithmetic, addresses, randomness and receiver. The
planner explicitly reports total_gate_cost_certified=False.

Native inputs are exact IID copies. Per-copy trace-distance error nu costs
at most N_raw*nu in addition; it is not silently covered by the displayed
epsilon ledger. No correct-marginal/frozen-bank replacement is allowed.

## 6. A Genuine Promise Difference, Not A Hard Example

For every prime p>=131, take the rank-two, one-qubit state and C_p action

    rho=[[1/2,1/4],[1/4,1/2]],  U(t)=diag(1,exp(2*pi*i*t/p)).

H is trivial. The only nontrivial subgroup is C_p and its twirl is I/2:

    TD(rho,T_Cp(rho))=1/4,
    min_(t!=0) TD(rho,U(t)rho U(t)^*)=sin(pi/p)/2.

Thus the old inverse pointwise gap grows as p while the new promise stays
constant. Its separate spectral wedges are |+> and |->. The squared packet
overlap averaged over C_p is 3/8, from the three charge masses 1/4,1/2,1/4.
This is a symbolic growing-prime separation between ASSUMPTIONS, not a quantum
advantage: the state has a tiny explicit description and is classically easy.
The p=131,257 evaluations only check formulas and decoder normalization.

## 7. Attempts To Falsify The Composition

- A whole-support wedge fails: it forgets unequal spectral weights. The
  decoder needs distinct spectral-bin blocks, not one wedge of all support.
- A falsely supplied delta can let coarsening merge all relevant eigenspaces
  and enlarge H. The example with nearly equal qubit eigenvalues has an
  arbitrarily small subgroup-twirl defect. The promise is substantive.
- Substituting pointwise displacement for (3) is unjustified and contradicted
  by Section 6. Old pointwise lower-bound report fields are explicitly removed.
- Incorrect rank metadata, bad grids, fine-measurement dephasing on arbitrary
  superpositions, and uncorrected growth are not repaired by this argument.
  We rely on the original fresh-target, capped, corrected-instrument proof.
- Shared random grids are handled conditionally; shared dilation scales are
  not. Interchanging these two rules invalidates the independence argument.
- High rank is still excluded. The prior mixed-copy lower bounds remain.
  This is not general mixed-state isomorphism or approximate-symmetry recovery.
- Supplied density tables, tableau/low-width descriptions, and known abelian
  learners remain classical/quantum baselines. The one-qubit example is easy.
- Only the pure dilation component has an independent AI review. No claim of
  review, Lean verification, novelty, or physical execution transfers to this
  composition. The spectral extraction proof remains a dependency risk.

## Decision And Dependencies

The pointwise-gap requirement can be removed for the same low-rank mixed task
under the stated subgroup-average promise and class-three restriction. This
is a bounded theorem-scope improvement, not a newly useful hard application.
Do not launch another parameter/control campaign or admit a speedup candidate.

Read with ../rees-coarse-spectrum-2026-10-24/COARSE_SPECTRUM.md and
../rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md. The known
copy-based primitives remain attributed to
[Kimmel et al.](https://arxiv.org/html/1608.00281#A3) and
[Bene Watts et al.](https://arxiv.org/html/2610.06737v1).
Their results do not certify the local group-theoretic composition.

A targeted check of Bene Watts et al., Section 5, found a gapped mixed-to-pure
one-way-state-generator reduction using the whole-support wedge. That is not
a theorem preserving this exact conjugation-stabilizer task or its averaged
gap. Their Section 1.2 explicitly notes loss of spectral information. This
distinction supports retaining separate spectral-bin packets here; it does
not establish novelty of our composition or refute their cryptographic result.

Next consequential scientific work: scrutinize the complete source composition
and seek a useful native family or specialist novelty comparison. Removing
more nearby assumptions without either would again risk low-impact extension.
