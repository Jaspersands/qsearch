"""Central Fourier bridge for native raw branch-character concentration.

The raw/polar matched-filter boundary left one quantitative escape: the raw
convolution could concentrate on singular sectors where polar whitening makes
a large correction.  A tempting identification of that concentration with
the noncentral orientation block ``F_nu`` is false for the actual right
convolution.  This module derives the correct operator.

Let ``R_h=direct_sum_e sigma_e(h)`` be the orientation-controlled source
representation, let ``E=|+>_e tensor I_C``, and ignore the fixed output Walsh
unitary.  The native raw field is

    K_h = R_h E.

For an irrep ``nu`` of dimension ``d_nu``, define the central compression

    Q_nu = E^* Pi_nu^(R) E
         = d_nu/|G| sum_h chi_nu(h^-1) E^* R_h E.          (1)

It is a positive contraction.  The normalized right-convolution multiplier

    M_nu = |G|^-1/2 sum_h rho_nu(h^-1) tensor K_h

obeys the exact conjugacy-twirl identity

    M_nu^* M_nu = |G|/d_nu^2 I_(d_nu) tensor Q_nu.        (2)

Consequently the raw convolution concentration is

    kappa = max_nu |G|/d_nu^2 ||Q_nu||.                  (3)

The older orientation block remains useful only through a trace identity. If
``F_nu=2^-k sum_e Inv(V_nu tensor sigma_e)``, then

    Tr(Q_nu)=d_nu Tr(F_nu),
    p_nu=Tr(Q_nu)/D=d_nu Tr(F_nu)/D=Tr(D_nu).             (4)

Thus ``Q_nu`` gives exactly the native raw Fourier-sector mass, but its
spectrum is not the spectrum of ``F_nu``.  Finite controls explicitly reject
that substitution.

Let ``P(n)`` be the partition number.  On sectors

    d_nu > sqrt(n!)/P(n),

equation (3) and ``Q_nu<=I`` imply ``kappa_nu<P(n)^2``.  The natural-sector
mass theorem puts ``1-o(1)`` conditioned native mass on these sectors.  At
``k=ceil(3 log_2(n!))+2``, the polar Gram residual satisfies

    E R <= (n!-1)(3/4)^k,

so the high-dimensional contribution to the whitening correction is bounded
by ``P(n)^2 E R=o(1)``.  Any surviving rescue of the branch-polar decoder must
therefore use coherent alignment with the vanishing-mass low-dimensional
sectors.  Sector mass alone does not bound that coherent cross-sector term,
so this is a localization theorem rather than a complete decoder no-go.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_branch_character_naimark_autocorrelation_fourier_boundary import (
    nonabelian_fourier_multiplier,
)
from self_dual_wreath_branch_character_raw_polar_matched_filter_boundary import (
    raw_candidate_relative_convolution,
)
from self_dual_wreath_joint_character_natural_sector_mass import (
    orientation_averaged_target_law,
    partition_number,
)
from self_dual_wreath_orientation_fourier_reduction import (
    Label,
    Partition,
    Permutation,
    _source_representation_rows,
    compressed_fourier_block,
    single_label_compressed_overlap_rows,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_branch_character_raw_concentration_central_fourier_bridge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-RAW-CONCENTRATION-"
    "CENTRAL-FOURIER-BRIDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CentralRawSectorControl:
    partition: Partition
    irrep_dimension: int
    carrier_dimension: int
    minimum_central_compression_eigenvalue: float
    maximum_central_compression_eigenvalue: float
    central_compression_is_positive_contraction: bool
    multiplier_gram_identity_residual: float
    central_to_orientation_trace_residual: float
    native_sector_probability: float
    expected_native_sector_probability: float
    native_sector_probability_residual: float
    raw_sector_concentration: float
    predicted_raw_sector_concentration: float
    raw_sector_concentration_residual: float
    naive_noncentral_F_gram_residual: float
    naive_noncentral_F_substitution_valid: bool
    status: str


@dataclass(frozen=True)
class CentralRawConcentrationControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    group_order: int
    source_pair_count: int
    carrier_dimension: int
    native_sector_probability_sum: float
    raw_convolution_concentration: float
    predicted_raw_convolution_concentration: float
    global_concentration_residual: float
    maximum_multiplier_gram_identity_residual: float
    maximum_trace_bridge_residual: float
    maximum_native_sector_probability_residual: float
    naive_noncentral_F_failure_count: int
    exact_central_fourier_bridge_verified: bool
    sector_controls: list[CentralRawSectorControl]
    status: str


@dataclass(frozen=True)
class NaturalBulkConcentrationScaling:
    n: int
    log2_group_order: float
    copy_count: int
    partition_count_decimal: str
    log2_low_dimension_threshold: float
    log2_high_sector_raw_concentration_upper_bound: float
    log2_polar_gram_residual_upper_bound: float
    log2_high_sector_whitening_correction_upper_bound: float
    natural_high_dimension_sector_mass_tends_to_one: bool
    high_sector_whitening_correction_tends_to_zero: bool
    low_sector_coherent_alignment_bounded: bool
    full_branch_polar_decoder_no_go_proved: bool
    status: str


@dataclass(frozen=True)
class CentralRawConcentrationTheorem:
    central_compression: str
    multiplier_gram: str
    concentration: str
    orientation_trace_bridge: str
    native_sector_mass: str
    natural_bulk_bound: str
    remaining_boundary: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CentralRawConcentrationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CentralRawConcentrationTheorem
    finite_controls: list[CentralRawConcentrationControl]
    scaling_records: list[NaturalBulkConcentrationScaling]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _inverse_permutation(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for source, target in enumerate(permutation):
        output[target] = source
    return tuple(output)


def _kron_all(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    output = np.asarray([[1.0]], dtype=complex)
    for matrix in matrices:
        output = np.kron(output, matrix)
    return output


def compressed_source_representation_rows(
    labels: tuple[Label, ...],
) -> dict[Permutation, np.ndarray]:
    """Return ``E^*R_hE`` for the uniform orientation embedding."""

    if not labels:
        raise ValueError("at least one source pair is required")
    tables = [dict(single_label_compressed_overlap_rows(label)) for label in labels]
    group = tuple(tables[0])
    return {
        permutation: _kron_all(
            tuple(table[permutation] for table in tables)
        )
        for permutation in group
    }


def central_compressed_isotypic_block(
    target: Partition,
    labels: tuple[Label, ...],
) -> np.ndarray:
    """Return the positive contraction ``Q_nu=E^*Pi_nu E`` in (1)."""

    rows = _source_representation_rows(target)
    compressed = compressed_source_representation_rows(labels)
    if tuple(rows) != tuple(compressed):
        raise ArithmeticError("target and source rows enumerate different groups")
    dimension = hook_length_dimension(target)
    order = len(rows)
    carrier = next(iter(compressed.values())).shape[0]
    block = sum(
        (
            np.trace(rows[_inverse_permutation(permutation)])
            * compressed[permutation]
            for permutation in rows
        ),
        np.zeros((carrier, carrier), dtype=complex),
    )
    block *= dimension / order
    return (block + block.conj().T) / 2.0


def audit_central_raw_concentration(
    control_id: str,
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-9,
) -> CentralRawConcentrationControl:
    convolution, group, fields = raw_candidate_relative_convolution(labels)
    order = len(group)
    carrier = next(iter(fields.values())).shape[1]
    n = len(group[0])
    expected_law = orientation_averaged_target_law(labels)
    sectors: list[CentralRawSectorControl] = []
    predicted_global = 0.0

    for target in integer_partitions(n):
        dimension = hook_length_dimension(target)
        central = central_compressed_isotypic_block(target, labels)
        eigenvalues = np.linalg.eigvalsh(central)
        positive_contraction = bool(
            eigenvalues[0] >= -100 * tolerance
            and eigenvalues[-1] <= 1.0 + 100 * tolerance
        )
        multiplier = nonabelian_fourier_multiplier(target, group, fields)
        gram = multiplier.conj().T @ multiplier
        predicted_gram = (
            order
            / dimension**2
            * np.kron(np.eye(dimension, dtype=complex), central)
        )
        gram_residual = float(np.linalg.norm(gram - predicted_gram, ord="fro"))

        orientation = compressed_fourier_block(target, labels)
        trace_residual = abs(
            float(np.trace(central).real)
            - dimension * float(np.trace(orientation).real)
        )
        native_probability = float(np.trace(central).real / carrier)
        expected_probability = float(expected_law[target])
        probability_residual = abs(native_probability - expected_probability)
        actual_concentration = float(np.linalg.eigvalsh(gram)[-1])
        predicted_concentration = float(
            order / dimension**2 * max(0.0, eigenvalues[-1])
        )
        concentration_residual = abs(
            actual_concentration - predicted_concentration
        )

        # This is the tempting but incorrect replacement Q_nu -> F_nu.
        naive_gram = order / dimension**2 * orientation
        naive_residual = float(np.linalg.norm(gram - naive_gram, ord="fro"))
        naive_valid = naive_residual <= 100 * tolerance
        predicted_global = max(predicted_global, predicted_concentration)
        verified = bool(
            positive_contraction
            and gram_residual <= 100 * tolerance
            and trace_residual <= 100 * tolerance
            and probability_residual <= 100 * tolerance
            and concentration_residual <= 100 * tolerance
        )
        sectors.append(
            CentralRawSectorControl(
                partition=target,
                irrep_dimension=dimension,
                carrier_dimension=carrier,
                minimum_central_compression_eigenvalue=float(eigenvalues[0]),
                maximum_central_compression_eigenvalue=float(eigenvalues[-1]),
                central_compression_is_positive_contraction=positive_contraction,
                multiplier_gram_identity_residual=gram_residual,
                central_to_orientation_trace_residual=trace_residual,
                native_sector_probability=native_probability,
                expected_native_sector_probability=expected_probability,
                native_sector_probability_residual=probability_residual,
                raw_sector_concentration=actual_concentration,
                predicted_raw_sector_concentration=predicted_concentration,
                raw_sector_concentration_residual=concentration_residual,
                naive_noncentral_F_gram_residual=naive_residual,
                naive_noncentral_F_substitution_valid=naive_valid,
                status=(
                    "central-raw-sector-bridge-verified"
                    if verified
                    else "central-raw-sector-control-failure"
                ),
            )
        )

    actual_global = float(np.linalg.svd(convolution, compute_uv=False)[0] ** 2)
    global_residual = abs(actual_global - predicted_global)
    probability_sum = sum(row.native_sector_probability for row in sectors)
    naive_failures = sum(
        not row.naive_noncentral_F_substitution_valid for row in sectors
    )
    verified = bool(
        all(row.status == "central-raw-sector-bridge-verified" for row in sectors)
        and abs(probability_sum - 1.0) <= 100 * tolerance
        and global_residual <= 100 * tolerance
        and naive_failures >= 1
    )
    return CentralRawConcentrationControl(
        control_id=control_id,
        n=n,
        labels=labels,
        group_order=order,
        source_pair_count=len(labels),
        carrier_dimension=carrier,
        native_sector_probability_sum=probability_sum,
        raw_convolution_concentration=actual_global,
        predicted_raw_convolution_concentration=predicted_global,
        global_concentration_residual=global_residual,
        maximum_multiplier_gram_identity_residual=max(
            row.multiplier_gram_identity_residual for row in sectors
        ),
        maximum_trace_bridge_residual=max(
            row.central_to_orientation_trace_residual for row in sectors
        ),
        maximum_native_sector_probability_residual=max(
            row.native_sector_probability_residual for row in sectors
        ),
        naive_noncentral_F_failure_count=naive_failures,
        exact_central_fourier_bridge_verified=verified,
        sector_controls=sectors,
        status=(
            "exact-central-raw-concentration-bridge"
            if verified
            else "central-raw-concentration-control-failure"
        ),
    )


def natural_bulk_concentration_scaling(
    n: int,
) -> NaturalBulkConcentrationScaling:
    if n < 4:
        raise ValueError("n must be at least four")
    order = math.factorial(n)
    log_order = math.log2(order)
    copies = math.ceil(3.0 * log_order) + 2
    count = partition_number(n)
    threshold = math.isqrt(order) // count
    if threshold < 1:
        raise ArithmeticError("dimension threshold is trivial")
    inverse_order = 2.0**(-log_order) if log_order < 1074 else 0.0
    log_order_minus_one = log_order + math.log2(1.0 - inverse_order)
    gram_log = log_order_minus_one + copies * math.log2(3.0 / 4.0)
    concentration_log = 2.0 * math.log2(count)
    correction_log = concentration_log + gram_log
    return NaturalBulkConcentrationScaling(
        n=n,
        log2_group_order=log_order,
        copy_count=copies,
        partition_count_decimal=str(count),
        log2_low_dimension_threshold=math.log2(threshold),
        log2_high_sector_raw_concentration_upper_bound=concentration_log,
        log2_polar_gram_residual_upper_bound=gram_log,
        log2_high_sector_whitening_correction_upper_bound=correction_log,
        natural_high_dimension_sector_mass_tends_to_one=True,
        high_sector_whitening_correction_tends_to_zero=True,
        low_sector_coherent_alignment_bounded=False,
        full_branch_polar_decoder_no_go_proved=False,
        status=(
            "high-dimensional-raw-concentration-cannot-rescue-polar-whitening"
            if correction_log < 0
            else "asymptotic-bulk-suppression-not-yet-visible"
        ),
    )


def run_central_raw_concentration_bridge() -> CentralRawConcentrationReport:
    controls = [
        audit_central_raw_concentration(
            "S3-SINGLE-PAIR-CENTRAL-RAW-BRIDGE",
            (((3,), (2, 1)),),
        ),
        audit_central_raw_concentration(
            "S3-THRESHOLD-CENTRAL-RAW-BRIDGE",
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
        ),
    ]
    scaling = [natural_bulk_concentration_scaling(n) for n in (32, 64, 128, 256, 512)]
    verified = bool(
        all(row.exact_central_fourier_bridge_verified for row in controls)
        and scaling[-1].high_sector_whitening_correction_tends_to_zero
        and scaling[-1].log2_high_sector_whitening_correction_upper_bound < 0
    )
    theorem = CentralRawConcentrationTheorem(
        central_compression=(
            "Q_nu=E^*Pi_nu^(R)E is a positive contraction obtained by central "
            "character projection of the uniform-orientation compression."
        ),
        multiplier_gram=(
            "For the actual right convolution, M_nu^*M_nu="
            "|G|/d_nu^2 I_(d_nu) tensor Q_nu."
        ),
        concentration=(
            "||C_K||^2=max_nu |G| ||Q_nu||/d_nu^2."
        ),
        orientation_trace_bridge=(
            "Tr(Q_nu)=d_nu Tr(F_nu), but Q_nu and the noncentral F_nu are not "
            "spectrally interchangeable."
        ),
        native_sector_mass=(
            "p_nu=Tr(Q_nu)/D=d_nu Tr(F_nu)/D=Tr(D_nu), exactly the native "
            "joint-character Fourier-sector law."
        ),
        natural_bulk_bound=(
            "On d_nu>sqrt(|G|)/P(n), raw concentration is below P(n)^2; "
            "therefore its product with the natural polar Gram residual vanishes."
        ),
        remaining_boundary=(
            "Only coherent alignment with the vanishing-mass low-dimensional "
            "sectors can still rescue the branch-polar whitening correction."
        ),
        scope=(
            "This localizes the remaining concentration escape. It does not bound "
            "cross-sector coherent decoding through the low-dimensional tail, reject "
            "the physical PGM, or prove a classical separation."
        ),
        theorem_verified=verified,
        status=(
            "raw-concentration-localized-to-low-dimensional-coherent-tail"
            if verified
            else "central-raw-concentration-bridge-control-failure"
        ),
    )
    tail = scaling[-1]
    return CentralRawConcentrationReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "identify_exact_raw_convolution_fourier_concentration",
                "resolved": verified,
                "resolution": (
                    "The exact multiplier Gram is the central compression Q_nu, "
                    "with the dimension-weighted norm formula in equation (3)."
                ),
            },
            {
                "obligation": "link_raw_concentration_to_native_sector_mass",
                "resolved": verified,
                "resolution": (
                    "Tr(Q_nu)/D equals both the orientation recoupling law and "
                    "Tr(D_nu)."
                ),
            },
            {
                "obligation": "exclude_high_dimensional_bulk_as_whitening_rescue",
                "resolved": verified,
                "resolution": (
                    "Q_nu<=I gives kappa_nu<P(n)^2 on 1-o(1) natural mass, and "
                    "P(n)^2 E R tends to zero."
                ),
            },
            {
                "obligation": "bound_low_dimensional_cross_sector_coherence",
                "resolved": False,
                "resolution": (
                    "Vanishing marginal mass does not alone control coherent Fourier "
                    "interference in group-label decoding. A state-weighted alignment "
                    "or trace-distance theorem is still required."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The existing noncentral orientation block F_nu directly gives raw multiplier concentration.",
                "resolved": True,
                "resolution": (
                    "False. Right-convolution squaring conjugacy-twirls the target "
                    "irrep and produces I tensor Q_nu. Finite standard-sector controls "
                    "show a nonzero spectral substitution residual."
                ),
            },
            {
                "objection": "High-dimensional target sectors may still have factorial raw concentration.",
                "resolved": True,
                "resolution": (
                    "Q_nu is a contraction, so |G| ||Q_nu||/d_nu^2<P(n)^2 "
                    "above the natural dimension threshold."
                ),
            },
            {
                "objection": "Vanishing low-sector mass completes a decoder no-go.",
                "resolved": False,
                "resolution": (
                    "Not without controlling coherent interference between Fourier "
                    "sectors in the correct-label amplitude. The report keeps this gate open."
                ),
            },
            {
                "objection": "This rejects the actual multiplicity-whitened physical PGM.",
                "resolved": False,
                "resolution": "The theorem concerns the branch-polar convolution only.",
            },
        ],
        headline_metrics={
            "exact_central_multiplier_gram_theorem_count": int(verified),
            "native_sector_mass_bridge_theorem_count": int(verified),
            "natural_high_sector_concentration_bound_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_central_fourier_bridge_verified for row in controls
            ),
            "naive_noncentral_F_substitution_failure_count": sum(
                row.naive_noncentral_F_failure_count for row in controls
            ),
            "tail_n": tail.n,
            "tail_log2_high_sector_concentration_upper_bound": (
                tail.log2_high_sector_raw_concentration_upper_bound
            ),
            "tail_log2_high_sector_whitening_correction_upper_bound": (
                tail.log2_high_sector_whitening_correction_upper_bound
            ),
            "low_sector_alignment_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "raw_convolution_central_fourier_block_identified": verified,
            "raw_concentration_formula_proved": verified,
            "noncentral_orientation_block_substitution_rejected": verified,
            "native_raw_sector_mass_matches_joint_D_nu_mass": verified,
            "high_dimensional_bulk_can_rescue_branch_polar_whitening": False,
            "low_dimensional_coherent_alignment_bounded": False,
            "full_branch_polar_decoder_rejected": False,
            "actual_physical_pgm_rejected": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Corrected the raw-concentration Fourier bridge: the central compression "
            "Q_nu, not the noncentral orientation block F_nu, controls the multiplier. "
            "The natural high-dimensional bulk cannot supply the whitening rescue; "
            "only the unresolved low-dimensional coherent tail remains."
        ),
        falsifiers_triggered=[
            "The raw multiplier Gram is not a scalar multiple of the existing noncentral F_nu block.",
            "Large raw concentration on the natural high-dimensional bulk cannot offset the proved polar Gram decay.",
            "Vanishing low-dimensional sector mass is insufficient by itself to conclude a full decoder no-go.",
        ],
    )


def write_central_raw_concentration_bridge_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_central_raw_concentration_bridge())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_central_raw_concentration_bridge_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
