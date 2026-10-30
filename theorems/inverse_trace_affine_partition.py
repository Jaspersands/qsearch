"""Exact trace-affine subinstance reductions and deterministic balancing.

Disjoint block witnesses retain all original K checks. Omitted coordinates
can be set to zero only at original zero-targets. The genus-zero acceptance
bound is often inconclusive after restriction, even when finite runs succeed.
The separate short-sum bound covers balanced native inputs at odd n>=61.
"""
from copy import deepcopy
from fractions import Fraction
import hashlib
import json

from theorems.balanced_codeword_filter import integer, trace_mask
from theorems.cubic_rs_affine_flats import solve_binary
from theorems.explicit_quadratic_opi import element
from theorems.inverse_trace_genus_zero import run_experiment
from theorems.inverse_trace_short_sums import short_sum_certificate
from theorems.inverse_trace_smt import validate_instance, verify_word


def balanced_trace_partition(instance):
    """Deterministic conditional expectation, O(nN) buckets, no field scan."""
    bits, points, targets, _ = validate_instance(instance)
    signs = [1-2*b for b in targets]
    total = sum(signs)

    def mean_square(prefix, fixed):
        remaining = 1 << (bits-fixed)
        excluded = int(prefix == 0)
        if remaining == excluded:
            return None
        buckets = {}
        for a, sign in zip(points, signs, strict=True):
            label = a >> fixed
            buckets[label] = buckets.get(label, 0)+sign*(1-2*((a & prefix).bit_count() % 2))
        numerator = remaining*sum(value*value for value in buckets.values())-excluded*total*total
        return Fraction(numerator, remaining-excluded)

    prefix, bound, steps = 0, mean_square(0, 0), []
    for fixed in range(1, bits+1):
        choices = [(prefix | (bit << (fixed-1))) for bit in (0, 1)]
        scored = [(score, value) for value in choices
                  if (score := mean_square(value, fixed)) is not None]
        score, prefix = min(scored)
        if score > bound:
            raise ArithmeticError("conditional expectation increased")
        steps.append({"fixed_bits": fixed, "functional_prefix": prefix,
                      "mean_square": [score.numerator, score.denominator]})
        bound = score
    if not prefix:
        raise ArithmeticError("zero functional was not excluded")
    equations = [(trace_mask(bits, 1 << j), (prefix >> j) & 1) for j in range(bits)]
    system = solve_binary(equations, bits)
    if not system["consistent"] or system["rank"] != bits:
        raise ArithmeticError("trace pairing failed")
    c = system["solution"]
    blocks = trace_partition(instance, c, 0)
    imbalance = len(blocks[0]["indices"])-len(blocks[1]["indices"])
    initial = Fraction((1 << bits)*len(points)-total*total, (1 << bits)-1)
    if imbalance*imbalance != bound or bound > initial:
        raise ArithmeticError("balanced partition certificate failed")
    return {"c": c, "d0": 0, "coordinate_functional": prefix,
            "imbalance": imbalance, "initial_mean_square": [initial.numerator, initial.denominator],
            "steps": steps, "blocks": blocks, "field_table_enumerated": False}


def trace_partition(instance, c, d0=0):
    bits, points, targets, _ = validate_instance(instance)
    integer(c, 1, (1 << bits)-1, "nonzero trace slope")
    integer(d0, 0, (1 << bits)-1, "trace offset")
    trace_one = next(1 << j for j in range(bits) if element(bits, 1 << j).trace() == 1)
    slope, offset = element(bits, c), element(bits, d0)
    indices = [[], []]
    for i, (point, target) in enumerate(zip(points, targets, strict=True)):
        mismatch = int((slope*element(bits, point)+offset).trace()) ^ target
        indices[mismatch].append(i)
    return [{"indices": indices[side], "c": c, "d0": d0 ^ (trace_one if side else 0)}
            for side in range(2)]


def _subinstance(instance, indices):
    result = deepcopy(instance)
    result["points"] = [instance["points"][i] for i in indices]
    result["targets"] = [instance["targets"][i] for i in indices]
    return result


def _block_run(instance, block, seed, allocation_seed, max_trials):
    indices = block["indices"]
    if not any(instance["targets"][i] for i in indices):
        return {"status": "VERIFIED_ZERO_BLOCK", "witness": [0]*len(indices),
                "trials": [], "reason": "all_block_targets_are_zero"}
    if len(indices) <= instance["checks"]:
        return {"status": "PARTITION_BLOCK_HAS_FULL_COLUMN_RANK", "witness": None,
                "trials": [], "reason": "only_zero_in_this_block_kernel_but_one_target_present"}
    return run_experiment(_subinstance(instance, indices), block["c"], block["d0"],
                          seed=seed, allocation_seed=allocation_seed, max_trials=max_trials)


def _result(instance, method):
    return {"method": method, "original_instance": deepcopy(instance),
            "original_instance_sha256": hashlib.sha256(json.dumps(instance, sort_keys=True).encode()).hexdigest(),
            "status": "UNKNOWN_PARTITION_TRIAL_LIMIT", "witness": None,
            "full_original_word_verified": False, "hardness_evidence": False,
            "unrestricted_target_solver_established": False, "uniform_sampler": False,
            "generic_partition_success_bound_established": False}


def run_zero_extended_experiment(instance, c, d0=0, *, seed=1032,
                                 allocation_seed=1033, max_trials=32):
    """Keep all one-targets; never silently drop an inconvenient constraint."""
    validate_instance(instance)
    for value, name in ((seed, "seed"), (allocation_seed, "allocation seed")):
        integer(value, 0, 2**32-1, name)
    integer(max_trials, 0, 10000, "per-block trial cap")
    block, omitted = trace_partition(instance, c, d0)
    if any(instance["targets"][i] for i in omitted["indices"]):
        raise ValueError("zero extension would omit an original one-target")
    result = _result(instance, "zero_extended_trace_affine_subinstance")
    run = _block_run(instance, block, seed, allocation_seed, max_trials)
    result.update(selected_indices=block["indices"], c=c, d0=d0, block_run=run)
    if run["witness"] is not None:
        word = [0]*len(instance["points"])
        for i, x in zip(block["indices"], run["witness"], strict=True):
            word[i] = x
        if not verify_word(instance, word):
            raise ArithmeticError("zero-extended result failed original-instance verification")
        result.update(status="VERIFIED_NATIVE_WITNESS", witness=word, full_original_word_verified=True)
    return result


def run_partitioned_experiment(instance, c, d0=0, *, seeds=(1034, 1036),
                               allocation_seeds=(1035, 1037), max_trials=32):
    """Solve the two disjoint blocks, or return UNKNOWN with paid failures."""
    validate_instance(instance)
    if len(seeds) != 2 or len(allocation_seeds) != 2:
        raise ValueError("two polynomial and two allocation seeds required")
    for value in tuple(seeds)+tuple(allocation_seeds):
        integer(value, 0, 2**32-1, "block seed")
    integer(max_trials, 0, 10000, "per-block trial cap")
    blocks = trace_partition(instance, c, d0)
    result = _result(instance, "two_disjoint_trace_affine_subinstances")
    result.update(c=c, d0=d0, max_trials_per_block=max_trials, blocks=[])
    word, all_succeeded = [0]*len(instance["points"]), True
    for index, block in enumerate(blocks):
        run = _block_run(instance, block, seeds[index], allocation_seeds[index], max_trials)
        result["blocks"].append({**block, "run": run})
        if run["witness"] is None:
            all_succeeded = False
            continue
        for i, x in zip(block["indices"], run["witness"], strict=True):
            word[i] = x
    if all_succeeded:
        if not verify_word(instance, word):
            raise ArithmeticError("disjoint-block result failed original-instance verification")
        result.update(status="VERIFIED_NATIVE_WITNESS", witness=word, full_original_word_verified=True)
    return result


def run_balanced_experiment(instance, *, seeds=(1034, 1036),
                            allocation_seeds=(1035, 1037), max_trials=32):
    """A capped seeded control of the proven IID algorithm, not its proof."""
    bits, points, targets, checks = validate_instance(instance)
    balance = balanced_trace_partition(instance)
    certificates = []
    for block in balance["blocks"]:
        indices = block["indices"]
        zeros = sum(targets[i] == 0 for i in indices)
        if zeros == len(indices):
            certificate = {"status": "TRIVIAL_ZERO_BLOCK", "expected_iid_trials_upper": 0}
        elif len(indices) <= checks:
            certificate = {"status": "OUTSIDE_CERTIFICATE_SCOPE"}
        else:
            certificate = short_sum_certificate(bits, len(indices), checks, zeros)
        certificates.append(certificate)
    certified = all(c["status"] in ("TRIVIAL_ZERO_BLOCK", "CERTIFIED_IID_SHORT_SUM_TRIAL_BOUND")
                    for c in certificates)
    native_scope = (bits % 2 == 1 and bits >= 61 and len(points) == bits*bits
                    and checks == bits*bits//8)
    if native_scope and not certified:
        raise ArithmeticError("balanced native theorem did not produce its expected certificate")
    result = run_partitioned_experiment(instance, balance["c"], balance["d0"],
                                       seeds=seeds, allocation_seeds=allocation_seeds,
                                       max_trials=max_trials)
    result.update(balance=balance, short_sum_certificates=certificates,
                  iid_partition_bound_established=certified,
                  native_family_expected_polynomial_search_theorem_applies=native_scope,
                  unrestricted_target_solver_established=native_scope,
                  generic_partition_success_bound_established=native_scope,
                  seeded_experiment_is_iid_proof=False)
    if certified:
        result["expected_total_iid_proposals_upper"] = sum(
            c["expected_iid_trials_upper"] for c in certificates)
    return result
