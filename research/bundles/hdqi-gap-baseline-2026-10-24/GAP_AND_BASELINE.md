# A Global Mass-Gap Bound And The Spectral-Clipping Comparator

## Research Outcome

There is a direct ALL-ORDERS gap bound for the new filtered parent when
beta^2 times the total squared coupling mass is small. It is not the desired
degree-based theorem. Moreover, a spectral-clipping construction already
gives polynomial pilot preparation in a larger total-mass regime. Thus
proving only the mass bound is not a promising breakthrough claim.

The value of this pass is a real lower bound, a priced competing algorithm,
and a sharper identification of the regime still worth attacking. The
overall research objective is not complete. These local arguments remain
independently unreviewed and have no novelty certification.

## Conventions

Use the explicit canonical independent Pauli generators O_i, coefficient
Hamiltonian H=sum J_i O_i and filtered parent F_beta from
../hdqi-filtered-parent-2026-10-24/FILTERED_PARENT.md. Define

    M=sum_i J_i^2, Lambda=sum_i |J_i|, C=exp(1/8).

H has norm at most Lambda. All its Pauli strings and coefficients are
public. No energy-spectrum oracle, quantum state or Gibbs sample is input.
Bounds below require this independent-label setting, not arbitrary
dependent Pauli Hamiltonians. The tests contain an explicit failure of
the moment premise for ZI+IZ+ZZ.

## Global Gap By Row-Operator Perturbation

Let D_beta map a coefficient vector psi to the tuple of functions
Q_i(s)psi, with the L2 norm weighted by w(s)=2 sech(2pi s). Then

    D_beta^dagger D_beta=F_beta, D_0^dagger D_0=N=sum_i n_i.

The two row maps have the SAME domain and codomain; D_0 is constant in s.
Its smallest singular value is zero, and its next singular value is one.

The public real-time expression for L_i(s) gives

    ||L_i(s)-Z_i|| <= C beta E_V|V+s| ||[H,Z_i]||
                     =2C beta |J_i| E_V|V+s|,

where V is normal of variance 1/4. We used C E exp(iV)=1 to subtract
Z_i and the unitary Duhamel estimate for conjugation. The canonical
commutator [H,Z_i]=2J_i O_i Z_i has norm exactly 2|J_i|.
Since Q_i(s)-n_i is half a difference of two unitary transforms of
L_i(s)-Z_i, it obeys the same bound. Therefore

    ||D_beta-D_0||^2
      <=4 C^2 beta^2 M E_s (E_V|V+s|)^2
      <=4 C^2 beta^2 M E_(s,V)(V+s)^2
      =(5/4) C^2 beta^2 M.

The second inequality is Jensen; Var(s)=1/16 and Var(V)=1/4. Set

    r=(sqrt(5)/2) C beta sqrt(M).

Singular-value perturbation/min-max gives

    gap(F_beta) >= (1-r)^2, provided r<1.

The exact pilot is already a zero vector. The same perturbation bound
shows no second zero vector exists when r<1, independently of the earlier
all-beta uniqueness proof. At r>=1 the lower bound is INCONCLUSIVE: one
must not square a negative 1-r and claim a positive gap.

For example beta^2 M<=1/(5 exp(1/4)) gives gap>=1/4 throughout the path
from zero to beta. Combined with the explicit access and derivative bounds
from the preceding pass, this gives a polynomial preparation construction
in that parameter regime. No quantum circuit has been executed here.

### Components

For a graph split into disconnected components, H and D_G factor across
their coefficient qubits. A filtered Z_i evolves only under its component
Hamiltonian, so F is a tensor sum of component parents. Thus M can be
replaced by the MAXIMUM component mass in the sufficient condition, and
the total gap is the minimum component gap. Reordering vertices is just
the known signed permutation and does not alter this conclusion.

This is still not a local-degree bound for a large connected graph. A
bounded-degree graph may have arbitrarily large component mass.

## A Stronger Direct Quantum Baseline

Spectral filtering and amplitude amplification are standard Gibbs-state
preparation techniques; see [Poulin--Wocjan](https://arxiv.org/abs/0905.2199)
and [Chowdhury--Somma](https://arxiv.org/abs/1603.02940). The concentration
and clipping estimates below are supplied explicitly for the current
canonical input. They are not attributed as a new algorithmic discovery.

### Subgaussian Spectral Measure

Let mu be the spectral measure of H in the vacuum. For every polynomial f,

    <0|f(H)|0>=tr_normalized f(H).

To see this, expand into Pauli words. Any nonempty parity label flips a
nonzero bit mask, giving both zero vacuum diagonal element and zero trace.
A word with zero parity label is a scalar identity and contributes equally.
Finite-dimensional functional calculus extends the equality to functions
of the spectrum, including exponentials and clipped filters.

Every traced word with any generator appearing an odd number of times
vanishes. Bound the remaining signed words by their absolute values and
sum the even multiplicities. For every real t,

    1 <= Z(t)=E_mu exp(tE) <= product_i cosh(t J_i) <= exp(t^2 M/2).

The lower bound follows from the zero mean and Jensen. This is a moment
bound, not an operator-norm bound on H: commuting inputs still have norm
Lambda, potentially much greater than sqrt(M).

### Clipped Filter And Error

For target error epsilon in (0,1), put

    A=log(64/epsilon^2),
    L=beta M + sqrt[M(beta^2 M+2A)].

If the public norm bound Lambda is smaller than L, use L=Lambda instead;
then there is no clipped spectral region. Otherwise define

    g_L(E)=min{1, exp[-beta(E+L)/2]}.

This is bounded by one. For t>=0, exponential Markov and the moment bound
give

    E_mu[exp(-beta E) 1_(E<-L)]
      <=exp[-tL+(beta+t)^2 M/2].

For M>0 and L>=beta M, set t=L/M-beta. The exponent becomes
beta^2 M/2-(L-beta M)^2/(2M), which is at most -A. Thus the weighted bad
tail is at most epsilon^2/64. M=0 means H=0 and the vacuum is exact.

Let u=exp(-beta H/2)|0> and v=exp(beta L/2)g_L(H)|0>. They agree above
the cutoff, and ||u-v||<=epsilon/8. Since ||u||=sqrt(Z(-beta))>=1, their
normalized states have trace distance at most epsilon/4.

The success probability p=||g_L(H)|0>||^2 has the explicit lower bound

    p>=p_0=exp(-beta L)(1-epsilon/8)^2.

Approximate g_L(H) in operator norm to eta=epsilon sqrt(p_0)/8. Normalizing
the approximate successful branch changes its state by at most epsilon/4.
The remaining epsilon/2 is reserved for amplification and implementation
errors. No successful branch may be renormalized while hiding its cost.

### Priced Implementation

Coherent energy estimation under the public Pauli Hamiltonian, a reversible
evaluation of g_L, a controlled amplitude rotation, and uncomputation give
a block encoding of the filter. The function is globally beta/2-Lipschitz
despite the cutoff kink. Energy error O(eta/beta) and failure amplitude
O(eta) therefore suffice; no promise of separated eigenvalues is needed.
Use the known spectral interval [-Lambda,Lambda] to avoid phase aliasing.
Real-time simulation, coherent arithmetic, additional precision bits and
ancillas are all charged. Standard bounded spectral approximation is an
alternative; no discontinuous exact energy projector is required.

Fixed-point or otherwise bounded amplitude amplification uses the explicit
lower bound p_0, the known vacuum preparation and the filter unitary and
its inverse. It does not assume the target state or its reflection.
The amplification scale is O(p_0^(-1/2)), with additional accuracy factors.
Use the dimensionless Hamiltonian beta H if beta is large and the input
couplings small. Even a deliberately conservative implementation polynomial
in m,beta Lambda,1/eta,1/sqrt(p_0) suffices for the following comparison.

Writing c=beta^2 M,

    beta L <= c + sqrt[c(c+2A)] <= 2c+A.

Since Lambda<=sqrt(m M), beta Lambda<=sqrt(m c). Thus all these costs are
polynomial in m,1/epsilon whenever beta^2 M=O(log(m/epsilon)), for
polynomial-bit-length explicit coefficient/temperature data.
In particular beta^2 M=O(log m) suffices for inverse-polynomial accuracy.
The constants in O(log m) must be fixed across an input family. A scalar
ledger for a single large input is not an asymptotic proof or quantum run.

This comparator does not require the filtered-parent gap at all. It also
does not prove a classical hardness result or a quantum advantage for an
operational output. The saved 64-term clipping control is deliberately a
classically easy commuting family with a known binomial spectrum.

## Revised Research Priority

For unit couplings in a large connected graph, M=m. At beta^2(d+1)=kappa,

    beta^2 M=kappa m/(d+1).

If m/(d+1)=O(log m), the direct comparator is already polynomial at fixed
kappa. A new gap theorem limited to such dense graphs would not settle
the remaining algorithmic problem. Componentwise preparations extend the
comparison to separate dense blocks, with accuracy apportioned across
components; replace log m by the total input/precision budget as needed.

The substantive unresolved regime has large connected weighted mass,
growing degree, beta^2(d+1) small, and beta^2 M beyond the logarithmic
comparison regime. Intermediate-degree expanding graphs are natural
stress cases. The mass perturbation bound gives no answer there. Do not
infer slow mixing merely because the bound is inconclusive or because
the direct comparator's cost upper bound is large.

## Other Proof Route Checked

[Cai--Zhan--Zlokapa, arXiv:2610.05953v1](https://arxiv.org/html/2610.05953v1)
proves a high-temperature SYK mixing result using a fermionic Jacobian and
a filtered/unfiltered comparison. Its Majorana anticommutation, even
fermionic Hamiltonian and disorder analysis cannot be silently transferred
to our commuting Z_i coupling operators and arbitrary canonical graph.
Its relative-form strategy is a potential technique, not an imported gap
theorem for this input. No such transfer was proved in this pass.

## Falsifiers And Scope

- The mass proof fails to imply anything positive when r>=1; tests enforce
  an inconclusive result there rather than an invalid squared bound.
- Dependence among the physical Pauli labels invalidates the spectral
  moment premise. Apply this argument to the redundancy-free pilot, not
  automatically to the physical decoded Hamiltonian.
- An undersized clipping threshold can give a wrong output despite a high
  success rate. The negative control measures that failure explicitly.
- Arbitrarily small filter approximation error is not free: eta contains
  sqrt(p_0), and all implementations must retain that dependence.
- The numeric ledgers evaluate analytic bounds in floating point; they
  are not outward-rounded proof certificates at adversarial thresholds.
- No novelty, independent review, formal proof, full degree-gap theorem,
  physical decoder application or operational speedup is established.

Next: attack a genuinely GLOBAL degree/weighted-local bound outside the
direct spectral comparator's regime, or find a full-parent counterexample
there. Do not spend the next pass demonstrating the easy dense cases.
