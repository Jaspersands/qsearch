from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement, product

import numpy as np
import pytest

from cyclotomic_rescaling_gate import reduce_element
from ternary_carry_packets import classical_polynomial, compile_packet
from ternary_schur_tensor import (
    NativeCubicTensor, disjoint_block_frame, evaluate_polynomial,
    public_polynomial, quadratic_source_ledger, random_labels, restricted_native_control, run_controls,
)


def third_difference(packet, base, directions):
    out = [0]*packet.secret_dimension
    for bits in product(range(2), repeat=3):
        point = tuple((base[j]+sum(b*d[j] for b, d in zip(bits, directions))) % 3 for j in range(packet.retained))
        out = [(x+(-1)**(3-sum(bits))*y) % 3 for x, y in zip(out, packet.residual(point))]
    return tuple(out)


def basis(h):
    return [tuple(int(i == j) for i in range(h)) for j in range(h)]


@pytest.mark.parametrize("seed", [48011, 48012, 48013])
def test_factored_weighted_schur_tensor_equals_native_mixed_differences(seed):
    packet = compile_packet(random_labels(2, 5, seed), 3)
    tensor = NativeCubicTensor.from_packet(packet)
    for indices in combinations_with_replacement(range(packet.retained), 3):
        directions = [basis(packet.retained)[i] for i in indices]
        expected = tensor.evaluate(*directions)
        for base in ((0,)*packet.retained, (1,)*packet.retained, (2,)*packet.retained):
            assert third_difference(packet, base, directions) == expected


def test_polarization_is_trilinear_for_general_directions_not_only_basis_controls():
    packet = compile_packet(random_labels(2, 5, 48011), 3)
    tensor = NativeCubicTensor.from_packet(packet)
    directions = list(product(range(3), repeat=packet.retained))
    for i in range(30):
        u, v, w = [directions[(i*multiplier+offset) % len(directions)] for multiplier, offset in ((5, 1), (7, 2), (11, 3))]
        assert tensor.evaluate(u, v, w) == third_difference(packet, (0,)*packet.retained, (u, v, w))
        assert tensor.evaluate(tuple(2*x % 3 for x in u), v, w) == tuple(2*x % 3 for x in tensor.evaluate(u, v, w))


def test_all_diagonal_polarizations_zero_does_not_admit_quadratic_state():
    packet = compile_packet(random_labels(2, 5, 48011), 3)
    tensor = NativeCubicTensor.from_packet(packet)
    assert all(not any(tensor.evaluate(v, v, v)) for v in product(range(3), repeat=packet.retained))
    admission = tensor.restriction(basis(packet.retained))
    assert admission["all_diagonal_triples_zero"]
    assert admission["mixed_cubic_witnesses"]
    assert not admission["classical_quadratic_restriction_admitted"]


@pytest.mark.parametrize("syndrome", [(0, 0), (1, 2), (2, 1)])
def test_tensor_has_exact_high_label_and_syndrome_invariance(syndrome):
    labels = random_labels(2, 5, 48011)
    reference = compile_packet(labels, 3)
    perturbed = [[reduce_element((y[0]-1, y[1]+1), 3) for y in row] for row in labels]
    changed = compile_packet(perturbed, 3, syndrome)
    assert list(NativeCubicTensor.from_packet(reference).entries()) == list(NativeCubicTensor.from_packet(changed).entries())


def test_sparse_public_polynomial_matches_entire_bounded_native_table_without_building_one():
    packet = compile_packet(random_labels(2, 5, 48011), 3, (1, 2))
    sparse = public_polynomial(packet)
    assert sparse["public_residual_evaluations"] == 2*packet.retained+packet.retained*(packet.retained-1)//2
    dense = classical_polynomial(packet)
    for l, row in enumerate(sparse["component_polynomials"]):
        assert {tuple(x["powers"]): x["coefficient"] for x in row} == {tuple(x["powers"]): x["coefficient"] for x in dense["component_polynomials"][l]["coefficients"]}
    for point in product(range(3), repeat=packet.retained):
        assert evaluate_polynomial(sparse, point) == packet.residual(point)
    assert not sparse["dense_3_to_h_phase_table_built"]
    assert not sparse["unknown_weighted_phase_oracle_supplied"]


def test_growing_width_representation_evaluates_beyond_dense_interpolation_cap():
    packet = compile_packet(random_labels(4, 20, 48021), 3)
    with pytest.raises(ValueError, match="dense interpolation"):
        classical_polynomial(packet)
    sparse = public_polynomial(packet)
    assert packet.retained == 16
    assert sparse["public_residual_evaluations"] == 152
    for i in range(10):
        point = tuple((j*j+i*j+i) % 3 for j in range(packet.retained))
        assert evaluate_polynomial(sparse, point) == packet.residual(point)


@pytest.mark.parametrize("n,m", [(1, 6), (2, 9), (4, 20)])
def test_disjoint_block_cancellation_is_admitted_but_not_constant_fraction_decoder(n, m):
    packet = compile_packet(random_labels(n, m, 48031), 3)
    tensor = NativeCubicTensor.from_packet(packet)
    frame = disjoint_block_frame(packet)
    record = tensor.restriction(frame)
    assert len(frame) == m//(n+1)
    assert record["classical_quadratic_restriction_admitted"]
    columns = record["physical_frame_columns"]
    assert all(not any(a and b for a, b in zip(columns[i], columns[j])) for i in range(len(columns)) for j in range(i+1, len(columns)))
    assert not record["quadratic_restriction_is_secret_decoder"]
    assert not record["higher_level_transfer_admitted"]


@pytest.mark.parametrize("seed", [48031, 48032])
def test_physical_disjoint_instrument_retains_all_native_branches_and_source_cost(seed):
    record = restricted_native_control(random_labels(1, 6, seed), [8])
    assert record["native_qutrits_consumed"] == 6 and record["retained_quadratic_qutrits"] == 3
    assert record["all_native_words_replayed"] == 729
    assert record["all_native_branch_probabilities_sum"] == pytest.approx(1)
    branches = record["all_initial_and_complement_outcomes"]
    assert len(branches) == 27
    for branch in branches:
        amplitudes = np.array([complex(*x) for x in branch["all_unnormalized_native_amplitudes"]])
        assert np.vdot(amplitudes, amplitudes).real == pytest.approx(1/27)
        expected = np.array([np.exp(2j*np.pi*(8*(branch["public_component_frequency_base_mod9"][0]+3*row[0]) % 9)/9)/27
                             for row in branch["public_divided_residual_table_mod3"]])
        assert max(abs(amplitudes-expected)) < 4e-12
        assert all(row["degree"] <= 2 for row in branch["quadratic_component_polynomials"])
    assert not record["original_even_source_acquisition_charged"]
    assert not record["full_secret_top_digit_recovered"]


def test_top_digit_changes_only_measured_branch_global_phase_not_output_state():
    labels = random_labels(1, 6, 48031)
    low, high = (restricted_native_control(labels, [s]) for s in (2, 8))
    for a, b in zip(low["all_initial_and_complement_outcomes"], high["all_initial_and_complement_outcomes"]):
        assert a["measured_initial_and_complement_syndrome"] == b["measured_initial_and_complement_syndrome"]
        first, second = (np.array([complex(*x) for x in row["all_unnormalized_native_amplitudes"]]) for row in (a, b))
        assert abs(np.vdot(first, second))/np.linalg.norm(first)/np.linalg.norm(second) == pytest.approx(1)


def test_source_scope_and_independence_are_checked_before_admission():
    packet = compile_packet(random_labels(2, 5, 48011), 3)
    tensor = NativeCubicTensor.from_packet(packet)
    with pytest.raises(ValueError, match="independent"):
        tensor.restriction([basis(packet.retained)[0]]*2)
    with pytest.raises(ValueError, match="canonical"):
        tensor.evaluate([True]*packet.retained, basis(packet.retained)[0], basis(packet.retained)[0])
    with pytest.raises(ValueError, match="level3"):
        NativeCubicTensor.from_packet(compile_packet(random_labels(2, 5, 48011), 5))


def test_report_keeps_all_algorithmic_claims_closed():
    assert not any(run_controls()["claim_gate"].values())


def test_disjoint_quadratic_source_is_iid_but_public_rotation_exposes_correlation():
    packet = compile_packet([[(1, 0)]]*4, 3)
    frame = disjoint_block_frame(packet)
    block = quadratic_source_ledger(packet, frame)
    rotated = tuple(tuple((a+sign*b) % 3 for a, b in zip(*frame)) for sign in (1, -1))
    mixed = quadratic_source_ledger(packet, rotated)
    assert (block["square_Schur_rank"], block["offdiagonal_Schur_rank"]) == (2, 0)
    assert block["conditional_product_qutrit_labels_IID_uniform"]
    assert (mixed["square_Schur_rank"], mixed["offdiagonal_Schur_rank"]) == (2, 1)
    assert not mixed["conditional_product_qutrit_labels_IID_uniform"]
    probability = mixed["all_component_cross_terms_cancel_probability"]
    assert Fraction(int(probability["numerator"]), int(probability["denominator"])) == Fraction(1, 3)
    assert not mixed["arbitrary_public_Clifford_or_basis_changes_excluded"]
    assert not mixed["correlated_quadratic_outputs_useless"]


@pytest.mark.parametrize("rotated", [False, True])
def test_exact_high_label_source_enumeration_matches_schur_entropy_and_filter_cost(rotated):
    packet = compile_packet([[(1, 0)]]*4, 3)
    frame = disjoint_block_frame(packet)
    if rotated:
        frame = tuple(tuple((a+sign*b) % 3 for a, b in zip(*frame)) for sign in (1, -1))
    law = quadratic_source_ledger(packet, frame)
    W = law["physical_frame_columns"]
    diagonal = Counter()
    accepted = 0
    # Native C1=1+3b and C2=2*C1+3d give independent uniform high b,d.
    for high_d in product(range(3), repeat=4):
        def residual(z):
            word = tuple(sum(w[i]*a for w, a in zip(W, z)) % 3 for i in range(4))
            total = sum((0 if j == 0 else 1 if j == 1 else 2+3*high_d[i]) for i, j in enumerate(word)) % 9
            assert total % 3 == 0
            return total//3
        first = [residual(z) for z in ((1, 0), (0, 1))]
        second = [residual(z) for z in ((2, 0), (0, 2))]
        cross = (residual((1, 1))-sum(first)) % 3
        if not cross:
            accepted += 1
            diagonal[tuple((2*x-y) % 3 for x, y in zip(first, second))] += 1
    assert Fraction(accepted, 81) == (Fraction(1, 3) if rotated else Fraction(1))
    assert len(diagonal) == 3**law["conditional_diagonal_label_entropy_per_component_trits"]
    assert len(set(diagonal.values())) == 1
    linear = Counter(tuple(sum(b*w[i] for i, b in enumerate(high_b)) % 3 for w in W) for high_b in product(range(3), repeat=4))
    assert len(linear) == 9 and len(set(linear.values())) == 1


def test_nonquadratic_frame_is_rejected_before_source_rank_argument():
    packet = compile_packet(random_labels(2, 5, 48011), 3)
    with pytest.raises(ValueError, match="quadratic restriction"):
        quadratic_source_ledger(packet, basis(packet.retained))
