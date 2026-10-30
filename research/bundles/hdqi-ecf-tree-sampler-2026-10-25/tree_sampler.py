"""Exact signed transfer-product output contraction on a tree decomposition.

No ECF or thermal promise is inferred. Runtime is exponential in factor count
and bag independence; the caller's decomposition is verified before use.
"""

from fractions import Fraction as Q
from itertools import combinations, product

from sympy.polys.domains import QQ, QQ_I


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, Q)):
        raise TypeError("explicit int/Fraction required, not floating input")
    return Q(value)


def gaussian(value):
    if isinstance(value, QQ_I.dtype):
        return value
    if isinstance(value, tuple) and len(value) == 2:
        real, imag = map(rational, value)
    else:
        real, imag = rational(value), Q(0)
    return QQ_I(QQ(real.numerator, real.denominator),
                QQ(imag.numerator, imag.denominator))


def conjugate(value):
    return QQ_I(value.x, -value.y)


def fraction(value):
    return Q(int(value.numerator), int(value.denominator))


def canonical_edges(size, edges):
    answer = []
    for edge in edges:
        if len(edge) != 2 or any(type(v) is not int or not 0 <= v < size for v in edge):
            raise ValueError("edge endpoints outside graph")
        a, b = sorted(edge)
        if a == b or (a, b) in answer:
            raise ValueError("self-loop or repeated edge")
        answer.append((a, b))
    return tuple(sorted(answer))


class Decomposition:
    def __init__(self, size, edges, bags, tree_edges, *, independence_bound=2):
        if type(size) is not int or size < 1:
            raise ValueError("positive explicit vertex count required")
        if type(independence_bound) is not int or independence_bound < 1:
            raise ValueError("positive independence bound required")
        self.size, self.bound = size, independence_bound
        self.edges = canonical_edges(size, edges)
        parsed = []
        for bag in bags:
            vertices = tuple(bag)
            if any(type(v) is not int or not 0 <= v < size for v in vertices):
                raise ValueError("bag vertex outside graph")
            if len(set(vertices)) != len(vertices):
                raise ValueError("repeated vertex in bag")
            parsed.append(frozenset(vertices))
        if not parsed:
            raise ValueError("empty decomposition")
        self.bags = tuple(parsed)
        self.tree_edges = canonical_edges(len(parsed), tree_edges)
        if len(self.tree_edges) != len(parsed)-1:
            raise ValueError("decomposition edges must form a tree")
        neighbors = [set() for _ in parsed]
        for a, b in self.tree_edges:
            neighbors[a].add(b)
            neighbors[b].add(a)
        self.parents, self.order = {0: None}, [0]
        for a in self.order:
            for b in sorted(neighbors[a]):
                if b not in self.parents:
                    self.parents[b] = a
                    self.order.append(b)
        if len(self.order) != len(parsed):
            raise ValueError("decomposition tree is disconnected")
        self.children = [tuple(b for b in sorted(neighbors[a]) if self.parents.get(b) == a)
                         for a in range(len(parsed))]
        self.masks = tuple(sum(1 << v for v in bag) for bag in self.bags)
        self.separators = tuple(0 if self.parents[a] is None else
                                self.masks[a] & self.masks[self.parents[a]]
                                for a in range(len(parsed)))
        adjacency = [0]*size
        for a, b in self.edges:
            adjacency[a] |= 1 << b
            adjacency[b] |= 1 << a
        self.adjacency = tuple(adjacency)
        for v in range(size):
            containing = {a for a, bag in enumerate(self.bags) if v in bag}
            if not containing:
                raise ValueError("vertex missing from decomposition")
            internal_edges = sum(a in containing and b in containing for a, b in self.tree_edges)
            if internal_edges != len(containing)-1:
                raise ValueError("running intersection fails")
        if any(not any(a in bag and b in bag for bag in self.bags) for a, b in self.edges):
            raise ValueError("graph edge not covered by a bag")
        for bag in self.bags:
            if any(self.independent(sum(1 << v for v in subset))
                   for subset in combinations(sorted(bag), independence_bound+1)):
                raise ValueError("claimed bag independence bound is false")
        self.independent_masks = tuple(tuple(sum(1 << v for v in subset)
                                             for k in range(min(len(bag), independence_bound)+1)
                                             for subset in combinations(sorted(bag), k)
                                             if self.independent(sum(1 << v for v in subset)))
                                       for bag in self.bags)
        self.owned_vertices, self.owned_edges = [[] for _ in parsed], [[] for _ in parsed]
        # Connected bag intersections have a unique highest bag. Assign every
        # unary/edge factor once; separator variables themselves are not summed twice.
        for v in range(size):
            owner = next(a for a in self.order if v in self.bags[a])
            self.owned_vertices[owner].append(v)
        for edge in self.edges:
            owner = next(a for a in self.order if set(edge) <= self.bags[a])
            self.owned_edges[owner].append(edge)

    def independent(self, mask):
        return not any(mask >> v & 1 and mask & self.adjacency[v] for v in range(self.size))

    def resource_record(self, factors):
        if type(factors) is not int or factors < 0:
            raise ValueError("nonnegative factor count required")
        counts = [len(masks)**(2*factors) for masks in self.independent_masks]
        return {"vertices": self.size, "edges": len(self.edges), "bags": len(self.bags),
                "bag_independence_bound": self.bound, "factor_count": factors,
                "replicas": 2*factors, "max_bag_pair_states": max(counts),
                "total_bag_pair_states_per_contraction": sum(counts),
                "state_enumeration_is_exponential_in_factors": True,
                "ecf_recognition_performed": False, "thermal_approximation_certified": False}


class TreeSampler:
    def __init__(self, decomposition, couplings, parameters, *, bases=None,
                 max_pair_states=2_000_000):
        self.decomposition = decomposition
        self.couplings = tuple(rational(j) for j in couplings)
        self.parameters = tuple(gaussian(u) for u in parameters)
        self.m, self.layers = decomposition.size, len(self.parameters)
        if len(self.couplings) != self.m or any(not j or abs(j) > 1 for j in self.couplings):
            raise ValueError("need one nonzero real coupling of magnitude <=1 per vertex")
        self.bases = ("Z",)*self.m if bases is None else tuple(bases)
        if len(self.bases) != self.m or any(b not in ("Z", "X") for b in self.bases):
            raise ValueError("one local Z/X measurement basis per vertex required")
        if type(max_pair_states) is not int or max_pair_states < 1:
            raise ValueError("positive explicit state budget required")
        self.resources = decomposition.resource_record(self.layers)
        if self.resources["total_bag_pair_states_per_contraction"] > max_pair_states:
            raise ValueError("charged pair-state count exceeds explicit budget")
        self._rows = self._compile_rows()
        self.norm_squared = self.mass({})
        if not self.norm_squared:
            raise ValueError("zero transfer vector; no output distribution")

    def _compile_rows(self):
        d, layers = self.decomposition, self.layers
        result = []
        local_weights = [[gaussian(1)]*(1 << layers) for _ in range(self.m)]
        for v in range(self.m):
            for bits in range(1 << layers):
                weight = gaussian(1)
                for layer in range(layers):
                    if bits >> layer & 1:
                        weight *= -self.parameters[layer]*gaussian(self.couplings[v])
                local_weights[v][bits] = weight
        for bag_index, masks in enumerate(d.independent_masks):
            rows = []
            for selections in product(masks, repeat=2*layers):
                at_vertex = {v: tuple(sum(((selections[offset+l] >> v) & 1) << l
                                         for l in range(layers)) for offset in (0, layers))
                             for v in d.bags[bag_index]}
                weight, parities = gaussian(1), []
                for v in d.owned_vertices[bag_index]:
                    ket, bra = at_vertex[v]
                    weight *= local_weights[v][ket]*conjugate(local_weights[v][bra])
                    parities.append((v, ket.bit_count() % 2, bra.bit_count() % 2))
                crossings = 0
                for i, j in d.owned_edges[bag_index]:
                    for copy in (0, 1):
                        earlier, later = at_vertex[i][copy], at_vertex[j][copy]
                        crossings += sum((earlier >> (q+1)).bit_count()
                                         for q in range(layers) if later >> q & 1)
                if crossings % 2:
                    weight = -weight
                if weight:
                    parent_key = tuple(mask & d.separators[bag_index] for mask in selections)
                    child_keys = tuple(tuple(mask & d.separators[child] for mask in selections)
                                       for child in d.children[bag_index])
                    rows.append((parent_key, child_keys, weight, tuple(parities)))
            result.append(tuple(rows))
        return tuple(result)

    def mass(self, pins):
        pins = dict(pins)
        if any(type(v) is not int or not 0 <= v < self.m or
               type(b) is not int or b not in (0, 1) for v, b in pins.items()):
            raise ValueError("pins must map native vertices to bits")
        messages = {}
        d = self.decomposition
        for bag_index in reversed(d.order):
            table = {}
            for parent_key, child_keys, weight, parities in self._rows[bag_index]:
                value = weight
                for v, ket, bra in parities:
                    if v not in pins:
                        if ket != bra:
                            value = gaussian(0)
                            break
                    elif self.bases[v] == "Z":
                        if ket != pins[v] or bra != pins[v]:
                            value = gaussian(0)
                            break
                    else:
                        value *= QQ_I(QQ((-1)**(pins[v]*(ket+bra)), 2))
                if not value:
                    continue
                for child, key in zip(d.children[bag_index], child_keys):
                    value *= messages[child].get(key, gaussian(0))
                    if not value:
                        break
                if value:
                    table[parent_key] = table.get(parent_key, gaussian(0))+value
            messages[bag_index] = table
        answer = messages[0].get((0,)*(2*self.layers), gaussian(0))
        if answer.y or answer.x < 0:
            raise ArithmeticError("exact marginal is nonreal or negative; never clip signs")
        return fraction(answer.x)

    def probability(self, word):
        if len(word) != self.m:
            raise ValueError("one bit per native vertex required")
        return self.mass(dict(enumerate(word)))/self.norm_squared

    def sample(self, rng, *, order=None):
        order = tuple(range(self.m)) if order is None else tuple(order)
        if (len(order) != self.m or any(type(v) is not int for v in order)
                or set(order) != set(range(self.m))):
            raise ValueError("sample order must be a permutation of native vertices")
        pins, current = {}, self.norm_squared
        for v in order:
            zero, one = self.mass({**pins, v: 0}), self.mass({**pins, v: 1})
            if zero+one != current or current <= 0:
                raise ArithmeticError("conditional masses fail exact partition identity")
            probability_one = one/current
            bit = int(rng.randrange(probability_one.denominator) < probability_one.numerator)
            pins[v], current = bit, (one if bit else zero)
        return tuple(pins[v] for v in range(self.m))


def arc_decomposition(arcs, *, universal_count=0):
    """Construct and verify two-clique bags from explicit rational circular arcs.

    Endpoints lie strictly in (0,1); start>end denotes wrapping around zero.
    This is not a graph recognizer or an ECF certificate.
    """
    arcs = tuple(tuple(map(rational, arc)) for arc in arcs)
    if not arcs or any(len(a) != 2 or not 0 < a[0] < 1 or not 0 < a[1] < 1
                       or a[0] == a[1] for a in arcs):
        raise ValueError("nondegenerate arcs with endpoints strictly between zero and one required")
    if type(universal_count) is not int or universal_count < 0:
        raise ValueError("nonnegative universal count required")
    endpoints = sorted({x for arc in arcs for x in arc})
    probes = [Q(0), *endpoints]
    probes += [(a+b)/2 for a, b in zip([Q(0), *endpoints], [*endpoints, Q(1)])]

    def contains(arc, point):
        a, b = arc
        return a <= point <= b if a < b else point >= a or point <= b

    size = len(arcs)+universal_count
    universal = set(range(len(arcs), size))
    edges = [(i, j) for i, j in combinations(range(size), 2)
             if i in universal or j in universal or
             any(contains(arcs[i], t) and contains(arcs[j], t) for t in probes)]
    cut = {v for v, arc in enumerate(arcs) if arc[0] > arc[1]}
    bags = [cut | universal | {v for v, arc in enumerate(arcs)
                              if v not in cut and contains(arc, t)} for t in sorted(set(probes))]
    return Decomposition(size, edges, bags, [(i, i+1) for i in range(len(bags)-1)])


def glue_decompositions(size, edges, pieces, links):
    """Join already globally labelled bag trees; verify the whole certificate.

    pieces are (bags, tree_edges); links are (piece, bag, piece, bag).
    No clique-separator discovery or unchecked promise is hidden here.
    """
    bags, tree_edges, offsets = [], [], []
    for local_bags, local_edges in pieces:
        offsets.append(len(bags))
        tree_edges.extend((a+offsets[-1], b+offsets[-1]) for a, b in local_edges)
        bags.extend(local_bags)
    for a, i, b, j in links:
        if any(type(v) is not int for v in (a, i, b, j)) or not (0 <= a < len(pieces) and 0 <= b < len(pieces)):
            raise ValueError("bad piece link")
        if not (0 <= i < len(pieces[a][0]) and 0 <= j < len(pieces[b][0])):
            raise ValueError("bad local bag link")
        tree_edges.append((offsets[a]+i, offsets[b]+j))
    return Decomposition(size, edges, bags, tree_edges)
