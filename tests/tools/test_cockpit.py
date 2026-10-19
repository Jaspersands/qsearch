from __future__ import annotations

import datetime as dt
import json
import subprocess
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


def ts(day: str, hour: int = 12, minute: int = 0) -> str:
    """A git %ct value (seconds since the epoch) for a UTC date and time."""
    when = dt.datetime.fromisoformat(f"{day}T{hour:02d}:{minute:02d}:00+00:00")
    return str(int(when.timestamp()))


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


def test_split_sections_recognises_tilde_fences() -> None:
    sections = cockpit.split_sections("## One\n\n~~~\n## not a heading\n~~~\n\n## Two\n")
    assert [section.heading for section in sections] == ["One", "Two"]
    assert "## not a heading" in sections[0].body


def test_split_sections_does_not_close_a_fence_with_the_other_fence_character() -> None:
    text = "## One\n\n````md\n~~~\n## still code\n```\n## also code\n````\n\n## Two\n"
    assert [section.heading for section in cockpit.split_sections(text)] == ["One", "Two"]


def test_an_unclosed_fence_ends_at_the_next_heading_instead_of_swallowing_the_file() -> None:
    text = "## One\n\n```python\nx = 1\n\n## Two\n\nbody\n\n## Three\n\n```text\ncode\n```\n\n## Four\n"
    sections = cockpit.split_sections(text)
    assert [section.heading for section in sections] == ["One", "Two", "Three", "Four"]
    assert "x = 1" in sections[0].body


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
    # Section 0 names Codex, but its style cues alone (glued numerals, caps) score 2, under the bar: abstain.
    # Section 1 names Gemini, and its style cues alone (dash, bold, LaTeX, stock phrase) agree.
    assert check == {"explicit_sections": 2, "agree": 1, "disagree": 0, "abstain": 1}


# ---------- Registry ids quoted in the handoff ----------

REGISTRY_IDS = {"NEG-DCP-FIXTURE-BARRIER", "NEG-DCP-FIXTURE-WRAPPED", "NEG-OLD", "NEG-QUARANTINED-X"}


def test_mentioned_registry_ids_joins_ids_wrapped_across_lines() -> None:
    body = _sections()[2].body
    assert cockpit.mentioned_registry_ids(body, REGISTRY_IDS) == {"NEG-DCP-FIXTURE-WRAPPED"}


def test_mentioned_registry_ids_ignores_ids_missing_from_the_registry() -> None:
    assert cockpit.mentioned_registry_ids("See NEG-NOT-IN-REGISTRY and NEG-OLD.", REGISTRY_IDS) == {"NEG-OLD"}


def test_mentioned_registry_ids_matches_double_hyphen_ids() -> None:
    ids = {"NEG--HIDDEN-INVOLUTION-SUPPORT-FILTER-NO-GO"}
    assert cockpit.mentioned_registry_ids("Adds `NEG--HIDDEN-INVOLUTION-SUPPORT-FILTER-NO-GO`.", ids) == ids


def test_mentioned_registry_ids_does_not_read_a_longer_token_as_a_shorter_id() -> None:
    ids = {"NEG-A-B", "NEG-A-B-C"}
    assert cockpit.mentioned_registry_ids("Only NEG-A-B-v2 and NEG-A-B_X here.", ids) == set()
    assert cockpit.mentioned_registry_ids("NEG-A-B-C, then (NEG-A-B).", ids) == {"NEG-A-B", "NEG-A-B-C"}


def test_registry_ids_include_quarantined_records(tmp_path) -> None:
    registry = tmp_path / "research" / "registry"
    registry.mkdir(parents=True)
    (registry / "negative_results.json").write_text('[{"id": "NEG-A"}, {"id": "WEAK-B"}, {"claim": "no id"}]')
    (registry / "quarantined_campaign_negatives.json").write_text('[{"id": "NEG-Q", "status": "QUARANTINED"}]')
    assert cockpit.registry_ids(tmp_path) == {"NEG-A", "WEAK-B", "NEG-Q"}


def test_registry_ids_are_empty_without_a_registry(tmp_path) -> None:
    assert cockpit.registry_ids(tmp_path) == set()


INVESTIGATION = "## Investigation 49 Proved — ETH Barrier\n\nRegistered negative result: `NEG-ETH-BARRIER`.\n"
INVESTIGATION_REWORDED = "## Investigation 49 Proved — ETH Barrier\n\nRegistered negative result: the ETH local-observable barrier.\n"
CODEX_PASS = "## Codex DCP Pass\n\nThe ETH barrier NEG-ETH-BARRIER does not touch the DCP sieve.\n\n"


def test_first_quoted_credits_the_section_that_quoted_an_id_in_the_first_committed_version() -> None:
    # The Gemini section that added the id later rewrote its line; today only a newer Codex section quotes it.
    current_text = CODEX_PASS + INVESTIGATION_REWORDED
    current = cockpit.split_sections(current_text)
    versions = [("2026-10-12", INVESTIGATION), ("2026-10-18", current_text)]
    quotes, stats = cockpit.first_quoted(current, versions, {"NEG-ETH-BARRIER"}, order=[1, 0])
    assert quotes == {0: [], 1: ["NEG-ETH-BARRIER"]}
    assert stats == {"from_history": 1, "from_current_text": 0, "lost": 0}


def test_first_quoted_prefers_a_section_new_in_that_version_over_an_older_one_edited_in_it() -> None:
    old = "## Old Survey\n\nNothing registered yet.\n"
    both = "## New Barrier\n\nRegisters NEG-X.\n\n## Old Survey\n\nNow also cites NEG-X.\n"
    current = cockpit.split_sections(both)
    quotes, _ = cockpit.first_quoted(current, [("2026-10-01", old), ("2026-10-02", both)], {"NEG-X"}, order=[1, 0])
    assert quotes == {0: ["NEG-X"], 1: []}


def test_first_quoted_reports_ids_whose_crediting_section_is_gone() -> None:
    current = cockpit.split_sections("## Later Note\n\nCites NEG-X again.\n")
    versions = [("2026-10-01", "## Removed Note\n\nRegisters NEG-X.\n")]
    quotes, stats = cockpit.first_quoted(current, versions, {"NEG-X"}, order=[0])
    assert quotes == {0: []}
    assert stats == {"from_history": 0, "from_current_text": 0, "lost": 1}


def test_first_quoted_falls_back_to_the_current_text_for_ids_no_commit_quotes() -> None:
    current = cockpit.split_sections("## Uncommitted\n\nRegisters NEG-Y and NEG-OLD.\n\n## Old\n\nCites NEG-OLD.\n")
    versions = [("2026-10-01", "## Old\n\nCites NEG-OLD.\n")]
    quotes, stats = cockpit.first_quoted(current, versions, {"NEG-Y", "NEG-OLD"}, order=[1, 0])
    assert quotes == {0: ["NEG-Y"], 1: ["NEG-OLD"]}
    assert stats == {"from_history": 1, "from_current_text": 1, "lost": 0}


def test_first_quoted_without_history_credits_the_oldest_current_mention() -> None:
    current = cockpit.split_sections("## B\n\nNEG-OLD\n\n## A\n\nNEG-OLD\n")
    quotes, stats = cockpit.first_quoted(current, [], {"NEG-OLD"}, order=[1, 0])
    assert quotes == {0: [], 1: ["NEG-OLD"]}
    assert stats == {"from_history": 0, "from_current_text": 1, "lost": 0}


# ---------- Registry growth from the registry's own history ----------


def _registry(*records: tuple[str, str, list[str]]) -> str:
    return json.dumps([{"id": rid, "claim": claim, "applies_to": tags} for rid, claim, tags in records])


BASE = ("NEG-BASE", "An old record from before the handoff.", [])
SIEVE = ("NEG-SIEVE-X", "The Kuperberg sieve does not beat the classical bound.", [])
COSET = ("NEG-COSET-Y", "No keyword from the table here.", ["PO-MEASUREMENT"])
HULL = ("CODE-HULL-Z", "Support splitting fails on these codes.", ["GOPPA"])
LOCAL = ("NEG-LOCAL-W", "A ternary lattice decoder bound.", [])


def test_record_direction_reads_the_records_id_claim_and_tags() -> None:
    assert cockpit.record_direction({"id": "NEG-SIEVE-X", "claim": SIEVE[1]}).direction == "dcp"
    assert cockpit.record_direction({"id": "CODE-X", "claim": "x", "applies_to": ["GOPPA", 3]}).direction == "code_equivalence"
    assert cockpit.record_direction({"id": "NEG-COSET-Y", "claim": COSET[1], "applies_to": COSET[2]}).direction == "unclassified"


def test_registry_gains_date_each_record_by_the_first_committed_version_containing_it() -> None:
    versions = [  # oldest first: (sha, UTC commit date, file text)
        ("c" * 40, "2026-08-01", _registry(BASE)),
        ("b" * 40, "2026-08-05", _registry(BASE, SIEVE, COSET)),
        ("a" * 40, "2026-08-09", "{ not json"),
        ("d" * 40, "2026-08-10", _registry(BASE, SIEVE, HULL)),  # COSET removed later: still a gain on 08-05
    ]
    current = json.loads(_registry(BASE, SIEVE, HULL, LOCAL))
    gains = cockpit.registry_gains(versions, current)
    assert gains["versions"] == 3
    assert gains["baseline"] == {"date": "2026-08-01", "records": 1}
    assert gains["gains"] == [
        {"id": "NEG-SIEVE-X", "date": "2026-08-05", "direction": "dcp", "weak": True},  # one body mention
        {"id": "NEG-COSET-Y", "date": "2026-08-05", "direction": "unclassified", "weak": False},
        {"id": "CODE-HULL-Z", "date": "2026-08-10", "direction": "code_equivalence", "weak": False},
        {"id": "NEG-LOCAL-W", "date": None, "direction": "lattice", "weak": True},  # only in the working tree
    ]


def test_registry_gains_are_none_without_a_committed_registry() -> None:
    assert cockpit.registry_gains([], None) is None
    assert cockpit.registry_gains([("a" * 40, "2026-08-01", "{ broken")], None) is None


def test_registry_summary_counts_gains_by_direction_and_day() -> None:
    gains = {
        "versions": 3,
        "baseline": {"date": "2026-08-01", "records": 1},
        "gains": [
            {"id": "NEG-SIEVE-X", "date": "2026-08-05", "direction": "dcp", "weak": False},
            {"id": "NEG-COSET-Y", "date": "2026-08-05", "direction": "unclassified", "weak": False},
            {"id": "CODE-HULL-Z", "date": "2026-08-10", "direction": "code_equivalence", "weak": True},
            {"id": "NEG-LOCAL-W", "date": None, "direction": "lattice", "weak": False},
        ],
    }
    summary = cockpit.registry_summary(gains)
    assert summary["source"] == "research/registry/negative_results.json"
    assert summary["baseline"] == {"date": "2026-08-01", "records": 1}
    assert summary["versions"] == 3
    assert summary["added"] == 3
    assert summary["uncommitted"] == 1
    assert summary["unclassified"] == 1
    assert summary["weak"] == 1
    assert summary["last_gain"] == "2026-08-10"
    assert summary["by_direction"] == {
        "hdqi": 0, "opi": 0, "bpqm": 0, "dcp": 1, "carrier_pgm": 0, "lattice": 1, "code_equivalence": 1, "unclassified": 1,
    }
    assert summary["days"] == [
        {"date": "2026-08-05", "records": 2, "by_direction": {"dcp": 1, "unclassified": 1}},
        {"date": "2026-08-10", "records": 1, "by_direction": {"code_equivalence": 1}},
        {"date": None, "records": 1, "by_direction": {"lattice": 1}},
    ]


# ---------- Chronology and inertia ----------


def test_chronological_order_sorts_by_first_commit_then_by_file_position() -> None:
    # File order is newest first. Index 3 was committed after indexes 1 and 2; index 0 is uncommitted.
    first_committed = {0: None, 1: "2026-10-01", 2: "2026-10-01", 3: "2026-10-05"}
    assert cockpit.chronological_order(4, first_committed) == [2, 1, 3, 0]


def test_chronological_order_without_history_reverses_the_file() -> None:
    assert cockpit.chronological_order(3, {}) == [2, 1, 0]


def _rows(*items):
    """Chronological rows from (direction, first committed date or None)."""
    return [{"index": i, "direction": d, "first_committed": day, "heading": f"S{i}"} for i, (d, day) in enumerate(items)]


def _gain(direction: str, day: str | None, rid: str = "NEG-A") -> dict:
    return {"id": rid, "date": day, "direction": direction, "weak": False}


def test_inertia_counts_a_directions_sections_since_the_registry_last_gained_a_record_in_it() -> None:
    chronological = _rows(
        ("dcp", "2026-10-01"),
        ("dcp", "2026-10-02"),  # committed on the gain day: not counted
        ("opi", "2026-10-03"),
        ("dcp", "2026-10-03"),
        ("other", "2026-10-04"),
        ("dcp", "2026-10-05"),
        ("dcp", None),  # not committed yet: newest
    )
    gains = [_gain("dcp", "2026-10-02", "NEG-A"), _gain("dcp", "2026-10-02", "NEG-B"), _gain("unclassified", "2026-10-04")]
    result = cockpit.inertia(chronological, threshold=3, gains=gains)
    assert result["available"] is True
    by_direction = {row["direction"]: row for row in result["directions"]}
    assert by_direction["dcp"]["streak"] == 3
    assert by_direction["dcp"]["flag"] is True
    assert by_direction["dcp"]["last_gain"] == {"date": "2026-10-02", "records": 2, "ids": ["NEG-A", "NEG-B"]}
    assert by_direction["dcp"]["gained"] == 2
    assert by_direction["opi"]["streak"] == 1
    assert by_direction["opi"]["flag"] is False
    assert by_direction["opi"]["last_gain"] is None
    assert "other" not in by_direction
    assert [row["direction"] for row in result["flags"]] == ["dcp"]


def test_inertia_streak_is_zero_when_the_registry_gained_a_record_after_the_last_section() -> None:
    chronological = _rows(("dcp", "2026-10-01"), ("dcp", "2026-10-01"), ("dcp", "2026-10-01"))
    result = cockpit.inertia(chronological, threshold=3, gains=[_gain("dcp", "2026-10-03")])
    assert result["directions"][0]["streak"] == 0
    assert result["flags"] == []
    assert result["runs"] == [{
        "direction": "dcp", "length": 3, "from_index": 0, "to_index": 2, "from_date": "2026-10-01",
        "to_date": "2026-10-01", "after_gain": None, "ended_by_gain": "2026-10-03", "ongoing": False,
    }]


def test_inertia_runs_are_split_by_registry_gains_in_their_own_direction_only() -> None:
    chronological = _rows(
        ("dcp", "2026-08-01"), ("dcp", "2026-08-02"), ("dcp", "2026-08-03"),
        ("dcp", "2026-08-04"),  # gain day
        ("lattice", "2026-08-04"),
        ("dcp", "2026-08-06"), ("dcp", "2026-08-07"), ("dcp", None),
    )
    gains = [_gain("dcp", "2026-08-04"), _gain("lattice", "2026-08-05"), _gain("code_equivalence", "2026-08-06")]
    result = cockpit.inertia(chronological, threshold=3, gains=gains)
    rows = {row["direction"]: row for row in result["directions"]}
    assert rows["dcp"]["streak"] == 3
    assert rows["lattice"]["streak"] == 0
    assert result["runs"] == [
        {"direction": "dcp", "length": 3, "from_index": 0, "to_index": 2, "from_date": "2026-08-01",
         "to_date": "2026-08-03", "after_gain": None, "ended_by_gain": "2026-08-04", "ongoing": False},
        {"direction": "dcp", "length": 3, "from_index": 5, "to_index": 7, "from_date": "2026-08-06",
         "to_date": None, "after_gain": "2026-08-04", "ended_by_gain": None, "ongoing": True},
    ]


def test_no_reported_run_spans_a_day_on_which_its_direction_gained_a_record() -> None:
    # The reviewer's counterexample: 24 code-equivalence sections over a stretch in which the registry gained
    # code-equivalence records on three days. Quoted ids would call all 24 one run; registry growth splits it.
    days = [f"2026-08-{day:02d}" for day in range(6, 30)]
    chronological = _rows(*[("code_equivalence", day) for day in days])
    gains = [_gain("code_equivalence", day, f"CODE-{day}") for day in ("2026-08-08", "2026-08-09", "2026-08-10")]
    result = cockpit.inertia(chronological, threshold=8, gains=gains)
    assert [(run["length"], run["from_date"], run["to_date"]) for run in result["runs"]] == [(19, "2026-08-11", "2026-08-29")]
    for run in result["runs"]:
        assert not [gain for gain in gains if run["from_date"] <= gain["date"] <= run["to_date"]]


def test_inertia_counts_uncommitted_registry_records_as_the_newest_gain() -> None:
    chronological = _rows(("dcp", "2026-10-01"), ("dcp", "2026-10-02"), ("dcp", None))
    result = cockpit.inertia(chronological, threshold=1, gains=[_gain("dcp", None, "NEG-NEW")])
    row = result["directions"][0]
    assert row["streak"] == 0
    assert row["last_gain"] == {"date": None, "records": 1, "ids": ["NEG-NEW"]}


def test_inertia_reports_how_many_sections_ago_a_direction_was_last_worked_on() -> None:
    chronological = _rows(("bpqm", "2026-10-01"), ("dcp", "2026-10-01"), ("dcp", "2026-10-01"))
    rows = {row["direction"]: row for row in cockpit.inertia(chronological, threshold=8, gains=[])["directions"]}
    assert rows["bpqm"]["sections_ago"] == 2
    assert rows["dcp"]["sections_ago"] == 0


def test_inertia_is_unavailable_without_registry_history() -> None:
    result = cockpit.inertia(_rows(("dcp", None)), threshold=8, gains=None)
    assert result == {"available": False, "threshold": 8, "directions": [], "flags": [], "runs": []}


def test_registry_days_mark_sections_committed_on_a_gain_day_in_their_direction() -> None:
    rows = _rows(("dcp", "2026-10-01"), ("dcp", "2026-10-02"), ("lattice", "2026-10-02"), ("other", "2026-10-02"), ("dcp", None))
    gains = [_gain("dcp", "2026-10-02"), _gain("unclassified", "2026-10-02")]
    assert cockpit.registry_days(rows, gains) == {0: False, 1: True, 2: False, 3: False, 4: False}


# ---------- Git (fake git output) ----------

RS, US = cockpit.RS, cockpit.US
SHA_A, SHA_B, SHA_C, SHA_D = "a" * 40, "b" * 40, "c" * 40, "d" * 40

COMMIT_LOG = (
    f"{RS}{SHA_A}{US}{ts('2026-10-18')}{US}Integrate prime character Morse/norm solvers\n\n"
    "theorems/prime_character_norm_attack.py\nresearch/PRIME_CHARACTER_NORM_ATTACK.md\n"
    f"{RS}{SHA_B}{US}{ts('2026-10-18', 9)}{US}Add DCP native tree receiver\n\n"
    "theorems/dcp_native_tree_receiver.py\n"
    f"{RS}{SHA_C}{US}{ts('2026-10-16')}{US}Update README wording\n\nREADME.md\n"
)


@pytest.mark.parametrize(
    "args",
    [
        (),
        ("commit",), ("add", "."), ("checkout", "main"), ("stash",), ("reset", "--hard"), ("clean", "-fd"), ("branch", "x"),
        ("log", "-p", "--output=/tmp/x"),
        (*cockpit.HANDOFF_LOG_ARGS[:2], "--output=/tmp/x", *cockpit.HANDOFF_LOG_ARGS[2:]),
        (*cockpit.STATUS_ARGS, "-o", "/tmp/x"),
        ("show", f"{SHA_A}:{cockpit.HANDOFF}", "--output=/tmp/x"),
        ("show", "--output=/tmp/x"),
        ("show", f"HEAD:{cockpit.HANDOFF}"),
        ("show", f"{SHA_A}:../outside.txt"),
        ("rev-parse", "--git-dir"),
    ],
)
def test_git_runner_refuses_every_argument_shape_the_builder_does_not_use(tmp_path, args) -> None:
    assert cockpit.allowed_git_args(args) is False
    with pytest.raises(ValueError):
        cockpit.git_runner(tmp_path)(*args)


def test_git_runner_allows_the_builders_own_commands() -> None:
    for args in (
        cockpit.COMMIT_LOG_ARGS, cockpit.SNAPSHOT_LOG_ARGS, cockpit.HANDOFF_LOG_ARGS, cockpit.REGISTRY_LOG_ARGS,
        cockpit.CHECKPOINT_LOG_ARGS, cockpit.STATUS_ARGS, cockpit.SHALLOW_ARGS,
        ("show", f"{SHA_A}:{cockpit.HANDOFF}"), ("show", f"{SHA_B}:{cockpit.SNAPSHOT}"), ("show", f"{SHA_C}:{cockpit.REGISTRY}"),
    ):
        assert cockpit.allowed_git_args(args) is True, args


def test_git_runner_decodes_output_that_is_not_utf8(tmp_path, monkeypatch) -> None:
    def fake_run(command, **kwargs):
        assert not kwargs.get("text")
        return subprocess.CompletedProcess(command, 0, stdout=b"## Heading \xff\xfe\n", stderr=b"")

    monkeypatch.setattr(cockpit.subprocess, "run", fake_run)
    assert cockpit.git_runner(tmp_path)(*cockpit.STATUS_ARGS) == "## Heading ��\n"


def test_utc_day_dates_a_commit_timestamp_in_utc() -> None:
    # 23:30 on Oct 18 in UTC-7 is 06:30 on Oct 19 in UTC; %cs would have said Oct 18.
    assert cockpit.utc_day(ts("2026-10-19", 6, 30)) == "2026-10-19"
    assert cockpit.utc_day("not a number") is None


def test_parse_commit_log_reads_sha_utc_date_subject_and_files() -> None:
    commits = cockpit.parse_commit_log(COMMIT_LOG)
    assert [c["sha"] for c in commits] == [SHA_A, SHA_B, SHA_C]
    assert commits[0]["date"] == "2026-10-18"
    assert commits[0]["subject"] == "Integrate prime character Morse/norm solvers"
    assert commits[1]["files"] == ["theorems/dcp_native_tree_receiver.py"]
    late = cockpit.parse_commit_log(f"{RS}{SHA_D}{US}{ts('2026-10-19', 6, 30)}{US}Late commit\n\nREADME.md\n")
    assert late[0]["date"] == "2026-10-19"


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
        (SHA_D, "2026-10-04", _snapshot("2026-10-04", negative_results=976, experiments=796, results=807)),
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


def test_head_lines_number_each_section_as_it_stands_in_the_head_commit() -> None:
    current = cockpit.split_sections("## New Top\n\nx\n\n## Kept\n\ny\n\n## Also Kept\n")
    head_text = "# Title\n\n## Kept\n\ny\n\n## Also Kept\n"
    assert cockpit.head_lines(current, head_text) == {0: None, 1: 3, 2: 7}
    assert cockpit.head_lines(current, None) == {0: None, 1: None, 2: None}


PORCELAIN = (
    " M research/AGENT_HANDOFF.md\n"
    "M  theorems/x.py\n"
    "?? scratch/a.txt\n"
    "?? scratch/b.txt\n"
    "R  old.py -> tools/new.py\n"
    "!! ignored.txt\n"
    " M .research_checkpoint.json\n"
)


def test_dirty_summary_publishes_totals_only() -> None:
    summary = cockpit.dirty_summary(PORCELAIN)
    assert summary == {"modified": 4, "untracked": 2, "total": 6}
    text = json.dumps(summary)
    assert "scratch" not in text and "a.txt" not in text and "theorems" not in text


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


def test_checkpoint_status_says_unknown_for_local_edits_without_git_status(tmp_path) -> None:
    (tmp_path / ".research_checkpoint.json").write_text(json.dumps(CHECKPOINT))
    status = cockpit.checkpoint_status(tmp_path, last_commit=None, commit_shas=[], dirty=None, today=dt.date(2026, 10, 19))
    assert status["uncommitted_changes"] is None
    assert status["commits_since"] is None


def test_checkpoint_status_is_none_without_a_checkpoint_file(tmp_path) -> None:
    assert cockpit.checkpoint_status(tmp_path, last_commit=None, commit_shas=[], dirty=set(), today=dt.date(2026, 10, 19)) is None


SPEND = {
    "generated_on": "2026-10-19",
    "days": [
        {"date": "2026-10-18", "runs": 3, "wall_seconds": 120.5, "cpu_seconds": None, "negatives_added": 1, "tokens": None},
        {"date": "2026-10-17", "runs": 1, "wall_seconds": 30.0, "cpu_seconds": 25.0, "negatives_added": 0, "tokens": 1200},
        {"date": "2026-10-16", "runs": 4, "wall_seconds": 0.0, "cpu_seconds": None, "negatives_added": 0, "tokens": 900},
    ],
}


def test_spend_summary_is_read_when_the_file_exists(tmp_path) -> None:
    path = tmp_path / "research" / "audits" / "spend_summary.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(SPEND))
    panel, warning = cockpit.spend_summary(tmp_path)
    assert warning is None
    assert panel["generated_on"] == "2026-10-19"
    assert [day["date"] for day in panel["days"]] == ["2026-10-16", "2026-10-17", "2026-10-18"]
    assert panel["days"][2] == SPEND["days"][0]
    assert panel["source"] == "research/audits/spend_summary.json"


def test_spend_summary_does_not_report_zero_wall_time_for_days_without_timed_runs(tmp_path) -> None:
    # The spend summary writes wall_seconds 0.0 and cpu_seconds null for a day with no timed run.
    path = tmp_path / "research" / "audits" / "spend_summary.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(SPEND))
    panel, _ = cockpit.spend_summary(tmp_path)
    assert panel["days"][0]["wall_seconds"] is None
    assert panel["days"][0]["cpu_seconds"] is None
    assert panel["days"][1]["wall_seconds"] == 30.0


def test_spend_summary_passes_uncached_tokens_through_when_present(tmp_path) -> None:
    path = tmp_path / "research" / "audits" / "spend_summary.json"
    path.parent.mkdir(parents=True)
    data = {"generated_on": "2026-10-19", "days": [{**SPEND["days"][1], "tokens_uncached": 40}]}
    path.write_text(json.dumps(data))
    panel, _ = cockpit.spend_summary(tmp_path)
    assert panel["days"][0]["tokens_uncached"] == 40
    path.write_text(json.dumps(SPEND))
    panel, _ = cockpit.spend_summary(tmp_path)
    assert all("tokens_uncached" not in day for day in panel["days"])


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
OLD_REGISTRY = json.dumps([{"id": "NEG-OLD", "claim": "An old record."}])
REGISTRY_NOW = json.dumps([
    {"id": "NEG-DCP-FIXTURE-WRAPPED", "claim": "The dihedral sieve pays for every list."},
    {"id": "NEG-OLD", "claim": "An old record."},
])


class FakeGit:
    """Canned output for the read-only git commands the builder runs; None for anything else."""

    def __init__(self, responses: dict[tuple[str, ...], str]):
        self.responses = responses
        self.calls: list[tuple[str, ...]] = []

    def __call__(self, *args: str) -> str | None:
        assert cockpit.allowed_git_args(args), args
        self.calls.append(args)
        return self.responses.get(args)


def _fake_git() -> FakeGit:
    return FakeGit({
        cockpit.SHALLOW_ARGS: "false\n",
        cockpit.COMMIT_LOG_ARGS: COMMIT_LOG,
        cockpit.SNAPSHOT_LOG_ARGS: f"{SHA_A}{US}{ts('2026-10-18')}\n{SHA_C}{US}{ts('2026-10-16')}\n",
        ("show", f"{SHA_C}:{cockpit.SNAPSHOT}"): _snapshot("2026-10-16", negative_results=970),
        ("show", f"{SHA_A}:{cockpit.SNAPSHOT}"): _snapshot("2026-10-18", negative_results=976),
        cockpit.HANDOFF_LOG_ARGS: f"{SHA_B}{US}{ts('2026-10-18', 9)}\n",
        ("show", f"{SHA_B}:{cockpit.HANDOFF}"): OLDER_HANDOFF,
        ("show", f"{SHA_A}:{cockpit.HANDOFF}"): OLDER_HANDOFF,
        cockpit.REGISTRY_LOG_ARGS: f"{SHA_B}{US}{ts('2026-10-18', 9)}\n{SHA_C}{US}{ts('2026-10-10')}\n",
        ("show", f"{SHA_C}:{cockpit.REGISTRY}"): OLD_REGISTRY,
        ("show", f"{SHA_B}:{cockpit.REGISTRY}"): REGISTRY_NOW,
        cockpit.CHECKPOINT_LOG_ARGS: f"{SHA_B}{US}{ts('2026-10-18', 9)}\n",
        cockpit.STATUS_ARGS: PORCELAIN,
    })


def _fake_repo(root):
    (root / "research" / "registry").mkdir(parents=True)
    (root / cockpit.HANDOFF).write_text(HANDOFF)
    (root / cockpit.REGISTRY).write_text(REGISTRY_NOW)
    (root / cockpit.QUARANTINE).write_text(json.dumps([{"id": "NEG-DCP-FIXTURE-BARRIER"}]))
    (root / cockpit.CHECKPOINT).write_text(json.dumps(CHECKPOINT))
    return root


TODAY = dt.date(2026, 10, 19)


def test_build_assembles_every_panel(tmp_path) -> None:
    payload = cockpit.build(_fake_repo(tmp_path), git=_fake_git(), inertia_threshold=1, today=TODAY)
    assert payload["generated_on"] == "2026-10-19"
    assert payload["head"] == {"sha": SHA_A[:8], "commit": SHA_A, "date": "2026-10-18"}
    assert payload["git"] == {"available": True, "shallow": False, "history": True}
    assert payload["warnings"] == []
    assert [d["id"] for d in payload["directions"]][-1] == "other"

    sections = payload["sections"]
    assert [s["index"] for s in sections] == [0, 1, 2, 3, 4]
    assert [s["direction"] for s in sections] == ["opi", "dcp", "dcp", "lattice", "other"]
    assert [s["agent"] for s in sections] == ["codex", "gemini", "unknown", "unknown", "unknown"]
    assert [s["first_committed"] for s in sections] == [None, "2026-10-18", "2026-10-18", "2026-10-18", "2026-10-18"]
    assert [s["order"] for s in sections] == [4, 3, 2, 1, 0]
    assert sections[1]["first_quoted_ids"] == ["NEG-DCP-FIXTURE-BARRIER"]
    assert sections[2]["first_quoted_ids"] == ["NEG-DCP-FIXTURE-WRAPPED"]
    assert [s["registry_day"] for s in sections] == [False, True, True, False, False]
    assert sections[2]["heading_date"] == "2026-09-02"
    older = OLDER_HANDOFF.splitlines()
    assert sections[0]["head_line"] is None
    for section in sections[1:]:
        assert older[section["head_line"] - 1] == f"## {section['heading']}"
        assert section["head_line"] < section["line"]

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

    registry = payload["registry"]
    assert registry["baseline"] == {"date": "2026-10-10", "records": 1}
    assert registry["added"] == 1
    assert registry["by_direction"]["dcp"] == 1
    assert registry["quoted"] == 1  # NEG-DCP-FIXTURE-WRAPPED; the quarantined id never was in the registry history
    assert payload["quotes"] == {"from_history": 2, "from_current_text": 0, "lost": 0}

    inertia = payload["inertia"]
    assert inertia["available"] is True
    assert [row["direction"] for row in inertia["flags"]] == ["opi", "lattice"]
    dcp = next(row for row in inertia["directions"] if row["direction"] == "dcp")
    assert dcp["streak"] == 0
    assert dcp["last_gain"] == {"date": "2026-10-18", "records": 1, "ids": ["NEG-DCP-FIXTURE-WRAPPED"]}

    assert payload["commits"] == {**payload["commits"], "total": 3, "complete": True}
    assert len(payload["commits"]["days"]) == 2
    assert [p["metrics"]["negative_results"] for p in payload["metrics"]["points"]] == [970, 976]
    assert payload["dirty"] == {"modified": 4, "untracked": 2, "total": 6}
    assert payload["checkpoint"]["commits_since"] == 1
    assert payload["checkpoint"]["uncommitted_changes"] is True
    assert "spend" not in payload
    assert str(tmp_path) not in json.dumps(payload)
    assert "scratch" not in json.dumps(payload)


def test_build_without_history_leaves_sections_undated_and_inertia_unavailable(tmp_path) -> None:
    git = _fake_git()
    payload = cockpit.build(_fake_repo(tmp_path), git=git, today=TODAY, history=False)
    assert all(s["first_committed"] is None for s in payload["sections"])
    assert cockpit.HANDOFF_LOG_ARGS not in git.calls
    assert cockpit.REGISTRY_LOG_ARGS not in git.calls
    assert payload["git"]["history"] is False
    assert payload["registry"] is None
    assert payload["inertia"]["available"] is False
    assert payload["quotes"]["from_history"] == 0


def test_build_warns_and_says_unknown_when_git_is_unavailable(tmp_path) -> None:
    payload = cockpit.build(_fake_repo(tmp_path), git=FakeGit({}), today=TODAY)
    assert payload["git"] == {"available": False, "shallow": None, "history": False}
    assert len(payload["warnings"]) == 1
    assert "git" in payload["warnings"][0]
    assert payload["head"] is None
    assert payload["commits"] == {"total": 0, "days": [], "complete": False}
    assert payload["metrics"] == {"keys": [], "points": []}
    assert payload["dirty"] is None
    assert payload["checkpoint"]["last_commit"] is None
    assert payload["checkpoint"]["uncommitted_changes"] is None
    assert payload["inertia"]["available"] is False
    assert len(payload["sections"]) == 5
    assert all(s["first_committed"] is None and s["head_line"] is None for s in payload["sections"])


def test_build_warns_about_a_shallow_clone_and_does_not_date_from_its_truncated_history(tmp_path) -> None:
    git = _fake_git()
    git.responses[cockpit.SHALLOW_ARGS] = "true\n"
    payload = cockpit.build(_fake_repo(tmp_path), git=git, today=TODAY)
    assert payload["git"] == {"available": True, "shallow": True, "history": False}
    assert len(payload["warnings"]) == 1
    assert "shallow" in payload["warnings"][0]
    assert "research metrics" in payload["warnings"][0]  # read from the same truncated history
    assert all(s["first_committed"] is None for s in payload["sections"])
    assert payload["inertia"]["available"] is False
    assert payload["commits"]["complete"] is False
    assert payload["checkpoint"]["last_commit"] is None
    assert payload["checkpoint"]["commits_since"] is None
    assert cockpit.HANDOFF_LOG_ARGS not in git.calls


def test_build_reads_a_handoff_with_bytes_that_are_not_utf8(tmp_path) -> None:
    root = _fake_repo(tmp_path)
    (root / cockpit.HANDOFF).write_bytes(b"## A DCP pass\n\nbody \xff\xfe\n\n## Second\n")
    payload = cockpit.build(root, git=FakeGit({}), today=TODAY)
    assert [s["heading"] for s in payload["sections"]] == ["A DCP pass", "Second"]


def test_build_includes_the_spend_panel_when_its_file_exists(tmp_path) -> None:
    root = _fake_repo(tmp_path)
    (root / "research" / "audits").mkdir(parents=True)
    (root / cockpit.SPEND).write_text(json.dumps(SPEND))
    payload = cockpit.build(root, git=_fake_git(), today=TODAY)
    assert [day["date"] for day in payload["spend"]["days"]] == ["2026-10-16", "2026-10-17", "2026-10-18"]


def test_main_writes_the_cockpit_json(tmp_path) -> None:
    root = _fake_repo(tmp_path)
    assert cockpit.main(["--root", str(root), "--inertia", "3"], git=_fake_git()) == 0
    payload = json.loads((root / "site" / "data" / "cockpit.json").read_text())
    assert payload["inertia"]["threshold"] == 3
    assert payload["settings"] == {"history": True, "inertia_threshold": 3}


def test_main_rejects_an_inertia_threshold_below_one(tmp_path) -> None:
    with pytest.raises(SystemExit):
        cockpit.main(["--root", str(tmp_path), "--inertia", "0"], git=FakeGit({}))
