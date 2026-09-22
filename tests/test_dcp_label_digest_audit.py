from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from dcp_label_digest_audit import (
    REQUIRED_SCOPE, audit_digest, coordinate_bit_bound, physical_observation_counts,
    run_digest_audit, scope_issues, slice_fiber_profile, sqrt_upper,
    write_digest_audit_report,
)


def test_outward_square_roots_are_integer_certified():
    for value in (Fraction(0), Fraction(1, 3), Fraction(2), Fraction(9, 4), Fraction(1, 1 << 513)):
        upper = sqrt_upper(value, 550)
        assert upper**2 >= value
        assert upper == 0 or (upper-Fraction(1, 1 << 550))**2 < value


@pytest.mark.parametrize("condition_on_z", [False, True])
def test_physical_prefix_matches_independent_complex_preparation(condition_on_z):
    n, m, modulus = 2, 3, 4
    fixed = lambda labels: (labels[0] + 2*labels[1] + labels[2]) % modulus
    adaptive = lambda labels, z: (labels[0]+z*labels[1]+labels[2]) % 2
    digest = adaptive if condition_on_z else fixed
    counts, denominator, _ = physical_observation_counts(n, m, digest, condition_on_z=condition_on_z)
    for secret in (0, 1, 2, 3):
        independently_prepared = {}
        for labels in product(range(modulus), repeat=m):
            residues = [sum(labels[j]*((b >> j) & 1) for j in range(m)) % modulus for b in range(1 << m)]
            phases = np.exp(2j*np.pi*secret*np.array(residues)/modulus) / np.sqrt(1 << m)
            for z in range(modulus//2):
                vector = np.zeros(1 << (m+1), dtype=complex)
                for b, residue in enumerate(residues):
                    if residue % (modulus//2) == z:
                        vector[2*b+residue//(modulus//2)] = phases[b]
                key = (digest(labels, z) if condition_on_z else digest(labels), z)
                independently_prepared.setdefault(key, np.zeros((len(vector), len(vector)), complex))
                independently_prepared[key] += np.outer(vector, vector.conj())/modulus**m
        signs = (-1)**(secret*(np.arange(1 << (m+1)) % 2))
        for key, matrix in independently_prepared.items():
            expected = counts.get(key, np.zeros_like(matrix))*np.outer(signs, signs)/denominator
            np.testing.assert_allclose(matrix, expected, atol=1e-14)


def test_born_weighting_not_uniform_branch_conditioning():
    row = audit_digest(3, 1, lambda _: 0, "one-sample")
    assert row["parity_trace_distance"] == pytest.approx(1/8)
    masses = row["z_born_mass_numerators"]
    assert masses[0] > masses[1]
    assert sum(masses.values()) == row["normalization_denominator"]


def test_one_sample_trace_distance_with_exact_rational_eigenvalues():
    import sympy as s
    blocks, denominator, _ = physical_observation_counts(3, 1, lambda y: 0)
    sign = s.diag(1, -1, 1, -1)
    distance = s.S(0)
    for counts in blocks.values():
        matrix = s.Matrix(counts.tolist())/denominator
        difference = matrix-sign*matrix*sign
        distance += sum(abs(value)*count for value, count in difference.eigenvals().items())/2
    assert distance == s.Rational(1, 8)


def test_incomplete_label_tables_cannot_certify_uniform_source_bounds():
    with pytest.raises(ValueError, match="complete uniform"):
        slice_fiber_profile(3, 1, {(i,): 0 for i in range(7)})


@pytest.mark.parametrize("seed", range(6))
def test_arbitrary_joint_digest_controls(seed):
    rng = np.random.default_rng(seed)
    table = {y: int(rng.integers(3)) for y in product(range(4), repeat=3)}
    row = audit_digest(2, 3, table.__getitem__, "random-joint")
    assert all(row["checks"].values())


def test_joint_sum_does_not_get_a_fake_per_coordinate_bit_budget():
    row = audit_digest(3, 3, lambda y: sum(y) % 8, "joint-sum")
    assert row["digest_outcomes"] == 8
    assert row["fiber_profile"]["maximum_slice_image_sizes"] == [8, 8, 8]
    assert row["fiber_profile"]["trace_distance_upper"] == {"numerator": 1, "denominator": 1}


def test_unbalanced_fibers_improve_on_alphabet_cardinality():
    _, _, table = physical_observation_counts(4, 1, lambda y: int(y[0] == 0))
    profile = slice_fiber_profile(4, 1, table)
    cap = profile["coordinate_beta_upper"][0]
    bound = Fraction(cap["numerator"], cap["denominator"])
    assert bound < sqrt_upper(Fraction(2, 16))


def test_compression_cannot_increase_actual_parity_information():
    full = audit_digest(3, 3, lambda y: y, "full")
    for digest in (lambda y: 0, lambda y: sum(y) % 8, lambda y: tuple(a >> 2 for a in y)):
        compressed = audit_digest(3, 3, digest, "compressed")
        assert compressed["parity_trace_distance"] <= full["parity_trace_distance"] + 1e-12


def test_analytic_scaling_and_full_label_escape_are_separate():
    assert coordinate_bit_bound(256, (86,)*(256**2)) < Fraction(1, 1 << 60)
    assert coordinate_bit_bound(256, (256,)*2) == 1
    assert coordinate_bit_bound(256, (240,)*(256**2)) == 1
    assert coordinate_bit_bound(4, ()) == 0


def test_scope_rejects_unproved_and_changed_access_premises():
    contract = {key: True for key in REQUIRED_SCOPE}
    assert not scope_issues(contract)
    for key in REQUIRED_SCOPE:
        for wrong in (False, "true", 1, None):
            assert scope_issues({**contract, key: wrong}) == [key]


def test_omitting_the_low_sum_measurement_invalidates_the_information_bound():
    # Actual one-sample DCP states, before the prefix, not a new problem family.
    modulus = 16
    states = []
    for secret in (0, 1):
        state = np.zeros((2, 2), complex)
        for label in range(modulus):
            vector = np.array([1, np.exp(2j*np.pi*secret*label/modulus)])/np.sqrt(2)
            state += np.outer(vector, vector.conj())/modulus
        states.append(state)
    distance = np.abs(np.linalg.eigvalsh(states[0]-states[1])).sum()/2
    assert distance == pytest.approx(.5)
    assert distance > float(coordinate_bit_bound(4, (0,)))
    # This pair-specific control does not recover parity for a uniform secret.


@pytest.mark.parametrize("n,m", [(0, 2), (2, 0), (True, 1), (5, 5), (2, 8)])
def test_invalid_or_exponential_controls_are_not_silently_run(n, m):
    with pytest.raises(ValueError):
        physical_observation_counts(n, m, lambda y: y)


def test_report_keeps_all_claim_limits():
    report = run_digest_audit()
    assert report["headline_metrics"]["finite_control_count"] == 32
    assert report["headline_metrics"]["finite_control_failure_count"] == 0
    assert not report["source"]["lean_replayed_locally"]
    for key in ("speedup_claim_allowed", "novelty_established", "formal_verification",
                "arbitrary_measurement_adaptive_digest_covered", "general_dcp_no_go"):
        assert report["claim_gate"][key] is False
    assert report["claim_gate"]["low_sum_conditioned_digest_covered"] is True


@pytest.mark.parametrize("seed", range(4))
def test_low_sum_dependent_joint_maps_use_the_separate_range_bound(seed):
    rng = np.random.default_rng(seed)
    table = {(y, z): int(rng.integers(2)) for y in product(range(8), repeat=2) for z in range(4)}
    row = audit_digest(3, 2, lambda y, z: table[y, z], "z-dependent", condition_on_z=True)
    assert all(row["checks"].values())
    cap = row["fiber_profile"]["trace_distance_upper"]
    assert Fraction(cap["numerator"], cap["denominator"]) <= 1
    assert "fiber_size_histograms" not in row["fiber_profile"]


def test_writer_respects_registry_toggle_and_custom_ids(tmp_path, monkeypatch):
    import dcp_label_digest_audit as module
    records, negatives = [], []
    monkeypatch.setattr(module, "upsert_experiment_result", records.append)
    monkeypatch.setattr(module, "upsert_negative_result", negatives.append)
    path = tmp_path / "digest.json"
    write_digest_audit_report(path, write_registry=False)
    assert path.exists() and not records and not negatives
    write_digest_audit_report(path, registry_experiment_id="EXP-CUSTOM", registry_candidate_id="CUSTOM",
                             registry_result_id="RESULT-CUSTOM")
    assert records[0].id == "RESULT-CUSTOM"
    assert records[0].candidate_id == "CUSTOM"
    assert negatives[0].applies_to == ["CUSTOM"]


def test_runner_registry_proof_and_access_boundary_integration(tmp_path, monkeypatch):
    import json
    from dcp_label_digest_audit import EXPERIMENT_ID, REPORT_PATH
    from experiment_runner import run_experiment
    from proof_tracker import _dcp_label_digest_lemmas
    from dequantization_checks import build_dequantization_report
    from research_registry import initialize_seed_registry, load_experiment_results, validate_registry
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=False)
    payload = write_digest_audit_report()
    for _ in range(2):
        assert run_experiment(EXPERIMENT_ID).status == "completed"
    assert len([r for r in load_experiment_results() if r["experiment_id"] == EXPERIMENT_ID]) == 1
    assert validate_registry()["valid"]
    assert any(row["id"].endswith("DCP-FIXED-DIGEST-ACCESS-BOUNDARY")
               for row in build_dequantization_report()["findings"])
    assert _dcp_label_digest_lemmas("DHS-GOWERS-SIEVE")[0].status.startswith("derived")
    payload["claim_gate"]["finite_controls_passed"] = 1
    REPORT_PATH.write_text(json.dumps(payload))
    assert _dcp_label_digest_lemmas("DHS-GOWERS-SIEVE")[0].status.startswith("blocked")


def test_cli_bootstraps_missing_experiment_and_validates_registry(tmp_path, monkeypatch):
    from argparse import Namespace
    import qsearch
    from research_registry import load_experiments, validate_registry
    from dcp_label_digest_audit import EXPERIMENT_ID
    monkeypatch.chdir(tmp_path)
    assert qsearch.command_dcp_label_digest_audit(Namespace()) == 0
    assert any(row["id"] == EXPERIMENT_ID for row in load_experiments())
    assert validate_registry()["valid"]
