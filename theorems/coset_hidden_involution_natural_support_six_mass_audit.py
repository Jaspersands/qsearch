"""Natural-source mass audit for bounded-support multiplicity generation.

For ``G=S_(2m)`` and ``K=C_2 wr S_m``, one Fourier coordinate of the
hidden-involution coset source has exact joint law

    q(lambda,(alpha,beta)) = 2 d_lambda d_(alpha,beta) b(lambda;alpha,beta)/|G|

on the ``h``-even branches ``|beta|`` even.  This module uses that law to
measure what fraction of the actual source has been touched by finite
support-six commutant scans.  It deliberately separates three statements:

1. a bounded-support orbit family generates a copy algebra on a finite block;
2. those blocks carry nonnegligible natural source mass;
3. the generators have inverse-polynomial normalized gaps and coherent access.

Only the first is currently observed.  At ``m=7``, repeated blocks carry
almost all source mass, but the selected low-dimensional audited blocks carry
only a tiny fraction.  The report ranks the highest-mass untested blocks and
records the ambient signed-sector workspace required by the present classical
compressor.  It is a target-selection and falsification tool, not a quantum
algorithm or a support-six theorem.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from coset_hidden_involution_multiplicity_twirl_projection import (
    REPORT_PATH as MULTIPLICITY_TWIRL_REPORT_PATH,
    run_multiplicity_twirl_projection,
)
from coset_hidden_involution_natural_recoupling_boundary import (
    hyperoctahedral_irrep_dimension,
)
from coset_hidden_involution_paired_tower_missing_label_boundary import (
    bipartitions,
    hyperoctahedral_branching_coefficient,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_natural_support_six_mass_audit.json"
)
HIGH_MASS_SUPPORT_SCAN_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_high_mass_support_scan.json"
)
SOURCE_WEIGHTED_SUPPORT_PORTFOLIO_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_source_weighted_support_portfolio.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-NATURAL-SUPPORT-SIX-MASS-AUDIT"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
BranchKey = tuple[Partition, Partition, Partition]


@dataclass(frozen=True)
class RepeatedBranchMassRecord:
    symmetric_partition: Partition
    hyperoctahedral_partition: Partition
    negative_hyperoctahedral_partition: Partition
    symmetric_irrep_dimension: int
    hyperoctahedral_irrep_dimension: int
    branching_multiplicity: int
    selected_character_isotypic_dimension: int
    selected_character_weight_space_dimension: int
    equal_weight_character_count: int
    natural_mass_numerator: int
    natural_mass_probability: float
    signed_weight_basis_entry_count: int
    current_compressor_status: str


@dataclass(frozen=True)
class FeasibilityWindow:
    maximum_symmetric_irrep_dimension: int
    maximum_selected_isotypic_dimension: int
    repeated_branch_count: int
    natural_mass_probability: float
    repeated_natural_mass_fraction: float
    status: str


@dataclass(frozen=True)
class NaturalSupportMassTheorem:
    exact_joint_law: str
    exact_normalization: str
    repeated_mass_conclusion: str
    audited_mass_conclusion: str
    selection_bias_conclusion: str
    exact_joint_law_normalized: bool
    repeated_blocks_have_dominant_mass: bool
    audited_support_six_blocks_have_nonnegligible_mass: bool
    low_ambient_scan_has_nonnegligible_mass: bool
    uniform_support_six_generation_proved: bool
    inverse_polynomial_gap_on_natural_mass_proved: bool
    coherent_natural_mass_transform_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalSupportMassReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: NaturalSupportMassTheorem
    half_degree: int
    exact_mass_denominator: int
    occupied_even_branch_count: int
    repeated_branch_count: int
    repeated_natural_mass_probability: float
    audited_rank_branch_count: int
    audited_rank_natural_mass_probability: float
    audited_fraction_of_repeated_natural_mass: float
    source_ranked_audited_branch_count: int
    source_ranked_natural_mass_gain: float
    feasibility_windows: list[FeasibilityWindow]
    highest_mass_untested_branches: list[RepeatedBranchMassRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _selected_weight_space_dimension(
    half_degree: int,
    symmetric_partition: Partition,
    negative_pair_count: int,
) -> int:
    positive_pair_count = half_degree - negative_pair_count
    return sum(
        hyperoctahedral_branching_coefficient(
            symmetric_partition,
            alpha,
            beta,
        )
        * hook_length_dimension(alpha)
        * hook_length_dimension(beta)
        for alpha in integer_partitions(positive_pair_count)
        for beta in integer_partitions(negative_pair_count)
    )


@lru_cache(maxsize=None)
def repeated_branch_census(
    half_degree: int,
) -> tuple[
    int,
    int,
    int,
    tuple[RepeatedBranchMassRecord, ...],
]:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    degree = 2 * half_degree
    denominator = math.factorial(degree)
    occupied_count = 0
    total_numerator = 0
    records = []
    weight_dimensions: dict[tuple[Partition, int], int] = {}
    for symmetric_partition in integer_partitions(degree):
        symmetric_dimension = hook_length_dimension(symmetric_partition)
        for alpha, beta in bipartitions(half_degree):
            if sum(beta) % 2:
                continue
            multiplicity = hyperoctahedral_branching_coefficient(
                symmetric_partition,
                alpha,
                beta,
            )
            if multiplicity == 0:
                continue
            occupied_count += 1
            carrier_dimension = hyperoctahedral_irrep_dimension(alpha, beta)
            numerator = (
                2
                * symmetric_dimension
                * carrier_dimension
                * multiplicity
            )
            total_numerator += numerator
            if multiplicity < 2:
                continue
            negative_count = sum(beta)
            weight_key = (symmetric_partition, negative_count)
            if weight_key not in weight_dimensions:
                weight_dimensions[weight_key] = _selected_weight_space_dimension(
                    half_degree,
                    symmetric_partition,
                    negative_count,
                )
            selected_dimension = (
                multiplicity
                * hook_length_dimension(alpha)
                * hook_length_dimension(beta)
            )
            equal_weight_count = math.comb(half_degree, negative_count)
            records.append(
                RepeatedBranchMassRecord(
                    symmetric_partition=symmetric_partition,
                    hyperoctahedral_partition=alpha,
                    negative_hyperoctahedral_partition=beta,
                    symmetric_irrep_dimension=symmetric_dimension,
                    hyperoctahedral_irrep_dimension=carrier_dimension,
                    branching_multiplicity=multiplicity,
                    selected_character_isotypic_dimension=selected_dimension,
                    selected_character_weight_space_dimension=(
                        weight_dimensions[weight_key]
                    ),
                    equal_weight_character_count=equal_weight_count,
                    natural_mass_numerator=numerator,
                    natural_mass_probability=numerator / denominator,
                    signed_weight_basis_entry_count=(
                        symmetric_dimension * weight_dimensions[weight_key]
                    ),
                    current_compressor_status=(
                        "finite-scan-feasible"
                        if symmetric_dimension <= 5000
                        and selected_dimension <= 300
                        else "requires-symbolic-or-matrix-free-transfer"
                    ),
                )
            )
    if total_numerator != denominator:
        raise ArithmeticError("hidden-involution joint source law did not normalize")
    return denominator, occupied_count, total_numerator, tuple(records)


def _branch_key_from_control(control: dict[str, Any]) -> BranchKey:
    return (
        tuple(int(value) for value in control["symmetric_partition"]),
        tuple(int(value) for value in control["hyperoctahedral_partition"]),
        tuple(
            int(value)
            for value in control.get("negative_hyperoctahedral_partition", [])
        ),
    )


def _load_or_build_multiplicity_report() -> dict[str, Any]:
    if MULTIPLICITY_TWIRL_REPORT_PATH.exists():
        try:
            payload = json.loads(MULTIPLICITY_TWIRL_REPORT_PATH.read_text())
            metrics = payload.get("headline_metrics", {})
            if (
                metrics.get("multiplicity_three_control_count", 0) >= 1
                and metrics.get("nontrivial_beta_control_count", 0) >= 3
            ):
                return payload
        except (json.JSONDecodeError, OSError):
            pass
    return asdict(run_multiplicity_twirl_projection())


def _load_high_mass_support_report() -> dict[str, Any]:
    if not HIGH_MASS_SUPPORT_SCAN_PATH.exists():
        return {}
    try:
        return json.loads(HIGH_MASS_SUPPORT_SCAN_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _load_source_weighted_portfolio_report() -> dict[str, Any]:
    if not SOURCE_WEIGHTED_SUPPORT_PORTFOLIO_PATH.exists():
        return {}
    try:
        return json.loads(SOURCE_WEIGHTED_SUPPORT_PORTFOLIO_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def run_natural_support_six_mass_audit(
    *,
    half_degree: int = 7,
    multiplicity_report: dict[str, Any] | None = None,
    high_mass_report: dict[str, Any] | None = None,
    portfolio_report: dict[str, Any] | None = None,
    priority_target_count: int = 20,
) -> NaturalSupportMassReport:
    if priority_target_count < 0:
        raise ValueError("priority_target_count must be nonnegative")
    denominator, occupied_count, total_numerator, repeated = repeated_branch_census(
        half_degree
    )
    del total_numerator
    repeated_numerator = sum(row.natural_mass_numerator for row in repeated)
    repeated_mass = repeated_numerator / denominator
    source_report = _load_or_build_multiplicity_report() if multiplicity_report is None else multiplicity_report
    selected_audited_keys = {
        _branch_key_from_control(control)
        for control in source_report.get("controls", [])
        if int(control.get("half_degree", -1)) == half_degree
        and control.get("compressed_twirl_projection_verified", False)
        and control.get("minimum_full_copy_algebra_support") is not None
        and int(control["minimum_full_copy_algebra_support"]) <= 6
    }
    audited_keys = set(selected_audited_keys)
    source_ranked_keys: set[BranchKey] = set()
    source_ranked_report = (
        _load_high_mass_support_report()
        if high_mass_report is None
        else high_mass_report
    )
    source_ranked_gate = source_ranked_report.get("claim_gate", {})
    if (
        int(source_ranked_report.get("half_degree", -1)) == half_degree
        and source_ranked_gate.get(
            "support_four_full_copy_algebra_numerically_certified",
            False,
        )
    ):
        source_ranked_keys.add(
            (
                tuple(source_ranked_report.get("symmetric_partition", [])),
                tuple(source_ranked_report.get("hyperoctahedral_partition", [])),
                tuple(
                    source_ranked_report.get(
                        "negative_hyperoctahedral_partition",
                        [],
                    )
                ),
            )
        )
        audited_keys.update(source_ranked_keys)
    source_portfolio = (
        _load_source_weighted_portfolio_report()
        if portfolio_report is None
        else portfolio_report
    )
    for scan in source_portfolio.get("scanned_branches", []):
        certificate = scan.get("separator_certificate", {})
        minimum_support = scan.get("certified_support_upper_bound")
        if (
            int(source_portfolio.get("half_degree", -1)) == half_degree
            and minimum_support is not None
            and int(minimum_support) <= 6
            and certificate.get(
                "scalar_common_commutant_numerically_certified",
                False,
            )
            and int(certificate.get("direct_commutant_nullity_at_1e8", 0)) == 1
        ):
            source_ranked_keys.add(
                (
                    tuple(scan.get("symmetric_partition", [])),
                    tuple(scan.get("hyperoctahedral_partition", [])),
                    tuple(scan.get("negative_hyperoctahedral_partition", [])),
                )
            )
    audited_keys.update(source_ranked_keys)
    by_key = {
        (
            row.symmetric_partition,
            row.hyperoctahedral_partition,
            row.negative_hyperoctahedral_partition,
        ): row
        for row in repeated
    }
    selected_audited_keys.intersection_update(by_key)
    source_ranked_keys.intersection_update(by_key)
    audited_keys.intersection_update(by_key)
    audited_numerator = sum(
        by_key[key].natural_mass_numerator
        for key in audited_keys
        if key in by_key
    )
    audited_mass = audited_numerator / denominator
    audited_fraction = audited_numerator / repeated_numerator
    selected_numerator = sum(
        by_key[key].natural_mass_numerator
        for key in selected_audited_keys
        if key in by_key
    )
    source_ranked_mass_gain = (audited_numerator - selected_numerator) / denominator

    windows = []
    for ambient_limit in (5000, 10000, 20000, 50000, 70000):
        selected = [
            row
            for row in repeated
            if row.symmetric_irrep_dimension <= ambient_limit
            and row.selected_character_isotypic_dimension <= 300
        ]
        mass = sum(row.natural_mass_numerator for row in selected) / denominator
        windows.append(
            FeasibilityWindow(
                maximum_symmetric_irrep_dimension=ambient_limit,
                maximum_selected_isotypic_dimension=300,
                repeated_branch_count=len(selected),
                natural_mass_probability=mass,
                repeated_natural_mass_fraction=mass / repeated_mass,
                status=(
                    "finite-window-natural-mass-negligible"
                    if mass < 0.01
                    else "finite-window-covers-visible-natural-mass"
                ),
            )
        )
    priority = sorted(
        (row for key, row in by_key.items() if key not in audited_keys),
        key=lambda row: (
            -row.natural_mass_numerator,
            row.signed_weight_basis_entry_count,
        ),
    )[:priority_target_count]
    exact = sum(
        2
        * hook_length_dimension(symmetric_partition)
        * hyperoctahedral_irrep_dimension(alpha, beta)
        * hyperoctahedral_branching_coefficient(
            symmetric_partition,
            alpha,
            beta,
        )
        for symmetric_partition in integer_partitions(2 * half_degree)
        for alpha, beta in bipartitions(half_degree)
        if sum(beta) % 2 == 0
    ) == denominator
    low_window_mass = windows[0].natural_mass_probability
    source_ranked_added = bool(source_ranked_keys)
    status = (
        "source-ranked-controls-cover-visible-but-not-typical-natural-mass"
        if audited_mass >= 0.01
        else (
            "source-ranked-support-four-control-raises-coverage-but-remains-subpercent"
            if source_ranked_added
            else "finite-support-six-controls-have-negligible-natural-mass"
        )
    )
    theorem = NaturalSupportMassTheorem(
        exact_joint_law=(
            "q(lambda,(alpha,beta))=2 d_lambda d_(alpha,beta) "
            "b(lambda;alpha,beta)/(2m)! on even |beta|."
        ),
        exact_normalization=(
            f"The complete m={half_degree} census sums exactly to "
            f"{denominator}/{denominator}."
        ),
        repeated_mass_conclusion=(
            f"Multiplicity-at-least-two blocks carry {repeated_mass:.12f} "
            "of the exact one-coordinate source mass."
        ),
        audited_mass_conclusion=(
            f"The support-six-closed audited rank-{half_degree} blocks carry only "
            f"{audited_mass:.12g} total source mass."
        ),
        selection_bias_conclusion=(
            "Source-ranked finite scans now cover visible but non-typical mass; proving "
            "or refuting a natural-mass theorem still requires growing-rank typical "
            "blocks or a symbolic transfer principle."
        ),
        exact_joint_law_normalized=exact,
        repeated_blocks_have_dominant_mass=repeated_mass >= 0.9,
        audited_support_six_blocks_have_nonnegligible_mass=audited_mass >= 0.01,
        low_ambient_scan_has_nonnegligible_mass=low_window_mass >= 0.01,
        uniform_support_six_generation_proved=False,
        inverse_polynomial_gap_on_natural_mass_proved=False,
        coherent_natural_mass_transform_compiled=False,
        theorem_verified=exact and repeated_mass >= 0.9,
        status=status,
    )
    metrics: dict[str, int | float] = {
        "exact_joint_source_normalization_theorem_count": int(exact),
        "occupied_even_branch_count": occupied_count,
        "repeated_branch_count": len(repeated),
        "repeated_natural_mass_probability": repeated_mass,
        "audited_rank_branch_count": len(audited_keys),
        "audited_rank_natural_mass_probability": audited_mass,
        "audited_fraction_of_repeated_natural_mass": audited_fraction,
        "source_ranked_audited_branch_count": len(source_ranked_keys),
        "source_ranked_natural_mass_gain": source_ranked_mass_gain,
        "convenience_selected_natural_mass_probability": (
            selected_numerator / denominator
        ),
        "ambient_5000_feasible_repeated_branch_count": windows[0].repeated_branch_count,
        "ambient_5000_feasible_natural_mass_probability": low_window_mass,
        "highest_mass_untested_branch_probability": priority[0].natural_mass_probability if priority else 0.0,
        "uniform_support_six_generation_theorem_count": 0,
        "inverse_polynomial_gap_on_natural_mass_theorem_count": 0,
        "coherent_natural_mass_transform_count": 0,
        "hidden_involution_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return NaturalSupportMassReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "the exact hidden-involution Fourier-coordinate source law and "
                "verified finite multiplicity-twirl controls"
            ),
            "output": (
                "exact natural-mass coverage, finite-scan feasibility windows, "
                "and a ranked queue of high-mass untested repeated blocks"
            ),
            "non_claim": (
                "No finite block closure is promoted to a natural-mass, spectral-gap, "
                "coherent-transform, decoder, or speedup theorem."
            ),
        },
        theorem=theorem,
        half_degree=half_degree,
        exact_mass_denominator=denominator,
        occupied_even_branch_count=occupied_count,
        repeated_branch_count=len(repeated),
        repeated_natural_mass_probability=repeated_mass,
        audited_rank_branch_count=len(audited_keys),
        audited_rank_natural_mass_probability=audited_mass,
        audited_fraction_of_repeated_natural_mass=audited_fraction,
        source_ranked_audited_branch_count=len(source_ranked_keys),
        source_ranked_natural_mass_gain=source_ranked_mass_gain,
        feasibility_windows=windows,
        highest_mass_untested_branches=priority,
        proof_obligations=[
            {
                "obligation": "find_support_six_counterexample_on_natural_mass",
                "resolved": False,
                "resolution": (
                    "Run matrix-free or symbolic copy-algebra tests on the ranked "
                    "high-mass blocks instead of adding low-dimensional controls."
                ),
            },
            {
                "obligation": "prove_uniform_support_six_generation",
                "resolved": False,
                "resolution": (
                    "A symbolic invariant must cover all naturally occupied repeated "
                    "bipartitions; finite rank-seven closure is insufficient."
                ),
            },
            {
                "obligation": "compile_task_relevant_adaptive_labels_on_natural_mass",
                "resolved": False,
                "resolution": (
                    "Algebra generation supplies no decoder. A single complete normalized spectrum "
                    "cannot retain polynomial minimum gaps on typical blocks; specify task-relevant "
                    "coarse gaps, an adaptive hierarchy, or a direct transform."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The successful rank-seven controls are representative.",
                "survives": False,
                "response": (
                    f"Their exact combined source mass is {audited_mass:.12g}, only "
                    f"{audited_fraction:.12g} of repeated-block mass."
                ),
            },
            {
                "challenge": "Scanning every small ambient irrep removes selection bias.",
                "survives": False,
                "response": (
                    f"The ambient-dimension-5000 window carries only {low_window_mass:.12g} "
                    "natural mass."
                ),
            },
            {
                "challenge": "Full matrix-algebra generation implies efficient resolution.",
                "survives": True,
                "response": (
                    "No normalized spectral gap, succinct joint separator, or coherent "
                    "source transform follows from generation alone."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_joint_source_law_normalized": exact,
            "repeated_blocks_carry_dominant_source_mass": repeated_mass >= 0.9,
            "audited_support_six_blocks_have_nonnegligible_mass": audited_mass >= 0.01,
            "source_ranked_high_mass_control_included": source_ranked_added,
            "low_ambient_scan_has_nonnegligible_mass": low_window_mass >= 0.01,
            "uniform_support_six_generation_proved": False,
            "inverse_polynomial_gap_on_natural_mass_proved": False,
            "coherent_natural_mass_transform_compiled": False,
            "hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The finite rank-seven closure controls do not cover typical natural mass, and no "
                "uniform generation, normalized gap, coherent transform, or decoder "
                "has been proved on typical blocks."
            ),
        },
        status=theorem.status,
        summary=(
            f"Censused {len(repeated)} repeated S_{2 * half_degree} branches: they "
            f"carry {repeated_mass:.6f} source mass, while the {len(audited_keys)} "
            f"audited support-six blocks cover only {audited_mass:.3e}."
        ),
        falsifiers_triggered=[
            "Selected low-dimensional support-six controls are not representative of the natural source law.",
            "A finite full copy algebra is not an inverse-polynomial-gap coherent resolver.",
            "Brute-force low-ambient scans cannot establish typical-block support-six generation.",
        ],
    )


def write_natural_support_six_mass_audit(
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
    payload = asdict(run_natural_support_six_mass_audit(**kwargs))
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
                title="Natural-mass audit of support-six multiplicity controls",
                status=payload["status"],
                hypothesis=(
                    "Finite support-six copy-algebra closure on selected S_14 blocks "
                    "covers a representative fraction of the hidden-involution source."
                ),
                protocol=(
                    "Enumerate every h-even S_14-to-K_7 branching pair, apply the exact "
                    "joint source law, measure audited and feasible-window mass, and rank "
                    "the highest-mass untested repeated blocks."
                ),
                positive_signal=(
                    "Support-six generation with inverse-polynomial normalized gaps on "
                    "a source-mass-one-minus-o(1) family and a coherent transform."
                ),
                falsifiers=[
                    "selected controls cover negligible exact source mass",
                    "small-ambient exhaustive windows remain source-negligible",
                    "copy-algebra generation lacks normalized spectral gaps",
                ],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "coset_hidden_involution_multiplicity_twirl_projection.py",
                    "coset_hidden_involution_high_mass_support_scan.py",
                    "coset_hidden_involution_source_weighted_support_portfolio.py",
                    "coset_hidden_involution_hyperoctahedral_branching_mass.py",
                    "exact hyperoctahedral branching coefficients",
                ],
                next_actions=[
                    "attack the next ranked high-mass untested S_14 blocks",
                    "replace ambient signed-sector QR by symbolic or matrix-free transfer",
                    "measure normalized joint-separator gaps on natural mass",
                    "search for a support-six counterexample before attempting a theorem",
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
                artifacts={
                    "coset_hidden_involution_natural_support_six_mass_audit": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="FINITE-S14-SUPPORT-SIX-CLOSURE-NEGLIGIBLE-NATURAL-MASS",
                source=registry_experiment_id,
                claim=(
                    "The convenience-selected rank-seven support-six closure controls are evidence "
                    "for behavior on a representative natural source family."
                ),
                reason_invalid=(
                    f"Before source-ranked scans, their exact joint source mass was only "
                    f"{payload['headline_metrics']['convenience_selected_natural_mass_probability']:.12g}."
                ),
                lesson=(
                    "Prioritize source-weighted typical blocks or prove a symbolic "
                    "all-block transfer; stop accumulating convenient low-dimensional examples."
                ),
                applies_to=[
                    registry_candidate_id,
                    "bounded-support hyperoctahedral commutants",
                    "finite multiplicity-space scans",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="FINITE-S14-VISIBLE-MASS-CLOSURE-NOT-TYPICAL-ASYMPTOTIC-MASS",
                source=registry_experiment_id,
                claim=(
                    "Low-support closure on several source-ranked S_14 branches proves a typical-source "
                    "all-rank commutant theorem."
                ),
                reason_invalid=(
                    f"All evidence remains at rank seven and covers only "
                    f"{payload['audited_rank_natural_mass_probability']:.12g} exact source mass."
                ),
                lesson=(
                    "Continue source-ranked falsification while deriving a uniform symbolic invariant; "
                    "finite visible mass is target-selection evidence, not asymptotics."
                ),
                applies_to=[
                    registry_candidate_id,
                    "bounded-support hyperoctahedral commutants",
                    "source-ranked finite scans",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="COPY-ALGEBRA-GENERATION-NOT-GAPPED-COHERENT-RESOLUTION",
                source=registry_experiment_id,
                claim=(
                    "Generating M_b with bounded-support orbit sums yields an efficient "
                    "coherent multiplicity resolver."
                ),
                reason_invalid=(
                    "Generation gives neither a succinct common separator nor an "
                    "inverse-polynomial normalized gap, coherent isotypic access, or "
                    "source-aware implementation."
                ),
                lesson=(
                    "Record normalized spectra and coherent access costs before treating "
                    "copy-algebra generation as algorithmic progress."
                ),
                applies_to=[
                    registry_candidate_id,
                    "support-six generation",
                    "multiplicity resolution",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_natural_support_six_mass_audit()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
