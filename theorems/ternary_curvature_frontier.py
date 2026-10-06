"""Sharp scalar curvature geometry and exact joint full-root source replay.

LOCAL DERIVATIONS / REVIEW PENDING. An optimal low-curvature frame is NOT
a full-root product-state compiler, recursive decoder, or general lower bound.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations, product
import json
import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parents[1]
_CORE = _ROOT / "core"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))

from flint import nmod_mat
import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_cyclic_extractor import _integer, _vectors, curvatures, random_even_source

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_curvature_frontier.json"


def _columns(columns, width):
    columns = tuple(tuple(v) for v in columns)
    if any(len(v) != width or any(type(x) is not int or x not in (0, 1, 2) for x in v) for v in columns):
        raise ValueError("canonical F3 columns of source width required")
    if columns and nmod_mat([[v[i] for v in columns] for i in range(width)], 3).rank() != len(columns):
        raise ValueError("independent retained columns required")
    return columns


def curvature_certificate(vectors, columns):
    vectors = _vectors(vectors); columns = _columns(columns, len(vectors))
    grams = tuple(tuple(tuple(sum(vectors[i][l]*u[i]*v[i] for i in range(len(vectors))) % 3
                              for v in columns) for u in columns) for l in range(len(vectors[0])))
    return {"source_width": len(vectors), "secret_dimension": len(vectors[0]),
            "retained_width": len(columns), "columns": columns, "component_Gram_matrices": grams,
            "low_phase_affine_on_every_measured_complement": not any(x for G in grams for row in G for x in row),
            "full_root_product_output_certified": False}


def scalar_witt_dimension(curvature):
    curvature = tuple(curvature)
    _vectors([(x,) for x in curvature])
    zeros, ones, twos = (curvature.count(x) for x in range(3))
    rank = ones+twos
    if rank % 2:
        witt = rank//2; anisotropic = 1
    elif not rank:
        witt = anisotropic = 0
    else:
        split = (rank//2+twos) % 2 == 0
        witt = rank//2-int(not split); anisotropic = 0 if split else 2
    return {"input_width": len(curvature), "rank": rank, "radical_dimension": zeros,
            "ones": ones, "twos": twos, "anisotropic_dimension": anisotropic,
            "nondegenerate_Witt_index": witt, "maximum_totally_isotropic_dimension": zeros+witt,
            "rank_only_dimension_upper_bound": len(curvature)-(rank+1)//2}


def scalar_witt_frame(curvature):
    """Optimal F3 diagonal frame using zero wires, mixed pairs and four-blocks."""
    curvature = tuple(curvature); ledger = scalar_witt_dimension(curvature)
    m = len(curvature); columns, blocks = [], []
    sites = [[i for i, x in enumerate(curvature) if x == digit] for digit in range(3)]
    def column(ids, coefficients):
        v = [0]*m
        for i, x in zip(ids, coefficients): v[i] = x
        columns.append(tuple(v))
    for i in sites[0]: column((i,), (1,))
    mixed = min(len(sites[1]), len(sites[2]))
    for a, b in zip(sites[1][:mixed], sites[2][:mixed]):
        column((a, b), (1, 1)); blocks.append({"case": "opposite_pair", "sites": (a, b)})
    remaining = sites[1][mixed:] or sites[2][mixed:]
    for j in range(0, len(remaining)//4*4, 4):
        ids = tuple(remaining[j:j+4])
        column(ids, (1, 1, 1, 0)); column(ids, (1, 2, 0, 1))
        blocks.append({"case": "same_sign_four", "sites": ids})
    tail = tuple(remaining[len(remaining)//4*4:])
    if len(tail) == 3:
        column(tail, (1, 1, 1)); blocks.append({"case": "same_sign_three", "sites": tail})
    certificate = curvature_certificate([(x,) for x in curvature], columns)
    assert certificate["low_phase_affine_on_every_measured_complement"]
    assert len(columns) == ledger["maximum_totally_isotropic_dimension"]
    return {"curvatures": curvature, "columns": tuple(columns), "blocks": blocks,
            "dimension_ledger": ledger, "certificate": certificate,
            "selection_reads_only_curvature": True, "construction_time_polynomial_in_width": True}


def simultaneous_retention_screen(vectors):
    """Basis and pair combinations only; NOT an exhaustive projective search."""
    vectors = _vectors(vectors); m, n = len(vectors), len(vectors[0])
    directions = [tuple(int(l == j) for l in range(n)) for j in range(n)]
    for a, b in combinations(range(n), 2):
        directions.extend(tuple(1 if l == a else c if l == b else 0 for l in range(n)) for c in (1, 2))
    records = []
    for direction in directions:
        curvature = tuple(sum(x*y for x, y in zip(v, direction)) % 3 for v in vectors)
        records.append({"direction": direction, "dimension_ledger": scalar_witt_dimension(curvature)})
    return {"source_width": m, "secret_dimension": n, "scalar_direction_screens": records,
            "simultaneous_isotropic_dimension_upper_bound": min(r["dimension_ledger"]["maximum_totally_isotropic_dimension"] for r in records),
            "all_projective_directions_enumerated": n <= 2,
            "public_F3_scalar_multiply_adds": m*n*len(directions),
            "simultaneous_optimal_frame_constructed": False, "general_quantum_decoder_lower_bound": False}


def coordinate_recipe(columns, width):
    _integer(width, "source width", 1); columns = _columns(columns, width)
    k = len(columns); full = list(columns)
    for i in range(width):
        if len(full) == width: break
        candidate = tuple(int(j == i) for j in range(width))
        if nmod_mat([[v[j] for v in [*full, candidate]] for j in range(width)], 3).rank() == len(full)+1:
            full.append(candidate)
    T = nmod_mat([[v[i] for v in full] for i in range(width)], 3)
    inverse = T.inv()
    A = [[int(inverse[i, j]) for j in range(width)] for i in range(width)]
    rows = [list(row) for row in A]; elimination = []
    for j in range(width):
        p = next(i for i in range(j, width) if rows[i][j])
        if p != j:
            rows[p], rows[j] = rows[j], rows[p]
            elimination.append({"gate": "SWAP", "first": p, "second": j})
        if rows[j][j] == 2:
            rows[j] = [2*x % 3 for x in rows[j]]
            elimination.append({"gate": "SCALE_F3", "target": j, "coefficient": 2})
        for i in range(width):
            if i != j and rows[i][j]:
                coefficient = -rows[i][j] % 3
                rows[i] = [(x+coefficient*y) % 3 for x, y in zip(rows[i], rows[j])]
                elimination.append({"gate": "SUM_F3", "control": j, "target": i, "coefficient": coefficient})
    assert rows == [[int(i == j) for j in range(width)] for i in range(width)]
    gates = []
    for gate in reversed(elimination):
        gate = dict(gate)
        if gate["gate"] == "SUM_F3": gate["coefficient"] = -gate["coefficient"] % 3
        gates.append(gate)
    return {"source_width": width, "retained_width": k,
            "inverse_columns": tuple(full), "forward_matrix": A, "gates": gates,
            "measure_only_complement_coordinates": tuple(range(k, width)),
            "all_outcomes_accepted": True, "acceptance": "1",
            "unknown_state_preparation_inverse_or_cloning_required": False,
            "coherent_pointer_unknown_anchor_phases_must_be_retained": True,
            "hardware_qubit_synthesis_and_aggregate_error_certified": False}


def apply_gate_word(word, recipe):
    word = list(word)
    if len(word) != recipe["source_width"] or any(type(x) is not int or x not in (0, 1, 2) for x in word):
        raise ValueError("canonical original word required")
    for gate in recipe["gates"]:
        if gate["gate"] == "SWAP":
            i, j = gate["first"], gate["second"]; word[i], word[j] = word[j], word[i]
        elif gate["gate"] == "SCALE_F3": word[gate["target"]] = word[gate["target"]]*gate["coefficient"] % 3
        else: word[gate["target"]] = (word[gate["target"]]+gate["coefficient"]*word[gate["control"]]) % 3
    return tuple(word)


def physical_word(recipe, logical):
    if len(logical) != recipe["source_width"] or any(type(x) is not int or x not in (0, 1, 2) for x in logical):
        raise ValueError("canonical logical and pointer word required")
    return tuple(sum(c[i]*x for c, x in zip(recipe["inverse_columns"], logical)) % 3 for i in range(len(logical)))


def source_control(source, columns, secret):
    """All original-root Born branches; dense calibration only, not a decoder."""
    if source.level % 2 or source.inputs > 7 or len(columns) > 5 or len(secret) != source.dimension:
        raise ValueError("even source / bounded dense replay / matching secret required")
    if any(type(x) is not int for x in secret):
        raise ValueError("integer calibration secret required")
    certificate = curvature_certificate(curvatures(source), columns)
    if not certificate["low_phase_affine_on_every_measured_complement"]:
        raise ValueError("all component curvature Gram matrices must vanish")
    recipe = coordinate_recipe(columns, source.inputs); k = len(columns); q = source.modulus
    words = list(product(range(3), repeat=source.inputs)); index = {w: i for i, w in enumerate(words)}
    phase = lambda F: np.exp(2j*math.pi*(sum(a*s for a, s in zip(F, secret)) % q)/q)
    original = np.array([phase(source.value(w)) for w in words])/math.sqrt(3**source.inputs)
    actual = np.zeros_like(original)
    for w, amplitude in zip(words, original): actual[index[apply_gate_word(w, recipe)]] = amplitude
    records, maximum_error = [], 0.
    for pointer in product(range(3), repeat=source.inputs-k):
        logicals = list(product(range(3), repeat=k))
        physical = [physical_word(recipe, (*z, *pointer)) for z in logicals]
        F = [source.value(w) for w in physical]; base = F[0]
        expected = np.array([phase(v) for v in F])/math.sqrt(3**source.inputs)
        branch = np.array([actual[index[(*z, *pointer)]] for z in logicals])
        maximum_error = max(maximum_error, float(np.max(abs(branch-expected))))
        probability = float(np.vdot(branch, branch).real)
        defects = []
        for z, value in zip(logicals, F):
            axes = [source.value(physical_word(recipe, (*tuple(x if i == j else 0 for i in range(k)), *pointer)))
                    for j, x in enumerate(z)]
            defect = tuple((a+(k-1)*b-sum(v[l] for v in axes)) % q for l, (a, b) in enumerate(zip(value, base)))
            if any(defect): defects.append({"logical_word": z, "mixed_frequency_defect": defect})
        assert all(all(x % 3 == 0 for x in d["mixed_frequency_defect"]) for d in defects)
        purity = None
        if k > 1:
            state = (branch/math.sqrt(probability)).reshape(3, -1); rho = state@state.conj().T
            purity = float(np.trace(rho@rho).real)
        records.append({"pointer": pointer, "physical_words": physical, "original_frequency_table": F,
                        "branch_amplitudes": [[float(x.real), float(x.imag)] for x in branch],
                        "probability": probability, "original_anchor_frequency": base,
                        "nonzero_mixed_phase_defects": defects,
                        "componentwise_separable_for_all_secrets": not defects,
                        "calibration_first_logical_purity": purity})
    assert maximum_error < 1e-12
    assert abs(sum(r["probability"] for r in records)-1) < 1e-12
    return {"original_even_level": source.level, "original_modulus": str(q),
            "native_labels": source.labels, "curvatures": curvatures(source),
            "calibration_secret_only": secret, "curvature_certificate": certificate,
            "recipe": recipe, "all_measured_pointer_branches": records,
            "maximum_full_root_gate_error": maximum_error,
            "calibration_purity_is_an_unknown_secret_estimator": False,
            "identically_labeled_quantum_copies_for_SWAP_test_supplied": False,
            "deterministic_native_control_not_fresh_IID_source_claim": True,
            "low_curvature_zero_implies_full_root_product": False,
            "recursive_source_law_or_speedup_supplied": False}


def subspaces(width):
    """Bounded independent optimality census, NOT a scalable search routine."""
    _integer(width, "census width", 1)
    if width > 4: raise ValueError("subspace census capped at width4")
    for k in range(width+1):
        for pivots in combinations(range(width), k):
            slots = [(i, j) for i, p in enumerate(pivots) for j in range(p+1, width) if j not in pivots]
            for entries in product(range(3), repeat=len(slots)):
                columns = [[int(j == p) for j in range(width)] for p in pivots]
                for (i, j), x in zip(slots, entries): columns[i][j] = x
                yield tuple(tuple(v) for v in columns)


def exhaustive_scalar_census(width=4):
    spaces = list(subspaces(width)); seen, checks = 0, 0
    for curvature in product(range(3), repeat=width):
        maximum = 0
        for S in spaces:
            checks += 1
            if all(sum(B*u*v for B, u, v in zip(curvature, a, b)) % 3 == 0 for a in S for b in S):
                maximum = max(maximum, len(S))
        assert maximum == scalar_witt_dimension(curvature)["maximum_totally_isotropic_dimension"]
        assert maximum == len(scalar_witt_frame(curvature)["columns"])
        seen += 1
    return {"source_width": width, "curvature_arrays": seen, "all_F3_subspaces": len(spaces),
            "curvature_subspace_pairs_checked": checks, "sharp_bound_and_compiler_agree_with_entire_census": True}


def iid_retention_ledger(width):
    _integer(width, "source width", 1)
    expectation = Fraction(2*width, 3)-Fraction(3**width-1, 2*3**width)
    return {"original_IID_even_inputs": width, "one_component_curvature_uniform_F3": True,
            "exact_expected_maximum_low_affine_width": str(expectation),
            "expected_width_upper_for_any_secret_dimension": str(expectation),
            "fractional_upper": "2/3",
            "this_step_certifies_full_root_product_states": False,
            "applying_the_same_IID_law_after_this_joint_step_certified": False,
            "arbitrary_coherent_decoder_lower_bound": False}


def build_report():
    L = 4
    def source(pairs):
        return native_source([[inverse_frequency_coordinates(a, c, L)] for a, c in pairs], L)
    entangled = source([(0, 1)]*4); frame = scalar_witt_frame((1,)*4)
    control = source_control(entangled, frame["columns"], (1,))
    zero_branch = control["all_measured_pointer_branches"][0]
    assert zero_branch["nonzero_mixed_phase_defects"]
    assert abs(zero_branch["calibration_first_logical_purity"]-19/27) < 1e-12
    positive = source([(1, 5), (2, 1), (4, 8), (5, 7)])
    positive_frame = scalar_witt_frame((0,)*4)
    positive_control = source_control(positive, positive_frame["columns"], (1,))
    assert all(b["componentwise_separable_for_all_secrets"] for b in positive_control["all_measured_pointer_branches"])
    larger = random_even_source(4, 16, 100, 88794)
    return {"status": "SHARP_LINEAR_CURVATURE_FRONTIER_AND_FULL_ROOT_ENTANGLEMENT_COUNTERCONTROL_REVIEW_PENDING",
            "scalar_optimality_census": exhaustive_scalar_census(),
            "optimal_native_mixed_phase_countercontrol": {"frame": frame, "source_control": control,
                "zero_pointer_exact_first_logical_purity": "19/27",
                "exact_nonzero_mixed_defect_falsifies_product_for_secret1": True},
            "native_zero_curvature_product_positive_control": positive_control,
            "larger_original_source_retention_screen": {
                "dimension": 4, "original_even_level": 16, "original_modulus": str(larger.modulus),
                "native_labels": larger.labels, "curvatures": curvatures(larger),
                "screen": simultaneous_retention_screen(curvatures(larger)),
                "same_public_parent_control_as_cyclic_extractor": True,
                "screening_public_labels_consumes_quantum_inputs": False,
                "dense_quantum_output_replayed": False,
                "simultaneous_frame_or_secret_estimator_supplied": False},
            "IID_width_frontiers": [iid_retention_ledger(m) for m in (1, 4, 16, 64, 256, 4096)],
            "lower_bound_scope": "affine F3 changes of original computational coordinates followed by complement measurements, with every retained component low-affine for all unknown secrets",
            "nonlinear_permutations_arbitrary_POVMs_or_coherent_junk_excluded_from_bound": True,
            "retention_screen_is_full_root_product_compiler": False,
            "novelty_claim": False, "accepted_candidate": False,
            "polynomial_full_depth_decoder": False, "general_quantum_algorithm_lower_bound": False}


def write_ternary_curvature_frontier_report(
    output_path: Path = REPORT,
    write_registry: bool = True,
    registry_candidate_id: str = "DHS-GOWERS-SIEVE",
    registry_experiment_id: str = "EXP-DHS-DCP-COHERENT-MATCHING-INTERFACE",
) -> dict:
    report = build_report()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    if write_registry:
        from research_registry import NegativeResultRecord, upsert_negative_result
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-NATIVE-TOTAL-ISOTROPY-DOES-NOT-COMPILE-IID-PRODUCTS",
                source=str(output_path),
                claim="Total isotropy of the F3 curvature form across active sites compiles the native source into independent full-root product states.",
                reason_invalid="While totally isotropic subspaces ensure low phase affine on every measured complement, full-root states retain nonzero mixed phase defects and entanglement; calibration first logical purity is 19/27 < 1 on the zero pointer branch, falsifying product state compilation.",
                lesson="Curvature cancellation alone does not yield independent native product outputs. Do not infer full-root product state compilation or independent IID children from total isotropy without accounting for mixed phase defects.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "zero_pointer_exact_first_logical_purity": "19/27",
                    "exact_nonzero_mixed_defect_falsifies_product_for_secret1": True,
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
        report = write_ternary_curvature_frontier_report(write_registry=not args.no_registry)
        print(json.dumps({"report": str(REPORT), "sharp_scalar_census": report["scalar_optimality_census"],
                          "product_claim_falsified": True, "polynomial_full_depth_decoder": False}))
    else:
        print(json.dumps(build_report(), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
