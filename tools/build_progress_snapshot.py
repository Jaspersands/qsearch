"""Build the small curated data file consumed by the public progress page."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
OUTPUT = RESEARCH / "progress_snapshot.json"


def read_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return fallback


def metric(payload: dict[str, Any], name: str, fallback: Any = 0) -> Any:
    return payload.get("headline_metrics", {}).get(name, fallback)


def latest_artifact_date(*payloads: Any) -> str:
    """Return the newest embedded artifact date without consulting wall-clock time."""
    timestamps: list[datetime] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in {"created_at", "updated_at", "timestamp"} and isinstance(child, str):
                    try:
                        timestamps.append(datetime.fromisoformat(child.replace("Z", "+00:00")))
                    except ValueError:
                        pass
                else:
                    visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for payload in payloads:
        visit(payload)
    return max(timestamps).astimezone(timezone.utc).date().isoformat() if timestamps else "unknown"


def build_snapshot() -> dict[str, Any]:
    registry = RESEARCH / "registry"
    experiments = read_json(registry / "experiments.json", [])
    results = read_json(registry / "experiment_results.json", [])
    findings = read_json(registry / "dequantization_checks.json", [])
    negatives = read_json(registry / "negative_results.json", [])
    proof_debt = read_json(RESEARCH / "proof_debt_report.json", {})
    marker = read_json(RESEARCH / "classical_baselines/dcp_marker_all_target_coverage.json", {})
    code_frontier = read_json(RESEARCH / "code_equivalence/code_frontier_triage.json", {})
    jm = read_json(RESEARCH / "representation/coset_jucys_murphy_label_transform.json", {})
    commutant = read_json(RESEARCH / "representation/coset_multiplicity_commutant_search.json", {})
    gap = read_json(RESEARCH / "representation/coset_commutant_gap_scaling.json", {})
    gap_certificate = read_json(
        RESEARCH / "representation/coset_commutant_gap_certificate.json", {}
    )
    racah = read_json(
        RESEARCH / "representation/coset_restricted_racah_control.json", {}
    )
    complete_racah = read_json(
        RESEARCH / "representation/coset_complete_racah_control.json", {}
    )
    hierarchical_racah = read_json(
        RESEARCH / "representation/coset_hierarchical_racah_control.json", {}
    )
    hierarchical_gap = read_json(
        RESEARCH / "representation/coset_hierarchical_gap_scaling.json", {}
    )
    sparse_gap = read_json(
        RESEARCH / "representation/coset_sparse_stable_gap_probe.json", {}
    )
    stable_trace = read_json(
        RESEARCH / "representation/coset_stable_trace_conjecture.json", {}
    )
    stable_trace_certificate = read_json(
        RESEARCH / "representation/coset_stable_trace_certificate.json", {}
    )
    stable_second_moment = read_json(
        RESEARCH / "representation/coset_stable_second_moment_certificate.json", {}
    )
    stable_third_moment = read_json(
        RESEARCH / "representation/coset_stable_third_moment_certificate.json", {}
    )
    stable_fourth_moment = read_json(
        RESEARCH / "representation/coset_stable_fourth_moment_certificate.json", {}
    )
    stable_root_separation = read_json(
        RESEARCH / "representation/coset_stable_root_separation_certificate.json", {}
    )
    stable_coherent_label = read_json(
        RESEARCH / "representation/coset_stable_coherent_label_certificate.json", {}
    )
    stable_transition = read_json(
        RESEARCH / "representation/coset_stable_subspace_transition_probe.json", {}
    )
    stable_complements = read_json(
        RESEARCH / "representation/coset_stable_complementary_sector_probe.json", {}
    )
    stable_shapes = read_json(
        RESEARCH / "representation/coset_stable_shape_family_certificate.json", {}
    )
    stable_shape_labels = read_json(
        RESEARCH / "representation/coset_stable_shape_label_probe.json", {}
    )
    stable_shape_traces = read_json(
        RESEARCH / "representation/coset_stable_shape_trace_certificate.json", {}
    )
    stable_shape_second_moments = read_json(
        RESEARCH / "representation/coset_stable_shape_second_moment_certificate.json",
        {},
    )
    stable_shape_cubic = read_json(
        RESEARCH / "representation/coset_stable_shape_cubic_determinant_certificate.json",
        {},
    )
    stable_shape_quadratic_gaps = read_json(
        RESEARCH / "representation/coset_stable_shape_quadratic_gap_certificate.json",
        {},
    )
    stable_shape_cubic_gap = read_json(
        RESEARCH / "representation/coset_stable_shape_cubic_gap_certificate.json",
        {},
    )
    stable_shape_coherent_labels = read_json(
        RESEARCH / "representation/coset_stable_shape_coherent_label_certificate.json",
        {},
    )
    stable_first_stage_labels = read_json(
        RESEARCH / "representation/coset_stable_first_stage_label_certificate.json",
        {},
    )
    stable_shape_router = read_json(
        RESEARCH / "representation/coset_stable_shape_router_certificate.json",
        {},
    )
    stable_encoded_tree = read_json(
        RESEARCH / "representation/coset_stable_encoded_tree_certificate.json",
        {},
    )
    stable_three_copy_frame = read_json(
        RESEARCH / "representation/coset_stable_three_copy_frame.json",
        {},
    )
    stable_frame_conditioning = read_json(
        RESEARCH / "representation/coset_stable_three_copy_frame_conditioning.json",
        {},
    )
    stable_branch_access = read_json(
        RESEARCH / "representation/coset_stable_branch_accessibility.json",
        {},
    )
    typical_irrep_transfer = read_json(
        RESEARCH / "representation/coset_typical_irrep_transfer_audit.json",
        {},
    )
    typical_commutant_moments = read_json(
        RESEARCH / "representation/coset_typical_commutant_moment_audit.json",
        {},
    )
    typical_class_contraction = read_json(
        RESEARCH / "representation/coset_typical_class_contraction_scaling.json",
        {},
    )
    typical_portfolio_collision = read_json(
        RESEARCH / "representation/coset_typical_portfolio_collision_certificate.json",
        {},
    )
    typical_third_generator = read_json(
        RESEARCH
        / "representation/coset_typical_independent_third_generator_certificate.json",
        {},
    )
    typical_high_multiplicity = read_json(
        RESEARCH / "representation/coset_typical_high_multiplicity_transfer.json",
        {},
    )
    typical_separator_gaps = read_json(
        RESEARCH / "representation/coset_typical_fixed_separator_gap_scaling.json",
        {},
    )
    typical_n9_probe = read_json(
        RESEARCH / "representation/coset_typical_n9_low_multiplicity_probe.json",
        {},
    )
    typical_n9_full = read_json(
        RESEARCH / "representation/coset_typical_n9_full_transfer.json",
        {},
    )
    typical_n10_feasibility = read_json(
        RESEARCH / "representation/coset_typical_n10_feasibility.json",
        {},
    )

    encoded = read_json(RESEARCH / "representation/coset_hidden_involution_encoded_restriction.json", {})
    reference_information = read_json(RESEARCH / "representation/coset_hidden_involution_reference_twirl_information.json", {})
    binary_instruments = read_json(RESEARCH / "representation/coset_binary_carrier_instruments.json", {})
    blocking = sum(bool(item.get("blocks_speedup_claim", False)) for item in findings)
    updated = latest_artifact_date(
        experiments,
        results,
        findings,
        negatives,
        proof_debt,
        marker,
        code_frontier,
        jm,
        commutant,
        gap,
        gap_certificate,
        racah,
        complete_racah,
        hierarchical_racah,
        hierarchical_gap,
        sparse_gap,
        stable_trace,
        stable_trace_certificate,
        stable_second_moment,
        stable_third_moment,
        stable_fourth_moment,
        stable_root_separation,
        stable_coherent_label,
        stable_transition,
        stable_complements,
        stable_shapes,
        stable_shape_labels,
        stable_shape_traces,
        stable_shape_second_moments,
        stable_shape_cubic,
        stable_shape_quadratic_gaps,
        stable_shape_cubic_gap,
        stable_shape_coherent_labels,
        stable_first_stage_labels,
        stable_shape_router,
        stable_encoded_tree,
        stable_three_copy_frame,
        stable_frame_conditioning,
        stable_branch_access,
        typical_irrep_transfer,
        typical_commutant_moments,
        typical_class_contraction,
        typical_portfolio_collision,
        typical_third_generator,
        typical_high_multiplicity,
        typical_separator_gaps,
        typical_n9_probe,
        typical_n9_full,
        typical_n10_feasibility,
    )
    gap_rows = metric(gap, "critical_gap_formula_finite_verified_count", 0)
    gap_total = metric(gap, "record_count", 0)
    gap_range = (
        f"n=6-{metric(gap, 'maximum_n', 10)}" if gap_rows else "finite n=6-10 calculations"
    )

    return {
        "updated_at": updated,
        "verdict": {
            "title": "No breakthrough yet",
            "detail": "Encoded subgroup access passes finite checks. No target measurement or decoder is supplied; speedup claims remain blocked.",
        },
        "overview": (
            "The current target is a useful measurement, not complete labels for every multiplicity. "
            "Spectral packing obstructs fixed-count normalized complete labels with inverse-polynomial gaps. "
            "Two QFTs instead extract a known subgroup carrier with an implicit copy code. Fixed-reference "
            "invariant identification is limited. Independent carrier discard also loses binary information; "
            "coherent retention does not itself supply a useful effect. Numerical checks are not formal proofs."
        ),
        "metrics": {
            "experiments": len(experiments),
            "results": len(results),
            "blocking_findings": blocking,
            "negative_results": len(negatives),
            "proof_debts": int(proof_debt.get("proof_debt_count", 0) or 0),
        },
        "tracks": [
            {
                "title": "Hidden shift / DHSP",
                "short_title": "DHSP",
                "status": "Current decoder route blocked",
                "tone": "blocked",
                "stage": 2,
                "summary": (
                    "Exact source models, sieve accounting, lattice attacks, and marker-aware decoders were implemented. "
                    "Fixed-depth nearest-plane lists eventually collapse, so small-n decoder success is not evidence of a polynomial algorithm."
                ),
                "evidence": (
                    f"The all-target census evaluated {metric(marker, 'legal_target_count', 'millions of')} legal targets; "
                    "the remaining question is a source-conditioned reduced-basis theorem, not another target sweep."
                ),
                "next": "Prove a random-label LLL geometry law or abandon nearest-plane branching.",
            },
            {
                "title": "Code equivalence",
                "short_title": "Codes",
                "status": "Generated frontier closed",
                "tone": "blocked",
                "stage": 1,
                "summary": (
                    "Goppa, quasi-cyclic, finite-geometry, rank-metric, and CFI-derived rows were attacked with "
                    "support, hull, Schur, syzygy, projector, recovery, and graph-side invariants."
                ),
                "evidence": (
                    f"Current triage retains {metric(code_frontier, 'proof_debt_row_count', 0)} viable code rows; "
                    "the last Goppa syzygy collision was resolved by the hull-projector route."
                ),
                "next": "Generate a new natural family that survives the complete classical triage gate.",
            },
            {
                "title": "Nonabelian coset states",
                "short_title": "Cosets",
                "status": "Encoded access checked; useful measurement open",
                "tone": "active",
                "stage": 3,
                "summary": (
                    "Two-QFT restriction preserves normalization and supports logical orbit averages without "
                    "decoding a copy basis. Independent carrier discard loses the detection signal. "
                    "The tested small-group binary gains have a classical latent-irrep explanation. "
                    "No useful detector or access to the unknown centralizer is supplied."
                ),
                "evidence": (
                    f"Finite isometries: {metric(encoded, 'finite_isometry_controls_passed', 0)}. "
                    f"Information-loss controls: {metric(reference_information, 'finite_binary_controls_passed', 0)}. "
                    f"Finite instrument schedules: {metric(binary_instruments, 'schedules_evaluated', 0)}. "
                    "No scalable QFT gate implementation or decoder is supplied."
                ),
                "next": "Construct a task-relevant logical effect; test information, normalization, and classical simulability.",
            },
        ],
        "milestones": [
            {
                "title": "The stable coupling-tree interface is complete",
                "detail": "Shape, first-stage, and second-stage observables give all 25 encoded labels on both trees and a polynomial left/right relabelling isometry.",
            },
            {
                "title": "The stable three-copy frame is filterable",
                "detail": "Fifty-four exact character-ratio inequalities prove lambda_min(F)>=(71/825)n^-5 and polynomial inverse-square-root filters for two involution families.",
            },
            {
                "title": "Natural access kills the fixed stable branch",
                "detail": "Its exact probability is d_W^3 d_xi Tr(F)/(n!)^3, at most (25/3)n^9/(n!)^3; postselection and generic amplification are superpolynomial.",
            },
            {
                "title": "Every fixed bounded-tail route is cut",
                "detail": "For fixed K, total weak-Fourier mass is at most 2 P_K n^(2K)/n!. Uniform adaptation to typical high-dimensional partitions is now mandatory.",
            },
            {
                "title": "An independent third generator repairs the known finite collisions",
                "detail": (
                    "TC2/TT1 and its disjoint extension are exactly degenerate at n=8. Exact parameterized fourth "
                    f"moments instead prove TT1+c*TC1 has simple spectrum for every c!=0 on "
                    f"{metric(typical_third_generator, 'certified_n8_low_multiplicity_simple_spectrum_target_count', 0)} "
                    "n=8 targets of multiplicity at most four, including both known collisions. Exact quotient transfer "
                    f"at c=1 extends this to {metric(typical_high_multiplicity, 'certified_n8_simple_spectrum_target_count', 0)}/"
                    f"{metric(typical_high_multiplicity, 'n8_nontrivial_multiplicity_target_count', 0)} targets through "
                    "multiplicity 17. Degree-28 transfer and class-Fourier contraction extend fixed-c1 separation to "
                    f"{metric(typical_n9_full, 'certified_n9_simple_spectrum_target_count', 0)}/"
                    f"{metric(typical_n9_full, 'n9_nontrivial_multiplicity_target_count', 0)} n=9 targets. All-n, gap, transform, "
                    "and decoder questions remain separate; typical complete-label inverse-polynomial gaps are obstructed."
                ),
            },
        ],
        "active_conjecture": {
            "summary": (
                "Can normalized implicit-copy operations implement useful collective binary detection or "
                "symmetry-breaking identification? Carrier extraction does not establish this. An older "
                "local systematic-core proof claim was also withdrawn without refuting the independent global BABA argument."
            ),
            "facts": [
                {"label": "Complete fixed-count labels", "value": "Packing obstruction"},
                {"label": "Encoded access", "value": f"{metric(encoded, 'finite_isometry_controls_passed', 0)} finite controls"},
                {"label": "Unknown alignment", "value": "Not granted"},
                {"label": "Target effect", "value": "Open"},
                {"label": "Hidden decoder", "value": "Open"},
            ],
        },
        "next_actions": [
            {
                "title": "Specify the logical target effect",
                "detail": "Formulate binary detection or a charged symmetry-breaking measurement. Complete typical spectral labels are not the target.",
            },
            {
                "title": "Keep natural branch mass in every theorem",
                "detail": "Aggregate over naturally sampled labels instead of postselecting sectors, and prove the retained mass remains inverse polynomial.",
            },
            {
                "title": "Derive and attack an outcome law",
                "detail": "Specify the hidden-involution-dependent measurement distribution, construct a decoder, and try to reproduce it with classical character and tensor methods.",
            },
        ],
        "execution_model": (
            "Research generation and experiments run interactively during active Codex sessions. A GitHub workflow "
            "validates pushed snapshots, and a scheduled backup can commit only validation-passing changes; neither "
            "mechanism performs autonomous quantum-algorithm research between sessions."
        ),
    }


def main() -> None:
    payload = build_snapshot()
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
