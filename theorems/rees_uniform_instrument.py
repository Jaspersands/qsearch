"""Prime-field Rees primitive budgets, not emitted circuits or HSP execution.

The supplied Lie profile and prime remain mathematical promises. Uniform
compilation is a written derivation using known QFT constructions and public
reversible arithmetic; the counters do not certify that derivation or the
underlying Rees identities. Only the ordinary, exact coherent-oracle route
is counted. Copy-source preparation has a different circuit schedule.
"""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

from theorems.uniform_bch_rees import symmetric_recovery_budget


def _ceil_log2(value):
    ceiling = (value.numerator + value.denominator - 1) // value.denominator
    return (ceiling - 1).bit_length()


def prime_field_instrument_budget(profile, *, prime, error=Fraction(1, 3)):
    """Refine the bounded whole-grade forest to a uniform primitive schedule.

    All counts are padded upper bounds, including abort paths and zero-scale
    targets. The qft error is an all-input, clean-workspace isometry error on
    the canonical subspace, NOT a basis-state probability error. Arithmetic
    is exact in the ideal finite-gate model; oracle approximation is excluded.
    No primality, Lie-algebra existence, class, or oracle promise is verified.
    """
    forest = symmetric_recovery_budget(profile, prime=prime, error=error)
    dimensions = forest["lower_central_dimensions"]
    c, n, dimension = len(dimensions), dimensions[0], sum(dimensions)
    leaves = forest["source_preparations"]
    samples = forest["final_fourier_samples"]
    stages = []
    for stage in forest["stages_top_down"]:
        d, rank = stage["grade"], stage["rank"]
        arity, nodes = stage["arity"], stage["conversions"]
        group_dimension = sum(dimensions[:d])
        quotient_dimension = group_dimension - rank
        # An XOR evaluator computes/copies/uncomputes; in-place translation
        # uses both forward and inverse XOR evaluators, hence four BCH passes.
        bch_passes = 4 * arity * nodes
        brackets_per_pass = (d - 1) * d * (d + 1) * (d + 2) // 6
        stages.append(dict(
            grade=d, central_dimension=rank, group_dimension=group_dimension,
            quotient_dimension=quotient_dimension, arity=arity, conversions=nodes,
            qft_calls_per_conversion=2*arity*rank+quotient_dimension,
            qft_calls=nodes*(2*arity*rank+quotient_dimension),
            central_coordinate_subtractions=nodes*arity*rank,
            controlled_right_actions=nodes*arity,
            bch_evaluation_passes=bch_passes,
            bracket_calls_per_bch_pass=brackets_per_pass,
            bracket_calls=bch_passes*brackets_per_pass,
            dense_structure_tensor_terms=bch_passes*brackets_per_pass*group_dimension**3,
        ))
    leaf_qfts, final_qfts = leaves*dimension, samples*n
    qfts = leaf_qfts + final_qfts + sum(s["qft_calls"] for s in stages)
    qmax = max(dimension, n, *(s["qft_calls_per_conversion"] for s in stages))
    instruments = forest["complete_instrument_calls"]
    eta = error / (3*instruments*qmax)
    edges = sum(s["controlled_right_actions"] for s in stages)
    if edges != leaves + forest["sde_calls"] - samples:
        raise ArithmeticError("fresh-source forest edge identity failed")
    if qfts > 6*dimension*leaves or qfts > instruments*qmax:
        raise ArithmeticError("Fourier primitive envelope failed")
    return dict(
        status="UNIFORM_PRIMITIVE_CERTIFICATE_NOT_CIRCUIT_EXECUTION",
        input_model="Explicit prime-field Lie coordinates; exact ordinary coherent hiding oracle.",
        recovery_budget=forest, supplied_prime=prime,
        canonical_field_limb_bits=(prime-1).bit_length(),
        cover_group_register_bits=dimension*(prime-1).bit_length(),
        stages_top_down=stages, forest_edges=edges,
        leaf_preparation_qft_calls=leaf_qfts, final_readout_qft_calls=final_qfts,
        single_coordinate_qft_calls=qfts,
        single_coordinate_qft_envelope=6*dimension*leaves,
        qft_calls_per_instrument_cap=qmax,
        qft_isometry_error_per_call=eta,
        qft_precision_bits=_ceil_log2(1/eta),
        qft_error_bound=qfts*eta,
        per_instrument_qft_error_bound=qmax*eta,
        complete_output_error_bound=(forest["rank_failure_bound"]
                                     + forest["solver_abort_bound"] + qfts*eta),
        ordinary_oracle_queries=c*leaves,
        leaf_linear_evaluation_compute_uncompute_pairs=c*leaves,
        central_coordinate_subtractions=sum(s["central_coordinate_subtractions"] for s in stages),
        controlled_right_actions=edges,
        bch_evaluation_passes=sum(s["bch_evaluation_passes"] for s in stages),
        bracket_calls=sum(s["bracket_calls"] for s in stages),
        dense_structure_tensor_terms=sum(s["dense_structure_tensor_terms"] for s in stages),
        classical_fair_bit_cap=forest["classical_fair_bit_cap"],
        classical_root_pow_gcd_pair_cap=forest["classical_root_pow_gcd_pair_cap"],
        compilation_derivation="research/REES_UNIFORM_INSTRUMENT_COMPILATION.md",
        uniform_compilation_status="DERIVED_IN_WRITTEN_ARGUMENT_NOT_MACHINE_CERTIFIED",
        canonical_subspace_reference_stable_error_required=True,
        joint_source_error_required=True,
        invalid_binary_records_abort=True,
        canonical_forbidden_labels_require_hidden_membership_test=False,
        zero_scale_is_identity_not_delta_zero=True,
        all_target_slots_consumed=True, classical_retry_extra_source_copies=0,
        cost_scope="Padded primitive caps; known uniform polynomial circuits, not a physical gate estimate.",
        runtime_model="T_nonoracle + ordinary_oracle_queries*T_f; oracle cost T_f separately supplied.",
        arbitrary_modulus_qft_cost="poly(log(p)+log(1/eta)), including finite-gate synthesis",
        bch_boolean_size_bound="O((d+1)^4*(D_d+1)^3*(log(p)+1)^3) per evaluation",
        internal_qft_gate_synthesis_errors_included_in_eta=True,
        exact_oracle_assumed=True, approximate_oracle_error_included=False,
        prime_validation_included=False, profile_existence_certified=False,
        circuit_generator_implemented=False, quantum_receiver_implemented=False,
        formal_total_policy_instantiated=False, physical_gate_clock=False,
        oracle_queries_executed=0, field_enumeration_used=False,
        whole_rees_correctness_certified=False, novelty_established=False,
        native_application_established=False, speedup_claim_allowed=False,
    )


def report():
    """Bind the resource calculation and mathematical contract to source bytes."""
    root = Path(__file__).resolve().parents[1]
    proof_note = "research/REES_UNIFORM_INSTRUMENT_COMPILATION.md"
    sources = (
        "theorems/rees_uniform_instrument.py", "theorems/uniform_bch_rees.py",
        "theorems/guarded_bch_permutation.py", "theorems/power_sde.py",
        "theorems/power_sde_budget.py", proof_note,
    )
    return dict(
        status="UNIFORM_PRIMITIVE_CERTIFICATE_NOT_CIRCUIT_EXECUTION",
        proof_note=proof_note,
        source_sha256={path: sha256((root/path).read_bytes()).hexdigest() for path in sources},
        source_hashes_certify_proof=False,
        uniform_compilation_status="DERIVED_IN_WRITTEN_ARGUMENT_NOT_MACHINE_CERTIFIED",
        oracle_queries_executed=0, circuit_generator_implemented=False,
        quantum_receiver_implemented=False, whole_rees_correctness_certified=False,
        candidate_promotion=False, proof_promotion=False,
        novelty_established=False, speedup_claim_allowed=False,
        cases=[prime_field_instrument_budget(profile, prime=p)
               for profile, p in (((4,), 2), ((6, 3, 1), 65537),
                                  ((13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1), 2**127-1))],
    )
