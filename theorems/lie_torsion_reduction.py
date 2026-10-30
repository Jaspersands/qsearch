"""Exact public arithmetic for the p-torsion Lie algebra of an explicit ring.

The tensor convention is [e_i, e_j]_k = structure_constants[i][j][k], with
coordinate k reduced modulo p**exponents[k]. This computes L[p], not L/pL;
in general [L[p], L[p]] is only a subgroup of L'[p]. No hidden-subgroup
recovery, outer reduction, quantum execution, or field source is implemented.
"""
from collections.abc import Mapping
from dataclasses import dataclass

from theorems.pilot_submodule import compile_pilot_frame
from theorems.prime_power_rees_descent import _module_contract


@dataclass(frozen=True)
class PTorsionReduction:
    """Computed frames include gamma_1 and the terminal zero term.

    torsion_embedding is column-wise: column i is p**(e_i-1) times ambient
    basis vector i. Frame lattice matrices use the pilot compiler's row-wise
    storage of column bases. Intrinsic exponents are Smith-factor exponents,
    not coordinates in the original ambient ordering.
    """

    prime: int
    exponents: tuple
    structure_constants: tuple
    torsion_embedding: tuple
    field_structure_constants: tuple
    original_lower_central_frames: tuple
    torsion_lower_central_frames: tuple
    public_arithmetic_only: bool = True
    original_hidden_subgroup_recovered: bool = False
    full_outer_reduction_implemented: bool = False

    @property
    def original_lower_central_exponents(self):
        return tuple(frame.intrinsic_exponents for frame in self.original_lower_central_frames)

    @property
    def original_class(self):
        return len(self.original_lower_central_frames) - 1

    @property
    def derived_rank(self):
        return len(self.original_lower_central_frames[1].active_indices)

    @property
    def torsion_lower_central_dimensions(self):
        return tuple(len(frame.active_indices) for frame in self.torsion_lower_central_frames)

    @property
    def torsion_class(self):
        return len(self.torsion_lower_central_frames) - 1


def _sequence(value, name):
    if isinstance(value, (str, bytes, Mapping)):
        raise ValueError(f"{name} must be a sequence of exact integer data")
    try:
        return tuple(value)
    except TypeError as error:
        raise ValueError(f"{name} must be a sequence") from error


def _validate_lie(prime, exponents, structure_constants):
    exponents = _sequence(exponents, "exponents")
    n = len(exponents)
    _, exponents, moduli = _module_contract([(0,) * n], exponents, prime, 1)
    tensor = tuple(tuple(_sequence(row, "bracket vector")
                         for row in _sequence(plane, "bracket plane"))
                   for plane in _sequence(structure_constants, "structure_constants"))
    if len(tensor) != n or any(len(plane) != n for plane in tensor):
        raise ValueError("an n-by-n-by-n bracket tensor is required")
    _module_contract([row for plane in tensor for row in plane], exponents, prime, 1)
    for i in range(n):
        for j in range(n):
            for k, modulus in enumerate(moduli):
                value = tensor[i][j][k]
                if moduli[i] * value % modulus or moduli[j] * value % modulus:
                    raise ValueError("bracket violates cyclic-order compatibility")
    for i in range(n):
        if any(tensor[i][i]):
            raise ValueError("alternating bracket requires [e_i,e_i]=0")
        for j in range(i + 1, n):
            if any((tensor[i][j][k] + tensor[j][i][k]) % modulus
                   for k, modulus in enumerate(moduli)):
                raise ValueError("alternating bracket requires skew symmetry")

    # Once alternation holds, repeated-index Jacobi identities cancel exactly.
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for coordinate, modulus in enumerate(moduli):
                    jacobi = sum(
                        tensor[j][k][a] * tensor[i][a][coordinate]
                        + tensor[k][i][a] * tensor[j][a][coordinate]
                        + tensor[i][j][a] * tensor[k][a][coordinate]
                        for a in range(n)
                    )
                    if jacobi % modulus:
                        raise ValueError("Jacobi identity fails in the stated mixed module")
    return exponents, moduli, tensor


def _lower_central_series(prime, exponents, moduli, tensor):
    """Generate gamma_(r+1)=[gamma_r,L], using at most sum(e_i) drops."""
    n = len(exponents)
    units = tuple(tuple(int(i == j) for i in range(n)) for j in range(n))
    frame = compile_pilot_frame(prime=prime, ambient_exponents=exponents,
                                pilot_columns=units)
    frames = [frame]
    length = sum(frame.intrinsic_exponents)
    for _ in range(sum(exponents)):
        columns = tuple(tuple(frame.lattice_basis[i][j] % moduli[i] for i in range(n))
                        for j in range(n))
        brackets = tuple(dict.fromkeys(
            tuple(sum(column[i] * tensor[i][j][k] for i in range(n)) % modulus
                  for k, modulus in enumerate(moduli))
            for column in columns if any(column) for j in range(n)
        ))
        brackets = tuple(column for column in brackets if any(column))
        if any(frame.encode(column) is None for column in brackets):
            raise ArithmeticError("lower central series failed exact module containment")
        next_frame = compile_pilot_frame(prime=prime, ambient_exponents=exponents,
                                         pilot_columns=brackets)
        next_length = sum(next_frame.intrinsic_exponents)
        frames.append(next_frame)
        if next_length == 0:
            return tuple(frames)
        if next_length == length:
            if next_frame.lattice_basis != frame.lattice_basis:
                raise ArithmeticError("equal-order nested modules have different canonical lattices")
            raise ValueError("Lie ring is not nilpotent: nonzero lower central term stabilizes")
        if next_length > length:
            raise ArithmeticError("lower central module order increased")
        frame, length = next_frame, next_length
    raise ArithmeticError("lower central series exceeded sum(exponents) strict drops")


def compile_p_torsion(*, prime, exponents, structure_constants):
    """Validate a nilpotent mixed-module Lie ring of class < p and compute L[p].

    The prime must be odd; exponents are nonempty positive Python integers.
    Tensor coordinates must be canonical Python integers, excluding bools.
    All spans and lower central terms are computed at full prime-power
    precision. No ambient group or field is enumerated.
    """
    exponents, moduli, tensor = _validate_lie(prime, exponents, structure_constants)
    original_frames = _lower_central_series(prime, exponents, moduli, tensor)
    original_class = len(original_frames) - 1
    if original_class >= prime:
        raise ValueError("Lazard scope requires nilpotency class < prime")

    n = len(exponents)
    scales = tuple(prime**(exponent - 1) for exponent in exponents)
    embedding = tuple(tuple(scales[i] if i == k else 0 for k in range(n)) for i in range(n))
    field_tensor = []
    for i in range(n):
        plane = []
        for j in range(n):
            bracket = tuple(scales[i] * scales[j] * tensor[i][j][k] % modulus
                            for k, modulus in enumerate(moduli))
            if any(value % scale for value, scale in zip(bracket, scales)):
                raise ArithmeticError("torsion bracket is not divisible by its coordinate scales")
            if original_frames[1].encode(bracket) is None:
                raise ArithmeticError("torsion derived bracket is outside the original derived module")
            plane.append(tuple((value // scale) % prime for value, scale in zip(bracket, scales)))
        field_tensor.append(tuple(plane))
    field_exponents, field_moduli, field_tensor = _validate_lie(prime, (1,) * n, field_tensor)
    torsion_frames = _lower_central_series(prime, field_exponents, field_moduli, field_tensor)
    result = PTorsionReduction(prime, exponents, tensor, embedding, field_tensor,
                               original_frames, torsion_frames)
    if result.torsion_lower_central_dimensions[1] > result.derived_rank:
        raise ArithmeticError("torsion derived dimension exceeds original intrinsic derived rank")
    if result.torsion_class > result.derived_rank + 1:
        raise ArithmeticError("torsion nilpotency class exceeds derived rank plus one")
    return result


def report():
    """Public falsifiers and exact readout, not an outer HSP solver run."""
    from hashlib import sha256
    from pathlib import Path

    from theorems.mixed_abelian_readout import recover_annihilator
    from theorems.pilot_submodule import verify_pilot_frame

    cases = []
    fixtures = (
        ("heisenberg_prime_squared", 3, (2, 2, 2), {(0, 1): (0, 0, 1)}),
        ("heisenberg_quotient_mod_p", 3, (1, 1, 1), {(0, 1): (0, 0, 1)}),
        ("short_factors_survive", 3, (1, 1, 3), {(0, 1): (0, 0, 9)}),
        ("rank_one_class_four", 5, (4, 4), {(0, 1): (0, 5)}),
        ("rank_one_class_128", 131, (128, 128), {(0, 1): (0, 131)}),
        ("small_prime_field_class_three", 5, (1, 1, 1, 1),
         {(0, 1): (0, 0, 1, 0), (0, 2): (0, 0, 0, 1)}),
        ("field_class_three", 163, (1, 1, 1, 1),
         {(0, 1): (0, 0, 1, 0), (0, 2): (0, 0, 0, 1)}),
    )
    for name, prime, exponents, brackets in fixtures:
        n = len(exponents)
        tensor = [[[0]*n for _ in range(n)] for _ in range(n)]
        for (i, j), vector in brackets.items():
            tensor[i][j] = list(vector)
            tensor[j][i] = [-x % prime**e for x, e in zip(vector, exponents)]
        result = compile_p_torsion(prime=prime, exponents=exponents, structure_constants=tensor)
        frames = result.original_lower_central_frames+result.torsion_lower_central_frames
        if not all(verify_pilot_frame(frame) for frame in frames):
            raise ArithmeticError("computed lower-central frame failed replay")
        rank = result.derived_rank
        core = ("PUBLISHED_ABELIAN" if rank == 0 else "PUBLISHED_NIL2" if rank == 1
                else "PUBLISHED_SMALL_COMMUTATOR" if prime < 16*(rank+1)**2
                else "CONDITIONAL_FIELD_REES")
        b = sum(exponents)
        cases.append(dict(
            name=name, prime=prime, exponents=exponents, structure_constants=tensor,
            original_class=result.original_class, derived_cyclic_rank=rank,
            original_lower_central_exponents=result.original_lower_central_exponents,
            torsion_class=result.torsion_class,
            torsion_lower_central_dimensions=result.torsion_lower_central_dimensions,
            torsion_embedding=result.torsion_embedding,
            field_structure_constants=result.field_structure_constants,
            lower_central_frames_verified=True,
            section_field_derived_dimension_upper=rank,
            section_field_class_upper=min(result.original_class, rank+1),
            local_solver_call_cap=b*(b+1)//2, proposed_core=core,
            original_hidden_subgroup_recovered=False,
        ))
    readout = []
    for name, p, exponents, labels in (
        ("ambient_mod_p_invisible", 3, (2, 3), [(3, 3), (0, 9)]),
        ("incomplete_fourier_span", 3, (1, 2), [(1, 0)]),
        ("complete_supplied_span_control", 3, (1, 2), [(1, 0), (0, 3)]),
        ("exponent_128", 3, (2, 128), [(3, 3**127)]),
    ):
        result = recover_annihilator(prime=p, ambient_exponents=exponents, fourier_labels=labels)
        readout.append(dict(name=name, result=result.certificate()))
    root = Path(__file__).resolve().parents[1]
    sources = (
        "theorems/lie_torsion_reduction.py", "tests/test_lie_torsion_reduction.py",
        "theorems/mixed_abelian_readout.py", "tests/test_mixed_abelian_readout.py",
        "theorems/pilot_submodule.py", "qsearch_cli/commands/sde.py",
        "tests/test_cli_parser_integrity.py",
        "research/UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md",
        "research/RANDOM_COLUMN_REES_PARAMETER_BOUND.md",
    )
    return dict(
        status="PUBLIC_RING_TO_FIELD_CONTROLS_NOT_HSP_EXECUTION",
        torsion_controls=cases, readout_controls=readout,
        conditional_parameter_bound="2^O(R log(R+2))*poly(full explicit input bits, log(1/epsilon))",
        source_sha256={p: sha256((root/p).read_bytes()).hexdigest() for p in sources},
        source_hashes_certify_proof=False, public_arithmetic_only=True,
        full_outer_reduction_implemented=False, field_core_newly_proved=False,
        quantum_receiver_implemented=False, original_oracle_queries_executed=0,
        candidate_promotion=False, proof_promotion=False, speedup_claim_allowed=False,
    )
