from copy import deepcopy
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import math
import subprocess

import numpy as np
import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_cyclic_extractor import random_even_source
from ternary_soft_fiber_cooling import (
    DERIVATION, REPORT, SoftFiberParent, action_certificate,
    class_uniform_residual_squared, complete_population_control, dense_parent,
    evolve_reference, population_certificate,
)


@pytest.fixture(scope="module")
def parent():
    source = random_even_source(2, 4, 5, 89881)
    return SoftFiberParent(source, source.value((0, 0, 0, 0, 0)))


@pytest.fixture(scope="module")
def artifact():
    return json.loads(REPORT.read_text())


@pytest.mark.parametrize("S", [3, 9, 27])
@pytest.mark.parametrize("t", [Fraction(0), Fraction(1, 27), Fraction(1, 3), Fraction(1)])
def test_exact_local_residual_for_every_marked_count_and_temperature(S, t):
    for r in range(S+1):
        value = class_uniform_residual_squared(S, r, t)
        assert 0 <= value <= r*(S-1)
        if r in (0, S) or t == 1:
            assert value == 0
        else:
            assert value == Fraction(r*(S-r))*(1-t)**2/(r+(S-r)*t*t)


@pytest.mark.parametrize("r,t", [(-1, 0), (4, 0), (True, 0), (1, 0.2), (1, True), (1, -1), (1, 2)])
def test_local_parent_schema_is_exact_not_float_or_unphysical(r, t):
    with pytest.raises(ValueError):
        class_uniform_residual_squared(3, r, t)


@pytest.mark.parametrize("t", ["0", "1/27", "1/3", "1"])
def test_every_actual_local_conditional_is_complete_and_full_root(parent, t):
    for block in combinations(range(parent.source.inputs), 2):
        table = parent.conditional((1, 0, 2, 1, 0), block, t)
        assert table["local_evaluations_charged"] == 9
        assert [tuple(e["digits"]) for e in table["entries"]] == list(product(range(3), repeat=2))
        for e in table["entries"]:
            word = [1, 0, 2, 1, 0]
            for i, x in zip(block, e["digits"]):
                word[i] = x
            assert e["marked"] == (parent.source.value(word) == parent.target)
        assert not table["full_fiber_count_oracle_used"]
        a = [Fraction(x) for x in table["kernel_relative_amplitudes"]]
        assert sum(x*x for x in a) == Fraction(table["kernel_normalizer_squared"]) > 0


def test_zero_temperature_unmarked_class_uses_its_continuous_limit(parent):
    for word in product(range(3), repeat=parent.source.inputs):
        table = parent.conditional(word, (0,), "0")
        if table["marked_count"] == 0:
            assert table["kernel_relative_amplitudes"] == ["1", "1", "1"]
            assert table["all_unmarked_zero_temperature_uses_continuous_limit"]
            assert table["kernel_normalizer_squared"] == "3"
            return
    pytest.fail("preregistered source has no wholly unmarked class")


@pytest.mark.parametrize("support,t", [(1, "1"), (1, "1/3"), (1, "1/27"), (1, "0"), (2, "1/3")])
def test_parent_psd_stationarity_and_state_specific_residual(parent, support, t):
    ref = parent.reference(support, t)
    H = dense_parent(ref)
    assert np.max(abs(H-H.T)) < 1e-14
    eigenvalues = np.linalg.eigvalsh(H)
    assert eigenvalues[0] >= -1e-13 and eigenvalues[-1] <= 1+1e-13
    D = len(H)
    marked = set(ref["marked_word_indices"])
    g = np.array([1 if i in marked else float(Fraction(t)) for i in range(D)])
    assert np.linalg.norm(H@g) < 1e-12
    u = np.ones(D)/math.sqrt(D)
    exact = Fraction(ref["parent_uniform_residual_squared_exact"])
    assert np.linalg.norm(H@u)**2 == pytest.approx(float(exact), abs=1e-14)
    assert exact <= Fraction(ref["mean_local_uniform_residual_squared_exact"]) <= Fraction(ref["uniform_residual_squared_upper"])
    if t == "1":
        assert exact == 0
    elif support == 1:
        assert any(j not in marked for i in marked for j, value in ref["parent_rows"][i] if value != "0") if t != "0" else True


def test_no_collision_premise_is_needed_even_for_many_marked_assignments():
    # Real even-native chart with structured labels, not an invented oracle candidate.
    label = inverse_frequency_coordinates(0, 1, 2)
    source = native_source(((label,), (label,), (label,)), 2)
    parent = SoftFiberParent(source, (0,))
    ref = parent.reference(2, "1/3")
    assert any(r > 1 for b in ref["local_block_certificates"] for r in b["conditional_marked_counts"])
    assert Fraction(ref["parent_uniform_residual_squared_exact"]) <= Fraction(ref["uniform_residual_squared_upper"])


@pytest.mark.parametrize("kind", ["local", "word", "work"])
def test_whole_reference_caps_never_produce_partial_certificates(parent, kind):
    with pytest.raises(ValueError):
        if kind == "local":
            parent.conditional((0,)*5, (0, 1), "1/3", max_local_words=8)
        elif kind == "word":
            parent.reference(1, "1/3", max_words=242)
        else:
            parent.reference(2, "1/3", max_work=1)


def test_large_batch_cap_is_checked_before_block_menu(monkeypatch):
    parent = SoftFiberParent(random_even_source(8, 4, 128, 99411), (0,)*8)
    monkeypatch.setattr("ternary_soft_fiber_cooling.combinations", lambda *a: pytest.fail("enormous block menu materialized"))
    with pytest.raises(ValueError, match="whole parent reference"):
        parent.reference(64, "1/3")
    table = parent.conditional((0,)*128, (0, 7, 63), "1/3")
    assert table["local_evaluations_charged"] == 27


@pytest.mark.parametrize("target", [(9, 0), (0,), (False, 0), (0.0, 0)])
def test_target_is_full_native_root_and_canonical(parent, target):
    with pytest.raises(ValueError):
        SoftFiberParent(parent.source, target)


@pytest.mark.parametrize("schedule", [
    [{"support": 1, "attenuation": "1/3", "duration": "1/10"}],
    [{"support": 1, "attenuation": "1/27", "duration": "1/10", "coefficient": "-2", "marker_coefficient": "3"},
     {"support": 1, "attenuation": "1", "duration": "1/10"}],
])
def test_signed_reheating_dynamics_charge_all_action(parent, schedule):
    result = evolve_reference(parent, schedule)
    cert = result["action_certificate"]
    assert cert["weighting_scope"] == "one_target_density"
    assert result["raw_fiber_success_numeric"] <= float(Fraction(cert["raw_fiber_success_upper"]))+1e-12
    A = sum(Fraction(s["duration"])*abs(Fraction(s.get("coefficient", "1"))) for s in schedule)
    L = sum(Fraction(s["duration"])*abs(Fraction(s.get("marker_coefficient", "0"))) for s in schedule)
    assert Fraction(cert["parent_action"]) == A and Fraction(cert["marked_projector_action"]) == L
    assert not result["numeric_simulation_is_asymptotic_or_rigorous_roundoff_certificate"]


def test_native_pair_population_purity_is_complete_not_seeded():
    result = complete_population_control()
    assert result["entire_IID_label_matrices_checked"] == 81
    assert Fraction(result["mean_collision_purity_exact"]) == Fraction(11, 27)


def test_polynomial_action_with_enlarged_batch_still_has_exponentially_small_success():
    result = population_certificate(128, 243, 648, 5, 128**2)
    assert Fraction(result["action_bound"]["raw_fiber_success_upper"]) < Fraction(1, 2**900)
    assert Fraction(result["source_weighted_fiber_erasure_squared_error_lower"]) > Fraction(99, 100)
    assert result["uses_no_small_collision_or_gap_premise"]
    assert result["uniform_per_instance_action_cap_required"]
    assert not result["efficient_fiber_eraser_supplied"]


def test_more_copies_do_not_remove_the_population_inverse_group_floor():
    a = population_certificate(8, 9, 24, 1, 64)
    b = population_certificate(8, 9, 100, 1, 64)
    G = 9**8
    assert Fraction(a["expected_source_collision_purity_exact"]) > Fraction(b["expected_source_collision_purity_exact"]) > Fraction(1, G)


def test_born_weighted_not_uniform_occupied_frequency_weighting(artifact):
    values = artifact["exact_parent_controls"][0]["full_frequency_values"]
    counts = {}
    for y in values:
        counts[tuple(y)] = counts.get(tuple(y), 0)+1
    purity = Fraction(sum(c*c for c in counts.values()), len(values)**2)
    assert str(purity) == artifact["source_collision_purity_exact"]
    assert purity != Fraction(1, len(counts))


def test_global_block_positive_control_prevents_an_all_hamiltonian_no_go(artifact):
    control = artifact["global_block_positive_control"]
    assert control["target_vector_error_numeric"] < 1e-12
    assert control["support"] == 5 and control["all_words_enumerated"] == 243
    assert control["full_table_preparation_is_charged_exponential"]
    assert control["positive_control_refutes_general_Hamiltonian_lower_bound"]
    assert not artifact["arbitrary_quantum_receiver_lower_bound"]


def test_report_derivation_and_all_false_claim_guards(artifact):
    assert artifact["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    for flag in ("quantum_hardware_gate_export_supplied", "efficient_fiber_eraser_supplied", "arbitrary_quantum_receiver_lower_bound", "quantum_speedup_proved", "candidate_record_accepted", "novelty_claim"):
        assert artifact[flag] is False


def test_independent_exact_replay():
    result = subprocess.run(["node", "research/certificates/ternary_soft_fiber_cooling_crosscheck.js"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "PASS"


@pytest.mark.parametrize("case", ["entry", "residual", "population", "claim", "cost", "scope"])
def test_independent_checker_rejects_tampering(artifact, tmp_path, case):
    bad = deepcopy(artifact)
    if case == "entry":
        bad["exact_parent_controls"][1]["parent_rows"][0][0][1] = "2"
    elif case == "residual":
        bad["exact_parent_controls"][1]["parent_uniform_residual_squared_exact"] = "0"
    elif case == "population":
        bad["population_scaling_ledgers"][-1]["expected_source_collision_purity_exact"] = "0"
    elif case == "claim":
        bad["arbitrary_quantum_receiver_lower_bound"] = True
    elif case == "cost":
        bad["exact_parent_controls"][1]["reference_work_upper"] = "1"
    else:
        bad["finite_dynamics_controls"][0]["action_certificate"]["weighting_scope"] = "original_source_Born_weighted_collision_purity"
    p = tmp_path/"tampered.json"
    p.write_text(json.dumps(bad))
    result = subprocess.run(["node", "research/certificates/ternary_soft_fiber_cooling_crosscheck.js", str(p)], capture_output=True, text=True)
    assert result.returncode != 0
