"""Independent exact cap checks, not a proof or hidden-oracle benchmark."""
from fractions import Fraction
from hashlib import sha256
from math import gcd, isqrt, prod
from pathlib import Path
import json

import pytest

from theorems import codimension_hybrid_budget as hybrid


def ceil_log2(value):
    power, exponent = 1, 0
    while power < value:
        power *= 2
        exponent += 1
    return exponent


@pytest.mark.parametrize("n,k,p,error", [
    (3, 3, 7, Fraction(1, 3)), (10, 3, 7, Fraction(1, 101)),
    (1, 1, 3, Fraction(7, 8)), (32, 12, 7, Fraction(1, 3)),
    (16, 8, 101, Fraction(1, 3)),
    (100, 2, 9, Fraction(1, 2**200)),
])
def test_classical_caps_and_each_error_share(n, k, p, error):
    result = hybrid.hybrid_codimension_budget(n, k, p, error)
    assert result["branch"] == "classical_collisions"
    budget = result["classical"]
    threshold = 16*(2*k)**(4*k+2)
    assert result["field_threshold"] == threshold > p
    I = p**k
    B = isqrt(2*I)+2
    t = n+ceil_log2(3/error)
    a = ceil_log2(3*t/error)
    Q = t*a*B
    L = ceil_log2(3*n*Q/error)
    assert budget["index_cap"] == I < budget["index_parameter_envelope"] == threshold**k
    assert budget["batch_size"] == B
    assert (B-2)**2 <= 2*I < (B-1)**2
    assert budget["birthday_exponent_lower_bound"] == Fraction(B*(B-1), 2*I) > 1
    assert budget["no_collision_probability_upper_bound"] == Fraction(1, 2)
    assert budget["no_collision_bound_is_strict"]
    assert budget["accepted_hidden_elements"] == t
    assert budget["rank_slack"] == t-n
    assert budget["batches_per_hidden_element"] == a
    assert budget["fresh_batch_cap"] == t*a
    assert budget["group_draw_cap"] == budget["original_query_cap"] == Q
    assert budget["scalar_coordinates_per_group_draw"] == n
    assert budget["scalar_uniform_draw_cap"] == result["classical_uniform_draw_cap"] == n*Q
    assert budget["integer_rejection_cap"] == L
    assert budget["bits_per_rejection_attempt"] == (p-1).bit_length()
    assert budget["fair_bit_cap"] == result["classical_fair_bit_cap"] == n*Q*L*(p-1).bit_length()
    assert budget["group_inverse_cap"] == budget["group_product_cap"] == t
    assert budget["label_order_comparison_cap"] == t*a*B*ceil_log2(Fraction(B))
    assert budget["label_equality_comparison_cap"] == t*a*(B-1)
    assert result["branch_requires_rees"] is False
    assert budget["batch_coordinate_storage_cap"] == n*B
    assert budget["accepted_coordinate_storage_cap"] == n*t
    failures = (Fraction(t, 2**a), Fraction(1, 2**(t-n)), Fraction(n*Q, 2**L))
    for name, bound in zip(("collision", "rank", "field_draw"), failures):
        assert budget[name+"_failure_bound"] == bound <= error/3
        assert budget[name+"_error_share"] == error/3
    assert sum(failures) == result["total_error_bound"] <= error
    assert result["original_queries"] == result["original_inputs"] == Q
    assert result["terminal_rees"] is result["abelian_intersections"] is None
    assert budget["collision_selection_uses_only_labels"]
    assert budget["identity_elements_retained"]
    assert budget["accepted_elements_are_independent_under_source_promise"]


@pytest.mark.parametrize("n,k,p,error", [
    (10, 3, 2**127-1, Fraction(1, 3)),
    (1, 1, 1031, Fraction(1, 11)),
    (7, 2, 2**61-1, Fraction(1, 2**30)),
    (12, 5, 2**127-1, Fraction(7, 8)),
])
def test_large_field_envelope_forest_and_original_query_transport(n, k, p, error):
    result = hybrid.hybrid_codimension_budget(n, k, p, error)
    assert result["branch"] == "large_field_rees"
    assert result["branch_requires_rees"] is True
    m = k*(k+1)//2
    c = 1 if m == 1 else min(2*k-1, m-1)
    profile = (m,)+tuple(m-d for d in range(2, c+1))
    assert result["field_threshold"] == 16*(2*k)**(4*k+2) <= p
    assert result["terminal_dimension_bound"] == m
    assert result["terminal_class_bound"] == c < p
    assert result["terminal_envelope_profile"] == profile
    assert result["terminal_profile_is_envelope"]
    terminal = result["terminal_rees"]
    assert terminal["lower_central_dimensions"] == profile
    assert terminal["error_target"] == result["terminal_error_share"] == error/2
    assert terminal["profile_role"] == "UNREALIZED_UPPER_ENVELOPE_NOT_ACTUAL_INPUT_PROFILE"
    assert terminal["actual_class_field_is_envelope_length_not_certification"]
    primitive = result["terminal_uniform_instrument"]
    assert primitive["recovery_budget"] == terminal
    assert primitive["profile_role"] == terminal["profile_role"]
    assert primitive["ordinary_oracle_queries"] == terminal["original_inputs"]
    assert primitive["per_instrument_qft_error_bound"] == terminal["instrument_error_per_call"]
    assert primitive["circuit_generator_implemented"] is False
    samples = m+ceil_log2(6/error)
    arities = []
    conversions = samples
    merges = measurements = nonlinear = 0
    for stage in reversed(terminal["stages_top_down"]):
        d, rank = stage["grade"], stage["rank"]
        reduced = gcd(d, p-1)
        assert rank == profile[d-1]
        assert reduced == stage["reduced_degree"] <= d <= c
        if reduced > 1:
            assert p >= 16*reduced**(2*reduced+2)
        arity = rank+1 if reduced == 1 else (rank+1)*((reduced-1)*rank+1)
        assert stage["arity"] == arity
        assert stage["conversions"] == conversions
        assert stage["consumed_targets"] == arity*conversions
        merges += conversions
        measurements += arity*conversions
        if reduced > 1:
            nonlinear += conversions
        conversions *= arity
        arities.append(arity)
    leaves = samples*prod(arities)
    assert terminal["final_fourier_samples"] == samples
    assert terminal["source_preparations"] == leaves
    assert terminal["original_inputs"] == c*leaves
    assert terminal["sde_calls"] == merges
    assert terminal["central_character_measurements"] == measurements
    assert terminal["complete_instrument_calls"] == leaves+merges+samples
    assert terminal["nonlinear_sde_calls"] == nonlinear
    assert terminal["instrument_error_per_call"] == error/(6*(leaves+merges+samples))
    rank = Fraction(1, (p-1)*p**(samples-m))
    bits = ceil_log2(6*nonlinear/error) if nonlinear else None
    abort = Fraction(nonlinear, 2**bits) if nonlinear else Fraction(0)
    assert terminal["solver_failure_bits_per_call"] == bits
    assert terminal["solver_abort_bound"] == abort <= error/6
    assert terminal["rank_failure_bound"] == rank <= error/6
    assert terminal["total_error_bound"] == rank+abort+error/6 <= error/2
    uniform_calls = fair_bits = root_pairs = 0
    actual_abort = Fraction(0)
    for stage in terminal["stages_top_down"]:
        degree, rank = stage["reduced_degree"], stage["rank"]
        caps = stage["randomness"]
        if degree == 1:
            assert caps is None
            continue
        roots = ((degree-1)*rank+1)*(rank+3)+degree*(degree+1)//2
        union = degree+roots*(degree-1)
        internal_bits = bits+1+ceil_log2(Fraction(union))
        calls = degree*internal_bits+sum(2*degree**j*internal_bits for j in range(2, degree+1))
        calls += roots*degree*(degree-1)*3*internal_bits
        rejection = bits+1+ceil_log2(Fraction(calls))
        pairs = roots*(degree-1)*3*internal_bits
        bit_cap = calls*rejection*(p-1).bit_length()
        failure = Fraction(union, 2**internal_bits)+Fraction(calls, 2**rejection)
        assert caps == dict(failure_bits=bits, root_calls=roots,
                            polynomial_pow_gcd_pairs=pairs, uniform_calls=calls,
                            bit_rejection_attempts=rejection, fair_bits=bit_cap,
                            abort_bound=failure)
        count = stage["conversions"]
        uniform_calls += count*calls
        fair_bits += count*bit_cap
        root_pairs += count*pairs
        actual_abort += count*failure
    assert actual_abort <= abort
    assert terminal["classical_uniform_draw_cap"] == uniform_calls
    assert terminal["classical_fair_bit_cap"] == fair_bits
    assert terminal["classical_root_pow_gcd_pair_cap"] == root_pairs
    assert prod(arities) <= result["terminal_leaf_parameter_bound"]
    bound = (m+1)*((2*k-1)*m+1)
    assert result["terminal_stage_arity_parameter_bound"] == bound
    assert result["terminal_leaf_parameter_bound"] == bound**(c-1)
    abelian = result["abelian_intersections"]
    extra = ceil_log2(4*n/error)
    assert abelian["call_cap"] == n
    assert abelian["early_abelian_terminal_solves_included"] is True
    assert abelian["early_abelian_dimension_bound"] == n
    assert abelian["rank_slack"] == extra
    assert abelian["samples_per_call"] == n+extra
    assert abelian["complete_sampler_call_cap"] == n*(n+extra)
    assert abelian["original_query_cap"] == n*(n+extra)
    assert abelian["rank_failure_bound"] == Fraction(n, 2**extra) <= error/4
    assert abelian["rank_error_share"] == error/4
    assert abelian["complete_sampler_approximation_share"] == error/4
    assert abelian["complete_sampler_error_per_call"]*n*(n+extra) == error/4
    assert abelian["exact_intersection_required"]
    assert result["abelian_original_queries"] == n*(n+extra)
    assert result["terminal_original_queries"] == c*leaves
    assert result["original_queries"] == result["original_inputs"] == n*(n+extra)+c*leaves
    assert result["query_transport_original_queries_per_call"] == 1
    assert result["total_error_bound"] == Fraction(n, 2**extra)+error/4+terminal["total_error_bound"] <= error
    for name in ("classical_uniform_draw_cap", "classical_fair_bit_cap", "classical_root_pow_gcd_pair_cap"):
        assert result[name] == terminal[name]


@pytest.mark.parametrize("k", [1, 2, 3, 8])
def test_threshold_neighbors_and_composite_prime_promise(k):
    threshold = 16*(2*k)**(4*k+2)
    # The exact threshold is even and therefore inadmissible. Its odd
    # neighbors exercise both sides without claiming either is prime.
    with pytest.raises(ValueError, match="odd prime"):
        hybrid.hybrid_codimension_budget(k, k, threshold)
    assert hybrid.hybrid_codimension_budget(k, k, threshold-1)["branch"] == "classical_collisions"
    above = hybrid.hybrid_codimension_budget(k, k, threshold+1)
    assert above["branch"] == "large_field_rees"
    assert above["prime_certified"] is False
    assert above["prime_validation_included"] is False
    assert above["prime_contract"] == "SUPPLIED_PROMISE_NOT_VERIFIED"
    # 1025=5*205 is deliberately accepted as an UNVERIFIED promise.
    composite = hybrid.hybrid_codimension_budget(1, 1, 1025)
    assert composite["branch"] == "large_field_rees"
    assert composite["prime_certified"] is False


@pytest.mark.parametrize("n,p", [(0, 3), (0, 2**127-1), (100, 7)])
def test_zero_query_case_never_invokes_terminal(n, p, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("zero-query case invoked the terminal")
    monkeypatch.setattr(hybrid, "prime_field_instrument_budget", forbidden)
    result = hybrid.hybrid_codimension_budget(n, 0, p)
    assert result["branch"] == "zero_query"
    assert result["original_queries"] == result["original_inputs"] == 0
    assert result["classical_uniform_draw_cap"] == result["classical_fair_bit_cap"] == 0
    assert result["total_error_bound"] == Fraction(0)
    assert result["terminal_rees"] is result["classical"] is result["abelian_intersections"] is None


@pytest.mark.parametrize("n,k,p,error", [
    (-1, 0, 3, Fraction(1, 3)), (3, -1, 3, Fraction(1, 3)),
    (3, 4, 3, Fraction(1, 3)), (0, 1, 3, Fraction(1, 3)),
    *[(n, k, p, Fraction(1, 3)) for n, k, p in
      ((True, 0, 3), (3.0, 1, 3), (3, True, 3), (3, 1.0, 3),
       (3, 1, True), (3, 1, 3.0), (3, 1, 1), (3, 1, 2), (3, 1, 4),
       (Fraction(3), 1, 3), (3, Fraction(1), 3), (3, 1, Fraction(3)))],
    *[(3, 1, 3, e) for e in (True, False, 0.1, 0, 1, "1/3", Fraction(0), Fraction(1), Fraction(-1))],
])
def test_strict_contracts(n, k, p, error):
    with pytest.raises(ValueError):
        hybrid.hybrid_codimension_budget(n, k, p, error)


@pytest.mark.parametrize("n,k,p", [(0, 0, 3), (10, 3, 7), (10, 3, 2**127-1)])
def test_flags_and_parameter_metadata(n, k, p):
    result = hybrid.hybrid_codimension_budget(n, k, p)
    assert result["status"] == "CONDITIONAL_ON_EXISTING_REES_WHOLE_PROOF_RESOURCE_CERTIFICATE"
    for flag in ("prime_certified", "prime_validation_included", "actual_class_certified",
                 "codimension_promise_certified", "profile_existence_certified",
                 "hidden_intersection_completeness_certified", "solver_implemented",
                 "quantum_receiver_implemented", "hidden_oracle_benchmark", "field_enumeration_used",
                 "native_application_established", "novelty_established", "speedup_claim_allowed",
                 "formal_total_policy_instantiated", "physical_gate_clock", "deterministic_arithmetic_step_counter"):
        assert result[flag] is False
    assert result["resource_certificate_only"] is True
    assert result["oracle_queries_executed"] == 0
    assert result["complexity"]["uses_generic_derived_rank_bound"] is False
    assert result["complexity"]["conditional_on_existing_rees_whole_proof"] is True
    assert "k^2 log(k+2)" in result["complexity"]["overall"]
    assert "k log(k+2)" in result["complexity"]["large_field"]
    assert result["growing_class_pointwise_correctness_supplied_promise"] is True
    assert result["growing_class_uniform_complete_instrument_efficiency_supplied_promise"] is False
    assert result["uniform_compilation_status"] == "DERIVED_IN_WRITTEN_ARGUMENT_NOT_MACHINE_CERTIFIED"
    assert result["growing_class_pointwise_correctness_certified"] is False
    assert result["growing_class_uniform_complete_instrument_efficiency_certified"] is False
    assert result["fixed_class_correctness_alone_suffices"] is False
    runtime = result["runtime_model"]
    assert runtime["total_time_bound"] == "T_nonoracle + Q*T_f"
    assert runtime["Q"] == "original_queries"
    assert runtime["oracle_evaluation_time_included_in_resource_caps"] is False
    assert runtime["oracle_evaluation_cost_certified"] is False
    assert runtime["label_width_is_oracle_evaluation_cost"] is False
    assert runtime["label_processing_cost_charged_to_nonoracle_time"] is True
    assert runtime["label_width_is_a_separate_bit_complexity_parameter"] is True
    assert "label_width" in result["complexity"]["overall"]


def test_report_is_exact_json_and_deterministic_without_execution():
    result = hybrid.report()
    assert result["total_time_bound"] == "T_nonoracle + Q*T_f"
    assert result["oracle_evaluation_cost_certified"] is False
    assert result["label_width_is_oracle_evaluation_cost"] is False
    assert result["growing_class_pointwise_correctness_supplied_promise"] is True
    assert result["growing_class_uniform_complete_instrument_efficiency_supplied_promise"] is False
    assert result["uniform_compilation_status"] == "DERIVED_IN_WRITTEN_ARGUMENT_NOT_MACHINE_CERTIFIED"
    assert result["fixed_class_correctness_alone_suffices"] is False
    assert result == hybrid.report() == json.loads(json.dumps(result))
    assert [case["branch"] for case in result["cases"]] == [
        "classical_collisions", "large_field_rees", "classical_collisions", "classical_collisions"]
    assert [(case["dimension"], case["codimension_bound"], case["supplied_prime"])
            for case in result["cases"]] == [(10, 3, 7), (10, 3, 2**127-1), (32, 12, 7), (16, 8, 101)]
    assert result["cases"][0]["error_target"] == {"numerator": 1, "denominator": 3}
    def no_float(value):
        assert not isinstance(value, (float, Fraction))
        if isinstance(value, dict):
            for item in value.values():
                no_float(item)
        elif isinstance(value, list):
            for item in value:
                no_float(item)
    no_float(result)


def test_report_binds_current_source_bytes_without_proof_promotion(monkeypatch):
    root = Path(hybrid.__file__).resolve().parents[1]
    paths = (
        "theorems/codimension_hybrid_budget.py", "theorems/uniform_bch_rees.py",
        "theorems/power_sde.py", "theorems/power_sde_budget.py",
        "theorems/bounded_codimension_reduction.py",
        "theorems/rees_uniform_instrument.py",
        "research/REES_UNIFORM_INSTRUMENT_COMPILATION.md",
        "research/BOUNDED_CODIMENSION_HYBRID_BOUND.md",
    )
    result = hybrid.report()
    assert result["proof_note"] == paths[-1]
    expected = {path: sha256((root/path).read_bytes()).hexdigest() for path in paths}
    assert result["source_sha256"] == expected
    for flag in ("source_hashes_certify_proof", "candidate_promotion", "proof_promotion"):
        assert result[flag] is False
    read_bytes = Path.read_bytes
    def edited_note(path):
        original = read_bytes(path)
        return original+b"\nChanged proof note\n" if path == root/paths[-1] else original
    monkeypatch.setattr(Path, "read_bytes", edited_note)
    refreshed = hybrid.report()
    assert refreshed["source_sha256"][paths[-1]] != expected[paths[-1]]
    assert all(refreshed["source_sha256"][path] == expected[path] for path in paths[:-1])


def test_huge_prime_uses_bit_lengths_not_field_loops():
    # Completion is an executable regression against iteration over p.
    # This odd integer is a supplied promise, not a primality test fixture.
    result = hybrid.hybrid_codimension_budget(3, 3, 2**4096-1)
    assert result["branch"] == "large_field_rees"
    assert result["prime_certified"] is False
