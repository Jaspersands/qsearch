"""Physical qutrit pilot test: Hermitian completion and a matched MPS baseline.

U_j=Z_0...Z_(j-1) X_j, ZX=omega XZ, omega**2+omega+1=0.
H=sum c_j(U_j+U_j^dagger). Exact coefficients use integer pairs a+b*omega.
Dense powers are charged bounded calibrations, never an efficient source.
Given a pilot MPS of bond D, the actual Bell readout has bond <=3D across
paired output/reference sites. This permits classical energy contraction;
it does NOT simulate arbitrary quantum source circuits or all measurements.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
from typing import Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
ARTIFACT = ROOT / "research/classical_baselines/hermitian_qutrit_pilot.json"
OMEGA = np.exp(2j * np.pi / 3)
Eisenstein = tuple[int, int]


def ring_multiply(x: Eisenstein, y: Eisenstein) -> Eisenstein:
    a, b = x
    c, d = y
    return a * c - b * d, a * d + b * c - b * d


def phase_rotate(x: Eisenstein, phase: int) -> Eisenstein:
    a, b = x
    return ((a, b), (-b, a - b), (b - a, -a))[phase % 3]


def digits(index: int, m: int) -> tuple[int, ...]:
    return tuple((index // 3 ** j) % 3 for j in range(m))


def encode(values: Sequence[int]) -> int:
    return sum(v * 3 ** j for j, v in enumerate(values))


def _coefficients(coefficients: Sequence[int]) -> tuple[int, ...]:
    c = tuple(coefficients)
    if not c or any(type(x) is not int or abs(x) > 10 ** 6 for x in c):
        raise ValueError("explicit nonempty integer coefficients with abs<=10^6 required")
    return c


def power_tables(coefficients: Sequence[int], degree: int, *, hermitian: bool = True) -> tuple[list[dict[int, Eisenstein]], int]:
    """Expand H**k in the ordered orthogonal basis E_r=prod_j U_j**r_j.

    E_r U_j**s = omega**(s*sum_(l>j) r_l) E_(r+s*e_j).
    Using both s=+1,-1 is essential for Hermiticity.
    """
    c = _coefficients(coefficients)
    if len(c) > 8:
        raise ValueError("exponential exact reference capped at 8 sites; unsupported is not hard")
    if type(degree) is not int or not 0 <= degree <= 10:
        raise ValueError("exact reference degree must be 0..10")
    m, work = len(c), 0
    powers = [3 ** j for j in range(m)]
    tables = [{0: (1, 0)}]
    for _ in range(degree):
        output: dict[int, Eisenstein] = {}
        for index, value in tables[-1].items():
            r = digits(index, m)
            suffix = sum(r)
            for j, weight in enumerate(c):
                suffix -= r[j]
                for sign in ((-1, 1) if hermitian else (1,)):
                    dest = index + ((r[j] + sign) % 3 - r[j]) * powers[j]
                    a, b = phase_rotate(value, sign * suffix)
                    u, v = output.get(dest, (0, 0))
                    output[dest] = u + weight * a, v + weight * b
                    work += 1
        tables.append({index: value for index, value in output.items() if value != (0, 0)})
    return tables, work


def shifted_filter(tables: list[dict[int, Eisenstein]], shift: int) -> dict[int, Eisenstein]:
    """Coefficients of (shift*I-H)**degree, not an even-power ground filter."""
    degree = len(tables) - 1
    result: dict[int, Eisenstein] = {}
    for k, table in enumerate(tables):
        weight = math.comb(degree, k) * shift ** (degree - k) * (-1) ** k
        for index, (a, b) in table.items():
            u, v = result.get(index, (0, 0))
            result[index] = u + weight * a, v + weight * b
    return {i: value for i, value in result.items() if value != (0, 0)}


def coefficient_vector(table: dict[int, Eisenstein], m: int) -> np.ndarray:
    output = np.zeros(3 ** m, dtype=complex)
    for index, (a, b) in table.items():
        output[index] = a + b * OMEGA
    return output


def _mod_determinant(matrix: np.ndarray, p: int) -> int:
    a = matrix.copy()
    det = 1
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i, j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[[j, pivot]] = a[[pivot, j]]
            det = -det
        value = int(a[j, j])
        det = det * value % p
        for i in range(j + 1, len(a)):
            a[i] = (a[i] - (int(a[i, j]) * pow(value, -1, p) % p) * a[j]) % p
    return det % p


def schmidt_minor(table: dict[int, Eisenstein], m: int, cut: int, *, prime: int = 31, root: int = 5) -> dict:
    """Exact lower bound, not a numerical rank or an asymptotic upper bound.

    A nonzero determinant under Z[omega]->F_p, omega->root implies a
    nonzero characteristic-zero minor. The site order and basis are fixed.
    """
    if (prime, root) not in ((7, 2), (13, 3), (31, 5)) or not 0 < cut < m:
        raise ValueError("use a verified splitting prime/root and a nontrivial cut")
    left = 3 ** cut
    original = np.zeros((left, 3 ** (m - cut)), dtype=np.int64)
    for index, (a, b) in table.items():
        original[index % left, index // left] = (a + root * b) % prime
    a, row_ids, selected_rows, selected_cols = original.copy(), list(range(left)), [], []
    rank = 0
    for col in range(a.shape[1]):
        pivot = next((i for i in range(rank, left) if a[i, col]), None)
        if pivot is None:
            continue
        a[[rank, pivot]] = a[[pivot, rank]]
        row_ids[rank], row_ids[pivot] = row_ids[pivot], row_ids[rank]
        selected_rows.append(row_ids[rank])
        selected_cols.append(col)
        a[rank] = a[rank] * pow(int(a[rank, col]), -1, prime) % prime
        for i in range(rank + 1, left):
            if a[i, col]:
                a[i] = (a[i] - int(a[i, col]) * a[rank]) % prime
        rank += 1
        if rank == left:
            break
    minor = original[np.ix_(selected_rows, selected_cols)]
    det = _mod_determinant(minor, prime)
    assert det != 0 or rank == 0
    return {"cut": cut, "site_order": list(range(m)), "schmidt_rank_lower_bound": rank,
            "splitting_prime": prime, "omega_image": root,
            "rows": selected_rows, "columns": selected_cols, "determinant_mod_prime": det,
            "minor_entries_mod_prime": minor.tolist(),
            "not_an_asymptotic_or_rank_upper_bound": True}


def exact_small_minor(table: dict[int, Eisenstein], cut: int, witness: dict) -> Eisenstein:
    rows, cols = witness["rows"], witness["columns"]
    if len(rows) > 6:
        raise ValueError("permutation determinant is a bounded independent check")
    total = (0, 0)
    for permutation in itertools.permutations(range(len(rows))):
        product = (1, 0)
        for j, column in enumerate(permutation):
            product = ring_multiply(product, table.get(rows[j] + 3 ** cut * cols[column], (0, 0)))
        parity = sum(permutation[i] > permutation[j] for i in range(len(rows)) for j in range(i + 1, len(rows)))
        sign = (-1) ** parity
        total = total[0] + sign * product[0], total[1] + sign * product[1]
    return total


def weyl_matrix(x: Sequence[int], z: Sequence[int]) -> np.ndarray:
    """Native X**x Z**z action, little-endian qutrit coordinates."""
    m = len(x)
    if not 1 <= m <= 4 or len(z) != m or any(type(v) is not int or v not in (0, 1, 2) for v in (*x, *z)):
        raise ValueError("dense Weyl calibration requires 1..4 qutrits")
    d = 3 ** m
    result = np.zeros((d, d), dtype=complex)
    for b in range(d):
        b_digits = digits(b, m)
        row = encode([(u + v) % 3 for u, v in zip(x, b_digits)])
        result[row, b] = OMEGA ** (sum(u * v for u, v in zip(z, b_digits)) % 3)
    return result


def native_hamiltonian(coefficients: Sequence[int], *, hermitian: bool = True) -> np.ndarray:
    c = _coefficients(coefficients)
    h = np.zeros((3 ** len(c),) * 2, dtype=complex)
    for j, weight in enumerate(c):
        u = weyl_matrix([int(i == j) for i in range(len(c))], [int(i < j) for i in range(len(c))])
        h += weight * (u + u.conj().T if hermitian else u)
    return h


def bell_prepare(pilot: np.ndarray, m: int) -> np.ndarray:
    """Execute public label SUMs, per-qutrit Fourier and pairwise SUMs.

    The input pilot itself is NOT prepared efficiently by this dense routine.
    Its output matrix is the pure state across output/reference registers.
    """
    if not 1 <= m <= 4 or pilot.shape != (3 ** m,):
        raise ValueError("dense Bell calibration requires <=4 qutrits")
    d = 3 ** m
    state = np.zeros((d, d), dtype=complex)
    for r, amplitude in enumerate(pilot):
        r_digits = digits(r, m)
        z = [(sum(r_digits[j + 1:]) % 3) for j in range(m)]
        state[r, encode(z)] = amplitude
    tensor = state.reshape((d,) + (3,) * m)
    for axis in range(1, m + 1):
        tensor = np.fft.ifft(tensor, axis=axis) * math.sqrt(3)
    state = tensor.reshape(d, d)
    output = np.zeros_like(state)
    for r in range(d):
        for b in range(d):
            a = encode([(u + v) % 3 for u, v in zip(digits(r, m), digits(b, m))])
            output[a, b] = state[r, b]
    return output


def pilot_mps_reference(pilot: np.ndarray, m: int, tolerance: float = 1e-12) -> tuple[list[np.ndarray], float]:
    """CHARGED exponential TT-SVD reference, not a new scalable pilot source."""
    tensor = pilot.reshape((3,) * m, order="F")
    tensors, left, discarded = [], 1, 0.0
    for _ in range(m - 1):
        matrix = tensor.reshape(left * 3, -1)
        u, s, vh = np.linalg.svd(matrix, full_matrices=False)
        keep = max(1, int(np.sum(s > tolerance)))
        discarded += float(np.sum(s[keep:] ** 2))
        tensors.append(u[:, :keep].reshape(left, 3, keep))
        tensor = s[:keep, None] * vh[:keep]
        left = keep
    tensors.append(tensor.reshape(left, 3, 1))
    return tensors, discarded


def bell_mps_from_pilot(pilot_mps: Sequence[np.ndarray]) -> list[np.ndarray]:
    """Actual finite-charge construction: paired-site Choi bond <=3D.

    T_j[(alpha,s),(a,b),(beta,s+b)] = A_j[alpha,a-b,beta]*omega**((a-b)*s)/sqrt(3).
    Left charge is 0; all final charges are summed. No exponential pilot table
    or physical Hamiltonian matrix is accessed by this transformation.
    """
    if not pilot_mps:
        raise ValueError("nonempty pilot MPS required")
    result = []
    for j, a in enumerate(pilot_mps):
        if a.ndim != 3 or min(a.shape) < 1 or not np.all(np.isfinite(a)):
            raise ValueError("finite nonempty three-axis MPS tensors required")
        dl, physical, dr = a.shape
        if physical != 3 or (j == 0 and dl != 1) or (j == len(pilot_mps) - 1 and dr != 1):
            raise ValueError("open-boundary qutrit pilot MPS required")
        if j and dl != pilot_mps[j - 1].shape[2]:
            raise ValueError("inconsistent MPS bonds")
        first, last = j == 0, j == len(pilot_mps) - 1
        t = np.zeros((dl if first else 3 * dl, 9, dr if last else 3 * dr), dtype=complex)
        for s in ((0,) if first else range(3)):
            for output, reference in itertools.product(range(3), repeat=2):
                r, sp = (output - reference) % 3, (s + reference) % 3
                for alpha in range(dl):
                    for beta in range(dr):
                        l, right = (alpha if first else 3 * alpha + s), (beta if last else 3 * beta + sp)
                        t[l, 3 * output + reference, right] = a[alpha, r, beta] * OMEGA ** (r * s % 3) / math.sqrt(3)
        result.append(t)
    return result


def product_expectation(mps: Sequence[np.ndarray], local_operators: Sequence[np.ndarray]) -> complex:
    if len(mps) != len(local_operators):
        raise ValueError("one local observable per site required")
    environment = np.ones((1, 1), dtype=complex)
    for tensor, operator in zip(mps, local_operators):
        environment = np.einsum("ab,asr,st,btq->rq", environment, tensor.conj(), operator, tensor, optimize=True)
    return complex(environment[0, 0])


def mps_energy(mps: Sequence[np.ndarray], coefficients: Sequence[int], *, paired: bool = True) -> float:
    """Matched classical contraction, not a shot-based or dense simulator."""
    c = _coefficients(coefficients)
    if len(c) != len(mps):
        raise ValueError("one coefficient per paired site required")
    x = weyl_matrix([1], [0])
    z = weyl_matrix([0], [1])
    identity = np.eye(3)
    energy = 0.0
    for j, weight in enumerate(c):
        operators = [z if i < j else x if i == j else identity for i in range(len(c))]
        if paired:
            operators = [np.kron(operator, identity) for operator in operators]
        energy += 2 * weight * product_expectation(mps, operators).real
    norm = product_expectation(mps, [np.eye(9 if paired else 3)] * len(c)).real
    if not math.isfinite(norm) or norm <= 0:
        raise ValueError("nonzero finite pilot norm required")
    return float(energy / norm)


def product_pilot_control(m: int = 64) -> dict:
    """Live scalable baseline and independent closed form; not an H-filter source.

    For a product pilot f, <U_j> = prod_(i<j) E[omega**r_i] *
    sum_r conjugate(f_j(r+1))*f_j(r). This follows by LEFT multiplication
    U_j E_r=omega**sum_(i<j)r_i E_(r+e_j), independent of the MPS code.
    """
    local_vectors = []
    for j in range(m):
        # Uniform local probabilities would zero the very first character,
        # making every later term invisible. Keep all prefix probes live.
        f = np.array([16, 1 + j % 3, 1j * (1 + j % 5)], dtype=complex)
        local_vectors.append(f / np.linalg.norm(f))
    pilot_mps = [f.reshape(1, 3, 1) for f in local_vectors]
    paired = bell_mps_from_pilot(pilot_mps)
    c = [1 + j % 7 for j in range(m)]
    contracted = mps_energy(paired, c)
    pilot_energy = mps_energy(pilot_mps, c, paired=False)
    prefix, direct = 1 + 0j, 0.0
    for weight, f in zip(c, local_vectors):
        overlap = sum(f[(r + 1) % 3].conjugate() * f[r] for r in range(3))
        direct += 2 * weight * (prefix * overlap).real
        prefix *= sum(abs(f[r]) ** 2 * OMEGA ** r for r in range(3))
    return {"sites": m, "pilot_max_bond": 1, "paired_output_max_bond": max(t.shape[2] for t in paired),
            "local_vector_recipe": "normalize([16,1+j%3,i*(1+j%5)])", "coefficients": c,
            "classical_mps_energy": contracted, "independent_closed_form_energy": float(direct),
            "direct_pilot_mps_energy": pilot_energy,
            "intertwiner_energy_error": abs(pilot_energy - contracted),
            "final_prefix_character_magnitude": float(abs(prefix)),
            "absolute_error": float(abs(contracted - direct)), "exponential_pilot_or_state_table_used": False,
            "is_polynomial_H_filter_pilot": False, "certified_roundoff": False}


def native_control(coefficients: Sequence[int], degree: int) -> dict:
    c, m = _coefficients(coefficients), len(coefficients)
    tables, work = power_tables(c, degree)
    shift = 2 * sum(abs(x) for x in c)
    table = shifted_filter(tables, shift)
    vector = coefficient_vector(table, m)
    norm = np.linalg.norm(vector)
    if not np.isfinite(norm) or norm <= 0:
        raise ValueError("zero/nonfinite filter has no normalized pilot; not a hardness result")
    vector /= norm
    prepared = bell_prepare(vector, m)
    h = native_hamiltonian(c)
    p = np.linalg.matrix_power(shift * np.eye(len(h)) - h, degree)
    reference = p / np.linalg.norm(p)
    seed_filter = p[:, 0] / np.linalg.norm(p[:, 0])
    pilot_mps, discarded = pilot_mps_reference(vector, m)
    paired_mps = bell_mps_from_pilot(pilot_mps)
    rho = prepared @ prepared.conj().T
    energy = float(np.trace(rho @ h).real)
    contracted = mps_energy(paired_mps, c)
    pilot_contracted = mps_energy(pilot_mps, c, paired=False)
    pilot_energy = float(np.vdot(vector, h @ vector).real)
    return {"coefficients": list(c), "degree": degree, "shift": shift,
            "polynomial": "(shift*I-H)^degree", "group_algebra_transition_updates": work,
            "explicit_pilot_basis_size": 3 ** m, "explicit_pilot_preparation_is_exponential": True,
            "full_prepared_state_error": float(np.linalg.norm(prepared - reference)),
            "pilot_is_filtered_seed_column_error": float(np.linalg.norm(vector - seed_filter)),
            "native_pilot_energy": pilot_energy, "direct_pilot_mps_energy": pilot_contracted,
            "source_output_energy_error": abs(pilot_energy - energy),
            "native_output_energy": energy, "classical_mps_energy": contracted,
            "classical_energy_error": abs(energy - contracted),
            "pilot_max_bond": max(t.shape[2] for t in pilot_mps),
            "paired_output_max_bond": max(t.shape[2] for t in paired_mps),
            "pilot_reference_discarded_weight": discarded,
            "public_logical_qutrit_clifford_gates": m * (m - 1) // 2 + 2 * m,
            "certified_floating_point_roundoff": False,
            "efficient_pilot_source_or_ground_gap_proved": False}


def run_controls() -> dict:
    rank_controls = []
    minimal_table = None
    minimal_witness = None
    # Retain the initial six/eight-site exploratory inputs through degree10,
    # including saturation, rather than selecting a growing-rank prefix.
    for c, max_degree in (([2, 3, 5, 7], 2), ([1] * 6, 6),
                          ([2, 3, 5, 7, 11, 13], 10), ([2, 3, 5, 7, 11, 13, 17, 19], 10)):
        for hermitian in (False, True):
            tables, work = power_tables(c, max_degree, hermitian=hermitian)
            for k in range(1, max_degree + 1):
                witness = schmidt_minor(tables[k], len(c), len(c) // 2)
                rank_controls.append({"coefficients": c, "hermitian": hermitian, "degree": k,
                                      "witness": witness, "asymptotic_rank_fit_performed": False})
                if len(c) == 4 and k == 2 and hermitian:
                    minimal_table, minimal_witness = tables[k], witness
    exact_det = exact_small_minor(minimal_table, 2, minimal_witness)
    assert minimal_witness["schmidt_rank_lower_bound"] == 4 and exact_det != (0, 0)
    natives = [native_control([2, 3], 2), native_control([2, -3, 5], 3), native_control([1, 2, 3], 2)]
    scalable = product_pilot_control()
    directional_collapse = power_tables([2, 3, 5, 7], 3, hermitian=False)[0][3]
    assert directional_collapse == {0: (2 ** 3 + 3 ** 3 + 5 ** 3 + 7 ** 3, 0)}
    return {"schema_version": "hermitian-qutrit-pilot-v1", "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "literature": ["https://arxiv.org/abs/2604.01022", "https://arxiv.org/abs/2601.18773", "https://arxiv.org/abs/1310.6049"],
            "minimal_hermitian_degree_two_determinant": list(exact_det),
            "one_way_cubic_collapse": {"coefficients": [2, 3, 5, 7], "A_cubed_scalar": directional_collapse[0][0],
                                      "does_not_apply_to_A_plus_adjoint": True},
            "degree_plus_one_bond_transfer_falsified": True, "rank_controls": rank_controls,
            "native_controls": natives, "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NO_NOVELTY_CLAIM",
            "scalable_product_pilot_control": scalable,
            "conditional_classical_baseline": "If a polynomial-bond controlled-precision pilot MPS is constructible, the paired output has bond<=3D and energy is classically contractible",
            "source_as_solution_identity": "For this canonical family alpha(P(H))=P(H)|0>; the Bell isometry intertwines left U_j multiplication, so source and output have the same energy for ANY pilot",
            "new_quantum_algorithm_claimed": False, "central_candidate_or_negative_created": False,
            "all_native_controls_pass": all(c["full_prepared_state_error"] < 1e-11 and c["classical_energy_error"] < 1e-10 and c["pilot_is_filtered_seed_column_error"] < 1e-11 and c["source_output_energy_error"] < 1e-10 for c in natives) and scalable["absolute_error"] < 1e-10 and scalable["intertwiner_energy_error"] < 1e-10,
            "not_established": ["Efficient general Hermitian pilot preparation", "Asymptotic rank lower bound", "Worst-case classical hardness", "Ground-filter degree/gap guarantee", "Classical simulation of arbitrary non-MPS quantum sources"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        ARTIFACT.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({"native_controls_pass": report["all_native_controls_pass"],
                      "minimal_exact_determinant": report["minimal_hermitian_degree_two_determinant"],
                      "rank_controls": len(report["rank_controls"]), "new_quantum_algorithm_claimed": False}, indent=2))


if __name__ == "__main__":
    main()
