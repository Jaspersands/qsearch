"""Fixed-input arithmetic controls, never a geometric source backend."""

from pathlib import Path
import sys

from flint import fmpz_mod_poly_ctx
from sympy import Matrix, diag, eye, zeros

import regular_kernel

# Avoid the common standalone module name used in the earlier bundle.
from importlib.util import module_from_spec, spec_from_file_location
path = Path(__file__).resolve().parent.parent/"source-pullback-2026-10-23"/"controls.py"
spec = spec_from_file_location("prior_pullback_controls", path)
prior = module_from_spec(spec)
sys.modules[spec.name] = prior
spec.loader.exec_module(prior)
from kernel_output import odd_maximal_order
sys.path.insert(0, str(path.parent.parent/"frobenius-order-completion-2026-10-25"))
from completion import recover_frobenius_polynomial, spectral_gate

POLYNOMIAL = (169, -130, 50, -10, 1)


def arithmetic_source(rank):
    order = odd_maximal_order(7)
    if rank == 0:
        ell = 5
        first = second = Matrix([2, 1, 0, 0])
    elif rank in (1, 2):
        ell = 17
        second = Matrix([2, 1, 2, 0])  # 3+i+j, norm 17.
        first = Matrix([4, 1, 0, 0]) if rank == 1 else second
    else:
        raise ValueError("rank zero, one or two required")
    phi = Matrix.vstack(first, zeros(4, 1), zeros(4, 1), second)
    gamma = Matrix.vstack(Matrix([3, 2, 0, 0]), zeros(4, 1), zeros(4, 1), Matrix([2, 3, 0, 0]))
    return prior.ArithmeticSource(7, ell, order, phi, (gamma,))


def acquire_polynomial(source):
    """Same coefficient bounds apply to a genuine polarized map of multiplier 13."""
    return recover_frobenius_polynomial(13, [(r, source.observe(r).target_maps[0])
                                           for r in (3, 11, 19)])


def previous_unknown_control(ell):
    """Local lift for the ORIGINAL T^4+25 prime, not an incoming curve isogeny."""
    ctx = fmpz_mod_poly_ctx(ell)
    _, factors = ctx([25, 0, 0, 0, 1]).factor()
    factor = sorted((tuple(int(f[j]) for j in range(f.degree()+1)) for f, _ in factors))[0]
    if len(factor) != 3:
        raise ValueError("this fixed control needs paired quadratic factors")
    a = Matrix([[0, -factor[0]], [1, -factor[1]]])
    permutation = eye(4)[:, [0, 2, 1, 3]]
    beta = permutation.T*diag(a, 5*a.inv_mod(ell*ell).T)*permutation
    return ell*beta, eye(4)[:, [0, 2]], spectral_gate([25, 0, 0, 0, 1], 5, ell)
