"""Source/access falsifiers, not a symmetry-learning algorithm benchmark."""
from fractions import Fraction
from itertools import permutations

import numpy as np
import pytest

from theorems.state_symmetry_coset_transfer import plan_orbit_state_transfer


def permutation_matrix(permutation):
    return np.eye(len(permutation))[:, permutation]


def trace_distance(left, right):
    return np.linalg.norm(left-right, ord='nuc')/2


def test_actual_nonabelian_controlled_action_and_tensor_source_kernel():
    action = [permutation_matrix(p) for p in permutations(range(3))]
    psi = np.array([2, 1, 1])/np.sqrt(6)
    orbits = np.array([r@psi for r in action]).T
    labels = np.array([np.kron(v, v) for v in orbits.T]).T
    gram = orbits.T.conj()@orbits
    assert np.allclose(labels.T.conj()@labels, gram**2)
    # Trace actual label registers of the coherent uniform-address source.
    joint = labels.T/np.sqrt(6)
    reduced = joint@joint.conj().T
    assert np.allclose(reduced, (gram**2).T/6)
    cosets = np.argmax(orbits, axis=0)
    ideal = (cosets[:, None] == cosets[None, :])/6
    assert np.allclose(gram[cosets[:, None] != cosets[None, :]], 5/6)
    for k in (1, 2, 4, 12):
        actual = (gram**k).T/6
        assert trace_distance(actual, ideal) <= np.sqrt(6)*(5/6)**k/2+1e-12
    # H fixes position zero but is not normal in S3.
    h, g = permutation_matrix((0, 2, 1)), permutation_matrix((1, 0, 2))
    assert np.allclose(h@psi, psi)
    assert not np.allclose(g@h@g.T@psi, psi)


def test_mixed_copy_source_has_the_same_kernel_without_purification_access():
    action = [permutation_matrix(p) for p in permutations(range(3))]
    e, u = np.eye(3)[:, 0], np.ones(3)/np.sqrt(3)
    rho = 0.7*np.outer(e, e)+0.3*np.outer(u, u)
    kernel = np.array([[np.trace(rho@b.T@a) for b in action] for a in action])
    cosets = [np.argmax(a@e) for a in action]
    expected = np.array([[1 if a == b else 0.3 for b in cosets] for a in cosets])
    assert np.allclose(kernel, expected)
    # Construct and trace the actual controlled-action mixed source.
    joint = np.block([[a@rho@b.T/6 for b in action] for a in action])
    reduced = np.trace(joint.reshape(6, 3, 6, 3), axis1=1, axis2=3)
    assert np.allclose(reduced, kernel/6)


def test_quotient_representatives_need_not_act_as_a_representation_everywhere():
    # G=S3 x C2, K=C2 fixes this source but not the whole workspace.
    permutations3 = list(permutations(range(3)))
    psi = np.kron(np.array([2, 1, 1])/np.sqrt(6), np.array([1, 0]))
    z = np.diag([1, -1])
    representatives = [np.kron(permutation_matrix(p),
                               z if p[0] == 1 else np.eye(2))
                       for p in permutations3]
    labels = np.array([r@psi for r in representatives]).T
    original = np.array([permutation_matrix(p)@np.array([2, 1, 1])/np.sqrt(6)
                         for p in permutations3]).T
    assert np.allclose(labels.T@labels, original.T@original)
    failures = []
    for i, p in enumerate(permutations3):
        for j, q in enumerate(permutations3):
            product = tuple(p[q[k]] for k in range(3))
            r = representatives[permutations3.index(product)]
            failures.append(not np.allclose(representatives[i]@representatives[j], r))
            assert np.allclose(representatives[i]@representatives[j]@psi, r@psi)
    assert any(failures)


def test_correct_copy_marginals_do_not_supply_the_tensor_power_kernel():
    rho, z = np.eye(2)/2, np.diag([1, -1])
    correlated = np.diag([0.5, 0, 0, 0.5])
    marginal = np.trace(correlated.reshape(2, 2, 2, 2), axis1=1, axis2=3)
    assert np.allclose(marginal, rho)
    assert np.trace(rho@z)**2 == 0
    assert np.trace(correlated@np.kron(z, z)) == 1
    # IID copies would hide the trivial subgroup of C2; this correlated
    # batch falsely makes the nonidentity element look like a symmetry.


def test_polar_comparison_has_close_full_unitary_completions():
    gram = np.array([[1, 0.01j, 0.02], [-0.01j, 1, -0.03j],
                     [0.02, 0.03j, 1]], dtype=complex)
    values, vectors = np.linalg.eigh(gram)
    labels = (vectors*np.sqrt(values))@vectors.conj().T
    target = np.eye(3, dtype=complex)
    radius = np.linalg.norm(gram-target, ord=2)
    assert radius < 1
    assert np.linalg.norm(labels-target, ord=2) <= radius
    for v, y in zip(labels.T, target.T):
        cosine = np.vdot(v, y).real
        assert abs(np.vdot(v, y).imag) < 1e-12 and cosine > 0
        sine = np.sqrt(1-cosine**2)
        u = (y-cosine*v)/sine
        rotation = target+(cosine-1)*(np.outer(v, v.conj())+np.outer(u, u.conj()))
        rotation += sine*(np.outer(u, v.conj())-np.outer(v, u.conj()))
        assert np.allclose(rotation@v, y)
        assert np.allclose(rotation.conj().T@rotation, target)
        assert np.linalg.norm(rotation-target, ord=2) <= radius+1e-12


def test_conjugate_pair_works_but_inverse_pair_breaks_nonnormal_cosets():
    psi = np.eye(3)[:, 0]
    g, h = permutation_matrix((1, 0, 2)), permutation_matrix((0, 2, 1))
    other = g@h
    assert np.allclose(g@psi, other@psi)
    bad_left = np.kron(g@psi, g.T@psi)
    bad_right = np.kron(other@psi, other.T@psi)
    assert np.vdot(bad_left, bad_right) == 0
    good_left = np.kron(g@psi, g.conj()@psi.conj())
    good_right = np.kron(other@psi, other.conj()@psi.conj())
    assert np.allclose(good_left, good_right)
    phases = np.exp(1j*np.array([0.3, 0.7, -0.2]))
    vectors = [phase*r@np.array([1, 1j, 2])/np.sqrt(6)
               for phase, r in zip(phases, (np.eye(3), g, other))]
    for a in vectors:
        for b in vectors:
            assert np.allclose(np.vdot(np.kron(a, a.conj()), np.kron(b, b.conj())),
                               abs(np.vdot(a, b))**2)


def test_phase_graph_does_not_inherit_an_absolute_overlap_gap():
    # R(g)=1 on a one-dimensional state: every g is projectively symmetric.
    # In G x Z_p, (identity,1) is outside the exact phase graph but has
    # overlap of modulus one. Tensor powers cannot remove this defect.
    p = 7
    phase = np.exp(-2j*np.pi/p)
    assert not np.allclose(phase, 1)
    assert np.isclose(abs(phase), 1)
    assert np.isclose(abs(phase**100), 1)
    pair = phase*phase.conjugate()
    assert np.isclose(pair, 1)  # This learns projective, not Bose, symmetry.


def test_filtering_phase_zero_generators_is_not_subgroup_intersection():
    # Generators (1,1),(2,1) of an additive subgroup of F5^2 both have
    # nonzero phase coordinate, yet their difference (4,0) is in the kernel.
    generators = ((1, 1), (2, 1))
    assert not [g for g in generators if g[1] == 0]
    assert tuple((a-b) % 5 for a, b in zip(*generators)) == (4, 0)


def test_small_gap_and_mixed_conjugation_are_not_free_extensions():
    overlap = Fraction(2**20-1, 2**20)
    assert overlap**16/2 > Fraction(49, 100)
    rho, z = np.eye(2)/2, np.diag([1, -1])
    assert np.allclose(z@rho@z, rho)
    assert np.trace(z@rho) == 0  # rho tensor rho* does NOT learn this commutant.


def test_exact_budget_charges_gap_all_calls_and_conjugate_preparation():
    plan = plan_orbit_state_transfer(2**1000, Fraction(1, 7), 10**80,
                                    Fraction(1, 10**9), projective_pair=True,
                                    conjugate_access=True)
    assert plan.copies_per_label == 7*plan.overlap_bits
    assert plan.preparations_per_label == 2*plan.copies_per_label
    assert plan.total_preparation_uses_bound == 10**80*plan.preparations_per_label
    assert plan.hybrid_error_bound <= plan.error_budget/4
    small = plan_orbit_state_transfer(6, Fraction(1, 4), 3)
    assert Fraction(3, 4)**small.copies_per_label <= Fraction(1, 2**small.overlap_bits)
    exact = plan_orbit_state_transfer(6, Fraction(1), 3)
    assert exact.copies_per_label == 1 and exact.hybrid_error_bound == 0
    more_calls = plan_orbit_state_transfer(6, Fraction(1, 4), 3000)
    worse_gap = plan_orbit_state_transfer(6, Fraction(1, 8), 3)
    assert more_calls.copies_per_label > small.copies_per_label
    assert worse_gap.copies_per_label == 2*small.copies_per_label


@pytest.mark.parametrize('args,kwargs', [
    ((0, Fraction(1, 4), 1), {}), ((True, Fraction(1, 4), 1), {}),
    ((6, 0.25, 1), {}), ((6, Fraction(0), 1), {}),
    ((6, Fraction(2), 1), {}), ((6, Fraction(1, 4), 0), {}),
    ((6, Fraction(1, 4), 1, 0.1), {}),
    ((6, Fraction(1, 4), 1), {'projective_pair': True}),
    ((6, Fraction(1, 4), 1), {'conjugate_access': 'yes'}),
])
def test_invalid_or_unpaid_promises_are_rejected(args, kwargs):
    with pytest.raises(ValueError):
        plan_orbit_state_transfer(*args, **kwargs)
