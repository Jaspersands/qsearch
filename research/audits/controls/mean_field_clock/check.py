"""One exact convention control; no parameter sweep or asymptotic inference."""
from itertools import product
from pathlib import Path
import json
from sage.all import CyclotomicField, QQ, matrix, vector

M = 3
F = CyclotomicField(8, names="zeta8")
zeta = F.gen()                         # exp(i*pi/4)
sqrt2 = zeta + zeta**(-1)
assert sqrt2**2 == 2
basis = list(product((0, 1), repeat=M))
index = {bits: i for i, bits in enumerate(basis)}
initial_amplitude = F(1)/(2*sqrt2)     # 1/sqrt(8)

# H_M = kappa/(M-1) sum_{i<j} Zi Zj. At t=pi/(2*kappa),
# theta=kappa*t/(M-1)=pi/4. Diagonal evolution is EXACT below.
amplitudes = vector(F, [
    initial_amplitude * zeta**(-sum(
        (1-2*bits[i])*(1-2*bits[j])
        for i in range(M) for j in range(i+1, M)
    ))
    for bits in basis
])
assert sum(a*a.conjugate() for a in amplitudes) == 1

rho = matrix(F, 2, 2, lambda i,j: sum(
    amplitudes[index[(i,)+env]] * amplitudes[index[(j,)+env]].conjugate()
    for env in product((0,1), repeat=M-1)
))
rho_Q = matrix(QQ, 2, 2, [QQ(x) for x in rho.list()])
hartree = matrix(QQ, [[QQ(1)/2, QQ(1)/2], [QQ(1)/2, QQ(1)/2]])
X = matrix(QQ, [[0,1],[1,0]])
Z = matrix(QQ, [[1,0],[0,-1]])
z_initial = (hartree*Z).trace()
f_divided_by_kappa = z_initial*Z
assert f_divided_by_kappa.is_zero()
assert rho_Q == matrix(QQ, [[QQ(1)/2,0],[0,QQ(1)/2]])
x_expectation = (rho_Q*X).trace()
difference_eigenvalues = sorted((rho_Q-hartree).eigenvalues())
trace_distance = sum(abs(x) for x in difference_eigenvalues)/2
assert x_expectation == 0
assert difference_eigenvalues == [-QQ(1)/2, QQ(1)/2]
assert trace_distance == QQ(1)/2

result = {
    "status": "passed_exact_single_convention_control",
    "copies": M,
    "field": "Q(zeta_8), zeta_8=exp(i*pi/4)",
    "hamiltonian": "kappa/(M-1) * sum_{i<j} Zi Zj, arbitrary kappa>0",
    "time": "pi/(2*kappa)",
    "pair_phase": "pi/4",
    "basis_order": ["".join(map(str,b)) for b in basis],
    "evolved_amplitudes": [str(a) for a in amplitudes],
    "reduced_density": [[str(x) for x in row] for row in rho_Q.rows()],
    "hartree_density": [[str(x) for x in row] for row in hartree.rows()],
    "source_f_divided_by_kappa": [[str(x) for x in row] for row in f_divided_by_kappa.rows()],
    "X_expectation": str(x_expectation),
    "difference_eigenvalues": [str(x) for x in difference_eigenvalues],
    "trace_distance": str(trace_distance),
    "scope": "M=3 phase/partial-trace convention only; all-M claim is analytic. No native PDE or box-mass lower bound."
}
out = Path(__file__).with_name("result.json")
out.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"status":result["status"], "copies":M,
                  "X_expectation":str(x_expectation), "trace_distance":str(trace_distance)}))
