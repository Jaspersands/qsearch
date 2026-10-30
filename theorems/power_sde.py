"""Two-level symmetric power-SDE contraction in a certified large field.

Public arbitrary labels, fixed reduced degree, capped classical draws.
No quantum receiver, novelty certificate, or enforced total arithmetic clock.
Proof and limitations: research/POWER_SDE_SYMMETRIC_CONTRACTION.md.
"""
from dataclasses import dataclass
from fractions import Fraction
import random

from theorems.cubic_diagonal_solver import _relation
from theorems.nil3_guarded_cyclic_dispatch import independent_columns_exact
from theorems.odd_power_sde import _representatives
from theorems.prime_character_opi import ring
from theorems.scalar_fermat_solver import _field_root


def _degree(degree):
    if type(degree) is not int or degree < 2:
        raise ValueError("integer reduced degree >=2 required")


def field_threshold(degree):
    _degree(degree)
    return 16*degree**(2*degree+2)


def validate_family(prime, degree):
    ring(prime)
    _degree(degree)
    if (prime-1) % degree:
        raise ValueError("reduced degree must divide prime-1")
    if prime < field_threshold(degree):
        raise ValueError("field is below the certified symmetric-contraction regime")


def power_arity(rank, degree):
    _degree(degree)
    if type(rank) is not int or rank < 0:
        raise ValueError("nonnegative integer rank required")
    return (rank+1)*((degree-1)*rank+1)


def _root(prime, degree, value, root_solver=None):
    root = (root_solver or _field_root)(prime, degree, value)
    if type(root) is not int or not 0 < root < prime or pow(root, degree, prime) != value:
        raise ArithmeticError("invalid nonzero power root")
    return root


@dataclass(frozen=True)
class SymmetricClosure:
    offsets: tuple[int, ...]
    roots: tuple[tuple[int, ...], ...]
    stage_draws: tuple[int, ...]
    stage_caps: tuple[int, ...]
    stage_success_bounds: tuple[Fraction, ...]
    abort_bound: Fraction
    root_calls: int


def symmetric_closure(prime, degree, representatives, *, rng=None, sampler_bits=32,
                      root_solver=None):
    """Sample t_i with every z_i*z_j*(t_i+t_j) a nonzero dth power.

    Stage j has j+1 distinct affine character constraints. The field guard
    certifies success >=1/(2*d**(j+1)), conditionally on EVERY earlier prefix.
    Union scalar failure <=(d-1)*2**(-sampler_bits). The default root
    backend is not capped; a supplied callback owns its separate budget.
    """
    validate_family(prime, degree)
    if type(sampler_bits) is not int or sampler_bits < 1:
        raise ValueError("positive integer sampler_bits required")
    z = tuple(representatives)
    if (len(z) != degree or any(type(a) is not int or not 0 < a < prime for a in z)
            or len({pow(a, (prime-1)//degree, prime) for a in z}) != degree):
        raise ValueError("complete distinct nonzero power-coset representatives required")
    rng = random.SystemRandom() if rng is None else rng
    offsets = [pow(2*z[0]*z[0], -1, prime)]
    draws, caps, bounds = [], [], []
    for j in range(1, degree):
        k = j+1
        cap = 2*degree**k*sampler_bits
        for attempt in range(1, cap+1):
            t = rng.randrange(0, prime)
            if type(t) is not int or not 0 <= t < prime:
                raise ValueError("random source returned a noncanonical field element")
            if not t or t in offsets:
                continue
            values = [2*z[j]*z[j]*t % prime]
            values += [z[i]*z[j]*(t+offsets[i]) % prime for i in range(j)]
            if all(a and pow(a, (prime-1)//degree, prime) == 1 for a in values):
                offsets.append(t)
                draws.append(attempt)
                caps.append(cap)
                bounds.append(Fraction(1, 2*degree**k))
                break
        else:
            raise RuntimeError(f"bounded symmetric scalar sampler exhausted at stage {j}")
    roots = [[0]*degree for _ in range(degree)]
    cache = {1: 1}
    for i in range(degree):
        for j in range(i, degree):
            value = z[i]*z[j]*(offsets[i]+offsets[j]) % prime
            if not value or pow(value, (prime-1)//degree, prime) != 1:
                raise ArithmeticError("invalid symmetric coefficient")
            if value not in cache:
                cache[value] = _root(prime, degree, value, root_solver)
            roots[i][j] = roots[j][i] = cache[value]
    if roots[0][0] != 1:
        raise ArithmeticError("distinguished coefficient must remain one")
    return SymmetricClosure(tuple(offsets), tuple(map(tuple, roots)), tuple(draws),
                            tuple(caps), tuple(bounds),
                            min(Fraction(1), Fraction(degree-1, 2**sampler_bits)), len(cache)-1)


@dataclass(frozen=True)
class PowerWitness:
    prime: int
    degree: int
    weights: tuple[int, ...]
    compressed_rank: int
    required_columns: int
    checked_axis_relations: int = 0
    distinguished_support_size: int = 0
    distinguished_vector_zero: bool = False
    root_calls: int = 0
    generator_draws: int = 0
    closure: SymmetricClosure | None = None
    sampling_abort_bound: Fraction = Fraction(0)


def power_weights(prime, degree, columns, *, rng=None,
                  generator_attempt_cap=128, sampler_bits=32, root_solver=None,
                  first_level_width=None, first_level_relations=None):
    """Checked nonzero SDE witness using a two-level collision contraction.

    Default width rank+1 gives O_d(rank**2) columns. Wider supplied linear
    relations are verified and PRESERVED, not replaced by deterministic
    nullspace vectors. Their width and root cost must be charged by callers.
    """
    from theorems.weighted_two_erasure_cascade import verify_general_degree_witness
    validate_family(prime, degree)
    if type(generator_attempt_cap) is not int or generator_attempt_cap < 1:
        raise ValueError("positive generator cap required")
    if type(sampler_bits) is not int or sampler_bits < 1:
        raise ValueError("positive integer sampler_bits required")
    compressed, rank = independent_columns_exact(columns, prime)
    width = rank+1 if first_level_width is None else first_level_width
    if type(width) is not int or width < rank+1:
        raise ValueError("first-level width must be at least rank+1")
    blocks = (degree-1)*rank+1
    required = width*blocks if rank else 1
    if len(columns) < required:
        raise ValueError(f"need {required} columns at rank {rank} and degree {degree}")
    if first_level_relations is not None:
        first_level_relations = tuple(tuple(row) for row in first_level_relations)
        if not rank or len(first_level_relations) != blocks:
            raise ValueError("one supplied relation per positive-rank first-level block required")
        for index, relation in enumerate(first_level_relations):
            block = compressed[index*width:(index+1)*width]
            if (len(relation) != width or not any(relation)
                    or any(type(x) is not int or not 0 <= x < prime for x in relation)
                    or any(sum(a*col[j] for a,col in zip(relation, block)) % prime
                           for j in range(rank))):
                raise ValueError("invalid supplied first-level relation")
    if not rank:
        weights = (1,)+(0,)*(len(columns)-1)
        verify_general_degree_witness(prime, columns, weights, degree)
        return PowerWitness(prime, degree, weights, rank, required)
    rng = random.SystemRandom() if rng is None else rng
    z, generator_draws, generator_abort = _representatives(prime, degree, rng, generator_attempt_cap)
    closure = symmetric_closure(prime, degree, z, rng=rng, sampler_bits=sampler_bits,
                                root_solver=root_solver)
    characters = {pow(a, (prime-1)//degree, prime): i for i, a in enumerate(z)}
    root_cache = {}
    axis_checks = 0

    def classify(value):
        coset = characters[pow(value, (prime-1)//degree, prime)]
        power = value*pow(z[coset], -1, prime) % prime
        if power not in root_cache:
            root_cache[power] = _root(prime, degree, power, root_solver)
        return coset, root_cache[power]

    def build(start, level):
        nonlocal axis_checks
        if level == 0:
            return {(): {start: 1}}, {(): tuple(compressed[start])}
        child_size = 1 if level == 1 else width
        count = width if level == 1 else blocks
        children = [build(start+i*child_size, level-1) for i in range(count)]
        keys = ((),) if level == 1 else tuple((i,) for i in range(degree))
        free_keys = keys if level == 1 else keys[:-1]
        if level == 1 and first_level_relations is not None:
            relation = first_level_relations[start//width]
        else:
            relation = _relation(prime, [tuple(x for key in free_keys for x in values[key])
                                         for _, values in children])
        first_coset, _ = classify(next(a for a in relation if a))
        multiplier = z[0]*pow(z[first_coset], -1, prime) % prime
        relation = tuple(a*multiplier % prime for a in relation)
        cells = {key+(i,): {} for key in keys for i in range(degree)}
        values = {key: [0]*rank for key in cells}
        for coefficient, (child_cells, child_values) in zip(relation, children):
            if not coefficient:
                continue
            coset, root = classify(coefficient)
            power = pow(root, degree, prime)
            for key in keys:
                out = key+(coset,)
                cells[out].update({i: root*b % prime for i, b in child_cells[key].items()})
                for j in range(rank):
                    values[out][j] = (values[out][j]+power*child_values[key][j]) % prime
        if not cells[(0,)*level]:
            raise ArithmeticError("lost distinguished representation support")
        for axis in range(level):
            rests = ((),) if level == 1 else tuple((i,) for i in range(degree))
            for rest in rests:
                axis_keys = [rest[:axis]+(i,)+rest[axis:] for i in range(degree)]
                if any(sum(z[i]*values[axis_keys[i]][j] for i in range(degree)) % prime
                       for j in range(rank)):
                    raise ArithmeticError("invalid collision tensor axis relation")
                axis_checks += 1
        return cells, values

    cells, values = build(0, 2)
    if any(sum(pow(closure.roots[i][j], degree, prime)*values[i, j][a]
               for i in range(degree) for j in range(degree)) % prime for a in range(rank)):
        raise ArithmeticError("symmetric contraction did not vanish")
    weights = [0]*len(columns)
    for (i, j), cell in cells.items():
        for index, root in cell.items():
            if weights[index]:
                raise ArithmeticError("collision representation supports overlap")
            weights[index] = closure.roots[i][j]*root % prime
    verify_general_degree_witness(prime, columns, weights, degree)
    return PowerWitness(prime, degree, tuple(weights), rank, required, axis_checks,
                        len(cells[0, 0]), not any(values[0, 0]), len(root_cache)+closure.root_calls,
                        generator_draws, closure,
                        min(Fraction(1), generator_abort+closure.abort_bound))


def report():
    cases = []
    for prime, degree, rank in ((2**61-1, 5, 2), (2**61-1, 5, 8),
                                (2**128-275, 4, 3), (65537, 2, 3)):
        rng = random.Random(20261028)
        count = power_arity(rank, degree)
        columns = [tuple(int(i == j) for i in range(rank)) for j in range(rank)]
        columns += [tuple(rng.randrange(prime) for _ in range(rank)) for _ in range(count-rank)]
        result = power_weights(prime, degree, columns, rng=rng)
        cases.append(dict(prime=prime, reduced_degree=degree, input_rank=result.compressed_rank,
                          required_columns=result.required_columns,
                          minus_one_is_power=pow(prime-1, (prime-1)//degree, prime) == 1,
                          nonzero_scales=sum(bool(s) for s in result.weights),
                          distinguished_support_size=result.distinguished_support_size,
                          distinguished_vector_zero=result.distinguished_vector_zero,
                          checked_axis_relations=result.checked_axis_relations,
                          root_calls=result.root_calls, generator_draws=result.generator_draws,
                          scalar_stage_draws=list(result.closure.stage_draws),
                          scalar_stage_caps=list(result.closure.stage_caps),
                          scalar_stage_success_lower_bounds=list(map(str, result.closure.stage_success_bounds)),
                          sampling_abort_bound=str(result.sampling_abort_bound),
                          exact_original_moment_verified=True))
    return dict(status="SCOPED_SYMMETRIC_POWER_SDE_NOT_QUANTUM_DISCOVERY",
                proof_note="research/POWER_SDE_SYMMETRIC_CONTRACTION.md",
                scaffold_source="https://arxiv.org/html/1503.09016v2",
                character_bound_source="https://arxiv.org/html/2403.04312v2#S2",
                input_promise="d>=2 divides p-1; p>=16*d**(2*d+2); arbitrary public columns",
                arity="(r+1)*((d-1)*r+1)", cases=cases,
                random_input_promise=False, input_labels_resampled=False, field_enumeration_used=False,
                even_degree_supported=True, all_prime_regimes_supported=False,
                degree_uniform_polynomial_time=False, backend_runtime_locally_clocked=False,
                quantum_receiver_implemented=False, novelty_established=False, speedup_claim_allowed=False)
