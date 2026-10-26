"""Classical reversal controls for a proposed hybrid reversible Hermite decoder.

This records field operations, not quantum gates. Full circuit compilation,
uniform proof review and novelty review remain pending.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from math import comb
from pathlib import Path

from theorems.hermite_compact_decoder import (
    DescendingSystem, divide_linear, leading, subtract, times_linear,
)
from theorems.hermite_pinned_decoder import canonical, jet, parameters
from theorems.hermite_parameter_theorem import ceil_log2

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "research/reductions/hermite_module_certificate.json"
REPORT = ROOT / "research/reductions/hermite_reversible_workspace.json"


def fixed_width_linear(values, root, p, *, inverse=False):
    """Bijection: multiply by X-root modulo X^L, with root nonzero."""
    canonical(values, len(values), p)
    if type(root) is not int or not 0 < root < p:
        raise ValueError("nonzero field point required")
    out = list(values)
    if not out:
        return out
    if inverse:
        inv = pow(root, -1, p)
        out[0] = -out[0]*inv % p
        for j in range(1, len(out)):
            out[j] = (out[j-1]-out[j])*inv % p
    else:
        for j in range(len(out)-1, 0, -1):
            out[j] = (out[j-1]-root*out[j]) % p
        out[0] = -root*out[0] % p
    return out


def collision_step(basis, weights, p):
    positions = {}
    for i, row in enumerate(basis):
        degree, position = leading(row, weights)
        if position in positions:
            j = positions[position]
            receiver, donor = (i, j) if degree >= leading(basis[j], weights)[0] else (j, i)
            a, b = basis[receiver][position], basis[donor][position]
            return {"receiver": receiver, "donor": donor,
                    "shift": len(a)-len(b),
                    "factor": a[-1]*pow(b[-1], -1, p) % p}
        positions[position] = i
    return None


def apply_cancellation(basis, record, p, *, inverse=False):
    receiver, donor = record["receiver"], record["donor"]
    factor = -record["factor"] if inverse else record["factor"]
    basis[receiver] = [subtract(a, b, factor, record["shift"], p)
                       for a, b in zip(basis[receiver], basis[donor])]


def reduce_traced(basis, weights, p):
    history = []
    while (record := collision_step(basis, weights, p)) is not None:
        old = leading(basis[record["receiver"]], weights)
        apply_cancellation(basis, record, p)
        if leading(basis[record["receiver"]], weights) >= old:
            raise ArithmeticError("cancellation did not decrease potential")
        history.append(record)
    return history


def undo_reduction(basis, weights, p, history):
    for record in reversed(history):
        apply_cancellation(basis, record, p, inverse=True)
        if collision_step(basis, weights, p) != record:
            raise ArithmeticError("cancellation history does not cleanly uncompute")


def local_received(received, point, ell, order, p):
    height = ell-order
    y = received[(point-1)*ell:point*ell]
    return [[1]+[0]*(height-1)] + [
        [comb(j+t, j)*y[j+t] % p for t in range(height)]
        for j in range(order+1)]


def expanded_basis(basis, point, height, p):
    return [[jet(poly, point, height, p) for poly in row] for row in basis]


def interpolation_choice(basis, expanded, local, t, weights, p):
    rank = len(basis)
    discrepancies = [sum(expanded[i][j][t-u]*local[j][u]
                          for j in range(rank) for u in range(t+1)) % p
                     for i in range(rank)]
    active = [i for i, value in enumerate(discrepancies) if value]
    if not active:
        return {"pivot": None, "factors": [], "cache_tails": []}
    pivot = min(active, key=lambda i: (leading(basis[i], weights), i))
    inv = pow(discrepancies[pivot], -1, p)
    return {"pivot": pivot,
            "factors": [x*inv % p if i != pivot else 0
                        for i, x in enumerate(discrepancies)],
            "cache_tails": [values[-1] for values in expanded[pivot]]}


def interpolate_traced(p, ell, order, radius, received):
    spec = parameters(p, ell, order, radius)
    canonical(received, spec["n"]*ell, p)
    rank, height = order+2, ell-order
    weights = [-(spec["k"]-1)]+[-j for j in range(order+1)]
    basis = [[[1] if i == j else [] for j in range(rank)] for i in range(rank)]
    history = []
    for point in range(1, p):
        local = local_received(received, point, ell, order, p)
        expanded = expanded_basis(basis, point, height, p)
        records = []
        for t in range(height):
            record = interpolation_choice(basis, expanded, local, t, weights, p)
            records.append(record)
            pivot = record["pivot"]
            if pivot is None:
                continue
            for i, factor in enumerate(record["factors"]):
                if not factor:
                    continue
                basis[i] = [subtract(a, b, factor, 0, p)
                            for a, b in zip(basis[i], basis[pivot])]
                expanded[i] = [[(x-factor*y) % p for x, y in zip(a, b)]
                               for a, b in zip(expanded[i], expanded[pivot])]
            basis[pivot] = [times_linear(poly, point, p) for poly in basis[pivot]]
            expanded[pivot] = [[0]+values[:-1] for values in expanded[pivot]]
        if expanded != expanded_basis(basis, point, height, p):
            raise ArithmeticError("local cache cannot be uncomputed from current basis")
        history.append(records)
    reductions = reduce_traced(basis, weights, p)
    bound = rank*rank*(spec["constraints"]+spec["k"])
    if len(reductions) > bound:
        raise ArithmeticError("row-cancellation potential bound failed")
    return {"parameters": spec, "basis": basis, "weights": weights,
            "interpolation_history": history, "reduction_history": reductions}


def uncompute_interpolation(trace, received):
    spec, basis = trace["parameters"], deepcopy(trace["basis"])
    p, ell, order = spec["p"], spec["ell"], spec["order"]
    height, rank, weights = ell-order, order+2, trace["weights"]
    undo_reduction(basis, weights, p, trace["reduction_history"])
    cleared = 0
    for point in range(p-1, 0, -1):
        local = local_received(received, point, ell, order, p)
        expanded = expanded_basis(basis, point, height, p)
        records = trace["interpolation_history"][point-1]
        for t in range(height-1, -1, -1):
            record, pivot = records[t], records[t]["pivot"]
            if pivot is not None:
                if any(values[0] for values in expanded[pivot]):
                    raise ArithmeticError("shifted cache has a nonzero constant term")
                basis[pivot] = [divide_linear(poly, point, p) if poly else []
                                for poly in basis[pivot]]
                expanded[pivot] = [values[1:]+[tail]
                                   for values, tail in zip(expanded[pivot], record["cache_tails"])]
                for i, factor in enumerate(record["factors"]):
                    if not factor:
                        continue
                    basis[i] = [subtract(a, b, -factor, 0, p)
                                for a, b in zip(basis[i], basis[pivot])]
                    expanded[i] = [[(x+factor*y) % p for x, y in zip(a, b)]
                                   for a, b in zip(expanded[i], expanded[pivot])]
            expected = interpolation_choice(basis, expanded, local, t, weights, p)
            if expected != record:
                raise ArithmeticError("interpolation history does not cleanly uncompute")
            cleared += 1
        if expanded != expanded_basis(basis, point, height, p):
            raise ArithmeticError("reverse cache does not equal recomputed jets")
    identity = [[[1] if i == j else [] for j in range(rank)] for i in range(rank)]
    return {"basis_restored_to_identity": basis == identity,
            "history_records_recomputed_and_clearable": cleared+len(trace["reduction_history"]),
            "cache_boundaries_verified": 2*(p-1),
            "native_quantum_gate_execution": False}


def vector_roundtrip(p, k, pieces, free_index=None, *, homogeneous=False):
    """Evaluate and reverse triangular assignment, keeping operator/input intact."""
    system = DescendingSystem(p, k, pieces)
    f = [0]*k

    def assigned(t):
        if not system.pivots[t]:
            return int(t == free_index)
        h = t+system.shift
        value = pieces[0][h] if not homogeneous and 0 <= h < len(pieces[0]) else 0
        value += sum(system.coefficient(h, u)*f[u] for u in range(t+1, k))
        return -value*pow(system.pivots[t], -1, p) % p

    for t in range(k-1, -1, -1):
        f[t] = (f[t]+assigned(t)) % p
    output = list(f)
    for t in range(k):
        f[t] = (f[t]-assigned(t)) % p
    return {"output": output, "scratch_all_zero": not any(f),
            "free_coordinates": len(system.free)}


def workspace_ledger(p, ell, order, radius):
    spec = parameters(p, ell, order, radius)
    u, m, k, z = order+2, spec["constraints"], spec["k"], spec["kernel_dimension_bound"]
    log_scale = ceil_log2(p*ell)
    return {"parameters": spec,
            "basis_field_slots_upper": u*u*(m+k+1),
            "interpolation_history_field_slots_upper": 2*u*m,
            "interpolation_history_index_slots_upper": m,
            "row_reduction_records_upper": u*u*(m+k),
            "row_reduction_record_contents": "one field factor, two row indices, one degree shift; public padded slots",
            "checkpoint_state_field_slots_upper_up_to_constants": z*(z+1),
            "checkpoint_log_scale_not_exact_depth": log_scale,
            "clean_row_oracle_scratch": "O(q*ell) field elements, NOT included in each checkpoint",
            "hybrid_reversible_bits": "O(((s+2)^2*q*ell + s^2*ell^2*log(q*ell))*log(q))",
            "sufficient_log_absorption_condition": ell*log_scale <= p,
            "log_absorption_condition": "ell*ceil(log2(q*ell)) <= q",
            "tight_region_bits": "O((s+2)^2*q*ell*log(q)); fixed s gives O_s(q*ell*log(q))",
            "whole_decoder_bennett_bound_replaced_only_in_proposal": True,
            "complete_quantum_circuit_compiled": False,
            "new_quantum_algorithm_claim_allowed": False}


def controls():
    raw = FIXTURE.read_bytes()
    fixture = json.loads(raw)
    spec, received = fixture["parameters"], fixture["received_word"]
    p, ell, order, radius = (spec[key] for key in ("p", "ell", "order", "radius"))
    trace = interpolate_traced(p, ell, order, radius, received)
    cleaned = uncompute_interpolation(trace, received)
    pairs = sorted(list(leading(row, trace["weights"])) for row in trace["basis"])
    reference = sorted(list(leading(row, trace["weights"])) for row in fixture["independent_basis"])
    eligible = [row for row in trace["basis"] if leading(row, trace["weights"])[0] <= spec["a"]]
    chosen = min(eligible, key=lambda row: (len(DescendingSystem(p, spec["k"], row).free),
                                          leading(row, trace["weights"])[0]))
    system = DescendingSystem(p, spec["k"], chosen)
    vector_checks = [vector_roundtrip(p, spec["k"], chosen)]
    vector_checks += [vector_roundtrip(p, spec["k"], chosen, t, homogeneous=True) for t in system.free]
    matched = vector_checks[0]["output"] == system.vector()
    matched = matched and all(check["output"] == system.vector(t, homogeneous=True)
                              for check, t in zip(vector_checks[1:], system.free))
    if not cleaned["basis_restored_to_identity"] or pairs != reference or not matched:
        raise ArithmeticError("native reversible-workspace control failed")
    return {"status": "HYBRID_REVERSIBLE_WORKSPACE_PROPOSAL_REVIEW_PENDING",
            "fixture": {"path": str(FIXTURE.relative_to(ROOT)),
                        "sha256": hashlib.sha256(raw).hexdigest()},
            "native_trace": {**cleaned, "leading_pairs": pairs,
                             "matches_independent_crt_profile": pairs == reference,
                             "interpolation_records": spec["constraints"],
                             "cancellation_records": len(trace["reduction_history"]),
                             "triangular_vectors_checked": len(vector_checks),
                             "all_vector_scratch_cleared": all(row["scratch_all_zero"] for row in vector_checks),
                             "all_vectors_match_reference": matched},
            "native_workspace_ledger": workspace_ledger(p, ell, order, radius),
            "scope": "classical field-operation reversal controls, not a quantum circuit or a measured space advantage",
            "new_quantum_algorithm_claim_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"output": str(args.output), "status": report["status"],
                      "native_trace": report["native_trace"]}))


if __name__ == "__main__":
    main()
