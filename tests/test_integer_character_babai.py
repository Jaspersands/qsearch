from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random

from flint import fmpz_mat
import pytest

from theorems import integer_character_babai as attack
from theorems import integer_character_near_vector as near
from theorems.native_rlwe_primal_babai import exact_row_profile, nearest_plane


@pytest.mark.parametrize("order,labels", [
    (18, [1, 5, 16]), (21, [1, 7, 3, 20]), (2*3**50, [1, 333, 17, 56, 13]),
])
def test_normalized_elimination_matches_independent_bareiss_and_babai(order, labels):
    _, basis = near.lattice_bases(labels, order)
    rows = [[int(v) for v in row] for row in fmpz_mat(basis).lll().tolist()]
    target = [random.Random(1700+i).randrange(order) for i in range(len(labels))]
    reference = exact_row_profile(rows)
    reference_babai = nearest_plane(rows, target, reference)
    actual = attack.exact_normalized_babai(rows, labels, order, target)
    assert actual["point"] == reference_babai["point"]
    assert actual["basis_coefficients"] == reference_babai["basis_coefficients"]
    assert actual["normalized_gram_pivots"] == [
        d//order**(2*k) for k, d in enumerate(reference["leading_gram_determinants"])]
    trace = sum(reference["gs_squared"], Q(0))/(order*order)
    assert actual["normalized_gs_trace_lower"] <= trace <= actual["normalized_gs_trace_upper"]
    assert actual["all_target_mean_square_upper"] >= trace/(4*len(labels))


def test_exact_ties_and_one_dimensional_case():
    result = attack.exact_normalized_babai([[1]], [1], 18, [7])
    assert result["point"] == [7]
    assert result["mean_square"] == 0
    assert result["all_target_mean_square_upper"] >= Q(1, 4*18**2)
    for sign, expected in [(1, [7, 18]), (-1, [7, 0])]:
        result = attack.exact_normalized_babai(
            [[1, 0], [0, 18]], [1, 0], 18, [7, sign*9])
        assert result["point"] == expected
        assert result["mean_square"] == Q(1, 8)


def test_exact_profile_does_not_assume_a_reduced_basis():
    labels, order = [1, 7, 3, 20], 21
    _, rows = near.lattice_bases(labels, order)
    rows[0] = [x+10**30*y for x, y in zip(rows[0], rows[-1])]
    rows[1], rows[2] = rows[2], rows[1]
    rows[-1] = [-x for x in rows[-1]]
    target = [-31, 42, -200, 107]
    reference = exact_row_profile(rows)
    expected = nearest_plane(rows, target, reference)
    actual = attack.exact_normalized_babai(rows, labels, order, target)
    assert actual["point"] == expected["point"]
    assert actual["basis_coefficients"] == expected["basis_coefficients"]
    shift = [2*x-3*y for x, y in zip(rows[0], rows[-1])]
    translated = attack.exact_normalized_babai(
        rows, labels, order, [t+s for t, s in zip(target, shift)])
    assert translated["point"] == [p+s for p, s in zip(actual["point"], shift)]
    assert translated["mean_square"] == actual["mean_square"]


def test_coordinate_elimination_retains_every_coordinate_and_full_index():
    labels, order = [1, 5, 3, 7], 21
    _, basis = near.lattice_bases(labels, order)
    transformed = [order if j == 0 else 0 for j in range(4)]
    inverse_generator = [(pow(5, -1, order)*a) % order for a in labels]
    for rows in [
        [[-v for v in basis[3]], basis[1], basis[0], basis[2]],
        [transformed, [-v for v in basis[3]], inverse_generator, basis[2]],
    ]:
        target = [-37, 42, 73, 10]
        reference = exact_row_profile(rows)
        actual = attack.exact_normalized_babai(rows, labels, order, target)
        expected = nearest_plane(rows, target, reference)
        assert actual["orthogonal_integer_prefix_rank"] == 2
        assert actual["exact_core_dimension"] == 2
        assert actual["point"] == expected["point"]
        assert actual["basis_coefficients"] == expected["basis_coefficients"]
        assert actual["normalized_gram_pivots"] == [
            d//order**(2*k) for k, d in enumerate(reference["leading_gram_determinants"])]
    with pytest.raises(ValueError, match="index"):
        attack.exact_normalized_babai([[order, 0], [0, order]], [1, 5], order, [1, 2])


def test_sub_lattice_and_nonmember_basis_are_rejected():
    labels, order = [1, 5, 16], 18
    _, basis = near.lattice_bases(labels, order)
    basis[1] = [2*x for x in basis[1]]
    with pytest.raises(ValueError, match="index"):
        attack.exact_normalized_babai(basis, labels, order, [1, 2, 3])
    _, basis = near.lattice_bases(labels, order)
    basis[1][2] += 1
    with pytest.raises(ValueError, match="not in"):
        attack.exact_normalized_babai(basis, labels, order, [1, 2, 3])


def test_basis_serialization_is_deterministic_and_exact(tmp_path):
    rows = [[2**1200, -3**701], [0, 7]]
    path = tmp_path/"basis.json.gz"
    first = attack.write_basis(path, rows)
    assert attack.read_basis(path) == rows
    assert attack.write_basis(path, rows) == first
    assert not path.with_suffix(".gz.tmp").exists()


def test_bounded_last_plane_search_matches_independent_fraction_rounding():
    labels, order = [1, 5, 3, 7], 21
    _, basis = near.lattice_bases(labels, order)
    rows = [basis[3], basis[1], basis[0], basis[2]]
    target = [3, 18, 5, 15]
    exact = attack.exact_normalized_babai(rows, labels, order, target)
    search = attack.bounded_last_plane_search(rows, labels, order, target, exact, radius=3)
    reference = exact_row_profile(rows)
    mu, gs = reference["mu"], reference["gs_squared"]
    inner = []
    for i, row in enumerate(rows):
        inner.append(sum(a*b for a, b in zip(row, target))
                     - sum(mu[i][j]*inner[j] for j in range(i)))
    for trial in search["trials"]:
        coordinates = [value/length for value, length in zip(inner, gs)]
        coefficients = [0]*len(rows)
        for i in range(len(rows)-1, -1, -1):
            value = coordinates[i]
            coefficients[i] = (2*value.numerator+value.denominator)//(2*value.denominator)
            if i == len(rows)-1:
                coefficients[i] += trial["offset"]
            for j in range(i):
                coordinates[j] -= coefficients[i]*mu[i][j]
        point = [sum(c*row[j] for c, row in zip(coefficients, rows)) for j in range(len(rows))]
        assignment = near.recover_assignment(labels, order, point)
        assert str(assignment) == trial["assignment_decimal"]
        assert str(near.witness(labels, target, order, assignment)["mean_square"]) == trial["mean_square"]
    assert search["trials_evaluated"] == 7
    assert Q(search["best"]["mean_square"]) == min(Q(t["mean_square"]) for t in search["trials"])
    assert not search["independent_samples_assumed"]
    assert not search["asymptotic_dequantization_claimed"]
    with pytest.raises(ValueError, match="radius"):
        attack.bounded_last_plane_search(rows, labels, order, target, exact, radius=-1)


def test_native_exact_full_dimensional_witness_replay():
    saved = json.loads(attack.REPORT.read_text())
    assert saved["producer_sha256"] == hashlib.sha256(Path(attack.__file__).read_bytes()).hexdigest()
    source_bytes = near.REPORT.read_bytes()
    assert saved["input_artifact_sha256"] == hashlib.sha256(source_bytes).hexdigest()
    native = json.loads(source_bytes)["native"]
    labels = list(map(int, native["public_labels_decimal"]))
    centers = list(map(int, native["centers_decimal"]))
    order = int(native["cyclic_order_decimal"])
    basis_path = attack.ROOT/saved["basis_artifact"]
    assert hashlib.sha256(basis_path.read_bytes()).hexdigest() == saved["basis_artifact_sha256"]
    provenance = attack.ROOT/saved["basis_provenance_artifact"]
    assert hashlib.sha256(provenance.read_bytes()).hexdigest() == saved["basis_provenance_sha256"]
    assert json.loads(provenance.read_text())["basis_artifact_sha256"] == saved["basis_artifact_sha256"]
    rows = attack.read_basis(basis_path)
    assert len(rows) == len(labels) == 1024
    for row in rows:
        near.recover_assignment(labels, order, row)
    pivots = list(map(int, saved["exact_arithmetic"]["normalized_gram_pivots_decimal"]))
    assert len(pivots) == len(rows) and all(p > 0 for p in pivots)
    assert pivots[-1] == 1
    prefix_rank = saved["exact_arithmetic"]["orthogonal_integer_prefix_rank"]
    assert prefix_rank+saved["exact_arithmetic"]["schur_steps"] == len(rows)
    assert pivots[:prefix_rank] == [order*order]*prefix_rank
    occupied = set()
    for row in rows[:prefix_rank]:
        support = [j for j, value in enumerate(row) if value]
        assert len(support) == 1 and abs(row[support[0]]) == order
        assert support[0] not in occupied
        occupied.add(support[0])
    columns = [j for j in range(len(labels)) if j not in occupied]
    core_prefix = exact_row_profile(
        [[row[j] for j in columns] for row in rows[prefix_rank:prefix_rank+8]])
    assert pivots[prefix_rank:prefix_rank+8] == [
        d//order**(2*k) for k, d in enumerate(core_prefix["leading_gram_determinants"])]
    prefix = exact_row_profile(rows[:8])
    assert pivots[:8] == [
        d//order**(2*k) for k, d in enumerate(prefix["leading_gram_determinants"])]
    precision = saved["exact_arithmetic"]["dyadic_precision"]
    lower_units = upper_units = 0
    for p, denominator in zip(pivots, [order*order]+pivots[:-1]):
        term = Q(p*2**precision, denominator)
        floor = term.numerator//term.denominator
        lower_units += floor
        upper_units += floor+(term.denominator != 1)
    trace = [Q(lower_units, 2**precision), Q(upper_units, 2**precision)]
    assert list(map(Q, saved["normalized_gs_trace_interval"])) == trace
    bound = trace[1]/(4*len(rows))
    assert Q(saved["all_target_mean_square_upper"]) == bound
    assert saved["all_targets_meet_quantum_grid_threshold"] == (bound <= near.GRID_THRESHOLD)
    assert list(map(Q, saved["continuous_haar_mean_square_interval"])) == [
        t/(12*len(rows)) for t in trace]
    coefficients = list(map(int, saved["basis_coefficients_decimal"]))
    assert len(coefficients) == len(rows)
    point = [sum(c*row[j] for c, row in zip(coefficients, rows)) for j in range(len(labels))]
    assert point == list(map(int, saved["babai_point_decimal"]))
    squared = Q(sum((c-v)**2 for c, v in zip(centers, point)), len(rows)*order*order)
    assert squared == Q(saved["babai_mean_square"]) <= bound
    assignment = near.recover_assignment(labels, order, point)
    assert str(assignment) == saved["assignment_decimal"]
    replay = near.witness(labels, centers, order, assignment)
    assert str(replay["mean_square"]) == saved["coordinate_centered_mean_square"]
    assert replay["accepted"] == saved["native_threshold_met"]
    assert not saved["classical_asymptotic_dequantization_proved"]
    assert not saved["failed_basis_proves_classical_hardness"]
    search = saved["bounded_last_plane_search"]
    assert search["predeclared_radius"] == 32
    assert search["trials_evaluated"] == len(search["trials"]) == 65
    for trial in search["trials"]:
        replay = near.witness(labels, centers, order, int(trial["assignment_decimal"]))
        assert str(replay["mean_square"]) == trial["mean_square"]
        assert replay["accepted"] == trial["threshold_met"]
    best = search["best"]
    assert Q(best["mean_square"]) == min(Q(t["mean_square"]) for t in search["trials"])
    assert best["threshold_met"] and Q(best["mean_square"]) < Q(63, 1000)
    assert best["offset"] == -17
    coefficients = list(map(int, best["basis_coefficients_decimal"]))
    point = [sum(c*row[j] for c, row in zip(coefficients, rows)) for j in range(len(labels))]
    assert point == list(map(int, best["point_decimal"]))
    assert str(near.recover_assignment(labels, order, point)) == best["assignment_decimal"]
    raw_square = Q(sum((c-v)**2 for c, v in zip(centers, point)), len(rows)*order*order)
    assert raw_square == Q(best["raw_mean_square"])
    last_squared = Q(pivots[-1], pivots[-2])
    assert Q(search["last_normalized_gs_squared"]) == last_squared
    assert raw_square <= bound+(best["offset"]**2+abs(best["offset"]))*last_squared/len(rows)
    assert not search["asymptotic_dequantization_claimed"]
