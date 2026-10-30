# Coefficient-Space HDQI Parent: A Precise Target, Not An Algorithm

## Research Decision

The source-construction branch has repeatedly reached conditional arithmetic
reductions rather than a natural executable source. This pass opens an
independent constructive question: can one prepare the noncommuting HDQI pilot
in polynomial time when kappa = beta^2 d is a sufficiently small constant?

Hastings and Schmidhuber, [arXiv:2610.03697v1, Sections II, VI, VII](https://arxiv.org/html/2610.03697v1),
give the pilot/TFD equivalence and a subexponential preparation algorithm in
this regime. Polynomial preparation remains open there; their physical-site
Feiguin-Klich gap theorem applies at beta d small. The partition function is
already classically tractable at small kappa. Solving preparation would not
by itself establish a quantum advantage for a classical output problem.

The proposed parent below is on COEFFICIENT qubits. Do not identify its gap
with the paper's physical-site parent gap. No novelty claim is certified.

## Input And Output

Input: an explicit simple graph G on m ordered vertices, real rational
couplings |J_i| <= 1, beta >= 0, and target trace-distance error epsilon.
Its maximum degree is d. Adjacency, Pauli strings and couplings are public;
there is no thermal-state oracle or uncharged spectral projector.

Define, on m label qubits,

    O_i = X_i product_{j<i, j~i} Z_j
    H = sum_i J_i O_i
    n_i = (I-Z_i)/2,  N = sum_i n_i
    t = beta/2,  S = exp(-t H).

Desired output is |pi_beta> = S|0^m>/||S|0^m>||, as a quantum state.
Ordered words O_1^y1 ... O_m^ym applied to |0> give |y>. Left multiplication
on these words has precisely the canonical O_i action. Consequently the
coefficients of exp(-beta H/2) in the normalized-trace orthonormal word basis
are S|0>. The known Clifford conversion gives the redundancy-free TFD.

This is an explicit finite-description Hamiltonian problem, not a planted
oracle separation. Classical simulators must receive the same graph and
couplings, not a more restricted access model.

## Exact Parent And Kernel

Set q_i = S n_i S^{-1} and F = sum_i q_i^dagger q_i. Similarity makes the
q_i commuting idempotents. Positivity gives

    ker(F) = intersection_i ker(q_i) = span{S|0>}.

There is a unique ground state for every finite beta. This elementary kernel
identity gives NO lower bound on the gap or upper bound on implementation
cost. Forming S or its inverse as a dense matrix is exponential work.

## Public Rotation And The Second-Order Lemma

Let K = sum_i J_i O_i Z_i, so K^dagger = -K and [K,N] = -H. The public
unitary R = exp(t K) can be synthesized using ordinary Pauli Hamiltonian
simulation of iK with polynomial norm sum, precision and string lengths.
It cancels the linear term of the parent:

    R F R^dagger = N + beta^2 B_raw + O_G(beta^3),

    B_raw = sum_i J_i^2 n_i
            - (1/2) sum_{i<j, i~j} J_i J_j O_j O_i (Z_i-Z_j).

The remainder is for a FIXED finite graph. Its constant has not been bounded
uniformly in m or d. This distinction is essential.

Proof: put C_i=[H,n_i] = -J_i O_i Z_i and D_i=[H,C_i]. Expansion gives

    q_i = n_i - t C_i + t^2 D_i/2 + O(t^3)
    q_i^dagger q_i = n_i + t[C_i,n_i]
                    + t^2({D_i,n_i}/2 - C_i^2) + O(t^3).

Summing the first-order coefficient gives H. Conjugating by exp(tK) cancels
it since [K,N]=-H. The t^2 coefficient after conjugation is

    sum_i ({D_i,n_i}/2 - C_i^2) + [K,H]/2 = 4 B_raw.

Direct Pauli multiplication gives the displayed edge formula. Every edge
term conserves N. In the single-excitation basis |i>, the compression is

    P_1 B_raw P_1 = diag(J_i^2) + diag(J) A_G diag(J).

For each fixed occupation of the other qubits, an edge acts on its
one-excitation subspace by a signed off-diagonal entry J_i J_j. The diagonal
matrix diag(J_i^2,J_j^2) plus that edge matrix is positive semidefinite
(nonnegative diagonal and determinant zero). Hence, for d>=1,

    B_raw >= sum_i (1-deg(i)) J_i^2 n_i >= -(d-1) N.

For d=0, B_raw>=0. Unit-coupling d-regular bipartite graphs attain
lambda_min(P_1 B_raw P_1)=1-d. Their finite-graph gap is therefore

    Delta_raw(beta) = 1 - (d-1) beta^2 + O_G(beta^4).

Why the fourth-order remainder for this gap despite cubic operator terms:
global Z parity changes the signs of H and K. The cubic rotated coefficient
changes excitation parity, so it has zero compression to P_1. There is no
first-order rotated term to mix P_1 with other excitation sectors. Ordinary
finite-dimensional degenerate perturbation theory then gives the statement.
Neither parity nor the edge calculation bounds higher orders uniformly.

## Exact Cost Falsifier: Raw Star Parent

For a star with hub 0 and d leaves,

    H = X_0 + Z_0 sum_{j=1}^d X_j.

Fix the leaf X eigenvalues, whose sum is a. On the hub H_a=X+aZ, with
r=sqrt(1+a^2). The hub q_0 is rank one and

    ||q_0^dagger q_0|| = <1|exp(-beta H_a)|1>
                         <1|exp(beta H_a)|1>
                       = 1 + sinh^2(beta r)/r^2.

sinh(beta r)/r is increasing for r>0 and beta>=0. Maximizing over leaf
sectors gives the EXACT full-space term norm

    ||h_0|| = 1 + sinh^2(beta sqrt(1+d^2))/(1+d^2).

At beta=c/sqrt(d) for fixed c>0,

    log ||h_0|| = 2c sqrt(d) - 2 log d - log 4 + o(1).

Thus a constant gap alone cannot make a standard norm-priced LCU/QSVT
simulation of this RAW parent polynomial in m=d+1. A block encoding must
normalize by at least the operator norm. The public unitary R does not
change it. The receipt evaluates this formula at large d WITHOUT matrices.

This is not a simulation lower bound against special fast-forwarding or
all state preparation algorithms. The star has collective symmetry and
is an intentionally EASY classical control. It refutes a proposed free
implementation step, not classical tractability or the gap conjecture.

## Bounded Projectors: Candidate Repair With Its Own Debt

Replace each raw term by the orthogonal projector pi_i onto range(q_i^dagger).
It has norm 1 and the same kernel. Let E_i=I-n_i. One exact formula is

    pi_i = I - S E_i (E_i S^2 E_i)^{-1}_{range E_i} E_i S.

In the dense controls a QR decomposition of S restricted to range(E_i)
computes the complementary subspace. This is NOT efficient quantum access.
The inverse above can be ill-conditioned; replacing it with an oracle is
not permitted. Spectral flattening of a huge-norm block encoding does not
automatically remove its normalization cost.

Set F_flat=sum_i pi_i. It is positive, has the same unique ground state,
and ||F_flat||<=m. Its second-order expansion after the same rotation is

    R F_flat R^dagger = N + beta^2 B_flat + O_G(beta^3)
    B_flat = B_raw - sum_i J_i^2 n_i.

To see the subtraction, h_i=q_i^dagger q_i obeys
h_i^2-h_i = 4t^2 J_i^2 n_i + O(t^3). Its nonzero eigenvalues are therefore
1+4t^2 J_i^2+O(t^3); flattening removes that t^2 multiple of n_i. Equivalently
one may Taylor expand the complementary-subspace projector formula.
The independent QR controls check this expansion.

Consequently B_flat>=-dN and

    P_1 B_flat P_1 = diag(J) A_G diag(J).

For unit d-regular bipartite graphs, Delta_flat=1-d beta^2+O_G(beta^4).
Bounded norm does NOT supply a uniform gap or an efficient circuit.

For completeness, every idempotent q has nonzero singular values at least
one: in an orthogonal decomposition by range(q), it has block form
[[I,A],[0,0]], and q q^dagger has nonzero block I+A A^dagger. Hence
h_i>=pi_i and F>=F_flat. A lower gap bound for the flat parent transfers
to the raw one; the reverse implication loses up to the maximum term norm,
which the star shows can be superpolynomial. The tests check this ordering.

## Second Falsifier: A Pairwise Gap Collapses After Flattening

The most immediate possible all-orders argument would prove that every pair
pi_i+pi_j has a uniformly separated nonzero spectrum. This is FALSE at the
square-root scale, including for the bounded projectors.

On the star, retain hub 0 and leaf 1 and fix all other leaf X eigenvalues
to +1. This is an invariant sector of pi_0 AND pi_1 because both commute
with those other X operators. It is NOT an invariant restriction of the
sum including all the other leaf projectors. Put a=d-1. The restricted
Hamiltonian is H_a=X_0+Z_0(X_1+a). In the X_1=+/- basis set

    b_+=a+1, b_-=a-1, r_+=sqrt(1+b_+^2), r_-=sqrt(1+b_-^2)
    S_+=exp[-beta (X+b_+ Z)/2], S_-=exp[-beta (X+b_- Z)/2]
    V_+=cosh(beta r_+) - (b_+/r_+) sinh(beta r_+)
    V_-=cosh(beta r_-) - (b_-/r_-) sinh(beta r_-)
    D=2+2[cosh(beta r_+)cosh(beta r_-)
          - a^2/(r_+r_-) sinh(beta r_+)sinh(beta r_-)].

The two kernels are planes

    A=span{(S_+|0>,0), (0,S_-|0>)}
    B={(S_+ u,S_- u): u in C^2}.

They intersect in dimension one. If theta is their other principal angle,

    sin^2(theta)=(V_+ + V_-)^2/(V_+ V_- D),
    gap_pair=1-cos(theta).

Proof of the angle identity: write v_s=S_s|0>, w_s=S_s|1>. A basis of B is
(v_+,v_-) and (w_+,w_-). Remove the latter's component parallel to the former.
Its squared norm becomes D/(V_+ + V_-), where
D=det(S_+^2+S_-^2). Its squared component orthogonal to A is
1/V_+ + 1/V_- because det(S_s)=1. Their ratio gives sin^2(theta).
The standard two-plane decomposition of the sum of complementary projectors
has eigenvalues 0, 1-cos(theta), 1+cos(theta), 2. This can also be verified
directly in the resulting four-dimensional basis.

At beta=c/sqrt(d), fixed c>0 and d tending to infinity,

    V_s ~ exp(beta r_s)/(4 b_s^2),
    1 - a^2/(r_+r_-) = 4/[(r_+r_-)(r_+r_-+a^2)] ~ 2/a^4,
    D ~ exp(2 beta a)/a^4,
    gap_pair ~ 2 a^4 exp(-2 beta a).

Thus the pair gap closes superpolynomially even at arbitrarily small fixed
kappa=c^2. The stable analytic log formula avoids diagonalizing an
ill-conditioned imaginary-time matrix. Tests compare it with independent
QR projectors and with an actual invariant block of a full small star.

This kills a UNIFORM PAIR-GAP proof strategy, not the full-parent gap
conjecture. The rare environment sector can have large energy under the
OTHER leaf terms, which were excluded from the pair sum. A useful proof
must exploit global constraints or a state-weighted estimate, not promote
a ground-state average to a worst-sector operator inequality.

## Next Decisive Theorem And Falsifiers

Target A: constants kappa_0,gamma>0 independent of m,d such that
F_flat^2 >= gamma F_flat whenever beta^2 d<=kappa_0. Alternatively, an
inverse-polynomial gap with a fully explicit parameter dependence suffices.
Graph sequences with a closing gap at arbitrarily small fixed kappa would
falsify the constant-gap target. A finite spectrum cannot establish it.
The pair-gap counterexample above requires a genuinely global proof.

The tempting inequality R F_flat R^dagger >= (1-C kappa)N is generally
WRONG as an all-orders target: R does not rotate the exact ground state
to |0> beyond low order. A correct proof must account for the moving
ground space or use the frustration-free squared-Hamiltonian criterion.

Target B: construct all required parent evolutions/projectors in
poly(m,1/epsilon) gates from G,J,beta, with explicit approximation and
derivative bounds along an adiabatic path. Target A does not imply B.
Alternatively construct a different bounded parent with the same output.

Conditional algorithm: start at |0>, follow a suitably priced gapped
parent path, undo R if using the rotated path, then apply the known
coefficient-to-TFD conversion. Adiabatic runtime must charge path length,
derivatives, precision, gap and simulation costs. None is waived here.

Target C: exhibit a noncommuting physical Hamiltonian and efficiently
reversible decoder whose verified average error is small under the TRUE
pilot distribution, with a useful output and a matched classical baseline.
Arbitrary-sign decoding robustness must not be inferred from a theorem
that requires random signs. Decoding and readout remain separate work.

Classical checks: exact Pauli symplectic reductions; commuting, clique,
star and bounded-width solvable families; tensor-network contraction with
actual bond/width costs; classical cluster expansions for the requested
observable; ordinary thermal sampling for any eventual classical output.
The present small dense computations are themselves classical controls.

## Assessment After Attempting To Kill The Proposal

- Kept: the public rotation and second-order graph identity are explicit,
  inexpensive to describe, and make square-root-degree scaling plausible.
- Rejected: raw-parent gap plus generic norm-priced simulation as a complete
  route. The star formula exposes a superpolynomial normalization factor.
- Rejected: uniformly gapped pairs of flattened projectors at fixed small
  beta^2 d. The explicit star sector violates this necessary premise of that
  proof strategy; it does not violate the global gap target.
- Unresolved: bounded-projector implementation and a uniform spectral gap.
  Operator-norm cluster expansions may still revert to beta d, not beta^2 d.
- Unresolved: an output task where this is more than improved preparation of
  a classically manageable observable. Do not count the partition function.
- No novelty assessment or independent review of these new lemmas has been
  completed. The separate Rees review does not cover this direction.

Priority: prove or falsify one of Targets A/B before building a workbench,
adding registry candidates, running large generic sweeps or polishing UI.

Vertex ordering is not an optimization variable here. Reordering the
canonical generators is conjugation by a public signed permutation on
coefficient labels: a qubit permutation and controlled-Z signs for the
edges whose order is reversed. This preserves n_i up to relabeling, hence
preserves both parent spectra. A separate test checks the full conjugacy.
