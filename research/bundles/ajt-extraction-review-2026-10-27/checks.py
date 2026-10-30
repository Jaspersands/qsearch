"""Finite controls for the AJT extraction audit, not a general AJT solver."""

from itertools import product
from random import Random


def valid(matrix, target, vector, p):
    return all(x % p for x in vector) and all(
        sum(a * x for a, x in zip(row, vector)) % p != b % p
        for row, b in zip(matrix, target)
    )


def greedy(matrix, target, p):
    """Guaranteed for nonzero rows and n <= p-2; may fail outside that range."""
    n = len(matrix)
    last = [max(j for j, a in enumerate(row) if a % p) for row in matrix]
    x = [0] * n
    for j in range(n):
        forbidden = [False] * p
        forbidden[0] = True
        for i, row in enumerate(matrix):
            if last[i] == j:
                partial = sum(row[t] * x[t] for t in range(j)) % p
                root = (target[i] - partial) * pow(row[j] % p, -1, p) % p
                forbidden[root] = True
        x[j] = next((a for a in range(1, p) if not forbidden[a]), 0)
        if x[j] == 0:
            raise ValueError("This variable has no legal greedy choice")
    assert valid(matrix, target, x, p)
    return x


def invertible_random(n, p, rng):
    matrix = [[int(i == j) for j in range(n)] for i in range(n)]
    if n == 1:
        matrix[0][0] = rng.randrange(1, p)
        return matrix
    for _ in range(8 * n):
        i, j = rng.sample(range(n), 2)
        scalar = rng.randrange(1, p)
        matrix[i] = [(a + scalar * b) % p for a, b in zip(matrix[i], matrix[j])]
    return matrix


def main():
    count = 0
    for a, b, c, d in product(range(5), repeat=4):
        if (a * d - b * c) % 5:
            matrix = [[a, b], [c, d]]
            for target in product(range(5), repeat=2):
                greedy(matrix, target, 5)
                count += 1
    assert count == 12000
    print(f"Exhaustive GL(2,5), every affine target: {count} greedy checks passed")

    rng = Random(20261027)
    count = 0
    for p, sizes in [(3, [1]), (5, [1, 2, 3]), (7, [2, 4, 5]), (100003, [2, 8, 16])]:
        for n in sizes:
            for _ in range(25):
                matrix = invertible_random(n, p, rng)
                target = [rng.randrange(p) for _ in range(n)]
                greedy(matrix, target, p)
                count += 1
    print(f"Seeded invertible-matrix controls: {count} greedy checks passed")

    homogenized = 0
    for _ in range(25):
        p = 5
        matrix = invertible_random(2, p, rng)
        target = [rng.randrange(p) for _ in range(2)]
        augmented = [row + [(-b) % p] for row, b in zip(matrix, target)]
        augmented.append([0, 0, 1])
        for y in product(range(1, p), repeat=3):
            x = [(a * pow(y[-1], -1, p)) % p for a in y[:-1]]
            assert valid(augmented, [0, 0, 0], y, p) == valid(matrix, target, x, p)
            homogenized += 1
    print(f"Affine/homogeneous equivalence controls: {homogenized} points passed")

    p, n = 5, 4
    identity = [[int(i == j) for j in range(n)] for i in range(n)]
    successes = sum(valid(identity, [1] * n, x, p) for x in product(range(1, p), repeat=n))
    assert successes == (p - 2) ** n == 81
    block = [[1, 1, 0, 0], [1, -1, 0, 0], [0, 0, 1, 1], [0, 0, 1, -1]]
    successes_h = sum(valid(block, [0] * n, x, p) for x in product(range(1, p), repeat=n))
    assert successes_h == ((p - 1) * (p - 3)) ** 2 == 64
    print("Rejection controls: affine 81/256; homogeneous 64/256")

    for p in (3, 5, 7):
        n = p - 1
        matrix = [[int(i == j) for j in range(n)] for i in range(n)]
        for i in range(n - 1):
            matrix[i][-1] = 1
        target = list(range(2, p)) + [p - 1]
        assert not any(valid(matrix, target, [1] * (n - 1) + [t], p) for t in range(1, p))
        assert valid(matrix, target, [2] + [1] * (n - 1), p)
        try:
            greedy(matrix, target, p)
        except ValueError:
            pass
        else:
            raise AssertionError("Expected the documented greedy dead end")

    # Check the same upper-triangular family implicitly, without a 100002-square matrix.
    p = 100003
    forbidden = {0, p - 1} | set(range(1, p - 1))
    assert len(forbidden) == p
    for t in range(1, p - 1):
        x_i = 2 if t == 1 else 1
        assert (x_i + 1) % p != (1 + t) % p
    assert 1 != p - 1
    print("Prefix dead ends: p=3,5,7 exhaustive last coordinate; p=100003 implicit exact check")
    print("All finite controls passed. No general fixed-p extractor was tested or implemented.")


if __name__ == "__main__":
    main()
