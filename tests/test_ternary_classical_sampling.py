from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import subprocess
from types import SimpleNamespace

import pytest

from theorems import ternary_classical_sampling as audit


def problem(forms, offsets):
    return {"spins": len(forms[0]), "forms": forms, "offsets": offsets}


def satisfies(clauses, bits):
    return all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause) for clause in clauses)


def test_encoding_is_bijective_for_every_two_spin_single_affine_exclusion():
    for row in product(range(3), repeat=2):
        for j in range(3):
            p = problem((row,), (j,))
            clauses, support = audit.encode(p)
            images, projections = [], []
            for bits in product((False, True), repeat=6):
                if satisfies(clauses, bits):
                    model = [i if bits[i-1] else -i for i in support]
                    images.append(audit.decode(p, model))
                    projections.append(tuple(bits[i-1] for i in support))
            exact = [word for word in product(range(3), repeat=2) if (sum(a*x for a, x in zip(row, word))+j) % 3]
            assert set(images) == set(exact)
            assert len(images) == len(set(images)) == len(set(projections)) == len(exact)


def test_three_spin_full_constraint_set_matches_native_truth_without_auxiliary_multiplicity():
    p = problem(((1, 2, 1), (0, 1, 2), (2, 0, 1)), (0, 1, 2))
    clauses, support = audit.encode(p)
    actual = []
    for bits in product((False, True), repeat=9):
        if satisfies(clauses, bits):
            actual.append(audit.decode(p, [i if bits[i-1] else -i for i in support]))
    expected = audit.exact_reference(p)
    assert set(actual) == set(expected["solutions"])
    assert len(actual) == expected["count"]


def test_free_original_spins_and_zero_forms_are_not_frozen_or_removed():
    p = problem(((1, 0), (1, 0), (0, 0)), (1, 2, 1))
    clauses, support = audit.encode(p)
    assert len(support) == 4 and audit.exact_reference(p)["count"] == 3
    assert set(audit.exact_reference(p)["solutions"]) == {(0, 0), (0, 1), (0, 2)}
    contradiction = problem(((0, 0),), (0,))
    assert () in audit.encode(contradiction)[0]
    assert audit.exact_reference(contradiction)["count"] == 0


@pytest.mark.parametrize("literals", ([1, -2], [1, 2, -4, -5], [1, -1, -4, -5],
                                    [1, -2, -4, -5, 6], [0, -2, -4, -5]))
def test_partial_ambiguous_or_wrong_projection_is_not_a_native_sample(literals):
    with pytest.raises(ValueError):
        audit.decode(problem(((0, 0),), (1,)), literals)


def test_native_validation_rejects_a_boolean_model_that_violates_the_original_offset():
    p = problem(((1, 0),), (0,))
    with pytest.raises(ValueError):
        audit.decode(p, [1, -2, -4, -5])


def test_exact_pool_sampling_requires_complete_census_and_accounts_for_storage():
    pytest.importorskip("pycosat")
    p = problem(((0, 0),), (1,))
    request = {"problem": p, "samples": 128, "seed": 77, "engine": "picosat-exact", "model_cap": 16}
    result = audit.worker(request)
    assert result["complete_model_count"] == 9
    assert result["complete_pool_storage_trits"] == 18
    assert not result["propagation_limit_used"] and not result["partial_pool_sampled"]
    assert not result["asymptotic_dequantization_established"]
    rng = random.Random(77)
    assert result["selected_pool_indices"] == [rng.randrange(9) for _ in range(128)]
    assert all(audit.valid(p, word) for word in result["returned_native_samples"])


def test_partial_exact_pool_is_NEVER_used_as_a_uniform_sampler():
    pytest.importorskip("pycosat")
    result = audit.worker({"problem": problem(((0, 0),), (1,)), "samples": 16,
                           "seed": 1, "engine": "picosat-exact", "model_cap": 2})
    assert result["status"] == "UNKNOWN_EXACT_POOL_CAP_NO_SAMPLES"
    assert result["returned_native_samples"] == []
    assert not result["partial_pool_sampled"]


def test_exact_unsatisfiable_reference_does_not_create_a_sample_or_a_general_proof():
    pytest.importorskip("pycosat")
    result = audit.worker({"problem": problem(((0, 0),), (0,)), "samples": 1,
                           "seed": 1, "engine": "picosat-exact"})
    assert result["complete_model_count"] == 0
    assert result["returned_native_samples"] == []
    assert not result["solver_proof_independently_checked"]


def test_external_worker_timeout_and_exit_remain_UNKNOWN(monkeypatch):
    p = problem(((0, 0),), (1,))
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], .1, output="partial samples")
    monkeypatch.setattr(audit.subprocess, "run", timeout)
    result = audit.run_backend(p, timeout=.1)
    assert result["status"].startswith("UNKNOWN_WORKER_TIMEOUT")
    assert not result["partial_sample_batch_used"]
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(
        returncode=255, stdout="The formula is unsatisfiable", stderr=""))
    result = audit.run_backend(p)
    assert result["status"] == "UNKNOWN_BACKEND_EXIT_OR_PROTOCOL_FAILURE"
    assert not result["asymptotic_dequantization_established"]


def test_parent_replays_original_input_and_rejects_forged_worker_models(monkeypatch):
    p = problem(((1, 0),), (0,))
    payload = {"status": "VERIFIED_NATIVE_SAMPLES", "problem_sha256": audit.problem_digest(p),
               "returned_native_samples": [[0, 0]]}
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(
        returncode=0, stdout=audit.MARKER+json.dumps(payload), stderr=""))
    with pytest.raises(ValueError):
        audit.run_backend(p, samples=1)


def test_unknown_reference_and_finite_histogram_are_not_uniformity_certificates():
    p = problem(((0, 0),), (1,))
    ref = audit.exact_reference(p)
    diagnostics = audit.sample_diagnostics(p, {"returned_native_samples": [(0, 0)]*10}, ref)
    assert Fraction(diagnostics["empirical_histogram_TV_from_exact_uniform"]) == Fraction(8, 9)
    assert diagnostics["empirical_histogram_TV_is_NOT_engine_distribution_TV"]
    assert audit.exact_reference(p, cap=1)["count"] is None


def test_saved_cases_are_the_UNCHANGED_original_native_inputs():
    saved = json.loads(audit.SAVED_SOURCE.read_text())["classical_original_dual_CSP_controls"]
    for p, original in zip(audit.saved_cases(), saved):
        assert p["forms"] == original["forms_H_transpose"]
        assert p["offsets"] == original["original_offsets"]
        assert p["source_seed"] == original["seed"]


def test_planted_joint_law_has_count_bias_and_is_not_a_fixed_input_sampling_oracle():
    from collections import Counter
    forms = ((1, 1), (1, 2), (2, 1), (2, 2))
    planted = Counter()
    for x in product(range(3), repeat=2):
        for y in product((1, 2), repeat=4):
            J = tuple((value-sum(a*b for a, b in zip(row, x))) % 3 for value, row in zip(y, forms))
            planted[J] += 1
    for J in product(range(3), repeat=4):
        p = problem(forms, J)
        count = audit.exact_reference(p)["count"]
        assert Fraction(planted[J], 9*16)/Fraction(1, 81) == Fraction(count, 9*Fraction(2, 3)**4)
    controls = audit.decoder_count_consequences()
    assert controls[0]["planting_to_uniform_original_offset_TV_exact"] == "2/9"
    assert all(not c["quiet_planting_supplies_fixed_input_sampler"] for c in controls)


@pytest.mark.parametrize("p", (problem(((True, 0),), (1,)), problem(((1, 0),), (3,)),
                                problem(((1, 1, 1, 1),), (1,))))
def test_invalid_or_non_native_domains_are_rejected(p):
    with pytest.raises(ValueError):
        audit.encode(p)


def test_live_report_is_bound_to_original_source_and_preserves_all_unknowns():
    report = json.loads(audit.REPORT.read_text())
    for path, digest in report["source_sha256"].items():
        assert digest == hashlib.sha256((audit.ROOT/path).read_bytes()).hexdigest()
    assert len(report["cases"]) == 4
    assert {p["problem"]["spins"] for p in report["cases"]} == {16, 32}
    assert not report["arbitrary_TV_accuracy_or_independent_backend_proof_claimed"]
    for case in report["cases"]:
        assert not case["asymptotic_dequantization_established"]
        assert not case["source_conditioned_on_success"]
        for word in case.get("returned_native_samples", []):
            assert audit.valid(case["problem"], word)
    pools = {c["problem"]["spins"]: c for c in report["cases"] if c["engine"] == "picosat-exact"}
    assert pools[16]["complete_model_count"] == 67
    assert pools[32]["complete_model_count"] == 10092
    assert all(not c["partial_pool_sampled"] and not c["propagation_limit_used"] for c in pools.values())
