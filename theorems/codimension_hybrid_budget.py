"""Exact conditional resource certificates, never a hidden-subgroup solver.

The large-field branch composes the existing whole-proof Rees assumptions
with exact abelian-ideal intersections. The small-field branch budgets fresh
classical collisions. Neither branch executes queries, draws randomness,
validates primality, or certifies an actual Lie algebra/hidden subgroup.
"""
from fractions import Fraction
from hashlib import sha256
from math import isqrt
from pathlib import Path

from theorems.rees_uniform_instrument import prime_field_instrument_budget


def _ceil_log2(value):
    """Exact ceiling for the positive rational inputs (all >=1) used here."""
    ceiling = (value.numerator + value.denominator - 1) // value.denominator
    return (ceiling - 1).bit_length()


def hybrid_codimension_budget(dimension, codimension_bound, prime,
                              error=Fraction(1, 3)):
    """Budget the classical/large-field split, conditional on supplied promises.

    Integers must be built-in ints (not bool); error must be a Fraction in
    (0,1). An odd prime p>=3 is a PROMISE: only its type/parity/range are
    checked. The actual class<p, codimension, source independence, coset
    labeling f(x)=f(y) iff x^-1*y is in H, and existing Rees whole-proof
    hypotheses remain unverified. Costs are caps, not measured execution.

    A terminal profile is a coordinatewise envelope, possibly unrealizable.
    Its forest is charged even when the true terminal dimension is smaller
    or no terminal call is necessary. Approximation budgets concern complete
    samplers/instruments, not only their normalized successful branches.
    Growing-class pointwise correctness remains a whole-proof dependency.
    Uniform instrument compilation now has a separate written derivation
    and terminal primitive certificate; neither is a machine-checked proof.
    Oracle evaluation time T_f is separate: T_total <= T_nonoracle + Q*T_f.
    Early abelian exits, including those larger than the Rees envelope, are
    counted within the at-most-n abelian calls, not as Rees terminals.
    """
    if type(dimension) is not int or dimension < 0:
        raise ValueError("dimension must be a nonnegative integer")
    if (type(codimension_bound) is not int
            or not 0 <= codimension_bound <= dimension):
        raise ValueError("codimension bound must be an integer in [0,dimension]")
    if type(prime) is not int or prime < 3 or prime % 2 == 0:
        raise ValueError("a supplied odd prime >=3 is required; primality is not checked")
    if type(error) is not Fraction or not 0 < error < 1:
        raise ValueError("error must be an exact Fraction in (0,1)")
    n, k, p = dimension, codimension_bound, prime
    result = dict(
        status="CONDITIONAL_ON_EXISTING_REES_WHOLE_PROOF_RESOURCE_CERTIFICATE",
        dimension=n, codimension_bound=k, supplied_prime=p, error_target=error,
        prime_contract="SUPPLIED_PROMISE_NOT_VERIFIED",
        actual_class_contract="SUPPLIED_ACTUAL_NILPOTENCY_CLASS_LT_PRIME",
        source_contract="Fresh independent uniform sources; exact hidden-coset labels.",
        whole_proof_dependency="Existing Rees pointwise/source correctness, plus the written "
                               "uniform prime-field instrument compilation derivation.",
        growing_class_pointwise_correctness_supplied_promise=True,
        growing_class_uniform_complete_instrument_efficiency_supplied_promise=False,
        uniform_compilation_status="DERIVED_IN_WRITTEN_ARGUMENT_NOT_MACHINE_CERTIFIED",
        uniform_compilation_derivation="research/REES_UNIFORM_INSTRUMENT_COMPILATION.md",
        growing_class_pointwise_correctness_certified=False,
        growing_class_uniform_complete_instrument_efficiency_certified=False,
        fixed_class_correctness_alone_suffices=False,
        prime_validation_included=False, prime_certified=False,
        actual_class_certified=False, codimension_promise_certified=False,
        profile_existence_certified=False, hidden_intersection_completeness_certified=False,
        resource_certificate_only=True, oracle_queries_executed=0,
        solver_implemented=False, quantum_receiver_implemented=False,
        hidden_oracle_benchmark=False, field_enumeration_used=False,
        native_application_established=False, novelty_established=False,
        speedup_claim_allowed=False, formal_total_policy_instantiated=False,
        deterministic_arithmetic_step_counter=False, physical_gate_clock=False,
        cost_scope="Exact query, source, randomness and algebraic primitive caps; "
                   "not a gate, public linear-algebra, label-bit-cost or wall-clock count.",
        runtime_model=dict(
            total_time_bound="T_nonoracle + Q*T_f",
            Q="original_queries",
            T_f="Separately charged upper bound on one original oracle evaluation.",
            T_nonoracle="Nonoracle operations, including label processing and uniformly "
                        "efficient complete instruments, under the supplied bit-cost promises.",
            oracle_evaluation_time_included_in_resource_caps=False,
            oracle_evaluation_cost_certified=False,
            label_width_is_oracle_evaluation_cost=False,
            label_processing_cost_charged_to_nonoracle_time=True,
            label_width_is_a_separate_bit_complexity_parameter=True,
        ),
        complexity=dict(
            overall="2^O(k^2 log(k+2)) * poly(n,log(p),label_width,log(1/error))",
            large_field="2^O(k log(k+2)) * poly(n,log(p),label_width,log(1/error))",
            parameter="codimension_bound",
            scope="Oracle call count and conditional nonoracle operation bounds, "
                  "not a bound on the cost of evaluating the oracle.",
            basis="Terminal dimension O(k^2), class O(k), whole-grade arity product.",
            uses_generic_derived_rank_bound=False,
            conditional_on_existing_rees_whole_proof=True,
        ),
        branch_requires_rees=False,
        field_threshold=None, classical=None, abelian_intersections=None,
        terminal_rees=None, terminal_uniform_instrument=None, terminal_profile_is_envelope=False,
        original_queries=0, original_inputs=0, abelian_original_queries=0,
        terminal_original_queries=0, query_transport_original_queries_per_call=1,
        classical_uniform_draw_cap=0, classical_fair_bit_cap=0,
        classical_root_pow_gcd_pair_cap=0, total_error_bound=Fraction(0),
    )
    if k == 0:
        result.update(branch="zero_query", zero_query_reason="The promised hidden subgroup is the whole group.")
        return result

    threshold = 16 * (2*k)**(4*k + 2)
    result["field_threshold"] = threshold
    if p < threshold:
        index = p**k
        batch_size = isqrt(2*index) + 2
        slack = _ceil_log2(3/error)
        samples = n + slack
        batches = _ceil_log2(3*samples/error)
        group_draws = samples * batches * batch_size
        scalar_calls = n * group_draws
        rejection_cap = _ceil_log2(3*scalar_calls/error)
        bit_width = (p-1).bit_length()
        collision_error = Fraction(samples, 2**batches)
        rank_error = Fraction(1, 2**slack)
        field_error = Fraction(scalar_calls, 2**rejection_cap)
        result.update(
            branch="classical_collisions", original_queries=group_draws,
            original_inputs=group_draws, classical_uniform_draw_cap=scalar_calls,
            classical_fair_bit_cap=scalar_calls*rejection_cap*bit_width,
            total_error_bound=collision_error+rank_error+field_error,
            classical=dict(
                index_cap=index, batch_size=batch_size,
                birthday_exponent_lower_bound=Fraction(batch_size*(batch_size-1), 2*index),
                no_collision_probability_upper_bound=Fraction(1, 2),
                no_collision_bound_is_strict=True,
                collision_selection="First repeated label in draw order; pair with its first occurrence.",
                collision_selection_uses_only_labels=True,
                accepted_element="x^-1*y; exactly uniform on H conditional on batch acceptance",
                accepted_elements_are_independent_under_source_promise=True,
                identity_elements_retained=True,
                rank_slack=slack, accepted_hidden_elements=samples,
                batches_per_hidden_element=batches, fresh_batch_cap=samples*batches,
                group_draw_cap=group_draws, original_query_cap=group_draws,
                group_inverse_cap=samples, group_product_cap=samples,
                label_processing="Sort by label and index, scan adjacent equal labels; retain earliest second index.",
                label_order_comparison_cap=samples*batches*batch_size*_ceil_log2(Fraction(batch_size)),
                label_equality_comparison_cap=samples*batches*(batch_size-1),
                label_comparison_bit_cost_parameter="label_width plus O(log(batch_size)) index bits",
                batch_coordinate_storage_cap=n*batch_size,
                accepted_coordinate_storage_cap=n*samples,
                scalar_uniform_draw_cap=scalar_calls, scalar_coordinates_per_group_draw=n,
                integer_rejection_cap=rejection_cap, bits_per_rejection_attempt=bit_width,
                fair_bit_cap=scalar_calls*rejection_cap*bit_width,
                collision_failure_bound=collision_error, rank_failure_bound=rank_error,
                field_draw_failure_bound=field_error,
                collision_error_share=error/3, rank_error_share=error/3,
                field_draw_error_share=error/3,
                index_parameter_envelope=threshold**k,
            ),
        )
        return result

    m = k*(k+1)//2
    class_bound = 1 if m == 1 else min(2*k-1, m-1)
    profile = (m,) + tuple(m-grade for grade in range(2, class_bound+1))
    terminal_instrument = prime_field_instrument_budget(profile, prime=p, error=error/2)
    terminal = terminal_instrument["recovery_budget"]
    terminal.update(
        profile_role="UNREALIZED_UPPER_ENVELOPE_NOT_ACTUAL_INPUT_PROFILE",
        actual_class_field_is_envelope_length_not_certification=True,
    )
    terminal_instrument["profile_role"] = "UNREALIZED_UPPER_ENVELOPE_NOT_ACTUAL_INPUT_PROFILE"
    extra = _ceil_log2(4*n/error)
    per_call = n + extra
    abelian_queries = n*per_call
    rank_error = Fraction(n, 2**extra)
    sampler_share = error/4
    # This class-sensitive product, not the generic derived-rank envelope,
    # has only O(k) factors with polynomial-in-k arities.
    arity_bound = (m+1)*((2*k-1)*m+1)
    result.update(
        branch="large_field_rees", branch_requires_rees=True, terminal_dimension_bound=m,
        terminal_class_bound=class_bound, terminal_envelope_profile=profile,
        terminal_profile_is_envelope=True, terminal_rees=terminal,
        terminal_uniform_instrument=terminal_instrument,
        terminal_leaf_parameter_bound=arity_bound**(class_bound-1),
        terminal_stage_arity_parameter_bound=arity_bound,
        abelian_intersections=dict(
            call_cap=n, samples_per_call=per_call, rank_slack=extra,
            early_abelian_terminal_solves_included=True,
            early_abelian_dimension_bound=n,
            complete_sampler_call_cap=abelian_queries,
            original_query_cap=abelian_queries,
            rank_failure_bound=rank_error, rank_error_share=error/4,
            complete_sampler_approximation_share=sampler_share,
            complete_sampler_error_per_call=sampler_share/abelian_queries,
            exact_intersection_required=True,
            source="Independent abelian Fourier samples, subject to complete-sampler approximation share.",
        ),
        abelian_original_queries=abelian_queries,
        terminal_original_queries=terminal["original_inputs"],
        original_queries=abelian_queries+terminal["original_inputs"],
        original_inputs=abelian_queries+terminal["original_inputs"],
        terminal_error_share=error/2,
        total_error_bound=rank_error+sampler_share+terminal["total_error_bound"],
        classical_uniform_draw_cap=terminal["classical_uniform_draw_cap"],
        classical_fair_bit_cap=terminal["classical_fair_bit_cap"],
        classical_root_pow_gcd_pair_cap=terminal["classical_root_pow_gcd_pair_cap"],
    )
    return result


def exact_json(value):
    """JSON-compatible structure without converting any rational to a float."""
    if isinstance(value, Fraction):
        return dict(numerator=value.numerator, denominator=value.denominator)
    if isinstance(value, dict):
        return {key: exact_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [exact_json(item) for item in value]
    return value


def report():
    """Small exact cases bound to current sources, not proof promotion.

    Re-read sources on each call so a final regeneration binds subsequent
    edits to the proof note or dependencies. Hashes certify byte identity,
    never mathematical correctness or completion of the whole-proof inputs.
    """
    root = Path(__file__).resolve().parents[1]
    proof_note = "research/BOUNDED_CODIMENSION_HYBRID_BOUND.md"
    sources = (
        "theorems/codimension_hybrid_budget.py",
        "theorems/uniform_bch_rees.py",
        "theorems/power_sde.py",
        "theorems/power_sde_budget.py",
        "theorems/bounded_codimension_reduction.py",
        "theorems/rees_uniform_instrument.py",
        "research/REES_UNIFORM_INSTRUMENT_COMPILATION.md",
        proof_note,
    )
    return exact_json(dict(
        status="CONDITIONAL_ON_EXISTING_REES_WHOLE_PROOF_RESOURCE_CERTIFICATE",
        proof_note=proof_note,
        source_sha256={path: sha256((root/path).read_bytes()).hexdigest() for path in sources},
        source_hashes_certify_proof=False, candidate_promotion=False, proof_promotion=False,
        growing_class_pointwise_correctness_supplied_promise=True,
        growing_class_uniform_complete_instrument_efficiency_supplied_promise=False,
        uniform_compilation_status="DERIVED_IN_WRITTEN_ARGUMENT_NOT_MACHINE_CERTIFIED",
        uniform_compilation_derivation="research/REES_UNIFORM_INSTRUMENT_COMPILATION.md",
        fixed_class_correctness_alone_suffices=False,
        total_time_bound="T_nonoracle + Q*T_f",
        oracle_evaluation_cost_certified=False, label_width_is_oracle_evaluation_cost=False,
        resource_certificate_only=True, hidden_oracle_benchmark=False,
        prime_validation_included=False, profile_existence_certified=False,
        quantum_receiver_implemented=False, native_application_established=False,
        speedup_claim_allowed=False,
        cases=[hybrid_codimension_budget(n, k, p)
               for n, k, p in ((10, 3, 7), (10, 3, 2**127-1), (32, 12, 7), (16, 8, 101))],
    ))
