from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.benchmark import dead_ends as de


def _record(i: int, mode: str, track: str = "dcp", templated: bool = False) -> dict:
    return {
        "id": f"NEG-{track.upper()}-{i}",
        "claim": f"Claim {i}: a coset observable gives a polynomial algorithm for family {i}.",
        "reason_invalid": "Falsified or refined by exact theorem evaluation." if templated else f"Support splitting separates instance {i} classically.",
        "lesson": f"Run classical canonicalization first ({i}).",
        "applies_to": [],
        "evidence": {},
        "source": "x",
    }


def _labels(records: list[dict], modes: list[str]) -> dict:
    return {
        r["id"]: {"mode": m, "track": "dcp", "label_source": "judge", "templated": r["reason_invalid"].startswith("Falsified")}
        for r, m in zip(records, modes)
    }


def test_select_is_stratified_skips_templated_and_unclear() -> None:
    records = [_record(i, "x") for i in range(40)] + [_record(99, "x", templated=True)]
    modes = ["classical_competitor"] * 20 + ["proof_gap"] * 10 + ["readout"] * 9 + ["unclear"] + ["proof_gap"]
    chosen = de.select(records, _labels(records, modes), n=12, seed=0)
    ids = [r["id"] for r in chosen]
    assert len(ids) == 12 and len(set(ids)) == 12
    assert "NEG-DCP-99" not in ids and "NEG-DCP-39" not in ids
    counts = {m: sum(1 for r in chosen if r["mode"] == m) for m in ("classical_competitor", "proof_gap", "readout")}
    assert min(counts.values()) >= 3


def test_select_skips_excluded_ids() -> None:
    records = [_record(i, "x") for i in range(10)]
    labels = _labels(records, ["readout"] * 10)
    chosen = de.select(records, labels, n=10, seed=0, exclude={"NEG-DCP-0", "NEG-DCP-1"})
    assert len(chosen) == 8 and not {"NEG-DCP-0", "NEG-DCP-1"} & {r["id"] for r in chosen}


def test_split_is_deterministic_and_balanced() -> None:
    ids = [f"R{i}" for i in range(100)]
    a, b = de.split(ids, heldout=0.5, seed=1), de.split(ids, heldout=0.5, seed=1)
    assert a == b and sum(v == "heldout" for v in a.values()) == 50


def test_leak_check_flags_shared_phrases() -> None:
    killer = "Support splitting separates the code pair classically in polynomial time."
    assert de.leaks("A coset observable distinguishes these codes.", killer, "") == []
    assert de.leaks("Even though support splitting separates the code pair, a coset observable helps.", killer, "")


def test_validate_items_reports_schema_and_leaks() -> None:
    good = {"id": "A", "proposal": "Use coset states to test code equivalence.", "track": "code_equivalence", "split": "dev",
            "kind": "dead_end", "killer": "Support splitting separates the pair.", "lesson": "Run baselines.",
            "failure_mode": "classical_competitor", "novelty": "published", "source_record": "NEG-A"}
    bad = dict(good, id="B", failure_mode="vibes", proposal="Support splitting separates the pair, but try coset states.")
    problems = de.validate([good, bad])
    assert not [p for p in problems if p.startswith("A:")]
    assert any("B:" in p and "failure_mode" in p for p in problems)
    assert any("B:" in p and "leak" in p for p in problems)


def test_prompt_contains_proposals_but_no_answers() -> None:
    items = [{"id": "A", "proposal": "Try coset states.", "track": "dcp", "split": "heldout", "kind": "dead_end",
              "killer": "SECRET KILLER", "lesson": "SECRET LESSON", "failure_mode": "readout", "novelty": "unclear", "source_record": "N"}]
    prompt = de.agent_prompt(items)
    assert "Try coset states." in prompt and "SECRET" not in prompt
    assert all(mode in prompt for mode in ("classical_competitor", "proof_gap"))


def _prompt_items() -> list[dict]:
    base = {"split": "heldout", "lesson": "", "novelty": None, "source_record": "N"}
    dead = [dict(base, id=f"DE-{i:06X}", proposal=f"Dead end {i}.", track="dcp", kind="dead_end",
                 killer="k", failure_mode="readout") for i in range(8)]
    ctrl = [dict(base, id=f"CT-{i:06X}", proposal=f"Control {i}.", track="dqi_opi", kind="control",
                 killer="", failure_mode=None) for i in range(4)]
    return dead + ctrl


def test_prompt_hides_item_kind_track_and_order() -> None:
    items = _prompt_items()
    prompt = de.agent_prompt(items)
    assert "DE-" not in prompt and "CT-" not in prompt
    assert "dqi_opi" not in prompt and "(dcp)" not in prompt
    order = [line for line in prompt.splitlines() if line.startswith("[P-")]
    assert len(order) == 12
    kinds = ["C" if "Control" in line else "D" for line in order]
    assert kinds != sorted(kinds) and kinds != sorted(kinds, reverse=True)


def test_reply_aliases_map_back_to_item_ids() -> None:
    items = _prompt_items()
    alias = de.prompt_alias(items[9]["id"])
    reply = json.dumps({"id": alias, "pursue": True, "failure_mode": None, "killer": ""})
    old_style = json.dumps({"id": "DE-000001", "pursue": False, "failure_mode": "readout", "killer": "k"})
    answers = de.parse_reply(reply + "\n" + old_style, items)
    assert answers[items[9]["id"]]["pursue"] is True
    assert answers["DE-000001"]["pursue"] is False
    assert alias not in answers


def test_disputed_gold_mode_is_left_out_of_mode_accuracy() -> None:
    items = [
        {"id": "A", "kind": "dead_end", "failure_mode": "readout", "split": "heldout"},
        {"id": "B", "kind": "dead_end", "failure_mode": "proof_gap", "split": "heldout", "failure_mode_disputed": True},
    ]
    answers = {"A": {"pursue": False, "failure_mode": "readout"}, "B": {"pursue": False, "failure_mode": "readout"}}
    score = de.score(items, answers, {})
    assert score["failure_mode_accuracy"] == pytest.approx(1.0)
    assert score["n_mode_scored"] == 1


def test_score_combines_answers_and_judge_verdicts() -> None:
    items = [
        {"id": "A", "kind": "dead_end", "failure_mode": "readout", "split": "heldout"},
        {"id": "B", "kind": "dead_end", "failure_mode": "proof_gap", "split": "heldout"},
        {"id": "C", "kind": "control", "failure_mode": None, "split": "heldout"},
    ]
    answers = {
        "A": {"pursue": False, "failure_mode": "readout", "killer": "x"},
        "B": {"pursue": True, "failure_mode": "readout", "killer": "y"},
        "C": {"pursue": True, "failure_mode": None, "killer": ""},
    }
    verdicts = {"A": 1.0, "B": 0.0}
    score = de.score(items, answers, verdicts)
    assert score["killer_found"] == pytest.approx(0.5)
    assert score["failure_mode_accuracy"] == pytest.approx(0.5)
    assert score["dead_ends_rejected"] == pytest.approx(0.5)
    assert score["controls_pursued"] == pytest.approx(1.0)
    assert score["n_dead_ends"] == 2 and score["n_controls"] == 1


def test_parse_agent_reply_extracts_jsonl_lines() -> None:
    reply = 'Here you go:\n```\n{"id": "A", "pursue": false, "failure_mode": "readout", "killer": "k"}\n{"id": "B", "pursue": true, "failure_mode": null, "killer": ""}\n```'
    parsed = de.parse_reply(reply)
    assert set(parsed) == {"A", "B"} and parsed["A"]["pursue"] is False


FIXTURE = Path(__file__).parent / "fixtures" / "arxiv_atom_sample.xml"


def _papers() -> dict:
    from tools.corpus.sources.arxiv import parse_atom

    return {p.arxiv_id: p for p in parse_atom(FIXTURE.read_bytes())}


def test_export_candidates_writes_batches_and_instructions(tmp_path: Path) -> None:
    records = [_record(i, "x") for i in range(9)]
    chosen = de.select(records, _labels(records, ["readout"] * 9), n=9, seed=0)
    de.export_candidates(chosen, {"NEG-DCP-0": "published"}, tmp_path, batches=2)
    batches = sorted(tmp_path.glob("batch_*.json"))
    assert len(batches) == 2 and (tmp_path / "INSTRUCTIONS.md").exists()
    rows = [row for b in batches for row in json.loads(b.read_text())["candidates"]]
    assert len(rows) == 9 and {"id", "claim", "reason_invalid", "lesson", "failure_mode"} <= set(rows[0])
    assert next(r for r in rows if r["id"] == "NEG-DCP-0")["novelty"] == "published"


def test_assemble_keeps_curated_rows_and_verified_controls() -> None:
    papers = _papers()
    pid, paper = next(iter(papers.items()))
    records = [_record(i, "x") for i in range(3)]
    labels = _labels(records, ["readout", "proof_gap", "readout"])
    curated = [
        {"source_record": "NEG-DCP-0", "keep": True, "proposal": "Measure each packet in a rotated basis to read the secret.",
         "killer": "The rotated basis gives no more than the X basis on mixed packets.", "lesson": "Bound local readout.", "difficulty": "medium"},
        {"source_record": "NEG-DCP-1", "keep": False, "note": "internal jargon only"},
        {"source_record": "NEG-DCP-2", "keep": True, "proposal": "Use a walk.", "killer": "No gap.", "lesson": "Prove a gap.", "difficulty": "hard"},
    ]
    controls = [
        {"proposal": "A known result.", "track": "dcp", "arxiv_id": pid, "quote": " ".join(paper.abstract.split()[2:12])},
        {"proposal": "A made-up result.", "track": "dcp", "arxiv_id": pid, "quote": "this sentence is not in the abstract anywhere"},
    ]
    items, report = de.assemble(curated, records, labels, {"NEG-DCP-0": "adjacent"}, controls, papers, seed=0)
    dead = [i for i in items if i["kind"] == "dead_end"]
    ctrl = [i for i in items if i["kind"] == "control"]
    assert sorted(i["source_record"] for i in dead) == ["NEG-DCP-0", "NEG-DCP-2"]
    assert {i["failure_mode"] for i in dead} == {"readout"}
    assert next(i for i in dead if i["source_record"] == "NEG-DCP-0")["novelty"] == "adjacent"
    assert len(ctrl) == 1 and ctrl[0]["source_record"] == f"arXiv:{pid}" and ctrl[0]["failure_mode"] is None
    assert report["dropped_controls"] == 1 and report["rejected_by_curator"] == 1
    assert len({i["id"] for i in items}) == len(items) and de.validate(items) == []


def test_assemble_drops_listed_duplicates() -> None:
    records = [_record(i, "x") for i in range(3)]
    labels = _labels(records, ["readout"] * 3)
    curated = [{"source_record": r["id"], "keep": True, "proposal": f"Proposal {i}.", "killer": f"Killer {i}.",
                "lesson": "L.", "difficulty": "easy"} for i, r in enumerate(records)]
    items, report = de.assemble(curated, records, labels, {}, [], {}, seed=0,
                                drop={"NEG-DCP-1": "same family as NEG-DCP-0", "NEG-DCP-7": "not curated"})
    assert sorted(i["source_record"] for i in items) == ["NEG-DCP-0", "NEG-DCP-2"]
    assert report["dropped_duplicates"] == 1


def test_review_applies_after_split_without_reshuffling() -> None:
    records = [_record(i, "x") for i in range(12)]
    labels = _labels(records, ["readout"] * 12)
    curated = [{"source_record": r["id"], "keep": True, "proposal": f"Measure packet set {i} in a rotated basis.",
                "killer": f"Mixed packets carry no phase {i}.", "lesson": "L.", "difficulty": "easy"} for i, r in enumerate(records)]
    base, _ = de.assemble(curated, records, labels, {}, [], {}, seed=0)
    first, second = base[0]["id"], base[1]["id"]
    review = {first: {"id": first, "verdict": "drop", "note": "killer wrong"},
              second: {"id": second, "verdict": "fix", "fixed_proposal": "Read packets one at a time.", "fixed_killer": None}}
    items, report = de.assemble(curated, records, labels, {}, [], {}, seed=0, review=review)
    assert first not in {i["id"] for i in items}
    assert {i["id"]: i["split"] for i in items} == {i["id"]: i["split"] for i in base if i["id"] != first}
    fixed = next(i for i in items if i["id"] == second)
    assert fixed["proposal"] == "Read packets one at a time." and fixed["killer"] == base[1]["killer"]
    assert report["dropped_in_review"] == 1 and report["fixed_in_review"] == 1


def test_review_marks_a_rejected_gold_mode_as_disputed() -> None:
    records = [_record(i, "x") for i in range(4)]
    labels = _labels(records, ["readout"] * 4)
    curated = [{"source_record": r["id"], "keep": True, "proposal": f"Measure packet set {i} in a rotated basis.",
                "killer": f"Mixed packets carry no phase {i}.", "lesson": "L.", "difficulty": "easy"} for i, r in enumerate(records)]
    base, _ = de.assemble(curated, records, labels, {}, [], {}, seed=0)
    target = base[0]["id"]
    review = {target: {"id": target, "verdict": "ok", "mode_fit": False, "note": "really a proof gap"}}
    items, report = de.assemble(curated, records, labels, {}, [], {}, seed=0, review=review)
    flags = {i["id"]: i.get("failure_mode_disputed", False) for i in items}
    assert flags[target] is True and not any(v for k, v in flags.items() if k != target)
    assert report["mode_disputed_in_review"] == 1


def test_load_drop_list_reads_reasons(tmp_path: Path) -> None:
    assert de.load_drop(tmp_path) == {}
    path = tmp_path / de.DROP_FILE
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"dropped": [{"source_record": "NEG-A", "kept_instead": "NEG-B", "reason": "same family"}]}))
    assert de.load_drop(tmp_path) == {"NEG-A": "same family"}


def test_load_review_keys_rows_by_item_id(tmp_path: Path) -> None:
    assert de.load_review(tmp_path) == {}
    path = tmp_path / de.REVIEW_FILE
    path.parent.mkdir(parents=True)
    path.write_text('{"id": "DE-1", "verdict": "ok"}\n{"id": "CT-2", "verdict": "drop", "note": "overstated"}\n')
    assert de.load_review(tmp_path)["CT-2"]["verdict"] == "drop" and set(de.load_review(tmp_path)) == {"DE-1", "CT-2"}


def test_judge_packets_skip_pursued_items() -> None:
    items = [
        {"id": "A", "kind": "dead_end", "proposal": "p", "killer": "k", "lesson": "l", "failure_mode": "readout"},
        {"id": "B", "kind": "dead_end", "proposal": "p", "killer": "k", "lesson": "l", "failure_mode": "readout"},
        {"id": "C", "kind": "control", "proposal": "p", "killer": "", "lesson": "", "failure_mode": None},
    ]
    answers = {"A": {"pursue": False, "killer": "mine"}, "B": {"pursue": True, "killer": ""}}
    packets = de.judge_packets(items, answers)
    assert [p["id"] for p in packets] == ["A"] and packets[0]["agent_killer"] == "mine"
    assert packets[0]["hidden_killer"] == "k"


def test_cli_prompt_and_score(tmp_path: Path) -> None:
    items = [
        {"id": "DE-1", "kind": "dead_end", "proposal": "Try a rotated basis.", "killer": "HIDDEN", "lesson": "L",
         "failure_mode": "readout", "novelty": None, "track": "dcp", "split": "heldout", "source_record": "N1", "difficulty": "easy"},
        {"id": "DE-2", "kind": "dead_end", "proposal": "Try a walk.", "killer": "HIDDEN", "lesson": "L",
         "failure_mode": "proof_gap", "novelty": None, "track": "dcp", "split": "dev", "source_record": "N2", "difficulty": "easy"},
        {"id": "CT-1", "kind": "control", "proposal": "A true claim.", "killer": "", "lesson": "", "failure_mode": None,
         "novelty": None, "track": "dcp", "split": "heldout", "source_record": "arXiv:1", "difficulty": None},
    ]
    path = tmp_path / de.ITEMS_FILE
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"canary": de.CANARY, "items": items}))
    prompt = tmp_path / "prompt.txt"
    assert de.main(["--root", str(tmp_path), "prompt", "--split", "heldout", "--out", str(prompt)]) == 0
    text = prompt.read_text()
    assert "Try a rotated basis." in text and "A true claim." in text and "Try a walk." not in text and "HIDDEN" not in text
    answers = tmp_path / "haiku.txt"
    answers.write_text('{"id": "DE-1", "pursue": false, "failure_mode": "readout", "killer": "x"}\n{"id": "CT-1", "pursue": true, "failure_mode": null, "killer": ""}\n')
    packets = tmp_path / "packets.json"
    assert de.main(["--root", str(tmp_path), "judge-export", "--split", "heldout", "--answers", f"haiku={answers}", "--out", str(packets)]) == 0
    assert [p["id"] for p in json.loads(packets.read_text())["packets"]] == ["DE-1"]
    verdicts = tmp_path / "v.jsonl"
    verdicts.write_text('{"agent": "haiku", "id": "DE-1", "verdict": 1, "note": "same"}\n')
    assert de.main(["--root", str(tmp_path), "score", "--split", "heldout", "--answers", f"haiku={answers}", "--verdicts", str(verdicts)]) == 0
    results = json.loads((tmp_path / de.RESULTS_FILE).read_text())
    assert results["agents"]["haiku"]["killer_found"] == 1.0 and results["agents"]["haiku"]["controls_pursued"] == 1.0
    assert (tmp_path / de.REPORT_FILE).exists()


def test_blind_hides_agent_names_and_unblind_restores_them() -> None:
    packets = [{"agent": a, "id": f"DE-{i}"} for a in ("opus", "haiku", "sonnet") for i in range(3)]
    blinded, key = de.blind(packets, seed=20261019)
    assert key == {"haiku": "X", "opus": "Y", "sonnet": "Z"}
    assert {p["agent"] for p in blinded} == {"X", "Y", "Z"}
    assert [(p["agent"], p["id"]) for p in blinded] != [(key[p["agent"]], p["id"]) for p in packets]
    rows = [{"agent": p["agent"], "id": p["id"], "verdict": 1} for p in blinded]
    assert sorted((r["agent"], r["id"]) for r in de.unblind(rows, key)) == sorted((p["agent"], p["id"]) for p in packets)


def test_cli_blinds_judge_packets_and_scores_through_the_key(tmp_path: Path) -> None:
    items = [{"id": "DE-1", "kind": "dead_end", "proposal": "Try a rotated basis.", "killer": "HIDDEN", "lesson": "L",
              "failure_mode": "readout", "novelty": None, "track": "dcp", "split": "heldout", "source_record": "N1", "difficulty": "easy"}]
    path = tmp_path / de.ITEMS_FILE
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"canary": de.CANARY, "items": items}))
    answers = tmp_path / "haiku.txt"
    answers.write_text('{"id": "DE-1", "pursue": false, "failure_mode": "readout", "killer": "x"}\n')
    packets, key = tmp_path / "packets.json", tmp_path / "key.json"
    assert de.main(["--root", str(tmp_path), "judge-export", "--answers", f"haiku={answers}", "--out", str(packets),
                    "--blind", "7", "--key", str(key)]) == 0
    label = json.loads(key.read_text())["haiku"]
    assert [p["agent"] for p in json.loads(packets.read_text())["packets"]] == [label] and "haiku" not in packets.read_text()
    verdicts = tmp_path / "v.jsonl"
    verdicts.write_text(json.dumps({"agent": label, "id": "DE-1", "verdict": 1}) + "\n")
    assert de.main(["--root", str(tmp_path), "score", "--answers", f"haiku={answers}", "--verdicts", str(verdicts), "--key", str(key)]) == 0
    assert json.loads((tmp_path / de.RESULTS_FILE).read_text())["agents"]["haiku"]["killer_found"] == 1.0


def test_render_reports_each_agent() -> None:
    results = {"agents": {"haiku": {"n_dead_ends": 2, "n_controls": 1, "dead_ends_rejected": 0.5, "failure_mode_accuracy": 0.5,
                                    "killer_found": 0.5, "controls_pursued": 1.0, "answered": 3}},
               "items": {"n": 3, "dead_ends": 2, "controls": 1, "split": "heldout"}, "generated_on": "2026-10-19"}
    text = de.render(results)
    assert "| haiku |" in text and "50%" in text and de.CANARY in text


def test_render_says_how_many_dead_ends_the_mode_score_covers() -> None:
    row = {"n_dead_ends": 72, "n_controls": 12, "dead_ends_rejected": 1.0, "failure_mode_accuracy": 0.5,
           "n_mode_scored": 69, "killer_found": 0.5, "controls_pursued": 1.0, "answered": 84}
    results = {"agents": {"haiku": row}, "items": {"n": 84, "dead_ends": 72, "controls": 12, "split": "heldout"},
               "generated_on": "2026-10-19"}
    assert "Failure mode right is scored on the 69 dead ends" in de.render(results)
