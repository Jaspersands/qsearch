from itertools import product
import random

from flint import fmpz_mat
import pytest

from theorems.abelian_quotient_torsion import (
    build_report, evaluate_preimage_generators, mixed_generator_control,
    p_torsion_words,
)


def _closure(generators, identity, multiply):
    seen, queue = {identity}, [identity]
    while queue:
        x = queue.pop()
        for generator in generators:
            y = multiply(x, generator)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return seen


@pytest.mark.parametrize("p", [2, 3, 5, 2**127-1])
def test_mixed_generator_counterexample_and_exact_repair(p):
    record = mixed_generator_control(p)
    assert record["naive_torsion_order"] == p
    assert record["actual_torsion_order"] == p*p
    assert record["torsion_words"] == ((p, 0), (-1, 1))
    assert not record["hidden_line_0_1_survives_naive_step"]
    assert record["hidden_line_0_1_survives_repaired_step"]


@pytest.mark.parametrize("p", [2, 3, 5])
def test_exhaustive_small_abelian_torsion_not_only_a_known_hidden_line(p):
    certificate = p_torsion_words(p, ((p*p, 0), (-p, p)))
    multiply = lambda a, b: ((a[0]+b[0]) % (p*p), (a[1]+b[1]) % p)
    power = lambda a, n: (n*a[0] % (p*p), n*a[1] % p)
    generators = evaluate_preimage_generators(certificate, ((1, 0), (1, 1)), (),
        identity=(0, 0), multiply=multiply, power=power)
    actual = _closure(generators, (0, 0), multiply)
    expected = {a for a in product(range(p*p), range(p)) if power(a, p) == (0, 0)}
    assert actual == expected
    for x in product(range(p*p), range(p)):
        hidden = _closure((x,), (0, 0), multiply)
        if len(hidden) > 1:
            assert len(hidden & actual) > 1


@pytest.mark.parametrize("p", [2, 3])
def test_nonabelian_preimage_keeps_the_whole_commutator_kernel(p):
    modulus = p*p
    def multiply(a, b):
        x, y, z = a
        X, Y, Z = b
        return ((x+X) % modulus, (y+Y) % modulus, (z+Z+x*Y) % modulus)
    def power(a, n):
        x, y, z = a
        return (n*x % modulus, n*y % modulus, (n*z+n*(n-1)//2*x*y) % modulus)
    identity = (0, 0, 0)
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    certificate = p_torsion_words(p, ((p*p, 0), (0, p*p)))
    generators = evaluate_preimage_generators(certificate, (X, Y), (Z,),
        identity=identity, multiply=multiply, power=power)
    actual = _closure(generators, identity, multiply)
    expected = {(x, y, z) for x, y, z in product(range(modulus), repeat=3)
                if x % p == y % p == 0}
    assert actual == expected and len(actual) == p**4
    without_kernel = _closure(generators[1:], identity, multiply)
    hidden_in_kernel = _closure((Z,), identity, multiply)
    assert without_kernel & hidden_in_kernel == {identity}
    assert hidden_in_kernel <= actual
    # Keeping only the known H0, instead of B, also loses outer-loop progress.
    H0 = _closure((power(Z, p),), identity, multiply)
    hidden = _closure((multiply(power(X, p), Z),), identity, multiply)
    insufficient = _closure((power(Z, p), *generators[1:]), identity, multiply)
    assert H0 < hidden <= actual
    assert hidden & insufficient == H0
    # The reduction's invariant must hold for every cyclic hidden subgroup.
    for g in product(range(modulus), repeat=3):
        hidden = _closure((g,), identity, multiply)
        if len(hidden) > 1:
            assert len(hidden & actual) > 1


def _nonzero_hnf(matrix):
    hnf = matrix.hnf()
    return tuple(tuple(int(hnf[i, j]) for j in range(hnf.ncols()))
                 for i in range(hnf.nrows()) if any(hnf[i, j] for j in range(hnf.ncols())))


@pytest.mark.parametrize("p", [2, 3, 43, 2**127-1])
def test_unimodular_basis_change_and_redundant_generator_relations(p):
    rng = random.Random(293)
    for _ in range(8):
        # D includes a trivial factor, so the generating list has redundancy.
        diagonal = [1, p, p*p, p**4]
        R = fmpz_mat([[diagonal[i] if i == j else 0 for j in range(4)] for i in range(4)])
        U = fmpz_mat([[int(i == j) for j in range(4)] for i in range(4)])
        for _ in range(8):
            i, j = rng.sample(range(4), 2)
            scale = rng.choice((-7, -3, 2, 5))
            for k in range(4):
                U[i, k] += scale*U[j, k]
        alternate = U*R
        rows = tuple(tuple(int(alternate[i, j]) for j in range(4)) for i in range(4))
        certificate = p_torsion_words(p, rows)
        assert certificate.quotient_order == p**7
        assert certificate.torsion_order == p**3
        assert certificate.descent_index == p**4
        expected = fmpz_mat([[([1, 1, p, p**3][i]) if i == j else 0
                             for j in range(4)] for i in range(4)])
        assert certificate.preimage_lattice_basis == _nonzero_hnf(expected)
        for a, word in zip(certificate.modular_relation_coefficients, certificate.generator_words):
            assert tuple(sum(a[i]*rows[i][j] for i in range(4)) for j in range(4)) == tuple(p*x for x in word)


def test_integer_word_coefficients_must_not_be_reduced_mod_prime():
    certificate = p_torsion_words(3, ((27,),))
    assert certificate.generator_words == ((9,),)
    assert certificate.generator_words[0][0] % 3 == 0  # Reduction would erase the generator.
    assert certificate.torsion_order == 3 and certificate.descent_index == 9


def test_elementary_and_trivial_quotients_do_not_force_a_strict_step():
    for rows in (((3, 0), (0, 3)), ((1, 0), (0, 1))):
        certificate = p_torsion_words(3, rows)
        assert certificate.elementary_quotient
        assert certificate.descent_index == 1


def test_valid_relations_do_not_certify_completeness_for_the_actual_group():
    # R describes C_9 x C_3; every row is ALSO valid in the smaller C_3^2.
    certificate = p_torsion_words(3, ((9, 0), (0, 3)))
    images_in_actual_group = tuple(tuple(x % 3 for x in word)
                                  for word in certificate.generator_words)
    assert images_in_actual_group == ((0, 0), (0, 1))
    assert not certificate.input_relation_completeness_certified


@pytest.mark.parametrize("p,rows", [(4, ((4,),)), (2, ()), (2, ((1, 2),)),
                                  (2, ((1, 0), (0, 0))), (2, ((3,),)),
                                  (2, ((True,),))])
def test_bad_presentations_rejected(p, rows):
    with pytest.raises(ValueError):
        p_torsion_words(p, rows)


def test_report_does_not_claim_a_quantum_backend_or_free_presentation():
    report = build_report()
    assert report["hidden_source_calls"] == 0
    for flag in ("field_enumeration_used", "factorization_used", "relation_acquisition_implemented",
                 "input_relation_completeness_certified", "full_outer_hsp_implemented",
                 "noiseless_rees_core_refuted", "independent_review", "novelty_established",
                 "speedup_claim_allowed"):
        assert report[flag] is False
