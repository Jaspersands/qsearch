"""One-level-shorter odd-power SDE construction in a certified large field.

Local exterior-algebra deduction from the published collision scaffold,
not established novelty, a quantum receiver, or a total-clock backend.
Every accepted witness is verified on the original public labels.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
from math import prod
import random

from theorems.cubic_diagonal_solver import _relation
from theorems.nil3_guarded_cyclic_dispatch import independent_columns_exact
from theorems.prime_character_opi import ring
from theorems.scalar_fermat_solver import _field_root


def _degree(degree):
    if type(degree) is not int or degree < 3 or degree % 2 == 0:
        raise ValueError("odd reduced degree >=3 required")


def validate_family(prime, degree):
    ring(prime)
    _degree(degree)
    if degree >= prime or (prime-1) % degree:
        raise ValueError("reduced degree must divide prime-1 and be below prime")
    if prime < 4*((degree-1)*(degree-2))**2:
        raise ValueError("field is below the certified ternary-curve regime")


def odd_power_arity(rank, degree):
    _degree(degree)
    if type(rank) is not int or rank < 0:
        raise ValueError("nonnegative integer rank required")
    return prod((degree-1)**level*rank+1 for level in range(degree-1))


def _sign(indices):
    return (-1)**sum(a > b for i, a in enumerate(indices) for b in indices[i+1:])


def _representatives(prime, degree, rng, attempts):
    # Degree is fixed in the complexity contract. Trial division avoids
    # importing an uncapped randomized integer-factorization dependency.
    divisors, remaining, divisor = [], degree, 2
    while divisor*divisor <= remaining:
        if remaining % divisor == 0:
            divisors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        divisors.append(remaining)
    phi = degree
    for q in divisors:
        phi = phi//q*(q-1)
    for draws in range(1, attempts+1):
        generator = rng.randrange(1, prime)
        if type(generator) is not int or not 0 < generator < prime:
            raise ValueError("random source returned a noncanonical field element")
        character = pow(generator, (prime-1)//degree, prime)
        if all(pow(character, degree//q, prime) != 1 for q in divisors):
            return (tuple(pow(generator, i, prime) for i in range(degree)),
                    draws, Fraction(degree-phi, degree)**attempts)
    raise RuntimeError("bounded power-coset generator sampler exhausted")


@dataclass(frozen=True)
class ScalarClosure:
    scales: tuple[int, ...]
    draws: int
    abort_bound: Fraction


def scalar_closure(prime, degree, representatives, *, rng=None, attempts=256):
    """Find a0,a1,a_last with z0*a0^d-z1*a1^d+z_last=0.

    The scalar curve has no rational points with a zero coordinate. Its
    genus is (d-1)(d-2)/2, so the field guard certifies success >=1/(2d).
    Only the classical uniform draws are capped; root extraction is not.
    """
    validate_family(prime, degree)
    if (len(representatives) != degree
            or any(type(z) is not int or not 0 < z < prime for z in representatives)
            or len({pow(z, (prime-1)//degree, prime) for z in representatives}) != degree):
        raise ValueError("complete distinct nonzero power-coset representatives required")
    if type(attempts) is not int or attempts < 1:
        raise ValueError("positive scalar attempt cap required")
    rng = random.SystemRandom() if rng is None else rng
    z0, z1, last = representatives[0], representatives[1], representatives[-1]
    for draw in range(1, attempts+1):
        a0 = rng.randrange(0, prime)
        if type(a0) is not int or not 0 <= a0 < prime:
            raise ValueError("random source returned a noncanonical field element")
        value = (z0*pow(a0, degree, prime)+last)*pow(z1, -1, prime) % prime
        if not value:
            raise ArithmeticError("distinct cosets cannot give a zero scalar coordinate")
        if pow(value, (prime-1)//degree, prime) != 1:
            continue
        a1 = _field_root(prime, degree, value)
        if not a0 or not a1 or (z0*pow(a0, degree, prime)-z1*pow(a1, degree, prime)+last) % prime:
            raise ArithmeticError("invalid scalar closure")
        scales = (a0, a1)+(0,)*(degree-3)+(1,)
        return ScalarClosure(scales, draw, Fraction(2*degree-1, 2*degree)**attempts)
    raise RuntimeError("bounded odd-power scalar curve sampler exhausted")


@dataclass(frozen=True)
class OddPowerWitness:
    prime: int
    degree: int
    weights: tuple[int, ...]
    compressed_rank: int
    required_columns: int
    collision_nodes: int = 0
    checked_axis_relations: int = 0
    checked_minor_relations: int = 0
    root_calls: int = 0
    generator_draws: int = 0
    scalar_draws: int = 0
    sampling_abort_bound: Fraction = Fraction(0)


def odd_power_weights(prime, degree, columns, *, rng=None,
                      generator_attempt_cap=128, scalar_attempt_cap=256):
    """Return a checked nonzero witness for every admissible label matrix.

    No input label or source is resampled. Field/degree regimes without
    the stated proof reject before construction. For fixed degree the
    construction size is polynomial in rank, with unclocked arithmetic
    dependencies as documented in research/ODD_POWER_EXTERIOR_SDE.md.
    """
    from theorems.weighted_two_erasure_cascade import verify_general_degree_witness
    validate_family(prime, degree)
    for cap in (generator_attempt_cap, scalar_attempt_cap):
        if type(cap) is not int or cap < 1:
            raise ValueError("positive sampler caps required")
    compressed, rank = independent_columns_exact(columns, prime)
    required = odd_power_arity(rank, degree)
    if len(columns) < required:
        raise ValueError(f"need {required} columns at rank {rank} and degree {degree}")
    if not rank:
        weights = (1,)+(0,)*(len(columns)-1)
        verify_general_degree_witness(prime, columns, weights, degree)
        return OddPowerWitness(prime, degree, weights, rank, required)
    rng = random.SystemRandom() if rng is None else rng
    reps, generator_draws, generator_abort = _representatives(prime, degree, rng, generator_attempt_cap)
    closure = scalar_closure(prime, degree, reps, rng=rng, attempts=scalar_attempt_cap)
    characters = {pow(z, (prime-1)//degree, prime): i for i, z in enumerate(reps)}
    roots = {}
    nodes, axis_checks = 0, 0

    def classify(value):
        coset = characters[pow(value, (prime-1)//degree, prime)]
        power = value*pow(reps[coset], -1, prime) % prime
        if power not in roots:
            roots[power] = _field_root(prime, degree, power)
        return coset, roots[power]

    def build(start, level):
        nonlocal nodes, axis_checks
        if level == 0:
            return {(): {start: 1}}, {(): tuple(compressed[start])}
        nodes += 1
        child_size = prod((degree-1)**j*rank+1 for j in range(level-1))
        child_count = (degree-1)**(level-1)*rank+1
        children = [build(start+k*child_size, level-1) for k in range(child_count)]
        keys = tuple(product(range(degree), repeat=level-1))
        # Axis constraints recover every last-index coordinate. Only the
        # (d-1)^(level-1) independent coordinates enter the dependence solve.
        free_keys = tuple(product(range(degree-1), repeat=level-1))
        relation = _relation(prime, [tuple(x for key in free_keys for x in values[key])
                                     for _, values in children])
        first_coset, _ = classify(next(a for a in relation if a))
        multiplier = reps[level-1]*pow(reps[first_coset], -1, prime) % prime
        relation = tuple(a*multiplier % prime for a in relation)
        cells = {key: {} for key in product(range(degree), repeat=level)}
        values = {key: [0]*rank for key in cells}
        for coefficient, (child_cells, child_values) in zip(relation, children):
            if not coefficient:
                continue
            coset, root = classify(coefficient)
            power = pow(root, degree, prime)
            for key in keys:
                output = key+(coset,)
                cells[output].update({i: root*b % prime for i, b in child_cells[key].items()})
                for j in range(rank):
                    values[output][j] = (values[output][j]+power*child_values[key][j]) % prime
        if not cells[tuple(range(level))]:
            raise ArithmeticError("lost the nonempty distinguished representation")
        for axis in range(level):
            for rest in product(range(degree), repeat=level-1):
                axis_keys = [rest[:axis]+(s,)+rest[axis:] for s in range(degree)]
                if any(sum(reps[s]*values[axis_keys[s]][j] for s in range(degree)) % prime
                       for j in range(rank)):
                    raise ArithmeticError("invalid collision tensor axis relation")
                axis_checks += 1
        return cells, values

    cells, values = build(0, degree-1)
    minor_terms = [tuple((key, _sign(key)) for key in permutations([j for j in range(degree) if j != i]))
                   for i in range(degree)]
    minors = [tuple(sum(sign*values[key][j] for key, sign in terms) % prime for j in range(rank))
              for terms in minor_terms]
    for i in range(degree):
        if any((reps[-1]*minors[i][j]-(-1)**(degree-1-i)*reps[i]*minors[-1][j]) % prime
               for j in range(rank)):
            raise ArithmeticError("invalid alternating minor relation")
    weights = [0]*len(columns)
    for scale, terms in zip(closure.scales, minor_terms):
        if not scale:
            continue
        for key, sign in terms:
            for index, root in cells[key].items():
                if weights[index]:
                    raise ArithmeticError("minor representations overlap")
                weights[index] = sign*scale*root % prime
    verify_general_degree_witness(prime, columns, weights, degree)
    return OddPowerWitness(prime, degree, tuple(weights), rank, required, nodes, axis_checks,
                           degree, len(roots)+1, generator_draws, closure.draws,
                           min(Fraction(1), generator_abort+closure.abort_bound))


def report():
    cases = []
    for prime, degree, rank in ((601, 5, 1), (601, 5, 2), (2**61-1, 5, 1)):
        rng = random.Random(20261028)
        count = odd_power_arity(rank, degree)
        columns = [tuple(int(i == j) for i in range(rank)) for j in range(rank)]
        columns += [tuple(rng.randrange(prime) for _ in range(rank)) for _ in range(count-rank)]
        result = odd_power_weights(prime, degree, columns, rng=rng)
        cases.append(dict(
            prime=prime, reduced_degree=degree, input_rank=result.compressed_rank,
            required_columns=result.required_columns,
            published_odd_degree_collision_bound=degree**(degree*(degree-1)//2)*(rank+1)**degree,
            compressed_full_depth_columns=count*((degree-1)**(degree-1)*rank+1),
            nonzero_scales=sum(bool(s) for s in result.weights), collision_nodes=result.collision_nodes,
            checked_axis_relations=result.checked_axis_relations,
            checked_minor_relations=result.checked_minor_relations,
            root_calls=result.root_calls, generator_draws=result.generator_draws,
            scalar_draws=result.scalar_draws,
            sampling_abort_bound=str(result.sampling_abort_bound),
            exact_original_moment_verified=True))
    return dict(
        status="SCOPED_ODD_POWER_SDE_CONSTRUCTION_NOT_QUANTUM_DISCOVERY",
        proof_note="research/ODD_POWER_EXTERIOR_SDE.md",
        scaffold_source="https://arxiv.org/html/1503.09016v2",
        scaffold_scope="Lemma12 and Theorem11; shorter exterior closure is a local deduction",
        input_promise="odd d>=3 dividing p-1; p>=4*((d-1)*(d-2))**2; arbitrary public columns",
        arity="product_{j=0}^{d-2} ((d-1)^j*r+1)", cases=cases,
        random_input_promise=False, input_labels_resampled=False, field_enumeration_used=False,
        even_degree_supported=False, all_prime_regimes_supported=False,
        backend_runtime_locally_clocked=False, quantum_receiver_implemented=False,
        novelty_established=False, speedup_claim_allowed=False)


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payload = json.dumps(report(), indent=2)+"\n"
    if args.write:
        (Path(__file__).resolve().parents[1]/"research/reductions/odd_power_sde.json").write_text(payload)
    print(payload, end="")
