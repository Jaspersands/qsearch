from __future__ import annotations

from pathlib import Path

from tools.corpus.sources import discover, parse_file


def _docs(root: Path, rel: str):
    return {doc.doc_id: doc for doc in parse_file(root, rel)}


def test_discover_finds_every_source_family(fake_repo: Path) -> None:
    found = set(discover(fake_repo))
    assert "research/registry/negative_results.json" in found
    assert "research/PRIME_CHARACTER_EXTERIOR_BOUND.md" in found
    assert "research/AGENT_HANDOFF.md" in found
    assert "theorems/prime_character_exterior_bound.py" in found
    assert "research/literature_records.json" in found
    assert "research/literature_audits/dihedral_sources.json" in found
    assert "research/hypotheses/bpqm_gibbs_frontier_contract.json" in found


def test_discover_skips_dict_shaped_registry_summaries(fake_repo: Path) -> None:
    assert "research/registry/reductions.json" not in set(discover(fake_repo))


def test_negative_record_carries_claim_reason_tags_and_line(fake_repo: Path) -> None:
    docs = _docs(fake_repo, "research/registry/negative_results.json")
    doc = docs["negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY"]
    assert doc.kind == "negative"
    assert "Local Helstrom readout" in doc.title
    assert "modulus-64 counterexample" in doc.text
    assert "does not order product measurements" in doc.text
    assert doc.meta["tags"] == ["DCP", "PO-MEASUREMENT"]
    assert doc.meta["status"] == "derived-review-pending"
    assert doc.meta["reason"].startswith("An explicit modulus-64")
    line = (fake_repo / doc.path).read_text().splitlines()[doc.line - 1]
    assert '"id": "NEG-DCP-LOCAL-HELSTROM-HIERARCHY"' in line


def test_negative_without_evidence_status_is_marked_retained(fake_repo: Path) -> None:
    docs = _docs(fake_repo, "research/registry/negative_results.json")
    assert docs["negative:NEG-OPI-MIXED-COSET-HARDNESS"].meta["status"] == "retained"


def test_quarantined_record_is_a_negative_with_quarantine_status(fake_repo: Path) -> None:
    docs = _docs(fake_repo, "research/registry/quarantined_campaign_negatives.json")
    doc = docs["quarantined:NEG-ANNEALING-GAP-BARRIER"]
    assert doc.kind == "negative"
    assert doc.meta["status"] == "QUARANTINED_OVERBROAD_NO_GO"
    assert "tunneling" in doc.text
    assert "universal no-go" in doc.text


def test_dequantization_check_and_proof_status_records(fake_repo: Path) -> None:
    deq = _docs(fake_repo, "research/registry/dequantization_checks.json")["dequant:DEQ-POLAR-GIBBS-SOURCE"]
    assert deq.kind == "dequant"
    assert deq.meta["severity"] == "high"
    assert "Charge the classical sampler" in deq.text
    proof = _docs(fake_repo, "research/registry/proof_status.json")
    assert list(proof) == ["proof:CODE-COSET-COLLECTIVE:PO-FAMILY"]


def test_note_is_chunked_by_heading_with_status_and_lines(fake_repo: Path) -> None:
    rel = "research/PRIME_CHARACTER_EXTERIOR_BOUND.md"
    docs = _docs(fake_repo, rel)
    assert set(docs) == {
        "note:PRIME_CHARACTER_EXTERIOR_BOUND#",
        "note:PRIME_CHARACTER_EXTERIOR_BOUND#scientific-question-and-outcome",
        "note:PRIME_CHARACTER_EXTERIOR_BOUND#exact-cycle-indicator",
    }
    chunk = docs["note:PRIME_CHARACTER_EXTERIOR_BOUND#exact-cycle-indicator"]
    assert chunk.kind == "note"
    assert chunk.title == "Fixed-Input OPI: A Smaller Classical Field-Size Guarantee › Exact Cycle Indicator"
    assert "alternating sum of exterior characters" in chunk.text
    assert chunk.meta["status"] == "review-pending"
    assert (fake_repo / rel).read_text().splitlines()[chunk.line - 1] == "## Exact Cycle Indicator"


def test_superseded_note_status(fake_repo: Path) -> None:
    docs = _docs(fake_repo, "research/OLD_HIERARCHY.md")
    assert {doc.meta["status"] for doc in docs.values()} == {"superseded"}


def test_long_section_is_split_into_word_bounded_chunks(fake_repo: Path) -> None:
    paragraphs = "\n\n".join(" ".join(f"word{p}x{i}" for i in range(150)) for p in range(5))
    (fake_repo / "research" / "LONG.md").write_text(f"# Long\n\n## Big Section\n\n{paragraphs}\n")
    docs = parse_file(fake_repo, "research/LONG.md")
    big = [doc for doc in docs if doc.doc_id.startswith("note:LONG#big-section")]
    assert len(big) >= 2
    assert all(len(doc.text.split()) <= 400 for doc in big)
    assert big[0].doc_id == "note:LONG#big-section"
    assert big[1].doc_id == "note:LONG#big-section-2"


def test_handoff_sections_get_rank_and_stable_ids_for_repeated_headings(fake_repo: Path) -> None:
    docs = parse_file(fake_repo, "research/AGENT_HANDOFF.md")
    sections = [doc for doc in docs if doc.meta.get("rank") is not None]
    assert [doc.kind for doc in sections] == ["handoff"] * 3
    assert [doc.meta["rank"] for doc in sections] == [0, 1, 2]
    ids = [doc.doc_id for doc in sections]
    # Duplicate headings are numbered from the oldest section, so ids survive new sections on top.
    assert ids[1] == "handoff:AGENT_HANDOFF:fixed-input-morse-norm-solver-2"
    assert ids[2] == "handoff:AGENT_HANDOFF:fixed-input-morse-norm-solver"


def test_theorem_module_uses_docstring_and_function_names(fake_repo: Path) -> None:
    docs = _docs(fake_repo, "theorems/prime_character_exterior_bound.py")
    doc = docs["theorem:prime_character_exterior_bound"]
    assert doc.kind == "theorem"
    assert doc.title == "Exterior-character bound for the fixed-input Morse norm solver."
    assert "exterior characters" in doc.text
    assert "large fixed input control" in doc.text
    assert doc.meta["functions"] == ["exterior_characters", "large_fixed_input_control"]


def test_unparseable_theorem_falls_back_to_raw_text(fake_repo: Path) -> None:
    docs = parse_file(fake_repo, "theorems/broken_module.py")
    assert [doc.doc_id for doc in docs] == ["theorem:broken_module"]
    assert "broken" in docs[0].text


def test_literature_audit_and_hypothesis_records(fake_repo: Path) -> None:
    lit = _docs(fake_repo, "research/literature_records.json")["literature:jordan-dqi-2024"]
    assert lit.kind == "literature"
    assert lit.meta["url"] == "https://arxiv.org/abs/2408.08292"
    assert "decoding of the dual code" in lit.text
    audit = _docs(fake_repo, "research/literature_audits/dihedral_sources.json")
    doc = audit["literature:dihedral_sources:ARXIV-quant-ph-0501044-v2"]
    assert "subset-sum fiber" in doc.text
    hyp = _docs(fake_repo, "research/hypotheses/bpqm_gibbs_frontier_contract.json")
    assert hyp["hypothesis:bpqm_gibbs_frontier_contract"].meta["status"] == "classical-competitor-found"


def test_malformed_json_falls_back_to_one_raw_text_doc(fake_repo: Path) -> None:
    rel = "research/hypotheses/broken_contract.json"
    (fake_repo / rel).write_text('{"problem": "bad \\escape in a hypothesis"}\n')
    docs = parse_file(fake_repo, rel)
    assert [doc.doc_id for doc in docs] == ["hypothesis:broken_contract"]
    assert docs[0].meta["status"] == "unparseable"
    assert "bad" in docs[0].text and "hypothesis" in docs[0].text


def test_templated_dequant_claims_are_titled_by_their_target(fake_repo: Path) -> None:
    import json

    rel = "research/registry/dequantization_checks.json"
    template = "Experiment result supports the candidate without triggering kill criteria."
    records = [
        {"id": f"DEQ-RESULT-{i}", "claim_under_test": template, "target_id": f"EXP-COSET-WIDGET-{i}",
         "required_action": "Resolve the falsifier.", "evidence": "x", "severity": "medium"}
        for i in range(4)
    ]
    (fake_repo / rel).write_text(json.dumps(records, indent=2))
    docs = parse_file(fake_repo, rel)
    assert docs[0].title == f"EXP-COSET-WIDGET-0: {template}"


def test_record_lines_are_exact_and_linear_in_file_size() -> None:
    import json
    import time

    from tools.corpus.sources.registry import _id_lines

    records = [{"id": f"NEG-{i}", "claim": "x " * 40} for i in range(20000)]
    text = "\n\n" + json.dumps(records, indent=2)  # leading blank lines must not shift the first line number
    lines = text.splitlines()
    start = time.process_time()
    found = _id_lines(text)
    elapsed = time.process_time() - start
    assert len(found) == 20000
    for rid in ("NEG-0", "NEG-777", "NEG-19999"):
        assert lines[found[rid] - 1].strip().startswith(f'"id": "{rid}"')
    assert elapsed < 1.0  # quadratic counting took tens of seconds on this input


def test_note_ids_are_unique_when_numbered_and_repeated_headings_collide(fake_repo: Path) -> None:
    long = " ".join(f"w{i}" for i in range(450))
    (fake_repo / "research" / "DUP.md").write_text(
        f"# Dup\n\n## Results\n\n{long}\n\n## Results\n\nsecond section here.\n\n## Results 2\n\nthird section here.\n"
    )
    ids = [doc.doc_id for doc in parse_file(fake_repo, "research/DUP.md")]
    assert len(ids) == len(set(ids)) == 4
    assert ids == [doc.doc_id for doc in parse_file(fake_repo, "research/DUP.md")]  # deterministic
    journal = "# H\n\n## Pass 2\n\nnewest pass text.\n\n## Pass\n\nmiddle pass text.\n\n## Pass\n\noldest pass text.\n"
    (fake_repo / "research" / "AGENT_HANDOFF.md").write_text(journal)
    ids = [doc.doc_id for doc in parse_file(fake_repo, "research/AGENT_HANDOFF.md")]
    assert len(ids) == len(set(ids)) == 3


def test_parser_crash_falls_back_to_raw_text_and_reports_the_problem(fake_repo: Path, monkeypatch) -> None:
    from tools.corpus import sources
    from tools.corpus.sources import parse_source

    def crash(root, rel, issues=None):
        raise AttributeError("'str' object has no attribute 'get'")

    monkeypatch.setattr(sources.registry, "parse", crash)
    docs, issues = parse_source(fake_repo, "research/registry/negative_results.json")
    assert [doc.meta["status"] for doc in docs] == ["unparseable"]
    assert issues and "AttributeError" in issues[0]
