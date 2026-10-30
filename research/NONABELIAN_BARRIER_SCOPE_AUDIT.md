# Nonabelian Barrier Scope Audit

Status: SIX OVERBROAD NO-GO RECORDS REVIEWED FOR SCOPED QUARANTINE; no new algorithm or speedup.
Dates: 2026-10-19; extended 2026-10-30. Explicit countercontrols, not a general nonabelian-HSP theorem.

## Research Decision

The registry was incorrectly excluding collective nonabelian measurements using
algebra dimensions as gate lower bounds. Correcting this is necessary before
selecting a receiver, not evidence that such a receiver has been discovered.
Only these individually reviewed records are eligible for quarantine by this producer:

- `NEG-SYMMETRIC-GROUP-KRONECKER-RACAH-BARRIER`
- `NEG-SU2-COMPACT-LIE-HSP-COMMUTANT-INFLATION`
- `NEG-COSET-MULTIPLICITY-CARRIER-DECOUPLING-TRILEMMA`
- `NEG-CFI-GRAPH-COSET-LUKS-SUBSUMPTION-BARRIER`
- `NEG-WREATH-COSET-PERMUTATION-HOLEVO-INFORMATION-COLLAPSE`
- `NEG-ARBITRARY-DEGREE-REGULATOR-EXPONENTIAL-BARRIER`

The sixth review is a separately scoped arithmetic correction, reusing the
same hash-bound quarantine implementation rather than another registry writer.
See [the corrected number-field note](ARBITRARY_DEGREE_NUMBER_FIELD_REGULATOR_BARRIER.md).
Published arbitrary-degree quantum unit-group and principal-ideal algorithms
contradict the old universal exponential-degree claim. This is not a new
repository algorithm, nor a claim about generic lattice problems. The first
five reviews and their archived originals are unchanged.

The [third record's correction](COSET_MULTIPLICITY_CARRIER_TRILEMMA.md)
retains conjugacy-orbit invariance for FINAL POVM effects, corrects its
unphysical information calculation, and gives structured pair-class-sum
access without assuming a general efficient Racah transform. Blind
intermediate labels do not erase the retained carrier state. The original
factorial-copy and exponential-circuit claims are withdrawn.

On quarantine, complete originals are preserved in `registry/quarantined_campaign_negatives.json`.
The producer binds their canonical JSON hashes, refuses changed evidence and
duplicate IDs, and archives before removing active rows. Unreviewed records are
not blanket-quarantined. Old notes below their warnings remain historical,
not valid statements of current research scope.

## Scoped CFI Retraction

The fourth record was reviewed on **2026-10-30**. Its complete live original
from `registry/negative_results.json` is bound to canonical SHA-256
`878a234da47c9296c97d138328817c7b6ba44c5490f146494c391d0fd43110ac`.
Canonicalization uses `json.dumps(record, sort_keys=True, separators=(",", ":"))`
with the default ASCII escaping, then UTF-8 encoding. Quarantine archives the
whole original, including its withdrawn claims and evidence, without rewriting it.

The valid baseline survives: **explicit graph isomorphism at fixed maximum
degree has a polynomial-time classical algorithm**. This remains the matched
baseline for fixed-degree explicit CFI graphs, so that problem does not support
an exponential quantum-versus-classical runtime separation. The original's
unsupported `O(N^4)` specialization is withdrawn; no replacement exponent is
asserted here.

Also withdrawn are the false single-copy mutual-information formula, the
dimension-to-runtime lower-bound inference, and the resulting universal quantum
intractability claim. A large commutant does not require every measurement to
diagonalize the entire algebra. An ensemble-specific information obstruction
cannot be promoted to a bound on all CFI encodings or quantum algorithms.
The surviving classical baseline **does not exclude polynomial quantum
improvements or settle other input problems**, including implicit/oracle inputs
or growing-degree families. No new quantum algorithm or speedup is established.

The CFI producer now routes registry changes through
`quarantine_reviewed_negatives()` and cannot re-register the old ID. Its live
report and registry have been refreshed. Fixture tests exercise exact original
preservation, incremental archive extension, and hash-bound rejection. The
corrected [CFI note](CFI_GRAPH_COSET_LUKS_SUBSUMPTION_BARRIER.md) retains the
classical baseline and proves the counts for the actual graph construction.

## Scoped Wreath-Coset Retraction

The fifth record was reviewed on **2026-10-30**. Its complete live original
from `registry/negative_results.json` is bound to canonical SHA-256
`70d9b4a8d8b377ee21ca70ec35d0b981eeab9007656ed9800ffb73f9f2166bd4`,
using the same canonicalization as the fourth record. The existing quarantine
mechanism preserves the complete original; the review does not rewrite its
historical claims or evidence.

The displayed `H_tau` is not a subgroup for noncentral `tau` under the stated
swap semidirect product. In particular, multiplying its elements
`((e,tau),1)` and `((pi,pi),0)` gives `((pi,tau*pi),1)`, whereas membership
would require the second component to be `pi*tau`. A noncommuting `pi`
therefore witnesses failure of closure. The claimed coset ensemble cannot be
justified by that displayed set.

Independently, for `rho_tau = direct_sum_nu p_nu rho_tau^(nu)`, the trace
product is `sum_nu p_nu^2 Tr(rho_tau^(nu) rho_tau'^(nu))`, not a sum with
only one factor of `p_nu`. The asserted inverse-conjugacy-class overlap
therefore does not follow. It also yields self-overlap `1` at the identity,
incompatible with the same record's purity `1/n!` for `n >= 2`.

The asserted `O(k^2/n)` Holevo bound is unsupported by these calculations;
evaluating `k^2/n` is not a proof of a bound. Shannon conditional entropy
does not upper-bound MAP guessing success by `2^-H`; the relevant guessing
quantity is conditional min-entropy. Even if the claimed Holevo premise were
granted, Fano's additive `1` gives only an `O(1/(n log n))` ceiling at fixed
`k`, not the asserted `O(1/(n^2 log n))` ceiling or factorial suppression.

Consequently this record establishes **no blanket code-equivalence obstruction
or universal `Omega(n log n)` copy lower bound**. A valid twisted-diagonal
repair and any classical recovery analysis are separate work; neither an
attack nor a replacement algorithm is asserted in these registry reasons.
The producer and CLI are now corrected and the live artifacts refreshed;
see [the source analysis](WREATH_COSET_PERMUTATION_HOLEVO_COLLAPSE.md) for
the separately derived normalized states and matched classical attack on
the repaired family. Fixture tests check all five hash-bound originals,
including the unchanged fourth CFI review, archive extension, idempotence,
and rejection of changed evidence. Unreviewed records are not retracted.

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

Scoped fixture verification, without requiring refreshed live artifacts:

    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python -m pytest -q -p no:cacheprovider tests/test_nonabelian_barrier_scope_audit.py -k 'not live_report_registry_and_site_exclude_only_reviewed_ids'

Live artifact refresh and full scoped verification:

    OPENBLAS_NUM_THREADS=1 python theorems/nonabelian_barrier_scope_audit.py --write --quarantine
    OPENBLAS_NUM_THREADS=1 python -m pytest -q tests/test_nonabelian_barrier_scope_audit.py
    python qsearch.py validate

The report is `representation/nonabelian_barrier_scope_audit.json`. Normal
execution performs no registry writes; `--quarantine` is explicit and idempotent.
Routine CLI/experiment wiring stays with Gemini and must preserve these scopes.
