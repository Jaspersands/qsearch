"""Certified classical reference for finite-register BPQM arithmetic.

Known BP-style log coordinates; local error derivation REVIEW PENDING. This
does not implement reversible quantum arithmetic or establish an advantage.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import arb, ctx, fmpq
from theorems.bpqm_gibbs_frontier import integer, rational

REPORT = ROOT/"research/phase_workbench/bpqm_log_reliability.json"


class ReliabilityLimit(RuntimeError):
    pass


def _ball(q):
    q = rational(q)
    return arb(fmpq(q.numerator, q.denominator))


def _fraction(point):
    q = point.fmpq()
    return Fraction(int(q.numerator), int(q.denominator))


def _quantize(evaluate, bits, guard=0):
    integer(bits, "fractional reliability bits", 8, 256)
    for extra in (64, 128, 256, 512):
        with ctx.workprec(bits+guard+extra):
            interval = evaluate()
            if not interval.is_finite():
                continue
            middle = _fraction(interval.mid())
            scaled = middle*(1 << bits)+Fraction(1, 2)
            value = Fraction(scaled.numerator//scaled.denominator, 1 << bits)
            error = _fraction(abs(interval-_ball(value)).upper())
            if error <= Fraction(1, 1 << bits):
                return {"value": str(value), "evaluation_error_upper": str(error),
                        "fractional_bits": bits, "arb_precision_bits": bits+guard+extra,
                        "integer_rounding_and_transcendental_error_included": True}
    raise ReliabilityLimit("UNKNOWN: reference arithmetic precision cap")


def initial_log(overlap, *, bits=64):
    c = rational(overlap)
    if not -1 < c < 1:
        raise ValueError("finite signed overlap required")
    return _quantize(lambda: _ball(c).atanh(), bits,
                     max(c.numerator.bit_length(), c.denominator.bit_length()))


def parity_log(left, right, herald, *, bits=64):
    a, b = rational(left), rational(right)
    integer(herald, "coherent herald bit", 0, 1)
    return _quantize(lambda: _ball(a+b if herald == 0 else b-a), bits)


def equality_log(left, right, *, bits=64):
    a, b = rational(left), rational(right)

    def logcosh(q):
        q = abs(q)
        return _ball(q)+(1+_ball(-2*q).exp()).log()-arb(2).log()

    return _quantize(lambda: (logcosh(a+b)-logcosh(a-b))/2, bits,
                     max(a.numerator.bit_length(), b.numerator.bit_length()))


def compression_angle_log(left, right, message_bit, *, bits=64):
    a, b = rational(left), rational(right)
    integer(message_bit, "compressed message bit", 0, 1)
    z = -a-b if message_bit == 0 else a-b
    return _quantize(lambda: -arb.pi()+2*_ball(-z).exp().atan() if z >= 0
                     else -2*_ball(z).exp().atan(), bits)


def precision_budget(max_tree_channels, equality_nodes_across_roots, epsilon, *, source_error=0):
    L, E = max_tree_channels, equality_nodes_across_roots
    integer(L, "maximum distinct original channels in a root tree", 1, 1 << 4096)
    integer(E, "equality multiplexers summed over all decoded roots", 0, 1 << 4096)
    eps, source = rational(epsilon), rational(source_error)
    if not 0 <= source < eps <= 1:
        raise ValueError("0<=source error<epsilon<=1 required")
    coefficient = 2*E*(2*L-1)
    bits = 8
    while Fraction(coefficient, 1 << bits) > eps-source:
        bits += 1
        if bits > 4096:
            raise ReliabilityLimit("UNKNOWN: declared precision-budget cap")
    bound = Fraction(coefficient, 1 << bits)+source
    return {"maximum_distinct_tree_channels": L, "equality_multiplexers_across_roots": E,
            "fractional_bits_sufficient": bits, "per_arithmetic_error_budget": str(Fraction(1, 1 << bits)),
            "logical_rotation_readout_TV_perturbation_upper": str(bound),
            "target_TV_perturbation": str(eps), "separate_source_state_error_upper_assumed": str(source),
            "bound_counts_A_copy_Adjoint_and_all_root_inverse_occurrences": True,
            "orthogonal_herald_branches_are_not_summed_as_sequential_gate_errors": True,
            "requires_all_heralds_and_arithmetic_garbage_retained_then_uncomputed": True,
            "bound_is_to_ideal_algorithm_not_Gibbs_without_ideal_correctness": True,
            "integer_register_overflow_must_be_excluded_separately": True,
            "finite_universal_gate_synthesis_error_included": False,
            "reversible_quantum_arithmetic_implemented": False,
            "local_derivation_status": "REVIEW_PENDING", "accepted_speedup_candidate": False}


def register_width(overlap, max_tree_channels, *, bits=64):
    integer(max_tree_channels, "distinct original tree channels", 1, 1 << 4096)
    leaf = initial_log(overlap, bits=bits)
    eta = Fraction(1, 1 << bits)
    magnitude = max_tree_channels*abs(Fraction(leaf["value"]))+(max_tree_channels-1)*eta
    integer_bits = 1+magnitude.__ceil__().bit_length()
    return {"initialized_log_reference": leaf, "approximate_register_absolute_value_upper": str(magnitude),
            "signed_integer_bits_sufficient": integer_bits, "fractional_bits": bits,
            "message_register_bits_sufficient": integer_bits+bits,
            "bounds_assume_disjoint_tree_inputs_and_rounding_error_at_most_one_unit": True,
            "scratch_herald_and_reversible_arithmetic_qubits_not_counted": True,
            "reversible_circuit_compiled": False}


def run_controls():
    pairs = (("0", "0"), ("1/5", "13/20"), ("-7/8", "3/4"),
             (str(1-Fraction(1, 1 << 256)), str(-1+Fraction(1, 1 << 255))))
    examples = []
    for a, b in pairs:
        left, right = initial_log(a), initial_log(b)
        examples.append({"overlaps": [a, b], "left": left, "right": right,
                         "parity_plus": parity_log(left["value"], right["value"], 0),
                         "parity_minus": parity_log(left["value"], right["value"], 1),
                         "equality": equality_log(left["value"], right["value"]),
                         "angles": [compression_angle_log(left["value"], right["value"], bit) for bit in (0, 1)]})
    return {"schema_version": "1.0", "subsystem": "bpqm_log_reliability", "examples": examples,
            "five_channel_three_root_budget": precision_budget(5, 6, "1/1000"),
            "five_channel_message_width": register_width("13/20", 5, bits=17),
            "illustrative_large_parameter_budget": precision_budget(1111111111111, (1 << 60)*1111111111110, "1/1000"),
            "illustrative_large_message_width": register_width("13/20", 1111111111111, bits=152),
            "large_parameter_graph_or_algorithm_constructed": False,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": hashlib.sha256((ROOT/"theorems/bpqm_gibbs_frontier.py").read_bytes()).hexdigest(),
            "reversible_quantum_arithmetic_implemented": False, "classical_hardness_proved": False,
            "accepted_speedup_candidate": False,
            "known_efficient_BPQM_reference": "https://arxiv.org/abs/2109.08170"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report["five_channel_three_root_budget"], indent=2))


if __name__ == "__main__":
    main()
