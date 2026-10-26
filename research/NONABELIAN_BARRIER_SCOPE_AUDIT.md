# Nonabelian Barrier Scope Audit

Status: TWO OVERBROAD NO-GO RECORDS QUARANTINED; no new algorithm or speedup.
Date: 2026-10-19. Explicit countercontrols, not a general nonabelian-HSP theorem.

## Research Decision

The registry was incorrectly excluding collective nonabelian measurements using
algebra dimensions as gate lower bounds. Correcting this is necessary before
selecting a receiver, not evidence that such a receiver has been discovered.
Only these two individually reviewed records are quarantined:

- `NEG-SYMMETRIC-GROUP-KRONECKER-RACAH-BARRIER`
- `NEG-SU2-COMPACT-LIE-HSP-COMMUTANT-INFLATION`

Complete originals are preserved in `registry/quarantined_campaign_negatives.json`.
The producer binds their canonical JSON hashes, refuses changed evidence and
duplicate IDs, and archives before removing active rows. Unreviewed records are
not blanket-quarantined. Old notes below their warnings remain historical,
not valid statements of current research scope.

## A Legal Single-Coset Measurement

For an order-two subgroup H={e,h} of a finite group G, its mixed regular coset
state is rho_h=(I+R_h)/|G|. Fix a PUBLIC involution t, without access to h.
The Hadamard test of R_t measures (I+R_t)/2, so trace orthogonality gives

    P(+ | h=t)=1; P(+ | h!=t)=1/2.

On a uniform ensemble of M distinct involutions, the mutual information is

    I = h2((1+1/M)/2) - (M-1)/M.

Binary relative entropy from uniform is at most chi-square/ln(2), and ln(2)>1/2.
Consequently 1/M-2/M^2 <= I <= 1/M. For transpositions in S_n, M=n(n-1)/2;
this is Theta(1/n^2), contradicting the old universal poly(n)/n! upper bound.

Permutations are encoded by their n images, each in ceil(log2 n) bits. Known
right multiplication by t=(i,j) swaps two image words. Its controlled version
uses ceil(log2 n) Fredkin gates, plus two H gates and one ancilla readout.
Neither the hidden involution nor an n! table is supplied to the test.

The exact verifier explicitly executes sparse H-controlled-R-H branches for
EVERY hidden transposition and EVERY coset representative in S_3 through S_6:
12,162 states. An independent dense S_4 test uses the full mixed state and
actual ancilla circuit. Larger n records evaluate formulas only.

**Why this is not progress toward a new speedup:** the transposition family
has only O(n^2) possibilities. Classically query f(e) and each f(t), comparing
outputs; this solves the same standard HSP promise in at most M+1 queries.
This is a counterexample to a claimed universal theorem, NOT a new oracle
problem, candidate, or graph-isomorphism algorithm.

The MRS hard case uses random products of n/2 disjoint transpositions, not a
single transposition. Its conjugacy class is superpolynomial. This public
membership test then has tiny information and does NOT evade that barrier.
[Moore--Russell--Schulman, Section 1 and Section 6](https://arxiv.org/abs/quant-ph/0501056).

## Spin One Is Not Spin Half

Write J=2j and s=2s_local. Starting with multiplicity m_0(0)=1, use the exact
Clebsch--Gordan recurrence: each J contributes m(J) copies of spins
|J-s|, |J-s|+2, ..., J+s. Check sum_J m(J)(J+1)=(s+1)^M.
The invariant commutant dimension is sum_J m(J)^2.

- Spin half: M=2 gives 2; M=3 gives 5; the general value is Catalan C_M.
- Spin one: M=2 gives 3; M=3 gives 15. The claimed Catalan formula is false.

Independent dense linear systems [X,J_x]=[X,J_y]=[X,J_z]=0 verify dimensions
3 for two spin-one systems and 5 for three qubits. Numerical nullities are
finite controls, with explicit singular-value threshold and gap; the recurrence
is exact integer arithmetic. No large Hilbert-space matrices are constructed.

The torus invariant |j,n,0> is a ZERO-WEIGHT state, not the usual extremal
spin-coherent state. Continuous HSPs also need an explicit oracle, discretization,
precision and error model before complexity assertions can be made.

## Large Algebra Does Not Force A Large Circuit

On M qubits, SWAP(1,2) tensor I commutes with collective SU(2). The Bell transform
U=CNOT(H tensor I) satisfies U^dagger SWAP U=diag(1,1,1,-1).
Measure by CNOT then H, then read the first two qubits; outcome 11 is the
antisymmetric sector. This uses TWO gates regardless of M, although the full
commutant has dimension Catalan C_M (6,564,120,420 at M=20).

The bounded producer checks the physical matrices, SU(2) generator commutators,
and diagonalization residuals at M<=6. M=20 is analytic only. This measures
ONE specified invariant, not every element, an arbitrary optimal HSP POVM,
or a simultaneous diagonalizer of a noncommutative algebra.

More substantively, efficient Schur/Clebsch--Gordan circuits have size
poly(M,d,log(1/epsilon)); exponential Hilbert or commutant dimension alone
cannot establish the advertised recoupling lower bound.
[Bacon--Chuang--Harrow](https://arxiv.org/abs/quant-ph/0407082).
This does not supply a general efficient symmetric-group Kronecker transform.
Worst-case hardness of EXACT classical coefficient evaluation is not a reduction
proving hardness of approximate quantum measurement implementation.

## What Remains Blocked

Weak irrep labels remain blind to conjugate orientations. For the GI coset
approach, Omega(n log n) jointly measured states are necessary for useful
information; that is a copy requirement, not a universal exponential gate
lower bound. [Hallgren--Roetteler--Sen](https://arxiv.org/abs/quant-ph/0511148).
Polynomial query complexity is achievable but its general algorithm takes
exponential time. [Ettinger--Hoyer--Knill](https://arxiv.org/abs/quant-ph/0401083).

Before re-entering GI/code equivalence, supply a PUBLIC, explicitly compiled
joint effect on the natural hard coset ensemble; prove useful distinguishing
mass at growing n, charge state preparation and accuracy, and compare matched
classical contractions and canonicalization. Neither a small commutant observable
nor a large formal PGM supplies this. Failure to exhibit such an effect is a
missing construction, not proof that all such constructions are impossible.

No additional barrier campaign or automatic candidate promotion follows this
correction. The next constructive direction must earn re-entry with an actual
receiver or natural reduction, not a renamed conditional interface.

## Reproduce

    OPENBLAS_NUM_THREADS=1 python theorems/nonabelian_barrier_scope_audit.py --write --quarantine
    OPENBLAS_NUM_THREADS=1 python -m pytest -q tests/test_nonabelian_barrier_scope_audit.py
    python qsearch.py validate

The report is `representation/nonabelian_barrier_scope_audit.json`. Normal
execution performs no registry writes; `--quarantine` is explicit and idempotent.
Routine CLI/experiment wiring stays with Gemini and must preserve these scopes.
