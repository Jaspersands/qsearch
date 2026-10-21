"""Explicit folded norm-character source, base-field rank and finite readout.

Known DQI/character mechanism, local application review pending. Bounded DFT
controls are not scalable quantum executions; the actual folded decoder is a
separate classical component. No hardness or speedup follows from this report.
"""

from __future__ import annotations

import argparse
import cmath
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import random
import sys

import numpy as np
from flint import fmpq, fmpz, fmpz_mod_ctx, fmpz_mod_mat, fq_default_ctx

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.folded_rs_decoder import parameters as decoder_parameters, vandermonde_syndrome
from theorems.prime_character_capacity_source import chi, coherent_distance_squared, rational
from theorems.prime_character_finite_readout import (dyadic_lower, mean_tail_lower,
                                                    propose_weights, rayleigh_interval,
                                                    sqrt_interval)
from theorems.prime_character_opi import ring

REPORT = ROOT / "research/classical_baselines/folded_norm_source.json"


def fraction(value):
    """Parse large exact certificates without changing Python's global limits."""
    if isinstance(value, str):
        q = fmpq(value)
        return Fraction(int(q.numerator), int(q.denominator))
    return Fraction(value)


@lru_cache(maxsize=12)
def extension_model(p, m):
    """Public irreducible-polynomial search and actual trace-dual computation."""
    R = ring(p)
    integer(m, "extension degree", 1, 63)
    rng = random.Random((p << 8) ^ m ^ 4801)
    tested, modulus = 0, None
    for _ in range(2048):
        coefficients = [rng.randrange(p) for _ in range(m)] + [1]
        tested += 1
        candidate = R(coefficients)
        if candidate.is_irreducible():
            modulus = candidate
            break
    if modulus is None:
        raise ValueError("public irreducible setup budget exhausted; not problem hardness")
    E = fq_default_ctx(modulus=modulus)
    basis = tuple(E.gen() ** i for i in range(m))
    gram = [[int((a*b).trace()) for b in basis] for a in basis]
    matrix = fmpz_mod_mat(gram, fmpz_mod_ctx(p))
    inverse = matrix.inv()
    if matrix * inverse != fmpz_mod_mat([[int(i == j) for j in range(m)] for i in range(m)], fmpz_mod_ctx(p)):
        raise ArithmeticError("computed trace-dual pairing is not the identity")
    determinant_character = chi(p, int(matrix.det()))
    if not determinant_character:
        raise ArithmeticError("finite-field trace pairing is degenerate")
    # Sum_z psi(z^2) is the trace-form quadratic Gauss sum. Diagonalizing
    # its Gram matrix gives chi_p(det G)*tau_p^m, retaining the actual sign.
    gauss_power = ((m if p % 4 == 3 else 0) + 2 * (determinant_character == -1)) % 4
    return {"p": p, "m": m, "Q": p ** m, "field": E, "basis": basis,
            "inverse_gram": tuple(tuple(int(inverse[i, j]) for j in range(m)) for i in range(m)),
            "gauss_unit_i_power": gauss_power,
            "record": {"p_decimal": str(p), "extension_degree": m,
                       "modulus_coefficients": list(map(int, modulus.coeffs())),
                       "irreducibility_tests_charged": tested,
                       "public_setup_uses_affine_target": False,
                       "trace_Gram_matrix": gram,
                       "trace_Gram_inverse": [[int(inverse[i, j]) for j in range(m)] for i in range(m)],
                       "trace_Gram_determinant_character": determinant_character,
                       "canonical_Gauss_unit_i_power": gauss_power,
                       "nonzero_Fourier_probabilities_flat": (p ** m) % 4 == 3,
                       "field_table_enumerated": False}}


def character(model, z):
    return chi(model["p"], int(z.norm()))


def dual_frequency(model, coordinates):
    p, m = model["p"], model["m"]
    if len(coordinates) != m or any(type(a) is not int or not 0 <= a < p for a in coordinates):
        raise ValueError("canonical base-field frequency vector required")
    return model["field"]([sum(row[j]*coordinates[j] for j in range(m)) % p
                           for row in model["inverse_gram"]])


def local_fourier(model, shift, sign, frequency, *, include_zero=True, gauss_override=None):
    """Numeric formula ONLY for bounded controls; large records remain exact."""
    p, Q = model["p"], model["Q"]
    if Q > 4096:
        raise ValueError("numerical Fourier controls are bounded, not large-field synthesis")
    if sign not in (-1, 1) or type(sign) is not int or type(include_zero) is not bool:
        raise ValueError("explicit sign and zero policy required")
    lam = dual_frequency(model, frequency)
    if lam == 0:
        return 0j
    phase = cmath.exp(-2j*math.pi*int((lam*shift).trace()) / p)
    tau = (1j ** model["gauss_unit_i_power"] if gauss_override is None else gauss_override) * math.sqrt(Q)
    eta = 1 if include_zero else -1
    return phase*(eta + sign*character(model, -lam)*tau) / math.sqrt(Q*Q - 1)


def block_ambiguity(p, n, m, K, ell):
    """Whole block ball, SCALAR rank K, no extension-linear-code assumption."""
    ring(p)
    integer(n, "folded blocks", 1, 4096)
    integer(m, "symbols per block", 1, 63)
    integer(K, "scalar syndrome rank", 1, n*m)
    integer(ell, "source radius strictly below scalar capacity", 0, min(n, (K - 1) // m))
    if n*m > p - 1:
        raise ValueError("distinct nonzero scalar evaluation points must exist")
    Q, spheres = p ** m, []
    for j in range(ell + 1):
        numerator = 0
        for r in range(ell + 1):
            dimension = m*(j + r) - K
            if dimension <= 0:
                continue
            for h in range(max(0, j + r - n), min(j, r, (dimension - 1) // m) + 1):
                # The shared-support image has dimension m*h and cannot
                # contain an error whose exact support is ALL of S.
                supports = math.comb(j, h)*math.comb(n - j, r - h)
                numerator += supports*(p ** dimension - p ** (m*h))
        spheres.append(min(Fraction(1), Fraction(numerator, (Q - 1) ** j)))
    epsilon = max(spheres)
    fiber = sum(math.comb(n, r) for r in range(ell + 1))
    return {"p_decimal": str(p), "n_blocks": n, "m_fold": m, "scalar_rank_K": K, "ell": ell,
            "whole_ball_competitors_included": True, "MDS_scalar_column_independence_required": True,
            "extension_linear_code_assumed": False,
            "intersection_dimension_formula": "m*(j+r)-K over F_p when union scalar rank is K",
            "sphere_bad_mass_upper_exact": [rational(q) for q in spheres],
            "any_radial_weight_bad_mass_upper_exact": rational(epsilon),
            "max_fiber_size_support_bound_decimal": str(fmpz(fiber)),
            "unique_source_mass_lower_exact": rational(1 - epsilon),
            "unique_herald_vs_ideal_trace_distance_squared_upper_exact": rational(coherent_distance_squared(epsilon, fiber)),
            "error_or_field_vectors_enumerated": False}


def score_certificate(p, n, m, K, ell, *, include_zero=True, thresholds=(), pruning_trials=4096):
    """Local Gram application; CONDITIONAL on exact source and error decoder."""
    if p % 4 != 3 or m % 2 != 1 or type(include_zero) is not bool:
        raise ValueError("flat source requires p3mod4 and odd extension degree")
    source = block_ambiguity(p, n, m, K, ell)
    rho = Fraction(p ** m + (1 if include_zero else -1), 2*p ** m)
    rayleigh = rayleigh_interval(n, rho, propose_weights(n, rho, ell))
    result = {"source": source, "density_exact": rational(rho), "rayleigh": rayleigh,
              "result_requires_exact_source_and_verified_decoder": True,
              "quantum_source_decoder_circuit_or_runtime_advantage_implemented": False,
              "local_application_independent_review_pending": True}
    exact = m*(2*ell + 1) <= K
    if not exact and m*(ell + 1) >= K:
        return result | {"status": "UNKNOWN_OBSERVABLE_RADIUS_REACHES_SCALAR_CAPACITY", "finite_mean_certified": False}
    companion = None if exact else block_ambiguity(p, n, m, K, ell + 1)
    epsilon = Fraction(0) if exact else fraction(companion["any_radial_weight_bad_mass_upper_exact"])
    fiber = 1 if exact else int(fmpz(companion["max_fiber_size_support_bound_decimal"]))
    delta = max(1, fiber - 1)*epsilon
    result |= {"observable_extra_block_radius": ell + 1, "extra_radius_companion": companion,
               "Gram_operator_error_upper_exact": rational(dyadic_upper(delta)),
               "exact_scalar_MDS_moment_regime": exact}
    if delta >= 1:
        return result | {"status": "UNKNOWN_GRAM_BOUND_TOO_WEAK", "finite_mean_certified": False}
    error = 2*delta/(1 - delta)
    _, tv = sqrt_interval(fraction(source["unique_herald_vs_ideal_trace_distance_squared_upper_exact"]))
    lower = max(Fraction(0), fraction(rayleigh["ambient_Rayleigh_lower_exact"]) - error - tv)
    success = fraction(source["unique_source_mass_lower_exact"])
    # The finite source theorem assumes exact unique decoding. Separately
    # pay worst-case randomized pruning failure before using this receiver.
    order = min(4, m)
    decoder_parameters(p, n, m, n*m - K, 3, ell, order)
    integer(pruning_trials, "charged independent decoder pruning trials", 1, 100000)
    gap = Fraction(n - ell - (n*m - K - 1) // m, n)
    miss = (1 - gap ** (order - 1)) ** pruning_trials
    missing_source_mass = fraction(source["any_radial_weight_bad_mass_upper_exact"]) + miss
    _, decoder_trace = sqrt_interval(min(Fraction(1), missing_source_mass))
    decoder_trace = min(Fraction(1), 2*decoder_trace)
    per_attempt = max(Fraction(0), success*lower - decoder_trace)
    return result | {"status": "CONDITIONAL_FINITE_MEAN_LOCAL_REVIEW_PENDING", "finite_mean_certified": True,
                     "heralded_mean_lower_exact": rational(dyadic_lower(lower)),
                     "herald_output_TV_upper_exact": rational(tv),
                     "tails": [{"accepted_count": threshold,
                                "exact_unique_decoder_one_attempt_lower_exact": rational(dyadic_lower(success*mean_tail_lower(n, lower, threshold))),
                                "bounded_pruning_one_attempt_lower_exact": rational(dyadic_lower(max(Fraction(0), success*mean_tail_lower(n, lower, threshold) - decoder_trace)))}
                               for threshold in thresholds],
                     "bounded_decoder_loss": {"interpolation_order_s": order, "affine_dimension_upper": order - 1,
                                              "pruning_agreement_gap_exact": rational(gap),
                                              "independent_pruning_trials_charged": pruning_trials,
                                              "per_unique_error_miss_upper_128bit_dyadic": rational(dyadic_upper(miss)),
                                              "full_flagged_output_trace_error_upper_exact": rational(decoder_trace),
                                              "per_attempt_expected_normalized_score_lower_exact": rational(dyadic_lower(per_attempt)),
                                              "failure_score_is_zero": True,
                                              "premise": "fresh classical uniform blocks before each preparation, native reversible decoder returns a validated error or failure; no circuit compilation/synthesis error included"},
                     "binomial_score_distribution_assumed": False, "accepted_speedup_candidate": False}


def dyadic_upper(value, bits=128):
    scale = 1 << bits
    return Fraction(-(-value.numerator*scale // value.denominator), scale)


def block_ball_envelope(p, n, m, K, radius):
    """Compact universal MDS bound; no vectors, support lists or 2^n integers.

    Bounds assume the actual native distinct-point Vandermonde map. Geometry
    feasibility is checked here; a specific matrix/generator is not supplied.
    """
    ring(p)
    if type(n) is not int or n < 1:
        raise ValueError("positive integer block count required")
    integer(m, "scalar symbols per block", 1, 63)
    integer(K, "native scalar rank", 1, n*m)
    integer(radius, "whole-ball radius", 0, min(n, (K - 1)//m))
    if n*m > p - 1 or p ** m < 2*n:
        raise ValueError("distinct-point geometry and Q>=2n required")
    gap = K - m*radius
    # M<=2^n and (1-1/Q)^(-radius)<=2. Replace p^(-gap) by
    # 2^(-gap) only in the last, deliberately coarse, universal bound.
    return {"n_blocks": n, "m_fold": m, "scalar_rank_K": K, "whole_ball_radius": radius,
            "scalar_capacity_gap": gap,
            "support_count_upper_symbolic": "2^n",
            "sphere_bad_mass_upper_symbolic": "2^(n+1)*p^(-scalar_capacity_gap)",
            "sphere_bad_mass_power_two_upper_exponent": n + 1 - gap,
            "radial_Gram_error_power_two_upper_exponent": 2*n + 1 - gap,
            "assumes_actual_distinct_point_scalar_Vandermonde_map": True,
            "actual_generator_or_matrix_verified_here": False,
            "extension_linear_code_assumed": False,
            "support_lists_field_tables_or_exponential_integers_constructed": False,
            "nonnegative_exponent_is_inconclusive_not_hardness": True}


def quarter_turn_source_bound(p, m, ell):
    """Trace bound for dropping only the tiny real part of each local phase.

    KEEP the computed Gauss unit on EVERY active block. This is not permission
    to discard relative radial phases or to change the field's Gauss sign.
    """
    ring(p)
    integer(m, "odd flat-source degree", 1, 63)
    if p % 4 != 3 or m % 2 == 0 or type(ell) is not int or ell < 0:
        raise ValueError("flat odd-extension source and nonnegative radius required")
    square_bound = min(Fraction(1), Fraction(ell, p ** m + 1))
    return {"maximum_active_blocks": ell,
            "full_source_pure_trace_distance_squared_upper_exact": rational(square_bound),
            "single_block_overlap_squared_exact": rational(Fraction(p ** m, p ** m + 1)),
            "premises": ["uniform independent nonzero E labels conditional on each support",
                         "same support/radial amplitudes in both sources",
                         "same computed Gauss unit, sign character and public shift phase",
                         "replace (eta+c*tau_E)/sqrt(Q+1) by c*tau_E/sqrt(Q), eta=+/-1"],
            "both_zero_policies_covered": True,
            "per_active_block_Gauss_unit_must_be_retained": True,
            "full_flagged_output_trace_cannot_increase_under_same_receiver": True,
            "conditional_postselected_output_has_no_such_unpaid_guarantee": True,
            "independent_source_phase_bound_not_a_compiled_circuit": True}


def uniform_family_certificate(p, n, *, synthesis_trace_budget=Fraction(1, 1000)):
    """All-n arithmetic theorem for a SPECIFIED known-mechanism composition.

    Not a circuit execution or a speedup theorem. Public field/generator
    validity and the full flagged synthesis trace budget remain explicit.
    """
    ring(p)
    if type(n) is not int or n < 3200 or n % 100:
        raise ValueError("n must be a multiple of100 at least3200")
    if p % 4 != 3 or p - 1 < 4*(31*n) ** 2:
        raise ValueError("p3mod4 and p-1>=4*(31n)^2 required")
    if (not isinstance(synthesis_trace_budget, (int, Fraction))
            or isinstance(synthesis_trace_budget, bool)
            or not 0 <= synthesis_trace_budget <= Fraction(1, 1000)):
        raise ValueError("exact full flagged synthesis trace budget in [0,1/1000] required")
    synthesis_trace_budget = Fraction(synthesis_trace_budget)
    m, K, ell, width, order, trials = 31, 62*n//5, n//4, 32, 4, 8192
    envelope = block_ball_envelope(p, n, m, K, ell + 1)
    delta = Fraction(1, 1 << 64)
    if envelope["radial_Gram_error_power_two_upper_exponent"] > -64:
        raise ArithmeticError("the advertised uniform Gram envelope failed")
    tv, gram, source_loss = Fraction(1, 10 ** 8), Fraction(1, 10 ** 12), Fraction(1, 10 ** 6)
    if tv*tv < 2*delta or 2*delta/(1 - delta) > gram or gram + tv + delta > source_loss:
        raise ArithmeticError("source/herald/Gram loss budget not proved")
    C, decoded_dimension = n*(m - order + 1), n*m - K
    D = (C - decoded_dimension + 1)//(order + 1)
    root_margin = (n - ell)*(m - order + 1) - (D + decoded_dimension - 1)
    gap = Fraction(n - ell - (decoded_dimension - 1)//m, n)
    miss_upper, decoder_loss = Fraction(1, 10 ** 12), Fraction(1, 10 ** 5)
    worst_miss_base = 1 - Fraction(3, 20) ** (order - 1)
    if (root_margin <= 0 or gap < Fraction(3, 20)
            or worst_miss_base ** trials > miss_upper
            or 4*(delta + miss_upper) > decoder_loss ** 2):
        raise ArithmeticError("bounded native decoder does not meet the uniform budget")
    link_product = (Fraction(1, 4) - Fraction(width - 2, n))*Fraction(3, 4)
    sqrt_floor = Fraction(531, 1250)
    if link_product < Fraction(231, 1280) or sqrt_floor ** 2 > Fraction(231, 1280):
        raise ArithmeticError("explicit uniform-window Rayleigh witness failed")
    # Both zero policies: diagonal>=1/2-1/(2Q)>=999/2000;
    # 2sqrt(rho(1-rho))=sqrt(1-Q^-2)>=1-Q^-1>=999/1000.
    ambient = Fraction(999, 2000) + Fraction(width - 1, width)*Fraction(999, 1000)*sqrt_floor
    mean = ambient - source_loss - decoder_loss - synthesis_trace_budget
    tail = mean_tail_lower(n, mean, 9*n//10)
    if mean < Fraction(909, 1000) or tail < Fraction(9, 100):
        raise ArithmeticError("uniform score/tail floor did not survive the paid losses")
    return {"status": "CONDITIONAL_UNIFORM_FAMILY_ARITHMETIC_THEOREM_REVIEW_PENDING",
            "p_decimal": str(fmpz(p)), "n_blocks": n, "m_fold": m, "scalar_rank_K": K,
            "ell": ell, "both_zero_policies_covered": True,
            "valid_for_all_fixed_public_shifts_and_signs": True,
            "public_input_premises": ["verified degree31 irreducible modulus and its stated coordinate basis",
                                      "verified gamma with first31n powers distinct over F_p",
                                      "same explicit native F_p coefficient domain for both parties"],
            "source_window": {"first_weight": ell - width + 1, "last_weight": ell,
                              "nonzero_unnormalized_weights": [1]*width, "squared_norm": width},
            "optional_quarter_turn_source_approximation": quarter_turn_source_bound(p, m, ell),
            "quarter_turn_error_must_fit_WITHIN_not_above_total_synthesis_budget": True,
            "extra_radius_envelope": envelope,
            "coarse_Gram_and_source_bad_mass_upper_exact": rational(delta),
            "source_Gram_herald_mean_loss_budget_exact": rational(source_loss),
            "native_decoder": {"decoded_polynomial_dimension": decoded_dimension,
                               "interpolation_order": order, "interpolation_D": D,
                               "strict_root_margin": root_margin,
                               "affine_dimension_upper": order - 1,
                               "pruning_gap_exact": rational(gap), "independent_pruning_trials": trials,
                               "miss_bound_expression": "(7973/8000)^8192 <= 1/10^12",
                               "full_flagged_decoder_trace_budget_exact": rational(decoder_loss)},
            "ambient_window_Rayleigh_lower_exact": rational(ambient),
            "full_flagged_synthesis_trace_budget_exact": rational(synthesis_trace_budget),
            "per_attempt_mean_lower_exact": rational(mean),
            "uniform_mean_floor_exact": "909/1000", "target_accepted_count": 9*n//10,
            "integer_support_tail_lower_exact": rational(tail),
            "uniform_one_attempt_target_probability_floor_exact": "9/100",
            "failure_outputs_have_score_zero": True,
            "binomial_or_IID_shift_assumption": False,
            "setup_order_sampling": {"bad_gamma_fraction_upper": "1/8",
                                     "distinct_power_test_field_products_per_trial": n*m,
                                     "does_not_certify_any_deterministic_seed": True,
                                     "not_a_free_high_order_generator_oracle": True},
            "polynomial_reversible_upper_scale_not_gate_count": "For positive synthesis error: O((31n)^3+8192*(31n)^2)*poly(log p, log(1/synthesis_error)) plus explicit source and F_p Fourier circuits",
            "zero_synthesis_budget_is_an_ideal_limit_not_a_finite_gate_claim": True,
            "arithmetic_only_no_field_table_support_enumeration_or_eigenproblem": True,
            "large_quantum_circuit_compiled_or_executed": False,
            "actual_public_input_or_synthesis_error_verified_here": False,
            "classical_hardness_runtime_advantage_novelty_or_candidate_admission": False}


def physical_control(include_zero=True):
    """Charged full source/erasure/FFT calibration, NOT a scalable receiver."""
    p, n, m, K = 7, 2, 3, 4
    model, points = extension_model(p, m), [pow(3, j, p) for j in range(n*m)]
    E = model["field"]
    shifts, signs = [E([1, 2, 0]), E([3, 1, 4])], [1, -1]
    amplitudes, wrong_amplitudes, quarter_amplitudes = ([1/math.sqrt(2)] for _ in range(3))
    errors, buckets = [(0,)*(n*m)], {}
    buckets[(0,)*K] = [0]
    for block in range(n):
        for frequency in product(range(p), repeat=m):
            if not any(frequency):
                continue
            error = [0]*(n*m)
            error[block*m:(block + 1)*m] = frequency
            syn = tuple(vandermonde_syndrome(p, points, error, K))
            buckets.setdefault(syn, []).append(len(errors))
            errors.append(tuple(error))
            amplitudes.append(local_fourier(model, shifts[block], signs[block], frequency, include_zero=include_zero) / 2)
            wrong_amplitudes.append(local_fourier(model, shifts[block], signs[block], frequency, include_zero=include_zero, gauss_override=1j) / 2)
            lam = dual_frequency(model, frequency)
            public_phase = cmath.exp(-2j*math.pi*int((lam*shifts[block]).trace()) / p)
            quarter_amplitudes.append(public_phase*signs[block]*character(model, -lam)
                                      * (1j ** model["gauss_unit_i_power"]) / (2*math.sqrt(model["Q"] - 1)))
    ideal, good, wrong, quarter_good = (np.zeros((p,)*K, complex) for _ in range(4))
    bad_mass = 0.0
    for syn, indices in buckets.items():
        ideal[syn] = sum(amplitudes[i] for i in indices)
        wrong[syn] = sum(wrong_amplitudes[i] for i in indices)
        if len(indices) == 1:
            good[syn] = amplitudes[indices[0]]
            quarter_good[syn] = quarter_amplitudes[indices[0]]
        else:
            bad_mass += sum(abs(amplitudes[i]) ** 2 for i in indices)
    source_norm = sum(abs(a) ** 2 for a in amplitudes)
    ideal_out, good_out, wrong_out = [np.fft.ifftn(a)*math.sqrt(p ** K) for a in (ideal, good, wrong)]
    rho = Fraction(model["Q"] + (1 if include_zero else -1), 2*model["Q"])
    native = np.zeros((p,)*K, complex)
    for coeffs in product(range(p), repeat=K):
        vals = [sum(a*pow(x, j, p) for j, a in enumerate(coeffs)) % p for x in points]
        gs = []
        for i in range(n):
            z = E(vals[i*m:(i + 1)*m]) - shifts[i]
            accepted = character(model, z) == signs[i] or (include_zero and z == 0)
            gs.append((int(accepted) - float(rho)) / math.sqrt(float(rho*(1 - rho))))
        native[coeffs] = (1/math.sqrt(2) + sum(gs)/2) / math.sqrt(p ** K)
    gram_error = float(np.max(abs(native - ideal_out)))
    if abs(source_norm - 1) > 1e-11 or gram_error > 1e-11:
        raise ArithmeticError("native block predicate and coherent Fourier source disagree")
    a, b = abs(ideal_out) ** 2, abs(wrong_out) ** 2
    wrong_tv = float(np.sum(abs(a/a.sum() - b/b.sum())) / 2)
    quarter_norm = sum(abs(a) ** 2 for a in quarter_amplitudes)
    overlap = sum(a.conjugate()*b for a, b in zip(quarter_amplitudes, amplitudes))
    phase_trace_squared = max(0.0, 1 - abs(overlap) ** 2)
    phase_bound = quarter_turn_source_bound(p, m, 1)
    good_mass, quarter_good_mass = float(np.vdot(good, good).real), float(np.vdot(quarter_good, quarter_good).real)
    success_overlap = np.vdot(good, quarter_good)
    # Success is a subnormalized pure output; collapse ALL failure registers
    # to one classical flag. No renormalization/postselection shortcut.
    flagged_trace = (math.sqrt(max(0.0, (good_mass + quarter_good_mass) ** 2 - 4*abs(success_overlap) ** 2))
                     + abs(good_mass - quarter_good_mass))/2
    if (abs(quarter_norm - 1) > 1e-11
            or phase_trace_squared > float(fraction(phase_bound["full_source_pure_trace_distance_squared_upper_exact"])) + 1e-12
            or flagged_trace ** 2 > phase_trace_squared + 1e-12):
        raise ArithmeticError("quarter-turn phase approximation violated the paid full-source trace bound")
    return {"p": p, "n_blocks": n, "m_fold": m, "scalar_rank_K": K,
            "include_zero": include_zero, "field": model["record"],
            "source_errors_enumerated_charged": len(errors), "native_messages_enumerated_charged": p ** K,
            "source_norm": source_norm, "source_ambiguous_mass": bad_mass,
            "unique_herald_probability": float(np.vdot(good_out, good_out).real),
            "native_filter_vs_full_FFT_max_error": gram_error,
            "wrong_prime_field_Gauss_sign_changes_native_output_TV": wrong_tv,
            "quarter_turn_phase_approximation": {"source_norm": quarter_norm,
                                                "source_overlap_real": float(overlap.real),
                                                "source_overlap_imaginary": float(overlap.imag),
                                                "source_trace_squared": phase_trace_squared,
                                                "full_success_failure_flagged_trace": flagged_trace,
                                                "analytic_bound": phase_bound},
            "ambiguity_bound": block_ambiguity(p, n, m, K, 1),
            "finite_mean_status": score_certificate(p, n, m, K, 1, include_zero=include_zero)["status"],
            "exhaustive_decoder_is_not_the_scalable_folded_decoder": True}


def run_controls():
    large = []
    p, m = (1 << 61) - 1, 31
    model = extension_model(p, m)
    for n, K, ell in ((25, 310, 6), (65, 806, 15), (127, 1550, 30)):
        # A strict native decoder root-count certificate, not a free oracle.
        _, D = decoder_parameters(p, n, m, n*m - K, 3, ell, 4)
        large.append({"n_blocks": n, "scalar_rank_K": K, "ell": ell,
                      "decoder_interpolation_D": D,
                      "field": model["record"],
                      "no_large_quantum_or_full_field_table_executed": True,
                      "score": score_certificate(p, n, m, K, ell, thresholds=(math.ceil(.85*n), math.ceil(.9*n)))})
    return {"schema_version": "folded-norm-source-v2", "physical_controls": [physical_control(z) for z in (True, False)],
            "large_analytic_source_and_score_controls": large,
            "uniform_family_arithmetic_certificates": [uniform_family_certificate(p, n) for n in (3200, 1000000)],
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("folded_rs_decoder.py", "prime_character_capacity_source.py", "prime_character_finite_readout.py", "prime_character_opi.py", "bpqm_gibbs_frontier.py")},
            "quantum_speedup_or_classical_hardness_claimed": False,
            "literature": ["https://kconrad.math.uconn.edu/blurbs/gradnumthy/Gauss-Jacobi-sums.pdf",
                           "https://arxiv.org/abs/2610.12357",
                           "https://arxiv.org/abs/2601.07137",
                           "https://arxiv.org/abs/1503.09016"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"physical": [{"zero_included": r["include_zero"], "Fourier_error": r["native_filter_vs_full_FFT_max_error"],
                                   "wrong_sign_TV": r["wrong_prime_field_Gauss_sign_changes_native_output_TV"]} for r in report["physical_controls"]],
                      "large": [{"n": r["n_blocks"], "K": r["scalar_rank_K"], "ell": r["ell"],
                                 "status": r["score"]["status"],
                                 "conditional_mean_lower": float(fraction(r["score"].get("heralded_mean_lower_exact", "0")))}
                                for r in report["large_analytic_source_and_score_controls"]],
                      "uniform_family_arithmetic_ONLY": [{"n": r["n_blocks"],
                                                          "target_accepted_count": r["target_accepted_count"],
                                                          "mean_lower": r["per_attempt_mean_lower_exact"],
                                                          "one_attempt_target_probability_floor": r["uniform_one_attempt_target_probability_floor_exact"],
                                                          "compiled_or_executed": r["large_quantum_circuit_compiled_or_executed"]}
                                                         for r in report["uniform_family_arithmetic_certificates"]]}, indent=2))


if __name__ == "__main__":
    main()
