from copy import deepcopy
import random

from flint import fmpz_mod_poly_ctx
import pytest

from theorems.hermite_compact_decoder import DescendingSystem, module_interpolant
from theorems.hermite_module_certificate import (
    certify_basis, crt_reduced_basis, dense_identity_space, hilbert_checks,
    native_controls,
)


@pytest.mark.parametrize("q,ell,order,radius", [(5, 4, 1, 0), (7, 4, 1, 1),
                                             (13, 8, 2, 3)])
def test_independent_crt_basis_certifies_whole_module_and_hilbert_dimensions(q, ell, order, radius):
    rng = random.Random(q)
    received = [rng.randrange(q) for _ in range((q-1)*ell)]
    independent = crt_reduced_basis(q, ell, order, radius, received)
    certificate = certify_basis(q, ell, order, radius, received, independent["basis"])
    original = module_interpolant(q, ell, order, radius, received)
    assert certificate["full_module_certified"]
    assert certificate["determinant_degree"] == (q-1)*(ell-order)
    assert sorted(certificate["leading_pairs"]) == sorted(original["basis_leading_pairs"])
    a = independent["parameters"]["a"]
    checks = hilbert_checks(q, ell, order, radius, received, independent, [-1, 0, a-1, a, a+2])
    assert all(row["module_dimension"] == row["independent_dense_nullity"] for row in checks)


def test_valid_constraints_do_not_certify_a_complete_module():
    q, ell, order, radius = 7, 4, 1, 1
    received = list(range(q))*3+[1, 2, 3]
    basis = crt_reduced_basis(q, ell, order, radius, received)["basis"]
    ctx = fmpz_mod_poly_ctx(q)
    incomplete = deepcopy(basis)
    incomplete[0] = [[int(c) for c in (ctx(poly)*ctx([-2, 1])).coeffs()] for poly in incomplete[0]]
    negative = certify_basis(q, ell, order, radius, received, incomplete)
    assert negative["invalid_row_point_pairs"] == []
    assert negative["determinant_degree"] == negative["required_codimension"]+1
    assert negative["issues"] == ["DETERMINANT_CODIMENSION_MISMATCH"]
    duplicate = deepcopy(basis)
    duplicate[0] = deepcopy(duplicate[1])
    assert not certify_basis(q, ell, order, radius, received, duplicate)["full_module_certified"]
    malformed = deepcopy(basis)
    malformed[0][0] = [1] if not malformed[0][0] else [
        (malformed[0][0][0]+1) % q]+malformed[0][0][1:]
    assert "INVALID_LOCAL_INTERPOLATION_CONSTRAINT" in certify_basis(
        q, ell, order, radius, received, malformed)["issues"]


@pytest.mark.parametrize("q,k", [(3, 7), (5, 17), (7, 20)])
def test_independent_polynomial_identity_columns_match_descending_solver(q, k):
    rng = random.Random(q*k)
    for _ in range(6):
        operator = [[rng.randrange(q) for _ in range(4)] for _ in range(3)]
        pieces = [[], *operator]
        dense = dense_identity_space(q, k, pieces, {}, 2)
        compact = DescendingSystem(q, k, pieces).solve({}, 2)
        assert dense["dimension"] == compact["remaining_dimension"]
        if dense["dimension"] == 0:
            assert dense["unique_polynomial"] == compact["polynomial"]
    frobenius = [[], [], [1]]
    assert dense_identity_space(q, k, frobenius, {}, 2)["dimension"] == (k+q-1)//q


def test_identity_inconsistency_is_not_lost_after_nonzero_pivots():
    pieces = [[0, 0, 0, 1], [1]]
    assert not dense_identity_space(5, 3, pieces, {}, 2)["consistent"]
    assert DescendingSystem(5, 3, pieces).solve({}, 2)["status"] == "ABSTAIN_INCONSISTENT"
    pieces = [[], [1]]
    assert not dense_identity_space(5, 3, pieces, {0: [1, 0]}, 2)["consistent"]


def test_native_module_and_actual_decoder_identity_certificate():
    report = native_controls()
    replay = certify_basis(31, 24, 4, 10, report["received_word"], report["independent_basis"])
    assert replay == report["certificate"]
    assert report["certificate"]["full_module_certified"]
    assert report["certificate"]["determinant_degree"] == 600
    assert report["matches_original_leading_profile"]
    assert report["identity_unpinned"]["dimension"] == 1
    assert all(row["dimension"] == 0 for row in report["identity_pinned"])
    assert not report["incomplete_submodule_negative"]["full_module_certified"]
    assert report["new_quantum_algorithm_claim_allowed"] is False
