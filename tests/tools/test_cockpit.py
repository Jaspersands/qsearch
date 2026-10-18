from __future__ import annotations

import datetime as dt
import json
import textwrap

import pytest

from tools.cockpit import build_cockpit as cockpit


HANDOFF = textwrap.dedent(
    """\
    # Research Agent Handoff

    Last updated: 2026-10-18

    ## Latest: Prime-Character OPI Norm Witness

    Previous goal pass was PROGRESS. The OPI norm solver recovers the SAME
    input, so the prime-character route is NOT a speedup. No GPT commit/push.
    Gemini can expose the standalone producer in CLI/EXP wiring later.
    Verification: twelve focused tests pass in4.2s with bounds at110 bits.

    ## Prior: Investigation 12 Proved — Dihedral Hidden Shift Barrier

    A major investigation of the dihedral hidden shift problem has been completed and verified in `research/DIHEDRAL_X.md`, with the result strictly enforced everywhere in the repository.

    ### Core Invariants & Status:
    - **Speedup claim**: `speedup_claim_allowed = False` strictly enforced everywhere in the code.
    - **Registered negative result**: `NEG-DCP-FIXTURE-BARRIER` (valid with 3 negative results).
    - **Theorem 1**: The bias is $\\epsilon = 2^{-n}$ for every $n \\ge 1$ and $q$ prime, so the subset-sum sieve fails.

    ## Native DCP Tree Receiver (2026-09-02)

    Files and experiment ID:

    ```text
    theorems/dcp_native_tree_receiver.py
    ## not a heading, it sits inside a code fence
    ```

    The dcp-native-tree receiver pays for every list. It registers NEG-DCP-FIXTURE-
    WRAPPED as a scoped negative and mentions NEG-NOT-IN-REGISTRY in passing.

    ## Ternary Lattice Decoder Notes

    A plain note about a ternary lattice decoder.

    ## Verification Checkpoint

    Tests pass.
    """
)


def _sections():
    return cockpit.split_sections(HANDOFF)


# ---------- Sections ----------


def test_split_sections_ignores_headings_inside_code_fences() -> None:
    headings = [section.heading for section in _sections()]
    assert headings == [
        "Latest: Prime-Character OPI Norm Witness",
        "Prior: Investigation 12 Proved — Dihedral Hidden Shift Barrier",
        "Native DCP Tree Receiver (2026-09-02)",
        "Ternary Lattice Decoder Notes",
        "Verification Checkpoint",
    ]
    assert "## not a heading" in _sections()[2].body


def test_split_sections_records_file_order_and_line_numbers() -> None:
    sections = _sections()
    assert [section.index for section in sections] == [0, 1, 2, 3, 4]
    lines = HANDOFF.splitlines()
    for section in sections:
        assert lines[section.line - 1] == f"## {section.heading}"


@pytest.mark.parametrize(
    ("heading", "expected"),
    [
        ("Native DCP Tree Receiver (2026-09-02)", "2026-09-02"),
        ("Antigravity Mechanical Wiring Completion Note (2026-08-24 - Pass 6)", "2026-08-24"),
        ("2026-09-10 Classical Evidence Corrections", "2026-09-10"),
        ("Ternary Lattice Decoder Notes", None),
    ],
)
def test_heading_date_reads_a_date_written_in_the_heading(heading: str, expected: str | None) -> None:
    assert cockpit.heading_date(heading) == expected


# ---------- Directions ----------


@pytest.mark.parametrize(
    ("heading", "body", "direction"),
    [
        ("Finite Low-Rate DQI Mean And Tail", "", "opi"),
        ("Independent Constructive HDQI Family Tested", "The HDQI energy is classical.", "hdqi"),
        ("Coherent BPQM Erasure Stage Executed", "", "bpqm"),
        ("Fourth Pass: Public Polar Source Design", "", "bpqm"),
        ("Latest: Centered Native List-Variance Cap", "Added dcp-native-tree-variance-cap with proofs.", "dcp"),
        ("Plancherel Carrier Racah Access Boundary", "", "carrier_pgm"),
        ("Latest Theory: Native Ternary Carry Receiver", "", "lattice"),
        ("Current Result", "`theorems/self_dual_wreath_polar.py` reduces the code equivalence pair.", "code_equivalence"),
        ("Verification Checkpoint", "Tests pass.", "other"),
    ],
)
def test_classify_direction_uses_the_keyword_table(heading: str, body: str, direction: str) -> None:
    assert cockpit.classify_direction(heading, body).direction == direction


def test_classify_direction_weights_the_heading_above_body_mentions() -> None:
    result = cockpit.classify_direction("Prime-Character OPI Bound", "Compare with the DCP sieve and the lattice CVP.")
    assert result.direction == "opi"
    assert result.scores["opi"] > result.scores["dcp"]


def test_classify_direction_marks_single_mention_decisions_as_weak() -> None:
    assert cockpit.classify_direction("Some Pass", "One lattice mention.").weak is True
    assert cockpit.classify_direction("Ternary Lattice Pass", "").weak is False


def test_every_direction_has_a_label_and_other_comes_last() -> None:
    ids = [direction.id for direction in cockpit.DIRECTIONS]
    assert ids[-1] == "other"
    assert {"dcp", "opi", "bpqm", "hdqi", "carrier_pgm", "lattice", "code_equivalence"} <= set(ids)
    assert all(direction.label for direction in cockpit.DIRECTIONS)


# ---------- Agent attribution ----------


def test_attribute_agent_reads_codex_conventions() -> None:
    section = _sections()[0]
    result = cockpit.attribute_agent(section.heading, section.body)
    assert result.agent == "codex"
    assert "no GPT commit" in result.cues
    assert "Gemini in third person" in result.cues


def test_attribute_agent_reads_gemini_conventions() -> None:
    section = _sections()[1]
    result = cockpit.attribute_agent(section.heading, section.body)
    assert result.agent == "gemini"
    assert "investigation heading" in result.cues
    assert "bold spans" in result.cues


def test_attribute_agent_says_unknown_without_enough_evidence() -> None:
    for section in _sections()[2:]:
        assert cockpit.attribute_agent(section.heading, section.body).agent == "unknown"


def test_attribution_check_compares_style_cues_with_explicit_cues() -> None:
    sections = _sections()
    check = cockpit.attribution_check([cockpit.attribute_agent(s.heading, s.body) for s in sections])
    # Section 0 is explicitly Codex, section 1 explicitly Gemini.
    assert check["explicit_sections"] == 2
    assert check["agree"] + check["disagree"] + check["abstain"] == 2
    assert check["disagree"] == 0


# ---------- Registry entries and inertia ----------

REGISTRY_IDS = {"NEG-DCP-FIXTURE-BARRIER", "NEG-DCP-FIXTURE-WRAPPED", "NEG-OLD", "NEG-QUARANTINED-X"}


def test_mentioned_registry_ids_joins_ids_wrapped_across_lines() -> None:
    body = _sections()[2].body
    assert cockpit.mentioned_registry_ids(body, REGISTRY_IDS) == {"NEG-DCP-FIXTURE-WRAPPED"}


def test_mentioned_registry_ids_ignores_ids_missing_from_the_registry() -> None:
    assert cockpit.mentioned_registry_ids("See NEG-NOT-IN-REGISTRY and NEG-OLD.", REGISTRY_IDS) == {"NEG-OLD"}


def test_registry_ids_include_quarantined_records(tmp_path) -> None:
    registry = tmp_path / "research" / "registry"
    registry.mkdir(parents=True)
    (registry / "negative_results.json").write_text('[{"id": "NEG-A"}, {"id": "WEAK-B"}, {"claim": "no id"}]')
    (registry / "quarantined_campaign_negatives.json").write_text('[{"id": "NEG-Q", "status": "QUARANTINED"}]')
    assert cockpit.registry_ids(tmp_path) == {"NEG-A", "WEAK-B", "NEG-Q"}


def test_registry_ids_are_empty_without_a_registry(tmp_path) -> None:
    assert cockpit.registry_ids(tmp_path) == set()


def test_new_registry_ids_credit_only_the_oldest_section_that_mentions_an_id() -> None:
    texts = [  # chronological, oldest first
        "Registered NEG-OLD.",
        "Mentions NEG-OLD again and NEG-NOT-IN-REGISTRY.",
        "Adds NEG-DCP-FIXTURE-BARRIER and repeats NEG-OLD.",
        "Nothing new.",
    ]
    assert cockpit.new_registry_ids(texts, REGISTRY_IDS) == [
        ["NEG-OLD"],
        [],
        ["NEG-DCP-FIXTURE-BARRIER"],
        [],
    ]


def test_chronological_order_sorts_by_first_commit_then_by_file_position() -> None:
    # File order is newest first. Index 3 was committed after indexes 1 and 2; index 0 is uncommitted.
    first_committed = {0: None, 1: "2026-10-01", 2: "2026-10-01", 3: "2026-10-05"}
    assert cockpit.chronological_order(4, first_committed) == [2, 1, 3, 0]


def test_chronological_order_without_history_reverses_the_file() -> None:
    assert cockpit.chronological_order(3, {}) == [2, 1, 0]


def _rows(*items):
    return [{"index": i, "direction": d, "new_registry_ids": ids, "first_committed": None} for i, (d, ids) in enumerate(items)]


def test_inertia_counts_a_directions_own_sections_since_its_last_new_entry() -> None:
    chronological = _rows(
        ("dcp", ["NEG-A"]),
        ("dcp", []),
        ("opi", []),
        ("dcp", []),
        ("other", []),
        ("dcp", []),
        ("dcp", []),
    )
    result = cockpit.inertia(chronological, threshold=4)
    by_direction = {row["direction"]: row for row in result["directions"]}
    assert by_direction["dcp"]["streak"] == 4
    assert by_direction["dcp"]["flag"] is True
    assert by_direction["dcp"]["last_new"]["ids"] == ["NEG-A"]
    assert by_direction["opi"]["streak"] == 1
    assert by_direction["opi"]["flag"] is False
    assert by_direction["opi"]["last_new"] is None
    assert "other" not in by_direction
    assert [row["direction"] for row in result["flags"]] == ["dcp"]


def test_inertia_threshold_is_configurable_and_a_new_entry_resets_the_streak() -> None:
    chronological = _rows(("dcp", []), ("dcp", []), ("dcp", []), ("dcp", ["NEG-B"]), ("dcp", []))
    assert cockpit.inertia(chronological, threshold=3)["flags"] == []
    assert {row["direction"]: row["streak"] for row in cockpit.inertia(chronological, threshold=3)["directions"]} == {"dcp": 1}


def test_inertia_reports_how_many_sections_ago_a_direction_was_last_worked_on() -> None:
    chronological = _rows(("bpqm", []), ("dcp", []), ("dcp", []))
    rows = {row["direction"]: row for row in cockpit.inertia(chronological, threshold=8)["directions"]}
    assert rows["bpqm"]["sections_ago"] == 2
    assert rows["dcp"]["sections_ago"] == 0


def test_inertia_lists_every_past_run_at_or_over_the_threshold() -> None:
    chronological = _rows(
        ("dcp", []), ("dcp", []), ("dcp", []), ("dcp", ["NEG-A"]), ("dcp", []), ("lattice", []), ("dcp", [])
    )
    runs = cockpit.inertia(chronological, threshold=3)["runs"]
    assert runs == [
        {"direction": "dcp", "length": 3, "from_index": 0, "to_index": 2, "from_date": None, "to_date": None, "ongoing": False},
    ]


# ---------- Git history (fake git output) ----------

RS, US = cockpit.RS, cockpit.US
SHA_A, SHA_B, SHA_C = "a" * 40, "b" * 40, "c" * 40

COMMIT_LOG = (
    f"{RS}{SHA_A}{US}2026-10-18{US}Integrate prime character Morse/norm solvers\n\n"
    "theorems/prime_character_norm_attack.py\nresearch/PRIME_CHARACTER_NORM_ATTACK.md\n"
    f"{RS}{SHA_B}{US}2026-10-18{US}Add DCP native tree receiver\n\n"
    "theorems/dcp_native_tree_receiver.py\n"
    f"{RS}{SHA_C}{US}2026-10-16{US}Update README wording\n\nREADME.md\n"
)


def test_git_runner_refuses_commands_that_write(tmp_path) -> None:
    run = cockpit.git_runner(tmp_path)
    for command in ("commit", "add", "checkout", "stash", "reset", "clean", "branch"):
        with pytest.raises(ValueError):
            run(command)


def test_parse_commit_log_reads_sha_date_subject_and_files() -> None:
    commits = cockpit.parse_commit_log(COMMIT_LOG)
    assert [c["sha"] for c in commits] == [SHA_A, SHA_B, SHA_C]
    assert commits[0]["date"] == "2026-10-18"
    assert commits[0]["subject"] == "Integrate prime character Morse/norm solvers"
    assert commits[1]["files"] == ["theorems/dcp_native_tree_receiver.py"]


def test_commits_per_day_counts_commits_and_their_topics() -> None:
    days = cockpit.commits_per_day(cockpit.parse_commit_log(COMMIT_LOG))
    assert [day["date"] for day in days] == ["2026-10-16", "2026-10-18"]
    assert days[0]["count"] == 1
    assert days[0]["topics"] == {"other": 1}
    assert days[1]["topics"] == {"opi": 1, "dcp": 1}
    assert days[1]["commits"][0] == {"sha": SHA_A[:8], "subject": "Integrate prime character Morse/norm solvers", "topic": "opi"}


@pytest.mark.parametrize(
    ("subject", "files", "topic"),
    [
        # A subject that names a direction decides, whatever the paths say.
        ("Integrate prime character readout", ["theorems/dcp_a.py", "theorems/dcp_b.py", "theorems/dcp_c.py"], "opi"),
        # A plain subject takes its topic from the paths when they all point one way ...
        ("Add receiver tests", ["theorems/dcp_native_tree.py", "tests/test_dcp_native_tree.py"], "dcp"),
        # ... but a commit touching several directions stays "other".
        ("Wire batch 5 modules", ["theorems/dcp_a.py", "theorems/racah_b.py", "theorems/goppa_c.py"], "other"),
        ("Update README wording", ["README.md"], "other"),
    ],
)
def test_commit_topic_trusts_the_subject_and_only_unanimous_paths(subject, files, topic) -> None:
    assert cockpit.commit_topic(subject, files) == topic


def _snapshot(updated_at: str | None, **metrics) -> str:
    payload = {"metrics": metrics}
    if updated_at:
        payload["updated_at"] = updated_at
    return json.dumps(payload)


def test_metrics_series_keeps_the_latest_snapshot_per_date() -> None:
    versions = [  # oldest first: (sha, commit date, file text)
        (SHA_C, "2026-10-01", _snapshot(None, negative_results=900, experiments=700)),
        (SHA_B, "2026-10-02", "{ not json"),
        (SHA_A, "2026-10-03", _snapshot("2026-10-01", negative_results=905, experiments=701, results=10, note="x")),
        ("d" * 40, "2026-10-04", _snapshot("2026-10-04", negative_results=976, experiments=796, results=807)),
    ]
    series = cockpit.metrics_series(versions)
    assert series["keys"] == ["experiments", "negative_results", "results"]
    assert series["points"] == [
        {"date": "2026-10-01", "commit": SHA_A[:8], "metrics": {"negative_results": 905, "experiments": 701, "results": 10}},
        {"date": "2026-10-04", "commit": "dddddddd", "metrics": {"negative_results": 976, "experiments": 796, "results": 807}},
    ]


@pytest.mark.parametrize(
    ("heading", "key"),
    [
        ("Latest: Ternary Lattice Decoder Notes", "ternary lattice decoder notes"),
        ("Latest Theory: Native Carry Source", "native carry source"),
        ("Current High-Reasoning Result: Racah Toric Obstruction (2026-08-13)", "racah toric obstruction 2026 08 13"),
        ("Prior: Investigation 60 Proved — Quantum Simulation", "investigation 60 proved quantum simulation"),
        ("Fixed-Input Morse Norm Solver: Explicit Geometry", "fixed input morse norm solver explicit geometry"),
    ],
)
def test_heading_key_drops_status_prefixes_that_agents_rewrite(heading: str, key: str) -> None:
    assert cockpit.heading_key(heading) == key


def test_first_committed_dates_each_section_by_the_first_version_containing_it() -> None:
    old = "# H\n\n## Latest: Ternary Lattice Decoder Notes\n\nx\n\n## Old Duplicate\n\ny\n"
    newer = (
        "# H\n\n## Native DCP Tree Receiver (2026-09-02)\n\nz\n\n## Ternary Lattice Decoder Notes\n\nx\n\n"
        "## Old Duplicate\n\ny\n\n## Verification Checkpoint\n\nw\n"
    )
    current = cockpit.split_sections(
        "## New Top\n\n## Old Duplicate\n\n## Native DCP Tree Receiver (2026-09-02)\n\n"
        "## Ternary Lattice Decoder Notes\n\n## Old Duplicate\n\n## Verification Checkpoint\n"
    )
    dates = cockpit.first_committed(current, [("2026-09-01", old), ("2026-09-03", newer)])
    assert dates == {
        0: None,  # never committed
        1: None,  # the second "Old Duplicate" is new; the lower one is the committed original
        2: "2026-09-03",
        3: "2026-09-01",  # matched despite the dropped "Latest:" prefix
        4: "2026-09-01",
        5: "2026-09-03",
    }


PORCELAIN = (
    " M research/AGENT_HANDOFF.md\n"
    "M  theorems/x.py\n"
    "?? scratch/a.txt\n"
    "?? scratch/b.txt\n"
    "R  old.py -> tools/new.py\n"
    "!! ignored.txt\n"
    " M .research_checkpoint.json\n"
)


def test_dirty_summary_counts_modified_and_untracked_files_without_naming_them() -> None:
    summary = cockpit.dirty_summary(PORCELAIN)
    assert summary == {
        "modified": 4,
        "untracked": 2,
        "total": 6,
        "by_area": {"(root)": 1, "research": 1, "scratch": 2, "theorems": 1, "tools": 1},
    }
    assert "a.txt" not in json.dumps(summary)


def test_dirty_paths_lists_paths_from_porcelain() -> None:
    assert cockpit.dirty_paths(PORCELAIN) == {
        "research/AGENT_HANDOFF.md", "theorems/x.py", "scratch/a.txt", "scratch/b.txt", "tools/new.py",
        ".research_checkpoint.json",
    }


CHECKPOINT = {
    "session_date": "2026-10-16",
    "objective": "Find or falsify Shor-level ideas.",
    "active_milestone": "42-43 corrected and tested.",
    "latest_verified_subsystem": "dcp_grand_synthesis",
    "total_verified_subsystems": 66,
    "completed_subsystems": ["a", "b"],
    "scientific_review_override": {"date": "2026-10-16", "status": "SCOPED_CORRECTIONS", "next_decision": "Read the decision note."},
}


def test_checkpoint_status_summarizes_the_research_checkpoint_file(tmp_path) -> None:
    (tmp_path / ".research_checkpoint.json").write_text(json.dumps(CHECKPOINT))
    status = cockpit.checkpoint_status(
        tmp_path,
        last_commit=(SHA_B, "2026-10-18"),
        commit_shas=[SHA_A, SHA_B, SHA_C],
        dirty={".research_checkpoint.json"},
        today=dt.date(2026, 10, 19),
    )
    assert status == {
        "file": ".research_checkpoint.json",
        "session_date": "2026-10-16",
        "days_since_session": 3,
        "active_milestone": "42-43 corrected and tested.",
        "latest_verified_subsystem": "dcp_grand_synthesis",
        "total_verified_subsystems": 66,
        "completed_subsystems": 2,
        "review": {"date": "2026-10-16", "status": "SCOPED_CORRECTIONS", "next_decision": "Read the decision note."},
        "last_commit": {"sha": SHA_B[:8], "date": "2026-10-18"},
        "commits_since": 1,
        "uncommitted_changes": True,
    }


def test_checkpoint_status_is_none_without_a_checkpoint_file(tmp_path) -> None:
    assert cockpit.checkpoint_status(tmp_path, last_commit=None, commit_shas=[], dirty=set(), today=dt.date(2026, 10, 19)) is None


SPEND = {
    "generated_on": "2026-10-19",
    "days": [
        {"date": "2026-10-18", "runs": 3, "wall_seconds": 120.5, "cpu_seconds": None, "negatives_added": 1, "tokens": None},
        {"date": "2026-10-17", "runs": 1, "wall_seconds": 30.0, "cpu_seconds": 25.0, "negatives_added": 0, "tokens": 1200},
    ],
}


def test_spend_summary_is_read_when_the_file_exists(tmp_path) -> None:
    path = tmp_path / "research" / "audits" / "spend_summary.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(SPEND))
    panel, warning = cockpit.spend_summary(tmp_path)
    assert warning is None
    assert panel["generated_on"] == "2026-10-19"
    assert [day["date"] for day in panel["days"]] == ["2026-10-17", "2026-10-18"]
    assert panel["days"][1] == SPEND["days"][0]
    assert panel["source"] == "research/audits/spend_summary.json"


def test_spend_summary_is_omitted_without_error_when_the_file_is_missing(tmp_path) -> None:
    assert cockpit.spend_summary(tmp_path) == (None, None)


def test_spend_summary_reports_a_malformed_file_instead_of_failing(tmp_path) -> None:
    path = tmp_path / "research" / "audits" / "spend_summary.json"
    path.parent.mkdir(parents=True)
    path.write_text('{"days": "not a list"}')
    panel, warning = cockpit.spend_summary(tmp_path)
    assert panel is None
    assert "spend_summary.json" in warning


# ---------- Whole build ----------

OLDER_HANDOFF = HANDOFF.replace(HANDOFF[HANDOFF.index("## Latest:"):HANDOFF.index("## Prior:")], "")


class FakeGit:
    """Canned output for the read-only git commands the builder runs; None for anything else."""

    def __init__(self, responses: dict[tuple[str, ...], str]):
        self.responses = responses
        self.calls: list[tuple[str, ...]] = []

    def __call__(self, *args: str) -> str | None:
        assert args[0] in {"log", "show", "status"}, args
        self.calls.append(args)
        return self.responses.get(args)


def _fake_git() -> FakeGit:
    return FakeGit({
        cockpit.COMMIT_LOG_ARGS: COMMIT_LOG,
        cockpit.SNAPSHOT_LOG_ARGS: f"{SHA_A}{US}2026-10-18\n{SHA_C}{US}2026-10-16\n",
        ("show", f"{SHA_C}:{cockpit.SNAPSHOT}"): _snapshot("2026-10-16", negative_results=970),
        ("show", f"{SHA_A}:{cockpit.SNAPSHOT}"): _snapshot("2026-10-18", negative_results=976),
        cockpit.HANDOFF_LOG_ARGS: f"{SHA_B}{US}2026-10-18\n",
        ("show", f"{SHA_B}:{cockpit.HANDOFF}"): OLDER_HANDOFF,
        cockpit.CHECKPOINT_LOG_ARGS: f"{SHA_B}{US}2026-10-18\n",
        cockpit.STATUS_ARGS: PORCELAIN,
    })


def _fake_repo(root):
    (root / "research" / "registry").mkdir(parents=True)
    (root / cockpit.HANDOFF).write_text(HANDOFF)
    (root / cockpit.REGISTRY).write_text(json.dumps([{"id": "NEG-DCP-FIXTURE-WRAPPED"}, {"id": "NEG-OLD"}]))
    (root / cockpit.QUARANTINE).write_text(json.dumps([{"id": "NEG-DCP-FIXTURE-BARRIER"}]))
    (root / cockpit.CHECKPOINT).write_text(json.dumps(CHECKPOINT))
    return root


TODAY = dt.date(2026, 10, 19)


def test_build_assembles_every_panel(tmp_path) -> None:
    payload = cockpit.build(_fake_repo(tmp_path), git=_fake_git(), inertia_threshold=1, today=TODAY)
    assert payload["generated_on"] == "2026-10-19"
    assert payload["head"] == {"sha": SHA_A[:8], "date": "2026-10-18"}
    assert [d["id"] for d in payload["directions"]][-1] == "other"

    sections = payload["sections"]
    assert [s["index"] for s in sections] == [0, 1, 2, 3, 4]
    assert [s["direction"] for s in sections] == ["opi", "dcp", "dcp", "lattice", "other"]
    assert [s["agent"] for s in sections] == ["codex", "gemini", "unknown", "unknown", "unknown"]
    assert [s["first_committed"] for s in sections] == [None, "2026-10-18", "2026-10-18", "2026-10-18", "2026-10-18"]
    assert [s["order"] for s in sections] == [4, 3, 2, 1, 0]
    assert sections[1]["new_registry_ids"] == ["NEG-DCP-FIXTURE-BARRIER"]
    assert sections[2]["new_registry_ids"] == ["NEG-DCP-FIXTURE-WRAPPED"]
    assert sections[2]["heading_date"] == "2026-09-02"

    assert payload["coverage"]["sections"] == 5
    assert payload["coverage"]["by_direction"]["dcp"] == 2
    assert payload["coverage"]["other_share"] == 0.2
    assert payload["attribution"]["by_agent"] == {"codex": 1, "gemini": 1, "unknown": 3}
    assert payload["attribution"]["check"]["disagree"] == 0
    cues = {cue["name"]: cue for cue in payload["attribution"]["cues"]}
    assert cues["no GPT commit"] == {"name": "no GPT commit", "agent": "codex", "weight": 3, "explicit": True, "sections": 1}
    assert cues["investigation heading"]["agent"] == "gemini"
    assert cues["hard-wrapped lines"]["agent"] == "codex"
    assert cues["unwrapped lines"]["agent"] == "gemini"
    assert cues["ampersand heading"]["sections"] == 0

    assert [row["direction"] for row in payload["inertia"]["flags"]] == ["opi", "lattice"]
    assert payload["commits"]["total"] == 3
    assert len(payload["commits"]["days"]) == 2
    assert [p["metrics"]["negative_results"] for p in payload["metrics"]["points"]] == [970, 976]
    assert payload["dirty"]["total"] == 6
    assert payload["checkpoint"]["commits_since"] == 1
    assert payload["checkpoint"]["uncommitted_changes"] is True
    assert "spend" not in payload
    assert str(tmp_path) not in json.dumps(payload)


def test_build_without_history_leaves_sections_undated(tmp_path) -> None:
    git = _fake_git()
    payload = cockpit.build(_fake_repo(tmp_path), git=git, today=TODAY, history=False)
    assert all(s["first_committed"] is None for s in payload["sections"])
    assert cockpit.HANDOFF_LOG_ARGS not in git.calls


def test_build_still_works_when_git_is_unavailable(tmp_path) -> None:
    payload = cockpit.build(_fake_repo(tmp_path), git=FakeGit({}), today=TODAY)
    assert payload["head"] is None
    assert payload["commits"] == {"total": 0, "days": []}
    assert payload["metrics"] == {"keys": [], "points": []}
    assert payload["dirty"] is None
    assert payload["checkpoint"]["last_commit"] is None
    assert len(payload["sections"]) == 5


def test_build_includes_the_spend_panel_when_its_file_exists(tmp_path) -> None:
    root = _fake_repo(tmp_path)
    (root / "research" / "audits").mkdir(parents=True)
    (root / cockpit.SPEND).write_text(json.dumps(SPEND))
    payload = cockpit.build(root, git=_fake_git(), today=TODAY)
    assert [day["date"] for day in payload["spend"]["days"]] == ["2026-10-17", "2026-10-18"]


def test_main_writes_the_cockpit_json(tmp_path) -> None:
    root = _fake_repo(tmp_path)
    assert cockpit.main(["--root", str(root), "--inertia", "3"], git=_fake_git()) == 0
    payload = json.loads((root / "site" / "data" / "cockpit.json").read_text())
    assert payload["inertia"]["threshold"] == 3
    assert payload["settings"] == {"history": True, "inertia_threshold": 3}


def test_main_rejects_an_inertia_threshold_below_one(tmp_path) -> None:
    with pytest.raises(SystemExit):
        cockpit.main(["--root", str(tmp_path), "--inertia", "0"], git=FakeGit({}))
