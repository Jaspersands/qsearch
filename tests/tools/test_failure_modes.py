from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from tools.audit import failure_modes as fm


def _neg(record_id: str, reason: str, claim: str = "A quantum route gives a speedup.", lesson: str = "", **extra) -> dict:
    return {
        "id": record_id,
        "claim": claim,
        "reason_invalid": reason,
        "lesson": lesson,
        "applies_to": extra.pop("applies_to", []),
        "evidence": extra.pop("evidence", {}),
        "source": "theorems/x.py",
        **extra,
    }


@pytest.mark.parametrize(
    ("reason", "mode"),
    [
        ("A polynomial-time conductor/t-closure signature separates the code pair.", "classical_competitor"),
        ("3-vertex individualization plus color refinement separates the pair classically.", "classical_competitor"),
        ("A correlated classical block-Prange sampler matches the joint quantum erasure load.", "classical_competitor"),
        ("Every fixed signed aggregate label remains uniform, so the observable has zero bias.", "no_signal"),
        ("A PGM-style distinguishability threshold exists only after exponentially many copies.", "readout"),
        ("No polynomial start-state preparation is known for the source superposition.", "state_prep"),
        ("Each score uses O(m 2^q) residue dynamic programming at q=Theta(n), exponential time.", "resource_blowup"),
        ("The scan ends at n=24; finite instances only, with no scaling law.", "finite_size"),
        ("No compressed recurrence is proved; the required lemma remains unproven.", "proof_gap"),
        ("arbitrary oracle_secret_finding proposal; N=3 simulation cap; toy oracle with planted secret", "hidden_advice"),
        ("The barrier was stated as a universal no-go without a scoped proof; it overgeneralizes one case.", "overbroad"),
    ],
)
def test_rules_pick_the_obvious_mode(reason: str, mode: str) -> None:
    assert fm.rule_label(_neg("NEG-X", reason)).primary == mode


def test_rules_return_unclear_without_cues() -> None:
    result = fm.rule_label(_neg("NEG-X", "Recorded.", claim="Placeholder."))
    assert result.primary == "unclear"
    assert result.cues == []


def test_templated_records_are_read_through_their_evidence_keys() -> None:
    record = _neg(
        "NEG-T",
        fm.TEMPLATED_REASON,
        claim="Initial negative claim for EXP-T.",
        evidence={"finite_control_count": 5, "uniform_scaling_theorem_count": 0},
    )
    assert fm.is_templated(record)
    text = fm.record_text(record)
    assert "finite control count" in text and "uniform scaling theorem count" in text


@pytest.mark.parametrize(
    ("record_id", "tags", "track"),
    [
        ("NEG-DCP-LOCAL-HELSTROM", [], "dcp"),
        ("NEG-X", ["DHS-GOWERS-SIEVE"], "dcp"),
        ("CODE-PROFILE-COLLISION-1", ["CODE-COSET-COLLECTIVE"], "code_equivalence"),
        ("NEG-SELF-DUAL-WREATH-MASS", ["CODE-COSET-COLLECTIVE"], "code_equivalence"),
        ("COSET-PGM-THRESHOLD", ["CODE-COSET-COLLECTIVE"], "coset_observables"),
        ("CFI-BASE-FAMILY-REJECTED-K5", [], "coset_observables"),
        ("LEGACY-NOVEL-ORACLE", [], "toy_oracle"),
        ("NEG-OPI-MIXED-COSET-HARDNESS", [], "dqi_opi"),
        ("S8-SIGN-CATEGORY-WALSH-FAILURE", ["CODE-COSET-COLLECTIVE"], "coset_observables"),
        ("NEG-SELF-DUAL-WREATH-POLAR-FACTOR-TRANSFER", ["CODE-COSET-COLLECTIVE"], "code_equivalence"),
        ("NEG-POLAR-CODE-GIBBS-SOURCE", [], "bpqm_gibbs"),
        ("NEG-BARREN-PLATEAUS-VARIATIONAL-QUANTUM-HORIZON", ["BARREN-PLATEAUS"], "applied_barriers"),
        ("NEG-CONTINUOUS-SPECTRUM-QPE-SINGULAR-MEASURE-BARRIER", ["QPE-CONTINUOUS-SPECTRUM"], "applied_barriers"),
        # An HSP over a noncompact Lie group, not an applied-QC barrier, despite "continuous spectrum".
        ("NEG-SL2R-NONCOMPACT-LIE-CONTINUOUS-SPECTRUM-BARRIER", ["SL2R-HSP", "NONCOMPACT-LIE-GROUP"], "coset_observables"),
        ("NEG-WIDGET", [], "other"),
    ],
)
def test_track_for(record_id: str, tags: list[str], track: str) -> None:
    assert fm.track_for(_neg(record_id, "x", applies_to=tags)) == track


def test_groups_merge_records_that_differ_only_in_numbers() -> None:
    records = [
        _neg("A", "Baseline sweep found 0 recoveries and 13 random recoveries.", lesson="Strengthen."),
        _neg("B", "Baseline sweep found 0 recoveries and 12 random recoveries.", lesson="Strengthen."),
        _neg("C", "Something else entirely.", lesson="Strengthen."),
    ]
    groups = fm.judge_groups(records)
    assert sorted(len(ids) for ids in groups.values()) == [1, 2]


def test_export_batches_cover_each_group_once(tmp_path: Path) -> None:
    records = [_neg(f"R{i}", f"reason number {chr(97 + i)}") for i in range(7)]
    paths = fm.export_batches(records, tmp_path, n_batches=3)
    assert len(paths) == 3
    keys = [item["key"] for path in paths for item in json.loads(path.read_text())["items"]]
    assert len(keys) == len(set(keys)) == 7
    item = json.loads(paths[0].read_text())["items"][0]
    assert {"key", "ids", "claim", "reason_invalid", "lesson", "evidence"} <= set(item)


def test_import_judgements_expands_groups_and_rejects_unknown_modes(tmp_path: Path) -> None:
    records = [_neg("A", "same reason"), _neg("B", "same reason"), _neg("C", "other reason")]
    batch = fm.export_batches(records, tmp_path / "in", n_batches=1)[0]
    items = json.loads(batch.read_text())["items"]
    out = tmp_path / "out.jsonl"
    out.write_text(
        "\n".join(
            json.dumps({"key": item["key"], "primary": "proof_gap", "secondary": ["finite_size"], "quote": "same"})
            for item in items
        )
    )
    labels = fm.import_judgements(records, [out], judge="test")
    assert set(labels) == {"A", "B", "C"}
    assert labels["A"] == {"primary": "proof_gap", "secondary": ["finite_size"], "quote": "same", "judge": "test"}
    bad = tmp_path / "bad.jsonl"
    bad.write_text(json.dumps({"key": items[0]["key"], "primary": "vibes", "secondary": [], "quote": ""}))
    with pytest.raises(ValueError):
        fm.import_judgements(records, [bad], judge="test")


def test_agreement_reports_strict_lenient_and_per_mode_scores() -> None:
    rule = {"A": "proof_gap", "B": "readout", "C": "no_signal", "D": "proof_gap"}
    judge = {
        "A": {"primary": "proof_gap", "secondary": []},
        "B": {"primary": "state_prep", "secondary": ["readout"]},
        "C": {"primary": "classical_competitor", "secondary": []},
        "D": {"primary": "proof_gap", "secondary": []},
    }
    score = fm.agreement(rule, judge)
    assert score["n"] == 4
    assert score["strict"] == pytest.approx(0.5)
    assert score["lenient"] == pytest.approx(0.75)
    assert score["per_mode"]["proof_gap"] == {"precision": 1.0, "recall": 1.0, "support": 2}
    assert score["per_mode"]["readout"]["precision"] == 0.0


def test_first_seen_reads_registry_git_history(tmp_path: Path) -> None:
    repo = tmp_path / "git"
    path = repo / "research" / "registry" / "negative_results.json"
    path.parent.mkdir(parents=True)

    def commit(records: list[dict], date: str) -> None:
        path.write_text(json.dumps(records))
        env = {**os.environ, "GIT_AUTHOR_DATE": f"{date}T12:00:00", "GIT_COMMITTER_DATE": f"{date}T12:00:00"}
        subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True, env=env)
        subprocess.run(
            ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", date],
            check=True,
            env=env,
        )

    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    commit([{"id": "A"}], "2026-08-01")
    commit([{"id": "A"}, {"id": "B"}], "2026-09-15")
    path.write_text(json.dumps([{"id": "A"}, {"id": "B"}, {"id": "C"}]))
    assert fm.first_seen(repo) == {"A": "2026-08-01", "B": "2026-09-15"}


def test_first_seen_outside_git_is_empty(tmp_path: Path) -> None:
    assert fm.first_seen(tmp_path) == {}


def test_analyse_prefers_judge_labels_and_renders_report() -> None:
    records = [
        _neg("NEG-DCP-A", "The scan ends at n=24; finite instances only."),
        _neg("CODE-B", "A polynomial-time canonicalization separates the code pair."),
        _neg("NEG-DCP-C", "Recorded."),
    ]
    judgements = {"labels": {"NEG-DCP-A": {"primary": "proof_gap", "secondary": ["finite_size"], "quote": "q", "judge": "j"}}}
    analysis = fm.analyse(records, judgements, {"NEG-DCP-A": "2026-08-01", "CODE-B": "2026-10-11"})
    rows = {row["id"]: row for row in analysis["records"]}
    assert rows["NEG-DCP-A"]["mode"] == "proof_gap" and rows["NEG-DCP-A"]["label_source"] == "judge"
    assert rows["CODE-B"]["mode"] == "classical_competitor" and rows["CODE-B"]["label_source"] == "rule"
    assert rows["NEG-DCP-C"]["mode"] == "unclear"
    assert analysis["counts"]["proof_gap"] == 1
    assert analysis["by_track"]["dcp"]["proof_gap"] == 1
    assert analysis["trend"]["2026-08"]["proof_gap"] == 1
    assert analysis["rule_agreement"]["n"] == 1
    report = fm.render(analysis)
    for heading in ("## Where proposals die", "## By track", "## Over time", "## How far to trust the labels", "## Pre-filters"):
        assert heading in report


def test_second_opinion_agreement_counts_judged_groups_not_expanded_records() -> None:
    # Four records share one reason (one group); two more are singletons.
    records = [_neg(f"G{i}", "shared reason text") for i in range(4)] + [_neg("S1", "first lone reason"), _neg("S2", "second lone reason")]
    first = {f"G{i}": {"primary": "proof_gap", "secondary": []} for i in range(4)}
    first |= {"S1": {"primary": "readout", "secondary": []}, "S2": {"primary": "state_prep", "secondary": []}}
    second = {f"G{i}": {"primary": "proof_gap", "secondary": []} for i in range(4)}
    second |= {"S1": {"primary": "finite_size", "secondary": []}, "S2": {"primary": "finite_size", "secondary": []}}
    analysis = fm.analyse(records, {"labels": first, "second_opinion": second}, {})
    opinion = analysis["second_opinion"]
    assert opinion["n"] == 3 and opinion["records"] == 6
    assert opinion["strict"] == pytest.approx(1 / 3, abs=1e-4)
    report = fm.render(analysis)
    assert "3 groups" in report and "independent" not in report


def test_cli_writes_outputs_without_judgements(fake_repo: Path) -> None:
    assert fm.main(["--root", str(fake_repo)]) == 0
    out = json.loads((fake_repo / "research" / "audits" / "failure_modes.json").read_text())
    assert out["total"] == 2
    assert {row["label_source"] for row in out["records"]} == {"rule"}
    assert (fake_repo / "research" / "audits" / "FAILURE_MODE_META_ANALYSIS.md").exists()
