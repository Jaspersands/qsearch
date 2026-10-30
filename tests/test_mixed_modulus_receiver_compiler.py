"""Tests for public mixed-modulus coordinate compiler and complete-channel error allocator."""
from fractions import Fraction
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from theorems import mixed_modulus_receiver_compiler as compiler
from theorems.pilot_receiver_policy import flagged_error_bound
from theorems.mixed_modulus_receiver_compiler import (
    TOL,
    MixedModulusCenterSpec,
    compile_mixed_modulus_instrument,
    verify_mixed_modulus_unit_scale_cancellation,
    CyclicQFTStageBudget,
    allocate_cyclic_qft_error_schedule,
    compile_prime_power_receiver_schedule,
    is_prime,
    qft_matrix,
)


def test_public_mixed_modulus_character_pairing_and_orthogonality():
    """Verify that verify_public_dual_bijection passes for Z=Z/3 x Z/9 and Z=Z/2 x Z/4 x Z/8."""
    # Test 1: Z = Z/3Z x Z/9Z (|Z| = 27)
    spec3 = MixedModulusCenterSpec(3, (1, 2))
    assert spec3.rank == 2
    assert spec3.moduli == (3, 9)
    assert spec3.order == 27
    res3 = spec3.verify_public_dual_bijection()
    assert res3["verified"] is True
    assert res3["order"] == 27
    assert res3["characters_verified"] == 27
    assert res3["orthogonality_max_error"] < 1e-10
    assert res3["completeness_max_error"] < 1e-10

    # Test 2: Z = Z/2Z x Z/4Z x Z/8Z (|Z| = 64)
    spec2 = MixedModulusCenterSpec(2, (1, 2, 3))
    assert spec2.rank == 3
    assert spec2.moduli == (2, 4, 8)
    assert spec2.order == 64
    res2 = spec2.verify_public_dual_bijection()
    assert res2["verified"] is True
    assert res2["order"] == 64
    assert res2["characters_verified"] == 64
    assert res2["orthogonality_max_error"] < 1e-10
    assert res2["completeness_max_error"] < 1e-10


def test_mixed_modulus_kraus_projectors_and_central_subgroup_orbit_density():
    """Finite regular-action reference on Z/3 x Z/9 with intersection <(1, 3)>."""
    spec = MixedModulusCenterSpec(3, (1, 2))
    elems = spec.elements()
    n_g = len(elems)
    assert n_g == 27

    elem_to_idx = {e: i for i, e in enumerate(elems)}

    # Faithful regular action of Z on G = Z: R_{embed(z)} |x> = |x - z mod moduli>
    def right_shift(x_idx: int, z: tuple[int, ...]) -> int:
        x_elem = elems[x_idx]
        shifted = spec.add(x_elem, spec.neg(z))
        return elem_to_idx[shifted]

    # Non-split cyclic subgroup H = <(1, 3)> of order 3
    # Elements: (0, 0), (1, 3), (2, 6)
    central_intersection = [(0, 0), (1, 3), (2, 6)]
    assert len(central_intersection) == 3

    # Run compiler
    instrument = compile_mixed_modulus_instrument(
        spec=spec,
        n_group=n_g,
        right_shift=right_shift,
        central_intersection=central_intersection,
    )

    assert instrument["verified"] is True
    assert instrument["hermitian_max_error"] < 1e-10
    assert instrument["idempotence_max_error"] < 1e-10
    assert instrument["orthogonality_max_error"] < 1e-10
    assert instrument["completeness_max_error"] < 1e-10
    assert instrument["kraus_equivalence_max_error"] < 1e-10

    # This constructed orbit density is not a general hidden-subgroup source.
    assert instrument["central_intersection_validated"] is True
    assert instrument["density_source"] == "constructed_central_subgroup_orbit_density"
    assert instrument["density_commutation_max_error"] < 1e-10
    assert instrument["density_commutes_with_projectors"] is True
    assert instrument["hidden_subgroup_state_certified"] is False

    outcome_probs = instrument["outcome_probabilities"]
    assert outcome_probs is not None
    assert len(outcome_probs) == 27

    # Check exact outcome distribution:
    # Exactly |Z| / |H| = 9 outcomes have prob 1/9, remaining 18 have prob 0
    non_zero_outcomes = []
    zero_outcomes = []
    for y, prob in outcome_probs.items():
        if abs(prob - 1.0 / 9.0) < 1e-10:
            non_zero_outcomes.append(y)
        elif abs(prob) < 1e-10:
            zero_outcomes.append(y)
        else:
            pytest.fail(f"unexpected probability {prob} for outcome {y}")

    assert len(non_zero_outcomes) == 9
    assert len(zero_outcomes) == 18

    # Verify that non-zero outcomes satisfy y_1 / 3 + 3 * y_2 / 9 == 0 mod 1
    # which is equivalent to y_1 + y_2 == 0 mod 3
    for y1, y2 in non_zero_outcomes:
        assert (y1 + y2) % 3 == 0

    # Verify that zero outcomes do NOT satisfy y_1 + y_2 == 0 mod 3
    for y1, y2 in zero_outcomes:
        assert (y1 + y2) % 3 != 0


def test_mixed_modulus_unit_scale_coherence_cancellation():
    """Verify active unit-scale off-coset coherence cancellation on Z = Z/3Z x Z/9Z at degree 2."""
    spec = MixedModulusCenterSpec(3, (1, 2))
    degree = 2

    # Constructed outcomes y_0, y_1, y_2, y_3
    # s = (1, 2, 4, 0), active subset A = {0, 1, 2}
    # s_0^2 = 1, s_1^2 = 4, s_2^2 = 16 = 7 mod 9
    # Coord 0: 1 * 1 + 4 * 2 + 7 * 0 = 9 == 0 mod 3
    # Coord 1: 1 * 2 + 4 * 5 + 7 * 2 = 36 == 0 mod 9
    y_cancelling = [(1, 2), (2, 5), (0, 2), (1, 1)]
    scales_cancelling = [1, 2, 4, 0]
    active = {0, 1, 2}

    result = verify_mixed_modulus_unit_scale_cancellation(
        spec=spec,
        degree=degree,
        outcomes=y_cancelling,
        active=active,
        scales=scales_cancelling,
    )

    assert result.cancels is True
    assert bool(result) is True
    assert result["cancels"] is True
    assert result["all_components_zero"] is True
    assert result["zero_sum_per_component"] == [0, 0]
    assert result["max_phase_turn_error"] == Fraction(0)

    # Perturb scales to non-cancelling tuple: e.g. s_0 = 2 instead of 1
    scales_non_cancelling = [2, 2, 4, 0]
    bad_result = verify_mixed_modulus_unit_scale_cancellation(
        spec=spec,
        degree=degree,
        outcomes=y_cancelling,
        active=active,
        scales=scales_non_cancelling,
    )
    assert bad_result.cancels is False
    assert bool(bad_result) is False
    assert bad_result["cancels"] is False

    # Also verify that raise_on_failure=True raises an exception on non-cancelling tuple
    with pytest.raises(ArithmeticError):
        verify_mixed_modulus_unit_scale_cancellation(
            spec=spec,
            degree=degree,
            outcomes=y_cancelling,
            active=active,
            scales=scales_non_cancelling,
            raise_on_failure=True,
        )

    # Inactive scale must be 0
    bad_inactive = [1, 2, 4, 1]
    with pytest.raises(ValueError):
        verify_mixed_modulus_unit_scale_cancellation(
            spec=spec,
            degree=degree,
            outcomes=y_cancelling,
            active=active,
            scales=bad_inactive,
            raise_on_failure=True,
        )


def test_cleve_watrous_cyclic_qft_error_allocator_composes_with_pilot_receiver_policy():
    """Verify allocate_cyclic_qft_error_schedule across a 3-stage prime-power descent schedule."""
    # 3 stages with prime 3
    spec0 = MixedModulusCenterSpec(3, (1,))       # rank 1
    spec1 = MixedModulusCenterSpec(3, (1, 2))    # rank 2
    spec2 = MixedModulusCenterSpec(3, (2, 3))    # rank 2

    stage_specs = [spec0, spec1, spec2]
    stage_copies = [10, 15, 20]
    abort_bounds = [Fraction(1, 1000), Fraction(1, 1000), Fraction(1, 1000)]
    eps_total = Fraction(1, 50)

    schedule = compile_prime_power_receiver_schedule(
        specs=stage_specs,
        stage_copies=stage_copies,
        total_error_target=eps_total,
        abort_bounds=abort_bounds,
    )

    assert schedule.self_certified is True
    assert schedule.total_copies == 45
    assert schedule.total_target_error == eps_total
    assert len(schedule.stages) == 3

    # Check each stage's internal consistency
    for t, stage in enumerate(schedule.stages):
        assert stage.stage_index == t
        assert stage.copy_count == stage_copies[t]
        assert stage.abort_bound == abort_bounds[t]
        assert stage.per_measurement_error == 2 * sum(stage.qft_accuracies) + stage.trans_accuracy
        assert stage.stage_quantum_error == stage.copy_count * stage.per_measurement_error
        assert stage.stage_total_error == stage.stage_quantum_error + stage.abort_bound

    # Total stage error must sum to <= eps_total
    assert schedule.total_stage_error <= eps_total

    # Certificate from flagged_error_bound
    cert = schedule.flagged_certificate
    assert cert["total_error_upper"] <= eps_total
    assert cert["acceptance_probability_division_used"] is False
    assert cert["assumptions_verified_by_calculator"] is False

    # Independent check calling flagged_error_bound directly
    max_meas = max(s.per_measurement_error for s in schedule.stages)
    indep_cert = flagged_error_bound(
        ideal_abort=Fraction(0),
        joint_input_distance=Fraction(0),
        measurement_calls=45,
        measurement_half_diamond=max_meas,
        action_calls=0,
        action_half_diamond=Fraction(0),
        control_preparation_distance=Fraction(0),
        classical_clock_abort=sum(abort_bounds),
    )
    assert indep_cert["total_error_upper"] <= eps_total


def test_mixed_modulus_spec_validation_and_arithmetic():
    """Test validation errors and group arithmetic on MixedModulusCenterSpec."""
    # Composite p rejected
    with pytest.raises(ValueError, match="prime integer"):
        MixedModulusCenterSpec(4, (1, 2))

    # p < 2 rejected
    with pytest.raises(ValueError, match="prime integer"):
        MixedModulusCenterSpec(1, (1,))

    # Empty exponents rejected
    with pytest.raises(ValueError, match="non-empty"):
        MixedModulusCenterSpec(3, ())

    # Non-positive exponent rejected
    with pytest.raises(ValueError, match="integers >= 1"):
        MixedModulusCenterSpec(3, (1, 0))

    spec = MixedModulusCenterSpec(5, (1, 2))
    assert spec.canonical([6, -1]) == (1, 24)
    assert spec.add([1, 2], [4, 24]) == (0, 1)
    assert spec.neg([1, 2]) == (4, 23)
    assert spec.scale(2, 2, [1, 1]) == (4, 4)


def test_error_allocator_budget_exhaustion_fails_closed():
    """Verify that an error target smaller than fixed abort fails closed."""
    spec = MixedModulusCenterSpec(3, (1,))
    with pytest.raises(ValueError, match="error budget exhausted"):
        compile_prime_power_receiver_schedule(
            specs=[spec],
            stage_copies=[10],
            total_error_target=Fraction(1, 100),
            abort_bounds=[Fraction(1, 50)],  # 0.02 > 0.01 target
        )


def _regular_c2(x, z):
    return (x - z[0]) % 2


@pytest.mark.parametrize("intersection", [[], [(1,)]])
def test_malformed_central_intersection_terminates(intersection):
    """Former infinite loops must fail promptly even on the regular C2 action."""
    code = f"""
from theorems.mixed_modulus_receiver_compiler import (
    MixedModulusCenterSpec, compile_mixed_modulus_instrument,
)
try:
    compile_mixed_modulus_instrument(
        MixedModulusCenterSpec(2, (1,)), 2, lambda x, z: (x-z[0]) % 2,
        central_intersection={intersection!r},
    )
except ValueError:
    pass
else:
    raise AssertionError('invalid intersection accepted')
"""
    result = subprocess.run(
        [sys.executable, "-B", "-c", code], capture_output=True, text=True,
        cwd=Path(__file__).resolve().parents[1], timeout=5,
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("intersection, message", [
    ([(0,), (0,)], "unique"),
    ([(0,), (4,)], "canonical"),
    ([(0,), (-1,)], "canonical"),
    ([(0,), (1,)], "closed"),
    ([0, 1], "coordinates"),
    ([(False,)], "integers"),
    ([(0.0,)], "integers"),
])
@pytest.mark.parametrize("supply_density", [False, True])
def test_intersection_validated_before_action_even_with_density(intersection, message, supply_density):
    def unexpected_action(x, z):
        pytest.fail("invalid subgroup reached action construction")

    with pytest.raises(ValueError, match=message):
        compile_mixed_modulus_instrument(
            MixedModulusCenterSpec(2, (2,)), 4, unexpected_action,
            central_intersection=intersection,
            density=np.eye(4) / 4 if supply_density else None,
        )


@pytest.mark.parametrize("density, message", [
    (np.array([[0.5, 1.5], [1.5, 0.5]]), "positive semidefinite"),
    (np.full((2, 2), np.nan), "finite"),
    (np.array([[0.5, np.inf], [0, 0.5]]), "finite"),
    (np.ones((2, 3)), "shape"),
    (np.array([0.5, 0.5]), "shape"),
    (np.eye(2), "trace"),
    (np.array([[0.5, 0.1], [0, 0.5]]), "Hermitian"),
    (np.array([[0.5 + 1j, 0], [0, 0.5]]), "trace"),
])
def test_invalid_density_rejected_before_action(density, message):
    def unexpected_action(x, z):
        pytest.fail("invalid density reached action construction")

    with pytest.raises(ValueError, match=message):
        compile_mixed_modulus_instrument(
            MixedModulusCenterSpec(2, (1,)), 2, unexpected_action, density=density,
        )


def test_density_tolerance_and_physical_probabilities():
    plus = np.ones((2, 2)) / 2
    minus = np.eye(2) - plus
    density = (1 + TOL / 4) * plus - TOL / 4 * minus
    result = compile_mixed_modulus_instrument(
        MixedModulusCenterSpec(2, (1,)), 2, _regular_c2, density=density,
    )
    assert result["density_validated"] is True
    assert result["numerical_tolerance"] == TOL
    probabilities = list(result["outcome_probabilities"].values())
    assert all(np.isfinite(p) and -TOL <= p <= 1 + TOL for p in probabilities)
    assert abs(sum(probabilities) - 1) <= TOL
    with pytest.raises(ValueError, match="positive semidefinite"):
        compile_mixed_modulus_instrument(
            MixedModulusCenterSpec(2, (1,)), 2, _regular_c2,
            density=(1 + 2 * TOL) * plus - 2 * TOL * minus,
        )


def test_probability_range_checked_separately_from_psd_tolerance():
    # Each negative eigenvalue is within TOL, but their outcome mass is not.
    plus = np.kron(np.eye(2), np.ones((2, 2)) / 2)
    minus = np.eye(4) - plus
    delta = 3 * TOL / 4
    density = (0.5 + delta) * plus - delta * minus
    with pytest.raises(ArithmeticError, match="probabilities.*physical"):
        compile_mixed_modulus_instrument(
            MixedModulusCenterSpec(2, (1,)), 4, lambda x, z: x ^ z[0],
            density=density,
        )


def test_supplied_density_matching_distribution_is_not_a_coset_state_certificate():
    # Biased orbit weights are physical and commute, but not the uniform orbit mixture.
    result = compile_mixed_modulus_instrument(
        MixedModulusCenterSpec(2, (1,)), 4, lambda x, z: x ^ z[0],
        central_intersection=[(0,)], density=np.diag([0.5, 0.5, 0, 0]),
    )
    assert result["verified"] is True
    assert result["density_source"] == "supplied_density"
    assert result["density_validated"] is True
    assert result["density_commutes_with_projectors"] is True
    assert result["central_intersection_distribution_checked"] is True
    assert result["outcome_probabilities"] == pytest.approx({(0,): 0.5, (1,): 0.5})
    assert result["hidden_subgroup_state_certified"] is False
    assert result["ambient_centrality_certified"] is False
    assert result["receiver_validity_certified"] is False


def test_supplied_noncommuting_density_is_only_a_physicality_check():
    result = compile_mixed_modulus_instrument(
        MixedModulusCenterSpec(2, (1,)), 2, _regular_c2,
        density=np.diag([1, 0]),
    )
    assert result["density_validated"] is True
    assert result["density_commutes_with_projectors"] is False
    assert result["central_intersection_distribution_checked"] is False
    assert result["hidden_subgroup_state_certified"] is False
    assert result["receiver_validity_certified"] is False
    assert result["outcome_probabilities"] == pytest.approx({(0,): 0.5, (1,): 0.5})


def test_supplied_density_mismatching_intersection_distribution_rejected():
    with pytest.raises(ArithmeticError, match="distribution mismatch"):
        compile_mixed_modulus_instrument(
            MixedModulusCenterSpec(2, (1,)), 2, _regular_c2,
            central_intersection=[(0,), (1,)], density=np.eye(2) / 2,
        )


@pytest.mark.parametrize("destination", [True, 0.0, Fraction(0), np.int64(0), -1, 2])
def test_action_indices_must_be_exact_integers_in_range(destination):
    with pytest.raises(ValueError, match="integer indices"):
        compile_mixed_modulus_instrument(
            MixedModulusCenterSpec(2, (1,)), 2, lambda x, z: destination,
        )


@pytest.mark.parametrize("p, n_group, action, message", [
    (2, 2, lambda x, z: 0, "permutations"),
    (2, 2, lambda x, z: 1 - x, "identity"),
    (3, 3, lambda x, z: x if z == (0,) else (1 - x if x < 2 else x), "composition"),
    (2, 2, lambda x, z: x, "free"),
    (2, 3, lambda x, z: (1 - x if x < 2 and z == (1,) else x), "free"),
])
def test_action_must_be_a_free_representation(p, n_group, action, message):
    with pytest.raises(ValueError, match=message):
        compile_mixed_modulus_instrument(MixedModulusCenterSpec(p, (1,)), n_group, action)


def test_dense_reference_scope_resources_and_cached_orbit_action():
    calls = []

    def action(x, z):
        calls.append((x, z))
        assert len(calls) <= 8, "action must be cached for orbit traversal"
        return x ^ z[0]

    result = compile_mixed_modulus_instrument(
        MixedModulusCenterSpec(2, (1,)), 4, action,
        central_intersection=[(0,), (1,)],
    )
    assert len(calls) == 8
    assert result["outcome_probabilities"] == pytest.approx({(0,): 1.0, (1,): 0.0})
    assert result["density_source"] == "constructed_central_subgroup_orbit_density"
    assert result["free_representation_verified"] is True
    assert result["verification_scope"] == "finite_numerical_instrument_checks"
    assert result["scalable_compiler_implemented"] is False
    assert result["ambient_centrality_certified"] is False
    assert result["hidden_subgroup_state_certified"] is False
    resources = result["resources"]
    assert resources["dense_unitary_dimension"] == 8
    assert resources["complex_entries_per_dense_unitary"] == 64
    assert resources["bytes_per_dense_unitary"] == result["circuit_unitary"].nbytes
    assert resources["cached_permutation_entries"] == 8
    assert resources["synthesized_gate_count"] is None


@pytest.mark.parametrize("value", [True, 1.0, Fraction(1), np.int64(1)])
def test_strict_coordinate_dimension_and_index_types(value):
    spec = MixedModulusCenterSpec(2, (1,))
    with pytest.raises(ValueError, match="integers"):
        spec.canonical((value,))
    with pytest.raises(ValueError, match="integer dimension"):
        qft_matrix(value)
    with pytest.raises(ValueError, match="active indices"):
        verify_mixed_modulus_unit_scale_cancellation(
            spec, 1, [(0,), (0,)], [0, value], [1, 1],
        )
    assert is_prime(value) is False


@pytest.mark.parametrize("outcomes, scales", [([], []), ([(1,)], [0])])
def test_empty_active_support_is_not_receiver_cancellation(outcomes, scales):
    spec = MixedModulusCenterSpec(2, (1,))
    result = verify_mixed_modulus_unit_scale_cancellation(spec, 1, outcomes, [], scales)
    assert result["phase_identity_verified"] is True
    assert result["nonempty_active_support"] is False
    assert result.cancels is False
    assert not result
    assert result["receiver_validity_certified"] is False
    with pytest.raises(ValueError, match="nonempty active support"):
        verify_mixed_modulus_unit_scale_cancellation(
            spec, 1, outcomes, [], scales, raise_on_failure=True,
        )


@pytest.mark.parametrize("copies", [Fraction(3, 2), Fraction(2), True, 2.0, 0, -1])
def test_copy_count_never_coerced(copies):
    spec = MixedModulusCenterSpec(2, (1,))
    for stage in [(spec, copies), {"center_spec": spec, "copy_count": copies}]:
        with pytest.raises(ValueError, match="copy_count.*positive integer"):
            allocate_cyclic_qft_error_schedule([stage], Fraction(1, 10))
    with pytest.raises(ValueError, match="copy_count.*positive integer"):
        compile_prime_power_receiver_schedule([spec], [copies], Fraction(1, 10))


@pytest.mark.parametrize("overrides, message", [
    ({"rank": 1, "moduli": (2, 4)}, "number of moduli"),
    ({"rank": 2, "moduli": (2, 4), "qft_accuracies": (Fraction(0),)}, "qft_accuracies"),
    ({"rank": True}, "rank"),
    ({"rank": Fraction(1)}, "rank"),
    ({"moduli": (2.0,)}, "moduli"),
    ({"moduli": (True,)}, "moduli"),
    ({"moduli": (1,)}, "moduli"),
    ({"moduli": ()}, "number of moduli"),
    ({"center_spec": MixedModulusCenterSpec(2, (2,))}, "match center_spec"),
    ({"center_spec": MixedModulusCenterSpec(2, (1, 2))}, "match center_spec"),
    ({"center_spec": False}, "center_spec"),
    ({"stage_index": True}, "stage_index"),
    ({"copy_count": Fraction(3, 2)}, "copy_count"),
])
def test_stage_shape_validation(overrides, message):
    args = dict(stage_index=0, rank=1, moduli=(2,), copy_count=1,
                qft_accuracies=(Fraction(0),), trans_accuracy=Fraction(0), abort_bound=Fraction(0))
    args.update(overrides)
    with pytest.raises(ValueError, match=message):
        CyclicQFTStageBudget(**args)
    if not ({"stage_index", "qft_accuracies"} & overrides.keys()):
        stage = {k: args[k] for k in ("rank", "moduli", "copy_count", "abort_bound")}
        stage["center_spec"] = args.get("center_spec")
        with pytest.raises(ValueError, match=message):
            allocate_cyclic_qft_error_schedule([stage], Fraction(1, 10))


@pytest.mark.parametrize("value", [0, True, 0.0, Fraction(-1, 10), Fraction(11, 10)])
def test_allowances_are_bounded_exact_fractions_before_budgeting(value):
    spec = MixedModulusCenterSpec(2, (1,))
    for key in ("joint_input_distance", "action_half_diamond", "control_preparation_distance", "ideal_abort"):
        with pytest.raises(ValueError, match="exact Fraction"):
            allocate_cyclic_qft_error_schedule([spec], Fraction(1, 10), **{key: value})
    for stage in [(spec, 1, value), {"center_spec": spec, "abort_bound": value}]:
        with pytest.raises(ValueError, match="exact Fraction"):
            allocate_cyclic_qft_error_schedule([stage], Fraction(1, 10))
    with pytest.raises(ValueError, match="exact Fraction"):
        compile_prime_power_receiver_schedule([spec], [1], Fraction(1, 10), abort_bounds=[value])
    for key in ("qft_accuracies", "trans_accuracy", "abort_bound"):
        args = dict(stage_index=0, rank=1, moduli=(2,), copy_count=1,
                    qft_accuracies=(Fraction(0),), trans_accuracy=Fraction(0), abort_bound=Fraction(0))
        args[key] = (value,) if key == "qft_accuracies" else value
        with pytest.raises(ValueError, match="exact Fraction"):
            CyclicQFTStageBudget(**args)


@pytest.mark.parametrize("calls", [True, 1.0, Fraction(1), -1])
def test_action_count_validated_before_budgeting(calls):
    with pytest.raises(ValueError, match="integer.*call counts"):
        allocate_cyclic_qft_error_schedule(
            [MixedModulusCenterSpec(2, (1,))], Fraction(1, 10), action_calls=calls,
        )


def test_uniform_per_stage_uses_weighted_sum_not_max_or_average(monkeypatch):
    calls = []

    def fixed_only(**kwargs):
        calls.append(kwargs)
        assert kwargs["measurement_calls"] == 0
        assert kwargs["measurement_half_diamond"] == Fraction(0)
        return flagged_error_bound(**kwargs)

    monkeypatch.setattr(compiler, "flagged_error_bound", fixed_only)
    spec = MixedModulusCenterSpec(2, (1,))
    schedule = allocate_cyclic_qft_error_schedule(
        [(spec, 1), (spec, 2)], Fraction(1, 10), strategy="uniform_per_stage",
    )
    assert len(calls) == 1
    cert = schedule.flagged_certificate
    assert schedule.total_copies == cert["measurement_calls"] == 3
    assert cert["stage_copy_counts"] == (1, 2)
    assert cert["per_stage_per_measurement_errors"] == (Fraction(1, 20), Fraction(1, 40))
    assert cert["per_stage_measurement_errors"] == (Fraction(1, 20), Fraction(1, 20))
    assert cert["measurement_error_sum"] == Fraction(1, 10)
    assert schedule.total_stage_error == cert["total_error_upper"] == Fraction(1, 10)
    assert 3 * max(cert["per_stage_per_measurement_errors"]) == Fraction(3, 20)
    assert cert["acceptance_probability_division_used"] is False
    assert cert["assumptions_verified_by_calculator"] is False
    assert cert["physical_implementation_verified"] is False
    assert cert["scalable_compiler_implemented"] is False
    assert schedule.physical_implementation_verified is False
    assert schedule.scalable_compiler_implemented is False
    assert schedule.certification_scope == "exact_conditional_error_budget_arithmetic"


@pytest.mark.parametrize("strategy", ["uniform_per_copy", "uniform_per_stage"])
def test_weighted_hybrid_includes_every_fixed_overhead(strategy):
    stages = [(MixedModulusCenterSpec(2, (1,)), 1, Fraction(1, 100)),
              (MixedModulusCenterSpec(2, (1, 2)), 2, Fraction(1, 50))]
    schedule = allocate_cyclic_qft_error_schedule(
        stages, Fraction(1, 2), strategy=strategy,
        joint_input_distance=Fraction(1, 100), action_calls=3,
        action_half_diamond=Fraction(1, 200),
        control_preparation_distance=Fraction(1, 100), ideal_abort=Fraction(1, 20),
    )
    measurement_sum = sum(s.copy_count * (2 * sum(s.qft_accuracies) + s.trans_accuracy)
                          for s in schedule.stages)
    hybrid = Fraction(1, 100) + 3 * Fraction(1, 200) + Fraction(1, 100) + measurement_sum
    unclipped = Fraction(1, 20) + hybrid + Fraction(3, 100)
    cert = schedule.flagged_certificate
    assert cert["measurement_error_sum"] == measurement_sum
    assert cert["unconditional_hybrid_distance"] == hybrid
    assert cert["unclipped_sum"] == unclipped == Fraction(1, 2)
    assert cert["total_error_upper"] == min(Fraction(1), unclipped)
    assert cert["classical_clock_abort"] == Fraction(3, 100)
    assert schedule.total_stage_error == measurement_sum + Fraction(3, 100)


def test_large_prime_budget_does_not_enumerate_center(monkeypatch):
    def no_enumeration(self):
        pytest.fail("budget arithmetic must not enumerate center elements")

    monkeypatch.setattr(MixedModulusCenterSpec, "elements", no_enumeration)
    prime = 2 ** 61 - 1
    spec = MixedModulusCenterSpec(prime, (1, 2))
    assert spec.moduli == (prime, prime ** 2)
    assert is_prime(prime) is True
    assert is_prime(prime * prime) is False
    schedule = allocate_cyclic_qft_error_schedule([(spec, 3)], Fraction(1, 10))
    assert schedule.flagged_certificate["total_error_upper"] == Fraction(1, 10)
    assert len(schedule.stages[0].qft_accuracies) == 2
    assert schedule.scalable_compiler_implemented is False
