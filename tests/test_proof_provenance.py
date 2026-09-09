import hashlib
import json
from pathlib import Path

import pytest

from proof_provenance import audit_proof_routes


def scope(conclusion="systematic BABA bound", quantifier="universal"):
    return {"domain": "systematic single-fiber BABA codes", "input_model": "explicit marked group presentation",
            "quantifier": quantifier, "conclusion": conclusion}


def claim(identifier, conclusion=None, *, routes=(), asserted="unresolved", quantifier="universal"):
    return {"id": identifier, "scope": scope(conclusion or identifier, quantifier),
            "asserted_level": asserted, "routes": list(routes)}


def evidence(tmp_path, node, identifier, level="derived-review-pending", data="Written derivation"):
    path = tmp_path / f"{identifier}.txt"
    path.write_text(data)
    return {"id": identifier, "path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "claim_id": node["id"], "scope": node["scope"], "level": level}


def route(identifier, evidence_id, *premises, diagnostics=()):
    return {"id": identifier, "conclusion_evidence": [evidence_id], "premises": list(premises), "diagnostics": list(diagnostics)}


def audit(tmp_path, claims, references):
    return audit_proof_routes({"schema_version": 1, "claims": claims, "evidence": references}, tmp_path)


def test_missing_cubic_premise_blocks_local_but_not_independent_global_route(tmp_path):
    cubic = claim("cubic-uniform-loss")
    bound = claim("bound", asserted="derived-review-pending",
                  routes=[route("local", "local-argument", cubic["id"]), route("global", "suffix-surface")])
    refs = [evidence(tmp_path, bound, "local-argument"), evidence(tmp_path, bound, "suffix-surface")]
    result = audit(tmp_path, [cubic, bound], refs)
    row = next(item for item in result["claims"] if item["id"] == "bound")
    assert [item["support_rank"] for item in row["routes"]] == [0, 3]
    assert result["unsupported_assertion_count"] == 0
    bound["routes"].pop()
    result = audit(tmp_path, [cubic, bound], refs)
    assert result["unsupported_assertion_count"] == 1
    assert not result["mathematical_truth_verified"]


def test_encoded_access_does_not_supply_a_decoder_attestation(tmp_path):
    access = claim("encoded-access", routes=[route("qfts", "access-argument")], asserted="derived-review-pending")
    decoder = claim("decoder", "hidden-element decoder", routes=[route("invalid-transfer", "access-argument", access["id"])],
                    asserted="derived-review-pending")
    report = audit(tmp_path, [access, decoder], [evidence(tmp_path, access, "access-argument")])
    assert report["unsupported_assertion_count"] == 1
    assert any(item["code"] == "scope-mismatch" for item in report["issues"])


def test_identification_bound_does_not_transfer_to_binary_decision(tmp_path):
    identification = claim("identification", "fixed-reference identification success bound")
    binary = claim("binary", "binary class decision impossible", routes=[route("invalid", "id-bound")], asserted="derived-review-pending")
    report = audit(tmp_path, [binary], [evidence(tmp_path, identification, "id-bound")])
    assert report["unsupported_assertion_count"] == 1


@pytest.mark.parametrize("level", ("observed", "exact-finite", "machine-checked"))
def test_no_finite_promotion_or_unimplemented_formal_checker(tmp_path, level):
    node = claim("uniform", routes=[route("route", "attestation")], asserted="derived-review-pending")
    report = audit(tmp_path, [node], [evidence(tmp_path, node, "attestation", level)])
    assert report["unsupported_assertion_count"] == 1


def test_source_edits_make_evidence_stale_without_repinning(tmp_path):
    node = claim("claim", routes=[route("route", "argument")], asserted="derived-review-pending")
    ref = evidence(tmp_path, node, "argument")
    (tmp_path / ref["path"]).write_text("Changed assertion")
    report = audit(tmp_path, [node], [ref])
    assert any(item["code"] == "stale-source" for item in report["issues"])
    assert report["unsupported_assertion_count"] == 1


def test_failed_diagnostic_blocks_route_without_claiming_counterexample(tmp_path):
    node = claim("claim", routes=[route("route", "argument", diagnostics=["control"])], asserted="derived-review-pending")
    ref = evidence(tmp_path, node, "control", "observed", json.dumps({"passed": False}))
    ref["predicates"] = [{"pointer": "/passed", "equals": True}]
    report = audit(tmp_path, [node], [evidence(tmp_path, node, "argument"), ref])
    assert any(item["code"] == "failed-diagnostic" for item in report["issues"])
    assert report["unsupported_assertion_count"] == 1
    assert all(item["supported_level"] == "unresolved" for item in report["claims"])


def test_boolean_checks_do_not_accept_integer_one(tmp_path):
    node = claim("claim", routes=[route("r", "arg", diagnostics=["control"])], asserted="derived-review-pending")
    ref = evidence(tmp_path, node, "control", data='{"passed":1}')
    ref["predicates"] = [{"pointer": "/passed", "equals": True}]
    assert audit(tmp_path, [node], [evidence(tmp_path, node, "arg"), ref])["unsupported_assertion_count"] == 1


def test_cycles_and_dangling_premises_cannot_self_certify(tmp_path):
    a = claim("a", routes=[route("r", "a-e", "b")], asserted="derived-review-pending")
    b = claim("b", routes=[route("r", "b-e", "a")], asserted="derived-review-pending")
    refs = [evidence(tmp_path, a, "a-e"), evidence(tmp_path, b, "b-e")]
    result = audit(tmp_path, [a, b], refs)
    assert result["unsupported_assertion_count"] == 2
    assert any(item["code"] == "dependency-cycle" for item in result["issues"])
    a["routes"][0]["premises"] = ["missing"]
    assert audit(tmp_path, [a], refs)["unsupported_assertion_count"] == 1


def test_duplicate_ids_are_rejected(tmp_path):
    with pytest.raises(ValueError):
        audit(tmp_path, [claim("same"), claim("same")], [])


def test_grounded_alternative_in_a_cycle_is_order_independent(tmp_path):
    a = claim("a", routes=[route("dependent", "a-e", "b"), route("independent", "a-e")], asserted="derived-review-pending")
    b = claim("b", routes=[route("dependent", "b-e", "a")], asserted="derived-review-pending")
    refs = [evidence(tmp_path, a, "a-e"), evidence(tmp_path, b, "b-e")]
    for nodes in ([a, b], [b, a]):
        result = audit(tmp_path, nodes, refs)
        assert result["unsupported_assertion_count"] == 0
        assert all(row["support_rank"] == 3 for row in result["claims"])


def test_curated_live_contracts_keep_local_gap_and_decoder_open():
    from proof_provenance_seed import build_initial_proof_routes
    root = Path(__file__).resolve().parents[1]
    report = audit_proof_routes(build_initial_proof_routes(root), root)
    rows = {row["id"]: row for row in report["claims"]}
    assert rows["LOCAL-SYSTEMATIC-BOUND"]["supported_level"] == "unresolved"
    assert rows["SYSTEMATIC-BABA-BOUND"]["supported_level"] == "derived-review-pending"
    assert rows["ENCODED-RESTRICTION"]["supported_level"] == "derived-review-pending"
    assert rows["HIDDEN-INVOLUTION-DECODER"]["supported_level"] == "unresolved"
    assert rows["BINARY-DETECTION-IMPOSSIBLE"]["supported_level"] == "unresolved"
    assert report["unsupported_assertion_count"] == 0


def test_registry_validation_rejects_an_unsupported_assertion(tmp_path, monkeypatch):
    from research_registry import initialize_seed_registry, validate_registry
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=True)
    bad = claim("unsupported", asserted="derived-review-pending")
    path = tmp_path / "research/registry/proof_routes.json"
    path.write_text(json.dumps({"schema_version": 1, "claims": [bad], "evidence": []}))
    result = validate_registry()
    assert not result["valid"]
    assert any(row["obligation_id"] == "PROOF-PROVENANCE" for row in result["issues"])


def test_initialization_never_overwrites_existing_pins(tmp_path):
    from proof_provenance_seed import initialize_proof_routes
    path = tmp_path / "manifest.json"
    root = Path(__file__).resolve().parents[1]
    initialize_proof_routes(path, root)
    before = path.read_bytes()
    with pytest.raises(FileExistsError):
        initialize_proof_routes(path, root)
    assert path.read_bytes() == before


def test_committed_manifest_pins_are_checked_without_regeneration():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "research/registry/proof_routes.json").read_text())
    result = audit_proof_routes(manifest, root)
    assert result["claim_count"] == 13
    assert result["unsupported_assertion_count"] == 0
    assert not any(row["code"] == "stale-source" for row in result["issues"])


def test_scoped_discard_bound_cannot_supply_general_binary_impossibility(tmp_path):
    discard = claim("discard", "classical-adaptive preinteraction twirl information bound")
    binary = claim("binary", "binary detection impossible for arbitrary coset-state algorithms",
                   routes=[route("bad-transfer", "discard-bound")], asserted="derived-review-pending")
    report = audit(tmp_path, [binary], [evidence(tmp_path, discard, "discard-bound")])
    assert report["unsupported_assertion_count"] == 1
    assert any(row["code"] == "scope-mismatch" for row in report["issues"])


@pytest.mark.parametrize("pointer", ("/rows/-1", "/rows/01", "/bad~2key"))
def test_invalid_json_pointers_fail_closed(tmp_path, pointer):
    node = claim("c", routes=[route("r", "e", diagnostics=["control"])], asserted="derived-review-pending")
    ref = evidence(tmp_path, node, "control", data='{"rows":[1,1],"bad~2key":1}')
    ref["predicates"] = [{"pointer": pointer, "equals": 1}]
    assert audit(tmp_path, [node], [evidence(tmp_path, node, "e"), ref])["unsupported_assertion_count"] == 1
