"""Regression gates for the retracted arbitrary-degree regulator barrier.

The arithmetic controls refute particular inferences, not full number-field
algorithms. Literature assertions remain source-audit obligations; these tests
only keep the reviewed correction and its quarantine integration in place.
"""

from fractions import Fraction
import hashlib
import json
import re

import pytest

from core import research_registry as registry
from theorems import nonabelian_barrier_scope_audit as audit


KEY = "NEG-ARBITRARY-DEGREE-REGULATOR-EXPONENTIAL-BARRIER"
ORIGINAL_SHA256 = "cd1ae36604d9f68eda100d19d07fc765df7cba283b3799b2cc651c4f221768f9"
NOTE = "research/ARBITRARY_DEGREE_NUMBER_FIELD_REGULATOR_BARRIER.md"
UNRELATED = {"id": "UNRELATED-NUMBER-FIELD-SCOPE-CONTROL", "claim": "preserve"}


@pytest.fixture
def original():
    live = [row for row in json.loads(audit.ACTIVE.read_text()) if row["id"] == KEY]
    saved = [row["original_record"] for row in json.loads(audit.ARCHIVE.read_text())
             if row["id"] == KEY]
    assert len(live) <= 1 and len(saved) <= 1
    assert live or saved, "The full original must remain available after quarantine"
    record = (live or saved)[0]
    assert all(row == record for row in live + saved)
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(canonical).hexdigest() == ORIGINAL_SHA256
    return record


@pytest.fixture
def isolated_registry(tmp_path, monkeypatch, original):
    originals = audit.reviewed_originals()
    originals[KEY] = original
    active = tmp_path / "negative_results.json"
    archive = tmp_path / "quarantined_campaign_negatives.json"
    active.write_text(json.dumps([*originals.values(), UNRELATED]))
    archive.write_text("[]")
    monkeypatch.setattr(audit, "ACTIVE", active)
    monkeypatch.setattr(audit, "ARCHIVE", archive)
    monkeypatch.setattr(registry, "NEGATIVE_RESULTS_PATH", active)
    monkeypatch.setattr(registry, "QUARANTINED_NEGATIVES_PATH", archive)
    return active, archive


def test_review_binds_complete_historical_record_and_number_field_note(original):
    assert KEY in audit.REVIEWED, "The false number-field barrier is not reviewed"
    review = audit.REVIEWED[KEY]
    assert review["sha256"] == audit.record_hash(original) == ORIGINAL_SHA256
    assert review.get("review", audit.NOTE) == NOTE
    assert review["reviewed_on"] and review["reasons"]
    assert original["source"] == NOTE


def test_quarantine_extends_archive_preserving_original_and_is_idempotent(
    isolated_registry, monkeypatch, original,
):
    active, archive = isolated_registry
    reviewed = audit.REVIEWED
    with monkeypatch.context() as earlier:
        earlier.setattr(audit, "REVIEWED", {k: v for k, v in reviewed.items() if k != KEY})
        audit.quarantine_reviewed_negatives()
    previously_saved = json.loads(archive.read_text())
    assert json.loads(active.read_text()) == [original, UNRELATED]

    audit.quarantine_reviewed_negatives()
    saved = json.loads(archive.read_text())
    assert len(saved) == len(previously_saved) + 1, "Number-field review was not archived"
    assert saved[:-1] == previously_saved
    row = saved[-1]
    assert row["id"] == KEY
    assert row["original_record"] == original
    assert row["original_sha256"] == audit.record_hash(row["original_record"]) == ORIGINAL_SHA256
    assert row["review"] == NOTE
    assert row["reviewed_on"] == reviewed[KEY]["reviewed_on"]
    assert row["retraction_reasons"] == reviewed[KEY]["reasons"]
    assert row["status"] == "QUARANTINED_OVERBROAD_NO_GO"
    assert row["original_checks_are_general_proofs"] is False
    assert row["reinstatement_requires_scoped_mathematical_review"] is True
    for previous in previously_saved:
        review = reviewed[previous["id"]]
        assert previous["review"] == review.get("review", audit.NOTE)
    assert json.loads(active.read_text()) == [UNRELATED]
    before = active.read_bytes(), archive.read_bytes()
    audit.quarantine_reviewed_negatives()
    assert before == (active.read_bytes(), archive.read_bytes())


@pytest.mark.parametrize("quarantine_first", (False, True))
@pytest.mark.parametrize("field", ("claim", "evidence"))
def test_changed_full_original_requires_independent_review_without_writes(
    isolated_registry, original, quarantine_first, field,
):
    assert KEY in audit.REVIEWED
    active, archive = isolated_registry
    if quarantine_first:
        audit.quarantine_reviewed_negatives()
    changed = json.loads(json.dumps(original))
    if field == "evidence":
        changed["evidence"]["mesh_volume_explosion"] = "changed after review"
    else:
        changed[field] = "changed after review"
    rows = [row for row in json.loads(active.read_text()) if row["id"] != KEY]
    active.write_text(json.dumps([*rows, changed]))
    before = active.read_bytes(), archive.read_bytes()
    with pytest.raises(ValueError, match="independent review"):
        audit.quarantine_reviewed_negatives()
    assert before == (active.read_bytes(), archive.read_bytes())


def test_changed_archived_evidence_requires_independent_review_without_writes(isolated_registry):
    assert KEY in audit.REVIEWED
    active, archive = isolated_registry
    audit.quarantine_reviewed_negatives()
    saved = json.loads(archive.read_text())
    row = next(row for row in saved if row["id"] == KEY)
    row["original_record"]["evidence"]["lattice_reconstruction_hardness"] = "changed"
    archive.write_text(json.dumps(saved))
    before = active.read_bytes(), archive.read_bytes()
    with pytest.raises(ValueError, match="independent review"):
        audit.quarantine_reviewed_negatives()
    assert before == (active.read_bytes(), archive.read_bytes())


def test_registry_blocks_repromotion_and_filters_raw_reintroduction(isolated_registry, original):
    assert KEY in audit.REVIEWED
    active, archive = isolated_registry
    audit.quarantine_reviewed_negatives()
    before = active.read_bytes(), archive.read_bytes()
    with pytest.raises(ValueError, match="quarantined"):
        registry.upsert_negative_result(registry.NegativeResultRecord(**original))
    assert before == (active.read_bytes(), archive.read_bytes())
    active.write_text(json.dumps([UNRELATED, original]))
    assert registry.load_negative_results() == [UNRELATED]


def test_historical_retrieval_case_keeps_evidence_but_not_active_negative_status(isolated_registry):
    from tools.corpus.sources.registry import parse

    assert KEY in audit.REVIEWED
    active, archive = isolated_registry
    cases = json.loads((audit.ROOT / "tests/tools/fixtures/corpus_heldout.json").read_text())
    assert any(case["id"] == KEY and case["query"] for case in cases)
    audit.quarantine_reviewed_negatives()
    assert f"negative:{KEY}" not in {doc.doc_id for doc in parse(active.parent, active.name)}
    historical = [doc for doc in parse(archive.parent, archive.name)
                  if doc.doc_id == f"quarantined:{KEY}"]
    assert len(historical) == 1
    assert historical[0].meta["status"] == "QUARANTINED_OVERBROAD_NO_GO"
    assert historical[0].meta["retraction"]


def test_report_keeps_published_algorithms_separate_from_new_solver_claims(isolated_registry):
    report = audit.build_report()
    assert report["reviewed_original_hashes"].get(KEY) == ORIGINAL_SHA256
    review = report["number_field_review"]
    assert review["note"] == NOTE
    assert review["arbitrary_degree_unit_group"] == "KNOWN_QUANTUM_POLYNOMIAL_TIME"
    assert review["principal_ideal_output"] == "COMPACT_GENERATOR_NOT_ARBITRARY_SHORT_GENERATOR"
    assert review["class_group_algorithm_assumption"] == "GRH"
    assert review["new_implementation_of_number_field_algorithm"] is False
    assert review["general_lattice_problem_solved"] is False
    assert "https://arxiv.org/abs/2510.02280" in report["primary_sources"]
    assert "https://arxiv.org/abs/2510.02280v2" in report["primary_sources"]
    assert "2510.02280v2" in review["corrected_cost_source"]
    for flag in ("new_quantum_algorithm", "general_circuit_lower_bound_proved",
                 "speedup_claim_allowed", "accepted_speedup_candidate"):
        assert report[flag] is False


def test_live_registry_quarantines_the_false_barrier_with_complete_evidence(original):
    active = json.loads(audit.ACTIVE.read_text())
    assert KEY not in {row["id"] for row in active}, "False lower bound remains active"
    assert KEY not in {row["id"] for row in registry.load_negative_results()}
    saved = [row for row in json.loads(audit.ARCHIVE.read_text()) if row["id"] == KEY]
    assert len(saved) == 1
    assert saved[0]["original_record"] == original
    assert saved[0]["original_sha256"] == ORIGINAL_SHA256
    assert saved[0]["review"] == NOTE
    assert saved[0]["status"] == "QUARANTINED_OVERBROAD_NO_GO"


@pytest.mark.parametrize("path,collection", (
    ("site/data/negatives.json", "records"),
    ("site/data/negative_map.json", "points"),
))
def test_live_negative_views_do_not_promote_false_lower_bound(path, collection):
    payload = json.loads((audit.ROOT / path).read_text())
    assert KEY not in {row["id"] for row in payload[collection]}, path


def test_saved_audit_includes_number_field_review_without_claiming_a_new_algorithm():
    report = json.loads(audit.REPORT.read_text())
    assert report["reviewed_original_hashes"].get(KEY) == ORIGINAL_SHA256
    assert report["retraction_reasons"][KEY] == audit.REVIEWED[KEY]["reasons"]
    assert report["producer_sha256"] == hashlib.sha256(
        audit.ROOT.joinpath("theorems/nonabelian_barrier_scope_audit.py").read_bytes()
    ).hexdigest()
    for flag in ("new_quantum_algorithm", "general_circuit_lower_bound_proved",
                 "speedup_claim_allowed", "accepted_speedup_candidate"):
        assert report[flag] is False


def test_corrected_note_is_explicitly_retracted_and_claims_no_new_speedup():
    note = (audit.ROOT / NOTE).read_text()
    opening = note[:1500].casefold()
    assert "retract" in opening or "withdrawn" in opening
    assert "formally proved & computationally verified" not in opening
    assert KEY in note
    for flag in ("speedup_claim_allowed", "accepted_speedup_candidate"):
        assert re.search(rf"{flag}\s*=\s*False\b", note)


def test_corrected_note_separates_primary_quantum_results_from_classical_lower_bounds():
    note = " ".join((audit.ROOT / NOTE).read_text().casefold().split())
    # Presence/scope guards, not a substitute for auditing these primary papers.
    for source in ("kitaev", "2014", "biasse", "song", "2016", "2510.02280"):
        assert source in note, f"Missing primary-result attribution: {source}"
    for qualification in ("polynomial", "degree", "compact", "precision", "grh"):
        assert qualification in note
    assert "v2" in note and "bit-size" in note and "typo" in note
    paragraphs = [" ".join(p.casefold().split())
                  for p in (audit.ROOT / NOTE).read_text().split("\n\n")]
    assert any(
        "classical" in p
        and re.search(r"lower bound|lower-bound|hardness|separation", p)
        and re.search(r"\b(no|not|unproved|unproven|unknown|open)\b", p)
        for p in paragraphs
    ), "Known polynomial quantum algorithms are not proved classical lower bounds"


def test_independent_dual_vectors_need_not_be_a_saturated_lattice_basis():
    # These are independent members of Z^2, but they generate only 2Z x Z.
    sampled_dual = ((2, 0), (0, 1))
    determinant = sampled_dual[0][0] * sampled_dual[1][1]
    assert determinant == 2
    assert 1 % sampled_dual[0][0] != 0  # (1, 0) is missing from the sampled span.
    inferred_primal = ((Fraction(1, 2), 0), (0, Fraction(1)))
    assert inferred_primal[0][0] * sampled_dual[0][0] == 1
    assert inferred_primal[1][1] * sampled_dual[1][1] == 1
    assert inferred_primal[0][0].denominator != 1  # Not in the true primal Z^2.
    assert inferred_primal[0][0] * inferred_primal[1][1] == Fraction(1, 2)
    assert Fraction(1, determinant) != 1  # True primal covolume is 1.


@pytest.mark.parametrize("rank,bits", ((1, 1), (2, 3), (32, 9), (128, 16)))
def test_exponential_grid_dimension_is_not_a_register_or_qft_gate_lower_bound(rank, bits):
    # Count the standard product circuit, never allocate its exponential state.
    cells_per_axis = 1 << bits
    grid_dimension = cells_per_axis ** rank
    qubits = rank * bits
    assert (grid_dimension - 1).bit_length() == qubits
    hadamards = [(axis, wire) for axis in range(rank) for wire in range(bits)]
    assert len(hadamards) == qubits  # Uniform preparation from the all-zero state.
    controlled_phases = [(axis, control, target) for axis in range(rank)
                         for target in range(bits) for control in range(target + 1, bits)]
    assert len(controlled_phases) == rank * bits * (bits - 1) // 2
    swaps = rank * (bits // 2)
    assert len(hadamards) + len(controlled_phases) + swaps <= rank * (bits * bits + bits)
    # Controlled rotations here are ideal gates. Synthesis precision, the field
    # oracle, lattice sampling/reconstruction and full-solver costs are NOT proved.
