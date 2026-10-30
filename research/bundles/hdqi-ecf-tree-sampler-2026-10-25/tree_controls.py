"""Exponential, bounded reference controls. Never production input or sampler."""

from itertools import combinations

from tree_sampler import conjugate, fraction, gaussian


def direct_native_vector(couplings, edges, parameters):
    m = len(couplings)
    if not 1 <= m <= 9:
        raise ValueError("exhaustive reference restricted to at most nine vertices")
    earlier = [sum(1 << a for a, b in edges if b == i) for i in range(m)]
    independent = [tuple(i for i in range(m) if mask >> i & 1) for mask in range(1 << m)
                   if not any(mask >> a & 1 and mask >> b & 1 for a, b in edges)]
    vector = {0: gaussian(1)}
    # Apply actual O_i actions to basis words. No layer-crossing formula used.
    for parameter in reversed(parameters):
        u, after = gaussian(parameter), {}
        for selected in independent:
            coefficient = gaussian(1)
            for i in selected:
                coefficient *= -u*gaussian(couplings[i])
            for word, amplitude in vector.items():
                target, value = word, coefficient*amplitude
                for i in reversed(selected):
                    if (target & earlier[i]).bit_count() % 2:
                        value = -value
                    target ^= 1 << i
                after[target] = after.get(target, gaussian(0))+value
        vector = after
    return tuple(vector.get(word, gaussian(0)) for word in range(1 << m))


def direct_output_masses(couplings, edges, parameters, bases):
    vector = list(direct_native_vector(couplings, edges, parameters))
    hadamards = 0
    for i, basis in enumerate(bases):
        if basis == "X":
            hadamards += 1
            for word in range(len(vector)):
                if not word >> i & 1:
                    a, b = vector[word], vector[word | (1 << i)]
                    vector[word], vector[word | (1 << i)] = a+b, a-b
    answer = []
    for amplitude in vector:
        square = amplitude*conjugate(amplitude)
        assert not square.y and square.x >= 0
        answer.append(fraction(square.x)/(1 << hadamards))
    return tuple(answer)


def small_ecf_check(size, edges):
    """Exhaustive recognition ONLY for bounded fixtures, not general input."""
    if size > 12:
        raise ValueError("bounded ECF fixture check")
    adjacency = [set() for _ in range(size)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    for v in range(size):
        for triple in combinations(adjacency[v], 3):
            if all(b not in adjacency[a] for a, b in combinations(triple, 2)):
                return False
    for length in range(4, size+1, 2):
        for vertices in combinations(range(size), length):
            chosen = set(vertices)
            if any(len(adjacency[v] & chosen) != 2 for v in chosen):
                continue
            reached, stack = {vertices[0]}, [vertices[0]]
            while stack:
                v = stack.pop()
                for w in adjacency[v] & chosen - reached:
                    reached.add(w)
                    stack.append(w)
            if reached == chosen:
                return False
    return True
