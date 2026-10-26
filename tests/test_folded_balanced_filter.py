"""Independent identities and failure controls, not quantum-speedup tests."""
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from math import comb

import pytest

from theorems import folded_balanced_filter as module


@pytest.fixture(scope="module")
def report():
    return module.build_report()


@pytest.mark.parametrize("bits", [17, 31, 61])
def test_native_rate_really_exceeds_quarter_with_strict_decoding_margin(bits):
    row = module.native_budget(bits)
    n, s, k, w, r = row["length"], row["fold"], row["scalar_dimension"], row["radius"], row["order"]
    assert Q(1, 4) < Q(k, s*n) <= Q(3, 8)
    assert Q(1, 2) < Q(w, n) < Q(r, r+1)*(1-Q(k, n*(s-r+1)))
    assert (n-w)*(s-r+1) > row["interpolation_degree"]+k-1
    assert row["padding_used"] == 8
    assert row["native_success_per_attempt_lower"] > Q(1, 64)
    assert row["eta_power_of_two_upper_exponent"] < -256
    assert row["eta_outward_rounded_upper"] == Q(1, 1 << 256)
    assert row["raw_value_register_bits"] == bits*s*n
    assert not row["complete_pruning_executed"] and not row["native_receiver_executed"]
    assert not row["worst_case_classical_hardness_established"]


def test_native_success_recomputes_exact_binomial_tail_and_paid_padding():
    row = module.native_budget(17)
    tail = Q(sum(comb(289, j) for j in range(148, 290)), 1 << 289)
    assert row["tail_exact"] == tail
    assert row["native_success_per_attempt_lower"] == (1-Q(1, 1 << 256))*(1-tail)**2/8
    assert row["fallback_padding"] > row["primitive_generator_padding"]
    assert row["complete_pruning_sequence_count"] == 289**7


def test_field_prime_certificate_cannot_be_assumed_for_arbitrary_exponent():
    for n in (2, 3, 5, 7, 13, 17, 19, 31, 61):
        assert module.mersenne_prime_certificate(n)
    for n in (4, 6, 11, 23, 29):
        assert not module.mersenne_prime_certificate(n)
    row = module.native_budget(29)
    assert not row["base_multiplicative_order_is_prime_certified"]
    assert row["padding_used"] == row["fallback_padding"]


@pytest.mark.parametrize("args", [
    (8, 2, 10, 5, 5, 1),  # root-count margin fails
    (4, 2, 8, 2, 1, 2),  # insufficient distinct nonzero points
    (8, 2, 10, 5, 1, 3),  # order exceeds folding
    (True, 67, 289, 1, 1, 8),
])
def test_invalid_parameters_are_not_silently_certified(args):
    with pytest.raises(ValueError):
        module.folded_parameters(*args)


def test_strict_literature_boundary_is_not_rounded_into_acceptance():
    # r1,s2,N4,K4 gives radius threshold1/4: w1 is EXACT equality.
    with pytest.raises(ValueError, match="strict"):
        module.folded_parameters(4, 2, 4, 4, 1, 1)


def test_weight_enumerator_keeps_scalar_remainders_and_positive_terms():
    q, s, n, k, beta = 8, 2, 3, 3, Q(1, 3)
    expected = (q**k-1)*beta**n + n*(1-beta)*beta**(n-1)*(q-1)
    exact = module.block_weight_enumerator(q, s, n, k, beta)
    assert exact == expected
    assert exact <= q**k*(beta+(1-beta)/q**s)**n
    assert module.block_weight_enumerator(q, s, n, k, 0) == 0
    assert module.block_weight_enumerator(q, s, n, k, 1) == q**k-1
    with pytest.raises(ValueError):
        module.block_weight_enumerator(7, s, n, k, beta)


def test_padding_does_not_exceed_the_public_message_space():
    row = module.folded_parameters(12, 200, 10, 1, 8, 100)
    assert row["fallback_padding"] <= 1 << 12


def test_finite_control_is_additive_not_extension_linear_and_catches_wrong_basis(report):
    controls = report["finite_controls"]
    assert len(controls) == 3
    for row in controls:
        assert row["trace_dual_native_annihilator_checked"]
        assert row["not_extension_field_linear"]
        assert row["wrong_basis_native_membership_disagreements"] > 0
        q = 1 << row["bits"]
        assert row["zero_block_nonzero_message_counts"] == [
            q**max(0, row["dimension"]-row["fold"]*t)-1 for t in range(row["length"]+1)]


def test_block_predicate_is_not_silent_folding_of_old_scalar_predicates(report):
    for row in report["finite_controls"]:
        assert Q(*row["one_block_zero_fourier_probability"]) == Q(1, 2)
        assert Q(*row["old_scalar_predicates_folded_zero_probability"]) == Q(1, 1 << row["fold"])
        assert row["one_block_zero_fourier_probability"] != row["old_scalar_predicates_folded_zero_probability"]
    assert not report["same_as_old_scalar_problem"]


def test_every_finite_target_and_rejected_projection_mass_is_included(report):
    assert sum(len(row["all_targets"]) for row in report["finite_controls"]) == 10
    saw_unpaid_norm_above_one = False
    for row in report["finite_controls"]:
        assert {tuple(c["targets"]) for c in row["all_targets"]} == set(product((0, 1), repeat=row["length"]))
        ball_mass = Q(sum(comb(row["length"], j) for j in range(row["radius"]+1)), 1 << row["length"])
        for c in row["all_targets"]:
            assert 0 <= Q(*c["native_success"]) <= Q(*c["herald"]) <= ball_mass
            assert Q(*c["herald"])+Q(*c["projected_rejection"]) == ball_mass
            assert c["reference_padding"] == (1 << row["bits"])**row["dimension"]
            saw_unpaid_norm_above_one |= Q(*c["full_native_norm"]) > 1
    assert saw_unpaid_norm_above_one


def test_mixed_targets_are_actually_solved_by_the_classical_subfield_attack(report):
    controls = report["even_fold_classical_controls"]
    assert len(controls) == 8
    mixed = [r for r in controls if sum(r["targets"]) == 1]
    assert len(mixed) == 3
    for row in mixed:
        assert row["status"] == "CLASSICAL_NATIVE_WITNESS"
        assert row["full_row_rank_guarantee"] and row["rank"] == 2
        assert row["syndrome"] == [0, 0]
        assert row["predicate_values"] == row["targets"]
        assert row["zero_subfield_trace_identity_verified"]
        assert any(row["solution"])
    assert any(r["status"] == "SUBFIELD_COMPLETION_INCONCLUSIVE" for r in controls)


def test_classical_accepted_completion_beats_uniform_rejection_in_exact_counts(report):
    for row in report["finite_controls"]:
        n, m = row["length"], (row["dimension"]+row["fold"]-1)//row["fold"]
        count = (1 << (row["bits"]*row["fold"]*n-row["bits"]*row["dimension"]))//(1 << (n-m))
        for target in row["all_targets"]:
            assert target["classical_completion_conditioned_codewords"] == count
            assert Q(*target["classical_completion_success_exact"]) == Q(*target["full_native_norm"])/(1 << m)
    for n in (17, 31, 61):
        row = module.native_budget(n)
        m = row["classical_accepted_completion_remaining_blocks"]
        assert m < row["length"]
        assert row["classical_accepted_completion_success_lower"] == (1-row["eta_outward_rounded_upper"])/(1 << m)
        assert row["classical_accepted_completion_success_lower"]*row["classical_accepted_completion_expected_attempts_upper"] == 1


def test_pruning_includes_ambiguous_messages_and_charges_rank_failures(report):
    row = report["complete_pruning_control"]
    assert row["complete_list_matches_independent_enumeration"]
    assert not row["field_enumeration_in_pruner"]
    assert row["exhaustive_reference_message_count"] == 512
    assert row["sequences_charged"] == 27
    assert len(row["results"]) >= 2
    assert row["failed_sequences"]["rank_unresolved"] > 0
    assert sum(c["successful_sequences"] for c in row["results"])+sum(row["failed_sequences"].values()) == 27
    for result in row["results"]:
        assert Q(result["successful_sequences"], 27) >= Q(*row["per_message_probability_floor"])


def test_small_reference_cannot_be_used_as_a_native_decoder():
    with pytest.raises(ValueError, match="cap"):
        module.finite_block_control(3, 2, 3, 2, 1)
    with pytest.raises(ValueError):
        module.finite_block_control(17, 67, 289, 7261, 147)
    with pytest.raises(ValueError):
        module._tower(True, 2)


def test_solve_distinguishes_field_zero_from_truthiness():
    context = module._tower(3, 2)[0]
    assert module._solve(context, [[context.zero()]], [context.one()], 1) is None
    result = module._solve(context, [[context.zero(), context.one()]], [context.one()], 2)
    assert result[1] == 1 and result[0][0] == 0 and result[0][1] == 1


def test_artifact_is_live_and_does_not_claim_integration_or_hardness(report):
    assert json.loads(module.REPORT.read_text()) == report
    assert report["not_a_new_decoder"] and not report["native_quantum_execution"]
    assert not report["classical_hardness"]
    for path, digest in report["source_hashes"].items():
        assert hashlib.sha256((module.ROOT/path).read_bytes()).hexdigest() == digest
