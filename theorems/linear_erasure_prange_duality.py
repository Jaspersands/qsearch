"""Positive affine-subspace instruments and matched affine Gibbs samplers.

Includes a constructive partial decoder for four-message even-parity blocks,
an exact optimality witness within this instrument cone, and falsifiers of
overbroad dequantization claims. No global quantum Gibbs algorithm is supplied.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import random

from flint import fmpq
import numpy as np

from parity_block_usd_prange import affine_system, overlap, uniform_affine_solution
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_certified_noise_sampler import rational

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/LINEAR_ERASURE_PRANGE_DUALITY.md"
REPORT = ROOT/"research/classical_baselines/linear_erasure_prange_duality.json"


def span(basis):
    values = {0}
    for b in basis:
        values |= {x^b for x in tuple(values)}
    return tuple(sorted(values))


def null_basis(basis, width):
    system = affine_system(tuple((b, 0) for b in basis), width)
    out = []
    for free in system["free"]:
        x = 1 << free
        for row in system["rref"]:
            if any(row[:-1]):
                pivot = next(j for j, a in enumerate(row[:-1]) if a)
                x |= row[free] << pivot
        out.append(x)
    return tuple(out)


@dataclass(frozen=True)
class AffineBranch:
    width: int
    basis: tuple[int, ...]
    weight: fmpq
    offset: int = 0

    def __post_init__(self):
        integer(self.width, "positive local binary width", 1)
        if type(self.basis) is not tuple:
            raise ValueError("explicit immutable subspace basis required")
        if any(type(x) is not int or not 0 < x < 2**self.width for x in self.basis):
            raise ValueError("nonzero binary subspace vectors required")
        if type(self.offset) is not int or not 0 <= self.offset < 2**self.width:
            raise ValueError("binary affine offset required")
        if affine_system(tuple((b, 0) for b in self.basis), self.width)["rank"] != len(self.basis):
            raise ValueError("subspace basis must be independent")
        w = rational(self.weight, "nonnegative exact branch weight")
        if not 0 <= w <= 1:
            raise ValueError("branch weight must be in[0,1]")
        object.__setattr__(self, "weight", w)

    @property
    def dimension(self):
        return len(self.basis)

    @property
    def annihilator(self):
        return null_basis(self.basis, self.width)

    def contains(self, x):
        return all(((x^self.offset)&v).bit_count() % 2 == 0 for v in self.annihilator)


def validate_mixture(branches):
    branches = tuple(branches)
    if not branches or any(not isinstance(b, AffineBranch) for b in branches):
        raise ValueError("explicit affine branches required")
    k = branches[0].width
    if any(b.width != k for b in branches) or sum(b.weight for b in branches) != 1:
        raise ValueError("common width and exact normalized mixture required")
    # Positivity must be certified without enumerating a growing local group.
    # Small calibration channels can instead supply an exact support cover.
    if not any(b.dimension == k and b.weight > 0 for b in branches):
        if k > 3 or any(not any(b.weight > 0 and b.contains(y) for b in branches) for y in range(2**k)):
            raise ValueError("positive full-space branch or bounded exact support cover required")
    return branches


def frequency_probability(branches, y):
    branches = validate_mixture(branches)
    integer(y, "frequency", 0)
    if y >= 2**branches[0].width:
        raise ValueError("frequency outside local group")
    return sum(b.weight/(2**b.dimension) for b in branches if b.contains(y))


def four_message_mixture(value):
    c, k = overlap(value), 3
    p = c*c
    return validate_mixture((AffineBranch(k, (1, 2, 4), (1-p)**2),
                             *(AffineBranch(k, (v,), p*(1-p)/2) for v in (1, 2, 4, 7)),
                             AffineBranch(k, (), p*p)))


def mixture_record(branches):
    branches = validate_mixture(branches)
    k = branches[0].width
    if k > 3:
        raise ValueError("full local certificate enumeration capped at width3")
    return {"width": k, "branches": [{"basis": b.basis, "offset": b.offset, "annihilator_basis": b.annihilator,
                                       "dimension": b.dimension, "weight": str(b.weight),
                                       "unknown_quantum_bits": k-b.dimension,
                                       "classical_affine_constraints": k-b.dimension} for b in branches],
            "frequency_probabilities": [str(frequency_probability(branches, y)) for y in range(2**k)],
            "mean_unknown_bits": str(sum(b.weight*(k-b.dimension) for b in branches)),
            "branch_codeword_phase": "(-1)^(d dot offset), retained until recovery permits correction",
            "codeword_branch_law_is_universal_coherent_prior_law": False,
            "universal_quantum_dequantization_claimed": False}


def branch_isometry(branches):
    branches = validate_mixture(branches)
    k, N = branches[0].width, 2**branches[0].width
    if k > 3:
        raise ValueError("constant-size instrument conformance capped at width3")
    T = np.zeros((N*len(branches), N))
    for index, branch in enumerate(branches):
        r, size = branch.dimension, 2**branch.dimension
        for t in range(size):
            x = branch.offset
            for j, b in enumerate(branch.basis):
                if (t >> j)&1:
                    x ^= b
            amplitude = math.sqrt(float(branch.weight/(size*frequency_probability(branches, x))))/math.sqrt(size)
            for out in range(size):
                T[index*N+out, x] = (-1)**((t&out).bit_count())*amplitude
    return T


def four_message_control(value):
    c, branches = overlap(value), four_message_mixture(value)
    p0, p1 = (1+c)/2, (1-c)/2
    P, R, rows = np.zeros((16, 16)), np.zeros((16, 16)), []
    for x in range(16):
        t = x >> 3
        v = (x&7) ^ (7 if t else 0)
        P[2*v+t, x] = 1
    for v in range(8):
        w = v.bit_count()
        mass = (p0**(4-w)*p1**w, p0**w*p1**(4-w))
        q = sum(mass)
        if q != frequency_probability(branches, v):
            raise ArithmeticError("four-message source does not equal branch mixture")
        a, b = math.sqrt(float(mass[0]/q)), math.sqrt(float(mass[1]/q))
        R[2*v:2*v+2, 2*v:2*v+2] = ((a, b), (-b, a))
        rows.append({"quotient": v, "conditional_masses": tuple(map(str, mass)), "quotient_mass": str(q)})
    compression = R@P
    T = branch_isometry(branches)
    U = np.kron(T, np.eye(2))@compression
    inputs, errors = [], []
    for d in range(8):
        cw = d | ((d.bit_count() % 2) << 3)
        message = np.array([(-1)**((cw&x).bit_count())*math.sqrt(float(p0**(4-x.bit_count())*p1**x.bit_count())) for x in range(16)])
        inputs.append(message)
        expected = np.zeros(U.shape[0])
        for j, branch in enumerate(branches):
            decoded = sum(((d&b).bit_count() % 2) << i for i, b in enumerate(branch.basis))
            expected[2*(j*8+decoded)] = math.sqrt(float(branch.weight))
        errors.append(float(np.linalg.norm(U@message-expected)))
    prior = sum(inputs)/np.linalg.norm(sum(inputs))
    out = U@prior
    prior_law = [float(np.sum(abs(out[16*j:16*(j+1)])**2)) for j in range(len(branches))]
    q0 = frequency_probability(branches, 0)
    prior_exact = [str(b.weight/(2**b.dimension*q0)) for b in branches]
    grams = []
    for d, e in product(range(8), repeat=2):
        z = d^e
        cw = z | ((z.bit_count() % 2) << 3)
        source = c**cw.bit_count()
        target = sum(b.weight for b in branches if all((z&v).bit_count() % 2 == 0 for v in b.basis))
        if source != target:
            raise ArithmeticError("input/output Gram identity failed")
        grams.append(str(source))
    return {"overlap": str(c), "mixture": mixture_record(branches), "compression": rows,
            "exact_input_output_Gram_entries": grams,
            "constant_local_input_dimension": 16, "constant_local_output_dimension": U.shape[0],
            "isometry_error_diagnostic": float(np.linalg.norm(U.T@U-np.eye(16))),
            "eight_codeword_output_errors_diagnostic": errors,
            "normalized_equal_superposition_branch_probabilities": prior_exact,
            "coherent_prior_branch_probabilities_diagnostic": prior_law,
            "mean_unknown_bits": str(4*c*c-c**4),
            "product_USD_parity_mean_unknown_bits": str(6*c*c-4*c**3+c**4),
            "full_block_USD_only_mean_unknown_bits": str(6*c*c-3*c**4),
            "global_coherent_Gibbs_sampler_implemented": False,
            "hardware_synthesis_implemented": False}


def all_local_spaces(width):
    integer(width, "bounded certificate width", 1)
    if width > 3:
        raise ValueError("complete dual certificate enumeration capped at width3")
    spaces = {(0,)}
    for size in range(1, width+1):
        for basis in combinations(range(1, 2**width), size):
            S = span(basis)
            if len(S) == 2**size:
                spaces.add(S)
    return tuple(sorted(spaces, key=lambda S: (len(S), S)))


def all_affine_spaces(width):
    spaces = {tuple(sorted(x^a for x in S)) for S in all_local_spaces(width) for a in range(2**width)}
    return tuple(sorted(spaces, key=lambda S: (len(S), S)))


def four_message_optimality(value):
    branches = four_message_mixture(value)
    dual = tuple(fmpq(3) if y == 0 else fmpq(1) if y.bit_count() % 2 else fmpq(-7, 3) for y in range(8))
    spaces = []
    for S in all_affine_spaces(3):
        cost = 3-(len(S).bit_length()-1)
        avg = sum(dual[y] for y in S)/len(S)
        if avg > cost:
            raise ArithmeticError("invalid exact affine-subspace dual bound")
        spaces.append({"members": S, "unknown_bits": cost, "dual_average": str(avg)})
    objective = sum(frequency_probability(branches, y)*dual[y] for y in range(8))
    actual = sum(b.weight*(3-b.dimension) for b in branches)
    if objective != actual:
        raise ArithmeticError("primal and dual instrument objectives disagree")
    return {"exact_dual_coefficients": tuple(map(str, dual)), "all_affine_subspaces": spaces,
            "primal_mean_unknown_bits": str(actual), "dual_lower_bound": str(objective),
            "optimal_within_positive_affine_subspace_instruments": True,
            "optimal_among_all_quantum_measurements": False}


@dataclass(frozen=True)
class AffineFactorInstance:
    outer_bits: int
    labels: tuple[tuple[int, ...], ...]
    signs: tuple[int, ...]

    def __post_init__(self):
        integer(self.outer_bits, "positive outer dimension", 1)
        if not self.labels or len(self.labels) != len(self.signs):
            raise ValueError("matching nonempty affine factor maps required")
        k = len(self.labels[0])
        if k < 1 or any(len(row) != k or any(type(a) is not int or not 0 <= a < 2**self.outer_bits for a in row) for row in self.labels):
            raise ValueError("common binary local width and public labels required")
        if any(type(b) is not int or not 0 <= b < 2**k for b in self.signs):
            raise ValueError("binary affine sign masks required")

    def frequency(self, x, i):
        return self.signs[i] ^ sum(((x&a).bit_count() % 2) << j for j, a in enumerate(self.labels[i]))

    def equations(self, branches, selected):
        branches = validate_mixture(branches)
        if len(selected) != len(self.labels) or branches[0].width != len(self.labels[0]):
            raise ValueError("one actual mixture branch per local factor required")
        if any(type(s) is not int or not 0 <= s < len(branches) for s in selected):
            raise ValueError("actual mixture branch index required")
        rows = []
        for a, b, s in zip(self.labels, self.signs, selected):
            for u in branches[s].annihilator:
                coeff = 0
                for j, label in enumerate(a):
                    if (u >> j)&1:
                        coeff ^= label
                rows.append((coeff, (u&(b^branches[s].offset)).bit_count() % 2))
        return tuple(rows)


def sample_affine_mixture(instance, branches, rng):
    branches = validate_mixture(branches)
    denominator = math.lcm(*(int(b.weight.denominator) for b in branches))
    counts = [int(b.weight*denominator) for b in branches]
    selected = []
    for _ in instance.labels:
        u = rng.randrange(denominator)
        for s, count in enumerate(counts):
            u -= count
            if u < 0:
                selected.append(s)
                break
    rows = instance.equations(branches, selected)
    system = affine_system(rows, instance.outer_bits)
    good = system["consistent"] and system["rank"] == len(rows)
    return {"branches": selected, "constraints": len(rows), "rank": system["rank"],
            "success": good, "outer": uniform_affine_solution(system, instance.outer_bits, rng) if good else 0,
            "fallback_mass_is_charged": True}


def rank_duality_control(instance, branches, selected):
    branches = validate_mixture(branches)
    rows = instance.equations(branches, selected)
    columns = []
    for labels, s in zip(instance.labels, selected):
        for u in branches[s].annihilator:
            # Construct the quantum column coordinate-by-coordinate from the
            # dual code, independently of the classical XOR equation builder.
            col = sum((sum(((a >> r)&1)*((u >> j)&1) for j, a in enumerate(labels)) % 2) << r for r in range(instance.outer_bits))
            columns.append(col)
    if tuple(columns) != tuple(a for a, _ in rows):
        raise ArithmeticError("quantum reconstruction and classical equation matrices are not transposes")
    rk = affine_system(tuple((col, 0) for col in columns), instance.outer_bits)["rank"]
    return {"outer_bits": instance.outer_bits, "labels": instance.labels, "signs": instance.signs,
            "selected_branches": tuple(selected), "quantum_reconstruction_columns": tuple(columns),
            "classical_equation_rows": rows, "rank": rk, "unknown_bits": len(columns),
            "quantum_unique_reconstruction_iff_classical_full_row_rank": True,
            "arbitrary_coherent_prior_success_from_rank_alone": False}


def complete_factor_control(instance, branches):
    branches = validate_mixture(branches)
    h, B, N = instance.outer_bits, len(instance.labels), len(branches)
    if h > 10 or N**B > 4096:
        return {"status": "UNKNOWN_FULL_LAW_CAP", "partial_law_promoted": False}
    proposal, records, tilts, bad, Zt = [fmpq(0)]*2**h, [], [], fmpq(0), fmpq(0)
    for selected in product(range(N), repeat=B):
        rows = instance.equations(branches, selected)
        system = affine_system(rows, h)
        solutions = tuple(x for x in range(2**h) if all((x&a).bit_count() % 2 == b for a, b in rows))
        weight = math.prod(branches[s].weight for s in selected)
        tilt = fmpq(len(solutions)*2**len(rows), 2**h)
        good = system["consistent"] and system["rank"] == len(rows)
        records.append({"branches": selected, "constraints": len(rows), "rank": system["rank"],
                        "solutions": solutions, "proposal_mass": str(weight), "tilt": str(tilt), "good": good})
        tilts.append(weight*tilt)
        Zt += weight*tilt
        if not good:
            proposal[0] += weight
            bad += weight
        else:
            for x in solutions:
                proposal[x] += weight/len(solutions)
    k = branches[0].width
    exact = [math.prod(2**k*frequency_probability(branches, instance.frequency(x, i)) for i in range(B)) for x in range(2**h)]
    normalization = sum(exact)
    exact = [v/normalization for v in exact]
    subsetTV = sum(abs(fmpq(r["proposal_mass"])-t/Zt) for r, t in zip(records, tilts))/2
    tv = sum(abs(a-b) for a, b in zip(proposal, exact))/2
    if sum(proposal) != 1 or tv > subsetTV+bad or normalization/2**h != Zt:
        raise ArithmeticError("matched mixture normalization or fallback accounting failed")
    return {"outer_bits": h, "labels": instance.labels, "signs": instance.signs,
            "branches": records, "bad_mass": str(bad), "tilted_normalization": str(Zt),
            "subset_TV": str(subsetTV), "complete_output_TV": str(tv),
            "Gibbs_probabilities": tuple(map(str, exact)), "sampler_probabilities": tuple(map(str, proposal)),
            "fixed_sign_bound_inferred_from_sign_average": False}


def scaling_bound(blocks, outer_bits, value, tilt="9/8"):
    integer(blocks, "positive block count", 1)
    integer(outer_bits, "positive outer count", 1)
    branches = four_message_mixture(value)
    t = rational(tilt, "exact Chernoff tilt")
    if t <= 1:
        raise ValueError("Chernoff tilt greater than1 required")
    cutoff = max(0, min(3*blocks, outer_bits-((blocks-1).bit_length()+8)))
    pgf = sum(b.weight*t**(3-b.dimension) for b in branches)
    tail = min(fmpq(1), pgf**blocks/t**(cutoff+1))
    rank = min(fmpq(1), fmpq(2**cutoff-1, 2**outer_bits))
    bad = min(fmpq(1), tail+rank)
    c = overlap(value)
    return {"blocks": blocks, "outer_bits": outer_bits, "overlap": str(c), "cutoff": cutoff,
            "Chernoff_tilt": str(t), "constraint_count_pgf_at_tilt": str(pgf),
            "constraint_tail_upper": str(tail), "rank_failure_union_upper": str(rank),
            "mean_classical_Gibbs_TV_upper": str(min(fmpq(1), 3*bad)),
            "matched_quantum_unknown_and_classical_constraint_load": str(4*c*c-c**4),
            "product_USD_parity_load": str(6*c*c-4*c**3+c**4),
            "threshold_above_joint_below_product": 4*c*c-c**4 < fmpq(outer_bits, blocks) < 6*c*c-4*c**3+c**4,
            "quantum_full_coherent_prior_success_proved": False,
            "random_sign_average_not_arbitrary_sign_guarantee": True}


def outside_linear_cone_control():
    q = tuple(map(fmpq, ("1/10", "3/10", "3/10", "3/10")))
    branches = validate_mixture((AffineBranch(2, (1, 2), "2/5"),
                                 AffineBranch(2, (3,), "1/5", 1),
                                 AffineBranch(2, (2,), "1/5", 1),
                                 AffineBranch(2, (1,), "1/5", 2)))
    if tuple(frequency_probability(branches, y) for y in range(4)) != q:
        raise ArithmeticError("signed-overlap channel has no matched affine decomposition")
    T, errors, grams = branch_isometry(branches), [], []
    for d in range(4):
        message = np.array([math.sqrt(float(q[y]))*(-1)**((d&y).bit_count()) for y in range(4)])
        expected = np.zeros(16)
        for i, b in enumerate(branches):
            decoded = sum(((d&v).bit_count() % 2) << j for j, v in enumerate(b.basis))
            expected[4*i+decoded] = (-1)**((d&b.offset).bit_count())*math.sqrt(float(b.weight))
        errors.append(float(np.linalg.norm(T@message-expected)))
    for d, e in product(range(4), repeat=2):
        z = d^e
        source = sum(q[y]*(-1)**((z&y).bit_count()) for y in range(4))
        target = sum(b.weight*(-1)**((z&b.offset).bit_count()) for b in branches if all((z&v).bit_count() % 2 == 0 for v in b.basis))
        if source != target:
            raise ArithmeticError("affine branch phase omitted from exact Gram")
        grams.append(str(target))
    dual = tuple(map(fmpq, ("-3", "1", "1", "1")))
    spaces = [{"members": S, "unknown_bits": 2-(len(S).bit_length()-1),
               "dual_average": str(sum(dual[y] for y in S)/len(S))} for S in all_affine_spaces(2)]
    load = sum(b.weight*(2-b.dimension) for b in branches)
    if any(fmpq(s["dual_average"]) > s["unknown_bits"] for s in spaces) or sum(q[y]*dual[y] for y in range(4)) != load:
        raise ArithmeticError("signed-overlap affine instrument optimality failed")
    instance = AffineFactorInstance(4, ((1, 2), (4, 8)), (1, 2))
    census = [complete_factor_control(AffineFactorInstance(2, ((1, 2), (2, 3)), signs), branches) for signs in product(range(4), repeat=2)]
    bad = fmpq(census[0]["bad_mass"])
    mean = sum(fmpq(c["complete_output_TV"]) for c in census)/16
    if mean > 3*bad:
        raise ArithmeticError("signed-overlap averaged affine sampler bound failed")
    return {"width": 2, "positive_frequency_probabilities": tuple(map(str, q)),
            "violated_necessary_condition": "q(0)>=q(y) for every y",
            "witness_frequency": 1, "witness_difference_q0_minus_qy": str(q[0]-q[1]),
            "negative_nonzero_Walsh_coefficients": tuple(str(sum(q[y]*(-1)**((d&y).bit_count()) for y in range(4))) for d in range(1, 4)),
            "linear_origin_subspace_mixture_excluded": True,
            "affine_coset_mixture_excluded": False, "classical_hardness_established": False,
            "matched_affine_instrument": mixture_record(branches),
            "exact_input_output_Gram_entries": grams,
            "codeword_output_errors_diagnostic": errors,
            "isometry_error_diagnostic": float(np.linalg.norm(T.T@T-np.eye(4))),
            "optimal_affine_mean_unknown_bits": str(load),
            "exact_dual_coefficients": tuple(map(str, dual)), "all_affine_subspaces": spaces,
            "complete_matched_classical_control": complete_factor_control(instance, branches),
            "complete_sign_census": {"outer_bits": 2, "labels": ((1, 2), (2, 3)), "cases": census,
                                     "mean_output_TV": str(mean), "mean_output_TV_upper": str(min(fmpq(1), 3*bad))},
            "rank_duality_controls": [rank_duality_control(instance, branches, selected) for selected in product(range(4), repeat=2)],
            "affine_branch_phases_discarded": False,
            "efficient_quantum_sampler_established": False}


def build_report():
    branches = four_message_mixture("1/2")
    censuses = []
    for h, labels in ((2, ((1, 2, 3), (2, 3, 1))), (4, ((1, 2, 4), (2, 4, 8)))):
        cases = [complete_factor_control(AffineFactorInstance(h, labels, signs), branches) for signs in product(range(8), repeat=2)]
        bad = fmpq(cases[0]["bad_mass"])
        mean = sum(fmpq(c["complete_output_TV"]) for c in cases)/64
        if mean > 3*bad:
            raise ArithmeticError("random-sign averaged dual sampler guarantee failed")
        censuses.append({"outer_bits": h, "labels": labels, "complete_sign_cases": cases,
                         "mean_output_TV": str(mean), "mean_output_TV_upper": str(min(fmpq(1), 3*bad))})
    rng = random.Random(133410)
    live = AffineFactorInstance(72, tuple(tuple(rng.randrange(2**72) for _ in range(3)) for _ in range(64)), tuple(rng.randrange(8) for _ in range(64)))
    return {"status": "POSITIVE_AFFINE_ERASURE_INSTRUMENT_DUALITY_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "four_message_quantum_controls": [four_message_control(c) for c in ("1/3", "1/2", "2/3")],
            "instrument_optimality_controls": [four_message_optimality(c) for c in ("1/3", "1/2", "2/3")],
            "complete_sign_censuses": censuses,
            "rank_duality_controls": [rank_duality_control(AffineFactorInstance(4, ((1, 2, 4), (2, 4, 8)), (1, 6)), branches, selected) for selected in product(range(6), repeat=2)],
            "scaling_controls": [scaling_bound(B, (21*B+19)//20, "1/2") for B in (64, 256, 1024, 4096)],
            "live_classical_instance": {"outer_bits": live.outer_bits, "labels": live.labels, "signs": live.signs},
            "live_classical_samples": [sample_affine_mixture(live, branches, rng) for _ in range(16)],
            "outside_linear_cone_control": outside_linear_cone_control(),
            "negative_scope": "positive affine-subspace erasure instruments have matched affine-mixture classical rank conditions, with branch phases retained",
            "universal_quantum_dequantization_claimed": False, "novelty_verified": False,
            "accepted_speedup_candidate": False, "native_hidden_shift_receiver_supplied": False}


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
                id="NEG-AFFINE-ERASURE-INSTRUMENT-MATCHED-CLASSICAL-DUAL",
                source=str(output_path),
                claim="Positive affine-subspace erasure instruments with retained branch phases evade matched classical constraint sampling.",
                reason_invalid="Every positive uniform-affine-subspace mixture supplies both a coherent quantum partial-linear-information instrument and a matched classical affine-constraint sampler where quantum reconstruction and classical equation matrices are exact transposes; mean unresolved loads are matched.",
                lesson="Affine branch phases and negative Gram entries outside the origin-linear cone do not create a quantum separation if the underlying mixture has an efficient low-load affine representation with matched classical equation rank conditions.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "local_partial_decoders": 4,
                    "exact_Gram_entries": 208,
                    "complete_signed_instances": 145,
                    "exact_dual_subspaces": 164,
                    "exact_rank_transposes": 52,
                    "four_message_optimal_load": "4*c^2 - c^4",
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
    print(json.dumps({"status": report["status"], "actual_local_partial_decoders": 4,
                      "complete_signed_instances": 145, "optimality_affine_subspaces_per_four_message_control": 51,
                      "live_classical_samples": 16,
                      "largest_mean_TV_upper_diagnostic": float(fmpq(report["scaling_controls"][-1]["mean_classical_Gibbs_TV_upper"])),
                      "quantum_advantage_established": False}, indent=2))


if __name__ == "__main__":
    main()
