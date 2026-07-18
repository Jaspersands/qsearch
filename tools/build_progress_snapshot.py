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
            "detail": (
                "Every speedup claim remains blocked. One restricted representation-theoretic gap theorem is now proved, "
                "and a bounded-support hierarchy resolves the complete finite S_6 Racah table. Stable-n gaps, a coherent "
                "recoupling circuit, and hidden-involution decoding remain open."
            ),
        },
        "overview": (
            "The project is now useful primarily as a research filter. It has replaced tiny-circuit search with "
            "proof obligations, access-model accounting, classical attacks, exact finite representation theory, "
            "and a permanent negative-result memory. The strongest surviving lead is not an algorithm: it is a "
            "specific bounded-support operator hierarchy with exact and falsifiable spectral theorem targets in a nonabelian HSP route."
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
                "status": "Active structural lead",
                "tone": "active",
                "stage": 3,
                "summary": (
                    "The project separated efficient Fourier/tableau labels from the genuinely open multiplicity-space, "
                    "Racah, transition-filter, and hidden-involution decoder operations."
                ),
                "evidence": (
                    f"YJM spectra were verified on {metric(jm, 'record_count', 3)} sectors, and bounded-support "
                    f"commutants split {metric(commutant, 'finite_all_block_split_count', 2)} finite multiplicity sectors up to multiplicity "
                    f"{metric(commutant, 'maximum_kronecker_multiplicity', 5)}. The stable multiplicity-two family now has "
                    f"{metric(gap_certificate, 'all_n_critical_gap_theorem_count', 0)} exact all-n gap theorem; "
                    f"the hierarchy resolves {metric(hierarchical_racah, 'complete_hierarchical_finite_racah_matrix_count', 0)}/"
                    f"{metric(hierarchical_racah, 'final_target_count', 0)} finite S_6 sectors. Sparse stable probes reconstruct "
                    f"{metric(sparse_gap, 'integer_characteristic_polynomial_candidate_count', 0)} integer quartics through "
                    f"n={metric(sparse_gap, 'maximum_n', 0)}."
                ),
                "next": "Prove the stable quartic coefficients and root gaps exactly, then compile the hierarchy coherently.",
            },
        ],
        "milestones": [
            {
                "title": "Toy circuit search was removed",
                "detail": "Candidates now require reductions, complexity accounting, falsifiers, classical baselines, and proof obligations before acceptance.",
            },
            {
                "title": "A nonabelian transform was split into precise subproblems",
                "detail": "Diagonal Jucys-Murphy labels are accessible, but exact multiplicity degeneracy proves that labels alone are not the internal Kronecker transform.",
            },
            {
                "title": "A restricted all-n commutant gap was proved",
                "detail": "Exact Specht polytabloids give raw gap 2(n-2) and LCU-normalized gap 2/[n(n-1)] for one stable multiplicity-two family.",
            },
            {
                "title": "The complete finite S_6 Racah table was resolved",
                "detail": "A second bounded-support Hamiltonian splits residual multiplicities up to four and produces unitary left/right matrices in all ten final sectors.",
            },
            {
                "title": "Stable sparse quartics became exact proof targets",
                "detail": "Target-only sparse extraction avoids dense Hamiltonians through n=11 and reconstructs five monic integer characteristic polynomials; no all-n formula is claimed.",
            },
        ],
        "active_conjecture": {
            "summary": (
                "For W_n=(n-2,2) and alpha_n=xi_n=(n-3,2,1), sparse multiplicity-four spectra through n=11 "
                "reconstruct monic integer quartics. Their trace fits 4n^3-46n^2+149n-118 on n=7..10 and matches "
                "the held-out n=11 value. The formula still requires an exact marked-cycle character proof."
            ),
            "facts": [
                {"label": "Pair gap", "value": "Exact inverse-quadratic theorem"},
                {"label": "Finite Racah table", "value": f"{metric(hierarchical_racah, 'complete_hierarchical_finite_racah_matrix_count', 0)}/10 S_6 sectors"},
                {"label": "Stable quartics", "value": f"n=7-{metric(sparse_gap, 'maximum_n', 0)}, integer reconstructed"},
                {"label": "Trace holdout", "value": f"{metric(stable_trace, 'holdout_match_count', 0)}/{metric(stable_trace, 'holdout_row_count', 0)} matched; proof open"},
                {"label": "Hidden decoder", "value": "Open"},
            ],
        },
        "next_actions": [
            {
                "title": "Prove the marked-cycle trace identity",
                "detail": "Evaluate the explicit shifted character sum exactly; interpolation and the n=11 holdout are theorem targets, not proof.",
            },
            {
                "title": "Recover the full stable quartic",
                "detail": "Derive traces H^2, H^3, and H^4, apply Newton identities, and prove inverse-polynomial root separation after LCU normalization.",
            },
            {
                "title": "Compile and test the actual decoder",
                "detail": "Turn nested labels into a uniform coherent circuit and show that its outcomes recover a hidden involution beyond legal graph/code baselines.",
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
