"""Marked-cluster Pauli comparator: exact capped reference, not a production FPRAS."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hdqi-cluster-baseline-2026-10-24"))
import cluster_baseline as c


class ForestBudgetExceeded(RuntimeError):
    """A failed random-walk budget is not a zero cluster contribution."""


def forest_count(host, vertices, roots):
    vertices, roots = tuple(vertices), frozenset(roots)
    if not roots or not roots.issubset(vertices) or len(set(vertices)) != len(vertices):
        raise ValueError("nonempty distinct prescribed roots within distinct vertices required")
    nonroots = [v for v in vertices if v not in roots]
    matrix = [[sum(u in host.neighbors[v] for u in vertices) if v == w
               else -int(w in host.neighbors[v]) for w in nonroots] for v in nonroots]
    return c.determinant(matrix)


def complete_forest_count(h, r):
    if type(h) is not int or type(r) is not int or h < 1 or r < 0:
        raise ValueError("positive root count and nonnegative excess required")
    return 1 if not r else h * (h+r)**(r-1)


def forest_order(h, parents):
    n, visited, order = h+len(parents), set(range(h)), []
    while len(visited) < n:
        changed = False
        for child, parent in enumerate(parents, h):
            if child not in visited and parent in visited:
                order.append((parent, child))
                visited.add(child)
                changed = True
        if not changed:
            raise ValueError("parent array has a cycle or invalid root")
    return tuple(order)


def uniform_forest(h, r, rng, max_steps_per_walk=100000):
    """Wilson sampling on the complete graph, with fixed roots already wired."""
    complete_forest_count(h, r)
    if type(max_steps_per_walk) is not int or max_steps_per_walk < 1:
        raise ValueError("positive walk budget required")
    n, in_tree, parents = h+r, set(range(h)), {}
    for start in range(h, n):
        if start in in_tree:
            continue
        path, positions = [start], {start: 0}
        for _ in range(max_steps_per_walk):
            current = path[-1]
            pick = rng.randrange(n-1)
            following = pick + int(pick >= current)
            if following in in_tree:
                path.append(following)
                break
            if following in positions:
                keep = positions[following] + 1
                for vertex in path[keep:]:
                    del positions[vertex]
                path = path[:keep]
            else:
                positions[following] = len(path)
                path.append(following)
        else:
            raise ForestBudgetExceeded("Wilson walk capped; no valid draw produced")
        for child, parent in zip(path, path[1:]):
            parents[child] = parent
            in_tree.add(child)
    return tuple(parents[v] for v in range(h, n))


def all_forests(h, r):
    """Exhaustive independent parent-array reference, capped at four vertices."""
    if h+r > 4:
        raise ValueError("forest enumeration is limited to four vertices")
    complete_forest_count(h, r)
    for parents in product(range(h+r), repeat=r):
        try:
            forest_order(h, parents)
        except ValueError:
            continue
        yield parents


def root_compositions(excess):
    if type(excess) is not int or excess < 0:
        raise ValueError("nonnegative excess required")
    for mask in range(1 << excess):
        cuts = [j for j in range(excess) if mask >> j & 1]
        yield (excess,) if not cuts else (cuts[0],) + tuple(
            b-a for a, b in zip(cuts, cuts[1:]+[excess]))


class Reference:
    def __init__(self, host, roots, ordinary, marked):
        roots = tuple(roots)
        if not roots or roots != tuple(sorted(set(roots))) or any(
                type(v) is not int or not 0 <= v < host.m for v in roots):
            raise ValueError("nonempty sorted distinct host roots required")
        self.host, self.roots = host, roots
        self.ordinary, self.marked = ordinary, marked
        self.base = c.Reference(host, ordinary)

    def root_weight(self, vertices):
        h, r = len(self.roots), len(vertices)-len(self.roots)
        count = forest_count(self.host, vertices, self.roots)
        if count == 0:
            raise ValueError("each component must meet a prescribed root")
        return self.marked(vertices) * F(complete_forest_count(h, r)*self.host.slots**r,
                                         math.factorial(r)*count)

    def draw_root(self, excess, rng):
        h = len(self.roots)
        if h+excess > self.host.m:
            return None
        order = forest_order(h, uniform_forest(h, excess, rng))
        labels, used = dict(enumerate(self.roots)), set(self.roots)
        for parent, child in order:
            neighbors = self.host.neighbors[labels[parent]]
            slot = rng.randrange(self.host.slots)
            if slot >= len(neighbors) or neighbors[slot] in used:
                return None
            labels[child] = neighbors[slot]
            used.add(neighbors[slot])
        vertices = tuple(sorted(used))
        return vertices, self.root_weight(vertices)

    def value(self, excess, limit, sizes, order, sets, weights):
        k, h = len(sizes)-1, len(self.roots)
        mass = 1 if k == 0 else sizes[0]*(h+excess)**(k-1)
        probability = F(1 << (limit-excess), (1 << (limit+1))-1)
        matrix = c.block_graph(self.host, [sets[i] for i in range(k+1)])
        answer = F((1 << excess)*mass, math.factorial(k))/probability
        answer *= F(c.ursell(matrix), c.tree_count(matrix))
        for parent, child in order:
            contacts = sum(self.host.touches((v,), sets[child]) for v in sets[parent])
            answer /= contacts
        return answer * math.prod(weights.values())

    def draw(self, limit, rng):
        if type(limit) is not int or limit < 0:
            raise ValueError("nonnegative truncation required")
        pick, excess = rng.randrange((1 << (limit+1))-1), 0
        while pick >= 1 << (limit-excess):
            pick -= 1 << (limit-excess)
            excess += 1
        cuts = [j for j in range(excess) if rng.randrange(2)]
        composition = (excess,) if not cuts else (cuts[0],) + tuple(
            b-a for a, b in zip(cuts, cuts[1:]+[excess]))
        sizes = (len(self.roots)+composition[0],)+composition[1:]
        sequence = []
        for _ in range(max(0, len(sizes)-2)):
            pick = rng.randrange(sum(sizes))
            for i, size in enumerate(sizes):
                if pick < size:
                    sequence.append(i)
                    break
                pick -= size
        order = c.rooted_order(len(sizes), c.prufer_tree(len(sizes), sequence))
        root = self.draw_root(composition[0], rng)
        if root is None:
            return F(0)
        sets, weights = {0: root[0]}, {0: root[1]}
        for parent, child in order:
            out = self.base.draw_touch(rng.choice(sets[parent]), sizes[child], rng)
            if out is None:
                return F(0)
            sets[child], weights[child] = out
        return self.value(excess, limit, sizes, order, sets, weights)

    @lru_cache(None)
    def root_outcomes(self, excess):
        h = len(self.roots)
        if self.host.m > 4 or h+excess > 4:
            raise ValueError("exhaustive root reference limited to four vertices")
        if h+excess > self.host.m:
            return ()
        counts = defaultdict(int)
        for parents in all_forests(h, excess):
            order = forest_order(h, parents)
            for slots in product(range(self.host.slots), repeat=excess):
                labels, used = dict(enumerate(self.roots)), set(self.roots)
                for (parent, child), slot in zip(order, slots):
                    neighbors = self.host.neighbors[labels[parent]]
                    if slot >= len(neighbors) or neighbors[slot] in used:
                        break
                    labels[child] = neighbors[slot]
                    used.add(neighbors[slot])
                else:
                    counts[tuple(sorted(used))] += 1
        denominator = complete_forest_count(h, excess)*self.host.slots**excess
        return tuple((vertices, self.root_weight(vertices), F(count, denominator))
                     for vertices, count in sorted(counts.items()))

    def exact_draw_mean(self, limit):
        if self.host.m > 4 or not 0 <= limit <= 3:
            raise ValueError("exact mean requires at most four vertices and order three")
        answer = F(0)
        for excess in range(limit+1):
            probability = F(1 << (limit-excess), (1 << (limit+1))-1)
            for composition in root_compositions(excess):
                if len(self.roots)+composition[0] > min(self.host.m, 4):
                    continue
                sizes = (len(self.roots)+composition[0],)+composition[1:]
                count = len(sizes)
                for sequence in product(range(count), repeat=max(0, count-2)):
                    order = c.rooted_order(count, c.prufer_tree(count, sequence))
                    tree_p = math.prod((F(sizes[i], sum(sizes)) for i in sequence), start=F(1))
                    base_p = probability * tree_p / (1 << excess)

                    def descend(position, sets, weights, p):
                        if position == len(order):
                            return p*self.value(excess, limit, sizes, order, sets, weights)
                        parent, child = order[position]
                        value = F(0)
                        for vertex in sets[parent]:
                            for s, y, q in self.base.touch_outcomes(vertex, sizes[child]):
                                value += descend(position+1, {**sets, child: s},
                                                 {**weights, child: y}, p*q/sizes[parent])
                        return value

                    for vertices, weight, p in self.root_outcomes(composition[0]):
                        answer += descend(0, {0: vertices}, {0: weight}, base_p*p)
        return answer


def direct_sum(host, roots, ordinary, marked, limit):
    """Independent ordered-tuple definition, not a tree/forest calculation."""
    if host.m > 4 or not 0 <= limit <= 3:
        raise ValueError("direct sum limited to four vertices and order three")
    answer, h = F(0), len(roots)
    for first in marked:
        for k in range(limit+1):
            for others in product(ordinary, repeat=k):
                sets = (first,)+others
                if sum(map(len, sets))-h <= limit:
                    answer += (F(c.ursell(c.block_graph(host, sets)), math.factorial(k)) *
                               marked[first] * math.prod(ordinary[s] for s in others))
    return answer


def ell(host, mask):
    return sum((sum(bool(mask >> i & 1) for i in host.neighbors[j] if i > j) % 2) << j
               for j in range(host.m))


def restricted_coefficients(host, vertices, beta, couplings, tolerance):
    """Rational Taylor coefficients with an l2 tail upper bound; m<=4 reference."""
    if len(vertices) > 4 or tolerance <= 0 or F(beta) < 0:
        raise ValueError("positive precision, nonnegative beta, at most four vertices required")
    js, beta = tuple(F(couplings[v]) for v in vertices), F(beta)
    scale = beta*sum(map(abs, js))/2
    state = [F(1)]+[F(0)]*((1 << len(vertices))-1)
    if not scale:
        return state, F(0), 1
    masks = [sum(1 << j for j in range(i) if vertices[j] in host.neighbors[vertices[i]])
             for i in range(len(vertices))]
    coefficients, majorant = state[:], F(1)
    upper = 3**math.ceil(scale)
    for order in range(1, 200):
        following = [F(0)]*len(state)
        for parity, coefficient in enumerate(state):
            for i, ji in enumerate(js):
                sign = (-1)**((parity & masks[i]).bit_count() % 2)
                following[parity ^ (1 << i)] += -beta*ji*sign*coefficient/(2*order)
        state = following
        coefficients = [a+b for a, b in zip(coefficients, state)]
        majorant *= scale/order
        if order+2 > scale:
            tail = majorant*scale/(order+1)/(1-scale/(order+2))
            if tail*(2*upper+tail) <= tolerance:
                return coefficients, tail, upper
    raise ValueError("Taylor cap reached; no estimate admitted")


def inserted_partition(host, vertices, roots, twist, beta, couplings, tolerance=F(1, 10**22)):
    if not set(roots).issubset(vertices):
        raise ValueError("insertion roots must be in restricted support")
    coefficients, tail, upper = restricted_coefficients(host, vertices, beta, couplings, tolerance)
    h = sum(1 << v for v in roots)
    w = twist ^ ell(host, h)
    small_h = sum(int(v in roots) << i for i, v in enumerate(vertices))
    small_w = sum((w >> v & 1) << i for i, v in enumerate(vertices))
    value = sum(a*coefficients[y ^ small_h]*(-1)**((y & small_w).bit_count() % 2)
                for y, a in enumerate(coefficients))
    return value, tail*(2*upper+tail)


def marked_activity(host, vertices, roots, twist, beta, couplings, tolerance=F(1, 10**22)):
    if not roots or not set(roots).issubset(vertices):
        raise ValueError("nonempty roots inside marked support required")
    extras = tuple(v for v in vertices if v not in roots)
    value, error = F(0), F(0)
    for size in range(len(extras)+1):
        for extra in combinations(extras, size):
            term, bound = inserted_partition(host, tuple(sorted((*roots, *extra))), roots,
                                             twist, beta, couplings, tolerance/(1 << len(extras)))
            value += (-1)**(len(extras)-size)*term
            error += bound
    return value, error


def pauli_plan(host, couplings, beta, pauli, epsilon=F(1, 8), delta=F(1, 16)):
    beta, epsilon, delta = map(F, (beta, epsilon, delta))
    couplings = tuple(map(F, couplings))
    if len(couplings) != host.m or any(abs(j) > 1 for j in couplings):
        raise ValueError("one bounded real coupling per generator required")
    if beta < 0 or not 0 < epsilon <= F(1, 4) or not 0 < delta < 1:
        raise ValueError("invalid temperature or error budgets")
    if len(pauli) != 3 or any(type(v) is not int for v in pauli):
        raise ValueError("integer Pauli masks and phase required")
    u, w, p = pauli
    if not 0 <= u < 1 << host.m or not 0 <= w < 1 << host.m or not 0 <= p < 4:
        raise ValueError("Pauli out of range")
    if (p-(u & w).bit_count()) % 2:
        raise ValueError("Hermitian Pauli required")
    b = beta*max(map(abs, couplings))
    bound = math.prod(min(F(1), beta*abs(j)) for i, j in enumerate(couplings) if u >> i & 1)
    regime = host.slots*b*b <= F(1, 64)
    out = {"m": host.m, "degree": host.slots-1, "flip_weight": u.bit_count(),
           "flip_bound": str(bound), "D_lambda": str(host.slots*b*b),
           "local_theorem_regime": regime, "production_estimator_executed": False,
           "quantum_gap_certified": False, "full_output_sampling": False}
    if p % 2:
        out.update(status="exact_zero_real_state", estimate=0)
    elif bound <= epsilon/4:
        out.update(status="zero_with_flip_bound", estimate=0)
    elif not regime:
        out.update(status="inconclusive_outside_cluster_regime", estimate=None)
    elif not u:
        out.update(status="existing_parity_cluster_comparator", estimate=None)
    else:
        big_b, tau, limit = 8**u.bit_count(), epsilon/4, 0
        while F(big_b, 3*4**limit) > tau/4:
            limit += 1
        # log(2/delta_r) <= ceil(log2(2/delta_r)); delta_r=delta/4.
        rounds = 1
        while F(1, 2**rounds) > delta/8:
            rounds += 1
        draws = math.ceil(128*big_b*big_b/(tau*tau))*rounds
        out.update(status="marked_cluster_comparator", estimate=None, excess_limit=limit,
                   bound_B=big_b, root_draws_upper=draws,
                   normalized_activity_error=str(tau/(32*big_b*(limit+1))),
                   log_partition_error=str(epsilon/(32*(big_b+1))),
                   maximum_activity_vertices=u.bit_count()+limit,
                   independently_reviewed=False)
    return out


def separated_family(k):
    if type(k) is not int or k < 2:
        raise ValueError("integer k>=2 required")
    g, r = k*k, k**4
    return {"k": k, "cliques": r, "clique_size": g, "m": r*g+r-1,
            "degree": g, "beta": str(F(1, 16*k)), "connector_coupling": str(F(1, 80*16**3)),
            "D_lambda": str(F(g+1, 256*g)), "log_C_lower": str(F(r, 40*16**4)),
            "connected": True, "all_couplings_nonzero": True,
            "graph_constructed": False, "classical_hardness_claimed": False}
