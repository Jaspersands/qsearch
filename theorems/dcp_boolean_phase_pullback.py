"""Consumed phase programs for source-faithful public Boolean pullbacks.

LOCAL DERIVATION / REVIEW PENDING. Known stochastic phase injection, not a new
algorithm or a reusable hidden-phase oracle. Each program is consumed once.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact
from dcp_carry_packets import compile_packet

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_boolean_phase_pullback.json"


@dataclass(frozen=True)
class BooleanANFMap:
    """Public Boolean map as XORs of monomials, not a truth-table oracle."""
    input_bits: int
    outputs: tuple[tuple[int, ...], ...]

    def __post_init__(self):
        if type(self.input_bits) is not int or self.input_bits < 1 or not self.outputs:
            raise ValueError("positive input width and nonempty public map required")
        for terms in self.outputs:
            if len(set(terms)) != len(terms) or any(type(mask) is not int or not 0 <= mask < 1 << self.input_bits for mask in terms):
                raise ValueError("canonical distinct valid ANF monomial masks required")
        object.__setattr__(self, "outputs", tuple(tuple(terms) for terms in self.outputs))

    def evaluate(self, assignment):
        if type(assignment) is not int or not 0 <= assignment < 1 << self.input_bits:
            raise ValueError("Boolean assignment out of range")
        return tuple(sum((assignment & mask) == mask for mask in terms) & 1 for terms in self.outputs)

    def resource_upper_bound(self):
        terms = [mask for output in self.outputs for mask in output]
        degree = max((mask.bit_count() for mask in terms), default=0)
        # One product chain per monomial, XOR its result into an accumulator,
        # then uncompute the chain. The whole Boolean evaluator is undone too.
        compute_toffoli = sum(2 * max(0, mask.bit_count() - 1) for mask in terms)
        compute_cnot = sum(mask != 0 for mask in terms)
        compute_x = sum(mask == 0 for mask in terms)
        return {"description_size_monomials": len(terms), "maximum_anf_degree": degree,
                "compute_uncompute_toffoli_upper_bound": 2 * compute_toffoli,
                "compute_uncompute_cnot_upper_bound": 2 * compute_cnot,
                "compute_uncompute_x_upper_bound": 2 * compute_x,
                "reusable_clean_work_qubits_upper_bound": 1 + max(0, degree - 1),
                "physical_gate_backend_exported": False}


def packet_pullback_functions(packet, public_map):
    """f_i(z)=(K h(z))_i. K and h must precede current high labels/signs."""
    if len(public_map.outputs) != packet.retained_qubits:
        raise ValueError("public map output width must equal packet logical width")
    functions = []
    for row in packet.kernel_rows:
        terms = set()
        for j, output in enumerate(public_map.outputs):
            if row >> j & 1:
                terms.symmetric_difference_update(output)
        functions.append(tuple(sorted(terms)))
    return BooleanANFMap(public_map.input_bits, tuple(functions))


def consumed_program_plan(labels, modulus, functions):
    labels = tuple(tuple(int(a) % modulus for a in row) for row in labels) if modulus > 0 else ()
    if modulus < 4 or modulus & (modulus - 1) or not labels or not labels[0] or any(len(row) != len(functions.outputs) for row in labels):
        raise ValueError("power-of-two modulus>=4 and labels matching every consumed program required")
    resources = functions.resource_upper_bound()
    return {"status": "CONSUMED_PROGRAM_INSTRUMENT_NOT_REUSABLE_ORACLE", "modulus": modulus,
            "dimension": len(labels), "public_labels": labels, "target_qubits": functions.input_bits,
            "public_boolean_anf_functions_hex": [[hex(term) for term in f] for f in functions.outputs],
            "program_phase_states_consumed": len(functions.outputs),
            "program_measurements_in_Z": len(functions.outputs),
            "boolean_accumulator_to_program_cnots": len(functions.outputs),
            "public_evaluator_resources": resources,
            "operations": ["compute_public_f_i_into_clean_accumulator",
                           "CNOT_accumulator_to_supplied_program_i",
                           "measure_program_i_in_Z_and_record_b_i",
                           "uncompute_public_f_i_and_reuse_clean_accumulator",
                           "replace_label_column_i_by_(-1)^b_i_times_original_column_i"],
            "one_step_kraus_identity": "K_b(z)=2^-1/2 exp(i theta b) exp(i(-1)^b theta f(z))",
            "branch_probability": "2^-m_independent_of_secret_labels_and_target_state_for_phase_only_programs",
            "all_outcomes_kept": True, "postselection_used": False,
            "secret_dependent_rotation_or_inverse_used": False,
            "same_program_or_phase_function_reusable": False,
            "all_input_bit_noise_models_covered": False,
            "physical_controlled_gate_precision_and_backend_verified": False,
            "unknown_residue_decoder": False, "speedup_claim_allowed": False}


def signed_label_update(labels, modulus, outcomes):
    if type(outcomes) is not int or not labels or not labels[0] or not 0 <= outcomes < 1 << len(labels[0]):
        raise ValueError("valid measured-program outcome mask required")
    return tuple(tuple((-a if outcomes >> i & 1 else a) % modulus for i, a in enumerate(row)) for row in labels)


def canonical_label_sign_orbits(labels, modulus):
    if modulus < 4 or modulus & (modulus - 1) or not labels or not labels[0] or any(len(row) != len(labels[0]) for row in labels):
        raise ValueError("nonempty rectangular labels and power-of-two modulus>=4 required")
    representatives = []
    for i in range(len(labels[0])):
        a = tuple(row[i] % modulus for row in labels)
        representatives.append(min(a, tuple(-x % modulus for x in a)))
    return tuple(representatives)


def sign_orbit_selector_certificate(labels, modulus):
    representatives = canonical_label_sign_orbits(labels, modulus)
    sizes = [1 if all(2 * x % modulus == 0 for x in column) else 2 for column in representatives]
    return {"status": "SIGN_ORBIT_INVARIANT_SELECTOR_SOURCE_IDENTITY",
            "canonical_public_sign_orbit_columns": representatives,
            "conditional_column_orbit_sizes": sizes,
            "allowed_selector": "arbitrary_public_function_of_all_canonical_sign_orbits_and_prior_only",
            "conditional_source": "independent_uniform_sign_orbit_elements_per_column_not_uniform_higher_labels",
            "native_unconditional_updated_label_law_preserved": True,
            "selector_recomputed_on_updated_labels_equals_preinjection_selector": True,
            "conditional_higher_labels_are_iid_uniform": False,
            "old_fixed_low_chart_high_label_moment_theorem_automatically_usable": False,
            "cost_or_success_of_a_particular_selector_proved": False,
            "new_hidden_phase_queries_or_copies_available": False,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def source_universal_product_gate(functions, modulus):
    """Exact flat phase-product test with f FIXED across all higher labels.

    Varying one original coefficient by 2 forces every mixed integer Boolean
    derivative to vanish mod(q/2). For q>=8 its magnitude<=2, hence it vanishes
    literally. A Boolean real-affine function is constant or a single literal.
    """
    if type(modulus) is not int or modulus < 8 or modulus & (modulus - 1):
        raise ValueError("source-universal literal necessity requires power-of-two q>=8")
    failures = []
    for i, terms in enumerate(functions.outputs):
        nonconstant = [mask for mask in terms if mask != 0]
        if len(nonconstant) > 1 or any(mask.bit_count() != 1 for mask in nonconstant):
            failures.append(i)
    return {"status": "LOCAL_SOURCE_UNIVERSAL_PHASE_PRODUCT_CRITERION_REVIEW_PENDING",
            "modulus": modulus, "source_universal_phase_product": not failures,
            "nonliteral_physical_coordinate_functions": failures,
            "requires_functions_fixed_across_all_current_higher_label_tables": True,
            "criterion": "every_physical_boolean_function_is_constant_or_one_possibly_complemented_variable",
            "proof": "all_secret_and_higher_label_product_phases_force_mixed_derivatives_zero_mod_q_over_2_then_zero_in_Z",
            "fixed_degree_or_low_anf_degree_alone_suffices": False,
            "high_label_adaptive_or_sign_orbit_selected_functions_covered": False,
            "general_measurements_or_nonproduct_decoders_closed": False,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def pullback_source_gate(*, functions_selected_from_low_labels_or_prior_only=False,
                         current_higher_labels_native_iid=False,
                         independent_phase_only_programs=False,
                         each_program_consumed_once=False,
                         outcome_conditioning_or_rejection=False):
    declarations = {"selector_precedes_current_higher_labels_and_program_outcomes": functions_selected_from_low_labels_or_prior_only,
                    "native_iid_current_higher_labels": current_higher_labels_native_iid,
                    "independent_phase_only_programs": independent_phase_only_programs,
                    "each_program_consumed_once": each_program_consumed_once}
    issues = [name + " is not established" for name, value in declarations.items() if not value]
    if outcome_conditioning_or_rejection:
        issues.append("outcome selection needs its own source and consumption ledger")
    return {"status": "CONDITIONAL_SIGN_COVARIANT_SOURCE_GATE_NOT_PROVEN_REDUCTION",
            "native_updated_source_certified_as_declared": not issues, "issues": issues,
            "declarations_programmatically_proven": False,
            "high_label_selected_functions_automatically_native": False,
            "repeated_same_function_queries_available": False, "candidate_record_accepted": False,
            "speedup_claim_allowed": False}


def _physical_instrument_controls():
    # Physical exponent equality is exact at growing q; no floating amplitudes.
    rows = []
    for q in (8, 16, 128):
        checks = 0
        for theta, outcome, fx, fy in itertools.product(range(q), range(2), range(2), range(2)):
            lhs = theta * ((outcome ^ fx) - (outcome ^ fy)) % q
            rhs = (-1 if outcome else 1) * theta * (fx - fy) % q
            assert lhs == rhs
            checks += 1
        rows.append({"modulus": q, "exact_density_phase_identities": checks,
                     "every_branch_kraus_norm_squared": exact(Fraction(1, 2)),
                     "target_can_be_entangled_with_an_untouched_reference": True})
    return rows


def _complete_pullback_control():
    # Actual supplied-state circuit, bounded exact exponent checks only.
    public_map = BooleanANFMap(2, ((1,), (3,)))
    functions = packet_pullback_functions(compile_packet([[1, 0, 1]], 8), public_map)
    checks, updated_counts = 0, Counter()
    for high in itertools.product(range(4), repeat=3):
        labels = [[1 + 2 * high[0], 2 * high[1], 1 + 2 * high[2]]]
        for outcome in range(8):
            updated = signed_label_update(labels, 8, outcome)
            updated_counts[updated[0]] += 1
            packet = compile_packet(updated, 8)
            assert packet.kernel_rows == (2, 1, 2)
            for secret, z in itertools.product(range(8), range(4)):
                f = functions.evaluate(z)
                branch = sum(labels[0][i] * ((outcome >> i & 1) ^ f[i]) for i in range(3))
                global_phase = sum(labels[0][i] * (outcome >> i & 1) for i in range(3))
                pullback = sum(updated[0][i] * f[i] for i in range(3))
                assert secret * (branch - global_phase - pullback) % 8 == 0
                assert pullback % 2 == 0
                logical = sum(bit << i for i, bit in enumerate(public_map.evaluate(z)))
                assert pullback // 2 % 4 == packet.residual(logical)[0]
                checks += 1
    # The map is deliberately nonlinear and not injective: no inverse is used.
    image = [public_map.evaluate(z) for z in range(4)]
    assert len(set(image)) < 4
    assert len(updated_counts) == 64 and set(updated_counts.values()) == {8}
    return {"modulus": 8, "all_higher_label_tables": 64, "all_program_outcomes": 8,
            "exact_branch_and_packet_pullback_checks": checks,
            "all_updated_higher_label_tables": len(updated_counts),
            "updated_table_multiplicity_from_all_branches": 8,
            "map_anf_hex": [[hex(t) for t in output] for output in public_map.outputs],
            "map_is_injective": False, "public_map_inverse_required": False,
            "compiled_functions_hex": [[hex(t) for t in output] for output in functions.outputs],
            "resource_plan": consumed_program_plan([[1, 0, 1]], 8, functions),
            "bounded_controls_are_not_algorithmic_advantage_evidence": True}


def _selector_source_controls():
    unconditional, orbit_selected, unsafe_selected = Counter(), Counter(), Counter()
    for label, outcome in itertools.product(range(8), range(2)):
        updated = signed_label_update([[label]], 8, outcome)[0][0]
        unconditional[updated] += 1
        before = canonical_label_sign_orbits([[label]], 8)
        after = canonical_label_sign_orbits([[updated]], 8)
        assert before == after
        if before == ((3,),):
            orbit_selected[updated] += 1
        if label < 4:
            unsafe_selected[updated] += 1
    assert set(unconditional.values()) == {2}
    assert orbit_selected == {3: 2, 5: 2}
    assert [unsafe_selected[i] for i in range(8)] == [2, 1, 1, 1, 0, 1, 1, 1]
    return {"modulus": 8, "all_original_label_sign_pairs": 16,
            "unconditional_updated_label_counts": [unconditional[i] for i in range(8)],
            "safe_sign_orbit_selected_3_counts": [orbit_selected[i] for i in range(8)],
            "unsafe_original_label_less_than_4_counts": [unsafe_selected[i] for i in range(8)],
            "sign_covariance_allows_higher_label_selection_but_not_old_iid_moments": True}


def run_controls():
    width = 64
    public_map = BooleanANFMap(width, ((1,), (1 << 63,), (1 | (1 << 63),)))
    good = {"functions_selected_from_low_labels_or_prior_only": True,
            "current_higher_labels_native_iid": True, "independent_phase_only_programs": True,
            "each_program_consumed_once": True}
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "physical_instruments": _physical_instrument_controls(),
            "complete_nonlinear_packet_pullback": _complete_pullback_control(),
            "scalable_public_map_control": {"input_bits": width, "description": public_map.resource_upper_bound(),
                                             "output_at_both_extreme_bits": public_map.evaluate(1 | (1 << 63)),
                                             "truth_table_enumeration_used": False},
            "source_gates": [pullback_source_gate(**good), pullback_source_gate(),
                             pullback_source_gate(**{**good, "functions_selected_from_low_labels_or_prior_only": False}),
                             pullback_source_gate(**good, outcome_conditioning_or_rejection=True)],
            "sign_orbit_selector_source": sign_orbit_selector_certificate([[1, 3, 4], [2, 5, 0]], 8),
            "selector_source_controls": _selector_source_controls(),
            "nonlinear_product_falsifier": source_universal_product_gate(
                BooleanANFMap(2, ((1,), (3,))), 8),
            "literature": [{"id": "ARXIV-quant-ph-0102037",
                            "url": "https://arxiv.org/abs/quant-ph/0102037",
                            "scope": "Known stochastic U(1) program-state processing; not a DCP decoder or repeated random-label access theorem."}],
            "claim_gate": {"nonlinear_public_pullback_uses_supplied_states_not_their_inverse": True,
                           "random_signed_programs_create_a_reusable_phase_oracle": False,
                           "multiple_copies_of_one_packet_prepared": False,
                           "uniform_source_assumed_after_high_label_dependent_selection": False,
                           "nonlinear_pullback_is_an_independent_phase_qubit_factory": False,
                           "independent_theorem_review": False, "novelty_claim": False,
                           "unknown_residue_decoder": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_carry_packets.py",
                                            ROOT / "theorems/dcp_bell_inference_kernel.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "claim_gate": report["claim_gate"]}, indent=2))


if __name__ == "__main__":
    main()
