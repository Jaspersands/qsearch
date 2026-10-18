"""Binary BPQM tree certificates versus Prange and affine-cluster baselines.

Known channel-combining mechanism, local certificate derivation REVIEW PENDING.
This evaluates a constructive decoder route; it is not a new quantum algorithm,
an implemented finite-block receiver, or a classical-hardness certificate.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools
import json
from math import isqrt, prod
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.parity_block_usd_prange import affine_system, uniform_affine_solution

REPORT = ROOT / "research/classical_baselines/bpqm_gibbs_frontier.json"


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise ValueError("exact rational required, not bool/float")
    return Fraction(value)


def integer(value, name, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{name} must be an integer in [{minimum},{maximum}]")
    return value


@dataclass(frozen=True)
class MessageLaw:
    """A heralded mixture of binary PSCs, overlaps j/grid, masses w/2^bits."""
    grid: int
    mass_bits: int
    weights: tuple[int, ...]

    def __post_init__(self):
        integer(self.grid, "overlap grid", 2, 512)
        integer(self.mass_bits, "mass precision", 8, 256)
        if self.grid & (self.grid - 1):
            raise ValueError("power-of-two overlap grid required")
        if (type(self.weights) is not tuple or len(self.weights) != self.grid + 1
                or any(type(w) is not int or w < 0 for w in self.weights)
                or sum(self.weights) != 1 << self.mass_bits):
            raise ValueError("exact normalized nonnegative integer message weights required")

    @property
    def fidelity(self):
        return Fraction(sum(j*w for j, w in enumerate(self.weights)), self.grid << self.mass_bits)

    def error_interval(self, precision_bits=80):
        integer(precision_bits, "square-root precision", 8, 256)
        scale, lower, upper = 1 << precision_bits, 0, 0
        for j, weight in enumerate(self.weights):
            radicand = (self.grid*self.grid - j*j)*scale*scale
            floor = isqrt(radicand)
            ceiling = floor + int(floor*floor != radicand)
            lower += weight*(self.grid*scale - ceiling)
            upper += weight*(self.grid*scale - floor)
        denominator = 2*self.grid*scale*(1 << self.mass_bits)
        return Fraction(lower, denominator), Fraction(upper, denominator)


def point_channel(overlap, grid=128, mass_bits=96, *, direction="degrade"):
    c = rational(overlap)
    if not 0 <= c <= 1 or direction not in ("degrade", "upgrade"):
        raise ValueError("overlap in [0,1] and an explicit degradation direction required")
    integer(grid, "overlap grid", 2, 512)
    integer(mass_bits, "mass precision", 8, 256)
    if grid & (grid-1):
        raise ValueError("power-of-two overlap grid required")
    index = (c*grid).__ceil__() if direction == "degrade" else (c*grid).__floor__()
    weights = [0]*(grid + 1)
    weights[index] = 1 << mass_bits
    return MessageLaw(grid, mass_bits, tuple(weights))


def combine(left, right, kind, *, direction="degrade"):
    """Exact binary PSC combination followed by physical information bounds.

    Larger overlap degrades a binary pure-state channel. Rounded-away mass is
    replaced by a completely uninformative channel (degrade) or a perfect one
    (upgrade). Flags are part of the channel, NOT free copies of quantum data.
    """
    if (not isinstance(left, MessageLaw) or not isinstance(right, MessageLaw)
            or (left.grid, left.mass_bits) != (right.grid, right.mass_bits)):
        raise ValueError("matching explicit message laws required")
    if kind not in ("equality", "parity") or direction not in ("degrade", "upgrade"):
        raise ValueError("explicit node kind and information direction required")
    G, L = left.grid, 1 << left.mass_bits
    raw = [0]*(G + 1)
    denominator = L*L*(2*G*G if kind == "parity" else 1)

    def add(numerator, divisor, weight):
        index = (numerator + divisor - 1)//divisor if direction == "degrade" else numerator//divisor
        if not 0 <= index <= G:
            raise ArithmeticError("PSC overlap outside [0,1]")
        raw[index] += weight

    for a, wa in enumerate(left.weights):
        if not wa:
            continue
        for b, wb in enumerate(right.weights):
            if not wb:
                continue
            weight = wa*wb
            if kind == "equality":
                add(a*b, G, weight)
            else:
                for sign in (1, -1):
                    d = G*G + sign*a*b
                    if d:
                        # c+ = G(a+b)/(G^2+ab), c- = G|a-b|/(G^2-ab).
                        numerator = G*G*(a+b if sign == 1 else abs(a-b))
                        add(numerator, d, weight*d)
    if sum(raw) != denominator:
        raise ArithmeticError("unnormalized exact channel-combining law")
    rounded = [value*L//denominator for value in raw]
    discarded = L - sum(rounded)
    if not 0 <= discarded <= G:
        raise ArithmeticError("mass-rounding budget invariant failed")
    rounded[G if direction == "degrade" else 0] += discarded
    return MessageLaw(G, left.mass_bits, tuple(rounded))


def _iteration(message, physical, variable_degree, check_degree, direction):
    check = message
    for _ in range(check_degree - 2):
        check = combine(check, message, "parity", direction=direction)
    result = physical
    for _ in range(variable_degree - 1):
        result = combine(result, check, "equality", direction=direction)
    return result


def tree_frontier(overlap, *, variable_degree=3, check_degree=6,
                  grid=128, mass_bits=96, max_iterations=24):
    """Finite Blackwell bounds and an exact sufficient convergence certificate.

    Once F <= f and c*(dc-1)^(dv-1)*f^(dv-2) < 1, the ORIGINAL unrounded
    recursion has doubly exponential decay. The implication uses the local
    derivation in BPQM_GIBBS_FRONTIER.md, not small-error curve fitting.
    """
    dv = integer(variable_degree, "variable degree", 3, 12)
    dc = integer(check_degree, "check degree", dv + 1, 32)
    integer(max_iterations, "iteration budget", 1, 128)
    c = rational(overlap)
    hi_base = point_channel(c, grid, mass_bits, direction="degrade")
    lo_base = point_channel(c, grid, mass_bits, direction="upgrade")
    lo, hi = lo_base, hi_base
    history, tree_channels, certificate = [], 1, False
    for level in range(1, max_iterations + 1):
        hi = _iteration(hi, hi_base, dv, dc, "degrade")
        lo = _iteration(lo, lo_base, dv, dc, "upgrade")
        tree_channels = 1 + (dv-1)*(dc-1)*tree_channels
        low_error, _ = lo.error_interval()
        _, high_error = hi.error_interval()
        contraction = c*(dc-1)**(dv-1)*hi.fidelity**(dv-2)
        certificate = contraction < 1
        history.append({"level": level, "mean_overlap_lower": str(lo.fidelity),
                        "mean_overlap_upper": str(hi.fidelity),
                        "symbol_error_lower": str(low_error), "symbol_error_upper": str(high_error),
                        "sufficient_contraction_factor_upper": str(contraction),
                        "distinct_original_tree_channel_outputs": tree_channels})
        if certificate:
            break
    return {"overlap_c_exact": str(c), "inverse_temperature": "atanh(c)",
            "variable_degree": dv, "check_degree": dc, "grid": grid, "mass_bits": mass_bits,
            "tree_convergence_certificate": certificate,
            "status": "SUFFICIENT_TREE_CONVERGENCE_CERTIFICATE_REVIEW_PENDING" if certificate else "UNKNOWN_NO_CONVERGENCE_CERTIFICATE_WITHIN_BUDGET",
            "history": history,
            "prange_rank_ceiling_overlap": str(Fraction(dv, dc)),
            "beyond_product_usd_prange_rank_ceiling": c > Fraction(dv, dc),
            "bound_scope": "binary_uniform_codeword_PSCs_on_independent_computation_trees",
            "resource_count_is_extrinsic_tree_not_full_block_decoder": True,
            "finite_graph_block_decoder_executed": False, "coherent_circuit_compiled": False,
            "unknown_quantum_outputs_cloned": False, "accepted_speedup_candidate": False}


def prange_rank_bound(overlap, code_length, variable_degree=3, check_degree=6):
    """Necessary dimension bound for full-rank Bernoulli-subset Prange only."""
    integer(code_length, "code length", 1, 10**12)
    integer(variable_degree, "variable degree", 3, 12)
    integer(check_degree, "check degree", variable_degree+1, 32)
    if code_length*variable_degree % check_degree:
        raise ValueError("integral number of regular checks required")
    c = rational(overlap)
    if not 0 <= c <= 1:
        raise ValueError("overlap must lie in [0,1]")
    ratio = Fraction(variable_degree, check_degree)
    exponent = (2*code_length*(c-ratio)**2).__floor__() if c > ratio else 0
    return {"code_length": code_length, "gibbs_spins": code_length*variable_degree//check_degree,
            "retained_clause_probability_exact": str(c),
            "full_row_rank_proposal_probability_power_two_upper_exponent": exponent,
            "proof": "Pr(full_row_rank)<=Pr(Bin(M,c)<=M*dv/dc)<=exp(-2*M*(c-dv/dc)^2)<=2^(-floor(2*M*(c-dv/dc)^2))" if exponent else "no_nontrivial_rank_bound",
            "all_classical_samplers_excluded": False,
            "rank_aware_cluster_sampler_is_covered_by_this_bound": False}


@dataclass(frozen=True)
class XorIsing:
    spins: int
    clauses: tuple[tuple[int, int], ...]

    def __post_init__(self):
        integer(self.spins, "spin count", 1, 100000)
        if (type(self.clauses) is not tuple or not self.clauses
                or any(type(a) is not int or not 0 <= a < 1 << self.spins
                       or type(b) is not int or b not in (0, 1) for a, b in self.clauses)):
            raise ValueError("explicit binary mask and sign clauses required")

    def satisfied(self, x):
        integer(x, "spin word", 0, (1 << self.spins)-1)
        return tuple(i for i, (a, b) in enumerate(self.clauses) if (a & x).bit_count() % 2 == b)


def affine_jump_geometry(system, width, modes=()):
    """Exact geometry of a uniform affine update, not a mixing assertion."""
    integer(width, "affine width", 1, 100000)
    modes = tuple(modes)
    if any(type(a) is not int or not 0 <= a < 1 << width for a in modes):
        raise ValueError("canonical binary parity masks required")
    if not system["consistent"]:
        raise ValueError("consistent affine system required")
    rows = system["rref"]
    if any(len(row) != width+1 or any(v not in (0, 1) for v in row)
           or (not any(row[:-1]) and row[-1]) for row in rows):
        raise ValueError("consistent binary augmented RREF rows required")
    basis = [sum(int(value) << j for j, value in enumerate(row[:-1]))
             for row in rows if any(row[:-1])]
    pivots = [mask & -mask for mask in basis]
    if (type(system["rank"]) is not int or system["rank"] != len(basis)
            or pivots != sorted(set(pivots))
            or any(mask & pivot for j, mask in enumerate(basis)
                   for i, pivot in enumerate(pivots) if i != j)):
        raise ValueError("verified reduced independent row basis required")
    fixed_coordinates = sum(mask.bit_count() == 1 for mask in basis)
    retained = []
    for a in modes:
        residue = a
        for mask in basis:
            if residue & (mask & -mask):
                residue ^= mask
        retained.append(residue == 0)
    nullity = width - system["rank"]
    return {"nullity": nullity, "coordinate_parities_fixed": fixed_coordinates,
            "expected_hamming_jump_exact": str(Fraction(width-fixed_coordinates, 2)),
            "holding_probability_exact": str(Fraction(1, 1 << nullity)),
            "parity_masks_hex": list(map(hex, modes)), "parity_retained": retained,
            "rank_deficiency_alone_determines_jump": False, "mixing_guarantee": False}


def cluster_step(model, overlap, x, rng, *, geometry=False, modes=()):
    """Polynomial affine-cluster Gibbs update, allowing dependent constraints.

    Correct stationary law is proved; rapid mixing is NOT. No codeword-state
    channel, coherent oracle, partition-function oracle or fresh unknown copy.
    """
    c = rational(overlap)
    if not 0 <= c < 1:
        raise ValueError("finite nonnegative inverse temperature required")
    probability = 2*c/(1+c)
    selected = tuple(i for i in model.satisfied(x)
                     if rng.randrange(probability.denominator) < probability.numerator)
    equations = tuple(model.clauses[i] for i in selected)
    system = affine_system(equations, model.spins)
    if not system["consistent"]:
        raise ArithmeticError("constraints satisfied by current state became inconsistent")
    result = {"word": uniform_affine_solution(system, model.spins, rng),
            "selected_count": len(selected), "selected_rank": system["rank"],
            "dependent_rows_retained": len(selected)-system["rank"],
            "mixing_guarantee": False}
    if geometry:
        result["geometry"] = affine_jump_geometry(system, model.spins, modes)
    return result


def exact_gibbs(model, overlap):
    """Exponential finite calibration, never the claimed scalable sampler."""
    c = rational(overlap)
    if not 0 <= c < 1 or model.spins > 8 or len(model.clauses) > 12:
        raise ValueError("bounded finite-temperature exact calibration required")
    weights = [prod(1+c if ((a & x).bit_count() % 2 == b) else 1-c
                    for a, b in model.clauses) for x in range(1 << model.spins)]
    normalization = sum(weights)
    return tuple(w/normalization for w in weights)


def exact_cluster_kernel(model, overlap):
    """Enumerate small transition rows and check the actual classical competitor."""
    target = exact_gibbs(model, overlap)
    c = rational(overlap)
    p = 2*c/(1+c)
    size = len(target)
    kernel = []
    for x in range(size):
        eligible = model.satisfied(x)
        row = [Fraction(0)]*size
        for bits in itertools.product((0, 1), repeat=len(eligible)):
            selected = tuple(eligible[j] for j, value in enumerate(bits) if value)
            weight = p**len(selected)*(1-p)**(len(eligible)-len(selected))
            solutions = [y for y in range(size) if all(
                (model.clauses[i][0] & y).bit_count() % 2 == model.clauses[i][1] for i in selected)]
            for y in solutions:
                row[y] += weight/len(solutions)
        kernel.append(tuple(row))
    balanced = all(target[x]*kernel[x][y] == target[y]*kernel[y][x]
                   for x in range(size) for y in range(size))
    if not balanced or any(sum(row) != 1 for row in kernel):
        raise ArithmeticError("affine-cluster stationary-law control failed")
    return target, tuple(kernel)


def run_controls():
    frontiers = [tree_frontier(c) for c in ("1/2", "13/20", "4/5")]
    model = XorIsing(3, ((3, 0), (6, 1), (5, 0), (7, 1)))
    target, kernel = exact_cluster_kernel(model, "13/20")
    return {"schema_version": "1.0", "subsystem": "bpqm_gibbs_frontier",
            "mechanism_status": "KNOWN_LITERATURE_LOCAL_CERTIFICATES_REVIEW_PENDING",
            "frontiers": frontiers, "prange_rank_control": prange_rank_bound("13/20", 4096),
            "prange_example_is_not_a_same_size_quantum_execution": True,
            "classical_cluster_control": {"spins": model.spins, "clauses": [list(row) for row in model.clauses],
                "overlap_c_exact": "13/20", "target_probabilities_exact": list(map(str, target)),
                "transition_rows_exact": [list(map(str, row)) for row in kernel],
                "detailed_balance_exact": True, "rapid_mixing_proved": False,
                "rank_dependent_constraints_legal": True},
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "affine_helper_sha256": hashlib.sha256(
                (ROOT/"theorems/parity_block_usd_prange.py").read_bytes()).hexdigest(),
            "accepted_speedup_candidate": False, "new_quantum_algorithm_claimed": False,
            "classical_hardness_proved": False, "finite_graph_decoder_implemented": False,
            "references": ["https://arxiv.org/abs/2609.05857", "https://arxiv.org/abs/2609.40345",
                           "https://arxiv.org/abs/2109.08170"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"frontiers": [{"c": r["overlap_c_exact"], "status": r["status"],
                                    "last_level": r["history"][-1]} for r in result["frontiers"]],
                      "classical_cluster_detailed_balance": result["classical_cluster_control"]["detailed_balance_exact"]}, indent=2))


if __name__ == "__main__":
    main()
