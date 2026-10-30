"""Resource/precision ledger and capped finite controls for coherent sign lifting.

No quantum circuit is compiled or executed. The all-size construction is
specified in COHERENT_SIGN.md; dense arrays below are verification only.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import permutations, product
import hashlib
import math
from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hdqi-sign-sampler-2026-10-24"))
import sign_sampler as s


def tables(model, eta):
    even, odd, proposal = [], [], []
    for x in model.x:
        e = s.parity_law(x, 0, eta)
        o = s.parity_law(x, 1, eta) if x else None
        e_sum = e.law.normalizer
        o_sum = x * o.law.normalizer if o else F(0)
        even.append(e)
        odd.append(o)
        proposal.append(s.RationalLaw.create((0, 1), (e_sum**2, o_sum**2)))
    return even, odd, proposal


def precision_ledger(model, epsilon=F(1, 8), delta=F(1, 16)):
    epsilon, delta = s.rational(epsilon), s.rational(delta)
    if not 0 < epsilon <= F(1, 4) or not 0 < delta <= F(1, 4):
        raise ValueError("epsilon and delta must be in (0,1/4]")
    mass = sum(j*j for j in model.couplings)
    bounds = s.ratio_bounds(model.m, model.degree, mass, max(map(abs, model.couplings)), model.beta)
    cbar = bounds["ratio_upper"]
    eta = epsilon*epsilon / (16384 * model.m * cbar*cbar)
    even, odd, proposal = tables(model, eta)
    length = sum(max(e.law.outcomes[-1], o.law.outcomes[-1] if o else 0)
                 for e, o in zip(even, odd))
    entries = sum(len(p.law.outcomes) for p in even + [o for o in odd if o])
    # A loose bound on abstract controlled rotations, not elementary gates.
    rotations = model.m + 4*entries + 2*length*(length+1)
    circuit_error = epsilon / (16*cbar)
    r = 0
    while F(1, 2**r) > delta:
        r += 1
    return {**bounds, "m": model.m, "degree": model.degree, "mass": mass,
            "epsilon": epsilon, "delta": delta, "site_tail": eta,
            "whole_trial_operator_error": circuit_error,
            "per_abstract_rotation_error": circuit_error/rotations,
            "abstract_rotation_count_bound": rotations,
            "local_table_entries": entries, "max_word_letters": length,
            "shuffle_history_bits_bound": sum((j-1).bit_length() for j in range(2, length+1)),
            "word_label_bits_bound": length * max(1, (model.m-1).bit_length()),
            "count_register_bits_bound": sum(max(e.law.outcomes[-1], o.law.outcomes[-1] if o else 0).bit_length()
                                               for e, o in zip(even, odd)),
            "largest_probability_integer_bits": max(law.cumulative[-1].bit_length() for law in
                                                     [p.law for p in even] + [p.law for p in odd if p] + proposal),
            "success_probability_lower": F(1, 2*cbar), "max_attempts": 2*cbar*r,
            "failure_probability_upper": F(1, 2**r),
            "conditional_trace_distance_upper": epsilon/4,
            "is_compiled_gate_count": False, "quantum_execution": False,
            "amplitude_amplification_used": False}


def known_sign(model, mask):
    return (-1)**mask.bit_count() * math.prod(-1 if j < 0 else 1
                                             for i, j in enumerate(model.couplings) if mask >> i & 1)


def labelled_permutations(counts):
    if not counts or any(type(n) is not int or n < 0 for n in counts) or sum(counts) > 7:
        raise ValueError("finite history control requires length <=7")
    word = tuple(i for i, n in enumerate(counts) for _ in range(n))
    for indices in permutations(range(len(word))):
        yield tuple(word[i] for i in indices)


def finite_histories(model, mask, eta, max_histories=4096):
    if model.m > 3 or type(mask) is not int or not 0 <= mask < 1 << model.m:
        raise ValueError("finite history control requires m<=3 and valid mask")
    even, odd, _ = tables(model, eta)
    laws = [odd[i] if mask >> i & 1 else even[i] for i in range(model.m)]
    if any(law is None for law in laws):
        raise ValueError("zero-probability label")
    out = []
    for entries in product(*(law.law.probabilities() for law in laws)):
        counts = tuple(k for k, _ in entries)
        if sum(counts) > 7:
            raise ValueError("finite history length cap exceeded")
        number = math.factorial(sum(counts))
        if len(out) + number > max_histories:
            raise ValueError("finite history count cap exceeded")
        probability = math.prod(p for _, p in entries)/number
        for word in labelled_permutations(counts):
            sign, endpoint = s.word_sign(model, word)
            assert endpoint == mask
            out.append((probability, sign))
    return tuple(out)


def householder_prepare(vector):
    """Dense control only: unitary with the specified real first column."""
    import numpy as np
    vector = np.asarray(vector, dtype=float)
    if vector.ndim != 1 or len(vector) > 4096 or abs(np.linalg.norm(vector)-1) > 1e-12:
        raise ValueError("small normalized real vector required")
    first = np.zeros_like(vector)
    first[0] = 1
    difference = first-vector
    norm = np.linalg.norm(difference)
    return np.eye(len(vector)) if norm < 1e-15 else np.eye(len(vector))-2*np.outer(difference, difference)/(norm*norm)


def finite_unitary_control(model, eta=F(1, 100), include_known_sign=True, unprepare=True):
    """Small explicit U^dagger D U blocks; not the scalable realization."""
    import numpy as np
    if model.m > 3:
        raise ValueError("finite unitary control requires m<=3")
    _, _, proposals = tables(model, eta)
    q = [math.prod(proposals[i].probabilities()[y >> i & 1][1] for i in range(model.m))
         for y in range(1 << model.m)]
    histories = [finite_histories(model, y, eta, max_histories=64) if q[y] else () for y in range(1 << model.m)]
    width = max(2, max(map(len, histories)))
    width = 1 << (width-1).bit_length()
    joint, expected = np.zeros((1 << model.m, width)), np.zeros(1 << model.m)
    unitarity = 0.0
    for y, history in enumerate(histories):
        if not history:
            continue
        amplitude, signs = np.zeros(width), np.ones(width)
        for i, (p, sign) in enumerate(history):
            amplitude[i], signs[i] = math.sqrt(float(p)), sign
        u = householder_prepare(amplitude)
        unitarity = max(unitarity, float(np.max(np.abs(u.T@u-np.eye(width)))))
        branch = signs * (u[:, 0])
        if unprepare:
            branch = u.T @ branch
        phase = known_sign(model, y) if include_known_sign else 1
        joint[y] = phase * math.sqrt(float(q[y])) * branch
        expected[y] = phase * math.sqrt(float(q[y])) * float(sum(p*sgn for p, sgn in history))
    return {"joint": joint, "expected_good": expected, "q": np.array(list(map(float, q))),
            "unitarity_error": unitarity, "work_width": width}


def finite_exact_branch(model, eta):
    """Exact multiset recurrence plus floating roots; independent of histories."""
    import numpy as np
    if model.m > 3:
        raise ValueError("finite branch control requires m<=3")
    even, odd, proposals = tables(model, eta)
    branch = []
    for y in range(1 << model.m):
        q = math.prod(proposals[i].probabilities()[y >> i & 1][1] for i in range(model.m))
        if not q:
            branch.append(0.0)
            continue
        laws = [odd[i] if y >> i & 1 else even[i] for i in range(model.m)]
        mean = F(0)
        for entries in product(*(law.law.probabilities() for law in laws)):
            counts = tuple(k for k, _ in entries)
            permutations_count = math.factorial(sum(counts)) // math.prod(math.factorial(k) for k in counts)
            mean += math.prod(p for _, p in entries) * F(s.exact_sign_sum(model, counts), permutations_count)
        branch.append(known_sign(model, y) * math.sqrt(float(q)) * float(mean))
    return np.array(branch)


def receipt():
    import numpy as np
    from scipy.linalg import expm
    sys.path.insert(0, str(ROOT / "hdqi-parent-gap-2026-10-23"))
    from parent_gap import build_model

    rows = []
    for name, js, edges in (("edge", [1, 1], [(0, 1)]),
                            ("signed_commuting", [1, -1], []),
                            ("path", [1, -1, F(1, 2)], [(0, 1), (1, 2)])):
        model = s.Model.create(js, F(1, 4), edges)
        plan = precision_ledger(model)
        control = finite_unitary_control(model)
        branch = finite_exact_branch(model, plan["site_tail"])
        h = build_model(model.m, model.edges, [float(j) for j in model.couplings]).h
        a = expm(-float(model.beta)*h/2)[:, 0]
        zc = math.prod(math.cosh(float(model.beta*j)) for j in model.couplings)
        rows.append({"name": name, "ledger": s.public_plan(plan),
                     "unitary_control_site_tail": "1/100",
                     "unitary_block_error": float(np.max(np.abs(control["joint"][:, 0]-control["expected_good"]))),
                     "unitarity_error": control["unitarity_error"],
                     "precise_success_probability": float(np.dot(branch, branch)),
                     "ideal_success_probability": float(np.dot(a, a)/zc),
                     "subnormalized_error": float(np.linalg.norm(branch-a/math.sqrt(zc))),
                     "normalized_vector_error": float(np.linalg.norm(branch/np.linalg.norm(branch)-a/np.linalg.norm(a)))})
    model = s.Model.create([1]*128, F(1, 8), sorted({tuple(sorted((i, (i+j) % 128))) for i in range(128) for j in range(1, 5)}))
    here = Path(__file__).resolve().parent
    paths = [here/f for f in ("coherent_sign.py", "test_coherent_sign.py", "COHERENT_SIGN.md", "HANDOFF.md")]
    paths += [ROOT/"hdqi-sign-sampler-2026-10-24"/f for f in ("sign_sampler.py", "SIGN_SAMPLER.md")]
    paths += [ROOT/"hdqi-cluster-baseline-2026-10-24/CLUSTER_BASELINE.md"]
    return {"status": "local_unreviewed_coherent_construction", "finite_controls": rows,
            "explicit_128_bit_resource_ledger_only": s.public_plan(precision_ledger(model)),
            "quantum_execution": False, "compiled_circuit": False,
            "degree_gap_proved": False, "speedup_admitted": False,
            "hashes": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("receipt.json"))
    args = parser.parse_args()
    data = receipt()
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"output": str(args.output.resolve()), "controls": len(data["finite_controls"]),
                      "quantum_execution": False}))

