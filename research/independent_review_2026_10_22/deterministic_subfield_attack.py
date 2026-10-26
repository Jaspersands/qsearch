"""One bounded native control of the deterministic degree-three theorem.

Uses the standard linear/partition matroid intersection exchange graph.
No random choices, input retries, shared-code imports or external writes.
"""
from collections import deque
import json
from pathlib import Path
from time import perf_counter

from verify_checkpoint import inverse, mul, irreducible
from subfield_attack import combine, packed_column
from subfield_extension_attack import add, solve, field_basis, relative_trace, initial_word, verify

HERE = Path(__file__).resolve().parent


def directions(n, modulus, basis):
    candidates = [(1 << j) ^ relative_trace(1 << j, n, 3, modulus)
                  for j in range(n)]
    a = next(v for v in candidates if v)
    span = {}
    for j, c in enumerate(basis):
        add(span, mul(a, c, modulus), 1 << j)
    b = next(v for v in candidates if solve(span, v)[0])
    t2 = next(c for c in basis if c not in (0, 1))
    answer = [inverse(a ^ mul(t, b, modulus), modulus) for t in (0, 1, t2)]
    assert all(relative_trace(inverse(u, modulus), n, 3, modulus) == 0 for u in answer)
    check = {}
    for j, u in enumerate(answer):
        for l, c in enumerate(basis):
            assert add(check, mul(u, c, modulus), 1 << (j*len(basis)+l))
    assert len(check) == n
    return answer, {'a': a, 'b': b, 'parameters': [0, 1, t2]}


def run():
    start = perf_counter()
    n, modulus = 9, (1 << 9) | (1 << 4) | 1
    N, K, m = n*n, n*n//8, n//3
    assert irreducible(n, modulus)
    points = list(range(N))
    targets = [0]*(3*K) + [1]*(N-3*K)
    basis = field_basis(n, 3, modulus)
    dirs, metadata = directions(n, modulus, basis)
    ground = [(i, j) for i in range(3*K) for j in range(3)]
    vectors = [packed_column(points[i], dirs[j], n, K, modulus) for i, j in ground]
    blocks = [[packed_column(points[i], mul(dirs[j], c, modulus), n, K, modulus)
               for c in basis] for i, j in ground]
    selected, paths, rank_reductions = set(), [], 0
    while len(selected) < 3*K:
        order = sorted(selected)
        pivots = {}
        for j, g in enumerate(order):
            for l, column in enumerate(blocks[g]):
                assert add(pivots, column, 1 << (j*m+l))
        assert len(pivots) == m*len(order)
        by_group = {ground[g][0]: g for g in selected}
        assert len(by_group) == len(selected)
        outsiders = [g for g in range(len(ground)) if g not in selected]
        circuits, sources = {}, []
        for g in outsiders:
            residual, cert = solve(pivots, vectors[g])
            rank_reductions += 1
            if residual:
                sources.append(g)
                circuits[g] = set(selected)  # replacement is valid for every member
            else:
                circuits[g] = {h for j, h in enumerate(order)
                               if (cert >> (j*m)) & ((1 << m)-1)}
        previous = {g: None for g in sources}
        queue, end = deque(sources), None
        while queue:
            g = queue.popleft()
            if g not in selected:
                owner = by_group.get(ground[g][0])
                if owner is None:
                    end = g
                    break
                neighbors = [owner]
            else:
                neighbors = [h for h in outsiders if g in circuits[h]]
            for h in neighbors:
                if h not in previous:
                    previous[h] = g
                    queue.append(h)
        assert end is not None, 'Rado certificate predicts a further augmenting path'
        path = []
        while end is not None:
            path.append(end)
            end = previous[end]
        selected.symmetric_difference_update(path)
        paths.append(list(reversed(path)))
        assert len(selected) == len(order)+1

    order, pivots = sorted(selected), {}
    for j, g in enumerate(order):
        for l, column in enumerate(blocks[g]):
            assert add(pivots, column, 1 << (j*m+l))
    assert len(pivots) == n*K
    word, h = initial_word(n, modulus, points, targets)
    residual, cert = solve(pivots, h)
    assert not residual
    for j, g in enumerate(order):
        i, direction = ground[g]
        coefficient = combine((cert >> (j*m)) & ((1 << m)-1), basis)
        word[i] = mul(dirs[direction], coefficient, modulus)
    result = {'n': n, 'N': N, 'K': K, 'modulus': modulus,
              'zero_targets': 3*K, 'directions': dirs, 'direction_construction': metadata,
              'selected_pairs': [ground[g] for g in order], 'augmenting_paths': paths,
              'rank_reductions': rank_reductions, 'binary_rank': len(pivots),
              'native_input': {'points': points, 'targets': targets}, 'witness': word}
    result.update(verify(n, modulus, points, targets, word))
    result['elapsed_seconds'] = perf_counter()-start
    (HERE/'deterministic_subfield_receipt.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['n', 'N', 'K', 'zero_targets', 'directions',
                      'binary_rank', 'rank_reductions', 'native_valid', 'elapsed_seconds']}, indent=2))
    print('augmentations requiring exchange:', sum(len(p)>1 for p in paths))


if __name__ == '__main__':
    run()
