"""Full binary carry-polar operators and scoped fixed-pivot-span obstructions.

LOCAL DERIVATION / REVIEW PENDING. Neither a decoder nor a general DCP no-go.
No assignments, secrets or exponentially many spans are searched by extraction.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact
from dcp_carry_packets import compile_packet, isotropic_readout_rows
from dcp_conditional_carry_features import _solve, pivot_pencil_coverage_certificate
from dcp_lowbit_fiber_normalizer import _apply_rows, _columns_value, _independent_extension

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_pivot_span_obstructions.json"
DIMENSION_THEOREM = "https://arxiv.org/pdf/1004.0579"


def _row_basis(rows, width):
    pivots = {}
    for row in rows:
        if type(row) is not int or not 0 <= row < 1 << width:
            raise ValueError("binary row outside declared width")
        for p in sorted(pivots, reverse=True):
            if row >> p & 1:
                row ^= pivots[p]
        if row:
            pivots[row.bit_length() - 1] = row
    for p in sorted(pivots):
        for q in sorted(pivots):
            if q > p and pivots[q] >> p & 1:
                pivots[q] ^= pivots[p]
    return tuple(pivots[p] for p in sorted(pivots))


def _nullspace(rows, width):
    basis = _row_basis(rows, width)
    pivots = {row.bit_length() - 1 for row in basis}
    return tuple((1 << j) | sum(((row >> j) & 1) << (row.bit_length() - 1) for row in basis)
                 for j in range(width) if j not in pivots)


def _flatten(rows, width):
    return sum(row << (width * l) for l, row in enumerate(rows))


def _restriction(rows, directions):
    return tuple(sum(((row & w).bit_count() & 1) << j for j, w in enumerate(directions)) for row in rows)


@dataclass(frozen=True)
class PolarOperatorFamily:
    input_bits: int
    constant_rows: tuple[int, ...]
    variation_rows: tuple[tuple[int, ...], ...]

    def __post_init__(self):
        d, n = self.input_bits, len(self.constant_rows)
        if type(d) is not int or d < n or not n:
            raise ValueError("positive output dimension and input width at least n required")
        if any(len(M) != n or any(type(row) is not int or not 0 <= row < 1 << d for row in M)
               for M in (self.constant_rows, *self.variation_rows)):
            raise ValueError("rectangular binary operator rows required")

    @property
    def dimension(self):
        return len(self.constant_rows)

    @property
    def background_bits(self):
        return len(self.variation_rows)

    @property
    def operators(self):
        return tuple(tuple(M[l] for M in self.variation_rows) for l in range(self.dimension))

    def matrix(self, background):
        if type(background) is not int or not 0 <= background < 1 << self.background_bits:
            raise ValueError("background outside actual parameter domain")
        return _actual_matrix(self, background)

    def record(self):
        return {"input_bits": self.input_bits, "dimension": self.dimension,
                "background_bits": self.background_bits,
                "constant_rows_hex": [hex(x) for x in self.constant_rows],
                "variation_rows_hex": [[hex(x) for x in M] for M in self.variation_rows],
                "polar_operators_rows_hex": [[hex(x) for x in D] for D in self.operators],
                "operator_convention": "D_l maps input U coefficients to background covector; rows indexed by V",
                "decoder_or_candidate": False}


def _actual_matrix(family, background):
    rows = list(family.constant_rows)
    for i, M in enumerate(family.variation_rows):
        if background >> i & 1:
            rows = [a ^ b for a, b in zip(rows, M)]
    return tuple(rows)


def packet_polar_operator_family(packet, isotropic_directions):
    if packet.modulus < 8 or packet.syndrome or len(packet.pivots) != packet.dimension:
        raise ValueError("full-rank zero-origin packet with q>=8 required")
    U, n, k = tuple(isotropic_directions), packet.dimension, packet.retained_qubits
    if len(U) < n:
        raise ValueError("isotropic chart must have at least n directions")
    low = compile_packet([[a % 4 for a in row] for row in packet.labels], 4)
    slopes = isotropic_readout_rows(low, U)
    V = _independent_extension(U, k)[len(U):]
    constant = tuple(sum((slope >> l & 1) << j for j, slope in enumerate(slopes)) for l in range(n))
    variations = []
    for v in V:
        c = low.residual(v)
        columns = [sum((a ^ b) << l for l, (a, b) in enumerate(zip(low.residual(v ^ u), c)))
                   ^ slope for u, slope in zip(U, slopes)]
        variations.append(tuple(sum((column >> l & 1) << j for j, column in enumerate(columns)) for l in range(n)))
    family = PolarOperatorFamily(len(U), constant, tuple(variations))
    return family, {"actual_packet_operator_family": True,
                    "labels": packet.labels, "modulus": packet.modulus, "logical_width": k,
                    "isotropic_directions_hex": [hex(u) for u in U],
                    "complement_directions_hex": [hex(v) for v in V],
                    "variation_selected_from_binary_labels_only": True,
                    "constant_part_depends_on_middle_label_bits": True,
                    "input_assignments_or_secret_states_enumerated": False,
                    "native_source_prevalence_verified": False}


def complete_row_block_certificate(family):
    """Largest E with F2^n tensor E contained in the background matrix image."""
    n, d, b = family.dimension, family.input_bits, family.background_bits
    generators = [_flatten(M, d) for M in family.variation_rows]
    image = _row_basis(generators, n * d)
    annihilator = _nullspace(image, n * d)
    constraints = _row_basis(((a >> (l * d)) & ((1 << d) - 1)
                              for a in annihilator for l in range(n)), d)
    E = _nullspace(constraints, d)
    witnesses = []
    for e in E:
        row_witnesses = []
        for l in range(n):
            target = e << (d * l)
            equations = [(sum(((M >> j) & 1) << i for i, M in enumerate(generators)), target >> j & 1)
                         for j in range(n * d)]
            _, y = _solve(equations, b)
            assert y is not None and _columns_value(generators, y) == target
            row_witnesses.append(hex(y))
        witnesses.append(row_witnesses)
    codim_E = len(constraints)
    restricted_rank_floor = max(0, n - codim_E)
    fraction_bound = math.prod(1 - Fraction(1, 1 << j) for j in range(1, restricted_rank_floor + 1))
    dimension_floor = max(0, len(image) - n * (d - n))
    dimension_excluded = dimension_floor > n * (n - 1) // 2
    if dimension_excluded:
        fraction_bound = min(fraction_bound, 1 - Fraction(1, 1 << n))
    return {"status": "MAXIMAL_COMPLETE_ROW_BLOCK_AND_ALL_FIXED_SPANS_NECESSARY_GATE",
            "background_matrix_image_dimension": len(image),
            "matrix_image_annihilator_basis_hex": [hex(x) for x in annihilator],
            "complete_row_block_basis_hex": [hex(x) for x in E],
            "complete_row_block_dimension": len(E), "complete_row_block_codimension": codim_E,
            "complete_row_block_background_witnesses_hex": witnesses,
            "annihilator_row_span_basis_hex": [hex(x) for x in constraints],
            "eligible_exact_fixed_pivot_span_must_annihilate_complete_row_block": True,
            "every_n_dimensional_span_complete_block_rank_lower_bound": restricted_rank_floor,
            "every_n_dimensional_span_variation_image_dimension_lower_bound": dimension_floor,
            "all_fixed_n_dimensional_spans_excluded_by_complete_block": restricted_rank_floor > 0,
            "all_fixed_n_dimensional_spans_excluded_by_dimension_theorem": dimension_excluded,
            "all_fixed_spans_uniform_background_invertibility_fraction_upper_bound": exact(fraction_bound),
            "dimension_theorem": {"source": DIMENSION_THEOREM, "theorem": 9,
                                  "field": "arbitrary field, including F2",
                                  "maximum_nonsingular_affine_dimension": n * (n - 1) // 2,
                                  "classification_for_larger_fields_used": False},
            "background_uniformity_and_fixed_W_required_for_fraction_bound": True,
            "background_adaptive_pivots_or_other_isotropic_charts_excluded": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def weighted_radical_span_screen(family, *, combination_cap=4095):
    n, d = family.dimension, family.input_bits
    if type(combination_cap) is not int or combination_cap < 0:
        raise ValueError("nonnegative explicit combination budget required")
    required = (1 << n) - 1
    if required > combination_cap:
        return {"status": "SKIPPED_EXPONENTIAL_WEIGHTED_COMBINATION_MENU",
                "required_combinations_decimal": str(required), "combination_cap": combination_cap,
                "all_fixed_spans_excluded": False, "skipped_is_a_mathematical_negative_result": False}
    records, generators = [], []
    for weight in range(1, 1 << n):
        rows = [0] * family.background_bits
        for l, D in enumerate(family.operators):
            if weight >> l & 1:
                rows = [a ^ b for a, b in zip(rows, D)]
        radical = _nullspace(rows, d)
        generators.extend(radical)
        records.append({"output_weight_hex": hex(weight), "radical_basis_hex": [hex(x) for x in radical]})
    span = _row_basis(generators, d)
    return {"status": "EXACT_BOUNDED_WEIGHTED_RADICAL_SPAN_NECESSARY_GATE",
            "combinations_evaluated": required, "combination_cap": combination_cap,
            "weighted_radicals": records, "eligible_direction_span_basis_hex": [hex(x) for x in span],
            "eligible_direction_span_dimension": len(span), "all_fixed_spans_excluded": len(span) < n,
            "necessary_gate_pass_proves_an_eligible_n_dimensional_pivot_span_exists": False,
            "enumerating_weight_combinations_is_polynomial_in_unbounded_n": False,
            "general_decoder_no_go": False, "speedup_claim_allowed": False}


def physical_schur_product_certificate(packet, logical_directions):
    if packet.syndrome or len(packet.pivots) != packet.dimension:
        raise ValueError("full-rank zero-origin physical code required")
    n, m, k, W = packet.dimension, packet.input_qubits, packet.retained_qubits, tuple(logical_directions)
    if len(W) != n or len(_row_basis(W, k)) != n:
        raise ValueError("n independent logical directions required")
    low = compile_packet([[a & 1 for a in row] for row in packet.labels], 4)
    isotropic_readout_rows(low, W)
    dual = tuple(sum((a & 1) << i for i, a in enumerate(row)) for row in packet.labels)
    physical = tuple(sum(x << i for i, x in enumerate(packet.assignment(w))) for w in W)
    products = tuple(b & w for w in physical for b in dual)
    quotient_dimension = len(_row_basis((*dual, *products), m)) - n
    column_ranks = [len(_row_basis((*dual, *(b & w for b in dual)), m)) - n for w in physical]
    used = 0
    disjoint = True
    for w in physical:
        disjoint &= used & w == 0
        used |= w
    outside_columns = [sum((b >> i & 1) << l for l, b in enumerate(dual)) for i in range(m) if not used >> i & 1]
    outside_rank = len(_row_basis(outside_columns, n))
    separated = disjoint and outside_rank == n
    if separated:
        assert quotient_dimension == sum(column_ranks)
    return {"status": "EXACT_PHYSICAL_CODE_SCHUR_PRODUCT_REFORMULATION",
            "physical_pivot_directions_hex": [hex(w) for w in physical],
            "dual_code_rows_hex": [hex(b) for b in dual],
            "polar_variation_dimension": quotient_dimension,
            "identity": "dim(C_perp + C_perp*W_physical)-n; * is coordinatewise product",
            "individual_column_variation_dimensions": column_ranks,
            "disjoint_physical_supports": bool(disjoint), "unused_physical_columns_binary_rank": outside_rank,
            "disjoint_support_and_unused_full_rank_certify_column_separability": separated,
            "all_constant_parts_excluded_by_disjoint_support_gate": separated and all(column_ranks),
            "selected_span_excluded_by_nonsingular_dimension_bound": quotient_dimension > n * (n - 1) // 2,
            "low_product_dimension_proves_a_nonsingular_pencil_exists": False,
            "all_code_subspaces_or_quantum_decoders_excluded": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def selected_pivot_span_certificate(family, directions):
    n, d = family.dimension, family.input_bits
    W = tuple(directions)
    if len(W) != n or len(_row_basis(W, d)) != n:
        raise ValueError("exactly n independent directions in the supplied U chart required")
    constant = _restriction(family.constant_rows, W)
    variations = tuple(_restriction(M, W) for M in family.variation_rows)
    selected = PolarOperatorFamily(n, constant, variations)
    core = complete_row_block_certificate(selected)
    coverage = pivot_pencil_coverage_certificate(constant, variations)
    rank = core["background_matrix_image_dimension"]
    dimension_excluded = rank > n * (n - 1) // 2
    probes = list(W) + [u ^ v for u, v in itertools.combinations(W, 2)]
    witness, surjective_checks = None, 0
    for w in probes:
        images = [_apply_rows(M, w) for M in family.variation_rows]
        if len(_row_basis(images, n)) != n:
            continue
        surjective_checks += 1
        target = _apply_rows(family.constant_rows, w)
        equations = [(sum(((value >> l) & 1) << i for i, value in enumerate(images)), target >> l & 1)
                     for l in range(n)]
        _, background = _solve(equations, family.background_bits)
        assert background is not None and _apply_rows(_actual_matrix(family, background), w) == 0
        witness = {"input_direction_hex": hex(w), "background_mask_hex": hex(background)}
        break
    excluded = dimension_excluded or core["complete_row_block_dimension"] > 0 or witness is not None or coverage["singular_background_mask_hex"] is not None
    fraction_upper = Fraction(1)
    if excluded:
        fraction_upper = 1 - Fraction(1, 1 << min(n, rank))
    if core["complete_row_block_dimension"]:
        fraction_upper = min(fraction_upper, math.prod(1 - Fraction(1, 1 << j)
                             for j in range(1, core["complete_row_block_dimension"] + 1)))
    if coverage["exact_uniform_background_invertibility_fraction"] is not None:
        fraction = coverage["exact_uniform_background_invertibility_fraction"]
        fraction_upper = min(fraction_upper, Fraction(fraction["sign"] * int(fraction["numerator_hex"], 16),
                                                     int(fraction["denominator_hex"], 16)))
    return {"status": "ACTUAL_SELECTED_SPAN_NECESSARY_OBSTRUCTIONS_NOT_DECODER",
            "directions_in_U_coordinates_hex": [hex(w) for w in W],
            "restricted_operator_family": selected.record(), "complete_row_block": core,
            "pencil_coverage": coverage, "dimension_theorem_excludes_every_constant_part": dimension_excluded,
            "all_backgrounds_invertible_excluded": excluded,
            "surjective_direction_background_witness": witness,
            "deterministic_direction_probe_menu_size": len(probes),
            "successful_surjective_probes_before_stopping": surjective_checks,
            "uniform_background_invertibility_fraction_upper_bound": exact(fraction_upper),
            "nonzero_determinant_complement_boolean_degree_upper_bound": min(n, rank),
            "no_obstruction_is_a_success_proof": False,
            "fixed_span_may_depend_on_middle_labels_but_not_on_background": True,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def run_controls():
    correlated = PolarOperatorFamily(2, (2, 3), ((1, 2),))
    full = PolarOperatorFamily(3, (1, 4), ((1, 0), (2, 0), (0, 1), (0, 2)))
    triangular = PolarOperatorFamily(2, (1, 2), ((2, 0),))
    dimension_only = PolarOperatorFamily(3, (1, 2, 4), ((3, 0, 0), (0, 6, 0), (0, 0, 5), (1, 2, 4)))
    abstract = []
    for name, family, W in (("binary_correlated_nonsingular_countercontrol", correlated, (1, 2)),
                             ("one_unused_coordinate_cannot_hide_complete_two_column_block", full, (1, 4)),
                             ("strict_triangular_positive_countercontrol", triangular, (1, 2)),
                             ("correlated_high_dimension_gate", dimension_only, (1, 2, 4))):
        abstract.append({"name": name, "operator_family": family.record(),
                         "all_span_certificate": complete_row_block_certificate(family),
                         "weighted_radical_screen": weighted_radical_span_screen(family),
                         "selected_span_certificate": selected_pivot_span_certificate(family, W),
                         "control_is_an_algorithm_candidate": False})
    source = json.loads((ROOT / "research/phase_workbench/dcp_conditional_carry_features.json").read_text())
    packets = []
    for row in source["systematic_packet_pencil_profiles"]:
        packet = compile_packet(row["labels"], row["modulus"])
        family, provenance = packet_polar_operator_family(packet, [int(u, 16) for u in row["isotropic_directions_hex"]])
        first = tuple(1 << j for j in range(family.dimension))
        physical_first = tuple(int(x, 16) for x in provenance["isotropic_directions_hex"][:family.dimension])
        schur = physical_schur_product_certificate(packet, physical_first)
        selected = selected_pivot_span_certificate(family, first)
        assert schur["polar_variation_dimension"] == selected["complete_row_block"]["background_matrix_image_dimension"]
        packets.append({"operator_family": family.record(), "provenance": provenance,
                        "source_scope": "systematic fixed-prefix finite profile; not an unconditional native success estimate",
                        "all_span_certificate": complete_row_block_certificate(family),
                        "weighted_radical_screen": weighted_radical_span_screen(family),
                        "physical_code_schur_certificate": schur,
                        "first_basis_pivot_span_certificate": selected})
    positive = compile_packet([[1, 0, 3, 2, 1], [0, 1, 2, 1, 1]], 8)
    family, provenance = packet_polar_operator_family(positive, (1, 2))
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "abstract_countercontrols": abstract,
            "native_correlated_positive_packet": {"operator_family": family.record(), "provenance": provenance,
                                                  "physical_code_schur_certificate": physical_schur_product_certificate(positive, (1, 2)),
                                                  "certificate": selected_pivot_span_certificate(family, (1, 2))},
            "systematic_actual_packet_operator_profiles": packets,
            "claim_gate": {"full_polar_operators_exported_without_assignment_enumeration": True,
                           "polynomial_all_span_complete_block_and_dimension_gates": True,
                           "weighted_radical_menu_charged_as_exponential": True,
                           "all_isotropic_charts_or_background_adaptive_pivots_ruled_out": False,
                           "full_growing_modulus_decoder_implemented": False,
                           "independent_theorem_review": False, "novelty_claim": False,
                           "candidate_record_accepted": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_conditional_carry_features.py",
                                            ROOT / "theorems/dcp_lowbit_fiber_normalizer.py", ROOT / "theorems/dcp_carry_packets.py",
                                            ROOT / "research/phase_workbench/dcp_conditional_carry_features.json")}}


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
