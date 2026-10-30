from itertools import product

import pytest

from abelian_action_normalizer import AbelianAction, _lattice, _order


def generated_group(action, generators, cap=5000):
    seen, queue = {action.identity}, [action.identity]
    for x in queue:
        for g in generators:
            y = action.multiply(x, g)
            if y not in seen:
                seen.add(y)
                queue.append(y)
                if len(seen) > cap:
                    raise AssertionError("finite control exceeded its fixed cap")
    return seen


def subgroup_elements(action, generators):
    seen, queue = {(0,) * action.rank}, [(0,) * action.rank]
    for x in queue:
        for g in generators:
            y = tuple((a + b) % m for a, b, m in zip(x, g, action.moduli))
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return seen


def independent_stabilizer(action, group, k_generators):
    k = subgroup_elements(action, k_generators)
    return {g for g in group if {action.apply(g, v) for v in k} == k}


def mixed_action(p=5):
    action = AbelianAction(p, (2, 1))
    return action, (action.matrix(((1, p), (0, 1))),
                    action.matrix(((1, 0), (1, 1))))


def triangular_action(p=5):
    action = AbelianAction(p, (1, 1, 1))
    return action, (action.matrix(((1, 1, 0), (0, 1, 0), (0, 0, 1))),
                    action.matrix(((1, 0, 0), (0, 1, 1), (0, 0, 1))))


@pytest.mark.parametrize("kind", [mixed_action, triangular_action])
def test_log_exp_is_exact_on_whole_noncommutative_group(kind):
    action, generators = kind()
    group = generated_group(action, generators)
    assert len(group) == 125
    logs = set()
    for g in group:
        x = action.logarithm(g)
        assert action.exponential(x) == g
        logs.add(x)
    for x in logs:
        assert action.logarithm(action.exponential(x)) == x
    for x, y in product(logs, repeat=2):
        assert action.add(x, y) in logs
        assert action.bracket(x, y) in logs


@pytest.mark.parametrize("k", [(), ((0, 0),), ((1, 0),), ((0, 1),),
                              ((5, 1),), ((5, 0),), ((1, 1),),
                              ((5, 0), (0, 1)), ((1, 0), (0, 1))])
def test_mixed_stabilizer_matches_actual_subgroup_action(k):
    action, generators = mixed_action()
    group = generated_group(action, generators)
    result = action.stabilizer(generators, k)
    expected = independent_stabilizer(action, group, k)
    actual = generated_group(action, result.stabilizer_group_generators)
    assert actual == expected
    assert result.stabilizer_order == len(expected)
    assert result.action_order == len(group)
    assert set(result.stabilizer_log_generators) <= {action.logarithm(g) for g in expected}


@pytest.mark.parametrize("k", [(), ((1, 0, 0),), ((0, 1, 0),), ((0, 0, 1),),
                              ((1, 2, 3),), ((1, 0, 0), (0, 1, 0)),
                              ((0, 1, 0), (0, 0, 1)),
                              ((1, 1, 0), (0, 1, 1)),
                              ((1, 0, 0), (0, 1, 0), (0, 0, 1))])
def test_elementary_stabilizer_matches_actual_subspace_action(k):
    action, generators = triangular_action()
    group = generated_group(action, generators)
    result = action.stabilizer(generators, k)
    expected = independent_stabilizer(action, group, k)
    assert generated_group(action, result.stabilizer_group_generators) == expected
    assert result.stabilizer_order == len(expected)


def test_brackets_are_required_not_only_span_of_generator_logs():
    action, generators = triangular_action()
    lattice, basis = action.lie_closure(generators)
    naive = _lattice(action.end_moduli, [action.encode(action.logarithm(g))
                                       for g in generators])
    assert _order(action.end_moduli, naive) == 25
    assert _order(action.end_moduli, lattice) == 125
    assert len(basis) == 3


def test_setwise_stabilizer_is_not_pointwise_centralizer():
    action, generators = triangular_action()
    k = ((1, 0, 0), (0, 1, 0))
    result = action.stabilizer(generators, k)
    assert result.stabilizer_order == 125
    assert action.apply(generators[0], k[1]) != k[1]


def test_mod_p_reduction_misses_mixed_module_information():
    action, generators = mixed_action()
    k = ((0, 1),)
    g = generators[0]
    assert tuple(tuple(x % 5 for x in row) for row in g) == action.identity
    assert not action.preserves(g, k)
    result = action.stabilizer(generators, k)
    assert result.stabilizer_order == 25 < result.action_order


def test_cyclic_prime_power_action_is_not_an_elementary_vector_space():
    action = AbelianAction(5, (3,))
    g = ((6,),)
    group = generated_group(action, (g,))
    assert len(group) == 25
    for k in [(), ((1,),), ((5,),), ((25,),)]:
        result = action.stabilizer((g,), k)
        assert result.action_order == result.stabilizer_order == 25
        assert generated_group(action, result.stabilizer_group_generators) == group


@pytest.mark.parametrize("k", [((1, 0),), ((5, 1),), ((5, 0), (0, 5))])
def test_nonfree_log_constraints_on_equal_prime_power_factors(k):
    action = AbelianAction(5, (2, 2))
    generators = (((1, 1), (0, 1)), ((1, 0), (5, 1)),
                  ((6, 0), (0, 1)), ((1, 0), (0, 6)))
    group = generated_group(action, generators)
    assert len(group) == 5**5
    expected = independent_stabilizer(action, group, k)
    result = action.stabilizer(generators, k)
    assert result.action_order == 5**5
    assert result.stabilizer_order == len(expected)
    assert generated_group(action, result.stabilizer_group_generators) == expected


def test_mixed_matrix_composition_on_every_module_element():
    action, generators = mixed_action()
    probes = generators + (action.identity, action.multiply(*generators))
    for x, y in product(probes, repeat=2):
        for v in product(range(25), range(5)):
            assert action.apply(action.multiply(x, y), v) == action.apply(x, action.apply(y, v))


def test_noncommuting_individually_unipotent_generators_are_not_enough():
    action = AbelianAction(5, (1, 1))
    upper, lower = ((1, 1), (0, 1)), ((1, 0), (1, 1))
    assert action.exponential(action.logarithm(upper)) == upper
    assert action.exponential(action.logarithm(lower)) == lower
    with pytest.raises(ValueError, match="joint augmentation"):
        action.stabilizer((upper, lower), ((1, 0),))


def test_changed_mixed_basis_and_redundant_generators():
    action, generators = mixed_action()
    change = ((2, 5), (1, 2))
    # Find this public inverse only in this bounded independent fixture.
    inverse = next(m for entries in product(range(25), range(5), range(5), range(5))
                   if (m := ((entries[0], 5*entries[1]), (entries[2], entries[3])))
                   and action.multiply(change, m) == action.identity)
    conjugated = tuple(action.multiply(action.multiply(change, g), inverse)
                       for g in generators)
    k = ((5, 1),)
    changed_k = tuple(action.apply(change, v) for v in k)
    result = action.stabilizer(conjugated * 2 + (action.identity,), changed_k * 3)
    reference = action.stabilizer(generators, k)
    expected = {action.multiply(action.multiply(change, g), inverse)
                for g in generated_group(action, reference.stabilizer_group_generators)}
    assert generated_group(action, result.stabilizer_group_generators) == expected


def test_large_prime_has_no_enumeration_dependency():
    p = 2**127 - 1
    action, generators = mixed_action(p)
    result = action.stabilizer(generators, ((0, 1),))
    assert result.action_order == p**3
    assert result.stabilizer_order == p**2
    assert all(action.preserves(g, ((0, 1),)) for g in result.stabilizer_group_generators)


@pytest.mark.parametrize("dimension,prime", [(4, 7), (8, 11), (12, 17)])
def test_growing_class_action_leaves_a_two_dimensional_quotient(dimension, prime):
    action = AbelianAction(prime, (1,) * dimension)
    g = tuple(tuple(int(i == j) + int(j == i+1) for j in range(dimension))
              for i in range(dimension))
    k = tuple(tuple(int(i == j) for i in range(dimension))
              for j in range(dimension-2))
    result = action.stabilizer((g,), k)
    assert result.action_order == result.stabilizer_order == prime
    assert all(action.preserves(h, k) for h in result.stabilizer_group_generators)
    quotient = tuple(tuple(g[i][j] for j in range(dimension-2, dimension))
                     for i in range(dimension-2, dimension))
    assert quotient == ((1, 1), (0, 1))
    # The semidirect product F_p^dimension rtimes <g> has class dimension;
    # quotienting by this supplied K leaves the known class-two group of
    # order p^3. No HSP intersection learner is used by this fixture.
    difference = action.add(g, action.scale(-1, action.identity))
    power = action.identity
    for _ in range(dimension-1):
        power = action.multiply(power, difference)
    assert power != action.zero
    assert action.multiply(power, difference) == action.zero


def test_noninvariant_intersection_requires_normalizing_before_quotienting():
    action, generators = triangular_action()
    k = ((0, 0, 1),)
    result = action.stabilizer(generators, k)
    assert result.stabilizer_order == 5 < 125
    assert not action.preserves(generators[1], k)


def test_action_stabilizer_need_not_be_normal():
    action, generators = triangular_action()
    k = ((0, 0, 1),)
    g, h = generators
    assert action.preserves(g, k)
    h_inverse = action.exponential(action.scale(-1, action.logarithm(h)))
    conjugate = action.multiply(action.multiply(h, g), h_inverse)
    assert not action.preserves(conjugate, k)


def test_logarithmic_containment_equivalence_on_mixed_module():
    action, generators = mixed_action()
    for g in generated_group(action, generators):
        for k in [((1, 0),), ((5, 1),), ((5, 0), (0, 1))]:
            assert action.preserves(g, k) == action.preserves(action.logarithm(g), k)


def test_empty_action_and_length_one_boundary():
    action = AbelianAction(3, (1,))
    for k in [(), ((1,),)]:
        result = action.stabilizer((), k)
        assert result.action_order == result.stabilizer_order == 1
        assert not result.stabilizer_group_generators
    assert action.logarithm(action.identity) == action.zero
    assert action.exponential(action.zero) == action.identity


@pytest.mark.parametrize("p,exponents", [(4, (1,)), (2, (1, 1)), (3, (3,)),
                                       (5, (0,)), (5, ())])
def test_invalid_prime_exponents_or_denominator_regime(p, exponents):
    with pytest.raises(ValueError):
        AbelianAction(p, exponents)


def test_invalid_mixed_module_map_and_nonnilpotent_matrix():
    action, _ = mixed_action()
    with pytest.raises(ValueError, match="mixed module"):
        action.matrix(((1, 1), (0, 1)))
    with pytest.raises(ValueError, match="nilpotent"):
        action.logarithm(((2, 0), (0, 1)))
    with pytest.raises(ValueError, match="nilpotent"):
        action.exponential(action.identity)
    with pytest.raises(ValueError, match="shape"):
        action.matrix(((1,),))
