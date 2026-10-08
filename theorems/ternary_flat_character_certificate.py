"""Exact finite-group flat certificate and conditional classical extraction.

LOCAL DERIVATION / REVIEW PENDING. Checks a supplied classical completion;
does not construct it from noisy native records or certify a quantum speedup.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path

from sympy import I, QQ, Symbol, cyclotomic_poly, exp, pi
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.exceptions import DMNonInvertibleMatrixError

from ternary_character_synchronization import _records
from ternary_cyclic_extractor import random_even_source
from ternary_covariant_noise import CovariantRecord, root_digits
from ternary_observable_moment_lift import difference_basis

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_FLAT_CHARACTER_CERTIFICATE.md"
REPORT = ROOT / "research/classical_baselines/ternary_flat_character_certificate.json"
NEGATIVE_SOURCE = ROOT / "research/classical_baselines/ternary_observable_moment_lift.json"


class _Reject(Exception):
    pass


class ResourceLimit(ValueError):
    pass


def compile_layout(records, base_frequencies=None, max_offsets=10000, max_nodes=1000, max_entries=1_000_000):
    records, n, q = _records(records)
    if any(type(x) is not int or x < 1 for x in (max_offsets, max_nodes, max_entries)):
        raise ValueError("positive whole-object caps required")
    basis = difference_basis(records)
    if basis["rank_mod3"] < n:
        return {"status": "UNKNOWN_NO_FULL_UNIT_DIFFERENCE_BASIS", "difference_basis": basis}
    rows = [row for r in records for row in (r.first, r.second)]
    differences = [tuple((a-b) % q for a, b in zip(r.first, r.second)) for r in records]
    required = {(0,)*n, *rows, *differences}
    raw = [(0,)*n, *rows, *differences] if base_frequencies is None else list(base_frequencies)
    if any(len(v) != n or any(type(x) is not int or not 0 <= x < q for x in v) for v in raw):
        raise ValueError("actual full-root frequency words required")
    V = list(dict.fromkeys(((0,)*n, *(tuple(x) for x in raw))))
    if not required.issubset(V):
        raise ValueError("base must retain every original native harmonic frequency")
    inverse = basis["modular_unit_difference_inverse"]
    S, lookup, trace = [], {}, []

    def offset(word):
        word = tuple(x % q for x in word)
        if word not in lookup:
            if len(S) >= max_offsets:
                raise ResourceLimit("whole offset-set cap exceeded")
            lookup[word] = len(S)
            S.append(word)
        return lookup[word]

    zero = offset((0,)*n)
    generators = [offset(differences[j]) for j in basis["basis_record_indices"]]

    def add(i, j):
        k = offset(tuple(a+b for a, b in zip(S[i], S[j])))
        trace.append({"left_offset": i, "right_offset": j, "result_offset": k})
        return k

    powers = {}

    def multiply(i, coefficient):
        total, power, bit = zero, i, 0
        while coefficient:
            if coefficient & 1:
                total = add(total, power)
            coefficient >>= 1
            bit += 1
            if coefficient:
                if (i, bit) not in powers:
                    powers[i, bit] = add(power, power)
                power = powers[i, bit]
        return total

    commuting = []
    for i, a in enumerate(generators):
        for b in generators[i+1:]:
            commuting.append({"left_generator": a, "right_generator": b, "sum_offset": add(a, b)})
    loops = [{"generator_offset": i, "integer_multiplier": q, "endpoint_offset": multiply(i, q)}
             for i in generators]
    if any(x["endpoint_offset"] != zero for x in loops):
        raise ArithmeticError("integer q-loop failed")
    targets = []
    for j, v in enumerate(V):
        coefficients = tuple(sum(v[k]*inverse[k][i] for k in range(n)) % q for i in range(n))
        total = zero
        for i, coefficient in zip(generators, coefficients):
            if coefficient:
                total = add(total, multiply(i, coefficient))
        if S[total] != v:
            raise ArithmeticError("flat translate reconstruction failed actual group frequency")
        targets.append({"base_frequency_index": j, "basis_coefficients": coefficients, "endpoint_offset": total})
    W, index = [], {}
    for v in V:
        for s in S:
            w = tuple((a+b) % q for a, b in zip(v, s))
            if w not in index:
                if len(W) >= max_nodes or (len(W)+1)**2 > max_entries:
                    raise ResourceLimit("whole translated moment matrix cap exceeded")
                index[w] = len(W)
                W.append(w)
    return {"status": "COMPLETE_FLAT_TRANSLATE_LAYOUT", "modulus": q, "components": n,
            "difference_basis": basis, "base_frequencies": V, "offsets": S,
            "generator_offsets": generators, "addition_trace": trace,
            "commutation_sums": commuting, "basis_q_loops": loops, "base_targets": targets,
            "extension_frequencies": W, "original_block_indices": [index[v] for v in V],
            "translated_node_indices": [[index[tuple((a+b) % q for a, b in zip(v, s))] for v in V] for s in S],
            "dense_classical_moment_entries": len(W)**2,
            "cyclotomic_field_degree": 2*q//3,
            "full_secret_grid_enumerated": False, "classical_completion_algorithm_supplied": False}


class Cyclotomic:
    def __init__(self, q, max_degree=54):
        root_digits(q)
        if type(max_degree) is not int or max_degree < 1:
            raise ValueError("positive exact cyclotomic field degree cap required")
        if 2*q//3 > max_degree:
            raise ResourceLimit("explicit cyclotomic field degree cap exceeded")
        self.q, self.degree = q, 2*q//3
        x = Symbol("x")
        self.K = QQ.algebraic_field((cyclotomic_poly(q, x), exp(2*pi*I/q)))
        self.z = self.K.unit
        self.powers = tuple(self.z**i for i in range(q))
        if self.z**q != self.K.one:
            raise ArithmeticError("cyclotomic quotient has wrong root order")

    def encode(self, value):
        return [str(Fraction(str(x))) for x in value.to_list()]

    def decode(self, value):
        if not isinstance(value, (tuple, list)) or any(type(x) is not str for x in value):
            raise ValueError("exact rational polynomial coefficient strings required")
        if len(value) > self.degree:
            raise ValueError("canonical reduced cyclotomic coefficient degree required")
        a = self.K([QQ(Fraction(x).numerator, Fraction(x).denominator) for x in value])
        if list(value) != self.encode(a):
            raise ValueError("canonical rational cyclotomic coefficient encoding required")
        return a

    def conjugate(self, value):
        coefficients = value.to_list()
        return sum((self.K.convert(a)*self.powers[-(len(coefficients)-1-i) % self.q]
                    for i, a in enumerate(coefficients)), self.K.zero)

    def matrix(self, rows):
        return DomainMatrix(rows, (len(rows), len(rows[0]) if rows else 0), self.K)

    def conjugate_matrix(self, matrix):
        return self.matrix([[self.conjugate(x) for x in row] for row in matrix.to_list()])

    def encode_matrix(self, matrix):
        return [[self.encode(x) for x in row] for row in matrix.to_list()]

    @staticmethod
    def retained_coefficient_bits(matrices, scalars=()):
        values = [x for M in matrices for row in M.to_list() for x in row]
        values.extend(scalars)
        height = 0
        for value in values:
            for coefficient in value.to_list():
                a = Fraction(str(coefficient))
                height = max(height, abs(a.numerator).bit_length(), a.denominator.bit_length())
        return height


@lru_cache(maxsize=16)
def _pi_interval(terms):
    def atan_interval(denominator):
        x = Fraction(1, denominator)
        total = sum(((-1)**j*x**(2*j+1)/ (2*j+1) for j in range(terms)), Fraction(0))
        next_term = (-1)**terms*x**(2*terms+1)/(2*terms+1)
        return min(total, total+next_term), max(total, total+next_term)
    a, b = atan_interval(5), atan_interval(239)
    return 16*a[0]-4*b[1], 16*a[1]-4*b[0]


def positive_weight_certificate(field, value, max_terms=128):
    if value != field.conjugate(value):
        return {"status": "REJECTED_NONREAL_CHARACTER_WEIGHT"}
    coefficients = value.to_list()
    if len(coefficients) <= 1:
        a = Fraction(str(coefficients[0])) if coefficients else Fraction(0)
        return {"status": "POSITIVE" if a > 0 else "ZERO" if a == 0 else "NEGATIVE",
                "rational_value": str(a), "lower": str(a), "upper": str(a)}
    terms = 8
    while terms <= max_terms:
        lo, hi = _pi_interval(terms)
        center, radius = (lo+hi)/2, (hi-lo)/2
        lower = upper = Fraction(0)
        for j, coefficient in enumerate(coefficients):
            k = len(coefficients)-1-j
            a = Fraction(str(coefficient))
            if not a:
                continue
            x = 2*k*center/field.q
            estimate = sum(((-1)**t*x**(2*t)/math.factorial(2*t) for t in range(terms)), Fraction(0))
            error = abs(x)**(2*terms)/math.factorial(2*terms)+2*k*radius/field.q
            left, right = estimate-error, estimate+error
            lower += a*(left if a > 0 else right)
            upper += a*(right if a > 0 else left)
        if lower > 0 or upper < 0:
            return {"status": "POSITIVE" if lower > 0 else "NEGATIVE", "lower": str(lower), "upper": str(upper),
                    "Machin_arctangent_terms": terms, "cosine_Taylor_terms": terms,
                    "interval_uses_only_exact_rational_arithmetic": True}
        terms *= 2
    return {"status": "UNKNOWN_ALGEBRAIC_WEIGHT_SIGN", "exact_zero_already_excluded": True}


def _raw_matrix(field, raw, size):
    if len(raw) != size or any(len(row) != size for row in raw):
        raise _Reject("complete matrix shape does not match compiled vocabulary")
    return field.matrix([[field.decode(x) for x in row] for row in raw])


def _saturated_guard(records, frequencies, original, field):
    basis = difference_basis(records)
    if basis["rank_mod3"] < len(records[0].first):
        return None
    index = {tuple(v): i for i, v in enumerate(frequencies)}
    values = original.to_list()
    for j in basis["basis_record_indices"]:
        r = records[j]
        if values[index[r.first]][index[r.second]] != field.K.one:
            return None
    zero = index[(0,)*len(records[0].first)]
    for i, v in enumerate(frequencies):
        if values[i][zero] != field.K.one:
            return {"frequency_index": i, "frequency": v,
                    "anchor_value": field.encode(values[i][zero]), "unit_difference_basis": basis,
                    "issue": "unit-basis pair expectations1 force secret0, inconsistent with retained original anchor"}
    return None


def verify_certificate(records, base_frequencies, original_matrix, extension_matrix,
                       max_nodes=1000, max_entries=1_000_000, max_field_degree=54):
    """Check supplied exact classical matrices; never trust a producer PSD flag."""
    records, n, q = _records(records)
    try:
        if len(base_frequencies)**2 > max_entries:
            raise ResourceLimit("whole original matrix cap exceeded")
        field = Cyclotomic(q, max_field_degree)
        original = _raw_matrix(field, original_matrix, len(base_frequencies))
        guard = _saturated_guard(records, base_frequencies, original, field)
        if guard:
            return {"status": "REJECTED_CHARACTER_DISTRIBUTION_SATURATION", "issues": [guard],
                    "character_distribution_certified": False, "completion_algorithm_supplied": False}
        layout = compile_layout(records, base_frequencies, max_nodes=max_nodes, max_entries=max_entries)
        if layout["status"] != "COMPLETE_FLAT_TRANSLATE_LAYOUT":
            return {"status": layout["status"], "character_distribution_certified": False}
        if list(map(tuple, base_frequencies)) != list(map(tuple, layout["base_frequencies"])):
            raise _Reject("original block must use complete canonical base vocabulary")
        N = len(layout["extension_frequencies"])
        M = _raw_matrix(field, extension_matrix, N)
        rows = M.to_list()
        base_indices = layout["original_block_indices"]
        if M.extract(base_indices, base_indices) != original:
            raise _Reject("supplied extension changed the retained original moment block")
        if field.conjugate_matrix(M).transpose() != M:
            raise _Reject("moment matrix is not exactly Hermitian")
        if any(rows[i][i] != field.K.one for i in range(N)):
            raise _Reject("moment diagonal is not exactly1")
        seen = {}
        W = layout["extension_frequencies"]
        for i, u in enumerate(W):
            for j, v in enumerate(W):
                difference = tuple((a-b) % q for a, b in zip(u, v))
                old = seen.setdefault(difference, rows[i][j])
                if old != rows[i][j]:
                    raise _Reject("full actual equal-frequency difference constraints fail")
        _, independent = original.rref()
        R = len(independent)
        if not R:
            raise _Reject("unit-diagonal matrix has zero rank")
        chosen = [base_indices[i] for i in independent]
        G = M.extract(chosen, chosen).transpose()
        try:
            inverse = G.inv()
        except DMNonInvertibleMatrixError as e:
            raise _Reject("selected base Hermitian metric is singular") from e
        coordinates = inverse*M.extract(list(range(N)), chosen).transpose()
        expected = coordinates.transpose()*G.transpose()*field.conjugate_matrix(coordinates)
        if expected != M:
            raise _Reject("extension rank is not flat over the retained original base")
        identity = DomainMatrix.eye(R, field.K).to_dense()
        operators = []
        metric_adjoint = lambda A: field.conjugate_matrix(A).transpose()*G
        for translated in layout["translated_node_indices"]:
            operator = coordinates.extract(list(range(R)), [translated[i] for i in independent])
            if metric_adjoint(operator)*operator != G:
                raise _Reject("translation is not unitary in the exact base Gram metric")
            for i, target in enumerate(translated):
                if operator*coordinates.extract(list(range(R)), [base_indices[i]]) != coordinates.extract(list(range(R)), [target]):
                    raise _Reject("translation does not preserve all base dependencies")
            operators.append(operator)
        if operators[0] != identity:
            raise _Reject("zero translation is not identity")
        for step in layout["addition_trace"]:
            if operators[step["left_offset"]]*operators[step["right_offset"]] != operators[step["result_offset"]]:
                raise _Reject("retained addition trace fails exact translation composition")
        generators = [operators[i] for i in layout["generator_offsets"]]
        for A in generators:
            if A**q != identity:
                raise _Reject("native group generator has incorrect q-order")
        for i, A in enumerate(generators):
            for B in generators[i+1:]:
                if A*B != B*A:
                    raise _Reject("native group translations do not commute")
        zero = W.index((0,)*n)
        anchor = coordinates.extract(list(range(R)), [zero])
        branches = [((), anchor)]
        scans = projector_terms = 0
        for A in generators:
            next_branches = []
            for eigenvalues, vector in branches:
                powers = [vector]
                for k in range(1, q):
                    powers.append(A*powers[-1])
                for value in range(q):
                    scans += 1
                    projected = DomainMatrix.zeros((R, 1), field.K).to_dense()
                    for k, power in enumerate(powers):
                        projected += power.scalarmul(field.powers[-value*k % q]/field.K.convert(q))
                        projector_terms += 1
                    if projected.is_zero_matrix:
                        continue
                    if A*projected != projected.scalarmul(field.powers[value]):
                        raise _Reject("projector does not isolate its exact root eigenvalue")
                    next_branches.append(((*eigenvalues, value), projected))
            if len(next_branches) > R:
                raise _Reject("joint eigenspace branching exceeded the certified flat rank")
            branches = next_branches
        inverse_D = layout["difference_basis"]["modular_unit_difference_inverse"]
        atoms = []
        for values, vector in branches:
            secret = tuple(sum(a*b for a, b in zip(row, values)) % q for row in inverse_D)
            weight = (field.conjugate_matrix(vector).transpose()*G*vector).to_list()[0][0]
            sign = positive_weight_certificate(field, weight)
            if sign["status"] != "POSITIVE":
                status = "UNKNOWN_ALGEBRAIC_WEIGHT_SIGN" if sign["status"].startswith("UNKNOWN") else "REJECTED_NONPOSITIVE_CHARACTER_WEIGHT"
                return {"status": status, "issues": [{"secret": secret, "weight": field.encode(weight), "sign": sign}],
                        "character_distribution_certified": False, "completion_algorithm_supplied": False}
            atoms.append({"secret": secret, "weight": field.encode(weight), "positive_weight_certificate": sign})
        if sum((field.decode(a["weight"]) for a in atoms), field.K.zero) != field.K.one:
            raise _Reject("extracted character weights do not sum exactly to1")
        decoded = [(a["secret"], field.decode(a["weight"])) for a in atoms]
        for i, u in enumerate(W):
            for j, v in enumerate(W):
                value = sum((weight*field.powers[sum((a-b)*s for a, b, s in zip(u, v, secret)) % q]
                             for secret, weight in decoded), field.K.zero)
                if value != rows[i][j]:
                    raise _Reject("positive extracted characters do not reproduce the complete supplied matrix")
        return {"status": "EXACT_FLAT_CHARACTER_DISTRIBUTION_CERTIFIED_REVIEW_PENDING",
                "character_distribution_certified": True, "PSD_certified_by_positive_character_reconstruction": True,
                "rank_original_exact": R, "rank_extension_exact": R, "character_atoms": atoms,
                "independent_base_frequency_indices": independent,
                "all_moment_entries_checked": N*N, "translation_operators_checked": len(operators),
                "projector_eigenvalues_scanned": scans, "projector_terms_charged": projector_terms,
                "field_degree_charged": field.degree, "full_secret_grid_size": str(q**n),
                "classical_extension_compact_JSON_bytes": len(json.dumps(extension_matrix, separators=(",", ":"))),
                "input_max_rational_coefficient_bits": field.retained_coefficient_bits([M]),
                "retained_coordinate_operator_atom_max_coefficient_bits": field.retained_coefficient_bits([inverse, coordinates, *operators], [weight for _, weight in decoded]),
                "all_internal_intermediate_bit_costs_certified": False,
                "full_secret_grid_enumerated": False, "floating_PSD_or_rank_tolerance_used": False,
                "original_block_retained_exactly": True, "classical_completion_algorithm_supplied": False,
                "native_noisy_recovery_proved": False, "quantum_speedup_proved": False}
    except ResourceLimit as e:
        return {"status": "UNKNOWN_RESOURCE_LIMIT", "issues": [str(e)], "character_distribution_certified": False}
    except (_Reject, ValueError, KeyError, IndexError, TypeError) as e:
        return {"status": "REJECTED_EXACT_CERTIFICATE", "issues": [str(e)], "character_distribution_certified": False}


def mixture_matrix(field, frequencies, atoms):
    """Known-atom calibration producer, never a decoder for native outcomes."""
    return field.matrix([[sum((weight*field.powers[sum((a-b)*s for a, b, s in zip(u, v, secret)) % field.q]
                               for secret, weight in atoms), field.K.zero) for v in frequencies] for u in frequencies])


def round_harmonic_score(records, verified):
    """Exact score dequantization consequence of a verified character mixture."""
    records, _, q = _records(records)
    if not verified.get("character_distribution_certified"):
        raise ValueError("verified positive character distribution required")
    field = Cyclotomic(q)
    atoms = verified["character_atoms"]
    scores = []
    for atom in atoms:
        score = field.K.zero
        for record in records:
            a, c = record.residual(atom["secret"])
            for e in (a, c, (a-c) % q):
                score += (field.powers[e]+field.powers[-e % q])/field.K.convert(2)
        scores.append(score)
    weights = [field.decode(atom["weight"]) for atom in atoms]
    if sum(weights, field.K.zero) != field.K.one:
        raise ValueError("normalized character distribution required")
    average = sum((w*s for w, s in zip(weights, scores)), field.K.zero)
    best = 0
    for i in range(1, len(atoms)):
        comparison = positive_weight_certificate(field, scores[i]-scores[best])
        if comparison["status"] not in ("POSITIVE", "ZERO", "NEGATIVE"):
            return {"status": "UNKNOWN_EXACT_SCORE_ORDERING", "native_noisy_recovery_proved": False}
        if comparison["status"] == "POSITIVE":
            best = i
    margin = positive_weight_certificate(field, scores[best]-average)
    if margin["status"] not in ("POSITIVE", "ZERO"):
        raise ArithmeticError("rounded character score did not dominate the exact mixture score")
    return {"status": "CLASSICAL_CHARACTER_DOMINATES_VERIFIED_NATIVE_HARMONIC_SCORE",
            "selected_secret": atoms[best]["secret"], "selected_score": field.encode(scores[best]),
            "mixture_score": field.encode(average), "margin_certificate": margin,
            "only_extracted_character_candidates_tested": len(atoms),
            "full_secret_grid_enumerated": False, "native_noisy_recovery_proved": False,
            "held_out_native_prediction_verified": False, "native_log_likelihood_is_this_score": False}


def native_control(n, r, inputs, seed, algebraic_weights=False):
    source = random_even_source(n, 2*r, inputs, seed)
    records = tuple(CovariantRecord(a, c, (0, 0), source.modulus) for a, c in source.frequencies)
    layout = compile_layout(records)
    field = Cyclotomic(source.modulus)
    secrets = ((0,)*n, tuple((2*i+1) % field.q for i in range(n)), (field.q-1,)*n)
    atoms = tuple((s, field.K.convert(w)) for s, w in zip(secrets, (QQ(1, 2), QQ(1, 3), QQ(1, 6))))
    if algebraic_weights:
        weight = (field.K.convert(2)+field.z+field.powers[-1])/field.K.convert(4)
        atoms = ((secrets[0], weight), (secrets[1], field.K.one-weight))
    extension = mixture_matrix(field, layout["extension_frequencies"], atoms)
    original = extension.extract(layout["original_block_indices"], layout["original_block_indices"])
    original_raw, extension_raw = field.encode_matrix(original), field.encode_matrix(extension)
    verified = verify_certificate(records, layout["base_frequencies"], original_raw, extension_raw)
    if not verified.get("character_distribution_certified"):
        raise ArithmeticError(f"honest native-label mixture failed exact certificate: {verified}")
    recovered = {tuple(a["secret"]): field.decode(a["weight"]) for a in verified["character_atoms"]}
    if recovered != dict(atoms):
        raise ArithmeticError("secret-blind extractor did not recover known calibration atoms")
    return {"seed": seed, "original_native_level": source.level, "original_ring_labels": source.labels,
            "original_native_frequencies": source.frequencies, "records": [r.public() for r in records],
            "layout": layout, "original_moment_matrix": original_raw, "extension_moment_matrix": extension_raw,
            "known_atoms_used_only_by_calibration_producer": True,
            "supplied_matrix_was_learned_from_noisy_native_records": False,
            "external_IID_native_supply_certified": False, "verification": verified,
            "harmonic_score_rounding": round_harmonic_score(records, verified)}


def native_nonextension_controls():
    source = json.loads(NEGATIVE_SOURCE.read_text())
    original_source = json.loads((ROOT/source["source_report"]).read_text())
    controls = []
    for c in source["native_controls"]:
        records = tuple(CovariantRecord(tuple(r["first"]), tuple(r["second"]), tuple(r["outcome"]), r["modulus"])
                        for r in c["records"])
        original_lift = next(x for x in original_source["native_controls"] if x["seed"] == c["source_seed"])["adaptive_character_lift"]
        selected = {}
        for i, node in enumerate(original_lift["nodes"]):
            selected.setdefault(tuple(node["frequency"]), i)
        frequencies = list(selected)
        field = Cyclotomic(records[0].modulus)
        classes = c["partition_witness"]["class_labels"]
        matrix = field.matrix([[field.K.one if classes[i] == classes[j] else field.K.zero
                                for j in selected.values()] for i in selected.values()])
        result = verify_certificate(records, frequencies, field.encode_matrix(matrix), [], max_nodes=1)
        if result["status"] != "REJECTED_CHARACTER_DISTRIBUTION_SATURATION":
            raise ArithmeticError("native nonextension falsifier was accepted or hidden by a resource cap")
        controls.append({"source_seed": c["source_seed"], "base_node_count": len(frequencies),
                         "exact_original_PSD_rank": c["partition_witness"]["matrix_rank_exact"],
                         "saturation_guard_runs_before_extension_construction": True, "verification": result})
    return controls


def run_controls():
    return {"status": "EXACT_NATIVE_FLAT_CERTIFICATE_CONDITIONAL_CLASSICAL_EXTRACTION_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_controls": [native_control(n, r, m, seed) for n, r, m, seed in ((2, 2, 3, 89641), (1, 3, 2, 89643))],
            "nonrational_positive_weight_countercontrol": native_control(2, 2, 3, 89641, algebraic_weights=True),
            "native_nonextension_source": str(NEGATIVE_SOURCE.relative_to(ROOT)),
            "native_nonextension_source_sha256": hashlib.sha256(NEGATIVE_SOURCE.read_bytes()).hexdigest(),
            "native_nonextension_controls": native_nonextension_controls(),
            "completion_solver_implemented": False, "approximate_flatness_proved": False,
            "native_noisy_decoder_supplied": False, "quantum_speedup_proved": False,
            "candidate_record_accepted": False, "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "verified_ranks": [c["verification"]["rank_extension_exact"] for c in report["native_controls"]]}, indent=2))


if __name__ == "__main__":
    main()
