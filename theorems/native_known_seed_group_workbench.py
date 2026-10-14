"""Actual native group coupling, integer kernel and paid postselection audit.

Local derivation / review pending. Original classical records only; no free
ideal inverse, efficient full decoder, or general quantum no-go is supplied.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random

from flint import fmpq, fmpq_poly
import numpy as np

from cyclotomic_rescaling_gate import multiply, pairing, reduce_element
from known_preparation_coherent_reflection import (
    IID, central_support, dense_preparation, encode_field, finite_field,
    reflection_budget, reflection_recipe,
)
from known_reflection_tensor_simulation import (
    ONE, Term, TensorState, conj as complex_conj,
    fourier_gate, integer_text, mul as complex_mul, root_entry, sample_basis, sum_complex,
    seed_tensor,
)
from native_state_hsp_bridge import NativeGroup, ring_words
from native_noncentral_filter_tradeoff import amplitude_polynomial
from ternary_certified_noise_sampler import sqrt_box
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/NATIVE_KNOWN_SEED_GROUP_WORKBENCH.md"
REPORT = ROOT/"research/reductions/native_known_seed_group_workbench.json"
FULL, SLICE = "FULL_NATIVE_GROUP", "INTEGER_SECRET_SLICE"


def domain_recipe(recipe, domain):
    n, q, L = recipe["secret_dimension"], int(recipe["modulus"]), recipe["native_even_level"]
    NativeGroup(L, n)
    if domain not in (FULL, SLICE): raise ValueError("declared full group or original integer-secret slice required")
    B, M = recipe["cohorts"], recipe["sites_per_cohort"]
    return {"domain": domain, "dimension": n, "modulus": str(q), "native_level": L,
            "work_coordinate_trits": n*root_digits(q) if domain == SLICE else n*L+1,
            "uniform_work_size": integer_text(q**n if domain == SLICE else 3*q**(2*n)),
            "source_preparation_calls": 1, "actual_source_inverse_calls": 1,
            "controlled_qutrit_cyclic_permutations": M,
            "controlled_character_branches_upper": 3*B*M,
            "index_comparison_compute_uncompute_pairs_upper": B,
            "original_classical_records_paid_once": 2*B*M,
            "point_inverse_uses_original_values_not_secret": True,
            "arbitrary_chosen_source_label_oracle_supplied": False,
            "QRAM_supplied": False, "physical_gate_compiler_supplied": False,
            "postselection_is_free": False,
            "work_Fourier_interference_is_classically_simulated_by_early_measurement": False}


def checked_group(recipe, g):
    G = NativeGroup(recipe["native_even_level"], recipe["secret_dimension"])
    return G, G.element(g)


def character_exponent(G, label, vector, q):
    phase = q*sum((pairing(a, v, G.level) for a, v in zip(G.vector(label), G.vector(vector))), Fraction())
    if phase.denominator != 1:
        raise ArithmeticError("native character exceeds its declared root")
    return int(phase) % q


def scalar_overlap_exact(recipe, g, tools=None):
    q = int(recipe["modulus"])
    Phi, powers, _ = finite_field(q) if tools is None else tools
    G, (v, t) = checked_group(recipe, g)
    value = fmpq_poly()
    for cohort, labels in zip(recipe["known_phase_numerators"], recipe["public_native_labels"]):
        term = powers[0]
        for phases, label in zip(cohort, labels):
            local = fmpq_poly()
            for out in range(3):
                k = character_exponent(G, label, G.rotate(v, out), q)
                local += powers[(phases[(out+t) % 3]-phases[out]+k) % q]/3
            term = (term*local) % Phi
        value += term/recipe["cohorts"]
    return value % Phi


def decoded_candidate(G, g):
    v, t = G.element(g)
    if not t: return None
    inverse_lambda = (1, 0) if t == 1 else (0, -1)
    return tuple(multiply((-a, -b), inverse_lambda, G.level) for a, b in v)


def finite_elements(recipe, domain):
    d = domain_recipe(recipe, domain)
    if int(d["uniform_work_size"]) > 4096:
        raise ValueError("full work enumeration is a bounded control, not scalable access")
    q, n, L = int(recipe["modulus"]), recipe["secret_dimension"], recipe["native_even_level"]
    if domain == SLICE:
        return tuple((tuple((x, 0) for x in b), 1) for b in product(range(q), repeat=n))
    return tuple((tuple(v), t) for v, t in product(product(ring_words(L), repeat=n), range(3)))


def integer_kernel_exact(recipe):
    q, n = int(recipe["modulus"]), recipe["secret_dimension"]
    B, M = recipe["cohorts"], recipe["sites_per_cohort"]
    if q > 9 or B*3**M > 512 or q**n > 81:
        raise ValueError("weighted word/frequency census is a bounded certificate only")
    Phi, powers, conjugate = finite_field(q)
    raw = recipe["source_receipts"]["original_classical_records"]
    counts, coefficients, words = Counter(), {}, []
    D = B*3**M
    for b in range(B):
        choices, phases = [], []
        for j in range(M):
            first, second = raw[2*(b*M+j):2*(b*M+j)+2]
            a, c = first["label"], second["label"]
            choices.append((tuple(a), tuple((y-x) % q for x, y in zip(a, c)), tuple(-x % q for x in c)))
            y, z = recipe["known_phase_numerators"][b][j][1:]
            phases.append((y, (z-y) % q, -z % q))
        for word in product(range(3), repeat=M):
            sigma = tuple(sum(choices[j][t][k] for j, t in enumerate(word)) % q for k in range(n))
            phase = sum(phases[j][t] for j, t in enumerate(word)) % q
            counts[sigma] += 1
            coefficients[sigma] = (coefficients.get(sigma, fmpq_poly())+powers[phase]/D) % Phi
            words.append({"cohort": b, "word": word, "frequency": sigma, "known_phase": phase})
    order = tuple(product(range(q), repeat=n))
    p2 = sum((fmpq(counts[k]**2, D*D) for k in order), fmpq(0))
    zero = sum((coefficients.get(k, fmpq_poly())*conjugate(coefficients.get(k, fmpq_poly())) for k in order), fmpq_poly()) % Phi
    return {"domain_words": D, "words": words, "frequencies": order,
            "pushforward_counts": tuple(counts[k] for k in order),
            "actual_Fourier_coefficients_exact": tuple(encode_field(coefficients.get(k, fmpq_poly())) for k in order),
            "ideal_collision_mass": str(p2), "actual_source_zero_mass_exact": encode_field(zero)}, coefficients, counts


def source_fixture(n, r, B, M, noisy, seed):
    q, rng = 3**r, random.Random(seed)
    secret, mask = tuple(rng.randrange(q) for _ in range(n)), tuple(rng.randrange(q) for _ in range(n))
    errors, records = [], []
    for i in range(2*B*M):
        a = tuple(rng.randrange(q) for _ in range(n))
        e = (-1, 1)[rng.randrange(2)] if noisy else 0
        records.append(NoisyLinearRecord(a, (sum(x*s for x, s in zip(a, secret))+e) % q, q, f"known-group-{seed}-{i}"))
        errors.append(e)
    recipe = reflection_recipe(records, mask, B, M)
    return recipe, tuple((x+y) % q for x, y in zip(secret, mask)), tuple(errors)


def literal_readout(recipe, elements):
    q, B, M = int(recipe["modulus"]), recipe["cohorts"], recipe["sites_per_cohort"]
    U, _, _, _ = dense_preparation(recipe["known_phase_numerators"], q)
    if len(elements)*U.shape[0] > 200000:
        raise ValueError("joint literal replay cap exceeded")
    G = NativeGroup(recipe["native_even_level"], recipe["secret_dimension"])
    rows, joint, normalization_error = [], [], 0.
    for g in elements:
        vector = []
        for cohort, labels in zip(recipe["known_phase_numerators"], recipe["public_native_labels"]):
            state = np.ones(1, complex)
            for phases, label in zip(cohort, labels):
                psi = np.exp(2j*np.pi*np.array(phases)/q)/np.sqrt(3)
                state = np.kron(state, G.induced_action(label, g)@psi)
            vector.extend(state/np.sqrt(B))
        after = U.conj().T@np.array(vector)
        normalization_error = max(normalization_error, abs(float(np.vdot(after, after).real)-1))
        rows.append((complex(after[0]), float(np.sum(abs(after[1:])**2))))
        joint.append(after/np.sqrt(len(elements)))
    return rows, normalization_error, np.array(joint)


def amplification_control(start, zero, correct, accepted, Phi, iterations=6):
    state, rows = start.copy(), []
    p_value = float(np.sum(abs(start[:, 0])**2))
    theta = np.arcsin(np.sqrt(min(1., max(0., p_value))))
    for j in range(iterations+1):
        a = amplitude_polynomial(j)
        gain = fmpq_poly()
        for k in reversed(range(len(a))): gain = (gain*zero+int(a[k])) % Phi
        amplified = (zero*gain*gain) % Phi
        amplified_correct, amplified_accepted = (correct*gain*gain) % Phi, (accepted*gain*gain) % Phi
        observed = float(np.sum(abs(state[:, 0])**2))
        if abs(observed-np.sin((2*j+1)*theta)**2) > 2e-10:
            raise ArithmeticError("actual whole-preparation amplification differs from its paid sine law")
        rows.append({"iterations": j, "source_zero_mass_exact": encode_field(amplified),
                     "correct_and_zero_mass_exact": encode_field(amplified_correct),
                     "candidate_and_zero_mass_exact": encode_field(amplified_accepted),
                     "actual_zero_probability": observed,
                     "amplification_gain_polynomial_ascending": tuple(str(a[k]) for k in range(len(a))),
                     "pure_joint_preparation_or_inverse_calls": 2*j+1,
                     "normalized_good_distribution_changed": False})
        reflected = state.copy()
        reflected[:, 0] *= -1
        state = 2*start*np.vdot(start, reflected)-reflected
    return {"exact_initial_zero_mass": encode_field(zero), "iteration_history": rows,
            "whole_orbit_reflection_is_actual_known_preparation_reflection": True,
            "point_gate_reflection_is_unknown_input_copy_reflection": False,
            "normalization_is_free": False}


def finite_control(n, r, B, M, noisy, seed):
    recipe, secret, errors = source_fixture(n, r, B, M, noisy, seed)
    q, L = 3**r, 2*r
    Phi, powers, conjugate = tools = finite_field(q)
    G = NativeGroup(L, n)
    native_secret = tuple((s, 0) for s in secret)
    H = set(G.hidden_elements(native_secret))
    support = central_support(recipe["public_native_labels"], L)
    C = len(set(tuple(x) for x in support["cohort_central_character_rows"]))
    overlap = fmpq_poly()
    for b in range(B):
        part = powers[0]
        for j in range(M):
            e, f = errors[2*(b*M+j):2*(b*M+j)+2]
            part = (part*(1+powers[e % q]+powers[f % q])/3) % Phi
        overlap += part/B
    distance2 = (1-overlap*conjugate(overlap)) % Phi
    out = []
    kernel, coefficients, counts = integer_kernel_exact(recipe)
    for domain in (FULL, SLICE):
        elements = finite_elements(recipe, domain)
        diagnostics, norm_error, joint = literal_readout(recipe, elements)
        rows, zero_total, correct_total, accepted_total = [], fmpq_poly(), fmpq_poly(), fmpq_poly()
        for g, (literal, other) in zip(elements, diagnostics):
            m = scalar_overlap_exact(recipe, g, tools)
            p = (m*conjugate(m)) % Phi
            value = sum(float(m[i])*np.exp(2j*np.pi*i/q) for i in range(len(m)))
            if abs(value-literal) > 2e-10 or abs(abs(value)**2+other-1) > 2e-10:
                raise ArithmeticError("actual controlled native action/inverse differs from exact zero branch")
            candidate = decoded_candidate(G, g)
            correct = candidate == native_secret
            rows.append({"group_element": g, "source_zero_amplitude_exact": encode_field(m),
                         "source_zero_probability_exact": encode_field(p),
                         "source_nonzero_probability_exact": encode_field((1-p) % Phi),
                         "decoded_candidate": candidate, "candidate_matches_truth_fixture": correct,
                         "literal_source_zero_amplitude": (literal.real, literal.imag)})
            zero_total += p/len(elements)
            if candidate is not None: accepted_total += p/len(elements)
            if correct: correct_total += p/len(elements)
        zero_total, correct_total, accepted_total = (p % Phi for p in (zero_total, correct_total, accepted_total))
        if domain == SLICE:
            kzero = fmpq_poly(list(reversed([fmpq(x) for x in kernel["actual_source_zero_mass_exact"]])))
            if zero_total != kzero:
                raise ArithmeticError("actual group law disagrees with weighted Fourier Parseval")
            # Check the complete Fourier law, including empty frequency fibres.
            for sigma in kernel["frequencies"]:
                transformed = fmpq_poly()
                for row, g in zip(rows, elements):
                    bvec = tuple(a for a, _ in g[0])
                    m = fmpq_poly(list(reversed([fmpq(x) for x in row["source_zero_amplitude_exact"]])))
                    phase = -sum(x*y for x, y in zip(sigma, bvec)) % q
                    transformed += m*powers[phase]/len(elements)
                if transformed % Phi != coefficients.get(tuple(sigma), fmpq_poly()):
                    raise ArithmeticError("joint work Fourier transform does not give actual fibre coefficients")
        out.append({"recipe": domain_recipe(recipe, domain), "group_rows": rows,
                    "source_zero_mass_exact": encode_field(zero_total),
                    "nonidentity_candidate_and_zero_mass_exact": encode_field(accepted_total),
                    "correct_decoding_and_zero_mass_exact": encode_field(correct_total),
                    "maximum_literal_total_probability_error": norm_error,
                    "literal_group_source_Schmidt_rank": int(np.sum(np.linalg.svd(joint, compute_uv=False) > 1e-10)),
                    "actual_whole_preparation_amplification": amplification_control(joint, zero_total, correct_total, accepted_total, Phi),
                    "full_group_central_conditional_correct_upper": str(min(fmpq(1), fmpq(C, 3**n))) if domain == FULL else None,
                    "full_group_ceiling_applied_to_integer_slice": False})
    return {"source_recipe": recipe, "truth_fixture_only": {"masked_integer_secret": secret, "errors": errors},
            "central_support": support, "distinct_central_characters": C,
            "actual_vs_ideal_pure_trace_distance_squared_exact": encode_field(distance2),
            "integer_kernel": kernel, "domain_controls": out,
            "true_hidden_subgroup_fixture": tuple(sorted(H)),
            "secret_or_errors_used_by_group_compiler": False, "accepted_speedup_candidate": False}


def collision_and_noise_ledger(n, r, B, M, moment, amplifications=0):
    integer(n, "positive original secret dimension", 1)
    integer(r, "positive root exponent", 1)
    integer(amplifications, "committed two-reflection iteration count")
    q, N, D = 3**r, 3**(n*r), B*3**M
    bound = reflection_budget(q, B, M, moment, 0, independence=IID)
    e2 = fmpq(bound["mean_pure_trace_distance_squared_upper"])
    collision = fmpq(1, N)+fmpq(N-1, N*D)
    true_lower = max(fmpq(0), 1-4*e2)/N
    conditional = max(fmpq(0), 1-4*e2)/(N*collision)
    factor = (2*amplifications+1)**2
    required_square = fmpq(1, 2)/collision
    root_floor = math.isqrt(int(required_square.numerator)//int(required_square.denominator))
    root_ceil = root_floor if root_floor*root_floor == required_square else root_floor+1
    required_iterations = root_ceil//2
    return {"dimension": n, "root_exponent": r, "native_even_level": 2*r,
            "cohorts": B, "sites_per_cohort": M,
            "integer_secret_count": integer_text(N), "kernel_word_count": integer_text(D),
            "native_backend_within_level_cap": 2*r <= 512,
            "mean_squared_pure_source_error_upper": str(e2),
            "source_error_bound": bound,
            "mean_ideal_collision_mass_exact": str(collision),
            "mean_actual_source_zero_upper": str(collision),
            "mean_correct_and_zero_lower": str(true_lower),
            "ensemble_conditional_correct_lower": str(conditional),
            "ensemble_conditioning_is_over_source_draws_and_quantum_outcomes": True,
            "conditional_correct_lower_is_unamplified_ensemble_statement": True,
            "amplified_ensemble_conditional_correct_lower": None,
            "conditional_event_positive_certified_by_source_bound": true_lower > 0,
            "two_reflection_iteration_count": amplifications,
            "mean_amplified_zero_success_upper": str(min(fmpq(1), factor*collision)),
            "necessary_iterations_for_half_mean_zero_success": integer_text(required_iterations),
            "necessary_iteration_bound_is_sufficient_decoder": False,
            "noise_source_assumptions": bound["IID_promise"],
            "conditional_pure_phase_bound_covers_generic_gate_errors": False,
            "constant_relative_condition_number_implies_free_normalization": False,
            "two_reflection_bound_is_general_quantum_query_lower_bound": False,
            "classical_brute_force_is_best_lattice_baseline": False,
            "efficient_decoder_supplied": False}


def finite_uniform_integer(limit, rng, attempt_cap):
    integer(limit, "positive uniform integer range", 1)
    integer(attempt_cap, "positive bounded uniform attempt cap", 1)
    bits, draws, value = (limit-1).bit_length(), [], None
    for _ in range(attempt_cap):
        candidate = rng.getrandbits(bits)
        if type(candidate) is not int or not 0 <= candidate < 2**bits:
            raise ValueError("canonical independent coin block required")
        draws.append(integer_text(candidate))
        if candidate < limit:
            value = candidate
            break
    return {"range": integer_text(limit), "coin_bits": bits, "draws": draws, "value": value,
            "status": "UNIFORM_INTEGER" if value is not None else "EXPLICIT_COIN_ABORT"}


def computational_readout_shadow(recipe, domain, rng, bits=24, failure_bits=24):
    spec = domain_recipe(recipe, domain)
    n, q, B, M = spec["dimension"], int(spec["modulus"]), recipe["cohorts"], recipe["sites_per_cohort"]
    integer(failure_bits, "positive unconditional coin error bits", 1)
    seed = seed_tensor(recipe, bits)
    components = n if domain == SLICE else 2*n+1
    cap = failure_bits+(components+M).bit_length()
    delta = fmpq(1, 2**bits)
    E = (1+delta)**(3*M+1)*(1+3*delta)**M-1
    abort = fmpq(components+M+1, 2**cap)
    budget = {"domain_recipe": spec, "approximation_bits": bits,
              "per_conditional_source_relative_error_upper": str(E),
              "whole_joint_readout_TV_or_abort_upper": str(min(fmpq(1), 2*E+abort)),
              "uniform_coin_attempt_cap": cap, "unconditional_coin_abort_upper": str(abort),
              "group_measured_early_is_legal_for_this_readout": True,
              "group_Fourier_or_whole_orbit_amplification_covered": False,
              "whole_completion_conditioning_allowed": False,
              "full_group_or_source_table_allocated": False, "secret_or_errors_read": False}
    draws = [finite_uniform_integer(q, rng, cap) for _ in range(n if domain == SLICE else 2*n)]
    if domain == FULL: draws.append(finite_uniform_integer(3, rng, cap))
    if any(d["value"] is None for d in draws):
        return {**budget, "status": "EXPLICIT_GROUP_COIN_ABORT", "group_coin_decisions": draws}
    values = tuple(d["value"] for d in draws)
    g = (tuple((x, 0) for x in values), 1) if domain == SLICE else (tuple(zip(values[:2*n:2], values[1:2*n:2])), values[-1])
    G, g = checked_group(recipe, g)
    terms = []
    for b, term in enumerate(seed.terms):
        factors = list(term.factors)
        for j in range(M):
            phases, label, v = recipe["known_phase_numerators"][b][j], recipe["public_native_labels"][b][j], term.factors[j+1]
            transformed = []
            for out in range(3):
                k = character_exponent(G, label, G.rotate(g[0], out), q)
                x = complex_mul(root_entry(q, k, bits), v[(out+g[1]) % 3])
                transformed.append(complex_mul(root_entry(q, -phases[out], bits), x))
            Fstar = tuple(tuple(complex_conj(fourier_gate(bits)[k][t]) for k in range(3)) for t in range(3))
            factors[j+1] = tuple(sum_complex(complex_mul(x, y) for x, y in zip(row, transformed)) for row in Fstar)
        lo, hi = sqrt_box(fmpq(1, B), bits+B.bit_length()+8)
        factor = (lo+hi)/2
        factors[0] = tuple((factor*((-1)**((b & k).bit_count())), fmpq(0)) for k in range(B))
        terms.append(Term(ONE, tuple(factors)))
    state = TensorState(tuple(terms), seed.shape)
    sampled = sample_basis(state, rng, cap)
    return {**budget, "status": sampled["status"], "group_element": g,
            "group_coin_decisions": draws, "source_sample": sampled,
            "source_tensor_terms": len(state.terms)}


def build_report():
    controls = [finite_control(*p) for p in ((1, 1, 1, 2, False, 85001), (3, 1, 1, 3, False, 85002),
                                            (1, 2, 1, 3, False, 85003), (1, 2, 2, 2, True, 85004))]
    ledgers = []
    for n in (8, 32, 64, 128):
        q, M = 3**n, n*n+24
        V = fmpq(q*q, 3*n**6)+fmpq(1, 2)
        for T in (0, n*n): ledgers.append(collision_and_noise_ledger(n, n, 1, M, V, T))
    shadows = []
    for domain, n, r, B, M, seed in ((FULL, 3, 1, 1, 3, 85002), (SLICE, 1, 2, 2, 2, 85004),
                                   (FULL, 4, 32, 2, 8, 85005), (SLICE, 4, 64, 2, 8, 85006)):
        recipe, _, _ = source_fixture(n, r, B, M, True, seed)
        shadows.append({"source_recipe": recipe, "shadow": computational_readout_shadow(recipe, domain, random.Random(seed+1))})
    dependencies = ("native_state_hsp_bridge.py", "cyclotomic_rescaling_gate.py", "native_noisy_phase_input.py",
                    "known_preparation_coherent_reflection.py", "known_reflection_tensor_simulation.py",
                    "native_noncentral_filter_tradeoff.py", "ternary_certified_noise_sampler.py")
    return {"status": "SCOPED_KNOWN_NATIVE_GROUP_COUPLING_AND_POSTSELECTION_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in dependencies},
            "finite_actual_group_controls": controls, "scalable_collision_noise_price_ledgers": ledgers,
            "computational_readout_classical_shadows": shadows,
            "research_decision": "SEEK_STRUCTURAL_FIBRE_PROCESSING_NOT_FREE_POSTSELECTION_OR_SEED_ONLY_COHERENCE",
            "unknown_quantum_only_input_inverse_supplied": False,
            "integer_slice_excluded_by_full_group_central_ceiling": False,
            "early_measurement_simulates_arbitrary_group_interference": False,
            "efficient_full_decoder_supplied": False, "physical_quantum_hardware_executed": False,
            "hardness_transfer_admitted": False, "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "actual_group_controls": len(report["finite_actual_group_controls"]),
                      "scalable_ledgers": len(report["scalable_collision_noise_price_ledgers"]),
                      "classical_shadows": len(report["computational_readout_classical_shadows"]),
                      "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__":
    main()
