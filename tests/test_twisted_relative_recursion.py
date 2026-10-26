"""Tests for theorems/twisted_relative_recursion.py (Milestone 18)."""
from __future__ import annotations

import json
import pytest

from theorems.class_three_ambient_frontend import _subspace_contains, _subspace_intersection
from theorems.class_three_monomial_jet import ClassThreeStructure, FullTaylorJetChart
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra, _fmpz_solve_coordinates
from theorems.twisted_relative_recursion import (
    JSON_PATH,
    MD_PATH,
    _strict_upper_triangular_lie_algebra,
    build_twisted_relative_recursion_report,
    compile_relative_abelian_twisted_leaf,
    compile_twisted_full_jet_leaf,
    learn_known_subalgebra_character_from_original_copies,
    public_character_normalizer_quotient,
    relative_quotient_algebra,
    render_markdown,
    twisted_image_call_bound,
    unrolled_twisted_relative_solve,
    verify_character_attached_weighted_cascade,
    verify_relative_abelian_quadratic_phase_erasure,
)
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket


def _heisenberg(p: int) -> PublicLieAlgebra:
    return PublicLieAlgebra(
        p=p,
        dimension=3,
        bracket_fn=lambda a, b: (0, 0, (a[0] * b[1] - a[1] * b[0]) % p),
    )


def test_twisted_image_call_bound_matches_section_8_recurrence() -> None:
    assert twisted_image_call_bound(0) == 0
    assert twisted_image_call_bound(1) == 1
    assert twisted_image_call_bound(2) == 3
    assert twisted_image_call_bound(3) == 4
    assert twisted_image_call_bound(4) == 7
    assert twisted_image_call_bound(5) == 8
    for c in range(4, 10):
        assert twisted_image_call_bound(c) <= c + 4
    for c in range(6, 10):
        assert twisted_image_call_bound(c) == c + 4
    with pytest.raises(ValueError, match="nonnegative"):
        twisted_image_call_bound(-1)


def test_relative_quotient_algebra_validates_scalar_center() -> None:
    p = 11
    heis = _heisenberg(p)
    std3 = [tuple(int(i == j) for j in range(3)) for i in range(3)]
    # Z = <z> is central of dim 1; Q = Heis / Z is 2D abelian (class 1)
    q_alg, sec, q_class = relative_quotient_algebra(heis, std3, [std3[2]])
    assert q_alg.dimension == 2
    assert len(sec) == 2
    assert q_class == 1

    # Noncentral Z = <x> must be rejected
    with pytest.raises(ValueError, match="central"):
        relative_quotient_algebra(heis, std3, [std3[0]])

    # Z of dimension 2 (<y, z>) must be rejected
    with pytest.raises(ValueError, match="dimension 0 or 1"):
        relative_quotient_algebra(heis, std3, [std3[1], std3[2]])


@pytest.mark.parametrize("p", [7, (1 << 127) - 1])
def test_character_normalizer_quotient_heisenberg_small_and_127bit(p: int) -> None:
    heis = _heisenberg(p)
    std3 = [tuple(int(i == j) for j in range(3)) for i in range(3)]
    k_basis = [std3[1], std3[2]]  # <y, z>
    chi_k = (3, 1)
    cnq = public_character_normalizer_quotient(
        heis,
        std3,
        k_basis,
        chi_k,
        prior_z_basis=[std3[2]],
        prior_z_character=(1,),
    )
    assert len(cnq.plain_normalizer_basis_in_ambient) == 3
    assert len(cnq.m_chi_basis_in_ambient) == 2
    assert len(cnq.k0_kernel_basis_in_ambient) == 1
    assert cnq.scalar_center_width == 1
    assert cnq.m_chi_strictly_smaller_than_plain_normalizer is True
    assert cnq.k0_ideal_in_plain_normalizer is False
    assert cnq.k0_ideal_in_m_chi is True
    assert cnq.z_new_central_in_quotient is True
    assert cnq.relative_quotient_class == 0

    # Lift and project round-trip inside M_chi modulo K_0
    s_vec = (1,)
    lifted = cnq.lift_to_ambient(s_vec)
    assert cnq.project_from_m_chi(lifted) == s_vec

    # Vector x outside M_chi is rejected by project_from_m_chi
    with pytest.raises(ValueError, match="does not lie in M_chi"):
        cnq.project_from_m_chi(std3[0])


def test_character_normalizer_quotient_rejects_inconsistent_prior_z() -> None:
    p = 7
    heis = _heisenberg(p)
    std3 = [tuple(int(i == j) for j in range(3)) for i in range(3)]
    # Prior Z = <z> has character (2,), while chi_k on <y, z> gives 1 on z
    with pytest.raises(ValueError, match="disagrees"):
        public_character_normalizer_quotient(
            heis,
            std3,
            [std3[1], std3[2]],
            (3, 1),
            prior_z_basis=[std3[2]],
            prior_z_character=(2,),
        )
    # Prior Z = <x> not contained in K = <y, z>
    with pytest.raises(ValueError, match="contained in learned K"):
        public_character_normalizer_quotient(
            heis,
            std3,
            [std3[1], std3[2]],
            (3, 1),
            prior_z_basis=[std3[0]],
            prior_z_character=(1,),
        )


def test_learn_known_subalgebra_character_from_original_copies_checks_commutator() -> None:
    p = 11
    heis = _heisenberg(p)
    std3 = [tuple(int(i == j) for j in range(3)) for i in range(3)]
    # On abelian K = <y, z>, any linear values are valid
    vals, copies = learn_known_subalgebra_character_from_original_copies(
        heis,
        [std3[1], std3[2]],
        lambda v: (4 * v[1] + 5 * v[2]) % p,
    )
    assert vals == (4, 5)
    assert copies == 2

    # On full Heis_3 = <x, y, z>, [x, y] = z, so character with nonzero value on z must be rejected
    with pytest.raises(ValueError, match="vanish on \\[K, K\\]"):
        learn_known_subalgebra_character_from_original_copies(
            heis,
            std3,
            lambda v: v[2] % p,
        )


def test_relative_abelian_quadratic_phase_erasure_and_no_evaluate_fixture(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _forbidden_eval(*args: object, **kwargs: object) -> None:
        raise AssertionError("evaluate_fixture must never be called during erasure")

    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", _forbidden_eval)

    leaf = compile_relative_abelian_twisted_leaf(7, 2, [1, 2], [[1, 3], [2, 4]], [1, 3])
    assert leaf.jet_width == 0
    assert leaf.degree == 2

    audit = verify_relative_abelian_quadratic_phase_erasure(p=7, slope_a=2, char_b=1)
    assert audit["naive_fourier_mass_outside_annihilator"] == pytest.approx(6.0 / 7.0)
    assert audit["erased_packet_final_degree"] == 0
    assert audit["erased_fourier_mass_outside_annihilator"] == pytest.approx(0.0)
    assert audit["erased_fourier_mass_inside_annihilator"] == pytest.approx(1.0)


def test_character_attached_weighted_cascade_erases_character_at_weight_one(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _forbidden_eval(*args: object, **kwargs: object) -> None:
        raise AssertionError("evaluate_fixture must never be called during weighted cascade")

    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", _forbidden_eval)

    audit = verify_character_attached_weighted_cascade(p=23, quotient_width=1)
    assert audit["twisted_parameter_count"] == audit["base_parameter_count"] + 1
    assert audit["character_term_weights"] == [1]
    assert audit["erased_root_weighted_degree"] == 0
    assert audit["post_fourier_residual_contains_character_params"] is False

    # Also test compile_twisted_full_jet_leaf wrapper directly
    p = 11
    st = ClassThreeStructure(
        p,
        (((0, 1), (p - 1, 0)),),
        (((0, 0), (0, 0)), ((0, 0), (0, 0))),
        (((1,), (0,)), ((0,), (0,))),
    )
    chart = FullTaylorJetChart(p=p, quotient_width=1, noncentral_width=2, degree=2)
    pinned = compile_twisted_full_jet_leaf(
        instance_id="inst-1",
        chart_id="chart-1",
        chart=chart,
        structure=st,
        labels=[(3, 2)] * 6,
        scales=[1, 1, 2, 2, 3, 3],
        outcomes=[(0,), (1,), (0,), (1,), (0,), (1,)],
        tensor_powers=[1, 2, 1, 2, 1, 2],
        ambient_class=4,
    )
    assert pinned.weighted_degree <= 6
    assert not pinned.consumed


def test_unrolled_twisted_relative_solve_recovers_ut7_subgroup_and_character() -> None:
    p = 19
    ut7, idx7 = _strict_upper_triangular_lie_algebra(7, p)
    std7 = [tuple(int(i == j) for j in range(ut7.dimension)) for i in range(ut7.dimension)]
    target_H = ut7.span([std7[idx7[(0, 3)]], std7[idx7[(1, 3)]], std7[idx7[(4, 5)]]])
    ell_amb = [0] * ut7.dimension
    ell_amb[idx7[(0, 3)]] = 5
    ell_amb[idx7[(1, 3)]] = 2
    ell_amb[idx7[(4, 5)]] = 7

    def char_oracle(amb_vec: tuple[int, ...]) -> int:
        assert _subspace_contains(target_H, [amb_vec], p)
        return sum(c * l_val for c, l_val in zip(amb_vec, ell_amb)) % p

    def rel_base_oracle(s_alg, z_basis, q_section, z_char, lift_fn):
        s_span = s_alg.span(list(z_basis) + list(q_section))
        L_lifts = [lift_fn(v) for v in s_span]
        inter_L = _subspace_intersection(target_H, L_lifts, ut7.dimension, p)
        out = []
        for vec_L in inter_L:
            coords = _fmpz_solve_coordinates(L_lifts, vec_L, p)
            assert coords is not None
            out.append(
                tuple(
                    sum(coords[i] * s_span[i][c] for i in range(len(s_span))) % p
                    for c in range(s_alg.dimension)
                )
            )
        return s_alg.span(out)

    def twisted_img_oracle(s_alg, n_s_basis, v_section, z_basis, z_char, branch_name, lift_fn):
        curr_s_span = s_alg.span(list(n_s_basis) + list(v_section))
        L_lifts = [lift_fn(v) for v in curr_s_span]
        inter_L = _subspace_intersection(target_H, L_lifts, ut7.dimension, p)
        adapted = list(n_s_basis) + list(v_section)
        n_dim = len(n_s_basis)
        v_proj = []
        for vec_L in inter_L:
            coords_s = _fmpz_solve_coordinates(L_lifts, vec_L, p)
            assert coords_s is not None
            h_vec = tuple(
                sum(coords_s[i] * curr_s_span[i][c] for i in range(len(curr_s_span))) % p
                for c in range(s_alg.dimension)
            )
            coords = _fmpz_solve_coordinates(adapted, h_vec, p)
            assert coords is not None
            v_vec = tuple(
                sum(coords[n_dim + j] * v_section[j][c] for j in range(len(v_section))) % p
                for c in range(s_alg.dimension)
            )
            if any(v_vec):
                v_proj.append(v_vec)
        return s_alg.span(v_proj)

    trace = unrolled_twisted_relative_solve(
        ut7,
        std7,
        single_copy_character_oracle=char_oracle,
        relative_abelian_base_oracle=rel_base_oracle,
        twisted_image_oracle=twisted_img_oracle,
        recover_final_bose_kernel=True,
    )
    assert trace.status == "SUCCESS"
    assert trace.image_and_base_calls <= trace.max_allowed_image_and_base_calls
    assert trace.character_learning_batches == 3  # 2 recursion nodes + 1 final H character
    assert list(trace.recovered_generators) == target_H
    assert trace.recovered_character_on_generators == (5, 2, 7)
    assert any(trace.m_chi_strict_shrink_flags)


def test_unrolled_twisted_relative_solve_aborts_on_noncommuting_relative_base() -> None:
    p = 11
    heis = _heisenberg(p)
    std3 = [tuple(int(i == j) for j in range(3)) for i in range(3)]
    # Start at r = 1: G = Heis_3, Z = <z>, chi_Z = (1,).
    # If a buggy relative abelian base returns BOTH x and y, [x, y] = z != 0 on faithful Z, which must ABORT!
    trace = unrolled_twisted_relative_solve(
        heis,
        std3,
        single_copy_character_oracle=lambda v: v[2] % p,
        relative_abelian_base_oracle=lambda s_alg, z_basis, q_sec, z_char, lift_fn: list(q_sec),
        twisted_image_oracle=lambda *args: [],
        initial_z_basis=[std3[2]],
        initial_z_character=(1,),
    )
    assert trace.status == "ABORT"
    assert trace.abort_reason == "RELATIVE_BASE_OUTPUT_NON_COMMUTING_ON_FAITHFUL_Z"


def test_unrolled_twisted_relative_solve_aborts_on_class_four_derived() -> None:
    p = 23
    ut9, _ = _strict_upper_triangular_lie_algebra(9, p)
    std9 = [tuple(int(i == j) for j in range(ut9.dimension)) for i in range(ut9.dimension)]
    # ut_9 has class 8, and N = [ut_9, ut_9] has class 4 > 3 -> must ABORT!
    trace = unrolled_twisted_relative_solve(
        ut9,
        std9,
        single_copy_character_oracle=lambda v: 0,
        relative_abelian_base_oracle=lambda *args: [],
        twisted_image_oracle=lambda *args: [],
    )
    assert trace.status == "ABORT"
    assert trace.abort_reason == "UNDERLYING_N_CLASS_EXCEEDS_THREE"


def test_written_artifacts_match_report_schema() -> None:
    report = build_twisted_relative_recursion_report()
    assert report["schema_version"] == "twisted_relative_recursion_v1"
    assert report["scope"]["accepted_speedup_candidate"] is False
    assert report["scope"]["novelty_claim"] is False
    assert report["scope"]["speedup_claim_allowed"] is False
    md = render_markdown(report)
    assert "Relative Scalar-Center Twisted Recursion" in md
    if JSON_PATH.exists():
        on_disk = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert on_disk["schema_version"] == "twisted_relative_recursion_v1"
    if MD_PATH.exists():
        assert "accepted_speedup_candidate" in MD_PATH.read_text(encoding="utf-8")
