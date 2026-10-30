"""Checked two-basis affine avoidance; a scoped deterministic baseline."""

from flint import nmod_mat

from small_prime import SystematicFiber


def greedy_avoid(matrix, forbidden, p):
    """Return a witness or UNKNOWN, never infer infeasibility from a dead end."""
    n = len(forbidden)
    if (not n or len(matrix) != n or any(len(row) != n for row in matrix)
            or any(type(a) is not int or not 0 <= a < p
                   for row in matrix for a in row)
            or any(type(a) is not int or not 0 <= a < p for a in forbidden)):
        raise ValueError("canonical square matrix and target required")
    # This also verifies p, independent rows, and the exact input dimensions.
    SystematicFiber(p, matrix, relation="full_support")
    buckets = [[] for _ in range(n)]
    for i, row in enumerate(matrix):
        last = max(j for j, value in enumerate(row) if value)
        buckets[last].append(i)
    values = []
    for j, bucket in enumerate(buckets):
        excluded = {0}
        for i in bucket:
            prefix = sum(matrix[i][t]*values[t] for t in range(j))
            excluded.add((forbidden[i]-prefix)*pow(matrix[i][j], -1, p) % p)
        # At most len(excluded)+1 trials are needed, without scanning all F_p.
        choice = next((a for a in range(1, min(p, len(excluded)+1))
                       if a not in excluded), None)
        if choice is None:
            return {"status": "UNKNOWN_GREEDY_DEAD_END", "witness": None,
                    "coordinate": j, "forbidden_values": sorted(excluded),
                    "infeasibility_established": False}
        values.append(choice)
    if not all(values) or any(sum(a*x for a, x in zip(row, values)) % p == b
                             for row, b in zip(matrix, forbidden)):
        raise ArithmeticError("greedy answer failed original affine inequalities")
    return {"status": "VERIFIED_AFFINE_AVOIDANCE", "witness": values,
            "largest_bucket": max(map(len, buckets)), "uniform_sampler": False}


def solve_native(p, parity, syndrome):
    fiber = SystematicFiber(p, parity, relation="full_support")
    syndrome = fiber.checked(syndrome, fiber.k)
    remaining = list(fiber.free)
    reduced, rank = nmod_mat([[int(fiber.B[i, j]) for j in remaining]
                             for i in range(fiber.k)], p).rref()
    if rank != fiber.k:
        return {"status": "UNKNOWN_NO_SECOND_BASIS", "witness": None,
                "infeasibility_established": False}
    second = [remaining[next(j for j in range(len(remaining)) if reduced[i, j])]
              for i in range(fiber.k)]
    occupied = set(fiber.pivots+second)
    rest = [j for j in range(fiber.m) if j not in occupied]
    target = [(syndrome[i]-sum(int(fiber.B[i, j]) for j in rest)) % p
              for i in range(fiber.k)]
    b = fiber.pivot_inverse*nmod_mat([[a] for a in target], p)
    transform = fiber.pivot_inverse*nmod_mat(
        [[int(fiber.B[i, j]) for j in second] for i in range(fiber.k)], p)
    matrix = [[int(transform[i, j]) for j in range(fiber.k)] for i in range(fiber.k)]
    result = greedy_avoid(matrix, [int(b[i, 0]) for i in range(fiber.k)], p)
    if result["witness"] is None:
        return result
    x = result["witness"]
    word = [1]*fiber.m
    for i, j in enumerate(second):
        word[j] = x[i]
    for i, j in enumerate(fiber.pivots):
        word[j] = (int(b[i, 0])-sum(matrix[i][t]*x[t] for t in range(fiber.k))) % p
    if not fiber.verifies(word, syndrome):
        raise ArithmeticError("avoidance failed ORIGINAL Bz=s/full support")
    return {"status": "VERIFIED_FULL_SUPPORT_WITNESS", "witness": word,
            "first_basis": fiber.pivots, "second_basis": second,
            "largest_bucket": result["largest_bucket"],
            "all_input_guarantee_from_k_le_p_minus_2": fiber.k <= p-2,
            "uniform_sampler": False, "quantum_advantage_established": False}
