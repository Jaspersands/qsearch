"""Paid copy-only principal-state source: budgets and finite channel controls.

This is not a quantum execution backend. Dense arrays below are test fixtures;
the proposed protocol receives IID copies, never a density-matrix description.
"""

from dataclasses import asdict, dataclass
from fractions import Fraction
from math import ceil

import numpy as np


def ceil_log2(x):
    x = Fraction(x)
    if x <= 0:
        raise ValueError("positive argument required")
    result = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    if Fraction(1 << result) < x:
        result += 1
    return result


@dataclass(frozen=True)
class SourceBudget:
    outputs: int
    gap: Fraction
    error: Fraction
    calibration_targets: int
    attempts_per_output: int
    target_cap: int
    phase_grid: int
    phase_bits: int
    median_repeats: int
    time_upper_bound: int
    program_copies_per_power: tuple
    program_copy_cap: int
    raw_copy_cap: int

    def receipt(self):
        data = asdict(self)
        data["gap"] = str(self.gap)
        data["error"] = str(self.error)
        data["simulation_diamond_bound"] = str(self.simulation_bound())
        data["ideal_bad_event_bound"] = str(3 * self.error / 8)
        data["gate_trace_distance_allowance"] = str(self.error / 8)
        data["whole_output_trace_distance_bound"] = str(5 * self.error / 8)
        data["physical_protocol_executed"] = False
        data["gap_verified"] = False
        data["speedup_claim"] = False
        return data

    def simulation_bound(self):
        per_qpe = sum(
            (Fraction(4 * (2 << j) ** 2, count)
             for j, count in enumerate(self.program_copies_per_power)),
            Fraction(0),
        )
        return self.target_cap * self.median_repeats * per_qpe


def source_budget(outputs, gap, error):
    """Conservative exact hard caps, polynomial in 1/gap (not log(1/gap))."""
    if isinstance(outputs, bool) or not isinstance(outputs, int) or outputs < 1:
        raise ValueError("outputs must be a positive integer")
    gap, error = Fraction(gap), Fraction(error)
    if not 0 < gap <= 1 or not 0 < error <= Fraction(1, 2):
        raise ValueError("require 0 < gap <= 1 and 0 < error <= 1/2")
    calibration = ceil(Fraction(ceil_log2(8 / error), 1) / gap)
    attempts = ceil(Fraction(ceil_log2(8 * outputs / error), 1) / gap)
    targets = calibration + outputs * attempts
    bits = ceil_log2(256 / gap)
    grid = 1 << bits
    repeats = 8 * ceil_log2(8 * targets / error) + 1
    time_bound = targets * repeats * 2 * (grid - 1)
    counts = tuple(ceil(16 * (2 << j) * time_bound / error) for j in range(bits))
    programs = targets * repeats * sum(counts)
    return SourceBudget(outputs, gap, error, calibration, attempts, targets,
                        grid, bits, repeats, time_bound, counts, programs,
                        targets + programs)


def _density(value):
    value = np.asarray(value, dtype=complex)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or not value.size:
        raise ValueError("square density matrix required")
    if not np.all(np.isfinite(value)):
        raise ValueError("finite density matrix required")
    if not np.allclose(value, value.conj().T, atol=1e-11):
        raise ValueError("Hermitian density matrix required")
    if not np.isclose(np.trace(value), 1, atol=1e-11):
        raise ValueError("unit trace required")
    if np.linalg.eigvalsh(value).min() < -1e-11:
        raise ValueError("positive density matrix required")
    return value


def controlled_collision(operator, program, angle):
    """Trace out one fresh program after exp(+i angle |1><1| tensor SWAP).

    Register order is control, reference, target. Linear on arbitrary operators;
    the program must be a density matrix independent of all three registers.
    """
    program = _density(program)
    operator = np.asarray(operator, dtype=complex)
    d = len(program)
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1]:
        raise ValueError("square operator required")
    if operator.shape[0] % (2 * d):
        raise ValueError("incompatible control/reference/target dimensions")
    if not np.isfinite(angle):
        raise ValueError("finite angle required")
    r = operator.shape[0] // (2 * d)
    if r < 1:
        raise ValueError("empty reference dimension")
    rd = r * d
    a, b = operator[:rd, :rd], operator[:rd, rd:]
    c, e = operator[rd:, :rd], operator[rd:, rd:]
    lifted = np.kron(np.eye(r), program)
    marginal = np.trace(e.reshape(r, d, r, d), axis1=1, axis2=3)
    cs, sn = np.cos(angle), np.sin(angle)
    return np.block([
        [a, cs * b - 1j * sn * b @ lifted],
        [cs * c + 1j * sn * lifted @ c,
         cs * cs * e + sn * sn * np.kron(marginal, program)
         + 1j * cs * sn * (lifted @ e - e @ lifted)],
    ])


def controlled_ideal(operator, program, time):
    program = _density(program)
    d = len(program)
    r = len(operator) // (2 * d)
    values, vectors = np.linalg.eigh(program)
    unitary = (vectors * np.exp(1j * time * values)) @ vectors.conj().T
    action = np.kron(np.eye(r), unitary)
    full = np.block([[np.eye(r * d), np.zeros_like(action)],
                     [np.zeros_like(action), action]])
    return full @ operator @ full.conj().T


def trace_distance(a, b):
    return float(np.linalg.svd(a - b, compute_uv=False).sum() / 2)


def phase_probabilities(eigenvalue, grid):
    """Ideal QPE distribution for phase (1+lambda)/4; finite test only."""
    if not 0 <= eigenvalue <= 1 or grid < 2 or grid & (grid - 1):
        raise ValueError("invalid eigenvalue or power-of-two grid")
    phase = (1 + eigenvalue) / 4
    delta = phase - np.arange(grid) / grid
    amplitude = np.sinc(grid * delta) / np.sinc(delta)
    probabilities = amplitude ** 2
    return probabilities / probabilities.sum()


def finite_qpe(program, grid, copies_per_power=None):
    """Dense subnormalized QPE outcome states, with real partial-SWAP noise.

    None uses exact exponentiation as an independent ideal control. Positive
    copy counts use only fresh-copy collision channels; no ideal rho evolution
    occurs on that branch. This tiny diagnostic is not the full capped source.
    """
    program = _density(program)
    if grid < 2 or grid & (grid - 1) or grid > 128:
        raise ValueError("finite control needs power-of-two grid <=128")
    bits, d = grid.bit_length() - 1, len(program)
    if copies_per_power is not None:
        if len(copies_per_power) != bits or any(
            isinstance(n, bool) or not isinstance(n, int) or n < 1
            for n in copies_per_power
        ):
            raise ValueError("one positive copy count per controlled power")
    state = np.kron(np.ones((grid, grid)) / grid, program)
    for j in range(bits):
        order = [i for bit in (0, 1) for i in range(grid) if (i >> j) & 1 == bit]
        indices = np.array([i * d + k for i in order for k in range(d)])
        arranged = state[np.ix_(indices, indices)]
        time = np.pi * (1 << j) / 2
        if copies_per_power is None:
            arranged = controlled_ideal(arranged, program, time)
        else:
            n = copies_per_power[j]
            for _ in range(n):
                arranged = controlled_collision(arranged, program, time / n)
        offset = np.ones(grid * d, dtype=complex)
        offset[grid * d // 2:] = (1j) ** (1 << j)
        arranged = offset[:, None] * arranged * offset.conj()[None, :]
        state[np.ix_(indices, indices)] = arranged
    indices = np.arange(grid)
    inverse_fourier = np.exp(-2j * np.pi * np.outer(indices, indices) / grid)
    inverse_fourier /= np.sqrt(grid)
    action = np.kron(inverse_fourier, np.eye(d))
    state = action @ state @ action.conj().T
    return [state[i*d:(i+1)*d, i*d:(i+1)*d] for i in range(grid)]
