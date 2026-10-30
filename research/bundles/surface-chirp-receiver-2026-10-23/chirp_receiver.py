"""Explicit prime-field surface receiver with a fresh-state backend.

The decoder receives only public weights and measurement outcomes. A real
backend must prepare the specified states using the original coherent
oracle; the neighboring Qiskit backend is a bounded proof control only.
"""

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sys

from sympy import Matrix, eye, isprime, sqrt_mod

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"siegel-classical-2026-10-23"))
from classical_siegel import covering_frames, mod, symplectic_form


@dataclass
class ChirpPacket:
    weight: int
    state: object


def pair_root(first, second, p):
    """Public gamma: first + second*gamma^2=0, with gamma != 1."""
    first, second = first % p, second % p
    if not first or not second:
        return None
    target = -first*pow(second, -1, p) % p
    if pow(target, (p-1)//2, p) != 1:
        return None
    roots = sqrt_mod(target, p, all_roots=True)
    return next(int(root) for root in roots if root != 1)


def pair_equation(first, second, gamma, s, frequency, p):
    """Return slope,value for b+slope*c=value from a measured pair."""
    first, second, gamma, s, frequency = (int(x) % p for x in (first, second, gamma, s, frequency))
    if not first or not second or gamma in (0, 1) or (first+second*gamma*gamma) % p:
        raise ValueError("compatible nonzero pair and nondegenerate root required")
    e = (first+second*gamma) % p
    return (s*pow(1-gamma, -1, p) % p, frequency*pow(2*e, -1, p) % p)


def learn_row(prepare, measure_pair, p, block_pairs):
    equations, copies, trials = [], 0, 0
    for stage in range(2):
        for _ in range(block_pairs):
            first, second = prepare(), prepare()
            copies += 2
            trials += 1
            if first is None or second is None:
                continue
            gamma = pair_root(first.weight, second.weight, p)
            if gamma is None:
                continue
            s, frequency = measure_pair(first, second, gamma, p)
            slope, value = pair_equation(first.weight, second.weight, gamma, s, frequency, p)
            if stage and slope == equations[0]["slope"]:
                continue
            equations.append({"first_weight": int(first.weight), "second_weight": int(second.weight),
                              "gamma": gamma, "s": int(s), "frequency": int(frequency),
                              "slope": slope, "value": value})
            break
        else:
            return {"status": "ABORT", "source_copies": copies, "pair_trials": trials,
                    "equations": equations, "reason": "fresh-pair budget exhausted"}
    first, second = equations
    c = (second["value"]-first["value"])*pow(second["slope"]-first["slope"], -1, p) % p
    b = (first["value"]-first["slope"]*c) % p
    return {"status": "ROW_RECOVERED_UNDER_STATE_PROMISE", "b": b, "diagonal": c,
            "source_copies": copies, "pair_trials": trials, "equations": equations}


def recover(prepare, measure_pair, query, p, *, block_pairs=64):
    """prepare(C,j) returns a new packet for E_(1-j,j), or None for r=0.

    Bad charts may return arbitrary states. Only original-oracle
    transvection tests can accept a reconstructed plane.
    """
    if not isprime(p) or p == 2 or type(block_pairs) is not int or block_pairs < 1:
        raise ValueError("odd prime and positive integer block budget required")
    copies, verifier_calls, records = 0, 1, []
    identity_label, j = query(eye(4)), symplectic_form(2)
    for chart_index, chart in enumerate(covering_frames(p)[::2]):
        rows = []
        for direction in (1, 0):
            row = learn_row(lambda: prepare(chart, direction), measure_pair, p, block_pairs)
            copies += row["source_copies"]
            rows.append(row)
            if row["status"] == "ABORT":
                break
        record = {"chart": chart_index, "rows": rows, "status": "ABORT"}
        records.append(record)
        if len(rows) != 2 or any(row["status"] == "ABORT" for row in rows):
            continue
        if rows[0]["b"] != rows[1]["b"]:
            record["status"] = "INCONSISTENT_ROWS"
            continue
        a, b, c = rows[1]["diagonal"], rows[0]["b"], rows[0]["diagonal"]
        candidate = mod(chart*Matrix([[a, b], [1, 0], [b, c], [0, 1]]), p)
        passed = True
        for column in range(2):
            v = candidate[:, column]
            verifier_calls += 1
            if query(mod(eye(4)+v*v.T*j, p)) != identity_label:
                passed = False
                break
        if not passed:
            record["status"] = "CERTIFICATE_REJECTED"
            continue
        record["status"] = "CERTIFIED"
        return {"status": "RECOVERED_UNDER_ORACLE_AND_STATE_PROMISES", "basis": candidate,
                "source_copies": copies, "verification_queries": verifier_calls,
                "source_copy_bound": 32*block_pairs, "verification_query_bound": 9,
                "ideal_failure_bound": str(min(Fraction(1), 4*Fraction(23, 27)**block_pairs)),
                "charts": records}
    return {"status": "ABORT", "basis": None, "source_copies": copies,
            "verification_queries": verifier_calls, "source_copy_bound": 32*block_pairs,
            "verification_query_bound": 9,
            "ideal_failure_bound": str(min(Fraction(1), 4*Fraction(23, 27)**block_pairs)),
            "charts": records}
