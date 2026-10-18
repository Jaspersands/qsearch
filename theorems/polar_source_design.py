"""Finite certified polar source design for native random-sign Gibbs sampling.

Known polarization/PSC degradation, local application review pending. Nonuniform
overlap grids avoid a false N/grid accuracy floor. No quantum speedup claim.
"""
from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from fractions import Fraction
from functools import cached_property, lru_cache
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer, rational
from theorems.polar_conditional_sampler import sample_gibbs

REPORT = ROOT/"research/classical_baselines/polar_source_design.json"
LARGE_REPORT = REPORT.with_name("polar_source_design_n32768_g256_p3.json")


@dataclass(frozen=True)
class Grid:
    intervals: int = 64
    power: int = 4
    mass_bits: int = 96

    def __post_init__(self):
        integer(self.intervals, "overlap grid intervals", 2, 256)
        integer(self.power, "nonuniform grid power", 1, 12)
        integer(self.mass_bits, "dyadic herald-mass precision", 16, 256)
        if self.intervals & (self.intervals-1):
            raise ValueError("power-of-two grid required")

    @property
    def denominator(self):
        return self.intervals**self.power

    @cached_property
    def nodes(self):
        return tuple(j**self.power for j in range(self.intervals+1))


def _rounded_index(grid, numerator, denominator, direction):
    value = Fraction(numerator, denominator)
    return (bisect_left(grid.nodes, value) if direction == "upper"
            else bisect_right(grid.nodes, value)-1)


@lru_cache(maxsize=32)
def _transitions(grid, direction):
    if direction not in ("upper", "lower"):
        raise ValueError("explicit physical degradation/upgrade direction required")
    nodes, D = grid.nodes, grid.denominator
    output = {}
    for i, a in enumerate(nodes):
        for j in range(i, len(nodes)):
            b = nodes[j]
            product = _rounded_index(grid, a*b, D, direction)
            parity = []
            for sign in (1, -1):
                d = D*D+sign*a*b
                if d:
                    index = _rounded_index(grid, D*D*(a+b if sign == 1 else abs(a-b)), d, direction)
                    parity.append((index, d))
            output[(i, j)] = (product, tuple(parity))
    return output


def point_law(c, grid, direction="upper"):
    c = rational(c)
    if not 0 <= c <= 1 or direction not in ("upper", "lower"):
        raise ValueError("overlap and explicit information direction required")
    index = _rounded_index(grid, c*grid.denominator, 1, direction)
    out = [0]*(grid.intervals+1)
    out[index] = 1 << grid.mass_bits
    return tuple(out)


def combine_self(weights, grid, kind, *, direction="upper", work=None):
    """Combine independent identical flagged PSCs; round each herald physically."""
    L, D = 1 << grid.mass_bits, grid.denominator
    if (type(weights) is not tuple or len(weights) != grid.intervals+1
            or any(type(w) is not int or w < 0 for w in weights) or sum(weights) != L):
        raise ValueError("exact normalized dyadic herald law required")
    if kind not in ("source_even", "source_odd"):
        raise ValueError("explicit polar source child required")
    transitions = _transitions(grid, direction)
    raw = [0]*len(weights)
    active = [j for j, w in enumerate(weights) if w]
    visits = 0
    for offset, i in enumerate(active):
        for j in active[offset:]:
            weight = weights[i]*weights[j]*(1 if i == j else 2)
            product, parity = transitions[(i, j)]
            visits += 1
            if kind == "source_even":
                raw[product] += weight
            else:
                for index, d in parity:
                    raw[index] += weight*d
    denominator = L*L*(2*D*D if kind == "source_odd" else 1)
    if sum(raw) != denominator:
        raise ArithmeticError("nonuniform polar combination lost total herald mass")
    rounded = [x*L//denominator for x in raw]
    discarded = L-sum(rounded)
    if not 0 <= discarded <= grid.intervals:
        raise ArithmeticError("dyadic mass-rounding budget exceeded")
    rounded[-1 if direction == "upper" else 0] += discarded
    if work is not None:
        work["active_support_pair_visits"] += visits
        work["channel_combinations"] += 1
        work["dyadic_rounding_mass_units"] += discarded
    return tuple(rounded)


def mean_overlap(weights, grid):
    return Fraction(sum(a*w for a, w in zip(grid.nodes, weights)), grid.denominator << grid.mass_bits)


def construct(N, c, count, *, grid=None, target_average_TV=Fraction(1, 10)):
    integer(N, "polar block length", 2, 32768)
    if N & (N-1):
        raise ValueError("power-of-two length required")
    integer(count, "source constraints / quantum code dimension", 0, N)
    grid = Grid() if grid is None else grid
    c = rational(c)
    target = rational(target_average_TV)
    if not 0 <= c < 1 or not 0 < target < 1:
        raise ValueError("finite overlap and nontrivial TV target required")
    laws = (point_law(c, grid),)
    work = {"active_support_pair_visits": 0, "channel_combinations": 0, "dyadic_rounding_mass_units": 0}
    while len(laws) < N:
        laws = tuple(child for parent in laws for child in (
            combine_self(parent, grid, "source_even", work=work),
            combine_self(parent, grid, "source_odd", work=work)))
    bounds = tuple(mean_overlap(law, grid) for law in laws)
    frozen = tuple(sorted(sorted(range(N), key=lambda i: (bounds[i], i))[:count]))
    total = sum((bounds[i] for i in frozen), Fraction(0))
    maximum = 0
    spent = Fraction(0)
    for i in sorted(range(N), key=lambda i: (bounds[i], i)):
        if spent+bounds[i] > target:
            break
        spent += bounds[i]
        maximum += 1
    return {"positions": N, "channel_overlap": str(c), "source_probability": str((1-c)/2),
            "constraint_count": count, "quantum_code_rate": str(Fraction(count, N)),
            "kernel_Gibbs_spin_dimension": N-count, "frozen_coordinates": list(frozen),
            "all_source_mean_absolute_bias_upper": list(map(str, bounds)),
            "frozen_prefix_bias_sum_upper": str(total/2),
            "uniform_sign_average_Gibbs_TV_upper": str(min(1, total)),
            "target_average_TV": str(target), "target_certified": total <= target,
            "status": "CERTIFIED_AVERAGE_GIBBS_TARGET_REVIEW_PENDING" if total <= target else "UNKNOWN_AT_THIS_GRID_AND_LENGTH_NOT_HARDNESS",
            "maximum_constraints_at_target": maximum,
            "maximum_frozen_coordinates_at_target": sorted(sorted(range(N), key=lambda i: (bounds[i], i))[:maximum]),
            "maximum_at_target_average_TV_upper": str(spent),
            "maximum_at_target_code_rate": str(Fraction(maximum, N)),
            "maximum_is_for_this_bound_vector_not_true_optimal_code": True,
            "beyond_product_USD_rate_ceiling": Fraction(count, N) > 1-c,
            "prefix_exact_family": frozen == tuple(range(len(frozen))),
            "grid": {"intervals": grid.intervals, "power": grid.power, "mass_bits": grid.mass_bits,
                     "overlap_denominator": grid.denominator},
            "construction_work": work, "transition_table_pair_entries": (grid.intervals+1)*(grid.intervals+2)//2,
            "maximum_retained_channel_mass_entries": N*(grid.intervals+1),
            "peak_channel_mass_entries_including_previous_level": (3*N//2)*(grid.intervals+1),
            "integer_arithmetic_intermediate_bits_upper": 2*grid.mass_bits+2*grid.denominator.bit_length()+2,
            "uniform_overlap_grid_error_floor_used": False, "full_source_table_materialized": False,
            "guarantee_is_average_uniform_sign_not_worst_sign": True,
            "quantum_decoder_executed": False, "local_degradation_and_hybrid_derivation_review_pending": True}


def run_controls():
    rows = [construct(N, Fraction(13, 20), N//2) for N in (16, 64, 256, 1024, 4096)]
    for row in rows[:2]:
        row["native_Gibbs_samples"] = [sample_gibbs(row["positions"], row["channel_overlap"],
                                                   tuple(row["frozen_coordinates"]),
                                                   int("a5"*((row["positions"]+7)//8), 16) & ((1 << row["positions"])-1), seed)
                                       for seed in (29, 71)]
        maximum_frozen = tuple(row["maximum_frozen_coordinates_at_target"])
        row["certified_set_Gibbs_samples"] = [sample_gibbs(row["positions"], row["channel_overlap"],
                                                        maximum_frozen, (1 << row["positions"])-1, seed)
                                             for seed in (29, 71)]
    base = rows[-1]
    values = tuple(map(Fraction, base["all_source_mean_absolute_bias_upper"]))
    k = 3*base["positions"]//8
    frozen = tuple(sorted(sorted(range(base["positions"]), key=lambda i: (values[i], i))[:k]))
    followup = {"positions": base["positions"], "channel_overlap": base["channel_overlap"],
                "source_probability": base["source_probability"], "constraint_count": k,
                "quantum_code_rate": "3/8", "Gibbs_spin_dimension": base["positions"]-k,
                "frozen_coordinates": list(frozen),
                "uniform_sign_average_Gibbs_TV_upper": str(sum(values[i] for i in frozen)),
                "source_bound_row_index": len(rows)-1,
                "rate_chosen_after_exploratory_bound_budget_not_predeclared": True,
                "prefix_exact_family": frozen == tuple(range(k)),
                "beyond_product_USD_rate_ceiling": Fraction(3, 8) > 1-Fraction(base["channel_overlap"]),
                "target_is_native_signed_kernel_Gibbs_not_word_decoding": True,
                "worst_case_sign_guarantee": False}
    return {"schema_version": "1.0", "subsystem": "polar_source_design", "instances": rows,
            "explicit_three_eighths_rate_followup": followup,
            **provenance()}


def provenance():
    helpers = ("bpqm_gibbs_frontier.py", "polar_conditional_sampler.py")
    return {
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest() for name in helpers},
            "accepted_speedup_candidate": False, "all_codes_dequantized": False,
            "worst_case_sign_sampler_certified": False,
            "literature": ["https://arxiv.org/html/2609.40345v1", "https://arxiv.org/pdf/2109.08170",
                           "https://arxiv.org/abs/1701.05583", "https://arxiv.org/html/2506.09239v2"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--length", type=int)
    parser.add_argument("--grid", type=int, default=64)
    parser.add_argument("--power", type=int, default=4)
    args = parser.parse_args()
    if args.length is not None:
        row = construct(args.length, Fraction(13, 20), args.length//2, grid=Grid(args.grid, args.power))
        path = REPORT.with_name(f"polar_source_design_n{args.length}_g{args.grid}_p{args.power}.json")
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"schema_version": "1.0", "subsystem": "polar_source_design",
                                        "instances": [row], **provenance()}, indent=2)+"\n", encoding="utf-8")
        excluded = {"all_source_mean_absolute_bias_upper", "frozen_coordinates", "maximum_frozen_coordinates_at_target"}
        print(json.dumps({k: v for k, v in row.items() if k not in excluded}, indent=2))
        return
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps([{"N": r["positions"], "rate": r["quantum_code_rate"],
                       "average_TV_upper": float(Fraction(r["uniform_sign_average_Gibbs_TV_upper"])),
                       "target_certified": r["target_certified"],
                       "maximum_constraints_at_target": r["maximum_constraints_at_target"],
                       "active_pairs": r["construction_work"]["active_support_pair_visits"]}
                      for r in report["instances"]], indent=2))


if __name__ == "__main__":
    main()
