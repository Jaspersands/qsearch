"""Checked disjoint-block repair for the original full-support relation.

This is a sufficient classical certificate, not a general extractor. Blocks
are supplied explicitly and verified from B; no geometry is trusted.
"""

from pathlib import Path
import sys

from flint import nmod_mat

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "ag-affine-sampling-2026-10-26"))
from affine_sampling import AffineFiber


class BlockRepair:
    def __init__(self, p, parity_rows, blocks):
        self.fiber = AffineFiber(p, parity_rows, relation="full_support")
        self.p = p
        self.blocks = tuple(tuple(block) for block in blocks)
        flat = [j for block in self.blocks for j in block]
        if (not self.blocks or any(not block for block in self.blocks)
                or any(type(j) is not int for j in flat)
                or sorted(flat) != list(range(self.fiber.m))):
            raise ValueError("blocks must be a disjoint partition of all coordinates")
        self.directions = []
        self.issues = []
        for block in self.blocks:
            submatrix = nmod_mat([[int(self.fiber.B[i, j]) for j in block]
                                 for i in range(self.fiber.k)], p)
            kernel, dimension = submatrix.nullspace()
            direction = next((tuple(int(kernel[i, j]) for i in range(len(block)))
                              for j in range(dimension)
                              if all(kernel[i, j] for i in range(len(block)))), None)
            self.directions.append(direction)
            if direction is None:
                self.issues.append("no full-support local nullspace basis vector found")
            if len(block) >= p:
                self.issues.append("block length is not smaller than the field")

    def solve(self, syndrome):
        target = self.fiber.checked(syndrome, self.fiber.k)
        if self.issues:
            return {"status": "UNKNOWN_NO_BLOCK_CERTIFICATE", "witness": None,
                    "issues": self.issues, "infeasibility_established": False}
        word = self.fiber.particular(target)
        scalars = []
        for block, direction in zip(self.blocks, self.directions):
            forbidden = {(-word[j]*pow(v, -1, self.p)) % self.p
                         for j, v in zip(block, direction)}
            scalar = next(t for t in range(len(block)+1) if t not in forbidden)
            scalars.append(scalar)
            for j, v in zip(block, direction):
                word[j] = (word[j]+scalar*v) % self.p
        if not self.fiber.verifies(word, target):
            raise ArithmeticError("block repair failed ORIGINAL input verification")
        return {"status": "VERIFIED_FULL_SUPPORT_WITNESS", "witness": word,
                "block_scalars": scalars, "syndrome": list(target),
                "uniform_output_law": False, "quantum_advantage_established": False}


def frozen_basis(p):
    """Exact non-AG countercontrol; intentionally use a poorly chosen basis."""
    from flint import fmpz
    if type(p) is not int or p < 3 or not fmpz(p).is_prime():
        raise ValueError("odd prime required")
    m = 2*(p-1)+1
    v = tuple(range(1, p))*2+(0,)
    return {"p": p, "m": m, "v": v, "syndrome": m % p,
            "state": (1,)*m, "kernel_basis_determinant": (1+sum(v[:-1])) % p,
            "rowspace_distance": m, "native_AG_instance": False}


def frozen_zero_coordinate(p, column, scalar):
    """An explicit zero of 1+scalar*(v+e_column-e_last), no search."""
    m = 2*(p-1)+1
    if (type(column) is not int or not 0 <= column < m-1
            or type(scalar) is not int or not 1 <= scalar < p):
        raise ValueError("valid basis column and nonzero scalar required")
    first = (-pow(scalar, -1, p)) % p-1
    return first+p-1 if column == first else first
