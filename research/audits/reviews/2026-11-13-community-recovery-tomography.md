# 2026-11-13 Finite one-particle tomography for community recovery

## Precise interface and conclusion

Condition on the frozen classical arrays and a fixed preparation protocol.
Assume fresh reproducible copies of one fixed density sigma on (C^n)^tensor ell,
with ell<=n, are available, and put

    rho=(1/ell)sum_j Tr_except_j sigma,  R=Re(rho),
    Tr(P_L rho)>=mu>0.

Here L is the real planted color span; it is never provided to the algorithm.
The actual accepted state may be complex or mixed. The proof assumes product
copies conditional on the frozen arrays. A sufficient sequential formulation
is that each new output has conditional state sigma given the complete preceding
measurement history in this schedule. Equal one-copy marginals alone do not
suffice for the concentration argument.

With at most O(n^6 log(n/eta_tom)) accepted copies, explicit finite measurements
and rational arithmetic produce a rational PSD trace-one matrix Rtilde with

    Rtilde >= R/2,      Tr(P_L Rtilde)>=mu/2,                        (1)

except with probability at most eta_tom. There is an exact PSD check and ABORT
on invalid output, so the subsequent rational rounding routine never receives
an indefinite matrix. No eigenbasis or PSD-projection oracle is used.

This pays the readout interface only. Source law, reproducibility of accepted
copies, their preparation cost, and their mass premise remain explicit inputs
from the retention review. STATE/TRAPS and the stable rounding proof were read;
no API/network/Git, archive, numerical experiment, or shared-status edit occurred.

## 1. Measuring the averaged marginal with finite schedules

Use one computational-basis batch for ALL n diagonal entries, and one separate
batch for each unordered pair i<j. Set

    b=ceil(log2(2n^2/eta_tom)), m0=n^4*b,
    m=ell*ceil(m0/ell),
    M=[1+binom(n,2)]*m <= 2n^6*b.                                 (2)

Integer bit lengths may replace the logarithmic ceiling with a larger integer.
In EACH batch cycle deterministically through the ell slot indices, measuring
each slot on exactly m/ell fresh copies of sigma. Discard the other registers
afterward. This realizes the averaged marginal in expectation exactly; no
approximate uniform-slot coin or repeated use of the same copy is needed.
Outcomes are independent across copies, although their slot-dependent laws
need not be identical. Hoeffding applies to this independent nonidentical case.

For the diagonal batch, let c_i be the computational outcome count and set

    Rhat_ii=c_i/m.                                                 (3)

Thus sum_i Rhat_ii=1 EXACTLY, because all diagonal estimates use one batch.
There is no later random trace renormalization.

For pair i<j, measure in the basis containing
|+>=(|i>+|j>)/sqrt(2), |->=(|i>-|j>)/sqrt(2), with all other basis vectors
unchanged. Record X=1/2 for +, -1/2 for -, and zero otherwise. Its mean on
a marginal rho_j is Re((rho_j)_ij), since p_+-p_-=2Re((rho_j)_ij). Set

    Rhat_ij=Rhat_ji=(c_+-c_-)/(2m).                                (4)

This factor is 1/2, not one or 1/4. The resulting Rhat is real symmetric
and rational even when the actual marginal has imaginary coherences.

## 2. Explicit pair-basis circuits

Embed the n outcomes in q=ceil(log2 n) qubits. An invertible affine binary
map sends the public pair i,j to 0 and one coordinate vector: XOR i, then
send the nonzero difference j XOR i to that vector by CNOT row operations.
This costs O(q^2) elementary reversible gates. Apply H to the differing bit,
controlled on the other q-1 bits being zero, then undo the affine map.
The resulting unitary is exactly the two-level Hadamard on i,j and identity
elsewhere. Computational measurement afterward realizes the required basis.

Multiple controls are computed into a clean ancilla with Toffoli gates and
uncomputed. Controlled-H itself has an exact Clifford+T realization: with
V=S H T H S^dagger (RY(pi/4) up to global phase), V Z V^dagger=H, so
(I tensor V) CZ (I tensor V^dagger) is controlled-H. The global phases cancel.
Hence these measurements use a fixed finite gate set and no arbitrary-angle
rotation compiler. Their gate count per accepted copy is O(log^2 n), with
polynomially bounded clean work. n=1 is trivial and has no pair batches.

The ideal input occupies only the valid n-level subspace. Padded binary
outcomes may be treated as an immediate ABORT; they have zero probability
under this interface and these exact measurement circuits. Any invalid-label
leakage in a separate approximate preparation must be charged there.

## 3. Concentration, trace adjustment, and exact PSD protection

Every variable used in (3),(4) has range of length one. For each entry,

    Pr(|Rhat_ij-R_ij|>1/n^2) <= 2exp(-2m/n^4).

There are n+binom(n,2)<=n^2 estimated real entries. A union bound and (2)
give simultaneous entry error <=1/n^2 with probability >=1-eta_tom. The
diagonal entries within their batch need not be mutually independent; this
union bound requires only independence across the copies used by each mean.

On that event E=Rhat-R is real symmetric and

    ||E||op<=||E||F<=n*max_ij|E_ij|<=1/n.

Define, without any estimated eigenvalues,

    Rtilde=(Rhat+I_n/n)/2.                                        (5)

Then Rhat+I_n/n>=R>=0, proving (1). Its trace is (1+1)/2=1 exactly.
R=Re(rho) is PSD because its real quadratic forms equal those of rho;
as a real symmetric matrix this also proves complex PSD. Moreover P_L is
real, so Tr(P_L R)=Tr(P_L rho). No rank-dependent mass loss occurs in (5).

Rhat has a common denominator dividing 2m, and Rtilde one dividing 4mn.
All coefficient bit lengths are O(log m+log n). To protect every branch,
test Rtilde>=0 exactly before rounding. Symmetric Schur-complement elimination
suffices: reject a negative diagonal; a zero diagonal with a nonzero row has
an indefinite two-by-two principal minor, while a zero row can be removed.
Otherwise pivot on a positive diagonal. Positive-pivot Schur complements
preserve the PSD equivalence.
There are at most n pivots. Fraction-free elimination/minor bounds give
polynomial bit lengths and time. This is a decision test, not a projection.
On the good estimation event it cannot ABORT. On its complement, an accepted
matrix is still PSD/trace-one, but its mass guarantee may fail within the
already charged probability eta_tom.

## 4. Accepted-copy and abort clocks; dependence boundary

The measurement schedule consumes exactly M accepted copies unless it aborts.
If the retained-state factory offers bounded-cost fresh attempts with a known
success lower bound s0>0 and the same normalized success output sigma, cap
each requested copy at

    Lcap=ceil(s0^-1 log(M/eta_cap))

attempts, and ABORT if none succeeds. The factory is invoked at most M*Lcap
times and this cap adds failure at most eta_cap. Larger integer log bounds
give a completely finite clock. Insert the retention review's actual s0 and
attempt cost here; neither is free or established by this readout lemma.

Fresh tensor-product attempts with a fixed success instrument produce product
copies of sigma conditional on any success/failure flag schedule. Therefore
first-success stopping and this cap do not bias successful outputs under
that premise. A shared random hidden state copied repeatedly instead would
invalidate the premise and Hoeffding, even if each marginal equaled sigma.
Conditioning on frozen graph arrays is legitimate: all the preceding bounds
are uniform conditional statements and can then be averaged over those arrays.
Freeze the accepted-state protocol before tomography; changing its normalized
output separately for different entry batches would not estimate a single R.

The fixed ACTUAL sigma may already incorporate circuit approximation. If
instead comparing each prepared copy to an ideal sigma, its approximation
error must be paid separately, for example by the M-copy hybrid bound. This
is distinct from a frozen input-law TV comparison, which transfers through
the entire algorithm once and is not multiplied by the number of copies.

## 5. Composition with the already proved classical readout

On the mass and frame-balance events, apply the rational rounding lemma to
Rtilde with parameter mu/2. It produces a constant list with agreement
advantage at least

    Delta'=mu^2/[4096*k^2*(k-1)]

except for its separately bounded rounding failure. Its rational Jacobi,
net, clipping and fixed-bit coins have polynomial cost on the coefficient
sizes above. Use the already proved UNIFORM original-Y score event to select
one labeling. It covers graph-dependent candidates, so no independent
validation graph, new clone, or independence between Rtilde and Y is assumed.

The readout adds eta_tom+eta_cap and the rounding failure to the existing
source/mass, balance and uniform-validation exceptional probabilities. Its
new quantum work is M accepted-copy requests and O(M log^2 n) exact gates;
its classical statistics/PSD test/rounding/scoring have polynomial BIT cost
for fixed p,k. No accepted-copy preparation or full quantum recovery theorem
is inferred solely from this conditional interface.
