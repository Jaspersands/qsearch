"""Independent finite pairing controls for exact terminal annihilator readout."""
from dataclasses import replace
from fractions import Fraction
from itertools import product
from math import prod
import random

from flint import fmpq_mat, fmpz_mat
import pytest

from theorems.mixed_abelian_readout import (
    canonical_modal_token, recover_annihilator, verify_annihilator,
)


def direct_annihilator(labels, moduli):
    return {x for x in product(*(range(m) for m in moduli))
            if all(sum(Fraction(a * b, m) for a, b, m in zip(label, x, moduli)).denominator == 1
                   for label in labels)}


def generated_subgroup(columns, moduli):
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


def check_exhaustive(prime, exponents, labels):
    moduli = tuple(prime**e for e in exponents)
    result = recover_annihilator(prime=prime, ambient_exponents=exponents, fourier_labels=labels)
    expected = direct_annihilator(labels, moduli)
    assert verify_annihilator(result)
    assert generated_subgroup(result.generator_columns, moduli) == expected
    assert result.subgroup_order == len(expected)
    span = generated_subgroup(labels, moduli)
    assert result.observed_span_order == len(span)
    assert result.subgroup_order * result.observed_span_order == prod(moduli)
    basis = fmpz_mat(result.lattice_basis)
    assert basis.transpose().is_hnf()
    assert prod(moduli) == int(basis.det()) * result.subgroup_order
    inverse = fmpq_mat(basis).inv()
    for x in product(*(range(m) for m in moduli)):
        coordinates = inverse * fmpq_mat([[a] for a in x])
        assert all(row[0].denominator == 1 for row in coordinates.tolist()) == (x in expected)
    assert result.observed_span_only is True
    assert result.hidden_subgroup_recovery_certified is False
    assert result.source_law_certified is False
    return result


@pytest.mark.parametrize("exponents", [(1, 2), (2, 1)])
def test_every_pair_of_labels_in_tiny_mixed_module(exponents):
    elements = list(product(*(range(3**e) for e in exponents)))
    for labels in product(elements, repeat=2):
        check_exhaustive(3, exponents, labels)


@pytest.mark.parametrize("prime,exponents", [(3, (2, 3)), (5, (1, 2)), (3, (1, 2, 1))])
def test_seeded_oblique_labels_match_all_exact_pairings(prime, exponents):
    rng = random.Random(20261030)
    for count in range(5):
        labels = [tuple(rng.randrange(prime**e) for e in exponents) for _ in range(count)]
        check_exhaustive(prime, exponents, labels)


@pytest.mark.parametrize("labels", [[], [(0, 0)], [(0, 0)] * 4])
def test_empty_or_zero_labels_return_entire_ambient_module(labels):
    result = check_exhaustive(3, (1, 2), labels)
    assert result.lattice_basis == ((1, 0), (0, 1))
    assert result.subgroup_order == 27
    assert result.observed_span_order == 1
    assert len(result.duality_certificate.label_pairings) == len(labels)


def test_full_fourier_span_returns_trivial_annihilator():
    result = check_exhaustive(3, (1, 2), [(1, 0), (0, 1)])
    assert result.lattice_basis == ((3, 0), (0, 9))
    assert result.generator_columns == ((0, 0), (0, 0))
    assert result.subgroup_order == 1


def test_different_generating_sets_have_same_canonical_lattice_token():
    generating_sets = [
        [(3, 3), (0, 9)],
        [(0, 9), (3, 3)],
        [(3, 12), (0, 9)],
        [(6, 6), (0, 18), (3, 3), (0, 0), (6, 6)],
    ]
    results = [check_exhaustive(3, (2, 3), labels) for labels in generating_sets]
    assert len({result.canonical_token for result in results}) == 1
    assert len({result.generator_columns for result in results}) == 1


def test_incomplete_fourier_span_strictly_overestimates_hidden_subgroup():
    moduli = (3, 9)
    hidden = generated_subgroup([(0, 3)], moduli)
    full_support = direct_annihilator(hidden, moduli)
    complete = check_exhaustive(3, (1, 2), tuple(full_support))
    incomplete = check_exhaustive(3, (1, 2), [(1, 0)])
    assert generated_subgroup(complete.generator_columns, moduli) == hidden
    assert hidden < generated_subgroup(incomplete.generator_columns, moduli)
    assert incomplete.subgroup_order == 9 > complete.subgroup_order == 3
    for result in (incomplete, complete):
        assert not result.certificate()["hidden_subgroup_recovery_certified"]
        assert not result.certificate()["source_law_certified"]


def test_labels_invisible_mod_p_still_impose_mixed_prime_power_pairings():
    labels = [(3, 3), (0, 9)]
    assert all(a % 3 == 0 for label in labels for a in label)
    result = check_exhaustive(3, (2, 3), labels)
    assert result.subgroup_order == 27 < 3**5
    subgroup = generated_subgroup(result.generator_columns, (9, 27))
    assert (1, 6) in subgroup
    assert (1, 3) not in subgroup


def test_raw_duality_canonical_transform_and_containment_are_exact():
    result = check_exhaustive(3, (2, 3), [(3, 3), (0, 9)])
    certificate = result.duality_certificate
    observed = fmpq_mat(certificate.pilot_frame.lattice_basis)
    diagonal = fmpq_mat([[9, 0], [0, 27]])
    dual = fmpq_mat(certificate.dual_basis)
    basis = fmpq_mat(result.lattice_basis)
    transform = fmpq_mat(certificate.canonical_transform)
    assert dual == diagonal * observed.inv().transpose()
    assert observed.transpose() * diagonal.inv() * dual == fmpq_mat([[1, 0], [0, 1]])
    assert basis == dual * transform
    assert abs(transform.det()) == 1
    assert basis * fmpq_mat(certificate.ambient_relations) == diagonal
    assert fmpq_mat(result.fourier_labels) * diagonal.inv() * basis == fmpq_mat(certificate.label_pairings)


def test_exponent_128_does_not_enumerate_module(monkeypatch):
    import builtins
    original_range = builtins.range

    def bounded_range(*args):
        interval = original_range(*args)
        if interval and abs(interval.stop - interval.start) // abs(interval.step) > 10000:
            pytest.fail("attempted module-sized enumeration")
        return interval

    monkeypatch.setattr(builtins, "range", bounded_range)
    result = recover_annihilator(prime=3, ambient_exponents=(2, 128),
                                 fourier_labels=[(3, 3**127)])
    assert result.lattice_basis == ((1, 0), (2, 3))
    assert result.subgroup_order == 3**129
    assert result.observed_span_order == 3
    assert verify_annihilator(result)


def test_certificate_replay_does_not_run_normal_form_solvers(monkeypatch):
    import theorems.mixed_abelian_readout as readout
    import theorems.pilot_submodule as pilot
    result = recover_annihilator(prime=3, ambient_exponents=(2, 3), fourier_labels=[(3, 3)])

    def fail(*args, **kwargs):
        pytest.fail("certificate replay recompiled a normal form")

    monkeypatch.setattr(readout, "compile_pilot_frame", fail)
    monkeypatch.setattr(pilot, "smith_normal_decomp", fail)
    assert verify_annihilator(result)
    assert result.certificate()["certificate_verified"]


@pytest.mark.parametrize("field", ["dual_basis", "canonical_transform", "ambient_relations", "label_pairings"])
def test_mutated_duality_certificate_is_rejected(field):
    result = recover_annihilator(prime=3, ambient_exponents=(2, 3), fourier_labels=[(3, 3)])
    certificate = result.duality_certificate
    rows = [list(row) for row in getattr(certificate, field)]
    rows[0][0] += 1
    broken = replace(certificate, **{field: tuple(tuple(row) for row in rows)})
    with pytest.raises((ArithmeticError, ValueError)):
        verify_annihilator(replace(result, duality_certificate=broken))


@pytest.mark.parametrize("changes", [
    {"lattice_basis": ((1, 0), (0, 1))},
    {"generator_columns": ((0, 0), (0, 0))},
    {"subgroup_order": 1}, {"observed_span_order": 1},
    {"fourier_labels": ()}, {"prime": 5},
    {"observed_span_only": False},
    {"hidden_subgroup_recovery_certified": True}, {"source_law_certified": True},
])
def test_mutated_result_is_rejected(changes):
    result = recover_annihilator(prime=3, ambient_exponents=(2, 3), fourier_labels=[(3, 3)])
    with pytest.raises((ArithmeticError, ValueError)):
        verify_annihilator(replace(result, **changes))


@pytest.mark.parametrize("changes", [
    {"prime": True}, {"prime": 3.0}, {"prime": 1}, {"prime": 2}, {"prime": 9},
    {"ambient_exponents": ()}, {"ambient_exponents": (0,)},
    {"ambient_exponents": (-1,)}, {"ambient_exponents": (True,)},
    {"ambient_exponents": (2.0,)}, {"ambient_exponents": None},
    {"ambient_exponents": "2"}, {"fourier_labels": None},
    {"fourier_labels": ""}, {"fourier_labels": {}},
    {"fourier_labels": [None]}, {"fourier_labels": [3]},
    {"fourier_labels": [(True,)]}, {"fourier_labels": [(1.0,)]},
    {"fourier_labels": [(Fraction(1),)]}, {"fourier_labels": [("1",)]},
    {"fourier_labels": [(-1,)]}, {"fourier_labels": [(9,)]},
    {"fourier_labels": [(1, 2)]}, {"fourier_labels": [()]},
])
def test_malformed_or_noncanonical_inputs_rejected(changes):
    kwargs = dict(prime=3, ambient_exponents=(2,), fourier_labels=[(3,)])
    kwargs.update(changes)
    with pytest.raises(ValueError):
        recover_annihilator(**kwargs)


def test_iterable_inputs_are_materialized_once_without_changing_coordinates():
    result = recover_annihilator(prime=3, ambient_exponents=iter([1, 2]),
                                 fourier_labels=(iter(label) for label in [(1, 3), (2, 6)]))
    assert result.ambient_exponents == (1, 2)
    assert result.fourier_labels == ((1, 3), (2, 6))
    assert verify_annihilator(result)


def test_modal_token_counts_aborts_and_rejects_ties():
    a = ((1, 0), (0, 1))
    b = ((3, 0), (0, 9))
    assert canonical_modal_token([]) is None
    assert canonical_modal_token([None]) is None
    assert canonical_modal_token([a, None, None]) is None
    assert canonical_modal_token([a, None]) is None
    assert canonical_modal_token([a, b]) is None
    assert canonical_modal_token([a, a, b, b, None]) is None
    assert canonical_modal_token(iter([a, a, b, None])) == a
    assert canonical_modal_token([a, b, b]) == b


@pytest.mark.parametrize("token", [
    (), ((0,),), ((-1,),), ((True,),), ((1.0,),),
    ((1, 1), (0, 1)), ((3, 0), (3, 1)), ((1, 0),), [[1]],
])
def test_modal_token_rejects_noncanonical_or_arbitrary_bases(token):
    with pytest.raises(ValueError):
        canonical_modal_token([token])


def test_modal_tokens_require_same_ambient_rank():
    with pytest.raises(ValueError):
        canonical_modal_token([((1,),), ((1, 0), (0, 1))])
