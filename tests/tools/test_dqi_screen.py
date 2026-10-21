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
