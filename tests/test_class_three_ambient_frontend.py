"""Tests for the ambient class-three filtration certifier, M/K normalizer quotient, unrolled Solve(L,f) recursion, and two-tree resource audit."""
from __future__ import annotations

import pytest

from theorems.class_three_ambient_frontend import (
    _fmpz_solve_coordinates,
    _subspace_intersection,
    build_class_three_ambient_frontend_report,
    certify_ambient_class_three_derived,
    class_four_normal_frequency_motion_probe,
    class_three_full_jet_resource_budget,
    ivanyos_santha_sde_arity,
    make_ut6_ambient_algebra,
    make_ut7_ambient_algebra,
    public_normalizer_quotient_algebra,
    unrolled_full_jet_solve,
)
from theorems.class_three_monomial_jet import align_full_jet, compile_full_jet_phase
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra


def test_ut7_ambient_filtration_and_exact_center_certification() -> None:
    algebra, std_basis, _ = make_ut7_ambient_algebra(19)
    cert = certify_ambient_class_three_derived(algebra, std_basis)
    assert cert.ambient_dimension == 21
    assert cert.ambient_class == 6
    assert cert.quotient_width == 6
    assert cert.derived_dimension == 15
    assert cert.derived_class == 3
    assert (cert.structure.a_width, cert.structure.b_width, cert.structure.c_width) == (9, 2, 4)
    assert cert.jet_degree == 4
    assert cert.weighted_phase_degree == 12
    assert cert.center_exact is True
    assert cert.gamma_c_minus_1_in_center is True
    assert cert.b_is_empty_class_two_branch is False

    # Proper subspace of Z(N) is rejected
    proper_c = cert.c_basis[:-1]
    with pytest.raises(ValueError, match="proper subspace"):
        certify_ambient_class_three_derived(algebra, std_basis, proposed_c_basis=proper_c)

    # Non-central vector in N is rejected
    non_central = list(cert.c_basis[:-1]) + [cert.a_basis[0]]
    with pytest.raises(ValueError, match="not central"):
        certify_ambient_class_three_derived(algebra, std_basis, proposed_c_basis=non_central)


def test_ut6_unified_class_two_empty_b_branch_certification() -> None:
    # ut_6(F_17) has ambient class c=5, D=3, and class(N)=2 with B=0, beta=(), delta=((),...,())
    alg6, basis6, _ = make_ut6_ambient_algebra(17)
    cert6 = certify_ambient_class_three_derived(alg6, basis6)
    assert cert6.ambient_dimension == 15
    assert cert6.ambient_class == 5
    assert cert6.derived_class == 2
    assert cert6.b_is_empty_class_two_branch is True
    assert cert6.structure.b_width == 0
    assert cert6.structure.beta == ()
    assert cert6.structure.a_width == 6
    assert cert6.structure.c_width == 4
    assert cert6.jet_degree == 3


def test_prime_bound_and_ambient_filtration_guards() -> None:
    alg_small, basis_small, _ = make_ut7_ambient_algebra(11)
    with pytest.raises(ValueError, match="p > max"):
        certify_ambient_class_three_derived(alg_small, basis_small)

    for p in (11, 2**127 - 1):
        def bad_filtration_bracket(left, right):
            q0, q1, a0, a1, b, c = left
            r0, r1, x0, x1, y, z = right
            return (
                0,
                0,
                (q0 * r1 - r0 * q1) % p,
                (q0 * x0 - r0 * a0) % p,
                (q0 * x1 - r0 * a1 + a0 * x1 - x0 * a1) % p,
                (q0 * y - r0 * b + a0 * y - x0 * b) % p,
            )

        bad_alg = PublicLieAlgebra(p=p, dimension=6, bracket_fn=bad_filtration_bracket)
        std6 = [tuple(int(i == j) for j in range(6)) for i in range(6)]
        with pytest.raises(ValueError, match="ambient filtration check failed"):
            certify_ambient_class_three_derived(bad_alg, std6)


def test_public_normalizer_quotient_handles_n_not_in_m_in_ut7() -> None:
    alg7, basis7, slots7 = make_ut7_ambient_algebra(19)
    e13_idx = slots7.index((0, 2))
    e35_idx = slots7.index((2, 4))
    k_basis = [tuple(int(i == e13_idx) for i in range(len(slots7)))]
    e35_vec = tuple(int(i == e35_idx) for i in range(len(slots7)))

    norm_quot = public_normalizer_quotient_algebra(alg7, basis7, k_basis)
    # N is NOT contained in M = N_L(K) because [E35, E13] = -E15 not in K
    assert norm_quot.derived_entirely_in_normalizer is False
    assert _fmpz_solve_coordinates(norm_quot.normalizer_basis, e35_vec, 19) is None
    # Yet S = M/K is well-defined and S' lies inside (N intersect M)/K with class(S') <= 3
    assert norm_quot.quotient_derived_in_n_intersect_m is True
    assert norm_quot.quotient_derived_class <= 3


def test_unrolled_full_jet_solve_recovers_arbitrary_h_and_enforces_caps() -> None:
    alg7, basis7, slots7 = make_ut7_ambient_algebra(19)
    e12_idx = slots7.index((0, 1))
    e13_idx = slots7.index((0, 2))
    hidden_H = [
        tuple(int(i == e12_idx) for i in range(len(slots7))),
        tuple(int(i == e13_idx) for i in range(len(slots7))),
    ]

    def abelian_oracle(curr_alg, curr_span, curr_lift):
        lifted_span = [curr_lift(v) for v in curr_span]
        inter_root = _subspace_intersection(lifted_span, hidden_H, len(slots7), curr_alg.p)
        out = []
        for root_vec in inter_root:
            coords = _fmpz_solve_coordinates(lifted_span, root_vec, curr_alg.p)
            assert coords is not None
            out.append(
                tuple(
                    sum(coords[j] * curr_span[j][c] for j in range(len(curr_span))) % curr_alg.p
                    for c in range(curr_alg.dimension)
                )
            )
        return out

    def image_oracle(s_alg, s_derived, v_section, branch_name, s_lift):
        adapted_s = list(s_derived) + list(v_section)
        lifted_s = [s_lift(v) for v in adapted_s]
        inter_root = _subspace_intersection(lifted_s, hidden_H, len(slots7), s_alg.p)
        u_lifts = []
        for root_vec in inter_root:
            coords = _fmpz_solve_coordinates(lifted_s, root_vec, s_alg.p)
            assert coords is not None
            v_coords = coords[len(s_derived) :]
            if any(v_coords):
                u_lifts.append(
                    tuple(
                        sum(v_coords[j] * v_section[j][c] for j in range(len(v_section))) % s_alg.p
                        for c in range(s_alg.dimension)
                    )
                )
        return s_alg.span(u_lifts)

    trace = unrolled_full_jet_solve(
        alg7,
        basis7,
        abelian_hsp_oracle=abelian_oracle,
        quotient_image_oracle=image_oracle,
    )
    assert trace.status == "SUCCESS"
    assert trace.image_calls <= trace.max_allowed_image_calls == 7
    assert trace.abelian_hsp_calls <= trace.max_allowed_abelian_calls == 3
    assert False in trace.normalizer_n_in_m_flags
    assert len(trace.recovered_generators) == 2
    for h_vec in hidden_H:
        assert _fmpz_solve_coordinates(trace.recovered_generators, h_vec, 19) is not None

    # Bad image oracle that returns the entire quotient V fails the strict class-drop guard
    abort_trace = unrolled_full_jet_solve(
        alg7,
        basis7,
        abelian_hsp_oracle=abelian_oracle,
        quotient_image_oracle=lambda s_alg, s_derived, v_section, branch, lift: v_section,
    )
    assert abort_trace.status == "ABORT"
    assert abort_trace.abort_reason == "IMAGE_PREIMAGE_CLASS_DID_NOT_DROP"


def test_two_tree_resource_budget_and_sde_recurrence() -> None:
    assert ivanyos_santha_sde_arity(1, 10) == 11
    assert ivanyos_santha_sde_arity(2, 3) == 1024

    budget = class_three_full_jet_resource_budget(
        p=19,
        ambient_class=6,
        quotient_width=6,
        a_width=9,
        b_width=2,
        c_width=4,
    )
    assert budget["jet_degree_D"] == 4
    assert budget["weighted_phase_degree_e"] == 12
    assert budget["second_erasure_degrees"] == [4, 3, 2, 1]
    assert budget["log2_ordinary_tree_leaves_full_D"] > budget["log2_ordinary_tree_leaves_wrong_D_minus_1"]
    assert budget["full_jet_tree_exceeds_class_two_tree"] is True
    assert budget["max_image_calls_c_plus_1"] == 7
    assert budget["max_abelian_hsp_calls"] == 3


def test_class_four_normal_subgroup_retains_carrier_dependent_frequency_motion() -> None:
    probe = class_four_normal_frequency_motion_probe(11)
    assert probe["normal_group_class"] == 4
    assert probe["distinct_mu1_shifts_across_carrier_x0"] == 11
    assert probe["x_independent_translation_holds"] is False


def test_report_builder_invariants() -> None:
    report = build_class_three_ambient_frontend_report()
    assert report["schema_version"] == "class_three_ambient_frontend_v2"
    assert report["scope"]["accepted_speedup_candidate"] is False
    assert report["scope"]["novelty_claim"] is False
    assert report["scope"]["speedup_claim_allowed"] is False
    assert report["ut7_ambient_certification"]["derived_class"] == 3
    assert report["ut6_class_two_empty_B_certification"]["b_is_empty_class_two_branch"] is True
    assert report["ut7_unrolled_solve_recursion"]["status"] == "SUCCESS"
    assert report["class_four_normal_obstruction_control"]["x_independent_translation_holds"] is False
