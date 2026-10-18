# Independent-Label Hamiltonian DQI: Constructive Test And Classical Falsifier

2026-10-17. Local derivation, review pending; no novelty claim.

## Question And Selection

Can a noncommuting Pauli family combine efficient HDQI pilot preparation and
trivial syndrome decoding into a substantial ENERGY optimization advantage?

This is independent of the recent DCP obstruction batch. We compared:

- Further DCP readout variations: no new end-to-end construction identified.
- Hermitian-code DQI: a real extension of the code family, but not by itself a
  solution to compact predicate preparation or the existing classical attacks.
  See [Gu and Jordan](https://arxiv.org/abs/2510.06603).
- General-Pauli HDQI: separates pilot-state preparation from decoding.
  [Bu, Gu and Li](https://arxiv.org/abs/2601.18773) give a conditional algorithm.
  [Wocjan](https://arxiv.org/abs/2604.01022) gives efficient pilot MPSs when
  each generator has a uniform commutation sign against its predecessors.
  That paper explicitly leaves useful jointly decodable families open.

We selected the third route because independent symplectic labels remove
the decoding premise by binary linear inversion. That makes the proposed
family falsifiable without implementing an assumed decoder oracle.

## Concrete Proposed Family

Input is an explicit list of Hermitian Pauli words P_j and signed rational
coefficients c_j, H=sum_j c_j P_j. No unknown oracle, random function, QRAM
table or hidden advice is supplied. The symplectic labels must be linearly
independent over F2. A verified ordering must make P_j either commute with
ALL preceding words or anticommute with ALL of them. Repeated/identity/
dependent labels are rejected; unsupported graphs mean UNKNOWN, not hard.

Canonical physical realizations on m qubits are:

    P_j = X_j                      (commuting addition)
    P_j = Z_0 ... Z_(j-1) X_j       (anticommuting addition).

The X pivot on each new qubit proves independence. A last anticommuting
addition can connect all m terms, so this is not merely a bounded-component
test. The saved m512 control has that property.

Proposed quantum mechanism: known predecessor-uniform pilot MPS, reversible
linear syndrome inversion, coherent Bell readout and a suitable polynomial
filter. A polynomial-time ground-energy algorithm could matter only if
the same explicit family resists classical optimum-energy computation.
Pilot theorem, polynomial degree, precision, normalization and readout must
all be charged; a preparation subroutine alone never proves a speedup.

## Local Radius Derivation

Set H_j=sum_(i<=j) c_i P_i and R_j=norm(H_j). Independence gives two facts:

1. No nonempty product of these Pauli labels is the identity. In particular,
   tr(P_j f(H_(j-1)))=0 for every polynomial f when P_j commutes with all
   previous terms. Each eigenspace of H_(j-1) therefore has equal +1/-1
   multiplicities for P_j (spectral projectors are finite polynomials).
2. A Pauli Q anticommuting with every P_i exists: solve the full-row-rank
   symplectic system with all-one right-hand side. Thus every H_j has a
   spectrum symmetric about zero. This is not assumed for dependent labels.

If P_j commutes with all predecessors, both independent sign sectors occur:

    R_j = R_(j-1) + abs(c_j).

If it anticommutes with all predecessors, cross terms cancel:

    H_j^2 = H_(j-1)^2 + c_j^2 I,
    R_j = sqrt(R_(j-1)^2 + c_j^2).

Starting from R_0=0 gives E_min=-R_m. This is an O(m)-operation scalar
expression after polynomial-time rank/order validation. Bit complexity is
polynomial in input length and log(1/epsilon): use outward dyadic square-root
rounding with b>=ceil(log2(m/epsilon)). Each root is monotone and 1-Lipschitz
as a function of nonnegative previous radius, so interval width is at most
(number of root steps)*2^(-b). The executable solver uses integer square
roots and Fractions, never a numerical eigensolver, to produce the enclosure.

This falsifies the proposed ground-ENERGY separation, not HDQI correctness,
Gibbs sampling, arbitrary computational-basis sampling or quantum outputs.
The classical task here is to compute an optimum energy, not emit a quantum
state. No unsupported output-sampling equivalence is inferred.

## Constructive Native Ground-State Check

The canonical family also has a direct recursive ground circuit. An isolated
addition appends the correct X eigenstate. An anticommuting addition appends
|0> and applies exp(-i theta Z_<j Y_j/2), theta=-atan2(c_j,R_(j-1)). The two
basis vectors are the old ground state tensored with0, and its Z_<j image
tensored with1; H_j restricts to [[-R,c],[c,R]]. The rotation prepares its
lower eigenvector. Each Pauli rotation has an O(j)-gate elementary
decomposition, yielding a polynomial canonical construction without HDQI.
Only bounded dense execution is implemented; no native Clifford transport
to a general input realization or compiled fault-tolerant circuit is claimed.

## Evidence And Scope Falsifiers

Run `python theorems/hdqi_predecessor_uniform.py --write` and
`python -m pytest tests/test_hdqi_predecessor_uniform.py -q`.

- Four saved native Hamiltonians retain every term/coefficient, discovered
  order, rational enclosure, dense smallest eigenvalue and executed ground
  state's eigenvector residual. Tests check every predecessor pattern up to
  five terms, signed/zero coefficients, Y terms and smaller realizations.
- All120 input permutations of a mixed five-term example check order search.
- Independent high-precision Decimal arithmetic checks rational enclosures.
- A512-term input has a live rank/order/rational certificate, NOT a dense
  quantum run or evidence of a speedup.
- Dependence matters: ZZI+IZZ+ZIZ has ground energy-1, not-3. Its labels sum
  to zero; the API rejects it. A path-P4 commutation graph is also rejected,
  without claiming hardness or integrability failure.

## Decision And Next Experiment

Do not compile HDQI or run larger parameter scans on the independent-label
predecessor-uniform family to claim an ENERGY advantage. The strongest
baseline is the radius solver, not annealing or a generic exponential method.
The local proof still needs independent mathematical review and prior-art
comparison; no central proof status or broad negative has been promoted.

A surviving proposal must specify dependent labels with a real polynomial
decoder and nontrivial optimization task, or a different pilot preparation
on a graph outside this condition. For dependent labels, first compute
actual product/central constraints and test the decoder's promised radius;
do not retain the independent sign-sector argument. For a sampling claim,
specify the accessible observable/output and a matched classical sampling
task separately. These are scientific requirements, not requests to build
another general research subsystem.
