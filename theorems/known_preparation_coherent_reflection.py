"""Costed fixed-bank pure-seed reflections and source-contract falsifiers.

Local derivation / review pending. Known classical preparation access only;
no ideal unknown inverse, full receiver, or quantum speedup is supplied.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
import math
from pathlib import Path

from flint import fmpq, fmpq_poly, nmod_mat
import numpy as np

from cyclotomic_rescaling_gate import multiply, pairing
from known_preparation_packet_simulation import known_source_packets, raw_source_fixture
from native_noisy_phase_input import checked_source_bank, prepare_inputs
from native_state_hsp_bridge import NativeGroup
from ternary_certified_noise_sampler import cosine_box, pi_box, rational, sqrt_box
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/KNOWN_PREPARATION_COHERENT_REFLECTION.md"
REPORT = ROOT/"research/reductions/known_preparation_coherent_reflection.json"
IID = "INDEPENDENT_SYMMETRIC_ORIGINAL_ERRORS_INDEPENDENT_OF_LABELS"


def checked_shape(cohorts, sites):
    integer(cohorts, "positive cohort count", 1)
    integer(sites, "positive sites per cohort", 1)
    if cohorts & (cohorts-1):
        raise ValueError("explicit Hadamard index preparation requires a power-of-two cohort count")


def reflection_recipe(records, mask, cohorts, sites):
    checked_shape(cohorts, sites)
    records, mask, q, n = checked_source_bank(records, mask)
    if len(records) != 2*cohorts*sites:
        raise ValueError("exactly two distinct paid original records per cohort site required")
    packets, source = known_source_packets(records, mask)
    prepared = prepare_inputs(records, mask, "0")
    phases = tuple(tuple(p.phase_numerators for p in packets[b*sites:(b+1)*sites]) for b in range(cohorts))
    if any(p.phase_numerators[1:] != r["known_phase_values"] for p, r in zip(packets, prepared.reduction_side_recipes)):
        raise ArithmeticError("coherent recipe disagrees with authoritative actual source preparation")
    labels = tuple(tuple(r.ring_labels for r in prepared.receiver_inputs[b*sites:(b+1)*sites]) for b in range(cohorts))
    return {"modulus": str(q), "native_even_level": 2*root_digits(q), "secret_dimension": n,
            "cohorts": cohorts, "sites_per_cohort": sites, "known_phase_numerators": phases,
            "public_native_labels": labels, "source_receipts": source,
            "original_classical_record_count": 2*cohorts*sites,
            "source_bank_reused_with_frozen_errors": True,
            "preparation_order": ["Hadamard_index_tensor_F3_sites", "known_controlled_diagonal"],
            "inverse_order": ["known_controlled_diagonal_inverse", "Hadamard_index_tensor_F3_sites_inverse"],
            "reflection_order": ["preparation_inverse", "zero_register_phase_flip", "preparation"],
            "controlled_diagonal_branches_per_preparation_upper": 2*cohorts*sites,
            "index_comparison_compute_uncompute_pairs_per_preparation_upper": cohorts,
            "qutrit_Fourier_gates_per_preparation": sites,
            "index_Hadamards_per_preparation": cohorts.bit_length()-1,
            "preparation_calls_per_reflection": 2,
            "multiplexor": "explicit index equality; no QRAM",
            "zero_test_synthesis_is_a_remaining_obligation": True,
            "ideal_unknown_state_inverse_supplied": False,
            "secret_or_errors_read_by_preparation": False,
            "relative_cohort_phases_may_be_discarded": False,
            "new_independent_originals_created_by_reuse": False,
            "hardware_synthesis_implemented": False}


def iid_characteristic_statistics(cohorts, sites, characteristic, *, independence):
    checked_shape(cohorts, sites)
    if independence != IID:
        raise ValueError("IID original error and label-independence promise required")
    g = rational(characteristic, "real symmetric error characteristic")
    if not -1 <= g <= 1:
        raise ValueError("symmetric characteristic must lie in [-1,1]")
    a, C = (1+2*g)/3, (3+4*g+2*g*g)/9
    A = a*a
    fidelity = A**sites+(C**sites-A**sites)/cohorts
    if not 0 <= fidelity <= 1:
        raise ArithmeticError("invalid pure-seed averaged fidelity")
    return {"cohorts": cohorts, "sites_per_cohort": sites, "characteristic": str(g),
            "single_overlap_mean": str(a), "single_overlap_mean_squared": str(A),
            "single_overlap_squared_mean": str(C), "mean_seed_fidelity": str(fidelity),
            "mean_pure_trace_distance_squared": str(1-fidelity),
            "mean_reflection_operator_error_squared": str(4*(1-fidelity)),
            "independence_promise": independence, "source_law_inferred_from_records": False}


def reflection_budget(q, cohorts, sites, moment, reflections, initial_copies=0, *,
                      independence, bits=64, preparation_operator_error="0",
                      zero_phase_operator_error="0", source_rounding_loss="0",
                      receiver_other_operations_loss="0"):
    root_digits(q)
    checked_shape(cohorts, sites)
    integer(reflections, "finite reflection query cap")
    integer(initial_copies, "finite initial pure-seed copy cap")
    integer(bits, "positive rational enclosure precision", 1)
    if independence != IID:
        raise ValueError("the composite bound requires an explicit IID original-source promise")
    V = rational(moment, "public integer second-moment upper")
    du = rational(preparation_operator_error, "complete preparation operator-error promise")
    ds = rational(zero_phase_operator_error, "complete zero-phase operator-error promise")
    rounding = rational(source_rounding_loss, "public source-rounding loss")
    other = rational(receiver_other_operations_loss, "complete receiver other-operations loss")
    if V < 0 or any(not 0 <= x <= 1 for x in (du, ds, rounding, other)):
        raise ValueError("nonnegative moment and bounded complete implementation promises required")
    pi_lo, pi_hi, terms = pi_box(bits)
    constant = fmpq(16, 9) if cohorts == 1 else fmpq(8, 3)
    e2 = min(fmpq(1), constant*pi_hi*pi_hi*sites*V/(q*q))
    rms = sqrt_box(e2, bits)
    initial = sqrt_box(initial_copies*e2, bits)
    hardware_initial = sqrt_box(initial_copies*du*du, bits)
    noise = min(fmpq(1), initial[1]+2*reflections*rms[1])
    hardware = min(fmpq(1), hardware_initial[1]+reflections*(2*du+ds)+other)
    total = min(fmpq(1), noise+hardware+rounding)
    return {"modulus": str(q), "cohorts": cohorts, "sites_per_cohort": sites,
            "original_classical_records_paid_once": str(2*cohorts*sites),
            "reflection_query_cap": str(reflections), "initial_point_seed_copies": str(initial_copies),
            "source_integer_second_moment_upper": str(V), "IID_promise": independence,
            "precision_bits": bits, "pi_interval": (str(pi_lo), str(pi_hi)), "Machin_terms": terms,
            "moment_constant": str(constant), "mean_pure_trace_distance_squared_upper": str(e2),
            "sqrt_e2_interval": tuple(map(str, rms)), "sqrt_K_e2_interval": tuple(map(str, initial)),
            "complete_preparation_operator_error_promise": str(du),
            "zero_phase_operator_error_promise": str(ds),
            "complete_receiver_other_operations_loss_promise": str(other),
            "sqrt_K_delta_U_squared_interval": tuple(map(str, hardware_initial)),
            "averaged_complete_receiver_noise_loss_upper": str(noise),
            "complete_hardware_loss_upper": str(hardware), "source_rounding_loss_upper": str(rounding),
            "complete_success_loss_upper": str(total), "bound_is_nonvacuous": total < 1,
            "noise_is_resampled_per_reflection": False,
            "averaged_copy_density_bound_used_as_operator_bound": False,
            "arbitrary_diagonal_queries_or_phase_powers_covered": False,
            "arbitrary_work_register_allowed_in_hybrid": True,
            "source_independence_established_by_unique_IDs": False,
            "receiver_or_classical_separation_supplied": False}


def finite_bank_gap_budget(n, level, sites, epsilon="1/2", failure_bits=32):
    integer(n, "positive native vector dimension", 1)
    integer(level, "native level at least two", 2)
    integer(sites, "positive cohort sites", 1)
    integer(failure_bits, "positive bank failure bits", 1)
    eps = rational(epsilon, "absolute nonhidden overlap upper")
    if not 0 < eps < 1:
        raise ValueError("nontrivial overlap threshold in (0,1) required")
    threshold = 4*(2*(n*level+1)+2+failure_bits)/(eps*eps)
    ceiling = (int(threshold.numerator)+int(threshold.denominator)-1)//int(threshold.denominator)
    B = 1 << (ceiling-1).bit_length()
    return {"dimension": n, "native_level": level, "sites_per_cohort": sites,
            "group_order_compact": {"base": 3, "exponent": n*level+1},
            "nonhidden_absolute_overlap_upper": str(eps), "ideal_absolute_overlap_gap_lower": str(1-eps),
            "bank_failure_bits": failure_bits, "bank_failure_upper": str(fmpq(1, 2**failure_bits)),
            "conservative_cohort_threshold": str(threshold), "Hadamard_cohort_count": str(B),
            "original_classical_records_required": str(2*B*sites),
            "seed_dimension_compact": {"coefficient": str(B), "base": 3, "exponent": sites},
            "native_backend_within_current_level_cap": level <= 512,
            "resource_profile_is_an_executed_bank": False,
            "seed_only_polynomial_dimension_when_sites_fixed": True,
            "IID_full_native_labels_and_ideal_states_are_external_promises": True,
            "observed_bank_has_been_certified": False, "efficient_subgroup_decoder_supplied": False,
            "gap_guarantee_includes_noise": False, "accepted_speedup_candidate": False}


def central_support(labels, level):
    labels = tuple(tuple(tuple(a) for a in cohort) for cohort in labels)
    if level < 2 or not labels or not labels[0]:
        raise ValueError("nonempty native cohorts at level >=2 required")
    n, M = len(labels[0][0]), len(labels[0])
    G = NativeGroup(level, n)
    if any(len(cohort) != M for cohort in labels):
        raise ValueError("equal cohort site count required")
    central = (1, 0)
    for _ in range(level-1):
        central = multiply(central, (-1, 1), level)
    rows = []
    for cohort in labels:
        row = [0]*n
        for label in cohort:
            for j, a in enumerate(G.vector(label)):
                coefficient = 3*pairing(a, central, level)
                if coefficient.denominator != 1:
                    raise ArithmeticError("native central character is not a third root")
                row[j] = (row[j]+int(coefficient)) % 3
        rows.append(tuple(row))
    differences = tuple(tuple((x-y) % 3 for x, y in zip(row, rows[0])) for row in rows[1:])

    def kernel(matrix):
        reduced = nmod_mat(matrix, 3).rref()[0].tolist() if matrix else []
        nonzero = [tuple(map(int, row)) for row in reduced if any(row)]
        pivots = [next(j for j, x in enumerate(row) if x) for row in nonzero]
        free = next((j for j in range(n) if j not in pivots), None)
        witness = None
        if free is not None:
            witness = [0]*n
            witness[free] = 1
            for row, pivot in zip(nonzero, pivots):
                witness[pivot] = (-row[free]) % 3
            witness = tuple(witness)
        return len(pivots), witness

    rank, fixed = kernel(rows)
    ray_rank, ray = kernel(differences)
    return {"native_level": level, "dimension": n, "cohorts": len(labels), "sites_per_cohort": M,
            "central_generator": central, "cohort_central_character_rows": rows,
            "vector_stabilizer_central_rank": rank, "ray_stabilizer_central_rank": ray_rank,
            "nonzero_extra_vector_stabilizer_witness": fixed,
            "nonzero_extra_ray_stabilizer_witness": ray,
            "vector_kernel_order": {"base": 3, "exponent": n-rank},
            "ray_kernel_order": {"base": 3, "exponent": n-ray_rank},
            "full_hidden_subgroup_or_gap_established": False,
            "noisy_seed_necessarily_fixed_by_H": False}


def dense_preparation(phases, q):
    root_digits(q)
    if not phases or not phases[0]:
        raise ValueError("nonempty phase cohorts required")
    B, M = len(phases), len(phases[0])
    checked_shape(B, M)
    D = B*3**M
    if D > 256:
        raise ValueError("literal dense replay is capped at dimension256")
    if any(len(row) != M or any(len(p) != 3 or p[0] != 0 or any(type(x) is not int or not 0 <= x < q for x in p) for p in row) for row in phases):
        raise ValueError("canonical actual phase bank with fixed zero-component gauge required")
    words = tuple(product(range(3), repeat=M))
    nums = tuple(sum(phases[b][j][t] for j, t in enumerate(word)) % q for b in range(B) for word in words)
    F = np.array([[np.exp(2j*np.pi*sum(x*y for x, y in zip(u, v))/3) for v in words] for u in words])/math.sqrt(3**M)
    H = np.array([[(-1)**((b & c).bit_count()) for c in range(B)] for b in range(B)])/math.sqrt(B)
    U = np.exp(2j*np.pi*np.array(nums)/q)[:, None]*np.kron(H, F)
    S = np.eye(D, dtype=complex)
    S[0, 0] = -1
    psi = U[:, 0]
    R = U@S@U.conj().T
    return U, psi, R, nums


def preparation_control(B, M, seed):
    _, receipt = raw_source_fixture(3, 2, B*M, seed)
    from ternary_noise_degradation import NoisyLinearRecord
    records = tuple(NoisyLinearRecord(tuple(r["label"]), r["value"], r["modulus"], r["source_id"]) for r in receipt["original_classical_records"])
    recipe = reflection_recipe(records, receipt["preparation_random_mask"], B, M)
    U, psi, R, nums = dense_preparation(recipe["known_phase_numerators"], 9)
    D = len(psi)
    errors = {"unitarity": float(np.max(abs(U.conj().T@U-np.eye(D)))),
              "inverse_returns_zero": float(np.max(abs(U.conj().T@psi-np.eye(D)[:, 0]))),
              "reflection_equals_rank_one_formula": float(np.max(abs(R-(np.eye(D)-2*np.outer(psi, psi.conj()))))),
              "reflection_squares_to_identity": float(np.max(abs(R@R-np.eye(D))))}
    if max(errors.values()) > 1e-11:
        raise ArithmeticError("literal preparation/reflection composite failed")
    return {"recipe": recipe, "seed_basis_phase_numerators": nums, "literal_dimension": D,
            "diagnostic_max_errors": errors, "central_support": central_support(recipe["public_native_labels"], 4),
            "dense_control_is_a_scalable_receiver": False}


def finite_field(q):
    root_digits(q)
    if q > 81:
        raise ValueError("cyclotomic expansion is a bounded certificate only")
    coeff = [0]*(2*q//3+1)
    coeff[0] = coeff[q//3] = coeff[2*q//3] = 1
    Phi = fmpq_poly(coeff)
    powers = tuple((fmpq_poly([0, 1])**j) % Phi for j in range(q))
    conj = lambda p: sum((p[i]*powers[(-i) % q] for i in range(len(p))), fmpq_poly()) % Phi
    return Phi, powers, conj


def encode_field(x):
    return [str(x[i]) for i in range(len(x)-1, -1, -1)]


def exact_iid_control(q, B, M):
    checked_shape(B, M)
    if q not in (3, 9) or B*M > 4:
        raise ValueError("exact error census is a bounded certificate only")
    Phi, powers, conj = finite_field(q)
    mean = fmpq_poly()
    for signs in product((-1, 1), repeat=2*B*M):
        overlaps = []
        for b in range(B):
            r = fmpq_poly([1])
            for j in range(M):
                i = 2*(b*M+j)
                r = (r*(1+powers[signs[i] % q]+powers[signs[i+1] % q])/3) % Phi
            overlaps.append(r)
        overlap = sum(overlaps, fmpq_poly())/B
        mean += overlap*conj(overlap)/2**(2*B*M)
    mean %= Phi
    g = (powers[1]+powers[-1])/2
    A, C = ((1+2*g)**2/9) % Phi, ((3+4*g+2*g*g)/9) % Phi
    formula = (A**M+(C**M-A**M)/B) % Phi
    if mean != formula:
        raise ArithmeticError("enumerated actual errors disagree with coherent IID fidelity law")
    return {"modulus": q, "cohorts": B, "sites_per_cohort": M, "error_law": ((-1, "1/2"), (1, "1/2")),
            "error_configurations_checked": 2**(2*B*M), "mean_fidelity_exact": encode_field(mean),
            "formula_fidelity_exact": encode_field(formula), "mean_trace_distance_squared_exact": encode_field((1-mean) % Phi),
            "mean_reflection_operator_error_squared_exact": encode_field((4*(1-mean)) % Phi),
            "ideal_phase_values_or_hidden_secret_used_as_oracle": False}


def frozen_bank_counterexample(q=81, T=20):
    root_digits(q)
    integer(T, "positive reuse count", 1)
    theta = 2*math.pi/q
    plus = np.ones(2, complex)/math.sqrt(2)
    R0 = np.eye(2)-2*np.outer(plus, plus.conj())
    observations, norm_errors = [], []
    for sign in (-1, 1):
        psi = np.array([1, np.exp(1j*sign*theta)])/math.sqrt(2)
        R = np.eye(2)-2*np.outer(psi, psi.conj())
        out = np.linalg.matrix_power(R@R0, T)@plus
        observations.append(float(abs(np.vdot(np.array([1, -1])/math.sqrt(2), out))**2))
        norm_errors.append(float(np.linalg.norm(R-R0, 2)))
    delta = (1-math.cos(theta))/2
    clo, chi = cosine_box(q, 1, 64)
    plo, phi = cosine_box(q, 2*T, 64)
    copy_box = ((1-chi)/2, (1-clo)/2)
    probability_box = ((1-phi)/2, (1-plo)/2)
    return {"modulus": q, "reflections_of_noisy_bank": T,
            "frozen_error_law": ((-1, "1/2"), (1, "1/2")),
            "actual_minus_probability_per_frozen_error": observations,
            "analytic_minus_probability": math.sin(T*theta)**2,
            "averaged_copy_trace_distance": delta,
            "invalid_T_times_copy_budget": T*delta,
            "reflection_operator_errors": norm_errors,
            "correct_clipped_T_operator_budget": min(1, 2*T*math.sin(theta/2)),
            "copy_trace_distance_box": tuple(map(str, copy_box)),
            "actual_minus_probability_box": tuple(map(str, probability_box)),
            "rational_falsifier_precision_bits": 64,
            "falsifier_is_certified_by_rational_boxes": probability_box[0] > T*copy_box[1],
            "averaged_copy_budget_falsified": min(observations) > T*delta,
            "candidate_algorithm": False, "source_model_changed_by_fresh_error_each_call": False}


def correlated_bank_counterexample(q=81, M=8):
    root_digits(q)
    integer(M, "positive correlated cohort sites", 1)
    theta = 2*math.pi/q
    observed = []
    for e, f in product((-1, 1), repeat=2):
        cohort = ((1+np.exp(1j*e*theta)+np.exp(1j*f*theta))/3)**M
        # The second entire cohort has the opposite frozen pair.
        overlap = (cohort+cohort.conjugate())/2
        observed.append(1-float(abs(overlap)**2))
    actual = sum(observed)/4
    assumed = reflection_budget(q, 2, M, "1", 1, independence=IID)
    bound = float(fmpq(assumed["mean_pure_trace_distance_squared_upper"]))
    Phi, powers, conj = finite_field(q)
    same_sign = ((1+2*powers[1])**M/3**M) % Phi
    real_same = (same_sign+conj(same_sign))/2
    opposite = ((1+powers[1]+powers[-1])**M/3**M) % Phi
    exact = (1-(real_same**2+opposite**2)/2) % Phi
    lower, upper = fmpq(0), fmpq(0)
    for k in range(len(exact)):
        coefficient = exact[k]
        if coefficient:
            lo, hi = cosine_box(q, k, 72)
            lower += coefficient*(lo if coefficient > 0 else hi)
            upper += coefficient*(hi if coefficient > 0 else lo)
    promised = fmpq(assumed["mean_pure_trace_distance_squared_upper"])
    return {"modulus": q, "cohorts": 2, "sites_per_cohort": M,
            "marginal_integer_second_moment": "1", "distinct_original_IDs_can_still_be_correlated": True,
            "joint_error_law": "same independent sign pair at every site; opposite pair in second cohort",
            "squared_trace_distance_per_pair": observed, "actual_mean_trace_distance_squared": actual,
            "misapplied_IID_moment_upper": bound, "IID_bound_is_falsified_without_IID": actual > bound,
            "mean_trace_distance_squared_exact": encode_field(exact),
            "certified_mean_trace_distance_squared_box": (str(lower), str(upper)),
            "misapplied_IID_budget": assumed,
            "falsifier_is_certified_by_rational_boxes": lower > promised,
            "source_independence_promise_satisfied": False, "universal_noise_no_go": False}


def build_report():
    controls = [preparation_control(B, M, 81000+B*100+M) for B, M in ((1, 3), (2, 1), (2, 2), (4, 2))]
    exact = [exact_iid_control(q, B, M) for q, B, M in ((3, 1, 1), (9, 1, 2), (9, 2, 1), (9, 2, 2))]
    budgets = []
    gaps = []
    for n, M, T, K in ((8, 64, 8, 1), (32, 1024, 32, 4), (128, 16384, 128, 1), (1024, 1, 1024**2, 4)):
        q = 3**n
        gap = finite_bank_gap_budget(n, 2*n, M)
        B = int(gap["Hadamard_cohort_count"])
        V = fmpq(q*q, 3*n**6)+fmpq(1, 2)
        budget = reflection_budget(q, B, M, V, T, K, independence=IID,
                                   preparation_operator_error="1/1099511627776", zero_phase_operator_error="1/1099511627776")
        budgets.append({"dimension": n, "budget": budget, "Gaussian_style_moment_is_a_promise_not_source_execution": True})
        gaps.append(gap)
    return {"status": "CONDITIONAL_KNOWN_BANK_REFLECTION_ACCESS_EXTERNAL_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "source_constructor_sha256": hashlib.sha256((ROOT/"theorems/native_noisy_phase_input.py").read_bytes()).hexdigest(),
            "preparation_controls": controls, "exact_IID_error_controls": exact,
            "characteristic_controls": [iid_characteristic_statistics(B, M, g, independence=IID) for B, M, g in
                                        ((1, 8, "9/10"), (4, 8, "9/10"), (1024, 64, "999/1000"), (2, 3, "-1"), (4, 8, "1"))],
            "scalable_reflection_budgets": budgets, "conditional_bank_gap_budgets": gaps,
            "frozen_bank_copy_budget_falsifier": frozen_bank_counterexample(),
            "correlated_bank_IID_budget_falsifier": correlated_bank_counterexample(),
            "research_decision": "REQUIRE_COSTED_WIDE_COHERENT_WORK_AND_ORIGINAL_DATA_BASELINES_BEFORE_ADMISSION",
            "unknown_quantum_only_phase_sources_covered": False,
            "generic_known_preparation_classical_simulation_proved": False,
            "quantum_hardware_executed": False, "efficient_receiver_supplied": False,
            "hardness_transfer_admitted": False, "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "remaining_proof_debt": ["external review of IID law, hybrid and bank-gap composition",
                                     "source rounding and original-data hardness promises",
                                     "complete physical controlled phases/Fourier/zero-test synthesis",
                                     "retained coherent work/group circuit and efficient full decoder",
                                     "same-original-data and tensor-rank classical attack suite",
                                     "no ideal source inverse imported for opaque quantum-only inputs"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "actual_preparation_controls": len(report["preparation_controls"]),
                      "exact_IID_error_controls": len(report["exact_IID_error_controls"]),
                      "scalable_noise_loss_upper": [r["budget"]["complete_success_loss_upper"] for r in report["scalable_reflection_budgets"]],
                      "copy_budget_falsified": report["frozen_bank_copy_budget_falsifier"]["averaged_copy_budget_falsified"],
                      "missing_IID_falsified": report["correlated_bank_IID_budget_falsifier"]["IID_bound_is_falsified_without_IID"],
                      "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__":
    main()
