"""Compare integer source certificates with complete original phase laws."""
from collections import Counter
from fractions import Fraction
from itertools import product, combinations
import json
from pathlib import Path
import subprocess

from flint import fmpq_mat, fmpz_mat
import pytest

from theorems.dcp_carry_congruence_source import (
    affine_congruence_source, certify_native_source, SourcePolicy, SELECTION,
    quadratic_inconsistency_control,
    overlap_closure, exact_json,
)
from theorems.dcp_carry_source_law import certify_q8_source

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "research/phase_workbench/dcp_carry_congruence_source.json"
CHECKER = ROOT / "research/certificates/dcp_carry_congruence_source_crosscheck.js"


def probability(record):
    return Fraction(int(record["numerator_hex"], 16), 1 << record["denominator_binary_exponent"])


def check_lattice(c):
    if c is None:
        return
    G, H = fmpz_mat(c["generator_rows"]), fmpz_mat(c["row_hnf_basis"])
    assert fmpz_mat(c["basis_from_generator_coefficients"]) * G == H
    assert fmpz_mat(c["generators_from_basis_coefficients"]) * H == G
    assert abs(int(H.det())) == c["integer_lattice_index"]


def in_output_coset(y, representative, law):
    inverse = fmpq_mat(law["output_kernel_integer_basis"]).inv()
    coeff = fmpq_mat([[a - b for a, b in zip(y, representative)]]) * inverse
    return all(x.denominator == 1 for x in coeff.tolist()[0])


@pytest.mark.parametrize("R,D,J,targets", [
    ((), (), ((1, 0), (0, 1)), ((),)),
    (((0, 0),), (4,), ((1, 0),), ((0,), (1,))),
    (((1, -1),), (2,), ((1, 0), (0, 1)), ((0,), (1,))),
    (((2, 0), (1, 1)), (4, 2), ((1, 1), (0, 1)), ((0, 0), (2, 1))),
    (((2, 2),), (4,), ((-1, 2),), ((0,), (1,))),
])
def test_affine_source_matches_every_uniform_input(R, D, J, targets):
    Q, m = 4, len(J[0])
    offsets = tuple(tuple(i + j for j in range(len(J))) for i in range(len(targets)))
    law = affine_congruence_source(R, D, J, Q, targets, offsets)
    check_lattice(law["constraint_lattice_certificate"])
    check_lattice(law["joint_lattice_certificate"])
    joint = Fraction(1)
    for i, target in enumerate(targets):
        hist = Counter()
        for z in product(range(Q), repeat=m):
            if any(sum(a * b for a, b in zip(row, z)) % d != t for row, d, t in zip(R, D, target)):
                continue
            y = tuple((sum(a * b for a, b in zip(row, z)) + off) % Q for row, off in zip(J, offsets[i]))
            hist[y] += 1
        mass = Fraction(sum(hist.values()), Q**m)
        joint *= mass
        assert law["components"][i]["acceptance_possible"] == bool(hist)
        if hist:
            assert mass == probability(law["acceptance_probability_per_consistent_component"])
            assert len(hist) == law["output_support_size_per_accepted_component"]
            assert len(set(hist.values())) == 1
            assert all(in_output_coset(y, law["components"][i]["output_coset_representative"], law) for y in hist)
    assert joint == probability(law["joint_native_acceptance_probability"])


def test_full_marginals_do_not_imply_joint_IID():
    law = affine_congruence_source(((1, -1),), (2,), ((1, 0), (0, 1)), 4, ((0,),))
    assert law["output_marginal_support_sizes"] == (4, 4)
    assert law["output_support_size_per_accepted_component"] == 8
    assert law["conditional_joint_labels_IID_uniform_mod_Q"] is False


def test_wrong_HNF_leading_block_would_claim_twice_the_output_support():
    law = affine_congruence_source(((2,),), (4,), ((1,),), 4, ((0,),))
    assert law["output_support_size_per_accepted_component"] == 2
    wrong_order = fmpz_mat([[1, 2], [0, 4], [4, 0]]).hnf()
    assert int(wrong_order[0, 0]) == 1
    assert 4 // int(wrong_order[0, 0]) != law["output_support_size_per_accepted_component"]


def original_phase_histogram(B, directions, t, background):
    """No monomial/congruence helper: test the actual Boolean phase function."""
    Q, q, m, d = 1 << (t - 1), 1 << t, len(B), len(directions)
    hist = Counter()
    for z in product(range(Q), repeat=m):
        A = tuple(b + 2 * x for b, x in zip(B, z))
        def phase(y):
            x = background
            for j, u in enumerate(directions):
                if y >> j & 1:
                    x ^= u
            return sum(a * ((x >> i) & 1) for i, a in enumerate(A))
        base = phase(0)
        linear = tuple(phase(1 << j) - base for j in range(d))
        if any((phase(y) - base - sum(a for j, a in enumerate(linear) if y >> j & 1)) % q for y in range(1 << d)):
            continue
        assert all(a % 2 == 0 for a in linear)
        hist[tuple(a // 2 % Q for a in linear)] += 1
    return hist


@pytest.mark.parametrize("B,U", [((1, 1, 1, 1), (3, 12)), ((1, 1, 1, 1), (3, 15)), ((0, 0, 0, 0), (3, 5, 9))])
@pytest.mark.parametrize("t", [3, 4])
@pytest.mark.parametrize("background", [0, 1, 3])
def test_higher_source_matches_complete_original_phase_table(B, U, t, background):
    result = certify_native_source((B,), U, t, background, selection_model=SELECTION)
    hist = original_phase_histogram(B, U, t, background)
    law = result["source_law"]
    assert probability(result["joint_native_acceptance_probability"]) == Fraction(sum(hist.values()), (1 << (t - 1)) ** len(B))
    assert len(hist) == law["output_support_size_per_accepted_component"]
    assert len(set(hist.values())) == 1
    assert all(in_output_coset(y, law["components"][0]["output_coset_representative"], law) for y in hist)
    top = Counter()
    for y, count in hist.items():
        top[tuple(x >> (t - 2) for x in y)] += count
    assert len(top) == 1 << len(U) and len(set(top.values())) == 1


@pytest.mark.parametrize("B,U", [(((1, 1, 1, 1),), (3, 12)), (((1, 1, 1, 1),), (3, 15)),
    (((1, 1, 0, 0, 1, 1), (0, 0, 1, 1, 1, 1)), (15, 51))])
def test_q8_reduction_matches_older_independent_binary_reference(B, U):
    old = certify_q8_source(B, U, selection_model=SELECTION)
    new = certify_native_source(B, U, 3, selection_model=SELECTION)
    assert new["acceptance_possible"] == old["acceptance_possible"]
    assert probability(new["joint_native_acceptance_probability"]) == Fraction(1, 2 ** old["inverse_acceptance_batch_exponent"])
    assert new["conditional_output_entropy_bits_IF_accepted"] == old["conditional_output_entropy_bits"]


@pytest.mark.parametrize("t", [3, 4, 8, 64])
def test_all_physical_backgrounds_give_same_affine_law_at_every_level(t):
    B, U = ((1, 1, 1, 1),), (3, 15)
    base = certify_native_source(B, U, t, selection_model=SELECTION)
    for x in range(16):
        current = certify_native_source(B, U, t, x, selection_model=SELECTION)
        assert current["joint_native_acceptance_probability"] == base["joint_native_acceptance_probability"]
        assert current["source_law"]["output_kernel_integer_basis"] == base["source_law"]["output_kernel_integer_basis"]
        assert in_output_coset(current["source_law"]["components"][0]["output_coset_representative"],
                               base["source_law"]["components"][0]["output_coset_representative"], base["source_law"])


def test_caps_and_missing_lineage_are_not_hardness_certificates():
    B, U = ((0, 0, 0, 0),), (3, 5, 9)
    with pytest.raises(ValueError, match="lineage"):
        certify_native_source(B, U, 8, selection_model="selected-after-higher-labels")
    for policy in (SourcePolicy(max_intersection_states=1), SourcePolicy(max_lattice_cells=1)):
        with pytest.raises(ValueError, match="UNKNOWN"):
            certify_native_source(B, U, 8, selection_model=SELECTION, policy=policy)
    record = certify_native_source(B, U, 8, selection_model=SELECTION)
    assert record["selection_lineage_programmatically_verified"] is False
    assert record["quantum_product_extraction_circuit_compiled"] is False


def test_low_bit_monomial_obstruction_is_rejected_before_HNF():
    # Both directions have even parity, but their overlap has odd parity.
    result = certify_native_source(((1, 1, 1),), (3, 5), 4, selection_model=SELECTION)
    assert result["acceptance_possible"] is False
    assert result["reason"] == "LOW_BIT_MIXED_MONOMIAL_OBSTRUCTION"


def test_all_parities_can_pass_while_integer_constraint_targets_are_impossible():
    c = quadratic_inconsistency_control()
    assert c["acceptance_possible"] is False
    assert probability(c["joint_native_acceptance_probability"]) == 0
    assert c["source_law"]["components"][0]["acceptance_possible"] is False
    assert any(Fraction(x).denominator != 1 for x in c["source_law"]["components"][0]["nonintegral_constraint_basis_coordinates"])


def test_overlap_compression_matches_all_mixed_subsets_including_generator_equal_meets():
    for U in ((3, 5, 9), (3, 15), (3, 5, 15), (7, 11, 13, 14)):
        for t in (3, 4, 8):
            expected = {}
            for h in range(2, min(t, len(U)) + 1):
                for S in combinations(range(len(U)), h):
                    e = (1 << max(U).bit_length()) - 1
                    for i in S:
                        e &= U[i]
                    if e and (e not in expected or (h, S) < (len(expected[e]), expected[e])):
                        expected[e] = S
            actual, _ = overlap_closure(U, t, 4096)
            assert dict(actual) == expected


def test_overlap_compression_exhausts_all_three_and_four_generator_families_on_four_coordinates():
    for d in (3, 4):
        for U in combinations(range(1, 16), d):
            for t in (3, 4):
                expected = {}
                for h in range(2, min(t, d) + 1):
                    for S in combinations(range(d), h):
                        e = 15
                        for j in S:
                            e &= U[j]
                        if e and (e not in expected or (h, S) < (len(expected[e]), expected[e])):
                            expected[e] = S
                assert dict(overlap_closure(U, t, 4096)[0]) == expected


def test_disjoint_large_packet_does_not_expand_its_exponential_monomial_menu():
    import sys
    limit = sys.get_int_max_str_digits()
    U = tuple(3 << (2*j) for j in range(64))
    c = certify_native_source(((0,) * 128,), U, 1024, selection_model=SELECTION)
    assert c["monomial_expansion_terms"] == 2**64 - 65
    assert c["monomials_checked"] == 0
    assert c["overlap_closure_work"]["pairwise_intersections_evaluated"] == 2016
    serialized = json.loads(json.dumps(exact_json(c)))
    support = serialized["source_law"]["output_support_size_per_accepted_component"]
    assert support.startswith("0x") and int(support, 16) == 1 << (1023 * 64)
    assert sys.get_int_max_str_digits() == limit


def test_huge_rejection_exponent_is_structured_not_a_decimal_overflow():
    c = certify_native_source(((0,) * 5,) * 16, (3, 5, 9, 17), 1024, selection_model=SELECTION)
    assert c["joint_native_acceptance_probability"] == {"numerator_hex": "0x1", "denominator_binary_exponent": 16352}
    assert c["source_law"]["expected_supplied_attempts_IF_fresh_batches_exist"] == {"power_of_two": 16352}
    json.dumps(exact_json(c))


def test_independent_integer_certificate_replay():
    proc = subprocess.run(["node", str(CHECKER)], capture_output=True, text=True, check=True)
    assert json.loads(proc.stdout)["verified"] is True


@pytest.mark.parametrize("tamper", ["containment", "index", "coset", "cost", "lineage"])
def test_independent_replay_rejects_false_source_certificates(tmp_path, tamper):
    report = json.loads(ARTIFACT.read_text())
    c = report["native_source_controls"][0]
    if tamper == "containment":
        c["source_law"]["joint_lattice_certificate"]["basis_from_generator_coefficients"][0][0] += 1
    elif tamper == "index":
        c["source_law"]["output_kernel_lattice_index"] = 100
    elif tamper == "coset":
        c = report["native_source_controls"][8]
        c["source_law"]["components"][0]["output_coset_representative"][0] += 1
    elif tamper == "cost":
        report["large_exact_not_enumerated_control"]["joint_native_acceptance_probability"]["denominator_binary_exponent"] = 0
    else:
        c["selection_lineage_programmatically_verified"] = True
    target = tmp_path / "corrupted.json"
    target.write_text(json.dumps(report))
    proc = subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)
    assert proc.returncode != 0
