from itertools import product
import json
import math
import random

import numpy as np
import pytest

from cyclotomic_rescaling_gate import ideal_chart, plus, reduce_element, residue
from ternary_carry_packets import (
    classical_polynomial, compile_packet, cubic_signature, matched_cubic_sum,
    physical_control, run_controls,
)


@pytest.fixture(scope="module")
def report():
    return run_controls()


def labels(seed=46011, level=3, m=5, n=2):
    rng = random.Random(seed)
    h0, _, h1 = ideal_chart(level)[0]
    return [[(rng.randrange(h0), rng.randrange(h1)) for _ in range(n)] for _ in range(m)]


def test_public_kernel_compiler_is_invertible_on_every_basis_state():
    p = compile_packet(labels())
    targets = set()
    for old in product(range(3), repeat=p.consumed):
        target = list(old)
        for row, pivot in zip(p.reduced_rows, p.pivots):
            target[pivot] = (old[pivot]+sum(row[f]*old[f] for f in p.free)) % 3
        targets.add(tuple(target))
        recovered = list(target)
        for row, pivot in zip(p.reduced_rows, p.pivots):
            recovered[pivot] = (target[pivot]-sum(row[f]*target[f] for f in p.free)) % 3
        assert tuple(recovered) == old
        child = compile_packet(p.labels, 3, tuple(target[pivot] for pivot in p.pivots))
        assert child.assignment(tuple(target[f] for f in p.free)) == old
    assert len(targets) == 3**p.consumed


@pytest.mark.parametrize("level", [3, 5, 7])
def test_actual_phase_frequency_division_and_top_secret_digit_loss(level):
    p = compile_packet(labels(level=level))
    q = p.phase_modulus
    base = p.component_frequencies(p.assignment((0,)*p.retained))
    for z in product(range(3), repeat=p.retained):
        residual = p.residual(z)
        frequency = p.component_frequencies(p.assignment(z))
        assert all((f-b) % q == 3*c for f, b, c in zip(frequency, base, residual))
        for s in (1, 2, q//3+1):
            assert sum(s*c for c in residual) % (q//3) == sum((s+q//3)*c for c in residual) % (q//3)
    assert not p.resource_record()["higher_secret_digit_retained_in_this_output"]


def evaluate(polynomials, z):
    return tuple(sum(c["coefficient"]*math.prod(x**e for x, e in zip(z, c["powers"]))
                     for c in row["coefficients"]) % 3 for row in polynomials)


def test_exact_cubic_interpolation_is_not_a_stabilizer_or_iid_shortcut(report):
    rows = [c for c in report["native_controls"] if c["resources"]["parent_level"] == 3]
    assert len(rows) == 3
    for row in rows:
        for branch in row["all_syndrome_branches"]:
            p = compile_packet(row["native_labels"], 3, branch["syndrome"])
            poly = branch["classical_cubic_polynomial"]
            assert poly["maximum_total_degree"] == 3
            for z in product(range(3), repeat=p.retained):
                assert evaluate(poly["component_polynomials"], z) == p.residual(z)
            assert not poly["quadratic_stabilizer_learning_automatically_applies"]
            assert not poly["identical_unknown_packet_copies_supplied"]
        assert min(b["first_retained_qutrit_purity"] for b in row["all_syndrome_branches"]) < .6
        purity = row["all_syndrome_branches"][0]["first_retained_qutrit_purity"]
        assert abs(purity-1/3) > .01 and abs(purity-1) > .01
        assert not row["resources"]["outputs_certified_as_IID_PSP_samples"]


def test_cubic_part_depends_only_on_low_labels_not_higher_digits_or_syndrome():
    original = compile_packet(labels())
    signature = cubic_signature(original)
    assert any(signature)
    lifts = [[plus(y, (-1, 1), 3) for y in row] for row in original.labels]
    assert [[residue(y) for y in row] for row in lifts] == [[residue(y) for y in row] for row in original.labels]
    full_polynomials = []
    for source in (original.labels, lifts):
        for syndrome in product(range(3), repeat=len(original.pivots)):
            p = compile_packet(source, 3, syndrome)
            assert cubic_signature(p) == signature
            full_polynomials.append(classical_polynomial(p))
    assert any(poly != full_polynomials[0] for poly in full_polynomials[1:])


def test_all_small_low_label_sources_have_at_most_cubic_degree():
    for low in product(range(3), repeat=3):
        source = [[(a, 0)] for a in low]
        p = compile_packet(source)
        for syndrome in product(range(3), repeat=len(p.pivots)):
            poly = classical_polynomial(compile_packet(source, 3, syndrome))
            assert poly["maximum_total_degree"] <= 3


def test_three_cubic_matched_distinct_packets_cancel_without_identical_state_promise():
    source = labels(m=4)
    packets = [compile_packet([[plus(y, (-k, k), 3) for y in row] for row in source], 3) for k in range(3)]
    assert len({p.labels for p in packets}) == 3
    assert all(cubic_signature(p) == cubic_signature(packets[0]) for p in packets)
    h = packets[0].retained
    zero = (0,)*h
    for shifts in product(list(product(range(3), repeat=h)), repeat=2):
        result = matched_cubic_sum(packets, [zero, *shifts])
        assert result["conditional_sum_degree"] <= 2
        for z, expected in zip(product(range(3), repeat=h), result["public_frequency_table"]):
            assert evaluate(result["component_polynomials"], z) == tuple(expected)
        assert not result["native_source_matching_supplied"]
        assert not result["quadratic_state_is_a_secret_decoder"]


def test_cubic_mismatch_is_rejected_instead_of_free_derivative_sampling():
    p = compile_packet(labels(46011))
    other = compile_packet(labels(46012))
    assert p.retained == other.retained
    assert cubic_signature(p) != cubic_signature(other)
    with pytest.raises(ValueError, match="tensors mismatch"):
        matched_cubic_sum([p, p, other], [(0,)*p.retained]*3)
    with pytest.raises(ValueError, match="no cloning"):
        matched_cubic_sum([p], [(0,)*p.retained])


def test_native_level3_frequency_has_fourth_additive_difference_zero():
    for y in [(a, b) for a in range(9) for b in range(3)]:
        packet = compile_packet([[y]])
        for j in range(3):
            for shifts in product((1, 2), repeat=4):
                value = 0
                for mask in range(16):
                    index = (j+sum(shifts[k] for k in range(4) if mask >> k & 1)) % 3
                    value += (-1)**mask.bit_count()*packet.component_frequencies((index,))[0]
                assert value % 9 == 0


def test_literal_source_and_syndrome_matching_costs_are_not_optimal_lower_bounds(report):
    row = report["literal_low_matrix_match_ledger"]
    assert row["second_and_third_IID_low_matrices_both_match_first_probability"] == {"base": 3, "exponent": -16}
    assert row["initial_zero_syndromes_for_three_packets_probability"] == {"base": 3, "exponent": -6}
    assert row["probabilities_are_conditioning_costs_not_optimal_matching_lower_bounds"]
    assert not row["more_general_public_tensor_alignment_excluded"]
    assert len(report["conditional_algebraic_sum_controls"]) == 9
    assert all(not c["full_three_packet_quantum_instrument_replayed"] for c in report["conditional_algebraic_sum_controls"])


def test_higher_levels_do_not_get_classical_cubic_learning_for_free(report):
    rows = [r for r in report["native_controls"] if r["resources"]["parent_level"] == 5]
    assert len(rows) == 3
    for row in rows:
        assert row["resources"]["retained_phase_modulus"] == 9
        assert all(b["classical_cubic_polynomial"] is None for b in row["all_syndrome_branches"])
    with pytest.raises(ValueError, match="only established"):
        classical_polynomial(compile_packet(labels(level=5), 5))
    counter = report["higher_level_fourth_difference_countercontrol"]
    assert counter["fourth_difference_by_secret_component"] == [3, 6]
    assert not counter["fixed_classical_cubic_receiver_transfer_allowed"]
    assert not counter["general_higher_level_receiver_excluded"]


def test_all_native_syndromes_are_kept_with_correct_probability_and_norm(report):
    for row in report["native_controls"]:
        rank = row["resources"]["measured_qutrits"]
        assert len(row["all_syndrome_branches"]) == 3**rank
        assert sum(b["probability"] for b in row["all_syndrome_branches"]) == pytest.approx(1)
        assert row["physical_full_output_norm"] == pytest.approx(1)
        assert all(b["probability"] == pytest.approx(3**(-rank)) for b in row["all_syndrome_branches"])
        assert row["resources"]["retained_joint_qutrits"] == row["resources"]["input_native_qutrits"]-rank
        assert not row["constant_fraction_retained_registers_is_a_decoder"]
        assert not row["resources"]["acquiring_intermediate_odd_level_inputs_charged_here"]
    assert not any(report["claim_gate"].values())
    json.loads(json.dumps(report, allow_nan=False))


@pytest.mark.parametrize("source,level,syndrome", [([], 3, None), ([[]], 3, None),
    ([[(1, 0)]], 2, None), ([[(1, 0)]], 3, [3]), ([[(1, 0)]], 3, [True]),
    ([[(1, .5)]], 3, None)])
def test_malformed_native_packets_rejected(source, level, syndrome):
    with pytest.raises(ValueError):
        compile_packet(source, level, syndrome)
