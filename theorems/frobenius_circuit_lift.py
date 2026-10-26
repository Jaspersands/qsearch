"""White-box mixed-Frobenius lifting, not a general circuit factorizer.

Nodes are topologically ordered tuples: ('var', i), ('const', a),
('add', left, right), ('mul', left, right), ('frob', child). The last
operation MEANS the p-th power, not a claimed annotation of another gate.
Constants are in F_p. A lift is always a valid specialization identity;
stabilizer equivalence additionally needs the checked no-carry degree bound.
No group basis acquisition or full stabilizer solver is implemented here.
"""
from dataclasses import dataclass

from flint import fmpz

from theorems.succinct_polynomial_stabilizer import white_box_derivative_guard


@dataclass(frozen=True)
class FrobeniusLift:
    prime: int
    original_dimension: int
    nodes: tuple[tuple, ...]
    output: int
    frobenius_depth: int
    degree_bound: int
    original_degree_bound: int
    source_node_count: int

    @property
    def variable_count(self):
        # Include the WHOLE matrix block at every level, not just used inputs.
        return self.original_dimension*(self.frobenius_depth+1)

    @property
    def node_bound(self):
        return self.source_node_count*(self.frobenius_depth+1)

    def value_and_gradient(self, point, coerce):
        """Reverse differentiation of the LIFT, in a caller-provided field.

        The caller must provide characteristic-p arithmetic and constant
        coercion. This does not differentiate the original p-th powers.
        Point coordinates are level-major: Y_(i,e) has index e*D+i.
        """
        if len(point) != self.variable_count:
            raise ValueError("one independent value per complete Frobenius block required")
        values = []
        for node in self.nodes:
            kind = node[0]
            if kind == "var":
                value = point[node[1]]
            elif kind == "const":
                value = coerce(node[1])
            elif kind == "add":
                value = values[node[1]]+values[node[2]]
            else:
                value = values[node[1]]*values[node[2]]
            values.append(value)
        adjoints = [coerce(0) for _ in self.nodes]
        adjoints[self.output] = coerce(1)
        gradient = [coerce(0) for _ in point]
        for index in range(len(self.nodes)-1, -1, -1):
            node, weight = self.nodes[index], adjoints[index]
            if node[0] == "var":
                gradient[node[1]] += weight
            elif node[0] == "add":
                adjoints[node[1]] += weight
                adjoints[node[2]] += weight
            elif node[0] == "mul":
                adjoints[node[1]] += weight*values[node[2]]
                adjoints[node[2]] += weight*values[node[1]]
        return values[self.output], tuple(gradient)


def lift_frobenius_circuit(prime, dimension, nodes, output=None):
    """Push exposed Frobenius gates to independent formal variable blocks.

    Memoization bounds the output DAG by s*(E+1). No monomial expansion,
    extraction of semantic p-th roots, or search for hidden symmetries.
    """
    if type(prime) is not int or prime <= 4 or not fmpz(prime).is_prime():
        raise ValueError("prime p>4 required for this research contract")
    if type(dimension) is not int or dimension < 1 or not nodes:
        raise ValueError("positive original dimension and nonempty circuit required")
    nodes = tuple(tuple(node) for node in nodes)
    if output is None:
        output = len(nodes)-1
    if type(output) is not int or not 0 <= output < len(nodes):
        raise ValueError("valid output node index required")
    ordinary, reduced, depths = [], [], []
    for index, node in enumerate(nodes):
        if not node or node[0] not in ("var", "const", "add", "mul", "frob"):
            raise ValueError("unsupported circuit node")
        kind = node[0]
        if len(node) != (3 if kind in ("add", "mul") else 2):
            raise ValueError("wrong node arity")
        if kind in ("var", "const"):
            bound = dimension if kind == "var" else prime
            if type(node[1]) is not int or not 0 <= node[1] < bound:
                raise ValueError("canonical variable or base-field constant required")
            ordinary.append(int(kind == "var"))
            reduced.append(int(kind == "var"))
            depths.append(0)
            continue
        if any(type(child) is not int or not 0 <= child < index for child in node[1:]):
            raise ValueError("topologically earlier operand indices required")
        if kind == "frob":
            child = node[1]
            ordinary.append(prime*ordinary[child])
            reduced.append(reduced[child])
            depths.append(depths[child]+1)
        else:
            combine = max if kind == "add" else sum
            ordinary.append(combine(ordinary[j] for j in node[1:]))
            reduced.append(combine(reduced[j] for j in node[1:]))
            depths.append(max(depths[j] for j in node[1:]))
    lifted, memo, pending = [], {}, [(output, 0)]
    while pending:
        key = pending[-1]
        if key in memo:
            pending.pop()
            continue
        index, level = key
        node = nodes[index]
        kind = node[0]
        children = ([(node[1], level+1)] if kind == "frob" else
                    [(j, level) for j in node[1:]] if kind in ("add", "mul") else [])
        missing = [child for child in children if child not in memo]
        if missing:
            pending.extend(missing)
            continue
        if kind == "frob":
            memo[key] = memo[children[0]]
        else:
            value = (("var", level*dimension+node[1]) if kind == "var" else
                     node if kind == "const" else (kind, *(memo[child] for child in children)))
            memo[key] = len(lifted)
            lifted.append(value)
        pending.pop()
    result = FrobeniusLift(prime, dimension, tuple(lifted), memo[(output, 0)],
                           depths[output], reduced[output], ordinary[output], len(nodes))
    if len(lifted) > result.node_bound:
        raise ArithmeticError("memoized circuit lift exceeded its polynomial node bound")
    return result


def mixed_frobenius_derivative_guard(lift):
    """Sufficient classical-attack regime; not an executed stabilizer solver."""
    if lift.degree_bound >= lift.prime:
        raise ValueError("no-carry specialization requires lifted degree < p")
    result = white_box_derivative_guard(lift.prime, lift.original_dimension,
                                       lift.degree_bound)
    return dict(result, lifted_variable_count=lift.variable_count,
                lifted_circuit_nodes=len(lift.nodes),
                original_degree_bound=lift.original_degree_bound,
                frobenius_gate_structure_required=True,
                arbitrary_circuit_root_extraction=False,
                stabilizer_solver_executed=False)
