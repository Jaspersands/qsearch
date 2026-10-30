"""Independent primitive-accounting regressions, not circuit verification."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import pytest

from theorems import rees_uniform_instrument as instrument


@pytest.mark.parametrize("profile,p", [
    ((1,), 2), ((4,), 2), ((3, 1), 65537), ((6, 3, 1), 65537),
    ((6, 3, 1), 1000003),
    ((8, 6, 5, 4, 3, 2, 1), 2**61-1),
    ((13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1), 2**127-1),
])
@pytest.mark.parametrize("error", [Fraction(1, 3), Fraction(1, 2**200)])
def test_independent_bottom_up_primitive_recurrence(profile, p, error):
    result = instrument.prime_field_instrument_budget(profile, prime=p, error=error)
    forest = result["recovery_budget"]
    n, c, dimension = profile[0], len(profile), sum(profile)
    nodes = forest["final_fourier_samples"]
    merges = edges = center = bch = brackets = terms = merge_qft = 0
    qmax = dimension
    for stage in reversed(result["stages_top_down"]):
        d, arity = stage["grade"], stage["arity"]
        assert stage["conversions"] == nodes
        group_dimension = sum(profile[:d])
        quotient_dimension = sum(profile[:d-1])
        rank = profile[d-1]
        assert stage["group_dimension"] == group_dimension
        assert stage["central_dimension"] == rank
        assert stage["quotient_dimension"] == quotient_dimension
        # Directly count the nested ODE bracket-convolution loops, without
        # using the planner's closed polynomial formula.
        calls = sum(1 for degree in range(d) for power in range(1, d)
                    for order in range(degree+1) for i in range(order+1))
        assert stage["bracket_calls_per_bch_pass"] == calls
        q = 2*arity*rank + quotient_dimension
        assert stage["qft_calls_per_conversion"] == q
        assert stage["qft_calls"] == nodes*q
        assert stage["central_coordinate_subtractions"] == nodes*arity*rank
        assert stage["controlled_right_actions"] == nodes*arity
        assert stage["bch_evaluation_passes"] == 4*nodes*arity
        assert stage["bracket_calls"] == 4*nodes*arity*calls
        assert stage["dense_structure_tensor_terms"] == 4*nodes*arity*calls*group_dimension**3
        merges += nodes
        edges += nodes*arity
        center += nodes*arity*rank
        bch += 4*nodes*arity
        brackets += 4*nodes*arity*calls
        terms += 4*nodes*arity*calls*group_dimension**3
        merge_qft += nodes*q
        qmax = max(qmax, q)
        nodes *= arity
    leaves, m = nodes, forest["final_fourier_samples"]
    qfts = dimension*leaves + merge_qft + n*m
    assert leaves == forest["source_preparations"]
    assert edges == result["forest_edges"] == result["controlled_right_actions"] == leaves+merges-m
    assert result["central_coordinate_subtractions"] == center
    assert result["bch_evaluation_passes"] == bch
    assert result["bracket_calls"] == brackets
    assert result["dense_structure_tensor_terms"] == terms
    assert result["single_coordinate_qft_calls"] == qfts
    assert qfts <= result["single_coordinate_qft_envelope"] == 6*dimension*leaves
    assert result["ordinary_oracle_queries"] == result["leaf_linear_evaluation_compute_uncompute_pairs"] == c*leaves
    assert result["qft_calls_per_instrument_cap"] == qmax
    eta = error/(3*(leaves+merges+m)*qmax)
    assert result["qft_isometry_error_per_call"] == eta
    assert result["qft_error_bound"] == qfts*eta <= error/3
    assert result["per_instrument_qft_error_bound"] == forest["instrument_error_per_call"]
    bits = result["qft_precision_bits"]
    assert Fraction(1, 2**bits) <= eta < Fraction(1, 2**(bits-1))
    assert result["complete_output_error_bound"] == (
        forest["rank_failure_bound"]+forest["solver_abort_bound"]+qfts*eta)
    assert result["complete_output_error_bound"] <= forest["total_error_bound"] <= error


def test_abelian_case_has_two_fourier_calls_per_coordinate_no_merges():
    result = instrument.prime_field_instrument_budget((4,), prime=2)
    m = 8
    assert result["recovery_budget"]["final_fourier_samples"] == m
    assert result["single_coordinate_qft_calls"] == 2*4*m
    assert result["qft_error_bound"] == Fraction(1, 9)
    assert result["ordinary_oracle_queries"] == m
    assert result["cover_group_register_bits"] == 4
    assert result["stages_top_down"] == []
    for key in ("forest_edges", "bch_evaluation_passes", "bracket_calls",
                "central_coordinate_subtractions", "controlled_right_actions"):
        assert result[key] == 0


def test_class_three_hand_count():
    result = instrument.prime_field_instrument_budget((6, 3, 1), prime=65537)
    # m=10, M2=(3+1)^2=16, M3=1+1=2; 160 top merges and 10 bottom.
    assert result["recovery_budget"]["source_preparations"] == 320
    assert result["ordinary_oracle_queries"] == 960
    assert result["forest_edges"] == 480
    assert result["single_coordinate_qft_calls"] == 3200+160*13+10*102+60 == 6360
    assert result["bch_evaluation_passes"] == 4*480
    assert result["bracket_calls"] == 4*(320*20+160*4) == 28160
    assert result["qft_calls_per_instrument_cap"] == 102


def test_nonlinear_cubic_stage_hand_count():
    result = instrument.prime_field_instrument_budget((6, 3, 1), prime=1000003)
    assert result["recovery_budget"]["stages_top_down"][0]["reduced_degree"] == 3
    assert result["recovery_budget"]["source_preparations"] == 960
    assert result["ordinary_oracle_queries"] == 2880
    assert result["forest_edges"] == 1120
    assert result["single_coordinate_qft_calls"] == 9600+160*21+10*102+60 == 14040
    assert result["bch_evaluation_passes"] == 4*1120
    assert result["bracket_calls"] == 4*(960*20+160*4) == 79360


@pytest.mark.parametrize("profile,p,error", [
    ((), 65537, Fraction(1, 3)), ((3, 3), 65537, Fraction(1, 3)),
    ((3, 2), 65537, Fraction(1, 3)), ((True,), 2, Fraction(1, 3)),
    ((3, 1), 2, Fraction(1, 3)), ((3, 1), 3, Fraction(1, 3)),
    ((4,), None, Fraction(1, 3)), ((4,), True, Fraction(1, 3)),
    ((4,), 2.0, Fraction(1, 3)),
    *[((4,), 2, error) for error in (0.1, 0, True, Fraction(0), Fraction(1))],
])
def test_reject_invalid_shapes_errors_and_unpaid_small_field_branch(profile, p, error):
    with pytest.raises(ValueError):
        instrument.prime_field_instrument_budget(profile, prime=p, error=error)


def test_scope_flags_do_not_promote_execution_or_proof():
    result = instrument.prime_field_instrument_budget((6, 3, 1), prime=65537)
    assert result["uniform_compilation_status"] == "DERIVED_IN_WRITTEN_ARGUMENT_NOT_MACHINE_CERTIFIED"
    for key in ("prime_validation_included", "profile_existence_certified",
                "circuit_generator_implemented", "quantum_receiver_implemented",
                "formal_total_policy_instantiated", "physical_gate_clock",
                "field_enumeration_used", "whole_rees_correctness_certified",
                "novelty_established", "native_application_established",
                "speedup_claim_allowed", "approximate_oracle_error_included",
                "canonical_forbidden_labels_require_hidden_membership_test"):
        assert result[key] is False
    assert result["oracle_queries_executed"] == result["classical_retry_extra_source_copies"] == 0
    for key in ("canonical_subspace_reference_stable_error_required", "joint_source_error_required",
                "zero_scale_is_identity_not_delta_zero", "all_target_slots_consumed",
                "exact_oracle_assumed", "internal_qft_gate_synthesis_errors_included_in_eta"):
        assert result[key] is True


def test_report_source_binding_and_no_promotion():
    payload = instrument.report()
    root = Path(instrument.__file__).resolve().parents[1]
    assert payload == instrument.report()
    assert len(payload["source_sha256"]) == 6
    for path, digest in payload["source_sha256"].items():
        assert sha256((root/path).read_bytes()).hexdigest() == digest
    assert payload["source_hashes_certify_proof"] is False
    assert payload["candidate_promotion"] is payload["proof_promotion"] is False
    assert payload["cases"][-1]["ordinary_oracle_queries"] == 1558649013834350592000


def test_huge_supplied_integer_does_not_enumerate_field(monkeypatch):
    def no_large_range(*args):
        result = range(*args)
        assert result.stop <= 100
        return result
    monkeypatch.setattr(instrument, "range", no_large_range, raising=False)
    # Deliberately not a prime certificate; the planner only uses its promise.
    result = instrument.prime_field_instrument_budget((6, 3, 1), prime=2**4096-1)
    assert result["canonical_field_limb_bits"] == 4096
    assert result["prime_validation_included"] is False
