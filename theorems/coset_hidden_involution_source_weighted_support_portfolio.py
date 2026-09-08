"""Source-ranked portfolio scan for hyperoctahedral copy-algebra closure.

This extends the single highest-mass S_14 diagnostic to the next ranked
repeated branches under the exact hidden-involution Fourier-coordinate law.
For each branch it exhausts support at most three and then evaluates a
deterministic support-four witness schedule until the common commutant is
numerically scalar or all representatives are exhausted.  Matrix checkpoints
make the expensive ambient Specht contractions resumable.

The portfolio tests whether low-support closure persists on visible finite
source mass and actively searches for a counterexample.  It does not promote
rank-seven floating-point evidence to an all-rank theorem, a gap-scaling
bound, a coherent transform, a decoder, or a quantum speedup.
"""

from __future__ import annotations

import json
import statistics
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from coset_hidden_involution_high_mass_support_scan import (
    SUPPORT_FOUR_PRIORITY,
    TARGET_ALPHA,
    TARGET_BETA,
    TARGET_SYMMETRIC_PARTITION,
    SeparatorCertificate,
    _checkpoint_provenance,
    _load_checkpoint,
    _representative_key,
    _write_checkpoint,
    separator_commutant_certificate,
)
from coset_hidden_involution_multiplicity_fiber_trace import (
    copy_matrix_for_orbit_representative,
    isolate_root_multiplicity_fiber,
)
from coset_hidden_involution_multiplicity_twirl_projection import (
    _generated_algebra_dimension,
    _matrix_span_dimension,
    hermitian_bounded_support_orbit_representatives,
    moved_point_support,
)
from coset_hidden_involution_natural_support_six_mass_audit import (
    RepeatedBranchMassRecord,
    repeated_branch_census,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_source_weighted_support_portfolio.json"
)
PROGRESS_PATH = Path("tmp/coset_hidden_involution_source_weighted_portfolio.json")
CACHE_DIRECTORY = Path("tmp/coset_hidden_involution_source_weighted_support")
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-SOURCE-WEIGHTED-SUPPORT-PORTFOLIO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

BranchKey = tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]
BASELINE_HIGH_MASS_KEY: BranchKey = (
    TARGET_SYMMETRIC_PARTITION,
    TARGET_ALPHA,
    TARGET_BETA,
)


@dataclass(frozen=True)
class PortfolioRepresentativeEvaluation:
    representative_index: int
    moved_point_support: int
    elapsed_seconds: float
    loaded_from_checkpoint: bool
    cumulative_matrix_span_dimension: int
    cumulative_scalar_commutant_certified: bool


@dataclass(frozen=True)
class SourceWeightedBranchScan:
    source_rank: int
    symmetric_partition: tuple[int, ...]
    hyperoctahedral_partition: tuple[int, ...]
    negative_hyperoctahedral_partition: tuple[int, ...]
    symmetric_irrep_dimension: int
    branching_multiplicity: int
    carrier_dimension: int
    natural_mass_numerator: int
    natural_mass_probability: float
    fraction_of_repeated_natural_mass: float
    root_signed_weight_residual: float
    root_yjm_content_residual: float
    root_orthonormality_residual: float
    support_three_orbit_representative_count: int
    support_three_matrix_span_dimension: int
    support_three_generated_algebra_dimension: int
    support_three_scalar_commutant_certified: bool
    evaluated_representative_count: int
    evaluated_support_four_representative_count: int
    all_support_four_representatives_evaluated: bool
    certified_support_upper_bound: int | None
    inferred_copy_algebra_dimension: int
    exact_copy_algebra_dimension: int
    separator_certificate: SeparatorCertificate
    matrix_evidence: dict[str, Any]
    evaluations: list[PortfolioRepresentativeEvaluation]
    elapsed_seconds: float
    status: str


@dataclass(frozen=True)
class SourceWeightedPortfolioReport:
    created_at: str
    theorem_contract: dict[str, Any]
    half_degree: int
    requested_branch_count: int
    scanned_branches: list[SourceWeightedBranchScan]
    portfolio_natural_mass_probability: float
    portfolio_fraction_of_repeated_natural_mass: float
    baseline_plus_portfolio_natural_mass_probability: float
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _branch_key(row: RepeatedBranchMassRecord) -> BranchKey:
    return (
        row.symmetric_partition,
        row.hyperoctahedral_partition,
        row.negative_hyperoctahedral_partition,
    )


def _partition_slug(partition: tuple[int, ...]) -> str:
    return "-".join(str(value) for value in partition) or "empty"


def _branch_cache_path(
    row: RepeatedBranchMassRecord,
    cache_directory: Path,
) -> Path:
    return cache_directory / (
        f"m7_l{_partition_slug(row.symmetric_partition)}"
        f"_a{_partition_slug(row.hyperoctahedral_partition)}"
        f"_b{_partition_slug(row.negative_hyperoctahedral_partition)}.npz"
    )


def source_ranked_targets(
    target_count: int = 5,
) -> tuple[tuple[int, RepeatedBranchMassRecord], ...]:
    if target_count < 1:
        raise ValueError("target_count must be positive")
    _, _, _, repeated = repeated_branch_census(7)
    ranked = sorted(
        (row for row in repeated if _branch_key(row) != BASELINE_HIGH_MASS_KEY),
        key=lambda row: (
            -row.natural_mass_numerator,
            row.signed_weight_basis_entry_count,
        ),
    )
    if target_count > len(ranked):
        raise ValueError("target_count exceeds the available repeated branches")
    return tuple((index + 2, row) for index, row in enumerate(ranked[:target_count]))


def classify_scan(certificate: SeparatorCertificate, *, exhaustive: bool) -> str:
    if certificate.scalar_common_commutant_numerically_certified:
        return "numerically-supported-scalar-commutant"
    if (exhaustive and certificate.direct_commutant_nullity_at_1e8 > 1
            and certificate.direct_commutant_nullity_at_1e9 > 1):
        return "numerical-nonscalar-commutant-needs-exact-witness"
    return "inconclusive-not-a-counterexample"


def scan_source_weighted_branch(
    source_rank: int,
    row: RepeatedBranchMassRecord,
    *,
    repeated_mass_numerator: int,
    cache_directory: Path = CACHE_DIRECTORY,
    support_four_priority: Sequence[int] = SUPPORT_FOUR_PRIORITY,
) -> SourceWeightedBranchScan:
    started = time.monotonic()
    root = isolate_root_multiplicity_fiber(
        7,
        row.symmetric_partition,
        row.hyperoctahedral_partition,
        row.negative_hyperoctahedral_partition,
    )
    representatives = hermitian_bounded_support_orbit_representatives(7, 4)
    if any(index < 0 or index >= len(representatives)
           or moved_point_support(representatives[index]) != 4
           for index in support_four_priority):
        raise ValueError("support-four schedule contains an invalid representative")
    lower_indices = tuple(
        index
        for index, representative in enumerate(representatives)
        if moved_point_support(representative) <= 3
    )
    schedule = (*lower_indices, *support_four_priority)
    cache_path = _branch_cache_path(row, cache_directory)
    provenance = _checkpoint_provenance(root)
    checkpoint = _load_checkpoint(cache_path, root.branching_multiplicity, provenance)
    matrices: list[np.ndarray] = []
    evaluations: list[PortfolioRepresentativeEvaluation] = []
    lower_certificate: SeparatorCertificate | None = None
    final_certificate: SeparatorCertificate | None = None
    seen: set[int] = set()
    for representative_index in schedule:
        if representative_index in seen:
            continue
        seen.add(representative_index)
        representative = representatives[representative_index]
        key = _representative_key(representative)
        evaluation_started = time.monotonic()
        loaded = key in checkpoint
        if loaded:
            matrix = checkpoint[key]
        else:
            matrix, _ = copy_matrix_for_orbit_representative(
                7,
                row.symmetric_partition,
                row.hyperoctahedral_partition,
                representative,
                row.negative_hyperoctahedral_partition,
            )
            checkpoint[key] = matrix
            _write_checkpoint(cache_path, checkpoint, provenance)
        matrices.append(matrix)
        support = moved_point_support(representative)
        certificate = separator_commutant_certificate(matrices)
        if support <= 3 and len(seen) == len(lower_indices):
            lower_certificate = certificate
        if support == 4:
            final_certificate = certificate
        evaluations.append(
            PortfolioRepresentativeEvaluation(
                representative_index=representative_index,
                moved_point_support=support,
                elapsed_seconds=time.monotonic() - evaluation_started,
                loaded_from_checkpoint=loaded,
                cumulative_matrix_span_dimension=_matrix_span_dimension(
                    matrices,
                    tolerance=1e-8,
                ),
                cumulative_scalar_commutant_certified=(
                    certificate.scalar_common_commutant_numerically_certified
                ),
            )
        )
        if (
            support == 4
            and certificate.scalar_common_commutant_numerically_certified
        ):
            break
    if lower_certificate is None:
        raise ArithmeticError("support-three orbit census was incomplete")
    if final_certificate is None:
        final_certificate = lower_certificate
    lower_matrices = [
        matrix
        for matrix, evaluation in zip(matrices, evaluations)
        if evaluation.moved_point_support <= 3
    ]
    lower_word_dimension = _generated_algebra_dimension(
        lower_matrices,
        dimension_upper_bound=root.branching_multiplicity**2,
        tolerance=1e-8,
    )
    lower_full = lower_certificate.scalar_common_commutant_numerically_certified
    final_full = final_certificate.scalar_common_commutant_numerically_certified
    minimum_support = 3 if lower_full else 4 if final_full else None
    all_support_four = len(seen) == len(representatives)
    return SourceWeightedBranchScan(
        source_rank=source_rank,
        symmetric_partition=row.symmetric_partition,
        hyperoctahedral_partition=row.hyperoctahedral_partition,
        negative_hyperoctahedral_partition=row.negative_hyperoctahedral_partition,
        symmetric_irrep_dimension=root.symmetric_irrep_dimension,
        branching_multiplicity=root.branching_multiplicity,
        carrier_dimension=row.hyperoctahedral_irrep_dimension,
        natural_mass_numerator=row.natural_mass_numerator,
        natural_mass_probability=row.natural_mass_probability,
        fraction_of_repeated_natural_mass=(
            row.natural_mass_numerator / repeated_mass_numerator
        ),
        root_signed_weight_residual=root.maximum_signed_weight_residual,
        root_yjm_content_residual=root.maximum_yjm_content_residual,
        root_orthonormality_residual=root.orthonormality_residual,
        support_three_orbit_representative_count=len(lower_indices),
        support_three_matrix_span_dimension=_matrix_span_dimension(
            lower_matrices,
            tolerance=1e-8,
        ),
        support_three_generated_algebra_dimension=(
            root.branching_multiplicity**2 if lower_full else lower_word_dimension
        ),
        support_three_scalar_commutant_certified=lower_full,
        evaluated_representative_count=len(evaluations),
        evaluated_support_four_representative_count=sum(
            evaluation.moved_point_support == 4 for evaluation in evaluations
        ),
        all_support_four_representatives_evaluated=all_support_four,
        certified_support_upper_bound=minimum_support,
        inferred_copy_algebra_dimension=(
            root.branching_multiplicity**2 if final_full else 0
        ),
        exact_copy_algebra_dimension=root.branching_multiplicity**2,
        separator_certificate=final_certificate,
        matrix_evidence={
            "provenance": provenance,
            "evidence_kind": "floating-point-generator-matrices-not-interval-certified",
            "representative_indices": [row.representative_index for row in evaluations],
            "generators": [matrix.tolist() for matrix in matrices],
        },
        evaluations=evaluations,
        elapsed_seconds=time.monotonic() - started,
        status=classify_scan(final_certificate, exhaustive=all_support_four),
    )


def _write_progress(scans: Sequence[SourceWeightedBranchScan]) -> None:
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(
        json.dumps(
            {
                "created_at": utc_now(),
                "completed_branch_count": len(scans),
                "scanned_branches": [asdict(scan) for scan in scans],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def run_source_weighted_support_portfolio(
    *,
    target_count: int = 5,
    cache_directory: Path = CACHE_DIRECTORY,
) -> SourceWeightedPortfolioReport:
    denominator, _, _, repeated = repeated_branch_census(7)
    repeated_numerator = sum(row.natural_mass_numerator for row in repeated)
    scans: list[SourceWeightedBranchScan] = []
    for source_rank, row in source_ranked_targets(target_count):
        scans.append(
            scan_source_weighted_branch(
                source_rank,
                row,
                repeated_mass_numerator=repeated_numerator,
                cache_directory=cache_directory,
            )
        )
        _write_progress(scans)
    portfolio_numerator = sum(scan.natural_mass_numerator for scan in scans)
    portfolio_mass = portfolio_numerator / denominator
    baseline = next(row for row in repeated if _branch_key(row) == BASELINE_HIGH_MASS_KEY)
    baseline_plus_portfolio = (
        baseline.natural_mass_numerator + portfolio_numerator
    ) / denominator
    closed = [scan for scan in scans if scan.certified_support_upper_bound]
    unresolved = [scan for scan in scans if not scan.certified_support_upper_bound]
    closed_mass = sum(scan.natural_mass_numerator for scan in closed) / denominator
    gaps = [
        scan.separator_certificate.lcu_normalized_minimum_gap for scan in closed
    ]
    full = len(closed) == len(scans)
    status = (
        "source-ranked-s14-portfolio-closes-by-support-four-asymptotics-open"
        if full
        else "source-ranked-s14-portfolio-has-unresolved-branches"
    )
    return SourceWeightedPortfolioReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "the next source-ranked repeated S_14 branches after the highest-mass baseline, "
                "with exact multiplicity-fiber orbit contractions"
            ),
            "output": (
                "branchwise support cutoffs, scalar-commutant certificates, normalized finite gaps, "
                "and exact cumulative source coverage"
            ),
            "non_claim": (
                "No fixed-rank portfolio proves all-rank closure, typical-mass concentration, "
                "inverse-polynomial gap scaling, coherent access, decoding, or speedup."
            ),
        },
        half_degree=7,
        requested_branch_count=target_count,
        scanned_branches=scans,
        portfolio_natural_mass_probability=portfolio_mass,
        portfolio_fraction_of_repeated_natural_mass=(
            portfolio_numerator / repeated_numerator
        ),
        baseline_plus_portfolio_natural_mass_probability=baseline_plus_portfolio,
        proof_obligations=[
            {
                "obligation": "find_or_exclude_support_four_counterexample_at_rank_seven",
                "resolved": False,
                "resolution": (
                    "Continue the exact source-ranked queue until a counterexample appears or all repeated "
                    "S_14 mass is covered; a finite prefix is not exhaustive."
                ),
            },
            {
                "obligation": "prove_uniform_all_rank_low_support_generation",
                "resolved": False,
                "resolution": (
                    "Identify a symbolic commutant invariant or partition-algebra generator theorem that "
                    "covers growing partitions and bipartitions."
                ),
            },
            {
                "obligation": "construct_adaptive_labels_or_direct_coherent_transform",
                "resolved": False,
                "resolution": (
                    "Single bounded-norm simple-spectrum separators cannot have inverse-polynomial "
                    "minimum gaps on typical high-multiplicity blocks. Test a succinct hierarchy of "
                    "coarse labels or a direct source-aware transform instead."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The portfolio is selected for convenience rather than source relevance.",
                "survives": False,
                "response": (
                    "Branches are ordered solely by their exact one-coordinate natural source mass after "
                    "the independently audited highest-mass baseline."
                ),
            },
            {
                "challenge": "A scalar commutant is an artifact of one numerical diagnostic.",
                "survives": False,
                "response": (
                    "Each closure requires both a simple-separator connected graph and an independent direct "
                    "commutator-nullspace calculation at two tolerances."
                ),
            },
            {
                "challenge": "Several visible-mass S_14 branches establish asymptotic typical closure.",
                "survives": True,
                "response": (
                    "All scans remain at one finite rank and use branch-specific optimized separators."
                ),
            },
        ],
        headline_metrics={
            "source_ranked_portfolio_branch_count": len(scans),
            "source_ranked_support_four_closure_count": len(closed),
            "source_ranked_support_four_counterexample_count": 0,
            "source_ranked_unresolved_branch_count": len(unresolved),
            "numerically_closed_natural_mass_probability": closed_mass,
            "portfolio_natural_mass_probability": portfolio_mass,
            "portfolio_fraction_of_repeated_natural_mass": (
                portfolio_numerator / repeated_numerator
            ),
            "baseline_plus_portfolio_natural_mass_probability": (
                baseline_plus_portfolio
            ),
            "minimum_finite_lcu_normalized_separator_gap": min(gaps) if gaps else 0.0,
            "median_finite_lcu_normalized_separator_gap": (
                statistics.median(gaps) if gaps else 0.0
            ),
            "maximum_scanned_branching_multiplicity": max(
                scan.branching_multiplicity for scan in scans
            ),
            "exact_symbolic_uniform_support_theorem_count": 0,
            "inverse_polynomial_gap_scaling_theorem_count": 0,
            "coherent_multiplicity_transform_count": 0,
            "hidden_involution_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "source_ranked_portfolio_scanned": len(scans) == target_count,
            "every_scanned_branch_closes_by_support_four": full,
            "support_four_counterexample_found": False,
            "finite_portfolio_has_visible_source_mass": closed_mass >= 0.01,
            "all_rank_uniform_support_bound_proved": False,
            "one_minus_o_one_natural_mass_coverage_proved": False,
            "inverse_polynomial_normalized_gap_proved": False,
            "polynomial_typical_ambient_compression_proved": False,
            "coherent_multiplicity_transform_compiled": False,
            "hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The source-ranked portfolio is finite-rank floating-point evidence with branch-specific "
                "separators and exponential ambient contractions."
            ),
        },
        status=status,
        summary=(
            f"Scanned {len(scans)} source-ranked repeated S_14 branches covering {portfolio_mass:.6f} "
            f"mass; {len(closed)} have numerical closure and {len(unresolved)} remain unresolved."
        ),
        falsifiers_triggered=[
            *(
                [
                    "The next source-ranked S_14 branches do not require support five or six for full copy-algebra generation."
                ]
                if full
                else [
                    "The scan did not certify closure everywhere; this is not a verified counterexample."
                ]
            ),
            "Finite visible source mass at S_14 is not an all-rank typical-mass or gap-scaling theorem.",
        ],
    )


def write_source_weighted_support_portfolio_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    for key in (
        "write_registry",
        "registry_experiment_id",
        "registry_candidate_id",
        "registry_result_id",
    ):
        kwargs.pop(key, None)
    payload = asdict(run_source_weighted_support_portfolio(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentRecord,
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Source-ranked S_14 bounded-support portfolio",
                status=payload["status"],
                hypothesis=(
                    "Fixed low-support hyperoctahedral orbit sums generate repeated copy algebras on "
                    "visible exact source mass, or a source-ranked counterexample identifies the boundary."
                ),
                protocol=(
                    "Exhaust support three on each branch, evaluate checkpointed support-four witnesses, "
                    "and certify scalar commutants by separator connectivity plus direct nullity."
                ),
                positive_signal=(
                    "A symbolic all-rank generator and scalable adaptive labels or a direct transform "
                    "on one-minus-o(1) source mass with coherent access and decoding."
                ),
                falsifiers=[
                    "a source-ranked branch remains non-scalar after all support-four representatives",
                    "direct commutant nullity disagrees with the separator graph",
                    "finite gaps collapse with multiplicity or rank",
                    "the ambient contraction has no polynomial coherent implementation",
                ],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "coset_hidden_involution_multiplicity_fiber_trace.py",
                    "coset_hidden_involution_high_mass_support_scan.py",
                    "exact hidden-involution source law",
                ],
                next_actions=[
                    "continue the source-ranked branch queue",
                    "upgrade finite closures with interval or exact arithmetic",
                    "fit and prove a symbolic low-support generator rule",
                    "test an adaptive coarse-label hierarchy or a direct transform, not a single globally gapped separator",
                ],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"source_weighted_support_portfolio": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="FINITE-S14-SOURCE-WEIGHTED-PORTFOLIO-NOT-ASYMPTOTIC-COMMUTANT-THEOREM",
                source=registry_experiment_id,
                claim=(
                    "Low-support closure on a visible-mass S_14 portfolio proves a uniform typical-source "
                    "multiplicity transform."
                ),
                reason_invalid=(
                    "The portfolio is one finite rank, uses branch-specific numerical separators, retains "
                    "exponential ambient rows, and has no coherent decoder."
                ),
                lesson=(
                    "Use the portfolio to discover a symbolic invariant or counterexample, not as a speedup claim."
                ),
                applies_to=[registry_candidate_id, "bounded-support commutant program"],
                evidence={"artifact": str(path)},
            )
        )
        if payload["claim_gate"]["every_scanned_branch_closes_by_support_four"]:
            upsert_negative_result(
                NegativeResultRecord(
                    id="SOURCE-RANKED-S14-PORTFOLIO-DOES-NOT-REQUIRE-SUPPORT-FIVE-OR-SIX",
                    source=registry_experiment_id,
                    claim=(
                        "The next source-ranked repeated S_14 branches require support five or six for full "
                        "copy-algebra generation."
                    ),
                    reason_invalid=(
                        "Every scanned branch has a robust support-at-most-four scalar-commutant witness."
                    ),
                    lesson=(
                        "The finite evidence now favors a low-support generator theorem; search for its exact "
                        "partition-algebra mechanism while continuing counterexample scans."
                    ),
                    applies_to=[registry_candidate_id, "rank-seven source-ranked portfolio"],
                    evidence={"artifact": str(path)},
                )
            )
    return payload


if __name__ == "__main__":
    result = write_source_weighted_support_portfolio_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
