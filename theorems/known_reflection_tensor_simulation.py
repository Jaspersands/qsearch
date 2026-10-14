"""Exact rational tensor counterpart for known full-system seed reflections.

No unknown source phases, subsystem reflections, or arbitrary quantum circuit
simulation. Local constructive closure and precision derivation review pending.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import random

from flint import fmpq
import numpy as np

from known_preparation_coherent_reflection import checked_shape, dense_preparation, reflection_recipe
from known_preparation_packet_simulation import ACCESS, known_source_packets, raw_source_fixture
from ternary_certified_noise_sampler import cosine_box, sqrt_box
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/KNOWN_REFLECTION_TENSOR_SIMULATION.md"
REPORT = ROOT/"research/classical_baselines/known_reflection_tensor_simulation.json"
ZERO, ONE = (fmpq(0), fmpq(0)), (fmpq(1), fmpq(0))


def add(a, b): return a[0]+b[0], a[1]+b[1]
def mul(a, b): return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]
def conj(a): return a[0], -a[1]
def scale(a, b): return a[0]*b, a[1]*b
def dot(a, b): return sum_complex(mul(conj(x), y) for x, y in zip(a, b))


def sum_complex(values):
    out = ZERO
    for value in values: out = add(out, value)
    return out


def integer_text(value):
    # FLINT serialization avoids Python's decimal-digit cap without changing it.
    return str(fmpq(value))


def encoded_integer(value):
    if type(value) is int:
        return value
    if type(value) is str:
        try:
            parsed = fmpq(value)
            if parsed.denominator == 1 and str(parsed) == value:
                return int(parsed.numerator)
        except (ValueError, ZeroDivisionError):
            pass
    raise ValueError("canonical exact integer phase/source descriptor required")


def dyadic_midpoint(lo, hi, bits):
    x = (lo+hi)/2*2**bits
    return fmpq(int(x.numerator)//int(x.denominator), 2**bits)


def root_entry(q, k, bits):
    root_digits(q)
    integer(bits, "positive root approximation bits", 1)
    if type(k) is not int:
        raise ValueError("known integer phase numerator required")
    k %= q
    if not k: return ONE
    precision = 2*bits+16
    lo, hi = cosine_box(q, k, precision)
    c = max(fmpq(-1), min(fmpq(1), dyadic_midpoint(lo, hi, precision)))
    a, b = sqrt_box(1-c*c, bits+8)
    s = (a+b)/2
    return c, s if 2*k < q else -s


def qutrit_vector(q, phases, bits):
    phases = tuple(phases)
    if len(phases) != 3 or any(type(k) is not int or not 0 <= k < q for k in phases):
        raise ValueError("explicit known canonical qutrit phases required")
    lo, hi = sqrt_box("1/3", bits+8)
    return tuple(scale(root_entry(q, k, bits), (lo+hi)/2) for k in phases)


@dataclass(frozen=True)
class Term:
    coefficient: tuple
    factors: tuple


@dataclass(frozen=True)
class TensorState:
    terms: tuple[Term, ...]
    shape: tuple[int, ...]

    def __post_init__(self):
        if not self.terms or not self.shape or any(type(d) is not int or d <= 0 for d in self.shape):
            raise ValueError("nonempty explicit tensor shape and terms required")
        if any(len(t.factors) != len(self.shape) or any(len(v) != d for v, d in zip(t.factors, self.shape)) for t in self.terms):
            raise ValueError("all product factors must match the declared tensor shape")

    def norm_squared(self):
        result = ZERO
        for a in self.terms:
            for b in self.terms:
                x = mul(conj(a.coefficient), b.coefficient)
                for left, right in zip(a.factors, b.factors): x = mul(x, dot(left, right))
                result = add(result, x)
        if result[1] != 0 or result[0] < 0:
            raise ArithmeticError("exact tensor Gram norm is not real nonnegative")
        return result[0]

    def project(self, slot, value):
        integer(slot, "local tensor slot")
        if slot >= len(self.shape) or type(value) is not int or not 0 <= value < self.shape[slot]:
            raise ValueError("legal computational projection required")
        out = []
        for term in self.terms:
            factors = list(term.factors)
            factors[slot] = tuple(x if j == value else ZERO for j, x in enumerate(factors[slot]))
            out.append(Term(term.coefficient, tuple(factors)))
        return TensorState(tuple(out), self.shape)

    def local_gate(self, slot, matrix):
        integer(slot, "local tensor slot")
        if slot >= len(self.shape): raise ValueError("legal local factor required")
        d = self.shape[slot]
        if len(matrix) != d or any(len(row) != d for row in matrix):
            raise ValueError("local gate cannot couple factors or add a work register")
        out = []
        for term in self.terms:
            factors = list(term.factors)
            factors[slot] = tuple(sum_complex(mul(x, y) for x, y in zip(row, factors[slot])) for row in matrix)
            out.append(Term(term.coefficient, tuple(factors)))
        return TensorState(tuple(out), self.shape)

    def full_system_reflection(self, seed, cohort_count, term_cap):
        integer(term_cap, "positive committed tensor term cap", 1)
        if self.shape != seed.shape or len(seed.terms) != cohort_count or any(t.coefficient != ONE for t in seed.terms):
            raise ValueError("reflection requires the actual full-system unscaled known cohort seed")
        if seed.shape != (cohort_count,)+(3,)*(len(seed.shape)-1) or any(t.factors[0] != tuple(ONE if i == b else ZERO for i in range(cohort_count)) for b, t in enumerate(seed.terms)):
            raise ValueError("explicit orthogonal cohort index sectors are required")
        if len(self.terms)+cohort_count > term_cap:
            raise ValueError("committed tensor term cap exhausted")
        overlap = ZERO
        for a in seed.terms:
            for b in self.terms:
                x = b.coefficient
                for left, right in zip(a.factors, b.factors): x = mul(x, dot(left, right))
                overlap = add(overlap, x)
        beta = scale(overlap, fmpq(-2, cohort_count))
        return TensorState(self.terms+tuple(Term(beta, t.factors) for t in seed.terms), self.shape)

    def diagnostic_vector(self):
        if np.prod(self.shape, dtype=object) > 256:
            raise ValueError("dense vector reconstruction is a bounded diagnostic only")
        out = np.zeros(int(np.prod(self.shape)), complex)
        for t in self.terms:
            v = np.array([complex(float(t.coefficient[0]), float(t.coefficient[1]))])
            for factor in t.factors:
                v = np.kron(v, np.array([complex(float(x), float(y)) for x, y in factor]))
            out += v
        return out


def seed_tensor(recipe, bits):
    if recipe.get("secret_or_errors_read_by_preparation") is not False or recipe.get("ideal_unknown_state_inverse_supplied") is not False:
        raise ValueError("actual same-original-data known recipe required, not an ideal source inverse")
    B, M, q = recipe["cohorts"], recipe["sites_per_cohort"], encoded_integer(recipe["modulus"])
    checked_shape(B, M)
    phases = recipe["known_phase_numerators"]
    if len(phases) != B or any(len(cohort) != M for cohort in phases):
        raise ValueError("complete explicit known phase cohorts required")
    receipt = recipe.get("source_receipts", {})
    if receipt.get("phase_access") != ACCESS:
        raise ValueError("original classical phase receipts required, not guessed unknown state factors")
    raw = tuple(NoisyLinearRecord(tuple(map(encoded_integer, r["label"])), encoded_integer(r["value"]), encoded_integer(r["modulus"]), r["source_id"]) for r in receipt["original_classical_records"])
    packets, _ = known_source_packets(raw, tuple(map(encoded_integer, receipt["preparation_random_mask"])))
    if len(packets) != B*M or any(p.modulus != q for p in packets) or any(tuple(p.phase_numerators) != tuple(map(encoded_integer, v)) for p, v in zip(packets, (v for cohort in phases for v in cohort))):
        raise ValueError("known factors disagree with the actual original phase receipts")
    terms = []
    for b, cohort in enumerate(phases):
        index = tuple(ONE if j == b else ZERO for j in range(B))
        terms.append(Term(ONE, (index,)+tuple(qutrit_vector(q, tuple(map(encoded_integer, p)), bits) for p in cohort)))
    return TensorState(tuple(terms), (B,)+(3,)*M)


def fourier_gate(bits):
    return tuple(qutrit_vector(3, tuple(i*j % 3 for j in range(3)), bits) for i in range(3))


def diagonal_gate(q, phases, bits):
    if len(phases) != 3: raise ValueError("known qutrit diagonal phases required")
    return tuple(tuple(root_entry(q, phases[i], bits) if i == j else ZERO for j in range(3)) for i in range(3))


def program_budget(B, M, reflections, local_gates, bits, sampling_failure_bits=24):
    checked_shape(B, M)
    integer(reflections, "committed reflection cap")
    integer(local_gates, "committed local gate cap")
    integer(bits, "positive approximation bits", 1)
    integer(sampling_failure_bits, "positive finite sampler error bits", 1)
    delta = fmpq(1, 2**bits)
    e = (1+delta)**M-1
    eta = 4*e+2*e*e
    E = (1+e)*(1+3*delta)**local_gates*(1+eta)**reflections-1
    cap = sampling_failure_bits+M.bit_length()
    abort = fmpq(M+1, 2**cap)
    p = 3*bits+32
    coefficient = reflections*(M*(local_gates+2)*p+B.bit_length()-1)
    return {"cohorts": B, "sites_per_cohort": M, "reflection_cap": reflections,
            "local_gate_cap": local_gates, "approximation_bits": bits,
            "max_tensor_terms": B*(reflections+1), "per_qutrit_vector_error_upper": str(delta),
            "seed_relative_vector_error_upper": str(e), "reflection_operator_error_upper": str(eta),
            "final_relative_vector_error_upper": str(E), "logical_measurement_TV_upper": str(min(fmpq(1), 2*E)),
            "sampling_failure_bits": sampling_failure_bits, "coin_attempt_cap_per_factor": cap,
            "unconditional_coin_abort_upper": str(abort),
            "complete_logical_sampling_TV_or_abort_upper": str(min(fmpq(1), 2*E+abort)),
            "dyadic_entry_denominator_exponent_upper": p,
            "factor_denominator_exponent_upper": (local_gates+1)*p,
            "coefficient_denominator_exponent_upper": coefficient,
            "source_noise_law_or_independence_required": False,
            "normalized_approximation_is_exact_ideal_quantum_program": False,
            "subsystem_reflections_or_entangled_work_covered": False,
            "quantum_only_unknown_source_covered": False,
            "conditioning_away_coin_abort_allowed": False}


def sample_basis(state, rng, attempt_cap):
    integer(attempt_cap, "positive finite rejection attempt cap", 1)
    current, decisions = state, []
    if current.norm_squared() == 0:
        raise ValueError("nonzero rational point vector required")
    for slot, d in enumerate(state.shape):
        children = tuple(current.project(slot, k) for k in range(d))
        weights = tuple(child.norm_squared() for child in children)
        if sum(weights, fmpq(0)) != current.norm_squared():
            raise ArithmeticError("exact computational branch norms do not sum to prefix norm")
        scale_denom = max(int(w.denominator) for w in weights)
        if scale_denom & (scale_denom-1):
            raise ValueError("dyadic tensor program required for bounded integer-weight sampling")
        counts = tuple(int(w*scale_denom) for w in weights)
        if any(fmpq(c, scale_denom) != w for c, w in zip(counts, weights)):
            raise ArithmeticError("integer conversion changed a branch weight")
        total, selected, attempts = sum(counts), None, []
        bits = (total-1).bit_length()
        for _ in range(attempt_cap):
            draw = rng.getrandbits(bits)
            if type(draw) is not int or not 0 <= draw < 2**bits:
                raise ValueError("independent canonical coin block required")
            attempts.append(integer_text(draw))
            if draw >= total: continue
            threshold = 0
            for k, count in enumerate(counts):
                threshold += count
                if draw < threshold:
                    selected = k
                    break
            break
        decisions.append({"slot": slot, "exact_branch_weights": tuple(map(str, weights)),
                          "integer_weight_scale": integer_text(scale_denom), "integer_weights": tuple(map(integer_text, counts)),
                          "uniform_integer_total": integer_text(total), "coin_bits_per_attempt": bits,
                          "coin_draws": attempts, "selected_outcome": selected})
        if selected is None:
            return {"status": "EXPLICIT_COIN_ATTEMPT_ABORT", "outcomes": None, "decisions": decisions,
                    "conditional_on_completion_is_exact_rational_program_law": False}
        current = children[selected]
    return {"status": "CERTIFIED_RATIONAL_POINT_SAMPLE", "outcomes": tuple(d["selected_outcome"] for d in decisions),
            "decisions": decisions, "conditional_on_completion_is_exact_ideal_quantum_law": False,
            "conditional_on_completion_is_exact_rational_program_law": False}


def run_control(B, M, digits, T, bits, seed_value):
    _, source = raw_source_fixture(2, digits, B*M, seed_value)
    raw = tuple(NoisyLinearRecord(tuple(r["label"]), r["value"], r["modulus"], r["source_id"]) for r in source["original_classical_records"])
    recipe = reflection_recipe(raw, source["preparation_random_mask"], B, M)
    seed = seed_tensor(recipe, bits)
    budget = program_budget(B, M, T, 2*T, bits)
    state, history = seed, []
    q = 3**digits
    literal = B*3**M <= 256
    vector, reflection = None, None
    if literal:
        _, vector, reflection, _ = dense_preparation(recipe["known_phase_numerators"], q)
    for t in range(T):
        slot = t % M+1
        phases = (0, (3*t+1) % q, (5*t+2) % q)
        state = state.local_gate(slot, diagonal_gate(q, phases, bits)).local_gate(slot, fourier_gate(bits))
        state = state.full_system_reflection(seed, B, budget["max_tensor_terms"])
        history.append({"step": t, "local_qutrit_slot": slot, "diagonal_phase_numerators": phases,
                        "tensor_terms": len(state.terms)})
        if literal:
            shape = (B,)+(3,)*M
            v = np.moveaxis(vector.reshape(shape), slot, -1)
            v *= np.exp(2j*np.pi*np.array(phases)/q)
            F = np.exp(2j*np.pi*np.outer(np.arange(3), np.arange(3))/3)/np.sqrt(3)
            v = np.einsum("ij,...j->...i", F, v)
            vector = reflection@np.moveaxis(v, -1, slot).reshape(-1)
    norm = state.norm_squared()
    if norm <= 0: raise ArithmeticError("approximate program produced zero norm")
    observed = None
    if literal:
        approximate = state.diagnostic_vector()/math.sqrt(float(norm))
        observed = float(np.sum(abs(abs(approximate)**2-abs(vector)**2))/2)
        if observed > float(fmpq(budget["logical_measurement_TV_upper"]))+1e-11:
            raise ArithmeticError("literal quantum law escaped certified global tensor approximation budget")
    sample = sample_basis(state, random.Random(seed_value+1), budget["coin_attempt_cap_per_factor"])
    denominators = [int(x.denominator).bit_length()-1 for t in state.terms for x in t.coefficient]
    factor_denominators = [int(x.denominator).bit_length()-1 for t in state.terms for v in t.factors for z in v for x in z]
    if max(denominators) > budget["coefficient_denominator_exponent_upper"] or max(factor_denominators) > budget["factor_denominator_exponent_upper"]:
        raise ArithmeticError("dyadic bit complexity exceeded the declared polynomial ledger")
    return {"modulus": str(q), "recipe": recipe, "budget": budget, "program_history": history,
            "final_tensor_terms": len(state.terms), "final_rational_norm_squared": str(norm),
            "largest_coefficient_denominator_exponent": max(denominators),
            "largest_factor_denominator_exponent": max(factor_denominators),
            "dense_quantum_law_TV_diagnostic": observed, "full_Hilbert_space_allocated": literal,
            "final_computational_sample": sample, "hidden_secret_or_error_used": False,
            "unknown_state_regenerated": False, "scalable_path_builds_root_table": False}


def build_report():
    controls = [run_control(B, M, d, T, bits, seed) for B, M, d, T, bits, seed in
                ((1, 3, 2, 4, 20, 83001), (2, 2, 2, 6, 20, 83002),
                 (2, 16, 16, 3, 20, 83003), (1, 32, 64, 3, 20, 83004))]
    return {"status": "SCOPED_KNOWN_FULL_SYSTEM_REFLECTION_TENSOR_SIMULATION_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest() for name in
                                  ("known_preparation_coherent_reflection.py", "known_preparation_packet_simulation.py",
                                   "native_noisy_phase_input.py", "ternary_certified_noise_sampler.py")},
            "controls": controls,
            "research_decision": "DEPRIORITIZE_KNOWN_COHORT_FULL_SYSTEM_REFLECTION_AND_LOCAL_GATE_PROGRAMS",
            "generic_quantum_classical_simulation_proved": False,
            "opaque_HSP_inputs_dequantized": False, "subsystem_reflection_programs_dequantized": False,
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "remaining_debt": ["external proof and implementation review",
                               "independent reconstruction of the complete tensor arithmetic, beyond ledger/coin replay",
                               "production source/primitive-family admission integration",
                               "actual coherent work coupling outside this closure and its own tensor baseline"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "tensor_terms": [c["final_tensor_terms"] for c in report["controls"]],
                      "roots": [c["modulus"] for c in report["controls"]],
                      "samples": [c["final_computational_sample"]["status"] for c in report["controls"]],
                      "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__":
    main()
