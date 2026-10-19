"""Independent field arithmetic, phases, scalar-rank collisions and score gates."""

from fractions import Fraction
import cmath
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import sys

import pytest

import theorems.folded_norm_source as module
from theorems.folded_norm_source import (REPORT, block_ambiguity, block_ball_envelope, dual_frequency,
                                        extension_model, fraction, local_fourier,
                                        physical_control, quarter_turn_source_bound, run_controls,
                                        score_certificate, uniform_family_certificate)
from theorems.folded_rs_decoder import parameters as decoder_parameters
from theorems.prime_character_finite_readout import rayleigh_interval


def multiply(a, b, p, modulus):
    m = len(modulus) - 1
    out = [0]*(2*m - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x*y) % p
    for i in range(2*m - 2, m - 1, -1):
        for j in range(m):
            out[i - m + j] = (out[i - m + j] - out[i]*modulus[j]) % p
    return tuple(out[:m])


def power(a, exponent, p, modulus):
    result = (1,) + (0,)*(len(a) - 1)
    while exponent:
        if exponent & 1:
            result = multiply(result, a, p, modulus)
        a = multiply(a, a, p, modulus)
        exponent //= 2
    return result


def character(a, p, modulus):
    if not any(a):
        return 0
    result = power(a, (p ** len(a) - 1) // 2, p, modulus)
    assert not any(result[1:]) and result[0] in (1, p - 1)
    return 1 if result[0] == 1 else -1


@pytest.mark.parametrize("p,m", [(3, 3), (7, 3), (3, 2), (5, 1)])
def test_norm_character_and_trace_pairing_against_independent_polynomial_arithmetic(p, m):
    model = extension_model(p, m)
    modulus, E = model["record"]["modulus_coefficients"], model["field"]
    for coords in product(range(p), repeat=m):
        z = E(list(coords))
        assert module.character(model, z) == character(coords, p, modulus)
        trace = tuple(sum(v[i] for v in [power(coords, p ** j, p, modulus) for j in range(m)]) % p for i in range(m))
        assert trace == (int(z.trace()),) + (0,)*(m - 1)
    for i in range(m):
        unit = [int(i == j) for j in range(m)]
        dual = dual_frequency(model, unit)
        assert [int((dual*b).trace()) for b in model["basis"]] == unit


@pytest.mark.parametrize("include_zero", [True, False])
@pytest.mark.parametrize("sign", [-1, 1])
def test_full_coordinate_DFT_with_a_nonscalar_linear_map_and_actual_trace_dual_basis(include_zero, sign):
    p, m = 3, 3
    model = extension_model(p, m)
    modulus, E = model["record"]["modulus_coefficients"], model["field"]
    shift = (1, 2, 1)
    rho = (p ** m + (1 if include_zero else -1))/(2*p ** m)
    for xi in product(range(p), repeat=m):
        total = 0j
        for x in product(range(p), repeat=m):
            # A=[[1,1,0],[0,1,1],[0,0,1]], NOT field multiplication.
            z = ((x[0] + x[1] - shift[0]) % p,
                 (x[1] + x[2] - shift[1]) % p, (x[2] - shift[2]) % p)
            accepted = character(z, p, modulus) == sign or (include_zero and not any(z))
            g = (int(accepted) - rho)/math.sqrt(rho*(1 - rho))
            total += g*cmath.exp(-2j*math.pi*sum(a*b for a, b in zip(xi, x))/p)/(p ** m)
        eta = (xi[0], (xi[1] - xi[0]) % p, (xi[2] - xi[1] + xi[0]) % p)
        predicted = local_fourier(model, E(list(shift)), sign, eta, include_zero=include_zero)
        assert abs(total - predicted) < 2e-14
        if any(xi):
            assert abs(abs(predicted) ** 2 - 1/(p ** m - 1)) < 1e-14


def test_extension_gauss_sign_and_nonflat_even_degree_countercontrol():
    odd, even = extension_model(3, 3), extension_model(3, 2)
    assert odd["gauss_unit_i_power"] == 3  # -i, NOT the prime-field +i.
    assert even["gauss_unit_i_power"] == 0
    E = even["field"]
    masses = [abs(local_fourier(even, E.zero(), 1, v)) ** 2
              for v in product(range(3), repeat=2) if any(v)]
    assert max(masses) - min(masses) > .1
    with pytest.raises(ValueError, match="odd extension"):
        score_certificate(3, 2, 2, 3, 1)


def test_whole_ball_scalar_rank_bound_is_exact_in_a_non_extension_linear_calibration():
    p, n, m, K = 5, 2, 2, 3
    points = [1, 2, 3, 4]
    buckets, errors = {}, []
    for block in range(n):
        for value in product(range(p), repeat=m):
            if not any(value):
                continue
            e = [0]*(n*m)
            e[block*m:(block + 1)*m] = value
            syndrome = tuple(sum(pow(x, j, p)*a for x, a in zip(points, e)) % p for j in range(K))
            buckets.setdefault(syndrome, []).append(len(errors))
            errors.append((block, e))
    bad = [0]*n
    for indices in buckets.values():
        if len(indices) > 1:
            for i in indices:
                bad[errors[i][0]] += 1
    assert bad == [4, 4]
    bound = block_ambiguity(p, n, m, K, 1)
    assert fraction(bound["sphere_bad_mass_upper_exact"][1]) == Fraction(4, 24) == Fraction(1, 6)
    assert not bound["extension_linear_code_assumed"]
    # Rounding scalar rank3 UP to two F_25 symbols would wrongly certify0.
    assert m*math.ceil(K/m) == 4 > K


def test_capacity_extra_radius_and_pruning_failure_are_not_silently_ignored():
    unknown = score_certificate(7, 2, 3, 4, 1)
    assert not unknown["finite_mean_certified"]
    assert unknown["status"] == "UNKNOWN_OBSERVABLE_RADIUS_REACHES_SCALAR_CAPACITY"
    with pytest.raises(ValueError, match="source radius"):
        block_ambiguity(7, 2, 3, 4, 2)
    thin = score_certificate((1 << 61) - 1, 25, 31, 310, 6, pruning_trials=1)
    paid = score_certificate((1 << 61) - 1, 25, 31, 310, 6, pruning_trials=4096)
    assert thin["finite_mean_certified"] and paid["finite_mean_certified"]
    assert fraction(thin["bounded_decoder_loss"]["per_attempt_expected_normalized_score_lower_exact"]) == 0
    assert fraction(paid["bounded_decoder_loss"]["per_attempt_expected_normalized_score_lower_exact"]) > Fraction(84, 100)
    b = paid["bounded_decoder_loss"]
    gap, rounds, rank = fraction(b["pruning_agreement_gap_exact"]), b["independent_pruning_trials_charged"], b["affine_dimension_upper"]
    assert (1 - gap ** rank) ** rounds <= fraction(b["per_unique_error_miss_upper_128bit_dyadic"])
    assert all(fraction(t["bounded_pruning_one_attempt_lower_exact"]) <= fraction(t["exact_unique_decoder_one_attempt_lower_exact"]) for t in paid["tails"])


def test_large_exact_certificates_do_not_disable_global_integer_string_limits():
    before = sys.get_int_max_str_digits()
    text = "1/" + "9"*9000
    q = fraction(text)
    assert q > 0 and q.denominator.bit_length() > 25000
    assert sys.get_int_max_str_digits() == before
    model = extension_model((1 << 61) - 1, 31)
    assert not model["record"]["field_table_enumerated"]
    assert model["record"]["canonical_Gauss_unit_i_power"] == 3
    with pytest.raises(ValueError, match="bounded"):
        local_fourier(model, model["field"].zero(), 1, [1] + [0]*30)


def test_full_physical_coalescence_unique_erasure_and_native_filter_replay():
    report = json.loads(REPORT.read_text())
    for row in report["physical_controls"]:
        assert row == physical_control(row["include_zero"])
        assert row["source_errors_enumerated_charged"] == 685
        assert row["native_messages_enumerated_charged"] == 2401
        assert abs(row["source_norm"] - 1) < 1e-12
        epsilon = fraction(row["ambiguity_bound"]["sphere_bad_mass_upper_exact"][1])
        assert abs(row["source_ambiguous_mass"] - float(epsilon)/2) < 1e-12
        assert abs(row["unique_herald_probability"] + row["source_ambiguous_mass"] - 1) < 1e-12
        assert row["native_filter_vs_full_FFT_max_error"] < 1e-12
        assert row["wrong_prime_field_Gauss_sign_changes_native_output_TV"] > .7
        assert row["finite_mean_status"] == "UNKNOWN_OBSERVABLE_RADIUS_REACHES_SCALAR_CAPACITY"
        phase = row["quarter_turn_phase_approximation"]
        expected_overlap = (1 + math.sqrt(343/344))/2
        assert abs(phase["source_overlap_real"] - expected_overlap) < 1e-12
        assert abs(phase["source_overlap_imaginary"]) < 1e-12
        assert phase["full_success_failure_flagged_trace"] ** 2 <= phase["source_trace_squared"] + 1e-12


@pytest.mark.parametrize("include_zero", [True, False])
def test_quarter_turn_source_trace_bound_for_complex_radial_weights_and_all_error_labels(include_zero):
    p, m, n = 3, 3, 2
    model = extension_model(p, m)
    E, modulus = model["field"], model["record"]["modulus_coefficients"]
    vectors = [v for v in product(range(p), repeat=m) if any(v)]
    local_exact, local_quarter = [], []
    gauss_unit = 1j ** model["gauss_unit_i_power"]
    for block, (shift, sign) in enumerate(((E([1, 2, 0]), 1), (E([2, 1, 1]), -1))):
        exact, quarter = [], []
        for v in vectors:
            lam = dual_frequency(model, v)
            phase = cmath.exp(-2j*math.pi*int((lam*shift).trace())/p)
            chi = character(tuple(map(int, (-lam).to_list())), p, modulus)
            exact.append(local_fourier(model, shift, sign, v, include_zero=include_zero))
            quarter.append(phase*sign*chi*gauss_unit/math.sqrt(model["Q"] - 1))
        local_exact.append(exact)
        local_quarter.append(quarter)
        inner = sum(a.conjugate()*b for a, b in zip(quarter, exact))
        assert abs(inner - math.sqrt(27/28)) < 1e-12
    # Enumerate the whole two-block source, not just a product-state proxy.
    # Relative phases differ across its weight sectors and must survive.
    weights, exact, quarter, missing_gauss = (1, 1j, -2), [], [], []
    for j in range(n + 1):
        for support in combinations(range(n), j):
            for labels in product(range(len(vectors)), repeat=j):
                scale = weights[j]/math.sqrt(6*math.comb(n, j))
                a = b = scale
                for block, label in zip(support, labels):
                    a *= local_exact[block][label]
                    b *= local_quarter[block][label]
                exact.append(a)
                quarter.append(b)
                missing_gauss.append(b/gauss_unit ** j)
    assert abs(sum(abs(a) ** 2 for a in exact) - 1) < 1e-12
    overlap = sum(a.conjugate()*b for a, b in zip(quarter, exact))
    r = math.sqrt(27/28)
    assert abs(overlap - (1 + r + 4*r*r)/6) < 1e-12
    tv_squared = 1 - abs(overlap) ** 2
    bound = quarter_turn_source_bound(p, m, 2)
    assert 0 < tv_squared <= float(fraction(bound["full_source_pure_trace_distance_squared_upper_exact"]))
    bad_overlap = sum(a.conjugate()*b for a, b in zip(missing_gauss, exact))
    assert 1 - abs(bad_overlap) ** 2 > .5
    assert bound["conditional_postselected_output_has_no_such_unpaid_guarantee"]


def test_phase_truncation_bound_handles_zero_radius_and_refuses_nonflat_families():
    assert quarter_turn_source_bound(7, 3, 0)["full_source_pure_trace_distance_squared_upper_exact"] == "0"
    assert quarter_turn_source_bound(7, 3, 1000)["full_source_pure_trace_distance_squared_upper_exact"] == "1"
    for p, m, ell in ((5, 3, 1), (7, 2, 1), (7, 3, -1), (7, 3, True)):
        with pytest.raises(ValueError):
            quarter_turn_source_bound(p, m, ell)


def test_compact_block_ball_envelope_dominates_detailed_scalar_rank_certificate():
    for p, n, m, K, radius in ((1019, 6, 31, 80, 2), (127, 8, 3, 10, 3)):
        detailed = block_ambiguity(p, n, m, K, radius)
        compact = block_ball_envelope(p, n, m, K, radius)
        epsilon = fraction(detailed["any_radial_weight_bad_mass_upper_exact"])
        M = int(detailed["max_fiber_size_support_bound_decimal"])
        gap = compact["scalar_capacity_gap"]
        assert epsilon <= Fraction(2 ** (n + 1), p ** gap)
        assert M*epsilon <= Fraction(2 ** (2*n + 1), p ** gap)
        exponent = compact["radial_Gram_error_power_two_upper_exponent"]
        assert M*epsilon <= Fraction(2) ** exponent
        assert not compact["extension_linear_code_assumed"]
        assert not compact["actual_generator_or_matrix_verified_here"]
    with pytest.raises(ValueError, match="geometry"):
        block_ball_envelope(7, 4, 3, 10, 1)


def test_uniform_family_matches_actual_decoder_geometry_and_exact_window_Rayleigh():
    p, n = (1 << 61) - 1, 3200
    certificate = uniform_family_certificate(p, n)
    native = certificate["native_decoder"]
    points, D = decoder_parameters(p, n, 31, 31*n - certificate["scalar_rank_K"], 3, n//4, 4)
    assert len(set(points)) == 31*n
    assert D == native["interpolation_D"] == 6016
    assert native["strict_root_margin"] == 1665
    assert fraction(native["pruning_gap_exact"]) == Fraction(481, 3200)
    assert Fraction(7973, 8000) ** 8192 < Fraction(1, 10 ** 12)
    window = certificate["source_window"]
    weights = [0]*window["first_weight"] + [1]*32
    assert len(weights) == n//4 + 1
    for eta in (-1, 1):
        rho = Fraction(p ** 31 + eta, 2*p ** 31)
        reference = rayleigh_interval(n, rho, weights)
        assert fraction(certificate["ambient_window_Rayleigh_lower_exact"]) <= fraction(reference["ambient_Rayleigh_lower_exact"])
    mean = fraction(certificate["per_attempt_mean_lower_exact"])
    assert mean == Fraction(36384099, 40000000) > Fraction(909, 1000)
    tail = fraction(certificate["integer_support_tail_lower_exact"])
    assert tail == (mean - Fraction(9*n//10 - 1, n))/(1 - Fraction(9*n//10 - 1, n)) >= Fraction(9, 100)
    assert not certificate["binomial_or_IID_shift_assumption"]
    assert not certificate["actual_public_input_or_synthesis_error_verified_here"]
    assert not certificate["classical_hardness_runtime_advantage_novelty_or_candidate_admission"]


def test_uniform_family_certificate_is_compact_beyond_any_enumeration_or_4096_block_cap():
    p, n = (1 << 127) - 1, 10 ** 12
    certificate = uniform_family_certificate(p, n)
    assert certificate["extra_radius_envelope"]["radial_Gram_error_power_two_upper_exponent"] == 32 - 53*n//20
    assert len(certificate["source_window"]["nonzero_unnormalized_weights"]) == 32
    assert len(json.dumps(certificate)) < 16000
    assert certificate["target_accepted_count"] == 9*n//10
    assert certificate["native_decoder"]["strict_root_margin"] == 13*n//25 + 1
    assert not certificate["large_quantum_circuit_compiled_or_executed"]
    assert certificate["arithmetic_only_no_field_table_support_enumeration_or_eigenproblem"]


def test_uniform_family_refuses_out_of_theorem_parameters_or_unpaid_precision():
    p = (1 << 61) - 1
    for n in (3100, 3201, 3200.0, True):
        with pytest.raises(ValueError, match="multiple"):
            uniform_family_certificate(p, n)
    with pytest.raises(ValueError, match="p3mod4"):
        uniform_family_certificate((1 << 31) - 1, 3200)
    for budget in (Fraction(-1, 1000), Fraction(2, 1000), .001, True):
        with pytest.raises(ValueError, match="trace budget"):
            uniform_family_certificate(p, 3200, synthesis_trace_budget=budget)
    ideal = uniform_family_certificate(p, 3200, synthesis_trace_budget=0)
    assert ideal["zero_synthesis_budget_is_an_ideal_limit_not_a_finite_gate_claim"]
    assert fraction(ideal["per_attempt_mean_lower_exact"]) > Fraction(91, 100)


def test_live_report_matches_source_and_all_direct_dependencies():
    report = json.loads(REPORT.read_text())
    assert report == run_controls()
    assert report["source_sha256"] == hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((module.ROOT / "theorems" / name).read_bytes()).hexdigest()
    assert not report["quantum_speedup_or_classical_hardness_claimed"]
