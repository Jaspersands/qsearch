# Post-conductivity selection: direct local divisor arithmetic

Selection for the 2026-11-12 dispatch, completed 2026-11-13 local time.
Current STATE/TRAPS/GOAL and the matching latest handoff title were checked.
Local corpus queries preceded the retained primary-source reads. No network,
API, Git, archive reading, numerical sweep, or new implementation.

**Top pick: construct the local Kummer HALF operation by one fraction-free
Riemann--Roch computation on the explicit signed divisor, with a uniform
coordinate reset proved on the existing sigma perturbations.** This is a
specific operation to attack, not a renewed request for unspecified stable
halving. It could complete the already bounded saturation algorithm for the
complete native dyadic local image. Its first decisive gate is below.

The other two candidates have different operations: a Gaudin
counterdiabatic generator obtained from exact Pauli equations, and a
small-cyclotomic specialization algorithm for full sparse function-field
relations. The last is absent from the front STATE. Neither repeats a
conductivity, coset, or phase-source barrier. The parent retains the final
research-priority decision.

## 1. Selected: fraction-free local HALF from signed divisors

**Native input/output and value.** A monic squarefree integer polynomial
`f`, degree `2g+1`, coefficient bit size `B`, defines `y^2=f(x)`. At the
hard dyadic prime, output the complete image of `J(Q_2)/2J(Q_2)` in the
explicit finite local squareclass coordinates, with bounded error `eta`.
Target: polynomial BIT cost in `g,B,log(1/eta)`. No Neron model, local
generators, exact p-adic zero oracle, splitting field, or conditioning
bound is input. The complete local image is itself useful descent data.
A general Selmer-dimension composition also needs the other local primes
and the retained global arithmetic; a dyadic proof alone must not silently
claim those additional interfaces.

**Paid structure.** The existing notes prove a polynomial number `kappa`
of saturation steps, exact finite-quotient bookkeeping modulo the fixed
error subgroup `E=2L`, and an explicit subgroup `U subset E` parametrized
by actual points

    sigma(z)=sum_i(P(t_i+2^R z_i)-P(t_i)).

The parameters, root residues, series accuracy, finite-grid distribution,
and signed divisor of length `2g` are paid. Replacing `h` by
`h+2 sigma(z)` preserves its required coset, and moves every half by
`sigma(z)`. Stoll Proposition 5.1 provides an exact-field half from a
square root of the Kummer representative, using degree-`O(g)` congruences.
The existing branch-resultant repair and the exact bounded-kernel shape
are useful later stages. None currently bounds all needed finite-precision
losses or constructs the reduced pair from the signed expression.

**The new operation.** Keep the current class as a closed divisor, without
splitting its support. Add the `O(g)` explicit signed perturbation terms.
For a degree-zero signed divisor `D_+-D_-`, clear poles with its known
`x`-denominator and compute `L(g infinity-D_++D_-)` directly. The numerator
lies in an `O(g)`-dimensional known hyperelliptic RR space, with basis
`x^j` and `x^j y`; vanishing is imposed in the closed support algebras,
including the necessary jet constraints. Thus the exact-field problem is
one polynomial-size interpolation matrix, rather than a long chain of
reduced additions. A kernel section determines the effective opposite
representative; hyperelliptic conjugation gives the requested sign.

Use fraction-free elimination and determinants to express the output
Mumford coefficients as ratios of maximal minors. A successful generic
chart has a visible maximal-rank minor and a visible monic-normalization
minor. These certify the expected rank instead of asking whether an
unknown p-adic number is exactly zero. A small minor is a failure of that
sample/chart, not an instruction to increase precision indefinitely.
All multiplicities, intersections and infinity/pole cases must remain in
the closed-divisor constraints; pairwise support separation is not advice.

**Exact first proof question.** Prove a computable polynomial precision
cap and a polynomially samplable finite grid such that, uniformly over
EVERY permitted saturation state, random `z` produces a certified RR
chart and reduced pair with constant success probability and

    coefficient valuations >= -P(g,B,v_2(disc f),R).

An explicit additive-loss bound over the entire `kappa`-step loop also
suffices. Merely proving `S_next <= poly(S_previous)` does not suffice:
polynomially many iterations of `S -> S^2` may need exponential precision.
The grid may have exponentially many points but must be sampled with
polynomially many trials, never enumerated.

A concrete route to this lemma is to normalize the input RR/Plucker data
primitively, express the chart minors on the explicit sigma family, and
prove a polynomial bound on a nonzero low-order coefficient plus a
finite-grid sublevel estimate and a certified analytic tail. Primitive
normalization may remove dependence on the absolute scale of the incoming
coordinates; it does NOT by itself prove the required low-order bound.
This is the mathematical content the next request should attack.

**Completion ledger and cheapest falsifier.** With the RR cap, apply the
existing bounded branch-resultant repair, local square roots, and Stoll
congruences. Still pay the nonzero Smith valuations of the Stoll matrix
and its augmented monic-normalization matrix; the current sufficient
precision is `M_out+K_M+2K_B`, plus entry-construction losses. A promising
common genericity test is to translate the possible half points by the
same sigma. There are at most `2^(2g)` rational two-torsion choices; a proof
may union-bound them with a polynomial extra precision allowance, but
must not enumerate them. This needs an actual sublevel estimate.

The cheapest falsifier is a native family for which every permitted
sigma-grid representative makes the relevant RR minors have
superpolynomial content, or for which the claimed cap grows
multiplicatively through saturation. Bounded individual support coordinates,
bounded matrix dimensions, and branch-resultant bounds alone do not
exclude this. If the RR gate passes but the Stoll minors do not, record
that distinction; do not label the full local image closed.

**Strongest classical baseline.** Stoll's halving/descent and ordinary
local squareclass arithmetic are classical. The proposed local compiler
would also be classical; the prospective quantum benefit in a global
Selmer computation remains confined to the already specified global
class/unit arithmetic. This is not a new quantum primitive or a separation.

## 2. Gaudin: directly compile a counterdiabatic generator

**Native input/output.** Even `N`, a product label `b`, rational target
`t in [0,1]`, and error `eta`, for the admitted picket-fence charges

    Q_i(t)=n_i+(t/2) sum_(j!=i)(SWAP_ij-I)/(i-j).

Prepare the continuously followed joint eigenstate from `b` in
`poly(N,input bits,1/eta)` gates. No Bethe roots, joint eigenvalues,
eigenbasis or target-dependent Hamiltonian is supplied. Efficient
preparation of interacting excited states is the external motivation.

**New operation.** Seek a Hermitian, number-conserving generator in the
explicit three-local ansatz

    A(t)=sum_(i<j) a_ij(t) C_ij
         +sum_(i<j,k distinct) b_ijk(t) C_ij Z_k,
    C_ij=X_i Y_j-Y_i X_j,

and solve the exact linear operator equations

    [Q_j, Q_i' + i[A,Q_i]]=0  for every i,j.

For this fixed-locality ansatz, all nested commutators have polynomially
many Pauli coefficients. The equations are linear in the unknown
coefficients and can be solved over rational functions in `t`, without
diagonalizing the `2^N`-dimensional space. On simple joint eigenspaces,
these identities make `A` transport the projectors. If it has a paid
polynomial integrated coefficient norm, precision bound, and no harmful
poles on `[0,1]`, simulating `A` directly prepares the branch. This is a
different constructive mechanism from proving a lower joint gap.

**Paid resources and next test.** The charges and Pauli arithmetic are
explicit. Existence and boundedness of this `A` are entirely unproved.
First solve the exact ansatz at one rational interior coupling for
`N=4` or `6`; inconsistency is a decisive falsifier of this ansatz. It
does not refute higher-body or other spectral-flow generators. A solution
at finite `N` supplies no all-`N` theorem; an all-`N` formula and its norm
ledger are the acceptance test. Equations on the whole Hilbert space
are stronger than equations only in one magnetization sector; retain
that distinction when reporting a negative test.

**Baseline/rank.** Classical Bethe continuation, tensor-network sampling
with charged bond dimension, and exact diagonalization remain the matched
comparators. The retained sources do not supply a full native sampler or
this gauge potential. This route has high upside but weaker positive
structure than the Kummer compiler; rank second. Do not retry the old gap
question or reinterpret the old prefix-norm failure as evidence for it.

## 3. Off-front-state: cyclotomic evaluation for full sparse relations

**Native input/output.** The original growing-degree field
`Q(T_1,...,T_s)[Y]/f`, with monic irreducible `f`, charged numerical
`Y`-degree, and nonzero units specified by sparse rational coefficients
and binary exponents. Return the FULL integer lattice `Rel={e:u^e=1}`
in polynomial sparse BIT complexity. The repository has a written
quantum modular-specialization algorithm and a classical algorithm for
`Alg={e:u^e is algebraic over Q}`. Degree one/two and monomial Kummer
families already have full classical matches.

**New operation and precise sufficient lemma.** Use binary Kronecker
substitution `T_j=X^(w_j)` with weights large enough to preserve the
nonzero denominator/discriminant/unit-resultant polynomial `P(X)`.
Its degree may be huge, but its degree's bit length and
`log ||P||_1` have explicit polynomial bounds from the original sparse
coefficients and the polynomial-size resultant determinants. No
determinant expansion is required.

The new question is whether the STRUCTURED resultants here satisfy

    m=ord_(X=1) P <= poly(native sparse input size).

If so, `Q=P/(X-1)^m` is integral and

    0 < |Q(1)| <= ||P||_1 (deg P)^m,

so `Q(1)` has polynomial bit length. Every bad prime cyclotomic order
`ell` obeys `Phi_ell | Q`, hence `ell | Q(1)`. Trying a polynomial number
of distinct small primes therefore finds a good root-of-unity evaluation.
Test each candidate directly in `Q(zeta_ell)[Y]/f`; do not compute `P`,
`m`, or `Q(1)`. The hypothesized universal bound pays the finite search.
Its algebra dimension and coefficient heights are polynomial because
the root of unity has small degree and binary powers reduce modulo `ell`.

Run classical Lenstra--Silverberg relations on the original evaluated
units and intersect with `Alg`. This retains joint embedding alignment
and torsion. For an `Alg` product, evaluation is injective on the field
of algebraic constants in the localized input algebra; therefore that
intersection is the original full `Rel`. This is an end-to-end
conditional classical match, not just an isolated constant-field oracle.

**Falsifier/baseline/rank.** Find a legal sparse input whose relevant
resultant has superpolynomial multiplicity at `X=1`; a generic circuit
such as `(X-1)^(2^m)` is not enough unless realized in this native
presentation with charged degree and sparse input size respected.
Conversely, bounds on the expanded resultant's support do not prove the
lemma. Existing sparse-Puiseux and dense-degree algorithms do not pay it.
The operation avoids the already refuted large rational specialization
and individual-norm shortcuts. It is concrete and potentially decisive,
but the multiplicity estimate is new and unproved here; rank third.

## Sources and dispatch boundary

Six corpus `been-tried`/`baselines` queries were run for the three
mechanisms. They locate the existing scoped notes and classical
comparators; their rankings are not literature verdicts.

Actual retained primary text read in this pass:

- Stoll, `audits/sources/local_halving_saturation/stoll.txt`, Section 5,
  Proposition 5.1 and the explicit p-adic precision warning. It supplies
  exact-field halving, not a uniform BIT theorem.
- Lutz et al., `audits/sources/gaudin_charge_tracking/lutz.txt`, the charge
  definitions and finite-coupling qualifications; the retained v3 was
  also searched for the proposed gauge-potential mechanism. This is not
  a complete literature search for counterdiabatic Gaudin algorithms.
- Lenstra--Silverberg Theorem 1.11, retained primary excerpt
  `audits/sources/sparse_charzero_relations/finite_Q_relations.txt`:
  polynomial full relations in an EXPLICIT finite Q-algebra.
- Oki, `audits/sources/general_sparse_constants/oki.txt`, Remark 12:
  its determinant-degree clock depends on numerical degree. It neither
  proves nor refutes the proposed torus multiplicity estimate.

The retained global quantum arithmetic theorem, the complete sparse
quantum relation composition, closest Gaudin counterdiabatic literature,
and any published sparse torus-multiplicity theorem NEED PARENT
PRIMARY-SOURCE CHECK before their scopes enter a new theorem or novelty
claim. No new source coverage is asserted from a failed local search.

Recommended next dispatch: attack the selected uniform RR coordinate
reset, with the explicit sigma formulas and closed-divisor input. Require
either a bounded randomized construction with an induction ledger or a
native counterfamily. Do not dispatch another general halving survey,
conductivity sampler barrier, gap-constant variant, or benchmark expansion.
