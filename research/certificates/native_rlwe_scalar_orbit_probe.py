"""Exact scalar-orbit generator obstruction and kernel-coordinate controls.

LOCAL DERIVATION / REVIEW PENDING. Covers two fixed native R-lines, NOT
cross-block mixtures, changed lifts, every quantum algorithm or hardness.
Uses one saved native d64 kernel and small identity/counterexample controls.
No source prior/noise sampler or unit-group oracle is implemented.
"""

import argparse
import json
import math
import random
from collections import Counter
from pathlib import Path

import sympy as sp
from flint import fmpz_mat


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--save', action='store_true')
args = parser.parse_args()
directory = Path(__file__).parent
rng = random.Random(290955)
counts = Counter()


def convolution(a):
    d = len(a)
    return sp.Matrix([[a[(i-j) % d]*(1 if i >= j else -1) for j in range(d)]
                       for i in range(d)])


def gram_schmidt(B):
    out = []
    for j in range(B.cols):
        v = B.col(j)
        for w in out:
            v -= w*(B.col(j).dot(w)/w.dot(w))
        assert v.dot(v) > 0
        out.append(v)
    return [v.dot(v) for v in out]


def native_completion_multiplier(f, k):
    d = len(f)
    J = convolution(f).row_join(-convolution(k))
    rows = fmpz_mat([[int(v) for v in J.T.row(i)] for i in range(2*d)])
    Hrows, U = rows.hnf(transform=True)
    assert U*rows == Hrows and abs(int(U.det())) == 1
    assert all(Hrows[i, j] == 0 for i in range(d, 2*d) for j in range(d))
    H = sp.Matrix([[int(Hrows[j, i]) for j in range(d)] for i in range(d)])
    coords = H.inv()*sp.eye(d).col(0)
    delta = math.lcm(*(int(v.q) for v in coords))
    top = sp.Matrix([[int(U[i, j]) for j in range(2*d)] for i in range(d)])
    answer = delta*top.T*coords
    assert all(v.q == 1 for v in answer)
    assert J*answer == delta*sp.eye(d).col(0)
    return delta, answer[:d, :], answer[d:, :]


for d in (4, 8):
    Cu = convolution([1, 1, 1]+[0]*(d-3))
    assert Cu.det() == 1
    for q in (17, 257):
        for replicate in range(2):
            m = [rng.randrange(-q//2+1, q//2+1) for _ in range(d)]
            M = convolution(m)
            B = (q*sp.eye(d)).row_join(-M).col_join(sp.zeros(d).row_join(sp.eye(d)))
            assert abs(int(B.det())) == q**d
            A_m = M.T*M+sp.eye(d)
            for a in (-2, 0, 2):
                for b in (-2, 0, 2):
                    Ua, Ub = Cu**a, Cu**b
                    change = sp.diag(Ua, Ub)
                    rotated = B*change
                    assert all(v.q == 1 for v in rotated)
                    assert abs(int(rotated.det())) == q**d
                    for swapped in (False, True):
                        C = rotated[:, d:].row_join(rotated[:, :d]) if swapped else rotated
                        first_gram = C[:, :d].T*C[:, :d]
                        invariant = A_m.det() if swapped else q**(2*d)
                        assert first_gram.det() == invariant
                        lengths = gram_schmidt(C)
                        assert sp.prod(lengths[:d]) == invariant
                        assert sp.prod(lengths[d:]) == sp.Rational(q**(2*d), invariant)
                        assert (sum(lengths[:d])/d)**d >= invariant
                        assert (sum(lengths[d:])/d)**d >= sp.Rational(q**(2*d), invariant)
                        counts['unit_prefix_and_gs_controls'] += 1
            # Nonunit scalar multiples cannot lower first-block Gram volume.
            for h in ([2]+[0]*(d-1), [1, 2]+[0]*(d-2)):
                Ch = convolution(h)
                transformed = Ch.T*A_m*Ch
                assert transformed.det() == A_m.det()*Ch.det()**2
                assert (transformed.trace()/d)**d >= transformed.det() >= A_m.det()
                counts['nonunit_scalar_volume_controls'] += 1

# Units really can repair SHAPE when the orbit already has small volume.
d = 4
Cu = convolution([1, 1, 1, 0])
bad = Cu**8
A_bad = 2*bad.T*bad
inverse = Cu**-8
A_repaired = inverse.T*A_bad*inverse
assert A_repaired == 2*sp.eye(d)
assert A_bad.det() == A_repaired.det() == 2**d
shape_energy_ratio = A_bad.trace()/A_repaired.trace()
assert shape_energy_ratio == 665857
counts['unit_shape_repair_counterexample'] += 1

# Completing in output coordinates can overcharge the needed multiplier.
for d in (2, 4, 8):
    q = 17
    m = [rng.randrange(q) for _ in range(d)]
    M = convolution(m)
    f = [0]*d
    k = [1]+[0]*(d-1)
    delta, z, F = native_completion_multiplier(f, k)
    G = M*F+q*z
    assert delta == 1
    assert convolution(f)*G-q*convolution(k)*F == q*sp.eye(d).col(0)
    assert all(v % q == 0 for v in G-M*F)
    # Ambient ideal (q,0) has integer order q, not the native order 1.
    ambient_delta, _, _ = native_completion_multiplier([0]*d, [q]+[0]*(d-1))
    assert ambient_delta == q
    counts['ambient_vs_native_completion_controls'] += 1
    for case in range(2):
        f = [1]+[rng.randrange(-2, 3) for _ in range(d-1)]
        k = [rng.randrange(-2, 3) for _ in range(d)]
        H = convolution([rng.randrange(-2, 3) for _ in range(d)])
        adjusted = sp.Matrix(k)-H*sp.Matrix(f)
        delta_before, _, _ = native_completion_multiplier(f, k)
        delta_after, _, _ = native_completion_multiplier(f, list(adjusted))
        assert delta_before == delta_after
        # M -> M+qH changes k -> k-Hf, but not the native-coordinate ideal.
        g = M*sp.Matrix(f)+q*sp.Matrix(k)
        assert g-(M+q*H)*sp.Matrix(f) == q*adjusted
        counts['native_ideal_lift_invariance_controls'] += 1

source = json.loads((directory/'native_rlwe_babai_profile_d64.json').read_text())
d, q = source['d'], int(source['q'])
centered = [(int(v)+q//2) % q-q//2 for v in source['native_ratio']]
Msp = convolution(centered).T
M = fmpz_mat([[int(v) for v in Msp.row(i)] for i in range(d)])
A_m = M.transpose()*M+fmpz_mat([[int(i == j) for j in range(d)] for i in range(d)])
det_m = int(A_m.det())
lanes = []
for lane in source['lanes']:
    E, t = int(lane['error_norm']), int(lane['chosen_label'])
    q_line_rejected = q*q*E*E >= t*t
    m_line_rejected = det_m*(E*E)**d >= t**(2*d)
    assert q_line_rejected and m_line_rejected
    lanes.append(dict(lane=lane['lane'], error_norm=str(E), label=str(t),
                      q_line_scalar_orbit_rejected=q_line_rejected,
                      centered_m_line_scalar_orbit_rejected=m_line_rejected))

row = [int(v) for v in source['reduced_row_basis'][0]]
g, f = sp.Matrix(row[:d]), -sp.Matrix(row[d:])
k = (g-Msp*f)/q
assert all(v.q == 1 for v in k)
assert any(f) and any(k)
counts['classical_lll_cross_block_escape'] += 1

# Easy labels prevent turning the finite obstruction into an ensemble theorem.
easy = convolution([0]*d)
assert (easy.T*easy+sp.eye(d)).det() == 1
assert all(int(lane['error_norm'])**(2*d) < int(lane['chosen_label'])**(2*d)
           for lane in source['lanes'])
counts['easy_label_nonobstruction_control'] += 1

output = dict(status='LOCAL_DERIVATION_REVIEW_PENDING', seed=290955,
              scope='two_fixed_native_scalar_lines_not_cross_block_mixing',
              quantum_algorithm=False, asymptotic_hardness_bound=False,
              source_noise_and_prior_laws_sampled=False,
              d=d, q=str(q), basis_lift='centered',
              parent_certificate='native_rlwe_babai_profile_d64.json',
              centered_m_line_gram_determinant=str(det_m), counts=dict(counts), lanes=lanes)
output['shape_control_exact_energy_ratio'] = str(shape_energy_ratio)
if args.save:
    (directory/'native_rlwe_scalar_orbit_d64.json').write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps({key: output[key] for key in ('status', 'scope', 'counts', 'lanes')}, indent=2))
