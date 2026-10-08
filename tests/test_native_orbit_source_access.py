from copy import deepcopy
from fractions import Fraction
import json
import subprocess

import numpy as np
import pytest

from native_orbit_source_access import (
    ROOT, OrbitControl, inverse, label_filter, native_fourier_filters,
    norm_squared, relative_orbit_reflection, run_controls, source_recipe,
)
from native_state_hsp_bridge import NativeGroup


@pytest.fixture(scope="module")
def report():
    return run_controls()


@pytest.fixture(scope="module", params=[1, 2])
def matrices(request):
    return OrbitControl(request.param, (2, 1)).matrices()


def test_orbit_source_is_the_complete_actual_coset_mixture(matrices):
    G, labels, elements, V, omega, prepared, density = matrices
    H = set(G.hidden_elements(G.vector(((2, 1),))))
    N, D = len(elements), 3*len(labels)
    assert np.allclose(V.conj().T@V, np.eye(D), atol=2e-12)
    assert np.allclose(V.conj().T@prepared, omega, atol=2e-12)
    for g in elements:
        assert G.compose(g, inverse(G, g)) == (((0, 0),), 0)
        assert G.compose(inverse(G, g), g) == (((0, 0),), 0)
    target = np.array([[int(G.compose(inverse(G, h), g) in H)/N for h in elements] for g in elements])
    assert np.allclose(density, target, atol=2e-12)
    assert np.isclose(np.trace(density), 1)
    assert np.linalg.matrix_rank(density, tol=1e-10) == N//3


def test_full_label_conditioning_does_not_supply_the_unconditioned_coset_promise(matrices):
    _, _, elements, V, omega, _, density = matrices
    N, D = len(elements), omega.shape[0]
    conditional = omega[:, :1]/np.linalg.norm(omega[:, :1])
    out = (V@conditional).reshape(N, D, 1)
    conditional_density = np.einsum("gie,hie->gh", out, out.conj())
    assert not np.allclose(conditional_density, density)
    assert np.linalg.matrix_rank(conditional_density, tol=1e-10) == 1


def test_arbitrary_source_isometry_does_not_imply_a_hidden_subgroup_indicator(matrices):
    _, _, elements, V, omega, _, density = matrices
    N, D = len(elements), omega.shape[0]
    generic = (V/np.sqrt(D)).reshape(N, D, D)
    generic_density = np.einsum("gie,hie->gh", generic, generic.conj())
    assert np.allclose(generic_density, np.eye(N)/N, atol=2e-12)
    assert not np.allclose(generic_density, density)
    assert source_recipe(2, 1)["original_exact_subgroup_indicator_required_for_uniform_coset_state"]
    assert not source_recipe(2, 1)["source_noise_and_gate_precision_certificate_supplied"]


def test_complete_fourier_label_partition_intertwines_and_does_not_amplify(matrices):
    G, _, elements, V, omega, prepared, _ = matrices
    N, D = len(elements), omega.shape[0]
    filters = native_fourier_filters(G, elements)
    assert len(filters) == (9 if G.level == 1 else 11)
    assert np.allclose(sum(P for _, P in filters), np.eye(N), atol=2e-12)
    for schema, P in filters:
        assert np.allclose(P.conj().T, P, atol=2e-12)
        assert np.allclose(P@P, P, atol=2e-12)
        assert round(np.trace(P).real) == schema["irrep_dimension"]**2
        PV = label_filter(P, V, N, D)
        C = V.conj().T@PV
        assert np.allclose(C@C, C, atol=2e-12)
        assert np.allclose(PV, V@C, atol=2e-12)
        initial = norm_squared(label_filter(P, prepared, N, D))
        state = prepared
        for _ in range(5):
            state = relative_orbit_reflection(V, state-2*label_filter(P, state, N, D))
            assert np.isclose(norm_squared(label_filter(P, state, N, D)), initial, atol=2e-12)


def test_noncentral_filter_one_iteration_is_a_seed_compression_polynomial(matrices):
    _, _, elements, V, omega, _, _ = matrices
    N, D = len(elements), omega.shape[0]
    rng = np.random.default_rng(81023)
    basis, _ = np.linalg.qr(rng.normal(size=(N, 4))+1j*rng.normal(size=(N, 4)))
    P = basis@basis.conj().T
    seed = rng.normal(size=(D, 2))+1j*rng.normal(size=(D, 2))
    seed /= np.linalg.norm(seed)
    state = V@seed
    C = V.conj().T@label_filter(P, V, N, D)
    assert np.linalg.norm(C@C-C) > .01
    after = relative_orbit_reflection(V, state-2*label_filter(P, state, N, D))
    actual_good = label_filter(P, after, N, D)
    predicted_good = label_filter(P, V@((3*np.eye(D)-4*C)@seed), N, D)
    assert np.allclose(actual_good, predicted_good, atol=2e-12)
    assert np.isclose(norm_squared(actual_good), np.trace(seed.conj().T@C@(3*np.eye(D)-4*C)@(3*np.eye(D)-4*C)@seed).real)


def test_coordinate_amplification_preserves_any_unknown_reference_entangled_seed(matrices):
    _, _, elements, V, omega, _, _ = matrices
    N, D = len(elements), omega.shape[0]
    rng = np.random.default_rng(478123)
    seed = rng.normal(size=(D, 3))+1j*rng.normal(size=(D, 3))
    seed /= np.linalg.norm(seed)
    P = np.zeros((N, N), complex)
    P[0, 0] = 1
    C = V.conj().T@label_filter(P, V, N, D)
    assert np.allclose(C, np.eye(D)/N, atol=2e-12)
    prepared = V@seed
    moved = relative_orbit_reflection(V, prepared-2*label_filter(P, prepared, N, D))
    success = label_filter(P, moved, N, D).reshape(N, D, 3)[0]
    assert np.allclose(success, (3-4/N)*seed/np.sqrt(N), atol=2e-12)
    assert norm_squared(success) > 1/N


def test_report_separates_counterfactual_fixed_reflection_from_known_relative_inverse(report):
    for c in report["complete_native_orbit_controls"]:
        p = Fraction(1, 3**c["native_level"])
        assert Fraction(c["exact_trivial_label_probability"]) == p
        assert Fraction(c["exact_counterfactual_true_probability"]) == p*(3-4*p)**2
        assert all(np.isclose(h["actual_trivial_label_probability"], float(p)) for h in c["relative_reflection_iteration_history"])
        assert c["relative_orbit_isometry_rank"] > c["desired_fixed_purification_reflection_rank"]
        assert not c["counterfactual_fixed_purification_reflection_is_supplied"]
        assert not c["source_creation_inverse_oracle_of_exact_nilpotent_theorem_supplied"]
        coord = c["noncentral_coordinate_amplification_countercontrol"]
        assert Fraction(coord["exact_probability_after_one_relative_iteration"]) > Fraction(coord["exact_initial_probability"])
        assert coord["output_seed_equals_original_unknown_seed"]
        assert not coord["secret_decoded"]
    assert report["primary_nonexact_Proposition3_does_not_require_creation_inverse"]
    assert not report["all_catalytic_or_noncommuting_receiver_strategies_ruled_out"]


@pytest.mark.parametrize("r,n", [(2,1), (8,8), (32,32), (128,128), (512,512)])
def test_growing_source_recipe_charges_original_copies_and_symbolic_group_register(r, n):
    recipe = source_recipe(r, n)
    assert recipe["group_order"] == {"base": 3, "exponent": r*n+1}
    assert recipe["group_coordinate_trits"] == r*n+1
    assert recipe["known_controlled_R_calls_per_orbit_source"] == 1
    assert recipe["relative_inverse_returns_unknown_input_not_a_known_blank"]
    assert not recipe["fixed_purification_preparation_oracle_supplied"]
    assert not recipe["growing_class_solver_supplied"]


@pytest.mark.parametrize("r,n", [(True,1), (0,1), (1,False), (1,0)])
def test_invalid_resource_models_rejected(r, n):
    with pytest.raises(ValueError):
        source_recipe(r, n)


def test_small_controls_cannot_be_promoted_to_a_growing_nonabelian_fourier_transform():
    with pytest.raises(ValueError, match="n1 levels1-2"):
        native_fourier_filters(NativeGroup(3), ())
    with pytest.raises(ValueError, match="n1 levels1-2"):
        native_fourier_filters(NativeGroup(2, 2), ())
    with pytest.raises(ValueError, match="levels1-2"):
        OrbitControl(3, (1,0)).matrices()
    with pytest.raises(ValueError):
        OrbitControl(True, (1,0))


def replay(data, tmp_path):
    f = tmp_path/"orbit.json"
    f.write_text(json.dumps(data, allow_nan=False))
    return subprocess.run(["node", str(ROOT/"research/certificates/native_orbit_source_access_crosscheck.js"), str(f)], capture_output=True, text=True)


def test_independent_exact_source_projector_replay(report, tmp_path):
    out = replay(report, tmp_path)
    assert out.returncode == 0, out.stderr
    result = json.loads(out.stdout)
    assert result["exact_coset_density_entries"] == 1620
    assert result["complete_irreplabel_filters"] == 40
    assert result["noncentral_amplification_countercontrols"] == 4


@pytest.mark.parametrize("mutation", ["density", "group", "label_mass", "missing_filter", "inverse", "rank", "counterfactual", "coordinate", "source_cost", "scope"])
def test_independent_checker_rejects_forged_access_and_quantum_signal(report, mutation, tmp_path):
    bad = deepcopy(report)
    c = bad["complete_native_orbit_controls"][0]
    if mutation == "density":
        c["full_group_coset_density_real_imag"][0][0][0] = 1
    elif mutation == "group":
        c["all_public_group_elements"] = c["all_public_group_elements"][:-1]
    elif mutation == "label_mass":
        c["complete_known_Fourier_label_partition"][0]["actual_initial_label_probability"] = 1
    elif mutation == "missing_filter":
        c["complete_known_Fourier_label_partition"].pop()
    elif mutation == "inverse":
        c["relative_preparation_inverse_return_error"] = .2
    elif mutation == "rank":
        c["relative_orbit_isometry_rank"] = 1
    elif mutation == "counterfactual":
        c["counterfactual_fixed_purification_reflection_is_supplied"] = True
    elif mutation == "coordinate":
        c["noncentral_coordinate_amplification_countercontrol"]["secret_decoded"] = True
    elif mutation == "source_cost":
        bad["growing_source_recipes"][0]["one_original_IID_native_copy_consumed_per_output"] = False
    else:
        bad["all_catalytic_or_noncommuting_receiver_strategies_ruled_out"] = True
    assert replay(bad, tmp_path).returncode != 0
