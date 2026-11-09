"""Tests for theorems/rees_blackbox_end_to_end.py (black-box chart acquisition + Rees core).

The Heisenberg group over F_5 is presented with a redundant third generator, so
the free pullback F_(3,2) -> G has a three-dimensional kernel. The tests assert
that the chart is acquired with no hiding-function query and passes its public
checks, that the Rees core then recovers H from opaque handles, and that both
negative controls are caught by a public check.
"""
from theorems import rees_blackbox_end_to_end as B


def test_free_rank_matches_witt_formula():
    for s, c in ((2, 2), (2, 3), (3, 2), (2, 4)):
        assert B.FreeNilpotent(s, c, 5).dim == B.free_rank(s, c)


def test_heisenberg_redundant_generator_end_to_end():
    out = B.run_group("heis5_s3", h_filter={"trivial", "<g0>", "<g2> (redundant gen)"},
                      negative_controls=True)
    h = out["header"]
    assert h["free_rank"] == 6 and h["chart_dim"] == 3 and h["order_G"] == 125
    assert h["kernel"]["kernel_dim"] == 3 and h["kernel_equals_true_fibre"]
    assert h["law_mass_outside_true_K_perp"] < 1e-12
    assert h["hiding_function_built_only_after_chart"]
    assert all(v is True for v in h["chart_public_checks"].values() if isinstance(v, bool))
    assert h["chart_exp_bijective_onto_G"]
    assert len(out["runs"]) == 3
    for row in out["runs"]:
        assert row["recovered_equals_log_H"] and row["blackbox_subgroup_recovered"]
        assert row["oracle_partition_matches_truth"]
        assert row["every_stage_output_equals_rho_H_d"] and row["queries_equal_charged"]
    neg = out["negative_controls"]
    assert neg["naive_pullback"]["checks"]["chart_exp_homomorphism"] is False
    assert neg["one_sample"]["caught_by_las_vegas_check"]


def test_strict_subkernel_is_not_caught_by_public_checks():
    """Limitation, recorded on purpose: a K' strictly inside K (here K cap gamma_2(F),
    forced from the true kernel, as an approximate Fourier transform could return)
    passes the Las Vegas check and every chart public check, because Phi still factors
    through F/K' as a homomorphism. Only the grading-side bijectivity test sees it."""
    r = B.strict_subkernel_control("heis5_s3")
    assert r["applicable"] and r["true_kernel_dim"] == 3 and r["subkernel_dim"] == 2
    assert r["las_vegas_rejected_vectors"] == 0
    assert all(v is True for v in r["checks"].values() if isinstance(v, bool))
    assert r["checks"]["homomorphism_check"].startswith("exhaustive")
    assert r["caught_by_public_checks"] is False
    assert r["chart_dim"] == 4 and r["chart_points"] == 625 and r["chart_exp_image_size"] == 125
    assert r["chart_exp_bijective_onto_G"] is False


def test_batched_oracle_matches_loop_and_counts_calls():
    for name in ("heis5_s3", "free23_5"):
        p, spec, mats, c = B.catalogue()[name]
        box = B.BlackBox(p, spec, mats, 1)
        g = box.generators
        xs = [g[0], g[1], box.identity, g[0]]
        ys = [g[1], g[0], g[1], g[0]]
        loop = [box.mul(x, y) for x, y in zip(xs, ys)]
        calls = box.calls
        assert list(box.mul_batch(xs, ys)) == loop and box.calls == calls+len(xs)


def test_ut5_generators_are_class_three_of_order_5_to_the_5():
    import numpy as np
    p, spec, mats, c = B.catalogue()["ut5_5"]
    assert spec == ("matrix", 5) and c == 3
    box = B.BlackBox(p, spec, mats, 1)
    assert len(box.closure(box.generators)) == 5**5
    # Lie side: X = log g0, Y = log g1 (g - I nilpotent; log by the finite series mod 5)
    def log(m):
        N = (np.array(m).reshape(5, 5)-np.eye(5, dtype=np.int64)) % p
        out, P = np.zeros((5, 5), dtype=np.int64), np.eye(5, dtype=np.int64)
        for k in range(1, 5):
            P = P @ N % p
            out = (out+(-1)**(k+1)*P*pow(k, -1, p)) % p
        return out
    X, Y = (log(m) for m in mats)
    br = lambda a, b: (a @ b-b @ a) % p
    xy = br(X, Y)
    deg3 = [br(X, xy), br(Y, xy)]
    assert all(m.any() for m in deg3)
    assert not any(br(a, b).any() for a in (X, Y) for b in deg3)
