import copy
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace

from flint import nmod_mat
import numpy as np
import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates
from ternary_carry_packets import compile_packet
from ternary_packet_line_receiver import (
    REPORT, complete_packet_audit, coupling_certificate, direction_certificate,
    exact_fraction_string, gaussian_binomial, packet_data, physical_line_receiver, population_gate,
    line_compilation, physical_compilation,
)
from ternary_quadratic_program_receiver import nullspace, teleport_tensor


def coupled(syndrome=(0,)):
    return compile_packet(tuple((inverse_frequency_coordinates(1, 2, 3),) for _ in range(3)), 3, syndrome)


def parse_fraction(text):
    def decimal(s):
        sign = -1 if s.startswith("-") else 1
        s = s.lstrip("-")
        value = 0
        for start in range(0, len(s), 1000):
            part = s[start:start+1000]
            value = value*10**len(part)+int(part)
        return sign*value
    fields = text.split("/")
    return Fraction(decimal(fields[0]), decimal(fields[1]) if len(fields) == 2 else 1)


def test_actual_native_identity_and_coupled_syndrome_gate_exhaust_all_directions():
    total, good = 0, 0
    for y in product(range(3), repeat=1):
        packet = coupled(y)
        c = coupling_certificate(packet)
        assert c["coupling_mask_rank"] == packet.consumed-1
        audit = complete_packet_audit(packet)
        total += audit["all_direction_shift_pairs_checked"]
        good += bool(audit["admitted_nonzero_directions"])
        if audit["admitted_nonzero_directions"]:
            assert c["original_low_syndrome"] == (0,)
            for direction in audit["direction_certificates"]:
                if direction["affine_for_every_Bell_shift_and_every_secret"]:
                    assert len(direction["physical_support"]) == 3
    assert total == 216 and good == 1


def test_decomposable_native_code_really_escapes_full_support_condition():
    pairs = (((1, 2), (0, 0)), ((2, 4), (0, 0)), ((0, 0), (1, 2)), ((0, 0), (2, 4)))
    labels = tuple(tuple(inverse_frequency_coordinates(*pair, 3) for pair in row) for row in pairs)
    all_admitted = 0
    for y in product(range(3), repeat=2):
        packet = compile_packet(labels, 3, y)
        audit = complete_packet_audit(packet)
        assert not audit["coupling"]["only_constant_diagonal_masks_preserve_kernel"]
        all_admitted += bool(audit["admitted_nonzero_directions"])
    assert all_admitted == 5
    branch = compile_packet(labels, 3, (0, 1))
    admitted = direction_certificate(branch, (1, 0))
    assert admitted["affine_for_every_Bell_shift_and_every_secret"]
    assert len(admitted["physical_support"]) == 2


def test_all_small_full_rank_loop_free_bad_codes_have_idempotent_separator():
    projections = []
    for entries in product(range(3), repeat=4):
        P = nmod_mat([entries[:2], entries[2:]], 3)
        if P*P == P and P.rank() == 1:
            projections.append(P)
    assert len(projections) == gaussian_binomial(2, 1)*3 == 12
    bad = 0
    for entries in product(range(3), repeat=8):
        C = [entries[:4], entries[4:]]
        if nmod_mat(C, 3).rank() != 2 or any(not C[0][i] and not C[1][i] for i in range(4)):
            continue
        columns = nullspace(C, 4)
        D = tuple(zip(*columns))
        A = [[C[l][i]*D[i][j] % 3 for i in range(4)] for l in range(2) for j in range(2)]
        if nmod_mat(A, 3).rank() == 3:
            continue
        bad += 1
        assert any(all(P*nmod_mat([[C[0][i]], [C[1][i]]], 3) in
                       (nmod_mat([[0], [0]], 3), nmod_mat([[C[0][i]], [C[1][i]]], 3)) for i in range(4))
                   for P in projections)
    assert bad > 0


@pytest.mark.parametrize("secret", [(0,), (1,), (2,)])
def test_actual_one_use_Bell_tensor_yields_exact_equations_for_every_outcome(secret):
    result = physical_line_receiver(coupled(), (1, 1), secret)
    assert len(result["all_Bell_branches"]) == 81
    assert result["maximum_physical_residual"] < 4e-12
    assert result["total_raw_Bell_probability"] == pytest.approx(1)
    assert result["one_supplied_program_consumed"]
    assert not result["virtual_branches_are_independent_source_programs"]


def test_nonaffine_and_higher_root_inputs_are_not_admitted_as_exact_field_protocol():
    with pytest.raises(ValueError, match="affine-line"):
        physical_line_receiver(coupled((1,)), (1, 1), (1,))
    with pytest.raises(ValueError, match="nonzero"):
        direction_certificate(coupled(), (0, 0))
    packet = compile_packet(((inverse_frequency_coordinates(1, 2, 5),),)*3, 5)
    with pytest.raises(ValueError, match="level3"):
        packet_data(packet)
    assert complete_packet_audit(coupled(), max_words=8)["status"] == "COMPLETE_PACKET_WORD_CAP_EXHAUSTED"


@pytest.mark.parametrize("width,direction", [(1, (1,)), (2, (1, 2)), (3, (1, 0, 1))])
def test_complete_known_line_compiler_preserves_arbitrary_entangled_packets(width, direction):
    result = physical_compilation(width, direction)
    assert result["maximum_Kraus_amplitude_residual"] < 4e-12
    assert result["total_raw_probability"] == pytest.approx(1)
    compiler = result["compiler"]
    assert not compiler["affine_phase_or_secret_promise_required"]
    assert compiler["same_supplied_packet_consumed"]
    assert compiler["Kraus_squared_coefficient_denominator"] == 3**(width+1)
    assert not compiler["classical_simulation_of_quantum_packet_claimed"]


def test_line_compiler_does_not_import_exact_affine_admission_or_grant_current_shift_selection():
    packet = coupled((1,))
    assert not direction_certificate(packet, (1, 1))["affine_for_every_Bell_shift_and_every_secret"]
    compiler = line_compilation(packet.retained, (1, 1))
    assert not compiler["affine_phase_or_secret_promise_required"]
    assert not compiler["arbitrary_unknown_teleported_data_or_multiple_lines_covered"]


@pytest.mark.parametrize("secret", [1, 2])
def test_nonaffine_rejection_does_not_erase_gated_information(secret):
    packet, v = coupled(), (1, 0)
    assert not direction_certificate(packet, v)["affine_for_every_Bell_shift_and_every_secret"]
    points = tuple(product(range(3), repeat=2))
    index = {z: i for i, z in enumerate(points)}
    data = np.zeros(9, complex)
    for j in range(3):
        data[index[tuple(j*x % 3 for x in v)]] = 1/np.sqrt(3)
    program = SimpleNamespace(width=2, components=1, value=packet.residual)
    tensor, _ = teleport_tensor(program, (secret,), data)
    flat, curved = 0, 0
    for ai, a in enumerate(points):
        phase = [packet.residual(tuple((x+j*y) % 3 for x, y in zip(a, v)))[0] for j in range(3)]
        linear, quadratic = (phase[2]-phase[1]) % 3, 2*sum(phase) % 3
        if quadratic:
            curved += 1
            expected = np.ones(3)/3
        else:
            flat += 1
            expected = np.eye(3)[secret*linear % 3]
        for bi, b in enumerate(points):
            branch = tensor[0, bi, ai]
            correction = sum(x*y for x, y in zip(b, v)) % 3
            child = np.array([branch[index[tuple((x+j*y) % 3 for x, y in zip(a, v))]]
                              *np.exp(2j*np.pi*j*correction/3)*9 for j in range(3)])
            np.testing.assert_allclose(abs(np.fft.fft(child)/np.sqrt(3))**2, expected, atol=4e-12)
    assert flat > 0 and curved > 0


def test_exact_large_rational_serialization_does_not_need_global_guard_changes():
    value = Fraction(2**20000, 3**17000)
    assert parse_fraction(exact_fraction_string(value)) == value
    assert parse_fraction(exact_fraction_string(-value)) == -value


def test_population_bounds_keep_clipping_and_exclude_other_receivers():
    assert population_gate(1, 4)["raw_exact_one_use_line_admission_probability_upper"] == "1"
    previous = Fraction(1)
    for n in (8, 16, 32, 64):
        gate = population_gate(n, 4*n)
        current = parse_fraction(gate["raw_exact_one_use_line_admission_probability_upper"])
        assert Fraction(1, 3**n) <= current < previous
        previous = current
        assert not gate["all_native_quantum_receivers_excluded"]
        assert not gate["multi_program_cubic_cancellation_factory_covered"]
        assert gate["high_label_informed_direction_search_allowed"]


CHECKER = Path(__file__).resolve().parents[1]/"research/certificates/ternary_packet_line_receiver_crosscheck.js"


def test_independent_native_phase_rank_population_and_Bell_replay():
    output = subprocess.run(["node", str(CHECKER)], check=True, capture_output=True, text=True)
    result = json.loads(output.stdout)
    assert result["status"] == "PASS"
    assert result["exact_direction_shift_pairs_checked"] > 8400
    assert result["physical_Bell_branches_checked"] == 243
    assert result["exact_line_Kraus_selector_rows_checked"] == 117
    assert result["arbitrary_packet_line_instrument_compiled"]
    assert not result["general_quantum_receiver_lower_bound"]


@pytest.mark.parametrize("mutation", ["scope", "phase", "gradient", "rank", "admission", "probability", "count", "Bell", "empty", "compiler_support", "compiler_scale", "compiler_scope"])
def test_tampered_access_phase_and_population_records_are_rejected(tmp_path, mutation):
    report = copy.deepcopy(json.loads(REPORT.read_text()))
    a = report["actual_source_controls"][0]["branches"][0]["audit"]
    if mutation == "scope":
        report["general_receiver_impossibility_claim"] = True
    elif mutation == "phase":
        a["actual_residual_table"][0][0] = 1
    elif mutation == "gradient":
        a["direction_certificates"][0]["line_sum_gradient"][0][0] ^= 1
    elif mutation == "rank":
        a["coupling"]["coupling_mask_rank"] += 1
    elif mutation == "admission":
        a["direction_certificates"][0]["affine_for_every_Bell_shift_and_every_secret"] = not a["direction_certificates"][0]["affine_for_every_Bell_shift_and_every_secret"]
    elif mutation == "probability":
        report["actual_source_controls"][0]["branches"][0]["raw_source_branch"]["raw_joint_branch_probability"] = "1"
    elif mutation == "count":
        report["population_gates"][1]["projection_terms"][0]["idempotent_projection_count"] = "1"
    elif mutation == "Bell":
        report["physical_receiver_controls"][0]["all_Bell_branches"][0]["answer"] = 2
    elif mutation == "empty":
        report["actual_source_controls"] = []
    elif mutation == "compiler_support":
        report["complete_line_instrument_compilers"][0]["compiler"]["all_shift_supports"][0]["compiled_Kraus_input_words"][0][0] = 2
    elif mutation == "compiler_scale":
        report["complete_line_instrument_compilers"][0]["compiler"]["Kraus_squared_coefficient_denominator"] = 1
    else:
        report["complete_line_instrument_compilers"][0]["compiler"]["arbitrary_unknown_teleported_data_or_multiple_lines_covered"] = True
    target = tmp_path/"tampered.json"
    target.write_text(json.dumps(report))
    result = subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)
    assert result.returncode != 0
