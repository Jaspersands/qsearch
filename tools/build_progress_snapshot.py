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
                "Every speedup claim remains blocked. The project has isolated one concrete representation-theoretic "
                "gap conjecture, while current hidden-shift and code-equivalence families have failed their classical tests."
            ),
        },
        "overview": (
            "The project is now useful primarily as a research filter. It has replaced tiny-circuit search with "
            "proof obligations, access-model accounting, classical attacks, exact finite representation theory, "
            "and a permanent negative-result memory. The strongest surviving lead is not an algorithm: it is a "
            "specific spectral-gap theorem that could unlock one missing transform in a nonabelian HSP route."
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
                    f"{metric(commutant, 'maximum_kronecker_multiplicity', 5)}."
                ),
                "next": "Prove the uniform normalized-gap formula, then attack coherent Racah transforms.",
            },
        ],
        "milestones": [
            {
                "title": "Toy circuit search was removed",
                "detail": "Candidates now require reductions, complexity accounting, falsifiers, classical baselines, and proof obligations before acceptance.",
            },
            {
                "title": "The density-one decoder optimism was reduced",
                "detail": "Exact all-target and witness-path experiments showed why fixed-depth lattice lists look good at small sizes and fail in the tail.",
            },
            {
                "title": "The current code frontier was classically exhausted",
                "detail": "Successive invariants and exact reductions eliminated every generated row as a hard quantum target.",
            },
            {
                "title": "A nonabelian transform was split into precise subproblems",
                "detail": "Diagonal Jucys-Murphy labels are accessible, but exact multiplicity degeneracy proves that labels alone are not the internal Kronecker transform.",
            },
            {
                "title": "Finite multiplicity blocks were split",
                "detail": "A polynomial-description commutant Hamiltonian splits all audited blocks, including multiplicity five, after charging its LCU normalization.",
            },
        ],
        "active_conjecture": {
            "summary": (
                "For lambda = mu = (n-2,2), one fixed transposition/3-cycle orbit Hamiltonian appears to have raw gap "
                "2(n-2) on the multiplicity-two target (n-3,2,1). With exactly n(n-1)(n-2) LCU terms, the normalized gap is inverse quadratic."
            ),
            "facts": [
                {"label": "Finite verification", "value": f"{gap_rows or 5}/{gap_total or 5} rows, {gap_range}"},
                {"label": "All-n proof", "value": "Open"},
                {"label": "Associator", "value": "Open"},
                {"label": "Hidden decoder", "value": "Open"},
            ],
        },
        "next_actions": [
            {
                "title": "Prove or kill the commutant gap formula",
                "detail": "Compute the exact 2x2 multiplicity action using the 2-subset permutation module, partition algebra, or orbit-character traces.",
            },
            {
                "title": "Construct overlapping Racah operations",
                "detail": "A one-tree multiplicity basis is insufficient because the three-copy overlapping class sums provably do not commute.",
            },
            {
                "title": "Demand an end-to-end natural-problem decoder",
                "detail": "No representation label or finite spectrum matters unless it recovers a hidden involution and beats legal graph/code baselines.",
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
