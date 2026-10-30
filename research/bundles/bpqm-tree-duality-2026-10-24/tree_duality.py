"""Binary tree channel duality with directed, exactly normalized bounds.

The integer-mass combiner adapts the resident bpqm_gibbs_frontier kernel.
Numerical UP means a degraded PSC but an upgraded BMS channel. This does not
simulate a loopy block decoder or establish a finite-graph sampling theorem.
"""

from dataclasses import dataclass
from fractions import Fraction as F


def rational(value):
    if type(value) not in (int, F, str):
        raise ValueError("exact rational required")
    return F(value)


def integer(value, name, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in [{low},{high}]")
    return value


@dataclass(frozen=True)
class Law:
    grid: int
    bits: int
    weights: tuple[int, ...]

    def __post_init__(self):
        integer(self.grid, "grid", 2, 512)
        integer(self.bits, "mass bits", 8, 256)
        if self.grid & (self.grid-1):
            raise ValueError("power-of-two grid required")
        if (type(self.weights) is not tuple or len(self.weights) != self.grid+1
                or any(type(w) is not int or w < 0 for w in self.weights)
                or sum(self.weights) != 1 << self.bits):
            raise ValueError("exactly normalized nonnegative integer masses required")

    def moment(self, power):
        integer(power, "moment", 1, 8)
        return F(sum(j**power*w for j, w in enumerate(self.weights)),
                 self.grid**power*(1 << self.bits))


def point(value, grid=128, bits=96, direction="up"):
    value = rational(value)
    if not 0 <= value <= 1 or direction not in ("up", "down"):
        raise ValueError("point in [0,1] and explicit rounding direction required")
    integer(grid, "grid", 2, 512)
    integer(bits, "mass bits", 8, 256)
    x = value*grid
    index = -(-x.numerator//x.denominator) if direction == "up" else x.numerator//x.denominator
    weights = [0]*(grid+1)
    weights[index] = 1 << bits
    return Law(grid, bits, tuple(weights))


def combine(left, right, kind, direction="up"):
    """Shared numeric rules, not shared physical meanings.

    product: PSC equality / BMS XOR.
    parallel: PSC parity / independent BMS observations of the same bit.
    """
    if (not isinstance(left, Law) or not isinstance(right, Law)
            or (left.grid, left.bits) != (right.grid, right.bits)):
        raise ValueError("matching channel laws required")
    if kind not in ("product", "parallel") or direction not in ("up", "down"):
        raise ValueError("invalid channel operation or bound direction")
    g, scale = left.grid, 1 << left.bits
    denominator = scale*scale*(2*g*g if kind == "parallel" else 1)
    raw = [0]*(g+1)

    def add(numerator, divisor, weight):
        j = (numerator+divisor-1)//divisor if direction == "up" else numerator//divisor
        if not 0 <= j <= g:
            raise ArithmeticError("invalid channel parameter")
        raw[j] += weight

    for a, wa in enumerate(left.weights):
        if not wa:
            continue
        for b, wb in enumerate(right.weights):
            if not wb:
                continue
            if kind == "product":
                add(a*b, g, wa*wb)
            else:
                for sign in (1, -1):
                    divisor = g*g+sign*a*b
                    if divisor:
                        add(g*g*(a+b if sign == 1 else abs(a-b)), divisor,
                            wa*wb*divisor)
    if sum(raw) != denominator:
        raise ArithmeticError("raw law is not exactly normalized")
    weights = [mass*scale//denominator for mass in raw]
    remainder = scale-sum(weights)
    if not 0 <= remainder <= g:
        raise ArithmeticError("invalid directed mass rounding")
    weights[g if direction == "up" else 0] += remainder
    return Law(g, left.bits, tuple(weights))


def A(law, degree, direction="up"):
    """D-1 parallel observations, with independent flags."""
    integer(degree, "spin degree", 3, 32)
    result = law
    for _ in range(degree-2):
        result = combine(result, law, "parallel", direction)
    return result


def B(law, c, arity, direction="up"):
    """Noisy parity of k-1 independent child messages."""
    integer(arity, "clause arity", 3, 12)
    result = point(c, law.grid, law.bits, direction)
    for _ in range(arity-1):
        result = combine(result, law, "product", direction)
    return result


def bounded_tree(c=F(13, 20), *, arity=3, degree=6, levels=13, grid=128, bits=96):
    c = rational(c)
    if not 0 < c < 1:
        raise ValueError("strict channel parameter required")
    integer(levels, "levels", 1, 64)
    classical = point(1, grid, bits)
    quantum = B(classical, c, arity)
    coefficient = (degree-1)*c*c
    history = []
    certificate = None
    for level in range(1, levels+1):
        classical = A(quantum, degree)
        quantum = B(classical, c, arity)
        q, fidelity = classical.moment(2), quantum.moment(1)
        contraction = coefficient*q**(arity-2)
        if certificate is None and contraction < 1:
            certificate = {"level": level, "q_upper": str(q),
                           "coefficient": str(coefficient),
                           "contraction": str(contraction),
                           "scope": "unrounded_free_boundary_tree_recursion_only"}
        history.append({"level": level, "q_classical_upper": str(q),
                        "mean_quantum_overlap_upper": str(fidelity),
                        "classical_contraction_upper": str(contraction),
                        "quantum_contraction_upper": str(c*(degree-1)**(arity-1)*fidelity**(arity-2))})
    return {"c": str(c), "arity": arity, "degree": degree, "grid": grid, "bits": bits,
            "history": history, "nonreconstruction_certificate": certificate,
            "final_classical_weights": list(classical.weights),
            "final_quantum_weights": list(quantum.weights),
            "threshold_identity_scope": "independent_binary_tree_DE_with_perfect_classical_boundary",
            "finite_graph_mixing_proved": False, "all_quantum_decoders_ruled_out": False,
            "classical_fixed_instance_Gibbs_sampler": False}


def all_plus_boundary_update(m, c, arity=3, degree=6):
    m, c = rational(m), rational(c)
    integer(arity, "clause arity", 3, 12)
    integer(degree, "spin degree", 3, 32)
    if not 0 <= m <= 1 or not 0 <= c < 1:
        raise ValueError("invalid boundary magnetization or coupling")
    a = c*m**(arity-1)
    return ((1+a)**(degree-1)-(1-a)**(degree-1))/((1+a)**(degree-1)+(1-a)**(degree-1))


def basin_bound(q, c, arity, degree, extra_levels):
    q, c = rational(q), rational(c)
    integer(arity, "arity", 3, 12)
    integer(degree, "degree", 3, 32)
    integer(extra_levels, "extra levels", 0, 16)
    if not 0 <= q <= 1 or not 0 < c < 1:
        raise ValueError("invalid moment or coupling")
    a, r = (degree-1)*c*c, arity-1
    if a*q**(r-1) >= 1:
        raise ValueError("no contraction certificate")
    result = q
    for _ in range(extra_levels):
        result = a*result**r
    return result
