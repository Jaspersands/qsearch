"""Polynomial coarse-only nonlinear involution: a costed Gaussian baseline.

Two bits of descent use (n+1)^2 original phase qubits. This closes an
implementation gap, not the exponential recursive supply or noisy-source gap.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
from random import Random

from theorems.dcp_adaptive_direction_rank_gate import binary_kernel, binary_map, dyadic, integer
from theorems.dcp_affine_fiber_rigidity import matrix, signature_certificate


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_disjoint_kernel_pairing.json"
CONTRACT = ROOT / "research/hypotheses/dcp_disjoint_kernel_pairing_contract.json"
KIND = "POLYNOMIAL_DISJOINT_PARITY_KERNEL"
CONTRACT_ID = "coarse_only_disjoint_kernel_nonlinear_involution_v1"


def make_program(labels):
    A = matrix(labels)
    n, m = len(A), len(A[0])
    if m < (n+1)**2:
        raise ValueError("UNKNOWN: disjoint-kernel sufficient supply requires (n+1)^2 inputs")
    coarse = tuple(tuple(a % 4 for a in row) for row in A)
    supports = []
    for j in range(n+1):
        start = j*(n+1)
        block = tuple(sum((row[start+i] & 1) << i for i in range(n+1)) for row in coarse)
        supports.append(binary_kernel(block, n+1)[0] << start)
    return {
        "kind": KIND, "width": m, "components": n, "descent_bits": 2,
        "coarse_labels": [list(row) for row in coarse], "disjoint_supports_hex": [hex(u) for u in supports],
        "selection_access": "coarse-public-labels-only", "uniform_efficient_program_supplied": True,
        "support_selection_access": "A-mod2-only-canonical-block-kernel",
        "table_lookup_is_a_free_coherent_oracle": False,
        "full_assignment_lookup_rows": 0,
        "algorithmic_baseline": "disjoint parity dependencies followed by binary Gaussian dependence",
        "new_sieve_exponent_claimed": False,
    }


def check_program(program):
    if program.get("kind") != KIND or program.get("descent_bits") != 2:
        raise ValueError("unsupported descent program")
    A = matrix(program["coarse_labels"])
    n, m = len(A), len(A[0])
    integer(program["width"], "program width", 1, 4096)
    integer(program["components"], "program components", 1, 4096)
    if m != program["width"] or n != program["components"] or m < (n+1)**2 or any(a > 3 for row in A for a in row):
        raise ValueError("invalid coarse program dimensions or labels")
    supports = tuple(int(u, 16) for u in program["disjoint_supports_hex"])
    if len(supports) != n+1:
        raise ValueError("n+1 supports required")
    occupied = 0
    for u in supports:
        integer(u, "nonempty disjoint support", 1, (1 << m)-1)
        if occupied & u or any(sum(a for i, a in enumerate(row) if u >> i & 1) % 2 for row in A):
            raise ValueError("disjoint original supports in ker(A mod2) required")
        occupied |= u
    if (program.get("selection_access") != "coarse-public-labels-only"
            or program.get("support_selection_access") != "A-mod2-only-canonical-block-kernel"
            or program.get("uniform_efficient_program_supplied") is not True
            or program.get("table_lookup_is_a_free_coherent_oracle") is not False
            or program.get("full_assignment_lookup_rows") != 0
            or program.get("new_sieve_exponent_claimed") is not False):
        raise ValueError("program access/cost/novelty claim mismatch")
    expected = make_program(A)["disjoint_supports_hex"]
    if list(program["disjoint_supports_hex"]) != expected:
        raise ValueError("canonical low-bit-only support provenance mismatch")
    return A, supports


def first_dependence(columns, n):
    """Canonical online column elimination; no search over subsets."""
    pivots = {}
    for j, value in enumerate(columns):
        witness = 1 << j
        for p in range(n-1, -1, -1):
            if not value >> p & 1:
                continue
            if p in pivots:
                value ^= pivots[p][0]
                witness ^= pivots[p][1]
            else:
                pivots[p] = (value, witness)
                break
        else:
            return witness
    raise ArithmeticError("n+1 columns in F2^n must have a nonempty dependence")


def control_columns(program, x):
    A, supports = check_program(program)
    integer(x, "original assignment", 0, (1 << program["width"])-1)
    return tuple(sum(((sum(a * (1-2*(x >> i & 1)) for i, a in enumerate(row) if u >> i & 1)//2) & 1) << l
                     for l, row in enumerate(A)) for u in supports)


def partner(program, x):
    columns = control_columns(program, x)
    dependence = first_dependence(columns, program["components"])
    direction = 0
    for j, u in enumerate(program["disjoint_supports_hex"]):
        if dependence >> j & 1:
            direction ^= int(u, 16)
    return x ^ direction


class BooleanNetwork:
    """Fresh-work-wire XOR/AND network exported as X/CX/CCX gates."""
    def __init__(self, inputs):
        self.inputs = inputs
        self.wires = inputs
        self.gates = []
        self.zero = self.xor(())
        self.one = self.xor((), 1)

    def xor(self, controls, constant=0):
        out = self.wires
        self.wires += 1
        if constant:
            self.gates.append(("X", out))
        self.gates.extend(("CX", c, out) for c in controls)
        return out

    def both(self, a, b):
        if a == b:
            return a
        out = self.wires
        self.wires += 1
        self.gates.append(("CCX", a, b, out))
        return out

    def not_(self, a):
        return self.xor((a,), 1)


def reversible_evaluator(program):
    """Static gate sequence for (x,z,0)->(x,z XOR (valid,F(x)),0).

    Pivots/branches are themselves Boolean wires. No host-language branch may
    depend on the unknown assignment. The cap limits exported certificates,
    not the uniform polynomial construction stated in the proof.
    """
    A, supports = check_program(program)
    n, m = len(A), len(A[0])
    if n > 8 or m > 256:
        raise ValueError("UNKNOWN: explicit reversible gate-export work cap")
    N = BooleanNetwork(m)
    columns = []
    for u in supports:
        columns.append([N.xor(tuple(i for i, a in enumerate(row) if u >> i & 1 and a & 1),
                              (sum(a for i, a in enumerate(row) if u >> i & 1)//2) & 1) for row in A])
    pivots = [[N.zero]*n for _ in range(n)]
    witnesses = [[N.zero]*(n+1) for _ in range(n)]
    occupied = [N.zero]*n
    found, result = N.zero, [N.zero]*(n+1)
    for j, column in enumerate(columns):
        v, w, active = column, [N.one if k == j else N.zero for k in range(n+1)], N.one
        for p in range(n-1, -1, -1):
            flag = N.both(active, v[p])
            reduce = N.both(flag, occupied[p])
            store = N.both(flag, N.not_(occupied[p]))
            old_v, old_w = pivots[p], witnesses[p]
            pivots[p] = [N.xor((a, N.both(store, b))) for a, b in zip(old_v, v)]
            witnesses[p] = [N.xor((a, N.both(store, b))) for a, b in zip(old_w, w)]
            occupied[p] = N.xor((occupied[p], store))
            v = [N.xor((a, N.both(reduce, b))) for a, b in zip(v, old_v)]
            w = [N.xor((a, N.both(reduce, b))) for a, b in zip(w, old_w)]
            active = N.xor((active, store))
        take = N.both(active, N.not_(found))
        result = [N.xor((a, N.both(take, b))) for a, b in zip(result, w)]
        found = N.xor((found, take))
    outputs = []
    for i in range(m):
        block = next((j for j, u in enumerate(supports) if u >> i & 1), None)
        outputs.append(i if block is None else N.xor((i, result[block])))
    # Embed network work after the public x and arbitrary XOR output register.
    def wire(i):
        return i if i < m else i+m+1
    compute = [tuple([gate[0]] + [wire(i) for i in gate[1:]]) for gate in N.gates]
    copies = [("CX", wire(value), m+i) for i, value in enumerate(outputs)] + [("X", 2*m)]
    gates = [list(gate) for gate in compute + copies + list(reversed(compute))]
    return {
        "kind": "X_CX_CCX_COMPUTE_COPY_UNCOMPUTE",
        "program_sha256": hashlib.sha256(json.dumps(program, sort_keys=True).encode()).hexdigest(),
        "input_bits": m, "xor_output_bits_including_valid": m+1,
        "zero_work_bits_required": N.wires-m, "total_qubits": N.wires+m+1,
        "gates": gates, "gate_counts": dict(Counter(gate[0] for gate in gates)),
        "unknown_source_inverse_used": False, "hardware_transpilation_executed": False,
        "cost_order": "O(n*m+n^3+m) elementary reversible gates and work bits",
    }


def apply_evaluator(word, circuit, inverse=False):
    integer(word, "evaluator packed wires", 0, (1 << circuit["total_qubits"])-1)
    for gate in reversed(circuit["gates"]) if inverse else circuit["gates"]:
        if all(word >> control & 1 for control in gate[1:-1]):
            word ^= 1 << gate[-1]
    return word


def feedforward_branches(labels, phase_bits, program):
    """All finite outcomes of a two-stage CNOT/Z receiver, no coherent solver.

    This census is a diagnostic. One real attempt follows ONE measured branch
    and executes at most O(m+n) CNOTs and two classical Gaussian routines.
    """
    from theorems.dcp_nonlinear_fiber_pairing import instance
    A = instance(labels, phase_bits, 2, max_width=10)
    coarse, supports = check_program(program)
    n, m, q = len(A), len(A[0]), 1 << phase_bits
    if tuple(tuple(a % 4 for a in row) for row in A) != coarse:
        raise ValueError("original source/coarse program mismatch")
    pivots = [(u & -u).bit_length()-1 for u in supports]
    pivot_mask = sum(1 << p for p in pivots)
    first = [(p, i) for p, u in zip(pivots, supports) for i in range(m) if i != p and u >> i & 1]
    def apply(x, gates):
        for c, target in gates:
            x ^= ((x >> c) & 1) << target
        return x
    branches = []
    for background in range(1 << m):
        if background & pivot_mask:
            continue
        d = first_dependence(control_columns(program, background), n)
        selected = (d & -d).bit_length()-1
        output = pivots[selected]
        second = [(output, p) for j, p in enumerate(pivots) if j != selected and d >> j & 1]
        for outcome in range(1 << n):
            other_pivots = [p for p in pivots if p != output]
            value = background | sum(((outcome >> j) & 1) << p for j, p in enumerate(other_pivots))
            x = apply(apply(value, reversed(second)), reversed(first))
            y = apply(apply(value | (1 << output), reversed(second)), reversed(first))
            if y != partner(program, x):
                raise ArithmeticError("feedforward receiver differs from nonlinear partner")
            delta = tuple(sum(a*((y >> i & 1)-(x >> i & 1)) for i,a in enumerate(row)) % q for row in A)
            if any(a % 4 for a in delta):
                raise ArithmeticError("feedforward outcome fails mod4 descent")
            branches.append({"first_background_hex": hex(background), "second_outcome": outcome,
                "classical_dependence_hex": hex(d), "output_physical_wire": output,
                "second_stage_CNOTs": [list(gate) for gate in second],
                "oriented_original_endpoints": [x,y], "output_label_hex": [hex(a//4) for a in delta],
                "nonzero_label": any(delta), "original_pair_width": (x ^ y).bit_count(),
                "unconditional_Born_mass": dyadic(Fraction(2,1 << m))})
    return {"first_stage_CNOTs": [list(gate) for gate in first],
            "first_measured_Z_wires": [i for i in range(m) if i not in pivots],
            "logical_pivot_wires": pivots, "branches": branches,
            "first_outcome_bits": m-n-1, "second_outcome_bits": n,
            "output_phase_qubits_per_actual_attempt": 1,
            "classical_feedforward_not_coherent_Gaussian_required": True,
            "census_is_an_executed_quantum_experiment": False,
            "actual_attempt_follows_one_branch_not_all_outcomes": True}


def finite_control(labels, phase_bits=4):
    from theorems.dcp_nonlinear_fiber_pairing import compiler_certificate
    program = make_program(labels)
    m = program["width"]
    if m > 10:
        raise ValueError("UNKNOWN: finite original-input census cap")
    histogram = Counter()
    for x in range(1 << m):
        y = partner(program, x)
        if y == x or partner(program, y) != x or control_columns(program, y) != control_columns(program, x):
            raise ArithmeticError("nonlinear involution/control invariance falsified")
        histogram[(x ^ y).bit_count()] += 1
    return {
        "program": program, "reversible_XOR_F": reversible_evaluator(program),
        "original_assignments_exhausted": 1 << m,
        "physical_direction_width_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "compiler": compiler_certificate(labels, phase_bits, 2, program),
        "CNOT_Z_feedforward_receiver": feedforward_branches(labels, phase_bits, program),
        "coarse_admission_probability": dyadic(Fraction(1)),
        "control_columns_invariant_under_partner": True,
    }


def frontier(n, phase_bits):
    integer(n, "vector dimension", 2, 128)
    integer(phase_bits, "input phase bits", 3, 4096)
    if (phase_bits-1)*(n+1).bit_length() > 12000:
        raise ValueError("UNKNOWN: exact recursive supply ledger work cap")
    m, stages = (n+1)**2, (phase_bits-1)//2
    return {
        "secret_vector_components": n, "phase_bits": phase_bits,
        "original_copies_per_two_bit_output_attempt": m,
        "two_bit_stages_without_overshooting_last_phase_bit": stages,
        "ideal_no_zero_filter_original_copies_after_these_stages": str(m**stages),
        "remaining_phase_bits_after_these_stages": phase_bits-2*stages,
        "ideal_no_failure_copies_including_last_one_bit_stage": str((n+1)**(phase_bits-1)),
        "pure_native_mean_useful_admission": dyadic(1-Fraction(1, 1 << ((phase_bits-2)*n))),
        "per_level_failures_and_fresh_batch_supply_must_be_added": True,
        "all_levels_source_and_noise_composition_certified": False,
        "new_Kuperberg_or_Regev_exponent": False,
        "elementary_evaluator_gate_order": "O(n^3) at m=(n+1)^2, plus reversible relation and ordering checks",
        "one_over_n2_visibility": dyadic(1-Fraction(1,n*n)) if n & (n-1) == 0 else None,
        "one_over_n2_visibility_worst_width_factor": dyadic((1-Fraction(1,n*n))**m) if n & (n-1) == 0 else None,
        "one_over_n_visibility_worst_width_factor": dyadic((1-Fraction(1,n))**m) if n & (n-1) == 0 else None,
        "visibility_factors_are_conservative_lower_bounds_NOT_noise_upper_bounds": True,
    }


def mean_visibility_from_weights(weights, visibility):
    """Exact mean over SECOND low bits, conditioned on parity B and supports.

    The signed half-sum columns are IID uniform in F2^n. This does NOT give
    the law conditional on an already fixed full coarse A modulo4.
    """
    weights = tuple(weights)
    if len(weights) < 2:
        raise ValueError("n+1 nonempty disjoint blocks required")
    for w in weights:
        integer(w, "physical support weight", 1, 4096)
    if type(visibility) not in (Fraction, int) or not 0 <= visibility <= 1:
        raise ValueError("exact visibility in [0,1] required")
    visibility = Fraction(visibility)
    dyadic(visibility)
    n = len(weights)-1
    independent, prior_weight_factor, total = Fraction(1), Fraction(1), Fraction(0)
    rows = []
    for j,w in enumerate(weights):
        probability = independent * Fraction(1, 1 << (n-j))
        conditional = visibility**w * prior_weight_factor
        total += probability * conditional
        rows.append({"first_dependent_column_index": j, "probability": dyadic(probability),
                     "conditional_mean_visibility": dyadic(conditional)})
        independent *= 1-Fraction(1, 1 << (n-j))
        prior_weight_factor *= (1+visibility**w)/2
    return {"physical_support_weights": list(weights), "visibility": dyadic(visibility),
            "first_dependence_law": rows, "native_mean_unfiltered_visibility": dyadic(total),
            "conditioned_on_parity_B_only_not_full_coarse_A": True,
            "support_selection_may_read_second_low_bits": False}


def native_noise_bound(n, visibility):
    integer(n,"native dimension",1,512)
    if type(visibility) not in (Fraction,int) or not 0 <= visibility <= 1:
        raise ValueError("exact independent original visibility required")
    v = Fraction(visibility)
    dyadic(v)
    radius = n//16
    bad = min(Fraction(1),Fraction((n+1)*sum(comb(n+1,w) for w in range(1,radius+1)),1 << n))
    a = v**(radius+1)
    # P[J=j]<=2^(j-n), and all retained block weights exceed radius.
    # The geometric sum includes the cancelling leading factor a exactly.
    good_upper = min(Fraction(1),Fraction(1,1 << n)*((1+a)**(n+1)-1))
    source_upper = bad+(1-bad)*good_upper
    return {"secret_vector_components":n,"original_copies":(n+1)**2,
            "visibility":dyadic(v),"low_block_support_cutoff":radius,
            "some_block_has_a_short_nonempty_kernel_vector_probability_upper_bound":dyadic(bad),
            "mean_visibility_given_no_short_block_upper_bound":dyadic(good_upper),
            "native_mean_unfiltered_visibility_upper_bound":dyadic(source_upper),
            "support_selection_is_parity_only_and_blocks_are_disjoint":True,
            "second_low_label_bits_and_original_Z_background_are_averaged":True,
            "fixed_full_coarse_matrix_inherits_this_probability_bound":False,
            "arbitrary_partial_or_collective_pairing_covered":False,
            "noise_promise":"independent balanced ORIGINAL-register dephasing"}


def build_report():
    small = finite_control(((1, 1, 1, 1),))
    rng = Random(6621)
    labels = tuple(tuple(rng.randrange(32) for _ in range(9)) for _ in range(2))
    medium = finite_control(labels, 5)
    # Explicit selected low columns, NOT an IID-native probability sample.
    A = tuple(tuple(((i+1) >> l & 1) + 2*((i+l) % 2) for i in range(49)) for l in range(6))
    program = make_program(A)
    inputs = [0, (1 << 49)-1] + [rng.getrandbits(49) for _ in range(30)]
    probes = []
    for x in inputs:
        y = partner(program, x)
        if y == x or partner(program, y) != x or control_columns(program, y) != control_columns(program, x):
            raise ArithmeticError("large-width reciprocity control failed")
        probes.append({"input_hex": hex(x), "partner_hex": hex(y)})
    return {
        "contract_id": CONTRACT_ID, "status": "LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING",
        "accepted_speedup_candidate": False, "novelty_claim": False,
        "external_theorem_review_complete": False, "source_quantum_preparations_executed": 0,
        "finite_controls": [small, medium],
        "parity_conditioned_noise_means": [mean_visibility_from_weights(
            [int(u,16).bit_count() for u in C["program"]["disjoint_supports_hex"]],Fraction(3,4))
            for C in (small,medium)],
        "selected_global_nonaffine_control": {"selection": "explicit distinct nonzero signatures, NOT IID",
            "signature_certificate": signature_certificate(A), "program": program, "sampled_original_inputs": probes,
            "nonaffinity_follows_from_global_rigidity_not_probe_statistics": True},
        "supply_and_noise_frontiers": [frontier(n, n) for n in (4, 8, 16, 32)],
        "native_noise_upper_frontiers": [native_noise_bound(n,v) for n in (32,64,128,256)
                                          for v in (Fraction(1,4),1-Fraction(1,n),1-Fraction(1,n*n))],
        "scope": {
            "coarse_only_uniform_higher_label_theorem_applies_with_fresh_batches": True,
            "uniformity_conditioned_on_old_full_A": False,
            "original_higher_label_transcript_must_be_discarded": True,
            "pure_zero_label_injection_backend_supplied": False,
            "arbitrary_correlated_noise_covered": False,
            "coherent_Gaussian_control_is_free": False,
            "elementary_reversible_gate_lists_exported_for_bounded_controls": True,
            "polynomial_supply_for_growing_phase_bits": False,
            "matched_classical_hardness_or_speedup_established": False,
            "improves_known_Gaussian_or_isotropic_asymptotics": False,
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "finite_controls": 2,
                      "polynomial_coarse_only_evaluator": True, "new_sieve_exponent": False,
                      "artifact": str(REPORT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
