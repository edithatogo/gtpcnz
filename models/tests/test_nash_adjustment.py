"""Regression controls for interpreting the teaching game's final strategy."""

from pathlib import Path

import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

from models.primarycare_model.nash_opt import PayoffMatrix, unilateral_deviation_gains


def test_asymmetric_deviation_gains() -> None:
    payoffs = PayoffMatrix(
        player0=np.array([[5.0, 0.0], [1.0, 2.0]]),
        player1=np.array([[4.0, 1.0], [0.0, 3.0]]),
    )
    assert unilateral_deviation_gains(payoffs, np.array([0.25, 0.75])) == pytest.approx((1.875, 0.375))
    assert unilateral_deviation_gains(PayoffMatrix.cooperative(), np.array([1.0, 1.0])) == (0.0, 0.0)


def test_step_convergence_is_reported_with_a_positive_deviation_gain() -> None:
    page = Path(__file__).resolve().parents[1] / "primarycare_model" / "pages" / "4_nash_convergence.py"
    app = AppTest.from_file(str(page), default_timeout=30).run()
    app.checkbox[0].uncheck()
    app.button[0].click().run()

    assert not app.exception
    result = "\n".join(markdown.value for markdown in app.markdown)
    assert "Step tolerance met:** True" in result
    assert "Unilateral payoff gains:** P0=0.0344955, P1=0.0344955" in result
    assert "**Equilibrium:**" not in result

    app.selectbox[0].select_index(1).run()
    assert not app.exception
    assert all("Unilateral payoff gains" not in markdown.value for markdown in app.markdown)
