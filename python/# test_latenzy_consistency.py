# test_latenzy_consistency.py
import numpy as np
import scipy.io as sio
import os
from latenzy import latenzy

# Force deterministic behavior
np.random.seed(1)

# Load example MATLAB data
data_path = os.path.join(os.path.dirname(__file__), '..', 'example_data')
mat_data = sio.loadmat(os.path.join(data_path, 'Topo2_20220126_AP.mat'), struct_as_record=False, squeeze_me=True)
sAP = mat_data['sAP']

# Apply inclusion criteria
clusters = sAP.sCluster
n_clusters = len(clusters)

is_good = np.zeros(n_clusters, dtype=bool)
low_contam = np.zeros(n_clusters, dtype=bool)
in_primary_visual = np.zeros(n_clusters, dtype=bool)

for i, c in enumerate(clusters):
    is_good[i] = c.KilosortGood
    low_contam[i] = c.Contamination < 0.1

    # Handle Area field exactly like MATLAB
    area_str = getattr(c, 'Area', '')
    if isinstance(area_str, str):
        in_primary_visual[i] = 'primary visual' in area_str.lower()
    elif isinstance(area_str, (np.str_, np.strc)):
        in_primary_visual[i] = 'primary visual' in str(area_str).lower()
    elif isinstance(area_str, (list, np.ndarray)) and len(area_str) > 0:
        in_primary_visual[i] = 'primary visual' in str(area_str[0]).lower()
    else:
        in_primary_visual[i] = False

# Combine inclusion criteria
idx_incl = (is_good | low_contam) & in_primary_visual

# Extract spike times for included clusters
spike_times_agg = [c.SpikeTimes for i, c in enumerate(clusters) if idx_incl[i]]

# Get event times (Python [3] = MATLAB {4})
event_times = sAP.cellBlock[3].vecStimOnTime

# Use 16th included cluster (Python index 16 = MATLAB 17)
spike_times = spike_times_agg[15]

# Run latenzy with deterministic resampling
latency, s_latenzy = latenzy(
    spike_times, event_times,
    use_dur=1,
    resamp_num=100,
    jitter_size=2,
    peak_alpha=0.05,
    do_stitch=True,
    use_par_pool=False,
    use_direct_quant=False,
    restrict_neg=True,
    make_plots=0
)

# Display results
print("Python latenzy output:")
print("Latency:", latency)
print("p-values:", s_latenzy['pValsPeak'])
