"""Primitive-character application of the guarded sampler, not a speedup.

The analytic implication and primitive projection are written proofs pending
independent review. Native records are classical witnesses, not quantum runs.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import arb, ctx, fmpq

from theorems import integer_character_interpolation as integer
from theorems import integer_character_near_vector as near
from theorems import integer_character_uniform as uniform

REPORT = ROOT / "research/reductions/integer_character_resonance.json"
SEED = 2026102027
TRIALS = 32
THRESHOLD = Q(1, 4)


def primitive_license(primes, cap, exponent):
    """Require the first-moment height guard also modulo 3^(k-1)."""
    record = integer.height_license(primes, cap, exponent, moment=1)
    if 3**(exponent-1) <= 2*max(primes)**(2*cap+1):
        raise ValueError("primitive projection needs the smaller-modulus height guard")
    return {
        **record,
        "strict_guard": "3^(k-1) > 2*B^(2*cap+1)",
        "primitive_probability": "2/3",
        "first_moment_preserved_after_primitive_projection": True,
        "scope": "written overlap argument; not a kernel-checked theorem",
    }


def primitive_success_budget():
    """Charge primitive rejection, finite precision and source heralding."""
    uniform.uniform_constants()
    epsilon, eta = Q(1, 10000), Q(1, 100000)
    robust = THRESHOLD+2*eta
    conditional = (uniform.MEAN_LOWER-robust)/(1-robust)
    joint = Q(2, 3)*conditional-epsilon
    herald = (Q(1, 2)-epsilon/8)**2
    if not (herald > Q(1, 8) and joint/8 > Q(1, 256)):
        raise ArithmeticError("primitive search error budget failed")
    return {
        "minimum_length": uniform.MIN_LENGTH,
        "cap_rule": "floor(7*m/200)",
        "active_probability": "1/20",
        "normalized_weighted_mean_lower": str(uniform.MEAN_LOWER),
        "target_normalized_score": str(THRESHOLD),
        "robust_threshold": str(robust),
        "verifier_absolute_error": str(eta),
        "output_tv_error": str(epsilon),
        "ideal_primitive_probability": "2/3",
        "primitive_and_accepted_given_herald_lower": str(joint),
        "source_herald_probability_lower": str(herald),
        "accepted_per_charged_trial_lower": "1/256",
        "trials_per_failure_bit": 256,
        "scope": "same paid source/decoder/QFT argument, with primitive rejection charged",
    }


def _q(value):
    return arb(fmpq(value.numerator, value.denominator))


def _enclosure(value):
    if not value.is_finite():
        raise ArithmeticError("nonfinite interval")
    return Q(str(value.lower().fmpq())), Q(str(value.upper().fmpq()))


@dataclass(frozen=True)
class ResonanceProblem:
    primes: tuple[int, ...]
    labels: tuple[int, ...]
    exponent: int
    cap: int

    def __post_init__(self):
        if type(self.primes) is not tuple or type(self.labels) is not tuple:
            raise ValueError("immutable public tuples required")
        integer.validate_public_labels(self.primes, self.labels, self.exponent)
        if self.primes != integer.prime_support(len(self.primes)):
            raise ValueError("the L-function bridge requires the complete prime prefix except 3")
        primitive_license(self.primes, self.cap, self.exponent)

    @property
    def order(self):
        return 2*3**(self.exponent-1)

    def evaluate(self, assignment, *, precision=96):
        if type(assignment) is not int or not 0 <= assignment < self.order:
            raise ValueError("canonical integer character label required")
        if type(precision) is not int or precision < 64:
            raise ValueError("integer interval precision at least 64 required")
        with ctx.workprec(precision):
            total, weight, log_product = arb(0), arb(0), arb(0)
            for p, label in zip(self.primes, self.labels):
                residue = label*assignment % self.order
                cosine = arb.cos_pi_fmpq(fmpq(2*residue, self.order))
                total += cosine/p
                weight += arb(1)/p
                # log |(1-chi(p)/p)^(-1)|, without complex branch choices.
                log_product -= (1-2*cosine/p+arb(1)/(p*p)).log()/2
            low, high = _enclosure(total/weight)
            if high-low > Q(1, 50000):
                raise ArithmeticError("normalized score interval exceeds verifier budget")
            product_low, product_high = _enclosure(log_product)
            s_low, s_high = _enclosure(total)
            w_low, w_high = _enclosure(weight)
        primitive = assignment % 3 != 0
        return {
            "assignment_decimal": str(assignment),
            "primitive": primitive,
            "score_lower": str(low), "score_upper": str(high),
            "weighted_sum_lower": str(s_low), "weighted_sum_upper": str(s_high),
            "weight_sum_lower": str(w_low), "weight_sum_upper": str(w_high),
            "log_truncated_euler_modulus_lower": str(product_low),
            "log_truncated_euler_modulus_upper": str(product_high),
            "threshold": str(THRESHOLD),
            "accepted": primitive and low >= THRESHOLD,
            "threshold_overlap": primitive and low < THRESHOLD <= high,
            "precision_bits": precision,
            "full_L_value_computed": False,
            "exact_modular_residues_used": True,
        }


def analytic_bridge(prime_bound):
    """Checks constants, not the all-B proof supplied in the companion note."""
    if type(prime_bound) is not int or prime_bound < 2:
        raise ValueError("integer prime bound at least two required")
    h = prime_bound.bit_length()
    with ctx.workprec(128):
        log2 = arb(2).log()
        if not (log2/2 > _q(Q(1, 3))
                and 4*log2**2+4*log2 < 5
                and 1+8*log2 < 8):
            raise ArithmeticError("elementary analytic constants failed")
        lower = arb(prime_bound+1).log().log()/4-43
        lo, hi = _enclosure(lower)
    return {
        "prime_bound": prime_bound,
        "sigma": str(1+Q(1, h)),
        "first_power_weight_change_upper": "5",
        "prime_tail_upper": "36",
        "higher_prime_powers_upper": "1",
        "log_abs_L_lower_formula": "log(log(B+1))/4 - 43",
        "lower_formula_enclosure": [str(lo), str(hi)],
        "implies_abs_L_above_one": lo > 0,
        "conditional_on": "complete prime prefix, primitive witness, S >= W/4",
        "at_s_equal_one_claimed": False,
        "critical_strip_claimed": False,
        "full_L_value_computed": False,
        "scope": "elementary written uniform proof pending independent review",
    }


def classical_control(problem, *, trials=TRIALS, seed=SEED):
    if type(trials) is not int or trials < 1 or type(seed) is not int:
        raise ValueError("positive integer trial budget and integer seed required")
    rng = random.Random(seed)
    records = []
    for _ in range(trials):
        x = 3*rng.randrange(problem.order//3)+1+rng.randrange(2)
        records.append(problem.evaluate(x))
    best = max(records, key=lambda row: Q(row["score_lower"]))
    return {
        "method": "fixed-seed uniform primitive labels; complete weighted objective",
        "seed": seed, "trials": trials,
        "accepted_count": sum(row["accepted"] for row in records),
        "best": best,
        "records": records,
        "quantum_calls": 0,
        "group_table_used": False,
        "cosine_and_log_factor_evaluations": trials*len(problem.primes),
        "scope": "finite witnesses only; not an asymptotic probability or hardness test",
    }


def report():
    data = near.REPORT.read_bytes()
    source = json.loads(data)
    if source["producer_sha256"] != hashlib.sha256(Path(near.__file__).read_bytes()).hexdigest():
        raise ValueError("reproduce the near-vector input artifact before reuse")
    native = source["native"]
    problem = ResonanceProblem(
        tuple(native["public_primes"]),
        tuple(map(int, native["public_labels_decimal"])),
        native["modulus_exponent"], native["cap_each_sign"])
    if problem.order != int(native["cyclic_order_decimal"]):
        raise ValueError("input order does not match the modulus exponent")
    return {
        "schema": "integer_character_resonance_v1",
        "status": "constructive_application_argument_pending_review_not_a_speedup",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_artifact_sha256": hashlib.sha256(data).hexdigest(),
        "dependency_sha256": {
            Path(module.__file__).name: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
            for module in (integer, uniform)
        },
        "problem": {
            "length": len(problem.primes), "prime_bound": problem.primes[-1],
            "modulus_exponent": problem.exponent,
            "cyclic_order_bits": problem.order.bit_length(),
            "objective": "S/W, S=sum Re(chi(p))/p, W=sum 1/p, all p<=B except 3",
            "centers": "all zero; a different problem from the saved random-target CVP",
            "required_output": "primitive character label x with S/W >= 1/4",
            "public_labels_verified": True,
            "public_preprocessing": native["preprocessing"],
        },
        "primitive_license": primitive_license(problem.primes, problem.cap, problem.exponent),
        "uniform_success_budget": primitive_success_budget(),
        "native_source_mean": integer.source_mean(len(problem.primes), problem.cap, Q(1, 20)),
        "analytic_bridge": analytic_bridge(problem.primes[-1]),
        "principal_character_rejection_control": problem.evaluate(0),
        "classical_control": classical_control(problem),
        "quantum_optimizer_executed": False,
        "coherent_circuit_compiled": False,
        "kernel_checked_proof": False,
        "classical_hardness_or_speedup_proved": False,
        "novelty_established": False,
        "blocked": [
            "independent review of primitive projection and inherited quantum source",
            "efficient classical primitive-character construction or resonator sampling",
            "uniform algorithmic comparison, not random-search failure",
            "novelty review against resonance and quantum Fourier-sampling literature",
            "useful external computational consequence beyond an extremal-character task",
        ],
        "references": [
            "https://arxiv.org/abs/1803.00760",
            "https://dlmf.nist.gov/25.15",
            "https://dlmf.nist.gov/27.8",
            "https://dlmf.nist.gov/27.2",
            "https://www.dei.unipd.it/~languasco/Littlewood_ineq.html",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    control = result["classical_control"]
    print(json.dumps({
        "output": str(args.output), "classical_trials": control["trials"],
        "classical_accepted": control["accepted_count"],
        "classical_best_score_lower": float(Q(control["best"]["score_lower"])),
        "native_full_L_lower_bound_above_one":
            result["analytic_bridge"]["implies_abs_L_above_one"],
        "speedup_claimed": False,
    }))


if __name__ == "__main__":
    main()
