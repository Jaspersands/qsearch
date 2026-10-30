"""Explicit-ring controls separating p-torsion, quotient, and original class."""
from itertools import product
from math import prod

import pytest

from theorems.lie_torsion_reduction import compile_p_torsion
from theorems.pilot_submodule import verify_pilot_frame


def test_live_report_preserves_rank_reduction_and_readout_scope():
    from hashlib import sha256
    from pathlib import Path
    from theorems.lie_torsion_reduction import report
    row = report()
    cases = {case["name"]: case for case in row["torsion_controls"]}
    large = cases["rank_one_class_128"]
    assert large["original_class"] == 128 and large["derived_cyclic_rank"] == 1
    assert large["torsion_class"] == 1 and large["section_field_class_upper"] == 2
    assert large["local_solver_call_cap"] == 256*257//2
    assert large["proposed_core"] == "PUBLISHED_NIL2"
    assert cases["small_prime_field_class_three"]["proposed_core"] == "PUBLISHED_SMALL_COMMUTATOR"
    assert cases["field_class_three"]["proposed_core"] == "CONDITIONAL_FIELD_REES"
    assert cases["heisenberg_prime_squared"]["torsion_class"] == 1
    assert cases["heisenberg_quotient_mod_p"]["torsion_class"] == 2
    orders = {case["name"]: case["result"]["subgroup_order"] for case in row["readout_controls"]}
    assert orders["incomplete_fourier_span"] == 9
    assert orders["complete_supplied_span_control"] == 3
    assert all(not case["result"]["hidden_subgroup_recovery_certified"]
               for case in row["readout_controls"])
    assert not row["full_outer_reduction_implemented"]
    assert not row["field_core_newly_proved"] and not row["speedup_claim_allowed"]
    root = Path(__file__).resolve().parents[1]
    for path, digest in row["source_sha256"].items():
        assert sha256((root/path).read_bytes()).hexdigest() == digest


def tensor_from_brackets(prime, exponents, brackets):
    n = len(exponents)
    tensor = [[[0] * n for _ in range(n)] for _ in range(n)]
    for (i, j), column in brackets.items():
        assert i < j
        for k, value in enumerate(column):
            tensor[i][j][k] = value % prime**exponents[k]
            tensor[j][i][k] = -value % prime**exponents[k]
    return tuple(tuple(tuple(row) for row in plane) for plane in tensor)


def bracket(x, y, tensor, moduli):
    return tuple(sum(x[i] * y[j] * tensor[i][j][k]
                     for i in range(len(x)) for j in range(len(y))) % modulus
                 for k, modulus in enumerate(moduli))


def additive_span(columns, moduli):
    found = {(0,) * len(moduli)}
    pending = list(found)
    while pending:
        x = pending.pop()
        for column in columns:
            y = tuple((a + b) % m for a, b, m in zip(x, column, moduli))
            if y not in found:
                found.add(y)
                pending.append(y)
    return found


def frame_span(frame):
    moduli = tuple(frame.prime**e for e in frame.ambient_exponents)
    columns = tuple(zip(*frame.lattice_basis))
    return additive_span(columns, moduli)


def direct_lower_central(tensor, moduli):
    n = len(moduli)
    units = [tuple(int(i == j) for i in range(n)) for j in range(n)]
    current = set(product(*(range(m) for m in moduli)))
    series = [current]
    while current != {(0,) * n}:
        columns = {bracket(x, unit, tensor, moduli) for x in current for unit in units}
        next_term = additive_span(columns, moduli)
        assert next_term < current
        series.append(next_term)
        current = next_term
    return series


def embed(x, result):
    return tuple(sum(a * column[k] for a, column in zip(x, result.torsion_embedding))
                 % result.prime**exponent for k, exponent in enumerate(result.exponents))


def test_heisenberg_over_prime_squared_separates_torsion_and_quotient():
    p = 3
    exponents = (2, 2, 2)
    tensor = tensor_from_brackets(p, exponents, {(0, 1): (0, 0, 1)})
    result = compile_p_torsion(prime=p, exponents=exponents, structure_constants=tensor)
    assert result.original_lower_central_exponents == ((2, 2, 2), (2,), ())
    assert result.original_class == 2 and result.derived_rank == 1
    assert result.torsion_embedding == ((3, 0, 0), (0, 3, 0), (0, 0, 3))
    assert result.torsion_lower_central_dimensions == (3, 0)
    assert result.torsion_class == 1
    derived = frame_span(result.original_lower_central_frames[1])
    derived_torsion = {x for x in derived if all(p * a % 9 == 0 for a in x)}
    torsion_derived = {embed(x, result) for x in frame_span(result.torsion_lower_central_frames[1])}
    assert torsion_derived == {(0, 0, 0)} < derived_torsion
    assert (0, 0, 3) in derived_torsion

    quotient_tensor = tuple(tuple(tuple(value % p for value in row) for row in plane)
                            for plane in tensor)
    quotient = compile_p_torsion(prime=p, exponents=(1, 1, 1), structure_constants=quotient_tensor)
    assert quotient.original_class == quotient.torsion_class == 2
    assert quotient.derived_rank == 1
    assert quotient.field_structure_constants[0][1] == (0, 0, 1)
    assert result.field_structure_constants != quotient.field_structure_constants
    assert result.public_arithmetic_only is True
    assert result.original_hidden_subgroup_recovered is False
    assert result.full_outer_reduction_implemented is False


@pytest.mark.parametrize("p,exponent", [(3, 2), (5, 3), (7, 6)])
def test_metacyclic_ring_has_large_original_class_but_rank_one(p, exponent):
    exponents = (exponent, exponent)
    tensor = tensor_from_brackets(p, exponents, {(0, 1): (0, p)})
    result = compile_p_torsion(prime=p, exponents=exponents, structure_constants=tensor)
    assert result.original_lower_central_exponents == (
        (exponent, exponent), *((e,) for e in range(exponent - 1, 0, -1)), ()
    )
    assert result.original_class == exponent
    assert result.derived_rank == 1
    assert result.torsion_lower_central_dimensions == (2, 0)
    assert result.torsion_class == 1


def test_oblique_lower_central_generators_keep_their_full_coordinate_coupling():
    tensor = tensor_from_brackets(5, (4, 4), {(0, 1): (5, 5)})
    result = compile_p_torsion(prime=5, exponents=(4, 4), structure_constants=tensor)
    assert result.original_lower_central_exponents == ((4, 4), (3,), (2,), (1,), ())
    assert result.original_class == 4 and result.derived_rank == 1
    for index, frame in enumerate(result.original_lower_central_frames[1:], start=1):
        expected = {(5**index * a, 5**index * a) for a in range(5**(4 - index))}
        assert frame_span(frame) == expected
    assert result.torsion_class == 1


def test_exponent_128_uses_bounded_module_spans_not_enumeration(monkeypatch):
    import builtins
    import theorems.lie_torsion_reduction as module
    original_range = builtins.range
    original_compile = module.compile_pilot_frame
    calls = []

    def bounded_range(*args):
        interval = original_range(*args)
        if interval and abs(interval.stop - interval.start) // abs(interval.step) > 10000:
            pytest.fail("attempted prime-power-sized enumeration")
        return interval

    def counted_compile(**kwargs):
        columns = kwargs["pilot_columns"]
        assert len(columns) <= 4
        calls.append(len(columns))
        return original_compile(**kwargs)

    monkeypatch.setattr(builtins, "range", bounded_range)
    monkeypatch.setattr(module, "compile_pilot_frame", counted_compile)
    tensor = tensor_from_brackets(131, (128, 128), {(0, 1): (0, 131)})
    result = compile_p_torsion(prime=131, exponents=(128, 128), structure_constants=tensor)
    assert result.original_class == 128
    assert result.derived_rank == 1
    assert result.original_lower_central_exponents[1] == (127,)
    assert result.original_lower_central_exponents[-2:] == ((1,), ())
    assert result.torsion_class == 1
    assert result.torsion_embedding == ((131**127, 0), (0, 131**127))
    assert len(calls) == 128 + 3


def test_coordinatewise_torsion_scales_retain_short_factors_and_bracket():
    tensor = tensor_from_brackets(3, (1, 1, 3), {(0, 1): (0, 0, 9)})
    result = compile_p_torsion(prime=3, exponents=(1, 1, 3), structure_constants=tensor)
    assert result.torsion_embedding == ((1, 0, 0), (0, 1, 0), (0, 0, 9))
    assert result.field_structure_constants[0][1] == (0, 0, 1)
    assert result.original_lower_central_exponents == ((1, 1, 3), (1,), ())
    assert result.torsion_lower_central_dimensions == (3, 1, 0)
    assert result.torsion_class == result.derived_rank + 1 == 2
    moduli = (3, 3, 27)
    field_elements = list(product(range(3), repeat=3))
    embedded = {embed(x, result) for x in field_elements}
    killed_by_p = {x for x in product(*(range(m) for m in moduli))
                   if all(3 * a % m == 0 for a, m in zip(x, moduli))}
    assert embedded == killed_by_p and len(embedded) == 3**3
    for x, y in product(field_elements, repeat=2):
        field_bracket = bracket(x, y, result.field_structure_constants, (3, 3, 3))
        assert embed(field_bracket, result) == bracket(embed(x, result), embed(y, result), tensor, moduli)


@pytest.mark.parametrize("exponents,central_coefficient", [((1, 1, 1), 1),
                                                           ((2, 2, 2), 1),
                                                           ((1, 1, 2), 3)])
def test_actual_lower_central_modules_match_independent_exhaustive_spans(exponents, central_coefficient):
    tensor = tensor_from_brackets(3, exponents, {(0, 1): (0, 0, central_coefficient)})
    result = compile_p_torsion(prime=3, exponents=exponents, structure_constants=tensor)
    for frames, coefficients, moduli in (
        (result.original_lower_central_frames, tensor, tuple(3**e for e in exponents)),
        (result.torsion_lower_central_frames, result.field_structure_constants, (3, 3, 3)),
    ):
        expected = direct_lower_central(coefficients, moduli)
        assert len(frames) == len(expected)
        for frame, subgroup in zip(frames, expected):
            assert verify_pilot_frame(frame)
            assert frame_span(frame) == subgroup
            assert prod(3**e for e in frame.intrinsic_exponents) == len(subgroup)


def test_intrinsic_derived_rank_is_not_coordinate_support_or_ambient_mod_p_rank():
    tensor = tensor_from_brackets(3, (2, 2, 2, 2), {(0, 1): (0, 0, 3, 3)})
    result = compile_p_torsion(prime=3, exponents=(2, 2, 2, 2), structure_constants=tensor)
    assert result.original_lower_central_exponents[1] == (1,)
    assert result.derived_rank == 1
    assert all(value % 3 == 0 for plane in tensor for row in plane for value in row)
    assert len(frame_span(result.original_lower_central_frames[1])) == 3


def test_field_filiform_example_attains_class_derived_rank_plus_one():
    tensor = tensor_from_brackets(5, (1, 1, 1, 1),
                                  {(0, 1): (0, 0, 1, 0), (0, 2): (0, 0, 0, 1)})
    result = compile_p_torsion(prime=5, exponents=(1, 1, 1, 1), structure_constants=tensor)
    assert result.original_class == result.torsion_class == 3
    assert result.derived_rank == 2
    assert result.torsion_lower_central_dimensions == (4, 2, 1, 0)
    assert result.torsion_class == result.derived_rank + 1
    assert result.field_structure_constants == tensor


def test_abelian_ring_has_rank_zero_and_class_one():
    tensor = tensor_from_brackets(3, (4, 1, 2), {})
    result = compile_p_torsion(prime=3, exponents=(4, 1, 2), structure_constants=tensor)
    assert result.original_lower_central_exponents == ((1, 2, 4), ())
    assert result.original_class == result.torsion_class == 1
    assert result.derived_rank == 0
    assert result.torsion_lower_central_dimensions == (3, 0)
    assert result.torsion_embedding == ((27, 0, 0), (0, 1, 0), (0, 0, 3))


def test_cyclic_abelian_boundary():
    result = compile_p_torsion(prime=3, exponents=(1,), structure_constants=(((0,),),))
    assert result.original_lower_central_exponents == ((1,), ())
    assert result.torsion_lower_central_dimensions == (1, 0)
    assert result.derived_rank == 0


def test_nonnilpotent_bracket_is_rejected_at_nonzero_stable_term(monkeypatch):
    import theorems.lie_torsion_reduction as module
    original_compile = module.compile_pilot_frame
    calls = []

    def counted_compile(**kwargs):
        calls.append(kwargs)
        return original_compile(**kwargs)

    monkeypatch.setattr(module, "compile_pilot_frame", counted_compile)
    tensor = tensor_from_brackets(3, (1, 1), {(0, 1): (0, 1)})
    with pytest.raises(ValueError, match="not nilpotent.*stabilizes"):
        compile_p_torsion(prime=3, exponents=(1, 1), structure_constants=tensor)
    assert len(calls) == 3


@pytest.mark.parametrize("exponent", [3, 4])
def test_nilpotency_class_at_least_prime_is_outside_lazard_scope(exponent):
    exponents = (exponent, exponent)
    tensor = tensor_from_brackets(3, exponents, {(0, 1): (0, 3)})
    with pytest.raises(ValueError, match="class < prime"):
        compile_p_torsion(prime=3, exponents=exponents, structure_constants=tensor)


@pytest.mark.parametrize("exponents,brackets", [
    ((1, 1, 1), {(0, 1): (1, 0, 0), (1, 2): (0, 1, 0), (0, 2): (0, 0, -1)}),
    ((2, 2, 2), {(0, 1): (0, 0, 1), (1, 2): (0, 3, 0)}),
])
def test_alternating_tensors_with_failed_jacobi_are_rejected_at_full_precision(exponents, brackets):
    tensor = tensor_from_brackets(3, exponents, brackets)
    with pytest.raises(ValueError, match="Jacobi"):
        compile_p_torsion(prime=3, exponents=exponents, structure_constants=tensor)


def test_both_input_orders_must_annihilate_each_bracket_coefficient():
    tensor = tensor_from_brackets(3, (1, 2), {(0, 1): (0, 1)})
    with pytest.raises(ValueError, match="order compatibility"):
        compile_p_torsion(prime=3, exponents=(1, 2), structure_constants=tensor)
    # This entry is compatible with its first input, but not its second.
    tensor = (((0, 0), (0, 0)), ((0, 1), (0, 0)))
    with pytest.raises(ValueError, match="order compatibility"):
        compile_p_torsion(prime=3, exponents=(1, 2), structure_constants=tensor)


@pytest.mark.parametrize("tensor", [(((1,),),),
                                    (((0, 0), (0, 1)), ((0, 1), (0, 0)))])
def test_nonalternating_brackets_rejected(tensor):
    with pytest.raises(ValueError, match="alternating"):
        compile_p_torsion(prime=3, exponents=(1,) * len(tensor), structure_constants=tensor)


@pytest.mark.parametrize("changes", [
    {"prime": True}, {"prime": 3.0}, {"prime": 2}, {"prime": 9},
    {"exponents": ()}, {"exponents": (0, 1)}, {"exponents": (-1, 1)},
    {"exponents": (True, 1)}, {"exponents": (1.0, 1)},
    {"exponents": None}, {"exponents": "11"},
    {"structure_constants": None}, {"structure_constants": ""},
    {"structure_constants": {}}, {"structure_constants": ()},
    {"structure_constants": (None, None)},
    {"structure_constants": (((0, 0),), ((0, 0),))},
    {"structure_constants": (((0,), (0,)), ((0,), (0,)))},
    {"structure_constants": (((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)))},
    {"structure_constants": (((0, 0), (True, 0)), ((0, 0), (0, 0)))},
    {"structure_constants": (((0, 0), (1.0, 0)), ((0, 0), (0, 0)))},
    {"structure_constants": (((0, 0), (-1, 0)), ((0, 0), (0, 0)))},
    {"structure_constants": (((0, 0), (3, 0)), ((0, 0), (0, 0)))},
])
def test_malformed_or_noncanonical_inputs_rejected(changes):
    kwargs = dict(prime=3, exponents=(1, 1), structure_constants=tensor_from_brackets(3, (1, 1), {}))
    kwargs.update(changes)
    with pytest.raises(ValueError):
        compile_p_torsion(**kwargs)


def test_iterable_inputs_are_frozen_once():
    tensor = tensor_from_brackets(3, (1, 1, 2), {(0, 1): (0, 0, 3)})
    result = compile_p_torsion(prime=3, exponents=iter([1, 1, 2]),
                               structure_constants=(map(iter, plane) for plane in tensor))
    assert result.exponents == (1, 1, 2)
    assert result.structure_constants == tensor
    assert result.torsion_class == 2
