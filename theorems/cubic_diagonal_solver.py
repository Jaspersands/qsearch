"""Public-label cubic SDE constructions, not a quantum receiver.

Implements Ivanyos--Santha (arXiv:1503.09016), Proposition 10's
three-level collision construction. Finite-field roots use FLINT; neither
the field nor its multiplicative group is enumerated. Nonresidue sampling
is explicitly capped. FLINT roots remain an expected-time arithmetic
dependency, not a locally clocked implementation; every witness is checked.
The optional two-level curve contraction has a separate proof/review note in
research/CUBIC_TWO_LEVEL_CONTRACTION.md; novelty is not established.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
import random

from flint import fmpz_mod_poly_ctx

from theorems.nil3_guarded_cyclic_dispatch import independent_columns_exact
from theorems.prime_character_opi import ring
from theorems.symbolic_scalar_phase_erasure import _fmpz_nullspace_basis


def cubic_arity(rank, *, construction="three_level"):
    if type(rank) is not int or rank < 0:
        raise ValueError("nonnegative integer equation rank required")
    if construction == "two_level_curve":
        return (rank+1)*(2*rank+1)
    if construction != "three_level":
        raise ValueError("unknown cubic construction")
    return (rank+1)*(3*rank+1)*(9*rank+1)


def verify_cubic_witness(prime, columns, weights):
    ring(prime)
    if (not columns or not columns[0] or len(weights) != len(columns)
            or any(type(s) is not int or not 0 <= s < prime for s in weights)
            or not any(weights)):
        raise ValueError("nonzero canonical witness with one scale per column required")
    width = len(columns[0])
    if any(len(col) != width or any(type(a) is not int or not 0 <= a < prime for a in col)
           for col in columns):
        raise ValueError("canonical equal-width columns required")
    if any(sum(pow(s, 3, prime)*col[j] for s, col in zip(weights, columns)) % prime
           for j in range(width)):
        raise ArithmeticError("cubic moment does not vanish on the original columns")


def _relation(prime, columns):
    rows = list(map(list, zip(*columns)))
    basis = _fmpz_nullspace_basis(rows, len(columns), prime)
    if not basis or not any(basis[0]):
        raise ArithmeticError("nonzero public linear dependence required")
    result = basis[0]
    if any(sum(a*col[j] for a, col in zip(result, columns)) % prime
           for j in range(len(columns[0]))):
        raise ArithmeticError("invalid linear dependence")
    return result


@dataclass(frozen=True)
class CubicWitness:
    prime: int
    weights: tuple[int, ...]
    compressed_rank: int
    required_columns: int
    method: str
    nonresidue_draws: int = 0
    nonresidue_abort_bound: Fraction = Fraction(0)
    collision_nodes: int = 0
    root_calls: int = 0
    checked_axis_relations: int = 0
    distinguished_cell_nonempty: bool = False
    curve_draws: int = 0
    curve_abort_bound: Fraction = Fraction(0)
    curve_scales: tuple[int, ...] = ()

    @property
    def sampling_abort_bound(self):
        return min(Fraction(1), self.nonresidue_abort_bound+self.curve_abort_bound)


@dataclass(frozen=True)
class CubicCurveWitness:
    scales: tuple[int, int, int]
    draws: int
    abort_bound: Fraction


def ternary_cubic_scales(prime, representatives, *, rng=None, attempt_cap=256):
    """Solve z3*a^3-z2*b^3+z1*c^3=0 with all scales nonzero.

    The representatives must occupy all three nonzero cube cosets. The
    smooth projective cubic has no rational point on a coordinate axis.
    Hasse--Weil gives >=p+1-2*sqrt(p) points, all in the a=1 chart. Each
    accepted b has exactly three c roots, so a uniform b succeeds with
    probability >=1/9 for p=1 mod3, p>=7. The cap bounds sampling only;
    FLINT's root routine is an expected-time dependency, not clocked here.
    """
    ring(prime)
    if prime <= 3 or prime % 3 != 1:
        raise ValueError("three-coset prime p=1 mod3, p>3 required")
    if (len(representatives) != 3
            or any(type(z) is not int or not 0 < z < prime for z in representatives)
            or len({pow(z, (prime-1)//3, prime) for z in representatives}) != 3):
        raise ValueError("three distinct nonzero cube-coset representatives required")
    if type(attempt_cap) is not int or attempt_cap < 1:
        raise ValueError("positive curve attempt cap required")
    z1, z2, z3 = representatives
    rng = rng if rng is not None else random.SystemRandom()
    for draws in range(1, attempt_cap+1):
        b = rng.randrange(0, prime)
        if type(b) is not int or not 0 <= b < prime:
            raise ValueError("random source returned a noncanonical field element")
        cube = (z2*pow(b, 3, prime)-z3)*pow(z1, -1, prime) % prime
        if not cube:
            raise ArithmeticError("distinct cube cosets cannot produce a zero coordinate")
        if pow(cube, (prime-1)//3, prime) != 1:
            continue
        found = fmpz_mod_poly_ctx(prime)([-cube, 0, 0, 1]).roots()
        if not found:
            raise ArithmeticError("missing ternary cubic root")
        c = min(int(item[0]) for item in found)
        if (not b or not 0 < c < prime or pow(c, 3, prime) != cube
                or (z3-z2*pow(b, 3, prime)+z1*pow(c, 3, prime)) % prime):
            raise ArithmeticError("invalid ternary cubic root or cancellation")
        return CubicCurveWitness((1, b, c), draws, Fraction(8, 9)**attempt_cap)
    raise RuntimeError("bounded ternary cubic curve sampler exhausted")


def cubic_weights(prime, columns, *, rng=None, nonresidue_attempt_cap=128,
                  construction="three_level", curve_attempt_cap=256):
    """Return verified scales using ONLY a public matrix over a prime field.

    For p=1 mod3 the required count is (r+1)(3r+1)(9r+1), where r is
    the actual equation rank. The two_level_curve alternative requires
    (r+1)(2r+1) columns and a capped scalar curve sampler. For p=2 mod3,
    r+1 suffices. No input label
    is resampled to improve rank or to select an easier quantum branch.
    Seeded RNGs are replay diagnostics, not independently random proofs.
    """
    ring(prime)
    if prime <= 3:
        raise ValueError("prime p>3 required")
    if type(nonresidue_attempt_cap) is not int or nonresidue_attempt_cap < 1:
        raise ValueError("positive nonresidue attempt cap required")
    if type(curve_attempt_cap) is not int or curve_attempt_cap < 1:
        raise ValueError("positive curve attempt cap required")
    compressed, rank = independent_columns_exact(columns, prime)
    collision_count = cubic_arity(rank, construction=construction)
    required = collision_count if prime % 3 == 1 else rank+1
    if len(columns) < required:
        raise ValueError(f"need {required} columns at equation rank {rank}")
    if not rank:
        weights = (1,)+(0,)*(len(columns)-1)
        verify_cubic_witness(prime, columns, weights)
        return CubicWitness(prime, weights, rank, 1, "zero_rank")
    if prime % 3 == 2:
        dependence = _relation(prime, compressed[:required])
        inverse = pow(3, -1, prime-1)
        weights = tuple(pow(a, inverse, prime) for a in dependence)+(0,)*(len(columns)-required)
        verify_cubic_witness(prime, columns, weights)
        return CubicWitness(prime, weights, rank, required, "bijective_cube")

    rng = rng if rng is not None else random.SystemRandom()
    for draws in range(1, nonresidue_attempt_cap+1):
        zeta = rng.randrange(1, prime)
        if type(zeta) is not int or not 1 <= zeta < prime:
            raise ValueError("random source returned a noncanonical field element")
        if pow(zeta, (prime-1)//3, prime) != 1:
            break
    else:
        raise RuntimeError("bounded cubic-nonresidue sampler exhausted")
    representatives = (1, zeta, zeta*zeta % prime)
    curve = (ternary_cubic_scales(prime, representatives, rng=rng,
                                 attempt_cap=curve_attempt_cap)
             if construction == "two_level_curve" else None)
    characters = tuple(pow(z, (prime-1)//3, prime) for z in representatives)
    polynomials = fmpz_mod_poly_ctx(prime)
    roots = {}
    stats = {"nodes": 0, "root_calls": 0, "axis_checks": 0}

    def classify(value):
        coset = characters.index(pow(value, (prime-1)//3, prime))
        cube = value*pow(representatives[coset], -1, prime) % prime
        if cube not in roots:
            found = polynomials([-cube, 0, 0, 1]).roots()
            stats["root_calls"] += 1
            if not found:
                raise ArithmeticError("FLINT returned no root of a certified nonzero cube")
            root = min(int(item[0]) for item in found)
            if not root or pow(root, 3, prime) != cube:
                raise ArithmeticError("invalid finite-field cube root")
            roots[cube] = root
        return coset, roots[cube]

    def build(start, level):
        if level == 0:
            return {(): {start: 1}}, {(): tuple(compressed[start])}
        stats["nodes"] += 1
        child_size = 1
        for j in range(level-1):
            child_size *= 3**j*rank+1
        child_count = 3**(level-1)*rank+1
        if curve is not None and level == 2:
            # The triples satisfy z1*w1+z2*w2+z3*w3=0, hence dimension <=2r.
            child_count = 2*rank+1
        children = [build(start+k*child_size, level-1) for k in range(child_count)]
        child_keys = tuple(product(range(3), repeat=level-1))
        concatenated = [tuple(a for key in child_keys for a in values[key])
                        for _, values in children]
        relation = _relation(prime, concatenated)
        first = next(a for a in relation if a)
        first_coset, _ = classify(first)
        scale = representatives[level-1]*pow(representatives[first_coset], -1, prime) % prime
        relation = tuple(a*scale % prime for a in relation)
        cells = {key: {} for key in product(range(3), repeat=level)}
        values = {key: [0]*rank for key in cells}
        for coefficient, (child_cells, child_values) in zip(relation, children):
            if not coefficient:
                continue
            coset, root = classify(coefficient)
            for key in child_keys:
                output_key = key+(coset,)
                cells[output_key].update({i: root*b % prime for i, b in child_cells[key].items()})
                for j in range(rank):
                    values[output_key][j] = (values[output_key][j]+pow(root, 3, prime)*child_values[key][j]) % prime
        distinguished = tuple(range(level))
        if not cells[distinguished]:
            raise ArithmeticError("collision construction lost its nonempty distinguished cell")
        # Check every tensor-axis identity before the alternating contraction.
        for axis in range(level):
            for rest in product(range(3), repeat=level-1):
                keys = [rest[:axis]+(s,)+rest[axis:] for s in range(3)]
                if any(sum(representatives[s]*values[keys[s]][j] for s in range(3)) % prime
                       for j in range(rank)):
                    raise ArithmeticError("invalid cubic collision axis relation")
                stats["axis_checks"] += 1
        return cells, values

    levels = 2 if curve is not None else 3
    cells, _ = build(0, levels)
    weights = [0]*len(columns)
    if curve is None:
        contractions = [(key, (-1)**sum(key[i] > key[j] for i in range(3) for j in range(i+1, 3)))
                        for key in permutations(range(3))]
    else:
        a, b, c = curve.scales
        contractions = [((0, 1), a), ((1, 0), -a),
                        ((0, 2), b), ((2, 0), -b),
                        ((1, 2), c), ((2, 1), -c)]
    for key, scale in contractions:
        for i, root in cells[key].items():
            if weights[i]:
                raise ArithmeticError("collision representations overlap")
            weights[i] = scale*root % prime
    verify_cubic_witness(prime, columns, weights)
    method = "two_level_curve_contraction" if curve is not None else "three_coset_collision"
    return CubicWitness(prime, tuple(weights), rank, required, method,
                        draws, Fraction(1, 3**nonresidue_attempt_cap), stats["nodes"],
                        stats["root_calls"]+int(curve is not None), stats["axis_checks"], True,
                        curve.draws if curve else 0, curve.abort_bound if curve else Fraction(0),
                        curve.scales if curve else ())


def report():
    cases = []
    for prime, rank in ((7, 2), (43, 3), (2**127-1, 3), (11, 3)):
        rng = random.Random(301)
        count = cubic_arity(rank) if prime % 3 == 1 else rank+1
        columns = [tuple(rng.randrange(prime) for _ in range(rank)) for _ in range(count)]
        witness = cubic_weights(prime, columns, rng=rng)
        cases.append(dict(prime=prime, input_columns=count, input_equations=rank,
                          compressed_rank=witness.compressed_rank, method=witness.method,
                          nonzero_scales=sum(bool(s) for s in witness.weights),
                          collision_nodes=witness.collision_nodes, root_calls=witness.root_calls,
                          checked_axis_relations=witness.checked_axis_relations,
                          nonresidue_draws=witness.nonresidue_draws,
                          nonresidue_abort_bound=str(witness.nonresidue_abort_bound),
                          exact_original_moment_verified=True))
    two_level_cases = []
    for prime, rank in ((7, 1), (13, 3), (97, 8), (2**127-1, 4)):
        rng = random.Random(301)
        count = cubic_arity(rank, construction="two_level_curve")
        columns = [tuple(int(i == j) for i in range(rank)) for j in range(rank)]
        columns += [tuple(rng.randrange(prime) for _ in range(rank)) for _ in range(count-rank)]
        witness = cubic_weights(prime, columns, rng=rng, construction="two_level_curve")
        two_level_cases.append(dict(
            prime=prime, input_columns=count, input_equations=rank,
            compressed_rank=witness.compressed_rank, method=witness.method,
            published_three_level_columns=cubic_arity(rank),
            nonzero_scales=sum(bool(s) for s in witness.weights),
            collision_nodes=witness.collision_nodes,
            checked_axis_relations=witness.checked_axis_relations,
            root_calls=witness.root_calls, curve_scales=list(witness.curve_scales),
            curve_draws=witness.curve_draws,
            sampling_abort_bound=str(witness.sampling_abort_bound),
            exact_original_moment_verified=True))
    return dict(status="CLASSICAL_CUBIC_SDE_BACKENDS_NOT_QUANTUM_DISCOVERY", cases=cases,
                source="https://arxiv.org/pdf/1503.09016",
                source_scope="Proposition10 three-level comparator; two-level closure is a local deduction",
                two_level_cases=two_level_cases,
                two_level_proof_note="research/CUBIC_TWO_LEVEL_CONTRACTION.md",
                two_level_uses_random_input_promise=False,
                two_level_independent_automated_review=True, human_review=False,
                scalar_curve_success_lower_bound="1/9 per independent uniform draw",
                sampling_caps_are_not_total_runtime_clocks=True,
                cubic_all_prime_backend_implemented=True, general_degree_backend_implemented=False,
                finite_field_root_dependency="FLINT degree-three roots; exact output verification",
                field_enumeration_used=False, full_quantum_receiver_implemented=False,
                independent_review=False, novelty_established=False, speedup_claim_allowed=False)


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payload = json.dumps(report(), indent=2)+"\n"
    if args.write:
        (Path(__file__).resolve().parents[1]/"research/reductions/cubic_diagonal_solver.json").write_text(payload)
    print(payload, end="")
