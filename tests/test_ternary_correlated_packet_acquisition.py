from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
import subprocess
from collections import Counter

import numpy as np
import pytest

from ternary_correlated_packet_acquisition import (
    DERIVATION, REPORT, PacketAcquisition, physical_control, retention_ledger,
)
from ternary_cyclic_extractor import curvatures, random_even_source
from ternary_phase_depth import NativePhaseHierarchy
from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source


def acquire(n=1, level=6, K=4, seed=88401):
    count = K*(n+1)**2
    source = random_even_source(n, level, count, seed)
    return PacketAcquisition.from_source(source, K, tuple(f"native-{i}" for i in range(count)), count)


@pytest.mark.parametrize("n,level,K", [(1, 4, 2), (1, 10, 4), (2, 6, 5), (4, 12, 9), (8, 16, 16)])
def test_original_source_supports_and_lineage_are_charged_without_assuming_a_decoder(n, level, K):
    acquisition = acquire(n, level, K)
    vectors = curvatures(acquisition.source)
    W = (n+1)**2
    assert len(set(acquisition.active)) == len(acquisition.active)
    assert set(acquisition.active).isdisjoint(acquisition.unused)
    assert len(acquisition.active)+len(acquisition.unused) == K*W
    for j, support in enumerate(acquisition.supports):
        assert support and all(j*W <= i < (j+1)*W for i in support)
        assert all(sum(vectors[i][l] for i in support) % 3 == 0 for l in range(n))
    record = acquisition.source_record()
    assert record["intermediate_odd_input_acquisition_charged"]
    assert record["acquired_original_native_inputs"] == K*W
    assert len(set(record["original_source_ids"])) == K*W
    assert not record["distinct_ids_certify_physical_independence"]
    assert not record["upstream_DCP_or_LWE_input_acquisition_implemented_here"]
    assert not record["unknown_preparation_inverse_or_amplification_used"]


@pytest.mark.parametrize("level", [4, 6, 8, 12])
def test_original_full_root_phase_and_growing_depth_hierarchy_agree(level):
    acquisition = acquire(2, level, 5, 88402)
    pointers = tuple(i % 3 for i in range(len(acquisition.pointers)))
    frame = acquisition.branch(pointers).packet
    branch = acquisition.branch(pointers, (1,)*len(frame.pivots))
    hierarchy = NativePhaseHierarchy.from_packet(branch.packet)
    for z in product(range(3), repeat=branch.packet.retained):
        expected = branch.original_residual(z)
        assert expected == branch.packet.residual(z) == hierarchy.derivative(z, ())
        assert expected == branch.original_residual(z, (2,)*len(acquisition.unused))
    assert hierarchy.retained_modulus == 3**(level//2-1)
    resources = branch.resources()
    assert resources["retained_additive_degree_upper_bound"] == level-1
    assert resources["retained_joint_logical_qutrits"] >= 5-2
    assert not resources["outputs_certified_as_IID_native_samples"]
    assert not resources["matched_packet_copies_or_unknown_weighted_phase_oracle_supplied"]
    # The standalone odd-input packet still correctly does NOT charge acquisition.
    assert not branch.packet.resource_record()["acquiring_intermediate_odd_level_inputs_charged_here"]


def test_two_stage_native_basis_permutation_is_reversible_with_unused_wires_retained():
    acquisition = acquire()
    for digits in product(range(3), repeat=len(acquisition.active)):
        original = [0]*acquisition.source.inputs
        for i, x in zip(acquisition.active, digits):
            original[i] = x
        for i in acquisition.unused:
            original[i] = i % 3
        actual = acquisition.forward(original)
        assert acquisition.inverse(*actual) == tuple(original)
        assert actual[3] == tuple(original[i] for i in acquisition.unused)


@pytest.fixture(scope="module")
def complete_control():
    return physical_control(acquire(), (1,))


def test_all_measured_branches_keep_unit_mass_and_charge_only_active_measurements(complete_control):
    acquisition = acquire()
    branches = complete_control["all_measurement_branches"]
    assert complete_control["complete_active_words_replayed"] == 243
    assert complete_control["total_raw_probability"] == pytest.approx(1)
    assert complete_control["maximum_amplitude_error"] < 1e-12
    assert not complete_control["untouched_word_cube_enumerated"]
    assert len({(tuple(b["pointers"]), tuple(b["syndrome"])) for b in branches}) == len(branches)
    for b in branches:
        rank = len(b["pivots"])
        correct = Fraction(1, 3**(len(acquisition.active)-len(acquisition.supports)+rank))
        incorrect = Fraction(1, 3**(acquisition.source.inputs-len(acquisition.supports)+rank))
        assert Fraction(b["raw_branch_probability"]) == correct != incorrect
        assert b["measured_probability"] == pytest.approx(float(correct))
        assert b["resources"]["all_pointer_and_syndrome_outcomes_accepted"]
        assert not b["resources"]["unused_original_registers_measured_or_discarded"]


def test_retained_logical_registers_can_be_entangled_not_IID_native_outputs(complete_control):
    assert complete_control["minimum_first_register_purity"] < 0.5
    assert not complete_control["entangled_calibration_is_population_or_speedup_evidence"]
    zero = physical_control(acquire(), (0,))
    assert zero["minimum_first_register_purity"] == pytest.approx(1)


def test_pointer_dependent_outer_rank_and_retained_width_keep_all_source_mass():
    # Actual native label calibration: first three supports have zero low row;
    # the last zero-curvature triple's tangent varies with its two pointers.
    pairs = [(3*(i % 3), int(i >= 12)+3*((i+1) % 3)) for i in range(16)]
    source = native_source([[inverse_frequency_coordinates(a,c,6)] for a,c in pairs],6)
    acquisition = PacketAcquisition.from_source(source,4,tuple(f"variable-rank-{i}" for i in range(16)),16)
    replay = physical_control(acquisition,(1,))
    assert len(acquisition.active) == 6
    assert replay["complete_active_words_replayed"] == 729
    branches = replay["all_measurement_branches"]
    assert Counter(len(b["pivots"]) for b in branches) == {0:3,1:18}
    assert Counter(len(b["free"]) for b in branches) == {4:3,3:18}
    assert sum(Fraction(b["raw_branch_probability"]) for b in branches) == 1
    assert replay["total_raw_probability"] == pytest.approx(1)
    assert replay["maximum_amplitude_error"] < 1e-12


def test_packet_payload_aliases_highest_secret_digit_but_untouched_states_need_not():
    acquisition = acquire()
    branch = acquisition.branch((0,)*len(acquisition.pointers))
    qp = branch.packet.phase_modulus//3
    for z in product(range(3), repeat=branch.packet.retained):
        value = branch.original_residual(z)[0]
        assert (3*qp*value) % acquisition.source.modulus == 0
        assert np.exp(2j*np.pi*value/qp) == pytest.approx(np.exp(2j*np.pi*(1+qp)*value/qp))
    # Actual untouched input frequencies can still distinguish s from s+q/3.
    assert any(any(a[0] % 3 for a in acquisition.source.frequencies[i]) for i in acquisition.unused)
    assert not branch.resources()["highest_parent_secret_digit_lost_from_untouched_original_registers"]


@pytest.mark.parametrize("n,r", [(2, 3), (8, 5), (32, 7), (128, 9)])
def test_retention_ledgers_do_not_recurse_joint_packets_as_native_samples(n, r):
    ledger = retention_ledger(n, r, 2*n)
    assert ledger["original_native_input_cap_required"] == 2*n*(n+1)**2
    assert ledger["retained_joint_logical_registers_lower_bound"] == n
    assert ledger["native_additive_degree_upper_bound"] == 2*r-1
    assert not ledger["full_depth_cost_obtained_by_repeating_this_ledger"]
    assert not ledger["joint_outputs_are_fresh_native_samples"]


@pytest.mark.parametrize("mutation", ["cap", "duplicate", "missing", "empty", "odd_level", "forged_frequencies", "too_few", "wrong_window", "bool_count", "empty_source"])
def test_source_gate_rejects_unaccounted_or_invalid_acquisition(mutation):
    source = random_even_source(1, 6, 16, 88401)
    K, cap, ids = 4, 16, tuple(f"id-{i}" for i in range(16))
    if mutation == "cap": cap = 15
    elif mutation == "duplicate": ids = ("same",)*16
    elif mutation == "missing": ids = ids[:-1]
    elif mutation == "empty": ids = ("",)+ids[1:]
    elif mutation == "odd_level": source = replace(source, level=5)
    elif mutation == "forged_frequencies": source = replace(source, frequencies=(((0,), (0,)),)*16)
    elif mutation == "too_few": K = 1
    elif mutation == "wrong_window": K = 3
    elif mutation == "bool_count": K = True
    elif mutation == "empty_source": source = replace(source,labels=())
    with pytest.raises(ValueError):
        PacketAcquisition.from_source(source, K, ids, cap)


def test_strict_outcomes_and_bounded_dense_replay():
    acquisition = acquire()
    for pointers in ((True,), (3,), (), (0, 0)):
        with pytest.raises(ValueError): acquisition.branch(pointers)
    frame = acquisition.branch((0,)).packet
    for y in ((True,)*len(frame.pivots), (3,)*len(frame.pivots), (0,)*(len(frame.pivots)+1)):
        with pytest.raises(ValueError): acquisition.branch((0,), y)
    wide = acquire(2, 6, 10, 88408)
    with pytest.raises(ValueError, match="nine qutrits"):
        physical_control(wide, (1, 2))


def test_live_artifact_independent_crosscheck_and_derivation_pin():
    import hashlib
    report = json.loads(REPORT.read_text())
    assert report["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    checker = DERIVATION.parent / "certificates/ternary_correlated_packet_acquisition_crosscheck.js"
    result = subprocess.run(["node", str(checker), str(REPORT)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["completeActiveWords"] == 243


@pytest.mark.parametrize("mutation", ["supply", "probability", "phase", "IID", "unused", "decoder", "missing_branch"])
def test_independent_verifier_rejects_false_phases_counts_or_promotions(tmp_path, mutation):
    report = json.loads(REPORT.read_text())
    dense = report["dense_original_instrument_control"]
    branch = dense["all_measurement_branches"][0]
    if mutation == "supply": dense["source"]["acquired_original_native_inputs"] -= 1
    elif mutation == "probability": branch["raw_branch_probability"] = "1"
    elif mutation == "phase": branch["logical_residual_frequencies"][1][0] = (branch["logical_residual_frequencies"][1][0]+1) % 9
    elif mutation == "IID": branch["resources"]["outputs_certified_as_IID_native_samples"] = True
    elif mutation == "unused": branch["resources"]["unused_original_registers_measured_or_discarded"] = True
    elif mutation == "decoder": report["novel_algorithm_or_quantum_speedup_claimed"] = True
    elif mutation == "missing_branch": dense["all_measurement_branches"].pop()
    target = tmp_path / "mutated.json"
    target.write_text(json.dumps(report))
    checker = DERIVATION.parent / "certificates/ternary_correlated_packet_acquisition_crosscheck.js"
    result = subprocess.run(["node", str(checker), str(target)], capture_output=True, text=True)
    assert result.returncode != 0
