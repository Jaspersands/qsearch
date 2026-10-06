"""Exact classical single-relation completion on the saved native d64 kernel.

LOCAL DERIVATION / REVIEW PENDING. One finite input, not a source-family
attack or efficient quantum generator. The relation comes from classical
LLL preprocessing, whose cost must not be hidden in a free input oracle.
Requires optional python-flint. Does not sample source prior/noise laws.
"""

import argparse
import json
import math
import time
from pathlib import Path

import sympy as sp
from flint import fmpq, fmpq_mat, fmpz_mat


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--save', action='store_true')
parser.add_argument('--relation-index', type=int, default=0)
parser.add_argument('--completion-method', choices=('norms', 'ideal-hnf', 'kernel-hnf'), default='norms')
args = parser.parse_args()
started = time.perf_counter()
directory = Path(__file__).parent
source = json.loads((directory/'native_rlwe_babai_profile_d64.json').read_text())
d, q = source['d'], int(source['q'])


def convolution(a):
    return fmpz_mat([[a[(i-j) % d]*(1 if i >= j else -1)
                      for j in range(d)] for i in range(d)])


def column(a):
    return fmpz_mat([[int(v)] for v in a])


def integral(a):
    assert all(v.q == 1 for row in a.tolist() for v in row)
    return fmpz_mat([[int(v.p) for v in row] for row in a.tolist()])


def nearest_integer(x):
    return (2*int(x.p)+int(x.q))//(2*int(x.q))


def scalar(a):
    assert a.nrows() == a.ncols() == 1
    return a[0, 0]


assert 0 <= args.relation_index < len(source['reduced_row_basis'])
vector = [int(v) for v in source['reduced_row_basis'][args.relation_index]]
g, f = column(vector[:d]), column([-v for v in vector[d:]])
Cg = convolution([int(g[i, 0]) for i in range(d)])
Cf = convolution([int(f[i, 0]) for i in range(d)])
M = convolution([int(v) for v in source['native_ratio']]).transpose()
assert all(int((g-M*f)[i, 0]) % q == 0 for i in range(d))
Nf, Ng = int(Cf.det()), int(Cg.det())
assert Nf and Ng
norm_gcd = math.gcd(Nf, Ng)
e0 = column([1]+[0]*(d-1))
if args.completion_method == 'norms':
    D = norm_gcd
    u, v, gcd = sp.gcdex(Nf, Ng)
    assert gcd == D and u*Nf+v*Ng == D
    adjf = integral(Nf*Cf.inv()*e0)
    adjg = integral(Ng*Cg.inv()*e0)
    G, F = (q*int(u))*adjf, (-q*int(v))*adjg
else:
    if args.completion_method == 'kernel-hnf':
        native_k = [(int(g[i, 0])-int((M*f)[i, 0]))//q for i in range(d)]
        k = column(native_k)
        assert g-M*f == q*k
        right = convolution(native_k)
    else:
        right = Cg
    # Row HNF retains either the ambient ideal or the native-coordinate ideal.
    J = fmpz_mat([[int(Cf[i, j]) if j < d else -int(right[i, j-d])
                   for j in range(2*d)] for i in range(d)])
    Hrows, transform = J.transpose().hnf(transform=True)
    assert transform*J.transpose() == Hrows and abs(int(transform.det())) == 1
    assert all(Hrows[i, j] == 0 for i in range(d, 2*d) for j in range(d))
    H = fmpz_mat([[int(Hrows[j, i]) for j in range(d)] for i in range(d)])
    coordinates = H.inv()*e0
    D = math.lcm(*(int(coordinates[i, 0].q) for i in range(d)))
    if args.completion_method == 'ideal-hnf':
        assert norm_gcd % D == 0
    top_transform = fmpz_mat([[int(transform[i, j]) for j in range(2*d)] for i in range(d)])
    bezout = integral(D*top_transform.transpose()*coordinates)
    assert J*bezout == D*e0
    if args.completion_method == 'kernel-hnf':
        z = column([int(bezout[i, 0]) for i in range(d)])
        F = column([int(bezout[d+i, 0]) for i in range(d)])
        G = M*F+q*z
        assert Cf*z-right*F == D*e0
    else:
        G = q*column([int(bezout[i, 0]) for i in range(d)])
        F = q*column([int(bezout[d+i, 0]) for i in range(d)])
assert Cf*G-Cg*F == (q*D)*e0
C_G = convolution([int(G[i, 0]) for i in range(d)])
C_F = convolution([int(F[i, 0]) for i in range(d)])
A = Cg.transpose()*Cg+Cf.transpose()*Cf
P = Cg.transpose()*C_G+Cf.transpose()*C_F
Ainv = A.inv()
alpha = Ainv*P*e0
gamma = column([nearest_integer(alpha[i, 0]) for i in range(d)])
delta = alpha-fmpq_mat(gamma)
assert scalar(delta.transpose()*delta) <= fmpq(d, 4)
Gred, Fred = G-Cg*gamma, F-Cf*gamma
assert Cf*Gred-Cg*Fred == (q*D)*e0
assert all(int((Gred-M*Fred)[i, 0]) % q == 0 for i in range(d))
C_Gr = convolution([int(Gred[i, 0]) for i in range(d)])
C_Fr = convolution([int(Fred[i, 0]) for i in range(d)])

# This Schur identity checks every embedding algebraically, not by FFT.
perpendicular_gram = (fmpq_mat(C_G.transpose()*C_G+C_F.transpose()*C_F)
                      -P.transpose()*Ainv*P)
assert perpendicular_gram == (q*D)**2*Ainv
norm1 = int(scalar(g.transpose()*g+f.transpose()*f))
norm2 = int(scalar(Gred.transpose()*Gred+Fred.transpose()*Fred))
trace_inverse = sum(Ainv[i, i] for i in range(d))
T_perp = fmpq((q*D)**2, d)*trace_inverse
rounding_energy = scalar(delta.transpose()*A*delta)
assert norm2 == T_perp+rounding_energy
assert rounding_energy <= fmpq(d*d*norm1, 4)
Phi = d*fmpq(4+d*d, 4)*norm1+(q*D)**2*trace_inverse
orbit_bound = d*(norm1+norm2)
assert orbit_bound <= Phi

B = fmpz_mat([[int(Cg[i, j]) if j < d else int(C_Gr[i, j-d]) for j in range(2*d)]
              if i < d else [-int(Cf[i-d, j]) if j < d else -int(C_Fr[i-d, j-d])
                             for j in range(2*d)] for i in range(2*d)])
assert abs(int(B.det())) == (q*D)**d
Gram = B.transpose()*B
bareiss = [[int(Gram[i, j]) for j in range(2*d)] for i in range(2*d)]
previous = 1
ceilings = []
for k in range(2*d):
    pivot = bareiss[k][k]
    assert pivot > 0
    ceilings.append((pivot+previous-1)//previous)
    for i in range(k+1, 2*d):
        for j in range(i, 2*d):
            numerator = pivot*bareiss[i][j]-bareiss[i][k]*bareiss[k][j]
            quotient, remainder = divmod(numerator, previous)
            assert not remainder
            bareiss[i][j] = quotient
            bareiss[j][i] = quotient
    previous = pivot
assert previous == (q*D)**(2*d)
Q = sum(ceilings)
# Q rounds up GS squares; the raw orbit bound bounds the unrounded sum.
assert Q <= orbit_bound+2*d
assert Q >= 2*d*q*D
lanes = []
for lane in source['lanes']:
    E, t = int(lane['error_norm']), int(lane['chosen_label'])
    exact_gate = E*E*Q < t*t
    orbit_gate = E*E*orbit_bound < t*t
    proxy_gate = E*E*Phi < t*t
    necessary_multiplier_budget = (t*t-1)//(2*d*q*E*E)
    if exact_gate:
        assert D <= necessary_multiplier_budget
    lanes.append(dict(lane=lane['lane'], error_norm=str(E), label=str(t),
                      exact_profile_gate=exact_gate, orbit_bound_gate=orbit_gate,
                      reciprocal_proxy_gate=proxy_gate,
                      necessary_multiplier_budget=str(necessary_multiplier_budget),
                      squared_margin_numerator=str(t*t),
                      squared_margin_denominator=str(E*E*Q)))

output = dict(status='LOCAL_DERIVATION_REVIEW_PENDING',
              scope='one_native_d64_classically_preprocessed_relation',
              asymptotic_attack_proved=False, quantum_algorithm=False,
              source_noise_and_prior_laws_sampled=False,
              parent_certificate='native_rlwe_babai_profile_d64.json',
              relation_origin='classical_lll_row', relation_index=args.relation_index,
              d=d, q=str(q), norm_gcd=str(norm_gcd), completion_multiplier=str(D),
              completion_method=args.completion_method, full_kernel_basis=D == 1,
              sublattice_index=str(D**d),
              f=[str(int(f[i, 0])) for i in range(d)],
              g=[str(int(g[i, 0])) for i in range(d)],
              reduced_F=[str(int(Fred[i, 0])) for i in range(d)],
              reduced_G=[str(int(Gred[i, 0])) for i in range(d)],
              norm1_squared=str(norm1), norm2_squared=str(norm2),
              perpendicular_energy=str(T_perp), rounding_energy=str(rounding_energy),
              inverse_gram_trace=str(trace_inverse), reciprocal_proxy=str(Phi),
              orbit_profile_bound=str(orbit_bound),
              gs_squared_integer_upper=[str(value) for value in ceilings],
              gs_squared_sum_upper=str(Q), lanes=lanes,
              elapsed_completion_and_checks_seconds=time.perf_counter()-started)
if args.completion_method == 'kernel-hnf':
    output['completion_ideal'] = 'native_coordinates_f_k'
    output['completion_matrix_lift'] = 'noncentered_residues'
    output['native_coordinate_k'] = [str(int(v)) for v in native_k]
if args.save:
    suffix = '' if args.relation_index == 0 else f'_row{args.relation_index}'
    if args.completion_method == 'ideal-hnf':
        suffix += '_hnf'
    elif args.completion_method == 'kernel-hnf':
        suffix += '_kernel_hnf'
    (directory/f'native_rlwe_balanced_relation_d64{suffix}.json').write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps({key: output[key] for key in (
    'status', 'scope', 'relation_index', 'norm_gcd', 'completion_multiplier',
    'completion_method', 'full_kernel_basis',
    'norm1_squared', 'norm2_squared', 'orbit_profile_bound',
    'gs_squared_sum_upper', 'lanes', 'elapsed_completion_and_checks_seconds')}, indent=2))
