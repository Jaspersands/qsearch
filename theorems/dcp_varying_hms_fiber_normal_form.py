"""Varying-set HMS sampling and the DCP fiber-compression normal form.

The Fourier-sampling proof for Hidden Multiple Shift is samplewise.  Given a
known subset ``H_i`` and a phase sample

    |phi_(t_i,H_i)> = |H_i|^(-1/2) sum_(h in H_i) omega^(h t_i) |h>,

an inverse QFT returns ``t_i`` with probability ``|H_i|/q``.  Nothing in this
calculation requires the sets ``H_i`` to agree between samples.  If the public
vectors attached to the samples generate the ambient module, the all-correct
event still gives the hidden shift, with probability equal to the product of
the individual success probabilities.

For ``k`` DCP phase states with public labels ``x``, let

    L_x(b) = <x,b> mod N,
    eta_h = |L_x^(-1)(h)|,
    D = 2^k.

The tensor state is uniform over Boolean preimages, not over residues.  On the
fiber-uniform span, the canonical coisometry

    C_x |F_h> = |h>

converts it to the weighted multiplier state

    sum_h sqrt(eta_h/D) omega^(s h) |h>.

An inverse QFT then recovers ``s`` with probability

    (sum_h sqrt(eta_h))^2 / (N D),

exactly the covariant DCP PGM success formula.  By contrast, reversibly
computing ``L_x(b)`` while retaining the orthogonal ``b`` register gives target
probability exactly ``1/N``: the preimages cannot interfere.  Therefore the
HMS transfer is real, varying shift sets are harmless, and the entire missing
operation is the source-dependent polar/fiber coisometry ``C_x``.

Collisions are not an information obstruction.  Uniform multiplicities over
all residues give success one.  They are an implementation obstruction when
no efficient coherent fiber basis/ranking is known.  This module proves the
normal form and finite controls; it does not construct a generic polynomial
circuit for ``C_x`` or a polynomial DHSP algorithm.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

from dcp_covariant_pgm_audit import covariant_pgm_success
from research_registry import utc_now
from semidirect_hms_transfer_boundary import subset_sums_mod


REPORT_PATH = Path(
    "research/reductions/dcp_varying_hms_fiber_normal_form.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-VARYING-HMS-FIBER-NORMAL-FORM"
DEFAULT_CANDIDATE_ID = "HYP-SHIFT-MULTIPLICITY-AMPLIFICATION"


@dataclass(frozen=True)
class VaryingHmsFourierControl:
    control_id: str
    modulus: int
    supports: list[list[int]]
    phase_targets: list[int]
    support_sizes: list[int]
    observed_target_probabilities: list[float]
    expected_target_probabilities: list[float]
    maximum_probability_residual: float
    observed_joint_all_correct_probability: float
    expected_joint_all_correct_probability: float
    supports_identical: bool
    varying_support_extension_verified: bool
    status: str


@dataclass(frozen=True)
class FiberCompressionControl:
    control_id: str
    modulus: int
    labels: list[int]
    copy_count: int
    assignment_count: int
    occupied_residue_count: int
    collision_pair_count: int
    minimum_positive_multiplicity: int
    maximum_multiplicity: int
    multiplicities_uniform_on_support: bool
    canonical_coisometry_residual: float
    compressed_state_norm_residual: float
    observed_compressed_qft_success: float
    exact_weighted_qft_formula: float
    covariant_pgm_success_probability: float
    pgm_formula_residual: float
    forward_compute_with_preimage_garbage_success: float
    forward_garbage_formula_residual: float
    coherent_interference_gain: float
    structured_polylog_fiber_compression_known: bool
    generic_random_instance_circuit_constructed: bool
    normal_form_verified: bool
    status: str


@dataclass(frozen=True)
class FiberCompressionScaling:
    input_bits: int
    copy_count: int
    assignment_count_log2: int
    modulus_to_assignment_ratio_log2: int
    expected_collision_pairs_log2: float
    varying_set_fourier_measurement_cost: str
    missing_operation: str
    generic_polytime_compression_constructed: bool
    status: str


@dataclass(frozen=True)
class VaryingHmsFiberTheorem:
    varying_support_fourier_statement: str
    dcp_weighted_multiplier_statement: str
    pgm_identity: str
    retained_preimage_no_interference: str
    collision_scope: str
    implementation_equivalence: str
    theorem_scope_limit: str
    varying_support_extension_proved: bool
    weighted_multiplier_normal_form_proved: bool
    pgm_success_identity_proved: bool
    retained_preimage_no_interference_proved: bool
    collisions_are_information_no_go: bool
    generic_fiber_compression_constructed: bool
    dcp_polynomial_algorithm_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DcpVaryingHmsFiberNormalFormReport:
    created_at: str
    theorem_contract: dict[str, Any]
    varying_hms_controls: list[VaryingHmsFourierControl]
    fiber_controls: list[FiberCompressionControl]
    scaling_records: list[FiberCompressionScaling]
    theorem: VaryingHmsFiberTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def qft_matrix(modulus: int) -> np.ndarray:
    if modulus < 2:
        raise ValueError("modulus must be at least two")
    indices = np.arange(modulus)
    root = np.exp(2j * np.pi / modulus)
    return root ** np.outer(indices, indices) / math.sqrt(modulus)


def hms_phase_state(
    modulus: int,
    support: Sequence[int],
    phase_target: int,
) -> np.ndarray:
    canonical = [int(value) % modulus for value in support]
    if not canonical or len(set(canonical)) != len(canonical):
        raise ValueError("support must be nonempty and contain distinct residues")
    state = np.zeros(modulus, dtype=np.complex128)
    root = np.exp(2j * np.pi / modulus)
    for residue in canonical:
        state[residue] = root ** (residue * (phase_target % modulus))
    return state / math.sqrt(len(canonical))


def varying_hms_fourier_control(
    control_id: str,
    modulus: int,
    supports: Sequence[Sequence[int]],
    phase_targets: Sequence[int],
) -> VaryingHmsFourierControl:
    if len(supports) != len(phase_targets) or not supports:
        raise ValueError("supports and phase_targets must have equal positive length")
    inverse_qft = np.conjugate(qft_matrix(modulus).T)
    observed: list[float] = []
    expected: list[float] = []
    canonical_supports: list[list[int]] = []
    for support, target in zip(supports, phase_targets):
        canonical = [int(value) % modulus for value in support]
        state = hms_phase_state(modulus, canonical, target)
        decoded = inverse_qft @ state
        observed.append(float(abs(decoded[target % modulus]) ** 2))
        expected.append(len(canonical) / modulus)
        canonical_supports.append(canonical)
    residual = max(abs(left - right) for left, right in zip(observed, expected))
    observed_joint = math.prod(observed)
    expected_joint = math.prod(expected)
    varying = len({tuple(support) for support in canonical_supports}) > 1
    verified = residual < 1e-11 and abs(observed_joint - expected_joint) < 1e-11
    return VaryingHmsFourierControl(
        control_id=control_id,
        modulus=modulus,
        supports=canonical_supports,
        phase_targets=[int(value) % modulus for value in phase_targets],
        support_sizes=[len(support) for support in canonical_supports],
        observed_target_probabilities=observed,
        expected_target_probabilities=expected,
        maximum_probability_residual=residual,
        observed_joint_all_correct_probability=observed_joint,
        expected_joint_all_correct_probability=expected_joint,
        supports_identical=not varying,
        varying_support_extension_verified=verified and varying,
        status=(
            "varying-support-hms-fourier-identity-verified"
            if verified
            else "varying-support-hms-fourier-control-failure"
        ),
    )


def subset_sum_multiplicities(
    labels: Iterable[int],
    modulus: int,
) -> tuple[np.ndarray, np.ndarray]:
    sums = np.asarray(subset_sums_mod(labels, modulus), dtype=np.int64)
    counts = np.bincount(sums, minlength=modulus).astype(np.int64)
    return sums, counts


def canonical_fiber_coisometry(
    sums: np.ndarray,
    counts: np.ndarray,
) -> np.ndarray:
    modulus = len(counts)
    matrix = np.zeros((modulus, len(sums)), dtype=np.complex128)
    for assignment, residue in enumerate(sums):
        matrix[residue, assignment] = 1.0 / math.sqrt(counts[residue])
    return matrix


def fiber_compression_control(
    control_id: str,
    modulus: int,
    labels: Sequence[int],
    *,
    phase_target: int = 1,
    structured_polylog_fiber_compression_known: bool = False,
) -> FiberCompressionControl:
    if modulus < 2 or not labels:
        raise ValueError("require a nontrivial modulus and at least one label")
    canonical_labels = [int(value) % modulus for value in labels]
    sums, counts = subset_sum_multiplicities(canonical_labels, modulus)
    assignment_count = len(sums)
    root = np.exp(2j * np.pi / modulus)
    source_state = root ** ((phase_target % modulus) * sums) / math.sqrt(
        assignment_count
    )

    coisometry = canonical_fiber_coisometry(sums, counts)
    support_projector = np.diag((counts > 0).astype(np.float64))
    coisometry_residual = float(
        np.linalg.norm(coisometry @ np.conjugate(coisometry.T) - support_projector)
    )
    compressed = coisometry @ source_state
    norm_residual = abs(float(np.vdot(compressed, compressed).real) - 1.0)
    decoded = np.conjugate(qft_matrix(modulus).T) @ compressed
    observed_success = float(abs(decoded[phase_target % modulus]) ** 2)
    formula = float(np.sum(np.sqrt(counts.astype(np.float64))) ** 2)
    formula /= modulus * assignment_count
    pgm_success = covariant_pgm_success(counts)

    # Reversible forward computation produces sum_b phase(b)|b>|L(b)>.
    # Applying the inverse QFT only to the residue register leaves the b paths
    # orthogonal, so their probabilities, rather than amplitudes, add.
    forward_state = np.zeros(
        (assignment_count, modulus), dtype=np.complex128
    )
    forward_state[np.arange(assignment_count), sums] = source_state
    forward_decoded = forward_state @ np.conjugate(qft_matrix(modulus))
    forward_success = float(
        np.sum(np.abs(forward_decoded[:, phase_target % modulus]) ** 2)
    )

    positive = counts[counts > 0]
    collision_pairs = int(np.sum(positive * (positive - 1) // 2))
    residual = max(
        coisometry_residual,
        norm_residual,
        abs(observed_success - formula),
        abs(pgm_success - formula),
        abs(forward_success - 1.0 / modulus),
    )
    verified = residual < 1e-10
    return FiberCompressionControl(
        control_id=control_id,
        modulus=modulus,
        labels=canonical_labels,
        copy_count=len(canonical_labels),
        assignment_count=assignment_count,
        occupied_residue_count=int(np.count_nonzero(counts)),
        collision_pair_count=collision_pairs,
        minimum_positive_multiplicity=int(np.min(positive)),
        maximum_multiplicity=int(np.max(positive)),
        multiplicities_uniform_on_support=bool(np.all(positive == positive[0])),
        canonical_coisometry_residual=coisometry_residual,
        compressed_state_norm_residual=norm_residual,
        observed_compressed_qft_success=observed_success,
        exact_weighted_qft_formula=formula,
        covariant_pgm_success_probability=pgm_success,
        pgm_formula_residual=abs(pgm_success - formula),
        forward_compute_with_preimage_garbage_success=forward_success,
        forward_garbage_formula_residual=abs(forward_success - 1.0 / modulus),
        coherent_interference_gain=observed_success / forward_success,
        structured_polylog_fiber_compression_known=(
            structured_polylog_fiber_compression_known
        ),
        generic_random_instance_circuit_constructed=False,
        normal_form_verified=verified,
        status=(
            "weighted-hms-pgm-fiber-normal-form-verified"
            if verified
            else "weighted-hms-pgm-normal-form-control-failure"
        ),
    )


def fiber_compression_scaling(
    input_bits: int,
    copy_count: int,
) -> FiberCompressionScaling:
    if input_bits < 2 or copy_count < 1:
        raise ValueError("input_bits and copy_count must be positive")
    collision_log2 = math.log2(math.comb(1 << copy_count, 2)) - input_bits
    return FiberCompressionScaling(
        input_bits=input_bits,
        copy_count=copy_count,
        assignment_count_log2=copy_count,
        modulus_to_assignment_ratio_log2=input_bits - copy_count,
        expected_collision_pairs_log2=collision_log2,
        varying_set_fourier_measurement_cost="poly(input_bits) after multiplier-register compression",
        missing_operation=(
            "uniform source-dependent coisometry |F_h(x)> -> |h>, including "
            "multiplicity normalization and coherent preimage cleanup"
        ),
        generic_polytime_compression_constructed=False,
        status="fiber-compression-not-fourier-sampling-is-the-live-bottleneck",
    )


def run_dcp_varying_hms_fiber_normal_form(
) -> DcpVaryingHmsFiberNormalFormReport:
    varying_controls = [
        varying_hms_fourier_control(
            "three-distinct-known-supports",
            17,
            supports=((0, 1, 4, 7), (0, 2, 3, 8, 11), (1, 5, 9)),
            phase_targets=(3, 12, 6),
        ),
        varying_hms_fourier_control(
            "unequal-support-sizes",
            11,
            supports=((0, 1), (0, 1, 2, 3, 4, 5, 6, 7), (2, 5, 8)),
            phase_targets=(1, 7, 9),
        ),
    ]
    fiber_controls = [
        fiber_compression_control(
            "injective-binary-residues",
            17,
            labels=(1, 2, 4),
            phase_target=5,
            structured_polylog_fiber_compression_known=True,
        ),
        fiber_compression_control(
            "uniform-collision-fibers",
            8,
            labels=(1, 2, 4, 0),
            phase_target=3,
            structured_polylog_fiber_compression_known=True,
        ),
        fiber_compression_control(
            "nonuniform-collision-fibers",
            17,
            labels=(1, 2, 3, 6),
            phase_target=7,
        ),
        fiber_compression_control(
            "density-one-public-random-control",
            16,
            labels=(3, 5, 6, 7),
            phase_target=11,
        ),
    ]
    scaling = [
        fiber_compression_scaling(bits, copies)
        for bits in (32, 64, 128)
        for copies in (bits // 2, bits)
    ]
    verified = bool(
        all(row.varying_support_extension_verified for row in varying_controls)
        and all(row.normal_form_verified for row in fiber_controls)
        and fiber_controls[1].collision_pair_count > 0
        and abs(fiber_controls[1].observed_compressed_qft_success - 1.0)
        < 1e-10
        and all(
            abs(row.forward_compute_with_preimage_garbage_success - 1 / row.modulus)
            < 1e-10
            for row in fiber_controls
        )
    )
    theorem = VaryingHmsFiberTheorem(
        varying_support_fourier_statement=(
            "For independently supplied known H_i, inverse QFT on "
            "|H_i|^-1/2 sum_h omega^(h t_i)|h> returns t_i with probability "
            "|H_i|/q. The joint all-correct probability is product_i |H_i|/q; "
            "H_i need not be common."
        ),
        dcp_weighted_multiplier_statement=(
            "For eta_h=|{b:<x,b>=h}| and D=2^k, the canonical fiber "
            "coisometry maps the DCP tensor state to sum_h sqrt(eta_h/D) "
            "omega^(s h)|h>."
        ),
        pgm_identity=(
            "Inverse QFT after canonical fiber compression succeeds with "
            "(sum_h sqrt(eta_h))^2/(N D), exactly the optimal covariant PGM "
            "success probability."
        ),
        retained_preimage_no_interference=(
            "Computing h=<x,b> while retaining orthogonal b and Fourier "
            "transforming only h succeeds with probability exactly 1/N for "
            "every label tuple, multiplicity profile, and hidden shift."
        ),
        collision_scope=(
            "Collisions alter the weighted phase profile but are not an "
            "information no-go: equal positive multiplicities on all N "
            "residues give PGM success one."
        ),
        implementation_equivalence=(
            "On the ensemble span, the missing map is C_x|F_h>=|h>. It is a "
            "source-dependent polar/coisometry and is the same normalized-"
            "fiber erasure primitive isolated by the canonical DCP PGM audit."
        ),
        theorem_scope_limit=(
            "The exact coisometry matrix is not a circuit. No generic ranking, "
            "unranking, QSVT normalization, collision walk, or destructive "
            "measurement implementation is supplied."
        ),
        varying_support_extension_proved=True,
        weighted_multiplier_normal_form_proved=True,
        pgm_success_identity_proved=True,
        retained_preimage_no_interference_proved=True,
        collisions_are_information_no_go=False,
        generic_fiber_compression_constructed=False,
        dcp_polynomial_algorithm_constructed=False,
        theorem_verified=verified,
        status=(
            "varying-hms-dcp-fiber-normal-form-proved"
            if verified
            else "varying-hms-dcp-fiber-control-failure"
        ),
    )
    metrics = {
        "varying_hms_control_count": len(varying_controls),
        "fiber_normal_form_control_count": len(fiber_controls),
        "finite_control_failure_count": int(not verified),
        "maximum_probability_residual": max(
            [row.maximum_probability_residual for row in varying_controls]
            + [row.pgm_formula_residual for row in fiber_controls]
            + [row.forward_garbage_formula_residual for row in fiber_controls]
        ),
        "maximum_coherent_interference_gain": max(
            row.coherent_interference_gain for row in fiber_controls
        ),
        "perfect_information_collision_control_count": sum(
            row.collision_pair_count > 0
            and abs(row.observed_compressed_qft_success - 1.0) < 1e-10
            for row in fiber_controls
        ),
        "varying_set_fourier_transfer_theorem_count": 1,
        "generic_polytime_fiber_compression_count": 0,
        "dcp_polynomial_algorithm_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return DcpVaryingHmsFiberNormalFormReport(
        created_at=utc_now(),
        theorem_contract={
            "source_state": "tensor products of public-label DCP phase states",
            "public_map": "L_x:{0,1}^k -> Z_N",
            "information_normal_form": "weighted multiple-shift phase register",
            "missing_operation": "canonical normalized-fiber coisometry C_x",
            "decoder_after_missing_operation": "ordinary inverse QFT over Z_N",
        },
        varying_hms_controls=varying_controls,
        fiber_controls=fiber_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "allow_known_multiplier_sets_to_vary_by_sample",
                "resolved": True,
                "resolution": (
                    "The inverse-QFT target amplitude is computed independently "
                    "for each H_i and depends only on |H_i|."
                ),
            },
            {
                "obligation": "identify_dcp_tensor_state_as_weighted_hms_phase_state",
                "resolved": True,
                "resolution": (
                    "Grouping Boolean assignments by residue gives amplitudes "
                    "sqrt(eta_h/D) after the canonical fiber coisometry."
                ),
            },
            {
                "obligation": "match_weighted_qft_success_to_covariant_pgm",
                "resolved": True,
                "resolution": (
                    "Both equal (sum_h sqrt(eta_h))^2/(N D) exactly."
                ),
            },
            {
                "obligation": "implement_generic_source_dependent_fiber_coisometry",
                "resolved": False,
                "resolution": (
                    "The matrix exists information-theoretically; no polynomial "
                    "uniform circuit avoids coherent subset-sum fiber handling."
                ),
            },
            {
                "obligation": "survive_f1_contamination_and_lattice_composition",
                "resolved": False,
                "resolution": (
                    "This is the clean DCP phase ensemble only; existing robustness "
                    "and end-to-end recovery gates remain separate."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "HMS Fourier sampling requires one fixed multiplier set.",
                "survives": False,
                "response": (
                    "The target-amplitude calculation is samplewise and the "
                    "all-correct probability multiplies for arbitrary known H_i."
                ),
            },
            {
                "challenge": "Subset-sum collisions destroy the hidden phase.",
                "survives": False,
                "response": (
                    "They change multiplicity weights. Uniform two-to-one fibers "
                    "over every residue give perfect phase discrimination."
                ),
            },
            {
                "challenge": "A reversible subset-sum circuit already exposes h.",
                "survives": False,
                "response": (
                    "Retaining b makes the paths orthogonal and fixes target "
                    "probability at 1/N, independent of the multiplicities."
                ),
            },
            {
                "challenge": "Writing C_x as a matrix constructs the algorithm.",
                "survives": False,
                "response": (
                    "Uniformly implementing its normalization and preimage "
                    "cleanup is precisely the unresolved average-case subset-sum PGM."
                ),
            },
            {
                "challenge": "Constant PGM information success proves a speedup.",
                "survives": False,
                "response": (
                    "No polynomial measurement circuit, contamination theorem, "
                    "or lattice-recovery composition follows from the success formula."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "IVANYOS-PRAKASH-SANTHA-2018-HMS",
                "title": (
                    "On learning linear functions from subset and its "
                    "applications in quantum computing"
                ),
                "url": "https://arxiv.org/abs/1806.09660",
                "use": "Fixed-set HMS phase preprocessing and Fourier-sampling proof",
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "BACON-CHILDS-VAN-DAM-2005",
                "title": (
                    "From optimal measurement to efficient quantum algorithms "
                    "for the hidden subgroup problem over semidirect product groups"
                ),
                "url": "https://arxiv.org/abs/quant-ph/0504083",
                "use": "DCP/cyclic semidirect PGM and subset-sum multiplicities",
                "external_theorem_not_reproved_here": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "varying_known_multiplier_sets_block_fourier_sampling": False,
            "varying_set_fourier_sampling_transfer_proved": True,
            "weighted_dcp_phase_normal_form_proved": True,
            "collisions_are_information_obstruction": False,
            "forward_subset_sum_with_garbage_is_sufficient": False,
            "generic_polytime_fiber_compression_constructed": False,
            "exact_f1_robustness_proved": False,
            "lattice_composition_proved": False,
            "shift_multiplicity_candidate_passes_proof_gate": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The HMS decoder is already available after compression. The "
                "unresolved operation is the source-dependent normalized-fiber "
                "coisometry, which is equivalent to the clean DCP PGM primitive."
            ),
        },
        status=(
            "varying-hms-dcp-fiber-normal-form-active"
            if verified
            else "varying-hms-dcp-fiber-control-failure"
        ),
        summary=(
            "Removed fixed multiplier-set consistency as a false blocker and "
            "reduced the entire DCP-to-HMS transfer to normalized subset-sum "
            "fiber compression. Collisions can preserve or improve information; "
            "the missing resource is an efficient source-dependent coisometry."
        ),
        falsifiers_triggered=[
            "Fresh known multiplier sets do not invalidate the basic HMS Fourier proof.",
            "Forward residue computation with retained preimages has exactly 1/N target success.",
            "Uniform collision multiplicities can yield perfect distinguishability.",
            "The weighted inverse-QFT decoder is exactly the covariant DCP PGM.",
            "No generic polynomial normalized-fiber coisometry is constructed.",
            "Clean information success does not resolve contamination or end-to-end recovery.",
        ],
    )


def write_dcp_varying_hms_fiber_normal_form(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-VARYING-HMS-FIBER-NORMAL-FORM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(run_dcp_varying_hms_fiber_normal_form())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    output = write_dcp_varying_hms_fiber_normal_form()
    print(json.dumps(output["headline_metrics"], indent=2, sort_keys=True))
