from itertools import product
from pathlib import Path
import random
import sys

from flint import fmpz_mat
import pytest

import a3_pullback as a3

sys.path.insert(0, str(Path(__file__).resolve().parent.parent /
                       "orthogonal-exterior-2026-10-27"))
from exterior_controls import all_subspaces

op = a3.op


def random_sl(p, seed):
    rng = random.Random(seed)
    g = op.eye(4)
    for _ in range(16):
        i, j = rng.sample(range(4), 2)
        e = [list(row) for row in op.eye(4)]
        e[i][j] = rng.randrange(p)
        g = op.mm(g, e, p)
    return g


def all_native_flags(p):
    points = tuple(all_subspaces(4, 1, p))
    planes = tuple(all_subspaces(4, 2, p))
    hyperplanes = tuple(all_subspaces(4, 3, p))
    for space in points+planes+hyperplanes:
        yield (space,)
    for point in points:
        for hyperplane in hyperplanes:
            if len(op.basis(point+hyperplane, p)) == 3:
                yield (point, hyperplane)


@pytest.mark.parametrize("p", [3, 5, 2**127-1])
def test_homomorphism_and_isometry_with_central_kernel(p):
    g, h = random_sl(p, 13), random_sl(p, 17)
    phi_g, phi_h = a3.exterior_square(g, p), a3.exterior_square(h, p)
    assert a3.exterior_square(op.mm(g, h, p), p) == op.mm(phi_g, phi_h, p)
    assert int(fmpz_mat(phi_g).det()) % p == 1
    assert a3.exterior_square(tuple(op.scale(-1, row, p) for row in op.eye(4)), p) == op.eye(6)
    for i in range(4):
        for j in range(i+1, 4):
            assert a3.wedge(op.mv(g, op.eye(4)[i], p), op.mv(g, op.eye(4)[j], p), p) == op.mv(phi_g, a3.wedge(op.eye(4)[i], op.eye(4)[j], p), p)


def test_all_730_flag_subspace_correspondences_and_equivariance_over_f3():
    p, counts, seen = 3, {}, set()
    matrices = (random_sl(p, 5), random_sl(p, 19))
    for flag in all_native_flags(p):
        space = a3.flag_to_singular(flag, p)
        assert space not in seen
        seen.add(space)
        counts[len(space)] = counts.get(len(space), 0)+1
        assert a3.supplied_space_to_flag(space, p) == flag
        for g in matrices:
            assert a3.flag_to_singular(a3.image_flag(g, flag, p), p) == op.image(a3.exterior_square(g, p), space, p)
    assert counts == {1: 130, 2: 520, 3: 80}
    assert len(seen) == 730


@pytest.mark.parametrize("dimensions", [(1,), (2,), (3,), (1, 3)])
@pytest.mark.parametrize("p", [3, 5, 2**127-1])
def test_opaque_pullback_fibers_match_exact_flag_stabilizer(dimensions, p):
    frame = random_sl(p, 43)
    flag = tuple(op.image(frame, op.eye(4)[:d], p) for d in dimensions)
    hidden = a3.flag_to_singular(flag, p)
    original = op.OpaqueFixtureOracle(hidden, p)
    pullback = a3.PullbackOracle(original, p)
    matrices = [op.eye(4)]
    for i, j in product(range(4), repeat=2):
        if i != j:
            g = [list(row) for row in op.eye(4)]
            g[i][j] = 1
            matrices.append(op.mm(op.mm(frame, g, p), op.inverse(frame, p), p))
    matrices += [random_sl(p, seed) for seed in range(6)]
    labels = [pullback(g) for g in matrices]
    images = [a3.image_flag(g, flag, p) for g in matrices]
    for i, j in product(range(len(matrices)), repeat=2):
        assert (labels[i] == labels[j]) == (images[i] == images[j])
    assert original.calls == pullback.calls == len(matrices)


def test_all_130_singular_lines_have_decomposable_rank_two_support():
    count = 0
    for line in all_subspaces(6, 1, 3):
        if op.quadratic(line[0], 3) == 0:
            assert len(a3.bivector_support(line[0], 3)) == 2
            assert a3.flag_to_singular((a3.bivector_support(line[0], 3),), 3) == line
            count += 1
    assert count == 130


def test_no_illegal_gl_oracle_or_non_singular_correspondence():
    g = [list(row) for row in op.eye(4)]
    g[0][0] = 2
    with pytest.raises(ValueError, match="SL4"):
        a3.exterior_square(g, 5)
    with pytest.raises(ValueError, match="totally singular"):
        a3.supplied_space_to_flag((op.add(op.eye(6)[0], op.eye(6)[3], 5),), 5)
    with pytest.raises(ValueError, match="flag types"):
        a3.flag_to_singular((op.eye(4)[:1], op.eye(4)[:2]), 3)
    with pytest.raises(ValueError, match="prime"):
        a3.exterior_square(op.eye(4), 9)
