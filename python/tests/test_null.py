"""Statistical calibration tests for latenzy and latenzy2 on data without a response."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from latenzy import latenzy, latenzy2  # noqa: E402

N_CELLS, N_TRIALS, ITI, RATE = 200, 100, 1.5, 10.0


def _poisson_cell(rng):
    T = N_TRIALS * ITI + 2
    spikes = np.sort(rng.uniform(0, T, rng.poisson(RATE * T)))
    events = 1 + np.arange(N_TRIALS) * ITI
    return spikes, events


def test_latenzy_null_false_positive_rate():
    """Constant-rate neurons should be detected at about alpha = 0.05."""
    rng = np.random.default_rng(0)
    hits = []
    for c in range(N_CELLS):
        spikes, events = _poisson_cell(rng)
        np.random.seed(c)
        hits.append(not np.isnan(latenzy(spikes, events, use_dur=[0, 1.0])[0]))
    assert 0.02 < np.mean(hits) < 0.09, f"false-positive rate {np.mean(hits):.3f}"


def test_latenzy2_null_false_positive_rate():
    """Two conditions drawn from the same constant-rate neuron should differ at about alpha = 0.05."""
    rng = np.random.default_rng(1)
    hits = []
    for c in range(N_CELLS):
        spikes, events = _poisson_cell(rng)
        np.random.seed(c)
        lat, _ = latenzy2(spikes, events[0::2], spikes, events[1::2], use_dur=[0, 1.0])
        hits.append(not np.isnan(lat))
    assert 0.02 < np.mean(hits) < 0.09, f"false-positive rate {np.mean(hits):.3f}"
