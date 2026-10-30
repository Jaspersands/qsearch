from itertools import product
import json

from flint import fq_default_poly_ctx
import pytest
import z3

from theorems.balanced_codeword_filter import reciprocal_trace
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_smt import (
    BinaryFieldCircuit, native_instance, restrict_instance, run_experiment,
    syndrome, validate_instance, vandermonde_eliminate_residual, verify_word,
)


def instance(bits, points, targets, checks=1):
    return {"bits": bits, "points": list(points), "targets": list(targets),
            "checks": checks,
            "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs()))}


@pytest.mark.parametrize("bits", [2, 3, 5])
def test_field_circuit_matches_independent_flint(bits):
    circuit = BinaryFieldCircuit(bits)
    for left, right in product(range(1 << bits), repeat=2):
        x, y = z3.BitVecVal(left, bits), z3.BitVecVal(right, bits)
        wanted = encoded(element(bits, left)*element(bits, right))
        assert z3.simplify(circuit.multiply(x, y)).as_long() == wanted
        assert z3.simplify(circuit.constant_product(circuit.shifts(x), right)).as_long() == wanted
        assert z3.simplify(circuit.trace(x)).as_long() == int(element(bits, left).trace())
    assert encoded(element(3, 3)*element(3, 3)) != (3*3) % 8


@pytest.mark.parametrize("bits", [2, 3, 5])
def test_zero_complete_inverse_graph_not_just_nonzero_product(bits):
    circuit = BinaryFieldCircuit(bits)
    for left, right in product(range(1 << bits), repeat=2):
        actual = z3.is_true(z3.simplify(circuit.inverse_graph(
            z3.BitVecVal(left, bits), z3.BitVecVal(right, bits))))
        inverse = encoded(element(bits, left)**-1) if left else 0
        assert actual == (right == inverse)


@pytest.mark.parametrize("pipeline", ["direct", "qfbv", "vandermonde"])
def test_full_solver_matches_exhaustive_original_relation(pipeline):
    for targets in product((0, 1), repeat=3):
        problem = instance(2, (0, 1, 2), targets)
        exists = any(verify_word(problem, word) for word in product(range(4), repeat=3))
        result = run_experiment(problem, full=True, timeout_ms=5000, pipeline=pipeline)
        assert (result["status"] == "VERIFIED_NATIVE_WITNESS") == exists
        if exists:
            assert verify_word(problem, result["witness"])
            assert result["full_original_word_verified"]
        else:
            assert result["status"] == "UNSAT_FULL_INSTANCE_REPORTED"
        assert not result["hardness_evidence"] and not result["uniform_sampler"]
        assert result["solver_pipeline"] == pipeline
        assert result["scope"] == "full_original_instance"
        assert result["solver_statistics"]


def test_invalid_pipeline_is_not_silently_changed():
    with pytest.raises(ValueError, match="pipeline"):
        run_experiment(native_instance(5), pipeline="other")


def test_random_prefix_is_accepted_and_uses_original_syndrome():
    problem = native_instance(17, 171, "random")
    indices, prefix, target = restrict_instance(problem, 172)
    assert indices == tuple(range(45)) and len(prefix) == 244
    assert all(reciprocal_trace(17, word) == problem["targets"][i] for i, word in prefix.items())
    assert target == syndrome(17, [problem["points"][i] for i in prefix], list(prefix.values()), 36)
    assert (indices, prefix, target) == restrict_instance(problem, 172)


def test_full_instance_does_not_inherit_the_prefix_restriction():
    problem = native_instance(17, 171, "random")
    indices, prefix, target = restrict_instance(problem, 172, full=True)
    assert indices == tuple(range(289)) and prefix == {}
    assert target == (0,)*36
    assert len(indices)-problem["checks"] == 253


@pytest.mark.parametrize("bits", [5, 7])
def test_trace_interpolation_does_not_imply_rs_product_consistency(bits):
    problem = native_instance(bits, 1028)
    points = [element(bits, a) for a in problem["points"]]
    ring = fq_default_poly_ctx(field(bits))
    variable, polynomial = ring.gen(), ring.one()
    for point in points:
        polynomial *= variable-point
    derivative = polynomial.derivative()
    length, checks = len(points), problem["checks"]
    assert derivative.degree() == length-1  # Odd length in characteristic two.
    assert (checks-1)+(length-checks-1) < derivative.degree()
    # A=1 satisfies every reciprocal-trace equation at odd extension degree,
    # but Af=P' would force f above the dual-RS degree bound.
    assert all(reciprocal_trace(bits, 1) == b for b in problem["targets"])
    assert syndrome(bits, problem["points"], [1]*length, checks)[0] == 1
    assert not verify_word(problem, [1]*length)
    # P'=V^2 gives a real codeword x_i=1/V(alpha_i), not arbitrary targets.
    square_root = ring([derivative[2*j]**(1 << (bits-1))
                        for j in range((derivative.degree()//2)+1)])
    assert square_root*square_root == derivative
    word = [encoded(square_root(point)**-1) for point in points]
    assert not any(syndrome(bits, problem["points"], word, checks))
    induced = dict(problem, targets=[reciprocal_trace(bits, x) for x in word])
    assert verify_word(induced, word)


@pytest.mark.parametrize("bits", [5, 7])
def test_odd_all_one_affine_as_family_has_nonzero_syndrome_polynomial(bits):
    problem = native_instance(bits, 1028)
    ring = fq_default_poly_ctx(field(bits))
    variable, denominator = ring.gen(), ring.one()
    factors = []
    for point in problem["points"]:
        affine = variable+element(bits, point)
        factor = affine*affine+affine+1
        factors.append(factor)
        denominator *= factor
    numerator = sum((denominator//factor for factor in factors), ring.zero())
    assert not numerator.is_zero()
    assert numerator.degree() <= 2*len(factors)-2
    successes = 0
    for value in range(1 << bits):
        parameter = element(bits, value)
        assert denominator(parameter) != 0
        words = [encoded(factor(parameter)**-1) for factor in factors]
        assert all(reciprocal_trace(bits, word) == 1 for word in words)
        zeroth = syndrome(bits, problem["points"], words, 1)[0]
        assert (zeroth == 0) == (numerator(parameter) == 0)
        successes += zeroth == 0
    assert successes <= min(1 << bits, numerator.degree())


@pytest.mark.parametrize("bits", [3, 5])
def test_nonlinear_as_parameters_escape_the_affine_only_obstruction(bits):
    for value in range(2, 1 << bits):
        parameter = element(bits, value)
        denominator = parameter*parameter+parameter+1
        word = tuple(map(encoded, (1/denominator, parameter**2/denominator,
                                   (parameter+1)**2/denominator)))
        assert all(reciprocal_trace(bits, x) == 1 for x in word)
        assert word[0] ^ word[1] ^ word[2] == 0
        # This is a three-coordinate sum identity, not all native K checks.
        assert len(word) != bits*bits


def test_rare_empty_residual_does_not_reject_full_problem(monkeypatch):
    import theorems.inverse_trace_smt as module
    problem = instance(5, (0, 1, 2, 3), (0, 1, 0, 0))
    whole = run_experiment(problem, full=True, timeout_ms=5000)
    assert whole["status"] == "VERIFIED_NATIVE_WITNESS"
    # A legitimate but exceptional accepted prefix; the residual forces
    # x0=x1 while asking for different inverse-trace bits.
    monkeypatch.setattr(module, "restrict_instance", lambda *args, **kwargs: ((0, 1), {2: 0, 3: 0}, (0,)))
    result = run_experiment(problem, timeout_ms=5000)
    assert result["status"] == "UNSAT_THIS_RESIDUAL_ONLY"
    assert result["scope"] == "fixed_accepted_prefix"
    assert result["witness"] is None and not result["hardness_evidence"]


def test_solver_limit_stays_unknown_and_preserves_input():
    problem = native_instance(5, 52)
    before = json.dumps(problem, sort_keys=True)
    result = run_experiment(problem, resource_limit=1, timeout_ms=1000)
    assert result["status"] == "UNKNOWN_SOLVER_LIMIT"
    assert result["reason_unknown"] and result["witness"] is None
    assert not result["hardness_evidence"]
    assert not result["polynomial_time_solver_established"]
    assert not result["whole_workflow_wall_clock_cap_enforced"]
    assert json.dumps(problem, sort_keys=True) == before


def test_independent_verifier_rejects_spurious_all_zero_word_and_bad_model(monkeypatch):
    import theorems.inverse_trace_smt as module
    problem = instance(3, (0, 1, 2), (0, 0, 0))
    assert verify_word(problem, (0, 0, 0))
    assert not verify_word(instance(3, (0, 1, 2), (1, 0, 0)), (0, 0, 0))
    monkeypatch.setattr(module, "verify_word", lambda *args: False)
    with pytest.raises(ArithmeticError, match="independent original-instance"):
        run_experiment(problem, full=True, timeout_ms=5000)


@pytest.mark.parametrize("change", [
    {"points": [1, 1, 2]}, {"targets": [0, 1]}, {"targets": [0, True, 1]},
    {"checks": 0}, {"field_modulus_coefficients": [1, 1]},
])
def test_invalid_public_input_fails_closed(change):
    problem = instance(3, (0, 1, 2), (0, 1, 1))
    problem.update(change)
    with pytest.raises(ValueError):
        validate_instance(problem)


def test_native_campaign_is_prime_degree_unplanted_and_reproducible():
    a = native_instance(17, 3)
    assert a == native_instance(17, 3)
    assert len(set(a["points"])) == 289 and a["checks"] == 36
    assert a["targets"] == [1]*289
    with pytest.raises(ValueError, match="prime extension"):
        native_instance(18)


def test_cli_writes_complete_replayable_instance(tmp_path, capsys):
    from argparse import ArgumentParser
    import qsearch
    from qsearch_cli.commands.general import add_inverse_trace_smt
    parser = ArgumentParser()
    parser.set_defaults(root=tmp_path)
    add_inverse_trace_smt(parser.add_subparsers(dest="command", required=True))
    args = parser.parse_args(["inverse-trace-smt", "--bits", "5", "--resource-limit", "1", "--write"])
    assert args.func is qsearch.command_inverse_trace_smt
    assert args.func(args) == 0
    result = json.loads(capsys.readouterr().out)
    saved = tmp_path/"research/classical_baselines/inverse_trace_smt.json"
    assert json.loads(saved.read_text()) == result
    assert result["status"] == "UNKNOWN_SOLVER_LIMIT"
    assert result["prefix_seed"] != args.seed
    assert result["solver_pipeline"] == "direct"
    assert len(result["instance"]["points"]) == 25


@pytest.mark.parametrize("bits", [5, 7])
def test_vandermonde_eliminate_residual_exact_algebraic_parametrization(bits):
    from random import Random
    problem = native_instance(bits, 1028, "random")
    indices, prefix, target_syndrome = restrict_instance(problem, 1029)
    checks = problem["checks"]
    points = problem["points"]

    pivot_indices, free_indices, constants, coeffs = vandermonde_eliminate_residual(
        bits, points, indices, target_syndrome, checks
    )
    assert len(pivot_indices) == checks
    assert len(free_indices) == len(indices) - checks
    assert len(constants) == checks
    assert len(coeffs) == checks
    assert all(len(row) == len(free_indices) for row in coeffs)

    rng = Random(20261028 + bits)
    for _ in range(10):
        free_vals = [rng.getrandbits(bits) for _ in free_indices]
        piv_vals = []
        for r in range(checks):
            val = element(bits, constants[r])
            for s in range(len(free_indices)):
                val += element(bits, coeffs[r][s]) * element(bits, free_vals[s])
            piv_vals.append(encoded(val))

        residual_vals = piv_vals + free_vals
        actual_syndrome = syndrome(
            bits,
            [points[i] for i in indices],
            residual_vals,
            checks,
        )
        assert actual_syndrome == target_syndrome

        word = [prefix.get(i, 0) for i in range(len(points))]
        for i, val in zip(indices, residual_vals):
            word[i] = val
        assert not any(syndrome(bits, points, word, checks))


@pytest.mark.parametrize("bits,timeout", [(5, 10000), (7, 15000)])
def test_vandermonde_pipeline_solves_and_verifies_native_residual_n5_and_n7(bits, timeout):
    problem = native_instance(bits, 1028)
    result = run_experiment(problem, pipeline="vandermonde", timeout_ms=timeout)
    assert result["status"] == "VERIFIED_NATIVE_WITNESS"
    assert result["full_original_word_verified"] is True
    assert result["solver_pipeline"] == "vandermonde"
    assert result["symbolic_field_variables"] == (
        len(result["residual_indices"]) + result["residual_free_field_variables"]
    )
    assert result["witness"] is not None
    assert verify_word(result["instance"], result["witness"])


@pytest.mark.parametrize("indices", [(-1, 0), (True, 0), (1.0, 0), (3, 0), (1, 1)])
def test_vandermonde_rejects_silently_reinterpreted_coordinate_indices(indices):
    with pytest.raises(ValueError):
        vandermonde_eliminate_residual(2, (0, 1, 2), indices, (0,), 1)


@pytest.mark.parametrize("points, target", [
    ((0, 0, 2), (0,)), ((0, 1, 4), (0,)), ((0, True, 2), (0,)),
    ((0, 1, 2), ()), ((0, 1, 2), (0, 0)),
    ((0, 1, 2), (-1,)), ((0, 1, 2), (4,)), ((0, 1, 2), (True,)),
])
def test_vandermonde_rejects_noncanonical_points_and_syndrome(points, target):
    with pytest.raises(ValueError):
        vandermonde_eliminate_residual(2, points, (0, 1), target, 1)


@pytest.mark.parametrize("checks", [1, 2, 3])
def test_vandermonde_permuted_residual_is_bijective_for_every_small_syndrome(checks):
    from functools import reduce
    from operator import xor
    from theorems.cubic_rs_affine_flats import multiply_binary
    points, indices, bits = (0, 1, 2, 3), (3, 1, 0), 2
    modulus = sum(int(c) << i for i, c in enumerate(field(bits).modulus().coeffs()))

    def mul(a, b):
        return multiply_binary(a, b, modulus, bits)

    def direct_syndrome(word):
        values = [0] * checks
        for index, value in zip(indices, word, strict=True):
            power = 1
            for j in range(checks):
                values[j] ^= mul(power, value)
                power = mul(power, points[index])
        return tuple(values)

    for target in product(range(4), repeat=checks):
        pivots, free, constants, coefficients = vandermonde_eliminate_residual(
            bits, points, indices, target, checks)
        assert pivots + free == indices
        reconstructed = set()
        for values in product(range(4), repeat=len(free)):
            head = tuple(constants[r] ^ reduce(xor, (mul(c, v) for c, v in
                         zip(coefficients[r], values, strict=True)), 0) for r in range(checks))
            reconstructed.add(head + values)
        exhaustive = {word for word in product(range(4), repeat=len(indices))
                      if direct_syndrome(word) == target}
        assert reconstructed == exhaustive
        assert len(reconstructed) == 4 ** len(free)
