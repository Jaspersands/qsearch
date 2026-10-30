# Offline Local Tangents: A Constructive, Still Patch-Exponential Route

2026-10-24. LOCAL UNREVIEWED deduction and capped classical controls.
No new polynomial preparation theorem, independently reviewed proof,
quantum execution, novelty certification, or speedup claim.

## 1. Scientific Decision

The previous pass tightened the classical baseline for diagonal Rees inputs.
This pass returns to the unresolved coherent HDQI pilot, asking a different
constructive question: can target local data be obtained without already
preparing the target, and converted into bounded unitary updates?

The answer below is conditional on the existing marked-cluster observable
proof and a quantitative local covariance bound. It gives an offline
compiler whose cost is exponential in patch size. It eliminates neither
patch growth nor the general degree-scale preparation blocker.

Primary context: [Motta et al., QITE](https://arxiv.org/html/1901.07653),
including Supplemental Information A.1-A.3, already uses local marginals,
Uhlmann's theorem, and least-squares local unitaries. The present note does
not claim those ideas. [Hastings--Schmidhuber, Section VI](https://arxiv.org/html/2610.03697v1#S6)
applies a related strategy to redundancy-free TFD preparation. Its Section
V.2 provides a canonical bipartite-graph entanglement counterexample;
separability is not a valid substitute for preparation in the desired regime.

Local contribution here: an explicit bounded polar formula, a trace-error
budget, and a fixed-endpoint compilation argument that needs no derivative
bound on the selected polar factors. These are elementary consequences of
standard tools, not a claimed new QITE paradigm. Do not interpret this as
a demonstrated fatal flaw in either cited paper.

## 2. Exact Access And Output

Input: explicit simple graph on m vertices, rational real |J_i|<=1, beta,
and canonical independent Paulis

    O_i = X_i product_{j<i, j~i} Z_j,  H = sum_i J_i O_i.

Target: the normalized TFD

    psi(t) = vec(exp(-t H/2)) / ||exp(-t H/2)||_F,

with one left and one right register, initially Bell pairs. The equivalent
pilot follows by the known explicit graph Clifford W. No target copies,
state-preparation oracle, density table, exact spectrum, or reflection are
inputs. Lambda=sum_i |J_i| is a public upper bound on ||H||.

For every term and time-grid point supply a patch containing its entire
left-register support, possibly also right-register qubits. Require

    eta_i(t) = sup_{||C||<=1, C outside patch}
               |<psi(t)|(O_i-<O_i>) C|psi(t)>| <= eta.       (1)

The supremum includes JOINT operators on all outside qubits of both copies.
Decay for individual Pauli probes or ordinary Gibbs two-point functions
does not establish (1). A correlation theorem with exact constants and
supports is a dependency, not inferred by this implementation. In the
canonical representation, O_i can occupy d+1 qubits, not a fixed-size site.

The prior local construction in
../hdqi-defect-observables-2026-10-24/DEFECT_OBSERVABLES.md supplies a claimed
classical additive estimator for ANY pilot Pauli when

    (d+1) (beta max_i |J_i|)^2 <= 1/64.                     (2)

That proof remains unreviewed; its current implementation is a capped
reference, not a production FPRAS. This pass does not upgrade its status.

## 3. Bounded Polar Tangent Without Inverses

Let O be a balanced Hermitian involution on a local patch. Use a fixed local
basis in which O=Z_A tensor I_B; a nonidentity Pauli has such a basis. Write

    psi = sqrt(p)|0>u_BC + sqrt(q)|1>v_BC, p+q=1,
    rho_AB = [[rho_00, R], [R*, rho_11]], r=||R||_1.

Take a FULL unitary polar completion W of R: if R=L Sigma V*, use W=L V*.
Define

    c=2r,
    K = c [[0, W], [-W*, 0]].                              (3)

Positivity gives r<=sqrt(pq)<=1/2, so ||K||=c<=1 and K*=-K.
Singular R is allowed. If r=0, K=0 regardless of completion. No inverse,
small-eigenvalue cutoff, minimum population or spectral separation appears.

For any c in [0,1] and unitary W, the squared tangent loss is

    J_rho(K) = ||(O-<O>)psi-K psi||^2
             = 1-<O>^2 + Tr rho (K* K - [O,K])
             = 4pq+c^2-4c Re Tr(R* W).

Thus (3) minimizes this objective over this fixed rho-independent class,
and its loss is exactly 4pq-4r^2. It need not minimize over every possible
anti-Hermitian generator; no such assertion is required.

If p,q>0, Uhlmann gives r=sqrt(pq) f, where f is the root fidelity of the
two normalized conditional C-marginals. Also

    eta = 2pq ||rho_C(u)-rho_C(v)||_1.

Since 1-f <= ||rho_C(u)-rho_C(v)||_1/2 and 1-f^2<=2(1-f),

    J_rho(K)=4pq(1-f^2) <= 2 eta.                         (4)

At p=0 or q=0 both the tangent and K vanish. This handles empty sectors
directly. General balanced Pauli eigenspaces just change the local basis.

## 4. Noisy Marginals And Polar Discontinuities

For two density matrices with ||rho-rho_hat||_1<=tau, every anti-Hermitian
K with ||K||<=1 obeys

    |J_rho(K)-J_rho_hat(K)| <= 5 tau.                      (5)

The expectation-square term costs at most 2tau; K*K and [O,K] cost at most
tau and 2tau. Apply (5) twice, using the same minimization class in Section
3. An approximate polar minimizer with objective excess at most xi gives

    J_rho(K_hat) <= 2 eta + 10 tau + xi.                   (6)

Do NOT infer ||K_hat-K||=O(tau). This is false near a singular off-diagonal
block. The tests give an operator jump >0.79 for density changes <5e-12,
while the tangent objective remains stable. Only the action-error statement
(6) is needed. Approximate numerical polar factors must be charged through
an objective certificate plus anti-Hermiticity/norm control, not presumed
to approximate a chosen exact polar factor in operator norm.

For an s-qubit patch, D=2^s. Estimate all D^2-1 nonidentity Pauli means to
error alpha and set the identity coefficient to 1. Orthogonality gives
Frobenius error <=sqrt(D) alpha. Project the reconstructed Hermitian matrix
onto PSD trace-one matrices in Frobenius norm. Euclidean projection is
nonexpansive because the true density lies in this convex set. Then

    ||rho_hat-rho||_1 <= D alpha.                         (7)

Use alpha=tau/D, NOT tau. Spectral simplex projection implements this;
clipping eigenvalues and renormalizing is not the same projection.

## 5. Paying For True Target Data

The canonical Clifford W sends TFD to pilot tensor zero ancillas. Each
TFD Pauli conjugates to exactly one signed Pauli. Its expectation is zero
if any zero ancilla has X or Y; otherwise it is one signed pilot Pauli.
`tfd_pauli_pullback` implements this in polynomial symbolic time, including
all Y and CZ phases, without constructing W or a density table. Tests
exhaust all paired Paulis for both two-vertex graphs.

Consequently (2) plus the PRIOR local observable proof supplies the moments
in (7) at specified true target times. Compute them classically BEFORE
quantum execution, and budget failure across all m*T*(D^2-1) estimates.
Their accuracy is tau/D, so their runtime also grows exponentially in s.
Apply the condition at the maximum beta; all earlier grid times qualify.

This is a proof-level access reduction. The live controls instead evaluate
small dense exact target states, conspicuously labeled as reference access.
Neither that reference nor a callback argument implements the FPRAS.
The 128-vertex symbolic pullback is executed, but no 128-qubit state is built.

Do not silently replace offline true marginals by tomography of the current
approximate state. The above proof would acquire state-dependent tangent
errors. Unitary telescoping alone does not give a stability theorem for that
different adaptive controller. This is a proof limitation, not a general
failure theorem for adaptive QITE.

## 6. Fixed-Endpoint Evolution Needs No Generator Derivative

The correctly normalized imaginary-time path satisfies

    psi' = -(H-<H>)psi/2,
    psi'' = ((H-<H>)^2/4 - Var(H)/2)psi,
    ||psi''|| <= 3 Lambda^2/2.                            (8)

At t_j=j beta/T choose each K_ij from its offline marginal; selections can
be discontinuous. Set B_ij=-J_i K_ij/2 and B_j=sum_i B_ij. Then

    ||B_j||<=Lambda/2,
    ||psi'(t_j)-B_j psi(t_j)|| <= Lambda r0/2,

provided each tangent residual is <=r0. Over a step h, Taylor's integral
remainder for the true path costs 3h^2 Lambda^2/4. The unitary exponential
remainder costs h^2 Lambda^2/8. A first-order product of the individual
exp(h B_ij) differs from exp(h B_j) by at most

    (h^2/2) sum_{i<k} ||[B_ij,B_kj]|| <= h^2 Lambda^2/8.

The complete step cost is therefore h Lambda r0/2+h^2 Lambda^2.
Telescoping these FIXED unitary steps gives

    ||prepared-psi(beta)|| <= beta Lambda r0/2
                             + beta^2 Lambda^2/T
                             + sum_gate_errors.           (9)

No derivative of K, spectral gap, postselection, inverse thermal map, or
Gronwall amplification is used. Local matrix unitaries still require paid
generic synthesis, polynomial in D and logarithmic precision. This is
not a small circuit claim.

For requested vector error epsilon choose

    r0 = epsilon/[2(1+beta Lambda)],
    T = max(1,ceil(4 beta^2 Lambda^2/epsilon)),
    eta <= r0^2/8, tau <= r0^2/40, xi <= r0^2/2,
    per-local-unitary operator error <= epsilon/(4mT).

Equations (6) and (9) give total error <=3epsilon/4, leaving slack.
The plan records these as REQUIREMENTS, never certificates that (1) holds.

## 7. What This Does Not Solve

The compiler cost is poly(m,T,D,1/tau,log(1/failure)), not poly(m,1/epsilon)
when s grows faster than log(m/epsilon). A doubled physical ball has
s=2|B| qubits and 4^s moments. Exact enumeration of its Hilbert space is
fully charged even if each individual moment is efficiently estimable.

If (1) has a certified bound A*C^(-ell), then ell must grow with
log(A/eta)/log C. For degree d>2, the elementary ball bound is

    |B| <= min(m, 1+d sum_{k=0}^{ell-1}(d-1)^k).

A logarithmic radius need not give a logarithmic ball. Do not call this
uniformly subexponential for growing d without separately checking that
|B|=o(m), or polynomial without |B|=O(log m). Polynomial-volume geometry
can improve the bill, but low-treewidth/tensor-network classical baselines
must then be compared. The numerical ball rows are upper-bound ledgers,
not proofs that every graph attains them or lower bounds against all methods.

Other falsifiers and limitations:

- The marked-cluster observable theorem may contain a gap; review it before
  calling this a native constructive preparation result.
- Inadequate far covariance invalidates local tangents. Single-site tests
  can all vanish while joint far covariance is one; an exact control shows it.
- Small time steps cannot remove a persistent tangent approximation floor.
- The norm bound is not a polynomial-size Pauli decomposition or efficient
  block encoding. No free matrix-to-quantum conversion is granted.
- Additive observable estimation does not imply full classical sampling,
  but this distinction by itself supplies no quantum advantage.
- No filtered-parent gap or new natural hard application was proved.

This is a bounded constructive closure, not the next Shor-level result.
The next high-impact question is whether local tangents admit a paid
compressed representation at degree-scale temperature on large connected
graphs. A new compression proposal needs a norm/error theorem and matched
classical tensor-network/sampling attack, not another full-ball simulation.
