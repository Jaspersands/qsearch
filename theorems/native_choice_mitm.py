"""Costed three-choice vector-sum engine over actual ternary residue rings.

This is a classical search primitive, not a quantum candidate generator or
an assertion that arbitrary input choices obey a native source distribution.
"""
from itertools import product

from flint import fmpq

from native_affine_fibre_relaxation import canonical_vector
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import integer


def solve_choices(choices, target, modulus, max_evaluations=100000, max_entries=100000):
    root_digits(modulus)
    integer(max_evaluations, "positive whole-search evaluation cap", 1)
    integer(max_entries, "positive left memory cap", 1)
    target = tuple(target)
    integer(len(target), "positive vector-sum dimension", 1)
    target = canonical_vector(target, len(target), modulus)
    choices = tuple(tuple(canonical_vector(v, len(target), modulus) for v in column) for column in choices)
    if any(len(column) != 3 or any(column[0]) for column in choices):
        raise ValueError("three canonical choices with a zero first choice required per parameter")
    t, n, left = len(choices), len(target), len(choices)//2
    lc, rc = 3**left, 3**(t-left)
    ledger = {"left_assignment_bound": str(fmpq(lc)), "right_assignment_bound": str(fmpq(rc)),
              "whole_search_assignment_bound": str(fmpq(lc+rc)), "left_memory_entry_bound": str(fmpq(lc)),
              "max_evaluations": max_evaluations, "max_entries": max_entries,
              "group_modulus": str(fmpq(modulus)), "group_dimension": n, "parameters": t,
              "residue_bits": modulus.bit_length(),
              "left_payload_bits_upper": str(fmpq(lc*(n*modulus.bit_length()+2*left))),
              "payload_bound_includes_runtime_object_overhead": False,
              "per_assignment_modular_additions_upper": n*max(left, t-left),
              "search_is_exponential_in_slice_parameters": True, "uniform_solution_sampler": False,
              "source_values_mask_secret_or_errors_used": False}
    if lc+rc > max_evaluations or lc > max_entries:
        return {"status": "SEARCH_CAP_EXCEEDED_NOT_NO_SOLUTION", "parameters": None, "cost": ledger,
                "assignments_evaluated": 0, "stored_entries": 0}
    def contribution(digits, offset):
        return tuple(sum(choices[offset+j][z][i] for j, z in enumerate(digits)) % modulus for i in range(n))
    table, count = {}, 0
    for digits in product(range(3), repeat=left):
        table.setdefault(contribution(digits, 0), digits);count += 1
    for digits in product(range(3), repeat=t-left):
        other = contribution(digits, left)
        needed = tuple((a-b) % modulus for a, b in zip(target, other));count += 1
        if needed in table:
            parameters = table[needed]+digits
            if contribution(parameters, 0) != target: raise ArithmeticError("MITM collision missed the exact ring target")
            return {"status": "VERIFIED_THREE_CHOICE_RING_SOLUTION", "parameters": parameters,
                    "cost": ledger, "assignments_evaluated": count, "stored_entries": len(table)}
    return {"status": "COMPLETE_CHOICE_SEARCH_NO_SOLUTION", "parameters": None,
            "cost": ledger, "assignments_evaluated": count, "stored_entries": len(table)}
