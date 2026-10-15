"""Coherent packet, public lattice instrument and unknown-register falsifiers."""
from copy import copy, deepcopy
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess

import numpy as np
import pytest
from qiskit.quantum_info import Statevector

from theorems.lattice_sine_packet import compile_packet, packet_plan, DyadicField, exact_affinity
from theorems.lattice_sine_window_source import (
    SineWindowSource, SinePhysicalBackend, compile_source, exact_reference,
    audit_template, simulate_batch, audit_batch, promise_budget, resource_estimate,
)
from theorems.lattice_qft_precision import CircuitResourcePolicy, QFTUsage, precision_plan


ROOT = Path(__file__).resolve().parents[1]
HARDER_CONTROL = SineWindowSource(((17, 0), (16, 1)), 7, 1, 0, 2, 4)


def value(poly, root):
    return sum(float(Fraction(x)) * np.exp(2j * np.pi * i / root)
               for i, x in enumerate(reversed(poly)))


@pytest.mark.parametrize("bits", range(1, 7))
def test_known_parent_packet_has_positive_amplitudes_and_clean_flag(bits):
    packet = compile_packet(bits)
    K = 1 << bits
    actual = Statevector.from_instruction(packet.circuit).data
    expected = np.zeros_like(actual)
    expected[:K] = np.sqrt(2 / K) * np.sin(np.pi * np.arange(K) / K)
    np.testing.assert_allclose(actual, expected, atol=5e-14, rtol=0)
    assert packet.plan["postselection_used"] is False
    assert packet.plan["known_zero_parent_success_probability"] == "1"


def test_packet_is_unitary_with_clean_AND_work_but_not_universal_flag_reset():
    p = compile_packet(3)
    state = np.zeros(1 << p.circuit.num_qubits, complex)
    state[:16] = np.exp(0.37j * np.arange(16)) / 4
    output = Statevector(state.copy()).evolve(p.circuit)
    np.testing.assert_allclose(output.data[16:], 0, atol=2e-14)
    assert np.sum(abs(output.data[8:16]) ** 2) > 0.1
    np.testing.assert_allclose(output.evolve(p.circuit.inverse()).data, state, atol=2e-14)


@pytest.mark.parametrize("bits", [1, 4, 32, 64])
def test_packet_resources_and_parameter_error_are_explicit(bits):
    p = compile_packet(bits)
    assert len(p.circuit.data) == 11 * bits + 9
    assert p.circuit.num_qubits == 2 * bits
    assert p.circuit.count_ops().get("ccx", 0) == 2 * (bits - 1)
    weight = Fraction(33, 4) - Fraction(7, 1 << bits)
    plan = p.plan
    encoded = Fraction(plan["encoded_binary64_pi"])
    err = max(abs(encoded - Fraction(plan["pi_lower"])), abs(encoded - Fraction(plan["pi_upper"])))
    assert Fraction(plan["retained_absolute_pi_weight"]) == weight
    assert Fraction(plan["encoded_rotation_operator_error_upper"]) == weight * err
    assert plan["hardware_synthesis_or_simulator_roundoff_certified"] is False


def test_packet_and_reference_caps_are_unknown_not_no_go():
    with pytest.raises(ValueError, match="UNKNOWN"):
        compile_packet(1023)
    with pytest.raises(ValueError, match="UNKNOWN"):
        compile_packet(8, CircuitResourcePolicy(max_qubits=4))
    with pytest.raises(ValueError, match="UNKNOWN"):
        exact_reference(SineWindowSource(((1,),), 7, 1, 0, 128, 4))


@pytest.mark.parametrize("K", [2, 4, 8, 16, 32, 64])
def test_exact_affinities_match_independent_convolution_and_quadratic_bound(K):
    F = DyadicField(2 * K)
    psi = np.sqrt(2 / K) * np.sin(np.pi * np.arange(K) / K)
    for d in range(-K, K + 1):
        got = exact_affinity(K, d, F)
        expected = sum(psi[x] * psi[x - d] for x in range(K) if 0 <= x - d < K)
        np.testing.assert_allclose(F.value(got), expected, atol=2e-14)
        assert got == exact_affinity(K, -d, F)
        assert -2e-14 <= F.value(got).real <= 1 + 2e-14
        assert 1 - F.value(got).real <= np.pi**2 * d**2 / (2 * K**2) + 2e-14
        if abs(d) >= K - 1:
            assert got == F.zero()
    assert exact_affinity(K, 0, F) == F.scalar(1)


@pytest.mark.parametrize("basis", [((1,),), ((-1,),)])
def test_public_evaluator_adds_into_arbitrary_Y_preserving_complex_phase(basis):
    source = SineWindowSource(basis, 3, 1, 0, 2, 2)
    c = compile_source(source)
    width = len(c.outputs[0])
    vector = np.zeros(1 << c.evaluator.num_qubits, complex)
    expected = np.zeros_like(vector)
    for b, a in product(range(2), repeat=2):
        y = (3 * b + a - 2) % (1 << width)
        inputs = b + 2 * a
        amplitude = (1j ** (b + 2 * a)) / 2
        vector[inputs + (y << 2)] = amplitude
        out = (y + source.point(b, (a,))[0]) % (1 << width)
        expected[inputs + (out << 2)] = amplitude
    result = Statevector(vector).evolve(c.evaluator)
    np.testing.assert_allclose(result.data, expected, atol=1e-13)
    np.testing.assert_allclose(result.evolve(c.evaluator.inverse()).data, vector, atol=1e-13)


def test_full_parent_uses_inplace_cyclic_QFT_and_retains_only_localization():
    s = SineWindowSource(((1,),), 3, 1, 0, 2, 2)
    c = compile_source(s)
    output = Statevector.from_instruction(c.coherent_parent)
    expected = np.zeros_like(output.data)
    for b, a, k in product(range(2), range(2), range(4)):
        y = s.point(b, (a,))[0] + 1  # K=2 packet is exactly |1>.
        index = b + 2 * (k & 1) + (y << 2)
        if k & 2:
            index += 1 << c.coherent_parent.find_bit(c.padding[0]).index
        expected[index] = np.exp(2j * np.pi * k * a / 4) / 4
    np.testing.assert_allclose(output.data, expected, atol=2e-13)
    np.testing.assert_allclose(output.evolve(c.coherent_parent.inverse()).data[0], 1, atol=2e-13)
    assert c.position_wires[0] == c.input_register[1]
    record = c.resource_record()
    assert record["mixed_colour_inverse_available"] is False
    assert record["full_parent_inverse_requires_localization_and_label_registers"] is True


@pytest.fixture(scope="module")
def reference():
    return exact_reference(HARDER_CONTROL)


def test_complete_Gram_and_every_cyclic_label_match_nontrivial_template(reference):
    R = reference["reference_root"]
    gram = np.array([[value(x, R) for x in row] for row in reference["complete_public_Gram"]])
    np.testing.assert_allclose(gram, gram.conj().T, atol=1e-14)
    assert np.linalg.eigvalsh(gram).min() >= -1e-14
    np.testing.assert_allclose(np.trace(gram), 1, atol=1e-14)
    audit = audit_template(HARDER_CONTROL, reference, (1, -1))
    assert audit["finite_marginal_template_matches"] is True
    assert audit["PRIVATE_AUDIT_ONLY_parent_shift"] == (0, -1)
    assert audit["PRIVATE_AUDIT_ONLY_cyclic_shift"] == 12
    assert audit["exact_marginal_visibility"] == ("1/4",)
    for row in reference["all_label_outcomes"]:
        assert row["joint_label_probability"] == ("1/16",)
        rho = np.array([[value(x, R) for x in r] for r in row["unnormalized_colour_density"]]) * 16
        assert np.linalg.eigvalsh(rho).min() >= -1e-14
        np.testing.assert_allclose(np.trace(rho @ rho), 17 / 32, atol=1e-14)
    # A tensor QFT would omit the carry-dependent phases of a cyclic shift.
    off = reference["all_label_outcomes"][1]["unnormalized_colour_density"][0][1]
    np.testing.assert_allclose(value(off, R), 1j / 128, atol=1e-14)


def test_aliases_and_wrong_residue_are_falsifiers_not_trial_selectors():
    alias = SineWindowSource(((1,),), 3, 1, 0, 2, 4)
    result = audit_template(alias, exact_reference(alias), (1,))
    assert result["status"] == "ALIASES_OR_MODEL_MISMATCH"
    wrong = SineWindowSource(((1,),), 7, 2, 0, 2, 4)
    result = audit_template(wrong, exact_reference(wrong), (1,))
    assert result["status"] == "WRONG_TRIAL_NOT_A_PROMISED_SOURCE"
    assert result["correct_trial_flag_given_to_receiver"] is False


def test_public_promise_budget_separates_assumptions_and_cross_colour_alias():
    s = SineWindowSource(((1,),), 5, 1, 0, 32, 4)
    budget = promise_budget(s, 1, 1, 8)
    # p^2>K^2 is insufficient: (p-1)^2 == K^2 is not the promised strict bound.
    assert budget["nonparallel_aliases_excluded_IF_promises_hold"] is True
    assert budget["parallel_cross_colour_aliases_excluded_IF_promises_hold"] is False
    assert budget["short_vector_norm_gap_and_correct_trial_are_unverified_assumptions"] is True
    assert budget["efficient_robust_receiver_supplied"] is False


@pytest.fixture(scope="module")
def compiled_batch(reference):
    c = compile_source(HARDER_CONTROL)
    batch = simulate_batch(c, shots=4, seed=40102, batch_tag="source-test")
    assert audit_batch(HARDER_CONTROL, reference, batch)["all_emitted_conditional_densities_agree"]
    return batch


def test_actual_unknown_registers_are_charged_mixed_and_localization_private(compiled_batch):
    batch = compiled_batch
    assert batch.metadata["actual_compiled_source_preparations_charged"] == 4
    assert batch.metadata["W_calls_charged"] == 24
    assert batch.metadata["conditioned_snapshot_keys_and_multiplicities_checked"] is True
    assert all(r.measured_cells == () for r in batch.receipts)
    assert all(np.trace(r @ r).real < 0.6 for r in batch._densities.values())
    backend = SinePhysicalBackend(batch, seed=21)
    first, second = batch.receipts[:2]
    assert "density" not in backend.public_view(first.id)
    result = backend.merge(first.id, second.id)
    child = result["output"]
    assert set(child["original_source_receipts"]) == {first.id, second.id}
    with pytest.raises(ValueError):
        backend.measure(first.id)
    for copier in (copy, deepcopy):
        with pytest.raises(ValueError):
            copier(backend)
    with pytest.raises(ValueError):
        SinePhysicalBackend(batch)


def test_approximate_instrument_has_its_own_reference_not_an_exact_DCP_promise():
    plan = precision_plan(4, usage=QFTUsage(direct_forward_calls=2), cutoff=0)
    compiled = compile_source(HARDER_CONTROL, plan)
    batch = simulate_batch(compiled, shots=2, seed=40103, batch_tag="cutoff-test")
    ref = exact_reference(HARDER_CONTROL, qft_cutoff=0)
    assert audit_batch(HARDER_CONTROL, ref, batch)["all_emitted_conditional_densities_agree"]
    assert batch.metadata["logical_readout_QFT_is_exact_reference"] is False
    assert audit_template(HARDER_CONTROL, ref, (1, -1))["finite_marginal_template_matches"] is False
    with pytest.raises(ValueError, match="matching QFT"):
        audit_batch(HARDER_CONTROL, exact_reference(HARDER_CONTROL), batch)
    # Physical operations remain legal even when no exact-DCP promise is given.
    backend = SinePhysicalBackend(batch)
    assert backend.measure(batch.receipts[0].id)["outcome"] in (0, 1)


def test_backend_rejects_disclosed_localization_or_invalid_labels():
    s = SineWindowSource(((1,),), 3, 1, 0, 2, 2)
    for label, cells in ((4, ()), (True, ()), (0, ((1,),))):
        batch = simulate_batch(compile_source(s), shots=1, seed=22)
        batch.receipts = (replace(batch.receipts[0], label=label, measured_cells=cells),)
        with pytest.raises(ValueError, match="canonical labels"):
            SinePhysicalBackend(batch)


def test_large_source_compiles_without_exponential_packet_table_or_simulation():
    s = SineWindowSource(((10000, 1000), (9999, 1000)), 389, 1, 0, 256, 128)
    c = compile_source(s)
    record = c.resource_record()
    assert record["compiled_qubits"] == resource_estimate(s)["total_source_qubits"] == 151
    with pytest.raises(ValueError, match="UNKNOWN"):
        simulate_batch(c, shots=1)


def test_label_projection_then_full_inverse_pays_its_Born_mass():
    c = compile_source(SineWindowSource(((1,),), 3, 1, 0, 2, 2))
    state = Statevector.from_instruction(c.coherent_parent).data
    mask = sum(1 << c.coherent_parent.find_bit(q).index for q in c.position_wires)
    projected = state.copy()
    projected[[bool(i & mask) for i in range(len(state))]] = 0
    mass = np.vdot(projected, projected).real
    np.testing.assert_allclose(mass, 1 / 4, atol=1e-13)
    undone = Statevector(projected / np.sqrt(mass)).evolve(c.coherent_parent.inverse())
    np.testing.assert_allclose(abs(undone.data[0]) ** 2, mass, atol=1e-13)


def test_compilation_and_sampling_do_not_call_dense_reference_or_private_template(monkeypatch):
    import theorems.lattice_sine_window_source as module
    def forbidden(*args, **kwargs):
        raise AssertionError("private/dense diagnostic entered physical preparation")
    monkeypatch.setattr(module, "exact_reference", forbidden)
    monkeypatch.setattr(module, "audit_template", forbidden)
    compiled = module.compile_source(SineWindowSource(((1,),), 7, 1, 0, 2, 4))
    assert len(module.simulate_batch(compiled, 1, 110).receipts) == 1


def test_approximate_QFT_usage_is_not_free_or_unlimited():
    c = compile_source(HARDER_CONTROL, precision_plan(4, cutoff=0))
    with pytest.raises(ValueError, match="QFT_QUERY_BUDGET_EXCEEDED"):
        simulate_batch(c, shots=2)
    r = c.resource_record()
    assert Fraction(r["packet_and_retained_QFT_parameter_operator_upper_per_parent"]) < Fraction(1, 10**12)
    assert r["packet_and_QFT_operator_upper_relative_to_ideal_full_QFT"] == "2"


def test_independent_JS_replays_live_artifact():
    proc = subprocess.run(["node", str(ROOT / "research/certificates/lattice_sine_window_source_crosscheck.js")],
                          capture_output=True, text=True, check=True)
    report = json.loads(proc.stdout)
    assert report["verified"] is True
    assert report["source_preparations"] == 34


@pytest.mark.parametrize("tamper", ["gram", "density", "visibility", "packet", "label", "precision", "cutoff", "claim"])
def test_independent_JS_rejects_corrupted_physics_or_claims(tmp_path, tamper):
    report = json.loads((ROOT / "research/phase_workbench/lattice_sine_window_source.json").read_text())
    c = report["actual_source_controls"][2]
    if tamper == "gram":
        c["exact_reference"]["complete_public_Gram"][0][0] = ["1"]
    elif tamper == "density":
        c["exact_reference"]["all_label_outcomes"][0]["unnormalized_colour_density"][0][1] = ["1"]
    elif tamper == "visibility":
        c["private_template_audit"]["exact_marginal_visibility"] = ["1"]
    elif tamper == "packet":
        c["compiled_resources"]["closed_resources"]["packet_plan"]["CCX_gates"] += 1
    elif tamper == "label":
        c["actual_sampling_audit"]["public_receipts"][0]["measured_cells"] = [[1, 2]]
    elif tamper == "precision":
        c["compiled_resources"]["packet_and_QFT_operator_upper_relative_to_ideal_full_QFT"] = "0"
    elif tamper == "cutoff":
        report["approximate_instrument_control"]["private_template_audit"]["finite_marginal_template_matches"] = True
    else:
        report["accepted_speedup_candidate"] = True
    target = tmp_path / "tampered.json"
    target.write_text(json.dumps(report))
    proc = subprocess.run(["node", str(ROOT / "research/certificates/lattice_sine_window_source_crosscheck.js"), str(target)],
                          capture_output=True, text=True)
    assert proc.returncode != 0
