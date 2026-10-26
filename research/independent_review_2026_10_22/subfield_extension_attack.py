"""Bounded controls for the arbitrary-point subfield attack extensions.

The even-degree control implements the elementary 3K-zero algorithm;
the stronger 2K theorem uses matroid union and is proved in the note.
All writes stay in this independent review directory. Run with -B.
"""
import json
from pathlib import Path
from random import Random
from time import perf_counter

from verify_checkpoint import inverse, irreducible, mul, trace
from subfield_attack import combine, frobenius, packed_column

HERE = Path(__file__).resolve().parent


def relative_trace(x, n, e, modulus):
    answer = 0
    for _ in range(e):
        answer ^= x
        x = frobenius(x, n//e, modulus)
    return answer


def field_basis(n, e, modulus):
    pivots, answer = {}, []
    for j in range(n):
        a = relative_trace(1 << j, n, e, modulus)
        v = a
        while v:
            p = v.bit_length()-1
            if p not in pivots:
                pivots[p] = v
                answer.append(a)
                break
            v ^= pivots[p]
    assert len(answer) == n//e
    assert all(frobenius(a, n//e, modulus) == a for a in answer)
    return answer


def add(pivots, v, certificate):
    while v:
        p = v.bit_length()-1
        if p not in pivots:
            pivots[p] = (v, certificate)
            return True
        pv, pc = pivots[p]
        v ^= pv
        certificate ^= pc
    return False


def solve(pivots, v):
    certificate = 0
    while v:
        p = v.bit_length()-1
        if p not in pivots:
            return v, certificate
        pv, pc = pivots[p]
        v ^= pv
        certificate ^= pc
    return 0, certificate


def initial_word(n, modulus, points, targets):
    c = next(1 << j for j in range(n) if trace(1 << j, n, modulus))
    t = inverse(c, modulus)
    word = [t if b else 0 for b in targets]
    K, h = len(points)//8, 0
    for alpha, value in zip(points, word):
        if value:
            h ^= packed_column(alpha, value, n, K, modulus)
    return word, h


def verify(n, modulus, points, targets, word):
    N, K = len(points), len(points)//8
    assert irreducible(n, modulus) and N == n*n and len(set(points)) == N
    syndromes, bad = [0]*K, []
    for i, (alpha, x, b) in enumerate(zip(points, word, targets)):
        z = inverse(x, modulus)
        assert not x or mul(x, z, modulus) == 1
        if trace(z, n, modulus) != b:
            bad.append(i)
        power = 1
        for j in range(K):
            syndromes[j] ^= mul(power, x, modulus)
            power = mul(power, alpha, modulus)
    assert not any(syndromes) and not bad
    return {'native_valid': True, 'nonzero_syndromes': 0,
            'bad_trace_positions': []}


def even_repair(n, modulus, points, targets):
    m, K = n//2, len(points)//8
    zeros = [i for i, b in enumerate(targets) if not b]
    assert len(zeros) >= 3*K
    basis = field_basis(n, 2, modulus)
    free, U = {}, []
    for i in zeros:
        column = packed_column(points[i], 1, n, K, modulus)
        if solve(free, column)[0]:
            offset = len(U)*m
            U.append(i)
            old = len(free)
            for j, a in enumerate(basis):
                assert add(free, packed_column(points[i], a, n, K, modulus),
                           1 << (offset+j))
            assert len(free) == old+m
    Uset = set(U)
    B = [i for i in zeros if i not in Uset][:K]
    assert len(B) == K and K <= len(U) <= 2*K-1
    theta = next(1 << j for j in range(n)
                 if frobenius(1 << j, m, modulus) != 1 << j)
    joined = free.copy()
    offset = len(U)*m
    for j, i in enumerate(B):
        for l, a in enumerate(basis):
            scale = mul(theta, a, modulus)
            add(joined, packed_column(points[i], scale, n, K, modulus),
                1 << (offset+j*m+l))
    assert len(joined) == n*K
    word, h = initial_word(n, modulus, points, targets)
    residual, coefficients = solve(joined, h)
    assert not residual
    rng, trials, nonzero_buffers = Random(203), [], 0
    for j, i in enumerate(B):
        y = combine((coefficients >> (offset+j*m)) & ((1 << m)-1), basis)
        if not y:
            word[i] = 0
            continue
        nonzero_buffers += 1
        base = mul(theta, y, modulus)
        for count in range(1, 257):
            x = base ^ combine(rng.getrandbits(m), basis)
            if trace(inverse(x, modulus), n, modulus) == 0:
                word[i] = x
                trials.append(count)
                break
        else:
            raise RuntimeError('buffer cap reached; no witness claimed')
        h ^= packed_column(points[i], word[i], n, K, modulus)
    residual, coefficients = solve(free, h)
    assert not residual
    for j, i in enumerate(U):
        word[i] = combine((coefficients >> (j*m)) & ((1 << m)-1), basis)
    result = {'n': n, 'N': len(points), 'K': K, 'modulus': modulus,
              'method': 'elementary even-degree 3K-zero repair',
              'free_indices': U, 'buffer_indices': B,
              'free_binary_rank': len(free), 'joined_binary_rank': len(joined),
              'nonzero_buffers': nonzero_buffers, 'buffer_trials': trials,
              'native_input': {'points': points, 'targets': targets},
              'witness': word}
    result.update(verify(n, modulus, points, targets, word))
    return result


def cubic_extension(n, modulus, points, targets):
    e, m, K = 3, n//3, len(points)//8
    assert n % e == 0 and irreducible(n, modulus)
    zeros = [i for i, b in enumerate(targets) if not b]
    assert len(zeros) >= e*K
    U = zeros[:e*K]
    basis = field_basis(n, e, modulus)
    rng, ranks = Random(204), []
    for trial in range(1, 9):
        directions = []
        for _ in U:
            w = rng.getrandbits(n)
            v = w ^ relative_trace(w, n, e, modulus)  # e is odd
            assert not relative_trace(v, n, e, modulus)
            if not v:
                break
            directions.append(inverse(v, modulus))
        if len(directions) != len(U):
            ranks.append('zero direction denominator')
            continue
        pivots = {}
        for j, (i, u) in enumerate(zip(U, directions)):
            for l, a in enumerate(basis):
                scale = mul(u, a, modulus)
                add(pivots, packed_column(points[i], scale, n, K, modulus),
                    1 << (j*m+l))
        ranks.append(len(pivots))
        if len(pivots) == n*K:
            break
    else:
        raise RuntimeError('direction cap reached; no witness claimed')
    word, h = initial_word(n, modulus, points, targets)
    residual, coefficients = solve(pivots, h)
    assert not residual
    for j, (i, u) in enumerate(zip(U, directions)):
        a = combine((coefficients >> (j*m)) & ((1 << m)-1), basis)
        word[i] = mul(a, u, modulus)
    result = {'n': n, 'N': len(points), 'K': K, 'modulus': modulus,
              'method': 'degree-three extension random accepted zero lines',
              'zero_targets': len(zeros), 'selected_zero_coordinates': len(U),
              'direction_trial_ranks': ranks, 'binary_rank': len(pivots),
              'directions': directions, 'selected_indices': U,
              'native_input': {'points': points, 'targets': targets},
              'witness': word}
    result.update(verify(n, modulus, points, targets, word))
    return result


def main():
    start = perf_counter()
    old = json.loads((HERE/'subfield_attack_receipt.json').read_text())
    bad = old['rank_failure_countercontrol']
    native = bad['native_input']
    repaired = even_repair(bad['n'], bad['modulus'], native['points'], native['targets'])
    n, modulus = 21, (1 << 21) | (1 << 2) | 1
    points = list(range(n*n))  # fixed supplied-point style, not random points
    rng = Random(205)
    targets = [rng.getrandbits(1) for _ in points]
    odd_case = cubic_extension(n, modulus, points, targets)
    result = {'scope': 'Two new proof-directed controls; no original input regenerated',
              'even_rank_failure_repaired': repaired, 'odd_composite_case': odd_case,
              'elapsed_seconds': perf_counter()-start}
    (HERE/'subfield_extension_receipt.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'even_repair': {k: repaired[k] for k in
          ('n', 'N', 'K', 'free_binary_rank', 'joined_binary_rank',
           'nonzero_buffers', 'native_valid')},
          'odd_composite': {k: odd_case[k] for k in
          ('n', 'N', 'K', 'zero_targets', 'binary_rank',
           'direction_trial_ranks', 'native_valid')},
          'elapsed_seconds': result['elapsed_seconds']}, indent=2))


if __name__ == '__main__':
    main()
