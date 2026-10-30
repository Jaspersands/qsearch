# A Priced, Bounded Parent For The HDQI Pilot

## Decision And Prior Art

The previous pass left TWO independent blockers for its flattened
coefficient parent: a global gap and an efficient implementation. This pass
replaces that parent. The construction below has a unique desired kernel,
bounded real-time-filter access and polynomial path-derivative bounds. Its
uniform gap remains open. It is not a polynomial preparation theorem.

This is an adaptation of known Gibbs-parent machinery, NOT a claim to have
invented filtered thermal constraints. [Leng, Jiang and Lin,
arXiv:2604.22996v1](https://arxiv.org/html/2604.22996v1), equations 7-11,
factor KMS parents into filtered left/right differences. Their preparation
result still requires a gap and warm-start access. We specialize the
factors to the coefficient algebra and supply public real-time access; an
adiabatic path from the vacuum avoids *assuming* a warm start, conditional
on that path's gap. No published gap guarantee is imported here.

The motivation is the small-beta^2 d pilot question in
[Hastings--Schmidhuber, arXiv:2610.03697v1](https://arxiv.org/html/2610.03697v1).
The existing predecessor-uniform route was checked in the repository and
already has a classical energy baseline. We do not revive it as a speedup.

## Public Input And Target

Use the same explicit graph G, real rational |J_i|<=1 and m coefficient
qubits as in the preceding bundle. Set

    O_i = X_i product_{j<i,j~i} Z_j, H = sum_i J_i O_i,
    S = exp(-beta H/2), |pi_beta> = S|0>/||S|0>||,
    n_i=(I-Z_i)/2, N=sum_i n_i, Lambda=sum_i |J_i| <= m.

H is a public list of at most m Pauli strings, each with at most m factors.
No spectral decomposition, imaginary-time evolution, thermal state or
matrix-inverse oracle is supplied to the quantum construction. All such
operations in the executable are explicitly CLASSICAL DENSE REFERENCES.

Let A be the operator algebra spanned by the 2^m ordered words
P(y)=O_1^y1 ... O_m^ym. They are orthonormal in normalized Hilbert-Schmidt
inner product and P(y)|0>=|y>. This identifies an m-qubit coefficient
state with an operator T in A. The coefficient state of S is the target.

Define the public diagonal Clifford

    D_G |y> = (-1)^{sum_{i<j,i~j} y_i y_j} |y>.

For T in A, right multiplication has coefficient representation
D_G T^T D_G: transposition reverses a word and D_G converts each left
generator to its right-regular counterpart. Left multiplication is T.

## Filter And Coefficient Constraint

For real s, define an operator L_i(s) by its energy-basis expression
(used ONLY to state the math and for small reference checks):

    L_i(s)_{ab} = exp[-(beta omega_ab)^2/8 - beta omega_ab/4]
                  exp[i beta s omega_ab] (Z_i)_{ab},
    omega_ab = E_a-E_b.

Write R_i(s)=L_i(s)^dagger. The filter obeys thermal balance, giving

    L_i(s) S = S R_i(s).

The operator-space constraint is (L_i(s) T - T R_i(s))/2. Factoring out
left multiplication by Z_i maps its output back into A, without changing
its Hilbert-Schmidt norm. Its coefficient-qubit implementation is

    Q_i(s) = [Z_i L_i(s) - D_G overline{L_i(s)} D_G]/2.

The bar means entrywise conjugation in the canonical computational basis,
not an unphysical conjugation of an unknown input state. H,Z_i,D_G are real
and public: conjugate the known circuit's phases and real-time direction.
The independent word-by-word tests verify this transpose/conjugation rule.

Define the new parent

    F_beta = sum_i integral_{R} w(s) Q_i(s)^dagger Q_i(s) ds,
    w(s)=2 sech(2 pi s), integral w=1.

It is positive and annihilates the desired pilot. At beta=0, Q_i=n_i,
so F_0=N, with known vacuum ground state and gap 1.

## Unique Kernel: A Local Proof, Review Pending

Positivity and the strictly positive time density imply that a zero vector
of F is annihilated by every Q_i(s): zero integral first gives almost-everywhere
zero; continuity then gives every real s.

Let B_i=exp[-beta^2 ad_H^2/8](Z_i), which is Hermitian, and
B_i(s)=exp(i beta s H) B_i exp(-i beta s H). Then

    L_i(s)=S^(1/2) B_i(s) S^(-1/2),
    R_i(s)=S^(-1/2) B_i(s) S^(1/2).

For a coefficient operator T in A, set X=S^(-1/2) T S^(-1/2), still in A.
The common-kernel equations are exactly [B_i(s),X]=0 for every i,s.
For beta>0, separate the finitely many distinct Bohr frequencies in this
analytic identity. Each component has the strictly nonzero scalar
exp[-beta^2 omega^2/8], so X commutes with every frequency component of Z_i
and hence with Z_i itself. This is an IDENTIFIABILITY proof, not an
instruction to resolve energy gaps or invert exponentially small filters.
At beta=0, B_i=Z_i and the same conclusion is immediate.

Commutation with every Z_i makes X diagonal. The only diagonal element of
A is a scalar identity: different nonzero words flip different nonzero
bit strings, and X|0> has precisely their coefficients. Thus X=cI, T=cS.
The kernel is exactly one-dimensional for every finite beta.

The infinite-time uniqueness argument gives no quantitative gap. Finite
quadrature can acquire approximate extra kernels; its error must be chosen
relative to a separately established gap. Tiny filtered frequencies are
not assumed measurable or recoverable at unit cost.

## Real-Time Access With Constant Normalization

Let V be a centered normal variable of variance 1/4, with density
p(v)=sqrt(2/pi) exp(-2v^2), and C=exp(1/8). Its characteristic function gives

    exp[-u^2/8-u/4] = C E_V exp[i V(1+u)].

Consequently

    L_i(s) = C E_V exp(iV)
             exp[i beta(V+s)H] Z_i exp[-i beta(V+s)H].

Every term on the right is a phase times a unitary. It follows that

    ||L_i(s)|| <= C, ||Q_i(s)|| <= C,
    ||F_beta|| <= m C^2 = m exp(1/4).

An LCU block encoding of Q_i has normalization C, independent of graph
degree, inverse temperature, dimension and tiny Bohr frequencies. Selecting
i and the time-bin labels gives a parent block encoding with normalization
at most m C^2. This replaces the previous exponential star normalization.
It does not simulate the old raw parent or its flattened projectors.

All gates are public Pauli products, D_G (one CZ per edge), controlled
real-time simulation of the explicit Pauli sum H, and computable scalar
weights/phases. A generic O(number of bins)-gate weight loader suffices;
there is no QRAM or state-loading oracle assumption. Gate counts for H
simulation depend polynomially on Lambda, time, m and target accuracy.
No optimized fault-tolerant circuit or hardware run is claimed.

## Explicit Quadrature And Its Error Budget

Let delta in (0,1) be an OPERATOR-norm parent approximation budget. Set

    S_cut = log[16m C^2/(pi delta)]/(2pi),
    h_s <= delta/(8m beta Lambda C^2),
    eta = delta/(4m C),
    V_cut = sqrt(log(2C/eta)/2),
    h_v <= eta/[C(1+2 beta Lambda)].

Use symmetric midpoint bins with their exact probability masses, without
renormalizing missing tails. For Lambda=0 the outer integrand is constant,
so one bin suffices; beta=0 is implemented exactly as N.

- The outer omitted mass is at most (4/pi)exp(-2pi S_cut), contributing
  at most delta/4 to the parent norm error.
- ||d_s(Q_i^dagger Q_i)|| <= 4 beta Lambda C^2. Exact bin masses therefore
  give outer midpoint error <=2m beta Lambda C^2 h_s <=delta/4.
- The Gaussian omitted mass is <=exp(-2V_cut^2). The inner integrand has
  derivative norm <=1+2 beta Lambda, including its exp(iv) phase. Thus
  each L_i approximation has error <=eta. Its norm is still <=C because
  positive bin masses sum to at most one. Each Q changes by <=eta, so
  the total quadratic-parent error is <=2mC eta=delta/2.

The total analytic quadrature error is <=delta. The largest real time is
beta(S_cut+V_cut), and both bin counts are polynomial in m,beta,1/delta.
Weight/phase arithmetic and Hamiltonian-simulation errors are SEPARATE
budgets, not included in delta. Allocate, for example, half of an overall
error tolerance to this quadrature and half to those implementation errors.
During a preparation of duration T, choose total simulator error consistent
with the final state error, not a fixed constant tolerance.

The executable resource ledger does not execute those quantum operations.
A small discrete reference checks the stated norm-error inequality. Large
ledgers are not automatically launched as dense experiments.

## Polynomial Path Derivatives, Not A Warm-Start Assumption

The same integral representation bounds first and second beta derivatives.
For a unitary-conjugation term at time beta(v+s), the derivative bounds are
2|v+s|Lambda and 4(v+s)^2 Lambda^2. The outer density has mean zero and
variance 1/16; V has variance 1/4. Cauchy-Schwarz therefore yields

    ||d_beta F_beta|| <= sqrt(5) m C^2 Lambda,
    ||d_beta^2 F_beta|| <= 5 m C^2 Lambda^2.

For the path u -> F_(u beta_target), multiply these by beta_target and
beta_target^2. Thus the path is polynomially priced and smooth. IF its
minimum gap is inverse-polynomial, standard adiabatic preparation starting
at |0> is polynomial (including accuracy and simulator error). A supplied
warm state, the unknown pilot, or the unknown ground projector is not an
input to that conditional algorithm.

The sole state-preparation theorem still missing is the minimum-gap bound
on the ENTIRE path. Uniqueness at each finite beta does not supply it.

## Second-Order Compatibility With The Desired Scale

Let H_R=D_G H D_G, K_L=sum_i J_i O_i Z_i and K_R=D_G K_L D_G. The beta
coefficient of F is (H+H_R)/4. The public anti-Hermitian generator
G=(K_L+K_R)/4 satisfies [G,N]=-(H+H_R)/4, cancelling this term under
the rotation exp(beta G).

For a checkable Taylor derivation, put C_i=[H,Z_i], D_i=[H,C_i]. Write

    Q_i(s)=n_i + beta(a_i + i s b_i) + beta^2 c_i(s) + O(beta^3),
    a_i=(-Z_i C_i + D_G C_i D_G)/8,
    b_i=( Z_i C_i + D_G C_i D_G)/2,
    E_s c_i(s)=-(Z_i D_i - D_G D_i D_G)/16.

The unrotated second coefficient is

    A_2=sum_i [n_i E c_i + (E c_i)^dagger n_i
               + a_i^dagger a_i + b_i^dagger b_i/16].

After conjugation it is B=A_2+[G,(H+H_R)/4]/2. Applying these expressions
to the one-excitation basis gives

    (P_1 B P_1)_ii = -J_i^2/2 + (1/4)sum_{j~i} J_j^2,
    (P_1 B P_1)_ij = -3 J_i J_j/4 for an edge, zero otherwise.

For unit d-regular graphs the least eigenvalue is -(d+1)/2, since the
adjacency matrix's largest eigenvalue is d. The finite-graph gap thus has
leading correction -(d+1) beta^2/2. Global parity removes the cubic
compression to P_1, as in the previous bundle. These are fixed-graph
Taylor statements: the higher-order constant is not uniform in m,d.
They do NOT establish a beta^2 d gap theorem.

## What Was Improved And What Would Kill It

Established locally, with written proofs and finite controls but no
independent review: exact one-dimensional kernel, bounded and explicit
real-time access, analytic quadrature error, derivative bounds, and the
displayed low-order compression. Standard filtered-parent machinery is
credited above; no new-algorithm or novelty certification is made.

Highest-impact remaining question:

    Do constants kappa_0,gamma>0 exist such that F_beta^2>=gamma F_beta
    for every explicit graph and |J_i|<=1 with beta^2(d+1)<=kappa_0?

An explicit inverse-polynomial bound would also suffice for preparation.
A family with a superpolynomially closing GLOBAL gap at arbitrarily small
fixed kappa would falsify this uniform algorithmic route. The previous
two-term star obstruction is not a statement about this new parent or its
global gap. Rare sectors, high excitation numbers and small spectral filter
weights remain strong adversarial targets.

The +1 temperature guard is essential if edgeless graphs are included.
For a single commuting term JX the exact parent gap is

    exp[-(beta J)^2] cosh(beta J).

It becomes arbitrarily small although beta^2 d=0 at every temperature.
The one-qubit factor is obtained by summing Q^dagger Q in the X eigenbasis;
its two rows differ only by time phases, so the time integral changes
nothing. A commuting m-term graph is a tensor sum of these one-qubit
parents. Its target state remains an explicitly preparable product state,
so this is a flaw in a temperature-unrestricted parent-gap claim, not a
hardness result. For d>=1, replacing d with d+1 changes only constants in
the requested square-root-degree regime. An algorithm can also directly
prepare all commuting components instead of using this parent there.

The construction may be completely known as a specialization of DLL/KMS
parents; that does not supply the missing redundancy-free gap theorem.
Do not count this access repair itself as an algorithmic breakthrough.

Even a successful preparation theorem would still need a useful physical
HDQI target with a priced reversible decoder and its actual error law,
or an operational sampling/observable task. Classical partition-function
tractability is already known in the regime. Commuting, predecessor-uniform,
low-rank/symmetric and low-width graphs require their strongest classical
baselines. An ability to emit a quantum state is not, alone, a separation
for a classical output problem.

Next work should attack the GLOBAL gap with the access assumptions now
explicit, not build a general registry, polish a UI or fit small spectra.

Numerical caution: the dense spectral reference can leak roundoff into an
exactly zero Bohr component. When the true filter suppresses the active
components below that leakage, a tiny computed gap is unreliable even
relatively. The one-qubit beta=10 test exercises this regime using an
independent exact two-frequency representation. Receipt gaps below 1e-11
are marked unresolved diagnostics; the threshold is not a rigorous error
interval. The new gap theorem is not inferred from any floating-point row.
