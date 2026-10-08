from fractions import Fraction
import json
import random
import subprocess

from flint import fmpq
import numpy as np
import pytest
from sympy import Matrix, symbols, factor

from cyclotomic_fiber_receiver import frequency_matrix, inverse_frequency_coordinates
from cyclotomic_rescaling_gate import MPI, ideal_chart, _phase
from native_noisy_phase_input import (
    REPORT, angle_recipe, even_frequency_matrix, finite_density_control, gate_budget,
    native_labels, prepare_inputs, quantum_input_bound, rounded_gaussian_quantum_profile,
    sqrt_box, trace_distance_box,
)
from ternary_noise_degradation import NoisyLinearRecord, unmask


def test_unbounded_even_map_follows_original_ramification_not_an_empirical_table():
    Z = Matrix([[0, -1], [1, -1]])
    T = -Z.inv()
    assert MPI**2 == -3*Z and T**3 == -Matrix.eye(2) and T**6 == Matrix.eye(2)
    for r in range(1, 25):
        q, original = frequency_matrix(2*r)
        matrix = Matrix(even_frequency_matrix(r))
        assert matrix == original and matrix.det() == -1 and q == 3**r
        assert ideal_chart(2*r)[0] == (q, 0, q)
        assert Matrix([[-1, 1]])*T**(r-1) == matrix[:1, :]
    # No HNF level cap or q-sized table can be used on this route.
    for r in (256, 257, 300, 10000):
        q, rng = 3**r, random.Random(r)
        a, c = tuple(rng.randrange(q) for _ in range(4)), tuple(rng.randrange(q) for _ in range(4))
        labels, matrix = native_labels(a, c, q), even_frequency_matrix(r)
        assert tuple((matrix[0][0]*u+matrix[0][1]*v) % q for u, v in labels) == a
        assert tuple((matrix[1][0]*u+matrix[1][1]*v) % q for u, v in labels) == c


@pytest.mark.parametrize("r", (1, 2, 3))
def test_small_native_label_bijection_matches_actual_source(r):
    q = 3**r
    labels = set()
    for a in range(q):
        for c in range(q):
            label = native_labels((a,), (c,), q)[0]
            assert label == inverse_frequency_coordinates(a, c, 2*r)
            labels.add(label)
    assert len(labels) == q*q


def test_trace_eigenfactorization_is_symbolic_not_a_fitted_small_example():
    phi = symbols("phi", real=True)
    lam = symbols("lam")
    t, r = (phi-1)/3, (phi**2-1)/3
    difference = Matrix([[0, t, t], [t, 0, r], [t, r, 0]])
    assert factor(difference.charpoly(lam).as_expr()-(lam+r)*(lam**2-r*lam-2*t*t)) == 0
    assert difference*Matrix([0, 1, -1]) == -r*Matrix([0, 1, -1])


@pytest.mark.parametrize("r", (1, 2, 3, 4))
def test_prepared_phase_family_is_original_integer_embedded_native_state(r):
    q, rng = 3**r, random.Random(131000+r)
    secret = tuple(rng.randrange(q) for _ in range(4))
    a, c = tuple(rng.randrange(q) for _ in range(4)), tuple(rng.randrange(q) for _ in range(4))
    labels = native_labels(a, c, q)
    actual = tuple(_phase(tuple((s, 0) for s in secret), labels, j, 2*r) for j in range(3))
    expected = tuple(np.exp(2j*np.pi*(sum(x*y for x, y in zip(row, secret)) % q)/q)
                     for row in ((0,)*4, a, c))
    assert max(abs(x-y) for x, y in zip(actual, expected)) < 3e-15


@pytest.mark.parametrize("phi", ("-1", "-1/2", "0", "1/4", "1/2", "999/1000", "1"))
def test_exact_trace_intervals_cover_eigenvalues_and_sharper_bound(phi):
    lo, hi = trace_distance_box(phi)
    value = float(fmpq(phi))
    matrix = np.array([[1, value, value], [value, 1, value*value], [value, value*value, 1]])/3
    distance = sum(abs(np.linalg.eigvalsh(matrix-np.ones((3, 3))/3)))/2
    assert float(lo)-2e-15 <= distance <= float(hi)+2e-15
    assert hi-lo <= fmpq(1, 2**64) and hi <= 1-fmpq(phi)
    assert min(np.linalg.eigvalsh(matrix)) >= -2e-15


def test_rational_sqrt_bounds_and_exact_perfect_squares():
    for x in ("0", "1", "4", "2", "123456789/100000000"):
        lo, hi = sqrt_box(x, 80)
        assert lo*lo <= fmpq(x) <= hi*hi and hi-lo <= fmpq(1, 2**80)
    assert sqrt_box(4, 80) == (2, 2)


@pytest.mark.parametrize("q", (3, 9, 27, 81))
def test_finite_density_controls_average_actual_independent_phase_errors(q):
    c = finite_density_control(q)
    assert c["numerical_trace_distance_diagnostic"] <= float(fmpq(c["moment_trace_distance_upper"]))
    assert not c["numeric_diagnostic_is_certificate"] and not c["calibration_is_LWE_hardness_source"]


def test_preparation_only_uses_known_values_and_charges_disjoint_originals():
    q, s, mask = 81, (17, 28), (4, 9)
    labels, errors = ((1, 0), (0, 1), (2, 3), (4, 5)), (-1, 0, 1, 0)
    samples = tuple(NoisyLinearRecord(a, (sum(x*y for x, y in zip(a, s))+e) % q, q, str(i))
                    for i, (a, e) in enumerate(zip(labels, errors)))
    batch = prepare_inputs(samples, mask, Fraction(1, 2))
    assert batch.source_ancestry == (("0", "1"), ("2", "3"))
    for j, recipe in enumerate(batch.reduction_side_recipes):
        expected = tuple((samples[2*j+k].value+sum(x*y for x, y in zip(labels[2*j+k], mask))) % q for k in range(2))
        assert recipe["known_phase_values"] == expected
        assert not recipe["secret_or_errors_as_preparation_inputs"] and not recipe["hardware_synthesized"]
    for view in batch.receiver_view():
        assert set(view) == {"modulus", "level", "ring_labels", "first_frequency", "second_frequency", "state_handle", "access"}
        assert "known_phase_values" not in view and "reduction_side_mask" not in view
    assert unmask(tuple((a+b) % q for a, b in zip(s, mask)), mask, q) == s
    assert not batch.bound["ideal_source_inverse_supplied"]


def test_reused_pair_is_not_allowed_to_masquerade_as_independent_input_states():
    a, b = NoisyLinearRecord((1,), 2, 9, "a"), NoisyLinearRecord((2,), 4, 9, "b")
    with pytest.raises(ValueError, match="independent original pair"):
        prepare_inputs((a, b, a, b), (0,), 1)
    with pytest.raises(ValueError):
        prepare_inputs((a, NoisyLinearRecord((1, 2), 0, 9, "c")), (0,), 1)


def test_shared_pair_two_copy_coherence_differs_from_independent_originals():
    q, chi = 3, ((-1, .25), (0, .5), (1, .25))
    phi = lambda k: sum(p*np.exp(2j*np.pi*k*e/q) for e, p in chi)
    reused, independent = phi(2)/9, phi(1)**2/9
    assert abs(reused-independent-1/48) < 1e-15


@pytest.mark.parametrize("M,kappa", ((1, 1), (512, 64), (2**80, 160)))
def test_gate_precision_scales_with_input_count(M, kappa):
    g = gate_budget(M, kappa)
    assert fmpq(g["M_state_preparation_trace_error_upper"]) <= fmpq(1, 2**kappa)
    assert g["local_gate_precision_bits"] == kappa+(2*M-1).bit_length()
    assert not g["universal_gate_synthesis_implemented"]


@pytest.mark.parametrize("q", (3, 81, 3**300))
def test_known_angles_have_exact_dyadic_precision_without_float(q):
    for k in (0, 1, q//2, q-1):
        a = angle_recipe(q, k, 100)
        theta = fmpq(a["dyadic_radian_angle"])
        lower, upper = fmpq(a["angle_lower"]), fmpq(a["angle_upper"])
        assert max(abs(theta-lower), abs(theta-upper)) == fmpq(a["angle_error_upper"])
        assert fmpq(a["angle_error_upper"]) <= fmpq(1, 2**100)
        assert not a["angle_description_is_hardware_synthesis"]


def test_large_root_loss_is_nonvacuous_but_no_receiver_or_hardness_is_admitted():
    valid = quantum_input_bound(3**80, 512, "1/2")
    assert valid["bound_is_nonvacuous"]
    assert not valid["efficient_receiver_supplied"] and not valid["hardness_transfer_admitted"]
    assert not valid["individual_pure_realization_has_this_noise_bound"]
    assert not quantum_input_bound(9, 512, "1/2")["bound_is_nonvacuous"]


def test_gaussian_source_profiles_charge_quantum_input_and_rounding_not_classical_noise_sampler():
    quantum = rounded_gaussian_quantum_profile(64, 3**16, "1/1048576", 512)
    classical = rounded_gaussian_quantum_profile(64, 3**64, "1/1048576", 512)
    invalid = rounded_gaussian_quantum_profile(64, 9, "1/1048576", 512)
    assert quantum["published_quantum_worst_case_source_parameter_guard"]
    assert not quantum["published_classical_worst_case_source_parameter_guard"]
    assert classical["published_classical_worst_case_source_parameter_guard"]
    assert not invalid["published_quantum_worst_case_source_parameter_guard"]
    assert not classical["hardness_transfer_admitted"] and not classical["general_full_ring_secret_covered"]
    assert fmpq(classical["composed_success_loss_upper"]) < fmpq(1, 10**8)
    assert "sampler_budget" not in classical
    assert rounded_gaussian_quantum_profile(64, 3**16, "1/2", 512)["composed_success_loss_upper"] == "1"


def test_independent_checker_replays_source_labels_angles_density_and_false_copy_shortcut():
    result = subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_noisy_phase_input_crosscheck.js")], capture_output=True, text=True, check=True)
    result = json.loads(result.stdout)
    assert result["status"] == "PASS" and result["classical_originals"] == 80
    assert result["native_gate_recipes"] == 40 and result["certified_known_angles"] == 80
    assert result["exact_density_entries"] == 36 and result["Gaussian_source_profiles"] == 4
    assert result["shared_pair_countercontrols"] == 1 and result["hardware_states_executed"] == 0


@pytest.mark.parametrize("mutation", ("density", "phase", "label", "reuse", "angle", "loss", "inverse", "leak", "hardness"))
def test_independent_checker_rejects_forged_input_or_access_certificates(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    batch = r["controls"][0]["batch"]
    if mutation == "density":
        r["exact_density_controls"][0]["averaged_phase_frame_density_exact"][1][2] = ["1/3"]
    elif mutation == "phase":
        batch["reduction_side_recipes"][0]["known_phase_values"][0] = 999
    elif mutation == "label":
        batch["receiver_inputs"][0]["ring_labels"][0][0] = 999
    elif mutation == "reuse":
        r["controls"][0]["source_records"][2]["source_id"] = r["controls"][0]["source_records"][0]["source_id"]
    elif mutation == "angle":
        batch["reduction_side_recipes"][0]["angles"][0]["angle_error_upper"] = "1"
    elif mutation == "loss":
        r["source_profiles"][0]["composed_success_loss_upper"] = "0"
    elif mutation == "inverse":
        r["ideal_unknown_source_inverse_supplied"] = True
    elif mutation == "leak":
        batch["receiver_inputs"][0]["known_phase_values"] = [0, 0]
    else:
        r["source_profiles"][0]["hardness_transfer_admitted"] = True
    file = tmp_path/"forged.json"
    file.write_text(json.dumps(r))
    assert subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_noisy_phase_input_crosscheck.js"), str(file)], capture_output=True).returncode != 0


@pytest.mark.parametrize("call", (
    lambda: even_frequency_matrix(True), lambda: native_labels((1,), (2,), 10),
    lambda: native_labels((True,), (2,), 9), lambda: quantum_input_bound(9, 1, .5),
    lambda: quantum_input_bound(9, 1, -1), lambda: trace_distance_box("3/2"),
    lambda: sqrt_box(-1, 8), lambda: angle_recipe(9, 9, 8),
    lambda: rounded_gaussian_quantum_profile(2, 9, 0, 1),
))
def test_false_or_floating_source_promises_fail_closed(call):
    with pytest.raises(ValueError):
        call()
