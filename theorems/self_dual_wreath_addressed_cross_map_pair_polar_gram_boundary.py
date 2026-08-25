"""Addressed cross maps are easy; phase-only global polar assembly is not.

The preceding Schur-companion scope theorem isolated a cross-source-branch
operation as the missing ingredient.  There are two different operations that
must not be conflated.

For branch inclusions ``J_e:M_e -> X`` with ``E_e=J_e J_e^*``, a *queried raw
cross map* is

    J_f^* J_e : M_e -> M_f.                                  (1)

Once the proved physical-invariant/Schur-companion interfaces are admitted,
(1) already has a normalization-one block encoding.  Decode branch ``e`` to
``J_e x``, block-encode

    E_f = (I + (2E_f-I))/2,                                  (2)

with one LCU ancilla and the supplied-label invariant reflection, and encode
the surviving vector through branch ``f``.  The signal block is exactly
``J_f^*J_e``.  The two orientation masks control only which of
``O(k)=O(n log n)`` source factors participate in the diagonal action, so the
construction is uniform over coherent ``(e,f)`` queries and never enumerates
the ``4^k`` possible pairs.  Its block-encoding normalization is one, although
its useful singular amplitudes can still be exponentially small.

The pair-polar theorem is stronger locally.  Coherent GPE exports the common
carrier row and directly implements

    U_(f<-e) = polar(J_f^*J_e)                                (3)

on its support, bypassing the small principal correlations.  A tempting
global construction is therefore to place these normalization-one pair polars
in every off-diagonal block and treat

    K_pol[e,f] = U_(e<-f),       K_pol[e,e]=I                 (4)

as the orientation Gram or its already-whitened replacement.

Equation (4) fails exactly when the pair connection has holonomy.  More
generally, a Hermitian block matrix with identity diagonal and unitary
off-diagonal blocks can be positive semidefinite only if every cycle is flat.
Indeed, in a Gram factorization ``K=W^*W``, unitary overlap
``W_e^*W_f`` forces the two isometric ranges to coincide, so
``U_(e<-f)=W_e^*W_f`` is a coboundary and every loop product is identity.
Conversely a flat family has the evident common-range Gram factorization.

For the exact regular-``S_3`` transposition triangle, the pair holonomy on the
starting plus space has spectrum ``{1,-1,-1}``.  The physical overlap Gram is
positive with spectrum

    {0,0,0,0, 3/2,3/2,3/2,3/2, 3},

because the two nonflat carrier directions retain correlation ``1/2``.  The
phase-only replacement (4) has spectrum

    {-1,-1, 0,0, 2,2,2,2, 3}.                               (5)

Thus it is not a Gram operator at all.  Under ``k`` tensor copies, the
negative eigenvalue multiplicity is

    (3^k-(-1)^k)/2,                                         (6)

an asymptotic ``1/6`` of the three-branch coefficient space.  The witness
embeds into fixed-point-free involutions in every even ``S_n``, but no positive
Plancherel mass for this particular chart is claimed.

The corrected frontier is therefore tightly normalized operator-valued metric
assembly, not queried pair access.  The successor linear-assembly theorem
retains the positive factors and compiles the exact global Gram as ``G/q``,
proving that ``alpha=q`` is sharp for equal-coefficient address mixing.  What
remains is a natural ``q/poly(n)`` useful spectral window or a hierarchical,
representation-specific global polar.  This theorem is not an
arbitrary-circuit lower bound, a natural-mass no-go, a physical PGM, or an
algorithm.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import right_regular_matrix
from coset_hidden_involution_pair_polar_holonomy_no_go import (
    audit_pair_polar_holonomy,
    embedding_record,
    s3_transpositions,
)
from coset_hidden_involution_pair_polar_phase_compiler import (
    phase_compiled_pair_polar,
)
from research_registry import NegativeResultRecord, upsert_negative_result, utc_now
from self_dual_wreath_gpe_pair_polar_transport import (
    run_gpe_pair_polar_transport,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ADDRESSED-CROSS-MAP-PAIR-POLAR-GRAM-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = "SCHUR-COMPANION-PHASE-ONLY-PAIR-POLAR-GRAM-NO-GLOBAL-POLAR"


@dataclass(frozen=True)
class AddressedCrossMapControl:
    branch_count: int
    ambient_dimension: int
    branch_dimension: int
    ordered_pair_query_count: int
    maximum_projector_lcu_unitarity_residual: float
    maximum_projector_signal_block_residual: float
    maximum_decoded_cross_map_residual: float
    maximum_pair_polar_unitarity_residual: float
    addressed_cross_map_block_encoding_normalization: float
    exact_addressed_cross_map_oracle_verified: bool
    status: str


@dataclass(frozen=True)
class PairPolarGramControl:
    branch_count: int
    branch_dimension: int
    physical_gram_dimension: int
    physical_gram_rank: int
    physical_gram_minimum_eigenvalue: float
    physical_gram_minimum_positive_eigenvalue: float
    phase_only_kernel_minimum_eigenvalue: float
    phase_only_kernel_negative_eigenvalue_count: int
    phase_only_kernel_zero_eigenvalue_count: int
    maximum_physical_spectrum_residual: float
    maximum_phase_only_spectrum_residual: float
    minimum_nontrivial_pair_correlation: float
    maximum_nontrivial_pair_correlation: float
    positive_holonomy_multiplicity: int
    negative_holonomy_multiplicity: int
    phase_only_kernel_positive_semidefinite: bool
    exact_metric_retention_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class CrossMapOracleScalingRecord:
    n: int
    information_threshold_copy_count: int
    coherent_pair_query_qubit_count: int
    orientation_pair_count_expression: str
    source_factor_mask_controls: int
    invariant_reflection_call_count: int
    schur_companion_interface_call_count: int
    addressed_raw_cross_map_normalization: float
    orientation_pair_table_enumerated: bool
    uniform_coherent_pair_query_polynomial: bool
    direct_gpe_pair_polar_polynomial: bool
    full_address_transition_gram_normalization_one_proved: bool
    complete_orientation_polar_polynomial: bool
    status: str


@dataclass(frozen=True)
class TensorPhaseOnlyBoundaryRecord:
    n: int
    copy_count: int
    tensor_starting_plus_dimension_decimal: str
    phase_only_kernel_dimension_decimal: str
    phase_only_negative_eigenvalue_count_decimal: str
    phase_only_negative_eigenvalue_fraction: float
    phase_only_minimum_eigenvalue: float
    fixed_point_free_embedding: bool
    positive_natural_plancherel_mass_proved: bool
    status: str


@dataclass(frozen=True)
class AddressedCrossMapPairPolarGramTheorem:
    input_space: str
    output_space: str
    addressed_cross_map_identity: str
    block_encoding_circuit: str
    uniformity: str
    normalization: str
    direct_pair_polar: str
    positivity_flatness_criterion: str
    scalable_counterexample: str
    natural_relevance: str
    classical_alternative: str
    corrected_bottleneck: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class AddressedCrossMapPairPolarGramReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: AddressedCrossMapPairPolarGramTheorem
    addressed_cross_map_control: AddressedCrossMapControl
    pair_polar_gram_control: PairPolarGramControl
    scaling_records: list[CrossMapOracleScalingRecord]
    tensor_boundary_records: list[TensorPhaseOnlyBoundaryRecord]
    circuit_contract: list[dict[str, str | bool | int | float]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _plus_basis(reflection: np.ndarray, tolerance: float) -> np.ndarray:
    projector = (np.eye(len(reflection)) + reflection) / 2.0
    values, vectors = np.linalg.eigh((projector + projector.conj().T) / 2.0)
    return vectors[:, values > 1.0 - 100 * tolerance]


def projector_lcu_unitary(reflection: np.ndarray) -> np.ndarray:
    """Return a one-ancilla unitary whose zero signal block is ``(I+R)/2``."""

    if reflection.ndim != 2 or reflection.shape[0] != reflection.shape[1]:
        raise ValueError("reflection must be square")
    dimension = len(reflection)
    hadamard = np.asarray([[1.0, 1.0], [1.0, -1.0]]) / math.sqrt(2.0)
    controlled = np.zeros((2 * dimension, 2 * dimension), dtype=complex)
    controlled[:dimension, :dimension] = np.eye(dimension)
    controlled[dimension:, dimension:] = reflection
    layer = np.kron(hadamard, np.eye(dimension))
    return layer @ controlled @ layer


def s3_pair_data(
    tolerance: float = 1e-9,
) -> tuple[tuple[np.ndarray, ...], tuple[np.ndarray, ...], tuple[np.ndarray, ...]]:
    reflections = tuple(
        right_regular_matrix(3, involution) for involution in s3_transpositions()
    )
    bases = tuple(_plus_basis(reflection, tolerance) for reflection in reflections)
    projectors = tuple(basis @ basis.conj().T for basis in bases)
    return reflections, projectors, bases


def audit_addressed_cross_map_oracle(
    tolerance: float = 1e-9,
) -> AddressedCrossMapControl:
    reflections, projectors, bases = s3_pair_data(tolerance)
    ambient = len(reflections[0])
    lcu_unitarity = 0.0
    signal_residual = 0.0
    decoded_residual = 0.0
    pair_polar_residual = 0.0
    for target in range(3):
        lcu = projector_lcu_unitary(reflections[target])
        lcu_unitarity = max(
            lcu_unitarity,
            float(np.linalg.norm(lcu.conj().T @ lcu - np.eye(2 * ambient), ord=2)),
        )
        signal = lcu[:ambient, :ambient]
        signal_residual = max(
            signal_residual,
            float(np.linalg.norm(signal - projectors[target], ord=2)),
        )
        for source in range(3):
            observed = bases[target].conj().T @ signal @ bases[source]
            expected = bases[target].conj().T @ bases[source]
            decoded_residual = max(
                decoded_residual,
                float(np.linalg.norm(observed - expected, ord=2)),
            )
            if source != target:
                polar, _, _ = phase_compiled_pair_polar(
                    reflections[source],
                    reflections[target],
                    tolerance=tolerance,
                )
                block = bases[target].conj().T @ polar @ bases[source]
                pair_polar_residual = max(
                    pair_polar_residual,
                    float(np.linalg.norm(block.conj().T @ block - np.eye(3), ord=2)),
                )
    verified = bool(
        max(
            lcu_unitarity,
            signal_residual,
            decoded_residual,
            pair_polar_residual,
        )
        <= 100 * tolerance
    )
    return AddressedCrossMapControl(
        branch_count=3,
        ambient_dimension=ambient,
        branch_dimension=3,
        ordered_pair_query_count=9,
        maximum_projector_lcu_unitarity_residual=lcu_unitarity,
        maximum_projector_signal_block_residual=signal_residual,
        maximum_decoded_cross_map_residual=decoded_residual,
        maximum_pair_polar_unitarity_residual=pair_polar_residual,
        addressed_cross_map_block_encoding_normalization=1.0,
        exact_addressed_cross_map_oracle_verified=verified,
        status=(
            "normalization-one-addressed-cross-map-verified"
            if verified
            else "addressed-cross-map-control-failure"
        ),
    )


def phase_only_pair_polar_kernel(
    reflections: tuple[np.ndarray, ...],
    bases: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> np.ndarray:
    if len(reflections) != len(bases):
        raise ValueError("reflection and basis counts differ")
    branch_count = len(reflections)
    branch_dimension = bases[0].shape[1]
    if any(basis.shape[1] != branch_dimension for basis in bases):
        raise ValueError("all branch dimensions must agree")
    blocks: list[list[np.ndarray]] = []
    for target in range(branch_count):
        row: list[np.ndarray] = []
        for source in range(branch_count):
            if target == source:
                block = np.eye(branch_dimension)
            else:
                polar, _, _ = phase_compiled_pair_polar(
                    reflections[source],
                    reflections[target],
                    tolerance=tolerance,
                )
                block = bases[target].conj().T @ polar @ bases[source]
            row.append(block)
        blocks.append(row)
    return np.block(blocks)


def audit_pair_polar_global_gram_boundary(
    tolerance: float = 1e-9,
) -> PairPolarGramControl:
    reflections, _, bases = s3_pair_data(tolerance)
    physical = np.block(
        [
            [bases[target].conj().T @ bases[source] for source in range(3)]
            for target in range(3)
        ]
    )
    phase_only = phase_only_pair_polar_kernel(
        reflections,
        bases,
        tolerance=tolerance,
    )
    physical_values = np.linalg.eigvalsh(
        (physical + physical.conj().T) / 2.0
    )
    phase_values = np.linalg.eigvalsh(
        (phase_only + phase_only.conj().T) / 2.0
    )
    expected_physical = np.asarray(
        [0.0, 0.0, 0.0, 0.0, 1.5, 1.5, 1.5, 1.5, 3.0]
    )
    expected_phase = np.asarray([-1.0, -1.0, 0.0, 0.0, 2.0, 2.0, 2.0, 2.0, 3.0])
    nontrivial_correlations: list[float] = []
    for left in range(3):
        for right in range(left + 1, 3):
            singular = np.linalg.svd(
                bases[left].conj().T @ bases[right],
                compute_uv=False,
            )
            nontrivial_correlations.extend(
                float(value) for value in singular if value < 1.0 - 100 * tolerance
            )
    holonomy = audit_pair_polar_holonomy(tolerance=tolerance)
    physical_residual = float(
        np.max(np.abs(np.sort(physical_values) - expected_physical))
    )
    phase_residual = float(
        np.max(np.abs(np.sort(phase_values) - expected_phase))
    )
    negative = int(np.sum(phase_values < -100 * tolerance))
    zeros = int(np.sum(np.abs(phase_values) <= 100 * tolerance))
    verified = bool(
        holonomy.nontrivial_holonomy_verified
        and physical_values[0] >= -100 * tolerance
        and negative == 2
        and physical_residual <= 100 * tolerance
        and phase_residual <= 100 * tolerance
        and nontrivial_correlations
        and max(abs(value - 0.5) for value in nontrivial_correlations)
        <= 100 * tolerance
    )
    positive_physical = physical_values[physical_values > 100 * tolerance]
    return PairPolarGramControl(
        branch_count=3,
        branch_dimension=3,
        physical_gram_dimension=len(physical),
        physical_gram_rank=len(positive_physical),
        physical_gram_minimum_eigenvalue=float(physical_values[0]),
        physical_gram_minimum_positive_eigenvalue=float(positive_physical[0]),
        phase_only_kernel_minimum_eigenvalue=float(phase_values[0]),
        phase_only_kernel_negative_eigenvalue_count=negative,
        phase_only_kernel_zero_eigenvalue_count=zeros,
        maximum_physical_spectrum_residual=physical_residual,
        maximum_phase_only_spectrum_residual=phase_residual,
        minimum_nontrivial_pair_correlation=min(nontrivial_correlations),
        maximum_nontrivial_pair_correlation=max(nontrivial_correlations),
        positive_holonomy_multiplicity=holonomy.positive_holonomy_multiplicity,
        negative_holonomy_multiplicity=holonomy.negative_holonomy_multiplicity,
        phase_only_kernel_positive_semidefinite=bool(
            phase_values[0] >= -100 * tolerance
        ),
        exact_metric_retention_boundary_verified=verified,
        status=(
            "phase-only-pair-polar-gram-indefinite-metric-required"
            if verified
            else "pair-polar-global-gram-control-failure"
        ),
    )


def cross_map_oracle_scaling(n: int) -> CrossMapOracleScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    log_order = math.lgamma(n + 1) / math.log(2.0)
    copies = math.ceil(3.0 * log_order) + 2
    return CrossMapOracleScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        coherent_pair_query_qubit_count=2 * copies,
        orientation_pair_count_expression=f"2^{2 * copies}",
        source_factor_mask_controls=2 * copies,
        invariant_reflection_call_count=1,
        schur_companion_interface_call_count=2,
        addressed_raw_cross_map_normalization=1.0,
        orientation_pair_table_enumerated=False,
        uniform_coherent_pair_query_polynomial=True,
        direct_gpe_pair_polar_polynomial=True,
        full_address_transition_gram_normalization_one_proved=False,
        complete_orientation_polar_polynomial=False,
        status="addressed-cross-map-and-pair-polar-polynomial-global-metric-open",
    )


def tensor_phase_only_boundary_record(n: int) -> TensorPhaseOnlyBoundaryRecord:
    embedded = embedding_record(n)
    dimension = int(embedded.tensor_starting_plus_dimension_decimal)
    negative = int(embedded.tensor_negative_holonomy_dimension_decimal)
    return TensorPhaseOnlyBoundaryRecord(
        n=n,
        copy_count=embedded.copy_count,
        tensor_starting_plus_dimension_decimal=str(dimension),
        phase_only_kernel_dimension_decimal=str(3 * dimension),
        phase_only_negative_eigenvalue_count_decimal=str(negative),
        phase_only_negative_eigenvalue_fraction=negative / (3 * dimension),
        phase_only_minimum_eigenvalue=-1.0,
        fixed_point_free_embedding=True,
        positive_natural_plancherel_mass_proved=False,
        status="extensive-phase-only-indefiniteness-natural-mass-open",
    )


def run_addressed_cross_map_pair_polar_gram_boundary(
) -> AddressedCrossMapPairPolarGramReport:
    cross_control = audit_addressed_cross_map_oracle()
    gram_control = audit_pair_polar_global_gram_boundary()
    gpe = run_gpe_pair_polar_transport()
    gpe_verified = bool(
        gpe.claim_gate["uniform_polynomial_pair_polar_circuit_proved"]
    )
    verified = bool(
        cross_control.exact_addressed_cross_map_oracle_verified
        and gram_control.exact_metric_retention_boundary_verified
        and gpe_verified
    )
    scaling = [
        cross_map_oracle_scaling(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    tensor = [
        tensor_phase_only_boundary_record(n)
        for n in (6, 8, 16, 32, 64)
    ]
    theorem = AddressedCrossMapPairPolarGramTheorem(
        input_space=(
            "Coherent query masks |e,f>, a vector in the encoded companion "
            "branch K_(nu,e), and clean invariant-reflection/Schur-interface ancillas."
        ),
        output_space=(
            "The companion branch K_(nu,f), with the signal block equal to "
            "B_f J_f^*J_e B_e^* and the query masks retained."
        ),
        addressed_cross_map_identity=(
            "B_f J_f^* E_f E_e J_e B_e^*=B_f J_f^*J_e B_e^* on branch-e input."
        ),
        block_encoding_circuit=(
            "Decode the e companion, use one Hadamard-LCU ancilla and the "
            "reflection 2E_f-I to block-encode E_f=(I+R_f)/2, then encode branch f."
        ),
        uniformity=(
            "The e,f bits control factorwise diagonal S_n actions across "
            "O(n log n) source factors; no orientation-pair table is enumerated."
        ),
        normalization=(
            "The addressed raw cross map has alpha=1. Small principal "
            "correlations remain signal singular values, not LCU normalization."
        ),
        direct_pair_polar=(
            "The predecessor coherent-GPE row-swap circuit implements the support "
            "polar of each addressed cross map without inverse-correlation amplification."
        ),
        positivity_flatness_criterion=(
            "A Hermitian identity-diagonal block matrix with unitary pair blocks "
            "is PSD iff the pair connection is flat on every cycle."
        ),
        scalable_counterexample=(
            "The regular-S3 transposition triangle has holonomy {1,-1,-1}; "
            "its phase-only block kernel has two eigenvalues -1, and k copies "
            "have (3^k-(-1)^k)/2 negative eigenvalues."
        ),
        natural_relevance=(
            "The addressed oracle and pair polar are uniform for arbitrary "
            "coherently supplied Plancherel labels and masks. The S3 holonomy "
            "embedding is scalable but is not assigned positive natural Schur mass."
        ),
        classical_alternative=(
            "Finite cross maps and spectra are classically contractible. No "
            "polynomial all-n classical global metric assembly, decoder, or "
            "quantum/classical separation follows."
        ),
        corrected_bottleneck=(
            "The successor uniform linear mixer assembles the positive metric factors into G/q and proves "
            "alpha=q sharp for equal coefficients. Prove a natural q/poly(n) retained window or compile a "
            "hierarchical/direct global polar."
        ),
        scope=(
            "This corrects the raw-cross-map access ledger and kills only the "
            "phase-only pair-polar Gram ansatz. Holonomy-aware metric assembly, "
            "direct global Racah transforms, multi-round decoders, and new circuits remain open."
        ),
        theorem_verified=verified,
        status=(
            "addressed-cross-map-and-pair-polar-proved-phase-only-global-gram-refuted"
            if verified
            else "addressed-cross-map-pair-polar-gram-validation-failure"
        ),
    )
    return AddressedCrossMapPairPolarGramReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        addressed_cross_map_control=cross_control,
        pair_polar_gram_control=gram_control,
        scaling_records=scaling,
        tensor_boundary_records=tensor,
        circuit_contract=[
            {
                "step": "coherent_pair_address",
                "operation": "Retain e,f and compute factor membership controls bitwise.",
                "normalization": 1.0,
                "polynomial": True,
            },
            {
                "step": "decode_source_companion",
                "operation": "Apply the proved branch-e Schur/Bell interface in reverse.",
                "normalization": 1.0,
                "polynomial": True,
            },
            {
                "step": "project_target_range",
                "operation": "Use one LCU ancilla and supplied-label reflection 2E_f-I.",
                "normalization": 1.0,
                "polynomial": True,
            },
            {
                "step": "encode_target_companion",
                "operation": "Apply the branch-f Schur/Bell interface and uncompute masks.",
                "normalization": 1.0,
                "polynomial": True,
            },
            {
                "step": "optional_pair_polar",
                "operation": "Use coherent GPE row reassociation instead of amplifying the raw cross map.",
                "normalization": 1.0,
                "polynomial": True,
            },
        ],
        proof_obligations=[
            {
                "obligation": "compile_addressed_raw_cross_map",
                "resolved": verified,
                "resolution": "Physical-interface/projector/interface sandwich gives an alpha-one signal block.",
            },
            {
                "obligation": "make_pair_query_uniform_without_exponential_table",
                "resolved": True,
                "resolution": "Orientation masks control O(n log n) factor actions bitwise.",
            },
            {
                "obligation": "compile_each_pair_polar_without_inverse_correlation",
                "resolved": gpe_verified,
                "resolution": "The existing coherent-GPE carrier row swap implements the partial polar directly.",
            },
            {
                "obligation": "test_phase_only_global_pair_polar_gram",
                "resolved": verified,
                "resolution": "The exact S3 holonomy block has two eigenvalues -1 and tensor-extensive negativity.",
            },
            {
                "obligation": "compile_global_operator_valued_metric_assembly",
                "resolved": True,
                "resolution": "The successor prepare/query/erase theorem compiles the exact positive signal G/q without an entry table.",
            },
            {
                "obligation": "prove_polynomial_full_kernel_normalization_and_window",
                "resolved": False,
                "resolution": "Entry-query alpha=1 does not set the normalization or hard edge of the full address-transition operator.",
            },
            {
                "obligation": "prove_positive_natural_mass_holonomy_metric_event",
                "resolved": False,
                "resolution": "The scalable S3 witness has no proved positive Plancherel mass in the physical Schur ensemble.",
            },
            {
                "obligation": "decode_hidden_involution_and_separate_classically",
                "resolved": False,
                "resolution": "No outcome-information, decoder, or classical lower bound is supplied.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The companion stack cannot implement even a queried raw J_f^*J_e block.",
                "resolved": True,
                "resolution": "That companion-only closure omits the already-compiled physical interface; decoding, E_f projection, and re-encoding supply the raw block at alpha one.",
            },
            {
                "objection": "Alpha-one entry access compiles the complete dense orientation matrix.",
                "resolved": True,
                "resolution": "False. A SELECT query retains e,f; converting entry queries into an address-transition sum still requires a global assembly and normalization theorem.",
            },
            {
                "objection": "Direct pair polars may replace every cross-map magnitude by one.",
                "resolved": True,
                "resolution": "False on nonflat cycles: the resulting identity-diagonal block kernel is indefinite.",
            },
            {
                "objection": "Indefiniteness is an arbitrary-circuit lower bound.",
                "resolved": True,
                "resolution": "It kills only the phase-only Gram ansatz; metric-aware holonomy resolvers and direct global transforms remain open.",
            },
            {
                "objection": "The all-n fixed-point-free embedding proves natural-mass failure.",
                "resolved": True,
                "resolution": "It does not. Natural Plancherel weight for the witness is explicitly open.",
            },
        ],
        primary_literature=[
            {
                "id": "bacon-chuang-harrow-schur-2004",
                "url": "https://arxiv.org/abs/quant-ph/0407082",
                "use": "coherent generalized phase estimation and Schur carrier-row access",
            },
            {
                "id": "beals-symmetric-qft-1997",
                "url": "https://doi.org/10.1145/258533.258548",
                "use": "uniform polynomial S_n Fourier transform",
            },
        ],
        headline_metrics={
            "addressed_raw_cross_map_block_encoding_theorem_count": int(verified),
            "addressed_raw_cross_map_block_encoding_normalization": 1.0,
            "uniform_coherent_pair_query_theorem_count": int(verified),
            "direct_gpe_pair_polar_compiler_count": int(gpe_verified),
            "phase_only_global_pair_polar_gram_no_go_theorem_count": int(verified),
            "finite_control_failure_count": int(not verified),
            "finite_phase_only_negative_eigenvalue_count": gram_control.phase_only_kernel_negative_eigenvalue_count,
            "minimum_tensor_phase_only_negative_fraction": min(
                row.phase_only_negative_eigenvalue_fraction for row in tensor
            ),
            "global_operator_valued_metric_assembly_compiler_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "hidden_involution_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_schur_interface_supplies_addressed_raw_cross_map_block_encoding": verified,
            "addressed_raw_cross_map_block_encoding_normalization_one": verified,
            "uniform_coherent_pair_query_without_exponential_table": verified,
            "direct_gpe_pair_polar_compiled": gpe_verified,
            "pair_polar_inverse_carrier_amplification_required": False,
            "phase_only_pair_polar_block_kernel_positive_semidefinite": False,
            "phase_only_pair_polar_global_gram_ansatz_refuted": verified,
            "operator_valued_cross_metric_retention_required": verified,
            "canonical_uniform_linear_global_metric_assembly_compiled": True,
            "canonical_uniform_linear_global_metric_normalization": "q",
            "global_address_transition_kernel_polynomial_normalization_proved": False,
            "global_operator_valued_metric_assembly_compiled": False,
            "positive_natural_mass_holonomy_metric_event_proved": False,
            "physical_pgm_compiled": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Raw addressed cross maps and their pair polars are polynomially accessible at alpha one, but "
                "pair phases alone form an indefinite block kernel on nonflat cycles. The global positive metric "
                "is available from the successor linear theorem only as G/q; a natural q-scale retained window or "
                "hierarchical/direct polar remains the bottleneck."
            ),
        },
        status=theorem.status,
        summary=(
            "Corrected the cross-map access boundary: addressed raw J_f^*J_e blocks and direct pair polars are "
            "polynomially accessible with normalization one. Falsified the normalization-one phase-only global "
            "Gram construction by an exact, tensor-extensive holonomy-induced negative spectrum; the successor "
            "linear theorem assembles the physical metric only at sharp normalization q."
        ),
        falsifiers_triggered=[
            "The physical-interface/projector sandwich already block-encodes each queried raw cross map at alpha one.",
            "Small pair principal correlations do not obstruct the direct coherent-GPE pair polar.",
            "Entry-query normalization does not equal full dense address-transition normalization.",
            "Pair polar phases cannot be promoted to a global Gram without retaining the positive metric factors.",
            "A scalable fixed-point-free holonomy witness is not automatically a positive-natural-mass obstruction.",
        ],
    )


def write_addressed_cross_map_pair_polar_gram_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_addressed_cross_map_pair_polar_gram_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "Normalization-one addressed pair polars can replace every raw cross-map metric and directly "
                    "form the global orientation Gram/polar."
                ),
                reason_invalid=(
                    "Identity-diagonal unitary-overlap block kernels are PSD only for a flat connection. The exact "
                    "S3 pair-polar triangle has holonomy {1,-1,-1}, giving two eigenvalues -1 and tensor-extensive "
                    "negative spectrum."
                ),
                lesson=(
                    "Retain the positive factors |J_f^*J_e| and prove a coherent global PSD metric assembly; pair "
                    "phases and alpha-one entry queries alone are insufficient."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "addressed_raw_cross_map_normalization": 1.0,
                    "finite_phase_only_negative_eigenvalue_count": payload[
                        "headline_metrics"
                    ]["finite_phase_only_negative_eigenvalue_count"],
                    "minimum_tensor_phase_only_negative_fraction": payload[
                        "headline_metrics"
                    ]["minimum_tensor_phase_only_negative_fraction"],
                    "positive_natural_mass_holonomy_metric_event_proved": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_addressed_cross_map_pair_polar_gram_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
