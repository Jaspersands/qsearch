from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from math import prod

import pytest

from theorems.inverse_trace_gibbs_target import (
    REPORT, ROOT, _ceil_log2, _ceiling, _floor, _pair_bounds,
    finite_fiber_audit, finite_pair_spectrum, gibbs_success_bound,
    heatbath_escape_bound, heatbath_mixing_certificate,
    mds_character_bound, native_certificate, reciprocal_bound, reference_heatbath,
    report,
)


@pytest.mark.parametrize("bits,length,checks", [(2, 4, 1), (3, 5, 2), (4, 4, 3)])
def test_mds_expression_equals_direct_nonzero_codeword_weight_enumerator(bits, length, checks):
    from theorems.explicit_quadratic_opi import element, field

    weights = []
    for coefficients in product(range(1 << bits), repeat=checks):
        if not any(coefficients):
            continue
        values = [sum((element(bits, c)*element(bits, a)**j
                       for j, c in enumerate(coefficients)), field(bits).zero())
                  for a in range(length)]
        weights.append(sum(v != 0 for v in values))
    for beta in (Q(0), Q(1, 7), Q(1, 2), Q(1)):
        exact = sum((beta**w for w in weights), Q(0))
        assert mds_character_bound(bits, length, checks, beta, exact=True) == exact
        assert mds_character_bound(bits, length, checks, beta) >= exact


def test_structured_bound_is_informative_when_minimum_distance_union_is_not():
    n, length, checks = 31, 961, 384
    beta, eta = reciprocal_bound(n, length, checks)
    coarse = ((1 << n)**checks-1)*beta**(length-checks+1)
    assert coarse > 1
    assert eta < Q(1, 4)


@pytest.mark.parametrize("params", [(2, 3, 1), (3, 4, 2), (4, 4, 1)])
def test_every_target_and_syndrome_obeys_count_bound(params):
    row = finite_fiber_audit(*params)
    bits, length, checks = params
    assert sum(map(sum, row["all_fiber_counts"])) == (1 << bits)**length
    assert all(sum(counts) == (1 << bits)**(length-checks) for counts in row["all_fiber_counts"])
    assert Q(*row["maximum_relative_deviation"]) <= Q(*row["exact_mds_envelope"])
    if params == (4, 4, 1):
        assert Q(*row["exact_mds_envelope"]) < 1
        assert row["minimum_fiber_count"] > 0
    assert not row["reference_is_polynomial_in_field_bits"]


def test_native_success_bound_agrees_with_all_exact_finite_partition_functions():
    row = finite_fiber_audit(4, 4, 1)
    eta = Q(*row["exact_mds_envelope"])
    bound = gibbs_success_bound(4, eta)
    base = bound["M"]
    for counts in row["all_fiber_counts"]:
        for b, witnesses in enumerate(counts):
            partition = sum(Q(count, base**((b ^ output).bit_count()))
                            for output, count in enumerate(counts))
            assert Q(witnesses)/partition >= bound["ideal_native_success_lower"]


@pytest.mark.parametrize("n", [17, 31, 61])
def test_native_mathematical_certificate_is_uniform_and_does_not_claim_sampling(n):
    row = native_certificate(n)
    assert row["length"] == n*n and row["checks"] == n*n//8
    assert row["fiber_relative_error_power2_upper"] <= -2
    assert Q(*row["ideal_native_success_lower"]) > Q(1, 5)
    assert Q(*row["conditional_native_success_lower"]) > Q(1, 10)
    assert row["uniform_all_targets_and_syndromes"]
    assert not row["polynomial_mixing_proved"]
    assert not row["native_large_chain_executed"]


def test_vacuous_count_bound_and_tv_error_do_not_become_success():
    assert gibbs_success_bound(11, Q(1))["ideal_native_success_lower"] == 0
    assert gibbs_success_bound(11, Q(4))["conditional_native_success_lower"] == 0
    row = gibbs_success_bound(11, Q(1, 4), sampler_tv=Q(1))
    assert row["conditional_native_success_lower"] == 0
    row = gibbs_success_bound(11, Q(1, 4), sampler_tv=Q(1, 10))
    assert row["conditional_native_success_lower"] == row["ideal_native_success_lower"]-Q(1, 10)
    assert row["conditional_native_success_lower"] > Q(1, 10)


@pytest.mark.parametrize("block", [1, 2, 3])
def test_native_binary_block_kernel_is_exact_and_does_not_hide_field_enumeration(block):
    row = reference_heatbath(3, 3, 1, (1, 0, 1), block_bits=block)
    assert row["detailed_balance_exact"] and row["irreducible_and_aperiodic"]
    assert row["states_enumerated"] == 64
    assert row["candidates_per_update"] == 2**block
    assert row["full_field_block_would_cost"] == 8**block
    fibers = finite_fiber_audit(3, 3, 1)["all_fiber_counts"][0]
    expected = Q(fibers[5])/sum(Q(count, 4**((5 ^ output).bit_count()))
                               for output, count in enumerate(fibers))
    assert Q(*row["stationary_native_success"]) == expected
    assert row["native_witnesses_enumerated"] == fibers[5]
    assert 0 < Q(*row["mean_solution_escape"]) <= 1
    assert not row["polynomial_mixing_proved"]
    assert not row["reference_is_scalable_sampler"]


@pytest.mark.parametrize("bits", [2, 3, 4, 5, 6])
def test_every_scalar_displacement_frequency_and_weighted_target_obeys_pair_bound(bits):
    row = finite_pair_spectrum(bits)
    assert row["displacement_frequency_pairs"] == (1 << bits)*((1 << bits)-1)
    assert row["weighted_displacement_target_controls"] == 6*((1 << bits)-1)
    assert row["zero_extensions_and_infinity_terms_checked"]
    assert not row["reference_is_polynomial_in_field_bits"]


def test_weighted_native_sum_equals_dual_expansion_for_every_displacement_and_target():
    from flint import fq_default_ctx

    bits, q, length, checks, r = 2, 4, 3, 1, Q(1, 4)
    context = fq_default_ctx(2, bits, "z")
    values = [context.zero(), context.one(), context.gen(), context.gen()+1]
    predicate = [0 if x == 0 else int((x**-1).trace()) for x in values]
    words = [(x, y, x ^ y) for x in range(q) for y in range(q)]
    chars = [[1-2*int((u*x).trace()) for x in values] for u in values]
    for v in words:
        assert not any(v) or sum(x != 0 for x in v) >= checks+1
        for b in product((0, 1), repeat=length):
            h = [[int(predicate[x] == bi)
                  *(r+(1-r)*int(predicate[x ^ vi] == bi))
                  for x in range(q)] for vi, bi in zip(v, b)]
            direct = sum(prod(h[i][x] for i, x in enumerate(word)) for word in words)
            fourier = [[sum(a*c for a, c in zip(hi, char)) for char in chars] for hi in h]
            dual = sum(prod(fi[u] for fi in fourier) for u in range(q))/q
            assert direct == dual
            mean_product = Q(q**(length-checks))*prod(fi[0]/q for fi in fourier)
            beta = max(abs(fi[u])/fi[0] for fi in fourier for u in range(1, q))
            assert abs(direct/mean_product-1) <= mds_character_bound(
                bits, length, checks, beta, exact=True)


@pytest.mark.parametrize("bits", [17, 31, 61])
def test_native_small_block_mixing_bound_has_correct_distances_rounding_and_scope(bits):
    length, checks = bits*bits, bits*bits//8
    raw = heatbath_escape_bound(bits, length, checks)
    row = heatbath_mixing_certificate(bits, length, checks)
    assert row["native_displacement_distance"] == checks+1
    assert raw["fiber_eta"] < Q(1, 4) and raw["pair_eta"] < Q(1, 4)
    assert raw["escape_upper"] < Q(1, 1 << (checks-4))
    assert row["nontrivial_mixing_obstruction"]
    assert row["mixing_scope"] == "WORST_INITIAL_STATE_ONLY"
    assert row["uniform_all_targets_and_distinct_evaluation_points"]
    assert row["requires_state_independent_block_selection"]
    assert not row["uniform_initial_witness_hitting_lower_bound"]
    assert not row["all_classical_algorithms_excluded"]
    assert not row["native_large_chain_executed"]
    assert Q(*row["stationary_native_success_upper"]) >= raw["stationary_success_upper"]
    assert Q(*row["pair_beta_upper"]) >= raw["pair_beta"]
    steps = row["worst_start_tv_quarter_steps_lower"]
    assert 1-raw["stationary_success_upper"]-(steps-1)*raw["escape_upper"] > Q(1, 4)
    assert 1-raw["stationary_success_upper"]-steps*raw["escape_upper"] <= Q(1, 4)


def test_large_blocks_and_vacuous_fiber_bounds_are_not_promoted_to_obstructions():
    row = heatbath_escape_bound(3, 3, 1, block_bits=1)
    assert row["fiber_eta"] >= 1
    assert row["escape_upper"] == row["stationary_success_upper"] == 1
    assert row["worst_start_tv_quarter_steps_lower"] == 0
    small = heatbath_escape_bound(17, 289, 36, block_bits=1)
    larger = heatbath_escape_bound(17, 289, 36, block_bits=3)
    assert larger["escape_upper"] == 7*small["escape_upper"]
    all_bits = heatbath_escape_bound(17, 289, 36, block_bits=17*(289-36))
    assert all_bits["escape_upper"] == 1
    assert not all_bits["nontrivial_mixing_obstruction"]


def test_empty_finite_solution_set_has_no_escape_statistic():
    row = reference_heatbath(2, 3, 1, (1, 1, 1))
    assert row["native_witnesses_enumerated"] == 0
    assert row["mean_solution_escape"] is None


def test_uniform_mixing_obstruction_also_applies_to_trivial_zero_target():
    row = heatbath_mixing_certificate(17, 289, 36)
    assert row["uniform_all_targets_and_distinct_evaluation_points"]
    assert row["worst_start_tv_quarter_steps_lower"] > 10**9
    # b=0 has the immediate witness x=0 under every linear H, despite this bound.
    native_zero_word = (0,)*row["length"]
    assert not any(native_zero_word)
    assert not row["all_classical_algorithms_excluded"]
    assert not row["uniform_initial_witness_hitting_lower_bound"]


def test_worst_start_obstruction_does_not_imply_uniform_start_first_hit_obstruction():
    # A proof-logic countercontrol, not a candidate algorithm or native model.
    eps = Q(1, 1024)
    kernel = ((1-eps, eps, 0), (Q(1, 2), 0, Q(1, 2)), (0, eps, 1-eps))
    pi = (1/(2+2*eps), eps/(1+eps), 1/(2+2*eps))
    assert all(pi[i]*kernel[i][j] == pi[j]*kernel[j][i]
               for i in range(3) for j in range(3))
    assert 1-pi[0]-100*eps > Q(1, 4)
    uniform_hit_by_one = Q(1, 3)+Q(1, 3)*kernel[1][0]
    assert uniform_hit_by_one == Q(1, 2)


@pytest.mark.parametrize("callback", [
    lambda: finite_pair_spectrum(7),
    lambda: _pair_bounds(3, Q(0)),
    lambda: _pair_bounds(3, 0.25),
    lambda: heatbath_escape_bound(3, 3, 1, block_bits=0),
    lambda: heatbath_escape_bound(3, 3, 1, block_bits=7),
    lambda: finite_fiber_audit(17, 289, 36),
    lambda: reference_heatbath(17, 289, 36, (0,)*289),
    lambda: reference_heatbath(3, 3, 1, (0, 1)),
    lambda: reference_heatbath(3, 3, 1, (True, 0, 1)),
    lambda: reference_heatbath(3, 3, 1, (0, 0, 1), block_bits=4),
    lambda: mds_character_bound(3, 4, 1, 0.5),
    lambda: mds_character_bound(3, 4, 1, Q(-1)),
    lambda: mds_character_bound(3, 9, 1, Q(1, 2)),
    lambda: gibbs_success_bound(7, Q(1, 4), inverse_temperature_base=6),
    lambda: gibbs_success_bound(7, Q(1, 4), sampler_tv=-0.1),
])
def test_caps_and_input_contracts(callback):
    with pytest.raises(ValueError):
        callback()


def test_report_rounding_is_outward_even_for_tiny_rational_bounds():
    for value in (Q(0), Q(1), Q(3), Q(3, 8), Q(1, 1 << 300), Q(7, 1 << 301)):
        lower = Q(*_floor(value))
        assert lower <= value < lower+Q(1, 1 << 128)
        upper_rounded = Q(*_ceiling(value))
        assert upper_rounded-Q(1, 1 << 128) < value <= upper_rounded
        power = _ceil_log2(value)
        if value == 0:
            assert power is None
        else:
            upper = Q(1 << power) if power >= 0 else Q(1, 1 << -power)
            assert upper/2 < value <= upper


def test_live_artifact_replays_with_source_proof_hashes_and_open_sampling_premise():
    data = json.loads(REPORT.read_text())
    assert data == report(include_finite=data["native_finite_controls_executed"],
                          include_pair=data["independent_pair_controls_executed"])
    assert data["source_sha256"] == hashlib.sha256(
        (ROOT / "theorems/inverse_trace_gibbs_target.py").read_bytes()).hexdigest()
    assert data["proof_sha256"] == hashlib.sha256(
        (ROOT / "research/INVERSE_TRACE_GIBBS_TARGET.md").read_bytes()).hexdigest()
    assert not data["sampler_total_variation_bound_proved"]
    assert not data["full_native_classical_solver_established"]
    assert not data["quantum_speedup_established"]
    assert data["local_mixing_derivation_external_review_pending"]
    assert all(row["nontrivial_mixing_obstruction"] for row in data["small_block_mixing_certificates"])


def test_bounds_only_report_cannot_claim_unexecuted_finite_controls():
    data = report(include_finite=False, include_pair=False)
    assert not data["native_finite_controls_executed"]
    assert not data["independent_pair_controls_executed"]
    assert data["pair_spectrum_controls"] == data["all_fiber_controls"] == data["kernel_controls"] == []
    assert len(data["small_block_mixing_certificates"]) == 3
