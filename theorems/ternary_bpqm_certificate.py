"""One-sided physical degradation certificates for signed ternary BPQM.

Exact simplex splitting and integer mass accounting, not Monte Carlo or a
finite-block quantum execution. Local derivation remains review pending.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from math import comb, isqrt, lcm
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.ternary_coloring_bpqm import PHYSICAL, error_bounds, spectrum

REPORT = ROOT/"research/phase_workbench/ternary_bpqm_certificate.json"


def canonical(values):
    values = tuple(values)
    return min(values[i:]+values[:i] for i in range(3))


def simplex_parts(numerators, denominator, grid):
    """Exact convex grid split: outputs (grid spectrum, integer branch mass).

    The returned masses sum to denominator. This linear identity of Gram
    matrices admits a frequency-controlled flag isometry followed by dephasing.
    """
    if denominator <= 0 or sum(numerators) != denominator or min(numerators) < 0:
        raise ValueError("exact normalized nonnegative spectrum numerators required")
    a, x = divmod(grid*numerators[0], denominator)
    b, y = divmod(grid*numerators[1], denominator)
    if x+y <= denominator:
        pieces = ((a, b, denominator-x-y), (a+1, b, x), (a, b+1, y))
    else:
        pieces = ((a+1, b+1, x+y-denominator),
                  (a+1, b, denominator-y), (a, b+1, denominator-x))
    result = []
    for i, j, mass in pieces:
        if mass:
            target = (i, j, grid-i-j)
            if min(target) < 0:
                raise ArithmeticError("simplex split left the probability simplex")
            result.append((target, mass))
    if sum(mass for _, mass in result) != denominator or any(
            sum(target[j]*mass for target, mass in result) != grid*numerators[j] for j in range(3)):
        raise ArithmeticError("simplex splitting does not preserve the exact Gram spectrum")
    return tuple(result)


@lru_cache(maxsize=400000)
def transitions(grid, left, right, kind):
    raw = defaultdict(int)
    if kind == "bit":
        weights = tuple(sum(left[(t-j) % 3]*right[j] for j in range(3)) for t in range(3))
        branches = [(weights, grid*grid)]
    elif kind == "check":
        branches = []
        for h in range(3):
            weights = tuple(left[(j+h) % 3]*right[j] for j in range(3))
            if sum(weights):
                branches.append((weights, sum(weights)))
    else:
        raise ValueError("bit or check node required")
    for weights, denominator in branches:
        for mu, mass in simplex_parts(weights, denominator, grid):
            raw[canonical(mu)] += mass
    if sum(raw.values()) != grid*grid:
        raise ArithmeticError("integer transition law lost branch probability")
    return tuple(sorted(raw.items()))


@dataclass(frozen=True)
class Law:
    grid: int
    bits: int
    weights: tuple

    def __post_init__(self):
        integer(self.grid, "ternary simplex grid", 6, 192)
        integer(self.bits, "mass precision", 16, 192)
        if self.grid % 6:
            raise ValueError("grid divisible by six preserves physical and perfect channels")
        seen = set()
        for mu, weight in self.weights:
            if (len(mu) != 3 or any(type(v) is not int or v < 0 for v in mu)
                    or sum(mu) != self.grid or mu != canonical(mu) or mu in seen
                    or type(weight) is not int or weight <= 0):
                raise ValueError("unique canonical grid spectra and positive integer masses required")
            seen.add(mu)
        if sum(weight for _, weight in self.weights) != 1 << self.bits:
            raise ValueError("exact normalized mass required")

    def fidelity_bounds(self, precision=80):
        integer(precision, "root precision", 16, 192)
        scale, lo, hi = 1 << precision, 0, 0
        for mu, weight in self.weights:
            a, b = mu[0]-mu[2], mu[1]-mu[2]
            radicand = (a*a-a*b+b*b)*scale*scale
            floor = isqrt(radicand)
            lo += weight*floor
            hi += weight*(floor+int(floor*floor != radicand))
        denominator = self.grid*scale*(1 << self.bits)
        return Fraction(lo, denominator), Fraction(hi, denominator)

    def error_upper(self):
        return sum(weight*error_bounds(tuple(Fraction(n, self.grid) for n in mu))[1]
                   for mu, weight in self.weights)/(1 << self.bits)


def point(mu, grid=24, bits=80):
    mu = spectrum(mu)
    integer(grid, "ternary simplex grid", 6, 192)
    integer(bits, "mass precision", 16, 192)
    if grid % 6:
        raise ValueError("grid divisible by six required")
    denominator = 1
    for value in mu:
        denominator = lcm(denominator, value.denominator)
    parts = simplex_parts(tuple(int(value*denominator) for value in mu), denominator, grid)
    probabilities = defaultdict(Fraction)
    for target, mass in parts:
        probabilities[canonical(target)] += Fraction(mass, denominator)
    return rounded_law(probabilities, grid, bits)


def rounded_law(probabilities, grid, bits):
    if sum(probabilities.values()) != 1:
        raise ArithmeticError("mass rounding requires a normalized exact input")
    scale = 1 << bits
    weights = {mu: (p*scale).__floor__() for mu, p in probabilities.items()}
    loss = scale-sum(weights.values())
    uninformative = canonical((grid, 0, 0))
    weights[uninformative] = weights.get(uninformative, 0)+loss
    return Law(grid, bits, tuple(sorted((mu, w) for mu, w in weights.items() if w)))


def coefficient_law(law, costs=None):
    """Actual independent uniform F_3^* coefficient, with its public flag.

    This is NOT a chosen permutation of a fixed problem. Any rounding loss
    is deliberately degraded to an uninformative channel.
    """
    raw = defaultdict(int)
    for mu, w in law.weights:
        raw[mu] += w
        raw[canonical((mu[0], mu[2], mu[1]))] += w
    weights = {mu: mass//2 for mu, mass in raw.items()}
    loss = (1 << law.bits)-sum(weights.values())
    if costs is not None:
        costs["rounding_loss_mass_units_total"] += loss
    weights[canonical((law.grid, 0, 0))] = weights.get(canonical((law.grid, 0, 0)), 0)+loss
    return Law(law.grid, law.bits, tuple(sorted((mu, w) for mu, w in weights.items() if w)))


def combine(left, right, kind, costs):
    if (left.grid, left.bits) != (right.grid, right.bits):
        raise ValueError("matching grid and precision required")
    G, L, raw = left.grid, 1 << left.bits, defaultdict(int)
    for mu, wa in left.weights:
        for nu, wb in right.weights:
            costs["message_pair_visits"] += 1
            for target, mass in transitions(G, mu, nu, kind):
                raw[target] += wa*wb*mass
    denominator = L*L*G*G
    if sum(raw.values()) != denominator:
        raise ArithmeticError("unnormalized actual node law")
    weights = {mu: value*L//denominator for mu, value in raw.items()}
    loss = L-sum(weights.values())
    if not 0 <= loss < len(raw)+1:
        raise ArithmeticError("dyadic mass-loss budget failed")
    costs["rounding_loss_mass_units_total"] += loss
    uninformative = canonical((G, 0, 0))
    weights[uninformative] = weights.get(uninformative, 0)+loss
    return Law(G, left.bits, tuple(sorted((mu, w) for mu, w in weights.items() if w)))


def tail_certificate(fidelity, dv, dc):
    f = Fraction(fidelity)
    if not 0 <= f <= 1:
        raise ValueError("mean fidelity upper bound required")
    # Published q-ary bound, with q=3 and physical F=1/2. Its polynomial
    # quotient is increasing, so this ONE finite upper bound controls the tail.
    integer(dv, "variable degree", 3, 6)
    integer(dc, "check degree", dv+1, 12)
    slope = sum(2**j*comb(dc-1, j)*f**(j-1) for j in range(1, dc))
    A = Fraction(1, 2)*slope**(dv-1)
    value = A*f**(dv-2)
    return {"certified": value < 1, "f_upper_exact": str(f),
            "A_upper_exact": str(A), "lambda_upper_exact": str(value),
            "tail_bound": "F_(L+t)<=f*lambda^(((dv-1)^t-1)/(dv-2))",
            "source": "https://arxiv.org/html/2609.05857v1#S5", "finite_block_error_inferred": False}


def frontier(*, dv=3, dc=6, grid=24, bits=80, iterations=24, progress=False):
    integer(dv, "variable degree", 3, 6)
    integer(dc, "check degree", dv+1, 12)
    integer(iterations, "iteration budget", 1, 64)
    physical = point(PHYSICAL, grid, bits)
    message, history, outputs = physical, [], 1
    costs = {"message_pair_visits": 0, "rounding_loss_mass_units_total": 0}
    certificate = None
    for level in range(1, iterations+1):
        incoming = coefficient_law(message, costs)
        check = incoming
        for _ in range(dc-2):
            check = combine(check, incoming, "check", costs)
        message = physical
        for _ in range(dv-1):
            message = combine(message, check, "bit", costs)
        _, hi = message.fidelity_bounds()
        candidate = tail_certificate(hi, dv, dc)
        outputs = 1+(dv-1)*(dc-1)*outputs
        row = {"level": level, "grid_states": len(message.weights),
               "mean_fidelity_upper_exact": str(hi), "symbol_error_upper_exact": str(message.error_upper()),
               "lambda_upper_exact": candidate["lambda_upper_exact"],
               "distinct_original_tree_outputs": outputs, "probability_mass_exact": "1"}
        history.append(row)
        if progress:
            print(json.dumps({"dv": dv, "dc": dc, "grid": grid, "level": level,
                              "F_upper_display_only": float(hi), "states": len(message.weights),
                              "certified": candidate["certified"]}), flush=True)
        if candidate["certified"]:
            certificate = dict(candidate, level=level)
            break
    return {"status": "SIGNED_TRINE_TREE_CONVERGENCE_CERTIFIED_REVIEW_PENDING" if certificate else "UNKNOWN_GRID_DEGRADATION_DID_NOT_CERTIFY",
            "variable_degree": dv, "check_degree": dc, "grid": grid, "mass_bits": bits,
            "history": history, "certificate": certificate, "costs": costs,
            "coefficient_model": "independent_uniform_nonzero_F3_socket_coefficients",
            "source_normalized_spectrum": ["0", "1/2", "1/2"], "source_overlap_exact": "-1/2",
            "asymptotic_block_theorem": "https://arxiv.org/html/2609.05857v1#S6",
            "source_matches_block_theorem_ensemble": "conditional_on_local_degradation_derivation_review",
            "finite_block_decoder_executed": False, "sampler_or_search_reduction_executed": False,
            "speedup_claim_allowed": False, "accepted_speedup_candidate": False}


def degradation_control(mu, grid=24):
    """Execute the frequency-controlled flag isometry, NOT free rounding."""
    import numpy as np
    from theorems.ternary_coloring_bpqm import state
    mu = spectrum(mu)
    denominator = lcm(*(p.denominator for p in mu))
    pieces = simplex_parts(tuple(int(p*denominator) for p in mu), denominator, grid)
    V = np.zeros((3*len(pieces), 3), complex)
    for j in range(3):
        if not mu[j]:
            V[j, j] = 1
        else:
            for h, (target, mass) in enumerate(pieces):
                V[3*h+j, j] = float(Fraction(mass*target[j], grid*denominator)/mu[j])**.5
    error = float(np.max(np.abs(V.conj().T @ V-np.eye(3))))
    for x in range(3):
        expected = np.concatenate([float(Fraction(mass, denominator))**.5*
                                   state(tuple(Fraction(t, grid) for t in target), x)
                                   for target, mass in pieces])
        actual = V @ state(mu, x)
        error = max(error, float(np.max(np.abs(actual-expected))))
        # Dephasing the flag keeps all blocks and their actual Born mass.
        for h, (target, mass) in enumerate(pieces):
            block = actual[3*h:3*h+3]
            psi = state(tuple(Fraction(t, grid) for t in target), x)
            error = max(error, float(np.max(np.abs(np.outer(block, block.conj())-
                                      float(Fraction(mass, denominator))*np.outer(psi, psi.conj())))))
    if error > 1e-11:
        raise ArithmeticError("claimed physical degradation isometry failed")
    return {"input_normalized_spectrum": list(map(str, mu)), "grid": grid,
            "split": [{"target": target, "probability_exact": str(Fraction(mass, denominator))}
                      for target, mass in pieces], "actual_isometry_amplitude_and_block_max_residual": error,
            "flag_dephasing_is_an_intentional_comparison_channel": True,
            "coherent_BPQM_receiver_compiler_inferred": False}


def native_constraint_control(spins, seed, *, timeout_ms=1000):
    """Classical search on the ORIGINAL signed socket-ensemble dual CSP.

    This does not infer uniform sampling from a SAT witness, and never
    filters parallel sockets, zero clauses, unsatisfiable inputs or timeouts.
    """
    integer(spins, "native ternary spins", 2, 256)
    integer(seed, "public input seed", 0, 2**32-1)
    integer(timeout_ms, "SAT millisecond cap", 1, 60000)
    clauses, rng = 2*spins, random.Random(seed)
    checks = [j for j in range(spins) for _ in range(6)]
    rng.shuffle(checks)
    sockets, forms = [], []
    for edge in range(clauses):
        coefficients = [0]*spins
        for j in checks[3*edge:3*edge+3]:
            a = rng.choice((1, 2))
            sockets.append((edge, j, a))
            coefficients[j] = (coefficients[j]+a) % 3
        forms.append(tuple(coefficients))
    offsets = tuple(rng.randrange(3) for _ in range(clauses))
    record = {"spins": spins, "clauses": clauses, "seed": seed, "sockets": sockets,
              "forms_H_transpose": forms, "original_offsets": offsets,
              "ensemble": "public_seeded_3_6_socket_generator_nonzero_coefficients_no_IID_certificate",
              "parallel_sockets_or_zero_forms_removed": False,
              "source_conditioned_on_satisfiability": False,
              "expected_solutions_uniform_offsets_exact": str(Fraction(3**spins*2**clauses, 3**clauses)),
              "classical_uniform_sampling_established": False,
              "quantum_sampler_executed": False, "speedup_claim_allowed": False}
    try:
        import z3
    except ImportError:
        return dict(record, status="UNKNOWN_Z3_BASELINE_UNAVAILABLE")
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    x = [z3.Int(f"x_{i}") for i in range(spins)]
    for value in x:
        solver.add(value >= 0, value < 3)
    for row, offset in zip(forms, offsets):
        solver.add((sum(a*value for a, value in zip(row, x))+offset) % 3 != 0)
    start = time.perf_counter()
    result = solver.check()
    record.update(solver="Z3", version=z3.get_version_string(), timeout_ms=timeout_ms,
                  solve_seconds=time.perf_counter()-start)
    if result == z3.sat:
        witness = tuple(solver.model().eval(value).as_long() for value in x)
        if not all((sum(a*v for a, v in zip(row, witness))+offset) % 3 for row, offset in zip(forms, offsets)):
            raise ArithmeticError("SAT witness fails the unchanged original ternary input")
        record.update(status="CLASSICAL_ORIGINAL_CSP_WITNESS", witness=witness)
    elif result == z3.unsat:
        record.update(status="SOLVER_UNSAT_NOT_INDEPENDENTLY_VERIFIED")
    else:
        record.update(status="UNKNOWN_SAT_TIMEOUT", reason_unknown=solver.reason_unknown())
    return record


def exclusion_readout_control():
    """Actual anti-trine effects and their SPECIFIC classical record channel.

    This does not exclude other readouts or classical CSP algorithms.
    """
    import numpy as np
    from math import log2
    from theorems.ternary_coloring_bpqm import OMEGA, state
    effects = []
    for z in range(3):
        anti = np.array([0., OMEGA**z, -OMEGA**(2*z)])/2**.5
        effect = 2*np.outer(anti, anti.conj())/3
        effect[0, 0] += Fraction(1, 3)
        effects.append(effect)
    probabilities = np.array([[np.vdot(state(PHYSICAL, u), E @ state(PHYSICAL, u)).real
                               for E in effects] for u in range(3)])
    expected = (np.ones((3, 3))-np.eye(3))/2
    residual = max(float(np.max(np.abs(sum(effects)-np.eye(3)))),
                   float(np.max(np.abs(probabilities-expected))))
    if residual > 1e-12 or min(np.linalg.eigvalsh(E).min() for E in effects) < -1e-12:
        raise ArithmeticError("physical exclusion readout failed")
    return {"readout": "fixed_single_copy_anti_trine_POVM",
            "probability_matrix_exact": [["0" if u == z else "1/2" for z in range(3)] for u in range(3)],
            "physical_effects_and_probabilities_residual": residual,
            "record_channel_capacity_bits_expression": "log2(3)-1",
            "capacity_bits_NUMERICAL_DISPLAY_ONLY": log2(3)-1,
            "three_six_nominal_code_rate_bits_expression": "log2(3)/2",
            "three_six_Fano_asymptotic_word_error_floor_expression": "1-2*(log2(3)-1)/log2(3)",
            "other_readouts_or_classical_CSP_algorithms_excluded": False,
            "classical_uniform_sampling_lower_bound_claimed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--grid", type=int, default=24)
    parser.add_argument("--iterations", type=int, default=24)
    parser.add_argument("--variable-degree", type=int, default=3)
    parser.add_argument("--check-degree", type=int, default=6)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    sources = [Path(__file__), ROOT/"theorems/ternary_coloring_bpqm.py", ROOT/"theorems/bpqm_gibbs_frontier.py"]
    before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    result = frontier(dv=args.variable_degree, dc=args.check_degree, grid=args.grid,
                      iterations=args.iterations, progress=True)
    controls = [degradation_control(mu, args.grid) for mu in
                (PHYSICAL, (Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)),
                 (0, Fraction(1, 7), Fraction(6, 7)), (Fraction(1, 3),)*3)]
    classical = [native_constraint_control(n, seed) for n, seed in ((16, 711), (32, 712))]
    exclusion = exclusion_readout_control()
    if before != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}:
        raise RuntimeError("producer or dependency changed during run")
    report = {"schema_version": 1, "source_sha256": before, "result": result,
              "actual_physical_degradation_controls": controls,
              "classical_original_dual_CSP_controls": classical,
              "specified_product_measurement_baseline": exclusion,
              "local_derivation_independently_reviewed": False}
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": result["status"], "certificate": result["certificate"]}, indent=2))


if __name__ == "__main__":
    main()
