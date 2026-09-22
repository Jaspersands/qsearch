from fractions import Fraction
from itertools import permutations, product
from math import comb

import pytest

from dcp_balanced_pairing import (
    BalancedPairingProgram, balanced_certificate, balanced_program_control,
    balanced_program_from_seed, block_masks, build_balanced_pairing_audit,
    comparator_schedule, exact_balanced_source_control, sort_records, unsort_records,
)
from dcp_pairing_programs import evaluate_mutual_program


def test_network_is_fixed_sorts_duplicates_and_uncomputes_every_flag():
    for values in product(range(3), repeat=4):
        original = [(x, i % 2, i) for i, x in enumerate(values)]
        records = original.copy()
        flags = sort_records(records)
        assert records == sorted(original)
        assert len(flags) == 6
        assert unsort_records(records, flags) == 6
        assert records == original and flags == []
    for size in (2, 4, 8, 16, 32):
        forward = list(comparator_schedule(size))
        assert forward[::-1] == list(comparator_schedule(size, reverse=True))
        q = size.bit_length()-1
        assert len(forward) == size*q*(q+1)//4
    # Zero-one principle check across all 8-wire Boolean inputs.
    for values in product(range(2), repeat=8):
        records = [(x, 0, 0) for x in values]
        sort_records(records)
        assert records == sorted(records)


def test_sort_without_history_is_not_a_reversible_primitive():
    inputs = list(permutations([(0, 0, 1), (1, 0, 2)]))
    outputs, with_history = set(), set()
    for initial in inputs:
        records = list(initial)
        flags = sort_records(records)
        outputs.add(tuple(records))
        with_history.add((tuple(records), tuple(flags)))
    assert len(outputs) == 1 and len(with_history) == 2


@pytest.mark.parametrize("args", [(2, 2, 1), (3, 4, 1), (2, 4, 1, 1)])
def test_balanced_family_has_the_claimed_natural_source_moments_and_coverage(args):
    row = exact_balanced_source_control(*args)
    assert all(row["checks"].values())
    assert row["observed_mass"] >= row["source_mass_lower"] > 0


@pytest.mark.parametrize("program", [
    BalancedPairingProgram((1, 0, 1, 0), 2, 1, (), 0),
    BalancedPairingProgram((1, 1, 1, 1), 2, 1, (), 0),
    BalancedPairingProgram((1, 2, 3, 4), 3, 1, (3, 6), 1),
    BalancedPairingProgram((1, 2, 3, 4), 3, 1, (0,), 1),
])
def test_join_equals_independent_graph_and_composes_with_physical_readout(program):
    row = balanced_program_control(program)
    assert row["failures"] == 0
    physical = evaluate_mutual_program(program.labels, 1 << program.n, row["proposal_table"])
    assert all(physical["physical_checks"].values())
    assert physical["maximum_residual"] < 1e-12
    assert physical["profile"]["heralded_success_fraction"] == float(row["accepted_source_mass"])


def test_larger_weight_join_matches_graph_without_building_full_physical_workspace():
    program = BalancedPairingProgram((1, 2, 3, 4, 5, 6), 3, 2, (3, 6), 0)
    assert balanced_program_control(program)["failures"] == 0


def test_capped_lists_have_constant_coverage_without_full_block_enumeration():
    program = BalancedPairingProgram((1, 2, 3, 0, 1, 2), 2, 1, (3, 6), 0)
    assert program.list_length == 2 < comb(3, 1)
    assert balanced_program_control(program)["failures"] == 0
    row = balanced_certificate(8, 64)
    assert row["each_list_length"] == 16 < row["available_block_supports"] == 32
    assert row["supports"] == 1 << 8
    assert row["source_mass_lower"] == Fraction(257, 8192)
    full = balanced_certificate(8, 64, 1, 32)
    assert full["source_mass_lower"] < row["source_mass_lower"]
    assert full["persistent_workspace_bits"] > row["persistent_workspace_bits"]


def test_xor_evaluator_is_a_clean_permutation_on_arbitrary_output_registers():
    program = BalancedPairingProgram((1, 0, 1, 0), 2, 1, (3,), 0)
    for b in range(16):
        values = set()
        proposal = program.propose(b)
        for output in range(32):
            row = program.evaluate_xor(b, output)
            assert row["workspace_clean"]
            assert row["output"] == output ^ (0 if proposal is None else 16 | proposal)
            assert program.evaluate_xor(b, row["output"])["output"] == output
            values.add(row["output"])
        assert values == set(range(32))


def test_colliding_keys_keep_full_multiplicity_not_one_witness_per_bucket():
    program = BalancedPairingProgram((1, 1, 1, 1), 2, 1, (), 0)
    row = program.evaluate_xor(0)
    assert row["neighbor_count_before_source_mark"] == 4
    assert row["support_xor_before_source_mark"] == 0
    assert program.propose(0) is None  # A deduplicating dictionary would falsely see uniqueness.


def test_balanced_supports_are_not_silently_the_entire_radius_ball():
    program = BalancedPairingProgram((1, 1, 0, 0), 2, 1, (), 0)
    # Flipping the first two bits is a half-period move, but both are in one block.
    assert sum(program.labels[:2]) % 4 == 2
    assert program.evaluate_xor(0)["neighbor_count_before_source_mark"] == 0
    assert balanced_certificate(2, 4, 1)["supports"] == 4 < sum(comb(4, w) for w in (1, 2))


def test_syndrome_equality_does_not_remove_source_mark_condition():
    program = BalancedPairingProgram((1, 0, 1, 0), 2, 1, (0,), 1)
    row = program.evaluate_xor(0)
    assert row["neighbor_count_before_source_mark"] == 1
    assert row["output"] == 0 and program.propose(0) is None


def test_exhaustive_small_labels_with_nontrivial_syndromes():
    for labels in product(range(4), repeat=4):
        assert balanced_program_control(BalancedPairingProgram(labels, 2, 1, (5, 10), 1))["failures"] == 0


def test_seed_factory_is_unrestricted_and_input_lists_cannot_change_the_program():
    programs = [balanced_program_from_seed((1, 2, 3, 4), 3, seed, 1) for seed in range(32)]
    assert {(p.hash_rows, p.hash_offset) for p in programs} == {((row,), offset) for row in range(16) for offset in (0, 1)}
    labels, rows = [1, 0, 1, 0], [0]
    program = BalancedPairingProgram(labels, 2, 1, rows, 0)
    labels[0], rows[0] = 0, 1
    assert program.labels == (1, 0, 1, 0) and program.hash_rows == (0,)


def test_actual_operation_counts_include_inverse_and_padding():
    program = BalancedPairingProgram((1, 2, 3, 4, 5, 6), 3, 1, (1, 2), 0)
    resource = balanced_certificate(3, 6, 1)
    assert resource["padded_records"] == 8 > 2*resource["each_list_length"]
    row = program.evaluate_xor(0)
    assert row["record_evaluations"] == resource["one_xor_record_evaluations"]
    assert row["comparators"] == resource["one_xor_comparators"]
    assert row["scan_steps"] == resource["one_xor_scan_steps"]
    # Resource certificate uses 3 hash bits here; the actual program uses 2.
    assert row["persistent_workspace_bits"] == resource["persistent_workspace_bits"]-(2*8+1)


def test_polynomial_coverage_does_not_make_the_list_time_or_space_polynomial():
    for n in (8, 9, 16, 31, 64, 128, 256, 512):
        row = balanced_certificate(n, 2*((n*n+1)//2))
        half, k = row["half_width"], row["per_block_weight"]
        assert comb(half, k-1)**2 < 1 << n <= row["supports"]
        assert 1 <= row["mean_degree"] < half**2
        assert row["source_mass_lower"] >= Fraction(1, 128*half**2)
        assert row["source_mass_lower"] >= Fraction(1, 128)
        assert row["hash_bits"] in (2, 3)
        assert row["available_block_supports"] >= row["each_list_length"]
        assert row["radius"] <= n//2
        assert row["joint_fault_signal_lower"] >= row["source_mass_lower"]/2
        assert row["each_list_length"]**2 >= 1 << n
        assert row["persistent_workspace_bits"] > 2*row["each_list_length"]
        assert row["coherent_ram_assumed"] is False
        assert row["polynomial_time_claimed"] is False
        assert Fraction(1, 8) < row["post_mark_expected_degree"] <= Fraction(1, 4)
        assert 4 <= row["syndrome_domain_over_supports"] < 8


def test_linear_sample_budget_already_gives_constant_scoped_noise_signal():
    for n in range(6, 129):
        row = balanced_certificate(n, 2*n)
        assert row["per_block_weight"] <= (n+3)//4
        assert row["radius"] <= Fraction(2*n, 3)
        assert row["source_mass_lower"] >= Fraction(1, 128)
        assert row["joint_fault_signal_lower"] >= Fraction(1, 384)
        assert row["each_list_length"]**2 >= 1 << n


@pytest.mark.parametrize("args", [(0, 4, 1), (3, 3, 1), (3, 4, True), (8, 4, None), (3, 4, 3)])
def test_invalid_or_unavailable_balanced_parameters_are_rejected(args):
    with pytest.raises(ValueError):
        balanced_certificate(*args)


def test_report_does_not_claim_classical_dcp_solution_or_quantum_speedup():
    row = build_balanced_pairing_audit()
    assert row["control_failures"] == 0
    assert len(row["program_controls"]) == 3
    for flag in ("classical_dcp_solver_constructed", "speedup_claim_allowed", "gate_export_implemented", "novelty_established"):
        assert row["contract"][flag] is False
