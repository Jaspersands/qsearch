from itertools import permutations
from fractions import Fraction

import numpy as np
import pytest

from coset_hidden_involution_encoded_restriction import (
    factor_left_hyperoctahedral_coset, finite_encoded_restriction,
    build_encoded_restriction_report, _wreath_matrix,
    finite_physical_fourier_control, finite_reference_orbit_control,
    matching_orbit_type, reference_invariant_identification_bound,
)
from coset_hidden_involution_binary_decision_reduction import compose_permutations
from coset_hidden_involution_bounded_support_commutant_generation import hyperoctahedral_group


def test_coset_factor_is_bijective_and_has_correct_left_action():
    subgroup = hyperoctahedral_group(2)
    seen = set()
    for g in permutations(range(4)):
        k, matching, t = factor_left_hyperoctahedral_coset(g)
        assert k in subgroup
        assert compose_permutations(k, t) == g
        assert (k, matching) not in seen
        seen.add((k, matching))
        for h in subgroup:
            k2, matching2, t2 = factor_left_hyperoctahedral_coset(compose_permutations(h, g))
            assert matching2 == matching and t2 == t
            assert k2 == compose_permutations(h, k)
    assert len(seen) == 24


def test_signed_induced_matrix_convention_is_a_representation():
    group = hyperoctahedral_group(3)
    for left in group[::5]:
        for right in group[::7]:
            np.testing.assert_allclose(
                _wreath_matrix((1, 1), (1,), compose_permutations(left, right)),
                _wreath_matrix((1, 1), (1,), left) @ _wreath_matrix((1, 1), (1,), right), atol=1e-12)


def test_fixed_column_changes_do_not_break_the_encoded_isometry():
    for column in (0, 5):
        row = finite_encoded_restriction((3, 2, 1), fixed_column=column)
        assert row["finite_normalization_and_covariance_verified"]
        assert row["embedding_isometry_residual"] < 1e-11


def test_repeated_copy_block_is_checked_not_only_multiplicity_free_controls():
    row = finite_encoded_restriction((4, 2, 2))
    assert row["finite_normalization_and_covariance_verified"]
    block = next(item for item in row["blocks"] if item["alpha"] == [2] and item["beta"] == [2])
    assert block["expected_copy_dimension"] == block["code_rank"] == 2
    assert block["encoded_multiplicity_ambient_dimension"] > 2
    assert block["carrier_identity_tensor_code_residual"] < 1e-9
    logical = block["logical_action"]
    assert logical["normalization_factor"] == 1
    assert logical["maximum_logical_operator_norm"] <= 1 + 1e-10
    assert logical["maximum_logical_commutator_norm"] > 1e-5
    assert logical["carrier_identity_tensor_logical_action_residual"] < 1e-9


def test_physical_coset_columns_do_not_receive_free_hidden_alignment():
    row = finite_physical_fourier_control()
    assert row["physical_convention_and_alignment_distinction_verified"]
    assert row["qft_unitarity_residual"] < 1e-10
    for control in row["reference_parity_controls"]:
        assert control["reference_odd_mass"] == pytest.approx(0 if control["aligned"] else 0.5)


@pytest.mark.parametrize("rank", (2, 3, 4))
def test_fixed_reference_orbits_bound_identification_not_binary_detection(rank):
    row = finite_reference_orbit_control(rank)
    assert row["partition_classification_verified"]
    assert sum(item["size"] for item in row["orbits"]) == row["hypotheses"]
    assert Fraction(row["identification_upper_bound"]) == Fraction(row["orbit_count"], row["hypotheses"])
    assert not row["binary_decision_ruled_out"]
    assert reference_invariant_identification_bound(rank, 0) == Fraction(1, row["hypotheses"])


def test_orbit_bound_has_explicit_classical_query_scope_and_scaling():
    assert reference_invariant_identification_bound(64) < Fraction(1, 2**300)
    assert reference_invariant_identification_bound(2, 4) == 1
    assert matching_orbit_type(((0, 1), (2, 3))) == (1, 1)
    assert matching_orbit_type(((0, 2), (1, 3))) == (2,)
    with pytest.raises(ValueError):
        matching_orbit_type(((0, 0), (1, 2)))
    with pytest.raises(ValueError):
        reference_invariant_identification_bound(0)


def test_report_does_not_promote_encoded_access_to_decoder_or_unknown_alignment():
    report = build_encoded_restriction_report()
    assert report["headline_metrics"]["finite_isometry_controls_passed"] == 5
    assert report["headline_metrics"]["scalable_factorization_trials_passed"] == 96
    assert report["headline_metrics"]["repeated_copy_blocks_verified"] >= 1
    assert report["access_contract"]["postselection_steps"] == 0
    assert not report["claim_gate"]["unknown_hidden_centralizer_access_granted"]
    assert not report["claim_gate"]["explicit_copy_basis_compiled"]
    assert not report["claim_gate"]["speedup_claim_allowed"]
    assert not report["claim_gate"]["binary_decision_ruled_out_by_reference_bound"]


def test_bad_permutations_and_fixed_columns_are_rejected():
    for value in ((0, 0), (0, 1, 2), ()):
        with pytest.raises(ValueError):
            factor_left_hyperoctahedral_coset(value)
    with pytest.raises(ValueError):
        finite_encoded_restriction((3, 1), fixed_column=3)


def test_clean_registry_runner_retains_access_boundary(tmp_path, monkeypatch):
    from experiment_runner import run_experiment, supported_experiment_ids
    from research_registry import initialize_seed_registry, load_negative_results, validate_registry
    from proof_tracker import _encoded_restriction_lemmas
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=True)
    identifier = "EXP-COSET-HIDDEN-INVOLUTION-ENCODED-RESTRICTION"
    assert identifier in supported_experiment_ids()
    result = run_experiment(identifier)
    assert result.status == "completed"
    assert any(item["id"] == "ENCODED-CARRIER-EXTRACTION-NOT-EXPLICIT-COPY-INDEX-OR-DECODER"
               for item in load_negative_results())
    from dequantization_checks import findings_from_negative_results
    findings = findings_from_negative_results([{"id": "CODE-COSET-COLLECTIVE"}], load_negative_results())
    assert any(item.id.endswith("FIXED-REFERENCE-IDENTIFICATION") for item in findings)
    lemmas = _encoded_restriction_lemmas("CODE-COSET-COLLECTIVE")
    assert lemmas[0].status == "derived-encoded-restriction-review-pending"
    assert lemmas[1].status == "derived-reference-orbit-bound-review-pending"
    assert lemmas[2].status.startswith("blocked-")
    assert validate_registry()["valid"]
