"""Check the saved native d64 profile and original-coordinate decoder.

LOCAL DERIVATION / REVIEW PENDING. Uses within-contract controls, not a
sampler for the spherical/hidden-elliptical source laws. No hidden values
enter witness construction or decoding. Requires optional python-flint.
"""

import argparse
import json
import math
import random
from pathlib import Path

from flint import fmpq, fmpq_mat, fmpz_mat


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--save', action='store_true')
args = parser.parse_args()
rng = random.Random(290954)
directory = Path(__file__).parent
payload = json.loads((directory/'native_rlwe_babai_profile_d64.json').read_text())
assert payload['basis_lift'] == 'centered'
d, q = payload['d'], int(payload['q'])
n = 2*d


def convolution(a):
    columns = [list(a)]
    for _ in range(1, len(a)):
        old = columns[-1]
        columns.append([-old[-1]]+old[:-1])
    return fmpz_mat([[columns[j][i] for j in range(len(a))] for i in range(len(a))])


def nearest_integer(x):
    return (2*int(x.p)+int(x.q))//(2*int(x.q))


def centered(x):
    return (int(x)+q//2) % q-q//2


R = fmpz_mat([[int(v) for v in row] for row in payload['reduced_row_basis']])
U = fmpz_mat([[int(v) for v in row] for row in payload['unimodular_transform']])
M_uncentered = convolution([int(v) for v in payload['native_ratio']]).transpose()
M = convolution([centered(v) for v in payload['native_ratio']]).transpose()
wrong_lift_columns = fmpz_mat([[q*(i==j) if j<d else -int(M_uncentered[i,j-d]) for j in range(n)]
                               if i<d else [int(i==j) for j in range(n)] for i in range(n)])
assert U*wrong_lift_columns.transpose() != R
native_columns = fmpz_mat([[q*(i==j) if j<d else -int(M[i,j-d]) for j in range(n)]
                           if i<d else [int(i==j) for j in range(n)] for i in range(n)])
assert U*native_columns.transpose() == R and abs(int(U.det())) == 1
public_normalized = fmpz_mat([[int(i==j) if j<d else int(M[i,j-d]) for j in range(n)] for i in range(d)])
assert all(int(v) % q == 0 for row in (public_normalized*R.transpose()).tolist() for v in row)

Gram = R*R.transpose()
A = [[int(Gram[i,j]) for j in range(n)] for i in range(n)]
L = fmpq_mat([[int(i==j) for j in range(n)] for i in range(n)])
previous = 1
ceilings = []
for k in range(n):
    pivot = A[k][k]
    assert pivot > 0
    ceilings.append((pivot+previous-1)//previous)
    for i in range(k+1, n):
        L[i,k] = fmpq(A[i][k], pivot)
    for i in range(k+1, n):
        for j in range(i, n):
            numerator = pivot*A[i][j]-A[i][k]*A[k][j]
            quotient, remainder = divmod(numerator, previous)
            assert not remainder
            A[i][j] = quotient
            A[j][i] = quotient
    previous = pivot
assert previous == q**(2*d)
assert [str(v) for v in ceilings] == payload['gs_squared_integer_upper']
Q = sum(ceilings)
assert str(Q) == payload['gs_squared_sum_upper']
R_transpose_inverse = fmpq_mat(R.transpose()).inv()


def preimage(section):
    beta = R_transpose_inverse*fmpq_mat([[v] for v in section])
    x = L.transpose()*beta
    coefficients = [0]*n
    for i in range(n-1, -1, -1):
        coefficient = nearest_integer(x[i,0])
        coefficients[i] = coefficient
        for j in range(i+1):
            x[j,0] -= coefficient*L[i,j]
    lattice = R.transpose()*fmpz_mat([[v] for v in coefficients])
    c = [section[i]-int(lattice[i,0]) for i in range(n)]
    assert 4*sum(v*v for v in c) <= Q
    return c


while True:
    a1 = [rng.randrange(q) for _ in range(d)]
    C1 = convolution(a1)
    if int(C1.det()) % q:
        break
a2_column = C1*fmpz_mat([[int(v)] for v in payload['native_ratio']])
a2 = [int(a2_column[i,0]) % q for i in range(d)]
C2 = convolution(a2)
F0, F1 = C1.transpose(), C2.transpose()
F_original = fmpz_mat([[int(F0[i,j]) if j<d else int(F1[i,j-d]) for j in range(n)] for i in range(d)])
F0inv = F0.inv()
inverse_column = [int(F0inv[i,0].p)*pow(int(F0inv[i,0].q), -1, q) % q for i in range(d)]
assert all(int(v) % q == 0 for row in (F_original*R.transpose()).tolist() for v in row)

rows = []
for lane in payload['lanes']:
    Rs, E = lane['prior_radius'], int(lane['error_norm'])
    t = q//(2*Rs+1)
    assert E*E*Q < t*t
    normalized_u = [centered(t*v) for v in inverse_column]
    c = preimage(normalized_u+[0]*d)
    syndrome = F_original*fmpz_mat([[v] for v in c])
    assert [int(syndrome[i,0]) % q for i in range(d)] == [t]+[0]*(d-1)
    norm2 = sum(v*v for v in c)
    assert 4*E*E*norm2 < t*t
    W0, W1 = convolution(c[:d]).transpose(), convolution(c[d:]).transpose()
    W = fmpz_mat([[int(W0[i,j]) if j<d else int(W1[i,j-d]) for j in range(n)] for i in range(d)])
    assert all((int(v)-t*int(i==j)) % q == 0 for i, row in enumerate((W*F_original.transpose()).tolist()) for j, v in enumerate(row))

    def decode(b):
        w = W*fmpz_mat([[v] for v in b])
        out = []
        for i in range(d):
            options = [r for r in range(-Rs, Rs+1) if centered(int(w[i,0])-t*r)**2 <= E*E*norm2]
            assert len(options) == 1
            out.append(options[0])
        return out

    s = [rng.randrange(-Rs, Rs+1) for _ in range(d)]
    root = math.isqrt(n)
    root += root*root < n
    limit = E//root
    error = [rng.randrange(-limit, limit+1) for _ in range(n)]
    assert sum(v*v for v in error) <= E*E
    signal = F_original.transpose()*fmpz_mat([[v] for v in s])
    b = [(int(signal[i,0])+error[i]) % q for i in range(n)]
    assert decode(b) == s

    # A held-out original record verifies the returned secret, not the finder.
    a3 = [rng.randrange(q) for _ in range(d)]
    C3 = convolution(a3)
    e3 = [rng.randrange(-limit, limit+1) for _ in range(d)]
    heldout_signal = C3*fmpz_mat([[v] for v in s])
    b3 = [(int(heldout_signal[i,0])+e3[i]) % q for i in range(d)]
    assert sum(v*v for v in e3) <= E*E

    fake = list(s)
    fake[0] = -Rs if s[0] != -Rs else Rs
    fake_signal = F_original.transpose()*fmpz_mat([[v] for v in fake])
    b_fake = [int(fake_signal[i,0]) % q for i in range(n)]
    outside_error2 = sum(centered(b_fake[i]-int(signal[i,0]))**2 for i in range(n))
    assert outside_error2 > E*E and decode(b_fake) == fake
    fake_heldout = C3*fmpz_mat([[v] for v in fake])
    fake_heldout_residual2 = sum(centered(b3[i]-int(fake_heldout[i,0]))**2 for i in range(d))
    assert fake_heldout_residual2 > E*E
    rows.append(dict(lane=lane['lane'], prior_radius=Rs, error_norm_bound=str(E),
                     actual_error_norm_squared=str(sum(v*v for v in error)),
                     label=str(t), witness=[str(v) for v in c], witness_norm_squared=str(norm2),
                     original_b=[str(v) for v in b], control_secret=s, recovered_secret=decode(b),
                     original_heldout_a=[str(v) for v in a3], original_heldout_b=[str(v) for v in b3],
                     heldout_residual_squared=str(sum(v*v for v in e3)),
                     out_of_contract_wrong_secret_control=True, heldout_rejected_wrong_secret=True))

output = dict(status='LOCAL_DERIVATION_REVIEW_PENDING', seed=290954,
              scope='d64_original_coordinate_within_contract_controls',
              source_noise_and_prior_laws_sampled=False, quantum_speedup_claim=False,
              noncentered_lift_transform_rejected=True,
              d=d, q=str(q), original_a1=[str(v) for v in a1], original_a2=[str(v) for v in a2],
              gs_squared_sum_upper=str(Q), decoded_coordinates=2*d, lanes=rows)
if args.save:
    destination = directory/'native_rlwe_babai_original_input_d64.json'
    destination.write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps(dict(status=output['status'], checked_saved_profile=True,
                     decoded_coordinates=output['decoded_coordinates'], lanes=len(rows),
                     out_of_contract_controls=2, wrong_secrets_rejected_by_heldout=2,
                     saved=args.save), indent=2))
