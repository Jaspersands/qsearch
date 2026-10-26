"""Interval certificate for a fixed-state coordinate heat-bath mixing obstruction.

No asymptotic, typical-start, tempering, or all-classical-algorithm lower bound.
The starting witness is inherited, not searched for by this producer.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import gcd
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import acb, arb, ctx, fmpq, nmod_mat
import numpy as np

from theorems import balanced_signed_mpi as mpi
from theorems.balanced_mpi_product_target import harmonic_certificate

REPORT = ROOT / "research/classical_baselines/balanced_mpi_heatbath_trap.json"
PORTFOLIO = ROOT / "research/phase_workbench/balanced_signed_mpi.json"


def ball(value):
    q = Q(value)
    return arb(fmpq(q.numerator, q.denominator))


def upper(value):
    if not value.is_finite():
        raise ArithmeticError("nonfinite interval")
    return Q(str(value.upper().fmpq()))


def lower(value):
    if not value.is_finite():
        raise ArithmeticError("nonfinite interval")
    return Q(str(value.lower().fmpq()))


def coefficients(residuals, order, t, harmonics):
    """Rigorous complex coefficients for half of each conjugate harmonic pair."""
    harmonic_certificate(len(residuals), t, harmonics)
    if type(order) is not int or order <= 3 or order % 2 == 0:
        raise ValueError("odd integer cyclic order greater than three required")
    if any(type(v) is not int for v in residuals):
        raise ValueError("integer residuals required")
    ratio = (ball(2*t).sqrt() /
             (ball(1-t).sqrt()+ball(1-3*t).sqrt()))
    roots = [acb(ball(Q(2*j, order))).exp_pi_i() for j in range(order)]
    return [
        [roots[(k*r) % order] * (2*(-1)**(k+1)*ratio**k/k)
         for r in residuals]
        for k in range(1, harmonics+1)
    ]


def interval_line(coeffs, slopes, order):
    """Rigorous inverse DFT of the harmonic log density, with constant omitted."""
    if any(len(row) != len(slopes) for row in coeffs):
        raise ValueError("one slope per row coefficient required")
    spectrum = [acb(0) for _ in range(order)]
    for k, row in enumerate(coeffs, 1):
        for coefficient, slope in zip(row, slopes):
            frequency = k*int(slope) % order
            spectrum[frequency] += coefficient
            spectrum[-frequency % order] += coefficient.conjugate()
    transformed = acb.dft(spectrum, inverse=True)
    if any(not value.imag.contains(0) for value in transformed):
        raise ArithmeticError("interval DFT failed conjugate symmetry")
    return [value.real*order for value in transformed]


def escape_log_upper(values, log_tail):
    """P(leave the current state) <= exp(returned bound), for this heat bath."""
    if len(values) < 2 or log_tail < 0:
        raise ValueError("nontrivial line and nonnegative log-tail bound required")
    peak = max(value.upper() for value in values[1:])
    return upper(arb(len(values)-1).log() + peak - values[0].lower() + 2*ball(log_tail))


def stationary_log_upper(base_value, log_tail, order, dimension, *, primitive_rows):
    """Jensen bound for odd N and surjective row maps, independent of full rank."""
    if not primitive_rows:
        raise ValueError("row-map surjectivity must be verified")
    if type(order) is not int or order <= 3 or order % 2 == 0:
        raise ValueError("odd cyclic order greater than three required")
    if type(dimension) is not int or dimension < 1 or log_tail < 0:
        raise ValueError("positive dimension and nonnegative tail required")
    return upper(base_value + ball(log_tail) - dimension*arb(order).log())


def dyadic_log_test(log_upper, bits):
    if type(bits) is not int or bits < 0:
        raise ValueError("nonnegative dyadic exponent required")
    return upper(ball(log_upper)+bits*arb(2).log()) <= 0


def finite_time_tv_lower(escape_bits, stationary_bits, steps_bits):
    if any(type(v) is not int or v < 0 for v in
           (escape_bits, stationary_bits, steps_bits)):
        raise ValueError("nonnegative integer exponents required")
    return max(Q(0), 1-Q(2)**(steps_bits-escape_bits)-Q(1, 2**stationary_bits))


def native_report(portfolio_path=PORTFOLIO, *, progress=None):
    data = portfolio_path.read_bytes()
    source = json.loads(data)["matched_classical_portfolio"]
    if (source["bits"], source["length"], source["evaluations"]) != (13, 6000, 420):
        raise ValueError("this certificate is predeclared for the native 6000-by-420 witness")
    bits, m, n, order = 13, 6000, 420, 8191
    t, harmonics, precision = Q(1, 20), 9, 96
    escape_bits, stationary_bits, steps_bits = 256, 256, 250
    supports, evaluations = mpi.points(bits, m, n)
    _, logs, generator = mpi.presentation(bits)
    matrix = np.array(logs, dtype=np.int64)[
        np.bitwise_xor(np.array(supports)[:, None], np.array(evaluations)[None, :])]
    rng = random.Random(source["center_seed"])
    centers = np.array([rng.randrange(order) for _ in range(m)], dtype=np.int64)
    if hashlib.sha256(centers.tobytes()).hexdigest() != source["centers_sha256"]:
        raise ArithmeticError("center replay does not match the source witness")
    assignment = np.array(source["best_assignment"], dtype=np.int64)
    if assignment.shape != (n,) or np.any(assignment < 0) or np.any(assignment >= order):
        raise ValueError("invalid saved native assignment")
    values = matrix @ assignment % order
    if values.tolist() != list(mpi.fast_public_matvec(bits, supports, evaluations, assignment.tolist())):
        raise ArithmeticError("independent public matrix products disagree")
    residuals = ((values-centers) % order).tolist()
    score = float(np.cos(2*np.pi*np.array(residuals)/order).mean())
    if abs(score-source["best_mean_cosine"]) > 1e-12:
        raise ArithmeticError("saved score replay failed")
    primitive = all(gcd(order, *(int(v) for v in row)) == 1 for row in matrix)
    cert = harmonic_certificate(m, t, harmonics)
    tail = Q(cert["uniform_log_weight_error_upper"])
    line_bounds = []
    with ctx.workprec(precision):
        coeffs = coefficients(residuals, order, t, harmonics)
        for j in range(n):
            line = interval_line(coeffs, matrix[:, j].tolist(), order)
            if j == 0:
                base = line[0]
                mass_log = stationary_log_upper(
                    base, tail, order, n, primitive_rows=primitive)
            elif not line[0].overlaps(base):
                raise ArithmeticError("line bases disagree as intervals")
            bound = escape_log_upper(line, tail)
            line_bounds.append(str(bound))
            if progress and (j+1) % 20 == 0:
                progress({"coordinates_checked": j+1, "of": n,
                          "largest_exit_log_upper": float(max(map(Q, line_bounds)))})
        maximum = max(map(Q, line_bounds))
        escape_ok = dyadic_log_test(maximum, escape_bits)
        mass_ok = dyadic_log_test(mass_log, stationary_bits)
        # A full floating diagnostic selected this direction; its saved
        # probability bound comes only from a new interval replay.
        basis_column, step = 238, 2539
        inverse = np.array(nmod_mat(matrix[:n].tolist(), order).inv().tolist(), dtype=np.int64)
        if not np.array_equal(matrix[:n] @ inverse % order, np.eye(n, dtype=np.int64)):
            raise ArithmeticError("systematic basis inverse failed exact replay")
        direction = inverse[:, basis_column]
        systematic = interval_line(coeffs, (matrix @ direction % order).tolist(), order)
        gain = systematic[step]-systematic[0]
        ratio_lower = (gain-2*ball(tail)).exp()
        exit_lower = lower(ratio_lower/(1+ratio_lower))
        systematic_control = {
            "information_rows": "0..419", "basis_column": basis_column,
            "step": step, "direction": direction.tolist(),
            "full_log_weight_gain_interval": [
                str(lower(gain-2*ball(tail))), str(upper(gain+2*ball(tail)))],
            "conditional_exit_probability_lower": str(exit_lower),
            "conditional_exit_at_least_2_to_minus_17_verified": exit_lower >= Q(1, 2**17),
            "random_scan_exit_probability_lower": str(exit_lower/n),
            "expected_first_exit_updates_upper": str(Q(n, 1)/exit_lower) if exit_lower > 0 else None,
            "move_selection": "complete 420-direction floating diagnostic, then interval replay",
            "mixing_time_upper_bound_claimed": False,
            "score_threshold_reached_claimed": False,
        }
    conclusion = escape_ok and mass_ok
    return {
        "schema": "balanced_mpi_heatbath_trap_v1",
        "status": "finite_fixed_start_mixing_obstruction" if conclusion else "not_certified",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_portfolio_artifact_sha256": hashlib.sha256(data).hexdigest(),
        "source_method": source["best_method"],
        "field_bits": bits, "cyclic_order": order, "length": m, "dimension": n,
        "field_modulus_coefficients": list(map(int, mpi.field(bits).modulus().coeffs())),
        "generator_encoding": generator,
        "support_encoding": "0..5999", "evaluation_encoding": "6000..6419",
        "center_seed": source["center_seed"],
        "centers": centers.tolist(), "assignment": assignment.tolist(),
        "replayed_mean_cosine": score,
        "active_probability": str(t), "harmonics": harmonics,
        "precision_bits": precision, "primitive_rows_verified": primitive,
        "harmonic_certificate": cert,
        "coordinate_log_exit_upper_bounds": line_bounds,
        "maximum_log_exit_upper": str(maximum),
        "stationary_state_log_mass_upper": str(mass_log),
        "escape_bound_bits": escape_bits, "escape_bound_verified": escape_ok,
        "stationary_mass_bound_bits": stationary_bits,
        "stationary_mass_bound_verified": mass_ok,
        "steps_exponent": steps_bits,
        "tv_lower_after_2_to_steps_exponent":
            str(finite_time_tv_lower(escape_bits, stationary_bits, steps_bits)) if conclusion else None,
        "chain": "random-scan original-coordinate exact product-target heat bath",
        "interval_fft_roundoff_included": True,
        "systematic_basis_escape_countercontrol": systematic_control,
        "typical_start_obstruction_proved": False,
        "systematic_basis_or_tempering_obstruction_proved": False,
        "asymptotic_mixing_lower_bound_proved": False,
        "classical_hardness_or_quantum_speedup_proved": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--portfolio", type=Path, default=PORTFOLIO)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = native_report(args.portfolio, progress=lambda item: print(json.dumps(item), flush=True))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in
                      ("status", "maximum_log_exit_upper", "escape_bound_verified",
                       "stationary_mass_bound_verified", "steps_exponent")}))


if __name__ == "__main__":
    main()
