"""Exact interval controls for the arithmetic contract, not quantum compilation."""
from fractions import Fraction
import json

import pytest

from theorems.bpqm_log_reliability import (
    REPORT, compression_angle_log, equality_log, initial_log, parity_log,
    precision_budget, register_width, run_controls,
)


def value(record):
    return Fraction(record["value"])


@pytest.mark.parametrize("a,b", [("0", "0"), ("1/5", "13/20"), ("-7/8", "3/4"),
                                 (str(1-Fraction(1, 1 << 256)), str(-1+Fraction(1, 1 << 255)))])
def test_log_updates_match_exact_signed_overlap_rules_with_certified_accumulated_errors(a, b):
    a, b = Fraction(a), Fraction(b)
    bits, eta = 32, Fraction(1, 1 << 32)
    left, right = initial_log(a, bits=bits), initial_log(b, bits=bits)
    for herald in (0, 1):
        c = (a+b)/(1+a*b) if herald == 0 else (b-a)/(1-a*b)
        target = initial_log(c, bits=192)
        actual = parity_log(left["value"], right["value"], herald, bits=bits)
        assert abs(value(target)-value(actual)) <= 3*eta+Fraction(target["evaluation_error_upper"])
    target = initial_log(a*b, bits=192)
    actual = equality_log(left["value"], right["value"], bits=bits)
    assert abs(value(target)-value(actual)) <= 2*eta+Fraction(target["evaluation_error_upper"])


@pytest.mark.parametrize("a,b", [("1000", "1000"), ("1000", "-1000"), ("0", "-1000000"),
                                 ("1/3", "-7/5")])
def test_extreme_and_cancelling_log_messages_do_not_divide_near_zero(a, b):
    for record in (equality_log(a, b), parity_log(a, b, 0), parity_log(a, b, 1),
                   compression_angle_log(a, b, 0), compression_angle_log(a, b, 1)):
        assert Fraction(record["evaluation_error_upper"]) <= Fraction(1, 1 << 64)
    for bit in (0, 1):
        theta = value(compression_angle_log(a, b, bit))
        assert -Fraction(22, 7) < theta <= 0


def test_boxplus_infinity_norm_lipschitz_and_angle_lipschitz_controls():
    eta = Fraction(1, 1 << 20)
    for a in (Fraction(-1000), Fraction(-1, 3), Fraction(), Fraction(1, 3), Fraction(1000)):
        for b in (Fraction(-1000), Fraction(-2, 7), Fraction(), Fraction(1000)):
            for da, db in ((eta, -eta), (eta, eta), (-eta, -eta)):
                base, changed = equality_log(a, b), equality_log(a+da, b+db)
                tolerance = Fraction(base["evaluation_error_upper"])+Fraction(changed["evaluation_error_upper"])
                assert abs(value(base)-value(changed)) <= eta+tolerance
                for bit in (0, 1):
                    base = compression_angle_log(a, b, bit)
                    changed = compression_angle_log(a+da, b+db, bit)
                    tolerance = Fraction(base["evaluation_error_upper"])+Fraction(changed["evaluation_error_upper"])
                    assert abs(value(base)-value(changed)) <= 2*eta+tolerance


def test_full_adjoint_budget_is_logarithmic_but_not_an_algorithm_or_gate_certificate():
    small = precision_budget(5, 6, "1/1000")
    assert small["fractional_bits_sufficient"] == 17
    assert Fraction(small["logical_rotation_readout_TV_perturbation_upper"]) <= Fraction(1, 1000)
    large = precision_budget(10**12, (1 << 60)*10**12, "1/1000")
    assert 145 <= large["fractional_bits_sufficient"] <= 155
    assert large["reversible_quantum_arithmetic_implemented"] is False
    assert large["finite_universal_gate_synthesis_error_included"] is False
    assert large["bound_is_to_ideal_algorithm_not_Gibbs_without_ideal_correctness"] is True
    assert precision_budget(1, 0, "1/1000")["fractional_bits_sufficient"] == 8


def test_source_error_is_paid_and_missing_headroom_is_rejected():
    result = precision_budget(5, 6, "1/1000", source_error="1/2000")
    assert result["fractional_bits_sufficient"] == 18
    with pytest.raises(ValueError):
        precision_budget(5, 6, "1/1000", source_error="1/1000")
    for a in (True, 1.0, 1, -1):
        with pytest.raises(ValueError):
            initial_log(a)
    with pytest.raises(ValueError):
        parity_log(0, 0, True)


def test_integer_range_is_separate_from_fractional_accuracy():
    small = register_width("13/20", 5, bits=17)
    assert small["message_register_bits_sufficient"] == 21
    large = register_width("13/20", 1111111111111, bits=152)
    assert large["message_register_bits_sufficient"] == 193
    assert Fraction(large["approximate_register_absolute_value_upper"]) < 2**(large["signed_integer_bits_sufficient"]-1)-Fraction(1, 1 << 152)
    assert large["scratch_herald_and_reversible_arithmetic_qubits_not_counted"] is True


def test_source_bound_artifact_replays_without_quantum_or_hardness_promotion():
    report = run_controls()
    assert report == json.loads(REPORT.read_text())
    assert report["large_parameter_graph_or_algorithm_constructed"] is False
    assert report["reversible_quantum_arithmetic_implemented"] is False
    assert report["accepted_speedup_candidate"] is False
