"""Unconditional q-ary decoder-to-product-coset sampling with actual BPQM gates.

Local reduction derivation REVIEW PENDING. Bounded complete circuit checks,
not a compiled growing-LDPC receiver or a classical-hardness claim.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import product
import json
from math import prod, sqrt
from pathlib import Path
import sys

import numpy as np
from flint import nmod_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.ternary_coloring_bpqm import OMEGA, PHYSICAL, check_branches, node_gates, spectrum

REPORT = ROOT/"research/reductions/ternary_decoded_sampler.json"


def index(word):
    value = 0
    for digit in word:
        value = 3*value+digit
    return value


def matrix_data(rows):
    rows = tuple(tuple(row) for row in rows)
    if (not rows or not rows[0] or len(rows) > 4 or len(rows[0]) > 6 or
            any(len(row) != len(rows[0]) or any(type(x) is not int or x not in (0, 1, 2) for x in row)
                for row in rows)):
        raise ValueError("bounded explicit rectangular canonical F3 matrix required")
    reduced, rank = nmod_mat(rows, 3).rref()
    m = len(rows[0])
    pivots = [next(j for j in range(m) if reduced[i, j]) for i in range(rank)]
    free = tuple(j for j in range(m) if j not in pivots)
    if not 1 <= len(free) <= 2 or m+2*len(free) > 9:
        raise ValueError("UNKNOWN: complete circuit reference needs 1<=k<=2 and <=9 qutrits")
    basis = []
    for f in free:
        word = [0]*m
        word[f] = 1
        for i, pivot in enumerate(pivots):
            word[pivot] = -int(reduced[i, f]) % 3
        basis.append(tuple(word))
    if any(sum(x*y for x, y in zip(g, row)) % 3 for g in basis for row in rows):
        raise ArithmeticError("public Gaussian kernel basis fails original rows")
    return {"H": rows, "rank": rank, "basis_G": tuple(basis), "information_coordinates": free,
            "length": m, "dimension": len(free), "gauge_dimension": len(rows)-rank}


def local_gate(tensor, gate, axes):
    """Apply a specified one/two-qutrit gate, with other axes retained."""
    axes = tuple(axes)
    rest = tuple(j for j in range(tensor.ndim) if j not in axes)
    order = axes+rest
    shape = tuple(tensor.shape[j] for j in order)
    result = gate @ np.transpose(tensor, order).reshape(3**len(axes), -1)
    return np.transpose(result.reshape(shape), np.argsort(order))


def root_transform(mu, check_row, root):
    """Actual single-check qutrit BPQM root unitary, including its herald.

    Returned dense matrix is ONLY the bounded compilation of listed local
    gates. No PGM matrix, unknown-codeword phase or coset-count lookup is used.
    """
    mu = spectrum(mu)
    if len(check_row) != 3 or any(a not in (1, 2) for a in check_row):
        raise ValueError("three physical wires and three nonzero public check coefficients required")
    integer(root, "root wire", 0, 2)
    leaves = [j for j in range(3) if j != root]
    tensor = np.eye(27, dtype=complex).reshape(3, 3, 3, 27)
    negation = np.eye(3)[[0, 2, 1]]
    channels = []
    factors = []
    for leaf in leaves:
        factor = (-check_row[leaf]*check_row[root]) % 3  # a_root^-1=a_root in F3*
        factors.append(factor)
        if factor == 2:
            tensor = local_gate(tensor, negation, (leaf,))
            channels.append((mu[0], mu[2], mu[1]))
        else:
            channels.append(mu)
    check, _ = node_gates(*channels)
    tensor = local_gate(tensor, check, leaves)
    branches = {h: message for h, _, message in check_branches(*channels)}
    combined = np.zeros_like(tensor)
    for herald in range(3):
        # The absent-source branch STILL gets a total unitary completion.
        message = branches.get(herald, (1, 0, 0))
        _, bit = node_gates(mu, message)
        mask = np.zeros(3)
        mask[herald] = 1
        projected = local_gate(tensor, np.diag(mask), (leaves[0],))
        combined += local_gate(projected, bit, (root, leaves[1]))
    Fourier = np.array([[OMEGA**(i*j) for j in range(3)] for i in range(3)])/sqrt(3)
    result = local_gate(combined, Fourier.conj().T, (root,)).reshape(27, 27)
    residual = float(np.max(np.abs(result.conj().T @ result-np.eye(27))))
    if residual > 1e-11:
        raise ArithmeticError("gate-compiled BPQM root is not unitary on its FULL domain")
    return result, {"root_wire": root, "check_row": check_row, "normalized_child_coefficients": factors,
                    "check_gate_calls": 1, "herald_controlled_bit_blocks": 3,
                    "zero_probability_herald_completions": sorted(set(range(3))-set(branches)),
                    "herald_phase_removed_or_measured": False,
                    "dense_PGM_or_coset_probability_oracle_used": False,
                    "full_domain_unitarity_max_residual": residual}


class Decoder:
    """Known reversible circuit on data and a modular estimate register."""
    def __init__(self, code, mu, *, mode="bpqm", offset=None):
        if mode not in ("bpqm", "product", "none"):
            raise ValueError("explicit gate-implemented decoder mode required")
        self.code, self.mu, self.mode = code, spectrum(mu), mode
        m, k = code["length"], code["dimension"]
        self.words = tuple(product(range(3), repeat=m))
        self.labels = tuple(product(range(3), repeat=k))
        self.offset = (0,)*k if offset is None else tuple(offset)
        if len(self.offset) != k or any(type(v) is not int or v not in (0, 1, 2) for v in self.offset):
            raise ValueError("canonical constant decoder-offset trits required")
        self.transforms, self.recipes = [], []
        Fourier = np.array([[OMEGA**(i*j) for j in range(3)] for i in range(3)])/sqrt(3)
        for root in (() if mode == "none" else code["information_coordinates"]):
            if mode == "bpqm":
                row = next((row for row in code["H"] if len(row) == 3 and all(row)), None)
                if row is None:
                    raise ValueError("bounded BPQM compiler requires a native three-wire star check")
                T, recipe = root_transform(mu, row, root)
                self.recipes.append(recipe)
            else:
                tensor = np.eye(3**m, dtype=complex).reshape((3,)*m+(3**m,))
                T = local_gate(tensor, Fourier.conj().T, (root,)).reshape(3**m, 3**m)
            self.transforms.append((root, T))

    def _offset(self, state, sign):
        result = np.empty_like(state)
        for r, digits in enumerate(self.labels):
            t = index(tuple((a+sign*b) % 3 for a, b in zip(digits, self.offset)))
            result[:, t] = state[:, r]
        return result

    def apply(self, state, *, inverse=False):
        state = np.asarray(state, dtype=complex)
        if state.ndim != 3 or state.shape[1:] != (len(self.labels), len(self.words)):
            raise ValueError("batch x estimate x original data state required")
        if inverse:
            state = self._offset(state, -1)
        steps = list(enumerate(self.transforms))
        for i, (root, T) in (reversed(steps) if inverse else steps):
            state = state @ T.T
            copied = np.empty_like(state)
            for r, digits in enumerate(self.labels):
                for z in range(3):
                    target = list(digits)
                    target[i] = (target[i]+(-z if inverse else z)) % 3
                    mask = np.array([word[root] == z for word in self.words])
                    copied[:, index(target), mask] = state[:, r, mask]
            state = copied @ T.conj()
        return state if inverse else self._offset(state, 1)


def sources(code, mu):
    labels = tuple(product(range(3), repeat=code["dimension"]))
    words = tuple(product(range(3), repeat=code["length"]))
    codewords = tuple(tuple(sum(u*g[j] for u, g in zip(label, code["basis_G"])) % 3
                           for j in range(code["length"])) for label in labels)
    phi = np.array([sqrt(float(prod(mu[y] for y in word))) for word in words])
    states = np.array([phi*np.array([OMEGA**sum(a*b for a, b in zip(d, y)) for y in words]) for d in codewords])
    return phi, states, codewords


def subtract_label(state, labels):
    output = np.empty_like(state)
    for u, a in enumerate(labels):
        for r, b in enumerate(labels):
            output[index(tuple((x-y) % 3 for x, y in zip(a, b))), r] = state[u, r]
    return output


def prepare_source(code, mu, offsets):
    """Execute product rotations, label Fourier gates and PUBLIC bilinear phases.

    The input is a known blank, not a normalized coset state or a hidden
    source-preparation oracle. The dense tensor is bounded reference storage.
    """
    m, k = code["length"], code["dimension"]
    tensor = np.zeros((3,)*(m+2*k), complex)
    tensor[(0,)*(m+2*k)] = 1
    Fourier = np.array([[OMEGA**(i*j) for j in range(3)] for i in range(3)])/sqrt(3)
    phi = np.sqrt(list(map(float, mu)))
    difference = phi-np.array([1., 0., 0.])
    denominator = float(difference @ difference)
    rotation = np.eye(3) if denominator == 0 else np.eye(3)-2*np.outer(difference, difference)/denominator
    for j in range(m):
        tensor = local_gate(tensor, rotation, (2*k+j,))
    for i, row in enumerate(code["basis_G"]):
        tensor = local_gate(tensor, Fourier, (i,))
        shift = sum(a*b for a, b in zip(row, offsets)) % 3
        tensor = local_gate(tensor, np.diag([OMEGA**(-a*shift) for a in range(3)]), (i,))
        for j, coefficient in enumerate(row):
            if coefficient:
                phase = np.diag([OMEGA**(coefficient*a*b) for a, b in product(range(3), repeat=2)])
                tensor = local_gate(tensor, phase, (i, 2*k+j))
    return tensor.reshape(3**k, 3**k, 3**m)


def circuit(code, decoder, offsets, *, wrong_adjoint=False):
    offsets = tuple(offsets)
    if len(offsets) != code["length"] or any(type(x) is not int or x not in (0, 1, 2) for x in offsets):
        raise ValueError("unchanged canonical public offsets required")
    phi, _, _ = sources(code, decoder.mu)
    N, D = len(decoder.labels), len(decoder.words)
    initial = prepare_source(code, decoder.mu, offsets)
    actual = decoder.apply(initial)
    actual = subtract_label(actual, decoder.labels)
    actual = decoder.apply(actual, inverse=not wrong_adjoint)
    ideal = np.zeros_like(actual)
    target = tuple(sum(a*b for a, b in zip(row, offsets)) % 3 for row in code["basis_G"])
    for i, y in enumerate(decoder.words):
        if tuple(sum(a*b for a, b in zip(row, y)) % 3 for row in code["basis_G"]) == target:
            ideal[0, 0, i] = sqrt(N)*phi[i]
    return actual, ideal


@lru_cache(maxsize=64)
def lift_chart(rows):
    """Public polynomial Gaussian chart for H^T x=w, including dependencies."""
    v, m = len(rows), len(rows[0])
    augmented = [[rows[j][e] for j in range(v)]+[int(e == f) for f in range(m)] for e in range(m)]
    reduced, _ = nmod_mat(augmented, 3).rref()
    R = tuple(tuple(int(reduced[i, j]) for j in range(v)) for i in range(m))
    S = tuple(tuple(int(reduced[i, v+j]) for j in range(m)) for i in range(m))
    pivots = tuple(next(j for j in range(v) if row[j]) for row in R if any(row))
    free = tuple(j for j in range(v) if j not in pivots)
    return R, S, pivots, free


def affine_lift(rows, target, free_trits):
    """Actual polynomial postprocessing with explicit uniform gauge coins.

    Returns None on inconsistent data, NOT a certificate that the original
    nonlinear CSP is unsatisfiable. No solution enumeration or retries.
    """
    rows = tuple(tuple(row) for row in rows)
    target, free_trits = tuple(target), tuple(free_trits)
    if (not rows or not rows[0] or any(len(row) != len(rows[0]) or
            any(type(x) is not int or x not in (0, 1, 2) for x in row) for row in rows)
            or len(target) != len(rows[0]) or any(type(x) is not int or x not in (0, 1, 2) for x in target)):
        raise ValueError("explicit canonical rectangular H and original target required")
    R, S, pivots, free = lift_chart(rows)
    if len(free_trits) != len(free) or any(type(x) is not int or x not in (0, 1, 2) for x in free_trits):
        raise ValueError("one explicit canonical uniform trit per gauge coordinate required")
    transformed = tuple(sum(a*b for a, b in zip(row, target)) % 3 for row in S)
    if any(transformed[len(pivots):]):
        return None
    x = [0]*len(rows)
    for j, value in zip(free, free_trits):
        x[j] = value
    for i, j in enumerate(pivots):
        x[j] = (transformed[i]-sum(R[i][f]*x[f] for f in free)) % 3
    if any(sum(row[e]*value for row, value in zip(rows, x)) % 3 != t for e, t in enumerate(target)):
        raise ArithmeticError("Gaussian lift fails unchanged original H^T x=w")
    return tuple(x)


def native_distribution(code, mu, offsets, data_probabilities):
    """Exponential reference of polynomial Gaussian solve + uniform gauge lift.

    Invalid data or a point outside the affine image gives ABSTAIN. No branch
    is retried, conditioned on success, or labelled an UNSAT certificate.
    """
    spins = tuple(product(range(3), repeat=len(code["H"])))
    exact = []
    for x in spins:
        y = tuple((j+sum(row[e]*value for row, value in zip(code["H"], x))) % 3
                  for e, j in enumerate(offsets))
        exact.append(prod(mu[value] for value in y))
    partition = sum(exact)
    target = np.array([float(p/partition) for p in exact]+[0.]) if partition else np.array([0.]*len(spins)+[1.])
    output = np.zeros(len(spins)+1)
    for y, probability in zip(product(range(3), repeat=code["length"]), data_probabilities):
        w = tuple((value-j) % 3 for value, j in zip(y, offsets))
        x0 = affine_lift(code["H"], w, (0,)*code["gauge_dimension"])
        if any(not mu[j] for j in y) or x0 is None:
            output[-1] += probability
        else:
            for coins in product(range(3), repeat=code["gauge_dimension"]):
                x = affine_lift(code["H"], w, coins)
                output[index(x)] += probability/3**code["gauge_dimension"]
    return output, target, partition


def word_errors(code, decoder):
    _, states, _ = sources(code, decoder.mu)
    N, D = len(decoder.labels), len(decoder.words)
    batch = np.zeros((N, N, D), complex)
    batch[:, 0] = states
    decoded = decoder.apply(batch)
    errors = [max(0., min(1., 1-float(np.vdot(decoded[u, u], decoded[u, u]).real))) for u in range(N)]
    return errors


def audit_case(rows, mu=PHYSICAL, *, mode="bpqm", offset=None, wrong_adjoint=False):
    code, mu = matrix_data(rows), spectrum(mu)
    decoder = Decoder(code, mu, mode=mode, offset=offset)
    errors = word_errors(code, decoder)
    delta = float(np.mean(errors))
    phi, _, _ = sources(code, mu)
    all_rows = []
    for offsets in product(range(3), repeat=code["length"]):
        actual, ideal = circuit(code, decoder, offsets, wrong_adjoint=wrong_adjoint)
        probabilities = (abs(actual)**2).sum(axis=(0, 1))
        output, target, partition = native_distribution(code, mu, offsets, probabilities)
        spin_proposal_acceptance = partition/(3**len(code["H"])*max(mu)**code["length"])
        squared_distance = float(np.vdot((actual-ideal).ravel(), (actual-ideal).ravel()).real)
        actual_norm, ideal_norm = float((abs(actual)**2).sum()), float((abs(ideal)**2).sum())
        TV = float(abs(output-target).sum()/2)
        # Same-input polynomial baseline: sample product y and solve/lift once.
        shadow, _, _ = native_distribution(code, mu, offsets, phi**2)
        if abs(actual_norm-1) > 1e-10 or abs(sum(output)-1) > 1e-10:
            raise ArithmeticError("full unconditional circuit/output normalization failed")
        if not wrong_adjoint and partition and TV > min(1., 2*sqrt(squared_distance))+1e-10:
            raise ArithmeticError("per-offset normalization-aware sampling inequality failed")
        all_rows.append({"original_offsets": offsets, "native_partition_exact": str(partition),
                         "uniform_original_spin_rejection_acceptance_exact": str(spin_proposal_acceptance),
                         "target_empty": not bool(partition), "actual_total_probability_numeric": actual_norm,
                         "comparison_vector_squared_norm_numeric": ideal_norm,
                         "full_state_distance_squared_numeric": squared_distance,
                         "unconditional_TV_with_ABSTAIN_numeric": TV,
                         "invalid_output_ABSTAIN_probability_numeric": float(output[-1]),
                         "source_label_zero_probability_numeric": float((abs(actual[0])**2).sum()),
                         "same_input_classical_shadow_TV_from_actual_numeric": float(abs(output-shadow).sum()/2),
                         "postselection_or_retries_used": False})
    mean_distance = float(np.mean([r["full_state_distance_squared_numeric"] for r in all_rows]))
    identity_residual = abs(mean_distance-2*delta)
    if not wrong_adjoint and identity_residual > 1e-10:
        raise ArithmeticError("average over ALL original offsets does not equal twice decoder error")
    classical_mean = sum(Fraction(row["uniform_original_spin_rejection_acceptance_exact"]) for row in all_rows)/len(all_rows)
    if classical_mean != Fraction(1, 3*max(mu))**code["length"]:
        raise ArithmeticError("same-input uniform-spin proposal population law failed")
    return {"H": code["H"], "G": code["basis_G"], "information_coordinates": code["information_coordinates"],
            "original_row_rank": code["rank"], "dependent_and_zero_rows_retained": True,
            "gauge_dimension": code["gauge_dimension"], "normalized_product_spectrum": list(map(str, mu)),
            "native_postprocessing": "actual_polynomial_Gaussian_solve_and_uniform_gauge_coins",
            "source_preparation": "executed_local_rotations_label_Fourier_and_public_G_controlled_phases",
            "source_or_normalized_coset_preparation_oracle_used": False,
            "decoder_mode": mode, "decoder_constant_offset": decoder.offset, "root_gate_recipes": decoder.recipes,
            "wrong_adjoint_deliberately_used": wrong_adjoint,
            "all_codeword_error_probabilities_numeric": errors, "mean_word_error_numeric": delta,
            "mean_full_state_distance_squared_numeric": mean_distance,
            "Parseval_identity_residual_numeric": identity_residual,
            "mean_unconditional_native_TV_numeric": float(np.mean([r["unconditional_TV_with_ABSTAIN_numeric"] for r in all_rows])),
            "empty_original_offset_fraction_exact": str(Fraction(sum(r["target_empty"] for r in all_rows), len(all_rows))),
            "mean_valid_native_output_probability_numeric": float(np.mean([1-r["invalid_output_ABSTAIN_probability_numeric"] for r in all_rows])),
            "mean_native_TV_on_NONEMPTY_targets_numeric": float(np.mean([r["unconditional_TV_with_ABSTAIN_numeric"] for r in all_rows if not r["target_empty"]])) if any(not r["target_empty"] for r in all_rows) else None,
            "average_TV_upper_from_word_error_NUMERICAL": min(1., 2*sqrt(2*delta)),
            "all_original_offset_rows": all_rows,
            "uniform_spin_rejection_mean_acceptance_exact": str(classical_mean),
            "product_then_affine_solve_mean_acceptance_exact": str(Fraction(1, 3**code["dimension"])),
            "retained_qutrits_in_bounded_reference": code["length"]+2*code["dimension"],
            "statevector_and_affine_fiber_census_cost_is_exponential": True,
            "scalable_whole_LDPC_receiver_compiled": False,
            "speedup_claim_allowed": False, "accepted_speedup_candidate": False}


def run_controls():
    paths = [Path(__file__), ROOT/"theorems/ternary_coloring_bpqm.py", ROOT/"theorems/bpqm_gibbs_frontier.py"]
    before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    star = ((1, 1, 1),)
    cases = [audit_case(star), audit_case(star, mode="none"), audit_case(star, offset=(1, 0)),
             audit_case(star, (Fraction(1, 4), Fraction(3, 8), Fraction(3, 8))),
             audit_case(star, (Fraction(1, 3),)*3),
             audit_case(((1, 2, 1), (2, 1, 2), (0, 0, 0))),
             audit_case(((1, 1, 0),), mode="product")]
    bad = audit_case(star, wrong_adjoint=True)
    if before != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}:
        raise RuntimeError("producer or dependency changed during run")
    return {"schema_version": 1, "status": "UNCONDITIONAL_QARY_REDUCTION_AND_BOUNDED_BPQM_GATES_REVIEW_PENDING",
            "source_sha256": before, "cases": cases, "wrong_adjoint_countercontrol": bad,
            "general_average_identity": "E_J ||actual_J-comparison_J||^2 = 2*delta",
            "general_average_TV_bound": "min(1,2*sqrt(2*delta))",
            "general_finite_block_error_or_speedup_from_examples_inferred": False,
            "local_reduction_proof_independently_reviewed": False,
            "natural_3_6_LDPC_sampler_executed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": report["status"], "controls": [
        {"decoder": r["decoder_mode"], "delta": r["mean_word_error_numeric"],
         "mean_TV": r["mean_unconditional_native_TV_numeric"],
         "identity_residual": r["Parseval_identity_residual_numeric"]} for r in report["cases"]],
        "wrong_adjoint_identity_residual": report["wrong_adjoint_countercontrol"]["Parseval_identity_residual_numeric"]}, indent=2))


if __name__ == "__main__":
    main()
