from dataclasses import replace
from fractions import Fraction

import pytest

from coset_hidden_involution_reference_twirl_information import (
    DEFAULT_EXPERIMENT_ID, NEGATIVE_ID, block_twirl_distance_squared_bound,
    adaptive_block_twirl_distance_squared_bound, finite_adaptive_reference_control,
    finite_coherent_reference_erasure_control,
    build_reference_twirl_information_report, finite_binary_control,
    finite_regular_basis_control, fixed_reference_mixture_chi_squared,
    matching_count, necessary_equal_block_size, orbit_block_chi_squared,
    reference_orbit_size, write_reference_twirl_information_report,
)
from representation_obstruction import integer_partitions


@pytest.mark.parametrize("m", range(1, 12))
def test_exact_reference_orbit_sizes_partition_the_natural_source(m):
    assert sum(reference_orbit_size(nu) for nu in integer_partitions(m)) == matching_count(m)


def test_independent_inputs_are_not_one_joint_twirl():
    separate = finite_binary_control(2, (1, 1))
    joint = finite_binary_control(2, (2,))
    assert separate["raw_binary_trace_distance"] == pytest.approx(3 / 8)
    assert separate["twirled_binary_trace_distance"] == pytest.approx(1 / 3)
    assert joint["twirled_binary_trace_distance"] == pytest.approx(3 / 8)
    assert joint["single_global_block_invariance_residual"] < 1e-10
    assert separate["twirled_trace"] == pytest.approx(1)


def test_six_point_noncommuting_controls_retain_physical_fourier_weights():
    separate = finite_binary_control(3, (1, 1))
    joint = finite_binary_control(3, (2,))
    assert separate["physical_finite_controls_verified"]
    assert joint["physical_finite_controls_verified"]
    assert separate["twirled_binary_trace_distance"] < joint["twirled_binary_trace_distance"]
    assert joint["twirled_binary_trace_distance"] == pytest.approx(joint["raw_binary_trace_distance"])


def test_regular_basis_independently_checks_fourier_purity_and_pinsker_constants():
    report = finite_regular_basis_control()
    assert report["independent_regular_controls_verified"]
    assert report["regular_binary_trace_distance"] == pytest.approx(1 / 3)
    assert {row["orbit_size"] for row in report["orbit_controls"]} == {1, 2}
    assert all(row["verified"] for row in report["orbit_controls"])


def test_large_moments_from_rare_orbits_are_not_success_certificates():
    assert fixed_reference_mixture_chi_squared(8, (1,) * 64) > 1_000_000
    assert block_twirl_distance_squared_bound(8, (1,) * 64) == Fraction(64, 184275)
    assert block_twirl_distance_squared_bound(8, (1,) * 64) < Fraction(1, 2500)
    for m in (1, 2, 3, 4):
        for b in (1, 2, 3):
            # The full-class mixture has regular-basis second moment (2^b-1)/M.
            assert fixed_reference_mixture_chi_squared(m, (b,)) == Fraction(2**b - 1, matching_count(m))


def test_exact_block_budget_is_necessary_and_not_sufficient():
    m, blocks, target = 128, 128**2, Fraction(1, 3)
    size = necessary_equal_block_size(m, blocks, target)
    assert size == 792
    assert block_twirl_distance_squared_bound(m, (size - 1,) * blocks) < target**2
    assert block_twirl_distance_squared_bound(m, (size,) * blocks) >= target**2
    assert block_twirl_distance_squared_bound(m, (1,) * blocks) < Fraction(1, 2**794)
    assert orbit_block_chi_squared(6, 3) == Fraction(7, 6)
    assert block_twirl_distance_squared_bound(2, ()) == 0
    assert fixed_reference_mixture_chi_squared(2, ()) == 0


def test_adaptive_hybrid_bound_is_weaker_and_does_not_assume_uniform_posteriors():
    assert adaptive_block_twirl_distance_squared_bound(8, (1, 2, 3)) == 3 * block_twirl_distance_squared_bound(8, (1, 2, 3))
    assert adaptive_block_twirl_distance_squared_bound(8, ()) == 0
    b = necessary_equal_block_size(128, 128**2, adaptive=True)
    assert b == 778
    assert adaptive_block_twirl_distance_squared_bound(128, (b - 1,) * 128**2) < Fraction(1, 9)
    assert adaptive_block_twirl_distance_squared_bound(128, (b,) * 128**2) >= Fraction(1, 9)
    for m in (2, 3, 4):
        control = finite_adaptive_reference_control(m)
        assert control["exact_transcript_control_verified"]
        assert Fraction(control["posterior_reciprocal_orbit_mean_after_positive"]) > Fraction(control["prior_reciprocal_orbit_mean"])
    assert finite_adaptive_reference_control(2)["transcript_trace_distance"] == "1/4"


@pytest.mark.parametrize("partition", integer_partitions(4))
def test_coherent_preinteraction_can_transfer_all_information_before_carrier_erasure(partition):
    row = finite_coherent_reference_erasure_control(partition)
    assert row["finite_identity_channel_recovery_verified"]
    assert row["all_matrix_unit_recovery_residual"] < 1e-10
    assert row["fourier_bell_factorization_residual"] < 1e-10
    assert row["matrix_units_checked"] == row["input_dimension"]**2
    assert row["input_hidden_information_already_transferred_to_reference"]
    assert not row["preinteraction_twirl_assumption_satisfied"]
    assert not row["hidden_involution_decoder_supplied"]


@pytest.mark.parametrize("bad", (0, -1, True, 1.5, "3"))
def test_invalid_integer_parameters_are_not_silently_coerced(bad):
    with pytest.raises(ValueError):
        matching_count(bad)
    with pytest.raises(ValueError):
        orbit_block_chi_squared(2, bad)
    with pytest.raises(ValueError):
        block_twirl_distance_squared_bound(4, (bad,))
    with pytest.raises(ValueError):
        necessary_equal_block_size(4, bad)


@pytest.mark.parametrize("bad", ((), (0,), (1, 2), (True,), (-1, 2)))
def test_invalid_orbit_partitions_are_rejected(bad):
    with pytest.raises(ValueError):
        reference_orbit_size(bad)


def test_report_limits_do_not_close_coherent_or_general_binary_routes():
    report = build_reference_twirl_information_report()
    gate = report["claim_gate"]
    assert gate["finite_controls_verified"]
    assert gate["scoped_blockwise_information_bound_derived"]
    assert gate["classically_adaptive_preinteraction_twirl_bound_derived"]
    for key in ("general_binary_detection_ruled_out", "single_global_twirl_ruled_out",
                "coherent_encoded_access_ruled_out", "quantum_controlled_reference_bound_derived",
                "new_general_entanglement_lower_bound_claimed", "machine_checked_proof", "speedup_claim_allowed"):
        assert gate[key] is False
    assert report["headline_metrics"]["finite_binary_controls_passed"] == 10
    assert report["headline_metrics"]["strict_finite_information_loss_controls"] >= 5
    assert "same h" in report["scope"]["prior"]
    assert "AND" in report["scope"]["equivalent_single_copy_discard"]
    assert "BEFORE memory interaction" in report["scope"]["adaptive_extension"]


def test_no_registry_flag_and_clean_registry_runner(tmp_path, monkeypatch):
    from experiment_runner import run_experiment, supported_experiment_ids
    from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry
    from dequantization_checks import findings_from_negative_results
    from proof_tracker import _reference_twirl_information_lemmas
    monkeypatch.chdir(tmp_path)
    write_reference_twirl_information_report(write_registry=False)
    assert not (tmp_path / "research/registry").exists()
    initialize_seed_registry(overwrite=True)
    assert DEFAULT_EXPERIMENT_ID in supported_experiment_ids()
    assert run_experiment(DEFAULT_EXPERIMENT_ID).status == "completed"
    assert any(row["experiment_id"] == DEFAULT_EXPERIMENT_ID for row in load_experiment_results())
    negatives = load_negative_results()
    negative = next(row for row in negatives if row["id"] == NEGATIVE_ID)
    assert "scope" in negative["evidence"]
    findings = findings_from_negative_results([{"id": "CODE-COSET-COLLECTIVE"}], negatives)
    finding = next(row for row in findings if row.id.endswith("REFERENCE-TWIRL-INFORMATION-LOSS"))
    assert "not classical dequantization" in finding.required_action
    lemmas = _reference_twirl_information_lemmas("CODE-COSET-COLLECTIVE")
    assert lemmas[0].status == "derived-blockwise-information-bound-review-pending"
    assert lemmas[1].status == "derived-adaptive-preinteraction-twirl-bound-review-pending"
    assert lemmas[2].status.startswith("blocked-")
    assert validate_registry()["valid"]


def test_missing_report_does_not_assert_a_supported_proof(tmp_path, monkeypatch):
    from proof_tracker import _reference_twirl_information_lemmas
    monkeypatch.chdir(tmp_path)
    assert all(row.status.startswith("blocked-") for row in _reference_twirl_information_lemmas("CODE-COSET-COLLECTIVE"))


def test_typed_gate_rejects_discard_even_when_mutation_is_renamed():
    from coset_recoupling_mechanism_synthesis import TEMPLATES, evaluate_template
    discarded = next(row for row in TEMPLATES if row.id == "MECH-INDEPENDENT-MULTIPLICITY-ONLY-DECODER")
    renamed = replace(discarded, id="OTHER-MUTATION-ID", known_no_go_violations=())
    evaluation = evaluate_template(renamed)
    assert evaluation.typed_interfaces_valid
    assert evaluation.decision == "rejected"
    assert any("Independent reference-carrier discard" in item for item in evaluation.known_no_go_violations)
    coherent = next(row for row in TEMPLATES if row.id == "MECH-ENCODED-REFERENCE-SYMMETRY-BREAKING")
    assert evaluate_template(coherent).decision == "proposal-only-missing-proof-capabilities"
