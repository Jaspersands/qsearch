from fractions import Fraction
from itertools import product
import random

import pytest
from sympy import Matrix, eye, zeros

from borel_residual import (
    build_borel_reduction, check_exceptional_planes, diagonalize_symmetric,
)
from residual import (
    analyze_pullback, alternating_form, column_basis, compatible_neighbor,
    inverse_mod, lift_split, mod, same_space,
)
from residual_controls import (
    OpaqueLabels, inert_stable_fixture, lagrangians, space_key,
    split_frobenius_fixture,
)
from kernel_output import action, product_actions


def reduction(kind):
    source = split_frobenius_fixture(0) if kind == "split" else inert_stable_fixture()
    result = analyze_pullback(source.order, source.reference_pullbacks()[0], 5,
                              source.characteristic, source.split(5))
    return build_borel_reduction(result.residual_operator, 5, source.characteristic,
                                 rng=random.Random(523)), source


def lines(p):
    return [Matrix([1, 0])] + [Matrix([a, 1]) for a in range(p)]


@pytest.mark.parametrize("kind", ["split", "nonsplit"])
def test_projective_parameterization_matches_full_prime_square_census(kind):
    r, source = reduction(kind)
    generated = [r.kernel_from_line(v) for v in lines(5)] + list(r.exceptional_planes)
    a = action(source.reference_pullbacks()[0], product_actions(lift_split(source.order, source.split(5), 5)))
    accepted = [k for k in lagrangians(5) if compatible_neighbor(a, k, 5)]
    assert len(generated) == (8 if kind == "split" else 6)
    assert {space_key(k, 5) for k in generated} == {space_key(k, 5) for k in accepted}
    assert not r.quantum_receiver_executed
    assert not r.geometric_input_verified
    assert Fraction(r.abort_bound) <= Fraction(1, 2**64)


@pytest.mark.parametrize("kind", ["split", "nonsplit"])
def test_every_small_group_element_has_exact_borel_collision_partition(kind):
    r, _ = reduction(kind)
    group = []
    for entries in product(range(5), repeat=4):
        a = Matrix(2, 2, entries)
        det = int(a.det()) % 5
        if det and (r.domain == "GL2" or det == 1):
            group.append(a)
    assert len(group) == (480 if r.domain == "GL2" else 120)
    for line in lines(5):
        oracle = OpaqueLabels(r.kernel_from_line(line), 5)
        labels_by_line, lines_by_label = {}, {}
        for a in group:
            image = r.embed(a)
            assert same_space(image * r.kernel_from_line(line), r.kernel_from_line(a * line), 5)
            key = space_key(a * line, 5)
            label = r.restricted_label(a, oracle)
            assert labels_by_line.setdefault(key, label) == label
            assert lines_by_label.setdefault(label, key) == key
        assert len(labels_by_line) == 6
        assert oracle.calls == len(group)


@pytest.mark.parametrize("kind", ["split", "nonsplit"])
def test_embedding_homomorphism_and_public_conjugation(kind):
    r, source = reduction(kind)
    a, b = Matrix([[1, 2], [0, 1]]), Matrix([[1, 0], [3, 1]])
    assert r.embed(a * b) == mod(r.embed(a) * r.embed(b), 5)
    v = Matrix([1, 2, 3, 4])
    s = mod(eye(4) + v * v.T * alternating_form(2), 5)
    conjugate = build_borel_reduction(s * r.beta * inverse_mod(s, 5), 5,
                                      source.characteristic, rng=random.Random(8))
    old = [s * r.kernel_from_line(v) for v in lines(5)] + [s * k for k in r.exceptional_planes]
    new = [conjugate.kernel_from_line(v) for v in lines(5)] + list(conjugate.exceptional_planes)
    assert {space_key(k, 5) for k in old} == {space_key(k, 5) for k in new}


@pytest.mark.parametrize("index", list(range(8)))
def test_split_exceptional_orbits_checked_before_borel_receiver(index):
    r, _ = reduction("split")
    kernels = list(r.exceptional_planes) + [r.kernel_from_line(v) for v in lines(5)]
    oracle = OpaqueLabels(kernels[index], 5)
    result = check_exceptional_planes(r, oracle)
    if index < 2:
        assert same_space(result.kernel, kernels[index], 5)
    else:
        assert result.kernel is None
    assert result.original_label_queries == oracle.calls <= 5
    assert not result.source_hsp_promise_verified


def test_no_exceptional_oracle_calls_in_nonsplit_case():
    r, _ = reduction("nonsplit")
    oracle = OpaqueLabels(r.kernel_from_line(Matrix([1, 0])), 5)
    result = check_exceptional_planes(r, oracle)
    assert result.kernel is None
    assert result.original_label_queries == oracle.calls == 0


@pytest.mark.parametrize("p,domain", [(7, "GL2"), (11, "SL2")])
def test_127_bit_frame_construction_and_action_without_field_enumeration(p, domain):
    ell = 2**127 - 1
    block = Matrix([[0, 1], [-p, 0]])
    r = build_borel_reduction(Matrix.diag(block, block), ell, p, rng=random.Random(483))
    assert r.domain == domain
    a, b = Matrix([[1, 89237], [0, 1]]), Matrix([[1, 0], [94287, 1]])
    assert r.embed(a * b) == mod(r.embed(a) * r.embed(b), ell)
    line = Matrix([74894231, 82734234])
    assert same_space(r.embed(a) * r.kernel_from_line(line), r.kernel_from_line(a * line), ell)
    assert Fraction(r.abort_bound) <= Fraction(1, 2**64)


def test_off_diagonal_only_form_diagonalization():
    form = Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 2], [0, 0, 2, 0]])
    frame, coefficients = diagonalize_symmetric(form, 5)
    assert mod(frame.T * form * frame, 5) == Matrix.diag(*coefficients)
    assert all(coefficients)


def test_nonsplit_random_abort_is_explicit_not_unbounded_retry():
    from scalar_cancellation import TrialBudgetExceeded

    class AlwaysSquare:
        def randrange(self, start, stop):
            return 1

    r, _ = reduction("nonsplit")
    with pytest.raises(TrialBudgetExceeded):
        build_borel_reduction(r.beta, 5, 7, rng=AlwaysSquare(), security_bits=3)


def test_invalid_beta_domain_and_output_are_rejected():
    r, _ = reduction("nonsplit")
    with pytest.raises(ValueError, match="domain"):
        r.embed(Matrix.diag(1, 2))
    with pytest.raises(ValueError, match="projective"):
        r.kernel_from_line(zeros(2, 1))
    with pytest.raises(ValueError, match="squared"):
        build_borel_reduction(eye(4), 5, 7)
    with pytest.raises(ValueError, match="skew-adjoint"):
        build_borel_reduction(2 * eye(4), 5, 11)


def test_local_fixtures_do_not_claim_to_execute_the_receiver():
    r, _ = reduction("nonsplit")
    assert not r.quantum_receiver_executed and not r.geometric_input_verified
    # Constant source is outside the original HSP promise. A local controller
    # cannot establish that promise by checking its own arithmetic.
    split, _ = reduction("split")
    selected = check_exceptional_planes(split, lambda _: "invalid_constant")
    assert selected.kernel is not None
    assert not selected.source_hsp_promise_verified


@pytest.mark.parametrize("p,seed", [(7, 9), (11, 3), (11, 19)])
def test_random_draw_count_includes_scalar_backend(p, seed):
    class CountingRandom(random.Random):
        calls = 0

        def randrange(self, *args):
            self.calls += 1
            return super().randrange(*args)

    rng = CountingRandom(seed)
    ell = 2**127 - 1
    block = Matrix([[0, 1], [-p, 0]])
    result = build_borel_reduction(Matrix.diag(block, block), ell, p, rng=rng)
    assert result.random_draws == rng.calls
