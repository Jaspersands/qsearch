# Evenly spaced Richardson-Gaudin candidate

Native input: even N, an N-bit initial occupation label b with N/2 ones,
parameter t in [0,1] given rationally as an endpoint, and trace-distance tolerance
eta. Set eps_i=i/N and physical g=t/N (i=1,...,N). On N qubits define
 Q_i(t)=n_i+(t/2) sum_{j!=i}(SWAP_ij-I)/(i-j), n_i=(I+Z_i)/2.
These mutually commute, preserve M=sum n_i, and sum Q_i=M. Track the joint
branch from product b at t=0, no intermediate eigenvalues/roots/eigenstate advice.
The concrete target is EVERY branch, not just a typical root or ground state.

Decisive question: are there absolute c>0,C finite such that for ALL even N,
ALL t in [0,1] and every pair of distinct SAME-sector joint branches,
 sum_i (q_i(t)-q'_i(t))^2 >= c*N^(-C)?
A proof closes the remaining gate in the written no-eigenvalue-advice joint-charge
random-dephasing traversal (included note), in poly(N,1/eta) gates. All Pauli
norms/derivatives are polynomial (individual O(log N), total O(N log N)).
Existing cluster counterfamily uses nonuniform sites and does NOT apply here.
No universal1/N constant is required. Refuting 1/N alone does not refute the target.

Strongest baseline obligations: classical eigenvalue-based quadratic Bethe ODE/
Newton tracking; exact diagonalization in dimension binomial(N,N/2); tensor
networks with proved bond-dimension cost; computational-basis sampling via paid
prefix norms. Classical root tracking alone is not an output quantum state and
is not an exact probability sampler without a separate readout construction.
No separation or novelty claim. Finite success/small Smale bound are not proof.
Quadratic equations are q_i^2-q_i+(t/2)*sum_j(q_i-q_j)/(i-j)=0, sum q_i=N/2.
Their real-root completeness/simplicity must be cited or checked under actual
Hermitian charge hypotheses, not assumed for arbitrary polynomial roots.

Prior work: actual source v3 leaves finite-g same-sector gap and classical
tracking unproved. General squared1/N is refuted by the repo's two-cluster
family; M=1 is already classically matched. Plain weak perturbation g<<spacing/N²
and g=infinity limits cannot close this fixed finite interaction path. No quantum
implementation is authorized before the exact classical/proof attacks.
