from fractions import Fraction
from itertools import product
import json
import math
import subprocess

import pytest

from ternary_covariant_noise import CovariantRecord, noise_probability
from ternary_native_cvp_reduction import (
    REPORT, bounded_source_controls, check_point, compile_cvp_instance, expected_costs,
    reduction_ledger, small_exact_reference, squared_residual_cost, wrong_residual_character,
)


def honest():
    secret, q = (2, 4), 9
    rows = (((1, 0), (0, 1)), ((1, 1), (2, 1)), ((3, 4), (4, 5)))
    return tuple(CovariantRecord(a, c, tuple(sum(x*s for x, s in zip(v, secret)) % q for v in (a, c)), q)
                 for a, c in rows), secret


@pytest.mark.parametrize("q", (3, 9, 27, 81))
def test_true_cost_and_finite_dirichlet_second_moment_agree_with_born_law(q):
    h = (q-1)//2
    moment = sum(x*x*math.cos(2*math.pi*x/q) for x in range(-h, h+1))/q
    exact_formula = -math.cos(math.pi/q)/(2*math.sin(math.pi/q)**2)
    assert moment == pytest.approx(exact_formula, abs=2e-12)
    direct = sum(noise_probability(q, a, c)*sum(((x+h) % q-h)**2 for x in (a, c))
                 for a, c in product(range(q), repeat=2))
    table = expected_costs(q)
    assert direct == pytest.approx(table["true_pair_cost_diagnostic"], abs=2e-11)
    gap = float(Fraction(table["uniform_pair_cost"]))-direct
    assert gap/q**2 >= 4/81-1e-14


@pytest.mark.parametrize("q", (3, 9, 27))
def test_every_nonprimitive_or_primitive_wrong_secret_has_uniform_joint_residual_law(q):
    for difference in range(1, q):
        for f in product(range(q), repeat=2):
            assert wrong_residual_character(q, (0, difference), f) == Fraction(int(f == (0, 0)))
    assert wrong_residual_character(q, (0, 0), (1, 0)) == Fraction(1, 3)


def test_uniform_noise_convolution_in_actual_ring_not_just_fourier_assertion():
    q, difference = 9, 3
    for a, c in product(range(q), repeat=2):
        averaged = sum(noise_probability(q, (a-difference*u) % q, (c-difference*v) % q)
                       for u, v in product(range(q), repeat=2))/q**2
        assert averaged == pytest.approx(1/q**2, abs=2e-16)


@pytest.mark.parametrize("n,r", ((1, 1), (4, 8), (64, 128)))
def test_budget_constants_and_norm_factor_are_not_confused(n, r):
    ledger = reduction_ledger(n, r, 16)
    assert ledger["original_measured_qutrits"] == 2048*(2*n*r+17)
    assert ledger["full_Euclidean_lattice_dimension"] == 2*ledger["original_measured_qutrits"]
    assert Fraction(9, 8)**2 < Fraction(1647, 1297)
    assert ledger["ideal_failure_probability_upper"] == "1/65536"
    assert not ledger["approximate_CVP_solver_supplied"] and not ledger["large_lattice_materialized"]
    assert not ledger["wrong_secret_difference_must_be_primitive"]
    assert not ledger["polynomial_original_copy_budget_proves_polynomial_time"]


def test_noise_trace_error_is_joint_and_additive_not_free_per_copy_error():
    ledger = reduction_ledger(2, 2, 8, Fraction(1, 10))
    assert Fraction(ledger["complete_failure_probability_upper"]) == Fraction(1, 256)+Fraction(1, 10)
    assert reduction_ledger(2, 2, 8, Fraction(1))["complete_failure_probability_upper"] == "1"
    with pytest.raises(ValueError):
        reduction_ledger(2, 2, 8, .1)


def test_actual_euclidean_cvp_instance_and_public_point_check():
    records, secret = honest()
    instance = compile_cvp_instance(records)
    assert instance["Euclidean_lattice_rows"] == instance["source_lattice"]["lattice_rows"]
    assert len(instance["Euclidean_lattice_rows"][0]) == 2*len(records)
    result = check_point(records, instance, instance["target"])
    assert result["candidate"] == secret and result["supplied_squared_distance"] == 0
    assert result["below_public_absolute_radius_threshold"]
    assert result["confidence_bits_supported_by_sample_count"] == 0
    assert not result["nearest_point_or_approximation_factor_certified"]
    assert not result["implemented_solver_or_speedup"]


def test_wrapping_a_code_point_keeps_candidate_but_changes_ordinary_distance():
    records, secret = honest()
    instance = compile_cvp_instance(records)
    point = tuple(x+9 for x in instance["target"])
    result = check_point(records, instance, point)
    assert result["candidate"] == secret
    assert result["supplied_squared_distance"] == 6*81
    assert result["nearest_representative_in_same_secret_coset_squared_distance"] == 0


def test_tampered_instance_and_invalid_lattice_point_rejected():
    records, _ = honest()
    instance = compile_cvp_instance(records)
    changed = {**instance, "target": (0,)*6}
    with pytest.raises(ValueError, match="actual source"):
        check_point(records, changed, instance["target"])
    bad = list(instance["target"])
    bad[-1] += 1
    with pytest.raises(ValueError, match="not in the native"):
        check_point(records, instance, bad)


def test_small_exact_cvp_reference_is_explicitly_exponential_and_whole_capped():
    records, secret = honest()
    result = small_exact_reference(records)
    assert result["minimizing_secrets"] == (secret,)
    assert result["optimum_squared_distance"] == squared_residual_cost(records, secret) == 0
    assert result["secret_evaluations"] == 81 and not result["reference_is_polynomial_time_decoder"]
    skipped = small_exact_reference(records, max_secrets=80)
    assert skipped["status"] == "WHOLE_CVP_REFERENCE_CAP_EXHAUSTED"
    assert not skipped["partial_optimum_claimed"]
    assert compile_cvp_instance(records, max_equations=5)["status"] == "WHOLE_LATTICE_CAP_EXHAUSTED"


def test_complete_bounded_controls_include_all_dual_indices_and_nonzero_differences():
    controls = bounded_source_controls()
    assert [c["modulus"] for c in controls] == [3, 9, 27]
    assert all(c["all_nonzero_secret_differences_and_dual_pairs_checked"] == (c["modulus"]-1)*c["modulus"]**2
               for c in controls)


@pytest.mark.parametrize("difference,frequency", (((), (0, 0)), ((9,), (0, 0)), ((True,), (0, 0)),
                                                 ((1,), (0,)), ((1,), (0, 9))))
def test_malformed_ring_differences_and_dual_indices_rejected(difference, frequency):
    with pytest.raises(ValueError):
        wrong_residual_character(9, difference, frequency)


def test_live_conditional_reduction_replays_independently():
    checker = REPORT.parents[1]/"certificates/ternary_native_cvp_reduction_crosscheck.js"
    output = subprocess.run(["node", str(checker)], text=True, capture_output=True, check=True)
    result = json.loads(output.stdout)
    assert result["status"] == "PASS" and result["exact_wrong_secret_dual_checks"] == 19620
    assert not result["near_exact_CVP_solver_supplied"]


@pytest.mark.parametrize("mutation", ("factor", "copies", "solver", "nonprimitive"))
def test_independent_checker_rejects_wrong_constants_and_unpaid_promises(tmp_path, mutation):
    report = json.loads(REPORT.read_text())
    ledger = report["population_ledgers"][0]
    if mutation == "factor":
        ledger["sufficient_norm_approximation_factor"] = "1647/1297"
    elif mutation == "copies":
        ledger["original_measured_qutrits"] -= 1
    elif mutation == "solver":
        ledger["approximate_CVP_solver_supplied"] = True
    else:
        ledger["wrong_secret_difference_must_be_primitive"] = True
    file = tmp_path/"forged.json"
    file.write_text(json.dumps(report))
    checker = REPORT.parents[1]/"certificates/ternary_native_cvp_reduction_crosscheck.js"
    assert subprocess.run(["node", str(checker), str(file)], capture_output=True).returncode != 0


def test_stronger_approximation_tolerance_is_not_free_and_bad_tradeoffs_rejected():
    cheap = reduction_ledger(4, 8, slack=Fraction(1, 81), norm_factor=Fraction(13, 12))
    balanced = reduction_ledger(4, 8)
    relaxed = reduction_ledger(4, 8, slack=Fraction(1, 4096), norm_factor=Fraction(19, 16))
    assert cheap["integer_copy_multiplier"] == 821
    assert cheap["original_measured_qutrits"] < balanced["original_measured_qutrits"] < relaxed["original_measured_qutrits"]
    for slack, factor in ((Fraction(1, 128), Fraction(19, 16)), (Fraction(2, 81), Fraction(1)),
                          (Fraction(0), Fraction(1))):
        with pytest.raises(ValueError):
            reduction_ledger(4, 8, slack=slack, norm_factor=factor)
