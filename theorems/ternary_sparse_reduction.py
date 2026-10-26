"""Solution-preserving ternary addition gadgets do not preserve decodability.

The paired-exclusion construction creates a disjoint short-word subcode.
Its signed-trine optimal discrimination bound is information theoretic, but
blocks only the small-WORD-error premise, not all possible sampling routes.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path
import random
import sys

import numpy as np
from flint import nmod_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.ternary_classical_sampling import SAVED_SOURCE, saved_cases, valid, validate_problem
from theorems.ternary_conditioned_sampling import REPORT as SAMPLES, natural, power_interval

REPORT = ROOT / "research/reductions/ternary_sparse_reduction.json"


def dense_data(problem):
    n = natural(problem["spins"], "original spin count", 1)
    forms, offsets = tuple(map(tuple, problem["forms"])), tuple(problem["offsets"])
    if n > 4096 or not forms or len(forms) != len(offsets) or any(
        len(row) != n or any(type(v) is not int or v not in (0, 1, 2) for v in row) for row in forms
    ) or any(type(j) is not int or j not in (0, 1, 2) for j in offsets):
        raise ValueError("explicit bounded canonical dense F3 problem required")
    return n, forms, offsets


def dense_valid(problem, word):
    n, forms, offsets = dense_data(problem)
    return len(word) == n and all(type(x) is int and x in (0, 1, 2) for x in word) and all(
        (j+sum(a*x for a, x in zip(row, word))) % 3 for row, j in zip(forms, offsets))


@dataclass(frozen=True)
class SparseReduction:
    source: dict
    target: dict
    additions: tuple
    pairs: tuple
    owners: tuple
    finals: tuple

    def lift(self, word):
        n, _, _ = dense_data(self.source)
        if len(word) != n or any(type(x) is not int or x not in (0, 1, 2) for x in word):
            raise ValueError("one canonical value for EVERY original spin required")
        extended = list(word)
        for left, a, right, b, output in self.additions:
            if output != len(extended):
                raise ArithmeticError("addition schedule is not forward triangular")
            extended.append((a*extended[left]+b*extended[right]) % 3)
        return tuple(extended)

    def lift_codeword(self, word, coins):
        """Explicit splitting C_sparse = C_dense plus the gadget subcode."""
        word, coins = tuple(word), tuple(coins)
        codeword(self.source, word)
        if len(coins) != len(self.pairs) or any(type(x) is not int or x not in (0, 1, 2) for x in coins):
            raise ValueError("one canonical gadget-subcode coordinate per pair required")
        out = [0]*len(self.target["forms"])
        for f, index in enumerate(self.finals):
            out[index] = word[f]
        for (p, q), owner, coin in zip(self.pairs, self.owners, coins):
            out[p], out[q] = coin, (-word[owner]-coin) % 3
        codeword(self.target, out)
        return tuple(out)

    def project_codeword(self, word):
        codeword(self.target, word)
        projected = tuple(word[index] for index in self.finals)
        codeword(self.source, projected)
        return projected


def codeword(problem, word):
    n, forms, _ = dense_data(problem)
    if len(word) != len(forms) or any(type(x) is not int or x not in (0, 1, 2) for x in word):
        raise ValueError("one canonical code coordinate per constraint required")
    if any(sum(row[i]*x for row, x in zip(forms, word)) % 3 for i in range(n)):
        raise ValueError("word does not lie in the exact parity-check kernel")


def sparsify(problem):
    """Replace a dense exclusion by ternary additions and one final exclusion.

    t=a*x+b*y iff t-a*x-b*y+1 !=0 AND t-a*x-b*y+2 !=0.
    There is exactly one auxiliary extension, not a SAT-only reduction.
    """
    n, forms, offsets = dense_data(problem)
    count = n+sum(max(0, sum(bool(a) for a in row)-3) for row in forms)
    if count > 4096:
        raise ValueError("UNKNOWN: explicit reduction reference spin cap")
    sparse, out_offsets, additions, pairs, owners, finals = [], [], [], [], [], []
    next_spin = n
    for owner, (row, offset) in enumerate(zip(forms, offsets)):
        terms = [(i, a) for i, a in enumerate(row) if a]
        while len(terms) > 3:
            (left, a), (right, b) = terms[:2]
            output = next_spin
            next_spin += 1
            equality = {left: -a % 3, right: -b % 3, output: 1}
            pairs.append((len(sparse), len(sparse)+1))
            owners.append(owner)
            sparse.extend((equality, equality))
            out_offsets.extend((1, 2))
            additions.append((left, a, right, b, output))
            terms = [(output, 1)]+terms[2:]
        finals.append(len(sparse))
        sparse.append(dict(terms))
        out_offsets.append(offset)
    target = {"spins": next_spin,
              "forms": [[row.get(j, 0) for j in range(next_spin)] for row in sparse],
              "offsets": out_offsets}
    validate_problem(target)
    source = {"spins": n, "forms": forms, "offsets": offsets}
    return SparseReduction(source, target, tuple(additions), tuple(pairs), tuple(owners), tuple(finals))


def short_subcode(problem, pairs):
    """Check disjoint witnesses e_p-e_q in ker(H), without enumerating it."""
    _, forms, offsets = validate_problem(problem)
    pairs = tuple(map(tuple, pairs))
    seen = set()
    for pair in pairs:
        if len(pair) != 2 or any(type(i) is not int or not 0 <= i < len(forms) for i in pair):
            raise ValueError("valid constraint-index pairs required")
        p, q = pair
        if p == q or p in seen or q in seen:
            raise ValueError("disjoint physical pair supports required for product bound")
        if not any(forms[p]) or forms[p] != forms[q]:
            raise ValueError("equal nonzero H columns required for e_p-e_q witness")
        seen.update(pair)
    return {"disjoint_pairs": pairs, "independent_short_subcode_dimension": len(pairs),
            "witnesses": "e_p-e_q for each recorded pair; disjoint support proves independence",
            "minimum_distance_at_most_2": bool(pairs),
            "all_ordered_offset_differences_are_1": all((offsets[q]-offsets[p]) % 3 == 1 for p, q in pairs)}


def success_bound(gadgets, bits=128):
    """Outward bound on ((3+2 sqrt(2))/6)^g for optimal whole-code success."""
    natural(gadgets, "disjoint gadgets")
    natural(bits, "precision", 1)
    scale = 1 << bits
    root = isqrt(2*scale*scale)
    low, high = Fraction(root, scale), Fraction(root+1, scale)
    p_lo, p_hi = (3+2*low)/6, (3+2*high)/6
    lower, _ = power_interval(p_lo, gadgets, bits)
    _, upper = power_interval(min(Fraction(1), p_hi), gadgets, bits)
    return {"disjoint_gadgets": gadgets, "one_pair_success_exact": "(3+2*sqrt(2))/6",
            "product_subcode_optimal_success_interval": [str(lower), str(upper)],
            "full_code_any_measurement_word_success_upper": str(upper),
            "full_code_any_measurement_word_error_lower": str(1-upper),
            "conditional_IID_offset_probability_of_ordered_pair_event": str(Fraction(1, 3**gadgets)),
            "offset_source_TV_lower_if_all_ordered_differences_1": str(1-Fraction(1, 3**gadgets)),
            "applies_to_one_original_signed_trine_output_per_code_coordinate": True,
            "small_word_error_premise_transfer_blocked": bool(gadgets),
            "all_sampling_or_sparsification_algorithms_ruled_out": False}


def pair_certificate():
    """Independent physical Gram, PGM primal and explicit SDP-dual replay."""
    omega = np.exp(2j*np.pi/3)
    trines = [np.array([0, omega**x, omega**(2*x)])/np.sqrt(2) for x in range(3)]
    physical = np.column_stack([np.kron(trines[x], trines[-x % 3]) for x in range(3)])
    nu = np.array([.5, .25, .25])
    states = np.column_stack([np.sqrt(nu)*omega**(x*np.arange(3)) for x in range(3)])
    measurement = np.column_stack([omega**(x*np.arange(3))/np.sqrt(3) for x in range(3)])
    dual = np.diag(np.sqrt(nu)*sum(np.sqrt(nu))/3)
    primal = sum(abs(np.vdot(measurement[:, x], states[:, x]))**2 for x in range(3))/3
    return {"effective_spectrum_exact": ["1/2", "1/4", "1/4"],
            "physical_vs_compressed_Gram_residual": float(np.max(abs(physical.conj().T@physical-states.conj().T@states))),
            "measurement_completeness_residual": float(np.max(abs(measurement@measurement.conj().T-np.eye(3)))),
            "dual_slack_minimum_eigenvalue": float(min(np.linalg.eigvalsh(dual-np.outer(v, v.conj())/3)[0] for v in states.T)),
            "primal_dual_gap": float(abs(primal-np.trace(dual))),
            "optimal_success_numeric_NOT_certificate": float(primal),
            "proof": "Y=(sum sqrt(nu))/3 diag(sqrt(nu)); Cauchy-Schwarz gives Y>=|psi_x><psi_x|/3. Tensor both primal and dual."}


def scramble(problem, seed):
    """Public invertible spin-basis change for same-input reduction controls."""
    n, forms, offsets = dense_data(problem)
    natural(seed, "seed")
    rng = random.Random(seed)
    T = np.eye(n, dtype=np.int64)
    if n > 1:
        for _ in range(12*n):
            i, j = rng.sample(range(n), 2)
            T[i] = (T[i]+rng.choice((1, 2))*T[j]) % 3
    matrix = nmod_mat(T.tolist(), 3)
    if matrix.rank() != n:
        raise ArithmeticError("public basis change lost invertibility")
    dense = {"spins": n, "forms": ((np.array(forms, dtype=np.int64)@T) % 3).tolist(), "offsets": offsets}
    return dense, matrix


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def run_controls():
    dependencies = [Path(__file__), SAMPLES, SAVED_SOURCE,
                    ROOT/"theorems/ternary_classical_sampling.py", ROOT/"theorems/ternary_conditioned_sampling.py"]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}
    recorded = json.loads(SAMPLES.read_text())["cases"]
    cases = []
    for i, problem in enumerate(saved_cases()):
        dense, T = scramble(problem, 7191+i)
        reduction = sparsify(dense)
        source_record = next(c for c in recorded if c["problem"] == problem)
        x = source_record["rank_rejection"]["sample"]
        vector = T.inv()*nmod_mat([[v] for v in x], 3)
        z = tuple(int(vector[j, 0]) for j in range(problem["spins"]))
        lifted = reduction.lift(z)
        if not valid(problem, x) or not dense_valid(dense, z) or not valid(reduction.target, lifted):
            raise ArithmeticError("same-input sample failed invertible basis/reduction replay")
        witness = short_subcode(reduction.target, reduction.pairs)
        cases.append({"original_problem": problem, "public_basis_seed": 7191+i,
                      "public_basis_T": [[int(T[r, c]) for c in range(T.ncols())] for r in range(T.nrows())],
                      "dense_problem_sha256": digest(dense), "sparse_problem_sha256": digest(reduction.target),
                      "original_spins": problem["spins"], "original_constraints": len(problem["forms"]),
                      "dense_form_weights": [sum(bool(a) for a in row) for row in dense["forms"]],
                      "expanded_spins": reduction.target["spins"], "expanded_constraints": len(reduction.target["forms"]),
                      "auxiliary_spins": len(reduction.additions), "short_subcode": witness,
                      "exact_code_quotient": "C_sparse / span{e_p-e_q} is isomorphic to C_dense by final-coordinate projection",
                      "rank_change_exact": len(reduction.additions),
                      "quantum_word_bound": success_bound(len(reduction.pairs)),
                      "original_sample": x, "dense_sample": z, "expanded_sample_sha256": digest(lifted),
                      "sample_replay_verified": True, "complete_solution_counts_recomputed": False,
                      "hard_dense_input_claimed": False, "random_LDPC_ensemble_membership_claimed": False})
    if hashes != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}:
        raise RuntimeError("source changed during reduction audit")
    return {"schema_version": 1, "status": "PAIRED_EQUALITY_GADGET_DECODING_TRANSFER_REJECTED_REVIEW_PENDING",
            "source_sha256": hashes, "pair_certificate": pair_certificate(), "same_input_controls": cases,
            "analytical_bounds": [success_bound(g) for g in (0, 1, 10, 100, 1000)],
            "source": "https://arxiv.org/abs/quant-ph/0005132",
            "generic_sparsification_or_sampler_no_go_claimed": False,
            "novel_quantum_algorithm_claimed": False, "independent_proof_review_complete": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    for case in report["same_input_controls"]:
        print(json.dumps({"spins": case["original_spins"], "gadgets": case["auxiliary_spins"],
                          "word_success_upper": float(Fraction(case["quantum_word_bound"]["full_code_any_measurement_word_success_upper"]))}))
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
