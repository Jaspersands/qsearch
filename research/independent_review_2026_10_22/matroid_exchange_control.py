"""One native fixture whose final augmentation provably requires exchange."""
from collections import deque
import json
from pathlib import Path

from deterministic_subfield_attack import directions
from subfield_extension_attack import field_basis, relative_trace, add, solve, initial_word, verify
from subfield_attack import packed_column, combine
from verify_checkpoint import mul, irreducible


def run():
    n, modulus, N, K, m = 6, 67, 36, 4, 2
    assert irreducible(n, modulus)
    basis = field_basis(n, 3, modulus)
    dirs, _ = directions(n, modulus, basis)
    # These distinct points/directions span the k-hyperplane
    # Tr_(F/k)(second syndrome component)=0.
    chosen = [(1, 1), (5, 0), (6, 2), (7, 2), (10, 0), (11, 1),
              (15, 0), (18, 0), (20, 1), (21, 1), (23, 0)]
    points = [a for a, _ in chosen] + [0]
    points += [a for a in range(1 << n) if a not in points][:N-len(points)]
    targets = [0]*(3*K) + [1]*(N-3*K)
    ground = [(i, j) for i in range(3*K) for j in range(3)]
    vectors = [packed_column(points[i], dirs[j], n, K, modulus) for i, j in ground]
    blocks = [[packed_column(points[i], mul(dirs[j], c, modulus), n, K, modulus)
               for c in basis] for i, j in ground]
    selected = {3*i+j for i, (_, j) in enumerate(chosen)}
    initial = sorted(selected)
    pivots = {}
    for index, g in enumerate(initial):
        i, j = ground[g]
        assert relative_trace(mul(dirs[j], points[i], modulus), n, 3, modulus) == 0
        for l, v in enumerate(blocks[g]):
            assert add(pivots, v, 1 << (index*m+l))
    assert len(pivots) == n*K-m
    # All three choices at the only unused coordinate are already in the span.
    assert all(solve(pivots, vectors[3*(3*K-1)+j])[0] == 0 for j in range(3))

    owners = {ground[g][0]: g for g in selected}
    outsiders = [g for g in range(len(ground)) if g not in selected]
    circuits, sources = {}, []
    for g in outsiders:
        residual, cert = solve(pivots, vectors[g])
        if residual:
            sources.append(g)
            circuits[g] = set(selected)
        else:
            circuits[g] = {h for j, h in enumerate(initial)
                           if (cert >> (j*m)) & ((1 << m)-1)}
    previous, queue, end = {g: None for g in sources}, deque(sources), None
    while queue:
        g = queue.popleft()
        if g not in selected:
            owner = owners.get(ground[g][0])
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
    assert end is not None
    path = []
    while end is not None:
        path.append(end)
        end = previous[end]
    path.reverse()
    assert len(path) >= 3
    selected.symmetric_difference_update(path)
    assert len(selected) == 3*K
    assert len({ground[g][0] for g in selected}) == 3*K
    order, pivots = sorted(selected), {}
    for j, g in enumerate(order):
        for l, v in enumerate(blocks[g]):
            assert add(pivots, v, 1 << (j*m+l))
    assert len(pivots) == n*K
    word, h = initial_word(n, modulus, points, targets)
    residual, cert = solve(pivots, h)
    assert not residual
    for j, g in enumerate(order):
        i, direction = ground[g]
        coefficient = combine((cert >> (j*m)) & ((1 << m)-1), basis)
        word[i] = mul(dirs[direction], coefficient, modulus)
    result = {'n': n, 'N': N, 'K': K, 'modulus': modulus, 'directions': dirs,
              'initial_pairs': [ground[g] for g in initial],
              'initial_binary_rank': n*K-m, 'initial_direct_addition_possible': False,
              'augmenting_path_pairs': [ground[g] for g in path],
              'final_pairs': [ground[g] for g in order], 'final_binary_rank': len(pivots),
              'native_input': {'points': points, 'targets': targets}, 'witness': word}
    result.update(verify(n, modulus, points, targets, word))
    (Path(__file__).resolve().parent/'matroid_exchange_receipt.json').write_text(
        json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['initial_direct_addition_possible',
          'augmenting_path_pairs', 'final_binary_rank', 'native_valid']}, indent=2))


if __name__ == '__main__':
    run()
