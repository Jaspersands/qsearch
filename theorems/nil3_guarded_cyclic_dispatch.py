"""Standalone guarded trivial/normal/transverse/abelian cyclic-H dispatcher.

Implements the five-step cyclic promise handler and fixed-batch sample bounds
described in research/NIL3_NORMAL_WORD_BRIDGE.md and
research/CLASS_THREE_HSP_THEOREM_DRAFT.md, starting from actual normal-word
coset states and public collector presentations. Also supplies arbitrary-prime
fmpz_mod_mat row compression and a capped conic square-weight solver with an
exact failure bound.

This module does NOT execute the outer ISS normalizer recursion, black-box
presentation acquisition, a general-prime SDE backend, or a compiled gate
circuit, and makes no speedup or novelty claim.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations
import json
from math import sqrt
from pathlib import Path
import random

from flint import fmpz_mod_ctx, fmpz_mod_mat
import numpy as np

from theorems.affine_phase_erasure import (
    copy_budget, initial_packet, leading_columns, sample_merge,
)
from theorems.folded_rs_decoder import affine_solution
from theorems.graded_hsp_phase_descent import _canonical, _dependence
from theorems.nil3_cocycle_receiver import (
    ClassThreeBCH, learn_normal_generator, partial_fourier_branch, sample_fourier,
)
from theorems.nil3_complete_budget import rank_failure, rank_sample_count
from theorems.nil3_normal_word_bridge import NormalWordLieBridge, matvec
from theorems.prime_character_opi import ring

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/nil3_guarded_cyclic_dispatch.json"


def independent_columns_exact(columns, p):
    """Arbitrary-precision equation-row compression preserving all input columns."""
    ring(p)
    if not columns or not columns[0]:
        raise ValueError("nonempty coefficient columns required")
    width = len(columns[0])
    for column in columns:
        _canonical(column, width, p)
    reduced, rank = fmpz_mod_mat(
        list(map(list, zip(*columns))), fmpz_mod_ctx(p)
    ).rref()
    if rank == 0:
        return [[0] for _ in columns], 0
    return [
        [int(reduced[j, i]) for j in range(rank)] for i in range(len(columns))
    ], int(rank)


def conic_failure_bound(p, attempts):
    """Exact probability that `attempts` uniform x in F_p fail -1-x^2 in (F_p^*)^2."""
    ring(p)
    if p % 4 != 3:
        raise ValueError("conic failure bound requires p=3 mod 4")
    if type(attempts) is not int or attempts < 1:
        raise ValueError("positive integer conic attempt cap required")
    # For p=3 mod 4, exactly (p+1)/2 values of x in F_p make -1-x^2 a nonzero square.
    return Fraction(p - 1, 2 * p) ** attempts


def square_weights_capped(p, columns, rng, *, conic_attempt_cap=128):
    """Arbitrary-precision p=3 mod 4 square solver with a proved conic failure cap."""
    ring(p)
    if p % 4 != 3:
        raise ValueError("square controller currently requires p=3 mod 4")
    if type(conic_attempt_cap) is not int or conic_attempt_cap < 1:
        raise ValueError("positive integer conic_attempt_cap required")
    compressed, rank = independent_columns_exact(columns, p)
    size = (rank + 1) ** 2
    if len(compressed) < size:
        raise ValueError(f"square controller needs {size} columns at rank {rank}")
    if rank == 0:
        return [1] + [0] * (len(compressed) - 1)

    def split(vectors):
        relation = _dependence(p, vectors)
        plus, minus = {}, {}
        for i, a in enumerate(relation):
            if a:
                target = plus if pow(a, (p - 1) // 2, p) == 1 else minus
                value = a if target is plus else -a % p
                target[i] = pow(value, (p + 1) // 4, p)
        value = [
            sum(vectors[i][j] * b * b for i, b in plus.items()) % p
            for j in range(rank)
        ]
        return plus, minus, value

    inner, values = [], []
    for start in range(0, size, rank + 1):
        plus, minus, value = split(compressed[start:start + rank + 1])
        blocks = (
            {start + i: b for i, b in plus.items()},
            {start + i: b for i, b in minus.items()},
        )
        if not any(value):
            selected = blocks[0] or blocks[1]
            return [selected.get(i, 0) for i in range(len(compressed))]
        inner.append(blocks)
        values.append(value)
    plus, minus, value = split(values)
    four = []
    for outer in (plus, minus):
        for side in (0, 1):
            four.append({
                i: b * scale % p
                for block, scale in outer.items()
                for i, b in inner[block][side].items()
            })
    if not any(value):
        selected = next(block for block in four if block)
        return [selected.get(i, 0) for i in range(len(compressed))]

    scales = None
    for _ in range(conic_attempt_cap):
        x = rng.randrange(p)
        y2 = (-1 - x * x) % p
        if pow(y2, (p - 1) // 2, p) == 1:
            scales = (x, pow(y2, (p + 1) // 4, p), 1, 0)
            break
    if scales is None:
        raise RuntimeError("bounded conic sampler exhausted")
    result = [0] * len(compressed)
    for block, scale in zip(four, scales):
        for i, b in block.items():
            result[i] = b * scale % p
    return result


def cancellation_weights_exact(packets, degree, rng=None, *, conic_attempt_cap=128):
    """Choose scales from public coefficient maps using arbitrary-precision RREF."""
    if degree not in (1, 2, 3):
        raise ValueError("implemented degrees are 1, 2, 3")
    p = packets[0].p
    columns = leading_columns(packets, degree)
    compressed, rank = independent_columns_exact(columns, p)
    if not rank:
        weights = [1] + [0] * (len(packets) - 1)
    elif degree == 2:
        weights = square_weights_capped(
            p, compressed, rng or random.Random(0), conic_attempt_cap=conic_attempt_cap
        )
    else:
        coefficients = _dependence(p, compressed)
        if degree == 3:
            if p % 3 != 2:
                raise ValueError("cubic controller currently requires p=2 mod3")
            coefficients = [pow(c, pow(3, -1, p - 1), p) for c in coefficients]
        weights = coefficients
    if not any(weights) or any(
        sum(column[j] * pow(c, degree, p) for column, c in zip(columns, weights)) % p
        for j in range(len(columns[0]))
    ):
        raise ArithmeticError("public leading-degree cancellation failed")
    return weights, rank


def adapted_presentation_exact(bridge: NormalWordLieBridge):
    """Arbitrary-precision adapted presentation; returns None if bridge is abelian."""
    p, d = bridge.p, bridge.dimension
    ctx = fmpz_mod_ctx(p)
    brackets = {
        (i, j): bridge.coordinates(
            bridge.lie_bracket(bridge.generators[i], bridge.generators[j])
        )
        for i, j in combinations(range(d), 2)
    }
    values = [row for row in brackets.values() if any(row)]
    if not values:
        return None
    reduced, n = fmpz_mod_mat(values, ctx).rref()
    n = int(n)
    derived = [tuple(int(reduced[i, j]) for j in range(d)) for i in range(n)]
    spanning, complement = list(derived), []
    for e in bridge.generators:
        if int(fmpz_mod_mat(spanning + [e], ctx).rref()[1]) > len(spanning):
            spanning.append(e)
            complement.append(e)
    if len(spanning) != d:
        raise ArithmeticError("failed to construct a full public Lie basis")
    basis = complement + derived
    forward = [list(row) for row in zip(*basis)]
    augmented = [row + list(e) for row, e in zip(forward, bridge.generators)]
    inverse_rref, rank = fmpz_mod_mat(augmented, ctx).rref()
    if int(rank) != d:
        raise ArithmeticError("public basis matrix is singular")
    inverse = [[int(inverse_rref[i, d + j]) for j in range(d)] for i in range(d)]

    def old_bracket(a, b):
        return tuple(
            sum((a[i] * b[j] - a[j] * b[i]) * value[k] for (i, j), value in brackets.items()) % p
            for k in range(d)
        )

    new_brackets = {
        (i, j): matvec(inverse, old_bracket(basis[i], basis[j]), p)
        for i, j in combinations(range(d), 2)
    }
    group = ClassThreeBCH(
        p,
        len(complement),
        n,
        {key: value for key, value in new_brackets.items() if any(value)},
    )
    return group, forward, inverse


def normal_word_coset_fixture(bridge: NormalWordLieBridge, generator_word, representative_word):
    """Fixture-only coset state in normal-word coordinates; supports trivial H."""
    p = bridge.p
    representative = bridge.canonical(representative_word)
    generator = bridge.canonical(generator_word)
    subgroup = {bridge.power(generator, t) for t in range(p)}
    if len(subgroup) not in (1, p):
        raise ValueError("fixture requires a trivial or order-p subgroup")
    scale = complex(1 / sqrt(len(subgroup)))
    return {bridge.multiply(representative, h): scale for h in subgroup}


def sample_normal_intersection_frequency(group: ClassThreeBCH, adapted_state, rng):
    """Step 1: measure q on an adapted coset state, apply Phi(-q), and QFT on N."""
    branches = {}
    for logarithm, amplitude in adapted_state.items():
        q, normal = group.to_chart(logarithm)
        twisted = group.action(group.scale(-1, q), normal)
        branch = branches.setdefault(q, {})
        branch[twisted] = branch.get(twisted, 0j) + amplitude
    q_keys = list(branches.keys())
    weights = [sum(abs(a) ** 2 for a in branches[q].values()) for q in q_keys]
    chosen_q = rng.choices(q_keys, weights=weights, k=1)[0]
    chosen_branch = branches[chosen_q]
    norm = sqrt(sum(abs(a) ** 2 for a in chosen_branch.values()))
    normalized_normal_state = {k: v / norm for k, v in chosen_branch.items()}
    return sample_fourier(group.p, normalized_normal_state, rng), len(normalized_normal_state)


def guarded_cyclic_dispatch(
    bridge: NormalWordLieBridge,
    source,
    *,
    error: Fraction = Fraction(1, 3),
    rng=None,
    normal_sample_override: int | None = None,
    quotient_sample_override: int | None = None,
    conic_attempt_cap: int = 128,
):
    """Five-step guarded cyclic-H dispatcher from actual normal-word coset states."""
    if not isinstance(error, Fraction) or not 0 < error <= Fraction(1, 2):
        raise ValueError("exact error Fraction in (0, 1/2] required")
    rng = rng if rng is not None else random.Random(0)
    eta = error / 8
    p, d = bridge.p, bridge.dimension
    setup_calls_before = bridge.collection_calls
    adapted = adapted_presentation_exact(bridge)
    public_setup_collection_calls = bridge.collection_calls - setup_calls_before

    # Case 0: Abelian ambient group G ([G,G] = 1)
    if adapted is None:
        t_abelian = (
            rank_sample_count(p, d, eta)
            if normal_sample_override is None
            else normal_sample_override
        )
        if type(t_abelian) is not int or t_abelian < 1:
            raise ValueError("positive abelian sample count required")
        frequencies = []
        for _ in range(t_abelian):
            raw_state = source()
            coord_state = {
                bridge.coordinates(word): amp for word, amp in raw_state.items()
            }
            frequencies.append(sample_fourier(p, coord_state, rng))
        solved = affine_solution(p, frequencies, [0] * len(frequencies), d)
        nullity = len(solved["basis"])
        if nullity > 1:
            return {
                "status": "INCOMPLETE_ABELIAN_RANK_FAILURE",
                "case": "INCOMPLETE_ABELIAN_RANK",
                "ambient_abelian": True,
                "source_copies": t_abelian,
                "normal_samples": t_abelian,
                "quotient_erasure_outputs": 0,
                "quotient_erasure_copies": 0,
                "hpgp_copies": 0,
                "public_setup_collection_calls": public_setup_collection_calls,
                "generators": None,
                "learned_subgroup": None,
            }
        if nullity == 0:
            return {
                "status": "SUCCESS",
                "case": "ABELIAN_TRIVIAL",
                "ambient_abelian": True,
                "source_copies": t_abelian,
                "normal_samples": t_abelian,
                "quotient_erasure_outputs": 0,
                "quotient_erasure_copies": 0,
                "hpgp_copies": 0,
                "public_setup_collection_calls": public_setup_collection_calls,
                "generators": [],
                "learned_subgroup": {bridge.zero},
            }
        gen_word = bridge.element(tuple(solved["basis"][0]))
        return {
            "status": "SUCCESS",
            "case": "ABELIAN_CYCLIC",
            "ambient_abelian": True,
            "source_copies": t_abelian,
            "normal_samples": t_abelian,
            "quotient_erasure_outputs": 0,
            "quotient_erasure_copies": 0,
            "hpgp_copies": 0,
            "public_setup_collection_calls": public_setup_collection_calls,
            "generators": [gen_word],
            "learned_subgroup": {bridge.power(gen_word, t) for t in range(p)},
        }

    group, forward, inverse = adapted
    m, n = group.m, group.n

    def adapted_source():
        raw_state = source()
        return {
            matvec(inverse, bridge.coordinates(word), p): amp
            for word, amp in raw_state.items()
        }

    def from_adapted_log(adapted_vec):
        return bridge.element(matvec(forward, adapted_vec, p))

    # Steps 1 & 2: Decide the normal case H <= N via fixed-batch twisted Fourier sampling
    t_normal = (
        rank_sample_count(p, n, eta)
        if normal_sample_override is None
        else normal_sample_override
    )
    if type(t_normal) is not int or t_normal < 1:
        raise ValueError("positive normal sample count required")
    normal_frequencies = []
    for _ in range(t_normal):
        freq, _ = sample_normal_intersection_frequency(group, adapted_source(), rng)
        normal_frequencies.append(freq)
    normal_sol = affine_solution(p, normal_frequencies, [0] * len(normal_frequencies), n)
    normal_nullity = len(normal_sol["basis"])
    if normal_nullity > 1:
        return {
            "status": "INCOMPLETE_NORMAL_RANK_FAILURE",
            "case": "INCOMPLETE_NORMAL_RANK",
            "ambient_abelian": False,
            "source_copies": t_normal,
            "normal_samples": t_normal,
            "normal_frequencies": normal_frequencies,
            "quotient_erasure_outputs": 0,
            "quotient_erasure_copies": 0,
            "hpgp_copies": 0,
            "public_setup_collection_calls": public_setup_collection_calls,
            "generators": None,
            "learned_subgroup": None,
        }
    if normal_nullity == 1:
        normal_vec = tuple(normal_sol["basis"][0])
        adapted_gen = group.from_chart((0,) * m, normal_vec)
        gen_word = from_adapted_log(adapted_gen)
        return {
            "status": "SUCCESS",
            "case": "NORMAL_CYCLIC",
            "ambient_abelian": False,
            "source_copies": t_normal,
            "normal_samples": t_normal,
            "normal_frequencies": normal_frequencies,
            "quotient_erasure_outputs": 0,
            "quotient_erasure_copies": 0,
            "hpgp_copies": 0,
            "public_setup_collection_calls": public_setup_collection_calls,
            "generators": [gen_word],
            "learned_subgroup": {bridge.power(gen_word, t) for t in range(p)},
        }

    # Steps 3 & 4: Phase erasure and fixed-batch quotient annihilator learning (permitting rank m)
    if p % 12 != 11:
        raise ValueError("implemented phase-erasure controller requires p=11 mod 12")
    t_quotient = (
        rank_sample_count(p, m, eta)
        if quotient_sample_override is None
        else quotient_sample_override
    )
    if type(t_quotient) is not int or t_quotient < 1:
        raise ValueError("positive quotient sample count required")
    budget = copy_budget(m, n)
    erasure_ledger = {
        "source_copies": 0,
        "zero_fourier_labels": 0,
        "merges": {"3": 0, "2": 0, "1": 0},
        "single_active_merges": {"3": 0, "2": 0, "1": 0},
        "max_equation_rank": {"3": 0, "2": 0, "1": 0},
        "fourier_samples": [],
        "max_final_phase_error": 0.0,
    }

    def produce(degree):
        if degree == 4:
            original = adapted_source()
            label = tuple(rng.randrange(p) for _ in range(n))
            state, probability = partial_fourier_branch(group, original, label)
            if len(state) not in (1, p) or abs(probability * (p ** n) - 1.0) > 1e-9:
                raise ValueError("trivial-or-cyclic quotient source promise failed")
            erasure_ledger["source_copies"] += 1
            erasure_ledger["zero_fourier_labels"] += int(not any(label))
            return state, initial_packet(p, m, label)
        inputs = [produce(degree + 1) for _ in range(budget[str(degree)])]
        states, packets = map(list, zip(*inputs))
        weights, rank = cancellation_weights_exact(
            packets, degree, rng, conic_attempt_cap=conic_attempt_cap
        )
        result, packet, _, _ = sample_merge(p, states, packets, weights, rng)
        if packet.degree >= degree or len(result) not in (1, p):
            raise ArithmeticError("phase-erasure degree/support invariant failed")
        key = str(degree)
        erasure_ledger["merges"][key] += 1
        erasure_ledger["single_active_merges"][key] += int(
            sum(bool(c) for c in weights) == 1
        )
        erasure_ledger["max_equation_rank"][key] = max(
            erasure_ledger["max_equation_rank"][key], rank
        )
        return result, packet

    for _ in range(t_quotient):
        state, _ = produce(1)
        anchor = next(iter(state.values()))
        erasure_ledger["max_final_phase_error"] = max(
            erasure_ledger["max_final_phase_error"],
            max(abs(a / anchor - 1) for a in state.values()),
        )
        frequency = sample_fourier(p, state, rng)
        erasure_ledger["fourier_samples"].append(frequency)

    quot_sol = affine_solution(
        p,
        erasure_ledger["fourier_samples"],
        [0] * len(erasure_ledger["fourier_samples"]),
        m,
    )
    quot_nullity = len(quot_sol["basis"])
    if quot_nullity > 1:
        return {
            "status": "INCOMPLETE_QUOTIENT_RANK_FAILURE",
            "case": "INCOMPLETE_QUOTIENT_RANK",
            "ambient_abelian": False,
            "source_copies": t_normal + erasure_ledger["source_copies"],
            "normal_samples": t_normal,
            "quotient_erasure_outputs": t_quotient,
            "quotient_erasure_copies": erasure_ledger["source_copies"],
            "quotient_erasure": erasure_ledger,
            "hpgp_copies": 0,
            "public_setup_collection_calls": public_setup_collection_calls,
            "generators": None,
            "learned_subgroup": None,
        }
    if quot_nullity == 0:
        return {
            "status": "SUCCESS",
            "case": "TRIVIAL",
            "ambient_abelian": False,
            "source_copies": t_normal + erasure_ledger["source_copies"],
            "normal_samples": t_normal,
            "quotient_erasure_outputs": t_quotient,
            "quotient_erasure_copies": erasure_ledger["source_copies"],
            "quotient_erasure": erasure_ledger,
            "hpgp_copies": 0,
            "public_setup_collection_calls": public_setup_collection_calls,
            "generators": [],
            "learned_subgroup": {bridge.zero},
        }

    # Step 5: Complete the nonzero transverse line via known quadratic HPGP
    direction = tuple(quot_sol["basis"][0])
    normal_coord, hpgp_ledger = learn_normal_generator(
        group, adapted_source, direction, rng
    )
    adapted_gen = group.from_chart(direction, normal_coord)
    gen_word = from_adapted_log(adapted_gen)
    total_copies = (
        t_normal + erasure_ledger["source_copies"] + hpgp_ledger["source_copies"]
    )
    return {
        "status": "SUCCESS",
        "case": "TRANSVERSE_CYCLIC",
        "ambient_abelian": False,
        "source_copies": total_copies,
        "normal_samples": t_normal,
        "quotient_erasure_outputs": t_quotient,
        "quotient_erasure_copies": erasure_ledger["source_copies"],
        "quotient_erasure": erasure_ledger,
        "hpgp_copies": hpgp_ledger["source_copies"],
        "known_quadratic_hpgp": hpgp_ledger,
        "learned_adapted_direction": list(direction),
        "learned_adapted_normal_coordinate": list(normal_coord),
        "public_setup_collection_calls": public_setup_collection_calls,
        "generators": [gen_word],
        "learned_subgroup": {bridge.power(gen_word, t) for t in range(p)},
    }


def filiform_class_three_bridge(p=11):
    """Non-split class-three normal-word bridge X^a Z^c Y^b A^d with [X,Y]=Z, [X,Z]=A.

    Notice Z is placed in slot 1 (between X and Y) so the derived ideal <Z, A>
    is in slots (1, 3) and must be moved to the end by adapted_presentation_exact.
    """
    inv2 = pow(2, -1, p)

    def collect(left, right):
        # Normal word order: (a, c, b, d) representing X^a Y^b Z^c A^d
        a, c, b, d = left
        x, z, y, w = right
        return (
            (a + x) % p,
            (c + z - b * x) % p,
            (b + y) % p,
            (d + w - c * x + b * x * (x - 1) * inv2) % p,
        )

    return NormalWordLieBridge(p, 4, collect)


def abelian_bridge(p=11, dimension=3):
    return NormalWordLieBridge(
        p, dimension, lambda a, b: tuple((x + y) % p for x, y in zip(a, b))
    )


def controls(seed=20261021):
    p = 11
    bridge = filiform_class_three_bridge(p)
    cases_spec = [
        ("TRIVIAL", (0, 0, 0, 0)),
        ("NORMAL_CYCLIC", (0, 2, 0, 5)),
        ("TRANSVERSE_CYCLIC", (1, 3, 2, 4)),
    ]
    executed_cases = []
    for expected_case, gen_word in cases_spec:
        source_rng = random.Random(seed + len(executed_cases) * 10)
        dispatch_rng = random.Random(seed + len(executed_cases) * 10 + 1)
        oracle_calls = 0

        def source():
            nonlocal oracle_calls
            oracle_calls += 1
            rep = tuple(source_rng.randrange(p) for _ in range(bridge.dimension))
            return normal_word_coset_fixture(bridge, gen_word, rep)

        result = guarded_cyclic_dispatch(
            bridge, source, error=Fraction(1, 3), rng=dispatch_rng
        )
        true_subgroup = {bridge.power(gen_word, t) for t in range(p)}
        if (
            result["status"] != "SUCCESS"
            or result["case"] != expected_case
            or result["source_copies"] != oracle_calls
            or result["learned_subgroup"] != true_subgroup
        ):
            raise ArithmeticError(f"guarded cyclic dispatch failed on {expected_case}")
        executed_cases.append({
            "expected_case": expected_case,
            "dispatched_case": result["case"],
            "status": result["status"],
            "generator_fixture": list(gen_word),
            "returned_generators": [list(g) for g in result["generators"]],
            "recovered_exact_subgroup": result["learned_subgroup"] == true_subgroup,
            "oracle_calls_consumed": oracle_calls,
            "normal_samples": result["normal_samples"],
            "quotient_erasure_outputs": result["quotient_erasure_outputs"],
            "quotient_erasure_copies": result["quotient_erasure_copies"],
            "hpgp_copies": result["hpgp_copies"],
            "public_setup_collection_calls": result["public_setup_collection_calls"],
        })

    # Abelian ambient controls (trivial and cyclic)
    ab_bridge = abelian_bridge(p, 3)
    for expected_case, gen_word in [
        ("ABELIAN_TRIVIAL", (0, 0, 0)),
        ("ABELIAN_CYCLIC", (2, 5, 7)),
    ]:
        source_rng = random.Random(seed + 100 + len(executed_cases))
        dispatch_rng = random.Random(seed + 200 + len(executed_cases))
        oracle_calls = 0

        def ab_source():
            nonlocal oracle_calls
            oracle_calls += 1
            rep = tuple(source_rng.randrange(p) for _ in range(ab_bridge.dimension))
            return normal_word_coset_fixture(ab_bridge, gen_word, rep)

        result = guarded_cyclic_dispatch(
            ab_bridge, ab_source, error=Fraction(1, 3), rng=dispatch_rng
        )
        true_subgroup = {ab_bridge.power(gen_word, t) for t in range(p)}
        if (
            result["status"] != "SUCCESS"
            or result["case"] != expected_case
            or result["source_copies"] != oracle_calls
            or result["learned_subgroup"] != true_subgroup
        ):
            raise ArithmeticError(f"abelian dispatch failed on {expected_case}")
        executed_cases.append({
            "expected_case": expected_case,
            "dispatched_case": result["case"],
            "status": result["status"],
            "generator_fixture": list(gen_word),
            "returned_generators": [list(g) for g in result["generators"]],
            "recovered_exact_subgroup": result["learned_subgroup"] == true_subgroup,
            "oracle_calls_consumed": oracle_calls,
            "normal_samples": result["normal_samples"],
            "quotient_erasure_outputs": result["quotient_erasure_outputs"],
            "quotient_erasure_copies": result["quotient_erasure_copies"],
            "hpgp_copies": result["hpgp_copies"],
            "public_setup_collection_calls": result["public_setup_collection_calls"],
        })

    # Large-prime (p = 2^127 - 1) row-compression and capped conic square-solver control
    large_p = (1 << 127) - 1
    large_rng = random.Random(seed + 999)
    large_cols = [
        [large_rng.randrange(large_p) for _ in range(3)] for _ in range(16)
    ]
    large_weights = square_weights_capped(
        large_p, large_cols, large_rng, conic_attempt_cap=128
    )
    large_verified = any(large_weights) and all(
        sum(col[j] * w * w for col, w in zip(large_cols, large_weights)) % large_p == 0
        for j in range(3)
    )
    if not large_verified:
        raise ArithmeticError("127-bit prime square_weights_capped verification failed")

    return {
        "id": "NIL3-GUARDED-CYCLIC-DISPATCH",
        "status": "standalone-guarded-cyclic-dispatch-executed-review-pending",
        "prime": p,
        "cases_executed": executed_cases,
        "large_prime_127bit_backend_control": {
            "prime_bits": large_p.bit_length(),
            "rank_tested": independent_columns_exact(large_cols, large_p)[1],
            "conic_attempt_cap": 128,
            "conic_failure_exact_16_trials": str(conic_failure_bound(large_p, 16)),
            "conic_failure_dyadic_upper_bound": str(Fraction(1, 1 << 128)),
            "square_relation_verified": large_verified,
        },
        "stops_at_m_minus_one_on_trivial_H": False,
        "full_rank_m_permitted_for_trivial_H": True,
        "incomplete_rank_recorded_as_failure": True,
        "ideal_learned_direction_injected": False,
        "iss_outer_normalizer_recursion_executed": False,
        "black_box_presentation_acquisition_executed": False,
        "general_prime_sde_backend_executed": False,
        "full_nil3_hsp_claim_admitted": False,
        "novelty_established": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = controls()
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
