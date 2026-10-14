"""Known-preparation source legality, literal adaptive laws and finite precision."""
from itertools import product
import inspect
import json
import random
import subprocess

from flint import fmpq
import numpy as np
import pytest

from theorems.known_preparation_packet_simulation import (
    ACCESS, REPORT, KnownPhasePacket, adaptive_law_control, adaptive_sample_control,
    binary_merge, born_boxes, certified_categorical, common_index_merge,
    known_diagonal, known_source_packets, project_binary, raw_source_fixture,
    readout, simulation_budget,
)
from native_noisy_phase_input import prepare_inputs
from ternary_cyclic_extractor import apply_cycle_basis
from ternary_noise_degradation import NoisyLinearRecord


@pytest.mark.parametrize("digits", (1, 2, 16, 64))
def test_source_receipts_reconstruct_actual_classical_preparation_without_secret_or_errors(digits):
    packets, receipt = raw_source_fixture(3, digits, 4, 18000+digits)
    q = 3**digits
    originals = [NoisyLinearRecord(tuple(map(int, r["label"])), int(r["value"]), int(r["modulus"]), r["source_id"]) for r in receipt["original_classical_records"]]
    actual = prepare_inputs(originals, tuple(map(int, receipt["preparation_random_mask"])), "1/2")
    for packet, recipe in zip(packets, actual.reduction_side_recipes):
        assert packet.phase_numerators == (0,)+recipe["known_phase_values"]
        assert packet.modulus == q and len(packet.original_sources) == 2
    assert not receipt["source_error_law_required_for_simulation"]
    assert not receipt["source_states_or_hidden_secret_read"]
    assert "secret" not in inspect.signature(known_source_packets).parameters


@pytest.mark.parametrize("size", (2, 3, 4))
@pytest.mark.parametrize("digits", (1, 2, 3))
def test_every_measured_common_index_branch_matches_literal_known_point_quantum_gate(size, digits):
    packets, _ = raw_source_fixture(2, digits, size, 18100+size+digits)
    original = np.ones(1, complex)
    for p in packets:
        original = np.kron(original, p.forward_vector())
    quantum = apply_cycle_basis(original, (1,)*size).reshape((3,)*size)
    for tail in product(range(3), repeat=size-1):
        packet, record = common_index_merge(packets, tail)
        projected = quantum[(slice(None),)+tail]
        probability = float(np.vdot(projected, projected).real)
        assert abs(probability-3**(1-size)) < 1e-12
        assert np.max(abs(packet.forward_vector()-projected/np.sqrt(probability))) < 1e-12
        assert record["exact_branch_probability_compact"] == {"base": 3, "exponent": 1-size}
        assert not record["dense_3_to_the_block_size_table_built"]


def test_large_merge_updates_only_three_exact_phases_with_no_underflow_or_tensor_cube():
    packets = [KnownPhasePacket(3**64, (0, i, 2*i), (f"large-{i}",)) for i in range(1000)]
    child, _ = common_index_merge(packets, (0,)*999)
    assert child.phase_numerators == (0, sum(range(1000)), 2*sum(range(1000)))
    assert len(child.original_sources) == 1000


def test_mixed_root_embeddings_preserve_full_actual_point_phases():
    left = KnownPhasePacket(9, (1, 2, 5), ("a",))
    right = KnownPhasePacket(27, (2, 4, 8), ("b",))
    child, _ = common_index_merge((left, right), (1,))
    assert child.modulus == 27
    assert child.phase_numerators == tuple((3*left.phase_numerators[t]+right.phase_numerators[(t+1) % 3]) % 27 for t in range(3))


@pytest.mark.parametrize("digits", (1, 2, 16, 64))
def test_projection_and_both_binary_signs_match_actual_CNOT_for_noisy_known_point_data(digits):
    originals, _ = raw_source_fixture(2, digits, 2, 18200+digits)
    packets = []
    for original in originals:
        binary, probability = project_binary(original)
        assert probability == fmpq(2, 3)
        assert np.max(abs(binary.forward_vector()-original.forward_vector()[:2]/np.sqrt(2/3))) < 1e-12
        packets.append(binary)
    U = np.eye(4)[[0, 1, 3, 2]]
    actual = (U@np.kron(packets[0].forward_vector(), packets[1].forward_vector())).reshape(2, 2)
    for bit in (0, 1):
        child, probability = binary_merge(*packets, bit)
        assert probability == fmpq(1, 2)
        assert np.max(abs(child.forward_vector()-actual[:, bit]*np.sqrt(2))) < 1e-12


@pytest.mark.parametrize("digits", (1, 2, 16, 64))
@pytest.mark.parametrize("kind", ("inverse_F3", "anti_trine"))
def test_exact_rational_Born_boxes_enclose_physical_local_instruments(digits, kind):
    packets, _ = raw_source_fixture(2, digits, 1, 18300+digits)
    packet = packets[0] if kind == "inverse_F3" else project_binary(packets[0])[0]
    if kind == "inverse_F3":
        U = np.exp(-2j*np.pi*np.outer(np.arange(3), np.arange(3))/3)/np.sqrt(3)
    else:
        U = np.column_stack((np.ones(3), -np.exp(-2j*np.pi*np.arange(3)/3)))/np.sqrt(3)
    probabilities = abs(U@packet.forward_vector())**2
    for p, (lo, hi) in zip(probabilities, born_boxes(packet, kind, 24)):
        assert float(lo)-1e-12 <= p <= float(hi)+1e-12
        assert hi-lo <= fmpq(1, 2**24)


def test_complete_72_path_adaptive_channel_matches_literal_quantum_operations():
    control = adaptive_law_control()
    packets, _ = raw_source_fixture(2, 2, 4, 17002)
    first = apply_cycle_basis(np.kron(packets[0].forward_vector(), packets[1].forward_vector()), (1, 1)).reshape(3, 3)
    F = np.exp(-2j*np.pi*np.outer(np.arange(3), np.arange(3))/3)/np.sqrt(3)
    V = np.column_stack((np.ones(3), -np.exp(-2j*np.pi*np.arange(3)/3)))/np.sqrt(3)
    CNOT = np.eye(4)[[0, 1, 3, 2]]
    total = 0.
    for row in control["paths"]:
        v, f = row["complement"], row["first_F3_outcome"]
        conditional = first[:, v]*np.sqrt(3)
        diagonal = np.exp(2j*np.pi*np.array([0, v, v*v])/3)
        p_f = abs((F@(diagonal*conditional))[f])**2
        if row["terminal"] == "LEFT_PROJECTION_REJECT":
            probability = p_f/9
        elif row["terminal"] == "RIGHT_PROJECTION_REJECT":
            probability = 2*p_f/27
        else:
            pair = np.kron(packets[2].forward_vector()[:2], packets[3].forward_vector()[:2])*(3/2)
            actual = (CNOT@pair).reshape(2, 2)[:, row["binary_complement"]]*np.sqrt(2)
            actual *= np.array([1, np.exp(2j*np.pi*f/3)])
            p_last = abs((V@actual)[row["anti_trine_outcome"]])**2
            probability = 2*p_f*p_last/27
        lo, hi = map(fmpq, row["joint_probability_box"])
        assert float(lo)-1e-12 <= probability <= float(hi)+1e-12
        total += probability
    assert len(control["paths"]) == 72 and abs(total-1) < 1e-12
    assert fmpq(control["lower_total"]) <= 1 <= fmpq(control["upper_total"])
    assert not control["public_controller_reads_private_phase_values"]
    assert not control["counterfactual_paths_are_simultaneous_physical_outputs"]


class FixedBits:
    def __init__(self, bits, value):
        self.bits, self.value = bits, value
    def getrandbits(self, width):
        assert width == self.bits
        return self.value


@pytest.mark.parametrize("bits", (4, 8))
@pytest.mark.parametrize("probabilities", (("1/3", "1/3", "1/3"), ("1/10", "1/5", "7/10"), ("2/3", "1/3")))
def test_all_dyadic_coin_cells_satisfy_unconditional_error_and_abort_bound(bits, probabilities):
    p = tuple(map(fmpq, probabilities))
    counts = [0]*(len(p)+1)
    for prefix in range(2**bits):
        r = certified_categorical(lambda k: tuple((x, x) for x in p), len(p), FixedBits(bits, prefix), max_bits=bits, block_bits=bits)
        counts[-1 if r["outcome"] is None else r["outcome"]] += 1
        assert not r["conditional_on_no_abort_is_the_exact_channel"]
    empirical = [fmpq(c, 2**bits) for c in counts]
    total_variation = sum(abs(a-b) for a, b in zip(empirical, p+(fmpq(0),)))/2
    assert total_variation <= empirical[-1] <= min(fmpq(1), fmpq(8, 2**bits))
    if bits == 4 and probabilities == ("1/10", "1/5", "7/10"):
        assert empirical[-1] > 0
        assert tuple(x/(1-empirical[-1]) for x in empirical[:-1]) != p


def test_precision_cap_aborts_an_unresolved_boundary_instead_of_conditioning_it_away():
    r = certified_categorical(lambda bits: ((fmpq(1, 3), fmpq(1, 3)),)*3, 3, FixedBits(8, 85), max_bits=8, block_bits=8)
    assert r["status"] == "EXPLICIT_COIN_PRECISION_ABORT" and r["outcome"] is None
    assert r["random_bits_read"] == 8


@pytest.mark.parametrize("calls", (1, 16, 2**64, 2**128))
@pytest.mark.parametrize("failure_bits", (1, 24, 64))
def test_adaptive_hybrid_budget_charges_all_calls(calls, failure_bits):
    r = simulation_budget(calls, failure_bits)
    assert fmpq(r["adaptive_unconditional_transcript_error_upper"]) == fmpq(8*calls, 2**r["per_call_precision_bits"])
    assert fmpq(r["adaptive_unconditional_transcript_error_upper"]) <= fmpq(1, 2**failure_bits)
    assert not r["conditioning_away_abort_allowed"]
    assert not r["arbitrary_wide_quantum_circuit_covered"] and not r["unknown_quantum_only_source_covered"]


@pytest.mark.parametrize("digits", (1, 2, 16, 64))
def test_live_certified_adaptive_workflow_keeps_source_access_and_precision_explicit(digits):
    r = adaptive_sample_control(digits, 17100+digits)
    assert r["status"] == "CERTIFIED_ADAPTIVE_TRANSCRIPT"
    assert r["source"]["phase_access"] == ACCESS
    assert len(r["transcript"]) <= int(r["budget"]["max_stochastic_calls"])
    assert not r["classical_hidden_secret_used"] and not r["unknown_quantum_input_simulated"]
    for step in r["transcript"]:
        assert step["sampling"]["status"] == "CERTIFIED_OUTCOME"


def test_unmeasured_entanglement_is_a_real_boundary_not_covered_by_product_packets():
    bell = np.array([1, 0, 0, 1])/np.sqrt(2)
    X = np.array([[0, 1], [1, 0]])
    actual = np.vdot(bell, np.kron(X, X)@bell).real
    false_product = np.eye(4)/4
    assert abs(actual-1) < 1e-12
    assert abs(np.trace(false_product@np.kron(X, X))) < 1e-12
    assert np.sum(abs(np.linalg.eigvalsh(np.outer(bell, bell)-false_product)))/2 > .7


@pytest.mark.parametrize("call", (
    lambda: KnownPhasePacket(9, (0, 1), ("a",), access="UNKNOWN_QUANTUM_ONLY_SOURCE"),
    lambda: KnownPhasePacket(9, (0, 1), ("a", "a")),
    lambda: KnownPhasePacket(9, (True, 1), ("a",)),
    lambda: common_index_merge((KnownPhasePacket(9, (0, 1, 2), ("a",)),)*2, (0,)),
    lambda: common_index_merge((KnownPhasePacket(9, (0, 1, 2), ("a",)),), (0,)),
    lambda: binary_merge(KnownPhasePacket(9, (0, 1), ("a",)), KnownPhasePacket(9, (0, 1), ("a",)), 0),
    lambda: born_boxes(KnownPhasePacket(9, (0, 1), ("a",)), "unmeasured_wide_unitary", 8),
    lambda: certified_categorical(lambda bits: ((fmpq(0), fmpq(0)),)*3, 3, random.Random(1)),
    lambda: simulation_budget(0),
))
def test_illegal_source_access_reuse_and_uncovered_primitives_fail_closed(call):
    with pytest.raises(ValueError):
        call()


def test_independent_known_source_and_exact_adaptive_transcript_replay():
    out = subprocess.run(["node", str(REPORT.parents[1]/"certificates/known_preparation_packet_simulation_crosscheck.js")], capture_output=True, text=True, check=True)
    r = json.loads(out.stdout)
    assert r["status"] == "PASS" and r["complete_adaptive_paths"] == 72
    assert r["certified_sample_controls"] == 4
    assert not r["unknown_quantum_only_source_dequantized"]


@pytest.mark.parametrize("mutation", ("phase", "mask", "raw_value", "coin", "interval", "cdf", "path", "copies", "scope", "abort"))
def test_checker_rejects_phase_leaks_false_precision_and_universal_promotion(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    c = r["certified_sample_controls"][1]
    if mutation == "phase":
        packet = c["source"]["known_source_receipts"][0]["packet"]
        packet["phase_numerators"][1] = str((int(packet["phase_numerators"][1])+1) % int(packet["modulus"]))
    elif mutation == "mask":
        c["source"]["preparation_random_mask"][0] = (int(c["source"]["preparation_random_mask"][0])+1) % 9
    elif mutation == "raw_value":
        c["source"]["original_classical_records"][0]["value"] = (int(c["source"]["original_classical_records"][0]["value"])+1) % 9
    elif mutation == "coin":
        c["transcript"][0]["sampling"]["decisions"][0]["coin_prefix"] = "999999"
    elif mutation == "interval":
        c["transcript"][2]["sampling"]["decisions"][0]["probability_boxes"][0] = ["0", "1"]
    elif mutation == "cdf":
        c["transcript"][0]["sampling"]["outcome"] = (c["transcript"][0]["sampling"]["outcome"]+1) % 3
    elif mutation == "path":
        r["complete_adaptive_law_control"]["paths"][0]["joint_probability_box"] = ["1", "1"]
    elif mutation == "copies":
        c["source"]["original_record_count"] -= 1
    elif mutation == "scope":
        r["unknown_HSP_phase_source_dequantized"] = True
    else:
        c["budget"]["conditioning_away_abort_allowed"] = True
    target = tmp_path/"forged.json"
    target.write_text(json.dumps(r))
    out = subprocess.run(["node", str(REPORT.parents[1]/"certificates/known_preparation_packet_simulation_crosscheck.js"), str(target)], capture_output=True)
    assert out.returncode != 0
