from __future__ import annotations

import pytest

from tools.dqi_screen import rules as R


def test_objective_and_threshold_hand_values() -> None:
    a = 39 / 127
    assert R.q_prange(a, 0.5) == pytest.approx(0.654, abs=5e-4)
    assert R.q_dqi(19 / 127, 0.5) == pytest.approx(0.857, abs=5e-4)
    assert R.q_dqi(0.9, 0.5) == 1.0
    assert R.lambda_crit(a, 0.5) == pytest.approx(0.024, abs=5e-4)
    assert R.lambda_crit(0.5, 0.5) == pytest.approx(0.067, abs=5e-4)
    assert R.rho_crit(0.5) == pytest.approx(0.092, abs=5e-4)
    assert R.lambda_crit(0.5, R.rho_crit(0.5)) == pytest.approx(0.25)  # rho_crit: lambda_crit meets alpha/2
    for bad in ((0.0, 0.5), (0.3, 1.0), (1.2, 0.5)):
        with pytest.raises(ValueError):
            R.q_prange(*bad)


A = 39 / 127


def test_reach_bounds_caps_and_cosine() -> None:
    a = A
    assert R.licensed_radius(40) == 19
    assert R.singleton_reach(a) == pytest.approx(0.154, abs=5e-4)
    assert R.distance_reach(40 / 127) == pytest.approx(20 / 127)
    assert R.sphere_packing_reach(a, 2**61 - 1) == pytest.approx(0.293, abs=5e-4)
    assert R.q_ary_entropy(R.q_ary_entropy_inverse(0.3, 7), 7) == pytest.approx(0.3, abs=1e-9)
    assert R.plotkin_reach(0.5, 2) == pytest.approx(0.125)
    assert R.margin_cap(a) == pytest.approx(0.207, abs=5e-4)
    assert R.margin_cap(0.5) == pytest.approx(0.183, abs=5e-4)
    assert R.margin_cap(1 - 1 / 2**0.5) == pytest.approx(R.UNIVERSAL_CAP, abs=1e-9)
    assert R.cosine_objective(209 / 6000) == pytest.approx(0.367, abs=5e-4)
    assert R.lambda_crit_cos(0.07) == pytest.approx(0.00246, abs=5e-6)
    assert R.lambda_crit_cos(0.8) is None


def test_restarts_and_subfield_hand_values() -> None:
    a = A
    assert R.restart_length(a, 0.816830 - R.q_prange(a, 0.5), 1) == pytest.approx(399.2, abs=0.1)
    assert R.existential_line(0.5, 0.5, 2**61 - 1) == 1.0
    assert R.existential_line(0.2, 0.5, 7) == pytest.approx(0.909, abs=5e-4)
    assert R.subfield_rate(0.3, 2, 1) == pytest.approx(0.6)
    assert R.subfield_baseline(0.5, 0.6, 100) == pytest.approx(0.8)
    assert R.subfield_blocks_at_half(0.5, 2, 1) is True and R.subfield_blocks_at_half(0.3, 2, 1) is False
