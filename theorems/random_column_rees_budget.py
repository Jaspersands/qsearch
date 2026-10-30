"""Conditional IID-label Rees tree caps, never quantum execution.

The intrinsic label-rank bound is a source promise, not inferred from the
observed rank of one bank. Whole failed trees are paid. This certificate
does not establish Rees correctness, source access, primality, or novelty.
"""
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path
import random

from theorems.random_column_power_sde import (
    projective_bank_bounds, random_column_budget, random_column_power_sde,
)
from theorems.uniform_bch_rees import scalar_line_budget


def _ceil_log2(value):
    integer = (value.numerator+value.denominator-1)//value.denominator
    return (integer-1).bit_length()


def random_column_tree_budget(profile, *, prime, uniform_parameter,
                              intrinsic_rank_bound, error=Fraction(1, 3)):
    """Padded large-field tree with bounded whole-tree restart and fair bits.

    This mode requires p>=16*u^2 and u>=max(c,a_bound+1,2). It deliberately
    does not execute the potentially enormous classical kernel-trial cap.
    The ordinary source, not copy-only source creation, is counted here.
    """
    if type(error) is not Fraction or not 0 < error < 1:
        raise ValueError("exact error Fraction in (0,1) required")
    if (type(uniform_parameter) is not int or uniform_parameter < 2
            or type(intrinsic_rank_bound) is not int or intrinsic_rank_bound < 0):
        raise ValueError("integer u>=2 and intrinsic rank bound>=0 required")
    if prime is None:
        raise ValueError("a supplied verified prime is required")
    base = scalar_line_budget(profile, 1, prime=prime)
    profile = base.lower_central_dimensions
    c, n, dimension = len(profile), profile[0], sum(profile)
    u, a_bound = uniform_parameter, intrinsic_rank_bound
    if u < max(c, a_bound+1):
        raise ValueError("require u>=class and u>intrinsic rank bound")
    if prime < 16*u*u:
        raise ValueError("random-column tree field guard p>=16*u^2 fails")
    width = 4*u
    leaves = width**(c-1)
    merges = (leaves-1)//(width-1)
    bits = _ceil_log2(Fraction(64*leaves))
    samples = n+_ceil_log2(3/error)
    attempts = 4*samples
    stages = []
    for grade, rank in enumerate(profile[1:], start=2):
        degree = gcd(grade, prime-1)
        a = min(rank, a_bound)
        moments = projective_bank_bounds(prime, degree, a, width)
        directions, mean = moments["D"], moments["mu"]
        bank_error = moments["bad_bank_upper"]
        nonlinear = degree > 1 and a > 0
        kernel_trials = 4*degree**width*bits if nonlinear else 0
        budget = random_column_budget(prime, degree, width, attempt_cap=kernel_trials,
                                      failure_bits=bits) if nonlinear else None
        root_cap = budget["root_split_attempt_cap"] if budget else 0
        roots = budget["root_call_cap"] if budget else 0
        calls = budget["uniform_call_cap"] if budget else 0
        rejection = budget["integer_rejection_cap"] if budget else 0
        root_error = budget["root_abort_upper"] if budget else Fraction(0)
        bit_error = budget["bit_abort_upper"] if budget else Fraction(0)
        kernel_error = Fraction(1, 2**bits) if nonlinear else Fraction(0)
        node_error = bank_error+kernel_error+root_error+bit_error if nonlinear else Fraction(0)
        nodes = width**(grade-2)
        stage_dimension = sum(profile[:grade])
        brackets = (grade-1)*grade*(grade+1)*(grade+2)//6
        stages.append(dict(
            grade=grade, ambient_label_dimension=rank, intrinsic_rank_upper_bound=a,
            reduced_degree=degree, width=width, conversions_per_tree=nodes,
            projective_directions=directions, projective_count_mean_lower_bound=mean,
            iid_bad_bank_bound=bank_error,
            good_bank_power_kernel_density_lower_bound=moments["good_bank_kernel_power_density_lower"],
            kernel_trial_cap=kernel_trials, kernel_exhaustion_bound=kernel_error,
            root_call_cap=roots, root_split_attempt_cap=root_cap,
            root_failure_bound=root_error, uniform_field_draw_cap=calls,
            integer_rejection_cap=rejection, integer_rejection_bound=bit_error,
            fair_bit_cap=calls*rejection*(prime-1).bit_length(),
            node_abort_bound=node_error,
            root_pow_gcd_pair_cap=roots*(degree-1)*root_cap,
            qft_calls_per_conversion=2*width*rank+stage_dimension-rank,
            bracket_calls_per_conversion=4*width*brackets,
        ))
    tree_abort = sum((s["conversions_per_tree"]*s["node_abort_bound"] for s in stages), Fraction(0))
    if tree_abort > Fraction(1, 16):
        raise ArithmeticError("one-tree constant failure budget failed")
    total_leaves, total_merges = attempts*leaves, attempts*merges
    instruments = total_leaves+total_merges+samples
    qmax = max(dimension, n, *(s["qft_calls_per_conversion"] for s in stages))
    qfts = total_leaves*dimension+samples*n+attempts*sum(
        s["conversions_per_tree"]*s["qft_calls_per_conversion"] for s in stages)
    eta = error/(3*instruments*qmax)
    fewer = Fraction(1, 2**(2*samples))
    rank_error = Fraction(1, (prime-1)*prime**(samples-n))
    return dict(
        status="CONDITIONAL_RANDOM_COLUMN_REES_BOUND_NOT_RECEIVER_EXECUTION",
        profile=profile, supplied_prime=prime, uniform_parameter=u,
        intrinsic_rank_bound=a_bound, field_threshold=16*u*u,
        width_per_grade=width, leaves_per_tree=leaves, merges_per_tree=merges,
        classical_failure_bits_per_node=bits, stages_top_down=list(reversed(stages)),
        tree_abort_bound=tree_abort, tree_abort_bound_used_for_restart=Fraction(1, 4),
        desired_terminal_samples=samples, whole_tree_attempt_cap=attempts,
        lifted_source_cap=total_leaves, original_oracle_query_cap=c*total_leaves,
        all_failed_trees_charged=True, labels_resampled_inside_kernel_trials=False,
        successful_outputs_required_to_decouple_from_records=True,
        fewer_successes_failure_bound=fewer, final_rank_failure_bound=rank_error,
        complete_instrument_call_cap=instruments, single_coordinate_qft_call_cap=qfts,
        qft_isometry_error_per_call=eta, qft_precision_bits=_ceil_log2(1/eta),
        complete_quantum_error_bound=qfts*eta,
        total_error_bound=fewer+rank_error+qfts*eta, error_target=error,
        classical_kernel_trial_cap=attempts*sum(s["conversions_per_tree"]*s["kernel_trial_cap"] for s in stages),
        classical_fair_bit_cap=attempts*sum(s["conversions_per_tree"]*s["fair_bit_cap"] for s in stages),
        classical_root_pow_gcd_pair_cap=attempts*sum(s["conversions_per_tree"]*s["root_pow_gcd_pair_cap"] for s in stages),
        compiled_bracket_call_cap=attempts*sum(s["conversions_per_tree"]*s["bracket_calls_per_conversion"] for s in stages),
        iid_intrinsic_label_law_required=True, joint_source_law_verified=False,
        observed_bank_rank_certifies_intrinsic_rank=False,
        fixed_bank_success_guaranteed=False, prime_validation_included=False,
        profile_existence_certified=False, intrinsic_rank_promise_verified=False,
        oracle_queries_executed=0, quantum_receiver_implemented=False,
        circuit_generator_implemented=False, physical_gate_clock=False,
        whole_rees_correctness_certified=False, novelty_established=False,
        native_application_established=False, speedup_claim_allowed=False,
        runtime_model="T_nonoracle + original_oracle_query_cap*T_f",
    )


def report():
    """Resource caps plus bounded seeded arithmetic controls, never HSP runs."""
    root = Path(__file__).resolve().parents[1]
    note = "research/RANDOM_COLUMN_REES_PARAMETER_BOUND.md"
    sources = (
        "theorems/random_column_rees_budget.py", "theorems/random_column_power_sde.py",
        "theorems/uniform_bch_rees.py", "theorems/bounded_power_roots.py",
        "theorems/power_sde_budget.py", note,
        "research/REES_UNIFORM_INSTRUMENT_COMPILATION.md",
    )
    cases = [
        random_column_tree_budget((3, 1), prime=101, uniform_parameter=2, intrinsic_rank_bound=1),
        random_column_tree_budget((6, 3, 1), prime=1009, uniform_parameter=4, intrinsic_rank_bound=3),
        random_column_tree_budget((13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1),
                                  prime=65537, uniform_parameter=12, intrinsic_rank_bound=11),
        random_column_tree_budget((6, 4, 3, 2, 1), prime=577,
                                  uniform_parameter=6, intrinsic_rank_bound=3),
    ]
    cases[-1]["profile_role"] = "CODIMENSION_3_TERMINAL_ENVELOPE_NOT_REALIZABILITY_CLAIM"
    controls = []
    for p, degree, width in ((101, 2, 8), (1009, 3, 6)):
        source = random.Random(741+p)
        bank = [(source.randrange(p),) for _ in range(width)]
        controls.append(random_column_power_sde(
            p, degree, bank, rank_bound=1, attempt_cap=8192,
            failure_bits=20, bit_source=random.Random(993+p)))
    adversarial = random_column_power_sde(
        5, 4, [(1,)]*3, rank_bound=1, attempt_cap=64,
        failure_bits=20, bit_source=random.Random(996))
    if any(control["status"] != "VERIFIED" for control in controls) or adversarial["status"] != "ABORT":
        raise ArithmeticError("bounded arithmetic report control changed")
    return dict(
        status="CONDITIONAL_RANDOM_COLUMN_REES_BOUND_NOT_RECEIVER_EXECUTION",
        proof_note=note,
        source_sha256={path:sha256((root/path).read_bytes()).hexdigest() for path in sources},
        source_hashes_certify_proof=False, cases=cases,
        arithmetic_controls=controls, adversarial_bank_control=adversarial,
        arithmetic_controls_certify_iid_source=False,
        proposed_all_prime_derived_factor="2^O(r log(r+2))",
        proposed_all_prime_codimension_factor="2^O(k log(k+2))",
        small_prime_derived_fallback="Published quantum small-commutator algorithm, not implemented here.",
        small_prime_codimension_fallback="Previously analyzed classical birthday algorithm.",
        quantum_receiver_implemented=False, novelty_established=False,
        candidate_promotion=False, proof_promotion=False, speedup_claim_allowed=False,
    )
