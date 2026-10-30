"""Bounded, independent falsifiers for the canonical-valid-subspace hybrid.

Tested claim: for the explicit two-stage unitaries below, ideal prefixes stay
in the canonical image of J and the joint system-reference output trace
distance is at most sum_i ||A_i J - J F_i||_op, despite actual-prefix leakage.
Additional controls distinguish basis-state densities from coherent action,
base channels from controlled unitaries, clean isometries from output-only
agreement, and label marginals from complete cq instruments.

All sizes and inputs are fixed. These numerical examples neither prove the
general hybrid theorem nor validate a Rees implementation, uniform circuit
generation, primitive counts, or scalable synthesis. No production code is
imported. Unitary errors retain phase; density distances ignore only genuine
global phase, never relative phase introduced by coherent control.
"""

import numpy as np
import pytest


ATOL = 1e-12
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def _density(ket):
    return np.outer(ket, ket.conj())


def _op_norm(matrix):
    return float(np.linalg.norm(matrix, ord=2))


def _trace_distance(left, right):
    difference = left - right
    np.testing.assert_allclose(difference, difference.conj().T, atol=ATOL)
    return float(np.abs(np.linalg.eigvalsh(difference)).sum() / 2)


def _assert_unitary(matrix):
    np.testing.assert_allclose(
        matrix.conj().T @ matrix, np.eye(len(matrix)), atol=ATOL
    )


def _extend(logical):
    extended = np.eye(3, dtype=complex)
    extended[:2, :2] = logical
    return extended


def _rotation(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s], [s, c]], dtype=complex)


@pytest.mark.parametrize("theta", [0.17, 0.43])
@pytest.mark.parametrize("mixed", [False, True])
def test_two_stage_canonical_hybrid_with_leakage_and_joint_reference(theta, mixed):
    j = np.eye(3, dtype=complex)[:, :2]
    invalid = np.eye(3) - j @ j.conj().T
    f1, f2 = H, np.diag([1, 1j])
    v1, v2 = _extend(f1), _extend(f2)
    leakage = np.eye(3, dtype=complex)
    leakage[np.ix_([0, 2], [0, 2])] = _rotation(theta)
    a1 = leakage @ v1
    a2 = v2 @ np.diag([1, 1, -1])
    for unitary in (v1, v2, a1, a2):
        _assert_unitary(unitary)
    np.testing.assert_allclose(j.conj().T @ j, np.eye(2), atol=ATOL)

    prefix = j
    for ideal in (v1, v2):
        prefix = ideal @ prefix
        np.testing.assert_allclose(invalid @ prefix, 0, atol=ATOL)
    errors = [_op_norm(a1 @ j - j @ f1), _op_norm(a2 @ j - j @ f2)]
    assert errors[0] == pytest.approx(2 * np.sin(theta / 2), abs=ATOL)
    assert errors[1] == pytest.approx(0, abs=ATOL)
    assert _op_norm(a2 - v2) == pytest.approx(2, abs=ATOL)
    assert _op_norm(invalid @ a1 @ j) == pytest.approx(np.sin(theta), abs=ATOL)

    # Ideal-prefix telescoping works; substituting the actual prefix does not
    # let one declare the second-stage contribution zero.
    late_ideal_term = (a2 - v2) @ v1 @ j
    np.testing.assert_allclose(late_ideal_term, 0, atol=ATOL)
    np.testing.assert_allclose(
        (a2 @ a1 - v2 @ v1) @ j,
        a2 @ (a1 - v1) @ j + late_ideal_term,
        atol=ATOL,
    )
    assert _op_norm((a2 - v2) @ a1 @ j) == pytest.approx(
        2 * np.sin(theta), abs=ATOL
    )

    # Tensor order is system then reference; the reference is never traced out.
    bell = np.array([1, 0, 0, 1j], dtype=complex) / np.sqrt(2)
    logical_rho = _density(bell)
    if mixed:
        logical_rho = 0.7 * logical_rho + 0.3 * np.eye(4) / 4
    embedding = np.kron(j, np.eye(2))
    rho = embedding @ logical_rho @ embedding.conj().T

    def evolve(system_unitary):
        joint = np.kron(system_unitary, np.eye(2))
        return joint @ rho @ joint.conj().T

    actual, ideal = evolve(a2 @ a1), evolve(v2 @ v1)
    for state in (actual, ideal):
        assert np.trace(state) == pytest.approx(1, abs=ATOL)
        assert np.linalg.eigvalsh(state).min() >= -ATOL
    distance = _trace_distance(actual, ideal)
    assert 0.05 < distance <= sum(errors) + ATOL
    first_output = evolve(a1)
    invalid_weight = np.trace(np.kron(invalid, np.eye(2)) @ first_output).real
    assert invalid_weight == pytest.approx(np.sin(theta)**2 / 2, abs=ATOL)
    # This is a density-level distinction, not a spurious global-phase defect.
    assert _trace_distance(actual, evolve(v2 @ a1)) > 0.1


def test_h_and_hz_basis_densities_agree_but_plus_outputs_are_orthogonal():
    hz = H @ Z
    for basis in np.eye(2, dtype=complex):
        left, right = _density(H @ basis), _density(hz @ basis)
        np.testing.assert_allclose(left, right, atol=ATOL)
        np.testing.assert_allclose(np.diag(left), np.diag(right), atol=ATOL)
    plus = np.ones(2, dtype=complex) / np.sqrt(2)
    left, right = H @ plus, hz @ plus
    assert abs(np.vdot(left, right)) < ATOL
    assert _trace_distance(_density(left), _density(right)) == pytest.approx(1)
    np.testing.assert_allclose(np.abs(left)**2, [1, 0], atol=ATOL)
    np.testing.assert_allclose(np.abs(right)**2, [0, 1], atol=ATOL)


def test_identity_global_phase_is_invisible_until_coherently_controlled():
    identity = np.eye(2, dtype=complex)
    # Matrix units span all input operators, so this is base-channel equality,
    # not merely equality on computational-basis input states.
    for row in range(2):
        for column in range(2):
            operator = np.zeros((2, 2), dtype=complex)
            operator[row, column] = 1
            np.testing.assert_allclose(
                identity @ operator @ identity.conj().T,
                (-identity) @ operator @ (-identity).conj().T,
                atol=ATOL,
            )
    assert _op_norm(identity - (-identity)) == pytest.approx(2)
    p0, p1 = np.diag([1, 0]), np.diag([0, 1])
    controlled_i = np.kron(p0, identity) + np.kron(p1, identity)
    controlled_minus_i = np.kron(p0, identity) + np.kron(p1, -identity)
    plus = np.ones(2, dtype=complex) / np.sqrt(2)
    source = np.kron(plus, np.array([1, 0], dtype=complex))
    left, right = controlled_i @ source, controlled_minus_i @ source
    assert abs(np.vdot(left, right)) < ATOL
    assert _trace_distance(_density(left), _density(right)) == pytest.approx(1)


@pytest.mark.parametrize("work_angle", [0.0, 0.11])
def test_clean_forward_and_adjoint_restricted_operator_errors_match(work_angle):
    zero = np.array([[1], [0]], dtype=complex)
    j = np.kron(np.eye(2), zero)
    f = H @ np.diag([1, 1j])
    actual = np.kron(_rotation(0.19) @ f, _rotation(work_angle))
    _assert_unitary(actual)
    _assert_unitary(f)
    forward = actual @ j - j @ f
    backward = actual.conj().T @ j - j @ f.conj().T
    np.testing.assert_allclose(
        backward, -actual.conj().T @ forward @ f.conj().T, atol=ATOL
    )
    assert 0.1 < _op_norm(forward) < 0.4
    assert _op_norm(backward) == pytest.approx(_op_norm(forward), abs=ATOL)


def test_dirty_work_output_channel_equality_does_not_certify_clean_inverse():
    zero, one = np.eye(2, dtype=complex)
    j = np.kron(np.eye(2), zero[:, None])
    dirty_j = np.kron(np.eye(2), one[:, None])
    # On clean work this preserves every data state but sets work to one.
    # Its other work sector flips data, making its inverse on clean work wrong.
    actual = np.kron(np.eye(2), np.outer(one, zero)) + np.kron(
        X, np.outer(zero, one)
    )
    _assert_unitary(actual)
    np.testing.assert_allclose(actual @ j, dirty_j, atol=ATOL)
    np.testing.assert_allclose(actual.conj().T @ j, dirty_j @ X, atol=ATOL)
    assert _op_norm(actual @ j - j) == pytest.approx(np.sqrt(2))

    def data_density(joint_ket):
        joint_rho = _density(joint_ket).reshape(2, 2, 2, 2)
        return np.trace(joint_rho, axis1=1, axis2=3)

    for data in (zero, one, np.array([1, 1j]) / np.sqrt(2)):
        np.testing.assert_allclose(
            data_density(actual @ j @ data), _density(data), atol=ATOL
        )
    reversed_output = actual.conj().T @ j @ zero
    assert _trace_distance(data_density(reversed_output), _density(zero)) == (
        pytest.approx(1)
    )
    np.testing.assert_allclose(actual.conj().T @ actual @ j, j, atol=ATOL)


def test_p3_character_instrument_and_dummy_have_same_labels_not_same_cq_state():
    p = 3
    indices = np.arange(p)
    characters = np.exp(2j * np.pi * np.outer(indices, indices) / p) / np.sqrt(p)
    _assert_unitary(characters)
    rho = np.eye(p, dtype=complex) / p
    measured = np.zeros((p * p, p * p), dtype=complex)
    dummy = np.zeros_like(measured)
    for label in range(p):
        projector = _density(characters[:, label])
        label_projector = _density(np.eye(p)[label])
        branch = projector @ rho @ projector
        assert np.trace(branch) == pytest.approx(1 / p, abs=ATOL)
        measured += np.kron(label_projector, branch)
        # Uniform classical label independent of the unchanged data register.
        dummy += np.kron(label_projector, rho / p)
    for state in (measured, dummy):
        assert np.trace(state) == pytest.approx(1, abs=ATOL)
        assert np.linalg.eigvalsh(state).min() >= -ATOL
        tensor = state.reshape(p, p, p, p)
        np.testing.assert_allclose(
            np.trace(tensor, axis1=1, axis2=3), np.eye(p) / p, atol=ATOL
        )
        np.testing.assert_allclose(
            np.trace(tensor, axis1=0, axis2=2), rho, atol=ATOL
        )
    assert _trace_distance(measured, dummy) == pytest.approx(1 - 1 / p, abs=ATOL)
