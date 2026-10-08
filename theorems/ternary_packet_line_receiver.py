"""Exact all-translation affine-line gate for one-use native cubic packets.

Public high-label-informed directions are allowed. The gate covers an exact
line-equation receiver, not arbitrary noncommuting or approximate decoding.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
from types import SimpleNamespace

from flint import nmod_mat
import numpy as np

from cyclotomic_fiber_receiver import frequency_coordinates, inverse_frequency_coordinates
from ternary_carry_packets import compile_packet
from ternary_correlated_packet_acquisition import PacketAcquisition, integer, word
from ternary_cyclic_extractor import random_even_source
from ternary_packet_pauli_gate import kernel_frame
from ternary_quadratic_program_receiver import linear_chart, teleport_tensor

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_packet_line_receiver.json"
DERIVATION = ROOT / "research/TERNARY_PACKET_LINE_RECEIVER.md"


def packet_data(packet):
    if packet.level != 3 or not packet.retained:
        raise ValueError("nonempty actual level3 field-root packet required")
    pairs = tuple(tuple(frequency_coordinates(y, 3) for y in row) for row in packet.labels)
    n, K = packet.secret_dimension, packet.consumed
    C = tuple(tuple(pairs[i][l][0] % 3 for i in range(K)) for l in range(n))
    kappa = tuple(tuple(((pairs[i][l][0]+pairs[i][l][1]) % 9)//3 for i in range(K)) for l in range(n))
    if any((a+b) % 3 for row in pairs for a, b in row):
        raise ArithmeticError("odd native frequency chart violated")
    D = kernel_frame(packet)
    base = packet.assignment((0,)*packet.retained)
    sigma = tuple(sum(a*t for a, t in zip(row, base)) % 3 for row in C)
    return {"frequency_pairs": pairs, "C": C, "kappa": kappa, "D": D, "base": base,
            "original_low_syndrome": sigma}


def coupling_certificate(packet):
    data = packet_data(packet)
    C, D = data["C"], data["D"]
    K, h = packet.consumed, packet.retained
    mask_rows = tuple(tuple(C[l][i]*D[i][j] % 3 for i in range(K))
                      for l in range(packet.secret_dimension) for j in range(h))
    coupling_rank = int(nmod_mat(mask_rows, 3).rank())
    if any(sum(row) % 3 for row in mask_rows):
        raise ArithmeticError("full support must preserve the low kernel")
    return {**data, "coupling_mask_rows": mask_rows, "coupling_mask_rank": coupling_rank,
            "only_constant_diagonal_masks_preserve_kernel": coupling_rank == K-1,
            "coupling_is_a_rank_certificate_not_a_direction_enumerator": True,
            "low_matrix_rank": int(nmod_mat(C, 3).rank()),
            "complete_direction_search_or_teleportation_success_claimed": False}


def direction_certificate(packet, direction, data=None):
    direction = word(direction, packet.retained)
    if not any(direction):
        raise ValueError("nonzero logical direction required")
    data = packet_data(packet) if data is None else data
    D, C, kappa, base = data["D"], data["C"], data["kappa"], data["base"]
    physical = tuple(sum(a*v for a, v in zip(row, direction)) % 3 for row in D)
    support = tuple(i for i, x in enumerate(physical) if x)
    gradient = tuple(tuple(-sum(C[l][i]*D[i][j] for i in support) % 3
                           for j in range(packet.retained)) for l in range(packet.secret_dimension))
    constant = tuple(sum(kappa[l][i]-C[l][i]*base[i] for i in support) % 3
                     for l in range(packet.secret_dimension))
    admitted = not any(constant) and not any(x for row in gradient for x in row)
    return {"logical_direction": direction, "physical_direction": physical, "physical_support": support,
            "line_sum_constant": constant, "line_sum_gradient": gradient,
            "affine_for_every_Bell_shift_and_every_secret": admitted,
            "direction_may_read_all_public_high_labels_and_syndrome": True,
            "direction_selected_before_current_Bell_shift_required": True,
            "known_nonzero_equation_or_uniform_equation_labels_guaranteed": False}


def residual_from_pairs(data, physical, base):
    pairs = data["frequency_pairs"]
    n = len(pairs[0])
    values = []
    for l in range(n):
        delta = sum((pairs[i][l][t-1] if t else 0)-(pairs[i][l][b-1] if b else 0)
                    for i, (t, b) in enumerate(zip(physical, base))) % 9
        if delta % 3:
            raise ArithmeticError("logical word escaped actual low syndrome")
        values.append(delta//3)
    return tuple(values)


def complete_packet_audit(packet, max_words=243):
    integer(max_words, "whole logical-word cap", 1)
    if 3**packet.retained > max_words:
        return {"status": "COMPLETE_PACKET_WORD_CAP_EXHAUSTED", "partial_affine_gate_proved": False}
    coupling = coupling_certificate(packet)
    points = tuple(product(range(3), repeat=packet.retained))
    table = {z: residual_from_pairs(coupling, packet.assignment(z), coupling["base"]) for z in points}
    directions, checks, admitted = [], 0, 0
    for v in points:
        if not any(v):
            continue
        certificate = direction_certificate(packet, v, coupling)
        all_affine = True
        for a in points:
            values = [table[tuple((x+j*y) % 3 for x, y in zip(a, v))] for j in range(3)]
            actual = tuple(sum(row[l] for row in values) % 3 for l in range(packet.secret_dimension))
            expected = tuple((c+sum(g*x for g, x in zip(row, a))) % 3
                             for c, row in zip(certificate["line_sum_constant"], certificate["line_sum_gradient"]))
            if actual != expected:
                raise ArithmeticError("native line-sum identity failed")
            all_affine = all_affine and not any(actual)
            checks += 1
        if all_affine != certificate["affine_for_every_Bell_shift_and_every_secret"]:
            raise ArithmeticError("exact all-translation affine admission failed")
        if all_affine:
            admitted += 1
        if coupling["only_constant_diagonal_masks_preserve_kernel"] and all_affine:
            if len(certificate["physical_support"]) != packet.consumed:
                raise ArithmeticError("coupled code admitted a proper nonempty support")
            if any((sum(row)-s) % 3 for row, s in zip(coupling["kappa"], coupling["original_low_syndrome"])):
                raise ArithmeticError("coupled code admitted wrong full syndrome")
        directions.append(certificate)
    return {"status": "COMPLETE_NATIVE_ALL_TRANSLATION_LINE_AUDIT", "native_labels": packet.labels,
            "odd_level": packet.level, "RREF_rows": packet.reduced_rows, "syndrome": packet.syndrome,
            "coupling": coupling, "logical_points": points, "actual_residual_table": tuple(table[z] for z in points),
            "direction_certificates": directions, "all_direction_shift_pairs_checked": checks,
            "admitted_nonzero_directions": admitted, "complete_direction_search_is_scalable": False,
            "one_unknown_program_supplied_or_decoder_implemented_by_this_audit": False}


def physical_line_receiver(packet, direction, secret):
    contract = direction_certificate(packet, direction)
    if not contract["affine_for_every_Bell_shift_and_every_secret"]:
        raise ValueError("one-use all-outcome affine-line admission required")
    if packet.retained > 3:
        raise ValueError("complete Bell tensor replay capped at three logical registers")
    secret = word(secret, packet.secret_dimension)
    h, N = packet.retained, 3**packet.retained
    points = tuple(product(range(3), repeat=h))
    index = {z: i for i, z in enumerate(points)}
    data = np.zeros(N, complex)
    for j in range(3):
        data[index[tuple(j*x % 3 for x in direction)]] = 1/math.sqrt(3)
    program = SimpleNamespace(width=h, components=packet.secret_dimension, value=packet.residual)
    tensor, _ = teleport_tensor(program, secret, data)
    worst, total, records = 0., 0., []
    for ai, a in enumerate(points):
        q0 = packet.residual(a)
        q1 = packet.residual(tuple((x+y) % 3 for x, y in zip(a, direction)))
        label = tuple((x-y) % 3 for x, y in zip(q1, q0))
        answer = sum(x*y for x, y in zip(secret, label)) % 3
        for bi, b in enumerate(points):
            branch = tensor[0, bi, ai]
            probability = float(np.sum(abs(branch)**2))
            total += probability
            correction = sum(x*y for x, y in zip(b, direction)) % 3
            clean = np.array([branch[index[tuple((x+j*y) % 3 for x, y in zip(a, direction))]]
                              *np.exp(2j*np.pi*j*correction/3) for j in range(3)])*N
            probabilities = abs(np.fft.fft(clean)/math.sqrt(3))**2
            worst = max(worst, abs(probability-1/N**2), abs(float(probabilities[answer])-1))
            records.append({"Bell_shift": a, "Bell_phase": b, "equation_label": label, "answer": answer,
                            "raw_Bell_probability": str(Fraction(1, N**2)),
                            "Fourier_probabilities": probabilities.tolist()})
    if worst > 4e-12 or abs(total-1) > 4e-12:
        raise ArithmeticError("actual one-use Bell circuit or exact equation failed")
    return {"native_labels": packet.labels, "syndrome": packet.syndrome, "direction": direction,
            "calibration_secret": secret, "all_Bell_branches": records, "maximum_physical_residual": worst,
            "total_raw_Bell_probability": total, "one_supplied_program_consumed": True,
            "virtual_branches_are_independent_source_programs": False}


def line_compilation(width, direction, max_words=243):
    """Exact instrument identity, including curved programs and reference systems."""
    integer(width, "line register width", 1)
    integer(max_words, "complete line compiler word cap", 1)
    direction = word(direction, width)
    if not any(direction):
        raise ValueError("nonzero fixed public line required")
    if 3**width > max_words:
        raise ValueError("complete line compiler calibration exceeds word cap")
    columns, gates = linear_chart((direction,), width)
    matrix = [[columns[j][i] for j in range(width)] for i in range(width)]
    inverse = nmod_mat(matrix, 3).inv()
    inv = tuple(tuple(int(inverse[i, j]) for j in range(width)) for i in range(width))
    records = []
    for a in product(range(3), repeat=width):
        coords = tuple(sum(x*y for x, y in zip(row, a)) % 3 for row in inv)
        base = tuple(sum(columns[j][i]*coords[j] for j in range(1, width)) % 3 for i in range(width))
        original = tuple(tuple((x+j*y) % 3 for x, y in zip(a, direction)) for j in range(3))
        compiled = tuple(tuple((x+(coords[0]+j)*y) % 3 for x, y in zip(base, direction)) for j in range(3))
        if original != compiled:
            raise ArithmeticError("compiled projection has wrong Kraus support")
        records.append({"Bell_shift": a, "public_random_line_shift": coords[0], "measured_quotient": coords[1:],
                        "original_Kraus_input_words": original, "compiled_Kraus_input_words": compiled})
    return {"width": width, "fixed_public_direction": direction, "chart_columns": columns,
            "inverse_chart_rows": inv, "chart_gates": gates, "all_shift_supports": records,
            "Kraus_squared_coefficient_denominator": 3**(width+1),
            "public_line_shift_probability": "1/3", "public_Bell_phase_probability": str(Fraction(1, 3**width)),
            "measured_quotient_registers": width-1, "same_supplied_packet_consumed": True,
            "arbitrary_packet_density_matrix_and_external_reference_covered": True,
            "affine_phase_or_secret_promise_required": False,
            "arbitrary_unknown_teleported_data_or_multiple_lines_covered": False,
            "classical_simulation_of_quantum_packet_claimed": False}


def physical_compilation(width, direction, seed=94190):
    if width > 3:
        raise ValueError("complete Bell/reference tensor calibration capped at three registers")
    proof = line_compilation(width, direction)
    points = tuple(product(range(3), repeat=width))
    index = {z: i for i, z in enumerate(points)}
    N = len(points)
    rng = np.random.default_rng(seed)
    packet = rng.normal(size=(2, N))+1j*rng.normal(size=(2, N))
    packet /= np.linalg.norm(packet)
    line = np.zeros(N, complex)
    for j in range(3):
        line[index[tuple(j*x % 3 for x in direction)]] = 1/math.sqrt(3)
    tensor = np.zeros((2, N, N, N), complex)
    for xi, x in enumerate(points):
        for ti, t in enumerate(points):
            a = index[tuple((y-z) % 3 for y, z in zip(t, x))]
            tensor[:, xi, a, ti] = line[xi]*packet[:, ti]
    tensor = np.fft.fftn(tensor.reshape((2,)+(3,)*width+(N, N)), axes=tuple(range(1, width+1)))/math.sqrt(N)
    tensor = tensor.reshape(2, N, N, N)
    worst, total = 0., 0.
    for ai, a in enumerate(points):
        record = proof["all_shift_supports"][ai]
        expected = packet[:, [index[z] for z in record["compiled_Kraus_input_words"]]]/math.sqrt(3*N)
        for bi, b in enumerate(points):
            raw = tensor[:, bi, ai]
            total += float(np.sum(abs(raw)**2))
            correction = sum(x*y for x, y in zip(b, direction)) % 3
            actual = np.stack([raw[:, index[tuple((x+j*y) % 3 for x, y in zip(a, direction))]]
                               *np.exp(2j*np.pi*j*correction/3) for j in range(3)], axis=1)
            worst = max(worst, float(np.max(abs(actual-expected))))
    if worst > 4e-12 or abs(total-1) > 4e-12:
        raise ArithmeticError("known-line Bell instrument and packet projection differ")
    return {"compiler": proof, "random_reference_entangled_packet_seed": seed,
            "reference_dimension": 2, "complete_Bell_branches_checked": N*N,
            "maximum_Kraus_amplitude_residual": worst, "total_raw_probability": total,
            "packet_is_secret_flat_phase_calibration_only": False}


def gaussian_binomial(n, r):
    if not 0 <= r <= n:
        raise ValueError("valid subspace dimension required")
    numerator, denominator = 1, 1
    for i in range(r):
        numerator *= 3**(n-i)-1
        denominator *= 3**(r-i)-1
    if numerator % denominator:
        raise ArithmeticError("nonintegral finite-field subspace count")
    return numerator//denominator


def exact_fraction_string(value):
    """Serialize bounded research rationals without changing Python's global guard."""
    def decimal(a):
        sign, a = ("-", -a) if a < 0 else ("", a)
        chunks = []
        while a >= 10**1000:
            a, part = divmod(a, 10**1000)
            chunks.append(f"{part:01000d}")
        return sign+str(a)+"".join(reversed(chunks))
    return decimal(value.numerator) if value.denominator == 1 else decimal(value.numerator)+"/"+decimal(value.denominator)


def population_gate(n, K):
    integer(n, "secret dimension", 1)
    integer(K, "odd input count", n+1)
    rank_failure = Fraction(3**n-1, 2*3**K)
    zero_column = Fraction(K, 3**n)
    terms = []
    for r in range(1, n):
        count = gaussian_binomial(n, r)*3**(r*(n-r))
        union_size = 3**r+3**(n-r)-1
        terms.append({"projection_rank": r, "idempotent_projection_count": str(count),
                      "complementary_subspace_union_size": str(union_size),
                      "probability_union_bound": exact_fraction_string(count*Fraction(union_size, 3**n)**K)})
    decomposable = sum((gaussian_binomial(n, r)*3**(r*(n-r))*Fraction(3**r+3**(n-r)-1, 3**n)**K
                        for r in range(1, n)), Fraction())
    bad = min(Fraction(1), rank_failure+zero_column+decomposable)
    raw = min(Fraction(1), bad+Fraction(1, 3**n))
    return {"dimension": n, "odd_inputs": K, "original_even_level4_input_cap": K*(n+1)**2,
            "rank_failure_upper": str(min(Fraction(1), rank_failure)),
            "zero_column_upper": str(min(Fraction(1), zero_column)), "projection_terms": terms,
            "bad_low_matrix_probability_upper": exact_fraction_string(bad),
            "good_matrix_admissible_syndrome_probability_upper": str(Fraction(1, 3**n)),
            "raw_exact_one_use_line_admission_probability_upper": exact_fraction_string(raw),
            "original_IID_source_premise_required": True, "high_label_informed_direction_search_allowed": True,
            "approximate_or_non_affine_line_receivers_covered": False,
            "multi_program_cubic_cancellation_factory_covered": False,
            "all_native_quantum_receivers_excluded": False}


def actual_source_control(n, K, seed):
    M = K*(n+1)**2
    source = random_even_source(n, 4, M, seed)
    acquisition = PacketAcquisition.from_source(source, K, tuple(f"line-{seed}-original-{i}" for i in range(M)), M)
    pointers = (0,)*len(acquisition.pointers)
    prototype = acquisition.branch(pointers).packet
    branches = []
    for syndrome in product(range(3), repeat=len(prototype.pivots)):
        branch = acquisition.branch(pointers, syndrome)
        audit = complete_packet_audit(branch.packet)
        # Check actual original-root phases too, not only the odd chart formula.
        if tuple(branch.original_residual(z) for z in audit["logical_points"]) != audit["actual_residual_table"]:
            raise ArithmeticError("original acquisition and packet residual disagree")
        branches.append({"raw_source_branch": branch.resources(), "audit": audit})
    return {"seed": seed, "source": acquisition.source_record(), "original_native_labels": source.labels,
            "selected_pointer": pointers, "all_syndromes_at_this_pointer_checked": True,
            "all_original_pointer_outcomes_checked": len(acquisition.pointers) == 0,
            "selected_pointer_is_population_or_free_source_claimed": False, "branches": branches}


def countercontrol(low, pairs, name):
    labels = tuple(tuple(inverse_frequency_coordinates(*pair, 3) for pair in row) for row in pairs)
    prototype = compile_packet(labels, 3)
    branches = [complete_packet_audit(compile_packet(labels, 3, y)) for y in product(range(3), repeat=len(prototype.pivots))]
    if tuple(tuple(row[0] % 3 for row in component) for component in zip(*pairs)) != tuple(low):
        raise ArithmeticError("engineered native low chart mismatch")
    return {"name": name, "engineered_not_population_sample": True, "branches": branches}


def build_report():
    connected_pairs = (((1, 2),), ((1, 2),), ((1, 2),))
    decomposed_pairs = (((1, 2), (0, 0)), ((2, 4), (0, 0)), ((0, 0), (1, 2)), ((0, 0), (2, 4)))
    line_packet = compile_packet(tuple(tuple(inverse_frequency_coordinates(*p, 3) for p in row) for row in connected_pairs), 3)
    return {"status": "ONE_USE_PACKET_LINE_COMPILED_EXACT_ADMISSION_SCOPED_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "actual_source_controls": [actual_source_control(1, 4, 94101), actual_source_control(2, 5, 94102)],
            "countercontrols": [countercontrol(((1, 1, 1),), connected_pairs, "coupled-three-site-native-packet"),
                                countercontrol(((1, 2, 0, 0), (0, 0, 1, 2)), decomposed_pairs, "decomposable-two-block-native-packet")],
            "population_gates": [population_gate(n, 4*n) for n in (1, 4, 8, 16, 32, 64)],
            "physical_receiver_controls": [physical_line_receiver(line_packet, (1, 1), (s,)) for s in range(3)],
            "complete_line_instrument_compilers": [physical_compilation(h, (1,)+(0,)*(h-2)+(1,) if h > 1 else (1,)) for h in (1, 2, 3)],
            "accepted_speedup_candidate": False, "general_receiver_impossibility_claim": False,
            "new_original_source_or_unknown_inverse_granted": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "actual_source_direction_shift_checks": sum(
        b["audit"]["all_direction_shift_pairs_checked"] for c in report["actual_source_controls"] for b in c["branches"]),
        "population_gates": [{"n": n, "raw_admission_upper_approximation_NOT_certificate": float(
            min(Fraction(1), Fraction(3**n-1, 2*3**(4*n))+Fraction(4*n+1, 3**n)
                +sum((gaussian_binomial(n, r)*3**(r*(n-r))*Fraction(3**r+3**(n-r)-1, 3**n)**(4*n)
                      for r in range(1, n)), Fraction())))} for n in (1, 4, 8, 16, 32, 64)]}, indent=2))


if __name__ == "__main__":
    main()
