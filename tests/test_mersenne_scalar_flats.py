from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from random import Random

import pytest

from theorems import mersenne_scalar_flats as attack
from theorems.cubic_rs_affine_flats import flat_points
from theorems.explicit_quadratic_opi import element, encoded
from theorems.mersenne_reciprocal_curve import make_instance, reciprocal_trace


@pytest.mark.parametrize("bits,s,dimension", [(3, 1, 1), (5, 2, 2), (7, 3, 2), (17, 3, 3)])
@pytest.mark.parametrize("target", [0, 1])
def test_flat_certificates_and_scalar_identity(bits, s, dimension, target):
    flat = attack.construct_flat(bits, s, target, dimension, Random(17030+target))
    assert flat["status"] == "ACCEPTED_FLAT"
    d = (1 << s)-1
    assert flat["mu"] and flat["lambda"]
    assert encoded(element(bits, flat["lambda"])**d) == flat["mu"]
    assert flat["local_equation_rank"] <= 1 << dimension < bits
    points = flat_points(flat["origin"], flat["directions"])
    assert len(set(points)) == 1 << dimension
    assert 0 not in points
    assert all(reciprocal_trace(bits, s, x) == target for x in points)
    scale = element(bits, flat["lambda"])
    assert encoded(scale*element(bits, flat["origin"])) == flat["unscaled_origin"]
    assert [encoded(scale*element(bits, v)) for v in flat["directions"]] == flat["unscaled_directions"]
    assert not flat["affine_lift_claimed"]


def test_exact_local_bound_and_conditioning():
    assert attack.local_flat_budget(17, 3, 3)["bad_translation_union_bound"] == Fraction(5391, 1 << 17)
    row = attack.local_flat_budget(31, 7, 4)
    assert row["bad_translation_union_bound"] == Fraction(58261647, 2147483648)
    assert row["bad_translation_bound_conditioned_outside_V"] == Fraction(58261631, (1 << 31)-16)
    assert "NOT_GLOBAL" in row["scope"]


def test_zero_mu_sample_uses_nonzero_kernel_vector():
    class ZeroFreeRng:
        def getrandbits(self, bits):
            return 4 if bits == 5 else 0

    flat = attack.construct_flat(5, 2, 0, 2, ZeroFreeRng(), attempts=1)
    assert flat["status"] == "ACCEPTED_FLAT"
    assert flat["mu"] != 0
    assert all(reciprocal_trace(5, 2, x) == 0 for x in flat_points(flat["origin"], flat["directions"]))


def test_origin_rejections_consume_exactly_the_capped_bit_clock():
    class ZeroRng:
        def __init__(self):
            self.widths = []

        def getrandbits(self, bits):
            self.widths.append(bits)
            return 0

    rng = ZeroRng()
    flat = attack.construct_flat(17, 3, 1, 3, rng, attempts=2)
    assert flat["status"] == "UNKNOWN_TRANSLATION_BUDGET"
    assert rng.widths == [17, 17]
    assert flat["attempts"] == flat["origins_in_V_rejected"] == 2
    assert flat["random_bits_consumed"] == 34
    assert flat["free_bit_draws"] == 0


def test_free_coordinate_clock_never_uses_randrange_rejection():
    class ClockRng:
        def __init__(self):
            self.widths = []

        def getrandbits(self, bits):
            self.widths.append(bits)
            return 4 if bits == 5 else 0

    rng = ClockRng()
    flat = attack.construct_flat(5, 2, 0, 2, rng, attempts=1)
    assert rng.widths == [5]+[1]*flat["free_bit_draws"]
    assert flat["free_bit_draws"] == 5-flat["local_equation_rank"]
    assert flat["random_bits_consumed"] == sum(rng.widths) <= flat["random_bit_cap"]


def test_budget_failure_is_local_and_does_not_retry_input(monkeypatch):
    calls = []
    real = attack.affine_system

    def inconsistent(equations, width):
        calls.append(len(equations))
        return dict(real(equations, width), consistent=False)

    monkeypatch.setattr(attack, "affine_system", inconsistent)
    instance = make_instance(5, 2, [7, 2, 11, 5], [1]*4, 1)
    result = attack.solve_with_flats(instance, 2, attempts=2)
    assert calls and all(size == 4 for size in calls)
    assert len(calls) <= 8
    assert result["status"] == "UNKNOWN_LOCAL_FLAT_BUDGET"
    assert result["actual_rank"] is None and result["witness"] is None
    assert result["input"] == instance
    assert result["attempted_input_instances"] == 1
    assert not result["global_unsatisfiability_claimed"]


@pytest.mark.parametrize("dimension", [-1, True, 3, 10])
def test_dimension_cannot_trigger_field_enumeration(dimension):
    with pytest.raises(ValueError):
        attack.local_flat_budget(5, 2, dimension)


@pytest.mark.parametrize("attempts", [0, 33, True])
def test_translation_cap_is_enforced(attempts):
    with pytest.raises(ValueError):
        attack.construct_flat(5, 2, 1, 2, Random(1), attempts)


def test_wrong_scalar_power_is_detectably_not_the_same_predicate():
    flat = attack.construct_flat(7, 3, 1, 2, Random(17030))
    wrong_scale = element(7, flat["mu"])
    wrong = [encoded(element(7, z)/wrong_scale) for z in
             flat_points(flat["unscaled_origin"], flat["unscaled_directions"])]
    assert any(reciprocal_trace(7, 3, x) != 1 for x in wrong)


def test_zero_and_independent_arithmetic_without_predicate_helper(monkeypatch):
    instance = make_instance(5, 2, [7, 19], [0, 0], 1)
    expected = [reciprocal_trace(5, 2, x) for x in range(16)]

    def forbidden(*args):
        raise AssertionError("verifier called backend/predicate arithmetic")

    monkeypatch.setattr(attack, "element", forbidden)
    monkeypatch.setattr(attack, "reciprocal_trace", forbidden)
    assert attack.verify_native_independently(instance, [0, 0])["valid"]
    instance["targets"] = [1, 1]
    assert not attack.verify_native_independently(instance, [0, 0])["valid"]
    for value, target in enumerate(expected):
        instance["targets"] = [target, target]
        assert attack.verify_native_independently(instance, [value, value])["valid"]


def test_strict_schema_and_modulus_gate():
    original = make_instance(5, 2, [7, 19], [0, 0], 1)
    for mutation in ("modulus", "extra", "missing_s", "duplicate", "boolean"):
        instance = deepcopy(original)
        if mutation == "modulus":
            instance["field_modulus_coefficients"][1] ^= 1
        elif mutation == "extra":
            instance["legacy"] = True
        elif mutation == "missing_s":
            del instance["s"]
        elif mutation == "duplicate":
            instance["points"] = [7, 7]
        else:
            instance["targets"][0] = False
        with pytest.raises(ValueError):
            attack.solve_with_flats(instance, 1)
        with pytest.raises(ValueError):
            attack.verify_native_independently(instance, [0, 0])


def test_original_syndrome_rows_and_witness_mutation():
    instance = make_instance(5, 2, [7, 19], [0, 0], 1)
    value = 3
    instance["targets"] = [reciprocal_trace(5, 2, value)]*2
    assert attack.verify_native_independently(instance, [value, value])["valid"]
    assert not attack.verify_native_independently(instance, [value ^ 1, value])["valid"]
    instance = make_instance(5, 2, [7, 19, 8], instance["targets"]+[0], 2)
    replay = attack.verify_native_independently(instance, [value, value, 0])
    assert replay["field_syndromes"][0] == 0
    assert replay["field_syndromes"][1] != 0
    assert not replay["valid"]


@pytest.mark.parametrize("witness", [[0], [False, 0], [-1, 0], [32, 0], "00"])
def test_independent_verifier_rejects_malformed_witness(witness):
    instance = make_instance(5, 2, [7, 19], [0, 0], 1)
    with pytest.raises(ValueError):
        attack.verify_native_independently(instance, witness)


def test_consistent_rank_deficiency_still_returns_verified_witness(monkeypatch):
    instance = make_instance(5, 2, [7, 19], [0, 0], 1)
    flat = attack.construct_flat(5, 2, 0, 2, Random(17030))
    monkeypatch.setattr(attack, "construct_flat", lambda *args: deepcopy(flat))
    result = attack.solve_with_flats(instance, 2)
    assert result["status"] == "VERIFIED_NATIVE_CLASSICAL_WITNESS"
    assert result["actual_rank"] == 2 < result["binary_equations"]
    assert not result["full_row_rank"]
    assert result["verification"]["valid"]


def test_arbitrary_valid_points_targets_and_scoped_inconsistency():
    instance = make_instance(5, 2, [19, 2, 7, 30], [0, 1, 0, 1], 3)
    result = attack.solve_with_flats(instance, 1, seed=17030)
    assert result["input"] == instance
    assert result["actual_rank"] == result["linear_system"]["rank"]
    assert result["status"] == "NO_SOLUTION_IN_THIS_PRODUCT_FLAT"
    assert not result["global_unsatisfiability_claimed"]
    assert not result["uniform_sampling"] and not result["asymptotic_solver"]


def test_fixed_native_n17_and_independent_mutation():
    specifications = attack.fixed_cases()
    assert [(row["instance"]["bits"], row["instance"]["s"], row["seed"], row["dimension"])
            for row in specifications] == [(17, 3, 17030, 3), (17, 3, 17031, 3), (31, 7, 31030, 4)]
    result = attack.solve_with_flats(**specifications[0])
    assert result["status"] == "VERIFIED_NATIVE_CLASSICAL_WITNESS"
    assert result["actual_rank"] == 612
    assert len(result["flats"]) == 289
    assert result["translation_cap"] == 32
    assert result["verification"]["valid"]
    witness = list(result["witness"])
    witness[0] ^= 1
    assert not attack.verify_native_independently(result["input"], witness)["valid"]


def test_report_requires_note_before_running(tmp_path, monkeypatch):
    monkeypatch.setattr(attack, "ROOT", tmp_path)
    monkeypatch.setattr(attack, "SOURCE_PATHS", ("research/MERSENNE_SCALAR_FLAT_ATTACK.md",))
    monkeypatch.setattr(attack, "solve_with_flats", lambda **kwargs: pytest.fail("run before note exists"))
    with pytest.raises(FileNotFoundError):
        attack.report()


def test_report_binds_sources_and_all_fixed_inputs_before_runs(tmp_path, monkeypatch):
    expected = {}
    for name in attack.SOURCE_PATHS:
        path = tmp_path/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(name, encoding="utf-8")
        expected[name] = hashlib.sha256(name.encode()).hexdigest()
    monkeypatch.setattr(attack, "ROOT", tmp_path)
    specifications = attack.fixed_cases()
    events = []

    def fixed():
        events.append("all_inputs_fixed")
        return specifications

    def solve(**specification):
        events.append(specification["seed"])
        return {"status": "TEST_ONLY", "input": specification["instance"]}

    monkeypatch.setattr(attack, "fixed_cases", fixed)
    monkeypatch.setattr(attack, "solve_with_flats", solve)
    result = attack.report()
    assert events == ["all_inputs_fixed", 17030, 17031, 31030]
    assert result["source_hashes"] == expected
    assert not result["quantum_algorithm"] and not result["novelty_claimed"]
    assert not result["uniform_sampling"] and not result["asymptotic_solver"]
    assert json.loads(json.dumps(attack._serialize(result)))["source_hashes"] == expected

    def modifying_solve(**specification):
        (tmp_path/attack.SOURCE_PATHS[0]).write_text("changed", encoding="utf-8")
        return {"status": "TEST_ONLY"}

    monkeypatch.setattr(attack, "solve_with_flats", modifying_solve)
    with pytest.raises(RuntimeError, match="changed during report"):
        attack.report()
