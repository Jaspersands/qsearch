"""Constructive three-message USD and its matched block-Prange sampler.

A joint quantum decoder beats separate USD, but the matched Gibbs sampling
threshold has an explicit correlated classical counterpart. No speedup claim.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random

from flint import fmpq, nmod_mat
import numpy as np

from ternary_certified_noise_sampler import rational
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/PARITY_BLOCK_USD_PRANGE.md"
REPORT = ROOT/"research/classical_baselines/parity_block_usd_prange.json"


def overlap(value):
    c = rational(value, "known binary pure-state overlap")
    if not 0 < c < 1:
        raise ValueError("strict overlap in(0,1) required")
    return c


def local_recipe(value):
    c = overlap(value)
    p0, p1 = (1+c)/2, (1-c)/2
    rows = []
    for v in range(4):
        x, y = v >> 1, v & 1
        mass = tuple((p1 if x^t else p0)*(p1 if y^t else p0)*(p1 if t else p0) for t in (0, 1))
        q = sum(mass)
        success = (1-c*c)/(4*q)
        rows.append({"frequency_quotient": v, "mass": tuple(map(str, mass)), "total_mass": str(q),
                     "compression_cosine_squared": str(mass[0]/q),
                     "compression_sine_squared": str(mass[1]/q),
                     "filter_success_squared": str(success), "filter_failure_squared": str(1-success)})
    return {"overlap": str(c), "rows": rows, "joint_success": str(1-c*c),
            "joint_erasure": str(c*c), "product_USD_with_parity_success": str(1-3*c*c+2*c**3),
            "coherent_failure_state_is_codeword_independent": True,
            "per_block_quantum_register_bits": 4,
            "operations": ["xor frequency bit3 into bits1 and2", "four quotient-controlled real rotations on bit3",
                           "quotient-controlled herald rotation", "Hadamards on bits1 and2 conditioned on success"],
            "unknown_codeword_in_gate_parameters": False, "hardware_synthesis_implemented": False}


def local_unitary(value):
    """Execute the constant-size public gate program; not a large decoder table."""
    recipe = local_recipe(value)
    P = np.zeros((8, 8))
    for x in range(8):
        a, b, t = x >> 2, (x >> 1) & 1, x & 1
        P[((a^t)*2+(b^t))*2+t, x] = 1
    R = np.zeros((8, 8))
    for v, row in enumerate(recipe["rows"]):
        a, b = math.sqrt(float(fmpq(row["compression_cosine_squared"]))), math.sqrt(float(fmpq(row["compression_sine_squared"])))
        R[2*v:2*v+2, 2*v:2*v+2] = ((a, b), (-b, a))
    U = np.kron(R@P, np.eye(2))
    filter = np.zeros((16, 16))
    for v, row in enumerate(recipe["rows"]):
        a, b = math.sqrt(float(fmpq(row["filter_success_squared"]))), math.sqrt(float(fmpq(row["filter_failure_squared"])))
        for t in (0, 1):
            idx = 4*v+2*t
            filter[idx:idx+2, idx:idx+2] = ((a, -b), (b, a))
    H = np.array(((1, 1), (1, -1)))/math.sqrt(2)
    H2, final = np.kron(H, H), np.zeros((16, 16))
    for v, w, t, flag in product(range(4), range(4), range(2), range(2)):
        final[4*v+2*t+flag, 4*w+2*t+flag] = H2[v, w] if flag == 0 else int(v == w)
    return final@filter@U


def local_control(value):
    c, U = overlap(value), local_unitary(value)
    a, b = math.sqrt(float((1+c)/2)), math.sqrt(float((1-c)/2))
    errors, grams = [], []
    inputs = []
    for u, v in product(range(2), repeat=2):
        d = (u, v, u^v)
        message = np.array((1.,))
        for bit in d:
            message = np.kron(message, (a, (-1)**bit*b))
        inputs.append(message)
        output = U@np.kron(message, (1., 0.))
        expected = np.zeros(16)
        expected[4*(2*u+v)] = math.sqrt(float(1-c*c))
        expected[1] = float(c)
        errors.append(float(np.linalg.norm(output-expected)))
    for i, j in product(range(4), repeat=2):
        grams.append(str(fmpq(1) if i == j else c*c))
    coherent = sum(inputs)/np.linalg.norm(sum(inputs))
    output = U@np.kron(coherent, (1., 0.))
    failure = sum(float(abs(output[i])**2) for i in range(16) if i&1)
    return {"recipe": local_recipe(c), "input_and_output_Gram_entries": grams,
            "unitarity_error_diagnostic": float(np.linalg.norm(U.T@U-np.eye(16))),
            "coherent_four_codeword_errors_diagnostic": errors,
            "normalized_equal_superposition_erasure_probability": str(4*c*c/(1+3*c*c)),
            "equal_superposition_erasure_diagnostic": failure,
            "classical_codeword_erasure_law_applies_to_every_coherent_prior": False,
            "numerical_controls_are_theorem_certificates": False}


@dataclass(frozen=True)
class BlockXOR:
    outer_bits: int
    labels: tuple[tuple[int, int, int], ...]
    signs: tuple[tuple[int, int, int], ...]

    def __post_init__(self):
        integer(self.outer_bits, "positive outer spin count", 1)
        if not self.labels or len(self.labels) != len(self.signs):
            raise ValueError("nonempty matching clause blocks and signs required")
        for a, j in zip(self.labels, self.signs):
            if len(a) != 3 or len(j) != 3 or any(type(x) is not int or not 0 <= x < 2**self.outer_bits for x in a) or any(type(x) is not int or x not in (0, 1) for x in j):
                raise ValueError("three binary-labelled signed clauses per block required")

    def selected_equations(self, selected):
        selected = tuple(selected)
        if len(set(selected)) != len(selected) or any(type(i) is not int or not 0 <= i < len(self.labels) for i in selected):
            raise ValueError("distinct actual block indices required")
        return tuple((a[k]^a[2], j[k]^j[2]) for i in selected
                     for a, j in ((self.labels[i], self.signs[i]),) for k in (0, 1))


def affine_system(equations, width):
    """Exact GF2 RREF via FLINT; sample all free coordinates uniformly."""
    integer(width, "positive affine width", 1)
    equations = tuple(equations)
    if any(type(a) is not int or not 0 <= a < 2**width or type(b) is not int or b not in (0, 1) for a, b in equations):
        raise ValueError("binary affine equations required")
    if not equations:
        return {"rank": 0, "consistent": True, "rref": (), "pivots": (), "free": tuple(range(width))}
    matrix = nmod_mat([[(a >> j)&1 for j in range(width)]+[b] for a, b in equations], 2)
    rref, _ = matrix.rref()
    rows = tuple(tuple(map(int, r)) for r in rref.tolist())
    pivots = tuple(next(j for j, x in enumerate(row[:-1]) if x) for row in rows if any(row[:-1]))
    return {"rank": len(pivots), "consistent": not any(not any(row[:-1]) and row[-1] for row in rows),
            "rref": rows, "pivots": pivots, "free": tuple(j for j in range(width) if j not in pivots)}


def uniform_affine_solution(system, width, rng):
    if not system["consistent"]:
        raise ValueError("inconsistent affine system has no uniform sample")
    x = sum(rng.randrange(2) << j for j in system["free"])
    for row in system["rref"]:
        if any(row[:-1]):
            pivot = next(j for j, a in enumerate(row[:-1]) if a)
            value = row[-1] ^ (sum(a*((x >> j)&1) for j, a in enumerate(row[:-1])) & 1)
            x ^= value << pivot
    return x


def conditional_inner_probability(instance, x, block, c):
    c = overlap(c)
    a, j = instance.labels[block], instance.signs[block]
    f = tuple(1 if ((x&t).bit_count()+s) % 2 == 0 else -1 for t, s in zip(a, j))
    w0, w1 = math.prod(1+c*y for y in f), math.prod(1-c*y for y in f)
    return w0/(w0+w1)


def sample_block_prange(instance, value, rng):
    c = overlap(value)
    p = c*c
    selected = tuple(i for i in range(len(instance.labels)) if rng.randrange(int(p.denominator)) < p.numerator)
    equations = instance.selected_equations(selected)
    system = affine_system(equations, instance.outer_bits)
    good = system["consistent"] and system["rank"] == len(equations)
    if not good:
        return {"selected": selected, "rank": system["rank"], "success": False, "outer": 0, "inner": 0,
                "fallback_mass_is_charged": True}
    x = uniform_affine_solution(system, instance.outer_bits, rng)
    z = 0
    for i in range(len(instance.labels)):
        p0 = conditional_inner_probability(instance, x, i, c)
        if rng.randrange(int(p0.denominator)) >= p0.numerator:
            z |= 1 << i
    return {"selected": selected, "rank": system["rank"], "success": True, "outer": x, "inner": z,
            "fallback_mass_is_charged": True}


def sample_planted_zero(instance, value, rng):
    if any(any(bits) for bits in instance.signs):
        raise ValueError("zero-sign planted sampler is not a general signed sampler")
    c, z = overlap(value), 0
    for i in range(len(instance.labels)):
        p0 = conditional_inner_probability(instance, 0, i, c)
        if rng.randrange(int(p0.denominator)) >= p0.numerator:
            z |= 1 << i
    return {"outer": 0, "inner": z, "scope": "all-zero signs only, with conditional inner spins"}


def exact_control(instance, value):
    c = overlap(value)
    B, h, p = len(instance.labels), instance.outer_bits, c*c
    if h+B > 14 or B > 8:
        return {"status": "UNKNOWN_EXACT_DISTRIBUTION_CAP", "partial_law_promoted": False}
    proposal, exact = [fmpq(0)]*(2**(h+B)), []
    subset_records, bad, subset_tilt, normalization = [], fmpq(0), [], fmpq(0)
    for mask in range(2**B):
        selected = tuple(i for i in range(B) if (mask >> i)&1)
        system = affine_system(instance.selected_equations(selected), h)
        count = 2**(h-system["rank"]) if system["consistent"] else 0
        q = p**len(selected)*(1-p)**(B-len(selected))
        t = fmpq(count*2**(2*len(selected)), 2**h)
        good = system["consistent"] and system["rank"] == 2*len(selected)
        subset_records.append({"mask": mask, "rank": system["rank"], "consistent": system["consistent"],
                               "solution_count": count, "proposal_mass": str(q), "tilt": str(t), "good": good})
        subset_tilt.append(q*t)
        normalization += q*t
        if not good:
            bad += q
            proposal[0] += q
            continue
        solutions = [x for x in range(2**h) if all(((a&x).bit_count() % 2) == b for a, b in instance.selected_equations(selected))]
        for x in solutions:
            for z in range(2**B):
                probability = q/count
                for i in range(B):
                    p0 = conditional_inner_probability(instance, x, i, c)
                    probability *= 1-p0 if (z >> i)&1 else p0
                proposal[x+(z << h)] += probability
    for z, x in product(range(2**B), range(2**h)):
        w = fmpq(1)
        for i, (a, j) in enumerate(zip(instance.labels, instance.signs)):
            w *= math.prod(1+c*(1 if (((a[k]&x).bit_count()+j[k]+((z >> i)&1)) % 2 == 0) else -1) for k in range(3))
        exact.append(w)
    Z = sum(exact)
    exact = [w/Z for w in exact]
    subset_tv = sum(abs(fmpq(s["proposal_mass"])-tilt/normalization) for s, tilt in zip(subset_records, subset_tilt))/2
    tv = sum(abs(a-b) for a, b in zip(proposal, exact))/2
    if sum(proposal) != 1 or tv > subset_tv+bad:
        raise ArithmeticError("complete sampler law or finite transfer inequality failed")
    return {"status": "EXACT_FULL_GIBBS_AND_BLOCK_PRANGE_CONTROL", "outer_bits": h,
            "labels": instance.labels, "signs": instance.signs, "overlap": str(c),
            "subsets": subset_records, "bad_subset_mass": str(bad), "tilted_subset_normalization": str(normalization),
            "subset_TV": str(subset_tv), "complete_output_TV": str(tv),
            "Gibbs_probabilities": tuple(map(str, exact)), "sampler_probabilities": tuple(map(str, proposal)),
            "failures_conditioned_away": False, "bounded_exact_law_is_scalable_sampler": False}


def random_matrix_failure_bound(blocks, outer_bits, value):
    integer(blocks, "positive independent clause block count", 1)
    integer(outer_bits, "positive outer dimension", 1)
    c, p = overlap(value), overlap(value)**2
    cutoff = max(0, min(blocks, (outer_bits-((blocks-1).bit_length()+8))//2))
    term, tail = (1-p)**blocks, fmpq(0)
    for s in range(blocks+1):
        if s > cutoff:
            tail += term
        if s < blocks:
            term *= fmpq(blocks-s, s+1)*p/(1-p)
    rank = min(fmpq(1), fmpq(2**(2*cutoff)-1, 2**outer_bits))
    bad = min(fmpq(1), tail+rank)
    rho, joint, separate = fmpq(outer_bits, blocks), 2*p, 3*p-c**3
    planted = (1+3*p)**blocks/2**outer_bits
    zero_sampler = min(fmpq(1), 1/planted)
    prange_atom = min(fmpq(1), tail+rank+fmpq(2**(2*cutoff), 2**outer_bits))
    planted_bad = max(fmpq(0), 1-zero_sampler-prange_atom)
    return {"blocks": blocks, "outer_bits": outer_bits, "overlap": str(c), "cutoff": cutoff,
            "exact_binomial_tail": str(tail), "good_size_rank_failure_union_upper": str(rank),
            "mean_bad_subset_probability_upper": str(bad), "mean_classical_Gibbs_TV_upper": str(min(fmpq(1), 3*bad)),
            "outer_constraints_per_block": str(rho), "joint_quantum_erasure_load_per_block": str(joint),
            "matched_classical_block_constraint_load_per_block": str(joint),
            "independent_clause_Prange_load_per_block": str(separate),
            "naive_baseline_would_suggest_quantum_threshold_improvement": joint < rho < separate,
            "all_zero_sign_partition_tilt_lower": str(planted),
            "all_zero_sign_block_Prange_mean_TV_lower": str(planted_bad),
            "all_zero_sign_zero_outer_sampler_mean_TV_upper": str(zero_sampler),
            "fixed_sign_claim_inferred_from_random_sign_average": False,
            "failure_of_one_classical_sampler_proves_quantum_advantage": False,
            "matched_classical_threshold_same": True, "efficient_quantum_advantage_established": False}


def build_report():
    controls = []
    matrices = ((2, ((1, 2, 3), (1, 3, 2))), (3, ((1, 2, 4), (2, 3, 5))), (1, ((1, 1, 1), (0, 1, 1))))
    for h, labels in matrices:
        census = [exact_control(BlockXOR(h, labels, tuple(tuple(bits[3*i:3*i+3]) for i in range(2))), "1/2")
                  for bits in product(range(2), repeat=6)]
        mean_tv = sum(fmpq(r["complete_output_TV"]) for r in census)/64
        bad = fmpq(census[0]["bad_subset_mass"])
        if mean_tv > 3*bad:
            raise ArithmeticError("complete random-sign dequantization bound failed")
        controls.append({"outer_bits": h, "labels": labels, "random_sign_cases": census,
                         "mean_complete_output_TV": str(mean_tv), "bad_subset_probability": str(bad),
                         "mean_TV_upper": str(min(fmpq(1), 3*bad))})
    live = []
    rng = random.Random(133400)
    instance = BlockXOR(16, tuple(tuple(rng.randrange(2**16) for _ in range(3)) for _ in range(24)),
                        tuple(tuple(rng.randrange(2) for _ in range(3)) for _ in range(24)))
    for _ in range(32):
        live.append(sample_block_prange(instance, "1/2", rng))
    return {"status": "CONSTRUCTIVE_PARITY_BLOCK_USD_CLASSICALLY_MATCHED_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "local_quantum_controls": [local_control(c) for c in ("1/3", "1/2", "2/3")],
            "complete_sign_censuses": controls,
            "scaling_controls": [random_matrix_failure_bound(B, (11*B+19)//20, "1/2") for B in (32, 128, 512, 4096)],
            "live_classical_instance": {"outer_bits": instance.outer_bits, "labels": instance.labels, "signs": instance.signs},
            "live_classical_samples": live,
            "negative_result_scope": "joint three-message parity USD does not establish a Gibbs sampling speedup over correlated block-Prange on this family",
            "general_DQI_impossibility_claimed": False, "native_LWE_decoder_supplied": False,
            "accepted_speedup_candidate": False, "hardware_synthesis_implemented": False}


def write_report(
    output_path: Path = REPORT,
    write_registry: bool = True,
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_experiment_id: str = "EXP-CODE-SELF-DUAL-WREATH-COHERENT-COMPONENT-TRIM-HYBRID",
) -> dict:
    report = build_report()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    if write_registry:
        import sys
        core_dir = str(ROOT / "core")
        if core_dir not in sys.path:
            sys.path.insert(0, core_dir)
        from research_registry import NegativeResultRecord, upsert_negative_result
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-PARITY-BLOCK-USD-MATCHED-CLASSICAL-PRANGE",
                source=str(output_path),
                claim="Collective three-message parity block USD decoding establishes a quantum Gibbs sampling advantage over classical Prange methods.",
                reason_invalid="Eliminating the Hamiltonian block spin yields a correlated classical block-Prange sampler whose constraint load 2*c^2 exactly matches the joint quantum erasure load, matching the random-sign Gibbs sampling threshold.",
                lesson="Joint parity block decoding improves on independent product USD, but eliminating the inner spins reveals an exact classical correlated constraint sampler with the same threshold. Comparing only against independent-clause Prange creates a false quantum advantage signal.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "joint_quantum_erasure_load_per_block": "2*c^2",
                    "matched_classical_block_constraint_load_per_block": "2*c^2",
                    "independent_clause_prange_load_per_block": "3*c^2 - c^3",
                    "exact_sign_cases_replayed": 192,
                    "all_zero_planted_sign_alternative_sampler_supplied": True,
                },
            )
        )
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--no-registry", action="store_true")
    args = parser.parse_args()
    if args.write:
        report = write_report(write_registry=not args.no_registry)
    else:
        report = build_report()
    print(json.dumps({"status": report["status"], "actual_local_quantum_programs": 3,
                      "complete_sign_cases": 192, "live_classical_samples": 32,
                      "large_control_TV_upper_diagnostic": float(fmpq(report["scaling_controls"][-1]["mean_classical_Gibbs_TV_upper"])),
                      "quantum_advantage_established": False}, indent=2))


if __name__ == "__main__":
    main()
