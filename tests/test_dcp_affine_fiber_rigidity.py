"""Exact original-label falsifiers for a deliberately narrow affine obstruction."""
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

import pytest

from theorems.dcp_adaptive_direction_rank_gate import binary_map, decode_dyadic
from theorems.dcp_affine_fiber_rigidity import (
    CONTRACT, CONTRACT_ID, REPORT, affine_coefficients, affine_group,
    build_report, finite_control, native_bound, separating_covector,
    signature_certificate, signatures,
)


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "research/certificates/dcp_affine_fiber_rigidity_crosscheck.js"


@pytest.fixture(scope="module")
def report():
    return build_report()


def original_delta(A, rows, c, x, modulus=4):
    y = binary_map(rows, x) ^ c
    return tuple(sum(a * ((y >> i & 1) - (x >> i & 1)) for i, a in enumerate(row)) % modulus for row in A)


def test_all_small_matrices_and_affine_maps_exact_coefficients_match_original_phase():
    count = 0
    for n, m in ((1, 1), (1, 2), (2, 2)):
        for flat in product(range(4), repeat=n*m):
            A = tuple(flat[j*m:(j+1)*m] for j in range(n))
            for rows, c in affine_group(m):
                C = affine_coefficients(A, rows, c)
                direct = [original_delta(A, rows, c, x) for x in range(1 << m)]
                assert C["preserves_all_original_assignments_mod4"] == all(not any(v) for v in direct)
                for x, value in enumerate(direct):
                    for l in range(n):
                        predicted = C["constant_mod4"][l]
                        predicted += sum(v for j, v in enumerate(C["linear_mod4_by_component"][l]) if x >> j & 1)
                        pairs = [(j, k) for j in range(m) for k in range(j+1, m)]
                        predicted += sum(v[l] for (j, k), v in zip(pairs, C["quadratic_mod4_by_lexicographic_input_pair"])
                                         if x >> j & 1 and x >> k & 1)
                        assert predicted % 4 == value[l]
                if C["is_global_affine_fibre_automorphism"]:
                    assert C["simultaneous_form_forbidden_entries"] == []
                    if signature_certificate(A)["nonzero_distinct_signatures"]:
                        assert rows == tuple(1 << i for i in range(m)) and c == 0
                count += 1
    assert count == 6536


def test_every_covector_separator_small_signatures_including_strict_containment():
    for a in range(64):
        for b in range(64):
            u = separating_covector(a, b)
            if not a or a == b:
                assert u is None
            else:
                assert (u & a).bit_count() % 2 == 1
                assert (u & b).bit_count() % 2 == 0
                assert u.bit_count() <= 2
    assert separating_covector(1, 3).bit_count() == 2


def test_mod4_global_identity_on_distinct_comparable_signatures(report):
    C = report["finite_controls"][1]
    assert signatures(((1, 0, 5), (0, 1, 1))) == (1, 2, 3)
    assert C["signature_certificate"]["nonzero_distinct_signatures"] is True
    assert C["complete_affine_bijections_tested"] == 1344
    assert len(C["global_mod4_automorphisms"]) == 1
    assert C["global_mod4_automorphisms"][0]["linear_rows_hex"] == ["0x1", "0x2", "0x4"]


def test_partial_affine_proposal_survives_rigid_global_gate_and_has_actual_nonzero_output(report):
    C = report["finite_controls"][1]
    P = C["partial_proposal_control"]
    assert C["signature_certificate"]["global_affine_mod4_automorphism_classification"] == "IDENTITY_ONLY"
    assert P["coefficients"]["is_global_affine_fibre_automorphism"] is False
    assert decode_dyadic(P["paid_input_useful_acceptance_probability"]) == Fraction(1, 4)
    assert {r["x_hex"] for r in P["useful_reciprocal_assignments"]} == {"0x3", "0x4"}
    assert all(r["output_label_hex"] == ["0x1", "0x0"] for r in P["useful_reciprocal_assignments"])


def test_repeated_and_zero_signature_exceptions_preserve_useful_outputs_and_pay_fixed_points(report):
    repeated, zero = report["finite_controls"][2:4]
    assert repeated["signature_certificate"]["nonzero_distinct_signatures"] is False
    assert zero["signature_certificate"]["nonzero_distinct_signatures"] is False
    rp, zp = (C["partial_proposal_control"] for C in (repeated, zero))
    assert rp["coefficients"]["is_global_affine_fibre_automorphism"] is True
    assert decode_dyadic(rp["paid_input_useful_acceptance_probability"]) == Fraction(1, 2)
    assert len(rp["fixed_assignments_hex"]) == 2
    assert zp["coefficients"]["is_global_affine_fibre_automorphism"] is True
    assert decode_dyadic(zp["paid_input_useful_acceptance_probability"]) == 1
    assert zp["fixed_assignments_hex"] == []


def test_failure_of_signature_gate_is_unknown_not_automatic_symmetry(report):
    C = report["finite_controls"][4]
    assert C["signature_certificate"]["nonzero_distinct_signatures"] is False
    assert C["signature_certificate"]["global_affine_mod4_automorphism_classification"] == "UNKNOWN"
    assert len(C["global_mod4_automorphisms"]) == 1


def test_parity_only_can_have_affine_kernel_translations_on_good_signatures():
    A, rows, c = ((1, 0, 5), (0, 1, 1)), (1, 2, 4), 7
    assert signature_certificate(A)["nonzero_distinct_signatures"] is True
    assert all(not any(original_delta(A, rows, c, x, modulus=2)) for x in range(8))
    assert not affine_coefficients(A, rows, c)["preserves_all_original_assignments_mod4"]


def test_simultaneous_form_invariance_for_every_binary_combination_of_rows():
    A = ((1, 5, 0), (2, 2, 4))
    p = signatures(A)
    for rows, c in affine_group(3):
        C = affine_coefficients(A, rows, c)
        if not C["is_global_affine_fibre_automorphism"]:
            continue
        for u in range(1 << len(A)):
            diag = [(u & sig).bit_count() & 1 for sig in p]
            for j in range(3):
                for k in range(3):
                    val = sum(diag[i] * (rows[i] >> j & 1) * (rows[i] >> k & 1) for i in range(3)) % 2
                    assert val == (diag[j] if j == k else 0)


def test_all_fibres_can_be_even_while_global_affine_pairing_is_impossible():
    # n4,m13 exceeds the sharp even-fibre threshold3n, with all13 distinct
    # nonzero low signatures. The pairing here is a charged exponential table.
    n, m = 4, 13
    A = tuple(tuple((p >> l) & 1 for p in range(1, m+1)) for l in range(n))
    assert signature_certificate(A)["nonzero_distinct_signatures"] is True
    fibres = defaultdict(list)
    for x in range(1 << m):
        value = tuple(sum(a for i, a in enumerate(row) if x >> i & 1) % 4 for row in A)
        fibres[value].append(x)
    table = {}
    for vertices in fibres.values():
        assert len(vertices) % 2 == 0
        for x, y in zip(vertices[::2], vertices[1::2]):
            table[x], table[y] = y, x
    assert len(table) == 1 << m
    assert all(table[x] != x and table[table[x]] == x for x in table)
    c = table[0]
    columns = [table[1 << j] ^ c for j in range(m)]
    affine_prediction = {x: c ^ binary_map(tuple(sum((col >> i & 1) << j for j, col in enumerate(columns))
                                               for i in range(m)), x) for x in table}
    assert any(table[x] != affine_prediction[x] for x in table)


def test_native_probability_exact_product_and_union_against_exhaustive_tables():
    for n, m in ((1, 1), (1, 2), (2, 2), (2, 3), (2, 4), (3, 3)):
        count = 0
        for cols in product(range(1 << n), repeat=m):
            count += 0 not in cols and len(set(cols)) == m
        actual = Fraction(count, 1 << (n*m))
        R = native_bound(n, m)
        assert decode_dyadic(R["exact_signature_gate_probability"]) == actual
        assert decode_dyadic(R["identity_only_probability_lower_bound"]) <= actual
        assert 1-actual <= decode_dyadic(R["rigidity_gate_failure_probability_upper_bound"])


def test_large_source_union_not_containment_bound_and_honest_exact_product_caps(report):
    R = native_bound(64, 192)
    assert decode_dyadic(R["rigidity_gate_failure_probability_upper_bound"]) == Fraction(18528, 1 << 64)
    assert decode_dyadic(R["rigidity_gate_failure_probability_upper_bound"]) < Fraction(1, 1 << 49)
    assert native_bound(1, 4)["bound_vacuous"] is True
    assert decode_dyadic(native_bound(1, 4)["exact_signature_gate_probability"]) == 0
    big = native_bound(512, 1536)
    assert big["exact_signature_gate_probability"] is None
    assert big["exact_probability_omitted_due_to_work_cap"] is True
    assert big["bound_vacuous"] is False
    assert all(s["certificate"]["nonzero_distinct_signatures"] for s in report["polynomial_signature_controls"])


def test_no_secret_or_higher_label_assumption_in_rigidity_gate():
    low = ((1, 0, 1), (0, 1, 1))
    for lift in range(32):
        A = tuple(tuple(a + 2*((lift + i + 3*l) % 11) for i, a in enumerate(row)) for l, row in enumerate(low))
        assert signature_certificate(A)["nonzero_distinct_signatures"] is True
        assert len(finite_control("unfiltered-higher-lift", A, phase_bits=5)["global_mod4_automorphisms"]) == 1


@pytest.mark.parametrize("A,rows,c", [
    ((), (1,), 0), (((1, 2), (1,)), (1, 2), 0), (((True,),), (1,), 0),
    (((-1,),), (1,), 0), (((1.0,),), (1,), 0), (((1,),), (True,), 0),
    (((1,),), (2,), 0), (((1,),), (1,), True), (((1,),), (1,), -1),
    (((1, 2),), (1,), 0),
])
def test_bad_input_cannot_inherit_exact_certificate(A, rows, c):
    with pytest.raises(ValueError):
        affine_coefficients(A, rows, c)


def test_explicit_work_caps_do_not_promote_unknown_to_a_no_go():
    with pytest.raises(ValueError, match="UNKNOWN"):
        list(affine_group(4))
    with pytest.raises(ValueError, match="UNKNOWN"):
        affine_coefficients(((1,)*128,), tuple(1 << i for i in range(128)), 0)
    with pytest.raises(ValueError, match="UNKNOWN"):
        signature_certificate(((0,)*4097,))


def js_check(report, tmp_path):
    target = tmp_path / "certificate.json"
    target.write_text(json.dumps(report))
    return subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)


def test_independent_replay_and_live_provenance(report, tmp_path):
    assert json.loads(REPORT.read_text()) == report
    contract = json.loads(CONTRACT.read_text())
    assert contract["contract_id"] == CONTRACT_ID
    assert contract["accepted_speedup_candidate"] is False
    checked = js_check(report, tmp_path)
    assert checked.returncode == 0, checked.stderr
    assert json.loads(checked.stdout)["native_frontiers"] == 14


@pytest.mark.parametrize("mutation", ["signature", "source", "census", "coefficient", "pair", "paid_mass",
                                         "union", "exact", "vacuity", "scope", "gate", "promotion"])
def test_forged_certificates_are_rejected(report, tmp_path, mutation):
    R = deepcopy(report)
    if mutation == "signature":
        R["polynomial_signature_controls"][0]["certificate"]["low_column_signatures_hex"][0] = "0x0"
    elif mutation == "source":
        R["finite_controls"][1]["signature_certificate"]["public_labels_hex"][0][0] = "0x3"
    elif mutation == "census":
        R["finite_controls"][0]["global_mod4_automorphisms"] = []
    elif mutation == "coefficient":
        R["finite_controls"][2]["partial_proposal_control"]["coefficients"]["linear_mod4_by_component"][0][0] = 2
    elif mutation == "pair":
        R["finite_controls"][1]["partial_proposal_control"]["useful_reciprocal_assignments"][0]["output_label_hex"] = ["0x0", "0x0"]
    elif mutation == "paid_mass":
        R["finite_controls"][2]["partial_proposal_control"]["paid_input_useful_acceptance_probability"] = {"numerator_hex":"0x1", "denominator_binary_exponent":0}
    elif mutation == "union":
        R["native_probability_frontiers"][6]["rigidity_gate_failure_probability_upper_bound"]["numerator_hex"] = "0x0"
    elif mutation == "exact":
        R["native_probability_frontiers"][6]["exact_signature_gate_probability"]["numerator_hex"] = "0x1"
    elif mutation == "vacuity":
        R["native_probability_frontiers"][0]["bound_vacuous"] = False
    elif mutation == "scope":
        R["scope"]["partial_proposals_excluded"] = True
    elif mutation == "gate":
        R["finite_controls"][4]["signature_certificate"]["global_affine_mod4_automorphism_classification"] = "IDENTITY_ONLY"
    else:
        R["accepted_speedup_candidate"] = True
    checked = js_check(R, tmp_path)
    assert checked.returncode != 0


def test_read_only_cli_is_bound_to_live_artifact(report):
    before = REPORT.read_bytes()
    result = subprocess.run([sys.executable, "qsearch.py", "dcp-affine-fiber-rigidity", "--no-write"],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == report["status"]
    assert REPORT.read_bytes() == before
