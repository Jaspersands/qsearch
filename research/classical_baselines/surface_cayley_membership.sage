"""Exact split controls for SURFACE_CAYLEY_MEMBERSHIP.md.

These supplied finite-field matrices do not execute native geometric
interpolation, recover an unknown kernel, or establish asymptotic success.
Retains the original 60-case control and wrong-adjoint falsifier only.
"""

from sage.all import *

set_random_seed(20261031)
p = 11
cases = 0
for ell in [13, 17, 19, 31, 61]:
    k = GF(ell)
    j = block_matrix(k, [
        [zero_matrix(k, 2), identity_matrix(k, 2)],
        [-identity_matrix(k, 2), zero_matrix(k, 2)],
    ])
    j8 = block_diagonal_matrix(j, j)
    adj = lambda a, form: form.inverse() * a.transpose() * form
    for _ in range(12):
        a = random_matrix(k, 4)
        x = p * block_matrix(k, [
            [zero_matrix(k, 4), a],
            [-adj(a, j), zero_matrix(k, 4)],
        ])
        assert adj(x, j8) == -x
        choices = []
        for z in range(10):
            m = k(1 + p*z)
            y = m*identity_matrix(k, 8) + x
            if m and y.det():
                choices.append((m, y))
        assert choices
        m, y = choices[0]
        d = y.det()
        u = (m*identity_matrix(k, 8) - x) * y.inverse()
        f = d*u
        assert adj(f, j8)*f == d*d*identity_matrix(k, 8)
        t = random_matrix(k, 2)
        t = t + t.transpose()
        v = block_matrix(k, [[identity_matrix(k, 2)], [t]])
        v2 = block_matrix(k, [
            [v, zero_matrix(k, 4, 2)],
            [zero_matrix(k, 4, 2), v],
        ])
        preserves = lambda op, basis: basis.augment(op*basis).rank() == basis.rank()
        assert preserves(a, v) == preserves(f, v2)
        cases += 1

print({
    'finite_split_Cayley_controls': int(cases),
    'all_pass': True,
    'native_geometry_executed': False,
})

# The already-run falsifier: -a in place of -a^dagger is not polarized.
k = GF(13)
p = 11
j = block_matrix(k, [
    [zero_matrix(k, 2), identity_matrix(k, 2)],
    [-identity_matrix(k, 2), zero_matrix(k, 2)],
])
j8 = block_diagonal_matrix(j, j)
adj = lambda a, form: form.inverse() * a.transpose() * form
a = zero_matrix(k, 4)
a[0, 1] = 1
x = p * block_matrix(k, [
    [zero_matrix(k, 4), a],
    [-a, zero_matrix(k, 4)],
])
m = k(1)
y = m*identity_matrix(k, 8) + x
d = y.det()
f = d*(m*identity_matrix(k, 8) - x)*y.inverse()
wrong_skew = adj(x, j8) == -x
wrong_polarized = adj(f, j8)*f == d*d*identity_matrix(k, 8)
defect_rank = (adj(f, j8)*f - d*d*identity_matrix(k, 8)).rank()
assert not wrong_skew
assert not wrong_polarized
assert defect_rank == 4
print({
    'ell': 13, 'p': 11, 'a': 'E12', 'm': 1,
    'd_mod_ell': int(d),
    'wrong_lower_block_skew_adjoint': wrong_skew,
    'wrong_lower_block_polarized': wrong_polarized,
    'polarization_defect_rank': int(defect_rank),
})
