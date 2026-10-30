"""Fixed-bank unit witnesses and paid pilots for mixed-order cancellation.

Only public-label arithmetic is executed. No physical source, complete
quantum receiver, all-prime ring HSP bound or novelty is certified here.
"""
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path
import random

from theorems.pilot_submodule import compile_pilot_frame
from theorems.prime_power_rees_descent import (
    _module_contract, lift_regular_module_witness, verify_module_witness,
)
from theorems.random_column_power_sde import (
    random_column_budget, random_column_power_sde, unit_projective_bank_bounds,
)
from theorems.symbolic_scalar_phase_erasure import _fmpz_rref
from theorems.weighted_two_erasure_cascade import bezout_reduced_exponent


def unit_module_plan(*, prime, degree, cyclic_rank_bound, uniform_parameter,
                     failure_bits=8, attempt_cap=None):
    """Exact conditional episode bounds, possibly vacuous outside the guard.

    A small supplied attempt cap is never upgraded to the recommended cap.
    The caller must supply fresh IID labels and independent fair bits.
    """
    R, u = cyclic_rank_bound, uniform_parameter
    if type(R) is not int or R < 1 or type(u) is not int or u < max(2, R+1):
        raise ValueError("positive cyclic rank and u>=max(2,R+1) required")
    if type(failure_bits) is not int or failure_bits < 1:
        raise ValueError("positive integer failure_bits required")
    _module_contract([(0,)], (1,), prime, degree)
    if u < degree:
        raise ValueError("u must bound the original grade degree")
    width, reduced = 4*u, gcd(degree, prime-1)
    block_size = 2*(2*reduced)**width
    recommended = block_size*failure_bits
    cap = recommended if attempt_cap is None else attempt_cap
    arithmetic = random_column_budget(prime, reduced, width,
                                      attempt_cap=cap, failure_bits=failure_bits)
    moments = unit_projective_bank_bounds(prime, reduced, R, width)
    pilot_failure = Fraction(1, (prime-1)*prime**(width-R))
    # exp(-K/block_size) <= 2^-floor(K/block_size); retain a vacuous
    # bound when a deliberately small execution cap buys no whole block.
    kernel_failure = Fraction(1, 2**(cap//block_size))
    failure = pilot_failure+moments["bad_bank_upper"]+kernel_failure+arithmetic["auxiliary_abort_upper"]
    return dict(
        prime=prime, degree=degree, reduced_degree=reduced,
        cyclic_rank_bound=R, uniform_parameter=u,
        pilot_source_count=width, bank_source_count=width,
        source_labels_cap=2*width, failure_bits=failure_bits,
        recommended_kernel_trial_cap=recommended, kernel_trial_cap=cap,
        recommended_cap_met=cap >= recommended,
        pilot_incompleteness_bound=pilot_failure,
        iid_bad_bank_bound=moments["bad_bank_upper"],
        kernel_exhaustion_bound=kernel_failure,
        auxiliary_arithmetic_abort_bound=arithmetic["auxiliary_abort_upper"],
        episode_abort_bound=min(Fraction(1), failure), arithmetic_budget=arithmetic,
        projective_moments=moments, field_threshold=16*u*u,
        large_field_guard_satisfied=prime >= 16*u*u,
        fresh_iid_source_required=True, iid_fair_bits_required=True,
        hidden_support_certified=False, quantum_receiver_implemented=False,
    )


def unit_module_witness(columns, *, prime, exponents, degree,
                        attempt_cap, failure_bits=8, bit_source=None):
    """One supplied intrinsic bank; no label refresh, support or minor search."""
    columns, exponents, _ = _module_contract(columns, exponents, prime, degree)
    reduced, lift_exponent = bezout_reduced_exponent(prime, degree)
    width, rank = len(columns), len(exponents)
    if width <= rank:
        raise ValueError("bank width must exceed intrinsic cyclic rank")
    random_column_budget(prime, reduced, width, attempt_cap=attempt_cap,
                         failure_bits=failure_bits)
    field_columns = [tuple(x % prime for x in col) for col in columns]
    observed = _fmpz_rref(list(map(list, zip(*field_columns))), prime)[1]
    result = dict(status="ABORT", reason="INTRINSIC_RESIDUE_RANK_DEFICIENT",
                  original_degree=degree, reduced_degree=reduced,
                  bezout_exponent=lift_exponent, intrinsic_cyclic_rank=rank,
                  residue_rank=observed, bank_columns=columns,
                  exponents=exponents, scales=None, labels_resampled=False,
                  quantum_receiver_implemented=False, source_law_certified=False)
    if observed != rank:
        return result
    field = random_column_power_sde(
        prime, reduced, field_columns, rank_bound=rank, attempt_cap=attempt_cap,
        failure_bits=failure_bits, bit_source=bit_source, require_nonzero=True)
    result["field_run"] = field
    if field["status"] != "VERIFIED":
        result["reason"] = field["reason"]
        return result
    weights = [pow(w, lift_exponent, prime) for w in field["weights"]]
    if not all(weights):
        raise ArithmeticError("unit kernel solver lost a coordinate")
    lifted = lift_regular_module_witness(columns, weights, prime=prime,
                                        exponents=exponents, degree=degree)
    if not lifted["original_module_verified"] or not all(s % prime for s in lifted["scales"]):
        raise ArithmeticError("full-support field witness lost regularity or units")
    result.update(status="VERIFIED_UNIT_MODULE_WITNESS", reason="EXACT_MIXED_ORDER_CANCELLATION",
                  field_witness_original_degree=weights, lift=lifted, scales=lifted["scales"])
    return result


def unit_pilot_episode(*, prime, ambient_exponents, degree, uniform_parameter,
                       draw_labels, attempt_cap, failure_bits=8, bit_source=None):
    """One bounded public-label episode. Incomplete pilots can safely succeed.

    The normal-form backend and label callback are not locally hard-clocked.
    Bad encodings/backend failures raise; canonical membership/rank failures
    and capped statistical failures explicitly abort.
    """
    exponents = tuple(ambient_exponents)
    _module_contract([(0,)*len(exponents)], exponents, prime, degree)
    plan = unit_module_plan(prime=prime, degree=degree, cyclic_rank_bound=len(exponents),
                            uniform_parameter=uniform_parameter, failure_bits=failure_bits,
                            attempt_cap=attempt_cap)
    if not callable(draw_labels):
        raise ValueError("finite label-bank callback required")
    source = random.SystemRandom() if bit_source is None else bit_source
    if isinstance(source, type) or not callable(getattr(source, "getrandbits", None)):
        raise ValueError("bit_source instance with callable getrandbits required")
    requests = []
    result = dict(status="ABORT", reason=None, plan=plan, requests=requests,
                  source_labels_consumed=0, quantum_receiver_implemented=False,
                  hidden_support_completeness_certified=False,
                  physical_iid_source_certified=False, normal_form_clock_certified=False)

    def acquire(count, stage):
        raw = draw_labels(count)
        if not isinstance(raw, (list, tuple)) or len(raw) != count:
            raise ValueError("source must return exactly the requested finite bank")
        columns, _, _ = _module_contract(raw, exponents, prime, degree)
        requests.append(dict(stage=stage, count=count, ambient_columns=columns))
        result["source_labels_consumed"] += count
        return columns

    pilots = acquire(plan["pilot_source_count"], "pilots")
    frame = compile_pilot_frame(prime=prime, ambient_exponents=exponents, pilot_columns=pilots)
    result["frame"] = frame.certificate()
    bank = acquire(plan["bank_source_count"], "bank")
    encoded = [frame.encode(col) for col in bank]
    requests[-1]["intrinsic_columns"] = encoded
    if any(col is None for col in encoded):
        result["reason"] = "OUTSIDE_PILOT_FRAME"
        return result
    if [frame.decode(col) for col in encoded] != list(bank):
        raise ArithmeticError("pilot embedding failed on original bank")
    if not frame.intrinsic_exponents:
        scales = [1]*len(bank)
        result["zero_rank_branch"] = True
    else:
        inner = unit_module_witness(encoded, prime=prime, exponents=frame.intrinsic_exponents,
                                    degree=degree, attempt_cap=attempt_cap,
                                    failure_bits=failure_bits, bit_source=source)
        result["intrinsic_run"] = inner
        if inner["status"] != "VERIFIED_UNIT_MODULE_WITNESS":
            result["reason"] = inner["reason"]
            return result
        scales = inner["scales"]
        result["zero_rank_branch"] = False
    if (not all(s % prime for s in scales)
            or not verify_module_witness(bank, scales, prime=prime, exponents=exponents, degree=degree)):
        raise ArithmeticError("unit witness failed original ambient-module verification")
    if result["source_labels_consumed"] != plan["source_labels_cap"]:
        raise ArithmeticError("fixed episode source accounting mismatch")
    result.update(status="VERIFIED_AMBIENT_UNIT_WITNESS", reason="EXACT_AMBIENT_CANCELLATION",
                  selected_request_indices=[1], selected_ambient_columns=bank,
                  scales=scales, original_ambient_verified=True)
    return result


def unit_tree_source_bound(*, prime, class_bound, cyclic_rank_bound, uniform_parameter):
    """Conditional predecessor tree only, NOT complete ring HSP accounting."""
    c, u = class_bound, uniform_parameter
    if type(c) is not int or c < 2 or type(u) is not int or u < c:
        raise ValueError("2<=class_bound<=u required")
    if prime < 16*u*u:
        raise ValueError("large-field tree requires p>=16*u^2")
    width = 8*u
    leaves = width**(c-1)
    bits = (64*leaves-1).bit_length()
    stages = []
    for grade in range(2, c+1):
        plan = unit_module_plan(prime=prime, degree=grade, cyclic_rank_bound=cyclic_rank_bound,
                                uniform_parameter=u, failure_bits=bits)
        stages.append(dict(grade=grade, nodes=width**(grade-2), plan=plan))
    bank_pilot = sum((s["nodes"]*(s["plan"]["pilot_incompleteness_bound"]+
                       s["plan"]["iid_bad_bank_bound"]) for s in stages), Fraction(0))
    failure = sum((s["nodes"]*s["plan"]["episode_abort_bound"] for s in stages), Fraction(0))
    if bank_pilot > Fraction(1, 64) or failure > Fraction(1, 16):
        raise ArithmeticError("constant whole-tree failure envelope failed")
    return dict(status="CONDITIONAL_MIXED_ORDER_SOURCE_TREE_NOT_HSP_BOUND",
                raw_arity_per_grade=width, leaves_per_output_tree=leaves,
                failure_bits_per_node=bits, stages=stages,
                bank_and_pilot_failure_bound=bank_pilot, tree_abort_bound=failure,
                classical_kernel_trial_cap=sum(s["nodes"]*s["plan"]["kernel_trial_cap"] for s in stages),
                discarded_pilots_charged=True, pointwise_source_composition_required=True,
                original_oracle_queries_included=False,
                quantum_receiver_implemented=False, all_prime_ring_hsp_bound=False,
                complete_quantum_error_accounting_included=False,
                class_bounded_by_derived_cyclic_rank=False, novelty_established=False)


def report():
    """Seeded mixed-order arithmetic fixtures plus a separate resource tree."""
    cases = []
    for name, p, es, generators, orders, degree, u, seed in (
        ("ambient_mod_p_zero", 101, (3,), [(101,)], (101**2,), 2, 2, 5101),
        ("oblique_mixed_order", 257, (2, 3), [(257, 257), (0, 257**2)], (257**2, 257), 2, 3, 5257),
    ):
        labels = random.Random(seed)
        def draw(count):
            out = []
            for _ in range(count):
                coefficients = [labels.randrange(order) for order in orders]
                out.append(tuple(sum(a*g[j] for a, g in zip(coefficients, generators)) % p**e
                                 for j, e in enumerate(es)))
            return out
        value = unit_pilot_episode(prime=p, ambient_exponents=es, degree=degree,
                                   uniform_parameter=u, draw_labels=draw, attempt_cap=32768,
                                   failure_bits=20, bit_source=random.Random(seed+1))
        cases.append(dict(name=name, fixture_generators=generators, fixture_orders=orders,
                          source_seed=seed, arithmetic_seed=seed+1, result=value))
    root = Path(__file__).resolve().parents[1]
    sources = ("theorems/unit_power_module.py", "theorems/random_column_power_sde.py",
               "theorems/pilot_submodule.py", "theorems/prime_power_rees_descent.py",
               "theorems/bounded_power_roots.py", "theorems/power_sde_budget.py",
               "research/UNIT_POWER_MODULE_CANCELLATION.md")
    return dict(status="BOUNDED_CLASSICAL_UNIT_MODULE_CONTROLS_NOT_QUANTUM_RECEIVER",
                cases=cases, source_sha256={p: sha256((root/p).read_bytes()).hexdigest() for p in sources},
                tree=unit_tree_source_bound(prime=1009, class_bound=3, cyclic_rank_bound=2, uniform_parameter=3),
                quantum_receiver_implemented=False, iid_source_certified=False,
                all_prime_ring_hsp_bound=False, speedup_claim_allowed=False,
                candidate_promotion=False, proof_promotion=False)
