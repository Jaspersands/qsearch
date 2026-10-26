"""One bounded native control for the proved even-degree subfield attack.

Only this review's independent field arithmetic is imported. No shared
repository module, cloud placeholder, source artifact, or Git state is used.
Run with python3 -B. Outputs a witness receipt beside this script.
"""
import json
from pathlib import Path
from random import Random
from time import perf_counter

from verify_checkpoint import inverse, irreducible, mul, trace

HERE = Path(__file__).resolve().parent


def frobenius(a, count, modulus):
    for _ in range(count):
        a = mul(a, a, modulus)
    return a


def subfield_basis(n, modulus):
    pivots, answer = {}, []
    for j in range(n):
        a = (1 << j) ^ frobenius(1 << j, n // 2, modulus)
        v = a
        while v:
            p = v.bit_length() - 1
            if p not in pivots:
                pivots[p] = v
                answer.append(a)
                break
            v ^= pivots[p]
    assert len(answer) == n // 2
    assert all(frobenius(a, n // 2, modulus) == a for a in answer)
    return answer


def combine(bits, basis):
    a = 0
    for j, value in enumerate(basis):
        if bits >> j & 1:
            a ^= value
    return a


def packed_column(alpha, scale, n, K, modulus):
    result, value = 0, scale
    for j in range(K):
        result |= value << (n * j)
        value = mul(value, alpha, modulus)
    return result


def solve_native(n, modulus, points, targets, seed):
    N, K, m = len(points), len(points) // 8, n // 2
    assert n % 2 == 0 and N == n*n and len(set(points)) == N
    assert len(targets) == N and irreducible(n, modulus)
    basis = subfield_basis(n, modulus)
    zeros = [i for i, b in enumerate(targets) if not b]
    ones = [i for i, b in enumerate(targets) if b]
    if len(zeros) < 2*K:
        return {'status': 'UNKNOWN', 'reason': 'too few zero targets'}
    word = [0]*N
    c = next(1 << j for j in range(n) if trace(1 << j, n, modulus))
    t = inverse(c, modulus)
    assert trace(inverse(t, modulus), n, modulus) == 1
    assert frobenius(t, m, modulus) != t
    for i in ones:
        word[i] = t
    U, attempts, buffer = zeros[:], 0, None
    if len(ones) % 2:
        buffer = U.pop(0)
        rng = Random(seed)
        for attempts in range(1, 257):
            u = t ^ combine(rng.getrandbits(m), basis)
            if trace(inverse(u, modulus), n, modulus) == 0:
                word[buffer] = u
                break
        else:
            return {'status': 'ABORT', 'reason': 'buffer cap'}
    h = 0
    for alpha, value in zip(points, word):
        if value:
            h ^= packed_column(alpha, value, n, K, modulus)
    first = h & ((1 << n)-1)
    assert frobenius(first, m, modulus) == first

    pivots, variable = {}, 0
    for i in U:
        for a in basis:
            v = packed_column(points[i], a, n, K, modulus)
            certificate = 1 << variable
            variable += 1
            while v:
                p = v.bit_length()-1
                if p not in pivots:
                    pivots[p] = (v, certificate)
                    break
                pv, pc = pivots[p]
                v ^= pv
                certificate ^= pc

    residual, solution = h, 0
    while residual:
        p = residual.bit_length()-1
        if p not in pivots:
            break
        pv, pc = pivots[p]
        residual ^= pv
        solution ^= pc
    expected_rank = m*(2*K-1)
    result = {'n': n, 'N': N, 'K': K, 'modulus': modulus,
              'zero_targets': len(zeros), 'one_targets': len(ones),
              'binary_rank': len(pivots), 'full_rank_in_W': expected_rank,
              'buffer_index': buffer, 'buffer_trials': attempts,
              'affine_system_consistent': not residual,
              'subfield_basis': basis}
    if len(pivots) != expected_rank or residual:
        result.update(status='UNKNOWN', reason='rank condition failed',
                      native_input={'points': points, 'targets': targets})
        return result
    for j, i in enumerate(U):
        word[i] = combine((solution >> (j*m)) & ((1 << m)-1), basis)

    # Read back the original native equations, without using the packed
    # linear-system representation or its elimination certificates.
    checks = [0]*K
    bad_bits = []
    for i, (alpha, x, b) in enumerate(zip(points, word, targets)):
        inv = inverse(x, modulus)
        assert x == 0 or mul(x, inv, modulus) == 1
        if trace(inv, n, modulus) != b:
            bad_bits.append(i)
        power = 1
        for j in range(K):
            checks[j] ^= mul(power, x, modulus)
            power = mul(power, alpha, modulus)
    assert not bad_bits and not any(checks)
    result.update(status='SUCCESS', native_valid=True,
                  nonzero_syndromes=sum(bool(x) for x in checks),
                  bad_trace_positions=bad_bits, witness=word,
                  native_input={'points': points, 'targets': targets})
    return result


def main():
    start = perf_counter()
    n, modulus = 20, (1 << 20) | (1 << 3) | 1
    assert irreducible(n, modulus)
    rng = Random(20261022)
    points = rng.sample(range(1 << n), n*n)
    targets = [rng.getrandbits(1) for _ in points]
    # One fixed random input and its explicit one-bit variant exercise
    # both parity branches; neither input is retried or regenerated.
    variant = targets[:]
    variant[0] ^= 1
    cases = [solve_native(n, modulus, points, targets, 101),
             solve_native(n, modulus, points, variant, 102)]

    # A valid native input outside the rank promise: all evaluation points
    # lie in the subfield. The one-hot target must trigger UNKNOWN.
    basis = subfield_basis(n, modulus)
    special_points = [combine(i, basis) for i in range(n*n)]
    special_bits = [1]+[0]*(n*n-1)
    countercontrol = solve_native(n, modulus, special_points, special_bits, 103)
    assert countercontrol['status'] == 'UNKNOWN'
    assert not countercontrol['affine_system_consistent']
    result = {'scope': 'One proof-directed native control, not an asymptotic experiment',
              'cases': cases, 'rank_failure_countercontrol': countercontrol,
              'elapsed_seconds': perf_counter()-start}
    (HERE/'subfield_attack_receipt.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'cases': [{k: c[k] for k in
          ('status', 'n', 'N', 'K', 'zero_targets', 'one_targets',
           'binary_rank', 'full_rank_in_W', 'buffer_trials', 'native_valid')}
          for c in cases], 'countercontrol': {k: countercontrol[k] for k in
          ('status', 'binary_rank', 'full_rank_in_W', 'affine_system_consistent')},
          'elapsed_seconds': result['elapsed_seconds']}, indent=2))


if __name__ == '__main__':
    main()
