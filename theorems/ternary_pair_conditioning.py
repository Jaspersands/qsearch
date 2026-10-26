"""Local source conditioning before coherent quotient decoding.

Duplicate-column subcodes can be imposed by explicit local preparation, not
decoded or postselected. This preserves the target but does not supply an
efficient residual decoder or an advantage over the matched classical law.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
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

from theorems.ternary_coloring_bpqm import OMEGA, PHYSICAL, check_branches, node_gates, spectrum
from theorems.ternary_classical_sampling import SAVED_SOURCE, saved_cases
from theorems.ternary_decoded_sampler import Decoder, index, local_gate, matrix_data, native_distribution, subtract_label

REPORT = ROOT / "research/reductions/ternary_pair_conditioning.json"


def canonical_word(word, size):
    word = tuple(word)
    if len(word) != size or any(type(x) is not int or x not in (0, 1, 2) for x in word):
        raise ValueError("complete canonical F3 word required")
    return word


@dataclass(frozen=True)
class PairConditioning:
    original_H: tuple
    original_spectra: tuple
    original_offsets: tuple
    pairs: tuple
    differences: tuple
    kept: tuple
    H: tuple
    spectra: tuple | None
    offsets: tuple
    local_masses: tuple

    @classmethod
    def build(cls, H, spectra, offsets, pairs):
        H = tuple(map(tuple, H))
        if not H or not H[0] or any(len(row) != len(H[0]) or
            any(type(x) is not int or x not in (0, 1, 2) for x in row) for row in H):
            raise ValueError("nonempty explicit canonical matrix required")
        mus = tuple(map(spectrum, spectra))
        if len(mus) != len(H[0]):
            raise ValueError("one normalized spectrum per physical coordinate required")
        offsets = canonical_word(offsets, len(mus))
        pairs = tuple(map(tuple, pairs))
        seen = set()
        for pair in pairs:
            if len(pair) != 2 or any(type(i) is not int or not 0 <= i < len(mus) for i in pair):
                raise ValueError("valid physical coordinate pairs required")
            p, q = pair
            if p == q or p in seen or q in seen:
                raise ValueError("disjoint physical pairs required")
            if not any(row[p] for row in H) or any(row[p] != row[q] for row in H):
                raise ValueError("equal nonzero H columns required")
            seen.update(pair)
        differences = tuple((offsets[p]-offsets[q]) % 3 for p, q in pairs)
        conditioned = list(mus)
        masses = []
        for (p, q), t in zip(pairs, differences):
            weights = tuple(mus[p][a]*mus[q][(a-t) % 3] for a in range(3))
            mass = sum(weights)
            masses.append(mass)
            if mass:
                conditioned[p] = spectrum(w/mass for w in weights)
        removed = {q for _, q in pairs}
        kept = tuple(i for i in range(len(mus)) if i not in removed)
        return cls(H, mus, offsets, pairs, differences, kept,
                   tuple(tuple(row[i] for i in kept) for row in H),
                   tuple(conditioned[i] for i in kept) if all(masses) else None,
                   tuple(offsets[i] for i in kept), tuple(masses))

    def expand(self, word):
        word = canonical_word(word, len(self.kept))
        expanded = [0]*len(self.original_offsets)
        for i, value in zip(self.kept, word):
            expanded[i] = value
        for (p, q), t in zip(self.pairs, self.differences):
            expanded[q] = (expanded[p]-t) % 3
        return tuple(expanded)

    def compress(self, word):
        word = canonical_word(word, len(self.original_offsets))
        if any((word[p]-word[q]) % 3 != t for (p, q), t in zip(self.pairs, self.differences)):
            raise ValueError("word lies outside the prescribed local syndrome sector")
        return tuple(word[i] for i in self.kept)

    def expand_state(self, state):
        """Actual SUM/shift circuit from blank removed wires; no projection."""
        state = np.asarray(state, dtype=complex)
        if state.ndim < 1 or state.shape[-1] != 3**len(self.kept):
            raise ValueError("last axis must hold the contracted physical register")
        m = len(self.original_offsets)
        if prod(state.shape[:-1])*3**m > 3**11:
            raise ValueError("UNKNOWN: bounded full-state expansion cap")
        lead = state.ndim-1
        tensor = np.zeros(state.shape[:-1]+(3,)*m, complex)
        selection = [slice(None)]*lead+[slice(None) if i in self.kept else 0 for i in range(m)]
        tensor[tuple(selection)] = state.reshape(state.shape[:-1]+(3,)*len(self.kept))
        for (p, q), t in zip(self.pairs, self.differences):
            tensor = local_gate(tensor, pair_gate(t), (lead+p, lead+q))
        return tensor.reshape(state.shape[:-1]+(3**m,))


def pair_gate(t):
    canonical_word((t,), 1)
    U = np.zeros((9, 9), complex)
    for a, b in product(range(3), repeat=2):
        U[3*a+(b+a-t) % 3, 3*a+b] = 1
    return U


def heterogeneous_root(mus, check, root):
    """Existing three-wire BPQM gate recipe with nonidentical local spectra."""
    mus = tuple(map(spectrum, mus))
    if len(mus) != 3 or len(check) != 3 or any(type(a) is not int or a not in (1, 2) for a in check):
        raise ValueError("three public nonzero check coefficients/spectra required")
    if type(root) is not int or root not in (0, 1, 2):
        raise ValueError("physical root index required")
    leaves = [j for j in range(3) if j != root]
    tensor = np.eye(27, dtype=complex).reshape(3, 3, 3, 27)
    channels = []
    for leaf in leaves:
        mu = mus[leaf]
        if (-check[leaf]*check[root]) % 3 == 2:
            tensor = local_gate(tensor, np.eye(3)[[0, 2, 1]], (leaf,))
            mu = (mu[0], mu[2], mu[1])
        channels.append(mu)
    check_gate, _ = node_gates(*channels)
    tensor = local_gate(tensor, check_gate, leaves)
    branches = {h: nu for h, _, nu in check_branches(*channels)}
    result = np.zeros_like(tensor)
    for herald in range(3):
        _, bit = node_gates(mus[root], branches.get(herald, (1, 0, 0)))
        mask = np.eye(3)[herald]
        part = local_gate(tensor, np.diag(mask), (leaves[0],))
        result += local_gate(part, bit, (root, leaves[1]))
    F = np.array([[OMEGA**(i*j) for j in range(3)] for i in range(3)])/sqrt(3)
    return local_gate(result, F.conj().T, (root,)).reshape(27, 27)


class ResidualDecoder(Decoder):
    def __init__(self, code, mus, *, mode="bpqm"):
        self.spectra = tuple(map(spectrum, mus))
        if len(self.spectra) != code["length"] or mode not in ("bpqm", "product", "none"):
            raise ValueError("explicit residual decoder and local spectra required")
        super().__init__(code, PHYSICAL, mode="product" if mode == "product" else "none")
        # Fail closed if a homogeneous-source helper is mistakenly used on this object.
        self.mu = None
        if mode == "bpqm":
            check = next((row for row in code["H"] if len(row) == 3 and all(row)), None)
            if check is None:
                raise ValueError("bounded residual BPQM requires three-wire single check")
            self.transforms = [(root, heterogeneous_root(self.spectra, check, root))
                               for root in code["information_coordinates"]]
        self.mode = mode


def source_arrays(code, mus):
    words = tuple(product(range(3), repeat=code["length"]))
    labels = tuple(product(range(3), repeat=code["dimension"]))
    rows = code["basis_G"]
    codewords = tuple(tuple(sum(u*g[j] for u, g in zip(label, rows)) % 3 for j in range(code["length"])) for label in labels)
    phi = np.array([sqrt(float(prod(mu[a] for mu, a in zip(mus, word)))) for word in words])
    states = np.array([phi*np.array([OMEGA**sum(a*b for a, b in zip(d, word)) for word in words]) for d in codewords])
    return words, labels, phi, states, codewords


def prepare(code, mus, offsets):
    """Known local rotations, Fourier labels and public bilinear phase gates."""
    m, k = code["length"], code["dimension"]
    if m+2*k > 9:
        raise ValueError("UNKNOWN: bounded preparation reference cap")
    offsets = canonical_word(offsets, m)
    mus = tuple(map(spectrum, mus))
    if len(mus) != m:
        raise ValueError("one local spectrum per wire required")
    tensor = np.zeros((3,)*(m+2*k), complex)
    tensor[(0,)*(m+2*k)] = 1
    F = np.array([[OMEGA**(i*j) for j in range(3)] for i in range(3)])/sqrt(3)
    for j, mu in enumerate(mus):
        v = np.sqrt(list(map(float, mu)))-np.array([1., 0., 0.])
        denominator = float(v@v)
        rotation = np.eye(3) if not denominator else np.eye(3)-2*np.outer(v, v)/denominator
        tensor = local_gate(tensor, rotation, (2*k+j,))
    for i, row in enumerate(code["basis_G"]):
        tensor = local_gate(tensor, F, (i,))
        shift = sum(a*b for a, b in zip(row, offsets)) % 3
        tensor = local_gate(tensor, np.diag([OMEGA**(-u*shift) for u in range(3)]), (i,))
        for j, coefficient in enumerate(row):
            if coefficient:
                gate = np.diag([OMEGA**(coefficient*u*y) for u, y in product(range(3), repeat=2)])
                tensor = local_gate(tensor, gate, (i, 2*k+j))
    return tensor.reshape(3**k, 3**k, 3**m)


def residual_circuit(code, decoder, offsets, *, wrong_adjoint=False):
    words, labels, phi, states, codewords = source_arrays(code, decoder.spectra)
    actual = prepare(code, decoder.spectra, offsets)
    formula = np.zeros_like(actual)
    for u, d in enumerate(codewords):
        formula[u, 0] = states[u]*OMEGA**(-sum(a*b for a, b in zip(d, offsets)))/sqrt(len(labels))
    prep_error = float(np.max(abs(actual-formula)))
    actual = decoder.apply(actual)
    actual = subtract_label(actual, labels)
    actual = decoder.apply(actual, inverse=not wrong_adjoint)
    ideal = np.zeros_like(actual)
    for j, word in enumerate(words):
        if all(sum(a*(y-t) for a, y, t in zip(row, word, offsets)) % 3 == 0 for row in code["basis_G"]):
            ideal[0, 0, j] = sqrt(len(labels))*phi[j]
    return actual, ideal, prep_error


def audit(t, *, mode="bpqm", wrong_adjoint=False):
    """All residual offsets in one fixed local-syndrome fiber; no rerolls."""
    canonical_word((t,), 1)
    H = ((1, 1, 1, 1),)
    initial = PairConditioning.build(H, (PHYSICAL,)*4, (t, 0, 0, 0), ((0, 1),))
    code = matrix_data(initial.H)
    decoder = ResidualDecoder(code, initial.spectra, mode=mode)
    words, labels, _, states, _ = source_arrays(code, initial.spectra)
    batch = np.zeros((len(labels), len(labels), len(words)), complex)
    batch[:, 0] = states
    decoded = decoder.apply(batch)
    delta = float(np.mean([1-np.vdot(decoded[u, u], decoded[u, u]).real for u in range(len(labels))]))
    results = []
    for residual in product(range(3), repeat=3):
        J = (residual[0], (residual[0]-t) % 3, residual[1], residual[2])
        conditioned = PairConditioning.build(H, (PHYSICAL,)*4, J, ((0, 1),))
        if conditioned.spectra != initial.spectra:
            raise ArithmeticError("source illegally depends on residual offset")
        actual, ideal, prep_error = residual_circuit(code, decoder, residual, wrong_adjoint=wrong_adjoint)
        expanded = conditioned.expand_state(actual)
        data_probabilities = np.sum(abs(expanded)**2, axis=(0, 1))
        original_code = {"H": H, "length": 4, "gauge_dimension": 0}
        output, target, partition = native_distribution(original_code, PHYSICAL, J, data_probabilities)
        classical = np.zeros(3**4)
        phi = source_arrays(code, initial.spectra)[2]
        for word, probability in zip(words, phi**2):
            classical[index(conditioned.expand(word))] += probability
        classical_output, _, _ = native_distribution(original_code, PHYSICAL, J, classical)
        acceptance = float(sum(classical_output[:-1]))
        conditional_TV = float(np.sum(abs(classical_output[:-1]/acceptance-target[:-1]))/2) if acceptance else None
        results.append({"original_J": J, "target_empty": not bool(partition),
                        "TV_including_ABSTAIN": float(np.sum(abs(output-target))/2),
                        "comparison_distance_squared": float(np.sum(abs(actual-ideal)**2)),
                        "source_preparation_residual": prep_error,
                        "actual_norm_squared": float(np.sum(abs(actual)**2)),
                        "classical_single_proposal_acceptance": acceptance,
                        "classical_conditional_TV_when_nonempty": conditional_TV,
                        "classical_native_output_including_ABSTAIN": classical_output.tolist(),
                        "actual_native_output_including_ABSTAIN": output.tolist(),
                        "target_native_output_including_ABSTAIN": target.tolist()})
    distance = float(np.mean([c["comparison_distance_squared"] for c in results]))
    return {"local_difference": t, "mode": mode, "wrong_adjoint_COUNTERCONTROL": wrong_adjoint,
            "local_mass": str(initial.local_masses[0]), "conditioned_spectra": [[str(x) for x in mu] for mu in initial.spectra],
            "residual_word_error": delta, "conditional_Parseval_residual": abs(distance-2*delta),
            "conditional_average_TV": float(np.mean([c["TV_including_ABSTAIN"] for c in results])),
            "conditional_TV_bound": min(1., 2*sqrt(2*max(0., delta))),
            "matched_classical_mean_acceptance": float(np.mean([c["classical_single_proposal_acceptance"] for c in results])),
            "classical_mean_acceptance_theory": str(Fraction(1, 3**code["dimension"])), "cases": results,
            "decoder_built_once_per_local_difference_NOT_per_residual_offset": True,
            "full_original_word_decoding_required": False, "rare_event_postselection_used": False,
            "source_rotations_are_bounded_known_probabilities_NOT_a_coset_oracle": True}


def adaptive_countercontrol():
    """A residual-offset adaptive decoder invalidates the Parseval step."""
    code = matrix_data(((1, 1, 1),))
    decoders = {mode: ResidualDecoder(code, (PHYSICAL,)*3, mode=mode) for mode in ("bpqm", "none")}
    _, labels, _, states, _ = source_arrays(code, (PHYSICAL,)*3)
    batch = np.zeros((9, 9, 27), complex)
    batch[:, 0] = states
    errors = {}
    for mode, decoder in decoders.items():
        result = decoder.apply(batch)
        errors[mode] = float(np.mean([1-np.vdot(result[u, u], result[u, u]).real for u in range(9)]))
    residuals = []
    for J in product(range(3), repeat=3):
        mode = "bpqm" if len(set(J)) == 1 else "none"
        actual, ideal, _ = residual_circuit(code, decoders[mode], J)
        residuals.append(float(np.sum(abs(actual-ideal)**2))-2*errors[mode])
    return {"selection_rule": "BPQM if all three remaining offsets agree, otherwise identity decoder",
            "average_Parseval_identity_failure": abs(float(np.mean(residuals))),
            "this_rule_is_OUTSIDE_the_fixed_local_syndrome_decoder_contract": True}


def native_inventory():
    records = []
    for problem in saved_cases():
        groups = {}
        for i, column in enumerate(problem["forms"]):
            if any(column):
                groups.setdefault(tuple(column), []).append(i)
        pairs = tuple((group[i], group[i+1]) for group in groups.values() for i in range(0, len(group)-1, 2))
        H = tuple(zip(*problem["forms"]))
        conditioned = PairConditioning.build(H, (PHYSICAL,)*len(problem["forms"]), problem["offsets"], pairs)
        rank = int(nmod_mat(H, 3).rank())
        records.append({"original_problem": problem, "disjoint_duplicate_pairs": pairs,
                        "local_differences": conditioned.differences, "local_masses": list(map(str, conditioned.local_masses)),
                        "original_decoding_dimension": len(problem["forms"])-rank,
                        "residual_decoding_dimension": len(conditioned.kept)-rank,
                        "local_support_empty": conditioned.spectra is None,
                        "local_amplitudes_computed": 3*len(pairs),
                        "generic_residual_decoder_supplied": False,
                        "quantum_receiver_executed_on_native_input": False})
    return records


def run_controls():
    dependencies = [Path(__file__), SAVED_SOURCE, ROOT/"theorems/ternary_classical_sampling.py",
                    ROOT/"theorems/ternary_coloring_bpqm.py", ROOT/"theorems/ternary_decoded_sampler.py"]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}
    controls = [audit(t, mode=mode) for mode in ("bpqm", "product", "none") for t in range(3)]
    controls.append(audit(0, wrong_adjoint=True))
    adaptive, native = adaptive_countercontrol(), native_inventory()
    bpqm = [c for c in controls if c["mode"] == "bpqm" and not c["wrong_adjoint_COUNTERCONTROL"]]
    syndrome_law = {"actual_uniform_input_difference_probabilities": ["1/3"]*3,
                    "Born_herald_probabilities_NOT_the_input_law": ["1/2", "1/4", "1/4"],
                    "correct_mean_word_error": sum(c["residual_word_error"] for c in bpqm)/3,
                    "incorrect_Born_weighted_mean_word_error": sum(float(Fraction(c["local_mass"]))*c["residual_word_error"] for c in bpqm)}
    if hashes != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}:
        raise RuntimeError("source changed during live conditional-source audit")
    return {"schema_version": 1, "status": "LOCAL_CONDITIONING_QUOTIENT_SAMPLER_CONSTRUCTION_REVIEW_PENDING",
            "source_sha256": hashes, "controls": controls, "residual_adaptivity_countercontrol": adaptive,
            "unchanged_native_inventory": native, "input_syndrome_vs_measurement_law": syndrome_law,
            "generic_efficient_residual_decoder_supplied": False, "quantum_advantage_claimed": False,
            "local_derivation_independently_reviewed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    for c in report["controls"]:
        print(json.dumps({k: c[k] for k in ("mode", "local_difference", "wrong_adjoint_COUNTERCONTROL", "conditional_Parseval_residual", "conditional_average_TV")}))
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
