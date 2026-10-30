# Hidden-Mode Access For The Full Native Thermal Purification

Status: conditional constructive derivation and exact finite-instance access
certificates. No quantum circuit has been compiled or executed. No uniform
polynomial scaling, classical hardness, useful-task reduction, novelty, or
quantum advantage is claimed. This new derivation has not had an independent
reasoning review; earlier Rees/exterior reviews do not cover it.

## Scientific Question

Can a free spectrum be turned into preparation of the FULL canonical thermal
purification without assuming an eigenbasis, normalized mode, or reference
ground-state oracle? The preceding line-graph construction does not answer
this for even-hole-free, claw-free (ECF) graphs that are not line graphs.

This note gives an explicit, conditional route through time-filtered Pauli
probes. It exposes both inverse frequency separation and inverse probe
overlap. Thermally negligible modes can be omitted with a state-error bound.
The deliverable is an access reduction, not an unconditional fast algorithm.

## Native Input And Efficient Classical Data

Input consists of m >= 2 ordered vertices, 1 <= R < m, and explicit nonzero
rational couplings |J_i| <= 1. On m physical qubits set

    O_i = X_i product_{max(0,i-R) <= j < i} Z_j,
    H = sum_i J_i O_i,                 Lambda = sum_i |J_i|.

No matrix, phase-state bank, amplitudes, or oracle is supplied. Two terms
anticommute exactly when 0 < |i-j| <= R. The frustration graph is the Rth
power of a path. Each vertex's left neighbors and right neighbors are cliques,
excluding a claw. In any cycle of length at least four, the minimum-index
vertex's two cycle neighbors are adjacent: they both lie within R positions
to its right. A purported induced cycle therefore has a chord. The graph is
connected and ECF. This proof covers arbitrary allowed m and R.

Choose 1 <= ell <= R+1 and the prefix clique K={0,...,ell-1}. Each vertex's
neighbors outside K form a clique, so K is simplicial. The explicit probe

    chi = product_{i in K} Z_i

anticommutes precisely with terms in K. It costs O(ell) elementary Paulis.
Hamiltonian simulation and its controlled/inverse versions are available
from the explicit Pauli list, with their ordinary time/precision costs.

The alternating independence polynomial is computed, not supplied:

    P_0(x)=1,
    P_t(x)=P_{t-1}(x)-J_{t-1}^2 x P_{max(0,t-R-1)}(x).

There are alpha=ceil(m/(R+1)) nonzero modes. The recurrence uses O(m alpha)
rational arithmetic operations; coefficient bit lengths are polynomial in
the explicit input length. Removing K leaves the same recurrence on the
suffix couplings. Exact real-root isolation of Q(y)=y^alpha P_m(1/y), followed
by rational interval arithmetic, certifies energies and weights. The code
fails inconclusively if simple roots, positive residues, or sufficient
precision cannot be certified. A finite bit cap is not a wall-clock cap.

For stable interval evaluation, write B(y)=y^b P_{G\K}(1/y), b=deg P_{G\K}.
At a root of Q, the residue formula simplifies to
w_k^2=y_k^(alpha-b-1) B(y_k)/Q'(y_k). Clique removal implies
alpha-b is zero or one. This cancels potentially enormous reciprocal
powers BEFORE interval evaluation; final weights are rounded outward to
dyadic intervals. No floating point is used in these certificates.

## Literature Premises

[Elman, Chapman and Flammia](https://arxiv.org/html/2012.07857) establish hidden
free-fermion solvability for ECF frustration graphs; their modes need not be
local or linear Jordan-Wigner modes. We use that structure, not an efficiency
claim about the associated change of basis.

[Fukai, Pozsgay and Vona II, Theorem 3.14 and Corollaries 3.15-3.16](https://arxiv.org/html/2605.31453)
give the following probe decomposition. With positive simple roots x_k of P,
epsilon_k=1/sqrt(x_k), and nonzero residual polynomial values,

    [H,Psi_k]=2 epsilon_k Psi_k,       {Psi_k,Psi_l}=delta_{k,-l} I,
    chi=sum_{k>0} w_k(Psi_k+Psi_k^dagger)+w_0 c_0,
    w_k^2=-P_{G\K}(x_k)/(x_k P'_G(x_k)),
    w_0^2=lim_{x->infinity} P_{G\K}(x)/P_G(x),
    sum_k w_k^2+w_0^2=1.

Here c_0 commutes with H and squares to I when present. Signs of w_k can be
absorbed into both Majoranas of the mode. The simple-root and nonzero-residue
conditions are checked, not inferred from a plotted free spectrum. The
general claw-free case with cycle sectors is outside this certificate.

Everything below is a local deduction using these premises and standard
block-encoding methods, not a claim that the cited papers prove our compiler.

## Filtered Access With Normalization Charged

Write c_k=Psi_k+Psi_k^dagger, d_k=-i(Psi_k-Psi_k^dagger),
Z_k=-i c_k d_k, and omega_k=2 epsilon_k. These are Hermitian unitaries with
canonical anticommutation relations, and H=sum_k epsilon_k Z_k. Then

    chi(t)=sum_k w_k[c_k cos(omega_k t)-d_k sin(omega_k t)]+w_0 c_0.

Define the two Hermitian filters

    A_c=(1/T) integral_{-T}^T cos(omega_k t) chi(t) dt,
    A_d=-(1/T) integral_{-T}^T sin(omega_k t) chi(t) dt.

Let Delta_k be a lower bound on the distance from +omega_k to every other
signed frequency and to zero. Including zero when its coefficient vanishes
is conservative. The unwanted-frequency sinc terms give

    ||A_c-w_k c_k||, ||A_d-w_k d_k|| <= 4(alpha+1)/(T Delta_k).

Indeed each nonzero integral of an oscillatory exponential has absolute
value at most 2/(T |frequency|). Summing the cosine/sine cross terms and the
zero component, using |w_j| <= 1, gives the displayed loose bound. Opposite
frequencies are at least omega_k away; the code can therefore use the
minimum of omega_k and the positive-frequency differences.

For M uniform midpoint terms on [-T,T], a derivative bound using
||[H,chi(t)]|| <= 2 Lambda and omega_k <= 2 Lambda gives quadrature error at
most 8 Lambda T/M. Using a midpoint of an energy enclosure of width h gives
an additional conservative bound 4 T h. The symmetric time grid and real
coefficients preserve Hermiticity.

The discrete LCU has normalization AT MOST TWO: its top block is A/2.
One can use a uniform time register, a computable signed coefficient with
absolute value at most one, and controlled exp(+iHt) chi exp(-iHt). No
unknown coefficient distribution or free mode normalization is assumed.
An arbitrary M register or a padded power-of-two register can be prepared
to the required accuracy with explicit arithmetic. A deliberately naive
table implementation is also polynomial in M, not free. M counts terms in
a coherent SELECT construction, NOT M independent laboratory experiments.

For desired clean-mode error delta, the ledger chooses each of the window,
quadrature, and frequency errors <= delta*w_lower/8. Thus total e is at
most 3 delta*w_lower/8. The singular values of A/2 are at least w_lower/4.
The polar factor S=sign(A) obeys

    ||S-c_k|| <= 2e/(|w_k|-e),

with the analogous bound for d_k, after absorbing the common sign into the
mode convention. For delta <= 1/256 this is less than 0.752 delta.

Use [QSVT polar/sign amplification](https://arxiv.org/abs/1806.01838) on A/2
with top-block error eta <= delta^2/512. It costs
O(w_lower^-1 log(1/eta)) block calls. The full clean-ancilla isometry error
relative to S is at most eta+sqrt(2 eta), not merely eta: the square-root
term bounds leakage from the desired ancilla sector. This is less than
0.064 delta. Together with the polar perturbation it is below delta.
The record's `polar_query_scale_not_gate_count=ceil(4/w_lower)` is only an
inverse-gap SCALE; it omits logarithms and is not an actual query/gate bound.

Hamiltonian simulation, coefficient arithmetic, and QSVT phase synthesis
errors must additionally be allocated across the actual circuit calls.
They are not implemented in this bundle. Dense eigendecomposition in
controls.py is solely a bounded validation reference, never compiler input.
Its extra end-to-end control evaluates the finite midpoint sum through a
geometric-series identity, takes a DENSE polar factor, and applies the
doubled rotations. This checks how the proposed steps compose; it does not
compile QSVT. The dense reference always requests 128-bit spectral intervals,
even when the preparation certificate could omit every mode at lower
precision. Numerical identities do not certify arbitrary long-time filters.

## Full Purification Without A Ground State Or Postselection

Let |M> denote vectorization with (A tensor B^T)|M>=|A M B>. Start from
|Omega>=|I>/sqrt(D), D=2^m. Define

    G_k=d_k tensor c_k^T,
    theta_k=atan(tanh(beta epsilon_k/2)),
    U_k=exp(-i theta_k G_k).

Each G_k is a Hermitian involution. Different G_k commute because each of
their two factors anticommutes. For M a product of functions of Z_j with
j != k, M commutes with c_k,d_k, and d_k c_k=-i Z_k. Hence

    U_k |M> = |M(cos(theta_k) I-sin(theta_k) Z_k)>.

The product therefore prepares

    product_k U_k |Omega>
      = |exp(-beta H/2)> / sqrt(Tr exp(-beta H)).

The equality uses tan(theta_k)=tanh(beta epsilon_k/2). CAR gives equally
sized occupation sectors, including the untouched degeneracy space, so
the product normalization is exact. No vacuum is found, and there is no
product of heralding probabilities or supplied partition-function oracle.
Raw Majoranas suffice; extra Jordan-Wigner parity strings are unnecessary
in the doubled generator. A common sign change of c_k,d_k cancels in G_k.

Implement exp(-i theta G) by coherent eigenvalue kickback for a known
Hermitian involution: two controlled G uses and one one-qubit rotation.
Replacing the four constituent controlled Majorana calls by clean-mode
approximations costs at most 4 delta per mode, by telescoping against the
ideal circuit. This does not assume the approximate dilated gate itself
is an involution. Transposition requires transposing elementary gates and
reversing their order in a known circuit; it is not access to an arbitrary
unknown-unitary transpose oracle. Clean input/output ancilla bounds hold
for the transpose as well because the target block is unitary.

For the independent canonical Pauli representation, the usual Bell-basis
and linear/phase cleanup converts this full purification to the native
coefficient pilot. Products O_S have distinct X supports S, so their Bell
labels are injective. The Z support and ordering phase are explicit linear
and quadratic functions of S. This final cleanup needs no eigenvectors.
This is the existing canonical-output interface, not a new decoding claim.

## Temperature-Aware Omission And Total Error

Omitting a mode replaces its rotation by I. More strongly than a linear
telescoping estimate, orthogonality of occupation sectors gives overlap
product_{omitted k} cos(theta_k) with the full state. For every nonempty
set S, Tr(product_{k in S} Z_k)=0: conjugate by c_j for j in S. Expanding
the product of omitted rotations proves the overlap identity, including
all degeneracy sectors. Consequently the squared vector distance is

    2(1-product_{omitted k} cos(theta_k))
        <= sum_{omitted k} theta_k^2
        <= (beta^2/4) sum_{omitted k} epsilon_k^2.

Pure-state trace distance is at most vector distance. The code greedily
omits increasing energies only while the OUTWARD-ROUNDED SQUARE ROOT of
this bound is <= requested_error/8. It also records the weaker linear
bound for comparison; tests include a native case where only the stronger
bound fits the omission budget.
It does NOT remove omitted frequencies from the active filters' gap test.

Set delta=requested_error/(64 alpha). Then 4 alpha delta <= error/16.
The derivative of theta with respect to energy is bounded by beta/2, so
using energy midpoints costs at most beta sum_{active} width/4. The ledger
requires this to be <= error/8. Allocate another error/16 to numerical
thermal-angle evaluation and error/8 to all circuit implementation errors
combined. Including omission, the total is <= error/2, leaving slack.
These are a compiler specification and a written proof, not a verified
gate-level implementation or a machine-checked theorem.

In particular beta=0 needs no mode rotations. A very small positive energy
may be irrelevant at fixed temperature and essential at much larger beta.

## Conditional Cost And Why It May Fail

For active modes, T=O(alpha/(delta w Delta)) and
M=O(Lambda T/(delta w)). QSVT uses O(w^-1 log(1/delta)) SELECT block calls;
each involves Hamiltonian evolution up to time T and explicitly accounted
coefficient/time arithmetic. A conservative direct SELECT implementation
may also pay polynomially in M. Root isolation and coefficient evaluation
are classical preprocessing. Thus the construction is polynomial when the
explicit input length, beta, error^-1, active Delta^-1 and active w^-1 are
polynomially bounded. There is NO proof these promises hold uniformly for
the growing-range family below. Large beta also increases required energy
precision. Constants in these intentionally loose filters are impractical.

Decisive counterexample to free mode access: m=2, R=1, J=(2^-b,1), ell=1.
There is one energy sqrt(1+2^-2b), so its gap from zero is constant, but
w^2=2^-2b/(1+2^-2b). This probe's amplification cost is exponential in b.
The alternative ell=2 has w=1. This defeats this PROBE, not the Hamiltonian
or all possible preparation methods. Tests enforce both sides.

Near-degenerate active modes, tiny residues, and bit-precision exhaustion
must remain explicit blockers. Grouped modes, other probes, Krylov methods,
or different thermal-state preparation may evade this particular cost;
this note is not a lower bound on quantum preparation.

## Matched Classical Baselines And Kill Criteria

- Fixed R is a one-dimensional bounded-range model. Tensor-network thermal
  algorithms and direct range-based contraction are serious baselines, not
  evidence for a major advantage.
- Constant alpha is also low ceiling: at most 2^alpha distinct energies let
  exp(-beta H/2) be represented by a polynomial in H of degree <=2^alpha-1.
  The resulting Pauli expansion has at most m^O(2^alpha) terms. For fixed
  alpha, direct coefficient construction/sampling is a polynomial-size
  alternative, subject to ordinary numerical precision accounting.
- Efficient partition functions or local correlations do not automatically
  give full native coefficient sampling. Conversely, failure of the old
  line-graph or positive-cluster sampler does not prove classical hardness.
- [Szasz-Schagrin et al., Section V](https://arxiv.org/html/2509.22585) give
  efficient classical dynamics of selected observables via transfer-matrix
  tensor contractions. Our full coefficient distribution is a distinct
  output, but this is a required baseline, not an excuse to ignore their
  machinery. [Fukai and Pozsgay](https://arxiv.org/html/2402.02984) already
  construct FFD circuits; a free spectrum alone is not circuit novelty.
- [Fukai, Yoshida and Katsura](https://arxiv.org/html/2603.22163) supply
  solvable dissipative models. Their Hermitian-Pauli jumps are unital, and
  their steady-state spaces can be degenerate. This does not furnish a
  unique finite-temperature canonical purification for our native H.
- The preceding sign-envelope, cluster, flux, and output-pinning notes remain
  relevant. Do not re-label the already dequantized relative-decoding chain
  as a new target. No oracle/query-model separation is being manufactured.

The exploratory family is m=N^2, R=N-1, ell=N, J_i=1, beta=1: both range
and mode count grow. Finite exact certificates are diagnostic only. The
smallest energies and residues already shrink fast; omission might rescue
active costs, but this must be proved, not fitted to a few sizes.

Next decisive work, in order:
1. Prove or refute polynomial ACTIVE separation and overlap after the stated
   error-budgeted truncation, allowing explicit alternative probes.
2. Derive the best classical full-output contraction/sampling bound on this
   same growing-range family, including near-degenerate-mode structure.
3. Only if those survive, implement the block encoding, polar compilation,
   and doubled rotations with a complete native resource ledger.
4. Find a useful native problem/reduction. Preparation alone, even if fast,
   is not a Shor-level algorithm or evidence of one.

Cut this family as an advantage candidate if the matched full-output
sampler is polynomial, if retained access costs are provably exponential
for all justified probes, or if useful-task structure never materializes.
Keep any valid preparation lemma as a reusable tool, not as a promoted
research candidate merely because its finite controls pass.
