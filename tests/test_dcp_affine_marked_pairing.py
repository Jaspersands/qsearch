from collections import Counter
from fractions import Fraction
from itertools import combinations, product

import pytest

from dcp_affine_marked_pairing import (
    MarkedPairingProgram, affine_hash, build_marked_pairing_audit,
    coverage_certificate, exact_source_control, finite_program_control,
    program_from_seed, support_count, support_masks,
)
from dcp_pairing_programs import evaluate_mutual_program


def test_affine_seed_is_exactly_three_wise_not_four_wise():
    width, bits = 3, 2
    seeds = list(product(product(range(1 << width), repeat=bits), range(1 << bits)))
    for vertices in combinations(range(8), 3):
        counts = Counter(tuple(affine_hash(v, rows, offset) for v in vertices) for rows, offset in seeds)
        assert len(counts) == 4**3
        assert set(counts.values()) == {len(seeds)//4**3}
    for rows, offset in seeds:
        assert affine_hash(0, rows, offset) ^ affine_hash(1, rows, offset) ^ affine_hash(2, rows, offset) ^ affine_hash(3, rows, offset) == 0


def test_pointwise_hash_matches_existing_full_table_reference():
    from self_dual_wreath_orientation_kernel_hash_thinning import affine_hash_mask
    for rows, offset in [((1, 6), 2), ((0, 0), 0), ((0, 0), 1)]:
        expected = affine_hash_mask(3, rows, offset)
        assert [affine_hash(b, rows, offset) == 0 for b in range(8)] == expected.tolist()


def test_program_factory_covers_all_seeds_without_conditioning_or_bias():
    programs = [program_from_seed((1, 3), 2, seed, 2) for seed in range(64)]
    assert {(p.hash_rows, p.hash_offset) for p in programs} == {
        (rows, offset) for rows in product(range(4), repeat=2) for offset in range(4)}
    assert len(programs) == len(set(programs))
    assert any(not any(p.marked(b) for b in range(4)) for p in programs)
    with pytest.raises(ValueError, match="seed"):
        program_from_seed((1, 3), 2, 64, 2)


def test_program_copies_public_inputs_to_keep_uncomputation_deterministic():
    labels, rows = [1, 3], [0]
    program = MarkedPairingProgram(labels, 2, 2, rows, 0)
    before = [program.propose(b) for b in range(4)]
    labels[0], rows[0] = 0, 1
    assert [program.propose(b) for b in range(4)] == before
    assert program.labels == (1, 3) and program.hash_rows == (0,)


def test_conditioning_full_rank_or_dropping_offset_invalidates_hash_premise():
    # Full-rank one-row hashes on two bits cannot mark these three vertices.
    count = sum(all(affine_hash(v, (row,), offset) == 0 for v in (0, 1, 2))
                for row in (1, 2, 3) for offset in (0, 1))
    assert count == 0  # Not theta^3=1/8.
    assert all(affine_hash(0, (row,), 0) == 0 for row in range(4))


def test_pairwise_independent_marks_alone_do_not_guarantee_isolated_edges():
    # Zero sets of affine maps over F_4: empty, singleton, or the whole field.
    law = {0: Fraction(3, 16), 15: Fraction(1, 16),
           **{1 << b: Fraction(3, 16) for b in range(4)}}
    assert sum(law.values()) == 1
    for b in range(4):
        assert sum(p for marked, p in law.items() if marked & (1 << b)) == Fraction(1, 4)
    for b, c in combinations(range(4), 2):
        assert sum(p for marked, p in law.items() if marked & (1 << b) and marked & (1 << c)) == Fraction(1, 16)
    # The half-period graph for N=4, labels=(2,2), radius=1 is a four-cycle.
    average = Fraction(0)
    for selected, probability in law.items():
        neighbors = [sum(1 << c for c in (b ^ 1, b ^ 2) if selected & (1 << c)) for b in range(4)]
        mass = sum(bool(selected & (1 << b)) and adjacent.bit_count() == 1
                   and neighbors[adjacent.bit_length()-1] == 1 << b
                   for b, adjacent in enumerate(neighbors))
        average += probability*Fraction(mass, 4)
    assert average == 0
    theta = Fraction(1, 4)
    assert theta**2*2-theta**3*(2*4-2*2) == Fraction(1, 16) > average


@pytest.mark.parametrize("n,width,radius", [(2, 2, 1), (2, 2, 2), (3, 3, 1), (2, 3, 2)])
def test_exact_natural_source_moments_and_isolated_edge_lower_bound(n, width, radius):
    row = exact_source_control(n, width, radius)
    assert all(row["checks"].values())
    assert row["observed_mass"] >= row["mass_lower"] > 0


def test_streamed_xor_evaluation_is_a_full_space_permutation_with_clean_workspace():
    program = MarkedPairingProgram((1, 3), 2, 2, (), 0)
    outputs = set()
    # Dirty work wires are retained too: no map is specified only on good inputs.
    for b, out, count, image in product(range(4), range(8), range(4), range(4)):
        result = program.evaluate_xor(b, out, count, image)
        assert (result["work_count"], result["work_image"]) == (count, image)
        outputs.add((b, result["output"], result["work_count"], result["work_image"]))
        assert result["support_predicate_calls"] == 6
    assert len(outputs) == 4*8*4*4


@pytest.mark.parametrize("program", [MarkedPairingProgram((1, 3, 0), 2, 2, (0, 0, 0), 0),
                                    MarkedPairingProgram((4, 1, 2), 3, 1, (2,), 0),
                                    MarkedPairingProgram((1, 2, 5), 3, 2, (1, 2), 0)])
def test_actual_program_composes_with_the_physical_six_call_compiler(program):
    control = finite_program_control(program)
    assert control["failures"] == 0
    physical = evaluate_mutual_program(program.labels, 1 << program.n, control["proposal_table"])
    assert all(physical["physical_checks"].values())
    assert physical["maximum_residual"] < 1e-12
    assert physical["profile"]["heralded_success_fraction"] == float(control["accepted_source_mass"])


def test_zero_or_multiple_marked_neighbors_fail():
    # With all labels at half-period and radius 1 this is a cube: no unique neighbors.
    program = MarkedPairingProgram((2, 2, 2), 2, 1, (), 0)
    assert all(program.propose(b) is None for b in range(8))
    empty = MarkedPairingProgram((2, 2, 2), 2, 1, (0,), 1)
    assert all(empty.propose(b) is None for b in range(8))


def test_minimal_radius_has_polynomial_mass_but_exponential_actual_work():
    for n in (8, 16, 64, 256, 512):
        row = coverage_certificate(n, n*n)
        assert row["unit_mean_degree_reached"]
        assert 1 <= row["mean_degree"] < n*n+1
        assert row["source_mass_lower"] >= Fraction(1, 128*(n*n+1))
        assert row["radius"] <= n//2
        assert row["joint_fault_signal_lower"] >= row["source_mass_lower"]/2
        assert row["six_xor_support_predicate_calls"] >= 12*(1 << n)
        assert row["public_seed_bits"] == row["hash_bits"]*(n*n+1)
        assert row["polynomial_time_claimed"] is False
        assert row["full_assignment_table_required"] is False


def test_support_enumerator_is_complete_without_duplicates():
    masks = list(support_masks(6, 3))
    assert len(masks) == len(set(masks)) == support_count(6, 3)
    assert set(masks) == {mask for mask in range(64) if 1 <= mask.bit_count() <= 3}


@pytest.mark.parametrize("args", [(0, 2, 1), (3, 0, None), (True, 2, 1), (3, 2, 3)])
def test_invalid_certificate_dimensions_are_rejected(args):
    with pytest.raises(ValueError):
        coverage_certificate(*args)


def test_report_does_not_promote_polynomial_coverage_to_a_speedup():
    report = build_marked_pairing_audit()
    assert report["control_failures"] == 0
    assert len(report["program_controls"]) == 3
    assert report["contract"]["finite_program_executed"] is True
    assert report["contract"]["polynomial_time_finder_constructed"] is False
    assert report["contract"]["speedup_claim_allowed"] is False
    assert all(row["quantum_search_implemented"] is False for row in report["scaling"])
