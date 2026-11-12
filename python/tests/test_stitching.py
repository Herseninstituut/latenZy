"""Regression tests for data stitching in get_pseudo_times (v1.1.1 fix).

Before v1.1.1, windows with use_dur[0] < 0 were treated as overlapping whenever
use_dur[1] + 2*|use_dur[0]| > ISI, so the edges of neighbouring windows were
counted twice and constant-rate neurons were detected as responsive.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dependencies import get_pseudo_times, get_rel_spike_times  # noqa: E402
from latenzy import latenzy  # noqa: E402


@pytest.mark.parametrize("use_dur", [[0, 0.8], [-0.3, 0.5], [-0.1, 0.5], [-0.45, 0.5], [0, 1.3]])
@pytest.mark.parametrize("isi_jitter", [0.0, 0.3])
def test_stitching_preserves_aligned_spikes(use_dur, isi_jitter):
    """Event-aligned spikes must be identical with and without stitching."""
    rng = np.random.default_rng(0)
    events = 1 + np.cumsum(1.0 + isi_jitter * rng.uniform(-1, 1, 60))
    spikes = np.sort(rng.uniform(0, events[-1] + 2, 6000))
    ps, pe = get_pseudo_times(spikes, events, use_dur, discard_edges=True)
    _, raw = get_rel_spike_times(spikes, events, use_dur)
    _, stitched = get_rel_spike_times(ps, pe, use_dur)
    for r, s in zip(raw, stitched):
        np.testing.assert_allclose(np.sort(r), np.sort(s), atol=1e-9)


def test_latenzy_null_negative_window():
    """Constant-rate neurons with a pre-event window should be detected at about alpha."""
    hits = []
    for c in range(100):
        rng = np.random.default_rng(c)
        events = 1 + np.arange(100) * 1.0
        spikes = np.sort(rng.uniform(0, 102, rng.poisson(10 * 102)))
        np.random.seed(c)
        hits.append(not np.isnan(latenzy(spikes, events, use_dur=[-0.3, 0.5])[0]))
    assert np.mean(hits) < 0.12, f"false-positive rate {np.mean(hits):.3f}"
