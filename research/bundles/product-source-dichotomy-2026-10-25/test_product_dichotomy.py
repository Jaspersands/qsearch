"""No small finite fixture is accepted as a hard algorithm candidate."""

from pathlib import Path
import sys

import pytest
from sympy import Matrix, eye, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_controls import run_control, source_fixture
from product_dichotomy import (
    action, classify_projectors, mod, product_actions, restrict_weak_blocks,
    standard_projectors,
)
from pullback import reconstruct_pullbacks


@pytest.mark.parametrize("kind,ranks,routing", [
    ("mixed", [2, 2], []), ("diagonal", [0, 0], [0, 1]),
    ("permuted", [0, 0], [1, 0]),
])
def test_complete_dichotomy_from_masked_legal_levels(kind, ranks, routing):
    record = run_control(kind)
    assert record["ranks"] == ranks
    assert record["target_to_source"] == routing
    assert record["exact_pullbacks_match"]
    assert record["crt_modulus"] > 2*record["pairing_bound"]
    assert not record["hidden_prime_weak_query"]
    assert not record["geometric_input_verified"]
    assert not record["elliptic_backend_executed"]
    assert not record["classical_hardness_established"]
    if routing:
        assert record["kernel_dimension"] is None
        assert record["status"] == "TWO_ELLIPTIC_WEAK_INSTANCES"
        assert record["masked_elliptic_block_checks"] > 0
    else:
        assert record["kernel_dimension"] == 2
        assert record["status"] == "CLASSICAL_KERNEL_UNDER_INPUT_PROMISE"


def test_insufficient_access_rejected_before_queries():
    source = source_fixture("mixed")
    with pytest.raises(ValueError, match="insufficient CRT"):
        reconstruct_pullbacks(source.order, 5, 11, (2, 2), (3,),
                              source.split, source.observe, max_auxiliary_prime=47)
    assert source.calls == []


@pytest.mark.parametrize("mutation", ["sum", "self_adjoint", "rank", "idempotent"])
def test_reject_inconsistent_exact_projector_claims(mutation):
    source = source_fixture("mixed")
    a, b = [x.copy() for x in source.reference_pullbacks()]
    e0, e1 = standard_projectors(source.order)
    if mutation == "sum":
        a += e0
    elif mutation == "self_adjoint":
        delta = zeros(16, 1)
        delta[4] = 1
        a, b = a+delta, b-delta
    elif mutation == "rank":
        a, b = zeros(16, 1), 5*(e0+e1)
    else:
        a, b = 2*e0+3*e1, 3*e0+2*e1
    with pytest.raises(ValueError):
        classify_projectors(source.order, 5, source.split(5), (a, b))


@pytest.mark.parametrize("ell", [2, 9, True])
def test_prime_scope(ell):
    source = source_fixture("mixed")
    with pytest.raises(ValueError, match="odd prime"):
        classify_projectors(source.order, ell, source.split(5), source.reference_pullbacks())


def test_reject_unfaithful_source_chart():
    source = source_fixture("diagonal")
    with pytest.raises(ValueError):
        classify_projectors(source.order, 5, (eye(2),)*4, source.reference_pullbacks())


def test_masks_preserved_not_normalized_or_decoupled():
    source = source_fixture("permuted")
    r = 7
    exact = mod(action(source.phi, product_actions(source.split(r))), r)
    for unit in range(1, r):
        blocks = restrict_weak_blocks(unit*exact, r, (1, 0))
        assert blocks[0] == mod(unit*exact[:2, 2:], r)
        assert blocks[1] == mod(unit*exact[2:, :2], r)
        assert blocks[0].det() % r == unit*unit*source.ell % r
        assert blocks[1].det() % r == unit*unit*source.ell % r


@pytest.mark.parametrize("routing", [(0, 0), (True, 0), (0,), (2, 0)])
def test_bad_routing_rejected(routing):
    with pytest.raises(ValueError, match="permutation"):
        restrict_weak_blocks(eye(4), 7, routing)


def test_mixed_response_cannot_enter_elliptic_branch():
    source = source_fixture("mixed")
    with pytest.raises(ValueError, match="routing"):
        restrict_weak_blocks(source.observe(7).weak_action, 7, (0, 1))


def test_singular_elliptic_block_rejected():
    with pytest.raises(ValueError, match="invertible"):
        restrict_weak_blocks(Matrix.diag(1, 0, 1, 1), 7, (0, 1))


def test_unpolarized_decomposition_is_not_product_polarization():
    source = source_fixture("mixed")
    e0, e1 = standard_projectors(source.order)
    off_diagonal = zeros(16, 1)
    off_diagonal[4:8, :] = source.order.unit
    # Conjugating coordinate projections by a nonunitary shear preserves
    # integrality/idempotence, but not the required Rosati adjunction.
    source.gammas = (e0-off_diagonal, e1+off_diagonal)
    with pytest.raises(ValueError, match="self-adjoint"):
        classify_projectors(source.order, 5, source.split(5), source.reference_pullbacks())
