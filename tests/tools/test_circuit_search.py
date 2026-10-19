from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from tools.circuit_search import dcp_readout as dr

MOD64 = ([2 * math.pi * 16 / 64, 2 * math.pi * 17 / 64], [1.0, 1.0])


def test_reproduces_the_three_recorded_scores() -> None:
    thetas, gammas = MOD64
    h0, h1 = dr.known_secret_hypotheses(thetas, gammas)
    assert dr.x_basis_tv(thetas, gammas) == pytest.approx(0.7745042850823902, abs=1e-12)
    assert dr.local_helstrom_product_tv(thetas, gammas) == pytest.approx(0.7409511253549592, abs=1e-12)
    assert dr.collective_tv(h0, h1) == pytest.approx(0.880059250893024, abs=1e-12)


def test_product_tv_with_x_directions_matches_x_basis_score() -> None:
    thetas, gammas = MOD64
    h0, h1 = dr.known_secret_hypotheses(thetas, gammas)
    x = [dr.direction(math.pi / 2, 0.0)] * 2
    assert dr.product_tv(h0, h1, x) == pytest.approx(dr.x_basis_tv(thetas, gammas), abs=1e-12)


def test_adaptive_tree_without_adaptation_equals_product() -> None:
    thetas, gammas = MOD64
    h0, h1 = dr.known_secret_hypotheses(thetas, gammas)
    n1, n2 = dr.direction(1.0, 0.3), dr.direction(0.7, 2.0)
    tree = {(): n1, (1,): n2, (-1,): n2}
    assert dr.adaptive_tv(h0, h1, tree, order=(0, 1)) == pytest.approx(dr.product_tv(h0, h1, [n1, n2]), abs=1e-12)


def test_circuit_simulation_matches_analytic_outcome_law() -> None:
    thetas, gammas = [0.9, 2.1], [0.8, 0.6]
    h0, _ = dr.known_secret_hypotheses(thetas, gammas)
    rng = np.random.default_rng(3)
    tree = {(): dr.direction(*rng.uniform(0, 3, 2)), (1,): dr.direction(*rng.uniform(0, 3, 2)), (-1,): dr.direction(*rng.uniform(0, 3, 2))}
    analytic = dr.adaptive_distribution(h0, tree, order=(1, 0))
    simulated = dr.simulate_adaptive_circuit(dr.density_matrix(h0), tree, order=(1, 0))
    for outcome, p in analytic.items():
        assert simulated[outcome] == pytest.approx(p, abs=1e-12)


def test_adaptive_search_reaches_helstrom_for_two_pure_product_states() -> None:
    rng = np.random.default_rng(11)
    thetas = list(rng.uniform(0.2, 3.0, 2))
    h0, h1 = dr.known_secret_hypotheses(thetas, [1.0, 1.0])
    best = dr.search_adaptive(h0, h1, restarts=12, seed=0)
    assert best.tv == pytest.approx(dr.collective_tv(h0, h1), abs=1e-6)


def test_bounds_are_ordered_on_mixed_packets() -> None:
    h0, h1 = dr.known_secret_hypotheses([0.785, 1.047, 2.094], [0.85, 0.8, 0.75])
    product = dr.search_product(h0, h1, restarts=6, seed=0).tv
    adaptive = dr.search_adaptive(h0, h1, restarts=6, seed=0).tv
    collective = dr.collective_tv(h0, h1)
    assert product <= adaptive + 1e-9 <= collective + 2e-9


def test_sign_symmetrized_hypothesis_is_a_mixture() -> None:
    h0, h1 = dr.unknown_sign_hypotheses([0.5, 1.0], [1.0, 1.0])
    assert len(h0) == 1 and len(h1) == 2
    assert sum(w for w, _ in h1) == pytest.approx(1.0)


def test_partial_transpose_detects_entanglement() -> None:
    bell = np.zeros((4, 4))
    bell[0, 0] = bell[0, 3] = bell[3, 0] = bell[3, 3] = 0.5
    assert np.linalg.eigvalsh(dr.partial_transpose(bell, [1], 2)).min() == pytest.approx(-0.5)
    product = np.kron(np.diag([0.7, 0.3]), np.diag([0.4, 0.6]))
    assert np.allclose(dr.partial_transpose(product, [0], 2), product)


def test_ppt_bound_equals_collective_for_two_pure_product_states() -> None:
    pytest.importorskip("cvxpy")
    h0, h1 = dr.known_secret_hypotheses(*MOD64)
    assert dr.ppt_tv(h0, h1) == pytest.approx(dr.collective_tv(h0, h1), abs=1e-6)


def test_ppt_bound_sits_between_adaptive_and_collective_for_unknown_sign() -> None:
    pytest.importorskip("cvxpy")
    h0, h1 = dr.unknown_sign_hypotheses(*MOD64)
    adaptive = dr.search_adaptive(h0, h1, restarts=4, seed=0).tv
    bound = dr.ppt_tv(h0, h1)
    assert adaptive <= bound + 1e-6
    assert bound <= dr.collective_tv(h0, h1) + 1e-6


def test_ppt_dual_certificate_is_tight_and_valid() -> None:
    pytest.importorskip("cvxpy")
    h0, h1 = dr.known_secret_hypotheses([0.785, 1.047, 2.094], [0.85, 0.8, 0.75])
    bound = dr.ppt_bound(h0, h1)
    assert bound["primal"] <= bound["upper"] + 1e-9
    assert bound["upper"] - bound["primal"] < 1e-5
    assert bound["upper"] < dr.collective_tv(h0, h1) - 1e-3
    rng = np.random.default_rng(5)
    for _ in range(5):
        dirs = [dr.direction(*rng.uniform(0, 3, 2)) for _ in range(3)]
        assert dr.product_tv(h0, h1, dirs) <= bound["upper"] + 1e-12


def test_cli_writes_results(tmp_path: Path) -> None:
    out = tmp_path / "result.json"
    assert dr.main(["--out", str(out), "--restarts", "3", "--instances", "mod64"]) == 0
    data = json.loads(out.read_text())
    row = data["instances"][0]
    assert row["name"] == "mod64" and row["known_secret"]["collective"] == pytest.approx(0.880059250893024, abs=1e-12)
    assert "best_adaptive" in row["known_secret"] and data["seed"] == 0
    if dr.ppt_bound(*dr.known_secret_hypotheses(*MOD64)) is not None:
        assert row["unknown_sign"]["ppt_upper"] == pytest.approx(row["unknown_sign"]["collective"], abs=1e-5)
        assert row["known_secret"]["certified_local_gap"] == pytest.approx(0.0, abs=1e-6)
        assert "PPT bound" in (tmp_path / "CIRCUIT_SEARCH_DCP_READOUT.md").read_text()
