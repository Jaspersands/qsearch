"""Normalization no-go for hash-thinned scalar orientation whitening.

The physical joint-character PGM reduces in target sector ``nu`` to the
orientation overlap kernel

    H_nu[e,f] = Tr(E_e E_f)/d_nu,

and affine hash thinning can suppress its off-diagonal Frobenius energy.  That
spectral improvement does not by itself normalize the physical analysis map.
This module charges the missing scale even under the favorable assumption that
the retained kernel is almost scalar.

Let ``q=2^k``, ``D`` be the source carrier dimension, ``r=d_nu``, and let
``N_nu`` be the canonical direct-analysis map.  In orientation rather than
Walsh coordinates,

    N_nu^* N_nu = I_r tensor H_nu/(qD).                  (1)

Let a full-rank affine hash retain ``S`` of density ``p`` and size ``s=pq``.
Conditioning on successful hash acceptance costs the available polynomial
``1/sqrt(p)`` amplitude amplification and gives

    N_(nu,S)^* N_(nu,S) = I_r tensor H_(nu,S)/(sD).      (2)

The diagonal mean has an exact physical interpretation.  If
``p_nu=Tr(D_nu)`` is the unthinned target-sector probability, then

    m_nu = Tr(H_nu)/q = D p_nu/r^2.                     (3)

Suppose the hash succeeds perfectly at its intended task and a retained bulk
obeys ``H_(nu,S) <= (1+epsilon)m_nu I``.  On the natural high-dimensional
sector event

    r > sqrt(n!)/P(n),

we have ``p_nu<=1`` and therefore

    m_nu <= D P(n)^2/n!.

At the information threshold ``q>=n!``, every retained canonical singular
value on that bulk is at most

    sigma <= sqrt(1+epsilon) P(n)/(n! sqrt(p)).           (4)

A bounded singular-value polynomial implementing the polar on a nonzero bulk
singular value must change from zero at the origin to approximately one at
``sigma``.  Bernstein's inequality therefore gives degree

    Omega(n! sqrt(p)/P(n)).                              (5)

For every inverse-polynomial hash density this is factorial up to
``exp(O(sqrt(n)))`` factors.  Hashing may improve condition number and retain
information, but the canonical physical top block is still too weak for
scalar whitening by generic amplitude amplification/QSVT.

Uniform random affine translations preserve every target-sector mass in
expectation because the orientation hash projector commutes with the diagonal
isotypic projector and every orientation is retained with probability ``p``.
Since total hash acceptance is exactly ``p``, the conditioned target law is
unchanged on average.  The existing natural high-row theorem therefore
survives a public random hash with high probability; rare low-row sectors do
not rescue this architecture.

This theorem rejects hash thinning followed by canonical scalar whitening.
It does not reject a direct structured polar of the orientation kernel, a
multi-round multiplicity transform, or the actual physical PGM implemented by
another access architecture.
"""

from __future__ import annotations

import json
import itertools
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_joint_character_analysis_map_normalization import (
    _direct_polar,
    joint_character_analysis_maps,
)
from self_dual_wreath_joint_character_multiplicity_gram import (
    Label,
    Partition,
    orientation_overlap_kernel,
    predicted_joint_multiplicity_operator,
    walsh_matrix,
)
from self_dual_wreath_joint_character_natural_sector_mass import partition_number
from self_dual_wreath_orientation_fourier_reduction import _w4_collision_free_labels
from self_dual_wreath_orientation_kernel_hash_thinning import affine_hash_mask


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_kernel_hash_normalization_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-KERNEL-HASH-NORMALIZATION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class HashConditionedAnalysisControl:
    control_id: str
    n: int
    target: Partition
    labels: tuple[Label, ...]
    irrep_dimension: int
    orientation_count: int
    source_carrier_dimension: int
    hash_output_bits: int
    hash_row_masks: tuple[int, ...]
    hash_offset: int
    retained_orientation_count: int
    hash_density: float
    enumerated_full_rank_hash_fiber_count: int
    maximum_orientation_inclusion_probability_residual: float
    conditioned_target_mass_transfer_residual: float
    target_sector_probability: float
    orientation_kernel_diagonal_mean: float
    sector_mass_mean_identity_residual: float
    conditional_analysis_input_dimension: int
    conditional_analysis_output_dimension: int
    conditional_analysis_gram_residual: float
    conditional_polar_scale_invariance_residual: float
    minimum_positive_retained_kernel_eigenvalue: float
    maximum_retained_kernel_eigenvalue: float
    maximum_relative_retained_kernel_deviation: float
    minimum_positive_conditional_singular_value: float
    maximum_conditional_singular_value: float
    generic_scalar_whitening_degree_lower_bound: int
    exact_hash_conditioned_normalization_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalHashNormalizationScaling:
    n: int
    log2_group_order: float
    information_threshold_copy_count: int
    hash_output_bits: int
    log2_hash_density: float
    partition_count_decimal: str
    relative_spectral_window: float
    log2_high_row_canonical_singular_value_upper_bound: float
    log2_generic_scalar_whitening_degree_lower_bound: float
    inverse_polynomial_hash_acceptance: bool
    ideal_almost_scalar_kernel_granted: bool
    random_hash_preserves_target_law_in_expectation: bool
    natural_high_row_mass_survives_random_hash: bool
    generic_scalar_whitening_polynomial: bool
    direct_structured_orientation_polar_ruled_out: bool
    status: str


@dataclass(frozen=True)
class HashNormalizationNoGoTheorem:
    orientation_basis_gram: str
    conditioned_hash_gram: str
    mean_sector_identity: str
    high_row_scale: str
    generic_degree_boundary: str
    random_hash_mass_transfer: str
    route_decision: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class HashNormalizationNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: HashNormalizationNoGoTheorem
    finite_controls: list[HashConditionedAnalysisControl]
    scaling_records: list[NaturalHashNormalizationScaling]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _selected_orientation_columns(
    irrep_dimension: int,
    orientation_count: int,
    mask: np.ndarray,
) -> list[int]:
    selected = np.flatnonzero(mask)
    return [
        row * orientation_count + int(orientation)
        for row in range(irrep_dimension)
        for orientation in selected
    ]


def _binary_row_rank(rows: tuple[int, ...]) -> int:
    pivots: dict[int, int] = {}
    for value in rows:
        reduced = value
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = reduced
                break
            reduced ^= pivots[pivot]
    return len(pivots)


def _active_full_rank_hash_fiber(
    bit_count: int,
    output_bits: int,
    kernel: np.ndarray,
    tolerance: float,
) -> tuple[tuple[int, ...], int, np.ndarray]:
    """Choose a deterministic active full-rank fiber for finite validation."""

    candidates: list[tuple[float, tuple[int, ...], int, np.ndarray]] = []
    for rows in itertools.combinations(range(1, 1 << bit_count), output_bits):
        if _binary_row_rank(rows) != output_bits:
            continue
        for offset in range(1 << output_bits):
            mask = affine_hash_mask(bit_count, rows, offset)
            selected = np.flatnonzero(mask)
            mass = float(np.trace(kernel[np.ix_(selected, selected)]).real)
            if mass > tolerance:
                candidates.append((mass, rows, offset, mask))
    if not candidates:
        raise ValueError("no active full-rank affine hash fiber exists")
    _, rows, offset, mask = max(
        candidates,
        key=lambda item: (item[0], tuple(-value for value in item[1]), -item[2]),
    )
    return rows, offset, mask


def _enumerate_full_rank_hash_fibers(
    bit_count: int,
    output_bits: int,
) -> tuple[np.ndarray, ...]:
    masks = []
    for rows in itertools.product(range(1, 1 << bit_count), repeat=output_bits):
        if _binary_row_rank(rows) != output_bits:
            continue
        for offset in range(1 << output_bits):
            masks.append(affine_hash_mask(bit_count, rows, offset))
    if not masks:
        raise ValueError("full-rank affine hash family is empty")
    return tuple(masks)


def generic_polar_degree_lower_bound(
    singular_value: float,
    *,
    error: float = 0.01,
) -> int:
    """Conservative Bernstein lower bound for scalar polar amplification."""

    if not 0 < singular_value <= 1:
        raise ValueError("singular value must lie in (0,1]")
    if not 0 <= error < 0.5:
        raise ValueError("error must lie in [0,1/2)")
    slope = (1.0 - 2.0 * error) / singular_value
    bernstein_factor = math.sqrt(max(0.0, 1.0 - singular_value**2))
    return max(1, math.floor(slope * bernstein_factor))


def audit_hash_conditioned_analysis(
    n: int,
    target: Partition,
    labels: tuple[Label, ...],
    *,
    hash_output_bits: int,
    control_id: str,
    tolerance: float = 1e-9,
) -> HashConditionedAnalysisControl:
    if hash_output_bits < 1 or hash_output_bits > len(labels):
        raise ValueError("hash output width must lie in [1,copy_count]")
    multiplicity, target_analysis, canonical, _ = joint_character_analysis_maps(
        target,
        labels,
    )
    _, _, projectors = predicted_joint_multiplicity_operator(target, labels)
    dimension = hook_length_dimension(target)
    count = 1 << len(labels)
    carrier = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    kernel = orientation_overlap_kernel(projectors, dimension)
    mean = float(np.trace(kernel).real / count)
    sector_probability = float(np.trace(multiplicity).real)
    mean_identity_residual = abs(
        mean - carrier * sector_probability / dimension**2
    )

    rows, offset, mask = _active_full_rank_hash_fiber(
        len(labels),
        hash_output_bits,
        kernel,
        tolerance,
    )
    retained = int(np.count_nonzero(mask))
    density = retained / count
    if retained != count >> hash_output_bits:
        raise ArithmeticError("chosen full-rank affine hash has wrong fiber size")
    full_rank_masks = _enumerate_full_rank_hash_fibers(
        len(labels),
        hash_output_bits,
    )
    inclusion = np.mean(np.stack(full_rank_masks).astype(float), axis=0)
    inclusion_residual = float(np.max(np.abs(inclusion - density)))
    diagonal = np.diag(kernel).real
    accepted_sector_masses = [
        dimension**2
        / (count * carrier)
        * float(np.dot(mask.astype(float), diagonal))
        for mask in full_rank_masks
    ]
    mass_transfer_residual = abs(
        float(np.mean(accepted_sector_masses)) / density
        - sector_probability
    )

    walsh = walsh_matrix(len(labels))
    orientation_canonical = canonical @ np.kron(
        np.eye(dimension, dtype=complex),
        walsh,
    )
    columns = _selected_orientation_columns(dimension, count, mask)
    conditioned = orientation_canonical[:, columns] / math.sqrt(density)
    selected = np.flatnonzero(mask)
    retained_kernel = kernel[np.ix_(selected, selected)]
    expected_gram = np.kron(
        np.eye(dimension, dtype=complex),
        retained_kernel,
    ) / (retained * carrier)
    gram_residual = float(
        np.linalg.norm(conditioned.conj().T @ conditioned - expected_gram)
    )

    orientation_target = target_analysis @ np.kron(
        np.eye(dimension, dtype=complex),
        walsh,
    )
    restricted_target = orientation_target[:, columns]
    polar_residual = float(
        np.linalg.norm(
            _direct_polar(conditioned, tolerance)
            - _direct_polar(restricted_target, tolerance),
        )
    )
    eigenvalues = np.linalg.eigvalsh(
        (retained_kernel + retained_kernel.conj().T) / 2.0
    ).real
    positive_eigenvalues = eigenvalues[eigenvalues > tolerance]
    if not len(positive_eigenvalues):
        raise ValueError("hash retained no active orientation-kernel mode")
    relative_deviation = float(np.max(np.abs(eigenvalues / mean - 1.0)))
    singular_values = np.linalg.svd(conditioned, compute_uv=False)
    positive_singular_values = singular_values[singular_values > tolerance]
    degree = generic_polar_degree_lower_bound(
        min(1.0, float(positive_singular_values[-1]))
    )
    verified = bool(
        mean_identity_residual <= 100 * tolerance
        and inclusion_residual <= 100 * tolerance
        and mass_transfer_residual <= 100 * tolerance
        and gram_residual <= 100 * tolerance
        and polar_residual <= 100 * tolerance
    )
    return HashConditionedAnalysisControl(
        control_id=control_id,
        n=n,
        target=target,
        labels=labels,
        irrep_dimension=dimension,
        orientation_count=count,
        source_carrier_dimension=carrier,
        hash_output_bits=hash_output_bits,
        hash_row_masks=rows,
        hash_offset=offset,
        retained_orientation_count=retained,
        hash_density=density,
        enumerated_full_rank_hash_fiber_count=len(full_rank_masks),
        maximum_orientation_inclusion_probability_residual=inclusion_residual,
        conditioned_target_mass_transfer_residual=mass_transfer_residual,
        target_sector_probability=sector_probability,
        orientation_kernel_diagonal_mean=mean,
        sector_mass_mean_identity_residual=mean_identity_residual,
        conditional_analysis_input_dimension=dimension * retained,
        conditional_analysis_output_dimension=conditioned.shape[0],
        conditional_analysis_gram_residual=gram_residual,
        conditional_polar_scale_invariance_residual=polar_residual,
        minimum_positive_retained_kernel_eigenvalue=float(positive_eigenvalues[0]),
        maximum_retained_kernel_eigenvalue=float(eigenvalues[-1]),
        maximum_relative_retained_kernel_deviation=relative_deviation,
        minimum_positive_conditional_singular_value=float(
            positive_singular_values[-1]
        ),
        maximum_conditional_singular_value=float(positive_singular_values[0]),
        generic_scalar_whitening_degree_lower_bound=degree,
        exact_hash_conditioned_normalization_verified=verified,
        status=(
            "exact-hash-conditioned-analysis-normalization"
            if verified
            else "hash-conditioned-analysis-control-failure"
        ),
    )


def natural_hash_normalization_scaling(
    n: int,
    *,
    hash_polynomial_degree: int = 8,
    error: float = 0.01,
) -> NaturalHashNormalizationScaling:
    if n < 4 or hash_polynomial_degree < 1:
        raise ValueError("invalid scaling parameters")
    log_order = math.log2(math.factorial(n))
    copies = math.ceil(log_order)
    hash_bits = min(copies, math.ceil(hash_polynomial_degree * math.log2(n)))
    log_density = -float(hash_bits)
    count = partition_number(n)
    window = n ** -0.125
    log_sigma = (
        0.5 * math.log2(1.0 + window)
        + math.log2(count)
        - log_order
        - 0.5 * log_density
    )
    log_degree = (
        math.log2(1.0 - 2.0 * error)
        - log_sigma
        + 0.5 * math.log2(max(1e-300, 1.0 - min(1.0, 2.0 ** (2 * log_sigma))))
    )
    return NaturalHashNormalizationScaling(
        n=n,
        log2_group_order=log_order,
        information_threshold_copy_count=copies,
        hash_output_bits=hash_bits,
        log2_hash_density=log_density,
        partition_count_decimal=str(count),
        relative_spectral_window=window,
        log2_high_row_canonical_singular_value_upper_bound=log_sigma,
        log2_generic_scalar_whitening_degree_lower_bound=log_degree,
        inverse_polynomial_hash_acceptance=True,
        ideal_almost_scalar_kernel_granted=True,
        random_hash_preserves_target_law_in_expectation=True,
        natural_high_row_mass_survives_random_hash=True,
        generic_scalar_whitening_polynomial=False,
        direct_structured_orientation_polar_ruled_out=False,
        status="hash-scalar-whitening-factorial-normalization-boundary",
    )


def run_hash_normalization_no_go() -> HashNormalizationNoGoReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    w4_labels = _w4_collision_free_labels()[0]
    controls = [
        audit_hash_conditioned_analysis(
            3,
            (3,),
            threshold_labels,
            hash_output_bits=1,
            control_id="W3-THRESHOLD-TRIVIAL-HASH",
        ),
        audit_hash_conditioned_analysis(
            3,
            (2, 1),
            threshold_labels,
            hash_output_bits=1,
            control_id="W3-THRESHOLD-STANDARD-HASH",
        ),
        audit_hash_conditioned_analysis(
            4,
            (3, 1),
            w4_labels,
            hash_output_bits=1,
            control_id="W4-COLLISION-FREE-31-HASH",
        ),
    ]
    scaling = [
        natural_hash_normalization_scaling(n)
        for n in (16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_hash_conditioned_normalization_verified for row in controls
    )
    verified = bool(
        failures == 0
        and scaling[-1].log2_generic_scalar_whitening_degree_lower_bound > 100
        and not scaling[-1].generic_scalar_whitening_polynomial
    )
    theorem = HashNormalizationNoGoTheorem(
        orientation_basis_gram=(
            "After undoing the branch Walsh transform, N_nu^*N_nu="
            "I_(d_nu) tensor H_nu/(q dim(C))."
        ),
        conditioned_hash_gram=(
            "For a full-rank affine fiber S of density p, conditioning on hash "
            "acceptance gives N_(nu,S)^*N_(nu,S)=I tensor H_(nu,S)/(|S|dim(C))."
        ),
        mean_sector_identity=(
            "m_nu=Tr(H_nu)/q=dim(C) Tr(D_nu)/d_nu^2 exactly."
        ),
        high_row_scale=(
            "Even granting H_(nu,S)<=(1+epsilon)m_nu I, natural high-row sectors "
            "have canonical singular scale at most sqrt(1+epsilon)P(n)/(n!sqrt(p))."
        ),
        generic_degree_boundary=(
            "Bounded singular-value scalar whitening requires degree "
            "Omega(n!sqrt(p)/P(n)), factorial for inverse-polynomial p."
        ),
        random_hash_mass_transfer=(
            "Uniform affine translation retains every orientation with probability p; "
            "commutation with target isotypic projection preserves the target law in expectation."
        ),
        route_decision=(
            "Hash thinning may improve H_nu conditioning but cannot turn canonical "
            "scalar whitening into a polynomial physical PGM decoder."
        ),
        scope=(
            "The lower bound applies to conditioned canonical access plus a bounded "
            "singular-value polynomial. Direct structured orientation polars and other "
            "multiplicity architectures remain open."
        ),
        theorem_verified=verified,
        status=(
            "orientation-hash-scalar-whitening-asymptotically-rejected"
            if verified
            else "orientation-hash-normalization-control-failure"
        ),
    )
    tail = scaling[-1]
    return HashNormalizationNoGoReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "charge_hash_conditioning_in_physical_analysis_map",
                "resolved": verified,
                "resolution": (
                    "The exact conditioned Gram is H_S/(|S|dim(C)); inverse-polynomial "
                    "acceptance removes only the explicit hash density."
                ),
            },
            {
                "obligation": "relate_kernel_diagonal_scale_to_target_sector_mass",
                "resolved": verified,
                "resolution": "m_nu=dim(C)p_nu/d_nu^2 follows by tracing D_nu.",
            },
            {
                "obligation": "test_hash_almost_scalar_bulk_as_polynomial_decoder",
                "resolved": verified,
                "resolution": (
                    "Rejected even under the ideal almost-scalar premise: canonical "
                    "singular amplitudes remain factorially small on natural high rows."
                ),
            },
            {
                "obligation": "construct_direct_structured_orientation_polar",
                "resolved": False,
                "resolution": (
                    "Scalar rescaling leaves the mathematical polar unchanged, so a "
                    "representation-specific circuit could bypass generic amplification."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "An almost-scalar H_nu makes whitening automatically efficient.",
                "resolved": True,
                "resolution": (
                    "Condition number and access normalization are distinct. The entire "
                    "almost-scalar spectrum sits at factorially small canonical amplitude."
                ),
            },
            {
                "objection": "Conditioning on an inverse-polynomial hash removes the small scale.",
                "resolved": True,
                "resolution": (
                    "It gains only 1/sqrt(p); the remaining lower bound is "
                    "Omega(n!sqrt(p)/P(n))."
                ),
            },
            {
                "objection": "The hash can redirect all accepted mass to rare low-row sectors.",
                "resolved": True,
                "resolution": (
                    "For a public uniformly translated affine hash, each orientation is "
                    "included with probability p and total acceptance is exactly p, so "
                    "the conditioned target law is preserved in expectation."
                ),
            },
            {
                "objection": "This is a circuit lower bound for the physical PGM.",
                "resolved": False,
                "resolution": (
                    "No. It rejects only canonical hash access followed by generic scalar whitening."
                ),
            },
        ],
        headline_metrics={
            "exact_hash_conditioned_gram_theorem_count": int(verified),
            "kernel_mean_sector_mass_identity_count": int(verified),
            "hash_scalar_whitening_normalization_no_go_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "tail_n": tail.n,
            "tail_log2_canonical_singular_upper_bound": (
                tail.log2_high_row_canonical_singular_value_upper_bound
            ),
            "tail_log2_generic_degree_lower_bound": (
                tail.log2_generic_scalar_whitening_degree_lower_bound
            ),
            "direct_structured_orientation_polar_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "hash_conditioned_canonical_gram_identified": verified,
            "kernel_mean_linked_to_physical_sector_mass": verified,
            "natural_high_row_mass_survives_random_public_hash": verified,
            "ideal_almost_scalar_hash_kernel_would_enable_scalar_whitening": False,
            "canonical_hash_scalar_whitening_polynomial": False,
            "canonical_hash_scalar_whitening_rejected": verified,
            "direct_structured_orientation_polar_ruled_out": False,
            "actual_physical_pgm_rejected": False,
            "polynomial_joint_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Charged the missing physical scale in orientation-kernel hash thinning. "
            "Even an ideal almost-scalar retained kernel has factorially small canonical "
            "singular amplitudes on natural high-row mass, so generic scalar whitening "
            "is not a polynomial decoder."
        ),
        falsifiers_triggered=[
            "Almost-scalar orientation kernels do not imply efficiently normalized physical analysis maps.",
            "Inverse-polynomial affine hash acceptance cannot remove the factorial Schur-row amplitude scale.",
            "Further hash-thinning work is useful only if paired with a genuinely structured direct polar, not scalar QSVT whitening.",
        ],
    )


def write_hash_normalization_no_go_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_hash_normalization_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_hash_normalization_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
